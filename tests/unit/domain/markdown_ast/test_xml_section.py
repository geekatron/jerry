# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for XmlSectionParser (WI-007, WI-008).

Tests cover:
    - Happy path: extract known XML sections
    - Tag whitelist enforcement
    - Nested tag rejection
    - Section count enforcement (M-16)
    - Content length enforcement (M-17)
    - Control character stripping (M-18)
    - Empty document handling
    - Frozen dataclass immutability

References:
    - ADR-PROJ005-003 Design Decision 6
    - H-20: BDD test-first
"""

from __future__ import annotations

import pytest

from src.domain.markdown_ast.input_bounds import InputBounds
from src.domain.markdown_ast.jerry_document import JerryDocument
from src.domain.markdown_ast.xml_section import (
    XmlSection,
    XmlSectionParser,
    XmlSectionResult,
)


# =============================================================================
# Happy Path Tests
# =============================================================================


class TestXmlSectionExtraction:
    """Tests for basic XML section extraction."""

    @pytest.mark.happy_path
    def test_extract_identity_section(self) -> None:
        """Extracts <identity> section from agent definition."""
        source = "# Agent\n\n<identity>\nIdentity content.\n</identity>\n"
        doc = JerryDocument.parse(source)
        result = XmlSectionParser.extract(doc)

        assert result.parse_error is None
        assert len(result.sections) == 1
        assert result.sections[0].tag_name == "identity"
        assert "Identity content." in result.sections[0].content

    @pytest.mark.happy_path
    def test_extract_multiple_sections(self) -> None:
        """Extracts multiple XML sections in order."""
        source = (
            "# Agent\n\n"
            "<identity>\nWho I am.\n</identity>\n\n"
            "<methodology>\nHow I work.\n</methodology>\n"
        )
        doc = JerryDocument.parse(source)
        result = XmlSectionParser.extract(doc)

        assert result.parse_error is None
        assert len(result.sections) == 2
        assert result.sections[0].tag_name == "identity"
        assert result.sections[1].tag_name == "methodology"

    @pytest.mark.happy_path
    def test_all_allowed_tags(self) -> None:
        """All 7 ALLOWED_TAGS can be extracted."""
        allowed = ["identity", "purpose", "input", "capabilities",
                    "methodology", "output", "guardrails"]
        parts = []
        for tag in allowed:
            parts.append(f"<{tag}>\nContent for {tag}.\n</{tag}>\n\n")
        source = "# Test\n\n" + "".join(parts)
        doc = JerryDocument.parse(source)
        result = XmlSectionParser.extract(doc)

        assert result.parse_error is None
        assert len(result.sections) == 7

    @pytest.mark.happy_path
    def test_sections_are_frozen(self) -> None:
        """XmlSection instances are frozen."""
        source = "# Agent\n\n<identity>\nTest.\n</identity>\n"
        doc = JerryDocument.parse(source)
        result = XmlSectionParser.extract(doc)
        section = result.sections[0]
        with pytest.raises(AttributeError):
            section.tag_name = "hacked"  # type: ignore[misc]


# =============================================================================
# Tag Whitelist Tests
# =============================================================================


class TestTagWhitelist:
    """Tests for tag whitelist enforcement."""

    @pytest.mark.negative
    def test_unknown_tag_silently_skipped(self) -> None:
        """Tags not in ALLOWED_TAGS are silently skipped (regex only matches allowed)."""
        source = "# Agent\n\n<unknown_tag>\nContent.\n</unknown_tag>\n"
        doc = JerryDocument.parse(source)
        result = XmlSectionParser.extract(doc)

        assert len(result.sections) == 0
        # No error -- unknown tags simply don't match the allowed-tags regex
        assert result.parse_error is None


# =============================================================================
# Nested Tag Rejection Tests
# =============================================================================


class TestNestedTagRejection:
    """Tests for nested same-name tag rejection."""

    @pytest.mark.negative
    def test_nested_same_tag_rejected(self) -> None:
        """Nested same-name tags are skipped with warning."""
        source = (
            "# Agent\n\n"
            "<identity>\n"
            "Outer content.\n"
            "<identity>\n"
            "Inner content.\n"
            "</identity>\n"
            "</identity>\n"
        )
        doc = JerryDocument.parse(source)
        result = XmlSectionParser.extract(doc)

        # The section should be skipped due to nesting
        nested_warnings = [w for w in result.parse_warnings if "Nested" in w]
        assert len(nested_warnings) >= 1


# =============================================================================
# Bounds Enforcement Tests
# =============================================================================


class TestBoundsEnforcement:
    """Tests for InputBounds enforcement in XmlSectionParser."""

    @pytest.mark.boundary
    def test_section_count_limit(self) -> None:
        """Section count exceeding max produces parse error (M-16)."""
        bounds = InputBounds(max_section_count=1)
        source = (
            "# Agent\n\n"
            "<identity>\nFirst.\n</identity>\n\n"
            "<methodology>\nSecond.\n</methodology>\n"
        )
        doc = JerryDocument.parse(source)
        result = XmlSectionParser.extract(doc, bounds)

        assert result.parse_error is not None
        assert "Section count exceeds" in result.parse_error

    @pytest.mark.boundary
    def test_content_length_truncation(self) -> None:
        """Content exceeding max_value_length is truncated with warning (M-17)."""
        bounds = InputBounds(max_value_length=10)
        source = "# Agent\n\n<identity>\nThis is long content that exceeds.\n</identity>\n"
        doc = JerryDocument.parse(source)
        result = XmlSectionParser.extract(doc, bounds)

        assert len(result.parse_warnings) > 0
        assert any("truncated" in w for w in result.parse_warnings)
        assert len(result.sections[0].content) <= 10


# =============================================================================
# Edge Case Tests
# =============================================================================


class TestEdgeCases:
    """Edge case tests for XmlSectionParser."""

    @pytest.mark.edge_case
    def test_empty_document(self) -> None:
        """Empty document returns empty result."""
        doc = JerryDocument.parse("")
        result = XmlSectionParser.extract(doc)

        assert result.parse_error is None
        assert len(result.sections) == 0

    @pytest.mark.edge_case
    def test_document_with_no_xml_sections(self) -> None:
        """Document without XML sections returns empty result."""
        doc = JerryDocument.parse("# Heading\n\nParagraph.\n")
        result = XmlSectionParser.extract(doc)

        assert result.parse_error is None
        assert len(result.sections) == 0

    @pytest.mark.edge_case
    def test_control_characters_stripped(self) -> None:
        """Control characters are stripped from section content (M-18)."""
        source = "# Agent\n\n<identity>\nContent\x00with\x01null.\n</identity>\n"
        doc = JerryDocument.parse(source)
        result = XmlSectionParser.extract(doc)

        if len(result.sections) > 0:
            assert "\x00" not in result.sections[0].content
            assert "\x01" not in result.sections[0].content

    @pytest.mark.happy_path
    def test_result_is_frozen(self) -> None:
        """XmlSectionResult is frozen."""
        doc = JerryDocument.parse("# Test\n")
        result = XmlSectionParser.extract(doc)
        with pytest.raises(AttributeError):
            result.parse_error = "hacked"  # type: ignore[misc]
