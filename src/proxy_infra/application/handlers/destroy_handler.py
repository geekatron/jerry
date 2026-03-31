# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""DestroyHandler — application handler for DestroyNodesCommand.

Implements the FM-007 teardown sequence:
  (1) Purge ./secrets/ directory
  (2) Remove engagement SSH key from ssh-agent (ssh-add -d)
  (3) Destroy VPS nodes via provisioner
  (4) Delete SSH keys via provider API
  (5) Delete firewalls via provider API
  (6) Delete pool manifest file
  (7) (removed) BPF bypass map — replaced by SO_MARK loop prevention (EN-023-010)
  (8) Post-teardown orphan verification (FM-018)

Additional gates:
  FM-028: --verify-credentials-rotated must be True before teardown_confirmed.
  F-C-003: Operator prompted to confirm API key revocation at provider panel.

References:
    - ADR-PROJ023-008: CLI Bounded Context Architecture for Proxy Infrastructure
    - EPIC-023-007: Proxy infrastructure automation
    - TASK-023-039: CLM Engagement Teardown for Proxy Infrastructure
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from src.proxy_infra.domain.exceptions.teardown_error import TeardownError

if TYPE_CHECKING:
    from src.proxy_infra.application.commands.destroy_nodes_command import DestroyNodesCommand
    from src.proxy_infra.domain.ports.proxy_provisioner_port import ProxyProvisionerPort
    from src.proxy_infra.domain.value_objects.destroy_result import DestroyResult
    from src.proxy_infra.infrastructure.persistence.pool_manifest_store import PoolManifestStore


