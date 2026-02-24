# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
BuildResult - Result of a vendor-specific agent build operation.

References:
    - ADR-PROJ010-003: LLM Portability Architecture
"""

from __future__ import annotations

from dataclasses import dataclass, field

from src.agents.domain.entities.generated_artifact import GeneratedArtifact


@dataclass
class BuildResult:
    """Result of a build operation.

    Attributes:
        built: Number of agents successfully built.
        failed: Number of agents that failed to build.
        artifacts: List of generated artifacts.
        errors: List of error messages for failed agents.
        dry_run: Whether this was a dry-run (no files written).
    """

    built: int = 0
    failed: int = 0
    artifacts: list[GeneratedArtifact] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    dry_run: bool = False
