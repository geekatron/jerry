# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for OutputResolver application service.

Tests cover:
    - GH #192 / REQ-OBP-003: OutputResolver application service specification
    - REQ-OBP-001: Config-first resolution (output.base_path from config)
    - REQ-OBP-002: JERRY_PROJECT fallback (projects/{JERRY_PROJECT}/)
    - REQ-OBP-002c: Terminal fallback (work/)
    - REQ-OBP-003a: Trailing slash guarantee
    - REQ-OBP-003h: ValueError propagation from OutputBasePath
    - EC-008, EC-021: Null byte in config value propagates ValueError
    - EC-025: Whitespace-only config value treated as set (not fallback)

Test Categories:
    - Happy path: Config priority, JERRY_PROJECT fallback, terminal fallback
    - Negative: ValueError propagation for null bytes
    - Edge cases: Empty config, None config, whitespace-only, trailing slash
"""

from __future__ import annotations

import os
from typing import Any
from unittest.mock import patch

import pytest

from src.configuration.application.services.output_resolver import OutputResolver


class StubConfigProvider:
    """Stub config provider for testing.

    Implements IConfigurationProvider protocol (structural typing).
    """

    def __init__(self, values: dict[str, Any] | None = None) -> None:
        self._values = values or {}

    def get(self, key: str) -> Any | None:
        """Get a configuration value by key."""
        return self._values.get(key)

    def get_string(self, key: str, default: str = "") -> str:
        """Get a configuration value as string."""
        val = self._values.get(key)
        return str(val) if val is not None else default

    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get a configuration value as boolean."""
        val = self._values.get(key)
        return bool(val) if val is not None else default

    def get_int(self, key: str, default: int = 0) -> int:
        """Get a configuration value as integer."""
        val = self._values.get(key)
        return int(val) if val is not None else default


class TestOutputResolverConfigPriority:
    """Tests for config-first resolution (REQ-OBP-001)."""

    def test_config_value_takes_priority(self) -> None:
        """When output.base_path is set in config, it takes priority over all fallbacks."""
        config = StubConfigProvider({"output.base_path": "custom/output"})
        resolver = OutputResolver(config_provider=config)

        with patch.dict(os.environ, {"JERRY_PROJECT": "PROJ-001"}, clear=False):
            result = resolver.resolve()

        assert result == "custom/output/"

    def test_config_value_with_trailing_slash(self) -> None:
        """Config value already ending in slash is not double-slashed."""
        config = StubConfigProvider({"output.base_path": "custom/output/"})
        resolver = OutputResolver(config_provider=config)
        result = resolver.resolve()
        assert result == "custom/output/"

    def test_config_value_absolute_path(self) -> None:
        """Absolute path in config is accepted per ADR INV-3."""
        config = StubConfigProvider({"output.base_path": "/tmp/jerry-output"})
        resolver = OutputResolver(config_provider=config)
        result = resolver.resolve()
        assert result == "/tmp/jerry-output/"

    def test_config_value_single_directory(self) -> None:
        """Single directory name in config is accepted."""
        config = StubConfigProvider({"output.base_path": "output"})
        resolver = OutputResolver(config_provider=config)
        result = resolver.resolve()
        assert result == "output/"


class TestOutputResolverJerryProjectFallback:
    """Tests for JERRY_PROJECT fallback (REQ-OBP-002)."""

    def test_jerry_project_fallback_when_config_is_none(self) -> None:
        """Falls back to projects/{JERRY_PROJECT}/ when config returns None."""
        config = StubConfigProvider({})
        resolver = OutputResolver(config_provider=config)

        with patch.dict(os.environ, {"JERRY_PROJECT": "PROJ-042"}, clear=False):
            result = resolver.resolve()

        assert result == "projects/PROJ-042/"

    def test_jerry_project_fallback_when_config_is_empty(self) -> None:
        """Falls back to JERRY_PROJECT when config value is empty string."""
        config = StubConfigProvider({"output.base_path": ""})
        resolver = OutputResolver(config_provider=config)

        with patch.dict(os.environ, {"JERRY_PROJECT": "PROJ-007"}, clear=False):
            result = resolver.resolve()

        assert result == "projects/PROJ-007/"

    def test_jerry_project_with_slug(self) -> None:
        """JERRY_PROJECT with slug suffix produces correct path."""
        config = StubConfigProvider({})
        resolver = OutputResolver(config_provider=config)

        with patch.dict(os.environ, {"JERRY_PROJECT": "PROJ-021-output-base-path"}, clear=False):
            result = resolver.resolve()

        assert result == "projects/PROJ-021-output-base-path/"


