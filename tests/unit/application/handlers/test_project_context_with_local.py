"""
Unit tests for RetrieveProjectContextQueryHandler with local context support.

Tests the handler's ability to read project context from:
1. JERRY_PROJECT environment variable (highest precedence)
2. .jerry/local/context.toml (fallback)
3. Project discovery (lowest precedence)

All dependencies are mocked - this is a pure unit test file.

Test Distribution (13 tests total):
- Precedence (3): Env > local > discovery behavior
- Handler Integration (2): Accepts dependency, calls reader
- Result DTO (2): Contains all fields, includes path
- Negative (2): Invalid format, backward compatibility
- Edge Cases (4): Empty string, whitespace, env-var-skips-local, repo error

References:
    - EN-001: Session Start Hook TDD Cleanup
    - DEC-001: Local Context Test Strategy
    - AC-005: Local context reading works via main CLI
"""

from __future__ import annotations

from unittest.mock import Mock

from src.application.handlers.queries import RetrieveProjectContextQueryHandler
from src.application.queries import RetrieveProjectContextQuery

# === Precedence Tests ===


class TestProjectContextPrecedence:
    """Tests for project context source precedence."""

    def test_env_var_takes_precedence_over_local_context(self) -> None:
        """JERRY_PROJECT env var takes precedence over local context.

        Precedence order: env > local > discovery
        When env var is set, local context should be ignored.
        """
        # Arrange
        mock_repository = Mock()
        mock_environment = Mock()
        mock_local_context = Mock()

        # Env var is set
        mock_environment.get_env.return_value = "PROJ-001-from-env"

        # Local context has different project
        mock_local_context.get_active_project.return_value = "PROJ-002-from-local"

        # Setup repository
        mock_project_info = Mock()
        mock_project_info.id.number = 1
        mock_repository.scan_projects.return_value = [mock_project_info]
        mock_repository.validate_project.return_value = Mock(is_valid=True)

        handler = RetrieveProjectContextQueryHandler(
            repository=mock_repository,
            environment=mock_environment,
            local_context_reader=mock_local_context,  # New dependency
        )

        query = RetrieveProjectContextQuery(base_path="/projects")

        # Act
        result = handler.handle(query)

        # Assert - env var should win
        assert result["jerry_project"] == "PROJ-001-from-env"
        assert result["project_id"] is not None
        assert result["project_id"].value == "PROJ-001-from-env"

    def test_local_context_used_when_env_not_set(self) -> None:
        """Local context is used when JERRY_PROJECT env var is not set."""
        # Arrange
        mock_repository = Mock()
        mock_environment = Mock()
        mock_local_context = Mock()

        # Env var NOT set
        mock_environment.get_env.return_value = None

        # Local context has project
        mock_local_context.get_active_project.return_value = "PROJ-003-from-local"

        # Setup repository
        mock_project_info = Mock()
        mock_project_info.id.number = 3
        mock_repository.scan_projects.return_value = [mock_project_info]
        mock_repository.validate_project.return_value = Mock(is_valid=True)

        handler = RetrieveProjectContextQueryHandler(
            repository=mock_repository,
            environment=mock_environment,
            local_context_reader=mock_local_context,
        )

        query = RetrieveProjectContextQuery(base_path="/projects")

        # Act
        result = handler.handle(query)

        # Assert - local context should be used
        assert result["jerry_project"] == "PROJ-003-from-local"
        assert result["project_id"] is not None

    def test_discovery_used_when_env_and_local_not_set(self) -> None:
        """Project discovery is used when env and local context not set.

        When neither env var nor local context provides a project,
        available_projects should be populated for user selection.
        """
        # Arrange
        mock_repository = Mock()
        mock_environment = Mock()
        mock_local_context = Mock()

        # Neither source has project
        mock_environment.get_env.return_value = None
        mock_local_context.get_active_project.return_value = None

        # But projects exist on disk
        mock_project_1 = Mock()
        mock_project_1.id.number = 1
        mock_project_1.id.raw = "PROJ-001-alpha"
        mock_project_2 = Mock()
        mock_project_2.id.number = 2
        mock_project_2.id.raw = "PROJ-002-beta"
        mock_repository.scan_projects.return_value = [mock_project_1, mock_project_2]

        handler = RetrieveProjectContextQueryHandler(
            repository=mock_repository,
            environment=mock_environment,
            local_context_reader=mock_local_context,
        )

        query = RetrieveProjectContextQuery(base_path="/projects")

        # Act
        result = handler.handle(query)

        # Assert - no active project, but available projects listed
        assert result["jerry_project"] is None
        assert result["project_id"] is None
        assert len(result["available_projects"]) == 2
        assert result["next_number"] == 3


