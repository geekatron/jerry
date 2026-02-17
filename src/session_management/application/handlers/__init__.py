# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Session Management Handlers.

Command and Query handlers for session management operations.
Handlers contain the application logic and coordinate domain operations.

Command Handlers:
    CreateSessionCommandHandler: Handle session creation
    EndSessionCommandHandler: Handle session completion
    AbandonSessionCommandHandler: Handle session abandonment

Query Handlers:
    GetSessionStatusQueryHandler: Get current session status
"""

from .commands import (
    AbandonSessionCommandHandler,
    CreateSessionCommandHandler,
    EndSessionCommandHandler,
)
from .queries import GetSessionStatusQueryHandler

__all__ = [
    "CreateSessionCommandHandler",
    "EndSessionCommandHandler",
    "AbandonSessionCommandHandler",
    "GetSessionStatusQueryHandler",
]
