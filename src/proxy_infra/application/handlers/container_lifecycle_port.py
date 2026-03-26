# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""ContainerLifecyclePort — Protocol for sidecar container lifecycle management.

Defines the application-layer port that the SidecarLifecycleHandler depends on.
Implementations wrap docker compose up/down for the socks-bridge sidecar,
activated via ``--profile socks``.

Design constraints:
    H-07: Application layer port — no infrastructure imports.
    H-10: One public class per file.
    H-11: All public methods have type annotations.
    TASK-023-011: CLM proxy pool integration and sidecar lifecycle.
"""

from __future__ import annotations

from typing import Protocol


class ContainerLifecyclePort(Protocol):
    """Protocol for socks-bridge sidecar container lifecycle operations.

    Implementations wrap docker compose up/down/restart for the socks-bridge
    service. The sidecar is activated via ``--profile socks``.
    """

    def start_sidecar(self, profile: str = "socks") -> bool:
        """Start the socks-bridge sidecar service with the given Compose profile.

        Args:
            profile: Docker Compose profile name to activate (default ``"socks"``).

        Returns:
            True if the sidecar started successfully.
        """
        ...

    def stop_sidecar(self) -> bool:
        """Stop and remove the socks-bridge sidecar service.

        Returns:
            True if the sidecar was stopped cleanly.
        """
        ...

    def is_sidecar_running(self) -> bool:
        """Check whether the socks-bridge sidecar container is alive.

        Returns:
            True if the container is in the running state.
        """
        ...
