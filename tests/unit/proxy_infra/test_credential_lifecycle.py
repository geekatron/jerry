# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""BDD test suite for STORY-023-005: Ephemeral Credential Lifecycle.

Architecture alignment (post-H-07 refactor):
  CredentialService  — pure domain; returns strings/tuples only; no file I/O.
  CredentialInjectionHandler  — application layer; writes 0600 secret files.
  CredentialDestructionHandler — application layer; urandom-overwrites + unlinks.

Test pyramid: 60% happy / 30% negative / 10% edge
Distribution: ~26 tests -> ~16 happy, ~8 negative, ~2 edge

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
from unittest.mock import patch

import pytest

from src.proxy_infra.application.handlers.credential_destruction_handler import (
    CredentialDestructionHandler,
)
from src.proxy_infra.application.handlers.credential_injection_handler import (
    CredentialInjectionHandler,
)
from src.proxy_infra.domain.services.credential_service import CredentialService
from src.proxy_infra.domain.value_objects.credential_descriptor import CredentialDescriptor

# Fake SSH key content used in tests.
# Deliberately NOT a real key header so it cannot be mistaken for live material.
_FAKE_SSH_KEY_BYTES: bytes = b"FAKE-TEST-KEY-DO-NOT-USE:" + b"A" * 64


# =============================================================================
# Shared fixtures
# =============================================================================


@pytest.fixture()
def generated_dir(tmp_path: Path) -> Path:
    """Return a temp directory simulating the engagement .generated/ directory."""
    d = tmp_path / ".generated"
    d.mkdir()
    return d


@pytest.fixture()
def credential_service() -> CredentialService:
    """Return a stateless CredentialService (no constructor args — pure domain)."""
    return CredentialService()


@pytest.fixture()
def injection_handler(generated_dir: Path) -> CredentialInjectionHandler:
    """Return a CredentialInjectionHandler targeting the temp generated_dir."""
    return CredentialInjectionHandler(generated_dir=generated_dir)


@pytest.fixture()
def destruction_handler(generated_dir: Path) -> CredentialDestructionHandler:
    """Return a CredentialDestructionHandler targeting the temp generated_dir."""
    return CredentialDestructionHandler(generated_dir=generated_dir)


def _make_descriptor(node_id: str, generated_dir: Path) -> CredentialDescriptor:
    """Write placeholder key files and return a CredentialDescriptor.

    Uses synthetic, non-real key bytes so that secret-scanning hooks are not
    triggered. The injection handler reads these bytes and copies them to the
    secret file — the content is irrelevant for injection/permission tests.
    """
    private_key_path = generated_dir / f"id_ed25519_{node_id}"
    public_key_path = generated_dir / f"id_ed25519_{node_id}.pub"
    private_key_path.write_bytes(_FAKE_SSH_KEY_BYTES)
    public_key_path.write_bytes(b"ssh-ed25519 FAKEPUBKEY jerry-proxy-" + node_id.encode())
    os.chmod(private_key_path, 0o600)
    return CredentialDescriptor(
        node_id=node_id,
        private_key_path=str(private_key_path),
        public_key_path=str(public_key_path),
    )


# =============================================================================
# TASK-023-033: CredentialService — pure domain logic
# =============================================================================


