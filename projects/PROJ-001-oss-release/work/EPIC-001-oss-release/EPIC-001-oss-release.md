# EPIC-001: OSS Release Preparation

> **Type:** epic
> **Status:** in_progress
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-10
> **Due:** —
> **Completed:** —
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
- Fix all CI build failures blocking PR merge (FEAT-001 - done)
- Conduct deep research on Claude Code best practices (FEAT-002)
- Optimize CLAUDE.md and all skills using decomposition/imports patterns (FEAT-003)
- Ensure tests pass across Python 3.11-3.14
- Clean up project artifacts and configuration
- Create multi-persona documentation

---

## Business Outcome Hypothesis

**We believe that** fixing all CI failures, conducting thorough research, and optimizing the framework

**Will result in** a stable, well-tested, well-documented framework that can be publicly shared and attract contributors

**We will know we have succeeded when** all CI checks pass green, documentation is complete for L0/L1/L2 personas, and the repository is ready for public access

---

## Children (Features/Capabilities)

### Feature Inventory

| ID | Title | Status | Priority | Progress |
|----|-------|--------|----------|----------|
| FEAT-001 | Fix CI Build Failures | done | high | 100% |
| FEAT-002 | Research and Preparation | done | high | 100% |
| FEAT-003 | CLAUDE.md Optimization | in_progress | critical | 57% |

### Feature Links

- [FEAT-001: Fix CI Build Failures](./FEAT-001-fix-ci-build-failures/FEAT-001-fix-ci-build-failures.md)
- [FEAT-002: Research and Preparation](./FEAT-002-research-and-preparation/FEAT-002-research-and-preparation.md)
- [FEAT-003: CLAUDE.md Optimization](./FEAT-003-claude-md-optimization/FEAT-003-claude-md-optimization.md)

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                     EPIC PROGRESS TRACKER                         |
+------------------------------------------------------------------+
| Features:  [#############.......] 67% (2/3 completed)             |
| Enablers:  [################....] 80% (16/20 completed)           |
| Bugs:      [####################] 100% (15/15 completed)          |
| Tasks:     [################....] 80% (~60/~75 completed)         |
+------------------------------------------------------------------+
| Overall:   [###############.....] 75%                              |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Features** | 3 |
| **Completed Features** | 2 (FEAT-001, FEAT-002) |
| **In Progress Features** | 1 (FEAT-003) |
| **Feature Completion %** | 67% |
| **Total Enablers** | 20 (4 FEAT-001 + 9 FEAT-002 + 7 FEAT-003) |
| **Completed Enablers** | 16 (4 FEAT-001 + 8 FEAT-002 + 4 FEAT-003) |
| **Total Bugs (FEAT-001)** | 7 (all resolved) |
| **Total Bugs (FEAT-003)** | 8 (all resolved) |

---

## Related Items

### PR Reference

- **PR #6:** [fix: Windows CRLF line ending support in VTT validator](https://github.com/geekatron/jerry/pull/6) — Merged

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-10 | Claude | pending | Epic created |
| 2026-02-10 | Claude | in_progress | FEAT-001 created with 5 bugs from PR #6 CI failures |
| 2026-02-10 | Claude | in_progress | Progress sync: 2/5 bugs completed (BUG-002, BUG-003). FEAT-001 restructured with EN-001, EN-002 Enablers. |
| 2026-02-11 | Claude | in_progress | EN-001 completed (BUG-001 + 3 tasks). EN-003 created and completed (BUG-006 regression from EN-001/TASK-002 + 2 tasks). Progress: 67% (4/6 bugs, 2/3 enablers). |
| 2026-02-11 | Claude | done | EN-002 completed (BUG-004 + BUG-005, 3 tasks). FEAT-001 100%. All 6 bugs resolved, all 3 enablers done. Full test suite 2510 passed locally. Pending CI verification on PR #6. |
| 2026-02-11 | Claude | in_progress | Reopened: BUG-007 filed for `test_synthesis_contains_canon_doc` failure. Content check threshold too low. |
| 2026-02-11 | Claude | done | BUG-007 resolved. Raised content check threshold to >= 3 files. 7/7 bugs completed. CI verified green. |
| 2026-02-11 | Claude | in_progress | Reopened: OSS launch not yet complete. FEAT-001 (CI fixes) done, but additional features needed. |
| 2026-02-11 | Claude | in_progress | Added FEAT-002 (Research, 7 enablers EN-101-107) and FEAT-003 (CLAUDE.md Optimization, 7 enablers EN-201-207, 44 tasks). |
| 2026-02-12 | Claude | in_progress | FEAT-002 closed (all 8 enablers done including EN-108 version bumping). PR #12 merged. 8 EN-202 bugs closed. EN-207 confirmed complete. FEAT-003 at 57%. |
