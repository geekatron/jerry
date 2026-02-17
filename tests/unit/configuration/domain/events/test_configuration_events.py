# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for Configuration Domain Events.

Tests cover:
    - AC-011.1: ConfigurationLoaded with source and key count
    - AC-011.2: ConfigurationValueChanged with key, old/new value
    - AC-011.3: ConfigurationError for failures
    - AC-011.4: All immutable (frozen dataclass)
    - AC-011.5: Extends DomainEvent base class

Test Categories:
    - Happy path: Valid event creation, serialization
    - Edge cases: None values, empty strings, factory methods
"""

from __future__ import annotations

import pytest

from src.configuration.domain.events.configuration_events import (
    ConfigurationError,
    ConfigurationLoaded,
    ConfigurationValueChanged,
)
from src.shared_kernel.domain_event import DomainEvent

# =============================================================================
# ConfigurationLoaded Tests
# =============================================================================


class TestConfigurationLoadedCreation:
    """Tests for ConfigurationLoaded instantiation."""

    def test_create_with_all_fields(self) -> None:
        """Create event with all fields specified."""
        event = ConfigurationLoaded(
            aggregate_id="config-001",
            aggregate_type="Configuration",
            source="project",
            source_path="/path/to/config.toml",
            keys_loaded=15,
            load_time_ms=42,
        )
        assert event.aggregate_id == "config-001"
        assert event.aggregate_type == "Configuration"
        assert event.source == "project"
        assert event.source_path == "/path/to/config.toml"
        assert event.keys_loaded == 15
        assert event.load_time_ms == 42

    def test_create_with_defaults(self) -> None:
        """Default values are applied."""
        event = ConfigurationLoaded(
            aggregate_id="config-001",
            aggregate_type="Configuration",
        )
        assert event.source == "unknown"
        assert event.source_path is None
        assert event.keys_loaded == 0
        assert event.load_time_ms == 0

    def test_create_factory_method(self) -> None:
        """Factory method creates valid event."""
        event = ConfigurationLoaded.create(
            aggregate_id="config-001",
            source="env",
            keys_loaded=10,
            source_path=None,
            load_time_ms=5,
        )
        assert event.aggregate_id == "config-001"
        assert event.aggregate_type == "Configuration"
        assert event.source == "env"
        assert event.keys_loaded == 10

    def test_extends_domain_event(self) -> None:
        """ConfigurationLoaded extends DomainEvent (AC-011.5)."""
        event = ConfigurationLoaded(
            aggregate_id="config-001",
            aggregate_type="Configuration",
        )
        assert isinstance(event, DomainEvent)

    def test_has_event_id_and_timestamp(self) -> None:
        """Event has auto-generated event_id and timestamp."""
        event = ConfigurationLoaded(
            aggregate_id="config-001",
            aggregate_type="Configuration",
        )
        assert event.event_id is not None
        assert len(event.event_id) > 0
        assert event.timestamp is not None


class TestConfigurationLoadedSerialization:
    """Tests for ConfigurationLoaded serialization."""

    def test_to_dict_includes_payload(self) -> None:
        """to_dict includes event-specific payload."""
        event = ConfigurationLoaded(
            aggregate_id="config-001",
            aggregate_type="Configuration",
            source="project",
            source_path="/config.toml",
            keys_loaded=5,
            load_time_ms=10,
        )
        data = event.to_dict()
        assert data["source"] == "project"
        assert data["source_path"] == "/config.toml"
        assert data["keys_loaded"] == 5
        assert data["load_time_ms"] == 10

    def test_from_dict_round_trip(self) -> None:
        """Serialization round-trip preserves data."""
        original = ConfigurationLoaded.create(
            aggregate_id="config-001",
            source="framework",
            keys_loaded=20,
            source_path="/framework/config.toml",
            load_time_ms=100,
        )
        data = original.to_dict()
        restored = ConfigurationLoaded.from_dict(data)
        assert restored.aggregate_id == original.aggregate_id
        assert restored.source == original.source
        assert restored.keys_loaded == original.keys_loaded
        assert restored.source_path == original.source_path

    def test_from_dict_with_missing_optional_fields(self) -> None:
        """from_dict handles missing optional fields."""
        data = {
            "aggregate_id": "config-001",
        }
        event = ConfigurationLoaded.from_dict(data)
        assert event.aggregate_id == "config-001"
        assert event.source == "unknown"
        assert event.keys_loaded == 0


class TestConfigurationLoadedImmutability:
    """Tests for ConfigurationLoaded immutability (AC-011.4)."""

    def test_frozen_cannot_modify_source(self) -> None:
        """Frozen dataclass prevents modification."""
        event = ConfigurationLoaded(
            aggregate_id="config-001",
            aggregate_type="Configuration",
            source="project",
        )
        with pytest.raises(AttributeError):
            event.source = "env"  # type: ignore[misc]

    def test_frozen_cannot_modify_keys_loaded(self) -> None:
        """Cannot modify keys_loaded."""
        event = ConfigurationLoaded(
            aggregate_id="config-001",
            aggregate_type="Configuration",
            keys_loaded=10,
        )
        with pytest.raises(AttributeError):
            event.keys_loaded = 20  # type: ignore[misc]


# =============================================================================
# ConfigurationValueChanged Tests
# =============================================================================


class TestConfigurationValueChangedCreation:
    """Tests for ConfigurationValueChanged instantiation."""

    def test_create_with_all_fields(self) -> None:
        """Create event with all fields specified."""
        event = ConfigurationValueChanged(
            aggregate_id="config-001",
            aggregate_type="Configuration",
            key="logging.level",
            old_value="INFO",
            new_value="DEBUG",
            source="env",
            reason="Debug mode enabled",
        )
        assert event.key == "logging.level"
        assert event.old_value == "INFO"
        assert event.new_value == "DEBUG"
        assert event.source == "env"
        assert event.reason == "Debug mode enabled"

    def test_create_factory_method(self) -> None:
        """Factory method creates valid event and converts values."""
        event = ConfigurationValueChanged.create(
            aggregate_id="config-001",
            key="timeout",
            old_value=30,
            new_value=60,
            source="project",
            reason="Increased timeout",
        )
        # Values are converted to strings
        assert event.old_value == "30"
        assert event.new_value == "60"
        assert event.source == "project"

    def test_create_factory_with_none_values(self) -> None:
        """Factory handles None values (for additions/removals)."""
        event = ConfigurationValueChanged.create(
            aggregate_id="config-001",
            key="new.key",
            old_value=None,
            new_value="value",
        )
        assert event.old_value is None
        assert event.new_value == "value"

    def test_extends_domain_event(self) -> None:
        """ConfigurationValueChanged extends DomainEvent (AC-011.5)."""
        event = ConfigurationValueChanged(
            aggregate_id="config-001",
            aggregate_type="Configuration",
        )
        assert isinstance(event, DomainEvent)


class TestConfigurationValueChangedProperties:
    """Tests for ConfigurationValueChanged property methods."""

    def test_is_addition_when_old_none_new_present(self) -> None:
        """is_addition returns True for new key."""
        event = ConfigurationValueChanged(
            aggregate_id="config-001",
            aggregate_type="Configuration",
            key="new.key",
            old_value=None,
            new_value="value",
        )
        assert event.is_addition is True
        assert event.is_removal is False
        assert event.is_update is False

    def test_is_removal_when_old_present_new_none(self) -> None:
        """is_removal returns True for removed key."""
        event = ConfigurationValueChanged(
            aggregate_id="config-001",
            aggregate_type="Configuration",
            key="removed.key",
            old_value="old",
            new_value=None,
        )
        assert event.is_addition is False
        assert event.is_removal is True
        assert event.is_update is False

    def test_is_update_when_both_present(self) -> None:
        """is_update returns True for value change."""
        event = ConfigurationValueChanged(
            aggregate_id="config-001",
            aggregate_type="Configuration",
            key="updated.key",
            old_value="old",
            new_value="new",
        )
        assert event.is_addition is False
        assert event.is_removal is False
        assert event.is_update is True

    def test_both_none_not_any_category(self) -> None:
        """Both values None is not addition, removal, or update."""
        event = ConfigurationValueChanged(
            aggregate_id="config-001",
            aggregate_type="Configuration",
            key="weird.key",
            old_value=None,
            new_value=None,
        )
        assert event.is_addition is False
        assert event.is_removal is False
        assert event.is_update is False


class TestConfigurationValueChangedSerialization:
    """Tests for ConfigurationValueChanged serialization."""

    def test_to_dict_includes_payload(self) -> None:
        """to_dict includes event-specific payload."""
        event = ConfigurationValueChanged(
            aggregate_id="config-001",
            aggregate_type="Configuration",
            key="logging.level",
            old_value="INFO",
            new_value="DEBUG",
            source="env",
            reason="Debug mode",
        )
        data = event.to_dict()
        assert data["key"] == "logging.level"
        assert data["old_value"] == "INFO"
        assert data["new_value"] == "DEBUG"
        assert data["source"] == "env"
        assert data["reason"] == "Debug mode"

    def test_from_dict_round_trip(self) -> None:
        """Serialization round-trip preserves data."""
        original = ConfigurationValueChanged.create(
            aggregate_id="config-001",
            key="setting",
            old_value="a",
            new_value="b",
            source="project",
            reason="Test change",
        )
        data = original.to_dict()
        restored = ConfigurationValueChanged.from_dict(data)
        assert restored.key == original.key
        assert restored.old_value == original.old_value
        assert restored.new_value == original.new_value


class TestConfigurationValueChangedImmutability:
    """Tests for ConfigurationValueChanged immutability (AC-011.4)."""

    def test_frozen_cannot_modify_key(self) -> None:
        """Frozen dataclass prevents key modification."""
        event = ConfigurationValueChanged(
            aggregate_id="config-001",
            aggregate_type="Configuration",
            key="original.key",
        )
        with pytest.raises(AttributeError):
            event.key = "modified.key"  # type: ignore[misc]


# =============================================================================
# ConfigurationError Tests
# =============================================================================


class TestConfigurationErrorCreation:
    """Tests for ConfigurationError instantiation."""

    def test_create_with_all_fields(self) -> None:
        """Create event with all fields specified."""
        event = ConfigurationError(
            aggregate_id="config-001",
            aggregate_type="Configuration",
            source="project",
            source_path="/config.toml",
            error_type="parse_error",
            error_message="Invalid TOML at line 15",
            recoverable=True,
            failed_keys=("bad.key1", "bad.key2"),
        )
        assert event.source == "project"
        assert event.source_path == "/config.toml"
        assert event.error_type == "parse_error"
        assert event.error_message == "Invalid TOML at line 15"
        assert event.recoverable is True
        assert event.failed_keys == ("bad.key1", "bad.key2")

    def test_create_with_defaults(self) -> None:
        """Default values are applied."""
        event = ConfigurationError(
            aggregate_id="config-001",
            aggregate_type="Configuration",
        )
        assert event.source == "unknown"
        assert event.error_type == "unknown"
        assert event.error_message == ""
        assert event.recoverable is True
        assert event.failed_keys == ()

    def test_create_factory_method(self) -> None:
        """Factory method creates valid event."""
        event = ConfigurationError.create(
            aggregate_id="config-001",
            source="framework",
            error_type="validation_error",
            error_message="Invalid value for timeout",
            source_path="/framework/config.toml",
            recoverable=True,
            failed_keys=["timeout"],
        )
        assert event.source == "framework"
        assert event.error_type == "validation_error"
        assert event.failed_keys == ("timeout",)

    def test_extends_domain_event(self) -> None:
        """ConfigurationError extends DomainEvent (AC-011.5)."""
        event = ConfigurationError(
            aggregate_id="config-001",
            aggregate_type="Configuration",
        )
        assert isinstance(event, DomainEvent)


class TestConfigurationErrorFactoryMethods:
    """Tests for ConfigurationError factory methods."""

    def test_parse_error_factory(self) -> None:
        """parse_error factory creates parse error event."""
        event = ConfigurationError.parse_error(
            aggregate_id="config-001",
            source="project",
            source_path="/config.toml",
            error_message="Invalid syntax at line 10",
        )
        assert event.error_type == "parse_error"
        assert event.recoverable is True
        assert event.source_path == "/config.toml"
        assert "Invalid syntax" in event.error_message

    def test_file_not_found_factory(self) -> None:
        """file_not_found factory creates file not found event."""
        event = ConfigurationError.file_not_found(
            aggregate_id="config-001",
            source="session_local",
            source_path="/missing/config.toml",
        )
        assert event.error_type == "file_not_found"
        assert event.recoverable is True
        assert "/missing/config.toml" in event.error_message


class TestConfigurationErrorProperties:
    """Tests for ConfigurationError property methods."""

    def test_is_parse_error_true(self) -> None:
        """is_parse_error returns True for parse errors."""
        event = ConfigurationError(
            aggregate_id="config-001",
            aggregate_type="Configuration",
            error_type="parse_error",
        )
        assert event.is_parse_error is True

    def test_is_parse_error_false(self) -> None:
        """is_parse_error returns False for other errors."""
        event = ConfigurationError(
            aggregate_id="config-001",
            aggregate_type="Configuration",
            error_type="file_not_found",
        )
        assert event.is_parse_error is False

    def test_is_file_error_file_not_found(self) -> None:
        """is_file_error returns True for file_not_found."""
        event = ConfigurationError(
            aggregate_id="config-001",
            aggregate_type="Configuration",
            error_type="file_not_found",
        )
        assert event.is_file_error is True

    def test_is_file_error_permission_denied(self) -> None:
        """is_file_error returns True for permission_denied."""
        event = ConfigurationError(
            aggregate_id="config-001",
            aggregate_type="Configuration",
            error_type="permission_denied",
        )
        assert event.is_file_error is True

    def test_is_file_error_false_for_parse_error(self) -> None:
        """is_file_error returns False for parse_error."""
        event = ConfigurationError(
            aggregate_id="config-001",
            aggregate_type="Configuration",
            error_type="parse_error",
        )
        assert event.is_file_error is False


class TestConfigurationErrorSerialization:
    """Tests for ConfigurationError serialization."""

    def test_to_dict_includes_payload(self) -> None:
        """to_dict includes event-specific payload."""
        event = ConfigurationError(
            aggregate_id="config-001",
            aggregate_type="Configuration",
            source="project",
            error_type="parse_error",
            error_message="Bad syntax",
            failed_keys=("key1", "key2"),
        )
        data = event.to_dict()
        assert data["source"] == "project"
        assert data["error_type"] == "parse_error"
        assert data["error_message"] == "Bad syntax"
        assert data["failed_keys"] == ["key1", "key2"]  # Converted to list

    def test_from_dict_round_trip(self) -> None:
        """Serialization round-trip preserves data."""
        original = ConfigurationError.create(
            aggregate_id="config-001",
            source="framework",
            error_type="validation_error",
            error_message="Invalid timeout",
            failed_keys=["timeout", "retry_count"],
        )
        data = original.to_dict()
        restored = ConfigurationError.from_dict(data)
        assert restored.source == original.source
        assert restored.error_type == original.error_type
        assert restored.failed_keys == original.failed_keys

    def test_from_dict_converts_list_to_tuple(self) -> None:
        """from_dict converts failed_keys list to tuple."""
        data = {
            "aggregate_id": "config-001",
            "failed_keys": ["key1", "key2"],
        }
        event = ConfigurationError.from_dict(data)
        assert isinstance(event.failed_keys, tuple)
        assert event.failed_keys == ("key1", "key2")


class TestConfigurationErrorImmutability:
    """Tests for ConfigurationError immutability (AC-011.4)."""

    def test_frozen_cannot_modify_error_type(self) -> None:
        """Frozen dataclass prevents error_type modification."""
        event = ConfigurationError(
            aggregate_id="config-001",
            aggregate_type="Configuration",
            error_type="parse_error",
        )
        with pytest.raises(AttributeError):
            event.error_type = "file_not_found"  # type: ignore[misc]

    def test_frozen_cannot_modify_failed_keys(self) -> None:
        """Frozen dataclass prevents failed_keys modification."""
        event = ConfigurationError(
            aggregate_id="config-001",
            aggregate_type="Configuration",
            failed_keys=("key1",),
        )
        with pytest.raises(AttributeError):
            event.failed_keys = ("key2",)  # type: ignore[misc]


# =============================================================================
# Event Type Name Tests
# =============================================================================


class TestEventTypeNames:
    """Tests for event type names used in serialization."""

    def test_configuration_loaded_event_type(self) -> None:
        """ConfigurationLoaded has correct event_type."""
        event = ConfigurationLoaded(
            aggregate_id="config-001",
            aggregate_type="Configuration",
        )
        # Event type is class name by default
        assert "ConfigurationLoaded" in event.to_dict()["event_type"]

    def test_configuration_value_changed_event_type(self) -> None:
        """ConfigurationValueChanged has correct event_type."""
        event = ConfigurationValueChanged(
            aggregate_id="config-001",
            aggregate_type="Configuration",
        )
        assert "ConfigurationValueChanged" in event.to_dict()["event_type"]

    def test_configuration_error_event_type(self) -> None:
        """ConfigurationError has correct event_type."""
        event = ConfigurationError(
            aggregate_id="config-001",
            aggregate_type="Configuration",
        )
        assert "ConfigurationError" in event.to_dict()["event_type"]
