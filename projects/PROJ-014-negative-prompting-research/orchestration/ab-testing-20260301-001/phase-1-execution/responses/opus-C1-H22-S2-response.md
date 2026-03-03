# Optimistic Concurrency Control in Event-Sourced Python Systems: Version Numbers vs. Timestamps

## L0: Executive Summary

**Recommendation: Use version numbers (sequential integers), not timestamps.**

Version numbers are the industry-standard approach for optimistic concurrency control (OCC) in event-sourced systems. Every major event store implementation -- EventStoreDB/KurrentDB, the Python `eventsourcing` library, Marten, Axon -- uses sequential integer version numbers as the primary concurrency mechanism. Timestamps are unsuitable as a primary OCC mechanism due to clock skew, NTP drift, and non-monotonic system clock behavior, but serve well as supplementary metadata for auditing and debugging.

For your end-of-day decision: go with version numbers. The remainder of this document provides the technical rationale, implementation patterns, and Python-specific guidance to support that decision.

---

## L1: Technical Analysis

### How Optimistic Concurrency Control Works in Event Sourcing

In an event-sourced system, all state changes are captured as an ordered sequence of domain events appended to a stream (typically one stream per aggregate). OCC protects aggregate consistency by detecting concurrent writes at append time rather than locking at read time.

The core protocol:

1. **Load** the aggregate by replaying its event stream. Record the current stream position (version).
2. **Execute** the command against the in-memory aggregate, producing new domain events.
3. **Append** the new events to the stream, passing the `expected_version` from step 1.
4. **Validate** at the store level: if the actual current version differs from `expected_version`, reject the write with a concurrency error.
5. **Retry** (optional): reload the aggregate at its current version and re-execute the command.

### Version Numbers: The Standard Approach

Version numbers are gapless, strictly increasing integers that track the position of events within a stream. Each new event increments the version by exactly one.

**Why version numbers work:**

| Property | Benefit |
|----------|---------|
| Deterministic ordering | No ambiguity about event sequence within a stream |
| Gapless sequence | Missing versions are immediately detectable as data corruption |
| Database-enforceable | Unique constraint on `(stream_id, version)` provides atomic conflict detection |
| No external dependencies | No reliance on system clocks, NTP, or time synchronization |
| Efficient comparison | Integer equality check is the cheapest possible conflict detection |

**Implementation in Python with the `eventsourcing` library (v9.5.3):**

The `eventsourcing` library implements OCC through its aggregate versioning system. When an aggregate is loaded from the repository, it carries a `version` attribute representing the count of events applied. On save, the library uses a database-level unique constraint to prevent two events from occupying the same version position:

```python
from eventsourcing.application import Application
from eventsourcing.domain import Aggregate, event
from eventsourcing.persistence import IntegrityError

class ShoppingCart(Aggregate):
    def __init__(self):
        self.items = []

    @event("ItemAdded")
    def add_item(self, item_name: str, quantity: int):
        self.items.append({"name": item_name, "quantity": quantity})

class ShoppingApp(Application):
    def create_cart(self) -> str:
        cart = ShoppingCart()
        self.save(cart)
        return cart.id

    def add_item(self, cart_id, item_name: str, quantity: int):
        cart = self.repository.get(cart_id)
        cart.add_item(item_name=item_name, quantity=quantity)
        self.save(cart)

# Concurrency detection in action:
app = ShoppingApp()
cart_id = app.create_cart()

# Load the same aggregate at version 1 (two "sessions")
cart_v1a = app.repository.get(cart_id)  # version == 1
cart_v1b = app.repository.get(cart_id)  # version == 1

# First write succeeds -- version goes from 1 to 2
cart_v1a.add_item(item_name="Widget", quantity=1)
app.save(cart_v1a)  # OK

# Second write from stale version fails
cart_v1b.add_item(item_name="Gadget", quantity=2)
try:
    app.save(cart_v1b)  # Raises IntegrityError -- expected version 1, actual is 2
except IntegrityError:
    # Reload and retry
    cart_current = app.repository.get(cart_id)
    cart_current.add_item(item_name="Gadget", quantity=2)
    app.save(cart_current)  # Succeeds at version 3
```

