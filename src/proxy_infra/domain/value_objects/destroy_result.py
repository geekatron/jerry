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
        destroyed: Provider node IDs that were successfully destroyed.
        failed: Provider node IDs that could not be destroyed.
        token_rotation_prompted: True when the operator was prompted to revoke
            the API key at the provider control panel per F-C-003. Indicates
            the teardown workflow surfaced the token rotation requirement.
    """

    destroyed: list[str]
    failed: list[str]
    token_rotation_prompted: bool = False

    def __post_init__(self) -> None:
        """Normalise field values to plain lists so equality checks work.

        Converts tuple inputs to lists for consistent ``result.failed == []``
        comparisons in the caller.
        """
        # object.__setattr__ bypasses the frozen guard for normalisation only.
        if isinstance(self.destroyed, tuple):
            object.__setattr__(self, "destroyed", list(self.destroyed))
        if isinstance(self.failed, tuple):
            object.__setattr__(self, "failed", list(self.failed))

    @property
    def is_all_successful(self) -> bool:
        """Return True if all requested nodes were successfully destroyed.

        Returns:
            True when the failed list is empty.
        """
        return len(self.failed) == 0

    @property
    def all_succeeded(self) -> bool:
        """Alias for is_all_successful for backwards compatibility.

        Returns:
            True when the failed list is empty.
        """
        return self.is_all_successful
