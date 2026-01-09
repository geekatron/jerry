"""
Shared Kernel - Cross-cutting value objects for Jerry Framework.

This module contains foundational types shared across all bounded contexts:
- Identity: VertexId hierarchy, EdgeId, JerryUri
- Audit: IAuditable protocol
- Concurrency: IVersioned protocol
- Base classes: EntityBase
- Exceptions: Domain error hierarchy

References:
    - Canon Section "Shared Kernel Specification" (L1716-1860)
"""
from __future__ import annotations

# Exceptions
from .exceptions import (
    ConcurrencyError,
    DomainError,
    InvariantViolationError,
    InvalidStateError,
    InvalidStateTransitionError,
    NotFoundError,
    ValidationError,
)

# Identity
from .vertex_id import (
    ActorId,
    EdgeId,
    EventId,
    KnowledgeId,
    PhaseId,
    PlanId,
    SubtaskId,
    TaskId,
    VertexId,
)
from .jerry_uri import JerryUri

# Protocols
from .auditable import IAuditable
from .versioned import IVersioned

# Base classes
from .entity_base import EntityBase


__all__ = [
    # Exceptions
    "DomainError",
    "NotFoundError",
    "InvalidStateError",
    "InvalidStateTransitionError",
    "InvariantViolationError",
    "ConcurrencyError",
    "ValidationError",
    # Identity
    "VertexId",
    "TaskId",
    "PhaseId",
    "PlanId",
    "SubtaskId",
    "KnowledgeId",
    "ActorId",
    "EventId",
    "EdgeId",
    "JerryUri",
    # Protocols
    "IAuditable",
    "IVersioned",
    # Base classes
    "EntityBase",
]
