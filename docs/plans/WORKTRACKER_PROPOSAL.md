# Jerry Framework - Implementation Work Tracker (Proposed)

> Granular implementation plan derived from ADR-034 unified design.
> **Source**: [ADR-034](../decisions/ADR-034-unified-wt-km-implementation.md) | [Unified Design](../design/work-034-e-003-unified-design.md)

**Created**: 2026-01-09
**Revised**: 2026-01-09
**Status**: PROPOSED (awaiting approval)
**Total Duration**: 32 weeks (4 phases)
**Branch**: TBD (implementation branch)

---

## Hierarchy Definition

| Level | ID Format | Scope | Duration | Example |
|-------|-----------|-------|----------|---------|
| **WORK** | WORK-NNN | Strategic work package | Weeks | WORK-101: Domain Layer |
| **TASK** | TASK-NNN-NN | Assignable deliverable | Days | TASK-101-01: Shared Kernel VOs |
| **Sub-task** | Checkbox | RED/GREEN/REFACTOR step | Hours | Implement VertexId with tests |

---

## Architecture & Testing Principles

> **MANDATORY**: All implementation MUST adhere to these principles.

### Architecture Pure Best Practices

| Pattern | Enforcement | Validation |
|---------|-------------|------------|
| DDD | Hard | Architecture tests verify bounded contexts |
| Hexagonal Architecture | Hard | No adapter imports in domain |
| Event Sourcing | Hard | Events immutable, append-only |
| CQRS | Hard | Commands return events, queries return DTOs |
| Repository Pattern | Hard | All data access via ports |
| Dispatcher Pattern | Hard | Events dispatched, not directly handled |
| Dependency Injection | Hard | No `new` in domain/application |

### Test Pyramid (Per Feature)

| Level | Count | Focus | Real Data |
|-------|-------|-------|-----------|
| Unit | Many | Single class/function | Mocked dependencies |
| Integration | Medium | Multiple components | Real SQLite |
| Contract | Few | Port compliance | Interface verification |
| System | Few | Multi-operation workflows | Full stack |
| E2E | Few | CLI to persistence | Real everything |
| Architecture | Always | Layer dependencies | Static analysis |

### BDD Red/Green/Refactor Protocol

```
1. RED: Write failing test with REAL assertions (no placeholders)
2. GREEN: Implement MINIMUM code to pass
3. REFACTOR: Clean up while maintaining GREEN
4. REPEAT: Until acceptance criteria met
```

### Test Coverage Requirements

| Scenario Type | Coverage |
|--------------|----------|
| Happy path | 100% of use cases |
| Edge cases | Boundary conditions, empty/max values |
| Failure scenarios | NotFound, InvalidState, Concurrent |
| Negative tests | Invalid input, malformed data |

---

## Quick Status

| Phase | Status | Progress | WORK Items | TASKs |
|-------|--------|----------|------------|-------|
| Phase 1: Work Tracker Foundation | PENDING | 0% | 4 | 18 |
| Phase 2: Shared Infrastructure | PENDING | 0% | 4 | 16 |
| Phase 3: KM Integration | PENDING | 0% | 4 | 16 |
| Phase 4: Advanced Features | PENDING | 0% | 4 | 14 |
| **Total** | | | **16** | **64** |

---

## Implementation Work Items Summary

| WORK ID | Name | TASKs | Duration | Dependencies |
|---------|------|-------|----------|--------------|
| WORK-101 | Domain Layer | 5 | Weeks 1-2 | None |
| WORK-102 | Repository Layer | 4 | Weeks 3-4 | WORK-101 |
| WORK-103 | CQRS Implementation | 5 | Weeks 5-6 | WORK-101, WORK-102 |
| WORK-104 | CLI Interface & BDD | 4 | Weeks 7-8 | WORK-103 |
| WORK-201 | Event Store | 3 | Weeks 9-10 | Phase 1 |
| WORK-202 | Graph Store | 4 | Weeks 11-12 | WORK-201 |
| WORK-203 | Semantic Index | 4 | Weeks 13-14 | WORK-202 |
| WORK-204 | RDF Serialization | 5 | Weeks 15-16 | WORK-202, WORK-203 |
| WORK-301 | KM Domain Layer | 4 | Weeks 17-18 | Phase 2 |
| WORK-302 | KM Repository Layer | 3 | Weeks 19-20 | WORK-301 |
| WORK-303 | KM CQRS Implementation | 5 | Weeks 21-22 | WORK-301, WORK-302 |
| WORK-304 | KM Interface Layer | 4 | Weeks 23-24 | WORK-303 |
| WORK-401 | Cross-Domain Integration | 4 | Weeks 25-26 | Phase 3 |
| WORK-402 | HybridRAG & Pattern Discovery | 4 | Weeks 27-28 | WORK-401 |
| WORK-403 | External API & Export | 3 | Weeks 29-30 | WORK-401 |
| WORK-404 | Documentation & Final Testing | 3 | Weeks 31-32 | All |