**Implementation with EventStoreDB/KurrentDB via `kurrentdbclient`:**

The KurrentDB Python client (successor to `esdbclient`) uses `expected_position` (equivalent to version) for OCC:

```python
# When appending events, pass the expected stream position.
# If actual position != expected position, ExpectedPositionError is raised.
#
# StreamState.NO_STREAM  -- stream must not exist
# StreamState.ANY        -- disable concurrency check
# StreamState.EXISTS     -- stream must have at least one event
# integer                -- exact expected position
```

**Implementation with PostgreSQL (custom event store):**

A common pattern for Python teams building on PostgreSQL uses an `aggregates` table with a version column and conditional UPDATE for conflict detection:

```sql
CREATE TABLE aggregates (
    uuid VARCHAR(36) NOT NULL PRIMARY KEY,
    version INT NOT NULL DEFAULT 1
);

CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    aggregate_uuid VARCHAR(36) NOT NULL REFERENCES aggregates(uuid),
    version INT NOT NULL,
    event_type VARCHAR(255) NOT NULL,
    data JSONB NOT NULL,
    UNIQUE (aggregate_uuid, version)
);
```

The append operation uses a conditional update:

```sql
-- Attempt to increment version; fails if concurrent write already incremented it
UPDATE aggregates SET version = :new_version
WHERE uuid = :aggregate_uuid AND version = :expected_version;

-- If rows_affected == 1: proceed with INSERT INTO events
-- If rows_affected == 0: raise ConcurrentStreamWriteError
```

### Timestamps: Why They Fall Short as Primary OCC

Timestamps are unreliable as a primary concurrency control mechanism for several well-documented reasons:

| Problem | Impact on OCC |
|---------|---------------|
| **Clock skew** | Different nodes in a distributed system have different clock values. Two events written "at the same time" may have timestamps that imply incorrect ordering. |
| **NTP drift and backward jumps** | System clocks are periodically adjusted by NTP. Clocks can jump backward, producing non-monotonic sequences. A "later" event may receive an "earlier" timestamp. |
| **Granularity collisions** | Two events within the same millisecond (or microsecond, depending on clock resolution) produce identical timestamps, making conflict detection impossible. |
| **No gap detection** | Unlike sequential integers, timestamps have no expected "next value," so missing events are not detectable through the sequence alone. |
| **Cross-system inconsistency** | In microservice architectures, each service has its own clock. Timestamps from different services are not directly comparable for ordering. |

**When timestamps are useful** (as supplementary metadata):

- **Audit trails**: Recording when an event was persisted for human-readable logs.
- **Time-based queries**: "Show me all events from the last 24 hours."
- **Debugging**: Correlating events with external system logs.
- **TTL/expiration**: Determining if snapshots or projections are stale.

Best practice: store timestamps alongside version numbers, but use version numbers for concurrency control.

### Hybrid Approaches

Some systems use both mechanisms:

| Approach | Use Case |
|----------|----------|
| **Version for writes, timestamp for reads** | Version numbers enforce write consistency; timestamps enable time-range queries on projections. |
| **Lamport timestamps** | Logical clocks that increment on every event and on every message received. More reliable than wall-clock time for distributed ordering, but still less suitable than stream-scoped version numbers for single-aggregate OCC. |
| **Vector clocks** | Track causal ordering across multiple nodes. Useful for detecting concurrent writes in multi-leader replication, but add significant complexity. Overkill for single-aggregate event streams. |

### Conflict Resolution Strategies

When a concurrency conflict is detected (version mismatch), you have several resolution options:

| Strategy | Description | When to Use |
|----------|-------------|-------------|
| **Retry with reload** | Reload aggregate at current version, re-execute command, re-append. Simplest and most common. | Commands are idempotent or stateless (e.g., "add item to cart"). |
| **Merge** | Inspect conflicting events and determine if they are compatible (non-conflicting fields). | Domain-specific: e.g., two users editing different sections of a document. |
| **Conflict event types blacklist** | Maintain a registry of event type pairs that conflict. Only reject when conflicting types collide. | Systems with many independent aggregate properties that rarely interact. |
| **Last-writer-wins** | Accept the latest write unconditionally. | Low-value data where correctness is less critical than availability. Generally not recommended for event-sourced systems. |
| **User resolution** | Surface the conflict to the user for manual resolution. | Collaborative editing, approval workflows. |

