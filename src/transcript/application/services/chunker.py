"""
TranscriptChunker Service.

Implements Option D chunking strategy: index + chunk files for LLM-efficient processing.
Addresses "Lost-in-the-Middle" problem by enabling selective chunk loading.

v2.1 (EN-026): Added token-based chunking to fix BUG-001 (chunk token overflow).
- Token-based: Uses TokenCounter to ensure chunks fit within Claude Code Read limit
- Segment-based: Legacy mode, deprecated but maintained for backward compatibility

Reference: EN-021-chunking-strategy.md, TDD-FEAT-004 Section 5, EN-026
Location: src/transcript/application/services/chunker.py
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Iterator

from src.transcript.domain.value_objects.parsed_segment import ParsedSegment

# Module logger for deprecation warnings
logger = logging.getLogger(__name__)


class TranscriptChunker:
    """Splits transcript segments into LLM-efficient chunks.

    Creates an index file with metadata and pointers to chunk files,
    enabling agents to request specific chunks instead of loading
    the entire transcript.

    Supports two chunking strategies:
    1. Token-based (recommended): Chunks by target token count for Claude Code
    2. Segment-based (deprecated): Chunks by segment count (legacy)

    Attributes:
        chunk_size: Number of segments per chunk (legacy)
        target_tokens: Target tokens per chunk (recommended)

    Example (recommended - token-based):
        >>> chunker = TranscriptChunker(target_tokens=18000)
        >>> index_path = chunker.chunk(segments, "/output/dir")

    Example (legacy - segment-based):
        >>> chunker = TranscriptChunker(chunk_size=500)  # Deprecated
        >>> index_path = chunker.chunk(segments, "/output/dir")

    Reference:
        - EN-021-chunking-strategy.md
        - EN-026 (Token-Based Chunking, BUG-001 fix)
        - Claude Code Read limit: 25,000 tokens (GitHub Issue #4002)
    """

    def __init__(
        self,
        chunk_size: int = 500,
        target_tokens: int | None = None,
        token_counter: "TokenCounter | None" = None,
    ) -> None:
        """Initialize chunker with segment or token-based strategy.

        Args:
            chunk_size: Number of segments per chunk (legacy, deprecated if
                       target_tokens not provided). Must be positive.
            target_tokens: Target tokens per chunk (recommended). When provided,
                          uses token-based chunking and ignores chunk_size.
                          Default when used: 18,000 (25% margin from 25K limit).
            token_counter: Injected TokenCounter instance. Created internally
                          if not provided when target_tokens is set.

        Raises:
            ValueError: If chunk_size is not positive.

        Note:
            Using chunk_size without target_tokens is deprecated and will log
            a warning. Migrate to token-based chunking for reliable Claude Code
            compatibility.
        """
        if chunk_size <= 0:
            raise ValueError(f"chunk_size must be positive, got {chunk_size}")

        self._chunk_size = chunk_size
        self._target_tokens = target_tokens
        self._token_counter = token_counter

        # Create TokenCounter internally if needed but not provided
        if target_tokens is not None and token_counter is None:
            from src.transcript.application.services.token_counter import TokenCounter
            self._token_counter = TokenCounter()

        # Log deprecation warning for segment-based chunking
        if target_tokens is None:
            logger.warning(
                "TranscriptChunker: Using segment-based chunking (chunk_size=%d) is "
                "deprecated. Migrate to token-based chunking with target_tokens=18000 "
                "for reliable Claude Code compatibility. See EN-026 for details.",
                chunk_size,
            )

    @property
    def chunk_size(self) -> int:
        """Return the configured chunk size (segment-based)."""
        return self._chunk_size

    @property
    def target_tokens(self) -> int | None:
        """Return the configured target tokens (token-based)."""
        return self._target_tokens

    def chunk(self, segments: list[ParsedSegment], output_dir: str) -> str:
        """Create index and chunk files from segments.

        Args:
            segments: List of ParsedSegment value objects to chunk.
            output_dir: Directory path for output files.

        Returns:
            Path to the generated index.json file.

        Raises:
            ValueError: If segments list is empty.
        """
        if not segments:
            raise ValueError("Cannot chunk empty segments list")

        output_path = Path(output_dir)
        chunks_dir = output_path / "chunks"
        chunks_dir.mkdir(parents=True, exist_ok=True)

        # Collect chunk metadata while writing chunk files
        chunk_metadata: list[dict[str, Any]] = []
        chunk_list = list(self._split_segments(segments))
        total_chunks = len(chunk_list)

        for chunk_index, chunk_segments in enumerate(chunk_list):
            chunk_num = chunk_index + 1
            chunk_id = f"chunk-{chunk_num:03d}"
            chunk_file = chunks_dir / f"{chunk_id}.json"

            # Calculate navigation
            prev_chunk = f"chunk-{chunk_num - 1:03d}.json" if chunk_num > 1 else None
            next_chunk = (
                f"chunk-{chunk_num + 1:03d}.json" if chunk_num < total_chunks else None
            )

            # Build chunk data
            chunk_data = self._create_chunk_data(
                chunk_id=chunk_id,
                segments=chunk_segments,
                previous=prev_chunk,
                next=next_chunk,
            )

            # Write chunk file
            chunk_file.write_text(json.dumps(chunk_data, indent=2))

            # Collect metadata for index
            chunk_metadata.append(
                self._create_chunk_metadata(
                    chunk_id=chunk_id,
                    segments=chunk_segments,
                    file_path=f"chunks/{chunk_id}.json",
                )
            )

        # Build and write index
        index_data = self._create_index_data(
            segments=segments,
            chunk_metadata=chunk_metadata,
        )
        index_file = output_path / "index.json"
        index_file.write_text(json.dumps(index_data, indent=2))

        return str(index_file)

    def _split_segments(
        self, segments: list[ParsedSegment]
    ) -> Iterator[list[ParsedSegment]]:
        """Yield batches of segments according to chunking strategy.

        Uses token-based splitting if target_tokens is set,
        otherwise falls back to segment-based splitting.

        Args:
            segments: Full list of segments to split.

        Yields:
            Batches of segments according to configured strategy.
        """
        if self._target_tokens is not None:
            # Token-based chunking (recommended)
            yield from self._split_by_tokens(segments)
        else:
            # Segment-based chunking (legacy)
            yield from self._split_by_count(segments)

    def _split_by_count(
        self, segments: list[ParsedSegment]
    ) -> Iterator[list[ParsedSegment]]:
        """Yield batches of segments by count (legacy segment-based).

        Args:
            segments: Full list of segments to split.

        Yields:
            Batches of segments, each with at most chunk_size items.
        """
        for i in range(0, len(segments), self._chunk_size):
            yield segments[i : i + self._chunk_size]

    def _split_by_tokens(
        self, segments: list[ParsedSegment]
    ) -> Iterator[list[ParsedSegment]]:
        """Yield batches of segments by token count.

        Accumulates segments until adding the next would exceed target_tokens,
        then yields the current batch and starts a new one.

        Args:
            segments: Full list of segments to split.

        Yields:
            Batches of segments, each with tokens <= target_tokens.
        """
        assert self._token_counter is not None
        assert self._target_tokens is not None

        current_batch: list[ParsedSegment] = []
        current_tokens = 0

        for segment in segments:
            segment_tokens = self._token_counter.count_segment_tokens(segment)

            # Check if adding this segment would exceed limit
            if current_tokens + segment_tokens > self._target_tokens and current_batch:
                # Yield current batch and start new one
                yield current_batch
                current_batch = [segment]
                current_tokens = segment_tokens
            else:
                # Add to current batch
                current_batch.append(segment)
                current_tokens += segment_tokens

        # Yield final batch if non-empty
        if current_batch:
            yield current_batch

    def _create_chunk_data(
        self,
        chunk_id: str,
        segments: list[ParsedSegment],
        previous: str | None,
        next: str | None,
    ) -> dict[str, Any]:
        """Create chunk file data structure.

        Args:
            chunk_id: Unique chunk identifier.
            segments: Segments in this chunk.
            previous: Previous chunk filename or None.
            next: Next chunk filename or None.

        Returns:
            Dictionary conforming to chunk.schema.json.
        """
        first_seg = segments[0]
        last_seg = segments[-1]

        return {
            "chunk_id": chunk_id,
            "schema_version": "1.0",
            "segment_range": [int(first_seg.id), int(last_seg.id)],
            "timestamp_range": {
                "start_ms": first_seg.start_ms,
                "end_ms": last_seg.end_ms,
            },
            "segments": [self._segment_to_dict(seg) for seg in segments],
            "navigation": {
                "previous": previous,
                "next": next,
                "index": "../index.json",
            },
        }

    def _create_chunk_metadata(
        self,
        chunk_id: str,
        segments: list[ParsedSegment],
        file_path: str,
    ) -> dict[str, Any]:
        """Create chunk metadata for the index file.

        Args:
            chunk_id: Unique chunk identifier.
            segments: Segments in this chunk.
            file_path: Relative path to chunk file.

        Returns:
            Dictionary for index.chunks array.
        """
        first_seg = segments[0]
        last_seg = segments[-1]

        # Count speakers in this chunk
        speaker_counts: dict[str, int] = {}
        word_count = 0
        for seg in segments:
            if seg.speaker:
                speaker_counts[seg.speaker] = speaker_counts.get(seg.speaker, 0) + 1
            word_count += len(seg.text.split())

        return {
            "chunk_id": chunk_id,
            "segment_range": [int(first_seg.id), int(last_seg.id)],
            "timestamp_range": {
                "start_ms": first_seg.start_ms,
                "end_ms": last_seg.end_ms,
            },
            "speaker_counts": speaker_counts,
            "word_count": word_count,
            "file": file_path,
        }

    def _create_index_data(
        self,
        segments: list[ParsedSegment],
        chunk_metadata: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Create index file data structure.

        Args:
            segments: Full list of all segments.
            chunk_metadata: Metadata for each chunk.

        Returns:
            Dictionary conforming to index.schema.json.
        """
        # Collect unique speakers and their counts
        speaker_counts: dict[str, int] = {}
        for seg in segments:
            if seg.speaker:
                speaker_counts[seg.speaker] = speaker_counts.get(seg.speaker, 0) + 1

        speakers_list = sorted(speaker_counts.keys())
        total_duration = segments[-1].end_ms if segments else 0

        index_data: dict[str, Any] = {
            "schema_version": "1.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_segments": len(segments),
            "total_chunks": len(chunk_metadata),
            "chunk_size": self._chunk_size,
            "duration_ms": total_duration,
            "speakers": {
                "count": len(speakers_list),
                "list": speakers_list,
                "segment_counts": speaker_counts,
            },
            "chunks": chunk_metadata,
        }

        # Include target_tokens if token-based chunking was used
        if self._target_tokens is not None:
            index_data["target_tokens"] = self._target_tokens

        return index_data

    def _segment_to_dict(self, segment: ParsedSegment) -> dict[str, Any]:
        """Convert ParsedSegment to dictionary for JSON serialization.

        Args:
            segment: ParsedSegment value object.

        Returns:
            Dictionary representation compatible with chunk.schema.json.
        """
        return {
            "id": segment.id,
            "start_ms": segment.start_ms,
            "end_ms": segment.end_ms,
            "speaker": segment.speaker,
            "text": segment.text,
            "raw_text": segment.raw_text,
        }


# Type hint for optional import
if TYPE_CHECKING:
    from src.transcript.application.services.token_counter import TokenCounter
