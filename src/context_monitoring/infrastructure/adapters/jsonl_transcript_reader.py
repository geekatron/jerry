# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
JsonlTranscriptReader - Adapter for reading context window usage from JSONL transcripts.

This adapter implements the ITranscriptReader port by scanning backward through
a Claude Code JSONL transcript file to find the last assistant entry with
``message.usage`` data, then returning the cumulative context window usage:
``input_tokens + cache_creation_input_tokens + cache_read_input_tokens``.

The reader uses an efficient backward-seek strategy to avoid reading the entire
file into memory.

File format expectation (Claude Code JSONL):
    Each line is a valid JSON object. Assistant entries have the structure::

        {"type": "assistant", "message": {"usage": {
            "input_tokens": N,
            "cache_creation_input_tokens": N,
            "cache_read_input_tokens": N
        }}}

    Non-assistant entries (user, progress, etc.) are skipped.

Raises:
    FileNotFoundError: If the transcript file does not exist.
    ValueError: If the file is empty, contains only whitespace, or has
        no entries with ``message.usage`` data.

References:
    - EN-004: ContextFillEstimator and ResumptionContextGenerator
    - SPIKE-003: Validation — corrected field path and three-field sum
    - FEAT-001: Context Detection
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

import json
import logging
import os

logger = logging.getLogger(__name__)

# Block size for backward file reading
_READ_BLOCK_SIZE: int = 4096


class JsonlTranscriptReader:
    """Infrastructure adapter for reading context window usage from JSONL transcripts.

    Scans backward through a Claude Code JSONL transcript file to find
    the last entry with ``message.usage`` data and returns the cumulative
    context window usage (sum of all input token fields).

    Example:
        >>> reader = JsonlTranscriptReader()
        >>> tokens = reader.read_latest_tokens("/path/to/transcript.jsonl")
        >>> print(f"Current context usage: {tokens}")
    """

    def read_latest_tokens(self, transcript_path: str) -> int:
        """Read cumulative context window usage from the latest assistant entry.

        Scans the JSONL file backward to find the last entry with
        ``message.usage`` data and returns the sum of ``input_tokens``,
        ``cache_creation_input_tokens``, and ``cache_read_input_tokens``.

        Args:
            transcript_path: Path to the JSONL transcript file.

        Returns:
            The cumulative context window token count.

        Raises:
            FileNotFoundError: If the transcript file does not exist.
            ValueError: If the file is empty, contains only whitespace,
                or has no entries with ``message.usage`` data.

        Example:
            >>> reader.read_latest_tokens("/path/to/transcript.jsonl")
            158119
        """
        if not os.path.exists(transcript_path):
            raise FileNotFoundError(
                f"Transcript file not found: {transcript_path}"
            )

        usage = self._find_latest_usage(transcript_path)

        if usage is None:
            raise ValueError(
                f"No entries with message.usage found in transcript: {transcript_path}"
            )

        return self._sum_context_tokens(usage)

    def _sum_context_tokens(self, usage: dict) -> int:
        """Sum all input token fields from a usage object.

        Computes: ``input_tokens + cache_creation_input_tokens + cache_read_input_tokens``.
        Missing cache fields default to 0.

        Args:
            usage: The ``message.usage`` dictionary from a Claude Code entry.

        Returns:
            The cumulative context window token count.
        """
        input_tokens = int(usage.get("input_tokens", 0))
        cache_creation = int(usage.get("cache_creation_input_tokens", 0))
        cache_read = int(usage.get("cache_read_input_tokens", 0))
        return input_tokens + cache_creation + cache_read

    def _extract_usage(self, line: str) -> dict | None:
        """Extract message.usage from a JSONL line if present.

        Args:
            line: A single JSONL line (already stripped).

        Returns:
            The usage dictionary if the entry has ``message.usage``,
            or None otherwise.
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

        # Must have at least input_tokens
        if "input_tokens" not in usage:
            return None

        return usage

    def _find_latest_usage(self, transcript_path: str) -> dict | None:
        """Scan backward through the transcript to find the last usage entry.

        Uses an efficient backward-seek strategy to read the file from
        the end, parsing lines in reverse order until an entry with
        ``message.usage`` is found.

        Args:
            transcript_path: Path to the JSONL transcript file.

        Returns:
            The ``message.usage`` dictionary from the last matching entry,
            or None if no matching entry is found.
        """
        with open(transcript_path, "rb") as fh:
            fh.seek(0, os.SEEK_END)
            file_size = fh.tell()

            if file_size == 0:
                return None

            accumulated: bytes = b""
            remaining = file_size
            processed_lines: int = 0

            while remaining > 0:
                block_size = min(_READ_BLOCK_SIZE, remaining)
                remaining -= block_size
                fh.seek(remaining)
                block = fh.read(block_size)
                accumulated = block + accumulated

                at_file_start = remaining == 0
                result = self._scan_accumulated_for_usage(
                    accumulated,
                    at_file_start=at_file_start,
                    already_processed=processed_lines,
                )

                if result is not None:
                    usage, new_processed = result
                    if usage is not None:
                        return usage
                    processed_lines = new_processed

        return None

    def _scan_accumulated_for_usage(
        self,
        data: bytes,
        *,
        at_file_start: bool,
        already_processed: int,
    ) -> tuple[dict | None, int] | None:
        """Scan accumulated bytes for usage entries, from end to start.

        Args:
            data: Raw bytes accumulated from backward reading.
            at_file_start: True if buffer includes the first byte of the file.
            already_processed: Number of lines already checked in prior calls.

        Returns:
            A tuple of (usage_dict_or_None, total_lines_processed) if new
            complete lines are available, or None if more data is needed.
        """
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            text = data.decode("utf-8", errors="replace")

        lines = text.splitlines()
        total_lines = len(lines)

        # Determine how many lines are complete (can be checked)
        # lines[0] may be a partial fragment unless at file start
        first_complete = 0 if at_file_start else 1

        # Only check lines we haven't processed yet
        # Lines are indexed 0..N-1, we process from end backward
        # already_processed lines from the end have been checked
        end_idx = total_lines - already_processed - 1
        start_idx = first_complete

        if end_idx < start_idx:
            return None  # No new complete lines to check

        for i in range(end_idx, start_idx - 1, -1):
            stripped = lines[i].strip()
            if not stripped:
                continue
            usage = self._extract_usage(stripped)
            if usage is not None:
                return (usage, total_lines - first_complete)

        # No usage found in new complete lines
        return (None, total_lines - first_complete)
