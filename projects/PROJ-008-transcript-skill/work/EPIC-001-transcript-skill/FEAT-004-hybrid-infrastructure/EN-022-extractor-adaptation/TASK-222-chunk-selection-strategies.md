# TASK-222: Document Chunk Selection Strategies

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
CREATED: 2026-01-29 (EN-022 Extractor Adaptation)
PURPOSE: Document strategies for selecting which chunks to process based on extraction task
-->

---

## Frontmatter

```yaml
# === IDENTITY ===
id: "TASK-222"
work_type: TASK

# === CORE METADATA ===
title: "Document Chunk Selection Strategies"
description: |
  Add documentation for chunk selection strategies that determine which chunks
  to load based on the extraction task. Different entity types require different
  approaches: some need all chunks, others can use index metadata only.

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
  - "chunk-selection"
  - "optimization"

# === DELIVERY ITEM PROPERTIES ===
effort: 2
acceptance_criteria: |
  AC-1: Chunk Selection Strategies section added to ts-extractor.md
  AC-2: Three strategies documented: sequential, index_only, selective
  AC-3: Task-to-strategy mapping table included
  AC-4: Rationale for each strategy explained
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

Different extraction tasks have different requirements for which chunks need to be processed. This task documents the three chunk selection strategies and when to use each.

### Selection Strategies

#### Strategy 1: Sequential (Process All)

```yaml
name: sequential
description: Process all chunks in order
use_when:
  - Entities can appear anywhere in transcript
  - No index metadata provides filtering hints
  - Comprehensive extraction required
cost: High (all chunks loaded)
accuracy: Highest (nothing missed)
```

**Applicable to:** action_items, decisions, questions

#### Strategy 2: Index Only

```yaml
name: index_only
description: Use index.json metadata without loading chunks
use_when:
  - Required data is available in index metadata
  - No need to see actual segment content
  - Optimization priority
cost: Minimal (only index.json)
accuracy: Full for aggregated data
```

**Applicable to:** speakers (count and list), summary statistics

#### Strategy 3: Selective

```yaml
name: selective
description: Load only chunks matching criteria
use_when:
  - Index provides hints (topics_preview, speaker_counts)
  - User requested specific timeframe or speaker
  - Optimization with targeted extraction
cost: Variable (only matching chunks)
accuracy: High for targeted scope
```

**Applicable to:** topic-specific extraction, speaker-focused queries

### Task-to-Strategy Mapping

| Extraction Task | Strategy | Rationale |
|-----------------|----------|-----------|
| action_items | sequential | Can appear in any segment |
| decisions | sequential | Context-dependent, distributed |
| questions | sequential | May occur throughout meeting |
| speakers | index_only | Full list in index.speakers |
| topics | selective | Use topics_preview for targeting |
| speaker-specific | selective | Use speaker_counts to find chunks |
| timeframe-specific | selective | Use timestamp_range in chunk metadata |

### File to Modify

- `skills/transcript/agents/ts-extractor.md`

---

## Acceptance Criteria

- [x] AC-1: Chunk Selection Strategies section added to ts-extractor.md
- [x] AC-2: Three strategies documented: sequential, index_only, selective
- [x] AC-3: Task-to-strategy mapping table included
- [x] AC-4: Rationale for each strategy explained

---

## Related Items

- Parent: [EN-022 Extractor Adaptation](./EN-022-extractor-adaptation.md)
- Depends On: TASK-221 (processing protocol uses strategies)
- Related: EN-021 (index.json structure with topics_preview)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| ts-extractor.md (updated) | Agent Definition | `skills/transcript/agents/ts-extractor.md` |

### Verification

- [ ] Acceptance criteria verified
- [ ] Strategy descriptions are clear
- [ ] Mapping table is complete
- [ ] Reviewed by: Human

---

## History

| Date       | Status      | Notes                          |
|------------|-------------|--------------------------------|
| 2026-01-29 | BACKLOG     | Task created from EN-022       |
| 2026-01-29 | DONE        | Added comprehensive Chunk Selection Strategies Reference section with detailed definitions for Sequential, Index Only, and Selective strategies. Includes Task-to-Strategy mapping table and decision flowchart. |

---
