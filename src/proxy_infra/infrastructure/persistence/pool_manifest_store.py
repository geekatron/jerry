# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""PoolManifestStore — reads and writes pool manifest YAML with integrity verification.

References:
    - ADR-PROJ023-008: Pool manifest as integration contract with CLM
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.proxy_infra.domain.value_objects.pool_manifest import PoolManifest


class PoolManifestStore:
    """Reads and writes pool manifest YAML with SHA-256 integrity verification.

    Implements the file-system based integration contract between proxy_infra
    and the Container Lifecycle Manager (CLM). Writes are atomic (write-to-temp
    then rename) to prevent partial reads by the CLM.

    Manifest location: work/engagements/{engagement_id}/proxy-pool.yaml

    Invariant enforced:
        PI-004: Integrity hash is verified on every read. ManifestIntegrityError
        is raised if the hash does not match the stored pool data.

    References:
        - ADR-PROJ023-008: Manifest integrity (PI-004), atomic write pattern
    """

    def load(self, engagement_id: str) -> PoolManifest:
        """Load and integrity-verify the pool manifest for an engagement.

        Args:
            engagement_id: Owning engagement identifier.

        Returns:
            PoolManifest with verified integrity.

        Raises:
            ManifestIntegrityError: If SHA-256 hash does not match (PI-004).
            FileNotFoundError: If no manifest exists for the engagement.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def save(self, manifest: PoolManifest) -> None:
        """Atomically write a pool manifest to disk.

        Computes SHA-256 hash of the serialized pool data, embeds it in
        the manifest, then writes to a temp file and renames to the final
        path to ensure atomic replacement.

        Args:
            manifest: The PoolManifest to persist.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def exists(self, engagement_id: str) -> bool:
        """Check whether a manifest file exists for an engagement.

        Args:
            engagement_id: Owning engagement identifier.

        Returns:
            True if the manifest file exists on disk.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def delete(self, engagement_id: str) -> None:
        """Delete the pool manifest for an engagement.

        Called during engagement teardown after all nodes are destroyed.

        Args:
            engagement_id: Owning engagement identifier.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")
