# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for lifecycle_dir_resolver.

Tests verify 3-tier resolution precedence:
    - Tier 1: JERRY_LIFECYCLE_DIR env var (highest priority)
    - Tier 2: Config-provided value
    - Tier 3: Platform default (~/.jerry/local/ or %APPDATA%/jerry/local/)

References:
    - PROJ-004: Context Resilience — lifecycle file location mismatch fix
"""

from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import patch

from src.infrastructure.adapters.configuration.lifecycle_dir_resolver import (
    _platform_default_lifecycle_dir,
    resolve_lifecycle_dir,
)


class TestResolveLifecycleDirEnvVar:
    """Tier 1: JERRY_LIFECYCLE_DIR env var takes precedence."""

    def test_env_var_takes_precedence(self, tmp_path: Path) -> None:
        """Env var wins over config value and platform default."""
        env_dir = str(tmp_path / "from-env")
        config_dir = str(tmp_path / "from-config")
        with patch.dict(os.environ, {"JERRY_LIFECYCLE_DIR": env_dir}):
            result = resolve_lifecycle_dir(config_value=config_dir)
        assert result == Path(env_dir).resolve()

    def test_env_var_with_tilde_expanded(self) -> None:
        """Env var with ~ gets expanded."""
        with patch.dict(os.environ, {"JERRY_LIFECYCLE_DIR": "~/my-jerry"}):
            result = resolve_lifecycle_dir()
        assert result == Path.home() / "my-jerry"

    def test_config_value_ignored_when_env_set(self, tmp_path: Path) -> None:
        """Config value is ignored when env var is set."""
        env_dir = str(tmp_path / "env-wins")
        with patch.dict(os.environ, {"JERRY_LIFECYCLE_DIR": env_dir}):
            result = resolve_lifecycle_dir(config_value="/some/config/path")
        assert result == Path(env_dir).resolve()


class TestResolveLifecycleDirConfig:
    """Tier 2: Config value used when no env var."""

    def test_config_value_used_when_no_env(self, tmp_path: Path) -> None:
        """Config value is used when JERRY_LIFECYCLE_DIR is not set."""
        config_dir = str(tmp_path / "from-config")
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("JERRY_LIFECYCLE_DIR", None)
            result = resolve_lifecycle_dir(config_value=config_dir)
        assert result == Path(config_dir).resolve()

    def test_tilde_expanded_in_config(self) -> None:
        """Config value with ~ gets expanded."""
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("JERRY_LIFECYCLE_DIR", None)
            result = resolve_lifecycle_dir(config_value="~/jerry-config")
        assert result == Path.home() / "jerry-config"


class TestResolveLifecycleDirPlatformDefault:
    """Tier 3: Platform default when no env var or config."""

    def test_platform_default_when_no_env_or_config(self) -> None:
        """Falls back to platform-appropriate default when nothing is set."""
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("JERRY_LIFECYCLE_DIR", None)
            result = resolve_lifecycle_dir()
        expected = _platform_default_lifecycle_dir()
        assert result == expected

    def test_returns_absolute_path(self) -> None:
        """All tiers return absolute paths."""
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("JERRY_LIFECYCLE_DIR", None)
            result = resolve_lifecycle_dir()
        assert result.is_absolute()

    def test_windows_platform_default(self) -> None:
        """On Windows with APPDATA, uses %APPDATA%/jerry/local/."""
        with (
            patch(
                "src.infrastructure.adapters.configuration.lifecycle_dir_resolver.sys"
            ) as mock_sys,
            patch.dict(os.environ, {"APPDATA": "C:\\Users\\test\\AppData\\Roaming"}),
        ):
            mock_sys.platform = "win32"
            result = _platform_default_lifecycle_dir()
        assert result == Path("C:\\Users\\test\\AppData\\Roaming") / "jerry" / "local"

    def test_missing_appdata_on_windows(self) -> None:
        """On Windows with no APPDATA, falls back to Path.home()."""
        with (
            patch(
                "src.infrastructure.adapters.configuration.lifecycle_dir_resolver.sys"
            ) as mock_sys,
            patch.dict(os.environ, {}, clear=False),
        ):
            os.environ.pop("APPDATA", None)
            mock_sys.platform = "win32"
            result = _platform_default_lifecycle_dir()
        assert result == Path.home() / ".jerry" / "local"
