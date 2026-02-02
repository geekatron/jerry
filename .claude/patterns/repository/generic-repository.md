# PAT-REPO-001: Generic Repository Pattern

> **Status**: MANDATORY
> **Category**: Repository Pattern
> **Location**: `src/work_tracking/domain/ports/repository.py`

---

## Overview

The Generic Repository is a domain port that abstracts aggregate persistence. It provides collection-like semantics for storing and retrieving aggregates without exposing storage implementation details.

---

## Industry Prior Art

| Source | Key Insight |
|--------|-------------|
| **Eric Evans** (DDD) | "A Repository represents all objects of a type as a conceptual set" |
| **Martin Fowler** | "Repository mediates between domain and data mapping layers" |
| **Vaughn Vernon** | "Repositories should be one per aggregate, not per entity" |

---

## Jerry Implementation

### Port Definition

```python
# File: src/work_tracking/domain/ports/repository.py
from __future__ import annotations

from typing import Generic, Protocol, TypeVar

from src.work_tracking.domain.aggregates.base import AggregateRoot


TAggregate = TypeVar("TAggregate", bound=AggregateRoot)
TId = TypeVar("TId", contravariant=True)


class IRepository(Protocol[TAggregate, TId]):
    """Generic repository port for aggregate persistence.

    Provides collection-like semantics:
    - get: Retrieve by ID (returns None if not found)
    - get_or_raise: Retrieve by ID (raises if not found)
    - save: Persist aggregate (insert or update)
    - delete: Remove aggregate
    - exists: Check if aggregate exists

    Design Principles:
    - One repository per aggregate root
    - Collection semantics, not CRUD
    - Optimistic concurrency via version checking
    - Domain-focused, not data-focused

    References:
        - PAT-ENT-003: AggregateRoot base class
        - PAT-EVT-004: Event Store (for event-sourced repos)
    """

    def get(self, id: TId) -> TAggregate | None:
        """Retrieve aggregate by ID.

        Returns None if aggregate doesn't exist.
        Use get_or_raise when aggregate should exist.
        """
        ...

    def get_or_raise(self, id: TId) -> TAggregate:
        """Retrieve aggregate or raise if not found.

        Raises:
            AggregateNotFoundError: If aggregate doesn't exist
        """
        ...

    def save(self, aggregate: TAggregate) -> None:
        """Persist aggregate.

        Handles both insert (new aggregate) and update (existing).
        For event-sourced aggregates, appends new events.

        Raises:
            ConcurrencyError: If version conflict detected
        """
        ...

    def delete(self, id: TId) -> bool:
        """Remove aggregate.

        Returns True if deleted, False if not found.
        For event-sourced aggregates, may be soft delete.
        """
        ...

    def exists(self, id: TId) -> bool:
        """Check if aggregate exists."""
        ...


class RepositoryError(Exception):
    """Base error for repository operations."""
    pass


class AggregateNotFoundError(RepositoryError):
    """Raised when aggregate doesn't exist."""

    def __init__(self, aggregate_type: str, aggregate_id: str) -> None:
        self.aggregate_type = aggregate_type
        self.aggregate_id = aggregate_id
        super().__init__(f"{aggregate_type} with ID {aggregate_id} not found")


class ConcurrencyError(RepositoryError):
    """Raised when optimistic concurrency check fails."""

    def __init__(
        self,
        aggregate_type: str,
        aggregate_id: str,
        expected_version: int,
        actual_version: int,
    ) -> None:
        self.aggregate_type = aggregate_type
        self.aggregate_id = aggregate_id
        self.expected_version = expected_version
        self.actual_version = actual_version
        super().__init__(
            f"Concurrency conflict for {aggregate_type} {aggregate_id}: "
            f"expected version {expected_version}, found {actual_version}"
        )
```

---

## Domain-Specific Repository

