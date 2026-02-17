# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
GetNextProjectNumberQuery - Query to determine the next available project number.

Scans existing projects and returns max(number) + 1.
If no projects exist, returns 1.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..ports import IProjectRepository


@dataclass
class GetNextProjectNumberQuery:
    """Query to determine the next available project number."""

    repository: IProjectRepository
    base_path: str

    def execute(self) -> int:
        """Execute the get next project number query.

        Returns:
            The next available project number (1-999)

        Raises:
            RepositoryError: If the projects directory cannot be accessed
            ValueError: If the maximum project number (999) has been reached
        """
        projects = self.repository.scan_projects(self.base_path)

        if not projects:
            return 1

        max_number = max(p.id.number for p in projects)

        if max_number >= 999:
            raise ValueError(
                "Maximum project number (999) reached. Archive or delete old projects to continue."
            )

        return max_number + 1
