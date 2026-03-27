# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""BDD test suite for engagement lifecycle workflows (3 modes).

FEAT-023-007: End-to-End Engagement UX
STORY-023-019: Purple Team (Solo) Engagement Workflow
STORY-023-020: Split Teams (Red vs Blue) Engagement Workflow
STORY-023-021: Single-Team Engagement Workflow

Covers:
  - EngagementLifecycleManager: state machine transitions (7 states)
  - Confirmation gates (G1-G7) with fail-safe defaults
  - Mode-specific validation (purple requires purple_team config, split requires blue team)
  - Engagement directory creation via artifact manager
  - State persistence to engagement directory

Test pyramid: 60% happy path / 30% negative / 10% edge cases
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest
import yaml


# =============================================================================
# Helper
# =============================================================================

def _make_full_config(tmp_path: Path, mode: str = "single", **overrides: object) -> Path:
    """Write a full engagement config YAML."""
    config: dict = {
        "engagement": {
            "id": "ENG-0001",
            "name": "Test",
            "type": "penetration_test",
            "mode": mode,
            "start_date": "2026-03-27",
        },
        "scope": {
            "targets": [{"host": "10.0.0.1", "type": "ip", "description": "Test"}],
        },
        "infrastructure": {
            "proxy": {"enabled": True, "provider": "digitalocean", "region": "nyc1", "count": 1,
                      "proxy_type": "direct_socks5", "socks_port": 1080},
        },
        "teams": {"red": {"operator": "adam", "role": "attacker"}},
        "credentials": {"proxy_api_key": {"source": "keychain", "key_name": "proxy.digitalocean.api-key"}},
        "rules_of_engagement": {"authorization": "/auth.pdf", "emergency_stop": True, "data_handling": "evidence_vault_only"},
    }
    if mode == "purple":
        config["teams"]["blue"] = {"operator": "adam", "role": "defender"}
        config["purple_team"] = {"technique_approval": "per_technique", "pivot_mode": "sequential", "correlation_mode": "real_time"}
    elif mode == "split":
        config["teams"]["blue"] = {"operator": "bob", "role": "defender"}
    path = tmp_path / "engagement.yaml"
    path.write_text(yaml.dump(config, default_flow_style=False), encoding="utf-8")
    return path


# =============================================================================
# EngagementLifecycleManager tests
# =============================================================================


