# TASK-105: Create Test Cases and Validation for ts-parser

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-007 (ts-parser Agent Implementation)
-->

---

## Frontmatter

```yaml
id: "TASK-105"
work_type: TASK
title: "Create Test Cases and Validation for ts-parser"
description: |
  Create and execute validation test cases for ts-parser using
  golden dataset transcripts from EN-015. Verify all FR requirements.

classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-26T18:30:00Z"
updated_at: "2026-01-26T18:30:00Z"

parent_id: "EN-007"

tags:
  - "testing"
  - "ts-parser"
  - "validation"

effort: 2
acceptance_criteria: |
  - All golden dataset transcripts parse successfully
  - All edge case transcripts handled per PAT-002
  - Format detection works for all three formats
  - Timestamp normalization verified
  - Encoding detection verified
  - Test results documented

due_date: null

activity: TESTING
original_estimate: 4
remaining_work: 4
time_spent: 0
```

---

## State Machine

**Current State:** `BACKLOG`

---

## Content

### Description

Execute comprehensive validation of ts-parser against the golden dataset transcripts created in EN-015. This task validates that all parsing requirements are met.

### Validation Matrix

| Test Input | Format | Expected Outcome | Status |
|------------|--------|------------------|--------|
| meeting-001.vtt | VTT | 45 segments, 4 speakers | [ ] |
| meeting-001.srt | SRT | 45 segments, 4 speakers | [ ] |
| meeting-001.txt | Plain | 45 segments, 4 speakers | [ ] |
| meeting-002.vtt | VTT | All segments parsed | [ ] |
| meeting-003.vtt | VTT | Edge cases handled | [ ] |
| empty.vtt | VTT | Empty array, no errors | [ ] |
| malformed.vtt | VTT | Partial recovery, warnings | [ ] |
| unicode.vtt | VTT | All characters preserved | [ ] |

### Acceptance Criteria

- [ ] All golden dataset VTT files parse without errors
- [ ] All golden dataset SRT files parse without errors
- [ ] Plain text format parses correctly
- [ ] Format auto-detection works for all formats
- [ ] Empty file returns empty segments array
- [ ] Malformed file recovers gracefully (PAT-002)
- [ ] Unicode characters preserved correctly
- [ ] Timestamps normalized to milliseconds
- [ ] All speakers detected correctly
- [ ] Segment counts match expected values

### Test Execution Steps

1. Parse each golden dataset transcript
2. Compare segment count to expected
3. Compare speaker list to expected
4. Verify timestamp format (milliseconds)
5. Verify canonical JSON schema compliance
6. Parse edge case transcripts
7. Verify error handling per PAT-002
8. Document all results

### Evidence Required

For each test:
- Input file path
- Expected outcome
- Actual outcome
- Pass/Fail status
- Any warnings or errors logged

### Related Items

- Parent: [EN-007: ts-parser Agent Implementation](./EN-007-vtt-parser.md)
- Blocked By: [TASK-102](./TASK-102-vtt-processing.md), [TASK-103](./TASK-103-srt-processing.md), [TASK-104](./TASK-104-plain-text-processing.md)
- Depends On: [TASK-131: Golden dataset](../EN-015-transcript-validation/TASK-131-golden-dataset-transcripts.md)
- Depends On: [TASK-133: Edge cases](../EN-015-transcript-validation/TASK-133-edge-case-transcripts.md)
- References: [TASK-134: Parser tests](../EN-015-transcript-validation/TASK-134-parser-tests.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Test execution log | Documentation | (in this file) |
| Test results summary | Evidence | (below) |

### Test Results

```
[To be filled during task execution]

Test ID | Input | Expected | Actual | Status
--------|-------|----------|--------|-------
(record results here)
```

### Verification

- [ ] All golden dataset tests pass
- [ ] All edge case tests pass
- [ ] No regressions from previous tests
- [ ] Reviewed by: (pending)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-26 | Created | Initial task creation per EN-007 |

