# TASK-137: Create Integration Test Specification

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-015 (Transcript Validation & Test Cases)
-->

---

## Frontmatter

```yaml
id: "TASK-137"
work_type: TASK
title: "Create Integration Test Specification (integration-tests.yaml)"
description: |
  Create YAML-based test specification for end-to-end pipeline validation.
  Tests full ts-parser → ts-extractor → ts-formatter workflow.

classification: ENABLER
status: DONE
resolution: COMPLETED
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-26T18:00:00Z"
updated_at: "2026-01-26T18:00:00Z"

parent_id: "EN-015"

tags:
  - "validation"
  - "testing"
  - "integration"
  - "end-to-end"

effort: 1
acceptance_criteria: |
  - End-to-end pipeline tests for all golden dataset transcripts
  - Error propagation tests (malformed input handling)
  - Context injection integration tests
  - Performance threshold tests

due_date: null

activity: TESTING
original_estimate: 2
remaining_work: 2
time_spent: 0
```

---

## State Machine

**Current State:** `DONE`

---

## Content

### Description

Create integration tests that validate the complete transcript skill pipeline from input file to 8-file packet output. Tests verify that all three agents work correctly together.

### Acceptance Criteria

- [x] End-to-end test for each golden dataset transcript (E2E-001, E2E-002, E2E-003)
- [x] Error propagation tests (malformed input → graceful degradation) (ERR-E2E-001, ERR-E2E-002)
- [x] Context injection tests (domain.yaml correctly applied) (CTX-001, CTX-002)
- [x] Performance tests (reasonable completion time) (PERF-001, PERF-002)
- [x] All tests exercise full pipeline (VTT → parser → extractor → formatter → packet)
- [x] Output validation against ground truth (F1 thresholds defined)

### Integration Test Flow

```
                    INTEGRATION TEST FLOW
                    =====================

    INPUT                 PIPELINE                      OUTPUT
    ─────                 ────────                      ──────

    ┌─────────────┐
    │ meeting.vtt │
    └──────┬──────┘
           │
           ▼
    ┌──────────────┐      ┌──────────────┐
    │  ts-parser   │─────▶│ parsed.json  │  (intermediate)
    └──────────────┘      └──────┬───────┘
                                 │
                                 ▼
                          ┌──────────────┐      ┌──────────────┐
                          │ ts-extractor │─────▶│extracted.json│  (intermediate)
                          └──────────────┘      └──────┬───────┘
                                                       │
                                                       ▼
                                                ┌──────────────┐
                                                │ ts-formatter │
                                                └──────┬───────┘
                                                       │
                                                       ▼
                                                ┌──────────────┐
                                                │  8-file      │
                                                │  packet/     │
                                                └──────────────┘
```

### Integration Assertion Types

| Type | Description | Parameters |
|------|-------------|------------|
| pipeline_success | Full pipeline completes | (none) |
| intermediate_valid | Intermediate output valid | stage, schema |
| final_packet_valid | Final 8-file packet valid | (none) |
| extraction_accuracy | Extraction matches ground truth | minimum_f1 |
| error_contained | Errors don't crash pipeline | input_type |
| context_applied | Domain context was applied | context_file |
| performance | Completes within time limit | max_seconds |

### Test Suite Structure

