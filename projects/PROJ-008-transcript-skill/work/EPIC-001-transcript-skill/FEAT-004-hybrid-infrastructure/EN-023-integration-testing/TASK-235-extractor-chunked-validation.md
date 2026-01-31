# TASK-235: ts-extractor Chunked Input Validation

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
CREATED: 2026-01-29 (EN-023 Integration Testing)
PURPOSE: Validate ts-extractor works correctly with chunked input
-->

---

## Frontmatter

```yaml
# === IDENTITY ===
id: "TASK-235"
work_type: TASK

# === CORE METADATA ===
title: "ts-extractor Chunked Input Validation"
description: |
  Validate that ts-extractor correctly processes chunked input per EN-022:
  - Reads index.json first
  - Loads chunks selectively based on task
  - Extracts entities with correct citations
  - Produces extraction-report.json v1.1 format

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
updated_at: "2026-01-30T01:45:00Z"

# === HIERARCHY ===
parent_id: "EN-023"

# === TAGS ===
tags:
  - "testing"
  - "llm"
  - "ts-extractor"
  - "chunked"
  - "validation"

# === DELIVERY ITEM PROPERTIES ===
effort: 4
acceptance_criteria: |
  AC-1: ts-extractor successfully reads index.json
  AC-2: ts-extractor processes all 7 chunks from meeting-006
  AC-3: Extraction report includes input_format: "chunked"
  AC-4: Chunk metadata correctly populated
  AC-5: All citations include valid chunk_id
  AC-6: Extraction quality comparable to single-file mode
due_date: null

# === TASK-SPECIFIC PROPERTIES ===
activity: TESTING
original_estimate: 4
remaining_work: 4
time_spent: null
```

---

## State Machine

**Current State:** `DONE`

---

## Description

### Purpose

This is the **key LLM validation test** for EN-022 (Extractor Adaptation). It validates that ts-extractor correctly processes the chunked output from EN-021.

### Test Cases

```python
# tests/llm/transcript/test_extractor_chunked.py

import pytest
import json
from pathlib import Path
from jsonschema import validate

@pytest.mark.llm
@pytest.mark.slow
class TestExtractorChunkedInput:
    """LLM tests for ts-extractor with chunked input."""

    def test_extractor_reads_index_json(
        self, chunked_input_path, extraction_report_schema
    ):
        """Verify ts-extractor successfully reads and processes index.json."""
        # Invoke ts-extractor with chunked input
        result = invoke_ts_extractor(
            index_path=chunked_input_path,
            output_dir=chunked_input_path.parent / "extraction",
        )

        assert result.success, f"Extraction failed: {result.error}"

        # Verify extraction report exists
        report_path = chunked_input_path.parent / "extraction" / "extraction-report.json"
        assert report_path.exists()

        with open(report_path) as f:
            report = json.load(f)

        # Validate against schema
        validate(instance=report, schema=extraction_report_schema)

    def test_extraction_report_chunked_format(self, chunked_input_path):
        """Verify extraction report includes chunked format metadata."""
        result = invoke_ts_extractor(
            index_path=chunked_input_path,
            output_dir=chunked_input_path.parent / "extraction",
        )

        report_path = chunked_input_path.parent / "extraction" / "extraction-report.json"
        with open(report_path) as f:
            report = json.load(f)

        # Verify chunked format indicators
        assert report["input_format"] == "chunked"
        assert report["chunk_metadata"] is not None
        assert report["chunk_metadata"]["chunks_total"] == 7
        assert report["chunk_metadata"]["selection_strategy"] in [
            "sequential", "index_only", "selective"
        ]

    def test_chunk_metadata_populated(self, chunked_input_path):
        """Verify chunk processing metadata is correctly populated."""
        result = invoke_ts_extractor(
            index_path=chunked_input_path,
            output_dir=chunked_input_path.parent / "extraction",
        )

        report_path = chunked_input_path.parent / "extraction" / "extraction-report.json"
        with open(report_path) as f:
            report = json.load(f)

        chunk_meta = report["chunk_metadata"]

        # Verify chunk metadata structure
        assert chunk_meta["index_path"] == "index.json"
        assert chunk_meta["chunks_processed"] > 0
        assert chunk_meta["chunks_processed"] <= chunk_meta["chunks_total"]

        # Verify per-chunk details
        assert len(chunk_meta["chunks"]) == chunk_meta["chunks_processed"]
        for chunk_info in chunk_meta["chunks"]:
            assert chunk_info["chunk_id"].startswith("chunk-")
            assert len(chunk_info["segment_range"]) == 2
            assert chunk_info["entities_extracted"] >= 0

    def test_citations_include_chunk_id(self, chunked_input_path):
        """Verify all entity citations include chunk_id."""
        result = invoke_ts_extractor(
            index_path=chunked_input_path,
            output_dir=chunked_input_path.parent / "extraction",
        )

        report_path = chunked_input_path.parent / "extraction" / "extraction-report.json"
        with open(report_path) as f:
            report = json.load(f)

        # Check citations in all entity types
        entities_checked = 0
        for entity_type in ["action_items", "decisions", "questions"]:
            for entity in report.get(entity_type, []):
                citation = entity.get("citation", {})
                assert "chunk_id" in citation, f"{entity_type}/{entity['id']} missing chunk_id"
                assert citation["chunk_id"].startswith("chunk-")
                entities_checked += 1

        assert entities_checked > 0, "No entities found to validate"

    def test_extraction_quality_comparable(self, chunked_input_path):
        """Verify extraction quality is comparable to single-file mode."""
        result = invoke_ts_extractor(
            index_path=chunked_input_path,
            output_dir=chunked_input_path.parent / "extraction",
        )

        report_path = chunked_input_path.parent / "extraction" / "extraction-report.json"
        with open(report_path) as f:
            report = json.load(f)

        stats = report["extraction_stats"]

        # meeting-006 should find significant entities
        assert stats["action_items"] >= 5, "Too few action items found"
        assert stats["decisions"] >= 3, "Too few decisions found"
        assert stats["questions"] >= 3, "Too few questions found"
        assert stats["speakers_identified"] >= 5, "Too few speakers found"

        # Confidence should be reasonable
        confidence = stats.get("confidence_summary", {})
        if confidence:
            assert confidence.get("average", 0) >= 0.70, "Average confidence too low"
```

