# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
CompleteWorkItemCommand - Command to complete a work item.

Data class containing the information needed to complete a work item.
Logic is in CompleteWorkItemCommandHandler.

References:
    - PHASE-45-ITEMS-COMMANDS.md: Implementation tracker
    - PAT-CQRS-001: Command Pattern
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CompleteWorkItemCommand:
    """Command to complete a work item.

    This command transitions a work item from IN_PROGRESS to DONE state.
    The handler will retrieve the work item, call complete(), and persist.

    Attributes:
        work_item_id: The unique identifier of the work item to complete
        reason: Optional completion reason or summary (for audit trail)

    Example:
        >>> command = CompleteWorkItemCommand(
        ...     work_item_id="WORK-001",
        ...     reason="All acceptance criteria met",
        ... )
    """

    work_item_id: str
    reason: str | None = None
