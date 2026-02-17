# PAT-EVT-002: CloudEvents Integration Pattern

> **Status**: RECOMMENDED
> **Category**: Event Pattern
> **Location**: `src/shared_kernel/integration_events/`

---

## Overview

CloudEvents is a CNCF specification for describing event data in a common way. Jerry uses CloudEvents format for integration events that cross bounded context or system boundaries, while internal domain events remain lightweight.

---

## Industry Prior Art

| Source | Key Insight |
|--------|-------------|
| **CNCF CloudEvents** | "A specification for describing event data in common formats" |
| **Microsoft Azure** | "CloudEvents provides interoperability across services, platforms, and systems" |
| **Knative** | "CloudEvents as the standard for event-driven architectures" |

---

## Jerry Implementation

### CloudEvent Structure

```python
# File: src/shared_kernel/integration_events/cloud_event.py
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4


def _current_utc() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True, slots=True)
class CloudEvent:
    """CloudEvents v1.0 compliant event.

    Used for integration events that cross system boundaries.
    Internal domain events use the lighter DomainEvent base.

    CloudEvents Spec: https://cloudevents.io/
    """

    # Required attributes (CloudEvents v1.0)
    specversion: str = "1.0"
    type: str = ""  # e.g., "jerry.work_tracking.task.completed"
    source: str = ""  # e.g., "/jerry/work-tracking"
    id: UUID = field(default_factory=uuid4)

    # Optional attributes
    subject: str | None = None  # e.g., "WORK-001"
    time: datetime = field(default_factory=_current_utc)
    datacontenttype: str = "application/json"

    # Data payload
    data: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to CloudEvents JSON format."""
        result = {
            "specversion": self.specversion,
            "type": self.type,
            "source": self.source,
            "id": str(self.id),
            "time": self.time.isoformat(),
            "datacontenttype": self.datacontenttype,
            "data": self.data,
        }
        if self.subject:
            result["subject"] = self.subject
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CloudEvent:
        """Deserialize from CloudEvents JSON format."""
        return cls(
            specversion=data.get("specversion", "1.0"),
            type=data["type"],
            source=data["source"],
            id=UUID(data["id"]),
            subject=data.get("subject"),
            time=datetime.fromisoformat(data["time"]),
            datacontenttype=data.get("datacontenttype", "application/json"),
            data=data.get("data", {}),
        )
```

---

## Event Type Naming

### Convention

```
jerry.{bounded_context}.{aggregate}.{event_verb}
```

### Examples

| Event | Type String |
|-------|-------------|
| Task created | `jerry.work_tracking.task.created` |
| Task completed | `jerry.work_tracking.task.completed` |
| Project activated | `jerry.session_management.project.activated` |
| Phase started | `jerry.work_tracking.phase.started` |

### Source Naming

```
/jerry/{bounded-context}
```

| Context | Source |
|---------|--------|
| Work Tracking | `/jerry/work-tracking` |
| Session Management | `/jerry/session-management` |
| Problem Solving | `/jerry/problem-solving` |

---

## Domain Event to CloudEvent Conversion

```python
# File: src/shared_kernel/integration_events/event_converter.py
from src.shared_kernel.domain_event import DomainEvent
from src.shared_kernel.integration_events.cloud_event import CloudEvent


class DomainToCloudEventConverter:
    """Converts domain events to CloudEvents for external publishing."""

    def __init__(self, source: str, context: str) -> None:
        self._source = source
        self._context = context

    def convert(self, domain_event: DomainEvent) -> CloudEvent:
        """Convert a domain event to CloudEvent format."""
        event_type = self._build_type(domain_event)

        return CloudEvent(
            type=event_type,
            source=self._source,
            subject=domain_event.aggregate_id,
            time=domain_event.timestamp,
            data=domain_event.to_dict(),
        )

    def _build_type(self, event: DomainEvent) -> str:
        """Build CloudEvent type from domain event class name.

        TaskCompleted -> jerry.work_tracking.task.completed
        """
        class_name = type(event).__name__

        # Extract aggregate and verb from class name
        # e.g., TaskCompleted -> task, completed
        import re
        parts = re.findall(r'[A-Z][a-z]+', class_name)

        if len(parts) >= 2:
            aggregate = parts[0].lower()
            verb = parts[-1].lower()
            return f"jerry.{self._context}.{aggregate}.{verb}"

        return f"jerry.{self._context}.{class_name.lower()}"


# Usage
converter = DomainToCloudEventConverter(
    source="/jerry/work-tracking",
    context="work_tracking",
)
cloud_event = converter.convert(TaskCompleted(task_id="WORK-001"))
```

