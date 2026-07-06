# TASK-003: Token and Branch-Protection Strategy

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
PURPOSE: Decide the credential and branch-protection posture for the force-pushed cowork-skeleton branch
-->

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-06-26T12:00:00Z
> **Completed:**
> **Parent:** EN-001
> **Owner:** adam.nowak
> **Activity:** design
> **Effort:** 2

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

Decide and document the credential and branch-protection posture for the automated force-push to `cowork-skeleton`: which identity pushes (default token, fine-grained PAT, or GitHub App), the minimum scope that identity needs, and how branch protection on `cowork-skeleton` coexists with an automated force-push. This task feeds FEAT-002 (security and threat model).

---

## Acceptance Criteria

- [ ] Push identity selected and justified (default token vs fine-grained PAT vs GitHub App)
- [ ] Selected identity is scoped to the minimum permission needed to push the target branch
- [ ] Branch-protection posture for `cowork-skeleton` documented and compatible with the automated force-push
- [ ] Strategy records the residual force-push risk for handoff to FEAT-002

---

## Related Items

- **Parent:** [EN-001: CI Sync Automation](./EN-001-ci-sync-automation.md)
- **Related:** FEAT-002 (Security and Threat Model)
- **GitHub Issue Parity (H-32):** Pending — child issues to be created after the approval gate; tracked under parent Epic [#305](https://github.com/geekatron/jerry/issues/305).

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-06-26 | pending | Task created |
