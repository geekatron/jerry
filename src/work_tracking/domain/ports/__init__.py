"""
Work Tracking Domain Ports.

Ports define contracts (interfaces) that the domain requires from
external systems. Adapters in the infrastructure layer implement these.

Components:
    - IEventStore: Append-only event storage with optimistic concurrency
    - StoredEvent: Immutable wrapper for persisted events
    - ConcurrencyError: Raised on version conflicts

References:
    - PAT-001: Event Store Interface Pattern
    - PAT-003: Optimistic Concurrency with File Locking
    - ADR-009: Event Storage Mechanism
"""
from __future__ import annotations

from .event_store import (
    ConcurrencyError,
    EventStoreError,
    IEventStore,
    StoredEvent,
    StreamNotFoundError,
)

__all__ = [
    # Event Store
    "IEventStore",
    "StoredEvent",
    "ConcurrencyError",
    "StreamNotFoundError",
    "EventStoreError",
]
