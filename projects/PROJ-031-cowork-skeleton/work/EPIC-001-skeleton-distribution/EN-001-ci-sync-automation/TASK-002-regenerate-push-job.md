# TASK-002: Regenerate-and-Push Job

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
PURPOSE: CI job that regenerates the skeleton from main and force-pushes the cowork-skeleton branch
-->

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-06-26T12:00:00Z
> **Completed:**
> **Parent:** EN-001
> **Owner:** adam.nowak
> **Activity:** deployment
> **Effort:** 3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Description](#description) | What this task does |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Related Items](#related-items) | Links and GitHub parity |
| [History](#history) | Status changes |

---

## Description

Implement the CI job that checks out `main`, runs the FEAT-001 regeneration transformation, runs the STORY-003 acceptance gate, and force-pushes the result to `cowork-skeleton`. The job regenerates the branch rather than merging into it, and is safe to re-run (idempotent).

---

## Acceptance Criteria

- [ ] Job regenerates the skeleton from the latest `main` and force-pushes `cowork-skeleton`
- [ ] Job performs a regenerate-from-scratch, never a merge into the skeleton branch
- [ ] Job aborts the push when the acceptance gate fails
- [ ] Re-running the job on the same `main` commit yields the same published result (idempotent)
- [ ] Job sends a failure notification when any step fails

---

## Related Items

- **Parent:** [EN-001: CI Sync Automation](./EN-001-ci-sync-automation.md)
- **Depends On:** STORY-001 (regeneration script), STORY-003 (acceptance gate)
- **GitHub Issue Parity (H-32):** Pending — child issues to be created after the approval gate; tracked under parent Epic [#305](https://github.com/geekatron/jerry/issues/305).

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-06-26 | pending | Task created |
