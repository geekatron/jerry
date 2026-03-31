# BUG-009: tspec-analyst has no cross-slice aggregate coverage (#196)

> **Type:** bug
> **Status:** pending
> **Priority:** medium
> **Impact:** high
> **Severity:** major
> **Created:** 2026-03-31
> **Parent:** PROJ-030-bugs
> **Depends On:** BUG-008
> **GitHub Issue:** [#196](https://github.com/geekatron/jerry/issues/196)
> **Coordinating Epic:** EPIC-002 (PROJ-024)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description of the defect |
| [Steps to Reproduce](#steps-to-reproduce) | How to observe the defect |
| [Fix](#fix) | Proposed resolution |
| [Dependency](#dependency) | Upstream dependency on BUG-008 |
| [Files](#files) | Affected source files |
| [Acceptance Criteria](#acceptance-criteria) | Conditions for resolution |

---

## Summary

tspec-analyst evaluates coverage in two isolated modes: full-UC or single-slice. No mechanism aggregates coverage across multiple slices. Per-slice 100% coverage can hide cross-slice extension branches that are never tested.

## Steps to Reproduce

1. Slice a use case into 3+ slices with `/use-case` uc-slicer
2. Generate Feature files for each slice with `/test-spec` tspec-generator
3. Run tspec-analyst on each slice individually -- each reports 100% coverage
4. Observe there is no way to run aggregate coverage across all slices to detect untested cross-slice extension branches

## Fix

Add aggregate coverage mode that collects all slice Feature files for a given UC and computes union coverage. Detect extension branches that span multiple slices.

## Dependency

Depends on BUG-008 (denominator fix) — aggregate coverage needs the correct denominator baseline before it can compute accurate rollup metrics.

## Files

- `skills/test-spec/agents/tspec-analyst.md` (lines 90-107, coverage formula)
- `skills/test-spec/agents/tspec-analyst.governance.yaml`

## Acceptance Criteria

- [ ] tspec-analyst supports aggregate mode across multiple slice Feature files
- [ ] Cross-slice extension branches are detected and reported
- [ ] Aggregate report shows per-slice and rollup coverage metrics
