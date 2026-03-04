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
        """FM-06: Regression test for heading dedup with HTML comment spacing."""
        # Arrange
        skill = make_skill(version="1.0.0")
        existing_body = "## Skill Version <!-- injected -->\n\n1.0.0\n"

        # Act
        result = builder.build(skill, existing_body=existing_body)

        # Assert
        assert "## Skill Version" not in result


class TestXmlTagDedup:
    """Tests for XML governance tag dedup during re-composition.

    When a SKILL.md body already has XML governance tags from a previous
    compose, the builder must skip those sections (dedup) to prevent
    duplication.
    """

    @pytest.mark.happy_path
    def test_build_when_xml_skill_version_tag_exists_then_section_skipped(
        self, builder: SkillGovernanceSectionBuilder, make_skill: callable
    ) -> None:
        # Arrange
        skill = make_skill(version="2.0.0")
        existing_body = "<skill_version>\n2.0.0\n</skill_version>\n"

        # Act
        result = builder.build(skill, existing_body=existing_body)

        # Assert
        assert "## Skill Version" not in result

    @pytest.mark.happy_path
    def test_build_when_xml_activation_keywords_tag_exists_then_section_skipped(
        self, builder: SkillGovernanceSectionBuilder, make_skill: callable
    ) -> None:
        # Arrange
        skill = make_skill(activation_keywords=("research", "analyze"))
        existing_body = "<activation_keywords>\n- research\n- analyze\n</activation_keywords>\n"

        # Act
        result = builder.build(skill, existing_body=existing_body)

        # Assert
        assert "## Activation Keywords" not in result

    @pytest.mark.happy_path
    def test_build_when_xml_agent_registry_tag_exists_then_section_skipped(
        self, builder: SkillGovernanceSectionBuilder, make_skill: callable
    ) -> None:
        # Arrange
        skill = make_skill(agents=("ps-researcher",))
        existing_body = "<agent_registry>\n- ps-researcher\n</agent_registry>\n"

        # Act
        result = builder.build(skill, existing_body=existing_body)

        # Assert
        assert "## Agent Registry" not in result

    @pytest.mark.happy_path
    def test_build_when_xml_context_injection_tag_exists_then_section_skipped(
        self, builder: SkillGovernanceSectionBuilder, make_skill: callable
    ) -> None:
        # Arrange
        skill = make_skill(context_injection={"rules": ["test.md"]})
        existing_body = "<context_injection>\nrules:\n- test.md\n</context_injection>\n"

        # Act
        result = builder.build(skill, existing_body=existing_body)

        # Assert
        assert "## Context Injection" not in result

    @pytest.mark.edge_case
    def test_build_when_mixed_xml_and_heading_then_all_skipped(
        self, builder: SkillGovernanceSectionBuilder, make_skill: callable
    ) -> None:
        """Re-composition with mix of XML tags and ## headings."""
        # Arrange
        skill = make_skill(
            version="1.0.0",
            activation_keywords=("test",),
        )
        existing_body = (
            "<skill_version>\n1.0.0\n</skill_version>\n\n## Activation Keywords\n\n- test\n"
        )

        # Act
        result = builder.build(skill, existing_body=existing_body)

        # Assert
        assert "## Skill Version" not in result
        assert "## Activation Keywords" not in result

    @pytest.mark.edge_case
    def test_build_when_self_closing_xml_tag_then_section_skipped(
        self, builder: SkillGovernanceSectionBuilder, make_skill: callable
    ) -> None:
        # Arrange — self-closing tag variant
        skill = make_skill(version="1.0.0")
        existing_body = "<skill_version/>\n"

        # Act
        result = builder.build(skill, existing_body=existing_body)

        # Assert
        assert "## Skill Version" not in result


class TestContextInjectionDeterminism:
    """FM-13: Context injection output must be deterministic regardless of dict insertion order.

    Verifies the FM-13 fix (sort_keys=True) in SkillGovernanceSectionBuilder.build().
    """

    @pytest.mark.happy_path
    def test_build_when_dict_insertion_order_differs_then_identical_output(
        self, builder: SkillGovernanceSectionBuilder, make_skill: callable
    ) -> None:
        """FM-13: Verify sort_keys=True produces identical YAML for dicts with different insertion order."""
        # Arrange — two dicts with identical content but different insertion order
        dict_a = {"zebra": "last", "alpha": "first", "middle": "center"}
        dict_b = {"alpha": "first", "middle": "center", "zebra": "last"}

        skill_a = make_skill(context_injection=dict_a)
        skill_b = make_skill(context_injection=dict_b)

        # Act
        result_a = builder.build(skill_a)
        result_b = builder.build(skill_b)

        # Assert — both must produce byte-identical output
        assert result_a == result_b
        assert "## Context Injection" in result_a

    @pytest.mark.edge_case
    def test_build_when_nested_dict_order_differs_then_identical_output(
        self, builder: SkillGovernanceSectionBuilder, make_skill: callable
    ) -> None:
        """FM-13: Verify determinism extends to nested dict structures."""
        # Arrange — nested dicts with different insertion order
        nested_a = {"rules": {"z_rule": "val", "a_rule": "val"}, "templates": ["t1"]}
        nested_b = {"templates": ["t1"], "rules": {"a_rule": "val", "z_rule": "val"}}

        skill_a = make_skill(context_injection=nested_a)
        skill_b = make_skill(context_injection=nested_b)

        # Act
        result_a = builder.build(skill_a)
        result_b = builder.build(skill_b)

        # Assert
        assert result_a == result_b
