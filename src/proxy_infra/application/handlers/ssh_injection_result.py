# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""SshInjectionResult value object (H-10: one class per file)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SshInjectionResult:
    """Result of a single SSH credential injection operation.

    Attributes:
        success: True when all 7 injection steps completed.
        node_id: The proxy node this result is for.
        stage_failed: Name of the failing stage, or None/empty on success.
        username: SOCKS5 username generated on the node (empty on failure).
        password: SOCKS5 password generated on the node (empty on failure).
        error: Human-readable error message if success is False.
    """

    success: bool
    node_id: str
    stage_failed: str | None = None
    username: str = ""
    password: str = ""
    error: str = ""
