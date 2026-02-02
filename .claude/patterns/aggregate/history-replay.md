# PAT-AGG-003: History Replay Pattern

> **Status**: MANDATORY
> **Category**: Aggregate Pattern
> **Location**: `src/work_tracking/domain/aggregates/base.py`

---

## Overview

The History Replay pattern enables reconstituting aggregates from their event stream. Instead of storing current state, the aggregate is rebuilt by replaying all historical events in order.

---

## Industry Prior Art

| Source | Key Insight |
|--------|-------------|
| **Greg Young** | "The current state is a left fold over the event stream" |
| **Martin Fowler** | "Event Sourcing ensures that all changes are stored as a sequence of events" |
| **Vaughn Vernon** | "Aggregates are reconstituted by replaying their event history" |

---

## Jerry Implementation

### Load from History

```python
# In AggregateRoot base class
class AggregateRoot(ABC):
    @classmethod
    def load_from_history(cls, events: Sequence[DomainEvent]) -> AggregateRoot:
        """Reconstruct aggregate from event stream.

        This is the primary way to load aggregates from the event store.
        Events are replayed in order to rebuild the current state.

        Args:
            events: Ordered sequence of domain events

        Returns:
            Reconstituted aggregate instance

        Raises:
            ValueError: If event stream is empty

        Example:
            events = event_store.read("WORK-001")
            work_item = WorkItem.load_from_history(events)
        """
        if not events:
            raise ValueError("Cannot load from empty event stream")

        # Create instance without triggering factory
        instance = cls.__new__(cls)
        instance._initialize(
            id=events[0].aggregate_id,
            version=0,
        )

        # Replay all events in order
        for event in events:
            instance._version += 1
            instance._apply(event)

            # Track timestamps
            if instance._created_on is None:
                instance._created_on = event.timestamp
            instance._modified_on = event.timestamp

        return instance

    @abstractmethod
    def _apply(self, event: DomainEvent) -> None:
        """Apply event to update aggregate state.

        CRITICAL: This method MUST be:
        - Deterministic (same input → same output)
        - Side-effect free (no I/O, no external calls)
        - Idempotent with version tracking

        This is called during:
        - Event recording (via _raise_event)
        - History replay (via load_from_history)
        """
        ...
```

### Apply Method Implementation

```python
class WorkItem(AggregateRoot):
    def _apply(self, event: DomainEvent) -> None:
        """Apply event to update state.

        Pattern matching ensures all event types are handled.
        Each case updates only the relevant state fields.
        """
        match event:
            case WorkItemCreated():
                self._title = event.title
                self._work_type = event.work_type
                self._priority = Priority.from_string(event.priority)
                self._description = event.description
                self._parent_id = event.parent_id
                self._status = WorkItemStatus.PENDING
                self._subtasks = []
                self._dependencies = []

            case StatusChanged():
                self._status = WorkItemStatus(event.new_status)

            case PriorityChanged():
                self._priority = Priority(event.new_priority)

            case SubtaskAdded():
                self._subtasks.append(event.subtask_id)

            case DependencyAdded():
                self._dependencies.append(event.dependency_id)

            case DependencyRemoved():
                if event.dependency_id in self._dependencies:
                    self._dependencies.remove(event.dependency_id)

            case WorkItemCompleted():
                self._status = WorkItemStatus.DONE
                self._quality_passed = event.quality_passed
                self._completed_at = event.timestamp

            case _:
                raise UnknownEventTypeError(
                    f"Unknown event type: {type(event).__name__}"
                )
```

---

## Replay Flow

```
Event Store                              Aggregate
┌────────────────────┐                  ┌────────────────────────┐
│ Stream: WORK-001   │                  │  WorkItem              │
│                    │                  │                        │
│ v1: WorkItemCreated│──────────────────│► _apply(Created)       │
│     title="Task"   │                  │  _title = "Task"       │
│                    │                  │  _status = PENDING     │
│ v2: StatusChanged  │──────────────────│► _apply(StatusChanged) │
│     → IN_PROGRESS  │                  │  _status = IN_PROGRESS │
│                    │                  │                        │
│ v3: PriorityChanged│──────────────────│► _apply(PriorityChanged│
│     → HIGH         │                  │  _priority = HIGH      │
│                    │                  │                        │
│ v4: WorkItemComplete│─────────────────│► _apply(Completed)     │
│     passed=true    │                  │  _status = DONE        │
└────────────────────┘                  └────────────────────────┘
                                               version = 4
```

---

## Repository Integration

```python
# In repository adapter
class EventSourcedWorkItemRepository:
    """Repository that uses event store for persistence."""

    def __init__(self, event_store: IEventStore) -> None:
        self._event_store = event_store

    def get(self, id: WorkItemId) -> WorkItem | None:
        """Load aggregate from event history."""
        stream_id = f"WorkItem-{id.value}"
        events = self._event_store.read(stream_id)

        if not events:
            return None

        return WorkItem.load_from_history(events)

    def save(self, aggregate: WorkItem) -> None:
        """Persist new events to event store."""
        stream_id = f"WorkItem-{aggregate.id}"
        events = aggregate.collect_events()

        if not events:
            return  # No changes

        # Calculate expected version
        expected_version = aggregate.version - len(events)

        self._event_store.append(
            stream_id=stream_id,
            events=events,
            expected_version=expected_version,
        )
```

