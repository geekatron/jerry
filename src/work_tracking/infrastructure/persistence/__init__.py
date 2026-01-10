"""
Work Tracking Persistence Adapters.

Infrastructure layer implementations of domain ports for
event storage and persistence.

Components:
    - InMemoryEventStore: Thread-safe in-memory event store (test double)

References:
    - PAT-001: Event Store Interface Pattern
    - PAT-003: Optimistic Concurrency with File Locking
"""
from __future__ import annotations

from .in_memory_event_store import InMemoryEventStore

__all__ = [
    "InMemoryEventStore",
]
