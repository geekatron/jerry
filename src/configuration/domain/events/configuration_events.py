# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Configuration Domain Events.

Domain events for the Configuration aggregate. These events capture all
significant state changes in configuration loading and updates.

All events are:
    - Immutable (frozen dataclasses)
    - Named in past tense
    - Contain aggregate reference data from DomainEvent base

References:
    - WI-011: Configuration Domain Events
    - ADR-009: Event Storage Mechanism
    - DDD Domain Events pattern (Evans, 2004)

Exports:
    ConfigurationLoaded: Emitted when configuration is loaded
    ConfigurationValueChanged: Emitted when a value is updated
    ConfigurationError: Emitted on configuration errors
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from src.shared_kernel.domain_event import DomainEvent, _current_timestamp, _generate_event_id

# =============================================================================
# Configuration Loading Event
# =============================================================================


@dataclass(frozen=True)
class ConfigurationLoaded(DomainEvent):
    """
    Emitted when configuration is successfully loaded from a source.

    This event captures the successful loading of configuration data
    from any of the 5 precedence levels.

    Attributes:
        source: The source type (env, session_local, project, framework, default)
        source_path: The file path if file-based source, or None for env/default
        keys_loaded: Number of configuration keys loaded
        load_time_ms: Time taken to load in milliseconds

    Examples:
        >>> event = ConfigurationLoaded(
        ...     aggregate_id="config-001",
        ...     aggregate_type="Configuration",
        ...     source="project",
        ...     source_path="/path/to/project/config.toml",
        ...     keys_loaded=15,
        ... )

    Invariants:
        - source must be one of: env, session_local, project, framework, default
        - keys_loaded must be >= 0
    """

    source: str = "unknown"
    source_path: str | None = None
    keys_loaded: int = 0
    load_time_ms: int = 0

    def _payload(self) -> dict[str, Any]:
        """Return event-specific payload data."""
        return {
            "source": self.source,
            "source_path": self.source_path,
            "keys_loaded": self.keys_loaded,
            "load_time_ms": self.load_time_ms,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ConfigurationLoaded:
        """Deserialize from dictionary."""
        timestamp_str = data.get("timestamp")
        timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else _current_timestamp()

        return cls(
            event_id=data.get("event_id", _generate_event_id()),
            aggregate_id=data["aggregate_id"],
            aggregate_type=data.get("aggregate_type", "Configuration"),
            version=data.get("version", 1),
            timestamp=timestamp,
            source=data.get("source", "unknown"),
            source_path=data.get("source_path"),
            keys_loaded=data.get("keys_loaded", 0),
            load_time_ms=data.get("load_time_ms", 0),
        )

    @classmethod
    def create(
        cls,
        aggregate_id: str,
        source: str,
        keys_loaded: int,
        source_path: str | None = None,
        load_time_ms: int = 0,
        version: int = 1,
    ) -> ConfigurationLoaded:
        """
        Factory method for creating ConfigurationLoaded event.

        Args:
            aggregate_id: ID of the configuration aggregate
            source: Source type (env, project, etc.)
            keys_loaded: Number of keys loaded
            source_path: Optional file path
            load_time_ms: Load time in milliseconds
            version: Event version

        Returns:
            New ConfigurationLoaded event
        """
        return cls(
            aggregate_id=aggregate_id,
            aggregate_type="Configuration",
            version=version,
            source=source,
            source_path=source_path,
            keys_loaded=keys_loaded,
            load_time_ms=load_time_ms,
        )


# =============================================================================
# Value Change Event
# =============================================================================


@dataclass(frozen=True)
class ConfigurationValueChanged(DomainEvent):
    """
    Emitted when a configuration value is updated.

    Captures both the old and new values for audit trails and
    potential rollback scenarios.

    Attributes:
        key: The configuration key that changed
        old_value: Previous value (as string for serialization)
        new_value: New value (as string for serialization)
        source: Where the change originated from
        reason: Optional reason for the change

    Examples:
        >>> event = ConfigurationValueChanged(
        ...     aggregate_id="config-001",
        ...     aggregate_type="Configuration",
        ...     key="logging.level",
        ...     old_value="INFO",
        ...     new_value="DEBUG",
        ...     source="env",
        ... )

    Invariants:
        - key must not be empty
        - old_value and new_value may be None (for additions/removals)
    """

    key: str = ""
    old_value: str | None = None
    new_value: str | None = None
    source: str = "unknown"
    reason: str | None = None

    def _payload(self) -> dict[str, Any]:
        """Return event-specific payload data."""
        return {
            "key": self.key,
            "old_value": self.old_value,
            "new_value": self.new_value,
            "source": self.source,
            "reason": self.reason,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ConfigurationValueChanged:
        """Deserialize from dictionary."""
        timestamp_str = data.get("timestamp")
        timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else _current_timestamp()

        return cls(
            event_id=data.get("event_id", _generate_event_id()),
            aggregate_id=data["aggregate_id"],
            aggregate_type=data.get("aggregate_type", "Configuration"),
            version=data.get("version", 1),
            timestamp=timestamp,
            key=data.get("key", ""),
            old_value=data.get("old_value"),
            new_value=data.get("new_value"),
            source=data.get("source", "unknown"),
            reason=data.get("reason"),
        )

    @classmethod
    def create(
        cls,
        aggregate_id: str,
        key: str,
        old_value: Any,
        new_value: Any,
        source: str = "unknown",
        reason: str | None = None,
        version: int = 1,
    ) -> ConfigurationValueChanged:
        """
        Factory method for creating ConfigurationValueChanged event.

        Args:
            aggregate_id: ID of the configuration aggregate
            key: Configuration key that changed
            old_value: Previous value (will be converted to string)
            new_value: New value (will be converted to string)
            source: Source of the change
            reason: Optional reason for change
            version: Event version

        Returns:
            New ConfigurationValueChanged event
        """
        return cls(
            aggregate_id=aggregate_id,
            aggregate_type="Configuration",
            version=version,
            key=key,
            old_value=str(old_value) if old_value is not None else None,
            new_value=str(new_value) if new_value is not None else None,
            source=source,
            reason=reason,
        )

    @property
    def is_addition(self) -> bool:
        """Check if this is a new key addition."""
        return self.old_value is None and self.new_value is not None

    @property
    def is_removal(self) -> bool:
        """Check if this is a key removal."""
        return self.old_value is not None and self.new_value is None

    @property
    def is_update(self) -> bool:
        """Check if this is a value update (not addition or removal)."""
        return self.old_value is not None and self.new_value is not None


# =============================================================================
# Configuration Error Event
# =============================================================================


@dataclass(frozen=True)
class ConfigurationError(DomainEvent):
    """
    Emitted when configuration loading or parsing fails.

    Captures error information for debugging and audit purposes.
    Does not necessarily indicate aggregate failure - the aggregate
    may continue with partial configuration.

    Attributes:
        source: The source that failed (env, project, etc.)
        source_path: File path if file-based, or None
        error_type: Type of error (parse_error, file_not_found, permission_denied, etc.)
        error_message: Human-readable error description
        recoverable: Whether the system can continue with partial config

    Examples:
        >>> event = ConfigurationError(
        ...     aggregate_id="config-001",
        ...     aggregate_type="Configuration",
        ...     source="project",
        ...     source_path="/path/to/config.toml",
        ...     error_type="parse_error",
        ...     error_message="Invalid TOML syntax at line 15",
        ...     recoverable=True,
        ... )

    Error Types:
        - parse_error: Configuration file has invalid syntax
        - file_not_found: Configuration file doesn't exist
        - permission_denied: Cannot read configuration file
        - validation_error: Configuration values don't pass validation
        - unknown: Unexpected error
    """

    source: str = "unknown"
    source_path: str | None = None
    error_type: str = "unknown"
    error_message: str = ""
    recoverable: bool = True
    failed_keys: tuple[str, ...] = field(default_factory=tuple)

    def _payload(self) -> dict[str, Any]:
        """Return event-specific payload data."""
        return {
            "source": self.source,
            "source_path": self.source_path,
            "error_type": self.error_type,
            "error_message": self.error_message,
            "recoverable": self.recoverable,
            "failed_keys": list(self.failed_keys),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ConfigurationError:
        """Deserialize from dictionary."""
        timestamp_str = data.get("timestamp")
        timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else _current_timestamp()

        failed_keys = data.get("failed_keys", [])
        if isinstance(failed_keys, list):
            failed_keys = tuple(failed_keys)

        return cls(
            event_id=data.get("event_id", _generate_event_id()),
            aggregate_id=data["aggregate_id"],
            aggregate_type=data.get("aggregate_type", "Configuration"),
            version=data.get("version", 1),
            timestamp=timestamp,
            source=data.get("source", "unknown"),
            source_path=data.get("source_path"),
            error_type=data.get("error_type", "unknown"),
            error_message=data.get("error_message", ""),
            recoverable=data.get("recoverable", True),
            failed_keys=failed_keys,
        )

    @classmethod
    def create(
        cls,
        aggregate_id: str,
        source: str,
        error_type: str,
        error_message: str,
        source_path: str | None = None,
        recoverable: bool = True,
        failed_keys: list[str] | None = None,
        version: int = 1,
    ) -> ConfigurationError:
        """
        Factory method for creating ConfigurationError event.

        Args:
            aggregate_id: ID of the configuration aggregate
            source: Source that failed
            error_type: Type of error
            error_message: Error description
            source_path: Optional file path
            recoverable: Whether system can continue
            failed_keys: List of keys that failed to load
            version: Event version

        Returns:
            New ConfigurationError event
        """
        return cls(
            aggregate_id=aggregate_id,
            aggregate_type="Configuration",
            version=version,
            source=source,
            source_path=source_path,
            error_type=error_type,
            error_message=error_message,
            recoverable=recoverable,
            failed_keys=tuple(failed_keys) if failed_keys else (),
        )

    @classmethod
    def parse_error(
        cls,
        aggregate_id: str,
        source: str,
        source_path: str,
        error_message: str,
        version: int = 1,
    ) -> ConfigurationError:
        """
        Factory for parse errors.

        Parse errors are typically recoverable as the system
        can continue with other configuration sources.
        """
        return cls.create(
            aggregate_id=aggregate_id,
            source=source,
            error_type="parse_error",
            error_message=error_message,
            source_path=source_path,
            recoverable=True,
            version=version,
        )

    @classmethod
    def file_not_found(
        cls,
        aggregate_id: str,
        source: str,
        source_path: str,
        version: int = 1,
    ) -> ConfigurationError:
        """
        Factory for file not found errors.

        File not found is recoverable - the system continues
        without this configuration source.
        """
        return cls.create(
            aggregate_id=aggregate_id,
            source=source,
            error_type="file_not_found",
            error_message=f"Configuration file not found: {source_path}",
            source_path=source_path,
            recoverable=True,
            version=version,
        )

    @property
    def is_parse_error(self) -> bool:
        """Check if this is a parse error."""
        return self.error_type == "parse_error"

    @property
    def is_file_error(self) -> bool:
        """Check if this is a file access error."""
        return self.error_type in ("file_not_found", "permission_denied")
