"""Unit and integration tests for LayeredConfigAdapter.

Tests verify:
- AC-014.1: Implements IConfigurationProvider port interface
- AC-014.2: Respects precedence order: env > project > root > defaults
- AC-014.3: Loads TOML config files using tomllib (stdlib)
- AC-014.4: Uses AtomicFileAdapter for file reads
- AC-014.5: Gracefully handles missing config files
- AC-014.6: Integration tests verifying precedence

References:
    - WI-014: Layered Config Adapter work item
    - PROJ-004-e-004: Configuration Precedence research
"""

from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import patch

from src.infrastructure.adapters.configuration.layered_config_adapter import (
    LayeredConfigAdapter,
)
from src.infrastructure.adapters.persistence.atomic_file_adapter import (
    AtomicFileAdapter,
)


class TestLayeredConfigAdapterInit:
    """Tests for LayeredConfigAdapter initialization."""

    def test_init_with_defaults_only(self) -> None:
        """Adapter works with only defaults."""
        with patch.dict(os.environ, clear=True):
            adapter = LayeredConfigAdapter(defaults={"key": "value"})
            assert adapter.get("key") == "value"

    def test_init_with_custom_env_prefix(self) -> None:
        """Custom env prefix is respected."""
        with patch.dict(os.environ, {"MYAPP_VAR": "test"}, clear=True):
            adapter = LayeredConfigAdapter(env_prefix="MYAPP_")
            assert adapter.get("var") == "test"

    def test_init_with_custom_file_adapter(self, tmp_path: Path) -> None:
        """Custom file adapter is used."""
        file_adapter = AtomicFileAdapter(lock_dir=tmp_path / "locks")
        with patch.dict(os.environ, clear=True):
            adapter = LayeredConfigAdapter(
                file_adapter=file_adapter,
                defaults={"test": "value"},
            )
            assert adapter.get("test") == "value"


class TestLayeredConfigAdapterPrecedence:
    """Tests for configuration precedence order."""

    def test_env_overrides_all(self, tmp_path: Path) -> None:
        """Environment variables have highest precedence."""
        root_config = tmp_path / "root.toml"
        root_config.write_text('[logging]\nlevel = "INFO"\n', encoding="utf-8")

        project_config = tmp_path / "project.toml"
        project_config.write_text('[logging]\nlevel = "WARNING"\n', encoding="utf-8")

        with patch.dict(os.environ, {"JERRY_LOGGING__LEVEL": "DEBUG"}, clear=True):
            adapter = LayeredConfigAdapter(
                root_config_path=root_config,
                project_config_path=project_config,
                defaults={"logging.level": "ERROR"},
            )
            assert adapter.get("logging.level") == "DEBUG"

    def test_project_overrides_root_and_defaults(self, tmp_path: Path) -> None:
        """Project config overrides root config and defaults."""
        root_config = tmp_path / "root.toml"
        root_config.write_text('[logging]\nlevel = "INFO"\n', encoding="utf-8")

        project_config = tmp_path / "project.toml"
        project_config.write_text('[logging]\nlevel = "WARNING"\n', encoding="utf-8")

        with patch.dict(os.environ, clear=True):
            adapter = LayeredConfigAdapter(
                root_config_path=root_config,
                project_config_path=project_config,
                defaults={"logging.level": "ERROR"},
            )
            assert adapter.get("logging.level") == "WARNING"

    def test_root_overrides_defaults(self, tmp_path: Path) -> None:
        """Root config overrides defaults."""
        root_config = tmp_path / "root.toml"
        root_config.write_text('[logging]\nlevel = "INFO"\n', encoding="utf-8")

        with patch.dict(os.environ, clear=True):
            adapter = LayeredConfigAdapter(
                root_config_path=root_config,
                defaults={"logging.level": "ERROR"},
            )
            assert adapter.get("logging.level") == "INFO"

    def test_defaults_used_when_nothing_else(self) -> None:
        """Defaults are used when no other source has the key."""
        with patch.dict(os.environ, clear=True):
            adapter = LayeredConfigAdapter(defaults={"logging.level": "INFO"})
            assert adapter.get("logging.level") == "INFO"

    def test_none_returned_when_key_missing(self) -> None:
        """None returned when key is in no source."""
        with patch.dict(os.environ, clear=True):
            adapter = LayeredConfigAdapter()
            assert adapter.get("nonexistent") is None


