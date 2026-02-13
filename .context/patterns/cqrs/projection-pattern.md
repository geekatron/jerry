# PAT-CQRS-004: Projection Pattern

> **Status**: RECOMMENDED
> **Category**: CQRS Pattern
> **Location**: `src/application/projections/`

---

## Overview

Projections are event handlers that build read-optimized views (read models) from domain events. They transform event streams into denormalized data structures optimized for specific queries.

---

## Industry Prior Art

| Source | Key Insight |
|--------|-------------|
| **Greg Young** | "Projections are just event handlers that build read models" |
| **Martin Fowler** | "Read models can be optimized for specific query patterns" |
| **Event Store** | "Projections transform events into useful representations" |

---

## Jerry Implementation

### Projection Port

```python
# File: src/application/ports/secondary/iprojection.py
from __future__ import annotations

from typing import Any, Protocol

from src.shared_kernel.domain_event import DomainEvent


class IProjection(Protocol):
    """Port for event projections.

    Projections handle events to build read models.
    Each projection is responsible for one read model.
    """

    def handle(self, event: DomainEvent) -> None:
        """Process an event and update read model.

        Args:
            event: Domain event to process
        """
        ...

    def get_handled_event_types(self) -> set[type]:
        """Return event types this projection handles."""
        ...
```

---

## Read Model Definition

```python
# File: src/application/read_models/work_item_list_model.py
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class WorkItemListEntry:
    """Single entry in the work item list read model.

    Optimized for list views with commonly displayed fields.
    """

    id: str
    title: str
    status: str
    priority: str
    work_type: str
    created_at: datetime
    updated_at: datetime

    # Computed/aggregated fields
    days_open: int = 0
    subtask_count: int = 0
    blocker_count: int = 0


@dataclass
class WorkItemListReadModel:
    """Read model for work item list queries.

    Denormalized view optimized for listing and filtering.
    """

    items: dict[str, WorkItemListEntry] = field(default_factory=dict)
    by_status: dict[str, set[str]] = field(default_factory=dict)
    by_priority: dict[str, set[str]] = field(default_factory=dict)
    total_count: int = 0

    def get_by_status(self, status: str) -> list[WorkItemListEntry]:
        """Get all items with given status."""
        ids = self.by_status.get(status, set())
        return [self.items[id] for id in ids if id in self.items]

    def get_by_priority(self, priority: str) -> list[WorkItemListEntry]:
        """Get all items with given priority."""
        ids = self.by_priority.get(priority, set())
        return [self.items[id] for id in ids if id in self.items]
```

---

## Projection Implementation

