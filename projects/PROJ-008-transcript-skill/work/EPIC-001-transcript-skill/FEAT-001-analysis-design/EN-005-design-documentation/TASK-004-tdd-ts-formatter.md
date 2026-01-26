# TASK-004: TDD - ts-formatter Agent Design

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
-->

---

## Frontmatter

```yaml
# === IDENTITY (Auto-generated, Immutable) ===
id: "TASK-004"
work_type: TASK

# === CORE METADATA ===
title: "Create TDD: ts-formatter Agent Design"
description: |
  Design the output-formatter (ts-formatter) agent responsible for:
  - Packet structure generation per ADR-002
  - File splitting logic per ADR-004
  - Anchor registry management per ADR-003
  - Backlinks generation
  - Token counting and enforcement

# === CLASSIFICATION ===
classification: ENABLER

# === LIFECYCLE STATE ===
status: DONE
resolution: completed

# === PRIORITY ===
priority: HIGH

# === PEOPLE ===
assignee: "ps-architect"
created_by: "Claude"

# === TIMESTAMPS ===
created_at: "2026-01-26T10:00:00Z"
updated_at: "2026-01-26T10:00:00Z"

# === HIERARCHY ===
parent_id: "EN-005"

# === TAGS ===
tags:
  - "tdd"
  - "ts-formatter"
  - "phase-1"

# === DELIVERY ITEM PROPERTIES ===
effort: 3
acceptance_criteria: |
  See Acceptance Criteria section below
due_date: null

# === TASK-SPECIFIC PROPERTIES ===
activity: DESIGN
original_estimate: 4
remaining_work: 4
time_spent: 0
```

---

## State Machine

**Initial State:** `BACKLOG`

**Valid States:** `BACKLOG`, `IN_PROGRESS`, `BLOCKED`, `DONE`, `REMOVED`

---

## Containment Rules

| Rule             | Value                           |
|------------------|---------------------------------|
| Allowed Children | Subtask                         |
| Allowed Parents  | Enabler                         |
| Max Depth        | 1                               |

---

## Content

### Description

Design the ts-formatter agent that handles the final stage of transcript processing - output generation. This agent implements the most ADR decisions (ADR-002, ADR-003, ADR-004).

**Core Responsibilities:**
1. **Packet Structure Generation:** Create hierarchical output per ADR-002
2. **File Splitting Logic:** Semantic boundary split per ADR-004 (31.5K soft limit)
3. **Anchor Registry Management:** Custom anchors per ADR-003
4. **Backlinks Generation:** Bidirectional linking
5. **Token Counting:** Monitor and enforce limits
6. **Index File Generation:** Create 00-index.md for navigation

**Requirements Coverage (from EN-003):**
- FR-012: Markdown Output Generation
- FR-013: Packet Structure Creation
- FR-014: File Splitting
- FR-015: Index Generation
- NFR-009: Token Budget Compliance (35K hard, 31.5K soft)
- NFR-010: Navigation Support
- IR-004: Backlink Format
- IR-005: Anchor Naming Convention

**Risk Mitigation (from FMEA):**
- R-014: Schema breaking changes - versioned schema per PAT-005

### Acceptance Criteria

- [ ] **AC-001:** Packet structure matches ADR-002 (00-index.md, 01-summary.md, etc.)
- [ ] **AC-002:** Split logic follows ADR-004 (31.5K soft limit, split at ## headings)
- [ ] **AC-003:** Anchor naming per ADR-003 conventions (`{type}-{nnn}`)
- [ ] **AC-004:** Backlinks template defined with `<backlinks>` section
- [ ] **AC-005:** Token counting algorithm specified (tiktoken-compatible)
- [ ] **AC-006:** Sample packet structure diagram
- [ ] **AC-007:** Split algorithm flowchart
- [ ] **AC-008:** L0/L1/L2 perspectives complete per DEC-001-001
- [ ] **AC-009:** ADR Compliance Checklist (ADR-001..005) complete
- [ ] **AC-010:** File created at `docs/TDD-ts-formatter.md`

### Dependencies

| Type | Item | Status |
|------|------|--------|
| Blocked By | TASK-001 TDD Overview | PENDING |
| Blocked By | TASK-002 TDD ts-parser | PENDING |
| Blocked By | TASK-003 TDD ts-extractor | PENDING |
| Enables | TASK-007 ts-formatter AGENT.md | Requires this design |

### Implementation Notes

**Design Patterns to Implement:**
- PAT-004: Citation-Required Extraction (backlinks verification)
- PAT-005: Versioned Schema Evolution
- PAT-006: Hexagonal Skill Architecture

**ADR-002 Packet Structure:**
```
transcript-{id}/
├── 00-index.md          # Navigation hub (~2K tokens)
├── 01-summary.md        # Executive summary (~5K tokens)
├── 02-transcript.md     # Full transcript (may split)
├── 03-speakers.md       # Speaker directory
├── 04-action-items.md   # Action items extracted
├── 05-decisions.md      # Decisions extracted
├── 06-questions.md      # Questions extracted
└── 07-topics.md         # Topic segments
```

**ADR-004 Split Algorithm:**
```
function shouldSplit(content, tokenCount):
  SOFT_LIMIT = 31500  # 90% of 35K
  HARD_LIMIT = 35000

  if tokenCount < SOFT_LIMIT:
    return false

  # Find nearest ## heading before soft limit
  splitPoint = findNearestHeading(content, SOFT_LIMIT)

  if splitPoint exists:
    return splitAt(splitPoint)
  else:
    # Force split at hard limit
    return forceSplitAt(HARD_LIMIT)
```

**ADR-003 Anchor Registry:**
```yaml
anchors:
  - id: "speaker-001"
    type: "speaker"
    file: "03-speakers.md"
    line: 15
  - id: "action-001"
    type: "action"
    file: "04-action-items.md"
    line: 8
  # ...

backlinks:
  "speaker-001":
    - file: "02-transcript.md"
      line: 42
    - file: "04-action-items.md"
      line: 12
```

### Related Items

- Parent: [EN-005 Design Documentation](./EN-005-design-documentation.md)
- Depends On: [TASK-001 TDD Overview](./TASK-001-tdd-overview.md)
- Depends On: [TASK-002 TDD ts-parser](./TASK-002-tdd-ts-parser.md)
- Depends On: [TASK-003 TDD ts-extractor](./TASK-003-tdd-ts-extractor.md)
- Related: [FR-012..015, NFR-009..010, IR-004..005](../EN-003-requirements-synthesis/requirements/REQUIREMENTS-SPECIFICATION.md)

---

## Time Tracking

| Metric            | Value           |
|-------------------|-----------------|
| Original Estimate | 4 hours         |
| Remaining Work    | 4 hours         |
| Time Spent        | 0 hours         |

---

## Evidence

### Deliverables

| Deliverable | Type | Link | Status |
|-------------|------|------|--------|
| TDD-ts-formatter.md | Technical Design Document | docs/TDD-ts-formatter.md | PENDING |

### Verification

- [ ] Acceptance criteria verified
- [ ] Sample packet structure diagram
- [ ] Split algorithm flowchart validated
- [ ] Anchor registry schema validated
- [ ] Reviewed by: TBD

---

## History

| Date       | Status      | Notes                          |
|------------|-------------|--------------------------------|
| 2026-01-26 | Created     | Initial task creation          |

---

*Task ID: TASK-004*
*Workflow ID: en005-tdd-20260126-001*
*Constitutional Compliance: P-002 (persisted), P-004 (provenance)*
