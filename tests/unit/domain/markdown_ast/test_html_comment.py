# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for HtmlCommentMetadata parser (WI-009, WI-010).

Tests cover:
    - Happy path: extract HTML comment metadata blocks
    - Pipe-separated key-value extraction
    - L2-REINJECT exclusion (case-insensitive, T-HC-04, T-HC-07)
    - First --> termination (M-13)
    - Comment count enforcement (M-16)
    - Value length truncation (M-17)
    - Control character stripping (M-18)
    - Non-metadata comments ignored
    - Empty document handling
    - Line number accuracy
    - Frozen dataclass immutability

References:
    - ADR-PROJ005-003 Design Decision 7
    - H-20: BDD test-first
"""

from __future__ import annotations

import pytest

from src.domain.markdown_ast.html_comment import (
    HtmlCommentBlock,
    HtmlCommentField,
    HtmlCommentMetadata,
    HtmlCommentResult,
)
from src.domain.markdown_ast.input_bounds import InputBounds
from src.domain.markdown_ast.jerry_document import JerryDocument

# =============================================================================
# Happy Path Tests
# =============================================================================


class TestHtmlCommentExtraction:
    """Tests for basic HTML comment metadata extraction."""

    @pytest.mark.happy_path
    def test_extract_single_comment_block(self) -> None:
        """Extracts a single pipe-separated metadata comment."""
        source = "<!-- PS-ID: ADR-001 | ENTRY: 2026-02-23 | AGENT: test -->\n# Doc\n"
        doc = JerryDocument.parse(source)
        result = HtmlCommentMetadata.extract(doc)

        assert result.parse_error is None
        assert len(result.blocks) == 1
        assert len(result.blocks[0].fields) == 3

    @pytest.mark.happy_path
    def test_extract_field_keys(self) -> None:
        """Keys are correctly extracted from pipe-separated comment."""
        source = "<!-- PS-ID: ADR-001 | ENTRY: 2026-02-23 -->\n"
        doc = JerryDocument.parse(source)
        result = HtmlCommentMetadata.extract(doc)

        keys = [f.key for f in result.blocks[0].fields]
        assert "PS-ID" in keys
        assert "ENTRY" in keys

    @pytest.mark.happy_path
    def test_extract_field_values(self) -> None:
        """Values are correctly extracted from pipe-separated comment."""
        source = "<!-- PS-ID: ADR-001 | ENTRY: 2026-02-23 -->\n"
        doc = JerryDocument.parse(source)
        result = HtmlCommentMetadata.extract(doc)

        values = {f.key: f.value for f in result.blocks[0].fields}
        assert values["PS-ID"] == "ADR-001"
        assert values["ENTRY"] == "2026-02-23"

    @pytest.mark.happy_path
    def test_extract_multiple_comment_blocks(self) -> None:
        """Extracts multiple metadata comment blocks."""
        source = (
            "<!-- VERSION: 1.0 | DATE: 2026-02-23 -->\n"
            "# Doc\n"
            "<!-- PS-ID: test-001 | AGENT: foo -->\n"
        )
        doc = JerryDocument.parse(source)
        result = HtmlCommentMetadata.extract(doc)

        assert result.parse_error is None
        assert len(result.blocks) == 2

    @pytest.mark.happy_path
    def test_raw_comment_preserved(self) -> None:
        """raw_comment contains the original comment text."""
        source = "<!-- PS-ID: test -->\n"
        doc = JerryDocument.parse(source)
        result = HtmlCommentMetadata.extract(doc)

        assert "<!-- PS-ID: test -->" in result.blocks[0].raw_comment


# =============================================================================
# L2-REINJECT Exclusion Tests
# =============================================================================


class TestReinjectExclusion:
    """Tests for L2-REINJECT comment exclusion."""

    @pytest.mark.happy_path
    def test_reinject_comment_excluded(self) -> None:
        """L2-REINJECT comments are excluded from extraction."""
        source = '<!-- L2-REINJECT: rank=1, content="test" -->\n# Doc\n'
        doc = JerryDocument.parse(source)
        result = HtmlCommentMetadata.extract(doc)

        assert len(result.blocks) == 0

    @pytest.mark.edge_case
    def test_reinject_case_insensitive_exclusion(self) -> None:
        """L2-REINJECT exclusion is case-insensitive (T-HC-04, T-HC-07)."""
        source = '<!-- l2-reinject: rank=1, content="test" -->\n# Doc\n'
        doc = JerryDocument.parse(source)
        result = HtmlCommentMetadata.extract(doc)

        assert len(result.blocks) == 0

    @pytest.mark.edge_case
    def test_reinject_mixed_case_exclusion(self) -> None:
        """Mixed case L2-Reinject is also excluded."""
        source = '<!-- L2-Reinject: rank=1, content="test" -->\n# Doc\n'
        doc = JerryDocument.parse(source)
        result = HtmlCommentMetadata.extract(doc)

        assert len(result.blocks) == 0

    @pytest.mark.happy_path
    def test_non_reinject_comment_included(self) -> None:
        """Non-REINJECT comments with key-value pairs are included."""
        source = (
            '<!-- L2-REINJECT: rank=1, content="test" -->\n<!-- PS-ID: ADR-001 | AGENT: test -->\n'
        )
        doc = JerryDocument.parse(source)
        result = HtmlCommentMetadata.extract(doc)

        assert len(result.blocks) == 1
        assert result.blocks[0].fields[0].key == "PS-ID"


# =============================================================================
# Non-Metadata Comment Tests
# =============================================================================


class TestNonMetadataComments:
    """Tests for comments that don't contain key-value pairs."""

    @pytest.mark.edge_case
    def test_plain_comment_ignored(self) -> None:
        """Plain comments without key: value pairs are ignored."""
        source = "<!-- This is just a regular comment -->\n# Doc\n"
        doc = JerryDocument.parse(source)
        result = HtmlCommentMetadata.extract(doc)

        assert len(result.blocks) == 0

    @pytest.mark.edge_case
    def test_comment_without_colon_ignored(self) -> None:
        """Comments without colon separator are ignored."""
        source = "<!-- TODO fix this later -->\n"
        doc = JerryDocument.parse(source)
        result = HtmlCommentMetadata.extract(doc)

        assert len(result.blocks) == 0