---

## Phase 1: Work Tracker Foundation (Weeks 1-8)

> **Goal**: Establish Work Tracker domain with full CQRS, proving hexagonal architecture patterns.
> **Reference**: [Unified Design §11 Phase 1](../design/work-034-e-003-unified-design.md#phase-1-work-tracker-foundation-weeks-1-8)

---

### WORK-101: Domain Layer - Shared Kernel & Work Tracker Entities

- **Status**: PENDING
- **Duration**: Weeks 1-2
- **Dependencies**: None
- **TASKs**: 5
- **Acceptance**: All BDD scenarios pass, architecture tests pass, 95%+ unit coverage
- **Reference**: [Unified Design §10.1](../design/work-034-e-003-unified-design.md#101-task-aggregate)

---

#### TASK-101-01: Shared Kernel Value Objects

- **Status**: PENDING
- **Estimated Duration**: 2-3 days
- **Files**: `src/domain/value_objects/`
- **Tests**: `tests/unit/domain/value_objects/`
- **Acceptance**: All VOs immutable, validated, 100% unit test coverage

**Sub-tasks:**

- [ ] **VertexId Base Class** (`vertex_id.py`)
  - [ ] RED: `test_vertex_id.py` - Valid UUID, invalid format, equality by value, immutability, empty string, whitespace
  - [ ] GREEN: Implement `@dataclass(frozen=True)` with UUID validation
  - [ ] REFACTOR: Ensure `__hash__` and `__eq__` work correctly

- [ ] **Domain-Specific IDs** (`ids.py`)
  - [ ] RED: `test_ids.py` - TaskId, PhaseId, PlanId, KnowledgeId creation; type distinctness; None/invalid handling
  - [ ] GREEN: Implement ID classes extending VertexId
  - [ ] REFACTOR: Extract common validation to base class

- [ ] **JerryURI Value Object** (`jerry_uri.py`)
  - [ ] RED: `test_jerry_uri.py` - Parse `jerry://task/abc-123`, nested paths, serialization, missing scheme, unknown type, malformed
  - [ ] GREEN: Implement parser with regex
  - [ ] REFACTOR: Add caching for parsed results

- [ ] **Priority Enum** (`priority.py`)
  - [ ] RED: `test_priority.py` - LOW/MEDIUM/HIGH/CRITICAL exist, ordering works, from_string parsing, case-insensitive, invalid string
  - [ ] GREEN: Implement IntEnum with comparison operators
  - [ ] REFACTOR: Add `__lt__`, `__le__` methods

- [ ] **Status Enums** (`status.py`)
  - [ ] RED: `test_status.py` - TaskStatus, PhaseStatus, PlanStatus states; valid transitions; invalid transition raises error
  - [ ] GREEN: Implement enums with transition validation
  - [ ] REFACTOR: Add `can_transition_to()` method

- [ ] **Tag Value Object** (`tag.py`)
  - [ ] RED: `test_tag.py` - Valid creation, normalized lowercase, trimmed whitespace, max length, empty/special chars rejected
  - [ ] GREEN: Implement with validation regex
  - [ ] REFACTOR: Add normalization in `__post_init__`

---

#### TASK-101-02: Task Aggregate Root

- **Status**: PENDING
- **Estimated Duration**: 3-4 days
- **Files**: `src/domain/aggregates/task.py`
- **Tests**: `tests/unit/domain/aggregates/test_task.py`
- **Acceptance**: Task lifecycle complete, all transitions emit events, invariants enforced

**Sub-tasks:**

- [ ] **Task Entity Core**
  - [ ] RED: Create with title/description, auto-generated TaskId, PENDING status, created_at, version=1; empty/long title rejected
  - [ ] GREEN: Implement `Task.__init__()` and `Task.create()` factory
  - [ ] REFACTOR: Extract validation to private methods

- [ ] **Task State Transitions**
  - [ ] RED: PENDING→IN_PROGRESS, IN_PROGRESS→COMPLETED/BLOCKED, BLOCKED→IN_PROGRESS, PENDING→CANCELLED; emits TaskTransitioned; same-state no-op; invalid transitions raise
  - [ ] GREEN: Implement `Task.transition_to()` with state machine
  - [ ] REFACTOR: Use state pattern or transition table

- [ ] **Task Completion**
  - [ ] RED: `complete()` sets COMPLETED + completed_at, emits TaskCompleted, requires IN_PROGRESS; with notes; from PENDING fails
  - [ ] GREEN: Implement `Task.complete(notes=None)`
  - [ ] REFACTOR: Ensure immutable event creation

- [ ] **Task Phase Assignment**
  - [ ] RED: `assign_to_phase()` sets phase_id, emits event, clears previous; None removes; COMPLETED task raises
  - [ ] GREEN: Implement `Task.assign_to_phase(phase_id)`
  - [ ] REFACTOR: Add phase validation callback option

- [ ] **Task Update Operations**
  - [ ] RED: `update_title/description`, `set_priority`, `add/remove_tag`; each increments version, emits TaskUpdated; duplicate tag no-op; COMPLETED update raises
  - [ ] GREEN: Implement update methods
  - [ ] REFACTOR: Extract common update pattern

- [ ] **Task Invariant Enforcement**
  - [ ] RED: BLOCKED requires blocker_reason; past due_date rejected; completed_at <= updated_at; clear blocker while BLOCKED fails
  - [ ] GREEN: Implement `_validate_invariants()` called after mutations
  - [ ] REFACTOR: Add invariant decorator

---

#### TASK-101-03: Phase Aggregate Root

- **Status**: PENDING
- **Estimated Duration**: 2-3 days
- **Files**: `src/domain/aggregates/phase.py`
- **Tests**: `tests/unit/domain/aggregates/test_phase.py`
- **Acceptance**: Phase lifecycle complete, task management works, completion validates tasks

**Sub-tasks:**

- [ ] **Phase Entity Core**
  - [ ] RED: Create with name/description, auto PhaseId, NOT_STARTED status, order_index, empty task_ids; empty name rejected
  - [ ] GREEN: Implement `Phase.__init__()` and `Phase.create()`
  - [ ] REFACTOR: Add validation methods

- [ ] **Phase Task Management**
  - [ ] RED: `add_task()` adds TaskId, emits event; `remove_task()` removes, emits; already-present no-op; non-present no-op; add to COMPLETED raises
  - [ ] GREEN: Implement `add_task()`, `remove_task()`
  - [ ] REFACTOR: Use set operations

- [ ] **Phase Completion Logic**
  - [ ] RED: `complete()` sets COMPLETED, emits PhaseCompleted, requires ACTIVE, requires all tasks completed; force=True bypasses; incomplete tasks raises
  - [ ] GREEN: Implement `Phase.complete(force=False)`
  - [ ] REFACTOR: Add task completion callback

- [ ] **Phase State Transitions**
  - [ ] RED: NOT_STARTED→ACTIVE valid; `activate()` emits PhaseActivated; NOT_STARTED→COMPLETED invalid; COMPLETED→ACTIVE invalid
  - [ ] GREEN: Implement `Phase.activate()`
  - [ ] REFACTOR: Add state machine

---

#### TASK-101-04: Plan Aggregate Root

- **Status**: PENDING
- **Estimated Duration**: 2-3 days
- **Files**: `src/domain/aggregates/plan.py`
- **Tests**: `tests/unit/domain/aggregates/test_plan.py`
- **Acceptance**: Plan lifecycle complete, phase management works, assumption tracking functional

**Sub-tasks:**

- [ ] **Plan Entity Core**
  - [ ] RED: Create with name/description, auto PlanId, DRAFT status, empty phases/assumptions; empty name rejected; name > 100 chars rejected
  - [ ] GREEN: Implement `Plan.__init__()` and `Plan.create()`
  - [ ] REFACTOR: Add metadata fields

- [ ] **Plan Phase Management**
  - [ ] RED: `add_phase()` with order, emits event; `remove_phase()` removes; `reorder_phases()` updates indices; `get_phases()` sorted; position shifts others; COMPLETED add raises; remove last raises
  - [ ] GREEN: Implement phase management methods
  - [ ] REFACTOR: Use OrderedDict or sorted list

- [ ] **Plan Assumption Tracking**
  - [ ] RED: `track_assumption()` adds text, emits event; `get_assumptions()` returns all; `validate_assumption()` marks status; duplicate no-op; empty text raises
  - [ ] GREEN: Implement assumption methods
  - [ ] REFACTOR: Create Assumption value object

- [ ] **Plan State Transitions**
  - [ ] RED: DRAFT→ACTIVE via `activate()`, emits event; ACTIVE→COMPLETED via `complete()`, requires phases done; ACTIVE→ARCHIVED via `archive()`; DRAFT→COMPLETED invalid; ARCHIVED→any invalid
  - [ ] GREEN: Implement `activate()`, `complete()`, `archive()`
  - [ ] REFACTOR: Add state machine

---

#### TASK-101-05: Domain Events & Exceptions

- **Status**: PENDING
- **Estimated Duration**: 2 days
- **Files**: `src/domain/events/`, `src/domain/exceptions.py`
- **Tests**: `tests/unit/domain/events/`, `tests/unit/domain/test_exceptions.py`, `tests/architecture/`
- **Acceptance**: CloudEvents 1.0 compliant, all exceptions have context, architecture tests pass

**Sub-tasks:**

- [ ] **CloudEventEnvelope Base** (`events/base.py`)
  - [ ] RED: `test_cloud_event_envelope.py` - specversion="1.0", type, source, id, time, data; JSON serialization; missing field raises
  - [ ] GREEN: Implement envelope dataclass
  - [ ] REFACTOR: Add JSON schema validation

- [ ] **Work Tracker Events** (`events/work_tracker.py`)
  - [ ] RED: `test_work_tracker_events.py` - TaskCreated/Updated/Transitioned/Completed; PhaseCreated/Activated/Completed; PlanCreated/Activated/Completed/Archived; all wrap in envelope; immutable
  - [ ] GREEN: Implement all event classes
  - [ ] REFACTOR: Add factory methods

- [ ] **Contract Tests for Events** (`tests/contract/events/`)
  - [ ] RED: All events validate against JSON schema; serialize/deserialize round-trip; event versioning
  - [ ] GREEN: Implement schema validation
  - [ ] REFACTOR: Add version migration support

- [ ] **Exception Hierarchy** (`exceptions.py`)
  - [ ] RED: `test_exceptions.py` - DomainError base; NotFoundError with entity_type/id; InvalidStateError with state/action; InvalidStateTransition with from/to; InvariantViolation; ConcurrencyError with versions; ValidationError with field/message
  - [ ] GREEN: Implement exception classes
  - [ ] REFACTOR: Add error codes

- [ ] **Architecture Tests** (`tests/architecture/`)
  - [ ] RED: `test_domain_architecture.py` - domain/ no imports from application/infrastructure/interface; stdlib only; aggregates extend base; VOs frozen
  - [ ] RED: `test_ddd_patterns.py` - private setters; behavior methods; immutable VOs; past-tense events
  - [ ] GREEN: Implement architecture validation
  - [ ] REFACTOR: Add CI integration

---

### WORK-102: Repository Layer - Ports & SQLite Adapters

- **Status**: PENDING
- **Duration**: Weeks 3-4
- **Dependencies**: WORK-101
- **TASKs**: 4
- **Acceptance**: All CRUD operations work, integration tests pass, 95%+ coverage
- **Reference**: [Unified Design §5.1](../design/work-034-e-003-unified-design.md#51-iworkitemrepository)

---

#### TASK-102-01: Repository Port Definitions

- **Status**: PENDING
- **Estimated Duration**: 1-2 days
- **Files**: `src/domain/ports/`
- **Tests**: `tests/unit/domain/ports/`
- **Acceptance**: All ports are abstract, fully typed, documented

**Sub-tasks:**

- [ ] **IWorkItemRepository Port** (`work_item_repository.py`)
  - [ ] RED: `test_work_item_repository.py` - get_task/save_task/delete_task/list_tasks signatures; same for Phase/Plan; ABC enforcement
  - [ ] GREEN: Implement abstract port interface
  - [ ] REFACTOR: Add type hints, docstrings

- [ ] **IUnitOfWork Port** (`unit_of_work.py`)
  - [ ] RED: `test_unit_of_work.py` - begin() context manager; commit(); rollback(); repository property; ABC enforcement
  - [ ] GREEN: Implement abstract port interface
  - [ ] REFACTOR: Add async support preparation

---

#### TASK-102-02: SQLite Schema & Migrations

- **Status**: PENDING
- **Estimated Duration**: 1-2 days
- **Files**: `migrations/001_work_tracker_schema.sql`
- **Tests**: `tests/integration/persistence/test_migrations.py`
- **Acceptance**: Schema created, idempotent, versioned

**Sub-tasks:**

- [ ] **Database Schema Migration**
  - [ ] RED: Creates tasks table with all columns; creates phases table; creates plans table; creates task_tags junction; idempotent; existing DB no-op; invalid migration raises
  - [ ] GREEN: Implement SQL migration script
  - [ ] REFACTOR: Add migration versioning table

---

#### TASK-102-03: SQLite Repository Adapter

- **Status**: PENDING
- **Estimated Duration**: 4-5 days
- **Files**: `src/infrastructure/persistence/sqlite_work_item_repo.py`
- **Tests**: `tests/integration/persistence/test_sqlite_*_repo.py`
- **Acceptance**: Full CRUD for all entities, optimistic concurrency, integration tests pass

**Sub-tasks:**

- [ ] **Task Repository CRUD**
  - [ ] RED: `test_sqlite_task_repo.py` - save inserts/updates; get returns/None; delete removes/False; list all/by status/priority/tags; concurrent update detected; stale version raises
  - [ ] GREEN: Implement Task CRUD methods
  - [ ] REFACTOR: Extract SQL to constants, parameterize

- [ ] **Phase Repository CRUD**
  - [ ] RED: `test_sqlite_phase_repo.py` - save/get/delete/list; list by plan_id; cascade delete removes associations; many tasks performant; orphan tasks option
  - [ ] GREEN: Implement Phase CRUD methods
  - [ ] REFACTOR: Add indexing for plan_id

- [ ] **Plan Repository CRUD**
  - [ ] RED: `test_sqlite_plan_repo.py` - save/get/delete/list; get with phases; list by status; cascade deletes phases; nested structure; delete active raises
  - [ ] GREEN: Implement Plan CRUD methods
  - [ ] REFACTOR: Add eager loading for phases

- [ ] **Optimistic Concurrency**
  - [ ] RED: `test_concurrency.py` - save increments version; outdated version fails; error includes expected/actual; concurrent updates detected
  - [ ] GREEN: Implement version checking
  - [ ] REFACTOR: Add retry logic option

---

#### TASK-102-04: Unit of Work & Contract Tests

- **Status**: PENDING
- **Estimated Duration**: 2 days
- **Files**: `src/infrastructure/persistence/sqlite_unit_of_work.py`
- **Tests**: `tests/integration/persistence/test_sqlite_unit_of_work.py`, `tests/contract/`
- **Acceptance**: Transactions work, rollback tested, contracts verified

**Sub-tasks:**

- [ ] **Unit of Work Implementation**
  - [ ] RED: `test_sqlite_unit_of_work.py` - begin starts transaction; commit persists; rollback reverts; context manager auto-commit/rollback; nested savepoints; failed UoW raises
  - [ ] GREEN: Implement SQLiteUnitOfWork
  - [ ] REFACTOR: Add connection pooling

- [ ] **Repository Contract Tests**
  - [ ] RED: `test_repository_contract.py` - adapter implements all methods; return types match; exceptions match; run against in-memory and file SQLite
  - [ ] GREEN: Implement contract test suite
  - [ ] REFACTOR: Parameterize for multiple adapters

---

### WORK-103: CQRS Implementation - Commands & Queries

- **Status**: PENDING
- **Duration**: Weeks 5-6
- **Dependencies**: WORK-101, WORK-102
- **TASKs**: 5
- **Acceptance**: All commands emit events, queries return DTOs, handlers tested
- **Reference**: [Unified Design §6.1-6.2](../design/work-034-e-003-unified-design.md#61-work-tracker-commands)

---

#### TASK-103-01: Task Commands & Handlers

- **Status**: PENDING
- **Estimated Duration**: 3 days
- **Files**: `src/application/commands/work_tracker/`, `src/application/handlers/commands/work_tracker/`
- **Tests**: `tests/unit/application/commands/`, `tests/unit/application/handlers/`
- **Acceptance**: All task commands functional, events dispatched, errors handled

**Sub-tasks:**

- [ ] **Task Command Definitions**
  - [ ] RED: `test_task_commands.py` - CreateTaskCommand has title/description/priority; UpdateTaskCommand has task_id + optionals; TransitionTaskCommand; CompleteTaskCommand; AssignTaskToPhaseCommand; immutable; invalid data raises
  - [ ] GREEN: Implement command dataclasses
  - [ ] REFACTOR: Add validation decorators

- [ ] **CreateTaskHandler**
  - [ ] RED: `test_create_task_handler.py` - creates via factory; saves via repo; dispatches TaskCreated; returns TaskId; rollback on dispatch failure; duplicate handling
  - [ ] GREEN: Implement handler
  - [ ] REFACTOR: Extract common handler pattern

- [ ] **UpdateTaskHandler**
  - [ ] RED: `test_update_task_handler.py` - fetches existing; applies updates; saves; dispatches TaskUpdated; not found raises; stale version raises
  - [ ] GREEN: Implement handler
  - [ ] REFACTOR: Use apply pattern

- [ ] **TransitionTaskHandler**
  - [ ] RED: `test_transition_task_handler.py` - transitions status; dispatches TaskTransitioned; invalid transition raises; not found raises
  - [ ] GREEN: Implement handler
  - [ ] REFACTOR: Add transition validation

- [ ] **CompleteTaskHandler**
  - [ ] RED: `test_complete_task_handler.py` - completes task; dispatches TaskCompleted; non-IN_PROGRESS raises
  - [ ] GREEN: Implement handler
  - [ ] REFACTOR: Add completion notes handling

---

#### TASK-103-02: Phase & Plan Commands & Handlers

- **Status**: PENDING
- **Estimated Duration**: 2-3 days
- **Files**: `src/application/commands/work_tracker/`, `src/application/handlers/commands/work_tracker/`
- **Tests**: `tests/unit/application/commands/`, `tests/unit/application/handlers/`
- **Acceptance**: All phase/plan commands functional, events dispatched

**Sub-tasks:**

- [ ] **Phase Command Definitions**
  - [ ] RED: `test_phase_commands.py` - CreatePhaseCommand with name/plan_id/order; CompletePhaseCommand; ActivatePhaseCommand; immutable
  - [ ] GREEN: Implement command dataclasses
  - [ ] REFACTOR: Ensure consistency

- [ ] **Phase Handlers**
  - [ ] RED: CreatePhaseHandler, CompletePhaseHandler, ActivatePhaseHandler - follow task handler pattern; test event emission
  - [ ] GREEN: Implement handlers
  - [ ] REFACTOR: Extract base handler

- [ ] **Plan Command Definitions**
  - [ ] RED: `test_plan_commands.py` - CreatePlanCommand; ActivatePlanCommand; CompletePlanCommand; immutable
  - [ ] GREEN: Implement command dataclasses
  - [ ] REFACTOR: Add builder pattern option

- [ ] **Plan Handlers**
  - [ ] RED: CreatePlanHandler, ActivatePlanHandler, CompletePlanHandler - follow pattern; test event emission; complete requires phases done
  - [ ] GREEN: Implement handlers
  - [ ] REFACTOR: Extract base handler

---

#### TASK-103-03: Query Definitions & DTOs

- **Status**: PENDING
- **Estimated Duration**: 2 days
- **Files**: `src/application/queries/work_tracker/`, `src/application/dtos/`
- **Tests**: `tests/unit/application/queries/`, `tests/unit/application/dtos/`
- **Acceptance**: All DTOs immutable with factories, queries typed

**Sub-tasks:**

- [ ] **Work Tracker DTOs**
  - [ ] RED: `test_work_tracker_dtos.py` - TaskDTO has all fields; PhaseDTO with task count; PlanDTO with phase list; immutable; `from_entity()` factory
  - [ ] GREEN: Implement `src/application/dtos/work_tracker.py`
  - [ ] REFACTOR: Add serialization methods

- [ ] **Task Queries**
  - [ ] RED: `test_task_queries.py` - GetTaskQuery has task_id; ListTasksQuery has filters; GetTaskHistoryQuery has task_id
  - [ ] GREEN: Implement query dataclasses
  - [ ] REFACTOR: Add pagination

- [ ] **Phase & Plan Queries**
  - [ ] RED: GetPhaseQuery, ListPhasesQuery, GetPlanQuery, ListPlansQuery with appropriate fields
  - [ ] GREEN: Implement query dataclasses
  - [ ] REFACTOR: Add pagination

---

#### TASK-103-04: Query Handlers

- **Status**: PENDING
- **Estimated Duration**: 2-3 days
- **Files**: `src/application/handlers/queries/work_tracker/`
- **Tests**: `tests/unit/application/handlers/queries/`
- **Acceptance**: All query handlers return DTOs, filters work

**Sub-tasks:**

- [ ] **Task Query Handlers**
  - [ ] RED: `test_task_query_handlers.py` - GetTaskQueryHandler returns TaskDTO/None; ListTasksQueryHandler returns list, applies filters; GetTaskHistoryQueryHandler returns events; empty list for no matches
  - [ ] GREEN: Implement handlers
  - [ ] REFACTOR: Add caching layer preparation

- [ ] **Phase & Plan Query Handlers**
  - [ ] RED: Same pattern - get returns DTO/None; list returns filtered list; include related data
  - [ ] GREEN: Implement handlers
  - [ ] REFACTOR: Add eager loading options

---

#### TASK-103-05: Event Dispatcher & Integration

- **Status**: PENDING
- **Estimated Duration**: 2 days
- **Files**: `src/domain/ports/event_dispatcher.py`, `src/infrastructure/messaging/`
- **Tests**: `tests/unit/domain/ports/`, `tests/integration/messaging/`, `tests/integration/application/`
- **Acceptance**: Events dispatched correctly, integration tests pass

**Sub-tasks:**

- [ ] **Event Dispatcher Port**
  - [ ] RED: `test_event_dispatcher.py` - dispatch(event); dispatch_all(events); subscribe(type, handler); ABC enforcement
  - [ ] GREEN: Implement `src/domain/ports/event_dispatcher.py`
  - [ ] REFACTOR: Add type constraints

- [ ] **In-Memory Dispatcher Adapter**
  - [ ] RED: `test_in_memory_dispatcher.py` - dispatch calls handlers; multiple handlers per type; no handler is no-op; exception doesn't stop others; async support; timeout handling
  - [ ] GREEN: Implement `src/infrastructure/messaging/in_memory_dispatcher.py`
  - [ ] REFACTOR: Add logging, retry logic

- [ ] **CQRS Integration Tests**
  - [ ] RED: `test_cqrs_integration.py` - create→query returns it; update→query shows changes; complete→query shows completed; events dispatched; full lifecycle
  - [ ] GREEN: Implement integration test suite
  - [ ] REFACTOR: Add performance assertions

---

### WORK-104: CLI Interface & BDD Tests

- **Status**: PENDING
- **Duration**: Weeks 7-8
- **Dependencies**: WORK-103
- **TASKs**: 4
- **Acceptance**: Full CRUD via CLI, 100% BDD scenario coverage, <100ms p95
- **Reference**: [Unified Design §7](../design/work-034-e-003-unified-design.md#7-interface-specifications)

---

#### TASK-104-01: CLI Adapter Implementation

- **Status**: PENDING
- **Estimated Duration**: 4-5 days
- **Files**: `src/interface/cli/work_tracker_cli.py`, `scripts/wt.py`
- **Tests**: `tests/e2e/cli/`
- **Acceptance**: All commands work, output formats correct, errors helpful

**Sub-tasks:**

- [ ] **CLI Entry Point**
  - [ ] RED: `test_work_tracker_cli.py` - `wt --help` shows usage; `--version` shows version; exit 0 success; exit 1 error; unknown command error
  - [ ] GREEN: Implement main CLI entry point
  - [ ] REFACTOR: Add rich output formatting

- [ ] **Task Subcommand**
  - [ ] RED: `test_task_cli.py` - `create "Title"` works; `list` works; `show <id>` works; `update <id> --title` works; `complete <id>` works; `delete <id>` works; `--json` outputs JSON; all optional fields; non-existent shows error
  - [ ] GREEN: Implement task subcommand
  - [ ] REFACTOR: Add confirmation prompts

- [ ] **Phase Subcommand**
  - [ ] RED: `test_phase_cli.py` - `create "Name" --plan <id>` works; `list --plan <id>` works; `show <id>` works; `complete <id>` works; without plan fails
  - [ ] GREEN: Implement phase subcommand
  - [ ] REFACTOR: Add progress indicator

- [ ] **Plan Subcommand**
  - [ ] RED: `test_plan_cli.py` - `create "Name"` works; `list` works; `show <id>` with phases; `activate <id>` works; `complete <id>` works; incomplete phases fails
  - [ ] GREEN: Implement plan subcommand
  - [ ] REFACTOR: Add tree view

- [ ] **CLI Error Handling**
  - [ ] RED: `test_cli_errors.py` - invalid ID format; database error; validation error; concurrent modification; all show helpful messages
  - [ ] GREEN: Implement error handling
  - [ ] REFACTOR: Add error codes for scripting

---

#### TASK-104-02: Work Tracker SKILL.md

- **Status**: PENDING
- **Estimated Duration**: 1 day
- **Files**: `skills/work-tracker/SKILL.md`
- **Tests**: Manual verification
- **Acceptance**: All commands documented, examples work, patterns clear

**Sub-tasks:**

- [ ] **Skill Documentation**
  - [ ] Create `skills/work-tracker/SKILL.md`
  - [ ] Document all task commands with examples
  - [ ] Document all phase commands with examples
  - [ ] Document all plan commands with examples
  - [ ] Include natural language patterns
  - [ ] Add troubleshooting section
  - [ ] Add quick reference card

---

#### TASK-104-03: BDD Test Suite

- **Status**: PENDING
- **Estimated Duration**: 3-4 days
- **Files**: `tests/bdd/work_tracker/`
- **Tests**: Feature files + step definitions
- **Acceptance**: All scenarios pass, no mocks in steps, real implementations

**Sub-tasks:**

- [ ] **Task Feature File** (`features/task.feature`)
  - [ ] Scenario: Create task with title and description
  - [ ] Scenario: Create task with priority and tags
  - [ ] Scenario: Transition task through states
  - [ ] Scenario: Complete task records completion time
  - [ ] Scenario: Assign task to phase
  - [ ] Scenario: Block task with reason
  - [ ] Scenario: Cancel pending task
  - [ ] Edge: Create task with max-length title
  - [ ] Negative: Create task with empty title fails
  - [ ] Negative: Complete task not in progress fails

- [ ] **Phase Feature File** (`features/phase.feature`)
  - [ ] Scenario: Create phase in plan
  - [ ] Scenario: Add tasks to phase
  - [ ] Scenario: Remove task from phase
  - [ ] Scenario: Complete phase when all tasks done
  - [ ] Negative: Complete phase with incomplete tasks fails

- [ ] **Plan Feature File** (`features/plan.feature`)
  - [ ] Scenario: Create plan with phases
  - [ ] Scenario: Activate draft plan
  - [ ] Scenario: Complete plan when all phases done
  - [ ] Scenario: Track assumptions on plan
  - [ ] Negative: Complete plan with incomplete phases fails

- [ ] **Step Definitions**
  - [ ] `steps/task_steps.py` - REAL implementations, no mocks
  - [ ] `steps/phase_steps.py` - REAL implementations, no mocks
  - [ ] `steps/plan_steps.py` - REAL implementations, no mocks

---

#### TASK-104-04: System Tests & Phase 1 Gate

- **Status**: PENDING
- **Estimated Duration**: 2 days
- **Files**: `tests/system/work_tracker/`
- **Tests**: System and performance tests
- **Acceptance**: All quality gates pass, performance targets met

**Sub-tasks:**

- [ ] **Multi-Operation Workflow Tests**
  - [ ] RED: `test_full_workflow.py` - create plan→phases→tasks→complete all; multiple plans interleaved; persistence across CLI invocations; concurrent operations safe
  - [ ] GREEN: Implement workflow tests
  - [ ] REFACTOR: Add data cleanup

- [ ] **Performance Tests**
  - [ ] RED: `test_performance.py` - create 1000 tasks < 10s; list 1000 tasks < 1s; single operation p95 < 100ms; memory bounded
  - [ ] GREEN: Implement performance tests
  - [ ] REFACTOR: Add benchmarking

- [ ] **Phase 1 Go/No-Go Gate Checklist**
  - [ ] All unit tests pass (95%+ coverage)
  - [ ] All integration tests pass
  - [ ] All BDD scenarios pass
  - [ ] All E2E tests pass
  - [ ] All architecture tests pass
  - [ ] All contract tests pass
  - [ ] CLI operations < 100ms p95
  - [ ] Code review approved
  - [ ] No critical/high security issues

---

## Phase 2: Shared Infrastructure (Weeks 9-16)

> **Goal**: Build shared infrastructure components (Event Store, Graph, Search, RDF).
> **Reference**: [Unified Design §11 Phase 2](../design/work-034-e-003-unified-design.md#phase-2-shared-infrastructure-weeks-9-16)

*[Phase 2-4 follow the same WORK → TASK → Sub-task structure as Phase 1. See full document for details.]*

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| WORK Items | 16 |
| TASKs | 64 |
| Estimated Sub-tasks | ~400 |
| Estimated Tests | ~845 |
| Duration | 32 weeks |

---

## Technology Stack

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Runtime | Python | 3.11+ | Zero-dependency core |
| Graph | NetworkX | 3.2.1 | Property graph |
| Vector Search | FAISS | 1.7.4 | Semantic similarity |
| RDF | RDFLib | 7.0.0 | Knowledge export |
| Persistence | SQLite | 3.x | Entity and event storage |
| Testing | pytest | 8.x | All test types |
| BDD | pytest-bdd | 7.x | BDD scenarios |

---

## Key Decisions (From ADR-034)

| Decision | Score | Choice | Alternative |
|----------|-------|--------|-------------|
| Architecture | 8.4/10 | Hexagonal | Layered (7.0) |
| Sequence | 8.65/10 | WT First | KM First (6.05) |
| Graph DB | 8.5/10 | NetworkX | Neo4j (7.05) |
| Vector Search | 8.1/10 | FAISS | Pinecone (7.25) |
| Database | 9.0/10 | SQLite | PostgreSQL (6.35) |

---

## Risk Register Summary

| ID | Risk | Probability | Impact | Mitigation |
|----|------|-------------|--------|------------|
| R-001 | Performance at scale | Medium | High | Validate at WT scale first |
| R-002 | Supernode formation | Medium | High | Edge count validator |
| R-003 | Test suite too slow | Medium | Medium | Parallel execution, isolation |
| R-004 | User AAR adoption | Medium | Medium | Track completion rate |
| R-005 | Schema evolution | Medium | High | Version envelope pattern |
| R-006 | Integration complexity | Medium | Medium | Feature flags, incremental |

---

## References

| Document | Size | Purpose |
|----------|------|---------|
| [ADR-034](../decisions/ADR-034-unified-wt-km-implementation.md) | 59KB | Architecture decision |
| [Unified Design](../design/work-034-e-003-unified-design.md) | 87KB | Technical specifications |
| [Trade-off Analysis](../analysis/work-034-e-004-tradeoff-analysis.md) | 39KB | Decision rationale |
| [Domain Synthesis](../synthesis/work-034-e-002-domain-synthesis.md) | 54KB | Domain model |
| [Domain Analysis](../research/work-034-e-001-domain-analysis.md) | 93KB | Research foundation |
| [Validation Report](../validation/work-034-e-006-validation-report.md) | 17KB | Approval status |

---

*Revised with proper WORK → TASK → Sub-task hierarchy on 2026-01-09*
