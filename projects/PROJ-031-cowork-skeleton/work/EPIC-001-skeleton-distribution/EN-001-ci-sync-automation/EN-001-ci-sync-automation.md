# EN-001: CI Sync Automation

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
PURPOSE: GitHub Actions workflow that regenerates the cowork-skeleton branch from main and force-pushes it
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** high
> **Impact:** medium
> **Enabler Type:** infrastructure
> **Created:** 2026-06-26T12:00:00Z
> **Due:**
> **Completed:**
> **Parent:** EPIC-001
> **Owner:** adam.nowak
> **Effort:** 8

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this enabler covers |
| [Problem Statement](#problem-statement) | Why CI automation is needed |
| [Business Value](#business-value) | How it supports the Epic |
| [Technical Approach](#technical-approach) | Workflow design |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Children Tasks](#children-tasks) | Task breakdown |
| [Progress Summary](#progress-summary) | Overall progress |
| [Related Items](#related-items) | Links, dependencies, GitHub parity |
| [History](#history) | Status changes |

---

## Summary

A GitHub Actions workflow that regenerates the `cowork-skeleton` branch from `main` and force-pushes it on each release. The model is regenerate, never merge: the workflow checks out `main`, runs the skeleton transformation (FEAT-001), and force-pushes the result to `cowork-skeleton`. Default triggers are GitHub Release published and manual `workflow_dispatch`.

**Technical Scope:**
- Workflow triggers (Release published, `workflow_dispatch`) and least-privilege permissions
- Regenerate-from-main job that force-pushes `cowork-skeleton`
- Token and branch-protection strategy for the force-push target
- Idempotency and failure notification

---

## Problem Statement

The `cowork-skeleton` branch must stay in sync with `main` without manual surgery. Merging `main` into a stripped branch would reintroduce `projects/` history and cause conflicts. Regenerating the branch from scratch on each release avoids drift, but a force-push to a published branch is a sensitive operation that requires careful trigger, token, and branch-protection design.

---

## Business Value

Makes the skeleton distribution self-maintaining: every release automatically publishes a fresh, validated skeleton, so users always receive a current Jerry without maintainers performing error-prone manual steps.

### Features Unlocked

- Hands-off skeleton publication on every release
- A reproducible audit trail for what each skeleton was generated from

---

## Technical Approach

1. **Triggers and permissions** — Run on `release: published` and `workflow_dispatch`; grant the minimum token scope needed to push the target branch.
2. **Regenerate-from-main job** — Check out `main`, run the FEAT-001 transformation, run the STORY-003 acceptance gate, then force-push to `cowork-skeleton`.
3. **Token and branch protection** — Decide between the default `GITHUB_TOKEN`, a fine-grained PAT, or a GitHub App, and define a branch-protection posture for `cowork-skeleton` that still permits the automated force-push.
4. **Failure handling** — Notify on failure and never publish a skeleton that fails the acceptance gate.

---

## Acceptance Criteria

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| TC-1 | Workflow runs on Release published and on manual `workflow_dispatch` | [ ] |
| TC-2 | Workflow regenerates the skeleton from `main` and force-pushes `cowork-skeleton` (no merge) | [ ] |
| TC-3 | Workflow runs with least-privilege token scope sufficient only to push the target branch | [ ] |
| TC-4 | Workflow refuses to publish when the STORY-003 acceptance gate fails | [ ] |
| TC-5 | Workflow notifies maintainers on failure | [ ] |

---

## Children Tasks

### Task Inventory

| ID | Title | Status | Owner |
|----|-------|--------|-------|
| TASK-001 | Workflow Triggers and Permissions | pending | -- |
| TASK-002 | Regenerate-and-Push Job | pending | -- |
| TASK-003 | Token and Branch-Protection Strategy | pending | -- |

### Task Links

- [TASK-001: Workflow Triggers and Permissions](./TASK-001-workflow-triggers-permissions.md)
- [TASK-002: Regenerate-and-Push Job](./TASK-002-regenerate-push-job.md)
- [TASK-003: Token and Branch-Protection Strategy](./TASK-003-token-branch-protection.md)

---

## Progress Summary

```
+------------------------------------------------------------------+
|                   ENABLER PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Tasks:     [....................] 0% (0/3 completed)             |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                              |
+------------------------------------------------------------------+
```

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-001: Jerry CoWork Skeleton Distribution](../EPIC-001-skeleton-distribution.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | FEAT-001 | Invokes the skeleton regeneration transformation and acceptance gate |
| Related | FEAT-002 | Threat model and remediations target this workflow |

### GitHub Issue Parity (H-32)

- **GitHub Issue:** Pending — per H-32, this jerry-repo Enabler requires a corresponding GitHub Issue. Child issues to be created after the approval gate; tracked under parent Epic [#305](https://github.com/geekatron/jerry/issues/305).

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-06-26 | adam.nowak | pending | Enabler created with three Tasks (Epic-level Enabler per INV-EN03) |
