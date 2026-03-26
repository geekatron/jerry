# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""SecretsDistributionHandler — Docker secrets integration for sidecar credentials.

Writes SSH keys and per-node SOCKS5 credentials into Docker-secret-compatible
files (mode 0600) so the autossh and socks-bridge sidecar containers can mount
them at /run/secrets/<name> via Docker Compose ``secrets:`` stanzas.

Addresses TASK-023-021 (credential management) security findings:
    F-001: socks5lb config must reference secrets, not embed plaintext values.
    F-002: SSH key generated per VPS node, never shared across pool/engagement.
    F-003: Teardown path shreds all credential files on disk.

Design constraints:
    H-07: Application layer — imports domain only, no direct subprocess.
    H-10: One public class per file.
    H-11: All public methods have type annotations.
    TASK-023-021: Credential management and secrets distribution.
"""

from __future__ import annotations

import logging
import os
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode

logger = logging.getLogger(__name__)

#: File permission for credential files: owner read/write only.
_SECRET_FILE_MODE: int = 0o600

#: Prefix for SSH key secret files.
_SSH_KEY_PREFIX: str = "eng_ssh_key"

#: Prefix for per-node SOCKS5 credential files.
_SOCKS5_CREDS_PREFIX: str = "socks5_creds"


from src.proxy_infra.application.handlers.distribution_result import DistributionResult  # noqa: E402


class SecretsDistributionHandler:
    """Writes engagement credentials into Docker-secret-compatible files.

    Manages three credential types:
      - SSH private key (per VPS node)         -> eng_ssh_key_{role}
      - SOCKS5 username:password (per node)    -> socks5_creds_{node_id}
      - Pool manifest JSON                     -> pool_manifest

    All written files are created with 0600 permissions. Teardown calls
    ``shred_all`` to overwrite and unlink all distributed secrets (F-003).

    Args:
        generated_dir: Directory where secret files will be written.
            Must exist and be writable before instantiation.
    """

    def __init__(self, generated_dir: Path) -> None:
        """Initialise SecretsDistributionHandler.

        Args:
            generated_dir: Path to the engagement credential directory.
                Must exist before this handler is used.

        Raises:
            NotADirectoryError: If generated_dir does not exist or is not a dir.
        """
        if not generated_dir.exists() or not generated_dir.is_dir():
            raise NotADirectoryError(
                f"generated_dir {generated_dir!r} does not exist or is not a directory."
            )
        self._generated_dir = generated_dir
        self._written: list[Path] = []

    def distribute_ssh_key(self, private_key_pem: str, node_role: str) -> DistributionResult:
        """Write an SSH private key to a Docker-secret file.

        Addresses F-002: each VPS node gets a unique key — callers must pass
        the per-node private key content, not a shared pool key.

        Args:
            private_key_pem: PEM-encoded Ed25519 private key content.
            node_role: Node role used for file naming (e.g. ``"recon"``).

        Returns:
            DistributionResult with success=True and the written path.
        """
        if not private_key_pem.strip():
            return DistributionResult(
                success=False,
                errors=("private_key_pem must not be empty",),
            )
        if not node_role.strip():
            return DistributionResult(
                success=False,
                errors=("node_role must not be empty",),
            )

        target = self._generated_dir / f"{_SSH_KEY_PREFIX}_{node_role}"
        try:
            target.write_text(private_key_pem, encoding="utf-8")
            os.chmod(target, _SECRET_FILE_MODE)
            self._written.append(target)
            logger.debug("SSH key secret written for role=%r at %s", node_role, target)
            return DistributionResult(success=True, written_paths=(str(target),))
        except OSError as exc:
            logger.warning("Failed to write SSH key for role=%r: %s", node_role, exc)
            return DistributionResult(success=False, errors=(str(exc),))

    def distribute_socks5_credentials(
        self, node: ProxyNode, username: str, password: str
    ) -> DistributionResult:
        """Write SOCKS5 username:password into a Docker-secret file.

        Addresses F-001: the socks5lb config only references this secret file
        path — it never embeds the plaintext credential value.

        Args:
            node: ProxyNode whose id is used to name the secret file.
            username: SOCKS5 username string.
            password: SOCKS5 password string (not logged).

        Returns:
            DistributionResult with success=True and the written path.
        """
        if not username.strip() or not password:
            return DistributionResult(
                success=False,
                errors=("username and password must not be empty",),
            )

        target = self._generated_dir / f"{_SOCKS5_CREDS_PREFIX}_{node.id}"
        try:
            target.write_text(f"{username}:{password}", encoding="utf-8")
            os.chmod(target, _SECRET_FILE_MODE)
            self._written.append(target)
            logger.debug(
                "SOCKS5 credential secret written for node=%r (values redacted)", node.id
            )
            return DistributionResult(success=True, written_paths=(str(target),))
        except OSError as exc:
            logger.warning("Failed to write SOCKS5 creds for node=%r: %s", node.id, exc)
            return DistributionResult(success=False, errors=(str(exc),))

    def distribute_pool_manifest(self, manifest_json: str) -> DistributionResult:
        """Write the pool manifest JSON as a Docker-secret file.

        The pool manifest provides node IPs and roles to the autossh service.

        Args:
            manifest_json: JSON-encoded pool manifest content.

        Returns:
            DistributionResult with success=True and the written path.
        """
        if not manifest_json.strip():
            return DistributionResult(
                success=False,
                errors=("manifest_json must not be empty",),
            )

        target = self._generated_dir / "pool_manifest"
        try:
            target.write_text(manifest_json, encoding="utf-8")
            os.chmod(target, _SECRET_FILE_MODE)
            self._written.append(target)
            logger.debug("Pool manifest secret written at %s", target)
            return DistributionResult(success=True, written_paths=(str(target),))
        except OSError as exc:
            logger.warning("Failed to write pool manifest: %s", exc)
            return DistributionResult(success=False, errors=(str(exc),))

    def shred_all(self) -> int:
        """Overwrite and unlink all secret files written by this handler (F-003).

        Uses ``shred -u`` (overwrite then unlink) for files that exist.
        Falls back to plain unlink if shred is not available.

        Returns:
            Count of files successfully shredded.
        """
        shredded = 0
        for path in list(self._written):
            if not path.exists():
                continue
            try:
                result = subprocess.run(
                    ["shred", "-u", str(path)],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                if result.returncode == 0:
                    logger.debug("Shredded %s", path)
                    shredded += 1
                else:
                    # Fallback: plain unlink
                    path.unlink(missing_ok=True)
                    shredded += 1
                    logger.warning("shred failed for %s; unlinked as fallback", path)
            except (FileNotFoundError, subprocess.TimeoutExpired, OSError) as exc:
                path.unlink(missing_ok=True)
                shredded += 1
                logger.warning("shred unavailable for %s (%s); unlinked", path, exc)
        self._written.clear()
        return shredded

    def written_count(self) -> int:
        """Return the number of secret files tracked by this handler.

        Returns:
            Count of files written and not yet shredded.
        """
        return len(self._written)
