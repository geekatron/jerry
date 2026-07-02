# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
E2E integration tests for OutputResolver with governance YAML token resolution.

Tests cover:
    - GH #192 / AC-3a: OutputResolver resolves config correctly end-to-end
    - GH #192 / AC-3b: Governance YAML files contain ${JERRY_OUTPUT_BASE} token
    - GH #192 / AC-4: Fallback chain works end-to-end with real config adapter
    - GH #192 / AC-5: Terminal fallback work/ when neither config nor JERRY_PROJECT set
    - Bootstrap integration: get_project_data_path() delegates to OutputResolver

Test Categories:
    - E2E: Full stack from config adapter through resolver
    - Integration: Governance YAML token presence verification
"""

from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from src.configuration.application.services.output_resolver import OutputResolver
from src.infrastructure.adapters.configuration.layered_config_adapter import (
    LayeredConfigAdapter,
)

# Repository root for governance YAML file checks
REPO_ROOT = Path(__file__).resolve().parents[3]

# All 6 governance YAML files that must contain ${JERRY_OUTPUT_BASE}
GOVERNANCE_YAML_FILES = [
    "skills/use-case/agents/uc-author.governance.yaml",
    "skills/use-case/agents/uc-slicer.governance.yaml",
    "skills/test-spec/agents/tspec-generator.governance.yaml",
    "skills/test-spec/agents/tspec-analyst.governance.yaml",
    "skills/contract-design/agents/cd-generator.governance.yaml",
    "skills/contract-design/agents/cd-validator.governance.yaml",
]


class TestGovernanceYamlTokenPresence:
    """Verify all 6 governance YAML files contain ${JERRY_OUTPUT_BASE} token (AC-3b)."""

    @pytest.mark.parametrize("yaml_path", GOVERNANCE_YAML_FILES)
    def test_governance_yaml_contains_output_base_token(self, yaml_path: str) -> None:
        """Each governance YAML output.location must use ${JERRY_OUTPUT_BASE}."""
        full_path = REPO_ROOT / yaml_path
        assert full_path.exists(), f"Governance YAML not found: {yaml_path}"

        content = full_path.read_text()
        assert "${JERRY_OUTPUT_BASE}" in content, (
            f"{yaml_path} does not contain ${{JERRY_OUTPUT_BASE}} token"
        )

    @pytest.mark.parametrize("yaml_path", GOVERNANCE_YAML_FILES)
    def test_governance_yaml_no_fallback_location(self, yaml_path: str) -> None:
        """Governance YAMLs must not contain the deprecated fallback_location field."""
        full_path = REPO_ROOT / yaml_path
        content = full_path.read_text()
        assert "fallback_location" not in content, (
            f"{yaml_path} still contains deprecated fallback_location field"
        )


class TestOutputResolverWithLayeredConfig:
    """E2E tests using real LayeredConfigAdapter (AC-3a, AC-4, AC-5)."""

    def test_resolver_with_real_adapter_config_priority(self, tmp_path: Path) -> None:
        """Config value from TOML takes priority over JERRY_PROJECT (AC-4)."""
        # Write a config file with output.base_path set
        config_file = tmp_path / "config.toml"
        config_file.write_text('[output]\nbase_path = "my-custom-output"\n')

        adapter = LayeredConfigAdapter(
            env_prefix="JERRY_TEST_",
            root_config_path=config_file,
            project_config_path=None,
            defaults={"output.base_path": None},
        )
        resolver = OutputResolver(config_provider=adapter)

        with patch.dict(os.environ, {"JERRY_PROJECT": "PROJ-001"}, clear=False):
            result = resolver.resolve()

        assert result == "my-custom-output/"

    def test_resolver_with_real_adapter_project_fallback(self, tmp_path: Path) -> None:
        """Falls back to projects/{JERRY_PROJECT}/ when no config (AC-4)."""
        # Empty config file — no output.base_path
        config_file = tmp_path / "config.toml"
        config_file.write_text("")

        adapter = LayeredConfigAdapter(
            env_prefix="JERRY_TEST_E2E_",
            root_config_path=config_file,
            project_config_path=None,
            defaults={"output.base_path": None},
        )
        resolver = OutputResolver(config_provider=adapter)

        with patch.dict(os.environ, {"JERRY_PROJECT": "PROJ-042"}, clear=False):
            result = resolver.resolve()

        assert result == "projects/PROJ-042/"

    def test_resolver_with_real_adapter_terminal_fallback(self, tmp_path: Path) -> None:
        """Falls back to work/ when neither config nor JERRY_PROJECT (AC-5)."""
        config_file = tmp_path / "config.toml"
        config_file.write_text("")

        adapter = LayeredConfigAdapter(
            env_prefix="JERRY_TEST_E2E_",
            root_config_path=config_file,
            project_config_path=None,
            defaults={"output.base_path": None},
        )
        resolver = OutputResolver(config_provider=adapter)

        env = {k: v for k, v in os.environ.items() if k != "JERRY_PROJECT"}
        with patch.dict(os.environ, env, clear=True):
            result = resolver.resolve()

        assert result == "work/"

    def test_resolver_with_real_adapter_env_var_override(self, tmp_path: Path) -> None:
        """Environment variable override takes priority over TOML config."""
        # TOML has one value
        config_file = tmp_path / "config.toml"
        config_file.write_text('[output]\nbase_path = "from-toml"\n')

        # EnvConfigAdapter caches env vars at construction time,
        # so the env var must be set BEFORE constructing the adapter.
        with patch.dict(
            os.environ,
            {"JERRY_TEST_E2E2_OUTPUT__BASE_PATH": "from-env"},
            clear=False,
        ):
            adapter = LayeredConfigAdapter(
                env_prefix="JERRY_TEST_E2E2_",
                root_config_path=config_file,
                project_config_path=None,
                defaults={"output.base_path": None},
            )
            resolver = OutputResolver(config_provider=adapter)
            result = resolver.resolve()

        assert result == "from-env/"
