# TASK-001: Create Cross-Layer Interaction Tests (L1-L5)

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 0.1.0
-->

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this task delivers |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Implementation Notes](#implementation-notes) | Technical guidance |
| [Time Tracking](#time-tracking) | Effort estimates and actuals |
| [Related Items](#related-items) | Dependencies and hierarchy |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Status changes and key events |

---

## Summary

```yaml
id: "TASK-001"
work_type: TASK
title: "Create cross-layer interaction tests (L1-L5)"
description: |
  Write end-to-end tests that exercise the full quality enforcement pipeline across all
  five layers: L1 (hooks), L2 (session context), L3 (rules), L4 (skill adversarial mode),
  and L5 (CI verification). Tests validate that the layers work together as a coherent
  system, catching interaction failures that unit tests for individual layers would miss.
classification: ENABLER
status: DONE
resolution: null
priority: HIGH
assignee: ""
created_by: "Claude"
created_at: "2026-02-14"
updated_at: "2026-02-14"
parent_id: "EN-711"
tags:
  - "e2e-testing"
  - "cross-layer"
  - "integration"
activity: TESTING
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Create end-to-end tests that validate the complete enforcement pipeline from session start (L2) through rule loading (L3), hook invocation (L1), skill adversarial mode (L4), to CI verification (L5). Test scenarios should include:

- Full pipeline execution from session initialization to quality gate evaluation
- Layer handoff validation (output of one layer correctly consumed by next)
- Failure propagation (violation detected at any layer correctly blocks downstream)
- Combined enforcement (multiple layers reinforcing the same quality constraint)

Tests should be located in `tests/e2e/` and runnable via `uv run pytest tests/e2e/`.

### Acceptance Criteria

- [ ] Cross-layer interaction tests exist in `tests/e2e/`
- [ ] Tests exercise the full L1-L5 pipeline end-to-end
- [ ] Tests validate correct layer handoff (output of one layer consumed by next)
- [ ] Tests validate failure propagation across layers
- [ ] All tests pass via `uv run pytest tests/e2e/`

### Implementation Notes

- Reference EPIC-002 EN-306 for adversarial integration testing design
- Reference EPIC-002 EN-406 for enforcement integration test scenarios
- Use realistic file system state for hook and session tests
- Consider test fixtures that set up multi-layer enforcement scenarios

### Related Items

- Parent: [EN-711: E2E Integration Testing](EN-711-e2e-integration-testing.md)
- Blocks: TASK-007 (adversarial review of test completeness)
- Related: EPIC-002 EN-306 (adversarial integration testing design)

---

## Time Tracking

| Metric | Value |
|--------|-------|
| Original Estimate | — |
| Remaining Work | 0 hours |
| Time Spent | — |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Cross-layer E2E tests | Test suite | `tests/e2e/` |

### Verification

- [ ] Acceptance criteria verified
- [ ] All cross-layer tests pass
- [ ] Test coverage for layer interactions is comprehensive
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------------|-------------|--------------------------------|
| 2026-02-14 | Created | Initial creation from EN-711 task decomposition |
