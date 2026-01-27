# TASK-134: Create Parser Test Specification

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-015 (Transcript Validation & Test Cases)
-->

---

## Frontmatter

```yaml
id: "TASK-134"
work_type: TASK
title: "Create Parser Test Specification (parser-tests.yaml)"
description: |
  Create YAML-based test specification for ts-parser agent validation.
  Covers VTT, SRT, plain text parsing, format detection, and error handling.

classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-26T18:00:00Z"
updated_at: "2026-01-26T18:00:00Z"

parent_id: "EN-015"

tags:
  - "validation"
  - "testing"
  - "ts-parser"

effort: 1
acceptance_criteria: |
  - Test suites for VTT, SRT, and plain text parsing
  - Error handling tests for edge cases
  - Format detection tests
  - Timestamp normalization tests
  - Speaker extraction tests

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

Create a comprehensive YAML test specification for validating the ts-parser agent. Tests are organized into suites covering each parsing capability defined in TDD-ts-parser.md.

### Acceptance Criteria

- [ ] VTT parsing test suite with 5+ test cases
- [ ] SRT parsing test suite with 3+ test cases
- [ ] Plain text parsing test suite with 2+ test cases
- [ ] Error handling test suite with 4+ test cases
- [ ] Format detection test suite with 3+ test cases
- [ ] Timestamp normalization test suite with 2+ test cases
- [ ] All tests map to FR requirements from TDD-ts-parser.md
- [ ] YAML validates against test specification schema

### Test Suites

| Suite | Test Count | Source Requirements |
|-------|------------|---------------------|
| vtt_parsing | 5 | FR-001, FR-004 |
| srt_parsing | 3 | FR-002, FR-004 |
| plain_text_parsing | 2 | FR-003 |
| error_handling | 4 | PAT-002 (Defensive Parsing) |
| format_detection | 3 | FR-004 |
| timestamp_normalization | 2 | TDD-ts-parser Section 4.2 |

### Test Case Template

```yaml
- id: "{suite}-{nnn}"
  name: "Test case name"
  description: "What this test validates"
  input: "path/to/input/file"
  assertions:
    - type: assertion_type
      expected: expected_value
    - type: another_assertion
      minimum: threshold_value
  requirements: ["FR-001", "PAT-002"]
```

### Assertion Types

| Type | Description | Parameters |
|------|-------------|------------|
| segment_count | Number of parsed segments | expected (int) |
| speaker_detected | Speakers found | expected (list) |
| format_detected | Detected format | expected (string) |
| no_errors | No parsing errors | (none) |
| timestamp_format | Timestamp format used | expected (string) |
| partial_recovery | Recovers from errors | expected (bool) |
| warnings | Warning messages | expected_count (string) |
| speaker_fallback | Fallback method used | expected (string) |

### Related Items

- Parent: [EN-015: Transcript Validation](./EN-015-transcript-validation.md)
- Blocked By: [TASK-131: Golden dataset transcripts](./TASK-131-golden-dataset-transcripts.md)
- Tests: [EN-007: ts-parser Agent](../EN-007-vtt-parser/EN-007-vtt-parser.md)
- References: [TDD-ts-parser.md](../../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-parser.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| parser-tests.yaml | Test Spec | test_data/validation/parser-tests.yaml |

### Verification

- [ ] All FR requirements have corresponding tests
- [ ] Edge case transcripts covered in error_handling suite
- [ ] YAML syntax is valid
- [ ] All input file paths exist
- [ ] Reviewed by: (pending)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-26 | Created | Initial task creation per EN-015 |

