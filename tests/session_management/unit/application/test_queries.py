# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for Application Layer Queries.

Test Categories:
    - ScanProjectsQuery: Project scanning with mock repository
    - ValidateProjectQuery: Project validation with ID parsing
    - GetNextProjectNumberQuery: Next number calculation
    - GetProjectContextQuery: Full context gathering

References:
    - ENFORCE-009: Application Layer Tests
    - CQRS Pattern: Queries return data, don't modify state
"""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from src.session_management.application.ports import RepositoryError
from src.session_management.application.queries.get_next_number import (
    GetNextProjectNumberQuery,
)
from src.session_management.application.queries.get_project_context import (
    GetProjectContextQuery,
)
from src.session_management.application.queries.scan_projects import ScanProjectsQuery
from src.session_management.application.queries.validate_project import (
    ValidateProjectQuery,
)
from src.session_management.domain.entities.project_info import ProjectInfo
from src.session_management.domain.value_objects.project_id import ProjectId
from src.session_management.domain.value_objects.project_status import ProjectStatus
from src.session_management.domain.value_objects.validation_result import (
    ValidationResult,
)

# =============================================================================
# Test Fixtures - Mock Repositories
# =============================================================================


def create_mock_project(
    number: int, slug: str = "test", status: ProjectStatus = ProjectStatus.IN_PROGRESS
) -> ProjectInfo:
    """Create a mock ProjectInfo for testing."""
    project_id = ProjectId.parse(f"PROJ-{number:03d}-{slug}")
    return ProjectInfo.create(
        project_id=project_id,
        status=status,
        has_plan=True,
        has_tracker=True,
        path=f"/projects/PROJ-{number:03d}-{slug}",
    )


@pytest.fixture
def mock_repository() -> Mock:
    """Create a mock IProjectRepository."""
    return Mock()


@pytest.fixture
def mock_environment() -> Mock:
    """Create a mock IEnvironmentProvider."""
    return Mock()


# =============================================================================
# ScanProjectsQuery Tests (ENFORCE-009.1)
# =============================================================================


class TestScanProjectsQueryHappyPath:
    """Happy path tests for ScanProjectsQuery."""

    def test_scan_projects_returns_sorted_list(self, mock_repository: Mock) -> None:
        """scan_projects should return projects sorted by number."""
        projects = [
            create_mock_project(3, "gamma"),
            create_mock_project(1, "alpha"),
            create_mock_project(2, "beta"),
        ]
        mock_repository.scan_projects.return_value = sorted(projects, key=lambda p: p.id.number)

        query = ScanProjectsQuery(repository=mock_repository, base_path="/projects")
        result = query.execute()

        assert len(result) == 3
        assert result[0].id.number == 1
        assert result[1].id.number == 2
        assert result[2].id.number == 3

    def test_scan_projects_returns_project_info_with_status(self, mock_repository: Mock) -> None:
        """scan_projects should return ProjectInfo with status."""
        projects = [
            create_mock_project(1, "alpha", ProjectStatus.IN_PROGRESS),
            create_mock_project(2, "beta", ProjectStatus.COMPLETED),
        ]
        mock_repository.scan_projects.return_value = projects

        query = ScanProjectsQuery(repository=mock_repository, base_path="/projects")
        result = query.execute()

        assert result[0].status == ProjectStatus.IN_PROGRESS
        assert result[1].status == ProjectStatus.COMPLETED

    def test_scan_projects_calls_repository_with_base_path(self, mock_repository: Mock) -> None:
        """scan_projects should pass base_path to repository."""
        mock_repository.scan_projects.return_value = []

        query = ScanProjectsQuery(repository=mock_repository, base_path="/custom/path")
        query.execute()

        mock_repository.scan_projects.assert_called_once_with("/custom/path")


class TestScanProjectsQueryEdgeCases:
    """Edge case tests for ScanProjectsQuery."""

    def test_scan_projects_with_empty_directory_returns_empty_list(
        self, mock_repository: Mock
    ) -> None:
        """scan_projects with no projects returns empty list."""
        mock_repository.scan_projects.return_value = []

        query = ScanProjectsQuery(repository=mock_repository, base_path="/projects")
        result = query.execute()

        assert result == []

    def test_scan_projects_with_single_project(self, mock_repository: Mock) -> None:
        """scan_projects with single project returns single-item list."""
        projects = [create_mock_project(1, "solo")]
        mock_repository.scan_projects.return_value = projects

        query = ScanProjectsQuery(repository=mock_repository, base_path="/projects")
        result = query.execute()

        assert len(result) == 1
        assert result[0].id.slug == "solo"

    def test_scan_projects_with_gaps_in_numbering(self, mock_repository: Mock) -> None:
        """scan_projects handles gaps in project numbering."""
        projects = [
            create_mock_project(1, "first"),
            create_mock_project(5, "fifth"),
            create_mock_project(10, "tenth"),
        ]
        mock_repository.scan_projects.return_value = sorted(projects, key=lambda p: p.id.number)

        query = ScanProjectsQuery(repository=mock_repository, base_path="/projects")
        result = query.execute()

        numbers = [p.id.number for p in result]
        assert numbers == [1, 5, 10]


class TestScanProjectsQueryFailureScenarios:
    """Failure scenario tests for ScanProjectsQuery."""

    def test_scan_projects_when_repository_raises_error(self, mock_repository: Mock) -> None:
        """scan_projects propagates RepositoryError."""
        mock_repository.scan_projects.side_effect = RepositoryError("Directory not found")

        query = ScanProjectsQuery(repository=mock_repository, base_path="/nonexistent")

        with pytest.raises(RepositoryError, match="Directory not found"):
            query.execute()


# =============================================================================
# ValidateProjectQuery Tests (ENFORCE-009.2)
# =============================================================================


class TestValidateProjectQueryHappyPath:
    """Happy path tests for ValidateProjectQuery."""

    def test_validate_project_when_exists_returns_valid(self, mock_repository: Mock) -> None:
        """validate_project returns valid result for existing project."""
        mock_repository.validate_project.return_value = ValidationResult.success()

        query = ValidateProjectQuery(
            repository=mock_repository,
            base_path="/projects",
            project_id_str="PROJ-001-test",
        )
        project_id, result = query.execute()

        assert project_id is not None
        assert project_id.number == 1
        assert result.is_valid is True

    def test_validate_project_includes_warnings_for_missing_files(
        self, mock_repository: Mock
    ) -> None:
        """validate_project returns warnings for missing files."""
        mock_repository.validate_project.return_value = ValidationResult.success(
            warnings=["Missing PLAN.md", "Missing WORKTRACKER.md"]
        )

        query = ValidateProjectQuery(
            repository=mock_repository,
            base_path="/projects",
            project_id_str="PROJ-001-test",
        )
        _, result = query.execute()

        assert result.is_valid is True
        assert result.has_warnings is True
        assert len(result.messages) == 2
        assert "Missing PLAN.md" in result.messages

    def test_validate_project_parses_project_id(self, mock_repository: Mock) -> None:
        """validate_project correctly parses project ID."""
        mock_repository.validate_project.return_value = ValidationResult.success()

        query = ValidateProjectQuery(
            repository=mock_repository,
            base_path="/projects",
            project_id_str="PROJ-042-my-project",
        )
        project_id, _ = query.execute()

        assert project_id is not None
        assert project_id.number == 42
        assert project_id.slug == "my-project"


class TestValidateProjectQueryNegativeCases:
    """Negative test cases for ValidateProjectQuery."""

    def test_validate_project_with_invalid_id_format_returns_failure(
        self, mock_repository: Mock
    ) -> None:
        """validate_project with invalid format returns failure."""
        query = ValidateProjectQuery(
            repository=mock_repository,
            base_path="/projects",
            project_id_str="invalid-format",
        )
        project_id, result = query.execute()

        assert project_id is None
        assert result.is_valid is False
        assert len(result.messages) > 0

    def test_validate_project_with_nonexistent_id_returns_invalid(
        self, mock_repository: Mock
    ) -> None:
        """validate_project with nonexistent project returns invalid."""
        mock_repository.validate_project.return_value = ValidationResult.failure(
            ["Project directory does not exist"]
        )

        query = ValidateProjectQuery(
            repository=mock_repository,
            base_path="/projects",
            project_id_str="PROJ-999-missing",
        )
        project_id, result = query.execute()

        assert project_id is not None  # Format was valid
        assert result.is_valid is False
        assert "does not exist" in result.messages[0]

    def test_validate_project_with_wrong_prefix_returns_failure(
        self, mock_repository: Mock
    ) -> None:
        """validate_project with wrong prefix returns failure."""
        query = ValidateProjectQuery(
            repository=mock_repository,
            base_path="/projects",
            project_id_str="TASK-001-test",  # Wrong prefix
        )
        project_id, result = query.execute()

        assert project_id is None
        assert result.is_valid is False


# =============================================================================
# GetNextProjectNumberQuery Tests (ENFORCE-009.3)
# =============================================================================


class TestGetNextProjectNumberQueryHappyPath:
    """Happy path tests for GetNextProjectNumberQuery."""

    def test_get_next_number_returns_incremented_value(self, mock_repository: Mock) -> None:
        """get_next_number returns max + 1."""
        projects = [
            create_mock_project(1, "alpha"),
            create_mock_project(2, "beta"),
            create_mock_project(3, "gamma"),
        ]
        mock_repository.scan_projects.return_value = projects

        query = GetNextProjectNumberQuery(repository=mock_repository, base_path="/projects")
        result = query.execute()

        assert result == 4


class TestGetNextProjectNumberQueryEdgeCases:
    """Edge case tests for GetNextProjectNumberQuery."""

    def test_get_next_number_with_no_projects_returns_001(self, mock_repository: Mock) -> None:
        """get_next_number with no projects returns 1."""
        mock_repository.scan_projects.return_value = []

        query = GetNextProjectNumberQuery(repository=mock_repository, base_path="/projects")
        result = query.execute()

        assert result == 1

    def test_get_next_number_with_gaps_uses_max_plus_one(self, mock_repository: Mock) -> None:
        """get_next_number ignores gaps, uses max + 1."""
        projects = [
            create_mock_project(1, "first"),
            create_mock_project(5, "fifth"),  # Gap: 2, 3, 4 missing
        ]
        mock_repository.scan_projects.return_value = projects

        query = GetNextProjectNumberQuery(repository=mock_repository, base_path="/projects")
        result = query.execute()

        assert result == 6  # max(5) + 1, not filling gap

    def test_get_next_number_with_single_project(self, mock_repository: Mock) -> None:
        """get_next_number with single project returns 2."""
        projects = [create_mock_project(1, "solo")]
        mock_repository.scan_projects.return_value = projects

        query = GetNextProjectNumberQuery(repository=mock_repository, base_path="/projects")
        result = query.execute()

        assert result == 2


class TestGetNextProjectNumberQueryNegativeCases:
    """Negative test cases for GetNextProjectNumberQuery."""

    def test_get_next_number_at_max_raises_error(self, mock_repository: Mock) -> None:
        """get_next_number at 999 raises ValueError."""
        projects = [create_mock_project(999, "final")]
        mock_repository.scan_projects.return_value = projects

        query = GetNextProjectNumberQuery(repository=mock_repository, base_path="/projects")

        with pytest.raises(ValueError, match="Maximum project number"):
            query.execute()


class TestGetNextProjectNumberQueryFailureScenarios:
    """Failure scenario tests for GetNextProjectNumberQuery."""

    def test_get_next_number_when_scan_fails_propagates_error(self, mock_repository: Mock) -> None:
        """get_next_number propagates RepositoryError from scan."""
        mock_repository.scan_projects.side_effect = RepositoryError("Permission denied")

        query = GetNextProjectNumberQuery(repository=mock_repository, base_path="/projects")

        with pytest.raises(RepositoryError, match="Permission denied"):
            query.execute()


# =============================================================================
# GetProjectContextQuery Tests (ENFORCE-009.4)
# =============================================================================


class TestGetProjectContextQueryHappyPath:
    """Happy path tests for GetProjectContextQuery."""

    def test_get_project_context_with_valid_project(
        self, mock_repository: Mock, mock_environment: Mock
    ) -> None:
        """get_project_context returns full context for valid project."""
        mock_environment.get_env.return_value = "PROJ-001-test"
        projects = [create_mock_project(1, "test")]
        mock_repository.scan_projects.return_value = projects
        mock_repository.validate_project.return_value = ValidationResult.success()

        query = GetProjectContextQuery(
            repository=mock_repository,
            environment=mock_environment,
            base_path="/projects",
        )
        result = query.execute()

        assert result["jerry_project"] == "PROJ-001-test"
        assert result["project_id"] is not None
        assert result["project_id"].number == 1
        assert result["validation"].is_valid is True
        assert len(result["available_projects"]) == 1
        assert result["next_number"] == 2

    def test_get_project_context_includes_available_projects(
        self, mock_repository: Mock, mock_environment: Mock
    ) -> None:
        """get_project_context includes list of available projects."""
        mock_environment.get_env.return_value = None
        projects = [
            create_mock_project(1, "alpha"),
            create_mock_project(2, "beta"),
        ]
        mock_repository.scan_projects.return_value = projects

        query = GetProjectContextQuery(
            repository=mock_repository,
            environment=mock_environment,
            base_path="/projects",
        )
        result = query.execute()

        assert len(result["available_projects"]) == 2
        assert result["next_number"] == 3


class TestGetProjectContextQueryEdgeCases:
    """Edge case tests for GetProjectContextQuery."""

    def test_get_project_context_without_jerry_project_set(
        self, mock_repository: Mock, mock_environment: Mock
    ) -> None:
        """get_project_context handles unset JERRY_PROJECT."""
        mock_environment.get_env.return_value = None
        mock_repository.scan_projects.return_value = []

        query = GetProjectContextQuery(
            repository=mock_repository,
            environment=mock_environment,
            base_path="/projects",
        )
        result = query.execute()

        assert result["jerry_project"] is None
        assert result["project_id"] is None
        assert result["validation"] is None
        assert result["available_projects"] == []
        assert result["next_number"] == 1

    def test_get_project_context_with_empty_jerry_project(
        self, mock_repository: Mock, mock_environment: Mock
    ) -> None:
        """get_project_context handles empty string JERRY_PROJECT."""
        mock_environment.get_env.return_value = ""
        mock_repository.scan_projects.return_value = []

        query = GetProjectContextQuery(
            repository=mock_repository,
            environment=mock_environment,
            base_path="/projects",
        )
        result = query.execute()

        # Empty string is falsy, so no validation attempted
        assert result["jerry_project"] == ""
        assert result["project_id"] is None

    def test_get_project_context_with_no_available_projects(
        self, mock_repository: Mock, mock_environment: Mock
    ) -> None:
        """get_project_context handles no available projects."""
        mock_environment.get_env.return_value = "PROJ-001-test"
        mock_repository.scan_projects.return_value = []
        mock_repository.validate_project.return_value = ValidationResult.failure(
            ["Project not found"]
        )

        query = GetProjectContextQuery(
            repository=mock_repository,
            environment=mock_environment,
            base_path="/projects",
        )
        result = query.execute()

        assert result["available_projects"] == []
        assert result["next_number"] == 1

    def test_get_project_context_next_number_capped_at_999(
        self, mock_repository: Mock, mock_environment: Mock
    ) -> None:
        """get_project_context caps next_number at 999."""
        mock_environment.get_env.return_value = None
        projects = [create_mock_project(998, "almost-max")]
        mock_repository.scan_projects.return_value = projects

        query = GetProjectContextQuery(
            repository=mock_repository,
            environment=mock_environment,
            base_path="/projects",
        )
        result = query.execute()

        assert result["next_number"] == 999


class TestGetProjectContextQueryNegativeCases:
    """Negative test cases for GetProjectContextQuery."""

    def test_get_project_context_with_invalid_jerry_project(
        self, mock_repository: Mock, mock_environment: Mock
    ) -> None:
        """get_project_context handles invalid JERRY_PROJECT format."""
        mock_environment.get_env.return_value = "invalid-format"
        mock_repository.scan_projects.return_value = []

        query = GetProjectContextQuery(
            repository=mock_repository,
            environment=mock_environment,
            base_path="/projects",
        )
        result = query.execute()

        assert result["jerry_project"] == "invalid-format"
        assert result["project_id"] is None
        assert result["validation"] is not None
        assert result["validation"].is_valid is False


class TestGetProjectContextQueryFailureScenarios:
    """Failure scenario tests for GetProjectContextQuery."""

    def test_get_project_context_handles_scan_failure_gracefully(
        self, mock_repository: Mock, mock_environment: Mock
    ) -> None:
        """get_project_context handles RepositoryError on scan."""
        mock_environment.get_env.return_value = None
        mock_repository.scan_projects.side_effect = RepositoryError("Directory inaccessible")

        query = GetProjectContextQuery(
            repository=mock_repository,
            environment=mock_environment,
            base_path="/projects",
        )
        result = query.execute()

        # Should not raise, returns defaults
        assert result["available_projects"] == []
        assert result["next_number"] == 1

    def test_get_project_context_validates_even_if_scan_fails(
        self, mock_repository: Mock, mock_environment: Mock
    ) -> None:
        """get_project_context still validates if scan fails."""
        mock_environment.get_env.return_value = "PROJ-001-test"
        mock_repository.scan_projects.side_effect = RepositoryError("Error")
        mock_repository.validate_project.return_value = ValidationResult.success()

        query = GetProjectContextQuery(
            repository=mock_repository,
            environment=mock_environment,
            base_path="/projects",
        )
        result = query.execute()

        # Validation still happens
        assert result["project_id"] is not None
        assert result["validation"].is_valid is True
