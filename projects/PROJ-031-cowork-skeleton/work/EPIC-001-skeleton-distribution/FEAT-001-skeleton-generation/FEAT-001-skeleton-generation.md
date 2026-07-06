# FEAT-001: Skeleton Generation

<!--
TEMPLATE: Feature
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.4
PURPOSE: Deterministic, idempotent regeneration of the projects-stripped CoWork skeleton with a minimal stub
-->

> **Type:** feature
> **Status:** pending
> **Priority:** high
> **Impact:** high
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

Define the deterministic, idempotent transformation that produces the CoWork skeleton from `main`: strip the `projects/` tree, add a minimal `projects/` stub (empty `projects/` plus a README guiding users to create their own project), and validate that the result loads as a CoWork plugin under the file limit. Running the transformation twice on the same input MUST yield the same output (idempotent).

**Value Proposition:**
- Reduces tracked file count from ~6,344 to ~1,744 (well under the ~5,000 CoWork limit)
- Keeps the plugin surface intact so Jerry remains fully functional after stripping
- Preserves fresh-install bootstrap via the minimal `projects/` stub (H-04)

---

## Benefit Hypothesis

**We believe that** a deterministic, idempotent skeleton-generation transformation

**Will result in** a reproducible distribution branch that CI can regenerate on demand without drift or manual steps

**We will know we have succeeded when** repeated regeneration from the same `main` commit produces byte-identical skeleton output that passes file-count and plugin-load validation

---

## Acceptance Criteria

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | Generated skeleton contains fewer than 5,000 tracked files | [ ] |
| AC-2 | Generated skeleton retains `.claude-plugin/`, `skills/`, `.claude/`, and `.context/` intact | [ ] |
| AC-3 | Generated skeleton contains a minimal `projects/` stub with a user-guidance README and no project subfolders | [ ] |
| AC-4 | Regenerating from the same source commit produces identical skeleton output (idempotent) | [ ] |
| AC-5 | A fresh install from the skeleton bootstraps a new project without error (H-04 satisfied) | [ ] |

---

## Children Stories

### Story Inventory

| ID | Type | Title | Status | Priority | Effort |
|----|------|-------|--------|----------|--------|
| STORY-001 | Story | Skeleton Regeneration Script | pending | high | 5 |
| STORY-002 | Story | Minimal projects/ Stub and README | pending | high | 3 |
| STORY-003 | Story | Skeleton Validation and Acceptance | pending | high | 5 |

### Work Item Links

- [STORY-001: Skeleton Regeneration Script](./STORY-001-regeneration-script/STORY-001-regeneration-script.md)
- [STORY-002: Minimal projects/ Stub and README](./STORY-002-projects-stub-readme/STORY-002-projects-stub-readme.md)
- [STORY-003: Skeleton Validation and Acceptance](./STORY-003-validation-acceptance/STORY-003-validation-acceptance.md)

---

## Progress Summary

```
+------------------------------------------------------------------+
|                   FEATURE PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Stories:   [....................] 0% (0/3 completed)              |
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
| Blocks | EN-001 | CI sync automation invokes this regeneration transformation |
| Related | FEAT-002 | Security review covers the regeneration/force-push pipeline |

### GitHub Issue Parity (H-32)

- **GitHub Issue:** Pending — per H-32, this jerry-repo Feature requires a corresponding GitHub Issue. Child issues to be created after the approval gate; tracked under parent Epic [#305](https://github.com/geekatron/jerry/issues/305).

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-06-26 | adam.nowak | pending | Feature created with three Stories |
