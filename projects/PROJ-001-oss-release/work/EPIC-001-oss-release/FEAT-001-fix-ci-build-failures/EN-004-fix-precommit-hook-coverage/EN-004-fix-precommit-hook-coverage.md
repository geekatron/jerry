# EN-004: Fix Pre-commit Hook Coverage

> **Type:** enabler
> **Status:** done
> **Priority:** high
> **Impact:** high
> **Enabler Type:** infrastructure
> **Created:** 2026-02-11
> **Due:** —
> **Completed:** 2026-02-11
> **Parent:** FEAT-001
> **Owner:** —
> **Effort:** —

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and technical scope |
| [Problem Statement](#problem-statement) | Why this enabler is needed |
| [Business Value](#business-value) | How enabler supports feature delivery |
| [Technical Approach](#technical-approach) | High-level technical approach |
| [Bugs](#bugs) | Bugs addressed by this enabler |
| [Decisions](#decisions) | Key decisions made |
| [Progress Summary](#progress-summary) | Overall enabler progress |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Related Items](#related-items) | Hierarchy and related work |
| [History](#history) | Status changes and key events |

---

## Summary

Fix two pre-commit hook coverage gaps that allow untested code to reach CI. ~~The session start hook warns about missing hooks but doesn't auto-install them~~ (BUG-010: revised — `make setup` already exists, warning improved), and the pytest pre-commit hook only triggers on Python file changes, skipping architecture tests that validate markdown content (BUG-011: fix confirmed).

**Technical Scope:**
- ~~Auto-install pre-commit hooks during session start~~ Improve session hook warning to reference `make setup` (BUG-010, DEC-001)
- Extend pytest hook trigger to include markdown file changes (BUG-011, DEC-002)

---

## Problem Statement

Two gaps in the pre-commit hook infrastructure cause repeated CI failures that could be caught locally:

1. **Warning doesn't reference `make setup` (BUG-010, revised):** The session start hook warning says "Run 'uv run pre-commit install'" instead of referencing the documented `make setup` mechanism. ~~Original framing was "no auto-install" but research (DEC-001) revealed `make setup` already handles installation.~~
2. **Python-only trigger (BUG-011):** The pytest hook in `.pre-commit-config.yaml` uses `types: [python]`, so markdown-only commits bypass the entire test suite — including architecture tests that validate markdown content (hardcoded paths, cross-project references).

Both gaps were identified as root causes of CI failures during markdown content corrections.

---

## Business Value

Resolves the root cause of repeated CI failures where locally-untested commits reach the pipeline. Prevents future regressions by ensuring all commits — regardless of file type — are validated locally before push.

### Features Unlocked

- ~~Zero-friction developer onboarding (hooks install automatically)~~
- Session hook warning aligns with documented `make setup` workflow
- Markdown-only commits validated locally (architecture tests run)
- Reduced CI failure rate from preventable issues

---

## Technical Approach

### BUG-010: Improve Session Hook Warning (DEC-001)
Update `check_precommit_hooks()` warning message in `scripts/session_start_hook.py` to reference `make setup` as the primary action, with Windows fallback.

### BUG-011: Extend Pytest Hook Trigger (DEC-002)
Change the pytest hook configuration in `.pre-commit-config.yaml`:
- Replace `types: [python]` with `types_or: [python, markdown]`
- This ensures pytest runs when either Python or markdown files are staged

---

## Bugs

| ID | Title | Status | Priority | Children |
|----|-------|--------|----------|----------|
| [BUG-010](./BUG-010-session-hook-no-auto-install.md) | ~~Session hook no auto-install~~ Warning doesn't reference `make setup` | done | low | TASK-001 |
| [BUG-011](./BUG-011-precommit-pytest-python-only.md) | Pre-commit pytest hook only triggers on Python file changes | done | high | TASK-001 |

### Tasks

| ID | Title | Parent | Status | Priority |
|----|-------|--------|--------|----------|
| [BUG-010/TASK-001](./BUG-010--TASK-001-auto-install-precommit-hooks.md) | ~~Auto-install~~ Improve warning message | BUG-010 | done | low |
| [BUG-011/TASK-001](./BUG-011--TASK-001-add-markdown-to-pytest-trigger.md) | Add markdown file types to pytest pre-commit hook trigger | BUG-011 | done | high |

### Decisions

| ID | Title | Status | Decisions |
|----|-------|--------|-----------|
| [DEC-001](./DEC-001-precommit-installation-strategy.md) | Pre-commit Hook Installation Strategy | ACCEPTED | D-001: Close BUG-010 (make setup exists), D-002: Improve warning text |
| [DEC-002](./DEC-002-pytest-hook-file-type-coverage.md) | Pytest Hook File Type Coverage | ACCEPTED | D-001: Use `types_or: [python, markdown]` |

### Dependency Chain

```
BUG-010 ── TASK-001 (improve warning)          [DONE]
         └─ DEC-001 (installation strategy)    [ACCEPTED]

BUG-011 ── TASK-001 (extend pytest trigger)    [DONE]
         └─ DEC-002 (file type coverage)       [ACCEPTED]
```

Both bugs are independent. BUG-010 is resolved.

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   ENABLER PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Bugs:      [####################] 100% (2/2 resolved)            |
| Tasks:     [####################] 100% (2/2 completed)           |
| Decisions: [####################] 100% (2/2 accepted)            |
+------------------------------------------------------------------+
| Overall:   [####################] 100%                            |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Bugs** | 2 |
| **Resolved Bugs** | 2 (BUG-010, BUG-011) |
| **Total Tasks** | 2 |
| **Completed Tasks** | 2 (BUG-010/TASK-001, BUG-011/TASK-001) |
| **Total Decisions** | 2 |
| **Accepted Decisions** | 2 (DEC-001, DEC-002) |
| **Completion %** | 100% |

---

## Acceptance Criteria

### Definition of Done

- [x] ~~Pre-commit hooks auto-install on session start when missing~~ Replaced by DEC-001: warning references `make setup`
- [x] Session hook warning references documented setup mechanism (DEC-001:D-002)
- [x] Pytest hook triggers on markdown file changes (BUG-011)
- [x] Markdown-only commits run architecture tests locally
- [x] All existing tests still pass (2514 passed)
- [x] No regressions in session start hook behavior

---

## Related Items

### Hierarchy

- **Parent:** [FEAT-001: Fix CI Build Failures](../FEAT-001-fix-ci-build-failures.md)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-11 | Claude | pending | Enabler created to group BUG-010 and BUG-011 (pre-commit hook coverage gaps). Root cause of repeated CI failures on markdown-only commits. |
| 2026-02-11 | Claude | in_progress | DEC-001 and DEC-002 created. BUG-010 revised: `make setup` already exists, auto-install rejected, warning improved instead. BUG-010 and TASK-001 marked done. Code changes applied to `session_start_hook.py` and `.pre-commit-config.yaml`. |
| 2026-02-11 | Claude | done | BUG-011 resolved: `types_or: [python, markdown]` applied per DEC-002. All bugs, tasks, and decisions complete. 100% done. |