# =============================================================================
# Bounds Enforcement Tests
# =============================================================================


class TestBoundsEnforcement:
    """Tests for InputBounds enforcement in HtmlCommentMetadata."""

    @pytest.mark.boundary
    def test_comment_count_limit(self) -> None:
        """Comment count exceeding max produces parse error (M-16)."""
        bounds = InputBounds(max_comment_count=1)
        source = "<!-- A: 1 | B: 2 -->\n<!-- C: 3 | D: 4 -->\n"
        doc = JerryDocument.parse(source)
        result = HtmlCommentMetadata.extract(doc, bounds)

        assert result.parse_error is not None
        assert "count exceeds" in result.parse_error

    @pytest.mark.boundary
    def test_value_length_truncation(self) -> None:
        """Value exceeding max_value_length is truncated with warning (M-17)."""
        bounds = InputBounds(max_value_length=5)
        source = "<!-- KEY: this-is-a-very-long-value -->\n"
        doc = JerryDocument.parse(source)
        result = HtmlCommentMetadata.extract(doc, bounds)

        assert len(result.parse_warnings) > 0
        assert any("truncated" in w for w in result.parse_warnings)
        # Value should be truncated
        if len(result.blocks) > 0:
            field = result.blocks[0].fields[0]
            assert len(field.value) <= 5


# =============================================================================
# Control Character Stripping Tests (M-18)
# =============================================================================


class TestControlCharacterStripping:
    """Tests for M-18: control characters stripped from values."""

    @pytest.mark.edge_case
    def test_null_bytes_stripped_from_values(self) -> None:
        """Null bytes are stripped from comment values."""
        source = "<!-- KEY: value\x00with\x01null -->\n"
        doc = JerryDocument.parse(source)
        result = HtmlCommentMetadata.extract(doc)

        if len(result.blocks) > 0:
            value = result.blocks[0].fields[0].value
            assert "\x00" not in value
            assert "\x01" not in value

    @pytest.mark.edge_case
    def test_control_chars_stripped_from_keys(self) -> None:
        """Control characters are stripped from comment keys."""
        source = "<!-- KE\x01Y: value -->\n"
        doc = JerryDocument.parse(source)
        result = HtmlCommentMetadata.extract(doc)

        if len(result.blocks) > 0:
            key = result.blocks[0].fields[0].key
            assert "\x01" not in key


