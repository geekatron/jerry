"""Unit tests for Session Command and Query Handlers.

Test Categories:
    - CreateSessionCommandHandler: Start new sessions
    - EndSessionCommandHandler: Complete sessions
    - AbandonSessionCommandHandler: Abandon sessions
    - GetSessionStatusQueryHandler: Query session status

References:
    - ENFORCE-009: Application Layer Tests
    - CQRS Pattern: Commands return events, Queries return DTOs
"""

from __future__ import annotations

from datetime import datetime
from unittest.mock import Mock

import pytest

from src.session_management.application.commands import (
    AbandonSessionCommand,
    CreateSessionCommand,
    EndSessionCommand,
)
from src.session_management.application.handlers.commands import (
    AbandonSessionCommandHandler,
    CreateSessionCommandHandler,
    EndSessionCommandHandler,
)
from src.session_management.application.handlers.commands.create_session_command_handler import (
    SessionAlreadyActiveError,
)
from src.session_management.application.handlers.commands.end_session_command_handler import (
    NoActiveSessionError,
)
from src.session_management.application.handlers.queries import GetSessionStatusQueryHandler
from src.session_management.application.queries import GetSessionStatusQuery
from src.session_management.domain.aggregates.session import Session, SessionStatus
from src.session_management.domain.events.session_events import (
    SessionAbandoned,
    SessionCompleted,
    SessionCreated,
)
from src.session_management.domain.value_objects.session_id import SessionId


# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def mock_repository() -> Mock:
    """Create a mock ISessionRepository."""
    return Mock()


@pytest.fixture
def active_session() -> Session:
    """Create an active session for testing."""
    session = Session.create(
        session_id=SessionId.generate(),
        description="Test session",
    )
    # Clear creation events by collecting them
    session.collect_events()
    return session


@pytest.fixture
def completed_session() -> Session:
    """Create a completed session for testing."""
    session = Session.create(
        session_id=SessionId.generate(),
        description="Completed session",
    )
    session.complete()
    session.collect_events()
    return session


# =============================================================================
# CreateSessionCommandHandler Tests
# =============================================================================


class TestCreateSessionCommandHandlerHappyPath:
    """Happy path tests for CreateSessionCommandHandler."""

    def test_create_session_returns_created_event(self, mock_repository: Mock) -> None:
        """create_session should return SessionCreated event."""
        mock_repository.get_active.return_value = None

        handler = CreateSessionCommandHandler(repository=mock_repository)
        command = CreateSessionCommand(description="New session")
        events = handler.handle(command)

        assert len(events) == 1
        assert isinstance(events[0], SessionCreated)

    def test_create_session_saves_to_repository(self, mock_repository: Mock) -> None:
        """create_session should save the new session to repository."""
        mock_repository.get_active.return_value = None

        handler = CreateSessionCommandHandler(repository=mock_repository)
        command = CreateSessionCommand(description="New session")
        handler.handle(command)

        mock_repository.save.assert_called_once()
        saved_session = mock_repository.save.call_args[0][0]
        assert isinstance(saved_session, Session)
        assert saved_session.description == "New session"

    def test_create_session_with_project_id(self, mock_repository: Mock) -> None:
        """create_session should accept optional project_id."""
        mock_repository.get_active.return_value = None

        handler = CreateSessionCommandHandler(repository=mock_repository)
        command = CreateSessionCommand(
            description="Project session",
            project_id="PROJ-001-test",
        )
        handler.handle(command)

        saved_session = mock_repository.save.call_args[0][0]
        assert saved_session.project_id == "PROJ-001-test"

    def test_create_session_with_no_description(self, mock_repository: Mock) -> None:
        """create_session should work without description."""
        mock_repository.get_active.return_value = None

        handler = CreateSessionCommandHandler(repository=mock_repository)
        command = CreateSessionCommand()
        events = handler.handle(command)

        assert len(events) == 1
        saved_session = mock_repository.save.call_args[0][0]
        assert saved_session.description == ""


