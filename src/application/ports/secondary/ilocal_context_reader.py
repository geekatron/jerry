# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ILocalContextReader - Local Context Configuration Port.

Defines the contract for reading local context configuration from
.jerry/local/context.toml files.

This is a secondary port (driven) used by handlers to access
machine-local configuration that is not committed to git.

References:
    - EN-001: Session Start Hook TDD Cleanup
    - TD-006: Missing local context support in main CLI
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class ILocalContextReader(Protocol):
    """Protocol for reading local context configuration.

    Local context provides machine-specific configuration that
    overrides environment variables and is not committed to git.

    The context file is located at: .jerry/local/context.toml

    Example TOML structure:
        [context]
        active_project = "PROJ-007-jerry-bugs"

        [preferences]
        auto_save = true
        theme = "dark"

    Example:
        >>> reader = FilesystemLocalContextAdapter(base_path=Path("/workspace"))
        >>> context = reader.read()
        >>> project = reader.get_active_project()
    """

    def read(self) -> dict[str, Any]:
        """Read the full local context configuration.

        Returns:
            Dictionary with parsed TOML content.
            Returns empty dict if file doesn't exist or is invalid.

        Note:
            This method never raises exceptions. It returns an empty
            dict on any error (missing file, invalid TOML, etc.)
        """
        ...

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
        ...