class TestSocks5CredentialGeneration:
    """TASK-023-033: SOCKS5 credential generation — pure domain, no I/O."""

    @pytest.mark.unit
    def test_generate_socks5_credentials_when_called_then_returns_username_and_password(
        self, credential_service: CredentialService
    ) -> None:
        """Happy: returns a tuple of two non-empty strings."""
        username, password = credential_service.generate_socks5_credentials("node-01")
        assert isinstance(username, str) and username
        assert isinstance(password, str) and password

    @pytest.mark.unit
    def test_generate_socks5_credentials_when_called_then_username_has_jerry_prefix(
        self, credential_service: CredentialService
    ) -> None:
        """Happy: username follows jerry-{sha256[:8]} convention."""
        username, _ = credential_service.generate_socks5_credentials("node-01")
        assert username.startswith("jerry-"), (
            f"Username should start with 'jerry-', got {username!r}"
        )
        hex_suffix = username[len("jerry-"):]
        assert len(hex_suffix) == 8, (
            f"Username hash suffix should be 8 hex chars, got {len(hex_suffix)}: {hex_suffix!r}"
        )

    @pytest.mark.unit
    def test_generate_socks5_credentials_when_called_then_password_has_sufficient_entropy(
        self, credential_service: CredentialService
    ) -> None:
        """Happy: password from secrets.token_urlsafe(16) is >= 22 base64url characters."""
        _, password = credential_service.generate_socks5_credentials("node-01")
        assert len(password) >= 22, (
            f"Password must be >= 22 chars for 128-bit entropy, got len={len(password)}"
        )

    @pytest.mark.unit
    def test_generate_socks5_credentials_when_two_nodes_then_produces_distinct_credentials(
        self, credential_service: CredentialService
    ) -> None:
        """Happy: different node IDs produce different credentials (no shared creds, F-004)."""
        creds1 = credential_service.generate_socks5_credentials("node-01")
        creds2 = credential_service.generate_socks5_credentials("node-02")
        assert creds1 != creds2, "Each node must receive unique SOCKS5 credentials"

    @pytest.mark.unit
    def test_generate_socks5_credentials_when_same_node_called_twice_then_passwords_differ(
        self, credential_service: CredentialService
    ) -> None:
        """Happy: each call issues a fresh random password (no deterministic repetition)."""
        _, pass1 = credential_service.generate_socks5_credentials("node-01")
        _, pass2 = credential_service.generate_socks5_credentials("node-01")
        assert pass1 != pass2, "Repeated calls for same node must produce different passwords"

    @pytest.mark.unit
    def test_generate_socks5_credentials_when_called_then_username_is_deterministic(
        self, credential_service: CredentialService
    ) -> None:
        """Happy: username is derived deterministically — same node_id yields same username."""
        username1, _ = credential_service.generate_socks5_credentials("node-01")
        username2, _ = credential_service.generate_socks5_credentials("node-01")
        assert username1 == username2, "Username must be deterministic for the same node_id"

    @pytest.mark.unit
    @pytest.mark.negative
    def test_generate_socks5_credentials_when_node_id_empty_then_raises_value_error(
        self, credential_service: CredentialService
    ) -> None:
        """Negative: empty node_id is rejected before any computation."""
        with pytest.raises(ValueError, match="node_id"):
            credential_service.generate_socks5_credentials("")

    @pytest.mark.unit
    @pytest.mark.negative
    def test_generate_socks5_credentials_when_node_id_whitespace_then_raises_value_error(
        self, credential_service: CredentialService
    ) -> None:
        """Negative: whitespace-only node_id is rejected."""
        with pytest.raises(ValueError, match="node_id"):
            credential_service.generate_socks5_credentials("   ")

    @pytest.mark.unit
    @pytest.mark.negative
    def test_generate_socks5_credentials_when_node_id_has_shell_chars_then_raises_value_error(
        self, credential_service: CredentialService
    ) -> None:
        """Negative: node_id containing shell-unsafe characters is rejected."""
        with pytest.raises(ValueError):
            credential_service.generate_socks5_credentials("node/01")


class TestSshKeyCommentAndFilenameGeneration:
    """TASK-023-033: SSH key comment and filename generation — pure domain, no I/O."""

    @pytest.mark.unit
    def test_generate_ssh_key_comment_when_called_then_returns_expected_format(
        self, credential_service: CredentialService
    ) -> None:
        """Happy: SSH key comment follows jerry-proxy-{node_id} convention."""
        comment = credential_service.generate_ssh_key_comment("do-12345")
        assert comment == "jerry-proxy-do-12345"

    @pytest.mark.unit
    def test_generate_ssh_key_comment_when_called_then_embeds_full_node_id(
        self, credential_service: CredentialService
    ) -> None:
        """Happy: generated comment contains the full node_id substring."""
        node_id = "vultr-abcde"
        comment = credential_service.generate_ssh_key_comment(node_id)
        assert node_id in comment

    @pytest.mark.unit
    def test_generate_credential_filename_when_no_suffix_then_returns_base_name(
        self, credential_service: CredentialService
    ) -> None:
        """Happy: filename without suffix is id_ed25519_{node_id}."""
        filename = credential_service.generate_credential_filename("do-12345")
        assert filename == "id_ed25519_do-12345"

    @pytest.mark.unit
    def test_generate_credential_filename_when_pub_suffix_then_returns_pub_name(
        self, credential_service: CredentialService
    ) -> None:
        """Happy: filename with .pub suffix is id_ed25519_{node_id}.pub."""
        filename = credential_service.generate_credential_filename("do-12345", ".pub")
        assert filename == "id_ed25519_do-12345.pub"

    @pytest.mark.unit
    @pytest.mark.negative
    def test_generate_ssh_key_comment_when_node_id_empty_then_raises_value_error(
        self, credential_service: CredentialService
    ) -> None:
        """Negative: empty node_id is rejected."""
        with pytest.raises(ValueError, match="node_id"):
            credential_service.generate_ssh_key_comment("")

    @pytest.mark.unit
    @pytest.mark.negative
    def test_generate_credential_filename_when_node_id_empty_then_raises_value_error(
        self, credential_service: CredentialService
    ) -> None:
        """Negative: empty node_id is rejected."""
        with pytest.raises(ValueError, match="node_id"):
            credential_service.generate_credential_filename("")


