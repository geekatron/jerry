# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
InMemorySessionRepository - In-memory session repository for testing/MVP.

A lightweight session repository that stores sessions in memory.
Suitable for testing and initial development.

For production, consider EventSourcedSessionRepository with file-based
event store.

References:
    - PAT-REPO-001: Repository Pattern
    - ENFORCE-008d.3.2: Session aggregate
"""

from __future__ import annotations

import threading

from src.session_management.domain.aggregates.session import Session, SessionStatus
from src.session_management.domain.value_objects.session_id import SessionId
from src.shared_kernel.domain_event import DomainEvent


class InMemorySessionRepository:
    """In-memory session repository implementation.

    Thread-safe repository that stores sessions in a dictionary.
    Sessions are keyed by their session ID.

    This implementation:
    - Stores sessions directly (not event-sourced)
    - Is thread-safe via RLock
    - Loses data on process termination

    Example:
        >>> repo = InMemorySessionRepository()
        >>> session = Session.create(SessionId.generate(), "Test")
        >>> repo.save(session)
        >>> loaded = repo.get(SessionId.parse(session.id))
        >>> loaded.description
        'Test'
    """

    def __init__(self) -> None:
        """Initialize empty repository."""
        self._sessions: dict[str, Session] = {}
        self._lock = threading.RLock()

    def get(self, session_id: SessionId) -> Session | None:
        """Retrieve a session by ID.

        Args:
            session_id: The session identifier

        Returns:
            Session if found, None otherwise
        """
        with self._lock:
            return self._sessions.get(session_id.value)

    def get_active(self) -> Session | None:
        """Get the currently active session.

        Returns:
            The active Session if one exists, None otherwise
        """
        with self._lock:
            for session in self._sessions.values():
                if session.status == SessionStatus.ACTIVE:
                    return session
            return None

    def save(self, session: Session) -> list[DomainEvent]:
        """Persist a session and return collected events.

        Args:
            session: The session to save

        Returns:
            List of domain events collected from the session.
        """
        with self._lock:
            pending_events = list(session.collect_events())
            self._sessions[session.id] = session
            return pending_events

    def exists(self, session_id: SessionId) -> bool:
        """Check if a session exists.

        Args:
            session_id: The session identifier to check

        Returns:
            True if the session exists, False otherwise
        """
        with self._lock:
            return session_id.value in self._sessions

    def clear(self) -> None:
        """Clear all sessions. Useful for testing."""
        with self._lock:
            self._sessions.clear()
