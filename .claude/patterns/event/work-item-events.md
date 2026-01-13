# PAT-EVT-003: WorkItem Domain Events

> **Status**: MANDATORY
> **Category**: Event Pattern
> **Location**: `src/work_tracking/domain/events/`

---

## Overview

WorkItem domain events capture all state changes to work items. Each event represents a specific business action that occurred, enabling event sourcing and audit trails.

---

## Industry Prior Art

| Source | Key Insight |
|--------|-------------|
| **Greg Young** | "Events are facts - they happened, they cannot be changed" |
| **Martin Fowler** | "Events capture the intent of the user's action" |
| **Vaughn Vernon** | "Domain events should be named in past tense, reflecting what happened" |

---

## Jerry Implementation

### Event Definitions

```python
# File: src/work_tracking/domain/events/work_item_events.py
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from src.shared_kernel.domain_event import DomainEvent


def _current_utc() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True, slots=True)
class WorkItemCreated(DomainEvent):
    """Raised when a new work item is created.

    This is the genesis event - every work item stream starts with this.
    """

    work_item_id: str
    title: str
    work_type: str
    priority: str
    description: str = ""
    parent_id: str | None = None

    @property
    def aggregate_id(self) -> str:
        return self.work_item_id

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": "WorkItemCreated",
            "work_item_id": self.work_item_id,
            "title": self.title,
            "work_type": self.work_type,
            "priority": self.priority,
            "description": self.description,
            "parent_id": self.parent_id,
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> WorkItemCreated:
        return cls(
            work_item_id=data["work_item_id"],
            title=data["title"],
            work_type=data["work_type"],
            priority=data["priority"],
            description=data.get("description", ""),
            parent_id=data.get("parent_id"),
            timestamp=datetime.fromisoformat(data["timestamp"]),
        )


@dataclass(frozen=True, slots=True)
class WorkItemStarted(DomainEvent):
    """Raised when work begins on an item.

    Transitions: PENDING → IN_PROGRESS
    """

    work_item_id: str
    started_at: datetime = field(default_factory=_current_utc)

    @property
    def aggregate_id(self) -> str:
        return self.work_item_id

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": "WorkItemStarted",
            "work_item_id": self.work_item_id,
            "started_at": self.started_at.isoformat(),
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> WorkItemStarted:
        return cls(
            work_item_id=data["work_item_id"],
            started_at=datetime.fromisoformat(data["started_at"]),
            timestamp=datetime.fromisoformat(data["timestamp"]),
        )


@dataclass(frozen=True, slots=True)
class WorkItemBlocked(DomainEvent):
    """Raised when work item is blocked.

    Transitions: IN_PROGRESS → BLOCKED
    """

    work_item_id: str
    blocked_by: str  # ID of blocking item or external reference
    reason: str
    blocked_at: datetime = field(default_factory=_current_utc)

    @property
    def aggregate_id(self) -> str:
        return self.work_item_id

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": "WorkItemBlocked",
            "work_item_id": self.work_item_id,
            "blocked_by": self.blocked_by,
            "reason": self.reason,
            "blocked_at": self.blocked_at.isoformat(),
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> WorkItemBlocked:
        return cls(
            work_item_id=data["work_item_id"],
            blocked_by=data["blocked_by"],
            reason=data["reason"],
            blocked_at=datetime.fromisoformat(data["blocked_at"]),
            timestamp=datetime.fromisoformat(data["timestamp"]),
        )


@dataclass(frozen=True, slots=True)
class WorkItemUnblocked(DomainEvent):
    """Raised when a block is resolved.

    Transitions: BLOCKED → IN_PROGRESS
    """

    work_item_id: str
    resolution: str
    unblocked_at: datetime = field(default_factory=_current_utc)

    @property
    def aggregate_id(self) -> str:
        return self.work_item_id

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": "WorkItemUnblocked",
            "work_item_id": self.work_item_id,
            "resolution": self.resolution,
            "unblocked_at": self.unblocked_at.isoformat(),
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> WorkItemUnblocked:
        return cls(
            work_item_id=data["work_item_id"],
            resolution=data["resolution"],
            unblocked_at=datetime.fromisoformat(data["unblocked_at"]),
            timestamp=datetime.fromisoformat(data["timestamp"]),
        )


@dataclass(frozen=True, slots=True)
class WorkItemCompleted(DomainEvent):
    """Raised when work item is completed.

    Transitions: IN_PROGRESS → DONE
    """

    work_item_id: str
    quality_passed: bool
    completed_at: datetime = field(default_factory=_current_utc)

    @property
    def aggregate_id(self) -> str:
        return self.work_item_id

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": "WorkItemCompleted",
            "work_item_id": self.work_item_id,
            "quality_passed": self.quality_passed,
            "completed_at": self.completed_at.isoformat(),
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> WorkItemCompleted:
        return cls(
            work_item_id=data["work_item_id"],
            quality_passed=data["quality_passed"],
            completed_at=datetime.fromisoformat(data["completed_at"]),
            timestamp=datetime.fromisoformat(data["timestamp"]),
        )


@dataclass(frozen=True, slots=True)
class WorkItemCancelled(DomainEvent):
    """Raised when work item is cancelled.

    Transitions: PENDING|IN_PROGRESS|BLOCKED → CANCELLED
    """

    work_item_id: str
    reason: str
    cancelled_at: datetime = field(default_factory=_current_utc)

    @property
    def aggregate_id(self) -> str:
        return self.work_item_id

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": "WorkItemCancelled",
            "work_item_id": self.work_item_id,
            "reason": self.reason,
            "cancelled_at": self.cancelled_at.isoformat(),
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> WorkItemCancelled:
        return cls(
            work_item_id=data["work_item_id"],
            reason=data["reason"],
            cancelled_at=datetime.fromisoformat(data["cancelled_at"]),
            timestamp=datetime.fromisoformat(data["timestamp"]),
        )


@dataclass(frozen=True, slots=True)
class WorkItemPriorityChanged(DomainEvent):
    """Raised when priority is updated."""

    work_item_id: str
    old_priority: str
    new_priority: str

    @property
    def aggregate_id(self) -> str:
        return self.work_item_id

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": "WorkItemPriorityChanged",
            "work_item_id": self.work_item_id,
            "old_priority": self.old_priority,
            "new_priority": self.new_priority,
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> WorkItemPriorityChanged:
        return cls(
            work_item_id=data["work_item_id"],
            old_priority=data["old_priority"],
            new_priority=data["new_priority"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
        )


@dataclass(frozen=True, slots=True)
class SubtaskAdded(DomainEvent):
    """Raised when a subtask is added to a work item."""

    work_item_id: str
    subtask_id: str
    subtask_title: str

    @property
    def aggregate_id(self) -> str:
        return self.work_item_id

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": "SubtaskAdded",
            "work_item_id": self.work_item_id,
            "subtask_id": self.subtask_id,
            "subtask_title": self.subtask_title,
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SubtaskAdded:
        return cls(
            work_item_id=data["work_item_id"],
            subtask_id=data["subtask_id"],
            subtask_title=data["subtask_title"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
        )


@dataclass(frozen=True, slots=True)
class DependencyAdded(DomainEvent):
    """Raised when a dependency is added."""

    work_item_id: str
    depends_on_id: str

    @property
    def aggregate_id(self) -> str:
        return self.work_item_id

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": "DependencyAdded",
            "work_item_id": self.work_item_id,
            "depends_on_id": self.depends_on_id,
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DependencyAdded:
        return cls(
            work_item_id=data["work_item_id"],
            depends_on_id=data["depends_on_id"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
        )
```

