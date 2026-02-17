# TASK-005: Add E2E test for auto-escalation override detection

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** BACKLOG
> **Priority:** HIGH
> **Activity:** DEVELOPMENT
> **Agents:** ps-architect
> **Created:** 2026-02-15
> **Parent:** EN-817

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

Create an E2E test that validates the auto-escalation cross-check in adv-selector.md by verifying that AE-001 through AE-006 rules are referenced and that the selection algorithm accounts for escalation overrides.

### Acceptance Criteria
- [ ] E2E test added to tests/e2e/
- [ ] Test validates AE rule references in adv-selector.md
- [ ] Test passes with `uv run pytest`

### Related Items
- Parent: [EN-817: Runtime Enforcement](EN-817-runtime-enforcement.md)

---

## Time Tracking

| Metric | Value |
|--------|-------|
| Original Estimate | — |
| Remaining Work | — |
| Time Spent | — |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| E2E test file | Test | --- |

### Verification
- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-15 | Created | Task created from EN-817 breakdown. |
