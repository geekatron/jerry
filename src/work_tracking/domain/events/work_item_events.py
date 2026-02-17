# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
WorkItem Domain Events.

Domain events for the WorkItem aggregate. These events capture all
significant state changes in work items.

All events are:
    - Immutable (frozen dataclasses)
    - Named in past tense
    - Contain aggregate reference data from DomainEvent base

References:
    - ADR-009: Event Storage Mechanism
    - impl-es-e-006-workitem-schema: WorkItem event catalog
    - DDD Domain Events pattern (Evans, 2004)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from src.shared_kernel.domain_event import DomainEvent, _current_timestamp, _generate_event_id

# =============================================================================
# WorkItem Creation Event
# =============================================================================


@dataclass(frozen=True)
class WorkItemCreated(DomainEvent):
    """
    Emitted when a new work item is created.

    This is the first event in any work item's event stream.
    It contains all initial data for the work item.

    Attributes:
        title: Human-readable title of the work item
        work_type: Type classification (task, bug, story, etc.)
        priority: Priority level (critical, high, medium, low)
        description: Optional detailed description
        parent_id: Optional parent work item's internal ID

    Example:
        >>> event = WorkItemCreated(
        ...     aggregate_id="12345",
        ...     aggregate_type="WorkItem",
        ...     title="Implement login",
        ...     work_type="task",
        ...     priority="high",
        ... )
    """

    title: str = ""
    work_type: str = "task"
    priority: str = "medium"
    description: str = ""
    parent_id: str | None = None

    def _payload(self) -> dict[str, Any]:
        """Return event-specific payload data."""
        return {
            "title": self.title,
            "work_type": self.work_type,
            "priority": self.priority,
            "description": self.description,
            "parent_id": self.parent_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> WorkItemCreated:
        """Deserialize from dictionary."""
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
            description=data.get("description", ""),
            parent_id=data.get("parent_id"),
        )


# =============================================================================
# Status Change Events
# =============================================================================


