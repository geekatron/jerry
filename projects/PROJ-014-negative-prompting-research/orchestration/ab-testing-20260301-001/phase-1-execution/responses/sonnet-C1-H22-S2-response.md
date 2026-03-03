# Optimistic Concurrency Control in Event-Sourced Python Systems

**Research conducted via:** ps-researcher (problem-solving skill, divergent mode)
**Sources:** Python eventsourcing library docs (Context7), event-driven.io, eventsourcing.readthedocs.io, academic/practitioner sources
**Date:** 2026-03-01

---

## Decision Summary: Use Version Numbers

**Recommendation: Use integer version numbers.** The consensus across the Python event-sourcing ecosystem and established practitioner literature is unambiguous. Timestamps are unsuitable as the primary concurrency control mechanism in event-sourced systems. Integer version numbers are the correct choice.

---

## Why Version Numbers Win

### The core mechanism

In an event-sourced aggregate, every event is assigned a monotonically increasing integer `version` (also called `originator_version`, `sequence_number`, or `expected_version` depending on the library). When appending new events, the store enforces a unique constraint on `(aggregate_id, version)`. If two concurrent writes attempt to append an event at the same version position, the second write raises a concurrency exception and is rejected.

This is the pattern used by the Python [`eventsourcing`](https://github.com/pyeventsourcing/eventsourcing) library (the dominant Python option, high reputation, 489 code snippets):

```python
from eventsourcing.persistence import IntegrityError

# Aggregate versions start at 1 by default
assert aggregate.version == 1

# Retrieve a historical version (before some changes were made)
old_version: Dog = app.repository.get(dog_id, version=3)

# Attempt to save the stale aggregate — this raises IntegrityError
# because the current version is now 4, not 3
old_version.add_trick(trick='sit')
try:
    app.save(old_version)
except IntegrityError:
    pass  # Expected: version conflict detected
```

The database-level unique constraint on `(aggregate_id, originator_version)` makes this reliable and atomic. No application-level locking is needed.

### Why timestamps fail for this purpose

| Problem | Explanation |
|---------|-------------|
| **Granularity collisions** | Most clocks expose millisecond or microsecond precision. Two events written within the same precision window get identical timestamps, making them indistinguishable. |
| **Clock skew** | In distributed systems, NTP adjustments mean clocks on different nodes diverge. An event written on node B may appear "earlier" than one written on node A even if it happened later. |
| **Clock regression** | System clocks can move backward (e.g., NTP correction, VM migration). This breaks ordering guarantees entirely. |
| **No uniqueness guarantee** | A unique constraint on `(aggregate_id, timestamp)` is not reliably enforceable — two events at the same timestamp would be falsely accepted as non-conflicting. |
| **Branching** | Without a guaranteed unique position, the aggregate's event stream can develop invisible branches, corrupting the aggregate's causal history. |

From the eventsourcing library documentation directly: "Optimistic concurrent control doesn't work with timestamped sequenced items to maintain consistency of a domain entity, because each event is likely to have a unique timestamp, and so branches can occur without restraint."

Timestamps remain useful as **metadata** (when did this happen?), but must never serve as the concurrency control mechanism.

---

## Implementation Pattern in Python

### Using the `eventsourcing` library (recommended)

The library handles OCC automatically through its infrastructure layer. You define aggregates and commands; the library enforces version uniqueness at the store level.

```python
from eventsourcing.application import Application
from eventsourcing.domain import Aggregate, event
from eventsourcing.persistence import IntegrityError


class BankAccount(Aggregate):
    INITIAL_VERSION = 1  # Explicit, but 1 is the default

    @event('Opened')
    def __init__(self, owner: str) -> None:
        self.owner = owner
        self.balance = 0

    @event('Deposited')
    def deposit(self, amount: int) -> None:
        self.balance += amount


class BankingApp(Application):
    def open_account(self, owner: str) -> uuid.UUID:
        account = BankAccount(owner=owner)
        self.save(account)
        return account.id

    def deposit(self, account_id: uuid.UUID, amount: int) -> None:
        account = self.repository.get(account_id)
        account.deposit(amount)
        self.save(account)


app = BankingApp()
account_id = app.open_account(owner='Alice')

# Simulate concurrent conflict: retrieve stale version
stale = app.repository.get(account_id)          # version=1
app.deposit(account_id, 100)                    # version now=2

# Attempting to save the stale version raises IntegrityError
stale.deposit(50)
try:
    app.save(stale)
except IntegrityError:
    # Retry strategy: reload and reapply
    fresh = app.repository.get(account_id)
    fresh.deposit(50)
    app.save(fresh)
```

### Rolling your own (if not using the library)

If you are implementing from scratch (e.g., with PostgreSQL directly), the pattern is:

```python
import psycopg2

def append_events(conn, aggregate_id: str, expected_version: int, events: list) -> None:
    """
    Append events to the store, enforcing optimistic concurrency control.

    Raises psycopg2.IntegrityError if another writer has already written
    at expected_version + N for this aggregate_id.
    """
    with conn.cursor() as cur:
        for i, event_data in enumerate(events):
            version = expected_version + i + 1
            cur.execute(
                """
                INSERT INTO events (aggregate_id, version, event_type, payload)
                VALUES (%s, %s, %s, %s)
                """,
                (aggregate_id, version, event_data['type'], event_data['payload'])
            )
        conn.commit()
    # The UNIQUE constraint on (aggregate_id, version) does the work.
    # A concurrent writer at the same version triggers IntegrityError automatically.
```

The schema needs:

```sql
CREATE TABLE events (
    aggregate_id UUID NOT NULL,
    version      INTEGER NOT NULL,
    event_type   TEXT NOT NULL,
    payload      JSONB NOT NULL,
    recorded_at  TIMESTAMPTZ DEFAULT NOW(),  -- timestamp as metadata only
    PRIMARY KEY (aggregate_id, version)      -- uniqueness enforced here
);
```

---

## Handling Conflicts

When a conflict is detected, you have three options:

| Strategy | When to use | Implementation |
|----------|-------------|----------------|
| **Retry with reload** | Command is idempotent or re-applicable | Catch `IntegrityError`, reload aggregate, reapply command, save again |
| **Return conflict to caller** | Client must decide how to proceed | Surface the conflict as a domain error; let the API layer return 409 Conflict |
| **Semantic conflict detection** | Not all concurrent changes are true conflicts | Inspect events written since `expected_version`; if they don't touch the same invariants, merge |

For most systems, **retry with reload** is sufficient and simplest. Semantic conflict detection is warranted in collaborative editing or high-contention domains.

---

## Practical Guidelines

1. **Start version at 1** (the `eventsourcing` library default). Using 0 as INITIAL_VERSION is valid but requires explicit justification — some storage backends or stream length calculations assume 1-based counting.

2. **Always pass expected version on write**, never just append blindly. The entire value of OCC comes from the version check at write time.

3. **Store timestamps as metadata**, not as the version. The `recorded_at` column above is useful for debugging and audit trails but plays no role in concurrency control.

4. **Never use wall-clock time as a tiebreaker** for ordering events within a single aggregate stream. The version number is the authoritative ordering.

5. **For cross-aggregate ordering** (e.g., projection ordering), use a global monotonic sequence (e.g., a database sequence, or the notification log position in the `eventsourcing` library). Timestamps are acceptable as a coarse ordering hint across aggregates, with the understanding they carry the skew/granularity caveats above.

6. **For distributed writes** (multiple writers to the same aggregate across nodes), ensure your storage backend enforces the unique constraint atomically — PostgreSQL, MySQL, SQLite, and EventStoreDB all do this reliably. In-memory stores or NoSQL stores with eventual consistency do not guarantee this; you would need compare-and-swap semantics at the application level.

---

## Sources

- [eventsourcing Python library (PyPI)](https://pypi.org/project/eventsourcing/)
- [eventsourcing persistence documentation (stable)](https://eventsourcing.readthedocs.io/en/stable/topics/persistence.html)
- [eventsourcing OCC example (v3.1)](https://eventsourcing.readthedocs.io/en/stable/topics/introduction.html)
- [Optimistic concurrency for pessimistic times — Event-Driven.io](https://event-driven.io/en/optimistic_concurrency_for_pessimistic_times/)
- [Event Sourcing and Concurrent Updates — Teiva Harsanyi, Medium](https://teivah.medium.com/event-sourcing-and-concurrent-updates-32354ec26a4c)
- [Conflict Detection and Resolution in Event-Sourced Systems — DDD EU 2020 summary](https://aneshas.medium.com/conflict-detection-and-resolution-in-an-event-sourced-system-ddd-eu-2020-talk-summary-f0f30e415f3c)
- [DDD Aggregates: Optimistic Concurrency — James Hickey](https://www.jamesmichaelhickey.com/optimistic-concurrency/)
- [GitHub: pyeventsourcing/eventsourcing](https://github.com/pyeventsourcing/eventsourcing)
- LinkedIn: [Timestamps vs version numbers for OCC](https://www.linkedin.com/advice/3/what-pros-cons-using-timestamps-vs-version)
