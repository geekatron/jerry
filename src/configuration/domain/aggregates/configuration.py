"""
Configuration Aggregate - Core domain aggregate for configuration management.

The Configuration aggregate is the primary entry point for configuration handling.
It encapsulates configuration state and enforces business invariants.

Lifecycle:
    1. Create via Configuration.create() factory method
    2. Query via get/get_* accessor methods
    3. Mutate via set() method (emits ConfigurationValueChanged)
    4. Persist via repository (collect_events)
    5. Reconstitute via Configuration.load_from_history()

References:
    - WI-010: Configuration Aggregate
    - ADR-PROJ004-001: JerryFramework Aggregate (FrameworkConfig pattern)
    - ADR-PROJ004-004: JerrySession Context (ConfigResolver pattern)
    - PAT-AGG-001: Aggregate Root pattern

Exports:
    Configuration: Event-sourced configuration aggregate
"""

from __future__ import annotations

import uuid
from collections.abc import Sequence
from datetime import datetime
from typing import Any

from src.configuration.domain.events.configuration_events import (
    ConfigurationError,
    ConfigurationLoaded,
    ConfigurationValueChanged,
)
from src.configuration.domain.value_objects import ConfigKey, ConfigSource, ConfigValue
from src.shared_kernel.domain_event import DomainEvent


