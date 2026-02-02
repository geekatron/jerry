"""
CancelWorkItemCommand - Command to cancel a work item.

Data class containing the information needed to cancel a work item.
Logic is in CancelWorkItemCommandHandler.

References:
    - PHASE-45-ITEMS-COMMANDS.md: Implementation tracker
    - PAT-CQRS-001: Command Pattern
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CancelWorkItemCommand:
    """Command to cancel a work item.

    This command transitions a work item to CANCELLED state.
    The reason is optional but recommended for documentation.

    Attributes:
        work_item_id: The unique identifier of the work item to cancel
        reason: Optional reason for cancellation (for audit trail)

    Example:
        >>> command = CancelWorkItemCommand(
        ...     work_item_id="WORK-001",
        ...     reason="Requirements changed, feature no longer needed",
        ... )
    """

    work_item_id: str
    reason: str | None = None
