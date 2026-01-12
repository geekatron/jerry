# PROJ-001-e-002: Graph-Ready Data Model Extraction from PLAN.md

> **PS ID:** PROJ-001
> **Entry ID:** e-002
> **Date:** 2026-01-09
> **Author:** ps-researcher agent (v2.0.0)
> **Sources:** `projects/archive/PLAN.md`
> **Topic:** Graph Database Architecture and Property Graph Model

---

## L0 - Executive Summary

- **Property Graph Model** adopted for Gremlin-compatible queries with Vertex/Edge base classes enabling future graph database migration
- **Six Node Types** (Plan, Phase, Task, Subtask, Actor, Event) connected by **six Edge Types** (CONTAINS, BELONGS_TO, DEPENDS_ON, EMITTED, PERFORMED_BY, REFERENCES)
- **Strongly Typed Identity Objects** via VertexId inheritance hierarchy with deterministic ID formats (e.g., "TASK-{uuid8}", "PHASE-{uuid8}")
- **Hexagonal Architecture** with IGraphRepository port supporting three adapter phases: FileGraph -> SQLite -> Graph DB
- **CloudEvents 1.0** integration treats Events as graph vertices connected via EMITTED edges for full audit trails

---

## L1 - Technical Specifications

### 1. Graph Primitives

#### Base Classes

| Class | Purpose | Properties |
|-------|---------|------------|
| `Vertex` | Base node class | `id`, `label`, `properties` |
| `Edge` | Base relationship class | `id`, `label`, `outV` (source), `inV` (target) |
| `VertexId` | Strongly typed ID base | Format varies by subclass |
| `EdgeId` | Generated edge identifier | Pattern: `"{outV}--{label}-->{inV}"` |

#### Directory Location
```
src/domain/graph/
├── primitives.py    # Vertex, Edge, VertexId, EdgeId
└── edge_labels.py   # EdgeLabels constants
```

---

### 2. Graph Schema

#### Node Types (Vertices)

| Vertex Type | Role | Aggregate Status |
|-------------|------|------------------|
| `Plan` | Top-level container | AR #3 (Secondary) |
| `Phase` | Logical grouping | AR #2 (Secondary) |
| `Task` | Work unit | AR #1 (Primary) |
| `Subtask` | Checklist item | Entity (within Task) |
| `Actor` | Performer reference | Reference object |
| `Event` | CloudEvent audit | CloudEvent vertex |

#### Edge Types (Relationships)

| Edge Label | Semantics | Direction |
|------------|-----------|-----------|
| `CONTAINS` | Parent has child | parent -> child |
| `BELONGS_TO` | Child references parent | child -> parent |
| `DEPENDS_ON` | Task dependency | task -> task |
| `EMITTED` | Aggregate produced event | aggregate -> event |
| `PERFORMED_BY` | Event actor attribution | event -> actor |
| `REFERENCES` | Evidence linkage | task -> evidence |

#### Edge Properties

| Property | Type | Purpose |
|----------|------|---------|
| `sequence` | int | Ordering of children |
| `created_at` | datetime | Audit timestamp |
| `dependency_type` | string | Semantic dependency classification |

#### ASCII Schema Diagram

```
                              +-------------+
                              |    ACTOR    |
                              |  (Vertex)   |
                              +------+------+
                                     |
                         PERFORMED_BY|
                                     |
+------------------------------------------------------------------------------+
|                                                                              |
|   +------------+   CONTAINS    +------------+   CONTAINS   +----------+     |
|   |    PLAN    |-------------->|   PHASE    |------------->|   TASK   |     |
|   |  (AR #3)   |               |  (AR #2)   |  (ID ref)    | (AR #1)  |     |
|   |  Vertex    |               |  Vertex    |              |  Vertex  |     |
|   +-----+------+               +-----+------+              +----+-----+     |
|         |                            |                          |           |
|         | EMITTED                    | EMITTED                  | CONTAINS  |
|         v                            v                          v           |
|   +------------+               +------------+            +----------+       |
|   |   EVENT    |               |   EVENT    |            | SUBTASK  |       |
|   |  Vertex    |               |  Vertex    |            |  Vertex  |       |
|   |(CloudEvent)|               |(CloudEvent)|            | (Entity) |       |
|   +------------+               +------------+            +----------+       |
|                                                                              |
+------------------------------------------------------------------------------+
```

---

### 3. Identity Objects (VertexId Hierarchy)

#### Inheritance Tree

```python
VertexId (base, graph primitive)
├── PlanId      "PLAN-{uuid8}"
├── PhaseId     "PHASE-{uuid8}"
├── TaskId      "TASK-{uuid8}"
├── SubtaskId   "TASK-xxx.{sequence}"   # Composite: parent TaskId + sequence
├── ActorId     "ACTOR-{type}-{id}"     # e.g., "ACTOR-CLAUDE-main"
└── EventId     "EVT-{uuid}"

EdgeId (base, graph primitive)
└── Generated: "{outV}--{label}-->{inV}"
    e.g., "TASK-ABC123--CONTAINS-->TASK-ABC123.1"
```

