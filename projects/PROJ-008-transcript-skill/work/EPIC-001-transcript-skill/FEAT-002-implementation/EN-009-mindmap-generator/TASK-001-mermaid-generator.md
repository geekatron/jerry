# TASK-001: Create Mermaid Generator Agent

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
CREATED: 2026-01-28 per DEC-003:AI-004
-->

---

## Frontmatter

```yaml
# === IDENTITY ===
id: "TASK-001"
work_type: TASK

# === CORE METADATA ===
title: "Create Mermaid Generator Agent"
description: |
  Implement the Mermaid mindmap generator that transforms extracted entities
  into valid Mermaid mindmap syntax. The generator creates hierarchical
  visualizations with topic nodes, entity connections, and deep links to
  source transcript locations.

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
created_at: "2026-01-28T14:00:00Z"
updated_at: "2026-01-28T14:00:00Z"

# === HIERARCHY ===
parent_id: "EN-009"

# === TAGS ===
tags:
  - "mermaid"
  - "visualization"
  - "mindmap"
  - "agent"

# === DELIVERY ITEM PROPERTIES ===
effort: 3
acceptance_criteria: |
  - Generates valid Mermaid mindmap syntax
  - Topics form hierarchical structure from extraction data
  - Entities connected to appropriate topic nodes
  - Deep links embedded per ADR-003
due_date: null

# === TASK-SPECIFIC PROPERTIES ===
activity: DEVELOPMENT
original_estimate: 6
remaining_work: 6
time_spent: 0
```

---

## Content

### Description

Create the Mermaid mindmap generator agent (`ts-mindmap-mermaid`) that:

1. **Consumes** ts-formatter output (8-file packet from EN-016)
2. **Transforms** extracted entities into hierarchical mindmap structure
3. **Outputs** valid Mermaid mindmap syntax with deep links

### Input Requirements

The agent receives:
- Extraction report JSON from ts-extractor
- Topic segmentation from ts-extractor
- 8-file packet structure from ts-formatter

### Output Specification

**File:** `07-mindmap/mindmap.mmd`

```mermaid
mindmap
  root((Meeting Title))
    Topic 1
      Subtopic A
        [Action: Task description](#action-001)
      Subtopic B
        [Question: What about X?](#question-001)
    Topic 2
      [Decision: Approved Y](#decision-001)
    Speakers
      Alice
        ::icon(fa fa-user)
      Bob
        ::icon(fa fa-user)
```

### Acceptance Criteria

- [x] **AC-1:** Generates valid Mermaid mindmap syntax (parseable by mermaid-cli)
- [x] **AC-2:** Root node contains meeting title/date
- [x] **AC-3:** Level 1 nodes are main topics from topic segmentation
- [x] **AC-4:** Level 2+ nodes contain subtopics and entities
- [x] **AC-5:** Action items include assignee in node text
- [x] **AC-6:** Questions show answered/unanswered status
- [x] **AC-7:** Decisions include rationale summary
- [x] **AC-8:** All entity nodes have deep links per ADR-003 format
- [x] **AC-9:** Handles 50+ topics without syntax errors
- [x] **AC-10:** Speaker nodes grouped under "Speakers" branch

### Implementation Notes

**Agent Definition Location:** `skills/transcript/agents/ts-mindmap-mermaid.md`

**Key Design Decisions:**
- Per ADR-005: Prompt-based implementation (no Python code)
- Per ADR-003: Deep links use `#entity-type-NNN` anchor format
- Per TDD-ts-formatter: Input is 8-file packet from EN-016

**Node Sizing Rules:**
- Root: Double parentheses `((text))`
- Topics: Square brackets `[text]`
- Entities: Plain text with link `[text](#anchor)`

### Related Items

- **Parent:** [EN-009](./EN-009-mindmap-generator.md)
- **Blocked By:** [EN-016](../EN-016-ts-formatter/EN-016-ts-formatter.md) (ts-formatter must complete first)
- **Blocks:** [TASK-003](./TASK-003-deep-link-embedding.md), [TASK-004](./TASK-004-unit-tests.md)
- **Reference:** [ADR-003](../../FEAT-001-analysis-design/EN-004-architecture-decisions/docs/adrs/adr-003.md) (Bidirectional Linking)

---

## Time Tracking

| Metric            | Value |
|-------------------|-------|
| Original Estimate | 6 hours |
| Remaining Work    | 6 hours |
| Time Spent        | 0 hours |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Agent definition | Markdown | skills/transcript/agents/ts-mindmap-mermaid.md |
| Sample output | Mermaid | skills/transcript/test_data/outputs/sample-mindmap.mmd |

### Verification

- [ ] Acceptance criteria verified
- [ ] Mermaid syntax validates with mermaid-cli
- [ ] Deep links resolve correctly
- [ ] Reviewed by: {REVIEWER}

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-28 | Created | Per DEC-003:AI-004 - enabler-scoped numbering |
| 2026-01-28 | DONE | Agent definition created: skills/transcript/agents/ts-mindmap-mermaid.md |
