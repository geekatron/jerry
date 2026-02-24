# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for EventSourcedSessionRepository.

Tests verify BDD scenarios from EN-001:
- Save and retrieve a session (round-trip)
- Session survives process termination (cross-process persistence)
- Get active session across all streams
- Abandon session with reason
- Optimistic concurrency prevents concurrent writes
- Event replay reconstitutes session correctly

References:
    - EN-001: FileSystemSessionRepository
    - PAT-REPO-002: Event-Sourced Repository Pattern
    - TD-018: Event Sourcing for WorkItem Repository (pattern source)
"""

from __future__ import annotations

from pathlib import Path

import pytest

from src.session_management.domain.aggregates.session import Session, SessionStatus
from src.session_management.domain.value_objects.project_id import ProjectId
from src.session_management.domain.value_objects.session_id import SessionId
from src.session_management.infrastructure.adapters.event_sourced_session_repository import (
    EventSourcedSessionRepository,
)
from src.work_tracking.domain.ports.event_store import ConcurrencyError
from src.work_tracking.infrastructure.persistence.filesystem_event_store import (
    FileSystemEventStore,
)


@pytest.fixture()
def event_store(tmp_path: Path) -> FileSystemEventStore:
    """Create a FileSystemEventStore backed by a temporary directory."""
    return FileSystemEventStore(tmp_path)


@pytest.fixture()
def repository(event_store: FileSystemEventStore) -> EventSourcedSessionRepository:
    """Create an EventSourcedSessionRepository with a FileSystemEventStore."""
    return EventSourcedSessionRepository(event_store)


@pytest.fixture()
def session_id() -> SessionId:
    """Generate a fresh SessionId for testing."""
    return SessionId.generate()


class TestSaveAndRetrieveSession:
    """BDD: Save and retrieve a session."""

    def test_save_and_get_round_trip(
        self, repository: EventSourcedSessionRepository, session_id: SessionId
    ) -> None:
        """Given a new Session created with id, when saved and retrieved, then matches."""
        # Given
        session = Session.create(session_id, description="Test session")

        # When
        repository.save(session)
        loaded = repository.get(session_id)

        # Then
        assert loaded is not None
        assert loaded.id == session_id.value
        assert loaded.status == SessionStatus.ACTIVE

    def test_save_and_get_preserves_description(
        self, repository: EventSourcedSessionRepository, session_id: SessionId
    ) -> None:
        """Saved session preserves description through round-trip."""
        session = Session.create(session_id, description="Working on EN-001")
        repository.save(session)

        loaded = repository.get(session_id)

        assert loaded is not None
        assert loaded.description == "Working on EN-001"

    def test_get_nonexistent_session_returns_none(
        self, repository: EventSourcedSessionRepository
    ) -> None:
        """Getting a non-existent session returns None."""
        missing_id = SessionId.generate()
        result = repository.get(missing_id)
        assert result is None


class TestCrossProcessPersistence:
    """BDD: Session survives process termination."""

    def test_session_survives_new_repository_instance(
        self, event_store: FileSystemEventStore, session_id: SessionId
    ) -> None:
        """Given a saved session, when a new repository instance is created, session is retrievable."""
        # Given: save session via first repository instance
        repo1 = EventSourcedSessionRepository(event_store)
        session = Session.create(session_id, description="Cross-process test")
        repo1.save(session)

        # When: create a new repository instance (simulating new process)
        repo2 = EventSourcedSessionRepository(event_store)
        loaded = repo2.get(session_id)

        # Then
        assert loaded is not None
        assert loaded.id == session_id.value
        assert loaded.status == SessionStatus.ACTIVE
        assert loaded.description == "Cross-process test"

    def test_session_survives_new_event_store_instance(
        self, tmp_path: Path, session_id: SessionId
    ) -> None:
        """Given a saved session, when new event store AND repository are created, session persists."""
        # Given: save via first event store + repository
        store1 = FileSystemEventStore(tmp_path)
        repo1 = EventSourcedSessionRepository(store1)
        session = Session.create(session_id, description="Full restart test")
        repo1.save(session)

        # When: create entirely new event store and repository (simulating process restart)
        store2 = FileSystemEventStore(tmp_path)
        repo2 = EventSourcedSessionRepository(store2)
        loaded = repo2.get(session_id)

        # Then
        assert loaded is not None
        assert loaded.id == session_id.value
        assert loaded.description == "Full restart test"


class TestGetActiveSession:
    """BDD: Get active session across all streams."""

    def test_get_active_returns_active_session(
        self, repository: EventSourcedSessionRepository
    ) -> None:
        """Given an active session, get_active returns it."""
        session_id = SessionId.generate()
        session = Session.create(session_id, description="Active session")
        repository.save(session)

        active = repository.get_active()

        assert active is not None
        assert active.id == session_id.value
        assert active.status == SessionStatus.ACTIVE

    def test_get_active_excludes_completed_sessions(
        self, repository: EventSourcedSessionRepository
    ) -> None:
        """Given active and completed sessions, get_active returns only the active one."""
        # Create active session
        active_id = SessionId.generate()
        active_session = Session.create(active_id, description="Active")
        repository.save(active_session)

        # Create and complete another session
        completed_id = SessionId.generate()
        completed_session = Session.create(completed_id, description="Completed")
        completed_session.complete(summary="Done")
        repository.save(completed_session)

        # When
        active = repository.get_active()

        # Then
        assert active is not None
        assert active.id == active_id.value

    def test_get_active_excludes_abandoned_sessions(
        self, repository: EventSourcedSessionRepository
    ) -> None:
        """Given active and abandoned sessions, get_active returns only the active one."""
        # Create active session
        active_id = SessionId.generate()
        active_session = Session.create(active_id, description="Active")
        repository.save(active_session)

        # Create and abandon another session
        abandoned_id = SessionId.generate()
        abandoned_session = Session.create(abandoned_id, description="Abandoned")
        abandoned_session.abandon(reason="context compaction")
        repository.save(abandoned_session)

        # When
        active = repository.get_active()

        # Then
        assert active is not None
        assert active.id == active_id.value

    def test_get_active_returns_none_when_no_active_sessions(
        self, repository: EventSourcedSessionRepository
    ) -> None:
        """Given only completed sessions, get_active returns None."""
        completed_id = SessionId.generate()
        completed_session = Session.create(completed_id, description="Completed")
        completed_session.complete(summary="Done")
        repository.save(completed_session)

        active = repository.get_active()

        assert active is None

    def test_get_active_returns_none_for_empty_repository(
        self, repository: EventSourcedSessionRepository
    ) -> None:
        """Given an empty repository, get_active returns None."""
        active = repository.get_active()
        assert active is None


class TestAbandonSessionWithReason:
    """BDD: Abandon session with reason."""

    def test_abandon_persists_status_and_reason(
        self, repository: EventSourcedSessionRepository
    ) -> None:
        """Given an active session, when abandoned with reason, status and reason persist."""
        session_id = SessionId.generate()
        session = Session.create(session_id, description="To be abandoned")
        session.abandon(reason="context compaction at 82%")
        repository.save(session)

        # Reload from repository
        loaded = repository.get(session_id)

        assert loaded is not None
        assert loaded.status == SessionStatus.ABANDONED

    def test_abandon_event_in_stream(
        self, repository: EventSourcedSessionRepository, event_store: FileSystemEventStore
    ) -> None:
        """The event stream should contain a SessionAbandoned event."""
        session_id = SessionId.generate()
        session = Session.create(session_id, description="To be abandoned")
        session.abandon(reason="context compaction at 82%")
        repository.save(session)

        # Read raw events from the event store
        stream_id = f"session-{session_id.value}"
        stored_events = event_store.read(stream_id)
        event_types = [se.event_type for se in stored_events]

        assert "SessionAbandoned" in event_types


class TestOptimisticConcurrency:
    """BDD: Optimistic concurrency prevents concurrent writes."""

    def test_concurrent_save_raises_concurrency_error(
        self, event_store: FileSystemEventStore
    ) -> None:
        """Given a session at version N, two concurrent saves should conflict."""
        session_id = SessionId.generate()

        # Create and save initial session
        session = Session.create(session_id, description="Concurrency test")
        repo = EventSourcedSessionRepository(event_store)
        repo.save(session)

        # Load session from two separate "processes"
        loaded1 = repo.get(session_id)
        loaded2 = repo.get(session_id)

        assert loaded1 is not None
        assert loaded2 is not None

        # Both modify the session
        loaded1.abandon(reason="first writer")
        loaded2.abandon(reason="second writer")

        # First save succeeds
        repo.save(loaded1)

        # Second save should raise ConcurrencyError
        with pytest.raises(ConcurrencyError):
            repo.save(loaded2)


class TestEventReplayReconstitution:
    """BDD: Event replay reconstitutes session correctly."""

    def test_replay_created_and_project_linked_and_abandoned(
        self, repository: EventSourcedSessionRepository
    ) -> None:
        """Given events: Created, ProjectLinked, Abandoned, session state is correct."""
        session_id = SessionId.generate()
        project_id = ProjectId.create(1, "test-project")

        # Create session with full lifecycle
        session = Session.create(session_id, description="Full lifecycle")
        session.link_project(project_id)
        session.abandon(reason="context compaction")
        repository.save(session)

        # Reload from repository (triggers event replay)
        loaded = repository.get(session_id)

        assert loaded is not None
        assert loaded.project_id == project_id.value
        assert loaded.status == SessionStatus.ABANDONED

    def test_replay_preserves_version(self, repository: EventSourcedSessionRepository) -> None:
        """Replayed session has correct version number."""
        session_id = SessionId.generate()
        project_id = ProjectId.create(2, "version-test")

        session = Session.create(session_id, description="Version test")
        session.link_project(project_id)
        session.abandon(reason="done")
        repository.save(session)

        loaded = repository.get(session_id)

        assert loaded is not None
        # Version should be 3: Created(1) + ProjectLinked(2) + Abandoned(3)
        assert loaded.version == 3


class TestExists:
    """Tests for the exists() method."""

    def test_exists_returns_true_for_saved_session(
        self, repository: EventSourcedSessionRepository
    ) -> None:
        """Exists returns True for a saved session."""
        session_id = SessionId.generate()
        session = Session.create(session_id, description="Exists test")
        repository.save(session)

        assert repository.exists(session_id) is True

    def test_exists_returns_false_for_unsaved_session(
        self, repository: EventSourcedSessionRepository
    ) -> None:
        """Exists returns False for an unsaved session."""
        session_id = SessionId.generate()
        assert repository.exists(session_id) is False


class TestSaveIdempotency:
    """Tests for save behavior with no pending events."""

    def test_save_with_no_pending_events_is_noop(
        self, repository: EventSourcedSessionRepository
    ) -> None:
        """Saving a session with no pending events does not raise."""
        session_id = SessionId.generate()
        session = Session.create(session_id, description="Idempotent save")
        repository.save(session)

        # Load session (no pending events after load)
        loaded = repository.get(session_id)
        assert loaded is not None

        # Save again should be a no-op (no pending events)
        repository.save(loaded)

        # Session should still be retrievable
        reloaded = repository.get(session_id)
        assert reloaded is not None
        assert reloaded.id == session_id.value
