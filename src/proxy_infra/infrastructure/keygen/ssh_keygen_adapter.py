# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""SshKeygenAdapter — infrastructure adapter for Ed25519 SSH keypair generation.

Wraps the ``ssh-keygen`` system command to produce per-engagement Ed25519
keypairs.  The private key is written with 0600 permissions; the public key
is written as a ``.pub`` sibling.

Security properties:
    - Private key file permissions enforced to 0600 immediately after generation.
    - Key comment contains the engagement ID for traceability.
    - No passphrase (``-N ""``) — keys are ephemeral and shredded at teardown.

Design constraints:
    H-07: Infrastructure layer — wraps system command, no domain logic.
    H-10: One public class per file.
    H-11: All public methods have type annotations.

References:
    - TASK-023-051: SSH keypair generation infrastructure adapter
    - FEAT-023-004: Hands-Free Engagement Pipeline Automation
    - F-002: SSH key generated per engagement, never shared across pool
"""

from __future__ import annotations

import logging
import os
import subprocess
from pathlib import Path

from src.proxy_infra.infrastructure.keygen.keygen_result import KeygenResult

logger = logging.getLogger(__name__)


class SshKeygenAdapter:
    """Generates Ed25519 SSH keypairs for engagement provisioning.

    Invokes ``ssh-keygen -t ed25519`` via subprocess.  The generated keypair
    is named ``id_ed25519_{engagement_id}`` and placed in the specified
    credential directory.
    """

    def generate(
        self,
        engagement_id: str,
        credential_dir: Path,
    ) -> KeygenResult:
        """Generate an Ed25519 SSH keypair for an engagement.

        Args:
            engagement_id: Engagement identifier used in the key filename
                and comment.
            credential_dir: Directory where the keypair files are written.
                Must exist and be writable.

        Returns:
            KeygenResult with paths to the private and public key files.

        Raises:
            NotADirectoryError: If credential_dir does not exist.
            subprocess.CalledProcessError: If ssh-keygen fails.
        """
        if not credential_dir.exists() or not credential_dir.is_dir():
            raise NotADirectoryError(
                f"Credential directory does not exist: {credential_dir}"
            )

        key_name = f"id_ed25519_{engagement_id}"
        private_key_path = credential_dir / key_name
        public_key_path = credential_dir / f"{key_name}.pub"

        # Remove existing key files to allow ssh-keygen to write fresh
        for p in (private_key_path, public_key_path):
            if p.exists():
                p.unlink()

        comment = f"jerry-proxy-{engagement_id}"

        subprocess.run(
            [
                "ssh-keygen",
                "-t", "ed25519",
                "-C", comment,
                "-f", str(private_key_path),
                "-N", "",  # No passphrase — ephemeral key, shredded at teardown
            ],
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
        )

        # Enforce 0600 on private key (ssh-keygen should set this, but we enforce)
        os.chmod(private_key_path, 0o600)

        logger.debug(
            "Generated Ed25519 keypair for engagement=%r at %s",
            engagement_id,
            private_key_path,
        )

        return KeygenResult(
            private_key_path=private_key_path,
            public_key_path=public_key_path,
        )
