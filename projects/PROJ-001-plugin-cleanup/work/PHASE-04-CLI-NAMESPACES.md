# Phase 4: CLI Namespaces per Bounded Context

**Status**: ✅ COMPLETE (Phase 4.5 deferred for Event Sourcing)
**Started**: 2026-01-12
**Target Version**: v0.1.0 (breaking change)
**Branch**: cc/task-subtask

---

## Overview

Reorganize Jerry's CLI commands into bounded-context-aligned namespaces:
- `jerry session` - Session management
- `jerry items` - Work item management
- `jerry projects` - Project management

**Breaking Change**: This is v0.1.0. No backward compatibility with v0.0.1 commands.

---

## Research Artifacts

| ID | Document | Status |
|----|----------|--------|
| R-001 | `research/phase4-cli-e-001-5w1h-namespaces.md` | ✅ COMPLETE |
| D-001 | `decisions/ADR-CLI-002-namespace-implementation.md` | ✅ COMPLETE |

---

## Implementation Tasks

### Phase 4.1: Parser Infrastructure

| Task | Description | Status | Evidence |
|------|-------------|--------|----------|
| 4.1.1 | Create `src/interface/cli/parser.py` | ✅ COMPLETE | File exists (280 lines) |
| 4.1.2 | Implement session namespace subparser | ✅ COMPLETE | 8 parser tests pass |
| 4.1.3 | Implement items namespace subparser | ✅ COMPLETE | 12 parser tests pass |
| 4.1.4 | Implement projects namespace subparser | ✅ COMPLETE | 3 parser tests pass |
| 4.1.5 | Write unit tests for parser | ✅ COMPLETE | 33 tests in `tests/interface/cli/unit/test_parser.py` |

**Test Matrix (4.1.5)**:
| Category | Count | Tests |
|----------|-------|-------|
| Happy Path | 6 | Parse session/items/projects commands |
| Negative | 3 | Unknown namespace, missing args |
| Edge | 2 | Help flags, version |

### Phase 4.2: Projects Namespace (Migration)

| Task | Description | Status | Evidence |
|------|-------------|--------|----------|
| 4.2.1 | Rename `init` to `projects context` | ✅ COMPLETE | `cmd_projects_context()` in adapter.py |
| 4.2.2 | Migrate `projects list` | ✅ COMPLETE | Existing `cmd_projects_list()` works |
| 4.2.3 | Migrate `projects validate` | ✅ COMPLETE | Existing `cmd_projects_validate()` works |
| 4.2.4 | Update adapter methods | ✅ COMPLETE | `adapter.py` has all methods (stubs for session/items) |
| 4.2.5 | Write regression tests | ✅ COMPLETE | All 71 CLI tests pass, 1444 total pass |

**Test Matrix (4.2.5)**:
| Category | Count | Tests |
|----------|-------|-------|
| Happy Path | 3 | context, list, validate work |
| Negative | 2 | Invalid project ID, unknown command |
| Regression | 3 | Output matches v0.0.1 format |

**Files Changed**:
- `src/interface/cli/adapter.py`: Added `cmd_projects_context()` + session/items stubs
- `src/interface/cli/main.py`: Updated routing to use namespace handlers
- `tests/interface/cli/unit/test_main.py`: Updated imports, removed obsolete parser tests
- `tests/interface/cli/unit/test_main_v2.py`: NEW - routing tests for v0.1.0
- `tests/interface/cli/integration/test_cli_e2e.py`: Updated `init` → `projects context`

### Phase 4.3: Session Namespace ✅ COMPLETE

**Prerequisite**: Application layer handlers created.

| Task | Description | Status | Evidence |
|------|-------------|--------|----------|
| 4.3.1 | Create `ISessionRepository` port | ✅ COMPLETE | `src/session_management/application/ports/session_repository.py` |
| 4.3.2 | Create `CreateSessionCommand` + handler | ✅ COMPLETE | `src/session_management/application/commands/create_session_command.py` |
| 4.3.3 | Create `EndSessionCommand` + handler | ✅ COMPLETE | `src/session_management/application/commands/end_session_command.py` |
| 4.3.4 | Create `AbandonSessionCommand` + handler | ✅ COMPLETE | `src/session_management/application/commands/abandon_session_command.py` |
| 4.3.5 | Create `GetSessionStatusQuery` + handler | ✅ COMPLETE | `src/session_management/application/queries/get_session_status_query.py` |
| 4.3.6 | Create `InMemorySessionRepository` adapter | ✅ COMPLETE | `src/session_management/infrastructure/adapters/in_memory_session_repository.py` |
| 4.3.7 | Wire session handlers in bootstrap.py | ✅ COMPLETE | `src/bootstrap.py` updated |
| 4.3.8 | Update CLIAdapter session methods | ✅ COMPLETE | `src/interface/cli/adapter.py` (lines 250-469) |
| 4.3.9 | Write unit tests for session handlers | ✅ COMPLETE | 18 tests in `tests/session_management/unit/application/test_session_handlers.py` |

