"""Contract tests for Session Start Hook output.

These tests validate that the hook output adheres to the documented contract
that Claude Code depends on for parsing. Breaking these tests means breaking
the integration with Claude.

Contract Specification (from scripts/session_start.py):
    Exit Codes:
        - Always 0 (Claude handles errors via output)

    Output Tags:
        - <project-context>: JERRY_PROJECT set and valid
        - <project-required>: No project selected
        - <project-error>: JERRY_PROJECT set but invalid

    Required Fields per Tag:
        project-context:
            - ProjectActive: {project_id}
            - ProjectPath: projects/{project_id}/
            - ValidationMessage: or ValidationWarnings:

        project-required:
            - ProjectRequired: true
            - AvailableProjects: (list)
            - NextProjectNumber: NNN
            - ProjectsJson: (valid JSON array)
            - ACTION REQUIRED message

        project-error:
            - InvalidProject: {value}
            - Error: {message}
            - AvailableProjects: (list)
            - NextProjectNumber: NNN
            - ACTION REQUIRED message

References:
    - ENFORCE-012: Contract Tests
    - scripts/session_start.py: Hook implementation
"""

from __future__ import annotations

import json
import re
import subprocess
import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest

# =============================================================================
# Contract Schema Definitions
# =============================================================================


PROJECT_CONTEXT_SCHEMA = {
    "tag": "project-context",
    "required_fields": ["ProjectActive:", "ProjectPath:"],
    "optional_fields": ["ValidationMessage:", "ValidationWarnings:"],
    "validation_field_required": True,  # One of ValidationMessage/Warnings must exist
}

PROJECT_REQUIRED_SCHEMA = {
    "tag": "project-required",
    "required_fields": [
        "ProjectRequired: true",
        "AvailableProjects:",
        "NextProjectNumber:",
        "ProjectsJson:",
    ],
    "action_required": True,
}

PROJECT_ERROR_SCHEMA = {
    "tag": "project-error",
    "required_fields": [
        "InvalidProject:",
        "Error:",
        "AvailableProjects:",
        "NextProjectNumber:",
    ],
    "action_required": True,
}


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
    """Get path to the session_start.py script (BUG-007 moved to src/interface/cli/)."""
    return project_root / "src" / "interface" / "cli" / "session_start.py"


def create_project(base_path: str, project_id: str) -> Path:
    """Create a valid project directory with required files."""
    proj_dir = Path(base_path) / project_id
    proj_dir.mkdir(parents=True)
    (proj_dir / "PLAN.md").write_text("# Plan")
    (proj_dir / "WORKTRACKER.md").write_text("# Tracker\nIN_PROGRESS")
    return proj_dir


def run_hook(
    script_path: Path, env_vars: dict, project_root: Path | None = None
) -> tuple[int, str]:
    """Run the session start hook via uv run and return exit code and stdout.

    Uses uv run to ensure correct dependency management (DISC-008, EN-004).
    Sets PYTHONPATH for local src/ imports (DISC-005).
    """
    import os

    env = os.environ.copy()
    env.update(env_vars)

    # Set PYTHONPATH to project root for "from src.X" imports (DISC-005)
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
    return result.returncode, result.stdout


def extract_tag_content(output: str, tag_name: str) -> str | None:
    """Extract content between opening and closing tags."""
    pattern = rf"<{tag_name}>(.*?)</{tag_name}>"
    match = re.search(pattern, output, re.DOTALL)
    return match.group(1) if match else None


# =============================================================================
# Contract Test: project-context Tag
# =============================================================================


