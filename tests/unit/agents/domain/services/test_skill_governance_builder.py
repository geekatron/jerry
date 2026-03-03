# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for SkillGovernanceSectionBuilder domain service.

Coverage targets:
- build() generates each section when field is non-empty
- build() skips sections for empty/default fields
- build() deduplicates against existing headings (case-insensitive)
- Activation keywords rendered as bullet list
- Agents rendered as bullet list
- Context injection rendered as YAML code block
"""

from __future__ import annotations

import pytest

from src.agents.domain.entities.canonical_skill import CanonicalSkill
from src.agents.domain.services.skill_governance_builder import (
    SkillGovernanceSectionBuilder,
)


@pytest.fixture()
def builder() -> SkillGovernanceSectionBuilder:
    """Fresh builder instance."""
    return SkillGovernanceSectionBuilder()


@pytest.fixture()
def make_skill() -> callable:
    """Factory for creating CanonicalSkill instances."""

    def _make(**overrides) -> CanonicalSkill:
        defaults = {
            "name": "test-skill",
            "version": "1.0.0",
        }
        defaults.update(overrides)
        return CanonicalSkill(**defaults)

    return _make


class TestBuildVersionSection:
    """Tests for ## Skill Version section."""

    @pytest.mark.happy_path
    def test_build_when_version_present_then_skill_version_heading_generated(
        self, builder: SkillGovernanceSectionBuilder, make_skill: callable
    ) -> None:
        # Arrange
        skill = make_skill(version="2.1.0")

        # Act
        result = builder.build(skill)

        # Assert
        assert "## Skill Version" in result
        assert "2.1.0" in result

    @pytest.mark.edge_case
    def test_build_when_version_empty_then_no_skill_version_section(
        self, builder: SkillGovernanceSectionBuilder, make_skill: callable
    ) -> None:
        # Arrange
        skill = make_skill(version="")

        # Act
        result = builder.build(skill)

        # Assert
        assert "## Skill Version" not in result


class TestBuildActivationKeywordsSection:
    """Tests for ## Activation Keywords section."""

    @pytest.mark.happy_path
    def test_build_when_keywords_present_then_bullet_list_generated(
        self, builder: SkillGovernanceSectionBuilder, make_skill: callable
    ) -> None:
        # Arrange
        skill = make_skill(activation_keywords=("research", "analyze", "investigate"))

        # Act
        result = builder.build(skill)

        # Assert
        assert "## Activation Keywords" in result
        assert "- research" in result
        assert "- analyze" in result
        assert "- investigate" in result

    @pytest.mark.boundary
    def test_build_when_no_keywords_then_no_activation_keywords_section(
        self, builder: SkillGovernanceSectionBuilder, make_skill: callable
    ) -> None:
        # Arrange
        skill = make_skill(activation_keywords=())

        # Act
        result = builder.build(skill)

        # Assert
        assert "## Activation Keywords" not in result

    @pytest.mark.edge_case
    def test_build_when_single_keyword_then_single_bullet(
        self, builder: SkillGovernanceSectionBuilder, make_skill: callable
    ) -> None:
        # Arrange
        skill = make_skill(activation_keywords=("solo-keyword",))

        # Act
        result = builder.build(skill)

        # Assert
        assert "## Activation Keywords" in result
        assert "- solo-keyword" in result


class TestBuildAgentRegistrySection:
    """Tests for ## Agent Registry section."""

    @pytest.mark.happy_path
    def test_build_when_agents_present_then_bullet_list_generated(
        self, builder: SkillGovernanceSectionBuilder, make_skill: callable
    ) -> None:
        # Arrange
        skill = make_skill(agents=("ps-researcher", "ps-analyst", "ps-critic"))

        # Act
        result = builder.build(skill)

        # Assert
        assert "## Agent Registry" in result
        assert "- ps-researcher" in result
        assert "- ps-analyst" in result
        assert "- ps-critic" in result

    @pytest.mark.boundary
    def test_build_when_no_agents_then_no_agent_registry_section(
        self, builder: SkillGovernanceSectionBuilder, make_skill: callable
    ) -> None:
        # Arrange
        skill = make_skill(agents=())

        # Act
        result = builder.build(skill)

        # Assert
        assert "## Agent Registry" not in result


