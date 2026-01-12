"""Unit tests for CLI namespace parser.

Test Categories:
    - Parser Structure: Namespace subparsers exist
    - Session Namespace: session start/end/status/abandon
    - Items Namespace: items create/list/show/start/complete
    - Projects Namespace: projects list/validate/context
    - Edge Cases: Help flags, unknown commands

References:
    - ADR-CLI-002: CLI Namespace Implementation
    - PHASE4-R-001: 5W1H Research
"""

from __future__ import annotations

import pytest

from src.interface.cli.parser import create_parser

# =============================================================================
# Parser Structure Tests
# =============================================================================


class TestParserStructure:
    """Tests for parser namespace structure."""

    def test_parser_has_version_option(self) -> None:
        """Parser should have --version option."""
        parser = create_parser()
        with pytest.raises(SystemExit):  # --version exits
            parser.parse_args(["--version"])

    def test_parser_has_json_option(self) -> None:
        """Parser should have --json option."""
        parser = create_parser()
        args = parser.parse_args(["--json", "projects", "list"])
        assert args.json is True

    def test_parser_has_session_namespace(self) -> None:
        """Parser should have session namespace."""
        parser = create_parser()
        args = parser.parse_args(["session", "status"])
        assert args.namespace == "session"

    def test_parser_has_items_namespace(self) -> None:
        """Parser should have items namespace."""
        parser = create_parser()
        args = parser.parse_args(["items", "list"])
        assert args.namespace == "items"

    def test_parser_has_projects_namespace(self) -> None:
        """Parser should have projects namespace."""
        parser = create_parser()
        args = parser.parse_args(["projects", "list"])
        assert args.namespace == "projects"

    def test_no_command_leaves_namespace_none(self) -> None:
        """Parser with no command should leave args.namespace as None."""
        parser = create_parser()
        args = parser.parse_args([])
        assert args.namespace is None


# =============================================================================
# Session Namespace Tests
# =============================================================================


class TestSessionNamespace:
    """Tests for session namespace commands."""

    def test_session_start_command(self) -> None:
        """session start command parses correctly."""
        parser = create_parser()
        args = parser.parse_args(["session", "start"])
        assert args.namespace == "session"
        assert args.command == "start"

    def test_session_start_with_name(self) -> None:
        """session start --name parses correctly."""
        parser = create_parser()
        args = parser.parse_args(["session", "start", "--name", "Feature Work"])
        assert args.namespace == "session"
        assert args.command == "start"
        assert args.name == "Feature Work"

    def test_session_start_with_description(self) -> None:
        """session start --description parses correctly."""
        parser = create_parser()
        args = parser.parse_args(["session", "start", "--description", "Working on feature X"])
        assert args.description == "Working on feature X"

    def test_session_end_command(self) -> None:
        """session end command parses correctly."""
        parser = create_parser()
        args = parser.parse_args(["session", "end"])
        assert args.namespace == "session"
        assert args.command == "end"

    def test_session_end_with_summary(self) -> None:
        """session end --summary parses correctly."""
        parser = create_parser()
        args = parser.parse_args(["session", "end", "--summary", "Completed feature X"])
        assert args.summary == "Completed feature X"

    def test_session_status_command(self) -> None:
        """session status command parses correctly."""
        parser = create_parser()
        args = parser.parse_args(["session", "status"])
        assert args.namespace == "session"
        assert args.command == "status"

    def test_session_abandon_command(self) -> None:
        """session abandon command parses correctly."""
        parser = create_parser()
        args = parser.parse_args(["session", "abandon"])
        assert args.namespace == "session"
        assert args.command == "abandon"

    def test_session_abandon_with_reason(self) -> None:
        """session abandon --reason parses correctly."""
        parser = create_parser()
        args = parser.parse_args(["session", "abandon", "--reason", "Context compaction"])
        assert args.reason == "Context compaction"


# =============================================================================
# Items Namespace Tests
# =============================================================================


