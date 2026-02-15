# TASK-004: Add E2E test for malformed template detection

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
> **Parent:** EN-819

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

Create an E2E test that validates the malformed template detection by checking that adv-executor.md contains the malformed template handling specification and that the handling behavior matches the expected pattern (CRITICAL finding + halt).

### Acceptance Criteria
- [ ] E2E test added to tests/e2e/
- [ ] Validates malformed template handling spec in adv-executor.md
- [ ] Test passes with `uv run pytest`

### Related Items
- Parent: [EN-819: SSOT Consistency & Template Resilience](EN-819-ssot-consistency.md)
- Depends on: TASK-003

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
| 2026-02-15 | Created | Task created from EN-819 breakdown. |
