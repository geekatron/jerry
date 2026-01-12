"""Unit tests for Jerry CLI v0.1.0 main module routing.

Test Categories:
    - Namespace Routing: Correct handler called for each namespace
    - Projects Namespace: context, list, validate commands
    - Session Namespace: Placeholder until handlers implemented
    - Items Namespace: Placeholder until handlers implemented

References:
    - ADR-CLI-002: CLI Namespace Implementation
    - Phase 4.2: Migrate projects namespace
"""

from __future__ import annotations

from unittest.mock import MagicMock, Mock, patch

from src.interface.cli.main import _handle_projects, main

# =============================================================================
# Projects Namespace Routing Tests
# =============================================================================


class TestHandleProjects:
    """Tests for _handle_projects routing function."""

    def test_routes_to_context_command(self) -> None:
        """projects context routes to cmd_projects_context."""
        mock_adapter = MagicMock()
        mock_adapter.cmd_projects_context.return_value = 0

        args = MagicMock()
        args.command = "context"

        result = _handle_projects(mock_adapter, args, json_output=False)

        assert result == 0
        mock_adapter.cmd_projects_context.assert_called_once_with(json_output=False)

    def test_routes_to_list_command(self) -> None:
        """projects list routes to cmd_projects_list."""
        mock_adapter = MagicMock()
        mock_adapter.cmd_projects_list.return_value = 0

        args = MagicMock()
        args.command = "list"

        result = _handle_projects(mock_adapter, args, json_output=False)

        assert result == 0
        mock_adapter.cmd_projects_list.assert_called_once_with(json_output=False)

    def test_routes_to_validate_command(self) -> None:
        """projects validate routes to cmd_projects_validate with project_id."""
        mock_adapter = MagicMock()
        mock_adapter.cmd_projects_validate.return_value = 0

        args = MagicMock()
        args.command = "validate"
        args.project_id = "PROJ-001-test"

        result = _handle_projects(mock_adapter, args, json_output=False)

        assert result == 0
        mock_adapter.cmd_projects_validate.assert_called_once_with(
            project_id_str="PROJ-001-test",
            json_output=False,
        )

    def test_passes_json_flag(self) -> None:
        """JSON flag is passed to adapter methods."""
        mock_adapter = MagicMock()
        mock_adapter.cmd_projects_list.return_value = 0

        args = MagicMock()
        args.command = "list"

        _handle_projects(mock_adapter, args, json_output=True)

        mock_adapter.cmd_projects_list.assert_called_once_with(json_output=True)

    def test_unknown_command_returns_error(self) -> None:
        """Unknown command returns exit code 1."""
        mock_adapter = MagicMock()

        args = MagicMock()
        args.command = "unknown"

        result = _handle_projects(mock_adapter, args, json_output=False)

        assert result == 1

    def test_no_command_returns_error(self) -> None:
        """No command (None) returns exit code 1."""
        mock_adapter = MagicMock()

        args = MagicMock()
        args.command = None

        result = _handle_projects(mock_adapter, args, json_output=False)

        assert result == 1


# =============================================================================
# Main Function Tests
# =============================================================================


class TestMainFunction:
    """Tests for main() entry point."""

    @patch("src.interface.cli.main.create_cli_adapter")
    @patch("src.interface.cli.main.create_parser")
    def test_projects_list_routes_correctly(
        self, mock_create_parser: Mock, mock_create_adapter: Mock
    ) -> None:
        """jerry projects list routes to correct handler."""
        mock_parser = MagicMock()
        mock_args = MagicMock()
        mock_args.namespace = "projects"
        mock_args.command = "list"
        mock_args.json = False
        mock_parser.parse_args.return_value = mock_args
        mock_create_parser.return_value = mock_parser

        mock_adapter = MagicMock()
        mock_adapter.cmd_projects_list.return_value = 0
        mock_create_adapter.return_value = mock_adapter

        result = main()

        assert result == 0
        mock_adapter.cmd_projects_list.assert_called_once()

    @patch("src.interface.cli.main.create_cli_adapter")
    @patch("src.interface.cli.main.create_parser")
    def test_no_namespace_shows_help_and_exits_zero(
        self, mock_create_parser: Mock, mock_create_adapter: Mock
    ) -> None:
        """No namespace shows help and exits with 0."""
        mock_parser = MagicMock()
        mock_args = MagicMock()
        mock_args.namespace = None
        mock_parser.parse_args.return_value = mock_args
        mock_create_parser.return_value = mock_parser

        result = main()

        assert result == 0
        mock_parser.print_help.assert_called_once()

    @patch("src.interface.cli.main.create_cli_adapter")
    @patch("src.interface.cli.main.create_parser")
    def test_json_flag_is_extracted(
        self, mock_create_parser: Mock, mock_create_adapter: Mock
    ) -> None:
        """--json flag is correctly extracted from args."""
        mock_parser = MagicMock()
        mock_args = MagicMock()
        mock_args.namespace = "projects"
        mock_args.command = "list"
        mock_args.json = True
        mock_parser.parse_args.return_value = mock_args
        mock_create_parser.return_value = mock_parser

        mock_adapter = MagicMock()
        mock_adapter.cmd_projects_list.return_value = 0
        mock_create_adapter.return_value = mock_adapter

        main()

        mock_adapter.cmd_projects_list.assert_called_once_with(json_output=True)


# =============================================================================
# Version Tests
# =============================================================================


class TestVersionUpdate:
    """Tests for version update to 0.1.0."""

    def test_version_is_0_1_0(self) -> None:
        """Version should be 0.1.0 for breaking change."""
        from src.interface.cli.parser import __version__

        assert __version__ == "0.1.0"
