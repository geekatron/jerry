# TASK-130: Validate All Domain Schemas Against JSON Schema

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-014 (Domain Context Files Implementation)
-->

---

## Frontmatter

```yaml
id: "TASK-130"
work_type: TASK
title: "Validate All Domain Schemas Against JSON Schema"
description: |
  Run JSON Schema validation against all domain context files
  (general.yaml, transcript.yaml, meeting.yaml) and document results.

classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-26T19:30:00Z"
updated_at: "2026-01-26T19:30:00Z"

parent_id: "EN-014"

tags:
  - "testing"
  - "domain-context"
  - "validation"
  - "REQ-CI-F-009"

effort: 1
acceptance_criteria: |
  - All domain schemas validate against JSON Schema
  - Validation results documented
  - Any errors fixed in source files
  - Inheritance mechanism verified

due_date: null

activity: TESTING
original_estimate: 2
remaining_work: 2
time_spent: 0
```

---

## State Machine

**Current State:** `BACKLOG`

---

## Content

### Description

Validate all domain context YAML files against the JSON Schema (TASK-129). This ensures structural consistency and catches configuration errors before runtime.

### Validation Matrix

| Domain File | Schema | Expected | Status |
|-------------|--------|----------|--------|
| general.yaml | domain-schema.json | PASS | [ ] |
| transcript.yaml | domain-schema.json | PASS | [ ] |
| meeting.yaml | domain-schema.json | PASS | [ ] |

### Validation Checks

| Check ID | Domain | Check | Expected | Status |
|----------|--------|-------|----------|--------|
| VAL-001 | general | schema_version format | "1.0.0" | [ ] |
| VAL-002 | general | domain field present | "general" | [ ] |
| VAL-003 | general | entity_definitions present | ≥1 entity | [ ] |
| VAL-004 | transcript | schema_version format | "1.0.0" | [ ] |
| VAL-005 | transcript | 5 core entities | action_item, decision, question, speaker, topic | [ ] |
| VAL-006 | transcript | extraction_rules present | ≥5 rules | [ ] |
| VAL-007 | transcript | confidence thresholds valid | 0-1 range | [ ] |
| VAL-008 | meeting | extends field | "transcript" | [ ] |
| VAL-009 | meeting | 3 meeting entities | attendee, agenda_item, follow_up | [ ] |
| VAL-010 | meeting | enum values valid | role, status, priority | [ ] |

### Inheritance Verification

```
TEST: Domain Inheritance
========================

1. Load meeting.yaml
2. Verify extends="transcript"
3. Load transcript.yaml
4. Merge entities:
   - meeting entities: attendee, agenda_item, follow_up
   - inherited entities: action_item, decision, question, speaker, topic
5. Verify total: 8 entities available

EXPECTED: Meeting domain has access to all 8 entities
```

### Edge Case Tests

| Test ID | Scenario | Expected |
|---------|----------|----------|
| EDGE-001 | Missing schema_version | FAIL: required field |
| EDGE-002 | Invalid semver format | FAIL: pattern mismatch |
| EDGE-003 | Confidence > 1.0 | FAIL: maximum constraint |
| EDGE-004 | Confidence < 0 | FAIL: minimum constraint |
| EDGE-005 | Unknown attribute type | FAIL: enum constraint |
| EDGE-006 | Unknown tier value | FAIL: enum constraint |
| EDGE-007 | Empty domain | FAIL: minLength constraint |
| EDGE-008 | Missing entity_definitions | FAIL: required field |

### Acceptance Criteria

- [ ] All 3 domain files pass JSON Schema validation
- [ ] No validation errors in any file
- [ ] Inheritance verified (meeting extends transcript)
- [ ] Confidence thresholds in valid range
- [ ] All enum values match schema constraints
- [ ] Edge cases documented
- [ ] Validation results recorded

### Related Items

- Parent: [EN-014: Domain Context Files Implementation](./EN-014-domain-context-files.md)
- Blocked By: [TASK-128: meeting.yaml](./TASK-128-meeting-domain-schema.md), [TASK-129: JSON Schema](./TASK-129-domain-json-schema.md)
- Validated By: [TASK-137: Context injection tests](../EN-015-transcript-validation/TASK-137-context-injection-tests.md)
- References: REQ-CI-F-009 (Schema Validation)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Validation results | Documentation | (in this file) |
| Fixed domain files (if needed) | Updates | contexts/*.yaml |

### Validation Results

```
[To be filled during task execution]

File | Result | Errors (if any)
-----|--------|----------------
general.yaml |  |
transcript.yaml |  |
meeting.yaml |  |
```

### Edge Case Results

```
[To be filled during task execution]

Test ID | Input | Expected | Actual | Status
--------|-------|----------|--------|-------
EDGE-001 |       |          |        |
EDGE-002 |       |          |        |
EDGE-003 |       |          |        |
EDGE-004 |       |          |        |
EDGE-005 |       |          |        |
EDGE-006 |       |          |        |
EDGE-007 |       |          |        |
EDGE-008 |       |          |        |
```

### Verification

- [ ] All domain files validate
- [ ] Inheritance works correctly
- [ ] Edge cases documented
- [ ] Reviewed by: (pending)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-26 | Created | Initial task creation per EN-014 |
