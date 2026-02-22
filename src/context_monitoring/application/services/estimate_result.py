# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
EstimateResult - Complete result from the context estimate pipeline.

Bundles the estimate, compaction detection, rotation action,
and threshold configuration for the CLI to serialize to JSON.

References:
    - FEAT-002: Status Line / Context Monitoring Unification
    - EN-010: Application Port (IContextStateStore) + ContextEstimateService
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

from dataclasses import dataclass

from src.context_monitoring.domain.value_objects.compaction_result import (
    CompactionResult,
)
from src.context_monitoring.domain.value_objects.context_estimate import (
    ContextEstimate,
)
from src.context_monitoring.domain.value_objects.rotation_action import RotationAction


@dataclass(frozen=True)
class EstimateResult:
    """Complete result from the context estimate pipeline.

    Bundles the estimate, compaction detection, rotation action,
    and threshold configuration for the CLI to serialize to JSON.

    Attributes:
        estimate: Computed context fill estimate.
        compaction: Compaction detection result.
        action: Recommended rotation action.
        thresholds: Threshold configuration dict.
    """

    estimate: ContextEstimate
    compaction: CompactionResult
    action: RotationAction
    thresholds: dict[str, float]
