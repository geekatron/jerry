# TASK-210: Index Schema Design

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
CREATED: 2026-01-29 (EN-021 Chunking Strategy)
PURPOSE: Define formal JSON Schema for index.json per TDD-FEAT-004 Section 5
-->

---

## Frontmatter

```yaml
# === IDENTITY ===
id: "TASK-210"
work_type: TASK

# === CORE METADATA ===
title: "Index Schema Design"
description: |
  Define formal JSON Schema for index.json that contains metadata and pointers
  to segment chunk files. Schema must support LLM-efficient chunk navigation
  and comply with JSON Schema Draft 2020-12 standard.

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
  - "index"
  - "chunking"
  - "infrastructure"

# === DELIVERY ITEM PROPERTIES ===
effort: 2
acceptance_criteria: |
  AC-1: JSON Schema Draft 2020-12 compliant index.json schema
  AC-2: Schema includes required fields: schema_version, total_segments, total_chunks, chunk_size, chunks
  AC-3: Schema includes source metadata (file, format, encoding)
  AC-4: Schema validates against TDD-FEAT-004 Section 5 specification
  AC-5: Schema file created at skills/transcript/test_data/schemas/index.schema.json
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

| From State    | Allowed Transitions                    |
|---------------|----------------------------------------|
| BACKLOG       | IN_PROGRESS, REMOVED                   |
| IN_PROGRESS   | BLOCKED, DONE, REMOVED                 |
| BLOCKED       | IN_PROGRESS, REMOVED                   |
| DONE          | IN_PROGRESS (Reopen)                   |
| REMOVED       | (Terminal)                             |

---

## Description

### Problem

EN-021 Chunking Strategy requires a formal JSON Schema for the index.json file that:
- Contains transcript metadata (source, format, encoding, duration)
- Provides chunk navigation (pointers to chunk files)
- Summarizes speakers and their segment counts
- Enables selective chunk loading to reduce LLM context usage

### Solution

Define a JSON Schema Draft 2020-12 compliant schema based on TDD-FEAT-004 Section 5 specification. The schema must be strict enough to catch malformed files but flexible enough to support future extensions.

### Technical Reference

**TDD-FEAT-004 Section 5 Index.json Required Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| schema_version | string | YES | Must be "1.0" |
| total_segments | integer | YES | Total segment count in source |
| total_chunks | integer | YES | Number of chunk files |
| chunk_size | integer | YES | Target segments per chunk (default: 500) |
| chunks | array | YES | Array of chunk metadata objects |
| source_file | string | NO | Original source filename |
| source_format | string | NO | Format (vtt, srt, txt) |
| generated_at | string | NO | ISO 8601 timestamp |
| duration_ms | integer | NO | Total duration in milliseconds |
| speakers | object | NO | Speaker summary metadata |

---

## Acceptance Criteria

- [x] AC-1: JSON Schema Draft 2020-12 compliant index.json schema created
- [x] AC-2: Schema includes required fields per TDD-FEAT-004 Section 5
- [x] AC-3: Schema includes source metadata (file, format, encoding)
- [x] AC-4: Schema validates against TDD-FEAT-004 Section 5 example
- [x] AC-5: Schema file created at `skills/transcript/test_data/schemas/index.schema.json`

---

## Implementation Notes

### Schema Location

```
skills/transcript/test_data/schemas/
├── index.schema.json        # Index file schema (this task)
├── chunk.schema.json        # Chunk file schema (TASK-211)
└── canonical-transcript.json # Existing parser output schema
```

### Validation Approach

1. Schema must validate the example index.json from TDD-FEAT-004 Section 5
2. Use JSON Schema $ref for reusable definitions
3. Use additionalProperties: false for strict validation in production

---

## Related Items

- Parent: [EN-021 Chunking Strategy](./EN-021-chunking-strategy.md)
- Depends On: EN-020 Python Parser (complete)
- Blocks: TASK-211 (Chunk Schema Design), TASK-212 (Chunking Algorithm)
- Reference: TDD-FEAT-004 Section 5

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| index.schema.json | JSON Schema | `skills/transcript/test_data/schemas/index.schema.json` |

### Verification

- [ ] Schema validates TDD-FEAT-004 Section 5 example
- [ ] Schema Draft 2020-12 compliance verified
- [ ] Reviewed by: Human

---

## History

| Date       | Status      | Notes                          |
|------------|-------------|--------------------------------|
| 2026-01-29 | BACKLOG     | Task created from EN-021       |
| 2026-01-29 | DONE        | Schema created. Draft 2020-12 compliant. Validated with jsonschema library. |
