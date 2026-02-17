# TASK-004: Integrate risk-based quality gates (C1-C4 mapping)

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
> **Assignee:** nse-risk

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

Integrate risk-based quality gates into the NASA-SE skill, mapping criticality levels (C1-C4) to review intensity and adversarial cycle requirements. C1/C2 (high criticality) requires full adversarial cycles with strict scoring thresholds; C3/C4 (lower criticality) allows abbreviated review with relaxed requirements.

---

## Acceptance Criteria

- [ ] Criticality levels C1-C4 mapped to review intensity levels
- [ ] C1 (mission-critical) quality gate requirements defined
- [ ] C2 (safety-relevant) quality gate requirements defined
- [ ] C3 (important) quality gate requirements defined with abbreviated review option
- [ ] C4 (routine) quality gate requirements defined with minimal review option
- [ ] Quality thresholds per criticality level reference SSOT (EN-701)
- [ ] Risk-based gate protocol documented with clear decision criteria
- [ ] Documentation follows markdown navigation standards

---

## Implementation Notes

- Reference ADR-EPIC002-001 for criticality-based review intensity design
- C1/C2 should require: full creator-critic-revision cycle, >= 0.92 threshold, independent reviewer
- C3 may allow: single-pass review with scoring, >= 0.85 threshold
- C4 may allow: self-review with checklist, no formal scoring
- Align with NPR 7123.1D risk classification where applicable
- Gate protocol should include: entry criteria, review steps, exit criteria, escalation path

---

## Related Items

- Parent: [EN-708: NASA-SE Adversarial Mode](EN-708-nasa-se-adversarial.md)
- Depends on: EN-701 (SSOT for criticality levels and thresholds)
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
| Risk-based quality gate mapping | Markdown | Integrated into SKILL.md or PLAYBOOK.md |

### Verification

- [ ] Acceptance criteria verified
- [ ] All four criticality levels have defined gate requirements
- [ ] Thresholds are consistent with EN-701 SSOT

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation from EN-708 task decomposition |