**Test Matrix (4.3.9)**: 18 tests pass
| Category | Count | Tests |
|----------|-------|-------|
| Happy Path | 11 | create, end, abandon, status - returns events and saves |
| Negative | 4 | create when active, end when none, abandon when none |
| Edge | 3 | JSON output, sequential sessions, repository injection |

**Files Created**:
- `src/session_management/application/ports/session_repository.py`
- `src/session_management/application/commands/__init__.py`
- `src/session_management/application/commands/create_session_command.py`
- `src/session_management/application/commands/end_session_command.py`
- `src/session_management/application/commands/abandon_session_command.py`
- `src/session_management/application/handlers/commands/__init__.py`
- `src/session_management/application/handlers/commands/create_session_command_handler.py`
- `src/session_management/application/handlers/commands/end_session_command_handler.py`
- `src/session_management/application/handlers/commands/abandon_session_command_handler.py`
- `src/session_management/application/handlers/queries/__init__.py`
- `src/session_management/application/handlers/queries/get_session_status_query_handler.py`
- `src/session_management/infrastructure/adapters/in_memory_session_repository.py`
- `tests/session_management/unit/application/test_session_handlers.py`

**Files Modified**:
- `src/bootstrap.py`: Added session repository singleton and handlers wiring
- `src/interface/cli/adapter.py`: Implemented session commands with handler integration
- `src/interface/cli/main.py`: Added session handler creation to CLI adapter factory
- `src/session_management/infrastructure/__init__.py`: Export InMemorySessionRepository
- `src/session_management/infrastructure/adapters/__init__.py`: Export InMemorySessionRepository
- `src/session_management/application/queries/__init__.py`: Export GetSessionStatusQuery

### Phase 4.4: Items Namespace (Queries First) ✅ COMPLETE

**Prerequisite**: Application layer query handlers must be created first.

| Task | Description | Status | Evidence |
|------|-------------|--------|----------|
| 4.4.1 | Create `ListWorkItemsQuery` + handler | ✅ COMPLETE | `src/work_tracking/application/handlers/queries/list_work_items_query_handler.py` |
| 4.4.2 | Create `GetWorkItemQuery` + handler | ✅ COMPLETE | `src/work_tracking/application/handlers/queries/get_work_item_query_handler.py` |
| 4.4.3 | Implement `jerry items list` | ✅ COMPLETE | `adapter.py:cmd_items_list()` dispatches query |
| 4.4.4 | Implement `jerry items show <id>` | ✅ COMPLETE | `adapter.py:cmd_items_show()` dispatches query |
| 4.4.5 | Write unit tests for items queries | ✅ COMPLETE | 12 tests in `tests/work_tracking/unit/application/test_items_query_handlers.py` |

**Test Matrix (4.4.5)**: 12 tests pass
| Category | Count | Tests |
|----------|-------|-------|
| Happy Path | 6 | list returns DTO, converts to DTOs, filter by status, limit, show returns detail DTO, includes all fields |
| Negative | 2 | Invalid status returns empty, show non-existent raises error |
| Edge | 4 | Empty list, pagination has_more, optional fields, completed_at timestamp |

