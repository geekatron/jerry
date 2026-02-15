# EN-803: S-014 LLM-as-Judge Template

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-14 (Claude)
PURPOSE: Create the execution template for S-014 LLM-as-Judge strategy
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
> **Effort:** 5

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

Create the execution template for S-014 LLM-as-Judge -- the highest-scored strategy (4.40 composite) used in every quality cycle from C1 through C4. The template includes the 6-dimension weighted rubric, a step-by-step scoring protocol, calibration examples at multiple score levels, and integration instructions for the creator-critic-revision cycle.

**Technical Scope:**
- Extract S-014 methodology from research-15-adversarial-strategies.md and EPIC-002 designs
- Integrate with existing quality-enforcement.md dimensions (Completeness 0.20, Internal Consistency 0.20, Methodological Rigor 0.20, Evidence Quality 0.15, Actionability 0.15, Traceability 0.10)
- Write template following the canonical TEMPLATE-FORMAT.md from EN-801
- Include calibration examples showing score boundaries at 0.85 (below threshold), 0.92 (threshold), and 0.97 (excellent)
- Define leniency bias countermeasures per quality-enforcement.md L2-REINJECT rank=4

---

## Problem Statement

S-014 LLM-as-Judge is referenced throughout the quality framework as the primary scoring mechanism but has no concrete execution template. Specific gaps:

1. **No scoring protocol** -- The 6-dimension rubric exists in quality-enforcement.md with weights, but there are no step-by-step instructions for how to apply each dimension to a deliverable.
2. **No calibration examples** -- Without examples showing what a 0.85, 0.92, or 0.97 score looks like, scoring is subjective and prone to leniency bias.
3. **No leniency bias countermeasures** -- Quality-enforcement.md notes that "leniency bias must be actively counteracted" but provides no concrete mechanism for doing so.
4. **No integration protocol** -- S-014 is used at every criticality level, but there is no template defining how scoring results feed into the creator-critic-revision cycle's iterate/accept decision.

---

## Business Value

S-014 LLM-as-Judge is the primary scoring mechanism for the entire quality framework, used at every criticality level from C1 through C4. Providing a concrete execution template ensures consistent, reproducible quality scoring with calibrated thresholds and leniency bias countermeasures. This is the highest-priority strategy template in FEAT-009 because all other quality cycle workflows depend on S-014 for scoring.

### Features Unlocked

- Standardized 6-dimension quality scoring protocol usable by adv-scorer agent (EN-810)
- Calibrated score thresholds enabling consistent iterate/accept decisions in creator-critic-revision cycles

---

## Technical Approach

1. **Extract S-014 methodology** from research-15-adversarial-strategies.md, focusing on the LLM-as-Judge paradigm, scoring approaches, and bias mitigation techniques documented during EPIC-002 research.
2. **Integrate with quality-enforcement.md** -- Map the 6 dimensions (Completeness, Internal Consistency, Methodological Rigor, Evidence Quality, Actionability, Traceability) to concrete scoring criteria with per-dimension rubrics at the 1-5 scale.
3. **Write template** following TEMPLATE-FORMAT.md from EN-801, including all 8 required sections (Identity, Purpose, Prerequisites, Execution Protocol, Output Format, Scoring Rubric, Examples, Integration).
4. **Create calibration examples** showing detailed scoring breakdowns at three threshold levels: 0.85 (below threshold -- revision required), 0.92 (threshold -- acceptable), 0.97 (excellent -- exemplary quality).
5. **Define leniency bias countermeasures** -- Include explicit instructions for scoring strictly, anchoring to rubric criteria rather than overall impression, and applying steelman (S-003) before scoring to ensure fair but rigorous assessment.

---

## Children (Tasks)

| ID | Title | Status | Activity | Agents |
|----|-------|--------|----------|--------|
| TASK-001 | Extract S-014 methodology from research and EPIC-002 designs | pending | RESEARCH | ps-researcher |
| TASK-002 | Write S-014-llm-as-judge.md following TEMPLATE-FORMAT | pending | DEVELOPMENT | ps-architect |
| TASK-003 | Creator-critic-revision quality cycle | pending | REVIEW | ps-critic |

### Task Dependencies

```
TASK-001 (extract methodology) ──> TASK-002 (write template) ──> TASK-003 (quality cycle)
```

---

## Progress Summary

### Status Overview

```
EN-803 S-014 LLM-as-Judge Template
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

- [ ] `.context/templates/adversarial/S-014-llm-as-judge.md` created
- [ ] Template follows TEMPLATE-FORMAT.md from EN-801
- [ ] All 8 required sections present and complete
- [ ] 6-dimension weighted rubric with per-dimension scoring criteria
- [ ] Step-by-step scoring protocol with decision points

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | Identity section specifies S-014, LLM-as-Judge, score 4.40, Iterative Self-Correction family | [ ] |
| AC-2 | Scoring rubric aligns with quality-enforcement.md dimensions and weights | [ ] |
| AC-3 | Per-dimension criteria defined at 1-5 scale with concrete descriptors | [ ] |
| AC-4 | Weighted composite calculation documented with formula | [ ] |
| AC-5 | Calibration example at 0.85 (below threshold) with dimension breakdown | [ ] |
| AC-6 | Calibration example at 0.92 (threshold) with dimension breakdown | [ ] |
| AC-7 | Calibration example at 0.97 (excellent) with dimension breakdown | [ ] |
| AC-8 | Leniency bias countermeasures documented | [ ] |
| AC-9 | Integration with creator-critic-revision cycle specified | [ ] |
| AC-10 | Template follows markdown navigation standards (H-23, H-24) | [ ] |

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
| 1 | S-014 LLM-as-Judge Template | `.context/templates/adversarial/S-014-llm-as-judge.md` | Delivered |

### Verification Checklist

- [x] Deliverable file exists at specified path
- [x] Template follows TEMPLATE-FORMAT.md from EN-801
- [x] All 8 required sections present and complete
- [x] 6-dimension weighted rubric with per-dimension scoring criteria
- [x] Calibration examples at 0.85, 0.92, and 0.97 score levels
- [x] Leniency bias countermeasures documented
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
| depends_on | quality-enforcement.md | Source of dimensions, weights, and threshold |
| related_to | EN-804 | S-010 Self-Refine uses S-014 for scoring |
| related_to | EN-805 | S-007 Constitutional AI uses S-014 for scoring |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-14 | Claude | pending | Enabler created with 3-task decomposition. Highest-priority strategy template -- S-014 is the primary scoring mechanism for the entire quality framework. |
