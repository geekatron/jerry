"""Session Domain Events - Facts about session lifecycle.

Domain events for the Session aggregate. These are immutable records
of things that happened to sessions.

Events:
    SessionCreated: A new session was started
    SessionCompleted: A session was successfully completed
    SessionAbandoned: A session was abandoned (e.g., context compaction)
    SessionProjectLinked: A session was linked to a project

References:
    - ENFORCE-008d.3.2: Session aggregate
    - Canon PAT-001: Event Store Interface Pattern
    - DDD Domain Events (Evans, 2004)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from src.shared_kernel.domain_event import DomainEvent


def _utc_now() -> datetime:
    """Return current UTC time."""
    return datetime.now(UTC)


@dataclass(frozen=True)
class SessionCreated(DomainEvent):
    """Event emitted when a new session is created.

    Attributes:
        aggregate_id: The SessionId value
        aggregate_type: Always "Session"
        version: Event version (1 for creation)
        description: Optional session description
        project_id: Optional linked project ID
    """

    description: str = ""
    project_id: str | None = None


@dataclass(frozen=True)
class SessionCompleted(DomainEvent):
    """Event emitted when a session is successfully completed.

    Attributes:
        aggregate_id: The SessionId value
        aggregate_type: Always "Session"
        version: Event version
        summary: Summary of work completed
        completed_at: Completion timestamp
    """

    summary: str = ""
    completed_at: datetime = field(default_factory=_utc_now)


@dataclass(frozen=True)
class SessionAbandoned(DomainEvent):
    """Event emitted when a session is abandoned.

    A session is abandoned when it cannot be properly completed,
    such as during context compaction or unexpected termination.

    Attributes:
        aggregate_id: The SessionId value
        aggregate_type: Always "Session"
        version: Event version
        reason: Reason for abandonment
    """

    reason: str = ""


@dataclass(frozen=True)
class SessionProjectLinked(DomainEvent):
    """Event emitted when a session is linked to a project.

    Attributes:
        aggregate_id: The SessionId value
        aggregate_type: Always "Session"
        version: Event version
        project_id: The linked ProjectId value
        previous_project_id: Previous project ID if re-linking
    """

    project_id: str = ""
    previous_project_id: str | None = None
