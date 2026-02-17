"""
Aggregate Pattern - Canonical implementation for Jerry Framework.

Aggregates implement apply_event(), collect_events(), and invariant enforcement.
Use event sourcing for state management.

This file is SELF-CONTAINED for use as a reference pattern. It defines inline
versions of DomainEvent and event classes so the pattern can be read without
any external imports. The real implementations live in:
    - src/shared_kernel/domain_event.py (DomainEvent base)
    - domain event modules (concrete events)

References:
    - architecture-standards.md (line 99)
    - work_tracking/domain/aggregates/base.py
    - DDD Aggregate pattern (Evans, 2004)

Exports:
    Example aggregate following Jerry conventions
"""

from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, TypeVar

# ---------------------------------------------------------------------------
# Inline helpers (mirrors shared_kernel/domain_event.py)
# ---------------------------------------------------------------------------


def _generate_event_id() -> str:
    """Generate a unique event ID."""
    return f"EVT-{uuid.uuid4()}"


def _current_timestamp() -> datetime:
    """Get current UTC timestamp."""
    return datetime.now(UTC)


# ---------------------------------------------------------------------------
# Inline DomainEvent base (simplified from shared_kernel/domain_event.py)
# In real code, import DomainEvent from src.shared_kernel.domain_event.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DomainEvent:
    """Simplified base class for pattern reference. See shared_kernel/domain_event.py."""

    aggregate_id: str
    aggregate_type: str
    event_id: str = field(default_factory=_generate_event_id)
    timestamp: datetime = field(default_factory=_current_timestamp)
    version: int = 1

    def _payload(self) -> dict[str, Any]:
        """Return event-specific payload data. Override is optional."""
        return {}


# ---------------------------------------------------------------------------
# Inline event classes (from domain_event_pattern.py)
# In real code, these would be separate event modules.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class WorkItemCreated(DomainEvent):
    """Creation event for WorkItem aggregate."""

    title: str = ""
    work_type: str = "task"
    priority: str = "medium"


@dataclass(frozen=True)
class StatusChanged(DomainEvent):
    """State transition event recording before/after status."""

    old_status: str = ""
    new_status: str = ""
    reason: str | None = None


@dataclass(frozen=True)
class QualityMetricsUpdated(DomainEvent):
    """Quality metrics update event with gate evaluation."""

    coverage_percent: float | None = None
    positive_tests: int | None = None
    negative_tests: int | None = None
    gate_level: str | None = None
    gate_passed: bool = False
    gate_failures: tuple[str, ...] = field(default_factory=tuple)


# Type variable for self-returning factory methods
TAggregateRoot = TypeVar("TAggregateRoot", bound="AggregateRoot")


# =============================================================================
# Base Aggregate Pattern
# =============================================================================


