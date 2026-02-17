# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for ConfigValue value object.

Tests cover:
    - AC-009.4: ConfigValue supports type coercion (str → bool/int/list)
    - AC-009.5: Immutability (frozen dataclass)
    - Type-safe accessors

Test Categories:
    - Happy path: Valid value creation, type coercions
    - Negative: Invalid values, coercion failures
    - Edge cases: Empty values, None handling, default fallbacks
"""

from __future__ import annotations

import pytest

from src.configuration.domain.value_objects.config_source import ConfigSource
from src.configuration.domain.value_objects.config_value import ConfigValue


class TestConfigValueCreation:
    """Tests for ConfigValue instantiation."""

    def test_create_string_value(self) -> None:
        """Create value with string."""
        cv = ConfigValue(key="debug", value="true", source=ConfigSource.ENV)
        assert cv.key == "debug"
        assert cv.value == "true"
        assert cv.source == ConfigSource.ENV

    def test_create_int_value(self) -> None:
        """Create value with integer."""
        cv = ConfigValue(key="port", value=8080, source=ConfigSource.PROJECT)
        assert cv.value == 8080

    def test_create_bool_value(self) -> None:
        """Create value with boolean."""
        cv = ConfigValue(key="enabled", value=True, source=ConfigSource.DEFAULT)
        assert cv.value is True

    def test_create_list_value(self) -> None:
        """Create value with list."""
        cv = ConfigValue(key="hosts", value=["a", "b", "c"], source=ConfigSource.ENV)
        assert cv.value == ["a", "b", "c"]

    def test_create_dict_value(self) -> None:
        """Create value with dictionary."""
        cv = ConfigValue(key="settings", value={"a": 1}, source=ConfigSource.PROJECT)
        assert cv.value == {"a": 1}

    def test_create_none_value(self) -> None:
        """Create value with None."""
        cv = ConfigValue(key="missing", value=None, source=ConfigSource.DEFAULT)
        assert cv.value is None


class TestConfigValueValidation:
    """Tests for ConfigValue validation."""

    def test_empty_key_raises_value_error(self) -> None:
        """Empty key raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            ConfigValue(key="", value="test", source=ConfigSource.ENV)
        assert "cannot be empty" in str(exc_info.value)


class TestConfigValueProperties:
    """Tests for ConfigValue property accessors."""

    def test_is_none_true_for_none_value(self) -> None:
        """is_none returns True for None value."""
        cv = ConfigValue(key="k", value=None, source=ConfigSource.DEFAULT)
        assert cv.is_none is True

    def test_is_none_false_for_value(self) -> None:
        """is_none returns False for non-None value."""
        cv = ConfigValue(key="k", value="test", source=ConfigSource.ENV)
        assert cv.is_none is False

    def test_is_empty_true_for_none(self) -> None:
        """is_empty returns True for None."""
        cv = ConfigValue(key="k", value=None, source=ConfigSource.DEFAULT)
        assert cv.is_empty is True

    def test_is_empty_true_for_empty_string(self) -> None:
        """is_empty returns True for empty string."""
        cv = ConfigValue(key="k", value="", source=ConfigSource.ENV)
        assert cv.is_empty is True

    def test_is_empty_false_for_value(self) -> None:
        """is_empty returns False for non-empty value."""
        cv = ConfigValue(key="k", value="test", source=ConfigSource.ENV)
        assert cv.is_empty is False

    def test_raw_returns_value_as_is(self) -> None:
        """raw property returns value unchanged."""
        cv = ConfigValue(key="k", value=42, source=ConfigSource.ENV)
        assert cv.raw == 42


