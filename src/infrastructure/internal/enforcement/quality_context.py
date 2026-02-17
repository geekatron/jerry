# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Structured result type for quality context generation.

Provides the immutable ``QualityContext`` dataclass used by the
SessionQualityContextGenerator to communicate the quality framework
preamble and its metadata back to the SessionStart hook.

References:
    - EN-706: SessionStart Quality Context Injection
    - EPIC-002 EN-405/TASK-006: Quality preamble specification
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class QualityContext:
    """Structured result of quality context generation.

    Attributes:
        preamble: The XML quality framework preamble string.
        token_estimate: Estimated token count for the preamble.
        sections_included: Number of XML sections in the preamble.
    """

    preamble: str
    token_estimate: int
    sections_included: int
