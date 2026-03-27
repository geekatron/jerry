# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""E2E integration tests for engagement lifecycle across all 3 modes.

FEAT-023-007 AC-4: E2E integration tests verify all 3 modes complete
the 6-phase lifecycle with confirmation gates.

Tests the full chain: config parse → create engagement → lifecycle transitions
→ artifact persistence → state verification.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml


def _write_config(tmp_path: Path, mode: str = "single") -> Path:
    """Write a full engagement config for the given mode."""
    config = {
        "engagement": {
            "id": f"ENG-E2E-{mode.upper()}",
            "name": f"E2E {mode.title()} Test",
            "type": "purple_team" if mode == "purple" else "penetration_test",
            "mode": mode,
            "start_date": "2026-03-27",
        },
        "scope": {"targets": [{"host": "10.0.0.1", "type": "ip", "description": "E2E target"}]},
        "infrastructure": {
            "proxy": {"enabled": True, "provider": "digitalocean", "region": "nyc1",
                      "count": 1, "proxy_type": "direct_socks5", "socks_port": 1080,
                      "operator_ip": "174.7.155.69"},
        },
        "teams": {"red": {"operator": "adam", "role": "attacker"}},
        "credentials": {"proxy_api_key": {"source": "keychain", "key_name": "proxy.digitalocean.api-key"}},
        "rules_of_engagement": {"authorization": "/auth.pdf", "emergency_stop": True,
                                "data_handling": "evidence_vault_only"},
    }
    if mode in ("purple", "split"):
        config["teams"]["blue"] = {
            "operator": "adam" if mode == "purple" else "bob",
            "role": "defender",
        }
    if mode == "purple":
        config["purple_team"] = {"technique_approval": "per_technique",
                                 "pivot_mode": "sequential", "correlation_mode": "real_time"}
    path = tmp_path / f"engagement-{mode}.yaml"
    path.write_text(yaml.dump(config, default_flow_style=False), encoding="utf-8")
    return path


class TestE2ESingleTeamLifecycle:
    """Full lifecycle test for single-team (red-only) mode."""

    def test_single_team_completes_full_lifecycle(self, tmp_path: Path) -> None:
        """Single-team mode traverses all 7 states to ARCHIVED."""
        from src.proxy_infra.application.handlers.engagement_lifecycle_manager import (
            EngagementLifecycleManager,
        )

        config_path = _write_config(tmp_path, mode="single")
        manager = EngagementLifecycleManager(engagement_dir=tmp_path / "engagements")

        state = manager.create(config_path)
        assert state.current_state == "DEFINED"
        assert state.mode == "single"

        state = manager.approve_scope(state.engagement_id)
        assert state.current_state == "PROVISIONING"

        state = manager.activate(state.engagement_id)
        assert state.current_state == "ACTIVE"

        state = manager.complete_execution(state.engagement_id)
        assert state.current_state == "ANALYZING"

        state = manager.complete_analysis(state.engagement_id)
        assert state.current_state == "REPORTING"

        state = manager.approve_report(state.engagement_id)
        assert state.current_state == "TEARDOWN"

        state = manager.complete_teardown(state.engagement_id)
        assert state.current_state == "ARCHIVED"

        # Verify 6 transitions recorded
        assert len(state.transitions) == 6

    def test_single_team_artifacts_persisted(self, tmp_path: Path) -> None:
        """Engagement directory and state file exist after creation."""
        from src.proxy_infra.application.handlers.engagement_lifecycle_manager import (
            EngagementLifecycleManager,
        )

        config_path = _write_config(tmp_path, mode="single")
        manager = EngagementLifecycleManager(engagement_dir=tmp_path / "engagements")
        state = manager.create(config_path)

        eng_dir = tmp_path / "engagements" / state.engagement_id
        assert eng_dir.exists()
        assert (eng_dir / "config" / "state.yaml").exists()
        assert (eng_dir / "config" / "engagement.yaml").exists()
        assert (eng_dir / "red-team" / "findings").is_dir()


class TestE2EPurpleTeamLifecycle:
    """Full lifecycle test for purple team (solo operator) mode."""

    def test_purple_team_completes_full_lifecycle(self, tmp_path: Path) -> None:
        """Purple mode traverses all 7 states with purple-specific config."""
        from src.proxy_infra.application.handlers.engagement_lifecycle_manager import (
            EngagementLifecycleManager,
        )

        config_path = _write_config(tmp_path, mode="purple")
        manager = EngagementLifecycleManager(engagement_dir=tmp_path / "engagements")

        state = manager.create(config_path)
        assert state.mode == "purple"

        state = manager.approve_scope(state.engagement_id)
        state = manager.activate(state.engagement_id)
        state = manager.complete_execution(state.engagement_id)
        state = manager.complete_analysis(state.engagement_id)
        state = manager.approve_report(state.engagement_id)
        state = manager.complete_teardown(state.engagement_id)

        assert state.current_state == "ARCHIVED"

    def test_purple_team_has_blue_team_directory(self, tmp_path: Path) -> None:
        """Purple mode creates both red-team and blue-team directories."""
        from src.proxy_infra.application.handlers.engagement_lifecycle_manager import (
            EngagementLifecycleManager,
        )

        config_path = _write_config(tmp_path, mode="purple")
        manager = EngagementLifecycleManager(engagement_dir=tmp_path / "engagements")
        state = manager.create(config_path)

        eng_dir = tmp_path / "engagements" / state.engagement_id
        assert (eng_dir / "red-team" / "findings").is_dir()
        assert (eng_dir / "blue-team" / "detections").is_dir()


class TestE2ESplitTeamLifecycle:
    """Full lifecycle test for split teams (red vs blue) mode."""

    def test_split_team_completes_full_lifecycle(self, tmp_path: Path) -> None:
        """Split mode traverses all 7 states."""
        from src.proxy_infra.application.handlers.engagement_lifecycle_manager import (
            EngagementLifecycleManager,
        )

        config_path = _write_config(tmp_path, mode="split")
        manager = EngagementLifecycleManager(engagement_dir=tmp_path / "engagements")

        state = manager.create(config_path)
        assert state.mode == "split"

        state = manager.approve_scope(state.engagement_id)
        state = manager.activate(state.engagement_id)
        state = manager.complete_execution(state.engagement_id)
        state = manager.complete_analysis(state.engagement_id)
        state = manager.approve_report(state.engagement_id)
        state = manager.complete_teardown(state.engagement_id)

        assert state.current_state == "ARCHIVED"

    def test_split_team_state_persists_across_transitions(self, tmp_path: Path) -> None:
        """State file updates after each transition."""
        from src.proxy_infra.application.handlers.engagement_lifecycle_manager import (
            EngagementLifecycleManager,
        )

        config_path = _write_config(tmp_path, mode="split")
        manager = EngagementLifecycleManager(engagement_dir=tmp_path / "engagements")
        state = manager.create(config_path)

        state_path = tmp_path / "engagements" / state.engagement_id / "config" / "state.yaml"

        # After creation
        persisted = yaml.safe_load(state_path.read_text())
        assert persisted["current_state"] == "DEFINED"

        # After scope approval
        manager.approve_scope(state.engagement_id)
        persisted = yaml.safe_load(state_path.read_text())
        assert persisted["current_state"] == "PROVISIONING"
        assert len(persisted["transitions"]) == 1
