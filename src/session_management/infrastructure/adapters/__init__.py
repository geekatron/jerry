"""
Adapters - Infrastructure Implementations of Ports

Adapters implement the port interfaces defined in the application layer.
They handle the technical details of external systems (filesystem, databases, etc.).
"""

from .filesystem_project_adapter import FilesystemProjectAdapter
from .in_memory_session_repository import InMemorySessionRepository
from .os_environment_adapter import OsEnvironmentAdapter

__all__ = [
    "FilesystemProjectAdapter",
    "InMemorySessionRepository",
    "OsEnvironmentAdapter",
]
