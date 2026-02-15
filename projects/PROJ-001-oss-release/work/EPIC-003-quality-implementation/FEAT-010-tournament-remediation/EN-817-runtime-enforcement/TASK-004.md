# TASK-004: Add E2E test for H-16 enforcement

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** pending
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
| [Evidence](#evidence) | Deliverables and verification |
| [Related Items](#related-items) | Parent and dependencies |
| [History](#history) | Change log |

---

## Summary

Create an E2E test that validates H-16 enforcement by checking that the adv-executor agent specification contains the H-16 ordering check and that S-002 execution requires S-003 in prior_strategies_executed.

### Acceptance Criteria
- [ ] E2E test added to tests/e2e/
- [ ] Test validates H-16 check presence in adv-executor.md
- [ ] Test passes with `uv run pytest`

### Related Items
- Parent: [EN-817: Runtime Enforcement](EN-817-runtime-enforcement.md)

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
