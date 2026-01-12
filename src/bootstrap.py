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
from src.session_management.application.handlers.commands import (
    AbandonSessionCommandHandler,
    CreateSessionCommandHandler,
    EndSessionCommandHandler,
)
from src.session_management.application.handlers.queries import GetSessionStatusQueryHandler
from src.session_management.application.queries import GetSessionStatusQuery
from src.session_management.infrastructure import (
    FilesystemProjectAdapter,
    InMemorySessionRepository,
    OsEnvironmentAdapter,
)
from src.work_tracking.application.handlers.queries import (
    GetWorkItemQueryHandler,
    ListWorkItemsQueryHandler,
)
from src.work_tracking.application.queries import (
    GetWorkItemQuery,
    ListWorkItemsQuery,
)
from src.work_tracking.infrastructure.adapters import InMemoryWorkItemRepository

# Module-level session repository singleton for session state persistence
# In production, this would be replaced with a file-based or database repository
_session_repository: InMemorySessionRepository | None = None

# Module-level work item repository singleton
# NOTE: TD-XXX - This is a simplified in-memory repository.
# Full event sourcing implementation is deferred to post-Phase 4.
_work_item_repository: InMemoryWorkItemRepository | None = None


def get_session_repository() -> InMemorySessionRepository:
    """Get the shared session repository instance.

    Returns:
        InMemorySessionRepository singleton instance

    Note:
        This is a module-level singleton to preserve session state
        across CLI invocations within the same process.
    """
    global _session_repository
    if _session_repository is None:
        _session_repository = InMemorySessionRepository()
    return _session_repository


def get_work_item_repository() -> InMemoryWorkItemRepository:
    """Get the shared work item repository instance.

    Returns:
        InMemoryWorkItemRepository singleton instance

    Note:
        This is a simplified in-memory repository. Full event sourcing
        implementation is deferred to post-Phase 4 (see TD-XXX).
    """
    global _work_item_repository
    if _work_item_repository is None:
        _work_item_repository = InMemoryWorkItemRepository()
    return _work_item_repository


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
    project_repository = FilesystemProjectAdapter()
    environment = OsEnvironmentAdapter()
    session_repository = get_session_repository()

    # Create project-related handlers
    retrieve_project_context_handler = RetrieveProjectContextQueryHandler(
        repository=project_repository,
        environment=environment,
    )
    scan_projects_handler = ScanProjectsQueryHandler(
        repository=project_repository,
    )
    validate_project_handler = ValidateProjectQueryHandler(
        repository=project_repository,
    )

    # Create session-related handlers
    get_session_status_handler = GetSessionStatusQueryHandler(
        repository=session_repository,
    )

    # Create work-item-related handlers
    work_item_repository = get_work_item_repository()
    list_work_items_handler = ListWorkItemsQueryHandler(
        repository=work_item_repository,
    )
    get_work_item_handler = GetWorkItemQueryHandler(
        repository=work_item_repository,
    )

    # Create and configure dispatcher
    dispatcher = QueryDispatcher()
    dispatcher.register(RetrieveProjectContextQuery, retrieve_project_context_handler.handle)
    dispatcher.register(ScanProjectsQuery, scan_projects_handler.handle)
    dispatcher.register(ValidateProjectQuery, validate_project_handler.handle)
    dispatcher.register(GetSessionStatusQuery, get_session_status_handler.handle)
    dispatcher.register(ListWorkItemsQuery, list_work_items_handler.handle)
    dispatcher.register(GetWorkItemQuery, get_work_item_handler.handle)

    return dispatcher


def create_session_command_handlers() -> dict:
    """Create session command handlers.

    Returns a dictionary of command handlers for session management.

    Returns:
        Dictionary mapping command types to handler instances
    """
    session_repository = get_session_repository()

    return {
        "create": CreateSessionCommandHandler(repository=session_repository),
        "end": EndSessionCommandHandler(repository=session_repository),
        "abandon": AbandonSessionCommandHandler(repository=session_repository),
    }
