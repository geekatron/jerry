# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""BDD test suite for SSH credential injection pipeline (7-step sequence).

STORY-023-008: Automated SSH Post-Boot Credential Injection
Tasks covered:
  - TASK-023-053: BDD tests for SSH injection pipeline (RED)
  - TASK-023-054: SshReadinessPort concrete adapter (TCP socket polling)
  - TASK-023-055: SSH credential injection handler (7-step on-node sequence)
  - TASK-023-056: SOCKS5 credential return flow

RED PHASE (H-20): All tests MUST FAIL before implementation exists.

The 7-step injection sequence (from CloudInitTemplateGenerator):
  1. Poll SSH availability on port 22 (timeout 180s)
  2. Connect to proxy node via SSH using the engagement Ed25519 key
  3. Generate SOCKS5 credentials on-node (openssl rand)
  4. Write /etc/microsocks.env + chmod 0600
  5. Start microsocks service (systemctl start microsocks)
  6. Verify SOCKS5 connectivity (curl --socks5-hostname)
  7. Update pool manifest to READY status

Test pyramid: 60% happy path / 30% negative / 10% edge cases
Naming convention: test_{scenario}_when_{condition}_then_{expected}
"""

from __future__ import annotations

import socket
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch, call

import pytest

from src.proxy_infra.domain.value_objects.node_status import NodeStatus
from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode
from src.proxy_infra.domain.value_objects.proxy_role import ProxyRole
from src.proxy_infra.domain.value_objects.proxy_type import ProxyType


# =============================================================================
# Shared fixtures
# =============================================================================


def _make_node(
    node_id: str = "do-12345",
    ip: str = "159.203.44.10",
    status: NodeStatus = NodeStatus.CONFIGURING,
) -> ProxyNode:
    """Create a test ProxyNode."""
    return ProxyNode(
        id=node_id,
        provider="digitalocean",
        ip=ip,
        region="nyc1",
        role=ProxyRole.ACTIVE,
        proxy_type=ProxyType.DIRECT_SOCKS5,
        status=status,
        ssh_key_id="key-123",
        created_at=datetime.now(timezone.utc),
        engagement_id="ENG-001",
        socks_port=1080,
    )


# =============================================================================
# TcpSshReadinessAdapter tests
# =============================================================================


class TestTcpSshReadinessAdapter:
    """Tests for the concrete SshReadinessPort TCP socket adapter."""

    def test_wait_when_ssh_available_immediately_then_returns_true(self) -> None:
        """SSH banner received on first poll attempt."""
        from src.proxy_infra.infrastructure.ssh.tcp_ssh_readiness_adapter import (
            TcpSshReadinessAdapter,
        )

        adapter = TcpSshReadinessAdapter()
        with patch("socket.create_connection") as mock_conn:
            mock_sock = MagicMock()
            mock_sock.recv.return_value = b"SSH-2.0-OpenSSH_9.6"
            mock_conn.return_value.__enter__ = MagicMock(return_value=mock_sock)
            mock_conn.return_value.__exit__ = MagicMock(return_value=False)

            result = adapter.wait_for_ssh("159.203.44.10", timeout_seconds=10)
            assert result is True

    def test_wait_when_ssh_unavailable_then_returns_false_after_timeout(self) -> None:
        """No SSH banner within timeout window."""
        from src.proxy_infra.infrastructure.ssh.tcp_ssh_readiness_adapter import (
            TcpSshReadinessAdapter,
        )

        adapter = TcpSshReadinessAdapter(poll_interval=0.01)
        with patch("socket.create_connection", side_effect=ConnectionRefusedError):
            result = adapter.wait_for_ssh("159.203.44.10", timeout_seconds=0.05)
            assert result is False

    def test_wait_when_connection_refused_then_retries(self) -> None:
        """Connection refused on first attempts, then succeeds."""
        from src.proxy_infra.infrastructure.ssh.tcp_ssh_readiness_adapter import (
            TcpSshReadinessAdapter,
        )

        adapter = TcpSshReadinessAdapter(poll_interval=0.01)
        mock_sock = MagicMock()
        mock_sock.recv.return_value = b"SSH-2.0-OpenSSH_9.6"

        effects = [ConnectionRefusedError, ConnectionRefusedError, MagicMock()]
        effects[2].__enter__ = MagicMock(return_value=mock_sock)
        effects[2].__exit__ = MagicMock(return_value=False)

        with patch("socket.create_connection", side_effect=effects):
            result = adapter.wait_for_ssh("159.203.44.10", timeout_seconds=5)
            assert result is True

    def test_wait_does_not_raise_on_timeout(self) -> None:
        """Timeout should return False, not raise an exception."""
        from src.proxy_infra.infrastructure.ssh.tcp_ssh_readiness_adapter import (
            TcpSshReadinessAdapter,
        )

        adapter = TcpSshReadinessAdapter(poll_interval=0.01)
        with patch("socket.create_connection", side_effect=socket.timeout):
            result = adapter.wait_for_ssh("159.203.44.10", timeout_seconds=0.05)
            assert result is False

    def test_adapter_polls_port_22(self) -> None:
        """Adapter must connect to port 22."""
        from src.proxy_infra.infrastructure.ssh.tcp_ssh_readiness_adapter import (
            TcpSshReadinessAdapter,
        )

        adapter = TcpSshReadinessAdapter(poll_interval=0.01)
        with patch("socket.create_connection", side_effect=ConnectionRefusedError) as mock_conn:
            adapter.wait_for_ssh("10.0.0.1", timeout_seconds=0.02)
            assert mock_conn.call_args[0][0] == ("10.0.0.1", 22)


# =============================================================================
# SshCredentialInjectionHandler tests
# =============================================================================


class TestSshCredentialInjectionHandler:
    """Tests for the 7-step SSH credential injection handler."""

    def test_inject_when_all_steps_succeed_then_returns_success(self) -> None:
        """Happy path: all 7 steps complete for a healthy node."""
        from src.proxy_infra.application.handlers.ssh_credential_injection_handler import (
            SshCredentialInjectionHandler,
        )

        ssh_readiness = MagicMock()
        ssh_readiness.wait_for_ssh.return_value = True

        ssh_executor = MagicMock()
        # Step 3: openssl rand returns username:password
        ssh_executor.execute.return_value = MagicMock(
            stdout="jerry-abc12345:randompassword123", returncode=0
        )

        socks_verifier = MagicMock()
        socks_verifier.verify.return_value = True

        manifest_writer = MagicMock()

        handler = SshCredentialInjectionHandler(
            ssh_readiness=ssh_readiness,
            ssh_executor=ssh_executor,
            socks_verifier=socks_verifier,
            manifest_writer=manifest_writer,
        )

        node = _make_node()
        result = handler.inject(
            node=node,
            private_key_path=Path("/tmp/id_ed25519_ENG-001"),
        )

        assert result.success is True
        assert result.node_id == "do-12345"

    def test_inject_when_ssh_timeout_then_returns_failure_at_ssh_wait(self) -> None:
        """SSH readiness timeout should halt injection at step 1."""
        from src.proxy_infra.application.handlers.ssh_credential_injection_handler import (
            SshCredentialInjectionHandler,
        )

        ssh_readiness = MagicMock()
        ssh_readiness.wait_for_ssh.return_value = False

        handler = SshCredentialInjectionHandler(
            ssh_readiness=ssh_readiness,
            ssh_executor=MagicMock(),
            socks_verifier=MagicMock(),
            manifest_writer=MagicMock(),
        )

        node = _make_node()
        result = handler.inject(
            node=node,
            private_key_path=Path("/tmp/id_ed25519_ENG-001"),
        )

        assert result.success is False
        assert result.stage_failed == "ssh_wait"

    def test_inject_when_cred_generation_fails_then_returns_failure(self) -> None:
        """On-node credential generation failure should halt at step 3."""
        from src.proxy_infra.application.handlers.ssh_credential_injection_handler import (
            SshCredentialInjectionHandler,
        )

        ssh_readiness = MagicMock()
        ssh_readiness.wait_for_ssh.return_value = True

        ssh_executor = MagicMock()
        ssh_executor.execute.return_value = MagicMock(stdout="", returncode=1)

        handler = SshCredentialInjectionHandler(
            ssh_readiness=ssh_readiness,
            ssh_executor=ssh_executor,
            socks_verifier=MagicMock(),
            manifest_writer=MagicMock(),
        )

        node = _make_node()
        result = handler.inject(
            node=node,
            private_key_path=Path("/tmp/id_ed25519_ENG-001"),
        )

        assert result.success is False
        assert result.stage_failed == "credential_generation"

    def test_inject_when_socks_verify_fails_then_returns_failure(self) -> None:
        """SOCKS5 connectivity verification failure should halt at step 6."""
        from src.proxy_infra.application.handlers.ssh_credential_injection_handler import (
            SshCredentialInjectionHandler,
        )

        ssh_readiness = MagicMock()
        ssh_readiness.wait_for_ssh.return_value = True

        ssh_executor = MagicMock()
        ssh_executor.execute.return_value = MagicMock(
            stdout="jerry-abc12345:randompassword123", returncode=0
        )

        socks_verifier = MagicMock()
        socks_verifier.verify.return_value = False

        handler = SshCredentialInjectionHandler(
            ssh_readiness=ssh_readiness,
            ssh_executor=ssh_executor,
            socks_verifier=socks_verifier,
            manifest_writer=MagicMock(),
        )

        node = _make_node()
        result = handler.inject(
            node=node,
            private_key_path=Path("/tmp/id_ed25519_ENG-001"),
        )

        assert result.success is False
        assert result.stage_failed == "socks_verify"

    def test_inject_updates_manifest_to_ready_on_success(self) -> None:
        """Pool manifest should be updated to READY only on successful injection."""
        from src.proxy_infra.application.handlers.ssh_credential_injection_handler import (
            SshCredentialInjectionHandler,
        )

        ssh_readiness = MagicMock()
        ssh_readiness.wait_for_ssh.return_value = True

        ssh_executor = MagicMock()
        ssh_executor.execute.return_value = MagicMock(
            stdout="jerry-abc12345:randompassword123", returncode=0
        )

        socks_verifier = MagicMock()
        socks_verifier.verify.return_value = True

        manifest_writer = MagicMock()

        handler = SshCredentialInjectionHandler(
            ssh_readiness=ssh_readiness,
            ssh_executor=ssh_executor,
            socks_verifier=socks_verifier,
            manifest_writer=manifest_writer,
        )

        node = _make_node()
        handler.inject(node=node, private_key_path=Path("/tmp/key"))

        manifest_writer.write.assert_called_once()

    def test_inject_does_not_update_manifest_on_failure(self) -> None:
        """Pool manifest should NOT be written when injection fails."""
        from src.proxy_infra.application.handlers.ssh_credential_injection_handler import (
            SshCredentialInjectionHandler,
        )

        ssh_readiness = MagicMock()
        ssh_readiness.wait_for_ssh.return_value = False

        manifest_writer = MagicMock()

        handler = SshCredentialInjectionHandler(
            ssh_readiness=ssh_readiness,
            ssh_executor=MagicMock(),
            socks_verifier=MagicMock(),
            manifest_writer=manifest_writer,
        )

        node = _make_node()
        handler.inject(node=node, private_key_path=Path("/tmp/key"))

        manifest_writer.write.assert_not_called()

    def test_inject_result_has_stage_failed_field(self) -> None:
        """InjectionResult from the handler must include stage_failed for diagnostics."""
        from src.proxy_infra.application.handlers.ssh_credential_injection_handler import (
            SshCredentialInjectionHandler,
        )

        ssh_readiness = MagicMock()
        ssh_readiness.wait_for_ssh.return_value = True

        ssh_executor = MagicMock()
        ssh_executor.execute.return_value = MagicMock(
            stdout="jerry-abc12345:randompassword123", returncode=0
        )

        socks_verifier = MagicMock()
        socks_verifier.verify.return_value = True

        handler = SshCredentialInjectionHandler(
            ssh_readiness=ssh_readiness,
            ssh_executor=ssh_executor,
            socks_verifier=socks_verifier,
            manifest_writer=MagicMock(),
        )

        node = _make_node()
        result = handler.inject(node=node, private_key_path=Path("/tmp/key"))

        assert hasattr(result, "stage_failed")
        assert result.stage_failed is None or result.stage_failed == ""


# =============================================================================
# SOCKS5 credential return flow tests
# =============================================================================


class TestSocks5CredentialReturn:
    """Tests for credential return from injected nodes to operator."""

    def test_return_when_injection_success_then_writes_cred_file(
        self, tmp_path: Path,
    ) -> None:
        """Successful injection should write socks5_creds_{node_id} file."""
        from src.proxy_infra.application.handlers.socks5_credential_return_handler import (
            Socks5CredentialReturnHandler,
        )

        handler = Socks5CredentialReturnHandler(credential_dir=tmp_path)
        result = handler.write_credentials(
            node_id="do-12345",
            username="jerry-abc12345",
            password="randompassword123",
        )

        assert result.success is True
        cred_file = tmp_path / "socks5_creds_do-12345"
        assert cred_file.exists()

    def test_return_when_success_then_file_has_0600_permissions(
        self, tmp_path: Path,
    ) -> None:
        """Credential files must have 0600 permissions."""
        import os
        import stat

        from src.proxy_infra.application.handlers.socks5_credential_return_handler import (
            Socks5CredentialReturnHandler,
        )

        handler = Socks5CredentialReturnHandler(credential_dir=tmp_path)
        handler.write_credentials(
            node_id="do-12345",
            username="jerry-abc12345",
            password="randompassword123",
        )

        cred_file = tmp_path / "socks5_creds_do-12345"
        mode = stat.S_IMODE(os.stat(cred_file).st_mode)
        assert mode == 0o600

    def test_return_when_success_then_file_contains_username_password(
        self, tmp_path: Path,
    ) -> None:
        """Credential file content should be username:password format."""
        from src.proxy_infra.application.handlers.socks5_credential_return_handler import (
            Socks5CredentialReturnHandler,
        )

        handler = Socks5CredentialReturnHandler(credential_dir=tmp_path)
        handler.write_credentials(
            node_id="do-12345",
            username="jerry-abc12345",
            password="randompassword123",
        )

        cred_file = tmp_path / "socks5_creds_do-12345"
        content = cred_file.read_text(encoding="utf-8")
        assert content == "jerry-abc12345:randompassword123"

    def test_return_when_empty_credentials_then_rejects(
        self, tmp_path: Path,
    ) -> None:
        """Empty username or password should be rejected."""
        from src.proxy_infra.application.handlers.socks5_credential_return_handler import (
            Socks5CredentialReturnHandler,
        )

        handler = Socks5CredentialReturnHandler(credential_dir=tmp_path)
        result = handler.write_credentials(
            node_id="do-12345",
            username="",
            password="randompassword123",
        )

        assert result.success is False

    def test_return_multiple_nodes_writes_separate_files(
        self, tmp_path: Path,
    ) -> None:
        """Each node gets its own credential file."""
        from src.proxy_infra.application.handlers.socks5_credential_return_handler import (
            Socks5CredentialReturnHandler,
        )

        handler = Socks5CredentialReturnHandler(credential_dir=tmp_path)
        handler.write_credentials("node-1", "user1", "pass1")
        handler.write_credentials("node-2", "user2", "pass2")
        handler.write_credentials("node-3", "user3", "pass3")

        assert (tmp_path / "socks5_creds_node-1").exists()
        assert (tmp_path / "socks5_creds_node-2").exists()
        assert (tmp_path / "socks5_creds_node-3").exists()
