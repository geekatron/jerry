"""Unit tests for Session aggregate.

Test Categories:
    - AggregateRoot Compliance: Event sourcing pattern implementation
    - Factory Method: Session.create() behavior
    - Lifecycle Commands: start, complete, abandon
    - Event Emission: Correct domain events raised
    - History Replay: Reconstitution from events
    - Edge Cases: Boundary conditions and error handling

References:
    - ENFORCE-008d.3.2: Session aggregate
    - Canon PAT-001: AggregateRoot Base Class
    - DDD Aggregate pattern (Evans, 2004)
"""

from __future__ import annotations

from datetime import datetime

import pytest

from src.session_management.domain.aggregates.session import (
    Session,
    SessionStatus,
)
from src.session_management.domain.events.session_events import (
    SessionAbandoned,
    SessionCompleted,
    SessionCreated,
    SessionProjectLinked,
)
from src.session_management.domain.value_objects.project_id import ProjectId
from src.session_management.domain.value_objects.session_id import SessionId
from src.work_tracking.domain.aggregates.base import AggregateRoot

# =============================================================================
# AggregateRoot Compliance Tests (I-008d.3.2.1)
# =============================================================================


class TestSessionAggregateRootCompliance:
    """Tests for AggregateRoot pattern compliance."""

    def test_session_extends_aggregate_root(self) -> None:
        """Session should inherit from AggregateRoot base class."""
        session_id = SessionId.generate()
        session = Session.create(session_id)
        assert isinstance(session, AggregateRoot)

    def test_session_has_id_property(self) -> None:
        """Session should have id property from AggregateRoot."""
        session_id = SessionId.generate()
        session = Session.create(session_id)
        assert hasattr(session, "id")
        assert session.id == session_id.value

    def test_session_has_version_property(self) -> None:
        """Session should track version for optimistic concurrency."""
        session_id = SessionId.generate()
        session = Session.create(session_id)
        assert hasattr(session, "version")
        assert session.version == 1  # After creation event

    def test_session_emits_events_on_state_change(self) -> None:
        """State changes should emit domain events."""
        session_id = SessionId.generate()
        session = Session.create(session_id)
        events = session.collect_events()
        assert len(events) >= 1
        assert isinstance(events[0], SessionCreated)

    def test_session_can_replay_from_history(self) -> None:
        """Session should be reconstructable from event history."""
        session_id = SessionId.generate()
        original = Session.create(session_id)
        events = original.collect_events()

        restored = Session.load_from_history(events)

        assert restored.id == original.id
        assert restored.version == original.version
        assert restored.status == original.status


# =============================================================================
# Factory Method Tests (I-008d.3.2.2)
# =============================================================================


class TestSessionCreate:
    """Tests for Session.create() factory method."""

    def test_create_with_session_id(self) -> None:
        """create() should accept SessionId."""
        session_id = SessionId.generate()
        session = Session.create(session_id)
        assert session.id == session_id.value

    def test_create_sets_active_status(self) -> None:
        """Newly created session should have ACTIVE status."""
        session_id = SessionId.generate()
        session = Session.create(session_id)
        assert session.status == SessionStatus.ACTIVE

    def test_create_emits_session_created_event(self) -> None:
        """create() should emit SessionCreated event."""
        session_id = SessionId.generate()
        session = Session.create(session_id)
        events = session.collect_events()
        assert len(events) == 1
        assert isinstance(events[0], SessionCreated)
        assert events[0].aggregate_id == session_id.value

    def test_create_with_project_id(self) -> None:
        """create() should accept optional project_id."""
        session_id = SessionId.generate()
        project_id = ProjectId.from_string("PROJ-001-test-project")
        session = Session.create(session_id, project_id=project_id)
        assert session.project_id == project_id.value

    def test_create_without_project_id(self) -> None:
        """create() without project_id should have None."""
        session_id = SessionId.generate()
        session = Session.create(session_id)
        assert session.project_id is None

    def test_create_with_description(self) -> None:
        """create() should accept optional description."""
        session_id = SessionId.generate()
        session = Session.create(session_id, description="Test session")
        assert session.description == "Test session"


# =============================================================================
# Lifecycle Command Tests (I-008d.3.2.3)
# =============================================================================


