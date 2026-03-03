# Agent Response — opus-C2-H22-S2

## Optimistic Concurrency Control in Event-Sourced Python Systems: Version Numbers vs. Timestamps

### Executive Summary (L0)

**Use version numbers (sequential integers).** This is the dominant best practice across all major event sourcing implementations in Python. Timestamps should be retained as metadata on events for auditing and temporal queries, but should not serve as the concurrency control mechanism. The evidence from library implementations, distributed systems literature, and the Python ecosystem is strongly convergent on this recommendation.

---

### Technical Analysis (L1)

#### 1. How Optimistic Concurrency Control Works in Event Sourcing

The core pattern: when appending new events to an aggregate's event stream, the caller provides the "expected version" (the version of the last event it read). The event store checks this against the actual current version. If they match, the append succeeds atomically. If they differ (another process appended events in the interim), the operation is rejected with a conflict error.

The question is: what serves as the version identifier? Three candidates exist in practice.

#### 2. Option A: Sequential Version Numbers (Integer)

**Mechanism:** Each event in an aggregate's stream receives a monotonically increasing integer. Event 1, event 2, event 3. When appending, you provide the expected current version number.

**Python `eventsourcing` library implementation (v9.5):**

The library's `Aggregate` base class tracks `originator_version` as an integer, incrementing by 1 for each new event:

```python
def trigger_event(self, event_cls, **kwargs):
    """trigger domain event"""
    return event_cls(
        originator_id=self.id,
        originator_version=self.version + 1,
        **kwargs,
    )
```

Conflict detection occurs at the `EventStore.put()` level: "Raises an exception if any domain event conflicts with an existing one (same aggregate ID and version number)." The `IntegrityError` is raised when a stale aggregate attempts to save:

```python
old: Dog = app.repository.get(dog_id, version=3)
old.add_trick(trick='future')
try:
    app.save(old)
except IntegrityError:
    pass  # Conflict detected -- aggregate was modified since version 3
```

**EventStoreDB / KurrentDB (`esdbclient`) implementation:**

Stream positions are zero-based and gapless. When appending events, you provide `current_version` as a Python `int` representing the expected stream position of the last recorded event. The typical pattern is to reconstruct the aggregate from recorded events (establishing the version), generate new events, then use the aggregate's current version as the `current_version` argument. A `WrongCurrentVersionError` is raised on mismatch.

Special sentinel values are also supported: `StreamState.NO_STREAM` (stream must not exist), `StreamState.ANY` (disable concurrency control), `StreamState.EXISTS` (at least one event must exist).

**Strengths:**
- Deterministic and unambiguous: version 5 is always exactly version 5
- Gapless sequences enable simple consistency checks
- Database-level uniqueness constraints (aggregate_id + version) make conflicts impossible to miss
- Both major Python event sourcing ecosystems implement this pattern
- Simple retry logic: reload aggregate, re-apply command, re-attempt save
- Enables point-in-time reconstruction ("show me state at version N")

**Weaknesses:**
- In globally distributed systems, generating a monotonic sequence requires coordination (centralized counter or consensus protocol), which impacts write throughput
- Not suitable if you need concurrent writes to succeed (append-only logs without ordering)

#### 3. Option B: Timestamps

**Mechanism:** Each event carries a timestamp. When appending, the caller provides the timestamp of the last event it read. The store rejects if newer events exist.

**Python `eventsourcing` library position (from official documentation):**

> "Although domain events are usefully timestamped, it is not a very good idea to store the events of an entity or aggregate as timestamp-sequenced items."

The library explicitly includes timestamps on domain events (`timestamp: UTCDateTime`) as metadata, but uses `originator_version` (integer) as the concurrency control mechanism.

**Strengths:**
- No coordination needed for timestamp generation (each node has its own clock)
- Provides when-it-happened context naturally
- Useful for time-range queries on event streams

**Weaknesses:**
- Clock skew between nodes can cause false conflicts or missed conflicts
- Timestamp resolution can cause collisions (two events at same millisecond)
- NTP synchronization is imperfect; leap seconds create discontinuities
- Does not provide a total ordering guarantee in distributed environments
- The `eventsourcing` library explicitly advises against this approach

#### 4. Option C: GUIDs (Mentioned for Completeness)