```python
# File: src/application/projections/work_item_list_projection.py
from __future__ import annotations

from datetime import datetime, timezone

from src.application.read_models.work_item_list_model import (
    WorkItemListEntry,
    WorkItemListReadModel,
)
from src.shared_kernel.domain_event import DomainEvent
from src.work_tracking.domain.events.work_item_events import (
    SubtaskAdded,
    WorkItemBlocked,
    WorkItemCancelled,
    WorkItemCompleted,
    WorkItemCreated,
    WorkItemPriorityChanged,
    WorkItemStarted,
    WorkItemUnblocked,
)


class WorkItemListProjection:
    """Projection that builds work item list read model.

    Handles all work item events to maintain a denormalized
    view optimized for list queries.
    """

    def __init__(self, read_model: WorkItemListReadModel | None = None) -> None:
        self._model = read_model or WorkItemListReadModel()

    @property
    def model(self) -> WorkItemListReadModel:
        """Access the read model."""
        return self._model

    def handle(self, event: DomainEvent) -> None:
        """Route event to appropriate handler method."""
        handler_name = f"_on_{type(event).__name__}"
        handler = getattr(self, handler_name, None)

        if handler:
            handler(event)

    def get_handled_event_types(self) -> set[type]:
        """Return all event types this projection handles."""
        return {
            WorkItemCreated,
            WorkItemStarted,
            WorkItemBlocked,
            WorkItemUnblocked,
            WorkItemCompleted,
            WorkItemCancelled,
            WorkItemPriorityChanged,
            SubtaskAdded,
        }

    def _on_WorkItemCreated(self, event: WorkItemCreated) -> None:
        """Handle work item creation."""
        entry = WorkItemListEntry(
            id=event.work_item_id,
            title=event.title,
            status="pending",
            priority=event.priority,
            work_type=event.work_type,
            created_at=event.timestamp,
            updated_at=event.timestamp,
        )

        self._model.items[event.work_item_id] = entry
        self._add_to_index("by_status", "pending", event.work_item_id)
        self._add_to_index("by_priority", event.priority, event.work_item_id)
        self._model.total_count += 1

    def _on_WorkItemStarted(self, event: WorkItemStarted) -> None:
        """Handle work item started."""
        entry = self._model.items.get(event.work_item_id)
        if entry:
            old_status = entry.status
            entry.status = "in_progress"
            entry.updated_at = event.timestamp
            self._move_in_index("by_status", old_status, "in_progress", event.work_item_id)

    def _on_WorkItemBlocked(self, event: WorkItemBlocked) -> None:
        """Handle work item blocked."""
        entry = self._model.items.get(event.work_item_id)
        if entry:
            old_status = entry.status
            entry.status = "blocked"
            entry.blocker_count += 1
            entry.updated_at = event.timestamp
            self._move_in_index("by_status", old_status, "blocked", event.work_item_id)

    def _on_WorkItemUnblocked(self, event: WorkItemUnblocked) -> None:
        """Handle work item unblocked."""
        entry = self._model.items.get(event.work_item_id)
        if entry:
            old_status = entry.status
            entry.status = "in_progress"
            entry.blocker_count = max(0, entry.blocker_count - 1)
            entry.updated_at = event.timestamp
            self._move_in_index("by_status", old_status, "in_progress", event.work_item_id)

    def _on_WorkItemCompleted(self, event: WorkItemCompleted) -> None:
        """Handle work item completed."""
        entry = self._model.items.get(event.work_item_id)
        if entry:
            old_status = entry.status
            entry.status = "done"
            entry.updated_at = event.timestamp
            self._move_in_index("by_status", old_status, "done", event.work_item_id)

    def _on_WorkItemCancelled(self, event: WorkItemCancelled) -> None:
        """Handle work item cancelled."""
        entry = self._model.items.get(event.work_item_id)
        if entry:
            old_status = entry.status
            entry.status = "cancelled"
            entry.updated_at = event.timestamp
            self._move_in_index("by_status", old_status, "cancelled", event.work_item_id)

    def _on_WorkItemPriorityChanged(self, event: WorkItemPriorityChanged) -> None:
        """Handle priority change."""
        entry = self._model.items.get(event.work_item_id)
        if entry:
            self._move_in_index(
                "by_priority",
                event.old_priority,
                event.new_priority,
                event.work_item_id,
            )
            entry.priority = event.new_priority
            entry.updated_at = event.timestamp

    def _on_SubtaskAdded(self, event: SubtaskAdded) -> None:
        """Handle subtask added."""
        entry = self._model.items.get(event.work_item_id)
        if entry:
            entry.subtask_count += 1
            entry.updated_at = event.timestamp

    def _add_to_index(self, index_name: str, key: str, item_id: str) -> None:
        """Add item to an index."""
        index = getattr(self._model, index_name)
        if key not in index:
            index[key] = set()
        index[key].add(item_id)

    def _remove_from_index(self, index_name: str, key: str, item_id: str) -> None:
        """Remove item from an index."""
        index = getattr(self._model, index_name)
        if key in index:
            index[key].discard(item_id)

    def _move_in_index(
        self,
        index_name: str,
        old_key: str,
        new_key: str,
        item_id: str,
    ) -> None:
        """Move item between index keys."""
        self._remove_from_index(index_name, old_key, item_id)
        self._add_to_index(index_name, new_key, item_id)
```

---

## Projection Manager

```python
# File: src/application/projections/projection_manager.py
from __future__ import annotations

from typing import Sequence

from src.application.ports.secondary.iprojection import IProjection
from src.shared_kernel.domain_event import DomainEvent


class ProjectionManager:
    """Manages multiple projections.

    Routes events to all registered projections that
    handle that event type.
    """

    def __init__(self, projections: Sequence[IProjection] | None = None) -> None:
        self._projections: list[IProjection] = list(projections) if projections else []
        self._event_handlers: dict[type, list[IProjection]] = {}
        self._build_handler_map()

    def register(self, projection: IProjection) -> None:
        """Register a projection."""
        self._projections.append(projection)
        self._build_handler_map()

    def apply(self, event: DomainEvent) -> None:
        """Apply event to all relevant projections."""
        event_type = type(event)
        handlers = self._event_handlers.get(event_type, [])

        for handler in handlers:
            handler.handle(event)

    def apply_batch(self, events: Sequence[DomainEvent]) -> None:
        """Apply multiple events in order."""
        for event in events:
            self.apply(event)

    def rebuild_from_events(self, events: Sequence[DomainEvent]) -> None:
        """Rebuild all projections from event history."""
        for event in events:
            self.apply(event)

    def _build_handler_map(self) -> None:
        """Build mapping of event types to projections."""
        self._event_handlers.clear()

        for projection in self._projections:
            for event_type in projection.get_handled_event_types():
                if event_type not in self._event_handlers:
                    self._event_handlers[event_type] = []
                self._event_handlers[event_type].append(projection)
```

---

## Integration with Event Store

