"""
Work Tracking Domain Events.

Domain events for the work_tracking bounded context.
All events are immutable and named in past tense.

Components:
    - WorkItem Events: Events for work item lifecycle

References:
    - ADR-009: Event Storage Mechanism
    - impl-es-e-006-workitem-schema: WorkItem event catalog
"""
from __future__ import annotations

from .work_item_events import (
    WorkItemCreated,
    StatusChanged,
    PriorityChanged,
    QualityMetricsUpdated,
    WorkItemCompleted,
    DependencyAdded,
    DependencyRemoved,
    AssigneeChanged,
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
]
