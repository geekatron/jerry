# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ISessionRepository - Port for Session Aggregate Persistence.

This port defines the contract for persisting and retrieving Session
aggregates. Since Session is event-sourced, implementations will typically
use an IEventStore under the hood.

References:
    - PAT-002: Repository Pattern
    - ENFORCE-008d.3.2: Session aggregate
"""

from __future__ import annotations

from typing import Protocol

from src.shared_kernel.domain_event import DomainEvent

from ...domain.aggregates.session import Session
from ...domain.value_objects.session_id import SessionId


class ISessionRepository(Protocol):
    """Port for Session aggregate persistence.

    This port abstracts the persistence mechanism for Session aggregates.
    Event-sourced implementations store/retrieve via event replay.

    Thread Safety:
        Implementations MUST ensure thread-safe operations.

    Example:
        >>> repo = EventSourcedSessionRepository(event_store)
        >>> session = Session.create(session_id, description="Bug fix")
        >>> repo.save(session)
        >>> loaded = repo.get(session_id)
    """

    def get(self, session_id: SessionId) -> Session | None:
        """Retrieve a session by ID.

        Args:
            session_id: The session identifier

        Returns:
            Session aggregate if found, None otherwise

        Example:
            >>> session = repo.get(SessionId.parse("sess_abc123"))
        """
        ...

    def get_active(self) -> Session | None:
        """Get the currently active session.

        Returns the most recent session that is in ACTIVE status.
        In Jerry, there should only be one active session at a time.

        Returns:
            The active Session if one exists, None otherwise

        Example:
            >>> active = repo.get_active()
            >>> if active:
            ...     print(f"Active session: {active.id}")
        """
        ...

    def save(self, session: Session) -> list[DomainEvent]:
        """Persist a session (new or updated).

        For event-sourced aggregates, this appends uncommitted events
        to the event store. Returns the collected events so callers
        don't need to call collect_events() separately.

        Args:
            session: The session aggregate to save

        Returns:
            List of domain events that were persisted.

        Raises:
            ConcurrencyError: If optimistic concurrency check fails

        Example:
            >>> session = Session.create(session_id, "Working on feature")
            >>> events = repo.save(session)
        """
        ...

    def exists(self, session_id: SessionId) -> bool:
        """Check if a session exists.

        Args:
            session_id: The session identifier to check

        Returns:
            True if the session exists, False otherwise

        Example:
            >>> if repo.exists(session_id):
            ...     print("Session found")
        """
        ...
