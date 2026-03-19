# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""GenerateDocsResult - Result from generating README documentation sections.

This result contains the outcome of a docs generation operation, including
rendered section content, drift detection results, and aggregate statistics.

References:
    - doc-module-spec.md Section: CLI Integration
    - PROJ-0037: Auto-Documentation Module
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class GenerateDocsResult:
    """Result from generating README documentation sections.

    Attributes:
        success: Whether the generation operation succeeded.
        sections: Mapping of marker names to rendered section content.
            Keys are section identifiers (e.g., ``"SKILLS_TABLE"``,
            ``"FEATURES"``).  Values are the fully rendered markdown strings.
        drift_detected: Three-state drift indicator:
            - ``True``: drift detected — README content differs from generated
              (``"check"`` mode).
            - ``False``: no drift — content matches (``"check"`` mode), or
              README was successfully updated (``"write"`` mode).
            - ``None``: not applicable — stdout/default mode (no file I/O).
        skills_count: Number of skills discovered and rendered.
        agents_count: Total number of agents across all skills.
        warnings: Non-fatal warnings encountered during extraction or rendering
            (e.g., skipped skills with missing required fields).
        error: Error details when ``success`` is ``False``.  Contains at
            minimum a ``"code"`` key and a ``"message"`` key.
    """

    success: bool
    sections: dict[str, str] = field(default_factory=dict)
    drift_detected: bool | None = None
    skills_count: int = 0
    agents_count: int = 0
    warnings: list[str] = field(default_factory=list)
    error: dict[str, str] | None = None
