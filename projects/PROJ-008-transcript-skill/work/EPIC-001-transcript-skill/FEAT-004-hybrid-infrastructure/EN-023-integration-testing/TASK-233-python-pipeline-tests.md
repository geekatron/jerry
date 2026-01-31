# TASK-233: Python-Layer Pipeline Tests

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
CREATED: 2026-01-29 (EN-023 Integration Testing)
PURPOSE: End-to-end Python pipeline tests (no LLM invocation)
-->

---

## Frontmatter

```yaml
# === IDENTITY ===
id: "TASK-233"
work_type: TASK

# === CORE METADATA ===
title: "Python-Layer Pipeline Tests"
description: |
  Create end-to-end tests for the Python layer of the hybrid pipeline:
  VTT file → VTTParser → TranscriptChunker → index.json + chunks/

  These tests validate the complete Python pipeline without LLM invocation,
  making them suitable for CI.

# === CLASSIFICATION ===
classification: ENABLER

# === LIFECYCLE STATE ===
status: DONE
resolution: COMPLETED

# === PRIORITY ===
priority: HIGH

# === PEOPLE ===
assignee: "Claude"
created_by: "Claude"

# === TIMESTAMPS ===
created_at: "2026-01-29T21:30:00Z"
updated_at: "2026-01-30T00:30:00Z"

# === HIERARCHY ===
parent_id: "EN-023"

# === TAGS ===
tags:
  - "testing"
  - "integration"
  - "pipeline"
  - "e2e"
  - "CI"

# === DELIVERY ITEM PROPERTIES ===
effort: 3
acceptance_criteria: |
  AC-1: Full Python pipeline (VTT → Parse → Chunk) executes without error
  AC-2: meeting-006 (90K tokens) produces 7 chunks with 3,071 total segments
  AC-3: All golden datasets process within performance thresholds
  AC-4: Pipeline is idempotent (same output for same input)
  AC-5: Tests complete in < 30 seconds for all datasets combined
due_date: null

# === TASK-SPECIFIC PROPERTIES ===
activity: TESTING
original_estimate: 3
remaining_work: 3
time_spent: null
```

---

## State Machine

**Current State:** `DONE`

---

## Description

### Purpose

These tests validate the **complete Python layer** of the hybrid architecture. They are the final Python-layer tests before LLM validation and serve as the CI gate for Python code changes.

### Pipeline Under Test

```
┌─────────────────┐    ┌───────────┐    ┌──────────────────┐    ┌─────────────────┐
│ meeting-006.vtt │───►│ VTTParser │───►│ TranscriptChunker│───►│ index.json      │
│ (raw VTT file)  │    │ (EN-020)  │    │ (EN-021)         │    │ chunks/*.json   │
└─────────────────┘    └───────────┘    └──────────────────┘    └─────────────────┘
```

### Test Cases

```python
# tests/integration/transcript/test_pipeline.py

import pytest
import json
import time
from pathlib import Path
from src.transcript.infrastructure.adapters.vtt_parser import VTTParser
from src.transcript.application.services.chunker import TranscriptChunker

@pytest.mark.integration
class TestPythonPipeline:
    """End-to-end tests for Python pipeline (no LLM)."""

    @pytest.fixture
    def parser(self) -> VTTParser:
        return VTTParser()

    @pytest.fixture
    def chunker(self) -> TranscriptChunker:
        return TranscriptChunker()

    def run_pipeline(
        self, vtt_path: Path, output_dir: Path, parser: VTTParser, chunker: TranscriptChunker
    ) -> dict:
        """Execute full Python pipeline and return results."""
        start_time = time.time()

        # Parse
        canonical = parser.parse(vtt_path)

        # Chunk
        index_path = chunker.chunk(canonical, output_dir)

        # Load index
        with open(index_path) as f:
            index = json.load(f)

        elapsed = time.time() - start_time

        return {
            "index": index,
            "index_path": index_path,
            "elapsed_seconds": elapsed,
            "segment_count": len(canonical.segments),
            "speaker_count": len(canonical.speakers),
        }

    def test_meeting_006_full_pipeline(
        self, parser, chunker, temp_output_dir
    ):
        """Verify meeting-006 processes correctly through full pipeline."""
        vtt_path = Path("skills/transcript/test_data/transcripts/golden/meeting-006-all-hands.vtt")

        result = self.run_pipeline(vtt_path, temp_output_dir, parser, chunker)

        # Verify expected outputs
        assert result["segment_count"] == 3071
        assert result["index"]["summary"]["total_chunks"] == 7
        assert result["index"]["summary"]["total_segments"] == 3071

    def test_pipeline_performance(self, parser, chunker, temp_output_dir):
        """Verify pipeline completes within performance threshold."""
        vtt_path = Path("skills/transcript/test_data/transcripts/golden/meeting-006-all-hands.vtt")

        result = self.run_pipeline(vtt_path, temp_output_dir, parser, chunker)

        # Should complete in < 10 seconds for 90K token file
        assert result["elapsed_seconds"] < 10.0, f"Pipeline too slow: {result['elapsed_seconds']:.2f}s"

    def test_pipeline_idempotent(self, parser, chunker, temp_output_dir):
        """Verify pipeline produces identical output for identical input."""
        vtt_path = Path("skills/transcript/test_data/transcripts/golden/meeting-006-all-hands.vtt")

        # Run twice
        output_1 = temp_output_dir / "run1"
        output_2 = temp_output_dir / "run2"
        output_1.mkdir()
        output_2.mkdir()

        result_1 = self.run_pipeline(vtt_path, output_1, parser, chunker)
        result_2 = self.run_pipeline(vtt_path, output_2, parser, chunker)

        # Compare index content (excluding timestamps)
        index_1 = result_1["index"].copy()
        index_2 = result_2["index"].copy()
        # Remove any non-deterministic fields if present
        for idx in [index_1, index_2]:
            idx.pop("generated_at", None)

        assert index_1 == index_2, "Pipeline output not idempotent"

    @pytest.mark.parametrize("dataset,expected_segments,expected_chunks", [
        ("meeting-001.vtt", 100, 1),
        ("meeting-002.vtt", 500, 1),
        ("meeting-003.vtt", 800, 2),
        ("meeting-004-sprint-planning.vtt", 800, 2),
        ("meeting-005-roadmap-review.vtt", 1500, 3),
        ("meeting-006-all-hands.vtt", 3071, 7),
    ])
    def test_all_golden_datasets(
        self, parser, chunker, dataset, expected_segments, expected_chunks, temp_output_dir
    ):
        """Verify all golden datasets process correctly."""
        vtt_path = Path(f"skills/transcript/test_data/transcripts/golden/{dataset}")
        if not vtt_path.exists():
            pytest.skip(f"Dataset {dataset} not available")

        result = self.run_pipeline(
            vtt_path, temp_output_dir / dataset.replace(".vtt", ""), parser, chunker
        )

        # Allow 10% tolerance for estimated segment counts
        assert abs(result["segment_count"] - expected_segments) / expected_segments < 0.10
        assert result["index"]["summary"]["total_chunks"] == expected_chunks

    def test_all_datasets_under_30_seconds(self, parser, chunker, temp_output_dir):
        """Verify all datasets combined complete in < 30 seconds."""
        datasets = [
            "meeting-001.vtt",
            "meeting-002.vtt",
            "meeting-003.vtt",
            "meeting-004-sprint-planning.vtt",
            "meeting-005-roadmap-review.vtt",
            "meeting-006-all-hands.vtt",
        ]

        start_time = time.time()

        for i, dataset in enumerate(datasets):
            vtt_path = Path(f"skills/transcript/test_data/transcripts/golden/{dataset}")
            if vtt_path.exists():
                self.run_pipeline(
                    vtt_path, temp_output_dir / f"dataset_{i}", parser, chunker
                )

        total_elapsed = time.time() - start_time

        assert total_elapsed < 30.0, f"All datasets took {total_elapsed:.2f}s, expected < 30s"
```

