"""
Work Tracking Application Ports.

Exports:
    IWorkItemRepository: Port for work item persistence operations
"""

from src.work_tracking.application.ports.work_item_repository import IWorkItemRepository

__all__ = [
    "IWorkItemRepository",
]
