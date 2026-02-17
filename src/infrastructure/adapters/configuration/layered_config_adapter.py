# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
LayeredConfigAdapter - Layered Configuration with Precedence

Implements the IConfigurationProvider port with layered configuration sources.
Precedence order (highest to lowest):
1. Environment Variables (JERRY_*)
2. Project Config (projects/PROJ-*/.jerry/config.toml)
3. Root Config (.jerry/config.toml)
4. Code Defaults

Implementation Notes:
    - Uses stdlib tomllib for TOML parsing (Python 3.11+)
    - Delegates file I/O to AtomicFileAdapter for safe concurrent access
    - Environment variables override all file-based configuration
    - Nested keys use dot notation (e.g., logging.level)

References:
    - WI-014: Layered Config Adapter work item
    - PROJ-004-e-004: Configuration Precedence research
    - ADR-PROJ004-001: JerryFramework Aggregate (IConfigurationLoader port)
"""

from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any, Protocol

from src.infrastructure.adapters.configuration.env_config_adapter import (
    EnvConfigAdapter,
)
from src.infrastructure.adapters.persistence.atomic_file_adapter import (
    AtomicFileAdapter,
)


class IConfigurationProvider(Protocol):
    """Port interface for configuration access.

    This protocol defines the contract for configuration providers,
    allowing the application layer to access configuration without
    knowing the underlying implementation.
    """

    def get(self, key: str) -> Any | None:
        """Get a configuration value by key."""
        ...

    def get_string(self, key: str, default: str = "") -> str:
        """Get a configuration value as string."""
        ...

    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get a configuration value as boolean."""
        ...

    def get_int(self, key: str, default: int = 0) -> int:
        """Get a configuration value as integer."""
        ...

    def get_list(self, key: str, default: list[Any] | None = None) -> list[Any]:
        """Get a configuration value as list."""
        ...

    def has(self, key: str) -> bool:
        """Check if a configuration key exists."""
        ...


