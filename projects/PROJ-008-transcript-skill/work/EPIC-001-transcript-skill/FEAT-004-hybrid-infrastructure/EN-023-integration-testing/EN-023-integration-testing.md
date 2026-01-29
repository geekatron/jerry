# EN-023: Integration Testing

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-01-28 (FEAT-004 Hybrid Infrastructure)
PURPOSE: End-to-end integration testing of hybrid architecture
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Enabler Type:** compliance
> **Created:** 2026-01-28T22:00:00Z
> **Due:** TBD
> **Completed:** -
> **Parent:** FEAT-004
> **Owner:** Claude
> **Effort:** 5

---

## Frontmatter

```yaml
id: "EN-023"
work_type: ENABLER
title: "Integration Testing"
classification: ENABLER
status: pending
priority: medium
impact: medium
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-28T22:00:00Z"
updated_at: "2026-01-28T22:00:00Z"
parent_id: "FEAT-004"
tags: ["enabler", "testing", "integration", "compliance"]
effort: 5
enabler_type: compliance
nfrs: ["NFR-003", "NFR-010"]
```

---

## Summary

Comprehensive end-to-end integration testing of the hybrid architecture, validating that Python parsing + chunking + LLM extraction produces complete, accurate results for all test datasets including the 90K token meeting-006-all-hands.vtt.

**Technical Value:**
- Validates complete pipeline
- Ensures no data loss
- Confirms quality thresholds
- Regression prevention

---

## Problem Statement

The hybrid architecture introduces new integration points:

1. **Python Parser → Chunker** - Data format compatibility
2. **Chunker → LLM Extractor** - Index/chunk reading
3. **End-to-End Pipeline** - Complete workflow validation

Each integration point needs testing to ensure:
- Data integrity maintained
- No segments lost
- Citations accurate
- Quality scores meet thresholds

---

## Technical Approach

### Test Datasets

| Dataset | Size | Segments | Purpose |
|---------|------|----------|---------|
| meeting-001 | 5K tokens | ~100 | Smoke test |
| meeting-002 | 15K tokens | ~500 | Small transcript |
| meeting-003 | 25K tokens | ~800 | Medium transcript |
| meeting-004 | 25K tokens | ~800 | Sprint planning format |
| meeting-005 | 45K tokens | ~1,500 | Roadmap review format |
| meeting-006 | 90K tokens | ~3,071 | Large all-hands (primary) |

### Integration Test Suite

```python
# tests/integration/test_hybrid_pipeline.py

class TestHybridPipeline:
    """Integration tests for hybrid parsing architecture."""

    def test_parser_to_chunker_data_integrity(self):
        """Verify no segments lost in parsing and chunking."""
        transcript = vtt_parser.parse("meeting-006.vtt")
        index_path = chunker.chunk(transcript, output_dir)

        # Load all chunks
        total_segments = sum(
            len(json.load(chunk)["segments"])
            for chunk in Path(output_dir / "chunks").glob("*.json")
        )

        assert total_segments == len(transcript.segments)
        assert total_segments == 3071

    def test_chunker_to_extractor_compatibility(self):
        """Verify extractor can read chunked format."""
        # Parse and chunk
        transcript = vtt_parser.parse("meeting-006.vtt")
        index_path = chunker.chunk(transcript, output_dir)

        # Verify index readable
        with open(index_path) as f:
            index = json.load(f)

        assert index["summary"]["total_segments"] == 3071
        assert index["summary"]["total_chunks"] == 7
        assert len(index["chunks"]) == 7

    def test_end_to_end_extraction_quality(self):
        """Verify extraction quality meets thresholds."""
        # Run full pipeline
        result = run_hybrid_pipeline("meeting-006.vtt")

        # Verify quality metrics
        assert result.extraction_report["action_items_found"] >= 9
        assert result.extraction_report["decisions_found"] >= 5
        assert result.quality_score >= 0.90

    def test_citation_accuracy(self):
        """Verify all citations reference valid segments."""
        result = run_hybrid_pipeline("meeting-006.vtt")

        for entity in result.all_entities:
            assert entity.citation.segment_id is not None
            assert 1 <= entity.citation.segment_id <= 3071
```

### Contract Tests

```yaml
# Integration contract tests

parser_output_contract:
  segments: array[Segment]
  speakers: array[string]
  duration_ms: integer >= 0

chunker_index_contract:
  schema_version: "1.0"
  summary:
    total_segments: integer > 0
    total_chunks: integer > 0
  chunks: array[ChunkMetadata]

chunker_chunk_contract:
  chunk_id: string matching "chunk-NNN"
  segments: array[Segment]
  navigation:
    previous: string | null
    next: string | null

extractor_input_contract:
  accepts:
    - canonical-transcript.json (legacy)
    - index.json + chunks/ (hybrid)
```

---

## NFRs Addressed

| NFR | Requirement | How Addressed |
|-----|-------------|---------------|
| NFR-003 | 85% precision/recall | End-to-end validation |
| NFR-010 | Quality >= 0.90 | ps-critic integration |

---

## Children (Tasks)

| ID | Title | Status | Priority |
|----|-------|--------|----------|
| TASK-180 | Create integration test fixtures | pending | high |
| TASK-181 | Parser → Chunker data integrity tests | pending | high |
| TASK-182 | Chunker → Extractor compatibility tests | pending | high |
| TASK-183 | End-to-end pipeline tests | pending | high |
| TASK-184 | Citation accuracy validation | pending | medium |
| TASK-185 | ps-critic quality gate test | pending | high |

---

## Acceptance Criteria

### Definition of Done

- [ ] Integration test suite complete
- [ ] All 6 datasets tested
- [ ] meeting-006 produces complete output (3,071 segments)
- [ ] ps-critic quality score >= 0.90
- [ ] CI/CD pipeline integration

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | Parser → Chunker: Zero segment loss | [ ] |
| AC-2 | Chunker → Extractor: Format compatible | [ ] |
| AC-3 | End-to-end: meeting-006 completes | [ ] |
| AC-4 | End-to-end: Quality >= 0.90 | [ ] |
| AC-5 | All citations valid | [ ] |

---

## Dependencies

| Type | Item | Description |
|------|------|-------------|
| Depends On | EN-020 | Python parser implementation |
| Depends On | EN-021 | Chunking strategy |
| Depends On | EN-022 | Extractor adaptation |
| Related | EN-015 | Transcript validation framework |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-28 | Claude | pending | Enabler created from DISC-009 |

---

## Metadata

```yaml
id: "EN-023"
parent_id: "FEAT-004"
work_type: ENABLER
title: "Integration Testing"
status: pending
priority: medium
impact: medium
enabler_type: compliance
tags: ["testing", "integration", "compliance"]
```