class TestLayeredConfigAdapterToml:
    """Tests for TOML file loading."""

    def test_load_valid_toml(self, tmp_path: Path) -> None:
        """Valid TOML is loaded correctly."""
        config = tmp_path / "config.toml"
        config.write_text(
            """
[jerry]
version = "1.0"

[logging]
level = "DEBUG"
format = "json"
""",
            encoding="utf-8",
        )

        with patch.dict(os.environ, clear=True):
            adapter = LayeredConfigAdapter(root_config_path=config)
            assert adapter.get("jerry.version") == "1.0"
            assert adapter.get("logging.level") == "DEBUG"
            assert adapter.get("logging.format") == "json"

    def test_missing_file_returns_empty(self, tmp_path: Path) -> None:
        """Missing config file is treated as empty."""
        missing_config = tmp_path / "missing.toml"

        with patch.dict(os.environ, clear=True):
            adapter = LayeredConfigAdapter(
                root_config_path=missing_config,
                defaults={"fallback": "value"},
            )
            assert adapter.get("fallback") == "value"

    def test_invalid_toml_returns_empty(self, tmp_path: Path) -> None:
        """Invalid TOML is treated as empty config."""
        config = tmp_path / "invalid.toml"
        config.write_text("this is not valid { toml", encoding="utf-8")

        with patch.dict(os.environ, clear=True):
            adapter = LayeredConfigAdapter(
                root_config_path=config,
                defaults={"fallback": "value"},
            )
            assert adapter.get("fallback") == "value"

    def test_empty_file_returns_empty(self, tmp_path: Path) -> None:
        """Empty config file is treated as empty config."""
        config = tmp_path / "empty.toml"
        config.write_text("", encoding="utf-8")

        with patch.dict(os.environ, clear=True):
            adapter = LayeredConfigAdapter(
                root_config_path=config,
                defaults={"fallback": "value"},
            )
            assert adapter.get("fallback") == "value"


class TestLayeredConfigAdapterTypedGetters:
    """Tests for typed getter methods."""

    def test_get_string(self, tmp_path: Path) -> None:
        """get_string returns string value."""
        config = tmp_path / "config.toml"
        config.write_text('name = "test"', encoding="utf-8")

        with patch.dict(os.environ, clear=True):
            adapter = LayeredConfigAdapter(root_config_path=config)
            assert adapter.get_string("name") == "test"
            assert adapter.get_string("missing", "default") == "default"

    def test_get_bool(self, tmp_path: Path) -> None:
        """get_bool returns boolean value."""
        config = tmp_path / "config.toml"
        config.write_text("enabled = true", encoding="utf-8")

        with patch.dict(os.environ, clear=True):
            adapter = LayeredConfigAdapter(root_config_path=config)
            assert adapter.get_bool("enabled") is True
            assert adapter.get_bool("missing", False) is False

    def test_get_int(self, tmp_path: Path) -> None:
        """get_int returns integer value."""
        config = tmp_path / "config.toml"
        config.write_text("count = 42", encoding="utf-8")

        with patch.dict(os.environ, clear=True):
            adapter = LayeredConfigAdapter(root_config_path=config)
            assert adapter.get_int("count") == 42
            assert adapter.get_int("missing", 10) == 10

    def test_get_float(self, tmp_path: Path) -> None:
        """get_float returns float value."""
        config = tmp_path / "config.toml"
        config.write_text("ratio = 3.14", encoding="utf-8")

        with patch.dict(os.environ, clear=True):
            adapter = LayeredConfigAdapter(root_config_path=config)
            assert adapter.get_float("ratio") == 3.14
            assert adapter.get_float("missing", 1.0) == 1.0

    def test_get_list(self, tmp_path: Path) -> None:
        """get_list returns list value."""
        config = tmp_path / "config.toml"
        config.write_text('items = ["a", "b", "c"]', encoding="utf-8")

        with patch.dict(os.environ, clear=True):
            adapter = LayeredConfigAdapter(root_config_path=config)
            assert adapter.get_list("items") == ["a", "b", "c"]
            assert adapter.get_list("missing", ["default"]) == ["default"]