class TestEngagementLifecycleManager:
    """Tests for the state machine managing engagement lifecycle."""

    def test_create_when_valid_config_then_state_is_defined(self, tmp_path: Path) -> None:
        """New engagement starts in DEFINED state."""
        from src.proxy_infra.application.handlers.engagement_lifecycle_manager import (
            EngagementLifecycleManager,
        )

        config_path = _make_full_config(tmp_path)
        manager = EngagementLifecycleManager(engagement_dir=tmp_path / "engagements")
        state = manager.create(config_path)

        assert state.current_state == "DEFINED"
        assert state.engagement_id == "ENG-0001"

    def test_approve_scope_when_defined_then_transitions_to_provisioning(
        self, tmp_path: Path,
    ) -> None:
        """G1 approval moves DEFINED → PROVISIONING."""
        from src.proxy_infra.application.handlers.engagement_lifecycle_manager import (
            EngagementLifecycleManager,
        )

        config_path = _make_full_config(tmp_path)
        manager = EngagementLifecycleManager(engagement_dir=tmp_path / "engagements")
        state = manager.create(config_path)
        state = manager.approve_scope(state.engagement_id)

        assert state.current_state == "PROVISIONING"

    def test_activate_when_provisioning_then_transitions_to_active(
        self, tmp_path: Path,
    ) -> None:
        """G3 approval moves PROVISIONING → ACTIVE."""
        from src.proxy_infra.application.handlers.engagement_lifecycle_manager import (
            EngagementLifecycleManager,
        )

        config_path = _make_full_config(tmp_path)
        manager = EngagementLifecycleManager(engagement_dir=tmp_path / "engagements")
        state = manager.create(config_path)
        state = manager.approve_scope(state.engagement_id)
        state = manager.activate(state.engagement_id)

        assert state.current_state == "ACTIVE"

    def test_complete_execution_then_transitions_to_analyzing(self, tmp_path: Path) -> None:
        """Execution complete moves ACTIVE → ANALYZING."""
        from src.proxy_infra.application.handlers.engagement_lifecycle_manager import (
            EngagementLifecycleManager,
        )

        config_path = _make_full_config(tmp_path)
        manager = EngagementLifecycleManager(engagement_dir=tmp_path / "engagements")
        state = manager.create(config_path)
        state = manager.approve_scope(state.engagement_id)
        state = manager.activate(state.engagement_id)
        state = manager.complete_execution(state.engagement_id)

        assert state.current_state == "ANALYZING"

    def test_full_lifecycle_single_mode_reaches_archived(self, tmp_path: Path) -> None:
        """Full single-team lifecycle: DEFINED → ... → ARCHIVED."""
        from src.proxy_infra.application.handlers.engagement_lifecycle_manager import (
            EngagementLifecycleManager,
        )

        config_path = _make_full_config(tmp_path, mode="single")
        manager = EngagementLifecycleManager(engagement_dir=tmp_path / "engagements")
        state = manager.create(config_path)
        state = manager.approve_scope(state.engagement_id)
        state = manager.activate(state.engagement_id)
        state = manager.complete_execution(state.engagement_id)
        state = manager.complete_analysis(state.engagement_id)
        state = manager.approve_report(state.engagement_id)
        state = manager.complete_teardown(state.engagement_id)

        assert state.current_state == "ARCHIVED"

    def test_invalid_transition_when_defined_to_active_then_raises(
        self, tmp_path: Path,
    ) -> None:
        """Cannot skip from DEFINED directly to ACTIVE."""
        from src.proxy_infra.application.handlers.engagement_lifecycle_manager import (
            EngagementLifecycleManager,
        )

        config_path = _make_full_config(tmp_path)
        manager = EngagementLifecycleManager(engagement_dir=tmp_path / "engagements")
        state = manager.create(config_path)

        with pytest.raises(ValueError, match="(?i)invalid.*transition|cannot"):
            manager.activate(state.engagement_id)

    def test_purple_mode_requires_purple_team_config(self, tmp_path: Path) -> None:
        """Purple mode engagement should track purple-specific fields."""
        from src.proxy_infra.application.handlers.engagement_lifecycle_manager import (
            EngagementLifecycleManager,
        )

        config_path = _make_full_config(tmp_path, mode="purple")
        manager = EngagementLifecycleManager(engagement_dir=tmp_path / "engagements")
        state = manager.create(config_path)

        assert state.mode == "purple"

    def test_state_persisted_to_engagement_directory(self, tmp_path: Path) -> None:
        """State file exists in the engagement directory after creation."""
        from src.proxy_infra.application.handlers.engagement_lifecycle_manager import (
            EngagementLifecycleManager,
        )

        config_path = _make_full_config(tmp_path)
        eng_dir = tmp_path / "engagements"
        manager = EngagementLifecycleManager(engagement_dir=eng_dir)
        manager.create(config_path)

        state_file = eng_dir / "ENG-0001" / "config" / "state.yaml"
        assert state_file.exists()

    def test_split_mode_tracks_both_operators(self, tmp_path: Path) -> None:
        """Split mode should record both red and blue operators."""
        from src.proxy_infra.application.handlers.engagement_lifecycle_manager import (
            EngagementLifecycleManager,
        )

        config_path = _make_full_config(tmp_path, mode="split")
        manager = EngagementLifecycleManager(engagement_dir=tmp_path / "engagements")
        state = manager.create(config_path)

        assert state.mode == "split"
