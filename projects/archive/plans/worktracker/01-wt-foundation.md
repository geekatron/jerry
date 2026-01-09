# Phase 1: Work Tracker Foundation (Weeks 1-8)

> **Goal**: Deliver a fully integrated vertical slice of Task + Sub-Task with file-based persistence and CLI interface.
> **Reference**: [Index](00-wt-index.md) | [Unified Design](../../design/work-034-e-003-unified-design.md)

**Status**: PENDING
**Duration**: Weeks 1-8
**WORK Items**: WORK-101 to WORK-104

---

## Phase 1 Overview

| WORK Item | Name | Duration | Dependencies |
|-----------|------|----------|--------------|
| WORK-101 | Domain Layer - Aggregates & Ports | Weeks 1-2 | None |
| WORK-102 | File-Based Repository Adapters | Weeks 3-4 | WORK-101 |
| WORK-103 | CQRS Implementation | Weeks 5-6 | WORK-101, WORK-102 |
| WORK-104 | CLI Interface & SKILL.md | Weeks 7-8 | WORK-103 |

---

## WORK-101: Domain Layer - Aggregates & Ports

**Status**: PENDING
**Duration**: Weeks 1-2
**Artifacts**: Domain entities, value objects, events, ports
**Dependencies**: None

### Sub-task 101.1: Shared Kernel Value Objects

**Files**: `src/domain/value_objects/`
**Tests**: `tests/unit/domain/value_objects/`

#### 101.1.1: VertexId Base Class (`vertex_id.py`)

- [ ] **RED**: Write `test_vertex_id.py`
  - [ ] Test valid UUID string creates VertexId
  - [ ] Test invalid UUID format raises `ValueError`
  - [ ] Test equality is by value, not reference
  - [ ] Test immutability - cannot reassign `value` attribute
  - [ ] Test empty string raises `ValueError`
  - [ ] Test whitespace-only string raises `ValueError`
  - [ ] Test `__hash__` returns consistent value for equal IDs
  - [ ] Test `__repr__` returns readable format
  - [ ] Test `__str__` returns raw UUID string
  - [ ] Test `from_string()` factory method
  - [ ] Test `generate()` factory creates valid UUID v4

- [ ] **GREEN**: Implement `VertexId`
  - [ ] Use `@dataclass(frozen=True)` for immutability
  - [ ] Implement UUID v4 validation regex
  - [ ] Implement `__hash__` based on value
  - [ ] Implement `__eq__` for value equality
  - [ ] Implement `generate()` classmethod using `uuid.uuid4()`
  - [ ] Implement `from_string()` classmethod with validation

- [ ] **REFACTOR**: Clean up implementation
  - [ ] Extract validation to private `_validate()` method
  - [ ] Add docstrings with examples
  - [ ] Ensure `__slots__` for memory efficiency

#### 101.1.2: TaskId Value Object (`task_id.py`)

- [ ] **RED**: Write `test_task_id.py`
  - [ ] Test TaskId extends VertexId
  - [ ] Test TaskId is distinct type from SubTaskId (not interchangeable)
  - [ ] Test `None` value raises `TypeError`
  - [ ] Test TaskId can be used as dict key
  - [ ] Test TaskId serializes to string correctly
  - [ ] Test TaskId deserializes from string correctly

- [ ] **GREEN**: Implement `TaskId`
  - [ ] Inherit from `VertexId`
  - [ ] Add type marker for serialization
  - [ ] Implement `__class_getitem__` for type hints

- [ ] **REFACTOR**: Ensure type safety
  - [ ] Add runtime type checking in factory methods
  - [ ] Add docstring with usage examples

#### 101.1.3: SubTaskId Value Object (`subtask_id.py`)

- [ ] **RED**: Write `test_subtask_id.py`
  - [ ] Test SubTaskId extends VertexId
  - [ ] Test SubTaskId is distinct type from TaskId (not interchangeable)
  - [ ] Test `None` value raises `TypeError`
  - [ ] Test SubTaskId can be used as dict key
  - [ ] Test SubTaskId serializes to string correctly
  - [ ] Test SubTaskId deserializes from string correctly

- [ ] **GREEN**: Implement `SubTaskId`
  - [ ] Inherit from `VertexId`
  - [ ] Add type marker for serialization

- [ ] **REFACTOR**: DRY with TaskId
  - [ ] Extract common ID behavior to base class if needed

#### 101.1.4: TaskStatus Enum (`task_status.py`)

- [ ] **RED**: Write `test_task_status.py`
  - [ ] Test all states exist: PENDING, IN_PROGRESS, COMPLETED, BLOCKED, CANCELLED
  - [ ] Test `from_string()` parses case-insensitively
  - [ ] Test invalid string raises `ValueError`
  - [ ] Test `can_transition_to()` validates state machine:
    - [ ] PENDING → IN_PROGRESS: valid
    - [ ] PENDING → CANCELLED: valid
    - [ ] PENDING → COMPLETED: invalid (must go through IN_PROGRESS)
    - [ ] IN_PROGRESS → COMPLETED: valid
    - [ ] IN_PROGRESS → BLOCKED: valid
    - [ ] IN_PROGRESS → CANCELLED: valid
    - [ ] BLOCKED → IN_PROGRESS: valid (unblock)
    - [ ] BLOCKED → CANCELLED: valid
    - [ ] COMPLETED → any: invalid (terminal state)
    - [ ] CANCELLED → any: invalid (terminal state)
  - [ ] Test `is_terminal` property returns True for COMPLETED, CANCELLED
  - [ ] Test `is_active` property returns True for IN_PROGRESS, BLOCKED

- [ ] **GREEN**: Implement `TaskStatus`
  - [ ] Use `Enum` with string values
  - [ ] Implement `can_transition_to(target: TaskStatus) -> bool`
  - [ ] Implement `from_string(value: str) -> TaskStatus`
  - [ ] Implement `is_terminal` property
  - [ ] Implement `is_active` property
  - [ ] Define transition matrix as class constant

- [ ] **REFACTOR**: Add state machine diagram in docstring
  - [ ] Document all valid transitions
  - [ ] Add examples of invalid transitions

#### 101.1.5: SubTaskStatus Enum (`subtask_status.py`)

- [ ] **RED**: Write `test_subtask_status.py`
  - [ ] Test all states exist: PENDING, IN_PROGRESS, COMPLETED, SKIPPED
  - [ ] Test `from_string()` parses case-insensitively
  - [ ] Test invalid string raises `ValueError`
  - [ ] Test `can_transition_to()` validates state machine:
    - [ ] PENDING → IN_PROGRESS: valid
    - [ ] PENDING → SKIPPED: valid
    - [ ] IN_PROGRESS → COMPLETED: valid
    - [ ] IN_PROGRESS → SKIPPED: valid
    - [ ] COMPLETED → any: invalid (terminal)
    - [ ] SKIPPED → any: invalid (terminal)
  - [ ] Test `is_terminal` property

- [ ] **GREEN**: Implement `SubTaskStatus`
  - [ ] Simpler state machine than TaskStatus (no BLOCKED)
  - [ ] Include SKIPPED state for optional sub-tasks

- [ ] **REFACTOR**: Extract common enum patterns
  - [ ] Consider base StatusEnum class

