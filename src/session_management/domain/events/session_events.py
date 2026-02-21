# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

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
from typing import Any

from src.shared_kernel.domain_event import DomainEvent


def _utc_now() -> datetime:
    """Return current UTC time."""
    return datetime.now(UTC)


def _generate_event_id() -> str:
    """Generate a unique event ID."""
    from src.shared_kernel.vertex_id import EventId

    return str(EventId.generate())


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

    def _payload(self) -> dict[str, Any]:
        """Return session-specific payload data."""
        return {
            "description": self.description,
            "project_id": self.project_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SessionCreated:
        """Deserialize SessionCreated from dictionary."""
        timestamp_str = data.get("timestamp")
        timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else _utc_now()

        return cls(
            event_id=data.get("event_id", _generate_event_id()),
            aggregate_id=data["aggregate_id"],
            aggregate_type=data["aggregate_type"],
            version=data.get("version", 1),
            timestamp=timestamp,
            description=data.get("description", ""),
            project_id=data.get("project_id"),
        )


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

    def _payload(self) -> dict[str, Any]:
        """Return session-specific payload data."""
        return {
            "summary": self.summary,
            "completed_at": self.completed_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SessionCompleted:
        """Deserialize SessionCompleted from dictionary."""
        timestamp_str = data.get("timestamp")
        timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else _utc_now()

        completed_at_str = data.get("completed_at")
        completed_at = datetime.fromisoformat(completed_at_str) if completed_at_str else _utc_now()

        return cls(
            event_id=data.get("event_id", _generate_event_id()),
            aggregate_id=data["aggregate_id"],
            aggregate_type=data["aggregate_type"],
            version=data.get("version", 1),
            timestamp=timestamp,
            summary=data.get("summary", ""),
            completed_at=completed_at,
        )


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

    def _payload(self) -> dict[str, Any]:
        """Return session-specific payload data."""
        return {
            "reason": self.reason,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SessionAbandoned:
        """Deserialize SessionAbandoned from dictionary."""
        timestamp_str = data.get("timestamp")
        timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else _utc_now()

        return cls(
            event_id=data.get("event_id", _generate_event_id()),
            aggregate_id=data["aggregate_id"],
            aggregate_type=data["aggregate_type"],
            version=data.get("version", 1),
            timestamp=timestamp,
            reason=data.get("reason", ""),
        )


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

    def _payload(self) -> dict[str, Any]:
        """Return session-specific payload data."""
        return {
            "project_id": self.project_id,
            "previous_project_id": self.previous_project_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SessionProjectLinked:
        """Deserialize SessionProjectLinked from dictionary."""
        timestamp_str = data.get("timestamp")
        timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else _utc_now()

        return cls(
            event_id=data.get("event_id", _generate_event_id()),
            aggregate_id=data["aggregate_id"],
            aggregate_type=data["aggregate_type"],
            version=data.get("version", 1),
            timestamp=timestamp,
            project_id=data.get("project_id", ""),
            previous_project_id=data.get("previous_project_id"),
        )
