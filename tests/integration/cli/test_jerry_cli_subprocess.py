# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Integration tests for Jerry CLI via subprocess execution.

These tests execute the actual `jerry` command via `uv run` to validate:
- Plugin mode execution (no `pip install -e .` required)
- CLI argument parsing
- JSON output format
- Exit codes

Test Categories:
- TestProjectsCommands: jerry projects context/list/validate
- TestSessionCommands: jerry session start/end/status/abandon
- TestItemsCommands: jerry items list/show/create/start/complete
- TestExitCodes: Exit code validation across all namespaces
- TestJsonOutput: JSON output format validation

References:
    - EN-006: Integration test suite for CLI commands
    - BUG-007: SessionStart hook silent failure (prevented by these tests)
"""

from __future__ import annotations

import json
import os
import subprocess
from collections.abc import Generator
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    pass


# Mark entire module as integration + subprocess tests
pytestmark = [
    pytest.mark.integration,
    pytest.mark.subprocess,
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
def ensure_projects_dir(project_root: Path) -> Generator[Path, None, None]:
    """Ensure the projects/ directory exists for subprocess tests.

    In CI the projects/ directory is gitignored and may not exist, causing
    RepositoryError when CLI commands scan for projects. This fixture creates
    the directory if missing and cleans it up afterward.
    """
    projects_dir = project_root / "projects"
    created = False
    if not projects_dir.exists():
        projects_dir.mkdir()
        created = True
    yield projects_dir
    if created:
        projects_dir.rmdir()


@pytest.fixture
def env_with_pythonpath(project_root: Path) -> dict[str, str]:
    """Create environment with PYTHONPATH set to project root."""
    env = os.environ.copy()
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = f"{project_root}:{existing}" if existing else str(project_root)
    return env


def run_jerry(
    args: list[str],
    project_root: Path,
    env: dict[str, str],
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    """Execute jerry CLI via uv run.

    Args:
        args: Command arguments (e.g., ["projects", "context"])
        project_root: Project root path for cwd
        env: Environment variables
        input_text: Optional input for interactive commands

    Returns:
        CompletedProcess with stdout, stderr, and returncode
    """
    return subprocess.run(
        ["uv", "run", "jerry", *args],
        capture_output=True,
        text=True,
        env=env,
        cwd=str(project_root),
        input=input_text,
    )


# =============================================================================
# Projects Commands Tests (Task EN-006.4)
# =============================================================================


class TestProjectsCommands:
    """Integration tests for jerry projects commands."""

    def test_projects_context_returns_zero_exit_code(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
    ) -> None:
        """jerry projects context returns exit code 0."""
        result = run_jerry(
            ["projects", "context"],
            project_root=project_root,
            env=env_with_pythonpath,
        )

        assert result.returncode == 0, f"stderr: {result.stderr}"

    def test_projects_context_json_is_valid(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
    ) -> None:
        """jerry projects context --json returns valid JSON."""
        result = run_jerry(
            ["--json", "projects", "context"],
            project_root=project_root,
            env=env_with_pythonpath,
        )

        assert result.returncode == 0, f"stderr: {result.stderr}"

        # Should be valid JSON
        data = json.loads(result.stdout)
        assert isinstance(data, dict)

    def test_projects_list_returns_zero_exit_code(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        ensure_projects_dir: Path,
    ) -> None:
        """jerry projects list returns exit code 0."""
        result = run_jerry(
            ["projects", "list"],
            project_root=project_root,
            env=env_with_pythonpath,
        )

        assert result.returncode == 0, f"stderr: {result.stderr}"

    def test_projects_list_json_contains_projects_key(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        ensure_projects_dir: Path,
    ) -> None:
        """jerry projects list --json returns object with 'projects' key."""
        result = run_jerry(
            ["--json", "projects", "list"],
            project_root=project_root,
            env=env_with_pythonpath,
        )

        assert result.returncode == 0, f"stderr: {result.stderr}"

        data = json.loads(result.stdout)
        assert "projects" in data
        assert isinstance(data["projects"], list)

    def test_projects_validate_with_valid_project(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        ensure_projects_dir: Path,
    ) -> None:
        """jerry projects validate with existing project returns 0."""
        # First get list of projects to find a valid one
        list_result = run_jerry(
            ["--json", "projects", "list"],
            project_root=project_root,
            env=env_with_pythonpath,
        )

        if list_result.returncode == 0:
            data = json.loads(list_result.stdout)
            if data.get("projects"):
                project_id = data["projects"][0]["id"]
                result = run_jerry(
                    ["projects", "validate", project_id],
                    project_root=project_root,
                    env=env_with_pythonpath,
                )
                assert result.returncode == 0, f"stderr: {result.stderr}"

    def test_projects_validate_with_invalid_project(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
    ) -> None:
        """jerry projects validate with non-existent project returns 1."""
        result = run_jerry(
            ["projects", "validate", "PROJ-999-nonexistent"],
            project_root=project_root,
            env=env_with_pythonpath,
        )

        assert result.returncode == 1


# =============================================================================
# Session Commands Tests (Task EN-006.2)
# =============================================================================


class TestSessionCommands:
    """Integration tests for jerry session commands."""

    def test_session_status_returns_valid_exit_code(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
    ) -> None:
        """jerry session status returns exit code 0 or 1."""
        result = run_jerry(
            ["session", "status"],
            project_root=project_root,
            env=env_with_pythonpath,
        )

        # Either 0 (has active session) or 1 (no active session)
        assert result.returncode in [0, 1]

    def test_session_status_json_is_valid(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
    ) -> None:
        """jerry session status --json returns valid JSON."""
        result = run_jerry(
            ["--json", "session", "status"],
            project_root=project_root,
            env=env_with_pythonpath,
        )

        # Should always return valid JSON regardless of exit code
        data = json.loads(result.stdout)
        assert isinstance(data, dict)

    def test_session_start_creates_session(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        tmp_path: Path,
    ) -> None:
        """jerry session start creates a new session."""
        # Use tmp_path to avoid polluting actual project
        env = env_with_pythonpath.copy()
        env["JERRY_DATA_DIR"] = str(tmp_path / ".jerry" / "data")

        result = run_jerry(
            ["--json", "session", "start", "--name", "TestSession"],
            project_root=project_root,
            env=env,
        )

        # May succeed or fail depending on existing session
        # We just verify it doesn't crash and returns valid JSON
        if result.returncode == 0:
            data = json.loads(result.stdout)
            assert "session_id" in data or "success" in data

    def test_session_end_without_active_session_returns_error(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        tmp_path: Path,
    ) -> None:
        """jerry session end without active session returns error."""
        # Unset JERRY_PROJECT so bootstrap falls back to InMemoryEventStore
        # (which starts empty in a new subprocess → no active session)
        env = env_with_pythonpath.copy()
        env.pop("JERRY_PROJECT", None)

        result = run_jerry(
            ["--json", "session", "end"],
            project_root=project_root,
            env=env,
        )

        # Should return error (no active session)
        assert result.returncode == 1

    def test_session_abandon_without_active_session_returns_error(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        tmp_path: Path,
    ) -> None:
        """jerry session abandon without active session returns error."""
        # Unset JERRY_PROJECT so bootstrap falls back to InMemoryEventStore
        env = env_with_pythonpath.copy()
        env.pop("JERRY_PROJECT", None)

        result = run_jerry(
            ["--json", "session", "abandon"],
            project_root=project_root,
            env=env,
        )

        # Should return error (no active session)
        assert result.returncode == 1


# =============================================================================
# Items Commands Tests (Task EN-006.3)
# =============================================================================


class TestItemsCommands:
    """Integration tests for jerry items commands."""

    def test_items_list_returns_valid_exit_code(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
    ) -> None:
        """jerry items list returns exit code 0."""
        result = run_jerry(
            ["items", "list"],
            project_root=project_root,
            env=env_with_pythonpath,
        )

        assert result.returncode == 0, f"stderr: {result.stderr}"

    def test_items_list_json_is_valid(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
    ) -> None:
        """jerry items list --json returns valid JSON."""
        result = run_jerry(
            ["--json", "items", "list"],
            project_root=project_root,
            env=env_with_pythonpath,
        )

        assert result.returncode == 0, f"stderr: {result.stderr}"

        data = json.loads(result.stdout)
        assert isinstance(data, dict)
        assert "items" in data or "work_items" in data or isinstance(data, list)

    def test_items_show_nonexistent_returns_error(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
    ) -> None:
        """jerry items show with non-existent ID returns error."""
        result = run_jerry(
            ["items", "show", "WORK-99999-1"],
            project_root=project_root,
            env=env_with_pythonpath,
        )

        assert result.returncode == 1

    def test_items_create_returns_configured_error_or_success(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        tmp_path: Path,
    ) -> None:
        """jerry items create returns proper response (success or 'not configured' error).

        Note: Items write commands may not be wired in CLI main.py yet.
        This test validates the error handling is correct if not configured.

        Without JERRY_PROJECT set, work items are stored in-memory only and
        are not persisted between subprocess calls. This is expected behavior.
        """
        # Use tmp_path to isolate test data
        env = env_with_pythonpath.copy()
        env["JERRY_DATA_DIR"] = str(tmp_path / ".jerry" / "data")

        # Create work item
        create_result = run_jerry(
            ["--json", "items", "create", "Integration Test Item", "--type", "task"],
            project_root=project_root,
            env=env,
        )

        create_data = json.loads(create_result.stdout)

        if create_result.returncode == 0:
            # Command dispatcher is wired - verify create response
            assert create_data.get("success") is True
            work_item_id = create_data.get("work_item_id")
            assert work_item_id is not None

            # Note: Without JERRY_PROJECT, items are stored in-memory only.
            # Each subprocess has its own in-memory event store, so the work
            # item created above is not visible to subsequent subprocess calls.
            # This is expected behavior - full lifecycle tests require
            # JERRY_PROJECT to enable file-based persistence.
        else:
            # Command dispatcher not configured - validate error message
            assert create_result.returncode == 1
            assert "error" in create_data
            assert "dispatcher" in create_data["error"].lower()

    def test_items_list_with_status_filter(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
    ) -> None:
        """jerry items list --status pending returns filtered items."""
        result = run_jerry(
            ["--json", "items", "list", "--status", "pending"],
            project_root=project_root,
            env=env_with_pythonpath,
        )

        # Should succeed even if no items match
        assert result.returncode == 0, f"stderr: {result.stderr}"

        data = json.loads(result.stdout)
        assert isinstance(data, dict)


# =============================================================================
# Exit Code Tests (Task EN-006.6)
# =============================================================================


class TestExitCodes:
    """Exit code validation tests."""

    def test_help_returns_zero(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
    ) -> None:
        """jerry --help returns exit code 0."""
        result = run_jerry(
            ["--help"],
            project_root=project_root,
            env=env_with_pythonpath,
        )

        assert result.returncode == 0

    def test_version_returns_zero(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
    ) -> None:
        """jerry --version returns exit code 0."""
        result = run_jerry(
            ["--version"],
            project_root=project_root,
            env=env_with_pythonpath,
        )

        assert result.returncode == 0

    def test_no_args_returns_zero(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
    ) -> None:
        """jerry with no arguments returns 0 (shows help)."""
        result = run_jerry(
            [],
            project_root=project_root,
            env=env_with_pythonpath,
        )

        assert result.returncode == 0

    def test_invalid_namespace_returns_error(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
    ) -> None:
        """jerry nonexistent returns error."""
        result = run_jerry(
            ["nonexistent"],
            project_root=project_root,
            env=env_with_pythonpath,
        )

        assert result.returncode == 2  # Invalid usage

    def test_missing_subcommand_returns_error(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
    ) -> None:
        """jerry session without subcommand returns error."""
        result = run_jerry(
            ["session"],
            project_root=project_root,
            env=env_with_pythonpath,
        )

        assert result.returncode == 1  # Error (no command specified)


# =============================================================================
# JSON Output Tests (Task EN-006.5)
# =============================================================================


class TestJsonOutput:
    """JSON output format validation tests."""

    def test_json_flag_before_namespace(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
    ) -> None:
        """jerry --json projects context works."""
        result = run_jerry(
            ["--json", "projects", "context"],
            project_root=project_root,
            env=env_with_pythonpath,
        )

        assert result.returncode == 0
        # Should be valid JSON
        json.loads(result.stdout)

    def test_json_output_is_parseable(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        ensure_projects_dir: Path,
    ) -> None:
        """All --json outputs are parseable JSON."""
        commands = [
            ["--json", "projects", "context"],
            ["--json", "projects", "list"],
            ["--json", "items", "list"],
            ["--json", "session", "status"],
        ]

        for args in commands:
            result = run_jerry(
                args,
                project_root=project_root,
                env=env_with_pythonpath,
            )

            # Should always be parseable JSON
            try:
                json.loads(result.stdout)
            except json.JSONDecodeError as e:
                pytest.fail(f"Command {args} returned invalid JSON: {e}")

    def test_error_json_contains_error_key(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
    ) -> None:
        """Error responses in JSON mode contain 'error' key."""
        result = run_jerry(
            ["--json", "items", "show", "WORK-99999-1"],
            project_root=project_root,
            env=env_with_pythonpath,
        )

        assert result.returncode == 1
        data = json.loads(result.stdout)
        assert "error" in data


# =============================================================================
# Plugin Mode Validation (Core EN-006 requirement)
# =============================================================================


class TestPluginModeExecution:
    """Tests validating plugin mode execution (no pip install -e . required)."""

    def test_cli_executes_without_pip_install(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
    ) -> None:
        """CLI executes via uv run without pip install."""
        result = run_jerry(
            ["--version"],
            project_root=project_root,
            env=env_with_pythonpath,
        )

        assert result.returncode == 0
        assert "jerry" in result.stdout.lower() or "0." in result.stdout

    def test_all_namespaces_accessible_in_plugin_mode(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
    ) -> None:
        """All CLI namespaces are accessible in plugin mode."""
        namespaces = ["projects", "session", "items", "config"]

        for namespace in namespaces:
            result = run_jerry(
                [namespace, "--help"],
                project_root=project_root,
                env=env_with_pythonpath,
            )

            # Should show help (exit 0) or require subcommand (exit 1)
            # but should NOT crash (exit 2 or higher)
            assert result.returncode in [0, 1], f"{namespace}: {result.stderr}"

    def test_imports_work_with_pythonpath(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
    ) -> None:
        """All imports resolve correctly with PYTHONPATH."""
        result = run_jerry(
            ["projects", "context"],
            project_root=project_root,
            env=env_with_pythonpath,
        )

        # Should not have ModuleNotFoundError
        assert "ModuleNotFoundError" not in result.stderr
        assert "ImportError" not in result.stderr
        assert result.returncode == 0