#### 101.1.6: Priority Enum (`priority.py`)

- [ ] **RED**: Write `test_priority.py`
  - [ ] Test all levels exist: LOW, NORMAL, HIGH, CRITICAL
  - [ ] Test ordering: LOW < NORMAL < HIGH < CRITICAL
  - [ ] Test `__lt__`, `__le__`, `__gt__`, `__ge__` operators
  - [ ] Test `from_string()` parses case-insensitively
  - [ ] Test `from_int()` maps 1-4 to priorities
  - [ ] Test invalid string raises `ValueError`
  - [ ] Test invalid int raises `ValueError`
  - [ ] Test default is NORMAL

- [ ] **GREEN**: Implement `Priority`
  - [ ] Use `IntEnum` for natural ordering
  - [ ] Values: LOW=1, NORMAL=2, HIGH=3, CRITICAL=4
  - [ ] Implement `from_string()` classmethod
  - [ ] Implement `from_int()` classmethod

- [ ] **REFACTOR**: Add display names
  - [ ] Add `display_name` property for UI

#### 101.1.7: Tag Value Object (`tag.py`)

- [ ] **RED**: Write `test_tag.py`
  - [ ] Test valid tag creation with alphanumeric + hyphen
  - [ ] Test tag is normalized to lowercase
  - [ ] Test leading/trailing whitespace is trimmed
  - [ ] Test max length enforcement (50 chars)
  - [ ] Test empty string raises `ValueError`
  - [ ] Test special characters (except hyphen) raise `ValueError`
  - [ ] Test spaces raise `ValueError`
  - [ ] Test equality is case-insensitive
  - [ ] Test `__hash__` works with normalized value

- [ ] **GREEN**: Implement `Tag`
  - [ ] Use `@dataclass(frozen=True)`
  - [ ] Normalize in `__post_init__`
  - [ ] Validate with regex: `^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$`

- [ ] **REFACTOR**: Add tag parsing
  - [ ] Add `parse_tags(text: str) -> list[Tag]` for comma-separated input

---

### Sub-task 101.2: Task Aggregate Root

**Files**: `src/domain/aggregates/task.py`
**Tests**: `tests/unit/domain/aggregates/test_task.py`

#### 101.2.1: Task Entity Core

- [ ] **RED**: Write `test_task_creation.py`
  - [ ] Test create with title only (defaults applied)
  - [ ] Test create with title and description
  - [ ] Test create with all optional fields (priority, tags, due_date)
  - [ ] Test auto-generated TaskId is valid UUID
  - [ ] Test initial status is PENDING
  - [ ] Test created_at is set to current time
  - [ ] Test updated_at equals created_at initially
  - [ ] Test version starts at 1
  - [ ] Test empty title raises `ValueError`
  - [ ] Test whitespace-only title raises `ValueError`
  - [ ] Test title > 200 chars raises `ValueError`
  - [ ] Test description > 5000 chars raises `ValueError`
  - [ ] Test due_date in past raises `ValueError` (configurable)
  - [ ] Test `TaskCreated` event is emitted

- [ ] **GREEN**: Implement `Task.__init__()` and `Task.create()`
  - [ ] Private `__init__` for reconstitution
  - [ ] Public `create()` factory for new tasks
  - [ ] Emit `TaskCreated` event from factory
  - [ ] Store pending events in `_events` list

- [ ] **REFACTOR**: Extract validation
  - [ ] Create `_validate_title()`, `_validate_description()` private methods
  - [ ] Add comprehensive docstrings

#### 101.2.2: Task State Transitions

- [ ] **RED**: Write `test_task_transitions.py`
  - [ ] Test `start()` transitions PENDING → IN_PROGRESS
  - [ ] Test `start()` emits `TaskStarted` event
  - [ ] Test `start()` on IN_PROGRESS raises `InvalidStateError`
  - [ ] Test `start()` on COMPLETED raises `InvalidStateError`
  - [ ] Test `complete()` transitions IN_PROGRESS → COMPLETED
  - [ ] Test `complete()` sets `completed_at` timestamp
  - [ ] Test `complete()` emits `TaskCompleted` event
  - [ ] Test `complete()` with notes stores completion notes
  - [ ] Test `complete()` on PENDING raises `InvalidStateError`
  - [ ] Test `complete()` on BLOCKED raises `InvalidStateError`
  - [ ] Test `block(reason)` transitions IN_PROGRESS → BLOCKED
  - [ ] Test `block()` requires reason string
  - [ ] Test `block()` emits `TaskBlocked` event
  - [ ] Test `block()` on PENDING raises `InvalidStateError`
  - [ ] Test `unblock()` transitions BLOCKED → IN_PROGRESS
  - [ ] Test `unblock()` clears blocker_reason
  - [ ] Test `unblock()` emits `TaskUnblocked` event
  - [ ] Test `cancel()` transitions PENDING/IN_PROGRESS/BLOCKED → CANCELLED
  - [ ] Test `cancel()` on COMPLETED raises `InvalidStateError`
  - [ ] Test `cancel()` emits `TaskCancelled` event
  - [ ] Test all transitions increment version
  - [ ] Test all transitions update `updated_at`

- [ ] **GREEN**: Implement transition methods
  - [ ] `start() -> None`
  - [ ] `complete(notes: str | None = None) -> None`
  - [ ] `block(reason: str) -> None`
  - [ ] `unblock() -> None`
  - [ ] `cancel() -> None`
  - [ ] Use `TaskStatus.can_transition_to()` for validation
  - [ ] Raise `InvalidStateError` with descriptive message

- [ ] **REFACTOR**: Implement state pattern or transition table
  - [ ] Consider `_transition(new_status, event_factory)` helper

#### 101.2.3: Task Attribute Updates

- [ ] **RED**: Write `test_task_updates.py`
  - [ ] Test `update_title(new_title)` changes title
  - [ ] Test `update_title()` emits `TaskUpdated` event
  - [ ] Test `update_title()` with invalid title raises `ValueError`
  - [ ] Test `update_title()` on COMPLETED raises `InvalidStateError`
  - [ ] Test `update_description(new_desc)` changes description
  - [ ] Test `update_description()` with None clears description
  - [ ] Test `set_priority(priority)` changes priority
  - [ ] Test `set_priority()` emits `TaskUpdated` event
  - [ ] Test `set_due_date(date)` changes due_date
  - [ ] Test `set_due_date(None)` clears due_date
  - [ ] Test `set_due_date()` with past date raises `ValueError`
  - [ ] Test `add_tag(tag)` adds tag to set
  - [ ] Test `add_tag()` with duplicate tag is no-op (idempotent)
  - [ ] Test `add_tag()` emits `TaskTagAdded` event (first time only)
  - [ ] Test `remove_tag(tag)` removes tag from set
  - [ ] Test `remove_tag()` with non-existent tag is no-op
  - [ ] Test `remove_tag()` emits `TaskTagRemoved` event (if existed)
  - [ ] Test all updates increment version
  - [ ] Test all updates set `updated_at`

