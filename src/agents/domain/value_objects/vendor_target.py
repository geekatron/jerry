# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
VendorTarget - Target LLM vendor for agent file generation.

References:
    - ADR-PROJ010-003: LLM Portability Architecture
"""

from __future__ import annotations

from enum import Enum


class VendorTarget(Enum):
    """Target vendor for agent file generation.

    Attributes:
        CLAUDE_CODE: Anthropic Claude Code (priority implementation).
        OPENAI: OpenAI API (future).
        GOOGLE_ADK: Google Agent Development Kit (future).
        OLLAMA: Ollama local models (future).

    Example:
        >>> VendorTarget.from_string("claude_code")
        <VendorTarget.CLAUDE_CODE: 'claude_code'>
    """

    CLAUDE_CODE = "claude_code"
    OPENAI = "openai"
    GOOGLE_ADK = "google_adk"
    OLLAMA = "ollama"

    @classmethod
    def from_string(cls, value: str) -> VendorTarget:
        """Parse vendor target from string.

        Args:
            value: Vendor name (case-insensitive).

        Returns:
            Matching VendorTarget enum value.

        Raises:
            ValueError: If value is not a valid vendor target.
        """
        normalized = value.lower().strip()
        for vendor in cls:
            if vendor.value == normalized:
                return vendor
        valid = [v.value for v in cls]
        raise ValueError(f"Invalid vendor target: {value!r}. Valid targets: {', '.join(valid)}")
