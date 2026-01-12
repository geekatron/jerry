# Event Sourcing Infrastructure: 5W1H Analysis

**ID**: IMPL-ES-5W1H
**Date**: 2026-01-09
**Author**: Claude (Distinguished Systems Engineer)
**Status**: RESEARCH COMPLETE

---

## Executive Summary

Full Event Sourcing with snapshot support requires implementing:
1. **IEventStore** - Append-only event persistence with version control
2. **ISnapshotStore** - Periodic state snapshots to optimize replay
3. **AggregateRoot** - Base class with event sourcing lifecycle
4. **TOON Serialization** - Token-efficient format for LLM interfaces

---

## 1. WHAT: Components to Implement

### 1.1 IEventStore Port

```python
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Sequence

T = TypeVar('T', bound='DomainEvent')

class IEventStore(ABC, Generic[T]):
    """Port for event persistence (Secondary Adapter pattern)."""

    @abstractmethod
    def append(self, stream_id: str, events: Sequence[T], expected_version: int) -> None:
        """Append events with optimistic concurrency."""

    @abstractmethod
    def read(self, stream_id: str, from_version: int = 0) -> Sequence[T]:
        """Read events from stream starting at version."""

    @abstractmethod
    def get_version(self, stream_id: str) -> int:
        """Get current version of stream."""
```

### 1.2 ISnapshotStore Port

```python
class ISnapshotStore(ABC):
    """Port for aggregate state snapshots."""

    @abstractmethod
    def save(self, stream_id: str, snapshot: Snapshot, version: int) -> None:
        """Save snapshot at specific version."""

    @abstractmethod
    def get_latest(self, stream_id: str) -> tuple[Snapshot, int] | None:
        """Get latest snapshot and its version."""
```

### 1.3 AggregateRoot Base Class

```python
@dataclass
class AggregateRoot(ABC):
    """Base class for event-sourced aggregates."""

    id: str
    version: int = 0
    _pending_events: list[DomainEvent] = field(default_factory=list)

    def _raise_event(self, event: DomainEvent) -> None:
        """Record and apply event."""
        self._pending_events.append(event)
        self._apply(event)
        self.version += 1

    @abstractmethod
    def _apply(self, event: DomainEvent) -> None:
        """Apply event to update state (implement in subclass)."""

    @classmethod
    def load_from_history(cls, events: Sequence[DomainEvent]) -> Self:
        """Reconstruct aggregate from event stream."""

    @classmethod
    def load_from_snapshot(cls, snapshot: Snapshot, events: Sequence[DomainEvent]) -> Self:
        """Reconstruct from snapshot + subsequent events."""
```

### 1.4 TOON Serialization (for LLM Interface)

```python
class ToonSerializer:
    """Token-Oriented Object Notation for LLM context efficiency."""

    def to_toon(self, events: list[DomainEvent]) -> str:
        """Convert events to TOON format (30-60% token savings)."""

    def from_toon(self, toon_str: str) -> list[dict]:
        """Parse TOON back to dictionaries."""
```

---

## 2. WHY: Justification

### 2.1 Event Sourcing Benefits

