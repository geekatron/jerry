"""End-to-end tests for Session Start Hook.

These tests validate the complete flow from script invocation to output,
including real filesystem operations and environment variable handling.

IMPORTANT: Tests MUST be run via uv to validate plugin execution model:

    uv run pytest tests/session_management/e2e/test_session_start.py

Do NOT use: python -m pytest (bypasses uv dependency management)
See: DISC-008 for rationale.

Test Categories:
    - Happy Path: Valid project scenarios
    - Edge Cases: Boundary conditions and special cases
    - Negative: Invalid input scenarios
    - Failure Scenarios: Error handling paths
    - Output Format: Structured output validation

References:
    - ENFORCE-011: E2E Tests
    - src/interface/cli/session_start.py: Entry point (PEP 723 inline deps)
    - DISC-007: Tests updated after BUG-007 fix
    - DISC-008: Must use uv run for test execution
"""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest

# Mark entire module as subprocess tests (requires uv)
# These tests run session_start.py via subprocess using uv run
pytestmark = [
    pytest.mark.subprocess,
]

# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def temp_root_dir() -> Generator[str, None, None]:
    """Create a temporary root directory with projects/ subdirectory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        projects_dir = Path(tmpdir) / "projects"
        projects_dir.mkdir()
        yield tmpdir


@pytest.fixture
def temp_projects_dir(temp_root_dir: str) -> str:
    """Get the projects directory within the temp root."""
    return str(Path(temp_root_dir) / "projects")


@pytest.fixture
def project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent.parent


@pytest.fixture
def session_start_script(project_root: Path) -> Path:
    """Get path to the session_start.py script.

    Note: After BUG-007 fix, script moved from scripts/ to src/interface/cli/
    and now uses PEP 723 inline metadata for dependency management.
    """
    return project_root / "src" / "interface" / "cli" / "session_start.py"


def create_project(
    base_path: str,
    project_id: str,
    status: str = "IN_PROGRESS",
    has_plan: bool = True,
    has_tracker: bool = True,
) -> Path:
    """Create a project directory with optional files.

    Args:
        base_path: Parent directory for the project
        project_id: Full project ID (e.g., "PROJ-001-test")
        status: Status string for WORKTRACKER.md
        has_plan: Whether to create PLAN.md
        has_tracker: Whether to create WORKTRACKER.md

    Returns:
        Path to the created project directory
    """
    proj_dir = Path(base_path) / project_id
    proj_dir.mkdir(parents=True)

    if has_plan:
        (proj_dir / "PLAN.md").write_text("# Plan\n\nProject plan content.")

    if has_tracker:
        (proj_dir / "WORKTRACKER.md").write_text(f"# Work Tracker\n\nStatus: {status}")

    return proj_dir


def run_session_start(
    script_path: Path,
    env_vars: dict | None = None,
    project_root: Path | None = None,
) -> tuple[int, str, str]:
    """Run the session_start.py script via uv run.

    IMPORTANT: Uses uv run to validate plugin execution model (DISC-008).
    Never use sys.executable directly - bypasses uv dependency management.

    Args:
        script_path: Path to the session_start.py script
        env_vars: Additional environment variables to set
        project_root: Project root for PYTHONPATH (required for local imports)

    Returns:
        Tuple of (exit_code, stdout, stderr)
    """
    env = os.environ.copy()
    if env_vars:
        env.update(env_vars)

    # Set PYTHONPATH to project root for "from src.X" imports (DISC-005)
    # Script uses absolute imports like "from src.infrastructure..."
    if project_root:
        existing_pythonpath = env.get("PYTHONPATH", "")
        env["PYTHONPATH"] = (
            f"{project_root}:{existing_pythonpath}" if existing_pythonpath else str(project_root)
        )

    result = subprocess.run(
        ["uv", "run", str(script_path)],
        capture_output=True,
        text=True,
        env=env,
        cwd=str(project_root) if project_root else None,
    )

    return result.returncode, result.stdout, result.stderr


# =============================================================================
# Happy Path Tests (6 tests)
# =============================================================================


class TestSessionStartHappyPath:
    """Happy path E2E tests for session start hook."""

    def test_valid_project_outputs_project_context(
        self, temp_projects_dir: str, session_start_script: Path, project_root: Path
    ) -> None:
        """Valid JERRY_PROJECT should output <project-context> tag."""
        create_project(temp_projects_dir, "PROJ-001-test")

        exit_code, stdout, _ = run_session_start(
            session_start_script,
            {
                "JERRY_PROJECT": "PROJ-001-test",
                "CLAUDE_PROJECT_DIR": str(Path(temp_projects_dir).parent),
            },
            project_root=project_root,
        )

        assert exit_code == 0
        assert "<project-context>" in stdout
        assert "ProjectActive: PROJ-001-test" in stdout
        assert "</project-context>" in stdout

    def test_valid_project_shows_validation_success(
        self, temp_projects_dir: str, session_start_script: Path, project_root: Path
    ) -> None:
        """Valid project with all files shows success validation."""
        create_project(temp_projects_dir, "PROJ-002-complete")

        exit_code, stdout, _ = run_session_start(
            session_start_script,
            {
                "JERRY_PROJECT": "PROJ-002-complete",
                "CLAUDE_PROJECT_DIR": str(Path(temp_projects_dir).parent),
            },
            project_root=project_root,
        )

        assert exit_code == 0
        assert "ValidationMessage: Project is properly configured" in stdout

    def test_no_project_set_shows_project_required(
        self, temp_projects_dir: str, session_start_script: Path, project_root: Path
    ) -> None:
        """No JERRY_PROJECT should output <project-required> tag."""
        create_project(temp_projects_dir, "PROJ-001-available")

        # Clear JERRY_PROJECT if set
        env = {"CLAUDE_PROJECT_DIR": str(Path(temp_projects_dir).parent)}
        env["JERRY_PROJECT"] = ""  # Explicitly clear

        exit_code, stdout, _ = run_session_start(
            session_start_script, env, project_root=project_root
        )

        assert exit_code == 0
        assert "<project-required>" in stdout
        assert "ProjectRequired: true" in stdout
        assert "</project-required>" in stdout

    def test_no_projects_available_shows_empty_list(
        self, temp_projects_dir: str, session_start_script: Path, project_root: Path
    ) -> None:
        """Empty projects directory shows no projects message."""
        env = {
            "JERRY_PROJECT": "",
            "CLAUDE_PROJECT_DIR": str(Path(temp_projects_dir).parent),
        }

        exit_code, stdout, _ = run_session_start(
            session_start_script, env, project_root=project_root
        )

        assert exit_code == 0
        assert "(no projects found)" in stdout
        assert "NextProjectNumber: 001" in stdout

    def test_multiple_projects_lists_all(
        self, temp_projects_dir: str, session_start_script: Path, project_root: Path
    ) -> None:
        """Multiple projects are listed with status icons."""
        create_project(temp_projects_dir, "PROJ-001-first", status="IN_PROGRESS")
        create_project(temp_projects_dir, "PROJ-002-second", status="COMPLETED")
        create_project(temp_projects_dir, "PROJ-003-third", status="DRAFT")

        env = {
            "JERRY_PROJECT": "",
            "CLAUDE_PROJECT_DIR": str(Path(temp_projects_dir).parent),
        }

        exit_code, stdout, _ = run_session_start(
            session_start_script, env, project_root=project_root
        )

        assert exit_code == 0
        assert "PROJ-001-first" in stdout
        assert "PROJ-002-second" in stdout
        assert "PROJ-003-third" in stdout
        assert "[ACTIVE]" in stdout
        assert "[DONE]" in stdout
        assert "[DRAFT]" in stdout

    def test_next_project_number_increments(
        self, temp_projects_dir: str, session_start_script: Path, project_root: Path
    ) -> None:
        """Next project number is max + 1."""
        create_project(temp_projects_dir, "PROJ-005-existing")
        create_project(temp_projects_dir, "PROJ-010-another")

        env = {
            "JERRY_PROJECT": "",
            "CLAUDE_PROJECT_DIR": str(Path(temp_projects_dir).parent),
        }

        exit_code, stdout, _ = run_session_start(
            session_start_script, env, project_root=project_root
        )

        assert exit_code == 0
        assert "NextProjectNumber: 011" in stdout


# =============================================================================
# Edge Case Tests (6 tests)
# =============================================================================


class TestSessionStartEdgeCases:
    """Edge case E2E tests for session start hook."""

    def test_project_with_long_slug(
        self, temp_projects_dir: str, session_start_script: Path, project_root: Path
    ) -> None:
        """Project with long slug is handled correctly."""
        long_slug = "this-is-a-very-long-project-slug"
        create_project(temp_projects_dir, f"PROJ-001-{long_slug}")

        exit_code, stdout, _ = run_session_start(
            session_start_script,
            {
                "JERRY_PROJECT": f"PROJ-001-{long_slug}",
                "CLAUDE_PROJECT_DIR": str(Path(temp_projects_dir).parent),
            },
            project_root=project_root,
        )

        assert exit_code == 0
        assert f"PROJ-001-{long_slug}" in stdout

    def test_project_number_boundary_001(
        self, temp_projects_dir: str, session_start_script: Path, project_root: Path
    ) -> None:
        """Project number 001 is valid."""
        create_project(temp_projects_dir, "PROJ-001-boundary-low")

        exit_code, stdout, _ = run_session_start(
            session_start_script,
            {
                "JERRY_PROJECT": "PROJ-001-boundary-low",
                "CLAUDE_PROJECT_DIR": str(Path(temp_projects_dir).parent),
            },
            project_root=project_root,
        )

        assert exit_code == 0
        assert "<project-context>" in stdout

    def test_project_number_boundary_999(
        self, temp_projects_dir: str, session_start_script: Path, project_root: Path
    ) -> None:
        """Project number 999 is valid and next number caps at 999."""
        create_project(temp_projects_dir, "PROJ-999-boundary-high")

        env = {
            "JERRY_PROJECT": "",
            "CLAUDE_PROJECT_DIR": str(Path(temp_projects_dir).parent),
        }

        exit_code, stdout, _ = run_session_start(
            session_start_script, env, project_root=project_root
        )

        assert exit_code == 0
        # Next number should cap at 999
        assert "NextProjectNumber: 999" in stdout

    def test_archive_directory_is_ignored(
        self, temp_projects_dir: str, session_start_script: Path, project_root: Path
    ) -> None:
        """Archive directory is not included in project list."""
        create_project(temp_projects_dir, "PROJ-001-active")
        # Create archive with what looks like a project
        archive_dir = Path(temp_projects_dir) / "archive"
        archive_dir.mkdir()
        (archive_dir / "PROJ-002-archived").mkdir()

        env = {
            "JERRY_PROJECT": "",
            "CLAUDE_PROJECT_DIR": str(Path(temp_projects_dir).parent),
        }

        exit_code, stdout, _ = run_session_start(
            session_start_script, env, project_root=project_root
        )

        assert exit_code == 0
        assert "PROJ-001-active" in stdout
        assert "PROJ-002-archived" not in stdout

    def test_hidden_directories_ignored(
        self, temp_projects_dir: str, session_start_script: Path, project_root: Path
    ) -> None:
        """Hidden directories are not scanned."""
        create_project(temp_projects_dir, "PROJ-001-visible")
        # Create hidden directory
        hidden = Path(temp_projects_dir) / ".hidden-project"
        hidden.mkdir()
        (hidden / "PLAN.md").write_text("# Hidden")

        env = {
            "JERRY_PROJECT": "",
            "CLAUDE_PROJECT_DIR": str(Path(temp_projects_dir).parent),
        }

        exit_code, stdout, _ = run_session_start(
            session_start_script, env, project_root=project_root
        )

        assert exit_code == 0
        assert "PROJ-001-visible" in stdout
        assert ".hidden" not in stdout

    def test_project_with_hyphenated_slug(
        self, temp_projects_dir: str, session_start_script: Path, project_root: Path
    ) -> None:
        """Project with multiple hyphens in slug is valid."""
        create_project(temp_projects_dir, "PROJ-001-multi-word-slug-name")

        exit_code, stdout, _ = run_session_start(
            session_start_script,
            {
                "JERRY_PROJECT": "PROJ-001-multi-word-slug-name",
                "CLAUDE_PROJECT_DIR": str(Path(temp_projects_dir).parent),
            },
            project_root=project_root,
        )

        assert exit_code == 0
        assert "<project-context>" in stdout


# =============================================================================
# Negative Tests (3 tests)
# =============================================================================


class TestSessionStartNegative:
    """Negative E2E tests for session start hook."""

    def test_invalid_project_id_format(
        self, temp_projects_dir: str, session_start_script: Path, project_root: Path
    ) -> None:
        """Invalid project ID format shows error."""
        exit_code, stdout, _ = run_session_start(
            session_start_script,
            {
                "JERRY_PROJECT": "invalid-format",
                "CLAUDE_PROJECT_DIR": str(Path(temp_projects_dir).parent),
            },
            project_root=project_root,
        )

        assert exit_code == 0  # Always 0
        assert "<project-error>" in stdout
        assert "InvalidProject: invalid-format" in stdout
        assert "ACTION REQUIRED" in stdout

    def test_nonexistent_project(
        self, temp_projects_dir: str, session_start_script: Path, project_root: Path
    ) -> None:
        """Non-existent project shows error with available alternatives."""
        create_project(temp_projects_dir, "PROJ-001-exists")

        exit_code, stdout, _ = run_session_start(
            session_start_script,
            {
                "JERRY_PROJECT": "PROJ-999-nonexistent",
                "CLAUDE_PROJECT_DIR": str(Path(temp_projects_dir).parent),
            },
            project_root=project_root,
        )

        assert exit_code == 0  # Always 0
        assert "<project-error>" in stdout
        assert "InvalidProject: PROJ-999-nonexistent" in stdout
        # Should show available alternatives
        assert "PROJ-001-exists" in stdout

    def test_project_missing_required_files(
        self, temp_projects_dir: str, session_start_script: Path, project_root: Path
    ) -> None:
        """Project missing PLAN.md or WORKTRACKER.md shows validation warnings."""
        # Create project with only PLAN.md (missing WORKTRACKER)
        proj_dir = Path(temp_projects_dir) / "PROJ-001-incomplete"
        proj_dir.mkdir()
        (proj_dir / "PLAN.md").write_text("# Plan")
        # No WORKTRACKER.md

        exit_code, stdout, _ = run_session_start(
            session_start_script,
            {
                "JERRY_PROJECT": "PROJ-001-incomplete",
                "CLAUDE_PROJECT_DIR": str(Path(temp_projects_dir).parent),
            },
            project_root=project_root,
        )

        assert exit_code == 0
        # Should still be valid but with warnings
        assert "<project-context>" in stdout or "<project-error>" in stdout


# =============================================================================
# Failure Scenario Tests (4 tests)
# =============================================================================


class TestSessionStartFailures:
    """Failure scenario E2E tests for session start hook."""

    def test_projects_directory_not_found(
        self, session_start_script: Path, project_root: Path
    ) -> None:
        """Non-existent projects directory handles gracefully."""
        exit_code, stdout, _ = run_session_start(
            session_start_script,
            {
                "JERRY_PROJECT": "",
                "CLAUDE_PROJECT_DIR": "/nonexistent/path",
            },
            project_root=project_root,
        )

        assert exit_code == 0  # Always 0
        # Should show empty list or error
        assert "(no projects found)" in stdout or "<project-error>" in stdout

    def test_corrupt_worktracker_handled(
        self, temp_projects_dir: str, session_start_script: Path, project_root: Path
    ) -> None:
        """Corrupt WORKTRACKER.md is handled gracefully."""
        proj_dir = Path(temp_projects_dir) / "PROJ-001-corrupt"
        proj_dir.mkdir()
        (proj_dir / "PLAN.md").write_text("# Plan")
        # Write binary data
        (proj_dir / "WORKTRACKER.md").write_bytes(b"\x00\x01\x02\xff\xfe")

        env = {
            "JERRY_PROJECT": "",
            "CLAUDE_PROJECT_DIR": str(Path(temp_projects_dir).parent),
        }

        exit_code, stdout, _ = run_session_start(
            session_start_script, env, project_root=project_root
        )

        assert exit_code == 0
        # Should list project even with corrupt file
        assert "PROJ-001-corrupt" in stdout

    def test_empty_worktracker_shows_unknown_status(
        self, temp_projects_dir: str, session_start_script: Path, project_root: Path
    ) -> None:
        """Empty WORKTRACKER.md shows unknown status."""
        proj_dir = Path(temp_projects_dir) / "PROJ-001-empty"
        proj_dir.mkdir()
        (proj_dir / "PLAN.md").write_text("# Plan")
        (proj_dir / "WORKTRACKER.md").write_text("")

        env = {
            "JERRY_PROJECT": "",
            "CLAUDE_PROJECT_DIR": str(Path(temp_projects_dir).parent),
        }

        exit_code, stdout, _ = run_session_start(
            session_start_script, env, project_root=project_root
        )

        assert exit_code == 0
        assert "PROJ-001-empty" in stdout
        assert "[?]" in stdout  # Unknown status icon

    def test_always_returns_exit_code_zero(
        self, temp_projects_dir: str, session_start_script: Path, project_root: Path
    ) -> None:
        """Script always returns exit code 0 for Claude to handle."""
        # Test various error conditions all return 0
        test_cases = [
            {"JERRY_PROJECT": "invalid", "CLAUDE_PROJECT_DIR": temp_projects_dir},
            {"JERRY_PROJECT": "", "CLAUDE_PROJECT_DIR": "/nonexistent"},
            {"JERRY_PROJECT": "PROJ-999-missing", "CLAUDE_PROJECT_DIR": temp_projects_dir},
        ]

        for env_vars in test_cases:
            exit_code, _, _ = run_session_start(
                session_start_script, env_vars, project_root=project_root
            )
            assert exit_code == 0, f"Expected exit 0 for {env_vars}"


# =============================================================================
# Output Format Tests (4 tests)
# =============================================================================


class TestSessionStartOutputFormat:
    """Output format validation E2E tests for session start hook."""

    def test_project_context_tag_structure(
        self, temp_projects_dir: str, session_start_script: Path, project_root: Path
    ) -> None:
        """<project-context> tag has required fields."""
        create_project(temp_projects_dir, "PROJ-001-format-test")

        exit_code, stdout, _ = run_session_start(
            session_start_script,
            {
                "JERRY_PROJECT": "PROJ-001-format-test",
                "CLAUDE_PROJECT_DIR": str(Path(temp_projects_dir).parent),
            },
            project_root=project_root,
        )

        assert exit_code == 0
        # Verify tag structure
        assert stdout.count("<project-context>") == 1
        assert stdout.count("</project-context>") == 1
        assert "ProjectActive:" in stdout
        assert "ProjectPath:" in stdout
        # Verify opening tag comes before closing
        open_idx = stdout.index("<project-context>")
        close_idx = stdout.index("</project-context>")
        assert open_idx < close_idx

    def test_project_required_tag_structure(
        self, temp_projects_dir: str, session_start_script: Path, project_root: Path
    ) -> None:
        """<project-required> tag has required fields."""
        create_project(temp_projects_dir, "PROJ-001-available")

        env = {
            "JERRY_PROJECT": "",
            "CLAUDE_PROJECT_DIR": str(Path(temp_projects_dir).parent),
        }

        exit_code, stdout, _ = run_session_start(
            session_start_script, env, project_root=project_root
        )

        assert exit_code == 0
        assert stdout.count("<project-required>") == 1
        assert stdout.count("</project-required>") == 1
        assert "ProjectRequired: true" in stdout
        assert "AvailableProjects:" in stdout
        assert "NextProjectNumber:" in stdout
        assert "ProjectsJson:" in stdout

    def test_project_error_tag_structure(
        self, temp_projects_dir: str, session_start_script: Path, project_root: Path
    ) -> None:
        """<project-error> tag has required fields."""
        exit_code, stdout, _ = run_session_start(
            session_start_script,
            {
                "JERRY_PROJECT": "invalid-id",
                "CLAUDE_PROJECT_DIR": str(Path(temp_projects_dir).parent),
            },
            project_root=project_root,
        )

        assert exit_code == 0
        assert stdout.count("<project-error>") == 1
        assert stdout.count("</project-error>") == 1
        assert "InvalidProject:" in stdout
        assert "Error:" in stdout
        assert "AvailableProjects:" in stdout

    def test_projects_json_is_valid_json(
        self, temp_projects_dir: str, session_start_script: Path, project_root: Path
    ) -> None:
        """ProjectsJson field contains valid JSON."""
        create_project(temp_projects_dir, "PROJ-001-json-test", status="IN_PROGRESS")
        create_project(temp_projects_dir, "PROJ-002-json-test", status="COMPLETED")

        env = {
            "JERRY_PROJECT": "",
            "CLAUDE_PROJECT_DIR": str(Path(temp_projects_dir).parent),
        }

        exit_code, stdout, _ = run_session_start(
            session_start_script, env, project_root=project_root
        )

        assert exit_code == 0

        # Extract JSON from output
        for line in stdout.split("\n"):
            if line.startswith("ProjectsJson:"):
                json_str = line[len("ProjectsJson:") :].strip()
                projects = json.loads(json_str)

                assert isinstance(projects, list)
                assert len(projects) == 2

                for proj in projects:
                    assert "id" in proj
                    assert "status" in proj
                break
        else:
            pytest.fail("ProjectsJson not found in output")


# =============================================================================
# PEP 723 Metadata Tests (2 tests) - Added for EN-004
# =============================================================================


class TestSessionStartPEP723:
    """Tests for PEP 723 inline script metadata.

    These tests validate that the session_start.py script contains proper
    PEP 723 inline metadata, enabling standalone execution via `uv run`
    without requiring pip install.

    References:
        - PEP 723: https://peps.python.org/pep-0723/
        - BUG-007: SessionStart hook required pip install
        - ADR e-010: Decision to use uv + PEP 723
    """

    def test_pep723_metadata_present(self, session_start_script: Path) -> None:
        """Script contains valid PEP 723 inline script metadata block."""
        content = session_start_script.read_text()

        # Verify PEP 723 opening marker
        assert "# /// script" in content, "Missing PEP 723 opening marker '# /// script'"

        # Verify PEP 723 closing marker (standalone line)
        assert "# ///" in content, "Missing PEP 723 closing marker '# ///'"

        # Verify required sections in metadata
        assert "requires-python" in content, "Missing 'requires-python' in PEP 723 metadata"

    def test_pep723_script_executes_standalone(
        self, session_start_script: Path, project_root: Path
    ) -> None:
        """Script executes via uv run without pip install.

        This is the key test that validates BUG-007 is fixed - the script
        must work without `pip install -e .` being run first.
        """
        # Run in a clean environment (no JERRY_PROJECT set)
        # This should succeed and produce <project-required> output
        env = {
            "JERRY_PROJECT": "",
            "CLAUDE_PROJECT_DIR": str(project_root),
        }

        exit_code, stdout, stderr = run_session_start(
            session_start_script,
            env,
            project_root=project_root,
        )

        # Must exit with 0 (script handles all errors internally)
        assert exit_code == 0, f"Script failed with exit code {exit_code}. stderr: {stderr}"

        # Must produce valid output (either project-required or project-context)
        assert "<project-required>" in stdout or "<project-context>" in stdout, (
            f"Script did not produce expected output tags. stdout: {stdout}"
        )
