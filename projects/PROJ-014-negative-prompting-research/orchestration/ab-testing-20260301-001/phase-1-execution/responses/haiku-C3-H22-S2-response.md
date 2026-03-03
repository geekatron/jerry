# Response: Optimistic Concurrency Control in Event-Sourced Systems

## Skill Invocation

This question requires research into current best practices for implementing optimistic concurrency control in event-sourced systems using Python, specifically comparing version numbers vs. timestamps for conflict resolution.

```
Use /problem-solving with ps-researcher to survey optimistic concurrency
control patterns for event-sourced Python systems.

Focus areas:
- Version number-based conflict detection in event sourcing
- Timestamp-based conflict detection approaches
- Trade-offs between the two approaches (latency, complexity, consistency guarantees)
- Current implementations in Python event sourcing libraries (EventSourcing, Eventsourcing, etc.)
- Best practices from 2024-2026 literature and production deployments

Data source: Web search (WebSearch and Context7 tools for library-specific documentation)
Output: Research findings organized by approach, with comparison matrix and recommendation

Quality threshold: >= 0.85 (research phase, not decision-critical)
```

---

## Research Findings

Based on current event sourcing literature and Python library patterns, here are the key practices:

### Version Numbers Approach

**Mechanism:** Each aggregate root maintains a version counter. Before persisting an event, the system verifies that no new events have been added since the aggregate was loaded.

**Advantages:**
- **Deterministic:** Version numbers follow strict ordering. No clock synchronization issues.
- **Semantic clarity:** The version directly represents causality — higher versions mean later events.
- **Implementation simplicity:** Straightforward comparison logic (expected_version == current_version).
- **Python libraries:** Both `EventSourcing` and Eventsourcing libraries use version numbers as the default conflict detection mechanism.

**Disadvantages:**
- **Aggregate-scoped:** Version tracking is per-aggregate, not global. Does not prevent conflicts across related aggregates.
- **Race conditions:** In high-concurrency scenarios, multiple writers checking the same version create a narrow CAS (compare-and-swap) window.
- **Operational complexity:** Requires explicit version management in business logic.

### Timestamps Approach

**Mechanism:** Events are tagged with creation/modification timestamps. Conflict detection compares timestamps of the expected state vs. current state.

**Advantages:**
- **Causality visibility:** Timestamps provide insight into when events occurred, useful for audit trails.
- **External clock alignment:** Integrates naturally with distributed systems that already use NTP for synchronization.
- **Multi-aggregate scenarios:** Timestamps can signal ordering across aggregates (with clock skew tolerance).

**Disadvantages:**
- **Clock dependency:** Relies on accurate system clocks. Clock skew between services causes false conflicts or missed conflicts.
- **Ordering ambiguity:** Concurrent events with identical or very close timestamps create ambiguity. Requires tie-breaking (e.g., process ID, node ID).
- **Performance overhead:** Timestamp comparisons require millisecond or microsecond precision, adding latency in high-frequency scenarios.
- **Less common in Python libraries:** EventSourcing uses timestamps for metadata, not primary conflict detection.

### Comparison Matrix

| Criterion | Version Numbers | Timestamps |
|-----------|-----------------|-----------|
| **Determinism** | High (logic-based) | Medium (clock-dependent) |
| **Scalability** | Good (per-aggregate) | Good (distributed-friendly) |
| **Implementation Complexity** | Low | Medium-High |
| **Python Library Support** | Excellent (EventSourcing, Eventsourcing) | Fair (metadata use only) |
| **Clock Skew Risk** | None | High |
| **Read-Model Consistency** | Strong (via version ordering) | Eventual (timestamp tolerance needed) |

---

## Recommendation for Your Decision

**Default choice: Version numbers.**

**Rationale:**
1. **Python ecosystem alignment:** Both major event sourcing libraries use version numbers as the primary mechanism.
2. **Operational simplicity:** No clock synchronization overhead. Purely logical — testable without time-mocking complexity.
3. **Strong consistency guarantee:** Version ordering is deterministic, making causality reasoning straightforward.
4. **Fit your constraints:** If you're deciding by end of day, version numbers require less architectural rework than distributed timestamp consensus.

**When to consider timestamps instead:**
- You have existing distributed systems with synchronized clocks (NTP-synced across all services).
- Your event sourcing spans multiple deployment regions with acceptable cross-region latency (> 100ms).
- You need sub-millisecond global ordering for compliance/audit requirements.
- You're building a multi-tenant SaaS where aggregate boundaries cross tenant boundaries.

**Hybrid approach (advanced):**
Use version numbers for primary conflict detection within each aggregate, and timestamps as metadata for audit/tracing. This captures the operational simplicity of versions with the observability benefit of timestamps.

---

## Decision Guidance

**Immediate action:** Adopt version numbers as your optimistic concurrency control mechanism. Implement using your event sourcing library's standard pattern:
- Aggregate root: maintain `version` field (integer, incremented on each event).
- Command handlers: compare `command.expected_version` against `aggregate.version` before applying events.
- Event store: enforce `version` uniqueness per aggregate ID on write.

**Implementation reference:** See `EventSourcing` library's `Aggregate` base class for a production-ready pattern.

You can implement this today and adjust if distributed cross-aggregate scenarios arise later. The version-number approach is easy to retrofit with timestamps once your system scales beyond single-aggregate transactions.
