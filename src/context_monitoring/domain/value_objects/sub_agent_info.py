# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
SubAgentInfo - Sub-agent metadata value object.

Immutable value object representing a Claude Code sub-agent's
lifecycle state and context usage.

References:
    - FEAT-002: Status Line / Context Monitoring Unification
    - EN-009: Domain VOs + ContextEstimateComputer Service
    - DEC-004 D-014: Sub-agent tracking via transcript parsing
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SubAgentInfo:
    """Sub-agent lifecycle and context usage data.

    Captures per-sub-agent metadata from lifecycle hooks
    (SubagentStart/SubagentStop) and transcript parsing.

    Attributes:
        agent_id: Unique agent identifier from Claude Code.
        agent_type: Agent type (e.g., "Explore", "Bash", "Plan").
        model: Model used by the agent (e.g., "claude-opus-4-6").
        status: Lifecycle status ("active" or "completed").
        context_tokens: Current context window tokens used.
            Zero if not yet computed.
        context_fill_pct: Context fill as percentage (0-100).
            Zero if not yet computed.
        output_tokens: Total output tokens generated.
            Zero if not yet computed.

    Example:
        >>> agent = SubAgentInfo(
        ...     agent_id="a01ef61",
        ...     agent_type="Explore",
        ...     model="claude-opus-4-6",
        ...     status="completed",
        ...     context_tokens=63143,
        ...     context_fill_pct=31.6,
        ...     output_tokens=12500,
        ... )
    """

    agent_id: str
    agent_type: str
    model: str
    status: str
    context_tokens: int = 0
    context_fill_pct: float = 0.0
    output_tokens: int = 0
