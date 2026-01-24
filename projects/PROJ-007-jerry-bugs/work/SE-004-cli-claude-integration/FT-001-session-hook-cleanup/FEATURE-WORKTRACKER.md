# FEATURE-WORKTRACKER: FT-001 Session Hook Cleanup

> **Feature:** Session Hook Architecture Cleanup
> **Solution Epic:** [SE-004](../../SE-004-cli-claude-integration/SOLUTION-WORKTRACKER.md) CLI and Claude Code Integration
> **Project:** PROJ-007-jerry-bugs
> **Status:** IN PROGRESS
> **Theme:** `developer-experience`
> **Created:** 2026-01-15
> **Last Updated:** 2026-01-15

---

## Overview

**REVISED SCOPE** (based on RCA): Eliminate the rogue `cli/session_start.py` file and properly implement session hook functionality through the main CLI entry point (`cli/main.py`).

### Problem Statement (Revised via RCA)

Root Cause Analysis revealed the true scope:

1. **`cli/session_start.py` shouldn't exist** - It's a rogue entry point that violates hexagonal architecture
2. **`cli/main.py` is missing functionality** - Features in session_start.py need to be migrated to main.py
3. **`session_start_hook.py` should call `cli/main.py`** - Not a separate entry point

**Original Issue**: A previous Claude Code session created `cli/session_start.py` as a shortcut instead of properly extending `cli/main.py` and `CLIAdapter`. This introduced:
- Direct infrastructure imports in interface layer (violates hexagonal)
- Duplicate CLI entry points (`jerry` and `jerry-session-start`)
- Duplicate JSON formatting responsibility

### Target Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Claude Code Hook System                       │
└───────────────────────────────────┬─────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│              scripts/session_start_hook.py                       │
│  - Bootstraps uv environment                                     │
│  - Error handling and logging                                    │
│  - Calls: uv run jerry projects context --format hook            │
│  - Wraps errors in JSON (output_json, output_error)              │
└───────────────────────────────────┬─────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                   src/interface/cli/main.py                      │
│  - Single entry point for all CLI commands                       │
│  - Routes to CLIAdapter                                          │
└───────────────────────────────────┬─────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                   src/interface/cli/adapter.py                   │
│  CLIAdapter.cmd_projects_context(format="hook")                  │
│  - Dispatches RetrieveProjectContextQuery                        │
│  - Formats output based on --format flag                         │
│  - Hook format: JSON with XML-like tags in additionalContext     │
└───────────────────────────────────┬─────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Application Layer                           │
│  RetrieveProjectContextQuery (with local context precedence)     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Enablers

| ID | Name | Status | Progress | Tracker |
|----|------|--------|----------|---------|
| [EN-001](./en-001-session-hook-tdd.md) | Session Start Hook TDD Cleanup | IN PROGRESS | 0/33 Tasks | [en-001](./en-001-session-hook-tdd.md) |

---

## Units of Work

| ID | Name | Status | Progress | Tracker |
|----|------|--------|----------|---------|
| *None yet* | - | - | - | - |

---

## Technical Debt

| ID | Title | Severity | Status | Tracker |
|----|-------|----------|--------|---------|
| [TD-001](./td-001-session-start-violates-hexagonal.md) | cli/session_start.py Violates Hexagonal Architecture | HIGH | DOCUMENTED | [td-001](./td-001-session-start-violates-hexagonal.md) |
| [TD-002](./td-002-duplicate-entry-points.md) | Duplicate CLI Entry Points | MEDIUM | DOCUMENTED | [td-002](./td-002-duplicate-entry-points.md) |
| [TD-003](./td-003-missing-local-context-support.md) | cli/main.py Missing Local Context Support | MEDIUM | DOCUMENTED | [td-003](./td-003-missing-local-context-support.md) |

---

## Discoveries

| ID | Title | Status | Tracker |
|----|-------|--------|---------|
| [DISC-001](./disc-001-functional-gap-analysis.md) | Functional Gap Between cli/main.py and cli/session_start.py | DOCUMENTED | [disc-001](./disc-001-functional-gap-analysis.md) |
| [DISC-002](./disc-002-architectural-drift-rca.md) | Architectural Drift Root Cause Analysis | DOCUMENTED | [disc-002](./disc-002-architectural-drift-rca.md) |

---

## Quick Reference: Work Item Counts

| Level | Total | Completed | In Progress | Pending |
|-------|-------|-----------|-------------|---------|
| Enablers | 1 | 0 | 1 | 0 |
| Units of Work | 0 | 0 | 0 | 0 |
| Tasks | 33 | 0 | 0 | 33 |
| Technical Debt | 3 | 0 | 0 | 3 |
| Discoveries | 2 | 2 | 0 | 0 |

---

## Related Artifacts

| Type | Location | Description |
|------|----------|-------------|
| Solution Epic | [../SOLUTION-WORKTRACKER.md](../SOLUTION-WORKTRACKER.md) | SE-004 CLI and Claude Code Integration |
| Hook Wrapper | `scripts/session_start_hook.py` | Current hook wrapper (calls rogue CLI) |
| Rogue CLI | `src/interface/cli/session_start.py` | **TO BE DELETED** - violates architecture |
| Main CLI | `src/interface/cli/main.py` | Proper CLI entry point |
| CLI Adapter | `src/interface/cli/adapter.py` | CLIAdapter (needs hook format support) |
| E2E Tests | `tests/session_management/e2e/test_session_start.py` | Existing E2E tests |
| Contract Tests | `tests/session_management/contract/test_hook_contract.py` | Existing contract tests |
| pyproject.toml | `pyproject.toml` | Has duplicate entry points |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-15 | Feature created | Claude |
| 2026-01-15 | EN-001 created: Session Start Hook TDD Cleanup | Claude |
| 2026-01-15 | **SCOPE REVISED**: RCA revealed cli/session_start.py is rogue file | Claude |
| 2026-01-15 | TD-001, TD-002, TD-003 documented (architecture violations) | Claude |
| 2026-01-15 | DISC-001, DISC-002 documented (gap analysis & RCA) | Claude |
| 2026-01-15 | EN-001 updated: 33 tasks across 8 phases | Claude |
