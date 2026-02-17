# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
GetWorkItemQuery - Query to retrieve a single work item by ID.

Data class containing query parameters for work item retrieval.
Logic is in GetWorkItemQueryHandler.

References:
    - PAT-CQRS-002: Query Pattern
    - Phase 4.4: Items Namespace Implementation
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GetWorkItemQuery:
    """Query to retrieve a single work item by ID.

    Attributes:
        work_item_id: The unique identifier of the work item to retrieve

    Example:
        >>> query = GetWorkItemQuery(work_item_id="12345")
    """

    work_item_id: str