class TestCreateSessionCommandHandlerErrors:
    """Error case tests for CreateSessionCommandHandler."""

    def test_create_session_when_active_exists_raises_error(
        self, mock_repository: Mock, active_session: Session
    ) -> None:
        """create_session should raise error if active session exists."""
        mock_repository.get_active.return_value = active_session

        handler = CreateSessionCommandHandler(repository=mock_repository)
        command = CreateSessionCommand(description="Another session")

        with pytest.raises(SessionAlreadyActiveError) as exc_info:
            handler.handle(command)

        assert active_session.id in str(exc_info.value)


# =============================================================================
# EndSessionCommandHandler Tests
# =============================================================================


class TestEndSessionCommandHandlerHappyPath:
    """Happy path tests for EndSessionCommandHandler."""

    def test_end_session_returns_completed_event(
        self, mock_repository: Mock, active_session: Session
    ) -> None:
        """end_session should return SessionCompleted event."""
        mock_repository.get_active.return_value = active_session

        handler = EndSessionCommandHandler(repository=mock_repository)
        command = EndSessionCommand(summary="Work completed")
        events = handler.handle(command)

        assert len(events) == 1
        assert isinstance(events[0], SessionCompleted)

    def test_end_session_saves_to_repository(
        self, mock_repository: Mock, active_session: Session
    ) -> None:
        """end_session should save the completed session."""
        mock_repository.get_active.return_value = active_session

        handler = EndSessionCommandHandler(repository=mock_repository)
        command = EndSessionCommand(summary="Work completed")
        handler.handle(command)

        mock_repository.save.assert_called_once()
        saved_session = mock_repository.save.call_args[0][0]
        assert saved_session.status == SessionStatus.COMPLETED

    def test_end_session_with_no_summary(
        self, mock_repository: Mock, active_session: Session
    ) -> None:
        """end_session should work without summary."""
        mock_repository.get_active.return_value = active_session

        handler = EndSessionCommandHandler(repository=mock_repository)
        command = EndSessionCommand()
        events = handler.handle(command)

        assert len(events) == 1
        assert isinstance(events[0], SessionCompleted)


class TestEndSessionCommandHandlerErrors:
    """Error case tests for EndSessionCommandHandler."""

    def test_end_session_when_no_active_raises_error(self, mock_repository: Mock) -> None:
        """end_session should raise error if no active session."""
        mock_repository.get_active.return_value = None

        handler = EndSessionCommandHandler(repository=mock_repository)
        command = EndSessionCommand(summary="Work completed")

        with pytest.raises(NoActiveSessionError):
            handler.handle(command)


# =============================================================================
# AbandonSessionCommandHandler Tests
# =============================================================================


class TestAbandonSessionCommandHandlerHappyPath:
    """Happy path tests for AbandonSessionCommandHandler."""

    def test_abandon_session_returns_abandoned_event(
        self, mock_repository: Mock, active_session: Session
    ) -> None:
        """abandon_session should return SessionAbandoned event."""
        mock_repository.get_active.return_value = active_session

        handler = AbandonSessionCommandHandler(repository=mock_repository)
        command = AbandonSessionCommand(reason="Context compaction")
        events = handler.handle(command)

        assert len(events) == 1
        assert isinstance(events[0], SessionAbandoned)

    def test_abandon_session_saves_to_repository(
        self, mock_repository: Mock, active_session: Session
    ) -> None:
        """abandon_session should save the abandoned session."""
        mock_repository.get_active.return_value = active_session

        handler = AbandonSessionCommandHandler(repository=mock_repository)
        command = AbandonSessionCommand(reason="Context compaction")
        handler.handle(command)

        mock_repository.save.assert_called_once()
        saved_session = mock_repository.save.call_args[0][0]
        assert saved_session.status == SessionStatus.ABANDONED

    def test_abandon_session_with_no_reason(
        self, mock_repository: Mock, active_session: Session
    ) -> None:
        """abandon_session should work without reason."""
        mock_repository.get_active.return_value = active_session

        handler = AbandonSessionCommandHandler(repository=mock_repository)
        command = AbandonSessionCommand()
        events = handler.handle(command)

        assert len(events) == 1
        assert isinstance(events[0], SessionAbandoned)


