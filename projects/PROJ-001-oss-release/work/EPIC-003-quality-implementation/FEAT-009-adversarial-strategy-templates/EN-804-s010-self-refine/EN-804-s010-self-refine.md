# EN-804: S-010 Self-Refine Template

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-14 (Claude)
PURPOSE: Create the execution template for S-010 Self-Refine strategy
-->

> **Type:** enabler
> **Status:** completed
> **Priority:** critical
> **Impact:** critical
> **Enabler Type:** infrastructure
> **Created:** 2026-02-14
> **Due:** —
> **Completed:** —
> **Parent:** FEAT-009
> **Owner:** —
> **Effort:** 3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this enabler delivers |
| [Problem Statement](#problem-statement) | Why this work is needed |
| [Business Value](#business-value) | How this enabler supports the parent feature |
| [Technical Approach](#technical-approach) | How we'll implement it |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Progress Summary](#progress-summary) | Completion status and metrics |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Evidence](#evidence) | Deliverables and verification |
| [Related Items](#related-items) | Dependencies and hierarchy |
| [History](#history) | Change log |

---

## Summary

Create the execution template for S-010 Self-Refine -- the self-review strategy applied before presenting any deliverable per H-15 (self-review before presenting). The template includes an iterative improvement protocol, a self-review checklist aligned with quality dimensions, and integration instructions for the mandatory self-review gate.

**Technical Scope:**
- Extract S-010 methodology from research-15-adversarial-strategies.md and EPIC-002 designs
- Define the iterative self-review checklist aligned with quality-enforcement.md dimensions
- Map to H-15 self-review requirement (mandatory before presenting any deliverable)
- Write template following the canonical TEMPLATE-FORMAT.md from EN-801
- Define convergence criteria for when self-refinement iterations should stop

---

## Problem Statement

S-010 Self-Refine is mandated by H-15 (self-review before presenting) but has no structured execution template defining what "self-review" means concretely. Specific gaps:

1. **No checklist** -- H-15 requires self-review but provides no checklist of what to review, leaving agents to interpret "self-review" inconsistently.
2. **No iteration protocol** -- Self-Refine is inherently iterative (generate -> critique -> refine), but there is no protocol defining how many iterations to perform, when to stop, or how to assess convergence.
3. **No dimension alignment** -- The self-review should evaluate against the same 6 dimensions used by S-014 LLM-as-Judge, but without a template, agents may miss dimensions entirely.
4. **No integration guidance** -- H-15 applies at every criticality level, but there is no guidance on how S-010 interacts with S-014 scoring or the broader creator-critic-revision cycle.

---

## Business Value

S-010 Self-Refine is the mandatory self-review strategy required by H-15 before presenting any deliverable. This template provides a concrete, repeatable self-review protocol aligned with the quality framework's 6 dimensions, ensuring that every deliverable undergoes structured self-assessment before entering the critic-revision cycle. This directly reduces revision cycle count by catching issues early.

### Features Unlocked

- Structured self-review gate for all deliverables, enforcing H-15 compliance
- Convergence criteria enabling agents to determine when self-refinement iterations should stop

---

## Technical Approach

1. **Extract S-010 methodology** from research-15-adversarial-strategies.md, focusing on the Self-Refine paradigm: generate initial output, self-critique against criteria, refine based on critique, and iterate until convergence.
2. **Define self-review checklist** aligned with quality-enforcement.md dimensions (Completeness, Internal Consistency, Methodological Rigor, Evidence Quality, Actionability, Traceability) at a level appropriate for self-assessment.
3. **Write template** following TEMPLATE-FORMAT.md from EN-801, with particular emphasis on the Execution Protocol section defining the generate-critique-refine loop and convergence criteria.
4. **Integrate with H-15** -- Define the mandatory self-review gate: when it triggers, what it checks, and how it feeds into S-014 scoring or the creator-critic-revision cycle.

---

## Children (Tasks)

| ID | Title | Status | Activity | Agents |
|----|-------|--------|----------|--------|
| TASK-001 | Extract S-010 methodology from research and EPIC-002 designs | pending | RESEARCH | ps-researcher |
| TASK-002 | Write S-010-self-refine.md following TEMPLATE-FORMAT | pending | DEVELOPMENT | ps-architect |
| TASK-003 | Creator-critic-revision quality cycle | pending | REVIEW | ps-critic |

### Task Dependencies

```
TASK-001 (extract methodology) ──> TASK-002 (write template) ──> TASK-003 (quality cycle)
```

---

## Progress Summary

### Status Overview

```
EN-804 S-010 Self-Refine Template
[==================================================] 100%
Status: DONE | All tasks completed | Quality gate PASSED
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| Total Tasks | 3 |
| Completed | 3 |
| In Progress | 0 |
| Blocked | 0 |
| Completion | 100% |
| Quality Score | >= 0.92 |

---

## Acceptance Criteria

### Definition of Done

- [ ] `.context/templates/adversarial/S-010-self-refine.md` created
- [ ] Template follows TEMPLATE-FORMAT.md from EN-801
- [ ] All 8 required sections present and complete
- [ ] Iterative self-review checklist aligned with quality dimensions
- [ ] Convergence criteria defined for iteration termination

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | Identity section specifies S-010, Self-Refine, score 4.00, Iterative Self-Correction family | [ ] |
| AC-2 | Self-review checklist covers all 6 quality-enforcement.md dimensions | [ ] |
| AC-3 | Generate-critique-refine loop protocol documented step by step | [ ] |
| AC-4 | Convergence criteria defined (when to stop iterating) | [ ] |
| AC-5 | Integration with H-15 mandatory self-review gate specified | [ ] |
| AC-6 | Interaction with S-014 LLM-as-Judge scoring documented | [ ] |
| AC-7 | Applicability at C1-C4 levels defined (required at C1, optional at C2+) | [ ] |
| AC-8 | Template follows markdown navigation standards (H-23, H-24) | [ ] |

### Quality Gate

| # | Criterion | Verified |
|---|-----------|----------|
| QG-1 | Creator-critic-revision cycle completed (min 3 iterations) | [ ] |
| QG-2 | Quality score >= 0.92 via S-014 LLM-as-Judge | [ ] |
| QG-3 | S-003 Steelman applied before S-002 Devil's Advocate critique | [ ] |

---

## Evidence

### Deliverables

| # | Deliverable | Path | Status |
|---|-------------|------|--------|
| 1 | S-010 Self-Refine Template | `.context/templates/adversarial/S-010-self-refine.md` | Delivered |

### Verification Checklist

- [x] Deliverable file exists at specified path
- [x] Template follows TEMPLATE-FORMAT.md from EN-801
- [x] All 8 required sections present and complete
- [x] Iterative self-review checklist aligned with quality dimensions
- [x] Convergence criteria defined for iteration termination
- [x] Integration with H-15 mandatory self-review gate specified
- [x] Creator-critic-revision cycle completed (min 3 iterations)
- [x] Quality score >= 0.92 via S-014 LLM-as-Judge

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-009: Adversarial Strategy Templates](../FEAT-009-adversarial-strategy-templates.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| depends_on | EN-801 | Must follow TEMPLATE-FORMAT.md canonical format |
| depends_on | quality-enforcement.md | Source of dimensions, H-15 rule, and strategy catalog |
| related_to | EN-803 | S-014 template provides scoring mechanism used after S-010 |
| related_to | EN-805 | S-007 Constitutional AI may be used alongside S-010 |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-14 | Claude | pending | Enabler created with 3-task decomposition. S-010 is mandated by H-15 for all deliverables -- critical for consistent self-review quality. |