- [ ] **GREEN**: Implement update methods
  - [ ] `update_title(title: str) -> None`
  - [ ] `update_description(description: str | None) -> None`
  - [ ] `set_priority(priority: Priority) -> None`
  - [ ] `set_due_date(due_date: datetime | None) -> None`
  - [ ] `add_tag(tag: Tag) -> None`
  - [ ] `remove_tag(tag: Tag) -> None`

- [ ] **REFACTOR**: Add bulk update method
  - [ ] `update(**kwargs)` for multiple fields at once
  - [ ] Single event emission for bulk update

#### 101.2.4: Task Sub-Task References

- [ ] **RED**: Write `test_task_subtask_refs.py`
  - [ ] Test `subtask_ids` property returns frozenset of SubTaskIds
  - [ ] Test `add_subtask_reference(subtask_id)` adds reference
  - [ ] Test `add_subtask_reference()` emits `SubTaskLinked` event
  - [ ] Test `add_subtask_reference()` with duplicate is no-op
  - [ ] Test `remove_subtask_reference(subtask_id)` removes reference
  - [ ] Test `remove_subtask_reference()` emits `SubTaskUnlinked` event
  - [ ] Test `has_subtask(subtask_id)` returns boolean
  - [ ] Test `subtask_count` property returns count
  - [ ] Test cannot complete Task if has incomplete sub-tasks (configurable)

- [ ] **GREEN**: Implement sub-task reference methods
  - [ ] Store references as `frozenset[SubTaskId]`
  - [ ] Reference only - actual SubTask is separate aggregate

- [ ] **REFACTOR**: Add sub-task query helpers
  - [ ] Document relationship with SubTask aggregate

---

### Sub-task 101.3: Sub-Task Aggregate Root

**Files**: `src/domain/aggregates/subtask.py`
**Tests**: `tests/unit/domain/aggregates/test_subtask.py`

#### 101.3.1: SubTask Entity Core

- [ ] **RED**: Write `test_subtask_creation.py`
  - [ ] Test create with title and parent task_id
  - [ ] Test create with optional description, order_index
  - [ ] Test auto-generated SubTaskId is valid UUID
  - [ ] Test initial status is PENDING
  - [ ] Test created_at is set to current time
  - [ ] Test version starts at 1
  - [ ] Test parent task_id is required
  - [ ] Test parent task_id cannot be changed after creation
  - [ ] Test empty title raises `ValueError`
  - [ ] Test title > 200 chars raises `ValueError`
  - [ ] Test order_index defaults to 0
  - [ ] Test `SubTaskCreated` event is emitted

- [ ] **GREEN**: Implement `SubTask.__init__()` and `SubTask.create()`
  - [ ] Private `__init__` for reconstitution
  - [ ] Public `create(task_id, title, ...)` factory
  - [ ] Emit `SubTaskCreated` event from factory

- [ ] **REFACTOR**: Ensure consistency with Task
  - [ ] Follow same patterns for validation, events

#### 101.3.2: SubTask State Transitions

- [ ] **RED**: Write `test_subtask_transitions.py`
  - [ ] Test `start()` transitions PENDING → IN_PROGRESS
  - [ ] Test `start()` emits `SubTaskStarted` event
  - [ ] Test `complete()` transitions IN_PROGRESS → COMPLETED
  - [ ] Test `complete()` sets `completed_at` timestamp
  - [ ] Test `complete()` emits `SubTaskCompleted` event
  - [ ] Test `skip(reason)` transitions PENDING → SKIPPED
  - [ ] Test `skip()` with reason stores skip_reason
  - [ ] Test `skip()` emits `SubTaskSkipped` event
  - [ ] Test `skip()` on IN_PROGRESS is valid (can skip after starting)
  - [ ] Test invalid transitions raise `InvalidStateError`
  - [ ] Test all transitions increment version
  - [ ] Test all transitions update `updated_at`

- [ ] **GREEN**: Implement transition methods
  - [ ] `start() -> None`
  - [ ] `complete() -> None`
  - [ ] `skip(reason: str | None = None) -> None`

- [ ] **REFACTOR**: Simpler state machine than Task
  - [ ] No BLOCKED state for sub-tasks
  - [ ] No CANCELLED state (use SKIPPED)

#### 101.3.3: SubTask Attribute Updates

- [ ] **RED**: Write `test_subtask_updates.py`
  - [ ] Test `update_title(new_title)` changes title
  - [ ] Test `update_description(new_desc)` changes description
  - [ ] Test `set_order_index(index)` changes order
  - [ ] Test all updates emit `SubTaskUpdated` event
  - [ ] Test all updates increment version
  - [ ] Test updates on COMPLETED raise `InvalidStateError`
  - [ ] Test updates on SKIPPED raise `InvalidStateError`

- [ ] **GREEN**: Implement update methods
  - [ ] `update_title(title: str) -> None`
  - [ ] `update_description(description: str | None) -> None`
  - [ ] `set_order_index(index: int) -> None`

- [ ] **REFACTOR**: Consistency with Task update patterns

---

### Sub-task 101.4: Domain Events

**Files**: `src/domain/events/`
**Tests**: `tests/unit/domain/events/`

#### 101.4.1: Event Base Classes (`base.py`)

- [ ] **RED**: Write `test_domain_event_base.py`
  - [ ] Test `DomainEvent` is immutable (frozen dataclass)
  - [ ] Test `event_id` is auto-generated UUID
  - [ ] Test `occurred_at` is auto-generated timestamp
  - [ ] Test `aggregate_id` is required
  - [ ] Test `aggregate_type` is required
  - [ ] Test `event_type` returns class name
  - [ ] Test `to_dict()` returns serializable dict
  - [ ] Test `from_dict()` reconstructs event

- [ ] **GREEN**: Implement `DomainEvent` base class
  - [ ] `@dataclass(frozen=True)`
  - [ ] Auto-generated `event_id: str`
  - [ ] Auto-generated `occurred_at: datetime`
  - [ ] Abstract `aggregate_id: str`
  - [ ] Abstract `aggregate_type: str`

- [ ] **REFACTOR**: Add CloudEvents envelope support
  - [ ] Prepare for CloudEvents 1.0 compliance in Phase 2

#### 101.4.2: Task Events (`task_events.py`)

- [ ] **RED**: Write `test_task_events.py`
  - [ ] Test `TaskCreated` has all task fields
  - [ ] Test `TaskStarted` has task_id, timestamp
  - [ ] Test `TaskCompleted` has task_id, completed_at, notes
  - [ ] Test `TaskBlocked` has task_id, reason
  - [ ] Test `TaskUnblocked` has task_id
  - [ ] Test `TaskCancelled` has task_id
  - [ ] Test `TaskUpdated` has task_id, changed_fields dict
  - [ ] Test `TaskTagAdded` has task_id, tag
  - [ ] Test `TaskTagRemoved` has task_id, tag
  - [ ] Test `SubTaskLinked` has task_id, subtask_id
  - [ ] Test `SubTaskUnlinked` has task_id, subtask_id
  - [ ] Test all events extend `DomainEvent`
  - [ ] Test all events are immutable

- [ ] **GREEN**: Implement Task events
  - [ ] One event class per significant state change
  - [ ] Include all relevant data for event sourcing

- [ ] **REFACTOR**: Group related events
  - [ ] Consider event versioning strategy

#### 101.4.3: SubTask Events (`subtask_events.py`)

