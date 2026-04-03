# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""ValidateFrontmatterResult -- aggregated result for frontmatter validation."""

from __future__ import annotations

from dataclasses import dataclass, field

from src.agents.application.commands.frontmatter_file_result import (
    FrontmatterFileResult,
)


@dataclass
class ValidateFrontmatterResult:
    """Aggregated result for the full validate-frontmatter command.

    Attributes:
        agent_results: Per-file results for agent .md files.
        skill_results: Per-file results for SKILL.md files.
    """

    agent_results: list[FrontmatterFileResult] = field(default_factory=list)
    skill_results: list[FrontmatterFileResult] = field(default_factory=list)

    @property
    def all_results(self) -> list[FrontmatterFileResult]:
        """Combined list of agent and skill results."""
        return self.agent_results + self.skill_results

    @property
    def total(self) -> int:
        """Total number of files examined."""
        return len(self.all_results)

    @property
    def passed(self) -> int:
        """Number of files that passed (including pass-with-warnings)."""
        return sum(1 for r in self.all_results if r.passed)

    @property
    def failed(self) -> int:
        """Number of files that failed."""
        return sum(1 for r in self.all_results if r.failed)

    @property
    def pass_with_warnings(self) -> int:
        """Number of files that passed with at least one warning."""
        return sum(1 for r in self.all_results if r.status == "pass_with_warnings")

    @property
    def no_frontmatter(self) -> int:
        """Number of files with no frontmatter block."""
        return sum(1 for r in self.all_results if r.status == "no_frontmatter")

    @property
    def parse_errors(self) -> int:
        """Number of files that could not be parsed."""
        return sum(1 for r in self.all_results if r.status == "parse_error")

    @property
    def is_valid(self) -> bool:
        """True only if zero files failed."""
        return self.failed == 0
