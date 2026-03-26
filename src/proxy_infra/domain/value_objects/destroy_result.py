# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""DestroyResult value object — outcome of a node destruction operation.

References:
    - ADR-PROJ023-008: CLI Bounded Context Architecture for Proxy Infrastructure
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class DestroyResult:
    """Immutable result of a node destruction operation.

    Attributes:
        succeeded_ids: Provider node IDs that were successfully destroyed.
        failed_ids: Provider node IDs that could not be destroyed.
        errors: Mapping of failed node ID to error description.
    """

    succeeded_ids: tuple[str, ...]
    failed_ids: tuple[str, ...]
    errors: dict[str, str] = field(default_factory=dict)

    @property
    def all_succeeded(self) -> bool:
        """Return True if all requested nodes were successfully destroyed.

        Returns:
            True when failed_ids is empty.
        """
        return len(self.failed_ids) == 0