---

## Event Registry

```python
# File: src/work_tracking/domain/events/event_registry.py
from typing import Any

from src.work_tracking.domain.events.work_item_events import (
    DependencyAdded,
    SubtaskAdded,
    WorkItemBlocked,
    WorkItemCancelled,
    WorkItemCompleted,
    WorkItemCreated,
    WorkItemPriorityChanged,
    WorkItemStarted,
    WorkItemUnblocked,
)


class EventRegistry:
    """Registry for deserializing events by type name."""

    _event_types = {
        "WorkItemCreated": WorkItemCreated,
        "WorkItemStarted": WorkItemStarted,
        "WorkItemBlocked": WorkItemBlocked,
        "WorkItemUnblocked": WorkItemUnblocked,
        "WorkItemCompleted": WorkItemCompleted,
        "WorkItemCancelled": WorkItemCancelled,
        "WorkItemPriorityChanged": WorkItemPriorityChanged,
        "SubtaskAdded": SubtaskAdded,
        "DependencyAdded": DependencyAdded,
    }

    @classmethod
    def deserialize(cls, data: dict[str, Any]) -> Any:
        """Deserialize event from dictionary."""
        event_type = data.get("event_type")
        if event_type not in cls._event_types:
            raise ValueError(f"Unknown event type: {event_type}")

        event_class = cls._event_types[event_type]
        return event_class.from_dict(data)

    @classmethod
    def register(cls, event_type: str, event_class: type) -> None:
        """Register a new event type."""
        cls._event_types[event_type] = event_class
```

---

## State Transition Diagram