class TestLayeredConfigAdapterHas:
    """Tests for has method."""

    def test_has_returns_true_for_existing(self, tmp_path: Path) -> None:
        """has returns True for existing keys."""
        config = tmp_path / "config.toml"
        config.write_text('key = "value"', encoding="utf-8")

        with patch.dict(os.environ, clear=True):
            adapter = LayeredConfigAdapter(root_config_path=config)
            assert adapter.has("key") is True

    def test_has_returns_false_for_missing(self) -> None:
        """has returns False for missing keys."""
        with patch.dict(os.environ, clear=True):
            adapter = LayeredConfigAdapter()
            assert adapter.has("missing") is False


class TestLayeredConfigAdapterGetSource:
    """Tests for get_source method."""

    def test_get_source_env(self) -> None:
        """get_source returns 'env' for environment variables."""
        with patch.dict(os.environ, {"JERRY_VAR": "value"}, clear=True):
            adapter = LayeredConfigAdapter()
            assert adapter.get_source("var") == "env"

    def test_get_source_project(self, tmp_path: Path) -> None:
        """get_source returns 'project' for project config."""
        project_config = tmp_path / "project.toml"
        project_config.write_text('key = "value"', encoding="utf-8")

        with patch.dict(os.environ, clear=True):
            adapter = LayeredConfigAdapter(project_config_path=project_config)
            assert adapter.get_source("key") == "project"

    def test_get_source_root(self, tmp_path: Path) -> None:
        """get_source returns 'root' for root config."""
        root_config = tmp_path / "root.toml"
        root_config.write_text('key = "value"', encoding="utf-8")

        with patch.dict(os.environ, clear=True):
            adapter = LayeredConfigAdapter(root_config_path=root_config)
            assert adapter.get_source("key") == "root"

    def test_get_source_default(self) -> None:
        """get_source returns 'default' for defaults."""
        with patch.dict(os.environ, clear=True):
            adapter = LayeredConfigAdapter(defaults={"key": "value"})
            assert adapter.get_source("key") == "default"

    def test_get_source_none_for_missing(self) -> None:
        """get_source returns None for missing keys."""
        with patch.dict(os.environ, clear=True):
            adapter = LayeredConfigAdapter()
            assert adapter.get_source("missing") is None


class TestLayeredConfigAdapterReload:
    """Tests for reload method."""

    def test_reload_picks_up_file_changes(self, tmp_path: Path) -> None:
        """reload picks up changes to config files."""
        config = tmp_path / "config.toml"
        config.write_text('key = "old"', encoding="utf-8")

        with patch.dict(os.environ, clear=True):
            adapter = LayeredConfigAdapter(root_config_path=config)
            assert adapter.get("key") == "old"

            config.write_text('key = "new"', encoding="utf-8")
            adapter.reload()

            assert adapter.get("key") == "new"

    def test_reload_picks_up_env_changes(self) -> None:
        """reload picks up changes to environment variables."""
        with patch.dict(os.environ, {"JERRY_VAR": "old"}, clear=True):
            adapter = LayeredConfigAdapter()
            assert adapter.get("var") == "old"

            os.environ["JERRY_VAR"] = "new"
            adapter.reload()

            assert adapter.get("var") == "new"


class TestLayeredConfigAdapterAllKeys:
    """Tests for all_keys method."""

    def test_all_keys_combines_sources(self, tmp_path: Path) -> None:
        """all_keys returns keys from all sources."""
        root_config = tmp_path / "root.toml"
        root_config.write_text('[a]\nb = "value"', encoding="utf-8")

        project_config = tmp_path / "project.toml"
        project_config.write_text('c = "value"', encoding="utf-8")

        with patch.dict(os.environ, {"JERRY_D": "value"}, clear=True):
            adapter = LayeredConfigAdapter(
                root_config_path=root_config,
                project_config_path=project_config,
                defaults={"e": "value"},
            )
            keys = adapter.all_keys()

            assert "a.b" in keys
            assert "c" in keys
            assert "d" in keys
            assert "e" in keys
