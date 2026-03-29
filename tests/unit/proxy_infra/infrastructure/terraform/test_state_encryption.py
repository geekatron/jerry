# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""RED phase tests for TASK-023-103: State Encryption with age.

Tests verify:
1. encrypt_state() produces .age file and removes plaintext
2. decrypt_state() restores original JSON content
3. Round-trip integrity
4. Missing age binary raises clear error
5. Encrypted file is not valid JSON
6. Error on nonexistent state file
7. Error on missing encrypted file
8. No shell=True in subprocess calls

All tests MUST FAIL before implementation (H-20 RED phase).
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest


@pytest.fixture()
def age_keypair(tmp_path: Path) -> tuple[str, Path]:
    """Generate a temporary age keypair for testing.

    Returns:
        Tuple of (recipient public key, identity file path).
    """
    identity_file = tmp_path / "age-identity.txt"
    result = subprocess.run(
        ["age-keygen", "-o", str(identity_file)],
        capture_output=True,
        text=True,
        check=True,
    )
    # Extract public key from stderr (age-keygen prints it there)
    for line in result.stderr.splitlines():
        if line.startswith("Public key:"):
            recipient = line.split(": ", 1)[1].strip()
            return recipient, identity_file
    # Fallback: read from the key file comment
    for line in identity_file.read_text().splitlines():
        if line.startswith("# public key:"):
            recipient = line.split(": ", 1)[1].strip()
            return recipient, identity_file
    raise RuntimeError("Could not extract public key from age-keygen output")


class TestStateEncryptionEncrypt:
    """Tests for encrypt_state() method."""

    def test_encrypt_state_produces_age_file(
        self, tmp_path: Path, age_keypair: tuple[str, Path]
    ) -> None:
        """encrypt_state() must write terraform.tfstate.age in engagement dir."""
        from src.proxy_infra.infrastructure.terraform.state_encryption import (
            StateEncryption,
        )

        recipient, _identity = age_keypair
        state_file = tmp_path / "terraform.tfstate"
        state_file.write_text(json.dumps({"version": 4, "resources": []}))

        encryption = StateEncryption(
            engagement_dir=tmp_path,
            age_recipient=recipient,
        )
        result = encryption.encrypt_state()

        assert result.exists()
        assert result.name == "terraform.tfstate.age"

    def test_encrypt_state_removes_plaintext_after_encryption(
        self, tmp_path: Path, age_keypair: tuple[str, Path]
    ) -> None:
        """terraform.tfstate must be deleted after .age file is written."""
        from src.proxy_infra.infrastructure.terraform.state_encryption import (
            StateEncryption,
        )

        recipient, _identity = age_keypair
        state_file = tmp_path / "terraform.tfstate"
        state_file.write_text(json.dumps({"version": 4, "resources": []}))

        encryption = StateEncryption(
            engagement_dir=tmp_path,
            age_recipient=recipient,
        )
        encryption.encrypt_state()

        assert not state_file.exists(), "Plaintext state must be removed after encryption"

    def test_encrypted_file_is_not_valid_json(
        self, tmp_path: Path, age_keypair: tuple[str, Path]
    ) -> None:
        """The .age file must not be parseable as JSON (verifies encryption occurred)."""
        from src.proxy_infra.infrastructure.terraform.state_encryption import (
            StateEncryption,
        )

        recipient, _identity = age_keypair
        state_file = tmp_path / "terraform.tfstate"
        state_file.write_text(json.dumps({"version": 4, "resources": []}))

        encryption = StateEncryption(
            engagement_dir=tmp_path,
            age_recipient=recipient,
        )
        result = encryption.encrypt_state()

        with pytest.raises((json.JSONDecodeError, UnicodeDecodeError)):
            json.loads(result.read_bytes().decode("utf-8", errors="strict"))


