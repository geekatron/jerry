# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
GovernanceSectionBuilder - Builds governance markdown sections from CanonicalAgent.

Converts governance metadata fields into ## heading sections that the
PromptTransformer will convert to XML tags for Claude Code agents.
Only generates sections for non-empty fields. Skips sections where a
heading already exists in the prompt body to prevent duplication.

References:
    - PROJ-012: Agent Configuration Extraction & Schema Enforcement
    - agent-development-standards.md: H-34 agent definition standards
"""

from __future__ import annotations

import re
from typing import Any

import yaml

from src.agents.domain.entities.canonical_agent import CanonicalAgent
from src.agents.domain.value_objects.tool_tier import ToolTier

# Human-readable labels for tool tiers
_TOOL_TIER_LABELS: dict[ToolTier, str] = {
    ToolTier.T1: "Read-Only",
    ToolTier.T2: "Read-Write",
    ToolTier.T3: "External",
    ToolTier.T4: "Persistent",
    ToolTier.T5: "Full",
}


class GovernanceSectionBuilder:
    """Builds markdown governance sections from CanonicalAgent fields.

    Converts governance metadata into ## heading sections that the
    PromptTransformer will convert to XML tags for Claude Code agents.
    Only generates sections for non-empty fields.
    """

    def build(self, agent: CanonicalAgent, existing_body: str = "") -> str:
        """Build all governance sections as markdown.

        Args:
            agent: Canonical agent definition.
            existing_body: Existing prompt body to check for duplicate headings.

        Returns:
            Concatenated ## heading sections for governance fields.
            Empty string if all governance fields are empty/default.
        """
        existing_headings = self._extract_headings(existing_body)
        sections: list[str] = []

        # Agent Version
        if agent.version and "agent version" not in existing_headings:
            sections.append(f"## Agent Version\n\n{agent.version}\n")

        # Tool Tier
        if agent.tool_tier and "tool tier" not in existing_headings:
            label = _TOOL_TIER_LABELS.get(agent.tool_tier, "")
            tier_text = f"{agent.tool_tier.value} ({label})" if label else agent.tool_tier.value
            sections.append(f"## Tool Tier\n\n{tier_text}\n")

        # Enforcement
        if agent.enforcement and "enforcement" not in existing_headings:
            sections.append(f"## Enforcement\n\n{self._format_dict(agent.enforcement)}\n")

        # Portability
        if agent.portability and "portability" not in existing_headings:
            sections.append(f"## Portability\n\n{self._format_dict(agent.portability)}\n")

        # Prior Art
        if agent.prior_art and "prior art" not in existing_headings:
            items = "\n".join(f"- {item}" for item in agent.prior_art)
            sections.append(f"## Prior Art\n\n{items}\n")

        # Session Context
        if agent.session_context and "session context" not in existing_headings:
            sections.append(f"## Session Context\n\n{self._format_dict(agent.session_context)}\n")

        return "\n".join(sections)

    def _format_dict(self, data: dict[str, Any]) -> str:
        """Format a dictionary as YAML content for readability.

        Args:
            data: Dictionary to format.

        Returns:
            YAML-formatted string.
        """
        return yaml.dump(
            data,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
            width=100,
        ).rstrip("\n")

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
