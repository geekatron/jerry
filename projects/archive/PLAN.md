# Jerry Work Tracker v3.0 - Comprehensive Implementation Plan

> **Status:** APPROVED - READY FOR IMPLEMENTATION
> **Created:** 2026-01-07
> **Last Updated:** 2026-01-07
> **Author:** Claude (Distinguished Systems Engineer persona)
> **Approval:** User approved 2026-01-07

---

## Executive Summary

This plan implements the Jerry Work Tracker skill with:
- **Graph-Ready Data Model** with Vertex/Edge abstractions (Gremlin-compatible)
- **Hexagonal Architecture** (Ports & Adapters)
- **Domain-Driven Design** with three Aggregate Roots
- **Event Sourcing** with CloudEvents 1.0
- **CQRS** (Command Query Responsibility Segregation)
- **Self-Healing Aspirations** (MAPE-K patterns)
- **Three-Tier Enforcement** (Soft → Medium → Hard)

### Key Design Decisions

| Decision | Choice | Evidence |
|----------|--------|----------|
| **Data Model** | Property Graph (Vertex/Edge) | Gremlin compatibility; GRAPH_DATA_MODEL_ANALYSIS.md |
| **Primary AR** | Task | Vernon's small aggregates; ECW performance issues |
| **Secondary ARs** | Phase, Plan | Eventual consistency; ID references only |
| **Event Schema** | CloudEvents 1.0 | User hard requirement; CNCF standard |
| **Identity Objects** | Strongly Typed (VertexId subclasses) | User requirement; graph compatibility |
| **Persistence** | File-based → SQLite → Graph DB | Phased migration path |

---

## 1. Problem Statement (5W1H Analysis)

### WHO is affected?
- Claude Code instances tracking multi-phase work
- Users managing complex projects across sessions
- Future graph database migrations

### WHAT problem are we solving?
- Context rot degrades LLM performance in long sessions
- Need persistent work tracking that survives context compaction
- ECW had Plan AR = slow, Phase AR = still slow
- Need graph-ready model for future extensibility

### WHERE does the problem manifest?
- Claude Code sessions with >256k token context
- Large work trackers with 50+ tasks
- Complex dependency relationships between tasks

### WHEN does it occur?
- During multi-hour coding sessions
- When projects grow beyond initial scope
- When querying task dependencies or progress

### WHY does it matter?
- Losing work state disrupts productivity
- Graph queries enable powerful analytics
- Future-proofing for graph database migration

### HOW will we solve it?
- Graph-ready data model (Vertex/Edge abstractions)
- Task-level Aggregate Root for minimal contention
- CloudEvents for auditable event sourcing
- Strongly typed IDs as VertexId subclasses

---

## 2. Architecture Overview

