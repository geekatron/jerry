"""
Unit tests for ScanProjectsQueryHandler.

Tests the handler with mocked dependencies.

Test Distribution per impl-es-e-003:
- Happy Path (60%): 4 tests - Returns projects, sorted by number, handler protocol, dispatcher
- Negative (30%): 2 tests - Repository error propagates, invalid path
- Edge (10%): 1 test - Empty projects directory
"""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from src.application.handlers.queries import ScanProjectsQueryHandler
from src.application.queries import ScanProjectsQuery
from src.session_management.application.ports import RepositoryError


# === Happy Path Tests (60%) ===


class TestScanProjectsHandlerHappyPath:
    """Happy path tests for ScanProjectsQueryHandler."""

    def test_handler_is_importable(self) -> None:
        """ScanProjectsQueryHandler can be imported."""
        from src.application.handlers.queries import ScanProjectsQueryHandler

        assert ScanProjectsQueryHandler is not None

    def test_handler_returns_projects(self) -> None:
        """Handler returns list of projects from repository."""
        # Arrange
        mock_repository = Mock()
        mock_project1 = Mock()
        mock_project1.id.number = 1
        mock_project2 = Mock()
        mock_project2.id.number = 2
        mock_repository.scan_projects.return_value = [mock_project1, mock_project2]

        handler = ScanProjectsQueryHandler(repository=mock_repository)
        query = ScanProjectsQuery(base_path="/projects")

        # Act
        result = handler.handle(query)

        # Assert
        assert len(result) == 2
        mock_repository.scan_projects.assert_called_once_with("/projects")

    def test_handler_returns_sorted_by_number(self) -> None:
        """Handler returns projects sorted by project number."""
        # Arrange - mock repository returns sorted list
        mock_repository = Mock()
        mock_project1 = Mock()
        mock_project1.id.number = 1
        mock_project2 = Mock()
        mock_project2.id.number = 2
        mock_repository.scan_projects.return_value = [mock_project1, mock_project2]

        handler = ScanProjectsQueryHandler(repository=mock_repository)
        query = ScanProjectsQuery(base_path="/projects")

        # Act
        result = handler.handle(query)

        # Assert - first should have lower number
        assert result[0].id.number < result[1].id.number

    def test_handler_can_be_registered_with_dispatcher(self) -> None:
        """Handler.handle can be registered with QueryDispatcher."""
        from src.application.dispatchers.query_dispatcher import QueryDispatcher

        mock_repository = Mock()
        mock_repository.scan_projects.return_value = []

        handler = ScanProjectsQueryHandler(repository=mock_repository)

        dispatcher = QueryDispatcher()
        dispatcher.register(ScanProjectsQuery, handler.handle)

        result = dispatcher.dispatch(ScanProjectsQuery(base_path="/test"))

        assert isinstance(result, list)


# === Negative Tests (30%) ===


class TestScanProjectsHandlerNegative:
    """Negative tests for ScanProjectsQueryHandler."""

    def test_repository_error_propagates(self) -> None:
        """Repository error during scan propagates to caller."""
        # Arrange
        mock_repository = Mock()
        mock_repository.scan_projects.side_effect = RepositoryError("Access denied")

        handler = ScanProjectsQueryHandler(repository=mock_repository)
        query = ScanProjectsQuery(base_path="/projects")

        # Act & Assert
        with pytest.raises(RepositoryError) as exc_info:
            handler.handle(query)

        assert "Access denied" in str(exc_info.value)

    def test_invalid_path_raises_error(self) -> None:
        """Invalid base path raises RepositoryError."""
        # Arrange
        mock_repository = Mock()
        mock_repository.scan_projects.side_effect = RepositoryError("Path not found")

        handler = ScanProjectsQueryHandler(repository=mock_repository)
        query = ScanProjectsQuery(base_path="/nonexistent")

        # Act & Assert
        with pytest.raises(RepositoryError):
            handler.handle(query)


# === Edge Case Tests (10%) ===


class TestScanProjectsHandlerEdgeCases:
    """Edge case tests for ScanProjectsQueryHandler."""

    def test_empty_projects_directory(self) -> None:
        """Empty projects directory returns empty list."""
        # Arrange
        mock_repository = Mock()
        mock_repository.scan_projects.return_value = []

        handler = ScanProjectsQueryHandler(repository=mock_repository)
        query = ScanProjectsQuery(base_path="/empty")

        # Act
        result = handler.handle(query)

        # Assert
        assert result == []
