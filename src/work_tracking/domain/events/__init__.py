"""
Work Tracking Domain Events.

Domain events for the work_tracking bounded context.
All events are immutable and named in past tense.

Components:
    - WorkItem Events: Events for work item lifecycle
    - QualityGate Events: Events for gate execution tracking

References:
    - ADR-008: Quality Gate Layer Configuration
    - ADR-009: Event Storage Mechanism
    - impl-es-e-006-workitem-schema: WorkItem event catalog
"""
from __future__ import annotations

from .quality_gate_events import (
    GateCheckCompleted,
    GateExecutionCompleted,
    GateExecutionStarted,
    RiskAssessed,
    ThresholdViolation,
)
from .work_item_events import (
    AssigneeChanged,
    DependencyAdded,
    DependencyRemoved,
    PriorityChanged,
    QualityMetricsUpdated,
    StatusChanged,
    WorkItemCompleted,
    WorkItemCreated,
)

__all__ = [
    # WorkItem Events
    "WorkItemCreated",
    "StatusChanged",
    "PriorityChanged",
    "QualityMetricsUpdated",
    "WorkItemCompleted",
    "DependencyAdded",
    "DependencyRemoved",
    "AssigneeChanged",
    # QualityGate Events
    "GateExecutionStarted",
    "GateCheckCompleted",
    "GateExecutionCompleted",
    "RiskAssessed",
    "ThresholdViolation",
]