class LayeredConfigAdapter:
    """Adapter implementing layered configuration with precedence.

    Combines configuration from multiple sources with proper precedence:
    1. Environment variables (highest priority)
    2. Project configuration file
    3. Root configuration file
    4. Code defaults (lowest priority)

    Implements the IConfigurationProvider protocol.

    Attributes:
        env_adapter: Adapter for environment variable configuration
        root_config: Configuration from root .jerry/config.toml
        project_config: Configuration from project .jerry/config.toml
        defaults: Default configuration values

    Example:
        >>> adapter = LayeredConfigAdapter(
        ...     root_config_path=Path(".jerry/config.toml"),
        ...     defaults={"logging.level": "INFO"}
        ... )
        >>> adapter.get("logging.level")
        'INFO'
    """

    def __init__(
        self,
        env_prefix: str = "JERRY_",
        root_config_path: Path | None = None,
        project_config_path: Path | None = None,
        defaults: dict[str, Any] | None = None,
        file_adapter: AtomicFileAdapter | None = None,
    ) -> None:
        """Initialize the layered configuration adapter.

        Args:
            env_prefix: Prefix for environment variables (default: JERRY_)
            root_config_path: Path to root config.toml (optional)
            project_config_path: Path to project config.toml (optional)
            defaults: Default configuration values (optional)
            file_adapter: AtomicFileAdapter for file I/O (optional, creates new if not provided)
        """
        self._file_adapter = file_adapter or AtomicFileAdapter()
        self._env_adapter = EnvConfigAdapter(prefix=env_prefix)
        self._root_config = self._load_toml(root_config_path)
        self._project_config = self._load_toml(project_config_path)
        self._defaults = defaults or {}

        # Store paths for reload capability
        self._root_config_path = root_config_path
        self._project_config_path = project_config_path

    def _load_toml(self, path: Path | None) -> dict[str, Any]:
        """Load and parse a TOML configuration file.

        Uses AtomicFileAdapter for safe file access with locking.

        Args:
            path: Path to the TOML file, or None to skip

        Returns:
            Parsed configuration dict, or empty dict if file missing/invalid
        """
        if path is None:
            return {}

        if not self._file_adapter.exists(path):
            return {}

        try:
            content = self._file_adapter.read_with_lock(path)
            if not content.strip():
                return {}
            return tomllib.loads(content)
        except tomllib.TOMLDecodeError:
            # Log error but continue with empty config
            return {}

    def _get_nested(self, data: dict[str, Any], key: str) -> Any | None:
        """Get a value from a nested dict using dot notation.

        Args:
            data: The dictionary to search
            key: Key in dot notation (e.g., "logging.level")

        Returns:
            The value if found, None otherwise
        """
        parts = key.split(".")
        current: Any = data
        for part in parts:
            if not isinstance(current, dict) or part not in current:
                return None
            current = current[part]
        return current

    def _has_nested(self, data: dict[str, Any], key: str) -> bool:
        """Check if a nested key exists in a dict.

        Args:
            data: The dictionary to check
            key: Key in dot notation

        Returns:
            True if the key exists
        """
        return self._get_nested(data, key) is not None

    def get(self, key: str) -> Any | None:
        """Get a configuration value following precedence order.

        Checks sources in order:
        1. Environment variables
        2. Project config
        3. Root config
        4. Defaults

        Args:
            key: Configuration key in dot notation

        Returns:
            The configuration value, or None if not found in any source
        """
        # Priority 1: Environment variable
        if self._env_adapter.has(key):
            return self._env_adapter.get(key)

        # Priority 2: Project config
        value = self._get_nested(self._project_config, key)
        if value is not None:
            return value

        # Priority 3: Root config
        value = self._get_nested(self._root_config, key)
        if value is not None:
            return value

        # Priority 4: Defaults
        return self._defaults.get(key)

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

    def get_float(self, key: str, default: float = 0.0) -> float:
        """Get a configuration value as float.

        Args:
            key: Configuration key in dot notation
            default: Default value if not found

        Returns:
            The value as float, or the default
        """
        value = self.get(key)
        if value is None:
            return default
        try:
            return float(value)
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
        """Check if a configuration key exists in any source.

        Args:
            key: Configuration key in dot notation

        Returns:
            True if the key exists in any configuration source
        """
        return self.get(key) is not None

    def get_source(self, key: str) -> str | None:
        """Determine which source provides a configuration value.

        Useful for debugging and understanding configuration precedence.

        Args:
            key: Configuration key in dot notation

        Returns:
            Source name ("env", "project", "root", "default") or None
        """
        if self._env_adapter.has(key):
            return "env"
        if self._has_nested(self._project_config, key):
            return "project"
        if self._has_nested(self._root_config, key):
            return "root"
        if key in self._defaults:
            return "default"
        return None

    def reload(self) -> None:
        """Reload configuration from all sources.

        Call this method if configuration files may have changed
        since the adapter was initialized.
        """
        self._env_adapter.refresh()
        self._root_config = self._load_toml(self._root_config_path)
        self._project_config = self._load_toml(self._project_config_path)

    def all_keys(self) -> set[str]:
        """Get all configuration keys from all sources.

        Returns:
            Set of all configuration keys (dot notation)
        """
        keys: set[str] = set()

        # Add environment keys
        keys.update(self._env_adapter.keys())

        # Add project config keys
        keys.update(self._flatten_keys(self._project_config))

        # Add root config keys
        keys.update(self._flatten_keys(self._root_config))

        # Add default keys
        keys.update(self._defaults.keys())

        return keys

    def _flatten_keys(self, data: dict[str, Any], prefix: str = "") -> set[str]:
        """Flatten nested dict keys to dot notation.

        Args:
            data: Dictionary to flatten
            prefix: Key prefix for recursion

        Returns:
            Set of flattened keys
        """
        keys: set[str] = set()
        for key, value in data.items():
            full_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                keys.update(self._flatten_keys(value, full_key))
            else:
                keys.add(full_key)
        return keys
