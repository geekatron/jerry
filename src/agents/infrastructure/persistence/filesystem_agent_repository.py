# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
FilesystemAgentRepository - Reads canonical agent files from the filesystem.

Reads .jerry.yaml + .jerry.prompt.md pairs from skills/*/composition/ directories.

References:
    - ADR-PROJ010-003: LLM Portability Architecture
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from src.agents.application.ports.agent_repository import IAgentRepository
from src.agents.domain.entities.canonical_agent import CanonicalAgent
from src.agents.domain.value_objects.body_format import BodyFormat
from src.agents.domain.value_objects.model_tier import ModelTier
from src.agents.domain.value_objects.tool_tier import ToolTier


class FilesystemAgentRepository(IAgentRepository):
    """Reads canonical agent definitions from the filesystem.

    Scans skills/*/composition/ for .jerry.yaml + .jerry.prompt.md pairs.

    Attributes:
        _skills_dir: Path to the skills/ directory.
    """

    def __init__(self, skills_dir: Path) -> None:
        """Initialize with skills directory path.

        Args:
            skills_dir: Path to skills/ directory.
        """
        self._skills_dir = skills_dir

    def get(self, agent_name: str) -> CanonicalAgent | None:
        """Retrieve a single canonical agent by name.

        Args:
            agent_name: Agent identifier (e.g., 'ps-architect').

        Returns:
            Parsed CanonicalAgent, or None if not found.
        """
        for skill_dir in self._skills_dir.iterdir():
            comp_dir = skill_dir / "composition"
            if not comp_dir.is_dir():
                continue

            yaml_path = comp_dir / f"{agent_name}.jerry.yaml"
            if yaml_path.exists():
                return self._load_agent(yaml_path)

        return None

    def list_all(self) -> list[CanonicalAgent]:
        """List all canonical agents across all skills.

        Returns:
            List of all parsed CanonicalAgent entities.
        """
        agents: list[CanonicalAgent] = []
        for skill_dir in sorted(self._skills_dir.iterdir()):
            if not skill_dir.is_dir():
                continue
            agents.extend(self.list_by_skill(skill_dir.name))
        return agents

    def list_by_skill(self, skill: str) -> list[CanonicalAgent]:
        """List canonical agents for a specific skill.

        Args:
            skill: Skill directory name (e.g., 'problem-solving').

        Returns:
            List of parsed CanonicalAgent entities for the skill.
        """
        comp_dir = self._skills_dir / skill / "composition"
        if not comp_dir.is_dir():
            return []

        agents: list[CanonicalAgent] = []
        for yaml_path in sorted(comp_dir.glob("*.jerry.yaml")):
            agent = self._load_agent(yaml_path)
            if agent:
                agents.append(agent)
        return agents

    def get_composition_dir(self, skill: str) -> Path:
        """Get the composition directory path for a skill.

        Args:
            skill: Skill directory name.

        Returns:
            Path to skills/{skill}/composition/.
        """
        return self._skills_dir / skill / "composition"

    def _load_agent(self, yaml_path: Path) -> CanonicalAgent | None:
        """Load a canonical agent from a .jerry.yaml file.

        Args:
            yaml_path: Path to the .jerry.yaml file.

        Returns:
            Parsed CanonicalAgent, or None if parsing fails.
        """
        try:
            yaml_content = yaml_path.read_text(encoding="utf-8")
            data = yaml.safe_load(yaml_content)
            if not isinstance(data, dict):
                return None

            # Load companion .jerry.prompt.md
            prompt_path = yaml_path.with_suffix("").with_suffix(".jerry.prompt.md")
            prompt_body = ""
            if prompt_path.exists():
                full_text = prompt_path.read_text(encoding="utf-8")
                # Strip the "# agent-name System Prompt" header line
                lines = full_text.split("\n")
                if lines and lines[0].startswith("# "):
                    prompt_body = "\n".join(lines[1:]).lstrip("\n")
                else:
                    prompt_body = full_text

            return self._parse_agent(data, prompt_body)
        except Exception:
            return None

    def _parse_agent(self, data: dict[str, Any], prompt_body: str) -> CanonicalAgent:
        """Parse a canonical agent from YAML data and prompt body.

        Args:
            data: Parsed YAML dictionary.
            prompt_body: System prompt content from .jerry.prompt.md.

        Returns:
            Parsed CanonicalAgent entity.
        """
        # Extract model tier
        model_data = data.get("model", {})
        if isinstance(model_data, dict):
            model_tier = ModelTier.from_string(model_data.get("tier", "reasoning_standard"))
            model_preferences = model_data.get("preferences", [])
        else:
            model_tier = ModelTier.REASONING_STANDARD
            model_preferences = []

        # Extract tools
        tools_data = data.get("tools", {})
        if isinstance(tools_data, dict):
            native_tools = tools_data.get("native", [])
            mcp_servers = tools_data.get("mcp", [])
            forbidden_tools = tools_data.get("forbidden", [])
        else:
            native_tools = []
            mcp_servers = []
            forbidden_tools = []

        # Extract body format from portability
        portability = data.get("portability", {})
        body_format_str = portability.get("body_format", "xml")
        body_format = BodyFormat.from_string(body_format_str)

        # Collect known fields to separate extra_yaml
        known_keys = {
            "name",
            "version",
            "description",
            "skill",
            "identity",
            "persona",
            "model",
            "tools",
            "tool_tier",
            "guardrails",
            "output",
            "constitution",
            "validation",
            "portability",
            "enforcement",
            "session_context",
            "prior_art",
        }
        extra_yaml = {k: v for k, v in data.items() if k not in known_keys}

        return CanonicalAgent(
            name=data["name"],
            version=data["version"],
            description=data["description"],
            skill=data["skill"],
            identity=data.get("identity", {}),
            persona=data.get("persona", {}),
            model_tier=model_tier,
            model_preferences=model_preferences,
            native_tools=native_tools,
            mcp_servers=mcp_servers,
            forbidden_tools=forbidden_tools,
            tool_tier=ToolTier.from_string(data.get("tool_tier", "T1")),
            guardrails=data.get("guardrails", {}),
            output=data.get("output", {}),
            constitution=data.get("constitution", {}),
            validation=data.get("validation", {}),
            portability=portability,
            enforcement=data.get("enforcement", {}),
            session_context=data.get("session_context", {}),
            prior_art=data.get("prior_art", []),
            prompt_body=prompt_body,
            body_format=body_format,
            extra_yaml=extra_yaml,
        )
