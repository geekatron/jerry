"""
Unit tests for ValidateProjectQueryHandler.

Tests the handler with mocked dependencies.

Test Distribution per impl-es-e-003:
- Happy Path (60%): 4 tests - Valid project returns success, handler protocol, dispatcher, returns tuple
- Negative (30%): 2 tests - Invalid project ID format, project not found
- Edge (10%): 1 test - Project with warnings
"""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from src.application.handlers.queries import ValidateProjectQueryHandler
from src.application.queries import ValidateProjectQuery


# === Happy Path Tests (60%) ===


class TestValidateProjectHandlerHappyPath:
    """Happy path tests for ValidateProjectQueryHandler."""

    def test_handler_is_importable(self) -> None:
        """ValidateProjectQueryHandler can be imported."""
        from src.application.handlers.queries import ValidateProjectQueryHandler

        assert ValidateProjectQueryHandler is not None

    def test_handler_returns_valid_for_existing_project(self) -> None:
        """Handler returns valid result for existing project."""
        # Arrange
        mock_repository = Mock()
        mock_validation = Mock()
        mock_validation.is_valid = True
        mock_validation.messages = []
        mock_repository.validate_project.return_value = mock_validation

        handler = ValidateProjectQueryHandler(repository=mock_repository)
        query = ValidateProjectQuery(
            base_path="/projects",
            project_id_str="PROJ-001-test",
        )

        # Act
        project_id, validation = handler.handle(query)

        # Assert
        assert project_id is not None
        assert str(project_id) == "PROJ-001-test"
        assert validation.is_valid is True

    def test_handler_returns_tuple(self) -> None:
        """Handler returns tuple of (ProjectId, ValidationResult)."""
        # Arrange
        mock_repository = Mock()
        mock_validation = Mock()
        mock_validation.is_valid = True
        mock_repository.validate_project.return_value = mock_validation

        handler = ValidateProjectQueryHandler(repository=mock_repository)
        query = ValidateProjectQuery(
            base_path="/projects",
            project_id_str="PROJ-002-another",
        )

        # Act
        result = handler.handle(query)

        # Assert
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_handler_can_be_registered_with_dispatcher(self) -> None:
        """Handler.handle can be registered with QueryDispatcher."""
        from src.application.dispatchers.query_dispatcher import QueryDispatcher

        mock_repository = Mock()
        mock_validation = Mock()
        mock_validation.is_valid = True
        mock_repository.validate_project.return_value = mock_validation

        handler = ValidateProjectQueryHandler(repository=mock_repository)

        dispatcher = QueryDispatcher()
        dispatcher.register(ValidateProjectQuery, handler.handle)

        result = dispatcher.dispatch(
            ValidateProjectQuery(base_path="/test", project_id_str="PROJ-001-x")
        )

        assert isinstance(result, tuple)


# === Negative Tests (30%) ===


class TestValidateProjectHandlerNegative:
    """Negative tests for ValidateProjectQueryHandler."""

    def test_invalid_project_id_format_returns_none(self) -> None:
        """Invalid project ID format returns None for project_id."""
        # Arrange
        mock_repository = Mock()

        handler = ValidateProjectQueryHandler(repository=mock_repository)
        query = ValidateProjectQuery(
            base_path="/projects",
            project_id_str="invalid-format",
        )

        # Act
        project_id, validation = handler.handle(query)

        # Assert
        assert project_id is None
        assert validation.is_valid is False

    def test_project_not_found_returns_invalid(self) -> None:
        """Non-existent project returns invalid validation."""
        # Arrange
        mock_repository = Mock()
        mock_validation = Mock()
        mock_validation.is_valid = False
        mock_validation.messages = ["Project directory not found"]
        mock_repository.validate_project.return_value = mock_validation

        handler = ValidateProjectQueryHandler(repository=mock_repository)
        query = ValidateProjectQuery(
            base_path="/projects",
            project_id_str="PROJ-999-nonexistent",
        )

        # Act
        project_id, validation = handler.handle(query)

        # Assert
        assert project_id is not None
        assert validation.is_valid is False


# === Edge Case Tests (10%) ===


class TestValidateProjectHandlerEdgeCases:
    """Edge case tests for ValidateProjectQueryHandler."""

    def test_project_with_warnings_returns_valid(self) -> None:
        """Project with warnings still returns valid but includes messages."""
        # Arrange
        mock_repository = Mock()
        mock_validation = Mock()
        mock_validation.is_valid = True
        mock_validation.has_warnings = True
        mock_validation.messages = ["Optional file WORKTRACKER.md not found"]
        mock_repository.validate_project.return_value = mock_validation

        handler = ValidateProjectQueryHandler(repository=mock_repository)
        query = ValidateProjectQuery(
            base_path="/projects",
            project_id_str="PROJ-003-warnings",
        )

        # Act
        project_id, validation = handler.handle(query)

        # Assert
        assert validation.is_valid is True
        assert validation.has_warnings is True
        assert len(validation.messages) > 0
