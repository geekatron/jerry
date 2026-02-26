# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ComposeAgentsCommand - Command to compose vendor-specific agent files with defaults.

References:
    - PROJ-012: Agent Configuration Extraction & Schema Enforcement
    - ADR-PROJ010-003: LLM Portability Architecture
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ComposeAgentsCommand:
    """Command to compose agent files by merging defaults with canonical source.

    Attributes:
        vendor: Target vendor adapter name (e.g., 'claude_code').
        agent_name: Optional specific agent to compose. None = compose all.
        output_dir: Directory to write composed files.
        clean: If True, remove existing .md files in output_dir before writing.
        dry_run: If True, show what would be generated without writing.
    """

    vendor: str
    output_dir: Path
    agent_name: str | None = None
    clean: bool = False
    dry_run: bool = False
