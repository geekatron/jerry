# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""SkillExtractor Application Service.

Extracts skill and agent metadata from the skills/ directory by reading
SKILL.md and agents/*.md frontmatter via the IFrontmatterReader port.

Location: src/docs/application/services/skill_extractor.py
Reference: doc-module-spec.md Section: Extraction Pipeline
           M-1: Input sanitization
           M-5: Schema validation
"""

from __future__ import annotations

import logging
import re
from glob import glob
from pathlib import Path
from typing import TYPE_CHECKING

from src.docs.domain.value_objects.agent_data import AgentData
from src.docs.domain.value_objects.skill_data import SkillData

if TYPE_CHECKING:
    from src.docs.domain.ports.frontmatter_reader import IFrontmatterReader

logger = logging.getLogger(__name__)

_SKILL_NAME_PATTERN = re.compile(r"^[a-zA-Z][a-zA-Z0-9-]*$")
_AGENT_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9-]*$")
_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")
_HTML_TAG_PATTERN = re.compile(r"<[^>]+>")
# M-1: Strip markdown links whose URL scheme is not in the allowlist.
# Allowlist: http://, https://, mailto:, and relative paths (no scheme).
# Strips [text](javascript:...), [text](data:...), [text](vbscript:...), etc.
_UNSAFE_LINK_PATTERN = re.compile(
    r"\[([^\]]*)\]\((?!https?://|mailto:|/)(?:[a-zA-Z][a-zA-Z0-9+\-.]*:)[^)]*\)"
)
_MAX_NAME_LENGTH = 100
_MAX_DESCRIPTION_LENGTH = 1024
_MAX_ACTIVATION_KEYWORDS = 30

# Case-insensitive exclusion patterns for agent files
_EXCLUDED_AGENT_PATTERNS = ("TEMPLATE", "EXTENSION")


class SkillExtractor:
    """Extract skill and agent metadata from the skills/ directory.

    Reads SKILL.md frontmatter and discovers agent definition files,
    applying M-1 sanitization and M-5 schema validation on all fields.

    Attributes:
        _reader: Frontmatter reader port for parsing YAML frontmatter.
    """

    def __init__(self, reader: IFrontmatterReader) -> None:
        """Initialize with a frontmatter reader.

        Args:
            reader: Implementation of IFrontmatterReader for reading
                YAML frontmatter from markdown files.
        """
        self._reader = reader

    def extract_all(self, skills_dir: str) -> list[SkillData]:
        """Extract metadata for all skills in the given directory.

        Globs for ``{skills_dir}/*/SKILL.md``, reads frontmatter from
        each, discovers agent files, validates and sanitizes all fields,
        and returns a sorted list of SkillData value objects.

        Args:
            skills_dir: Path to the skills directory (e.g., ``"skills/"``).

        Returns:
            Alphabetically sorted list of SkillData for all valid skills.
            Skills with missing required ``name`` field are skipped with
            a warning.
        """
        skill_files = sorted(glob(str(Path(skills_dir) / "*" / "SKILL.md")))
        skills: list[SkillData] = []

        for skill_file in skill_files:
            skill_data = self._extract_skill(skill_file)
            if skill_data is not None:
                skills.append(skill_data)

        skills.sort(key=lambda s: s.name)
        return skills

    def _extract_skill(self, skill_file: str) -> SkillData | None:
        """Extract a single skill from its SKILL.md file.

        Args:
            skill_file: Path to the SKILL.md file.

        Returns:
            SkillData if valid, None if the skill should be skipped.
        """
        try:
            frontmatter = self._reader.read_frontmatter(skill_file)
        except (FileNotFoundError, ValueError, RuntimeError) as e:
            logger.warning("Failed to read frontmatter from %s: %s", skill_file, e)
            return None

        # M-5: name is required
        raw_name = frontmatter.get("name")
        if not raw_name:
            logger.warning("Skipping %s: missing required 'name' field", skill_file)
            return None

        # M-1: Validate and sanitize name
        name = str(raw_name).strip()[:_MAX_NAME_LENGTH]
        if not _SKILL_NAME_PATTERN.match(name):
            logger.warning(
                "Skipping %s: name '%s' does not match pattern %s",
                skill_file,
                name,
                _SKILL_NAME_PATTERN.pattern,
            )
            return None

        # M-1: Validate version
        raw_version = frontmatter.get("version", "0.0.0")
        version = str(raw_version).strip()
        if not _VERSION_PATTERN.match(version):
            version = "0.0.0"

        # M-1: Sanitize description — strip HTML, truncate
        raw_description = frontmatter.get("description", "")
        description = self._sanitize_description(str(raw_description))

        # M-5: Default for missing description
        if not description:
            description = "(no description)"

        # M-5: Validate activation-keywords count (max 30)
        # Policy: warn-only (no truncation). Keywords are routing metadata
        # consumed by the skill router, not by the doc module. Truncation
        # would silently alter routing behavior. Warning alerts the skill
        # author to reduce their keyword count.
        raw_keywords = frontmatter.get("activation-keywords")
        if isinstance(raw_keywords, list) and len(raw_keywords) > _MAX_ACTIVATION_KEYWORDS:
            logger.warning(
                "%s: 'activation-keywords' has %d entries (max %d); "
                "skill author should reduce keyword count",
                skill_file,
                len(raw_keywords),
                _MAX_ACTIVATION_KEYWORDS,
            )

        # Extract agents
        skill_dir = str(Path(skill_file).parent)
        agents = self._extract_agents(skill_dir)

        return SkillData(
            name=name,
            description=description,
            version=version,
            agent_count=len(agents),
            agents=agents,
            file_path=skill_file,
        )

    def _extract_agents(self, skill_dir: str) -> list[AgentData]:
        """Extract agent metadata from the skill's agents/ directory.

        Args:
            skill_dir: Path to the skill directory containing agents/.

        Returns:
            List of AgentData for valid, non-excluded agent files.
        """
        agents_dir = Path(skill_dir) / "agents"
        if not agents_dir.is_dir():
            return []

        agent_files = sorted(agents_dir.glob("*.md"))
        agents: list[AgentData] = []

        for agent_file in agent_files:
            # Exclude TEMPLATE and EXTENSION files (case-insensitive)
            filename_upper = agent_file.name.upper()
            if any(pattern in filename_upper for pattern in _EXCLUDED_AGENT_PATTERNS):
                continue

            agent_data = self._extract_agent(str(agent_file))
            if agent_data is not None:
                agents.append(agent_data)

        return agents

    def _extract_agent(self, agent_file: str) -> AgentData | None:
        """Extract a single agent from its definition file.

        Args:
            agent_file: Path to the agent .md file.

        Returns:
            AgentData if valid, None if the agent should be skipped.
        """
        try:
            frontmatter = self._reader.read_frontmatter(agent_file)
        except (FileNotFoundError, ValueError, RuntimeError) as e:
            logger.warning("Failed to read agent frontmatter from %s: %s", agent_file, e)
            return None

        raw_name = frontmatter.get("name")
        if not raw_name:
            logger.warning("Skipping agent %s: missing 'name' field", agent_file)
            return None

        name = str(raw_name).strip()
        if not _AGENT_NAME_PATTERN.match(name):
            logger.warning(
                "Skipping agent %s: name '%s' does not match pattern %s",
                agent_file,
                name,
                _AGENT_NAME_PATTERN.pattern,
            )
            return None

        raw_description = frontmatter.get("description", "")
        description = self._sanitize_description(str(raw_description))
        if not description:
            description = "(no description)"

        model = str(frontmatter.get("model", "")).strip()

        return AgentData(
            name=name,
            description=description,
            model=model,
            file_path=agent_file,
        )

    @staticmethod
    def _sanitize_description(text: str) -> str:
        """Sanitize a description field (M-1).

        Strips HTML tags and markdown links whose URL scheme is not in the
        allowlist (http://, https://, mailto:, relative paths with no scheme).
        Dangerous schemes such as ``javascript:``, ``data:``, and
        ``vbscript:`` are neutralized by replacing the full link with the
        link text only. The result is then truncated to the maximum allowed
        length.

        Args:
            text: Raw description text.

        Returns:
            Sanitized description string.
        """
        # Strip HTML tags
        sanitized = _HTML_TAG_PATTERN.sub("", text)
        # Replace unsafe markdown links [text](scheme:...) with plain text
        sanitized = _UNSAFE_LINK_PATTERN.sub(r"\1", sanitized)
        return sanitized.strip()[:_MAX_DESCRIPTION_LENGTH]