- [ ] **RED**: Write `test_subtask_events.py`
  - [ ] Test `SubTaskCreated` has all subtask fields + task_id
  - [ ] Test `SubTaskStarted` has subtask_id, timestamp
  - [ ] Test `SubTaskCompleted` has subtask_id, completed_at
  - [ ] Test `SubTaskSkipped` has subtask_id, reason
  - [ ] Test `SubTaskUpdated` has subtask_id, changed_fields
  - [ ] Test all events extend `DomainEvent`
  - [ ] Test all events include parent task_id for correlation

- [ ] **GREEN**: Implement SubTask events
  - [ ] Include `task_id` in all events for correlation

- [ ] **REFACTOR**: Ensure event naming consistency

---

### Sub-task 101.5: Repository Ports

**Files**: `src/domain/ports/`
**Tests**: `tests/unit/domain/ports/`

#### 101.5.1: Task Repository Port (`task_repository.py`)

- [ ] **RED**: Write `test_task_repository_port.py`
  - [ ] Test `ITaskRepository` is ABC
  - [ ] Test `get(task_id)` returns `Task | None`
  - [ ] Test `save(task)` returns `None`
  - [ ] Test `delete(task_id)` returns `bool`
  - [ ] Test `list_all()` returns `list[Task]`
  - [ ] Test `list_by_status(status)` returns filtered list
  - [ ] Test `list_by_priority(priority)` returns filtered list
  - [ ] Test `list_by_tag(tag)` returns filtered list
  - [ ] Test `exists(task_id)` returns `bool`
  - [ ] Test all methods are abstract

- [ ] **GREEN**: Implement `ITaskRepository` ABC
  - [ ] Define all method signatures with type hints
  - [ ] Add docstrings with contracts

- [ ] **REFACTOR**: Add query specification pattern
  - [ ] Consider `TaskQuery` dataclass for complex queries

#### 101.5.2: SubTask Repository Port (`subtask_repository.py`)

- [ ] **RED**: Write `test_subtask_repository_port.py`
  - [ ] Test `ISubTaskRepository` is ABC
  - [ ] Test `get(subtask_id)` returns `SubTask | None`
  - [ ] Test `save(subtask)` returns `None`
  - [ ] Test `delete(subtask_id)` returns `bool`
  - [ ] Test `list_by_task(task_id)` returns list ordered by `order_index`
  - [ ] Test `list_by_status(status)` returns filtered list
  - [ ] Test `exists(subtask_id)` returns `bool`
  - [ ] Test `count_by_task(task_id)` returns count
  - [ ] Test `count_incomplete_by_task(task_id)` returns count of non-terminal

- [ ] **GREEN**: Implement `ISubTaskRepository` ABC
  - [ ] Define all method signatures
  - [ ] Add docstrings

- [ ] **REFACTOR**: Add bulk operations
  - [ ] `save_all(subtasks: list[SubTask])` for efficiency

#### 101.5.3: Unit of Work Port (`unit_of_work.py`)

- [ ] **RED**: Write `test_unit_of_work_port.py`
  - [ ] Test `IUnitOfWork` is ABC
  - [ ] Test `task_repository` property returns `ITaskRepository`
  - [ ] Test `subtask_repository` property returns `ISubTaskRepository`
  - [ ] Test `commit()` is abstract
  - [ ] Test `rollback()` is abstract
  - [ ] Test context manager protocol (`__enter__`, `__exit__`)
  - [ ] Test `__exit__` calls rollback on exception

- [ ] **GREEN**: Implement `IUnitOfWork` ABC
  - [ ] Repository properties
  - [ ] Transaction methods
  - [ ] Context manager protocol

- [ ] **REFACTOR**: Add event collection
  - [ ] `collect_events()` to gather events from all aggregates

---

### Sub-task 101.6: Domain Exceptions

**Files**: `src/domain/exceptions.py`
**Tests**: `tests/unit/domain/test_exceptions.py`

#### 101.6.1: Exception Hierarchy

- [ ] **RED**: Write `test_domain_exceptions.py`
  - [ ] Test `DomainError` is base exception
  - [ ] Test `DomainError` has `message` attribute
  - [ ] Test `EntityNotFoundError` has `entity_type`, `entity_id`
  - [ ] Test `EntityNotFoundError` message includes type and ID
  - [ ] Test `InvalidStateError` has `current_state`, `attempted_action`
  - [ ] Test `InvalidStateTransitionError` has `from_state`, `to_state`
  - [ ] Test `ValidationError` has `field`, `message`, `value`
  - [ ] Test `ConcurrencyError` has `expected_version`, `actual_version`
  - [ ] Test all exceptions are serializable

- [ ] **GREEN**: Implement exception hierarchy
  - [ ] `DomainError(Exception)`
  - [ ] `EntityNotFoundError(DomainError)`
  - [ ] `InvalidStateError(DomainError)`
  - [ ] `InvalidStateTransitionError(InvalidStateError)`
  - [ ] `ValidationError(DomainError)`
  - [ ] `ConcurrencyError(DomainError)`

- [ ] **REFACTOR**: Add error codes
  - [ ] Unique error codes for each exception type

---

### Sub-task 101.7: Architecture Tests

**Files**: `tests/architecture/`

#### 101.7.1: Layer Dependency Tests

- [ ] **RED**: Write `test_domain_architecture.py`
  - [ ] Test domain/ has no imports from application/
  - [ ] Test domain/ has no imports from infrastructure/
  - [ ] Test domain/ has no imports from interface/
  - [ ] Test domain/ only imports from stdlib + domain/
  - [ ] Test all aggregates extend proper base
  - [ ] Test all value objects are frozen dataclasses
  - [ ] Test all events are frozen dataclasses
  - [ ] Test all ports are ABCs
  - [ ] Test no concrete implementations in domain/

- [ ] **GREEN**: Implement architecture validation
  - [ ] Use AST parsing or import analysis
  - [ ] Fail fast on violations

- [ ] **REFACTOR**: Add to CI pipeline
  - [ ] Run on every commit

---

## WORK-102: File-Based Repository Adapters

**Status**: PENDING
**Duration**: Weeks 3-4
**Artifacts**: JSON adapter, TOON adapter, file management
**Dependencies**: WORK-101

### Sub-task 102.1: File Store Infrastructure

**Files**: `src/infrastructure/persistence/`
**Tests**: `tests/integration/persistence/`

#### 102.1.1: File Store Base (`file_store.py`)

- [ ] **RED**: Write `test_file_store.py`
  - [ ] Test `FileStore` creates directory if not exists
  - [ ] Test `FileStore` with custom base path
  - [ ] Test `get_file_path(entity_type, entity_id)` returns correct path
  - [ ] Test `read_file(path)` returns content or None if not exists
  - [ ] Test `write_file(path, content)` creates/overwrites file
  - [ ] Test `delete_file(path)` removes file, returns bool
  - [ ] Test `list_files(entity_type)` returns all files in directory
  - [ ] Test `file_exists(path)` returns bool
  - [ ] Test atomic write (write to temp, then rename)
  - [ ] Test handles concurrent reads safely
  - [ ] Test handles special characters in IDs
  - [ ] Test handles very long content

