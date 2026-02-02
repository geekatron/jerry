"""
RetrieveProjectContextQueryHandler - Handler for RetrieveProjectContextQuery.

This handler retrieves the full project context including:
- Current JERRY_PROJECT environment variable
- Local context from .jerry/local/context.toml
- Parsed and validated project ID
- List of available projects
- Next available project number

Project resolution follows precedence order:
1. JERRY_PROJECT environment variable (highest precedence)
2. Local context active_project (.jerry/local/context.toml)
3. Project discovery (available_projects for user selection)

Dependencies are injected via constructor, query data via handle().

References:
    - EN-001: Session Start Hook TDD Cleanup
    - TD-006: Missing local context support in main CLI
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from src.application.queries.retrieve_project_context_query import (
    RetrieveProjectContextQuery,
)
from src.session_management.application.ports import (
    IEnvironmentProvider,
    IProjectRepository,
    RepositoryError,
)
from src.session_management.domain import InvalidProjectIdError, ProjectId, ValidationResult

if TYPE_CHECKING:
    from src.application.ports.secondary.ilocal_context_reader import ILocalContextReader


class RetrieveProjectContextQueryHandler:
    """Handler for RetrieveProjectContextQuery.

    Retrieves the full context for the current project configuration.
    Uses injected dependencies to access filesystem and environment.

    Project resolution precedence:
    1. JERRY_PROJECT environment variable (highest)
    2. Local context active_project
    3. Discovery (available_projects list)

    Attributes:
        _repository: Repository for project operations
        _environment: Provider for environment variables
        _local_context_reader: Optional reader for local context
    """

    def __init__(
        self,
        repository: IProjectRepository,
        environment: IEnvironmentProvider,
        local_context_reader: ILocalContextReader | None = None,
    ) -> None:
        """Initialize the handler with dependencies.

        Args:
            repository: Repository for project operations
            environment: Provider for environment variables
            local_context_reader: Optional reader for .jerry/local/context.toml
                                  (backward compatible - None means ignore local context)
        """
        self._repository = repository
        self._environment = environment
        self._local_context_reader = local_context_reader

    def handle(self, query: RetrieveProjectContextQuery) -> dict[str, Any]:
        """Handle the RetrieveProjectContextQuery.

        Implements precedence order for project resolution:
        1. JERRY_PROJECT environment variable (highest precedence)
        2. Local context active_project (.jerry/local/context.toml)
        3. Project discovery (available_projects for user selection)

        Args:
            query: Query data containing base_path

        Returns:
            Dictionary with context information:
            - jerry_project: The resolved project string (from env or local context)
            - project_id: Parsed ProjectId (or None if invalid/not set)
            - validation: ValidationResult for the project (or None)
            - available_projects: List of ProjectInfo for selection
            - next_number: Next available project number
        """
        # Step 1: Check environment variable (highest precedence)
        jerry_project = self._environment.get_env("JERRY_PROJECT")

        # Step 2: Fall back to local context if env not set
        if jerry_project is None and self._local_context_reader is not None:
            jerry_project = self._local_context_reader.get_active_project()

        result: dict[str, Any] = {
            "jerry_project": jerry_project,
            "project_id": None,
            "validation": None,
            "available_projects": [],
            "next_number": 1,
        }

        # Step 3: Scan for available projects (discovery)
        try:
            result["available_projects"] = self._repository.scan_projects(query.base_path)
            if result["available_projects"]:
                max_num = max(p.id.number for p in result["available_projects"])
                result["next_number"] = min(max_num + 1, 999)
        except RepositoryError:
            # If we can't scan, leave defaults
            pass

        # Step 4: If project is set (from env or local), validate it
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
