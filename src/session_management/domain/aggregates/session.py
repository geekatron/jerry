"""Session Aggregate - Event-sourced aggregate for work session tracking.

The Session aggregate represents a work context for an agent. It tracks
the lifecycle of a session from creation to completion or abandonment.

Lifecycle:
    1. Create via Session.create() factory method
    2. Optionally link to a project via link_project()
    3. Complete via complete() or abandon via abandon()
    4. Persist via repository (collect_events)
    5. Reconstitute via Session.load_from_history()

References:
    - ENFORCE-008d.3.2: Session aggregate
    - Canon PAT-001: AggregateRoot Base Class
    - DDD Aggregate pattern (Evans, 2004)

Exports:
    Session: Event-sourced session aggregate
    SessionStatus: Enum for session lifecycle states
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Sequence

from src.shared_kernel.domain_event import DomainEvent
from src.work_tracking.domain.aggregates.base import AggregateRoot

from ..events.session_events import (
    SessionAbandoned,
    SessionCompleted,
    SessionCreated,
    SessionProjectLinked,
)
from ..value_objects.project_id import ProjectId
from ..value_objects.session_id import SessionId


class SessionStatus(Enum):
    """Lifecycle status for a Session.

    States:
        ACTIVE: Session is active and work is ongoing
        COMPLETED: Session was successfully completed
        ABANDONED: Session was abandoned (e.g., context compaction)
    """

    ACTIVE = "active"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class Session(AggregateRoot):
    """Event-sourced aggregate for work session tracking.

    A Session represents a work context for an agent. It tracks which project
    is being worked on and the lifecycle of the session.

    State Management:
        All state changes emit domain events. State is modified only via
        the _apply() method when processing events, ensuring deterministic
        replay from event history.

    Business Rules:
        - A session starts in ACTIVE status
        - Only ACTIVE sessions can be completed or abandoned
        - Only ACTIVE sessions can have projects linked
        - Once completed or abandoned, a session cannot be modified

    Attributes:
        id: Unique identifier (SessionId value)
        status: Current lifecycle status
        description: Optional session description
        project_id: Linked project ID (if any)
        completed_at: Completion timestamp (if completed)

    Example:
        >>> session = Session.create(
        ...     session_id=SessionId.generate(),
        ...     description="Working on feature X",
        ... )
        >>> session.link_project(project_id)
        >>> session.complete(summary="Feature X implemented")
        >>> events = session.collect_events()
    """

    _aggregate_type: str = "Session"

    # State fields initialized by events
    _status: SessionStatus
    _description: str
    _project_id: str | None
    _completed_at: datetime | None

    # ==========================================================================
    # Factory Methods
    # ==========================================================================

    @classmethod
    def create(
        cls,
        session_id: SessionId,
        description: str = "",
        project_id: ProjectId | None = None,
    ) -> Session:
        """Create a new session.

        Factory method that creates a new Session aggregate by raising
        a SessionCreated event.

        Args:
            session_id: Unique session identity
            description: Optional session description
            project_id: Optional initial project link

        Returns:
            New Session aggregate with ACTIVE status

        Example:
            >>> session = Session.create(
            ...     session_id=SessionId.generate(),
            ...     description="Bug fix session",
            ... )
            >>> session.status
            <SessionStatus.ACTIVE: 'active'>
        """
        # Create instance without calling __init__
        session = cls.__new__(cls)
        session._initialize(session_id.value)

        # Initialize mutable state
        session._project_id = None
        session._completed_at = None

        # Raise creation event
        event = SessionCreated(
            aggregate_id=session_id.value,
            aggregate_type=cls._aggregate_type,
            version=1,
            description=description,
            project_id=project_id.value if project_id else None,
        )
        session._raise_event(event)

        return session

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def status(self) -> SessionStatus:
        """Current lifecycle status."""
        return self._status

    @property
    def description(self) -> str:
        """Session description."""
        return self._description

    @property
    def project_id(self) -> str | None:
        """Linked project ID, if any."""
        return self._project_id

    @property
    def completed_at(self) -> datetime | None:
        """Completion timestamp, if completed."""
        return self._completed_at

    # ==========================================================================
    # Command Methods
    # ==========================================================================

    def complete(self, summary: str = "") -> None:
        """Complete the session.

        Marks the session as successfully completed.

        Args:
            summary: Summary of work completed

        Raises:
            ValueError: If session is already completed or abandoned
        """
        if self._status == SessionStatus.COMPLETED:
            raise ValueError("Session is already completed")
        if self._status == SessionStatus.ABANDONED:
            raise ValueError("Session is already abandoned")

        event = SessionCompleted(
            aggregate_id=self._id,
            aggregate_type=self._aggregate_type,
            version=self._version + 1,
            summary=summary,
        )
        self._raise_event(event)

    def abandon(self, reason: str = "") -> None:
        """Abandon the session.

        Marks the session as abandoned, typically due to context compaction
        or unexpected termination.

        Args:
            reason: Reason for abandonment

        Raises:
            ValueError: If session is already completed or abandoned
        """
        if self._status == SessionStatus.COMPLETED:
            raise ValueError("Session is already completed")
        if self._status == SessionStatus.ABANDONED:
            raise ValueError("Session is already abandoned")

        event = SessionAbandoned(
            aggregate_id=self._id,
            aggregate_type=self._aggregate_type,
            version=self._version + 1,
            reason=reason,
        )
        self._raise_event(event)

    def link_project(self, project_id: ProjectId) -> None:
        """Link this session to a project.

        Args:
            project_id: The project to link to

        Raises:
            ValueError: If session is not active
        """
        if self._status != SessionStatus.ACTIVE:
            raise ValueError(
                f"Cannot link project to session in {self._status.value} status"
            )

        event = SessionProjectLinked(
            aggregate_id=self._id,
            aggregate_type=self._aggregate_type,
            version=self._version + 1,
            project_id=project_id.value,
            previous_project_id=self._project_id,
        )
        self._raise_event(event)

    # ==========================================================================
    # Event Application
    # ==========================================================================

    def _apply(self, event: DomainEvent) -> None:
        """Apply an event to update aggregate state.

        This method is called during event raising and history replay.
        Must be deterministic and side-effect free.

        Args:
            event: The domain event to apply
        """
        if isinstance(event, SessionCreated):
            self._status = SessionStatus.ACTIVE
            self._description = event.description
            self._project_id = event.project_id
            self._completed_at = None

        elif isinstance(event, SessionCompleted):
            self._status = SessionStatus.COMPLETED
            self._completed_at = event.completed_at

        elif isinstance(event, SessionAbandoned):
            self._status = SessionStatus.ABANDONED

        elif isinstance(event, SessionProjectLinked):
            self._project_id = event.project_id

    # ==========================================================================
    # History Replay
    # ==========================================================================

    @classmethod
    def load_from_history(cls, events: Sequence[DomainEvent]) -> Session:
        """Reconstruct Session by replaying events.

        Args:
            events: Historical events in version order

        Returns:
            Session with state rebuilt from events

        Raises:
            ValueError: If events sequence is empty or invalid
        """
        if not events:
            raise ValueError("Cannot load from empty event history")

        # Validate events
        cls._validate_event_sequence(events)

        # Create uninitialized instance
        session = cls.__new__(cls)

        # Initialize from first event
        first_event = events[0]
        session._id = first_event.aggregate_id
        session._version = 0
        session._pending_events = []
        session._created_on = first_event.timestamp
        session._modified_on = None

        # Initialize mutable state
        session._project_id = None
        session._completed_at = None

        # Replay all events
        for event in events:
            session._version = event.version
            session._apply(event)
            session._modified_on = event.timestamp

        return session
