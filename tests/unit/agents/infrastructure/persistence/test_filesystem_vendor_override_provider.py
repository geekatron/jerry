# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for FilesystemVendorOverrideProvider."""

from __future__ import annotations

from pathlib import Path

import yaml

from src.agents.infrastructure.persistence.filesystem_vendor_override_provider import (
    FilesystemVendorOverrideProvider,
)


class TestGetOverrides:
    """Tests for FilesystemVendorOverrideProvider.get_overrides()."""

    def test_loads_override_file(self, tmp_path: Path) -> None:
        skills_dir = tmp_path / "skills"
        comp_dir = skills_dir / "problem-solving" / "composition"
        comp_dir.mkdir(parents=True)
        override_file = comp_dir / "ps-architect.claude-code.yaml"
        override_file.write_text(
            yaml.dump({"maxTurns": 5, "background": True}),
            encoding="utf-8",
        )

        provider = FilesystemVendorOverrideProvider(skills_dir)
        result = provider.get_overrides("ps-architect", "problem-solving", "claude_code")

        assert result["maxTurns"] == 5
        assert result["background"] is True

    def test_missing_file_returns_empty(self, tmp_path: Path) -> None:
        skills_dir = tmp_path / "skills"
        provider = FilesystemVendorOverrideProvider(skills_dir)
        result = provider.get_overrides("ps-architect", "problem-solving", "claude_code")
        assert result == {}

    def test_missing_composition_dir_returns_empty(self, tmp_path: Path) -> None:
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()
        provider = FilesystemVendorOverrideProvider(skills_dir)
        result = provider.get_overrides("ps-architect", "problem-solving", "claude_code")
        assert result == {}

    def test_vendor_slug_conversion(self, tmp_path: Path) -> None:
        skills_dir = tmp_path / "skills"
        comp_dir = skills_dir / "test-skill" / "composition"
        comp_dir.mkdir(parents=True)
        (comp_dir / "test-agent.google-adk.yaml").write_text(
            yaml.dump({"model": "gemini"}), encoding="utf-8"
        )

        provider = FilesystemVendorOverrideProvider(skills_dir)
        result = provider.get_overrides("test-agent", "test-skill", "google_adk")

        assert result["model"] == "gemini"

    def test_invalid_yaml_returns_empty(self, tmp_path: Path) -> None:
        skills_dir = tmp_path / "skills"
        comp_dir = skills_dir / "skill" / "composition"
        comp_dir.mkdir(parents=True)
        (comp_dir / "agent.claude-code.yaml").write_text("{{bad yaml:", encoding="utf-8")

        provider = FilesystemVendorOverrideProvider(skills_dir)
        result = provider.get_overrides("agent", "skill", "claude_code")

        assert result == {}

    def test_non_dict_yaml_returns_empty(self, tmp_path: Path) -> None:
        skills_dir = tmp_path / "skills"
        comp_dir = skills_dir / "skill" / "composition"
        comp_dir.mkdir(parents=True)
        (comp_dir / "agent.claude-code.yaml").write_text("- just a list", encoding="utf-8")

        provider = FilesystemVendorOverrideProvider(skills_dir)
        result = provider.get_overrides("agent", "skill", "claude_code")

        assert result == {}

    def test_path_construction(self, tmp_path: Path) -> None:
        """Override file path follows skills/{skill}/composition/{agent}.{slug}.yaml."""
        skills_dir = tmp_path / "skills"
        comp_dir = skills_dir / "nasa-se" / "composition"
        comp_dir.mkdir(parents=True)
        (comp_dir / "nse-architecture.claude-code.yaml").write_text(
            yaml.dump({"isolation": "worktree"}), encoding="utf-8"
        )

        provider = FilesystemVendorOverrideProvider(skills_dir)
        result = provider.get_overrides("nse-architecture", "nasa-se", "claude_code")

        assert result["isolation"] == "worktree"

    def test_unknown_vendor_uses_underscore_to_hyphen(self, tmp_path: Path) -> None:
        skills_dir = tmp_path / "skills"
        comp_dir = skills_dir / "skill" / "composition"
        comp_dir.mkdir(parents=True)
        (comp_dir / "agent.my-vendor.yaml").write_text(yaml.dump({"x": 1}), encoding="utf-8")

        provider = FilesystemVendorOverrideProvider(skills_dir)
        result = provider.get_overrides("agent", "skill", "my_vendor")

        assert result["x"] == 1
