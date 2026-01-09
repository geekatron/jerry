# Jerry Framework - Implementation Work Tracker (Proposed)

> Granular implementation plan derived from ADR-034 unified design.
> **Source**: [ADR-034](../decisions/ADR-034-unified-wt-km-implementation.md) | [Unified Design](../design/work-034-e-003-unified-design.md)

**Created**: 2026-01-09
**Revised**: 2026-01-09
**Status**: PROPOSED (awaiting approval)
**Total Duration**: 32 weeks (4 phases)
**Branch**: TBD (implementation branch)

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

| Phase | Status | Progress |
|-------|--------|----------|
| Phase 1: Work Tracker Foundation | PENDING | 0% |
| Phase 2: Shared Infrastructure | PENDING | 0% |
| Phase 3: KM Integration | PENDING | 0% |
| Phase 4: Advanced Features | PENDING | 0% |

---

## Implementation Work Items

| Work Item | Status | Artifacts | Duration | Dependencies |
|-----------|--------|-----------|----------|--------------|
| WORK-101 | PENDING | Domain entities, VOs, events | Weeks 1-2 | None |
| WORK-102 | PENDING | Repository ports & adapters | Weeks 3-4 | WORK-101 |
| WORK-103 | PENDING | CQRS commands & queries | Weeks 5-6 | WORK-101, WORK-102 |
| WORK-104 | PENDING | CLI interface, BDD tests | Weeks 7-8 | WORK-103 |
| WORK-201 | PENDING | Event store port & adapter | Weeks 9-10 | Phase 1 |
| WORK-202 | PENDING | Graph store (NetworkX) | Weeks 11-12 | WORK-201 |
| WORK-203 | PENDING | Semantic index (FAISS) | Weeks 13-14 | WORK-202 |
| WORK-204 | PENDING | RDF serializer (RDFLib) | Weeks 15-16 | WORK-202, WORK-203 |
| WORK-301 | PENDING | KM domain entities | Weeks 17-18 | Phase 2 |
| WORK-302 | PENDING | KM repository layer | Weeks 19-20 | WORK-301 |
| WORK-303 | PENDING | KM CQRS & AAR handlers | Weeks 21-22 | WORK-301, WORK-302 |
| WORK-304 | PENDING | KM CLI & SKILL.md | Weeks 23-24 | WORK-303 |
| WORK-401 | PENDING | Cross-domain handlers | Weeks 25-26 | Phase 3 |
| WORK-402 | PENDING | HybridRAG & pattern discovery | Weeks 27-28 | WORK-401 |
| WORK-403 | PENDING | SPARQL endpoint & export | Weeks 29-30 | WORK-401 |
| WORK-404 | PENDING | Documentation & final tests | Weeks 31-32 | All |

---

## Phase 1: Work Tracker Foundation (Weeks 1-8)

