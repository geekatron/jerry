# TASK-001: Workflow Triggers and Permissions

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
PURPOSE: Configure CI workflow triggers and least-privilege permissions for skeleton regeneration
-->

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-06-26T12:00:00Z
> **Completed:**
> **Parent:** EN-001
> **Owner:** adam.nowak
> **Activity:** deployment
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

Configure the regeneration workflow's triggers and permission scope: run on `release: published` and manual `workflow_dispatch`, and declare the minimum permissions the workflow needs (no broad write access beyond what the push target requires).

---

## Acceptance Criteria

- [ ] Workflow triggers on Release published
- [ ] Workflow triggers on manual `workflow_dispatch`
- [ ] Workflow declares least-privilege permissions sufficient only for the regeneration and push
- [ ] Workflow does not trigger on unrelated branch pushes or pull requests

---

## Related Items

- **Parent:** [EN-001: CI Sync Automation](./EN-001-ci-sync-automation.md)
- **GitHub Issue Parity (H-32):** Pending — child issues to be created after the approval gate; tracked under parent Epic [#305](https://github.com/geekatron/jerry/issues/305).

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-06-26 | pending | Task created |
