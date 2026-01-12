"""
Unit tests for RetrieveProjectContextQueryHandler.

Tests the handler with mocked dependencies.

Test Distribution per impl-es-e-003:
- Happy Path (60%): 4 tests - Valid project, project not set, handler protocol, dispatcher registration
- Negative (30%): 2 tests - Invalid project format, repository error
- Edge (10%): 1 test - Empty projects directory
"""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from src.application.handlers.queries import RetrieveProjectContextQueryHandler
from src.application.queries import RetrieveProjectContextQuery


# === Happy Path Tests (60%) ===


class TestGetProjectContextHandlerHappyPath:
    """Happy path tests for RetrieveProjectContextQueryHandler."""

    def test_handler_is_importable(self) -> None:
        """RetrieveProjectContextQueryHandler can be imported."""
        from src.application.handlers.queries import RetrieveProjectContextQueryHandler

        assert RetrieveProjectContextQueryHandler is not None

    def test_handler_returns_context_when_project_set(self) -> None:
        """Handler returns full context when JERRY_PROJECT is set."""
        # Arrange - mock dependencies
        mock_repository = Mock()
        mock_environment = Mock()

        mock_environment.get_env.return_value = "PROJ-001-test"

        mock_project_info = Mock()
        mock_project_info.id.number = 1
        mock_repository.scan_projects.return_value = [mock_project_info]

        mock_validation = Mock()
        mock_validation.is_valid = True
        mock_repository.validate_project.return_value = mock_validation

        handler = RetrieveProjectContextQueryHandler(
            repository=mock_repository,
            environment=mock_environment,
        )

        query = RetrieveProjectContextQuery(base_path="/projects")

        # Act
        result = handler.handle(query)

        # Assert
        assert result["jerry_project"] == "PROJ-001-test"
        assert result["project_id"] is not None
        assert result["validation"] is not None

    def test_handler_returns_context_when_project_not_set(self) -> None:
        """Handler returns context with available projects when JERRY_PROJECT not set."""
        # Arrange
        mock_repository = Mock()
        mock_environment = Mock()

        mock_environment.get_env.return_value = None

        mock_project_info = Mock()
        mock_project_info.id.number = 1
        mock_repository.scan_projects.return_value = [mock_project_info]

        handler = RetrieveProjectContextQueryHandler(
            repository=mock_repository,
            environment=mock_environment,
        )

        query = RetrieveProjectContextQuery(base_path="/projects")

        # Act
        result = handler.handle(query)

        # Assert
        assert result["jerry_project"] is None
        assert result["available_projects"] == [mock_project_info]

    def test_handler_can_be_registered_with_dispatcher(self) -> None:
        """Handler.handle can be registered with QueryDispatcher."""
        from src.application.dispatchers.query_dispatcher import QueryDispatcher

        mock_repository = Mock()
        mock_environment = Mock()
        mock_environment.get_env.return_value = None
        mock_repository.scan_projects.return_value = []

        handler = RetrieveProjectContextQueryHandler(
            repository=mock_repository,
            environment=mock_environment,
        )

        dispatcher = QueryDispatcher()
        dispatcher.register(RetrieveProjectContextQuery, handler.handle)

        result = dispatcher.dispatch(RetrieveProjectContextQuery(base_path="/test"))

        assert isinstance(result, dict)


# === Negative Tests (30%) ===


class TestGetProjectContextHandlerNegative:
    """Negative tests for RetrieveProjectContextQueryHandler."""

    def test_invalid_project_format_returns_error(self) -> None:
        """Invalid project ID format returns validation failure."""
        # Arrange
        mock_repository = Mock()
        mock_environment = Mock()

        mock_environment.get_env.return_value = "invalid-format"
        mock_repository.scan_projects.return_value = []

        handler = RetrieveProjectContextQueryHandler(
            repository=mock_repository,
            environment=mock_environment,
        )

        query = RetrieveProjectContextQuery(base_path="/projects")

        # Act
        result = handler.handle(query)

        # Assert
        assert result["jerry_project"] == "invalid-format"
        assert result["project_id"] is None
        assert result["validation"] is not None
        assert result["validation"].is_valid is False

    def test_repository_error_returns_empty_projects(self) -> None:
        """Repository error during scan returns empty available projects."""
        from src.session_management.application.ports import RepositoryError

        # Arrange
        mock_repository = Mock()
        mock_environment = Mock()

        mock_environment.get_env.return_value = None
        mock_repository.scan_projects.side_effect = RepositoryError("Access denied")

        handler = RetrieveProjectContextQueryHandler(
            repository=mock_repository,
            environment=mock_environment,
        )

        query = RetrieveProjectContextQuery(base_path="/projects")

        # Act
        result = handler.handle(query)

        # Assert - should handle error gracefully
        assert result["jerry_project"] is None
        assert result["available_projects"] == []


# === Edge Case Tests (10%) ===


class TestGetProjectContextHandlerEdgeCases:
    """Edge case tests for RetrieveProjectContextQueryHandler."""

    def test_empty_projects_directory(self) -> None:
        """Empty projects directory returns empty list."""
        # Arrange
        mock_repository = Mock()
        mock_environment = Mock()

        mock_environment.get_env.return_value = None
        mock_repository.scan_projects.return_value = []

        handler = RetrieveProjectContextQueryHandler(
            repository=mock_repository,
            environment=mock_environment,
        )

        query = RetrieveProjectContextQuery(base_path="/empty")

        # Act
        result = handler.handle(query)

        # Assert
        assert result["available_projects"] == []
        assert result["next_number"] == 1
