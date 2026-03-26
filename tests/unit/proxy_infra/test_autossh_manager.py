# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""BDD unit tests for AutosshManager.

Covers TASK-023-022: autossh tunnel manager for Type A SSH-tunnel proxy nodes.

All subprocess.Popen calls are mocked — no real autossh binary required.

Test pyramid: 60% happy path / 30% negative / 10% edge cases

Scenarios:
  - start_tunnels spawns one process per SSH_TUNNEL node
  - start_tunnels skips DIRECT_SOCKS5 nodes
  - start_tunnels assigns sequential ports starting at base_port+1
  - start_tunnels returns node_id -> local_port mapping
  - start_tunnels raises RuntimeError when SSH key file missing
  - health_check returns True for alive tunnel (poll returns None)
  - health_check returns False for dead tunnel (poll returns exit code)
  - stop_all terminates all managed processes
  - stop_all is safe to call when no tunnels running
  - stop_tunnel stops specific node and returns True
  - stop_tunnel returns False for unknown node_id
  - tunnel_count reflects current managed tunnel count
  - local_port_for returns correct port for managed node
  - local_port_for returns None for unknown node
  - SSH command includes StrictHostKeyChecking=no (OPSEC)
  - SSH command includes UserKnownHostsFile=/dev/null (OPSEC)
  - SSH command uses -D for dynamic SOCKS5 forwarding
  - SSH command uses -M 0 to disable monitoring port