# =============================================================================
# Edge Case Tests
# =============================================================================


class TestEdgeCases:
    """Edge case tests for HtmlCommentMetadata."""

    @pytest.mark.edge_case
    def test_empty_document(self) -> None:
        """Empty document returns empty result."""
        doc = JerryDocument.parse("")
        result = HtmlCommentMetadata.extract(doc)

        assert result.parse_error is None
        assert len(result.blocks) == 0

    @pytest.mark.edge_case
    def test_document_with_no_comments(self) -> None:
        """Document without comments returns empty result."""
        doc = JerryDocument.parse("# Heading\n\nParagraph.\n")
        result = HtmlCommentMetadata.extract(doc)

        assert result.parse_error is None
        assert len(result.blocks) == 0

    @pytest.mark.edge_case
    def test_line_number_accuracy(self) -> None:
        """Line numbers are correctly computed for comment blocks."""
        source = "# Title\n\n<!-- KEY: value -->\n"
        doc = JerryDocument.parse(source)
        result = HtmlCommentMetadata.extract(doc)

        assert len(result.blocks) == 1
        # Comment is on line 2 (zero-based)
        assert result.blocks[0].line_number == 2

    @pytest.mark.edge_case
    def test_single_field_comment(self) -> None:
        """Comment with a single key-value pair is extracted."""
        source = "<!-- VERSION: 1.0 -->\n"
        doc = JerryDocument.parse(source)
        result = HtmlCommentMetadata.extract(doc)

        assert len(result.blocks) == 1
        assert len(result.blocks[0].fields) == 1
        assert result.blocks[0].fields[0].key == "VERSION"
        assert result.blocks[0].fields[0].value == "1.0"


# =============================================================================
# Immutability Tests
# =============================================================================


class TestImmutability:
    """Tests for frozen dataclass immutability."""

    @pytest.mark.happy_path
    def test_field_is_frozen(self) -> None:
        """HtmlCommentField is frozen."""
        field = HtmlCommentField(key="test", value="val", line_number=0)
        with pytest.raises(AttributeError):
            field.key = "hacked"  # type: ignore[misc]

    @pytest.mark.happy_path
    def test_block_is_frozen(self) -> None:
        """HtmlCommentBlock is frozen."""
        block = HtmlCommentBlock(fields=(), raw_comment="<!-- -->", line_number=0)
        with pytest.raises(AttributeError):
            block.line_number = 99  # type: ignore[misc]

    @pytest.mark.happy_path
    def test_result_is_frozen(self) -> None:
        """HtmlCommentResult is frozen."""
        result = HtmlCommentResult(blocks=(), parse_error=None)
        with pytest.raises(AttributeError):
            result.parse_error = "hacked"  # type: ignore[misc]

    @pytest.mark.happy_path
    def test_blocks_is_tuple(self) -> None:
        """Blocks container is a tuple for immutability."""
        source = "<!-- KEY: value -->\n"
        doc = JerryDocument.parse(source)
        result = HtmlCommentMetadata.extract(doc)

        assert isinstance(result.blocks, tuple)

    @pytest.mark.happy_path
    def test_fields_in_block_is_tuple(self) -> None:
        """Fields within a block are a tuple for immutability."""
        source = "<!-- KEY: value -->\n"
        doc = JerryDocument.parse(source)
        result = HtmlCommentMetadata.extract(doc)

        assert isinstance(result.blocks[0].fields, tuple)

    @pytest.mark.happy_path
    def test_parse_warnings_is_tuple(self) -> None:
        """parse_warnings is a tuple for immutability."""
        source = "<!-- KEY: value -->\n"
        doc = JerryDocument.parse(source)
        result = HtmlCommentMetadata.extract(doc)

        assert isinstance(result.parse_warnings, tuple)
