# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Agent Configuration Query Handlers.

Thin handlers that delegate to AgentConfigResolver.
No business logic in handlers - orchestration only.

References:
    - PROJ-012: Agent Configuration Extraction & Schema Enforcement
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from src.application.queries.agent_config_queries import (
    ListAgentConfigsQuery,
    ShowAgentConfigQuery,
    ValidateAgentConfigQuery,
)

if TYPE_CHECKING:
    from src.infrastructure.adapters.configuration.agent_config_resolver import (
        AgentConfigResolver,
        AgentInfo,
        ValidationResult,
    )


class ValidateAgentConfigQueryHandler:
    """Handler for ValidateAgentConfigQuery.

    Validates one or all agents against the JSON Schema.

    Attributes:
        _resolver: AgentConfigResolver for composition and validation.
    """

    def __init__(self, resolver: AgentConfigResolver) -> None:
        """Initialize the handler.

        Args:
            resolver: AgentConfigResolver instance.
        """
        self._resolver = resolver

    def handle(self, query: ValidateAgentConfigQuery) -> list[ValidationResult]:
        """Handle the validation query.

        Args:
            query: Query with paths and optional agent name.

        Returns:
            List of ValidationResult (one per agent, or one if agent_name specified).
        """
        if query.agent_name is not None:
            return self._resolver.validate_single(
                query.skills_dir,
                query.agent_name,
                query.schema_path,
                query.defaults_path,
            )

        return self._resolver.validate_all(query.skills_dir, query.schema_path, query.defaults_path)


class ListAgentConfigsQueryHandler:
    """Handler for ListAgentConfigsQuery.

    Lists all discovered agents with summary info.

    Attributes:
        _resolver: AgentConfigResolver for agent discovery.
    """

    def __init__(self, resolver: AgentConfigResolver) -> None:
        """Initialize the handler.

        Args:
            resolver: AgentConfigResolver instance.
        """
        self._resolver = resolver

    def handle(self, query: ListAgentConfigsQuery) -> list[AgentInfo]:
        """Handle the list query.

        Args:
            query: Query with skills_dir and optional skill filter.

        Returns:
            List of AgentInfo objects.
        """
        agents = self._resolver.discover_agents(query.skills_dir)
        if query.skill_filter:
            agents = [a for a in agents if a.skill == query.skill_filter]
        return agents


class ShowAgentConfigQueryHandler:
    """Handler for ShowAgentConfigQuery.

    Shows fully composed agent configuration.

    Attributes:
        _resolver: AgentConfigResolver for composition.
    """

    def __init__(self, resolver: AgentConfigResolver) -> None:
        """Initialize the handler.

        Args:
            resolver: AgentConfigResolver instance.
        """
        self._resolver = resolver

    def handle(self, query: ShowAgentConfigQuery) -> dict[str, Any]:
        """Handle the show query.

        Args:
            query: Query with agent name and paths.

        Returns:
            Dict with composed config or error.
        """
        agent_file = self._resolver.find_agent_file(query.skills_dir, query.agent_name)
        if agent_file is None:
            return {"error": f"Agent '{query.agent_name}' not found"}

        if query.raw:
            frontmatter = self._resolver._extract_frontmatter(agent_file)
            if frontmatter is None:
                return {"error": f"No YAML frontmatter in {agent_file}"}
            return frontmatter

        defaults = self._resolver.load_defaults(query.defaults_path)
        return self._resolver.compose_agent_config(agent_file, defaults)