"""

from __future__ import annotations

import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.proxy_infra.domain.value_objects.node_status import NodeStatus
from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode
from src.proxy_infra.domain.value_objects.proxy_role import ProxyRole
from src.proxy_infra.domain.value_objects.proxy_type import ProxyType
from src.proxy_infra.infrastructure.tunnel.autossh_manager import AutosshManager


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture()
def ssh_key_file(tmp_path: Path) -> Path:
    """Create a temporary SSH key file."""
    key_file = tmp_path / "eng_ssh_key"
    key_file.write_text("--- FAKE ED25519 KEY ---")
    return key_file


@pytest.fixture()
def manager(ssh_key_file: Path) -> AutosshManager:
    """AutosshManager with a real key file on disk."""
    return AutosshManager(ssh_key_path=ssh_key_file, base_port=12000)


def _make_node(
    node_id: str = "node-001",
    ip: str = "203.0.113.10",
    proxy_type: ProxyType = ProxyType.SSH_TUNNEL,
) -> ProxyNode:
    """Build a minimal ProxyNode for test use."""
    return ProxyNode(
        id=node_id,
        provider="vultr",
        ip=ip,
        region="fra1",
        role=ProxyRole.RECON,
        proxy_type=proxy_type,
        status=NodeStatus.READY,
        ssh_key_id="key-001",
        created_at=datetime(2026, 3, 25, tzinfo=timezone.utc),
        engagement_id="ENG-2026-001",
        socks_port=1080,
    )


def _make_alive_process() -> MagicMock:
    """Mock Popen process that reports as running (poll returns None)."""
    proc = MagicMock()
    proc.poll.return_value = None
    proc.pid = 12345
    return proc


def _make_dead_process(returncode: int = 1) -> MagicMock:
    """Mock Popen process that reports as exited."""
    proc = MagicMock()
    proc.poll.return_value = returncode
    proc.returncode = returncode
    proc.pid = 99999
    return proc


# =============================================================================
# start_tunnels — happy path (60%)
# =============================================================================


class TestStartTunnelsHappyPath:
    """Happy path tests for AutosshManager.start_tunnels()."""

    def test_start_tunnels_spawns_one_process_per_ssh_node(
        self, manager: AutosshManager
    ) -> None:
        """GIVEN 2 SSH_TUNNEL nodes WHEN start_tunnels THEN 2 processes spawned."""
        nodes = [
            _make_node("node-001", "10.0.0.1"),
            _make_node("node-002", "10.0.0.2"),
        ]
        with patch("subprocess.Popen", return_value=_make_alive_process()) as mock_popen:
            manager.start_tunnels(nodes)
        assert mock_popen.call_count == 2

    def test_start_tunnels_returns_node_to_port_mapping(
        self, manager: AutosshManager
    ) -> None:
        """GIVEN 2 nodes WHEN start_tunnels THEN returns dict with both node_ids."""
        nodes = [
            _make_node("node-001", "10.0.0.1"),
            _make_node("node-002", "10.0.0.2"),
        ]
        with patch("subprocess.Popen", return_value=_make_alive_process()):
            port_map = manager.start_tunnels(nodes)
        assert "node-001" in port_map
        assert "node-002" in port_map

    def test_start_tunnels_assigns_sequential_ports(
        self, manager: AutosshManager
    ) -> None:
        """GIVEN base_port=12000 and 3 nodes WHEN start_tunnels THEN ports 12001 12002 12003."""
        nodes = [
            _make_node("node-001"),
            _make_node("node-002"),
            _make_node("node-003"),
        ]
        with patch("subprocess.Popen", return_value=_make_alive_process()):
            port_map = manager.start_tunnels(nodes)
        assert port_map["node-001"] == 12001
        assert port_map["node-002"] == 12002
        assert port_map["node-003"] == 12003

    def test_start_tunnels_updates_tunnel_count(
        self, manager: AutosshManager
    ) -> None:
        """GIVEN 2 nodes WHEN start_tunnels THEN tunnel_count == 2."""
        nodes = [_make_node("n1"), _make_node("n2")]
        with patch("subprocess.Popen", return_value=_make_alive_process()):
            manager.start_tunnels(nodes)
        assert manager.tunnel_count() == 2

    def test_start_tunnels_with_single_node(
        self, manager: AutosshManager
    ) -> None:
        """GIVEN 1 node WHEN start_tunnels THEN 1 process spawned on port 12001."""
        nodes = [_make_node("node-001")]
        with patch("subprocess.Popen", return_value=_make_alive_process()):
            port_map = manager.start_tunnels(nodes)
        assert port_map["node-001"] == 12001

    def test_start_tunnels_skips_direct_socks5_nodes(
        self, manager: AutosshManager
    ) -> None:
        """GIVEN mix of SSH_TUNNEL and DIRECT_SOCKS5 WHEN start_tunnels THEN only SSH_TUNNEL started."""
        nodes = [
            _make_node("node-ssh", proxy_type=ProxyType.SSH_TUNNEL),
            _make_node("node-direct", proxy_type=ProxyType.DIRECT_SOCKS5),
        ]
        with patch("subprocess.Popen", return_value=_make_alive_process()) as mock_popen:
            port_map = manager.start_tunnels(nodes)
        assert mock_popen.call_count == 1
        assert "node-ssh" in port_map
        assert "node-direct" not in port_map

    def test_start_tunnels_with_empty_node_list(
        self, manager: AutosshManager
    ) -> None:
        """GIVEN empty node list WHEN start_tunnels THEN returns empty dict."""
        with patch("subprocess.Popen", return_value=_make_alive_process()):
            port_map = manager.start_tunnels([])
        assert port_map == {}
        assert manager.tunnel_count() == 0


# =============================================================================
# start_tunnels — failures
# =============================================================================


class TestStartTunnelsFailures:
    """Failure path tests for AutosshManager.start_tunnels()."""

    def test_start_tunnels_raises_when_key_file_missing(self, tmp_path: Path) -> None:
        """GIVEN SSH key file does not exist WHEN start_tunnels THEN raises RuntimeError."""
        mgr = AutosshManager(ssh_key_path=tmp_path / "missing_key")
        with pytest.raises(RuntimeError, match="SSH key file not found"):
            mgr.start_tunnels([_make_node()])

    def test_start_tunnels_all_direct_socks5_returns_empty_map(
        self, manager: AutosshManager
    ) -> None:
        """GIVEN all nodes are DIRECT_SOCKS5 WHEN start_tunnels THEN empty map returned."""
        nodes = [_make_node("d1", proxy_type=ProxyType.DIRECT_SOCKS5)]
        with patch("subprocess.Popen", return_value=_make_alive_process()):
            port_map = manager.start_tunnels(nodes)
        assert port_map == {}


# =============================================================================
# health_check
# =============================================================================


class TestHealthCheck:
    """Tests for AutosshManager.health_check()."""

    def test_health_check_returns_true_for_alive_process(
        self, manager: AutosshManager
    ) -> None:
        """GIVEN process polling None WHEN health_check THEN node reports True."""
        nodes = [_make_node("node-001")]
        with patch("subprocess.Popen", return_value=_make_alive_process()):
            manager.start_tunnels(nodes)
        status = manager.health_check()
        assert status["node-001"] is True

    def test_health_check_returns_false_for_dead_process(
        self, manager: AutosshManager
    ) -> None:
        """GIVEN process polling exit code WHEN health_check THEN node reports False."""
        nodes = [_make_node("node-001")]
        with patch("subprocess.Popen", return_value=_make_dead_process(returncode=1)):
            manager.start_tunnels(nodes)
        status = manager.health_check()
        assert status["node-001"] is False

    def test_health_check_empty_when_no_tunnels(
        self, manager: AutosshManager
    ) -> None:
        """GIVEN no tunnels started WHEN health_check THEN returns empty dict."""
        status = manager.health_check()
        assert status == {}

    def test_health_check_mixed_alive_and_dead(
        self, manager: AutosshManager
    ) -> None:
        """GIVEN one alive and one dead WHEN health_check THEN both reported correctly."""
        alive_proc = _make_alive_process()
        dead_proc = _make_dead_process()

        nodes = [_make_node("n-alive"), _make_node("n-dead")]
        side_effects = [alive_proc, dead_proc]
        with patch("subprocess.Popen", side_effect=side_effects):
            manager.start_tunnels(nodes)
        status = manager.health_check()
        assert status["n-alive"] is True
        assert status["n-dead"] is False


# =============================================================================
# stop_all / stop_tunnel
# =============================================================================


class TestStopTunnels:
    """Tests for stop_all() and stop_tunnel()."""

    def test_stop_all_terminates_all_processes(
        self, manager: AutosshManager
    ) -> None:
        """GIVEN 2 running tunnels WHEN stop_all THEN both processes terminated."""
        proc1 = _make_alive_process()
        proc2 = _make_alive_process()
        nodes = [_make_node("n1"), _make_node("n2")]
        with patch("subprocess.Popen", side_effect=[proc1, proc2]):
            manager.start_tunnels(nodes)
        manager.stop_all()
        proc1.terminate.assert_called_once()
        proc2.terminate.assert_called_once()

    def test_stop_all_clears_tunnel_registry(
        self, manager: AutosshManager
    ) -> None:
        """GIVEN 2 tunnels WHEN stop_all THEN tunnel_count drops to 0."""
        nodes = [_make_node("n1"), _make_node("n2")]
        with patch("subprocess.Popen", return_value=_make_alive_process()):
            manager.start_tunnels(nodes)
        manager.stop_all()
        assert manager.tunnel_count() == 0

    def test_stop_all_is_safe_with_no_tunnels(
        self, manager: AutosshManager
    ) -> None:
        """GIVEN no tunnels WHEN stop_all THEN no error raised."""
        manager.stop_all()  # Should not raise

    def test_stop_tunnel_returns_true_for_known_node(
        self, manager: AutosshManager
    ) -> None:
        """GIVEN tunnel for node-001 WHEN stop_tunnel('node-001') THEN returns True."""
        nodes = [_make_node("node-001")]
        with patch("subprocess.Popen", return_value=_make_alive_process()):
            manager.start_tunnels(nodes)
        result = manager.stop_tunnel("node-001")
        assert result is True

    def test_stop_tunnel_removes_node_from_registry(
        self, manager: AutosshManager
    ) -> None:
        """GIVEN tunnel for node-001 WHEN stop_tunnel THEN tunnel_count decrements."""
        nodes = [_make_node("node-001")]
        with patch("subprocess.Popen", return_value=_make_alive_process()):
            manager.start_tunnels(nodes)
        manager.stop_tunnel("node-001")
        assert manager.tunnel_count() == 0

    def test_stop_tunnel_returns_false_for_unknown_node(
        self, manager: AutosshManager
    ) -> None:
        """GIVEN no tunnel for 'ghost' WHEN stop_tunnel('ghost') THEN returns False."""
        result = manager.stop_tunnel("ghost")
        assert result is False


# =============================================================================
# local_port_for accessor
# =============================================================================


class TestLocalPortFor:
    """Tests for AutosshManager.local_port_for()."""

    def test_local_port_for_returns_correct_port(
        self, manager: AutosshManager
    ) -> None:
        """GIVEN tunnel started on port 12001 WHEN local_port_for THEN returns 12001."""
        nodes = [_make_node("node-001")]
        with patch("subprocess.Popen", return_value=_make_alive_process()):
            manager.start_tunnels(nodes)
        assert manager.local_port_for("node-001") == 12001

    def test_local_port_for_returns_none_for_unknown_node(
        self, manager: AutosshManager
    ) -> None:
        """GIVEN no tunnel for 'nobody' WHEN local_port_for THEN returns None."""
        assert manager.local_port_for("nobody") is None


# =============================================================================
# SSH command content (OPSEC checks) — edge / safety
# =============================================================================


class TestSshCommandSecurity:
    """Tests verifying OPSEC-critical SSH flags are present in the command."""

    def test_ssh_command_contains_strict_host_checking_no(
        self, manager: AutosshManager
    ) -> None:
        """GIVEN any node WHEN build SSH command THEN StrictHostKeyChecking=no present."""
        cmd = manager._build_ssh_command("10.0.0.1", 12001)
        cmd_str = " ".join(cmd)
        assert "StrictHostKeyChecking=no" in cmd_str

    def test_ssh_command_contains_userknownhostsfile_devnull(
        self, manager: AutosshManager
    ) -> None:
        """GIVEN any node WHEN build SSH command THEN UserKnownHostsFile=/dev/null present."""
        cmd = manager._build_ssh_command("10.0.0.1", 12001)
        cmd_str = " ".join(cmd)
        assert "UserKnownHostsFile=/dev/null" in cmd_str

    def test_ssh_command_uses_dynamic_forwarding_flag(
        self, manager: AutosshManager
    ) -> None:
        """GIVEN port 12001 WHEN build SSH command THEN -D 127.0.0.1:12001 present."""
        cmd = manager._build_ssh_command("10.0.0.1", 12001)
        assert "-D" in cmd
        assert "127.0.0.1:12001" in cmd

    def test_ssh_command_uses_m_zero_for_monitoring_disable(
        self, manager: AutosshManager
    ) -> None:
        """GIVEN any node WHEN build SSH command THEN -M 0 present (monitoring disabled)."""
        cmd = manager._build_ssh_command("10.0.0.1", 12001)
        assert "-M" in cmd
        m_idx = cmd.index("-M")
        assert cmd[m_idx + 1] == "0"

    def test_ssh_command_includes_exit_on_forward_failure(
        self, manager: AutosshManager
    ) -> None:
        """GIVEN any node WHEN build SSH command THEN ExitOnForwardFailure=yes present."""
        cmd = manager._build_ssh_command("10.0.0.1", 12001)
        cmd_str = " ".join(cmd)
        assert "ExitOnForwardFailure=yes" in cmd_str

    def test_ssh_command_includes_server_alive_interval(
        self, manager: AutosshManager
    ) -> None:
        """GIVEN any node WHEN build SSH command THEN ServerAliveInterval=15 present."""
        cmd = manager._build_ssh_command("10.0.0.1", 12001)
        cmd_str = " ".join(cmd)
        assert "ServerAliveInterval=15" in cmd_str

    def test_autossh_env_contains_required_vars(
        self, manager: AutosshManager
    ) -> None:
        """GIVEN node-001 WHEN build env THEN AUTOSSH_* vars present."""
        env = manager._build_autossh_env("node-001")
        assert env["AUTOSSH_GATETIME"] == "0"
        assert env["AUTOSSH_POLL"] == "30"
        assert env["AUTOSSH_MAXSTART"] == "0"
        assert "node-001" in env["AUTOSSH_LOGFILE"]
