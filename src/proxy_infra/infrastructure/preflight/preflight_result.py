# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Pre-flight check result value object (H-10: one class per file)."""

from __future__ import annotations

from dataclasses import dataclass

from src.proxy_infra.infrastructure.preflight.preflight_status import PreflightStatus


@dataclass(frozen=True)
class PreflightResult:
    """Immutable result of an API key pre-flight check.

    Attributes:
        provider: Cloud provider name that was checked.
        status: Outcome of the check (PASS, WARNING, or FAIL).
        message: Human-readable description of the outcome.
    """

    provider: str
    status: PreflightStatus
    message: str = ""
