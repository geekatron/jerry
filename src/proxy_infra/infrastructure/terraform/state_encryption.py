# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""State file encryption with age for terraform state protection.

Encrypts terraform.tfstate with age after every terraform operation and
decrypts before operations that read state. Per OPSEC control R-001:
plaintext state files must never rest unencrypted on disk.

References:
    - TASK-023-103: State encryption with age
    - ADR-EN023-003: Infrastructure provisioning (Option C: Hybrid)
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

from src.proxy_infra.infrastructure.terraform.age_not_found_error import (
    AgeNotFoundError,
)
from src.proxy_infra.infrastructure.terraform.encryption_error import (
    EncryptionError,
)
from src.proxy_infra.infrastructure.terraform.state_file_not_found_error import (
    StateFileNotFoundError,
)


class StateEncryption:
    """Encrypts and decrypts terraform state files using age.

    The encryption lifecycle ensures that plaintext state never persists
    on disk after a terraform operation completes. Encrypted state is
    stored as terraform.tfstate.age alongside the terraform working
    directory.

    All subprocess calls use list args (never shell=True) per T-009.

    Attributes:
        engagement_dir: Engagement-scoped directory containing state files.
        age_recipient: age public key for encryption.
        age_binary: Path or name of the age binary.
    """

    def __init__(
        self,
        engagement_dir: Path,
        age_recipient: str,
        age_binary: str = "age",
    ) -> None:
        """Initialise state encryption with age recipient public key.

        Args:
            engagement_dir: Directory containing terraform state files.
            age_recipient: age recipient public key (starts with 'age1').
            age_binary: Path or name of the age binary. Defaults to 'age'.
        """
        self._engagement_dir = engagement_dir
        self._recipient = age_recipient
        self._age_binary = age_binary

    @property
    def _state_file(self) -> Path:
        """Path to the plaintext terraform state file.

        Returns:
            Path to terraform.tfstate in the engagement directory.
        """
        return self._engagement_dir / "terraform.tfstate"

    @property
    def _encrypted_file(self) -> Path:
        """Path to the encrypted terraform state file.

        Returns:
            Path to terraform.tfstate.age in the engagement directory.
        """
        return self._engagement_dir / "terraform.tfstate.age"

    def encrypt_state(self) -> Path:
        """Encrypt terraform.tfstate and remove plaintext.

        Reads the plaintext state file, encrypts it with age using the
        configured recipient public key, writes the ciphertext to
        terraform.tfstate.age, then removes the plaintext file.

        Returns:
            Path to the encrypted .age file.

        Raises:
            StateFileNotFoundError: If terraform.tfstate does not exist.
            AgeNotFoundError: If the age binary is not found.
            EncryptionError: If encryption fails.
        """
        if not self._state_file.exists():
            raise StateFileNotFoundError(
                f"terraform.tfstate not found at {self._state_file} — "
                f"cannot encrypt nonexistent state file"
            )

        try:
            result = subprocess.run(
                [
                    self._age_binary,
                    "--encrypt",
                    "--recipient",
                    self._recipient,
                    "--output",
                    str(self._encrypted_file),
                    str(self._state_file),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
        except FileNotFoundError as exc:
            raise AgeNotFoundError(
                f"age binary not found at '{self._age_binary}' — "
                f"install age (https://github.com/FiloSottile/age) "
                f"and ensure it is in PATH"
            ) from exc

        if result.returncode != 0:
            raise EncryptionError(
                f"age encryption failed (exit {result.returncode}): {result.stderr}"
            )

        os.chmod(self._encrypted_file, 0o600)
        self._state_file.unlink()

        return self._encrypted_file

    def decrypt_state(self) -> Path:
        """Decrypt terraform.tfstate.age to terraform.tfstate.

        Reads the encrypted state file, decrypts it with age using the
        configured identity (from AGE_IDENTITY_FILE env var or default path),
        and writes the plaintext to terraform.tfstate.

        Returns:
            Path to the decrypted terraform.tfstate file.

        Raises:
            StateFileNotFoundError: If terraform.tfstate.age does not exist.
            AgeNotFoundError: If the age binary is not found.
            EncryptionError: If decryption fails.
        """
        if not self._encrypted_file.exists():
            raise StateFileNotFoundError(
                f"terraform.tfstate.age not found at {self._encrypted_file} — "
                f"cannot decrypt nonexistent encrypted state file"
            )

        identity_file = os.environ.get(
            "AGE_IDENTITY_FILE",
            str(Path.home() / ".config" / "jerry" / "age-identity.txt"),
        )

        try:
            result = subprocess.run(
                [
                    self._age_binary,
                    "--decrypt",
                    "--identity",
                    identity_file,
                    "--output",
                    str(self._state_file),
                    str(self._encrypted_file),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
        except FileNotFoundError as exc:
            raise AgeNotFoundError(
                f"age binary not found at '{self._age_binary}' — "
                f"install age and ensure it is in PATH"
            ) from exc

        if result.returncode != 0:
            raise EncryptionError(
                f"age decryption failed (exit {result.returncode}): {result.stderr}"
            )

        os.chmod(self._state_file, 0o600)

        return self._state_file
