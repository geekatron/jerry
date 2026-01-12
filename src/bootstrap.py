"""
Composition Root - Application Bootstrap.

This module is the sole owner of dependency wiring.
It creates infrastructure adapters and wires them to handlers.

The key principle: NO adapter should instantiate its own dependencies.
All dependencies are created HERE and injected.

This follows the Composition Root pattern from Clean Architecture:
- Infrastructure adapters are instantiated here
- Handlers receive adapters via constructor injection
- Dispatcher is configured with handlers
- CLI adapter receives the dispatcher

Example:
    >>> from src.bootstrap import create_query_dispatcher
    >>> dispatcher = create_query_dispatcher()
    >>> # dispatcher is fully configured with all handlers
"""

from __future__ import annotations

import os
from pathlib import Path

from src.application.dispatchers.query_dispatcher import QueryDispatcher
from src.application.handlers.queries import (
    RetrieveProjectContextQueryHandler,
    ScanProjectsQueryHandler,
    ValidateProjectQueryHandler,
)
from src.application.queries import (
    RetrieveProjectContextQuery,
    ScanProjectsQuery,
    ValidateProjectQuery,
)
from src.session_management.infrastructure import (
    FilesystemProjectAdapter,
    OsEnvironmentAdapter,
)


def get_projects_directory() -> str:
    """Determine the projects directory path.

    Returns:
        Absolute path to the projects directory

    Resolution order:
        1. CLAUDE_PROJECT_DIR environment variable (set by Claude Code)
        2. Current working directory
    """
    project_root = os.environ.get("CLAUDE_PROJECT_DIR")
    if project_root:
        return str(Path(project_root) / "projects")

    return str(Path.cwd() / "projects")


def create_query_dispatcher() -> QueryDispatcher:
    """Create a fully configured QueryDispatcher.

    This is the factory function that wires all query handlers
    with their infrastructure dependencies.

    Returns:
        QueryDispatcher with all handlers registered
    """
    # Create infrastructure adapters (secondary adapters)
    repository = FilesystemProjectAdapter()
    environment = OsEnvironmentAdapter()

    # Create handlers with injected dependencies
    retrieve_project_context_handler = RetrieveProjectContextQueryHandler(
        repository=repository,
        environment=environment,
    )
    scan_projects_handler = ScanProjectsQueryHandler(
        repository=repository,
    )
    validate_project_handler = ValidateProjectQueryHandler(
        repository=repository,
    )

    # Create and configure dispatcher
    dispatcher = QueryDispatcher()
    dispatcher.register(RetrieveProjectContextQuery, retrieve_project_context_handler.handle)
    dispatcher.register(ScanProjectsQuery, scan_projects_handler.handle)
    dispatcher.register(ValidateProjectQuery, validate_project_handler.handle)

    return dispatcher
