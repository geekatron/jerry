# ADR-009: Event Storage Mechanism

**Status**: Proposed
**Date**: 2026-01-09
**Deciders**: Development Team
**Technical Story**: INIT-DEV-SKILL

---

## Context

The Jerry Framework development skill uses Domain-Driven Design with Domain Events to capture significant state changes. Constraint c-007 requires Event Sourcing support, but the domain event definitions in e-008 do not specify how events are stored and replayed.

### Problem Statement

1. **Domain events are defined** (WorkItemCreated, TestSuiteExecuted, etc.) but storage mechanism is unspecified
2. **Event replay** may be needed for audit, debugging, or state reconstruction
3. **Multi-instance access** requires event storage to handle concurrency (aligned with ADR-006)
4. **No external database** available; filesystem is the only persistence mechanism
5. **Context compaction** may lose event history without persistent storage

### Decision Drivers

- **DD-001**: Filesystem-only persistence (no external database)
- **DD-002**: Multi-instance concurrency safety (aligned with ADR-006)
- **DD-003**: Audit trail for work item lifecycle
- **DD-004**: Optional event replay capability
- **DD-005**: Minimal performance overhead
- **DD-006**: Compatible with context compaction strategies
- **DD-007**: Domain layer purity (no infrastructure in domain)

### Research Findings

From e-007 Synthesis, Pattern Theme 6 (Context Engineering):
> "Aggressive context management combats context rot. Offload state to filesystem, compact at 25% threshold, use Handle Pattern for large data."

From e-008 Architecture Analysis:
> "Domain Events: WorkItemCreated, StatusChanged, TestSuiteExecuted, ReviewCompleted, QualityGateEvaluated. These represent significant domain state changes that may need to be persisted and replayed."

From e-009 Test Strategy:
> "Event-driven testing: Verify domain events are emitted correctly and can be used to reconstruct state."

---

## Considered Options

### Option 1: Full Event Sourcing (Append-Only Event Store)

Store all events in append-only log; reconstruct state by replaying events.

**Implementation**:
```python
# Storage: .jerry/data/events/{entity_id}/events.jsonl
# Each line is a single event JSON

def append_event(entity_id: str, event: DomainEvent) -> None:
    events_file = f".jerry/data/events/{entity_id}/events.jsonl"
    with FileLock(f"{events_file}.lock"):
        with open(events_file, 'a') as f:
            f.write(json.dumps(event.to_dict()) + '\n')

def load_events(entity_id: str) -> list[DomainEvent]:
    events_file = f".jerry/data/events/{entity_id}/events.jsonl"
    if not os.path.exists(events_file):
        return []
    with open(events_file) as f:
        return [DomainEvent.from_dict(json.loads(line)) for line in f]

def reconstruct_state(entity_id: str) -> WorkItem:
    events = load_events(entity_id)
    state = WorkItem.empty()
    for event in events:
        state = state.apply(event)
    return state
```

**Pros**:
- Complete audit trail
- State reconstruction possible
- Natural fit for DDD

**Cons**:
- Slow reconstruction for long event streams
- Snapshot complexity needed for performance
- Storage grows unboundedly
- Complex for multi-instance concurrent append

### Option 2: Event Log (Append-Only, No Replay)

Store events for audit/debugging but maintain separate current state.

**Implementation**:
```python
# Events: .jerry/data/events/event_log.jsonl (global log)
# State: .jerry/data/items/WORK-NNN.json (current state per item)

def emit_event(event: DomainEvent) -> None:
    # Append to global event log
    log_file = ".jerry/data/events/event_log.jsonl"
    with FileLock(f"{log_file}.lock"):
        with open(log_file, 'a') as f:
            f.write(json.dumps({
                "timestamp": datetime.utcnow().isoformat(),
                "event_type": event.__class__.__name__,
                "entity_id": event.entity_id,
                "data": event.to_dict()
            }) + '\n')

def save_state(item: WorkItem) -> None:
    # Save current state separately
    atomic_write_json(f".jerry/data/items/{item.id}.json", item.to_dict())
```

**Pros**:
- Simple implementation
- Fast state access (no replay needed)
- Audit trail preserved
- Decoupled concerns

