# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for skills/ast/scripts/ast_ops.py.

Tests cover all public functions in the /ast skill script wrapper:
    - parse_file: Read and parse markdown, return structured info
    - query_frontmatter: Extract frontmatter fields as dict
    - modify_frontmatter: Modify a frontmatter field and write back
    - validate_file: Validate file structure (nav table + stub schema)
    - render_file: Parse and render normalized markdown
    - extract_reinject: Extract L2-REINJECT directives
    - validate_nav_table_file: Validate nav table compliance

Test categories:
    - Happy path: Valid files, expected outputs
    - Negative: File not found, empty file, no frontmatter, missing key
    - Edge cases: File with only frontmatter, file with reinject + nav table

References:
    - ST-005: /ast Claude Skill
    - H-20: BDD test-first (RED phase written before implementation)
    - H-21: 90% line coverage required
"""

from __future__ import annotations

import os
import tempfile

import pytest

from skills.ast.scripts.ast_ops import (
    extract_reinject,
    modify_frontmatter,
    parse_file,
    query_frontmatter,
    render_file,
    validate_file,
    validate_nav_table_file,
)


# ---------------------------------------------------------------------------
# Fixtures: temp file helpers
# ---------------------------------------------------------------------------


def _write_temp(content: str, suffix: str = ".md") -> str:
    """Write content to a temporary file and return its absolute path."""
    fd, path = tempfile.mkstemp(suffix=suffix)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(content)
    return path


# ---------------------------------------------------------------------------
# Fixtures: content strings
# ---------------------------------------------------------------------------

SIMPLE_FRONTMATTER_MD = """\
# ST-005: Implement AST Skill

> **Type:** story
> **Status:** pending
> **Priority:** high
> **Owner:** alice

## Overview

Some overview content here.
"""

NO_FRONTMATTER_MD = """\
# Plain Document

## Section One

No frontmatter here.

## Section Two

