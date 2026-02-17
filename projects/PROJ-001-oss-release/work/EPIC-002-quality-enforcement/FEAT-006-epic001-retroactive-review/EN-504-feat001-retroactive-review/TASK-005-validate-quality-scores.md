# TASK-005: Validate quality scores >= 0.92

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** BACKLOG
> **Priority:** HIGH
> **Activity:** REVIEW
> **Created:** 2026-02-16
> **Parent:** EN-504

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Content](#content) | Description, acceptance criteria, implementation notes |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Status changes and key events |

---

## Content

### Description

After remediation (TASK-004), validate that all reviewed FEAT-001 deliverables achieve >= 0.92 weighted composite quality score. Apply S-014 (LLM-as-Judge) scoring with dimension-level rubrics per ADR-EPIC002-001.

For each deliverable, calculate:
- Completeness (0.20 weight)
- Internal Consistency (0.20 weight)
- Methodological Rigor (0.20 weight)
- Evidence Quality (0.15 weight)
- Actionability (0.15 weight)
- Traceability (0.10 weight)

### Acceptance Criteria

- [ ] All reviewed deliverables scored using S-014 LLM-as-Judge
- [ ] All scores >= 0.92 weighted composite
- [ ] Dimension-level breakdown documented for each deliverable
- [ ] Quality score report persisted as deliverable

### Implementation Notes

If any deliverable scores below 0.92 after remediation, additional revision cycles are required. The quality score must be calculated with active counteraction of leniency bias per quality-enforcement.md L2-REINJECT guidance.

### Related Items

- Parent: [EN-504: FEAT-001 Retroactive Quality Review](EN-504-feat001-retroactive-review.md)
- Depends on: TASK-004

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Quality score report | Document | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] All scores >= 0.92
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Validation phase for EN-504 FEAT-001 retroactive review. |
