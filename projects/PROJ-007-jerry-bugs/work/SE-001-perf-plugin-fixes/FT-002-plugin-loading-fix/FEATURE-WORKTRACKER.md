# FEATURE-WORKTRACKER: FT-002 Plugin Loading Fix

> **Feature ID:** FT-002
> **Solution Epic:** SE-001
> **Project:** PROJ-007-jerry-bugs
> **Status:** PENDING
> **Created:** 2026-01-14
> **Last Updated:** 2026-01-14

---

## Overview

Fix Jerry plugin not loading when started via `claude --plugin-dir`. The plugin should print a message or interact with the user on session start.

---

## Enablers

| ID | Name | Status | Tasks |
|----|------|--------|-------|
| [EN-002](./en-002.md) | Investigate plugin loading failure | PENDING | See en-002.md |

---

## Units of Work

*None yet - to be created after investigation.*

---

## Bugs

| ID | Description | Status | Enabler |
|----|-------------|--------|---------|
| [BUG-002](./bug-002-plugin-not-loading.md) | Plugin not loading/interacting via --plugin-dir | PENDING | EN-002 |

---

## Related Work

| Project | Reference | Description |
|---------|-----------|-------------|
| PROJ-005-plugin-bugs | [WORKTRACKER.md](../../../../PROJ-005-plugin-bugs/WORKTRACKER.md) | Previous plugin fixes |
| PROJ-005 SE-001 | FT-001, FT-002 | Manifest fixes, session_start.py fix |

---

## Evidence

| ID | Type | Source | Relevance |
|----|------|--------|-----------|
| E-001 | Config | `hooks/hooks.json:4-14` | SessionStart hook configuration |
| E-002 | Code | `session_start.py:36-39` | PEP 723 metadata (empty dependencies) |
| E-003 | Code | `session_start.py:50-57` | Imports from src.infrastructure |

---

## Related Artifacts

| Type | Location | Description |
|------|----------|-------------|
| Solution Tracker | [../SOLUTION-WORKTRACKER.md](../SOLUTION-WORKTRACKER.md) | Parent SE-001 |
| Investigation | [../../../investigations/](../../../investigations/) | ps-investigator report |
| Hook Config | `hooks/hooks.json` | Hook configuration |
| Plugin Manifest | `.claude-plugin/plugin.json` | Plugin definition |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-14 | FT-002 created | Claude |
