# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for FilesystemProjectAdapter.

Test Categories:
    - Scan Projects: Directory scanning with audit metadata
    - Get Project: Single project retrieval with audit metadata
    - Validate Project: Project validation behavior
    - Audit Compliance: IAuditable fields on returned ProjectInfo
    - Version Compliance: IVersioned fields on returned ProjectInfo

References:
    - ENFORCE-008d.4: Infrastructure Updates
    - Canon PAT-007: EntityBase Class (IAuditable, IVersioned)
    - ADR-013: Shared Kernel Module
"""

from __future__ import annotations

import tempfile
from datetime import UTC, datetime
from pathlib import Path

import pytest

from src.session_management.application.ports import RepositoryError
from src.session_management.domain.value_objects.project_id import ProjectId
from src.session_management.domain.value_objects.project_status import ProjectStatus
from src.session_management.infrastructure.adapters.filesystem_project_adapter import (
    FilesystemProjectAdapter,
)
from src.shared_kernel.auditable import IAuditable
from src.shared_kernel.versioned import IVersioned

# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def adapter() -> FilesystemProjectAdapter:
    """Create a FilesystemProjectAdapter instance."""
    return FilesystemProjectAdapter()


@pytest.fixture
def temp_projects_dir():
    """Create a temporary projects directory with test projects."""
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)

        # Create valid project directories
        proj_001 = base / "PROJ-001-alpha"
        proj_001.mkdir()
        (proj_001 / "PLAN.md").write_text("# Alpha Plan")
        (proj_001 / "WORKTRACKER.md").write_text("# Alpha Tracker\nIN_PROGRESS")

        proj_002 = base / "PROJ-002-beta"
        proj_002.mkdir()
        (proj_002 / "PLAN.md").write_text("# Beta Plan")
        (proj_002 / "WORKTRACKER.md").write_text("# Beta Tracker\nCOMPLETED")

        proj_003 = base / "PROJ-003-gamma"
        proj_003.mkdir()
        # No PLAN.md or WORKTRACKER.md (incomplete project)

        # Create invalid directories that should be ignored
        (base / ".hidden").mkdir()
        (base / "archive").mkdir()
        (base / "random-folder").mkdir()
        (base / "README.md").write_text("# Projects")

        yield str(base)


@pytest.fixture
def temp_single_project():
    """Create a temporary directory with a single project."""
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)

        proj = base / "PROJ-042-test"
        proj.mkdir()
        (proj / "PLAN.md").write_text("# Test Plan")
        (proj / "WORKTRACKER.md").write_text("# Test Tracker\nDRAFT")

        yield str(base), "PROJ-042-test"


# =============================================================================
# Scan Projects - Audit Metadata Tests (I-008d.4.1)
# =============================================================================


class TestScanProjectsAuditMetadata:
    """Tests for IAuditable compliance on scanned projects."""

    def test_scanned_projects_implement_iauditable(
        self, adapter: FilesystemProjectAdapter, temp_projects_dir: str
    ) -> None:
        """Scanned ProjectInfo should implement IAuditable protocol."""
        projects = adapter.scan_projects(temp_projects_dir)
        assert len(projects) >= 1
        for project in projects:
            assert isinstance(project, IAuditable)

    def test_scanned_projects_have_created_by(
        self, adapter: FilesystemProjectAdapter, temp_projects_dir: str
    ) -> None:
        """Scanned ProjectInfo should have created_by field."""
        projects = adapter.scan_projects(temp_projects_dir)
        for project in projects:
            assert hasattr(project, "created_by")
            assert project.created_by == "System"

    def test_scanned_projects_have_created_at(
        self, adapter: FilesystemProjectAdapter, temp_projects_dir: str
    ) -> None:
        """Scanned ProjectInfo should have created_at timestamp."""
        before = datetime.now(UTC)
        projects = adapter.scan_projects(temp_projects_dir)
        after = datetime.now(UTC)

        for project in projects:
            assert hasattr(project, "created_at")
            assert isinstance(project.created_at, datetime)
            assert before <= project.created_at <= after

    def test_scanned_projects_have_updated_by(
        self, adapter: FilesystemProjectAdapter, temp_projects_dir: str
    ) -> None:
        """Scanned ProjectInfo should have updated_by field."""
        projects = adapter.scan_projects(temp_projects_dir)
        for project in projects:
            assert hasattr(project, "updated_by")
            assert project.updated_by == "System"

    def test_scanned_projects_have_updated_at(
        self, adapter: FilesystemProjectAdapter, temp_projects_dir: str
    ) -> None:
        """Scanned ProjectInfo should have updated_at timestamp."""
        projects = adapter.scan_projects(temp_projects_dir)
        for project in projects:
            assert hasattr(project, "updated_at")
            assert isinstance(project.updated_at, datetime)


# =============================================================================
# Scan Projects - Version Metadata Tests (I-008d.4.2)
# =============================================================================


class TestScanProjectsVersionMetadata:
    """Tests for IVersioned compliance on scanned projects."""

    def test_scanned_projects_implement_iversioned(
        self, adapter: FilesystemProjectAdapter, temp_projects_dir: str
    ) -> None:
        """Scanned ProjectInfo should implement IVersioned protocol."""
        projects = adapter.scan_projects(temp_projects_dir)
        assert len(projects) >= 1
        for project in projects:
            assert isinstance(project, IVersioned)

    def test_scanned_projects_have_version_zero(
        self, adapter: FilesystemProjectAdapter, temp_projects_dir: str
    ) -> None:
        """Scanned ProjectInfo should have version 0 (new discovery)."""
        projects = adapter.scan_projects(temp_projects_dir)
        for project in projects:
            assert hasattr(project, "version")
            assert project.version == 0


# =============================================================================
# Scan Projects - Session ID Tests (I-008d.4.3)
# =============================================================================


class TestScanProjectsSessionId:
    """Tests for session_id field on scanned projects."""

    def test_scanned_projects_have_session_id_none(
        self, adapter: FilesystemProjectAdapter, temp_projects_dir: str
    ) -> None:
        """Scanned ProjectInfo should have session_id as None (no active session)."""
        projects = adapter.scan_projects(temp_projects_dir)
        for project in projects:
            assert hasattr(project, "session_id")
            assert project.session_id is None


# =============================================================================
# Get Project - Audit Metadata Tests (I-008d.4.4)
# =============================================================================


class TestGetProjectAuditMetadata:
    """Tests for IAuditable compliance on get_project."""

    def test_get_project_implements_iauditable(
        self, adapter: FilesystemProjectAdapter, temp_single_project: tuple[str, str]
    ) -> None:
        """get_project should return ProjectInfo implementing IAuditable."""
        base_path, project_name = temp_single_project
        project_id = ProjectId.parse(project_name)
        project = adapter.get_project(base_path, project_id)
        assert project is not None
        assert isinstance(project, IAuditable)

    def test_get_project_has_created_by(
        self, adapter: FilesystemProjectAdapter, temp_single_project: tuple[str, str]
    ) -> None:
        """get_project should return ProjectInfo with created_by."""
        base_path, project_name = temp_single_project
        project_id = ProjectId.parse(project_name)
        project = adapter.get_project(base_path, project_id)
        assert project is not None
        assert project.created_by == "System"

    def test_get_project_has_created_at(
        self, adapter: FilesystemProjectAdapter, temp_single_project: tuple[str, str]
    ) -> None:
        """get_project should return ProjectInfo with created_at."""
        before = datetime.now(UTC)
        base_path, project_name = temp_single_project
        project_id = ProjectId.parse(project_name)
        project = adapter.get_project(base_path, project_id)
        after = datetime.now(UTC)

        assert project is not None
        assert isinstance(project.created_at, datetime)
        assert before <= project.created_at <= after

    def test_get_project_has_updated_by(
        self, adapter: FilesystemProjectAdapter, temp_single_project: tuple[str, str]
    ) -> None:
        """get_project should return ProjectInfo with updated_by."""
        base_path, project_name = temp_single_project
        project_id = ProjectId.parse(project_name)
        project = adapter.get_project(base_path, project_id)
        assert project is not None
        assert project.updated_by == "System"

    def test_get_project_has_updated_at(
        self, adapter: FilesystemProjectAdapter, temp_single_project: tuple[str, str]
    ) -> None:
        """get_project should return ProjectInfo with updated_at."""
        base_path, project_name = temp_single_project
        project_id = ProjectId.parse(project_name)
        project = adapter.get_project(base_path, project_id)
        assert project is not None
        assert isinstance(project.updated_at, datetime)


# =============================================================================
# Get Project - Version Metadata Tests (I-008d.4.5)
# =============================================================================


class TestGetProjectVersionMetadata:
    """Tests for IVersioned compliance on get_project."""

    def test_get_project_implements_iversioned(
        self, adapter: FilesystemProjectAdapter, temp_single_project: tuple[str, str]
    ) -> None:
        """get_project should return ProjectInfo implementing IVersioned."""
        base_path, project_name = temp_single_project
        project_id = ProjectId.parse(project_name)
        project = adapter.get_project(base_path, project_id)
        assert project is not None
        assert isinstance(project, IVersioned)

    def test_get_project_has_version_zero(
        self, adapter: FilesystemProjectAdapter, temp_single_project: tuple[str, str]
    ) -> None:
        """get_project should return ProjectInfo with version 0."""
        base_path, project_name = temp_single_project
        project_id = ProjectId.parse(project_name)
        project = adapter.get_project(base_path, project_id)
        assert project is not None
        assert project.version == 0


# =============================================================================
# Get Project - Session ID Tests (I-008d.4.6)
# =============================================================================


class TestGetProjectSessionId:
    """Tests for session_id field on get_project."""

    def test_get_project_has_session_id_none(
        self, adapter: FilesystemProjectAdapter, temp_single_project: tuple[str, str]
    ) -> None:
        """get_project should return ProjectInfo with session_id as None."""
        base_path, project_name = temp_single_project
        project_id = ProjectId.parse(project_name)
        project = adapter.get_project(base_path, project_id)
        assert project is not None
        assert project.session_id is None


# =============================================================================
# Scan Projects - Functional Tests (Existing Behavior)
# =============================================================================


class TestScanProjectsFunctional:
    """Tests for basic scan_projects functionality."""

    def test_scan_finds_valid_projects(
        self, adapter: FilesystemProjectAdapter, temp_projects_dir: str
    ) -> None:
        """scan_projects should find valid project directories."""
        projects = adapter.scan_projects(temp_projects_dir)
        project_ids = [str(p.id) for p in projects]
        assert "PROJ-001-alpha" in project_ids
        assert "PROJ-002-beta" in project_ids
        assert "PROJ-003-gamma" in project_ids

    def test_scan_ignores_hidden_directories(
        self, adapter: FilesystemProjectAdapter, temp_projects_dir: str
    ) -> None:
        """scan_projects should ignore hidden directories."""
        projects = adapter.scan_projects(temp_projects_dir)
        project_ids = [str(p.id) for p in projects]
        assert not any(".hidden" in pid for pid in project_ids)

    def test_scan_ignores_archive_directory(
        self, adapter: FilesystemProjectAdapter, temp_projects_dir: str
    ) -> None:
        """scan_projects should ignore archive directory."""
        projects = adapter.scan_projects(temp_projects_dir)
        project_ids = [str(p.id) for p in projects]
        assert not any("archive" in pid.lower() for pid in project_ids)

    def test_scan_returns_sorted_by_number(
        self, adapter: FilesystemProjectAdapter, temp_projects_dir: str
    ) -> None:
        """scan_projects should return projects sorted by number."""
        projects = adapter.scan_projects(temp_projects_dir)
        numbers = [p.id.number for p in projects]
        assert numbers == sorted(numbers)

    def test_scan_reads_project_status(
        self, adapter: FilesystemProjectAdapter, temp_projects_dir: str
    ) -> None:
        """scan_projects should read status from WORKTRACKER.md."""
        projects = adapter.scan_projects(temp_projects_dir)
        status_map = {str(p.id): p.status for p in projects}
        assert status_map["PROJ-001-alpha"] == ProjectStatus.IN_PROGRESS
        assert status_map["PROJ-002-beta"] == ProjectStatus.COMPLETED

    def test_scan_detects_incomplete_projects(
        self, adapter: FilesystemProjectAdapter, temp_projects_dir: str
    ) -> None:
        """scan_projects should detect incomplete projects (missing files)."""
        projects = adapter.scan_projects(temp_projects_dir)
        gamma = next(p for p in projects if "gamma" in str(p.id))
        assert gamma.has_plan is False
        assert gamma.has_tracker is False
        assert gamma.is_complete is False


# =============================================================================
# Get Project - Functional Tests (Existing Behavior)
# =============================================================================


class TestGetProjectFunctional:
    """Tests for basic get_project functionality."""

    def test_get_existing_project(
        self, adapter: FilesystemProjectAdapter, temp_single_project: tuple[str, str]
    ) -> None:
        """get_project should return ProjectInfo for existing project."""
        base_path, project_name = temp_single_project
        project_id = ProjectId.parse(project_name)
        project = adapter.get_project(base_path, project_id)
        assert project is not None
        assert str(project.id) == project_name

    def test_get_nonexistent_project(
        self, adapter: FilesystemProjectAdapter, temp_single_project: tuple[str, str]
    ) -> None:
        """get_project should return None for nonexistent project."""
        base_path, _ = temp_single_project
        project_id = ProjectId.parse("PROJ-999-missing")
        project = adapter.get_project(base_path, project_id)
        assert project is None

    def test_get_project_reads_files(
        self, adapter: FilesystemProjectAdapter, temp_single_project: tuple[str, str]
    ) -> None:
        """get_project should detect existing files."""
        base_path, project_name = temp_single_project
        project_id = ProjectId.parse(project_name)
        project = adapter.get_project(base_path, project_id)
        assert project is not None
        assert project.has_plan is True
        assert project.has_tracker is True

    def test_get_project_reads_status(
        self, adapter: FilesystemProjectAdapter, temp_single_project: tuple[str, str]
    ) -> None:
        """get_project should read status from WORKTRACKER.md."""
        base_path, project_name = temp_single_project
        project_id = ProjectId.parse(project_name)
        project = adapter.get_project(base_path, project_id)
        assert project is not None
        assert project.status == ProjectStatus.DRAFT


# =============================================================================
# Error Handling Tests
# =============================================================================


class TestErrorHandling:
    """Tests for error handling."""

    def test_scan_nonexistent_directory_raises(self, adapter: FilesystemProjectAdapter) -> None:
        """scan_projects should raise RepositoryError for nonexistent directory."""
        with pytest.raises(RepositoryError, match="does not exist"):
            adapter.scan_projects("/nonexistent/path")

    def test_scan_file_instead_of_directory_raises(
        self, adapter: FilesystemProjectAdapter, temp_single_project: tuple[str, str]
    ) -> None:
        """scan_projects should raise RepositoryError for file path."""
        base_path, project_name = temp_single_project
        file_path = str(Path(base_path) / project_name / "PLAN.md")
        with pytest.raises(RepositoryError, match="not a directory"):
            adapter.scan_projects(file_path)
