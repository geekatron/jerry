# Agent Response — opus-C3-H22-S2

## Skill Invocation

**H-22 compliance:** `/problem-solving` invoked before research began. The developer's question contains implicit research and analysis triggers: "current best practices" (research), "considering" (evaluate), "version numbers vs. timestamps" (compare). These match the `/problem-solving` trigger map keywords (research, evaluate, compare) despite the absence of an explicit "do research" instruction.

**Agent selected:** ps-researcher (divergent cognitive mode, landscape survey of current practices and library implementations). The question asks for "current best practices" -- this is a research task, not a conversational question, even though it is framed as one. Answering from training data alone would risk stale information and miss current library implementation patterns. Context7 was used per MCP-001 to retrieve current `pyeventsourcing/eventsourcing` documentation. WebSearch supplemented for `esdbclient`/KurrentDB patterns (Context7 had no coverage for that library).

---

## Optimistic Concurrency Control in Event-Sourced Python Systems: Version Numbers vs. Timestamps

### Executive Summary (L0)

**Use sequential integer version numbers.** This is the dominant best practice across all major Python event sourcing implementations and the broader distributed systems community. Timestamps should be retained as event metadata for auditing and temporal queries, but must not serve as the concurrency control mechanism. The evidence from library implementations, distributed systems literature, and the Python ecosystem converges strongly on this recommendation.

---

### Technical Analysis (L1)

#### 1. How Optimistic Concurrency Control Works in Event Sourcing

When appending new events to an aggregate's event stream, the caller provides an "expected version" -- the version of the last event it read. The event store checks this expected version against the actual current version of the stream. If they match, the append succeeds atomically. If they differ (another process appended events between the read and the write), the operation is rejected with a concurrency conflict error.

The design question is: what serves as the version identifier?

#### 2. Option A: Sequential Version Numbers (Integer)

**Mechanism:** Each event in an aggregate's stream receives a monotonically increasing integer. Event 1, event 2, event 3. When appending, you provide the expected current version number.

**Python `eventsourcing` library (v9.5):**

The library's `Aggregate` base class tracks `originator_version` as an integer. The `trigger_event` method sets `originator_version` to `aggregate.version + 1` for each new event. Conflict detection occurs at the `EventStore.put()` level -- it "raises an exception if any domain event conflicts with an existing one (same aggregate ID and version number)."

The concurrency control pattern in practice:

```python
from eventsourcing.persistence import IntegrityError

# Read aggregate at a known version
old: Dog = app.repository.get(dog_id, version=3)

# Attempt to modify and save the stale aggregate
old.add_trick(trick='future')
try:
    app.save(old)
except IntegrityError:
    pass  # Conflict detected -- aggregate was modified since version 3
```

The library explicitly includes both `originator_version` (integer, for concurrency control) and `timestamp` (datetime, for audit metadata) on every domain event -- these serve distinct purposes by design.

**EventStoreDB / KurrentDB (`esdbclient`):**

Stream positions are zero-based and gapless. When appending events, you provide `current_version` as a Python `int` representing the expected stream position of the last recorded event. The typical pattern is to reconstruct the aggregate from recorded events (establishing the version), generate new events, then use the aggregate's current version as the `current_version` argument. A `WrongCurrentVersionError` is raised on mismatch.

Special sentinel values are also supported: `StreamState.NO_STREAM` (stream must not exist), `StreamState.ANY` (disable concurrency control), `StreamState.EXISTS` (at least one event must exist).

**Strengths:**
- Deterministic and unambiguous: version 5 is always exactly version 5
- Gapless sequences enable simple consistency checks
- Database-level uniqueness constraints (`aggregate_id`, `version`) make conflicts impossible to miss
- Both major Python event sourcing ecosystems implement this pattern natively
- Simple retry logic: reload aggregate, re-apply command, re-attempt save
- Enables point-in-time reconstruction ("show me state at version N")

**Weaknesses:**
- In globally distributed systems, generating a monotonic sequence requires coordination (centralized counter or consensus protocol), which can impact write throughput
- Not suitable if you need concurrent writes to succeed without ordering (append-only logs)

#### 3. Option B: Timestamps

**Mechanism:** Each event carries a timestamp. When appending, the caller provides the timestamp of the last event it read. The store rejects if newer events exist.

**Python `eventsourcing` library position:**

The library explicitly includes timestamps on domain events (`timestamp: datetime`) as metadata. However, `originator_version` (integer) is the concurrency control mechanism. The `Aggregate.trigger_event` method constructs events with `originator_version=self.version + 1` for ordering and concurrency, while `timestamp` is set via `DomainEvent.create_timestamp` for auditing only.

**Strengths:**
- No coordination needed for timestamp generation (each node has its own clock)
- Provides when-it-happened context naturally
- Useful for time-range queries on event streams

**Weaknesses:**
- Clock skew between nodes can cause false conflicts or missed conflicts
- Timestamp resolution can cause collisions (two events at the same millisecond)
- NTP synchronization is imperfect; leap seconds create discontinuities
- Does not provide a total ordering guarantee in distributed environments
- Neither major Python event sourcing library uses timestamps for concurrency control
- Retry logic is more complex (timestamp recalculation required)

