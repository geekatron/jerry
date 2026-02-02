"""
Read Models Infrastructure - Adapter Implementations.

This module provides concrete implementations of IReadModelStore
for persisting and retrieving materialized views.

Available Adapters:
    - InMemoryReadModelStore: Volatile in-memory storage (for testing)
"""

from __future__ import annotations

from src.infrastructure.read_models.in_memory_read_model_store import (
    InMemoryReadModelStore,
)

__all__ = [
    "InMemoryReadModelStore",
]
