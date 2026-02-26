# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ComposeAgentsCommandHandler - Composes agent files with defaults.

Generates vendor-specific agent files from canonical source, then
deep-merges with base defaults to produce fully composed output.
Writes to the same skill-scoped paths as build (skills/{skill}/agents/).

Flow:
  1. repository.get(name) or list_all() -> CanonicalAgent(s)
  2. vendor_adapter.generate(agent) -> GeneratedArtifact (.md + .governance)
  3. Parse frontmatter from generated .md artifact content
  4. Parse governance from generated .governance.yaml artifact content
  5. Include agent.extra_yaml fields (maxTurns, skills, hooks, memory, isolation)
  6. Merge: defaults_composer.compose(defaults, frontmatter + governance + extra_yaml)
  7. Write composed .md to artifact.path (skills/{skill}/agents/{agent}.md)

References:
    - PROJ-012: Agent Configuration Extraction & Schema Enforcement
    - ADR-PROJ010-003: LLM Portability Architecture
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import TYPE_CHECKING, Any

import yaml

from src.agents.application.commands.compose_agents_command import (
    ComposeAgentsCommand,
)
from src.agents.application.handlers.commands.compose_result import ComposeResult
from src.agents.domain.services.defaults_composer import DefaultsComposer

if TYPE_CHECKING:
    from src.agents.application.ports.agent_repository import IAgentRepository
    from src.agents.application.ports.vendor_adapter import IVendorAdapter
    from src.agents.domain.entities.canonical_agent import CanonicalAgent


class ComposeAgentsCommandHandler:
    """Handler for ComposeAgentsCommand.

    Reads canonical agents, generates vendor-specific output in-memory,
    merges with defaults, and writes composed files to skill agent directories.

    Attributes:
        _repository: Repository for reading canonical agent source.
        _adapters: Map of vendor name -> adapter instance.
        _defaults_composer: Domain service for merging defaults.
        _defaults: Base defaults dictionary.
        _config_var_resolver: Callable for ${jerry.*} variable resolution.
    """

    def __init__(
        self,
        repository: IAgentRepository,
        adapters: dict[str, IVendorAdapter],
        defaults_composer: DefaultsComposer,
        defaults: dict[str, Any],
        config_var_resolver: Callable[[str], str | None] | None = None,
    ) -> None:
        """Initialize with dependencies.

        Args:
            repository: Repository for reading canonical agents.
            adapters: Map of vendor name -> adapter instance.
            defaults_composer: Domain service for defaults merging.
            defaults: Base defaults dictionary.
            config_var_resolver: Optional resolver for ${jerry.*} variables.
        """
        self._repository = repository
        self._adapters = adapters
        self._defaults_composer = defaults_composer
        self._defaults = defaults
        self._config_var_resolver = config_var_resolver

    def handle(self, command: ComposeAgentsCommand) -> ComposeResult:
        """Handle the ComposeAgentsCommand.

        Args:
            command: Compose command with vendor, optional agent filter.

        Returns:
            ComposeResult with counts and output paths.

        Raises:
            ValueError: If the specified vendor adapter is not available.
        """
        adapter = self._adapters.get(command.vendor)
        if adapter is None:
            available = ", ".join(sorted(self._adapters.keys()))
            raise ValueError(f"Unknown vendor: {command.vendor!r}. Available: {available}")

        # Get agents to compose
        if command.agent_name:
            agent = self._repository.get(command.agent_name)
            if agent is None:
                return ComposeResult(
                    errors=[f"Agent not found: {command.agent_name}"],
                    failed=1,
                    dry_run=command.dry_run,
                )
            agents = [agent]
        else:
            agents = self._repository.list_all()

        # Clean existing agent .md files if requested
        if command.clean and not command.dry_run:
            for agent in agents:
                artifacts = adapter.generate(agent)
                for artifact in artifacts:
                    if artifact.path.exists():
                        artifact.path.unlink()

        result = ComposeResult(dry_run=command.dry_run)

        for agent in agents:
            try:
                composed_content, output_path = self._compose_agent(agent, adapter)

                if not command.dry_run:
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    output_path.write_text(composed_content, encoding="utf-8")

                result.output_paths.append(str(output_path))
                result.composed += 1
            except Exception as e:
                result.errors.append(f"{agent.name}: {e}")
                result.failed += 1

        return result

    def _compose_agent(self, agent: CanonicalAgent, adapter: IVendorAdapter) -> tuple[str, Path]:
        """Compose a single agent: generate, parse, merge defaults, serialize.

        Args:
            agent: Canonical agent entity.
            adapter: Vendor adapter for generating base output.

        Returns:
            Tuple of (composed .md content, output Path).
        """
        # 1. Generate vendor-specific artifacts in-memory
        artifacts = adapter.generate(agent)

        # 2. Find the .md artifact and use its path as output location
        md_artifact = next(a for a in artifacts if a.artifact_type == "agent_definition")
        output_path = md_artifact.path

        # 3. Parse frontmatter from the .md artifact
        frontmatter, body = self._parse_md(md_artifact.content)

        # 4. Parse governance from the .governance.yaml artifact
        gov_artifact = next((a for a in artifacts if a.artifact_type == "governance"), None)
        gov_data: dict[str, Any] = {}
        if gov_artifact:
            gov_data = yaml.safe_load(gov_artifact.content) or {}

        # 5. Build per-agent config: frontmatter + governance + extra_yaml
        agent_config = dict(frontmatter)
        for key, value in gov_data.items():
            if key not in agent_config:
                agent_config[key] = value

        # 6. Include extra_yaml fields (maxTurns, skills, hooks, memory, isolation, etc.)
        for key, value in agent.extra_yaml.items():
            if key not in agent_config:
                agent_config[key] = value

        # 7. Merge with defaults
        composed = self._defaults_composer.compose(
            self._defaults,
            agent_config,
            self._config_var_resolver,
        )

        # 8. Serialize back to YAML frontmatter + body
        yaml_str = yaml.dump(
            composed,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
            width=200,
        )
        return f"---\n{yaml_str}---\n{body}", output_path

    @staticmethod
    def _parse_md(content: str) -> tuple[dict[str, Any], str]:
        """Parse an .md file into frontmatter dict and body string.

        Args:
            content: Full .md file content.

        Returns:
            Tuple of (frontmatter_dict, body_string).
        """
        if not content.startswith("---"):
            return {}, content

        end = content.find("---", 3)
        if end == -1:
            return {}, content

        fm_text = content[3:end].strip()
        body = content[end + 3 :].lstrip("\n")

        try:
            fm_data = yaml.safe_load(fm_text) or {}
        except yaml.YAMLError:
            fm_data = {}

        return fm_data, body