- [ ] **GREEN**: Implement `FileStore`
  - [ ] Base path configuration
  - [ ] Directory management
  - [ ] Atomic write operations
  - [ ] File listing with glob

- [ ] **REFACTOR**: Add file locking
  - [ ] Optional locking for concurrent writes
  - [ ] Consider `fcntl` or `portalocker`

#### 102.1.2: Serialization Port (`serialization.py`)

- [ ] **RED**: Write `test_serialization_port.py`
  - [ ] Test `ISerializer` is ABC
  - [ ] Test `serialize(entity)` returns string
  - [ ] Test `deserialize(data, entity_type)` returns entity
  - [ ] Test `file_extension` property returns extension
  - [ ] Test `content_type` property returns MIME type

- [ ] **GREEN**: Implement `ISerializer` ABC
  - [ ] Generic serialization interface
  - [ ] Support for entity type hints

- [ ] **REFACTOR**: Add schema versioning
  - [ ] Version field in serialized output

---

### Sub-task 102.2: JSON Adapter

**Files**: `src/infrastructure/persistence/json_adapter.py`
**Tests**: `tests/integration/persistence/test_json_adapter.py`

#### 102.2.1: JSON Serializer

- [ ] **RED**: Write `test_json_serializer.py`
  - [ ] Test Task serializes to valid JSON
  - [ ] Test Task JSON includes all fields
  - [ ] Test Task deserializes back to equal entity
  - [ ] Test SubTask serializes to valid JSON
  - [ ] Test SubTask JSON includes task_id reference
  - [ ] Test SubTask deserializes back to equal entity
  - [ ] Test handles datetime fields (ISO 8601)
  - [ ] Test handles UUID fields
  - [ ] Test handles enum fields
  - [ ] Test handles frozenset fields (as list)
  - [ ] Test handles None values
  - [ ] Test handles empty strings
  - [ ] Test handles special characters (unicode)
  - [ ] Test pretty-print option
  - [ ] Test compact output option
  - [ ] Test invalid JSON raises `DeserializationError`
  - [ ] Test missing required field raises `DeserializationError`
  - [ ] Test extra fields are ignored (forward compatibility)

- [ ] **GREEN**: Implement `JsonSerializer`
  - [ ] Implement `ISerializer`
  - [ ] Custom JSON encoder for domain types
  - [ ] Custom JSON decoder for domain types
  - [ ] `file_extension = ".json"`
  - [ ] `content_type = "application/json"`

- [ ] **REFACTOR**: Add schema validation
  - [ ] JSON Schema for validation
  - [ ] Version migration support

#### 102.2.2: JSON Task Repository

- [ ] **RED**: Write `test_json_task_repository.py`
  - [ ] Test `save()` creates new file for new task
  - [ ] Test `save()` overwrites file for existing task
  - [ ] Test `get()` returns task from file
  - [ ] Test `get()` returns None for non-existent
  - [ ] Test `delete()` removes file, returns True
  - [ ] Test `delete()` returns False for non-existent
  - [ ] Test `list_all()` returns all tasks from files
  - [ ] Test `list_all()` returns empty list when no files
  - [ ] Test `list_by_status()` filters correctly
  - [ ] Test `list_by_priority()` filters correctly
  - [ ] Test `list_by_tag()` filters correctly
  - [ ] Test `exists()` returns correct boolean
  - [ ] Test corrupted file raises `RepositoryError`
  - [ ] Test file permission error raises `RepositoryError`

- [ ] **GREEN**: Implement `JsonTaskRepository`
  - [ ] Implement `ITaskRepository`
  - [ ] Use `FileStore` and `JsonSerializer`
  - [ ] File naming: `{task_id}.json`

- [ ] **REFACTOR**: Add caching layer
  - [ ] In-memory cache for frequently accessed tasks
  - [ ] Cache invalidation on save/delete

#### 102.2.3: JSON SubTask Repository

- [ ] **RED**: Write `test_json_subtask_repository.py`
  - [ ] Test `save()` creates new file for new subtask
  - [ ] Test `get()` returns subtask from file
  - [ ] Test `get()` returns None for non-existent
  - [ ] Test `delete()` removes file, returns True
  - [ ] Test `list_by_task()` returns all subtasks for task
  - [ ] Test `list_by_task()` returns ordered by order_index
  - [ ] Test `list_by_task()` returns empty list when none
  - [ ] Test `list_by_status()` filters correctly
  - [ ] Test `count_by_task()` returns correct count
  - [ ] Test `count_incomplete_by_task()` returns correct count

- [ ] **GREEN**: Implement `JsonSubTaskRepository`
  - [ ] Implement `ISubTaskRepository`
  - [ ] Use `FileStore` and `JsonSerializer`
  - [ ] File naming: `{subtask_id}.json`
  - [ ] Consider subdirectory per parent task for performance

- [ ] **REFACTOR**: Optimize listing
  - [ ] Index file for faster queries by task_id

---

### Sub-task 102.3: TOON Adapter

**Files**: `src/infrastructure/persistence/toon_adapter.py`
**Tests**: `tests/integration/persistence/test_toon_adapter.py`

#### 102.3.1: TOON Serializer

- [ ] **RED**: Write `test_toon_serializer.py`
  - [ ] Test Task serializes to valid TOON
  - [ ] Test Task TOON includes all fields
  - [ ] Test Task deserializes back to equal entity
  - [ ] Test SubTask serializes to valid TOON
  - [ ] Test SubTask TOON includes task_id reference
  - [ ] Test SubTask deserializes back to equal entity
  - [ ] Test handles datetime fields
  - [ ] Test handles UUID fields
  - [ ] Test handles enum fields
  - [ ] Test handles frozenset fields
  - [ ] Test handles None values
  - [ ] Test handles special characters (quoting)
  - [ ] Test invalid TOON raises `DeserializationError`
  - [ ] Test TOON is significantly smaller than JSON (measure tokens)
  - [ ] Test round-trip JSON ↔ TOON preserves data

- [ ] **GREEN**: Implement `ToonSerializer`
  - [ ] Implement `ISerializer`
  - [ ] Use `python-toon` library
  - [ ] Custom encoding for domain types
  - [ ] `file_extension = ".toon"`
  - [ ] `content_type = "text/toon"`

- [ ] **REFACTOR**: Add token counting
  - [ ] Method to estimate token savings vs JSON

#### 102.3.2: TOON Task Repository

- [ ] **RED**: Write `test_toon_task_repository.py`
  - [ ] Test `save()` creates .toon file
  - [ ] Test `get()` reads .toon file
  - [ ] Test `delete()` removes .toon file
  - [ ] Test `list_all()` returns all tasks
  - [ ] Test filtering works same as JSON adapter
  - [ ] Test same contract as `ITaskRepository`

- [ ] **GREEN**: Implement `ToonTaskRepository`
  - [ ] Same interface as `JsonTaskRepository`
  - [ ] Use `ToonSerializer` instead

- [ ] **REFACTOR**: Extract common base
  - [ ] `FileTaskRepository` base class with serializer injection

#### 102.3.3: TOON SubTask Repository

- [ ] **RED**: Write `test_toon_subtask_repository.py`
  - [ ] Test same contract as JSON adapter
  - [ ] Test TOON-specific serialization

