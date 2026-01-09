"""
Infrastructure Layer - Session Management Bounded Context

Concrete implementations of ports (adapters for external systems).

Components:
    - adapters/: Adapter implementations (FilesystemProjectAdapter, OsEnvironmentAdapter)
"""

from .adapters import FilesystemProjectAdapter, OsEnvironmentAdapter

__all__ = [
    "FilesystemProjectAdapter",
    "OsEnvironmentAdapter",
]
