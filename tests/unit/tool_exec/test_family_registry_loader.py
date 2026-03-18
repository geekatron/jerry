# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for FamilyRegistryLoader."""

from __future__ import annotations

from pathlib import Path

import pytest

from src.tool_exec.infrastructure.registry.family_registry_loader import (
    FamilyRegistryLoader,
)


class TestFamilyRegistryLoaderParsing:
    """Tests for registry YAML parsing."""

    def test_parse_valid_registry(self, tmp_path: Path) -> None:
        """Valid registry YAML is parsed into ToolFamilyInfo objects."""
        registry = tmp_path / "tool_families.yaml"
        registry.write_text(
            """
families:
  - name: test-family
    description: A test family
    resolver_module: src.tool_exec.infrastructure.adapters.rainbow_tool_resolver
    resolver_class: RainbowToolResolver
    config_path: skills/rainbow/config/tool-exec.yaml
    enabled: true
"""
        )

        loader = FamilyRegistryLoader(registry)
        families = loader.list_families()

        assert len(families) == 1
        assert families[0].name == "test-family"
        assert families[0].description == "A test family"
        assert families[0].enabled is True

    def test_parse_disabled_family(self, tmp_path: Path) -> None:
        """Disabled families are parsed but not loaded."""
        registry = tmp_path / "tool_families.yaml"
        registry.write_text(
            """
families:
  - name: disabled-family
    description: A disabled family
    resolver_module: nonexistent.module
    resolver_class: NonexistentClass
    config_path: nonexistent.yaml
    enabled: false
"""
        )

        loader = FamilyRegistryLoader(registry)
        families = loader.list_families()

        assert len(families) == 1
        assert families[0].enabled is False

    def test_missing_registry_raises(self) -> None:
        """Missing registry file raises FileNotFoundError."""
        loader = FamilyRegistryLoader("/nonexistent/path.yaml")
        with pytest.raises(FileNotFoundError):
            loader.list_families()

    def test_malformed_registry_raises(self, tmp_path: Path) -> None:
        """Registry without 'families' key raises ValueError."""
        registry = tmp_path / "tool_families.yaml"
        registry.write_text("some_key: some_value\n")

        loader = FamilyRegistryLoader(registry)
        with pytest.raises(ValueError, match="families"):
            loader.list_families()


class TestFamilyRegistryLoaderLoading:
    """Tests for dynamic resolver loading."""

    def test_load_real_rainbow_resolver(self) -> None:
        """Load the real rainbow resolver from tool_families.yaml."""
        # Find the repo root
        repo_root = Path(__file__).resolve().parents[3]
        registry_path = repo_root / "tool_families.yaml"
        config_path = repo_root / "skills" / "rainbow" / "config" / "tool-exec.yaml"

        if not registry_path.exists():
            pytest.skip("tool_families.yaml not found")
        if not config_path.exists():
            pytest.skip("tool-exec.yaml not found")

        loader = FamilyRegistryLoader(registry_path)
        resolvers = loader.load()

        assert "rainbow" in resolvers
        assert resolvers["rainbow"].can_resolve("nuclei")

    def test_load_skips_disabled_families(self, tmp_path: Path) -> None:
        """Disabled families are not loaded."""
        registry = tmp_path / "tool_families.yaml"
        registry.write_text(
            """
families:
  - name: disabled-family
    description: Should be skipped
    resolver_module: nonexistent.module
    resolver_class: NonexistentClass
    config_path: nonexistent.yaml
    enabled: false
"""
        )

        loader = FamilyRegistryLoader(registry)
        resolvers = loader.load()

        assert len(resolvers) == 0
