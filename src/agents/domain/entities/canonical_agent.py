# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
CanonicalAgent - Parsed canonical agent definition entity.

Represents the merged content of a .agent.yaml structured data file
and its companion .prompt.md system prompt file.

References:
    - ADR-PROJ010-003: LLM Portability Architecture
    - agent-development-standards.md: H-34 agent definition standards
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from src.agents.domain.value_objects.body_format import BodyFormat
from src.agents.domain.value_objects.model_tier import ModelTier
from src.agents.domain.value_objects.tool_tier import ToolTier


@dataclass(frozen=True)
class CanonicalAgent:
    """Parsed canonical agent definition.

    Combines structured data from .agent.yaml with the system prompt
    body from .prompt.md into a single domain entity.

    Attributes:
        name: Agent identifier in kebab-case.
        version: Semantic version string.
        description: WHAT+WHEN+triggers description.
        skill: Parent skill directory name.
        identity: Identity block (role, expertise, cognitive_mode).
        persona: Optional persona configuration.
        model_tier: Abstract model capability tier.
        model_preferences: Ordered vendor-specific model preferences.
        native_tools: Abstract native tool capability names.
        mcp_servers: MCP server names.
        forbidden_tools: Tools this agent must NOT have.
        tool_tier: Security tier classification.
        guardrails: Guardrails configuration.
        output: Output specification.
        constitution: Constitutional compliance block.
        validation: Post-completion validation checks.
        portability: Cross-vendor portability configuration.
        enforcement: Enforcement tier and escalation.
        session_context: Handoff protocol configuration.
        prior_art: Referenced prior art citations.
        prompt_body: Raw system prompt content from .prompt.md.
        body_format: Target body format for vendor transformation.
        extra_yaml: Additional YAML fields not covered by named attributes.
    """

    name: str
    version: str
    description: str
    skill: str
    identity: dict[str, Any]
    tool_tier: ToolTier
    native_tools: list[str]
    prompt_body: str
    constitution: dict[str, Any]
    guardrails: dict[str, Any]
    persona: dict[str, Any] = field(default_factory=dict)
    model_tier: ModelTier = ModelTier.REASONING_STANDARD
    model_preferences: list[str] = field(default_factory=list)
    mcp_servers: list[str] = field(default_factory=list)
    forbidden_tools: list[str] = field(default_factory=list)
    output: dict[str, Any] = field(default_factory=dict)
    validation: dict[str, Any] = field(default_factory=dict)
    portability: dict[str, Any] = field(default_factory=dict)
    enforcement: dict[str, Any] = field(default_factory=dict)
    session_context: dict[str, Any] = field(default_factory=dict)
    prior_art: list[str] = field(default_factory=list)
    body_format: BodyFormat = BodyFormat.XML
    extra_yaml: dict[str, Any] = field(default_factory=dict)

    @property
    def has_mcp(self) -> bool:
        """Check if this agent uses any MCP servers."""
        return len(self.mcp_servers) > 0

    @property
    def has_delegation(self) -> bool:
        """Check if this agent can delegate to sub-agents."""
        return "agent_delegate" in self.native_tools

    @property
    def cognitive_mode(self) -> str:
        """Extract cognitive mode from identity block."""
        return self.identity.get("cognitive_mode", "convergent")

    @property
    def role(self) -> str:
        """Extract role from identity block."""
        return self.identity.get("role", "")

    @property
    def expertise(self) -> list[str]:
        """Extract expertise list from identity block."""
        return self.identity.get("expertise", [])
