"""
Work Tracking Infrastructure Layer.

Exports adapters for work item persistence.
"""

from src.work_tracking.infrastructure.adapters import InMemoryWorkItemRepository

__all__ = [
    "InMemoryWorkItemRepository",
]
