# TASK-223: Update Extraction Report Schema

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
CREATED: 2026-01-29 (EN-022 Extractor Adaptation)
PURPOSE: Update extraction-report.json schema to include chunk metadata
-->

---

## Frontmatter

```yaml
# === IDENTITY ===
id: "TASK-223"
work_type: TASK

# === CORE METADATA ===
title: "Update Extraction Report Schema"
description: |
  Update the extraction-report.json schema to include metadata about chunk
  processing. This enables downstream consumers to understand which chunks
  were processed and how entities map back to source chunks.

# === CLASSIFICATION ===
classification: ENABLER

# === LIFECYCLE STATE ===
status: DONE
resolution: COMPLETED

# === PRIORITY ===
priority: MEDIUM

# === PEOPLE ===
assignee: "Claude"
created_by: "Claude"

# === TIMESTAMPS ===
created_at: "2026-01-29T20:30:00Z"
updated_at: "2026-01-29T20:30:00Z"

# === HIERARCHY ===
parent_id: "EN-022"

# === TAGS ===
tags:
  - "ts-extractor"
  - "schema"
  - "extraction-report"

# === DELIVERY ITEM PROPERTIES ===
effort: 2
acceptance_criteria: |
  AC-1: extraction-report.json includes input_format field (single_file | chunked)
  AC-2: For chunked format, includes chunks_processed metadata
  AC-3: Entity citations include chunk_id for traceability
  AC-4: Schema in ts-extractor.md Output Schema section updated
  AC-5: Backward compatible (single_file format unchanged)
due_date: null

# === TASK-SPECIFIC PROPERTIES ===
activity: DOCUMENTATION
original_estimate: 2
remaining_work: 2
time_spent: null
```

---

## State Machine

**Current State:** `DONE`

---

## Description

### Purpose

When the extractor processes chunked input, the extraction report should capture which chunks were processed and include chunk_id in citations. This enables:

1. **Traceability** - Know which chunk each entity came from
2. **Debugging** - Identify if specific chunks had issues
3. **Optimization** - Track which selection strategy was used

### Schema Updates

#### New Fields in extraction-report.json

```json
{
  "version": "1.1",
  "input_format": "chunked",  // NEW: "single_file" | "chunked"
  "chunk_metadata": {         // NEW: Only present for chunked format
    "index_path": "index.json",
    "chunks_processed": 7,
    "chunks_total": 7,
    "selection_strategy": "sequential",
    "chunks": [
      {
        "chunk_id": "chunk-001",
        "segment_range": [1, 500],
        "entities_extracted": 5
      }
    ]
  },
  "extraction_stats": { ... },
  ...
}
```

#### Updated Citation Schema

```json
{
  "citation": {
    "segment_id": "seg-042",
    "chunk_id": "chunk-001",   // NEW: For chunked input
    "anchor": "#seg-042",
    "timestamp_ms": 930000,
    "text_snippet": "Bob, can you send me the report by Friday?"
  }
}
```

### Files to Update

1. `skills/transcript/agents/ts-extractor.md` - Output Schema section
2. `skills/transcript/test_data/schemas/extraction-report.json` - If exists, or create

### Backward Compatibility

For single-file input:
- `input_format` = "single_file"
- `chunk_metadata` = null (omitted)
- `citation.chunk_id` = null (omitted)

---

## Acceptance Criteria

- [x] AC-1: extraction-report.json includes input_format field (single_file | chunked)
- [x] AC-2: For chunked format, includes chunks_processed metadata
- [x] AC-3: Entity citations include chunk_id for traceability
- [x] AC-4: Schema in ts-extractor.md Output Schema section updated
- [x] AC-5: Backward compatible (single_file format unchanged)

---

## Related Items

- Parent: [EN-022 Extractor Adaptation](./EN-022-extractor-adaptation.md)
- Depends On: TASK-221 (protocol determines what metadata to capture)
- Related: EN-021 (chunk_id format must match)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| ts-extractor.md (updated) | Agent Definition | `skills/transcript/agents/ts-extractor.md` |
| extraction-report.json | JSON Schema | `skills/transcript/test_data/schemas/extraction-report.json` |

### Verification

- [ ] Acceptance criteria verified
- [ ] Schema changes are backward compatible
- [ ] chunk_id format matches EN-021 chunk naming
- [ ] Reviewed by: Human

---

## History

| Date       | Status      | Notes                          |
|------------|-------------|--------------------------------|
| 2026-01-29 | BACKLOG     | Task created from EN-022       |
| 2026-01-29 | DONE        | Updated ts-extractor.md Output Schema (v1.1 with chunk metadata, citation.chunk_id, topic.chunk_ids). Updated extraction-report.json schema with ChunkMetadata, ChunkProcessingInfo, conditional validation. Backward compatible with single_file format. |

---