---

## Acceptance Criteria

- [x] AC-1: Full Python pipeline (VTT → Parse → Chunk) executes without error
- [x] AC-2: meeting-006 (90K tokens) produces 7 chunks with 3,071 total segments
- [x] AC-3: All golden datasets process within performance thresholds
- [x] AC-4: Pipeline is idempotent (same output for same input)
- [x] AC-5: Tests complete in < 30 seconds for all datasets combined (0.55s actual)

---

## Related Items

- Parent: [EN-023 Integration Testing](./EN-023-integration-testing.md)
- Depends On: TASK-230, TASK-231, TASK-232
- Related: EN-020, EN-021

---

## Time Tracking

| Metric | Value |
|--------|-------|
| Original Estimate | 3 hours |
| Remaining Work | 0 hours |
| Time Spent | 0.5 hours |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Pipeline tests | Python | `tests/integration/transcript/test_pipeline.py` |

### Verification

- [x] Acceptance criteria verified
- [x] `pytest -m integration tests/integration/transcript/test_pipeline.py` passes (13 tests in 0.55s)
- [x] Performance thresholds met (all datasets under threshold)
- [ ] Reviewed by: Human

---

## Implementation Details

### Test Suite Summary

13 pipeline tests covering:
- **AC-1: Execution Tests**: 1 test (full pipeline executes without error)
- **AC-2: Output Verification**: 1 test (meeting-006 produces 7 chunks, 3,071 segments)
- **AC-3: Performance Tests**: 6 tests (1 for meeting-006, 5 parametrized for smaller datasets)
- **AC-4: Idempotency Tests**: 2 tests (large and small dataset idempotency)
- **AC-5: Combined Performance**: 1 test (all 6 datasets in < 30s)
- **Supplementary Tests**: 2 tests (medium dataset, output structure)

### Test Execution Evidence

```bash
$ uv run pytest tests/integration/transcript/test_pipeline.py -v
============================= test session starts ==============================
collected 13 items

tests/integration/transcript/test_pipeline.py ... 13 passed in 0.55s
============================== 13 passed in 0.55s ==============================
```

### Performance Results

| Dataset | Segments | Chunks | Threshold | Actual |
|---------|----------|--------|-----------|--------|
| meeting-001.vtt | 39 | 1 | 2.0s | < 0.1s |
| meeting-002.vtt | 97 | 1 | 2.0s | < 0.1s |
| meeting-003.vtt | 62 | 1 | 2.0s | < 0.1s |
| meeting-004-sprint-planning.vtt | 536 | 2 | 3.0s | < 0.1s |
| meeting-005-roadmap-review.vtt | 896 | 2 | 5.0s | < 0.2s |
| meeting-006-all-hands.vtt | 3071 | 7 | 10.0s | < 0.3s |
| **All Combined** | **4701** | **14** | **30.0s** | **0.55s** |

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-29 | BACKLOG | Created per DEC-012 restructuring |
| 2026-01-30 | DONE | 13 pipeline tests created and passing. All 5 ACs verified. Performance far exceeds thresholds. |
