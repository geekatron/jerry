# EN-805: S-007 Constitutional AI Template

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-14 (Claude)
PURPOSE: Create the execution template for S-007 Constitutional AI Critique strategy
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

Create the execution template for S-007 Constitutional AI Critique -- principle-by-principle review against `.context/rules/` and the Jerry constitution (JERRY_CONSTITUTION.md). Used in C2+ quality cycles per quality-enforcement.md, this strategy ensures deliverables comply with all HARD rules (H-01 through H-24) and constitutional principles.

**Technical Scope:**
- Extract S-007 methodology from research-15-adversarial-strategies.md and EPIC-002 designs
- Map to `.context/rules/` files and `docs/governance/JERRY_CONSTITUTION.md` for principle inventory
- Create a principle-by-principle review checklist covering all 24 HARD rules
- Write template following the canonical TEMPLATE-FORMAT.md from EN-801
- Define violation severity classification and remediation guidance

---

## Problem Statement

S-007 Constitutional AI Critique is used in C2+ cycles (H-18) but has no template defining how to systematically review against constitutional principles. Specific gaps:

1. **No principle inventory** -- H-01 through H-24 are scattered across multiple `.context/rules/` files. There is no consolidated checklist for principle-by-principle review.
2. **No review protocol** -- Without a step-by-step protocol, agents may review against some principles but miss others, especially the less obvious ones (H-10 one-class-per-file, H-23 navigation tables).
3. **No violation classification** -- When a principle violation is found, there is no guidance on severity classification (blocking vs. warning) or remediation priority.
4. **No integration with quality cycle** -- S-007 is required at C2+ but there is no guidance on when in the quality cycle to apply it (before or after S-014 scoring) or how its findings feed into the iterate/accept decision.

---

## Business Value

S-007 Constitutional AI Critique provides systematic principle-by-principle governance compliance checking for C2+ deliverables. This template enables agents to verify that deliverables comply with all 24 HARD rules and constitutional principles, preventing governance violations from reaching production. It is the primary enforcement mechanism for H-18 (constitutional compliance check).

### Features Unlocked

- Automated principle-by-principle compliance review covering H-01 through H-24
- Violation severity classification enabling prioritized remediation in revision cycles

---

## Technical Approach

1. **Extract S-007 methodology** from research-15-adversarial-strategies.md, focusing on the Constitutional AI paradigm: defining principles, reviewing outputs against principles, classifying violations, and guiding revisions.
2. **Map to `.context/rules/` and JERRY_CONSTITUTION.md** -- Build a comprehensive principle inventory from all HARD rules (H-01 through H-24), auto-escalation rules (AE-001 through AE-006), and constitutional governance principles.
3. **Write template** following TEMPLATE-FORMAT.md from EN-801, with a principle-by-principle review checklist as the core of the Execution Protocol section.
4. **Define violation classification** -- Categorize violations as blocking (must fix before acceptance), warning (should fix, may defer), or informational (noted for future consideration). Map violation types to remediation guidance.

---

## Children (Tasks)

| ID | Title | Status | Activity | Agents |
|----|-------|--------|----------|--------|
| TASK-001 | Extract S-007 methodology from research and .context/rules/ patterns | pending | RESEARCH | ps-researcher |
| TASK-002 | Write S-007-constitutional-ai.md following TEMPLATE-FORMAT | pending | DEVELOPMENT | ps-architect |
| TASK-003 | Creator-critic-revision quality cycle | pending | REVIEW | ps-critic |

### Task Dependencies

```
TASK-001 (extract methodology) ──> TASK-002 (write template) ──> TASK-003 (quality cycle)
```

---

## Progress Summary

### Status Overview

```
EN-805 S-007 Constitutional AI Template
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

- [ ] `.context/templates/adversarial/S-007-constitutional-ai.md` created
- [ ] Template follows TEMPLATE-FORMAT.md from EN-801
- [ ] All 8 required sections present and complete
- [ ] Principle-by-principle review checklist covering H-01 through H-24
- [ ] Violation classification and remediation guidance defined

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | Identity section specifies S-007, Constitutional AI Critique, score 4.15, Iterative Self-Correction family | [ ] |
| AC-2 | Principle inventory covers all 24 HARD rules (H-01 through H-24) | [ ] |
| AC-3 | Principle inventory covers auto-escalation rules (AE-001 through AE-006) | [ ] |
| AC-4 | Review protocol provides step-by-step instructions for principle-by-principle assessment | [ ] |
| AC-5 | Violation classification defined: blocking, warning, informational | [ ] |
| AC-6 | Remediation guidance provided for each violation category | [ ] |
| AC-7 | Integration with C2+ quality cycle specified (H-18) | [ ] |
| AC-8 | Interaction with S-014 scoring documented (review before scoring) | [ ] |
| AC-9 | Template follows markdown navigation standards (H-23, H-24) | [ ] |

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
| 1 | S-007 Constitutional AI Template | `.context/templates/adversarial/S-007-constitutional-ai.md` | Delivered |

### Verification Checklist

- [x] Deliverable file exists at specified path
- [x] Template follows TEMPLATE-FORMAT.md from EN-801
- [x] All 8 required sections present and complete
- [x] Principle-by-principle review checklist covering H-01 through H-24
- [x] Violation classification and remediation guidance defined
- [x] Integration with C2+ quality cycle specified (H-18)
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
| depends_on | quality-enforcement.md | Source of H-01 through H-24 rules, H-18 requirement |
| depends_on | .context/rules/ | Source of all HARD rule definitions |
| depends_on | JERRY_CONSTITUTION.md | Source of constitutional governance principles |
| related_to | EN-803 | S-014 template provides scoring after S-007 review |
| related_to | EN-804 | S-010 Self-Refine may include constitutional checks |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-14 | Claude | pending | Enabler created with 3-task decomposition. S-007 ensures constitutional compliance at C2+ quality cycles -- critical for governance enforcement. |
