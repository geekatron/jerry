# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
FilesystemSkillRepository - Reads canonical skill files from the filesystem.

Reads skill.jerry.yaml from skills/*/composition/ directories and
existing SKILL.md body content for composition.

References:
    - PROJ-012: Skill Composition Pipeline
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import yaml

from src.agents.application.ports.skill_repository import ISkillRepository
from src.agents.domain.entities.canonical_skill import CanonicalSkill

logger = logging.getLogger(__name__)


class FilesystemSkillRepository(ISkillRepository):
    """Reads canonical skill definitions from the filesystem.

    Scans skills/*/composition/ for skill.jerry.yaml files.

    Attributes:
        _skills_dir: Path to the skills/ directory.
    """

    def __init__(self, skills_dir: Path) -> None:
        """Initialize with skills directory path.

        Args:
            skills_dir: Path to skills/ directory.
        """
        self._skills_dir = skills_dir

    def get(self, skill_name: str) -> CanonicalSkill | None:
        """Retrieve a single canonical skill by name.

        Args:
            skill_name: Skill identifier (e.g., 'problem-solving').

        Returns:
            Parsed CanonicalSkill, or None if not found.
        """
        yaml_path = self._skills_dir / skill_name / "composition" / "skill.jerry.yaml"
        if not yaml_path.exists():
            return None

        return self._load_skill(yaml_path, skill_name)

    def list_all(self) -> list[CanonicalSkill]:
        """List all canonical skills.

        Returns:
            List of all parsed CanonicalSkill entities.
        """
        skills: list[CanonicalSkill] = []
        for skill_dir in sorted(self._skills_dir.iterdir()):
            if not skill_dir.is_dir():
                continue
            yaml_path = skill_dir / "composition" / "skill.jerry.yaml"
            if yaml_path.exists():
                skill = self._load_skill(yaml_path, skill_dir.name)
                if skill:
                    skills.append(skill)
        return skills

    def get_skill_md_path(self, skill_name: str) -> Path:
        """Get the SKILL.md path for a skill.

        Args:
            skill_name: Skill directory name.

        Returns:
            Path to skills/{skill}/SKILL.md.
        """
        return self._skills_dir / skill_name / "SKILL.md"

    def _load_skill(self, yaml_path: Path, skill_name: str) -> CanonicalSkill | None:
        """Load a canonical skill from a skill.jerry.yaml file.

        Args:
            yaml_path: Path to the skill.jerry.yaml file.
            skill_name: Skill directory name.

        Returns:
            Parsed CanonicalSkill, or None if parsing fails.
        """
        try:
            yaml_content = yaml_path.read_text(encoding="utf-8")
            data = yaml.safe_load(yaml_content)
            if not isinstance(data, dict):
                logger.warning(
                    "Skill '%s': %s did not parse as a YAML mapping",
                    skill_name,
                    yaml_path,
                )
                return None

            # Load existing SKILL.md body
            skill_md_path = self._skills_dir / skill_name / "SKILL.md"
            skill_body = ""
            if skill_md_path.exists():
                full_text = skill_md_path.read_text(encoding="utf-8")
                _, skill_body = self._parse_skill_md(full_text)

            return self._parse_skill(data, skill_body)
        except yaml.YAMLError:
            logger.warning(
                "Skill '%s': failed to parse YAML from %s",
                skill_name,
                yaml_path,
                exc_info=True,
            )
            return None
        except (KeyError, TypeError) as exc:
            logger.warning(
                "Skill '%s': missing required field in %s: %s",
                skill_name,
                yaml_path,
                exc,
            )
            return None
        except OSError:
            logger.warning(
                "Skill '%s': I/O error reading %s",
                skill_name,
                yaml_path,
                exc_info=True,
            )
            return None

    def _parse_skill(self, data: dict[str, Any], skill_body: str) -> CanonicalSkill:
        """Parse a canonical skill from YAML data and existing body.

        Args:
            data: Parsed YAML dictionary from skill.jerry.yaml.
            skill_body: Existing SKILL.md body content.

        Returns:
            Parsed CanonicalSkill entity.
        """
        activation_keywords = data.get("activation-keywords", [])
        agents = data.get("agents", [])

        return CanonicalSkill(
            name=data["name"],
            version=data["version"],
            activation_keywords=tuple(activation_keywords) if activation_keywords else (),
            agents=tuple(agents) if agents else (),
            context_injection=data.get("context_injection", {}),
            license=data.get("license", ""),
            compatibility=data.get("compatibility", ""),
            metadata=data.get("metadata", {}),
            skill_body=skill_body,
        )

    @staticmethod
    def _parse_skill_md(content: str) -> tuple[dict[str, Any], str]:
        """Parse SKILL.md into frontmatter dict and body string.

        Args:
            content: Full SKILL.md file content.

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
