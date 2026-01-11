"""
Ports - Interface Definitions for Infrastructure Adapters

Ports define the contracts that infrastructure adapters must implement.
This follows the Hexagonal Architecture (Ports & Adapters) pattern.

These are "secondary ports" (driven) - they are called by the application
to interact with external systems (filesystem, environment, etc.).
"""

from .environment import IEnvironmentProvider
from .exceptions import RepositoryError
from .project_repository import IProjectRepository

__all__ = [
    "IProjectRepository",
    "IEnvironmentProvider",
    "RepositoryError",
]
