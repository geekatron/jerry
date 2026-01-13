"""
Unit tests for Configuration Aggregate.

Tests cover:
    - AC-010.1: Configuration aggregate root with version tracking
    - AC-010.2: Nested key access (config.get("logging.level"))
    - AC-010.3: Type-safe accessors (get_string, get_bool, get_int, get_list)
    - AC-010.4: Emits ConfigurationLoaded on creation
    - AC-010.5: Emits ConfigurationValueChanged on mutations

Test Categories:
    - Happy path: Valid creation, queries, mutations
    - Negative: Invalid keys, missing values
    - Edge cases: Deep nesting, merges, history replay
"""

from __future__ import annotations

import pytest

from src.configuration.domain.aggregates.configuration import Configuration
from src.configuration.domain.events.configuration_events import (
    ConfigurationLoaded,
    ConfigurationValueChanged,
)
from src.configuration.domain.value_objects import ConfigSource, ConfigValue
from src.shared_kernel.exceptions import ValidationError

# =============================================================================
# Factory Method Tests
# =============================================================================


class TestConfigurationCreate:
    """Tests for Configuration.create() factory method."""

    def test_create_with_data(self) -> None:
        """Create configuration with initial data."""
        config = Configuration.create(
            data={"debug": True, "logging": {"level": "DEBUG"}},
            source="project",
        )
        assert config.get("debug") is True
        assert config.get("logging.level") == "DEBUG"

    def test_create_with_custom_id(self) -> None:
        """Create configuration with specific ID."""
        config = Configuration.create(
            data={},
            config_id="my-config-id",
        )
        assert config.id == "my-config-id"

    def test_create_auto_generates_id(self) -> None:
        """Auto-generated ID follows expected format."""
        config = Configuration.create(data={})
        assert config.id.startswith("CONFIG-")
        assert len(config.id) > 7  # "CONFIG-" plus some hex

    def test_create_empty_data(self) -> None:
        """Create with empty data dictionary."""
        config = Configuration.create(data={})
        assert config.keys == []

    def test_create_with_source_path(self) -> None:
        """Create with source path records in event."""
        config = Configuration.create(
            data={"key": "value"},
            source="project",
            source_path="/path/to/config.toml",
        )
        events = config.collect_events()
        assert len(events) == 1
        assert isinstance(events[0], ConfigurationLoaded)
        loaded_event = events[0]
        assert loaded_event.source_path == "/path/to/config.toml"


class TestConfigurationEmpty:
    """Tests for Configuration.empty() factory method."""

    def test_empty_creates_default_source(self) -> None:
        """Empty configuration has default source."""
        config = Configuration.empty()
        assert config.source == "default"

    def test_empty_has_no_keys(self) -> None:
        """Empty configuration has no keys."""
        config = Configuration.empty()
        assert config.keys == []

    def test_empty_with_custom_id(self) -> None:
        """Empty with custom ID."""
        config = Configuration.empty(config_id="empty-001")
        assert config.id == "empty-001"


# =============================================================================
# Property Tests
# =============================================================================


class TestConfigurationProperties:
    """Tests for Configuration property accessors."""

    def test_id_property(self) -> None:
        """ID property returns the identifier."""
        config = Configuration.create(data={}, config_id="test-id")
        assert config.id == "test-id"

    def test_version_increments(self) -> None:
        """Version increments with each event."""
        config = Configuration.create(data={})
        initial_version = config.version
        config.set("key", "value")
        assert config.version == initial_version + 1

    def test_source_property(self) -> None:
        """Source property returns creation source."""
        config = Configuration.create(data={}, source="env")
        assert config.source == "env"

    def test_data_property_returns_copy(self) -> None:
        """Data property returns a copy, not the internal dict."""
        config = Configuration.create(data={"key": "value"})
        data_copy = config.data
        data_copy["modified"] = True
        # Internal data should not be modified
        assert config.get("modified") is None

    def test_keys_property_flattens_nested(self) -> None:
        """Keys property returns flattened dot-notation keys."""
        config = Configuration.create(
            data={
                "a": 1,
                "b": {
                    "c": 2,
                    "d": {
                        "e": 3,
                    },
                },
            }
        )
        keys = config.keys
        assert "a" in keys
        assert "b.c" in keys
        assert "b.d.e" in keys

    def test_created_at_set_on_creation(self) -> None:
        """Created at is set when configuration is created."""
        config = Configuration.create(data={})
        assert config.created_at is not None

    def test_modified_at_updates_on_change(self) -> None:
        """Modified at updates when configuration changes."""
        config = Configuration.create(data={})
        config.collect_events()
        initial_modified = config.modified_at
        config.set("key", "value")
        assert config.modified_at is not None
        assert config.modified_at >= initial_modified


