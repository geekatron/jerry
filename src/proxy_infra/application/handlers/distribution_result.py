# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""DistributionResult value object (H-10: one class per file)."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class DistributionResult:
    """Result of a secrets distribution operation.

    Attributes:
        success: True when all secrets were written without error.
        written_paths: Paths of secret files successfully written.
        errors: Error descriptions for any files that could not be written.
    """

    success: bool
    written_paths: tuple[str, ...] = field(default_factory=tuple)
    errors: tuple[str, ...] = field(default_factory=tuple)
