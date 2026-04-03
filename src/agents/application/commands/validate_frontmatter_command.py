# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ValidateFrontmatterCommand -- Command for claude-code frontmatter validation.

References:
    - PROJ-024: CLI frontmatter validation command
    - STORY-025: Port P-003 validation from standalone script
    - docs/schemas/claude-code-frontmatter-v1.schema.json
    - docs/schemas/claude-code-skill-frontmatter-v1.schema.json
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ValidateFrontmatterCommand:
    """Command for validating Claude Code frontmatter in agent and skill files.

    Attributes:
        agent_filter: If set, validate only this single agent by name (stem of .md file).
        skill_filter: If set, validate only the SKILL.md for this skill directory name.
        repo_root: Absolute path to repository root. Resolved from __file__ if None.
    """

    agent_filter: str | None = None
    skill_filter: str | None = None
    repo_root: Path | None = None
