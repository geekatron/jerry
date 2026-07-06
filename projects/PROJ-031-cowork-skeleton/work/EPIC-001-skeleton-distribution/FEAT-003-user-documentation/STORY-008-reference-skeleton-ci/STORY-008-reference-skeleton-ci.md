# STORY-008: Reference: Skeleton Branch and CI Workflow

<!--
TEMPLATE: Story
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
PURPOSE: Diataxis reference for the skeleton branch and CI workflow; hosts the MkDocs wiring Task
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
| [Children Tasks](#children-tasks) | MkDocs wiring task |
| [Progress Summary](#progress-summary) | Overall progress |
| [Related Items](#related-items) | Links, dependencies, GitHub parity |
| [History](#history) | Status changes |

---

## User Story

**As a** Jerry user or contributor

**I want** authoritative reference documentation for the skeleton branch and its CI workflow

**So that** I can look up exactly what the skeleton contains and how the regeneration pipeline behaves

---

## Summary

Write the Diataxis reference (via `/diataxis`) describing the `cowork-skeleton` branch and the regeneration CI workflow: what the skeleton includes and excludes, the minimal `projects/` stub, the triggers and behavior of the regenerate-and-force-push workflow, and the acceptance gate. Information-oriented and austere. This Story also hosts the MkDocs wiring Task (TASK-004), because a Task cannot be a direct child of a Feature under the containment rules.

**Scope:**
- Reference: skeleton branch contents (included/excluded, stub)
- Reference: CI workflow triggers, regenerate-not-merge behavior, acceptance gate
- Hosts TASK-004 (MkDocs/docs.yml wiring of all four documents)

---

## Acceptance Criteria

### Acceptance Checklist

- [ ] Reference describes what the skeleton branch includes and excludes
- [ ] Reference describes the minimal `projects/` stub
- [ ] Reference describes the CI workflow triggers and regenerate-not-merge behavior
- [ ] Reference is information-oriented and austere (Diataxis reference, no how-to mixing)

---

## Children Tasks

### Task Inventory

| ID | Title | Status | Owner |
|----|-------|--------|-------|
| TASK-004 | MkDocs and docs.yml Wiring | pending | -- |

### Task Links

- [TASK-004: MkDocs and docs.yml Wiring](./TASK-004-mkdocs-docs-wiring.md)

---

## Progress Summary

```
+------------------------------------------------------------------+
|                    STORY PROGRESS TRACKER                         |
+------------------------------------------------------------------+
| Tasks:     [....................] 0% (0/1 completed)             |
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
| Depends On | FEAT-001 | Reference documents the generated skeleton and stub |
| Depends On | EN-001 | Reference documents the CI sync workflow |

### GitHub Issue Parity (H-32)

- **GitHub Issue:** Pending — per H-32, GitHub Issue parity is required. Child issues to be created after the approval gate; tracked under parent Epic [#305](https://github.com/geekatron/jerry/issues/305).

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-06-26 | adam.nowak | pending | Story created; hosts TASK-004 (MkDocs wiring) |
