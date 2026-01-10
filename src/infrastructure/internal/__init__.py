"""
Infrastructure Internal Abstractions.

These are PRIVATE to the infrastructure layer and should NOT be
exposed to domain or application layers.

Components:
    - IFileStore: File operations abstraction (read/write/lock)
    - ISerializer: Serialization abstraction (serialize/deserialize)
    - LocalFileStore: Local filesystem implementation
    - JsonSerializer: JSON format implementation

Design Principles:
    - These abstractions are composed by repository adapters
    - They enable testability through dependency injection
    - They are NOT ports (ports are in domain/application layers)

References:
    - PAT-010: Composed Infrastructure Adapters
    - WORKTRACKER: IMPL-REPO-002
"""
from __future__ import annotations

from .file_store import IFileStore, LocalFileStore
from .serializer import ISerializer, JsonSerializer

__all__ = [
    "IFileStore",
    "LocalFileStore",
    "ISerializer",
    "JsonSerializer",
]
