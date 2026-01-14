# FEATURE-WORKTRACKER: FT-001 Lock File Cleanup

> **Feature ID:** FT-001
> **Solution Epic:** SE-001
> **Project:** PROJ-007-jerry-bugs
> **Status:** IN PROGRESS
> **Created:** 2026-01-14
> **Last Updated:** 2026-01-14

---

## Overview

Address lock file accumulation causing performance degradation. The `AtomicFileAdapter` creates lock files in `.jerry/local/locks/` but never cleans them up.

---

## Enablers

| ID | Name | Status | Tasks |
|----|------|--------|-------|
| [EN-001](./en-001.md) | Investigate lock file accumulation | IN PROGRESS | See en-001.md |

---

## Units of Work

| ID | Title | Status | Tasks | ADR |
|----|-------|--------|-------|-----|
| UoW-001 | Implement Lock File Lifecycle Management | READY | 3 phases | ADR-PROJ007-001 |

### UoW-001: Lock File Lifecycle Management

**Based on:** ADR-PROJ007-001 (Hybrid cleanup approach)

| Task | Description | Status |
|------|-------------|--------|
| T-001 | Implement `_cleanup_lock_file()` in AtomicFileAdapter | PENDING |
| T-002 | Implement `LockFileGarbageCollector` service | PENDING |
| T-003 | Add unit/integration tests for cleanup | PENDING |
| T-004 | Integrate GC with session_start | PENDING |

---

## Bugs

| ID | Description | Status | Enabler |
|----|-------------|--------|---------|
| [BUG-001](./bug-001-lock-file-accumulation.md) | 97 lock files in .jerry/local/locks/ never cleaned | INVESTIGATING | EN-001 |

---

## Technical Debt

| ID | Description | Status |
|----|-------------|--------|
| TD-001 | Lock file cleanup never implemented per ADR-006 | DOCUMENTED |

---

## Evidence

| ID | Type | Source | Relevance |
|----|------|--------|-----------|
| E-001 | Code | `atomic_file_adapter.py:72-76` | Lock file creation without cleanup |
| E-002 | Data | `.jerry/local/locks/` | 97 lock files accumulated |
| E-003 | Doc | `ADR-006` line 195-196 | "Lock file cleanup needed for crashed processes" |

---

## Related Artifacts

| Type | Location | Description |
|------|----------|-------------|
| Solution Tracker | [../SOLUTION-WORKTRACKER.md](../SOLUTION-WORKTRACKER.md) | Parent SE-001 |
| Investigation | [../../../investigations/](../../../investigations/) | ps-investigator report |
| Source Code | `src/infrastructure/adapters/persistence/atomic_file_adapter.py` | Code under investigation |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-14 | FT-001 created | Claude |
| 2026-01-14 | EN-001 investigation started | Claude |
