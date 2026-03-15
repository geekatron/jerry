# BUG-010: tspec-analyst has no cross-slice aggregate coverage mechanism (#196)

> **Type:** bug
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Severity:** major
> **Created:** 2026-03-14
> **Parent:** PROJ-030-bugs
> **Owner:** unassigned

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and key details |
| [Steps to Reproduce](#steps-to-reproduce) | Steps to reproduce the issue |
| [Acceptance Criteria](#acceptance-criteria) | Conditions for bug to be fixed |
| [Related Items](#related-items) | Hierarchy and related work items |
| [History](#history) | Status changes and key events |

---

## Summary

A use case with multiple slices can achieve 100% per-slice coverage while missing extension branches that are only visible at the aggregate level. The tspec-analyst agent lacks a cross-slice aggregate coverage mechanism, so coverage gaps spanning multiple slices go undetected. This was identified as RT-006 during C4 tournament S-001 Red Team analysis.

**Key Details:**
- **File:** `skills/test-spec/agents/tspec-analyst.md`
- **Symptom:** 100% per-slice coverage reported despite missing aggregate-level extension branches
- **Frequency:** When use cases are decomposed into multiple slices with shared extensions
- **Fix Complexity:** Medium
- **Source:** C4 tournament S-001 Red Team (RT-006)

---

## Steps to Reproduce

1. Create a use case with multiple slices that share extension branches
2. Generate BDD feature files per slice using tspec-generator
3. Run tspec-analyst coverage analysis on each slice individually
4. Observe 100% coverage per slice
5. Manually verify against the full use case -- extension branches visible only at aggregate level are missing

---

## Acceptance Criteria

- [ ] tspec-analyst supports cross-slice aggregate coverage analysis
- [ ] Coverage report identifies extension branches missing at the aggregate level
- [ ] Per-slice coverage and aggregate coverage are reported separately
- [ ] Coverage gaps spanning multiple slices are flagged with affected slice references

---

## Related Items

### Hierarchy

- **Parent:** PROJ-030-bugs

### Related Items

- **GitHub Issue:** [#196](https://github.com/geekatron/jerry/issues/196)
- **Parent Issue:** [#194](https://github.com/geekatron/jerry/issues/194)
- **Labels:** bug

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-03-14 | pending | Triaged from GitHub Issue #196 |
