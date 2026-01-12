"""Unit tests for Jerry CLI adapter and bootstrap helpers.

Tests cover:
- CLIAdapter command methods (adapter.py)
- Output formatting (adapter.py)
- Bootstrap helpers (bootstrap.py)

Note: After the TD-015 Clean Architecture refactoring:
- Command handlers are now methods on CLIAdapter
- CLIAdapter receives dispatcher via constructor injection
- get_projects_directory() moved to src.bootstrap

Note: Parser tests are in test_parser.py (Phase 4.1)
Note: Main routing tests are in test_main_v2.py (Phase 4.2)
"""

from __future__ import annotations

import json
from unittest.mock import MagicMock, Mock, patch

import pytest

from src.bootstrap import get_projects_directory
from src.interface.cli.adapter import CLIAdapter
from src.interface.cli.parser import __version__
from src.session_management.domain import ProjectId, ProjectStatus, ValidationResult


class MockProjectInfo:
    """Mock ProjectInfo for testing."""

    def __init__(self, id_str: str, status: str = "IN_PROGRESS"):
        self.id = ProjectId.parse(id_str)
        self.status = ProjectStatus[status]

    def __str__(self) -> str:
        return str(self.id)


class TestFormatProjectTable:
    """Tests for CLIAdapter._format_project_table method."""

    def test_empty_list_returns_no_projects_message(self):
        """Empty project list should return appropriate message."""
        mock_dispatcher = Mock()
        adapter = CLIAdapter(dispatcher=mock_dispatcher, projects_dir="/test")
        result = adapter._format_project_table([])
        assert result == "No projects found."

    def test_single_project_formats_correctly(self):
        """Single project should be formatted as table row."""
        mock_dispatcher = Mock()
        adapter = CLIAdapter(dispatcher=mock_dispatcher, projects_dir="/test")
        projects = [MockProjectInfo("PROJ-001-test", "IN_PROGRESS")]
        result = adapter._format_project_table(projects)

        assert "PROJ-001-test" in result
        assert "in_progress" in result
        assert "projects/PROJ-001-test/" in result

    def test_multiple_projects_format_correctly(self):
        """Multiple projects should all appear in table."""
        mock_dispatcher = Mock()
        adapter = CLIAdapter(dispatcher=mock_dispatcher, projects_dir="/test")
        projects = [
            MockProjectInfo("PROJ-001-alpha", "IN_PROGRESS"),
            MockProjectInfo("PROJ-002-beta", "COMPLETED"),
        ]
        result = adapter._format_project_table(projects)

        assert "PROJ-001-alpha" in result
        assert "PROJ-002-beta" in result
        assert "in_progress" in result
        assert "completed" in result


class TestGetProjectsDirectory:
    """Tests for get_projects_directory function."""

    def test_uses_claude_project_dir_if_set(self):
        """Should use CLAUDE_PROJECT_DIR environment variable if set."""
        with patch.dict("os.environ", {"CLAUDE_PROJECT_DIR": "/test/root"}):
            result = get_projects_directory()
            assert result == "/test/root/projects"

    def test_falls_back_to_cwd_if_no_env(self):
        """Should use current working directory if CLAUDE_PROJECT_DIR not set."""
        with patch.dict("os.environ", {}, clear=True):
            with patch("pathlib.Path.cwd") as mock_cwd:
                mock_path = MagicMock()
                mock_path.__truediv__ = MagicMock(return_value="/cwd/projects")
                mock_path.__str__ = MagicMock(return_value="/cwd/projects")
                mock_cwd.return_value = mock_path
                get_projects_directory()
                # Should attempt to use cwd
                mock_cwd.assert_called()