@dataclass(frozen=True)
class StatusChanged(DomainEvent):
    """
    Emitted when work item status transitions.

    Records the state machine transition with optional reason.

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


@dataclass(frozen=True)
class WorkItemCompleted(DomainEvent):
    """
    Emitted when work item reaches a terminal state (DONE or CANCELLED).

    Contains completion metrics for tracking and reporting.

    Attributes:
        final_status: Terminal status (done or cancelled)
        duration_seconds: Total time from creation to completion
        completion_reason: Optional reason for completion/cancellation

    Example:
        >>> event = WorkItemCompleted(
        ...     aggregate_id="12345",
        ...     aggregate_type="WorkItem",
        ...     final_status="done",
        ...     duration_seconds=3600,
        ... )
    """

    final_status: str = "done"
    duration_seconds: int = 0
    completion_reason: str | None = None

    def _payload(self) -> dict[str, Any]:
        """Return event-specific payload data."""
        return {
            "final_status": self.final_status,
            "duration_seconds": self.duration_seconds,
            "completion_reason": self.completion_reason,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> WorkItemCompleted:
        """Deserialize from dictionary."""
        timestamp_str = data.get("timestamp")
        timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else _current_timestamp()

        return cls(
            event_id=data.get("event_id", _generate_event_id()),
            aggregate_id=data["aggregate_id"],
            aggregate_type=data.get("aggregate_type", "WorkItem"),
            version=data.get("version", 1),
            timestamp=timestamp,
            final_status=data.get("final_status", "done"),
            duration_seconds=data.get("duration_seconds", 0),
            completion_reason=data.get("completion_reason"),
        )


# =============================================================================
# Priority Change Events
# =============================================================================


@dataclass(frozen=True)
class PriorityChanged(DomainEvent):
    """
    Emitted when work item priority is adjusted.

    Attributes:
        old_priority: Previous priority value
        new_priority: New priority value
        reason: Optional reason for priority change

    Example:
        >>> event = PriorityChanged(
        ...     aggregate_id="12345",
        ...     aggregate_type="WorkItem",
        ...     old_priority="medium",
        ...     new_priority="critical",
        ...     reason="Production issue",
        ... )
    """

    old_priority: str = ""
    new_priority: str = ""
    reason: str | None = None

    def _payload(self) -> dict[str, Any]:
        """Return event-specific payload data."""
        return {
            "old_priority": self.old_priority,
            "new_priority": self.new_priority,
            "reason": self.reason,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PriorityChanged:
        """Deserialize from dictionary."""
        timestamp_str = data.get("timestamp")
        timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else _current_timestamp()

        return cls(
            event_id=data.get("event_id", _generate_event_id()),
            aggregate_id=data["aggregate_id"],
            aggregate_type=data.get("aggregate_type", "WorkItem"),
            version=data.get("version", 1),
            timestamp=timestamp,
            old_priority=data.get("old_priority", ""),
            new_priority=data.get("new_priority", ""),
            reason=data.get("reason"),
        )


# =============================================================================
# Quality Metrics Events
# =============================================================================


@dataclass(frozen=True)
class QualityMetricsUpdated(DomainEvent):
    """
    Emitted when test results are recorded for the work item.

    Contains coverage, test distribution, and quality gate evaluation.

    Attributes:
        coverage_percent: Test coverage percentage (0-100), or None
        positive_tests: Count of happy path tests
        negative_tests: Count of error handling tests
        edge_case_tests: Count of boundary condition tests
        gate_level: Quality gate level evaluated (L0, L1, L2)
        gate_passed: Whether quality gate requirements were met
        gate_failures: List of specific gate failures

    Example:
        >>> event = QualityMetricsUpdated(
        ...     aggregate_id="12345",
        ...     aggregate_type="WorkItem",
        ...     coverage_percent=85.5,
        ...     positive_tests=10,
        ...     negative_tests=5,
        ...     edge_case_tests=3,
        ...     gate_level="L2",
        ...     gate_passed=True,
        ... )
    """

    coverage_percent: float | None = None
    positive_tests: int | None = None
    negative_tests: int | None = None
    edge_case_tests: int | None = None
    gate_level: str | None = None
    gate_passed: bool = False
    gate_failures: tuple[str, ...] = field(default_factory=tuple)

    def _payload(self) -> dict[str, Any]:
        """Return event-specific payload data."""
        return {
            "coverage_percent": self.coverage_percent,
            "positive_tests": self.positive_tests,
            "negative_tests": self.negative_tests,
            "edge_case_tests": self.edge_case_tests,
            "gate_level": self.gate_level,
            "gate_passed": self.gate_passed,
            "gate_failures": list(self.gate_failures),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> QualityMetricsUpdated:
        """Deserialize from dictionary."""
        timestamp_str = data.get("timestamp")
        timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else _current_timestamp()

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
            edge_case_tests=data.get("edge_case_tests"),
            gate_level=data.get("gate_level"),
            gate_passed=data.get("gate_passed", False),
            gate_failures=gate_failures,
        )


# =============================================================================
# Dependency Events
# =============================================================================


@dataclass(frozen=True)
class DependencyAdded(DomainEvent):
    """
    Emitted when a dependency is linked to the work item.

    Attributes:
        dependency_id: ID of the work item that this item depends on
        dependency_type: Type of dependency (blocks, blocked_by, related)

    Example:
        >>> event = DependencyAdded(
        ...     aggregate_id="12345",
        ...     aggregate_type="WorkItem",
        ...     dependency_id="67890",
        ...     dependency_type="blocks",
        ... )
    """

    dependency_id: str = ""
    dependency_type: str = "blocks"

    def _payload(self) -> dict[str, Any]:
        """Return event-specific payload data."""
        return {
            "dependency_id": self.dependency_id,
            "dependency_type": self.dependency_type,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DependencyAdded:
        """Deserialize from dictionary."""
        timestamp_str = data.get("timestamp")
        timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else _current_timestamp()

        return cls(
            event_id=data.get("event_id", _generate_event_id()),
            aggregate_id=data["aggregate_id"],
            aggregate_type=data.get("aggregate_type", "WorkItem"),
            version=data.get("version", 1),
            timestamp=timestamp,
            dependency_id=data.get("dependency_id", ""),
            dependency_type=data.get("dependency_type", "blocks"),
        )


@dataclass(frozen=True)
class DependencyRemoved(DomainEvent):
    """
    Emitted when a dependency is unlinked from the work item.

    Attributes:
        dependency_id: ID of the work item that was unlinked

    Example:
        >>> event = DependencyRemoved(
        ...     aggregate_id="12345",
        ...     aggregate_type="WorkItem",
        ...     dependency_id="67890",
        ... )
    """

    dependency_id: str = ""

    def _payload(self) -> dict[str, Any]:
        """Return event-specific payload data."""
        return {
            "dependency_id": self.dependency_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DependencyRemoved:
        """Deserialize from dictionary."""
        timestamp_str = data.get("timestamp")
        timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else _current_timestamp()

        return cls(
            event_id=data.get("event_id", _generate_event_id()),
            aggregate_id=data["aggregate_id"],
            aggregate_type=data.get("aggregate_type", "WorkItem"),
            version=data.get("version", 1),
            timestamp=timestamp,
            dependency_id=data.get("dependency_id", ""),
        )


# =============================================================================
# Assignee Events
# =============================================================================


@dataclass(frozen=True)
class AssigneeChanged(DomainEvent):
    """
    Emitted when work item is reassigned.

    Attributes:
        old_assignee: Previous assignee (agent or human), or None
        new_assignee: New assignee (agent or human), or None

    Example:
        >>> event = AssigneeChanged(
        ...     aggregate_id="12345",
        ...     aggregate_type="WorkItem",
        ...     old_assignee=None,
        ...     new_assignee="agent:qa-engineer",
        ... )
    """

    old_assignee: str | None = None
    new_assignee: str | None = None

    def _payload(self) -> dict[str, Any]:
        """Return event-specific payload data."""
        return {
            "old_assignee": self.old_assignee,
            "new_assignee": self.new_assignee,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AssigneeChanged:
        """Deserialize from dictionary."""
        timestamp_str = data.get("timestamp")
        timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else _current_timestamp()

        return cls(
            event_id=data.get("event_id", _generate_event_id()),
            aggregate_id=data["aggregate_id"],
            aggregate_type=data.get("aggregate_type", "WorkItem"),
            version=data.get("version", 1),
            timestamp=timestamp,
            old_assignee=data.get("old_assignee"),
            new_assignee=data.get("new_assignee"),
        )
