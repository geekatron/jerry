"""
GetProjectContextQuery - Query to get the full context for a project.

Used by the session start hook to gather all information needed
for the structured output.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ...domain import InvalidProjectIdError, ProjectId, ValidationResult
from ..ports import IEnvironmentProvider, IProjectRepository, RepositoryError


@dataclass
class GetProjectContextQuery:
    """Query to get the full context for a project."""

    repository: IProjectRepository
    environment: IEnvironmentProvider
    base_path: str

    def execute(self) -> dict[str, Any]:
        """Execute the get project context query.

        Returns:
            Dictionary with context information:
            - jerry_project: The JERRY_PROJECT env var value (or None)
            - project_id: Parsed ProjectId (or None if invalid/not set)
            - validation: ValidationResult for the project (or None)
            - available_projects: List of ProjectInfo for selection
            - next_number: Next available project number
        """
        jerry_project = self.environment.get_env("JERRY_PROJECT")

        result: dict[str, Any] = {
            "jerry_project": jerry_project,
            "project_id": None,
            "validation": None,
            "available_projects": [],
            "next_number": 1,
        }

        # Scan for available projects
        try:
            result["available_projects"] = self.repository.scan_projects(self.base_path)
            if result["available_projects"]:
                max_num = max(p.id.number for p in result["available_projects"])
                result["next_number"] = min(max_num + 1, 999)
        except RepositoryError:
            # If we can't scan, leave defaults
            pass

        # If JERRY_PROJECT is set, validate it
        if jerry_project:
            try:
                project_id = ProjectId.parse(jerry_project)
                result["project_id"] = project_id
                result["validation"] = self.repository.validate_project(self.base_path, project_id)
            except InvalidProjectIdError as e:
                result["validation"] = ValidationResult.failure([e.message])

        return result
