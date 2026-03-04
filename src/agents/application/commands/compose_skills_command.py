# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ComposeSkillsCommand - Command to compose SKILL.md files with governance sections.

References:
    - PROJ-012: Skill Composition Pipeline
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ComposeSkillsCommand:
    """Command to compose SKILL.md files by injecting governance sections.

    Reads skill.jerry.yaml canonical source, builds governance sections,
    and injects them into SKILL.md body.

    Attributes:
        skill_name: Optional specific skill to compose. None = compose all.
        dry_run: If True, show what would be generated without writing.
    """

    skill_name: str | None = None
    dry_run: bool = False