class AggregateRoot(ABC):
    """
    Base class for event-sourced aggregates.

    Aggregates SHOULD:
    - Implement _apply() for event-specific state mutations
    - Use _raise_event() to record state changes
    - Expose factory methods for creation (not __init__)
    - Maintain invariants before raising events

    Thread Safety:
        Aggregates are NOT thread-safe. Each instance should
        only be accessed by a single thread at a time.

    Invariants:
        - ID is immutable once set
        - Version increases monotonically with each event
        - Events must be applied in version order

    Example:
        >>> item = WorkItem.create(id="12345", title="Implement login")
        >>> item.change_status("in_progress")
        >>> events = item.collect_events()
        >>> len(events)
        2
    """

    _aggregate_type: str = "Aggregate"

    def __init__(self, id: str) -> None:
        """Initialize aggregate with identity."""
        self._initialize(id)

    def _initialize(self, id: str, version: int = 0) -> None:
        """
        Initialize aggregate internal state.

        Args:
            id: Unique identifier for this aggregate
            version: Starting version (default 0 for new aggregates)
        """
        if not id:
            raise ValueError("Aggregate ID cannot be empty")

        self._id = id
        self._version = version
        self._pending_events: list[DomainEvent] = []
        self._created_on: datetime | None = None
        self._modified_on: datetime | None = None

    @property
    def id(self) -> str:
        """Unique identifier for this aggregate."""
        return self._id

    @property
    def version(self) -> int:
        """Current version of the aggregate."""
        return self._version

    @property
    def created_on(self) -> datetime | None:
        """Timestamp when the aggregate was created."""
        return self._created_on

    @property
    def modified_on(self) -> datetime | None:
        """Timestamp of the last modification."""
        return self._modified_on

    def _raise_event(self, event: DomainEvent) -> None:
        """
        Record a new domain event.

        This method:
        1. Increments the version
        2. Applies the event to update state
        3. Adds the event to the pending list
        4. Updates modification timestamp

        Args:
            event: The domain event to raise

        Raises:
            ValueError: If event aggregate_id doesn't match this aggregate
        """
        if event.aggregate_id != self._id:
            raise ValueError(
                f"Event aggregate_id '{event.aggregate_id}' does not match "
                f"aggregate ID '{self._id}'"
            )

        self._version += 1
        self._apply(event)
        self._pending_events.append(event)
        self._modified_on = event.timestamp

        if self._created_on is None:
            self._created_on = event.timestamp

    @abstractmethod
    def _apply(self, event: DomainEvent) -> None:
        """
        Apply an event to update aggregate state.

        Implement in subclasses to handle event-specific state mutations.
        This method must be deterministic.

        Args:
            event: The domain event to apply

        Note:
            - Do NOT raise new events from within _apply
            - Do NOT perform side effects (I/O, logging, etc.)
            - Do NOT validate business rules (that's done before raising)
        """
        ...

    def collect_events(self) -> Sequence[DomainEvent]:
        """
        Return and clear pending events.

        Returns:
            List of events raised since last collection
        """
        events = list(self._pending_events)
        self._pending_events.clear()
        return events

    def has_pending_events(self) -> bool:
        """Check if there are uncommitted events."""
        return len(self._pending_events) > 0

    @classmethod
    def load_from_history(
        cls: type[TAggregateRoot],
        events: Sequence[DomainEvent],
    ) -> TAggregateRoot:
        """
        Reconstruct aggregate by replaying events.

        Args:
            events: Historical events in version order

        Returns:
            Aggregate with state rebuilt from events

        Raises:
            ValueError: If events sequence is empty
            ValueError: If events are not in sequential version order
        """
        if not events:
            raise ValueError("Cannot load from empty event history")

        cls._validate_event_sequence(events)

        # Create uninitialized instance
        aggregate = cls.__new__(cls)

        # Initialize from first event
        first_event = events[0]
        aggregate._id = first_event.aggregate_id
        aggregate._version = 0
        aggregate._pending_events = []
        aggregate._created_on = first_event.timestamp
        aggregate._modified_on = None

        # Replay all events
        for event in events:
            aggregate._version = event.version
            aggregate._apply(event)
            aggregate._modified_on = event.timestamp

        return aggregate

    @classmethod
    def _validate_event_sequence(cls, events: Sequence[DomainEvent]) -> None:
        """Validate that events form a valid sequence."""
        if not events:
            return

        first_id = events[0].aggregate_id
        expected_version = events[0].version

        for i, event in enumerate(events):
            if event.aggregate_id != first_id:
                raise ValueError(
                    f"Event at index {i} has aggregate_id '{event.aggregate_id}' "
                    f"but expected '{first_id}'"
                )
            if event.version != expected_version:
                raise ValueError(
                    f"Event at index {i} has version {event.version} "
                    f"but expected {expected_version}"
                )
            expected_version += 1


# =============================================================================
# Concrete Aggregate Example
# =============================================================================