# =============================================================================
# Nested Key Resolution Tests (AC-010.2)
# =============================================================================


class TestNestedKeyResolution:
    """Tests for nested key access via dot-notation."""

    def test_get_simple_key(self) -> None:
        """Get value with simple key."""
        config = Configuration.create(data={"debug": True})
        assert config.get("debug") is True

    def test_get_nested_two_levels(self) -> None:
        """Get value with two-level nesting."""
        config = Configuration.create(data={"logging": {"level": "DEBUG"}})
        assert config.get("logging.level") == "DEBUG"

    def test_get_nested_three_levels(self) -> None:
        """Get value with three-level nesting."""
        config = Configuration.create(
            data={"database": {"connection": {"timeout": 30}}}
        )
        assert config.get("database.connection.timeout") == 30

    def test_get_nested_four_levels(self) -> None:
        """Get value with four-level deep nesting."""
        config = Configuration.create(
            data={"a": {"b": {"c": {"d": "deep"}}}}
        )
        assert config.get("a.b.c.d") == "deep"

    def test_get_missing_key_returns_default(self) -> None:
        """Missing key returns default value."""
        config = Configuration.create(data={})
        assert config.get("missing.key", "default") == "default"

    def test_get_partial_path_missing(self) -> None:
        """Partial path missing returns default."""
        config = Configuration.create(data={"logging": {}})
        assert config.get("logging.level.detail", "default") == "default"

    def test_get_returns_none_by_default(self) -> None:
        """Missing key returns None if no default specified."""
        config = Configuration.create(data={})
        assert config.get("missing") is None

    def test_get_namespace_returns_dict(self) -> None:
        """Get namespace prefix returns dictionary."""
        config = Configuration.create(
            data={"logging": {"level": "DEBUG", "format": "json"}}
        )
        namespace = config.get_namespace("logging")
        assert namespace == {"level": "DEBUG", "format": "json"}

    def test_get_namespace_missing_returns_empty(self) -> None:
        """Missing namespace returns empty dict."""
        config = Configuration.create(data={})
        assert config.get_namespace("missing") == {}


# =============================================================================
# Type-Safe Accessor Tests (AC-010.3)
# =============================================================================


