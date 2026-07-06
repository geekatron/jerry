# STORY-007: How-To: Sync/Update Skeleton and Troubleshoot File-Limit

<!--
TEMPLATE: Story
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
PURPOSE: Diataxis how-to for syncing/updating the skeleton and troubleshooting the file-limit
-->

> **Type:** story
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Created:** 2026-06-26T12:00:00Z
> **Due:**
> **Completed:**
> **Parent:** FEAT-003
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

**As a** Jerry user who already installed the skeleton

**I want** task-focused how-to guides for updating the skeleton and fixing file-limit errors

**So that** I can keep my install current and recover when CoWork rejects the plugin for size

---

## Summary

Write the Diataxis how-to guides (via `/diataxis`) for the two recurring user tasks: updating an existing CoWork install to the latest skeleton, and troubleshooting the CoWork file-limit when a plugin fails to load. Goal-oriented and action-only, written for a competent user who already has Jerry installed.

**Scope:**
- How-to: update an existing install to the latest `cowork-skeleton`
- How-to: diagnose and resolve a CoWork file-limit load failure
- Action-only steps (no tutorial-style teaching)

---

## Acceptance Criteria

### Acceptance Checklist

- [ ] User can update an existing install to the latest skeleton by following the guide
- [ ] User can diagnose a CoWork file-limit load failure using the troubleshooting steps
- [ ] User can resolve the file-limit failure and reach a loading plugin
- [ ] Guides are action-only and goal-oriented (Diataxis how-to, no tutorial mixing)

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

- **Parent Feature:** [FEAT-003: User Documentation (Diataxis) and MkDocs](../FEAT-003-user-documentation.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | EN-001 | Update guide reflects the CI sync workflow |
| Related | TASK-004 | Document is wired into MkDocs navigation |

### GitHub Issue Parity (H-32)

- **GitHub Issue:** Pending — per H-32, GitHub Issue parity is required. Child issues to be created after the approval gate; tracked under parent Epic [#305](https://github.com/geekatron/jerry/issues/305).

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-06-26 | adam.nowak | pending | Story created |
