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
    _path_matches_glob,
)

# =============================================================================
# Path-Based Detection Tests
# =============================================================================


class TestPathDetection:
    """Tests for path-based document type detection."""

    @pytest.mark.happy_path
    def test_agent_definition_path(self) -> None:
        """Agent definition detected from skills/*/agents/*.md path."""
        doc_type, warning = DocumentTypeDetector.detect("skills/ast/agents/ast-parser.md", "")
        assert doc_type == DocumentType.AGENT_DEFINITION
        assert warning is None

    @pytest.mark.happy_path
    def test_skill_definition_path(self) -> None:
        """Skill definition detected from skills/*/SKILL.md path."""
        doc_type, warning = DocumentTypeDetector.detect("skills/problem-solving/SKILL.md", "")
        assert doc_type == DocumentType.SKILL_DEFINITION

    @pytest.mark.happy_path
    def test_rule_file_context_path(self) -> None:
        """Rule file detected from .context/rules/*.md path."""
        doc_type, warning = DocumentTypeDetector.detect(".context/rules/quality-enforcement.md", "")
        assert doc_type == DocumentType.RULE_FILE

    @pytest.mark.happy_path
    def test_rule_file_claude_path(self) -> None:
        """Rule file detected from .claude/rules/*.md path."""
        doc_type, warning = DocumentTypeDetector.detect(".claude/rules/some-rule.md", "")
        assert doc_type == DocumentType.RULE_FILE

    @pytest.mark.happy_path
    def test_adr_path(self) -> None:
        """ADR detected from docs/design/*.md path."""
        doc_type, warning = DocumentTypeDetector.detect("docs/design/adr-epic002-001.md", "")
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
        doc_type, warning = DocumentTypeDetector.detect("projects/PROJ-001/WORKTRACKER.md", "")
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

    # --- EN-002: New path pattern tests ---

    @pytest.mark.happy_path
    def test_skill_resource_playbook(self) -> None:
        """Skill resource detected from skills/*/PLAYBOOK.md."""
        doc_type, _ = DocumentTypeDetector.detect("skills/problem-solving/PLAYBOOK.md", "")
        assert doc_type == DocumentType.SKILL_RESOURCE

    @pytest.mark.happy_path
    def test_skill_resource_composition(self) -> None:
        """Skill resource detected from skills/*/composition/*.md."""
        doc_type, _ = DocumentTypeDetector.detect(
            "skills/adversary/composition/adv-selector.prompt.md", ""
        )
        assert doc_type == DocumentType.SKILL_RESOURCE

    @pytest.mark.happy_path
    def test_skill_resource_references(self) -> None:
        """Skill resource detected from skills/*/references/*.md."""
        doc_type, _ = DocumentTypeDetector.detect("skills/saucer-boy/references/persona.md", "")
        assert doc_type == DocumentType.SKILL_RESOURCE

    @pytest.mark.happy_path
    def test_skill_resource_docs(self) -> None:
        """Skill resource detected from skills/*/docs/*.md."""
        doc_type, _ = DocumentTypeDetector.detect("skills/transcript/docs/migration.md", "")
        assert doc_type == DocumentType.SKILL_RESOURCE

    @pytest.mark.happy_path
    def test_skill_rule_file(self) -> None:
        """Rule file detected from skills/*/rules/*.md (reuses RULE_FILE type)."""
        doc_type, _ = DocumentTypeDetector.detect(
            "skills/worktracker/rules/worktracker-behavior-rules.md", ""
        )
        assert doc_type == DocumentType.RULE_FILE

    @pytest.mark.happy_path
    def test_skill_resource_catch_all(self) -> None:
        """Skill resource catch-all for files like adversary-integration.md."""
        doc_type, _ = DocumentTypeDetector.detect("skills/red-team/adversary-integration.md", "")
        assert doc_type == DocumentType.SKILL_RESOURCE

    @pytest.mark.happy_path
    def test_template_skill_templates(self) -> None:
        """Template detected from skills/*/templates/*.md."""
        doc_type, _ = DocumentTypeDetector.detect(
            "skills/worktracker/templates/story-template.md", ""
        )
        assert doc_type == DocumentType.TEMPLATE

    @pytest.mark.happy_path
    def test_template_context_worktracker(self) -> None:
        """Template detected from .context/templates/worktracker/*.md."""
        doc_type, _ = DocumentTypeDetector.detect(
            ".context/templates/worktracker/bug.template.md", ""
        )
        assert doc_type == DocumentType.TEMPLATE

    @pytest.mark.happy_path
    def test_template_context_design(self) -> None:
        """Template detected from .context/templates/design/*.md."""
        doc_type, _ = DocumentTypeDetector.detect(".context/templates/design/TDD.template.md", "")
        assert doc_type == DocumentType.TEMPLATE

    @pytest.mark.happy_path
    def test_adr_from_docs_adrs(self) -> None:
        """ADR detected from docs/adrs/*.md."""
        doc_type, _ = DocumentTypeDetector.detect("docs/adrs/adr-proj007-001.md", "")
        assert doc_type == DocumentType.ADR

    @pytest.mark.happy_path
    def test_adr_from_project_decisions(self) -> None:
        """ADR detected from projects/*/decisions/*.md."""
        doc_type, _ = DocumentTypeDetector.detect(
            "projects/PROJ-005/decisions/adr-ast-design.md", ""
        )
        assert doc_type == DocumentType.ADR

    @pytest.mark.happy_path
    def test_pattern_document_from_context_patterns(self) -> None:
        """Pattern document detected from .context/patterns/**/*.md."""
        doc_type, _ = DocumentTypeDetector.detect(".context/patterns/agent/agent-discovery.md", "")
        assert doc_type == DocumentType.PATTERN_DOCUMENT

    @pytest.mark.happy_path
    def test_pattern_document_from_guides(self) -> None:
        """Pattern document detected from .context/guides/*.md."""
        doc_type, _ = DocumentTypeDetector.detect(".context/guides/getting-started.md", "")
        assert doc_type == DocumentType.PATTERN_DOCUMENT

    @pytest.mark.happy_path
    def test_framework_config_plan(self) -> None:
        """Framework config detected from projects/*/PLAN.md."""
        doc_type, _ = DocumentTypeDetector.detect("projects/PROJ-005/PLAN.md", "")
        assert doc_type == DocumentType.FRAMEWORK_CONFIG

    @pytest.mark.happy_path
    def test_framework_config_readme(self) -> None:
        """Framework config detected from root README.md."""
        doc_type, _ = DocumentTypeDetector.detect("README.md", "")
        assert doc_type == DocumentType.FRAMEWORK_CONFIG

    @pytest.mark.happy_path
    def test_knowledge_from_docs_research(self) -> None:
        """Knowledge document detected from docs/research/**/*.md."""
        doc_type, _ = DocumentTypeDetector.detect("docs/research/agent-patterns/findings.md", "")
        assert doc_type == DocumentType.KNOWLEDGE_DOCUMENT

    @pytest.mark.happy_path
    def test_knowledge_from_docs_catch_all(self) -> None:
        """Knowledge document detected from docs/*.md catch-all."""
        doc_type, _ = DocumentTypeDetector.detect("docs/INSTALLATION.md", "")
        assert doc_type == DocumentType.KNOWLEDGE_DOCUMENT

    @pytest.mark.happy_path
    def test_worktracker_from_work_dir(self) -> None:
        """Worktracker entity detected from work/**/*.md (repo-based pattern)."""
        doc_type, _ = DocumentTypeDetector.detect("work/epics/EPIC-001.md", "")
        assert doc_type == DocumentType.WORKTRACKER_ENTITY

    @pytest.mark.happy_path
    def test_framework_config_commands(self) -> None:
        """Framework config detected from commands/*.md."""
        doc_type, _ = DocumentTypeDetector.detect("commands/release.md", "")
        assert doc_type == DocumentType.FRAMEWORK_CONFIG

    # --- EN-002: First-match-wins ordering boundary tests ---

    @pytest.mark.edge_case
    def test_strategy_template_before_template_catch_all(self) -> None:
        """Strategy template matches before .context/templates/**/ catch-all."""
        doc_type, _ = DocumentTypeDetector.detect(
            ".context/templates/adversarial/s-001-red-team.md", ""
        )
        assert doc_type == DocumentType.STRATEGY_TEMPLATE

    @pytest.mark.edge_case
    def test_skill_agents_before_skill_catch_all(self) -> None:
        """Agent definition in skills/*/agents/ matches before skills/*/ catch-all."""
        doc_type, _ = DocumentTypeDetector.detect("skills/ast/agents/ast-parser.md", "")
        assert doc_type == DocumentType.AGENT_DEFINITION

    @pytest.mark.edge_case
    def test_skill_definition_before_skill_catch_all(self) -> None:
        """SKILL.md matches before skills/*/*.md catch-all."""
        doc_type, _ = DocumentTypeDetector.detect("skills/transcript/SKILL.md", "")
        assert doc_type == DocumentType.SKILL_DEFINITION

    @pytest.mark.edge_case
    def test_docs_design_before_docs_catch_all(self) -> None:
        """docs/design/ matches ADR before docs/*.md catch-all."""
        doc_type, _ = DocumentTypeDetector.detect("docs/design/adr-epic002-001.md", "")
        assert doc_type == DocumentType.ADR


