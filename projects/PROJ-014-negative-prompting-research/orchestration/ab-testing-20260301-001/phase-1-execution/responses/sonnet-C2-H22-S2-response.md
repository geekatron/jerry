# Optimistic Concurrency Control in Event-Sourced Systems: Python Best Practices

> Research synthesized via ps-researcher. Date: 2026-03-01.
> Decision deadline: end of day. Recommendation: version numbers.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Recommendation](#recommendation) | Bottom line up front for your decision |
| [Version Numbers vs Timestamps](#version-numbers-vs-timestamps) | Trade-off analysis |
| [How OCC Works in Event Sourcing](#how-occ-works-in-event-sourcing) | Core mechanism |
| [Python Implementation](#python-implementation) | Practical code patterns |
| [Conflict Handling](#conflict-handling) | Retry strategies |
| [Sources](#sources) | Research citations |

---

## Recommendation

**Use version numbers. Do not use timestamps for optimistic concurrency control in event-sourced systems.**

This is a settled question in the event sourcing community. Both EventStoreDB and Marten (the two most widely deployed event stores) use sequential integer version numbers derived from the event position within the aggregate's stream. The Python `eventsourcing` library does the same.

Timestamps serve a different purpose: they record *when* an event occurred. They are useful for auditing and querying, but they are not reliable concurrency guards. Use both -- version numbers for OCC enforcement, timestamps for event metadata -- but never substitute one for the other.

---

## Version Numbers vs Timestamps

### Version Numbers

| Property | Detail |
|----------|--------|
| Precision | Exact -- each event occupies exactly one position. No two events share a version. |
| Monotonicity | Guaranteed -- version N+1 always follows version N within a stream. |
| Conflict detection | Binary and unambiguous -- expected version either matches or it does not. |
| Missing event detection | Possible -- gaps in sequence signal data integrity problems. |
| Implementation complexity | Low -- integer comparison + unique constraint in the event store. |
| Distributed systems | Scoped to a single aggregate stream; no global counter required. |

### Timestamps

| Property | Detail |
|----------|--------|
| Precision | Limited -- millisecond granularity means two events within the same millisecond share a timestamp, making it impossible to distinguish them for concurrency purposes. |
| Monotonicity | Not guaranteed -- clock skew across servers, NTP corrections, and daylight saving time adjustments can cause timestamps to go backward or repeat. |
| Conflict detection | Unreliable -- two concurrent writes can carry identical timestamps, creating silent overwrites rather than detected conflicts. |
| Distributed systems | Clocks across nodes are not synchronized to sub-millisecond accuracy in practice, making cross-node timestamp comparison unsafe as a concurrency mechanism. |

The version number approach is strictly superior for OCC. Timestamps carry known failure modes that cannot be mitigated without specialized infrastructure (e.g., TrueTime in Google Spanner, or Hybrid Logical Clocks in CockroachDB). Unless you are running on such infrastructure, timestamps are not a safe concurrency guard.

---

## How OCC Works in Event Sourcing

The mechanism is straightforward:

1. **Read phase:** Load the aggregate from the event store. Record the current version number (the position of the last event in the aggregate's stream).
2. **Process phase:** Apply the command to the aggregate. Produce new domain events.
3. **Write phase:** Append new events to the stream, specifying the *expected version* (the version recorded at read time). The event store rejects the write if the stream's current version no longer matches the expected version -- indicating a concurrent write occurred between step 1 and step 3.
4. **Conflict handling:** On rejection, reload the aggregate, re-apply the command, and retry.

The event store enforces the constraint atomically, typically via a unique index on `(aggregate_id, version)` in the underlying database. This means the check-and-append is a single atomic operation -- no application-level locking is required.

```
                      ┌─────────────────────────────────┐
                      │         Event Store              │
                      │                                  │
  load(id)    ──────> │  stream: [v1, v2, v3]            │
  returns v3          │  current_version = 3             │
                      │                                  │
  append(events,      │  IF current_version == 3:        │
    expected=3) ────> │    store events at v4, v5, ...   │
                      │  ELSE:                           │
                      │    raise ConcurrencyError        │
                      └─────────────────────────────────┘
```

---

## Python Implementation

### Using the `eventsourcing` library (recommended starting point)

The `eventsourcing` library (v9.5.x as of this writing) provides OCC out of the box via `IntegrityError`. The library enforces uniqueness on `(originator_id, originator_version)`:

```python
from eventsourcing.application import Application
from eventsourcing.domain import Aggregate
from eventsourcing.persistence import IntegrityError


class Order(Aggregate):
    def __init__(self, order_id: str, customer: str) -> None:
        self.order_id = order_id
        self.customer = customer
        self.status = "pending"

    @classmethod
    def create(cls, order_id: str, customer: str) -> "Order":
        return cls._create(cls.Created, id=order_id, order_id=order_id, customer=customer)

    def confirm(self) -> None:
        self._trigger_(self.Confirmed)

    def apply_confirmed(self, event: "Order.Confirmed") -> None:
        self.status = "confirmed"

    class Created(Aggregate.Created):
        order_id: str
        customer: str

    class Confirmed(Aggregate.Event):
        pass


class OrderApp(Application):
    def create_order(self, order_id: str, customer: str) -> str:
        order = Order.create(order_id=order_id, customer=customer)
        self.save(order)
        return order.id

    def confirm_order(self, order_id: str) -> None:
        order = self.repository.get(order_id)
        order.confirm()
        self.save(order)


# Optimistic concurrency conflict example:
app = OrderApp()
order_id = app.create_order("ord-001", "Alice")

# Load the same aggregate twice -- simulating two concurrent operations
order_v1 = app.repository.get(order_id)  # version 1
order_v2 = app.repository.get(order_id)  # version 1

# First save succeeds -- advances to version 2
order_v1.confirm()
app.save(order_v1)

# Second save fails -- expected version 1 no longer matches
order_v2.confirm()
try:
    app.save(order_v2)
except IntegrityError:
    # Reload and retry
    order_fresh = app.repository.get(order_id)
    order_fresh.confirm()
    app.save(order_fresh)
```

### Rolling your own event store (SQLAlchemy + PostgreSQL)

If you are not using the `eventsourcing` library, implement OCC by enforcing a unique constraint at the database level and catching the violation:

```python
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Session


class Base(DeclarativeBase):
    pass


class StoredEvent(Base):
    __tablename__ = "events"

    id: sa.orm.Mapped[UUID] = sa.orm.mapped_column(
        sa.UUID, primary_key=True, default=uuid4
    )
    aggregate_id: sa.orm.Mapped[UUID] = sa.orm.mapped_column(sa.UUID, nullable=False)
    # version is the position within the aggregate's stream, starting at 1
    version: sa.orm.Mapped[int] = sa.orm.mapped_column(sa.Integer, nullable=False)
    event_type: sa.orm.Mapped[str] = sa.orm.mapped_column(sa.String, nullable=False)
    payload: sa.orm.Mapped[dict] = sa.orm.mapped_column(sa.JSON, nullable=False)
    # timestamp is metadata, NOT the concurrency token
    occurred_at: sa.orm.Mapped[datetime] = sa.orm.mapped_column(
        sa.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    __table_args__ = (
        # This unique constraint IS the OCC mechanism.
        # An INSERT with a duplicate (aggregate_id, version) raises IntegrityError.
        sa.UniqueConstraint("aggregate_id", "version", name="uq_events_aggregate_version"),
    )


@dataclass
class DomainEvent:
    aggregate_id: UUID
    version: int          # OCC token -- position in stream
    event_type: str
    payload: dict[str, Any]
    occurred_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class OptimisticConcurrencyError(Exception):
    pass


class EventStore:
    def __init__(self, session: Session) -> None:
        self._session = session

    def load(self, aggregate_id: UUID) -> list[DomainEvent]:
        rows = (
            self._session.query(StoredEvent)
            .filter_by(aggregate_id=aggregate_id)
            .order_by(StoredEvent.version)
            .all()
        )
        return [
            DomainEvent(
                aggregate_id=row.aggregate_id,
                version=row.version,
                event_type=row.event_type,
                payload=row.payload,
                occurred_at=row.occurred_at,
            )
            for row in rows
        ]

    def append(
        self,
        events: list[DomainEvent],
        expected_version: int,
    ) -> None:
        """Append events atomically.

        Raises OptimisticConcurrencyError if the stream has been modified
        since expected_version was observed.
        """
        # Verify expected version before writing (belt-and-suspenders;
        # the unique constraint below is the definitive atomic guard)
        current = (
            self._session.query(sa.func.max(StoredEvent.version))
            .filter_by(aggregate_id=events[0].aggregate_id)
            .scalar()
            or 0
        )
        if current != expected_version:
            raise OptimisticConcurrencyError(
                f"Concurrency conflict: expected version {expected_version}, "
                f"found {current}."
            )

        try:
            for event in events:
                stored = StoredEvent(
                    aggregate_id=event.aggregate_id,
                    version=event.version,
                    event_type=event.event_type,
                    payload=event.payload,
                    occurred_at=event.occurred_at,
                )
                self._session.add(stored)
            self._session.commit()
        except sa.exc.IntegrityError as exc:
            self._session.rollback()
            raise OptimisticConcurrencyError(
                "Concurrency conflict detected by database unique constraint."
            ) from exc
```

Note that the in-application version check is not sufficient on its own -- a race condition between the check and the INSERT is still possible. The unique constraint on `(aggregate_id, version)` is the authoritative atomic guard. The in-application check is an early-exit optimization to produce a cleaner error message before hitting the database.

---

## Conflict Handling

When `OptimisticConcurrencyError` is raised, the standard pattern is reload-and-retry:

```python
import time
from typing import Callable, TypeVar

T = TypeVar("T")


def with_retry(
    operation: Callable[[], T],
    max_retries: int = 3,
    backoff_seconds: float = 0.1,
) -> T:
    """Execute operation with exponential backoff on concurrency conflicts."""
    for attempt in range(max_retries):
        try:
            return operation()
        except OptimisticConcurrencyError:
            if attempt == max_retries - 1:
                raise
            time.sleep(backoff_seconds * (2 ** attempt))
    raise RuntimeError("Unreachable")


# Usage:
def confirm_order(order_id: UUID, store: EventStore) -> None:
    def attempt() -> None:
        events = store.load(order_id)
        current_version = events[-1].version if events else 0
        # Rebuild aggregate state from events, apply command, produce new events
        new_event = DomainEvent(
            aggregate_id=order_id,
            version=current_version + 1,
            event_type="OrderConfirmed",
            payload={},
        )
        store.append([new_event], expected_version=current_version)

    with_retry(attempt)
```

**Practical notes on retry strategy:**

- Exponential backoff with jitter reduces thundering-herd problems under high contention.
- Monitor your conflict rate. A sustained conflict rate above 5% suggests your aggregate boundaries are too coarse -- multiple operations contend on the same aggregate too frequently. Consider splitting the aggregate or redesigning the command flow.
- Not all conflicts are worth retrying. If the business rule requires that a specific version was the basis for a decision (e.g., "confirm this order only if it is still in the state I read"), re-applying the command after reload may not be correct. Evaluate whether the command is idempotent and whether the post-reload state still satisfies the command's preconditions.

---

## Summary Decision Matrix

| Criterion | Version Numbers | Timestamps |
|-----------|----------------|------------|
| Conflict detection reliability | Exact | Unreliable (clock skew, precision limits) |
| Implementation complexity | Low | High (requires clock synchronization infrastructure) |
| Industry adoption | Universal (EventStoreDB, Marten, eventsourcing lib) | Rare for OCC |
| Missing event detection | Yes | No |
| Distributed system safety | Yes (stream-scoped) | No (requires TrueTime/HLC) |
| Suitable as audit metadata | No (use timestamp for this) | Yes |

**Final answer:** Use version numbers as the OCC token. Store timestamps as event metadata for auditing. Do not conflate the two roles.

---

## Sources

- [Optimistic concurrency control - Event Sourcing in Python (eventsourcing docs)](https://eventsourcing.readthedocs.io/en/v3.1.0/topics/examples/concurrency.html)
- [eventsourcing library on PyPI](https://pypi.org/project/eventsourcing/)
- [eventsourcing GitHub repository](https://github.com/pyeventsourcing/eventsourcing)
- [Optimistic Concurrency Control: A Practical Guide for 2025 (Shadecoder)](https://www.shadecoder.com/topics/optimistic-concurrency-control-a-practical-guide-for-2025)
- [Optimistic concurrency for pessimistic times (Event-Driven.io)](https://event-driven.io/en/optimistic_concurrency_for_pessimistic_times/)
- [Event Sourcing and Concurrent Updates (Teiva Harsanyi, Medium)](https://teivah.medium.com/event-sourcing-and-concurrent-updates-32354ec26a4c)
- [What are the pros and cons of using timestamps vs version numbers for optimistic concurrency control? (LinkedIn Advice)](https://www.linkedin.com/advice/3/what-pros-cons-using-timestamps-vs-version)
- [Optimistic Locking (Fraktalio)](https://fraktalio.com/blog/optimistic-locking.html)
- [The trouble with timestamps (Aphyr)](https://aphyr.com/posts/299-the-trouble-with-timestamps)
- [How to Build Event Sourcing Implementation (OneUptime, 2026-01-30)](https://oneuptime.com/blog/post/2026-01-30-event-sourcing-implementation/view)