class TestConfigValueAsString:
    """Tests for as_string() type coercion."""

    def test_as_string_from_string(self) -> None:
        """String value returned as-is."""
        cv = ConfigValue(key="k", value="hello", source=ConfigSource.ENV)
        assert cv.as_string() == "hello"

    def test_as_string_from_int(self) -> None:
        """Integer converted to string."""
        cv = ConfigValue(key="k", value=42, source=ConfigSource.ENV)
        assert cv.as_string() == "42"

    def test_as_string_from_bool(self) -> None:
        """Boolean converted to string."""
        cv = ConfigValue(key="k", value=True, source=ConfigSource.ENV)
        assert cv.as_string() == "True"

    def test_as_string_none_returns_default(self) -> None:
        """None value returns default."""
        cv = ConfigValue(key="k", value=None, source=ConfigSource.DEFAULT)
        assert cv.as_string("default") == "default"

    def test_as_string_none_returns_empty_by_default(self) -> None:
        """None value returns empty string by default."""
        cv = ConfigValue(key="k", value=None, source=ConfigSource.DEFAULT)
        assert cv.as_string() == ""


class TestConfigValueAsBool:
    """Tests for as_bool() type coercion (AC-009.4)."""

    def test_as_bool_from_true_string(self) -> None:
        """'true' string converted to True."""
        cv = ConfigValue(key="k", value="true", source=ConfigSource.ENV)
        assert cv.as_bool() is True

    def test_as_bool_from_true_uppercase(self) -> None:
        """'TRUE' string converted to True."""
        cv = ConfigValue(key="k", value="TRUE", source=ConfigSource.ENV)
        assert cv.as_bool() is True

    def test_as_bool_from_yes_string(self) -> None:
        """'yes' string converted to True."""
        cv = ConfigValue(key="k", value="yes", source=ConfigSource.ENV)
        assert cv.as_bool() is True

    def test_as_bool_from_yes_uppercase(self) -> None:
        """'YES' string converted to True."""
        cv = ConfigValue(key="k", value="YES", source=ConfigSource.ENV)
        assert cv.as_bool() is True

    def test_as_bool_from_one_string(self) -> None:
        """'1' string converted to True."""
        cv = ConfigValue(key="k", value="1", source=ConfigSource.ENV)
        assert cv.as_bool() is True

    def test_as_bool_from_on_string(self) -> None:
        """'on' string converted to True."""
        cv = ConfigValue(key="k", value="on", source=ConfigSource.ENV)
        assert cv.as_bool() is True

    def test_as_bool_from_false_string(self) -> None:
        """'false' string converted to False."""
        cv = ConfigValue(key="k", value="false", source=ConfigSource.ENV)
        assert cv.as_bool() is False

    def test_as_bool_from_no_string(self) -> None:
        """'no' string converted to False."""
        cv = ConfigValue(key="k", value="no", source=ConfigSource.ENV)
        assert cv.as_bool() is False

    def test_as_bool_from_zero_string(self) -> None:
        """'0' string converted to False."""
        cv = ConfigValue(key="k", value="0", source=ConfigSource.ENV)
        assert cv.as_bool() is False

    def test_as_bool_from_bool_true(self) -> None:
        """Boolean True returned as-is."""
        cv = ConfigValue(key="k", value=True, source=ConfigSource.ENV)
        assert cv.as_bool() is True

    def test_as_bool_from_bool_false(self) -> None:
        """Boolean False returned as-is."""
        cv = ConfigValue(key="k", value=False, source=ConfigSource.ENV)
        assert cv.as_bool() is False

    def test_as_bool_from_int_nonzero(self) -> None:
        """Non-zero integer converted to True."""
        cv = ConfigValue(key="k", value=1, source=ConfigSource.ENV)
        assert cv.as_bool() is True
        cv2 = ConfigValue(key="k", value=42, source=ConfigSource.ENV)
        assert cv2.as_bool() is True

    def test_as_bool_from_int_zero(self) -> None:
        """Zero integer converted to False."""
        cv = ConfigValue(key="k", value=0, source=ConfigSource.ENV)
        assert cv.as_bool() is False

    def test_as_bool_none_returns_default(self) -> None:
        """None value returns default."""
        cv = ConfigValue(key="k", value=None, source=ConfigSource.DEFAULT)
        assert cv.as_bool(default=True) is True

    def test_as_bool_unrecognized_returns_false(self) -> None:
        """Unrecognized string value returns False (not in truthy set)."""
        cv = ConfigValue(key="k", value="maybe", source=ConfigSource.ENV)
        # "maybe" is not in truthy set ("true", "1", "yes", "on")
        # so it returns False, not the default
        assert cv.as_bool(default=True) is False

    def test_as_bool_with_whitespace(self) -> None:
        """Whitespace around value is stripped."""
        cv = ConfigValue(key="k", value="  true  ", source=ConfigSource.ENV)
        assert cv.as_bool() is True


