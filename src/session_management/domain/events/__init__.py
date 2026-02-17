# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Domain Events - Facts that happened in the past.

Domain events use past tense (e.g., ProjectCreated, not CreateProject).
They are immutable records of something that occurred.

Exports:
    SessionCreated: Event emitted when a new session is created
    SessionCompleted: Event emitted when a session is completed
    SessionAbandoned: Event emitted when a session is abandoned
    SessionProjectLinked: Event emitted when a session is linked to a project
"""

from __future__ import annotations

from .session_events import (
    SessionAbandoned,
    SessionCompleted,
    SessionCreated,
    SessionProjectLinked,
)

__all__ = [
    "SessionCreated",
    "SessionCompleted",
    "SessionAbandoned",
    "SessionProjectLinked",
]