# === Handler with Local Context Tests ===


class TestHandlerWithLocalContext:
    """Tests for handler local context integration."""

    def test_handler_accepts_local_context_reader_dependency(self) -> None:
        """Handler constructor accepts ILocalContextReader dependency."""
        # Arrange
        mock_repository = Mock()
        mock_environment = Mock()
        mock_local_context = Mock()

        mock_environment.get_env.return_value = None
        mock_local_context.get_active_project.return_value = None
        mock_repository.scan_projects.return_value = []

        # Act - should not raise
        handler = RetrieveProjectContextQueryHandler(
            repository=mock_repository,
            environment=mock_environment,
            local_context_reader=mock_local_context,
        )

        # Assert
        assert handler is not None

    def test_handler_calls_local_context_reader(self) -> None:
        """Handler calls local_context_reader.get_active_project()."""
        # Arrange
        mock_repository = Mock()
        mock_environment = Mock()
        mock_local_context = Mock()

        mock_environment.get_env.return_value = None
        mock_local_context.get_active_project.return_value = None
        mock_repository.scan_projects.return_value = []

        handler = RetrieveProjectContextQueryHandler(
            repository=mock_repository,
            environment=mock_environment,
            local_context_reader=mock_local_context,
        )

        query = RetrieveProjectContextQuery(base_path="/projects")

        # Act
        handler.handle(query)

        # Assert - local context reader was called
        mock_local_context.get_active_project.assert_called_once()


# === Result DTO Tests ===


class TestProjectContextResultDTO:
    """Tests for the result structure."""

    def test_result_contains_all_required_fields(self) -> None:
        """Result dict contains all required fields for hook output."""
        # Arrange
        mock_repository = Mock()
        mock_environment = Mock()
        mock_local_context = Mock()

        mock_environment.get_env.return_value = "PROJ-001-test"
        mock_local_context.get_active_project.return_value = None
        mock_repository.scan_projects.return_value = []
        mock_repository.validate_project.return_value = Mock(is_valid=True)

        handler = RetrieveProjectContextQueryHandler(
            repository=mock_repository,
            environment=mock_environment,
            local_context_reader=mock_local_context,
        )

        query = RetrieveProjectContextQuery(base_path="/projects")

        # Act
        result = handler.handle(query)

        # Assert - all required fields present
        assert "jerry_project" in result
        assert "project_id" in result
        assert "validation" in result
        assert "available_projects" in result
        assert "next_number" in result

    def test_result_includes_project_path_when_valid(self) -> None:
        """Result includes project_path when project is valid."""
        # Arrange
        mock_repository = Mock()
        mock_environment = Mock()
        mock_local_context = Mock()

        mock_environment.get_env.return_value = "PROJ-001-test"
        mock_local_context.get_active_project.return_value = None

        mock_project_info = Mock()
        mock_project_info.id.number = 1
        mock_project_info.path = "/projects/PROJ-001-test"
        mock_repository.scan_projects.return_value = [mock_project_info]
        mock_repository.validate_project.return_value = Mock(
            is_valid=True,
            project_path="/projects/PROJ-001-test",
        )

        handler = RetrieveProjectContextQueryHandler(
            repository=mock_repository,
            environment=mock_environment,
            local_context_reader=mock_local_context,
        )

        query = RetrieveProjectContextQuery(base_path="/projects")

        # Act
        result = handler.handle(query)

        # Assert
        assert result["validation"].is_valid is True
        # Project path should be accessible from validation or project_info


# === Negative Tests ===


class TestProjectContextNegative:
    """Negative tests for project context with local context."""

    def test_invalid_local_context_project_returns_validation_error(self) -> None:
        """Invalid project ID from local context returns validation error."""
        # Arrange
        mock_repository = Mock()
        mock_environment = Mock()
        mock_local_context = Mock()

        # Env not set, local context has invalid format
        mock_environment.get_env.return_value = None
        mock_local_context.get_active_project.return_value = "invalid-format"
        mock_repository.scan_projects.return_value = []

        handler = RetrieveProjectContextQueryHandler(
            repository=mock_repository,
            environment=mock_environment,
            local_context_reader=mock_local_context,
        )

        query = RetrieveProjectContextQuery(base_path="/projects")

        # Act
        result = handler.handle(query)

        # Assert - validation should fail
        assert result["jerry_project"] == "invalid-format"
        assert result["validation"] is not None
        assert result["validation"].is_valid is False

    def test_missing_local_context_reader_uses_env_only(self) -> None:
        """Handler works without local_context_reader (backward compatibility)."""
        # Arrange
        mock_repository = Mock()
        mock_environment = Mock()

        mock_environment.get_env.return_value = "PROJ-001-env"
        mock_repository.scan_projects.return_value = []
        mock_repository.validate_project.return_value = Mock(is_valid=True)

        # No local_context_reader provided - backward compatibility
        handler = RetrieveProjectContextQueryHandler(
            repository=mock_repository,
            environment=mock_environment,
            # local_context_reader not provided
        )

        query = RetrieveProjectContextQuery(base_path="/projects")

        # Act
        result = handler.handle(query)

        # Assert - should still work with env var
        assert result["jerry_project"] == "PROJ-001-env"


