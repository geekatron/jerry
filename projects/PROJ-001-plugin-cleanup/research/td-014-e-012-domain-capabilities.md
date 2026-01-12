# TD-014-E-012: Domain Capabilities Inventory

> **Research Task:** TD-014.R2
> **Date:** 2026-01-11
> **Researcher:** ps-researcher (Agent af7a232)
> **Status:** COMPLETE

---

## Executive Summary (L0)

The Jerry Framework domain layer contains a **fully-featured work tracking system** with strong invariants, quality gate enforcement, and event sourcing patterns. Two aggregates (`WorkItem`, `Session`) provide the core business capabilities, supported by 14+ value objects and 15+ domain events. The CLI adapter should act as a thin translation layer that invokes these domain capabilities while preserving all business logic constraints.

---

## Technical Findings (L1)

### AGGREGATES

#### 1. WorkItem Aggregate

**Location**: `src/work_tracking/domain/aggregates/work_item.py`

**Root Entity**: `WorkItem`

**Key Invariants**:
- Status transitions follow a state machine (PENDING → IN_PROGRESS → BLOCKED → DONE/CANCELLED)
- Quality gates must be met before completion (except for SPIKE work types)
- Dependencies form a DAG (no self-references allowed)
- Only one assignee at a time
- Title cannot be empty

**Capabilities Exposed**:

| Method | Purpose | Constraints |
|--------|---------|-------------|
| `WorkItem.create()` | Factory to create new work items | Title required |
| `start_work(reason)` | Transition to IN_PROGRESS | Must be PENDING |
| `block(reason)` | Transition to BLOCKED | Must be active |
| `complete(reason)` | Transition to DONE | Enforces quality gates |
| `cancel(reason)` | Transition to CANCELLED | Must be active |
| `reopen(reason)` | Reopen from DONE | Must be DONE |
| `change_priority(new_priority, reason)` | Update priority | Valid Priority value |
| `update_quality_metrics(coverage, ratio)` | Record test results | Valid metrics |
| `add_dependency(dependency_id, dependency_type)` | Link dependencies | No self-reference |
| `remove_dependency(dependency_id)` | Unlink dependencies | Must exist |
| `assign(assignee)` | Assign or unassign work | - |

#### 2. Session Aggregate

**Location**: `src/session_management/domain/aggregates/session.py`

**Root Entity**: `Session`

**Key Invariants**:
- Session starts in ACTIVE status
- Only ACTIVE sessions can be completed, abandoned, or have projects linked
- Once completed or abandoned, session cannot be modified

**Capabilities Exposed**:

| Method | Purpose | Constraints |
|--------|---------|-------------|
| `Session.create(session_id, description, project_id)` | Create new session | - |
| `complete(summary)` | Mark as successfully completed | Must be ACTIVE |
| `abandon(reason)` | Mark as abandoned | Must be ACTIVE |
| `link_project(project_id)` | Link session to project | Must be ACTIVE |

---

### VALUE OBJECTS

#### Work Tracking Domain

| Value Object | Location | Key Properties |
|--------------|----------|----------------|
| `WorkItemStatus` | `work_item_status.py` | States: PENDING, IN_PROGRESS, BLOCKED, DONE, CANCELLED |
| `Priority` | `priority.py` | CRITICAL(1), HIGH(2), MEDIUM(3), LOW(4) |
| `WorkType` | `work_type.py` | EPIC, STORY, TASK, SUBTASK, BUG, SPIKE |
| `WorkItemId` | `work_item_id.py` | Hybrid: Snowflake + WORK-nnn display |
| `TestCoverage` | `test_coverage.py` | 0-100 validated percentage |
| `TestRatio` | `test_ratio.py` | positive, negative, edge_case counts |
| `GateLevel` | `quality_gate.py` | L0 (Syntax), L1 (Semantic), L2 (Review) |
| `RiskTier` | `quality_gate.py` | T1 (Low) to T4 (Critical) |
| `GateResult` | `quality_gate.py` | PENDING, PASSED, FAILED, SKIPPED |
| `Threshold` | `quality_gate.py` | Numeric threshold with bounds |
| `GateCheckDefinition` | `quality_gate.py` | Immutable check definition |

#### Session Management Domain

| Value Object | Location | Key Properties |
|--------------|----------|----------------|
| `ProjectId` | `project_id.py` | Format: PROJ-{nnn}-{slug} |
| `SessionId` | Extends `VertexId` | Shared kernel ID |
| `ProjectStatus` | `project_status.py` | UNKNOWN, DRAFT, IN_PROGRESS, COMPLETED, ARCHIVED |
| `ValidationResult` | `validation_result.py` | success/failure + messages |

---

### DOMAIN EVENTS

#### WorkItem Events

| Event | Trigger |
|-------|---------|
| `WorkItemCreated` | New work item created |
| `StatusChanged` | Status transition with reason |
| `WorkItemCompleted` | Item reached DONE or CANCELLED |
| `PriorityChanged` | Priority updated |
| `QualityMetricsUpdated` | Test results recorded |
| `DependencyAdded` | Dependency linked |
| `DependencyRemoved` | Dependency unlinked |
| `AssigneeChanged` | Assignment updated |

