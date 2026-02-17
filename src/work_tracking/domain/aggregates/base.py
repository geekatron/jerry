# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
AggregateRoot - Base class for event-sourced aggregates.

Provides the foundation for all event-sourced domain aggregates in the
work_tracking domain. Implements the lifecycle for raising, applying,
and collecting domain events.

Lifecycle:
    1. Create: Factory method constructs aggregate via creation event
    2. Mutate: Commands call _raise_event() to record changes
    3. Apply: Events mutate state via _apply() dispatcher
    4. Persist: collect_events() returns pending events for storage
    5. Load: load_from_history() reconstructs from event stream

References:
    - PAT-001: Event Store Interface Pattern
    - IMPL-ES-003: AggregateRoot Base Class
    - pyeventsourcing Aggregate base class pattern
    - DDD Aggregate pattern (Evans, 2004)

Exports:
    AggregateRoot: Abstract base class for event-sourced aggregates
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from datetime import datetime
from typing import TypeVar

from src.shared_kernel.domain_event import DomainEvent

# Type variable for self-returning factory methods
TAggregateRoot = TypeVar("TAggregateRoot", bound="AggregateRoot")


class AggregateRoot(ABC):
    """
    Base class for event-sourced aggregates.

    An aggregate is a cluster of domain objects that can be treated as a
    single unit. The AggregateRoot is the only member of the aggregate that
    outside objects are allowed to hold references to.

    This base class provides:
        - Identity and version tracking
        - Event lifecycle management (raise, apply, collect)
        - History replay for reconstitution
        - Timestamp tracking (created_on, modified_on)

    Thread Safety:
        Aggregates are NOT thread-safe. Each aggregate instance should
        only be accessed by a single thread at a time.

    Invariants:
        - ID is immutable once set
        - Version increases monotonically with each event
        - Events must be applied in version order
        - Pending events are cleared after collection

    Example:
        >>> class WorkItem(AggregateRoot):
        ...     @classmethod
        ...     def create(cls, id: str, title: str) -> WorkItem:
        ...         item = cls.__new__(cls)
        ...         item._initialize(id)
        ...         item._raise_event(WorkItemCreated(...))
        ...         return item
        ...
        ...     def _apply(self, event: DomainEvent) -> None:
        ...         if isinstance(event, WorkItemCreated):
        ...             self._title = event.title

    References:
        - Martin Fowler: Aggregate
          https://martinfowler.com/bliki/DDD_Aggregate.html
        - Eric Evans: Domain-Driven Design, Chapter 6
    """

    # Type name for event correlation. Subclasses should override.
    _aggregate_type: str = "Aggregate"

    def __init__(self, id: str) -> None:
        """
        Initialize aggregate with identity.

        Args:
            id: Unique identifier for this aggregate instance

        Note:
            Prefer using _initialize() in factory methods to avoid
            calling __init__ directly with complex initialization.
        """
        self._initialize(id)

    def _initialize(self, id: str, version: int = 0) -> None:
        """
        Initialize aggregate internal state.

        Called by __init__ and can be called by factory methods
        for more control over initialization.

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
        """
        Unique identifier for this aggregate.

        The ID is immutable once the aggregate is created.
        """
        return self._id

    @property
    def version(self) -> int:
        """
        Current version of the aggregate.

        Increments with each event applied. Used for optimistic
        concurrency control when persisting events.
        """
        return self._version

    @property
    def created_on(self) -> datetime | None:
        """
        Timestamp when the aggregate was created.

        Set from the first event's timestamp during creation or
        history replay. None if no events have been applied.
        """
        return self._created_on

    @property
    def modified_on(self) -> datetime | None:
        """
        Timestamp of the last modification.

        Updated each time an event is applied. None if no events
        have been applied.
        """
        return self._modified_on

    def _raise_event(self, event: DomainEvent) -> None:
        """
        Record a new domain event.

        This method:
            1. Increments the version
            2. Applies the event to update state
            3. Adds the event to the pending list for persistence
            4. Updates modification timestamp

        Args:
            event: The domain event to raise

        Raises:
            ValueError: If event aggregate_id doesn't match this aggregate

        Note:
            The event's version should match the new version of the aggregate.
            This is validated during persistence, not here.

        Example:
            >>> def change_title(self, new_title: str) -> None:
            ...     event = TitleChanged(
            ...         aggregate_id=self.id,
            ...         aggregate_type=self._aggregate_type,
            ...         version=self.version + 1,
            ...         new_title=new_title,
            ...     )
            ...     self._raise_event(event)
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

        # Set created_on from first event
        if self._created_on is None:
            self._created_on = event.timestamp

    @abstractmethod
    def _apply(self, event: DomainEvent) -> None:
        """
        Apply an event to update aggregate state.

        Implement in subclasses to handle event-specific state mutations.
        This method must be deterministic: replaying the same events must
        always produce the same state.

        Args:
            event: The domain event to apply

        Note:
            - Do NOT raise new events from within _apply
            - Do NOT perform side effects (I/O, logging, etc.)
            - Do NOT validate business rules (that's done before raising)

        Example:
            >>> def _apply(self, event: DomainEvent) -> None:
            ...     if isinstance(event, WorkItemCreated):
            ...         self._title = event.title
            ...         self._status = "backlog"
            ...     elif isinstance(event, StatusChanged):
            ...         self._status = event.new_status
        """
        ...

    def collect_events(self) -> Sequence[DomainEvent]:
        """
        Return and clear pending events.

        Call this after successful persistence to get events that
        need to be published or stored.

        Returns:
            List of events raised since last collection

        Note:
            Events are cleared after collection. If persistence fails,
            the aggregate may need to be reloaded from history.

        Example:
            >>> events = aggregate.collect_events()
            >>> event_store.append(aggregate.id, events, expected_version)
        """
        events = list(self._pending_events)
        self._pending_events.clear()
        return events

    def has_pending_events(self) -> bool:
        """
        Check if there are uncommitted events.

        Returns:
            True if events have been raised but not yet collected
        """
        return len(self._pending_events) > 0

    @classmethod
    def load_from_history(
        cls: type[TAggregateRoot],
        events: Sequence[DomainEvent],
    ) -> TAggregateRoot:
        """
        Reconstruct aggregate by replaying events.

        Creates a new aggregate instance and applies all events
        in order to rebuild the state.

        Args:
            events: Historical events in version order

        Returns:
            Aggregate with state rebuilt from events

        Raises:
            ValueError: If events sequence is empty
            ValueError: If events are not in sequential version order

        Note:
            Events are applied but NOT added to pending events,
            since they are already persisted.

        Example:
            >>> events = event_store.read("WORK-001")
            >>> item = WorkItem.load_from_history(events)
        """
        if not events:
            raise ValueError("Cannot load from empty event history")

        # Validate events are in order
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
        """
        Validate that events form a valid sequence.

        Args:
            events: Sequence of events to validate

        Raises:
            ValueError: If events are not in sequential order
            ValueError: If events have inconsistent aggregate IDs
        """
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

    def __eq__(self, other: object) -> bool:
        """
        Aggregates are equal if they have the same ID.

        Note: This compares identity, not state. Two aggregates
        with the same ID may have different states if one has
        unpersisted changes.
        """
        if not isinstance(other, AggregateRoot):
            return NotImplemented
        return self._id == other._id

    def __hash__(self) -> int:
        """Hash by ID for set/dict usage."""
        return hash(self._id)

    def __repr__(self) -> str:
        """Informative representation for debugging."""
        return (
            f"{self.__class__.__name__}("
            f"id={self._id!r}, "
            f"version={self._version}, "
            f"pending_events={len(self._pending_events)})"
        )
