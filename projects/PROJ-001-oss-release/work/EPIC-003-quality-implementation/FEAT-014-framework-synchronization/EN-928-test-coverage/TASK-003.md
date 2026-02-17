# TASK-003: Run full test suite and verify H-21 coverage

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** BACKLOG
> **Priority:** MEDIUM
> **Activity:** TESTING
> **Agents:** ps-critic
> **Created:** 2026-02-17
> **Parent:** EN-928

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this task delivers |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Time Tracking](#time-tracking) | Effort estimates and actuals |
| [Evidence](#evidence) | Deliverables and verification |
| [Related Items](#related-items) | Parent and dependencies |
| [History](#history) | Change log |

---

## Summary

Run the full test suite after TASK-001 and TASK-002 are complete. Verify that all new tests pass, no regressions are introduced, and the overall test coverage meets the H-21 requirement of >= 90% line coverage. Document coverage results as evidence.

### Acceptance Criteria

- [ ] Full test suite passes with `uv run pytest`
- [ ] No regressions introduced by new tests
- [ ] Line coverage >= 90% (H-21)
- [ ] Coverage report generated and reviewed

### Related Items

- Parent: [EN-928: Test Coverage Expansion](EN-928-test-coverage.md)
- Depends on: TASK-001 (template tests), TASK-002 (skill tests)

---

## Time Tracking

| Metric | Value |
|--------|-------|
| Original Estimate | --- |
| Remaining Work | --- |
| Time Spent | --- |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Test suite execution results | Test Report | --- |
| Coverage report | Test Report | --- |

### Verification

- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-17 | Created | Task created from EN-928 technical approach. |
