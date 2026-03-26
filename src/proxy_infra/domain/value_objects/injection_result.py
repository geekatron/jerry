# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""InjectionResult value object — outcome of a single credential injection operation.

References:
    - TASK-023-034: Credential injection specification
    - STORY-023-005: Ephemeral Credential Lifecycle
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class InjectionResult:
    """Immutable result of a single credential injection operation.

    Attributes:
        node_id: The proxy node this result is for.
        success: True if the credential file was written successfully.
        secret_path: Absolute path to the written secret file, or empty
            string if the injection failed.
        error: Human-readable error message if success is False.
    """

    node_id: str
    success: bool
    secret_path: str = ""
    error: str = ""
