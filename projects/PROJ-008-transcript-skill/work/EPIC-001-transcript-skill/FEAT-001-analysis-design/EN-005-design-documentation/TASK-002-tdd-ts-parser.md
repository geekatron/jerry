# TASK-002: TDD - ts-parser Agent Design

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
-->

---

## Frontmatter

```yaml
# === IDENTITY (Auto-generated, Immutable) ===
id: "TASK-002"
work_type: TASK

# === CORE METADATA ===
title: "Create TDD: ts-parser Agent Design"
description: |
  Design the transcript-parser (ts-parser) agent responsible for:
  - VTT/SRT/TXT format detection and parsing
  - Timestamp normalization
  - Canonical transcript JSON schema generation
  - Error handling for malformed input

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
  - "ts-parser"
  - "phase-1"

# === DELIVERY ITEM PROPERTIES ===
effort: 2
acceptance_criteria: |
  See Acceptance Criteria section below
due_date: null

# === TASK-SPECIFIC PROPERTIES ===
activity: DESIGN
original_estimate: 3
remaining_work: 3
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

Design the ts-parser agent that handles the first stage of transcript processing. This agent is responsible for:
1. **Format Detection:** Identify VTT, SRT, or plain text formats
2. **Parsing Logic:** Extract speaker labels, timestamps, and utterances
3. **Normalization:** Convert all timestamps to canonical millisecond format
4. **Schema Generation:** Output well-defined JSON structure

**Requirements Coverage (from EN-003):**
- FR-001: VTT Parsing
- FR-002: SRT Parsing
- FR-003: Plain Text Parsing
- FR-004: Format Auto-Detection
- NFR-006: Timestamp Normalization (10ms precision)
- NFR-007: Large File Handling (60+ minute transcripts)

**Risk Mitigation (from FMEA):**
- R-002: SRT timestamp issues - defensive parsing per PAT-002

### Acceptance Criteria

- [ ] **AC-001:** Input formats documented (VTT, SRT, TXT) with grammar/BNF
- [ ] **AC-002:** Canonical JSON schema defined with JSON Schema validation
- [ ] **AC-003:** Parsing algorithm documented with flowchart
- [ ] **AC-004:** Error cases enumerated (malformed timestamps, missing speakers, etc.)
- [ ] **AC-005:** Token budget compliance: <5K per agent invocation
- [ ] **AC-006:** Timestamp normalization logic per NFR-006
- [ ] **AC-007:** PAT-002 (Defensive Parsing) pattern implemented
- [ ] **AC-008:** L0/L1/L2 perspectives complete per DEC-001-001
- [ ] **AC-009:** ADR Compliance Checklist (ADR-001, ADR-002) complete
- [ ] **AC-010:** File created at `docs/TDD-ts-parser.md`

### Dependencies

| Type | Item | Status |
|------|------|--------|
| Blocked By | TASK-001 TDD Overview | PENDING |
| Parallel | TASK-003 TDD ts-extractor | Can run parallel after TASK-001 |
| Enables | TASK-004 TDD ts-formatter | Requires this output |
| Enables | TASK-005 ts-parser AGENT.md | Requires this design |

### Implementation Notes

**Key Design Patterns:**
- PAT-002: Defensive Parsing - Handle malformed input gracefully
- Multi-format support with single canonical output

**JSON Schema Requirements:**
```json
{
  "transcript_id": "string",
  "format_detected": "VTT|SRT|TXT",
  "duration_ms": "number",
  "utterances": [
    {
      "speaker": "string|null",
      "start_ms": "number",
      "end_ms": "number",
      "text": "string"
    }
  ]
}
```

**Error Handling Matrix:**
| Error | Detection | Recovery |
|-------|-----------|----------|
| Malformed timestamp | Regex validation | Log warning, use best-effort |
| Missing speaker | Pattern match fail | Use "UNKNOWN" placeholder |
| Empty utterance | Empty text check | Skip with warning |
| Encoding issues | Decode exception | Try common encodings |

### Related Items

- Parent: [EN-005 Design Documentation](./EN-005-design-documentation.md)
- Depends On: [TASK-001 TDD Overview](./TASK-001-tdd-overview.md)
- Related: [FR-001..004 Requirements](../EN-003-requirements-synthesis/requirements/REQUIREMENTS-SPECIFICATION.md)

---

## Time Tracking

| Metric            | Value           |
|-------------------|-----------------|
| Original Estimate | 3 hours         |
| Remaining Work    | 3 hours         |
| Time Spent        | 0 hours         |

---

## Evidence

### Deliverables

| Deliverable | Type | Link | Status |
|-------------|------|------|--------|
| TDD-ts-parser.md | Technical Design Document | docs/TDD-ts-parser.md | PENDING |

### Verification

- [ ] Acceptance criteria verified
- [ ] JSON schema validated against sample transcripts
- [ ] Error handling matrix complete
- [ ] Reviewed by: TBD

---

## History

| Date       | Status      | Notes                          |
|------------|-------------|--------------------------------|
| 2026-01-26 | Created     | Initial task creation          |

---

*Task ID: TASK-002*
*Workflow ID: en005-tdd-20260126-001*
*Constitutional Compliance: P-002 (persisted), P-004 (provenance)*
