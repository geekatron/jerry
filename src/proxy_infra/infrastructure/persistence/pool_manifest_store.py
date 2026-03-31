# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""PoolManifestStore — reads and writes pool manifest YAML with integrity verification.

Implements the file-system integration contract between the proxy_infra bounded
context and the Container Lifecycle Manager (CLM).

Manifest location: {base_dir}/work/engagements/{engagement_id}/proxy-pool.yaml

Invariants enforced:
    PI-004: SHA-256 integrity hash verified on every read. ManifestIntegrityError
        raised if the stored hash does not match computed hash.

Atomic write pattern:
    Writes go to a .tmp sibling file; os.replace() is used for atomic rename.
    This prevents partial reads by the CLM during manifest updates.

References:
    - ADR-PROJ023-008: Pool manifest as integration contract with CLM
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

import os
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

import yaml

from src.proxy_infra.domain.services.proxy_pool_service import ProxyPoolService
from src.proxy_infra.domain.value_objects.node_status import NodeStatus
from src.proxy_infra.domain.value_objects.pool_manifest import PoolManifest
from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode
from src.proxy_infra.domain.value_objects.proxy_pool import ProxyPool
from src.proxy_infra.domain.value_objects.proxy_role import ProxyRole
from src.proxy_infra.domain.value_objects.proxy_type import ProxyType

if TYPE_CHECKING:
    pass


#: Relative path template from base_dir to the manifest file.
_MANIFEST_RELATIVE: str = "work/engagements/{engagement_id}/proxy-pool.yaml"


