# FEATURE-WORKTRACKER: FT-001 ASCII Splash Screen

> **Feature ID:** FT-001
> **Solution Epic:** SE-002
> **Project:** PROJ-007-jerry-bugs
> **Status:** IN PROGRESS
> **Target Version:** v0.3.0
> **Created:** 2026-01-14
> **Last Updated:** 2026-01-14

---

## Overview

Add a visually appealing ASCII art splash screen when Jerry initializes via the session start hook. The splash should convey Jerry's personality - helpful, wise, and a bit playful.

**Goal:** Make Jerry's startup memorable and delightful while maintaining professionalism.

---

## Acceptance Criteria

| ID | Criteria | Status |
|----|----------|--------|
| AC-001 | ASCII art displays on session start | PENDING |
| AC-002 | Art is visible in standard terminal (80+ cols) | PENDING |
| AC-003 | Art includes "Jerry" branding | PENDING |
| AC-004 | Art does not break existing hook output format | PENDING |
| AC-005 | Art can be disabled via environment variable | PENDING |

---

## Enablers

| ID | Name | Status | Tasks | Orchestration |
|----|------|--------|-------|---------------|
| [EN-001](./en-001-research-jerry-of-the-day.md) | Research Spike - Jerry of the Day | IN PROGRESS | 3 | ps-researcher |
| [EN-002](./en-002-research-shane-mcconkey.md) | Research Spike - Shane McConkey | PENDING | 4 | nse-explorer |

### EN-001: Jerry of the Day Research
Research the skiing/snowboarding "Jerry" culture phenomenon. Extract insights for creating Jerry Framework's personality - the framework helps prevent "Jerry of the Day" moments caused by context rot.

### EN-002: Shane McConkey Research
Research Shane McConkey and his "Saucer Boy" persona. Shane embodies the "wise fool" archetype - appearing foolish while being brilliant. Perfect inspiration for Jerry Framework's voice. Note: Our bot account `saucer-boy` is named after Shane's alter ego.

---

## Technical Debt

*None documented yet.*

---

## Discoveries

*None documented yet.*

---

## Units of Work

| ID | Title | Status | Tasks | Blocked By |
|----|-------|--------|-------|------------|
| [UoW-001](./uow-001-implement-ascii-splash.md) | Implement ASCII Splash Screen | PENDING | TBD | EN-001, EN-002 |

---

## Orchestration

This feature uses a cross-pollinated pipeline for research:

| Workflow ID | Pattern | Status |
|-------------|---------|--------|
| `jerry-persona-20260114` | Cross-Pollinated Pipeline | IN PROGRESS |

**Pipelines:**
- **Pipeline A (ps)**: Problem-Solving - Jerry of the Day research and synthesis
- **Pipeline B (nse)**: NASA SE - Shane McConkey exploration and architecture

**Artifacts:** `orchestration/jerry-persona-20260114/`

See: [ORCHESTRATION_PLAN.md](../../../orchestration/jerry-persona-20260114/ORCHESTRATION_PLAN.md)

---

## Design Considerations

### Placement Options

1. **Before hook output** - Art displays first, then `<project-context>` tags
2. **Integrated with output** - Art is part of the initialization message
3. **Separate command** - `jerry splash` command for on-demand display

### Art Style Ideas

```
   ___
  |_  |
    | | ___  _ __ _ __ _   _
    | |/ _ \| '__| '__| | | |
/\__/ / (_) | |  | |  | |_| |
\____/ \___/|_|  |_|   \__, |
                        __/ |
                       |___/
```

Or a more elaborate design with a mascot/icon.

### Environment Variable

```bash
JERRY_SPLASH=0  # Disable splash screen
JERRY_SPLASH=1  # Enable splash screen (default)
```

---

## Evidence

*To be collected during implementation.*

---

## Related Artifacts

| Type | Location | Description |
|------|----------|-------------|
| Solution Tracker | [../SOLUTION-WORKTRACKER.md](../SOLUTION-WORKTRACKER.md) | Parent SE-002 |
| Session Start | `src/interface/cli/session_start.py` | Target file for splash |
| Hook Config | `hooks/hooks.json` | Hook configuration |
| Orchestration Plan | `orchestration/jerry-persona-20260114/ORCHESTRATION_PLAN.md` | Workflow plan |
| Orchestration State | `orchestration/jerry-persona-20260114/ORCHESTRATION.yaml` | SSOT |
| Bot Account | GitHub `saucer-boy` | Named after Shane's alter ego |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-14 | FT-001 created | Claude |
| 2026-01-14 | Initial design considerations documented | Claude |
| 2026-01-14 | EN-001 created: Jerry of the Day research spike | Claude |
| 2026-01-14 | EN-002 created: Shane McConkey research spike | Claude |
| 2026-01-14 | Orchestration workflow jerry-persona-20260114 initiated | Claude |
| 2026-01-14 | UoW-001 blocked by enablers until research complete | Claude |