class TestStateEncryptionDecrypt:
    """Tests for decrypt_state() method."""

    def test_decrypt_state_restores_original_json(
        self, tmp_path: Path, age_keypair: tuple[str, Path], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """decrypt_state() must produce valid JSON matching original content."""
        from src.proxy_infra.infrastructure.terraform.state_encryption import (
            StateEncryption,
        )

        recipient, identity_file = age_keypair
        monkeypatch.setenv("AGE_IDENTITY_FILE", str(identity_file))

        original = {"version": 4, "resources": [{"type": "test"}]}
        state_file = tmp_path / "terraform.tfstate"
        state_file.write_text(json.dumps(original))

        encryption = StateEncryption(
            engagement_dir=tmp_path,
            age_recipient=recipient,
        )
        encryption.encrypt_state()
        decrypted_path = encryption.decrypt_state()

        decrypted = json.loads(decrypted_path.read_text())
        assert decrypted == original

    def test_round_trip_integrity(
        self, tmp_path: Path, age_keypair: tuple[str, Path], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Encrypt then decrypt must produce byte-identical content."""
        from src.proxy_infra.infrastructure.terraform.state_encryption import (
            StateEncryption,
        )

        recipient, identity_file = age_keypair
        monkeypatch.setenv("AGE_IDENTITY_FILE", str(identity_file))

        original_content = json.dumps({"version": 4, "resources": []}, indent=2)
        state_file = tmp_path / "terraform.tfstate"
        state_file.write_text(original_content)

        encryption = StateEncryption(
            engagement_dir=tmp_path,
            age_recipient=recipient,
        )
        encryption.encrypt_state()
        decrypted_path = encryption.decrypt_state()

        assert decrypted_path.read_text() == original_content


class TestStateEncryptionErrors:
    """Tests for error handling."""

    def test_missing_age_binary_raises_clear_error(self, tmp_path: Path) -> None:
        """AgeNotFoundError must be raised with helpful message when age not in PATH."""
        from src.proxy_infra.infrastructure.terraform.age_not_found_error import (
            AgeNotFoundError,
        )
        from src.proxy_infra.infrastructure.terraform.state_encryption import (
            StateEncryption,
        )

        state_file = tmp_path / "terraform.tfstate"
        state_file.write_text("{}")

        encryption = StateEncryption(
            engagement_dir=tmp_path,
            age_recipient="age1test",
            age_binary="/nonexistent/age",
        )

        with pytest.raises(AgeNotFoundError):
            encryption.encrypt_state()

    def test_encrypt_state_raises_on_nonexistent_state_file(self, tmp_path: Path) -> None:
        """StateFileNotFoundError when terraform.tfstate is absent."""
        from src.proxy_infra.infrastructure.terraform.state_encryption import (
            StateEncryption,
        )
        from src.proxy_infra.infrastructure.terraform.state_file_not_found_error import (
            StateFileNotFoundError,
        )

        encryption = StateEncryption(
            engagement_dir=tmp_path,
            age_recipient="age1test",
        )

        with pytest.raises(StateFileNotFoundError):
            encryption.encrypt_state()

    def test_decrypt_state_raises_on_missing_encrypted_file(self, tmp_path: Path) -> None:
        """Clear error when .age file is absent."""
        from src.proxy_infra.infrastructure.terraform.state_encryption import (
            StateEncryption,
        )
        from src.proxy_infra.infrastructure.terraform.state_file_not_found_error import (
            StateFileNotFoundError,
        )

        encryption = StateEncryption(
            engagement_dir=tmp_path,
            age_recipient="age1test",
        )

        with pytest.raises(StateFileNotFoundError):
            encryption.decrypt_state()

    def test_age_subprocess_uses_list_args_not_shell_true(self) -> None:
        """Architecture test: no shell=True in state_encryption.py."""
        import ast

        source = Path("src/proxy_infra/infrastructure/terraform/state_encryption.py")
        if not source.exists():
            pytest.skip("state_encryption.py not yet created")

        tree = ast.parse(source.read_text())
        violations = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Attribute) and func.attr == "run":
                    for kw in node.keywords:
                        if kw.arg == "shell" and isinstance(kw.value, ast.Constant):
                            if kw.value.value is True:
                                violations.append(f"line {node.lineno}")

        assert violations == [], f"T-009 violation: shell=True in state_encryption.py: {violations}"
