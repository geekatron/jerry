# Optimistic Concurrency Control in Event-Sourced Python Systems

> **Skill invoked:** `/problem-solving` (ps-researcher + ps-analyst)
> **Routing rationale:** The request requires gathering and synthesizing current technical information — a research task with a decision deadline. Keyword triggers: "best practices", "considering", "need to make a decision". H-22 mandates `/problem-solving` proactive invocation before content is produced.
> **Date:** 2026-03-01

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Decision Summary](#l0-decision-summary) | What to choose and why — one paragraph |
| [L1: Technical Implementation](#l1-technical-implementation) | Python code patterns, version numbers vs timestamps |
| [L2: Trade-off Analysis](#l2-trade-off-analysis) | Architectural implications and edge cases |
| [Sources](#sources) | All referenced material |

---

## L0: Decision Summary

**Use version numbers. Do not use timestamps.**

Version numbers (monotonically incrementing integers per aggregate stream) are the established best practice for optimistic concurrency control in event-sourced systems. The canonical Python library `eventsourcing` (v9.5.x) implements this natively. Every major event store — EventStoreDB, Marten, Axon — uses stream version numbers as the concurrency guard. Timestamps introduce clock skew risk in any environment with more than one process, are not guaranteed unique at millisecond granularity, and carry no causal ordering guarantee in distributed deployments. Version numbers are monotonic, deterministic, and carry their correctness proof in the event store's append logic itself.

---

## L1: Technical Implementation

### Core Mechanism

Optimistic concurrency in event sourcing works by attaching an `expected_version` to every write operation. If the stream's actual version at write time does not match the expected version, the write is rejected with a conflict error — no lock held, no blocking.

```python
from eventsourcing.persistence import IntegrityError

# Load aggregate — captures version at read time
aggregate = app.repository.get(aggregate_id)
current_version = aggregate.version  # e.g., 5

# Apply command — increments version on the pending event
aggregate.do_something()

# Save — library enforces: stored version must still == 5
try:
    app.save(aggregate)
except IntegrityError:
    # Version mismatch: another writer committed between our read and write
    # Retry strategy: reload, reapply command, save again
    aggregate = app.repository.get(aggregate_id)
    aggregate.do_something()
    app.save(aggregate)
```

The `eventsourcing` library tracks `originator_version` on every event. When the infrastructure layer appends a new event, it checks that `originator_version == current_stream_version + 1`. If not, it raises `IntegrityError`. This check delegates to the database's transactional semantics (PostgreSQL, SQLite, etc.) — no application-level locking required.

### PostgreSQL-Native Version Guard

When building a custom event store on PostgreSQL, the version check is expressed as a conditional UPDATE:

```sql
UPDATE aggregates
    SET version = %(new_version)s
WHERE aggregate_uuid = %(aggregate_id)s
  AND version = %(expected_version)s;
-- If 0 rows affected: concurrent write detected -> raise ConcurrentStreamWriteError
```

This is atomic at the database level. The check-and-increment happens inside a single transaction. No application-level mutex, no SELECT FOR UPDATE, no advisory lock needed.

```python
from dataclasses import dataclass
from uuid import UUID
from typing import Sequence

@dataclass
class EventStream:
    aggregate_id: UUID
    events: list
    version: int  # version AT TIME OF READ — used as expected_version on next write

class ConcurrentStreamWriteError(Exception):
    pass

class EventStore:
    def load_stream(self, aggregate_id: UUID) -> EventStream:
        # Fetch events + current version from storage
        ...

    def append_to_stream(
        self,
        aggregate_id: UUID,
        events: Sequence,
        expected_version: int,  # must match current stored version
    ) -> None:
        rows_affected = self._conditional_version_update(
            aggregate_id, expected_version, expected_version + len(events)
        )
        if rows_affected == 0:
            raise ConcurrentStreamWriteError(
                f"Aggregate {aggregate_id} was modified. "
                f"Expected version {expected_version}."
            )
        self._insert_events(events)
```

### Retry Pattern

The retry pattern is the standard response to a `ConcurrentStreamWriteError`:

```python
import time
from functools import wraps

def with_optimistic_retry(max_attempts: int = 3, backoff_seconds: float = 0.1):
    """Decorator for command handlers that may encounter concurrency conflicts."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return fn(*args, **kwargs)
                except ConcurrentStreamWriteError:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(backoff_seconds * (2 ** attempt))  # exponential backoff
        return wrapper
    return decorator

@with_optimistic_retry(max_attempts=3)
def handle_cancel_order(order_id: UUID, event_store: EventStore) -> None:
    stream = event_store.load_stream(order_id)
    order = rebuild_from_events(stream.events)
    order.cancel()  # raises DomainError if business rules prevent cancellation
    event_store.append_to_stream(order_id, order.pending_events, stream.version)
```

### Using the `eventsourcing` Library Directly

```python
from eventsourcing.application import Application
from eventsourcing.domain import Aggregate, event

class Order(Aggregate):
    @event("OrderPlaced")
    def __init__(self, customer_id: str) -> None:
        self.customer_id = customer_id
        self.status = "placed"

    @event("OrderCancelled")
    def cancel(self) -> None:
        if self.status != "placed":
            raise ValueError("Only placed orders can be cancelled")
        self.status = "cancelled"

class OrderService(Application):
    def place_order(self, customer_id: str) -> str:
        order = Order(customer_id=customer_id)
        self.save(order)
        return str(order.id)

    def cancel_order(self, order_id: str) -> None:
        order = self.repository.get(order_id)
        order.cancel()
        self.save(order)  # raises IntegrityError on version conflict

# version is managed automatically; aggregate.version reflects event count
```

---

## L2: Trade-off Analysis

### Version Numbers vs. Timestamps: Definitive Comparison

| Criterion | Version Numbers | Timestamps |
|-----------|----------------|------------|
| **Correctness in distributed systems** | Guaranteed — monotonic, source of truth is the event store | Not guaranteed — clock skew between nodes causes false positives and missed conflicts |
| **Uniqueness guarantee** | Yes — stream version is strictly unique per aggregate stream | No — two events can share a timestamp at millisecond resolution |
| **Causal ordering** | Yes — version N always precedes version N+1 | No — NTP correction, leap seconds, and clock drift break causal ordering |
| **Implementation complexity** | Low — conditional UPDATE on integer column | Higher — requires hybrid logical clocks (HLCs) or vector clocks for correctness |
| **Conflict detection accuracy** | Exact — conflict detected iff and only iff a concurrent write occurred | Unreliable — clock skew can suppress or create false conflicts |
| **Debuggability** | High — version sequence is a direct audit trail | Low — timestamp values require clock synchronization context to interpret |
| **Library support (Python)** | Native in `eventsourcing` 9.x, all major event stores | Not natively supported; requires custom implementation |

### When Timestamps Appear Attractive (and Why to Resist)

Timestamps feel appealing because they carry temporal semantics — you can tell "when" something happened. In practice:

1. **Clock skew is real**: Even with NTP, nodes in a distributed system can diverge by tens to hundreds of milliseconds. Two writes that appear to have the same timestamp may have a genuine causal relationship that the timestamp cannot capture.
2. **Monotonicity is not guaranteed**: System clock rollbacks (NTP correction, daylight saving, VM migration) break the assumption that a later timestamp means a later event.
3. **Granularity collisions**: At microsecond resolution, concurrent writes on the same aggregate from the same host can produce identical timestamps.
4. **Research finding**: Academic study of timestamp granularity in OCC ([arXiv:1811.04967](https://arxiv.org/abs/1811.04967)) shows correctness degrades significantly as timestamp granularity coarsens relative to transaction duration.

If you need both temporal data and causal ordering, the correct pattern is: **store the version number as the concurrency guard AND store a wall-clock timestamp as metadata on each event for observability purposes.** These are orthogonal concerns.

### Architectural Recommendation

For a Python event-sourced system making an end-of-day decision:

1. **Use `eventsourcing` 9.5.x** — it handles the version tracking, IntegrityError signaling, and database adapter integration. Version numbers are built in; you do not implement them manually.
2. **If building a custom store on PostgreSQL** — use the conditional UPDATE pattern shown in L1. The `breadcrumbs collector` article documents this as the established PostgreSQL pattern for event-sourced systems.
3. **Do not use wall-clock timestamps as concurrency guards** — store them as event metadata (`created_at`) only.
4. **For the retry strategy** — exponential backoff with 3 attempts covers the vast majority of conflict scenarios in non-pathological write patterns. Persistent conflicts (beyond 3 attempts) indicate a design problem (too many writers on the same aggregate), not a concurrency strategy problem.

### Known Limitation to Disclose

Version-number OCC does not prevent all anomalies in aggregate designs that span multiple streams. If a command must be atomic across two aggregates, the version guard on each aggregate stream does not provide cross-stream atomicity. In that case, consider the Saga/Process Manager pattern or accept eventual consistency at the multi-aggregate boundary. This is a known architectural constraint of event sourcing, not a weakness of version-number OCC specifically.

---

## Sources

- [eventsourcing library documentation — Optimistic concurrency control example](https://eventsourcing.readthedocs.io/en/v3.1.0/topics/examples/concurrency.html)
- [eventsourcing library introduction (stable, 9.5.x)](https://eventsourcing.readthedocs.io/en/stable/topics/introduction.html)
- [GitHub: pyeventsourcing/eventsourcing](https://github.com/pyeventsourcing/eventsourcing)
- [Implementing Event Sourcing in Python part 2 — robust event store atop PostgreSQL](https://breadcrumbscollector.tech/implementing-event-sourcing-in-python-part-2-robust-event-store-atop-postgresql/)
- [Optimistic concurrency for pessimistic times — Event-Driven.io](https://event-driven.io/en/optimistic_concurrency_for_pessimistic_times/)
- [Event Sourcing and Concurrent Updates — Teiva Harsanyi (Medium)](https://teivah.medium.com/event-sourcing-and-concurrent-updates-32354ec26a4c)
- [Marten: Optimistic Concurrency documentation](https://martendb.io/documents/concurrency)
- [The Impact of Timestamp Granularity in Optimistic Concurrency Control — arXiv:1811.04967](https://arxiv.org/abs/1811.04967)
- [LinkedIn: Pros and cons of timestamps vs version numbers for OCC](https://www.linkedin.com/advice/3/what-pros-cons-using-timestamps-vs-version)
- [Timestamp-based concurrency control — Wikipedia](https://en.wikipedia.org/wiki/Timestamp-based_concurrency_control)
- [AWS Prescriptive Guidance: Event sourcing pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/event-sourcing.html)
