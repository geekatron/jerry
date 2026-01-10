# Research: Work Item Schema and Domain Events

**PS ID:** impl-es
**Entry ID:** e-006
**Date:** 2026-01-09
**Author:** ps-researcher agent v2.0.0
**Topic:** Work Item Schema and Domain Events

---

## L0: Executive Summary (ELI5)

A Work Item is like a sticky note on a project board - it tracks what needs to be done, who's doing it, and when it's finished. But our work items are smarter: they remember everything that happened to them and can prove they meet quality standards.

**Key concepts:**

1. **Work Item Domain Model** - The "shape" of a work item with fields like title, status, and quality metrics
2. **Domain Events** - A record of everything that happened ("Item created", "Status changed", "Tests passed")
3. **Value Objects** - Small pieces like IDs and percentages that validate themselves
4. **Quality Metrics** - Numbers that prove work is done well (test coverage, test ratios)

**Why this matters:** AI agents need to track their work reliably across sessions, prove they've met quality gates, and never lose history when context windows fill up.

---

## L1: Technical Findings

### 1. Work Item Domain Model

#### 1.1 Core Attributes

Based on ADR-007 (ID Generation) and ADR-009 (Event Storage), plus industry patterns:

```python
@dataclass
class WorkItem:
    """
    Aggregate root for work tracking domain.

    An aggregate root is the entry point for all changes to the aggregate.
    External code should only modify WorkItem state through its methods.
    """

    # Identity (ADR-007 hybrid pattern)
    id: WorkItemId                     # Snowflake internal + WORK-nnn display

    # Core attributes
    title: str                         # Human-readable summary
    description: str                   # Detailed description (optional)
    work_type: WorkType                # TASK, BUG, STORY, SPIKE, EPIC

    # Lifecycle
    status: WorkItemStatus             # PENDING, IN_PROGRESS, BLOCKED, DONE, CANCELLED
    priority: Priority                 # CRITICAL, HIGH, MEDIUM, LOW

    # Quality metrics (c-004, c-006 constraints)
    test_coverage: TestCoverage | None # Percentage with validation
    test_ratio: TestRatio | None       # Positive/negative/edge distribution

    # Relationships
    parent_id: WorkItemId | None       # Epic/Story parent
    dependencies: list[WorkItemId]     # Blocking items (DAG)

    # Timestamps
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None

    # Assignment
    assignee: str | None               # Agent or human

    # Event history (ADR-009)
    _version: int                      # Optimistic concurrency
    _recent_events: list[dict]         # Embedded history (last N events)
```

#### 1.2 Work Type Classification

From e-006 (Task Templates) research:

| Type | Description | Typical Size | Has Subtasks |
|------|-------------|--------------|--------------|
| EPIC | Large initiative, spans sprints | Weeks-months | Yes (Stories) |
| STORY | User-valuable feature | 1-5 days | Yes (Tasks) |
| TASK | Specific work unit | Hours-days | Optional |
| SUBTASK | Atomic work item | Hours | No |
| BUG | Defect/problem | Variable | Optional |
| SPIKE | Research/learning | Timeboxed | No |

#### 1.3 Status Transitions

State machine with valid transitions:

```
                    +-----------+
                    | CANCELLED |
                    +-----------+
                         ^
                         |
    +---------+    +------------+    +---------+    +------+
    | PENDING | -> | IN_PROGRESS| -> | BLOCKED | -> | DONE |
    +---------+    +------------+    +---------+    +------+
         ^              |                 |             ^
         |              v                 v             |
         +--------------+-----------------+-------------+
                        (can return to IN_PROGRESS)
```

Valid transitions:

| From | To | Trigger |
|------|----|---------|
| PENDING | IN_PROGRESS | Work starts |
| PENDING | CANCELLED | Removed from scope |
| IN_PROGRESS | BLOCKED | Dependency or issue |
| IN_PROGRESS | DONE | All criteria met |
| IN_PROGRESS | CANCELLED | Removed from scope |
| BLOCKED | IN_PROGRESS | Blocker resolved |
| BLOCKED | CANCELLED | Removed from scope |
| DONE | IN_PROGRESS | Reopened (rare) |

---

### 2. Domain Events Catalog

#### 2.1 Event Base Design