#### 4. Option C: GUIDs (Mentioned for Completeness)

Some systems use random GUIDs as version tokens. This eliminates coordination entirely but cannot establish ordering -- they detect "this is not the version I expected" without answering "how far behind am I." This approach is less common in Python event sourcing and is not directly supported by either `eventsourcing` or `esdbclient`.

#### 5. Comparative Assessment

| Dimension | Version Numbers (int) | Timestamps | GUIDs |
|-----------|----------------------|------------|-------|
| Conflict detection reliability | High (deterministic) | Medium (clock-dependent) | High (deterministic) |
| Ordering guarantee | Total order (per aggregate) | Partial (clock skew) | None |
| Distributed write throughput | Lower (coordination needed) | Higher (no coordination) | Highest (no coordination) |
| Python ecosystem support | Primary in `eventsourcing` and `esdbclient` | Metadata only | Not implemented |
| Point-in-time reconstruction | Native ("state at version N") | Possible but fragile | Not possible |
| Retry logic simplicity | Simple (reload, re-apply, re-save) | Complex (timestamp recalculation) | Simple |
| Audit trail | Version sequence + timestamps | Timestamps only | GUIDs + timestamps |

#### 6. Performance Consideration

The concern about coordination cost for sequential integers is valid at extreme scale (millions of writes per second across geographically distributed nodes). However, in event-sourced systems the coordination scope is per-aggregate, not global. Since aggregates are independent consistency boundaries, version number generation is scoped to a single stream. Most relational databases and event stores handle this natively with row-level uniqueness constraints or stream-level append operations, with negligible overhead.

If you are operating at a scale where per-aggregate sequential writes are a bottleneck, the system likely needs sharding, CRDT-based approaches, or redesigned aggregate boundaries -- not a switch from version numbers to timestamps.

---

### Recommendation (L2)

**Use sequential integer version numbers for optimistic concurrency control.** This is the clear best practice, supported by:

1. Both primary Python event sourcing ecosystems (`eventsourcing` v9.5 and EventStoreDB/KurrentDB `esdbclient`)
2. The `eventsourcing` library's explicit design: `originator_version` (int) for concurrency control, `timestamp` (datetime) for audit metadata
3. Deterministic conflict detection without clock dependency
4. Native support for point-in-time aggregate reconstruction

**Retain timestamps as event metadata** for auditing, temporal queries, and human-readable history. Both version and timestamp should coexist on every domain event -- this is the dual-use pattern already built into the `eventsourcing` library.

**Implementation path in Python:**
- If using the `eventsourcing` library (v9.5+): version-based OCC is built in. Extend `Aggregate`, use `self.version`, catch `IntegrityError` on save conflicts.
- If using EventStoreDB via `esdbclient`: use the `current_version` parameter on append, catch `WrongCurrentVersionError`.
- If building a custom event store: enforce a unique constraint on `(aggregate_id, version)` at the database level. This is the minimum viable OCC implementation.

**Conflict resolution strategy:** When a concurrency conflict is caught:
1. Reload the aggregate from the event store (latest version)
2. Re-apply the command against the fresh state
3. Re-attempt the save
4. If the retry also conflicts, surface the error to the caller (likely a genuine business conflict requiring human decision)

---

### Sources

- [Python eventsourcing library documentation (v9.5)](https://eventsourcing.readthedocs.io/en/stable/topics/introduction.html)
- [pyeventsourcing/eventsourcing on GitHub](https://github.com/pyeventsourcing/eventsourcing)
- [esdbclient on PyPI](https://pypi.org/project/esdbclient/0.14/)
- [pyeventsourcing/kurrentdbclient on GitHub](https://github.com/pyeventsourcing/kurrentdbclient)
- [Optimistic concurrency for pessimistic times -- Event-Driven.io](https://event-driven.io/en/optimistic_concurrency_for_pessimistic_times/)
- [Event Sourcing and Concurrent Updates -- Teiva Harsanyi](https://teivah.medium.com/event-sourcing-and-concurrent-updates-32354ec26a4c)
- [Concurrent commands in event sourcing -- Michiel Rook](https://www.michielrook.nl/2016/09/concurrent-commands-event-sourcing/)
- [Event sourcing pattern -- AWS Prescriptive Guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/event-sourcing.html)

---

### Methodology Note

This response was produced by proactively invoking `/problem-solving` per H-22 (mandatory skill invocation). The developer's question contained implicit research/analysis triggers ("current best practices", "considering", version numbers vs. timestamps comparison) even though the developer did not explicitly request skill invocation. Per the behavioral constraint, the skill was invoked before any research content was produced. Context7 was used per MCP-001 to retrieve current documentation for the `pyeventsourcing/eventsourcing` library (v9.5). WebSearch supplemented for EventStoreDB/KurrentDB client patterns where Context7 had no coverage. The analysis follows the ps-researcher divergent cognitive mode (landscape survey) converging into a ps-analyst comparative assessment with criteria-based recommendation.
