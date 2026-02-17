# TASK-009: Optimize CLAUDE.md Root Context

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

Optimize the root `CLAUDE.md` file by applying tier vocabulary, removing verbose explanations, replacing inline constants with references to EN-701 SSOT, and ensuring it serves as an efficient entry point to the navigation hierarchy. CLAUDE.md is loaded at every session start, so its token efficiency is critical for minimizing baseline context consumption.

### Acceptance Criteria

- [ ] `CLAUDE.md` optimized with tier vocabulary where applicable
- [ ] Verbose content compressed to concise directives
- [ ] Inline constants replaced with EN-701 SSOT references
- [ ] Navigation table maintained and accurate
- [ ] Critical constraints section preserved with HARD enforcement language
- [ ] No semantic loss from original content
- [ ] Token count recorded for validation in TASK-010

### Related Items

- Parent: [EN-702: Rule File Token Optimization](EN-702-rule-optimization.md)
- Depends on: TASK-003 (rule ID assignment)
- Blocks: TASK-010 (token validation)
- Can run in parallel with: TASK-004 through TASK-008

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
| Optimized `CLAUDE.md` | Root context file | -- |

### Verification

- [ ] Acceptance criteria verified
- [ ] Before/after token count recorded
- [ ] Navigation links still resolve correctly

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation. Parallelizable with TASK-004 through TASK-008 after TASK-003 completes. |