| Benefit | Description | Reference |
|---------|-------------|-----------|
| Audit Trail | Complete history of all state changes | [Fowler ES](https://martinfowler.com/eaaDev/EventSourcing.html) |
| Time Travel | Reconstruct state at any point in time | [Microsoft ES Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing) |
| CQRS Ready | Natural fit for command/query separation | [microservices.io](https://microservices.io/patterns/data/event-sourcing.html) |
| Debug/Replay | Replay events to diagnose issues | ADR-009 |

### 2.2 Snapshot Benefits

| Benefit | Description | When to Apply |
|---------|-------------|---------------|
| Performance | Avoid replaying entire stream | Replay time > 100ms |
| Scalability | Bounded replay cost | Aggregates with many events |
| Memory | Limit memory during reconstruction | Large aggregate state |

**Industry Guidance**: "Snapshots are performance optimization, not foundation. Add when replay exceeds 100ms for hot aggregates." — [Domain Centric](https://domaincentric.net/blog/event-sourcing-snapshotting)

### 2.3 TOON Benefits for LLM Context

| Metric | JSON | TOON | Savings |
|--------|------|------|---------|
| Tokens | 100% | 60% | **40%** |
| Accuracy | 69.7% | 73.9% | **+4.2%** |
| Readability | Verbose | Compact | Better |

**Source**: [TOON Format](https://toonformat.dev/), [GitHub](https://github.com/toon-format/toon)

---

## 3. WHO: Stakeholders

| Role | Concern | Impact |
|------|---------|--------|
| Domain Layer | AggregateRoot base class | All aggregates inherit |
| Application Layer | Repository implementations | Uses IEventStore, ISnapshotStore |
| Infrastructure | Adapters (InMemory, SQLite) | Implements ports |
| Interface Layer | TOON serialization | Token efficiency for LLMs |

---

## 4. WHERE: Directory Structure

Following ADR-003 (Bounded Context First, One File Per Concept):

```
src/
├── shared_kernel/
│   ├── ports/
│   │   ├── __init__.py
│   │   ├── event_store.py       # IEventStore
│   │   └── snapshot_store.py    # ISnapshotStore
│   ├── aggregate_root.py        # AggregateRoot base
│   └── snapshot.py              # Snapshot value object
│
├── infrastructure/
│   ├── persistence/
│   │   ├── __init__.py
│   │   ├── in_memory_event_store.py
│   │   ├── in_memory_snapshot_store.py
│   │   ├── sqlite_event_store.py      # Phase 2
│   │   └── sqlite_snapshot_store.py   # Phase 2
│   └── serialization/
│       ├── __init__.py
│       ├── json_serializer.py
│       └── toon_serializer.py          # LLM interface
│
tests/
├── shared_kernel/
│   ├── test_event_store_port.py        # Contract tests
│   ├── test_snapshot_store_port.py     # Contract tests
│   └── test_aggregate_root.py
├── infrastructure/
│   ├── test_in_memory_event_store.py
│   └── test_toon_serializer.py
```

---

## 5. WHEN: Prerequisites & Ordering

### 5.1 Dependencies

```
IMPL-001: SnowflakeIdGenerator ✅
    ↓
IMPL-002: DomainEvent Base ✅
    ↓
IMPL-003: WorkItemId ✅
    ↓
IMPL-004: Quality Value Objects ← Do first (no ES dependency)
    ↓
IMPL-ES-001: IEventStore ← Port + InMemory adapter
    ↓
IMPL-ES-002: ISnapshotStore ← Port + InMemory adapter
    ↓
IMPL-ES-003: AggregateRoot ← Base class with ES lifecycle
    ↓
IMPL-005: WorkItem Aggregate ← First ES-enabled aggregate
```

### 5.2 Snapshot Frequency Strategy

Based on industry research:

| Strategy | When to Use | Configuration |
|----------|-------------|---------------|
| Event Count | Default | Every 100 events (configurable) |
| Time-Based | Long-running | Weekly/Daily |
| State-Based | Business events | On status = COMPLETED |
| Behavioral | User sessions | Session boundaries |

**Recommendation**: Start with event count (N=100, configurable per aggregate type).

---

## 6. HOW: Implementation Approach

### 6.1 BDD Cycle per Component

```
RED → GREEN → REFACTOR

1. Write feature file with scenarios
2. Write unit tests (failing)
3. Implement minimum code to pass
4. Refactor for quality
5. Verify coverage ≥ 90%
```

### 6.2 IEventStore Implementation

**Optimistic Concurrency**:
```python
def append(self, stream_id: str, events: Sequence[DomainEvent], expected_version: int) -> None:
    current = self.get_version(stream_id)
    if current != expected_version:
        raise ConcurrencyError(f"Expected {expected_version}, got {current}")
    # Append events atomically
```

**Version Tracking**:
```python
# Each event increments version
# Stream: [v1, v2, v3, ...] where v_i = i
# get_version returns latest version number
```

### 6.3 Snapshot Integration with Repository

```python
class EventSourcedRepository(Generic[T]):
    def __init__(self, event_store: IEventStore, snapshot_store: ISnapshotStore):
        self.events = event_store
        self.snapshots = snapshot_store
        self.snapshot_frequency = 100  # Configurable

    def get(self, aggregate_id: str) -> T:
        # 1. Try to load latest snapshot
        snapshot_data = self.snapshots.get_latest(aggregate_id)

        if snapshot_data:
            snapshot, snapshot_version = snapshot_data
            # 2. Load only events AFTER snapshot
            events = self.events.read(aggregate_id, from_version=snapshot_version + 1)
            return T.load_from_snapshot(snapshot, events)
        else:
            # 3. Full replay if no snapshot
            events = self.events.read(aggregate_id)
            return T.load_from_history(events)

    def save(self, aggregate: T) -> None:
        pending = aggregate.collect_events()
        self.events.append(aggregate.id, pending, aggregate.version - len(pending))

        # 4. Create snapshot if threshold reached
        if aggregate.version % self.snapshot_frequency == 0:
            self.snapshots.save(aggregate.id, aggregate.to_snapshot(), aggregate.version)
```

### 6.4 TOON Serialization for LLM Context

**When to use TOON**:
- Primary Adapters (LLM interface layer)
- Event summaries sent to Claude
- Aggregate state in prompts

**When to use JSON**:
- Persistence (SQLite, filesystem)
- Internal API communication
- Debugging/logging

**Example TOON output** (events array):
```
events
  @type timestamp aggregate_id
  WorkItemCreated 2026-01-09T10:00:00Z WORK-001
  StatusChanged 2026-01-09T11:00:00Z WORK-001
  TestSuiteExecuted 2026-01-09T12:00:00Z WORK-001
```

vs JSON equivalent:
```json
{"events":[{"type":"WorkItemCreated","timestamp":"2026-01-09T10:00:00Z","aggregate_id":"WORK-001"},{"type":"StatusChanged","timestamp":"2026-01-09T11:00:00Z","aggregate_id":"WORK-001"},{"type":"TestSuiteExecuted","timestamp":"2026-01-09T12:00:00Z","aggregate_id":"WORK-001"}]}
```

**Token savings**: ~40% (fewer delimiters, no quotes)

---

## 7. Test Strategy

### 7.1 Test Distribution Targets

| Category | Target | Focus Areas |
|----------|--------|-------------|
| Positive | 60-65% | Happy path, serialization roundtrips |
| Negative | 25-30% | Concurrency errors, invalid versions |
| Edge | 10-15% | Empty streams, first snapshot, boundary |

### 7.2 Contract Tests for Ports

```python
class EventStoreContractTests(ABC):
    """Contract tests that any IEventStore implementation must pass."""

    @abstractmethod
    def create_store(self) -> IEventStore:
        """Factory method for specific implementation."""

    def test_append_increments_version(self):
        store = self.create_store()
        store.append("stream-1", [event], expected_version=0)
        assert store.get_version("stream-1") == 1

    def test_concurrency_error_on_version_mismatch(self):
        store = self.create_store()
        store.append("stream-1", [event], expected_version=0)
        with pytest.raises(ConcurrencyError):
            store.append("stream-1", [event], expected_version=0)  # Wrong!
```

---

## 8. References

### Industry Sources

1. [Martin Fowler - Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html)
2. [Microsoft Azure - Event Sourcing Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing)
3. [AWS - Event Sourcing Pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/event-sourcing.html)
4. [Domain Centric - Snapshotting](https://domaincentric.net/blog/event-sourcing-snapshotting)
5. [Kurrent - Snapshots in Event Sourcing](https://www.kurrent.io/blog/snapshots-in-event-sourcing)
6. [DEV Community - Snapshot Strategies](https://dev.to/alex_aslam/snapshot-strategies-optimizing-event-replays-36oo)

### TOON Format

7. [TOON Format Official](https://toonformat.dev/)
8. [GitHub - toon-format/toon](https://github.com/toon-format/toon)
9. [FreeCodeCamp - What is TOON](https://www.freecodecamp.org/news/what-is-toon-how-token-oriented-object-notation-could-change-how-ai-sees-data/)
10. [Analytics Vidhya - TOON 60% Token Savings](https://www.analyticsvidhya.com/blog/2025/11/toon-token-oriented-object-notation/)

### Library References

11. [pyeventsourcing/eventsourcing](https://github.com/pyeventsourcing/eventsourcing) - Python ES library (Context7)

### Internal ADRs

12. ADR-007: ID Generation Strategy
13. ADR-009: Event Storage Mechanism
14. ADR-IMPL-001: Unified Implementation Alignment

---

*Document Version: 1.0*
*Last Updated: 2026-01-09*
