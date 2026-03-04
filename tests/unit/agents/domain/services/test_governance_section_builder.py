# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for GovernanceSectionBuilder domain service.

Coverage targets:
- build() with individual governance fields present/absent
- build() with all fields present generates all sections
- build() with all fields empty generates no sections
- Sections appended after existing body content
- Existing headings not duplicated
"""

from __future__ import annotations

from typing import Any

import pytest

from src.agents.domain.services.governance_section_builder import GovernanceSectionBuilder
from src.agents.domain.value_objects.tool_tier import ToolTier


class TestBuildVersionSection:
    """Tests for version governance section."""

    def test_build_version_section_when_version_present_then_heading_with_version(
        self, make_canonical_agent: Any
    ) -> None:
        # Arrange
        builder = GovernanceSectionBuilder()
        agent = make_canonical_agent(version="2.1.0")

        # Act
        result = builder.build(agent)

        # Assert
        assert "## Agent Version" in result
        assert "2.1.0" in result


class TestBuildToolTierSection:
    """Tests for tool tier governance section."""

    def test_build_tool_tier_section_when_tier_set_then_heading_with_tier_value(
        self, make_canonical_agent: Any
    ) -> None:
        # Arrange
        builder = GovernanceSectionBuilder()
        agent = make_canonical_agent(tool_tier=ToolTier.T3)

        # Act
        result = builder.build(agent)

        # Assert
        assert "## Tool Tier" in result
        assert "T3" in result

    @pytest.mark.parametrize(
        ("tier", "expected_label"),
        [
            (ToolTier.T1, "Read-Only"),
            (ToolTier.T2, "Read-Write"),
            (ToolTier.T3, "External"),
            (ToolTier.T4, "Persistent"),
            (ToolTier.T5, "Full"),
        ],
    )
    def test_build_tool_tier_section_includes_human_label(
        self, make_canonical_agent: Any, tier: ToolTier, expected_label: str
    ) -> None:
        # Arrange
        builder = GovernanceSectionBuilder()
        agent = make_canonical_agent(tool_tier=tier)

        # Act
        result = builder.build(agent)

        # Assert
        assert expected_label in result


class TestBuildEnforcementSection:
    """Tests for enforcement governance section."""

    def test_build_enforcement_section_when_enforcement_present_then_heading_with_content(
        self, make_canonical_agent: Any
    ) -> None:
        # Arrange
        builder = GovernanceSectionBuilder()
        agent = make_canonical_agent(
            enforcement={"quality_gate_tier": "C2", "escalation_path": "orchestrator"}
        )

        # Act
        result = builder.build(agent)

        # Assert
        assert "## Enforcement" in result
        assert "quality_gate_tier" in result
        assert "C2" in result


class TestBuildPortabilitySection:
    """Tests for portability governance section."""

    def test_build_portability_section_when_portability_present_then_heading_with_content(
        self, make_canonical_agent: Any
    ) -> None:
        # Arrange
        builder = GovernanceSectionBuilder()
        agent = make_canonical_agent(
            portability={
                "enabled": True,
                "minimum_context_window": 128000,
            }
        )

        # Act
        result = builder.build(agent)

        # Assert
        assert "## Portability" in result
        assert "128000" in result


class TestBuildPriorArtSection:
    """Tests for prior art governance section."""

    def test_build_prior_art_section_when_citations_present_then_heading_with_list(
        self, make_canonical_agent: Any
    ) -> None:
        # Arrange
        builder = GovernanceSectionBuilder()
        agent = make_canonical_agent(prior_art=["ADR-PROJ007-001", "Phase 3 Synthesis"])

        # Act
        result = builder.build(agent)

        # Assert
        assert "## Prior Art" in result
        assert "ADR-PROJ007-001" in result
        assert "Phase 3 Synthesis" in result


class TestBuildSessionContextSection:
    """Tests for session context governance section."""

    def test_build_session_context_section_when_context_present_then_heading_with_content(
        self, make_canonical_agent: Any
    ) -> None:
        # Arrange
        builder = GovernanceSectionBuilder()
        agent = make_canonical_agent(
            session_context={
                "on_receive": ["validate handoff schema"],
                "on_send": ["attach key_findings"],
            }
        )

        # Act
        result = builder.build(agent)

        # Assert
        assert "## Session Context" in result
        assert "on_receive" in result


class TestBuildAll:
    """Tests for build() with multiple fields."""

    def test_build_all_when_all_fields_present_then_all_sections_generated(
        self, make_canonical_agent: Any
    ) -> None:
        # Arrange
        builder = GovernanceSectionBuilder()
        agent = make_canonical_agent(
            version="1.2.0",
            tool_tier=ToolTier.T2,
            enforcement={"quality_gate_tier": "C2"},
            portability={"enabled": True},
            prior_art=["ADR-001"],
            session_context={"on_receive": ["validate"]},
        )

        # Act
        result = builder.build(agent)

        # Assert
        assert "## Agent Version" in result
        assert "## Tool Tier" in result
        assert "## Enforcement" in result
        assert "## Portability" in result
        assert "## Prior Art" in result
        assert "## Session Context" in result

    def test_build_all_when_empty_fields_then_no_sections_generated(
        self, make_canonical_agent: Any
    ) -> None:
        # Arrange
        builder = GovernanceSectionBuilder()
        agent = make_canonical_agent(
            enforcement={},
            portability={},
            prior_art=[],
            session_context={},
        )

        # Act
        result = builder.build(agent)

        # Assert — only version and tool_tier are always present (non-empty)
        assert "## Enforcement" not in result
        assert "## Portability" not in result
        assert "## Prior Art" not in result
        assert "## Session Context" not in result


class TestBuildWithExistingBody:
    """Tests for duplicate heading prevention."""

    def test_sections_appended_after_existing_body_content(self, make_canonical_agent: Any) -> None:
        # Arrange
        builder = GovernanceSectionBuilder()
        agent = make_canonical_agent(
            version="1.0.0",
            enforcement={"quality_gate_tier": "C2"},
        )
        existing_body = "## Identity\n\nI am an agent.\n\n## Purpose\n\nTo serve.\n"

        # Act
        result = builder.build(agent, existing_body=existing_body)

        # Assert — governance sections present and after existing body
        assert "## Enforcement" in result
        assert result.index("## Enforcement") > 0

    def test_existing_enforcement_heading_not_duplicated(self, make_canonical_agent: Any) -> None:
        # Arrange
        builder = GovernanceSectionBuilder()
        agent = make_canonical_agent(
            enforcement={"quality_gate_tier": "C2"},
        )
        existing_body = "## Enforcement\n\nExisting enforcement content.\n"

        # Act
        result = builder.build(agent, existing_body=existing_body)

        # Assert — no duplicate Enforcement heading
        assert result.count("## Enforcement") == 0

    def test_existing_session_context_heading_not_duplicated(
        self, make_canonical_agent: Any
    ) -> None:
        # Arrange
        builder = GovernanceSectionBuilder()
        agent = make_canonical_agent(
            session_context={"on_receive": ["validate"]},
        )
        existing_body = "## Session Context\n\nAlready present.\n"

        # Act
        result = builder.build(agent, existing_body=existing_body)

        # Assert
        assert result.count("## Session Context") == 0

    def test_build_skips_section_when_heading_exists_case_insensitive(
        self, make_canonical_agent: Any
    ) -> None:
        """Heading dedup should be case-insensitive."""
        # Arrange
        builder = GovernanceSectionBuilder()
        agent = make_canonical_agent(
            version="2.0.0",
            tool_tier=ToolTier.T3,
        )
        body_with_uppercase = "## AGENT VERSION\n\n2.0.0\n\n## TOOL TIER\n\nT3\n"

        # Act
        result = builder.build(agent, existing_body=body_with_uppercase)

        # Assert
        assert "## Agent Version" not in result
        assert "## Tool Tier" not in result