```python
# File: src/work_tracking/domain/ports/work_item_repository.py
from typing import Protocol, Sequence

from src.work_tracking.domain.aggregates.work_item import WorkItem
from src.work_tracking.domain.value_objects.work_item_id import WorkItemId
from src.work_tracking.domain.value_objects.work_item_status import WorkItemStatus


class IWorkItemRepository(Protocol):
    """Repository for WorkItem aggregate.

    Extends generic repository with domain-specific queries.
    """

    def get(self, id: WorkItemId) -> WorkItem | None:
        """Get work item by ID."""
        ...

    def get_or_raise(self, id: WorkItemId) -> WorkItem:
        """Get work item or raise AggregateNotFoundError."""
        ...

    def save(self, work_item: WorkItem) -> None:
        """Persist work item."""
        ...

    def delete(self, id: WorkItemId) -> bool:
        """Delete work item."""
        ...

    def exists(self, id: WorkItemId) -> bool:
        """Check if work item exists."""
        ...

    # Domain-specific queries
    def find_by_status(self, status: WorkItemStatus) -> Sequence[WorkItem]:
        """Find all work items with given status."""
        ...

    def find_by_parent(self, parent_id: WorkItemId) -> Sequence[WorkItem]:
        """Find all children of a work item."""
        ...

    def count_by_status(self, status: WorkItemStatus) -> int:
        """Count work items with given status."""
        ...
```

---

## Repository Adapter

```python
# File: src/work_tracking/infrastructure/persistence/work_item_repository.py
from typing import Sequence

from src.work_tracking.domain.aggregates.work_item import WorkItem
from src.work_tracking.domain.ports.event_store import IEventStore
from src.work_tracking.domain.ports.repository import (
    AggregateNotFoundError,
    ConcurrencyError,
)
from src.work_tracking.domain.ports.work_item_repository import IWorkItemRepository
from src.work_tracking.domain.value_objects.work_item_id import WorkItemId
from src.work_tracking.domain.value_objects.work_item_status import WorkItemStatus


class EventSourcedWorkItemRepository:
    """Event-sourced implementation of work item repository.

    Uses event store for persistence.
    Reconstructs aggregates via history replay.
    """

    def __init__(self, event_store: IEventStore) -> None:
        self._event_store = event_store

    def get(self, id: WorkItemId) -> WorkItem | None:
        """Load aggregate from event history."""
        stream_id = self._stream_id(id)
        events = self._event_store.read(stream_id)

        if not events:
            return None

        domain_events = [self._to_domain_event(e) for e in events]
        return WorkItem.load_from_history(domain_events)

    def get_or_raise(self, id: WorkItemId) -> WorkItem:
        """Load aggregate or raise if not found."""
        work_item = self.get(id)
        if work_item is None:
            raise AggregateNotFoundError("WorkItem", id.value)
        return work_item

    def save(self, work_item: WorkItem) -> None:
        """Append new events to stream."""
        stream_id = self._stream_id(WorkItemId(work_item.id))
        events = work_item.collect_events()

        if not events:
            return

        stored_events = [self._to_stored_event(e, stream_id) for e in events]
        expected_version = work_item.version - len(events)

        try:
            self._event_store.append(stream_id, stored_events, expected_version)
        except self._event_store.ConcurrencyError as e:
            raise ConcurrencyError(
                aggregate_type="WorkItem",
                aggregate_id=work_item.id,
                expected_version=expected_version,
                actual_version=e.actual_version,
            )

    def delete(self, id: WorkItemId) -> bool:
        """Soft delete by appending tombstone event."""
        stream_id = self._stream_id(id)
        return self._event_store.delete_stream(stream_id)

    def exists(self, id: WorkItemId) -> bool:
        """Check if stream exists."""
        stream_id = self._stream_id(id)
        return self._event_store.stream_exists(stream_id)

    def _stream_id(self, id: WorkItemId) -> str:
        """Generate stream ID from work item ID."""
        return f"WorkItem-{id.value}"
```

---

## Key Principles

### 1. One Per Aggregate

