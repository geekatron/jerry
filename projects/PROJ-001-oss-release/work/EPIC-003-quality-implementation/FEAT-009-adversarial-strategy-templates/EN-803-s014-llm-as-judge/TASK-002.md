# TASK-002: Write S-014-llm-as-judge.md Following TEMPLATE-FORMAT

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** DONE
> **Priority:** HIGH
> **Activity:** DEVELOPMENT
> **Agents:** ps-architect
> **Created:** 2026-02-14
> **Parent:** EN-803

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

Create the S-014 LLM-as-Judge template at `.context/templates/adversarial/S-014-llm-as-judge.md` with all 8 required sections from TEMPLATE-FORMAT.md. Include the 6-dimension weighted rubric with per-dimension scoring criteria at the 1-5 scale, step-by-step scoring protocol, calibration examples showing detailed dimension breakdowns at 0.85 (below threshold), 0.92 (threshold), and 0.97 (excellent) score levels, and leniency bias countermeasures.

### Acceptance Criteria

- [ ] File created at `.context/templates/adversarial/S-014-llm-as-judge.md`
- [ ] Identity section: S-014, LLM-as-Judge, score 4.40, Iterative Self-Correction family
- [ ] Purpose section: when and why to use, applicability across C1-C4
- [ ] Prerequisites section: required inputs (deliverable, rubric, context)
- [ ] Execution Protocol section: step-by-step scoring instructions with decision points
- [ ] Output Format section: scoring report structure with dimension breakdowns
- [ ] Scoring Rubric section: 6 dimensions with per-dimension criteria at 1-5 scale, weighted composite formula
- [ ] Examples section: calibration at 0.85, 0.92, 0.97 with full dimension breakdowns
- [ ] Integration section: placement in quality cycle, iterate/accept decision logic
- [ ] Leniency bias countermeasures explicitly documented in Execution Protocol
- [ ] File follows markdown navigation standards (H-23, H-24)
- [ ] Quality gate: Deliverable reviewed via creator-critic-revision cycle (min 3 iterations)
- [ ] Quality gate: Score >= 0.92 via S-014 LLM-as-Judge rubric
- [ ] Quality gate: S-003 Steelman applied before S-002 Devil's Advocate critique

### Related Items

- Parent: [EN-803: S-014 LLM-as-Judge Template](EN-803-s014-llm-as-judge.md)
- Depends on: TASK-001 (methodology extraction)
- Blocks: TASK-003 (quality cycle)

---

## Time Tracking

| Metric | Value |
|--------|-------|
| Original Estimate | — |
| Remaining Work | 0 hours |
| Time Spent | — |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| `.context/templates/adversarial/S-014-llm-as-judge.md` | Strategy template | --- |

### Verification

- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation. Core deliverable -- the S-014 template is the primary scoring mechanism for the entire quality framework. |
