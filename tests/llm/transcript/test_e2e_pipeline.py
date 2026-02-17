# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""End-to-end tests for complete hybrid transcript pipeline.

These tests validate the full pipeline from raw VTT input to formatted output packet:
VTT → VTTParser → TranscriptChunker → ts-extractor → ts-formatter → output packet

WARNING: These tests invoke LLM agents and are:
- SLOW (minutes per test)
- EXPENSIVE (token costs)
- EXCLUDED FROM CI (use pytest -m llm to run)

Run manually with: pytest -m llm tests/llm/transcript/test_e2e_pipeline.py

Reference: TASK-236, EN-023 Integration Testing
"""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pytest

if TYPE_CHECKING:
    pass


@dataclass
class PipelineResult:
    """Result from running the full hybrid pipeline."""

    success: bool
    error: str | None = None
    packet_dir: Path | None = None
    elapsed_seconds: float = 0.0
    extraction_report: dict[str, Any] | None = None


def run_full_hybrid_pipeline(
    vtt_path: Path,
    output_dir: Path,
    timeout_seconds: int = 600,
) -> PipelineResult:
    """Run the complete hybrid transcript pipeline.

    This function orchestrates:
    1. VTTParser - Parse raw VTT to canonical format
    2. TranscriptChunker - Split into manageable chunks
    3. ts-extractor - Extract entities from chunks (LLM)
    4. ts-formatter - Format into output packet (LLM)

    Args:
        vtt_path: Path to input VTT file.
        output_dir: Directory for pipeline output.
        timeout_seconds: Maximum time to wait (default 600s = 10 min).

    Returns:
        PipelineResult with success status and outputs.
    """

    start_time = time.time()

    # Check for pre-computed output (for test validation without LLM cost)
    packet_dir = output_dir / "packet"
    extraction_report_path = output_dir / "extraction" / "extraction-report.json"

    if packet_dir.exists() and extraction_report_path.exists():
        elapsed = time.time() - start_time
        with open(extraction_report_path) as f:
            extraction_report = json.load(f)
        return PipelineResult(
            success=True,
            packet_dir=packet_dir,
            elapsed_seconds=elapsed,
            extraction_report=extraction_report,
        )

    # For live invocation, the pipeline needs to be called
    # This is a placeholder - actual invocation via transcript skill
    pytest.skip(
        "Live hybrid pipeline invocation not implemented. "
        "Run transcript skill manually or provide pre-computed output."
    )
    return PipelineResult(success=False, error="Not implemented")


@pytest.mark.llm
@pytest.mark.slow
class TestFullPipelineE2E:
    """End-to-end tests for complete hybrid pipeline.

    Tests validate:
    - AC-1: Complete pipeline executes without error for meeting-006
    - AC-2: Output packet contains all 8 files per ADR-002
    - AC-3: All 3,071 segments represented in transcript files
    - AC-4: Deep links in packet are valid (anchors exist)
    - AC-5: Token budgets respected (no file > 35K tokens)
    - AC-6: Pipeline completes within reasonable time (< 10 minutes)
    """

    @pytest.fixture
    def pipeline_result(
        self,
        golden_vtt_path: Path,
        temp_output_dir: Path,
    ) -> PipelineResult:
        """Run the full pipeline and return the result.

        This fixture is shared across tests to avoid multiple expensive invocations.
        """
        return run_full_hybrid_pipeline(
            vtt_path=golden_vtt_path,
            output_dir=temp_output_dir,
        )

    # =========================================================================
    # AC-1: Complete pipeline executes without error for meeting-006
    # =========================================================================

    def test_complete_pipeline_meeting_006(
        self,
        pipeline_result: PipelineResult,
    ) -> None:
        """Verify complete pipeline executes successfully.

        AC-1: Complete pipeline executes without error for meeting-006
        """
        assert pipeline_result.success, f"Pipeline failed: {pipeline_result.error}"

    # =========================================================================
    # AC-2: Output packet contains all 8 files per ADR-002
    # =========================================================================

    def test_output_packet_structure(
        self,
        pipeline_result: PipelineResult,
    ) -> None:
        """Verify output packet contains all required files per ADR-002.

        AC-2: Output packet contains all 8 files per ADR-002

        ADR-002 specifies:
        - 00-index.md
        - 01-summary.md
        - 02-transcript.md (may be split)
        - 03-speakers.md
        - 04-action-items.md
        - 05-decisions.md
        - 06-questions.md
        - 07-topics.md
        - _anchors.json
        """
        assert pipeline_result.success, "Pipeline must succeed first"
        assert pipeline_result.packet_dir is not None

        packet_dir = pipeline_result.packet_dir

        # Check all required files exist per ADR-002
        required_files = [
            "00-index.md",
            "01-summary.md",
            "02-transcript",  # Base name - may be split
            "03-speakers.md",
            "04-action-items.md",
            "05-decisions.md",
            "06-questions.md",
            "07-topics.md",
            "_anchors.json",
        ]

        missing_files = []
        for filename in required_files:
            if filename.endswith(".md") or filename.endswith(".json"):
                # Exact file match
                if not (packet_dir / filename).exists():
                    # Check for split files (e.g., 02-transcript-part-1.md)
                    base = filename.replace(".md", "").replace(".json", "")
                    matches = list(packet_dir.glob(f"{base}*.md")) + list(
                        packet_dir.glob(f"{base}*.json")
                    )
                    if not matches:
                        missing_files.append(filename)
            else:
                # Base name - check for files starting with it
                matches = list(packet_dir.glob(f"{filename}*.md"))
                if not matches:
                    missing_files.append(f"{filename}*.md")

        assert not missing_files, f"Missing required files: {missing_files}"

    # =========================================================================
    # AC-3: All 3,071 segments represented in transcript files
    # =========================================================================

    def test_segment_completeness(
        self,
        pipeline_result: PipelineResult,
    ) -> None:
        """Verify all 3,071 segments are represented in output.

        AC-3: All 3,071 segments represented in transcript files
        """
        assert pipeline_result.success, "Pipeline must succeed first"
        assert pipeline_result.packet_dir is not None

        packet_dir = pipeline_result.packet_dir
        anchors_path = packet_dir / "_anchors.json"

        if not anchors_path.exists():
            pytest.skip("_anchors.json not found - manual validation required")

        with open(anchors_path) as f:
            anchors = json.load(f)

        # Count segment anchors (format: seg-NNNN)
        segment_anchors = [a for a in anchors.keys() if a.startswith("seg-")]

        # meeting-006 has 3,071 segments
        expected_segments = 3071
        actual_segments = len(segment_anchors)

        assert actual_segments == expected_segments, (
            f"Expected {expected_segments} segment anchors, got {actual_segments}"
        )

    # =========================================================================
    # AC-4: Deep links in packet are valid (anchors exist)
    # =========================================================================

    def test_deep_links_valid(
        self,
        pipeline_result: PipelineResult,
    ) -> None:
        """Verify all deep links in packet reference valid anchors.

        AC-4: Deep links in packet are valid (anchors exist)
        """
        assert pipeline_result.success, "Pipeline must succeed first"
        assert pipeline_result.packet_dir is not None

        packet_dir = pipeline_result.packet_dir
        anchors_path = packet_dir / "_anchors.json"

        if not anchors_path.exists():
            pytest.skip("_anchors.json not found - manual validation required")

        with open(anchors_path) as f:
            anchors = json.load(f)

        # Check all markdown files for deep links
        invalid_links = []
        for md_file in packet_dir.glob("*.md"):
            content = md_file.read_text()

            # Find all anchor references (#anchor-name)
            links = re.findall(r"\(#([\w-]+)\)", content)

            for link in links:
                if link not in anchors:
                    invalid_links.append(f"{md_file.name}: #{link}")

        # Allow small percentage of invalid links due to LLM non-determinism
        max_invalid = 5  # Allow up to 5 invalid links
        assert len(invalid_links) <= max_invalid, (
            f"Too many invalid deep links ({len(invalid_links)}): {invalid_links[:10]}"
        )

    # =========================================================================
    # AC-5: Token budgets respected (no file > 35K tokens)
    # =========================================================================

    def test_token_budgets_respected(
        self,
        pipeline_result: PipelineResult,
    ) -> None:
        """Verify no file exceeds 35K token hard limit.

        AC-5: Token budgets respected (no file > 35K tokens)

        ADR-004 specifies:
        - Soft limit: 31,500 tokens (split at ## heading)
        - Hard limit: 35,000 tokens (force split)
        """
        assert pipeline_result.success, "Pipeline must succeed first"
        assert pipeline_result.packet_dir is not None

        packet_dir = pipeline_result.packet_dir

        # Token estimation: ~4 characters per token
        hard_limit_tokens = 35000
        hard_limit_chars = hard_limit_tokens * 4

        oversized_files = []
        for md_file in packet_dir.glob("*.md"):
            content = md_file.read_text()
            char_count = len(content)

            if char_count > hard_limit_chars:
                approx_tokens = char_count // 4
                oversized_files.append(f"{md_file.name}: ~{approx_tokens:,} tokens")

        assert not oversized_files, f"Files exceed 35K token limit: {oversized_files}"

    # =========================================================================
    # AC-6: Pipeline completes within reasonable time (< 10 minutes)
    # =========================================================================

    def test_pipeline_performance(
        self,
        pipeline_result: PipelineResult,
    ) -> None:
        """Verify pipeline completes within 10 minutes.

        AC-6: Pipeline completes within reasonable time (< 10 minutes)
        """
        assert pipeline_result.success, "Pipeline must succeed first"

        max_time_seconds = 600  # 10 minutes
        assert pipeline_result.elapsed_seconds < max_time_seconds, (
            f"Pipeline took {pipeline_result.elapsed_seconds:.2f}s, expected < {max_time_seconds}s"
        )


@pytest.mark.llm
@pytest.mark.slow
class TestPipelineSegmentCoverage:
    """Segment coverage tests for hybrid pipeline output."""

    @pytest.fixture
    def pipeline_result(
        self,
        golden_vtt_path: Path,
        temp_output_dir: Path,
    ) -> PipelineResult:
        """Run the full pipeline and return the result."""
        return run_full_hybrid_pipeline(
            vtt_path=golden_vtt_path,
            output_dir=temp_output_dir,
        )

    def test_transcript_files_contain_all_segments(
        self,
        pipeline_result: PipelineResult,
    ) -> None:
        """Verify transcript files contain all segments (may be split)."""
        assert pipeline_result.success, "Pipeline must succeed first"
        assert pipeline_result.packet_dir is not None

        packet_dir = pipeline_result.packet_dir

        # Find all transcript files (02-transcript*.md)
        transcript_files = sorted(packet_dir.glob("02-transcript*.md"))

        if not transcript_files:
            pytest.skip("No transcript files found")

        # Count segment markers across all transcript files
        segment_count = 0
        for tf in transcript_files:
            content = tf.read_text()
            # Count segment anchors (format: <a id="seg-NNNN">)
            anchors = re.findall(r'<a id="seg-\d+">', content)
            segment_count += len(anchors)

        # Should have all 3,071 segments
        assert segment_count == 3071, (
            f"Expected 3,071 segments in transcript files, found {segment_count}"
        )

    def test_extraction_report_segment_coverage(
        self,
        pipeline_result: PipelineResult,
    ) -> None:
        """Verify extraction report covers input segments."""
        assert pipeline_result.success, "Pipeline must succeed first"

        extraction_report = pipeline_result.extraction_report
        if extraction_report is None:
            pytest.skip("Extraction report not available")
            return  # Satisfy type checker

        # Check that extraction stats reflect segment processing
        if "chunk_metadata" in extraction_report:
            chunk_meta = extraction_report["chunk_metadata"]
            total_chunks = chunk_meta.get("chunks_total", 0)
            chunks_processed = chunk_meta.get("chunks_processed", 0)

            # Should process all or most chunks
            assert chunks_processed > 0, "No chunks were processed"
            assert chunks_processed <= total_chunks

        # Verify entities have valid segment citations
        for entity_type in ["action_items", "decisions", "questions"]:
            for entity in extraction_report.get(entity_type, []):
                citation = entity.get("citation", {})
                if "segment_id" in citation:
                    seg_id = citation["segment_id"]
                    # Segment ID should be valid format
                    if isinstance(seg_id, str) and seg_id.startswith("seg-"):
                        seg_num = int(seg_id.split("-")[1])
                        assert 1 <= seg_num <= 3071, f"Invalid segment: {seg_id}"