class TestConfigValueAsInt:
    """Tests for as_int() type coercion."""

    def test_as_int_from_int(self) -> None:
        """Integer returned as-is."""
        cv = ConfigValue(key="k", value=42, source=ConfigSource.ENV)
        assert cv.as_int() == 42

    def test_as_int_from_string(self) -> None:
        """Numeric string converted to int."""
        cv = ConfigValue(key="k", value="42", source=ConfigSource.ENV)
        assert cv.as_int() == 42

    def test_as_int_from_negative_string(self) -> None:
        """Negative numeric string converted to int."""
        cv = ConfigValue(key="k", value="-10", source=ConfigSource.ENV)
        assert cv.as_int() == -10

    def test_as_int_none_returns_default(self) -> None:
        """None value returns default."""
        cv = ConfigValue(key="k", value=None, source=ConfigSource.DEFAULT)
        assert cv.as_int(default=99) == 99

    def test_as_int_invalid_returns_default(self) -> None:
        """Invalid string returns default."""
        cv = ConfigValue(key="k", value="not-a-number", source=ConfigSource.ENV)
        assert cv.as_int(default=0) == 0

    def test_as_int_float_string_returns_default(self) -> None:
        """Float string returns default (int() fails on float strings)."""
        cv = ConfigValue(key="k", value="3.14", source=ConfigSource.ENV)
        assert cv.as_int(default=0) == 0

    def test_as_int_from_bool(self) -> None:
        """Boolean converts to int (True=1, False=0)."""
        cv_true = ConfigValue(key="k", value=True, source=ConfigSource.ENV)
        cv_false = ConfigValue(key="k", value=False, source=ConfigSource.ENV)
        # Bool is subclass of int, int(True)=1, int(False)=0
        assert cv_true.as_int() == 1
        assert cv_false.as_int() == 0


class TestConfigValueAsFloat:
    """Tests for as_float() type coercion."""

    def test_as_float_from_float(self) -> None:
        """Float returned as-is."""
        cv = ConfigValue(key="k", value=3.14, source=ConfigSource.ENV)
        assert cv.as_float() == 3.14

    def test_as_float_from_int(self) -> None:
        """Integer converted to float."""
        cv = ConfigValue(key="k", value=42, source=ConfigSource.ENV)
        assert cv.as_float() == 42.0

    def test_as_float_from_string(self) -> None:
        """Numeric string converted to float."""
        cv = ConfigValue(key="k", value="3.14", source=ConfigSource.ENV)
        assert cv.as_float() == 3.14

    def test_as_float_from_int_string(self) -> None:
        """Integer string converted to float."""
        cv = ConfigValue(key="k", value="42", source=ConfigSource.ENV)
        assert cv.as_float() == 42.0

    def test_as_float_none_returns_default(self) -> None:
        """None value returns default."""
        cv = ConfigValue(key="k", value=None, source=ConfigSource.DEFAULT)
        assert cv.as_float(default=1.5) == 1.5

    def test_as_float_invalid_returns_default(self) -> None:
        """Invalid string returns default."""
        cv = ConfigValue(key="k", value="not-a-number", source=ConfigSource.ENV)
        assert cv.as_float(default=0.0) == 0.0

    def test_as_float_from_bool(self) -> None:
        """Boolean converts to float (True=1.0, False=0.0)."""
        cv_true = ConfigValue(key="k", value=True, source=ConfigSource.ENV)
        cv_false = ConfigValue(key="k", value=False, source=ConfigSource.ENV)
        # Bool is subclass of int, float(True)=1.0, float(False)=0.0
        assert cv_true.as_float() == 1.0
        assert cv_false.as_float() == 0.0