class TestProjectContextTagContract:
    """Contract tests for <project-context> tag structure."""

    def test_output_contains_required_project_context_tag(
        self,
        temp_projects_dir: str,
        temp_root_dir: str,
        session_start_script: Path,
        project_root: Path,
    ) -> None:
        """When project is valid, output MUST contain <project-context> tag."""
        create_project(temp_projects_dir, "PROJ-001-test")

        _, stdout = run_hook(
            session_start_script,
            {"JERRY_PROJECT": "PROJ-001-test", "CLAUDE_PROJECT_DIR": temp_root_dir},
            project_root=project_root,
        )

        # Contract: Tag must exist
        assert "<project-context>" in stdout, "Missing opening <project-context> tag"
        assert "</project-context>" in stdout, "Missing closing </project-context> tag"

        # Contract: Tags must be properly nested (opening before closing)
        open_idx = stdout.index("<project-context>")
        close_idx = stdout.index("</project-context>")
        assert open_idx < close_idx, "Tags not properly nested"

    def test_project_context_contains_required_fields(
        self,
        temp_projects_dir: str,
        temp_root_dir: str,
        session_start_script: Path,
        project_root: Path,
    ) -> None:
        """<project-context> tag MUST contain all required fields."""
        create_project(temp_projects_dir, "PROJ-001-test")

        _, stdout = run_hook(
            session_start_script,
            {"JERRY_PROJECT": "PROJ-001-test", "CLAUDE_PROJECT_DIR": temp_root_dir},
            project_root=project_root,
        )

        content = extract_tag_content(stdout, "project-context")
        assert content is not None, "Could not extract project-context content"

        # Contract: Required fields
        for field in PROJECT_CONTEXT_SCHEMA["required_fields"]:
            assert field in content, f"Missing required field: {field}"

        # Contract: Must have either ValidationMessage or ValidationWarnings
        has_validation = "ValidationMessage:" in content or "ValidationWarnings:" in content
        assert has_validation, "Missing validation field (Message or Warnings)"

    def test_project_active_field_format(
        self,
        temp_projects_dir: str,
        temp_root_dir: str,
        session_start_script: Path,
        project_root: Path,
    ) -> None:
        """ProjectActive field MUST contain the project ID."""
        create_project(temp_projects_dir, "PROJ-042-example")

        _, stdout = run_hook(
            session_start_script,
            {"JERRY_PROJECT": "PROJ-042-example", "CLAUDE_PROJECT_DIR": temp_root_dir},
            project_root=project_root,
        )

        # Contract: ProjectActive contains exact project ID
        assert "ProjectActive: PROJ-042-example" in stdout

    def test_project_path_field_format(
        self,
        temp_projects_dir: str,
        temp_root_dir: str,
        session_start_script: Path,
        project_root: Path,
    ) -> None:
        """ProjectPath field MUST follow projects/{id}/ format."""
        create_project(temp_projects_dir, "PROJ-001-test")

        _, stdout = run_hook(
            session_start_script,
            {"JERRY_PROJECT": "PROJ-001-test", "CLAUDE_PROJECT_DIR": temp_root_dir},
            project_root=project_root,
        )

        # Contract: ProjectPath follows specific format
        assert "ProjectPath: projects/PROJ-001-test/" in stdout


# =============================================================================
# Contract Test: project-required Tag
# =============================================================================


class TestProjectRequiredTagContract:
    """Contract tests for <project-required> tag structure."""

    def test_output_contains_required_project_required_tag(
        self,
        temp_projects_dir: str,
        temp_root_dir: str,
        session_start_script: Path,
        project_root: Path,
    ) -> None:
        """When no project set, output MUST contain <project-required> tag."""
        create_project(temp_projects_dir, "PROJ-001-available")

        _, stdout = run_hook(
            session_start_script,
            {"JERRY_PROJECT": "", "CLAUDE_PROJECT_DIR": temp_root_dir},
            project_root=project_root,
        )

        # Contract: Tag must exist
        assert "<project-required>" in stdout, "Missing <project-required> tag"
        assert "</project-required>" in stdout, "Missing </project-required> tag"

    def test_project_required_contains_required_fields(
        self,
        temp_projects_dir: str,
        temp_root_dir: str,
        session_start_script: Path,
        project_root: Path,
    ) -> None:
        """<project-required> tag MUST contain all required fields."""
        create_project(temp_projects_dir, "PROJ-001-test")

        _, stdout = run_hook(
            session_start_script,
            {"JERRY_PROJECT": "", "CLAUDE_PROJECT_DIR": temp_root_dir},
            project_root=project_root,
        )

        content = extract_tag_content(stdout, "project-required")
        assert content is not None, "Could not extract project-required content"

        # Contract: Required fields
        for field in PROJECT_REQUIRED_SCHEMA["required_fields"]:
            assert field in content or field in stdout, f"Missing required field: {field}"

    def test_output_action_required_message_present_when_needed(
        self,
        temp_root_dir: str,
        session_start_script: Path,
        project_root: Path,
    ) -> None:
        """ACTION REQUIRED message MUST appear when project selection needed."""
        _, stdout = run_hook(
            session_start_script,
            {"JERRY_PROJECT": "", "CLAUDE_PROJECT_DIR": temp_root_dir},
            project_root=project_root,
        )

        # Contract: ACTION REQUIRED must be present
        assert "ACTION REQUIRED" in stdout, "Missing ACTION REQUIRED message"

    def test_next_project_number_format(
        self,
        temp_root_dir: str,
        session_start_script: Path,
        project_root: Path,
    ) -> None:
        """NextProjectNumber MUST be 3-digit zero-padded format."""
        _, stdout = run_hook(
            session_start_script,
            {"JERRY_PROJECT": "", "CLAUDE_PROJECT_DIR": temp_root_dir},
            project_root=project_root,
        )

        # Contract: NextProjectNumber format is NNN (3 digits)
        match = re.search(r"NextProjectNumber: (\d{3})", stdout)
        assert match is not None, "NextProjectNumber not in NNN format"
        assert match.group(1) == "001", "Empty projects should start at 001"


