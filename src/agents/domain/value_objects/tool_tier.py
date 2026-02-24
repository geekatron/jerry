# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ToolTier - Security tier classification for agent tool access.

Five tiers implement the principle of least privilege (AR-006).

References:
    - agent-development-standards.md: Tool Security Tiers
"""

from __future__ import annotations

from enum import Enum


class ToolTier(Enum):
    """Agent tool security tier.

    Attributes:
        T1: Read-Only (Read, Glob, Grep).
        T2: Read-Write (T1 + Write, Edit, Bash).
        T3: External (T2 + WebSearch, WebFetch, Context7).
        T4: Persistent (T2 + Memory-Keeper).
        T5: Full (T3 + T4 + Task delegation).

    Example:
        >>> ToolTier.from_string("T3")
        <ToolTier.T3: 'T3'>
    """

    T1 = "T1"
    T2 = "T2"
    T3 = "T3"
    T4 = "T4"
    T5 = "T5"

    @classmethod
    def from_string(cls, value: str) -> ToolTier:
        """Parse tool tier from string.

        Args:
            value: Tier name (e.g., 'T1', 'T3').

        Returns:
            Matching ToolTier enum value.

        Raises:
            ValueError: If value is not a valid tool tier.
        """
        normalized = value.upper().strip()
        for tier in cls:
            if tier.value == normalized:
                return tier
        valid = [t.value for t in cls]
        raise ValueError(f"Invalid tool tier: {value!r}. Valid tiers: {', '.join(valid)}")

    @classmethod
    def calculate_from_tools(
        cls,
        native_tools: list[str],
        mcp_servers: list[str] | None = None,
    ) -> ToolTier:
        """Calculate the minimum required tool tier from a tool list.

        Args:
            native_tools: Abstract native tool names.
            mcp_servers: MCP server names (e.g., ['context7', 'memory-keeper']).

        Returns:
            Minimum ToolTier that satisfies the tool requirements.
        """
        mcp_servers = mcp_servers or []
        has_delegate = "agent_delegate" in native_tools
        has_memory_keeper = "memory-keeper" in mcp_servers
        has_external = (
            any(t in native_tools for t in ("web_search", "web_fetch")) or "context7" in mcp_servers
        )
        has_write = any(t in native_tools for t in ("file_write", "file_edit", "shell_execute"))

        if has_delegate:
            return cls.T5
        if has_memory_keeper and has_external:
            return cls.T5
        if has_memory_keeper:
            return cls.T4
        if has_external:
            return cls.T3
        if has_write:
            return cls.T2
        return cls.T1