class TestSessionLifecycle:
    """Tests for session lifecycle state transitions."""

    def test_complete_from_active(self) -> None:
        """Active session can be completed."""
        session_id = SessionId.generate()
        session = Session.create(session_id)
        session.complete(summary="Work completed successfully")
        assert session.status == SessionStatus.COMPLETED

    def test_complete_emits_session_completed_event(self) -> None:
        """complete() should emit SessionCompleted event."""
        session_id = SessionId.generate()
        session = Session.create(session_id)
        session.collect_events()  # Clear creation event
        session.complete(summary="Done")
        events = session.collect_events()
        assert len(events) == 1
        assert isinstance(events[0], SessionCompleted)
        assert events[0].summary == "Done"

    def test_complete_sets_completed_at(self) -> None:
        """complete() should set completed_at timestamp."""
        session_id = SessionId.generate()
        session = Session.create(session_id)
        session.complete(summary="Done")
        assert session.completed_at is not None
        assert isinstance(session.completed_at, datetime)

    def test_complete_already_completed_raises(self) -> None:
        """Completing an already completed session should raise."""
        session_id = SessionId.generate()
        session = Session.create(session_id)
        session.complete(summary="Done")
        with pytest.raises(ValueError, match="already completed"):
            session.complete(summary="Again")

    def test_abandon_from_active(self) -> None:
        """Active session can be abandoned."""
        session_id = SessionId.generate()
        session = Session.create(session_id)
        session.abandon(reason="Context compaction")
        assert session.status == SessionStatus.ABANDONED

    def test_abandon_emits_session_abandoned_event(self) -> None:
        """abandon() should emit SessionAbandoned event."""
        session_id = SessionId.generate()
        session = Session.create(session_id)
        session.collect_events()  # Clear creation event
        session.abandon(reason="Lost context")
        events = session.collect_events()
        assert len(events) == 1
        assert isinstance(events[0], SessionAbandoned)
        assert events[0].reason == "Lost context"

    def test_abandon_already_abandoned_raises(self) -> None:
        """Abandoning an already abandoned session should raise."""
        session_id = SessionId.generate()
        session = Session.create(session_id)
        session.abandon(reason="First")
        with pytest.raises(ValueError, match="already abandoned"):
            session.abandon(reason="Second")


# =============================================================================
# Project Linking Tests (I-008d.3.2.4)
# =============================================================================


class TestSessionProjectLinking:
    """Tests for linking sessions to projects."""

    def test_link_project_to_active_session(self) -> None:
        """Active session can be linked to a project."""
        session_id = SessionId.generate()
        project_id = ProjectId.from_string("PROJ-001-my-project")
        session = Session.create(session_id)
        session.link_project(project_id)
        assert session.project_id == project_id.value

    def test_link_project_emits_event(self) -> None:
        """link_project() should emit SessionProjectLinked event."""
        session_id = SessionId.generate()
        project_id = ProjectId.from_string("PROJ-001-my-project")
        session = Session.create(session_id)
        session.collect_events()  # Clear creation event
        session.link_project(project_id)
        events = session.collect_events()
        assert len(events) == 1
        assert isinstance(events[0], SessionProjectLinked)
        assert events[0].project_id == project_id.value

    def test_link_project_to_completed_session_raises(self) -> None:
        """Linking project to completed session should raise."""
        session_id = SessionId.generate()
        project_id = ProjectId.from_string("PROJ-001-my-project")
        session = Session.create(session_id)
        session.complete(summary="Done")
        with pytest.raises(ValueError, match="Cannot link project"):
            session.link_project(project_id)

    def test_relink_project_updates_value(self) -> None:
        """Re-linking project should update to new value."""
        session_id = SessionId.generate()
        project_id_1 = ProjectId.from_string("PROJ-001-first")
        project_id_2 = ProjectId.from_string("PROJ-002-second")
        session = Session.create(session_id)
        session.link_project(project_id_1)
        session.link_project(project_id_2)
        assert session.project_id == project_id_2.value


# =============================================================================
# Event Application Tests (I-008d.3.2.5)
# =============================================================================


