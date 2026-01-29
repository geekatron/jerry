# TASK-232: Chunker Output Contract Tests

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
CREATED: 2026-01-29 (EN-023 Integration Testing)
PURPOSE: Contract tests validating chunker output schemas
-->

---

## Frontmatter

```yaml
# === IDENTITY ===
id: "TASK-232"
work_type: TASK

# === CORE METADATA ===
title: "Chunker Output Contract Tests"
description: |
  Create contract tests validating that TranscriptChunker output
  conforms to the JSON schemas defined in EN-021:
  - index.json schema validation
  - chunk-NNN.json schema validation
  - Cross-reference integrity between index and chunks

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
  - "contract"
  - "schema"
  - "validation"
  - "CI"

# === DELIVERY ITEM PROPERTIES ===
effort: 2
acceptance_criteria: |
  AC-1: index.json output validates against index-schema.json
  AC-2: All chunk-NNN.json files validate against chunk-schema.json
  AC-3: Cross-references between index and chunks are consistent
  AC-4: Segment ID ranges are non-overlapping and complete
  AC-5: Tests use jsonschema library for validation
due_date: null

# === TASK-SPECIFIC PROPERTIES ===
activity: TESTING
original_estimate: 2
remaining_work: 2
time_spent: null
```

---

## State Machine

**Current State:** `BACKLOG`

---

## Description

### Purpose

Contract tests ensure the TranscriptChunker output maintains compatibility with downstream consumers (ts-extractor). These are **deterministic Python tests** that run in CI.

### Schemas to Validate

**From EN-021:**
- `skills/transcript/test_data/schemas/index-schema.json`
- `skills/transcript/test_data/schemas/chunk-schema.json`

### Test Cases

```python
# tests/contract/transcript/test_chunker_schemas.py

import pytest
import json
from pathlib import Path
from jsonschema import validate, ValidationError
from src.transcript.infrastructure.adapters.vtt_parser import VTTParser
from src.transcript.application.services.chunker import TranscriptChunker

@pytest.mark.contract
class TestChunkerOutputSchemas:
    """Contract tests for chunker output schema compliance."""

    @pytest.fixture
    def index_schema(self) -> dict:
        schema_path = Path("skills/transcript/test_data/schemas/index-schema.json")
        with open(schema_path) as f:
            return json.load(f)

    @pytest.fixture
    def chunk_schema(self) -> dict:
        schema_path = Path("skills/transcript/test_data/schemas/chunk-schema.json")
        with open(schema_path) as f:
            return json.load(f)

    @pytest.fixture
    def chunked_output(self, temp_output_dir) -> Path:
        """Generate chunked output from meeting-006."""
        parser = VTTParser()
        chunker = TranscriptChunker()

        vtt_path = Path("skills/transcript/test_data/transcripts/golden/meeting-006-all-hands.vtt")
        canonical = parser.parse(vtt_path)
        return chunker.chunk(canonical, temp_output_dir)

    def test_index_json_validates_against_schema(
        self, chunked_output, index_schema
    ):
        """Verify index.json conforms to index-schema.json."""
        index_path = chunked_output
        with open(index_path) as f:
            index_data = json.load(f)

        # Should not raise ValidationError
        validate(instance=index_data, schema=index_schema)

    def test_all_chunks_validate_against_schema(
        self, chunked_output, chunk_schema
    ):
        """Verify all chunk-NNN.json files conform to chunk-schema.json."""
        chunks_dir = chunked_output.parent / "chunks"

        for chunk_file in chunks_dir.glob("chunk-*.json"):
            with open(chunk_file) as f:
                chunk_data = json.load(f)

            # Should not raise ValidationError
            validate(instance=chunk_data, schema=chunk_schema)

    def test_index_chunk_cross_references(self, chunked_output):
        """Verify index references match actual chunk files."""
        with open(chunked_output) as f:
            index = json.load(f)

        chunks_dir = chunked_output.parent / "chunks"
        actual_chunks = set(p.name for p in chunks_dir.glob("chunk-*.json"))
        index_chunks = set(c["chunk_id"] + ".json" for c in index["chunks"])

        assert actual_chunks == index_chunks, "Index and filesystem chunks mismatch"

    def test_segment_ranges_non_overlapping(self, chunked_output):
        """Verify segment ID ranges don't overlap between chunks."""
        with open(chunked_output) as f:
            index = json.load(f)

        all_ranges = []
        for chunk_meta in index["chunks"]:
            start, end = chunk_meta["segment_range"]
            all_ranges.append((start, end))

        # Sort by start and check no overlaps
        all_ranges.sort()
        for i in range(len(all_ranges) - 1):
            current_end = all_ranges[i][1]
            next_start = all_ranges[i + 1][0]
            assert next_start > current_end, f"Overlap at chunk boundary {i}"

    def test_segment_ranges_complete(self, chunked_output):
        """Verify segment ranges cover all segments without gaps."""
        with open(chunked_output) as f:
            index = json.load(f)

        total_segments = index["summary"]["total_segments"]

        # Verify first chunk starts at 1
        first_range = index["chunks"][0]["segment_range"]
        assert first_range[0] == 1, "First chunk should start at segment 1"

        # Verify last chunk ends at total_segments
        last_range = index["chunks"][-1]["segment_range"]
        assert last_range[1] == total_segments, "Last chunk should end at total_segments"

        # Verify no gaps
        all_ranges = sorted(c["segment_range"] for c in index["chunks"])
        for i in range(len(all_ranges) - 1):
            current_end = all_ranges[i][1]
            next_start = all_ranges[i + 1][0]
            assert next_start == current_end + 1, f"Gap between chunks at segment {current_end}"
```

---

## Acceptance Criteria

- [ ] AC-1: index.json output validates against index-schema.json
- [ ] AC-2: All chunk-NNN.json files validate against chunk-schema.json
- [ ] AC-3: Cross-references between index and chunks are consistent
- [ ] AC-4: Segment ID ranges are non-overlapping and complete
- [ ] AC-5: Tests use jsonschema library for validation

---

## Related Items

- Parent: [EN-023 Integration Testing](./EN-023-integration-testing.md)
- Depends On: TASK-230 (test infrastructure)
- Related: EN-021 (chunking strategy, schemas)
- Schemas: `skills/transcript/test_data/schemas/`

---

## Time Tracking

| Metric | Value |
|--------|-------|
| Original Estimate | 2 hours |
| Remaining Work | 2 hours |
| Time Spent | - |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Contract tests | Python | `tests/contract/transcript/test_chunker_schemas.py` |

### Verification

- [ ] Acceptance criteria verified
- [ ] `pytest -m contract tests/contract/transcript/` passes
- [ ] Reviewed by: Human

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-29 | BACKLOG | Created per DEC-012 restructuring |
