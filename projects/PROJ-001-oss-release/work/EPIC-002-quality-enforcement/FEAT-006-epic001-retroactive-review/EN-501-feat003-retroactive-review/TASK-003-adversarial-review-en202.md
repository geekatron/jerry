# TASK-003: Apply adversarial review to EN-202 (CLAUDE.md rewrite)

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

Apply adversarial quality review to EN-202 (CLAUDE.md rewrite) deliverables using the strategies defined in FEAT-004. The CLAUDE.md file is loaded on every Claude session and is the highest-impact deliverable in FEAT-003.

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

The CLAUDE.md rewrite optimized the root context file for token efficiency and clarity. Review should focus on: completeness (all critical information present), clarity (unambiguous instructions), token efficiency (no redundancy), and correctness (all references and navigation links valid).

### Related Items

- Parent: [EN-501: FEAT-003 Retroactive Quality Review](EN-501-feat003-retroactive-review.md)
- Depends on: TASK-001 (audit must identify EN-202 deliverables)
- Parallel with: TASK-002

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| EN-202 adversarial review document | Document | pending |
| EN-202 quality score breakdown | Document | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] >= 3 creator-critic-revision iterations completed
- [ ] Quality score >= 0.92
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Adversarial review of EN-202 CLAUDE.md rewrite. |
