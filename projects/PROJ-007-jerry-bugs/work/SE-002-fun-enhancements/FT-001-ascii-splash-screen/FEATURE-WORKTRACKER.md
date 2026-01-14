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

*None required - straightforward implementation.*

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
| [UoW-001](./uow-001-implement-ascii-splash.md) | Implement ASCII Splash Screen | PENDING | TBD | - |

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

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-14 | FT-001 created | Claude |
| 2026-01-14 | Initial design considerations documented | Claude |
