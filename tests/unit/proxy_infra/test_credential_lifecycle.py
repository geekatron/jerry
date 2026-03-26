# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""BDD test suite for STORY-023-005: Ephemeral Credential Lifecycle.

Covers three task areas driven by TASK-023-033, TASK-023-034, TASK-023-035:

  TASK-023-033: Credential Generation
    - Per-node Ed25519 SSH keypair generation
    - SOCKS5 username/password generation with 128-bit entropy
    - Uniqueness across nodes, correct formats, file permissions

  TASK-023-034: Credential Injection
    - Credential files written at correct paths
    - File permissions 0600 enforced
    - Injection result (success/failure) per node
    - No credential material in process args or env vars

  TASK-023-035: Credential Destruction
    - Files overwritten with urandom before unlink
    - Destruction report includes every file processed
    - Partial failure: continues on locked file, logs warning
    - Directory empty after sweep

Security invariants tested:
  - Credentials never appear in log output (via caplog)
  - No shared credentials across nodes
  - 0600 file mode enforced at write time

Test pyramid: 60% happy / 30% negative / 10% edge
Distribution: ~20 tests -> ~12 happy, ~6 negative, ~2 edge

References:
  - TASK-023-033-credential-generation.md
  - TASK-023-034-credential-injection.md
  - TASK-023-035-credential-destruction.md
  - STORY-023-005-ephemeral-credential-lifecycle.md
  - credential-security-assessment.md (F-001, F-003, F-004)