class TestTypeCoercionThroughAggregate:
    """Tests for type-safe accessor methods."""

    def test_get_string(self) -> None:
        """get_string returns string value."""
        config = Configuration.create(data={"level": "DEBUG"}, source="project")
        assert config.get_string("level") == "DEBUG"

    def test_get_string_converts_int(self) -> None:
        """get_string converts int to string."""
        config = Configuration.create(data={"port": 8080}, source="project")
        assert config.get_string("port") == "8080"

    def test_get_string_default_for_missing(self) -> None:
        """get_string returns default for missing key."""
        config = Configuration.create(data={}, source="default")
        assert config.get_string("missing", "default") == "default"

    def test_get_bool_true_values(self) -> None:
        """get_bool interprets truthy strings."""
        for val in [True, "true", "TRUE", "1", "yes", "on"]:
            config = Configuration.create(data={"flag": val}, source="project")
            assert config.get_bool("flag") is True, f"Failed for {val}"

    def test_get_bool_false_values(self) -> None:
        """get_bool interprets falsy strings."""
        for val in [False, "false", "FALSE", "0", "no", "off"]:
            config = Configuration.create(data={"flag": val}, source="project")
            assert config.get_bool("flag") is False, f"Failed for {val}"

    def test_get_bool_default_for_missing(self) -> None:
        """get_bool returns default for missing key."""
        config = Configuration.create(data={}, source="default")
        assert config.get_bool("missing", True) is True

    def test_get_int(self) -> None:
        """get_int returns integer value."""
        config = Configuration.create(data={"count": 42}, source="project")
        assert config.get_int("count") == 42

    def test_get_int_from_string(self) -> None:
        """get_int converts string to int."""
        config = Configuration.create(data={"count": "42"}, source="project")
        assert config.get_int("count") == 42

    def test_get_int_default_for_invalid(self) -> None:
        """get_int returns default for non-numeric."""
        config = Configuration.create(data={"count": "invalid"}, source="project")
        assert config.get_int("count", 99) == 99

    def test_get_float(self) -> None:
        """get_float returns float value."""
        config = Configuration.create(data={"ratio": 3.14}, source="project")
        assert config.get_float("ratio") == 3.14

    def test_get_float_from_string(self) -> None:
        """get_float converts string to float."""
        config = Configuration.create(data={"ratio": "3.14"}, source="project")
        assert config.get_float("ratio") == 3.14

    def test_get_list_from_array(self) -> None:
        """get_list returns list value."""
        config = Configuration.create(data={"hosts": ["a", "b", "c"]}, source="project")
        assert config.get_list("hosts") == ["a", "b", "c"]

    def test_get_list_from_comma_string(self) -> None:
        """get_list splits comma-separated string."""
        config = Configuration.create(data={"hosts": "a,b,c"}, source="project")
        assert config.get_list("hosts") == ["a", "b", "c"]

    def test_get_list_default_for_missing(self) -> None:
        """get_list returns default for missing."""
        config = Configuration.create(data={}, source="default")
        assert config.get_list("missing", ["x"]) == ["x"]

    def test_get_value_returns_config_value(self) -> None:
        """get_value returns ConfigValue wrapper."""
        config = Configuration.create(data={"key": "value"}, source="project")
        cv = config.get_value("key")
        assert isinstance(cv, ConfigValue)
        assert cv.key == "key"
        assert cv.value == "value"
        assert cv.source == ConfigSource.PROJECT


class TestHasMethod:
    """Tests for has() existence check."""

    def test_has_existing_key(self) -> None:
        """has returns True for existing key."""
        config = Configuration.create(data={"key": "value"})
        assert config.has("key") is True

    def test_has_nested_key(self) -> None:
        """has returns True for nested key."""
        config = Configuration.create(data={"a": {"b": "c"}})
        assert config.has("a.b") is True

    def test_has_missing_key(self) -> None:
        """has returns False for missing key."""
        config = Configuration.create(data={})
        assert config.has("missing") is False


# =============================================================================
# Command Method Tests
# =============================================================================


class TestConfigurationSet:
    """Tests for Configuration.set() command method."""

    def test_set_simple_key(self) -> None:
        """Set a simple key value."""
        config = Configuration.create(data={}, source="project")
        config.collect_events()  # Clear creation event
        config.set("debug", True)
        # Note: set() stores values as strings in events.
        # When event is applied, the value becomes the string representation.
        assert config.get("debug") == "True"  # String after event apply
        assert config.get_bool("debug") is True  # Use typed getter for bool

    def test_set_nested_key(self) -> None:
        """Set creates nested structure."""
        config = Configuration.create(data={}, source="project")
        config.collect_events()
        config.set("logging.level", "DEBUG")
        assert config.get("logging.level") == "DEBUG"
        assert config.get("logging") == {"level": "DEBUG"}

    def test_set_deep_nested_key(self) -> None:
        """Set creates deep nested structure."""
        config = Configuration.create(data={}, source="project")
        config.collect_events()
        config.set("a.b.c.d", "value")
        assert config.get("a.b.c.d") == "value"

    def test_set_overwrites_existing(self) -> None:
        """Set overwrites existing value."""
        config = Configuration.create(data={"key": "old"}, source="project")
        config.collect_events()
        config.set("key", "new")
        assert config.get("key") == "new"

    def test_set_no_event_if_same_value(self) -> None:
        """No event emitted if value unchanged."""
        config = Configuration.create(data={"key": "value"}, source="project")
        config.collect_events()
        config.set("key", "value")  # Same value
        events = config.collect_events()
        assert len(events) == 0

    def test_set_with_reason(self) -> None:
        """Set includes reason in event."""
        config = Configuration.create(data={}, source="project")
        config.collect_events()
        config.set("debug", True, reason="Enable debug mode")
        events = config.collect_events()
        assert len(events) == 1
        assert events[0].reason == "Enable debug mode"


