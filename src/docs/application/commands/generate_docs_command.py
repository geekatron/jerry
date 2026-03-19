# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""GenerateDocsCommand - Command to generate README documentation sections.

This command instructs the system to extract skill metadata and render
auto-generated documentation sections into the README.md file.

References:
    - doc-module-spec.md Section: CLI Integration
    - PROJ-0037: Auto-Documentation Module
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GenerateDocsCommand:
    """Command to generate auto-documentation sections for the README.

    Attributes:
        readme_path: Path to the README.md file to operate on.
        mode: Execution mode — one of:
            ``None``      print generated content only (default / stdout)
            ``"check"``   compare generated against current README; set drift_detected
            ``"write"``   atomically rewrite README with generated sections
    """

    readme_path: str = "README.md"
    mode: str | None = None