> **Goal**: Establish Work Tracker domain with full CQRS, proving hexagonal architecture patterns.
> **Reference**: [Unified Design 11 Phase 1](../design/work-034-e-003-unified-design.md#phase-1-work-tracker-foundation-weeks-1-8)

### WORK-101: Domain Layer - Shared Kernel & Work Tracker Entities

- **Status**: PENDING
- **Duration**: Weeks 1-2
- **Dependencies**: None
- **Acceptance**: All BDD scenarios pass, architecture tests pass, 95%+ unit coverage
- **Reference**: [Unified Design 10.1](../design/work-034-e-003-unified-design.md#101-task-aggregate)

#### 101.1: Shared Kernel Value Objects

**Files**: `src/domain/value_objects/`

- [ ] **101.1.1: VertexId Base Class**
  - [ ] RED: Write failing tests for VertexId
    - [ ] `tests/unit/domain/value_objects/test_vertex_id.py`
    - [ ] Test: Valid UUID creation
    - [ ] Test: Invalid format raises ValueError
    - [ ] Test: Equality by value (not identity)
    - [ ] Test: Immutability (frozen dataclass)
    - [ ] Edge: Empty string raises ValueError
    - [ ] Edge: Whitespace-only raises ValueError
  - [ ] GREEN: Implement `src/domain/value_objects/vertex_id.py`
  - [ ] REFACTOR: Ensure `@dataclass(frozen=True)`, `__hash__` works

- [ ] **101.1.2: Domain-Specific IDs**
  - [ ] RED: Write failing tests for each ID type
    - [ ] `tests/unit/domain/value_objects/test_ids.py`
    - [ ] Test: TaskId creation with valid UUID
    - [ ] Test: PhaseId creation with valid UUID
    - [ ] Test: PlanId creation with valid UUID
    - [ ] Test: KnowledgeId creation with valid UUID
    - [ ] Test: Each ID type is distinct (TaskId != PhaseId)
    - [ ] Edge: None value raises TypeError
    - [ ] Negative: Non-UUID string raises ValueError
  - [ ] GREEN: Implement `src/domain/value_objects/ids.py`
  - [ ] REFACTOR: Extract common validation to base class

- [ ] **101.1.3: JerryURI Value Object**
  - [ ] RED: Write failing tests
    - [ ] `tests/unit/domain/value_objects/test_jerry_uri.py`
    - [ ] Test: Parse `jerry://task/abc-123` correctly
    - [ ] Test: Parse `jerry://plan/xyz/phase/001` correctly
    - [ ] Test: Serialize back to string
    - [ ] Edge: Missing scheme raises ValueError
    - [ ] Edge: Unknown entity type raises ValueError
    - [ ] Negative: Malformed URI raises ValueError
    - [ ] Negative: Empty string raises ValueError
  - [ ] GREEN: Implement `src/domain/value_objects/jerry_uri.py`
  - [ ] REFACTOR: Use regex pattern, cache parsed results

- [ ] **101.1.4: Priority Enum**
  - [ ] RED: Write failing tests
    - [ ] `tests/unit/domain/value_objects/test_priority.py`
    - [ ] Test: Priority.LOW, MEDIUM, HIGH, CRITICAL exist
    - [ ] Test: Ordering comparison works (LOW < HIGH)
    - [ ] Test: From string parsing works
    - [ ] Edge: Case-insensitive parsing
    - [ ] Negative: Invalid string raises ValueError
  - [ ] GREEN: Implement `src/domain/value_objects/priority.py`
  - [ ] REFACTOR: Implement `__lt__`, `__le__` for comparison

- [ ] **101.1.5: Status Enums**
  - [ ] RED: Write failing tests
    - [ ] `tests/unit/domain/value_objects/test_status.py`
    - [ ] Test: TaskStatus states (PENDING, IN_PROGRESS, BLOCKED, COMPLETED, CANCELLED)
    - [ ] Test: PhaseStatus states (NOT_STARTED, ACTIVE, COMPLETED)
    - [ ] Test: PlanStatus states (DRAFT, ACTIVE, COMPLETED, ARCHIVED)
    - [ ] Test: Valid transitions defined
    - [ ] Negative: Invalid transition raises InvalidStateTransition
  - [ ] GREEN: Implement `src/domain/value_objects/status.py`
  - [ ] REFACTOR: Add `can_transition_to()` method

- [ ] **101.1.6: Tag Value Object**
  - [ ] RED: Write failing tests
    - [ ] `tests/unit/domain/value_objects/test_tag.py`
    - [ ] Test: Valid tag creation
    - [ ] Test: Normalized to lowercase
    - [ ] Test: Whitespace trimmed
    - [ ] Edge: Max length (50 chars) enforced
    - [ ] Negative: Empty tag raises ValueError
    - [ ] Negative: Special characters raise ValueError
  - [ ] GREEN: Implement `src/domain/value_objects/tag.py`
  - [ ] REFACTOR: Add validation regex

- [ ] **101.1.7: Architecture Tests for Value Objects**
  - [ ] `tests/architecture/test_value_objects_architecture.py`
  - [ ] Test: All VOs are frozen dataclasses
  - [ ] Test: No external imports in value_objects/
  - [ ] Test: All VOs implement `__hash__`
  - [ ] Test: All VOs implement `__eq__`

#### 101.2: Task Aggregate Root

**Files**: `src/domain/aggregates/task.py`

- [ ] **101.2.1: Task Entity Core**
  - [ ] RED: Write failing tests for Task creation
    - [ ] `tests/unit/domain/aggregates/test_task.py`
    - [ ] Test: Create task with title, description
    - [ ] Test: Task has auto-generated TaskId
    - [ ] Test: Task starts in PENDING status
    - [ ] Test: Task has created_at timestamp
    - [ ] Test: Task has version=1 (optimistic concurrency)
    - [ ] Edge: Empty title raises ValueError
    - [ ] Edge: Title > 200 chars raises ValueError
    - [ ] Negative: None title raises TypeError
  - [ ] GREEN: Implement Task.__init__() and Task.create()
  - [ ] REFACTOR: Extract validation to private methods

- [ ] **101.2.2: Task State Transitions**
  - [ ] RED: Write failing tests for transitions
    - [ ] Test: PENDING -> IN_PROGRESS valid
    - [ ] Test: IN_PROGRESS -> COMPLETED valid
    - [ ] Test: IN_PROGRESS -> BLOCKED valid
    - [ ] Test: BLOCKED -> IN_PROGRESS valid
    - [ ] Test: PENDING -> CANCELLED valid
    - [ ] Test: transition emits TaskTransitioned event
    - [ ] Edge: Same state transition is no-op
    - [ ] Negative: COMPLETED -> IN_PROGRESS raises InvalidStateTransition
    - [ ] Negative: CANCELLED -> any raises InvalidStateTransition
  - [ ] GREEN: Implement Task.transition_to()
  - [ ] REFACTOR: Use state machine pattern

- [ ] **101.2.3: Task Completion**
  - [ ] RED: Write failing tests for completion
    - [ ] Test: complete() sets status=COMPLETED
    - [ ] Test: complete() sets completed_at timestamp
    - [ ] Test: complete() emits TaskCompleted event
    - [ ] Test: complete() requires IN_PROGRESS status
    - [ ] Edge: complete() with notes adds completion notes
    - [ ] Negative: complete() on PENDING raises InvalidStateTransition
  - [ ] GREEN: Implement Task.complete()
  - [ ] REFACTOR: Ensure immutable event creation

- [ ] **101.2.4: Task Phase Assignment**
  - [ ] RED: Write failing tests for phase assignment
    - [ ] Test: assign_to_phase() sets phase_id
    - [ ] Test: assign_to_phase() emits TaskAssignedToPhase event
    - [ ] Test: assign_to_phase() clears previous assignment
    - [ ] Edge: Assign to None removes from phase
    - [ ] Negative: Assign COMPLETED task raises InvalidStateError
  - [ ] GREEN: Implement Task.assign_to_phase()
  - [ ] REFACTOR: Add phase validation

- [ ] **101.2.5: Task Update Operations**
  - [ ] RED: Write failing tests for updates
    - [ ] Test: update_title() changes title
    - [ ] Test: update_description() changes description
    - [ ] Test: set_priority() changes priority
    - [ ] Test: add_tag() adds tag to set
    - [ ] Test: remove_tag() removes tag
    - [ ] Test: Each update increments version
    - [ ] Test: Each update emits TaskUpdated event
    - [ ] Edge: Add duplicate tag is no-op
    - [ ] Negative: Update COMPLETED task raises InvalidStateError
  - [ ] GREEN: Implement update methods
  - [ ] REFACTOR: Extract common update pattern

- [ ] **101.2.6: Task Invariant Enforcement**
  - [ ] RED: Write tests for business invariants
    - [ ] Test: Task with BLOCKED status must have blocker_reason
    - [ ] Test: Task with due_date in past raises ValidationError on create
    - [ ] Test: Completed task has completed_at <= updated_at
    - [ ] Negative: Clear blocker_reason while BLOCKED raises InvariantViolation
  - [ ] GREEN: Implement invariant checks
  - [ ] REFACTOR: Add `_validate_invariants()` method

- [ ] **101.2.7: Task Domain Events**
  - [ ] RED: Write tests for event structure
    - [ ] `tests/unit/domain/events/test_task_events.py`
    - [ ] Test: TaskCreated has task_id, title, created_at
    - [ ] Test: TaskTransitioned has from_status, to_status
    - [ ] Test: TaskCompleted has completed_at
    - [ ] Test: All events are CloudEvents 1.0 compliant
    - [ ] Test: Events are immutable (frozen)
  - [ ] GREEN: Implement `src/domain/events/work_tracker.py`
  - [ ] REFACTOR: Extract CloudEventEnvelope base class

#### 101.3: Phase Aggregate Root

**Files**: `src/domain/aggregates/phase.py`

- [ ] **101.3.1: Phase Entity Core**
  - [ ] RED: Write failing tests for Phase creation
    - [ ] `tests/unit/domain/aggregates/test_phase.py`
    - [ ] Test: Create phase with name, description
    - [ ] Test: Phase has auto-generated PhaseId
    - [ ] Test: Phase starts in NOT_STARTED status
    - [ ] Test: Phase has order_index for sequencing
    - [ ] Test: Phase has empty task_ids set initially
    - [ ] Edge: Empty name raises ValueError
    - [ ] Negative: Duplicate order_index in same plan (handled by Plan AR)
  - [ ] GREEN: Implement Phase.__init__() and Phase.create()
  - [ ] REFACTOR: Add validation methods

- [ ] **101.3.2: Phase Task Management**
  - [ ] RED: Write failing tests for task management
    - [ ] Test: add_task() adds TaskId to set
    - [ ] Test: add_task() emits TaskAddedToPhase event
    - [ ] Test: remove_task() removes TaskId from set
    - [ ] Test: remove_task() emits TaskRemovedFromPhase event
    - [ ] Edge: Add already-present task is no-op
    - [ ] Edge: Remove non-present task is no-op
    - [ ] Negative: Add task to COMPLETED phase raises InvalidStateError
  - [ ] GREEN: Implement add_task(), remove_task()
  - [ ] REFACTOR: Use set operations

- [ ] **101.3.3: Phase Completion Logic**
  - [ ] RED: Write failing tests for completion
    - [ ] Test: complete() sets status=COMPLETED
    - [ ] Test: complete() emits PhaseCompleted event
    - [ ] Test: complete() requires ACTIVE status
    - [ ] Test: complete() requires all tasks completed (or validates via callback)
    - [ ] Edge: complete(force=True) completes regardless of tasks
    - [ ] Negative: complete() with incomplete tasks raises PhaseNotCompletable
  - [ ] GREEN: Implement Phase.complete()
  - [ ] REFACTOR: Add task completion callback

- [ ] **101.3.4: Phase State Transitions**
  - [ ] RED: Write failing tests for phase transitions
    - [ ] Test: NOT_STARTED -> ACTIVE valid
    - [ ] Test: ACTIVE -> COMPLETED valid (via complete())
    - [ ] Test: activate() emits PhaseActivated event
    - [ ] Negative: NOT_STARTED -> COMPLETED raises InvalidStateTransition
    - [ ] Negative: COMPLETED -> ACTIVE raises InvalidStateTransition
  - [ ] GREEN: Implement Phase.activate()
  - [ ] REFACTOR: Add state machine

#### 101.4: Plan Aggregate Root

**Files**: `src/domain/aggregates/plan.py`

- [ ] **101.4.1: Plan Entity Core**
  - [ ] RED: Write failing tests for Plan creation
    - [ ] `tests/unit/domain/aggregates/test_plan.py`
    - [ ] Test: Create plan with name, description
    - [ ] Test: Plan has auto-generated PlanId
    - [ ] Test: Plan starts in DRAFT status
    - [ ] Test: Plan has empty phases list initially
    - [ ] Test: Plan has empty assumptions set
    - [ ] Edge: Empty name raises ValueError
    - [ ] Edge: Name > 100 chars raises ValueError
  - [ ] GREEN: Implement Plan.__init__() and Plan.create()
  - [ ] REFACTOR: Add metadata fields

- [ ] **101.4.2: Plan Phase Management**
  - [ ] RED: Write failing tests for phase management
    - [ ] Test: add_phase() adds PhaseId with order
    - [ ] Test: add_phase() emits PhaseAddedToPlan event
    - [ ] Test: remove_phase() removes PhaseId
    - [ ] Test: reorder_phases() updates order_index values
    - [ ] Test: get_phases() returns sorted by order_index
    - [ ] Edge: Add phase at specific position shifts others
    - [ ] Negative: Add phase to COMPLETED plan raises InvalidStateError
    - [ ] Negative: Remove last phase raises PlanRequiresPhase
  - [ ] GREEN: Implement add_phase(), remove_phase(), reorder_phases()
  - [ ] REFACTOR: Use OrderedDict or sorted list

- [ ] **101.4.3: Plan Assumption Tracking**
  - [ ] RED: Write failing tests for assumptions
    - [ ] Test: track_assumption() adds assumption text
    - [ ] Test: track_assumption() emits AssumptionTracked event
    - [ ] Test: get_assumptions() returns all assumptions
    - [ ] Test: validate_assumption() marks as validated/invalidated
    - [ ] Edge: Duplicate assumption text is no-op
    - [ ] Negative: Empty assumption text raises ValueError
  - [ ] GREEN: Implement assumption methods
  - [ ] REFACTOR: Create Assumption value object

- [ ] **101.4.4: Plan State Transitions**
  - [ ] RED: Write failing tests for plan transitions
    - [ ] Test: DRAFT -> ACTIVE valid (via activate())
    - [ ] Test: ACTIVE -> COMPLETED valid (via complete())
    - [ ] Test: ACTIVE -> ARCHIVED valid (via archive())
    - [ ] Test: activate() emits PlanActivated event
    - [ ] Test: complete() requires all phases completed
    - [ ] Negative: DRAFT -> COMPLETED raises InvalidStateTransition
    - [ ] Negative: ARCHIVED -> any raises InvalidStateTransition
  - [ ] GREEN: Implement activate(), complete(), archive()
  - [ ] REFACTOR: Add state machine

#### 101.5: Domain Events (CloudEvents 1.0)

**Files**: `src/domain/events/`

- [ ] **101.5.1: CloudEventEnvelope Base**
  - [ ] RED: Write failing tests for envelope
    - [ ] `tests/unit/domain/events/test_cloud_event_envelope.py`
    - [ ] Test: Envelope has specversion="1.0"
    - [ ] Test: Envelope has type (e.g., "jerry.task.created")
    - [ ] Test: Envelope has source (e.g., "jerry://worktracker")
    - [ ] Test: Envelope has id (UUID)
    - [ ] Test: Envelope has time (ISO 8601)
    - [ ] Test: Envelope has data (event payload)
    - [ ] Test: Envelope serializes to JSON
    - [ ] Edge: Missing required field raises ValidationError
  - [ ] GREEN: Implement `src/domain/events/base.py`
  - [ ] REFACTOR: Add JSON schema validation

- [ ] **101.5.2: Work Tracker Events**
  - [ ] RED: Write failing tests for each event
    - [ ] `tests/unit/domain/events/test_work_tracker_events.py`
    - [ ] Test: TaskCreated, TaskUpdated, TaskTransitioned, TaskCompleted
    - [ ] Test: PhaseCreated, PhaseActivated, PhaseCompleted
    - [ ] Test: PlanCreated, PlanActivated, PlanCompleted, PlanArchived
    - [ ] Test: TaskAssignedToPhase, TaskRemovedFromPhase
    - [ ] Test: Each event wraps in CloudEventEnvelope
    - [ ] Test: Events are immutable
  - [ ] GREEN: Implement `src/domain/events/work_tracker.py`
  - [ ] REFACTOR: Add factory methods

- [ ] **101.5.3: Contract Tests for Events**
  - [ ] `tests/contract/events/test_event_schema.py`
  - [ ] Test: All events validate against JSON schema
  - [ ] Test: Events can be serialized/deserialized
  - [ ] Test: Event versioning (v1 schema)

#### 101.6: Domain Exceptions

**Files**: `src/domain/exceptions.py`

- [ ] **101.6.1: Exception Hierarchy**
  - [ ] RED: Write failing tests for exceptions
    - [ ] `tests/unit/domain/test_exceptions.py`
    - [ ] Test: DomainError is base class
    - [ ] Test: NotFoundError has entity_type, entity_id
    - [ ] Test: InvalidStateError has current_state, attempted_action
    - [ ] Test: InvalidStateTransition has from_state, to_state
    - [ ] Test: InvariantViolation has invariant_name, details
    - [ ] Test: ConcurrencyError has expected_version, actual_version
    - [ ] Test: ValidationError has field_name, message
  - [ ] GREEN: Implement exception classes
  - [ ] REFACTOR: Add error codes for machine-readable handling

#### 101.7: Architecture Tests for Domain Layer

**Files**: `tests/architecture/`

- [ ] **101.7.1: Layer Dependency Tests**
  - [ ] `tests/architecture/test_domain_architecture.py`
  - [ ] Test: domain/ has NO imports from application/
  - [ ] Test: domain/ has NO imports from infrastructure/
  - [ ] Test: domain/ has NO imports from interface/
  - [ ] Test: domain/ only uses stdlib imports
  - [ ] Test: All aggregates extend AggregateRoot base
  - [ ] Test: All value objects are frozen dataclasses

- [ ] **101.7.2: DDD Pattern Compliance**
  - [ ] `tests/architecture/test_ddd_patterns.py`
  - [ ] Test: Aggregates have private setters
  - [ ] Test: Aggregates expose behavior methods, not data
  - [ ] Test: Value objects are immutable
  - [ ] Test: Domain events are past-tense named

---

### WORK-102: Repository Layer - Ports & SQLite Adapters

- **Status**: PENDING
- **Duration**: Weeks 3-4
- **Dependencies**: WORK-101
- **Acceptance**: All CRUD operations work, integration tests pass, 95%+ coverage
- **Reference**: [Unified Design 5.1](../design/work-034-e-003-unified-design.md#51-iworkitemrepository)

#### 102.1: Repository Port Definitions

**Files**: `src/domain/ports/`

- [ ] **102.1.1: IWorkItemRepository Port**
  - [ ] RED: Write failing tests for port interface
    - [ ] `tests/unit/domain/ports/test_work_item_repository.py`
    - [ ] Test: Interface defines get_task(id) -> Task | None
    - [ ] Test: Interface defines save_task(task) -> None
    - [ ] Test: Interface defines delete_task(id) -> bool
    - [ ] Test: Interface defines list_tasks(filters) -> List[Task]
    - [ ] Test: Same methods for Phase and Plan
    - [ ] Contract: Port is abstract (ABC)
  - [ ] GREEN: Implement `src/domain/ports/work_item_repository.py`
  - [ ] REFACTOR: Add type hints, docstrings

- [ ] **102.1.2: IUnitOfWork Port**
  - [ ] RED: Write failing tests for UoW interface
    - [ ] `tests/unit/domain/ports/test_unit_of_work.py`
    - [ ] Test: Interface defines begin() context manager
    - [ ] Test: Interface defines commit()
    - [ ] Test: Interface defines rollback()
    - [ ] Test: Interface provides repository property
    - [ ] Contract: Commit on exit, rollback on exception
  - [ ] GREEN: Implement `src/domain/ports/unit_of_work.py`
  - [ ] REFACTOR: Add async support preparation

#### 102.2: SQLite Repository Adapter

**Files**: `src/infrastructure/persistence/`

- [ ] **102.2.1: Database Schema Migration**
  - [ ] RED: Write failing migration tests
    - [ ] `tests/integration/persistence/test_migrations.py`
    - [ ] Test: Migration creates tasks table
    - [ ] Test: Migration creates phases table
    - [ ] Test: Migration creates plans table
    - [ ] Test: Migration creates task_tags junction table
    - [ ] Test: Migration is idempotent
    - [ ] Edge: Run migration on existing DB does nothing
    - [ ] Negative: Invalid migration raises MigrationError
  - [ ] GREEN: Implement `migrations/001_work_tracker_schema.sql`
  - [ ] REFACTOR: Add migration versioning

- [ ] **102.2.2: Task Repository CRUD**
  - [ ] RED: Write failing integration tests
    - [ ] `tests/integration/persistence/test_sqlite_task_repo.py`
    - [ ] Test: save_task() inserts new task
    - [ ] Test: save_task() updates existing task
    - [ ] Test: get_task() returns task by ID
    - [ ] Test: get_task() returns None for missing ID
    - [ ] Test: delete_task() removes task
    - [ ] Test: delete_task() returns False for missing ID
    - [ ] Test: list_tasks() returns all tasks
    - [ ] Test: list_tasks(status=) filters by status
    - [ ] Test: list_tasks(priority=) filters by priority
    - [ ] Test: list_tasks(tags=) filters by tags
    - [ ] Edge: Concurrent update detected (version mismatch)
    - [ ] Negative: Save with stale version raises ConcurrencyError
  - [ ] GREEN: Implement SQLite adapter task methods
  - [ ] REFACTOR: Extract SQL to constants, add parameterization

- [ ] **102.2.3: Phase Repository CRUD**
  - [ ] RED: Write failing integration tests
    - [ ] `tests/integration/persistence/test_sqlite_phase_repo.py`
    - [ ] Test: save_phase() inserts/updates
    - [ ] Test: get_phase() returns phase
    - [ ] Test: delete_phase() removes phase
    - [ ] Test: list_phases() returns phases
    - [ ] Test: list_phases(plan_id=) filters by plan
    - [ ] Test: Cascade: delete phase removes task associations
    - [ ] Edge: Get phase with many tasks is performant
    - [ ] Negative: Delete phase with orphan tasks option
  - [ ] GREEN: Implement SQLite adapter phase methods
  - [ ] REFACTOR: Add indexing for plan_id

- [ ] **102.2.4: Plan Repository CRUD**
  - [ ] RED: Write failing integration tests
    - [ ] `tests/integration/persistence/test_sqlite_plan_repo.py`
    - [ ] Test: save_plan() inserts/updates
    - [ ] Test: get_plan() returns plan with phases
    - [ ] Test: delete_plan() removes plan
    - [ ] Test: list_plans() returns plans
    - [ ] Test: list_plans(status=) filters by status
    - [ ] Test: Cascade: delete plan deletes phases
    - [ ] Edge: Get plan with nested structure
    - [ ] Negative: Delete active plan raises ActivePlanError
  - [ ] GREEN: Implement SQLite adapter plan methods
  - [ ] REFACTOR: Add eager loading for phases

- [ ] **102.2.5: Optimistic Concurrency**
  - [ ] RED: Write failing tests for concurrency
    - [ ] `tests/integration/persistence/test_concurrency.py`
    - [ ] Test: Save increments version
    - [ ] Test: Save with outdated version fails
    - [ ] Test: Error includes expected vs actual version
    - [ ] Negative: Concurrent updates detected
  - [ ] GREEN: Implement version checking in save methods
  - [ ] REFACTOR: Add retry logic option

#### 102.3: Unit of Work Implementation

**Files**: `src/infrastructure/persistence/sqlite_unit_of_work.py`

- [ ] **102.3.1: Transaction Management**
  - [ ] RED: Write failing integration tests
    - [ ] `tests/integration/persistence/test_sqlite_unit_of_work.py`
    - [ ] Test: Begin starts transaction
    - [ ] Test: Commit persists all changes
    - [ ] Test: Rollback reverts all changes
    - [ ] Test: Context manager auto-commits on success
    - [ ] Test: Context manager auto-rollbacks on exception
    - [ ] Edge: Nested transactions (savepoints)
    - [ ] Negative: Commit on failed UoW raises UnitOfWorkError
  - [ ] GREEN: Implement SQLiteUnitOfWork
  - [ ] REFACTOR: Add connection pooling

#### 102.4: Contract Tests for Repository

**Files**: `tests/contract/`

- [ ] **102.4.1: Repository Port Compliance**
  - [ ] `tests/contract/persistence/test_repository_contract.py`
  - [ ] Test: SQLite adapter implements all IWorkItemRepository methods
  - [ ] Test: Return types match port signatures
  - [ ] Test: Exceptions match port specifications
  - [ ] Run contract against in-memory and file SQLite

---

### WORK-103: CQRS Implementation - Commands & Queries

- **Status**: PENDING
- **Duration**: Weeks 5-6
- **Dependencies**: WORK-101, WORK-102
- **Acceptance**: All commands emit events, queries return DTOs, handlers tested
- **Reference**: [Unified Design 6.1-6.2](../design/work-034-e-003-unified-design.md#61-work-tracker-commands)

#### 103.1: Command Definitions

**Files**: `src/application/commands/work_tracker/`

- [ ] **103.1.1: Task Commands**
  - [ ] RED: Write failing tests for command structures
    - [ ] `tests/unit/application/commands/test_task_commands.py`
    - [ ] Test: CreateTaskCommand has title, description, priority
    - [ ] Test: UpdateTaskCommand has task_id, optional fields
    - [ ] Test: TransitionTaskCommand has task_id, target_status
    - [ ] Test: CompleteTaskCommand has task_id, optional notes
    - [ ] Test: AssignTaskToPhaseCommand has task_id, phase_id
    - [ ] Test: Commands are immutable (frozen dataclass)
    - [ ] Negative: Invalid command data raises ValidationError
  - [ ] GREEN: Implement command classes
  - [ ] REFACTOR: Add validation decorators

- [ ] **103.1.2: Phase Commands**
  - [ ] RED: Write failing tests
    - [ ] `tests/unit/application/commands/test_phase_commands.py`
    - [ ] Test: CreatePhaseCommand has name, plan_id, order
    - [ ] Test: CompletePhaseCommand has phase_id
    - [ ] Test: ActivatePhaseCommand has phase_id
  - [ ] GREEN: Implement command classes
  - [ ] REFACTOR: Ensure consistency

- [ ] **103.1.3: Plan Commands**
  - [ ] RED: Write failing tests
    - [ ] `tests/unit/application/commands/test_plan_commands.py`
    - [ ] Test: CreatePlanCommand has name, description
    - [ ] Test: ActivatePlanCommand has plan_id
    - [ ] Test: CompletePlanCommand has plan_id
  - [ ] GREEN: Implement command classes
  - [ ] REFACTOR: Add builder pattern option

#### 103.2: Command Handlers

**Files**: `src/application/handlers/commands/work_tracker/`

- [ ] **103.2.1: CreateTaskHandler**
  - [ ] RED: Write failing unit tests (mocked repo)
    - [ ] `tests/unit/application/handlers/test_create_task_handler.py`
    - [ ] Test: Handler creates Task via factory
    - [ ] Test: Handler saves Task via repository
    - [ ] Test: Handler dispatches TaskCreated event
    - [ ] Test: Handler returns TaskId
    - [ ] Edge: Handler rolls back on dispatch failure
    - [ ] Negative: Duplicate task title handling
  - [ ] GREEN: Implement CreateTaskCommandHandler
  - [ ] REFACTOR: Extract common handler pattern

- [ ] **103.2.2: UpdateTaskHandler**
  - [ ] RED: Write failing unit tests
    - [ ] `tests/unit/application/handlers/test_update_task_handler.py`
    - [ ] Test: Handler fetches existing Task
    - [ ] Test: Handler applies updates
    - [ ] Test: Handler saves updated Task
    - [ ] Test: Handler dispatches TaskUpdated event
    - [ ] Negative: Task not found raises NotFoundError
    - [ ] Negative: Stale version raises ConcurrencyError
  - [ ] GREEN: Implement UpdateTaskCommandHandler
  - [ ] REFACTOR: Use apply pattern

- [ ] **103.2.3: TransitionTaskHandler**
  - [ ] RED: Write failing unit tests
    - [ ] `tests/unit/application/handlers/test_transition_task_handler.py`
    - [ ] Test: Handler transitions task status
    - [ ] Test: Handler dispatches TaskTransitioned event
    - [ ] Negative: Invalid transition raises InvalidStateTransition
    - [ ] Negative: Task not found raises NotFoundError
  - [ ] GREEN: Implement TransitionTaskCommandHandler
  - [ ] REFACTOR: Add transition validation

- [ ] **103.2.4: CompleteTaskHandler**
  - [ ] RED: Write failing unit tests
    - [ ] `tests/unit/application/handlers/test_complete_task_handler.py`
    - [ ] Test: Handler completes task
    - [ ] Test: Handler dispatches TaskCompleted event
    - [ ] Negative: Complete non-IN_PROGRESS raises InvalidStateError
  - [ ] GREEN: Implement CompleteTaskCommandHandler
  - [ ] REFACTOR: Add completion notes handling

- [ ] **103.2.5: Phase and Plan Handlers**
  - [ ] RED: Write failing unit tests for each handler
    - [ ] CreatePhaseHandler, CompletePhaseHandler
    - [ ] CreatePlanHandler, ActivatePlanHandler, CompletePlanHandler
    - [ ] Tests follow same pattern as task handlers
  - [ ] GREEN: Implement all handlers
  - [ ] REFACTOR: Extract base handler class

#### 103.3: Query Definitions and Handlers

**Files**: `src/application/queries/work_tracker/`, `src/application/dtos/`

- [ ] **103.3.1: DTOs**
  - [ ] RED: Write failing tests for DTOs
    - [ ] `tests/unit/application/dtos/test_work_tracker_dtos.py`
    - [ ] Test: TaskDTO has all display fields
    - [ ] Test: PhaseDTO has phase fields + task count
    - [ ] Test: PlanDTO has plan fields + phase list
    - [ ] Test: DTOs are immutable
    - [ ] Test: DTOs have from_entity() factory
  - [ ] GREEN: Implement `src/application/dtos/work_tracker.py`
  - [ ] REFACTOR: Add serialization methods

- [ ] **103.3.2: Task Queries**
  - [ ] RED: Write failing tests
    - [ ] `tests/unit/application/queries/test_task_queries.py`
    - [ ] Test: GetTaskQuery has task_id
    - [ ] Test: ListTasksQuery has filters (status, priority, tags)
    - [ ] Test: GetTaskHistoryQuery has task_id
  - [ ] GREEN: Implement query classes
  - [ ] REFACTOR: Add pagination to list queries

- [ ] **103.3.3: Query Handlers**
  - [ ] RED: Write failing unit tests (mocked repo)
    - [ ] `tests/unit/application/handlers/queries/test_task_query_handlers.py`
    - [ ] Test: GetTaskQueryHandler returns TaskDTO
    - [ ] Test: GetTaskQueryHandler returns None for missing
    - [ ] Test: ListTasksQueryHandler returns List[TaskDTO]
    - [ ] Test: ListTasksQueryHandler applies filters
    - [ ] Test: GetTaskHistoryQueryHandler returns events
    - [ ] Edge: Empty list returned for no matches
  - [ ] GREEN: Implement query handlers
  - [ ] REFACTOR: Add caching layer preparation

#### 103.4: Event Dispatcher

**Files**: `src/domain/ports/event_dispatcher.py`, `src/infrastructure/messaging/`

- [ ] **103.4.1: Event Dispatcher Port**
  - [ ] RED: Write failing tests for port
    - [ ] `tests/unit/domain/ports/test_event_dispatcher.py`
    - [ ] Test: Interface defines dispatch(event) -> None
    - [ ] Test: Interface defines dispatch_all(events) -> None
    - [ ] Test: Interface defines subscribe(event_type, handler)
    - [ ] Contract: Port is abstract
  - [ ] GREEN: Implement `src/domain/ports/event_dispatcher.py`
  - [ ] REFACTOR: Add type constraints

- [ ] **103.4.2: In-Memory Dispatcher Adapter**
  - [ ] RED: Write failing integration tests
    - [ ] `tests/integration/messaging/test_in_memory_dispatcher.py`
    - [ ] Test: dispatch() calls registered handlers
    - [ ] Test: Multiple handlers for same event type
    - [ ] Test: No handler is no-op (or configurable)
    - [ ] Test: Handler exception doesn't stop other handlers
    - [ ] Edge: Async handler support
    - [ ] Negative: Handler timeout handling
  - [ ] GREEN: Implement `src/infrastructure/messaging/in_memory_dispatcher.py`
  - [ ] REFACTOR: Add logging, retry logic

#### 103.5: Integration Tests for CQRS

**Files**: `tests/integration/application/`

- [ ] **103.5.1: Command-Query Round Trip**
  - [ ] `tests/integration/application/test_cqrs_integration.py`
  - [ ] Test: Create task -> Query task returns it
  - [ ] Test: Update task -> Query shows updates
  - [ ] Test: Complete task -> Query shows completed
  - [ ] Test: Events are dispatched during commands
  - [ ] Test: Full task lifecycle CRUD

---

### WORK-104: CLI Interface & BDD Tests

- **Status**: PENDING
- **Duration**: Weeks 7-8
- **Dependencies**: WORK-103
- **Acceptance**: Full CRUD via CLI, 100% BDD scenario coverage, <100ms p95
- **Reference**: [Unified Design 7](../design/work-034-e-003-unified-design.md#7-interface-specifications)

#### 104.1: CLI Adapter

**Files**: `src/interface/cli/`

- [ ] **104.1.1: CLI Entry Point**
  - [ ] RED: Write failing E2E tests
    - [ ] `tests/e2e/cli/test_work_tracker_cli.py`
    - [ ] Test: `wt --help` shows usage
    - [ ] Test: `wt --version` shows version
    - [ ] Test: Exit code 0 on success
    - [ ] Test: Exit code 1 on error
    - [ ] Negative: Unknown command shows error
  - [ ] GREEN: Implement `src/interface/cli/work_tracker_cli.py`
  - [ ] REFACTOR: Add rich output formatting

- [ ] **104.1.2: Task Subcommand**
  - [ ] RED: Write failing E2E tests
    - [ ] `tests/e2e/cli/test_task_cli.py`
    - [ ] Test: `wt task create "Title"` creates task
    - [ ] Test: `wt task list` lists tasks
    - [ ] Test: `wt task show <id>` shows task details
    - [ ] Test: `wt task update <id> --title "New"` updates
    - [ ] Test: `wt task complete <id>` completes task
    - [ ] Test: `wt task delete <id>` deletes task
    - [ ] Test: Output is valid JSON with `--json` flag
    - [ ] Edge: Create with all optional fields
    - [ ] Negative: Show non-existent task shows error
  - [ ] GREEN: Implement task subcommand
  - [ ] REFACTOR: Add confirmation prompts

- [ ] **104.1.3: Phase Subcommand**
  - [ ] RED: Write failing E2E tests
    - [ ] `tests/e2e/cli/test_phase_cli.py`
    - [ ] Test: `wt phase create "Name" --plan <id>` creates phase
    - [ ] Test: `wt phase list --plan <id>` lists phases
    - [ ] Test: `wt phase show <id>` shows phase
    - [ ] Test: `wt phase complete <id>` completes phase
    - [ ] Negative: Create phase without plan fails
  - [ ] GREEN: Implement phase subcommand
  - [ ] REFACTOR: Add progress indicator

- [ ] **104.1.4: Plan Subcommand**
  - [ ] RED: Write failing E2E tests
    - [ ] `tests/e2e/cli/test_plan_cli.py`
    - [ ] Test: `wt plan create "Name"` creates plan
    - [ ] Test: `wt plan list` lists plans
    - [ ] Test: `wt plan show <id>` shows plan with phases
    - [ ] Test: `wt plan activate <id>` activates plan
    - [ ] Test: `wt plan complete <id>` completes plan
    - [ ] Negative: Complete plan with incomplete phases fails
  - [ ] GREEN: Implement plan subcommand
  - [ ] REFACTOR: Add tree view for plan structure

- [ ] **104.1.5: CLI Error Handling**
  - [ ] RED: Write failing tests for error scenarios
    - [ ] `tests/e2e/cli/test_cli_errors.py`
    - [ ] Test: Invalid ID format shows helpful error
    - [ ] Test: Database error shows user-friendly message
    - [ ] Test: Validation error shows field and message
    - [ ] Test: Concurrent modification shows retry suggestion
  - [ ] GREEN: Implement error handling
  - [ ] REFACTOR: Add error codes for scripting

#### 104.2: Work Tracker SKILL.md

**Files**: `skills/work-tracker/SKILL.md`

- [ ] **104.2.1: Skill Documentation**
  - [ ] Create `skills/work-tracker/SKILL.md`
  - [ ] Document all commands with examples
  - [ ] Include natural language patterns
  - [ ] Add troubleshooting section
  - [ ] Add quick reference card

#### 104.3: BDD Test Suite

**Files**: `tests/bdd/work_tracker/`

- [ ] **104.3.1: Task Feature File**
  - [ ] `tests/bdd/work_tracker/features/task.feature`
  - [ ] Scenario: Create task with title and description
  - [ ] Scenario: Create task with priority and tags
  - [ ] Scenario: Transition task through states
  - [ ] Scenario: Complete task records completion time
  - [ ] Scenario: Assign task to phase
  - [ ] Scenario: Block task with reason
  - [ ] Scenario: Cancel pending task
  - [ ] Edge Scenario: Create task with max-length title
  - [ ] Negative Scenario: Create task with empty title fails
  - [ ] Negative Scenario: Complete task not in progress fails

- [ ] **104.3.2: Phase Feature File**
  - [ ] `tests/bdd/work_tracker/features/phase.feature`
  - [ ] Scenario: Create phase in plan
  - [ ] Scenario: Add tasks to phase
  - [ ] Scenario: Remove task from phase
  - [ ] Scenario: Complete phase when all tasks done
  - [ ] Negative Scenario: Complete phase with incomplete tasks fails

- [ ] **104.3.3: Plan Feature File**
  - [ ] `tests/bdd/work_tracker/features/plan.feature`
  - [ ] Scenario: Create plan with phases
  - [ ] Scenario: Activate draft plan
  - [ ] Scenario: Complete plan when all phases done
  - [ ] Scenario: Track assumptions on plan
  - [ ] Negative Scenario: Complete active plan with incomplete phases fails

- [ ] **104.3.4: Step Definitions**
  - [ ] `tests/bdd/work_tracker/steps/task_steps.py`
  - [ ] `tests/bdd/work_tracker/steps/phase_steps.py`
  - [ ] `tests/bdd/work_tracker/steps/plan_steps.py`
  - [ ] All steps use REAL implementations (no mocks)

#### 104.4: System Tests

**Files**: `tests/system/work_tracker/`

- [ ] **104.4.1: Multi-Operation Workflows**
  - [ ] `tests/system/work_tracker/test_full_workflow.py`
  - [ ] Test: Create plan -> Add phases -> Add tasks -> Complete all
  - [ ] Test: Create multiple plans, interleave operations
  - [ ] Test: Database persists across CLI invocations
  - [ ] Test: Concurrent CLI operations don't corrupt data

- [ ] **104.4.2: Performance Tests**
  - [ ] `tests/system/work_tracker/test_performance.py`
  - [ ] Test: Create 1000 tasks in < 10s
  - [ ] Test: List 1000 tasks in < 1s
  - [ ] Test: Single operation p95 < 100ms
  - [ ] Test: Memory usage stays bounded

#### 104.5: Phase 1 Go/No-Go Gate

- [ ] **104.5.1: Quality Gates**
  - [ ] All unit tests pass (target: 95%+ coverage)
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
> **Reference**: [Unified Design 11 Phase 2](../design/work-034-e-003-unified-design.md#phase-2-shared-infrastructure-weeks-9-16)

### WORK-201: Event Store Implementation

- **Status**: PENDING
- **Duration**: Weeks 9-10
- **Dependencies**: Phase 1 complete
- **Acceptance**: CloudEvents 1.0 compliant, append-only semantics, replay works
- **Reference**: [Unified Design 5.5](../design/work-034-e-003-unified-design.md#55-ieventstore)

#### 201.1: Event Store Port

**Files**: `src/domain/ports/event_store.py`

- [ ] **201.1.1: IEventStore Interface**
  - [ ] RED: Write failing tests for port
    - [ ] `tests/unit/domain/ports/test_event_store.py`
    - [ ] Test: append(event) adds event to stream
    - [ ] Test: get(event_id) returns single event
    - [ ] Test: get_by_subject(subject_id) returns events for entity
    - [ ] Test: get_by_type(event_type) returns events by type
    - [ ] Test: replay(from_position) returns ordered events
    - [ ] Test: get_snapshot(subject_id) returns latest snapshot
    - [ ] Test: save_snapshot(snapshot) persists snapshot
    - [ ] Contract: Port is abstract
  - [ ] GREEN: Implement port interface
  - [ ] REFACTOR: Add type hints for CloudEventEnvelope

#### 201.2: SQLite Event Store Adapter

**Files**: `src/infrastructure/event_store/`

- [ ] **201.2.1: Event Store Schema**
  - [ ] RED: Write failing migration tests
    - [ ] `tests/integration/event_store/test_migrations.py`
    - [ ] Test: Creates events table (id, type, subject, time, data)
    - [ ] Test: Creates snapshots table
    - [ ] Test: Creates indexes for subject, type, time
    - [ ] Test: Events table is append-only (no UPDATE/DELETE triggers)
  - [ ] GREEN: Implement `migrations/002_event_store_schema.sql`
  - [ ] REFACTOR: Add partitioning preparation

- [ ] **201.2.2: Event Store CRUD**
  - [ ] RED: Write failing integration tests
    - [ ] `tests/integration/event_store/test_sqlite_event_store.py`
    - [ ] Test: append() inserts event with auto-increment position
    - [ ] Test: get() returns event by ID
    - [ ] Test: get_by_subject() returns all events for subject
    - [ ] Test: get_by_type() returns events of type
    - [ ] Test: Events ordered by position
    - [ ] Edge: get() for non-existent returns None
    - [ ] Edge: get_by_subject() for new entity returns empty
    - [ ] Negative: Modifying event raises ImmutableEventError
  - [ ] GREEN: Implement `src/infrastructure/event_store/sqlite_event_store.py`
  - [ ] REFACTOR: Add batch insert

- [ ] **201.2.3: Event Replay**
  - [ ] RED: Write failing tests for replay
    - [ ] `tests/integration/event_store/test_event_replay.py`
    - [ ] Test: replay() returns all events from position 0
    - [ ] Test: replay(from_position=N) skips first N events
    - [ ] Test: replay(to_position=M) stops at M
    - [ ] Test: replay() handles large event counts (1000+)
    - [ ] Test: replay() maintains exact ordering
    - [ ] Edge: replay() on empty store returns empty
  - [ ] GREEN: Implement replay functionality
  - [ ] REFACTOR: Add streaming/generator support

- [ ] **201.2.4: Snapshot Management**
  - [ ] RED: Write failing tests for snapshots
    - [ ] `tests/integration/event_store/test_snapshots.py`
    - [ ] Test: save_snapshot() persists aggregate state
    - [ ] Test: get_snapshot() returns latest for subject
    - [ ] Test: Snapshot includes version/position
    - [ ] Test: Multiple snapshots, latest returned
    - [ ] Edge: No snapshot returns None
  - [ ] GREEN: Implement snapshot methods
  - [ ] REFACTOR: Add snapshot frequency configuration

#### 201.3: Contract Tests for Event Store

- [ ] `tests/contract/event_store/test_event_store_contract.py`
- [ ] Test: Adapter implements all IEventStore methods
- [ ] Test: CloudEvents 1.0 compliance for stored events
- [ ] Test: Immutability guarantees

---

### WORK-202: Graph Store Implementation

- **Status**: PENDING
- **Duration**: Weeks 11-12
- **Dependencies**: WORK-201
- **Acceptance**: Traversal operations work, persistence to disk, performance baseline met
- **Reference**: [Unified Design 5.3](../design/work-034-e-003-unified-design.md#53-igraphstore)

#### 202.1: Graph Store Port

**Files**: `src/domain/ports/graph_store.py`

- [ ] **202.1.1: IGraphStore Interface**
  - [ ] RED: Write failing tests for port
    - [ ] `tests/unit/domain/ports/test_graph_store.py`
    - [ ] Test: add_vertex(vertex) adds node to graph
    - [ ] Test: get_vertex(id) returns vertex
    - [ ] Test: update_vertex(vertex) updates properties
    - [ ] Test: remove_vertex(id) removes node and edges
    - [ ] Test: add_edge(source, target, relation) adds edge
    - [ ] Test: get_edges(vertex_id, direction) returns edges
    - [ ] Test: remove_edge(source, target, relation) removes edge
    - [ ] Test: traverse(start, depth, direction) returns subgraph
    - [ ] Test: shortest_path(start, end) returns path
    - [ ] Contract: Port is abstract
  - [ ] GREEN: Implement port interface
  - [ ] REFACTOR: Add Vertex, Edge value objects

- [ ] **202.1.2: Graph Value Objects**
  - [ ] RED: Write failing tests
    - [ ] `tests/unit/domain/value_objects/test_graph.py`
    - [ ] Test: Vertex has id, type, properties
    - [ ] Test: Edge has source_id, target_id, relation, properties
    - [ ] Test: Both are immutable
  - [ ] GREEN: Implement `src/domain/value_objects/graph.py`
  - [ ] REFACTOR: Add validation

#### 202.2: NetworkX Graph Adapter

**Files**: `src/infrastructure/graph/`

- [ ] **202.2.1: Graph CRUD Operations**
  - [ ] RED: Write failing integration tests
    - [ ] `tests/integration/graph/test_networkx_graph_store.py`
    - [ ] Test: add_vertex() creates node
    - [ ] Test: get_vertex() returns node data
    - [ ] Test: update_vertex() modifies properties
    - [ ] Test: remove_vertex() deletes node and edges
    - [ ] Test: add_edge() creates directed edge
    - [ ] Test: get_edges() returns incoming/outgoing/both
    - [ ] Test: remove_edge() deletes edge
    - [ ] Edge: Add duplicate vertex updates properties
    - [ ] Edge: Remove non-existent vertex is no-op
    - [ ] Negative: Invalid vertex type raises ValidationError
  - [ ] GREEN: Implement `src/infrastructure/graph/networkx_graph_store.py`
  - [ ] REFACTOR: Add property indexing

- [ ] **202.2.2: Graph Traversal**
  - [ ] RED: Write failing tests for traversal
    - [ ] `tests/integration/graph/test_graph_traversal.py`
    - [ ] Test: traverse(depth=1) returns immediate neighbors
    - [ ] Test: traverse(depth=2) returns 2-hop neighbors
    - [ ] Test: traverse(direction=OUTGOING) follows outbound
    - [ ] Test: traverse(direction=INCOMING) follows inbound
    - [ ] Test: traverse() respects edge type filters
    - [ ] Test: shortest_path() returns path if exists
    - [ ] Test: shortest_path() returns None if no path
    - [ ] Edge: traverse() on isolated node returns just node
    - [ ] Edge: traverse(depth=0) returns start node only
  - [ ] GREEN: Implement traversal methods
  - [ ] REFACTOR: Use BFS algorithm

- [ ] **202.2.3: Graph Persistence**
  - [ ] RED: Write failing tests for persistence
    - [ ] `tests/integration/graph/test_graph_persistence.py`
    - [ ] Test: save() writes graph to file
    - [ ] Test: load() restores graph from file
    - [ ] Test: Round-trip preserves all data
    - [ ] Test: Load non-existent file returns empty graph
    - [ ] Edge: Large graph (1000 vertices) save/load
    - [ ] Negative: Corrupted file raises GraphCorruptionError
  - [ ] GREEN: Implement save/load with gpickle
  - [ ] REFACTOR: Add file locking

#### 202.3: Performance Baseline

- [ ] **202.3.1: Graph Performance Tests**
  - [ ] `tests/performance/graph/test_graph_performance.py`
  - [ ] Benchmark: Add 500 vertices < 1s
  - [ ] Benchmark: 2-hop traversal from any node < 100ms
  - [ ] Benchmark: Save/load 500-node graph < 500ms
  - [ ] Document baseline metrics in `docs/performance/graph-baseline.md`

---

### WORK-203: Semantic Index Implementation

- **Status**: PENDING
- **Duration**: Weeks 13-14
- **Dependencies**: WORK-202
- **Acceptance**: kNN search functional, persistence to disk, performance baseline met
- **Reference**: [Unified Design 5.4](../design/work-034-e-003-unified-design.md#54-isemanticindex)

#### 203.1: Semantic Index Port

**Files**: `src/domain/ports/semantic_index.py`

- [ ] **203.1.1: ISemanticIndex Interface**
  - [ ] RED: Write failing tests for port
    - [ ] `tests/unit/domain/ports/test_semantic_index.py`
    - [ ] Test: add(id, embedding) adds vector
    - [ ] Test: update(id, embedding) updates vector
    - [ ] Test: remove(id) removes vector
    - [ ] Test: search(query_embedding, k) returns k nearest
    - [ ] Test: search_by_text(text, k) embeds and searches
    - [ ] Test: save(path) persists index
    - [ ] Test: load(path) restores index
    - [ ] Test: rebuild() rebuilds index from source
    - [ ] Contract: Port is abstract
  - [ ] GREEN: Implement port interface
  - [ ] REFACTOR: Add SearchResult value object

- [ ] **203.1.2: SearchResult Value Object**
  - [ ] RED: Write failing tests
    - [ ] `tests/unit/domain/value_objects/test_search_result.py`
    - [ ] Test: SearchResult has id, score, metadata
    - [ ] Test: SearchResult is immutable
    - [ ] Test: SearchResult comparable by score
  - [ ] GREEN: Implement `src/domain/value_objects/search_result.py`
  - [ ] REFACTOR: Add ranking helpers

#### 203.2: FAISS Semantic Index Adapter

**Files**: `src/infrastructure/search/`

- [ ] **203.2.1: FAISS Index CRUD**
  - [ ] RED: Write failing integration tests
    - [ ] `tests/integration/search/test_faiss_semantic_index.py`
    - [ ] Test: add() inserts embedding with ID
    - [ ] Test: update() replaces embedding
    - [ ] Test: remove() deletes embedding
    - [ ] Test: ID mapping maintained correctly
    - [ ] Edge: Add with existing ID updates
    - [ ] Edge: Remove non-existent ID is no-op
    - [ ] Negative: Mismatched embedding dimension raises DimensionError
  - [ ] GREEN: Implement `src/infrastructure/search/faiss_semantic_index.py`
  - [ ] REFACTOR: Add batch operations

- [ ] **203.2.2: FAISS Search**
  - [ ] RED: Write failing tests for search
    - [ ] `tests/integration/search/test_faiss_search.py`
    - [ ] Test: search(embedding, k=5) returns 5 nearest
    - [ ] Test: Results ordered by similarity (closest first)
    - [ ] Test: search() with k > count returns all
    - [ ] Test: search() on empty index returns empty
    - [ ] Edge: Search with exact match returns score ~1.0
    - [ ] Edge: Search with k=0 returns empty
  - [ ] GREEN: Implement search functionality
  - [ ] REFACTOR: Add score normalization

- [ ] **203.2.3: FAISS Persistence**
  - [ ] RED: Write failing tests for persistence
    - [ ] `tests/integration/search/test_faiss_persistence.py`
    - [ ] Test: save() writes index to file
    - [ ] Test: load() restores index from file
    - [ ] Test: Round-trip preserves embeddings and IDs
    - [ ] Test: Load non-existent file returns empty index
    - [ ] Edge: Large index (1000 embeddings) save/load
    - [ ] Negative: Corrupted file raises IndexCorruptionError
  - [ ] GREEN: Implement save/load with faiss.write_index
  - [ ] REFACTOR: Add index metadata

- [ ] **203.2.4: Embedding Provider**
  - [ ] RED: Write failing tests
    - [ ] `tests/unit/search/test_embedding_provider.py`
    - [ ] Test: embed_text() returns fixed-dimension vector
    - [ ] Test: Consistent embeddings for same text
    - [ ] Test: Different texts have different embeddings
    - [ ] Edge: Empty text handling
    - [ ] Edge: Very long text handling
  - [ ] GREEN: Implement `src/infrastructure/search/embedding_provider.py`
  - [ ] REFACTOR: Add caching

#### 203.3: Performance Baseline

- [ ] **203.3.1: Semantic Index Performance Tests**
  - [ ] `tests/performance/search/test_faiss_performance.py`
  - [ ] Benchmark: Add 1000 embeddings < 1s
  - [ ] Benchmark: kNN search (k=10) < 50ms
  - [ ] Benchmark: Save/load 1000 embeddings < 500ms
  - [ ] Document baseline metrics in `docs/performance/search-baseline.md`

---

### WORK-204: RDF Serialization Implementation

- **Status**: PENDING
- **Duration**: Weeks 15-16
- **Dependencies**: WORK-202, WORK-203
- **Acceptance**: Export to Turtle/JSON-LD, SPARQL queries work
- **Reference**: [Unified Design 5.6](../design/work-034-e-003-unified-design.md#56-irdfserializer)

#### 204.1: RDF Serializer Port

**Files**: `src/domain/ports/rdf_serializer.py`

- [ ] **204.1.1: IRDFSerializer Interface**
  - [ ] RED: Write failing tests for port
    - [ ] `tests/unit/domain/ports/test_rdf_serializer.py`
    - [ ] Test: add_triple(s, p, o) adds RDF triple
    - [ ] Test: add_entity(entity) converts to triples
    - [ ] Test: serialize(format) returns string (turtle, xml, json-ld, n3)
    - [ ] Test: save(path, format) writes to file
    - [ ] Test: load(path) reads from file
    - [ ] Test: query(sparql) executes SPARQL query
    - [ ] Contract: Port is abstract
  - [ ] GREEN: Implement port interface
  - [ ] REFACTOR: Add namespace management

#### 204.2: RDFLib Serializer Adapter

**Files**: `src/infrastructure/rdf/`

- [ ] **204.2.1: RDF Graph Operations**
  - [ ] RED: Write failing integration tests
    - [ ] `tests/integration/rdf/test_rdflib_serializer.py`
    - [ ] Test: add_triple() adds to graph
    - [ ] Test: add_entity() creates multiple triples
    - [ ] Test: Graph uses Jerry namespace
    - [ ] Edge: Add duplicate triple is no-op
    - [ ] Negative: Invalid URI raises URIError
  - [ ] GREEN: Implement `src/infrastructure/rdf/rdflib_serializer.py`
  - [ ] REFACTOR: Add namespace prefix management

- [ ] **204.2.2: RDF Serialization**
  - [ ] RED: Write failing tests for serialization
    - [ ] `tests/integration/rdf/test_rdf_serialization.py`
    - [ ] Test: serialize("turtle") returns valid Turtle
    - [ ] Test: serialize("xml") returns valid RDF/XML
    - [ ] Test: serialize("json-ld") returns valid JSON-LD
    - [ ] Test: serialize("n3") returns valid N3
    - [ ] Test: save() writes to file
    - [ ] Test: load() reads from file
    - [ ] Test: Round-trip preserves data
    - [ ] Edge: Empty graph serializes to minimal output
  - [ ] GREEN: Implement serialization methods
  - [ ] REFACTOR: Add format validation

- [ ] **204.2.3: SPARQL Query**
  - [ ] RED: Write failing tests for SPARQL
    - [ ] `tests/integration/rdf/test_sparql_query.py`
    - [ ] Test: Simple SELECT query returns results
    - [ ] Test: FILTER query works
    - [ ] Test: ASK query returns boolean
    - [ ] Test: CONSTRUCT query returns graph
    - [ ] Edge: Query on empty graph returns empty
    - [ ] Negative: Invalid SPARQL raises QuerySyntaxError
  - [ ] GREEN: Implement query method
  - [ ] REFACTOR: Add query caching

- [ ] **204.2.4: Jerry Ontology**
  - [ ] `src/infrastructure/rdf/jerry_ontology.py`
  - [ ] Define Jerry namespace
  - [ ] Define Task, Phase, Plan classes
  - [ ] Define relationships (hasTask, belongsToPhase, etc.)
  - [ ] Define KnowledgeItem, Pattern, Lesson classes
  - [ ] Write ontology tests

#### 204.3: Phase 2 Go/No-Go Gate

- [ ] **204.3.1: Quality Gates**
  - [ ] All Phase 2 unit tests pass
  - [ ] All integration tests pass
  - [ ] All contract tests pass
  - [ ] Performance baselines documented
  - [ ] Work Tracker entities stored in graph
  - [ ] Events stored in event store
  - [ ] Code review approved
  - [ ] No critical/high security issues

---

## Phase 3: Knowledge Management Integration (Weeks 17-24)

> **Goal**: Implement KM domain entities and integrate with Work Tracker.
> **Reference**: [Unified Design 11 Phase 3](../design/work-034-e-003-unified-design.md#phase-3-knowledge-management-integration-weeks-17-24)

### WORK-301: KM Domain Layer

- **Status**: PENDING
- **Duration**: Weeks 17-18
- **Dependencies**: Phase 2 complete
- **Acceptance**: Pattern, Lesson, Assumption entities with BDD scenarios pass
- **Reference**: [Unified Design 4.3](../design/work-034-e-003-unified-design.md#43-knowledge-management-domain)

#### 301.1: KM Value Objects

**Files**: `src/domain/value_objects/knowledge/`

- [ ] **301.1.1: KnowledgeType Enum**
  - [ ] RED: Write failing tests
    - [ ] `tests/unit/domain/value_objects/knowledge/test_knowledge_type.py`
    - [ ] Test: KnowledgeType.PATTERN, LESSON, ASSUMPTION exist
    - [ ] Test: From string parsing works
    - [ ] Negative: Invalid type raises ValueError
  - [ ] GREEN: Implement `src/domain/value_objects/knowledge/knowledge_type.py`
  - [ ] REFACTOR: Add descriptions

- [ ] **301.1.2: Evidence Value Object**
  - [ ] RED: Write failing tests
    - [ ] `tests/unit/domain/value_objects/knowledge/test_evidence.py`
    - [ ] Test: Evidence has type, source, content, timestamp
    - [ ] Test: Evidence is immutable
    - [ ] Test: Evidence types (OBSERVATION, OUTCOME, REFERENCE, METRIC)
    - [ ] Edge: Empty content raises ValueError
  - [ ] GREEN: Implement `src/domain/value_objects/knowledge/evidence.py`
  - [ ] REFACTOR: Add validation

- [ ] **301.1.3: Confidence Value Object**
  - [ ] RED: Write failing tests
    - [ ] `tests/unit/domain/value_objects/knowledge/test_confidence.py`
    - [ ] Test: Confidence has score (0.0-1.0)
    - [ ] Test: Confidence has justification
    - [ ] Test: Confidence comparable
    - [ ] Edge: Score < 0 raises ValueError
    - [ ] Edge: Score > 1 raises ValueError
  - [ ] GREEN: Implement confidence value object
  - [ ] REFACTOR: Add level helpers (HIGH, MEDIUM, LOW)

#### 301.2: KnowledgeItem Aggregate

**Files**: `src/domain/aggregates/knowledge/`

- [ ] **301.2.1: KnowledgeItem Base**
  - [ ] RED: Write failing tests
    - [ ] `tests/unit/domain/aggregates/knowledge/test_knowledge_item.py`
    - [ ] Test: KnowledgeItem has id, title, description
    - [ ] Test: KnowledgeItem has knowledge_type
    - [ ] Test: KnowledgeItem has tags set
    - [ ] Test: KnowledgeItem has source_uri (optional)
    - [ ] Test: KnowledgeItem has created_at, updated_at
    - [ ] Test: add_evidence() adds evidence
    - [ ] Test: link_to() creates relationship
    - [ ] Edge: Empty title raises ValueError
  - [ ] GREEN: Implement `src/domain/aggregates/knowledge/knowledge_item.py`
  - [ ] REFACTOR: Extract common behavior

- [ ] **301.2.2: Pattern Entity**
  - [ ] RED: Write failing tests
    - [ ] `tests/unit/domain/aggregates/knowledge/test_pattern.py`
    - [ ] Test: Pattern extends KnowledgeItem
    - [ ] Test: Pattern has context, problem, solution, consequences
    - [ ] Test: Pattern has applicability_conditions
    - [ ] Test: Pattern tracks application_count
    - [ ] Test: apply() increments count, emits PatternApplied
    - [ ] Edge: Pattern without solution raises ValidationError
  - [ ] GREEN: Implement `src/domain/aggregates/knowledge/pattern.py`
  - [ ] REFACTOR: Add pattern template

- [ ] **301.2.3: Lesson Entity**
  - [ ] RED: Write failing tests
    - [ ] `tests/unit/domain/aggregates/knowledge/test_lesson.py`
    - [ ] Test: Lesson extends KnowledgeItem
    - [ ] Test: Lesson has observation, reflection, action
    - [ ] Test: Lesson has source_task_id (optional)
    - [ ] Test: Lesson can be materialized to Pattern
    - [ ] Test: materialize() emits LessonMaterialized
    - [ ] Edge: Lesson without observation raises ValidationError
  - [ ] GREEN: Implement `src/domain/aggregates/knowledge/lesson.py`
  - [ ] REFACTOR: Add AAR prompts

- [ ] **301.2.4: Assumption Entity**
  - [ ] RED: Write failing tests
    - [ ] `tests/unit/domain/aggregates/knowledge/test_assumption.py`
    - [ ] Test: Assumption extends KnowledgeItem
    - [ ] Test: Assumption has hypothesis, validation_criteria
    - [ ] Test: Assumption has status (UNTESTED, VALIDATED, INVALIDATED)
    - [ ] Test: validate() sets status, adds evidence
    - [ ] Test: invalidate() sets status, adds evidence
    - [ ] Test: validate() emits AssumptionValidated
    - [ ] Negative: Validate without evidence raises ValidationError
  - [ ] GREEN: Implement `src/domain/aggregates/knowledge/assumption.py`
  - [ ] REFACTOR: Add validation workflow

#### 301.3: KM Domain Events

**Files**: `src/domain/events/knowledge.py`

- [ ] **301.3.1: Knowledge Events**
  - [ ] RED: Write failing tests
    - [ ] `tests/unit/domain/events/test_knowledge_events.py`
    - [ ] Test: PatternCreated, PatternUpdated, PatternApplied
    - [ ] Test: LessonCreated, LessonUpdated, LessonMaterialized
    - [ ] Test: AssumptionCreated, AssumptionValidated, AssumptionInvalidated
    - [ ] Test: EvidenceAdded, KnowledgeLinked
    - [ ] Test: All events CloudEvents 1.0 compliant
  - [ ] GREEN: Implement events
  - [ ] REFACTOR: Ensure consistency with WT events

---

### WORK-302: KM Repository Layer

- **Status**: PENDING
- **Duration**: Weeks 19-20
- **Dependencies**: WORK-301
- **Acceptance**: Full CRUD for knowledge items, integration tests pass
- **Reference**: [Unified Design 5.2](../design/work-034-e-003-unified-design.md#52-iknowledgerepository)

#### 302.1: Knowledge Repository Port

**Files**: `src/domain/ports/knowledge_repository.py`

- [ ] **302.1.1: IKnowledgeRepository Interface**
  - [ ] RED: Write failing tests for port
    - [ ] `tests/unit/domain/ports/test_knowledge_repository.py`
    - [ ] Test: get(id) returns KnowledgeItem
    - [ ] Test: save(item) persists item
    - [ ] Test: delete(id) removes item
    - [ ] Test: list_by_type(type) returns items of type
    - [ ] Test: list_by_tags(tags) returns items with tags
    - [ ] Test: get_by_source(source_uri) returns items from source
    - [ ] Contract: Port is abstract
  - [ ] GREEN: Implement port interface
  - [ ] REFACTOR: Add pagination

#### 302.2: SQLite Knowledge Repository

**Files**: `src/infrastructure/persistence/sqlite_knowledge_repo.py`

- [ ] **302.2.1: Knowledge Schema**
  - [ ] RED: Write failing migration tests
    - [ ] `tests/integration/persistence/test_km_migrations.py`
    - [ ] Test: Creates knowledge_items table
    - [ ] Test: Creates evidence table (1:N)
    - [ ] Test: Creates knowledge_tags junction table
    - [ ] Test: Creates knowledge_links table
  - [ ] GREEN: Implement `migrations/003_knowledge_schema.sql`
  - [ ] REFACTOR: Add indexes

- [ ] **302.2.2: Knowledge CRUD**
  - [ ] RED: Write failing integration tests
    - [ ] `tests/integration/persistence/test_sqlite_knowledge_repo.py`
    - [ ] Test: save() inserts Pattern
    - [ ] Test: save() inserts Lesson
    - [ ] Test: save() inserts Assumption
    - [ ] Test: get() returns correct subtype
    - [ ] Test: delete() removes item and evidence
    - [ ] Test: list_by_type() filters correctly
    - [ ] Test: list_by_tags() filters correctly
    - [ ] Test: get_by_source() finds items
    - [ ] Edge: Update existing item
    - [ ] Negative: Get non-existent returns None
  - [ ] GREEN: Implement repository adapter
  - [ ] REFACTOR: Add polymorphic loading

---

### WORK-303: KM CQRS Implementation

- **Status**: PENDING
- **Duration**: Weeks 21-22
- **Dependencies**: WORK-301, WORK-302
- **Acceptance**: All commands/queries functional, AAR handler working
- **Reference**: [Unified Design 6.3-6.4](../design/work-034-e-003-unified-design.md#63-knowledge-management-commands)

#### 303.1: KM Commands

**Files**: `src/application/commands/km/`

- [ ] **303.1.1: Pattern Commands**
  - [ ] RED: Write failing tests
    - [ ] CreatePatternCommand, UpdatePatternCommand, ApplyPatternCommand
    - [ ] Tests follow WORK-103 pattern
  - [ ] GREEN: Implement commands
  - [ ] REFACTOR: Add validation

- [ ] **303.1.2: Lesson Commands**
  - [ ] RED: Write failing tests
    - [ ] CreateLessonCommand, UpdateLessonCommand, MaterializeLessonCommand
    - [ ] Tests follow WORK-103 pattern
  - [ ] GREEN: Implement commands
  - [ ] REFACTOR: Add validation

- [ ] **303.1.3: Assumption Commands**
  - [ ] RED: Write failing tests
    - [ ] CreateAssumptionCommand, ValidateAssumptionCommand, InvalidateAssumptionCommand
    - [ ] Tests follow WORK-103 pattern
  - [ ] GREEN: Implement commands
  - [ ] REFACTOR: Add validation

- [ ] **303.1.4: Cross-Cutting Commands**
  - [ ] RED: Write failing tests
    - [ ] AddEvidenceCommand, LinkKnowledgeCommand
    - [ ] Tests for linking across types
  - [ ] GREEN: Implement commands
  - [ ] REFACTOR: Add bidirectional linking

#### 303.2: KM Command Handlers

**Files**: `src/application/handlers/commands/km/`

- [ ] **303.2.1: Pattern Handlers**
  - [ ] RED: Write failing unit tests (mocked repo)
    - [ ] CreatePatternHandler, UpdatePatternHandler, ApplyPatternHandler
    - [ ] Tests follow WORK-103 handler pattern
    - [ ] Test event emission
  - [ ] GREEN: Implement handlers
  - [ ] REFACTOR: Extract common behavior

- [ ] **303.2.2: Lesson Handlers**
  - [ ] RED: Write failing unit tests
    - [ ] CreateLessonHandler, UpdateLessonHandler, MaterializeLessonHandler
    - [ ] MaterializeLessonHandler creates Pattern from Lesson
    - [ ] Test graph edge creation
  - [ ] GREEN: Implement handlers
  - [ ] REFACTOR: Add materialization workflow

- [ ] **303.2.3: Assumption Handlers**
  - [ ] RED: Write failing unit tests
    - [ ] CreateAssumptionHandler, ValidateAssumptionHandler, InvalidateAssumptionHandler
    - [ ] Test evidence requirement for validation
  - [ ] GREEN: Implement handlers
  - [ ] REFACTOR: Add notification

#### 303.3: KM Queries

**Files**: `src/application/queries/km/`

- [ ] **303.3.1: KM DTOs**
  - [ ] RED: Write failing tests
    - [ ] PatternDTO, LessonDTO, AssumptionDTO, EvidenceDTO
    - [ ] Tests for from_entity() factories
  - [ ] GREEN: Implement `src/application/dtos/knowledge.py`
  - [ ] REFACTOR: Add serialization

- [ ] **303.3.2: Query Definitions**
  - [ ] RED: Write failing tests
    - [ ] GetKnowledgeQuery, ListPatternsQuery, ListLessonsQuery, ListAssumptionsQuery
    - [ ] SearchKnowledgeQuery (semantic), GetRelatedKnowledgeQuery (graph)
  - [ ] GREEN: Implement queries
  - [ ] REFACTOR: Add pagination

- [ ] **303.3.3: Query Handlers**
  - [ ] RED: Write failing unit tests
    - [ ] Handler for each query type
    - [ ] Semantic search uses ISemanticIndex
    - [ ] Related query uses IGraphStore traversal
  - [ ] GREEN: Implement handlers
  - [ ] REFACTOR: Add caching

#### 303.4: AAR Event Handler

**Files**: `src/application/event_handlers/km/`

- [ ] **303.4.1: AAR Prompt Handler**
  - [ ] RED: Write failing tests
    - [ ] `tests/unit/application/event_handlers/test_aar_prompt_handler.py`
    - [ ] Test: TaskCompleted triggers AAR prompt
    - [ ] Test: PhaseCompleted triggers AAR prompt
    - [ ] Test: Handler creates pending AAR
    - [ ] Test: AAR has what_happened, what_learned, what_next
    - [ ] Edge: Skip AAR for trivial tasks (configurable)
  - [ ] GREEN: Implement `src/application/event_handlers/km/aar_prompt_handler.py`
  - [ ] REFACTOR: Add prompt templates

- [ ] **303.4.2: Materialize Lesson Handler**
  - [ ] RED: Write failing tests
    - [ ] `tests/unit/application/event_handlers/test_materialize_lesson_handler.py`
    - [ ] Test: AARCompleted triggers lesson creation
    - [ ] Test: Lesson links to source task
    - [ ] Test: Lesson added to graph
    - [ ] Test: Lesson embedded in semantic index
  - [ ] GREEN: Implement `src/application/event_handlers/km/materialize_lesson_handler.py`
  - [ ] REFACTOR: Add batching

---

### WORK-304: KM Interface Layer

- **Status**: PENDING
- **Duration**: Weeks 23-24
- **Dependencies**: WORK-303
- **Acceptance**: Full KM operations via CLI and SKILL, cross-domain BDD passes
- **Reference**: [Unified Design 7](../design/work-034-e-003-unified-design.md#7-interface-specifications)

#### 304.1: KM CLI Adapter

**Files**: `src/interface/cli/km_cli.py`

- [ ] **304.1.1: Pattern Subcommand**
  - [ ] RED: Write failing E2E tests
    - [ ] `tests/e2e/cli/test_pattern_cli.py`
    - [ ] Test: `km pattern create` creates pattern
    - [ ] Test: `km pattern list` lists patterns
    - [ ] Test: `km pattern show <id>` shows details
    - [ ] Test: `km pattern apply <id> --task <task_id>` applies pattern
    - [ ] Negative: Create without required fields fails
  - [ ] GREEN: Implement pattern subcommand
  - [ ] REFACTOR: Add interactive mode

- [ ] **304.1.2: Lesson Subcommand**
  - [ ] RED: Write failing E2E tests
    - [ ] `tests/e2e/cli/test_lesson_cli.py`
    - [ ] Test: `km lesson create` creates lesson
    - [ ] Test: `km lesson list` lists lessons
    - [ ] Test: `km lesson show <id>` shows details
    - [ ] Test: `km lesson materialize <id>` creates pattern
    - [ ] Negative: Materialize without observation fails
  - [ ] GREEN: Implement lesson subcommand
  - [ ] REFACTOR: Add AAR wizard

- [ ] **304.1.3: Assumption Subcommand**
  - [ ] RED: Write failing E2E tests
    - [ ] `tests/e2e/cli/test_assumption_cli.py`
    - [ ] Test: `km assumption create` creates assumption
    - [ ] Test: `km assumption list` lists assumptions
    - [ ] Test: `km assumption validate <id> --evidence "..."` validates
    - [ ] Test: `km assumption invalidate <id> --evidence "..."` invalidates
    - [ ] Negative: Validate without evidence fails
  - [ ] GREEN: Implement assumption subcommand
  - [ ] REFACTOR: Add evidence attachment

- [ ] **304.1.4: Search and Related Commands**
  - [ ] RED: Write failing E2E tests
    - [ ] `tests/e2e/cli/test_km_search_cli.py`
    - [ ] Test: `km search "query"` returns semantic results
    - [ ] Test: `km related <id>` returns graph neighbors
    - [ ] Test: Output formats (table, json)
    - [ ] Edge: Empty results handled
  - [ ] GREEN: Implement search commands
  - [ ] REFACTOR: Add result highlighting

#### 304.2: KM SKILL.md

**Files**: `skills/km/SKILL.md`

- [ ] **304.2.1: Skill Documentation**
  - [ ] Create `skills/km/SKILL.md`
  - [ ] Document pattern commands
  - [ ] Document lesson commands
  - [ ] Document assumption commands
  - [ ] Document search and related commands
  - [ ] Add natural language examples
  - [ ] Add quick reference

#### 304.3: Cross-Domain BDD Tests

**Files**: `tests/bdd/cross_domain/`

- [ ] **304.3.1: Task to Lesson Flow**
  - [ ] `tests/bdd/cross_domain/features/task_to_lesson.feature`
  - [ ] Scenario: Complete task triggers AAR prompt
  - [ ] Scenario: Submit AAR creates lesson
  - [ ] Scenario: Lesson links to source task
  - [ ] Scenario: Lesson searchable by task content
  - [ ] Negative Scenario: Skip AAR for cancelled task

- [ ] **304.3.2: Pattern Application Flow**
  - [ ] `tests/bdd/cross_domain/features/pattern_application.feature`
  - [ ] Scenario: Search patterns by problem
  - [ ] Scenario: Apply pattern to task
  - [ ] Scenario: Pattern application_count incremented
  - [ ] Scenario: Applied pattern linked to task
  - [ ] Negative Scenario: Apply inapplicable pattern fails

- [ ] **304.3.3: Assumption Validation Flow**
  - [ ] `tests/bdd/cross_domain/features/assumption_validation.feature`
  - [ ] Scenario: Track assumption on plan
  - [ ] Scenario: Link task to validate assumption
  - [ ] Scenario: Task completion validates assumption
  - [ ] Scenario: Task failure invalidates assumption
  - [ ] Negative Scenario: Validate without task link

#### 304.4: Phase 3 Go/No-Go Gate

- [ ] **304.4.1: Quality Gates**
  - [ ] KM entity CRUD working
  - [ ] AAR prompt flow functional
  - [ ] Semantic search returning results
  - [ ] Graph traversal working
  - [ ] Cross-domain BDD scenarios pass
  - [ ] All unit tests pass (95%+ coverage)
  - [ ] All integration tests pass
  - [ ] Code review approved
  - [ ] No critical/high security issues

---

## Phase 4: Advanced Features (Weeks 25-32)

> **Goal**: Complete cross-domain integration, HybridRAG, and external APIs.
> **Reference**: [Unified Design 11 Phase 4](../design/work-034-e-003-unified-design.md#phase-4-advanced-features-weeks-25-32)

### WORK-401: Cross-Domain Integration

- **Status**: PENDING
- **Duration**: Weeks 25-26
- **Dependencies**: Phase 3 complete
- **Acceptance**: Task→Lesson, Phase→Pattern flows automated
- **Reference**: [Unified Design 4.4](../design/work-034-e-003-unified-design.md#44-cross-domain-integration)

#### 401.1: Cross-Domain Event Handlers

**Files**: `src/application/event_handlers/cross_domain/`

- [ ] **401.1.1: TaskCompleted Handler**
  - [ ] RED: Write failing tests
    - [ ] `tests/unit/application/event_handlers/cross_domain/test_task_completed.py`
    - [ ] Test: Handler triggers AAR prompt creation
    - [ ] Test: Handler updates graph with completion
    - [ ] Test: Handler updates semantic index
    - [ ] Edge: Handler configurable by task type
    - [ ] Negative: Handler failure doesn't block completion
  - [ ] GREEN: Implement `src/application/event_handlers/cross_domain/task_completed_handler.py`
  - [ ] REFACTOR: Add retry logic

- [ ] **401.1.2: PhaseCompleted Handler**
  - [ ] RED: Write failing tests
    - [ ] `tests/unit/application/event_handlers/cross_domain/test_phase_completed.py`
    - [ ] Test: Handler triggers pattern candidate analysis
    - [ ] Test: Handler aggregates lessons from phase
    - [ ] Test: Handler updates graph
  - [ ] GREEN: Implement `src/application/event_handlers/cross_domain/phase_completed_handler.py`
  - [ ] REFACTOR: Add aggregation logic

- [ ] **401.1.3: PatternApplied Handler**
  - [ ] RED: Write failing tests
    - [ ] `tests/unit/application/event_handlers/cross_domain/test_pattern_applied.py`
    - [ ] Test: Handler creates graph edge
    - [ ] Test: Handler tracks application in task
    - [ ] Test: Handler updates pattern stats
  - [ ] GREEN: Implement `src/application/event_handlers/cross_domain/pattern_applied_handler.py`
  - [ ] REFACTOR: Add bidirectional linking

- [ ] **401.1.4: AssumptionValidation Handler**
  - [ ] RED: Write failing tests
    - [ ] `tests/unit/application/event_handlers/cross_domain/test_assumption_validation.py`
    - [ ] Test: Handler updates linked plan
    - [ ] Test: Handler updates graph
    - [ ] Test: Handler triggers notifications
    - [ ] Negative: Invalid assumption blocks related tasks
  - [ ] GREEN: Implement `src/application/event_handlers/cross_domain/assumption_validation_handler.py`
  - [ ] REFACTOR: Add plan impact analysis

#### 401.2: Knowledge Materializer Service

**Files**: `src/application/services/knowledge_materializer.py`

- [ ] **401.2.1: Lesson Materialization**
  - [ ] RED: Write failing tests
    - [ ] `tests/unit/application/services/test_knowledge_materializer.py`
    - [ ] Test: materialize_lesson() creates Pattern
    - [ ] Test: Pattern inherits lesson metadata
    - [ ] Test: Pattern linked to source lesson
    - [ ] Test: Graph edge created
    - [ ] Edge: Multiple lessons combine to pattern
  - [ ] GREEN: Implement materialize_lesson()
  - [ ] REFACTOR: Add template system

- [ ] **401.2.2: Pattern Discovery**
  - [ ] RED: Write failing tests
    - [ ] Test: discover_patterns() finds recurring lessons
    - [ ] Test: Clustering by semantic similarity
    - [ ] Test: Candidate patterns have confidence scores
    - [ ] Edge: No patterns found returns empty
  - [ ] GREEN: Implement discover_patterns()
  - [ ] REFACTOR: Add ML-based clustering

#### 401.3: Graph Enrichment

- [ ] **401.3.1: Auto-Graph Integration**
  - [ ] RED: Write failing tests
    - [ ] `tests/integration/graph/test_auto_enrichment.py`
    - [ ] Test: Task creation adds vertex
    - [ ] Test: Task update updates vertex
    - [ ] Test: Task completion adds edges
    - [ ] Test: Phase creation adds vertex
    - [ ] Test: Knowledge item creation adds vertex
  - [ ] GREEN: Implement auto-enrichment
  - [ ] REFACTOR: Add batch processing

---

### WORK-402: HybridRAG & Pattern Discovery

- **Status**: PENDING
- **Duration**: Weeks 27-28
- **Dependencies**: WORK-401
- **Acceptance**: Semantic + graph retrieval working, pattern candidates surfaced
- **Reference**: [Unified Design 8](../design/work-034-e-003-unified-design.md#8-hybrid-rag-specification)

#### 402.1: HybridRAG Service

**Files**: `src/application/services/hybrid_rag.py`

- [ ] **402.1.1: Hybrid Search**
  - [ ] RED: Write failing tests
    - [ ] `tests/unit/application/services/test_hybrid_rag.py`
    - [ ] Test: search() combines semantic and graph results
    - [ ] Test: Semantic results enriched with graph context
    - [ ] Test: Graph traversal from semantic matches
    - [ ] Test: Result fusion and deduplication
    - [ ] Test: Ranking by relevance score
    - [ ] Edge: Empty semantic results uses graph only
    - [ ] Edge: Empty graph uses semantic only
  - [ ] GREEN: Implement `src/application/services/hybrid_rag.py`
  - [ ] REFACTOR: Add configurable weights

- [ ] **402.1.2: Context Enrichment**
  - [ ] RED: Write failing tests
    - [ ] Test: enrich() adds related items to results
    - [ ] Test: Depth-limited traversal
    - [ ] Test: Filter by relationship type
    - [ ] Edge: Cycle detection in graph
  - [ ] GREEN: Implement enrichment
  - [ ] REFACTOR: Add caching

- [ ] **402.1.3: HybridRAG Query**
  - [ ] RED: Write failing tests
    - [ ] `tests/unit/application/queries/test_hybrid_search.py`
    - [ ] Test: HybridSearchQuery has query text, filters
    - [ ] Test: Handler uses HybridRAG service
    - [ ] Test: Results include context
  - [ ] GREEN: Implement `src/application/queries/hybrid_search.py`
  - [ ] REFACTOR: Add result formatting

#### 402.2: Pattern Discovery Service

**Files**: `src/application/services/pattern_discovery.py`

- [ ] **402.2.1: Lesson Clustering**
  - [ ] RED: Write failing tests
    - [ ] `tests/unit/application/services/test_pattern_discovery.py`
    - [ ] Test: cluster_lessons() groups similar lessons
    - [ ] Test: Clustering by semantic similarity
    - [ ] Test: Minimum cluster size configurable
    - [ ] Test: Clusters have centroid
    - [ ] Edge: Single lesson returns no clusters
  - [ ] GREEN: Implement lesson clustering
  - [ ] REFACTOR: Add cluster quality metrics

- [ ] **402.2.2: Pattern Candidate Generation**
  - [ ] RED: Write failing tests
    - [ ] Test: generate_candidates() creates PatternCandidate from cluster
    - [ ] Test: Candidate has confidence score
    - [ ] Test: Candidate has source lessons
    - [ ] Test: Candidate has proposed context/problem/solution
    - [ ] Edge: Low-confidence candidates filtered
  - [ ] GREEN: Implement candidate generation
  - [ ] REFACTOR: Add LLM-based synthesis option

- [ ] **402.2.3: PatternCandidate Value Object**
  - [ ] RED: Write failing tests
    - [ ] `tests/unit/domain/value_objects/test_pattern_candidate.py`
    - [ ] Test: PatternCandidate has title, confidence, source_lessons
    - [ ] Test: PatternCandidate has proposed_pattern data
    - [ ] Test: PatternCandidate is immutable
  - [ ] GREEN: Implement `src/domain/value_objects/pattern_candidate.py`
  - [ ] REFACTOR: Add validation

---

### WORK-403: External API & Export

- **Status**: PENDING
- **Duration**: Weeks 29-30
- **Dependencies**: WORK-401
- **Acceptance**: SPARQL endpoint functional, RDF export working
- **Reference**: [Unified Design 9](../design/work-034-e-003-unified-design.md#9-external-api-specification)

#### 403.1: SPARQL Endpoint

**Files**: `src/interface/api/sparql_endpoint.py`

- [ ] **403.1.1: Query Endpoint**
  - [ ] RED: Write failing tests
    - [ ] `tests/integration/api/test_sparql_endpoint.py`
    - [ ] Test: POST /sparql accepts query
    - [ ] Test: SELECT returns results
    - [ ] Test: ASK returns boolean
    - [ ] Test: CONSTRUCT returns graph
    - [ ] Test: Content negotiation (json, xml, turtle)
    - [ ] Edge: Empty result set handled
    - [ ] Negative: Invalid SPARQL returns 400
    - [ ] Negative: Query timeout returns 408
  - [ ] GREEN: Implement endpoint
  - [ ] REFACTOR: Add rate limiting

- [ ] **403.1.2: Query Validation**
  - [ ] RED: Write failing tests
    - [ ] Test: Validate query syntax
    - [ ] Test: Reject UPDATE/DELETE queries
    - [ ] Test: Reject CONSTRUCT with external sources
    - [ ] Negative: Injection attempt blocked
  - [ ] GREEN: Implement validation
  - [ ] REFACTOR: Add query logging

#### 403.2: Export/Import Commands

**Files**: `src/application/commands/export.py`, `src/application/commands/import.py`

- [ ] **403.2.1: Export Command**
  - [ ] RED: Write failing tests
    - [ ] `tests/unit/application/commands/test_export.py`
    - [ ] Test: ExportCommand has format, path
    - [ ] Test: Handler exports all entities
    - [ ] Test: Handler exports to Turtle, JSON-LD, RDF/XML
    - [ ] Test: Handler includes relationships
    - [ ] Edge: Large export handled
  - [ ] GREEN: Implement export command and handler
  - [ ] REFACTOR: Add streaming

- [ ] **403.2.2: Import Command**
  - [ ] RED: Write failing tests
    - [ ] `tests/unit/application/commands/test_import.py`
    - [ ] Test: ImportCommand has path, merge_strategy
    - [ ] Test: Handler imports entities
    - [ ] Test: Handler resolves conflicts
    - [ ] Test: Handler validates data
    - [ ] Edge: Duplicate handling
    - [ ] Negative: Invalid format rejected
  - [ ] GREEN: Implement import command and handler
  - [ ] REFACTOR: Add preview mode

- [ ] **403.2.3: CLI Integration**
  - [ ] RED: Write failing E2E tests
    - [ ] `tests/e2e/cli/test_export_cli.py`
    - [ ] Test: `jerry export --format turtle -o out.ttl`
    - [ ] Test: `jerry import data.ttl`
    - [ ] Test: Round-trip preserves data
  - [ ] GREEN: Implement `src/interface/cli/export_cli.py`
  - [ ] REFACTOR: Add progress indicator

---

### WORK-404: Documentation & Final Testing

- **Status**: PENDING
- **Duration**: Weeks 31-32
- **Dependencies**: All
- **Acceptance**: Full documentation, all tests pass, system validated
- **Reference**: Final quality gates

#### 404.1: Integration Test Suite

**Files**: `tests/integration/`

- [ ] **404.1.1: Full Workflow Tests**
  - [ ] `tests/integration/test_full_workflow.py`
  - [ ] Test: Create plan -> phases -> tasks -> complete all
  - [ ] Test: Task completion -> AAR -> Lesson -> Pattern
  - [ ] Test: Search patterns -> apply -> track
  - [ ] Test: Assumption tracking and validation
  - [ ] Test: Export -> delete -> import -> verify

- [ ] **404.1.2: Performance Tests**
  - [ ] `tests/integration/test_performance.py`
  - [ ] Test: 1000 tasks CRUD < 30s
  - [ ] Test: 1000 knowledge items CRUD < 30s
  - [ ] Test: Semantic search (1000 items) < 1s
  - [ ] Test: Graph traversal (1000 vertices, depth 3) < 1s
  - [ ] Test: Memory usage bounded

- [ ] **404.1.3: Data Integrity Tests**
  - [ ] `tests/integration/test_data_integrity.py`
  - [ ] Test: Concurrent operations don't corrupt
  - [ ] Test: Transaction rollback works
  - [ ] Test: Foreign key integrity
  - [ ] Test: Event replay reconstructs state
  - [ ] Test: Snapshot consistency

#### 404.2: User Documentation

**Files**: `docs/user-guide/`

- [ ] **404.2.1: Getting Started Guide**
  - [ ] `docs/user-guide/getting-started.md`
  - [ ] Installation instructions
  - [ ] First task creation
  - [ ] First lesson capture
  - [ ] Quick reference

- [ ] **404.2.2: Work Tracker Guide**
  - [ ] `docs/user-guide/work-tracker.md`
  - [ ] Task management
  - [ ] Phase and plan management
  - [ ] Best practices
  - [ ] Troubleshooting

- [ ] **404.2.3: Knowledge Management Guide**
  - [ ] `docs/user-guide/knowledge-management.md`
  - [ ] Patterns, lessons, assumptions
  - [ ] AAR workflow
  - [ ] Search and discovery
  - [ ] Best practices

- [ ] **404.2.4: CLI Reference**
  - [ ] `docs/user-guide/cli-reference.md`
  - [ ] Complete command reference
  - [ ] Options and flags
  - [ ] Examples
  - [ ] Exit codes

#### 404.3: Developer Documentation

**Files**: `docs/dev-guide/`

- [ ] **404.3.1: Architecture Guide**
  - [ ] `docs/dev-guide/architecture.md`
  - [ ] Hexagonal architecture overview
  - [ ] Domain model
  - [ ] CQRS implementation
  - [ ] Event sourcing
  - [ ] Dependency injection

- [ ] **404.3.2: Extension Guide**
  - [ ] `docs/dev-guide/extending.md`
  - [ ] Adding new entity types
  - [ ] Adding new commands/queries
  - [ ] Adding new adapters
  - [ ] Plugin architecture

- [ ] **404.3.3: Testing Guide**
  - [ ] `docs/dev-guide/testing.md`
  - [ ] Test pyramid
  - [ ] Writing unit tests
  - [ ] Writing integration tests
  - [ ] Writing BDD scenarios
  - [ ] Contract testing

#### 404.4: Final Go/No-Go Gate

- [ ] **404.4.1: Quality Gates**
  - [ ] All unit tests pass (target: 95%+ coverage)
  - [ ] All integration tests pass
  - [ ] All BDD scenarios pass
  - [ ] All E2E tests pass
  - [ ] All contract tests pass
  - [ ] All architecture tests pass
  - [ ] All system tests pass
  - [ ] Performance targets met (<100ms p95)
  - [ ] Documentation complete
  - [ ] Security review passed
  - [ ] Final code review approved
  - [ ] No critical/high issues open

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
| R-003 | Test suite too slow | Medium | Medium | Parallel execution, test isolation |
| R-004 | User AAR adoption | Medium | Medium | Track completion rate |
| R-005 | Schema evolution | Medium | High | Version envelope pattern |
| R-006 | Integration complexity | Medium | Medium | Feature flags, incremental rollout |

---

## Testing Summary by Type

| Test Type | Count (Est.) | Purpose |
|-----------|--------------|---------|
| Unit | ~500 | Isolated component testing |
| Integration | ~150 | Multi-component testing |
| Contract | ~30 | Port compliance |
| System | ~20 | Multi-operation workflows |
| E2E | ~50 | CLI to persistence |
| BDD | ~60 | Business scenarios |
| Architecture | ~20 | Layer dependencies |
| Performance | ~15 | Baseline validation |

**Total Estimated Tests**: ~845

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

*Revised from WORK-034 artifacts on 2026-01-09 with comprehensive Architecture Pure and BDD Red/Green/Refactor sub-tasks*
