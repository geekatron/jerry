# PAT-EVT-001: DomainEvent Pattern

> **Status**: MANDATORY
> **Category**: Event Pattern
> **Location**: `src/shared_kernel/domain_event.py`

---

## Overview

DomainEvent is the base class for all domain events in Jerry. Domain events represent facts that have happened in the domain - they are immutable records of past occurrences.

---

## Industry Prior Art

| Source | Key Insight |
|--------|-------------|
| **Eric Evans** (DDD) | "Domain events represent something that happened that domain experts care about" |
| **Udi Dahan** | "Domain events are notifications of past occurrences" |
| **Greg Young** | "Events are facts - they happened and cannot be changed" |

---

## Jerry Implementation

```python
# File: src/shared_kernel/domain_event.py
from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, ClassVar
from uuid import uuid4


def _generate_event_id() -> str:
    """Generate unique event identifier."""
    return str(uuid4())


def _current_timestamp() -> datetime:
    """Return current UTC timestamp."""
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class DomainEvent(ABC):
    """Base class for all domain events.

    Domain events are:
    - Immutable (frozen dataclass)
    - Named in past tense (TaskCreated, not TaskCreate)
    - Self-descriptive (contain all data needed to understand what happened)
    - Timestamped (when the event occurred)

    Usage:
        @dataclass(frozen=True)
        class TaskCreated(DomainEvent):
            title: str
            priority: str

    References:
        - PAT-AGG-002: Event Collection pattern
        - PAT-EVT-004: Event Store port
    """

    aggregate_id: str
    aggregate_type: str
    event_id: str = field(default_factory=_generate_event_id)
    timestamp: datetime = field(default_factory=_current_timestamp)
    version: int = 1

    def to_dict(self) -> dict[str, Any]:
        """Serialize event to dictionary.

        Used for persistence and messaging.
        """
        return {
            "event_type": self.__class__.__name__,
            "event_id": self.event_id,
            "aggregate_id": self.aggregate_id,
            "aggregate_type": self.aggregate_type,
            "version": self.version,
            "timestamp": self.timestamp.isoformat(),
            **self._payload(),
        }

    def _payload(self) -> dict[str, Any]:
        """Return event-specific payload data.

        Override in subclasses to include additional fields.
        """
        return {}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DomainEvent:
        """Deserialize event from dictionary.

        Must be implemented by subclasses for polymorphic deserialization.
        """
        raise NotImplementedError(
            f"{cls.__name__} must implement from_dict for deserialization"
        )
```

---

## Event Naming Convention

| Correct | Wrong | Why |
|---------|-------|-----|
| `TaskCreated` | `TaskCreate` | Events are past tense |
| `StatusChanged` | `ChangeStatus` | Events are nouns, not verbs |
| `WorkItemCompleted` | `WorkItemWasCompleted` | Avoid "Was" prefix |
| `PriorityUpdated` | `UpdatePriority` | Describes what happened |

---

## Concrete Event Example

```python
# File: src/work_tracking/domain/events/work_item_events.py
from dataclasses import dataclass
from typing import Any

from src.shared_kernel.domain_event import DomainEvent


@dataclass(frozen=True)
class WorkItemCreated(DomainEvent):
    """Event raised when a new work item is created."""

    title: str = ""
    work_type: str = "task"
    priority: str = "medium"
    description: str = ""
    parent_id: str | None = None

    def _payload(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "work_type": self.work_type,
            "priority": self.priority,
            "description": self.description,
            "parent_id": self.parent_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> WorkItemCreated:
        return cls(
            aggregate_id=data["aggregate_id"],
            aggregate_type=data["aggregate_type"],
            event_id=data["event_id"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            version=data.get("version", 1),
            title=data.get("title", ""),
            work_type=data.get("work_type", "task"),
            priority=data.get("priority", "medium"),
            description=data.get("description", ""),
            parent_id=data.get("parent_id"),
        )


@dataclass(frozen=True)
class StatusChanged(DomainEvent):
    """Event raised when work item status changes."""

    old_status: str = ""
    new_status: str = ""
    reason: str = ""

    def _payload(self) -> dict[str, Any]:
        return {
            "old_status": self.old_status,
            "new_status": self.new_status,
            "reason": self.reason,
        }
```

---

## Event Registry

For polymorphic deserialization:

```python
# File: src/shared_kernel/event_registry.py
from typing import Callable, Type

from src.shared_kernel.domain_event import DomainEvent


class EventRegistry:
    """Registry for event type deserialization.

    Enables reconstructing typed events from stored dictionaries.
    """

    _registry: dict[str, Type[DomainEvent]] = {}

    @classmethod
    def register(cls, event_class: Type[DomainEvent]) -> Type[DomainEvent]:
        """Register event class for deserialization."""
        cls._registry[event_class.__name__] = event_class
        return event_class

    @classmethod
    def deserialize(cls, data: dict[str, Any]) -> DomainEvent:
        """Deserialize event from dictionary."""
        event_type = data.get("event_type")
        if event_type not in cls._registry:
            raise UnknownEventTypeError(f"Unknown event type: {event_type}")

        event_class = cls._registry[event_type]
        return event_class.from_dict(data)


# Usage with decorator
@EventRegistry.register
@dataclass(frozen=True)
class TaskCreated(DomainEvent):
    title: str = ""
```

---

## Testing Pattern

```python
def test_domain_event_is_immutable():
    """Events cannot be modified after creation."""
    event = WorkItemCreated(
        aggregate_id="WORK-001",
        aggregate_type="WorkItem",
        title="Test Task",
    )

    with pytest.raises(FrozenInstanceError):
        event.title = "Changed Title"


def test_domain_event_serializes_to_dict():
    """Events can be serialized for persistence."""
    event = WorkItemCreated(
        aggregate_id="WORK-001",
        aggregate_type="WorkItem",
        title="Test Task",
        priority="high",
    )

    data = event.to_dict()

    assert data["event_type"] == "WorkItemCreated"
    assert data["aggregate_id"] == "WORK-001"
    assert data["title"] == "Test Task"
    assert data["priority"] == "high"


def test_domain_event_deserializes_from_dict():
    """Events can be reconstructed from stored data."""
    data = {
        "event_type": "WorkItemCreated",
        "event_id": "evt-123",
        "aggregate_id": "WORK-001",
        "aggregate_type": "WorkItem",
        "timestamp": "2026-01-11T10:00:00+00:00",
        "title": "Test Task",
    }

    event = WorkItemCreated.from_dict(data)

    assert event.aggregate_id == "WORK-001"
    assert event.title == "Test Task"
```

---

## Jerry-Specific Decisions

> **Jerry Decision**: Internal domain events use DomainEvent base class. CloudEvents format (PAT-EVT-002) is only used for external integration events.

> **Jerry Decision**: Events are named as `{Entity}{PastVerb}` - e.g., `WorkItemCreated`, `StatusChanged`. No "Was" prefix.

> **Jerry Decision**: All events include `event_id`, `timestamp`, and `version` for ordering and idempotency.

---

## References

- **Eric Evans**: Domain-Driven Design (2003), Domain Events
- **Udi Dahan**: [Domain Events – Salvation](https://udidahan.com/2009/06/14/domain-events-salvation/)
- **Martin Fowler**: [Domain Event](https://martinfowler.com/eaaDev/DomainEvent.html)
- **Design Canon**: Section 5.5 - Domain Events
- **Related Patterns**: PAT-AGG-002 (Event Collection), PAT-EVT-004 (IEventStore)
