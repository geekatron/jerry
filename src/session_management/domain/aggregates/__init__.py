# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Session Management Domain Aggregates.

This module contains the aggregate roots for the session management domain.

Exports:
    Session: Event-sourced aggregate for work session tracking
"""

from __future__ import annotations

from .session import Session, SessionStatus

__all__ = ["Session", "SessionStatus"]
