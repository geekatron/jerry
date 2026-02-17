# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Integration tests for VTTParser → TranscriptChunker pipeline.

Tests validate data integrity, speaker preservation, and timestamp continuity
between the parser (EN-020) and chunker (EN-021) components.

Reference: TASK-231, EN-023 Integration Testing
"""

from __future__ import annotations

import json
from collections.abc import Generator
from pathlib import Path

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
        chunker.chunk(parse_result.segments, str(output_dir))

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
            f"Segment loss in {dataset}: original={original_count}, in_chunks={chunk_segment_count}"
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

        assert chunker_speakers == parser_speakers, f"Speaker mismatch in {dataset}"

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
                    f"segment {i - 1} start_ms={prev_seg['start_ms']} > "
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
        assert len(chunk_files) == 7, f"Expected 7 chunk files, found {len(chunk_files)}"

    @pytest.mark.parametrize(
        "dataset,expected_chunks",
        [
            # Actual segment counts verified: 39, 97, 62, 536, 896, 3071
            # With chunk_size=500: ceil(segments/500) = expected_chunks
            ("meeting-001.vtt", 1),  # 39 segments → 1 chunk
            ("meeting-002.vtt", 1),  # 97 segments → 1 chunk
            ("meeting-003.vtt", 1),  # 62 segments → 1 chunk
            ("meeting-004-sprint-planning.vtt", 2),  # 536 segments → 2 chunks
            ("meeting-005-roadmap-review.vtt", 2),  # 896 segments → 2 chunks
            ("meeting-006-all-hands.vtt", 7),  # 3071 segments → 7 chunks
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
            f"Expected {expected_chunks} chunks for {dataset}, got {index_data['total_chunks']}"
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
                assert nav["previous"] is None, "First chunk should have no previous link"
            else:
                expected_prev = f"chunk-{i:03d}.json"
                assert nav["previous"] == expected_prev, f"Chunk {i + 1} has wrong previous link"

            # Last chunk has no next
            if i == total_chunks - 1:
                assert nav["next"] is None, "Last chunk should have no next link"
            else:
                expected_next = f"chunk-{i + 2:03d}.json"
                assert nav["next"] == expected_next, f"Chunk {i + 1} has wrong next link"

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


# =============================================================================
# TOKEN-BASED CHUNKING INTEGRATION TESTS (EN-026, TASK-265)
# =============================================================================


@pytest.mark.integration
class TestTokenBasedChunkingIntegration:
    """Integration tests for token-based chunking with real VTT files.

    Tests verify:
    - AC-1: All chunks under target token limit (18K default)
    - AC-2: index.json contains target_tokens field
    - AC-3: Zero segment loss with token-based chunking
    - AC-4: Speaker preservation with token-based chunking
    - AC-5: Backward compatibility (segment-based mode with target_tokens=None)

    Reference: EN-026, TASK-265, DISC-001 (JSON overhead ~22%)
    """

    @pytest.fixture
    def parser(self) -> VTTParser:
        """Create VTTParser instance."""
        return VTTParser()

    @pytest.fixture
    def token_chunker(self) -> TranscriptChunker:
        """Create TranscriptChunker with token-based chunking (18K target)."""
        return TranscriptChunker(target_tokens=18000)

    @pytest.fixture
    def golden_datasets_dir(self) -> Path:
        """Path to golden transcript datasets."""
        return Path("skills/transcript/test_data/transcripts/golden")

    @pytest.fixture
    def temp_output_dir(self, tmp_path: Path) -> Generator[Path, None, None]:
        """Temporary directory for test outputs."""
        output = tmp_path / "token_based_output"
        output.mkdir(parents=True, exist_ok=True)
        yield output

    # =========================================================================
    # AC-1: Chunks Under Target Token Limit
    # =========================================================================

    def test_token_based_chunks_under_limit_meeting_006(
        self,
        parser: VTTParser,
        token_chunker: TranscriptChunker,
        golden_datasets_dir: Path,
        temp_output_dir: Path,
    ) -> None:
        """Verify all chunks are under target token limit for meeting-006.

        AC-1: All generated chunks under 18,000 tokens (raw content)
        Note: Serialized JSON will be ~22% larger per DISC-001.
        """
        from src.transcript.application.services.token_counter import TokenCounter

        vtt_path = golden_datasets_dir / "meeting-006-all-hands.vtt"
        if not vtt_path.exists():
            pytest.skip(f"Golden dataset not found: {vtt_path}")

        # Parse and chunk
        parse_result = parser.parse(str(vtt_path))
        output_dir = temp_output_dir / "token-limit-test"
        output_dir.mkdir(parents=True, exist_ok=True)
        token_chunker.chunk(parse_result.segments, str(output_dir))

        # Verify each chunk is under target
        token_counter = TokenCounter()
        chunks_dir = output_dir / "chunks"

        for chunk_file in sorted(chunks_dir.glob("chunk-*.json")):
            with open(chunk_file) as f:
                chunk_data = json.load(f)

            # Count tokens in segment text only (raw content)
            segment_text = " ".join(seg["text"] for seg in chunk_data["segments"])
            raw_tokens = token_counter.count_tokens(segment_text)

            # Raw content should be under 18,000 tokens
            assert raw_tokens <= 18000, (
                f"{chunk_file.name} raw content exceeds limit: {raw_tokens} tokens"
            )

    def test_token_based_serialized_chunks_under_read_limit(
        self,
        parser: VTTParser,
        token_chunker: TranscriptChunker,
        golden_datasets_dir: Path,
        temp_output_dir: Path,
    ) -> None:
        """Verify serialized JSON chunks are under Claude Code Read limit (25K).

        DISC-001: JSON serialization adds ~22% overhead.
        Target 18K raw → ~22K serialized → safely under 25K limit.
        """
        from src.transcript.application.services.token_counter import TokenCounter

        vtt_path = golden_datasets_dir / "meeting-006-all-hands.vtt"
        if not vtt_path.exists():
            pytest.skip(f"Golden dataset not found: {vtt_path}")

        # Parse and chunk
        parse_result = parser.parse(str(vtt_path))
        output_dir = temp_output_dir / "serialized-limit-test"
        output_dir.mkdir(parents=True, exist_ok=True)
        token_chunker.chunk(parse_result.segments, str(output_dir))

        # Verify each serialized chunk is under Claude Code Read limit
        token_counter = TokenCounter()
        chunks_dir = output_dir / "chunks"
        claude_code_read_limit = 25000

        for chunk_file in sorted(chunks_dir.glob("chunk-*.json")):
            # Read entire file and count tokens
            file_content = chunk_file.read_text()
            total_tokens = token_counter.count_tokens(file_content)

            assert total_tokens <= claude_code_read_limit, (
                f"{chunk_file.name} exceeds Claude Code Read limit: "
                f"{total_tokens} > {claude_code_read_limit}"
            )

    # =========================================================================
    # AC-2: index.json Contains target_tokens Field
    # =========================================================================

    def test_token_based_index_contains_target_tokens(
        self,
        parser: VTTParser,
        token_chunker: TranscriptChunker,
        golden_datasets_dir: Path,
        temp_output_dir: Path,
    ) -> None:
        """Verify index.json contains target_tokens field.

        AC-2: index.json schema includes target_tokens field
        """
        vtt_path = golden_datasets_dir / "meeting-006-all-hands.vtt"
        if not vtt_path.exists():
            pytest.skip(f"Golden dataset not found: {vtt_path}")

        # Parse and chunk
        parse_result = parser.parse(str(vtt_path))
        output_dir = temp_output_dir / "target-tokens-field"
        output_dir.mkdir(parents=True, exist_ok=True)
        index_path = token_chunker.chunk(parse_result.segments, str(output_dir))

        # Load index and verify field
        with open(index_path) as f:
            index_data = json.load(f)

        assert "target_tokens" in index_data, "index.json missing 'target_tokens' field"
        assert index_data["target_tokens"] == 18000, (
            f"Expected target_tokens=18000, got {index_data['target_tokens']}"
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
    def test_token_based_all_datasets_have_target_tokens(
        self,
        parser: VTTParser,
        token_chunker: TranscriptChunker,
        golden_datasets_dir: Path,
        temp_output_dir: Path,
        dataset: str,
    ) -> None:
        """Verify target_tokens field present for all datasets."""
        vtt_path = golden_datasets_dir / dataset
        if not vtt_path.exists():
            pytest.skip(f"Dataset not found: {vtt_path}")

        # Parse and chunk
        parse_result = parser.parse(str(vtt_path))
        output_dir = temp_output_dir / dataset.replace(".vtt", "")
        output_dir.mkdir(parents=True, exist_ok=True)
        index_path = token_chunker.chunk(parse_result.segments, str(output_dir))

        with open(index_path) as f:
            index_data = json.load(f)

        assert "target_tokens" in index_data, f"{dataset}: index.json missing 'target_tokens' field"

    # =========================================================================
    # AC-3: Zero Segment Loss with Token-Based Chunking
    # =========================================================================

    def test_token_based_zero_segment_loss(
        self,
        parser: VTTParser,
        token_chunker: TranscriptChunker,
        golden_datasets_dir: Path,
        temp_output_dir: Path,
    ) -> None:
        """Verify zero segment loss with token-based chunking.

        AC-3: All segments preserved after token-based chunking.
        """
        vtt_path = golden_datasets_dir / "meeting-006-all-hands.vtt"
        if not vtt_path.exists():
            pytest.skip(f"Golden dataset not found: {vtt_path}")

        # Parse
        parse_result = parser.parse(str(vtt_path))
        original_count = parse_result.segment_count

        # Chunk with token-based
        output_dir = temp_output_dir / "zero-loss-token"
        output_dir.mkdir(parents=True, exist_ok=True)
        index_path = token_chunker.chunk(parse_result.segments, str(output_dir))

        # Verify via index
        with open(index_path) as f:
            index_data = json.load(f)

        assert index_data["total_segments"] == original_count, (
            f"Segment count mismatch in index: "
            f"parser={original_count}, index={index_data['total_segments']}"
        )

        # Verify by counting segments in all chunks
        chunks_dir = output_dir / "chunks"
        chunk_segment_count = 0
        for chunk_file in sorted(chunks_dir.glob("chunk-*.json")):
            with open(chunk_file) as f:
                chunk_data = json.load(f)
            chunk_segment_count += len(chunk_data["segments"])

        assert chunk_segment_count == original_count, (
            f"Segment loss with token-based chunking: "
            f"original={original_count}, in_chunks={chunk_segment_count}"
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
    def test_token_based_zero_segment_loss_all_datasets(
        self,
        parser: VTTParser,
        token_chunker: TranscriptChunker,
        golden_datasets_dir: Path,
        temp_output_dir: Path,
        dataset: str,
    ) -> None:
        """Verify zero segment loss for all datasets with token-based chunking."""
        vtt_path = golden_datasets_dir / dataset
        if not vtt_path.exists():
            pytest.skip(f"Dataset not found: {vtt_path}")

        # Parse and chunk
        parse_result = parser.parse(str(vtt_path))
        original_count = parse_result.segment_count

        output_dir = temp_output_dir / dataset.replace(".vtt", "")
        output_dir.mkdir(parents=True, exist_ok=True)
        token_chunker.chunk(parse_result.segments, str(output_dir))

        # Count segments in chunks
        chunks_dir = output_dir / "chunks"
        chunk_segment_count = 0
        for chunk_file in sorted(chunks_dir.glob("chunk-*.json")):
            with open(chunk_file) as f:
                chunk_data = json.load(f)
            chunk_segment_count += len(chunk_data["segments"])

        assert chunk_segment_count == original_count, (
            f"Segment loss in {dataset} with token-based: "
            f"original={original_count}, in_chunks={chunk_segment_count}"
        )

    # =========================================================================
    # AC-4: Speaker Preservation with Token-Based Chunking
    # =========================================================================

    def test_token_based_speaker_preservation(
        self,
        parser: VTTParser,
        token_chunker: TranscriptChunker,
        golden_datasets_dir: Path,
        temp_output_dir: Path,
    ) -> None:
        """Verify speaker counts preserved with token-based chunking.

        AC-4: Speaker metadata preserved correctly.
        """
        vtt_path = golden_datasets_dir / "meeting-006-all-hands.vtt"
        if not vtt_path.exists():
            pytest.skip(f"Golden dataset not found: {vtt_path}")

        # Parse
        parse_result = parser.parse(str(vtt_path))
        parser_speakers = set(parse_result.speakers)

        # Chunk with token-based
        output_dir = temp_output_dir / "speaker-token"
        output_dir.mkdir(parents=True, exist_ok=True)
        index_path = token_chunker.chunk(parse_result.segments, str(output_dir))

        # Verify speakers match
        with open(index_path) as f:
            index_data = json.load(f)

        chunker_speakers = set(index_data["speakers"]["list"])

        assert chunker_speakers == parser_speakers, "Speaker mismatch with token-based chunking"

    # =========================================================================
    # AC-5: Backward Compatibility (segment-based mode)
    # =========================================================================

    def test_segment_based_mode_still_works(
        self,
        parser: VTTParser,
        golden_datasets_dir: Path,
        temp_output_dir: Path,
    ) -> None:
        """Verify segment-based chunking still works with target_tokens=None.

        AC-5: Backward compatibility maintained.
        """
        vtt_path = golden_datasets_dir / "meeting-006-all-hands.vtt"
        if not vtt_path.exists():
            pytest.skip(f"Golden dataset not found: {vtt_path}")

        # Use segment-based chunker (no target_tokens)
        segment_chunker = TranscriptChunker(chunk_size=500, target_tokens=None)

        # Parse and chunk
        parse_result = parser.parse(str(vtt_path))
        output_dir = temp_output_dir / "segment-based"
        output_dir.mkdir(parents=True, exist_ok=True)
        index_path = segment_chunker.chunk(parse_result.segments, str(output_dir))

        # Verify segment-based behavior (7 chunks for 3071 segments)
        with open(index_path) as f:
            index_data = json.load(f)

        assert index_data["total_chunks"] == 7, (
            f"Expected 7 chunks with segment-based, got {index_data['total_chunks']}"
        )
        assert "target_tokens" not in index_data or index_data["target_tokens"] is None

    # =========================================================================
    # Supplementary: Token-Based Produces Fewer Chunks Than Segment-Based
    # =========================================================================

    def test_token_based_produces_different_chunk_count_than_segment_based(
        self,
        parser: VTTParser,
        golden_datasets_dir: Path,
        temp_output_dir: Path,
    ) -> None:
        """Token-based chunking produces different chunk count than segment-based.

        This demonstrates that token-based chunking is actually being used,
        not falling back to segment-based behavior.
        """
        vtt_path = golden_datasets_dir / "meeting-006-all-hands.vtt"
        if not vtt_path.exists():
            pytest.skip(f"Golden dataset not found: {vtt_path}")

        parse_result = parser.parse(str(vtt_path))

        # Segment-based
        segment_chunker = TranscriptChunker(chunk_size=500, target_tokens=None)
        segment_output = temp_output_dir / "compare-segment"
        segment_output.mkdir(parents=True, exist_ok=True)
        segment_index_path = segment_chunker.chunk(parse_result.segments, str(segment_output))

        with open(segment_index_path) as f:
            segment_index = json.load(f)

        # Token-based
        token_chunker = TranscriptChunker(target_tokens=18000)
        token_output = temp_output_dir / "compare-token"
        token_output.mkdir(parents=True, exist_ok=True)
        token_index_path = token_chunker.chunk(parse_result.segments, str(token_output))

        with open(token_index_path) as f:
            token_index = json.load(f)

        # They should produce different chunk counts
        # (meeting-006: segment-based=7 chunks, token-based should be different)
        segment_chunks = segment_index["total_chunks"]
        token_chunks = token_index["total_chunks"]

        # Token-based with 18K target should produce fewer chunks than segment-based
        # because 18K tokens can hold more than 500 short segments
        assert token_chunks != segment_chunks or (segment_chunks == 1 and token_chunks == 1), (
            f"Expected different chunk counts: "
            f"segment-based={segment_chunks}, token-based={token_chunks}"
        )
