# FEAT-003: User Documentation (Diataxis) and MkDocs

<!--
TEMPLATE: Feature
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.4
PURPOSE: Diataxis four-quadrant user documentation for the CoWork skeleton, wired into the MkDocs site
-->

> **Type:** feature
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Created:** 2026-06-26T12:00:00Z
> **Due:**
> **Completed:**
> **Parent:** EPIC-001
> **Owner:** adam.nowak
> **Target Sprint:**

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Feature overview and value proposition |
| [Benefit Hypothesis](#benefit-hypothesis) | Expected benefits |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Children Stories](#children-stories) | Work decomposition |
| [Progress Summary](#progress-summary) | Overall progress |
| [Related Items](#related-items) | Links, dependencies, GitHub parity |
| [History](#history) | Status changes |

---

## Summary

Produce user-facing documentation for the CoWork skeleton across all four Diataxis quadrants and publish it to the MkDocs site: a tutorial (install Jerry in Claude CoWork), a how-to (sync/update the skeleton and troubleshoot the file-limit), a reference (the skeleton branch and CI workflow), and an explanation (why the skeleton exists). A wiring Task connects the four documents into the MkDocs navigation and publish pipeline.

**Value Proposition:**
- Gives users a guided path from zero to a working CoWork install
- Documents the sync/update and troubleshooting workflow
- Explains the rationale so users trust and correctly use the skeleton

---

## Benefit Hypothesis

**We believe that** documenting the skeleton across all four Diataxis quadrants and publishing to MkDocs

**Will result in** users installing and maintaining the CoWork skeleton without maintainer support

**We will know we have succeeded when** all four documents are published in the MkDocs site navigation and a new user can install from the tutorial alone

---

## Acceptance Criteria

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | Tutorial, how-to, reference, and explanation documents each exist and follow their Diataxis quadrant | [ ] |
| AC-2 | All four documents are reachable from the published MkDocs site navigation | [ ] |
| AC-3 | A new user can complete a CoWork install following the tutorial without external help | [ ] |
| AC-4 | The how-to covers skeleton sync/update and file-limit troubleshooting | [ ] |

---

## Children Stories

### Story Inventory

| ID | Type | Title | Status | Priority | Effort |
|----|------|-------|--------|----------|--------|
| STORY-006 | Story | Tutorial: Install Jerry in Claude CoWork | pending | medium | 3 |
| STORY-007 | Story | How-To: Sync/Update Skeleton and Troubleshoot File-Limit | pending | medium | 3 |
| STORY-008 | Story | Reference: Skeleton Branch and CI Workflow | pending | medium | 3 |
| STORY-009 | Story | Explanation: Why the Skeleton Exists | pending | medium | 2 |

### Work Item Links

- [STORY-006: Tutorial: Install Jerry in Claude CoWork](./STORY-006-tutorial-install-cowork/STORY-006-tutorial-install-cowork.md)
- [STORY-007: How-To: Sync/Update Skeleton and Troubleshoot File-Limit](./STORY-007-howto-sync-skeleton/STORY-007-howto-sync-skeleton.md)
- [STORY-008: Reference: Skeleton Branch and CI Workflow](./STORY-008-reference-skeleton-ci/STORY-008-reference-skeleton-ci.md)
- [STORY-009: Explanation: Why the Skeleton Exists](./STORY-009-explanation-why-skeleton/STORY-009-explanation-why-skeleton.md)

> **Note:** TASK-004 (MkDocs and docs.yml wiring) lives under STORY-008 because a Feature cannot directly contain a Task per the containment rules (Feature allows only Story and Enabler children). See STORY-008.

---

## Progress Summary

```
+------------------------------------------------------------------+
|                   FEATURE PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Stories:   [....................] 0% (0/4 completed)              |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                              |
+------------------------------------------------------------------+
```

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-001: Jerry CoWork Skeleton Distribution](../EPIC-001-skeleton-distribution.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | FEAT-001 | Reference and how-to document the generated skeleton and stub |
| Depends On | EN-001 | Reference documents the CI sync workflow |

### GitHub Issue Parity (H-32)

- **GitHub Issue:** Pending — per H-32, this jerry-repo Feature requires a corresponding GitHub Issue. Child issues to be created after the approval gate; tracked under parent Epic [#305](https://github.com/geekatron/jerry/issues/305).

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-06-26 | adam.nowak | pending | Feature created with four Diataxis Stories; mkdocs wiring Task nested under STORY-008 |
