"""
TokenCounter Service.

Provides token counting functionality using tiktoken library.
Used by TranscriptChunker to ensure chunks fit within Claude Code's Read tool limit.

Reference: EN-026 (Token-Based Chunking), BUG-001 fix
Design Decision: DEC-001 D-004 (TokenCounter as separate injectable service)

Location: src/transcript/application/services/token_counter.py
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

import tiktoken

if TYPE_CHECKING:
    from src.transcript.domain.value_objects.parsed_segment import ParsedSegment


class TokenCounter:
    """Service for counting tokens using tiktoken.

    Wraps tiktoken library to provide consistent token counting for
    transcript chunking. Uses p50k_base encoding by default as the best
    approximation for Claude tokenization (per research in EN-026).

    Attributes:
        encoding_name: Name of the tiktoken encoding being used.

    Example:
        >>> counter = TokenCounter()
        >>> counter.count_tokens("hello world")
        2
        >>> segment = ParsedSegment(id="1", start_ms=0, end_ms=1000,
        ...                         speaker="Alice", text="Hello",
        ...                         raw_text="<v Alice>Hello</v>")
        >>> counter.count_segment_tokens(segment)
        45  # Includes JSON structure overhead

    Reference:
        - Claude Code Read limit: 25,000 tokens (GitHub Issue #4002)
        - Target per chunk: 18,000 tokens (25% safety margin)
        - Encoding: p50k_base (best Claude approximation)
    """

    def __init__(self, encoding_name: str = "p50k_base") -> None:
        """Initialize TokenCounter with specified encoding.

        Args:
            encoding_name: Name of tiktoken encoding. Default is 'p50k_base'
                          which is the best approximation for Claude tokenization.

        Raises:
            KeyError: If encoding_name is not a valid tiktoken encoding.
        """
        self._encoding_name = encoding_name
        # Cache encoding instance for efficiency (per TASK-261 AC)
        self._encoding = tiktoken.get_encoding(encoding_name)

    @property
    def encoding_name(self) -> str:
        """Return the name of the encoding being used."""
        return self._encoding_name

    def count_tokens(self, text: str) -> int:
        """Count tokens in plain text.

        Args:
            text: The text to count tokens for.

        Returns:
            Number of tokens in the text.

        Example:
            >>> counter = TokenCounter()
            >>> counter.count_tokens("hello world")
            2
        """
        if not text:
            return 0
        return len(self._encoding.encode(text))

    def count_segment_tokens(self, segment: ParsedSegment) -> int:
        """Count tokens for a segment including JSON serialization overhead.

        This method accounts for the full JSON structure that will be
        written to chunk files, not just the text content.

        Args:
            segment: ParsedSegment value object to count tokens for.

        Returns:
            Number of tokens including JSON structure overhead.

        Note:
            The JSON structure includes keys like 'id', 'start_ms', 'end_ms',
            'speaker', 'text', 'raw_text' plus JSON syntax characters.
            This overhead is significant and must be counted for accurate
            chunk sizing.
        """
        # Serialize segment to JSON (same format as chunker uses)
        segment_dict = {
            "id": segment.id,
            "start_ms": segment.start_ms,
            "end_ms": segment.end_ms,
            "speaker": segment.speaker,
            "text": segment.text,
            "raw_text": segment.raw_text,
        }
        json_str = json.dumps(segment_dict)
        return self.count_tokens(json_str)
