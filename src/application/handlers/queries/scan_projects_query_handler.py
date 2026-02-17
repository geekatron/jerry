# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ScanProjectsQueryHandler - Handler for ScanProjectsQuery.

This handler retrieves all available projects from the repository.
Returns a sorted list of ProjectInfo objects.

Dependencies are injected via constructor, query data via handle().
"""

from __future__ import annotations

from src.application.queries.scan_projects_query import ScanProjectsQuery
from src.session_management.application.ports import IProjectRepository
from src.session_management.domain import ProjectInfo


class ScanProjectsQueryHandler:
    """Handler for ScanProjectsQuery.

    Scans the projects directory and returns all valid projects.

    Attributes:
        _repository: Repository for project operations
    """

    def __init__(self, repository: IProjectRepository) -> None:
        """Initialize the handler with dependencies.

        Args:
            repository: Repository for project operations
        """
        self._repository = repository

    def handle(self, query: ScanProjectsQuery) -> list[ProjectInfo]:
        """Handle the ScanProjectsQuery.

        Args:
            query: Query data containing base_path

        Returns:
            List of ProjectInfo objects sorted by project number

        Raises:
            RepositoryError: If the projects directory cannot be accessed
        """
        return self._repository.scan_projects(query.base_path)
