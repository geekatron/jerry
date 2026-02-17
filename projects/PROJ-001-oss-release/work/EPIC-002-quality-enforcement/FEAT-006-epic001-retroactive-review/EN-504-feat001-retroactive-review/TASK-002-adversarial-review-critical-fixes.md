# TASK-002: Apply adversarial review to critical fixes

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

Apply adversarial quality review to the most critical FEAT-001 fixes using the strategies defined in FEAT-004. Focus on infrastructure changes (CI configuration, test setup, dependency management) that have the widest blast radius.

Review must include:
- Minimum 3 creator-critic-revision iterations
- Application of relevant adversarial strategies (S-014 LLM-as-Judge, S-003 Steelman, S-002 Devil's Advocate)
- Quality scoring against the 6 dimensions (completeness, internal consistency, methodological rigor, evidence quality, actionability, traceability)
- Target quality score >= 0.92 weighted composite

### Acceptance Criteria

- [ ] Critical fixes identified from TASK-001 audit reviewed
- [ ] Adversarial review completed with >= 3 iterations per fix
- [ ] Quality score >= 0.92 achieved for each reviewed fix
- [ ] All adversarial findings documented
- [ ] Review artifacts persisted to filesystem

### Implementation Notes

Prioritize CI pipeline configuration, test infrastructure changes, and dependency management fixes. Less critical cosmetic or documentation-only fixes may be reviewed at a lighter level.

### Related Items

- Parent: [EN-504: FEAT-001 Retroactive Quality Review](EN-504-feat001-retroactive-review.md)
- Depends on: TASK-001 (audit must identify critical fixes)
- Parallel with: TASK-003

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Critical fixes adversarial review document | Document | pending |
| Quality score breakdowns | Document | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] >= 3 creator-critic-revision iterations per fix
- [ ] Quality scores >= 0.92
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Adversarial review of critical FEAT-001 fixes. |