- [ ] **GREEN**: Implement `ToonSubTaskRepository`
  - [ ] Same interface as `JsonSubTaskRepository`
  - [ ] Use `ToonSerializer`

- [ ] **REFACTOR**: Extract common base
  - [ ] `FileSubTaskRepository` base class

---

### Sub-task 102.4: Unit of Work Implementation

**Files**: `src/infrastructure/persistence/file_unit_of_work.py`
**Tests**: `tests/integration/persistence/test_file_unit_of_work.py`

#### 102.4.1: File Unit of Work

- [ ] **RED**: Write `test_file_unit_of_work.py`
  - [ ] Test `task_repository` property returns configured repository
  - [ ] Test `subtask_repository` property returns configured repository
  - [ ] Test `commit()` is no-op for file-based (auto-commit on save)
  - [ ] Test `rollback()` is no-op for file-based (no transactions)
  - [ ] Test context manager works
  - [ ] Test `collect_events()` gathers events from saved aggregates
  - [ ] Test factory method for JSON format
  - [ ] Test factory method for TOON format
  - [ ] Test configurable base path

- [ ] **GREEN**: Implement `FileUnitOfWork`
  - [ ] Implement `IUnitOfWork`
  - [ ] Inject serializer type (JSON or TOON)
  - [ ] Factory methods: `create_json()`, `create_toon()`

- [ ] **REFACTOR**: Add format auto-detection
  - [ ] Detect format from existing files

---

### Sub-task 102.5: Contract Tests

**Files**: `tests/contract/`

#### 102.5.1: Repository Contract Tests

- [ ] **RED**: Write `test_repository_contract.py`
  - [ ] Parameterized tests for all repository implementations
  - [ ] Test save/get round-trip
  - [ ] Test delete behavior
  - [ ] Test list behavior
  - [ ] Test filter behavior
  - [ ] Test not-found behavior
  - [ ] Ensure JSON and TOON adapters behave identically

- [ ] **GREEN**: Implement contract test suite
  - [ ] Use pytest parameterization
  - [ ] Run same tests against both adapters

- [ ] **REFACTOR**: Add performance contracts
  - [ ] Max time for operations
  - [ ] Memory bounds

---

## WORK-103: CQRS Implementation

**Status**: PENDING
**Duration**: Weeks 5-6
**Artifacts**: Commands, queries, handlers, dispatcher
**Dependencies**: WORK-101, WORK-102

### Sub-task 103.1: Command Definitions

**Files**: `src/application/commands/`
**Tests**: `tests/unit/application/commands/`

#### 103.1.1: Task Commands (`task_commands.py`)

- [ ] **RED**: Write `test_task_commands.py`
  - [ ] Test `CreateTaskCommand` has title, optional description, priority, tags, due_date
  - [ ] Test `CreateTaskCommand` is immutable
  - [ ] Test `CreateTaskCommand` validates title not empty
  - [ ] Test `StartTaskCommand` has task_id
  - [ ] Test `CompleteTaskCommand` has task_id, optional notes
  - [ ] Test `BlockTaskCommand` has task_id, reason
  - [ ] Test `UnblockTaskCommand` has task_id
  - [ ] Test `CancelTaskCommand` has task_id
  - [ ] Test `UpdateTaskCommand` has task_id, optional title, description, priority, due_date
  - [ ] Test `AddTagCommand` has task_id, tag
  - [ ] Test `RemoveTagCommand` has task_id, tag
  - [ ] Test `AddSubTaskReferenceCommand` has task_id, subtask_id
  - [ ] Test `RemoveSubTaskReferenceCommand` has task_id, subtask_id

- [ ] **GREEN**: Implement Task commands
  - [ ] `@dataclass(frozen=True)` for all commands
  - [ ] Validation in `__post_init__`

- [ ] **REFACTOR**: Add command metadata
  - [ ] `command_type` property
  - [ ] `correlation_id` field

#### 103.1.2: SubTask Commands (`subtask_commands.py`)

- [ ] **RED**: Write `test_subtask_commands.py`
  - [ ] Test `CreateSubTaskCommand` has task_id, title, optional description, order_index
  - [ ] Test `StartSubTaskCommand` has subtask_id
  - [ ] Test `CompleteSubTaskCommand` has subtask_id
  - [ ] Test `SkipSubTaskCommand` has subtask_id, optional reason
  - [ ] Test `UpdateSubTaskCommand` has subtask_id, optional title, description, order_index
  - [ ] Test all commands are immutable

- [ ] **GREEN**: Implement SubTask commands
  - [ ] Same patterns as Task commands

- [ ] **REFACTOR**: Ensure consistency

---

### Sub-task 103.2: Command Handlers

**Files**: `src/application/handlers/commands/`
**Tests**: `tests/unit/application/handlers/`

#### 103.2.1: Task Command Handlers (`task_handlers.py`)

- [ ] **RED**: Write `test_task_command_handlers.py`
  - [ ] Test `CreateTaskHandler` creates task via factory
  - [ ] Test `CreateTaskHandler` saves via repository
  - [ ] Test `CreateTaskHandler` returns TaskId
  - [ ] Test `CreateTaskHandler` collects TaskCreated event
  - [ ] Test `StartTaskHandler` fetches task
  - [ ] Test `StartTaskHandler` calls task.start()
  - [ ] Test `StartTaskHandler` saves updated task
  - [ ] Test `StartTaskHandler` raises EntityNotFoundError if not found
  - [ ] Test `CompleteTaskHandler` same pattern
  - [ ] Test `BlockTaskHandler` same pattern
  - [ ] Test `UnblockTaskHandler` same pattern
  - [ ] Test `CancelTaskHandler` same pattern
  - [ ] Test `UpdateTaskHandler` applies partial updates
  - [ ] Test `AddTagHandler` adds tag
  - [ ] Test `RemoveTagHandler` removes tag
  - [ ] Test handlers collect events for dispatch

- [ ] **GREEN**: Implement Task handlers
  - [ ] `ICommandHandler[TCommand, TResult]` interface
  - [ ] Inject `IUnitOfWork`
  - [ ] Fetch → Mutate → Save pattern

- [ ] **REFACTOR**: Extract base handler
  - [ ] Common fetch-mutate-save logic

#### 103.2.2: SubTask Command Handlers (`subtask_handlers.py`)

- [ ] **RED**: Write `test_subtask_command_handlers.py`
  - [ ] Test `CreateSubTaskHandler` creates subtask
  - [ ] Test `CreateSubTaskHandler` adds reference to parent task
  - [ ] Test `CreateSubTaskHandler` raises if parent task not found
  - [ ] Test `StartSubTaskHandler` starts subtask
  - [ ] Test `CompleteSubTaskHandler` completes subtask
  - [ ] Test `SkipSubTaskHandler` skips subtask
  - [ ] Test `UpdateSubTaskHandler` updates subtask
  - [ ] Test handlers collect events

- [ ] **GREEN**: Implement SubTask handlers
  - [ ] Same patterns as Task handlers
  - [ ] Coordinate with parent Task for reference

- [ ] **REFACTOR**: Add transaction coordinator
  - [ ] Ensure Task and SubTask saved atomically

---

### Sub-task 103.3: Query Definitions