class TestSessionEventApplication:
    """Tests for event application and state reconstruction."""

    def test_apply_session_created(self) -> None:
        """SessionCreated event should set initial state."""
        session_id = SessionId.generate()
        session = Session.create(session_id, description="Test")
        assert session.status == SessionStatus.ACTIVE
        assert session.description == "Test"
        assert session.project_id is None

    def test_apply_session_completed(self) -> None:
        """SessionCompleted event should update status and timestamp."""
        session_id = SessionId.generate()
        session = Session.create(session_id)
        session.complete(summary="Done")
        assert session.status == SessionStatus.COMPLETED
        assert session.completed_at is not None

    def test_apply_session_abandoned(self) -> None:
        """SessionAbandoned event should update status."""
        session_id = SessionId.generate()
        session = Session.create(session_id)
        session.abandon(reason="Context lost")
        assert session.status == SessionStatus.ABANDONED

    def test_apply_session_project_linked(self) -> None:
        """SessionProjectLinked event should update project_id."""
        session_id = SessionId.generate()
        project_id = ProjectId.from_string("PROJ-001-my-project")
        session = Session.create(session_id)
        session.link_project(project_id)
        assert session.project_id == project_id.value


# =============================================================================
# History Replay Tests (I-008d.3.2.6)
# =============================================================================


class TestSessionHistoryReplay:
    """Tests for reconstructing Session from event history."""

    def test_replay_simple_lifecycle(self) -> None:
        """Replay create → complete lifecycle."""
        session_id = SessionId.generate()
        original = Session.create(session_id, description="Test session")
        original.complete(summary="Work done")
        events = original.collect_events()

        restored = Session.load_from_history(events)

        assert restored.id == original.id
        assert restored.status == SessionStatus.COMPLETED
        assert restored.description == "Test session"

    def test_replay_with_project_link(self) -> None:
        """Replay create → link_project → complete lifecycle."""
        session_id = SessionId.generate()
        project_id = ProjectId.from_string("PROJ-001-my-project")
        original = Session.create(session_id)
        original.link_project(project_id)
        original.complete(summary="Done")
        events = original.collect_events()

        restored = Session.load_from_history(events)

        assert restored.project_id == project_id.value
        assert restored.status == SessionStatus.COMPLETED

    def test_replay_empty_history_raises(self) -> None:
        """Replaying empty event history should raise ValueError."""
        with pytest.raises(ValueError, match="empty event history"):
            Session.load_from_history([])

    def test_replay_preserves_version(self) -> None:
        """Replayed session should have correct version."""
        session_id = SessionId.generate()
        original = Session.create(session_id)  # version 1
        original.complete(summary="Done")  # version 2
        events = original.collect_events()

        restored = Session.load_from_history(events)

        assert restored.version == 2


# =============================================================================
# Edge Cases Tests (I-008d.3.2.7)
# =============================================================================


class TestSessionEdgeCases:
    """Edge case and boundary tests."""

    def test_session_equality_by_id(self) -> None:
        """Two sessions with same ID should be equal."""
        session_id = SessionId.generate()
        session1 = Session.create(session_id)
        events = session1.collect_events()
        session2 = Session.load_from_history(events)
        assert session1 == session2

    def test_session_hash_uses_id(self) -> None:
        """Session hash should be based on ID."""
        session_id = SessionId.generate()
        session = Session.create(session_id)
        assert hash(session) == hash(session_id.value)

    def test_session_can_use_in_set(self) -> None:
        """Session should work in sets."""
        session_id = SessionId.generate()
        session = Session.create(session_id)
        events = session.collect_events()
        restored = Session.load_from_history(events)

        session_set = {session, restored}
        assert len(session_set) == 1  # Same ID

    def test_no_pending_events_after_collect(self) -> None:
        """collect_events() should clear pending events."""
        session_id = SessionId.generate()
        session = Session.create(session_id)
        events1 = session.collect_events()
        events2 = session.collect_events()
        assert len(events1) == 1
        assert len(events2) == 0

    def test_repr_shows_useful_info(self) -> None:
        """__repr__ should show session info."""
        session_id = SessionId.generate()
        session = Session.create(session_id)
        repr_str = repr(session)
        assert "Session" in repr_str
        assert session_id.value in repr_str

    def test_created_on_set_from_first_event(self) -> None:
        """created_on should be set from first event's timestamp."""
        session_id = SessionId.generate()
        session = Session.create(session_id)
        assert session.created_on is not None
        assert isinstance(session.created_on, datetime)
