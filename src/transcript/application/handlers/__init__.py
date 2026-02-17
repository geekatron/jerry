# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Transcript Application Handlers.

Command and query handlers for transcript operations.

Reference: TDD-FEAT-004-hybrid-infrastructure.md v1.2.0
"""

from __future__ import annotations

from .commands import ParseTranscriptCommandHandler

__all__ = ["ParseTranscriptCommandHandler"]
