"""Unit tests for EnvConfigAdapter.

Tests verify:
- AC-013.1: Maps env vars with JERRY_ prefix to config keys
- AC-013.2: Uses __ for nested keys (e.g., JERRY_LOGGING__LEVEL)
- AC-013.3: Auto-converts string values to bool/int/float/list
- AC-013.4: Implements IConfigurationProvider port interface
- AC-013.5: Unit tests for all type conversions
- AC-013.6: Unit tests for key mapping edge cases

References:
    - WI-013: Environment Variable Adapter work item
    - PROJ-004-e-004: Configuration Precedence research
"""

from __future__ import annotations

import os
from unittest.mock import patch

import pytest

from src.infrastructure.adapters.configuration.env_config_adapter import (
    EnvConfigAdapter,
)


class TestEnvConfigAdapterInit:
    """Tests for EnvConfigAdapter initialization."""

    def test_init_with_default_prefix(self) -> None:
        """Default prefix is JERRY_."""
        with patch.dict(os.environ, clear=True):
            adapter = EnvConfigAdapter()
            assert adapter.prefix == "JERRY_"

    def test_init_with_custom_prefix(self) -> None:
        """Custom prefix is respected."""
        with patch.dict(os.environ, clear=True):
            adapter = EnvConfigAdapter(prefix="MYAPP_")
            assert adapter.prefix == "MYAPP_"


class TestEnvConfigAdapterKeyMapping:
    """Tests for environment variable to config key mapping."""

    def test_simple_key_mapping(self) -> None:
        """Simple env var maps to lowercase key."""
        with patch.dict(os.environ, {"JERRY_LEVEL": "INFO"}, clear=True):
            adapter = EnvConfigAdapter()
            assert adapter.get("level") == "INFO"

    def test_nested_key_mapping(self) -> None:
        """Env var with __ maps to nested key with dots."""
        with patch.dict(os.environ, {"JERRY_LOGGING__LEVEL": "DEBUG"}, clear=True):
            adapter = EnvConfigAdapter()
            assert adapter.get("logging.level") == "DEBUG"

    def test_deeply_nested_key_mapping(self) -> None:
        """Multiple __ map to multiple dots."""
        with patch.dict(
            os.environ, {"JERRY_A__B__C__D": "value"}, clear=True
        ):
            adapter = EnvConfigAdapter()
            assert adapter.get("a.b.c.d") == "value"

    def test_non_prefixed_vars_ignored(self) -> None:
        """Environment variables without prefix are ignored."""
        with patch.dict(
            os.environ,
            {"JERRY_INCLUDED": "yes", "OTHER_VAR": "ignored"},
            clear=True,
        ):
            adapter = EnvConfigAdapter()
            assert adapter.has("included")
            assert not adapter.has("other_var")

    def test_env_to_config_key_method(self) -> None:
        """Test _env_to_config_key directly."""
        adapter = EnvConfigAdapter()
        assert adapter._env_to_config_key("JERRY_LOGGING__LEVEL") == "logging.level"
        assert adapter._env_to_config_key("JERRY_SIMPLE") == "simple"
        assert adapter._env_to_config_key("JERRY_A__B__C") == "a.b.c"