#### Quality Gate Events

| Event | Trigger |
|-------|---------|
| `GateExecutionStarted` | Gate execution begins |
| `GateCheckCompleted` | Individual check finishes |
| `GateExecutionCompleted` | Full gate execution finishes |
| `RiskAssessed` | Risk tier assessed |
| `ThresholdViolation` | Metric violates threshold |

#### Session Events

| Event | Trigger |
|-------|---------|
| `SessionCreated` | New session starts |
| `SessionCompleted` | Session successfully completed |
| `SessionAbandoned` | Session abandoned |
| `SessionProjectLinked` | Session linked to project |

---

### DOMAIN SERVICES

#### 1. IWorkItemIdGenerator Protocol

**Location**: `src/work_tracking/domain/services/id_generator.py`

**Port Interface**:
```python
create() -> WorkItemId                              # Auto-increment display number
create_with_sequence(sequence: int) -> WorkItemId   # Use specific display number
```

**Implementation**: `WorkItemIdGenerator`
- Thread-safe via internal locking
- Hybrid Snowflake + sequential numbering
- Configurable worker_id and sequence initialization

#### 2. IQualityGateValidator Protocol

**Location**: `src/work_tracking/domain/services/quality_validator.py`

**Port Interface**:
```python
validate(gate_level, coverage, ratio) -> ValidationResult
assess_risk(file_patterns, keywords) -> RiskTier
```

**Implementation**: `QualityGateValidator`
- Stateless validation logic
- Configurable thresholds per gate level:
  - L0: No coverage requirement
  - L1: 80% coverage + positive/negative tests
  - L2: 90% coverage + positive/negative/edge case tests

---

### DOMAIN PORTS (Hexagonal Architecture)

#### 1. IRepository

**Location**: `src/work_tracking/domain/ports/repository.py`

Generic aggregate persistence port:
- `get(id)` - Retrieve aggregate or None
- `get_or_raise(id)` - Retrieve or raise AggregateNotFoundError
- `save(aggregate)` - Persist with optimistic concurrency
- `delete(id)` - Remove aggregate
- `exists(id)` - Check existence

#### 2. Event Store Port

**Location**: `src/work_tracking/domain/ports/event_store.py`
- Append-only event storage
- Event stream retrieval by aggregate ID

#### 3. Snapshot Store Port

**Location**: `src/work_tracking/domain/ports/snapshot_store.py`
- Snapshot storage for event-sourced aggregates

---

## Strategic Implications (L2)

### CLI Exposure Recommendations

Based on the architecture and invariants, the following domain capabilities should be exposed via CLI:

#### WorkItem Operations (Primary Commands)

| Command | Maps To | Example |
|---------|---------|---------|
| `jerry create <title>` | `WorkItem.create()` | `jerry create "Fix bug" --type BUG` |
| `jerry start <id>` | `start_work()` | `jerry start WORK-001` |
| `jerry block <id>` | `block()` | `jerry block WORK-001 --reason "Waiting on API"` |
| `jerry complete <id>` | `complete()` | `jerry complete WORK-001` |
| `jerry cancel <id>` | `cancel()` | `jerry cancel WORK-001` |
| `jerry reopen <id>` | `reopen()` | `jerry reopen WORK-001` |
| `jerry priority <id>` | `change_priority()` | `jerry priority WORK-001 HIGH` |
| `jerry assign <id>` | `assign()` | `jerry assign WORK-001 @user` |

#### Session Operations

| Command | Maps To | Example |
|---------|---------|---------|
| `jerry session create` | `Session.create()` | `jerry session create --project PROJ-001` |
| `jerry session link` | `link_project()` | `jerry session link PROJ-001` |
| `jerry session complete` | `complete()` | `jerry session complete --summary "Done"` |
| `jerry session abandon` | `abandon()` | `jerry session abandon --reason "Blocked"` |

### Critical Constraints for CLI Adapter

1. **Never bypass aggregates**: CLI must call aggregate methods, not reconstruct state
2. **Event collection**: All commands must collect and return domain events for persistence
3. **Quality gates**: `WorkItem.complete()` enforces gates - cannot be bypassed via CLI
4. **Immutability**: Value objects are frozen; CLI must create new instances for updates
5. **Validation**: All domain exceptions must be handled with user-friendly messages

---

## Summary Table

| Category | Count | Key Items |
|----------|-------|-----------|
| Aggregates | 2 | WorkItem, Session |
| Value Objects | 14+ | Priority, Status, WorkType, Id, Coverage, etc. |
| Domain Events | 15+ | WorkItemCreated, StatusChanged, SessionCompleted, etc. |
| Domain Services | 2 | WorkItemIdGenerator, QualityGateValidator |
| Ports | 3 | IRepository, EventStore, SnapshotStore |

---

## Document Lineage

| Artifact | Relationship |
|----------|--------------|
| TD-014 | Parent tech debt item |
| TD-014.R1 | Sibling research (use cases) |
| TD-014.R3 | Sibling research (knowledge base patterns) |
