"""
VertexId - Base class for all entity identifiers.

This module defines the VertexId base class and all domain-specific ID subclasses.
VertexId provides graph-ready abstraction enabling future migration to native graph databases.

References:
    - Canon PAT-001 (L56-117): VertexId base class
    - Canon PAT-002 (L119-165): Domain-specific IDs
    - Canon PAT-004 (L222-260): EdgeId

Exports:
    VertexId (base class)
    TaskId, PhaseId, PlanId, SubtaskId, KnowledgeId, ActorId, EventId (subclasses)
    EdgeId (relationship identifier)
"""
from __future__ import annotations

import re
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Pattern


@dataclass(frozen=True)
class VertexId(ABC):
    """
    Graph-ready abstraction for all entity IDs.

    Invariants:
        - Immutable (frozen dataclass)
        - Value equality (two VertexIds with same value are equal)
        - Valid format (subclass-specific validation)

    Usage:
        task_id = TaskId.generate()
        task_id = TaskId.from_string("TASK-a1b2c3d4")
    """

    value: str

    def __post_init__(self) -> None:
        if not self._is_valid_format(self.value):
            raise ValueError(f"Invalid {self.__class__.__name__} format: {self.value}")

    @classmethod
    @abstractmethod
    def _is_valid_format(cls, value: str) -> bool:
        """Subclass-specific format validation."""
        ...

    @classmethod
    @abstractmethod
    def generate(cls) -> VertexId:
        """Generate a new ID with proper format."""
        ...

    @classmethod
    def from_string(cls, value: str) -> VertexId:
        """Parse ID from string representation."""
        return cls(value)

    def __str__(self) -> str:
        return self.value

    def __hash__(self) -> int:
        return hash(self.value)


# Domain-Specific ID Classes


@dataclass(frozen=True)
class TaskId(VertexId):
    """Task entity identifier. Format: TASK-{uuid8}"""

    _PATTERN: ClassVar[Pattern[str]] = re.compile(r"^TASK-[a-f0-9]{8}$")

    @classmethod
    def _is_valid_format(cls, value: str) -> bool:
        return bool(cls._PATTERN.match(value))

    @classmethod
    def generate(cls) -> TaskId:
        return cls(f"TASK-{uuid.uuid4().hex[:8]}")


@dataclass(frozen=True)
class PhaseId(VertexId):
    """Phase entity identifier. Format: PHASE-{uuid8}"""

    _PATTERN: ClassVar[Pattern[str]] = re.compile(r"^PHASE-[a-f0-9]{8}$")

    @classmethod
    def _is_valid_format(cls, value: str) -> bool:
        return bool(cls._PATTERN.match(value))

    @classmethod
    def generate(cls) -> PhaseId:
        return cls(f"PHASE-{uuid.uuid4().hex[:8]}")


@dataclass(frozen=True)
class PlanId(VertexId):
    """Plan entity identifier. Format: PLAN-{uuid8}"""

    _PATTERN: ClassVar[Pattern[str]] = re.compile(r"^PLAN-[a-f0-9]{8}$")

    @classmethod
    def _is_valid_format(cls, value: str) -> bool:
        return bool(cls._PATTERN.match(value))

    @classmethod
    def generate(cls) -> PlanId:
        return cls(f"PLAN-{uuid.uuid4().hex[:8]}")


@dataclass(frozen=True)
class SubtaskId(VertexId):
    """Subtask entity identifier. Format: TASK-{uuid8}.{n}"""

    _PATTERN: ClassVar[Pattern[str]] = re.compile(r"^TASK-[a-f0-9]{8}\.\d+$")

    @classmethod
    def _is_valid_format(cls, value: str) -> bool:
        return bool(cls._PATTERN.match(value))

    @classmethod
    def generate(cls) -> SubtaskId:
        raise NotImplementedError("SubtaskId requires parent TaskId; use from_parent()")

    @classmethod
    def from_parent(cls, parent_id: TaskId, sequence: int) -> SubtaskId:
        """Create SubtaskId from parent TaskId and sequence number."""
        if sequence < 1:
            raise ValueError("Subtask sequence must be >= 1")
        return cls(f"{parent_id.value}.{sequence}")

    @property
    def parent_id(self) -> TaskId:
        """Extract parent TaskId from subtask ID."""
        parent_value = self.value.rsplit(".", 1)[0]
        return TaskId(parent_value)

    @property
    def sequence(self) -> int:
        """Extract sequence number from subtask ID."""
        return int(self.value.rsplit(".", 1)[1])


@dataclass(frozen=True)
class KnowledgeId(VertexId):
    """Knowledge entity identifier. Format: KNOW-{uuid8}"""

    _PATTERN: ClassVar[Pattern[str]] = re.compile(r"^KNOW-[a-f0-9]{8}$")

    @classmethod
    def _is_valid_format(cls, value: str) -> bool:
        return bool(cls._PATTERN.match(value))

    @classmethod
    def generate(cls) -> KnowledgeId:
        return cls(f"KNOW-{uuid.uuid4().hex[:8]}")


@dataclass(frozen=True)
class ActorId(VertexId):
    """Actor entity identifier. Format: ACTOR-{TYPE}-{id}"""

    _PATTERN: ClassVar[Pattern[str]] = re.compile(r"^ACTOR-[A-Z]+-[a-z0-9-]+$")

    @classmethod
    def _is_valid_format(cls, value: str) -> bool:
        return bool(cls._PATTERN.match(value))

    @classmethod
    def generate(cls) -> ActorId:
        raise NotImplementedError("ActorId requires type and id; use for_type()")

    @classmethod
    def for_type(cls, actor_type: str, actor_id: str) -> ActorId:
        """Create ActorId for specific actor type."""
        if not actor_type.isupper():
            raise ValueError("Actor type must be uppercase")
        if not actor_id.islower() or not actor_id.replace("-", "").isalnum():
            raise ValueError("Actor id must be lowercase alphanumeric with hyphens")
        return cls(f"ACTOR-{actor_type}-{actor_id}")

    @classmethod
    def claude(cls, instance: str = "main") -> ActorId:
        """Create ActorId for Claude agent."""
        return cls.for_type("CLAUDE", instance)

    @classmethod
    def system(cls) -> ActorId:
        """Create ActorId for system operations."""
        return cls.for_type("SYSTEM", "internal")


@dataclass(frozen=True)
class EventId(VertexId):
    """Event entity identifier. Format: EVT-{uuid}"""

    _PATTERN: ClassVar[Pattern[str]] = re.compile(
        r"^EVT-[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$"
    )

    @classmethod
    def _is_valid_format(cls, value: str) -> bool:
        return bool(cls._PATTERN.match(value))

    @classmethod
    def generate(cls) -> EventId:
        return cls(f"EVT-{uuid.uuid4()}")


# EdgeId for graph relationships


@dataclass(frozen=True)
class EdgeId:
    """
    Deterministic edge identifier generated from endpoints and label.

    Format: "{source_id}--{label}-->{target_id}"

    References:
        - Canon PAT-004 (L222-260)
    """

    source_id: VertexId
    target_id: VertexId
    label: str

    def __post_init__(self) -> None:
        if not self.label:
            raise ValueError("Edge label cannot be empty")
        if not self.label.isupper():
            raise ValueError("Edge label must be uppercase")

    @property
    def value(self) -> str:
        return f"{self.source_id}--{self.label}-->{self.target_id}"

    def __str__(self) -> str:
        return self.value

    def __hash__(self) -> int:
        return hash(self.value)