class TestItemsNamespace:
    """Tests for items namespace commands."""

    def test_items_list_command(self) -> None:
        """items list command parses correctly."""
        parser = create_parser()
        args = parser.parse_args(["items", "list"])
        assert args.namespace == "items"
        assert args.command == "list"

    def test_items_list_with_status_filter(self) -> None:
        """items list --status parses correctly."""
        parser = create_parser()
        args = parser.parse_args(["items", "list", "--status", "pending"])
        assert args.status == "pending"

    def test_items_list_with_type_filter(self) -> None:
        """items list --type parses correctly."""
        parser = create_parser()
        args = parser.parse_args(["items", "list", "--type", "task"])
        assert args.type == "task"

    def test_items_show_command(self) -> None:
        """items show <id> command parses correctly."""
        parser = create_parser()
        args = parser.parse_args(["items", "show", "WORK-001"])
        assert args.namespace == "items"
        assert args.command == "show"
        assert args.id == "WORK-001"

    def test_items_create_command(self) -> None:
        """items create <title> command parses correctly."""
        parser = create_parser()
        args = parser.parse_args(["items", "create", "Implement feature X"])
        assert args.namespace == "items"
        assert args.command == "create"
        assert args.title == "Implement feature X"

    def test_items_create_with_type(self) -> None:
        """items create --type parses correctly."""
        parser = create_parser()
        args = parser.parse_args(["items", "create", "Fix bug Y", "--type", "bug"])
        assert args.type == "bug"

    def test_items_create_with_parent(self) -> None:
        """items create --parent parses correctly."""
        parser = create_parser()
        args = parser.parse_args(["items", "create", "Subtask Z", "--parent", "WORK-001"])
        assert args.parent == "WORK-001"

    def test_items_start_command(self) -> None:
        """items start <id> command parses correctly."""
        parser = create_parser()
        args = parser.parse_args(["items", "start", "WORK-001"])
        assert args.namespace == "items"
        assert args.command == "start"
        assert args.id == "WORK-001"

    def test_items_complete_command(self) -> None:
        """items complete <id> command parses correctly."""
        parser = create_parser()
        args = parser.parse_args(["items", "complete", "WORK-001"])
        assert args.namespace == "items"
        assert args.command == "complete"
        assert args.id == "WORK-001"

    def test_items_block_command(self) -> None:
        """items block <id> --reason parses correctly."""
        parser = create_parser()
        args = parser.parse_args(
            ["items", "block", "WORK-001", "--reason", "Waiting on dependency"]
        )
        assert args.namespace == "items"
        assert args.command == "block"
        assert args.id == "WORK-001"
        assert args.reason == "Waiting on dependency"

    def test_items_cancel_command(self) -> None:
        """items cancel <id> command parses correctly."""
        parser = create_parser()
        args = parser.parse_args(["items", "cancel", "WORK-001"])
        assert args.namespace == "items"
        assert args.command == "cancel"
        assert args.id == "WORK-001"


# =============================================================================
# Projects Namespace Tests
# =============================================================================


class TestProjectsNamespace:
    """Tests for projects namespace commands."""

    def test_projects_list_command(self) -> None:
        """projects list command parses correctly."""
        parser = create_parser()
        args = parser.parse_args(["projects", "list"])
        assert args.namespace == "projects"
        assert args.command == "list"

    def test_projects_validate_command(self) -> None:
        """projects validate <project_id> command parses correctly."""
        parser = create_parser()
        args = parser.parse_args(["projects", "validate", "PROJ-001-test"])
        assert args.namespace == "projects"
        assert args.command == "validate"
        assert args.project_id == "PROJ-001-test"

    def test_projects_context_command(self) -> None:
        """projects context command parses correctly (formerly 'init')."""
        parser = create_parser()
        args = parser.parse_args(["projects", "context"])
        assert args.namespace == "projects"
        assert args.command == "context"


# =============================================================================
# Edge Cases Tests
# =============================================================================


class TestParserEdgeCases:
    """Edge case tests for parser."""

    def test_json_flag_before_namespace(self) -> None:
        """--json flag can come before namespace."""
        parser = create_parser()
        args = parser.parse_args(["--json", "session", "status"])
        assert args.json is True
        assert args.namespace == "session"

    def test_unknown_namespace_fails(self) -> None:
        """Unknown namespace should cause error."""
        parser = create_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(["unknown", "command"])

    def test_unknown_command_fails(self) -> None:
        """Unknown command in valid namespace should cause error."""
        parser = create_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(["session", "unknown"])

    def test_missing_required_arg_fails(self) -> None:
        """Missing required argument should cause error."""
        parser = create_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(["items", "show"])  # Missing id

    def test_items_block_requires_reason(self) -> None:
        """items block requires --reason argument."""
        parser = create_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(["items", "block", "WORK-001"])  # Missing --reason
