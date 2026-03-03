# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ComposeSkillResult - Result of composing SKILL.md files.

References:
    - PROJ-012: Skill Composition Pipeline
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ComposeSkillResult:
    """Result of composing SKILL.md files with governance sections.

    Attributes:
        composed: Number of skills successfully composed.
        failed: Number of skills that failed.
        output_paths: List of output file paths written.
        errors: List of error messages for failures.
        warnings: List of non-fatal warning messages.
        dry_run: Whether this was a dry-run.
    """

    composed: int = 0
    failed: int = 0
    output_paths: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    dry_run: bool = False
