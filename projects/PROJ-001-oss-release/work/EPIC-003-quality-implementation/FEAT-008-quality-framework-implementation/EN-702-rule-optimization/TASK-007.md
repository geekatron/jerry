# TASK-007: Optimize python-environment.md and project-workflow.md

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

Optimize `.context/rules/python-environment.md` and `.context/rules/project-workflow.md` by applying rule IDs from TASK-003, replacing verbose explanations with concise HARD/MEDIUM/SOFT enforcement language, removing cross-file redundancy, replacing inline constants with references to EN-701 SSOT, and tagging critical rules for L2 re-injection.

### Acceptance Criteria

- [ ] `python-environment.md` optimized with rule IDs and tier vocabulary
- [ ] `project-workflow.md` optimized with rule IDs and tier vocabulary
- [ ] HARD rules use MUST/SHALL/NEVER language
- [ ] MEDIUM rules use SHOULD/RECOMMENDED language
- [ ] Inline constants replaced with EN-701 SSOT references
- [ ] Critical rules tagged for L2 re-injection (V-024)
- [ ] Markdown navigation standards (NAV-001 through NAV-006) maintained
- [ ] No semantic loss from original rules
- [ ] Per-file token count recorded for validation in TASK-010

### Related Items

- Parent: [EN-702: Rule File Token Optimization](EN-702-rule-optimization.md)
- Depends on: TASK-003 (rule ID assignment)
- Blocks: TASK-010 (token validation)
- Can run in parallel with: TASK-004, TASK-005, TASK-006, TASK-008, TASK-009

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
| Optimized `python-environment.md` | Rule file | -- |
| Optimized `project-workflow.md` | Rule file | -- |

### Verification

- [ ] Acceptance criteria verified
- [ ] Before/after token counts recorded
- [ ] Semantic equivalence confirmed

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation. Parallelizable with TASK-004 through TASK-006, TASK-008, TASK-009 after TASK-003 completes. |
