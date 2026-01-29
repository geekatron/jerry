# TASK-221: Add Chunked Processing Protocol

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
CREATED: 2026-01-29 (EN-022 Extractor Adaptation)
PURPOSE: Document the step-by-step protocol for processing chunked transcripts
-->

---

## Frontmatter

```yaml
# === IDENTITY ===
id: "TASK-221"
work_type: TASK

# === CORE METADATA ===
title: "Add Chunked Processing Protocol"
description: |
  Add a new "Chunked Processing Protocol" section to ts-extractor.md that defines
  the step-by-step workflow for extracting entities from chunked transcripts.
  Covers reading index, planning extraction, processing chunks, and merging results.

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
  - "chunked-processing"
  - "protocol"

# === DELIVERY ITEM PROPERTIES ===
effort: 3
acceptance_criteria: |
  AC-1: Chunked Processing Protocol section added to ts-extractor.md
  AC-2: Step 1 (Read Index) documented with required metadata
  AC-3: Step 2 (Plan Extraction) documented with task-based decisions
  AC-4: Step 3 (Process Chunks) documented with iteration and citation rules
  AC-5: Step 4 (Merge Results) documented with deduplication and aggregation
due_date: null

# === TASK-SPECIFIC PROPERTIES ===
activity: DOCUMENTATION
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

When processing chunked transcripts (Format B), the extractor must follow a specific workflow to efficiently extract entities while preserving citations. This task documents that protocol.

### Protocol Steps

#### Step 1: Read Index

```yaml
action: Read index.json
extracts:
  - total_segments: For progress tracking
  - total_chunks: For iteration planning
  - speakers.list: Initial speaker registry
  - speakers.segment_counts: Speaker distribution
  - chunks[].timestamp_range: For topic correlation
  - topics_preview: For selective loading
```

#### Step 2: Plan Extraction

```yaml
action: Decide which chunks to process based on task
strategies:
  action_items: process_all  # Can appear anywhere
  decisions: process_all     # Can appear anywhere
  questions: process_all     # Distributed throughout
  speakers: index_only       # Available from index metadata
  topics: selective          # Use topics_preview hints
```

#### Step 3: Process Chunks

```yaml
action: Iterate through required chunks
for_each_chunk:
  - Load chunk-NNN.json
  - Extract entities using existing pipeline
  - Preserve segment_id for citations
  - Track chunk_id in entity metadata
  - Release chunk from context before loading next
```

#### Step 4: Merge Results

```yaml
action: Combine extractions from all chunks
operations:
  - Aggregate speakers (may span chunks)
  - Deduplicate entities by content similarity
  - Maintain citation chains
  - Calculate confidence_summary across all
  - Update extraction_stats totals
```

### File to Modify

- `skills/transcript/agents/ts-extractor.md`

---

## Acceptance Criteria

- [x] AC-1: Chunked Processing Protocol section added to ts-extractor.md
- [x] AC-2: Step 1 (Read Index) documented with required metadata
- [x] AC-3: Step 2 (Plan Extraction) documented with task-based decisions
- [x] AC-4: Step 3 (Process Chunks) documented with iteration and citation rules
- [x] AC-5: Step 4 (Merge Results) documented with deduplication and aggregation

---

## Related Items

- Parent: [EN-022 Extractor Adaptation](./EN-022-extractor-adaptation.md)
- Depends On: TASK-220 (input formats section)
- Related: TASK-222 (chunk selection strategies)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| ts-extractor.md (updated) | Agent Definition | `skills/transcript/agents/ts-extractor.md` |

### Verification

- [ ] Acceptance criteria verified
- [ ] Protocol steps are clear and actionable
- [ ] Reviewed by: Human

---

## History

| Date       | Status      | Notes                          |
|------------|-------------|--------------------------------|
| 2026-01-29 | BACKLOG     | Task created from EN-022       |
| 2026-01-29 | DONE        | Added comprehensive Chunked Processing Protocol with 4 steps: Read Index, Plan Extraction, Process Chunks, Merge Results. Includes code examples and YAML specifications. |

---
