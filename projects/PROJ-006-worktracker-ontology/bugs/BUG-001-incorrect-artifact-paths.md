# BUG-001: Incorrect Artifact Paths for reviews/ and discoveries/

> **Bug ID:** BUG-001
> **Severity:** Medium
> **Status:** RESOLVED
> **Created:** 2026-01-14
> **Resolved:** 2026-01-14
> **Affected:** CL-003 review artifact, DISC-004 discovery artifact

---

## Summary

Pipeline artifacts (`reviews/` and `discoveries/` folders) were incorrectly placed inside `work/SE-001/FT-001/` instead of at the project root level alongside other pipeline artifacts (`research/`, `analysis/`, `synthesis/`, etc.).

## Root Cause

When creating the Critic Loop infrastructure, the `reviews/` and `discoveries/` folders were created relative to the ORCHESTRATION.yaml file location (`work/SE-001/FT-001/`) rather than at the project root where all other pipeline artifacts are stored.

This violated the established pattern:
- **Pipeline artifacts** (research, analysis, synthesis, decisions, templates, reviews, discoveries) → Project root
- **Work tracking documents** (enablers, work items, orchestration) → `work/` hierarchy

## Impact

1. Inconsistent artifact organization
2. Path references in markdown files pointed to wrong locations
3. Potential confusion for future session recovery

## Resolution

1. Moved `reviews/` contents from `work/SE-001/FT-001/reviews/` to project root `reviews/`
2. Moved `discoveries/` contents from `work/SE-001/FT-001/discoveries/` to project root `discoveries/`
3. Updated all path references in:
   - `en-004.md` (link paths)
   - `FEATURE-WORKTRACKER.md` (link paths)
   - `SOLUTION-WORKTRACKER.md` (artifact registry)
   - `WORKTRACKER.md` (artifact registry)
4. Added `artifact_paths` section to ORCHESTRATION.yaml (v2.1) to prevent future occurrences

## Prevention Measures

Added `artifact_paths` configuration section to ORCHESTRATION.yaml that clearly documents:

```yaml
artifact_paths:
  # Pipeline artifacts at project root
  research: "research/"
  analysis: "analysis/"
  synthesis: "synthesis/"
  decisions: "decisions/"
  templates: "templates/"
  reviews: "reviews/"           # Critic review artifacts
  discoveries: "discoveries/"   # Discovery documents
  reports: "reports/"
  runbooks: "runbooks/"

  # Work tracking documents in work/ hierarchy
  work_tracking: "work/"
  solution_epic: "work/SE-{id}/"
  feature: "work/SE-{se_id}/FT-{id}/"
```

## Files Changed

| File | Change |
|------|--------|
| `reviews/CL-003-synthesis-review.md` | Moved from `work/SE-001/FT-001/reviews/` |
| `reviews/REVIEW-TEMPLATE.md` | Moved from `work/SE-001/FT-001/reviews/` |
| `discoveries/disc-004-critic-loops.md` | Moved from `work/SE-001/FT-001/discoveries/` |
| `work/SE-001/FT-001/en-004.md` | Updated link paths (2 occurrences) |
| `work/SE-001/FT-001/FEATURE-WORKTRACKER.md` | Updated link paths (3 occurrences) |
| `work/SE-001/SOLUTION-WORKTRACKER.md` | Updated artifact registry, added discovery row |
| `WORKTRACKER.md` | Updated artifact registry paths, added discovery row |
| `work/SE-001/FT-001/ORCHESTRATION.yaml` | Added artifact_paths section, bumped to v2.1 |

## Lessons Learned

1. Before creating new artifact folders, consult the established pattern in existing artifact registries
2. The ORCHESTRATION.yaml artifact_paths section is now the canonical reference for artifact locations
3. Pipeline artifacts always go at project root; only work tracking documents go in `work/` hierarchy

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-14 | Bug identified and documented | Human |
| 2026-01-14 | Resolution implemented, ORCHESTRATION.yaml v2.1 | Claude |
