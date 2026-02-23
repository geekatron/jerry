# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for UniversalDocument facade (WI-013).

Tests cover:
    - Parser invocation matrix correctness for all 11 DocumentType values
    - Explicit document_type override
    - Auto-detection via file_path
    - Structure-only detection fallback
    - Parse error aggregation (DD-9)
    - Type detection warning forwarding (M-14)
    - Deep immutability of result fields

References:
    - ADR-PROJ005-003 Design Decision 3 (Parser Invocation Matrix)
    - ADR-PROJ005-003 Design Decision 9 (Error Handling Strategy)
    - H-20: BDD test-first
"""

from __future__ import annotations

import pytest

from src.domain.markdown_ast.document_type import DocumentType
from src.domain.markdown_ast.universal_document import (
    UniversalDocument,
    UniversalParseResult,
)


# =============================================================================
# Fixtures
# =============================================================================


AGENT_DEF_SOURCE = """\
---
name: test-agent
version: 1.0.0
description: Test agent
model: opus
---

# Test Agent

<identity>
This is the identity section.
</identity>

<methodology>
This is the methodology.
</methodology>
"""

WORKTRACKER_SOURCE = """\
# EPIC-001 Test Epic

> **Type:** epic
> **Status:** pending
> **Priority:** high

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overview |

## Summary

An epic for testing.
"""

RULE_FILE_SOURCE = """\
# Test Rule

