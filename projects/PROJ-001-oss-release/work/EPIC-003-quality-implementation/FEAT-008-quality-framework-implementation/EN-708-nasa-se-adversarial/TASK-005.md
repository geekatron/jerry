# TASK-005: Create strategy selection guidance for NSE domain contexts

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
> **Parent:** EN-708
> **Assignee:** ps-analyst

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

Create a decision matrix mapping NASA systems engineering domain contexts (requirements review, design verification, risk assessment, V&V activities) to recommended adversarial strategies. This guidance helps SE agents select the most effective strategy for their current SE process context.

---

## Acceptance Criteria

- [ ] Decision matrix maps NSE contexts to recommended adversarial strategies
- [ ] Contexts covered include: requirements review, design verification, risk assessment, V&V
- [ ] Each context-strategy mapping includes rationale for effectiveness
- [ ] Guidance is traceable to EPIC-002 EN-303 decision tree design
- [ ] Matrix references SSOT (EN-701) for strategy encodings
- [ ] NPR 7123.1D process alignment noted where applicable
- [ ] Documentation follows markdown navigation standards

---

## Implementation Notes

- Reference EPIC-002 EN-303 for the decision tree for situational strategy selection
- Requirements review context may benefit from completeness/ambiguity strategies
- Design verification may benefit from assumption challenging and boundary analysis
- Risk assessment may benefit from failure mode and stress-testing strategies
- V&V activities may benefit from independent verification and cross-checking strategies
- Strategies should be referenced by their SSOT encoding (e.g., S-001, S-002, etc.)

---

## Related Items

- Parent: [EN-708: NASA-SE Adversarial Mode](EN-708-nasa-se-adversarial.md)
- Depends on: EN-701 (SSOT for strategy encodings)
- Depends on: EPIC-002 EN-303 (decision tree design)
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
| Strategy selection matrix | Markdown | Integrated into SKILL.md or PLAYBOOK.md |

### Verification

- [ ] Acceptance criteria verified
- [ ] All major NSE contexts are covered
- [ ] Strategy recommendations align with EPIC-002 EN-303

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation from EN-708 task decomposition |
