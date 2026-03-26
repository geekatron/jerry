# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""ProvisionResult value object (H-10: one class per file)."""

from __future__ import annotations

from dataclasses import dataclass

from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode


@dataclass(frozen=True)
class ProvisionResult:
    """Result of an auto-provision pipeline run.

    Attributes:
        success: True when the full provision -> health-check sequence completed.
        node: The provisioned ProxyNode, or None on failure before provisioning.
        stage_failed: Name of the pipeline stage that failed, or None on success.
        error: Human-readable error description when success=False.
    """

    success: bool
    node: ProxyNode | None
    stage_failed: str | None = None
    error: str | None = None
