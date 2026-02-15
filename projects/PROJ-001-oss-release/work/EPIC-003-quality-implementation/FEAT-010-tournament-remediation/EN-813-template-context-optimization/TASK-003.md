# TASK-003: Measure and validate context consumption <= 10,000 tokens

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** BACKLOG
> **Priority:** HIGH
> **Activity:** REVIEW
> **Agents:** ps-critic
> **Created:** 2026-02-15
> **Parent:** EN-813

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

Measure actual context consumption when adv-executor uses lazy loading for a simulated C4 tournament (all 10 strategies). Validate that total template context is <= 10,000 tokens. Document the before/after comparison.

### Acceptance Criteria

- [ ] Measurement methodology documented
- [ ] Before measurement (full loading) captured
- [ ] After measurement (lazy loading) captured
- [ ] <= 10,000 token target met or deviation justified

### Related Items

- Parent: [EN-813: Template Context Optimization](EN-813-template-context-optimization.md)
- Dependency: TASK-002 (lazy loading must be implemented)

---

## Time Tracking

| Metric | Value |
|--------|-------|
| Original Estimate | — |
| Remaining Work | — |
| Time Spent | — |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Measurement methodology document | Documentation | --- |
| Before/after context consumption report | Report | --- |
| Token budget validation | Analysis | --- |

### Verification

- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-15 | Created | Task created from EN-813 technical approach. |
