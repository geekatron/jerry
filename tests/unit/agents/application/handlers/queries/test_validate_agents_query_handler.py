# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for ValidateAgentsQueryHandler."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

from src.agents.application.handlers.queries.validate_agents_query_handler import (
    ValidateAgentsQueryHandler,
)
from src.agents.application.queries.validate_agents_query import ValidateAgentsQuery
from src.agents.domain.value_objects.tool_tier import ToolTier

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_handler(
    agents: list[Any],
    single_agent: Any | None = None,
    schema_path: Path | None = None,
) -> tuple[ValidateAgentsQueryHandler, MagicMock]:
    """Build handler with mocked repository."""
    mock_repo = MagicMock()
    mock_repo.list_all.return_value = agents
    mock_repo.get.return_value = single_agent

    handler = ValidateAgentsQueryHandler(
        repository=mock_repo,
        schema_path=schema_path or Path("/dev/null"),
    )
    return handler, mock_repo


# ---------------------------------------------------------------------------
# handle() — all-agent queries
# ---------------------------------------------------------------------------


class TestHandleAllAgents:
    """Tests for ValidateAgentsQueryHandler.handle() without agent filter."""

    def test_all_pass_returns_valid_result(self, make_canonical_agent: Any) -> None:
        # Arrange — two fully-compliant agents
        agents = [make_canonical_agent(name=f"agent-{i}", skill="skill") for i in range(2)]
        handler, _ = _make_handler(agents)
        query = ValidateAgentsQuery()

        # Act
        result = handler.handle(query)

        # Assert
        assert result.is_valid
        assert result.total == 2
        assert result.passed == 2
        assert result.failed == 0
        assert result.issues == []

    def test_some_fail_returns_invalid_result(self, make_canonical_agent: Any) -> None:
        # Arrange — one valid, one invalid (missing constitution)
        valid_agent = make_canonical_agent(name="good-agent")
        bad_agent = make_canonical_agent(
            name="bad-agent",
            constitution={
                "principles_applied": [],  # missing all three principles
                "forbidden_actions": [],
            },
        )
        handler, _ = _make_handler([valid_agent, bad_agent])
        query = ValidateAgentsQuery()

        # Act
        result = handler.handle(query)

        # Assert
        assert not result.is_valid
        assert result.total == 2
        assert result.passed == 1
        assert result.failed == 1
        assert len(result.issues) > 0

    def test_empty_repository_returns_valid_with_zero_counts(self) -> None:
        # Arrange — no agents
        handler, _ = _make_handler([])
        query = ValidateAgentsQuery()

        # Act
        result = handler.handle(query)

        # Assert
        assert result.is_valid
        assert result.total == 0
        assert result.passed == 0
        assert result.failed == 0


# ---------------------------------------------------------------------------
# handle() — specific agent filter
# ---------------------------------------------------------------------------


class TestHandleSpecificAgent:
    """Tests for ValidateAgentsQueryHandler.handle() with agent_name filter."""

    def test_specific_agent_found_and_validated(self, make_canonical_agent: Any) -> None:
        # Arrange
        agent = make_canonical_agent(name="ps-analyst")
        handler, mock_repo = _make_handler([], single_agent=agent)
        query = ValidateAgentsQuery(agent_name="ps-analyst")

        # Act
        result = handler.handle(query)

        # Assert
        assert result.total == 1
        mock_repo.get.assert_called_once_with("ps-analyst")

    def test_specific_agent_not_found_returns_empty_result(self) -> None:
        # Arrange — repo.get() returns None
        handler, _ = _make_handler([], single_agent=None)
        query = ValidateAgentsQuery(agent_name="ghost-agent")

        # Act
        result = handler.handle(query)

        # Assert
        assert result.total == 0
        assert result.is_valid


# ---------------------------------------------------------------------------
# _validate_agent() — constitution checks
# ---------------------------------------------------------------------------


class TestValidateAgentConstitutionChecks:
    """Tests for the constitutional triplet validation in _validate_agent()."""

    def test_missing_p003_in_principles_produces_issue(self, make_canonical_agent: Any) -> None:
        # Arrange
        agent = make_canonical_agent(
            constitution={
                "principles_applied": [
                    "P-020: User Authority (Hard)",
                    "P-022: No Deception (Hard)",
                ],
                "forbidden_actions": [
                    "Spawn recursive subagents (P-003)",
                    "Override user decisions (P-020)",
                    "Misrepresent capabilities or confidence (P-022)",
                ],
            }
        )
        handler, _ = _make_handler([])

        # Act
        issues = handler._validate_agent(agent)

        # Assert
        principle_issues = [i for i in issues if "P-003" in i.message and "principles" in i.field]
        assert len(principle_issues) == 1

    def test_missing_p020_in_forbidden_actions_produces_issue(
        self, make_canonical_agent: Any
    ) -> None:
        # Arrange
        agent = make_canonical_agent(
            constitution={
                "principles_applied": [
                    "P-003: No Recursive Subagents (Hard)",
                    "P-020: User Authority (Hard)",
                    "P-022: No Deception (Hard)",
                ],
                "forbidden_actions": [
                    "Spawn recursive subagents (P-003)",
                    # P-020 missing from forbidden_actions
                    "Misrepresent capabilities or confidence (P-022)",
                ],
            }
        )
        handler, _ = _make_handler([])

        # Act
        issues = handler._validate_agent(agent)

        # Assert
        action_issues = [i for i in issues if "P-020" in i.message and "forbidden" in i.field]
        assert len(action_issues) == 1

    def test_all_three_present_produces_no_constitution_issues(
        self, make_canonical_agent: Any, sample_constitution: dict[str, Any]
    ) -> None:
        # Arrange — full constitution with all three entries
        agent = make_canonical_agent(constitution=sample_constitution)
        handler, _ = _make_handler([])

        # Act
        issues = handler._validate_agent(agent)

        # Assert — no constitution-related issues
        constitution_issues = [i for i in issues if "constitution" in i.field]
        assert constitution_issues == []


