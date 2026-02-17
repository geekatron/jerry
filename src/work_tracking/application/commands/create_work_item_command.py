# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
CreateWorkItemCommand - Command to create a new work item.

Data class containing the information needed to create a work item.
Logic is in CreateWorkItemCommandHandler.

References:
    - PHASE-45-ITEMS-COMMANDS.md: Implementation tracker
    - PAT-CQRS-001: Command Pattern
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CreateWorkItemCommand:
    """Command to create a new work item.

    This command creates a new work item with the specified properties.
    The handler will generate a unique ID and emit a WorkItemCreated event.

    Attributes:
        title: The title of the work item (required)
        work_type: The type of work (task, bug, story, spike). Defaults to "task"
        priority: The priority level (low, medium, high, critical). Defaults to "medium"
        description: Optional detailed description
        parent_id: Optional parent work item ID for hierarchical items

    Example:
        >>> command = CreateWorkItemCommand(
        ...     title="Implement login feature",
        ...     work_type="story",
        ...     priority="high",
        ...     description="Add OAuth2 login support",
        ... )
    """

    title: str
    work_type: str = "task"
    priority: str = "medium"
    description: str = ""
    parent_id: str | None = None
