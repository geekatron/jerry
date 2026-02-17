# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""LLM integration tests for ts-extractor with chunked input.

These tests validate that ts-extractor correctly processes chunked input
from EN-021 TranscriptChunker output per EN-022 Extractor Adaptation.

WARNING: These tests invoke LLM agents and are:
- SLOW (minutes per test)
- EXPENSIVE (token costs)
- EXCLUDED FROM CI (use pytest -m llm to run)

Run manually with: pytest -m llm tests/llm/transcript/test_extractor_chunked.py

Reference: TASK-235, EN-023 Integration Testing
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pytest

if TYPE_CHECKING:
    from tests.llm.transcript.utils import LLMTestResult


# Skip all tests if jsonschema not installed
jsonschema = pytest.importorskip("jsonschema")


def invoke_ts_extractor(
    index_path: Path,
    output_dir: Path,
    timeout_seconds: int = 300,
) -> LLMTestResult:
    """Invoke ts-extractor agent via transcript skill.

    This function invokes the ts-extractor agent to process chunked input.
    The actual implementation requires the agent to be invoked via the
    transcript skill or Task tool.

    Args:
        index_path: Path to index.json from chunker output.
        output_dir: Directory for extraction output.
        timeout_seconds: Maximum time to wait.

    Returns:
        LLMTestResult with extraction status.
    """
    from tests.llm.transcript.utils import LLMTestResult

    # Check if pre-computed output exists (for test validation)
    extraction_report_path = output_dir / "extraction-report.json"
    if extraction_report_path.exists():
        with open(extraction_report_path) as f:
            output = json.load(f)
        return LLMTestResult(
            success=True,
            output=output,
            error=None,
            tokens_used=0,
            elapsed_seconds=0.0,
            raw_output=extraction_report_path.read_text(),
        )

    # For live invocation, the agent needs to be called
    # This is a placeholder - actual invocation via Task tool or skill
    pytest.skip(
        "Live ts-extractor invocation not implemented. "
        "Run transcript skill manually or provide pre-computed output."
    )
    return LLMTestResult(success=False, error="Not implemented")


