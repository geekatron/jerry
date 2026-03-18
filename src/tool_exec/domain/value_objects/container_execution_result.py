# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""ContainerExecutionResult value object.

Extracted from container_executor.py to comply with H-10 (one class per file).

References:
    - ADR-PROJ023-001: Container Execution Mode
    - CC-001: H-10 one-class-per-file remediation
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.tool_exec.domain.value_objects.filter_result import FilterResult


@dataclass
class ContainerExecutionResult:
    """Result of executing a tool command in a container.

    Attributes:
        exit_code: The process exit code.
        stdout: Captured standard output (may be filtered).
        stderr: Captured standard error (may be filtered).
        raw_stdout: Original unfiltered stdout.
        raw_stderr: Original unfiltered stderr.
            FINDING-004 (CWE-200): Introduced so that both streams can be
            quarantined when a credential is detected in either one.
        credential_detected: Whether the credential filter triggered on either stream.
        filter_result: Full credential filter result for stdout, or None if not applied.
        container_service: The Docker Compose service that ran the command.
    """

    exit_code: int
    stdout: str
    stderr: str
    raw_stdout: str
    raw_stderr: str = ""
    credential_detected: bool = False
    filter_result: FilterResult | None = None
    container_service: str = ""