class TestCLIAdapterCmdInit:
    """Tests for CLIAdapter.cmd_init method.

    Note: After TD-015 refactoring, command handlers are now
    methods on CLIAdapter with injected dispatcher.
    """

    def test_returns_zero_on_success(self):
        """cmd_init should return 0 on success."""
        mock_dispatcher = Mock()
        mock_dispatcher.dispatch.return_value = {
            "jerry_project": None,
            "project_id": None,
            "validation": None,
            "available_projects": [],
            "next_number": 1,
        }

        adapter = CLIAdapter(dispatcher=mock_dispatcher, projects_dir="/test")
        result = adapter.cmd_init(json_output=False)
        assert result == 0

    def test_outputs_json_when_flag_set(self, capsys):
        """cmd_init should output JSON when json_output is True."""
        mock_dispatcher = Mock()
        mock_dispatcher.dispatch.return_value = {
            "jerry_project": "PROJ-001-test",
            "project_id": ProjectId.parse("PROJ-001-test"),
            "validation": ValidationResult.success(),
            "available_projects": [],
            "next_number": 2,
        }

        adapter = CLIAdapter(dispatcher=mock_dispatcher, projects_dir="/test")
        result = adapter.cmd_init(json_output=True)
        captured = capsys.readouterr()

        assert result == 0
        output = json.loads(captured.out)
        assert output["jerry_project"] == "PROJ-001-test"
        assert output["validation"]["is_valid"] is True


class TestCLIAdapterCmdProjectsList:
    """Tests for CLIAdapter.cmd_projects_list method."""

    def test_returns_zero_on_success(self):
        """cmd_projects_list should return 0 on success."""
        mock_dispatcher = Mock()
        mock_dispatcher.dispatch.return_value = []

        adapter = CLIAdapter(dispatcher=mock_dispatcher, projects_dir="/test")
        result = adapter.cmd_projects_list(json_output=False)
        assert result == 0

    def test_outputs_json_when_flag_set(self, capsys):
        """cmd_projects_list should output JSON when json_output is True."""
        mock_dispatcher = Mock()
        mock_dispatcher.dispatch.return_value = [
            MockProjectInfo("PROJ-001-test"),
        ]

        adapter = CLIAdapter(dispatcher=mock_dispatcher, projects_dir="/test")
        result = adapter.cmd_projects_list(json_output=True)
        captured = capsys.readouterr()

        assert result == 0
        output = json.loads(captured.out)
        assert output["count"] == 1
        assert len(output["projects"]) == 1


class TestCLIAdapterCmdProjectsValidate:
    """Tests for CLIAdapter.cmd_projects_validate method."""

    def test_returns_zero_for_valid_project(self):
        """cmd_projects_validate should return 0 for valid project."""
        mock_dispatcher = Mock()
        mock_dispatcher.dispatch.return_value = (
            ProjectId.parse("PROJ-001-test"),
            ValidationResult.success(),
        )

        adapter = CLIAdapter(dispatcher=mock_dispatcher, projects_dir="/test")
        result = adapter.cmd_projects_validate(
            project_id_str="PROJ-001-test",
            json_output=False,
        )
        assert result == 0

    def test_returns_one_for_invalid_project(self):
        """cmd_projects_validate should return 1 for invalid project."""
        mock_dispatcher = Mock()
        mock_dispatcher.dispatch.return_value = (
            None,
            ValidationResult.failure(["Invalid format"]),
        )

        adapter = CLIAdapter(dispatcher=mock_dispatcher, projects_dir="/test")
        result = adapter.cmd_projects_validate(
            project_id_str="INVALID-ID",
            json_output=False,
        )
        assert result == 1

    def test_outputs_json_when_flag_set(self, capsys):
        """cmd_projects_validate should output JSON when json_output is True."""
        mock_dispatcher = Mock()
        mock_dispatcher.dispatch.return_value = (
            ProjectId.parse("PROJ-001-test"),
            ValidationResult.success(),
        )

        adapter = CLIAdapter(dispatcher=mock_dispatcher, projects_dir="/test")
        result = adapter.cmd_projects_validate(
            project_id_str="PROJ-001-test",
            json_output=True,
        )
        captured = capsys.readouterr()

        assert result == 0
        output = json.loads(captured.out)
        assert output["is_valid"] is True


class TestVersion:
    """Tests for version constant."""

    def test_version_is_string(self):
        """Version should be a string."""
        assert isinstance(__version__, str)

    def test_version_matches_expected_format(self):
        """Version should match semantic versioning format."""
        import re

        pattern = r"^\d+\.\d+\.\d+$"
        assert re.match(pattern, __version__), f"Version {__version__} doesn't match semver"
