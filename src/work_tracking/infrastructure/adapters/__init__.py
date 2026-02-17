# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Work Tracking Infrastructure Adapters.

Exports:
    InMemoryWorkItemRepository: In-memory implementation of IWorkItemRepository
"""

from src.work_tracking.infrastructure.adapters.in_memory_work_item_repository import (
    InMemoryWorkItemRepository,
)

__all__ = [
    "InMemoryWorkItemRepository",
]
