"""
Integration tests for CLI local context support.

Tests that the CLI correctly reads project context from .jerry/local/context.toml
when JERRY_PROJECT environment variable is not set.

These tests verify the full wiring: CLI → dispatcher → handler → adapter → filesystem.

Test Distribution per testing-standards.md:
- Happy Path (60%): 3 tests - local context read, JSON output, precedence
- Negative (30%): 2 tests - missing file, invalid format
- Edge (10%): 1 test - empty context file

References:
    - EN-001: Session Start Hook TDD Cleanup
    - DISC-008: Bootstrap wiring gap (this is what we're testing)
    - TD-003: Missing local context support
    - AC-005: Local context reading works via main CLI
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    pass


# Mark as integration tests
pytestmark = [
    pytest.mark.integration,
]


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def project_root() -> Path:
    """Get the project root directory."""
    # Navigate from tests/integration/cli to project root
    return Path(__file__).parent.parent.parent.parent


@pytest.fixture
def env_without_jerry_project(project_root: Path) -> dict[str, str]:
    """Create environment WITHOUT JERRY_PROJECT set."""
    env = os.environ.copy()
    env.pop("JERRY_PROJECT", None)  # Remove if set
    # Set PYTHONPATH for imports
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = f"{project_root}:{existing}" if existing else str(project_root)
    return env


@pytest.fixture
def temp_local_context(tmp_path: Path) -> Path:
    """Create a temporary .jerry/local/context.toml file."""
    local_dir = tmp_path / ".jerry" / "local"
    local_dir.mkdir(parents=True)
    context_file = local_dir / "context.toml"
    return context_file


def run_jerry_with_cwd(
    args: list[str],
    project_root: Path,
    env: dict[str, str],
    cwd: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    """Execute jerry CLI via uv run with custom working directory.

    Args:
        args: Command arguments (e.g., ["projects", "context"])
        project_root: Project root for finding uv
        env: Environment variables
        cwd: Working directory (uses tmp_path for isolation)

    Returns:
        CompletedProcess with stdout, stderr, and returncode
    """
    return subprocess.run(
        ["uv", "run", "jerry", *args],
        capture_output=True,
        text=True,
        env=env,
        cwd=str(cwd or project_root),
    )


# =============================================================================
# Happy Path Tests (60%) - T-014, T-015
# =============================================================================


class TestCLILocalContextHappyPath:
    """Happy path tests for CLI local context support."""

    def test_cli_reads_project_from_local_context_when_env_not_set(
        self,
        project_root: Path,
        env_without_jerry_project: dict[str, str],
        tmp_path: Path,
    ) -> None:
        """CLI reads active_project from .jerry/local/context.toml when JERRY_PROJECT not set.

        This tests the full wiring: CLI → dispatcher → handler → adapter → filesystem.
        EN-001 T-015.

        Expected to FAIL until bootstrap.py is updated to wire FilesystemLocalContextAdapter.
        """
        # Arrange - create local context file
        local_dir = tmp_path / ".jerry" / "local"
        local_dir.mkdir(parents=True)
        context_file = local_dir / "context.toml"
        context_file.write_text('[context]\nactive_project = "PROJ-007-jerry-bugs"\n')

        # Also create projects dir structure expected by CLI
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        (projects_dir / "PROJ-007-jerry-bugs").mkdir()
        (projects_dir / "PROJ-007-jerry-bugs" / "PLAN.md").write_text("# Plan")

        # Set CLAUDE_PROJECT_DIR to tmp_path so CLI looks there
        env = env_without_jerry_project.copy()
        env["CLAUDE_PROJECT_DIR"] = str(tmp_path)

        # Act
        result = run_jerry_with_cwd(
            ["--json", "projects", "context"],
            project_root=project_root,
            env=env,
            cwd=tmp_path,
        )

        # Assert - should read from local context
        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)

        # The project should be set from local context
        assert data["jerry_project"] == "PROJ-007-jerry-bugs", (
            f"Expected project from local context, got: {data['jerry_project']}"
        )

    def test_cli_json_output_has_all_required_fields(
        self,
        project_root: Path,
        env_without_jerry_project: dict[str, str],
        tmp_path: Path,
    ) -> None:
        """CLI JSON output contains all required fields.

        EN-001 T-014 - Validates JSON output structure when using local context.
        """
        # Arrange - create local context file
        local_dir = tmp_path / ".jerry" / "local"
        local_dir.mkdir(parents=True)
        context_file = local_dir / "context.toml"
        context_file.write_text('[context]\nactive_project = "PROJ-007-jerry-bugs"\n')

        # Create projects structure
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        (projects_dir / "PROJ-007-jerry-bugs").mkdir()
        (projects_dir / "PROJ-007-jerry-bugs" / "PLAN.md").write_text("# Plan")

        env = env_without_jerry_project.copy()
        env["CLAUDE_PROJECT_DIR"] = str(tmp_path)

        # Act
        result = run_jerry_with_cwd(
            ["--json", "projects", "context"],
            project_root=project_root,
            env=env,
            cwd=tmp_path,
        )

        # Assert - all required fields present
        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)

        # Required fields from RetrieveProjectContextQuery result
        assert "jerry_project" in data, "Missing jerry_project field"
        assert "project_id" in data, "Missing project_id field"
        assert "validation" in data, "Missing validation field"
        assert "available_projects" in data, "Missing available_projects field"
        assert "next_number" in data, "Missing next_number field"

        # Verify values when using local context
        assert data["jerry_project"] == "PROJ-007-jerry-bugs"
        assert data["project_id"] == "PROJ-007-jerry-bugs"

    def test_env_var_takes_precedence_over_local_context(
        self,
        project_root: Path,
        tmp_path: Path,
    ) -> None:
        """JERRY_PROJECT env var takes precedence over local context.

        Precedence: env > local > discovery
        """
        # Arrange - create local context with one project
        local_dir = tmp_path / ".jerry" / "local"
        local_dir.mkdir(parents=True)
        context_file = local_dir / "context.toml"
        context_file.write_text('[context]\nactive_project = "PROJ-002-from-local"\n')

        # Create projects structure
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        (projects_dir / "PROJ-001-from-env").mkdir()
        (projects_dir / "PROJ-001-from-env" / "PLAN.md").write_text("# Plan")
        (projects_dir / "PROJ-002-from-local").mkdir()
        (projects_dir / "PROJ-002-from-local" / "PLAN.md").write_text("# Plan")

        # Set env var to different project
        env = os.environ.copy()
        env["JERRY_PROJECT"] = "PROJ-001-from-env"
        env["CLAUDE_PROJECT_DIR"] = str(tmp_path)
        env["PYTHONPATH"] = str(project_root)

        # Act
        result = run_jerry_with_cwd(
            ["--json", "projects", "context"],
            project_root=project_root,
            env=env,
            cwd=tmp_path,
        )

        # Assert - env var should win
        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)

        assert data["jerry_project"] == "PROJ-001-from-env", (
            f"Expected env var to take precedence, got: {data['jerry_project']}"
        )


# =============================================================================
# Negative Tests (30%)
# =============================================================================


class TestCLILocalContextNegative:
    """Negative tests for CLI local context support."""

    def test_missing_local_context_falls_through_to_discovery(
        self,
        project_root: Path,
        env_without_jerry_project: dict[str, str],
        tmp_path: Path,
    ) -> None:
        """Missing .jerry/local/context.toml should fall through to discovery.

        When neither env var nor local context provides project,
        CLI should show available projects for selection.
        """
        # Arrange - NO local context file, NO env var
        # But create some projects for discovery
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        (projects_dir / "PROJ-001-alpha").mkdir()
        (projects_dir / "PROJ-001-alpha" / "PLAN.md").write_text("# Plan")

        env = env_without_jerry_project.copy()
        env["CLAUDE_PROJECT_DIR"] = str(tmp_path)

        # Act
        result = run_jerry_with_cwd(
            ["--json", "projects", "context"],
            project_root=project_root,
            env=env,
            cwd=tmp_path,
        )

        # Assert - should show available projects
        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)

        assert data["jerry_project"] is None, (
            f"Expected no active project, got: {data['jerry_project']}"
        )
        assert len(data["available_projects"]) >= 1, "Expected available_projects to be populated"

    def test_invalid_project_in_local_context_returns_validation_error(
        self,
        project_root: Path,
        env_without_jerry_project: dict[str, str],
        tmp_path: Path,
    ) -> None:
        """Invalid project format in local context should return validation error."""
        # Arrange - create local context with invalid format
        local_dir = tmp_path / ".jerry" / "local"
        local_dir.mkdir(parents=True)
        context_file = local_dir / "context.toml"
        context_file.write_text('[context]\nactive_project = "invalid-format"\n')

        # Create projects dir
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()

        env = env_without_jerry_project.copy()
        env["CLAUDE_PROJECT_DIR"] = str(tmp_path)

        # Act
        result = run_jerry_with_cwd(
            ["--json", "projects", "context"],
            project_root=project_root,
            env=env,
            cwd=tmp_path,
        )

        # Assert - should indicate validation failure
        assert result.returncode == 0, (
            f"stderr: {result.stderr}"
        )  # CLI succeeds but validation fails
        data = json.loads(result.stdout)

        assert data["jerry_project"] == "invalid-format", (
            f"Expected raw value from local context, got: {data['jerry_project']}"
        )
        assert data["validation"] is not None
        assert data["validation"]["is_valid"] is False, (
            "Expected validation to fail for invalid format"
        )


# =============================================================================
# Edge Case Tests (10%)
# =============================================================================


class TestCLILocalContextEdgeCases:
    """Edge case tests for CLI local context support."""

    def test_empty_local_context_file_falls_through_to_discovery(
        self,
        project_root: Path,
        env_without_jerry_project: dict[str, str],
        tmp_path: Path,
    ) -> None:
        """Empty .jerry/local/context.toml should fall through to discovery.

        Edge case: File exists but has no content.
        """
        # Arrange - create empty local context file
        local_dir = tmp_path / ".jerry" / "local"
        local_dir.mkdir(parents=True)
        context_file = local_dir / "context.toml"
        context_file.write_text("")  # Empty file

        # Create projects for discovery
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        (projects_dir / "PROJ-001-test").mkdir()
        (projects_dir / "PROJ-001-test" / "PLAN.md").write_text("# Plan")

        env = env_without_jerry_project.copy()
        env["CLAUDE_PROJECT_DIR"] = str(tmp_path)

        # Act
        result = run_jerry_with_cwd(
            ["--json", "projects", "context"],
            project_root=project_root,
            env=env,
            cwd=tmp_path,
        )

        # Assert - should fall through to discovery
        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)

        # Empty file means no active_project, so falls through to discovery
        assert data["jerry_project"] is None, (
            f"Expected no active project from empty file, got: {data['jerry_project']}"
        )
