# TASK-106: Implement Enhanced Error Capture Mechanism

<!--
TEMPLATE: Task
VERSION: 1.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-007 (ts-parser Agent Implementation)
CREATED: 2026-01-27 per W3C WebVTT research and TDD-ts-parser v1.2
-->

---

## Frontmatter

```yaml
id: "TASK-106"
work_type: TASK
title: "Implement Enhanced Error Capture Mechanism"
description: |
  Implement the enhanced error capture mechanism per TDD-ts-parser.md v1.2 Section 6.1.
  This enables PAT-002 Defensive Parsing to surface warnings, errors, and skipped segments
  to downstream consumers without failing the overall parse.

  Source: W3C WebVTT research (EN-007:DISC-002) identified need for robust error capture
  to handle edge cases like empty cues, malformed timestamps, and invalid voice tags.

classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-27T20:00:00Z"
updated_at: "2026-01-27T20:00:00Z"

parent_id: "EN-007"

tags:
  - "implementation"
  - "ts-parser"
  - "error-handling"
  - "PAT-002"

effort: 2
acceptance_criteria: |
  - parse_metadata object added to canonical output schema
  - parse_status field captures complete|partial|failed states
  - parse_warnings array captures non-fatal issues (WARN-*)
  - parse_errors array captures recoverable errors (ERR-*)
  - skipped_segments array captures omitted cues (SKIP-*)
  - All error codes from TDD-ts-parser.md v1.2 implemented
  - ts-parser.md agent definition updated with error capture behavior

due_date: null

activity: DEVELOPMENT
original_estimate: 4
remaining_work: 4
time_spent: 0
```

---

## State Machine

**Current State:** `BACKLOG`

**State History:**
- 2026-01-27: BACKLOG (created per W3C WebVTT research)

---

## Content

### Description

Implement the enhanced error capture mechanism defined in TDD-ts-parser.md v1.2 Section 6.1. This task enables PAT-002 (Defensive Parsing) to surface detailed error information to downstream consumers.

### Background

During W3C WebVTT research (EN-007:DISC-002), edge case testing revealed the need for a robust error capture mechanism. The parser must:

1. Continue parsing despite individual segment errors
2. Capture and categorize all issues encountered
3. Surface error details to downstream consumers (ts-extractor)
4. Enable quality assessment of parsed output

### Requirements (from TDD-ts-parser.md v1.2)

#### parse_metadata Schema

```json
{
  "parse_metadata": {
    "parse_status": "partial|complete|failed",
    "parse_warnings": [...],
    "parse_errors": [...],
    "skipped_segments": [...]
  }
}
```

#### Error Code Implementation

| Code | Category | Description | Implementation |
|------|----------|-------------|----------------|
| WARN-001 | Timestamp | Malformed timestamp, best-effort parsed | Regex fallback |
| WARN-002 | Timestamp | Negative duration, times swapped | Swap start/end |
| WARN-003 | Encoding | Fallback encoding used | Encoding chain |
| WARN-004 | Voice Tag | Class annotation stripped | Strip `.class` |
| ERR-001 | Voice Tag | Invalid syntax, extracted as anonymous | Null speaker |
| ERR-002 | Payload | Empty after tag stripping | Skip segment |
| ERR-003 | Structure | Malformed cue structure | Best effort |
| SKIP-001 | Payload | Empty cue text | Skip |
| SKIP-002 | Payload | Whitespace-only payload | Skip |
| SKIP-003 | Voice Tag | Empty voice annotation | Anonymous |

### Acceptance Criteria

- [ ] `parse_metadata` object added to canonical output
- [ ] `parse_status` correctly set based on error count
- [ ] All WARN-* codes captured with context (cue_index, raw_value)
- [ ] All ERR-* codes captured with recovery_action
- [ ] All SKIP-* codes captured with reason
- [ ] ts-parser.md agent definition updated (Section: Error Handling)
- [ ] Edge case tests (vtt-013, vtt-014) validate error capture
- [ ] Unit tests for each error code scenario

### Test Cases

Reference test cases that exercise error capture:

| Test ID | File | Error Types |
|---------|------|-------------|
| vtt-013 | `empty_and_malformed.vtt` | SKIP-001, SKIP-002, SKIP-003 |
| vtt-014 | `combined_edge_cases.vtt` | All error types |

### Related Items

- Parent: [EN-007: ts-parser Agent Implementation](./EN-007-vtt-parser.md)
- Design: [TDD-ts-parser.md v1.2](../../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-parser.md)
- Research: [W3C WebVTT Test Suite Research](./research/webvtt-test-suite-research.md)
- Discovery: [DISC-002: Test Infrastructure](./EN-007--DISC-002-test-infrastructure-dependency.md)
- **Enables**: [TASK-102](./TASK-102-vtt-processing.md), [TASK-103](./TASK-103-srt-processing.md), [TASK-104](./TASK-104-plain-text-processing.md) (error surfacing during verification)

### Execution Order

**Recommended:** Execute TASK-106 BEFORE TASK-102, TASK-103, TASK-104 so that format processing verification can properly capture and surface parsing errors.

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| ts-parser.md Error Handling | Agent | skills/transcript/agents/ts-parser.md |
| Error capture test results | Test Evidence | (link to test output) |
| parse_metadata examples | JSON | (link to example output) |

### Verification

- [ ] All error codes implemented
- [ ] Edge case VTT files produce expected error output
- [ ] parse_status transitions correctly (complete → partial → failed)
- [ ] Reviewed by: (pending)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-27 | Created | Task created per W3C WebVTT research findings and TDD-ts-parser.md v1.2 enhancement |
