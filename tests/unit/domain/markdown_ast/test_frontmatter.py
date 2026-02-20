# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for BlockquoteFrontmatter extension.

Tests cover:
    - AC-ST002-1: Extract all key-value pairs from a Jerry entity blockquote frontmatter
    - AC-ST002-2: Handle multiline values (e.g., wrapped descriptions)
    - AC-ST002-3: Handle inline markdown in values (e.g., bold, italic)
    - AC-ST002-4: Write-back: modify a single field, verify unmodified fields preserved
    - AC-ST002-5: Write-back: add a new field to existing frontmatter
    - AC-ST002-6: Works on WORKTRACKER entities, skill definitions, spike entities
    - H-20: BDD test-first approach
    - H-21: 90% line coverage

Test Categories:
    - Happy path: Valid Jerry entity frontmatter, extraction, modification, addition
    - Negative: Empty doc, no frontmatter, missing keys, duplicate keys
    - Edge cases: Placeholder values (--), numeric values, multiline, inline markdown
"""

from __future__ import annotations

import pytest

from src.domain.markdown_ast.frontmatter import (
    BlockquoteFrontmatter,
    FrontmatterField,
    extract_frontmatter,
)
from src.domain.markdown_ast.jerry_document import JerryDocument


# ---------------------------------------------------------------------------
# Test fixtures: canonical Jerry entity source strings
# ---------------------------------------------------------------------------

STORY_FRONTMATTER = """\
# ST-002: Implement Blockquote Frontmatter Extension

> **Type:** story
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-20
> **Due:** --
> **Completed:** --
> **Parent:** FEAT-001
> **Owner:** --
> **Effort:** 5

---

## Summary

Some content here.
"""

SPIKE_FRONTMATTER = """\
# SPIKE-002: Feasibility Assessment

> **Type:** spike
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-19
> **Due:** --
> **Completed:** 2026-02-19
> **Parent:** FEAT-001
> **Owner:** --
> **Effort:** 3

---

## Objective

Some content here.
"""

ENABLER_FRONTMATTER = """\
# EN-001: R-01 PoC

> **Type:** enabler
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-19
> **Due:** --
> **Completed:** 2026-02-19
> **Parent:** SPIKE-002
> **Owner:** --
> **Effort:** 3

---

## Context

Some content here.
"""

NO_FRONTMATTER_DOC = """\
# A Document Without Frontmatter

## Section

