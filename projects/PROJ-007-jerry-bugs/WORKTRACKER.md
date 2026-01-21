# WORKTRACKER: PROJ-007-jerry-bugs (Global Manifest)

> **Project:** Jerry Performance and Plugin Bugs
> **Status:** IN PROGRESS
> **Created:** 2026-01-14
> **Last Updated:** 2026-01-15

---

## Strategic Themes

| Theme | Description |
|-------|-------------|
| `performance` | Session performance and resource management |
| `plugin-reliability` | Plugin loading and initialization correctness |
| `user-experience` | Fun enhancements and visual improvements |
| `stakeholder-engagement` | Demo, presentations, and executive buy-in |
| `developer-experience` | Developer workflow, CLI tooling, and Claude Code integration |

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
| [SE-004](./work/SE-004-cli-claude-integration/SOLUTION-WORKTRACKER.md) | CLI and Claude Code Integration | IN PROGRESS | 0/1 Features | [SOLUTION-WORKTRACKER.md](./work/SE-004-cli-claude-integration/SOLUTION-WORKTRACKER.md) |

---

## Quick Reference: Work Item Counts

| Level | Total | Completed | In Progress | Pending |
|-------|-------|-----------|-------------|---------|
| Solution Epics | 4 | 0 | 4 | 0 |
| Features | 5 | 1 | 4 | 0 |
| Enablers | 5 | 4 | 1 | 0 |
| Units of Work | 3 | 1 | 1 | 1 |
| Tasks | 55 | 0 | 0 | 55 |
| Technical Debt | 6 | 0 | 0 | 6 |
| Discoveries | 10 | 8 | 0 | 2 |

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
| disc-001 | Requirement Gap | uv portability requirement missed in ADR-PROJ007-002 | RESOLVED ✅ | SE-001/FT-002 |
| disc-002 | Test Gap | CI vs Hook environment discrepancy - CI passes but hook fails | OPEN | SE-001/FT-002 |
| disc-003 | Inconsistency | Hooks use mixed execution (SessionStart=uv, others=python3) | DOCUMENTED | SE-001/FT-002 |
| disc-004 | Functional Gap | cli/main.py missing hook output format, local context, status icons | DOCUMENTED | SE-004/FT-001 |
| disc-005 | Architectural Drift | cli/session_start.py created as shortcut violating hexagonal architecture | DOCUMENTED | SE-004/FT-001 |
| disc-006 | Correction | Hook format correction - `hookSpecificOutput.additionalContext` IS official (supersedes disc-003 in SE-004) | DOCUMENTED ✅ | SE-004/FT-001 |
| disc-007 | Empirical Test | Combined `systemMessage` + `additionalContext` works for SessionStart | CONFIRMED ✅ | SE-004/FT-001 |

---

## Technical Debt Registry

| ID | Type | Description | Status | Feature |
|----|------|-------------|--------|---------|
| TD-001 | Tech Debt | Lock file cleanup never implemented (ADR-006) | DOCUMENTED | SE-001/FT-001 |
| TD-002 | Test Gap | CI tests don't match hook execution environment | DOCUMENTED | SE-001/FT-002 |
| TD-003 | Inconsistency | Hooks use mixed execution (uv vs python3) | DOCUMENTED | SE-001/FT-002 |
| TD-004 | Architecture Violation | cli/session_start.py imports infrastructure directly (violates hexagonal) | DOCUMENTED | SE-004/FT-001 |
| TD-005 | Duplicate Entry Points | pyproject.toml has both `jerry` and `jerry-session-start` | DOCUMENTED | SE-004/FT-001 |
| TD-006 | Missing Functionality | cli/main.py lacks local context support (.jerry/local/context.toml) | DOCUMENTED | SE-004/FT-001 |

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
| 2026-01-15 | SE-004 created: CLI and Claude Code Integration | Claude |
| 2026-01-15 | Added `developer-experience` strategic theme | Claude |
| 2026-01-15 | FT-001 (SE-004) created: Session Hook Architecture Cleanup | Claude |
| 2026-01-15 | EN-001 (SE-004/FT-001) created: Session Start Hook TDD Cleanup (21 tasks) | Claude |
| 2026-01-15 | **RCA COMPLETED**: cli/session_start.py identified as rogue file | Claude |
| 2026-01-15 | TD-004, TD-005, TD-006 documented (SE-004/FT-001 architecture violations) | Claude |
| 2026-01-15 | disc-004, disc-005 documented (SE-004/FT-001 gap analysis & RCA) | Claude |
| 2026-01-15 | EN-001 (SE-004/FT-001) REVISED: 33 tasks across 8 TDD phases | Claude |
| 2026-01-20 | disc-006 created: Hook format correction (supersedes disc-003 in SE-004/FT-001) | Claude |
| 2026-01-20 | EN-001 (SE-004/FT-001) MAJOR REVISION: Corrected per DISC-004, 55 BDD tasks | Claude |
| 2026-01-21 | disc-007 CONFIRMED: Combined systemMessage + additionalContext works (DISC-005) | Claude |
| 2026-01-21 | EN-001 updated with verified combined hook output format | Claude |
