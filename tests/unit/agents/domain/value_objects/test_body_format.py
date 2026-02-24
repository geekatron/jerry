# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for BodyFormat value object.

Tests enum membership and from_string() parsing across happy paths,
negative cases, and edge cases (case normalisation, whitespace stripping).
"""

from __future__ import annotations

import pytest

from src.agents.domain.value_objects.body_format import BodyFormat

# =============================================================================
# Tests: Enum membership and values
# =============================================================================


class TestBodyFormatEnum:
    """Verify all three format members and their string values."""

    @pytest.mark.happy_path
    def test_xml_value(self) -> None:
        """XML member has the canonical lowercase string value."""
        assert BodyFormat.XML.value == "xml"

    @pytest.mark.happy_path
    def test_markdown_value(self) -> None:
        """MARKDOWN member has the canonical lowercase string value."""
        assert BodyFormat.MARKDOWN.value == "markdown"

    @pytest.mark.happy_path
    def test_rccf_value(self) -> None:
        """RCCF member has the canonical lowercase string value."""
        assert BodyFormat.RCCF.value == "rccf"

    @pytest.mark.happy_path
    def test_exactly_three_members(self) -> None:
        """Enum contains exactly three members."""
        assert len(list(BodyFormat)) == 3

    @pytest.mark.happy_path
    def test_all_values_unique(self) -> None:
        """All enum values are distinct strings."""
        values = [f.value for f in BodyFormat]
        assert len(values) == len(set(values))


# =============================================================================
# Tests: from_string() — happy paths
# =============================================================================


class TestFromString:
    """BodyFormat.from_string() parsing tests."""

    @pytest.mark.happy_path
    def test_xml_lowercase(self) -> None:
        """Lowercase 'xml' parses to XML."""
        # Arrange / Act / Assert
        assert BodyFormat.from_string("xml") is BodyFormat.XML

    @pytest.mark.happy_path
    def test_markdown_lowercase(self) -> None:
        """Lowercase 'markdown' parses to MARKDOWN."""
        assert BodyFormat.from_string("markdown") is BodyFormat.MARKDOWN

    @pytest.mark.happy_path
    def test_rccf_lowercase(self) -> None:
        """Lowercase 'rccf' parses to RCCF."""
        assert BodyFormat.from_string("rccf") is BodyFormat.RCCF

    # ------------------------------------------------------------------
    # Edge cases: case normalisation
    # ------------------------------------------------------------------

    @pytest.mark.edge_case
    def test_xml_uppercase(self) -> None:
        """Uppercase 'XML' is normalised and parses correctly."""
        assert BodyFormat.from_string("XML") is BodyFormat.XML

    @pytest.mark.edge_case
    def test_markdown_uppercase(self) -> None:
        """Uppercase 'MARKDOWN' is normalised and parses correctly."""
        assert BodyFormat.from_string("MARKDOWN") is BodyFormat.MARKDOWN

    @pytest.mark.edge_case
    def test_rccf_uppercase(self) -> None:
        """Uppercase 'RCCF' is normalised and parses correctly."""
        assert BodyFormat.from_string("RCCF") is BodyFormat.RCCF

    @pytest.mark.edge_case
    def test_mixed_case_xml(self) -> None:
        """Mixed-case 'Xml' is normalised and parses correctly."""
        assert BodyFormat.from_string("Xml") is BodyFormat.XML

    @pytest.mark.edge_case
    def test_mixed_case_markdown(self) -> None:
        """Mixed-case 'Markdown' is normalised correctly."""
        assert BodyFormat.from_string("Markdown") is BodyFormat.MARKDOWN

    # ------------------------------------------------------------------
    # Edge cases: whitespace stripping
    # ------------------------------------------------------------------

    @pytest.mark.edge_case
    def test_leading_whitespace_stripped(self) -> None:
        """Leading whitespace is stripped before matching."""
        assert BodyFormat.from_string("  xml") is BodyFormat.XML

    @pytest.mark.edge_case
    def test_trailing_whitespace_stripped(self) -> None:
        """Trailing whitespace is stripped before matching."""
        assert BodyFormat.from_string("rccf  ") is BodyFormat.RCCF

    @pytest.mark.edge_case
    def test_whitespace_and_case_combined(self) -> None:
        """Both whitespace stripping and case normalisation apply together."""
        assert BodyFormat.from_string("  MARKDOWN  ") is BodyFormat.MARKDOWN

    # ------------------------------------------------------------------
    # Negative cases
    # ------------------------------------------------------------------

    @pytest.mark.negative
    def test_invalid_format_raises_value_error(self) -> None:
        """Unknown format name raises ValueError with a helpful message."""
        with pytest.raises(ValueError, match="Invalid body format"):
            BodyFormat.from_string("html")

    @pytest.mark.negative
    def test_empty_string_raises_value_error(self) -> None:
        """Empty string is not a valid format and raises ValueError."""
        with pytest.raises(ValueError, match="Invalid body format"):
            BodyFormat.from_string("")

    @pytest.mark.negative
    def test_whitespace_only_raises_value_error(self) -> None:
        """Whitespace-only string normalises to empty and raises ValueError."""
        with pytest.raises(ValueError, match="Invalid body format"):
            BodyFormat.from_string("   ")

    @pytest.mark.negative
    def test_partial_name_raises_value_error(self) -> None:
        """Partial format name (e.g. 'mark') is not accepted."""
        with pytest.raises(ValueError, match="Invalid body format"):
            BodyFormat.from_string("mark")

    @pytest.mark.negative
    def test_error_message_lists_all_valid_formats(self) -> None:
        """ValueError message includes every valid format name."""
        with pytest.raises(ValueError) as exc_info:
            BodyFormat.from_string("yaml")
        message = str(exc_info.value)
        assert "xml" in message
        assert "markdown" in message
        assert "rccf" in message

    @pytest.mark.negative
    def test_numeric_string_raises_value_error(self) -> None:
        """A numeric string is not a valid format."""
        with pytest.raises(ValueError, match="Invalid body format"):
            BodyFormat.from_string("1")