**Files**: `src/application/queries/`
**Tests**: `tests/unit/application/queries/`

#### 103.3.1: Task Queries (`task_queries.py`)

- [ ] **RED**: Write `test_task_queries.py`
  - [ ] Test `GetTaskQuery` has task_id
  - [ ] Test `ListTasksQuery` has optional filters: status, priority, tag
  - [ ] Test `GetTaskWithSubTasksQuery` has task_id
  - [ ] Test all queries are immutable

- [ ] **GREEN**: Implement Task queries
  - [ ] `@dataclass(frozen=True)`

- [ ] **REFACTOR**: Add pagination
  - [ ] `limit`, `offset` fields

#### 103.3.2: SubTask Queries (`subtask_queries.py`)

- [ ] **RED**: Write `test_subtask_queries.py`
  - [ ] Test `GetSubTaskQuery` has subtask_id
  - [ ] Test `ListSubTasksByTaskQuery` has task_id
  - [ ] Test `ListSubTasksQuery` has optional status filter

- [ ] **GREEN**: Implement SubTask queries

- [ ] **REFACTOR**: Add sorting options

---

### Sub-task 103.4: Query Handlers

**Files**: `src/application/handlers/queries/`
**Tests**: `tests/unit/application/handlers/`

#### 103.4.1: Task Query Handlers (`task_query_handlers.py`)

- [ ] **RED**: Write `test_task_query_handlers.py`
  - [ ] Test `GetTaskHandler` returns TaskDTO or None
  - [ ] Test `ListTasksHandler` returns list of TaskDTO
  - [ ] Test `ListTasksHandler` applies filters
  - [ ] Test `GetTaskWithSubTasksHandler` returns TaskWithSubTasksDTO
  - [ ] Test handlers don't modify state

- [ ] **GREEN**: Implement Task query handlers
  - [ ] `IQueryHandler[TQuery, TResult]` interface
  - [ ] Return DTOs, not aggregates

- [ ] **REFACTOR**: Add caching hints

#### 103.4.2: SubTask Query Handlers (`subtask_query_handlers.py`)

- [ ] **RED**: Write `test_subtask_query_handlers.py`
  - [ ] Test `GetSubTaskHandler` returns SubTaskDTO or None
  - [ ] Test `ListSubTasksByTaskHandler` returns ordered list
  - [ ] Test `ListSubTasksHandler` applies status filter

- [ ] **GREEN**: Implement SubTask query handlers

- [ ] **REFACTOR**: Optimize for common queries

---

### Sub-task 103.5: DTOs

**Files**: `src/application/dtos/`
**Tests**: `tests/unit/application/dtos/`

#### 103.5.1: Task DTOs (`task_dto.py`)

- [ ] **RED**: Write `test_task_dto.py`
  - [ ] Test `TaskDTO` has all Task fields
  - [ ] Test `TaskDTO` is immutable
  - [ ] Test `TaskDTO.from_entity()` creates DTO from Task
  - [ ] Test `TaskDTO` serializes to dict
  - [ ] Test `TaskSummaryDTO` has subset of fields (id, title, status)
  - [ ] Test `TaskWithSubTasksDTO` includes list of SubTaskDTO

- [ ] **GREEN**: Implement Task DTOs
  - [ ] `@dataclass(frozen=True)`
  - [ ] `from_entity()` factory

- [ ] **REFACTOR**: Add serialization methods

#### 103.5.2: SubTask DTOs (`subtask_dto.py`)

- [ ] **RED**: Write `test_subtask_dto.py`
  - [ ] Test `SubTaskDTO` has all SubTask fields
  - [ ] Test `SubTaskDTO.from_entity()` creates DTO
  - [ ] Test `SubTaskSummaryDTO` has subset

- [ ] **GREEN**: Implement SubTask DTOs

- [ ] **REFACTOR**: Ensure consistency with Task DTOs

---

### Sub-task 103.6: Event Dispatcher

**Files**: `src/application/dispatcher/`
**Tests**: `tests/unit/application/dispatcher/`

#### 103.6.1: Event Dispatcher Port and Adapter

- [ ] **RED**: Write `test_event_dispatcher.py`
  - [ ] Test `IEventDispatcher` is ABC
  - [ ] Test `dispatch(event)` is abstract
  - [ ] Test `dispatch_all(events)` is abstract
  - [ ] Test `subscribe(event_type, handler)` is abstract
  - [ ] Test `InMemoryEventDispatcher` dispatches to handlers
  - [ ] Test multiple handlers for same event type
  - [ ] Test handler exception doesn't stop other handlers
  - [ ] Test async handler support (future)

- [ ] **GREEN**: Implement `IEventDispatcher` and `InMemoryEventDispatcher`
  - [ ] Simple in-memory implementation for Phase 1

- [ ] **REFACTOR**: Add event logging
  - [ ] Log all dispatched events

---

### Sub-task 103.7: CQRS Integration Tests

**Files**: `tests/integration/application/`

#### 103.7.1: End-to-End CQRS Tests

- [ ] **RED**: Write `test_cqrs_integration.py`
  - [ ] Test create task → query returns it
  - [ ] Test create task → start → query shows IN_PROGRESS
  - [ ] Test create task → complete → query shows COMPLETED
  - [ ] Test create task with subtasks → query with subtasks
  - [ ] Test complete subtasks → complete task workflow
  - [ ] Test events are dispatched correctly
  - [ ] Test full lifecycle with file persistence

- [ ] **GREEN**: Implement integration tests
  - [ ] Use real file system (temp directory)
  - [ ] Test both JSON and TOON adapters

- [ ] **REFACTOR**: Add performance benchmarks

---

## WORK-104: CLI Interface & SKILL.md

**Status**: PENDING
**Duration**: Weeks 7-8
**Artifacts**: CLI adapter, SKILL.md, BDD tests
**Dependencies**: WORK-103

### Sub-task 104.1: CLI Primary Adapter

**Files**: `src/interface/cli/`
**Tests**: `tests/e2e/cli/`

#### 104.1.1: CLI Entry Point (`wt.py`)

- [ ] **RED**: Write `test_cli_entry.py`
  - [ ] Test `wt --help` shows usage
  - [ ] Test `wt --version` shows version
  - [ ] Test `wt` with no args shows help
  - [ ] Test unknown command shows error
  - [ ] Test exit code 0 on success
  - [ ] Test exit code 1 on error
  - [ ] Test `--format json` option
  - [ ] Test `--format toon` option
  - [ ] Test `--data-dir` option for custom path

- [ ] **GREEN**: Implement CLI entry point
  - [ ] Use argparse
  - [ ] Subcommand structure
  - [ ] Global options

- [ ] **REFACTOR**: Add rich output formatting
  - [ ] Colors for status
  - [ ] Tables for lists

#### 104.1.2: Task Subcommand (`task_cli.py`)

