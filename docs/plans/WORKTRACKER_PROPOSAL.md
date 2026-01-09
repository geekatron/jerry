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

---

### WORK-201: Event Store - CloudEvents Persistence

- **Status**: PENDING
- **Duration**: Weeks 9-10
- **Dependencies**: Phase 1 complete
- **TASKs**: 3
- **Acceptance**: CloudEvents 1.0 compliant, append-only, queryable by type/source/time
- **Reference**: [Unified Design §5.3](../design/work-034-e-003-unified-design.md#53-ieventstore)

---

#### TASK-201-01: Event Store Port Definition

- **Status**: PENDING
- **Estimated Duration**: 1-2 days
- **Files**: `src/domain/ports/event_store.py`
- **Tests**: `tests/unit/domain/ports/test_event_store.py`
- **Acceptance**: All methods abstract, fully typed, CloudEvents compliant

**Sub-tasks:**

- [ ] **IEventStore Port**
  - [ ] RED: `test_event_store_port.py` - append(event); get_events_for_aggregate(id); get_all_events(); get_events_by_type(type); get_events_since(timestamp); ABC enforcement; type hints complete
  - [ ] GREEN: Implement abstract port interface
  - [ ] REFACTOR: Add docstrings, JSON schema reference

- [ ] **Event Stream Abstraction**
  - [ ] RED: `test_event_stream.py` - EventStream iterable; supports slicing; lazy evaluation; position tracking; empty stream handling
  - [ ] GREEN: Implement EventStream class
  - [ ] REFACTOR: Add __repr__ and debugging aids

---

#### TASK-201-02: SQLite Event Store Adapter

- **Status**: PENDING
- **Estimated Duration**: 3-4 days
- **Files**: `src/infrastructure/event_store/sqlite_event_store.py`, `migrations/002_event_store_schema.sql`
- **Tests**: `tests/integration/event_store/test_sqlite_event_store.py`
- **Acceptance**: Append-only, indexed queries, optimistic concurrency

**Sub-tasks:**

- [ ] **Event Store Schema**
  - [ ] RED: events table with id/type/source/time/data/aggregate_id/version; indexes on aggregate_id, type, time; idempotent
  - [ ] GREEN: Implement SQL migration
  - [ ] REFACTOR: Add partition hint column for future sharding

- [ ] **Append Operations**
  - [ ] RED: `test_sqlite_append.py` - append single event; append batch atomic; duplicate id rejected; aggregate version incremented; CloudEvents envelope validated
  - [ ] GREEN: Implement append methods
  - [ ] REFACTOR: Add batch optimization

- [ ] **Query Operations**
  - [ ] RED: `test_sqlite_query.py` - get_for_aggregate returns ordered; get_by_type filters; get_since excludes older; get_all paginated; empty returns empty list
  - [ ] GREEN: Implement query methods
  - [ ] REFACTOR: Add cursor-based pagination

- [ ] **Optimistic Concurrency**
  - [ ] RED: `test_event_concurrency.py` - expected version check; version mismatch raises; gap detection; concurrent appends handled
  - [ ] GREEN: Implement version checking
  - [ ] REFACTOR: Add retry with backoff option

---

#### TASK-201-03: Event Store Contract Tests & Integration

- **Status**: PENDING
- **Estimated Duration**: 2 days
- **Files**: `tests/contract/event_store/`, `tests/integration/event_store/`
- **Tests**: Contract and integration tests
- **Acceptance**: All contracts pass, WT events persisted correctly

**Sub-tasks:**

- [ ] **Contract Test Suite**
  - [ ] RED: `test_event_store_contract.py` - all port methods implemented; return types correct; exceptions correct; run in-memory and file
  - [ ] GREEN: Implement contract tests
  - [ ] REFACTOR: Parameterize for future adapters

- [ ] **Work Tracker Integration**
  - [ ] RED: `test_wt_event_integration.py` - create task → event stored; complete task → events ordered; query by task aggregate works; replay builds state
  - [ ] GREEN: Implement WT event store integration
  - [ ] REFACTOR: Add snapshot preparation

---

### WORK-202: Graph Store - NetworkX Adapter

- **Status**: PENDING
- **Duration**: Weeks 11-12
- **Dependencies**: WORK-201
- **TASKs**: 4
- **Acceptance**: Full traversal operations, WT entities as vertices, performance targets met
- **Reference**: [Unified Design §5.4](../design/work-034-e-003-unified-design.md#54-igraphstore)

---

#### TASK-202-01: Graph Store Port Definition

- **Status**: PENDING
- **Estimated Duration**: 1-2 days
- **Files**: `src/domain/ports/graph_store.py`
- **Tests**: `tests/unit/domain/ports/test_graph_store.py`
- **Acceptance**: All traversal operations defined, typed, ABC enforced

**Sub-tasks:**

- [ ] **IGraphStore Port**
  - [ ] RED: `test_graph_store_port.py` - add_vertex(id, properties); add_edge(from, to, type, properties); get_vertex(id); get_edges(id); traverse(start, depth); remove_vertex(); remove_edge(); ABC enforcement
  - [ ] GREEN: Implement abstract port interface
  - [ ] REFACTOR: Add type constraints for properties

- [ ] **Traversal Operations**
  - [ ] RED: `test_traversal_ops.py` - BFS traversal; DFS traversal; path_between(a, b); neighbors(id); ancestors(id); descendants(id); cycle detection
  - [ ] GREEN: Implement traversal method signatures
  - [ ] REFACTOR: Add filtering predicates

---

#### TASK-202-02: NetworkX Graph Adapter

- **Status**: PENDING
- **Estimated Duration**: 3-4 days
- **Files**: `src/infrastructure/graph/networkx_graph_store.py`
- **Tests**: `tests/integration/graph/test_networkx_graph_store.py`
- **Acceptance**: All port methods implemented, traversals work, properties stored

**Sub-tasks:**

- [ ] **Vertex Operations**
  - [ ] RED: `test_networkx_vertices.py` - add_vertex creates node; properties stored; get returns dict/None; update merges props; remove deletes; duplicate id updates
  - [ ] GREEN: Implement vertex CRUD
  - [ ] REFACTOR: Add property validation

- [ ] **Edge Operations**
  - [ ] RED: `test_networkx_edges.py` - add_edge connects; type stored; properties stored; get returns edges; remove deletes; missing vertex raises; duplicate edge updates
  - [ ] GREEN: Implement edge CRUD
  - [ ] REFACTOR: Add edge type constraints

- [ ] **Traversal Implementation**
  - [ ] RED: `test_networkx_traversal.py` - BFS yields in order; DFS yields in order; path_between returns shortest; max_depth limits; no path returns None; cycle handling
  - [ ] GREEN: Implement traversal algorithms
  - [ ] REFACTOR: Add visited caching

- [ ] **Graph Persistence**
  - [ ] RED: `test_graph_persistence.py` - save to JSON; load from JSON; round-trip preserves structure; corrupt file raises; merge strategy
  - [ ] GREEN: Implement persistence methods
  - [ ] REFACTOR: Add GraphML export option

---

#### TASK-202-03: Work Tracker Graph Integration

- **Status**: PENDING
- **Estimated Duration**: 2 days
- **Files**: `src/application/event_handlers/graph_projector.py`
- **Tests**: `tests/integration/application/test_graph_projector.py`
- **Acceptance**: WT entities projected to graph, relationships correct

**Sub-tasks:**

- [ ] **Graph Projector Event Handler**
  - [ ] RED: `test_graph_projector.py` - TaskCreated adds vertex; TaskAssignedToPhase adds edge; PhaseCreated adds vertex; PlanCreated adds vertex; PlanActivated adds status edge; idempotent replays
  - [ ] GREEN: Implement GraphProjector handler
  - [ ] REFACTOR: Add batch processing

- [ ] **Graph Query Service**
  - [ ] RED: `test_graph_query_service.py` - get_task_relationships(id); get_phase_hierarchy(id); get_plan_structure(id); orphan detection; connected component analysis
  - [ ] GREEN: Implement query service
  - [ ] REFACTOR: Add caching layer

---

#### TASK-202-04: Graph Store Contract Tests

- **Status**: PENDING
- **Estimated Duration**: 1-2 days
- **Files**: `tests/contract/graph/`
- **Tests**: Contract tests
- **Acceptance**: All contracts pass, future adapters can swap in

**Sub-tasks:**

- [ ] **Contract Test Suite**
  - [ ] RED: `test_graph_store_contract.py` - all methods implemented; return types match; exception types match; traversal order consistent
  - [ ] GREEN: Implement contract tests
  - [ ] REFACTOR: Add performance baselines

- [ ] **Supernode Prevention Tests**
  - [ ] RED: `test_supernode_prevention.py` - edge count alert at 100; soft limit at 500; warning logged; exception at hard limit
  - [ ] GREEN: Implement edge count validator
  - [ ] REFACTOR: Add configurable thresholds

---

### WORK-203: Semantic Index - FAISS Adapter

- **Status**: PENDING
- **Duration**: Weeks 13-14
- **Dependencies**: WORK-202
- **TASKs**: 4
- **Acceptance**: kNN search works, embeddings stored, similarity threshold configurable
- **Reference**: [Unified Design §5.5](../design/work-034-e-003-unified-design.md#55-isemanticindex)

---

#### TASK-203-01: Semantic Index Port Definition

- **Status**: PENDING
- **Estimated Duration**: 1-2 days
- **Files**: `src/domain/ports/semantic_index.py`
- **Tests**: `tests/unit/domain/ports/test_semantic_index.py`
- **Acceptance**: All search operations defined, embedding interface clear

**Sub-tasks:**

- [ ] **ISemanticIndex Port**
  - [ ] RED: `test_semantic_index_port.py` - add_embedding(id, vector, metadata); search_similar(vector, k, threshold); remove_embedding(id); get_embedding(id); update_embedding(); ABC enforcement
  - [ ] GREEN: Implement abstract port interface
  - [ ] REFACTOR: Add dimension constraint

- [ ] **IEmbeddingProvider Port**
  - [ ] RED: `test_embedding_provider_port.py` - embed_text(text) returns vector; embed_batch(texts) returns vectors; dimension property; ABC enforcement
  - [ ] GREEN: Implement abstract port interface
  - [ ] REFACTOR: Add caching hint

---

#### TASK-203-02: FAISS Semantic Index Adapter

- **Status**: PENDING
- **Estimated Duration**: 3-4 days
- **Files**: `src/infrastructure/search/faiss_semantic_index.py`
- **Tests**: `tests/integration/search/test_faiss_semantic_index.py`
- **Acceptance**: kNN search works, metadata stored, persistence works

**Sub-tasks:**

- [ ] **FAISS Index Setup**
  - [ ] RED: `test_faiss_setup.py` - index created with dimension; flat index for small scale; IVF index option; index empty initially; wrong dimension raises
  - [ ] GREEN: Implement index initialization
  - [ ] REFACTOR: Add index type configuration

- [ ] **Embedding Operations**
  - [ ] RED: `test_faiss_embeddings.py` - add stores vector + metadata; get returns vector; update replaces; remove deletes; batch add atomic; duplicate id updates
  - [ ] GREEN: Implement embedding CRUD
  - [ ] REFACTOR: Add ID mapping optimization

- [ ] **Similarity Search**
  - [ ] RED: `test_faiss_search.py` - search returns k nearest; threshold filters; distance scores returned; empty index returns empty; metadata included in results
  - [ ] GREEN: Implement search methods
  - [ ] REFACTOR: Add reranking option

- [ ] **Index Persistence**
  - [ ] RED: `test_faiss_persistence.py` - save to file; load from file; round-trip preserves vectors; metadata persisted separately; corrupt file raises
  - [ ] GREEN: Implement persistence
  - [ ] REFACTOR: Add incremental update option

---

#### TASK-203-03: Simple Embedding Provider

- **Status**: PENDING
- **Estimated Duration**: 2 days
- **Files**: `src/infrastructure/search/simple_embedding_provider.py`
- **Tests**: `tests/unit/infrastructure/search/test_simple_embedding_provider.py`
- **Acceptance**: Deterministic embeddings for testing, swappable for real provider

**Sub-tasks:**

- [ ] **TF-IDF Based Provider**
  - [ ] RED: `test_tfidf_provider.py` - embed_text returns fixed-dim vector; similar texts have high similarity; different texts have low similarity; empty text handled; deterministic
  - [ ] GREEN: Implement TF-IDF vectorizer
  - [ ] REFACTOR: Add vocabulary persistence

- [ ] **Provider Swapping**
  - [ ] RED: `test_provider_swap.py` - can swap providers at runtime; dimension mismatch raises; re-index triggered on swap
  - [ ] GREEN: Implement provider management
  - [ ] REFACTOR: Add migration path docs

---

#### TASK-203-04: Semantic Index Contract Tests

- **Status**: PENDING
- **Estimated Duration**: 1-2 days
- **Files**: `tests/contract/search/`
- **Tests**: Contract tests
- **Acceptance**: All contracts pass, provider-agnostic

**Sub-tasks:**

- [ ] **Contract Test Suite**
  - [ ] RED: `test_semantic_index_contract.py` - all methods implemented; return types match; search results ranked; concurrent access safe
  - [ ] GREEN: Implement contract tests
  - [ ] REFACTOR: Add latency benchmarks

- [ ] **Work Tracker Semantic Integration**
  - [ ] RED: `test_wt_semantic.py` - task titles indexed; search finds similar tasks; tag-based boosting; description included
  - [ ] GREEN: Implement WT semantic indexing
  - [ ] REFACTOR: Add relevance tuning

---

### WORK-204: RDF Serialization - RDFLib Adapter

- **Status**: PENDING
- **Duration**: Weeks 15-16
- **Dependencies**: WORK-202, WORK-203
- **TASKs**: 5
- **Acceptance**: Export to Turtle/JSON-LD, SPARQL queries work, round-trip preserves data
- **Reference**: [Unified Design §5.6](../design/work-034-e-003-unified-design.md#56-irdfserializer)

---

#### TASK-204-01: RDF Serializer Port Definition

- **Status**: PENDING
- **Estimated Duration**: 1-2 days
- **Files**: `src/domain/ports/rdf_serializer.py`
- **Tests**: `tests/unit/domain/ports/test_rdf_serializer.py`
- **Acceptance**: Export/import methods defined, format-agnostic

**Sub-tasks:**

- [ ] **IRDFSerializer Port**
  - [ ] RED: `test_rdf_serializer_port.py` - serialize_entity(entity) returns triples; serialize_graph(entities) returns graph; deserialize(triples); export(format); import_file(path); ABC enforcement
  - [ ] GREEN: Implement abstract port interface
  - [ ] REFACTOR: Add namespace management

- [ ] **Jerry Ontology Definition**
  - [ ] RED: `test_jerry_ontology.py` - Task class defined; Phase class defined; Plan class defined; relationships typed; properties have domains/ranges
  - [ ] GREEN: Implement `src/domain/ontology/jerry.ttl`
  - [ ] REFACTOR: Add OWL reasoning support

---

#### TASK-204-02: RDFLib Adapter Implementation

- **Status**: PENDING
- **Estimated Duration**: 3-4 days
- **Files**: `src/infrastructure/rdf/rdflib_serializer.py`
- **Tests**: `tests/integration/rdf/test_rdflib_serializer.py`
- **Acceptance**: All formats supported, namespace handling correct

**Sub-tasks:**

- [ ] **Entity Serialization**
  - [ ] RED: `test_rdflib_serialize.py` - Task serializes to triples; Phase serializes with relationships; Plan includes nested; null properties omitted; URI encoding correct
  - [ ] GREEN: Implement entity serializers
  - [ ] REFACTOR: Add blank node handling

- [ ] **Graph Operations**
  - [ ] RED: `test_rdflib_graph.py` - multiple entities merged; no duplicate triples; relationships connected; namespaces declared; graph stats available
  - [ ] GREEN: Implement graph building
  - [ ] REFACTOR: Add named graphs support

- [ ] **Format Export**
  - [ ] RED: `test_rdflib_export.py` - Turtle format works; JSON-LD works; N-Triples works; pretty-print option; streaming for large graphs
  - [ ] GREEN: Implement format exporters
  - [ ] REFACTOR: Add compression option

- [ ] **Format Import**
  - [ ] RED: `test_rdflib_import.py` - parse Turtle; parse JSON-LD; invalid format raises; missing namespace handled; entity reconstruction
  - [ ] GREEN: Implement format importers
  - [ ] REFACTOR: Add validation mode

---

#### TASK-204-03: SPARQL Query Support

- **Status**: PENDING
- **Estimated Duration**: 2-3 days
- **Files**: `src/infrastructure/rdf/sparql_executor.py`
- **Tests**: `tests/integration/rdf/test_sparql_executor.py`
- **Acceptance**: SELECT/ASK/CONSTRUCT queries work, variables bound correctly

**Sub-tasks:**

- [ ] **Query Execution**
  - [ ] RED: `test_sparql_select.py` - SELECT returns bindings; WHERE filters; OPTIONAL works; FILTER expressions; ORDER BY; LIMIT/OFFSET; aggregate functions
  - [ ] GREEN: Implement SELECT queries
  - [ ] REFACTOR: Add query optimization hints

- [ ] **ASK/CONSTRUCT Queries**
  - [ ] RED: `test_sparql_ask_construct.py` - ASK returns boolean; CONSTRUCT returns new graph; template expansion; UNION handling
  - [ ] GREEN: Implement ASK/CONSTRUCT
  - [ ] REFACTOR: Add result caching

- [ ] **Query Security**
  - [ ] RED: `test_sparql_security.py` - query timeout enforced; depth limit; result size limit; injection prevention; allowed patterns only
  - [ ] GREEN: Implement security constraints
  - [ ] REFACTOR: Add audit logging

---

#### TASK-204-04: Work Tracker RDF Export

- **Status**: PENDING
- **Estimated Duration**: 2 days
- **Files**: `src/application/commands/export/`, `src/application/queries/export/`
- **Tests**: `tests/integration/application/test_rdf_export.py`
- **Acceptance**: Full WT export works, relationships preserved, importable

**Sub-tasks:**

- [ ] **Export Command**
  - [ ] RED: `test_export_command.py` - ExportToRDFCommand specifies format/entities/path; handler creates file; streaming for large exports; progress callback
  - [ ] GREEN: Implement export command/handler
  - [ ] REFACTOR: Add incremental export

- [ ] **Import Query**
  - [ ] RED: `test_import_query.py` - ImportFromRDFQuery specifies path/merge_strategy; handler parses and creates entities; conflict resolution; validation errors reported
  - [ ] GREEN: Implement import query/handler
  - [ ] REFACTOR: Add dry-run mode

---

#### TASK-204-05: Phase 2 Gate & Integration Tests

- **Status**: PENDING
- **Estimated Duration**: 2 days
- **Files**: `tests/system/infrastructure/`
- **Tests**: System tests
- **Acceptance**: All infrastructure components integrated, quality gates pass

**Sub-tasks:**

- [ ] **Cross-Infrastructure Integration**
  - [ ] RED: `test_infrastructure_integration.py` - event→graph projection works; graph→semantic indexing works; semantic→RDF export works; full pipeline end-to-end
  - [ ] GREEN: Implement integration tests
  - [ ] REFACTOR: Add orchestration service

- [ ] **Phase 2 Go/No-Go Gate Checklist**
  - [ ] All unit tests pass (95%+ coverage)
  - [ ] All integration tests pass
  - [ ] All contract tests pass
  - [ ] Event Store append < 10ms p95
  - [ ] Graph traversal < 50ms p95
  - [ ] Semantic search < 100ms p95
  - [ ] RDF export < 1s for 1000 entities
  - [ ] No memory leaks in 24hr run

---

## Phase 3: Knowledge Management Integration (Weeks 17-24)

> **Goal**: Implement KM domain entities and connect to Work Tracker through events.
> **Reference**: [Unified Design §11 Phase 3](../design/work-034-e-003-unified-design.md#phase-3-knowledge-management-integration-weeks-17-24)

---

### WORK-301: KM Domain Layer - Entities & Value Objects

- **Status**: PENDING
- **Duration**: Weeks 17-18
- **Dependencies**: Phase 2 complete
- **TASKs**: 4
- **Acceptance**: All KM entities defined, events emit, architecture tests pass
- **Reference**: [Unified Design §10.4](../design/work-034-e-003-unified-design.md#104-knowledgeitem-aggregate)

---

#### TASK-301-01: KM Value Objects

- **Status**: PENDING
- **Estimated Duration**: 2 days
- **Files**: `src/domain/value_objects/knowledge/`
- **Tests**: `tests/unit/domain/value_objects/knowledge/`
- **Acceptance**: All VOs immutable, validated, 100% coverage

**Sub-tasks:**

- [ ] **KnowledgeId Value Object** (`knowledge_id.py`)
  - [ ] RED: `test_knowledge_id.py` - PAT-NNN format for patterns; LES-NNN for lessons; ASM-NNN for assumptions; type prefix validation; empty/invalid rejected
  - [ ] GREEN: Implement with format validation
  - [ ] REFACTOR: Add type inference from prefix

- [ ] **Evidence Value Object** (`evidence.py`)
  - [ ] RED: `test_evidence.py` - type enum (TASK_COMPLETION, USER_FEEDBACK, PATTERN_MATCH); source reference; confidence 0.0-1.0; timestamp; immutable; invalid confidence raises
  - [ ] GREEN: Implement Evidence dataclass
  - [ ] REFACTOR: Add evidence chain support

- [ ] **EvidenceType Enum** (`evidence_type.py`)
  - [ ] RED: `test_evidence_type.py` - all types defined; from_string parsing; display names; ordering by strength
  - [ ] GREEN: Implement enum
  - [ ] REFACTOR: Add confidence multipliers

- [ ] **Confidence Value Object** (`confidence.py`)
  - [ ] RED: `test_confidence.py` - 0.0-1.0 range; combine() aggregates; decay over time; boost with new evidence; string formatting (Low/Medium/High)
  - [ ] GREEN: Implement Confidence class
  - [ ] REFACTOR: Add probability operations

---

#### TASK-301-02: KnowledgeItem Aggregate Root

- **Status**: PENDING
- **Estimated Duration**: 3-4 days
- **Files**: `src/domain/aggregates/knowledge_item.py`
- **Tests**: `tests/unit/domain/aggregates/test_knowledge_item.py`
- **Acceptance**: Full lifecycle, evidence tracking, type-specific behavior

**Sub-tasks:**

- [ ] **KnowledgeItem Core**
  - [ ] RED: Create with content/type/tags; auto-generated ID; evidence list; confidence calculated; empty content rejected; long content truncated
  - [ ] GREEN: Implement `KnowledgeItem.__init__()` and factory
  - [ ] REFACTOR: Add content normalization

- [ ] **Evidence Management**
  - [ ] RED: `add_evidence()` appends, emits event; `get_evidence()` returns list; confidence recalculated; duplicate evidence no-op; expired evidence filtered
  - [ ] GREEN: Implement evidence methods
  - [ ] REFACTOR: Add evidence expiration policy

- [ ] **Type-Specific Behavior**
  - [ ] RED: Pattern requires example_count > 0; Lesson requires outcome (POSITIVE/NEGATIVE/NEUTRAL); Assumption requires validation_status; type-specific factories
  - [ ] GREEN: Implement type-specific validation
  - [ ] REFACTOR: Use strategy pattern for types

- [ ] **Knowledge Linking**
  - [ ] RED: `link_to(other_id, relationship)` creates link, emits event; `get_links()` returns relationships; circular link detection; unlink removes; duplicate link no-op
  - [ ] GREEN: Implement linking methods
  - [ ] REFACTOR: Add relationship types enum

---

#### TASK-301-03: KM Domain Events

- **Status**: PENDING
- **Estimated Duration**: 2 days
- **Files**: `src/domain/events/knowledge.py`
- **Tests**: `tests/unit/domain/events/test_knowledge_events.py`
- **Acceptance**: CloudEvents compliant, all mutations emit events

**Sub-tasks:**

- [ ] **KM Event Definitions**
  - [ ] RED: `test_km_events.py` - KnowledgeItemCreated; KnowledgeItemUpdated; EvidenceAdded; ConfidenceChanged; KnowledgeLinked; KnowledgeArchived; all in envelope
  - [ ] GREEN: Implement event classes
  - [ ] REFACTOR: Add event factories

- [ ] **Cross-Domain Events**
  - [ ] RED: `test_cross_domain_events.py` - TaskCompletedTriggersAAR; PatternSuggested; LessonExtracted; AssumptionValidated; source tracking
  - [ ] GREEN: Implement cross-domain events
  - [ ] REFACTOR: Add correlation ID propagation

---

#### TASK-301-04: KM Architecture Tests

- **Status**: PENDING
- **Estimated Duration**: 1-2 days
- **Files**: `tests/architecture/test_km_architecture.py`
- **Tests**: Architecture tests
- **Acceptance**: All DDD patterns enforced, no layer violations

**Sub-tasks:**

- [ ] **KM Layer Tests**
  - [ ] RED: `test_km_layers.py` - km domain no application imports; VOs frozen; aggregate methods return self or VO; events immutable; no infrastructure leakage
  - [ ] GREEN: Implement architecture tests
  - [ ] REFACTOR: Add pattern detector

- [ ] **Integration Boundary Tests**
  - [ ] RED: `test_km_boundaries.py` - WT→KM via events only; no direct aggregate access; port interface between domains; shared kernel only for VOs
  - [ ] GREEN: Implement boundary tests
  - [ ] REFACTOR: Document bounded context map

---

### WORK-302: KM Repository Layer - Ports & SQLite Adapter

- **Status**: PENDING
- **Duration**: Weeks 19-20
- **Dependencies**: WORK-301
- **TASKs**: 3
- **Acceptance**: Full CRUD for KM entities, integration tests pass
- **Reference**: [Unified Design §5.2](../design/work-034-e-003-unified-design.md#52-iknowledgerepository)

---

#### TASK-302-01: KM Repository Port

- **Status**: PENDING
- **Estimated Duration**: 1-2 days
- **Files**: `src/domain/ports/knowledge_repository.py`
- **Tests**: `tests/unit/domain/ports/test_knowledge_repository.py`
- **Acceptance**: All methods abstract, typed, documented

**Sub-tasks:**

- [ ] **IKnowledgeRepository Port**
  - [ ] RED: `test_knowledge_repo_port.py` - get(id); save(item); delete(id); list_by_type(type); list_by_tag(tag); search_by_content(query); ABC enforcement
  - [ ] GREEN: Implement abstract port
  - [ ] REFACTOR: Add batch operations

- [ ] **Query Specifications**
  - [ ] RED: `test_km_query_specs.py` - KMQuerySpec has filters; by_type; by_tags_any/all; by_confidence_min; by_date_range; combine with AND/OR
  - [ ] GREEN: Implement specification pattern
  - [ ] REFACTOR: Add fluent builder

---

#### TASK-302-02: SQLite KM Repository Adapter

- **Status**: PENDING
- **Estimated Duration**: 3-4 days
- **Files**: `src/infrastructure/persistence/sqlite_knowledge_repo.py`, `migrations/003_knowledge_schema.sql`
- **Tests**: `tests/integration/persistence/test_sqlite_knowledge_repo.py`
- **Acceptance**: Full CRUD, evidence stored, full-text search works

**Sub-tasks:**

- [ ] **KM Schema Migration**
  - [ ] RED: knowledge_items table; evidence table (FK); tags junction; links table; FTS index on content; idempotent
  - [ ] GREEN: Implement migration
  - [ ] REFACTOR: Add index optimization

- [ ] **Knowledge CRUD**
  - [ ] RED: `test_sqlite_knowledge_crud.py` - save inserts/updates; get returns/None; delete removes; list by type; list by tag; cascade evidence; version incremented
  - [ ] GREEN: Implement CRUD methods
  - [ ] REFACTOR: Add lazy loading for evidence

- [ ] **Full-Text Search**
  - [ ] RED: `test_sqlite_km_fts.py` - search content returns ranked; snippet extraction; highlight matches; no results returns empty; special chars escaped
  - [ ] GREEN: Implement FTS5 integration
  - [ ] REFACTOR: Add relevance tuning

- [ ] **Link Operations**
  - [ ] RED: `test_sqlite_km_links.py` - save link; get outgoing; get incoming; bidirectional queries; delete cascades; orphan detection
  - [ ] GREEN: Implement link operations
  - [ ] REFACTOR: Add link type constraints

---

#### TASK-302-03: KM Repository Contract Tests

- **Status**: PENDING
- **Estimated Duration**: 1-2 days
- **Files**: `tests/contract/persistence/test_knowledge_repo_contract.py`
- **Tests**: Contract tests
- **Acceptance**: All contracts pass, adapter-agnostic

**Sub-tasks:**

- [ ] **Contract Test Suite**
  - [ ] RED: All port methods implemented; return types match; exceptions match; search behavior consistent
  - [ ] GREEN: Implement contract tests
  - [ ] REFACTOR: Parameterize for adapters

- [ ] **Cross-Repository Tests**
  - [ ] RED: `test_cross_repo.py` - WT task references KM item; KM item references WT task; foreign key via JerryURI; integrity maintained
  - [ ] GREEN: Implement cross-repo tests
  - [ ] REFACTOR: Add cascade options

---

### WORK-303: KM CQRS Implementation - Commands, Queries, Handlers

- **Status**: PENDING
- **Duration**: Weeks 21-22
- **Dependencies**: WORK-301, WORK-302
- **TASKs**: 5
- **Acceptance**: All KM operations via CQRS, AAR flow works
- **Reference**: [Unified Design §6.3-6.4](../design/work-034-e-003-unified-design.md#63-km-commands)

---

#### TASK-303-01: KM Commands & Handlers

- **Status**: PENDING
- **Estimated Duration**: 3 days
- **Files**: `src/application/commands/km/`, `src/application/handlers/commands/km/`
- **Tests**: `tests/unit/application/commands/km/`, `tests/unit/application/handlers/km/`
- **Acceptance**: All KM commands functional, events dispatched

**Sub-tasks:**

- [ ] **KM Command Definitions**
  - [ ] RED: `test_km_commands.py` - CreateKnowledgeItemCommand; UpdateKnowledgeItemCommand; AddEvidenceCommand; LinkKnowledgeCommand; ArchiveKnowledgeCommand; immutable; validation
  - [ ] GREEN: Implement command dataclasses
  - [ ] REFACTOR: Add builders

- [ ] **Create/Update Handlers**
  - [ ] RED: `test_km_create_handler.py` - creates via factory; saves; dispatches event; returns ID; duplicate detection; type validation
  - [ ] RED: `test_km_update_handler.py` - fetches; updates; saves; dispatches; not found raises
  - [ ] GREEN: Implement handlers
  - [ ] REFACTOR: Extract base handler

- [ ] **Evidence Handler**
  - [ ] RED: `test_add_evidence_handler.py` - fetches item; adds evidence; recalculates confidence; saves; dispatches EvidenceAdded; not found raises
  - [ ] GREEN: Implement handler
  - [ ] REFACTOR: Add evidence validation

- [ ] **Link Handler**
  - [ ] RED: `test_link_handler.py` - validates both IDs exist; creates link; dispatches KnowledgeLinked; circular detection; already linked no-op
  - [ ] GREEN: Implement handler
  - [ ] REFACTOR: Add relationship constraints

---

#### TASK-303-02: KM Queries & Handlers

- **Status**: PENDING
- **Estimated Duration**: 2-3 days
- **Files**: `src/application/queries/km/`, `src/application/handlers/queries/km/`
- **Tests**: `tests/unit/application/queries/km/`, `tests/unit/application/handlers/queries/km/`
- **Acceptance**: All KM queries return DTOs, search works

**Sub-tasks:**

- [ ] **KM DTOs**
  - [ ] RED: `test_km_dtos.py` - KnowledgeItemDTO; EvidenceDTO; LinkDTO; from_entity factories; immutable; serializable
  - [ ] GREEN: Implement DTOs
  - [ ] REFACTOR: Add projection methods

- [ ] **KM Query Definitions**
  - [ ] RED: `test_km_queries.py` - GetKnowledgeItemQuery; ListKnowledgeItemsQuery with filters; SearchKnowledgeQuery; GetRelatedKnowledgeQuery; GetKnowledgeGraphQuery
  - [ ] GREEN: Implement query dataclasses
  - [ ] REFACTOR: Add pagination

- [ ] **KM Query Handlers**
  - [ ] RED: `test_km_query_handlers.py` - get returns DTO/None; list applies filters; search ranks results; related follows links; graph returns structure
  - [ ] GREEN: Implement handlers
  - [ ] REFACTOR: Add caching

---

#### TASK-303-03: After Action Review (AAR) Flow

- **Status**: PENDING
- **Estimated Duration**: 3 days
- **Files**: `src/application/event_handlers/aar_handler.py`, `src/application/commands/km/aar_commands.py`
- **Tests**: `tests/integration/application/test_aar_flow.py`
- **Acceptance**: Task completion triggers AAR prompt, lessons captured

**Sub-tasks:**

- [ ] **AAR Trigger Handler**
  - [ ] RED: `test_aar_trigger.py` - TaskCompleted triggers AAR prompt; PhaseCompleted triggers summary; configurable delay; opt-out respected; repeat suppression
  - [ ] GREEN: Implement AARTriggerHandler
  - [ ] REFACTOR: Add user preference storage

- [ ] **AAR Capture Commands**
  - [ ] RED: `test_aar_capture.py` - CaptureAARCommand has task_id/lessons/patterns; creates KnowledgeItems; links to task; evidence from task completion
  - [ ] GREEN: Implement AAR capture
  - [ ] REFACTOR: Add template suggestions

- [ ] **AAR Skip/Defer**
  - [ ] RED: `test_aar_skip.py` - SkipAARCommand records skip; DeferAARCommand schedules later; skip reason tracked; analytics for adoption
  - [ ] GREEN: Implement skip/defer
  - [ ] REFACTOR: Add reminder system

---

#### TASK-303-04: Cross-Domain Event Handlers

- **Status**: PENDING
- **Estimated Duration**: 2 days
- **Files**: `src/application/event_handlers/cross_domain/`
- **Tests**: `tests/integration/application/test_cross_domain_handlers.py`
- **Acceptance**: WT events trigger KM actions, bidirectional

**Sub-tasks:**

- [ ] **WT→KM Handlers**
  - [ ] RED: `test_wt_to_km_handlers.py` - TaskCompleted→AARPrompt; PatternDetected→PatternSuggestion; PlanCompleted→LessonsSummary; idempotent
  - [ ] GREEN: Implement WT→KM handlers
  - [ ] REFACTOR: Add handler registry

- [ ] **KM→WT Handlers**
  - [ ] RED: `test_km_to_wt_handlers.py` - PatternMatched→TaskSuggestion; LessonRelevant→TaskAnnotation; AssumptionInvalidated→TaskWarning
  - [ ] GREEN: Implement KM→WT handlers
  - [ ] REFACTOR: Add relevance scoring

---

#### TASK-303-05: KM CQRS Integration Tests

- **Status**: PENDING
- **Estimated Duration**: 2 days
- **Files**: `tests/integration/application/test_km_cqrs_integration.py`
- **Tests**: Integration tests
- **Acceptance**: Full CQRS lifecycle works, cross-domain events propagate

**Sub-tasks:**

- [ ] **KM Lifecycle Tests**
  - [ ] RED: `test_km_lifecycle.py` - create→query; update→query shows changes; add evidence→confidence changes; archive→not in list; full lifecycle
  - [ ] GREEN: Implement lifecycle tests
  - [ ] REFACTOR: Add data generators

- [ ] **Cross-Domain Integration**
  - [ ] RED: `test_cross_domain_integration.py` - complete task→AAR→lesson created; lesson linked to task; query shows relationship; graph includes both
  - [ ] GREEN: Implement cross-domain tests
  - [ ] REFACTOR: Add saga testing

---

### WORK-304: KM Interface Layer - CLI & SKILL.md

- **Status**: PENDING
- **Duration**: Weeks 23-24
- **Dependencies**: WORK-303
- **TASKs**: 4
- **Acceptance**: Full KM operations via CLI, natural language patterns work
- **Reference**: [Unified Design §7.2](../design/work-034-e-003-unified-design.md#72-km-cli)

---

#### TASK-304-01: KM CLI Implementation

- **Status**: PENDING
- **Estimated Duration**: 3-4 days
- **Files**: `src/interface/cli/km_cli.py`
- **Tests**: `tests/e2e/cli/test_km_cli.py`
- **Acceptance**: All KM commands work, output formats correct

**Sub-tasks:**

- [ ] **KM CLI Entry Point**
  - [ ] RED: `test_km_cli.py` - `km --help` shows usage; `--version`; exit codes; unknown command error; subcommand routing
  - [ ] GREEN: Implement main CLI
  - [ ] REFACTOR: Add rich formatting

- [ ] **Knowledge Subcommand**
  - [ ] RED: `test_km_knowledge_cli.py` - `create --type pattern "content"`; `list --type lesson`; `show <id>`; `search "query"`; `link <id1> <id2> --rel references`; `--json`
  - [ ] GREEN: Implement knowledge subcommand
  - [ ] REFACTOR: Add autocomplete

- [ ] **AAR Subcommand**
  - [ ] RED: `test_km_aar_cli.py` - `aar capture --task <id> --lesson "text"`; `aar pending` lists; `aar skip <task_id> --reason`; `aar defer <task_id>`
  - [ ] GREEN: Implement AAR subcommand
  - [ ] REFACTOR: Add interactive mode

- [ ] **Export/Import Subcommand**
  - [ ] RED: `test_km_export_cli.py` - `export --format turtle --output file.ttl`; `import file.ttl --merge`; progress indicator; error summary
  - [ ] GREEN: Implement export/import
  - [ ] REFACTOR: Add streaming

---

#### TASK-304-02: KM SKILL.md

- **Status**: PENDING
- **Estimated Duration**: 1-2 days
- **Files**: `skills/km/SKILL.md`
- **Tests**: Manual verification
- **Acceptance**: Natural language patterns work, examples clear

**Sub-tasks:**

- [ ] **Skill Documentation**
  - [ ] Create `skills/km/SKILL.md`
  - [ ] Document knowledge CRUD patterns
  - [ ] Document AAR capture patterns
  - [ ] Document search patterns
  - [ ] Document export/import patterns
  - [ ] Add troubleshooting section
  - [ ] Add integration with WT skill

---

#### TASK-304-03: KM BDD Test Suite

- **Status**: PENDING
- **Estimated Duration**: 3 days
- **Files**: `tests/bdd/km/`
- **Tests**: Feature files + step definitions
- **Acceptance**: All scenarios pass, real implementations

**Sub-tasks:**

- [ ] **Knowledge Feature File** (`features/knowledge.feature`)
  - [ ] Scenario: Create pattern from task experience
  - [ ] Scenario: Create lesson from task completion
  - [ ] Scenario: Add evidence to knowledge item
  - [ ] Scenario: Link related knowledge items
  - [ ] Scenario: Search knowledge by content
  - [ ] Edge: Create knowledge with max evidence
  - [ ] Negative: Create with invalid type fails

- [ ] **AAR Feature File** (`features/aar.feature`)
  - [ ] Scenario: Complete task triggers AAR prompt
  - [ ] Scenario: Capture lessons from AAR
  - [ ] Scenario: Skip AAR with reason
  - [ ] Scenario: Defer AAR to later
  - [ ] Negative: Capture AAR for non-existent task fails

- [ ] **Step Definitions**
  - [ ] `steps/knowledge_steps.py` - REAL implementations
  - [ ] `steps/aar_steps.py` - REAL implementations

---

#### TASK-304-04: Phase 3 Gate & Integration

- **Status**: PENDING
- **Estimated Duration**: 2 days
- **Files**: `tests/system/km/`
- **Tests**: System tests
- **Acceptance**: All quality gates pass, cross-domain works

**Sub-tasks:**

- [ ] **System Tests**
  - [ ] RED: `test_km_system.py` - full WT→KM flow; create plan→complete tasks→capture lessons→search; persistence across sessions; concurrent access
  - [ ] GREEN: Implement system tests
  - [ ] REFACTOR: Add load testing

- [ ] **Phase 3 Go/No-Go Gate Checklist**
  - [ ] All unit tests pass (95%+ coverage)
  - [ ] All integration tests pass
  - [ ] All BDD scenarios pass
  - [ ] All E2E tests pass
  - [ ] AAR capture < 200ms p95
  - [ ] Knowledge search < 100ms p95
  - [ ] Cross-domain events < 50ms propagation
  - [ ] AAR adoption rate tracking in place

---

## Phase 4: Advanced Features (Weeks 25-32)

> **Goal**: Implement HybridRAG, pattern discovery, external API, and final documentation.
> **Reference**: [Unified Design §11 Phase 4](../design/work-034-e-003-unified-design.md#phase-4-advanced-features-weeks-25-32)

---

### WORK-401: Cross-Domain Integration - Enhanced Handlers

- **Status**: PENDING
- **Duration**: Weeks 25-26
- **Dependencies**: Phase 3 complete
- **TASKs**: 4
- **Acceptance**: Bidirectional flow works, graph enriched, queries unified
- **Reference**: [Unified Design §8](../design/work-034-e-003-unified-design.md#8-integration-architecture)

---

#### TASK-401-01: Enhanced Graph Integration

- **Status**: PENDING
- **Estimated Duration**: 3 days
- **Files**: `src/application/services/unified_graph_service.py`
- **Tests**: `tests/integration/application/test_unified_graph.py`
- **Acceptance**: WT + KM in single graph, traversals work across domains

**Sub-tasks:**

- [ ] **Unified Graph Service**
  - [ ] RED: `test_unified_graph_service.py` - get_task_with_knowledge(id); get_pattern_with_tasks(id); traverse_cross_domain(start, depth); path_between_domains(wt_id, km_id)
  - [ ] GREEN: Implement UnifiedGraphService
  - [ ] REFACTOR: Add query optimization

- [ ] **Graph Materialization**
  - [ ] RED: `test_graph_materialization.py` - materialize_task_knowledge_links(); refresh_on_event(); incremental updates; full rebuild option
  - [ ] GREEN: Implement materialization
  - [ ] REFACTOR: Add background refresh

- [ ] **Cross-Domain Queries**
  - [ ] RED: `test_cross_domain_queries.py` - "Find patterns related to my active tasks"; "Find tasks that used this lesson"; "Show knowledge graph for plan"
  - [ ] GREEN: Implement cross-domain query handlers
  - [ ] REFACTOR: Add query templates

---

#### TASK-401-02: Enriched Query Handlers

- **Status**: PENDING
- **Estimated Duration**: 2-3 days
- **Files**: `src/application/handlers/queries/enriched/`
- **Tests**: `tests/unit/application/handlers/queries/test_enriched_queries.py`
- **Acceptance**: Queries return enriched data from multiple sources

**Sub-tasks:**

- [ ] **Task with Knowledge Query**
  - [ ] RED: `test_task_with_knowledge.py` - GetTaskWithKnowledgeQuery returns TaskDTO + related patterns/lessons; confidence scores; source links
  - [ ] GREEN: Implement enriched handler
  - [ ] REFACTOR: Add lazy loading

- [ ] **Knowledge with Context Query**
  - [ ] RED: `test_knowledge_with_context.py` - GetKnowledgeWithContextQuery returns KnowledgeDTO + source tasks + usage history + related items
  - [ ] GREEN: Implement enriched handler
  - [ ] REFACTOR: Add context window

- [ ] **Dashboard Query**
  - [ ] RED: `test_dashboard_query.py` - GetDashboardQuery returns tasks summary + recent knowledge + patterns trending + lessons applied
  - [ ] GREEN: Implement dashboard handler
  - [ ] REFACTOR: Add caching

---

#### TASK-401-03: Event Saga Implementation

- **Status**: PENDING
- **Estimated Duration**: 2-3 days
- **Files**: `src/application/sagas/`
- **Tests**: `tests/integration/application/test_sagas.py`
- **Acceptance**: Multi-step operations atomic, compensation works

**Sub-tasks:**

- [ ] **Saga Coordinator**
  - [ ] RED: `test_saga_coordinator.py` - execute_saga(steps); step failure triggers compensation; partial rollback; idempotent steps; timeout handling
  - [ ] GREEN: Implement SagaCoordinator
  - [ ] REFACTOR: Add saga persistence

- [ ] **Task Completion Saga**
  - [ ] RED: `test_task_completion_saga.py` - complete task→update graph→trigger AAR→create knowledge; any failure rolls back; partial state handled
  - [ ] GREEN: Implement TaskCompletionSaga
  - [ ] REFACTOR: Add async steps

- [ ] **Pattern Discovery Saga**
  - [ ] RED: `test_pattern_discovery_saga.py` - detect pattern→validate→create item→link sources→index; user confirmation step; rejection handling
  - [ ] GREEN: Implement PatternDiscoverySaga
  - [ ] REFACTOR: Add confidence gates

---

#### TASK-401-04: Integration Tests & Performance

- **Status**: PENDING
- **Estimated Duration**: 2 days
- **Files**: `tests/integration/cross_domain/`
- **Tests**: Integration and performance tests
- **Acceptance**: Cross-domain operations meet latency targets

**Sub-tasks:**

- [ ] **Cross-Domain Performance Tests**
  - [ ] RED: `test_cross_domain_perf.py` - cross-domain query < 150ms p95; saga completion < 500ms; graph traversal 3 hops < 100ms
  - [ ] GREEN: Implement performance tests
  - [ ] REFACTOR: Add profiling

- [ ] **Stress Tests**
  - [ ] RED: `test_cross_domain_stress.py` - 100 concurrent cross-domain queries; saga under load; event storm handling
  - [ ] GREEN: Implement stress tests
  - [ ] REFACTOR: Add circuit breaker tests

---

### WORK-402: HybridRAG & Pattern Discovery

- **Status**: PENDING
- **Duration**: Weeks 27-28
- **Dependencies**: WORK-401
- **TASKs**: 4
- **Acceptance**: Semantic + graph retrieval works, patterns discovered
- **Reference**: [Unified Design §9.1-9.2](../design/work-034-e-003-unified-design.md#91-hybridrag-architecture)

---

#### TASK-402-01: HybridRAG Service

- **Status**: PENDING
- **Estimated Duration**: 3-4 days
- **Files**: `src/application/services/hybrid_rag.py`
- **Tests**: `tests/integration/application/test_hybrid_rag.py`
- **Acceptance**: Combined semantic + graph retrieval, ranking works

**Sub-tasks:**

- [ ] **Hybrid Retrieval**
  - [ ] RED: `test_hybrid_retrieval.py` - retrieve(query) uses semantic + graph; results merged; duplicates removed; scores combined; configurable weights
  - [ ] GREEN: Implement HybridRAGService
  - [ ] REFACTOR: Add strategy pattern for retrieval

- [ ] **Re-ranking**
  - [ ] RED: `test_reranking.py` - rerank_results(query, candidates); relevance scoring; diversity promotion; recency boost; user preference weighting
  - [ ] GREEN: Implement re-ranker
  - [ ] REFACTOR: Add ML-based ranker option

- [ ] **Context Assembly**
  - [ ] RED: `test_context_assembly.py` - assemble_context(query, k); chunk selection; overlap handling; token budget; priority ordering
  - [ ] GREEN: Implement context assembler
  - [ ] REFACTOR: Add sliding window

- [ ] **Query Expansion**
  - [ ] RED: `test_query_expansion.py` - expand_query(query); synonym addition; related term discovery; entity recognition; disambiguation
  - [ ] GREEN: Implement query expansion
  - [ ] REFACTOR: Add feedback loop

---

#### TASK-402-02: Pattern Discovery Service

- **Status**: PENDING
- **Estimated Duration**: 3-4 days
- **Files**: `src/application/services/pattern_discovery.py`
- **Tests**: `tests/integration/application/test_pattern_discovery.py`
- **Acceptance**: Patterns detected from recurring behaviors, user confirmation

**Sub-tasks:**

- [ ] **Similarity Detection**
  - [ ] RED: `test_similarity_detection.py` - detect_similar_items(threshold); cluster formation; centroid calculation; outlier handling; minimum cluster size
  - [ ] GREEN: Implement similarity detector
  - [ ] REFACTOR: Add incremental clustering

- [ ] **Pattern Candidate Generation**
  - [ ] RED: `test_pattern_candidates.py` - generate_candidates(clusters); pattern template extraction; confidence scoring; source tracking; duplicate filtering
  - [ ] GREEN: Implement candidate generator
  - [ ] REFACTOR: Add template refinement

- [ ] **Pattern Validation**
  - [ ] RED: `test_pattern_validation.py` - validate_pattern(candidate); minimum evidence; user confirmation; rejection tracking; false positive rate
  - [ ] GREEN: Implement validator
  - [ ] REFACTOR: Add auto-approval threshold

- [ ] **Pattern Evolution**
  - [ ] RED: `test_pattern_evolution.py` - update_pattern_with_evidence(); merge similar patterns; split divergent patterns; deprecation tracking
  - [ ] GREEN: Implement evolution logic
  - [ ] REFACTOR: Add versioning

---

#### TASK-402-03: HybridRAG CLI Integration

- **Status**: PENDING
- **Estimated Duration**: 2 days
- **Files**: `src/interface/cli/rag_cli.py`
- **Tests**: `tests/e2e/cli/test_rag_cli.py`
- **Acceptance**: RAG queries via CLI, results formatted

**Sub-tasks:**

- [ ] **RAG Subcommand**
  - [ ] RED: `test_rag_cli.py` - `rag search "query"`; `rag context "query" --budget 2000`; `--semantic-only`; `--graph-only`; `--json`
  - [ ] GREEN: Implement RAG CLI
  - [ ] REFACTOR: Add streaming output

- [ ] **Pattern Discovery CLI**
  - [ ] RED: `test_pattern_discovery_cli.py` - `pattern discover`; `pattern candidates`; `pattern approve <id>`; `pattern reject <id> --reason`
  - [ ] GREEN: Implement pattern CLI
  - [ ] REFACTOR: Add batch operations

---

#### TASK-402-04: HybridRAG Tests & Benchmarks

- **Status**: PENDING
- **Estimated Duration**: 2 days
- **Files**: `tests/integration/application/test_rag_benchmarks.py`
- **Tests**: Benchmark tests
- **Acceptance**: Retrieval quality measured, performance targets met

**Sub-tasks:**

- [ ] **Quality Benchmarks**
  - [ ] RED: `test_rag_quality.py` - precision@k measured; recall@k measured; MRR calculated; baseline comparison; quality regression detection
  - [ ] GREEN: Implement quality benchmarks
  - [ ] REFACTOR: Add golden dataset

- [ ] **Performance Benchmarks**
  - [ ] RED: `test_rag_performance.py` - retrieval < 200ms p95; re-ranking < 50ms; context assembly < 100ms; end-to-end < 400ms p95
  - [ ] GREEN: Implement performance benchmarks
  - [ ] REFACTOR: Add continuous tracking

---

### WORK-403: External API & Export

- **Status**: PENDING
- **Duration**: Weeks 29-30
- **Dependencies**: WORK-401
- **TASKs**: 3
- **Acceptance**: SPARQL endpoint works, RDF export/import functional
- **Reference**: [Unified Design §7.3](../design/work-034-e-003-unified-design.md#73-external-api)

---

#### TASK-403-01: SPARQL Endpoint

- **Status**: PENDING
- **Estimated Duration**: 3-4 days
- **Files**: `src/interface/api/sparql_endpoint.py`
- **Tests**: `tests/integration/api/test_sparql_endpoint.py`
- **Acceptance**: SELECT/ASK/CONSTRUCT queries work, security enforced

**Sub-tasks:**

- [ ] **HTTP Endpoint**
  - [ ] RED: `test_sparql_http.py` - POST /sparql accepts query; GET /sparql with query param; content negotiation; CORS handling; rate limiting
  - [ ] GREEN: Implement HTTP handler
  - [ ] REFACTOR: Add request validation

- [ ] **Query Execution**
  - [ ] RED: `test_sparql_execution.py` - SELECT returns JSON/XML; ASK returns boolean; CONSTRUCT returns RDF; timeout enforced; error messages helpful
  - [ ] GREEN: Implement query executor
  - [ ] REFACTOR: Add query caching

- [ ] **Security**
  - [ ] RED: `test_sparql_security.py` - query whitelist; depth limit; result limit; injection blocked; unauthorized access rejected
  - [ ] GREEN: Implement security layer
  - [ ] REFACTOR: Add audit logging

---

#### TASK-403-02: Bulk Export/Import

- **Status**: PENDING
- **Estimated Duration**: 2-3 days
- **Files**: `src/application/commands/export/`, `src/application/commands/import/`
- **Tests**: `tests/integration/application/test_bulk_export_import.py`
- **Acceptance**: Large exports work, import validates, progress tracked

**Sub-tasks:**

- [ ] **Bulk Export**
  - [ ] RED: `test_bulk_export.py` - export 10,000 items; streaming output; progress callback; resume on failure; format options; compression
  - [ ] GREEN: Implement bulk exporter
  - [ ] REFACTOR: Add parallel processing

- [ ] **Bulk Import**
  - [ ] RED: `test_bulk_import.py` - import 10,000 items; validation pass; conflict resolution; transaction batching; error report; rollback option
  - [ ] GREEN: Implement bulk importer
  - [ ] REFACTOR: Add dry-run mode

- [ ] **Export/Import CLI**
  - [ ] RED: `test_export_import_cli.py` - `export --format turtle --output data.ttl --all`; `import data.ttl --validate-only`; `--merge`; progress bar
  - [ ] GREEN: Implement CLI commands
  - [ ] REFACTOR: Add scheduling option

---

#### TASK-403-03: API Contract Tests

- **Status**: PENDING
- **Estimated Duration**: 1-2 days
- **Files**: `tests/contract/api/`
- **Tests**: Contract tests
- **Acceptance**: API contracts verified, backwards compatible

**Sub-tasks:**

- [ ] **SPARQL Contract Tests**
  - [ ] RED: `test_sparql_contract.py` - endpoint response format; error codes; content types; pagination; versioning
  - [ ] GREEN: Implement contract tests
  - [ ] REFACTOR: Add OpenAPI spec

- [ ] **Export Contract Tests**
  - [ ] RED: `test_export_contract.py` - export format validates; import format validates; round-trip preserves; version migration
  - [ ] GREEN: Implement contract tests
  - [ ] REFACTOR: Add schema evolution tests

---

### WORK-404: Documentation & Final Testing

- **Status**: PENDING
- **Duration**: Weeks 31-32
- **Dependencies**: All previous WORK items
- **TASKs**: 3
- **Acceptance**: Documentation complete, all gates pass, release ready
- **Reference**: [Unified Design §11 Phase 4](../design/work-034-e-003-unified-design.md#phase-4-advanced-features-weeks-25-32)

---

#### TASK-404-01: User Documentation

- **Status**: PENDING
- **Estimated Duration**: 3-4 days
- **Files**: `docs/user-guide/`
- **Tests**: Manual verification
- **Acceptance**: All features documented, examples work, getting started guide complete

**Sub-tasks:**

- [ ] **Getting Started Guide**
  - [ ] `docs/user-guide/getting-started.md` - installation, first task, first knowledge item, AAR walkthrough
  - [ ] Verify all commands work
  - [ ] Add troubleshooting section

- [ ] **Work Tracker Guide**
  - [ ] `docs/user-guide/work-tracker.md` - task lifecycle, phase management, plan creation, CLI reference
  - [ ] Add diagrams
  - [ ] Add best practices

- [ ] **Knowledge Management Guide**
  - [ ] `docs/user-guide/knowledge-management.md` - patterns/lessons/assumptions, evidence, linking, AAR
  - [ ] Add examples
  - [ ] Add integration patterns

- [ ] **Advanced Features Guide**
  - [ ] `docs/user-guide/advanced.md` - HybridRAG, SPARQL, export/import, pattern discovery
  - [ ] Add query examples
  - [ ] Add performance tips

- [ ] **API Reference**
  - [ ] `docs/api/` - CLI reference, SPARQL reference, export formats
  - [ ] Generate from code where possible
  - [ ] Add examples for each endpoint

---

#### TASK-404-02: Final Integration Testing

- **Status**: PENDING
- **Estimated Duration**: 3-4 days
- **Files**: `tests/system/final/`
- **Tests**: System and E2E tests
- **Acceptance**: All workflows pass, no regressions

**Sub-tasks:**

- [ ] **Full Workflow Tests**
  - [ ] RED: `test_full_workflow.py` - create plan→phases→tasks→complete→AAR→lessons→patterns→export→import→search
  - [ ] GREEN: Implement full workflow test
  - [ ] REFACTOR: Add data cleanup

- [ ] **Regression Test Suite**
  - [ ] RED: `test_regression_suite.py` - all Phase 1-4 gates re-verified; no degradation; performance within bounds
  - [ ] GREEN: Implement regression suite
  - [ ] REFACTOR: Add CI integration

- [ ] **Load Testing**
  - [ ] RED: `test_load.py` - 1000 concurrent users; 10,000 tasks; 5,000 knowledge items; sustained load 1hr; memory stable
  - [ ] GREEN: Implement load tests
  - [ ] REFACTOR: Add profiling report

- [ ] **Security Testing**
  - [ ] RED: `test_security.py` - injection tests; authorization tests; data isolation; audit trail; OWASP top 10 checks
  - [ ] GREEN: Implement security tests
  - [ ] REFACTOR: Add penetration test prep

---

#### TASK-404-03: Release Preparation

- **Status**: PENDING
- **Estimated Duration**: 2 days
- **Files**: Various
- **Tests**: Release checklist
- **Acceptance**: Release artifacts ready, changelog complete

**Sub-tasks:**

- [ ] **Final Gate Checklist**
  - [ ] All 845+ tests pass
  - [ ] Coverage > 90%
  - [ ] All BDD scenarios pass
  - [ ] All contract tests pass
  - [ ] All architecture tests pass
  - [ ] Performance targets met
  - [ ] Security review approved
  - [ ] Documentation reviewed

- [ ] **Release Artifacts**
  - [ ] `CHANGELOG.md` updated
  - [ ] Version bumped
  - [ ] Migration guide if needed
  - [ ] Release notes drafted

- [ ] **Deployment Preparation**
  - [ ] CI/CD pipeline verified
  - [ ] Rollback procedure documented
  - [ ] Monitoring configured
  - [ ] Alerting configured

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| WORK Items | 16 |
| TASKs | 64 |
| Estimated Sub-tasks | ~400 |
| Estimated Tests | ~845 |
| Duration | 32 weeks |

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
