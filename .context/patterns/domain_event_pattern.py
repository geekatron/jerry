"""
Domain Event Pattern - Canonical implementation for Jerry Framework.

Domain events are immutable value objects representing significant state changes.
Use past-tense naming and include EVENT_TYPE class variable.

This file is SELF-CONTAINED for use as a reference pattern. The real base class
lives in src/shared_kernel/domain_event.py. The inline DomainEvent here is a
simplified version matching the real API surface.

References:
    - architecture-standards.md (line 98)
    - shared_kernel/domain_event.py (authoritative implementation)
    - ADR-009: Event Storage Mechanism

Exports:
    Example domain events following Jerry conventions
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

# ---------------------------------------------------------------------------
# Inline helpers (mirrors shared_kernel/domain_event.py)
# In real code, import from src.shared_kernel.domain_event instead.
# ---------------------------------------------------------------------------


def _generate_event_id() -> str:
    """Generate a unique event ID. Real impl uses EventId.generate()."""
    return f"EVT-{uuid.uuid4()}"


def _current_timestamp() -> datetime:
    """Get current UTC timestamp."""
    return datetime.now(UTC)


# ---------------------------------------------------------------------------
# Inline DomainEvent base class (simplified from shared_kernel/domain_event.py)
# In real code, import DomainEvent from src.shared_kernel.domain_event.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DomainEvent:
    """
    Base class for all domain events (simplified pattern version).

    The authoritative implementation is in src/shared_kernel/domain_event.py.
    This inline version captures the essential API for pattern reference.

    Attributes:
        aggregate_id: ID of the aggregate this event belongs to
        aggregate_type: Type name of the aggregate (e.g., "WorkItem")
        event_id: Unique identifier for this event instance
        timestamp: When the event occurred (UTC)
        version: Version number of the aggregate after this event
    """

    aggregate_id: str
    aggregate_type: str
    event_id: str = field(default_factory=_generate_event_id)
    timestamp: datetime = field(default_factory=_current_timestamp)
    version: int = 1

    def __post_init__(self) -> None:
        """Validate event after initialization."""
        if not self.aggregate_id:
            raise ValueError("aggregate_id cannot be empty")
        if not self.aggregate_type:
            raise ValueError("aggregate_type cannot be empty")
        if self.version < 1:
            raise ValueError("version must be >= 1")

    def to_dict(self) -> dict[str, Any]:
        """Serialize event to dictionary."""
        return {
            "event_type": self.__class__.__name__,
            "event_id": self.event_id,
            "aggregate_id": self.aggregate_id,
            "aggregate_type": self.aggregate_type,
            "version": self.version,
            "timestamp": self.timestamp.isoformat(),
            **self._payload(),
        }

    def _payload(self) -> dict[str, Any]:
        """
        Return event-specific payload data.

        The base class returns an empty dict by default. Override in subclasses
        ONLY if you have additional fields to serialize. Overriding is OPTIONAL.

        Returns:
            Dictionary of additional event-specific data.
        """
        return {}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DomainEvent:
        """Deserialize event from dictionary."""
        timestamp_str = data.get("timestamp")
        timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else _current_timestamp()
        return cls(
            event_id=data.get("event_id", _generate_event_id()),
            aggregate_id=data["aggregate_id"],
            aggregate_type=data["aggregate_type"],
            version=data.get("version", 1),
            timestamp=timestamp,
        )


# =============================================================================
# Pattern 1: Simple Creation Event
# =============================================================================


@dataclass(frozen=True)
class WorkItemCreated(DomainEvent):
    """
    Example creation event - first event in an aggregate's stream.

    Domain events SHOULD:
    - Use past tense naming (Created, not Create)
    - Inherit from DomainEvent base class
    - Be frozen (immutable) dataclasses
    - Include all data needed to reconstruct state

    Attributes:
        title: Human-readable title
        work_type: Type classification
        priority: Priority level

    Example:
        >>> event = WorkItemCreated(
        ...     aggregate_id="12345",
        ...     aggregate_type="WorkItem",
        ...     title="Implement login",
        ...     work_type="task",
        ...     priority="high",
        ... )
        >>> event.title
        'Implement login'
    """

    title: str = ""
    work_type: str = "task"
    priority: str = "medium"

    def _payload(self) -> dict[str, Any]:
        """
        Return event-specific payload data.

        Override is OPTIONAL -- the base class returns {} by default.
        Override only when your event has additional fields beyond the
        base DomainEvent fields (aggregate_id, aggregate_type, version, etc.).
        """
        return {
            "title": self.title,
            "work_type": self.work_type,
            "priority": self.priority,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> WorkItemCreated:
        """
        Deserialize from dictionary.

        Factory method for event reconstitution from storage.

        Args:
            data: Dictionary containing event fields

        Returns:
            Reconstructed event instance

        Example:
            >>> data = {
            ...     "aggregate_id": "12345",
            ...     "aggregate_type": "WorkItem",
            ...     "title": "Implement login",
            ...     "work_type": "task",
            ... }
            >>> event = WorkItemCreated.from_dict(data)
        """
        timestamp_str = data.get("timestamp")
        timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else _current_timestamp()

        return cls(
            event_id=data.get("event_id", _generate_event_id()),
            aggregate_id=data["aggregate_id"],
            aggregate_type=data.get("aggregate_type", "WorkItem"),
            version=data.get("version", 1),
            timestamp=timestamp,
            title=data.get("title", ""),
            work_type=data.get("work_type", "task"),
            priority=data.get("priority", "medium"),
        )


# =============================================================================
# Pattern 2: State Transition Event
# =============================================================================


@dataclass(frozen=True)
class StatusChanged(DomainEvent):
    """
    Example state transition event - records before and after values.

    Captures state machine transitions with optional reason.

    Attributes:
        old_status: Previous status value
        new_status: New status value
        reason: Optional reason for the transition

    Example:
        >>> event = StatusChanged(
        ...     aggregate_id="12345",
        ...     aggregate_type="WorkItem",
        ...     old_status="pending",
        ...     new_status="in_progress",
        ...     reason="Starting implementation",
        ... )
    """

    old_status: str = ""
    new_status: str = ""
    reason: str | None = None

    def _payload(self) -> dict[str, Any]:
        """Return event-specific payload data."""
        return {
            "old_status": self.old_status,
            "new_status": self.new_status,
            "reason": self.reason,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> StatusChanged:
        """Deserialize from dictionary."""
        timestamp_str = data.get("timestamp")
        timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else _current_timestamp()

        return cls(
            event_id=data.get("event_id", _generate_event_id()),
            aggregate_id=data["aggregate_id"],
            aggregate_type=data.get("aggregate_type", "WorkItem"),
            version=data.get("version", 1),
            timestamp=timestamp,
            old_status=data.get("old_status", ""),
            new_status=data.get("new_status", ""),
            reason=data.get("reason"),
        )


# =============================================================================
# Pattern 3: Complex Event with Collections
# =============================================================================


@dataclass(frozen=True)
class QualityMetricsUpdated(DomainEvent):
    """
    Example complex event - contains metrics and gate evaluation.

    Demonstrates handling of optional fields and collections.

    Attributes:
        coverage_percent: Test coverage percentage (0-100), or None
        positive_tests: Count of happy path tests
        negative_tests: Count of error handling tests
        gate_level: Quality gate level evaluated
        gate_passed: Whether quality gate requirements were met
        gate_failures: List of specific gate failures (immutable tuple)

    Example:
        >>> event = QualityMetricsUpdated(
        ...     aggregate_id="12345",
        ...     aggregate_type="WorkItem",
        ...     coverage_percent=85.5,
        ...     positive_tests=10,
        ...     negative_tests=5,
        ...     gate_level="L2",
        ...     gate_passed=True,
        ... )
    """

    coverage_percent: float | None = None
    positive_tests: int | None = None
    negative_tests: int | None = None
    gate_level: str | None = None
    gate_passed: bool = False
    gate_failures: tuple[str, ...] = field(default_factory=tuple)

    def _payload(self) -> dict[str, Any]:
        """Return event-specific payload data."""
        return {
            "coverage_percent": self.coverage_percent,
            "positive_tests": self.positive_tests,
            "negative_tests": self.negative_tests,
            "gate_level": self.gate_level,
            "gate_passed": self.gate_passed,
            "gate_failures": list(self.gate_failures),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> QualityMetricsUpdated:
        """Deserialize from dictionary."""
        timestamp_str = data.get("timestamp")
        timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else _current_timestamp()

        # Convert list to tuple for immutability
        gate_failures = data.get("gate_failures", [])
        if isinstance(gate_failures, list):
            gate_failures = tuple(gate_failures)

        return cls(
            event_id=data.get("event_id", _generate_event_id()),
            aggregate_id=data["aggregate_id"],
            aggregate_type=data.get("aggregate_type", "WorkItem"),
            version=data.get("version", 1),
            timestamp=timestamp,
            coverage_percent=data.get("coverage_percent"),
            positive_tests=data.get("positive_tests"),
            negative_tests=data.get("negative_tests"),
            gate_level=data.get("gate_level"),
            gate_passed=data.get("gate_passed", False),
            gate_failures=gate_failures,
        )