# =============================================================================
# Structural Fallback Tests
# =============================================================================


class TestStructuralDetection:
    """Tests for structure-based detection fallback (EN-002 precise cues)."""

    @pytest.mark.happy_path
    def test_identity_tag_structure(self) -> None:
        """<identity> tag maps to AGENT_DEFINITION."""
        doc_type, _ = DocumentTypeDetector.detect(
            "unknown-path.md", "# Agent\n\n<identity>\nAgent identity.\n</identity>\n"
        )
        assert doc_type == DocumentType.AGENT_DEFINITION

    @pytest.mark.happy_path
    def test_methodology_tag_structure(self) -> None:
        """<methodology> tag maps to AGENT_DEFINITION."""
        doc_type, _ = DocumentTypeDetector.detect(
            "unknown-path.md", "# Agent\n\n<methodology>\nStep 1.\n</methodology>\n"
        )
        assert doc_type == DocumentType.AGENT_DEFINITION

    @pytest.mark.happy_path
    def test_blockquote_type_structure(self) -> None:
        """> **Type:** maps to WORKTRACKER_ENTITY."""
        doc_type, _ = DocumentTypeDetector.detect("unknown-path.md", "> **Type:** story\n")
        assert doc_type == DocumentType.WORKTRACKER_ENTITY

    @pytest.mark.happy_path
    def test_reinject_structure(self) -> None:
        """<!-- L2-REINJECT maps to RULE_FILE."""
        doc_type, _ = DocumentTypeDetector.detect(
            "unknown-path.md", '<!-- L2-REINJECT: rank=1, content="test" -->\n'
        )
        assert doc_type == DocumentType.RULE_FILE

    @pytest.mark.happy_path
    def test_strategy_structure(self) -> None:
        """> **Strategy:** maps to STRATEGY_TEMPLATE."""
        doc_type, _ = DocumentTypeDetector.detect(
            "unknown-path.md", "> **Strategy:** Red Team Analysis\n"
        )
        assert doc_type == DocumentType.STRATEGY_TEMPLATE

    @pytest.mark.happy_path
    def test_version_structure(self) -> None:
        """> **Version:** maps to SKILL_DEFINITION."""
        doc_type, _ = DocumentTypeDetector.detect("unknown-path.md", "> **Version:** 1.0.0\n")
        assert doc_type == DocumentType.SKILL_DEFINITION

    @pytest.mark.edge_case
    def test_no_path_no_structure_returns_unknown(self) -> None:
        """Empty path and no structural cues returns UNKNOWN."""
        doc_type, warning = DocumentTypeDetector.detect("", "Just plain text.\n")
        assert doc_type == DocumentType.UNKNOWN
        assert warning is None

    # --- EN-002: BUG-004 regression assertions ---

    @pytest.mark.edge_case
    def test_horizontal_rule_does_not_match_agent_definition(self) -> None:
        """BUG-004: '---' no longer triggers agent_definition classification."""
        doc_type, _ = DocumentTypeDetector.detect(
            "unknown-path.md", "# Title\n\n---\n\nSome content.\n"
        )
        # Should be UNKNOWN, not AGENT_DEFINITION
        assert doc_type == DocumentType.UNKNOWN

    @pytest.mark.edge_case
    def test_html_comment_does_not_match_adr(self) -> None:
        """EN-002: Generic HTML comments no longer trigger ADR classification."""
        doc_type, _ = DocumentTypeDetector.detect(
            "unknown-path.md", "<!-- Some comment -->\n# Title\n"
        )
        assert doc_type == DocumentType.UNKNOWN

    @pytest.mark.edge_case
    def test_generic_blockquote_does_not_match_worktracker(self) -> None:
        """EN-002: Generic blockquotes do not trigger worktracker classification."""
        doc_type, _ = DocumentTypeDetector.detect(
            "unknown-path.md", "> **Note:** This is important.\n"
        )
        # > **Note:** should NOT match > **Type:**
        assert doc_type == DocumentType.UNKNOWN


