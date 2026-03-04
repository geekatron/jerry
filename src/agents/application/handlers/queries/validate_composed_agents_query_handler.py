# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ValidateComposedAgentsQueryHandler - Validates composed agent .md files.

Loads composed .md files from skill agent directories and runs
ComposeValidator checks (CV-001 through CV-007) against each.

References:
    - PROJ-012: Agent Configuration Extraction & Schema Enforcement
    - P-022: No Deception (silent pass-through violates this)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

from src.agents.application.queries.validate_composed_agents_query import (
    ValidateComposedAgentsQuery,
)
from src.agents.domain.services.compose_validator import (
    ComposeValidator,
)

if TYPE_CHECKING:
    pass


@dataclass
class ComposedValidationResult:
    """Result of validating composed agent files.

    Attributes:
        total: Total agents checked.
        passed: Number that passed validation.
        failed: Number that failed (had errors).
        warnings_count: Number of agents with warnings only.
        errors: List of error messages.
        warnings: List of warning messages.
        is_valid: True if no errors.
    """

    total: int = 0
    passed: int = 0
    failed: int = 0
    warnings_count: int = 0
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        """Check if all agents passed (no errors)."""
        return self.failed == 0


class ValidateComposedAgentsQueryHandler:
    """Handler for ValidateComposedAgentsQuery.

    Loads composed .md files from skill agent directories and
    runs ComposeValidator checks against each.

    Attributes:
        _skills_dir: Path to the skills/ directory.
        _validator: ComposeValidator instance.
    """

    def __init__(
        self,
        skills_dir: Path,
        validator: ComposeValidator,
    ) -> None:
        """Initialize with dependencies.

        Args:
            skills_dir: Path to skills/ directory containing agent files.
            validator: ComposeValidator for running checks.
        """
        self._skills_dir = skills_dir
        self._validator = validator

    def handle(self, query: ValidateComposedAgentsQuery) -> ComposedValidationResult:
        """Handle the ValidateComposedAgentsQuery.

        Args:
            query: Query with optional agent name filter.

        Returns:
            ComposedValidationResult with validation outcomes.
        """
        # Find composed agent .md files
        agent_files = self._find_composed_agents(query.agent_name)
        result = ComposedValidationResult(total=len(agent_files))

        for agent_path in agent_files:
            agent_name = agent_path.stem
            content = agent_path.read_text(encoding="utf-8")

            validation = self._validator.validate(content, agent_name=agent_name)

            if validation.errors:
                result.failed += 1
                for finding in validation.errors:
                    result.errors.append(f"{agent_name}: [{finding.check_id}] {finding.message}")
            else:
                result.passed += 1

            if validation.warnings:
                result.warnings_count += 1
                for finding in validation.warnings:
                    result.warnings.append(f"{agent_name}: [{finding.check_id}] {finding.message}")

        return result

    def _find_composed_agents(self, agent_name: str | None) -> list[Path]:
        """Find composed agent .md files in skill directories.

        Args:
            agent_name: Optional specific agent name to find.

        Returns:
            List of paths to composed .md files.
        """
        agent_files: list[Path] = []

        if not self._skills_dir.exists():
            return agent_files

        for skill_dir in sorted(self._skills_dir.iterdir()):
            if not skill_dir.is_dir():
                continue
            agents_dir = skill_dir / "agents"
            if not agents_dir.exists():
                continue
            for md_file in sorted(agents_dir.glob("*.md")):
                if agent_name and md_file.stem != agent_name:
                    continue
                agent_files.append(md_file)

        return agent_files
