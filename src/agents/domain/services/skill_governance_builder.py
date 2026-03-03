# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
SkillGovernanceSectionBuilder - Builds governance markdown sections from CanonicalSkill.

Converts governance metadata fields into ## heading sections injected
into SKILL.md body. Unlike agents, no XML transformation is needed —
SKILL.md body is human-authored documentation consumed by the MAIN CONTEXT.

Governance sections use ## headings with heading dedup from GovernanceSectionBuilder.

References:
    - PROJ-012: Skill Composition Pipeline
    - agent-development-standards.md: Pattern from GovernanceSectionBuilder
"""

from __future__ import annotations

import re

import yaml

from src.agents.domain.entities.canonical_skill import CanonicalSkill


class SkillGovernanceSectionBuilder:
    """Builds markdown governance sections from CanonicalSkill fields.

    Converts governance metadata into ## heading sections injected
    into SKILL.md body. Only generates sections for non-empty fields.
    Skips sections where a heading already exists to prevent duplication.
    """

    def build(self, skill: CanonicalSkill, existing_body: str = "") -> str:
        """Build all governance sections as markdown.

        Args:
            skill: Canonical skill definition.
            existing_body: Existing SKILL.md body to check for duplicate headings.

        Returns:
            Concatenated ## heading sections for governance fields.
            Empty string if all governance fields are empty/default.
        """
        existing_headings = self._extract_headings(existing_body)
        sections: list[str] = []

        # Skill Version
        if skill.version and "skill version" not in existing_headings:
            sections.append(f"## Skill Version\n\n{skill.version}\n")

        # Activation Keywords
        if skill.activation_keywords and "activation keywords" not in existing_headings:
            items = "\n".join(f"- {kw}" for kw in skill.activation_keywords)
            sections.append(f"## Activation Keywords\n\n{items}\n")

        # Agent Registry
        if skill.agents and "agent registry" not in existing_headings:
            items = "\n".join(f"- {agent}" for agent in skill.agents)
            sections.append(f"## Agent Registry\n\n{items}\n")

        # Context Injection
        if skill.context_injection and "context injection" not in existing_headings:
            formatted = yaml.dump(
                skill.context_injection,
                default_flow_style=False,
                sort_keys=False,
                allow_unicode=True,
                width=100,
            ).rstrip("\n")
            sections.append(f"## Context Injection\n\n```yaml\n{formatted}\n```\n")

        return "\n".join(sections)

    def _extract_headings(self, body: str) -> set[str]:
        """Extract all ## level headings from markdown body (case-insensitive).

        Args:
            body: Markdown body text.

        Returns:
            Set of heading names in lowercase (without ## prefix).
        """
        headings: set[str] = set()
        for match in re.finditer(r"^##\s+(.+?)(?:\s*<!--.*-->)?\s*$", body, re.MULTILINE):
            headings.add(match.group(1).strip().lower())
        return headings
