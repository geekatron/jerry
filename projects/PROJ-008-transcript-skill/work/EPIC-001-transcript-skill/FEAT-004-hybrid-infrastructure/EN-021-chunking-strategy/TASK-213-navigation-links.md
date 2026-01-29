# TASK-213: Navigation Links

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
CREATED: 2026-01-29 (EN-021 Chunking Strategy)
PURPOSE: Add prev/next chunk pointers for navigation
-->

---

## Frontmatter

```yaml
# === IDENTITY ===
id: "TASK-213"
work_type: TASK

# === CORE METADATA ===
title: "Navigation Links"
description: |
  Add bidirectional navigation links between chunks and back-links to index.
  Enables LLM agents to traverse chunks without loading the full index.

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
created_at: "2026-01-29T20:00:00Z"
updated_at: "2026-01-29T20:00:00Z"

# === HIERARCHY ===
parent_id: "EN-021"

# === TAGS ===
tags:
  - "navigation"
  - "linking"
  - "ux"

# === DELIVERY ITEM PROPERTIES ===
effort: 2
acceptance_criteria: |
  AC-1: Each chunk has "navigation" object with previous, next, index fields
  AC-2: First chunk has previous: null
  AC-3: Last chunk has next: null
  AC-4: All chunks have index: "index.json"
  AC-5: Navigation links validated by unit tests
due_date: null

# === TASK-SPECIFIC PROPERTIES ===
activity: DEVELOPMENT
original_estimate: 2
remaining_work: 2
time_spent: null
```

---

## State Machine

**Current State:** `DONE`

---

## Description

### Problem

LLM agents need to navigate between chunks without loading the full index. Each chunk should provide:
- Link to previous chunk (or null for first)
- Link to next chunk (or null for last)
- Link back to index for metadata lookup

### Solution

Add navigation object to each chunk file:

```json
{
  "chunk_id": "chunk-003",
  "navigation": {
    "previous": "chunks/chunk-002.json",
    "next": "chunks/chunk-004.json",
    "index": "index.json"
  }
}
```

### Edge Cases

| Chunk | Previous | Next |
|-------|----------|------|
| chunk-001 | null | chunks/chunk-002.json |
| chunk-002 | chunks/chunk-001.json | chunks/chunk-003.json |
| chunk-007 (last) | chunks/chunk-006.json | null |

---

## Acceptance Criteria

- [x] AC-1: Each chunk has "navigation" object with previous, next, index fields
- [x] AC-2: First chunk has previous: null
- [x] AC-3: Last chunk has next: null
- [x] AC-4: All chunks have index: "../index.json"
- [x] AC-5: Navigation links validated by unit tests (4 tests in TestChunkerNavigation)

---

## Related Items

- Parent: [EN-021 Chunking Strategy](./EN-021-chunking-strategy.md)
- Depends On: TASK-212 (Chunking Algorithm)
- Blocks: TASK-214 (Unit Tests)

---

## Evidence

### Verification

- [ ] Navigation links match chunk order
- [ ] First/last chunk edge cases handled
- [ ] Relative paths work from chunk directory
- [ ] Reviewed by: Human

---

## History

| Date       | Status      | Notes                          |
|------------|-------------|--------------------------------|
| 2026-01-29 | BACKLOG     | Task created from EN-021       |
| 2026-01-29 | DONE        | Navigation implemented as part of TASK-212. 4 dedicated tests verify all ACs. |
