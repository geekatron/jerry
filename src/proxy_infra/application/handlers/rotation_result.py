# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""RotationResult value object (H-10: one class per file)."""

from __future__ import annotations

from dataclasses import dataclass

from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode


@dataclass(frozen=True)
class RotationResult:
    """Result of a proxy rotation operation.

    Attributes:
        success: True when the full rotation cycle completed.
        burned_node_id: ID of the node that was retired.
        replacement_node: The newly provisioned replacement node, or None.
        trigger: Rotation trigger event identifier.
        error: Human-readable error when success=False.
    """

    success: bool
    burned_node_id: str
    replacement_node: ProxyNode | None
    trigger: str = ""
    error: str | None = None
