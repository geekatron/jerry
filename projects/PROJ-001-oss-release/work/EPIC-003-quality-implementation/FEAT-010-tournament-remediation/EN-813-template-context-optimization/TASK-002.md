# TASK-002: Update adv-executor.md to load only Execution Protocol section

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** BACKLOG
> **Priority:** HIGH
> **Activity:** DEVELOPMENT
> **Agents:** ps-architect
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

Update the adv-executor.md agent specification to implement lazy loading — load only the Execution Protocol section during strategy execution. Other sections (Identity, Purpose, Prerequisites, Output Format, Scoring Rubric, Examples, Integration) are loaded on-demand only when explicitly referenced.

### Acceptance Criteria

- [ ] adv-executor spec updated with lazy loading instructions
- [ ] Full template only loaded when explicitly needed
- [ ] Backward compatible with existing invocation patterns

### Related Items

- Parent: [EN-813: Template Context Optimization](EN-813-template-context-optimization.md)
- Dependency: TASK-001 (section parser must exist)

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
| Updated adv-executor.md specification | Documentation | --- |
| Lazy loading implementation | Code | --- |
| Backward compatibility verification | Test | --- |

### Verification

- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-15 | Created | Task created from EN-813 technical approach. |
