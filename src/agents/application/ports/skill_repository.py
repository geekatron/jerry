# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ISkillRepository - Port for reading canonical skill source files.

References:
    - PROJ-012: Skill Composition Pipeline
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from src.agents.domain.entities.canonical_skill import CanonicalSkill


class ISkillRepository(ABC):
    """Port for reading canonical skill definitions from the filesystem.

    Reads skill.jerry.yaml + existing SKILL.md from skills/*/composition/
    and returns parsed CanonicalSkill entities.
    """

    @abstractmethod
    def get(self, skill_name: str) -> CanonicalSkill | None:
        """Retrieve a single canonical skill by name.

        Args:
            skill_name: Skill identifier (e.g., 'problem-solving').

        Returns:
            Parsed CanonicalSkill, or None if not found.
        """

    @abstractmethod
    def list_all(self) -> list[CanonicalSkill]:
        """List all canonical skills.

        Returns:
            List of all parsed CanonicalSkill entities.
        """

    @abstractmethod
    def get_skill_md_path(self, skill_name: str) -> Path:
        """Get the SKILL.md path for a skill.

        Args:
            skill_name: Skill directory name.

        Returns:
            Path to skills/{skill}/SKILL.md.
        """
