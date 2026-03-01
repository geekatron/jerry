# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ComposeResult - Result of composing agent files.

References:
    - PROJ-012: Agent Configuration Extraction & Schema Enforcement
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ComposeResult:
    """Result of composing vendor-specific agent files with defaults.

    Attributes:
        composed: Number of agents successfully composed.
        failed: Number of agents that failed.
        output_paths: List of output file paths written.
        errors: List of error messages for failures.
        dry_run: Whether this was a dry-run.
    """

    composed: int = 0
    failed: int = 0
    output_paths: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    dry_run: bool = False
