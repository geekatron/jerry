# TASK-002: Write S-010-self-refine.md Following TEMPLATE-FORMAT

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
> **Created:** 2026-02-14
> **Parent:** EN-804

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

Create the S-010 Self-Refine template at `.context/templates/adversarial/S-010-self-refine.md` with all 8 required sections from TEMPLATE-FORMAT.md. Include the iterative self-review checklist aligned with quality-enforcement.md dimensions, the generate-critique-refine loop protocol with concrete steps, convergence criteria for iteration termination, and integration with H-15 mandatory self-review gate.

### Acceptance Criteria

- [ ] File created at `.context/templates/adversarial/S-010-self-refine.md`
- [ ] Identity section: S-010, Self-Refine, score 4.00, Iterative Self-Correction family
- [ ] Purpose section: when and why to use, H-15 mandatory trigger
- [ ] Prerequisites section: required inputs (deliverable draft, quality dimensions, context)
- [ ] Execution Protocol section: generate-critique-refine loop with numbered steps
- [ ] Output Format section: self-review report structure with improvement tracking
- [ ] Scoring Rubric section: self-assessment criteria aligned with 6 quality dimensions
- [ ] Examples section: before/after showing refinement improvement
- [ ] Integration section: H-15 gate placement, handoff to S-014 for formal scoring
- [ ] Convergence criteria defined (diminishing returns threshold, maximum iteration cap)
- [ ] File follows markdown navigation standards (H-23, H-24)
- [ ] Quality gate: Deliverable reviewed via creator-critic-revision cycle (min 3 iterations)
- [ ] Quality gate: Score >= 0.92 via S-014 LLM-as-Judge rubric
- [ ] Quality gate: S-003 Steelman applied before S-002 Devil's Advocate critique

### Related Items

- Parent: [EN-804: S-010 Self-Refine Template](EN-804-s010-self-refine.md)
- Depends on: TASK-001 (methodology extraction)
- Blocks: TASK-003 (quality cycle)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| `.context/templates/adversarial/S-010-self-refine.md` | Strategy template | --- |

### Verification

- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation. Core deliverable -- S-010 template operationalizes the H-15 mandatory self-review requirement. |
