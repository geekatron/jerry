# WORKTRACKER: PROJ-007-jerry-bugs (Global Manifest)

> **Project:** Jerry Performance and Plugin Bugs
> **Status:** IN PROGRESS
> **Created:** 2026-01-14
> **Last Updated:** 2026-01-14

---

## Strategic Themes

| Theme | Description |
|-------|-------------|
| `performance` | Session performance and resource management |
| `plugin-reliability` | Plugin loading and initialization correctness |

---

## Initiatives

*None - PROJ-007 is a focused bug-fix project, not a multi-team initiative.*

---

## Solution Epics

| ID | Name | Status | Progress | Tracker |
|----|------|--------|----------|---------|
| [SE-001](./work/SE-001-perf-plugin-fixes/SOLUTION-WORKTRACKER.md) | Performance and Plugin Bug Fixes | IN PROGRESS | 0/2 Features | [SOLUTION-WORKTRACKER.md](./work/SE-001-perf-plugin-fixes/SOLUTION-WORKTRACKER.md) |

---

## Quick Reference: Work Item Counts

| Level | Total | Completed | In Progress | Pending |
|-------|-------|-----------|-------------|---------|
| Solution Epics | 1 | 0 | 1 | 0 |
| Features | 2 | 0 | 0 | 2 |
| Enablers | 2 | 0 | 1 | 1 |
| Units of Work | 0 | 0 | 0 | 0 |
| Tasks | 0 | 0 | 0 | 0 |

---

## Bugs Registry

| ID | Type | Description | Status | Feature | Enabler |
|----|------|-------------|--------|---------|---------|
| BUG-001 | Bug | Lock files accumulating without cleanup | INVESTIGATING | FT-001 | EN-001 |
| BUG-002 | Bug | Jerry plugin not loading/interacting | PENDING | FT-002 | EN-002 |

---

## Discoveries Registry

| ID | Type | Description | Status | Feature |
|----|------|-------------|--------|---------|
| *(none yet)* | - | - | - | - |

---

## Technical Debt Registry

| ID | Type | Description | Status | Feature |
|----|------|-------------|--------|---------|
| TD-001 | Tech Debt | Lock file cleanup never implemented (ADR-006) | DOCUMENTED | FT-001 |

---

## Related Artifacts

| Type | Location | Description |
|------|----------|-------------|
| Project Plan | [PLAN.md](./PLAN.md) | High-level project plan |
| Investigations | [investigations/](./investigations/) | ps-investigator reports |
| PROJ-005 Reference | [../PROJ-005-plugin-bugs/](../PROJ-005-plugin-bugs/) | Previous plugin bug fixes |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-14 | Project created for performance and plugin bugs | Claude |
| 2026-01-14 | Initial investigation started for BUG-001 (lock files) | Claude |
