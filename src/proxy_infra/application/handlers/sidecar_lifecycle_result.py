# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""SidecarLifecycleResult value object (H-10: one class per file)."""

from __future__ import annotations

from dataclasses import dataclass

from src.proxy_infra.application.handlers.sidecar_action import SidecarAction


@dataclass(frozen=True)
class SidecarLifecycleResult:
    """Result of a sidecar lifecycle operation.

    Attributes:
        action: The operation that was performed.
        success: True if the operation completed without error.
        running: True if the sidecar container is currently running.
        error: Error description when success=False.
    """

    action: SidecarAction
    success: bool
    running: bool
    error: str = ""