```python
# File: src/application/projections/event_store_projector.py
from src.application.ports.secondary.iprojection import IProjection
from src.application.projections.projection_manager import ProjectionManager
from src.work_tracking.domain.ports.event_store import IEventStore


class EventStoreProjector:
    """Projects events from event store to read models.

    Can be used for:
    - Initial read model population
    - Read model rebuild after schema change
    - Catch-up projection for new read models
    """

    def __init__(
        self,
        event_store: IEventStore,
        projection_manager: ProjectionManager,
    ) -> None:
        self._event_store = event_store
        self._projection_manager = projection_manager

    def project_stream(self, stream_id: str) -> int:
        """Project all events from a stream.

        Returns:
            Number of events projected
        """
        events = self._event_store.read(stream_id)
        domain_events = [self._deserialize(e) for e in events]

        for event in domain_events:
            self._projection_manager.apply(event)

        return len(events)

    def project_all_streams(self, stream_prefix: str) -> int:
        """Project events from all matching streams.

        Returns:
            Total number of events projected
        """
        # Implementation depends on event store capabilities
        # May need to iterate over all streams matching prefix
        total = 0
        # ... stream iteration logic
        return total

    def _deserialize(self, stored_event) -> DomainEvent:
        """Convert stored event to domain event."""
        from src.work_tracking.domain.events.event_registry import EventRegistry
        return EventRegistry.deserialize(stored_event.data)
```

---

## Projection Flow

```
         Event Source                    Projection Layer
              │                                  │
              │  WorkItemCreated                 │
              │─────────────────────────────────►│
              │                                  ▼
              │                         ┌────────────────┐
              │                         │ Projection     │
              │                         │ Manager        │
              │                         └───────┬────────┘
              │                                 │
              │                    ┌────────────┴────────────┐
              │                    │                         │
              │                    ▼                         ▼
              │          ┌─────────────────┐      ┌─────────────────┐
              │          │ WorkItemList    │      │ ProjectStats    │
              │          │ Projection      │      │ Projection      │
              │          └────────┬────────┘      └────────┬────────┘
              │                   │                        │
              │                   ▼                        ▼
              │          ┌─────────────────┐      ┌─────────────────┐
              │          │ List Read Model │      │ Stats Read Model│
              │          └─────────────────┘      └─────────────────┘
```

---

## Testing Pattern

```python
def test_projection_handles_work_item_created():
    """Projection creates entry on WorkItemCreated."""
    projection = WorkItemListProjection()

    event = WorkItemCreated(
        work_item_id="WORK-001",
        title="Test Task",
        work_type="task",
        priority="high",
    )
    projection.handle(event)

    assert "WORK-001" in projection.model.items
    entry = projection.model.items["WORK-001"]
    assert entry.title == "Test Task"
    assert entry.status == "pending"


def test_projection_updates_indexes():
    """Projection maintains status and priority indexes."""
    projection = WorkItemListProjection()

    # Create and start
    projection.handle(WorkItemCreated(
        work_item_id="WORK-001",
        title="Test",
        work_type="task",
        priority="high",
    ))
    projection.handle(WorkItemStarted(work_item_id="WORK-001"))

    # Verify indexes
    assert "WORK-001" not in projection.model.by_status.get("pending", set())
    assert "WORK-001" in projection.model.by_status.get("in_progress", set())


def test_projection_manager_routes_to_multiple_projections():
    """Manager routes events to all relevant projections."""
    list_projection = WorkItemListProjection()
    stats_projection = ProjectStatsProjection()

    manager = ProjectionManager([list_projection, stats_projection])

    event = WorkItemCreated(
        work_item_id="WORK-001",
        title="Test",
        work_type="task",
        priority="medium",
    )
    manager.apply(event)

    # Both projections updated
    assert "WORK-001" in list_projection.model.items
    assert stats_projection.model.total_items == 1
```

---

## Jerry-Specific Decisions

> **Jerry Decision**: Projections are in-memory for simplicity. File-based persistence for development, database-backed for production (future).

> **Jerry Decision**: Each projection is responsible for one read model. Multiple projections can handle the same event type.

> **Jerry Decision**: Projection handler methods follow `_on_{EventTypeName}` naming convention for automatic routing.

---

## Anti-Patterns

### 1. Projection with Business Logic

```python
# WRONG: Business logic in projection
class WorkItemProjection:
    def _on_WorkItemCreated(self, event):
        if self._validate_business_rule(event):  # Business logic!
            self._model.items[event.id] = ...

# CORRECT: Projection only transforms data
class WorkItemProjection:
    def _on_WorkItemCreated(self, event):
        self._model.items[event.id] = WorkItemEntry(...)
```

### 2. Querying in Projection

```python
# WRONG: Querying other services
class WorkItemProjection:
    def _on_WorkItemCreated(self, event):
        user = self._user_service.get(event.user_id)  # Query!
        self._model.items[event.id] = WorkItemEntry(user_name=user.name)

# CORRECT: Store only event data, denormalize via events
class WorkItemProjection:
    def _on_WorkItemCreated(self, event):
        self._model.items[event.id] = WorkItemEntry(user_id=event.user_id)
```

---

## References

- **Greg Young**: [Event Sourcing and Projections](https://cqrs.files.wordpress.com/2010/11/cqrs_documents.pdf)
- **Event Store**: [Projections](https://developers.eventstore.com/server/v23.10/projections/)
- **Design Canon**: Section 6.5 - Projections
- **Related Patterns**: PAT-CQRS-002 (Query), PAT-EVT-004 (Event Store)
