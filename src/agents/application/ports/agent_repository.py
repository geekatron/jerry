# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
IAgentRepository - Port for reading canonical agent source files.

References:
    - ADR-PROJ010-003: LLM Portability Architecture
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from src.agents.domain.entities.canonical_agent import CanonicalAgent


class IAgentRepository(ABC):
    """Port for reading canonical agent definitions from the filesystem.

    Reads .jerry.yaml + .jerry.prompt.md pairs from skills/*/composition/
    and returns parsed CanonicalAgent entities.
    """

    @abstractmethod
    def get(self, agent_name: str) -> CanonicalAgent | None:
        """Retrieve a single canonical agent by name.

        Args:
            agent_name: Agent identifier (e.g., 'ps-architect').

        Returns:
            Parsed CanonicalAgent, or None if not found.
        """

    @abstractmethod
    def list_all(self) -> list[CanonicalAgent]:
        """List all canonical agents across all skills.

        Returns:
            List of all parsed CanonicalAgent entities.
        """

    @abstractmethod
    def list_by_skill(self, skill: str) -> list[CanonicalAgent]:
        """List canonical agents for a specific skill.

        Args:
            skill: Skill directory name (e.g., 'problem-solving').

        Returns:
            List of parsed CanonicalAgent entities for the skill.
        """

    @abstractmethod
    def get_composition_dir(self, skill: str) -> Path:
        """Get the composition directory path for a skill.

        Args:
            skill: Skill directory name.

        Returns:
            Path to skills/{skill}/composition/.
        """