# =============================================================================
# Contract Test: project-error Tag
# =============================================================================


class TestProjectErrorTagContract:
    """Contract tests for <project-error> tag structure."""

    def test_output_contains_project_error_tag_on_invalid(
        self,
        temp_root_dir: str,
        session_start_script: Path,
        project_root: Path,
    ) -> None:
        """When project invalid, output MUST contain <project-error> tag."""
        _, stdout = run_hook(
            session_start_script,
            {"JERRY_PROJECT": "invalid-format", "CLAUDE_PROJECT_DIR": temp_root_dir},
            project_root=project_root,
        )

        # Contract: Tag must exist
        assert "<project-error>" in stdout, "Missing <project-error> tag"
        assert "</project-error>" in stdout, "Missing </project-error> tag"

    def test_project_error_contains_required_fields(
        self,
        temp_root_dir: str,
        session_start_script: Path,
        project_root: Path,
    ) -> None:
        """<project-error> tag MUST contain all required fields."""
        _, stdout = run_hook(
            session_start_script,
            {"JERRY_PROJECT": "bad-id", "CLAUDE_PROJECT_DIR": temp_root_dir},
            project_root=project_root,
        )

        content = extract_tag_content(stdout, "project-error")
        assert content is not None, "Could not extract project-error content"

        # Contract: Required fields
        for field in PROJECT_ERROR_SCHEMA["required_fields"]:
            assert field in content or field in stdout, f"Missing required field: {field}"

    def test_action_required_on_error(
        self,
        temp_root_dir: str,
        session_start_script: Path,
        project_root: Path,
    ) -> None:
        """ACTION REQUIRED message MUST appear on error."""
        _, stdout = run_hook(
            session_start_script,
            {"JERRY_PROJECT": "invalid", "CLAUDE_PROJECT_DIR": temp_root_dir},
            project_root=project_root,
        )

        # Contract: ACTION REQUIRED must be present
        assert "ACTION REQUIRED" in stdout


# =============================================================================
# Contract Test: JSON Schema
# =============================================================================