class Configuration:
    """
    Event-sourced aggregate for configuration management.

    Configuration is the primary aggregate in the configuration domain.
    It manages hierarchical key-value configuration with support for
    nested keys, type coercion, and change tracking.

    State Management:
        All state changes emit domain events. State is modified only via
        the _apply() method when processing events, ensuring deterministic
        replay from event history.

    Business Rules:
        - Keys are validated using ConfigKey format
        - Empty keys are not allowed
        - Value changes emit ConfigurationValueChanged events
        - Loading emits ConfigurationLoaded events

    Attributes:
        id: Unique identifier for this configuration instance
        version: Current version (increments with each event)
        source: Primary source this configuration was loaded from
        data: The underlying configuration dictionary

    Examples:
        >>> config = Configuration.create(
        ...     data={"logging": {"level": "DEBUG"}},
        ...     source="project",
        ... )
        >>> config.get("logging.level")
        'DEBUG'
        >>> config.get_string("logging.level", default="INFO")
        'DEBUG'
        >>> config.set("logging.level", "INFO")
        >>> events = config.collect_events()
    """

    _aggregate_type: str = "Configuration"

    def __init__(self) -> None:
        """Private constructor. Use Configuration.create() or load_from_history()."""
        self._id: str = ""
        self._version: int = 0
        self._data: dict[str, Any] = {}
        self._source: str = "unknown"
        self._pending_events: list[DomainEvent] = []
        self._created_at: datetime | None = None
        self._modified_at: datetime | None = None

    # =========================================================================
    # Factory Methods
    # =========================================================================

    @classmethod
    def create(
        cls,
        data: dict[str, Any] | None = None,
        source: str = "unknown",
        source_path: str | None = None,
        config_id: str | None = None,
    ) -> Configuration:
        """
        Create a new Configuration aggregate.

        Factory method that creates a new Configuration by raising
        a ConfigurationLoaded event.

        Args:
            data: Initial configuration dictionary (default: empty)
            source: Source type (env, project, framework, etc.)
            source_path: Optional file path for file-based sources
            config_id: Optional ID (auto-generated if not provided)

        Returns:
            New Configuration aggregate with LOADED state

        Examples:
            >>> config = Configuration.create(
            ...     data={"debug": True, "logging": {"level": "DEBUG"}},
            ...     source="project",
            ...     source_path="/path/to/config.toml",
            ... )
            >>> config.get("debug")
            True
        """
        config = cls()
        config._id = config_id or f"CONFIG-{uuid.uuid4().hex[:8]}"
        config._data = data if data is not None else {}
        config._source = source

        # Count keys for the event
        keys_loaded = cls._count_keys(config._data)

        # Raise creation event
        event = ConfigurationLoaded.create(
            aggregate_id=config._id,
            source=source,
            keys_loaded=keys_loaded,
            source_path=source_path,
            version=1,
        )
        config._raise_event(event)

        return config

    @classmethod
    def empty(cls, config_id: str | None = None) -> Configuration:
        """
        Create an empty Configuration.

        Convenience factory for creating a configuration with no data.

        Args:
            config_id: Optional ID (auto-generated if not provided)

        Returns:
            Empty Configuration aggregate
        """
        return cls.create(data={}, source="default", config_id=config_id)

    # =========================================================================
    # Properties
    # =========================================================================

    @property
    def id(self) -> str:
        """Unique identifier for this configuration."""
        return self._id

    @property
    def version(self) -> int:
        """Current version of the configuration."""
        return self._version

    @property
    def source(self) -> str:
        """Primary source this configuration was loaded from."""
        return self._source

    @property
    def data(self) -> dict[str, Any]:
        """The underlying configuration dictionary (read-only view)."""
        return dict(self._data)

    @property
    def created_at(self) -> datetime | None:
        """When this configuration was created."""
        return self._created_at

    @property
    def modified_at(self) -> datetime | None:
        """When this configuration was last modified."""
        return self._modified_at

    @property
    def keys(self) -> list[str]:
        """List of all configuration keys (flattened dot-notation)."""
        return list(self._flatten_keys(self._data))

    # =========================================================================
    # Query Methods
    # =========================================================================

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value by dot-notation key.

        Supports nested key access using dots as separators.

        Args:
            key: Configuration key (e.g., "logging.level")
            default: Default value if key not found

        Returns:
            Configuration value or default

        Examples:
            >>> config.get("logging.level")
            'DEBUG'
            >>> config.get("missing.key", "default")
            'default'
        """
        parts = key.split(".")
        current = self._data

        for part in parts:
            if not isinstance(current, dict):
                return default
            if part not in current:
                return default
            current = current[part]

        return current

    def get_value(self, key: str) -> ConfigValue:
        """
        Get a configuration value with full provenance.

        Returns a ConfigValue wrapper with source information
        and type coercion methods.

        Args:
            key: Configuration key

        Returns:
            ConfigValue with value and source

        Examples:
            >>> cv = config.get_value("logging.level")
            >>> cv.as_string()
            'DEBUG'
            >>> cv.source
            <ConfigSource.PROJECT: 3>
        """
        value = self.get(key)
        source = ConfigSource.from_string(self._source)
        return ConfigValue(key=key, value=value, source=source)

    def get_string(self, key: str, default: str = "") -> str:
        """
        Get a configuration value as string.

        Args:
            key: Configuration key
            default: Default value if not found

        Returns:
            String value

        Examples:
            >>> config.get_string("logging.level", "INFO")
            'DEBUG'
        """
        return self.get_value(key).as_string(default)

    def get_bool(self, key: str, default: bool = False) -> bool:
        """
        Get a configuration value as boolean.

        Interprets "true", "1", "yes", "on" as True (case-insensitive).

        Args:
            key: Configuration key
            default: Default value if not found

        Returns:
            Boolean value

        Examples:
            >>> config.get_bool("debug", False)
            True
        """
        return self.get_value(key).as_bool(default)

    def get_int(self, key: str, default: int = 0) -> int:
        """
        Get a configuration value as integer.

        Args:
            key: Configuration key
            default: Default value if not found or not convertible

        Returns:
            Integer value

        Examples:
            >>> config.get_int("max_retries", 3)
            5
        """
        return self.get_value(key).as_int(default)

    def get_float(self, key: str, default: float = 0.0) -> float:
        """
        Get a configuration value as float.

        Args:
            key: Configuration key
            default: Default value if not found or not convertible

        Returns:
            Float value
        """
        return self.get_value(key).as_float(default)

    def get_list(self, key: str, default: list[str] | None = None) -> list[str]:
        """
        Get a configuration value as list.

        If the value is a string, splits by comma.
        If already a list, returns as strings.

        Args:
            key: Configuration key
            default: Default value if not found

        Returns:
            List of strings

        Examples:
            >>> config.get_list("allowed_hosts", [])
            ['localhost', '127.0.0.1']
        """
        return self.get_value(key).as_list(default=default)

    def has(self, key: str) -> bool:
        """
        Check if a configuration key exists.

        Args:
            key: Configuration key

        Returns:
            True if key exists

        Examples:
            >>> config.has("logging.level")
            True
        """
        return self.get(key) is not None

    def get_namespace(self, prefix: str) -> dict[str, Any]:
        """
        Get all values under a namespace prefix.

        Args:
            prefix: Key prefix (e.g., "logging")

        Returns:
            Dictionary of values under the prefix

        Examples:
            >>> config.get_namespace("logging")
            {'level': 'DEBUG', 'format': 'json'}
        """
        value = self.get(prefix)
        if isinstance(value, dict):
            return dict(value)
        return {}

    # =========================================================================
    # Command Methods
    # =========================================================================

    def set(self, key: str, value: Any, reason: str | None = None) -> None:
        """
        Set a configuration value.

        Emits a ConfigurationValueChanged event.

        Args:
            key: Configuration key (dot-notation)
            value: New value
            reason: Optional reason for the change

        Raises:
            ValidationError: If key is invalid

        Examples:
            >>> config.set("logging.level", "INFO")
            >>> config.set("debug", True, reason="Enabling debug mode")
        """
        # Validate key (raises ValidationError if invalid)
        ConfigKey(key)

        # Get old value
        old_value = self.get(key)

        # Skip if no change
        if old_value == value:
            return

        # Set the value
        self._set_nested(key, value)

        # Raise event
        event = ConfigurationValueChanged.create(
            aggregate_id=self._id,
            key=key,
            old_value=old_value,
            new_value=value,
            source=self._source,
            reason=reason,
            version=self._version + 1,
        )
        self._raise_event(event)

    def merge(self, other: dict[str, Any], source: str = "merge") -> None:
        """
        Merge another configuration dictionary.

        Values from 'other' override existing values.
        Emits events for each changed key.

        Args:
            other: Dictionary to merge
            source: Source label for the merged values
        """
        for key in self._flatten_keys(other):
            new_value = self._get_from_dict(other, key)
            old_value = self.get(key)
            if new_value != old_value:
                self._set_nested(key, new_value)
                event = ConfigurationValueChanged.create(
                    aggregate_id=self._id,
                    key=key,
                    old_value=old_value,
                    new_value=new_value,
                    source=source,
                    version=self._version + 1,
                )
                self._raise_event(event)

    # =========================================================================
    # Event Infrastructure
    # =========================================================================

    def _raise_event(self, event: DomainEvent) -> None:
        """
        Record a new domain event.

        Updates version, applies event, and adds to pending list.
        """
        self._version += 1
        self._apply(event)
        self._pending_events.append(event)
        self._modified_at = event.timestamp

        if self._created_at is None:
            self._created_at = event.timestamp

    def _apply(self, event: DomainEvent) -> None:
        """
        Apply an event to update aggregate state.

        This method is called during event raising and history replay.
        Must be deterministic and side-effect free.
        """
        if isinstance(event, ConfigurationLoaded):
            self._source = event.source

        elif isinstance(event, ConfigurationValueChanged):
            if event.new_value is not None:
                self._set_nested(event.key, event.new_value)
            else:
                self._remove_key(event.key)

        elif isinstance(event, ConfigurationError):
            # Errors are informational - don't modify state
            pass

    def collect_events(self) -> Sequence[DomainEvent]:
        """
        Return and clear pending events.

        Returns:
            List of events raised since last collection
        """
        events = list(self._pending_events)
        self._pending_events.clear()
        return events

    def has_pending_events(self) -> bool:
        """Check if there are uncommitted events."""
        return len(self._pending_events) > 0

    # =========================================================================
    # History Replay
    # =========================================================================

    @classmethod
    def load_from_history(
        cls,
        events: Sequence[DomainEvent],
        initial_data: dict[str, Any] | None = None,
    ) -> Configuration:
        """
        Reconstruct Configuration by replaying events.

        Args:
            events: Historical events in version order
            initial_data: Optional initial data before events

        Returns:
            Configuration with state rebuilt from events

        Raises:
            ValueError: If events sequence is empty
        """
        if not events:
            raise ValueError("Cannot load from empty event history")

        config = cls()
        config._id = events[0].aggregate_id
        config._data = initial_data if initial_data is not None else {}
        config._version = 0
        config._created_at = events[0].timestamp

        for event in events:
            config._version = event.version
            config._apply(event)
            config._modified_at = event.timestamp

        return config

    # =========================================================================
    # Private Helpers
    # =========================================================================

    def _set_nested(self, key: str, value: Any) -> None:
        """Set a value at a nested key path."""
        parts = key.split(".")
        current = self._data

        for part in parts[:-1]:
            if part not in current or not isinstance(current[part], dict):
                current[part] = {}
            current = current[part]

        current[parts[-1]] = value

    def _remove_key(self, key: str) -> None:
        """Remove a key from the configuration."""
        parts = key.split(".")
        current = self._data

        for part in parts[:-1]:
            if part not in current or not isinstance(current[part], dict):
                return
            current = current[part]

        if parts[-1] in current:
            del current[parts[-1]]

    @staticmethod
    def _count_keys(data: dict[str, Any], prefix: str = "") -> int:
        """Count total number of leaf keys in nested dictionary."""
        count = 0
        for key, value in data.items():
            if isinstance(value, dict):
                count += Configuration._count_keys(value, f"{prefix}{key}.")
            else:
                count += 1
        return count

    @staticmethod
    def _flatten_keys(data: dict[str, Any], prefix: str = "") -> list[str]:
        """Flatten nested dictionary to list of dot-notation keys."""
        keys = []
        for key, value in data.items():
            full_key = f"{prefix}{key}" if prefix else key
            if isinstance(value, dict):
                keys.extend(Configuration._flatten_keys(value, f"{full_key}."))
            else:
                keys.append(full_key)
        return keys

    @staticmethod
    def _get_from_dict(data: dict[str, Any], key: str) -> Any:
        """Get value from nested dictionary using dot-notation key."""
        parts = key.split(".")
        current = data

        for part in parts:
            if not isinstance(current, dict) or part not in current:
                return None
            current = current[part]

        return current

    # =========================================================================
    # String Representation
    # =========================================================================

    def __str__(self) -> str:
        """Return summary for display."""
        return f"Configuration(id={self._id}, keys={len(self.keys)}, source={self._source})"

    def __repr__(self) -> str:
        """Return detailed representation for debugging."""
        return (
            f"Configuration("
            f"id={self._id!r}, "
            f"version={self._version}, "
            f"source={self._source!r}, "
            f"keys={len(self.keys)}, "
            f"pending_events={len(self._pending_events)})"
        )

    def __eq__(self, other: object) -> bool:
        """Configurations are equal if they have the same ID."""
        if not isinstance(other, Configuration):
            return NotImplemented
        return self._id == other._id

    def __hash__(self) -> int:
        """Hash by ID for set/dict usage."""
        return hash(self._id)
