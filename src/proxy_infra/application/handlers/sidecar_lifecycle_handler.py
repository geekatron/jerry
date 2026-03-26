# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""SidecarLifecycleHandler — manages socks-bridge sidecar container lifecycle.

Application handler that starts, stops, and restarts the socks-bridge Docker
sidecar service via an injected ContainerLifecyclePort. Bridges the application
command flow to the Docker Compose profile-based sidecar activation defined in
TASK-023-011 and TASK-023-012.

Design constraints:
    H-07: Application layer — imports domain only, no direct infrastructure calls.
    H-10: One public class per file.
    H-11: All public methods have type annotations.
    TASK-023-011: CLM proxy pool integration and sidecar lifecycle.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.proxy_infra.application.handlers.container_lifecycle_port import (
        ContainerLifecyclePort,
    )

logger = logging.getLogger(__name__)


from src.proxy_infra.application.handlers.sidecar_action import SidecarAction  # noqa: E402
from src.proxy_infra.application.handlers.sidecar_lifecycle_result import SidecarLifecycleResult  # noqa: E402


class SidecarLifecycleHandler:
    """Manages socks-bridge sidecar container lifecycle via CLM port.

    Integrates with ContainerLifecycleManager (TASK-023-011) to start/stop/
    restart the socks-bridge Docker Compose profile sidecar for Option B
    (sidecar bridge) and to support proxy pool injection.

    The handler operates on the ContainerLifecyclePort interface — it never
    imports Docker SDK or subprocess directly (H-07 application-layer rule).

    Args:
        clm: ContainerLifecyclePort implementation (injected at composition root).
        socks_profile: Docker Compose profile name for sidecar activation.
    """

    def __init__(
        self,
        clm: ContainerLifecyclePort,
        socks_profile: str = "socks",
    ) -> None:
        """Initialise the sidecar lifecycle handler.

        Args:
            clm: ContainerLifecyclePort that wraps docker compose commands.
            socks_profile: Profile name passed to ``--profile`` on compose up.
        """
        self._clm = clm
        self._socks_profile = socks_profile

    def start(self) -> SidecarLifecycleResult:
        """Start the socks-bridge sidecar container.

        Invokes CLM with the socks profile. The sidecar only starts when
        the ``--profile socks`` flag is present in docker compose up.

        Returns:
            SidecarLifecycleResult indicating success and running state.
        """
        logger.info("Starting socks-bridge sidecar (profile=%s)", self._socks_profile)
        ok = self._clm.start_sidecar(profile=self._socks_profile)
        running = self._clm.is_sidecar_running() if ok else False
        return SidecarLifecycleResult(
            action=SidecarAction.START,
            success=ok,
            running=running,
            error="" if ok else "CLM start_sidecar returned False",
        )

    def stop(self) -> SidecarLifecycleResult:
        """Stop and remove the socks-bridge sidecar container.

        Returns:
            SidecarLifecycleResult indicating success and running state.
        """
        logger.info("Stopping socks-bridge sidecar")
        ok = self._clm.stop_sidecar()
        running = self._clm.is_sidecar_running()
        return SidecarLifecycleResult(
            action=SidecarAction.STOP,
            success=ok,
            running=running,
            error="" if ok else "CLM stop_sidecar returned False",
        )

    def restart(self) -> SidecarLifecycleResult:
        """Restart the socks-bridge sidecar container.

        Performs stop then start in sequence.

        Returns:
            SidecarLifecycleResult indicating success and running state after restart.
        """
        logger.info("Restarting socks-bridge sidecar")
        stop_result = self.stop()
        if not stop_result.success:
            return SidecarLifecycleResult(
                action=SidecarAction.RESTART,
                success=False,
                running=stop_result.running,
                error=f"Stop phase failed: {stop_result.error}",
            )
        start_result = self.start()
        return SidecarLifecycleResult(
            action=SidecarAction.RESTART,
            success=start_result.success,
            running=start_result.running,
            error=start_result.error,
        )

    def status(self) -> SidecarLifecycleResult:
        """Query the current running status of the sidecar container.

        Returns:
            SidecarLifecycleResult with running=True when the container is alive.
        """
        running = self._clm.is_sidecar_running()
        return SidecarLifecycleResult(
            action=SidecarAction.STATUS,
            success=True,
            running=running,
        )
