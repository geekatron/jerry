# PAT-ENT-002: IVersioned Protocol

> **Status**: MANDATORY
> **Category**: Entity
> **Also Known As**: Optimistic Concurrency, Version Tracking

---

## Intent

Implement optimistic concurrency control via version tracking to prevent lost updates.

---

## Problem

Without version tracking:
- Concurrent modifications cause lost updates
- Last-write-wins silently loses changes
- No detection of stale data modifications
- Event sourcing append operations may conflict

---

## Solution

Track a version number that increments on each save, enabling concurrency checks.

### Implementation

```python
from typing import Protocol

class IVersioned(Protocol):
    """Optimistic concurrency control via version tracking.

    Every save operation increments the version. When saving, the
    expected version is compared against the actual version - if
    they don't match, a ConcurrencyError is raised.
    """

    @property
    def version(self) -> int:
        """Current version number.

        Starts at 0 for new entities and increments with each
        persisted change.
        """
        ...

    def get_expected_version(self) -> int:
        """Return version for concurrency check.

        Used when appending events to ensure no concurrent
        modifications have occurred.
        """
        return self.version
```

---

## Jerry Implementation

### File Location

`src/shared_kernel/interfaces/versioned.py`

### Concurrency Check Flow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Client A      │     │   Event Store   │     │   Client B      │
│   version=5     │     │   version=5     │     │   version=5     │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                       │                       │
         │  append(expected=5)   │                       │
         │──────────────────────>│                       │
         │                       │  version=6            │
         │       OK              │                       │
         │<──────────────────────│                       │
         │                       │                       │
         │                       │   append(expected=5)  │
         │                       │<──────────────────────│
         │                       │                       │
         │                       │   ConcurrencyError!   │
         │                       │──────────────────────>│
         │                       │                       │
```

### Integration with AggregateRoot

```python
@dataclass
class AggregateRoot(ABC):
    """Base class implementing IVersioned."""
    _version: int = 0

    @property
    def version(self) -> int:
        return self._version

    def _raise_event(self, event: DomainEvent) -> None:
        """Add event and increment version."""
        self._uncommitted_events.append(event)
        self._apply(event)
        self._version += 1  # Version increments with each event
```

### Event Store Integration

```python
class IEventStore(ABC):
    @abstractmethod
    def append(
        self,
        stream_id: str,
        events: List[DomainEvent],
        expected_version: int,  # From IVersioned.get_expected_version()
        metadata: Dict[str, Any] = None
    ) -> None:
        """
        Append events to stream atomically.
        Raises ConcurrencyError if expected_version doesn't match actual.
        """
        pass
```

---

## Consequences

| Type | Consequence |
|------|-------------|
| (+) | Prevents lost updates from concurrent modifications |
| (+) | Enables optimistic locking (no database locks needed) |
| (+) | Detects stale data before persistence |
| (+) | Works naturally with event sourcing |
| (-) | Clients must handle ConcurrencyError and retry |

---

## Error Handling

```python
class ConcurrencyError(DomainError):
    """Optimistic concurrency conflict."""

    def __init__(self, expected_version: int, actual_version: int):
        self.expected_version = expected_version
        self.actual_version = actual_version
        super().__init__(
            f"Concurrency conflict: expected version {expected_version}, "
            f"actual version {actual_version}"
        )

# Usage
try:
    event_store.append(stream_id, events, expected_version=5)
except ConcurrencyError as e:
    # Reload aggregate and retry
    aggregate = repository.find_by_id(aggregate_id)
    # Re-apply command logic
    # Retry append
```

---

## Related Patterns

- [PAT-ENT-001: IAuditable](./iauditable.md) - Audit metadata
- [PAT-ENT-003: AggregateRoot](./aggregate-root.md) - Implements IVersioned
- [PAT-EVT-004: IEventStore](../event/ieventstore.md) - Uses expected_version

---

## Design Canon Reference

Lines 290-316 in Jerry Design Canon v1.0

---

*Pattern documented by Claude (Opus 4.5) as part of TD-017*
