"""
Aggregate module for work_tracking domain.

Contains AggregateRoot base class and concrete aggregate implementations.

Components:
    - AggregateRoot: Base class for event-sourced aggregates
    - WorkItem: Primary work tracking aggregate

References:
    - PAT-001: Event Store Interface Pattern
    - IMPL-ES-003: AggregateRoot Base Class implementation
    - IMPL-005: WorkItem Aggregate implementation
"""
from __future__ import annotations

from .base import AggregateRoot
from .work_item import QualityGateNotMetError, WorkItem

__all__ = [
    "AggregateRoot",
    "WorkItem",
    "QualityGateNotMetError",
]
