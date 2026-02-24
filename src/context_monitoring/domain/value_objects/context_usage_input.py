# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ContextUsageInput - Parsed context usage data from Claude Code JSON.

Immutable value object representing the exact current_usage data that
Claude Code provides on stdin to the status line command.

References:
    - FEAT-002: Status Line / Context Monitoring Unification
    - EN-009: Domain VOs + ContextEstimateComputer Service
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ContextUsageInput:
    """Parsed context usage data from Claude Code stdin JSON.

    Captures the exact token counts from the Claude Code status line
    JSON ``context_window.current_usage`` block plus session metadata
    needed for compaction detection.

    Attributes:
        session_id: Claude Code session identifier. Persists through
            compaction; changes on ``/clear``.
        input_tokens: Fresh input tokens from last API call.
        cache_creation_input_tokens: Tokens used to create cache.
        cache_read_input_tokens: Tokens read from cache.
        context_window_size: Dynamic context window size from Claude Code
            (200K standard, 500K Enterprise, 1M extended).
        used_percentage: Pre-calculated percentage used (from Claude Code).
            Can be None before first API call.
        remaining_percentage: Pre-calculated percentage remaining.
            Can be None before first API call.

    Example:
        >>> usage = ContextUsageInput(
        ...     session_id="abc123",
        ...     input_tokens=8500,
        ...     cache_creation_input_tokens=5000,
        ...     cache_read_input_tokens=12000,
        ...     context_window_size=200000,
        ...     used_percentage=73.0,
        ...     remaining_percentage=27.0,
        ... )
        >>> usage.total_context_tokens
        25500
    """

    session_id: str
    input_tokens: int
    cache_creation_input_tokens: int
    cache_read_input_tokens: int
    context_window_size: int
    used_percentage: float | None = None
    remaining_percentage: float | None = None

    @property
    def total_context_tokens(self) -> int:
        """Total tokens contributing to context window fill.

        Returns:
            Sum of input_tokens + cache_creation + cache_read.
        """
        return self.input_tokens + self.cache_creation_input_tokens + self.cache_read_input_tokens
