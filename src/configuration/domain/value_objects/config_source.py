"""
ConfigSource - Enum for configuration source precedence levels.

Defines the 5-level configuration precedence model per ADR-PROJ004-004.
Sources with lower values have higher precedence.

References:
    - WI-009: Configuration Value Objects
    - ADR-PROJ004-004: JerrySession Context (5-level precedence)
    - PAT-VO-002: Enum Value Object pattern

Exports:
    ConfigSource: Enum for configuration source types
"""

from __future__ import annotations

from enum import IntEnum


class ConfigSource(IntEnum):
    """
    Configuration source levels with precedence ordering.

    Sources are ordered by precedence (lower value = higher precedence).
    This enables numeric comparison: if source1 < source2, source1 wins.

    Precedence Order (highest to lowest):
        1. ENV (1): Environment variables (JERRY_*)
        2. SESSION_LOCAL (2): .jerry/local/context.toml
        3. PROJECT (3): projects/PROJ-*/config.toml
        4. FRAMEWORK (4): .jerry/config.toml
        5. DEFAULT (5): Code defaults

    Attributes:
        ENV: Environment variables with JERRY_ prefix
        SESSION_LOCAL: Session-local overrides (gitignored)
        PROJECT: Project-specific configuration
        FRAMEWORK: Framework-wide defaults
        DEFAULT: Hardcoded defaults in code

    Examples:
        >>> ConfigSource.ENV < ConfigSource.PROJECT
        True
        >>> ConfigSource.ENV.has_priority_over(ConfigSource.PROJECT)
        True
        >>> sorted([ConfigSource.PROJECT, ConfigSource.ENV, ConfigSource.DEFAULT])
        [<ConfigSource.ENV: 1>, <ConfigSource.PROJECT: 3>, <ConfigSource.DEFAULT: 5>]
    """

    ENV = 1
    SESSION_LOCAL = 2
    PROJECT = 3
    FRAMEWORK = 4
    DEFAULT = 5

    @property
    def display_name(self) -> str:
        """
        Human-readable display name.

        Returns:
            Formatted display name

        Example:
            >>> ConfigSource.SESSION_LOCAL.display_name
            'Session Local'
        """
        return self.name.replace("_", " ").title()

    @property
    def description(self) -> str:
        """
        Get description of where this source loads from.

        Returns:
            Description of the configuration source location

        Example:
            >>> ConfigSource.ENV.description
            'Environment variables (JERRY_*)'
        """
        descriptions = {
            ConfigSource.ENV: "Environment variables (JERRY_*)",
            ConfigSource.SESSION_LOCAL: ".jerry/local/context.toml",
            ConfigSource.PROJECT: "projects/PROJ-*/config.toml",
            ConfigSource.FRAMEWORK: ".jerry/config.toml",
            ConfigSource.DEFAULT: "Code defaults",
        }
        return descriptions.get(self, "Unknown source")

    @property
    def is_file_based(self) -> bool:
        """
        Check if this source reads from a file.

        Returns:
            True if source is file-based (not ENV or DEFAULT)

        Example:
            >>> ConfigSource.PROJECT.is_file_based
            True
            >>> ConfigSource.ENV.is_file_based
            False
        """
        return self in (ConfigSource.SESSION_LOCAL, ConfigSource.PROJECT, ConfigSource.FRAMEWORK)

    @property
    def is_volatile(self) -> bool:
        """
        Check if this source can change during runtime.

        Returns:
            True for ENV (can change) and SESSION_LOCAL (can be edited)

        Example:
            >>> ConfigSource.ENV.is_volatile
            True
            >>> ConfigSource.DEFAULT.is_volatile
            False
        """
        return self in (ConfigSource.ENV, ConfigSource.SESSION_LOCAL)

    @property
    def precedence(self) -> int:
        """
        Get precedence level (1 = highest, 5 = lowest).

        Returns:
            Precedence value (same as enum value)

        Example:
            >>> ConfigSource.ENV.precedence
            1
        """
        return self.value

    def has_priority_over(self, other: ConfigSource) -> bool:
        """
        Check if this source has priority over another.

        Args:
            other: Source to compare against

        Returns:
            True if this source has higher priority (lower value)

        Example:
            >>> ConfigSource.ENV.has_priority_over(ConfigSource.PROJECT)
            True
            >>> ConfigSource.DEFAULT.has_priority_over(ConfigSource.FRAMEWORK)
            False
        """
        return self.value < other.value

    @classmethod
    def from_string(cls, value: str) -> ConfigSource:
        """
        Parse source from string (case-insensitive).

        Args:
            value: Source name string

        Returns:
            Matching ConfigSource

        Raises:
            ValueError: If value doesn't match a valid source

        Example:
            >>> ConfigSource.from_string("env")
            <ConfigSource.ENV: 1>
            >>> ConfigSource.from_string("PROJECT")
            <ConfigSource.PROJECT: 3>
        """
        normalized = value.strip().upper().replace("-", "_").replace(" ", "_")
        try:
            return cls[normalized]
        except KeyError:
            valid = ", ".join(s.name for s in cls)
            raise ValueError(
                f"Invalid configuration source: '{value}'. Valid sources: {valid}"
            )

    def __str__(self) -> str:
        """Return lowercase name for display."""
        return self.name.lower()

    def __repr__(self) -> str:
        """Return detailed representation for debugging."""
        return f"ConfigSource.{self.name}"
