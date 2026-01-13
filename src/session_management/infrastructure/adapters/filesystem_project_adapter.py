"""
FilesystemProjectAdapter - Filesystem-Based Project Repository

Implements the IProjectRepository port using standard filesystem operations.
Handles scanning directories, reading files, and validating project structure.
"""

from __future__ import annotations

import re
from pathlib import Path

from ...application.ports import RepositoryError
from ...domain import (
    InvalidProjectIdError,
    ProjectId,
    ProjectInfo,
    ProjectStatus,
    ValidationResult,
)

# Pattern to match valid project directory names
PROJECT_DIR_PATTERN = re.compile(r"^PROJ-\d{3}-[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")


class FilesystemProjectAdapter:
    """Adapter for accessing project information from the filesystem.

    This adapter implements the IProjectRepository protocol,
    scanning the projects directory and reading project metadata.
    """

    def scan_projects(self, base_path: str) -> list[ProjectInfo]:
        """Scan the base path for available projects.

        Args:
            base_path: Path to the projects directory

        Returns:
            List of ProjectInfo objects for discovered projects,
            sorted by project number ascending

        Raises:
            RepositoryError: If the base path is inaccessible
        """
        projects_dir = Path(base_path)

        # Validate base path exists and is a directory
        if not projects_dir.exists():
            raise RepositoryError(f"Projects directory does not exist: {base_path}")

        if not projects_dir.is_dir():
            raise RepositoryError(f"Projects path is not a directory: {base_path}")

        projects: list[ProjectInfo] = []

        try:
            for item in projects_dir.iterdir():
                # Skip hidden directories, files, and archive
                if not item.is_dir():
                    continue
                if item.name.startswith("."):
                    continue
                if item.name.lower() == "archive":
                    continue

                # Check if directory name matches project pattern
                if not PROJECT_DIR_PATTERN.match(item.name):
                    continue

                # Try to parse as a valid ProjectId
                try:
                    project_id = ProjectId.parse(item.name)
                except InvalidProjectIdError:
                    continue

                # Get project info
                project_info = self._read_project_info(item, project_id)
                projects.append(project_info)

        except PermissionError as e:
            raise RepositoryError(
                f"Permission denied accessing projects directory: {base_path}", cause=e
            ) from e
        except OSError as e:
            raise RepositoryError(f"Error accessing projects directory: {e}", cause=e) from e

        # Sort by project number
        projects.sort(key=lambda p: p.id.number)
        return projects

    def get_project(self, base_path: str, project_id: ProjectId) -> ProjectInfo | None:
        """Get information about a specific project.

        Args:
            base_path: Path to the projects directory
            project_id: The project identifier to look up

        Returns:
            ProjectInfo if found, None otherwise
        """
        project_path = Path(base_path) / str(project_id)

        if not project_path.exists() or not project_path.is_dir():
            return None

        return self._read_project_info(project_path, project_id)

    def validate_project(self, base_path: str, project_id: ProjectId) -> ValidationResult:
        """Validate that a project exists and is properly configured.

        Args:
            base_path: Path to the projects directory
            project_id: The project identifier to validate

        Returns:
            ValidationResult indicating success/failure with messages
        """
        project_path = Path(base_path) / str(project_id)

        # Check if directory exists
        if not project_path.exists():
            return ValidationResult.failure([f"Project directory does not exist: {project_path}"])

        if not project_path.is_dir():
            return ValidationResult.failure([f"Project path is not a directory: {project_path}"])

        # Check for required files and collect warnings
        warnings: list[str] = []

        plan_path = project_path / "PLAN.md"
        tracker_path = project_path / "WORKTRACKER.md"

        if not plan_path.exists():
            warnings.append("Missing PLAN.md")
        elif plan_path.stat().st_size == 0:
            warnings.append("PLAN.md is empty")

        if not tracker_path.exists():
            warnings.append("Missing WORKTRACKER.md")
        elif tracker_path.stat().st_size == 0:
            warnings.append("WORKTRACKER.md is empty")

        # Project exists, return success with any warnings
        return ValidationResult.success(warnings if warnings else None)

    def project_exists(self, base_path: str, project_id: ProjectId) -> bool:
        """Check if a project directory exists.

        Args:
            base_path: Path to the projects directory
            project_id: The project identifier to check

        Returns:
            True if the project directory exists, False otherwise
        """
        project_path = Path(base_path) / str(project_id)
        return project_path.exists() and project_path.is_dir()

    def _read_project_info(self, project_path: Path, project_id: ProjectId) -> ProjectInfo:
        """Read project information from the filesystem.

        Args:
            project_path: Path to the project directory
            project_id: The parsed project identifier

        Returns:
            ProjectInfo populated with available data
        """
        # Check for PLAN.md and WORKTRACKER.md
        has_plan = (project_path / "PLAN.md").exists()
        has_tracker = (project_path / "WORKTRACKER.md").exists()

        # Try to determine status from WORKTRACKER.md
        status = self._read_project_status(project_path / "WORKTRACKER.md")

        return ProjectInfo(
            id=project_id,
            status=status,
            has_plan=has_plan,
            has_tracker=has_tracker,
            path=str(project_path),
        )

    def _read_project_status(self, tracker_path: Path) -> ProjectStatus:
        """Read project status from WORKTRACKER.md.

        Args:
            tracker_path: Path to the WORKTRACKER.md file

        Returns:
            ProjectStatus parsed from file content, or UNKNOWN if unreadable
        """
        if not tracker_path.exists():
            return ProjectStatus.UNKNOWN

        try:
            # Read first 2KB to find status indicators
            content = tracker_path.read_text(encoding="utf-8")[:2048]

            # Look for status indicators in order of precedence
            content_upper = content.upper()

            if "COMPLETED" in content_upper or "DONE" in content_upper:
                return ProjectStatus.COMPLETED
            if "IN_PROGRESS" in content_upper or "IN PROGRESS" in content_upper:
                return ProjectStatus.IN_PROGRESS
            if "DRAFT" in content_upper:
                return ProjectStatus.DRAFT
            if "ARCHIVED" in content_upper:
                return ProjectStatus.ARCHIVED

            return ProjectStatus.UNKNOWN

        except (OSError, UnicodeDecodeError):
            return ProjectStatus.UNKNOWN
