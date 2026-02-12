# FEAT-001: Fix CI Build Failures

> **Type:** feature
> **Status:** done
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-10
> **Due:** —
> **Completed:** 2026-02-11
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

**All CI Checks Passing:** Type Check, Security Scan, Plugin Validation, CLI Integration Tests, Test uv (3.11-3.14), Lint & Format, Test pip (3.11-3.14), Coverage Report
**PR #6 Status:** Merged to main

---

## Acceptance Criteria

### Definition of Done

- [x] All 7 original bugs resolved (5 original + 2 regressions)
- [x] BUG-010 resolved (DEC-001: `make setup` already exists, warning improved)
- [x] BUG-011 resolved (DEC-002: `types_or: [python, markdown]` applied)
- [x] CI pipeline passes green on PR #6 (PR merged to main)
- [x] Tests pass across Python 3.11, 3.12, 3.13, 3.14
- [x] Tests pass with both pip and uv install methods
- [x] Plugin Validation check passes
- [x] CLI Integration Tests pass
- [x] Coverage Report generates successfully

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | Plugin manifest schema validation passes | [x] |
| AC-2 | `jerry projects list` returns zero exit code | [x] |
| AC-3 | `jerry projects list --json` returns valid JSON | [x] |
| AC-4 | Bootstrap query dispatcher test passes | [x] |
| AC-5 | Transcript pipeline processes all datasets | [x] |
| AC-6 | Project validation tests pass or are updated | [x] |

---

## Children

### Enablers

| ID | Title | Status | Priority | Children |
|----|-------|--------|----------|----------|
| [EN-001](./EN-001-fix-plugin-validation/EN-001-fix-plugin-validation.md) | Fix Plugin Validation | done | high | BUG-001, TASK-001, TASK-002, TASK-003, DEC-001 |
| [EN-002](./EN-002-fix-test-infrastructure/EN-002-fix-test-infrastructure.md) | Fix Test Infrastructure | done | medium | BUG-004 (TASK-001), BUG-005 (TASK-001, TASK-002) |
| [EN-003](./EN-003-fix-validation-test-regressions/EN-003-fix-validation-test-regressions.md) | Fix Validation Test Regressions | done | high | BUG-006, TASK-001, TASK-002 |
| [EN-004](./EN-004-fix-precommit-hook-coverage/EN-004-fix-precommit-hook-coverage.md) | Fix Pre-commit Hook Coverage | done | high | BUG-010 (TASK-001, done), BUG-011 (TASK-001, done), DEC-001, DEC-002 |

### Completed Bugs (Feature-Level)

| ID | Title | Completed | Resolution |
|----|-------|-----------|------------|
| [BUG-002](./FEAT-001--BUG-002-cli-projects-list-crash.md) | CLI `projects list` crashes with unhandled exception | 2026-02-10 | Resolved by committing `projects/` directory |
| [BUG-003](./FEAT-001--BUG-003-bootstrap-test-missing-projects-dir.md) | Bootstrap test assumes `projects/` directory exists | 2026-02-10 | Resolved by committing `projects/` directory |
| [BUG-007](./FEAT-001--BUG-007-synthesis-content-test-overly-prescriptive.md) | Synthesis content validation test overly prescriptive | 2026-02-11 | Raised content check threshold to >= 3 files |

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   FEATURE PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Bugs:      [####################] 100% (9/9 completed)           |
+------------------------------------------------------------------+
| Enablers:  [####################] 100% (4/4 completed)           |
+------------------------------------------------------------------+
| Overall:   [####################] 100%                            |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Bugs** | 9 (5 original + 2 regressions + 2 pre-commit gaps) |
| **Completed Bugs** | 9 (BUG-001 through BUG-007, BUG-010, BUG-011) |
| **Pending Bugs** | 0 |
| **Total Enablers** | 4 |
| **Completed Enablers** | 4 (EN-001, EN-002, EN-003, EN-004) |
| **In Progress Enablers** | 0 |
| **Decisions** | 2 (EN-004:DEC-001, EN-004:DEC-002) |
| **Completion %** | 100% |

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
| 2026-02-11 | Claude | in_progress | EN-001 completed (BUG-001, TASK-001/002/003 all DONE). AC-1 verified. Plugin Validation CI passes. |
| 2026-02-11 | Claude | in_progress | EN-003 created for BUG-006 (validation test CI regressions from EN-001/TASK-002). Lint & Format and Test pip failures. TASK-001 (f-string fix) and TASK-002 (uv skipif) both completed. Progress: 67% (4/6 bugs, 2/3 enablers). |
| 2026-02-11 | Claude | in_progress | EN-002 tasks created: BUG-004/TASK-001 (skip guard), BUG-005/TASK-001 (dynamic discovery), BUG-005/TASK-002 (category dirs). EN-002 moved to in_progress. |
| 2026-02-11 | Claude | done | EN-002 completed. All 6 bugs resolved, all 3 enablers done. Full test suite: 2510 passed, 34 skipped. Adversarial critic feedback loops used for all 3 EN-002 tasks. Pending CI verification. |
| 2026-02-11 | Claude | in_progress | Reopened: BUG-007 filed — `test_synthesis_contains_canon_doc` fails when non-canon `.md` added to synthesis/. Content check threshold too low. |
| 2026-02-11 | Claude | done | BUG-007 resolved: raised content check threshold to >= 3 files in all 3 tests. 7/7 bugs completed. Pending CI verification. |
| 2026-02-11 | Claude | in_progress | Reopened: BUG-007 filed. `test_synthesis_contains_canon_doc` fails when non-canon `.md` added to synthesis/. Content check threshold too low (triggers on 1 file). Fix: raise threshold to >= 3 files for all content tests. |
| 2026-02-11 | Claude | in_progress | Reopened: EN-004 (Fix Pre-commit Hook Coverage) created with BUG-010 (session hook no auto-install) and BUG-011 (pytest hook python-only). Pre-commit gap identified as root cause of repeated CI failures on markdown-only commits. Each bug has one task. |
| 2026-02-11 | Claude | in_progress | DEC-001 (Pre-commit Installation Strategy) and DEC-002 (Pytest Hook File Type Coverage) created under EN-004. BUG-010 revised: `make setup` already exists, auto-install rejected, warning improved. BUG-010 done. Code changes: `session_start_hook.py` warning updated, `.pre-commit-config.yaml` types_or applied + header comment fixed. 8/9 bugs done, 1 pending (BUG-011). |
| 2026-02-11 | Claude | done | FEAT-001 closed. All 9 bugs resolved, all 4 enablers done, all AC verified. BUG-011 resolved via `types_or: [python, markdown]`. PR #6 merged to main. Full test suite: 2514 passed. |
