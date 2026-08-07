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
import os
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
        """ast_parse prints an error message when file does not exist."""
        ast_parse(str(nonexistent_file))
        captured = capsys.readouterr()
        assert "not found" in captured.out.lower() or "error" in captured.out.lower()

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
        """ast_render prints an error message when file does not exist."""
        ast_render(str(nonexistent_file))
        captured = capsys.readouterr()
        assert "not found" in captured.out.lower() or "error" in captured.out.lower()

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
        """ast_validate prints an error message when file does not exist."""
        ast_validate(str(nonexistent_file))
        captured = capsys.readouterr()
        assert "not found" in captured.out.lower() or "error" in captured.out.lower()

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
        """ast_query prints an error message when file does not exist."""
        ast_query(str(nonexistent_file), "heading")
        captured = capsys.readouterr()
        assert "not found" in captured.out.lower() or "error" in captured.out.lower()

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


# =============================================================================
# BUG-010 (GH #337): Path containment must anchor to the USER'S project root,
# not the plugin's own install tree. M-08/M-10 security checks stay intact.
# =============================================================================


class TestBug010ProjectRootContainment:
    """Containment anchored to CLAUDE_PROJECT_DIR/cwd, never to __file__."""

    def test_get_repo_root_when_claude_project_dir_set_then_returns_user_root(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """Root resolution honors CLAUDE_PROJECT_DIR instead of walking __file__."""
        # Arrange
        user_root = tmp_path / "user-project"
        user_root.mkdir()
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(user_root))

        # Act
        root = ast_commands_module._get_repo_root()

        # Assert
        assert root == user_root

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

        Reconciliation seam (BUG-010 T-3): pytest's tmp_path lives inside the
        real tempfile.gettempdir() (and, on Linux CI, inside the real /tmp).
        Under the widened default allowed roots, an "outside" fixture built
        from tmp_path would otherwise silently PASS containment via the temp
        default roots -- a false negative on this security-regression test.
        Neutralizing both temp defaults via monkeypatch keeps `outside`
        genuinely outside every allowed root, preserving the test's intent.
        """
        # Arrange
        monkeypatch.setattr(
            project_root_module, "_HARDCODED_TMP", tmp_path / "does-not-exist-tmp-marker"
        )
        monkeypatch.setattr(
            tempfile, "gettempdir", lambda: str(tmp_path / "controlled-tempdir-not-used-by-test")
        )
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

    def test_containment_when_symlink_escapes_project_root_then_rejected(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """M-10 preserved: symlinks pointing outside the project root are rejected.

        Reconciliation seam (BUG-010 T-3): see the seam rationale docstring
        on ``test_containment_when_file_outside_project_root_then_rejected``
        above -- the symlink target here is likewise built from tmp_path and
        would otherwise fall inside the real default temp roots.
        """
        # Arrange
        monkeypatch.setattr(
            project_root_module, "_HARDCODED_TMP", tmp_path / "does-not-exist-tmp-marker"
        )
        monkeypatch.setattr(
            tempfile, "gettempdir", lambda: str(tmp_path / "controlled-tempdir-not-used-by-test")
        )
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
    # Scope widening (PR #341 owner review, 2026-08-07): default allowed
    # roots grow to include OS temp/scratchpad dirs; --root is an
    # exclusive override. See eng-lead-implementation-plan.md T-2.
    # -------------------------------------------------------------------

    def test_containment_when_file_in_gettempdir_with_different_project_dir_then_allowed(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """Scratchpad scenario (owner's PR #341 review comment, literal repro):
        a file under tempfile.gettempdir() validates even though
        CLAUDE_PROJECT_DIR points to a completely different directory."""
        # Arrange
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path / "user-project"))
        scratch_dir = Path(tempfile.mkdtemp())
        target = scratch_dir / "scratchpad.md"
        target.write_text("# Scratch\n", encoding="utf-8")

        try:
            # Act
            resolved, error = ast_commands_module._check_path_containment(str(target))

            # Assert
            assert error is None
            assert resolved == target.resolve()
        finally:
            target.unlink(missing_ok=True)
            scratch_dir.rmdir()

    @pytest.mark.skipif(sys.platform == "win32", reason="/tmp is POSIX-only")
    def test_containment_when_file_in_slash_tmp_then_allowed(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """A file under /tmp validates by default on POSIX systems, even
        though gettempdir() may resolve elsewhere (e.g. $TMPDIR on macOS)."""
        if not Path("/tmp").exists():
            pytest.skip("/tmp does not exist on this system")

        # Arrange
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path / "user-project"))
        marker_dir = Path("/tmp") / f"jerry-test-{uuid.uuid4().hex}"
        marker_dir.mkdir()
        target = marker_dir / "scratchpad.md"
        target.write_text("# Scratch\n", encoding="utf-8")

        try:
            # Act
            resolved, error = ast_commands_module._check_path_containment(str(target))

            # Assert
            assert error is None
            assert resolved == target.resolve()
        finally:
            target.unlink(missing_ok=True)
            marker_dir.rmdir()

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
        though CLAUDE_PROJECT_DIR/tempdir defaults are irrelevant."""
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

    def test_containment_when_symlink_escapes_from_temp_root_then_rejected(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """M-10 holds even when the symlink itself sits inside an allowed
        (controlled) temp root: the target still must not escape ALL
        allowed roots, not just the project root."""
        # Arrange: fully control the allowed temp root via the T-3 seam
        controlled_tmp = tmp_path / "controlled-tmp"
        controlled_tmp.mkdir()
        monkeypatch.setattr(project_root_module, "_HARDCODED_TMP", controlled_tmp)
        monkeypatch.setattr(tempfile, "gettempdir", lambda: str(controlled_tmp))
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path / "user-project"))

        outside = tmp_path / "outside-everything"
        outside.mkdir()
        real_file = outside / "real.md"
        real_file.write_text("# Real\n", encoding="utf-8")
        link = controlled_tmp / "innocent.md"
        link.symlink_to(real_file)

        # Act
        resolved, error = ast_commands_module._check_path_containment(str(link))

        # Assert
        assert resolved is None
        assert error is not None
        assert "escapes" in error

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

    def test_ast_modify_when_root_given_and_write_target_outside_root_then_rejected_at_write_time(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """Exercises the L507-514 write-time TOCTOU recheck in isolation: the
        read step is mocked to succeed unconditionally (simulating a file
        that already passed containment at read time), proving the
        write-time recheck -- not the read-time check -- is what rejects a
        mismatched --root immediately before the write. Regression guard
        for the TOCTOU recheck being wired to the same `root` value as the
        read (WI-020, M-21)."""
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

    # -------------------------------------------------------------------
    # R-4 (owner-resolved): stderr transparency note when containment
    # matches via a temp/scratchpad root rather than the project root.
    # Must not fire for project-root or explicit --root matches.
    # -------------------------------------------------------------------

    def test_check_path_containment_when_matched_via_temp_root_then_prints_transparency_note(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """R-4: when a file passes containment only via a temp/scratchpad
        root (not the project root), a one-line stderr transparency note
        fires -- stdout (the JSON/render payload channel) stays untouched."""
        # Arrange: control the temp root via the T-3 seam so this file is
        # genuinely outside the project root and inside a known temp root.
        controlled_tmp = tmp_path / "controlled-tmp"
        controlled_tmp.mkdir()
        monkeypatch.setattr(project_root_module, "_HARDCODED_TMP", controlled_tmp)
        monkeypatch.setattr(tempfile, "gettempdir", lambda: str(controlled_tmp))
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path / "user-project"))
        target = controlled_tmp / "scratch.md"
        target.write_text("# Scratch\n", encoding="utf-8")

        # Act
        resolved, error = ast_commands_module._check_path_containment(str(target))

        # Assert
        assert error is None
        captured = capsys.readouterr()
        assert captured.out == ""
        assert "temp" in captured.err.lower()
        assert captured.err.count("\n") == 1

    def test_check_path_containment_when_matched_via_project_root_then_no_transparency_note(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """R-4: no note fires when the file matches the project root (the
        normal, expected case) -- only the temp-root fallback is noteworthy."""
        # Arrange
        user_root = tmp_path / "user-project"
        user_root.mkdir()
        target = user_root / "PLAN.md"
        target.write_text("# Plan\n", encoding="utf-8")
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(user_root))

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
        notes are scoped to the DEFAULT-set fallback, not deliberate,
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

    # -------------------------------------------------------------------
    # R-3 (owner-resolved): broad --root stderr warning propagates through
    # _check_path_containment (unit-level coverage lives in
    # test_project_root.py::TestBroadRootWarning).
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
# H-01 (RED-BUG010 red-team remediation, CWE-552/CWE-668/CWE-281): ownership
# gate for temp-default-root matches only. Multi-user temp directories
# (tempfile.gettempdir(), /tmp) are often shared and world-writable; without
# an ownership check, jerry ast would read/write another user's file on a
# shared/CI host under default configuration (no --root). The gate applies
# ONLY to temp-default-root matches -- never to the project root or an
# explicit --root match, both of which remain pure user-discretion.
# =============================================================================