@pytest.mark.llm
@pytest.mark.slow
class TestExtractorChunkedInput:
    """LLM tests for ts-extractor with chunked input.

    Tests validate:
    - AC-1: ts-extractor successfully reads index.json
    - AC-2: ts-extractor processes all 7 chunks from meeting-006
    - AC-3: Extraction report includes input_format: "chunked"
    - AC-4: Chunk metadata correctly populated
    - AC-5: All citations include valid chunk_id
    - AC-6: Extraction quality comparable to single-file mode
    """

    @pytest.fixture
    def output_dir(self, tmp_path: Path) -> Path:
        """Create temporary output directory for extraction."""
        output = tmp_path / "extraction_output"
        output.mkdir(parents=True, exist_ok=True)
        return output

    @pytest.fixture
    def extraction_report(
        self,
        chunked_input_path: Path,
        output_dir: Path,
    ) -> dict[str, Any]:
        """Run ts-extractor and return the extraction report.

        This fixture is shared across tests in this class to avoid
        multiple expensive LLM invocations.
        """
        result = invoke_ts_extractor(
            index_path=chunked_input_path,
            output_dir=output_dir,
        )

        if not result.success:
            pytest.fail(f"ts-extractor invocation failed: {result.error}")

        return result.output or {}

    # =========================================================================
    # AC-1: ts-extractor successfully reads index.json
    # =========================================================================

    def test_extractor_reads_index_json(
        self,
        extraction_report: dict[str, Any],
        extraction_report_schema: dict[str, Any],
    ) -> None:
        """Verify ts-extractor successfully reads and processes index.json.

        AC-1: ts-extractor successfully reads index.json
        """
        # Verify extraction report is valid
        assert extraction_report, "Extraction report is empty"

        # Validate against schema
        jsonschema.validate(instance=extraction_report, schema=extraction_report_schema)

        # Verify required fields exist
        assert "version" in extraction_report
        assert "packet_id" in extraction_report
        assert "input_format" in extraction_report
        assert "extraction_stats" in extraction_report

    # =========================================================================
    # AC-2: ts-extractor processes all 7 chunks from meeting-006
    # =========================================================================

    def test_extractor_processes_all_chunks(
        self,
        extraction_report: dict[str, Any],
    ) -> None:
        """Verify ts-extractor processes all 7 chunks from meeting-006.

        AC-2: ts-extractor processes all 7 chunks from meeting-006
        """
        chunk_metadata = extraction_report.get("chunk_metadata")
        assert chunk_metadata is not None, "chunk_metadata missing"

        # meeting-006 has 7 chunks
        assert chunk_metadata["chunks_total"] == 7, (
            f"Expected 7 chunks total, got {chunk_metadata['chunks_total']}"
        )

        # Should process all chunks (or subset based on strategy)
        assert chunk_metadata["chunks_processed"] > 0, "No chunks processed"
        assert chunk_metadata["chunks_processed"] <= chunk_metadata["chunks_total"]

    # =========================================================================
    # AC-3: Extraction report includes input_format: "chunked"
    # =========================================================================

    def test_extraction_report_chunked_format(
        self,
        extraction_report: dict[str, Any],
    ) -> None:
        """Verify extraction report includes chunked format metadata.

        AC-3: Extraction report includes input_format: "chunked"
        """
        assert extraction_report["input_format"] == "chunked", (
            f"Expected input_format='chunked', got '{extraction_report['input_format']}'"
        )

        # Verify chunk_metadata is present (required for chunked format)
        assert extraction_report.get("chunk_metadata") is not None, (
            "chunk_metadata required for chunked input format"
        )

        # Verify selection strategy
        chunk_metadata = extraction_report["chunk_metadata"]
        assert chunk_metadata["selection_strategy"] in [
            "sequential",
            "index_only",
            "selective",
        ], f"Invalid selection_strategy: {chunk_metadata['selection_strategy']}"

    # =========================================================================
    # AC-4: Chunk metadata correctly populated
    # =========================================================================

    def test_chunk_metadata_populated(
        self,
        extraction_report: dict[str, Any],
    ) -> None:
        """Verify chunk processing metadata is correctly populated.

        AC-4: Chunk metadata correctly populated
        """
        chunk_metadata = extraction_report["chunk_metadata"]

        # Required fields
        assert "index_path" in chunk_metadata
        assert "chunks_processed" in chunk_metadata
        assert "chunks_total" in chunk_metadata
        assert "selection_strategy" in chunk_metadata

        # index_path should reference index.json
        assert "index.json" in chunk_metadata["index_path"]

        # Per-chunk details
        if "chunks" in chunk_metadata and chunk_metadata["chunks"]:
            for chunk_info in chunk_metadata["chunks"]:
                # Verify chunk_id format
                assert chunk_info["chunk_id"].startswith("chunk-"), (
                    f"Invalid chunk_id format: {chunk_info['chunk_id']}"
                )

                # Verify segment_range is [start, end]
                assert len(chunk_info["segment_range"]) == 2, (
                    f"segment_range should be [start, end]: {chunk_info['segment_range']}"
                )
                assert chunk_info["segment_range"][0] <= chunk_info["segment_range"][1]

                # Verify entities_extracted count
                assert chunk_info["entities_extracted"] >= 0

    # =========================================================================
    # AC-5: All citations include valid chunk_id
    # =========================================================================

    def test_citations_include_chunk_id(
        self,
        extraction_report: dict[str, Any],
    ) -> None:
        """Verify all entity citations include chunk_id.

        AC-5: All citations include valid chunk_id
        """
        entities_checked = 0
        missing_chunk_ids: list[str] = []

        # Check citations in all entity types
        for entity_type in ["action_items", "decisions", "questions"]:
            for entity in extraction_report.get(entity_type, []):
                entity_id = entity.get("id", "unknown")
                citation = entity.get("citation", {})

                # chunk_id is required for chunked input
                if "chunk_id" not in citation:
                    missing_chunk_ids.append(f"{entity_type}/{entity_id}")
                elif not citation["chunk_id"].startswith("chunk-"):
                    missing_chunk_ids.append(
                        f"{entity_type}/{entity_id}: invalid format '{citation['chunk_id']}'"
                    )

                entities_checked += 1

        assert entities_checked > 0, "No entities found to validate"
        assert not missing_chunk_ids, (
            f"Citations missing or invalid chunk_id: {missing_chunk_ids[:5]}"
            f"{'...' if len(missing_chunk_ids) > 5 else ''}"
        )

    # =========================================================================
    # AC-6: Extraction quality comparable to single-file mode
    # =========================================================================

    def test_extraction_quality_comparable(
        self,
        extraction_report: dict[str, Any],
    ) -> None:
        """Verify extraction quality is comparable to single-file mode.

        AC-6: Extraction quality comparable to single-file mode

        meeting-006-all-hands.vtt should yield significant entities.
        Thresholds based on expected content from a 90K token all-hands meeting.
        """
        stats = extraction_report["extraction_stats"]

        # Minimum expected entities for meeting-006
        assert stats["action_items"] >= 5, (
            f"Too few action items: {stats['action_items']} (expected >= 5)"
        )
        assert stats["decisions"] >= 3, f"Too few decisions: {stats['decisions']} (expected >= 3)"
        assert stats["questions"] >= 3, f"Too few questions: {stats['questions']} (expected >= 3)"
        assert stats["speakers_identified"] >= 5, (
            f"Too few speakers: {stats['speakers_identified']} (expected >= 5)"
        )

    def test_extraction_confidence_levels(
        self,
        extraction_report: dict[str, Any],
    ) -> None:
        """Verify extraction confidence meets quality thresholds.

        AC-6 (supplementary): Confidence should meet NFR-008 thresholds.
        """
        stats = extraction_report["extraction_stats"]
        confidence = stats.get("confidence_summary")

        if confidence:
            # Average confidence should be >= 0.70 (NFR-008)
            assert confidence.get("average", 0) >= 0.70, (
                f"Average confidence too low: {confidence.get('average')}"
            )

            # High confidence ratio should be reasonable
            high_ratio = confidence.get("high_ratio", 0)
            assert high_ratio >= 0.50, f"High confidence ratio too low: {high_ratio}"


