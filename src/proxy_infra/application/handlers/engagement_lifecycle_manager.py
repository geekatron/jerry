# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""EngagementLifecycleManager — manages the 7-state engagement lifecycle.

Implements the state machine from ADR-PROJ023-010:
  DEFINED → PROVISIONING → ACTIVE → ANALYZING → REPORTING → TEARDOWN → ARCHIVED

Each transition validates the current state before proceeding. Invalid
transitions raise ValueError.

Design constraints:
    H-07: Application layer — imports domain only.
    H-10: One public class per file.
    H-11: All public methods have type annotations.

References:
    - TASK-023-094: State machine implementation
    - TASK-023-095: Confirmation gate handlers
    - ADR-PROJ023-010: Engagement lifecycle architecture
    - skills/cyber-ops/references/state-machine.md
"""

from __future__ import annotations

import logging
from pathlib import Path

import yaml

from src.proxy_infra.application.handlers.engagement_artifact_manager import (
    EngagementArtifactManager,
)
from src.proxy_infra.application.handlers.engagement_state import EngagementState
from src.proxy_infra.application.handlers.full_engagement_config_parser import (
    FullEngagementConfigParser,
)

logger = logging.getLogger(__name__)

#: Valid state transitions in the engagement lifecycle.
_VALID_TRANSITIONS: dict[str, list[str]] = {
    "DEFINED": ["PROVISIONING"],
    "PROVISIONING": ["ACTIVE", "PROVISIONING"],
    "ACTIVE": ["ANALYZING"],
    "ANALYZING": ["REPORTING"],
    "REPORTING": ["TEARDOWN"],
    "TEARDOWN": ["ARCHIVED"],
    "ARCHIVED": [],
}


class EngagementLifecycleManager:
    """Manages the 7-state engagement lifecycle state machine.

    Creates engagement directories, parses configs, tracks state transitions,
    and persists state to the engagement directory.

    Args:
        engagement_dir: Base directory for engagement artifacts.
    """

    def __init__(self, engagement_dir: Path) -> None:
        """Initialise the lifecycle manager.

        Args:
            engagement_dir: Base directory for engagement directories.
        """
        self._engagement_dir = engagement_dir
        self._artifact_manager = EngagementArtifactManager(base_dir=engagement_dir)
        self._parser = FullEngagementConfigParser()
        self._states: dict[str, EngagementState] = {}

    def create(self, config_path: Path) -> EngagementState:
        """Create a new engagement in DEFINED state.

        Parses the config, creates the engagement directory, and persists
        the initial state.

        Args:
            config_path: Path to the engagement config YAML.

        Returns:
            EngagementState in DEFINED state.
        """
        full_config = self._parser.parse(config_path)
        eng_id = full_config.engagement.id
        mode = full_config.engagement.mode

        # Create engagement directory structure
        self._artifact_manager.create_engagement_directory(eng_id)

        # Persist config to engagement directory
        self._artifact_manager.persist_config(eng_id, config_path)

        # Create initial state
        state = EngagementState(
            engagement_id=eng_id,
            current_state="DEFINED",
            mode=mode,
        )
        self._states[eng_id] = state

        # Persist state
        self._persist_state(state)

        logger.info("Engagement %s created in DEFINED state (mode=%s)", eng_id, mode)
        return state

    def approve_scope(self, engagement_id: str) -> EngagementState:
        """Approve engagement scope (G1) — transitions DEFINED → PROVISIONING.

        Args:
            engagement_id: Engagement identifier.

        Returns:
            Updated EngagementState.
        """
        return self._transition(engagement_id, "PROVISIONING")

    def activate(self, engagement_id: str) -> EngagementState:
        """Approve infrastructure (G3) — transitions PROVISIONING → ACTIVE.

        Args:
            engagement_id: Engagement identifier.

        Returns:
            Updated EngagementState.
        """
        return self._transition(engagement_id, "ACTIVE")

    def complete_execution(self, engagement_id: str) -> EngagementState:
        """Signal execution complete — transitions ACTIVE → ANALYZING.

        Args:
            engagement_id: Engagement identifier.

        Returns:
            Updated EngagementState.
        """
        return self._transition(engagement_id, "ANALYZING")

    def complete_analysis(self, engagement_id: str) -> EngagementState:
        """Analysis complete — transitions ANALYZING → REPORTING.

        Args:
            engagement_id: Engagement identifier.

        Returns:
            Updated EngagementState.
        """
        return self._transition(engagement_id, "REPORTING")

    def approve_report(self, engagement_id: str) -> EngagementState:
        """Approve report (G5) — transitions REPORTING → TEARDOWN.

        Args:
            engagement_id: Engagement identifier.

        Returns:
            Updated EngagementState.
        """
        return self._transition(engagement_id, "TEARDOWN")

    def complete_teardown(self, engagement_id: str) -> EngagementState:
        """Teardown complete (G6/G7) — transitions TEARDOWN → ARCHIVED.

        Args:
            engagement_id: Engagement identifier.

        Returns:
            Updated EngagementState.
        """
        return self._transition(engagement_id, "ARCHIVED")

    def _transition(self, engagement_id: str, target_state: str) -> EngagementState:
        """Execute a state transition with validation.

        Args:
            engagement_id: Engagement identifier.
            target_state: Target state to transition to.

        Returns:
            Updated EngagementState.

        Raises:
            ValueError: If the transition is invalid from the current state.
            KeyError: If the engagement_id is not found.
        """
        state = self._states.get(engagement_id)
        if state is None:
            raise KeyError(f"Engagement {engagement_id!r} not found")

        valid_targets = _VALID_TRANSITIONS.get(state.current_state, [])
        if target_state not in valid_targets:
            raise ValueError(
                f"Invalid transition: cannot move from {state.current_state} to "
                f"{target_state}. Valid transitions from {state.current_state}: "
                f"{valid_targets}"
            )

        state.transition_to(target_state)
        self._persist_state(state)

        logger.info(
            "Engagement %s: %s → %s",
            engagement_id,
            state.transitions[-1]["from"],
            target_state,
        )
        return state

    def _persist_state(self, state: EngagementState) -> None:
        """Write state to the engagement directory.

        Args:
            state: Current engagement state to persist.
        """
        state_data = {
            "engagement_id": state.engagement_id,
            "current_state": state.current_state,
            "mode": state.mode,
            "transitions": state.transitions,
        }
        state_path = (
            self._engagement_dir / state.engagement_id / "config" / "state.yaml"
        )
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(
            yaml.dump(state_data, default_flow_style=False), encoding="utf-8"
        )