class TestJsonSchemaContract:
    """Contract tests for JSON output format."""

    def test_output_json_matches_schema(
        self,
        temp_projects_dir: str,
        temp_root_dir: str,
        session_start_script: Path,
        project_root: Path,
    ) -> None:
        """ProjectsJson MUST be valid JSON array with id and status fields."""
        create_project(temp_projects_dir, "PROJ-001-test")
        create_project(temp_projects_dir, "PROJ-002-another")

        _, stdout = run_hook(
            session_start_script,
            {"JERRY_PROJECT": "", "CLAUDE_PROJECT_DIR": temp_root_dir},
            project_root=project_root,
        )

        # Extract JSON from output
        json_match = re.search(r"ProjectsJson: (.+)", stdout)
        assert json_match is not None, "ProjectsJson field not found"

        json_str = json_match.group(1).strip()

        # Contract: Must be valid JSON
        try:
            projects = json.loads(json_str)
        except json.JSONDecodeError as e:
            pytest.fail(f"ProjectsJson is not valid JSON: {e}")

        # Contract: Must be an array
        assert isinstance(projects, list), "ProjectsJson must be an array"

        # Contract: Each item must have id and status
        for proj in projects:
            assert "id" in proj, "Project item missing 'id' field"
            assert "status" in proj, "Project item missing 'status' field"

    def test_json_id_matches_project_id_format(
        self,
        temp_projects_dir: str,
        temp_root_dir: str,
        session_start_script: Path,
        project_root: Path,
    ) -> None:
        """JSON id field MUST match PROJ-NNN-slug format."""
        create_project(temp_projects_dir, "PROJ-001-test")

        _, stdout = run_hook(
            session_start_script,
            {"JERRY_PROJECT": "", "CLAUDE_PROJECT_DIR": temp_root_dir},
            project_root=project_root,
        )

        json_match = re.search(r"ProjectsJson: (.+)", stdout)
        assert json_match is not None, "ProjectsJson not found"
        projects = json.loads(json_match.group(1).strip())

        for proj in projects:
            # Contract: ID format is PROJ-NNN-slug
            assert re.match(r"PROJ-\d{3}-[a-z0-9-]+", proj["id"]), (
                f"Invalid id format: {proj['id']}"
            )

    def test_json_status_is_valid_enum(
        self,
        temp_projects_dir: str,
        temp_root_dir: str,
        session_start_script: Path,
        project_root: Path,
    ) -> None:
        """JSON status field MUST be a valid ProjectStatus enum value."""
        create_project(temp_projects_dir, "PROJ-001-test")

        _, stdout = run_hook(
            session_start_script,
            {"JERRY_PROJECT": "", "CLAUDE_PROJECT_DIR": temp_root_dir},
            project_root=project_root,
        )

        json_match = re.search(r"ProjectsJson: (.+)", stdout)
        assert json_match is not None, "ProjectsJson not found"
        projects = json.loads(json_match.group(1).strip())

        valid_statuses = {"IN_PROGRESS", "COMPLETED", "DRAFT", "ARCHIVED", "UNKNOWN"}

        for proj in projects:
            assert proj["status"] in valid_statuses, (
                f"Invalid status: {proj['status']}. Must be one of {valid_statuses}"
            )


# =============================================================================
# Contract Test: Exit Code Semantics
# =============================================================================


class TestExitCodeContract:
    """Contract tests for exit code semantics."""

    def test_output_exit_code_semantics_match_hook_spec(
        self,
        temp_projects_dir: str,
        temp_root_dir: str,
        session_start_script: Path,
        project_root: Path,
    ) -> None:
        """Exit code MUST always be 0 (Claude handles errors via output)."""
        test_cases = [
            # Valid project
            {"JERRY_PROJECT": "PROJ-001-test", "CLAUDE_PROJECT_DIR": temp_root_dir},
            # No project
            {"JERRY_PROJECT": "", "CLAUDE_PROJECT_DIR": temp_root_dir},
            # Invalid project
            {"JERRY_PROJECT": "invalid", "CLAUDE_PROJECT_DIR": temp_root_dir},
            # Non-existent directory
            {"JERRY_PROJECT": "", "CLAUDE_PROJECT_DIR": "/nonexistent"},
        ]

        # Create project for valid case
        create_project(temp_projects_dir, "PROJ-001-test")

        for env_vars in test_cases:
            exit_code, _ = run_hook(session_start_script, env_vars, project_root=project_root)

            # Contract: Exit code is ALWAYS 0
            assert exit_code == 0, (
                f"Exit code must be 0 for all cases. Got {exit_code} for {env_vars}"
            )

    def test_exactly_one_tag_type_per_output(
        self,
        temp_projects_dir: str,
        temp_root_dir: str,
        session_start_script: Path,
        project_root: Path,
    ) -> None:
        """Output MUST contain exactly one of the three tag types."""
        create_project(temp_projects_dir, "PROJ-001-test")

        # Test valid project
        _, stdout = run_hook(
            session_start_script,
            {"JERRY_PROJECT": "PROJ-001-test", "CLAUDE_PROJECT_DIR": temp_root_dir},
            project_root=project_root,
        )

        tag_count = sum(
            [
                "<project-context>" in stdout,
                "<project-required>" in stdout,
                "<project-error>" in stdout,
            ]
        )

        # Contract: Exactly one tag type
        assert tag_count == 1, f"Expected exactly 1 tag type, found {tag_count}"