- [ ] **RED**: Write `test_task_cli.py`
  - [ ] Test `wt task create "Title"` creates task
  - [ ] Test `wt task create "Title" --description "Desc"` with description
  - [ ] Test `wt task create "Title" --priority high` with priority
  - [ ] Test `wt task create "Title" --tag bug --tag urgent` with tags
  - [ ] Test `wt task create "Title" --due 2026-02-01` with due date
  - [ ] Test `wt task list` shows all tasks
  - [ ] Test `wt task list --status pending` filters by status
  - [ ] Test `wt task list --priority high` filters by priority
  - [ ] Test `wt task list --tag bug` filters by tag
  - [ ] Test `wt task show <id>` shows task details
  - [ ] Test `wt task show <id> --subtasks` shows with subtasks
  - [ ] Test `wt task start <id>` starts task
  - [ ] Test `wt task complete <id>` completes task
  - [ ] Test `wt task complete <id> --notes "Done"` with notes
  - [ ] Test `wt task block <id> --reason "Waiting"` blocks task
  - [ ] Test `wt task unblock <id>` unblocks task
  - [ ] Test `wt task cancel <id>` cancels task
  - [ ] Test `wt task update <id> --title "New"` updates title
  - [ ] Test `wt task delete <id>` deletes task
  - [ ] Test `wt task delete <id> --force` skips confirmation
  - [ ] Test error messages are helpful
  - [ ] Test invalid ID format shows error
  - [ ] Test not found shows appropriate message

- [ ] **GREEN**: Implement task subcommand
  - [ ] Wire to command/query handlers
  - [ ] Output formatting

- [ ] **REFACTOR**: Add interactive mode
  - [ ] Confirmation prompts for destructive actions

#### 104.1.3: SubTask Subcommand (`subtask_cli.py`)

- [ ] **RED**: Write `test_subtask_cli.py`
  - [ ] Test `wt subtask create <task_id> "Title"` creates subtask
  - [ ] Test `wt subtask create <task_id> "Title" --description "Desc"`
  - [ ] Test `wt subtask create <task_id> "Title" --order 1` with order
  - [ ] Test `wt subtask list <task_id>` shows subtasks for task
  - [ ] Test `wt subtask show <id>` shows subtask details
  - [ ] Test `wt subtask start <id>` starts subtask
  - [ ] Test `wt subtask complete <id>` completes subtask
  - [ ] Test `wt subtask skip <id>` skips subtask
  - [ ] Test `wt subtask skip <id> --reason "Not needed"` with reason
  - [ ] Test `wt subtask update <id> --title "New"` updates
  - [ ] Test `wt subtask delete <id>` deletes
  - [ ] Test error handling

- [ ] **GREEN**: Implement subtask subcommand

- [ ] **REFACTOR**: Add bulk operations
  - [ ] `wt subtask complete-all <task_id>`

---

### Sub-task 104.2: SKILL.md

**Files**: `skills/worktracker/SKILL.md`

#### 104.2.1: Work Tracker Skill Definition

- [ ] **Write SKILL.md**
  - [ ] Natural language patterns for task operations
  - [ ] Examples for common workflows
  - [ ] Integration with CLI commands
  - [ ] Error handling patterns
  - [ ] Quick reference section

- [ ] **Test skill patterns**
  - [ ] Manual testing with Claude Code
  - [ ] Verify pattern recognition

- [ ] **Document**
  - [ ] Add to skill index
  - [ ] Cross-reference with CLI

---

### Sub-task 104.3: BDD Test Suite

**Files**: `tests/bdd/`

#### 104.3.1: Task Feature Files

- [ ] **Write `features/task.feature`**
  - [ ] Scenario: Create task with title only
  - [ ] Scenario: Create task with all options
  - [ ] Scenario: Start pending task
  - [ ] Scenario: Complete in-progress task
  - [ ] Scenario: Block in-progress task
  - [ ] Scenario: Unblock blocked task
  - [ ] Scenario: Cancel pending task
  - [ ] Scenario: List tasks by status
  - [ ] Scenario: Update task attributes
  - [ ] Scenario: Add and remove tags
  - [ ] Edge: Create task with max-length title
  - [ ] Edge: Create task with due date today
  - [ ] Negative: Create task with empty title
  - [ ] Negative: Start already-started task
  - [ ] Negative: Complete pending task
  - [ ] Negative: Complete cancelled task

- [ ] **Implement step definitions** (`steps/task_steps.py`)
  - [ ] REAL CLI invocations (no mocks)
  - [ ] File system verification
  - [ ] Output parsing

#### 104.3.2: SubTask Feature Files

- [ ] **Write `features/subtask.feature`**
  - [ ] Scenario: Create subtask for task
  - [ ] Scenario: Complete subtask
  - [ ] Scenario: Skip subtask with reason
  - [ ] Scenario: Reorder subtasks
  - [ ] Scenario: Complete all subtasks then complete task
  - [ ] Negative: Create subtask for non-existent task
  - [ ] Negative: Complete subtask for completed task

- [ ] **Implement step definitions** (`steps/subtask_steps.py`)
  - [ ] REAL CLI invocations

#### 104.3.3: Workflow Feature Files

- [ ] **Write `features/workflow.feature`**
  - [ ] Scenario: Full task lifecycle with subtasks
  - [ ] Scenario: Concurrent subtask completion
  - [ ] Scenario: Task with blocked subtask
  - [ ] Scenario: Export to TOON format

- [ ] **Implement step definitions** (`steps/workflow_steps.py`)

---

### Sub-task 104.4: System Tests & Phase 1 Gate

**Files**: `tests/system/`

#### 104.4.1: System Integration Tests

- [ ] **RED**: Write `test_system_integration.py`
  - [ ] Test full workflow via CLI
  - [ ] Test persistence across CLI invocations
  - [ ] Test JSON and TOON format interop
  - [ ] Test data directory isolation
  - [ ] Test concurrent CLI invocations (multiple terminals)

- [ ] **GREEN**: Implement system tests
  - [ ] Real file system
  - [ ] Real CLI process invocation

- [ ] **REFACTOR**: Add chaos testing
  - [ ] Interrupt mid-operation
  - [ ] Corrupt file recovery

#### 104.4.2: Performance Tests

- [ ] **RED**: Write `test_performance.py`
  - [ ] Test create 100 tasks < 10s
  - [ ] Test list 100 tasks < 1s
  - [ ] Test single operation < 100ms p95
  - [ ] Test file size reasonable (< 1KB per task)
  - [ ] Test memory usage bounded

- [ ] **GREEN**: Implement performance tests
  - [ ] Benchmarking with pytest-benchmark

- [ ] **REFACTOR**: Add profiling

#### 104.4.3: Phase 1 Go/No-Go Checklist

- [ ] All unit tests pass (95%+ coverage)
- [ ] All integration tests pass
- [ ] All contract tests pass
- [ ] All BDD scenarios pass
- [ ] All E2E tests pass
- [ ] All architecture tests pass
- [ ] Performance targets met
- [ ] SKILL.md complete and tested
- [ ] No critical bugs
- [ ] Code review approved

---

## Estimated Test Counts

| Category | Count |
|----------|-------|
| Unit tests (domain) | ~150 |
| Unit tests (application) | ~100 |
| Integration tests | ~50 |
| Contract tests | ~20 |
| E2E tests | ~30 |
| BDD scenarios | ~40 |
| Architecture tests | ~10 |
| System tests | ~20 |
| Performance tests | ~10 |
| **Total** | **~430** |

---

*Phase 1 plan created 2026-01-09*
