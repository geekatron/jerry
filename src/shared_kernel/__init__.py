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

# Protocols
from .auditable import IAuditable
from .domain_event import DomainEvent, EventRegistry, get_global_registry

# Base classes
from .entity_base import EntityBase

# Exceptions
from .exceptions import (
    ConcurrencyError,
    DomainError,
    InvalidStateError,
    InvalidStateTransitionError,
    InvariantViolationError,
    NotFoundError,
    ValidationError,
)
from .jerry_uri import JerryUri
from .snowflake_id import SnowflakeIdGenerator
from .versioned import IVersioned

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
    "SnowflakeIdGenerator",
    "DomainEvent",
    "EventRegistry",
    "get_global_registry",
    # Protocols
    "IAuditable",
    "IVersioned",
    # Base classes
    "EntityBase",
]