#### ID Format Specifications

| ID Type | Format | Example |
|---------|--------|---------|
| PlanId | `PLAN-{uuid8}` | `PLAN-a1b2c3d4` |
| PhaseId | `PHASE-{uuid8}` | `PHASE-e5f6g7h8` |
| TaskId | `TASK-{uuid8}` | `TASK-ABC12345` |
| SubtaskId | `TASK-{parent}.{seq}` | `TASK-ABC123.1` |
| ActorId | `ACTOR-{type}-{id}` | `ACTOR-CLAUDE-main` |
| EventId | `EVT-{uuid}` | `EVT-a1b2c3d4` |
| EdgeId | `{outV}--{label}-->{inV}` | `PHASE-001--CONTAINS-->TASK-001` |

#### Directory Location
```
src/domain/value_objects/
├── identifiers.py   # TaskId, PhaseId, PlanId, SubtaskId
├── actor.py         # Actor, ActorType, ActorId
```

---

### 4. Hexagonal Architecture with Graph Abstractions

#### Port Definition: IGraphRepository

```python
# src/domain/ports/graph_repository.py
from typing import TypeVar, Generic, List, Optional
from domain.graph.primitives import Vertex, Edge, VertexId

T = TypeVar('T', bound=Vertex)

class IGraphRepository(Generic[T]):
    """Secondary port for graph persistence operations."""

    def get(self, id: VertexId) -> Optional[T]:
        """Retrieve vertex by ID."""
        ...

    def save(self, vertex: T) -> None:
        """Persist vertex (upsert)."""
        ...

    def delete(self, id: VertexId) -> bool:
        """Remove vertex and connected edges."""
        ...

    def traverse(self, start: VertexId, edge_label: str) -> List[Vertex]:
        """Follow edges from starting vertex."""
        ...

    def add_edge(self, edge: Edge) -> None:
        """Create relationship between vertices."""
        ...
```

#### Other Secondary Ports

| Port | Purpose |
|------|---------|
| `IEventStore` | Persist CloudEvents as vertices |
| `IEventBus` | Publish/subscribe for eventual consistency |

#### Adapter Implementations (Phased Migration)

| Phase | Adapter | Status |
|-------|---------|--------|
| 1 | `FileGraphRepository` | File-based JSON storage |
| 2 | `SQLiteGraphRepository` | Relational with graph queries |
| 3 | `GraphDbAdapter` | Native graph database (TinkerPop) |

#### Architecture Diagram

```
+------------------------------------------------------------------------------+
|                         INTERFACE LAYER (Primary Adapters)                   |
|  +-------------+  +-------------+  +-------------+                          |
|  |  CLI (wt)   |  | Skill REPL  |  | Sub-agents  |                          |
|  +------+------+  +------+------+  +------+------+                          |
+---------|-----------------|-----------------|---------------------------------+
          |         PRIMARY PORTS             |
+---------|-----------------|-----------------|---------------------------------+
|         |   APPLICATION LAYER (CQRS)        |                                |
|  +------+-----------------------------------+------+                         |
|  | Commands              | Queries                 |                         |
|  | - CreateTask          | - GetTask               |                         |
|  | - CompleteTask        | - GetProgress           |                         |
|  | - AddSubtask          | - TraversePath          |                         |
|  +----------------------------------------------+                            |
|                          |                                                   |
|                    Dispatcher + Middleware                                   |
+--------------------------|---------------------------------------------------+
                           |
+--------------------------|---------------------------------------------------+
|                          |  DOMAIN LAYER (Zero Dependencies)                 |
|  +----------------------------------------------+                            |
|  | Graph Primitives         Aggregates          |                            |
|  | - Vertex (base)          - Task (AR, Vertex) |                            |
|  | - Edge (base)            - Phase (AR, Vertex)|                            |
|  | - VertexId (base)        - Plan (AR, Vertex) |                            |
|  +----------------------------------------------+                            |
|                          |                                                   |
|                   SECONDARY PORTS                                            |
|            +-------------+-------------+                                     |
|            | IGraphRepository<T>       |                                     |
|            | IEventStore               |                                     |
|            | IEventBus                 |                                     |
|            +-------------+-------------+                                     |
+--------------------------|---------------------------------------------------+
                           |
+--------------------------|---------------------------------------------------+
|                          |  INFRASTRUCTURE LAYER (Adapters)                  |
|  +-------------+  +------+------+  +-------------+  +-------------+          |
|  | FileGraph   |  |  SQLite     |  |  Graph DB   |  | InMemory    |          |
|  | Repository  |  | Repository  |  |  Adapter    |  | EventBus    |          |
|  | (Phase 1)   |  | (Phase 2)   |  | (Phase 3)   |  |             |          |
|  +-------------+  +-------------+  +-------------+  +-------------+          |
+------------------------------------------------------------------------------+
```

