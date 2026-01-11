"""
Unit Tests - Application Layer

Unit tests for use cases with in-memory test doubles.
These tests verify query logic without real I/O.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

import pytest

# Add scripts directory to path for imports
scripts_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(scripts_dir))

from domain import (
    ProjectId,
    ProjectInfo,
    ProjectStatus,
    ValidationResult,
)

from application.ports import RepositoryError
from application.queries import (
    GetNextProjectNumberQuery,
    ScanProjectsQuery,
    ValidateProjectQuery,
)

# =============================================================================
# Test Doubles (In-Memory Implementations)
# =============================================================================


@dataclass
class InMemoryProjectRepository:
    """In-memory implementation of IProjectRepository for testing."""

    projects: dict[str, ProjectInfo] = field(default_factory=dict)
    should_raise: Exception | None = None

    def scan_projects(self, base_path: str) -> list[ProjectInfo]:
        if self.should_raise:
            raise self.should_raise
        return sorted(self.projects.values(), key=lambda p: p.id.number)

    def get_project(self, base_path: str, project_id: ProjectId) -> ProjectInfo | None:
        if self.should_raise:
            raise self.should_raise
        return self.projects.get(str(project_id))

    def validate_project(self, base_path: str, project_id: ProjectId) -> ValidationResult:
        if self.should_raise:
            raise self.should_raise
        project = self.projects.get(str(project_id))
        if project is None:
            return ValidationResult.failure([f"Project not found: {project_id}"])
        warnings = project.warnings
        return ValidationResult.success(warnings if warnings else None)

    def project_exists(self, base_path: str, project_id: ProjectId) -> bool:
        if self.should_raise:
            raise self.should_raise
        return str(project_id) in self.projects

    def add_project(self, project: ProjectInfo) -> None:
        """Helper to add a project to the repository."""
        self.projects[str(project.id)] = project


@dataclass
class InMemoryEnvironmentProvider:
    """In-memory implementation of IEnvironmentProvider for testing."""

    env_vars: dict[str, str] = field(default_factory=dict)

    def get_env(self, name: str) -> str | None:
        value = self.env_vars.get(name)
        if value is None or value.strip() == "":
            return None
        return value.strip()

    def get_env_or_default(self, name: str, default: str) -> str:
        value = self.get_env(name)
        return value if value is not None else default


# =============================================================================
# ScanProjectsQuery Tests
# =============================================================================


class TestScanProjectsQueryHappyPath:
    """Happy path tests for ScanProjectsQuery."""

    def test_scan_projects_returns_sorted_list(self):
        """Projects should be returned sorted by number."""
        repo = InMemoryProjectRepository()
        repo.add_project(ProjectInfo.create("PROJ-003-third", status="DRAFT"))
        repo.add_project(ProjectInfo.create("PROJ-001-first", status="IN_PROGRESS"))
        repo.add_project(ProjectInfo.create("PROJ-002-second", status="COMPLETED"))

        query = ScanProjectsQuery(repository=repo, base_path="/projects")
        result = query.execute()

        assert len(result) == 3
        assert result[0].id.number == 1
        assert result[1].id.number == 2
        assert result[2].id.number == 3

    def test_scan_projects_returns_project_info_with_status(self):
        """Each project should include status information."""
        repo = InMemoryProjectRepository()
        repo.add_project(
            ProjectInfo.create(
                "PROJ-001-test", status="IN_PROGRESS", has_plan=True, has_tracker=True
            )
        )

        query = ScanProjectsQuery(repository=repo, base_path="/projects")
        result = query.execute()

        assert len(result) == 1
        assert result[0].status == ProjectStatus.IN_PROGRESS
        assert result[0].has_plan is True
        assert result[0].has_tracker is True


class TestScanProjectsQueryEdgeCases:
    """Edge case tests for ScanProjectsQuery."""

    def test_scan_projects_with_empty_repo_returns_empty_list(self):
        """Empty repository should return empty list."""
        repo = InMemoryProjectRepository()
        query = ScanProjectsQuery(repository=repo, base_path="/projects")
        result = query.execute()
        assert result == []

    def test_scan_projects_handles_gaps_in_numbering(self):
        """Gaps in project numbers should be handled correctly."""
        repo = InMemoryProjectRepository()
        repo.add_project(ProjectInfo.create("PROJ-001-first"))
        repo.add_project(ProjectInfo.create("PROJ-005-fifth"))
        repo.add_project(ProjectInfo.create("PROJ-010-tenth"))

        query = ScanProjectsQuery(repository=repo, base_path="/projects")
        result = query.execute()

        assert len(result) == 3
        assert [p.id.number for p in result] == [1, 5, 10]

    def test_scan_projects_sorts_by_number_not_alphabetically(self):
        """Sorting should be numeric, not alphabetic."""
        repo = InMemoryProjectRepository()
        # Alphabetically: 002-b, 010-a, 100-c
        # Numerically: 002-b, 010-a, 100-c (same in this case)
        # But let's test with: 009-z, 010-a, 011-m
        repo.add_project(ProjectInfo.create("PROJ-010-aaa"))
        repo.add_project(ProjectInfo.create("PROJ-009-zzz"))
        repo.add_project(ProjectInfo.create("PROJ-011-mmm"))

        query = ScanProjectsQuery(repository=repo, base_path="/projects")
        result = query.execute()

        assert [p.id.number for p in result] == [9, 10, 11]


class TestScanProjectsQueryFailure:
    """Failure scenario tests for ScanProjectsQuery."""

    def test_scan_projects_when_repo_unavailable_raises_error(self):
        """Repository error should propagate."""
        repo = InMemoryProjectRepository()
        repo.should_raise = RepositoryError("Cannot access directory")

        query = ScanProjectsQuery(repository=repo, base_path="/projects")

        with pytest.raises(RepositoryError) as exc_info:
            query.execute()
        assert "Cannot access directory" in str(exc_info.value)


# =============================================================================
# ValidateProjectQuery Tests
# =============================================================================


class TestValidateProjectQueryHappyPath:
    """Happy path tests for ValidateProjectQuery."""

    def test_validate_project_when_exists_returns_valid(self):
        """Valid project should return valid result."""
        repo = InMemoryProjectRepository()
        repo.add_project(ProjectInfo.create("PROJ-001-test", has_plan=True, has_tracker=True))

        query = ValidateProjectQuery(
            repository=repo, base_path="/projects", project_id_str="PROJ-001-test"
        )
        project_id, result = query.execute()

        assert project_id is not None
        assert project_id.value == "PROJ-001-test"
        assert result.is_valid is True

    def test_validate_project_includes_warnings_for_missing_files(self):
        """Missing files should generate warnings."""
        repo = InMemoryProjectRepository()
        repo.add_project(ProjectInfo.create("PROJ-001-test", has_plan=False, has_tracker=True))

        query = ValidateProjectQuery(
            repository=repo, base_path="/projects", project_id_str="PROJ-001-test"
        )
        project_id, result = query.execute()

        assert result.is_valid is True
        assert result.has_warnings is True
        assert any("PLAN" in msg for msg in result.messages)


class TestValidateProjectQueryEdgeCases:
    """Edge case tests for ValidateProjectQuery."""

    def test_validate_project_with_missing_plan_returns_warning(self):
        """Missing PLAN.md should be a warning, not error."""
        repo = InMemoryProjectRepository()
        repo.add_project(ProjectInfo.create("PROJ-001-test", has_plan=False, has_tracker=True))

        query = ValidateProjectQuery(
            repository=repo, base_path="/projects", project_id_str="PROJ-001-test"
        )
        _, result = query.execute()

        assert result.is_valid is True  # Still valid, just has warning

    def test_validate_project_with_missing_tracker_returns_warning(self):
        """Missing WORKTRACKER.md should be a warning."""
        repo = InMemoryProjectRepository()
        repo.add_project(ProjectInfo.create("PROJ-001-test", has_plan=True, has_tracker=False))

        query = ValidateProjectQuery(
            repository=repo, base_path="/projects", project_id_str="PROJ-001-test"
        )
        _, result = query.execute()

        assert result.is_valid is True
        assert any("WORKTRACKER" in msg for msg in result.messages)


class TestValidateProjectQueryNegative:
    """Negative tests for ValidateProjectQuery."""

    def test_validate_project_with_nonexistent_id_returns_invalid(self):
        """Non-existent project should return invalid result."""
        repo = InMemoryProjectRepository()

        query = ValidateProjectQuery(
            repository=repo, base_path="/projects", project_id_str="PROJ-999-nonexistent"
        )
        project_id, result = query.execute()

        assert project_id is not None  # ID format is valid
        assert result.is_valid is False
        assert "not found" in result.first_message.lower()

    def test_validate_project_with_invalid_id_format_returns_invalid(self):
        """Invalid ID format should return invalid result with None ID."""
        repo = InMemoryProjectRepository()

        query = ValidateProjectQuery(
            repository=repo, base_path="/projects", project_id_str="invalid-format"
        )
        project_id, result = query.execute()

        assert project_id is None  # Invalid format
        assert result.is_valid is False


# =============================================================================
# GetNextProjectNumberQuery Tests
# =============================================================================


class TestGetNextProjectNumberQueryHappyPath:
    """Happy path tests for GetNextProjectNumberQuery."""

    def test_get_next_number_returns_incremented_value(self):
        """Next number should be max + 1."""
        repo = InMemoryProjectRepository()
        repo.add_project(ProjectInfo.create("PROJ-001-first"))
        repo.add_project(ProjectInfo.create("PROJ-002-second"))
        repo.add_project(ProjectInfo.create("PROJ-003-third"))

        query = GetNextProjectNumberQuery(repository=repo, base_path="/projects")
        result = query.execute()

        assert result == 4


class TestGetNextProjectNumberQueryEdgeCases:
    """Edge case tests for GetNextProjectNumberQuery."""

    def test_get_next_number_with_no_projects_returns_001(self):
        """Empty repository should return 1."""
        repo = InMemoryProjectRepository()

        query = GetNextProjectNumberQuery(repository=repo, base_path="/projects")
        result = query.execute()

        assert result == 1

    def test_get_next_number_with_gaps_uses_max_plus_one(self):
        """Gaps in numbering should be ignored, use max + 1."""
        repo = InMemoryProjectRepository()
        repo.add_project(ProjectInfo.create("PROJ-001-first"))
        repo.add_project(ProjectInfo.create("PROJ-010-tenth"))
        # Gap at 2-9

        query = GetNextProjectNumberQuery(repository=repo, base_path="/projects")
        result = query.execute()

        assert result == 11  # max(1, 10) + 1 = 11

    def test_get_next_number_at_max_raises_error(self):
        """Reaching 999 should raise error."""
        repo = InMemoryProjectRepository()
        repo.add_project(ProjectInfo.create("PROJ-999-last"))

        query = GetNextProjectNumberQuery(repository=repo, base_path="/projects")

        with pytest.raises(ValueError) as exc_info:
            query.execute()
        assert "999" in str(exc_info.value) or "maximum" in str(exc_info.value).lower()


class TestGetNextProjectNumberQueryFailure:
    """Failure scenario tests for GetNextProjectNumberQuery."""

    def test_get_next_number_when_scan_fails_propagates_error(self):
        """Repository error should propagate."""
        repo = InMemoryProjectRepository()
        repo.should_raise = RepositoryError("Access denied")

        query = GetNextProjectNumberQuery(repository=repo, base_path="/projects")

        with pytest.raises(RepositoryError):
            query.execute()