class TestTempRootOwnershipGate:
    """H-01: st_uid/geteuid() ownership gate scoped to temp-default matches."""

    def test_containment_when_temp_root_file_owned_by_current_user_then_allowed(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """The dominant deployment model: a temp-root file owned by the
        current process user passes containment unchanged."""
        # Arrange
        controlled_tmp = tmp_path / "controlled-tmp"
        controlled_tmp.mkdir()
        monkeypatch.setattr(project_root_module, "_HARDCODED_TMP", controlled_tmp)
        monkeypatch.setattr(tempfile, "gettempdir", lambda: str(controlled_tmp))
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path / "user-project"))
        target = controlled_tmp / "scratch.md"
        target.write_text("# Scratch\n", encoding="utf-8")

        # Act
        resolved, error = ast_commands_module._check_path_containment(str(target))

        # Assert
        assert error is None
        assert resolved == target.resolve()

    @pytest.mark.skipif(sys.platform == "win32", reason="os.geteuid() is POSIX-only")
    def test_containment_when_temp_root_file_owned_by_other_user_then_rejected(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """A temp-root match owned by a different UID than the current
        process is REJECTED -- the H-01 fix. Simulated by monkeypatching
        os.geteuid() to return a UID guaranteed to differ from the real
        file owner, since constructing a genuinely foreign-owned file is
        not possible in a single-user CI runner."""
        # Arrange
        controlled_tmp = tmp_path / "controlled-tmp"
        controlled_tmp.mkdir()
        monkeypatch.setattr(project_root_module, "_HARDCODED_TMP", controlled_tmp)
        monkeypatch.setattr(tempfile, "gettempdir", lambda: str(controlled_tmp))
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path / "user-project"))
        target = controlled_tmp / "scratch.md"
        target.write_text("# Scratch\n", encoding="utf-8")
        real_uid = os.geteuid()
        monkeypatch.setattr(os, "geteuid", lambda: real_uid + 1)

        # Act
        resolved, error = ast_commands_module._check_path_containment(str(target))

        # Assert
        assert resolved is None
        assert error is not None
        assert "owned by another user" in error

    @pytest.mark.skipif(sys.platform == "win32", reason="os.geteuid() is POSIX-only")
    def test_containment_when_project_root_file_and_foreign_uid_then_still_allowed(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """The ownership gate is scoped strictly to temp-default-root
        matches: a project-root match is unaffected even when geteuid()
        is monkeypatched to disagree with the file's real owner."""
        # Arrange
        user_root = tmp_path / "user-project"
        user_root.mkdir()
        target = user_root / "PLAN.md"
        target.write_text("# Plan\n", encoding="utf-8")
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(user_root))
        real_uid = os.geteuid()
        monkeypatch.setattr(os, "geteuid", lambda: real_uid + 1)

        # Act
        resolved, error = ast_commands_module._check_path_containment(str(target))

        # Assert
        assert error is None
        assert resolved == target.resolve()

    @pytest.mark.skipif(sys.platform == "win32", reason="os.geteuid() is POSIX-only")
    def test_containment_when_explicit_root_file_and_foreign_uid_then_still_allowed(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """The ownership gate does not apply to an explicit --root match
        either -- that remains the user's own deliberate escape hatch."""
        # Arrange
        explicit_root = tmp_path / "explicit-root"
        explicit_root.mkdir()
        target = explicit_root / "scratch.md"
        target.write_text("# Scratch\n", encoding="utf-8")
        real_uid = os.geteuid()
        monkeypatch.setattr(os, "geteuid", lambda: real_uid + 1)

        # Act
        resolved, error = ast_commands_module._check_path_containment(
            str(target), explicit_root=str(explicit_root)
        )

        # Assert
        assert error is None
        assert resolved == target.resolve()

    def test_check_temp_root_ownership_when_owned_by_current_user_then_none(
        self, tmp_path: Path
    ) -> None:
        """Direct unit coverage of the ownership-gate helper: a
        current-user-owned file yields no error."""
        # Arrange
        target = tmp_path / "scratch.md"
        target.write_text("# Scratch\n", encoding="utf-8")

        # Act
        error = ast_commands_module._check_temp_root_ownership(target.resolve(), str(target))

        # Assert
        assert error is None

    @pytest.mark.skipif(sys.platform == "win32", reason="os.geteuid() is POSIX-only")
    def test_check_temp_root_ownership_when_owned_by_other_user_then_error(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """Direct unit coverage: a foreign-owned file yields a descriptive
        error message referencing the offending path."""
        # Arrange
        target = tmp_path / "scratch.md"
        target.write_text("# Scratch\n", encoding="utf-8")
        real_uid = os.geteuid()
        monkeypatch.setattr(os, "geteuid", lambda: real_uid + 1)

        # Act
        error = ast_commands_module._check_temp_root_ownership(target.resolve(), str(target))

        # Assert
        assert error is not None
        assert "owned by another user" in error
        assert str(target) in error

    def test_check_temp_root_ownership_when_windows_then_skipped_without_crash(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """os.geteuid() does not exist on Windows; the gate MUST be
        skipped there (guarded on os.name), never raise AttributeError.
        Windows' per-user %TEMP% already isolates temp directories by
        user under normal, non-elevated sessions."""
        # Arrange
        target = tmp_path / "scratch.md"
        target.write_text("# Scratch\n", encoding="utf-8")
        monkeypatch.setattr(os, "name", "nt")
        monkeypatch.delattr(os, "geteuid", raising=False)

        # Act
        error = ast_commands_module._check_temp_root_ownership(target.resolve(), str(target))

        # Assert
        assert error is None

    def test_check_temp_root_ownership_when_stat_oserror_then_fails_open(
        self, tmp_path: Path
    ) -> None:
        """A stat() failure (e.g. the path vanished between checks) fails
        open here -- the pre-existing size-check stat() later in
        _check_path_containment applies its own OSError handling."""
        # Arrange: a path that does not exist, so .stat() raises OSError.
        missing = tmp_path / "does-not-exist.md"

        # Act
        error = ast_commands_module._check_temp_root_ownership(missing, str(missing))

        # Assert
        assert error is None
