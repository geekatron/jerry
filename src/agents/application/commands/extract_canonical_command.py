# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ExtractCanonicalCommand - Command to extract canonical source from vendor files.

References:
    - ADR-PROJ010-003: LLM Portability Architecture
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExtractCanonicalCommand:
    """Command to reverse-engineer canonical source from existing vendor files.

    Attributes:
        agent_name: Specific agent to extract. None = extract all.
        source_adapter: Source vendor format (default: 'claude_code').
    """

    agent_name: str | None = None
    source_adapter: str = "claude_code"