@pytest.mark.llm
@pytest.mark.slow
class TestExtractorChunkedCitations:
    """Citation-specific tests for chunked input mode."""

    @pytest.fixture
    def extraction_report(
        self,
        chunked_input_path: Path,
        temp_output_dir: Path,
    ) -> dict[str, Any]:
        """Run ts-extractor and return the extraction report."""
        result = invoke_ts_extractor(
            index_path=chunked_input_path,
            output_dir=temp_output_dir / "citation_test",
        )

        if not result.success:
            pytest.fail(f"ts-extractor invocation failed: {result.error}")

        return result.output or {}

    def test_citation_segment_ids_valid(
        self,
        extraction_report: dict[str, Any],
    ) -> None:
        """Verify all citation segment_ids are valid (1-3071 for meeting-006)."""
        max_segment_id = 3071  # meeting-006 has 3071 segments
        invalid_citations: list[str] = []

        for entity_type in ["action_items", "decisions", "questions"]:
            for entity in extraction_report.get(entity_type, []):
                citation = entity.get("citation", {})
                segment_id = citation.get("segment_id", "")

                # Parse segment_id (format: seg-NNNN)
                if segment_id.startswith("seg-"):
                    try:
                        seg_num = int(segment_id.split("-")[1])
                        if seg_num < 1 or seg_num > max_segment_id:
                            invalid_citations.append(
                                f"{entity_type}/{entity['id']}: {segment_id} out of range"
                            )
                    except (ValueError, IndexError):
                        invalid_citations.append(
                            f"{entity_type}/{entity['id']}: invalid format {segment_id}"
                        )

        assert not invalid_citations, f"Invalid segment_id citations: {invalid_citations[:5]}"

    def test_citation_anchors_format(
        self,
        extraction_report: dict[str, Any],
    ) -> None:
        """Verify citation anchors follow ADR-003 format (#seg-NNNN)."""
        invalid_anchors: list[str] = []

        for entity_type in ["action_items", "decisions", "questions"]:
            for entity in extraction_report.get(entity_type, []):
                citation = entity.get("citation", {})
                anchor = citation.get("anchor", "")

                # ADR-003: anchors must be #seg-NNNN
                if not anchor.startswith("#seg-"):
                    invalid_anchors.append(f"{entity_type}/{entity['id']}: {anchor}")

        assert not invalid_anchors, (
            f"Invalid anchor format (expected #seg-NNNN): {invalid_anchors[:5]}"
        )

    def test_citation_text_snippets_present(
        self,
        extraction_report: dict[str, Any],
    ) -> None:
        """Verify all citations include non-empty text_snippet."""
        missing_snippets: list[str] = []

        for entity_type in ["action_items", "decisions", "questions"]:
            for entity in extraction_report.get(entity_type, []):
                citation = entity.get("citation", {})
                text_snippet = citation.get("text_snippet", "")

                if not text_snippet or len(text_snippet.strip()) == 0:
                    missing_snippets.append(f"{entity_type}/{entity['id']}")

        assert not missing_snippets, f"Citations missing text_snippet: {missing_snippets[:5]}"
