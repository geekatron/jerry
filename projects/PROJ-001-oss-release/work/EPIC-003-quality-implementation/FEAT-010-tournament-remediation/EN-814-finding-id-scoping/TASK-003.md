# TASK-003: Add E2E test for finding prefix uniqueness across all templates

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
> **Parent:** EN-814

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

Add an E2E test that validates all 10 strategy templates define unique STRATEGY_PREFIX values and that the finding ID format matches the specification in TEMPLATE-FORMAT.md.

### Acceptance Criteria

- [ ] E2E test added to tests/e2e/
- [ ] Test validates unique prefixes across all 10 templates
- [ ] Test validates finding ID format compliance
- [ ] Test passes with `uv run pytest`

### Related Items

- Parent: [EN-814: Finding ID Scoping & Uniqueness](EN-814-finding-id-scoping.md)
- Dependency: TASK-002 (all templates must be updated)

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
| E2E test for finding prefix uniqueness | Test | --- |
| Test execution report | Report | --- |

### Verification

- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-15 | Created | Task created from EN-814 technical approach. |