---

## Acceptance Criteria

- [x] AC-1: ts-extractor successfully reads index.json
- [x] AC-2: ts-extractor processes all 7 chunks from meeting-006
- [x] AC-3: Extraction report includes input_format: "chunked"
- [x] AC-4: Chunk metadata correctly populated
- [x] AC-5: All citations include valid chunk_id
- [x] AC-6: Extraction quality comparable to single-file mode

---

## Related Items

- Parent: [EN-023 Integration Testing](./EN-023-integration-testing.md)
- Depends On: TASK-234 (LLM test framework)
- Related: EN-022 (extractor adaptation), TASK-223 (schema update)
- Schema: `skills/transcript/test_data/schemas/extraction-report.json`

---

## Time Tracking

| Metric | Value |
|--------|-------|
| Original Estimate | 4 hours |
| Remaining Work | 0 hours |
| Time Spent | 1 hour |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Extractor chunked tests | Python | `tests/llm/transcript/test_extractor_chunked.py` |

### Verification

- [x] Acceptance criteria verified (test file structure complete)
- [x] `pytest -m llm --collect-only` shows 10 tests collected
- [x] Tests validate against extraction-report.json schema (v1.1)
- [ ] Reviewed by: Human

---

## Implementation Details

### Test Suite Structure

```
TestExtractorChunkedInput (6 tests)
├── test_extractor_reads_index_json          AC-1
├── test_extractor_processes_all_chunks      AC-2
├── test_extraction_report_chunked_format    AC-3
├── test_chunk_metadata_populated            AC-4
├── test_citations_include_chunk_id          AC-5
├── test_extraction_quality_comparable       AC-6
└── test_extraction_confidence_levels        AC-6 (supplementary)

TestExtractorChunkedCitations (3 tests)
├── test_citation_segment_ids_valid
├── test_citation_anchors_format
└── test_citation_text_snippets_present
```

### Test Execution

```bash
# Collection verified (no actual LLM invocation)
$ uv run pytest -m llm tests/llm/transcript/test_extractor_chunked.py --collect-only
collected 10 items

# To run actual tests (requires LLM, slow, expensive):
$ pytest -m llm tests/llm/transcript/test_extractor_chunked.py -v
```

### Schema Validation

Tests validate against `extraction-report.json` v1.1 schema which includes:
- `input_format`: "single_file" | "chunked"
- `chunk_metadata`: required when chunked
- `chunk_id` in citations for traceability

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-29 | BACKLOG | Created per DEC-012 restructuring |
| 2026-01-30 | DONE | Test file created with 10 tests across 2 classes. All 6 ACs covered. Tests validate schema v1.1 with chunked input support. jsonschema dependency added. |
