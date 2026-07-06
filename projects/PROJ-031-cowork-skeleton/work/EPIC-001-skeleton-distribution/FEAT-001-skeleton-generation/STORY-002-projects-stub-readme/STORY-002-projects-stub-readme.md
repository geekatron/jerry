# STORY-002: Minimal projects/ Stub and README

<!--
TEMPLATE: Story
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
PURPOSE: Minimal projects/ stub that preserves fresh-install bootstrap on the skeleton branch
-->

> **Type:** story
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-06-26T12:00:00Z
> **Due:**
> **Completed:**
> **Parent:** FEAT-001
> **Owner:** adam.nowak
> **Effort:** 3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | As a / I want / So that |
| [Summary](#summary) | Scope and approach |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Progress Summary](#progress-summary) | Overall progress |
| [Related Items](#related-items) | Links, dependencies, GitHub parity |
| [History](#history) | Status changes |

---

## User Story

**As a** new Jerry user installing from the CoWork skeleton

**I want** a minimal `projects/` stub with clear guidance to create my own project

**So that** Jerry bootstraps correctly on a fresh install even though all sample projects were stripped

---

## Summary

Author the minimal `projects/` stub that ships on the skeleton branch: an empty `projects/` directory plus a README that explains the skeleton has no bundled projects and walks the user through creating their first project so that H-04 (active project required) is satisfiable out of the box.

**Scope:**
- Minimal `projects/` directory that persists in git (no real project content)
- README guiding first-project creation and pointing at `/worktracker` and bootstrap
- Content that survives regeneration (the stub is the canonical fixture installed by STORY-001)

---

## Acceptance Criteria

### Acceptance Checklist

- [ ] User sees a `projects/` README on the skeleton branch explaining no projects are bundled
- [ ] README guides the user to create their first project and set the active project (H-04)
- [ ] Stub contains no real project subfolders carried over from `main`
- [ ] Stub `projects/` directory persists in git on a fresh clone of the skeleton branch
- [ ] Bootstrap on a fresh skeleton install reaches a state where an active project can be set

---

## Progress Summary

```
+------------------------------------------------------------------+
|                    STORY PROGRESS TRACKER                         |
+------------------------------------------------------------------+
| Tasks:     [....................] 0% (0/0 defined)                |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                              |
+------------------------------------------------------------------+
```

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-001: Skeleton Generation](../FEAT-001-skeleton-generation.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Blocks | STORY-001 | The regeneration script installs this stub |

### GitHub Issue Parity (H-32)

- **GitHub Issue:** Pending — per H-32, GitHub Issue parity is required. Child issues to be created after the approval gate; tracked under parent Epic [#305](https://github.com/geekatron/jerry/issues/305).

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-06-26 | adam.nowak | pending | Story created |
