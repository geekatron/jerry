# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
EnvConfigAdapter - Environment Variable Configuration Adapter

Reads configuration from environment variables with automatic type conversion
and key mapping (e.g., JERRY_LOGGING__LEVEL -> logging.level).

Implementation Notes:
    - Prefix filtering: Only reads variables starting with JERRY_ (configurable)
    - Key mapping: Uses __ as separator for nested keys
    - Type coercion: Automatically converts to bool, int, float, list, dict
    - Caching: Loads environment on initialization for consistent reads

References:
    - WI-013: Environment Variable Adapter work item
    - PROJ-004-e-004: Configuration Precedence research
    - 12-Factor App: https://12factor.net/config
"""

from __future__ import annotations

import json
import os
from typing import Any


class EnvConfigAdapter:
    """Adapter for reading configuration from environment variables.

    Scans environment variables with a configured prefix and provides
    access to them as configuration values with automatic type conversion.

    Attributes:
        prefix: The environment variable prefix (default: JERRY_)

    Example:
        >>> # With JERRY_LOGGING__LEVEL=DEBUG set in environment
        >>> adapter = EnvConfigAdapter()
        >>> adapter.get("logging.level")
        'DEBUG'
        >>> adapter.has("logging.level")
        True
    """

    def __init__(self, prefix: str = "JERRY_") -> None:
        """Initialize the adapter with environment variable prefix.

        Args:
            prefix: Prefix for environment variables to scan (default: JERRY_)
        """
        self._prefix = prefix
        self._cache: dict[str, Any] = {}
        self._load_from_env()

    @property
    def prefix(self) -> str:
        """Get the environment variable prefix."""
        return self._prefix

    def _load_from_env(self) -> None:
        """Scan environment for prefixed variables and cache them."""
        for key, value in os.environ.items():
            if key.startswith(self._prefix):
                config_key = self._env_to_config_key(key)
                self._cache[config_key] = self._parse_value(value)

    def _env_to_config_key(self, env_key: str) -> str:
        """Convert environment variable name to config key.

        Removes the prefix and converts __ to dot notation.
        Example: JERRY_LOGGING__LEVEL -> logging.level

        Args:
            env_key: Environment variable name

        Returns:
            Configuration key in dot notation
        """
        key = env_key[len(self._prefix) :]
        return key.lower().replace("__", ".")

    def _config_to_env_key(self, config_key: str) -> str:
        """Convert config key to environment variable name.

        Adds the prefix and converts dots to __.
        Example: logging.level -> JERRY_LOGGING__LEVEL

        Args:
            config_key: Configuration key in dot notation

        Returns:
            Environment variable name
        """
        return self._prefix + config_key.upper().replace(".", "__")

    def _parse_value(self, value: str) -> Any:
        """Parse string value to appropriate Python type.

        Type conversion order:
        1. Boolean (true/false, yes/no, on/off, 1/0)
        2. Integer
        3. Float
        4. JSON array or object
        5. Comma-separated list
        6. String (default)

        Args:
            value: String value from environment

        Returns:
            Parsed value with appropriate type
        """
        # Handle empty string
        if not value:
            return ""

        # Boolean detection
        value_lower = value.lower()
        if value_lower in ("true", "yes", "on", "1"):
            return True
        if value_lower in ("false", "no", "off", "0"):
            return False

        # Integer detection
        try:
            return int(value)
        except ValueError:
            pass

        # Float detection
        try:
            return float(value)
        except ValueError:
            pass

        # JSON array or object
        if value.startswith("[") or value.startswith("{"):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                pass

        # Comma-separated list (only if not quoted)
        if "," in value and not value.startswith('"') and not value.startswith("'"):
            return [v.strip() for v in value.split(",")]

        return value

    def get(self, key: str) -> Any | None:
        """Get a configuration value by key.

        Args:
            key: Configuration key in dot notation

        Returns:
            The configuration value, or None if not found
        """
        return self._cache.get(key)

    def get_string(self, key: str, default: str = "") -> str:
        """Get a configuration value as string.

        Args:
            key: Configuration key in dot notation
            default: Default value if not found

        Returns:
            The value as string, or the default
        """
        value = self.get(key)
        if value is None:
            return default
        return str(value)

    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get a configuration value as boolean.

        Args:
            key: Configuration key in dot notation
            default: Default value if not found

        Returns:
            The value as boolean, or the default
        """
        value = self.get(key)
        if value is None:
            return default
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ("true", "yes", "on", "1")
        return bool(value)

    def get_int(self, key: str, default: int = 0) -> int:
        """Get a configuration value as integer.

        Args:
            key: Configuration key in dot notation
            default: Default value if not found

        Returns:
            The value as integer, or the default
        """
        value = self.get(key)
        if value is None:
            return default
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    def get_list(self, key: str, default: list[Any] | None = None) -> list[Any]:
        """Get a configuration value as list.

        Args:
            key: Configuration key in dot notation
            default: Default value if not found

        Returns:
            The value as list, or the default
        """
        value = self.get(key)
        if value is None:
            return default if default is not None else []
        if isinstance(value, list):
            return value
        return [value]

    def has(self, key: str) -> bool:
        """Check if a configuration key exists.

        Args:
            key: Configuration key in dot notation

        Returns:
            True if the key exists in the environment configuration
        """
        return key in self._cache

    def refresh(self) -> None:
        """Reload configuration from environment.

        Call this method if environment variables may have changed
        since the adapter was initialized.
        """
        self._cache.clear()
        self._load_from_env()

    def keys(self) -> list[str]:
        """Get all configuration keys.

        Returns:
            List of all configuration keys found in environment
        """
        return list(self._cache.keys())