Just content.
"""

EMPTY_MD = ""

NAV_TABLE_MD = """\
# My Document

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | What this covers |
| [Details](#details) | Deep dive |

## Overview

Content here.

## Details

More content.
"""

REINJECT_MD = """\
# Rule File

<!-- L2-REINJECT: rank=1, tokens=50, content="Constitutional: No recursive subagents." -->

## Rules

Some rules here.

<!-- L2-REINJECT: rank=2, tokens=30, content="UV only for Python." -->
"""

FULL_VALID_MD = """\
# Full Document

> **Type:** story
> **Status:** pending

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | Summary |

<!-- L2-REINJECT: rank=1, tokens=20, content="Test rule." -->

## Overview

Content.
"""


# ---------------------------------------------------------------------------
# parse_file tests
# ---------------------------------------------------------------------------


class TestParseFile:
    """Tests for parse_file()."""

    @pytest.mark.happy_path
    def test_parse_returns_dict(self) -> None:
        """parse_file returns a dict with expected keys."""
        path = _write_temp(SIMPLE_FRONTMATTER_MD)
        try:
            result = parse_file(path)
            assert isinstance(result, dict)
            assert "file_path" in result
            assert "source_length" in result
            assert "node_types" in result
            assert "heading_count" in result
            assert "has_frontmatter" in result
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_parse_detects_frontmatter(self) -> None:
        """parse_file detects frontmatter presence."""
        path = _write_temp(SIMPLE_FRONTMATTER_MD)
        try:
            result = parse_file(path)
            assert result["has_frontmatter"] is True
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_parse_no_frontmatter(self) -> None:
        """parse_file correctly reports no frontmatter."""
        path = _write_temp(NO_FRONTMATTER_MD)
        try:
            result = parse_file(path)
            assert result["has_frontmatter"] is False
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_parse_counts_headings(self) -> None:
        """parse_file counts headings correctly."""
        path = _write_temp(SIMPLE_FRONTMATTER_MD)
        try:
            result = parse_file(path)
            # SIMPLE_FRONTMATTER_MD has "# ST-005..." and "## Overview"
            assert result["heading_count"] >= 2
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_parse_returns_file_path(self) -> None:
        """parse_file echoes back the absolute file path."""
        path = _write_temp(SIMPLE_FRONTMATTER_MD)
        try:
            result = parse_file(path)
            assert result["file_path"] == path
        finally:
            os.unlink(path)

    @pytest.mark.edge_case
    def test_parse_empty_file(self) -> None:
        """parse_file handles empty files gracefully."""
        path = _write_temp(EMPTY_MD)
        try:
            result = parse_file(path)
            assert result["source_length"] == 0
            assert result["has_frontmatter"] is False
            assert result["heading_count"] == 0
        finally:
            os.unlink(path)

    @pytest.mark.negative
    def test_parse_file_not_found(self) -> None:
        """parse_file raises FileNotFoundError for missing files."""
        with pytest.raises(FileNotFoundError):
            parse_file("/nonexistent/path/to/file.md")


# ---------------------------------------------------------------------------
# query_frontmatter tests
# ---------------------------------------------------------------------------


class TestQueryFrontmatter:
    """Tests for query_frontmatter()."""

    @pytest.mark.happy_path
    def test_query_returns_dict(self) -> None:
        """query_frontmatter returns a dict of key-value pairs."""
        path = _write_temp(SIMPLE_FRONTMATTER_MD)
        try:
            result = query_frontmatter(path)
            assert isinstance(result, dict)
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_query_extracts_all_fields(self) -> None:
        """query_frontmatter extracts all frontmatter key-value pairs."""
        path = _write_temp(SIMPLE_FRONTMATTER_MD)
        try:
            result = query_frontmatter(path)
            assert result["Type"] == "story"
            assert result["Status"] == "pending"
            assert result["Priority"] == "high"
            assert result["Owner"] == "alice"
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_query_no_frontmatter_returns_empty_dict(self) -> None:
        """query_frontmatter returns empty dict when no frontmatter present."""
        path = _write_temp(NO_FRONTMATTER_MD)
        try:
            result = query_frontmatter(path)
            assert result == {}
        finally:
            os.unlink(path)

    @pytest.mark.edge_case
    def test_query_empty_file_returns_empty_dict(self) -> None:
        """query_frontmatter returns empty dict for empty files."""
        path = _write_temp(EMPTY_MD)
        try:
            result = query_frontmatter(path)
            assert result == {}
        finally:
            os.unlink(path)

    @pytest.mark.negative
    def test_query_file_not_found(self) -> None:
        """query_frontmatter raises FileNotFoundError for missing files."""
        with pytest.raises(FileNotFoundError):
            query_frontmatter("/nonexistent/path/to/file.md")


# ---------------------------------------------------------------------------
# modify_frontmatter tests
# ---------------------------------------------------------------------------


class TestModifyFrontmatter:
    """Tests for modify_frontmatter()."""

    @pytest.mark.happy_path
    def test_modify_returns_new_content(self) -> None:
        """modify_frontmatter returns the new file content as a string."""
        path = _write_temp(SIMPLE_FRONTMATTER_MD)
        try:
            result = modify_frontmatter(path, "Status", "in-progress")
            assert isinstance(result, str)
            assert "in-progress" in result
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_modify_writes_to_file(self) -> None:
        """modify_frontmatter writes the modified content back to the file."""
        path = _write_temp(SIMPLE_FRONTMATTER_MD)
        try:
            modify_frontmatter(path, "Status", "done")
            with open(path, encoding="utf-8") as f:
                content = f.read()
            assert "done" in content
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_modify_preserves_other_fields(self) -> None:
        """modify_frontmatter preserves unmodified frontmatter fields."""
        path = _write_temp(SIMPLE_FRONTMATTER_MD)
        try:
            result = modify_frontmatter(path, "Status", "done")
            assert "Type" in result
            assert "Priority" in result
            assert "Owner" in result
        finally:
            os.unlink(path)

    @pytest.mark.negative
    def test_modify_missing_key_raises(self) -> None:
        """modify_frontmatter raises KeyError when the key does not exist."""
        path = _write_temp(SIMPLE_FRONTMATTER_MD)
        try:
            with pytest.raises(KeyError):
                modify_frontmatter(path, "NonExistentKey", "value")
        finally:
            os.unlink(path)

    @pytest.mark.negative
    def test_modify_no_frontmatter_raises(self) -> None:
        """modify_frontmatter raises KeyError when the file has no frontmatter."""
        path = _write_temp(NO_FRONTMATTER_MD)
        try:
            with pytest.raises(KeyError):
                modify_frontmatter(path, "Status", "done")
        finally:
            os.unlink(path)

    @pytest.mark.negative
    def test_modify_file_not_found(self) -> None:
        """modify_frontmatter raises FileNotFoundError for missing files."""
        with pytest.raises(FileNotFoundError):
            modify_frontmatter("/nonexistent/path/to/file.md", "Status", "done")


# ---------------------------------------------------------------------------
# validate_file tests
# ---------------------------------------------------------------------------


class TestValidateFile:
    """Tests for validate_file()."""

    @pytest.mark.happy_path
    def test_validate_returns_dict(self) -> None:
        """validate_file returns a dict with validation result keys."""
        path = _write_temp(NAV_TABLE_MD)
        try:
            result = validate_file(path)
            assert isinstance(result, dict)
            assert "is_valid" in result
            assert "nav_table_valid" in result
            assert "missing_nav_entries" in result
            assert "orphaned_nav_entries" in result
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_validate_valid_nav_table(self) -> None:
        """validate_file marks a document with valid nav table as valid."""
        path = _write_temp(NAV_TABLE_MD)
        try:
            result = validate_file(path)
            assert result["nav_table_valid"] is True
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_validate_no_schema_uses_stub(self) -> None:
        """validate_file with no schema arg uses stub validation (always pass)."""
        path = _write_temp(SIMPLE_FRONTMATTER_MD)
        try:
            result = validate_file(path)
            assert "schema_valid" in result
            # Stub: schema_valid is always True when no schema provided
            assert result["schema_valid"] is True
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_validate_with_schema_returns_schema_valid_key(self) -> None:
        """validate_file with a schema arg returns schema_valid and schema_violations keys."""
        path = _write_temp(SIMPLE_FRONTMATTER_MD)
        try:
            result = validate_file(path, schema="story")
            assert "schema_valid" in result
            assert "schema_violations" in result
            # SIMPLE_FRONTMATTER_MD is missing required story fields,
            # so schema_valid should be False with real validation.
            assert result["schema_valid"] is False
            assert len(result["schema_violations"]) > 0
        finally:
            os.unlink(path)

    @pytest.mark.negative
    def test_validate_missing_nav_table(self) -> None:
        """validate_file detects missing nav table."""
        path = _write_temp(SIMPLE_FRONTMATTER_MD)
        try:
            result = validate_file(path)
            assert result["nav_table_valid"] is False
        finally:
            os.unlink(path)

    @pytest.mark.negative
    def test_validate_file_not_found(self) -> None:
        """validate_file raises FileNotFoundError for missing files."""
        with pytest.raises(FileNotFoundError):
            validate_file("/nonexistent/path/to/file.md")

    @pytest.mark.edge_case
    def test_validate_empty_file(self) -> None:
        """validate_file handles empty file without crashing."""
        path = _write_temp(EMPTY_MD)
        try:
            result = validate_file(path)
            assert isinstance(result, dict)
            assert result["nav_table_valid"] is False
        finally:
            os.unlink(path)


# ---------------------------------------------------------------------------
# render_file tests
# ---------------------------------------------------------------------------


class TestRenderFile:
    """Tests for render_file()."""

    @pytest.mark.happy_path
    def test_render_returns_string(self) -> None:
        """render_file returns a string."""
        path = _write_temp(SIMPLE_FRONTMATTER_MD)
        try:
            result = render_file(path)
            assert isinstance(result, str)
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_render_content_preserved(self) -> None:
        """render_file preserves the key content of the markdown."""
        path = _write_temp(SIMPLE_FRONTMATTER_MD)
        try:
            result = render_file(path)
            assert "ST-005" in result
            assert "Overview" in result
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_render_is_idempotent(self) -> None:
        """render_file output is idempotent (rendering twice gives same result)."""
        path = _write_temp(SIMPLE_FRONTMATTER_MD)
        try:
            first = render_file(path)
            # Write rendered content back and render again
            with open(path, "w", encoding="utf-8") as f:
                f.write(first)
            second = render_file(path)
            assert first == second
        finally:
            os.unlink(path)

    @pytest.mark.edge_case
    def test_render_empty_file_returns_empty_string(self) -> None:
        """render_file returns empty string for empty file."""
        path = _write_temp(EMPTY_MD)
        try:
            result = render_file(path)
            assert result == ""
        finally:
            os.unlink(path)

    @pytest.mark.negative
    def test_render_file_not_found(self) -> None:
        """render_file raises FileNotFoundError for missing files."""
        with pytest.raises(FileNotFoundError):
            render_file("/nonexistent/path/to/file.md")


# ---------------------------------------------------------------------------
# extract_reinject tests
# ---------------------------------------------------------------------------


class TestExtractReinject:
    """Tests for extract_reinject()."""

    @pytest.mark.happy_path
    def test_extract_returns_list(self) -> None:
        """extract_reinject returns a list of dicts."""
        path = _write_temp(REINJECT_MD)
        try:
            result = extract_reinject(path)
            assert isinstance(result, list)
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_extract_finds_all_directives(self) -> None:
        """extract_reinject finds all L2-REINJECT directives."""
        path = _write_temp(REINJECT_MD)
        try:
            result = extract_reinject(path)
            assert len(result) == 2
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_extract_directive_fields(self) -> None:
        """extract_reinject returns dicts with rank, tokens, content, line_number."""
        path = _write_temp(REINJECT_MD)
        try:
            result = extract_reinject(path)
            directive = result[0]
            assert "rank" in directive
            assert "tokens" in directive
            assert "content" in directive
            assert "line_number" in directive
            assert directive["rank"] == 1
            assert directive["tokens"] == 50
            assert "No recursive subagents" in directive["content"]
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_extract_no_directives_returns_empty_list(self) -> None:
        """extract_reinject returns empty list when no directives found."""
        path = _write_temp(NO_FRONTMATTER_MD)
        try:
            result = extract_reinject(path)
            assert result == []
        finally:
            os.unlink(path)

    @pytest.mark.edge_case
    def test_extract_empty_file_returns_empty_list(self) -> None:
        """extract_reinject returns empty list for empty files."""
        path = _write_temp(EMPTY_MD)
        try:
            result = extract_reinject(path)
            assert result == []
        finally:
            os.unlink(path)

    @pytest.mark.negative
    def test_extract_file_not_found(self) -> None:
        """extract_reinject raises FileNotFoundError for missing files."""
        with pytest.raises(FileNotFoundError):
            extract_reinject("/nonexistent/path/to/file.md")


# ---------------------------------------------------------------------------
# validate_nav_table_file tests
# ---------------------------------------------------------------------------


class TestValidateNavTableFile:
    """Tests for validate_nav_table_file()."""

    @pytest.mark.happy_path
    def test_validate_nav_returns_dict(self) -> None:
        """validate_nav_table_file returns a dict with expected keys."""
        path = _write_temp(NAV_TABLE_MD)
        try:
            result = validate_nav_table_file(path)
            assert isinstance(result, dict)
            assert "is_valid" in result
            assert "missing_entries" in result
            assert "orphaned_entries" in result
            assert "entries" in result
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_validate_nav_valid_document(self) -> None:
        """validate_nav_table_file correctly validates a compliant document."""
        path = _write_temp(NAV_TABLE_MD)
        try:
            result = validate_nav_table_file(path)
            assert result["is_valid"] is True
            assert result["missing_entries"] == []
            assert result["orphaned_entries"] == []
        finally:
            os.unlink(path)

    @pytest.mark.negative
    def test_validate_nav_no_nav_table(self) -> None:
        """validate_nav_table_file detects missing nav table."""
        path = _write_temp(NO_FRONTMATTER_MD)
        try:
            result = validate_nav_table_file(path)
            assert result["is_valid"] is False
        finally:
            os.unlink(path)

    @pytest.mark.negative
    def test_validate_nav_missing_entries(self) -> None:
        """validate_nav_table_file detects headings not covered in nav table."""
        # Document with headings but no nav table
        path = _write_temp(SIMPLE_FRONTMATTER_MD)
        try:
            result = validate_nav_table_file(path)
            assert result["is_valid"] is False
            # Overview heading exists but no nav table covers it
            assert len(result["missing_entries"]) >= 1
        finally:
            os.unlink(path)

    @pytest.mark.edge_case
    def test_validate_nav_empty_file(self) -> None:
        """validate_nav_table_file handles empty file gracefully."""
        path = _write_temp(EMPTY_MD)
        try:
            result = validate_nav_table_file(path)
            assert isinstance(result, dict)
            assert result["is_valid"] is False
        finally:
            os.unlink(path)

    @pytest.mark.negative
    def test_validate_nav_file_not_found(self) -> None:
        """validate_nav_table_file raises FileNotFoundError for missing files."""
        with pytest.raises(FileNotFoundError):
            validate_nav_table_file("/nonexistent/path/to/file.md")

    @pytest.mark.happy_path
    def test_validate_nav_entries_are_serializable(self) -> None:
        """validate_nav_table_file entries are dicts (JSON-serializable)."""
        path = _write_temp(NAV_TABLE_MD)
        try:
            result = validate_nav_table_file(path)
            for entry in result["entries"]:
                assert isinstance(entry, dict)
                assert "section_name" in entry
                assert "anchor" in entry
                assert "description" in entry
        finally:
            os.unlink(path)
