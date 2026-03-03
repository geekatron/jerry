# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for CanonicalSkill domain entity.

Coverage targets:
- Construction with all fields (happy path)
- Construction with defaults (happy path)
- Frozen immutability (security)
- Empty/boundary values (boundary)
- Single-char and edge-case names (edge case)
"""

from __future__ import annotations

import pytest

from src.agents.domain.entities.canonical_skill import CanonicalSkill


class TestCanonicalSkillConstruction:
    """Tests for CanonicalSkill dataclass construction."""

    @pytest.mark.happy_path
    def test_construction_when_all_fields_provided_then_all_accessible(self) -> None:
        # Arrange / Act
        skill = CanonicalSkill(
            name="problem-solving",
            version="1.2.0",
            activation_keywords=("research", "analyze"),
            agents=("ps-researcher", "ps-analyst"),
            context_injection={"rules": ["quality-enforcement.md"]},
            license="Apache-2.0",
            compatibility="Claude Code >= 1.0",
            metadata={"author": "test"},
            skill_body="# Problem Solving\n\nBody content.",
        )

        # Assert
        assert skill.name == "problem-solving"
        assert skill.version == "1.2.0"
        assert skill.activation_keywords == ("research", "analyze")
        assert skill.agents == ("ps-researcher", "ps-analyst")
        assert skill.context_injection == {"rules": ["quality-enforcement.md"]}
        assert skill.license == "Apache-2.0"
        assert skill.compatibility == "Claude Code >= 1.0"
        assert skill.metadata == {"author": "test"}
        assert skill.skill_body == "# Problem Solving\n\nBody content."

    @pytest.mark.happy_path
    def test_construction_when_only_required_fields_then_defaults_applied(self) -> None:
        # Arrange / Act
        skill = CanonicalSkill(name="minimal", version="0.1.0")

        # Assert
        assert skill.name == "minimal"
        assert skill.version == "0.1.0"
        assert skill.activation_keywords == ()
        assert skill.agents == ()
        assert skill.context_injection == {}
        assert skill.license == ""
        assert skill.compatibility == ""
        assert skill.metadata == {}
        assert skill.skill_body == ""


class TestCanonicalSkillBoundary:
    """Tests for boundary values."""

    @pytest.mark.boundary
    def test_construction_when_zero_agents_then_empty_tuple(self) -> None:
        # Arrange / Act
        skill = CanonicalSkill(name="no-agents", version="1.0.0", agents=())

        # Assert
        assert skill.agents == ()
        assert len(skill.agents) == 0

    @pytest.mark.boundary
    def test_construction_when_zero_activation_keywords_then_empty_tuple(self) -> None:
        # Arrange / Act
        skill = CanonicalSkill(name="no-keywords", version="1.0.0", activation_keywords=())

        # Assert
        assert skill.activation_keywords == ()
        assert len(skill.activation_keywords) == 0

    @pytest.mark.boundary
    def test_construction_when_single_agent_then_tuple_of_one(self) -> None:
        # Arrange / Act
        skill = CanonicalSkill(name="one-agent", version="1.0.0", agents=("solo-agent",))

        # Assert
        assert len(skill.agents) == 1
        assert skill.agents[0] == "solo-agent"

    @pytest.mark.boundary
    def test_construction_when_many_agents_then_all_preserved(self) -> None:
        # Arrange
        agents = tuple(f"agent-{i}" for i in range(20))

        # Act
        skill = CanonicalSkill(name="many-agents", version="1.0.0", agents=agents)

        # Assert
        assert len(skill.agents) == 20
        assert skill.agents[0] == "agent-0"
        assert skill.agents[19] == "agent-19"


class TestCanonicalSkillEdgeCase:
    """Tests for edge-case values."""

    @pytest.mark.edge_case
    def test_construction_when_single_char_name_then_accepted(self) -> None:
        # Arrange / Act
        skill = CanonicalSkill(name="x", version="1.0.0")

        # Assert
        assert skill.name == "x"

    @pytest.mark.edge_case
    def test_construction_when_empty_name_then_still_constructs(self) -> None:
        # Arrange / Act — dataclass does not enforce non-empty
        skill = CanonicalSkill(name="", version="1.0.0")

        # Assert
        assert skill.name == ""

    @pytest.mark.edge_case
    def test_construction_when_empty_version_then_still_constructs(self) -> None:
        # Arrange / Act
        skill = CanonicalSkill(name="test", version="")

        # Assert
        assert skill.version == ""

    @pytest.mark.edge_case
    def test_construction_when_empty_context_injection_then_empty_dict(self) -> None:
        # Arrange / Act
        skill = CanonicalSkill(name="test", version="1.0.0", context_injection={})

        # Assert
        assert skill.context_injection == {}

    @pytest.mark.edge_case
    def test_construction_when_multiline_skill_body_then_preserved(self) -> None:
        # Arrange
        body = "# Title\n\nParagraph 1.\n\n## Section\n\nParagraph 2.\n"

        # Act
        skill = CanonicalSkill(name="body-test", version="1.0.0", skill_body=body)

        # Assert
        assert skill.skill_body == body
        assert "\n\n" in skill.skill_body


class TestCanonicalSkillSecurity:
    """Security-focused tests for frozen dataclass."""

    @pytest.mark.security
    def test_frozen_dataclass_when_mutate_name_then_raises_frozen_error(self) -> None:
        # Arrange
        skill = CanonicalSkill(name="immutable", version="1.0.0")

        # Act / Assert
        with pytest.raises(AttributeError):
            skill.name = "mutated"  # type: ignore[misc]

    @pytest.mark.security
    def test_frozen_dataclass_when_mutate_version_then_raises_frozen_error(self) -> None:
        # Arrange
        skill = CanonicalSkill(name="immutable", version="1.0.0")

        # Act / Assert
        with pytest.raises(AttributeError):
            skill.version = "9.9.9"  # type: ignore[misc]

    @pytest.mark.security
    def test_frozen_dataclass_when_mutate_agents_then_raises_frozen_error(self) -> None:
        # Arrange
        skill = CanonicalSkill(name="immutable", version="1.0.0", agents=("agent-1",))

        # Act / Assert
        with pytest.raises(AttributeError):
            skill.agents = ("agent-2",)  # type: ignore[misc]

    @pytest.mark.security
    def test_frozen_dataclass_when_mutate_activation_keywords_then_raises_frozen_error(
        self,
    ) -> None:
        # Arrange
        skill = CanonicalSkill(
            name="immutable",
            version="1.0.0",
            activation_keywords=("keyword-1",),
        )

        # Act / Assert
        with pytest.raises(AttributeError):
            skill.activation_keywords = ("keyword-2",)  # type: ignore[misc]
