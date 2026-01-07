# Jerry Work Tracker v3.0 - Implementation Plan

> **Status:** DESIGN - AWAITING APPROVAL
> **Created:** 2026-01-07
> **Last Updated:** 2026-01-07
> **Author:** Claude (Distinguished Systems Engineer persona)

---

## Executive Summary

This plan implements the Jerry Work Tracker skill using:
- **Hexagonal Architecture** (Ports & Adapters)
- **Domain-Driven Design** with three Aggregate Roots
- **Event Sourcing** with CloudEvents 1.0
- **CQRS** (Command Query Responsibility Segregation)

### Key Design Decisions

| Decision | Choice | Evidence |
|----------|--------|----------|
| Primary Aggregate Root | **Task** | Vernon's "small aggregates" principle; ECW performance issues |
| Secondary Aggregate Roots | **Phase**, **Plan** | Eventual consistency; reference by ID only |
| Event Schema | **CloudEvents 1.0** | User hard requirement; CNCF standard |
| Identity Objects | **Strongly Typed** | User hard requirement; domain clarity |
| Persistence | **File-based Event Store** | Claude Code Web compatibility |

---

## 1. Problem Statement (5W1H Analysis)

### WHO is affected?
- Claude Code instances tracking multi-phase work
- Users managing complex projects across sessions
- Future maintainers of the Jerry framework

### WHAT problem are we solving?
- Context rot degrades LLM performance in long sessions
- Need persistent work tracking that survives context compaction
- Previous ECW implementations had performance issues with large aggregates

### WHERE does the problem manifest?
- Claude Code sessions with >256k token context
- Large work trackers with 50+ tasks
- Concurrent operations on the same plan

### WHEN does it occur?
- During multi-hour coding sessions
- When projects grow beyond initial scope
- During context compaction/summarization

### WHY does it matter?
- Losing work state disrupts productivity
- Performance degradation frustrates users
- Cannot scale to enterprise-level project tracking

### HOW will we solve it?
- Task-level Aggregate Root for minimal contention
- Eventual consistency for progress calculations
- CloudEvents for auditable event sourcing
- Strongly typed IDs for domain clarity

---

## 2. Architecture Overview

