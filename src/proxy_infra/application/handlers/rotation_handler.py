# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""RotationHandler — orchestrates burned-proxy detection and replacement.

Rotation sequence (provision-before-destroy, PI-003):
    1. Detect burned node (health failure or explicit OPSEC trigger)
    2. Provision replacement node via AutoProvisionHandler
    3. Update pool manifest with new node replacing burned entry
    4. Destroy burned node via provisioner port

Addresses TASK-023-015 (proxy health monitoring and rotation) and the 8
rotation trigger events RT-01 through RT-08.

Design constraints:
    H-07: Application layer — imports domain ports only, no infrastructure.
    H-10: One public class per file.
    H-11: All public methods have type annotations.
    TASK-023-015: Proxy health monitoring and rotation.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.proxy_infra.application.handlers.auto_provision_handler import AutoProvisionHandler
    from src.proxy_infra.application.handlers.manifest_writer_port import ManifestWriterPort
    from src.proxy_infra.domain.ports.proxy_provisioner_port import ProxyProvisionerPort
    from src.proxy_infra.domain.value_objects.provision_config import ProvisionConfig
    from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode

logger = logging.getLogger(__name__)


from src.proxy_infra.application.handlers.rotation_result import RotationResult  # noqa: E402


class RotationHandler:
    """Orchestrates burned-proxy detection and replacement.

    Implements provision-before-destroy (PI-003): the replacement node is
    fully provisioned, health-checked, and written to the manifest BEFORE
    the burned node is destroyed. This ensures pool size never drops below
    the minimum during rotation.

    The 8 rotation triggers (RT-01 through RT-08) are caller responsibilities;
    the handler receives an already-identified burned_node and trigger label.

    Args:
        auto_provisioner: AutoProvisionHandler for the replacement pipeline.
        provisioner: ProxyProvisionerPort for destroying the burned node.
        manifest_writer: ManifestWriterPort for recording manifest changes.
    """

    def __init__(
        self,
        auto_provisioner: AutoProvisionHandler,
        provisioner: ProxyProvisionerPort,
        manifest_writer: ManifestWriterPort,
    ) -> None:
        """Initialise RotationHandler with all required ports.

        Args:
            auto_provisioner: Full provisioning pipeline handler.
            provisioner: Port for cloud VPS destruction.
            manifest_writer: Port for manifest update after rotation.
        """
        self._auto_provisioner = auto_provisioner
        self._provisioner = provisioner
        self._manifest_writer = manifest_writer

    def handle(
        self,
        burned_node: ProxyNode,
        replacement_config: ProvisionConfig,
        trigger: str = "",
    ) -> RotationResult:
        """Execute the full rotation: provision replacement → update manifest → destroy burned.

        Implements provision-before-destroy (PI-003). If replacement provisioning
        fails, the burned node is NOT destroyed — the operator retains the burned
        node until a replacement can be established.

        Args:
            burned_node: The proxy node to be retired.
            replacement_config: Provisioning configuration for the replacement node.
            trigger: Rotation trigger identifier for audit log (e.g. "RT-01").

        Returns:
            RotationResult with success=True when the full cycle completes.
        """
        logger.info(
            "Rotation triggered: node=%s trigger=%s",
            burned_node.id,
            trigger or "unspecified",
        )

        # Stage 1: Provision replacement (provision-before-destroy per PI-003)
        logger.info("Stage 1/3 — provisioning replacement node")
        provision_result = self._auto_provisioner.handle(replacement_config)
        if not provision_result.success:
            return RotationResult(
                success=False,
                burned_node_id=burned_node.id,
                replacement_node=None,
                trigger=trigger,
                error=(
                    f"Replacement provisioning failed at stage "
                    f"'{provision_result.stage_failed}': {provision_result.error}"
                ),
            )
        replacement = provision_result.node
        logger.info(
            "Stage 1/3 complete — replacement node: id=%s ip=%s",
            replacement.id,
            replacement.ip,
        )

        # Stage 2: Write replacement to manifest (already done by auto_provisioner,
        # but record the burned node removal explicitly)
        logger.info("Stage 2/3 — recording burned node retirement in manifest")
        self._manifest_writer.write(replacement)

        # Stage 3: Destroy the burned node
        logger.info("Stage 3/3 — destroying burned node: %s", burned_node.id)
        destroy_result = self._provisioner.destroy([burned_node.id])
        if not destroy_result.all_succeeded:
            logger.warning(
                "Burned node %s destroy reported failure: %s — rotation continues",
                burned_node.id,
                destroy_result,
            )

        logger.info(
            "Rotation complete: burned=%s replacement=%s trigger=%s",
            burned_node.id,
            replacement.id,
            trigger,
        )
        return RotationResult(
            success=True,
            burned_node_id=burned_node.id,
            replacement_node=replacement,
            trigger=trigger,
        )
