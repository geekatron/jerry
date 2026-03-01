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


@dataclass(frozen=True)
class ComposeAgentsCommand:
    """Command to compose agent files by merging defaults with canonical source.

    Compose writes to the same skill-scoped paths as build
    (skills/{skill}/agents/{agent}.md), replacing the build output
    with defaults-merged full-frontmatter versions.

    Attributes:
        vendor: Target vendor adapter name (e.g., 'claude_code').
        agent_name: Optional specific agent to compose. None = compose all.
        clean: If True, remove existing agent .md files before writing.
        dry_run: If True, show what would be generated without writing.
    """

    vendor: str
    agent_name: str | None = None
    clean: bool = False
    dry_run: bool = False
