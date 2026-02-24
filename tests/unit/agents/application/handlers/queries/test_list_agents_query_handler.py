# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for ListAgentsQueryHandler."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

from src.agents.application.handlers.queries.list_agents_query_handler import (
    ListAgentsQueryHandler,
)
from src.agents.application.queries.list_agents_query import ListAgentsQuery
from src.agents.domain.value_objects.model_tier import ModelTier
from src.agents.domain.value_objects.tool_tier import ToolTier

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_handler(
    agents: list[Any],
    skill_agents: list[Any] | None = None,
) -> tuple[ListAgentsQueryHandler, MagicMock]:
    """Build handler with mocked repository."""
    mock_repo = MagicMock()
    mock_repo.list_all.return_value = agents
    mock_repo.list_by_skill.return_value = skill_agents if skill_agents is not None else agents

    handler = ListAgentsQueryHandler(repository=mock_repo)
    return handler, mock_repo


# ---------------------------------------------------------------------------
# handle() — list all agents
# ---------------------------------------------------------------------------


class TestHandleListAll:
    """Tests for ListAgentsQueryHandler.handle() without skill filter."""

    def test_list_all_returns_summaries_for_all_agents(self, make_canonical_agent: Any) -> None:
        # Arrange
        agents = [make_canonical_agent(name=f"agent-{i}", skill="skill") for i in range(3)]
        handler, mock_repo = _make_handler(agents)
        query = ListAgentsQuery()

        # Act
        result = handler.handle(query)

        # Assert
        assert result.total == 3
        assert len(result.agents) == 3
        mock_repo.list_all.assert_called_once()
        mock_repo.list_by_skill.assert_not_called()

    def test_list_all_empty_returns_zero_total(self) -> None:
        # Arrange
        handler, _ = _make_handler([])
        query = ListAgentsQuery()

        # Act
        result = handler.handle(query)

        # Assert
        assert result.total == 0
        assert result.agents == []

    def test_summary_fields_populated_correctly(self, make_canonical_agent: Any) -> None:
        # Arrange
        agent = make_canonical_agent(
            name="ps-analyst",
            skill="problem-solving",
            description="Short description",
            model_tier=ModelTier.REASONING_HIGH,
        )
        handler, _ = _make_handler([agent])
        query = ListAgentsQuery()

        # Act
        result = handler.handle(query)

        # Assert — check all summary fields
        summary = result.agents[0]
        assert summary.name == "ps-analyst"
        assert summary.skill == "problem-solving"
        assert summary.version == agent.version
        assert summary.tool_tier == ToolTier.T2.value  # default from conftest
        assert summary.model_tier == ModelTier.REASONING_HIGH.value
        assert summary.cognitive_mode == agent.cognitive_mode

    def test_total_matches_agents_list_length(self, make_canonical_agent: Any) -> None:
        # Arrange
        agents = [make_canonical_agent(name=f"agent-{i}") for i in range(5)]
        handler, _ = _make_handler(agents)
        query = ListAgentsQuery()

        # Act
        result = handler.handle(query)

        # Assert
        assert result.total == len(result.agents)


# ---------------------------------------------------------------------------
# handle() — filter by skill
# ---------------------------------------------------------------------------


class TestHandleFilterBySkill:
    """Tests for ListAgentsQueryHandler.handle() with skill filter."""

    def test_list_by_skill_calls_repository_method(self, make_canonical_agent: Any) -> None:
        # Arrange
        agents = [make_canonical_agent(name="ps-analyst", skill="problem-solving")]
        handler, mock_repo = _make_handler([], skill_agents=agents)
        query = ListAgentsQuery(skill="problem-solving")

        # Act
        handler.handle(query)

        # Assert
        mock_repo.list_by_skill.assert_called_once_with("problem-solving")
        mock_repo.list_all.assert_not_called()

    def test_list_by_skill_returns_only_matching_agents(self, make_canonical_agent: Any) -> None:
        # Arrange
        skill_agents = [
            make_canonical_agent(name="ps-analyst", skill="problem-solving"),
            make_canonical_agent(name="ps-critic", skill="problem-solving"),
        ]
        handler, _ = _make_handler([], skill_agents=skill_agents)
        query = ListAgentsQuery(skill="problem-solving")

        # Act
        result = handler.handle(query)

        # Assert
        assert result.total == 2
        assert all(s.skill == "problem-solving" for s in result.agents)

    def test_list_by_unknown_skill_returns_empty(self) -> None:
        # Arrange — repository returns empty for unknown skill
        handler, _ = _make_handler([], skill_agents=[])
        query = ListAgentsQuery(skill="ghost-skill")

        # Act
        result = handler.handle(query)

        # Assert
        assert result.total == 0
        assert result.agents == []


# ---------------------------------------------------------------------------
# handle() — description truncation
# ---------------------------------------------------------------------------


class TestHandleDescriptionTruncation:
    """Tests for description truncation at 80 characters."""

    def test_description_shorter_than_80_not_truncated(self, make_canonical_agent: Any) -> None:
        # Arrange
        short_desc = "A short description."
        assert len(short_desc) <= 80
        agent = make_canonical_agent(description=short_desc)
        handler, _ = _make_handler([agent])
        query = ListAgentsQuery()

        # Act
        result = handler.handle(query)

        # Assert
        assert result.agents[0].description == short_desc
        assert not result.agents[0].description.endswith("...")

    def test_description_exactly_80_chars_not_truncated(self, make_canonical_agent: Any) -> None:
        # Arrange — exactly 80 characters
        exact_desc = "x" * 80
        assert len(exact_desc) == 80
        agent = make_canonical_agent(description=exact_desc)
        handler, _ = _make_handler([agent])
        query = ListAgentsQuery()

        # Act
        result = handler.handle(query)

        # Assert — 80 is NOT > 80, so no truncation
        assert result.agents[0].description == exact_desc

    def test_description_over_80_chars_truncated_with_ellipsis(
        self, make_canonical_agent: Any
    ) -> None:
        # Arrange — 100 characters, longer than 80
        long_desc = "A" * 100
        assert len(long_desc) > 80
        agent = make_canonical_agent(description=long_desc)
        handler, _ = _make_handler([agent])
        query = ListAgentsQuery()

        # Act
        result = handler.handle(query)

        # Assert — truncated to first 80 chars + "..."
        summary_desc = result.agents[0].description
        assert summary_desc.endswith("...")
        assert summary_desc == long_desc[:80] + "..."

    def test_description_81_chars_triggers_truncation(self, make_canonical_agent: Any) -> None:
        # Arrange — 81 characters (boundary case: > 80)
        boundary_desc = "B" * 81
        agent = make_canonical_agent(description=boundary_desc)
        handler, _ = _make_handler([agent])
        query = ListAgentsQuery()

        # Act
        result = handler.handle(query)

        # Assert
        assert result.agents[0].description.endswith("...")

    def test_multiple_agents_each_truncated_independently(self, make_canonical_agent: Any) -> None:
        # Arrange
        agents = [
            make_canonical_agent(name="agent-short", description="Short."),
            make_canonical_agent(name="agent-long", description="L" * 200),
        ]
        handler, _ = _make_handler(agents)
        query = ListAgentsQuery()

        # Act
        result = handler.handle(query)

        # Assert — short one preserved, long one truncated
        by_name = {s.name: s for s in result.agents}
        assert not by_name["agent-short"].description.endswith("...")
        assert by_name["agent-long"].description.endswith("...")
