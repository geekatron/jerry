# ADR-016: CloudEvents SDK Architecture (Hexagonal Separation)

> **Document ID**: PROJ-001-e-016-v1-adr-cloudevents-sdk
> **PS ID**: PROJ-001
> **Entry ID**: e-016-v1
> **Date**: 2026-01-10
> **Author**: Claude (Opus 4.5) with user guidance
> **Status**: ACCEPTED
> **Supersedes**: CloudEvents section of PROJ-001-e-013-v2-adr-shared-kernel.md (lines 191-345)
>
> **Sources**:
> - **Prior ADR**: `decisions/PROJ-001-e-013-v2-adr-shared-kernel.md`
> - **Canon**: `synthesis/PROJ-001-e-011-v1-jerry-design-canon.md` (PAT-EVT-001, PAT-EVT-002)
> - **CloudEvents Python SDK**: https://github.com/cloudevents/sdk-python
> - **CloudEvents Spec**: https://github.com/cloudevents/spec
> - **SDK Feature Matrix**: https://github.com/cloudevents/spec/blob/main/cloudevents/SDK.md

---

## L0: Executive Summary

### Problem

ADR-013-v2 specified implementing CloudEvents 1.0 envelopes in `shared_kernel` using stdlib-only code. While this preserves zero-dependency constraints, it:

1. **Conflates concerns**: CloudEvents is a **transport format**, not a domain concept
2. **Ignores infrastructure benefits**: Protocol bindings (HTTP, Kafka) require re-implementation
3. **Violates Hexagonal Architecture**: Transport concerns belong in infrastructure, not shared kernel

### Decision

**ACCEPT** a revised architecture that separates domain events from transport format:

| Layer | Component | Dependencies | Responsibility |
|-------|-----------|--------------|----------------|
| **Domain** | `JerryEvent` base class | stdlib only | Business intent expression |
| **Shared Kernel** | `DomainEvent` (existing) | stdlib only | Event identity, timestamps |
| **Infrastructure** | `CloudEventsAdapter` | `cloudevents` SDK | Transport serialization, protocol bindings |

### Key Insight

> "Domain events express **business intent** ('TaskCompleted'). CloudEvents express **interoperability** ('here's a standard envelope for any system to read'). These are different concerns that belong in different layers."

---

## Context

### What ADR-013-v2 Specified

Lines 191-345 of e-013-v2 defined a `CloudEventEnvelope` dataclass in `shared_kernel/cloud_events.py`:

```python
# FROM e-013-v2 (NOW SUPERSEDED)
@dataclass(frozen=True)
class CloudEventEnvelope:
    specversion: str = "1.0"
    type: str = ""
    source: str = ""
    id: str = ""
    # ... stdlib-only implementation
```

### Why This Is Problematic

1. **CloudEvents is a transport format**: The CNCF CloudEvents specification defines how to encode events for interoperability across systems. It's not a domain concept.

2. **Protocol bindings are non-trivial**: The CloudEvents spec defines bindings for:
   - HTTP (structured mode, binary mode, batched mode)
   - Kafka (structured mode, binary mode)
   - AMQP, MQTT, WebSockets

3. **SDK provides tested implementations**: The official CloudEvents Python SDK (v1.12.0) implements these bindings. Re-implementing them adds maintenance burden without benefit.

4. **Hexagonal Architecture principle**: Infrastructure concerns (external system integration) belong in the infrastructure layer, not shared kernel.

### Research Findings

#### CloudEvents Python SDK Capabilities

| Attribute | Value |
|-----------|-------|
| Package | `cloudevents` on PyPI |
| Version | 1.12.0 (June 2025), 2.0.0a1 pre-release (Dec 2025) |
| Python Support | 3.9, 3.10, 3.11, 3.12, 3.13 |
| Dependencies | Minimal (optional pydantic) |
| Maintenance | Active, CNCF-backed |
| Spec Versions | v1.0, v0.3 |

#### Protocol Binding Support (from SDK.md)

