# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ComposeAgentsCommandHandler - Composes agent files with defaults.

Generates vendor-specific agent files from canonical source, then
deep-merges with layered defaults to produce fully composed output.
Writes to the same skill-scoped paths as build (skills/{skill}/agents/).

4-layer merge order:
  1. Jerry governance defaults     (jerry-agent-defaults.yaml)
  2. Vendor defaults               (jerry-claude-code-defaults.yaml)
  3. Canonical agent config        (from .jerry.yaml via adapter + governance + extra_yaml)
  4. Per-agent vendor overrides    (skills/{skill}/composition/{agent}.claude-code.yaml)

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
    from src.agents.application.ports.vendor_override_provider import IVendorOverrideProvider
    from src.agents.domain.entities.canonical_agent import CanonicalAgent
    from src.agents.domain.value_objects.vendor_override_spec import VendorOverrideSpec


class ComposeAgentsCommandHandler:
    """Handler for ComposeAgentsCommand.

    Reads canonical agents, generates vendor-specific output in-memory,
    merges with layered defaults, and writes composed files to skill agent directories.

    Attributes:
        _repository: Repository for reading canonical agent source.
        _adapters: Map of vendor name -> adapter instance.
        _defaults_composer: Domain service for merging defaults.
        _governance_defaults: Layer 1: Jerry governance defaults.
        _vendor_defaults: Layer 2: Vendor-specific defaults.
        _vendor_override_provider: Provider for layer 4 per-agent vendor overrides.
        _vendor_override_spec: Allowlist spec for validating vendor overrides.
        _config_var_resolver: Callable for ${jerry.*} variable resolution.
    """

    def __init__(
        self,
        repository: IAgentRepository,
        adapters: dict[str, IVendorAdapter],
        defaults_composer: DefaultsComposer,
        governance_defaults: dict[str, Any],
        vendor_defaults: dict[str, Any] | None = None,
        vendor_override_provider: IVendorOverrideProvider | None = None,
        vendor_override_spec: VendorOverrideSpec | None = None,
        config_var_resolver: Callable[[str], str | None] | None = None,
    ) -> None:
        """Initialize with dependencies.

        Args:
            repository: Repository for reading canonical agents.
            adapters: Map of vendor name -> adapter instance.
            defaults_composer: Domain service for defaults merging.
            governance_defaults: Layer 1: Jerry governance defaults.
            vendor_defaults: Layer 2: Vendor-specific defaults (None = empty).
            vendor_override_provider: Provider for layer 4 overrides (None = no overrides).
            vendor_override_spec: Spec for validating vendor overrides (None = skip validation).
            config_var_resolver: Optional resolver for ${jerry.*} variables.
        """
        self._repository = repository
        self._adapters = adapters
        self._defaults_composer = defaults_composer
        self._governance_defaults = governance_defaults
        self._vendor_defaults = vendor_defaults or {}
        self._vendor_override_provider = vendor_override_provider
        self._vendor_override_spec = vendor_override_spec
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
                composed_content, output_path = self._compose_agent(agent, adapter, command.vendor)

                if not command.dry_run:
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    output_path.write_text(composed_content, encoding="utf-8")

                result.output_paths.append(str(output_path))
                result.composed += 1
            except Exception as e:
                result.errors.append(f"{agent.name}: {e}")
                result.failed += 1

        return result

    def _compose_agent(
        self, agent: CanonicalAgent, adapter: IVendorAdapter, vendor: str
    ) -> tuple[str, Path]:
        """Compose a single agent: generate, parse, merge 4 layers, serialize.

        Args:
            agent: Canonical agent entity.
            adapter: Vendor adapter for generating base output.
            vendor: Vendor identifier for override lookup.

        Returns:
            Tuple of (composed .md content, output Path).

        Raises:
            ValueError: If vendor overrides contain disallowed keys.
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

        # 5. Build per-agent config (Layer 3): frontmatter + governance + extra_yaml
        agent_config = dict(frontmatter)
        for key, value in gov_data.items():
            if key not in agent_config:
                agent_config[key] = value

        for key, value in agent.extra_yaml.items():
            if key not in agent_config:
                agent_config[key] = value

        # 6. Load per-agent vendor overrides (Layer 4)
        vendor_overrides: dict[str, Any] = {}
        if self._vendor_override_provider is not None:
            vendor_overrides = self._vendor_override_provider.get_overrides(
                agent_name=agent.name,
                skill=agent.skill,
                vendor=vendor,
            )

        # 7. Validate vendor overrides against allowlist
        if vendor_overrides and self._vendor_override_spec is not None:
            errors = self._vendor_override_spec.validate(vendor_overrides)
            if errors:
                raise ValueError(f"Invalid vendor overrides for {agent.name}: {'; '.join(errors)}")

        # 8. Merge all 4 layers
        composed = self._defaults_composer.compose_layered(
            governance_defaults=self._governance_defaults,
            vendor_defaults=self._vendor_defaults,
            agent_config=agent_config,
            vendor_overrides=vendor_overrides or None,
            resolver=self._config_var_resolver,
        )

        # 9. Filter to vendor-only fields (Claude Code official frontmatter)
        composed = self._filter_vendor_frontmatter(composed)

        # 10. Serialize back to YAML frontmatter + body
        yaml_str = yaml.dump(
            composed,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
            width=200,
        )
        return f"---\n{yaml_str}---\n{body}", output_path

    # Claude Code's 12 official frontmatter fields, in documentation order.
    _VENDOR_FIELDS: tuple[str, ...] = (
        "name",
        "description",
        "model",
        "tools",
        "disallowedTools",
        "mcpServers",
        "permissionMode",
        "maxTurns",
        "skills",
        "hooks",
        "memory",
        "background",
        "isolation",
    )

    @staticmethod
    def _filter_vendor_frontmatter(composed: dict[str, Any]) -> dict[str, Any]:
        """Filter composed dict to only Claude Code official frontmatter fields.

        Governance fields (version, persona, guardrails, constitution, etc.) are
        stripped — they belong in .governance.yaml and the prompt body, not in
        frontmatter that Claude Code silently discards.

        Args:
            composed: Fully merged configuration dict.

        Returns:
            New dict with only Claude Code official fields, in documentation order.
        """
        return {
            key: composed[key]
            for key in ComposeAgentsCommandHandler._VENDOR_FIELDS
            if key in composed
        }

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