From ADR-009 and [Microsoft Learn DDD patterns](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/domain-events-design-implementation):

```python
@dataclass(frozen=True)
class DomainEvent:
    """
    Base class for domain events.

    Domain events capture facts about the domain that happened in the past.
    They are immutable and named in past tense.

    References:
        - ADR-009: Event Storage Mechanism
        - Martin Fowler: https://martinfowler.com/eaaDev/DomainEvent.html
    """

    # Event identity
    event_id: str              # UUID for deduplication
    event_type: str            # Class name for serialization
    event_version: int         # Schema version (default 1)

    # Event timing
    timestamp: datetime        # When it happened (UTC)

    # Aggregate reference
    aggregate_id: str          # WorkItemId.internal_id
    aggregate_type: str        # "WorkItem"
    aggregate_version: int     # Optimistic concurrency token

    # Metadata
    correlation_id: str | None # Links related events
    causation_id: str | None   # Event that caused this one
    actor: str | None          # Who/what triggered it
```

#### 2.2 Work Item Events

| Event | Payload | When Emitted |
|-------|---------|--------------|
| WorkItemCreated | title, work_type, priority | New item created |
| WorkItemUpdated | changed_fields | Any field modified |
| StatusChanged | old_status, new_status, reason | Status transition |
| PriorityChanged | old_priority, new_priority | Priority adjusted |
| AssigneeChanged | old_assignee, new_assignee | Reassignment |
| DependencyAdded | dependency_id | Dependency linked |
| DependencyRemoved | dependency_id | Dependency unlinked |
| QualityMetricsUpdated | coverage, ratio | Test results recorded |
| WorkItemCompleted | final_status, duration | Done/Cancelled |

#### 2.3 Event Payload Examples

```python
@dataclass(frozen=True)
class WorkItemCreated(DomainEvent):
    """Emitted when a new work item is created."""

    title: str
    work_type: str           # Serialized WorkType
    priority: str            # Serialized Priority
    parent_id: str | None    # Parent's internal_id

    @property
    def event_type(self) -> str:
        return "WorkItemCreated"

    @property
    def event_version(self) -> int:
        return 1


@dataclass(frozen=True)
class StatusChanged(DomainEvent):
    """Emitted when work item status transitions."""

    old_status: str
    new_status: str
    reason: str | None       # Why the change happened

    @property
    def event_type(self) -> str:
        return "StatusChanged"


@dataclass(frozen=True)
class QualityMetricsUpdated(DomainEvent):
    """Emitted when test results are recorded."""

    # Test coverage
    coverage_percent: float | None

    # Test ratio distribution
    positive_tests: int | None
    negative_tests: int | None
    edge_case_tests: int | None

    # Quality gate evaluation
    gate_level: str | None   # L0, L1, L2
    gate_passed: bool
    gate_failures: list[str] # Specific failures

    @property
    def event_type(self) -> str:
        return "QualityMetricsUpdated"
```

---

### 3. Value Object Catalog

#### 3.1 WorkItemId (Already Implemented)

From ADR-007 and existing implementation at `src/work_tracking/domain/value_objects/work_item_id.py`:

```python
@dataclass(frozen=True, slots=True)
class WorkItemId:
    """
    Hybrid identity combining Snowflake internal ID with human-readable display ID.

    Invariants:
        - internal_id is non-negative (Snowflake IDs are always positive)
        - display_number is positive (starts at 1)
        - display_id format is WORK-{number} with 3-digit minimum padding
    """

    internal_id: int     # 64-bit Snowflake for uniqueness
    display_id: str      # WORK-042 for human readability

    @classmethod
    def create(cls, internal_id: int, display_number: int) -> WorkItemId:
        """Factory method with validation."""
        ...

    @property
    def display_number(self) -> int:
        """Extract numeric portion."""
        ...

    @property
    def internal_hex(self) -> str:
        """Hex representation for debugging."""
        ...
```

**Design Rationale:**
- Collision-free (Snowflake internals)
- Human-readable (WORK-nnn display)
- Time-sortable (Snowflake timestamp component)
- No coordination required between agents

#### 3.2 TestCoverage Value Object

