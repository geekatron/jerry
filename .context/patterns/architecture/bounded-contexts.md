# PAT-ARCH-003: Bounded Contexts Pattern

> **Status**: MANDATORY
> **Category**: Architecture Pattern
> **Location**: `src/*/`

---

## Overview

Bounded Contexts define explicit boundaries within which a domain model is consistent. Each context has its own ubiquitous language, domain model, and can evolve independently.

---

## Industry Prior Art

| Source | Key Insight |
|--------|-------------|
| **Eric Evans** | "Explicitly define the context within which a model applies" |
| **Vaughn Vernon** | "Bounded Contexts are a semantic boundary, not just a code boundary" |
| **Martin Fowler** | "Each Bounded Context can have its own architecture" |

---

## Jerry Bounded Contexts

### Context Map

```
┌─────────────────────────────────────────────────────────────────┐
│                        Jerry Framework                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌───────────────────┐         ┌───────────────────┐           │
│  │ session_management│◄───────►│   work_tracking   │           │
│  │                   │   SK    │                   │           │
│  │  • Project        │         │  • WorkItem       │           │
│  │  • Session        │         │  • Phase          │           │
│  │  • ProjectInfo    │         │  • Task           │           │
│  └─────────┬─────────┘         └─────────┬─────────┘           │
│            │                             │                      │
│            │ SK                          │ SK                   │
│            ▼                             ▼                      │
│  ┌─────────────────────────────────────────────────┐           │
│  │               shared_kernel                      │           │
│  │  - VertexId, SnowflakeIdGenerator               │           │
│  │  - DomainEvent, AggregateRoot                   │           │
│  │  - IAuditable, IVersioned                       │           │
│  │  - Common exceptions                            │           │
│  └─────────────────────────────────────────────────┘           │
│                                                                 │
│  ┌───────────────────┐                                         │
│  │  problem_solving  │  (Future - ps-* agents)                 │
│  │                   │                                         │
│  │  • ProblemSpace   │                                         │
│  │  • Analysis       │                                         │
│  │  • Solution       │                                         │
│  └───────────────────┘                                         │
│                                                                 │
│  Legend: SK = Shared Kernel, ◄──► = Partnership                │
└─────────────────────────────────────────────────────────────────┘
```

---

## Context Descriptions

### Session Management Context

**Purpose**: Manage project workspaces and user sessions.

**Core Concepts**:
- **Project**: A workspace with its own PLAN.md and WORKTRACKER.md
- **Session**: Active user session within a project
- **ProjectInfo**: Metadata about project (status, path)

**Ubiquitous Language**:
- "Activate project" = Set JERRY_PROJECT environment
- "Scan projects" = Discover available project directories
- "Project context" = Current active project state

```
src/session_management/
├── domain/
│   ├── aggregates/
│   │   └── project.py
│   ├── entities/
│   │   └── project_info.py
│   └── value_objects/
│       └── project_id.py
├── application/
│   ├── commands/
│   ├── queries/
│   └── handlers/
└── infrastructure/
    └── adapters/
```

---

### Work Tracking Context

**Purpose**: Track work items, tasks, and their lifecycle.

**Core Concepts**:
- **WorkItem**: Unit of work (task, bug, epic)
- **Phase**: Project phase grouping work items
- **Subtask**: Child work items
- **Dependency**: Work item relationships

**Ubiquitous Language**:
- "Create task" = New work item of type task
- "Complete work item" = Transition to DONE status
- "Block work item" = Set BLOCKED status with blocker

```
src/work_tracking/
├── domain/
│   ├── aggregates/
│   │   └── work_item.py
│   ├── entities/
│   │   └── phase.py
│   ├── value_objects/
│   │   ├── work_item_id.py
│   │   ├── work_item_status.py
│   │   └── priority.py
│   ├── events/
│   │   └── work_item_events.py
│   └── services/
│       └── quality_validator.py
├── application/
│   ├── commands/
│   ├── queries/
│   └── handlers/
└── infrastructure/
    └── persistence/
```

---

### Shared Kernel

**Purpose**: Code shared across bounded contexts.

**Contains**:
- Identity types (VertexId hierarchy)
- Base classes (DomainEvent, AggregateRoot)
- Common protocols (IAuditable, IVersioned)
- Shared exceptions (DomainError hierarchy)

**Rules**:
- Shared kernel is owned by ALL contexts
- Changes require agreement from all contexts
- Keep minimal - only truly shared concepts

```
src/shared_kernel/
├── identity/
│   ├── vertex_id.py
│   └── snowflake_id_generator.py
├── domain/
│   ├── domain_event.py
│   └── aggregate_root.py
├── protocols/
│   ├── iauditable.py
│   └── iversioned.py
└── exceptions.py
```

---

## Context Relationships

### Shared Kernel (SK)

Shared code that multiple contexts depend on. Changes affect all contexts.

```python
# Both contexts use VertexId from shared kernel
from src.shared_kernel.identity.vertex_id import WorkItemId, ProjectId
```

### Partnership

Contexts collaborate and co-evolve. Changes are coordinated.

