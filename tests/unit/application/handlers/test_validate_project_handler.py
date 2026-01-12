"""
Unit tests for ValidateProjectHandler.

Tests the handler with mocked dependencies.

Test Distribution per impl-es-e-003:
- Happy Path (60%): 4 tests - Valid project returns success, handler protocol, dispatcher, returns tuple
- Negative (30%): 2 tests - Invalid project ID format, project not found
- Edge (10%): 1 test - Project with warnings
"""

from __future__ import annotations

from dataclasses import dataclass
from unittest.mock import Mock

import pytest


# === Query Data Object ===


@dataclass
class ValidateProjectQueryData:
    """Query data for validating a project.

    This is a pure data object - no dependencies, no behavior.
    """

    base_path: str
    project_id_str: str


# === Happy Path Tests (60%) ===


class TestValidateProjectHandlerHappyPath:
    """Happy path tests for ValidateProjectHandler."""

    def test_handler_is_importable(self) -> None:
        """ValidateProjectHandler can be imported."""
        from src.application.handlers.validate_project_handler import (
            ValidateProjectHandler,
        )

        assert ValidateProjectHandler is not None

    def test_handler_returns_valid_for_existing_project(self) -> None:
        """Handler returns valid result for existing project."""
        from src.application.handlers.validate_project_handler import (
            ValidateProjectHandler,
        )

        # Arrange
        mock_repository = Mock()
        mock_validation = Mock()
        mock_validation.is_valid = True
        mock_validation.messages = []
        mock_repository.validate_project.return_value = mock_validation

        handler = ValidateProjectHandler(repository=mock_repository)
        query = ValidateProjectQueryData(
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
        from src.application.handlers.validate_project_handler import (
            ValidateProjectHandler,
        )

        # Arrange
        mock_repository = Mock()
        mock_validation = Mock()
        mock_validation.is_valid = True
        mock_repository.validate_project.return_value = mock_validation

        handler = ValidateProjectHandler(repository=mock_repository)
        query = ValidateProjectQueryData(
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
        from src.application.handlers.validate_project_handler import (
            ValidateProjectHandler,
        )

        mock_repository = Mock()
        mock_validation = Mock()
        mock_validation.is_valid = True
        mock_repository.validate_project.return_value = mock_validation

        handler = ValidateProjectHandler(repository=mock_repository)

        dispatcher = QueryDispatcher()
        dispatcher.register(ValidateProjectQueryData, handler.handle)

        result = dispatcher.dispatch(
            ValidateProjectQueryData(base_path="/test", project_id_str="PROJ-001-x")
        )

        assert isinstance(result, tuple)


# === Negative Tests (30%) ===


class TestValidateProjectHandlerNegative:
    """Negative tests for ValidateProjectHandler."""

    def test_invalid_project_id_format_returns_none(self) -> None:
        """Invalid project ID format returns None for project_id."""
        from src.application.handlers.validate_project_handler import (
            ValidateProjectHandler,
        )

        # Arrange
        mock_repository = Mock()

        handler = ValidateProjectHandler(repository=mock_repository)
        query = ValidateProjectQueryData(
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
        from src.application.handlers.validate_project_handler import (
            ValidateProjectHandler,
        )

        # Arrange
        mock_repository = Mock()
        mock_validation = Mock()
        mock_validation.is_valid = False
        mock_validation.messages = ["Project directory not found"]
        mock_repository.validate_project.return_value = mock_validation

        handler = ValidateProjectHandler(repository=mock_repository)
        query = ValidateProjectQueryData(
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
    """Edge case tests for ValidateProjectHandler."""

    def test_project_with_warnings_returns_valid(self) -> None:
        """Project with warnings still returns valid but includes messages."""
        from src.application.handlers.validate_project_handler import (
            ValidateProjectHandler,
        )

        # Arrange
        mock_repository = Mock()
        mock_validation = Mock()
        mock_validation.is_valid = True
        mock_validation.has_warnings = True
        mock_validation.messages = ["Optional file WORKTRACKER.md not found"]
        mock_repository.validate_project.return_value = mock_validation

        handler = ValidateProjectHandler(repository=mock_repository)
        query = ValidateProjectQueryData(
            base_path="/projects",
            project_id_str="PROJ-003-warnings",
        )

        # Act
        project_id, validation = handler.handle(query)

        # Assert
        assert validation.is_valid is True
        assert validation.has_warnings is True
        assert len(validation.messages) > 0
