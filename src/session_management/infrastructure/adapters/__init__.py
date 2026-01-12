"""
Adapters - Infrastructure Implementations of Ports

Adapters implement the port interfaces defined in the application layer.
They handle the technical details of external systems (filesystem, databases, etc.).
"""

from .filesystem_project_adapter import FilesystemProjectAdapter
from .os_environment_adapter import OsEnvironmentAdapter

__all__ = [
    "FilesystemProjectAdapter",
    "OsEnvironmentAdapter",
]
