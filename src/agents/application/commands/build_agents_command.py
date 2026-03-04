# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
BuildAgentsCommand - Command to build vendor-specific agent files.

References:
    - ADR-PROJ010-003: LLM Portability Architecture
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BuildAgentsCommand:
    """Command to build vendor-specific agent files from canonical source.

    Attributes:
        vendor: Target vendor name (e.g., 'claude_code').
        agent_name: Optional specific agent to build. None = build all.
        dry_run: If True, show what would be generated without writing.
    """

    vendor: str
    agent_name: str | None = None
    dry_run: bool = False
