# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""CredentialInjectionHandler — application handler for writing generated credentials
into Docker-secrets-compatible files on the operator's host.

Writes SSH private keys and SOCKS5 credential files to the engagement's
generated_dir with 0600 permissions, making them available for Docker
Compose secret mounts at /run/secrets/<name> inside containers.

This addresses TASK-023-034 (F-001 remediation): credentials are never
placed in environment variables or process arguments — only in 0600 files
readable by the Docker daemon for secret injection.

Security invariants:
  - All written files enforced 0600 permissions (owner-only r/w)
  - Credential values never passed to log calls
  - node_id validated before any I/O

References:
  - TASK-023-034: Credential injection specification
  - STORY-023-005: Ephemeral Credential Lifecycle
  - credential-security-assessment.md: Pattern A (Docker Compose secrets)
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import TYPE_CHECKING

from src.proxy_infra.domain.value_objects.injection_result import InjectionResult

if TYPE_CHECKING:
    from src.proxy_infra.domain.value_objects.credential_descriptor import CredentialDescriptor

_logger = logging.getLogger(__name__)


class CredentialInjectionHandler:
    """Writes generated credential material to Docker-secret-compatible files.

    Injects:
      - SSH private keys  ->  {generated_dir}/ssh_key_{node_id}
      - SOCKS5 credentials -> {generated_dir}/socks5_creds_{node_id}

    All written files are created with 0600 permissions. The files are
    intended to be referenced by Docker Compose ``secrets:`` stanzas, which
    bind-mount them read-only into containers at /run/secrets/<name>.

    Args:
        generated_dir: The engagement's generated credential directory
            (typically a tmpfs-backed .generated/ path).
    """

    def __init__(self, generated_dir: Path) -> None:
        """Initialise CredentialInjectionHandler.

        Args:
            generated_dir: Directory where secret files will be written.
                Must exist before this handler is used.

        Raises:
            NotADirectoryError: If generated_dir does not exist or is not a
                directory.
        """
        if not generated_dir.exists() or not generated_dir.is_dir():
            raise NotADirectoryError(
                f"generated_dir {generated_dir!r} does not exist or is not a directory. "
                "Create the directory before instantiating CredentialInjectionHandler."
            )
        self._generated_dir = generated_dir

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    def inject_ssh_key(
        self,
        descriptor: CredentialDescriptor,
        node_id: str,
    ) -> InjectionResult:
        """Copy the SSH private key from descriptor into a Docker-secret file.

        Reads the private key from descriptor.private_key_path and writes it
        to {generated_dir}/ssh_key_{node_id} with 0600 permissions.

        Args:
            descriptor: Credential descriptor produced by CredentialService.
                Must have a valid private_key_path.
            node_id: Proxy node identifier used to name the secret file.

        Returns:
            InjectionResult with success=True on success, or success=False
            with an error message if the source file cannot be read.
        """
        self._validate_node_id(node_id)

        secret_path = self._generated_dir / f"ssh_key_{node_id}"
        source_path = Path(descriptor.private_key_path)

        if not source_path.exists():
            _logger.warning(
                "SSH key injection failed for node %r: source file not found at %r",
                node_id,
                str(source_path),
            )
            return InjectionResult(
                node_id=node_id,
                success=False,
                error=(
                    f"Source private key file not found: {descriptor.private_key_path!r}. "
                    "Generate the keypair before injecting."
                ),
            )

        try:
            key_bytes = source_path.read_bytes()
            secret_path.write_bytes(key_bytes)
            os.chmod(secret_path, 0o600)
            _logger.debug(
                "SSH key secret file written for node %r at %r",
                node_id,
                str(secret_path),
            )
            return InjectionResult(
                node_id=node_id,
                success=True,
                secret_path=str(secret_path),
            )
        except OSError as exc:
            _logger.warning(
                "SSH key injection failed for node %r: %s",
                node_id,
                exc,
            )
            return InjectionResult(
                node_id=node_id,
                success=False,
                error=str(exc),
            )

    def inject_socks5_credentials(
        self,
        username: str,
        password: str,
        node_id: str,
    ) -> InjectionResult:
        """Write SOCKS5 username:password into a Docker-secret file.

        Writes ``{username}:{password}`` to {generated_dir}/socks5_creds_{node_id}
        with 0600 permissions. The file content is never logged.

        Args:
            username: SOCKS5 username (e.g. ``jerry-a1b2c3d4``).
            password: SOCKS5 password (128-bit entropy from
                ``secrets.token_urlsafe``).
            node_id: Proxy node identifier used to name the secret file.

        Returns:
            InjectionResult with success=True on success.

        Raises:
            ValueError: If node_id is empty or whitespace-only.
        """
        self._validate_node_id(node_id)

        creds_path = self._generated_dir / f"socks5_creds_{node_id}"

        try:
            creds_path.write_text(f"{username}:{password}", encoding="utf-8")
            os.chmod(creds_path, 0o600)
            _logger.debug(
                "SOCKS5 credential secret file written for node %r at %r "
                "(credential values redacted)",
                node_id,
                str(creds_path),
            )
            return InjectionResult(
                node_id=node_id,
                success=True,
                secret_path=str(creds_path),
            )
        except OSError as exc:
            _logger.warning(
                "SOCKS5 credentials injection failed for node %r: %s",
                node_id,
                exc,
            )
            return InjectionResult(
                node_id=node_id,
                success=False,
                error=str(exc),
            )

    # -------------------------------------------------------------------------
    # Private helpers
    # -------------------------------------------------------------------------

    @staticmethod
    def _validate_node_id(node_id: str) -> None:
        """Validate node_id is non-empty and non-whitespace.

        Args:
            node_id: The node identifier to validate.

        Raises:
            ValueError: If node_id fails validation.
        """
        if not isinstance(node_id, str) or not node_id.strip():
            raise ValueError(
                f"node_id must be a non-empty, non-whitespace string. "
                f"Received: {node_id!r}."
            )
