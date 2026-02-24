# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ExtractResult - Result of a canonical extraction operation.

References:
    - ADR-PROJ010-003: LLM Portability Architecture
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ExtractResult:
    """Result of an extract operation.

    Attributes:
        extracted: Number of agents successfully extracted.
        failed: Number of agents that failed extraction.
        errors: List of error messages for failed agents.
    """

    extracted: int = 0
    failed: int = 0
    errors: list[str] = field(default_factory=list)