class TestCredentialServiceSecurityInvariants:
    """Security invariants for CredentialService: no credential values in logs."""

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

    @pytest.mark.unit
    @pytest.mark.security
    def test_generate_socks5_credentials_when_called_then_password_not_in_repr(
        self, credential_service: CredentialService
    ) -> None:
        """Security: CredentialService repr must not include generated password values."""
        _, password = credential_service.generate_socks5_credentials("node-01")
        assert password not in repr(credential_service), (
            "Password must not appear in CredentialService repr"
        )


# =============================================================================
# TASK-023-034: CredentialInjectionHandler — application layer
# =============================================================================


class TestCredentialInjection:
    """TASK-023-034: Credential injection happy-path and negative tests."""

    @pytest.mark.unit
    def test_inject_ssh_key_when_valid_descriptor_then_returns_success_result(
        self,
        injection_handler: CredentialInjectionHandler,
        generated_dir: Path,
    ) -> None:
        """Happy: injection returns InjectionResult with success=True and node_id set."""
        descriptor = _make_descriptor("node-01", generated_dir)
        result = injection_handler.inject_ssh_key(descriptor, node_id="node-01")
        assert result.success is True
        assert result.node_id == "node-01"

    @pytest.mark.unit
    def test_inject_ssh_key_when_called_then_secret_file_exists_at_expected_path(
        self,
        injection_handler: CredentialInjectionHandler,
        generated_dir: Path,
    ) -> None:
        """Happy: SSH key secret file written at {generated_dir}/ssh_key_{node_id}."""
        descriptor = _make_descriptor("node-01", generated_dir)
        injection_handler.inject_ssh_key(descriptor, node_id="node-01")
        secret_path = generated_dir / "ssh_key_node-01"
        assert secret_path.exists(), f"Secret file not found at {secret_path}"

    @pytest.mark.unit
    def test_inject_ssh_key_when_called_then_secret_file_has_0600_permissions(
        self,
        injection_handler: CredentialInjectionHandler,
        generated_dir: Path,
    ) -> None:
        """Happy: injected SSH key secret file has owner-only read/write permissions."""
        descriptor = _make_descriptor("node-01", generated_dir)
        injection_handler.inject_ssh_key(descriptor, node_id="node-01")
        secret_path = generated_dir / "ssh_key_node-01"
        file_mode = stat.filemode(os.stat(secret_path).st_mode)
        assert file_mode == "-rw-------", (
            f"Injected SSH key should have 0600 permissions, got {file_mode}"
        )

    @pytest.mark.unit
    def test_inject_ssh_key_when_called_then_result_secret_path_matches_written_file(
        self,
        injection_handler: CredentialInjectionHandler,
        generated_dir: Path,
    ) -> None:
        """Happy: InjectionResult.secret_path points to the actually-written file."""
        descriptor = _make_descriptor("node-01", generated_dir)
        result = injection_handler.inject_ssh_key(descriptor, node_id="node-01")
        assert result.secret_path
        assert Path(result.secret_path).exists()

    @pytest.mark.unit
    def test_inject_socks5_credentials_when_valid_then_returns_success_result(
        self,
        credential_service: CredentialService,
        injection_handler: CredentialInjectionHandler,
    ) -> None:
        """Happy: SOCKS5 injection returns InjectionResult with success=True."""
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
    def test_inject_socks5_credentials_when_called_then_password_not_exposed_in_env(
        self,
        credential_service: CredentialService,
        injection_handler: CredentialInjectionHandler,
    ) -> None:
        """Security: SOCKS5 password must not be placed in any environment variable."""
        username, password = credential_service.generate_socks5_credentials("node-01")
        injection_handler.inject_socks5_credentials(
            username=username, password=password, node_id="node-01"
        )
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
        """Negative: source key file not found yields success=False result."""
        missing_path = str(generated_dir / "does_not_exist")
        fake_descriptor = CredentialDescriptor(
            node_id="node-99",
            private_key_path=missing_path,
            public_key_path=missing_path + ".pub",
        )
        result = injection_handler.inject_ssh_key(fake_descriptor, node_id="node-99")
        assert result.success is False
        assert result.node_id == "node-99"

    @pytest.mark.unit
    @pytest.mark.negative
    def test_inject_ssh_key_when_source_missing_then_error_message_is_non_empty(
        self,
        injection_handler: CredentialInjectionHandler,
        generated_dir: Path,
    ) -> None:
        """Negative: failure result carries a non-empty error message."""
        missing_path = str(generated_dir / "does_not_exist")
        fake_descriptor = CredentialDescriptor(
            node_id="node-99",
            private_key_path=missing_path,
            public_key_path=missing_path + ".pub",
        )
        result = injection_handler.inject_ssh_key(fake_descriptor, node_id="node-99")
        assert result.error, "Failure result must have a non-empty error message"

    @pytest.mark.unit
    @pytest.mark.negative
    def test_inject_socks5_credentials_when_node_id_empty_then_raises_value_error(
        self,
        injection_handler: CredentialInjectionHandler,
    ) -> None:
        """Negative: empty node_id is rejected before any file I/O."""
        with pytest.raises(ValueError, match="node_id"):
            injection_handler.inject_socks5_credentials(
                username="jerry-abcd1234", password="somepassword", node_id=""
            )

    @pytest.mark.unit
    @pytest.mark.negative
    def test_inject_ssh_key_when_write_raises_oserror_then_returns_failure(
        self,
        injection_handler: CredentialInjectionHandler,
        generated_dir: Path,
    ) -> None:
        """Negative: OSError during secret file write produces success=False result."""
        descriptor = _make_descriptor("node-01", generated_dir)
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


