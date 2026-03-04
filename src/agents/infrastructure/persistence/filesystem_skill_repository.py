# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
FilesystemSkillRepository - Reads canonical skill files from the filesystem.

Reads canonical source triplet from skills/*/composition/:
  - skill.jerry.yaml: governance metadata (name, version, description, etc.)
  - skill.jerry.prompt.md: body content (human-authored skill documentation)
  - skill.claude-code.yaml: vendor overrides (allowed-tools, etc.)

Fallback: when skill.jerry.prompt.md does not exist, reads body from
existing SKILL.md for migration compatibility.

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

    Scans skills/*/composition/ for canonical source files.

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

        Note:
            Parse errors are silently discarded. Use
            :meth:`list_all_with_diagnostics` to receive parse error
            messages alongside the successfully parsed skills.

        Returns:
            List of all successfully parsed CanonicalSkill entities.
        """
        skills, _ = self.list_all_with_diagnostics()
        return skills

    def list_all_with_diagnostics(self) -> tuple[list[CanonicalSkill], list[str]]:
        """List all canonical skills with parse error diagnostics.

        Returns:
            Tuple of (parsed skills, parse error messages).
            Parse errors include skill name and failure reason.
        """
        skills: list[CanonicalSkill] = []
        errors: list[str] = []
        for skill_dir in sorted(self._skills_dir.iterdir()):
            if not skill_dir.is_dir():
                continue
            yaml_path = skill_dir / "composition" / "skill.jerry.yaml"
            if yaml_path.exists():
                skill = self._load_skill(yaml_path, skill_dir.name)
                if skill:
                    skills.append(skill)
                else:
                    errors.append(f"{skill_dir.name}: failed to parse {yaml_path}")
        return skills, errors

    def get_agent_body_formats(self, skill_name: str) -> dict[str, str]:
        """Get body_format values for all agents in a skill.

        Args:
            skill_name: Skill identifier (e.g., 'problem-solving').

        Returns:
            Dict of agent_name -> body_format string.
            Empty dict if skill has no agents or no composition directory.
        """
        comp_dir = self._skills_dir / skill_name / "composition"
        if not comp_dir.is_dir():
            return {}

        formats: dict[str, str] = {}
        for yaml_file in sorted(comp_dir.glob("*.jerry.yaml")):
            agent_name = yaml_file.stem.replace(".jerry", "")
            if agent_name == "skill":
                continue  # Skip the skill-level canonical source
            try:
                data = yaml.safe_load(yaml_file.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    portability = data.get("portability", {})
                    if isinstance(portability, dict):
                        bf = portability.get("body_format", "")
                        if bf:
                            formats[agent_name] = str(bf)
            except (yaml.YAMLError, OSError):
                logger.warning(
                    "Skill '%s': failed to read body_format from %s",
                    skill_name,
                    yaml_file,
                )
        return formats

    def get_skill_md_path(self, skill_name: str) -> Path:
        """Get the SKILL.md path for a skill.

        Args:
            skill_name: Skill directory name.

        Returns:
            Path to skills/{skill}/SKILL.md.
        """
        return self._skills_dir / skill_name / "SKILL.md"

    def _load_skill(self, yaml_path: Path, skill_name: str) -> CanonicalSkill | None:
        """Load a canonical skill from source files.

        Reads the canonical source triplet:
          1. skill.jerry.yaml — governance metadata
          2. skill.jerry.prompt.md — body content (fallback: SKILL.md body)
          3. skill.claude-code.yaml — vendor overrides (optional)

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

            # Load body: prefer skill.jerry.prompt.md, fallback to SKILL.md
            prompt_body = self._load_prompt_body(skill_name)

            # Load vendor overrides (optional)
            vendor_overrides = self._load_vendor_overrides(skill_name)

            return self._parse_skill(data, prompt_body, vendor_overrides)
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

    def _load_prompt_body(self, skill_name: str) -> str:
        """Load body content from canonical prompt source or SKILL.md fallback.

        Args:
            skill_name: Skill directory name.

        Returns:
            Body content string. Empty string if no source found.
        """
        # Prefer canonical source: skill.jerry.prompt.md
        prompt_md_path = self._skills_dir / skill_name / "composition" / "skill.jerry.prompt.md"
        if prompt_md_path.exists():
            return prompt_md_path.read_text(encoding="utf-8")

        # Fallback: read body from existing SKILL.md (migration path)
        skill_md_path = self._skills_dir / skill_name / "SKILL.md"
        if skill_md_path.exists():
            full_text = skill_md_path.read_text(encoding="utf-8")
            _, body = self._parse_skill_md(full_text)
            return body

        return ""

    def _load_vendor_overrides(self, skill_name: str) -> dict[str, Any]:
        """Load vendor overrides from skill.claude-code.yaml.

        Args:
            skill_name: Skill directory name.

        Returns:
            Dict of vendor override fields. Empty dict if file not found.
        """
        vendor_path = self._skills_dir / skill_name / "composition" / "skill.claude-code.yaml"
        if not vendor_path.exists():
            return {}

        try:
            vendor_data = yaml.safe_load(vendor_path.read_text(encoding="utf-8"))
            if isinstance(vendor_data, dict):
                return vendor_data
        except (yaml.YAMLError, OSError):
            logger.warning(
                "Skill '%s': failed to parse vendor overrides from %s",
                skill_name,
                vendor_path,
            )

        return {}

    def _parse_skill(
        self,
        data: dict[str, Any],
        prompt_body: str,
        vendor_overrides: dict[str, Any] | None = None,
    ) -> CanonicalSkill:
        """Parse a canonical skill from YAML data and source files.

        Args:
            data: Parsed YAML dictionary from skill.jerry.yaml.
            prompt_body: Body content from prompt source.
            vendor_overrides: Vendor overrides from skill.claude-code.yaml.

        Returns:
            Parsed CanonicalSkill entity.
        """
        activation_keywords = data.get("activation-keywords", [])
        agents = data.get("agents", [])

        return CanonicalSkill(
            name=data["name"],
            version=data["version"],
            description=data.get("description", ""),
            activation_keywords=tuple(activation_keywords) if activation_keywords else (),
            agents=tuple(agents) if agents else (),
            context_injection=data.get("context_injection", {}),
            license=data.get("license", ""),
            compatibility=data.get("compatibility", ""),
            metadata=data.get("metadata", {}),
            prompt_body=prompt_body,
            vendor_overrides=vendor_overrides or {},
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

        end = content.find("\n---", 3)
        if end == -1:
            return {}, content

        fm_text = content[4:end]
        body = content[end + 4 :].lstrip("\n")

        try:
            fm_data = yaml.safe_load(fm_text) or {}
        except yaml.YAMLError:
            fm_data = {}

        return fm_data, body