```python
@dataclass(frozen=True, slots=True)
class TestCoverage:
    """
    Test coverage percentage with validation.

    Invariants:
        - percent is between 0.0 and 100.0 inclusive
        - Can be compared, sorted, and used in quality gate calculations

    Example:
        >>> coverage = TestCoverage.from_percent(85.5)
        >>> coverage.meets_threshold(80.0)
        True
    """

    percent: float

    def __post_init__(self) -> None:
        if not 0.0 <= self.percent <= 100.0:
            raise ValueError(
                f"Coverage must be between 0 and 100, got {self.percent}"
            )

    @classmethod
    def from_percent(cls, value: float) -> TestCoverage:
        """Create from percentage value."""
        return cls(percent=round(value, 2))

    @classmethod
    def from_fraction(cls, covered: int, total: int) -> TestCoverage:
        """Create from lines covered / total lines."""
        if total == 0:
            return cls(percent=0.0)
        return cls(percent=round((covered / total) * 100, 2))

    def meets_threshold(self, threshold: float) -> bool:
        """Check if coverage meets or exceeds threshold."""
        return self.percent >= threshold

    def __str__(self) -> str:
        return f"{self.percent:.1f}%"

    def __lt__(self, other: TestCoverage) -> bool:
        return self.percent < other.percent
```

#### 3.3 TestRatio Value Object

Based on constraint c-006 (happy path, negative, edge case distribution):

```python
@dataclass(frozen=True, slots=True)
class TestRatio:
    """
    Distribution of test types (positive/negative/edge cases).

    Invariants:
        - All counts are non-negative
        - At least one test must exist (total > 0)

    Quality Gate Integration (c-006):
        - L0: Positive tests only is acceptable
        - L1: Must have positive + negative tests
        - L2: Must have positive + negative + edge case tests

    Example:
        >>> ratio = TestRatio(positive=5, negative=3, edge_case=2)
        >>> ratio.total
        10
        >>> ratio.positive_percent
        50.0
    """

    positive: int      # Happy path tests
    negative: int      # Error handling tests
    edge_case: int     # Boundary condition tests

    def __post_init__(self) -> None:
        if self.positive < 0 or self.negative < 0 or self.edge_case < 0:
            raise ValueError("Test counts must be non-negative")
        if self.total == 0:
            raise ValueError("At least one test is required")

    @property
    def total(self) -> int:
        """Total number of tests."""
        return self.positive + self.negative + self.edge_case

    @property
    def positive_percent(self) -> float:
        """Percentage of positive tests."""
        return (self.positive / self.total) * 100

    @property
    def negative_percent(self) -> float:
        """Percentage of negative tests."""
        return (self.negative / self.total) * 100

    @property
    def edge_case_percent(self) -> float:
        """Percentage of edge case tests."""
        return (self.edge_case / self.total) * 100

    def meets_level(self, level: str) -> bool:
        """
        Check if ratio meets quality gate level requirements.

        L0: positive > 0
        L1: positive > 0 and negative > 0
        L2: positive > 0 and negative > 0 and edge_case > 0
        """
        if level == "L0":
            return self.positive > 0
        elif level == "L1":
            return self.positive > 0 and self.negative > 0
        elif level == "L2":
            return self.positive > 0 and self.negative > 0 and self.edge_case > 0
        else:
            raise ValueError(f"Unknown quality level: {level}")

    def __str__(self) -> str:
        return f"P:{self.positive}/N:{self.negative}/E:{self.edge_case}"
```

#### 3.4 WorkItemStatus Value Object

Enum with transition validation:

```python
from enum import Enum


class WorkItemStatus(Enum):
    """
    Work item lifecycle status.

    States form a directed graph with valid transitions.
    Invalid transitions raise InvalidStateTransitionError.
    """

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    DONE = "done"
    CANCELLED = "cancelled"

    _VALID_TRANSITIONS: dict[str, set[str]] = {
        "pending": {"in_progress", "cancelled"},
        "in_progress": {"blocked", "done", "cancelled"},
        "blocked": {"in_progress", "cancelled"},
        "done": {"in_progress"},  # Reopen capability
        "cancelled": set(),  # Terminal state
    }

    def can_transition_to(self, target: WorkItemStatus) -> bool:
        """Check if transition to target status is valid."""
        return target.value in self._VALID_TRANSITIONS.get(self.value, set())

    def validate_transition(self, target: WorkItemStatus) -> None:
        """Raise if transition is invalid."""
        if not self.can_transition_to(target):
            raise InvalidStateTransitionError(
                f"Cannot transition from {self.value} to {target.value}"
            )

    @property
    def is_terminal(self) -> bool:
        """Check if this is a terminal state."""
        return self in (WorkItemStatus.DONE, WorkItemStatus.CANCELLED)

    @property
    def is_active(self) -> bool:
        """Check if this is an active work state."""
        return self in (WorkItemStatus.IN_PROGRESS, WorkItemStatus.BLOCKED)
```

