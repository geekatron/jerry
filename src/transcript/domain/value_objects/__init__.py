# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Transcript Domain Value Objects.

Exports:
- ParsedSegment: Canonical transcript segment representation
- ParseResult: Result from parsing operations

Reference: TDD-FEAT-004-hybrid-infrastructure.md v1.2.0, Section 4
"""

from src.transcript.domain.value_objects.parse_result import ParseResult
from src.transcript.domain.value_objects.parsed_segment import ParsedSegment

__all__ = ["ParsedSegment", "ParseResult"]
