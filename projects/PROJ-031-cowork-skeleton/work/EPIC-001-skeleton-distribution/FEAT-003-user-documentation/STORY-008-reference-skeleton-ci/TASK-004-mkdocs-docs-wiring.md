# TASK-004: MkDocs and docs.yml Wiring

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
PURPOSE: Wire the four Diataxis documents into mkdocs.yml navigation and the docs.yml publish pipeline
-->

> **Type:** task
> **Status:** pending
> **Priority:** medium
> **Created:** 2026-06-26T12:00:00Z
> **Completed:**
> **Parent:** STORY-008
> **Owner:** adam.nowak
> **Activity:** documentation
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

Wire the four Diataxis documents (tutorial, how-to, reference, explanation) into the MkDocs site navigation (`mkdocs.yml` nav) and ensure they are published by the docs publish workflow (`docs.yml`). This task is parented under STORY-008 because a Feature cannot directly contain a Task per the containment rules (Feature children are limited to Story and Enabler).

---

## Acceptance Criteria

- [ ] All four documents appear in the MkDocs site navigation
- [ ] All four documents are published by the docs publish workflow
- [ ] Navigation entries resolve to the correct rendered pages on the published site
- [ ] No broken internal links between the four documents on the published site

---

## Related Items

- **Parent:** [STORY-008: Reference: Skeleton Branch and CI Workflow](./STORY-008-reference-skeleton-ci.md)
- **Related:** STORY-006, STORY-007, STORY-009 (the documents being wired)
- **GitHub Issue Parity (H-32):** Pending — child issues to be created after the approval gate; tracked under parent Epic [#305](https://github.com/geekatron/jerry/issues/305).

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-06-26 | pending | Task created |
