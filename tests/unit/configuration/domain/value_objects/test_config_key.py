# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for ConfigKey value object.

Tests cover:
    - AC-009.1: ConfigKey with dot-notation support
    - AC-009.2: ConfigKey.to_env_key() conversion
    - AC-009.5: Immutability (frozen dataclass)

Test Categories:
    - Happy path: Valid key creation, conversions
    - Negative: Invalid formats, empty keys
    - Edge cases: Single segment, deep nesting, special characters
"""

from __future__ import annotations

import pytest

from src.configuration.domain.value_objects.config_key import ConfigKey
from src.shared_kernel.exceptions import ValidationError


class TestConfigKeyCreation:
    """Tests for ConfigKey instantiation."""

    def test_create_single_segment_key(self) -> None:
        """Single segment key is valid."""
        key = ConfigKey("debug")
        assert key.value == "debug"

    def test_create_two_segment_key(self) -> None:
        """Two-segment dot-notation key is valid."""
        key = ConfigKey("logging.level")
        assert key.value == "logging.level"

    def test_create_multi_segment_key(self) -> None:
        """Multi-segment deep key is valid."""
        key = ConfigKey("database.connection.pool.size")
        assert key.value == "database.connection.pool.size"

    def test_create_key_with_underscores(self) -> None:
        """Keys with underscores are valid."""
        key = ConfigKey("database_connection.pool_size")
        assert key.value == "database_connection.pool_size"

    def test_create_key_with_hyphens(self) -> None:
        """Keys with hyphens are valid."""
        key = ConfigKey("log-level")
        assert key.value == "log-level"

    def test_create_key_with_numbers(self) -> None:
        """Keys with numbers (not leading) are valid."""
        key = ConfigKey("server2.port80")
        assert key.value == "server2.port80"


class TestConfigKeyValidation:
    """Tests for ConfigKey validation errors."""

    def test_empty_key_raises_validation_error(self) -> None:
        """Empty string raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            ConfigKey("")
        assert exc_info.value.field == "key"
        assert "cannot be empty" in str(exc_info.value)

    def test_whitespace_only_raises_validation_error(self) -> None:
        """Whitespace-only string raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            ConfigKey("   ")
        assert exc_info.value.field == "key"

    def test_leading_whitespace_raises_validation_error(self) -> None:
        """Leading whitespace raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            ConfigKey(" debug")
        assert "whitespace" in str(exc_info.value).lower()

    def test_trailing_whitespace_raises_validation_error(self) -> None:
        """Trailing whitespace raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            ConfigKey("debug ")
        assert "whitespace" in str(exc_info.value).lower()

    def test_leading_dot_raises_validation_error(self) -> None:
        """Leading dot raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            ConfigKey(".debug")
        assert exc_info.value.field == "key"

    def test_trailing_dot_raises_validation_error(self) -> None:
        """Trailing dot raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            ConfigKey("debug.")
        assert exc_info.value.field == "key"

    def test_consecutive_dots_raises_validation_error(self) -> None:
        """Consecutive dots raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            ConfigKey("logging..level")
        assert exc_info.value.field == "key"

    def test_leading_number_raises_validation_error(self) -> None:
        """Leading number raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            ConfigKey("2server.port")
        assert exc_info.value.field == "key"

    def test_special_characters_raise_validation_error(self) -> None:
        """Special characters (except underscore/hyphen) raise ValidationError."""
        invalid_chars = ["debug@level", "debug#level", "debug$level", "debug%level"]
        for invalid in invalid_chars:
            with pytest.raises(ValidationError):
                ConfigKey(invalid)


class TestConfigKeyProperties:
    """Tests for ConfigKey property accessors."""

    def test_parts_single_segment(self) -> None:
        """Parts returns tuple for single segment."""
        key = ConfigKey("debug")
        assert key.parts == ("debug",)

    def test_parts_multiple_segments(self) -> None:
        """Parts splits by dots."""
        key = ConfigKey("logging.level")
        assert key.parts == ("logging", "level")

    def test_parts_deep_key(self) -> None:
        """Parts handles deep nesting."""
        key = ConfigKey("a.b.c.d.e")
        assert key.parts == ("a", "b", "c", "d", "e")

    def test_namespace_single_segment_returns_none(self) -> None:
        """Namespace is None for root-level key."""
        key = ConfigKey("debug")
        assert key.namespace is None

    def test_namespace_two_segments(self) -> None:
        """Namespace returns parent for two segments."""
        key = ConfigKey("logging.level")
        assert key.namespace == "logging"

    def test_namespace_multiple_segments(self) -> None:
        """Namespace returns parent path for multiple segments."""
        key = ConfigKey("database.connection.pool")
        assert key.namespace == "database.connection"

    def test_leaf_single_segment(self) -> None:
        """Leaf returns the key itself for single segment."""
        key = ConfigKey("debug")
        assert key.leaf == "debug"

    def test_leaf_multiple_segments(self) -> None:
        """Leaf returns last segment for multiple segments."""
        key = ConfigKey("logging.level")
        assert key.leaf == "level"

    def test_depth_single_segment(self) -> None:
        """Depth is 1 for single segment."""
        key = ConfigKey("debug")
        assert key.depth == 1

    def test_depth_multiple_segments(self) -> None:
        """Depth counts all segments."""
        key = ConfigKey("a.b.c.d")
        assert key.depth == 4


class TestConfigKeyEnvConversion:
    """Tests for environment variable conversion (AC-009.2)."""

    def test_to_env_key_single_segment(self) -> None:
        """Single segment converts to uppercase with prefix."""
        key = ConfigKey("debug")
        assert key.to_env_key() == "JERRY_DEBUG"

    def test_to_env_key_multiple_segments(self) -> None:
        """Dots become double underscores."""
        key = ConfigKey("logging.level")
        assert key.to_env_key() == "JERRY_LOGGING__LEVEL"

    def test_to_env_key_with_underscores(self) -> None:
        """Underscores are preserved."""
        key = ConfigKey("database_connection.pool_size")
        assert key.to_env_key() == "JERRY_DATABASE_CONNECTION__POOL_SIZE"

    def test_to_env_key_with_hyphens(self) -> None:
        """Hyphens become single underscores."""
        key = ConfigKey("log-level")
        assert key.to_env_key() == "JERRY_LOG_LEVEL"

    def test_to_env_key_custom_prefix(self) -> None:
        """Custom prefix is applied."""
        key = ConfigKey("debug")
        assert key.to_env_key(prefix="APP_") == "APP_DEBUG"

    def test_to_env_key_empty_prefix(self) -> None:
        """Empty prefix is allowed."""
        key = ConfigKey("debug")
        assert key.to_env_key(prefix="") == "DEBUG"

    def test_from_env_key_single_segment(self) -> None:
        """Parse single segment env var."""
        key = ConfigKey.from_env_key("JERRY_DEBUG")
        assert key.value == "debug"

    def test_from_env_key_multiple_segments(self) -> None:
        """Parse multi-segment env var (double underscore to dot)."""
        key = ConfigKey.from_env_key("JERRY_LOGGING__LEVEL")
        assert key.value == "logging.level"

    def test_from_env_key_with_single_underscore(self) -> None:
        """Single underscores become hyphens."""
        key = ConfigKey.from_env_key("JERRY_LOG_LEVEL")
        assert key.value == "log-level"

    def test_from_env_key_custom_prefix(self) -> None:
        """Parse with custom prefix."""
        key = ConfigKey.from_env_key("APP_DEBUG", prefix="APP_")
        assert key.value == "debug"

    def test_from_env_key_missing_prefix_raises(self) -> None:
        """Missing prefix raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            ConfigKey.from_env_key("DEBUG")
        assert "JERRY_" in str(exc_info.value)

    def test_from_env_key_wrong_prefix_raises(self) -> None:
        """Wrong prefix raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            ConfigKey.from_env_key("APP_DEBUG", prefix="JERRY_")
        assert "JERRY_" in str(exc_info.value)

    def test_round_trip_conversion(self) -> None:
        """Convert to env and back preserves key (with hyphen)."""
        original = ConfigKey("logging.log-level")
        env_key = original.to_env_key()
        restored = ConfigKey.from_env_key(env_key)
        assert restored.value == original.value


class TestConfigKeyNavigation:
    """Tests for key navigation methods."""

    def test_child_creates_nested_key(self) -> None:
        """Child appends segment."""
        key = ConfigKey("logging")
        child = key.child("level")
        assert child.value == "logging.level"

    def test_child_chaining(self) -> None:
        """Multiple child calls build path."""
        key = ConfigKey("a").child("b").child("c")
        assert key.value == "a.b.c"

    def test_parent_returns_parent_key(self) -> None:
        """Parent returns enclosing namespace."""
        key = ConfigKey("logging.level")
        parent = key.parent()
        assert parent is not None
        assert parent.value == "logging"

    def test_parent_root_returns_none(self) -> None:
        """Root key has no parent."""
        key = ConfigKey("debug")
        assert key.parent() is None

    def test_parent_deep_key(self) -> None:
        """Parent of deep key returns immediate parent."""
        key = ConfigKey("a.b.c.d")
        parent = key.parent()
        assert parent is not None
        assert parent.value == "a.b.c"


class TestConfigKeyMatching:
    """Tests for key matching and comparison."""

    def test_starts_with_exact_match(self) -> None:
        """Exact match returns True."""
        key = ConfigKey("logging")
        assert key.starts_with("logging") is True

    def test_starts_with_prefix_match(self) -> None:
        """Child key starts with parent."""
        key = ConfigKey("logging.level")
        assert key.starts_with("logging") is True

    def test_starts_with_partial_segment_no_match(self) -> None:
        """Partial segment does not match."""
        key = ConfigKey("logging.level")
        assert key.starts_with("log") is False

    def test_starts_with_config_key(self) -> None:
        """Accepts ConfigKey as prefix."""
        key = ConfigKey("logging.level")
        prefix = ConfigKey("logging")
        assert key.starts_with(prefix) is True

    def test_starts_with_no_match(self) -> None:
        """Unrelated prefix returns False."""
        key = ConfigKey("logging.level")
        assert key.starts_with("database") is False

    def test_relative_to_removes_prefix(self) -> None:
        """Relative removes prefix."""
        key = ConfigKey("logging.level")
        relative = key.relative_to("logging")
        assert relative is not None
        assert relative.value == "level"

    def test_relative_to_exact_match_returns_none(self) -> None:
        """Relative to exact match returns None."""
        key = ConfigKey("logging")
        assert key.relative_to("logging") is None

    def test_relative_to_no_match_returns_none(self) -> None:
        """Relative to non-prefix returns None."""
        key = ConfigKey("logging.level")
        assert key.relative_to("database") is None

    def test_relative_to_config_key(self) -> None:
        """Accepts ConfigKey as prefix."""
        key = ConfigKey("a.b.c")
        prefix = ConfigKey("a")
        relative = key.relative_to(prefix)
        assert relative is not None
        assert relative.value == "b.c"


class TestConfigKeyImmutability:
    """Tests for immutability (AC-009.5)."""

    def test_frozen_cannot_modify_value(self) -> None:
        """Frozen dataclass prevents attribute modification."""
        key = ConfigKey("debug")
        with pytest.raises(AttributeError):
            key.value = "modified"  # type: ignore[misc]

    def test_equality_by_value(self) -> None:
        """Two keys with same value are equal."""
        key1 = ConfigKey("logging.level")
        key2 = ConfigKey("logging.level")
        assert key1 == key2

    def test_hash_consistency(self) -> None:
        """Keys can be used in sets/dicts."""
        key1 = ConfigKey("debug")
        key2 = ConfigKey("debug")
        key_set = {key1, key2}
        assert len(key_set) == 1


class TestConfigKeyStringRepresentation:
    """Tests for string representations."""

    def test_str_returns_value(self) -> None:
        """str() returns the key value."""
        key = ConfigKey("logging.level")
        assert str(key) == "logging.level"

    def test_repr_includes_class_name(self) -> None:
        """repr() includes class name for debugging."""
        key = ConfigKey("debug")
        assert "ConfigKey" in repr(key)
        assert "debug" in repr(key)
