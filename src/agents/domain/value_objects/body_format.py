# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
BodyFormat - System prompt body format for vendor transformation.

References:
    - ADR-PROJ010-003: LLM Portability Architecture
"""

from __future__ import annotations

from enum import Enum


class BodyFormat(Enum):
    """Prompt body output format.

    Attributes:
        XML: Convert ## headings to XML tags (Claude-optimized).
        MARKDOWN: Pass through markdown headings unchanged.
        RCCF: Reorder to Role-Context-Constraints-Format.

    Example:
        >>> BodyFormat.from_string("xml")
        <BodyFormat.XML: 'xml'>
    """

    XML = "xml"
    MARKDOWN = "markdown"
    RCCF = "rccf"

    @classmethod
    def from_string(cls, value: str) -> BodyFormat:
        """Parse body format from string.

        Args:
            value: Format name (case-insensitive).

        Returns:
            Matching BodyFormat enum value.

        Raises:
            ValueError: If value is not a valid body format.
        """
        normalized = value.lower().strip()
        for fmt in cls:
            if fmt.value == normalized:
                return fmt
        valid = [f.value for f in cls]
        raise ValueError(f"Invalid body format: {value!r}. Valid formats: {', '.join(valid)}")
