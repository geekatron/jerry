"""
TranscriptChunker Service.

Implements Option D chunking strategy: index + chunk files for LLM-efficient processing.
Addresses "Lost-in-the-Middle" problem by enabling selective chunk loading.

Reference: EN-021-chunking-strategy.md, TDD-FEAT-004 Section 5
Location: src/transcript/application/services/chunker.py
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Iterator

from src.transcript.domain.value_objects.parsed_segment import ParsedSegment


class TranscriptChunker:
    """Splits transcript segments into LLM-efficient chunks.

    Creates an index file with metadata and pointers to chunk files,
    enabling agents to request specific chunks instead of loading
    the entire transcript.

    Attributes:
        chunk_size: Number of segments per chunk (default: 500)

    Example:
        >>> chunker = TranscriptChunker(chunk_size=500)
        >>> index_path = chunker.chunk(segments, "/output/dir")
        >>> print(index_path)  # /output/dir/index.json

    Reference: EN-021-chunking-strategy.md, TDD-FEAT-004 Section 5
    """

    def __init__(self, chunk_size: int = 500) -> None:
        """Initialize chunker with specified chunk size.

        Args:
            chunk_size: Number of segments per chunk. Must be positive.

        Raises:
            ValueError: If chunk_size is not positive.
        """
        if chunk_size <= 0:
            raise ValueError(f"chunk_size must be positive, got {chunk_size}")
        self._chunk_size = chunk_size

    @property
    def chunk_size(self) -> int:
        """Return the configured chunk size."""
        return self._chunk_size

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
        """Yield batches of segments according to chunk_size.

        Args:
            segments: Full list of segments to split.

        Yields:
            Batches of segments, each with at most chunk_size items.
        """
        for i in range(0, len(segments), self._chunk_size):
            yield segments[i : i + self._chunk_size]

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

        return {
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