# =============================================================================
# TASK-023-035: CredentialDestructionHandler — application layer
# =============================================================================


class TestCredentialDestruction:
    """TASK-023-035: Credential destruction tests."""

    @pytest.mark.unit
    def test_destroy_when_files_exist_then_returns_report_listing_each_file(
        self,
        destruction_handler: CredentialDestructionHandler,
        generated_dir: Path,
    ) -> None:
        """Happy: destroy_all report lists every credential file that was processed."""
        (generated_dir / "socks5_creds_node-01").write_text("jerry-abcd1234:somepass")
        (generated_dir / "ssh_key_node-01").write_bytes(b"SYNTHETIC-KEY-DATA")

        report = destruction_handler.destroy_all()

        assert len(report.destroyed_files) == 2

    @pytest.mark.unit
    def test_destroy_when_files_exist_then_files_are_removed(
        self,
        destruction_handler: CredentialDestructionHandler,
        generated_dir: Path,
    ) -> None:
        """Happy: after destruction all credential files in generated_dir are unlinked."""
        creds_path = generated_dir / "socks5_creds_node-01"
        ssh_path = generated_dir / "ssh_key_node-01"
        creds_path.write_text("jerry-abcd1234:somepass")
        ssh_path.write_bytes(b"SYNTHETIC-KEY-DATA")
        assert creds_path.exists() and ssh_path.exists()

        destruction_handler.destroy_all()

        assert not creds_path.exists(), "SOCKS5 creds file must be deleted after destruction"
        assert not ssh_path.exists(), "SSH key file must be deleted after destruction"

    @pytest.mark.unit
    def test_destroy_when_called_then_uses_urandom_for_overwrite(
        self,
        destruction_handler: CredentialDestructionHandler,
        generated_dir: Path,
    ) -> None:
        """Happy: destroy_all calls os.urandom before unlinking (one-pass secure wipe)."""
        cred_file = generated_dir / "socks5_creds_node-01"
        cred_file.write_text("jerry-abcd1234:somepass")

        with patch("os.urandom", wraps=os.urandom) as mock_urandom:
            destruction_handler.destroy_all()
            assert mock_urandom.called, "os.urandom must be used to overwrite credential files"

    @pytest.mark.unit
    def test_destroy_when_called_then_report_entry_has_overwrite_confirmed_true(
        self,
        destruction_handler: CredentialDestructionHandler,
        generated_dir: Path,
    ) -> None:
        """Happy: DestructionEntry.overwrite_confirmed is True when overwrite succeeded."""
        cred_file = generated_dir / "socks5_creds_node-01"
        cred_file.write_text("jerry-abcd1234:somepass")

        report = destruction_handler.destroy_all()

        assert len(report.destroyed_files) == 1
        entry = report.destroyed_files[0]
        assert entry.overwrite_confirmed is True

    @pytest.mark.unit
    def test_destroy_when_called_then_report_entry_contains_file_path(
        self,
        destruction_handler: CredentialDestructionHandler,
        generated_dir: Path,
    ) -> None:
        """Happy: DestructionEntry.file_path references the destroyed file."""
        cred_file = generated_dir / "socks5_creds_node-01"
        cred_file.write_text("user:pass")

        report = destruction_handler.destroy_all()

        assert len(report.destroyed_files) == 1
        assert "socks5_creds_node-01" in report.destroyed_files[0].file_path

    @pytest.mark.unit
    def test_destroy_when_directory_empty_then_returns_empty_report(
        self,
        destruction_handler: CredentialDestructionHandler,
    ) -> None:
        """Edge: destroy_all on an empty directory returns a report with no destroyed files."""
        report = destruction_handler.destroy_all()
        assert report.destroyed_files == []
        assert report.failed_files == []

    @pytest.mark.unit
    @pytest.mark.negative
    def test_destroy_when_file_cannot_be_unlinked_then_continues_processing_remaining_files(
        self,
        destruction_handler: CredentialDestructionHandler,
        generated_dir: Path,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        """Negative: PermissionError on one file does not abort sweep of remaining files."""
        good_file = generated_dir / "socks5_creds_node-01"
        bad_file = generated_dir / "ssh_key_node-02"
        good_file.write_text("user:pass")
        bad_file.write_text("SYNTHETIC-KEY")

        original_unlink = Path.unlink

        def selective_unlink(self: Path, missing_ok: bool = False) -> None:
            if self.name == "ssh_key_node-02":
                raise PermissionError("file locked by another process")
            original_unlink(self, missing_ok=missing_ok)

        with caplog.at_level(logging.WARNING):
            with patch.object(Path, "unlink", selective_unlink):
                report = destruction_handler.destroy_all()

        assert len(report.destroyed_files) == 1, (
            "The unlockable file should appear in destroyed_files"
        )
        assert len(report.failed_files) == 1, (
            "The locked file should be tracked in failed_files"
        )

    @pytest.mark.unit
    @pytest.mark.negative
    def test_destroy_when_file_locked_then_warning_is_logged(
        self,
        destruction_handler: CredentialDestructionHandler,
        generated_dir: Path,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        """Negative: a WARNING is logged when a file cannot be destroyed (F-003 tolerance)."""
        bad_file = generated_dir / "ssh_key_node-02"
        bad_file.write_text("SYNTHETIC-KEY")

        def always_fail_unlink(self: Path, missing_ok: bool = False) -> None:
            raise PermissionError("file locked")

        with caplog.at_level(logging.WARNING):
            with patch.object(Path, "unlink", always_fail_unlink):
                destruction_handler.destroy_all()

        warning_records = [r for r in caplog.records if r.levelno >= logging.WARNING]
        assert warning_records, "A WARNING must be logged when a file cannot be destroyed"

    @pytest.mark.unit
    @pytest.mark.negative
    def test_destroy_when_file_locked_then_failed_files_entry_is_tuple_of_path_and_error(
        self,
        destruction_handler: CredentialDestructionHandler,
        generated_dir: Path,
    ) -> None:
        """Negative: failed_files entries are (path_str, error_str) tuples."""
        bad_file = generated_dir / "ssh_key_node-02"
        bad_file.write_text("SYNTHETIC-KEY")

        def always_fail_unlink(self: Path, missing_ok: bool = False) -> None:
            raise PermissionError("file locked")

        with patch.object(Path, "unlink", always_fail_unlink):
            report = destruction_handler.destroy_all()

        assert len(report.failed_files) == 1
        entry = report.failed_files[0]
        assert isinstance(entry, tuple) and len(entry) == 2
        path_str, error_str = entry
        assert "ssh_key_node-02" in path_str
        assert error_str

    @pytest.mark.unit
    @pytest.mark.security
    def test_destroy_when_called_then_credential_values_not_logged(
        self,
        destruction_handler: CredentialDestructionHandler,
        generated_dir: Path,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        """Security: credential file contents must not appear in log output during destruction."""
        sentinel = "ultra_secret_password_9876"
        cred_file = generated_dir / "socks5_creds_node-01"
        cred_file.write_text(f"jerry-testnode:{sentinel}")

        with caplog.at_level(logging.DEBUG):
            destruction_handler.destroy_all()

        assert sentinel not in caplog.text, (
            "Credential values must never appear in logs during destruction"
        )


# =============================================================================
# Constructor guard tests — edge cases for both handlers
# =============================================================================


class TestConstructorGuards:
    """Edge: handlers reject a non-existent generated_dir at construction time."""

    @pytest.mark.unit
    @pytest.mark.edge_case
    def test_injection_handler_when_dir_missing_then_raises_not_a_directory_error(
        self, tmp_path: Path
    ) -> None:
        """Edge: CredentialInjectionHandler raises NotADirectoryError for missing dir."""
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