### 2.1 Bounded Contexts

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        JERRY WORK TRACKER                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────┐    ┌─────────────────────┐                     │
│  │  WORK MANAGEMENT    │    │  PROGRESS REPORTING │                     │
│  │  BOUNDED CONTEXT    │    │  BOUNDED CONTEXT    │                     │
│  │                     │    │                     │                     │
│  │  Aggregates:        │    │  Read Models:       │                     │
│  │  - Task (Primary)   │───►│  - ProgressView     │                     │
│  │  - Phase (Secondary)│    │  - TimelineView     │                     │
│  │  - Plan (Tertiary)  │    │  - SummaryView      │                     │
│  │                     │    │                     │                     │
│  └─────────────────────┘    └─────────────────────┘                     │
│           │                                                              │
│           │ Domain Events (CloudEvents)                                  │
│           ▼                                                              │
│  ┌─────────────────────┐                                                │
│  │    EVENT STORE      │                                                │
│  │  (Source of Truth)  │                                                │
│  └─────────────────────┘                                                │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Aggregate Root Design (Per Vernon's Principles)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PRIMARY AGGREGATE: TASK                               │
│                    (Transactional Consistency)                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Task                                                                    │
│  ├── task_id: TaskId (strongly typed)                                   │
│  ├── phase_id: PhaseId (reference only)                                 │
│  ├── title: str                                                         │
│  ├── description: Optional[str]                                         │
│  ├── status: TaskStatus (state machine)                                 │
│  ├── verification: Optional[str]                                        │
│  ├── evidence_refs: List[EvidenceId]                                    │
│  ├── blocking_info: Optional[BlockingInfo]                              │
│  └── subtasks: List[Subtask]  ← CHILD ENTITIES (same aggregate)         │
│       ├── subtask_id: SubtaskId                                         │
│       ├── title: str                                                    │
│       └── checked: bool                                                 │
│                                                                          │
│  Invariants (enforced within aggregate):                                 │
│  - Cannot complete task unless all subtasks checked                     │
│  - Cannot complete task unless evidence attached (if required)          │
│  - Status transitions must follow state machine                         │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                 SECONDARY AGGREGATE: PHASE                               │
│                 (Eventual Consistency with Task)                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Phase                                                                   │
│  ├── phase_id: PhaseId (strongly typed)                                 │
│  ├── plan_id: PlanId (reference only)                                   │
│  ├── display_number: int                                                │
│  ├── title: str                                                         │
│  ├── status: PhaseStatus (derived from tasks)                           │
│  ├── task_ids: List[TaskId]  ← REFERENCES ONLY (not full objects)       │
│  └── target_date: Optional[date]                                        │
│                                                                          │
│  Progress: Calculated via projection (eventual consistency)              │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                  TERTIARY AGGREGATE: PLAN                                │
│                 (Eventual Consistency with Phase)                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Plan                                                                    │
│  ├── plan_id: PlanId (strongly typed)                                   │
│  ├── initiative_id: Optional[InitiativeId] (reference)                  │
│  ├── title: str                                                         │
│  ├── description: Optional[str]                                         │
│  ├── status: PlanStatus (derived from phases)                           │
│  └── phase_ids: List[PhaseId]  ← REFERENCES ONLY                        │
│                                                                          │
│  Progress: Calculated via projection (eventual consistency)              │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.3 Hexagonal Architecture Layers

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         INTERFACE LAYER                                   │
│                      (Primary Adapters - Drives)                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                       │
│  │  CLI (wt)   │  │ Skill REPL  │  │ Sub-agents  │                       │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘                       │
└─────────┼────────────────┼────────────────┼──────────────────────────────┘
          │                │                │
          └────────────────┼────────────────┘
                           │
                    PRIMARY PORTS
            ┌──────────────┴──────────────┐
            │  IWorkTrackerFacade         │
            │  IProgressQueryService      │
            └──────────────┬──────────────┘
                           │
┌──────────────────────────┼───────────────────────────────────────────────┐
│                          │  APPLICATION LAYER                             │
│                          │  (Use Cases / CQRS)                           │
│  ┌───────────────────────┼───────────────────────────────────┐           │
│  │ Command Handlers      │       Query Handlers              │           │
│  │ - CreateTaskHandler   │       - GetTaskQuery              │           │
│  │ - CompleteTaskHandler │       - GetProgressQuery          │           │
│  │ - AddSubtaskHandler   │       - ListTasksQuery            │           │
│  └───────────────────────┴───────────────────────────────────┘           │
│                          │                                                │
│                    Dispatcher + Middleware                                │
│                    (Logging, Validation, Events)                         │
└──────────────────────────┼───────────────────────────────────────────────┘
                           │
┌──────────────────────────┼───────────────────────────────────────────────┐
│                          │  DOMAIN LAYER                                  │
│                          │  (Business Logic - Zero Dependencies)          │
│  ┌───────────────────────┼───────────────────────────────────┐           │
│  │ Aggregates            │       Value Objects               │           │
│  │ - Task (AR)           │       - TaskId, PhaseId, PlanId   │           │
│  │ - Phase (AR)          │       - TaskStatus, PhaseStatus   │           │
│  │ - Plan (AR)           │       - Actor, Evidence5W1H       │           │
│  │                       │                                   │           │
│  │ Domain Events         │       Domain Services             │           │
│  │ - TaskCreated         │       - ProgressCalculation       │           │
│  │ - TaskCompleted       │       - CompletionGuardService    │           │
│  └───────────────────────┴───────────────────────────────────┘           │
│                          │                                                │
│                   SECONDARY PORTS                                         │
│            ┌─────────────┴─────────────┐                                 │
│            │ IEventStore               │                                 │
│            │ ITaskRepository           │                                 │
│            │ IPhaseRepository          │                                 │
│            │ IPlanRepository           │                                 │
│            │ IEventBus                 │                                 │
│            └─────────────┬─────────────┘                                 │
└──────────────────────────┼───────────────────────────────────────────────┘
                           │
┌──────────────────────────┼───────────────────────────────────────────────┐
│                          │  INFRASTRUCTURE LAYER                          │
│                          │  (Secondary Adapters - Driven)                 │
│  ┌─────────────┐  ┌──────┴──────┐  ┌─────────────┐  ┌─────────────┐      │
│  │ FileEvent   │  │   JSON      │  │  Markdown   │  │ InMemory    │      │
│  │ Store       │  │ Repository  │  │  Adapter    │  │ EventBus    │      │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘      │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Strongly Typed Identity Objects

Per user requirement: *"wrapping IDs in domain-specific types instead of UUID/GUID"*

```python
# src/domain/value_objects/identifiers.py

@dataclass(frozen=True)
class TaskId:
    """Strongly typed Task identifier."""
    value: str

    def __post_init__(self):
        if not self.value or not self.value.startswith("TASK-"):
            raise ValueError(f"Invalid TaskId: {self.value}")

    @classmethod
    def generate(cls) -> "TaskId":
        return cls(f"TASK-{uuid.uuid4().hex[:8].upper()}")

@dataclass(frozen=True)
class PhaseId:
    """Strongly typed Phase identifier."""
    value: str

    @classmethod
    def generate(cls) -> "PhaseId":
        return cls(f"PHASE-{uuid.uuid4().hex[:8].upper()}")

@dataclass(frozen=True)
class PlanId:
    """Strongly typed Plan identifier."""
    value: str

    @classmethod
    def generate(cls) -> "PlanId":
        return cls(f"PLAN-{uuid.uuid4().hex[:8].upper()}")

@dataclass(frozen=True)
class SubtaskId:
    """Strongly typed Subtask identifier - scoped to parent Task."""
    task_id: TaskId
    sequence: int

    def __str__(self) -> str:
        # Display format: "TASK-ABC123.1"
        return f"{self.task_id.value}.{self.sequence}"
```

---

## 4. CloudEvents Domain Events

Per user requirement: *"CloudEvents will be our Event Schema"*

### 4.1 Base CloudEvent Structure

```json
{
  "specversion": "1.0",
  "type": "com.jerry.worktracker.task.created.v1",
  "source": "/jerry/worktracker/tasks/TASK-ABC123",
  "id": "evt-a1b2c3d4-5678-90ab-cdef-1234567890ab",
  "time": "2026-01-07T14:30:00Z",
  "datacontenttype": "application/json",
  "subject": "TASK-ABC123",
  "data": {
    "task_id": "TASK-ABC123",
    "phase_id": "PHASE-001",
    "title": "Implement TaskId value object",
    "created_by": {"type": "CLAUDE", "id": "main"}
  }
}
```

### 4.2 Event Type Hierarchy

| Event Type | Description | Aggregate |
|------------|-------------|-----------|
| `com.jerry.worktracker.task.created.v1` | Task created | Task |
| `com.jerry.worktracker.task.started.v1` | Task started | Task |
| `com.jerry.worktracker.task.completed.v1` | Task completed | Task |
| `com.jerry.worktracker.task.blocked.v1` | Task blocked | Task |
| `com.jerry.worktracker.task.unblocked.v1` | Task unblocked | Task |
| `com.jerry.worktracker.subtask.added.v1` | Subtask added | Task |
| `com.jerry.worktracker.subtask.checked.v1` | Subtask checked | Task |
| `com.jerry.worktracker.phase.created.v1` | Phase created | Phase |
| `com.jerry.worktracker.phase.task_added.v1` | Task ref added | Phase |
| `com.jerry.worktracker.plan.created.v1` | Plan created | Plan |
| `com.jerry.worktracker.plan.phase_added.v1` | Phase ref added | Plan |

---

## 5. Eventual Consistency Flow

### 5.1 Task Completion → Phase Progress Update

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    TASK COMPLETION EVENT FLOW                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. User: "mark task 5.3 complete"                                      │
│     │                                                                    │
│     ▼                                                                    │
│  2. Load Task aggregate (TASK-ABC123)  ← Fast: single task only         │
│     │                                                                    │
│     ▼                                                                    │
│  3. Task.complete(actor)                                                │
│     ├── Validate: all subtasks checked? ✓                               │
│     ├── Validate: evidence attached? ✓                                  │
│     └── Emit: TaskCompletedEvent                                        │
│     │                                                                    │
│     ▼                                                                    │
│  4. Persist to EventStore (single transaction)                          │
│     │                                                                    │
│     ▼                                                                    │
│  5. Return success to user immediately                                   │
│                                                                          │
│  ══════════════════════════════════════════════════════════════════════ │
│                    EVENTUAL CONSISTENCY BOUNDARY                         │
│  ══════════════════════════════════════════════════════════════════════ │
│                                                                          │
│  6. EventBus publishes TaskCompletedEvent                               │
│     │                                                                    │
│     ▼                                                                    │
│  7. ProgressProjection handler receives event                           │
│     ├── Load Phase read model                                            │
│     ├── Recalculate progress from all task states                       │
│     └── Persist updated progress                                         │
│     │                                                                    │
│     ▼                                                                    │
│  8. PhaseProgressUpdatedEvent emitted (optional)                        │
│     │                                                                    │
│     ▼                                                                    │
│  9. PlanProgressProjection updates                                      │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 6. State Machines

### 6.1 Task Status State Machine

```
                         ┌──────────────┐
                         │   PENDING    │
                         └──────┬───────┘
                                │
              ┌─────────────────┼─────────────────┐
              │ start()         │ skip()          │ block()
              ▼                 ▼                 ▼
       ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
       │ IN_PROGRESS  │  │   SKIPPED    │  │   BLOCKED    │
       └──────┬───────┘  └──────────────┘  └──────┬───────┘
              │                                    │
              │ complete()                         │ unblock()
              │ [guards: subtasks, evidence]       │
              ▼                                    ▼
       ┌──────────────┐                    ┌──────────────┐
       │   COMPLETE   │                    │   PENDING    │
       └──────────────┘                    └──────────────┘
              │
              │ reopen()
              ▼
       ┌──────────────┐
       │ IN_PROGRESS  │
       └──────────────┘

   Completion Guards:
   1. All subtasks must be checked (or no subtasks)
   2. Evidence attached (if settings.require_evidence)
```

### 6.2 Phase Status State Machine

```
       ┌──────────────┐
       │   PENDING    │
       └──────┬───────┘
              │ start()
              ▼
       ┌──────────────┐  block()  ┌──────────────┐
       │ IN_PROGRESS  │──────────►│   BLOCKED    │
       └──────┬───────┘           └──────┬───────┘
              │                          │
              │ complete()               │ unblock()
              │ [all tasks done]         │
              ▼                          ▼
       ┌──────────────┐           ┌──────────────┐
       │   COMPLETE   │           │ IN_PROGRESS  │
       └──────────────┘           └──────────────┘

   Phase completion: derived from task states
   - PENDING: no tasks started
   - IN_PROGRESS: at least one task started
   - BLOCKED: any task blocked
   - COMPLETE: all tasks complete or skipped
```

---

## 7. Directory Structure

```
jerry/
├── src/
│   ├── __init__.py
│   ├── domain/                          # Zero external dependencies
│   │   ├── __init__.py
│   │   ├── aggregates/
│   │   │   ├── __init__.py
│   │   │   ├── task.py                  # Task AR + Subtask entities
│   │   │   ├── phase.py                 # Phase AR
│   │   │   └── plan.py                  # Plan AR
│   │   ├── value_objects/
│   │   │   ├── __init__.py
│   │   │   ├── identifiers.py           # TaskId, PhaseId, PlanId, SubtaskId
│   │   │   ├── status.py                # TaskStatus, PhaseStatus, PlanStatus
│   │   │   └── actor.py                 # Actor value object
│   │   ├── events/
│   │   │   ├── __init__.py
│   │   │   ├── base.py                  # CloudEvent base class
│   │   │   ├── task_events.py
│   │   │   ├── phase_events.py
│   │   │   └── plan_events.py
│   │   └── ports/
│   │       ├── __init__.py
│   │       ├── repositories.py          # ITaskRepository, IPhaseRepository, IPlanRepository
│   │       ├── event_store.py           # IEventStore
│   │       └── event_bus.py             # IEventBus
│   ├── application/
│   │   ├── __init__.py
│   │   ├── dispatcher.py
│   │   ├── commands/
│   │   │   └── task_commands.py
│   │   ├── queries/
│   │   │   └── progress_queries.py
│   │   └── dtos/
│   │       └── task_dto.py
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── persistence/
│   │   │   ├── file_event_store.py
│   │   │   └── json_repository.py
│   │   └── projections/
│   │       └── progress_projection.py
│   └── interface/
│       ├── __init__.py
│       └── cli/
│           └── main.py
└── tests/
    ├── unit/
    │   └── domain/
    │       ├── test_task_id.py
    │       ├── test_task.py
    │       └── test_task_status.py
    ├── integration/
    ├── bdd/
    │   └── features/
    │       └── task_completion.feature
    └── architecture/
        └── test_dependencies.py
```

---

## 8. Implementation Phases

### Phase 1: Domain Layer (Foundation)

| Task | Description | Verification |
|------|-------------|--------------|
| DOM-001 | Implement TaskId, PhaseId, PlanId, SubtaskId | Unit tests |
| DOM-002 | Implement TaskStatus with state machine | Unit tests |
| DOM-003 | Implement PhaseStatus, PlanStatus | Unit tests |
| DOM-004 | Implement Actor value object | Unit tests |
| DOM-005 | Implement CloudEvent base class | Unit tests |
| DOM-006 | Implement task domain events | Unit tests |
| DOM-007 | Implement Subtask entity | Unit tests |
| DOM-008 | Implement Task aggregate root | Unit tests |
| DOM-009 | Implement Phase aggregate root | Unit tests |
| DOM-010 | Implement Plan aggregate root | Unit tests |
| DOM-011 | Define port interfaces | Interface review |

### Phase 2: Application Layer

| Task | Description | Verification |
|------|-------------|--------------|
| APP-001 | Implement command dispatcher | Unit tests |
| APP-002 | Implement CreateTaskHandler | Unit tests |
| APP-003 | Implement CompleteTaskHandler | Unit tests |
| APP-004 | Implement AddSubtaskHandler | Unit tests |
| APP-005 | Implement query handlers | Unit tests |
| APP-006 | Implement DTOs | Schema validation |

### Phase 3: Infrastructure Layer

| Task | Description | Verification |
|------|-------------|--------------|
| INF-001 | Implement FileEventStore | Integration tests |
| INF-002 | Implement TaskRepository | Integration tests |
| INF-003 | Implement PhaseRepository | Integration tests |
| INF-004 | Implement PlanRepository | Integration tests |
| INF-005 | Implement ProgressProjection | Integration tests |
| INF-006 | Implement InMemoryEventBus | Integration tests |

### Phase 4: Interface Layer

| Task | Description | Verification |
|------|-------------|--------------|
| INT-001 | Implement CLI entry point | E2E tests |
| INT-002 | Implement task subcommands | E2E tests |
| INT-003 | Implement progress queries | E2E tests |
| INT-004 | Implement output formatters | E2E tests |

### Phase 5: Testing & Validation

| Task | Description | Verification |
|------|-------------|--------------|
| TST-001 | Achieve 95% domain test coverage | Coverage report |
| TST-002 | BDD feature tests | All scenarios pass |
| TST-003 | Architecture dependency tests | No violations |
| TST-004 | CloudEvents contract tests | Schema validation |

---

## 9. BDD Test Specifications

### Feature: Task Completion

```gherkin
Feature: Task Completion
  As a Claude agent
  I want to complete tasks with proper guards
  So that work is properly validated before marking done

  Background:
    Given a plan "API Optimization" exists
    And a phase "Implementation" with number 1 exists
    And a task "Implement caching" in phase 1 exists

  Scenario: Complete task with all subtasks checked
    Given the task has subtasks:
      | title              | checked |
      | Write tests        | true    |
      | Implement feature  | true    |
      | Update docs        | true    |
    When I complete the task
    Then the task status should be "COMPLETE"
    And a TaskCompletedEvent should be emitted

  Scenario: Cannot complete task with unchecked subtasks
    Given the task has subtasks:
      | title              | checked |
      | Write tests        | true    |
      | Implement feature  | false   |
    When I try to complete the task
    Then I should receive an error "Cannot complete: unchecked subtasks"
    And the task status should remain "IN_PROGRESS"

  Scenario: Complete task triggers progress update
    Given phase 1 has 2 tasks
    And task 1.1 is already complete
    When I complete task 1.2
    Then the task status should be "COMPLETE"
    And eventually the phase progress should be 100%
```

---

## 10. Risk Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Context rot during implementation | High | Medium | Frequent commits; detailed WORKTRACKER.md |
| Event schema changes | Medium | High | Version events from day 1 |
| Projection inconsistency | Medium | Medium | Rebuild command; idempotent handlers |
| Test isolation failures | High | Medium | Fresh fixtures per test; no global state |
| Performance regression | Medium | Low | Benchmark suite; small aggregates |

---

## 11. References

### Primary Sources
1. **Vaughn Vernon** - *Implementing Domain-Driven Design* (2013)
2. **Vaughn Vernon** - "Effective Aggregate Design" series
3. **Eric Evans** - *Domain-Driven Design* (2003)
4. **CloudEvents** - CNCF Specification v1.0

### Secondary Sources
5. **Martin Fowler** - CQRS, Event Sourcing patterns
6. **Alistair Cockburn** - Hexagonal Architecture

### ECW Lessons Learned
7. `docs/knowledge/dragonsbelurkin/glimmering-brewing-lake.md`
8. `docs/research/AGGREGATE_ROOT_ANALYSIS.md`

---

## Approval

**Status:** AWAITING USER APPROVAL

**Approval Required For:**
- [ ] Three Aggregate Root design (Task, Phase, Plan)
- [ ] CloudEvents schema approach
- [ ] Strongly typed identity objects
- [ ] Eventual consistency for progress calculations
- [ ] Implementation phase sequence

---

*Document Version: 2.0*
*Last Updated: 2026-01-07*
