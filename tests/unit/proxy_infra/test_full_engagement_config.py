# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""BDD test suite for full engagement config parser (v1.0.0) + from_full_config bridge.

FEAT-023-006: Engagement Config Integration
STORY-023-017: Full Engagement Config Parser (v1.0.0)

Covers:
  - FullEngagementConfig value object: 8-section schema parsing
  - from_full_config() bridge: extracts proxy-relevant fields → EngagementConfig
  - Validation: required fields, mode-specific requirements, credential references
  - Backward compatibility: existing EngagementConfig still works unchanged

Test pyramid: 60% happy path / 30% negative / 10% edge cases
Naming convention: test_{scenario}_when_{condition}_then_{expected}
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from src.proxy_infra.domain.value_objects.engagement_config import EngagementConfig


# =============================================================================
# Helper
# =============================================================================

def _write_full_config(tmp_path: Path, overrides: dict | None = None) -> Path:
    """Write a valid full engagement config YAML."""
    config = {
        "engagement": {
            "id": "ENG-0001",
            "name": "Test Engagement",
            "type": "penetration_test",
            "mode": "single",
            "start_date": "2026-03-27",
        },
        "scope": {
            "targets": [{"host": "10.0.0.1", "type": "ip", "description": "Test target"}],
        },
        "infrastructure": {
            "proxy": {
                "enabled": True,
                "provider": "digitalocean",
                "region": "nyc1",
                "count": 3,
                "proxy_type": "direct_socks5",
                "socks_port": 1080,
                "operator_ip": "174.7.155.69",
            },
        },
        "teams": {
            "red": {"operator": "adam", "role": "attacker"},
        },
        "credentials": {
            "proxy_api_key": {
                "source": "keychain",
                "key_name": "proxy.digitalocean.api-key",
            },
        },
        "rules_of_engagement": {
            "authorization": "/path/to/auth.pdf",
            "emergency_stop": True,
            "data_handling": "evidence_vault_only",
        },
    }
    if overrides:
        _deep_merge(config, overrides)
    path = tmp_path / "engagement.yaml"
    path.write_text(yaml.dump(config, default_flow_style=False), encoding="utf-8")
    return path


def _deep_merge(base: dict, override: dict) -> None:
    """Recursively merge override into base."""
    for k, v in override.items():
        if k in base and isinstance(base[k], dict) and isinstance(v, dict):
            _deep_merge(base[k], v)
        else:
            base[k] = v


# =============================================================================
# FullEngagementConfig value object tests
# =============================================================================


class TestFullEngagementConfig:
    """Tests for the FullEngagementConfig v1.0.0 value object."""

    def test_parse_when_valid_full_config_then_all_sections_accessible(
        self, tmp_path: Path,
    ) -> None:
        """Happy path: valid full config produces accessible section objects."""
        from src.proxy_infra.domain.value_objects.full_engagement_config import (
            FullEngagementConfig,
        )
        from src.proxy_infra.application.handlers.full_engagement_config_parser import (
            FullEngagementConfigParser,
        )

        config_path = _write_full_config(tmp_path)
        parser = FullEngagementConfigParser()
        config = parser.parse(config_path)

        assert config.engagement.id == "ENG-0001"
        assert config.engagement.mode == "single"
        assert config.scope.targets[0]["host"] == "10.0.0.1"
        assert config.infrastructure.proxy.enabled is True
        assert config.infrastructure.proxy.count == 3

    def test_parse_when_missing_engagement_id_then_raises(self, tmp_path: Path) -> None:
        """Missing engagement.id must be rejected."""
        from src.proxy_infra.application.handlers.full_engagement_config_parser import (
            FullEngagementConfigParser,
        )

        config_path = _write_full_config(tmp_path, {"engagement": {"id": ""}})
        parser = FullEngagementConfigParser()
        with pytest.raises(ValueError, match="engagement.id"):
            parser.parse(config_path)

    def test_parse_when_no_targets_then_raises(self, tmp_path: Path) -> None:
        """Empty targets list must be rejected."""
        from src.proxy_infra.application.handlers.full_engagement_config_parser import (
            FullEngagementConfigParser,
        )

        config_path = _write_full_config(tmp_path, {"scope": {"targets": []}})
        parser = FullEngagementConfigParser()
        with pytest.raises(ValueError, match="targets"):
            parser.parse(config_path)

    def test_parse_when_invalid_mode_then_raises(self, tmp_path: Path) -> None:
        """Invalid mode value must be rejected."""
        from src.proxy_infra.application.handlers.full_engagement_config_parser import (
            FullEngagementConfigParser,
        )

        config_path = _write_full_config(tmp_path, {"engagement": {"mode": "invalid"}})
        parser = FullEngagementConfigParser()
        with pytest.raises(ValueError, match="mode"):
            parser.parse(config_path)

    def test_parse_when_split_mode_but_no_blue_team_then_raises(self, tmp_path: Path) -> None:
        """Split mode requires blue team operator."""
        from src.proxy_infra.application.handlers.full_engagement_config_parser import (
            FullEngagementConfigParser,
        )

        config_path = _write_full_config(tmp_path, {
            "engagement": {"mode": "split"},
            "teams": {"red": {"operator": "adam", "role": "attacker"}},
        })
        parser = FullEngagementConfigParser()
        with pytest.raises(ValueError, match="(?i)blue.*split"):
            parser.parse(config_path)


