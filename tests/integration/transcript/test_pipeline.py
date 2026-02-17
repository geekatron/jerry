# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""End-to-end Python pipeline integration tests.

Tests validate the complete Python layer pipeline:
VTT file → VTTParser → TranscriptChunker → index.json + chunks/

These tests are suitable for CI (no LLM invocation) and focus on:
- Full pipeline execution without error
- Performance thresholds
- Idempotency validation
- All golden datasets processing

Reference: TASK-233, EN-023 Integration Testing
"""

from __future__ import annotations

import json
import time
from collections.abc import Generator
from dataclasses import dataclass
from pathlib import Path

import pytest

from src.transcript.application.services.chunker import TranscriptChunker
from src.transcript.infrastructure.adapters.vtt_parser import VTTParser


@dataclass
class PipelineResult:
    """Results from a Python pipeline execution."""

    index_path: Path
    index_data: dict
    segment_count: int
    speaker_count: int
    chunk_count: int
    elapsed_seconds: float


@pytest.mark.integration
class TestPythonPipeline:
    """End-to-end tests for Python pipeline (no LLM).

    Tests verify:
    - AC-1: Full pipeline executes without error
    - AC-2: meeting-006 produces 7 chunks with 3,071 segments
    - AC-3: All golden datasets process within performance thresholds
    - AC-4: Pipeline is idempotent
    - AC-5: All datasets complete in < 30 seconds combined
    """

    @pytest.fixture
    def parser(self) -> VTTParser:
        """Create VTTParser instance."""
        return VTTParser()

    @pytest.fixture
    def chunker(self) -> TranscriptChunker:
        """Create TranscriptChunker instance with default chunk size."""
        return TranscriptChunker()

    @pytest.fixture
    def golden_datasets_dir(self) -> Path:
        """Path to golden transcript datasets."""
        return Path("skills/transcript/test_data/transcripts/golden")

    @pytest.fixture
    def temp_output_dir(self, tmp_path: Path) -> Generator[Path, None, None]:
        """Temporary directory for pipeline outputs."""
        output = tmp_path / "pipeline_output"
        output.mkdir(parents=True, exist_ok=True)
        yield output

    def run_pipeline(
        self,
        vtt_path: Path,
        output_dir: Path,
        parser: VTTParser,
        chunker: TranscriptChunker,
    ) -> PipelineResult:
        """Execute full Python pipeline and return structured results.

        Pipeline: VTT → Parse → Chunk → index.json + chunks/
        """
        start_time = time.time()

        # Step 1: Parse VTT
        parse_result = parser.parse(str(vtt_path))

        # Step 2: Chunk segments
        output_dir.mkdir(parents=True, exist_ok=True)
        index_path = chunker.chunk(parse_result.segments, str(output_dir))

        # Step 3: Load index for verification
        with open(index_path) as f:
            index_data = json.load(f)

        elapsed = time.time() - start_time

        return PipelineResult(
            index_path=Path(index_path),
            index_data=index_data,
            segment_count=parse_result.segment_count,
            speaker_count=len(parse_result.speakers),
            chunk_count=index_data["total_chunks"],
            elapsed_seconds=elapsed,
        )

    # =========================================================================
    # AC-1: Full Pipeline Execution Tests
    # =========================================================================

    def test_pipeline_executes_without_error(
        self,
        parser: VTTParser,
        chunker: TranscriptChunker,
        golden_datasets_dir: Path,
        temp_output_dir: Path,
    ) -> None:
        """Verify full Python pipeline executes without error.

        AC-1: Full Python pipeline (VTT → Parse → Chunk) executes without error
        """
        vtt_path = golden_datasets_dir / "meeting-006-all-hands.vtt"
        if not vtt_path.exists():
            pytest.skip(f"Golden dataset not found: {vtt_path}")

        # Should complete without raising any exceptions
        result = self.run_pipeline(
            vtt_path,
            temp_output_dir / "ac1-test",
            parser,
            chunker,
        )

        # Verify outputs exist
        assert result.index_path.exists(), "index.json not created"
        chunks_dir = result.index_path.parent / "chunks"
        assert chunks_dir.exists(), "chunks/ directory not created"
        assert len(list(chunks_dir.glob("chunk-*.json"))) > 0, "No chunk files created"

    # =========================================================================
    # AC-2: meeting-006 Output Verification
    # =========================================================================

    def test_meeting_006_produces_expected_output(
        self,
        parser: VTTParser,
        chunker: TranscriptChunker,
        golden_datasets_dir: Path,
        temp_output_dir: Path,
    ) -> None:
        """Verify meeting-006 produces 7 chunks with 3,071 total segments.

        AC-2: meeting-006 (90K tokens) produces 7 chunks with 3,071 total segments
        """
        vtt_path = golden_datasets_dir / "meeting-006-all-hands.vtt"
        if not vtt_path.exists():
            pytest.skip(f"Golden dataset not found: {vtt_path}")

        result = self.run_pipeline(
            vtt_path,
            temp_output_dir / "ac2-test",
            parser,
            chunker,
        )

        # Verify segment count
        assert result.segment_count == 3071, f"Expected 3071 segments, got {result.segment_count}"
        assert result.index_data["total_segments"] == 3071, (
            f"Index reports wrong segment count: {result.index_data['total_segments']}"
        )

        # Verify chunk count
        assert result.chunk_count == 7, f"Expected 7 chunks, got {result.chunk_count}"

        # Verify actual chunk files
        chunks_dir = result.index_path.parent / "chunks"
        chunk_files = list(chunks_dir.glob("chunk-*.json"))
        assert len(chunk_files) == 7, f"Expected 7 chunk files, found {len(chunk_files)}"

    # =========================================================================
    # AC-3: Performance Threshold Tests
    # =========================================================================

    def test_meeting_006_performance_threshold(
        self,
        parser: VTTParser,
        chunker: TranscriptChunker,
        golden_datasets_dir: Path,
        temp_output_dir: Path,
    ) -> None:
        """Verify meeting-006 (largest dataset) completes within threshold.

        AC-3: All golden datasets process within performance thresholds
        - meeting-006 (~90K tokens, 3071 segments): < 10 seconds
        """
        vtt_path = golden_datasets_dir / "meeting-006-all-hands.vtt"
        if not vtt_path.exists():
            pytest.skip(f"Golden dataset not found: {vtt_path}")

        result = self.run_pipeline(
            vtt_path,
            temp_output_dir / "perf-test",
            parser,
            chunker,
        )

        # Large file should complete in < 10 seconds
        assert result.elapsed_seconds < 10.0, (
            f"Pipeline too slow for meeting-006: {result.elapsed_seconds:.2f}s (threshold: 10s)"
        )

    @pytest.mark.parametrize(
        "dataset,expected_segments,expected_chunks,max_seconds",
        [
            # Verified segment counts from TASK-231
            ("meeting-001.vtt", 39, 1, 2.0),
            ("meeting-002.vtt", 97, 1, 2.0),
            ("meeting-003.vtt", 62, 1, 2.0),
            ("meeting-004-sprint-planning.vtt", 536, 2, 3.0),
            ("meeting-005-roadmap-review.vtt", 896, 2, 5.0),
        ],
    )
    def test_smaller_datasets_performance(
        self,
        parser: VTTParser,
        chunker: TranscriptChunker,
        golden_datasets_dir: Path,
        temp_output_dir: Path,
        dataset: str,
        expected_segments: int,
        expected_chunks: int,
        max_seconds: float,
    ) -> None:
        """Verify smaller datasets complete within their performance thresholds.

        AC-3: All golden datasets process within performance thresholds
        """
        vtt_path = golden_datasets_dir / dataset
        if not vtt_path.exists():
            pytest.skip(f"Dataset not found: {vtt_path}")

        result = self.run_pipeline(
            vtt_path,
            temp_output_dir / dataset.replace(".vtt", ""),
            parser,
            chunker,
        )

        # Verify segment count matches expected
        assert result.segment_count == expected_segments, (
            f"Segment count mismatch for {dataset}: "
            f"expected {expected_segments}, got {result.segment_count}"
        )

        # Verify chunk count matches expected
        assert result.chunk_count == expected_chunks, (
            f"Chunk count mismatch for {dataset}: "
            f"expected {expected_chunks}, got {result.chunk_count}"
        )

        # Verify performance
        assert result.elapsed_seconds < max_seconds, (
            f"Pipeline too slow for {dataset}: "
            f"{result.elapsed_seconds:.2f}s (threshold: {max_seconds}s)"
        )

    # =========================================================================
    # AC-4: Idempotency Tests
    # =========================================================================

    def test_pipeline_is_idempotent(
        self,
        parser: VTTParser,
        chunker: TranscriptChunker,
        golden_datasets_dir: Path,
        temp_output_dir: Path,
    ) -> None:
        """Verify pipeline produces identical output for identical input.

        AC-4: Pipeline is idempotent (same output for same input)
        """
        vtt_path = golden_datasets_dir / "meeting-006-all-hands.vtt"
        if not vtt_path.exists():
            pytest.skip(f"Golden dataset not found: {vtt_path}")

        # Run pipeline twice with separate output directories
        result_1 = self.run_pipeline(
            vtt_path,
            temp_output_dir / "run1",
            parser,
            chunker,
        )
        result_2 = self.run_pipeline(
            vtt_path,
            temp_output_dir / "run2",
            parser,
            chunker,
        )

        # Compare index data (excluding any timestamps or generated fields)
        index_1 = result_1.index_data.copy()
        index_2 = result_2.index_data.copy()

        # Remove any non-deterministic fields if present
        for idx in [index_1, index_2]:
            idx.pop("generated_at", None)
            idx.pop("processing_time_ms", None)

        assert index_1 == index_2, "Pipeline output not idempotent: index.json differs between runs"

        # Compare chunk contents
        chunks_dir_1 = result_1.index_path.parent / "chunks"
        chunks_dir_2 = result_2.index_path.parent / "chunks"

        chunk_files_1 = sorted(chunks_dir_1.glob("chunk-*.json"))
        chunk_files_2 = sorted(chunks_dir_2.glob("chunk-*.json"))

        assert len(chunk_files_1) == len(chunk_files_2), (
            "Different number of chunk files between runs"
        )

        for cf1, cf2 in zip(chunk_files_1, chunk_files_2, strict=True):
            with open(cf1) as f:
                chunk_1 = json.load(f)
            with open(cf2) as f:
                chunk_2 = json.load(f)

            # Remove non-deterministic fields
            for ch in [chunk_1, chunk_2]:
                ch.pop("generated_at", None)

            assert chunk_1 == chunk_2, f"Chunk content differs between runs: {cf1.name}"

    def test_pipeline_idempotent_for_all_datasets(
        self,
        parser: VTTParser,
        chunker: TranscriptChunker,
        golden_datasets_dir: Path,
        temp_output_dir: Path,
    ) -> None:
        """Verify idempotency holds for a representative small dataset.

        AC-4 (supplementary): Verify idempotency on smaller dataset for speed.
        """
        vtt_path = golden_datasets_dir / "meeting-001.vtt"
        if not vtt_path.exists():
            pytest.skip(f"Dataset not found: {vtt_path}")

        # Run twice
        result_1 = self.run_pipeline(
            vtt_path,
            temp_output_dir / "idem1",
            parser,
            chunker,
        )
        result_2 = self.run_pipeline(
            vtt_path,
            temp_output_dir / "idem2",
            parser,
            chunker,
        )

        # Verify deterministic output
        assert result_1.segment_count == result_2.segment_count
        assert result_1.chunk_count == result_2.chunk_count
        assert result_1.speaker_count == result_2.speaker_count

    # =========================================================================
    # AC-5: Combined Performance Test
    # =========================================================================

    def test_all_datasets_complete_under_30_seconds(
        self,
        parser: VTTParser,
        chunker: TranscriptChunker,
        golden_datasets_dir: Path,
        temp_output_dir: Path,
    ) -> None:
        """Verify all datasets combined complete in < 30 seconds.

        AC-5: Tests complete in < 30 seconds for all datasets combined
        """
        datasets = [
            "meeting-001.vtt",
            "meeting-002.vtt",
            "meeting-003.vtt",
            "meeting-004-sprint-planning.vtt",
            "meeting-005-roadmap-review.vtt",
            "meeting-006-all-hands.vtt",
        ]

        start_time = time.time()
        processed_count = 0

        for i, dataset in enumerate(datasets):
            vtt_path = golden_datasets_dir / dataset
            if not vtt_path.exists():
                continue

            self.run_pipeline(
                vtt_path,
                temp_output_dir / f"dataset_{i}",
                parser,
                chunker,
            )
            processed_count += 1

        total_elapsed = time.time() - start_time

        # All 6 datasets should complete in < 30 seconds
        assert total_elapsed < 30.0, f"All datasets took {total_elapsed:.2f}s, expected < 30s"

        # Skip if golden datasets are not available (e.g., CI where VTT files are not committed)
        if processed_count == 0:
            pytest.skip("No golden VTT datasets available")

        # Verify we processed all available datasets
        assert processed_count >= 6, (
            f"Expected to process 6 datasets, only processed {processed_count}"
        )

    # =========================================================================
    # Supplementary Pipeline Tests
    # =========================================================================

    def test_pipeline_handles_medium_dataset(
        self,
        parser: VTTParser,
        chunker: TranscriptChunker,
        golden_datasets_dir: Path,
        temp_output_dir: Path,
    ) -> None:
        """Test pipeline with medium dataset (meeting-004, 536 segments).

        Supplements AC-1 with medium-size dataset validation.
        """
        vtt_path = golden_datasets_dir / "meeting-004-sprint-planning.vtt"
        if not vtt_path.exists():
            pytest.skip(f"Dataset not found: {vtt_path}")

        result = self.run_pipeline(
            vtt_path,
            temp_output_dir / "medium-test",
            parser,
            chunker,
        )

        # Verify expected output
        assert result.segment_count == 536
        assert result.chunk_count == 2

        # Verify chunk contents sum correctly
        chunks_dir = result.index_path.parent / "chunks"
        total_in_chunks = 0
        for chunk_file in chunks_dir.glob("chunk-*.json"):
            with open(chunk_file) as f:
                chunk_data = json.load(f)
            total_in_chunks += len(chunk_data["segments"])

        assert total_in_chunks == 536, (
            f"Segments in chunks ({total_in_chunks}) != parser count (536)"
        )

    def test_pipeline_output_structure_complete(
        self,
        parser: VTTParser,
        chunker: TranscriptChunker,
        golden_datasets_dir: Path,
        temp_output_dir: Path,
    ) -> None:
        """Verify pipeline produces complete output structure.

        Validates:
        - index.json exists with required fields
        - chunks/ directory exists with chunk files
        - All required metadata present
        """
        vtt_path = golden_datasets_dir / "meeting-001.vtt"
        if not vtt_path.exists():
            pytest.skip(f"Dataset not found: {vtt_path}")

        result = self.run_pipeline(
            vtt_path,
            temp_output_dir / "structure-test",
            parser,
            chunker,
        )

        # Check index.json structure
        assert "total_segments" in result.index_data
        assert "total_chunks" in result.index_data
        assert "chunks" in result.index_data
        assert "speakers" in result.index_data

        # Check chunks directory
        chunks_dir = result.index_path.parent / "chunks"
        assert chunks_dir.is_dir()

        # Check chunk files exist per index
        for chunk_meta in result.index_data["chunks"]:
            chunk_file = chunks_dir / Path(chunk_meta["file"]).name
            assert chunk_file.exists(), f"Chunk file missing: {chunk_file}"