class WorkItem(AggregateRoot):
    """
    Example concrete aggregate - Work item with status tracking.

    Demonstrates:
    - Factory method for creation
    - Command methods that raise events
    - Invariant enforcement before raising events
    - Event application pattern matching

    Attributes:
        id: Unique identifier
        title: Human-readable title
        status: Current status
        priority: Priority level
        coverage_percent: Test coverage percentage
    """

    _aggregate_type = "WorkItem"

    def __init__(self, id: str) -> None:
        """Private constructor - use create() factory method."""
        super().__init__(id)
        self._title: str = ""
        self._status: str = "backlog"
        self._priority: str = "medium"
        self._coverage_percent: float | None = None

    @classmethod
    def create(cls, id: str, title: str, priority: str = "medium") -> WorkItem:
        """
        Factory method to create a new work item.

        Args:
            id: Unique identifier
            title: Human-readable title
            priority: Priority level (default: medium)

        Returns:
            New WorkItem instance with creation event

        Raises:
            ValueError: If title is empty

        Example:
            >>> item = WorkItem.create("12345", "Implement login", "high")
            >>> item.title
            'Implement login'
        """
        if not title:
            raise ValueError("Title cannot be empty")

        # Create uninitialized instance
        item = cls.__new__(cls)
        item._initialize(id)
        item._title = ""
        item._status = "backlog"
        item._priority = "medium"
        item._coverage_percent = None

        # Raise creation event
        event = WorkItemCreated(
            aggregate_id=id,
            aggregate_type=cls._aggregate_type,
            version=1,
            title=title,
            work_type="task",
            priority=priority,
        )
        item._raise_event(event)

        return item

    @property
    def title(self) -> str:
        """Human-readable title."""
        return self._title

    @property
    def status(self) -> str:
        """Current status."""
        return self._status

    @property
    def priority(self) -> str:
        """Priority level."""
        return self._priority

    def change_status(self, new_status: str, reason: str | None = None) -> None:
        """
        Change work item status.

        Enforces state transition rules before raising event.

        Args:
            new_status: New status value
            reason: Optional reason for the change

        Raises:
            ValueError: If status transition is invalid

        Example:
            >>> item = WorkItem.create("12345", "Implement login")
            >>> item.change_status("in_progress", "Starting work")
        """
        # Invariant: validate state transition
        valid_transitions = {
            "backlog": {"in_progress", "cancelled"},
            "in_progress": {"done", "blocked", "cancelled"},
            "blocked": {"in_progress", "cancelled"},
            "done": set(),
            "cancelled": set(),
        }

        if new_status not in valid_transitions.get(self._status, set()):
            raise ValueError(f"Cannot transition from {self._status} to {new_status}")

        # Raise event
        event = StatusChanged(
            aggregate_id=self._id,
            aggregate_type=self._aggregate_type,
            version=self._version + 1,
            old_status=self._status,
            new_status=new_status,
            reason=reason,
        )
        self._raise_event(event)

    def update_quality_metrics(
        self,
        coverage_percent: float | None = None,
        positive_tests: int | None = None,
        negative_tests: int | None = None,
    ) -> None:
        """
        Update quality metrics for this work item.

        Args:
            coverage_percent: Test coverage percentage
            positive_tests: Count of happy path tests
            negative_tests: Count of error handling tests

        Example:
            >>> item = WorkItem.create("12345", "Implement login")
            >>> item.update_quality_metrics(coverage_percent=85.5, positive_tests=10)
        """
        event = QualityMetricsUpdated(
            aggregate_id=self._id,
            aggregate_type=self._aggregate_type,
            version=self._version + 1,
            coverage_percent=coverage_percent,
            positive_tests=positive_tests,
            negative_tests=negative_tests,
            gate_level="L2",
            gate_passed=coverage_percent >= 90.0 if coverage_percent else False,
        )
        self._raise_event(event)

    def _apply(self, event: DomainEvent) -> None:
        """
        Apply an event to update aggregate state.

        Pattern matching on event type to dispatch to appropriate handler.
        """
        if isinstance(event, WorkItemCreated):
            self._title = event.title
            self._status = "backlog"
            self._priority = event.priority

        elif isinstance(event, StatusChanged):
            self._status = event.new_status

        elif isinstance(event, QualityMetricsUpdated):
            self._coverage_percent = event.coverage_percent
