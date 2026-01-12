# PAT-ENT-004: EntityBase Pattern

> **Status**: RECOMMENDED
> **Category**: Entity Pattern
> **Location**: `src/shared_kernel/entity_base.py`

---

## Overview

EntityBase combines the common concerns of domain entities:
- **Identity** via VertexId (PAT-ID-001)
- **Audit tracking** via IAuditable (PAT-ENT-001)
- **Optimistic concurrency** via IVersioned (PAT-ENT-002)

This provides a consistent foundation for all domain entities while avoiding inheritance hierarchies.

---

## Industry Prior Art

| Source | Key Insight |
|--------|-------------|
| **Eric Evans** (DDD) | "Entities have identity and lifecycle; identity is what matters, not attributes" |
| **Martin Fowler** | "Audit trail through created_at/updated_at is a cross-cutting concern" |
| **Vaughn Vernon** | "Entity identity should be unique across the system lifetime" |

---

## Jerry Implementation

```python
# File: src/shared_kernel/entity_base.py
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from src.shared_kernel.vertex_id import VertexId


def _utc_now() -> datetime:
    """Return current UTC timestamp."""
    return datetime.now(timezone.utc)


@dataclass
class EntityBase:
    """Base class combining VertexId, IAuditable, IVersioned.

    Provides:
    - Identity via VertexId hierarchy
    - Audit tracking (created_by, created_at, updated_by, updated_at)
    - Version tracking for optimistic concurrency

    Usage:
        @dataclass
        class Task(EntityBase):
            title: str
            status: TaskStatus

    References:
        - PAT-ID-001: VertexId pattern
        - PAT-ENT-001: IAuditable protocol
        - PAT-ENT-002: IVersioned protocol
    """

    _id: VertexId
    _version: int = 0
    _created_by: str = "System"
    _created_at: datetime = field(default_factory=_utc_now)
    _updated_by: str = "System"
    _updated_at: datetime = field(default_factory=_utc_now)

    @property
    def id(self) -> VertexId:
        """Entity identity."""
        return self._id

    @property
    def version(self) -> int:
        """Current version for optimistic concurrency."""
        return self._version

    @property
    def created_by(self) -> str:
        """Creator identifier."""
        return self._created_by

    @property
    def created_at(self) -> datetime:
        """Creation timestamp."""
        return self._created_at

    @property
    def updated_by(self) -> str:
        """Last modifier identifier."""
        return self._updated_by

    @property
    def updated_at(self) -> datetime:
        """Last modification timestamp."""
        return self._updated_at

    def get_expected_version(self) -> int:
        """Version expected by repository for optimistic concurrency check."""
        return self._version

    def _mark_updated(self, by: str = "System") -> None:
        """Update audit metadata.

        Called by subclass methods when entity is modified.
        """
        self._updated_by = by
        self._updated_at = _utc_now()
        self._version += 1
```

---

## Usage Example

```python
# File: src/work_tracking/domain/entities/task.py
from dataclasses import dataclass

from src.shared_kernel.entity_base import EntityBase
from src.shared_kernel.vertex_id import TaskId
from src.work_tracking.domain.value_objects.work_item_status import WorkItemStatus


@dataclass
class Task(EntityBase):
    """Task entity with audit tracking and versioning.

    Invariants:
    - Title cannot be empty
    - Status transitions follow state machine
    """

    title: str
    status: WorkItemStatus = WorkItemStatus.PENDING
    description: str = ""

    @classmethod
    def create(
        cls,
        title: str,
        description: str = "",
        created_by: str = "System",
    ) -> Task:
        """Factory method to create new task."""
        if not title.strip():
            raise ValueError("Title cannot be empty")

        return cls(
            _id=TaskId.generate(),
            title=title,
            description=description,
            _created_by=created_by,
            _updated_by=created_by,
        )

    def update_title(self, new_title: str, by: str = "System") -> None:
        """Update task title."""
        if not new_title.strip():
            raise ValueError("Title cannot be empty")

        self.title = new_title
        self._mark_updated(by)

    def start(self, by: str = "System") -> None:
        """Transition to in_progress status."""
        self.status.validate_transition(WorkItemStatus.IN_PROGRESS)
        self.status = WorkItemStatus.IN_PROGRESS
        self._mark_updated(by)
```

