"""
Work Tracking Domain Ports.

Ports define contracts (interfaces) that the domain requires from
external systems. Adapters in the infrastructure layer implement these.

Components:
    - IEventStore: Append-only event storage with optimistic concurrency
    - IRepository: Generic aggregate persistence
    - StoredEvent: Immutable wrapper for persisted events

References:
    - PAT-001: Event Store Interface Pattern
    - PAT-003: Optimistic Concurrency with File Locking
    - PAT-009: Generic Repository Port
    - ADR-009: Event Storage Mechanism
"""

from __future__ import annotations

from .event_store import (
    ConcurrencyError as EventStoreConcurrencyError,
)
from .event_store import (
    EventStoreError,
    IEventStore,
    StoredEvent,
    StreamNotFoundError,
)
from .repository import (
    AggregateNotFoundError,
    IRepository,
    RepositoryError,
)
from .repository import (
    ConcurrencyError as RepositoryConcurrencyError,
)

__all__ = [
    # Event Store
    "IEventStore",
    "StoredEvent",
    "EventStoreConcurrencyError",
    "StreamNotFoundError",
    "EventStoreError",
    # Repository
    "IRepository",
    "AggregateNotFoundError",
    "RepositoryConcurrencyError",
    "RepositoryError",
]
