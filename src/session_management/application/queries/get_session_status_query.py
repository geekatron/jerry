# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
GetSessionStatusQuery - Query to get current session status.

Data class containing query parameters for session status retrieval.
Logic is in GetSessionStatusQueryHandler.

References:
    - ENFORCE-008d.3.2: Session aggregate
    - PAT-CQRS-002: Query Pattern
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GetSessionStatusQuery:
    """Query to get current session status.

    This query retrieves the status of the current active session,
    or indicates that no session is active.

    This is a parameterless query - it simply retrieves current state.

    Example:
        >>> query = GetSessionStatusQuery()
    """

    pass
