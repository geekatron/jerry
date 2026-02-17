# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
FilesystemLocalContextAdapter - Local Context File Reader.

Implements ILocalContextReader for reading .jerry/local/context.toml
files from the filesystem.

This adapter:
- Reads TOML files from .jerry/local/context.toml
- Returns empty dict on missing file or parse errors (fail-safe)
- Never raises exceptions to callers

References:
    - EN-001: Session Start Hook TDD Cleanup
    - TD-006: Missing local context support in main CLI
"""

from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any


class FilesystemLocalContextAdapter:
    """Filesystem adapter for reading local context configuration.

    Reads machine-local configuration from .jerry/local/context.toml.
    This file is typically gitignored and contains user preferences
    and the active project selection.

    Attributes:
        _base_path: Root directory where .jerry/local/ is located
        _context_path: Full path to context.toml file
    """

    CONTEXT_FILE_PATH = ".jerry/local/context.toml"

    def __init__(self, base_path: Path | str) -> None:
        """Initialize the adapter with a base path.

        Args:
            base_path: Root directory containing .jerry/local/
        """
        self._base_path = Path(base_path)
        self._context_path = self._base_path / self.CONTEXT_FILE_PATH

    def read(self) -> dict[str, Any]:
        """Read the full local context configuration.

        Returns:
            Dictionary with parsed TOML content.
            Returns empty dict if file doesn't exist or is invalid.

        Note:
            This method never raises exceptions. It returns an empty
            dict on any error (missing file, invalid TOML, etc.)
        """
        if not self._context_path.exists():
            return {}

        try:
            with self._context_path.open("rb") as f:
                content = f.read()
                if not content:
                    return {}
                return tomllib.loads(content.decode("utf-8"))
        except (OSError, tomllib.TOMLDecodeError, UnicodeDecodeError):
            return {}

    def get_active_project(self) -> str | None:
        """Get the active project ID from local context.

        Convenience method to read context.active_project directly.

        Returns:
            The active project ID string, or None if not set.

        Note:
            This method never raises exceptions. It returns None
            if the file doesn't exist, is invalid, or if
            context.active_project is not defined.
        """
        context = self.read()
        context_section = context.get("context", {})
        active_project = context_section.get("active_project")

        # Ensure it's a string or None
        if isinstance(active_project, str):
            return active_project
        return None
