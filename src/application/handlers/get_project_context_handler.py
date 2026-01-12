"""
GetProjectContextHandler - Handler for GetProjectContextQuery.

This handler retrieves the full project context including:
- Current JERRY_PROJECT environment variable
- Parsed and validated project ID
- List of available projects
- Next available project number

Dependencies are injected via constructor, query data via handle().
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from src.session_management.application.ports import (
    IEnvironmentProvider,
    IProjectRepository,
    RepositoryError,
)
from src.session_management.domain import InvalidProjectIdError, ProjectId, ValidationResult


@dataclass
class GetProjectContextQueryData:
    """Query data for getting project context.

    This is a pure data object - no dependencies, no behavior.
    Used by the dispatcher to route to the handler.
    """

    base_path: str


class GetProjectContextHandler:
    """Handler for GetProjectContextQuery.

    Retrieves the full context for the current project configuration.
    Uses injected dependencies to access filesystem and environment.

    Attributes:
        _repository: Repository for project operations
        _environment: Provider for environment variables
    """

    def __init__(
        self,
        repository: IProjectRepository,
        environment: IEnvironmentProvider,
    ) -> None:
        """Initialize the handler with dependencies.

        Args:
            repository: Repository for project operations
            environment: Provider for environment variables
        """
        self._repository = repository
        self._environment = environment

    def handle(self, query: GetProjectContextQueryData) -> dict[str, Any]:
        """Handle the GetProjectContextQuery.

        Args:
            query: Query data containing base_path

        Returns:
            Dictionary with context information:
            - jerry_project: The JERRY_PROJECT env var value (or None)
            - project_id: Parsed ProjectId (or None if invalid/not set)
            - validation: ValidationResult for the project (or None)
            - available_projects: List of ProjectInfo for selection
            - next_number: Next available project number
        """
        jerry_project = self._environment.get_env("JERRY_PROJECT")

        result: dict[str, Any] = {
            "jerry_project": jerry_project,
            "project_id": None,
            "validation": None,
            "available_projects": [],
            "next_number": 1,
        }

        # Scan for available projects
        try:
            result["available_projects"] = self._repository.scan_projects(query.base_path)
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
                result["validation"] = self._repository.validate_project(
                    query.base_path, project_id
                )
            except InvalidProjectIdError as e:
                result["validation"] = ValidationResult.failure([e.message])

        return result