class TestOutputResolverTerminalFallback:
    """Tests for terminal fallback to work/ (REQ-OBP-002c)."""

    def test_terminal_fallback_when_no_config_no_project(self) -> None:
        """Falls back to work/ when neither config nor JERRY_PROJECT is set."""
        config = StubConfigProvider({})
        resolver = OutputResolver(config_provider=config)

        env = {k: v for k, v in os.environ.items() if k != "JERRY_PROJECT"}
        with patch.dict(os.environ, env, clear=True):
            result = resolver.resolve()

        assert result == "work/"

    def test_terminal_fallback_when_config_none_and_project_empty(self) -> None:
        """Falls back to work/ when config is None and JERRY_PROJECT is empty string."""
        config = StubConfigProvider({})
        resolver = OutputResolver(config_provider=config)

        with patch.dict(os.environ, {"JERRY_PROJECT": ""}, clear=False):
            result = resolver.resolve()

        assert result == "work/"

    def test_terminal_fallback_when_config_empty_and_no_project(self) -> None:
        """Falls back to work/ when config is empty string and no JERRY_PROJECT."""
        config = StubConfigProvider({"output.base_path": ""})
        resolver = OutputResolver(config_provider=config)

        env = {k: v for k, v in os.environ.items() if k != "JERRY_PROJECT"}
        with patch.dict(os.environ, env, clear=True):
            result = resolver.resolve()

        assert result == "work/"


class TestOutputResolverTrailingSlash:
    """Tests for trailing slash guarantee (REQ-OBP-003a)."""

    def test_adds_trailing_slash_to_config_value(self) -> None:
        """Config value without trailing slash gets one added."""
        config = StubConfigProvider({"output.base_path": "my-output"})
        resolver = OutputResolver(config_provider=config)
        assert resolver.resolve() == "my-output/"

    def test_preserves_existing_trailing_slash(self) -> None:
        """Config value with trailing slash is not double-slashed."""
        config = StubConfigProvider({"output.base_path": "my-output/"})
        resolver = OutputResolver(config_provider=config)
        assert resolver.resolve() == "my-output/"

    def test_jerry_project_path_has_trailing_slash(self) -> None:
        """JERRY_PROJECT fallback path always ends with /."""
        config = StubConfigProvider({})
        resolver = OutputResolver(config_provider=config)

        with patch.dict(os.environ, {"JERRY_PROJECT": "PROJ-001"}, clear=False):
            result = resolver.resolve()

        assert result.endswith("/")

    def test_terminal_fallback_has_trailing_slash(self) -> None:
        """Terminal fallback 'work/' ends with /."""
        config = StubConfigProvider({})
        resolver = OutputResolver(config_provider=config)

        env = {k: v for k, v in os.environ.items() if k != "JERRY_PROJECT"}
        with patch.dict(os.environ, env, clear=True):
            result = resolver.resolve()

        assert result == "work/"
        assert result.endswith("/")


class TestOutputResolverValueErrorPropagation:
    """Tests for ValueError propagation from OutputBasePath (REQ-OBP-003h)."""

    def test_null_byte_in_config_raises_value_error(self) -> None:
        """Config value with null byte propagates ValueError (EC-008, EC-021)."""
        config = StubConfigProvider({"output.base_path": "work/\x00evil"})
        resolver = OutputResolver(config_provider=config)

        with pytest.raises(ValueError, match="null bytes"):
            resolver.resolve()

    def test_only_null_byte_in_config_raises_value_error(self) -> None:
        """Config value that is just a null byte propagates ValueError."""
        config = StubConfigProvider({"output.base_path": "\x00"})
        resolver = OutputResolver(config_provider=config)

        with pytest.raises(ValueError, match="null bytes"):
            resolver.resolve()


class TestOutputResolverEdgeCases:
    """Edge case tests."""

    def test_whitespace_only_config_treated_as_set(self) -> None:
        """Whitespace-only config value is treated as set, not fallback (EC-025)."""
        config = StubConfigProvider({"output.base_path": "   "})
        resolver = OutputResolver(config_provider=config)

        with patch.dict(os.environ, {"JERRY_PROJECT": "PROJ-001"}, clear=False):
            result = resolver.resolve()

        # Whitespace is non-empty, so it's treated as a set value
        assert result == "   /"

    def test_config_value_with_spaces_in_path(self) -> None:
        """Paths with spaces are valid."""
        config = StubConfigProvider({"output.base_path": "my output/dir"})
        resolver = OutputResolver(config_provider=config)
        assert resolver.resolve() == "my output/dir/"

    def test_config_value_integer_coerced_to_string(self) -> None:
        """Non-string config value is coerced via str()."""
        config = StubConfigProvider({"output.base_path": 42})
        resolver = OutputResolver(config_provider=config)
        assert resolver.resolve() == "42/"

    def test_resolve_is_idempotent(self) -> None:
        """Multiple calls to resolve() return the same result."""
        config = StubConfigProvider({"output.base_path": "stable/"})
        resolver = OutputResolver(config_provider=config)
        assert resolver.resolve() == resolver.resolve()

    def test_resolver_does_not_create_directories(self) -> None:
        """Resolver returns a path string; it does not create filesystem directories."""
        config = StubConfigProvider({"output.base_path": "nonexistent/deep/path"})
        resolver = OutputResolver(config_provider=config)
        result = resolver.resolve()
        assert result == "nonexistent/deep/path/"
        # No assertion on filesystem — resolver is pure path resolution
