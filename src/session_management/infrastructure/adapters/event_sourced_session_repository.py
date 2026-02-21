# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
EventSourcedSessionRepository - Event-sourced implementation of ISessionRepository.

Persists Session aggregates via event streams, enabling full history tracking,
event replay, and cross-process persistence. Uses IEventStore for persistence
(injected dependency).

Architecture:
    - Implements ISessionRepository port
    - Uses IEventStore secondary port for persistence
    - Converts between DomainEvent and StoredEvent
    - Reconstitutes Sessions via Session.load_from_history()

References:
    - EN-001: FileSystemSessionRepository
    - PAT-REPO-002: Event-Sourced Repository Pattern
    - TD-018: Event Sourcing for WorkItem Repository (pattern source)

Exports:
    EventSourcedSessionRepository: Event-sourced session repository
"""

from __future__ import annotations

import threading
from typing import Protocol
from uuid import UUID

from src.session_management.domain.aggregates.session import Session, SessionStatus
from src.session_management.domain.events.session_events import (
    SessionAbandoned,
    SessionCompleted,
    SessionCreated,
    SessionProjectLinked,
)
from src.session_management.domain.value_objects.session_id import SessionId
from src.shared_kernel.domain_event import DomainEvent, EventRegistry
from src.work_tracking.domain.ports.event_store import (
    IEventStore,
    StoredEvent,
    StreamNotFoundError,
)


# Extended event store protocol with utility methods
class IEventStoreWithUtilities(IEventStore, Protocol):
    """Extended event store with utility methods for listing streams."""

    def get_all_stream_ids(self) -> list[str]:
        """Get all stream IDs in the store."""
        ...


# =============================================================================
# Event Registry for Session Events
# =============================================================================

# Create a registry for all Session domain events
_session_event_registry = EventRegistry()
_session_event_registry.register(SessionCreated)
_session_event_registry.register(SessionCompleted)
_session_event_registry.register(SessionAbandoned)
_session_event_registry.register(SessionProjectLinked)


def get_session_event_registry() -> EventRegistry:
    """Get the event registry for Session events.

    Returns:
        EventRegistry containing all Session event types.
    """
    return _session_event_registry


# =============================================================================
# Stream ID Convention
# =============================================================================


def _make_stream_id(session_id: str) -> str:
    """Create stream ID from session ID.

    Args:
        session_id: The session identifier string.

    Returns:
        Stream ID in the format 'session-{session_id}'.
    """
    return f"session-{session_id}"


def _extract_session_id(stream_id: str) -> str:
    """Extract session ID from stream ID.

    Args:
        stream_id: The stream identifier string.

    Returns:
        The session identifier extracted from the stream ID.
    """
    if stream_id.startswith("session-"):
        return stream_id[len("session-"):]
    return stream_id


# =============================================================================
# Event Conversion Utilities
# =============================================================================


def _domain_event_to_stored_event(
    event: DomainEvent,
    stream_id: str,
) -> StoredEvent:
    """Convert a DomainEvent to a StoredEvent for persistence.

    Args:
        event: The domain event to convert.
        stream_id: The stream ID for storage.

    Returns:
        StoredEvent ready for persistence.
    """
    # Get event data including event_type
    event_data = event.to_dict()

    # Extract event_id - it's a string, convert to UUID if possible
    event_id_str = event.event_id
    try:
        event_uuid = UUID(event_id_str.replace("EVT-", ""))
    except (ValueError, AttributeError):
        # If can't convert, let StoredEvent generate a new one
        from uuid import uuid4

        event_uuid = uuid4()

    return StoredEvent(
        stream_id=stream_id,
        version=event.version,
        event_type=type(event).__name__,
        data=event_data,
        timestamp=event.timestamp,
        event_id=event_uuid,
    )


def _stored_event_to_domain_event(
    stored_event: StoredEvent,
    registry: EventRegistry,
) -> DomainEvent:
    """Convert a StoredEvent back to a DomainEvent.

    Args:
        stored_event: The stored event from persistence.
        registry: Event registry for type lookup.

    Returns:
        Reconstituted DomainEvent.

    Raises:
        ValueError: If event type is not registered.
    """
    return registry.deserialize(stored_event.data)


# =============================================================================
# EventSourcedSessionRepository
# =============================================================================


class EventSourcedSessionRepository:
    """Event-sourced implementation of ISessionRepository.

    Persists Session aggregates as event streams using the injected IEventStore.
    Sessions are reconstituted by replaying their event history via
    Session.load_from_history().

    Thread Safety:
        All public methods are protected by a threading.RLock for in-process
        thread safety. File-level locking is handled by the underlying
        FileSystemEventStore.

    Example:
        >>> event_store = FileSystemEventStore(project_path)
        >>> repository = EventSourcedSessionRepository(event_store)
        >>> session = Session.create(SessionId.generate(), "Test session")
        >>> repository.save(session)
        >>> loaded = repository.get(SessionId.parse(session.id))
    """

    def __init__(self, event_store: IEventStoreWithUtilities) -> None:
        """Initialize event-sourced session repository.

        Args:
            event_store: The event store for persistence (must support get_all_stream_ids).
        """
        self._event_store = event_store
        self._registry = get_session_event_registry()
        self._lock = threading.RLock()

    def get(self, session_id: SessionId) -> Session | None:
        """Retrieve a session by ID.

        Reads all events for the session and reconstitutes it
        via Session.load_from_history().

        Args:
            session_id: The session identifier.

        Returns:
            The session if found, None otherwise.
        """
        with self._lock:
            stream_id = _make_stream_id(session_id.value)

            if not self._event_store.stream_exists(stream_id):
                return None

            try:
                stored_events = self._event_store.read(stream_id)
            except StreamNotFoundError:
                return None

            if not stored_events:
                return None

            # Convert StoredEvents to DomainEvents
            domain_events = [
                _stored_event_to_domain_event(se, self._registry) for se in stored_events
            ]

            # Reconstitute Session from event history
            return Session.load_from_history(domain_events)

    def get_active(self) -> Session | None:
        """Get the currently active session.

        Returns the most recent session that is in ACTIVE status.
        Scans all session streams and reconstitutes each to check status.

        Returns:
            The active Session if one exists, None otherwise.
        """
        with self._lock:
            stream_ids = self._event_store.get_all_stream_ids()

            # Filter to only session streams
            session_stream_ids = [sid for sid in stream_ids if sid.startswith("session-")]

            for stream_id in session_stream_ids:
                session_id_str = _extract_session_id(stream_id)
                session_id = SessionId.from_string(session_id_str)
                session = self.get(session_id)

                if session is not None and session.status == SessionStatus.ACTIVE:
                    return session

            return None

    def save(self, session: Session) -> list[DomainEvent]:
        """Persist a session by saving its pending events.

        Collects uncommitted events from the session and appends
        them to the event store with optimistic concurrency checking.

        Args:
            session: The session aggregate to save.

        Returns:
            List of domain events that were saved.

        Raises:
            ConcurrencyError: If version mismatch detected.
        """
        with self._lock:
            stream_id = _make_stream_id(session.id)

            # Collect pending events from the aggregate
            pending_events = list(session.collect_events())

            if not pending_events:
                return []  # Nothing to save

            # Convert to stored events
            stored_events = [
                _domain_event_to_stored_event(event, stream_id) for event in pending_events
            ]

            # Calculate expected version
            # If first event is version 1, expected_version should be 0 (new stream)
            # Otherwise, expected_version is the version before the first pending event
            first_event_version = stored_events[0].version
            expected_version = first_event_version - 1

            # For new streams, use -1 (or 0, both accepted)
            if expected_version <= 0:
                expected_version = -1

            # Append to event store
            self._event_store.append(stream_id, stored_events, expected_version)

            # Return the events that were saved
            return pending_events

    def exists(self, session_id: SessionId) -> bool:
        """Check if a session exists.

        Args:
            session_id: The session identifier to check.

        Returns:
            True if the session exists, False otherwise.
        """
        with self._lock:
            stream_id = _make_stream_id(session_id.value)
            return self._event_store.stream_exists(stream_id)


# =============================================================================
# Protocol Compliance Assertion
# =============================================================================


def _assert_protocol_compliance() -> None:
    """Static assertion that EventSourcedSessionRepository implements ISessionRepository."""
    from src.session_management.application.ports.session_repository import (
        ISessionRepository,
    )
    from src.work_tracking.infrastructure.persistence.filesystem_event_store import (
        FileSystemEventStore,
    )

    store: IEventStoreWithUtilities = FileSystemEventStore("/tmp")
    repository: ISessionRepository = EventSourcedSessionRepository(store)
    _ = repository  # Suppress unused variable warning
