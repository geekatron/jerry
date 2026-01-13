# FEATURE-WORKTRACKER: FT-002 SessionStart Hook Fix

> **Feature ID:** FT-002
> **Name:** SessionStart Hook Fix
> **Status:** VERIFICATION PENDING
> **Parent:** [SE-001](../SOLUTION-WORKTRACKER.md)
> **Created:** 2026-01-13
> **Last Updated:** 2026-01-13

---

## Overview

This feature addresses BUG-007 where the SessionStart hook fails silently in plugin mode because `scripts/session_start.py` delegates to modules requiring `pip install -e .`.

### Problem Statement

After successful plugin installation, the SessionStart hook fails silently:
- **Symptom:** No Jerry Framework startup message appears
- **Root Cause:** `scripts/session_start.py` is a "legacy wrapper" that delegates to `src/interface/cli/session_start.py`, which imports from infrastructure layer requiring pip installation

### Approved Solution (ADR e-010)

**Option A: uv run in hooks.json**
- Change hook command to: `uv run ${CLAUDE_PLUGIN_ROOT}/src/interface/cli/session_start.py`
- Add PEP 723 inline metadata to session_start.py
- Delete `scripts/session_start.py` (legacy wrapper)
- Validation: GO (92% confidence)

### Success Criteria

- [ ] `scripts/session_start.py` deleted (use src/ directly)
- [ ] SessionStart hook produces valid output for all 3 tag types
- [ ] Project context detection works via JERRY_PROJECT env var
- [ ] No import errors when executed standalone
- [ ] Exit code is always 0
- [ ] Works on fresh clone without pip install

---

## Enablers

| ID | Name | Status | Bugs | Tasks |
|----|------|--------|------|-------|
| [EN-003](./en-003.md) | Fix session_start.py pip dependency | COMPLETED | BUG-007 | 7/7 |

---

## Units of Work

*None - This feature consists only of technical enablers (bug fixes).*

---

## Research Artifacts

| Entry ID | Type | Description | Location |
|----------|------|-------------|----------|
| e-006 | Investigation | Functional Requirements (12 FRs) | [../../investigations/PROJ-005-e-006-functional-requirements.md](../../investigations/PROJ-005-e-006-functional-requirements.md) |
| e-007 | Research | Plugin Patterns (10 patterns) | [../../research/PROJ-005-e-007-plugin-patterns.md](../../research/PROJ-005-e-007-plugin-patterns.md) |
| e-008 | Research | uv + PEP 723 Dependency Management | [../../research/PROJ-005-e-008-uv-dependency-management.md](../../research/PROJ-005-e-008-uv-dependency-management.md) |
| e-009 | Analysis | Trade-off Analysis (Option A: 44/50) | [../../analysis/PROJ-005-e-009-tradeoffs.md](../../analysis/PROJ-005-e-009-tradeoffs.md) |
| e-010 | Decision | ADR: uv Session Start (Accepted) | [../../decisions/PROJ-005-e-010-adr-uv-session-start.md](../../decisions/PROJ-005-e-010-adr-uv-session-start.md) |
| e-011 | Validation | Validation Report (GO, 92%) | [../../analysis/PROJ-005-e-011-validation.md](../../analysis/PROJ-005-e-011-validation.md) |

---

## Discoveries

| ID | Description | Status |
|----|-------------|--------|
| DISC-003 | pre_tool_use.py, subagent_stop.py, post_tool_use.py are properly standalone | NOTED |
| DISC-004 | ps-* artifact naming convention violated (e-006 vs e-001) | OPEN |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-13 | Created feature tracker | Claude |
| 2026-01-13 | Linked research artifacts e-006 through e-011 | Claude |
| 2026-01-13 | ADR approved - ready for implementation | Claude |