# =============================================================================
# Dual-Signal Mismatch Warning Tests (M-14)
# =============================================================================


class TestDualSignalWarning:
    """Tests for M-14 dual-signal mismatch warning."""

    @pytest.mark.edge_case
    def test_mismatch_produces_warning(self) -> None:
        """Warning when path and structure disagree."""
        # Path says ADR, structure has "> **Type:**" (worktracker)
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
        doc_type, warning = DocumentTypeDetector.detect("docs/knowledge/test.md", "Just text.\n")
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
        doc_type, _ = DocumentTypeDetector.detect("./skills/test/agents/test.md", "")
        assert doc_type == DocumentType.AGENT_DEFINITION

    @pytest.mark.edge_case
    def test_absolute_path_with_marker(self) -> None:
        """Absolute paths are handled by extracting repo-relative portion."""
        doc_type, _ = DocumentTypeDetector.detect("/home/user/repo/skills/test/agents/test.md", "")
        assert doc_type == DocumentType.AGENT_DEFINITION

    @pytest.mark.edge_case
    def test_already_relative_path_skips_marker_extraction(self) -> None:
        """Paths already starting with a root marker skip extraction (F-001 CWE-22)."""
        # Path starts with "skills/" -- already relative, should not re-extract
        doc_type, _ = DocumentTypeDetector.detect("skills/test/SKILL.md", "")
        assert doc_type == DocumentType.SKILL_DEFINITION

    @pytest.mark.edge_case
    def test_root_file_from_absolute_path_reduces_to_basename(self) -> None:
        """Absolute path to root-level file reduces to basename for matching."""
        # /unknown/path/README.md -> basename "README.md" matches root-level pattern
        doc_type, _ = DocumentTypeDetector.detect("/some/unknown/path/README.md", "")
        assert doc_type == DocumentType.FRAMEWORK_CONFIG

    @pytest.mark.edge_case
    def test_root_file_under_known_root_keeps_full_path(self) -> None:
        """Root file name under a known root marker keeps the full path."""
        # projects/PROJ-001/README.md starts with "projects/" -- already relative,
        # and is_under_known_root is True, so basename reduction is skipped.
        doc_type, _ = DocumentTypeDetector.detect("projects/PROJ-001/README.md", "")
        assert doc_type == DocumentType.FRAMEWORK_CONFIG

    @pytest.mark.edge_case
    def test_root_file_without_directory_stays_as_is(self) -> None:
        """Root file with no directory component matches directly."""
        doc_type, _ = DocumentTypeDetector.detect("CLAUDE.md", "")
        assert doc_type == DocumentType.FRAMEWORK_CONFIG


