# STORY-001: Skeleton Regeneration Script

<!--
TEMPLATE: Story
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
PURPOSE: Deterministic, idempotent script that strips projects/ and adds the minimal stub
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
> **Effort:** 5

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

**As a** Jerry maintainer

**I want** a deterministic, idempotent regeneration script that strips `projects/` and installs the minimal stub

**So that** the CoWork skeleton can be reproduced from any `main` commit without manual steps or drift

---

## Summary

Build the transformation that takes a checkout of `main` and produces the skeleton: remove all real project content under `projects/`, install the minimal stub (empty `projects/` plus user-guidance README), and leave the plugin surface untouched. The script MUST be deterministic (same input yields same output) and idempotent (re-running on an already-stripped tree is a no-op).

**Scope:**
- Strip logic for the `projects/` tree (real project folders removed)
- Stub installation hook (consumes STORY-002 output)
- Idempotency and determinism guarantees

---

## Acceptance Criteria

### Acceptance Checklist

- [ ] Script removes all real project subfolders under `projects/` from the working tree
- [ ] Script leaves `.claude-plugin/`, `skills/`, `.claude/`, and `.context/` unmodified
- [ ] Script produces identical output when run twice on the same source commit (idempotent)
- [ ] Script exits non-zero and changes nothing when the source tree is malformed or the stub is missing
- [ ] Script output contains the minimal `projects/` stub after completion

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
| Depends On | STORY-002 | Needs the minimal stub content to install |
| Blocks | STORY-003 | Validation runs against the script output |
| Blocks | EN-001 | CI workflow invokes this script |

### GitHub Issue Parity (H-32)

- **GitHub Issue:** Pending — per H-32, GitHub Issue parity is required. Child issues to be created after the approval gate; tracked under parent Epic [#305](https://github.com/geekatron/jerry/issues/305).

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-06-26 | adam.nowak | pending | Story created |