```yaml
test_suites:
  end_to_end:
    description: "Full pipeline integration tests"
    tests:
      - id: e2e-001
        name: "meeting-001 full pipeline"
        input: "transcripts/golden/meeting-001.vtt"
        ground_truth: "transcripts/golden/meeting-001.expected.json"
        context: "contexts/meeting.yaml"
        assertions:
          - type: pipeline_success
          - type: final_packet_valid
          - type: extraction_accuracy
            minimum_f1: 0.80
        requirements: ["E2E-001"]

      - id: e2e-002
        name: "meeting-002 full pipeline (complex)"
        input: "transcripts/golden/meeting-002.vtt"
        ground_truth: "transcripts/golden/meeting-002.expected.json"
        assertions:
          - type: pipeline_success
          - type: extraction_accuracy
            minimum_f1: 0.75
        requirements: ["E2E-001"]

      - id: e2e-003
        name: "meeting-003 full pipeline (edge cases)"
        input: "transcripts/golden/meeting-003.vtt"
        ground_truth: "transcripts/golden/meeting-003.expected.json"
        assertions:
          - type: pipeline_success
          - type: final_packet_valid
        requirements: ["E2E-001"]

  error_propagation:
    description: "Error handling integration tests"
    tests:
      - id: err-e2e-001
        name: "Malformed input graceful degradation"
        input: "transcripts/edge_cases/malformed.vtt"
        assertions:
          - type: error_contained
            input_type: "malformed"
          - type: pipeline_success
            # Should still produce output with warnings
        requirements: ["PAT-002"]

      - id: err-e2e-002
        name: "Empty input produces empty output"
        input: "transcripts/edge_cases/empty.vtt"
        assertions:
          - type: pipeline_success
          - type: final_packet_valid
            # Packet exists but with minimal content
        requirements: ["PAT-002"]

  context_injection:
    description: "Context injection integration tests"
    tests:
      - id: ctx-001
        name: "Meeting context applied correctly"
        input: "transcripts/golden/meeting-001.vtt"
        context: "contexts/meeting.yaml"
        assertions:
          - type: context_applied
            context_file: "meeting.yaml"
          - type: pipeline_success
        requirements: ["EN-013", "EN-014"]

      - id: ctx-002
        name: "General context fallback works"
        input: "transcripts/golden/meeting-001.vtt"
        context: "contexts/general.yaml"
        assertions:
          - type: context_applied
            context_file: "general.yaml"
          - type: pipeline_success
        requirements: ["EN-013", "EN-014"]

  performance:
    description: "Performance threshold tests"
    tests:
      - id: perf-001
        name: "15-minute transcript completes in 60 seconds"
        input: "transcripts/golden/meeting-001.vtt"
        assertions:
          - type: performance
            max_seconds: 60
        requirements: ["REQ-CI-P-001"]

      - id: perf-002
        name: "Large transcript completes in 5 minutes"
        input: "transcripts/edge_cases/large.vtt"
        assertions:
          - type: performance
            max_seconds: 300
        requirements: ["REQ-CI-P-001"]
```

### Related Items

- Parent: [EN-015: Transcript Validation](./EN-015-transcript-validation.md)
- Blocked By: [TASK-134: Parser tests](./TASK-134-parser-tests.md)
- Blocked By: [TASK-135: Extractor tests](./TASK-135-extractor-tests.md)
- Blocked By: [TASK-136: Formatter tests](./TASK-136-formatter-tests.md)
- Tests: All three agents (EN-007, EN-008, EN-009)
- Tests: Context injection (EN-013, EN-014)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| integration-tests.yaml | Test Spec | test_data/validation/integration-tests.yaml |

### Verification

- [x] All golden dataset transcripts have E2E tests (E2E-001, E2E-002, E2E-003)
- [x] Error propagation tested (ERR-E2E-001 malformed, ERR-E2E-002 empty)
- [x] Context injection tested (CTX-001 transcript domain, CTX-002 general fallback)
- [x] Performance thresholds defined (PERF-001 60s, PERF-002 5min)
- [x] YAML syntax is valid (extends existing integration-tests.yaml)
- [x] Reviewed by: Self-review during implementation

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-26 | Created | Initial task creation per EN-015 |
| 2026-01-28 | **DONE** | Extended integration-tests.yaml with 4 new test suites: (1) **end-to-end**: E2E-001..003 golden dataset full pipeline tests, (2) **error-propagation**: ERR-E2E-001..002 malformed/empty input handling, (3) **context-injection**: CTX-001..002 transcript domain and general fallback, (4) **performance**: PERF-001..002 timing thresholds. Added 20+ new assertion types. Total test count now 10 E2E + error + context + perf tests. File extended from ~690 lines to ~1100 lines. |

