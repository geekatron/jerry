# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
EndSessionCommand - Command to end the current session.

Data class containing the information needed to complete a session.
Logic is in EndSessionCommandHandler.

References:
    - ENFORCE-008d.3.2: Session aggregate
    - PAT-CQRS-001: Command Pattern
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EndSessionCommand:
    """Command to end the current session.

    This command marks the current active session as completed.
    If there's no active session, the handler will raise an error.

    Attributes:
        summary: Optional summary of work completed

    Example:
        >>> command = EndSessionCommand(
        ...     summary="Completed feature X, ready for review",
        ... )
    """

    summary: str | None = None