```
                                    WorkItemCreated
                                          │
                                          ▼
                                    ┌──────────┐
                                    │ PENDING  │
                                    └────┬─────┘
                                         │ WorkItemStarted
                                         ▼
                               ┌─────────────────┐
                      ┌───────►│  IN_PROGRESS    │◄───────┐
                      │        └───────┬─────────┘        │
                      │                │                  │
          WorkItemUnblocked            │         WorkItemBlocked
                      │                │                  │
                      │         ┌──────┴──────┐           │
                      │         │             │           │
                      │         ▼             ▼           │
                ┌─────┴─────┐              ┌──────────┐   │
                │  BLOCKED  │◄─────────────│  (can    │───┘
                └───────────┘              │ complete)│
                                           └────┬─────┘
                                                │ WorkItemCompleted
                                                ▼
                                          ┌──────────┐
                                          │   DONE   │
                                          └──────────┘

                    ─── WorkItemCancelled ───►  CANCELLED
                    (from PENDING, IN_PROGRESS, or BLOCKED)
```

---

## Event Application in Aggregate

```python
# In WorkItem aggregate
class WorkItem(AggregateRoot):
    def _apply(self, event: DomainEvent) -> None:
        """Apply event to update state."""
        match event:
            case WorkItemCreated():
                self._id = event.work_item_id
                self._title = event.title
                self._work_type = event.work_type
                self._priority = Priority(event.priority)
                self._status = Status.PENDING
                self._created_at = event.timestamp

            case WorkItemStarted():
                self._status = Status.IN_PROGRESS
                self._started_at = event.started_at

            case WorkItemBlocked():
                self._status = Status.BLOCKED
                self._blocked_by = event.blocked_by
                self._block_reason = event.reason

            case WorkItemUnblocked():
                self._status = Status.IN_PROGRESS
                self._blocked_by = None
                self._block_reason = None

            case WorkItemCompleted():
                self._status = Status.DONE
                self._completed_at = event.completed_at
                self._quality_passed = event.quality_passed

            case WorkItemCancelled():
                self._status = Status.CANCELLED
                self._cancelled_at = event.cancelled_at
                self._cancel_reason = event.reason

            case WorkItemPriorityChanged():
                self._priority = Priority(event.new_priority)

            case SubtaskAdded():
                self._subtask_ids.append(event.subtask_id)

            case DependencyAdded():
                self._dependency_ids.append(event.depends_on_id)
```

---

## Testing Pattern

```python
def test_work_item_created_event_captures_all_data():
    """WorkItemCreated captures creation details."""
    event = WorkItemCreated(
        work_item_id="WORK-001",
        title="Implement feature",
        work_type="task",
        priority="high",
        description="Feature description",
        parent_id="EPIC-001",
    )

    assert event.work_item_id == "WORK-001"
    assert event.title == "Implement feature"
    assert event.parent_id == "EPIC-001"
    assert event.aggregate_id == "WORK-001"


def test_event_serialization_roundtrip():
    """Events serialize and deserialize correctly."""
    original = WorkItemCompleted(
        work_item_id="WORK-001",
        quality_passed=True,
    )

    data = original.to_dict()
    restored = WorkItemCompleted.from_dict(data)

    assert restored.work_item_id == original.work_item_id
    assert restored.quality_passed == original.quality_passed


def test_aggregate_applies_events_correctly():
    """Aggregate state updated by applying events."""
    events = [
        WorkItemCreated(
            work_item_id="WORK-001",
            title="Test Task",
            work_type="task",
            priority="medium",
        ),
        WorkItemStarted(work_item_id="WORK-001"),
        WorkItemCompleted(work_item_id="WORK-001", quality_passed=True),
    ]

    work_item = WorkItem.load_from_history(events)

    assert work_item.id == "WORK-001"
    assert work_item.status == Status.DONE
```

---

## Jerry-Specific Decisions

> **Jerry Decision**: Each event class lives in work_item_events.py for cohesion. Separate files only if event count exceeds 15.

> **Jerry Decision**: Events include both `timestamp` (inherited from DomainEvent) and action-specific timestamps (e.g., `completed_at`).

> **Jerry Decision**: Event Registry provides centralized deserialization. All events must be registered.

---

## References

- **Greg Young**: [Event Sourcing](https://cqrs.files.wordpress.com/2010/11/cqrs_documents.pdf)
- **Martin Fowler**: [Domain Event](https://martinfowler.com/eaaDev/DomainEvent.html)
- **Design Canon**: Section 5.3 - Domain Events
- **Related Patterns**: PAT-EVT-001 (DomainEvent), PAT-AGG-001 (WorkItem Aggregate)
