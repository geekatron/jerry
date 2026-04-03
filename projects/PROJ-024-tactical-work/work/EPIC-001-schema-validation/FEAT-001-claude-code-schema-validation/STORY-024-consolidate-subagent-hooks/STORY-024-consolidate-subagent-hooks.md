# STORY-024: Consolidate Dual SubagentStop Hooks (GH #178)

> **Type:** story
> **Status:** completed
> **Priority:** medium
> **Impact:** medium
> **Created:** 2026-03-30T00:00:00Z
> **Due:**
> **Completed:** 2026-03-30T12:00:00Z
> **Parent:** FEAT-001
> **Owner:**
> **Effort:** 2
> **GitHub Issue:** [#178](https://github.com/geekatron/jerry/issues/178)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What and why |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Dependencies](#dependencies) | Relationship to other work |
| [History](#history) | Change log |

---

## Summary

SubagentStop hook logic exists in both `scripts/` (standalone) and CLI (`src/`). The standalone script bypasses Clean Architecture and creates a parallel code path that drifts from the CLI. Consolidate to the CLI implementation only.

---

## Architectural Constraints

| Constraint | Rationale |
|------------|-----------|
| **MUST NOT introduce new scripts** | The scripts/ directory is for build tooling only, not runtime hooks. Hook logic belongs in `src/` under Clean Architecture. |
| **Consolidated implementation MUST live in `src/`** | Domain rules in domain layer, hook handling in application/infrastructure layers. The `.claude/hooks/` entry point invokes `uv run jerry ...` CLI commands. |
| **MUST follow Clean Architecture** | SubagentStop enforcement logic follows hexagonal layers: domain (stop rules), application (command handler), infrastructure (hook adapter). |
| **MUST be testable via `tests/`** | Tests go in `tests/` (unit/integration/e2e), not `scripts/tests/`. CLI command is the test boundary. |
| **MUST follow TDD Red/Green/Refactor (H-20)** | Write failing tests for consolidated CLI SubagentStop BEFORE implementation. Red: test exercises CLI command, fails. Green: consolidate implementation, test passes. Refactor: remove duplicate. |

---

## Acceptance Criteria

- [x] Single SubagentStop implementation in `src/` (Clean Architecture)
- [x] `scripts/subagent_stop.py` deleted (if it exists as standalone)
- [x] `.claude/hooks/` entry point invokes via `uv run jerry ...` CLI command
- [x] Hook behavior unchanged (same blocking/warning behavior verified by tests)
- [x] Tests in `tests/` (not `scripts/tests/`) cover the consolidated implementation
- [x] All existing tests pass
- [x] No references to the removed duplicate
- [x] Zero new files in `scripts/`

---

## Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocked By | STORY-023 | Remove deprecated hook first to avoid conflicts |
| Blocks | BUG-005 | Hook infrastructure clean before fixing hook tests |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-30 | adam.nowak | pending | Created from PROJ-024 session. Linked to GH #178. |
| 2026-03-30 | adam.nowak | completed | Commit `e28514a8`. Deleted standalone script, consolidated hooks.json to single CLI path, rewrote 26 SubagentStop tests. GH #178 closed. |