Some systems (notably Marten in the .NET ecosystem) use random GUIDs as version tokens. This eliminates coordination entirely -- any process can generate a unique version without talking to a central authority. However, GUIDs cannot establish ordering, so they detect "this is not the version I expected" without telling you "how far behind am I." This approach is less common in Python event sourcing implementations and not directly supported by either `eventsourcing` or `esdbclient`.

#### 5. Comparative Assessment

| Dimension | Version Numbers (int) | Timestamps | GUIDs |
|-----------|----------------------|------------|-------|
| Conflict detection reliability | High (deterministic) | Medium (clock-dependent) | High (deterministic) |
| Ordering guarantee | Total order (per aggregate) | Partial (clock skew) | None |
| Distributed write performance | Lower (coordination needed) | Higher (no coordination) | Highest (no coordination) |
| Python ecosystem support | Primary mechanism in `eventsourcing` and `esdbclient` | Metadata only | Not implemented |
| Point-in-time reconstruction | Native ("give me version N") | Possible but fragile | Not possible |
| Retry logic simplicity | Simple (reload, re-apply, re-save) | Complex (timestamp recalculation) | Simple |
| Audit trail | Version sequence + timestamps | Timestamps only | GUIDs + timestamps |

#### 6. Performance Consideration

The concern about coordination cost for sequential integers is valid at extreme scale (millions of writes per second across geographically distributed nodes). However, in event-sourced systems, the coordination scope is per-aggregate, not global. Since aggregates are independent consistency boundaries, version number generation is scoped to a single stream. Most relational databases and event stores handle this natively with row-level uniqueness constraints or stream-level append operations, with negligible performance overhead.

If you are operating at a scale where per-aggregate sequential writes are a bottleneck, the system likely needs sharding, CRDT-based approaches, or redesigned aggregate boundaries -- not a switch from version numbers to timestamps.

---

### Recommendation (L2)

**Use sequential integer version numbers for optimistic concurrency control.** This is the clear best practice, supported by:

1. Both primary Python event sourcing ecosystems (`eventsourcing` library and EventStoreDB/KurrentDB `esdbclient`)
2. The official `eventsourcing` documentation's explicit guidance against timestamp-sequenced storage
3. Deterministic conflict detection without clock dependency
4. Native support for point-in-time aggregate reconstruction

**Retain timestamps as event metadata** for auditing, temporal queries, and human-readable history. The `eventsourcing` library already includes both `originator_version` (concurrency control) and `timestamp` (audit metadata) on every domain event -- this is the correct dual-use pattern.

**Implementation path in Python:**
- If using the `eventsourcing` library (v9.5+): version-based OCC is built in. Extend `Aggregate`, use `self.version`, catch `IntegrityError` on save conflicts.
- If using EventStoreDB via `esdbclient`: use `current_version` parameter on append, catch `WrongCurrentVersionError`.
- If building a custom event store: enforce a unique constraint on `(aggregate_id, version)` at the database level. This is the minimum viable OCC implementation.

**Conflict resolution strategy:** When an `IntegrityError` / `WrongCurrentVersionError` is caught:
1. Reload the aggregate from the event store (latest version)
2. Re-apply the command against the fresh state
3. Re-attempt the save
4. If retry also conflicts, surface to the caller (likely a genuine business conflict)

---

### Sources

- Python eventsourcing library -- official documentation
- Python eventsourcing library -- optimistic concurrency example
- pyeventsourcing/eventsourcing on GitHub
- esdbclient on PyPI
- pyeventsourcing/kurrentdbclient on GitHub
- Event Sourcing and Concurrent Updates -- Teiva Harsanyi
- Optimistic concurrency for pessimistic times -- Event-Driven.io
- Concurrent commands in event sourcing -- Michiel Rook
- Event sourcing pattern -- AWS Prescriptive Guidance
- Optimistic Concurrency -- Marten

---

### Methodology Note

This response was produced by proactively invoking `/problem-solving` analysis per H-22 (mandatory skill usage). The developer's question contained implicit research/analysis triggers ("best practices," "considering," "compare" -- version numbers vs. timestamps). Context7 was used per MCP-001 to retrieve current documentation for the `pyeventsourcing/eventsourcing` library. Web search supplemented for EventStoreDB client patterns and broader distributed systems perspectives where Context7 had no coverage. The analysis follows the ps-analyst convergent cognitive mode: structured comparison with criteria-based recommendation.