class TestConfigurationMerge:
    """Tests for Configuration.merge() command method."""

    def test_merge_adds_new_keys(self) -> None:
        """Merge adds new keys."""
        config = Configuration.create(data={"a": 1}, source="project")
        config.collect_events()
        config.merge({"b": 2})
        # Initial data keeps original type, merged values become strings
        assert config.get("a") == 1
        assert config.get("b") == "2"  # Merged value serialized to string
        assert config.get_int("b") == 2  # Use typed getter for int

    def test_merge_overwrites_existing(self) -> None:
        """Merge overwrites existing values."""
        config = Configuration.create(data={"key": "old"}, source="project")
        config.collect_events()
        config.merge({"key": "new"})
        assert config.get("key") == "new"

    def test_merge_nested_data(self) -> None:
        """Merge handles nested dictionaries."""
        config = Configuration.create(data={"a": {"b": 1}}, source="project")
        config.collect_events()
        config.merge({"a": {"c": 2}})
        # Initial data keeps original type, merged values become strings
        assert config.get("a.b") == 1
        assert config.get("a.c") == "2"  # Merged nested value serialized to string
        assert config.get_int("a.c") == 2  # Use typed getter for int

    def test_merge_emits_events_per_change(self) -> None:
        """Merge emits event for each changed key."""
        config = Configuration.create(data={"a": 1}, source="project")
        config.collect_events()
        config.merge({"b": 2, "c": 3})
        events = config.collect_events()
        assert len(events) == 2  # Two new keys

    def test_merge_no_event_if_unchanged(self) -> None:
        """Merge doesn't emit event for unchanged keys."""
        config = Configuration.create(data={"a": 1}, source="project")
        config.collect_events()
        config.merge({"a": 1})  # Same value
        events = config.collect_events()
        assert len(events) == 0


# =============================================================================
# Event Emission Tests (AC-010.4, AC-010.5)
# =============================================================================


class TestConfigurationLoadedEvent:
    """Tests for ConfigurationLoaded event emission (AC-010.4)."""

    def test_create_emits_loaded_event(self) -> None:
        """Creation emits ConfigurationLoaded event."""
        config = Configuration.create(data={"key": "value"})
        events = config.collect_events()
        assert len(events) == 1
        assert isinstance(events[0], ConfigurationLoaded)

    def test_loaded_event_has_correct_source(self) -> None:
        """Loaded event has correct source."""
        config = Configuration.create(data={}, source="project")
        events = config.collect_events()
        assert events[0].source == "project"

    def test_loaded_event_counts_keys(self) -> None:
        """Loaded event counts keys correctly."""
        config = Configuration.create(
            data={"a": 1, "b": {"c": 2, "d": 3}}
        )
        events = config.collect_events()
        assert events[0].keys_loaded == 3  # a, b.c, b.d

    def test_loaded_event_has_aggregate_id(self) -> None:
        """Loaded event has matching aggregate ID."""
        config = Configuration.create(data={}, config_id="test-id")
        events = config.collect_events()
        assert events[0].aggregate_id == "test-id"


class TestConfigurationValueChangedEvent:
    """Tests for ConfigurationValueChanged event emission (AC-010.5)."""

    def test_set_emits_value_changed_event(self) -> None:
        """Set emits ConfigurationValueChanged event."""
        config = Configuration.create(data={})
        config.collect_events()
        config.set("key", "value")
        events = config.collect_events()
        assert len(events) == 1
        assert isinstance(events[0], ConfigurationValueChanged)

    def test_value_changed_event_captures_old_value(self) -> None:
        """Value changed captures old value."""
        config = Configuration.create(data={"key": "old"})
        config.collect_events()
        config.set("key", "new")
        events = config.collect_events()
        assert events[0].old_value == "old"
        assert events[0].new_value == "new"

    def test_value_changed_event_for_addition(self) -> None:
        """Addition has None old value."""
        config = Configuration.create(data={})
        config.collect_events()
        config.set("new_key", "value")
        events = config.collect_events()
        assert events[0].old_value is None
        assert events[0].new_value == "value"
        assert events[0].is_addition is True


