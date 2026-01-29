# TASK-220: Update ts-extractor.md Input Section

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
CREATED: 2026-01-29 (EN-022 Extractor Adaptation)
PURPOSE: Add chunked input format support to ts-extractor agent definition
-->

---

## Frontmatter

```yaml
# === IDENTITY ===
id: "TASK-220"
work_type: TASK

# === CORE METADATA ===
title: "Update ts-extractor.md Input Section"
description: |
  Add new "Input Formats" section to ts-extractor.md documenting support for
  both legacy single-file input and new chunked input from EN-021. Define
  Format A (single file) and Format B (chunked) with usage guidance.

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
created_at: "2026-01-29T20:30:00Z"
updated_at: "2026-01-29T20:30:00Z"

# === HIERARCHY ===
parent_id: "EN-022"

# === TAGS ===
tags:
  - "ts-extractor"
  - "documentation"
  - "input-formats"

# === DELIVERY ITEM PROPERTIES ===
effort: 2
acceptance_criteria: |
  AC-1: ts-extractor.md contains new "Input Formats" section after "Capabilities"
  AC-2: Format A (single file) documented with path, use case, and constraints
  AC-3: Format B (chunked) documented with index.json and chunk files
  AC-4: Recommendation guidance: chunked for >1000 segments
due_date: null

# === TASK-SPECIFIC PROPERTIES ===
activity: DOCUMENTATION
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

The ts-extractor agent definition currently assumes a single `canonical-transcript.json` input file. With the chunking infrastructure from EN-021, the agent needs documentation for two input formats:

1. **Format A (Legacy)** - Single canonical-transcript.json for small transcripts
2. **Format B (Chunked)** - Index + chunk files for large transcripts

### Implementation Details

Add the following section to `ts-extractor.md` after the "Capabilities" section:

```markdown
## Input Formats

The extractor supports two input formats. Choose based on transcript size.

### Format A: Single File (Legacy)

**Use when:** Transcript has < 1000 segments

```yaml
input:
  format: single_file
  path: canonical-transcript.json
  constraints:
    - Entire transcript loaded into context
    - Suitable for transcripts < 30,000 tokens
```

### Format B: Chunked (Recommended)

**Use when:** Transcript has ≥ 1000 segments

```yaml
input:
  format: chunked
  index_path: index.json
  chunks_path: chunks/
  constraints:
    - Read index.json first for metadata
    - Load chunks selectively based on task
    - Each chunk ≤ 500 segments
```

### Format Selection Decision Tree

```
Segments count?
    │
    ├─ < 1000 → Format A (Single File)
    │              └─ Simpler, full context
    │
    └─ ≥ 1000 → Format B (Chunked)
                   └─ Selective loading, better accuracy
```
```

### File to Modify

- `skills/transcript/agents/ts-extractor.md`

---

## Acceptance Criteria

- [x] AC-1: ts-extractor.md contains new "Input Formats" section after "Capabilities"
- [x] AC-2: Format A (single file) documented with path, use case, and constraints
- [x] AC-3: Format B (chunked) documented with index.json and chunk files
- [x] AC-4: Recommendation guidance: chunked for >1000 segments

---

## Related Items

- Parent: [EN-022 Extractor Adaptation](./EN-022-extractor-adaptation.md)
- Depends On: EN-021 (provides chunk format schemas)
- Related: TASK-221 (chunked processing protocol)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| ts-extractor.md (updated) | Agent Definition | `skills/transcript/agents/ts-extractor.md` |

### Verification

- [x] Acceptance criteria verified
- [x] Section appears in correct location in agent definition (after Capabilities, before Processing Instructions)
- [ ] Reviewed by: Human

---

## History

| Date       | Status      | Notes                          |
|------------|-------------|--------------------------------|
| 2026-01-29 | BACKLOG     | Task created from EN-022       |
| 2026-01-29 | DONE        | Added Input Formats section to ts-extractor.md with Format A (single file), Format B (chunked), decision tree, and auto-detection logic. |

---