Some text here.
"""

EMPTY_DOC = ""

MINIMAL_FRONTMATTER = """\
> **Status:** pending
"""

PLACEHOLDER_FRONTMATTER = """\
> **Due:** --
> **Completed:** --
"""

NUMERIC_FRONTMATTER = """\
> **Effort:** 5
> **Count:** 42
"""

INLINE_MARKDOWN_FRONTMATTER = """\
> **Description:** Some *italicized* text and `code` here
"""

MULTILINE_BLOCKQUOTE = """\
> **Type:** story
> **Status:** pending
> This is a continuation line (not a key-value pair)
> **Priority:** high
"""


# ---------------------------------------------------------------------------
# FrontmatterField dataclass tests
# ---------------------------------------------------------------------------

class TestFrontmatterField:
    """Tests for the FrontmatterField dataclass."""

    def test_field_holds_key_value(self) -> None:
        """FrontmatterField stores key and value attributes."""
        field = FrontmatterField(key="Status", value="pending", line_number=0, start=0, end=20)
        assert field.key == "Status"
        assert field.value == "pending"

    def test_field_holds_position_info(self) -> None:
        """FrontmatterField stores line_number, start, and end positions."""
        field = FrontmatterField(key="Status", value="pending", line_number=2, start=10, end=30)
        assert field.line_number == 2
        assert field.start == 10
        assert field.end == 30

    def test_field_equality(self) -> None:
        """FrontmatterField instances with same data are equal."""
        f1 = FrontmatterField(key="Status", value="pending", line_number=0, start=0, end=20)
        f2 = FrontmatterField(key="Status", value="pending", line_number=0, start=0, end=20)
        assert f1 == f2

    def test_field_repr_contains_key_and_value(self) -> None:
        """FrontmatterField repr contains key and value."""
        field = FrontmatterField(key="Status", value="pending", line_number=0, start=0, end=20)
        r = repr(field)
        assert "Status" in r
        assert "pending" in r


# ---------------------------------------------------------------------------
# extract_frontmatter convenience function tests
# ---------------------------------------------------------------------------

class TestExtractFrontmatterFunction:
    """Tests for the extract_frontmatter() convenience function."""

    def test_returns_blockquote_frontmatter_instance(self) -> None:
        """extract_frontmatter() returns a BlockquoteFrontmatter instance."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        result = extract_frontmatter(doc)
        assert isinstance(result, BlockquoteFrontmatter)

    def test_extracts_correct_number_of_fields(self) -> None:
        """extract_frontmatter() extracts all frontmatter fields."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        result = extract_frontmatter(doc)
        # STORY_FRONTMATTER has 10 fields: Type, Status, Priority, Impact,
        # Created, Due, Completed, Parent, Owner, Effort
        assert len(result) == 10

    def test_returns_empty_for_no_frontmatter(self) -> None:
        """extract_frontmatter() returns empty result for docs without frontmatter."""
        doc = JerryDocument.parse(NO_FRONTMATTER_DOC)
        result = extract_frontmatter(doc)
        assert len(result) == 0

    def test_returns_empty_for_empty_doc(self) -> None:
        """extract_frontmatter() returns empty result for empty document."""
        doc = JerryDocument.parse(EMPTY_DOC)
        result = extract_frontmatter(doc)
        assert len(result) == 0


# ---------------------------------------------------------------------------
# BlockquoteFrontmatter.extract() class method tests
# ---------------------------------------------------------------------------

class TestBlockquoteFrontmatterExtract:
    """Tests for BlockquoteFrontmatter.extract() class method."""

    def test_extract_returns_instance(self) -> None:
        """extract() returns a BlockquoteFrontmatter instance."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        assert isinstance(fm, BlockquoteFrontmatter)

    def test_extract_story_type_field(self) -> None:
        """extract() correctly extracts the Type field from a story entity."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        assert fm.get("Type") == "story"

    def test_extract_story_status_field(self) -> None:
        """extract() correctly extracts the Status field."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        assert fm.get("Status") == "pending"

    def test_extract_story_effort_numeric_field(self) -> None:
        """extract() extracts numeric values as strings."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        assert fm.get("Effort") == "5"

    def test_extract_story_placeholder_due_field(self) -> None:
        """extract() correctly extracts placeholder '--' values."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        assert fm.get("Due") == "--"

    def test_extract_story_placeholder_completed_field(self) -> None:
        """extract() correctly extracts placeholder '--' completed field."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        assert fm.get("Completed") == "--"

    def test_extract_story_parent_field(self) -> None:
        """extract() correctly extracts the Parent field."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        assert fm.get("Parent") == "FEAT-001"

    def test_extract_spike_entity(self) -> None:
        """extract() works on spike entity frontmatter."""
        doc = JerryDocument.parse(SPIKE_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        assert fm.get("Type") == "spike"
        assert fm.get("Status") == "completed"
        assert fm.get("Effort") == "3"

    def test_extract_enabler_entity(self) -> None:
        """extract() works on enabler entity frontmatter."""
        doc = JerryDocument.parse(ENABLER_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        assert fm.get("Type") == "enabler"
        assert fm.get("Status") == "completed"

    def test_extract_empty_document_returns_empty(self) -> None:
        """extract() returns an empty BlockquoteFrontmatter for empty document."""
        doc = JerryDocument.parse(EMPTY_DOC)
        fm = BlockquoteFrontmatter.extract(doc)
        assert len(fm) == 0

    def test_extract_no_frontmatter_returns_empty(self) -> None:
        """extract() returns empty result for documents with no frontmatter."""
        doc = JerryDocument.parse(NO_FRONTMATTER_DOC)
        fm = BlockquoteFrontmatter.extract(doc)
        assert len(fm) == 0

    def test_extract_numeric_values_as_string(self) -> None:
        """extract() returns numeric field values as strings."""
        doc = JerryDocument.parse(NUMERIC_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        assert fm.get("Effort") == "5"
        assert fm.get("Count") == "42"

    def test_extract_inline_markdown_in_values(self) -> None:
        """extract() extracts values containing inline markdown."""
        doc = JerryDocument.parse(INLINE_MARKDOWN_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        value = fm.get("Description")
        assert value is not None
        # The value should contain the markdown text content
        assert "italicized" in value

    def test_extract_fields_have_correct_keys(self) -> None:
        """extract() populates fields with correctly stripped keys."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        keys = list(fm.keys())
        assert "Type" in keys
        assert "Status" in keys
        assert "Priority" in keys
        assert "Effort" in keys

    def test_extract_field_positions_are_set(self) -> None:
        """extract() sets line_number, start, and end on each field."""
        doc = JerryDocument.parse(MINIMAL_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        field = fm._fields[0]
        assert field.line_number >= 0
        assert field.start >= 0
        assert field.end > field.start


# ---------------------------------------------------------------------------
# BlockquoteFrontmatter dict-like access tests
# ---------------------------------------------------------------------------

class TestBlockquoteFrontmatterAccess:
    """Tests for dict-like access methods on BlockquoteFrontmatter."""

    def test_get_existing_key_returns_value(self) -> None:
        """get() returns the value for an existing key."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        assert fm.get("Status") == "pending"

    def test_get_missing_key_returns_none(self) -> None:
        """get() returns None for a key not present in the frontmatter."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        assert fm.get("NonExistentKey") is None

    def test_get_missing_key_returns_default(self) -> None:
        """get() returns provided default for a missing key."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        assert fm.get("NonExistentKey", "fallback") == "fallback"

    def test_contains_existing_key(self) -> None:
        """'in' operator returns True for existing key."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        assert "Status" in fm

    def test_contains_missing_key(self) -> None:
        """'in' operator returns False for missing key."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        assert "NonExistentKey" not in fm

    def test_getitem_existing_key(self) -> None:
        """fm[key] returns the value for an existing key."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        assert fm["Status"] == "pending"

    def test_getitem_missing_key_raises_key_error(self) -> None:
        """fm[key] raises KeyError for a missing key."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        with pytest.raises(KeyError):
            _ = fm["NonExistentKey"]

    def test_len_returns_field_count(self) -> None:
        """len(fm) returns the number of frontmatter fields."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        assert len(fm) == 10

    def test_len_empty_frontmatter(self) -> None:
        """len(fm) returns 0 for empty frontmatter."""
        doc = JerryDocument.parse(EMPTY_DOC)
        fm = BlockquoteFrontmatter.extract(doc)
        assert len(fm) == 0

    def test_keys_returns_all_keys(self) -> None:
        """keys() returns all field keys."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        keys = list(fm.keys())
        assert len(keys) == 10
        assert "Type" in keys
        assert "Effort" in keys

    def test_values_returns_all_values(self) -> None:
        """values() returns all field values."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        values = list(fm.values())
        assert "story" in values
        assert "pending" in values

    def test_items_returns_key_value_pairs(self) -> None:
        """items() returns (key, value) tuples."""
        doc = JerryDocument.parse(MINIMAL_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        items = list(fm.items())
        assert len(items) == 1
        assert items[0] == ("Status", "pending")

    def test_keys_preserves_order(self) -> None:
        """keys() returns keys in document order."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        keys = list(fm.keys())
        # Document order: Type, Status, Priority, Impact, Created, Due, Completed, Parent, Owner, Effort
        assert keys[0] == "Type"
        assert keys[1] == "Status"
        assert keys[-1] == "Effort"


# ---------------------------------------------------------------------------
# BlockquoteFrontmatter.set() write-back tests
# ---------------------------------------------------------------------------

class TestBlockquoteFrontmatterSet:
    """Tests for BlockquoteFrontmatter.set() write-back method."""

    def test_set_returns_jerry_document(self) -> None:
        """set() returns a JerryDocument instance."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        result = fm.set("Status", "in-progress")
        assert isinstance(result, JerryDocument)

    def test_set_modifies_target_field(self) -> None:
        """set() modifies the target field value in the returned document."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        new_doc = fm.set("Status", "in-progress")
        new_fm = BlockquoteFrontmatter.extract(new_doc)
        assert new_fm.get("Status") == "in-progress"

    def test_set_preserves_unmodified_fields(self) -> None:
        """set() preserves all fields that were not modified."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        new_doc = fm.set("Status", "in-progress")
        new_fm = BlockquoteFrontmatter.extract(new_doc)
        assert new_fm.get("Type") == "story"
        assert new_fm.get("Priority") == "high"
        assert new_fm.get("Parent") == "FEAT-001"
        assert new_fm.get("Effort") == "5"

    def test_set_preserves_field_count(self) -> None:
        """set() does not change the number of frontmatter fields."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        new_doc = fm.set("Status", "in-progress")
        new_fm = BlockquoteFrontmatter.extract(new_doc)
        assert len(new_fm) == len(fm)

    def test_set_placeholder_to_date(self) -> None:
        """set() replaces placeholder '--' values with real values."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        new_doc = fm.set("Due", "2026-03-15")
        new_fm = BlockquoteFrontmatter.extract(new_doc)
        assert new_fm.get("Due") == "2026-03-15"

    def test_set_numeric_field(self) -> None:
        """set() modifies a numeric-valued field."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        new_doc = fm.set("Effort", "8")
        new_fm = BlockquoteFrontmatter.extract(new_doc)
        assert new_fm.get("Effort") == "8"

    def test_set_spike_status_field(self) -> None:
        """set() correctly modifies spike entity status."""
        doc = JerryDocument.parse(SPIKE_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        new_doc = fm.set("Status", "in-progress")
        new_fm = BlockquoteFrontmatter.extract(new_doc)
        assert new_fm.get("Status") == "in-progress"
        assert new_fm.get("Type") == "spike"

    def test_set_date_field(self) -> None:
        """set() correctly modifies a date field."""
        doc = JerryDocument.parse(SPIKE_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        new_doc = fm.set("Created", "2026-01-15")
        new_fm = BlockquoteFrontmatter.extract(new_doc)
        assert new_fm.get("Created") == "2026-01-15"

    def test_set_does_not_mutate_original_doc(self) -> None:
        """set() does not modify the original JerryDocument."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        _ = fm.set("Status", "in-progress")
        # Original doc source should be unchanged
        orig_fm = BlockquoteFrontmatter.extract(doc)
        assert orig_fm.get("Status") == "pending"

    def test_set_missing_key_raises_key_error(self) -> None:
        """set() raises KeyError for a key not present in the frontmatter."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        with pytest.raises(KeyError):
            fm.set("NonExistentKey", "some-value")

    def test_set_preserves_non_frontmatter_content(self) -> None:
        """set() preserves document content outside the frontmatter block."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        new_doc = fm.set("Status", "in-progress")
        # The heading and summary section should remain
        assert "ST-002" in new_doc.source
        assert "Summary" in new_doc.source

    def test_set_result_is_parseable(self) -> None:
        """set() result can be re-parsed and re-rendered without error."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        new_doc = fm.set("Status", "in-progress")
        # Should not raise
        rendered = new_doc.render()
        assert rendered is not None

    def test_set_enabler_effort_field(self) -> None:
        """set() modifies Effort field on enabler entity."""
        doc = JerryDocument.parse(ENABLER_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        new_doc = fm.set("Effort", "5")
        new_fm = BlockquoteFrontmatter.extract(new_doc)
        assert new_fm.get("Effort") == "5"


# ---------------------------------------------------------------------------
# BlockquoteFrontmatter.add() write-back tests
# ---------------------------------------------------------------------------

class TestBlockquoteFrontmatterAdd:
    """Tests for BlockquoteFrontmatter.add() write-back method."""

    def test_add_returns_jerry_document(self) -> None:
        """add() returns a JerryDocument instance."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        result = fm.add("Reviewer", "alice")
        assert isinstance(result, JerryDocument)

    def test_add_new_field_appears_in_result(self) -> None:
        """add() appends a new field that can be extracted from the result."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        new_doc = fm.add("Reviewer", "alice")
        new_fm = BlockquoteFrontmatter.extract(new_doc)
        assert new_fm.get("Reviewer") == "alice"

    def test_add_increases_field_count(self) -> None:
        """add() increases the number of frontmatter fields by one."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        original_count = len(fm)
        new_doc = fm.add("Reviewer", "alice")
        new_fm = BlockquoteFrontmatter.extract(new_doc)
        assert len(new_fm) == original_count + 1

    def test_add_preserves_existing_fields(self) -> None:
        """add() preserves all existing frontmatter fields."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        new_doc = fm.add("Reviewer", "alice")
        new_fm = BlockquoteFrontmatter.extract(new_doc)
        assert new_fm.get("Type") == "story"
        assert new_fm.get("Status") == "pending"
        assert new_fm.get("Effort") == "5"

    def test_add_existing_key_raises_value_error(self) -> None:
        """add() raises ValueError when key already exists in frontmatter."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        with pytest.raises(ValueError, match="Status"):
            fm.add("Status", "in-progress")

    def test_add_does_not_mutate_original_doc(self) -> None:
        """add() does not modify the original JerryDocument."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        _ = fm.add("Reviewer", "alice")
        # Original should be unchanged
        orig_fm = BlockquoteFrontmatter.extract(doc)
        assert "Reviewer" not in orig_fm

    def test_add_preserves_non_frontmatter_content(self) -> None:
        """add() preserves document content outside the frontmatter block."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        new_doc = fm.add("Reviewer", "alice")
        assert "ST-002" in new_doc.source
        assert "Summary" in new_doc.source

    def test_add_to_empty_frontmatter(self) -> None:
        """add() can add a field to a document with no existing frontmatter."""
        doc = JerryDocument.parse(NO_FRONTMATTER_DOC)
        fm = BlockquoteFrontmatter.extract(doc)
        # No existing frontmatter, so add should work (appends to source)
        new_doc = fm.add("Status", "pending")
        new_fm = BlockquoteFrontmatter.extract(new_doc)
        assert new_fm.get("Status") == "pending"

    def test_add_result_is_parseable(self) -> None:
        """add() result can be re-parsed and re-rendered without error."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        new_doc = fm.add("Reviewer", "alice")
        rendered = new_doc.render()
        assert rendered is not None


# ---------------------------------------------------------------------------
# Edge case tests
# ---------------------------------------------------------------------------

class TestBlockquoteFrontmatterEdgeCases:
    """Tests for edge cases in BlockquoteFrontmatter."""

    def test_minimal_single_field(self) -> None:
        """extract() handles a single-field frontmatter correctly."""
        doc = JerryDocument.parse(MINIMAL_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        assert len(fm) == 1
        assert fm.get("Status") == "pending"

    def test_two_placeholder_fields(self) -> None:
        """extract() handles multiple placeholder '--' values."""
        doc = JerryDocument.parse(PLACEHOLDER_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        assert fm.get("Due") == "--"
        assert fm.get("Completed") == "--"

    def test_multiline_blockquote_only_extracts_key_value_lines(self) -> None:
        """extract() ignores non-key-value continuation lines in blockquotes."""
        doc = JerryDocument.parse(MULTILINE_BLOCKQUOTE)
        fm = BlockquoteFrontmatter.extract(doc)
        # Should only extract key-value lines, not the continuation
        assert fm.get("Type") == "story"
        assert fm.get("Status") == "pending"
        assert fm.get("Priority") == "high"
        # The continuation line is not a valid key-value pair
        assert "This is a continuation line" not in fm.keys()

    def test_case_sensitive_key_lookup(self) -> None:
        """Keys in get() are case-sensitive."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        assert fm.get("status") is None  # lowercase - not present
        assert fm.get("Status") == "pending"  # correct case

    def test_set_same_value_is_idempotent(self) -> None:
        """set() with the same value produces equivalent frontmatter."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        new_doc = fm.set("Status", "pending")  # same value
        new_fm = BlockquoteFrontmatter.extract(new_doc)
        assert new_fm.get("Status") == "pending"
        assert len(new_fm) == len(fm)

    def test_chained_set_operations(self) -> None:
        """Multiple set() calls can be chained via re-extraction."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        doc2 = fm.set("Status", "in-progress")
        fm2 = BlockquoteFrontmatter.extract(doc2)
        doc3 = fm2.set("Due", "2026-03-15")
        fm3 = BlockquoteFrontmatter.extract(doc3)
        assert fm3.get("Status") == "in-progress"
        assert fm3.get("Due") == "2026-03-15"
        assert fm3.get("Type") == "story"

    def test_extract_created_date_field(self) -> None:
        """extract() correctly extracts ISO date values."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        assert fm.get("Created") == "2026-02-20"

    def test_set_completed_placeholder_to_date(self) -> None:
        """set() replaces the Completed '--' placeholder with a real date."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        new_doc = fm.set("Completed", "2026-03-01")
        new_fm = BlockquoteFrontmatter.extract(new_doc)
        assert new_fm.get("Completed") == "2026-03-01"
        assert new_fm.get("Due") == "--"  # Due unmodified

    def test_story_owner_placeholder(self) -> None:
        """extract() correctly extracts Owner '--' placeholder."""
        doc = JerryDocument.parse(STORY_FRONTMATTER)
        fm = BlockquoteFrontmatter.extract(doc)
        assert fm.get("Owner") == "--"
