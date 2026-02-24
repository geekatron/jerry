# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ISubAgentReader - Port for reading sub-agent lifecycle and context usage.

This port defines the contract for reading sub-agent information including
lifecycle state (from hook events) and context window usage (from transcript
parsing). Implementations combine data from multiple sources to produce
a unified view of all sub-agents in the current session.

References:
    - EN-018: Sub-Agent Transcript Parser
    - DEC-004 D-014: Sub-agent tracking via transcript parsing + hooks
    - FEAT-002: Status Line / Context Monitoring Unification
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from src.context_monitoring.domain.value_objects.sub_agent_info import SubAgentInfo


@runtime_checkable
class ISubAgentReader(Protocol):
    """Port for reading sub-agent lifecycle and context usage data.

    Combines sub-agent lifecycle data (from SubagentStop hooks) with
    context window usage data (from transcript parsing) to produce
    per-agent metrics including context fill percentage.

    Thread Safety:
        Implementations SHOULD ensure thread-safe read access.

    Example:
        >>> reader: ISubAgentReader = TranscriptSubAgentReader(...)
        >>> agents = reader.read_sub_agents(context_window_size=200_000)
        >>> for agent in agents:
        ...     print(f"{agent.agent_id}: {agent.context_fill_pct}%")
    """

    def read_sub_agents(self, context_window_size: int) -> list[SubAgentInfo]:
        """Read sub-agent lifecycle and context usage data.

        Reads agent metadata from the lifecycle tracking file and
        parses transcript JSONL files for per-agent context window
        usage. Computes fill percentage using the provided
        context_window_size.

        Args:
            context_window_size: The main session's context window size
                (e.g., 200000) for computing per-agent fill percentage.
                Must be > 0 for meaningful fill percentages.

        Returns:
            List of SubAgentInfo with per-agent context fill data.
            Returns empty list if no agents have been recorded.
        """
        ...