**Cons**:
- Events and state can drift (eventual consistency)
- Cannot reconstruct state from events alone
- Not "true" event sourcing

### Option 3: Hybrid (State + Embedded Events)

Store current state with embedded event history per entity.

**Implementation**:
```python
# Single file per entity: .jerry/data/items/WORK-NNN.json
# Contains both current state and event history

{
    "id": "WORK-001",
    "status": "completed",
    "title": "Implement feature X",
    "_version": 5,
    "_events": [
        {"type": "WorkItemCreated", "timestamp": "2026-01-09T10:00:00Z", ...},
        {"type": "StatusChanged", "timestamp": "2026-01-09T11:00:00Z", "new_status": "in_progress"},
        {"type": "StatusChanged", "timestamp": "2026-01-09T12:00:00Z", "new_status": "completed"}
    ],
    "_event_count": 3
}

def save_with_event(item: WorkItem, event: DomainEvent) -> None:
    with store.locked_read_write(f"items/{item.id}.json") as data:
        data.update(item.to_dict())
        if "_events" not in data:
            data["_events"] = []
        data["_events"].append(event.to_dict())
        data["_event_count"] = len(data["_events"])
```

**Pros**:
- Atomic state + event update (no drift)
- Self-contained entity files
- Uses existing locking strategy (ADR-006)
- Event history available for replay if needed

**Cons**:
- Event history limited by file size
- Need event pruning strategy for long-lived entities
- Slightly larger files

### Option 4: Session-Scoped Event Buffer (Recommended)

Store events in memory during session; persist aggregated state changes. Optionally flush event buffer to file on significant boundaries.

**Implementation**:
```python
class SessionEventBuffer:
    """In-memory event buffer with optional persistence."""

    def __init__(self, session_id: str, persist_to_file: bool = True):
        self.session_id = session_id
        self.events: list[DomainEvent] = []
        self.persist = persist_to_file
        self.flush_threshold = 50  # Events before auto-flush

    def emit(self, event: DomainEvent) -> None:
        """Record event and auto-flush if threshold reached."""
        self.events.append(event)
        if len(self.events) >= self.flush_threshold:
            self.flush()

    def flush(self) -> None:
        """Persist events to session file."""
        if not self.persist or not self.events:
            return

        session_file = f".jerry/data/sessions/{self.session_id}/events.jsonl"
        os.makedirs(os.path.dirname(session_file), exist_ok=True)

        with FileLock(f"{session_file}.lock"):
            with open(session_file, 'a') as f:
                for event in self.events:
                    f.write(json.dumps(event.to_dict()) + '\n')

        self.events.clear()

    def get_events_for_entity(self, entity_id: str) -> list[DomainEvent]:
        """Get all events for an entity in this session."""
        return [e for e in self.events if e.entity_id == entity_id]
```

**State Storage** (separate, per ADR-006):
```python
# Current state persisted independently using atomic writes
def save_work_item(item: WorkItem) -> None:
    atomic_write_json(f".jerry/data/items/{item.id}.json", item.to_dict())
```

