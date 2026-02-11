# FEAT-001: Fix CI Build Failures

> **Type:** feature
> **Status:** in_progress
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-10
> **Due:** —
> **Completed:** —
> **Parent:** EPIC-001
> **Owner:** Adam Nowak
> **Target Sprint:** —

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and value proposition |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Children](#children) | Enablers and completed bugs |
| [Progress Summary](#progress-summary) | Overall feature progress |
| [Related Items](#related-items) | Hierarchy and dependencies |
| [History](#history) | Status changes and key events |

---

## Summary

Fix all CI build failures on PR #6 (`feature/PROJ-001-vtt-troubleshooting`) to unblock the merge to main. The CI pipeline has 5 distinct failure categories affecting Plugin Validation, CLI Integration Tests, Bootstrap Tests, Transcript Pipeline Tests, and Project Validation Tests. All failures reproduce across Python 3.11-3.14, both pip and uv install methods.

**Value Proposition:**
- Unblock PR #6 merge to main
- Ensure CI pipeline passes green across all Python versions
- Establish clean baseline for OSS release

**Passing Checks:** Lint & Format, Type Check, Security Scan
**Failing Checks:** Plugin Validation, CLI Integration Tests, Test pip (3.11-3.14), Test uv (3.11-3.14), Coverage Report (skipped)

---

## Acceptance Criteria

### Definition of Done

- [ ] All 5 bugs resolved
- [ ] CI pipeline passes green on PR #6
- [ ] Tests pass across Python 3.11, 3.12, 3.13, 3.14
- [ ] Tests pass with both pip and uv install methods
- [ ] Plugin Validation check passes
- [ ] CLI Integration Tests pass
- [ ] Coverage Report generates successfully

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | Plugin manifest schema validation passes | [ ] |
| AC-2 | `jerry projects list` returns zero exit code | [ ] |
| AC-3 | `jerry projects list --json` returns valid JSON | [ ] |
| AC-4 | Bootstrap query dispatcher test passes | [ ] |
| AC-5 | Transcript pipeline processes all datasets | [ ] |
| AC-6 | Project validation tests pass or are updated | [ ] |

---

## Children

### Enablers

| ID | Title | Status | Priority | Children |
|----|-------|--------|----------|----------|
| [EN-001](./EN-001-fix-plugin-validation/EN-001-fix-plugin-validation.md) | Fix Plugin Validation | in_progress | high | BUG-001, TASK-001/002/003, DEC-001 |
| [EN-002](./EN-002-fix-test-infrastructure/EN-002-fix-test-infrastructure.md) | Fix Test Infrastructure | pending | medium | BUG-004, BUG-005 |

### Completed Bugs (Feature-Level)

| ID | Title | Completed | Resolution |
|----|-------|-----------|------------|
| [BUG-002](./FEAT-001--BUG-002-cli-projects-list-crash.md) | CLI `projects list` crashes with unhandled exception | 2026-02-10 | Resolved by committing `projects/` directory |
| [BUG-003](./FEAT-001--BUG-003-bootstrap-test-missing-projects-dir.md) | Bootstrap test assumes `projects/` directory exists | 2026-02-10 | Resolved by committing `projects/` directory |

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   FEATURE PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Bugs:      [########............] 40% (2/5 completed)             |
+------------------------------------------------------------------+
| Overall:   [########............] 40%                              |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Bugs** | 5 |
| **Completed Bugs** | 2 (BUG-002, BUG-003) |
| **In Progress Bugs** | 1 (BUG-001) |
| **Pending Bugs** | 2 (BUG-004, BUG-005) |
| **Completion %** | 40% |

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-001: OSS Release Preparation](../EPIC-001-oss-release.md)

### PR Reference

- **PR #6:** [fix: Windows CRLF line ending support in VTT validator](https://github.com/geekatron/jerry/pull/6)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-10 | Claude | pending | Feature created |
| 2026-02-10 | Claude | in_progress | 5 bugs triaged from PR #6 CI failures |
| 2026-02-10 | Claude | in_progress | BUG-002 and BUG-003 resolved (committing projects/ dir). BUG-001 root cause corrected (marketplace schema, not draft mismatch). BUG-004 and BUG-005 root causes confirmed. Progress: 40% (2/5 bugs completed). |
| 2026-02-10 | Claude | in_progress | Restructured to use Enablers: EN-001 (Fix Plugin Validation) groups BUG-001 + tasks + decision; EN-002 (Fix Test Infrastructure) groups BUG-004 + BUG-005. Completed BUG-002/003 remain at Feature level. |
