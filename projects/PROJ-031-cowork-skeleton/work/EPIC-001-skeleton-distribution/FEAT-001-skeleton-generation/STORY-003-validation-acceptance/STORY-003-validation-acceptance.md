# STORY-003: Skeleton Validation and Acceptance

<!--
TEMPLATE: Story
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
PURPOSE: Acceptance checks proving the skeleton is under the file limit and still loads as a plugin
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

**I want** an automated acceptance check on the generated skeleton

**So that** a regeneration that breaks the file limit or the plugin surface is rejected before it is published

---

## Summary

Define the acceptance gate that every generated skeleton MUST pass before it becomes the published `cowork-skeleton` branch: assert the tracked-file count is under the CoWork limit AND assert the plugin still loads (the plugin surface `.claude-plugin/`, `skills/`, `.claude/`, `.context/` is present and well-formed). This gate is consumed by EN-001 (CI) as a publish precondition.

**Scope:**
- Tracked-file count assertion against the CoWork limit (~5,000)
- Plugin-load assertion (required surface present and parseable)
- Pass/fail signal usable as a CI gate

---

## Acceptance Criteria

### Acceptance Checklist

- [ ] Acceptance check reports the skeleton tracked-file count and fails when it is 5,000 or more
- [ ] Acceptance check fails when any required plugin path is missing or malformed
- [ ] Acceptance check passes for a correctly generated skeleton (under limit, surface intact)
- [ ] Acceptance check emits a machine-readable pass/fail result for CI consumption
- [ ] Acceptance check confirms the minimal `projects/` stub is present

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
| Depends On | STORY-001 | Validation runs against the regeneration output |
| Blocks | EN-001 | CI uses this check as a publish precondition |

### GitHub Issue Parity (H-32)

- **GitHub Issue:** Pending — per H-32, GitHub Issue parity is required. Child issues to be created after the approval gate; tracked under parent Epic [#305](https://github.com/geekatron/jerry/issues/305).

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-06-26 | adam.nowak | pending | Story created |