**Pros**:
- Minimal runtime overhead (events in memory)
- Session-scoped history for debugging
- Current state always consistent (separate storage)
- Compatible with ADR-006 locking strategy
- Natural fit for context compaction (events don't bloat context)

**Cons**:
- Event history lost on crash (unless flushed)
- No cross-session event continuity by default
- Cannot reconstruct state from events alone

---

## Decision Outcome

**Chosen Option**: Option 4 (Session-Scoped Event Buffer) with Option 3 (Hybrid) for critical entities

This hybrid approach provides:
1. **Session Event Buffer**: In-memory events for current session, flushed to session file on boundaries
2. **Embedded Events for WorkItems**: Critical entities embed recent event history (last N events)
3. **Separate State Storage**: Current state persisted via ADR-006 atomic writes

### Rationale

From e-007 Synthesis:
> "Context is precious. Compact at 25% threshold; use Handle Pattern for large data."

Event storage should not bloat the working context. Session-scoped buffers keep events available for debugging without permanent storage overhead. Critical entities embed recent history for audit trail.

From ADR-006 (File Locking Strategy):
> "Write operations: Pessimistic lock with timeout and backoff. Atomic writes: Always use temp-file-rename pattern."

Event storage must align with these patterns for consistency.

### Event Storage Architecture

```
.jerry/data/
├── items/
│   └── WORK-001.json              # Current state + embedded recent events
├── sessions/
│   └── {session_id}/
│       └── events.jsonl           # Session event log (append-only)
└── events/
    └── archive/                   # Optional: archived event logs
```

### Consequences

**Positive**:
- Minimal runtime overhead (events in memory until flush)
- Session-scoped debugging capability
- Audit trail for work items (embedded events)
- Compatible with context compaction strategies
- No unbounded growth (session events pruned)

**Negative**:
- Cannot reconstruct state from events alone
- Events may be lost on crash (acceptable trade-off)
- Need event pruning for embedded events

**Neutral**:
- Session files accumulate until manual cleanup
- Embedded event count configurable

---

## Implementation

### Domain Event Base Class

```python
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
import uuid

@dataclass(frozen=True)
class DomainEvent:
    """Base class for all domain events.

    Domain events are immutable value objects representing
    significant state changes in the domain.
    """
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    entity_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize event to dictionary."""
        return {
            "event_type": self.__class__.__name__,
            "event_id": self.event_id,
            "timestamp": self.timestamp.isoformat(),
            "entity_id": self.entity_id,
            **self._payload()
        }

    def _payload(self) -> dict[str, Any]:
        """Override in subclasses to add event-specific data."""
        return {}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DomainEvent":
        """Deserialize event from dictionary."""
        # Factory method - would use event type registry in real impl
        raise NotImplementedError("Use specific event class")
```

### Concrete Domain Events

```python
@dataclass(frozen=True)
class WorkItemCreated(DomainEvent):
    """Emitted when a new work item is created."""
    title: str = ""
    work_type: str = ""

    def _payload(self) -> dict[str, Any]:
        return {"title": self.title, "work_type": self.work_type}

@dataclass(frozen=True)
class StatusChanged(DomainEvent):
    """Emitted when work item status changes."""
    old_status: str = ""
    new_status: str = ""

    def _payload(self) -> dict[str, Any]:
        return {"old_status": self.old_status, "new_status": self.new_status}

@dataclass(frozen=True)
class TestSuiteExecuted(DomainEvent):
    """Emitted when tests are run against a work item."""
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    coverage_percent: float = 0.0

    def _payload(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "failed": self.failed,
            "skipped": self.skipped,
            "coverage_percent": self.coverage_percent
        }

@dataclass(frozen=True)
class QualityGateEvaluated(DomainEvent):
    """Emitted when quality gate is evaluated."""
    gate_level: str = ""  # L0, L1, L2
    passed: bool = False
    failures: list[str] = field(default_factory=list)

    def _payload(self) -> dict[str, Any]:
        return {
            "gate_level": self.gate_level,
            "passed": self.passed,
            "failures": list(self.failures)
        }

@dataclass(frozen=True)
class ReviewCompleted(DomainEvent):
    """Emitted when code review is completed."""
    reviewer_type: str = ""  # agent, human
    verdict: str = ""  # approved, changes_requested, rejected
    comments_count: int = 0

    def _payload(self) -> dict[str, Any]:
        return {
            "reviewer_type": self.reviewer_type,
            "verdict": self.verdict,
            "comments_count": self.comments_count
        }
```

### Session Event Buffer Implementation

```python
import os
import json
from pathlib import Path
from filelock import FileLock
from typing import Callable

class SessionEventBuffer:
    """In-memory event buffer with optional file persistence.

    Implements session-scoped event storage per ADR-009.
    Uses file locking per ADR-006 for concurrent access safety.
    """

    def __init__(
        self,
        session_id: str,
        data_dir: str = ".jerry/data",
        persist: bool = True,
        flush_threshold: int = 50,
        max_embedded_events: int = 20
    ):
        self.session_id = session_id
        self.data_dir = Path(data_dir)
        self.persist = persist
        self.flush_threshold = flush_threshold
        self.max_embedded_events = max_embedded_events
        self._events: list[DomainEvent] = []
        self._handlers: list[Callable[[DomainEvent], None]] = []

    @property
    def events(self) -> list[DomainEvent]:
        """Read-only access to buffered events."""
        return list(self._events)

    def register_handler(self, handler: Callable[[DomainEvent], None]) -> None:
        """Register an event handler for side effects."""
        self._handlers.append(handler)

    def emit(self, event: DomainEvent) -> None:
        """Emit a domain event.

        1. Add to in-memory buffer
        2. Notify registered handlers
        3. Auto-flush if threshold reached
        """
        self._events.append(event)

        # Notify handlers (e.g., logging, metrics)
        for handler in self._handlers:
            try:
                handler(event)
            except Exception:
                pass  # Handlers should not fail event emission

        # Auto-flush if threshold reached
        if len(self._events) >= self.flush_threshold:
            self.flush()

    def flush(self) -> None:
        """Persist buffered events to session file."""
        if not self.persist or not self._events:
            return

        session_dir = self.data_dir / "sessions" / self.session_id
        session_dir.mkdir(parents=True, exist_ok=True)
        session_file = session_dir / "events.jsonl"

        lock = FileLock(f"{session_file}.lock", timeout=30)
        with lock:
            with open(session_file, 'a', encoding='utf-8') as f:
                for event in self._events:
                    f.write(json.dumps(event.to_dict()) + '\n')

        self._events.clear()

    def get_events_for_entity(self, entity_id: str) -> list[DomainEvent]:
        """Get all buffered events for a specific entity."""
        return [e for e in self._events if e.entity_id == entity_id]

    def get_recent_events(self, count: int = 10) -> list[DomainEvent]:
        """Get most recent events from buffer."""
        return self._events[-count:]

    def load_session_events(self) -> list[dict]:
        """Load all persisted events for this session."""
        session_file = self.data_dir / "sessions" / self.session_id / "events.jsonl"
        if not session_file.exists():
            return []

        events = []
        with open(session_file, encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    events.append(json.loads(line))
        return events

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.flush()
```

### Work Item with Embedded Events

```python
from dataclasses import dataclass, field

@dataclass
class WorkItem:
    """Work item entity with embedded event history."""

    id: str
    title: str
    status: str = "pending"
    work_type: str = "task"
    _version: int = 0
    _recent_events: list[dict] = field(default_factory=list)
    _max_events: int = field(default=20, repr=False)

    def apply_event(self, event: DomainEvent) -> None:
        """Apply event and record in history."""
        # Update state based on event type
        if isinstance(event, StatusChanged):
            self.status = event.new_status

        # Record in embedded history
        self._recent_events.append(event.to_dict())

        # Prune old events if over limit
        if len(self._recent_events) > self._max_events:
            self._recent_events = self._recent_events[-self._max_events:]

        self._version += 1

    def to_dict(self) -> dict:
        """Serialize to dictionary including event history."""
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "work_type": self.work_type,
            "_version": self._version,
            "_recent_events": self._recent_events,
            "_event_count": len(self._recent_events)
        }

    @classmethod
    def from_dict(cls, data: dict) -> "WorkItem":
        """Deserialize from dictionary."""
        return cls(
            id=data["id"],
            title=data["title"],
            status=data.get("status", "pending"),
            work_type=data.get("work_type", "task"),
            _version=data.get("_version", 0),
            _recent_events=data.get("_recent_events", [])
        )
```

### Integration with Work Item Repository

```python
class FileSystemWorkItemRepository:
    """Repository implementation with event support.

    Integrates with:
    - ADR-006: File locking for concurrent access
    - ADR-007: Snowflake IDs for unique identifiers
    - ADR-009: Session event buffer for event storage
    """

    def __init__(
        self,
        store: ConcurrentFileStore,
        event_buffer: SessionEventBuffer
    ):
        self.store = store
        self.event_buffer = event_buffer

    def save(self, item: WorkItem, event: DomainEvent | None = None) -> None:
        """Save work item with optional event emission."""
        with self.store.locked_read_write(f"items/{item.id}.json") as data:
            if event:
                item.apply_event(event)
                self.event_buffer.emit(event)

            data.update(item.to_dict())

    def get(self, item_id: str) -> WorkItem | None:
        """Retrieve work item by ID."""
        data = self.store.read(f"items/{item_id}.json")
        if data is None:
            return None
        return WorkItem.from_dict(data)

    def create(self, title: str, work_type: str = "task") -> WorkItem:
        """Create new work item with unique ID."""
        item_id = f"WORK-{self.store.id_generator.generate_hex()[:8].upper()}"
        item = WorkItem(id=item_id, title=title, work_type=work_type)

        event = WorkItemCreated(
            entity_id=item_id,
            title=title,
            work_type=work_type
        )

        self.save(item, event)
        return item
```

---

## Validation

### Unit Tests

```python
import pytest
from datetime import datetime, timezone

class TestDomainEvents:
    """Tests for domain event serialization."""

    def test_event_serialization_round_trip(self):
        """Verify events can be serialized and deserialized."""
        event = WorkItemCreated(
            entity_id="WORK-001",
            title="Test item",
            work_type="task"
        )

        data = event.to_dict()

        assert data["event_type"] == "WorkItemCreated"
        assert data["entity_id"] == "WORK-001"
        assert data["title"] == "Test item"
        assert "timestamp" in data
        assert "event_id" in data

    def test_event_immutability(self):
        """Verify events are immutable."""
        event = StatusChanged(
            entity_id="WORK-001",
            old_status="pending",
            new_status="in_progress"
        )

        with pytest.raises(AttributeError):
            event.new_status = "completed"


class TestSessionEventBuffer:
    """Tests for session event buffer."""

    def test_emit_adds_to_buffer(self, tmp_path):
        """Verify emit adds events to buffer."""
        buffer = SessionEventBuffer(
            session_id="test-session",
            data_dir=str(tmp_path),
            persist=False
        )

        event = WorkItemCreated(entity_id="WORK-001", title="Test")
        buffer.emit(event)

        assert len(buffer.events) == 1
        assert buffer.events[0] == event

    def test_flush_persists_events(self, tmp_path):
        """Verify flush writes events to file."""
        buffer = SessionEventBuffer(
            session_id="test-session",
            data_dir=str(tmp_path),
            persist=True
        )

        event = WorkItemCreated(entity_id="WORK-001", title="Test")
        buffer.emit(event)
        buffer.flush()

        # Buffer should be cleared
        assert len(buffer.events) == 0

        # File should contain event
        session_file = tmp_path / "sessions" / "test-session" / "events.jsonl"
        assert session_file.exists()

        loaded = buffer.load_session_events()
        assert len(loaded) == 1
        assert loaded[0]["entity_id"] == "WORK-001"

    def test_auto_flush_at_threshold(self, tmp_path):
        """Verify auto-flush when threshold reached."""
        buffer = SessionEventBuffer(
            session_id="test-session",
            data_dir=str(tmp_path),
            persist=True,
            flush_threshold=5
        )

        for i in range(5):
            buffer.emit(WorkItemCreated(entity_id=f"WORK-{i:03d}", title=f"Item {i}"))

        # Should have auto-flushed
        assert len(buffer.events) == 0

        loaded = buffer.load_session_events()
        assert len(loaded) == 5

    def test_get_events_for_entity(self, tmp_path):
        """Verify filtering events by entity."""
        buffer = SessionEventBuffer(
            session_id="test-session",
            data_dir=str(tmp_path),
            persist=False
        )

        buffer.emit(WorkItemCreated(entity_id="WORK-001", title="Item 1"))
        buffer.emit(WorkItemCreated(entity_id="WORK-002", title="Item 2"))
        buffer.emit(StatusChanged(entity_id="WORK-001", old_status="pending", new_status="active"))

        events = buffer.get_events_for_entity("WORK-001")

        assert len(events) == 2
        assert all(e.entity_id == "WORK-001" for e in events)


class TestWorkItemEmbeddedEvents:
    """Tests for work item embedded event history."""

    def test_apply_event_updates_state(self):
        """Verify applying event updates work item state."""
        item = WorkItem(id="WORK-001", title="Test", status="pending")

        event = StatusChanged(
            entity_id="WORK-001",
            old_status="pending",
            new_status="in_progress"
        )

        item.apply_event(event)

        assert item.status == "in_progress"
        assert item._version == 1
        assert len(item._recent_events) == 1

    def test_event_pruning_at_limit(self):
        """Verify old events are pruned when limit reached."""
        item = WorkItem(id="WORK-001", title="Test", _max_events=5)

        for i in range(10):
            event = StatusChanged(
                entity_id="WORK-001",
                old_status=f"status-{i}",
                new_status=f"status-{i+1}"
            )
            item.apply_event(event)

        # Should only have last 5 events
        assert len(item._recent_events) == 5
        assert item._version == 10

    def test_serialization_includes_events(self):
        """Verify to_dict includes event history."""
        item = WorkItem(id="WORK-001", title="Test")
        event = WorkItemCreated(entity_id="WORK-001", title="Test", work_type="task")
        item.apply_event(event)

        data = item.to_dict()

        assert "_recent_events" in data
        assert len(data["_recent_events"]) == 1
        assert data["_event_count"] == 1
```

### Integration Tests

```python
class TestEventStorageIntegration:
    """Integration tests for event storage with repository."""

    def test_create_emits_event(self, tmp_path):
        """Verify creating work item emits WorkItemCreated event."""
        store = ConcurrentFileStore(str(tmp_path / "data"))
        buffer = SessionEventBuffer(
            session_id="test",
            data_dir=str(tmp_path / "data"),
            persist=False
        )
        repo = FileSystemWorkItemRepository(store, buffer)

        item = repo.create("Test task", "task")

        assert len(buffer.events) == 1
        assert isinstance(buffer.events[0], WorkItemCreated)
        assert buffer.events[0].entity_id == item.id

    def test_save_with_event_persists_both(self, tmp_path):
        """Verify save persists both state and event."""
        store = ConcurrentFileStore(str(tmp_path / "data"))
        buffer = SessionEventBuffer(
            session_id="test",
            data_dir=str(tmp_path / "data"),
            persist=True
        )
        repo = FileSystemWorkItemRepository(store, buffer)

        item = repo.create("Test task", "task")

        event = StatusChanged(
            entity_id=item.id,
            old_status="pending",
            new_status="in_progress"
        )
        repo.save(item, event)

        # Reload and verify
        reloaded = repo.get(item.id)
        assert reloaded.status == "in_progress"
        assert len(reloaded._recent_events) == 2  # Created + StatusChanged
```

---

## References

### Primary Sources

1. **Event Sourcing** (Martin Fowler)
   - https://martinfowler.com/eaaDev/EventSourcing.html

2. **Domain-Driven Design** (Eric Evans)
   - Domain Events pattern

3. **CQRS and Event Sourcing** (Greg Young)
   - https://cqrs.wordpress.com/

### Research Documents

4. **e-007 Research Synthesis**
   - Theme 6: Context Engineering patterns
   - Document: `projects/PROJ-001-plugin-cleanup/research/dev-skill-e-007-synthesis.md`

5. **e-008 Architecture Analysis**
   - Domain event definitions
   - Document: `projects/PROJ-001-plugin-cleanup/research/dev-skill-e-008-architecture-analysis.md`

6. **e-009 Test Strategy**
   - Event-driven testing approach
   - Document: `projects/PROJ-001-plugin-cleanup/research/dev-skill-e-009-test-strategy.md`

### Related ADRs

7. **ADR-006: File Locking Strategy**
   - Concurrent access safety for event files
   - Document: `projects/PROJ-001-plugin-cleanup/design/ADR-006-file-locking-strategy.md`

8. **ADR-007: ID Generation Strategy**
   - Unique event IDs via Snowflake pattern
   - Document: `projects/PROJ-001-plugin-cleanup/design/ADR-007-id-generation-strategy.md`

---

## Pattern Traceability

| Pattern ID | Pattern Name | Implementation Component |
|------------|--------------|-------------------------|
| PAT-004-e001 | Pre-Rot Compaction | Session event buffer with flush threshold |
| PAT-003-e001 | Handle Pattern | Event references vs. inline events |
| c-007 | Event Sourcing | Domain events + embedded history |
| PAT-001-e005 | Atomic Write | Event file persistence |
| PAT-002-e005 | File Locking | Concurrent event log access |

---

*ADR created: 2026-01-09*
*Author: Orchestrator (remediation)*
*Technical Story: INIT-DEV-SKILL*
*Constraint addressed: c-007 (Event Sourcing)*
