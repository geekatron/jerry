# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
TranscriptSubAgentReader - Adapter for reading sub-agent context usage.

Reads sub-agent lifecycle data from the lifecycle JSON file (written by
the SubagentStop hook, EN-017) and parses each agent's JSONL transcript
to extract the last cumulative usage entry. Combines both sources to
produce SubAgentInfo value objects with per-agent context fill metrics.

Key insight: The Anthropic API returns cumulative token usage in each
response. Therefore, only the last ``usage`` entry in a sub-agent
transcript represents its current context fill. No summation across
entries is needed.

Design Principles:
    - **Fail-graceful**: Missing/corrupt files produce zero-token agents,
      never raise exceptions.
    - **Efficient**: Reads only the last 8KB of each transcript (the last
      few JSONL entries), avoiding full-file reads.
    - **Composable**: Uses SubAgentInfo domain value objects.

References:
    - EN-018: Sub-Agent Transcript Parser
    - EN-017: Sub-Agent Lifecycle Hooks (lifecycle file writer)
    - DEC-004 D-014: Sub-agent tracking via transcript parsing
    - FEAT-002: Status Line / Context Monitoring Unification
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any

from src.context_monitoring.domain.value_objects.sub_agent_info import SubAgentInfo

logger = logging.getLogger(__name__)

# Read only the last 8KB of transcript files — sufficient for the last
# few JSONL entries in sub-agent transcripts.
_TAIL_READ_SIZE: int = 8192


class TranscriptSubAgentReader:
    """Infrastructure adapter for reading sub-agent context usage.

    Reads the lifecycle tracking file (written by SubagentStop hooks)
    and parses each agent's JSONL transcript for per-agent context
    window usage data.

    Attributes:
        _lifecycle_path: Path to the sub-agent lifecycle JSON file.

    Example:
        >>> reader = TranscriptSubAgentReader(
        ...     lifecycle_path=Path(".jerry/local/subagent-lifecycle.json"),
        ... )
        >>> agents = reader.read_sub_agents(context_window_size=200_000)
    """

    def __init__(self, lifecycle_path: Path) -> None:
        """Initialize the reader.

        Args:
            lifecycle_path: Path to the sub-agent lifecycle JSON file
                (written by HooksSubagentStopHandler).
        """
        self._lifecycle_path = lifecycle_path

    def read_sub_agents(self, context_window_size: int) -> list[SubAgentInfo]:
        """Read sub-agent lifecycle and context usage data.

        Reads agent metadata from the lifecycle file, then parses each
        agent's transcript JSONL for the last cumulative usage entry.
        Computes fill percentage using the provided context_window_size.

        Args:
            context_window_size: The main session's context window size
                for computing per-agent fill percentage.

        Returns:
            List of SubAgentInfo with per-agent context fill data.
            Returns empty list if no agents have been recorded.
        """
        lifecycle = self._load_lifecycle()
        agents_data = lifecycle.get("agents", {})

        if not agents_data:
            return []

        result: list[SubAgentInfo] = []
        for agent_id, data in agents_data.items():
            context_tokens = 0
            output_tokens = 0

            transcript_path = data.get("transcript_path", "")
            if transcript_path:
                usage = self._read_last_usage(transcript_path)
                if usage is not None:
                    context_tokens = self._sum_context_tokens(usage)
                    output_tokens = int(usage.get("output_tokens", 0))

            fill_pct = (
                round(context_tokens / context_window_size * 100, 1)
                if context_window_size > 0
                else 0.0
            )

            result.append(
                SubAgentInfo(
                    agent_id=agent_id,
                    agent_type=data.get("agent_type", ""),
                    model=data.get("model", ""),
                    status=data.get("status", "completed"),
                    context_tokens=context_tokens,
                    context_fill_pct=fill_pct,
                    output_tokens=output_tokens,
                )
            )

        return result

    def _load_lifecycle(self) -> dict[str, Any]:
        """Load the lifecycle JSON file.

        Returns:
            The lifecycle data dictionary, or empty dict if the file
            is missing, empty, or corrupt.
        """
        if not self._lifecycle_path.exists():
            return {}
        try:
            content = self._lifecycle_path.read_text(encoding="utf-8")
            if not content.strip():
                return {}
            return json.loads(content)
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("Failed to read lifecycle file: %s", exc)
            return {}

    def _read_last_usage(self, transcript_path: str) -> dict[str, Any] | None:
        """Read the last usage entry from a sub-agent JSONL transcript.

        Reads the last 8KB of the file and scans lines in reverse to
        find the last entry with ``message.usage`` data. This is efficient
        because the Anthropic API returns cumulative usage, so only the
        last entry matters.

        Args:
            transcript_path: Path to the sub-agent JSONL transcript.

        Returns:
            The ``message.usage`` dictionary from the last matching entry,
            or None if no matching entry is found.
        """
        try:
            if not os.path.exists(transcript_path):
                return None

            file_size = os.path.getsize(transcript_path)
            if file_size == 0:
                return None

            with open(transcript_path, "rb") as fh:
                # Read last N bytes — sufficient for last few JSONL entries
                read_size = min(_TAIL_READ_SIZE, file_size)
                fh.seek(file_size - read_size)
                chunk = fh.read(read_size)

            text = chunk.decode("utf-8", errors="replace")
            lines = text.splitlines()

            # Scan from end to find last line with usage data
            for line in reversed(lines):
                stripped = line.strip()
                if not stripped:
                    continue
                usage = self._extract_usage(stripped)
                if usage is not None:
                    return usage

            return None
        except OSError as exc:
            logger.warning("Failed to read transcript %s: %s", transcript_path, exc)
            return None

    @staticmethod
    def _extract_usage(line: str) -> dict[str, Any] | None:
        """Extract message.usage from a JSONL line if present.

        Args:
            line: A single JSONL line (stripped).

        Returns:
            The usage dictionary if the entry has ``message.usage``
            with at least ``input_tokens``, or None otherwise.
        """
        try:
            data = json.loads(line)
        except (json.JSONDecodeError, TypeError):
            return None

        if not isinstance(data, dict):
            return None

        message = data.get("message")
        if not isinstance(message, dict):
            return None

        usage = message.get("usage")
        if not isinstance(usage, dict):
            return None

        if "input_tokens" not in usage:
            return None

        return usage

    @staticmethod
    def _sum_context_tokens(usage: dict[str, Any]) -> int:
        """Sum all input token fields from a usage object.

        Computes: ``input_tokens + cache_creation_input_tokens + cache_read_input_tokens``.

        Args:
            usage: The ``message.usage`` dictionary.

        Returns:
            The cumulative context window token count.
        """
        return (
            int(usage.get("input_tokens", 0))
            + int(usage.get("cache_creation_input_tokens", 0))
            + int(usage.get("cache_read_input_tokens", 0))
        )
