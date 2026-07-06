# STORY-006: Tutorial: Install Jerry in Claude CoWork

<!--
TEMPLATE: Story
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
PURPOSE: Diataxis tutorial guiding a new user through installing Jerry in Claude CoWork
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

**As a** new Jerry user on Claude CoWork

**I want** a step-by-step tutorial for installing Jerry from the skeleton branch

**So that** I can reach a working Jerry install through guided hands-on steps

---

## Summary

Write the Diataxis tutorial (via `/diataxis`) that takes a first-time user from nothing to a working Jerry install in Claude CoWork using the `cowork-skeleton` branch. Learning-oriented: prerequisites, ordered steps, a visible result at each step, and no alternative branches.

**Scope:**
- Prerequisites and starting state
- Ordered install steps using the skeleton branch
- A first bootstrap that produces a working project

---

## Acceptance Criteria

### Acceptance Checklist

- [ ] Reader can follow ordered steps from prerequisites to a working CoWork install
- [ ] Tutorial uses the `cowork-skeleton` branch as the install source
- [ ] Tutorial shows a visible result at each step (learning-oriented)
- [ ] Tutorial ends with the reader bootstrapping a first project
- [ ] Document is classified as a Diataxis tutorial (no how-to or reference mixing)

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
| Depends On | FEAT-001 | Tutorial installs from the generated skeleton |
| Related | TASK-004 | Document is wired into MkDocs navigation |

### GitHub Issue Parity (H-32)

- **GitHub Issue:** Pending — per H-32, GitHub Issue parity is required. Child issues to be created after the approval gate; tracked under parent Epic [#305](https://github.com/geekatron/jerry/issues/305).

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-06-26 | adam.nowak | pending | Story created |
