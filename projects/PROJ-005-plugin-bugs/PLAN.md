# PROJ-005: Plugin Installation Bugs

> **Project ID:** PROJ-005-plugin-bugs
> **Status:** VERIFICATION PENDING
> **Branch:** cc/jerry-plugin-bugs
> **Created:** 2026-01-13
> **Last Updated:** 2026-01-13

---

## Overview

This project addressed critical bugs preventing the Jerry Framework plugin from functioning correctly after installation via the local marketplace strategy in Claude Code.

### Problems Solved

| Problem | Status | Solution |
|---------|--------|----------|
| Plugin installation fails with validation errors | FIXED | Fixed plugin.json and marketplace.json |
| SessionStart hook fails silently | FIXED | Implemented uv run with PYTHONPATH |

---

## Work Hierarchy

This project follows the SAFe-aligned worktracker ontology:

```
WORKTRACKER.md (Global Manifest)
└── SE-001: Plugin Installation & Runtime Fixes
    ├── FT-001: Manifest Validation Fixes [COMPLETED]
    │   ├── EN-001: Fix plugin.json [COMPLETED]
    │   └── EN-002: Fix marketplace.json [COMPLETED]
    └── FT-002: SessionStart Hook Fix [VERIFICATION PENDING]
        └── EN-003: Fix session_start.py pip dependency [COMPLETED]
```

### Work Items Summary

| ID | Type | Name | Status |
|----|------|------|--------|
| SE-001 | Solution Epic | Plugin Installation & Runtime Fixes | VERIFICATION PENDING |
| FT-001 | Feature | Manifest Validation Fixes | COMPLETED |
| FT-002 | Feature | SessionStart Hook Fix | VERIFICATION PENDING |
| EN-001 | Enabler | Fix plugin.json validation errors | COMPLETED |
| EN-002 | Enabler | Fix marketplace.json validation errors | COMPLETED |
| EN-003 | Enabler | Fix session_start.py pip dependency | COMPLETED |

---

## Bugs Fixed

| ID | Description | Feature | Enabler |
|----|-------------|---------|---------|
| BUG-001 | plugin.json had 6 unrecognized fields | FT-001 | EN-001 |
| BUG-002 | plugin.json paths missing ./ prefix | FT-001 | EN-001 |
| BUG-003 | plugin.json skills used file paths | FT-001 | EN-001 |
| BUG-004 | marketplace.json invalid 'skills' field | FT-001 | EN-002 |
| BUG-005 | marketplace.json invalid 'strict' field | FT-001 | EN-002 |
| BUG-006 | marketplace.json email typo | FT-001 | EN-002 |
| BUG-007 | session_start.py requires pip | FT-002 | EN-003 |

---

## Key Decisions

| ADR | Decision | Status |
|-----|----------|--------|
| [e-010](./decisions/PROJ-005-e-010-adr-uv-session-start.md) | Use uv run with PYTHONPATH for SessionStart hook | ACCEPTED |

---

## Research Artifacts

| Entry | Type | Description |
|-------|------|-------------|
| [e-006](./investigations/PROJ-005-e-006-functional-requirements.md) | Investigation | Functional Requirements (12 FRs) |
| [e-007](./research/PROJ-005-e-007-plugin-patterns.md) | Research | Plugin Patterns (10 patterns) |
| [e-008](./research/PROJ-005-e-008-uv-dependency-management.md) | Research | uv + PEP 723 Dependency Management |
| [e-009](./analysis/PROJ-005-e-009-tradeoffs.md) | Analysis | Trade-off Analysis (Option A: 44/50) |
| [e-010](./decisions/PROJ-005-e-010-adr-uv-session-start.md) | Decision | ADR: uv Session Start |
| [e-011](./analysis/PROJ-005-e-011-validation.md) | Validation | Validation Report (GO, 92%) |

---

## Verification Remaining

Before marking project as COMPLETE:

- [ ] End-to-end test: Fresh clone + plugin install + session start
- [ ] Contract tests pass (13 tests)
- [ ] Documentation updated (INSTALLATION.md)

---

## Files Modified

| File | Change |
|------|--------|
| `.claude-plugin/plugin.json` | Removed invalid fields, fixed paths |
| `.claude-plugin/marketplace.json` | Removed invalid fields, fixed typo |
| `hooks/hooks.json` | Updated SessionStart to use uv run |
| `src/interface/cli/session_start.py` | Added PEP 723 metadata |
| `scripts/session_start.py` | DELETED (legacy wrapper) |
| `docs/INSTALLATION.md` | Added uv requirement |

---

## Related Links

| Document | Location |
|----------|----------|
| Work Tracker | [WORKTRACKER.md](./WORKTRACKER.md) |
| Solution Epic | [work/SE-001/SOLUTION-WORKTRACKER.md](./work/SE-001/SOLUTION-WORKTRACKER.md) |
| Archive | [work/archive/](./work/archive/) |