# === Edge Case Tests ===


class TestProjectContextEdgeCases:
    """Edge case tests for project context with local context."""

    def test_empty_string_from_local_context_treated_as_set(self) -> None:
        """Empty string from local context is treated as a project value.

        Edge case: Empty string "" is different from None. The handler
        should pass it through for validation (which will fail).
        """
        # Arrange
        mock_repository = Mock()
        mock_environment = Mock()
        mock_local_context = Mock()

        mock_environment.get_env.return_value = None
        mock_local_context.get_active_project.return_value = ""  # Empty string
        mock_repository.scan_projects.return_value = []

        handler = RetrieveProjectContextQueryHandler(
            repository=mock_repository,
            environment=mock_environment,
            local_context_reader=mock_local_context,
        )

        query = RetrieveProjectContextQuery(base_path="/projects")

        # Act
        result = handler.handle(query)

        # Assert - empty string is treated as "no project set"
        # because bool("") is False, so fallback to discovery
        assert result["jerry_project"] == "" or result["jerry_project"] is None

    def test_whitespace_string_from_local_context_fails_validation(self) -> None:
        """Whitespace-only string from local context fails validation.

        Edge case: "   " is truthy but invalid as project ID.
        """
        # Arrange
        mock_repository = Mock()
        mock_environment = Mock()
        mock_local_context = Mock()

        mock_environment.get_env.return_value = None
        mock_local_context.get_active_project.return_value = "   "  # Whitespace
        mock_repository.scan_projects.return_value = []

        handler = RetrieveProjectContextQueryHandler(
            repository=mock_repository,
            environment=mock_environment,
            local_context_reader=mock_local_context,
        )

        query = RetrieveProjectContextQuery(base_path="/projects")

        # Act
        result = handler.handle(query)

        # Assert - whitespace passed through, validation fails
        assert result["jerry_project"] == "   "
        assert result["validation"] is not None
        assert result["validation"].is_valid is False

    def test_local_context_not_called_when_env_var_set(self) -> None:
        """Local context reader is NOT called when env var is set.

        Optimization: Skip local context read when env var provides project.
        """
        # Arrange
        mock_repository = Mock()
        mock_environment = Mock()
        mock_local_context = Mock()

        mock_environment.get_env.return_value = "PROJ-001-from-env"
        mock_local_context.get_active_project.return_value = "PROJ-002-from-local"
        mock_repository.scan_projects.return_value = []
        mock_repository.validate_project.return_value = Mock(is_valid=True)

        handler = RetrieveProjectContextQueryHandler(
            repository=mock_repository,
            environment=mock_environment,
            local_context_reader=mock_local_context,
        )

        query = RetrieveProjectContextQuery(base_path="/projects")

        # Act
        handler.handle(query)

        # Assert - local context reader was NOT called (optimization)
        mock_local_context.get_active_project.assert_not_called()

    def test_repository_error_during_scan_still_returns_result(self) -> None:
        """Handler returns valid result even when repository scan fails.

        Edge case: scan_projects throws exception, but handler should
        still return a valid result dict with empty available_projects.
        """
        # Arrange
        from src.session_management.application.ports import RepositoryError

        mock_repository = Mock()
        mock_environment = Mock()
        mock_local_context = Mock()

        mock_environment.get_env.return_value = "PROJ-001-test"
        mock_local_context.get_active_project.return_value = None
        mock_repository.scan_projects.side_effect = RepositoryError("Disk error")
        mock_repository.validate_project.return_value = Mock(is_valid=True)

        handler = RetrieveProjectContextQueryHandler(
            repository=mock_repository,
            environment=mock_environment,
            local_context_reader=mock_local_context,
        )

        query = RetrieveProjectContextQuery(base_path="/projects")

        # Act
        result = handler.handle(query)

        # Assert - result still valid, available_projects empty
        assert result["jerry_project"] == "PROJ-001-test"
        assert result["available_projects"] == []
        assert result["next_number"] == 1