---

## Composition vs Inheritance

EntityBase uses composition of concerns rather than deep inheritance:

```
EntityBase
    ├── Identity (VertexId)
    ├── Auditing (IAuditable)
    └── Versioning (IVersioned)
```

This is preferred over:

```
# AVOID: Deep inheritance hierarchy
class Entity(ABC):
    pass

class AuditableEntity(Entity):
    pass

class VersionedAuditableEntity(AuditableEntity):
    pass

class Task(VersionedAuditableEntity):
    pass
```

> **Jerry Decision**: Use flat composition in EntityBase rather than inheritance chains. This keeps the hierarchy shallow and each concern clearly separated.

---

## Protocol Compliance

EntityBase satisfies multiple protocols:

```python
from typing import runtime_checkable, Protocol

@runtime_checkable
class IAuditable(Protocol):
    created_by: str
    created_at: datetime
    updated_by: str
    updated_at: datetime

@runtime_checkable
class IVersioned(Protocol):
    version: int
    def get_expected_version(self) -> int: ...

# EntityBase satisfies both protocols
entity = Task.create(title="Example")
assert isinstance(entity, IAuditable)  # True
assert isinstance(entity, IVersioned)  # True
```

---

## Optimistic Concurrency

The version field enables optimistic concurrency control:

```python
# In repository adapter
def save(self, entity: EntityBase) -> None:
    """Save entity with optimistic concurrency check."""
    expected_version = entity.get_expected_version() - 1

    # Check version in database
    current = self._store.get(entity.id)
    if current and current.version != expected_version:
        raise ConcurrencyError(
            f"Entity {entity.id} was modified by another process. "
            f"Expected version {expected_version}, found {current.version}"
        )

    self._store.save(entity)
```

---

## Audit Trail

EntityBase automatically tracks who modified an entity and when:

```python
task = Task.create(title="Research", created_by="user-123")
print(task.created_by)  # "user-123"
print(task.created_at)  # 2026-01-11T10:00:00Z

task.update_title("Research API", by="user-456")
print(task.updated_by)  # "user-456"
print(task.updated_at)  # 2026-01-11T10:05:00Z
print(task.version)     # 1
```

---

## When to Use EntityBase vs AggregateRoot

| Use Case | Base Class |
|----------|------------|
| Root entity with event sourcing | `AggregateRoot` (PAT-ENT-003) |
| Child entity within aggregate | `EntityBase` |
| Standalone entity without events | `EntityBase` |
| Graph vertex | `EntityBase` + `VertexId` |

---

## Testing Pattern

```python
def test_task_tracks_audit_metadata_when_updated():
    """Entity tracks who and when modifications occur."""
    # Arrange
    task = Task.create(title="Original", created_by="creator")
    original_created_at = task.created_at

    # Act
    task.update_title("Updated", by="modifier")

    # Assert
    assert task.created_by == "creator"
    assert task.created_at == original_created_at  # Unchanged
    assert task.updated_by == "modifier"
    assert task.updated_at > original_created_at
    assert task.version == 1


def test_task_version_increments_on_each_update():
    """Version increments with each modification."""
    task = Task.create(title="Test")
    assert task.version == 0

    task.update_title("Updated 1")
    assert task.version == 1

    task.update_title("Updated 2")
    assert task.version == 2
```

---

## References

- **Eric Evans**: Domain-Driven Design (2003), Chapter 5 - Entities
- **Vaughn Vernon**: Implementing DDD (2013), Entity Identity
- **Design Canon**: Section 5.3 - Entity Patterns
- **Related Patterns**: PAT-ID-001 (VertexId), PAT-ENT-001 (IAuditable), PAT-ENT-002 (IVersioned)