class TestConfigValueAsList:
    """Tests for as_list() type coercion (AC-009.4)."""

    def test_as_list_from_comma_separated(self) -> None:
        """Comma-separated string split into list."""
        cv = ConfigValue(key="k", value="a,b,c", source=ConfigSource.ENV)
        assert cv.as_list() == ["a", "b", "c"]

    def test_as_list_from_comma_separated_with_spaces(self) -> None:
        """Spaces around items are stripped."""
        cv = ConfigValue(key="k", value="a, b , c", source=ConfigSource.ENV)
        assert cv.as_list() == ["a", "b", "c"]

    def test_as_list_from_single_item(self) -> None:
        """Single item returns single-element list."""
        cv = ConfigValue(key="k", value="single", source=ConfigSource.ENV)
        assert cv.as_list() == ["single"]

    def test_as_list_from_list(self) -> None:
        """List value returned with string conversion."""
        cv = ConfigValue(key="k", value=["a", "b", "c"], source=ConfigSource.ENV)
        assert cv.as_list() == ["a", "b", "c"]

    def test_as_list_from_list_with_numbers(self) -> None:
        """List with numbers converted to strings."""
        cv = ConfigValue(key="k", value=[1, 2, 3], source=ConfigSource.ENV)
        assert cv.as_list() == ["1", "2", "3"]

    def test_as_list_custom_separator(self) -> None:
        """Custom separator splits correctly."""
        cv = ConfigValue(key="k", value="a;b;c", source=ConfigSource.ENV)
        assert cv.as_list(separator=";") == ["a", "b", "c"]

    def test_as_list_none_returns_default(self) -> None:
        """None value returns default."""
        cv = ConfigValue(key="k", value=None, source=ConfigSource.DEFAULT)
        assert cv.as_list(default=["x"]) == ["x"]

    def test_as_list_none_returns_empty_by_default(self) -> None:
        """None value returns empty list by default."""
        cv = ConfigValue(key="k", value=None, source=ConfigSource.DEFAULT)
        assert cv.as_list() == []

    def test_as_list_empty_string_returns_default(self) -> None:
        """Empty string returns default."""
        cv = ConfigValue(key="k", value="", source=ConfigSource.ENV)
        assert cv.as_list(default=["x"]) == ["x"]

    def test_as_list_whitespace_only_returns_default(self) -> None:
        """Whitespace-only string returns default."""
        cv = ConfigValue(key="k", value="   ", source=ConfigSource.ENV)
        assert cv.as_list() == []

    def test_as_list_from_single_non_string(self) -> None:
        """Single non-string/non-list value wrapped in list."""
        cv = ConfigValue(key="k", value=42, source=ConfigSource.ENV)
        assert cv.as_list() == ["42"]

    def test_as_list_filters_empty_items(self) -> None:
        """Empty items from split are filtered out."""
        cv = ConfigValue(key="k", value="a,,b,,,c", source=ConfigSource.ENV)
        assert cv.as_list() == ["a", "b", "c"]


class TestConfigValueAsDict:
    """Tests for as_dict() type coercion."""

    def test_as_dict_from_dict(self) -> None:
        """Dictionary returned as copy."""
        original = {"a": 1, "b": 2}
        cv = ConfigValue(key="k", value=original, source=ConfigSource.ENV)
        result = cv.as_dict()
        assert result == {"a": 1, "b": 2}
        # Should be a copy, not the same object
        assert result is not original

    def test_as_dict_none_returns_default(self) -> None:
        """None value returns default."""
        cv = ConfigValue(key="k", value=None, source=ConfigSource.DEFAULT)
        assert cv.as_dict(default={"x": 1}) == {"x": 1}

    def test_as_dict_none_returns_empty_by_default(self) -> None:
        """None value returns empty dict by default."""
        cv = ConfigValue(key="k", value=None, source=ConfigSource.DEFAULT)
        assert cv.as_dict() == {}

    def test_as_dict_non_dict_returns_default(self) -> None:
        """Non-dict value returns default."""
        cv = ConfigValue(key="k", value="not-a-dict", source=ConfigSource.ENV)
        assert cv.as_dict(default={"x": 1}) == {"x": 1}