```python
# CORRECT: One repository per aggregate root
work_item_repo: IWorkItemRepository
phase_repo: IPhaseRepository
plan_repo: IPlanRepository

# WRONG: Repository for non-root entity
subtask_repo: ISubtaskRepository  # Subtasks accessed via WorkItem
```

### 2. Collection Semantics

```python
# Repository is like a collection
repo.get(id)      # Like dict.get()
repo.save(item)   # Like set.add()
repo.delete(id)   # Like set.remove()
repo.exists(id)   # Like id in collection
```

### 3. Domain-Focused

```python
# CORRECT: Domain queries
repo.find_by_status(WorkItemStatus.IN_PROGRESS)
repo.find_by_parent(parent_id)

# WRONG: Data queries (SQL-like)
repo.select_where({"status": "in_progress", "priority": {"$gt": 2}})
```

---

## Testing Pattern

```python
def test_repository_saves_and_retrieves_aggregate():
    """Repository persists aggregate state."""
    repo = EventSourcedWorkItemRepository(InMemoryEventStore())

    work_item = WorkItem.create(
        id="WORK-001",
        title="Test Task",
    )
    work_item.start()

    repo.save(work_item)
    retrieved = repo.get(WorkItemId("WORK-001"))

    assert retrieved is not None
    assert retrieved.id == "WORK-001"
    assert retrieved.status == WorkItemStatus.IN_PROGRESS


def test_repository_raises_on_not_found():
    """get_or_raise raises for missing aggregate."""
    repo = EventSourcedWorkItemRepository(InMemoryEventStore())

    with pytest.raises(AggregateNotFoundError) as exc_info:
        repo.get_or_raise(WorkItemId("NONEXISTENT"))

    assert "NONEXISTENT" in str(exc_info.value)


def test_repository_detects_concurrency_conflict():
    """Concurrent saves are detected."""
    event_store = InMemoryEventStore()
    repo = EventSourcedWorkItemRepository(event_store)

    # First save
    item = WorkItem.create(id="WORK-001", title="Test")
    repo.save(item)

    # Simulate concurrent modification
    item1 = repo.get(WorkItemId("WORK-001"))
    item2 = repo.get(WorkItemId("WORK-001"))

    item1.start()
    repo.save(item1)  # Succeeds

    item2.start()
    with pytest.raises(ConcurrencyError):
        repo.save(item2)  # Fails - stale version
```

---

## Jerry-Specific Decisions

> **Jerry Decision**: Repositories are protocol-based ports, not abstract base classes. This enables better testing and composition.

> **Jerry Decision**: Event-sourced repositories append events, not snapshots. Snapshots are optional optimization (PAT-REPO-003).

> **Jerry Decision**: Domain-specific queries return aggregate collections, not DTOs. For read-optimized queries, use projections.

---

## Anti-Patterns

### 1. Generic CRUD Repository

```python
# WRONG: Generic CRUD
class CrudRepository:
    def insert(self, data: dict): ...
    def update(self, id: str, data: dict): ...
    def select(self, where: dict): ...

# CORRECT: Domain-focused
class IWorkItemRepository:
    def save(self, work_item: WorkItem): ...
    def find_by_status(self, status: WorkItemStatus): ...
```

### 2. Anemic Repository

```python
# WRONG: Repository just wraps ORM
class WorkItemRepository:
    def save(self, item: WorkItemModel):
        self._session.add(item)  # No domain logic

# CORRECT: Repository works with aggregates
class WorkItemRepository:
    def save(self, item: WorkItem):
        events = item.collect_events()
        self._event_store.append(...)
```

---

## References

- **Eric Evans**: Domain-Driven Design (2003), Chapter 6 - Repositories
- **Martin Fowler**: [Repository Pattern](https://martinfowler.com/eaaCatalog/repository.html)
- **Vaughn Vernon**: Implementing DDD (2013), Chapter 12
- **Design Canon**: Section 5.6 - Repository Pattern
- **Related Patterns**: PAT-ENT-003 (AggregateRoot), PAT-EVT-004 (Event Store)