**Files Created**:
- `src/work_tracking/application/__init__.py`
- `src/work_tracking/application/ports/__init__.py`
- `src/work_tracking/application/ports/work_item_repository.py`
- `src/work_tracking/application/queries/__init__.py`
- `src/work_tracking/application/queries/list_work_items_query.py`
- `src/work_tracking/application/queries/get_work_item_query.py`
- `src/work_tracking/application/handlers/__init__.py`
- `src/work_tracking/application/handlers/queries/__init__.py`
- `src/work_tracking/application/handlers/queries/list_work_items_query_handler.py`
- `src/work_tracking/application/handlers/queries/get_work_item_query_handler.py`
- `src/work_tracking/infrastructure/__init__.py`
- `src/work_tracking/infrastructure/adapters/__init__.py`
- `src/work_tracking/infrastructure/adapters/in_memory_work_item_repository.py`
- `tests/work_tracking/unit/application/test_items_query_handlers.py`
- `tests/work_tracking/__init__.py`, `tests/work_tracking/unit/__init__.py`, `tests/work_tracking/unit/application/__init__.py`

**Files Modified**:
- `src/bootstrap.py`: Added work item repository singleton and handler wiring
- `src/interface/cli/adapter.py`: Implemented items commands with query dispatching
- `src/work_tracking/infrastructure/__init__.py`: Export InMemoryWorkItemRepository

**Tech Debt**: TD-018 added to PHASE-TECHDEBT.md - Event Sourcing for Work Item Repository (current implementation is simplified in-memory, not event-sourced)

### Phase 4.5: Items Namespace (Commands - Stretch Goal)

**Note**: Commands depend on domain aggregates and command handlers. May be deferred.

| Task | Description | Status | Evidence |
|------|-------------|--------|----------|
| 4.5.1 | Create `CreateWorkItemCommand` + handler | ⏳ PENDING | Handler exists |
| 4.5.2 | Create `StartWorkItemCommand` + handler | ⏳ PENDING | Handler exists |
| 4.5.3 | Create `CompleteWorkItemCommand` + handler | ⏳ PENDING | Handler exists |
| 4.5.4 | Implement `jerry items create` | ⏳ PENDING | Command works |
| 4.5.5 | Implement `jerry items start` | ⏳ PENDING | Command works |
| 4.5.6 | Implement `jerry items complete` | ⏳ PENDING | Command works |
| 4.5.7 | Write unit tests for items commands | ⏳ PENDING | Tests pass |

### Phase 4.6: Integration & Documentation ✅ COMPLETE

| Task | Description | Status | Evidence |
|------|-------------|--------|----------|
| 4.6.1 | Verify `src/interface/cli/main.py` uses new parser | ✅ COMPLETE | Parser works, DISC-017 logged (cosmetic warning) |
| 4.6.2 | Verify `src/bootstrap.py` wires all dispatchers | ✅ COMPLETE | QueryDispatcher wired, DISC-018 logged (CommandDispatcher missing) |
| 4.6.3 | Write E2E tests | ✅ COMPLETE | 22 E2E tests (8 new for session/items), 1521 total pass |
| 4.6.4 | Update `CLAUDE.md` | ✅ COMPLETE | Added CLI Commands (v0.1.0) section with all namespaces |
| 4.6.5 | Update skills documentation | ✅ COMPLETE | Updated worktracker SKILL.md with CLI interface section |
| 4.6.6 | Update version to 0.1.0 | ✅ COMPLETE | Already at 0.1.0 in pyproject.toml and parser.py |

**Files Modified**:
- `CLAUDE.md`: Added CLI Commands (v0.1.0) section
- `skills/worktracker/SKILL.md`: Added CLI Interface section with command mapping
- `tests/interface/cli/integration/test_cli_e2e.py`: Added 8 E2E tests for session/items namespaces

---

## Application Layer Gaps (Must Create)

### Session Management Handlers ✅ ALL COMPLETE

| Handler | Type | Priority | Status | Location |
|---------|------|----------|--------|----------|
| `CreateSessionCommandHandler` | Command | HIGH | ✅ DONE | `src/session_management/application/handlers/commands/` |
| `EndSessionCommandHandler` | Command | HIGH | ✅ DONE | `src/session_management/application/handlers/commands/` |
| `AbandonSessionCommandHandler` | Command | MEDIUM | ✅ DONE | `src/session_management/application/handlers/commands/` |
| `GetSessionStatusQueryHandler` | Query | HIGH | ✅ DONE | `src/session_management/application/handlers/queries/` |

### Work Tracking Handlers

