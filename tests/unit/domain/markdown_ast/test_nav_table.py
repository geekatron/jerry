# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for navigation table helpers.

Tests cover:
    - AC-ST008-1: Find navigation table in a Jerry document (first table after frontmatter)
    - AC-ST008-2: Extract section names and anchor links from navigation table
    - AC-ST008-3: Validate every ## heading has a navigation entry
    - AC-ST008-4: Validate every navigation link resolves to a valid heading anchor
    - AC-ST008-5: Report missing/orphaned entries with line numbers
    - H-20: BDD test-first approach
    - H-21: 90% line coverage

Test Categories:
    - Happy path: Valid nav table, all headings covered, all links valid
    - Negative: Missing nav table, missing entries, orphaned entries, invalid anchors
    - Edge cases: Empty document, nav table only, no ## headings, special chars in headings
"""

from __future__ import annotations

import pytest

from src.domain.markdown_ast.jerry_document import JerryDocument
from src.domain.markdown_ast.nav_table import (
    NavEntry,
    NavValidationResult,
    extract_nav_table,
    heading_to_anchor,
    validate_nav_table,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

VALID_JERRY_DOC = """\
# My Document

> **Type:** rule
> **Status:** active

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this covers |
| [Problem Statement](#problem-statement) | Why this matters |
| [Technical Approach](#technical-approach) | How to implement |

---

## Summary

Some summary content here.

---

## Problem Statement

Why this matters content.

---

## Technical Approach

How to implement content.
"""

VALID_JERRY_DOC_WITH_ANCHORS_ONLY = """\
# Title

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overview |
| [Details](#details) | More info |

---

## Summary

Content.

---

## Details

More content.
"""

MISSING_NAV_TABLE_DOC = """\
# My Document

## Summary

Some content here.

## Details

More content.

## Conclusion

Final content.
"""

ORPHANED_ENTRY_DOC = """\
# My Document

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this covers |
| [Nonexistent Section](#nonexistent-section) | This heading does not exist |

---

## Summary

Some content.
"""

MISSING_HEADING_DOC = """\
# My Document

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this covers |

---

## Summary

Some content.

---

## Unlisted Section

This section is not in the nav table.
"""

SHORT_DOC = """\
# Short

Just a few lines.
"""


# ---------------------------------------------------------------------------
# Tests for heading_to_anchor()
# ---------------------------------------------------------------------------


class TestHeadingToAnchor:
    """Tests for the heading_to_anchor() conversion function."""

    def test_lowercase_single_word(self) -> None:
        """Single word is lowercased."""
        assert heading_to_anchor("Summary") == "summary"

    def test_spaces_become_hyphens(self) -> None:
        """Spaces are replaced with hyphens."""
        assert heading_to_anchor("Problem Statement") == "problem-statement"

    def test_already_lowercase(self) -> None:
        """Already lowercase input is unchanged in case."""
        assert heading_to_anchor("details") == "details"

    def test_mixed_case_with_spaces(self) -> None:
        """Mixed case with spaces is lowercased and hyphenated."""
        assert heading_to_anchor("Technical Approach") == "technical-approach"

    def test_special_chars_removed_parentheses(self) -> None:
        """Parentheses are removed from anchor."""
        assert heading_to_anchor("Children (Tasks)") == "children-tasks"

    def test_special_chars_removed_colon(self) -> None:
        """Colons are removed from anchor."""
        assert heading_to_anchor("Section: Overview") == "section-overview"

    def test_multiple_spaces_collapse(self) -> None:
        """Multiple consecutive spaces collapse to single hyphen."""
        assert heading_to_anchor("A  B") == "a-b"

    def test_leading_trailing_whitespace(self) -> None:
        """Leading and trailing whitespace is stripped."""
        assert heading_to_anchor("  Summary  ") == "summary"

    def test_empty_string(self) -> None:
        """Empty string returns empty string."""
        assert heading_to_anchor("") == ""

    def test_hard_rule_index_example(self) -> None:
        """HARD Rule Index heading from quality-enforcement.md."""
        assert heading_to_anchor("HARD Rule Index") == "hard-rule-index"

    def test_standards_medium_example(self) -> None:
        """Standards (MEDIUM) from markdown-navigation-standards.md."""
        assert heading_to_anchor("Standards (MEDIUM)") == "standards-medium"

    def test_numbers_preserved(self) -> None:
        """Numbers are preserved in anchors."""
        assert heading_to_anchor("Section 2") == "section-2"

    def test_hyphens_preserved(self) -> None:
        """Existing hyphens are preserved."""
        assert heading_to_anchor("Auto-Escalation Rules") == "auto-escalation-rules"


# ---------------------------------------------------------------------------
# Tests for extract_nav_table()
# ---------------------------------------------------------------------------


class TestExtractNavTable:
    """Tests for extract_nav_table() function."""

    def test_returns_list_for_valid_document(self) -> None:
        """extract_nav_table() returns a list for a document with nav table."""
        doc = JerryDocument.parse(VALID_JERRY_DOC)
        result = extract_nav_table(doc)
        assert result is not None
        assert isinstance(result, list)

    def test_returns_none_when_no_nav_table(self) -> None:
        """extract_nav_table() returns None when no nav table is present."""
        doc = JerryDocument.parse(MISSING_NAV_TABLE_DOC)
        result = extract_nav_table(doc)
        assert result is None

    def test_returns_none_for_empty_document(self) -> None:
        """extract_nav_table() returns None for an empty document."""
        doc = JerryDocument.parse("")
        result = extract_nav_table(doc)
        assert result is None

    def test_entries_are_nav_entry_instances(self) -> None:
        """extract_nav_table() returns a list of NavEntry instances."""
        doc = JerryDocument.parse(VALID_JERRY_DOC)
        result = extract_nav_table(doc)
        assert result is not None
        for entry in result:
            assert isinstance(entry, NavEntry)

    def test_correct_number_of_entries(self) -> None:
        """extract_nav_table() extracts the correct number of nav entries."""
        doc = JerryDocument.parse(VALID_JERRY_DOC)
        result = extract_nav_table(doc)
        assert result is not None
        assert len(result) == 3

    def test_entry_section_names(self) -> None:
        """extract_nav_table() correctly extracts section names."""
        doc = JerryDocument.parse(VALID_JERRY_DOC)
        result = extract_nav_table(doc)
        assert result is not None
        names = [e.section_name for e in result]
        assert "Summary" in names
        assert "Problem Statement" in names
        assert "Technical Approach" in names

    def test_entry_anchors(self) -> None:
        """extract_nav_table() correctly extracts anchor links."""
        doc = JerryDocument.parse(VALID_JERRY_DOC)
        result = extract_nav_table(doc)
        assert result is not None
        anchors = [e.anchor for e in result]
        assert "summary" in anchors
        assert "problem-statement" in anchors
        assert "technical-approach" in anchors

    def test_entry_descriptions(self) -> None:
        """extract_nav_table() correctly extracts descriptions."""
        doc = JerryDocument.parse(VALID_JERRY_DOC)
        result = extract_nav_table(doc)
        assert result is not None
        descs = [e.description for e in result]
        assert any("What this covers" in d for d in descs)
        assert any("Why this matters" in d for d in descs)
        assert any("How to implement" in d for d in descs)

    def test_entry_line_numbers_are_non_negative(self) -> None:
        """extract_nav_table() assigns non-negative (0-based) line numbers."""
        doc = JerryDocument.parse(VALID_JERRY_DOC)
        result = extract_nav_table(doc)
        assert result is not None
        for entry in result:
            assert entry.line_number >= 0

    def test_entry_line_numbers_are_ordered(self) -> None:
        """extract_nav_table() assigns increasing line numbers in order."""
        doc = JerryDocument.parse(VALID_JERRY_DOC)
        result = extract_nav_table(doc)
        assert result is not None
        line_nums = [e.line_number for e in result]
        assert line_nums == sorted(line_nums)

    def test_two_entry_nav_table(self) -> None:
        """extract_nav_table() works with a two-entry nav table."""
        doc = JerryDocument.parse(VALID_JERRY_DOC_WITH_ANCHORS_ONLY)
        result = extract_nav_table(doc)
        assert result is not None
        assert len(result) == 2

    def test_no_nav_table_returns_none_for_short_doc(self) -> None:
        """extract_nav_table() returns None for a short doc with no table."""
        doc = JerryDocument.parse(SHORT_DOC)
        result = extract_nav_table(doc)
        assert result is None

    def test_non_nav_table_does_not_confuse_extractor(self) -> None:
        """A table without anchor links is not treated as a nav table."""
        source = """\
# My Doc

## Section

| ID | Rule | Source |
|----|------|--------|
| H-01 | No recursive | P-003 |
| H-02 | User authority | P-020 |
"""
        doc = JerryDocument.parse(source)
        result = extract_nav_table(doc)
        assert result is None


# ---------------------------------------------------------------------------
# Tests for NavEntry dataclass
# ---------------------------------------------------------------------------


class TestNavEntry:
    """Tests for the NavEntry dataclass."""

    def test_nav_entry_creation(self) -> None:
        """NavEntry can be created with required fields."""
        entry = NavEntry(
            section_name="Summary",
            anchor="summary",
            description="What this covers",
            line_number=10,
        )
        assert entry.section_name == "Summary"
        assert entry.anchor == "summary"
        assert entry.description == "What this covers"
        assert entry.line_number == 10

    def test_nav_entry_is_frozen(self) -> None:
        """NavEntry is immutable (frozen dataclass)."""
        entry = NavEntry(
            section_name="Summary",
            anchor="summary",
            description="Description",
            line_number=5,
        )
        with pytest.raises((AttributeError, TypeError)):
            entry.section_name = "Changed"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Tests for validate_nav_table()
# ---------------------------------------------------------------------------


class TestValidateNavTable:
    """Tests for validate_nav_table() function."""

    def test_returns_nav_validation_result(self) -> None:
        """validate_nav_table() returns a NavValidationResult instance."""
        doc = JerryDocument.parse(VALID_JERRY_DOC)
        result = validate_nav_table(doc)
        assert isinstance(result, NavValidationResult)

    def test_valid_document_passes(self) -> None:
        """validate_nav_table() marks a fully valid document as valid."""
        doc = JerryDocument.parse(VALID_JERRY_DOC)
        result = validate_nav_table(doc)
        assert result.is_valid is True

    def test_valid_document_no_missing_entries(self) -> None:
        """validate_nav_table() reports no missing entries for a valid document."""
        doc = JerryDocument.parse(VALID_JERRY_DOC)
        result = validate_nav_table(doc)
        assert result.missing_entries == []

    def test_valid_document_no_orphaned_entries(self) -> None:
        """validate_nav_table() reports no orphaned entries for a valid document."""
        doc = JerryDocument.parse(VALID_JERRY_DOC)
        result = validate_nav_table(doc)
        assert result.orphaned_entries == []

    def test_valid_document_entries_populated(self) -> None:
        """validate_nav_table() populates entries list for a valid document."""
        doc = JerryDocument.parse(VALID_JERRY_DOC)
        result = validate_nav_table(doc)
        assert len(result.entries) == 3

    def test_missing_nav_table_is_invalid(self) -> None:
        """validate_nav_table() reports invalid when no nav table exists."""
        doc = JerryDocument.parse(MISSING_NAV_TABLE_DOC)
        result = validate_nav_table(doc)
        assert result.is_valid is False

    def test_missing_nav_table_has_missing_entries(self) -> None:
        """validate_nav_table() reports all ## headings as missing when no nav table."""
        doc = JerryDocument.parse(MISSING_NAV_TABLE_DOC)
        result = validate_nav_table(doc)
        # MISSING_NAV_TABLE_DOC has 3 ## headings: Summary, Details, Conclusion
        assert len(result.missing_entries) == 3

    def test_missing_nav_table_empty_entries(self) -> None:
        """validate_nav_table() returns empty entries list when no nav table."""
        doc = JerryDocument.parse(MISSING_NAV_TABLE_DOC)
        result = validate_nav_table(doc)
        assert result.entries == []

    def test_orphaned_entry_detected(self) -> None:
        """validate_nav_table() detects nav entries with no matching heading."""
        doc = JerryDocument.parse(ORPHANED_ENTRY_DOC)
        result = validate_nav_table(doc)
        assert result.is_valid is False
        orphaned_names = [e.section_name for e in result.orphaned_entries]
        assert "Nonexistent Section" in orphaned_names

    def test_missing_heading_detected(self) -> None:
        """validate_nav_table() detects ## headings missing from nav table."""
        doc = JerryDocument.parse(MISSING_HEADING_DOC)
        result = validate_nav_table(doc)
        assert result.is_valid is False
        assert "Unlisted Section" in result.missing_entries

    def test_missing_heading_listed_section_not_flagged(self) -> None:
        """validate_nav_table() does not flag headings that are in the nav table."""
        doc = JerryDocument.parse(MISSING_HEADING_DOC)
        result = validate_nav_table(doc)
        assert "Summary" not in result.missing_entries

    def test_empty_document_is_invalid(self) -> None:
        """validate_nav_table() marks an empty document as invalid."""
        doc = JerryDocument.parse("")
        result = validate_nav_table(doc)
        assert result.is_valid is False

    def test_empty_document_empty_entries(self) -> None:
        """validate_nav_table() returns empty entries for empty document."""
        doc = JerryDocument.parse("")
        result = validate_nav_table(doc)
        assert result.entries == []

    def test_document_sections_heading_excluded_from_missing(self) -> None:
        """validate_nav_table() excludes the 'Document Sections' heading itself."""
        doc = JerryDocument.parse(VALID_JERRY_DOC)
        result = validate_nav_table(doc)
        # 'Document Sections' is the nav table heading and should not be
        # reported as missing from the nav table
        assert "Document Sections" not in result.missing_entries

    def test_valid_simple_document_passes(self) -> None:
        """validate_nav_table() correctly validates a simple two-section document."""
        doc = JerryDocument.parse(VALID_JERRY_DOC_WITH_ANCHORS_ONLY)
        result = validate_nav_table(doc)
        assert result.is_valid is True
        assert result.missing_entries == []
        assert result.orphaned_entries == []

    def test_nav_validation_result_has_entries(self) -> None:
        """NavValidationResult entries attribute contains NavEntry objects."""
        doc = JerryDocument.parse(VALID_JERRY_DOC)
        result = validate_nav_table(doc)
        for entry in result.entries:
            assert isinstance(entry, NavEntry)

    def test_orphaned_entry_result_entries_populated(self) -> None:
        """validate_nav_table() still populates entries even when there are orphans."""
        doc = JerryDocument.parse(ORPHANED_ENTRY_DOC)
        result = validate_nav_table(doc)
        # entries should be populated even when invalid
        assert len(result.entries) > 0

    def test_nav_table_heading_nav_anchor_validation(self) -> None:
        """validate_nav_table() detects nav entries with wrong anchors."""
        source = """\
# My Document

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#wrong-anchor) | What this covers |

---

## Summary

Content here.
"""
        doc = JerryDocument.parse(source)
        result = validate_nav_table(doc)
        # The anchor #wrong-anchor does not match heading_to_anchor("Summary") = "summary"
        assert result.is_valid is False
        orphaned_names = [e.section_name for e in result.orphaned_entries]
        assert "Summary" in orphaned_names

    def test_mixed_errors_detected(self) -> None:
        """validate_nav_table() detects both missing and orphaned in same document."""
        source = """\
# My Document

## Document Sections

| Section | Purpose |
|---------|---------|
| [Ghost Entry](#ghost-entry) | Not a real heading |

---

## Real Section

Content here.

## Another Real Section

More content.
"""
        doc = JerryDocument.parse(source)
        result = validate_nav_table(doc)
        assert result.is_valid is False
        assert len(result.missing_entries) >= 1
        assert len(result.orphaned_entries) >= 1
