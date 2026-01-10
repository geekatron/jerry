"""
Aggregate module for work_tracking domain.

Contains AggregateRoot base class for event-sourced aggregates.

References:
    - PAT-001: Event Store Interface Pattern
    - IMPL-ES-003: AggregateRoot Base Class implementation
"""
from __future__ import annotations

from .base import AggregateRoot

__all__ = [
    "AggregateRoot",
]
