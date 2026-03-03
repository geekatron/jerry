# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
CanonicalSkill - Parsed canonical skill definition entity.

Represents the content of a skill.jerry.yaml canonical source file
combined with the existing SKILL.md body for composition.

References:
    - PROJ-012: Skill Composition Pipeline
    - skill-canonical-v1.schema.json: Schema for canonical source
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class CanonicalSkill:
    """Parsed canonical skill definition.

    Combines structured data from skill.jerry.yaml with the SKILL.md
    body into a single domain entity for composition.

    Attributes:
        name: Skill identifier in kebab-case.
        version: Semantic version string.
        activation_keywords: Trigger phrases for routing.
        agents: Optional list of agent names in this skill.
        context_injection: Optional context injection configuration.
        license: Optional license identifier.
        compatibility: Optional environment requirements.
        metadata: Optional custom key-value pairs.
        skill_body: Existing SKILL.md body content (after frontmatter).
    """

    name: str
    version: str
    activation_keywords: tuple[str, ...] = ()
    agents: tuple[str, ...] = ()
    context_injection: dict[str, Any] = field(default_factory=dict)
    license: str = ""
    compatibility: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    skill_body: str = ""
