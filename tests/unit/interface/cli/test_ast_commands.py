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
import tempfile
import uuid
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pytest

import src.interface.cli.ast_commands as ast_commands_module
import src.interface.cli.project_root as project_root_module
from src.interface.cli.ast_commands import (
    ast_frontmatter,
    ast_modify,
    ast_parse,
    ast_query,
    ast_reinject,
    ast_render,
    ast_validate,
    node_to_dict,
    token_to_dict,
)
from src.interface.cli.parser import create_parser

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(autouse=True)
def _disable_path_containment() -> None:
    """Disable path containment checks for CLI tests using temp files.

    Test files are created in temp directories (e.g. /tmp) which are outside
    the repository root. Path containment (WI-018, M-08) is a production
    security feature that is tested separately with dedicated test cases.
    """
    original = ast_commands_module._ENFORCE_PATH_CONTAINMENT
    ast_commands_module._ENFORCE_PATH_CONTAINMENT = False
    yield  # type: ignore[misc]
    ast_commands_module._ENFORCE_PATH_CONTAINMENT = original


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

    def test_parse_outputs_json_with_file_key(
        self, tmp_md_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_parse outputs JSON containing file key."""
        ast_parse(str(tmp_md_file))
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "file" in data
        assert str(tmp_md_file) in data["file"]

    def test_parse_outputs_json_with_tokens_key(
        self, tmp_md_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_parse outputs JSON containing tokens list."""
        ast_parse(str(tmp_md_file))
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "tokens" in data
        assert isinstance(data["tokens"], list)
        assert len(data["tokens"]) > 0

    def test_parse_outputs_json_with_tree_key(
        self, tmp_md_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_parse outputs JSON containing tree with root type."""
        ast_parse(str(tmp_md_file))
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "tree" in data
        assert data["tree"]["type"] == "root"

    def test_parse_token_has_required_fields(
        self, tmp_md_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
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

    def test_parse_file_not_found_returns_exit_code_2(
        self, nonexistent_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_parse returns exit code 2 when file does not exist."""
        result = ast_parse(str(nonexistent_file))
        assert result == 2

    def test_parse_file_not_found_prints_error(
        self, nonexistent_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_parse prints an error message to stderr (not stdout) when
        the file does not exist (GH #371: stdout must stay clean for
        JSON-consuming pipelines)."""
        ast_parse(str(nonexistent_file))
        captured = capsys.readouterr()
        assert captured.out == ""
        assert "not found" in captured.err.lower() or "error" in captured.err.lower()

    def test_parse_output_is_valid_json(
        self, tmp_md_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_parse output is parseable as JSON."""
        ast_parse(str(tmp_md_file))
        captured = capsys.readouterr()
        # Should not raise
        data = json.loads(captured.out)
        assert data is not None

    def test_parse_tree_has_children(
        self, tmp_md_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_parse tree root contains children list."""
        ast_parse(str(tmp_md_file))
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "children" in data["tree"]
        assert isinstance(data["tree"]["children"], list)

    def test_parse_oserror_returns_exit_code_2(
        self, tmp_md_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_parse returns 2 when file read raises OSError."""
        from unittest.mock import patch as mock_patch

        # Mock Path.read_text at instance level to simulate OSError
        with mock_patch.object(Path, "read_text", side_effect=OSError("Permission denied")):
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

    def test_render_outputs_markdown_text(
        self, tmp_md_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_render outputs non-empty markdown text."""
        ast_render(str(tmp_md_file))
        captured = capsys.readouterr()
        assert len(captured.out.strip()) > 0

    def test_render_preserves_heading(
        self, tmp_md_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_render output contains the original heading content."""
        ast_render(str(tmp_md_file))
        captured = capsys.readouterr()
        assert "Hello World" in captured.out

    def test_render_file_not_found_returns_exit_code_2(
        self, nonexistent_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_render returns exit code 2 when file does not exist."""
        result = ast_render(str(nonexistent_file))
        assert result == 2

    def test_render_file_not_found_prints_error(
        self, nonexistent_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_render prints an error message to stderr (not stdout) when
        the file does not exist (GH #371)."""
        ast_render(str(nonexistent_file))
        captured = capsys.readouterr()
        assert captured.out == ""
        assert "not found" in captured.err.lower() or "error" in captured.err.lower()

    def test_render_is_idempotent_on_normalized_input(
        self, tmp_path: Path, capsys: pytest.CaptureFixture
    ) -> None:
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
    """Tests for ast_validate function."""

    def test_validate_returns_exit_code_0_for_valid_file(self, tmp_md_file: Path) -> None:
        """ast_validate returns 0 for a parseable file."""
        with patch("sys.stdout", new_callable=StringIO):
            result = ast_validate(str(tmp_md_file))
        assert result == 0

    def test_validate_no_schema_outputs_json(
        self, tmp_md_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_validate without --schema outputs JSON with nav table results."""
        ast_validate(str(tmp_md_file))
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "is_valid" in data
        assert "nav_table_valid" in data
        assert "missing_nav_entries" in data
        assert "orphaned_nav_entries" in data
        assert "schema_valid" in data
        assert data["schema_valid"] is True
        assert "schema_violations" in data
        assert data["schema_violations"] == []

    def test_validate_with_unknown_schema_returns_exit_code_2(self, tmp_md_file: Path) -> None:
        """ast_validate with an unknown --schema type returns 2 (usage error)."""
        with patch("sys.stdout", new_callable=StringIO):
            result = ast_validate(str(tmp_md_file), schema="entity")
        assert result == 2

    def test_validate_with_task_schema_returns_exit_code_1_for_invalid_doc(
        self, tmp_md_file: Path
    ) -> None:
        """ast_validate with --schema task returns 1 when document has violations."""
        # tmp_md_file does not have required 'Type', 'Status', etc. fields
        with patch("sys.stdout", new_callable=StringIO):
            result = ast_validate(str(tmp_md_file), schema="task")
        assert result == 1

    def test_validate_with_schema_outputs_json_report(
        self, tmp_md_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_validate with --schema outputs a JSON report with nav table fields."""
        ast_validate(str(tmp_md_file), schema="task")
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "is_valid" in data
        assert "nav_table_valid" in data
        assert "missing_nav_entries" in data
        assert "orphaned_nav_entries" in data
        assert "schema_valid" in data
        assert "violations" in data
        assert "entity_type" in data
        assert data["entity_type"] == "task"

    def test_validate_with_none_schema_returns_exit_code_0(self, tmp_md_file: Path) -> None:
        """ast_validate with schema=None returns 0."""
        with patch("sys.stdout", new_callable=StringIO):
            result = ast_validate(str(tmp_md_file), schema=None)
        assert result == 0

    def test_validate_file_not_found_returns_exit_code_2(
        self, nonexistent_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_validate returns exit code 2 when file does not exist."""
        result = ast_validate(str(nonexistent_file))
        assert result == 2

    def test_validate_file_not_found_prints_error(
        self, nonexistent_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_validate prints an error message to stderr (not stdout) when
        the file does not exist (GH #371)."""
        ast_validate(str(nonexistent_file))
        captured = capsys.readouterr()
        assert captured.out == ""
        assert "not found" in captured.err.lower() or "error" in captured.err.lower()

    def test_validate_with_unknown_schema_prints_error_to_stderr_only(
        self, tmp_md_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_validate with an unknown --schema type prints the error to
        stderr, leaving stdout empty (GH #371: unknown-schema is a
        diagnostic, not a JSON payload)."""
        result = ast_validate(str(tmp_md_file), schema="entity")
        captured = capsys.readouterr()
        assert result == 2
        assert captured.out == ""
        assert "error" in captured.err.lower()

    def test_validate_nav_flag_includes_entries(
        self, tmp_path: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_validate --nav includes detailed nav table entries."""
        md = (
            "# Title\n\n"
            "| Section | Purpose |\n"
            "|---------|----------|\n"
            "| [Details](#details) | Info |\n\n"
            "## Details\n\nSome text.\n"
        )
        md_file = tmp_path / "nav.md"
        md_file.write_text(md, encoding="utf-8")
        ast_validate(str(md_file), nav=True)
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "nav_entries" in data
        assert isinstance(data["nav_entries"], list)
        assert len(data["nav_entries"]) > 0
        entry = data["nav_entries"][0]
        assert "section_name" in entry
        assert "anchor" in entry
        assert "description" in entry
        assert "line_number" in entry

    def test_validate_no_nav_flag_excludes_entries(
        self, tmp_md_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_validate without --nav does not include nav_entries key."""
        ast_validate(str(tmp_md_file))
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "nav_entries" not in data

    def test_validate_with_schema_and_nav_includes_entries(
        self, tmp_path: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_validate with --schema AND --nav includes nav_entries in output."""
        md = (
            "# TASK-099 Test Task\n\n"
            "> **Type:** task\n"
            "> **Status:** pending\n"
            "> **Priority:** medium\n"
            "> **Created:** 2026-02-23\n"
            "> **Parent:** FEAT-001\n\n"
            "| Section | Purpose |\n"
            "|---------|----------|\n"
            "| [Summary](#summary) | Overview |\n\n"
            "## Summary\n\nThis is a test task.\n"
        )
        md_file = tmp_path / "task.md"
        md_file.write_text(md, encoding="utf-8")
        ast_validate(str(md_file), schema="task", nav=True)
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "nav_entries" in data
        assert isinstance(data["nav_entries"], list)
        assert len(data["nav_entries"]) > 0
        entry = data["nav_entries"][0]
        assert "section_name" in entry
        assert "anchor" in entry
        assert "description" in entry
        assert "line_number" in entry

    def test_validate_with_schema_returns_exit_code_0_for_valid_doc(
        self, tmp_path: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_validate with --schema returns 0 when document passes validation."""
        md = (
            "# TASK-100 Valid Task\n\n"
            "> **Type:** task\n"
            "> **Status:** pending\n"
            "> **Priority:** high\n"
            "> **Created:** 2026-02-23\n"
            "> **Parent:** FEAT-001\n\n"
            "| Section | Purpose |\n"
            "|---------|----------|\n"
            "| [Summary](#summary) | Overview |\n\n"
            "## Summary\n\nA fully valid task document.\n"
        )
        md_file = tmp_path / "valid-task.md"
        md_file.write_text(md, encoding="utf-8")
        result = ast_validate(str(md_file), schema="task")
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert result == 0
        assert data["is_valid"] is True
        assert data["schema_valid"] is True
        assert data["violations"] == []


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

    def test_query_outputs_json_with_selector_key(
        self, tmp_md_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_query outputs JSON containing selector key."""
        ast_query(str(tmp_md_file), "heading")
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "selector" in data
        assert data["selector"] == "heading"

    def test_query_outputs_json_with_count_key(
        self, tmp_md_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_query outputs JSON with count of matching nodes."""
        ast_query(str(tmp_md_file), "heading")
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "count" in data
        assert isinstance(data["count"], int)
        assert data["count"] > 0

    def test_query_outputs_json_with_nodes_key(
        self, tmp_md_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_query outputs JSON with nodes list."""
        ast_query(str(tmp_md_file), "heading")
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "nodes" in data
        assert isinstance(data["nodes"], list)
        assert len(data["nodes"]) == data["count"]

    def test_query_node_has_required_fields(
        self, tmp_md_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_query node objects include type, tag, map, content fields."""
        ast_query(str(tmp_md_file), "heading")
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        node = data["nodes"][0]
        assert "type" in node
        assert "tag" in node
        assert "map" in node
        assert "content" in node

    def test_query_blockquote_selector(
        self, tmp_md_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_query works with blockquote selector."""
        ast_query(str(tmp_md_file), "blockquote")
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["selector"] == "blockquote"
        assert data["count"] >= 1

    def test_query_no_results_returns_exit_code_0(
        self, tmp_md_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_query returns 0 even when no nodes match selector."""
        result = ast_query(str(tmp_md_file), "code_block")
        assert result == 0

    def test_query_no_results_has_count_zero(
        self, tmp_md_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_query returns count=0 when no nodes match."""
        ast_query(str(tmp_md_file), "code_block")
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["count"] == 0
        assert data["nodes"] == []

    def test_query_multiple_headings(
        self, tmp_heading_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_query returns all matching heading nodes."""
        ast_query(str(tmp_heading_file), "heading")
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["count"] == 3

    def test_query_file_not_found_returns_exit_code_2(
        self, nonexistent_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_query returns exit code 2 when file does not exist."""
        result = ast_query(str(nonexistent_file), "heading")
        assert result == 2

    def test_query_file_not_found_prints_error(
        self, nonexistent_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_query prints an error message to stderr (not stdout) when
        the file does not exist (GH #371)."""
        ast_query(str(nonexistent_file), "heading")
        captured = capsys.readouterr()
        assert captured.out == ""
        assert "not found" in captured.err.lower() or "error" in captured.err.lower()

    def test_query_output_is_valid_json(
        self, tmp_md_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_query output is parseable as JSON."""
        ast_query(str(tmp_md_file), "heading")
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data is not None


# =============================================================================
# ast_frontmatter Tests
# =============================================================================


class TestAstFrontmatter:
    """Tests for ast_frontmatter function."""

    def test_frontmatter_returns_exit_code_0(self, tmp_md_file: Path) -> None:
        """ast_frontmatter returns 0 for a valid file with frontmatter."""
        with patch("sys.stdout", new_callable=StringIO):
            result = ast_frontmatter(str(tmp_md_file))
        assert result == 0

    def test_frontmatter_outputs_json_dict(
        self, tmp_md_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_frontmatter outputs a JSON object with frontmatter fields."""
        ast_frontmatter(str(tmp_md_file))
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert isinstance(data, dict)
        assert data.get("Key") == "value"

    def test_frontmatter_empty_for_no_frontmatter(
        self, tmp_path: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_frontmatter returns {} for files without frontmatter."""
        plain_file = tmp_path / "plain.md"
        plain_file.write_text("# Just heading\n\nNo frontmatter.\n", encoding="utf-8")
        ast_frontmatter(str(plain_file))
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data == {}

    def test_frontmatter_file_not_found(
        self, nonexistent_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_frontmatter returns exit code 2 for missing file."""
        result = ast_frontmatter(str(nonexistent_file))
        assert result == 2

    def test_frontmatter_output_is_valid_json(
        self, tmp_md_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_frontmatter output is parseable as JSON."""
        ast_frontmatter(str(tmp_md_file))
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data is not None


# =============================================================================
# ast_modify Tests
# =============================================================================


class TestAstModify:
    """Tests for ast_modify function."""

    @pytest.fixture()
    def tmp_entity_file(self, tmp_path: Path) -> Path:
        """Create a temporary file with blockquote frontmatter."""
        md = "# Test Entity\n\n> **Status:** pending\n> **Type:** story\n\n## Details\n\nContent.\n"
        f = tmp_path / "entity.md"
        f.write_text(md, encoding="utf-8")
        return f

    def test_modify_returns_exit_code_0(self, tmp_entity_file: Path) -> None:
        """ast_modify returns 0 on successful modification."""
        with patch("sys.stdout", new_callable=StringIO):
            result = ast_modify(str(tmp_entity_file), "Status", "done")
        assert result == 0

    def test_modify_writes_file_back(self, tmp_entity_file: Path) -> None:
        """ast_modify writes the modified content back to disk."""
        with patch("sys.stdout", new_callable=StringIO):
            ast_modify(str(tmp_entity_file), "Status", "done")
        content = tmp_entity_file.read_text(encoding="utf-8")
        assert "done" in content

    def test_modify_outputs_json_status(
        self, tmp_entity_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_modify outputs JSON with file, key, value, status fields."""
        ast_modify(str(tmp_entity_file), "Status", "done")
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["key"] == "Status"
        assert data["value"] == "done"
        assert data["status"] == "modified"

    def test_modify_preserves_other_fields(self, tmp_entity_file: Path) -> None:
        """ast_modify preserves other frontmatter fields."""
        with patch("sys.stdout", new_callable=StringIO):
            ast_modify(str(tmp_entity_file), "Status", "done")
        content = tmp_entity_file.read_text(encoding="utf-8")
        assert "story" in content

    def test_modify_missing_key_returns_exit_code_1(
        self, tmp_entity_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_modify returns 1 when key does not exist in frontmatter."""
        result = ast_modify(str(tmp_entity_file), "NonExistent", "value")
        assert result == 1

    def test_modify_missing_key_prints_error_to_stderr_only(
        self, tmp_entity_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_modify prints the key-not-found error to stderr, leaving
        stdout empty (GH #371)."""
        result = ast_modify(str(tmp_entity_file), "NonExistent", "value")
        captured = capsys.readouterr()
        assert result == 1
        assert captured.out == ""
        assert "not found" in captured.err.lower()

    def test_modify_file_not_found(
        self, nonexistent_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_modify returns exit code 2 for missing file."""
        result = ast_modify(str(nonexistent_file), "Status", "done")
        assert result == 2


# =============================================================================
# ast_reinject Tests
# =============================================================================


class TestAstReinject:
    """Tests for ast_reinject function."""

    @pytest.fixture()
    def tmp_reinject_file(self, tmp_path: Path) -> Path:
        """Create a temporary file with L2-REINJECT directives."""
        md = (
            "# Rule File\n\n"
            '<!-- L2-REINJECT: rank=1, tokens=50, content="Test content here for reinject." -->\n\n'
            "## Section\n\nText.\n"
        )
        f = tmp_path / "rules.md"
        f.write_text(md, encoding="utf-8")
        return f

    def test_reinject_returns_exit_code_0(self, tmp_reinject_file: Path) -> None:
        """ast_reinject returns 0 on success."""
        with patch("sys.stdout", new_callable=StringIO):
            result = ast_reinject(str(tmp_reinject_file))
        assert result == 0

    def test_reinject_outputs_json_list(
        self, tmp_reinject_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_reinject outputs a JSON list of directives."""
        ast_reinject(str(tmp_reinject_file))
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert isinstance(data, list)
        assert len(data) > 0

    def test_reinject_directive_has_required_fields(
        self, tmp_reinject_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_reinject directives contain rank, tokens, content, line_number."""
        ast_reinject(str(tmp_reinject_file))
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        directive = data[0]
        assert "rank" in directive
        assert "tokens" in directive
        assert "content" in directive
        assert "line_number" in directive

    def test_reinject_empty_for_no_directives(
        self, tmp_path: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_reinject returns [] for files without directives."""
        plain_file = tmp_path / "plain.md"
        plain_file.write_text("# No directives\n\nJust text.\n", encoding="utf-8")
        ast_reinject(str(plain_file))
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data == []

    def test_reinject_file_not_found(
        self, nonexistent_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_reinject returns exit code 2 for missing file."""
        result = ast_reinject(str(nonexistent_file))
        assert result == 2


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

    def test_ast_validate_nav_flag(self) -> None:
        """ast validate --nav flag parses correctly."""
        parser = create_parser()
        args = parser.parse_args(["ast", "validate", "WORKTRACKER.md", "--nav"])
        assert args.nav is True

    def test_ast_validate_nav_defaults_to_false(self) -> None:
        """ast validate --nav defaults to False."""
        parser = create_parser()
        args = parser.parse_args(["ast", "validate", "WORKTRACKER.md"])
        assert args.nav is False

    def test_ast_query_command_parses_correctly(self) -> None:
        """ast query command parses file and selector arguments."""
        parser = create_parser()
        args = parser.parse_args(["ast", "query", "WORKTRACKER.md", "blockquote"])
        assert args.command == "query"
        assert args.file == "WORKTRACKER.md"
        assert args.selector == "blockquote"

    def test_ast_frontmatter_command_parses_correctly(self) -> None:
        """ast frontmatter command parses file argument."""
        parser = create_parser()
        args = parser.parse_args(["ast", "frontmatter", "file.md"])
        assert args.command == "frontmatter"
        assert args.file == "file.md"

    def test_ast_modify_command_parses_correctly(self) -> None:
        """ast modify command parses file, --key, --value arguments."""
        parser = create_parser()
        args = parser.parse_args(["ast", "modify", "file.md", "--key", "Status", "--value", "done"])
        assert args.command == "modify"
        assert args.file == "file.md"
        assert args.key == "Status"
        assert args.value == "done"

    def test_ast_reinject_command_parses_correctly(self) -> None:
        """ast reinject command parses file argument."""
        parser = create_parser()
        args = parser.parse_args(["ast", "reinject", "file.md"])
        assert args.command == "reinject"
        assert args.file == "file.md"

    def test_ast_no_command_leaves_command_none(self) -> None:
        """ast namespace with no subcommand leaves command as None."""
        parser = create_parser()
        args = parser.parse_args(["ast"])
        assert args.namespace == "ast"
        assert args.command is None

    # -------------------------------------------------------------------
    # BUG-010 scope widening (T-5): --root flag on every ast subcommand.
    # -------------------------------------------------------------------

    def test_ast_root_flag_parses_correctly(self) -> None:
        """--root flag value is parsed onto args.root."""
        parser = create_parser()
        args = parser.parse_args(["ast", "parse", "file.md", "--root", "/some/dir"])
        assert args.root == "/some/dir"

    def test_ast_root_flag_defaults_to_none(self) -> None:
        """--root flag defaults to None when omitted."""
        parser = create_parser()
        args = parser.parse_args(["ast", "parse", "file.md"])
        assert getattr(args, "root", None) is None

    @pytest.mark.parametrize(
        ("command", "extra_args"),
        [
            ("parse", ["file.md"]),
            ("render", ["file.md"]),
            ("validate", ["file.md"]),
            ("query", ["file.md", "heading"]),
            ("frontmatter", ["file.md"]),
            ("modify", ["file.md", "--key", "Status", "--value", "done"]),
            ("reinject", ["file.md"]),
            ("detect", ["file.md"]),
            ("sections", ["file.md"]),
            ("metadata", ["file.md"]),
        ],
    )
    def test_ast_root_flag_available_on_every_subcommand(
        self, command: str, extra_args: list[str]
    ) -> None:
        """--root is available and parses identically on all 10 ast
        subcommands. Prevents silent drift if a future subcommand is added
        without the flag."""
        parser = create_parser()
        args = parser.parse_args(["ast", command, *extra_args, "--root", "/x"])
        assert args.root == "/x"

    def test_add_root_argument_docstring_does_not_reference_removed_temp_scratchpad_default(
        self,
    ) -> None:
        """A-4 (BUG-010 C4 tournament, eng-reviewer F-1/CC-006): the
        ``_add_root_argument`` docstring must not claim the default
        allowed roots include "OS temp/scratchpad directories" -- that
        behavior was REMOVED under Option C (no directory is auto-
        trusted). The docstring must describe the actual Option C
        default: the project root plus explicitly-configured
        ``ast.trusted_roots``, matching the ``--help`` text already
        generated below it."""
        from src.interface.cli import parser as parser_module

        docstring = parser_module._add_root_argument.__doc__ or ""
        # The stale claim was that OS temp/scratchpad dirs are part of
        # the default allowed set -- that phrasing must be gone.
        assert "plus os temp" not in docstring.lower()
        assert "plus temp" not in docstring.lower()
        # The correct Option C model must be present instead.
        assert "trusted_roots" in docstring

    # -------------------------------------------------------------------
    # BUG-010 Option C, C6: --quiet flag on every ast subcommand.
    # -------------------------------------------------------------------

    def test_ast_quiet_flag_defaults_to_false(self) -> None:
        """--quiet flag defaults to False when omitted."""
        parser = create_parser()
        args = parser.parse_args(["ast", "parse", "file.md"])
        assert args.quiet is False

    def test_ast_quiet_flag_parses_correctly(self) -> None:
        """--quiet flag sets args.quiet to True when supplied."""
        parser = create_parser()
        args = parser.parse_args(["ast", "parse", "file.md", "--quiet"])
        assert args.quiet is True

    @pytest.mark.parametrize(
        ("command", "extra_args"),
        [
            ("parse", ["file.md"]),
            ("render", ["file.md"]),
            ("validate", ["file.md"]),
            ("query", ["file.md", "heading"]),
            ("frontmatter", ["file.md"]),
            ("modify", ["file.md", "--key", "Status", "--value", "done"]),
            ("reinject", ["file.md"]),
            ("detect", ["file.md"]),
            ("sections", ["file.md"]),
            ("metadata", ["file.md"]),
        ],
    )
    def test_ast_quiet_flag_available_on_every_subcommand(
        self, command: str, extra_args: list[str]
    ) -> None:
        """--quiet is available and parses identically on all 10 ast
        subcommands. Prevents silent drift if a future subcommand is added
        without the flag."""
        parser = create_parser()
        args = parser.parse_args(["ast", command, *extra_args, "--quiet"])
        assert args.quiet is True


# =============================================================================
# Main Routing Integration Tests
# =============================================================================


class TestMainAstRouting:
    """Tests for ast namespace routing in main()."""

    def test_main_routes_ast_parse(self, tmp_md_file: Path) -> None:
        """main() routes 'ast parse' to ast_parse function."""
        from src.interface.cli.main import main

        with patch("sys.argv", ["jerry", "ast", "parse", str(tmp_md_file)]):
            with patch("sys.stdout", new_callable=StringIO):
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

    def test_main_routes_ast_frontmatter(self, tmp_md_file: Path) -> None:
        """main() routes 'ast frontmatter' to ast_frontmatter function."""
        from src.interface.cli.main import main

        with patch("sys.argv", ["jerry", "ast", "frontmatter", str(tmp_md_file)]):
            with patch("sys.stdout", new_callable=StringIO):
                result = main()
        assert result == 0

    def test_main_routes_ast_modify(self, tmp_path: Path) -> None:
        """main() routes 'ast modify' to ast_modify function."""
        from src.interface.cli.main import main

        md = "# Entity\n\n> **Status:** pending\n\n## Details\n"
        f = tmp_path / "entity.md"
        f.write_text(md, encoding="utf-8")

        with patch(
            "sys.argv", ["jerry", "ast", "modify", str(f), "--key", "Status", "--value", "done"]
        ):
            with patch("sys.stdout", new_callable=StringIO):
                result = main()
        assert result == 0

    def test_main_routes_ast_reinject(self, tmp_md_file: Path) -> None:
        """main() routes 'ast reinject' to ast_reinject function."""
        from src.interface.cli.main import main

        with patch("sys.argv", ["jerry", "ast", "reinject", str(tmp_md_file)]):
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

    def test_main_ast_no_command_prints_error_to_stderr_only(
        self, capsys: pytest.CaptureFixture
    ) -> None:
        """main() with a bare 'jerry ast' (no subcommand) prints the
        'No ast command specified' diagnostic to stderr, leaving stdout
        empty (GH #371: the router's own diagnostic print was missed by
        the original ast_commands.py-scoped fix)."""
        from src.interface.cli.main import main

        with patch("sys.argv", ["jerry", "ast"]):
            result = main()
        captured = capsys.readouterr()
        assert result == 1
        assert captured.out == ""
        assert "no ast command specified" in captured.err.lower()

    def test_main_ast_unknown_command_returns_1(self, tmp_md_file: Path) -> None:
        """main() returns 1 for unknown ast subcommand."""

        # Simulate args with unknown command via direct call to _handle_ast
        from src.interface.cli.main import _handle_ast

        class FakeArgs:
            command = "nonexistent"
            file = str(tmp_md_file)

        with patch("sys.stdout", new_callable=StringIO):
            result = _handle_ast(FakeArgs(), json_output=False)
        assert result == 1

    def test_handle_ast_unknown_command_prints_error_to_stderr_only(
        self, tmp_md_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """_handle_ast prints the 'Unknown ast command' diagnostic to
        stderr, leaving stdout empty (GH #371, same defect class as the
        no-subcommand case: a router-level diagnostic, not a JSON/render
        payload)."""
        from src.interface.cli.main import _handle_ast

        class FakeArgs:
            command = "nonexistent"
            file = str(tmp_md_file)

        result = _handle_ast(FakeArgs(), json_output=False)
        captured = capsys.readouterr()
        assert result == 1
        assert captured.out == ""
        assert "unknown ast command" in captured.err.lower()

    # -------------------------------------------------------------------
    # BUG-010 scope widening (T-6): --root pass-through in main().
    # -------------------------------------------------------------------

    def test_main_routes_ast_parse_with_root_flag(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """main() threads --root through to ast_parse; a --root that DOES
        contain the file allows it, with containment actually enforced."""
        from src.interface.cli.main import main

        monkeypatch.setattr(ast_commands_module, "_ENFORCE_PATH_CONTAINMENT", True)
        root_dir = tmp_path / "allowed-root"
        root_dir.mkdir()
        md_file = root_dir / "test.md"
        md_file.write_text("# Hello\n", encoding="utf-8")

        with patch("sys.argv", ["jerry", "ast", "parse", str(md_file), "--root", str(root_dir)]):
            with patch("sys.stdout", new_callable=StringIO):
                result = main()
        assert result == 0

    def test_main_routes_ast_parse_with_root_flag_rejects_outside_root(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """main() threads --root through to ast_parse; a --root that does
        NOT contain the file is rejected (exit code 2)."""
        from src.interface.cli.main import main

        monkeypatch.setattr(ast_commands_module, "_ENFORCE_PATH_CONTAINMENT", True)
        md_file = tmp_path / "test.md"
        md_file.write_text("# Hello\n", encoding="utf-8")
        unrelated_root = tmp_path / "unrelated-root"
        unrelated_root.mkdir()

        with patch(
            "sys.argv", ["jerry", "ast", "parse", str(md_file), "--root", str(unrelated_root)]
        ):
            with patch("sys.stdout", new_callable=StringIO):
                result = main()
        assert result == 2

    # -------------------------------------------------------------------
    # BUG-010 Option C, C6: --quiet pass-through in main().
    # -------------------------------------------------------------------

    def test_main_routes_ast_parse_with_quiet_flag_suppresses_broad_root_warning(
        self,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """main() threads --quiet through to ast_parse; a broad --root
        (the filesystem/drive root, portable via Path.anchor) would
        normally warn on stderr, but --quiet suppresses it."""
        from src.interface.cli.main import main

        monkeypatch.setattr(ast_commands_module, "_ENFORCE_PATH_CONTAINMENT", True)
        md_file = tmp_path / "test.md"
        md_file.write_text("# Hello\n", encoding="utf-8")

        with patch(
            "sys.argv",
            ["jerry", "ast", "parse", str(md_file), "--root", str(tmp_path.anchor), "--quiet"],
        ):
            with patch("sys.stdout", new_callable=StringIO):
                result = main()
        assert result == 0
        captured = capsys.readouterr()
        assert captured.err == ""


# =============================================================================
# BUG-010 (GH #337): Path containment must anchor to the USER'S project root,
# not the plugin's own install tree. M-08/M-10 security checks stay intact.
# =============================================================================


class TestBug010ProjectRootContainment:
    """Containment anchored to CLAUDE_PROJECT_DIR/cwd, never to __file__.

    BUG-010 Option C: the default allowed set is the project root plus
    zero-or-more user-declared ``ast.trusted_roots`` entries -- no
    directory is auto-trusted. Tests use
    ``monkeypatch.setattr(project_root_module, "_load_trusted_roots", ...)``
    as the seam for controlling configured trusted roots (replacing the
    removed ``_HARDCODED_TMP``/``tempfile.gettempdir()`` monkeypatch seam).
    """

    def _no_configured_roots(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Force _load_trusted_roots() to return an empty list for this test."""
        monkeypatch.setattr(project_root_module, "_load_trusted_roots", lambda: [])

    def test_containment_when_file_in_user_project_then_allowed(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """A file inside the user's project root validates even though it is far
        outside the Jerry install tree (the exact GH #337 repro)."""
        # Arrange
        user_root = tmp_path / "user-project"
        (user_root / "projects" / "PROJ-001-example").mkdir(parents=True)
        target = user_root / "projects" / "PROJ-001-example" / "PLAN.md"
        target.write_text("# Plan\n", encoding="utf-8")
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(user_root))

        # Act
        resolved, error = ast_commands_module._check_path_containment(str(target))

        # Assert
        assert error is None
        assert resolved == target.resolve()

    def test_containment_when_relative_path_in_cwd_project_then_allowed(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """Relative paths resolve against cwd and pass when cwd is the project root."""
        # Arrange
        monkeypatch.delenv("CLAUDE_PROJECT_DIR", raising=False)
        monkeypatch.chdir(tmp_path)
        target = tmp_path / "PLAN.md"
        target.write_text("# Plan\n", encoding="utf-8")

        # Act
        resolved, error = ast_commands_module._check_path_containment("PLAN.md")

        # Assert
        assert error is None
        assert resolved == target.resolve()

    def test_containment_when_file_outside_project_root_then_rejected(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """M-08 preserved: paths outside the resolved project root are rejected.

        BUG-010 Option C: no directory is auto-trusted, so an "outside"
        fixture built from tmp_path is genuinely outside every allowed
        root (project root + zero configured trusted roots) without
        needing to neutralize any temp-default seam.
        """
        # Arrange
        self._no_configured_roots(monkeypatch)
        user_root = tmp_path / "user-project"
        user_root.mkdir()
        outside = tmp_path / "elsewhere"
        outside.mkdir()
        target = outside / "escape.md"
        target.write_text("# Escape\n", encoding="utf-8")
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(user_root))

        # Act
        resolved, error = ast_commands_module._check_path_containment(str(target))

        # Assert
        assert resolved is None
        assert error is not None
        assert "escapes" in error

    def test_containment_when_file_outside_project_root_then_error_includes_remediation_hint(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """A-6 (BUG-010 C4 tournament, FM-007, optional): the containment-
        escape error carries a short actionable remediation hint (how to
        grant access) rather than just stating the rejection."""
        # Arrange
        self._no_configured_roots(monkeypatch)
        user_root = tmp_path / "user-project"
        user_root.mkdir()
        outside = tmp_path / "elsewhere"
        outside.mkdir()
        target = outside / "escape.md"
        target.write_text("# Escape\n", encoding="utf-8")
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(user_root))

        # Act
        resolved, error = ast_commands_module._check_path_containment(str(target))

        # Assert
        assert resolved is None
        assert error is not None
        assert "trusted_roots" in error or "--root" in error

    @pytest.mark.skipif(
        sys.platform == "win32", reason="symlink creation requires elevated privileges on Windows"
    )
    def test_containment_when_symlink_escapes_project_root_then_rejected(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """M-10 preserved: symlinks pointing outside the project root are
        rejected. BUG-010 Option C: no auto-trusted temp default exists,
        so the symlink target here is genuinely outside every allowed
        root without needing a neutralizing seam."""
        # Arrange
        self._no_configured_roots(monkeypatch)
        user_root = tmp_path / "user-project"
        user_root.mkdir()
        outside = tmp_path / "secret"
        outside.mkdir()
        real_file = outside / "real.md"
        real_file.write_text("# Real\n", encoding="utf-8")
        link = user_root / "innocent.md"
        link.symlink_to(real_file)
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(user_root))

        # Act
        resolved, error = ast_commands_module._check_path_containment(str(link))

        # Assert
        assert resolved is None
        assert error is not None
        assert "escapes" in error

    # -------------------------------------------------------------------
    # BUG-010 Option C: default allowed roots are the project root plus
    # zero-or-more user-declared ast.trusted_roots entries; --root is an
    # exclusive override. See eng-lead-option-c-plan.md Section 4.C.
    # -------------------------------------------------------------------

    def test_containment_when_file_in_configured_trusted_root_then_allowed(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """A file under a user-declared ast.trusted_roots entry validates
        even though CLAUDE_PROJECT_DIR points to a different directory."""
        # Arrange
        user_root = tmp_path / "user-project"
        user_root.mkdir()
        trusted_dir = tmp_path / "scratchpad"
        trusted_dir.mkdir()
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(user_root))
        monkeypatch.setattr(project_root_module, "_load_trusted_roots", lambda: [str(trusted_dir)])
        target = trusted_dir / "scratch.md"
        target.write_text("# Scratch\n", encoding="utf-8")

        # Act
        resolved, error = ast_commands_module._check_path_containment(str(target))

        # Assert
        assert error is None
        assert resolved == target.resolve()

    def test_containment_when_file_in_gettempdir_and_not_configured_then_rejected(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """CRITICAL negative regression: a file under tempfile.gettempdir()
        is REJECTED by default -- the prior always-widen behavior is
        removed. Only an explicitly configured ast.trusted_roots entry
        (or --root) grants access outside the project root."""
        # Arrange
        self._no_configured_roots(monkeypatch)
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path / "user-project"))
        scratch_dir = Path(tempfile.mkdtemp())
        target = scratch_dir / "scratchpad.md"
        target.write_text("# Scratch\n", encoding="utf-8")

        try:
            # Act
            resolved, error = ast_commands_module._check_path_containment(str(target))

            # Assert
            assert resolved is None
            assert error is not None
            assert "escapes" in error
        finally:
            target.unlink(missing_ok=True)
            scratch_dir.rmdir()

    @pytest.mark.skipif(sys.platform == "win32", reason="/tmp is POSIX-only")
    def test_containment_when_file_in_slash_tmp_and_not_configured_then_rejected(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """Negative regression: a file under /tmp is REJECTED by default on
        POSIX systems -- /tmp is never auto-trusted under Option C."""
        if not Path("/tmp").exists():
            pytest.skip("/tmp does not exist on this system")

        # Arrange
        self._no_configured_roots(monkeypatch)
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path / "user-project"))
        marker_dir = Path("/tmp") / f"jerry-test-{uuid.uuid4().hex}"
        marker_dir.mkdir()
        target = marker_dir / "scratchpad.md"
        target.write_text("# Scratch\n", encoding="utf-8")

        try:
            # Act
            resolved, error = ast_commands_module._check_path_containment(str(target))

            # Assert
            assert resolved is None
            assert error is not None
            assert "escapes" in error
        finally:
            target.unlink(missing_ok=True)
            marker_dir.rmdir()

    @pytest.mark.skipif(
        sys.platform == "win32", reason="symlink creation requires elevated privileges on Windows"
    )
    def test_containment_when_symlink_target_in_configured_root_then_allowed(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """M-10: a symlink whose target resolves inside a configured
        trusted root is allowed, even when the symlink itself lives
        elsewhere (e.g. inside the project root)."""
        # Arrange
        trusted_dir = tmp_path / "configured-trusted"
        trusted_dir.mkdir()
        user_root = tmp_path / "user-project"
        user_root.mkdir()
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(user_root))
        monkeypatch.setattr(project_root_module, "_load_trusted_roots", lambda: [str(trusted_dir)])
        real_file = trusted_dir / "real.md"
        real_file.write_text("# Real\n", encoding="utf-8")
        link = user_root / "innocent.md"
        link.symlink_to(real_file)

        # Act
        resolved, error = ast_commands_module._check_path_containment(str(link))

        # Assert
        assert error is None
        assert resolved == link.resolve()

    @pytest.mark.skipif(
        sys.platform == "win32", reason="symlink creation requires elevated privileges on Windows"
    )
    def test_containment_when_symlink_escapes_all_configured_roots_then_rejected(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """M-10 holds even when the symlink itself sits inside an allowed
        (configured) root: the target still must not escape ALL allowed
        roots, not just the project root."""
        # Arrange
        configured_root = tmp_path / "configured-trusted"
        configured_root.mkdir()
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path / "user-project"))
        monkeypatch.setattr(
            project_root_module, "_load_trusted_roots", lambda: [str(configured_root)]
        )

        outside = tmp_path / "outside-everything"
        outside.mkdir()
        real_file = outside / "real.md"
        real_file.write_text("# Real\n", encoding="utf-8")
        link = configured_root / "innocent.md"
        link.symlink_to(real_file)

        # Act
        resolved, error = ast_commands_module._check_path_containment(str(link))

        # Assert
        assert resolved is None
        assert error is not None
        assert "escapes" in error

    def test_containment_when_explicit_root_given_then_file_in_project_root_rejected(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """--root exclusivity (CRITICAL): a file inside the project root is
        REJECTED when an unrelated --root is supplied. Proves --root is a
        true override, not additive."""
        # Arrange
        user_root = tmp_path / "user-project"
        user_root.mkdir()
        target = user_root / "PLAN.md"
        target.write_text("# Plan\n", encoding="utf-8")
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(user_root))
        other_root = tmp_path / "unrelated"
        other_root.mkdir()

        # Act
        resolved, error = ast_commands_module._check_path_containment(
            str(target), explicit_root=str(other_root)
        )

        # Assert
        assert resolved is None
        assert error is not None
        assert "escapes" in error

    def test_containment_when_explicit_root_given_then_file_in_explicit_root_allowed(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """Companion positive case: a matching --root allows the file even
        though CLAUDE_PROJECT_DIR/configured trusted roots are irrelevant."""
        # Arrange
        user_root = tmp_path / "user-project"
        user_root.mkdir()
        target = user_root / "PLAN.md"
        target.write_text("# Plan\n", encoding="utf-8")
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path / "different-project"))

        # Act
        resolved, error = ast_commands_module._check_path_containment(
            str(target), explicit_root=str(user_root)
        )

        # Assert
        assert error is None
        assert resolved == target.resolve()

    def test_read_file_when_root_argument_provided_then_threaded_to_containment_check(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """_read_file threads its root argument through to the containment
        check at the _read_file boundary, independent of any ast_* caller."""
        # Arrange
        monkeypatch.setattr(ast_commands_module, "_ENFORCE_PATH_CONTAINMENT", True)
        explicit_root = tmp_path / "allowed-root"
        explicit_root.mkdir()
        target = explicit_root / "doc.md"
        target.write_text("# Doc\n", encoding="utf-8")
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path / "different-project"))

        # Act
        content, exit_code = ast_commands_module._read_file(str(target), root=str(explicit_root))

        # Assert
        assert exit_code == 0
        assert content is not None

        # Negative companion: a mismatched root rejects the same file.
        content2, exit_code2 = ast_commands_module._read_file(
            str(target), root=str(tmp_path / "unrelated")
        )
        assert exit_code2 == 2
        assert content2 is None

    def test_read_file_when_containment_escape_then_error_printed_to_stderr_only(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """GH #371: the read-time containment-escape diagnostic
        (``Error: Path escapes allowed containment roots: ...``) MUST be
        printed to stderr, not stdout -- a consumer piping ``jerry ast``
        output to a JSON parser (e.g. ``jq``) must never see diagnostic
        text mixed into stdout."""
        # Arrange
        self._no_configured_roots(monkeypatch)
        monkeypatch.setattr(ast_commands_module, "_ENFORCE_PATH_CONTAINMENT", True)
        user_root = tmp_path / "user-project"
        user_root.mkdir()
        outside = tmp_path / "elsewhere"
        outside.mkdir()
        target = outside / "escape.md"
        target.write_text("# Escape\n", encoding="utf-8")
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(user_root))

        # Act
        content, exit_code = ast_commands_module._read_file(str(target))

        # Assert
        assert exit_code == 2
        assert content is None
        captured = capsys.readouterr()
        assert captured.out == ""
        assert "escapes" in captured.err.lower()
        assert ast_commands_module._CONTAINMENT_ESCAPE_HINT in captured.err

    def test_ast_modify_when_root_given_and_write_target_outside_root_then_rejected_at_write_time(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """Exercises the write-time TOCTOU recheck in isolation: the read
        step is mocked to succeed unconditionally (simulating a file that
        already passed containment at read time), proving the write-time
        recheck -- not the read-time check -- is what rejects a mismatched
        --root immediately before the write. Regression guard for the
        TOCTOU recheck being wired to the same `root` value as the read
        (WI-020, M-21)."""
        # Arrange
        monkeypatch.setattr(ast_commands_module, "_ENFORCE_PATH_CONTAINMENT", True)
        user_root = tmp_path / "user-project"
        user_root.mkdir()
        target = user_root / "entity.md"
        original = "# Entity\n\n> **Status:** pending\n\n## Details\n"
        target.write_text(original, encoding="utf-8")
        unrelated_root = tmp_path / "unrelated"
        unrelated_root.mkdir()

        with patch.object(ast_commands_module, "_read_file", return_value=(original, 0)):
            # Act
            result = ast_modify(str(target), "Status", "done", root=str(unrelated_root))

        # Assert
        assert result == 2
        assert target.read_text(encoding="utf-8") == original  # unmodified

    @pytest.mark.skipif(
        sys.platform == "win32", reason="symlink creation requires elevated privileges on Windows"
    )
    def test_ast_modify_when_symlink_swapped_between_read_and_write_then_rejected_at_write_time(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """C2 fix, the actual TOCTOU attack: a symlink resolves inside an
        allowed root at read time, then is repointed outside all allowed
        roots before the write executes. Because the write-time recheck
        calls the IDENTICAL _check_path_containment function used at read
        time (fresh os.path.realpath() resolution every call), the swap
        is caught and the write is rejected -- the file on disk is
        unmodified."""
        # Arrange
        monkeypatch.setattr(ast_commands_module, "_ENFORCE_PATH_CONTAINMENT", True)
        user_root = tmp_path / "user-project"
        user_root.mkdir()
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(user_root))
        self._no_configured_roots(monkeypatch)

        original = "# Entity\n\n> **Status:** pending\n\n## Details\n"
        inside_target = user_root / "real-inside.md"
        inside_target.write_text(original, encoding="utf-8")

        outside_dir = tmp_path / "outside-everything"
        outside_dir.mkdir()
        outside_target = outside_dir / "real-outside.md"
        outside_target.write_text(original, encoding="utf-8")

        link = user_root / "entity.md"
        link.symlink_to(inside_target)

        # Read succeeds: symlink currently resolves inside the project root.
        source, read_exit_code = ast_commands_module._read_file(str(link))
        assert read_exit_code == 0
        assert source == original

        # Attacker swaps the symlink to point outside all allowed roots
        # between the read and the write.
        link.unlink()
        link.symlink_to(outside_target)

        # Act: ast_modify re-reads (mocked to reuse the already-read
        # source, simulating a single logical invocation) then performs
        # its own write-time recheck, which must re-resolve the live
        # (now-swapped) symlink target.
        with patch.object(ast_commands_module, "_read_file", return_value=(source, 0)):
            result = ast_modify(str(link), "Status", "done")

        # Assert
        assert result == 2
        assert outside_target.read_text(encoding="utf-8") == original  # unmodified
        assert inside_target.read_text(encoding="utf-8") == original  # unmodified

    @pytest.mark.skipif(
        sys.platform == "win32", reason="symlink creation requires elevated privileges on Windows"
    )
    def test_ast_modify_when_write_time_escape_rejected_then_error_includes_containment_hint(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Regression guard: the write-time containment-escape error (A-1
        TOCTOU recheck) must carry the same `_CONTAINMENT_ESCAPE_HINT`
        (``configure ast.trusted_roots or pass --root``) that the
        read-time escape messages in `_check_path_containment` already
        carry (added by A-6), so a user hitting the write-time escape
        gets the same actionable remediation guidance as one hitting the
        read-time escape. Reuses the symlink-swap harness: a symlink that
        resolves inside an allowed root at read time, then is repointed
        outside all allowed roots before the write-time recheck runs."""
        # Arrange
        monkeypatch.setattr(ast_commands_module, "_ENFORCE_PATH_CONTAINMENT", True)
        user_root = tmp_path / "user-project"
        user_root.mkdir()
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(user_root))
        self._no_configured_roots(monkeypatch)

        original = "# Entity\n\n> **Status:** pending\n\n## Details\n"
        inside_target = user_root / "real-inside.md"
        inside_target.write_text(original, encoding="utf-8")

        outside_dir = tmp_path / "outside-everything"
        outside_dir.mkdir()
        outside_target = outside_dir / "real-outside.md"
        outside_target.write_text(original, encoding="utf-8")

        link = user_root / "entity.md"
        link.symlink_to(inside_target)

        # Read succeeds: symlink currently resolves inside the project root.
        source, read_exit_code = ast_commands_module._read_file(str(link))
        assert read_exit_code == 0
        assert source == original

        # Attacker swaps the symlink to point outside all allowed roots
        # between the read and the write.
        link.unlink()
        link.symlink_to(outside_target)

        # Act
        with patch.object(ast_commands_module, "_read_file", return_value=(source, 0)):
            result = ast_modify(str(link), "Status", "done")

        # Assert
        assert result == 2
        captured = capsys.readouterr()
        assert captured.out == ""
        assert ast_commands_module._CONTAINMENT_ESCAPE_HINT in captured.err

    @pytest.mark.skipif(
        sys.platform == "win32", reason="symlink creation requires elevated privileges on Windows"
    )
    def test_ast_modify_when_write_time_check_resolves_swapped_target_then_write_lands_on_validated_path(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """A-1 regression (CWE-367 write-path check!=use TOCTOU): the write
        destination must be EXACTLY the resolved path the write-time
        containment check validates -- never a separately-resolved value
        captured before the check ran. Both the pre-swap and post-swap
        symlink targets live inside the allowed root (so the write-time
        check accepts either), which isolates the assertion to "which file
        receives the write" rather than accept/reject. Simulates the TOCTOU
        window (a swap occurring between the removed line-620 naive
        resolve() and the write-time recheck) by re-pointing the symlink
        the instant `_check_path_containment` is invoked -- i.e. as late as
        possible before the check performs its own fresh resolution. Prior
        to the fix, `target_path` was captured via a separate, earlier
        `Path(file_path).resolve()` call that would still observe the
        pre-swap target here (since nothing swaps the link before that
        earlier call runs), so this test is RED against the pre-fix code:
        the write would land on `pre_swap_target` instead of the
        check-validated `post_swap_target`."""
        # Arrange
        monkeypatch.setattr(ast_commands_module, "_ENFORCE_PATH_CONTAINMENT", True)
        user_root = tmp_path / "user-project"
        user_root.mkdir()
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(user_root))
        self._no_configured_roots(monkeypatch)

        original = "# Entity\n\n> **Status:** pending\n\n## Details\n"
        pre_swap_target = user_root / "pre-swap.md"
        pre_swap_target.write_text(original, encoding="utf-8")
        post_swap_target = user_root / "post-swap.md"
        post_swap_target.write_text(original, encoding="utf-8")

        link = user_root / "entity.md"
        link.symlink_to(pre_swap_target)

        real_check = ast_commands_module._check_path_containment

        def swap_then_check(
            file_path: str, explicit_root: str | None = None, quiet: bool = False
        ) -> tuple[Path | None, str | None]:
            # Simulate an attacker re-pointing the symlink in the TOCTOU
            # window between the (now-removed) naive resolve and this
            # check's own fresh resolution.
            link.unlink()
            link.symlink_to(post_swap_target)
            return real_check(file_path, explicit_root, quiet)

        monkeypatch.setattr(ast_commands_module, "_check_path_containment", swap_then_check)

        with patch.object(ast_commands_module, "_read_file", return_value=(original, 0)):
            # Act
            result = ast_modify(str(link), "Status", "done")

        # Assert
        assert result == 0
        assert "done" in post_swap_target.read_text(encoding="utf-8")
        assert pre_swap_target.read_text(encoding="utf-8") == original  # unmodified

    def test_ast_modify_when_configured_root_match_then_transparency_note_prints_exactly_once(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Regression proving the quiet=True internal write-time recheck
        does not double-print the R-4 transparency note: it fires once at
        read time (via _read_file) and is suppressed at write time (DD-3)."""
        # Arrange
        monkeypatch.setattr(ast_commands_module, "_ENFORCE_PATH_CONTAINMENT", True)
        user_root = tmp_path / "user-project"
        user_root.mkdir()
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(user_root))
        trusted_dir = tmp_path / "configured-trusted"
        trusted_dir.mkdir()
        monkeypatch.setattr(project_root_module, "_load_trusted_roots", lambda: [str(trusted_dir)])
        target = trusted_dir / "entity.md"
        original = "# Entity\n\n> **Status:** pending\n\n## Details\n"
        target.write_text(original, encoding="utf-8")

        # Act
        result = ast_modify(str(target), "Status", "done")

        # Assert
        assert result == 0
        captured = capsys.readouterr()
        assert captured.err.count("configured trusted root") == 1

    # -------------------------------------------------------------------
    # R-4 (generalized, BUG-010 Option C): stderr transparency note when
    # containment matches via a configured trusted root rather than the
    # project root. Must not fire for project-root or explicit --root
    # matches.
    # -------------------------------------------------------------------

    def test_check_path_containment_when_matched_via_configured_root_then_prints_generalized_transparency_note(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """R-4: when a file passes containment only via a configured
        trusted root (not the project root), a one-line stderr
        transparency note fires -- stdout (the JSON/render payload
        channel) stays untouched."""
        # Arrange
        trusted_dir = tmp_path / "configured-trusted"
        trusted_dir.mkdir()
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path / "user-project"))
        monkeypatch.setattr(project_root_module, "_load_trusted_roots", lambda: [str(trusted_dir)])
        target = trusted_dir / "scratch.md"
        target.write_text("# Scratch\n", encoding="utf-8")

        # Act
        resolved, error = ast_commands_module._check_path_containment(str(target))

        # Assert
        assert error is None
        captured = capsys.readouterr()
        assert captured.out == ""
        assert "configured trusted root" in captured.err.lower()
        assert captured.err.count("\n") == 1

    def test_check_path_containment_when_matched_via_project_root_then_no_transparency_note(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """R-4: no note fires when the file matches the project root (the
        normal, expected case) -- only a configured-root match is
        noteworthy."""
        # Arrange
        user_root = tmp_path / "user-project"
        user_root.mkdir()
        target = user_root / "PLAN.md"
        target.write_text("# Plan\n", encoding="utf-8")
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(user_root))
        self._no_configured_roots(monkeypatch)

        # Act
        resolved, error = ast_commands_module._check_path_containment(str(target))

        # Assert
        assert error is None
        captured = capsys.readouterr()
        assert captured.err == ""

    def test_check_path_containment_when_explicit_root_given_then_no_transparency_note(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """R-4: no note fires for an explicit --root match, even when the
        supplied root happens to be a temp-like directory -- transparency
        notes are scoped to the configured-root fallback, not deliberate,
        explicit user choice via --root."""
        # Arrange
        explicit_root = tmp_path / "explicit-temp-like-root"
        explicit_root.mkdir()
        target = explicit_root / "scratch.md"
        target.write_text("# Scratch\n", encoding="utf-8")

        # Act
        resolved, error = ast_commands_module._check_path_containment(
            str(target), explicit_root=str(explicit_root)
        )

        # Assert
        assert error is None
        captured = capsys.readouterr()
        assert captured.err == ""

    def test_check_path_containment_when_quiet_true_then_suppresses_transparency_note(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """C6: quiet=True suppresses the R-4 configured-root transparency
        note."""
        # Arrange
        trusted_dir = tmp_path / "configured-trusted"
        trusted_dir.mkdir()
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path / "user-project"))
        monkeypatch.setattr(project_root_module, "_load_trusted_roots", lambda: [str(trusted_dir)])
        target = trusted_dir / "scratch.md"
        target.write_text("# Scratch\n", encoding="utf-8")

        # Act
        resolved, error = ast_commands_module._check_path_containment(str(target), quiet=True)

        # Assert
        assert error is None
        captured = capsys.readouterr()
        assert captured.out == ""
        assert captured.err == ""

    def test_check_path_containment_when_quiet_true_then_suppresses_broad_root_warning(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """C6: quiet=True suppresses the R-3 broad-root warning, propagated
        through the _check_path_containment boundary."""
        # Arrange
        target = tmp_path / "file.md"
        target.write_text("# File\n", encoding="utf-8")

        # Act
        ast_commands_module._check_path_containment(
            str(target), explicit_root=str(tmp_path.anchor), quiet=True
        )

        # Assert
        captured = capsys.readouterr()
        assert captured.err == ""

    # -------------------------------------------------------------------
    # R-3 (owner-resolved): broad --root stderr warning propagates through
    # _check_path_containment (unit-level coverage lives in
    # test_project_root.py::TestGetContainmentRoots).
    # -------------------------------------------------------------------

    def test_check_path_containment_when_explicit_root_is_broad_then_warns(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """A broad --root (filesystem/drive root, detected portably via
        Path.anchor) triggers the R-3 stderr warning through the full
        _check_path_containment call path."""
        # Arrange
        target = tmp_path / "file.md"
        target.write_text("# File\n", encoding="utf-8")

        # Act
        ast_commands_module._check_path_containment(str(target), explicit_root=str(tmp_path.anchor))

        # Assert
        captured = capsys.readouterr()
        assert "Warning" in captured.err


# =============================================================================
# DD-2 (owner-resolved: remove entirely): the H-01 ownership gate
# (_check_temp_root_ownership, _is_temp_default_root_match,
# _warn_if_temp_root_match) is deleted outright, not retained. Its sole
# rationale -- safe auto-trust of shared, multi-tenant OS temp
# directories -- no longer exists under Option C: a "configured" root is
# never auto-trusted, it is a deliberate user declaration, structurally
# identical in trust posture to --root (which has never had an ownership
# gate). This regression guard replaces the deleted
# TestTempRootOwnershipGate class (8 tests) to prevent silent
# reintroduction of the removed machinery.
# =============================================================================


class TestOwnershipGateRemoved:
    """DD-2: guard against silent reintroduction of the removed H-01 gate."""

    def test_ast_commands_module_when_imported_then_check_temp_root_ownership_is_not_defined(
        self,
    ) -> None:
        """_check_temp_root_ownership (and its supporting helpers) must not
        exist on the ast_commands module -- Option C removes temp-default
        auto-trust entirely, so the gate that protected it has no
        remaining rationale."""
        assert not hasattr(ast_commands_module, "_check_temp_root_ownership")
        assert not hasattr(ast_commands_module, "_is_temp_default_root_match")
        assert not hasattr(ast_commands_module, "_warn_if_temp_root_match")

    def test_ast_commands_module_when_imported_then_get_repo_root_is_not_defined(self) -> None:
        """A-5 (BUG-010 C4 tournament, SR-005): ``_get_repo_root`` is dead
        code -- its sole caller was its own dedicated test (now removed);
        path containment is computed from ``project_root.get_containment_roots``,
        not from this legacy single-root convenience accessor. Guard
        against silent reintroduction."""
        assert not hasattr(ast_commands_module, "_get_repo_root")
