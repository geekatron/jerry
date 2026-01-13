"""
ConfigValue - Resolved configuration value with provenance and type coercion.

Wraps a configuration value with its source information and provides
type-safe accessors for common types.

References:
    - WI-009: Configuration Value Objects
    - AC-009.4: ConfigValue supports type coercion (str → bool/int/list)
    - ADR-PROJ004-004: JerrySession Context (ConfigValue pattern)
    - PAT-VO-001: Immutable Value Object pattern

Exports:
    ConfigValue: Immutable configuration value with type coercion
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.configuration.domain.value_objects.config_source import ConfigSource


@dataclass(frozen=True, slots=True)
class ConfigValue:
    """
    Resolved configuration value with provenance and type coercion.

    Encapsulates a configuration value along with metadata about its
    source (where it came from) and the key it was resolved from.

    Attributes:
        key: The configuration key that was resolved
        value: The raw value (can be any type)
        source: Where the value came from (ENV, PROJECT, etc.)

    Invariants:
        - Key cannot be empty
        - Source must be a valid ConfigSource

    Examples:
        >>> cv = ConfigValue(key="logging.level", value="DEBUG", source=ConfigSource.ENV)
        >>> cv.as_string()
        'DEBUG'
        >>> cv.as_bool(default=False)
        False
        >>> cv = ConfigValue(key="debug", value="true", source=ConfigSource.ENV)
        >>> cv.as_bool()
        True

    Type Coercion:
        - as_string(): Returns str(value) or default
        - as_bool(): Interprets "true", "1", "yes" as True
        - as_int(): Attempts int() conversion
        - as_float(): Attempts float() conversion
        - as_list(): Splits comma-separated string or returns list
    """

    key: str
    value: Any
    source: ConfigSource

    def __post_init__(self) -> None:
        """Validate value after initialization."""
        if not self.key:
            raise ValueError("ConfigValue key cannot be empty")

    @property
    def is_none(self) -> bool:
        """
        Check if the value is None.

        Returns:
            True if value is None
        """
        return self.value is None

    @property
    def is_empty(self) -> bool:
        """
        Check if the value is None or empty string.

        Returns:
            True if value is None or empty string
        """
        return self.value is None or self.value == ""

    @property
    def raw(self) -> Any:
        """
        Get the raw value without conversion.

        Returns:
            The raw value as-is
        """
        return self.value

    def as_string(self, default: str = "") -> str:
        """
        Get value as string.

        Args:
            default: Default value if None

        Returns:
            String representation of value

        Examples:
            >>> ConfigValue("k", "hello", ConfigSource.ENV).as_string()
            'hello'
            >>> ConfigValue("k", 42, ConfigSource.ENV).as_string()
            '42'
            >>> ConfigValue("k", None, ConfigSource.ENV).as_string("default")
            'default'
        """
        if self.value is None:
            return default
        return str(self.value)

    def as_bool(self, default: bool = False) -> bool:
        """
        Get value as boolean.

        Interprets the following as True (case-insensitive):
        - Boolean True
        - String: "true", "1", "yes", "on"
        - Integer: Non-zero values

        Args:
            default: Default value if None or not convertible

        Returns:
            Boolean value

        Examples:
            >>> ConfigValue("k", "true", ConfigSource.ENV).as_bool()
            True
            >>> ConfigValue("k", "YES", ConfigSource.ENV).as_bool()
            True
            >>> ConfigValue("k", "1", ConfigSource.ENV).as_bool()
            True
            >>> ConfigValue("k", "false", ConfigSource.ENV).as_bool()
            False
            >>> ConfigValue("k", "no", ConfigSource.ENV).as_bool()
            False
        """
        if self.value is None:
            return default

        if isinstance(self.value, bool):
            return self.value

        if isinstance(self.value, int):
            return self.value != 0

        if isinstance(self.value, str):
            return self.value.lower().strip() in ("true", "1", "yes", "on")

        return default

    def as_int(self, default: int = 0) -> int:
        """
        Get value as integer.

        Args:
            default: Default value if None or not convertible

        Returns:
            Integer value

        Examples:
            >>> ConfigValue("k", "42", ConfigSource.ENV).as_int()
            42
            >>> ConfigValue("k", 42, ConfigSource.ENV).as_int()
            42
            >>> ConfigValue("k", "invalid", ConfigSource.ENV).as_int(99)
            99
        """
        if self.value is None:
            return default

        if isinstance(self.value, int) and not isinstance(self.value, bool):
            return self.value

        try:
            return int(self.value)
        except (TypeError, ValueError):
            return default

    def as_float(self, default: float = 0.0) -> float:
        """
        Get value as float.

        Args:
            default: Default value if None or not convertible

        Returns:
            Float value

        Examples:
            >>> ConfigValue("k", "3.14", ConfigSource.ENV).as_float()
            3.14
            >>> ConfigValue("k", 3.14, ConfigSource.ENV).as_float()
            3.14
        """
        if self.value is None:
            return default

        if isinstance(self.value, (int, float)) and not isinstance(self.value, bool):
            return float(self.value)

        try:
            return float(self.value)
        except (TypeError, ValueError):
            return default

    def as_list(self, separator: str = ",", default: list[str] | None = None) -> list[str]:
        """
        Get value as list of strings.

        If value is already a list, returns it as strings.
        If value is a string, splits by separator.

        Args:
            separator: Separator for splitting strings (default: comma)
            default: Default value if None

        Returns:
            List of strings

        Examples:
            >>> ConfigValue("k", "a,b,c", ConfigSource.ENV).as_list()
            ['a', 'b', 'c']
            >>> ConfigValue("k", ["a", "b"], ConfigSource.ENV).as_list()
            ['a', 'b']
            >>> ConfigValue("k", "single", ConfigSource.ENV).as_list()
            ['single']
        """
        if default is None:
            default = []

        if self.value is None:
            return default

        if isinstance(self.value, list):
            return [str(item) for item in self.value]

        if isinstance(self.value, str):
            if not self.value.strip():
                return default
            return [item.strip() for item in self.value.split(separator) if item.strip()]

        # Single value that's not a list or string
        return [str(self.value)]

    def as_dict(self, default: dict[str, Any] | None = None) -> dict[str, Any]:
        """
        Get value as dictionary.

        Args:
            default: Default value if None or not a dict

        Returns:
            Dictionary value

        Note:
            Only returns the value if it's already a dict.
            Does not attempt to parse strings as dictionaries.
        """
        if default is None:
            default = {}

        if self.value is None:
            return default

        if isinstance(self.value, dict):
            return dict(self.value)

        return default

    def or_default(self, default: Any) -> ConfigValue:
        """
        Return a new ConfigValue with default if current value is None.

        Args:
            default: Default value to use

        Returns:
            Self if value is not None, otherwise new ConfigValue with default

        Example:
            >>> cv = ConfigValue("k", None, ConfigSource.ENV)
            >>> cv.or_default("fallback").as_string()
            'fallback'
        """
        if self.value is not None:
            return self
        return ConfigValue(key=self.key, value=default, source=ConfigSource.DEFAULT)

    @classmethod
    def of(cls, key: str, value: Any, source: ConfigSource = ConfigSource.DEFAULT) -> ConfigValue:
        """
        Factory method for creating ConfigValue.

        Args:
            key: Configuration key
            value: Configuration value
            source: Configuration source

        Returns:
            New ConfigValue

        Example:
            >>> ConfigValue.of("debug", True, ConfigSource.ENV)
            ConfigValue(key='debug', value=True, source=<ConfigSource.ENV: 1>)
        """
        return cls(key=key, value=value, source=source)

    @classmethod
    def empty(cls, key: str, source: ConfigSource = ConfigSource.DEFAULT) -> ConfigValue:
        """
        Create a ConfigValue with None value.

        Args:
            key: Configuration key
            source: Configuration source

        Returns:
            ConfigValue with None value

        Example:
            >>> ConfigValue.empty("missing").is_none
            True
        """
        return cls(key=key, value=None, source=source)

    def __str__(self) -> str:
        """Return string representation for display."""
        return f"{self.key}={self.value} (from {self.source.name.lower()})"

    def __repr__(self) -> str:
        """Return detailed representation for debugging."""
        return f"ConfigValue(key={self.key!r}, value={self.value!r}, source={self.source!r})"

    def __bool__(self) -> bool:
        """
        Truth value based on value being non-None and non-empty.

        Returns:
            True if value is not None and not empty string
        """
        return not self.is_empty
