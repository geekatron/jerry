# TASK-003: Add template compliance to orchestration SKILL.md

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
> **Created:** 2026-02-15
> **Parent:** EN-820

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Content](#content) | Description, acceptance criteria, implementation notes |
| [Time Tracking](#time-tracking) | Effort estimates |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Status changes and key events |

---

## Content

### Description

Add a WTI-007 row to the Constitutional Compliance table in `skills/orchestration/SKILL.md`. This ensures orchestration workflows are aware of worktracker template requirements when creating entity files during multi-phase orchestration plans.

Orchestration workflows frequently create worktracker entity files (enablers, tasks) as part of implementation phases. Without a reference to WTI-007 in the orchestration skill, orchestration agents may create entity files without consulting canonical templates.

### Acceptance Criteria

- [x] Constitutional Compliance table in orchestration SKILL.md includes a WTI-007 row
- [x] Row correctly references worktracker template compliance requirement
- [x] Row specifies when the rule applies (entity file creation during orchestration)

### Implementation Notes

File: `skills/orchestration/SKILL.md`, location: Constitutional Compliance table. Add a row following the existing table format:

| WTI-007 | Mandatory Template Usage | Entity files created during orchestration MUST use canonical templates from `.context/templates/worktracker/` |

### Related Items

- Parent: [EN-820](EN-820-fix-behavioral-root-cause.md)
- Related: TASK-004 (parallel orchestration integration task)

---

## Time Tracking

| Metric | Value |
|--------|-------|
| Original Estimate | 0.25 hours |
| Remaining Work | 0.25 hours |
| Time Spent | 0 hours |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| WTI-007 compliance row | Code change | `skills/orchestration/SKILL.md` Constitutional Compliance table |

### Verification

- [x] Acceptance criteria verified
- [x] Row follows existing Constitutional Compliance table formatting
- [x] Reviewed by: Claude (adversarial C3 cycle, 0.941 PASS)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-15 | Created | Initial creation. Part of EN-820 orchestration integration. |
| 2026-02-15 | DONE | Implemented. Commit 1b98ecc. |
