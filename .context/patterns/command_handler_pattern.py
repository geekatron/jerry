"""
Command/Query Handler Pattern - Canonical CQRS implementation for Jerry Framework.

Commands modify state and return None. Queries read state and return DTOs.
Handlers are injected with dependencies, receive data via handle() method.

This file is SELF-CONTAINED for use as a reference pattern. Any types
needed from other patterns are defined inline with minimal stubs.

References:
    - architecture-standards.md (lines 66-93)
    - application/queries/retrieve_project_context_query.py
    - CQRS pattern (Martin Fowler)

Exports:
    Example command, query, and handler implementations
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

# ---------------------------------------------------------------------------
# Inline stub for WorkItem aggregate (from aggregate_pattern.py)
# In real code, import from the domain layer.
# ---------------------------------------------------------------------------


class WorkItem:
    """
    Stub for pattern reference. See aggregate_pattern.py for full implementation.

    In real code this would be imported from the domain layer, e.g.:
        from src.work_tracking.domain.aggregates.work_item import WorkItem
    """

    def __init__(self, id: str) -> None:
        """Initialize stub."""
        self._id = id

    @classmethod
    def create(cls, id: str, title: str, priority: str = "medium") -> WorkItem:
        """Factory method to create a new work item."""
        if not title:
            raise ValueError("Title cannot be empty")
        return cls(id)

    @property
    def id(self) -> str:
        """Unique identifier."""
        return self._id


# =============================================================================
# Command Pattern
# =============================================================================


@dataclass(frozen=True)
class CreateWorkItemCommand:
    """
    Example command - Request to create a new work item.

    Commands SHOULD:
    - Use {Verb}{Noun}Command naming pattern
    - Be frozen dataclasses (immutable)
    - Return None or domain events from handlers
    - Contain all data needed to execute the operation

    File naming: create_work_item_command.py

    Attributes:
        title: Human-readable title
        work_type: Type classification
        priority: Priority level

    Example:
        >>> cmd = CreateWorkItemCommand(
        ...     title="Implement login",
        ...     work_type="task",
        ...     priority="high",
        ... )
    """

    title: str
    work_type: str = "task"
    priority: str = "medium"


class CreateWorkItemCommandHandler:
    """
    Example command handler - Executes CreateWorkItemCommand.

    Handlers SHOULD:
    - Use {CommandName}Handler naming pattern
    - Accept dependencies via constructor
    - Accept command data via handle() method
    - Validate business rules before executing
    - Return None or domain events

    File naming: create_work_item_command_handler.py

    Dependencies are injected at construction time.
    Command data is passed to handle() at execution time.

    Example:
        >>> handler = CreateWorkItemCommandHandler(repository, id_generator)
        >>> handler.handle(CreateWorkItemCommand("Implement login"))
    """

    def __init__(
        self,
        repository: IWorkItemRepository,
        id_generator: IIdGenerator,
    ) -> None:
        """
        Initialize handler with dependencies.

        Args:
            repository: Repository for persisting work items
            id_generator: Service for generating unique IDs
        """
        self._repository = repository
        self._id_generator = id_generator

    def handle(self, command: CreateWorkItemCommand) -> None:
        """
        Execute the CreateWorkItemCommand.

        Args:
            command: Command data containing title, work_type, priority

        Raises:
            ValidationError: If command data is invalid
            InvariantViolationError: If business rules are violated

        Example:
            >>> cmd = CreateWorkItemCommand("Implement login", priority="high")
            >>> handler.handle(cmd)
        """
        # Generate unique ID
        work_item_id = self._id_generator.generate()

        # Create aggregate via factory method
        # In real code: from src.work_tracking.domain.aggregates.work_item import WorkItem
        work_item = WorkItem.create(
            id=str(work_item_id),
            title=command.title,
            priority=command.priority,
        )

        # Persist aggregate
        self._repository.save(work_item)


# =============================================================================
# Query Pattern
# =============================================================================


@dataclass(frozen=True)
class RetrieveProjectContextQuery:
    """
    Example query - Request for project context data.

    Queries SHOULD:
    - Use {Verb}{Noun}Query naming pattern
    - Be frozen dataclasses (immutable)
    - Return DTOs (not domain entities) from handlers
    - Contain parameters needed for data retrieval

    Verb selection:
    - Get/Retrieve: Single item by ID
    - List: Collection of items
    - Scan: Discovery operation
    - Validate: Validation check

    File naming: retrieve_project_context_query.py

    Attributes:
        base_path: Path to the projects directory

    Example:
        >>> query = RetrieveProjectContextQuery(base_path="/projects")
    """

    base_path: str


class RetrieveProjectContextQueryHandler:
    """
    Example query handler - Executes RetrieveProjectContextQuery.

    Handlers SHOULD:
    - Use {QueryName}Handler naming pattern
    - Accept dependencies via constructor
    - Accept query data via handle() method
    - Return DTOs (dictionaries or dataclasses), never domain entities

    File naming: retrieve_project_context_query_handler.py

    Dependencies are injected at construction time.
    Query data is passed to handle() at execution time.

    Example:
        >>> handler = RetrieveProjectContextQueryHandler(repository, environment)
        >>> context = handler.handle(RetrieveProjectContextQuery("/projects"))
        >>> context["jerry_project"]
        'PROJ-001-example'
    """

    def __init__(
        self,
        repository: IProjectRepository,
        environment: IEnvironmentProvider,
    ) -> None:
        """
        Initialize handler with dependencies.

        Args:
            repository: Repository for project operations
            environment: Provider for environment variables
        """
        self._repository = repository
        self._environment = environment

    def handle(self, query: RetrieveProjectContextQuery) -> dict[str, Any]:
        """
        Execute the RetrieveProjectContextQuery.

        Args:
            query: Query data containing base_path

        Returns:
            Dictionary with context information (DTO):
            - jerry_project: The resolved project string
            - project_id: Parsed ProjectId (or None)
            - available_projects: List of ProjectInfo
            - next_number: Next available project number

        Example:
            >>> query = RetrieveProjectContextQuery("/projects")
            >>> result = handler.handle(query)
            >>> result["jerry_project"]
            'PROJ-001-example'
        """
        # Get environment variable
        jerry_project = self._environment.get_env("JERRY_PROJECT")

        result: dict[str, Any] = {
            "jerry_project": jerry_project,
            "project_id": None,
            "available_projects": [],
            "next_number": 1,
        }

        # Scan for available projects
        result["available_projects"] = self._repository.scan_projects(query.base_path)

        if result["available_projects"]:
            max_num = max(p.id.number for p in result["available_projects"])
            result["next_number"] = min(max_num + 1, 999)

        # Parse and validate if project is set
        if jerry_project:
            # In real code: from src.session_management.domain import ProjectId
            try:
                project_id = self._repository.parse_project_id(jerry_project)
                result["project_id"] = project_id
                result["validation"] = self._repository.validate_project(
                    query.base_path, project_id
                )
            except Exception as e:
                result["validation"] = {"valid": False, "errors": [str(e)]}

        return result


# =============================================================================
# Protocol Definitions (Ports)
# =============================================================================


class IWorkItemRepository:
    """
    Example secondary port - Repository for work items.

    Ports SHOULD:
    - Use I{Noun} naming pattern
    - Be defined in application/ports/secondary or domain/ports
    - Use Protocol or ABC for interface definition
    """

    def save(self, work_item: Any) -> None:
        """Persist a work item."""
        ...

    def get(self, id: str) -> Any | None:
        """Retrieve a work item by ID."""
        ...


class IIdGenerator:
    """
    Example secondary port - ID generation service.

    Domain services defined as ports.
    """

    def generate(self) -> int:
        """Generate a unique ID."""
        ...


class IProjectRepository:
    """Example secondary port - Repository for projects."""

    def scan_projects(self, base_path: str) -> list[Any]:
        """Scan for available projects."""
        ...

    def validate_project(self, base_path: str, project_id: Any) -> dict[str, Any]:
        """Validate a project."""
        ...

    def parse_project_id(self, project_string: str) -> Any:
        """Parse a project ID string into a ProjectId value object."""
        ...


class IEnvironmentProvider:
    """Example secondary port - Environment variable access."""

    def get_env(self, name: str) -> str | None:
        """Get environment variable value."""
        ...
