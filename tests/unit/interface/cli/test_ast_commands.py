# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for jerry ast CLI commands.

Tests cover:
    - AC-ST004-1: ast parse outputs valid JSON AST
    - AC-ST004-2: ast render produces roundtripped markdown
    - AC-ST004-3: ast validate reports validation results (stub)
    - AC-ST004-4: ast query returns structured data by selector
    - AC-ST004-5: Exit codes: 0 (success), 1 (validation failure), 2 (parse error)
    - AC-ST004-6: File-not-found handled with exit code 2
    - H-20: BDD test-first approach
    - H-21: 90% line coverage

Test Categories:
    - ast_parse: Happy path, JSON output, file-not-found
    - ast_render: Happy path, file-not-found
    - ast_validate: Happy path, with schema, file-not-found
    - ast_query: Happy path, JSON output, no results, file-not-found
    - token_to_dict: Helper serialization
    - node_to_dict: Helper serialization
    - CLI routing: parser and main routing
"""

from __future__ import annotations

import json
import sys
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pytest

from src.interface.cli.ast_commands import (
    ast_parse,
    ast_query,
    ast_render,
    ast_validate,
    node_to_dict,
    token_to_dict,
)
from src.interface.cli.parser import create_parser


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture()
def tmp_md_file(tmp_path: Path) -> Path:
    """Create a temporary markdown file for testing."""
    md_content = "# Hello World\n\nThis is a paragraph.\n\n> **Key:** value\n\n## Section Two\n\nMore text.\n"
    md_file = tmp_path / "test.md"
    md_file.write_text(md_content, encoding="utf-8")
    return md_file


@pytest.fixture()
def tmp_heading_file(tmp_path: Path) -> Path:
    """Create a markdown file with multiple headings."""
    md_content = "# First\n\n## Second\n\n### Third\n\nParagraph here.\n"
    md_file = tmp_path / "headings.md"
    md_file.write_text(md_content, encoding="utf-8")
    return md_file


@pytest.fixture()
def nonexistent_file(tmp_path: Path) -> Path:
    """Return a path to a file that does not exist."""
    return tmp_path / "nonexistent.md"


# =============================================================================
# token_to_dict Helper Tests
# =============================================================================


class TestTokenToDict:
    """Tests for the token_to_dict serialization helper."""

    def test_converts_basic_token_fields(self) -> None:
        """token_to_dict includes type, tag, nesting, content fields."""
        from markdown_it import MarkdownIt

        md = MarkdownIt("commonmark")
        tokens = md.parse("# Hello\n")
        # find the heading_open token
        heading_open = next(t for t in tokens if t.type == "heading_open")
        result = token_to_dict(heading_open)
        assert result["type"] == "heading_open"
        assert result["tag"] == "h1"
        assert "nesting" in result
        assert "map" in result
        assert "content" in result

    def test_map_is_list_or_none(self) -> None:
        """token_to_dict converts map to list or None."""
        from markdown_it import MarkdownIt

        md = MarkdownIt("commonmark")
        tokens = md.parse("# Hello\n")
        for token in tokens:
            result = token_to_dict(token)
            assert result["map"] is None or isinstance(result["map"], list)

    def test_content_is_string(self) -> None:
        """token_to_dict returns content as string."""
        from markdown_it import MarkdownIt

        md = MarkdownIt("commonmark")
        tokens = md.parse("Paragraph text.\n")
        for token in tokens:
            result = token_to_dict(token)
            assert isinstance(result["content"], str)


# =============================================================================
# node_to_dict Helper Tests
# =============================================================================


class TestNodeToDict:
    """Tests for the node_to_dict serialization helper."""

    def test_converts_node_type(self) -> None:
        """node_to_dict includes node type."""
        from src.domain.markdown_ast.jerry_document import JerryDocument

        doc = JerryDocument.parse("# Hello\n")
        headings = doc.query("heading")
        assert len(headings) > 0
        result = node_to_dict(headings[0])
        assert result["type"] == "heading"

    def test_includes_tag_field(self) -> None:
        """node_to_dict includes tag from opening token."""
        from src.domain.markdown_ast.jerry_document import JerryDocument

        doc = JerryDocument.parse("# Hello\n")
        headings = doc.query("heading")
        result = node_to_dict(headings[0])
        assert "tag" in result

    def test_includes_map_field(self) -> None:
        """node_to_dict includes map (line range) from opening token."""
        from src.domain.markdown_ast.jerry_document import JerryDocument

        doc = JerryDocument.parse("# Hello\n")
        headings = doc.query("heading")
        result = node_to_dict(headings[0])
        assert "map" in result

    def test_includes_content_from_inline_children(self) -> None:
        """node_to_dict extracts text content from inline children."""
        from src.domain.markdown_ast.jerry_document import JerryDocument

        doc = JerryDocument.parse("# Hello World\n")
        headings = doc.query("heading")
        result = node_to_dict(headings[0])
        assert "content" in result
        assert "Hello World" in result["content"]


# =============================================================================
# ast_parse Tests
# =============================================================================


class TestAstParse:
    """Tests for ast_parse function."""

    def test_parse_returns_exit_code_0_on_success(self, tmp_md_file: Path) -> None:
        """ast_parse returns 0 for a valid file."""
        with patch("sys.stdout", new_callable=StringIO):
            result = ast_parse(str(tmp_md_file))
        assert result == 0

    def test_parse_outputs_json_with_file_key(self, tmp_md_file: Path, capsys: pytest.CaptureFixture) -> None:
        """ast_parse outputs JSON containing file key."""
        ast_parse(str(tmp_md_file))
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "file" in data
        assert str(tmp_md_file) in data["file"]

    def test_parse_outputs_json_with_tokens_key(self, tmp_md_file: Path, capsys: pytest.CaptureFixture) -> None:
        """ast_parse outputs JSON containing tokens list."""
        ast_parse(str(tmp_md_file))
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "tokens" in data
        assert isinstance(data["tokens"], list)
        assert len(data["tokens"]) > 0

    def test_parse_outputs_json_with_tree_key(self, tmp_md_file: Path, capsys: pytest.CaptureFixture) -> None:
        """ast_parse outputs JSON containing tree with root type."""
        ast_parse(str(tmp_md_file))
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "tree" in data
        assert data["tree"]["type"] == "root"

    def test_parse_token_has_required_fields(self, tmp_md_file: Path, capsys: pytest.CaptureFixture) -> None:
        """ast_parse tokens contain type, tag, nesting, map, content fields."""
        ast_parse(str(tmp_md_file))
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        token = data["tokens"][0]
        assert "type" in token
        assert "tag" in token
        assert "nesting" in token
        assert "map" in token
        assert "content" in token

    def test_parse_file_not_found_returns_exit_code_2(self, nonexistent_file: Path, capsys: pytest.CaptureFixture) -> None:
        """ast_parse returns exit code 2 when file does not exist."""
        result = ast_parse(str(nonexistent_file))
        assert result == 2

    def test_parse_file_not_found_prints_error(self, nonexistent_file: Path, capsys: pytest.CaptureFixture) -> None:
        """ast_parse prints an error message when file does not exist."""
        ast_parse(str(nonexistent_file))
        captured = capsys.readouterr()
        assert "not found" in captured.out.lower() or "error" in captured.out.lower()

    def test_parse_output_is_valid_json(self, tmp_md_file: Path, capsys: pytest.CaptureFixture) -> None:
        """ast_parse output is parseable as JSON."""
        ast_parse(str(tmp_md_file))
        captured = capsys.readouterr()
        # Should not raise
        data = json.loads(captured.out)
        assert data is not None

    def test_parse_tree_has_children(self, tmp_md_file: Path, capsys: pytest.CaptureFixture) -> None:
        """ast_parse tree root contains children list."""
        ast_parse(str(tmp_md_file))
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "children" in data["tree"]
        assert isinstance(data["tree"]["children"], list)

    def test_parse_oserror_returns_exit_code_2(self, tmp_md_file: Path, capsys: pytest.CaptureFixture) -> None:
        """ast_parse returns 2 when file read raises OSError."""
        from unittest.mock import patch as mock_patch
        from pathlib import Path as MockPath

        with mock_patch("src.interface.cli.ast_commands.Path") as MockPathClass:
            mock_instance = MockPathClass.return_value
            mock_instance.exists.return_value = True
            mock_instance.read_text.side_effect = OSError("Permission denied")
            result = ast_parse(str(tmp_md_file))
        assert result == 2


# =============================================================================
# ast_render Tests
# =============================================================================


class TestAstRender:
    """Tests for ast_render function."""

    def test_render_returns_exit_code_0_on_success(self, tmp_md_file: Path) -> None:
        """ast_render returns 0 for a valid file."""
        with patch("sys.stdout", new_callable=StringIO):
            result = ast_render(str(tmp_md_file))
        assert result == 0

    def test_render_outputs_markdown_text(self, tmp_md_file: Path, capsys: pytest.CaptureFixture) -> None:
        """ast_render outputs non-empty markdown text."""
        ast_render(str(tmp_md_file))
        captured = capsys.readouterr()
        assert len(captured.out.strip()) > 0

    def test_render_preserves_heading(self, tmp_md_file: Path, capsys: pytest.CaptureFixture) -> None:
        """ast_render output contains the original heading content."""
        ast_render(str(tmp_md_file))
        captured = capsys.readouterr()
        assert "Hello World" in captured.out

    def test_render_file_not_found_returns_exit_code_2(self, nonexistent_file: Path, capsys: pytest.CaptureFixture) -> None:
        """ast_render returns exit code 2 when file does not exist."""
        result = ast_render(str(nonexistent_file))
        assert result == 2

    def test_render_file_not_found_prints_error(self, nonexistent_file: Path, capsys: pytest.CaptureFixture) -> None:
        """ast_render prints an error message when file does not exist."""
        ast_render(str(nonexistent_file))
        captured = capsys.readouterr()
        assert "not found" in captured.out.lower() or "error" in captured.out.lower()

    def test_render_is_idempotent_on_normalized_input(self, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
        """ast_render produces stable output for normalized markdown."""
        # Write clean normalized content
        md_file = tmp_path / "normalized.md"
        md_file.write_text("# Title\n\nBody text.\n", encoding="utf-8")
        ast_render(str(md_file))
        captured = capsys.readouterr()
        first_output = captured.out

        # Write the rendered output back and render again
        md_file2 = tmp_path / "normalized2.md"
        md_file2.write_text(first_output, encoding="utf-8")
        ast_render(str(md_file2))
        captured2 = capsys.readouterr()
        assert captured2.out == first_output


# =============================================================================
# ast_validate Tests
# =============================================================================


class TestAstValidate:
    """Tests for ast_validate function (stub)."""

    def test_validate_returns_exit_code_0_for_valid_file(self, tmp_md_file: Path) -> None:
        """ast_validate returns 0 (stub: always success for parseable file)."""
        with patch("sys.stdout", new_callable=StringIO):
            result = ast_validate(str(tmp_md_file))
        assert result == 0

    def test_validate_outputs_some_message(self, tmp_md_file: Path, capsys: pytest.CaptureFixture) -> None:
        """ast_validate outputs a result message."""
        ast_validate(str(tmp_md_file))
        captured = capsys.readouterr()
        assert len(captured.out.strip()) > 0

    def test_validate_with_unknown_schema_returns_exit_code_2(self, tmp_md_file: Path) -> None:
        """ast_validate with an unknown --schema type returns 2 (usage error)."""
        with patch("sys.stdout", new_callable=StringIO):
            result = ast_validate(str(tmp_md_file), schema="entity")
        assert result == 2

    def test_validate_with_task_schema_returns_exit_code_1_for_invalid_doc(self, tmp_md_file: Path) -> None:
        """ast_validate with --schema task returns 1 when document has violations."""
        # tmp_md_file does not have required 'Type', 'Status', etc. fields
        with patch("sys.stdout", new_callable=StringIO):
            result = ast_validate(str(tmp_md_file), schema="task")
        assert result == 1

    def test_validate_with_schema_outputs_json_report(self, tmp_md_file: Path, capsys: pytest.CaptureFixture) -> None:
        """ast_validate with --schema outputs a JSON report."""
        ast_validate(str(tmp_md_file), schema="task")
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "is_valid" in data
        assert "violations" in data
        assert "entity_type" in data
        assert data["entity_type"] == "task"

    def test_validate_with_none_schema_returns_exit_code_0(self, tmp_md_file: Path) -> None:
        """ast_validate with schema=None returns 0 (stub)."""
        with patch("sys.stdout", new_callable=StringIO):
            result = ast_validate(str(tmp_md_file), schema=None)
        assert result == 0

    def test_validate_file_not_found_returns_exit_code_2(self, nonexistent_file: Path, capsys: pytest.CaptureFixture) -> None:
        """ast_validate returns exit code 2 when file does not exist."""
        result = ast_validate(str(nonexistent_file))
        assert result == 2

    def test_validate_file_not_found_prints_error(self, nonexistent_file: Path, capsys: pytest.CaptureFixture) -> None:
        """ast_validate prints an error message when file does not exist."""
        ast_validate(str(nonexistent_file))
        captured = capsys.readouterr()
        assert "not found" in captured.out.lower() or "error" in captured.out.lower()


# =============================================================================
# ast_query Tests
# =============================================================================


class TestAstQuery:
    """Tests for ast_query function."""

    def test_query_returns_exit_code_0_on_match(self, tmp_md_file: Path) -> None:
        """ast_query returns 0 when results are found."""
        with patch("sys.stdout", new_callable=StringIO):
            result = ast_query(str(tmp_md_file), "heading")
        assert result == 0

    def test_query_outputs_json_with_selector_key(self, tmp_md_file: Path, capsys: pytest.CaptureFixture) -> None:
        """ast_query outputs JSON containing selector key."""
        ast_query(str(tmp_md_file), "heading")
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "selector" in data
        assert data["selector"] == "heading"

    def test_query_outputs_json_with_count_key(self, tmp_md_file: Path, capsys: pytest.CaptureFixture) -> None:
        """ast_query outputs JSON with count of matching nodes."""
        ast_query(str(tmp_md_file), "heading")
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "count" in data
        assert isinstance(data["count"], int)
        assert data["count"] > 0

    def test_query_outputs_json_with_nodes_key(self, tmp_md_file: Path, capsys: pytest.CaptureFixture) -> None:
        """ast_query outputs JSON with nodes list."""
        ast_query(str(tmp_md_file), "heading")
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "nodes" in data
        assert isinstance(data["nodes"], list)
        assert len(data["nodes"]) == data["count"]

    def test_query_node_has_required_fields(self, tmp_md_file: Path, capsys: pytest.CaptureFixture) -> None:
        """ast_query node objects include type, tag, map, content fields."""
        ast_query(str(tmp_md_file), "heading")
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        node = data["nodes"][0]
        assert "type" in node
        assert "tag" in node
        assert "map" in node
        assert "content" in node

    def test_query_blockquote_selector(self, tmp_md_file: Path, capsys: pytest.CaptureFixture) -> None:
        """ast_query works with blockquote selector."""
        ast_query(str(tmp_md_file), "blockquote")
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["selector"] == "blockquote"
        assert data["count"] >= 1

    def test_query_no_results_returns_exit_code_0(self, tmp_md_file: Path, capsys: pytest.CaptureFixture) -> None:
        """ast_query returns 0 even when no nodes match selector."""
        result = ast_query(str(tmp_md_file), "code_block")
        assert result == 0

    def test_query_no_results_has_count_zero(self, tmp_md_file: Path, capsys: pytest.CaptureFixture) -> None:
        """ast_query returns count=0 when no nodes match."""
        ast_query(str(tmp_md_file), "code_block")
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["count"] == 0
        assert data["nodes"] == []

    def test_query_multiple_headings(self, tmp_heading_file: Path, capsys: pytest.CaptureFixture) -> None:
        """ast_query returns all matching heading nodes."""
        ast_query(str(tmp_heading_file), "heading")
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["count"] == 3

    def test_query_file_not_found_returns_exit_code_2(self, nonexistent_file: Path, capsys: pytest.CaptureFixture) -> None:
        """ast_query returns exit code 2 when file does not exist."""
        result = ast_query(str(nonexistent_file), "heading")
        assert result == 2

    def test_query_file_not_found_prints_error(self, nonexistent_file: Path, capsys: pytest.CaptureFixture) -> None:
        """ast_query prints an error message when file does not exist."""
        ast_query(str(nonexistent_file), "heading")
        captured = capsys.readouterr()
        assert "not found" in captured.out.lower() or "error" in captured.out.lower()

    def test_query_output_is_valid_json(self, tmp_md_file: Path, capsys: pytest.CaptureFixture) -> None:
        """ast_query output is parseable as JSON."""
        ast_query(str(tmp_md_file), "heading")
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data is not None


# =============================================================================
# Parser Integration Tests
# =============================================================================


class TestParserAstNamespace:
    """Tests for ast namespace in the CLI parser."""

    def test_parser_has_ast_namespace(self) -> None:
        """Parser should have ast namespace."""
        parser = create_parser()
        args = parser.parse_args(["ast", "parse", "file.md"])
        assert args.namespace == "ast"

    def test_ast_parse_command_parses_correctly(self) -> None:
        """ast parse command parses file argument."""
        parser = create_parser()
        args = parser.parse_args(["ast", "parse", "WORKTRACKER.md"])
        assert args.command == "parse"
        assert args.file == "WORKTRACKER.md"

    def test_ast_render_command_parses_correctly(self) -> None:
        """ast render command parses file argument."""
        parser = create_parser()
        args = parser.parse_args(["ast", "render", "WORKTRACKER.md"])
        assert args.command == "render"
        assert args.file == "WORKTRACKER.md"

    def test_ast_validate_command_parses_correctly(self) -> None:
        """ast validate command parses file argument."""
        parser = create_parser()
        args = parser.parse_args(["ast", "validate", "WORKTRACKER.md"])
        assert args.command == "validate"
        assert args.file == "WORKTRACKER.md"

    def test_ast_validate_with_schema_option(self) -> None:
        """ast validate --schema option parses correctly."""
        parser = create_parser()
        args = parser.parse_args(["ast", "validate", "WORKTRACKER.md", "--schema", "entity"])
        assert args.schema == "entity"

    def test_ast_validate_schema_defaults_to_none(self) -> None:
        """ast validate --schema defaults to None."""
        parser = create_parser()
        args = parser.parse_args(["ast", "validate", "WORKTRACKER.md"])
        assert getattr(args, "schema", None) is None

    def test_ast_query_command_parses_correctly(self) -> None:
        """ast query command parses file and selector arguments."""
        parser = create_parser()
        args = parser.parse_args(["ast", "query", "WORKTRACKER.md", "blockquote"])
        assert args.command == "query"
        assert args.file == "WORKTRACKER.md"
        assert args.selector == "blockquote"

    def test_ast_no_command_leaves_command_none(self) -> None:
        """ast namespace with no subcommand leaves command as None."""
        parser = create_parser()
        args = parser.parse_args(["ast"])
        assert args.namespace == "ast"
        assert args.command is None


# =============================================================================
# Main Routing Integration Tests
# =============================================================================


class TestMainAstRouting:
    """Tests for ast namespace routing in main()."""

    def test_main_routes_ast_parse(self, tmp_md_file: Path) -> None:
        """main() routes 'ast parse' to ast_parse function."""
        from src.interface.cli.main import main

        with patch("sys.argv", ["jerry", "ast", "parse", str(tmp_md_file)]):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main()
        assert result == 0

    def test_main_routes_ast_render(self, tmp_md_file: Path) -> None:
        """main() routes 'ast render' to ast_render function."""
        from src.interface.cli.main import main

        with patch("sys.argv", ["jerry", "ast", "render", str(tmp_md_file)]):
            with patch("sys.stdout", new_callable=StringIO):
                result = main()
        assert result == 0

    def test_main_routes_ast_validate(self, tmp_md_file: Path) -> None:
        """main() routes 'ast validate' to ast_validate function."""
        from src.interface.cli.main import main

        with patch("sys.argv", ["jerry", "ast", "validate", str(tmp_md_file)]):
            with patch("sys.stdout", new_callable=StringIO):
                result = main()
        assert result == 0

    def test_main_routes_ast_query(self, tmp_md_file: Path) -> None:
        """main() routes 'ast query' to ast_query function."""
        from src.interface.cli.main import main

        with patch("sys.argv", ["jerry", "ast", "query", str(tmp_md_file), "heading"]):
            with patch("sys.stdout", new_callable=StringIO):
                result = main()
        assert result == 0

    def test_main_ast_no_command_returns_1(self) -> None:
        """main() returns 1 when ast namespace has no subcommand."""
        from src.interface.cli.main import main

        with patch("sys.argv", ["jerry", "ast"]):
            with patch("sys.stdout", new_callable=StringIO):
                result = main()
        assert result == 1

    def test_main_ast_unknown_command_returns_1(self, tmp_md_file: Path) -> None:
        """main() returns 1 for unknown ast subcommand."""
        from src.interface.cli.main import main
        import argparse

        # Simulate args with unknown command via direct call to _handle_ast
        from src.interface.cli.main import _handle_ast

        class FakeArgs:
            command = "nonexistent"
            file = str(tmp_md_file)

        with patch("sys.stdout", new_callable=StringIO):
            result = _handle_ast(FakeArgs(), json_output=False)
        assert result == 1
