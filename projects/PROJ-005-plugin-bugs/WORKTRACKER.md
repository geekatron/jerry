# WORKTRACKER: PROJ-005-plugin-bugs (Global Manifest)

> **Project:** Plugin Installation & Runtime Bugs
> **Status:** IN PROGRESS (SE-002 active)
> **Created:** 2026-01-13
> **Last Updated:** 2026-01-13
> **SE-001 Completed:** 2026-01-13

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
| [SE-001](./work/SE-001/SOLUTION-WORKTRACKER.md) | Plugin Installation & Runtime Fixes | COMPLETED | 2/2 Features | [SOLUTION-WORKTRACKER.md](./work/SE-001/SOLUTION-WORKTRACKER.md) |
| [SE-002](./work/SE-002/SOLUTION-WORKTRACKER.md) | Plugin Quality Assurance & Regression Prevention | IN PROGRESS | 0/1 Features | [SOLUTION-WORKTRACKER.md](./work/SE-002/SOLUTION-WORKTRACKER.md) |

---

## Quick Reference: Work Item Counts

| Level | Total | Completed | In Progress | Pending |
|-------|-------|-----------|-------------|---------|
| Solution Epics | 2 | 1 | 1 | 0 |
| Features | 3 | 2 | 1 | 0 |
| Enablers | 6 | 3 | 0 | 3 |
| Units of Work | 1 | 0 | 0 | 1 |
| Tasks | 19 + 36 | 19 | 0 | 36 |

---

## Bugs & Discoveries Registry

| ID | Type | Description | Status | Feature | Enabler |
|----|------|-------------|--------|---------|---------|
| [BUG-001](./work/SE-001/FT-001/en-001.md) | Bug | plugin.json had 6 unrecognized fields | FIXED | FT-001 | EN-001 |
| [BUG-002](./work/SE-001/FT-001/en-001.md) | Bug | plugin.json paths missing ./ prefix | FIXED | FT-001 | EN-001 |
| [BUG-003](./work/SE-001/FT-001/en-001.md) | Bug | plugin.json skills used file paths | FIXED | FT-001 | EN-001 |
| [BUG-004](./work/SE-001/FT-001/en-002.md) | Bug | marketplace.json invalid 'skills' field | FIXED | FT-001 | EN-002 |
| [BUG-005](./work/SE-001/FT-001/en-002.md) | Bug | marketplace.json invalid 'strict' field | FIXED | FT-001 | EN-002 |
| [BUG-006](./work/SE-001/FT-001/en-002.md) | Bug | marketplace.json email typo | FIXED | FT-001 | EN-002 |
| [BUG-007](./work/SE-001/FT-002/bug-007.md) | Bug | session_start.py requires pip | FIXED | FT-002 | EN-003 |
| [DISC-001](./work/SE-001/FT-001/en-001.md) | Discovery | skills field needs directory format | NOTED | FT-001 | EN-001 |
| [DISC-002](./work/SE-001/FT-001/en-002.md) | Discovery | marketplace vs plugin.json schema differs | NOTED | FT-001 | EN-002 |
| [DISC-003](./work/SE-001/FT-002/en-003.md) | Discovery | Other hook scripts are standalone | NOTED | FT-002 | EN-003 |
| DISC-004 | Discovery | ps-* artifact naming violation | DOCUMENTED | FT-002 | - |
| [DISC-005](./work/SE-001/FT-002/disc-005.md) | Discovery | PYTHONPATH required for uv run | RESOLVED | FT-002 | EN-003 |
| [DISC-006](./work/SE-002/FT-003/disc-006.md) | Discovery | Duplicate tests/ folders (root vs scripts/) | DOCUMENTED | FT-003 | - |
| [DISC-007](./work/SE-002/FT-003/disc-007.md) | Discovery | Existing session_start.py tests broken | REQUIRES ACTION | FT-003 | EN-004 |
| [DISC-008](./work/SE-002/FT-003/disc-008.md) | Discovery | Test execution must use uv, not python3 | REQUIRES ACTION | FT-003 | EN-005 |

---

## Related Artifacts

| Type | Location | Description |
|------|----------|-------------|
| Project Plan | [PLAN.md](./PLAN.md) | High-level project plan |
| Research | [research/](./research/) | Research artifacts (e-007, e-008) |
| Analysis | [analysis/](./analysis/) | Trade-off and validation reports (e-009, e-011) |
| Decisions | [decisions/](./decisions/) | ADRs (e-010) |
| Investigations | [investigations/](./investigations/) | Functional requirements (e-006) |
| Archive | [work/archive/](./work/archive/) | Superseded documents |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-13 | Restructured to ontology-based hierarchy | Claude |
| 2026-01-13 | Created SE-001, FT-001, FT-002, EN-001 to EN-003 | Claude |
| 2026-01-13 | Migrated from flat WORKTRACKER.md | Claude |
| 2026-01-13 | BUG-007 FIXED, DISC-005 added, EN-003 completed | Claude |
| 2026-01-13 | Relocated WORKTRACKER.md to project root per ontology | Claude |
| 2026-01-13 | **SE-001 COMPLETED** - User verified SessionStart hook working | Claude |
| 2026-01-13 | Created SE-002: Plugin Quality Assurance & Regression Prevention | Claude |
| 2026-01-13 | Created FT-003: SessionStart & CLI Integration Testing | Claude |
| 2026-01-13 | Created EN-004, EN-005, EN-006, WI-001 (Tech Debt prevention) | Claude |
