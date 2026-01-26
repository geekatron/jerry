# TASK-003: TDD - ts-extractor Agent Design

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
-->

---

## Frontmatter

```yaml
# === IDENTITY (Auto-generated, Immutable) ===
id: "TASK-003"
work_type: TASK

# === CORE METADATA ===
title: "Create TDD: ts-extractor Agent Design"
description: |
  Design the entity-extractor (ts-extractor) agent responsible for:
  - Speaker identification with multi-pattern detection
  - Action item extraction with confidence scoring
  - Decision recognition
  - Question extraction
  - Topic segmentation

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
  - "ts-extractor"
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

Design the ts-extractor agent that handles semantic entity extraction from parsed transcripts. This is the most complex agent implementing the Tiered Extraction Pipeline (PAT-001).

**Core Responsibilities:**
1. **Speaker Identification:** Multi-pattern detection with 4-pattern fallback chain (PAT-003)
2. **Action Item Detection:** Extract with assignee, due date, confidence
3. **Decision Recognition:** Capture decisions with context and rationale
4. **Question Extraction:** Identify open questions and who asked
5. **Topic Segmentation:** Detect topic boundaries in conversation

**Requirements Coverage (from EN-003):**
- FR-005: Speaker Identification
- FR-006: Action Item Extraction
- FR-007: Decision Recognition
- FR-008: Question Extraction
- FR-009: Topic Segmentation
- FR-010: Confidence Scoring
- FR-011: Citation Generation
- NFR-003: Extraction Accuracy (>85% precision/recall)
- NFR-004: Processing Time (<30s per transcript)
- NFR-008: Confidence Threshold (0.7 default)

**Risk Mitigation (from FMEA):**
- R-004: Missing voice tags - 4-pattern fallback chain
- R-006/R-007: Precision/Recall issues - confidence thresholds
- R-008: Hallucination - citation validation per PAT-004

### Acceptance Criteria

- [ ] **AC-001:** Entity types defined with JSON schemas
- [ ] **AC-002:** Extraction patterns documented (regex + semantic)
- [ ] **AC-003:** Tiered approach specified (rule → ML → LLM) per PAT-001
- [ ] **AC-004:** Confidence scoring mechanism defined (0.0-1.0 scale)
- [ ] **AC-005:** Citation format specified per ADR-003
- [ ] **AC-006:** 4-pattern speaker detection chain documented per PAT-003
- [ ] **AC-007:** Sample extractions for each entity type
- [ ] **AC-008:** L0/L1/L2 perspectives complete per DEC-001-001
- [ ] **AC-009:** ADR Compliance Checklist (ADR-001, ADR-002, ADR-003) complete
- [ ] **AC-010:** File created at `docs/TDD-ts-extractor.md`

### Dependencies

| Type | Item | Status |
|------|------|--------|
| Blocked By | TASK-001 TDD Overview | PENDING |
| Parallel | TASK-002 TDD ts-parser | Can run parallel after TASK-001 |
| Enables | TASK-004 TDD ts-formatter | Requires this output |
| Enables | TASK-006 ts-extractor AGENT.md | Requires this design |

### Implementation Notes

**Design Patterns to Implement:**
- PAT-001: Tiered Extraction Pipeline (Rule → ML → LLM)
- PAT-003: Multi-Pattern Speaker Detection (4-pattern fallback)
- PAT-004: Citation-Required Extraction (no hallucinations)

**Tiered Extraction Strategy:**
```
Tier 1: Rule-Based (Fast, High Precision)
├── Regex patterns for action items ("TODO:", "Action:")
├── Question marks for questions
└── Speaker label patterns

Tier 2: ML-Based (Medium Speed, Balanced)
├── NER for person names
├── Date extraction for due dates
└── Sentiment for decision polarity

Tier 3: LLM-Based (Slow, High Recall)
├── Semantic understanding for implicit actions
├── Context-aware speaker resolution
└── Topic boundary detection
```

**Entity JSON Schemas:**
```json
{
  "action_items": [{
    "id": "string",
    "text": "string",
    "assignee": "string|null",
    "due_date": "ISO8601|null",
    "confidence": "number (0.0-1.0)",
    "citation": "anchor reference per ADR-003"
  }],
  "decisions": [{
    "id": "string",
    "text": "string",
    "decided_by": "string|null",
    "confidence": "number",
    "citation": "anchor reference"
  }],
  "questions": [{
    "id": "string",
    "text": "string",
    "asked_by": "string|null",
    "answered": "boolean",
    "citation": "anchor reference"
  }],
  "topics": [{
    "id": "string",
    "title": "string",
    "start_ms": "number",
    "end_ms": "number"
  }]
}
```

### Related Items

- Parent: [EN-005 Design Documentation](./EN-005-design-documentation.md)
- Depends On: [TASK-001 TDD Overview](./TASK-001-tdd-overview.md)
- Related: [FR-005..011 Requirements](../EN-003-requirements-synthesis/requirements/REQUIREMENTS-SPECIFICATION.md)

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
| TDD-ts-extractor.md | Technical Design Document | docs/TDD-ts-extractor.md | PENDING |

### Verification

- [ ] Acceptance criteria verified
- [ ] Sample extractions for each entity type
- [ ] Pattern regex/rules documented
- [ ] Confidence scoring validated
- [ ] Reviewed by: TBD

---

## History

| Date       | Status      | Notes                          |
|------------|-------------|--------------------------------|
| 2026-01-26 | Created     | Initial task creation          |

---

*Task ID: TASK-003*
*Workflow ID: en005-tdd-20260126-001*
*Constitutional Compliance: P-002 (persisted), P-004 (provenance)*
