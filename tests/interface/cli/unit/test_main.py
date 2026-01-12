"""Unit tests for Jerry CLI main module.

Tests cover:
- Argument parsing
- Output formatting
- Command handler logic
"""

from __future__ import annotations

import argparse
import json
from unittest.mock import MagicMock, patch

import pytest

from src.interface.cli.main import (
    __version__,
    cmd_init,
    cmd_projects_list,
    cmd_projects_validate,
    create_parser,
    format_project_table,
    get_projects_directory,
)
from src.session_management.domain import ProjectId, ProjectStatus, ValidationResult


class MockProjectInfo:
    """Mock ProjectInfo for testing."""

    def __init__(self, id_str: str, status: str = "IN_PROGRESS"):
        self.id = ProjectId.parse(id_str)
        self.status = ProjectStatus[status]

    def __str__(self) -> str:
        return str(self.id)


class TestCreateParser:
    """Tests for create_parser function."""

    def test_parser_has_version_option(self):
        """Parser should have --version option."""
        parser = create_parser()
        # Verify --version exists by checking it doesn't raise
        with pytest.raises(SystemExit):  # --version exits
            parser.parse_args(["--version"])

    def test_parser_has_json_option(self):
        """Parser should have --json option."""
        parser = create_parser()
        args = parser.parse_args(["--json", "init"])
        assert args.json is True

    def test_parser_has_init_command(self):
        """Parser should have init command."""
        parser = create_parser()
        args = parser.parse_args(["init"])
        assert args.command == "init"

    def test_parser_has_projects_list_command(self):
        """Parser should have projects list command."""
        parser = create_parser()
        args = parser.parse_args(["projects", "list"])
        assert args.command == "projects"
        assert args.projects_command == "list"

    def test_parser_has_projects_validate_command(self):
        """Parser should have projects validate command with project_id arg."""
        parser = create_parser()
        args = parser.parse_args(["projects", "validate", "PROJ-001-test"])
        assert args.command == "projects"
        assert args.projects_command == "validate"
        assert args.project_id == "PROJ-001-test"

    def test_parser_no_command_leaves_command_none(self):
        """Parser with no command should leave args.command as None."""
        parser = create_parser()
        args = parser.parse_args([])
        assert args.command is None


class TestFormatProjectTable:
    """Tests for format_project_table function."""

    def test_empty_list_returns_no_projects_message(self):
        """Empty project list should return appropriate message."""
        result = format_project_table([])
        assert result == "No projects found."

    def test_single_project_formats_correctly(self):
        """Single project should be formatted as table row."""
        projects = [MockProjectInfo("PROJ-001-test", "IN_PROGRESS")]
        result = format_project_table(projects)

        assert "PROJ-001-test" in result
        assert "in_progress" in result
        assert "projects/PROJ-001-test/" in result

    def test_multiple_projects_format_correctly(self):
        """Multiple projects should all appear in table."""
        projects = [
            MockProjectInfo("PROJ-001-alpha", "IN_PROGRESS"),
            MockProjectInfo("PROJ-002-beta", "COMPLETED"),
        ]
        result = format_project_table(projects)

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


class TestCmdInit:
    """Tests for cmd_init command handler."""

    def test_returns_zero_on_success(self):
        """cmd_init should return 0 on success."""
        args = argparse.Namespace(json=False)

        with patch("src.interface.cli.main.GetProjectContextQuery") as mock_query:
            mock_query.return_value.execute.return_value = {
                "jerry_project": None,
                "project_id": None,
                "validation": None,
                "available_projects": [],
                "next_number": 1,
            }

            result = cmd_init(args)
            assert result == 0

    def test_outputs_json_when_flag_set(self, capsys):
        """cmd_init should output JSON when --json flag is set."""
        args = argparse.Namespace(json=True)

        with patch("src.interface.cli.main.GetProjectContextQuery") as mock_query:
            mock_query.return_value.execute.return_value = {
                "jerry_project": "PROJ-001-test",
                "project_id": ProjectId.parse("PROJ-001-test"),
                "validation": ValidationResult.success(),
                "available_projects": [],
                "next_number": 2,
            }

            result = cmd_init(args)
            captured = capsys.readouterr()

            assert result == 0
            output = json.loads(captured.out)
            assert output["jerry_project"] == "PROJ-001-test"
            assert output["validation"]["is_valid"] is True


class TestCmdProjectsList:
    """Tests for cmd_projects_list command handler."""

    def test_returns_zero_on_success(self):
        """cmd_projects_list should return 0 on success."""
        args = argparse.Namespace(json=False)

        with patch("src.interface.cli.main.ScanProjectsQuery") as mock_query:
            mock_query.return_value.execute.return_value = []

            result = cmd_projects_list(args)
            assert result == 0

    def test_outputs_json_when_flag_set(self, capsys):
        """cmd_projects_list should output JSON when --json flag is set."""
        args = argparse.Namespace(json=True)

        with patch("src.interface.cli.main.ScanProjectsQuery") as mock_query:
            mock_query.return_value.execute.return_value = [
                MockProjectInfo("PROJ-001-test"),
            ]

            result = cmd_projects_list(args)
            captured = capsys.readouterr()

            assert result == 0
            output = json.loads(captured.out)
            assert output["count"] == 1
            assert len(output["projects"]) == 1


class TestCmdProjectsValidate:
    """Tests for cmd_projects_validate command handler."""

    def test_returns_zero_for_valid_project(self):
        """cmd_projects_validate should return 0 for valid project."""
        args = argparse.Namespace(json=False, project_id="PROJ-001-test")

        with patch("src.interface.cli.main.ValidateProjectQuery") as mock_query:
            mock_query.return_value.execute.return_value = (
                ProjectId.parse("PROJ-001-test"),
                ValidationResult.success(),
            )

            result = cmd_projects_validate(args)
            assert result == 0

    def test_returns_one_for_invalid_project(self):
        """cmd_projects_validate should return 1 for invalid project."""
        args = argparse.Namespace(json=False, project_id="INVALID-ID")

        with patch("src.interface.cli.main.ValidateProjectQuery") as mock_query:
            mock_query.return_value.execute.return_value = (
                None,
                ValidationResult.failure(["Invalid format"]),
            )

            result = cmd_projects_validate(args)
            assert result == 1

    def test_outputs_json_when_flag_set(self, capsys):
        """cmd_projects_validate should output JSON when --json flag is set."""
        args = argparse.Namespace(json=True, project_id="PROJ-001-test")

        with patch("src.interface.cli.main.ValidateProjectQuery") as mock_query:
            mock_query.return_value.execute.return_value = (
                ProjectId.parse("PROJ-001-test"),
                ValidationResult.success(),
            )

            result = cmd_projects_validate(args)
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