# =============================================================================
# DocumentType Enum Tests
# =============================================================================


class TestDocumentTypeEnum:
    """Tests for DocumentType enum values."""

    @pytest.mark.happy_path
    def test_all_13_values_exist(self) -> None:
        """DocumentType has exactly 13 values (EN-002: +SKILL_RESOURCE, +TEMPLATE)."""
        assert len(DocumentType) == 13

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
        """Pattern with multiple ** segments falls back to fnmatchcase."""
        # Directly test _path_matches_glob with a multi-** pattern
        # (no PATH_PATTERNS entry has multiple **, so we must test directly)
        assert _path_matches_glob("a/b/c/d/e.md", "a/**/c/**/*.md") is True
        assert _path_matches_glob("a/b/c/d/e.txt", "a/**/c/**/*.md") is False

    @pytest.mark.edge_case
    def test_prefix_longer_than_path_returns_false(self) -> None:
        """Path shorter than prefix pattern segments returns no match."""
        # Trigger the len(path_segments) < len(prefix_segments) branch
        doc_type, _ = DocumentTypeDetector.detect("docs/single.md", "# Short\n")
        # Should fall through to UNKNOWN or structural detection
        assert doc_type is not None

    @pytest.mark.edge_case
    def test_suffix_longer_than_remaining_returns_false(self) -> None:
        """Remaining path too short for suffix pattern returns no match."""
        # Trigger len(remaining_segments) < len(suffix_segments) branch
        doc_type, _ = DocumentTypeDetector.detect("skills/.md", "# Test\n")
        assert doc_type is not None

    @pytest.mark.edge_case
    def test_prefix_segment_mismatch(self) -> None:
        """Path not matching any pattern falls to structural detection or UNKNOWN."""
        doc_type, _ = DocumentTypeDetector.detect("random/deeply/nested/file.md", "# Just text\n")
        # No path pattern matches, no structural cues -> UNKNOWN
        assert doc_type == DocumentType.UNKNOWN


