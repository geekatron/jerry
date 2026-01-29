"""Integration tests for VTTParser → TranscriptChunker pipeline.

Tests validate data integrity, speaker preservation, and timestamp continuity
between the parser (EN-020) and chunker (EN-021) components.

Reference: TASK-231, EN-023 Integration Testing
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Generator

import pytest

from src.transcript.application.services.chunker import TranscriptChunker
from src.transcript.infrastructure.adapters.vtt_parser import VTTParser


@pytest.mark.integration
class TestParserChunkerIntegration:
    """Integration tests for Parser → Chunker pipeline.

    Tests verify:
    - AC-1: Zero segment loss in handoff
    - AC-2: Speaker count preservation
    - AC-3: Timestamp continuity across chunks
    - AC-4: meeting-006 produces expected chunk count
    - AC-5: Tests run with pytest -m integration
    """

    @pytest.fixture
    def parser(self) -> VTTParser:
        """Create VTTParser instance."""
        return VTTParser()

    @pytest.fixture
    def chunker(self) -> TranscriptChunker:
        """Create TranscriptChunker instance with default chunk size (500)."""
        return TranscriptChunker()

    @pytest.fixture
    def golden_datasets_dir(self) -> Path:
        """Path to golden transcript datasets."""
        return Path("skills/transcript/test_data/transcripts/golden")

    @pytest.fixture
    def temp_output_dir(self, tmp_path: Path) -> Generator[Path, None, None]:
        """Temporary directory for test outputs."""
        output = tmp_path / "integration_output"
        output.mkdir(parents=True, exist_ok=True)
        yield output

    # =========================================================================
    # AC-1: Zero Segment Loss Tests
    # =========================================================================

    def test_zero_segment_loss_meeting_006(
        self,
        parser: VTTParser,
        chunker: TranscriptChunker,
        golden_datasets_dir: Path,
        temp_output_dir: Path,
    ) -> None:
        """Verify no segments are lost in parser → chunker handoff for meeting-006.

        AC-1: Zero segment loss in parser → chunker handoff (all 6 datasets)
        Primary test for the largest dataset (~90K tokens, 3071 segments).
        """
        vtt_path = golden_datasets_dir / "meeting-006-all-hands.vtt"
        if not vtt_path.exists():
            pytest.skip(f"Golden dataset not found: {vtt_path}")

        # Parse VTT file
        parse_result = parser.parse(str(vtt_path))
        original_count = parse_result.segment_count

        # Chunk the segments
        output_dir = temp_output_dir / "meeting-006"
        output_dir.mkdir(parents=True, exist_ok=True)
        index_path = chunker.chunk(parse_result.segments, str(output_dir))

        # Load all chunks and count segments
        chunks_dir = output_dir / "chunks"
        total_segments = 0
        for chunk_file in sorted(chunks_dir.glob("chunk-*.json")):
            with open(chunk_file) as f:
                chunk_data = json.load(f)
            total_segments += len(chunk_data["segments"])

        # Verify zero segment loss
        assert total_segments == original_count, (
            f"Segment loss detected: original={original_count}, after_chunk={total_segments}"
        )
        # Verify known count for meeting-006
        assert total_segments == 3071, (
            f"Expected 3071 segments for meeting-006, got {total_segments}"
        )

    @pytest.mark.parametrize(
        "dataset",
        [
            "meeting-001.vtt",
            "meeting-002.vtt",
            "meeting-003.vtt",
            "meeting-004-sprint-planning.vtt",
            "meeting-005-roadmap-review.vtt",
            "meeting-006-all-hands.vtt",
        ],
    )
    def test_zero_segment_loss_all_datasets(
        self,
        parser: VTTParser,
        chunker: TranscriptChunker,
        golden_datasets_dir: Path,
        temp_output_dir: Path,
        dataset: str,
    ) -> None:
        """Verify zero segment loss for all golden datasets.

        AC-1: Zero segment loss in parser → chunker handoff (all 6 datasets)
        """
        vtt_path = golden_datasets_dir / dataset
        if not vtt_path.exists():
            pytest.skip(f"Dataset not found: {vtt_path}")

        # Parse VTT file
        parse_result = parser.parse(str(vtt_path))
        original_count = parse_result.segment_count

        # Chunk the segments
        output_dir = temp_output_dir / dataset.replace(".vtt", "")
        output_dir.mkdir(parents=True, exist_ok=True)
        index_path = chunker.chunk(parse_result.segments, str(output_dir))

        # Load index and verify via metadata
        with open(index_path) as f:
            index_data = json.load(f)

        assert index_data["total_segments"] == original_count, (
            f"Index reports different segment count for {dataset}: "
            f"parser={original_count}, index={index_data['total_segments']}"
        )

        # Also verify by counting segments in all chunks
        chunks_dir = output_dir / "chunks"
        chunk_segment_count = 0
        for chunk_file in sorted(chunks_dir.glob("chunk-*.json")):
            with open(chunk_file) as f:
                chunk_data = json.load(f)
            chunk_segment_count += len(chunk_data["segments"])

        assert chunk_segment_count == original_count, (
            f"Segment loss in {dataset}: "
            f"original={original_count}, in_chunks={chunk_segment_count}"
        )

    # =========================================================================
    # AC-2: Speaker Count Preservation Tests
    # =========================================================================

    def test_speaker_count_preservation_meeting_006(
        self,
        parser: VTTParser,
        chunker: TranscriptChunker,
        golden_datasets_dir: Path,
        temp_output_dir: Path,
    ) -> None:
        """Verify speaker counts match between parser output and chunker index.

        AC-2: Speaker counts match between parser output and chunker index
        """
        vtt_path = golden_datasets_dir / "meeting-006-all-hands.vtt"
        if not vtt_path.exists():
            pytest.skip(f"Golden dataset not found: {vtt_path}")

        # Parse VTT file
        parse_result = parser.parse(str(vtt_path))
        parser_speakers = set(parse_result.speakers)

        # Chunk the segments
        output_dir = temp_output_dir / "speaker-test"
        output_dir.mkdir(parents=True, exist_ok=True)
        index_path = chunker.chunk(parse_result.segments, str(output_dir))

        # Load index and compare speakers
        with open(index_path) as f:
            index_data = json.load(f)

        chunker_speakers = set(index_data["speakers"]["list"])

        assert chunker_speakers == parser_speakers, (
            f"Speaker mismatch: parser={parser_speakers}, chunker={chunker_speakers}"
        )

        # Also verify speaker count
        assert index_data["speakers"]["count"] == len(parser_speakers), (
            f"Speaker count mismatch: "
            f"parser={len(parser_speakers)}, index={index_data['speakers']['count']}"
        )

    @pytest.mark.parametrize(
        "dataset",
        [
            "meeting-001.vtt",
            "meeting-002.vtt",
            "meeting-003.vtt",
            "meeting-004-sprint-planning.vtt",
            "meeting-005-roadmap-review.vtt",
        ],
    )
    def test_speaker_preservation_all_datasets(
        self,
        parser: VTTParser,
        chunker: TranscriptChunker,
        golden_datasets_dir: Path,
        temp_output_dir: Path,
        dataset: str,
    ) -> None:
        """Verify speaker lists match for all smaller datasets.

        AC-2: Speaker counts match between parser output and chunker index
        """
        vtt_path = golden_datasets_dir / dataset
        if not vtt_path.exists():
            pytest.skip(f"Dataset not found: {vtt_path}")

        # Parse and chunk
        parse_result = parser.parse(str(vtt_path))
        parser_speakers = set(parse_result.speakers)

        output_dir = temp_output_dir / dataset.replace(".vtt", "")
        output_dir.mkdir(parents=True, exist_ok=True)
        index_path = chunker.chunk(parse_result.segments, str(output_dir))

        with open(index_path) as f:
            index_data = json.load(f)

        chunker_speakers = set(index_data["speakers"]["list"])

        assert chunker_speakers == parser_speakers, (
            f"Speaker mismatch in {dataset}"
        )

    # =========================================================================
    # AC-3: Timestamp Continuity Tests
    # =========================================================================

    def test_timestamp_continuity_meeting_006(
        self,
        parser: VTTParser,
        chunker: TranscriptChunker,
        golden_datasets_dir: Path,
        temp_output_dir: Path,
    ) -> None:
        """Verify timestamps are continuous across chunk boundaries.

        AC-3: Timestamps are continuous across chunk boundaries

        For each chunk transition, the first segment of chunk N+1 should
        have a start_ms >= the end_ms of the last segment in chunk N.
        """
        vtt_path = golden_datasets_dir / "meeting-006-all-hands.vtt"
        if not vtt_path.exists():
            pytest.skip(f"Golden dataset not found: {vtt_path}")

        # Parse and chunk
        parse_result = parser.parse(str(vtt_path))
        output_dir = temp_output_dir / "timestamp-test"
        output_dir.mkdir(parents=True, exist_ok=True)
        chunker.chunk(parse_result.segments, str(output_dir))

        # Check timestamp continuity across chunks
        chunks_dir = output_dir / "chunks"
        chunk_files = sorted(chunks_dir.glob("chunk-*.json"))

        prev_end_ms = 0
        for chunk_file in chunk_files:
            with open(chunk_file) as f:
                chunk_data = json.load(f)

            segments = chunk_data["segments"]
            first_segment = segments[0]
            last_segment = segments[-1]

            # First segment should start at or after previous chunk's last segment end
            assert first_segment["start_ms"] >= prev_end_ms, (
                f"Timestamp discontinuity at {chunk_file.name}: "
                f"first_start_ms={first_segment['start_ms']} < prev_end_ms={prev_end_ms}"
            )

            # Update prev_end_ms for next iteration
            prev_end_ms = last_segment["end_ms"]

    def test_timestamp_ordering_within_chunks(
        self,
        parser: VTTParser,
        chunker: TranscriptChunker,
        golden_datasets_dir: Path,
        temp_output_dir: Path,
    ) -> None:
        """Verify timestamps are strictly ordered within each chunk.

        AC-3 (supplementary): Timestamps should be monotonically increasing
        within each chunk.
        """
        vtt_path = golden_datasets_dir / "meeting-006-all-hands.vtt"
        if not vtt_path.exists():
            pytest.skip(f"Golden dataset not found: {vtt_path}")

        # Parse and chunk
        parse_result = parser.parse(str(vtt_path))
        output_dir = temp_output_dir / "ordering-test"
        output_dir.mkdir(parents=True, exist_ok=True)
        chunker.chunk(parse_result.segments, str(output_dir))

        # Check ordering within each chunk
        chunks_dir = output_dir / "chunks"
        for chunk_file in sorted(chunks_dir.glob("chunk-*.json")):
            with open(chunk_file) as f:
                chunk_data = json.load(f)

            segments = chunk_data["segments"]
            for i in range(1, len(segments)):
                prev_seg = segments[i - 1]
                curr_seg = segments[i]

                assert curr_seg["start_ms"] >= prev_seg["start_ms"], (
                    f"Timestamp ordering violation in {chunk_file.name}: "
                    f"segment {i-1} start_ms={prev_seg['start_ms']} > "
                    f"segment {i} start_ms={curr_seg['start_ms']}"
                )

    # =========================================================================
    # AC-4: meeting-006 Chunk Count Test
    # =========================================================================

    def test_meeting_006_produces_seven_chunks(
        self,
        parser: VTTParser,
        chunker: TranscriptChunker,
        golden_datasets_dir: Path,
        temp_output_dir: Path,
    ) -> None:
        """Verify meeting-006 (3,071 segments) produces exactly 7 chunks.

        AC-4: meeting-006 (3,071 segments) processes correctly into 7 chunks

        With default chunk_size=500:
        - Chunks 1-6: 500 segments each = 3000 segments
        - Chunk 7: 71 remaining segments
        - Total: 7 chunks for 3071 segments
        """
        vtt_path = golden_datasets_dir / "meeting-006-all-hands.vtt"
        if not vtt_path.exists():
            pytest.skip(f"Golden dataset not found: {vtt_path}")

        # Parse and chunk
        parse_result = parser.parse(str(vtt_path))
        output_dir = temp_output_dir / "chunk-count-test"
        output_dir.mkdir(parents=True, exist_ok=True)
        index_path = chunker.chunk(parse_result.segments, str(output_dir))

        # Load index and verify chunk count
        with open(index_path) as f:
            index_data = json.load(f)

        assert index_data["total_chunks"] == 7, (
            f"Expected 7 chunks for meeting-006, got {index_data['total_chunks']}"
        )

        # Also verify by counting actual chunk files
        chunks_dir = output_dir / "chunks"
        chunk_files = list(chunks_dir.glob("chunk-*.json"))
        assert len(chunk_files) == 7, (
            f"Expected 7 chunk files, found {len(chunk_files)}"
        )

    @pytest.mark.parametrize(
        "dataset,expected_chunks",
        [
            # Actual segment counts verified: 39, 97, 62, 536, 896, 3071
            # With chunk_size=500: ceil(segments/500) = expected_chunks
            ("meeting-001.vtt", 1),   # 39 segments → 1 chunk
            ("meeting-002.vtt", 1),   # 97 segments → 1 chunk
            ("meeting-003.vtt", 1),   # 62 segments → 1 chunk
            ("meeting-004-sprint-planning.vtt", 2),   # 536 segments → 2 chunks
            ("meeting-005-roadmap-review.vtt", 2),    # 896 segments → 2 chunks
            ("meeting-006-all-hands.vtt", 7),         # 3071 segments → 7 chunks
        ],
    )
    def test_all_datasets_produce_expected_chunks(
        self,
        parser: VTTParser,
        chunker: TranscriptChunker,
        golden_datasets_dir: Path,
        temp_output_dir: Path,
        dataset: str,
        expected_chunks: int,
    ) -> None:
        """Verify all datasets produce expected chunk counts.

        AC-4 (supplementary): Test chunk counts for all golden datasets.
        """
        vtt_path = golden_datasets_dir / dataset
        if not vtt_path.exists():
            pytest.skip(f"Dataset not found: {vtt_path}")

        # Parse and chunk
        parse_result = parser.parse(str(vtt_path))
        output_dir = temp_output_dir / dataset.replace(".vtt", "")
        output_dir.mkdir(parents=True, exist_ok=True)
        index_path = chunker.chunk(parse_result.segments, str(output_dir))

        with open(index_path) as f:
            index_data = json.load(f)

        assert index_data["total_chunks"] == expected_chunks, (
            f"Expected {expected_chunks} chunks for {dataset}, "
            f"got {index_data['total_chunks']}"
        )

    # =========================================================================
    # Supplementary Data Integrity Tests
    # =========================================================================

    def test_chunk_navigation_links(
        self,
        parser: VTTParser,
        chunker: TranscriptChunker,
        golden_datasets_dir: Path,
        temp_output_dir: Path,
    ) -> None:
        """Verify chunk navigation links are correct."""
        vtt_path = golden_datasets_dir / "meeting-006-all-hands.vtt"
        if not vtt_path.exists():
            pytest.skip(f"Golden dataset not found: {vtt_path}")

        # Parse and chunk
        parse_result = parser.parse(str(vtt_path))
        output_dir = temp_output_dir / "navigation-test"
        output_dir.mkdir(parents=True, exist_ok=True)
        chunker.chunk(parse_result.segments, str(output_dir))

        chunks_dir = output_dir / "chunks"
        chunk_files = sorted(chunks_dir.glob("chunk-*.json"))
        total_chunks = len(chunk_files)

        for i, chunk_file in enumerate(chunk_files):
            with open(chunk_file) as f:
                chunk_data = json.load(f)

            nav = chunk_data["navigation"]

            # First chunk has no previous
            if i == 0:
                assert nav["previous"] is None, (
                    f"First chunk should have no previous link"
                )
            else:
                expected_prev = f"chunk-{i:03d}.json"
                assert nav["previous"] == expected_prev, (
                    f"Chunk {i+1} has wrong previous link"
                )

            # Last chunk has no next
            if i == total_chunks - 1:
                assert nav["next"] is None, (
                    f"Last chunk should have no next link"
                )
            else:
                expected_next = f"chunk-{i+2:03d}.json"
                assert nav["next"] == expected_next, (
                    f"Chunk {i+1} has wrong next link"
                )

    def test_segment_ids_are_sequential(
        self,
        parser: VTTParser,
        chunker: TranscriptChunker,
        golden_datasets_dir: Path,
        temp_output_dir: Path,
    ) -> None:
        """Verify segment IDs are sequential across all chunks."""
        vtt_path = golden_datasets_dir / "meeting-006-all-hands.vtt"
        if not vtt_path.exists():
            pytest.skip(f"Golden dataset not found: {vtt_path}")

        # Parse and chunk
        parse_result = parser.parse(str(vtt_path))
        output_dir = temp_output_dir / "seq-id-test"
        output_dir.mkdir(parents=True, exist_ok=True)
        chunker.chunk(parse_result.segments, str(output_dir))

        chunks_dir = output_dir / "chunks"
        expected_id = 1

        for chunk_file in sorted(chunks_dir.glob("chunk-*.json")):
            with open(chunk_file) as f:
                chunk_data = json.load(f)

            for seg in chunk_data["segments"]:
                assert int(seg["id"]) == expected_id, (
                    f"Expected segment ID {expected_id}, got {seg['id']}"
                )
                expected_id += 1

        # Final check: should have seen all 3071 segments
        assert expected_id == 3072, (
            f"Expected to process 3071 segments, stopped at {expected_id - 1}"
        )
