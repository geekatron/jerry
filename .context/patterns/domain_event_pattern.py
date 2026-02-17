"""
Domain Event Pattern - Canonical implementation for Jerry Framework.

Domain events are immutable value objects representing significant state changes.
Use past-tense naming and include EVENT_TYPE class variable.

References:
    - architecture-standards.md (line 98)
    - shared_kernel/domain_event.py
    - ADR-009: Event Storage Mechanism

Exports:
    Example domain events following Jerry conventions
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from src.shared_kernel.domain_event import DomainEvent, _current_timestamp, _generate_event_id

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
        """Return event-specific payload data."""
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