class TestAbandonSessionCommandHandlerErrors:
    """Error case tests for AbandonSessionCommandHandler."""

    def test_abandon_session_when_no_active_raises_error(self, mock_repository: Mock) -> None:
        """abandon_session should raise error if no active session."""
        mock_repository.get_active.return_value = None

        handler = AbandonSessionCommandHandler(repository=mock_repository)
        command = AbandonSessionCommand(reason="Test abandonment")

        # AbandonSessionCommandHandler also uses NoActiveSessionError
        # Import it from its definition module
        from src.session_management.application.handlers.commands.abandon_session_command_handler import (
            NoActiveSessionError as AbandonNoActiveSessionError,
        )

        with pytest.raises(AbandonNoActiveSessionError):
            handler.handle(command)


# =============================================================================
# GetSessionStatusQueryHandler Tests
# =============================================================================


class TestGetSessionStatusQueryHandlerHappyPath:
    """Happy path tests for GetSessionStatusQueryHandler."""

    def test_status_when_no_session_returns_inactive(self, mock_repository: Mock) -> None:
        """status should return has_active_session=False when no session."""
        mock_repository.get_active.return_value = None

        handler = GetSessionStatusQueryHandler(repository=mock_repository)
        query = GetSessionStatusQuery()
        result = handler.handle(query)

        assert result.has_active_session is False
        assert result.session_id is None
        assert result.status is None

    def test_status_when_active_returns_session_info(
        self, mock_repository: Mock, active_session: Session
    ) -> None:
        """status should return session info when active session exists."""
        mock_repository.get_active.return_value = active_session

        handler = GetSessionStatusQueryHandler(repository=mock_repository)
        query = GetSessionStatusQuery()
        result = handler.handle(query)

        assert result.has_active_session is True
        assert result.session_id == active_session.id
        assert result.status == "active"
        assert result.description == "Test session"

    def test_status_returns_all_session_fields(
        self, mock_repository: Mock, active_session: Session
    ) -> None:
        """status should return all relevant session fields."""
        # Add project_id to the session for testing
        active_session._project_id = "PROJ-001-test"
        mock_repository.get_active.return_value = active_session

        handler = GetSessionStatusQueryHandler(repository=mock_repository)
        query = GetSessionStatusQuery()
        result = handler.handle(query)

        assert result.has_active_session is True
        assert result.session_id is not None
        assert result.status == "active"
        assert result.description == "Test session"
        assert result.project_id == "PROJ-001-test"
        assert result.started_at is not None
        assert isinstance(result.started_at, datetime)


# =============================================================================
# Edge Cases
# =============================================================================


class TestSessionHandlerEdgeCases:
    """Edge case tests for session handlers."""

    def test_create_multiple_sessions_sequentially(self, mock_repository: Mock) -> None:
        """Should be able to create sessions after previous ones end."""
        # First session
        mock_repository.get_active.return_value = None
        handler = CreateSessionCommandHandler(repository=mock_repository)
        command = CreateSessionCommand(description="Session 1")
        events = handler.handle(command)
        session1_id = events[0].aggregate_id

        # Simulate session end (mock returns None now)
        mock_repository.get_active.return_value = None

        # Second session
        command = CreateSessionCommand(description="Session 2")
        events = handler.handle(command)
        session2_id = events[0].aggregate_id

        assert session1_id != session2_id

    def test_handler_receives_correct_repository(self, mock_repository: Mock) -> None:
        """Handler should use injected repository."""
        mock_repository.get_active.return_value = None

        handler = CreateSessionCommandHandler(repository=mock_repository)
        handler.handle(CreateSessionCommand())

        mock_repository.get_active.assert_called_once()
        mock_repository.save.assert_called_once()
