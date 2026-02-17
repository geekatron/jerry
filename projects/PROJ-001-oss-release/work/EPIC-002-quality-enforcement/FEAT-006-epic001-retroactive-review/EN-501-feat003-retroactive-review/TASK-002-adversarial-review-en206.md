# TASK-002: Apply adversarial review to EN-206 (context distribution)

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
> **Parent:** EN-501

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

Apply adversarial quality review to EN-206 (context distribution) deliverables using the strategies defined in FEAT-004. The .context/ restructure affects all rule loading and is the highest-risk deliverable in FEAT-003.

Review must include:
- Minimum 3 creator-critic-revision iterations
- Application of relevant adversarial strategies (S-014 LLM-as-Judge, S-003 Steelman, S-002 Devil's Advocate)
- Quality scoring against the 6 dimensions (completeness, internal consistency, methodological rigor, evidence quality, actionability, traceability)
- Target quality score >= 0.92 weighted composite

### Acceptance Criteria

- [ ] Adversarial review completed with >= 3 iterations
- [ ] Quality score >= 0.92 achieved
- [ ] All adversarial findings documented
- [ ] Review artifacts persisted to filesystem

### Implementation Notes

The context distribution restructure moved content from CLAUDE.md into `.context/rules/` files that are auto-loaded by Claude. Review should focus on: completeness of the distribution (no content lost), consistency between files, and effectiveness of the progressive loading approach.

### Related Items

- Parent: [EN-501: FEAT-003 Retroactive Quality Review](EN-501-feat003-retroactive-review.md)
- Depends on: TASK-001 (audit must identify EN-206 deliverables)
- Parallel with: TASK-003

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| EN-206 adversarial review document | Document | pending |
| EN-206 quality score breakdown | Document | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] >= 3 creator-critic-revision iterations completed
- [ ] Quality score >= 0.92
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Adversarial review of EN-206 context distribution. |