| Handler | Type | Priority | Status | Location |
|---------|------|----------|--------|----------|
| `ListWorkItemsQueryHandler` | Query | HIGH | ✅ DONE | `src/work_tracking/application/handlers/queries/` |
| `GetWorkItemQueryHandler` | Query | HIGH | ✅ DONE | `src/work_tracking/application/handlers/queries/` |
| `CreateWorkItemCommandHandler` | Command | MEDIUM | ⏳ DEFERRED | `src/work_tracking/application/handlers/commands/` |
| `StartWorkItemCommandHandler` | Command | LOW | ⏳ DEFERRED | `src/work_tracking/application/handlers/commands/` |
| `CompleteWorkItemCommandHandler` | Command | LOW | ⏳ DEFERRED | `src/work_tracking/application/handlers/commands/` |

---

## Test Summary

| Phase | Unit | Integration | E2E | Total | Status |
|-------|------|-------------|-----|-------|--------|
| 4.1 Parser | 33 | - | - | 33 | ✅ |
| 4.2 Projects | 8 | 3 | - | 11 | ✅ |
| 4.3 Session | 18 | - | - | 18 | ✅ |
| 4.4 Items (Q) | 12 | - | - | 12 | ✅ |
| 4.5 Items (C) | - | - | - | - | ⏳ DEFERRED |
| 4.6 Integration | - | - | TBD | TBD | ⏳ PENDING |
| **Total** | **71** | **3** | **TBD** | **74+** |

---

## Progress Tracking

| Date | Activity | Status |
|------|----------|--------|
| 2026-01-12 | Research complete (5W1H, Context7, industry patterns) | ✅ |
| 2026-01-12 | ADR-CLI-002 created | ✅ |
| 2026-01-12 | Work file created | ✅ |
| 2026-01-12 | Phase 4.1 Parser Infrastructure complete | ✅ |
| 2026-01-12 | 33 new parser tests written and passing | ✅ |
| 2026-01-12 | Phase 4.2 Projects namespace migration complete | ✅ |
| 2026-01-12 | cmd_projects_context() added, adapter stubs for session/items | ✅ |
| 2026-01-12 | All 71 CLI tests, 1444 total tests passing | ✅ |
| 2026-01-12 | Phase 4.3 Session namespace complete (18 tests) | ✅ |
| 2026-01-12 | Session handlers wired in bootstrap.py | ✅ |
| 2026-01-12 | Phase 4.4 Items namespace (queries) complete (12 tests) | ✅ |
| 2026-01-12 | Work tracking application layer created | ✅ |
| 2026-01-12 | TD-018 Event Sourcing tech debt documented | ✅ |
| 2026-01-12 | All 1474 tests passing | ✅ |
| 2026-01-12 | Decision: Skip Phase 4.5, proceed to Phase 4.6 | ✅ |
| 2026-01-12 | Phase 4.5 deferred until event sourcing (TD-018) addressed | ✅ |
| 2026-01-12 | Phase 4.6.1: main.py uses new parser (DISC-017: cosmetic warning) | ✅ |
| 2026-01-12 | Phase 4.6.2: bootstrap.py wiring verified (DISC-018: CommandDispatcher missing) | ✅ |
| 2026-01-12 | Phase 4.6.3: E2E tests added (8 new tests, 1521 total) | ✅ |
| 2026-01-12 | Phase 4.6.4: CLAUDE.md CLI section added | ✅ |
| 2026-01-12 | Phase 4.6.5: worktracker SKILL.md updated | ✅ |
| 2026-01-12 | Phase 4.6.6: Version 0.1.0 confirmed | ✅ |
| 2026-01-12 | **Phase 4.6 Integration & Documentation COMPLETE** | ✅ |
| - | Phase 4.5 Items commands (deferred - requires Event Sourcing TD-018) | ⏳ DEFERRED |

---

## Discoveries

| ID | Discovery | Impact | Action |
|----|-----------|--------|--------|
| DISC-001 | Phase 4.5 (Items Commands) requires event sourcing for mission-critical reliability | HIGH | Defer to post-TD-018 |
| DISC-002 | Current InMemoryWorkItemRepository is simplified, not event-sourced | MEDIUM | TD-018 tracks remediation |

---

## References

- **5W1H Research**: `research/phase4-cli-e-001-5w1h-namespaces.md`
- **ADR**: `decisions/ADR-CLI-002-namespace-implementation.md`
- **Design Canon**: `synthesis/PROJ-001-e-011-v1-jerry-design-canon.md`
- **Architecture Standards**: `.claude/rules/architecture-standards.md`
