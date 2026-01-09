"""
IProjectRepository - Port for Project Persistence

This port defines the contract for reading project data from
whatever storage mechanism is used (filesystem, database, etc.).
"""

from __future__ import annotations
from typing import Protocol

from ...domain import ProjectId, ProjectInfo, ValidationResult


class IProjectRepository(Protocol):
    """Port for accessing project information.

    This port defines the contract for reading project data from
    whatever storage mechanism is used (filesystem, database, etc.).
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
        ...

    def get_project(self, base_path: str, project_id: ProjectId) -> ProjectInfo | None:
        """Get information about a specific project.

        Args:
            base_path: Path to the projects directory
            project_id: The project identifier to look up

        Returns:
            ProjectInfo if found, None otherwise
        """
        ...

    def validate_project(
        self, base_path: str, project_id: ProjectId
    ) -> ValidationResult:
        """Validate that a project exists and is properly configured.

        Args:
            base_path: Path to the projects directory
            project_id: The project identifier to validate

        Returns:
            ValidationResult indicating success/failure with messages
        """
        ...

    def project_exists(self, base_path: str, project_id: ProjectId) -> bool:
        """Check if a project directory exists.

        Args:
            base_path: Path to the projects directory
            project_id: The project identifier to check

        Returns:
            True if the project directory exists, False otherwise
        """
        ...