#### 3.5 Priority Value Object

```python
from enum import IntEnum


class Priority(IntEnum):
    """
    Work item priority with numeric ordering.

    Uses IntEnum for natural sorting (lower value = higher priority).
    """

    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

    @classmethod
    def from_string(cls, value: str) -> Priority:
        """Parse case-insensitive priority string."""
        normalized = value.upper().replace(" ", "_")
        try:
            return cls[normalized]
        except KeyError:
            return cls.MEDIUM  # Default fallback

    def __str__(self) -> str:
        return self.name.lower()
```

---

### 4. Event Versioning Strategy

Based on [Event-Driven.io patterns](https://event-driven.io/en/how_to_do_event_versioning/) and [theburningmonk's 2025 guide](https://theburningmonk.com/2025/04/event-versioning-strategies-for-event-driven-architectures/):

#### 4.1 Versioning Approach

**Selected Strategy: Weak Schema with Version Field**

```python
@dataclass(frozen=True)
class DomainEvent:
    """Base event with version tracking."""

    event_version: int = 1  # Schema version

    # ... other fields
```

**Rationale:**
1. **Backward compatibility first** - Never break old consumers
2. **Additive changes only** - New fields are optional with defaults
3. **No breaking changes** - Renaming or removing fields forbidden
4. **Upcasting for migration** - Transform old events at read time

#### 4.2 Safe vs Unsafe Changes

| Safe Changes | Unsafe Changes |
|--------------|----------------|
| Add optional field | Remove field |
| Add new event type | Rename field |
| Add enum value | Change field type |
| Add nested object | Make optional required |
| Deprecate (keep old) | Replace enum values |

#### 4.3 Event Migration Pattern

From [EventSourcingDB best practices](https://docs.eventsourcingdb.io/best-practices/versioning-events/):

```python
class EventUpcaster:
    """
    Transform events from old versions to current version.

    Upcasting happens at read time, allowing old events to
    coexist with new events in the event store.
    """

    def upcast(self, event_data: dict) -> dict:
        """Upcast event to current version."""
        version = event_data.get("event_version", 1)
        event_type = event_data.get("event_type")

        # Apply version-specific transformations
        if event_type == "StatusChanged" and version == 1:
            # V1 didn't have 'reason' field - add default
            event_data["reason"] = None
            event_data["event_version"] = 2

        return event_data
```

#### 4.4 Versioning Best Practices

From [Solace Events, Schemas and Payloads](https://solace.com/blog/events-schemas-payloads/):

1. **Include version in every event** - Enables future migration
2. **Support transition periods** - Run old and new in parallel
3. **Use additive changes** - Never remove, only add
4. **Document deprecations** - Clear timelines for removal
5. **Test version compatibility** - Both forward and backward

---

### 5. Aggregate Root Behavior

#### 5.1 WorkItem as Aggregate Root

From [Microsoft DDD patterns](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/domain-events-design-implementation):

```python
@dataclass
class WorkItem:
    """
    WorkItem aggregate root.

    Aggregate roots are the only entry point for modifications.
    All state changes emit domain events.

    References:
        - Eric Evans, Domain-Driven Design (Blue Book)
        - Vaughn Vernon, Implementing Domain-Driven Design
    """

    id: WorkItemId
    title: str
    status: WorkItemStatus
    # ... other fields

    _pending_events: list[DomainEvent] = field(default_factory=list)

    def start_work(self, actor: str) -> None:
        """
        Transition to IN_PROGRESS status.

        Raises:
            InvalidStateTransitionError: If transition not allowed
        """
        self.status.validate_transition(WorkItemStatus.IN_PROGRESS)

        old_status = self.status
        self.status = WorkItemStatus.IN_PROGRESS
        self.updated_at = datetime.now(timezone.utc)

        self._emit(StatusChanged(
            aggregate_id=str(self.id.internal_id),
            aggregate_type="WorkItem",
            aggregate_version=self._version,
            old_status=old_status.value,
            new_status=self.status.value,
            reason=None,
            actor=actor,
        ))

    def complete(self, actor: str, reason: str | None = None) -> None:
        """
        Transition to DONE status.

        Raises:
            InvalidStateTransitionError: If not in completable state
            QualityGateNotMetError: If quality requirements not satisfied
        """
        self.status.validate_transition(WorkItemStatus.DONE)

        # Validate quality gates if applicable
        if self.work_type not in (WorkType.SPIKE,):
            self._validate_quality_gates()

        old_status = self.status
        self.status = WorkItemStatus.DONE
        self.completed_at = datetime.now(timezone.utc)
        self.updated_at = self.completed_at

        duration = self.completed_at - self.created_at

        self._emit(WorkItemCompleted(
            aggregate_id=str(self.id.internal_id),
            aggregate_type="WorkItem",
            aggregate_version=self._version,
            final_status="done",
            duration_seconds=int(duration.total_seconds()),
            actor=actor,
        ))

    def update_quality_metrics(
        self,
        coverage: TestCoverage | None,
        ratio: TestRatio | None,
        actor: str,
    ) -> None:
        """Record test execution results."""
        self.test_coverage = coverage
        self.test_ratio = ratio
        self.updated_at = datetime.now(timezone.utc)

        # Evaluate quality gate
        gate_level, passed, failures = self._evaluate_quality_gate()

        self._emit(QualityMetricsUpdated(
            aggregate_id=str(self.id.internal_id),
            aggregate_type="WorkItem",
            aggregate_version=self._version,
            coverage_percent=coverage.percent if coverage else None,
            positive_tests=ratio.positive if ratio else None,
            negative_tests=ratio.negative if ratio else None,
            edge_case_tests=ratio.edge_case if ratio else None,
            gate_level=gate_level,
            gate_passed=passed,
            gate_failures=failures,
            actor=actor,
        ))

    def _emit(self, event: DomainEvent) -> None:
        """Add event to pending events queue."""
        self._pending_events.append(event)
        self._version += 1

    def collect_events(self) -> list[DomainEvent]:
        """Retrieve and clear pending events."""
        events = list(self._pending_events)
        self._pending_events.clear()
        return events
```

---

## L2: Strategic Patterns and Trade-offs

### PAT-001: Hybrid Identity Pattern (ADR-007)

**Problem:** Need unique IDs without coordination, but also human-readable references.

**Solution:** Snowflake internal ID + sequential display ID.

| Aspect | Benefit | Cost |
|--------|---------|------|
| Uniqueness | No collisions ever | Two ID systems to manage |
| Human UX | WORK-042 is memorable | Display ID gaps if items deleted |
| Time-sorting | Internal IDs are chronological | Extra parsing for timeline queries |
| Distribution | No coordination needed | Worker ID entropy required |

**When to use:** Multi-agent, distributed work tracking systems.

### PAT-002: Embedded Event History (ADR-009)

**Problem:** Need event audit trail without unbounded storage growth.

**Solution:** Store last N events embedded in work item, flush full history to session files.

| Aspect | Benefit | Cost |
|--------|---------|------|
| Audit trail | Recent history always available | Limited history in entity |
| Storage | Bounded growth | Full history requires file access |
| Context | Events don't bloat context | May lose events on crash |
| Debugging | Session replay possible | Cross-session continuity optional |

**When to use:** Agent systems with context window constraints.

### PAT-003: Event Versioning with Upcasting

**Problem:** Event schemas evolve but old events must remain valid.

**Solution:** Version field + additive-only changes + read-time upcasting.

| Aspect | Benefit | Cost |
|--------|---------|------|
| Compatibility | Old events always readable | Migration code to maintain |
| Evolution | Add fields freely | Cannot remove or rename |
| Testing | Clear version contracts | Need compatibility tests |
| Simplicity | No schema registry needed | Upcasters accumulate over time |

**When to use:** Any event-sourced or event-driven system.

### PAT-004: Status State Machine

**Problem:** Invalid status transitions could corrupt work item state.

**Solution:** Explicit transition validation in value object.

| Aspect | Benefit | Cost |
|--------|---------|------|
| Safety | Invalid transitions rejected | Transition matrix to maintain |
| Clarity | Valid paths documented | Terminal states need special handling |
| Events | Transitions emit events | More events generated |
| Testing | Easy to test transitions | Need coverage of all paths |

**When to use:** Any domain with lifecycle states.

### PAT-005: Quality Gate Value Objects

**Problem:** Quality metrics need validation and comparison operations.

**Solution:** TestCoverage and TestRatio as self-validating value objects.

| Aspect | Benefit | Cost |
|--------|---------|------|
| Validation | Invalid values rejected at creation | Extra classes |
| Business logic | meets_threshold(), meets_level() | Logic split from aggregate |
| Immutability | Thread-safe, hashable | New instance for each change |
| Testing | Easy unit testing | More test files |

**When to use:** Numeric business rules with validation constraints.

---

## References

### Primary Sources

1. **ADR-007: ID Generation Strategy**
   - Document: `projects/PROJ-001-plugin-cleanup/design/ADR-007-id-generation-strategy.md`
   - Covers: Snowflake IDs, hybrid identity, collision prevention

2. **ADR-009: Event Storage Mechanism**
   - Document: `projects/PROJ-001-plugin-cleanup/design/ADR-009-event-storage-mechanism.md`
   - Covers: Session event buffer, embedded events, domain event base class

3. **e-006: Task Template Schemas**
   - Document: `projects/PROJ-001-plugin-cleanup/research/dev-skill-e-006-task-templates.md`
   - Covers: Work type hierarchy, acceptance criteria, success criteria schemas

### Industry References

4. [Domain events: Design and implementation - Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/domain-events-design-implementation)

5. [Domain Event - Martin Fowler](https://martinfowler.com/eaaDev/DomainEvent.html)

6. [Event versioning strategies for event-driven architectures - theburningmonk](https://theburningmonk.com/2025/04/event-versioning-strategies-for-event-driven-architectures/)

7. [How to (not) do the events versioning? - Event-Driven.io](https://event-driven.io/en/how_to_do_event_versioning/)

8. [Versioning Events - EventSourcingDB](https://docs.eventsourcingdb.io/best-practices/versioning-events/)

9. [Events, Schemas and Payloads - Solace](https://solace.com/blog/events-schemas-payloads/)

10. [Domain-Driven Design in 2025 - Saven Tech](https://saventech.com/domain-driven-design-ddd-in-2025/)

---

## Pattern Traceability Matrix

| Pattern ID | Pattern Name | Source | Implementation |
|------------|--------------|--------|----------------|
| PAT-001-e006 | Hybrid Identity | ADR-007 | WorkItemId value object |
| PAT-002-e006 | Embedded Event History | ADR-009 | _recent_events in WorkItem |
| PAT-003-e006 | Event Versioning | Research | event_version field |
| PAT-004-e006 | Status State Machine | e-006 | WorkItemStatus enum |
| PAT-005-e006 | Quality Gate VOs | c-004, c-006 | TestCoverage, TestRatio |

---

## Implementation Checklist

### Value Objects to Implement

- [x] WorkItemId (already implemented)
- [ ] TestCoverage
- [ ] TestRatio
- [ ] WorkItemStatus (enum with transitions)
- [ ] Priority (IntEnum)
- [ ] WorkType (enum)

### Domain Events to Implement

- [ ] DomainEvent base class
- [ ] WorkItemCreated
- [ ] StatusChanged
- [ ] QualityMetricsUpdated
- [ ] WorkItemCompleted
- [ ] PriorityChanged
- [ ] AssigneeChanged
- [ ] DependencyAdded
- [ ] DependencyRemoved

### Aggregate Root

- [ ] WorkItem entity with event emission
- [ ] State transition validation
- [ ] Quality gate validation
- [ ] Event collection and clearing

---

*Document created: 2026-01-09*
*Author: ps-researcher agent v2.0.0*
*PS Context: impl-es / e-006*
