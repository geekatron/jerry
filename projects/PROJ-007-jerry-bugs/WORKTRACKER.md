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
| `user-experience` | Fun enhancements and visual improvements |
| `stakeholder-engagement` | Demo, presentations, and executive buy-in |

---

## Initiatives

*None - PROJ-007 is a focused bug-fix project, not a multi-team initiative.*

---

## Solution Epics

| ID | Name | Status | Progress | Tracker |
|----|------|--------|----------|---------|
| [SE-001](./work/SE-001-perf-plugin-fixes/SOLUTION-WORKTRACKER.md) | Performance and Plugin Bug Fixes | IN PROGRESS | 1/2 Features | [SOLUTION-WORKTRACKER.md](./work/SE-001-perf-plugin-fixes/SOLUTION-WORKTRACKER.md) |
| [SE-002](./work/SE-002-fun-enhancements/SOLUTION-WORKTRACKER.md) | Fun Enhancements | IN PROGRESS | 0/1 Features | [SOLUTION-WORKTRACKER.md](./work/SE-002-fun-enhancements/SOLUTION-WORKTRACKER.md) |
| [SE-003](./work/SE-003-demo-stakeholder-engagement/SOLUTION-WORKTRACKER.md) | Demo and Stakeholder Engagement | IN PROGRESS | 0/1 Features | [SOLUTION-WORKTRACKER.md](./work/SE-003-demo-stakeholder-engagement/SOLUTION-WORKTRACKER.md) |

---

## Quick Reference: Work Item Counts

| Level | Total | Completed | In Progress | Pending |
|-------|-------|-----------|-------------|---------|
| Solution Epics | 3 | 0 | 3 | 0 |
| Features | 4 | 1 | 3 | 0 |
| Enablers | 4 | 4 | 0 | 0 |
| Units of Work | 3 | 1 | 1 | 1 |
| Tasks | 37 | 12 | 0 | 25 |
| Technical Debt | 3 | 0 | 0 | 3 |
| Discoveries | 6 | 4 | 0 | 2 |

---

## Bugs Registry

| ID | Type | Description | Status | Feature | Enabler |
|----|------|-------------|--------|---------|---------|
| BUG-001 | Bug | Lock files accumulating without cleanup | INVESTIGATING | FT-001 | EN-001 |
| BUG-002 | Bug | Jerry plugin not loading/interacting | **RESOLVED** ✅ | FT-002 | EN-002 |

---

## Discoveries Registry

| ID | Type | Description | Status | Feature |
|----|------|-------------|--------|---------|
| disc-001 | Requirement Gap | uv portability requirement missed in ADR-PROJ007-002 | RESOLVED ✅ | FT-002 |
| disc-002 | Test Gap | CI vs Hook environment discrepancy - CI passes but hook fails | OPEN | FT-002 |
| disc-003 | Inconsistency | Hooks use mixed execution (SessionStart=uv, others=python3) | DOCUMENTED | FT-002 |

---

## Technical Debt Registry

| ID | Type | Description | Status | Feature |
|----|------|-------------|--------|---------|
| TD-001 | Tech Debt | Lock file cleanup never implemented (ADR-006) | DOCUMENTED | FT-001 |
| TD-002 | Test Gap | CI tests don't match hook execution environment | DOCUMENTED | FT-002 |
| TD-003 | Inconsistency | Hooks use mixed execution (uv vs python3) | DOCUMENTED | FT-002 |

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
| 2026-01-14 | disc-001 created: uv portability requirement gap | Claude |
| 2026-01-14 | disc-002 identified: CI vs Hook environment discrepancy | Claude |
| 2026-01-14 | disc-003 documented: Hooks use inconsistent execution methods | Claude |
| 2026-01-14 | TD-002 created: CI test coverage gap | Claude |
| 2026-01-14 | TD-003 created: Hooks execution inconsistency | Claude |
| 2026-01-14 | EN-003 created: Validate solution hypothesis | Claude |
| 2026-01-14 | UoW-001 detailed: 12 TDD/BDD tasks for plugin fix | Claude |
| 2026-01-14 | FT-002 MERGED: Plugin loading fix v0.2.0 (PR #13) | Claude |
| 2026-01-14 | BUG-002 RESOLVED via FT-002 | Claude |
| 2026-01-14 | SE-002 created: Fun Enhancements | Claude |
| 2026-01-14 | FT-001 (SE-002) created: ASCII Splash Screen | Claude |
| 2026-01-14 | jerry-persona-20260114 orchestration COMPLETE (7/7 agents) | Claude |
| 2026-01-14 | SE-003 created: Demo and Stakeholder Engagement | Claude |
| 2026-01-14 | FT-001 (SE-003) created: CPO Demo and Stakeholder Presentation | Claude |
| 2026-01-14 | UoW-001 (SE-003/FT-001) created: Demo Planning and Execution | Claude |
