# TASK-004: Add template reference to orchestration plan template

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

Add a "Worktracker Entity Templates" note to `skills/orchestration/templates/ORCHESTRATION_PLAN.template.md` stating that entity files created during orchestration MUST use canonical templates from `.context/templates/worktracker/`.

This ensures that every orchestration plan document generated from the template includes a visible reminder for implementers to use canonical templates when creating worktracker entity files (enablers, tasks, etc.) as part of orchestrated workflows.

### Acceptance Criteria

- [ ] Orchestration plan template includes a "Worktracker Entity Templates" note or section
- [ ] Note specifies the canonical template location: `.context/templates/worktracker/`
- [ ] Note uses MUST language (HARD enforcement) for template usage
- [ ] Note integrates naturally with the existing template structure

### Implementation Notes

File: `skills/orchestration/templates/ORCHESTRATION_PLAN.template.md`. Add a note in an appropriate location (likely near implementation phase guidance or deliverable definitions) with content such as:

> **Worktracker Entity Templates:** Entity files (EPIC, FEATURE, ENABLER, TASK, etc.) created during orchestration MUST use canonical templates from `.context/templates/worktracker/`. Read the template first, then populate. Do not create entity files from memory.

### Related Items

- Parent: [EN-820](EN-820-fix-behavioral-root-cause.md)
- Related: TASK-003 (parallel orchestration integration task)

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
| -- | -- | Unpopulated (BACKLOG status) |

### Verification

- [ ] Acceptance criteria verified
- [ ] Note follows existing template formatting conventions
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-15 | Created | Initial creation. Part of EN-820 orchestration integration. |
