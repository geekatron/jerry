"""
Infrastructure Layer - Session Management Bounded Context

Concrete implementations of ports (adapters for external systems).

Components:
    - adapters/: Adapter implementations (FilesystemProjectAdapter, OsEnvironmentAdapter,
                 InMemorySessionRepository)
"""

from .adapters import FilesystemProjectAdapter, InMemorySessionRepository, OsEnvironmentAdapter

__all__ = [
    "FilesystemProjectAdapter",
    "InMemorySessionRepository",
    "OsEnvironmentAdapter",
]
