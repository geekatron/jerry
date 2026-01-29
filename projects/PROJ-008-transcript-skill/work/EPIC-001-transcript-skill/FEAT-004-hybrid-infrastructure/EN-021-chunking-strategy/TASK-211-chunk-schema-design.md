# TASK-211: Chunk Schema Design

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
CREATED: 2026-01-29 (EN-021 Chunking Strategy)
PURPOSE: Define formal JSON Schema for chunk-NNN.json per TDD-FEAT-004 Section 5
-->

---

## Frontmatter

```yaml
# === IDENTITY ===
id: "TASK-211"
work_type: TASK

# === CORE METADATA ===
title: "Chunk Schema Design"
description: |
  Define formal JSON Schema for chunk-NNN.json files that contain segments
  and navigation links. Schema must be compatible with index.json and
  support LLM-efficient processing.

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
created_at: "2026-01-29T20:00:00Z"
updated_at: "2026-01-29T20:00:00Z"

# === HIERARCHY ===
parent_id: "EN-021"

# === TAGS ===
tags:
  - "json-schema"
  - "chunk"
  - "segments"
  - "navigation"

# === DELIVERY ITEM PROPERTIES ===
effort: 2
acceptance_criteria: |
  AC-1: JSON Schema Draft 2020-12 compliant chunk-NNN.json schema
  AC-2: Schema includes required fields: chunk_id, schema_version, segment_range, segments
  AC-3: Schema includes navigation links (previous, next, index)
  AC-4: Segment schema compatible with EN-020 ParsedSegment
  AC-5: Schema file created at skills/transcript/test_data/schemas/chunk.schema.json
due_date: null

# === TASK-SPECIFIC PROPERTIES ===
activity: DESIGN
original_estimate: 2
remaining_work: 2
time_spent: null
```

---

## State Machine

**Current State:** `BACKLOG`

---

## Description

### Problem

Each chunk file (chunk-001.json, chunk-002.json, etc.) must follow a consistent schema that:
- Contains a batch of segments (typically 500)
- Provides navigation links to adjacent chunks
- Maintains segment integrity from canonical format
- Enables LLM agents to process chunks independently

### Technical Reference

**TDD-FEAT-004 Section 5 Chunk File Required Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| chunk_id | string | YES | Unique chunk identifier (e.g., "chunk-001") |
| schema_version | string | YES | Must be "1.0" |
| segment_range | array | YES | [start_id, end_id] inclusive |
| timestamp_range | object | YES | {start_ms, end_ms} |
| segments | array | YES | Array of segment objects |
| navigation | object | YES | {previous, next, index} links |

---

## Acceptance Criteria

- [x] AC-1: JSON Schema Draft 2020-12 compliant chunk schema created
- [x] AC-2: Schema includes required fields per TDD-FEAT-004 Section 5
- [x] AC-3: Schema includes navigation links (previous, next, index)
- [x] AC-4: Segment schema compatible with EN-020 ParsedSegment
- [x] AC-5: Schema file created at `skills/transcript/test_data/schemas/chunk.schema.json`

---

## Related Items

- Parent: [EN-021 Chunking Strategy](./EN-021-chunking-strategy.md)
- Depends On: TASK-210 (Index Schema Design)
- Blocks: TASK-212 (Chunking Algorithm)
- Reference: TDD-FEAT-004 Section 5

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| chunk.schema.json | JSON Schema | `skills/transcript/test_data/schemas/chunk.schema.json` |

### Verification

- [ ] Schema validates TDD-FEAT-004 Section 5 chunk example
- [ ] Segment schema compatible with ParsedSegment
- [ ] Reviewed by: Human

---

## History

| Date       | Status      | Notes                          |
|------------|-------------|--------------------------------|
| 2026-01-29 | BACKLOG     | Task created from EN-021       |
| 2026-01-29 | DONE        | Schema created. Draft 2020-12 compliant. Segment compatible with ParsedSegment. |