### 2.1 Graph-Ready Data Model

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PROPERTY GRAPH MODEL                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│    VERTICES (Nodes)                    EDGES (Relationships)                 │
│    ─────────────────                   ──────────────────────                │
│    • Plan (AR #3)                      • CONTAINS (parent→child)            │
│    • Phase (AR #2)                     • BELONGS_TO (child→parent)          │
│    • Task (AR #1)                      • DEPENDS_ON (task→task)             │
│    • Subtask (Entity)                  • EMITTED (aggregate→event)          │
│    • Actor (Reference)                 • PERFORMED_BY (event→actor)         │
│    • Event (CloudEvent)                • REFERENCES (task→evidence)         │
│                                                                              │
│    Base Classes:                       Common Properties:                    │
│    • Vertex (id, label, properties)    • sequence (ordering)                │
│    • Edge (id, label, outV, inV)       • created_at (audit)                 │
│    • VertexId (strongly typed)         • dependency_type (semantic)         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Graph Schema

```
                              ┌─────────────┐
                              │    ACTOR    │
                              │  (Vertex)   │
                              └──────┬──────┘
                                     │
                         PERFORMED_BY│
                                     │
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│   ┌────────────┐   CONTAINS    ┌────────────┐   CONTAINS   ┌──────────┐     │
│   │    PLAN    │──────────────►│   PHASE    │─────────────►│   TASK   │     │
│   │  (AR #3)   │               │  (AR #2)   │  (ID ref)    │ (AR #1)  │     │
│   │  Vertex    │               │  Vertex    │              │  Vertex  │     │
│   └─────┬──────┘               └─────┬──────┘              └────┬─────┘     │
│         │                            │                          │           │
│         │ EMITTED                    │ EMITTED                  │ CONTAINS  │
│         ▼                            ▼                          ▼           │
│   ┌────────────┐               ┌────────────┐            ┌──────────┐       │
│   │   EVENT    │               │   EVENT    │            │ SUBTASK  │       │
│   │  Vertex    │               │  Vertex    │            │  Vertex  │       │
│   │(CloudEvent)│               │(CloudEvent)│            │ (Entity) │       │
│   └────────────┘               └────────────┘            └──────────┘       │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 2.3 Hexagonal Architecture with Graph Abstractions

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                         INTERFACE LAYER (Primary Adapters)                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                          │
│  │  CLI (wt)   │  │ Skill REPL  │  │ Sub-agents  │                          │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘                          │
└─────────┼────────────────┼────────────────┼──────────────────────────────────┘
          │         PRIMARY PORTS           │
┌─────────┼────────────────┼────────────────┼──────────────────────────────────┐
│         │   APPLICATION LAYER (CQRS)      │                                  │
│  ┌──────┴─────────────────────────────────┴──────┐                          │
│  │ Commands              │ Queries               │                          │
│  │ • CreateTask          │ • GetTask             │                          │
│  │ • CompleteTask        │ • GetProgress         │                          │
│  │ • AddSubtask          │ • TraversePath        │                          │
│  └───────────────────────┴───────────────────────┘                          │
│                          │                                                   │
│                    Dispatcher + Middleware                                   │
└──────────────────────────┼───────────────────────────────────────────────────┘
                           │
┌──────────────────────────┼───────────────────────────────────────────────────┐
│                          │  DOMAIN LAYER (Zero Dependencies)                 │
│  ┌───────────────────────┼───────────────────────────────────┐              │
│  │ Graph Primitives      │       Aggregates                  │              │
│  │ • Vertex (base)       │       • Task (AR, Vertex)         │              │
│  │ • Edge (base)         │       • Phase (AR, Vertex)        │              │
│  │ • VertexId (base)     │       • Plan (AR, Vertex)         │              │
│  │                       │                                   │              │
│  │ Value Objects         │       Domain Events               │              │
│  │ • TaskId (VertexId)   │       • CloudEventVertex          │              │
│  │ • PhaseId (VertexId)  │       • TaskCreatedEvent          │              │
│  │ • PlanId (VertexId)   │       • TaskCompletedEvent        │              │
│  │ • EdgeLabels          │                                   │              │
│  └───────────────────────┴───────────────────────────────────┘              │
│                          │                                                   │
│                   SECONDARY PORTS                                            │
│            ┌─────────────┴─────────────┐                                    │
│            │ IGraphRepository<T>       │                                    │
│            │ IEventStore               │                                    │
│            │ IEventBus                 │                                    │
│            └─────────────┬─────────────┘                                    │
└──────────────────────────┼───────────────────────────────────────────────────┘
                           │
┌──────────────────────────┼───────────────────────────────────────────────────┐
│                          │  INFRASTRUCTURE LAYER (Adapters)                  │
│  ┌─────────────┐  ┌──────┴──────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ FileGraph   │  │  SQLite     │  │  Graph DB   │  │ InMemory    │         │
│  │ Repository  │  │ Repository  │  │  Adapter    │  │ EventBus    │         │
│  │ (Phase 1)   │  │ (Phase 2)   │  │ (Phase 3)   │  │             │         │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘         │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Strongly Typed Identity Objects (Graph-Ready)

```python
# Inheritance hierarchy:
VertexId (base, graph primitive)
├── PlanId      "PLAN-{uuid8}"
├── PhaseId     "PHASE-{uuid8}"
├── TaskId      "TASK-{uuid8}"
├── SubtaskId   "TASK-xxx.{sequence}"
├── ActorId     "ACTOR-{type}-{id}"
└── EventId     "EVT-{uuid}"

EdgeId (base, graph primitive)
└── Generated: "{outV}--{label}-->{inV}"
```

---

## 4. CloudEvents Domain Events

### 4.1 Event Type Hierarchy

| Event Type | Aggregate | Trigger |
|------------|-----------|---------|
| `com.jerry.task.created.v1` | Task | Task.create() |
| `com.jerry.task.started.v1` | Task | Task.start() |
| `com.jerry.task.completed.v1` | Task | Task.complete() |
| `com.jerry.task.blocked.v1` | Task | Task.block() |
| `com.jerry.subtask.added.v1` | Task | Task.add_subtask() |
| `com.jerry.subtask.checked.v1` | Task | Subtask.check() |
| `com.jerry.phase.created.v1` | Phase | Phase.create() |
| `com.jerry.phase.task_added.v1` | Phase | Phase.add_task_ref() |
| `com.jerry.plan.created.v1` | Plan | Plan.create() |

### 4.2 CloudEvent as Graph Vertex

```json
{
  "specversion": "1.0",
  "type": "com.jerry.task.completed.v1",
  "source": "/jerry/tasks/TASK-ABC123",
  "id": "EVT-a1b2c3d4",
  "time": "2026-01-07T14:30:00Z",
  "subject": "TASK-ABC123",
  "datacontenttype": "application/json",
  "data": {
    "task_id": "TASK-ABC123",
    "phase_id": "PHASE-001",
    "completed_by": {"type": "CLAUDE", "id": "main"},
    "subtasks_completed": 5
  }
}
```

---

## 5. Eventual Consistency Event Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    TASK COMPLETION EVENT FLOW                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. User: "mark task 5.3 complete"                                          │
│     │                                                                        │
│     ▼                                                                        │
│  2. Load Task vertex (TASK-ABC123)  ← Fast: single vertex only              │
│     │                                                                        │
│     ▼                                                                        │
│  3. Task.complete(actor)                                                    │
│     ├── Validate: all subtasks checked? ✓                                   │
│     ├── Validate: evidence attached? ✓                                      │
│     └── Create: TaskCompletedEvent vertex                                   │
│     │                                                                        │
│     ▼                                                                        │
│  4. Persist to Graph Store:                                                 │
│     ├── Update Task vertex (status)                                         │
│     └── Create EMITTED edge → Event vertex                                  │
│     │                                                                        │
│     ▼                                                                        │
│  5. Return success immediately                                               │
│                                                                              │
│  ═══════════════════════════════════════════════════════════════════════════│
│                    EVENTUAL CONSISTENCY BOUNDARY                             │
│  ═══════════════════════════════════════════════════════════════════════════│
│                                                                              │
│  6. EventBus publishes TaskCompletedEvent                                   │
│     │                                                                        │
│     ▼                                                                        │
│  7. ProgressProjection traverses graph:                                     │
│     g.V('PHASE-001').out('CONTAINS').hasLabel('Task').group().by('status')  │
│     │                                                                        │
│     ▼                                                                        │
│  8. Update Phase progress (derived from task states)                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Directory Structure

```
jerry/
├── src/
│   ├── __init__.py
│   ├── domain/                          # Zero external dependencies
│   │   ├── __init__.py
│   │   ├── graph/                       # Graph primitives
│   │   │   ├── __init__.py
│   │   │   ├── primitives.py            # Vertex, Edge, VertexId, EdgeId
│   │   │   └── edge_labels.py           # EdgeLabels constants
│   │   ├── aggregates/
│   │   │   ├── __init__.py
│   │   │   ├── task.py                  # Task (AR, extends Vertex)
│   │   │   ├── phase.py                 # Phase (AR, extends Vertex)
│   │   │   └── plan.py                  # Plan (AR, extends Vertex)
│   │   ├── entities/
│   │   │   ├── __init__.py
│   │   │   └── subtask.py               # Subtask (extends Vertex)
│   │   ├── value_objects/
│   │   │   ├── __init__.py
│   │   │   ├── identifiers.py           # TaskId, PhaseId, PlanId, SubtaskId
│   │   │   ├── status.py                # TaskStatus, PhaseStatus, PlanStatus
│   │   │   └── actor.py                 # Actor, ActorType, ActorId
│   │   ├── events/
│   │   │   ├── __init__.py
│   │   │   ├── base.py                  # CloudEventVertex base
│   │   │   ├── task_events.py           # Task domain events
│   │   │   ├── phase_events.py          # Phase domain events
│   │   │   └── plan_events.py           # Plan domain events
│   │   └── ports/
│   │       ├── __init__.py
│   │       ├── graph_repository.py      # IGraphRepository<T>
│   │       ├── event_store.py           # IEventStore
│   │       └── event_bus.py             # IEventBus
│   ├── application/
│   │   ├── __init__.py
│   │   ├── dispatcher.py
│   │   ├── commands/
│   │   │   ├── task_commands.py
│   │   │   └── phase_commands.py
│   │   ├── queries/
│   │   │   ├── task_queries.py
│   │   │   └── progress_queries.py
│   │   └── dtos/
│   │       └── task_dto.py
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── persistence/
│   │   │   ├── file_graph_repository.py # Phase 1: File-based
│   │   │   └── sqlite_graph_repository.py # Phase 2: SQLite
│   │   └── projections/
│   │       └── progress_projection.py
│   └── interface/
│       ├── __init__.py
│       └── cli/
│           └── main.py
└── tests/
    ├── unit/
    │   └── domain/
    │       ├── graph/
    │       │   ├── test_vertex.py
    │       │   └── test_edge.py
    │       ├── value_objects/
    │       │   ├── test_task_id.py
    │       │   └── test_status.py
    │       └── aggregates/
    │           └── test_task.py
    ├── integration/
    ├── bdd/
    │   └── features/
    │       └── task_completion.feature
    └── architecture/
        └── test_dependencies.py
```

---

## 7. Implementation Phases

### Phase 1: Graph Primitives + Domain Layer

| Task ID | Description | BDD Cycle | Verification |
|---------|-------------|-----------|--------------|
| DOM-001 | Implement Vertex base class | RED→GREEN→REFACTOR | Unit tests |
| DOM-002 | Implement Edge base class | RED→GREEN→REFACTOR | Unit tests |
| DOM-003 | Implement VertexId base class | RED→GREEN→REFACTOR | Unit tests |
| DOM-004 | Implement EdgeId class | RED→GREEN→REFACTOR | Unit tests |
| DOM-005 | Implement EdgeLabels constants | N/A | Code review |
| DOM-006 | Implement TaskId (extends VertexId) | RED→GREEN→REFACTOR | Unit tests |
| DOM-007 | Implement PhaseId (extends VertexId) | RED→GREEN→REFACTOR | Unit tests |
| DOM-008 | Implement PlanId (extends VertexId) | RED→GREEN→REFACTOR | Unit tests |
| DOM-009 | Implement SubtaskId (composite) | RED→GREEN→REFACTOR | Unit tests |
| DOM-010 | Implement TaskStatus state machine | RED→GREEN→REFACTOR | Unit tests |
| DOM-011 | Implement PhaseStatus state machine | RED→GREEN→REFACTOR | Unit tests |
| DOM-012 | Implement PlanStatus state machine | RED→GREEN→REFACTOR | Unit tests |
| DOM-013 | Implement Actor value object | RED→GREEN→REFACTOR | Unit tests |
| DOM-014 | Implement CloudEventVertex base | RED→GREEN→REFACTOR | Unit tests |
| DOM-015 | Implement task domain events | RED→GREEN→REFACTOR | Unit tests |
| DOM-016 | Implement Subtask entity (Vertex) | RED→GREEN→REFACTOR | Unit tests |
| DOM-017 | Implement Task aggregate (Vertex) | RED→GREEN→REFACTOR | Unit tests |
| DOM-018 | Implement Phase aggregate (Vertex) | RED→GREEN→REFACTOR | Unit tests |
| DOM-019 | Implement Plan aggregate (Vertex) | RED→GREEN→REFACTOR | Unit tests |
| DOM-020 | Define IGraphRepository port | N/A | Interface review |
| DOM-021 | Define IEventStore port | N/A | Interface review |
| DOM-022 | Define IEventBus port | N/A | Interface review |

### Phase 2: Application Layer

| Task ID | Description | BDD Cycle | Verification |
|---------|-------------|-----------|--------------|
| APP-001 | Implement command dispatcher | RED→GREEN→REFACTOR | Unit tests |
| APP-002 | Implement CreateTaskCommand | RED→GREEN→REFACTOR | Unit tests |
| APP-003 | Implement CompleteTaskCommand | RED→GREEN→REFACTOR | Unit tests |
| APP-004 | Implement AddSubtaskCommand | RED→GREEN→REFACTOR | Unit tests |
| APP-005 | Implement CheckSubtaskCommand | RED→GREEN→REFACTOR | Unit tests |
| APP-006 | Implement GetTaskQuery | RED→GREEN→REFACTOR | Unit tests |
| APP-007 | Implement GetProgressQuery | RED→GREEN→REFACTOR | Unit tests |
| APP-008 | Implement TraversePathQuery | RED→GREEN→REFACTOR | Unit tests |
| APP-009 | Implement TaskDTO | N/A | Schema validation |

### Phase 3: Infrastructure Layer

| Task ID | Description | BDD Cycle | Verification |
|---------|-------------|-----------|--------------|
| INF-001 | Implement FileGraphRepository | RED→GREEN→REFACTOR | Integration tests |
| INF-002 | Implement FileEventStore | RED→GREEN→REFACTOR | Integration tests |
| INF-003 | Implement InMemoryEventBus | RED→GREEN→REFACTOR | Integration tests |
| INF-004 | Implement ProgressProjection | RED→GREEN→REFACTOR | Integration tests |
| INF-005 | Implement JSON serialization | RED→GREEN→REFACTOR | Contract tests |

### Phase 4: Interface Layer

| Task ID | Description | BDD Cycle | Verification |
|---------|-------------|-----------|--------------|
| INT-001 | Implement CLI entry point | RED→GREEN→REFACTOR | E2E tests |
| INT-002 | Implement task subcommands | RED→GREEN→REFACTOR | E2E tests |
| INT-003 | Implement output formatters | RED→GREEN→REFACTOR | E2E tests |

### Phase 5: Testing & Validation

| Task ID | Description | Verification |
|---------|-------------|--------------|
| TST-001 | Achieve 95% domain test coverage | Coverage report |
| TST-002 | BDD feature tests complete | All scenarios pass |
| TST-003 | Architecture dependency tests | No violations |
| TST-004 | CloudEvents contract tests | Schema validation |
| TST-005 | Graph traversal tests | Gremlin pattern compliance |

---

## 8. BDD Test Specifications

### Feature: Task as Graph Vertex

```gherkin
Feature: Task Graph Operations
  As a developer
  I want Tasks to be graph vertices
  So that I can traverse relationships

  Scenario: Create task creates vertex with ID
    Given a phase "PHASE-001" exists
    When I create a task "Implement feature"
    Then a Task vertex should exist
    And the vertex should have a strongly-typed TaskId
    And the vertex should have label "Task"

  Scenario: Add subtask creates CONTAINS edge
    Given a task "TASK-001" exists
    When I add subtask "Write tests"
    Then a Subtask vertex should exist
    And a CONTAINS edge should exist from Task to Subtask
    And the edge should have sequence property

  Scenario: Complete task emits event as vertex
    Given a task "TASK-001" with all subtasks checked
    When I complete the task
    Then an Event vertex should exist
    And an EMITTED edge should connect Task to Event
    And the Event should be CloudEvents 1.0 compliant
```

### Feature: Graph Traversal

```gherkin
Feature: Graph Traversal Queries
  As a user
  I want to traverse task relationships
  So that I can understand dependencies

  Scenario: Traverse phase to tasks
    Given a phase with 3 tasks
    When I traverse CONTAINS edges from phase
    Then I should get 3 Task vertices

  Scenario: Calculate progress via traversal
    Given a phase with tasks: 2 complete, 1 pending
    When I query phase progress
    Then the progress should be 66%
```

---

## 9. Risk Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Graph abstraction overhead | Medium | Medium | Benchmark against direct storage |
| Gremlin compatibility gaps | Low | Medium | Test patterns early |
| Event schema evolution | Medium | High | Version from day 1 |
| Context compaction | High | Medium | Frequent commits; detailed WORKTRACKER.md |

---

## 10. References

### Research Documents
1. `docs/research/GRAPH_DATA_MODEL_ANALYSIS.md` - Graph model design
2. `docs/research/AGGREGATE_ROOT_ANALYSIS.md` - AR sizing decision
3. `docs/research/ECW_COMPREHENSIVE_LESSONS_LEARNED.md` - ECW patterns

### External References
4. Apache TinkerPop - https://tinkerpop.apache.org/
5. Practical Gremlin - https://www.kelvinlawrence.net/book/PracticalGremlin.html
6. CloudEvents 1.0 - https://cloudevents.io/
7. Vaughn Vernon - Implementing DDD

---

## 11. Approval

**Status:** ✅ APPROVED

**Approved Items:**
- [x] Graph-ready data model (Vertex/Edge)
- [x] Task-level Aggregate Root design
- [x] CloudEvents 1.0 schema
- [x] Three-Tier Enforcement patterns (aspirational)
- [x] Eventual consistency event flows
- [x] Self-healing architecture (aspirational)
- [x] Implementation phase sequence

---

*Document Version: 2.0*
*Last Updated: 2026-01-07*
