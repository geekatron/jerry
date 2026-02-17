# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
BlockWorkItemCommand - Command to block a work item.

Data class containing the information needed to block a work item.
Logic is in BlockWorkItemCommandHandler.

References:
    - PHASE-45-ITEMS-COMMANDS.md: Implementation tracker
    - PAT-CQRS-001: Command Pattern
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BlockWorkItemCommand:
    """Command to block a work item.

    This command transitions a work item to BLOCKED state.
    The reason is required to document why the work is blocked.

    Attributes:
        work_item_id: The unique identifier of the work item to block
        reason: The reason for blocking (required for documentation)

    Example:
        >>> command = BlockWorkItemCommand(
        ...     work_item_id="WORK-001",
        ...     reason="Waiting for API documentation from external team",
        ... )
    """

    work_item_id: str
    reason: str