---

## Integration Event Publisher

```python
# File: src/application/ports/secondary/iintegration_event_publisher.py
from typing import Protocol

from src.shared_kernel.integration_events.cloud_event import CloudEvent


class IIntegrationEventPublisher(Protocol):
    """Port for publishing integration events."""

    def publish(self, event: CloudEvent) -> None:
        """Publish an integration event.

        Args:
            event: CloudEvent to publish
        """
        ...

    def publish_batch(self, events: list[CloudEvent]) -> None:
        """Publish multiple integration events atomically."""
        ...
```

---

## When to Use CloudEvents vs Domain Events

| Aspect | Domain Events | CloudEvents |
|--------|---------------|-------------|
| Scope | Within bounded context | Across contexts/systems |
| Format | Lightweight, Jerry-specific | CloudEvents v1.0 spec |
| Consumers | Same context handlers | External systems, other BCs |
| Persistence | Event Store | Integration bus/queue |
| Serialization | to_dict/from_dict | CloudEvents JSON format |

### Decision Flow

```
                    ┌─────────────────────────────────┐
                    │ Does event cross BC boundary?   │
                    └───────────────┬─────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
              Yes (External)                  No (Internal)
                    │                               │
                    ▼                               ▼
            ┌───────────────┐              ┌───────────────┐
            │  CloudEvent   │              │  DomainEvent  │
            └───────────────┘              └───────────────┘
```

---

## Testing Pattern

```python
def test_cloud_event_has_required_attributes():
    """CloudEvent has all required fields per spec."""
    event = CloudEvent(
        type="jerry.work_tracking.task.created",
        source="/jerry/work-tracking",
        data={"task_id": "WORK-001"},
    )

    assert event.specversion == "1.0"
    assert event.type == "jerry.work_tracking.task.created"
    assert event.source == "/jerry/work-tracking"
    assert event.id is not None


def test_cloud_event_serialization_roundtrip():
    """CloudEvent serializes and deserializes correctly."""
    original = CloudEvent(
        type="jerry.work_tracking.task.completed",
        source="/jerry/work-tracking",
        subject="WORK-001",
        data={"completed_at": "2026-01-11T10:00:00Z"},
    )

    serialized = original.to_dict()
    restored = CloudEvent.from_dict(serialized)

    assert restored.type == original.type
    assert restored.source == original.source
    assert restored.subject == original.subject
    assert restored.data == original.data


def test_domain_to_cloud_event_conversion():
    """Domain events convert to CloudEvents correctly."""
    domain_event = TaskCompleted(
        task_id="WORK-001",
        completed_at=datetime.now(timezone.utc),
    )

    converter = DomainToCloudEventConverter(
        source="/jerry/work-tracking",
        context="work_tracking",
    )
    cloud_event = converter.convert(domain_event)

    assert cloud_event.type == "jerry.work_tracking.task.completed"
    assert cloud_event.source == "/jerry/work-tracking"
    assert cloud_event.subject == "WORK-001"
```

---

## Jerry-Specific Decisions

> **Jerry Decision**: Domain events remain lightweight. CloudEvents are used ONLY for cross-boundary integration.

> **Jerry Decision**: Event type follows `jerry.{context}.{aggregate}.{verb}` pattern for consistent routing.

> **Jerry Decision**: DomainToCloudEventConverter handles the translation layer, keeping domain events pure.

---

## Anti-Patterns

### 1. Using CloudEvents for Internal Events

```python
# WRONG: CloudEvents for internal use (overhead)
class TaskRepository:
    def save(self, task: Task) -> None:
        cloud_event = CloudEvent(type="...", source="...", data=...)
        self._event_store.append(cloud_event)

# CORRECT: Domain events internally, convert at boundary
class TaskRepository:
    def save(self, task: Task) -> None:
        domain_events = task.collect_events()
        self._event_store.append(stream_id, domain_events)
```

### 2. Embedding Business Logic in Event Type

```python
# WRONG: Business logic in type
type = "jerry.work_tracking.task.completed_with_high_quality"

# CORRECT: Business data in payload
type = "jerry.work_tracking.task.completed"
data = {"quality_score": "high"}
```

---

## References

- **CNCF CloudEvents**: [Specification](https://cloudevents.io/)
- **CloudEvents JSON Format**: [Spec](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/formats/json-format.md)
- **Design Canon**: Section 5.4 - Integration Events
- **Related Patterns**: PAT-EVT-001 (DomainEvent), PAT-ARCH-003 (Bounded Contexts)
