"""
Unit tests for GetProjectContextHandler.

Tests the handler with mocked dependencies.

Test Distribution per impl-es-e-003:
- Happy Path (60%): 4 tests - Valid project, project not set, handler protocol, dispatcher registration
- Negative (30%): 2 tests - Invalid project format, repository error
- Edge (10%): 1 test - Empty projects directory
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from unittest.mock import MagicMock, Mock

import pytest


# === Query Data Object ===


@dataclass
class GetProjectContextQueryData:
    """Query data for getting project context.

    This is a pure data object - no dependencies, no behavior.
    Used by the dispatcher to route to the handler.
    """

    base_path: str


# === Happy Path Tests (60%) ===


class TestGetProjectContextHandlerHappyPath:
    """Happy path tests for GetProjectContextHandler."""

    def test_handler_is_importable(self) -> None:
        """GetProjectContextHandler can be imported."""
        from src.application.handlers.get_project_context_handler import (
            GetProjectContextHandler,
        )

        assert GetProjectContextHandler is not None

    def test_handler_returns_context_when_project_set(self) -> None:
        """Handler returns full context when JERRY_PROJECT is set."""
        from src.application.handlers.get_project_context_handler import (
            GetProjectContextHandler,
        )

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

        handler = GetProjectContextHandler(
            repository=mock_repository,
            environment=mock_environment,
        )

        query = GetProjectContextQueryData(base_path="/projects")

        # Act
        result = handler.handle(query)

        # Assert
        assert result["jerry_project"] == "PROJ-001-test"
        assert result["project_id"] is not None
        assert result["validation"] is not None

    def test_handler_returns_context_when_project_not_set(self) -> None:
        """Handler returns context with available projects when JERRY_PROJECT not set."""
        from src.application.handlers.get_project_context_handler import (
            GetProjectContextHandler,
        )

        # Arrange
        mock_repository = Mock()
        mock_environment = Mock()

        mock_environment.get_env.return_value = None

        mock_project_info = Mock()
        mock_project_info.id.number = 1
        mock_repository.scan_projects.return_value = [mock_project_info]

        handler = GetProjectContextHandler(
            repository=mock_repository,
            environment=mock_environment,
        )

        query = GetProjectContextQueryData(base_path="/projects")

        # Act
        result = handler.handle(query)

        # Assert
        assert result["jerry_project"] is None
        assert result["available_projects"] == [mock_project_info]

    def test_handler_can_be_registered_with_dispatcher(self) -> None:
        """Handler.handle can be registered with QueryDispatcher."""
        from src.application.dispatchers.query_dispatcher import QueryDispatcher
        from src.application.handlers.get_project_context_handler import (
            GetProjectContextHandler,
        )

        mock_repository = Mock()
        mock_environment = Mock()
        mock_environment.get_env.return_value = None
        mock_repository.scan_projects.return_value = []

        handler = GetProjectContextHandler(
            repository=mock_repository,
            environment=mock_environment,
        )

        dispatcher = QueryDispatcher()
        dispatcher.register(GetProjectContextQueryData, handler.handle)

        result = dispatcher.dispatch(GetProjectContextQueryData(base_path="/test"))

        assert isinstance(result, dict)


# === Negative Tests (30%) ===


class TestGetProjectContextHandlerNegative:
    """Negative tests for GetProjectContextHandler."""

    def test_invalid_project_format_returns_error(self) -> None:
        """Invalid project ID format returns validation failure."""
        from src.application.handlers.get_project_context_handler import (
            GetProjectContextHandler,
        )

        # Arrange
        mock_repository = Mock()
        mock_environment = Mock()

        mock_environment.get_env.return_value = "invalid-format"
        mock_repository.scan_projects.return_value = []

        handler = GetProjectContextHandler(
            repository=mock_repository,
            environment=mock_environment,
        )

        query = GetProjectContextQueryData(base_path="/projects")

        # Act
        result = handler.handle(query)

        # Assert
        assert result["jerry_project"] == "invalid-format"
        assert result["project_id"] is None
        assert result["validation"] is not None
        assert result["validation"].is_valid is False

    def test_repository_error_returns_empty_projects(self) -> None:
        """Repository error during scan returns empty available projects."""
        from src.application.handlers.get_project_context_handler import (
            GetProjectContextHandler,
        )
        from src.session_management.application.ports import RepositoryError

        # Arrange
        mock_repository = Mock()
        mock_environment = Mock()

        mock_environment.get_env.return_value = None
        mock_repository.scan_projects.side_effect = RepositoryError("Access denied")

        handler = GetProjectContextHandler(
            repository=mock_repository,
            environment=mock_environment,
        )

        query = GetProjectContextQueryData(base_path="/projects")

        # Act
        result = handler.handle(query)

        # Assert - should handle error gracefully
        assert result["jerry_project"] is None
        assert result["available_projects"] == []


# === Edge Case Tests (10%) ===


class TestGetProjectContextHandlerEdgeCases:
    """Edge case tests for GetProjectContextHandler."""

    def test_empty_projects_directory(self) -> None:
        """Empty projects directory returns empty list."""
        from src.application.handlers.get_project_context_handler import (
            GetProjectContextHandler,
        )

        # Arrange
        mock_repository = Mock()
        mock_environment = Mock()

        mock_environment.get_env.return_value = None
        mock_repository.scan_projects.return_value = []

        handler = GetProjectContextHandler(
            repository=mock_repository,
            environment=mock_environment,
        )

        query = GetProjectContextQueryData(base_path="/empty")

        # Act
        result = handler.handle(query)

        # Assert
        assert result["available_projects"] == []
        assert result["next_number"] == 1
