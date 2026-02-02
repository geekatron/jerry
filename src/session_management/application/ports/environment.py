"""
IEnvironmentProvider - Port for Environment Access

This port abstracts environment variable access to enable
testing without modifying the actual environment.
"""

from __future__ import annotations

from typing import Protocol


class IEnvironmentProvider(Protocol):
    """Port for accessing environment variables.

    This port abstracts environment variable access to enable
    testing without modifying the actual environment.
    """

    def get_env(self, name: str) -> str | None:
        """Get an environment variable value.

        Args:
            name: The environment variable name

        Returns:
            The value if set, None if not set or empty
        """
        ...

    def get_env_or_default(self, name: str, default: str) -> str:
        """Get an environment variable value with a default.

        Args:
            name: The environment variable name
            default: Default value if not set

        Returns:
            The value if set, default otherwise
        """
        ...