---

### 5. CloudEvents Integration

#### Event as Vertex Pattern

Events are first-class graph citizens:
1. Aggregates emit events as domain operations complete
2. Events become `Event` vertices in the graph
3. `EMITTED` edge connects aggregate vertex to event vertex
4. `PERFORMED_BY` edge connects event to actor vertex

#### CloudEvent JSON Schema (1.0 Compliant)

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

#### Event Type Hierarchy

| Event Type | Aggregate | Trigger |
|------------|-----------|---------|
| `com.jerry.task.created.v1` | Task | `Task.create()` |
| `com.jerry.task.started.v1` | Task | `Task.start()` |
| `com.jerry.task.completed.v1` | Task | `Task.complete()` |
| `com.jerry.task.blocked.v1` | Task | `Task.block()` |
| `com.jerry.subtask.added.v1` | Task | `Task.add_subtask()` |
| `com.jerry.subtask.checked.v1` | Task | `Subtask.check()` |
| `com.jerry.phase.created.v1` | Phase | `Phase.create()` |
| `com.jerry.phase.task_added.v1` | Phase | `Phase.add_task_ref()` |
| `com.jerry.plan.created.v1` | Plan | `Plan.create()` |

---

### 6. Gremlin Compatibility

#### Supported Traversal Patterns

The graph model is designed for TinkerPop Gremlin compatibility:

```gremlin
// Get all tasks in a phase
g.V('PHASE-001').out('CONTAINS').hasLabel('Task')

// Calculate phase progress
g.V('PHASE-001').out('CONTAINS').hasLabel('Task').group().by('status')

// Find task dependencies
g.V('TASK-001').out('DEPENDS_ON').hasLabel('Task')

// Get task with subtasks
g.V('TASK-001').out('CONTAINS').hasLabel('Subtask')

// Find events emitted by aggregate
g.V('TASK-001').out('EMITTED').hasLabel('Event')

// Trace actor's actions
g.V('ACTOR-CLAUDE-main').in('PERFORMED_BY').hasLabel('Event')
```

#### Progress Calculation via Traversal

```
1. User: "mark task 5.3 complete"
2. Load Task vertex (TASK-ABC123)           <- Single vertex load
3. Task.complete(actor)
   - Validate subtasks
   - Create TaskCompletedEvent vertex
4. Persist:
   - Update Task vertex
   - Create EMITTED edge to Event
5. Return success

=== EVENTUAL CONSISTENCY BOUNDARY ===

6. EventBus publishes TaskCompletedEvent
7. ProgressProjection traverses:
   g.V('PHASE-001').out('CONTAINS').hasLabel('Task').group().by('status')
8. Update Phase progress
```

---

## L2 - Strategic Context

### Why Property Graph Model?

1. **Future Extensibility**: Native graph databases (Neo4j, JanusGraph, Amazon Neptune) use property graph model
2. **Relationship-First Design**: Work tracking is inherently relational (dependencies, containment, attribution)
3. **Gremlin Compatibility**: Industry-standard traversal language enables portable queries
4. **Eventual Consistency**: Graph edges enable event-driven updates without tight coupling

### Trade-offs Accepted

| Decision | Benefit | Cost |
|----------|---------|------|
| Graph abstraction layer | Portable across storage backends | Some performance overhead |
| Strongly typed IDs | Type safety, self-documenting | More boilerplate code |
| Events as vertices | Full audit trail, graph queries | Storage growth |
| Task as primary AR | Fast operations, low contention | More eventual consistency |

### Evidence for Decision

From PLAN.md Key Design Decisions table:

| Decision | Choice | Evidence |
|----------|--------|----------|
| Data Model | Property Graph (Vertex/Edge) | Gremlin compatibility; GRAPH_DATA_MODEL_ANALYSIS.md |
| Primary AR | Task | Vernon's small aggregates; ECW performance issues |
| Event Schema | CloudEvents 1.0 | User hard requirement; CNCF standard |
| Identity Objects | Strongly Typed (VertexId subclasses) | User requirement; graph compatibility |
| Persistence | File-based -> SQLite -> Graph DB | Phased migration path |

### References

1. Apache TinkerPop - https://tinkerpop.apache.org/
2. Practical Gremlin - https://www.kelvinlawrence.net/book/PracticalGremlin.html
3. CloudEvents 1.0 - https://cloudevents.io/
4. Vaughn Vernon - Implementing DDD
5. Internal: `docs/research/GRAPH_DATA_MODEL_ANALYSIS.md`
6. Internal: `docs/research/AGGREGATE_ROOT_ANALYSIS.md`
7. Internal: `docs/research/ECW_COMPREHENSIVE_LESSONS_LEARNED.md`

---

*Document generated by ps-researcher agent (v2.0.0)*
*Source: projects/archive/PLAN.md (v2.0, 2026-01-07)*
