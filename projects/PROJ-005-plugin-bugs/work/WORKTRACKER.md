# WORKTRACKER: PROJ-005-plugin-bugs (Global Manifest)

> **Project:** Plugin Installation & Runtime Bugs
> **Status:** IN PROGRESS
> **Created:** 2026-01-13
> **Last Updated:** 2026-01-13

---

## Strategic Themes

| Theme | Description |
|-------|-------------|
| `plugin-quality` | Plugin installation reliability and runtime correctness |
| `developer-experience` | Smooth plugin development and testing workflow |

---

## Initiatives

*None - PROJ-005 is a focused bug-fix project, not a multi-team initiative.*

---

## Solution Epics

| ID | Name | Status | Progress | Tracker |
|----|------|--------|----------|---------|
| [SE-001](./SE-001/SOLUTION-WORKTRACKER.md) | Plugin Installation & Runtime Fixes | IN PROGRESS | 2/3 Features | [SOLUTION-WORKTRACKER.md](./SE-001/SOLUTION-WORKTRACKER.md) |

---

## Quick Reference: Work Item Counts

| Level | Total | Completed | In Progress | Pending |
|-------|-------|-----------|-------------|---------|
| Solution Epics | 1 | 0 | 1 | 0 |
| Features | 2 | 1 | 1 | 0 |
| Enablers | 3 | 2 | 1 | 0 |
| Tasks | 19 | 16 | 3 | 0 |

---

## Bugs & Discoveries Registry

| ID | Type | Description | Status | Feature | Enabler |
|----|------|-------------|--------|---------|---------|
| BUG-001 | Bug | plugin.json had 6 unrecognized fields | FIXED | FT-001 | EN-001 |
| BUG-002 | Bug | plugin.json paths missing ./ prefix | FIXED | FT-001 | EN-001 |
| BUG-003 | Bug | plugin.json skills used file paths | FIXED | FT-001 | EN-001 |
| BUG-004 | Bug | marketplace.json invalid 'skills' field | FIXED | FT-001 | EN-002 |
| BUG-005 | Bug | marketplace.json invalid 'strict' field | FIXED | FT-001 | EN-002 |
| BUG-006 | Bug | marketplace.json email typo | FIXED | FT-001 | EN-002 |
| **BUG-007** | **Bug** | **session_start.py requires pip** | **OPEN** | **FT-002** | **EN-003** |
| DISC-001 | Discovery | skills field needs directory format | NOTED | FT-001 | EN-001 |
| DISC-002 | Discovery | marketplace vs plugin.json schema differs | NOTED | FT-001 | EN-002 |
| DISC-003 | Discovery | Other hook scripts are standalone | NOTED | FT-002 | EN-003 |
| DISC-004 | Discovery | ps-* artifact naming violation | OPEN | FT-002 | EN-003 |

---

## Related Artifacts

| Type | Location | Description |
|------|----------|-------------|
| Project Plan | [../PLAN.md](../PLAN.md) | High-level project plan |
| Bug Tracking | [./PHASE-BUGS.md](./PHASE-BUGS.md) | Detailed bug reports |
| Re-Analysis Plan | [./PHASE-06-REANALYSIS-PLAN.md](./PHASE-06-REANALYSIS-PLAN.md) | Orchestration plan |
| Research | [../research/](../research/) | Research artifacts (e-007, e-008) |
| Analysis | [../analysis/](../analysis/) | Trade-off and validation reports |
| Decisions | [../decisions/](../decisions/) | ADRs |
| Investigations | [../investigations/](../investigations/) | Functional requirements |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-13 | Restructured to ontology-based hierarchy | Claude |
| 2026-01-13 | Created SE-001, FT-001, FT-002, EN-001 to EN-003 | Claude |
| 2026-01-13 | Migrated from flat WORKTRACKER.md | Claude |