```
session_management ◄──► work_tracking

# Work tracking needs project context
# Session management needs work item counts
```

### Customer-Supplier (Future)

One context provides service to another.

```
problem_solving (Customer) ◄── work_tracking (Supplier)

# Problem solving uses work tracking data
# Work tracking doesn't depend on problem solving
```

---

## Context Communication

### Within Context

Direct method calls, domain events.

```python
# Within work_tracking context
work_item.complete()  # Domain method
events = work_item.collect_events()  # Domain events
```

### Between Contexts

Integration events (CloudEvents), Anti-Corruption Layer.

```python
# Cross-context communication via integration events
from src.shared_kernel.integration_events import CloudEvent

event = CloudEvent(
    type="jerry.work_tracking.task.completed",
    source="/jerry/work-tracking",
    data={"task_id": "WORK-001"},
)
event_publisher.publish(event)
```

### Anti-Corruption Layer

Translate between context languages.

```python
# session_management speaking to work_tracking
class WorkTrackingACL:
    """Anti-Corruption Layer for work tracking context."""

    def __init__(self, work_tracking_query_dispatcher):
        self._dispatcher = work_tracking_query_dispatcher

    def get_active_work_count(self, project_id: str) -> int:
        """Translate our project_id to work_tracking query."""
        # Our context: project_id
        # Their context: query by status
        query = ListWorkItemsQuery(
            status="in_progress",
            project_filter=project_id,
        )
        result = self._dispatcher.dispatch(query)
        return result.total
```

---

## Directory Structure

```
src/
├── session_management/              # Bounded Context
│   ├── domain/
│   │   ├── aggregates/
│   │   ├── entities/
│   │   ├── value_objects/
│   │   └── ports/
│   ├── application/
│   │   ├── commands/
│   │   ├── queries/
│   │   └── handlers/
│   └── infrastructure/
│       └── adapters/
│
├── work_tracking/                   # Bounded Context
│   ├── domain/
│   │   ├── aggregates/
│   │   ├── entities/
│   │   ├── value_objects/
│   │   ├── events/
│   │   ├── services/
│   │   └── ports/
│   ├── application/
│   │   ├── commands/
│   │   ├── queries/
│   │   └── handlers/
│   └── infrastructure/
│       └── persistence/
│
├── problem_solving/                 # Future Bounded Context
│   └── (planned)
│
└── shared_kernel/                   # Shared Code
    ├── identity/
    ├── domain/
    ├── protocols/
    └── exceptions.py
```

---

## Testing Pattern

```python
def test_contexts_do_not_cross_import():
    """Bounded contexts don't import from each other."""
    import ast

    work_tracking_files = Path("src/work_tracking").rglob("*.py")

    for file in work_tracking_files:
        tree = ast.parse(file.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert "session_management" not in alias.name

            if isinstance(node, ast.ImportFrom):
                if node.module:
                    assert "session_management" not in node.module


def test_shared_kernel_has_no_context_imports():
    """Shared kernel doesn't import from contexts."""
    shared_kernel_files = Path("src/shared_kernel").rglob("*.py")

    for file in shared_kernel_files:
        tree = ast.parse(file.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module:
                    assert "work_tracking" not in node.module
                    assert "session_management" not in node.module
```

---

## Jerry-Specific Decisions

> **Jerry Decision**: Each bounded context has full hexagonal architecture (domain, application, infrastructure).

> **Jerry Decision**: Cross-context communication uses CloudEvents format for integration events.

> **Jerry Decision**: Shared kernel is minimal: identity, base classes, protocols, exceptions only.

> **Jerry Decision**: No direct imports across context boundaries. Use ACL or integration events.

---

## Anti-Patterns

### 1. Shared Domain Model

```python
# WRONG: Both contexts share WorkItem
# src/work_tracking/domain/work_item.py - used by session_management too

# CORRECT: Each context has its own model
# src/work_tracking/domain/work_item.py
# src/session_management/domain/project.py (has task_count, not WorkItem)
```

### 2. Cross-Context Imports

```python
# WRONG: Direct import across contexts
from src.work_tracking.domain.aggregates.work_item import WorkItem

# CORRECT: Use integration events or ACL
work_item_completed_event = await event_bus.subscribe(
    "jerry.work_tracking.task.completed"
)
```

### 3. Bloated Shared Kernel

```python
# WRONG: Context-specific code in shared kernel
# src/shared_kernel/work_item.py  # This belongs in work_tracking!

# CORRECT: Only truly shared, stable concepts
# src/shared_kernel/identity/vertex_id.py  # Used by all
```

---

## References

- **Eric Evans**: Domain-Driven Design (2003), Chapter 14 - Bounded Contexts
- **Vaughn Vernon**: Implementing DDD (2013), Chapter 3
- **Martin Fowler**: [Bounded Context](https://martinfowler.com/bliki/BoundedContext.html)
- **Design Canon**: Section 3.1 - Bounded Contexts
- **Related Patterns**: PAT-ARCH-001 (Composition Root), PAT-EVT-002 (CloudEvents)
