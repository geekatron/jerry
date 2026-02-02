"""
ConfigKey - Immutable configuration key with dot-notation support.

Configuration keys use dot-notation (e.g., "logging.level") and can be
converted to/from environment variable format (e.g., "JERRY_LOGGING__LEVEL").

References:
    - WI-009: Configuration Value Objects
    - AC-009.1: ConfigKey with dot-notation support
    - AC-009.2: ConfigKey.to_env_key() conversion
    - PAT-VO-001: Immutable Value Object pattern

Exports:
    ConfigKey: Immutable configuration key value object
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from re import Pattern
from typing import ClassVar

from src.shared_kernel.exceptions import ValidationError


@dataclass(frozen=True, slots=True)
class ConfigKey:
    """
    Immutable configuration key with dot-notation support.

    Configuration keys support hierarchical namespacing using dots.
    Keys can be converted to/from environment variable format.

    Attributes:
        value: The key string in dot-notation (e.g., "logging.level")

    Invariants:
        - Key cannot be empty
        - Key must match pattern: word(.word)* where word is alphanumeric with underscores
        - Consecutive dots are not allowed
        - Leading/trailing dots are not allowed

    Examples:
        >>> key = ConfigKey("logging.level")
        >>> key.to_env_key()
        'JERRY_LOGGING__LEVEL'
        >>> ConfigKey.from_env_key("JERRY_LOGGING__LEVEL")
        ConfigKey(value='logging.level')
        >>> key.parts
        ('logging', 'level')
        >>> key.namespace
        'logging'

    Conversion Rules:
        - Dot (.) in key → Double underscore (__) in env var
        - Lowercase in key → UPPERCASE in env var
        - JERRY_ prefix is added/stripped automatically
    """

    value: str

    # Pattern for valid key segments: alphanumeric with underscores, hyphens allowed
    _SEGMENT_PATTERN: ClassVar[Pattern[str]] = re.compile(r"^[a-zA-Z][a-zA-Z0-9_-]*$")

    # Full key pattern: segments separated by dots
    _KEY_PATTERN: ClassVar[Pattern[str]] = re.compile(
        r"^[a-zA-Z][a-zA-Z0-9_-]*(\.[a-zA-Z][a-zA-Z0-9_-]*)*$"
    )

    # Default environment variable prefix
    _DEFAULT_PREFIX: ClassVar[str] = "JERRY_"

    def __post_init__(self) -> None:
        """Validate key format after initialization."""
        if not self.value:
            raise ValidationError(
                field="key",
                message="Configuration key cannot be empty",
            )

        # Strip whitespace
        stripped = self.value.strip()
        if stripped != self.value:
            # If whitespace was present, create new instance with stripped value
            # But since frozen, we need to validate the input
            raise ValidationError(
                field="key",
                message="Configuration key cannot have leading or trailing whitespace",
            )

        if not self._KEY_PATTERN.match(self.value):
            raise ValidationError(
                field="key",
                message=(
                    f"Invalid configuration key format: '{self.value}'. "
                    "Keys must be alphanumeric segments separated by dots "
                    "(e.g., 'logging.level', 'database.connection_string')"
                ),
            )

    @property
    def parts(self) -> tuple[str, ...]:
        """
        Split key into individual segments.

        Returns:
            Tuple of key segments

        Example:
            >>> ConfigKey("logging.level").parts
            ('logging', 'level')
        """
        return tuple(self.value.split("."))

    @property
    def namespace(self) -> str | None:
        """
        Get the namespace (parent key path).

        Returns:
            Namespace string, or None if this is a root-level key

        Example:
            >>> ConfigKey("logging.level").namespace
            'logging'
            >>> ConfigKey("debug").namespace is None
            True
        """
        parts = self.parts
        if len(parts) <= 1:
            return None
        return ".".join(parts[:-1])

    @property
    def leaf(self) -> str:
        """
        Get the leaf segment (final part of the key).

        Returns:
            The last segment of the key

        Example:
            >>> ConfigKey("logging.level").leaf
            'level'
        """
        return self.parts[-1]

    @property
    def depth(self) -> int:
        """
        Get the nesting depth of the key.

        Returns:
            Number of segments in the key

        Example:
            >>> ConfigKey("logging.level").depth
            2
            >>> ConfigKey("debug").depth
            1
        """
        return len(self.parts)

    def to_env_key(self, prefix: str | None = None) -> str:
        """
        Convert to environment variable name.

        Args:
            prefix: Environment variable prefix (default: "JERRY_")

        Returns:
            Environment variable name in UPPERCASE format

        Example:
            >>> ConfigKey("logging.level").to_env_key()
            'JERRY_LOGGING__LEVEL'
            >>> ConfigKey("database.host").to_env_key(prefix="APP_")
            'APP_DATABASE__HOST'
        """
        if prefix is None:
            prefix = self._DEFAULT_PREFIX
        env_name = self.value.upper().replace(".", "__").replace("-", "_")
        return f"{prefix}{env_name}"

    @classmethod
    def from_env_key(cls, env_key: str, prefix: str | None = None) -> ConfigKey:
        """
        Create ConfigKey from environment variable name.

        Args:
            env_key: Environment variable name
            prefix: Expected prefix (default: "JERRY_")

        Returns:
            ConfigKey parsed from environment variable name

        Raises:
            ValidationError: If env_key doesn't have expected prefix

        Example:
            >>> ConfigKey.from_env_key("JERRY_LOGGING__LEVEL")
            ConfigKey(value='logging.level')
        """
        if prefix is None:
            prefix = cls._DEFAULT_PREFIX

        if not env_key.startswith(prefix):
            raise ValidationError(
                field="env_key",
                message=f"Environment variable must start with '{prefix}': {env_key}",
            )

        # Remove prefix and convert format
        key_part = env_key[len(prefix) :]
        # Single underscores in env vars become hyphens in keys
        # Double underscores become dots
        key = key_part.lower().replace("__", ".").replace("_", "-")
        return cls(key)

    def child(self, segment: str) -> ConfigKey:
        """
        Create a child key by appending a segment.

        Args:
            segment: Segment to append

        Returns:
            New ConfigKey with appended segment

        Example:
            >>> ConfigKey("logging").child("level")
            ConfigKey(value='logging.level')
        """
        return ConfigKey(f"{self.value}.{segment}")

    def parent(self) -> ConfigKey | None:
        """
        Get the parent key.

        Returns:
            Parent ConfigKey, or None if this is a root-level key

        Example:
            >>> ConfigKey("logging.level").parent()
            ConfigKey(value='logging')
        """
        namespace = self.namespace
        return ConfigKey(namespace) if namespace else None

    def starts_with(self, prefix: ConfigKey | str) -> bool:
        """
        Check if this key starts with a prefix.

        Args:
            prefix: Prefix to check (ConfigKey or string)

        Returns:
            True if this key starts with the prefix

        Example:
            >>> ConfigKey("logging.level").starts_with("logging")
            True
            >>> ConfigKey("logging.level").starts_with("log")
            False
        """
        prefix_str = prefix.value if isinstance(prefix, ConfigKey) else prefix
        # Must match at segment boundary
        if self.value == prefix_str:
            return True
        return self.value.startswith(f"{prefix_str}.")

    def relative_to(self, prefix: ConfigKey | str) -> ConfigKey | None:
        """
        Get the key relative to a prefix.

        Args:
            prefix: Prefix to remove

        Returns:
            New ConfigKey without the prefix, or None if not a child

        Example:
            >>> ConfigKey("logging.level").relative_to("logging")
            ConfigKey(value='level')
        """
        prefix_str = prefix.value if isinstance(prefix, ConfigKey) else prefix
        if not self.starts_with(prefix_str):
            return None
        if self.value == prefix_str:
            return None
        relative = self.value[len(prefix_str) + 1 :]  # +1 for the dot
        return ConfigKey(relative) if relative else None

    def __str__(self) -> str:
        """Return the key value for display."""
        return self.value

    def __repr__(self) -> str:
        """Return detailed representation for debugging."""
        return f"ConfigKey(value={self.value!r})"
