# EPIC-001: OSS Release Preparation

> **Type:** epic
> **Status:** done
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-10
> **Due:** —
> **Completed:** 2026-02-11
> **Parent:** —
> **Owner:** Adam Nowak
> **Target Quarter:** FY26-Q1

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and key objectives |
| [Business Outcome Hypothesis](#business-outcome-hypothesis) | Expected business outcomes |
| [Children (Features/Capabilities)](#children-featurescapabilities) | Feature inventory and tracking |
| [Progress Summary](#progress-summary) | Overall epic progress |
| [Related Items](#related-items) | Hierarchy and dependencies |
| [History](#history) | Status changes and key events |

---

## Summary

Prepare the Jerry framework for public open-source release on GitHub. This epic covers all work needed to ensure the codebase is clean, CI is passing, documentation is complete, and the project is welcoming to contributors.

**Key Objectives:**
- Fix all CI build failures blocking PR merge
- Ensure tests pass across Python 3.11-3.14
- Clean up project artifacts and configuration

---

## Business Outcome Hypothesis

**We believe that** fixing all CI failures and preparing Jerry for OSS release

**Will result in** a stable, well-tested framework that can be publicly shared and attract contributors

**We will know we have succeeded when** all CI checks pass green on the release PR and the repository is ready for public access

---

## Children (Features/Capabilities)

### Feature Inventory

| ID | Title | Status | Priority | Progress |
|----|-------|--------|----------|----------|
| FEAT-001 | Fix CI Build Failures | done | high | 100% |

### Feature Links

- [FEAT-001: Fix CI Build Failures](./FEAT-001-fix-ci-build-failures/FEAT-001-fix-ci-build-failures.md)

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                     EPIC PROGRESS TRACKER                         |
+------------------------------------------------------------------+
| Features:  [####################] 100% (1/1 completed)            |
| Bugs:      [####################] 100% (6/6 completed)            |
| Enablers:  [####################] 100% (3/3 completed)            |
+------------------------------------------------------------------+
| Overall:   [####################] 100%                             |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Features** | 1 |
| **Completed Features** | 1 |
| **In Progress Features** | 0 |
| **Pending Features** | 0 |
| **Feature Completion %** | 100% |
| **Total Bugs** | 6 (5 original + 1 regression) |
| **Completed Bugs** | 6 (BUG-001, BUG-002, BUG-003, BUG-004, BUG-005, BUG-006) |
| **Bug Completion %** | 100% |

---

## Related Items

### PR Reference

- **PR #6:** [fix: Windows CRLF line ending support in VTT validator](https://github.com/geekatron/jerry/pull/6) — Build failing, blocking merge

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-10 | Claude | pending | Epic created |
| 2026-02-10 | Claude | in_progress | FEAT-001 created with 5 bugs from PR #6 CI failures |
| 2026-02-10 | Claude | in_progress | Progress sync: 2/5 bugs completed (BUG-002, BUG-003). FEAT-001 restructured with EN-001, EN-002 Enablers. |
| 2026-02-11 | Claude | in_progress | EN-001 completed (BUG-001 + 3 tasks). EN-003 created and completed (BUG-006 regression from EN-001/TASK-002 + 2 tasks). Progress: 67% (4/6 bugs, 2/3 enablers). |
| 2026-02-11 | Claude | done | EN-002 completed (BUG-004 + BUG-005, 3 tasks). FEAT-001 100%. All 6 bugs resolved, all 3 enablers done. Full test suite 2510 passed locally. Pending CI verification on PR #6. |