class TestEventCollection:
    """Tests for event collection infrastructure."""

    def test_collect_events_clears_pending(self) -> None:
        """Collecting events clears pending list."""
        config = Configuration.create(data={})
        events1 = config.collect_events()
        events2 = config.collect_events()
        assert len(events1) == 1
        assert len(events2) == 0

    def test_has_pending_events(self) -> None:
        """has_pending_events reports correctly."""
        config = Configuration.create(data={})
        assert config.has_pending_events() is True
        config.collect_events()
        assert config.has_pending_events() is False
        config.set("key", "value")
        assert config.has_pending_events() is True


# =============================================================================
# History Replay Tests
# =============================================================================


class TestHistoryReplay:
    """Tests for Configuration.load_from_history()."""

    def test_load_from_single_event(self) -> None:
        """Load from single loaded event."""
        original = Configuration.create(data={"key": "value"}, config_id="test-id")
        events = list(original.collect_events())

        restored = Configuration.load_from_history(events)
        assert restored.id == "test-id"
        assert restored.source == original.source

    def test_load_replays_value_changes(self) -> None:
        """Load replays value change events."""
        original = Configuration.create(data={"a": 1})
        original.set("b", 2)
        original.set("a", 10)  # Modify existing
        events = list(original.collect_events())

        restored = Configuration.load_from_history(events)
        assert restored.get("a") == "10"  # Note: stored as string in event
        assert restored.get("b") == "2"

    def test_load_preserves_version(self) -> None:
        """Load restores correct version."""
        original = Configuration.create(data={})
        original.set("a", 1)
        original.set("b", 2)
        events = list(original.collect_events())

        restored = Configuration.load_from_history(events)
        assert restored.version == original.version

    def test_load_from_empty_raises(self) -> None:
        """Load from empty events raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            Configuration.load_from_history([])
        assert "empty event history" in str(exc_info.value)

    def test_load_with_initial_data(self) -> None:
        """Load can start with initial data."""
        original = Configuration.create(data={"a": 1})
        original.set("b", 2)
        events = list(original.collect_events())

        restored = Configuration.load_from_history(events, initial_data={"z": 99})
        # z is in initial data but not modified by events
        assert restored.get("z") == 99


# =============================================================================
# Validation Tests
# =============================================================================


class TestConfigurationValidation:
    """Tests for key validation."""

    def test_set_with_invalid_key_raises(self) -> None:
        """Set with invalid key format raises ValidationError."""
        config = Configuration.create(data={})
        with pytest.raises(ValidationError):
            config.set(".invalid", "value")

    def test_set_with_empty_key_raises(self) -> None:
        """Set with empty key raises ValidationError."""
        config = Configuration.create(data={})
        with pytest.raises(ValidationError):
            config.set("", "value")


# =============================================================================
# Equality and Hashing Tests
# =============================================================================


class TestConfigurationEquality:
    """Tests for equality and hashing."""

    def test_equality_by_id(self) -> None:
        """Configurations with same ID are equal."""
        config1 = Configuration.create(data={}, config_id="same-id")
        config2 = Configuration.create(data={"different": True}, config_id="same-id")
        assert config1 == config2

    def test_inequality_different_ids(self) -> None:
        """Configurations with different IDs are not equal."""
        config1 = Configuration.create(data={}, config_id="id-1")
        config2 = Configuration.create(data={}, config_id="id-2")
        assert config1 != config2

    def test_hash_consistency(self) -> None:
        """Configurations can be used in sets/dicts."""
        config1 = Configuration.create(data={}, config_id="test-id")
        config2 = Configuration.create(data={}, config_id="test-id")
        config_set = {config1, config2}
        assert len(config_set) == 1


# =============================================================================
# String Representation Tests
# =============================================================================


class TestConfigurationStringRepresentation:
    """Tests for string representations."""

    def test_str_includes_summary(self) -> None:
        """str includes ID, key count, source."""
        config = Configuration.create(
            data={"a": 1, "b": 2},
            source="project",
            config_id="test-id",
        )
        result = str(config)
        assert "test-id" in result
        assert "2" in result  # key count
        assert "project" in result

    def test_repr_includes_details(self) -> None:
        """repr includes detailed info."""
        config = Configuration.create(data={}, config_id="test-id")
        result = repr(config)
        assert "Configuration" in result
        assert "test-id" in result
        assert "version" in result
