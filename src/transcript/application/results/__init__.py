# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Transcript application results.

This module provides result data classes for transcript commands.

References:
    - TDD-FEAT-004 Section 11: Jerry CLI Integration
    - TASK-251: Implement CLI Transcript Namespace
"""

from __future__ import annotations

from .parse_transcript_result import ParseTranscriptResult

__all__ = ["ParseTranscriptResult"]