# =============================================================================
# from_full_config bridge tests
# =============================================================================


class TestFromFullConfigBridge:
    """Tests for extracting proxy EngagementConfig from full config."""

    def test_bridge_when_proxy_enabled_then_returns_engagement_config(
        self, tmp_path: Path,
    ) -> None:
        """Full config with proxy enabled produces valid EngagementConfig."""
        from src.proxy_infra.application.handlers.full_engagement_config_parser import (
            FullEngagementConfigParser,
        )

        config_path = _write_full_config(tmp_path)
        parser = FullEngagementConfigParser()
        eng_config = parser.extract_proxy_config(config_path)

        assert isinstance(eng_config, EngagementConfig)
        assert eng_config.engagement_id == "ENG-0001"
        assert eng_config.provider == "digitalocean"
        assert eng_config.count == 3
        assert eng_config.operator_ip != ""

    def test_bridge_when_proxy_disabled_then_raises(self, tmp_path: Path) -> None:
        """Full config with proxy disabled must raise."""
        from src.proxy_infra.application.handlers.full_engagement_config_parser import (
            FullEngagementConfigParser,
        )

        config_path = _write_full_config(tmp_path, {
            "infrastructure": {"proxy": {"enabled": False}},
        })
        parser = FullEngagementConfigParser()
        with pytest.raises(ValueError, match="proxy.*not enabled"):
            parser.extract_proxy_config(config_path)

    def test_bridge_preserves_backward_compat_with_narrow_parser(
        self, tmp_path: Path,
    ) -> None:
        """The narrow EngagementConfigParser still works with narrow YAML."""
        from src.proxy_infra.application.handlers.engagement_config_parser import (
            EngagementConfigParser,
        )

        narrow_path = tmp_path / "narrow.yaml"
        narrow_path.write_text(yaml.dump({
            "engagement_id": "ENG-0001",
            "provider": "digitalocean",
            "region": "nyc1",
            "count": 1,
            "proxy_type": "direct_socks5",
            "socks_port": 1080,
            "operator_ip": "174.7.155.69",
        }), encoding="utf-8")

        parser = EngagementConfigParser()
        config = parser.parse(narrow_path)
        assert config.engagement_id == "ENG-0001"


# =============================================================================
# Cross-skill handoff contract tests
# =============================================================================


class TestEngagementHandoffContracts:
    """Tests for cross-skill engagement artifact persistence."""

    def test_engagement_directory_created_with_correct_structure(
        self, tmp_path: Path,
    ) -> None:
        """Engagement directory must have the canonical subdirectory structure."""
        from src.proxy_infra.application.handlers.engagement_artifact_manager import (
            EngagementArtifactManager,
        )

        manager = EngagementArtifactManager(base_dir=tmp_path)
        eng_dir = manager.create_engagement_directory("ENG-0001")

        assert (eng_dir / "red-team" / "findings").is_dir()
        assert (eng_dir / "blue-team" / "detections").is_dir()
        assert (eng_dir / "analysis").is_dir()
        assert (eng_dir / "config").is_dir()
        assert (eng_dir / "credentials").is_dir()

    def test_engagement_config_persisted_to_config_dir(self, tmp_path: Path) -> None:
        """Engagement YAML config is copied to the engagement config directory."""
        from src.proxy_infra.application.handlers.engagement_artifact_manager import (
            EngagementArtifactManager,
        )

        manager = EngagementArtifactManager(base_dir=tmp_path)
        eng_dir = manager.create_engagement_directory("ENG-0001")
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        config_path = _write_full_config(source_dir)
        manager.persist_config("ENG-0001", config_path)

        assert (eng_dir / "config" / "engagement.yaml").exists()

    def test_handoff_artifact_written_to_correct_subdir(self, tmp_path: Path) -> None:
        """Handoff artifacts go to the team-specific subdirectory."""
        from src.proxy_infra.application.handlers.engagement_artifact_manager import (
            EngagementArtifactManager,
        )

        manager = EngagementArtifactManager(base_dir=tmp_path)
        manager.create_engagement_directory("ENG-0001")
        manager.write_artifact(
            engagement_id="ENG-0001",
            team="red-team",
            category="findings",
            filename="initial-recon.md",
            content="# Initial Recon\n\nFindings here.",
        )

        artifact = tmp_path / "ENG-0001" / "red-team" / "findings" / "initial-recon.md"
        assert artifact.exists()
        assert "Initial Recon" in artifact.read_text()
