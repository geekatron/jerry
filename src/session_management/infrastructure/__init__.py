# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

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
