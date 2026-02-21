# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ITranscriptReader - Port for reading cumulative context window usage.

This port defines the contract for reading the cumulative context window
token usage from a Claude Code JSONL transcript file. The return value
represents the total tokens consumed in the context window, computed as:
``input_tokens + cache_creation_input_tokens + cache_read_input_tokens``.

The port is intentionally minimal: it provides a single method for reading
the most recent cumulative usage, enabling context fill estimation.

References:
    - EN-004: ContextFillEstimator and ResumptionContextGenerator
    - SPIKE-003: Corrected semantics — cumulative usage, not marginal input_tokens
    - FEAT-001: Context Detection
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class ITranscriptReader(Protocol):
    """Port for reading cumulative context window usage from JSONL transcripts.

    This protocol defines the contract for reading the cumulative context
    window token usage from a Claude Code transcript file. Implementations
    scan the transcript for the last entry with ``message.usage`` data
    and return the sum of all input token fields.

    Thread Safety:
        Implementations SHOULD ensure thread-safe read access.

    Example:
        >>> reader: ITranscriptReader = JsonlTranscriptReader()
        >>> token_count = reader.read_latest_tokens("/path/to/transcript.jsonl")
        >>> print(f"Current context usage: {token_count} tokens")
    """

    def read_latest_tokens(self, transcript_path: str) -> int:
        """Read cumulative context window usage from the latest assistant entry.

        Scans the JSONL transcript for the last entry with ``message.usage``
        data and returns the cumulative context window token count:
        ``input_tokens + cache_creation_input_tokens + cache_read_input_tokens``.

        Args:
            transcript_path: Path to the JSONL transcript file.

        Returns:
            The cumulative context window token count (sum of all input
            token fields from the last assistant entry with usage data).

        Raises:
            FileNotFoundError: If the transcript file does not exist.
            ValueError: If the file is empty, contains only whitespace,
                or has no entries with ``message.usage`` data.

        Example:
            >>> reader.read_latest_tokens("/path/to/transcript.jsonl")
            158119
        """
        ...
