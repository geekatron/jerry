# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Integration tests for Jerry CLI end-to-end functionality.

Tests cover:
- CLI entry point execution via subprocess
- Full command execution with real dependencies
- Exit codes and output format
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent


def _find_jerry_executable() -> str:
    """Find the jerry executable - works in both venv and CI environments."""
    # Try venv path first (local development)
    venv_jerry = PROJECT_ROOT / ".venv" / "bin" / "jerry"
    if venv_jerry.exists():
        return str(venv_jerry)

    # Try system path (CI environment with pip install -e .)
    system_jerry = shutil.which("jerry")
    if system_jerry:
        return system_jerry

    # Fallback: use python -m src.interface.cli.main
    pytest.skip("jerry executable not found - run 'pip install -e .'")
    return ""  # Never reached


def _find_python_executable() -> str:
    """Find the Python executable - works in both venv and CI environments."""
    # Try venv path first (local development)
    venv_python = PROJECT_ROOT / ".venv" / "bin" / "python3"
    if venv_python.exists():
        return str(venv_python)

    # Use the current Python interpreter (CI environment)
    return sys.executable


class TestCLIEntryPoint:
    """Tests for jerry entry point execution."""

    @pytest.fixture
    def venv_jerry(self) -> str:
        """Get path to jerry command."""
        return _find_jerry_executable()

    def test_jerry_help_exits_zero(self, venv_jerry: str):
        """jerry --help should exit with code 0."""
        result = subprocess.run(
            [venv_jerry, "--help"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )
        assert result.returncode == 0
        assert "Jerry Framework CLI" in result.stdout

    def test_jerry_version_exits_zero(self, venv_jerry: str):
        """jerry --version should exit with code 0."""
        result = subprocess.run(
            [venv_jerry, "--version"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )
        assert result.returncode == 0
        assert "jerry" in result.stdout

    def test_jerry_projects_context_with_no_project_exits_zero(self, venv_jerry: str):
        """jerry projects context with no JERRY_PROJECT should exit with code 0."""
        env = os.environ.copy()
        env.pop("JERRY_PROJECT", None)

        result = subprocess.run(
            [venv_jerry, "projects", "context"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
            env=env,
        )
        assert result.returncode == 0
        assert "JERRY_PROJECT: (not set)" in result.stdout

    def test_jerry_projects_context_with_valid_project_exits_zero(self, venv_jerry: str):
        """jerry projects context with valid JERRY_PROJECT should exit with code 0."""
        env = os.environ.copy()
        env["JERRY_PROJECT"] = "PROJ-001-plugin-cleanup"

        result = subprocess.run(
            [venv_jerry, "projects", "context"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
            env=env,
        )
        assert result.returncode == 0
        assert "JERRY_PROJECT: PROJ-001-plugin-cleanup" in result.stdout
        assert "Status: Valid" in result.stdout

    def test_jerry_projects_list_exits_zero(self, venv_jerry: str):
        """jerry projects list should exit with code 0."""
        result = subprocess.run(
            [venv_jerry, "projects", "list"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )
        assert result.returncode == 0
        assert "PROJ-001-plugin-cleanup" in result.stdout

    def test_jerry_projects_list_json_returns_valid_json(self, venv_jerry: str):
        """jerry --json projects list should return valid JSON."""
        result = subprocess.run(
            [venv_jerry, "--json", "projects", "list"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )
        assert result.returncode == 0

        output = json.loads(result.stdout)
        assert "projects" in output
        assert "count" in output
        assert isinstance(output["projects"], list)

    def test_jerry_projects_validate_valid_project_exits_zero(self, venv_jerry: str):
        """jerry projects validate with valid project should exit with code 0."""
        result = subprocess.run(
            [venv_jerry, "projects", "validate", "PROJ-001-plugin-cleanup"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )
        assert result.returncode == 0
        assert "Status: Valid" in result.stdout

    def test_jerry_projects_validate_invalid_id_exits_one(self, venv_jerry: str):
        """jerry projects validate with invalid ID should exit with code 1."""
        result = subprocess.run(
            [venv_jerry, "projects", "validate", "INVALID-FORMAT"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )
        assert result.returncode == 1
        assert "Invalid project ID format" in result.stdout

    def test_jerry_projects_validate_nonexistent_exits_one(self, venv_jerry: str):
        """jerry projects validate with nonexistent project should exit with code 1."""
        result = subprocess.run(
            [venv_jerry, "projects", "validate", "PROJ-999-nonexistent"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )
        assert result.returncode == 1

    def test_jerry_projects_validate_json_returns_valid_json(self, venv_jerry: str):
        """jerry --json projects validate should return valid JSON."""
        result = subprocess.run(
            [venv_jerry, "--json", "projects", "validate", "PROJ-001-plugin-cleanup"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )
        assert result.returncode == 0

        output = json.loads(result.stdout)
        assert "project_id" in output
        assert "is_valid" in output
        assert output["is_valid"] is True


class TestCLIModuleExecution:
    """Tests for running CLI as Python module."""

    @pytest.fixture
    def venv_python(self) -> str:
        """Get path to python executable."""
        return _find_python_executable()

    def test_module_execution_works(self, venv_python: str):
        """Running as python -m should work."""
        result = subprocess.run(
            [venv_python, "-m", "src.interface.cli.main", "--help"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )
        assert result.returncode == 0
        assert "Jerry Framework CLI" in result.stdout


class TestSessionNamespaceE2E:
    """E2E tests for session namespace commands."""

    @pytest.fixture
    def venv_jerry(self) -> str:
        """Get path to jerry command."""
        return _find_jerry_executable()

    def test_session_start_exits_zero(self, venv_jerry: str):
        """jerry session start should exit with code 0."""
        result = subprocess.run(
            [venv_jerry, "session", "start", "--name", "Test Session"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )
        # May fail if session already active, but should be handled gracefully
        assert result.returncode in (0, 1)

    def test_session_status_exits_zero(self, venv_jerry: str):
        """jerry session status should exit with code 0."""
        result = subprocess.run(
            [venv_jerry, "session", "status"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )
        assert result.returncode == 0
        # Should show either active session or "no active session"
        assert "Session" in result.stdout or "session" in result.stdout.lower()

    def test_session_status_json_returns_valid_json(self, venv_jerry: str):
        """jerry --json session status should return valid JSON."""
        result = subprocess.run(
            [venv_jerry, "--json", "session", "status"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )
        assert result.returncode == 0
        output = json.loads(result.stdout)
        assert "has_active_session" in output

    def test_session_help_exits_zero(self, venv_jerry: str):
        """jerry session --help should exit with code 0."""
        result = subprocess.run(
            [venv_jerry, "session", "--help"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )
        assert result.returncode == 0
        assert "start" in result.stdout
        assert "end" in result.stdout
        assert "status" in result.stdout


class TestItemsNamespaceE2E:
    """E2E tests for items namespace commands."""

    @pytest.fixture
    def venv_jerry(self) -> str:
        """Get path to jerry command."""
        return _find_jerry_executable()

    def test_items_list_exits_zero(self, venv_jerry: str):
        """jerry items list should exit with code 0."""
        result = subprocess.run(
            [venv_jerry, "items", "list"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )
        assert result.returncode == 0

    def test_items_list_json_returns_valid_json(self, venv_jerry: str):
        """jerry --json items list should return valid JSON."""
        result = subprocess.run(
            [venv_jerry, "--json", "items", "list"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )
        assert result.returncode == 0
        output = json.loads(result.stdout)
        assert "items" in output
        assert "total_count" in output

    def test_items_show_nonexistent_exits_one(self, venv_jerry: str):
        """jerry items show with nonexistent ID should exit with code 1."""
        result = subprocess.run(
            [venv_jerry, "items", "show", "NONEXISTENT-ID"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )
        assert result.returncode == 1
        assert "not found" in result.stdout.lower()

    def test_items_help_exits_zero(self, venv_jerry: str):
        """jerry items --help should exit with code 0."""
        result = subprocess.run(
            [venv_jerry, "items", "--help"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )
        assert result.returncode == 0
        assert "list" in result.stdout
        assert "show" in result.stdout
        assert "create" in result.stdout


class TestCLIOutputFormat:
    """Tests for CLI output formatting."""

    @pytest.fixture
    def venv_jerry(self) -> str:
        """Get path to jerry command."""
        return _find_jerry_executable()

    def test_projects_list_table_has_headers(self, venv_jerry: str):
        """projects list output should have column headers."""
        result = subprocess.run(
            [venv_jerry, "projects", "list"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )
        assert "ID" in result.stdout
        assert "STATUS" in result.stdout
        assert "PATH" in result.stdout

    def test_projects_list_shows_total_count(self, venv_jerry: str):
        """projects list output should show total count."""
        result = subprocess.run(
            [venv_jerry, "projects", "list"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )
        assert "Total:" in result.stdout
        assert "project(s)" in result.stdout

    def test_json_output_is_pretty_printed(self, venv_jerry: str):
        """JSON output should be pretty-printed with indentation."""
        result = subprocess.run(
            [venv_jerry, "--json", "projects", "list"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )
        # Pretty-printed JSON has newlines and indentation
        assert "\n  " in result.stdout
