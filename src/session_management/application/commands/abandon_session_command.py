"""
AbandonSessionCommand - Command to abandon the current session.

Data class containing the information needed to abandon a session.
Logic is in AbandonSessionCommandHandler.

References:
    - ENFORCE-008d.3.2: Session aggregate
    - PAT-CQRS-001: Command Pattern
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AbandonSessionCommand:
    """Command to abandon the current session.

    This command marks the current active session as abandoned.
    Use when the session cannot be completed normally, such as
    during context compaction or unexpected termination.

    Attributes:
        reason: Optional reason for abandonment

    Example:
        >>> command = AbandonSessionCommand(
        ...     reason="Context compaction triggered",
        ... )
    """

    reason: str | None = None
