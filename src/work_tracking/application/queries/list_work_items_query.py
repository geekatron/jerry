# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ListWorkItemsQuery - Query to list work items with optional filtering.

Data class containing query parameters for work item listing.
Logic is in ListWorkItemsQueryHandler.

References:
    - PAT-CQRS-002: Query Pattern
    - Phase 4.4: Items Namespace Implementation
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ListWorkItemsQuery:
    """Query to list work items with optional filtering.

    This query supports filtering by status and pagination through
    limit parameter.

    Attributes:
        status: Optional status filter (pending, in_progress, etc.)
        limit: Maximum number of items to return (None for all)

    Example:
        >>> query = ListWorkItemsQuery(status="in_progress", limit=10)
        >>> query = ListWorkItemsQuery()  # All items
    """

    status: str | None = None
    limit: int | None = None
