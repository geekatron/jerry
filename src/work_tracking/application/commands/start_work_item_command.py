# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
StartWorkItemCommand - Command to start work on an item.

Data class containing the information needed to start a work item.
Logic is in StartWorkItemCommandHandler.

References:
    - PHASE-45-ITEMS-COMMANDS.md: Implementation tracker
    - PAT-CQRS-001: Command Pattern
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StartWorkItemCommand:
    """Command to start work on a work item.

    This command transitions a work item from PENDING to IN_PROGRESS state.
    The handler will retrieve the work item, call start_work(), and persist.

    Attributes:
        work_item_id: The unique identifier of the work item to start
        reason: Optional reason for starting (for audit trail)

    Example:
        >>> command = StartWorkItemCommand(
        ...     work_item_id="WORK-001",
        ...     reason="Starting implementation phase",
        ... )
    """

    work_item_id: str
    reason: str | None = None
