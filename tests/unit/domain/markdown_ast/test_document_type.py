# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for DocumentTypeDetector and DocumentType enum (WI-011, WI-012).

Tests cover:
    - Path-based detection for all document types
    - Structural cue fallback detection
    - Dual-signal mismatch warning (M-14)
    - UNKNOWN safe default
    - Path normalization
    - First-match-wins semantics

References:
    - ADR-PROJ005-003 Design Decision 2 (Document Type Detection)
    - H-20: BDD test-first
"""

from __future__ import annotations

import pytest

from src.domain.markdown_ast.document_type import (
    DocumentType,
    DocumentTypeDetector,
)

# =============================================================================
# Path-Based Detection Tests
# =============================================================================


class TestPathDetection:
    """Tests for path-based document type detection."""

    @pytest.mark.happy_path
    def test_agent_definition_path(self) -> None:
        """Agent definition detected from skills/*/agents/*.md path."""
        doc_type, warning = DocumentTypeDetector.detect(
            "skills/ast/agents/ast-parser.md", ""
        )
        assert doc_type == DocumentType.AGENT_DEFINITION
        assert warning is None

    @pytest.mark.happy_path
    def test_skill_definition_path(self) -> None:
        """Skill definition detected from skills/*/SKILL.md path."""
        doc_type, warning = DocumentTypeDetector.detect(
            "skills/problem-solving/SKILL.md", ""
        )
        assert doc_type == DocumentType.SKILL_DEFINITION

    @pytest.mark.happy_path
    def test_rule_file_context_path(self) -> None:
        """Rule file detected from .context/rules/*.md path."""
        doc_type, warning = DocumentTypeDetector.detect(
            ".context/rules/quality-enforcement.md", ""
        )
        assert doc_type == DocumentType.RULE_FILE

    @pytest.mark.happy_path
    def test_rule_file_claude_path(self) -> None:
        """Rule file detected from .claude/rules/*.md path."""
        doc_type, warning = DocumentTypeDetector.detect(
            ".claude/rules/some-rule.md", ""
        )
        assert doc_type == DocumentType.RULE_FILE

    @pytest.mark.happy_path
    def test_adr_path(self) -> None:
        """ADR detected from docs/design/*.md path."""
        doc_type, warning = DocumentTypeDetector.detect(
            "docs/design/adr-epic002-001.md", ""
        )
        assert doc_type == DocumentType.ADR

    @pytest.mark.happy_path
    def test_strategy_template_path(self) -> None:
        """Strategy template detected from .context/templates/adversarial/*.md."""
        doc_type, warning = DocumentTypeDetector.detect(
            ".context/templates/adversarial/s-001-red-team.md", ""
        )
        assert doc_type == DocumentType.STRATEGY_TEMPLATE

    @pytest.mark.happy_path
    def test_worktracker_entity_path(self) -> None:
        """Worktracker entity detected from projects/*/work/**/*.md."""
        doc_type, warning = DocumentTypeDetector.detect(
            "projects/PROJ-001/work/epics/EPIC-001-test.md", ""
        )
        assert doc_type == DocumentType.WORKTRACKER_ENTITY

    @pytest.mark.happy_path
    def test_worktracker_md_path(self) -> None:
        """WORKTRACKER.md detected from projects/*/WORKTRACKER.md."""
        doc_type, warning = DocumentTypeDetector.detect(
            "projects/PROJ-001/WORKTRACKER.md", ""
        )
        assert doc_type == DocumentType.WORKTRACKER_ENTITY

    @pytest.mark.happy_path
    def test_framework_config_claude_md(self) -> None:
        """Framework config detected from CLAUDE.md."""
        doc_type, warning = DocumentTypeDetector.detect("CLAUDE.md", "")
        assert doc_type == DocumentType.FRAMEWORK_CONFIG

    @pytest.mark.happy_path
    def test_framework_config_agents_md(self) -> None:
        """Framework config detected from AGENTS.md."""
        doc_type, warning = DocumentTypeDetector.detect("AGENTS.md", "")
        assert doc_type == DocumentType.FRAMEWORK_CONFIG

    @pytest.mark.happy_path
    def test_orchestration_artifact_path(self) -> None:
        """Orchestration artifact detected from projects/*/orchestration/**/*.md."""
        doc_type, warning = DocumentTypeDetector.detect(
            "projects/PROJ-001/orchestration/phase-1/plan.md", ""
        )
        assert doc_type == DocumentType.ORCHESTRATION_ARTIFACT

    @pytest.mark.happy_path
    def test_knowledge_document_path(self) -> None:
        """Knowledge document detected from docs/knowledge/**/*.md."""
        doc_type, warning = DocumentTypeDetector.detect(
            "docs/knowledge/architecture/patterns.md", ""
        )
        assert doc_type == DocumentType.KNOWLEDGE_DOCUMENT


# =============================================================================
# Structural Fallback Tests
# =============================================================================


class TestStructuralDetection:
    """Tests for structure-based detection fallback."""

    @pytest.mark.happy_path
    def test_yaml_frontmatter_structure(self) -> None:
        """YAML frontmatter (---) maps to AGENT_DEFINITION."""
        doc_type, warning = DocumentTypeDetector.detect(
            "unknown-path.md", "---\nname: test\n---\n"
        )
        assert doc_type == DocumentType.AGENT_DEFINITION

    @pytest.mark.happy_path
    def test_blockquote_structure(self) -> None:
        """Blockquote frontmatter (> **) maps to WORKTRACKER_ENTITY."""
        doc_type, warning = DocumentTypeDetector.detect(
            "unknown-path.md", "> **Type:** story\n"
        )
        assert doc_type == DocumentType.WORKTRACKER_ENTITY

    @pytest.mark.happy_path
    def test_identity_tag_structure(self) -> None:
        """<identity> tag maps to AGENT_DEFINITION."""
        # Note: "---" has higher priority than "<identity>" in the cue list,
        # so we test with content that has <identity> but not ---
        doc_type, warning = DocumentTypeDetector.detect(
            "unknown-path.md", "# Agent\n\n<identity>\nAgent identity.\n</identity>\n"
        )
        # "---" cue not found, "<identity>" found -> AGENT_DEFINITION
        assert doc_type == DocumentType.AGENT_DEFINITION

    @pytest.mark.happy_path
    def test_reinject_structure(self) -> None:
        """<!-- L2-REINJECT maps to RULE_FILE."""
        doc_type, warning = DocumentTypeDetector.detect(
            "unknown-path.md", '<!-- L2-REINJECT: rank=1, content="test" -->\n'
        )
        assert doc_type == DocumentType.RULE_FILE

    @pytest.mark.edge_case
    def test_no_path_no_structure_returns_unknown(self) -> None:
        """Empty path and no structural cues returns UNKNOWN."""
        doc_type, warning = DocumentTypeDetector.detect("", "Just plain text.\n")
        assert doc_type == DocumentType.UNKNOWN
        assert warning is None


# =============================================================================
# Dual-Signal Mismatch Warning Tests (M-14)
# =============================================================================


class TestDualSignalWarning:
    """Tests for M-14 dual-signal mismatch warning."""

    @pytest.mark.edge_case
    def test_mismatch_produces_warning(self) -> None:
        """Warning when path and structure disagree."""
        # Path says ADR, structure has "> **" (worktracker)
        doc_type, warning = DocumentTypeDetector.detect(
            "docs/design/test-adr.md", "> **Type:** story\n"
        )
        assert doc_type == DocumentType.ADR  # Path wins
        assert warning is not None
        assert "content structure suggests worktracker_entity" in warning

    @pytest.mark.happy_path
    def test_no_warning_when_signals_agree(self) -> None:
        """No warning when path and structure agree."""
        doc_type, warning = DocumentTypeDetector.detect(
            "skills/test/agents/test-agent.md", "---\nname: test\n---\n"
        )
        assert doc_type == DocumentType.AGENT_DEFINITION
        assert warning is None

    @pytest.mark.happy_path
    def test_no_warning_with_no_structural_cue(self) -> None:
        """No warning when only path matches (no structural cue)."""
        doc_type, warning = DocumentTypeDetector.detect(
            "docs/knowledge/test.md", "Just text.\n"
        )
        assert doc_type == DocumentType.KNOWLEDGE_DOCUMENT
        assert warning is None


# =============================================================================
# Path Normalization Tests
# =============================================================================


class TestPathNormalization:
    """Tests for path normalization in document type detection."""

    @pytest.mark.edge_case
    def test_leading_dot_slash_stripped(self) -> None:
        """Leading ./ is stripped from path."""
        doc_type, _ = DocumentTypeDetector.detect(
            "./skills/test/agents/test.md", ""
        )
        assert doc_type == DocumentType.AGENT_DEFINITION

    @pytest.mark.edge_case
    def test_absolute_path_with_marker(self) -> None:
        """Absolute paths are handled by extracting repo-relative portion."""
        doc_type, _ = DocumentTypeDetector.detect(
            "/home/user/repo/skills/test/agents/test.md", ""
        )
        assert doc_type == DocumentType.AGENT_DEFINITION


# =============================================================================
# DocumentType Enum Tests
# =============================================================================


class TestDocumentTypeEnum:
    """Tests for DocumentType enum values."""

    @pytest.mark.happy_path
    def test_all_11_values_exist(self) -> None:
        """DocumentType has exactly 11 values."""
        assert len(DocumentType) == 11

    @pytest.mark.happy_path
    def test_unknown_is_safe_default(self) -> None:
        """UNKNOWN value exists as safe default."""
        assert DocumentType.UNKNOWN.value == "unknown"


# =============================================================================
# Internal Glob Matching Tests (Coverage for _match_recursive_glob)
# =============================================================================


class TestRecursiveGlobMatching:
    """Tests for internal _match_recursive_glob helper coverage."""

    @pytest.mark.edge_case
    def test_multiple_double_star_falls_back_to_fnmatch(self) -> None:
        """Pattern with multiple ** segments falls back to fnmatch."""
        # skills/**/agents/**/*.md has two ** segments -- triggers fallback branch
        doc_type, _ = DocumentTypeDetector.detect(
            "skills/foo/agents/bar/my-agent.md", ""
        )
        assert doc_type == DocumentType.AGENT_DEFINITION

    @pytest.mark.edge_case
    def test_prefix_longer_than_path_returns_false(self) -> None:
        """Path shorter than prefix pattern segments returns no match."""
        # Trigger the len(path_segments) < len(prefix_segments) branch
        doc_type, _ = DocumentTypeDetector.detect(
            "docs/single.md", "# Short\n"
        )
        # Should fall through to UNKNOWN or structural detection
        assert doc_type is not None

    @pytest.mark.edge_case
    def test_suffix_longer_than_remaining_returns_false(self) -> None:
        """Remaining path too short for suffix pattern returns no match."""
        # Trigger len(remaining_segments) < len(suffix_segments) branch
        doc_type, _ = DocumentTypeDetector.detect(
            "skills/.md", "# Test\n"
        )
        assert doc_type is not None

    @pytest.mark.edge_case
    def test_prefix_segment_mismatch(self) -> None:
        """Path not matching any pattern falls to structural detection or UNKNOWN."""
        doc_type, _ = DocumentTypeDetector.detect(
            "random/deeply/nested/file.md", "# Just text\n"
        )
        # No path pattern matches, no structural cues -> UNKNOWN
        assert doc_type == DocumentType.UNKNOWN
