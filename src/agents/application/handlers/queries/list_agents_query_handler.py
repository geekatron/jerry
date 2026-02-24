# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ListAgentsQueryHandler - Lists canonical agents with metadata.

References:
    - ADR-PROJ010-003: LLM Portability Architecture
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from src.agents.application.queries.list_agents_query import ListAgentsQuery

if TYPE_CHECKING:
    from src.agents.application.ports.agent_repository import IAgentRepository


@dataclass(frozen=True)
class AgentSummary:
    """Summary of a single agent for listing.

    Attributes:
        name: Agent identifier.
        skill: Parent skill name.
        version: Semantic version.
        tool_tier: Security tier.
        cognitive_mode: Reasoning mode.
        model_tier: Abstract model tier.
        description: Short description.
    """

    name: str
    skill: str
    version: str
    tool_tier: str
    cognitive_mode: str
    model_tier: str
    description: str


@dataclass
class ListAgentsResult:
    """Result of list agents query.

    Attributes:
        agents: List of agent summaries.
        total: Total count.
    """

    agents: list[AgentSummary] = field(default_factory=list)
    total: int = 0


class ListAgentsQueryHandler:
    """Handler for ListAgentsQuery.

    Attributes:
        _repository: Repository for reading canonical agents.
    """

    def __init__(self, repository: IAgentRepository) -> None:
        """Initialize with repository.

        Args:
            repository: Repository for reading canonical agents.
        """
        self._repository = repository

    def handle(self, query: ListAgentsQuery) -> ListAgentsResult:
        """Handle the ListAgentsQuery.

        Args:
            query: Query with optional skill filter.

        Returns:
            ListAgentsResult with agent summaries.
        """
        if query.skill:
            agents = self._repository.list_by_skill(query.skill)
        else:
            agents = self._repository.list_all()

        summaries = [
            AgentSummary(
                name=a.name,
                skill=a.skill,
                version=a.version,
                tool_tier=a.tool_tier.value,
                cognitive_mode=a.cognitive_mode,
                model_tier=a.model_tier.value,
                description=a.description[:80] + "..."
                if len(a.description) > 80
                else a.description,
            )
            for a in agents
        ]

        return ListAgentsResult(agents=summaries, total=len(summaries))
