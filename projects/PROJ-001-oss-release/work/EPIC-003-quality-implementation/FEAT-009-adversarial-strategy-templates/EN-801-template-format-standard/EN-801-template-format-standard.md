# EN-801: Template Format Standard

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-14 (Claude)
PURPOSE: Define the canonical template format for adversarial strategy templates
-->

> **Type:** enabler
> **Status:** pending
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

Define the canonical template format for adversarial strategy templates. All sections, fields, scoring rubrics, and usage examples will be standardized in a single format definition file that all subsequent strategy templates (S-014, S-010, S-007, S-003, S-002, etc.) must follow.

**Technical Scope:**
- Survey existing templates in `.context/templates/` to identify common patterns
- Define the 8 required sections: Identity, Purpose, Prerequisites, Execution Protocol, Output Format, Scoring Rubric, Examples, Integration
- Specify field requirements and placeholder conventions for each section
- Write the canonical format file at `.context/templates/adversarial/TEMPLATE-FORMAT.md`
- Ensure format aligns with quality-enforcement.md dimensions and markdown navigation standards

---

## Problem Statement

Strategies are referenced by ID (S-001 through S-014) throughout the quality framework but have no standardized execution format. Without a canonical template:

1. **Inconsistent implementations** -- Each strategy template would define different sections, fields, and scoring approaches, making them difficult to use interchangeably.
2. **Non-reproducible results** -- Without a standardized execution protocol section, the same strategy applied by different agents could produce incomparable outputs.
3. **Integration gaps** -- Without a defined integration section, strategy templates cannot specify how they connect to the quality gate, criticality levels, or the creator-critic-revision cycle.
4. **Onboarding friction** -- New strategy template authors have no reference for what sections are required, what fields to include, or what format to follow.

---

## Business Value

Establishing the canonical template format is the foundation for all adversarial strategy templates in FEAT-009. Without a standardized format, strategy templates would be inconsistent and difficult to integrate into the quality cycle. This enabler ensures all subsequent strategy templates (S-001 through S-014) share a common structure, enabling automated validation and predictable agent execution.

### Features Unlocked

- Standardized template format enabling consistent strategy template authoring across EN-803 through EN-809
- Automated format compliance testing via EN-812 integration tests

---

## Technical Approach

1. **Survey existing templates** in `.context/templates/` (design/, worktracker/, requirements/) to identify common structural patterns, section conventions, and field formats that can be adapted for adversarial strategy templates.
2. **Define required sections** -- Specify the 8 mandatory sections (Identity, Purpose, Prerequisites, Execution Protocol, Output Format, Scoring Rubric, Examples, Integration) with field-level specifications for each.
3. **Write TEMPLATE-FORMAT.md** at `.context/templates/adversarial/TEMPLATE-FORMAT.md` with all sections, placeholder markers, and usage instructions following markdown navigation standards (H-23, H-24).
4. **Validate against quality framework** -- Ensure the template format integrates with quality-enforcement.md dimensions (Completeness, Internal Consistency, Methodological Rigor, Evidence Quality, Actionability, Traceability) and criticality levels (C1-C4).

---

## Children (Tasks)

| ID | Title | Status | Activity | Agents |
|----|-------|--------|----------|--------|
| TASK-001 | Research existing template patterns in .context/templates/ | pending | RESEARCH | ps-researcher |
| TASK-002 | Define canonical adversarial strategy template sections and fields | pending | DEVELOPMENT | ps-architect |
| TASK-003 | Write TEMPLATE-FORMAT.md | pending | DEVELOPMENT | ps-architect |

### Task Dependencies

```
TASK-001 (research patterns) ──> TASK-002 (define sections) ──> TASK-003 (write format file)
```

---

## Progress Summary

### Status Overview

```
EN-801 Template Format Standard
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

- [ ] `.context/templates/adversarial/TEMPLATE-FORMAT.md` created
- [ ] All 8 required sections defined with field specifications
- [ ] Format integrates with quality-enforcement.md dimensions and weights
- [ ] Format supports criticality levels C1-C4 with appropriate depth
- [ ] Placeholder conventions documented for template authors
- [ ] File follows markdown navigation standards (H-23, H-24)

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | Identity section specifies strategy ID, name, score, and family | [ ] |
| AC-2 | Purpose section specifies when and why to use the strategy | [ ] |
| AC-3 | Prerequisites section specifies required inputs and context | [ ] |
| AC-4 | Execution Protocol section provides step-by-step instructions | [ ] |
| AC-5 | Output Format section specifies deliverable structure | [ ] |
| AC-6 | Scoring Rubric section aligns with quality-enforcement.md 6 dimensions | [ ] |
| AC-7 | Examples section includes calibration examples at multiple score levels | [ ] |
| AC-8 | Integration section maps to criticality levels and quality cycle | [ ] |

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
| 1 | Template Format Standard | `.context/templates/adversarial/TEMPLATE-FORMAT.md` | Delivered |

### Verification Checklist

- [x] Deliverable file exists at specified path
- [x] All 8 required sections defined with field specifications
- [x] Format integrates with quality-enforcement.md dimensions and weights
- [x] Markdown navigation standards (H-23, H-24) followed
- [x] Creator-critic-revision cycle completed (min 3 iterations)
- [x] Quality score >= 0.92 via S-014 LLM-as-Judge

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-009: Adversarial Strategy Templates](../FEAT-009-adversarial-strategy-templates.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| depends_on | quality-enforcement.md | Source of quality dimensions, weights, and strategy catalog |
| blocks | EN-803 | S-014 template must follow this format standard |
| blocks | EN-804 | S-010 template must follow this format standard |
| blocks | EN-805 | S-007 template must follow this format standard |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-14 | Claude | pending | Enabler created with 3-task decomposition. Foundation enabler for FEAT-009 -- all subsequent strategy templates depend on this format standard. |
