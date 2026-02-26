# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ExtractCanonicalCommandHandler - Extracts canonical source from vendor files.

References:
    - ADR-PROJ010-003: LLM Portability Architecture
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

import yaml

from src.agents.application.commands.extract_canonical_command import (
    ExtractCanonicalCommand,
)
from src.agents.application.handlers.commands.extract_result import ExtractResult
from src.agents.domain.entities.canonical_agent import CanonicalAgent

if TYPE_CHECKING:
    from src.agents.application.ports.vendor_adapter import IVendorAdapter


class ExtractCanonicalCommandHandler:
    """Handler for ExtractCanonicalCommand.

    Reads existing vendor-specific agent files and produces canonical
    .agent.yaml + .prompt.md source files.

    Attributes:
        _adapters: Map of vendor name -> adapter instance.
        _skills_dir: Path to the skills/ directory.
    """

    def __init__(
        self,
        adapters: dict[str, IVendorAdapter],
        skills_dir: Path,
    ) -> None:
        """Initialize with dependencies.

        Args:
            adapters: Map of adapter name -> adapter instance.
            skills_dir: Path to skills/ directory.
        """
        self._adapters = adapters
        self._skills_dir = skills_dir

    def handle(self, command: ExtractCanonicalCommand) -> ExtractResult:
        """Handle the ExtractCanonicalCommand.

        Args:
            command: Extract command with optional agent filter.

        Returns:
            ExtractResult with counts.

        Raises:
            ValueError: If the specified adapter is not available.
        """
        adapter = self._adapters.get(command.source_vendor)
        if adapter is None:
            available = ", ".join(sorted(self._adapters.keys()))
            raise ValueError(f"Unknown vendor: {command.source_vendor!r}. Available: {available}")

        result = ExtractResult()

        # Find all existing agent files
        agent_files = self._find_agent_files(command.agent_name)

        for md_path, gov_path in agent_files:
            try:
                canonical = adapter.extract(
                    agent_md_path=str(md_path),
                    governance_yaml_path=str(gov_path) if gov_path else None,
                )
                self._write_canonical(canonical)
                result.extracted += 1
            except Exception as e:
                result.errors.append(f"{md_path.stem}: {e}")
                result.failed += 1

        return result

    def _find_agent_files(
        self,
        agent_name: str | None = None,
    ) -> list[tuple[Path, Path | None]]:
        """Find existing vendor agent files.

        Args:
            agent_name: Optional specific agent name filter.

        Returns:
            List of (md_path, governance_yaml_path) tuples.
        """
        results: list[tuple[Path, Path | None]] = []

        for skill_dir in sorted(self._skills_dir.iterdir()):
            agents_dir = skill_dir / "agents"
            if not agents_dir.is_dir():
                continue

            for md_file in sorted(agents_dir.glob("*.md")):
                if agent_name and md_file.stem != agent_name:
                    continue

                gov_file = agents_dir / f"{md_file.stem}.governance.yaml"
                results.append((md_file, gov_file if gov_file.exists() else None))

        return results

    def _write_canonical(self, agent: CanonicalAgent) -> None:
        """Write canonical source files for an extracted agent.

        Args:
            agent: Extracted canonical agent entity.
        """
        composition_dir = self._skills_dir / agent.skill / "composition"
        composition_dir.mkdir(parents=True, exist_ok=True)

        # Write .agent.yaml
        yaml_data = self._build_yaml_data(agent)
        yaml_path = composition_dir / f"{agent.name}.agent.yaml"
        yaml_content = yaml.dump(
            yaml_data,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
            width=100,
        )
        yaml_path.write_text(
            f"# Canonical Agent Definition\n"
            f"# Schema: docs/schemas/agent-canonical-v1.schema.json\n\n"
            f"{yaml_content}",
            encoding="utf-8",
        )

        # Write .prompt.md
        prompt_path = composition_dir / f"{agent.name}.prompt.md"
        prompt_path.write_text(
            f"# {agent.name} System Prompt\n\n{agent.prompt_body}",
            encoding="utf-8",
        )

    def _build_yaml_data(self, agent: CanonicalAgent) -> dict[str, Any]:
        """Build the YAML dictionary for an .agent.yaml file.

        Args:
            agent: Canonical agent entity.

        Returns:
            Dictionary ready for YAML serialization.
        """
        data: dict[str, Any] = {
            "name": agent.name,
            "version": agent.version,
            "description": agent.description,
            "skill": agent.skill,
            "identity": agent.identity,
        }

        if agent.persona:
            data["persona"] = agent.persona

        model_data: dict[str, Any] = {"tier": agent.model_tier.value}
        if agent.model_preferences:
            model_data["preferences"] = agent.model_preferences
        data["model"] = model_data

        tools: dict[str, Any] = {"native": agent.native_tools}
        if agent.mcp_servers:
            tools["mcp"] = agent.mcp_servers
        if agent.forbidden_tools:
            tools["forbidden"] = agent.forbidden_tools
        data["tools"] = tools

        data["tool_tier"] = agent.tool_tier.value
        data["guardrails"] = agent.guardrails

        if agent.output:
            data["output"] = agent.output

        data["constitution"] = agent.constitution

        if agent.validation:
            data["validation"] = agent.validation

        if agent.portability:
            data["portability"] = agent.portability
        else:
            data["portability"] = {
                "enabled": True,
                "minimum_context_window": 128000,
                "reasoning_strategy": "adaptive",
                "body_format": agent.body_format.value,
            }

        if agent.enforcement:
            data["enforcement"] = agent.enforcement

        if agent.session_context:
            data["session_context"] = agent.session_context

        if agent.prior_art:
            data["prior_art"] = agent.prior_art

        # Include any extra fields
        data.update(agent.extra_yaml)

        return data