# ---------------------------------------------------------------------------
# _validate_agent() — delegate tool on non-T5
# ---------------------------------------------------------------------------


class TestValidateAgentDelegateTool:
    """Tests for the agent_delegate restriction check in _validate_agent()."""

    def test_non_t5_with_agent_delegate_produces_issue(
        self, make_canonical_agent: Any, sample_constitution: dict[str, Any]
    ) -> None:
        # Arrange — T2 agent with agent_delegate in native_tools
        agent = make_canonical_agent(
            tool_tier=ToolTier.T2,
            native_tools=["file_read", "agent_delegate"],
            constitution=sample_constitution,
        )
        handler, _ = _make_handler([])

        # Act
        issues = handler._validate_agent(agent)

        # Assert
        delegate_issues = [i for i in issues if "agent_delegate" in i.message]
        assert len(delegate_issues) == 1
        assert "P-003" in delegate_issues[0].message

    def test_t5_with_agent_delegate_produces_no_delegate_issue(
        self, make_canonical_agent: Any, sample_constitution: dict[str, Any]
    ) -> None:
        # Arrange — T5 agent with agent_delegate is valid
        agent = make_canonical_agent(
            tool_tier=ToolTier.T5,
            native_tools=["file_read", "agent_delegate"],
            constitution=sample_constitution,
        )
        handler, _ = _make_handler([])

        # Act
        issues = handler._validate_agent(agent)

        # Assert — no issue about agent_delegate for T5
        delegate_issues = [i for i in issues if "agent_delegate" in i.message]
        assert delegate_issues == []

    def test_non_t5_without_agent_delegate_produces_no_delegate_issue(
        self, make_canonical_agent: Any, sample_constitution: dict[str, Any]
    ) -> None:
        # Arrange — T2 agent without agent_delegate
        agent = make_canonical_agent(
            tool_tier=ToolTier.T2,
            native_tools=["file_read", "file_write"],
            constitution=sample_constitution,
        )
        handler, _ = _make_handler([])

        # Act
        issues = handler._validate_agent(agent)

        # Assert
        delegate_issues = [i for i in issues if "agent_delegate" in i.message]
        assert delegate_issues == []


# ---------------------------------------------------------------------------
# _validate_agent() — expertise minimum
# ---------------------------------------------------------------------------


class TestValidateAgentExpertise:
    """Tests for the expertise minimum check in _validate_agent()."""

    def test_insufficient_expertise_produces_issue(
        self, make_canonical_agent: Any, sample_constitution: dict[str, Any]
    ) -> None:
        # Arrange — only one expertise entry (minimum is 2)
        agent = make_canonical_agent(
            identity={
                "role": "Minimalist",
                "expertise": ["single-expertise"],
                "cognitive_mode": "convergent",
            },
            constitution=sample_constitution,
        )
        handler, _ = _make_handler([])

        # Act
        issues = handler._validate_agent(agent)

        # Assert
        expertise_issues = [i for i in issues if "expertise" in i.field]
        assert len(expertise_issues) == 1
        assert "2" in expertise_issues[0].message

    def test_zero_expertise_produces_issue(
        self, make_canonical_agent: Any, sample_constitution: dict[str, Any]
    ) -> None:
        # Arrange
        agent = make_canonical_agent(
            identity={
                "role": "Empty",
                "expertise": [],
                "cognitive_mode": "convergent",
            },
            constitution=sample_constitution,
        )
        handler, _ = _make_handler([])

        # Act
        issues = handler._validate_agent(agent)

        # Assert
        expertise_issues = [i for i in issues if "expertise" in i.field]
        assert len(expertise_issues) == 1

    def test_two_or_more_expertise_entries_produces_no_issue(
        self, make_canonical_agent: Any, sample_constitution: dict[str, Any]
    ) -> None:
        # Arrange — exactly two expertise entries (the minimum)
        agent = make_canonical_agent(
            identity={
                "role": "Specialist",
                "expertise": ["skill-a", "skill-b"],
                "cognitive_mode": "convergent",
            },
            constitution=sample_constitution,
        )
        handler, _ = _make_handler([])

        # Act
        issues = handler._validate_agent(agent)

        # Assert
        expertise_issues = [i for i in issues if "expertise" in i.field]
        assert expertise_issues == []

    def test_compliant_agent_produces_no_issues(
        self, make_canonical_agent: Any, sample_constitution: dict[str, Any]
    ) -> None:
        # Arrange — fully compliant agent
        agent = make_canonical_agent(constitution=sample_constitution)
        handler, _ = _make_handler([])

        # Act
        issues = handler._validate_agent(agent)

        # Assert
        assert issues == []
