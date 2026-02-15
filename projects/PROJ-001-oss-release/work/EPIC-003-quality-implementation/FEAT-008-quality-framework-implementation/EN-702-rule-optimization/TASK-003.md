# TASK-003: Assign Rule IDs (H-01 through H-24, M-xx, S-xx)

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** DONE
> **Priority:** HIGH
> **Activity:** DESIGN
> **Agents:** ps-architect
> **Created:** 2026-02-14
> **Parent:** EN-702

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

Assign unique rule IDs to all rules identified in TASK-002's content audit. HARD rules receive IDs H-01 through H-24, MEDIUM rules receive M-xx prefixes, and SOFT rules receive S-xx prefixes. Produce a rule ID registry mapping each ID to its rule text, source file, and enforcement tier. This registry enables traceable compliance references and L2 re-injection targeting.

### Acceptance Criteria

- [ ] All HARD rules assigned unique IDs (H-01 through H-24)
- [ ] All MEDIUM rules assigned unique IDs (M-01 through M-xx)
- [ ] All SOFT rules assigned unique IDs (S-01 through S-xx)
- [ ] Rule ID registry produced with: ID, rule text, source file, tier
- [ ] No duplicate IDs across any tier
- [ ] IDs are stable and suitable for cross-referencing in other documents
- [ ] Registry includes mapping to EN-701 SSOT constants where applicable

### Related Items

- Parent: [EN-702: Rule File Token Optimization](EN-702-rule-optimization.md)
- Depends on: TASK-002 (content audit)
- Blocks: TASK-004 through TASK-009 (optimization tasks)

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
| Rule ID registry | Design artifact | -- |

### Verification

- [ ] Acceptance criteria verified
- [ ] All IDs unique and consistently formatted
- [ ] Registry cross-referenced with audit report

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation. Design gate -- rule IDs must be assigned before optimization tasks can apply them to files. |