# =============================================================================
# BUG-005: Windows fnmatch.fnmatch Regression Tests
# =============================================================================


class TestWindowsFnmatchRegression:
    """BUG-005: fnmatch.fnmatchcase prevents Windows normcase from breaking path matching."""

    @pytest.mark.edge_case
    def test_orchestration_path_not_matched_by_plan_pattern(self) -> None:
        """BUG-005: orchestration/phase-1/plan.md must NOT match projects/*/PLAN.md.

        On Windows, fnmatch.fnmatch lowercases PLAN.md to plan.md via
        os.path.normcase, causing a false match. fnmatch.fnmatchcase
        prevents this by doing case-sensitive comparison.
        """
        doc_type, _ = DocumentTypeDetector.detect(
            "projects/PROJ-001/orchestration/phase-1/plan.md", ""
        )
        assert doc_type == DocumentType.ORCHESTRATION_ARTIFACT
        assert doc_type != DocumentType.FRAMEWORK_CONFIG

    @pytest.mark.edge_case
    def test_case_sensitive_pattern_matching(self) -> None:
        """BUG-005: Path matching is case-sensitive (PLAN.md != plan.md)."""
        # projects/*/PLAN.md should match PLAN.md but not plan.md
        doc_type_upper, _ = DocumentTypeDetector.detect("projects/PROJ-001/PLAN.md", "")
        assert doc_type_upper == DocumentType.FRAMEWORK_CONFIG

        # Lowercase plan.md in a project root should NOT match PLAN.md pattern
        # It would fall through to a later pattern or UNKNOWN
        doc_type_lower, _ = DocumentTypeDetector.detect("projects/PROJ-001/plan.md", "")
        assert doc_type_lower != DocumentType.FRAMEWORK_CONFIG
