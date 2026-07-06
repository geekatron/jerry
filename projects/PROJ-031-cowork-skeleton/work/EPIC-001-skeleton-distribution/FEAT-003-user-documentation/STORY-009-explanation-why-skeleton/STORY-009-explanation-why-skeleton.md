# STORY-009: Explanation: Why the Skeleton Exists

<!--
TEMPLATE: Story
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
PURPOSE: Diataxis explanation of why the CoWork skeleton exists and how the distribution model works
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
> **Effort:** 2

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

**As a** Jerry user or contributor evaluating the skeleton distribution

**I want** an explanation of why the skeleton exists and how the regenerate-not-merge model works

**So that** I understand the rationale and trust the distribution approach

---

## Summary

Write the Diataxis explanation (via `/diataxis`) covering the conceptual background: the CoWork file-limit constraint, why `projects/` is stripped, why the branch is regenerated from `main` rather than merged, and the trade-offs of the derived-branch distribution model. Understanding-oriented and discursive.

**Scope:**
- The CoWork file-limit problem and why Jerry exceeds it
- Why `projects/` is stripped and a minimal stub kept
- Why regenerate-not-merge, and the trade-offs of the model

---

## Acceptance Criteria

### Acceptance Checklist

- [ ] Explanation describes the CoWork file-limit constraint and why Jerry exceeds it
- [ ] Explanation describes why `projects/` is stripped and a minimal stub kept
- [ ] Explanation describes why the branch is regenerated rather than merged
- [ ] Explanation is understanding-oriented and discursive (Diataxis explanation, no how-to mixing)

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
| Related | TASK-004 | Document is wired into MkDocs navigation |

### GitHub Issue Parity (H-32)

- **GitHub Issue:** Pending — per H-32, GitHub Issue parity is required. Child issues to be created after the approval gate; tracked under parent Epic [#305](https://github.com/geekatron/jerry/issues/305).

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-06-26 | adam.nowak | pending | Story created |