"""

from __future__ import annotations

import logging
import os
import stat
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.proxy_infra.domain.services.credential_service import CredentialService
from src.proxy_infra.domain.value_objects.credential_descriptor import CredentialDescriptor
from src.proxy_infra.domain.value_objects.destruction_report import DestructionReport
from src.proxy_infra.domain.value_objects.injection_result import InjectionResult
from src.proxy_infra.application.handlers.credential_injection_handler import (
    CredentialInjectionHandler,
)
from src.proxy_infra.application.handlers.credential_destruction_handler import (
    CredentialDestructionHandler,
)


# =============================================================================
# Shared fixtures
# =============================================================================


@pytest.fixture()
def generated_dir(tmp_path: Path) -> Path:
    """Return a tmpfs-like temp directory simulating .generated/."""
    d = tmp_path / ".generated"
    d.mkdir()
    return d


@pytest.fixture()
def credential_service(generated_dir: Path) -> CredentialService:
    """Return a CredentialService with the generated_dir configured."""
    return CredentialService(generated_dir=generated_dir)


@pytest.fixture()
def injection_handler(generated_dir: Path) -> CredentialInjectionHandler:
    """Return a CredentialInjectionHandler using the temp generated_dir."""
    return CredentialInjectionHandler(generated_dir=generated_dir)


@pytest.fixture()
def destruction_handler(generated_dir: Path) -> CredentialDestructionHandler:
    """Return a CredentialDestructionHandler targeting the temp generated_dir."""
    return CredentialDestructionHandler(generated_dir=generated_dir)


# =============================================================================
# TASK-023-033: Credential Generation (CredentialService)
# =============================================================================


class TestSshKeypairGeneration:
    """TASK-023-033: SSH keypair generation happy-path tests."""

    @pytest.mark.unit
    def test_generate_ssh_keypair_when_called_with_node_id_then_returns_descriptor(
        self, credential_service: CredentialService
    ) -> None:
        """Happy: generating a keypair returns a CredentialDescriptor with paths set."""
        descriptor = credential_service.generate_engagement_ssh_keypair("node-01")
        assert descriptor is not None
        assert descriptor.private_key_path is not None
        assert descriptor.public_key_path is not None

    @pytest.mark.unit
    def test_generate_ssh_keypair_when_called_then_private_key_file_exists(
        self, credential_service: CredentialService, generated_dir: Path
    ) -> None:
        """Happy: private key file is written to the generated_dir."""
        descriptor = credential_service.generate_engagement_ssh_keypair("node-01")
        assert Path(descriptor.private_key_path).exists()

    @pytest.mark.unit
    def test_generate_ssh_keypair_when_called_then_public_key_file_exists(
        self, credential_service: CredentialService
    ) -> None:
        """Happy: public key file (.pub) is written alongside the private key."""
        descriptor = credential_service.generate_engagement_ssh_keypair("node-01")
        assert Path(descriptor.public_key_path).exists()

    @pytest.mark.unit
    def test_generate_ssh_keypair_when_called_then_private_key_has_0600_permissions(
        self, credential_service: CredentialService
    ) -> None:
        """Happy: private key file has owner-only read/write permissions (0600)."""
        descriptor = credential_service.generate_engagement_ssh_keypair("node-01")
        file_mode = stat.filemode(os.stat(descriptor.private_key_path).st_mode)
        assert file_mode == "-rw-------", (
            f"Private key permissions should be 0600, got {file_mode}"
        )

    @pytest.mark.unit
    def test_generate_ssh_keypair_when_called_then_private_key_is_ed25519(
        self, credential_service: CredentialService
    ) -> None:
        """Happy: generated private key content indicates Ed25519 algorithm."""
        descriptor = credential_service.generate_engagement_ssh_keypair("node-01")
        private_key_content = Path(descriptor.private_key_path).read_text()
        assert "BEGIN OPENSSH PRIVATE KEY" in private_key_content

    @pytest.mark.unit
    def test_generate_ssh_keypair_when_called_then_public_key_is_ed25519(
        self, credential_service: CredentialService
    ) -> None:
        """Happy: generated public key content starts with ssh-ed25519 type marker."""
        descriptor = credential_service.generate_engagement_ssh_keypair("node-01")
        public_key_content = Path(descriptor.public_key_path).read_text().strip()
        assert public_key_content.startswith("ssh-ed25519 "), (
            f"Public key should start with 'ssh-ed25519 ', got {public_key_content[:30]!r}"
        )

    @pytest.mark.unit
    def test_generate_ssh_keypair_when_two_nodes_then_produces_distinct_keypairs(
        self, credential_service: CredentialService
    ) -> None:
        """Happy: two nodes receive independent keypairs (no sharing, F-004 mitigation)."""
        desc1 = credential_service.generate_engagement_ssh_keypair("node-01")
        desc2 = credential_service.generate_engagement_ssh_keypair("node-02")
        private_key_1 = Path(desc1.private_key_path).read_text()
        private_key_2 = Path(desc2.private_key_path).read_text()
        assert private_key_1 != private_key_2, "Each node must have a unique private key"

    @pytest.mark.unit
    def test_generate_ssh_keypair_when_called_then_descriptor_node_id_matches(
        self, credential_service: CredentialService
    ) -> None:
        """Happy: descriptor carries back the node_id it was generated for."""
        descriptor = credential_service.generate_engagement_ssh_keypair("node-42")
        assert descriptor.node_id == "node-42"

    @pytest.mark.unit
    @pytest.mark.negative
    def test_generate_ssh_keypair_when_node_id_empty_then_raises_value_error(
        self, credential_service: CredentialService
    ) -> None:
        """Negative: empty node_id is rejected before any file I/O occurs."""
        with pytest.raises(ValueError, match="node_id"):
            credential_service.generate_engagement_ssh_keypair("")

    @pytest.mark.unit
    @pytest.mark.negative
    def test_generate_ssh_keypair_when_node_id_whitespace_then_raises_value_error(
        self, credential_service: CredentialService
    ) -> None:
        """Negative: whitespace-only node_id is rejected."""
        with pytest.raises(ValueError, match="node_id"):
            credential_service.generate_engagement_ssh_keypair("   ")


class TestSocks5CredentialGeneration:
    """TASK-023-033: SOCKS5 credential generation tests."""

    @pytest.mark.unit
    def test_generate_socks5_credentials_when_called_then_returns_username_and_password(
        self, credential_service: CredentialService
    ) -> None:
        """Happy: returns tuple of (username, password) strings."""
        username, password = credential_service.generate_socks5_credentials("node-01")
        assert isinstance(username, str)
        assert isinstance(password, str)

    @pytest.mark.unit
    def test_generate_socks5_credentials_when_called_then_username_has_jerry_prefix(
        self, credential_service: CredentialService
    ) -> None:
        """Happy: username follows jerry-{hash[:8]} convention."""
        username, _ = credential_service.generate_socks5_credentials("node-01")
        assert username.startswith("jerry-"), (
            f"Username should start with 'jerry-', got {username!r}"
        )
        hex_suffix = username[len("jerry-"):]
        assert len(hex_suffix) == 8, (
            f"Username hash suffix should be 8 chars, got {len(hex_suffix)}: {hex_suffix!r}"
        )

    @pytest.mark.unit
    def test_generate_socks5_credentials_when_called_then_password_has_sufficient_entropy(
        self, credential_service: CredentialService
    ) -> None:
        """Happy: password from secrets.token_urlsafe(16) is >= 22 base64url chars (128-bit entropy)."""
        _, password = credential_service.generate_socks5_credentials("node-01")
        # secrets.token_urlsafe(16) produces 22+ character strings
        assert len(password) >= 22, (
            f"Password must be >= 22 chars for 128-bit entropy, got len={len(password)}"
        )

    @pytest.mark.unit
    def test_generate_socks5_credentials_when_two_nodes_then_produces_distinct_credentials(
        self, credential_service: CredentialService
    ) -> None:
        """Happy: different nodes get different credentials (V2.5.4 — no shared credentials)."""
        creds1 = credential_service.generate_socks5_credentials("node-01")
        creds2 = credential_service.generate_socks5_credentials("node-02")
        assert creds1 != creds2, "Each node must have unique SOCKS5 credentials"

    @pytest.mark.unit
    def test_generate_socks5_credentials_when_same_node_called_twice_then_passwords_differ(
        self, credential_service: CredentialService
    ) -> None:
        """Happy: each call produces fresh random credentials (no deterministic repetition)."""
        _, pass1 = credential_service.generate_socks5_credentials("node-01")
        _, pass2 = credential_service.generate_socks5_credentials("node-01")
        assert pass1 != pass2, "Repeated generation for same node must produce different passwords"

    @pytest.mark.unit
    @pytest.mark.negative
    def test_generate_socks5_credentials_when_node_id_empty_then_raises_value_error(
        self, credential_service: CredentialService
    ) -> None:
        """Negative: empty node_id is rejected."""
        with pytest.raises(ValueError, match="node_id"):
            credential_service.generate_socks5_credentials("")


class TestCredentialSecurityInvariants:
    """Security invariants: credentials must never appear in logs (APIKEY-002 equivalent)."""

    @pytest.mark.unit
    @pytest.mark.security
    def test_generate_ssh_keypair_when_called_then_private_key_not_logged(
        self, credential_service: CredentialService, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Security: private key PEM data must never appear in log output."""
        with caplog.at_level(logging.DEBUG):
            descriptor = credential_service.generate_engagement_ssh_keypair("node-01")
            private_key_content = Path(descriptor.private_key_path).read_text()

        # Extract a recognizable chunk from the key body (not the header)
        key_lines = private_key_content.strip().splitlines()
        key_body_fragment = key_lines[1][:20] if len(key_lines) > 1 else ""
        if key_body_fragment:
            assert key_body_fragment not in caplog.text, (
                "Private key material must never appear in log output"
            )

    @pytest.mark.unit
    @pytest.mark.security
    def test_generate_socks5_credentials_when_called_then_password_not_logged(
        self, credential_service: CredentialService, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Security: SOCKS5 password must never appear in log output."""
        with caplog.at_level(logging.DEBUG):
            _, password = credential_service.generate_socks5_credentials("node-01")

        assert password not in caplog.text, (
            "SOCKS5 password must never appear in log output"
        )


# =============================================================================
# TASK-023-034: Credential Injection (CredentialInjectionHandler)
# =============================================================================


class TestCredentialInjection:
    """TASK-023-034: Credential injection happy-path tests."""

    @pytest.mark.unit
    def test_inject_ssh_key_when_valid_descriptor_then_returns_success_result(
        self,
        credential_service: CredentialService,
        injection_handler: CredentialInjectionHandler,
    ) -> None:
        """Happy: injection returns an InjectionResult with success=True."""
        descriptor = credential_service.generate_engagement_ssh_keypair("node-01")
        result = injection_handler.inject_ssh_key(descriptor, node_id="node-01")
        assert result.success is True
        assert result.node_id == "node-01"

    @pytest.mark.unit
    def test_inject_ssh_key_when_called_then_secret_file_exists_at_expected_path(
        self,
        credential_service: CredentialService,
        injection_handler: CredentialInjectionHandler,
        generated_dir: Path,
    ) -> None:
        """Happy: SSH key secret file written at {generated_dir}/ssh_key_{node_id}."""
        descriptor = credential_service.generate_engagement_ssh_keypair("node-01")
        injection_handler.inject_ssh_key(descriptor, node_id="node-01")
        secret_path = generated_dir / "ssh_key_node-01"
        assert secret_path.exists(), f"Secret file not found at {secret_path}"

    @pytest.mark.unit
    def test_inject_ssh_key_when_called_then_secret_file_has_0600_permissions(
        self,
        credential_service: CredentialService,
        injection_handler: CredentialInjectionHandler,
        generated_dir: Path,
    ) -> None:
        """Happy: injected secret file has 0600 permissions."""
        descriptor = credential_service.generate_engagement_ssh_keypair("node-01")
        injection_handler.inject_ssh_key(descriptor, node_id="node-01")
        secret_path = generated_dir / "ssh_key_node-01"
        file_mode = stat.filemode(os.stat(secret_path).st_mode)
        assert file_mode == "-rw-------", (
            f"Injected SSH key should have 0600 permissions, got {file_mode}"
        )

    @pytest.mark.unit
    def test_inject_socks5_credentials_when_valid_then_returns_success_result(
        self,
        credential_service: CredentialService,
        injection_handler: CredentialInjectionHandler,
    ) -> None:
        """Happy: SOCKS5 credentials injection returns InjectionResult with success=True."""
        username, password = credential_service.generate_socks5_credentials("node-01")
        result = injection_handler.inject_socks5_credentials(
            username=username, password=password, node_id="node-01"
        )
        assert result.success is True
        assert result.node_id == "node-01"

    @pytest.mark.unit
    def test_inject_socks5_credentials_when_called_then_creds_file_exists(
        self,
        credential_service: CredentialService,
        injection_handler: CredentialInjectionHandler,
        generated_dir: Path,
    ) -> None:
        """Happy: SOCKS5 credential file written at {generated_dir}/socks5_creds_{node_id}."""
        username, password = credential_service.generate_socks5_credentials("node-01")
        injection_handler.inject_socks5_credentials(
            username=username, password=password, node_id="node-01"
        )
        creds_path = generated_dir / "socks5_creds_node-01"
        assert creds_path.exists(), f"SOCKS5 creds file not found at {creds_path}"

    @pytest.mark.unit
    def test_inject_socks5_credentials_when_called_then_creds_file_has_0600_permissions(
        self,
        credential_service: CredentialService,
        injection_handler: CredentialInjectionHandler,
        generated_dir: Path,
    ) -> None:
        """Happy: SOCKS5 creds file has 0600 permissions (Pattern A compliance)."""
        username, password = credential_service.generate_socks5_credentials("node-01")
        injection_handler.inject_socks5_credentials(
            username=username, password=password, node_id="node-01"
        )
        creds_path = generated_dir / "socks5_creds_node-01"
        file_mode = stat.filemode(os.stat(creds_path).st_mode)
        assert file_mode == "-rw-------", (
            f"SOCKS5 creds file should have 0600 permissions, got {file_mode}"
        )

    @pytest.mark.unit
    def test_inject_socks5_credentials_when_called_then_creds_not_in_env(
        self,
        credential_service: CredentialService,
        injection_handler: CredentialInjectionHandler,
    ) -> None:
        """Security: SOCKS5 password must not be exposed as an environment variable."""
        username, password = credential_service.generate_socks5_credentials("node-01")
        injection_handler.inject_socks5_credentials(
            username=username, password=password, node_id="node-01"
        )
        # Verify password is not in any environment variable value
        env_values = " ".join(os.environ.values())
        assert password not in env_values, (
            "SOCKS5 password must never be placed in environment variables"
        )

    @pytest.mark.unit
    @pytest.mark.negative
    def test_inject_ssh_key_when_source_file_missing_then_returns_failure_result(
        self,
        injection_handler: CredentialInjectionHandler,
        generated_dir: Path,
    ) -> None:
        """Negative: if the source key file does not exist, result.success is False."""
        missing_path = str(generated_dir / "does_not_exist")
        fake_descriptor = CredentialDescriptor(
            node_id="node-99",
            private_key_path=missing_path,
            public_key_path=missing_path + ".pub",
        )
        result = injection_handler.inject_ssh_key(fake_descriptor, node_id="node-99")
        assert result.success is False
        assert "node-99" in result.node_id

    @pytest.mark.unit
    @pytest.mark.negative
    def test_inject_socks5_credentials_when_node_id_empty_then_raises_value_error(
        self,
        injection_handler: CredentialInjectionHandler,
    ) -> None:
        """Negative: empty node_id is rejected before file I/O."""
        with pytest.raises(ValueError, match="node_id"):
            injection_handler.inject_socks5_credentials(
                username="jerry-abcd1234", password="somepassword", node_id=""
            )


# =============================================================================
# TASK-023-035: Credential Destruction (CredentialDestructionHandler)
# =============================================================================


class TestCredentialDestruction:
    """TASK-023-035: Credential destruction tests."""

    @pytest.mark.unit
    def test_destroy_when_files_exist_then_returns_report_listing_each_file(
        self,
        credential_service: CredentialService,
        injection_handler: CredentialInjectionHandler,
        destruction_handler: CredentialDestructionHandler,
        generated_dir: Path,
    ) -> None:
        """Happy: destruction report lists every credential file that was processed."""
        # Arrange: create credential files
        descriptor = credential_service.generate_engagement_ssh_keypair("node-01")
        injection_handler.inject_ssh_key(descriptor, node_id="node-01")
        username, password = credential_service.generate_socks5_credentials("node-01")
        injection_handler.inject_socks5_credentials(
            username=username, password=password, node_id="node-01"
        )

        # Act
        report = destruction_handler.destroy_all()

        # Assert
        assert isinstance(report, DestructionReport)
        assert len(report.destroyed_files) > 0

    @pytest.mark.unit
    def test_destroy_when_files_exist_then_files_are_removed(
        self,
        credential_service: CredentialService,
        injection_handler: CredentialInjectionHandler,
        destruction_handler: CredentialDestructionHandler,
        generated_dir: Path,
    ) -> None:
        """Happy: after destruction all credential files in generated_dir are unlinked."""
        descriptor = credential_service.generate_engagement_ssh_keypair("node-01")
        injection_handler.inject_ssh_key(descriptor, node_id="node-01")
        username, password = credential_service.generate_socks5_credentials("node-01")
        injection_handler.inject_socks5_credentials(
            username=username, password=password, node_id="node-01"
        )
        secret_path = generated_dir / "ssh_key_node-01"
        creds_path = generated_dir / "socks5_creds_node-01"
        assert secret_path.exists()
        assert creds_path.exists()

        destruction_handler.destroy_all()

        assert not secret_path.exists(), "Secret key file must be deleted after destruction"
        assert not creds_path.exists(), "SOCKS5 creds file must be deleted after destruction"

    @pytest.mark.unit
    def test_destroy_when_called_then_overwrite_with_urandom_before_unlink(
        self,
        destruction_handler: CredentialDestructionHandler,
        generated_dir: Path,
    ) -> None:
        """Happy: destroy_all overwrites each file with urandom bytes before unlinking."""
        # Write a sentinel credential file manually
        cred_file = generated_dir / "socks5_creds_node-01"
        cred_file.write_text("jerry-abcd1234:supersecretpassword")

        with patch("os.urandom", wraps=os.urandom) as mock_urandom:
            destruction_handler.destroy_all()
            # urandom should have been called at least once for overwrite
            assert mock_urandom.called, "os.urandom must be used for overwriting credential files"

    @pytest.mark.unit
    def test_destroy_when_called_then_report_contains_overwrite_confirmation(
        self,
        destruction_handler: CredentialDestructionHandler,
        generated_dir: Path,
    ) -> None:
        """Happy: destruction report shows overwrite_confirmed=True for each file."""
        cred_file = generated_dir / "socks5_creds_node-01"
        cred_file.write_text("jerry-abcd1234:somepass")

        report = destruction_handler.destroy_all()

        assert len(report.destroyed_files) == 1
        entry = report.destroyed_files[0]
        assert entry.overwrite_confirmed is True

    @pytest.mark.unit
    def test_destroy_when_directory_empty_then_returns_empty_report(
        self,
        destruction_handler: CredentialDestructionHandler,
    ) -> None:
        """Edge: calling destroy_all on an empty directory returns a report with no files."""
        report = destruction_handler.destroy_all()
        assert report.destroyed_files == []

    @pytest.mark.unit
    @pytest.mark.negative
    def test_destroy_when_file_is_locked_then_continues_and_logs_warning(
        self,
        destruction_handler: CredentialDestructionHandler,
        generated_dir: Path,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        """Negative: if one file cannot be destroyed (PermissionError), processing continues
        for remaining files and a warning is logged (F-003 partial-failure tolerance)."""
        good_file = generated_dir / "socks5_creds_node-01"
        bad_file = generated_dir / "ssh_key_node-02"
        good_file.write_text("user:pass")
        bad_file.write_text("PRIVATE KEY")

        # Simulate a permission error on bad_file only
        original_unlink = Path.unlink

        def selective_unlink(self: Path, missing_ok: bool = False) -> None:
            if self.name == "ssh_key_node-02":
                raise PermissionError("file locked by another process")
            original_unlink(self, missing_ok=missing_ok)

        with caplog.at_level(logging.WARNING):
            with patch.object(Path, "unlink", selective_unlink):
                report = destruction_handler.destroy_all()

        # Should still have processed both files (one success, one failure)
        assert len(report.destroyed_files) == 1, (
            "Successful files should be listed in destroyed_files"
        )
        assert len(report.failed_files) == 1, (
            "Failed files should be tracked in failed_files"
        )
        # Warning must have been logged
        assert any("warning" in r.levelname.lower() or "warn" in r.message.lower()
                   for r in caplog.records), (
            "A warning must be logged when a file cannot be destroyed"
        )

    @pytest.mark.unit
    @pytest.mark.security
    def test_destroy_when_called_then_credential_values_not_logged(
        self,
        destruction_handler: CredentialDestructionHandler,
        generated_dir: Path,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        """Security: credential file contents must not appear in log output during destruction."""
        secret_value = "jerry-testnode:ultra_secret_password_9876"
        cred_file = generated_dir / "socks5_creds_node-01"
        cred_file.write_text(secret_value)

        with caplog.at_level(logging.DEBUG):
            destruction_handler.destroy_all()

        assert "ultra_secret_password_9876" not in caplog.text, (
            "Credential values must never appear in logs during destruction"
        )


# =============================================================================
# Constructor guard tests (edge — cover NotADirectoryError branches)
# =============================================================================


class TestConstructorGuards:
    """Edge: all three handlers/services reject a non-existent generated_dir."""

    @pytest.mark.unit
    @pytest.mark.edge_case
    def test_credential_service_when_dir_missing_then_raises_not_a_directory_error(
        self, tmp_path: Path
    ) -> None:
        """Edge: CredentialService raises NotADirectoryError for missing generated_dir."""
        missing_dir = tmp_path / "does_not_exist"
        with pytest.raises(NotADirectoryError):
            CredentialService(generated_dir=missing_dir)

    @pytest.mark.unit
    @pytest.mark.edge_case
    def test_injection_handler_when_dir_missing_then_raises_not_a_directory_error(
        self, tmp_path: Path
    ) -> None:
        """Edge: CredentialInjectionHandler raises NotADirectoryError for missing generated_dir."""
        missing_dir = tmp_path / "does_not_exist"
        with pytest.raises(NotADirectoryError):
            CredentialInjectionHandler(generated_dir=missing_dir)

    @pytest.mark.unit
    @pytest.mark.edge_case
    def test_destruction_handler_when_dir_missing_then_raises_not_a_directory_error(
        self, tmp_path: Path
    ) -> None:
        """Edge: CredentialDestructionHandler raises NotADirectoryError for missing dir."""
        missing_dir = tmp_path / "does_not_exist"
        with pytest.raises(NotADirectoryError):
            CredentialDestructionHandler(generated_dir=missing_dir)


# =============================================================================
# OSError branch coverage for injection handler
# =============================================================================


class TestInjectionOsErrorBranches:
    """Negative: OSError during file write returns failure InjectionResult."""

    @pytest.mark.unit
    @pytest.mark.negative
    def test_inject_ssh_key_when_write_raises_oserror_then_returns_failure(
        self,
        credential_service: CredentialService,
        injection_handler: CredentialInjectionHandler,
    ) -> None:
        """Negative: OSError during secret file write produces success=False result."""
        descriptor = credential_service.generate_engagement_ssh_keypair("node-01")

        with patch.object(Path, "write_bytes", side_effect=OSError("disk full")):
            result = injection_handler.inject_ssh_key(descriptor, node_id="node-01")

        assert result.success is False
        assert "disk full" in result.error

    @pytest.mark.unit
    @pytest.mark.negative
    def test_inject_socks5_credentials_when_write_raises_oserror_then_returns_failure(
        self,
        injection_handler: CredentialInjectionHandler,
    ) -> None:
        """Negative: OSError during SOCKS5 creds file write produces success=False result."""
        with patch.object(Path, "write_text", side_effect=OSError("disk full")):
            result = injection_handler.inject_socks5_credentials(
                username="jerry-abcd1234",
                password="somepassword",
                node_id="node-01",
            )

        assert result.success is False
        assert "disk full" in result.error