class PoolManifestStore:
    """Reads and writes pool manifest YAML with SHA-256 integrity verification.

    Implements the file-system based integration contract between proxy_infra
    and the Container Lifecycle Manager (CLM). Writes are atomic (write-to-temp
    then rename) to prevent partial reads by the CLM.

    Manifest location: {base_dir}/work/engagements/{engagement_id}/proxy-pool.yaml

    Invariants enforced:
        PI-004: Integrity hash is verified on every read. ManifestIntegrityError
            is raised if the hash does not match the stored pool data.

    References:
        - ADR-PROJ023-008: Manifest integrity (PI-004), atomic write pattern
    """

    def __init__(
        self,
        base_dir: Path | str,
    ) -> None:
        """Initialize PoolManifestStore.

        Args:
            base_dir: Root directory of the engagement workspace. Manifests are
                written to {base_dir}/work/engagements/{engagement_id}/proxy-pool.yaml.
        """
        self._base_dir = Path(base_dir)
        self._pool_service = ProxyPoolService(provisioner=None)  # type: ignore[arg-type]

    # ------------------------------------------------------------------
    # Path resolution
    # ------------------------------------------------------------------

    def _manifest_path(self, engagement_id: str) -> Path:
        """Return the absolute path to the manifest file for an engagement.

        Args:
            engagement_id: Owning engagement identifier.

        Returns:
            Absolute Path to the proxy-pool.yaml file.
        """
        return self._base_dir / _MANIFEST_RELATIVE.format(engagement_id=engagement_id)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load(self, engagement_id: str) -> PoolManifest:
        """Load and integrity-verify the pool manifest for an engagement.

        Reads the YAML file from disk, reconstructs the PoolManifest domain
        object, and verifies the SHA-256 integrity hash (PI-004).

        Args:
            engagement_id: Owning engagement identifier.

        Returns:
            PoolManifest with verified integrity.

        Raises:
            ManifestIntegrityError: If SHA-256 hash does not match (PI-004).
            FileNotFoundError: If no manifest exists for the engagement.
        """
        path = self._manifest_path(engagement_id)
        if not path.exists():
            raise FileNotFoundError(
                f"Pool manifest not found for engagement {engagement_id!r}. "
                f"Expected path: {path}. "
                f"Run 'jerry proxy provision' to create the proxy pool first."
            )

        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        manifest = self._deserialise(raw)

        # PI-004: verify hash before returning any data to caller
        self._pool_service.verify_manifest_integrity(manifest)

        return manifest

    def save(self, manifest: PoolManifest) -> None:
        """Atomically write a pool manifest to disk.

        Ensures the engagement directory exists, serialises the manifest to
        YAML, writes to a .tmp sibling file, then uses os.replace() to
        atomically rename to the final path. This prevents partial reads
        by the CLM during manifest updates.

        Args:
            manifest: The PoolManifest to persist.
        """
        path = self._manifest_path(manifest.engagement_id)
        path.parent.mkdir(parents=True, exist_ok=True)

        data = self._serialise(manifest)
        yaml_text = yaml.safe_dump(data, default_flow_style=False, sort_keys=False)

        tmp_path = path.with_suffix(".tmp")
        tmp_path.write_text(yaml_text, encoding="utf-8")
        # Atomic replace — CLM never observes a half-written file
        os.replace(tmp_path, path)

    def exists(self, engagement_id: str) -> bool:
        """Check whether a manifest file exists for an engagement.

        Args:
            engagement_id: Owning engagement identifier.

        Returns:
            True if the manifest file exists on disk.
        """
        return self._manifest_path(engagement_id).exists()

    def delete(self, engagement_id: str) -> None:
        """Delete the pool manifest for an engagement.

        Idempotent — does not raise if no manifest exists. Called during
        engagement teardown after all nodes are destroyed.

        Args:
            engagement_id: Owning engagement identifier.
        """
        path = self._manifest_path(engagement_id)
        if path.exists():
            path.unlink()

    # ------------------------------------------------------------------
    # Serialisation / deserialisation
    # ------------------------------------------------------------------

    def _serialise(self, manifest: PoolManifest) -> dict[str, Any]:
        """Serialise a PoolManifest to a YAML-compatible dictionary.

        Args:
            manifest: The PoolManifest to serialise.

        Returns:
            Dictionary suitable for yaml.safe_dump.
        """
        nodes_data = []
        for node in manifest.pool.nodes:
            nodes_data.append(
                {
                    "id": node.id,
                    "provider": node.provider,
                    "ip": node.ip,
                    "region": node.region,
                    "role": node.role.value,
                    "proxy_type": node.proxy_type.value,
                    "status": node.status.value,
                    "ssh_key_id": node.ssh_key_id,
                    "socks_port": node.socks_port,
                    "created_at": node.created_at.isoformat(),
                    "engagement_id": node.engagement_id,
                    "fingerprint": node.fingerprint,
                }
            )

        return {
            "version": manifest.version,
            "engagement_id": manifest.engagement_id,
            "integrity_hash": manifest.integrity_hash,
            "updated_at": manifest.updated_at.isoformat(),
            "audit_trail": list(manifest.audit_trail),
            "pool": {
                "lb_strategy": manifest.pool.lb_strategy,
                "fail_mode": manifest.pool.fail_mode,
                "max_nodes": manifest.pool.max_nodes,
                "engagement_id": manifest.pool.engagement_id,
                "nodes": nodes_data,
            },
        }

    def _deserialise(self, data: dict[str, Any]) -> PoolManifest:
        """Reconstruct a PoolManifest from a YAML-loaded dictionary.

        Args:
            data: Dictionary loaded from the YAML manifest file.

        Returns:
            Reconstructed PoolManifest domain object.
        """
        pool_data = data["pool"]
        nodes = tuple(
            ProxyNode(
                id=n["id"],
                provider=n["provider"],
                ip=n["ip"],
                region=n["region"],
                role=ProxyRole(n["role"]),
                proxy_type=ProxyType(n["proxy_type"]),
                status=NodeStatus(n["status"]),
                ssh_key_id=n["ssh_key_id"],
                socks_port=int(n["socks_port"]),
                created_at=datetime.fromisoformat(n["created_at"]),
                engagement_id=n["engagement_id"],
                fingerprint=n.get("fingerprint"),
            )
            for n in pool_data.get("nodes", [])
        )

        pool = ProxyPool(
            nodes=nodes,
            lb_strategy=pool_data.get("lb_strategy", "round_robin"),
            fail_mode=pool_data.get("fail_mode", "closed"),
            max_nodes=int(pool_data.get("max_nodes", 10)),
            engagement_id=pool_data.get("engagement_id", ""),
        )

        updated_raw = data.get("updated_at", datetime.now(UTC).isoformat())
        if isinstance(updated_raw, str):
            updated_at = datetime.fromisoformat(updated_raw)
        else:
            updated_at = updated_raw  # type: ignore[assignment]

        return PoolManifest(
            version=str(data.get("version", "1")),
            engagement_id=str(data["engagement_id"]),
            pool=pool,
            integrity_hash=str(data["integrity_hash"]),
            updated_at=updated_at,
            audit_trail=tuple(data.get("audit_trail", [])),
        )
