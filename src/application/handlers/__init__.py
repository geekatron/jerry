"""
Application Handlers Package.

Contains query and command handlers that implement use cases.

Structure:
    queries/ - Query handlers (read operations)
    commands/ - Command handlers (write operations)

Exports:
    RetrieveProjectContextQueryHandler: Handler for RetrieveProjectContextQuery
    ScanProjectsQueryHandler: Handler for ScanProjectsQuery
    ValidateProjectQueryHandler: Handler for ValidateProjectQuery

Backward Compatibility Aliases (deprecated):
    GetProjectContextHandler -> RetrieveProjectContextQueryHandler
    GetProjectContextQueryData -> RetrieveProjectContextQuery
    ScanProjectsHandler -> ScanProjectsQueryHandler
    ScanProjectsQueryData -> ScanProjectsQuery
    ValidateProjectHandler -> ValidateProjectQueryHandler
    ValidateProjectQueryData -> ValidateProjectQuery
"""

# New imports from correct locations
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

# Backward compatibility aliases (deprecated - will be removed)
GetProjectContextHandler = RetrieveProjectContextQueryHandler
GetProjectContextQueryData = RetrieveProjectContextQuery
ScanProjectsHandler = ScanProjectsQueryHandler
ScanProjectsQueryData = ScanProjectsQuery
ValidateProjectHandler = ValidateProjectQueryHandler
ValidateProjectQueryData = ValidateProjectQuery

__all__ = [
    # New names
    "RetrieveProjectContextQueryHandler",
    "RetrieveProjectContextQuery",
    "ScanProjectsQueryHandler",
    "ScanProjectsQuery",
    "ValidateProjectQueryHandler",
    "ValidateProjectQuery",
    # Deprecated aliases
    "GetProjectContextHandler",
    "GetProjectContextQueryData",
    "ScanProjectsHandler",
    "ScanProjectsQueryData",
    "ValidateProjectHandler",
    "ValidateProjectQueryData",
]
