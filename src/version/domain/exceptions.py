# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Domain exceptions for the version bounded context.

References:
    - BUG-002: Version bump regex rejects uppercase scopes
"""

from __future__ import annotations

from src.shared_kernel.exceptions import DomainError


class CommitParseError(DomainError):
    """Failed to parse a conventional commit subject.

    Attributes:
        subject: The commit subject that failed to parse.
        reason: Why parsing failed.
    """

    def __init__(self, subject: str, reason: str) -> None:
        self.subject = subject
        self.reason = reason
        super().__init__(f"Cannot parse commit '{subject}': {reason}")
