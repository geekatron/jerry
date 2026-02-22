# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
CheckpointService - Application service for checkpoint lifecycle.

Orchestrates checkpoint creation by:
1. Reading ORCHESTRATION.yaml for resumption state (fail-open)
2. Parsing structured fields from ORCHESTRATION.yaml (TASK-001)
3. Generating the next sequential checkpoint ID
4. Assembling CheckpointData with context state and metadata
5. Delegating persistence to the ICheckpointRepository
6. Writing checkpoint metadata back to ORCHESTRATION.yaml (TASK-003)

Fail-open behavior: If ORCHESTRATION.yaml is absent or unreadable,
the service proceeds without resumption state rather than failing.

References:
    - EN-003: Context Monitoring Bounded Context Foundation
    - EN-008 TASK-001: Structured checkpoint field extraction
    - EN-008 TASK-003: Checkpoint write-back to ORCHESTRATION.yaml
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from src.context_monitoring.application.ports.checkpoint_repository import (
    ICheckpointRepository,
)
from src.context_monitoring.domain.value_objects.checkpoint_data import CheckpointData
from src.context_monitoring.domain.value_objects.fill_estimate import FillEstimate

logger = logging.getLogger(__name__)


class CheckpointService:
    """Application service for checkpoint lifecycle management.

    Orchestrates the creation of checkpoints by combining context state
    with optional ORCHESTRATION.yaml data and persisting via the
    repository port.

    Attributes:
        repository: The checkpoint repository for persistence
        orchestration_path: Path to ORCHESTRATION.yaml (optional)

    Example:
        >>> service = CheckpointService(
        ...     repository=filesystem_repo,
        ...     orchestration_path=Path("ORCHESTRATION.yaml"),
        ... )
        >>> cp = service.create_checkpoint(
        ...     context_state=fill_estimate,
        ...     trigger="pre_compact",
        ... )
    """

    def __init__(
        self,
        repository: ICheckpointRepository,
        orchestration_path: Path | None = None,
    ) -> None:
        """Initialize the CheckpointService.

        Args:
            repository: The checkpoint repository for persistence.
            orchestration_path: Path to ORCHESTRATION.yaml. If None or
                nonexistent, the service operates in fail-open mode.
        """
        self._repository = repository
        self._orchestration_path = orchestration_path

    def create_checkpoint(
        self,
        context_state: FillEstimate,
        trigger: str,
    ) -> CheckpointData:
        """Create and persist a new checkpoint.

        Reads ORCHESTRATION.yaml for resumption state (fail-open if absent),
        generates the next checkpoint ID, assembles CheckpointData, and
        persists via the repository. Then writes checkpoint metadata back
        to ORCHESTRATION.yaml resumption section (TASK-003, fail-open).

        Args:
            context_state: Current context fill estimate.
            trigger: What triggered the checkpoint (e.g., "pre_compact", "manual").

        Returns:
            The created CheckpointData instance.
        """
        checkpoint_id = self._repository.next_checkpoint_id()
        resumption_state = self._build_resumption_state()
        created_at = datetime.now(UTC).isoformat()

        checkpoint = CheckpointData(
            checkpoint_id=checkpoint_id,
            context_state=context_state,
            resumption_state=resumption_state,
            created_at=created_at,
        )

        self._repository.save(checkpoint)
        logger.info(
            "Checkpoint %s created (trigger=%s, fill=%.2f)",
            checkpoint_id,
            trigger,
            context_state.fill_percentage,
        )

        # TASK-003: Write checkpoint metadata back to ORCHESTRATION.yaml
        self._write_back_checkpoint(checkpoint)

        return checkpoint

    def _build_resumption_state(self) -> dict[str, Any] | None:
        """Build resumption state from ORCHESTRATION.yaml.

        TASK-001: Parses ORCHESTRATION.yaml with yaml.safe_load() to extract
        structured fields (current_phase, agent_statuses, quality_gate_state,
        next_actions). Falls back to raw content if YAML parsing fails.
        Returns None if file is absent or unreadable (fail-open).

        Returns:
            Dict with structured orchestration data, or None if unavailable.
        """
        if self._orchestration_path is None:
            return None

        try:
            if not self._orchestration_path.exists():
                logger.debug(
                    "ORCHESTRATION.yaml not found at %s (fail-open)",
                    self._orchestration_path,
                )
                return None

            content = self._orchestration_path.read_text(encoding="utf-8")

            # TASK-001: Parse YAML for structured fields
            structured = self._extract_structured_fields(content)
            if structured is not None:
                return structured

            # Fallback: raw content if parsing fails
            return {"orchestration_raw": content}
        except (OSError, PermissionError) as exc:
            logger.warning(
                "Failed to read ORCHESTRATION.yaml at %s: %s (fail-open)",
                self._orchestration_path,
                exc,
            )
            return None

    def _extract_structured_fields(self, content: str) -> dict[str, Any] | None:
        """Extract structured fields from ORCHESTRATION.yaml content.

        TASK-001: Parses YAML and extracts key fields for downstream
        consumption. Fail-open: returns None if parsing fails.

        Args:
            content: Raw YAML string.

        Returns:
            Dict with structured fields, or None on parse failure.
        """
        try:
            import yaml  # noqa: PLC0415

            data = yaml.safe_load(content)
            if not isinstance(data, dict):
                return None

            result: dict[str, Any] = {}

            # Extract workflow metadata
            workflow = data.get("workflow", {})
            if isinstance(workflow, dict):
                result["workflow_id"] = workflow.get("id")
                result["workflow_status"] = workflow.get("status")
                result["workflow_name"] = workflow.get("name")

            # Extract current phase from pipelines
            pipelines = data.get("pipelines", {})
            if isinstance(pipelines, dict):
                agent_statuses: list[dict[str, str]] = []
                for _pipeline_key, pipeline in pipelines.items():
                    if not isinstance(pipeline, dict):
                        continue
                    current_phase = pipeline.get("current_phase")
                    if current_phase is not None:
                        result.setdefault("current_phase", current_phase)

                    # Extract agent statuses from phases
                    for phase in pipeline.get("phases", []):
                        if not isinstance(phase, dict):
                            continue
                        for agent in phase.get("agents", []):
                            if isinstance(agent, dict):
                                agent_statuses.append(
                                    {
                                        "id": str(agent.get("id", "")),
                                        "status": str(agent.get("status", "")),
                                    }
                                )
                if agent_statuses:
                    result["agent_statuses"] = agent_statuses

            # Extract quality gate state from resumption section
            resumption = data.get("resumption", {})
            if isinstance(resumption, dict):
                quality = resumption.get("quality_trajectory", {})
                if isinstance(quality, dict):
                    result["quality_gate_state"] = {
                        "gates_completed": quality.get("gates_completed", []),
                        "gates_remaining": quality.get("gates_remaining", []),
                        "current_gate": quality.get("current_gate"),
                        "total_iterations_used": quality.get("total_iterations_used", 0),
                    }

                recovery = resumption.get("recovery_state", {})
                if isinstance(recovery, dict):
                    result["recovery_state"] = recovery

            # Extract next actions
            next_actions = data.get("next_actions", {})
            if isinstance(next_actions, dict):
                result["next_actions"] = next_actions.get("immediate", [])

            # Keep raw content as fallback for full context
            result["orchestration_raw"] = content

            return result

        except Exception as exc:  # noqa: BLE001
            logger.debug(
                "YAML parsing failed for ORCHESTRATION.yaml: %s (falling back to raw)",
                exc,
            )
            return None

    def _write_back_checkpoint(self, checkpoint: CheckpointData) -> None:
        """Write checkpoint metadata back to ORCHESTRATION.yaml resumption section.

        TASK-003: Updates the resumption.recovery_state fields with the latest
        checkpoint information. Fail-open: logs warning on any failure.

        Args:
            checkpoint: The checkpoint data to write back.
        """
        if self._orchestration_path is None:
            return

        try:
            if not self._orchestration_path.exists():
                return

            import yaml  # noqa: PLC0415

            content = self._orchestration_path.read_text(encoding="utf-8")
            data = yaml.safe_load(content)
            if not isinstance(data, dict):
                return

            # Ensure resumption.recovery_state exists
            resumption = data.setdefault("resumption", {})
            if not isinstance(resumption, dict):
                return
            recovery = resumption.setdefault("recovery_state", {})
            if not isinstance(recovery, dict):
                return

            # Update checkpoint fields
            recovery["last_checkpoint"] = checkpoint.checkpoint_id
            recovery["context_fill_at_update"] = round(checkpoint.context_state.fill_percentage, 4)
            recovery["updated_at"] = checkpoint.created_at

            # Update compaction events count
            compaction = resumption.setdefault("compaction_events", {})
            if isinstance(compaction, dict):
                count = compaction.get("count", 0)
                if isinstance(count, int):
                    compaction["count"] = count + 1
                events_list = compaction.setdefault("events", [])
                if isinstance(events_list, list):
                    events_list.append(
                        {
                            "checkpoint_id": checkpoint.checkpoint_id,
                            "fill_percentage": round(checkpoint.context_state.fill_percentage, 4),
                            "tier": checkpoint.context_state.tier.name,
                            "timestamp": checkpoint.created_at,
                        }
                    )

            # Write back (non-atomic; concurrent writes may conflict)
            output = yaml.dump(data, default_flow_style=False, sort_keys=False)
            self._orchestration_path.write_text(output, encoding="utf-8")

            logger.debug(
                "Checkpoint %s written back to ORCHESTRATION.yaml",
                checkpoint.checkpoint_id,
            )
        except Exception as exc:  # noqa: BLE001
            logger.warning(
                "Failed to write checkpoint back to ORCHESTRATION.yaml: %s (fail-open)",
                exc,
            )
