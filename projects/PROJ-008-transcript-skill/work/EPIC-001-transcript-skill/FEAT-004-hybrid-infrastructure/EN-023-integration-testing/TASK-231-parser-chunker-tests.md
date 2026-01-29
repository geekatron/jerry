# TASK-231: Parser → Chunker Integration Tests

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
CREATED: 2026-01-29 (EN-023 Integration Testing)
PURPOSE: Integration tests for VTTParser → TranscriptChunker pipeline
-->

---

## Frontmatter

```yaml
# === IDENTITY ===
id: "TASK-231"
work_type: TASK

# === CORE METADATA ===
title: "Parser → Chunker Integration Tests"
description: |
  Create integration tests validating the VTTParser → TranscriptChunker pipeline:
  - Data integrity (zero segment loss)
  - Speaker count preservation
  - Timestamp continuity across chunks
  - All golden datasets tested

# === CLASSIFICATION ===
classification: ENABLER

# === LIFECYCLE STATE ===
status: BACKLOG
resolution: null

# === PRIORITY ===
priority: HIGH

# === PEOPLE ===
assignee: "Claude"
created_by: "Claude"

# === TIMESTAMPS ===
created_at: "2026-01-29T21:30:00Z"
updated_at: "2026-01-29T21:30:00Z"

# === HIERARCHY ===
parent_id: "EN-023"

# === TAGS ===
tags:
  - "testing"
  - "integration"
  - "parser"
  - "chunker"
  - "CI"

# === DELIVERY ITEM PROPERTIES ===
effort: 3
acceptance_criteria: |
  AC-1: Zero segment loss in parser → chunker handoff (all 6 datasets)
  AC-2: Speaker counts match between parser output and chunker index
  AC-3: Timestamps are continuous across chunk boundaries
  AC-4: meeting-006 (3,071 segments) processes correctly into 7 chunks
  AC-5: Tests pass with pytest -m integration marker
due_date: null

# === TASK-SPECIFIC PROPERTIES ===
activity: TESTING
original_estimate: 3
remaining_work: 3
time_spent: null
```

---

## State Machine

**Current State:** `BACKLOG`

---

## Description

### Purpose

These tests validate the integration point between VTTParser (EN-020) and TranscriptChunker (EN-021). They are **Python-only tests** that run in CI without LLM invocation.

### Test Matrix

| Dataset | Segments | Expected Chunks | Test Focus |
|---------|----------|-----------------|------------|
| meeting-001 | ~100 | 1 | Small file baseline |
| meeting-002 | ~500 | 1 | Near chunk boundary |
| meeting-003 | ~800 | 2 | Multi-chunk |
| meeting-004 | ~800 | 2 | Sprint planning format |
| meeting-005 | ~1,500 | 3 | Roadmap review |
| meeting-006 | 3,071 | 7 | Large all-hands (primary) |

### Test Cases

```python
# tests/integration/transcript/test_parser_chunker.py

import pytest
from pathlib import Path
from src.transcript.infrastructure.adapters.vtt_parser import VTTParser
from src.transcript.application.services.chunker import TranscriptChunker

@pytest.mark.integration
class TestParserChunkerIntegration:
    """Integration tests for Parser → Chunker pipeline."""

    @pytest.fixture
    def parser(self) -> VTTParser:
        return VTTParser()

    @pytest.fixture
    def chunker(self) -> TranscriptChunker:
        return TranscriptChunker()

    def test_zero_segment_loss_meeting_006(
        self, parser, chunker, golden_vtt_path, temp_output_dir
    ):
        """Verify no segments lost in parser → chunker handoff."""
        # Parse
        canonical = parser.parse(golden_vtt_path)
        original_count = len(canonical.segments)

        # Chunk
        index_path = chunker.chunk(canonical, temp_output_dir)

        # Load all chunks and count segments
        chunks_dir = temp_output_dir / "chunks"
        total_segments = 0
        for chunk_file in sorted(chunks_dir.glob("chunk-*.json")):
            with open(chunk_file) as f:
                chunk = json.load(f)
            total_segments += len(chunk["segments"])

        assert total_segments == original_count
        assert total_segments == 3071  # Known count for meeting-006

    def test_speaker_count_preservation(
        self, parser, chunker, golden_vtt_path, temp_output_dir
    ):
        """Verify speaker counts match between parser and chunker index."""
        canonical = parser.parse(golden_vtt_path)
        parser_speakers = set(canonical.speakers)

        index_path = chunker.chunk(canonical, temp_output_dir)
        with open(index_path) as f:
            index = json.load(f)
        chunker_speakers = set(index["summary"]["speakers"])

        assert chunker_speakers == parser_speakers

    def test_timestamp_continuity(
        self, parser, chunker, golden_vtt_path, temp_output_dir
    ):
        """Verify timestamps are continuous across chunks."""
        canonical = parser.parse(golden_vtt_path)
        index_path = chunker.chunk(canonical, temp_output_dir)

        chunks_dir = temp_output_dir / "chunks"
        prev_end_ms = 0

        for chunk_file in sorted(chunks_dir.glob("chunk-*.json")):
            with open(chunk_file) as f:
                chunk = json.load(f)

            first_segment = chunk["segments"][0]
            last_segment = chunk["segments"][-1]

            # First segment should start at or after previous chunk end
            assert first_segment["start_ms"] >= prev_end_ms
            prev_end_ms = last_segment["end_ms"]

    @pytest.mark.parametrize("dataset,expected_chunks", [
        ("meeting-001.vtt", 1),
        ("meeting-002.vtt", 1),
        ("meeting-003.vtt", 2),
        ("meeting-004-sprint-planning.vtt", 2),
        ("meeting-005-roadmap-review.vtt", 3),
        ("meeting-006-all-hands.vtt", 7),
    ])
    def test_all_datasets_chunk_correctly(
        self, parser, chunker, dataset, expected_chunks, temp_output_dir
    ):
        """Verify all golden datasets produce expected chunk counts."""
        vtt_path = Path(f"skills/transcript/test_data/transcripts/golden/{dataset}")
        if not vtt_path.exists():
            pytest.skip(f"Dataset {dataset} not available")

        canonical = parser.parse(vtt_path)
        index_path = chunker.chunk(canonical, temp_output_dir / dataset)

        with open(index_path) as f:
            index = json.load(f)

        assert index["summary"]["total_chunks"] == expected_chunks
```

---

## Acceptance Criteria

- [ ] AC-1: Zero segment loss in parser → chunker handoff (all 6 datasets)
- [ ] AC-2: Speaker counts match between parser output and chunker index
- [ ] AC-3: Timestamps are continuous across chunk boundaries
- [ ] AC-4: meeting-006 (3,071 segments) processes correctly into 7 chunks
- [ ] AC-5: Tests pass with pytest -m integration marker

---

## Related Items

- Parent: [EN-023 Integration Testing](./EN-023-integration-testing.md)
- Depends On: TASK-230 (test infrastructure)
- Related: EN-020 (VTTParser), EN-021 (TranscriptChunker)

---

## Time Tracking

| Metric | Value |
|--------|-------|
| Original Estimate | 3 hours |
| Remaining Work | 3 hours |
| Time Spent | - |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Parser-Chunker tests | Python | `tests/integration/transcript/test_parser_chunker.py` |

### Verification

- [ ] Acceptance criteria verified
- [ ] `pytest -m integration tests/integration/transcript/test_parser_chunker.py` passes
- [ ] All 6 datasets pass
- [ ] Reviewed by: Human

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-29 | BACKLOG | Created per DEC-012 restructuring |