class TestBuildContextInjectionSection:
    """Tests for ## Context Injection section."""

    @pytest.mark.happy_path
    def test_build_when_context_injection_present_then_yaml_code_block(
        self, builder: SkillGovernanceSectionBuilder, make_skill: callable
    ) -> None:
        # Arrange
        skill = make_skill(
            context_injection={"rules": ["quality-enforcement.md", "coding-standards.md"]}
        )

        # Act
        result = builder.build(skill)

        # Assert
        assert "## Context Injection" in result
        assert "```yaml" in result
        assert "quality-enforcement.md" in result
        assert "```" in result

    @pytest.mark.boundary
    def test_build_when_empty_context_injection_then_no_section(
        self, builder: SkillGovernanceSectionBuilder, make_skill: callable
    ) -> None:
        # Arrange
        skill = make_skill(context_injection={})

        # Act
        result = builder.build(skill)

        # Assert
        assert "## Context Injection" not in result


class TestBuildAllSections:
    """Tests for build() with multiple fields."""

    @pytest.mark.happy_path
    def test_build_when_all_fields_present_then_all_four_sections_generated(
        self, builder: SkillGovernanceSectionBuilder, make_skill: callable
    ) -> None:
        # Arrange
        skill = make_skill(
            version="1.2.0",
            activation_keywords=("research", "analyze"),
            agents=("ps-researcher",),
            context_injection={"rules": ["test.md"]},
        )

        # Act
        result = builder.build(skill)

        # Assert
        assert "## Skill Version" in result
        assert "## Activation Keywords" in result
        assert "## Agent Registry" in result
        assert "## Context Injection" in result

    @pytest.mark.edge_case
    def test_build_when_only_version_then_only_skill_version_section(
        self, builder: SkillGovernanceSectionBuilder, make_skill: callable
    ) -> None:
        # Arrange
        skill = make_skill(
            version="1.0.0",
            activation_keywords=(),
            agents=(),
            context_injection={},
        )

        # Act
        result = builder.build(skill)

        # Assert
        assert "## Skill Version" in result
        assert "## Activation Keywords" not in result
        assert "## Agent Registry" not in result
        assert "## Context Injection" not in result

    @pytest.mark.boundary
    def test_build_when_all_fields_empty_then_empty_string(
        self, builder: SkillGovernanceSectionBuilder, make_skill: callable
    ) -> None:
        # Arrange
        skill = make_skill(
            version="",
            activation_keywords=(),
            agents=(),
            context_injection={},
        )

        # Act
        result = builder.build(skill)

        # Assert
        assert result == ""


class TestHeadingDedup:
    """Tests for duplicate heading prevention."""

    @pytest.mark.happy_path
    def test_build_when_existing_heading_matches_then_section_skipped(
        self, builder: SkillGovernanceSectionBuilder, make_skill: callable
    ) -> None:
        # Arrange
        skill = make_skill(version="2.0.0")
        existing_body = "## Skill Version\n\n2.0.0\n"

        # Act
        result = builder.build(skill, existing_body=existing_body)

        # Assert
        assert "## Skill Version" not in result

    @pytest.mark.edge_case
    def test_build_when_heading_exists_case_insensitive_then_section_skipped(
        self, builder: SkillGovernanceSectionBuilder, make_skill: callable
    ) -> None:
        # Arrange
        skill = make_skill(
            version="2.0.0",
            activation_keywords=("test",),
        )
        existing_body = "## SKILL VERSION\n\n2.0.0\n\n## ACTIVATION KEYWORDS\n\n- test\n"

        # Act
        result = builder.build(skill, existing_body=existing_body)

        # Assert
        assert "## Skill Version" not in result
        assert "## Activation Keywords" not in result

    @pytest.mark.happy_path
    def test_build_when_some_headings_exist_then_only_missing_sections_generated(
        self, builder: SkillGovernanceSectionBuilder, make_skill: callable
    ) -> None:
        # Arrange
        skill = make_skill(
            version="1.0.0",
            activation_keywords=("research",),
            agents=("ps-researcher",),
        )
        existing_body = "## Skill Version\n\n1.0.0\n"

        # Act
        result = builder.build(skill, existing_body=existing_body)

        # Assert
        assert "## Skill Version" not in result
        assert "## Activation Keywords" in result
        assert "## Agent Registry" in result

    @pytest.mark.edge_case
    def test_build_when_heading_has_html_comment_then_still_detected(
        self, builder: SkillGovernanceSectionBuilder, make_skill: callable
    ) -> None:
        # Arrange
        skill = make_skill(version="1.0.0")
        existing_body = "## Skill Version <!-- injected -->\n\n1.0.0\n"

        # Act
        result = builder.build(skill, existing_body=existing_body)

        # Assert
        assert "## Skill Version" not in result