| Binding | Python SDK | Notes |
|---------|------------|-------|
| HTTP Binary | :heavy_check_mark: | `to_binary()` function |
| HTTP Structured | :heavy_check_mark: | `to_structured()` function |
| HTTP Batch | :x: | Not implemented |
| **Kafka Binary** | :heavy_check_mark: | Header-based attributes |
| **Kafka Structured** | :heavy_check_mark: | JSON in message value |
| AMQP | :x: | Not implemented (Java/C# only) |
| MQTT | :x: | Not implemented (JS only) |

**Key Finding**: The Python SDK supports **both HTTP and Kafka bindings** - exactly what Jerry needs for future ADO sync and event streaming.

---

## Decision

### Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           HEXAGONAL ARCHITECTURE                         │
└─────────────────────────────────────────────────────────────────────────┘

DOMAIN LAYER (stdlib only)
┌─────────────────────────────────────────────────────────────────────────┐
│  JerryEvent (base class)                                                 │
│    + event_type: str              # "task.completed.v1"                  │
│    + aggregate_id: str            # Business identifier                  │
│    + aggregate_type: str          # "Task", "Phase", etc.                │
│    + payload: dict[str, Any]      # Event-specific data                  │
│    + to_dict() -> dict            # Standard serialization               │
│                                                                          │
│  TaskCompleted(JerryEvent)        # Concrete domain event                │
│  PhaseStarted(JerryEvent)         # Concrete domain event                │
│  WorkItemCreated(JerryEvent)      # Concrete domain event                │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ translated by
                                    ▼
APPLICATION LAYER (ports)
┌─────────────────────────────────────────────────────────────────────────┐
│  IEventPublisher (port interface)                                        │
│    + publish(event: JerryEvent) -> None                                  │
│    + publish_batch(events: list[JerryEvent]) -> None                     │
│                                                                          │
│  IEventSubscriber (port interface)                                       │
│    + subscribe(event_type: str, handler: Callable) -> None               │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ implemented by
                                    ▼
INFRASTRUCTURE LAYER (external dependencies allowed)
┌─────────────────────────────────────────────────────────────────────────┐
│  CloudEventsAdapter                                                      │
│    + __init__(sdk: cloudevents)   # SDK injection                        │
│    + to_cloudevent(event: JerryEvent) -> CloudEvent                      │
│    + from_cloudevent(ce: CloudEvent) -> JerryEvent                       │
│                                                                          │
│  HttpEventPublisher : IEventPublisher                                    │
│    + uses CloudEventsAdapter + cloudevents.to_binary/to_structured       │
│                                                                          │
│  KafkaEventPublisher : IEventPublisher                                   │
│    + uses CloudEventsAdapter + cloudevents Kafka bindings                │
│                                                                          │
│  InMemoryEventPublisher : IEventPublisher                                │
│    + for testing, no CloudEvents needed                                  │
└─────────────────────────────────────────────────────────────────────────┘
```

### Translation Layer

The `CloudEventsAdapter` translates between domain events and CloudEvents format:

```python
# infrastructure/adapters/cloud_events_adapter.py
from __future__ import annotations

from cloudevents.http import CloudEvent
from cloudevents.conversion import to_binary, to_structured

from src.domain.events import JerryEvent


class CloudEventsAdapter:
    """Translates Jerry domain events to CloudEvents format.

    This adapter lives in the infrastructure layer and depends on the
    cloudevents SDK. Domain code never imports this directly.
    """

    SOURCE_PREFIX = "/jerry"
    SPEC_VERSION = "1.0"

    def to_cloudevent(self, event: JerryEvent) -> CloudEvent:
        """Convert a Jerry domain event to CloudEvents format.

        Args:
            event: The domain event to convert.

        Returns:
            CloudEvent object suitable for HTTP/Kafka transport.
        """
        attributes = {
            "specversion": self.SPEC_VERSION,
            "type": f"com.jerry.{event.event_type}",
            "source": f"{self.SOURCE_PREFIX}/{event.aggregate_type.lower()}s/{event.aggregate_id}",
            "id": event.event_id,
            "time": event.timestamp.isoformat() + "Z",
            "subject": event.aggregate_id,
            "datacontenttype": "application/json",
        }
        return CloudEvent(attributes, event.payload)

    def from_cloudevent(self, ce: CloudEvent) -> dict:
        """Parse CloudEvent back to domain event data.

        Args:
            ce: CloudEvent received from external system.

        Returns:
            Dictionary with event data for domain event reconstruction.
        """
        return {
            "event_type": ce["type"].replace("com.jerry.", ""),
            "aggregate_id": ce["subject"],
            "payload": ce.data,
            "event_id": ce["id"],
        }

    def to_http_binary(self, event: JerryEvent) -> tuple[dict, bytes]:
        """Serialize for HTTP binary content mode (headers + body)."""
        ce = self.to_cloudevent(event)
        return to_binary(ce)

    def to_http_structured(self, event: JerryEvent) -> tuple[dict, bytes]:
        """Serialize for HTTP structured content mode (JSON body)."""
        ce = self.to_cloudevent(event)
        return to_structured(ce)
```

### What Changes from e-013-v2

| Aspect | e-013-v2 (Superseded) | e-016 (New) |
|--------|----------------------|-------------|
| CloudEvents location | `shared_kernel/cloud_events.py` | `infrastructure/adapters/` |
| Dependencies | stdlib only | `cloudevents` SDK |
| Protocol bindings | Must implement ourselves | SDK provides |
| Domain events | CloudEventEnvelope | JerryEvent (stdlib) |
| Translation | In shared kernel | At infrastructure boundary |

### What Stays the Same

- **DomainEvent base class** in `shared_kernel/domain_event.py` - unchanged
- **Canon patterns** PAT-EVT-001 and PAT-EVT-002 - still valid (layer-agnostic)
- **Event types** (TaskCompleted, etc.) - still domain objects

---

## Consequences

### Positive

1. **Clean separation of concerns**: Domain events express business intent, CloudEvents handle transport
2. **Free protocol bindings**: HTTP and Kafka support without implementation effort
3. **Future-proofing**: CloudEvents 2.0 changes handled by SDK updates + translation shim
4. **Tested code**: SDK is CNCF-maintained with broad adoption
5. **Hexagonal compliance**: Infrastructure concerns stay in infrastructure layer

### Negative

1. **External dependency in infrastructure**: `cloudevents` package required
2. **Translation overhead**: Extra object creation at infrastructure boundary
3. **Learning curve**: Developers must understand the boundary

### Neutral

1. **Domain stays clean**: No changes to existing domain event patterns
2. **Canon unchanged**: PAT-EVT-001/002 remain valid as layer-agnostic patterns

---

## Implementation Plan

### Phase 1: Domain Event Base (Week 1)

Update `JerryEvent` base class in domain layer:

```python
# src/domain/events/jerry_event.py
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class JerryEvent:
    """Base class for all Jerry domain events.

    Domain events capture business-meaningful occurrences. They are
    serialized to CloudEvents format at the infrastructure boundary
    for external system interoperability.

    Attributes:
        event_type: Event type in dot notation (e.g., "task.completed.v1")
        aggregate_id: Identifier of the aggregate that emitted this event
        aggregate_type: Type name of the aggregate (e.g., "Task")
        payload: Event-specific data dictionary
        event_id: Unique event identifier (auto-generated)
        timestamp: When the event occurred (auto-generated)
    """

    event_type: str
    aggregate_id: str
    aggregate_type: str
    payload: dict[str, Any] = field(default_factory=dict)
    event_id: str = field(default_factory=lambda: f"EVT-{uuid4()}")
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary for persistence."""
        return {
            "event_type": self.event_type,
            "aggregate_id": self.aggregate_id,
            "aggregate_type": self.aggregate_type,
            "payload": self.payload,
            "event_id": self.event_id,
            "timestamp": self.timestamp.isoformat(),
        }
```

### Phase 2: CloudEvents Adapter (Week 2)

Create adapter in infrastructure layer:

```
src/infrastructure/adapters/
├── __init__.py
└── cloud_events_adapter.py  # CloudEventsAdapter class
```

### Phase 3: Publisher Implementations (Week 3)

Create concrete publishers:

```
src/infrastructure/publishers/
├── __init__.py
├── http_event_publisher.py     # HttpEventPublisher : IEventPublisher
├── kafka_event_publisher.py    # KafkaEventPublisher : IEventPublisher
└── in_memory_publisher.py      # InMemoryEventPublisher (testing)
```

### Phase 4: Integration Tests (Week 4)

Test the full translation and publishing flow:

```
tests/infrastructure/integration/
├── test_cloudevents_adapter.py
├── test_http_publisher.py
└── test_kafka_publisher.py
```

---

## Dependencies

### New Package Required

Add to `pyproject.toml`:

```toml
[project.dependencies]
cloudevents = "^1.12.0"
```

### Compatibility

- Python 3.11+ (Jerry requirement)
- CloudEvents SDK supports 3.9-3.13 (compatible)

---

## References

- [CloudEvents Python SDK](https://github.com/cloudevents/sdk-python) - Official CNCF SDK
- [CloudEvents Specification](https://github.com/cloudevents/spec) - CNCF CloudEvents 1.0
- [SDK Feature Matrix](https://github.com/cloudevents/spec/blob/main/cloudevents/SDK.md) - Language support
- [Kafka Protocol Binding](https://github.com/cloudevents/spec/blob/main/cloudevents/bindings/kafka-protocol-binding.md)
- [HTTP Protocol Binding](https://github.com/cloudevents/spec/blob/main/cloudevents/bindings/http-protocol-binding.md)

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v1 | 2026-01-10 | Claude | Initial version, supersedes CloudEvents section of e-013-v2 |
