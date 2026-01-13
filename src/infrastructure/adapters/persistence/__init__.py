"""Persistence adapters for file I/O operations.

Provides adapters for safe concurrent file access with locking and atomic writes.
"""

from src.infrastructure.adapters.persistence.atomic_file_adapter import AtomicFileAdapter

__all__ = ["AtomicFileAdapter"]
