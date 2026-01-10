"""
Work Tracking Domain Layer.

Contains the core domain model: value objects, entities, aggregates,
domain events, and domain services.

This layer has NO external dependencies (stdlib only).
"""
from __future__ import annotations

# Value Objects
from .value_objects.work_item_id import WorkItemId

__all__ = [
    "WorkItemId",
]
