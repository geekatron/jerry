# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
BuildAgentsCommandHandler - Builds vendor-specific agent files from canonical source.

References:
    - ADR-PROJ010-003: LLM Portability Architecture
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.agents.application.commands.build_agents_command import BuildAgentsCommand
from src.agents.application.handlers.commands.build_result import BuildResult

if TYPE_CHECKING:
    from src.agents.application.ports.agent_repository import IAgentRepository
    from src.agents.application.ports.vendor_adapter import IVendorAdapter


class BuildAgentsCommandHandler:
    """Handler for BuildAgentsCommand.

    Reads canonical agent definitions and generates vendor-specific
    output files using the specified vendor adapter.

    Attributes:
        _repository: Repository for reading canonical agent source.
        _adapters: Map of vendor name -> adapter instance.
    """

    def __init__(
        self,
        repository: IAgentRepository,
        adapters: dict[str, IVendorAdapter],
    ) -> None:
        """Initialize with dependencies.

        Args:
            repository: Repository for reading canonical agents.
            adapters: Map of adapter name -> adapter instance.
        """
        self._repository = repository
        self._adapters = adapters

    def handle(self, command: BuildAgentsCommand) -> BuildResult:
        """Handle the BuildAgentsCommand.

        Args:
            command: Build command with adapter name and optional agent filter.

        Returns:
            BuildResult with counts and generated artifacts.

        Raises:
            ValueError: If the specified adapter is not available.
        """
        adapter = self._adapters.get(command.vendor)
        if adapter is None:
            available = ", ".join(sorted(self._adapters.keys()))
            raise ValueError(f"Unknown vendor: {command.vendor!r}. Available: {available}")

        # Get agents to build
        if command.agent_name:
            agent = self._repository.get(command.agent_name)
            if agent is None:
                return BuildResult(
                    errors=[f"Agent not found: {command.agent_name}"],
                    failed=1,
                    dry_run=command.dry_run,
                )
            agents = [agent]
        else:
            agents = self._repository.list_all()

        result = BuildResult(dry_run=command.dry_run)

        for agent in agents:
            try:
                artifacts = adapter.generate(agent)
                result.artifacts.extend(artifacts)

                if not command.dry_run:
                    for artifact in artifacts:
                        artifact.path.parent.mkdir(parents=True, exist_ok=True)
                        artifact.path.write_text(artifact.content, encoding="utf-8")

                result.built += 1
            except Exception as e:
                result.errors.append(f"{agent.name}: {e}")
                result.failed += 1

        return result
