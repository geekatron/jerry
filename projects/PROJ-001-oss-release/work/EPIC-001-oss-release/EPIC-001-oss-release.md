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
| FEAT-001 | Fix CI Build Failures | in_progress | high | 0% |

### Feature Links

- [FEAT-001: Fix CI Build Failures](./FEAT-001-fix-ci-build-failures/FEAT-001-fix-ci-build-failures.md)

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                     EPIC PROGRESS TRACKER                         |
+------------------------------------------------------------------+
| Features:  [....................] 0% (0/1 completed)              |
| Bugs:      [....................] 0% (0/5 completed)              |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                               |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Features** | 1 |
| **Completed Features** | 0 |
| **In Progress Features** | 1 |
| **Pending Features** | 0 |
| **Feature Completion %** | 0% |

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