class TestConfigValueOrDefault:
    """Tests for or_default() method."""

    def test_or_default_with_value_returns_self(self) -> None:
        """Non-None value returns self."""
        cv = ConfigValue(key="k", value="test", source=ConfigSource.ENV)
        result = cv.or_default("fallback")
        assert result is cv

    def test_or_default_with_none_returns_new_value(self) -> None:
        """None value returns new ConfigValue with default."""
        cv = ConfigValue(key="k", value=None, source=ConfigSource.ENV)
        result = cv.or_default("fallback")
        assert result.value == "fallback"
        assert result.source == ConfigSource.DEFAULT
        assert result.key == "k"


class TestConfigValueFactoryMethods:
    """Tests for factory methods."""

    def test_of_creates_value(self) -> None:
        """of() factory creates ConfigValue."""
        cv = ConfigValue.of("debug", True, ConfigSource.ENV)
        assert cv.key == "debug"
        assert cv.value is True
        assert cv.source == ConfigSource.ENV

    def test_of_default_source(self) -> None:
        """of() uses DEFAULT source by default."""
        cv = ConfigValue.of("debug", True)
        assert cv.source == ConfigSource.DEFAULT

    def test_empty_creates_none_value(self) -> None:
        """empty() creates ConfigValue with None."""
        cv = ConfigValue.empty("missing")
        assert cv.key == "missing"
        assert cv.value is None
        assert cv.is_none is True

    def test_empty_with_source(self) -> None:
        """empty() accepts source parameter."""
        cv = ConfigValue.empty("missing", ConfigSource.PROJECT)
        assert cv.source == ConfigSource.PROJECT


class TestConfigValueImmutability:
    """Tests for immutability (AC-009.5)."""

    def test_frozen_cannot_modify_value(self) -> None:
        """Frozen dataclass prevents attribute modification."""
        cv = ConfigValue(key="k", value="test", source=ConfigSource.ENV)
        with pytest.raises(AttributeError):
            cv.value = "modified"  # type: ignore[misc]

    def test_equality_by_value(self) -> None:
        """Two ConfigValues with same data are equal."""
        cv1 = ConfigValue(key="k", value="test", source=ConfigSource.ENV)
        cv2 = ConfigValue(key="k", value="test", source=ConfigSource.ENV)
        assert cv1 == cv2

    def test_hash_consistency(self) -> None:
        """ConfigValues can be used in sets/dicts."""
        cv1 = ConfigValue(key="k", value="test", source=ConfigSource.ENV)
        cv2 = ConfigValue(key="k", value="test", source=ConfigSource.ENV)
        cv_set = {cv1, cv2}
        assert len(cv_set) == 1


class TestConfigValueStringRepresentation:
    """Tests for string representations."""

    def test_str_includes_key_value_source(self) -> None:
        """str() includes key, value, and source."""
        cv = ConfigValue(key="debug", value="true", source=ConfigSource.ENV)
        result = str(cv)
        assert "debug" in result
        assert "true" in result
        assert "env" in result.lower()

    def test_repr_includes_class_name(self) -> None:
        """repr() includes class name."""
        cv = ConfigValue(key="k", value="test", source=ConfigSource.ENV)
        assert "ConfigValue" in repr(cv)


class TestConfigValueBoolConversion:
    """Tests for __bool__ dunder method."""

    def test_bool_true_for_non_empty_value(self) -> None:
        """Non-empty value is truthy."""
        cv = ConfigValue(key="k", value="test", source=ConfigSource.ENV)
        assert bool(cv) is True

    def test_bool_false_for_none(self) -> None:
        """None value is falsy."""
        cv = ConfigValue(key="k", value=None, source=ConfigSource.DEFAULT)
        assert bool(cv) is False

    def test_bool_false_for_empty_string(self) -> None:
        """Empty string is falsy."""
        cv = ConfigValue(key="k", value="", source=ConfigSource.ENV)
        assert bool(cv) is False
