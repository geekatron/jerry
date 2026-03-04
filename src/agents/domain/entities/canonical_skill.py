# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
CanonicalSkill - Parsed canonical skill definition entity.

Represents the content of canonical source files for skill composition:
  - skill.jerry.yaml: governance metadata (name, version, description, etc.)
  - skill.jerry.prompt.md: body content (human-authored skill documentation)
  - skill.claude-code.yaml: vendor overrides (allowed-tools, etc.)

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

    Combines structured data from three canonical sources into a single
    domain entity for composition.

    Attributes:
        name: Skill identifier in kebab-case.
        version: Semantic version string.
        description: What the skill does and when to use it.
        activation_keywords: Trigger phrases for routing.
        agents: Optional list of agent names in this skill.
        context_injection: Optional context injection configuration.
        license: Optional license identifier.
        compatibility: Optional environment requirements.
        metadata: Optional custom key-value pairs.
        prompt_body: Body content from skill.jerry.prompt.md (or SKILL.md fallback).
        vendor_overrides: Vendor-specific overrides from skill.claude-code.yaml.
    """

    name: str
    version: str
    description: str = ""
    activation_keywords: tuple[str, ...] = ()
    agents: tuple[str, ...] = ()
    context_injection: dict[str, Any] = field(default_factory=dict)
    license: str = ""
    compatibility: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    prompt_body: str = ""
    vendor_overrides: dict[str, Any] = field(default_factory=dict)
