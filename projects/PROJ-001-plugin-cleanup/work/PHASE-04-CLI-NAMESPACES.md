# Phase 4: CLI Namespaces per Bounded Context

**Status**: 🔄 IN PROGRESS
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

### Phase 4.3: Session Namespace

**Prerequisite**: Application layer handlers must be created first.

| Task | Description | Status | Evidence |
|------|-------------|--------|----------|
| 4.3.1 | Create `CreateSessionCommand` + handler | ⏳ PENDING | Handler exists |
| 4.3.2 | Create `EndSessionCommand` + handler | ⏳ PENDING | Handler exists |
| 4.3.3 | Create `AbandonSessionCommand` + handler | ⏳ PENDING | Handler exists |
| 4.3.4 | Create `GetSessionStatusQuery` + handler | ⏳ PENDING | Handler exists |
| 4.3.5 | Implement `jerry session start` | ⏳ PENDING | Command works |
| 4.3.6 | Implement `jerry session end` | ⏳ PENDING | Command works |
| 4.3.7 | Implement `jerry session status` | ⏳ PENDING | Command works |
| 4.3.8 | Implement `jerry session abandon` | ⏳ PENDING | Command works |
| 4.3.9 | Write unit tests for session commands | ⏳ PENDING | Tests pass |

**Test Matrix (4.3.9)**:
| Category | Count | Tests |
|----------|-------|-------|
| Happy Path | 4 | start, end, status, abandon work |
| Negative | 3 | start when active, end when none, abandon without reason |
| Edge | 2 | JSON output, multiple sessions |

### Phase 4.4: Items Namespace (Queries First)

**Prerequisite**: Application layer query handlers must be created first.

| Task | Description | Status | Evidence |
|------|-------------|--------|----------|
| 4.4.1 | Create `ListWorkItemsQuery` + handler | ⏳ PENDING | Handler exists |
| 4.4.2 | Create `GetWorkItemQuery` + handler | ⏳ PENDING | Handler exists |
| 4.4.3 | Implement `jerry items list` | ⏳ PENDING | Command works |
| 4.4.4 | Implement `jerry items show <id>` | ⏳ PENDING | Command works |
| 4.4.5 | Write unit tests for items queries | ⏳ PENDING | Tests pass |

**Test Matrix (4.4.5)**:
| Category | Count | Tests |
|----------|-------|-------|
| Happy Path | 4 | list all, list by status, list by type, show by ID |
| Negative | 2 | Show non-existent ID, invalid filters |
| Edge | 2 | Empty list, JSON output |

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

### Phase 4.6: Integration & Documentation

| Task | Description | Status | Evidence |
|------|-------------|--------|----------|
| 4.6.1 | Update `src/interface/cli/main.py` | ⏳ PENDING | Uses new parser |
| 4.6.2 | Update `src/bootstrap.py` | ⏳ PENDING | Wires command dispatcher |
| 4.6.3 | Write E2E tests | ⏳ PENDING | Full workflows pass |
| 4.6.4 | Update `CLAUDE.md` | ⏳ PENDING | CLI section updated |
| 4.6.5 | Update skills documentation | ⏳ PENDING | Skills reference new commands |
| 4.6.6 | Update version to 0.1.0 | ⏳ PENDING | `pyproject.toml` updated |

---

## Application Layer Gaps (Must Create)

### Session Management Handlers

| Handler | Type | Priority | Location |
|---------|------|----------|----------|
| `CreateSessionCommandHandler` | Command | HIGH | `src/session_management/application/handlers/commands/` |
| `EndSessionCommandHandler` | Command | HIGH | `src/session_management/application/handlers/commands/` |
| `AbandonSessionCommandHandler` | Command | MEDIUM | `src/session_management/application/handlers/commands/` |
| `GetSessionStatusQueryHandler` | Query | HIGH | `src/session_management/application/handlers/queries/` |

### Work Tracking Handlers

| Handler | Type | Priority | Location |
|---------|------|----------|----------|
| `ListWorkItemsQueryHandler` | Query | HIGH | `src/work_tracking/application/handlers/queries/` |
| `GetWorkItemQueryHandler` | Query | HIGH | `src/work_tracking/application/handlers/queries/` |
| `CreateWorkItemCommandHandler` | Command | MEDIUM | `src/work_tracking/application/handlers/commands/` |
| `StartWorkItemCommandHandler` | Command | LOW | `src/work_tracking/application/handlers/commands/` |
| `CompleteWorkItemCommandHandler` | Command | LOW | `src/work_tracking/application/handlers/commands/` |

---

## Test Summary

| Phase | Unit | Integration | E2E | Total |
|-------|------|-------------|-----|-------|
| 4.1 Parser | 11 | - | - | 11 |
| 4.2 Projects | 8 | 3 | - | 11 |
| 4.3 Session | 9 | 3 | 2 | 14 |
| 4.4 Items (Q) | 8 | 2 | 2 | 12 |
| 4.5 Items (C) | 9 | 2 | 2 | 13 |
| 4.6 Integration | - | - | 5 | 5 |
| **Total** | **45** | **10** | **11** | **~66** |

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
| - | Phase 4.3 Session namespace implementation | ⏳ NEXT |

---

## References

- **5W1H Research**: `research/phase4-cli-e-001-5w1h-namespaces.md`
- **ADR**: `decisions/ADR-CLI-002-namespace-implementation.md`
- **Design Canon**: `synthesis/PROJ-001-e-011-v1-jerry-design-canon.md`
- **Architecture Standards**: `.claude/rules/architecture-standards.md`
