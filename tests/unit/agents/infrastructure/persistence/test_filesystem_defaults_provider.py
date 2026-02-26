# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for FilesystemDefaultsProvider with split defaults support."""

from __future__ import annotations

from pathlib import Path

import yaml

from src.agents.infrastructure.persistence.filesystem_defaults_provider import (
    FilesystemDefaultsProvider,
)


class TestGetDefaults:
    """Tests for FilesystemDefaultsProvider.get_defaults()."""

    def test_loads_governance_defaults(self, tmp_path: Path) -> None:
        gov_path = tmp_path / "jerry-agent-defaults.yaml"
        gov_path.write_text(
            yaml.dump({"version": "1.0.0", "persona": {"tone": "professional"}}),
            encoding="utf-8",
        )
        provider = FilesystemDefaultsProvider(gov_path)
        defaults = provider.get_defaults()
        assert defaults["version"] == "1.0.0"
        assert defaults["persona"]["tone"] == "professional"

    def test_missing_file_returns_empty_dict(self, tmp_path: Path) -> None:
        provider = FilesystemDefaultsProvider(tmp_path / "missing.yaml")
        assert provider.get_defaults() == {}

    def test_caches_defaults(self, tmp_path: Path) -> None:
        gov_path = tmp_path / "defaults.yaml"
        gov_path.write_text(yaml.dump({"a": 1}), encoding="utf-8")
        provider = FilesystemDefaultsProvider(gov_path)
        first = provider.get_defaults()
        gov_path.write_text(yaml.dump({"a": 2}), encoding="utf-8")
        second = provider.get_defaults()
        assert first == second == {"a": 1}

    def test_returns_copy_not_reference(self, tmp_path: Path) -> None:
        gov_path = tmp_path / "defaults.yaml"
        gov_path.write_text(yaml.dump({"a": 1}), encoding="utf-8")
        provider = FilesystemDefaultsProvider(gov_path)
        first = provider.get_defaults()
        first["a"] = 999
        second = provider.get_defaults()
        assert second["a"] == 1

    def test_invalid_yaml_returns_empty_dict(self, tmp_path: Path) -> None:
        gov_path = tmp_path / "bad.yaml"
        gov_path.write_text("{{invalid yaml:", encoding="utf-8")
        provider = FilesystemDefaultsProvider(gov_path)
        assert provider.get_defaults() == {}

    def test_non_dict_yaml_returns_empty_dict(self, tmp_path: Path) -> None:
        gov_path = tmp_path / "list.yaml"
        gov_path.write_text("- item1\n- item2", encoding="utf-8")
        provider = FilesystemDefaultsProvider(gov_path)
        assert provider.get_defaults() == {}


class TestGetVendorDefaults:
    """Tests for FilesystemDefaultsProvider.get_vendor_defaults()."""

    def test_loads_vendor_defaults(self, tmp_path: Path) -> None:
        vendor_dir = tmp_path / "schemas"
        vendor_dir.mkdir()
        vendor_file = vendor_dir / "jerry-claude-code-defaults.yaml"
        vendor_file.write_text(
            yaml.dump({"permissionMode": "default", "background": False}),
            encoding="utf-8",
        )
        provider = FilesystemDefaultsProvider(tmp_path / "gov.yaml", vendor_defaults_dir=vendor_dir)
        vendor = provider.get_vendor_defaults("claude_code")
        assert vendor["permissionMode"] == "default"
        assert vendor["background"] is False

    def test_no_vendor_dir_returns_empty(self, tmp_path: Path) -> None:
        provider = FilesystemDefaultsProvider(tmp_path / "gov.yaml")
        assert provider.get_vendor_defaults("claude_code") == {}

    def test_missing_vendor_file_returns_empty(self, tmp_path: Path) -> None:
        vendor_dir = tmp_path / "schemas"
        vendor_dir.mkdir()
        provider = FilesystemDefaultsProvider(tmp_path / "gov.yaml", vendor_defaults_dir=vendor_dir)
        assert provider.get_vendor_defaults("claude_code") == {}

    def test_caches_vendor_defaults(self, tmp_path: Path) -> None:
        vendor_dir = tmp_path / "schemas"
        vendor_dir.mkdir()
        vendor_file = vendor_dir / "jerry-claude-code-defaults.yaml"
        vendor_file.write_text(yaml.dump({"a": 1}), encoding="utf-8")
        provider = FilesystemDefaultsProvider(tmp_path / "gov.yaml", vendor_defaults_dir=vendor_dir)
        first = provider.get_vendor_defaults("claude_code")
        vendor_file.write_text(yaml.dump({"a": 2}), encoding="utf-8")
        second = provider.get_vendor_defaults("claude_code")
        assert first == second == {"a": 1}

    def test_returns_copy_not_reference(self, tmp_path: Path) -> None:
        vendor_dir = tmp_path / "schemas"
        vendor_dir.mkdir()
        (vendor_dir / "jerry-claude-code-defaults.yaml").write_text(
            yaml.dump({"a": 1}), encoding="utf-8"
        )
        provider = FilesystemDefaultsProvider(tmp_path / "gov.yaml", vendor_defaults_dir=vendor_dir)
        first = provider.get_vendor_defaults("claude_code")
        first["a"] = 999
        second = provider.get_vendor_defaults("claude_code")
        assert second["a"] == 1

    def test_vendor_slug_mapping(self, tmp_path: Path) -> None:
        vendor_dir = tmp_path / "schemas"
        vendor_dir.mkdir()
        (vendor_dir / "jerry-google-adk-defaults.yaml").write_text(
            yaml.dump({"provider": "google"}), encoding="utf-8"
        )
        provider = FilesystemDefaultsProvider(tmp_path / "gov.yaml", vendor_defaults_dir=vendor_dir)
        result = provider.get_vendor_defaults("google_adk")
        assert result["provider"] == "google"

    def test_unknown_vendor_uses_underscore_to_hyphen(self, tmp_path: Path) -> None:
        vendor_dir = tmp_path / "schemas"
        vendor_dir.mkdir()
        (vendor_dir / "jerry-my-vendor-defaults.yaml").write_text(
            yaml.dump({"x": 1}), encoding="utf-8"
        )
        provider = FilesystemDefaultsProvider(tmp_path / "gov.yaml", vendor_defaults_dir=vendor_dir)
        result = provider.get_vendor_defaults("my_vendor")
        assert result["x"] == 1