---

## Snapshot Optimization

For aggregates with many events, snapshots improve performance:

```python
class SnapshotOptimizedRepository:
    """Repository with snapshot support for long event streams."""

    SNAPSHOT_FREQUENCY = 10  # Per Jerry Design Canon

    def get(self, id: WorkItemId) -> WorkItem | None:
        """Load from snapshot + recent events."""
        stream_id = f"WorkItem-{id.value}"

        # Try to load from snapshot
        snapshot = self._snapshot_store.get(stream_id)

        if snapshot:
            # Load events after snapshot
            events = self._event_store.read(
                stream_id,
                from_version=snapshot.version + 1,
            )
            aggregate = snapshot.aggregate
            for event in events:
                aggregate._version += 1
                aggregate._apply(event)
            return aggregate
        else:
            # Full replay from beginning
            events = self._event_store.read(stream_id)
            if not events:
                return None
            return WorkItem.load_from_history(events)

    def save(self, aggregate: WorkItem) -> None:
        """Save events and snapshot if needed."""
        stream_id = f"WorkItem-{aggregate.id}"
        events = aggregate.collect_events()

        if not events:
            return

        expected_version = aggregate.version - len(events)
        self._event_store.append(stream_id, events, expected_version)

        # Take snapshot every N events
        if aggregate.version % self.SNAPSHOT_FREQUENCY == 0:
            self._snapshot_store.save(
                stream_id=stream_id,
                version=aggregate.version,
                aggregate=aggregate,
            )
```

> **Jerry Decision**: Snapshot every 10 events. This balances storage cost with replay performance.

---

## Determinism Requirements

The `_apply` method MUST be deterministic:

```python
# CORRECT: Deterministic apply
def _apply(self, event: DomainEvent) -> None:
    match event:
        case StatusChanged():
            self._status = WorkItemStatus(event.new_status)

# WRONG: Non-deterministic (uses current time)
def _apply(self, event: DomainEvent) -> None:
    match event:
        case StatusChanged():
            self._status = WorkItemStatus(event.new_status)
            self._updated_at = datetime.now()  # NON-DETERMINISTIC!

# CORRECT: Use timestamp from event
def _apply(self, event: DomainEvent) -> None:
    match event:
        case StatusChanged():
            self._status = WorkItemStatus(event.new_status)
            self._modified_on = event.timestamp  # From event
```

---

## Testing Pattern

```python
def test_aggregate_reconstitutes_from_event_history():
    """Aggregate state matches after replay."""
    # Create and operate on aggregate
    original = WorkItem.create(id="WORK-001", title="Test Task")
    original.start()
    original.set_priority(Priority.HIGH)
    original.complete()

    events = original.collect_events()

    # Reconstitute from events
    reconstituted = WorkItem.load_from_history(events)

    # State should match
    assert reconstituted.id == original.id
    assert reconstituted.title == original.title
    assert reconstituted.status == WorkItemStatus.DONE
    assert reconstituted.priority == Priority.HIGH
    assert reconstituted.version == 4


def test_replay_is_deterministic():
    """Same events always produce same state."""
    events = [
        WorkItemCreated(..., title="Test", priority="medium"),
        StatusChanged(..., new_status="in_progress"),
        PriorityChanged(..., new_priority="high"),
    ]

    result1 = WorkItem.load_from_history(events)
    result2 = WorkItem.load_from_history(events)

    assert result1.title == result2.title
    assert result1.status == result2.status
    assert result1.priority == result2.priority
    assert result1.version == result2.version


def test_empty_event_stream_raises_error():
    """Cannot reconstitute from empty stream."""
    with pytest.raises(ValueError) as exc_info:
        WorkItem.load_from_history([])

    assert "empty event stream" in str(exc_info.value)
```

---

## Anti-Patterns

### 1. Non-Deterministic Apply

```python
# WRONG: Uses current time
def _apply(self, event: DomainEvent) -> None:
    self._updated_at = datetime.now()  # Different each replay!
```

### 2. External Calls in Apply

```python
# WRONG: Makes external call
def _apply(self, event: DomainEvent) -> None:
    self._exchange_rate = forex_api.get_rate()  # Side effect!
```

### 3. Missing Event Type

```python
# WRONG: Silently ignores unknown events
def _apply(self, event: DomainEvent) -> None:
    match event:
        case WorkItemCreated():
            ...
        case _:
            pass  # Unknown events silently ignored!

# CORRECT: Fail explicitly
def _apply(self, event: DomainEvent) -> None:
    match event:
        case WorkItemCreated():
            ...
        case _:
            raise UnknownEventTypeError(type(event).__name__)
```

---

## References

- **Greg Young**: [CQRS and Event Sourcing](https://cqrs.files.wordpress.com/2010/11/cqrs_documents.pdf)
- **Martin Fowler**: [Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html)
- **Design Canon**: Section 5.5 - Event Sourcing
- **Related Patterns**: PAT-EVT-004 (IEventStore), PAT-AGG-002 (Event Collection)