The retry-with-reload strategy is the recommended default for most Python event-sourced systems.

---

## L2: Decision Framework

### Recommendation Matrix

| Criterion | Version Numbers | Timestamps |
|-----------|----------------|------------|
| Conflict detection reliability | Strong -- deterministic, gap-free | Weak -- clock skew, granularity limits |
| Implementation complexity | Low -- integer comparison | Medium -- clock synchronization needed |
| Library/framework support | Universal -- all major event stores | Partial -- typically supplementary only |
| Distributed system safety | Safe -- no external clock dependency | Unsafe without logical clocks |
| Auditability | Good -- sequence is verifiable | Good -- human-readable time values |
| Performance | Optimal -- integer comparison | Comparable for single writes |

### Decision: Use Version Numbers

For your Python event-sourced system, use sequential integer version numbers as the primary OCC mechanism. Store wall-clock timestamps as supplementary event metadata for auditing and debugging.

### Recommended Implementation Path

1. **If using an existing library**: adopt `eventsourcing` (v9.5.3, released January 2026) which provides built-in OCC via aggregate versioning and `IntegrityError` on conflicts. For EventStoreDB/KurrentDB backends, use `kurrentdbclient` which exposes `expected_position` for OCC.

2. **If building a custom event store on PostgreSQL**: use the `aggregates` table pattern with conditional `UPDATE ... WHERE version = :expected` and a unique constraint on `(stream_id, version)` in the events table.

3. **Conflict resolution**: start with retry-with-reload. Add domain-specific merge logic only when you have concrete use cases that require it.

4. **Timestamps**: add a `created_at` column to your events table populated with `datetime.now(timezone.utc)`. Use it for queries and debugging, not for concurrency control.

---

## Sources

- [Python eventsourcing library (v9.5.3) -- Introduction](https://eventsourcing.readthedocs.io/en/stable/topics/introduction.html)
- [Python eventsourcing library -- PyPI](https://pypi.org/project/eventsourcing/)
- [Python eventsourcing -- GitHub](https://github.com/pyeventsourcing/eventsourcing)
- [KurrentDB Python client (kurrentdbclient) -- GitHub](https://github.com/pyeventsourcing/kurrentdbclient)
- [esdbclient (EventStoreDB Python client) -- PyPI](https://pypi.org/project/esdbclient/0.14/)
- [Implementing Event Sourcing in Python -- Robust Event Store atop PostgreSQL](https://breadcrumbscollector.tech/implementing-event-sourcing-in-python-part-2-robust-event-store-atop-postgresql/)
- [Optimistic Concurrency for Pessimistic Times -- Event-Driven.io](https://event-driven.io/en/optimistic_concurrency_for_pessimistic_times/)
- [Simple Event Sourcing: Consistency (Part 2) -- Zilverline](https://www.zilverline.com/blog/simple-event-sourcing-consistency-part-2)
- [Event Sourcing and Concurrent Updates -- Teiva Harsanyi](https://teivah.medium.com/event-sourcing-and-concurrent-updates-32354ec26a4c)
- [Concurrent Commands in Event Sourcing -- Michiel Rook](https://www.michielrook.nl/2016/09/concurrent-commands-event-sourcing/)
- [Event Sourcing Pattern -- AWS Prescriptive Guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/event-sourcing.html)
- [Event Sourcing Pattern -- Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing)
- [Optimistic Concurrency Control: A Practical Guide for 2025 -- Shadecoder](https://www.shadecoder.com/topics/optimistic-concurrency-control-a-practical-guide-for-2025)

---

*Research conducted via `/problem-solving` with ps-researcher cognitive mode. Data sources: Context7 (eventsourcing library documentation), WebSearch, WebFetch. Criticality: C1 (routine research, reversible in one session). Self-review (S-010) applied before output.*