<!-- L2-REINJECT: rank=1, tokens=10, content="Test rule content." -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [HARD Rules](#hard-rules) | Constraints |

## HARD Rules

Some rules here.
"""

ADR_SOURCE = """\
# ADR: Test Decision

<!-- PS-ID: ADR-001 | ENTRY: 2026-02-23 | AGENT: test-agent -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [Status](#status) | State |
| [Context](#context) | Background |
| [Decision](#decision) | Choice |
| [Consequences](#consequences) | Results |

## Status

Accepted.

## Context

Some context.

## Decision

The decision.

## Consequences

Some consequences.
"""

STRATEGY_SOURCE = """\
# Strategy Template

> **Strategy:** Red Team Analysis
> **ID:** S-001
> **Family:** Role-Based Adversarialism

## Prompt Template

Execute red team analysis.

## Rubric

Score from 0 to 1.
"""


# =============================================================================
# Parser Invocation Matrix Tests (WI-013)
# =============================================================================


class TestParserInvocationMatrix:
    """Verify correct parsers are invoked per DocumentType."""

    @pytest.mark.happy_path
    def test_agent_definition_invokes_yaml_xml_nav(self) -> None:
        """AGENT_DEFINITION invokes YAML, XML, and nav parsers."""
        result = UniversalDocument.parse(
            AGENT_DEF_SOURCE,
            document_type=DocumentType.AGENT_DEFINITION,
        )
        assert result.document_type == DocumentType.AGENT_DEFINITION
        assert result.yaml_frontmatter is not None
        assert result.xml_sections is not None
        assert result.nav_entries is not None
        # Not invoked:
        assert result.blockquote_frontmatter is None
        assert result.html_comments is None
        assert result.reinject_directives is None

    @pytest.mark.happy_path
    def test_skill_definition_invokes_yaml_nav(self) -> None:
        """SKILL_DEFINITION invokes YAML and nav parsers."""
        source = "---\nname: test\nversion: 1.0.0\ndescription: test\n---\n# Skill\n"
        result = UniversalDocument.parse(
            source,
            document_type=DocumentType.SKILL_DEFINITION,
        )
        assert result.yaml_frontmatter is not None
        assert result.nav_entries is not None
        assert result.xml_sections is None
        assert result.blockquote_frontmatter is None

    @pytest.mark.happy_path
    def test_rule_file_invokes_reinject_nav(self) -> None:
        """RULE_FILE invokes reinject and nav parsers."""
        result = UniversalDocument.parse(
            RULE_FILE_SOURCE,
            document_type=DocumentType.RULE_FILE,
        )
        assert result.reinject_directives is not None
        assert len(result.reinject_directives) == 1
        assert result.nav_entries is not None
        assert result.yaml_frontmatter is None
        assert result.xml_sections is None

    @pytest.mark.happy_path
    def test_adr_invokes_html_nav(self) -> None:
        """ADR invokes HTML comment and nav parsers."""
        result = UniversalDocument.parse(
            ADR_SOURCE,
            document_type=DocumentType.ADR,
        )
        assert result.html_comments is not None
        assert result.nav_entries is not None
        assert result.yaml_frontmatter is None
        assert result.reinject_directives is None

    @pytest.mark.happy_path
    def test_strategy_template_invokes_blockquote_only(self) -> None:
        """STRATEGY_TEMPLATE invokes blockquote only (no nav)."""
        result = UniversalDocument.parse(
            STRATEGY_SOURCE,
            document_type=DocumentType.STRATEGY_TEMPLATE,
        )
        assert result.blockquote_frontmatter is not None
        assert result.nav_entries is None  # Excluded per matrix
        assert result.yaml_frontmatter is None

    @pytest.mark.happy_path
    def test_worktracker_entity_invokes_blockquote_nav(self) -> None:
        """WORKTRACKER_ENTITY invokes blockquote and nav parsers."""
        result = UniversalDocument.parse(
            WORKTRACKER_SOURCE,
            document_type=DocumentType.WORKTRACKER_ENTITY,
        )
        assert result.blockquote_frontmatter is not None
        assert result.nav_entries is not None
        assert result.yaml_frontmatter is None

    @pytest.mark.happy_path
    def test_framework_config_invokes_reinject_nav(self) -> None:
        """FRAMEWORK_CONFIG invokes reinject and nav parsers."""
        source = '<!-- L2-REINJECT: rank=1, tokens=5, content="test" -->\n# Config\n'
        result = UniversalDocument.parse(
            source,
            document_type=DocumentType.FRAMEWORK_CONFIG,
        )
        assert result.reinject_directives is not None
        assert result.nav_entries is not None

    @pytest.mark.happy_path
    def test_orchestration_artifact_invokes_html_nav(self) -> None:
        """ORCHESTRATION_ARTIFACT invokes HTML comment and nav parsers."""
        source = "<!-- PS-ID: test | ENTRY: 2026-02-23 -->\n# Orchestration\n"
        result = UniversalDocument.parse(
            source,
            document_type=DocumentType.ORCHESTRATION_ARTIFACT,
        )
        assert result.html_comments is not None
        assert result.nav_entries is not None

    @pytest.mark.happy_path
    def test_pattern_document_invokes_blockquote_nav(self) -> None:
        """PATTERN_DOCUMENT invokes blockquote and nav parsers."""
        source = "> **Name:** Test Pattern\n# Pattern\n"
        result = UniversalDocument.parse(
            source,
            document_type=DocumentType.PATTERN_DOCUMENT,
        )
        assert result.blockquote_frontmatter is not None
        assert result.nav_entries is not None

    @pytest.mark.happy_path
    def test_knowledge_document_invokes_nav_only(self) -> None:
        """KNOWLEDGE_DOCUMENT invokes nav parser only."""
        source = "# Knowledge\n\n## Summary\n\nSome knowledge.\n"
        result = UniversalDocument.parse(
            source,
            document_type=DocumentType.KNOWLEDGE_DOCUMENT,
        )
        assert result.nav_entries is not None
        assert result.yaml_frontmatter is None
        assert result.blockquote_frontmatter is None
        assert result.xml_sections is None
        assert result.html_comments is None
        assert result.reinject_directives is None

    @pytest.mark.happy_path
    def test_unknown_invokes_nav_only(self) -> None:
        """UNKNOWN type invokes nav parser only."""
        result = UniversalDocument.parse(
            "# Unknown Doc\n",
            document_type=DocumentType.UNKNOWN,
        )
        assert result.nav_entries is not None
        assert result.yaml_frontmatter is None


# =============================================================================
# Type Detection Tests
# =============================================================================


class TestTypeDetection:
    """Tests for document type detection in UniversalDocument.parse()."""

    @pytest.mark.happy_path
    def test_explicit_type_override(self) -> None:
        """Explicit document_type bypasses auto-detection."""
        result = UniversalDocument.parse(
            "# Just a heading\n",
            document_type=DocumentType.AGENT_DEFINITION,
        )
        assert result.document_type == DocumentType.AGENT_DEFINITION

    @pytest.mark.happy_path
    def test_auto_detection_from_path(self) -> None:
        """File path triggers auto-detection."""
        result = UniversalDocument.parse(
            AGENT_DEF_SOURCE,
            file_path="skills/test/agents/test-agent.md",
        )
        assert result.document_type == DocumentType.AGENT_DEFINITION

    @pytest.mark.happy_path
    def test_structure_only_detection(self) -> None:
        """When no file_path and no document_type, uses structure detection."""
        # Use content with "> **" cue but no "---" (table separators contain
        # "---" which would match AGENT_DEFINITION first in the priority list).
        simple_worktracker = (
            "# EPIC-001 Test Epic\n\n"
            "> **Type:** epic\n"
            "> **Status:** pending\n\n"
            "## Summary\n\nAn epic for testing.\n"
        )
        result = UniversalDocument.parse(simple_worktracker)
        # Structure detection finds "> **" -> WORKTRACKER_ENTITY
        assert result.document_type == DocumentType.WORKTRACKER_ENTITY

    @pytest.mark.edge_case
    def test_type_detection_warning_on_mismatch(self) -> None:
        """Warning generated when path and structure disagree (M-14)."""
        # Path says RULE_FILE, but content has "> **" (worktracker structure)
        result = UniversalDocument.parse(
            WORKTRACKER_SOURCE,
            file_path=".context/rules/test-rule.md",
        )
        assert result.document_type == DocumentType.RULE_FILE  # Path wins
        assert result.type_detection_warning is not None
        assert "content structure suggests" in result.type_detection_warning


# =============================================================================
# Parse Error Aggregation Tests (DD-9)
# =============================================================================


class TestParseErrorAggregation:
    """Tests for parse error aggregation."""

    @pytest.mark.happy_path
    def test_no_errors_on_valid_input(self) -> None:
        """No parse errors for valid input."""
        result = UniversalDocument.parse(
            AGENT_DEF_SOURCE,
            document_type=DocumentType.AGENT_DEFINITION,
        )
        assert result.parse_errors == ()

    @pytest.mark.negative
    def test_yaml_parse_error_aggregated(self) -> None:
        """YAML parse errors are collected in parse_errors."""
        invalid_yaml = "---\n: invalid yaml:\n  bad: [unclosed\n---\n"
        result = UniversalDocument.parse(
            invalid_yaml,
            document_type=DocumentType.AGENT_DEFINITION,
        )
        assert len(result.parse_errors) > 0
        assert any("YamlFrontmatter" in e for e in result.parse_errors)

    @pytest.mark.happy_path
    def test_parse_errors_is_tuple(self) -> None:
        """parse_errors is a tuple for immutability."""
        result = UniversalDocument.parse("# Test\n", document_type=DocumentType.UNKNOWN)
        assert isinstance(result.parse_errors, tuple)


# =============================================================================
# Result Immutability Tests
# =============================================================================


class TestResultImmutability:
    """Tests for UniversalParseResult immutability."""

    @pytest.mark.happy_path
    def test_result_is_frozen(self) -> None:
        """UniversalParseResult is a frozen dataclass."""
        result = UniversalDocument.parse("# Test\n", document_type=DocumentType.UNKNOWN)
        with pytest.raises(AttributeError):
            result.document_type = DocumentType.ADR  # type: ignore[misc]

    @pytest.mark.happy_path
    def test_xml_sections_is_tuple(self) -> None:
        """XML sections are returned as tuple."""
        result = UniversalDocument.parse(
            AGENT_DEF_SOURCE,
            document_type=DocumentType.AGENT_DEFINITION,
        )
        assert isinstance(result.xml_sections, tuple)

    @pytest.mark.happy_path
    def test_nav_entries_is_tuple(self) -> None:
        """Nav entries are returned as tuple."""
        result = UniversalDocument.parse(
            WORKTRACKER_SOURCE,
            document_type=DocumentType.WORKTRACKER_ENTITY,
        )
        assert isinstance(result.nav_entries, tuple)

    @pytest.mark.happy_path
    def test_reinject_directives_is_tuple(self) -> None:
        """Reinject directives are returned as tuple."""
        result = UniversalDocument.parse(
            RULE_FILE_SOURCE,
            document_type=DocumentType.RULE_FILE,
        )
        assert isinstance(result.reinject_directives, tuple)


# =============================================================================
# JerryDocument Always Present
# =============================================================================


class TestJerryDocumentPresent:
    """Verify JerryDocument is always present in results."""

    @pytest.mark.happy_path
    def test_jerry_document_always_set(self) -> None:
        """jerry_document is never None."""
        result = UniversalDocument.parse("# Simple\n", document_type=DocumentType.UNKNOWN)
        assert result.jerry_document is not None
        assert result.jerry_document.source == "# Simple\n"


# =============================================================================
# UniversalParseResult Import Coverage
# =============================================================================


class TestUniversalParseResultDataclass:
    """Coverage for UniversalParseResult frozen dataclass."""

    @pytest.mark.happy_path
    def test_parse_result_is_importable(self) -> None:
        """UniversalParseResult can be imported from its own module."""
        from src.domain.markdown_ast.universal_parse_result import (
            UniversalParseResult as UPR,
        )
        # Verify the class exists and is a dataclass
        import dataclasses
        assert dataclasses.is_dataclass(UPR)

    @pytest.mark.happy_path
    def test_parse_result_fields_correct(self) -> None:
        """UniversalParseResult has all expected fields."""
        import dataclasses

        field_names = {f.name for f in dataclasses.fields(UniversalParseResult)}
        expected = {
            "document_type", "jerry_document", "yaml_frontmatter",
            "blockquote_frontmatter", "xml_sections", "html_comments",
            "reinject_directives", "nav_entries", "type_detection_warning",
            "parse_errors",
        }
        assert field_names == expected
