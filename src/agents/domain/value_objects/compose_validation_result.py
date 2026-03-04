# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ComposeValidationResult - Result of validating a composed agent or skill output.

References:
    - PROJ-012: Agent Configuration Extraction & Schema Enforcement
"""

from __future__ import annotations

from dataclasses import dataclass, field

from src.agents.domain.value_objects.validation_finding import ValidationFinding


@dataclass
class ComposeValidationResult:
    """Result of validating a single composed agent or skill output.

    Attributes:
        agent_name: Name of the validated agent or skill.
        errors: List of error-severity findings.
        warnings: List of warning-severity findings.
    """

    agent_name: str = ""
    errors: list[ValidationFinding] = field(default_factory=list)
    warnings: list[ValidationFinding] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        """Check if no errors were found."""
        return len(self.errors) == 0

    def all_findings(self) -> list[ValidationFinding]:
        """Return all findings (errors + warnings)."""
        return self.errors + self.warnings
