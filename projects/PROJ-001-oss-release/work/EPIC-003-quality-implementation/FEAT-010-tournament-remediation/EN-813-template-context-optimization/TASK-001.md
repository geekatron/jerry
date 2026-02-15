# TASK-001: Implement section-boundary parsing in adv-executor

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** pending
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
| [Evidence](#evidence) | Deliverables and verification |
| [Related Items](#related-items) | Parent and dependencies |
| [History](#history) | Change log |

---

## Summary

Implement section-boundary parsing logic in adv-executor to identify Execution Protocol section boundaries using markdown heading detection (## headings). Parse template files to extract only the Execution Protocol content between its ## heading and the next ## heading.

### Acceptance Criteria

- [ ] Section parser correctly identifies Execution Protocol boundaries in all 10 templates
- [ ] Parser handles edge cases (missing section, empty section)
- [ ] Unit test validates parsing accuracy

### Related Items

- Parent: [EN-813: Template Context Optimization](EN-813-template-context-optimization.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Section-boundary parsing implementation | Code | --- |
| Unit tests for section parser | Test | --- |
| Edge case handling logic | Code | --- |

### Verification

- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-15 | Created | Task created from EN-813 technical approach. |