class DestroyHandler:
    """Handles DestroyNodesCommand with the FM-007 teardown sequence.

    Enforces the correct destruction order: secrets purged first, SSH agent
    key removed, VPS nodes destroyed, then local state cleaned up. The
    --verify-credentials-rotated gate (FM-028) blocks teardown completion
    until the operator has confirmed credential rotation. Post-teardown
    orphan verification (FM-018) ensures no cloud resources remain.

    Zone 3 approval gate (including optional --force bypass) is enforced
    at the CLI layer before this handler is called.

    The handler does NOT import infrastructure adapters directly — it operates
    through the ProxyProvisionerPort interface (H-07 application-layer rule).

    References:
        - ADR-PROJ023-008: Application handler pattern
        - FM-007: Teardown sequence ordering
        - FM-018: Post-teardown orphan verification
        - FM-028: Credential rotation gate
        - F-C-003: Token rotation prompt
    """

    def __init__(
        self,
        provisioner: ProxyProvisionerPort | None = None,
        manifest_store: PoolManifestStore | None = None,
        bpf_port: Any = None,
        pool_service: Any = None,
    ) -> None:
        """Initialize DestroyHandler with the provisioner port and optional adapters.

        Args:
            provisioner: ProxyProvisionerPort implementation that performs the
                actual cloud API calls. Takes precedence over pool_service.provisioner
                when provided directly.
            manifest_store: Optional PoolManifestStore for reading and deleting
                pool manifests during teardown. When None, teardown proceeds in
                zero-proxy mode (no manifest operations).
            bpf_port: Optional BPF adapter. Retained for interface compatibility;
                bypass map operations removed per EN-023-010.
            pool_service: Optional ProxyPoolService. When provisioner is None, the
                provisioner is sourced from pool_service._provisioner. Supports
                backwards-compatible injection pattern from tests.
        """
        if provisioner is not None:
            self._provisioner = provisioner
        elif pool_service is not None:
            self._provisioner = pool_service._provisioner
        else:
            self._provisioner = None

        self._manifest_store = manifest_store
        self._bpf_port = bpf_port

    def handle(self, command: DestroyNodesCommand) -> DestroyResult:
        """Execute a teardown command with the FM-007 sequence.

        Args:
            command: The destroy command containing engagement_id and teardown flags.

        Returns:
            DestroyResult with success/failure details per node, and
            token_rotation_prompted=True to surface the F-C-003 requirement.

        Raises:
            TeardownError: If credentials have not been rotated (FM-028),
                if VPS destruction fails for any node, or if orphan resources
                remain after teardown (FM-018).
        """
        from src.proxy_infra.domain.value_objects.destroy_result import DestroyResult

        # FM-028: block teardown until operator confirms credential rotation
        if not getattr(command, "verify_credentials_rotated", True):
            raise TeardownError(
                f"Teardown blocked for engagement {command.engagement_id!r}: "
                f"credentials have not been verified as rotated (FM-028). "
                f"Pass --verify-credentials-rotated after revoking the API key "
                f"at the provider control panel (F-C-003)."
            )

        # Determine which nodes to destroy from manifest (or explicit list)
        nodes_to_destroy: list[str] = []
        if self._manifest_store is not None and self._manifest_store.exists(command.engagement_id):
            manifest = self._manifest_store.load(command.engagement_id)
            if command.node_ids:
                nodes_to_destroy = list(command.node_ids)
            else:
                nodes_to_destroy = [n.id for n in manifest.pool.nodes]
        elif command.node_ids:
            nodes_to_destroy = list(command.node_ids)

        # --- FM-007 sequence ---

        # Step 1: Purge secrets directory first
        self._purge_secrets(command.engagement_id)

        # Step 2: Remove SSH key from agent
        self._remove_ssh_agent_key(command.engagement_id)

        # Step 3: Destroy VPS nodes via provisioner
        destroyed: list[str] = []
        if nodes_to_destroy and self._provisioner is not None:
            result = self._provisioner.destroy(nodes_to_destroy)
            if not result.is_all_successful:
                failed_ids = ", ".join(result.failed)
                raise TeardownError(
                    f"VPS destruction failed for nodes [{failed_ids}] in "
                    f"engagement {command.engagement_id!r}. "
                    f"Manual cleanup required — check provider console."
                )
            destroyed = result.destroyed

        # Steps 4 & 5: SSH key and firewall cleanup are handled by the provisioner
        # destroy() call in production adapters.

        # Step 6: Delete pool manifest file
        if self._manifest_store is not None:
            self._manifest_store.delete(command.engagement_id)

        # Step 7: (removed) BPF bypass map no longer exists — EN-023-010 uses
        # SO_MARK on Envoy upstream sockets for loop prevention.

        # Step 8: Post-teardown orphan verification (FM-018)
        if self._provisioner is not None:
            orphans = self._provisioner.list_instances(engagement_tag=command.engagement_id)
            if orphans:
                orphan_ids = ", ".join(o.id for o in orphans)
                raise TeardownError(
                    f"Orphan verification failed for engagement {command.engagement_id!r}: "
                    f"cloud instances still running after teardown: [{orphan_ids}] (FM-018). "
                    f"Manual cleanup required at the provider console."
                )

        # F-C-003: signal that the operator must be prompted to revoke the API key
        return DestroyResult(
            destroyed=destroyed,
            failed=[],
            token_rotation_prompted=True,
        )

    # ------------------------------------------------------------------
    # Teardown step helpers (overridable for testing per FM-007)
    # ------------------------------------------------------------------

    def _purge_secrets(self, engagement_id: str) -> None:
        """Purge the engagement secrets directory (FM-007 Step 1).

        Args:
            engagement_id: Owning engagement identifier.
        """
        # Default no-op; infrastructure bootstrap injects a concrete
        # implementation. Tests override this method directly.

    def _remove_ssh_agent_key(self, engagement_id: str) -> None:
        """Remove the engagement SSH key from the local ssh-agent (FM-007 Step 2).

        Equivalent to running: ssh-add -d <engagement_key_path>

        Args:
            engagement_id: Owning engagement identifier.
        """
        # Default no-op; infrastructure bootstrap injects a concrete
        # implementation. Tests override this method directly.
