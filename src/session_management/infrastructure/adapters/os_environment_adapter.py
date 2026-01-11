"""
OsEnvironmentAdapter - Environment Variable Access Adapter

Implements the IEnvironmentProvider port using os.environ.
"""

from __future__ import annotations

import os


class OsEnvironmentAdapter:
    """Adapter for accessing environment variables via os.environ.

    This adapter implements the IEnvironmentProvider protocol,
    providing a simple wrapper around os.environ with additional
    handling for empty values.
    """

    def get_env(self, name: str) -> str | None:
        """Get an environment variable value.

        Args:
            name: The environment variable name

        Returns:
            The value if set and non-empty, None otherwise
        """
        value = os.environ.get(name)
        if value is None or value.strip() == "":
            return None
        return value.strip()

    def get_env_or_default(self, name: str, default: str) -> str:
        """Get an environment variable value with a default.

        Args:
            name: The environment variable name
            default: Default value if not set or empty

        Returns:
            The value if set and non-empty, default otherwise
        """
        value = self.get_env(name)
        return value if value is not None else default
