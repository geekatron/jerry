# TASK-004: Integrate quality scoring rubric (S-014 LLM-as-Judge)

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** DONE
> **Priority:** high
> **Activity:** DEVELOPMENT
> **Created:** 2026-02-14
> **Parent:** EN-707
> **Assignee:** ps-architect

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this task delivers |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Implementation Notes](#implementation-notes) | Technical guidance |
| [Time Tracking](#time-tracking) | Effort estimates and actuals |
| [Related Items](#related-items) | Dependencies and hierarchy |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Change log |

---

## Summary

Integrate the LLM-as-Judge (S-014) quality scoring rubric into the problem-solving skill. Define scoring dimensions (completeness, accuracy, evidence quality, logical coherence, actionability) and the >= 0.92 acceptance threshold for PS deliverables. Document how scoring is applied at each adversarial cycle exit gate.

---

## Acceptance Criteria

- [ ] Quality scoring rubric defined with PS-specific dimensions
- [ ] Scoring dimensions include: completeness, accuracy, evidence quality, logical coherence, actionability
- [ ] LLM-as-Judge (S-014) methodology referenced and integrated
- [ ] Quality threshold (>= 0.92) documented as pass/fail gate
- [ ] Scoring integration points defined for each PS workflow phase
- [ ] Rubric references SSOT (EN-701) for threshold constants
- [ ] Documentation follows markdown navigation standards

---

## Implementation Notes

- Reference EPIC-002 Final Synthesis for quality scoring methodology
- S-014 (LLM-as-Judge) provides the scoring paradigm; adapt dimensions to PS context
- Each dimension should have clear criteria for 0.0 to 1.0 scoring
- Weighted scoring may be appropriate (e.g., evidence quality weighted higher for research)
- Document the scoring rubric in a format that can be consumed by both humans and LLM agents

---

## Related Items

- Parent: [EN-707: Problem-Solving Adversarial Mode](EN-707-problem-solving-adversarial.md)
- Depends on: EN-701 (SSOT for quality threshold constants)
- Blocks: TASK-006 (adversarial review)

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
| Quality scoring rubric | Markdown | Integrated into SKILL.md or PLAYBOOK.md |

### Verification

- [ ] Acceptance criteria verified
- [ ] Scoring dimensions are clearly defined with measurable criteria
- [ ] Threshold is consistent with EN-701 SSOT

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation from EN-707 task decomposition |
