# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""FrontmatterFileResult -- validation result for a single .md file."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class FrontmatterFileResult:
    """Validation result for a single .md file.

    Attributes:
        path: Absolute path to the file.
        file_type: Either 'agent' or 'skill'.
        relative_path: Path relative to repository root.
        status: One of 'pass', 'pass_with_warnings', 'fail',
                'no_frontmatter', 'parse_error'.
        errors: List of (field, constraint, current_value) tuples.
        warnings: List of (field, constraint, current_value) tuples.
        frontmatter: Parsed YAML dict, or None if unavailable.
    """

    path: Path
    file_type: str
    relative_path: str
    status: str = "unknown"
    errors: list[tuple[str, str, str]] = field(default_factory=list)
    warnings: list[tuple[str, str, str]] = field(default_factory=list)
    frontmatter: dict[str, Any] | None = None

    @property
    def passed(self) -> bool:
        """Return True if this file passed (with or without warnings)."""
        return self.status in ("pass", "pass_with_warnings")

    @property
    def failed(self) -> bool:
        """Return True if this file failed validation."""
        return self.status in ("fail", "no_frontmatter", "parse_error")
