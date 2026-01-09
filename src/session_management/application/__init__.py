"""
Application Layer - Session Management Bounded Context

Use cases (commands and queries) that orchestrate domain logic.
This layer depends on the domain layer and defines ports for infrastructure.

Components:
    - ports/: Secondary port interfaces (IProjectRepository, IEnvironmentProvider)
    - queries/: Read operations (ScanProjects, ValidateProject, etc.)
    - commands/: Write operations (future)
"""

from .ports import IProjectRepository, IEnvironmentProvider, RepositoryError
from .queries import (
    ScanProjectsQuery,
    ValidateProjectQuery,
    GetNextProjectNumberQuery,
    GetProjectContextQuery,
)

__all__ = [
    # Ports
    "IProjectRepository",
    "IEnvironmentProvider",
    "RepositoryError",
    # Queries
    "ScanProjectsQuery",
    "ValidateProjectQuery",
    "GetNextProjectNumberQuery",
    "GetProjectContextQuery",
]
