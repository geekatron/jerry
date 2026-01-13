"""
ScanProjectsQuery - Query to scan for all available projects.

Returns a sorted list of all valid projects found in the projects directory.
Invalid directory names are silently ignored.
"""

from __future__ import annotations

from dataclasses import dataclass

from ...domain import ProjectInfo
from ..ports import IProjectRepository


@dataclass
class ScanProjectsQuery:
    """Query to scan for all available projects."""

    repository: IProjectRepository
    base_path: str

    def execute(self) -> list[ProjectInfo]:
        """Execute the scan projects query.

        Returns:
            List of ProjectInfo objects sorted by project number

        Raises:
            RepositoryError: If the projects directory cannot be accessed
        """
        return self.repository.scan_projects(self.base_path)