class TestEnvConfigAdapterTypeConversion:
    """Tests for automatic type conversion."""

    def test_boolean_true_values(self) -> None:
        """Boolean true values are converted."""
        true_values = ["true", "True", "TRUE", "yes", "Yes", "on", "ON", "1"]
        for i, val in enumerate(true_values):
            with patch.dict(os.environ, {f"JERRY_BOOL{i}": val}, clear=True):
                adapter = EnvConfigAdapter()
                assert adapter.get(f"bool{i}") is True, f"Failed for value: {val}"

    def test_boolean_false_values(self) -> None:
        """Boolean false values are converted."""
        false_values = ["false", "False", "FALSE", "no", "No", "off", "OFF", "0"]
        for i, val in enumerate(false_values):
            with patch.dict(os.environ, {f"JERRY_BOOL{i}": val}, clear=True):
                adapter = EnvConfigAdapter()
                assert adapter.get(f"bool{i}") is False, f"Failed for value: {val}"

    def test_integer_conversion(self) -> None:
        """Integer values are converted."""
        with patch.dict(os.environ, {"JERRY_COUNT": "42"}, clear=True):
            adapter = EnvConfigAdapter()
            assert adapter.get("count") == 42
            assert isinstance(adapter.get("count"), int)

    def test_negative_integer_conversion(self) -> None:
        """Negative integers are converted."""
        with patch.dict(os.environ, {"JERRY_OFFSET": "-10"}, clear=True):
            adapter = EnvConfigAdapter()
            assert adapter.get("offset") == -10

    def test_float_conversion(self) -> None:
        """Float values are converted."""
        with patch.dict(os.environ, {"JERRY_RATIO": "3.14"}, clear=True):
            adapter = EnvConfigAdapter()
            assert adapter.get("ratio") == 3.14
            assert isinstance(adapter.get("ratio"), float)

    def test_json_array_conversion(self) -> None:
        """JSON array values are converted."""
        with patch.dict(
            os.environ, {"JERRY_LIST": '["a", "b", "c"]'}, clear=True
        ):
            adapter = EnvConfigAdapter()
            assert adapter.get("list") == ["a", "b", "c"]

    def test_json_object_conversion(self) -> None:
        """JSON object values are converted."""
        with patch.dict(
            os.environ, {"JERRY_CONFIG": '{"key": "value"}'}, clear=True
        ):
            adapter = EnvConfigAdapter()
            assert adapter.get("config") == {"key": "value"}

    def test_comma_separated_list_conversion(self) -> None:
        """Comma-separated values are converted to list."""
        with patch.dict(os.environ, {"JERRY_ITEMS": "a, b, c"}, clear=True):
            adapter = EnvConfigAdapter()
            assert adapter.get("items") == ["a", "b", "c"]

    def test_string_preserved_for_non_matching(self) -> None:
        """Non-matching values remain as strings."""
        with patch.dict(os.environ, {"JERRY_TEXT": "hello world"}, clear=True):
            adapter = EnvConfigAdapter()
            assert adapter.get("text") == "hello world"


class TestEnvConfigAdapterTypedGetters:
    """Tests for typed getter methods."""

    def test_get_string(self) -> None:
        """get_string returns string value."""
        with patch.dict(os.environ, {"JERRY_NAME": "test"}, clear=True):
            adapter = EnvConfigAdapter()
            assert adapter.get_string("name") == "test"
            assert adapter.get_string("missing", "default") == "default"

    def test_get_bool(self) -> None:
        """get_bool returns boolean value."""
        with patch.dict(os.environ, {"JERRY_ENABLED": "true"}, clear=True):
            adapter = EnvConfigAdapter()
            assert adapter.get_bool("enabled") is True
            assert adapter.get_bool("missing", False) is False

    def test_get_int(self) -> None:
        """get_int returns integer value."""
        with patch.dict(os.environ, {"JERRY_COUNT": "42"}, clear=True):
            adapter = EnvConfigAdapter()
            assert adapter.get_int("count") == 42
            assert adapter.get_int("missing", 10) == 10

    def test_get_list(self) -> None:
        """get_list returns list value."""
        with patch.dict(os.environ, {"JERRY_ITEMS": "a,b,c"}, clear=True):
            adapter = EnvConfigAdapter()
            assert adapter.get_list("items") == ["a", "b", "c"]
            assert adapter.get_list("missing", ["default"]) == ["default"]


class TestEnvConfigAdapterHas:
    """Tests for has method."""

    def test_has_returns_true_for_existing(self) -> None:
        """has returns True for existing keys."""
        with patch.dict(os.environ, {"JERRY_EXISTS": "value"}, clear=True):
            adapter = EnvConfigAdapter()
            assert adapter.has("exists") is True

    def test_has_returns_false_for_missing(self) -> None:
        """has returns False for missing keys."""
        with patch.dict(os.environ, clear=True):
            adapter = EnvConfigAdapter()
            assert adapter.has("missing") is False


class TestEnvConfigAdapterRefresh:
    """Tests for refresh method."""

    def test_refresh_reloads_environment(self) -> None:
        """refresh picks up new environment variables."""
        with patch.dict(os.environ, {"JERRY_VAR": "old"}, clear=True):
            adapter = EnvConfigAdapter()
            assert adapter.get("var") == "old"

            os.environ["JERRY_VAR"] = "new"
            os.environ["JERRY_NEW"] = "added"
            adapter.refresh()

            assert adapter.get("var") == "new"
            assert adapter.get("new") == "added"


class TestEnvConfigAdapterKeys:
    """Tests for keys method."""

    def test_keys_returns_all_config_keys(self) -> None:
        """keys returns all discovered config keys."""
        with patch.dict(
            os.environ,
            {"JERRY_A": "1", "JERRY_B__C": "2", "OTHER": "ignored"},
            clear=True,
        ):
            adapter = EnvConfigAdapter()
            keys = adapter.keys()
            assert "a" in keys
            assert "b.c" in keys
            assert len(keys) == 2
