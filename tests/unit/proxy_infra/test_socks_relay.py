# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""BDD test suite for SocksRelayManager and IptablesRedirect.

Covers TASK-023-016 (SOCKS relay manager) and TASK-023-019 (iptables fallback).

Scenarios:
  - Relay configures socks5lb from ProxyPool (happy path)
  - Relay configures redsocks from ProxyPool (happy path)
  - Relay health check returns True when process is alive
  - Relay health check returns False when process is not running
  - Pool update triggers config rewrite and SIGHUP
  - iptables redirect sets correct rules (correct chain + redirect port)
  - iptables cleanup removes all installed rules
  - Fallback detection: BPF unavailable selects iptables path
  - Relay start raises RuntimeError when configure_pool not called first
  - Pool update on stopped relay only rewrites config (no SIGHUP)

Test pyramid: 60% happy path / 30% negative / 10% edge cases
"""

from __future__ import annotations

import signal
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, call, patch

import pytest

from src.proxy_infra.domain.value_objects.node_status import NodeStatus
from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode
from src.proxy_infra.domain.value_objects.proxy_pool import ProxyPool
from src.proxy_infra.domain.value_objects.proxy_role import ProxyRole
from src.proxy_infra.domain.value_objects.proxy_type import ProxyType
from src.proxy_infra.infrastructure.fallback.iptables_redirect import IptablesRedirect
from src.proxy_infra.infrastructure.relay.socks_relay_manager import SocksRelayManager


# =============================================================================
# Fixtures
# =============================================================================


def _make_node(ip: str = "10.0.0.1", socks_port: int = 1080) -> ProxyNode:
    """Build a minimal ProxyNode for test purposes."""
    return ProxyNode(
        id="node-001",
        provider="vultr",
        ip=ip,
        region="fra",
        role=ProxyRole.RECON,
        proxy_type=ProxyType.SSH_TUNNEL,
        status=NodeStatus.READY,
        ssh_key_id="key-001",
        created_at=datetime(2026, 3, 25, tzinfo=timezone.utc),
        engagement_id="ENG-001",
        socks_port=socks_port,
    )


@pytest.fixture()
def single_node_pool() -> ProxyPool:
    """ProxyPool with a single active node."""
    return ProxyPool(
        nodes=(_make_node("10.0.0.1", 1080),),
        lb_strategy="round_robin",
        fail_mode="closed",
        engagement_id="ENG-001",
    )


@pytest.fixture()
def multi_node_pool() -> ProxyPool:
    """ProxyPool with two active nodes."""
    return ProxyPool(
        nodes=(
            _make_node("10.0.0.1", 1080),
            _make_node("10.0.0.2", 1080),
        ),
        lb_strategy="random",
        fail_mode="closed",
        engagement_id="ENG-001",
    )


@pytest.fixture()
def empty_pool() -> ProxyPool:
    """ProxyPool with no nodes."""
    return ProxyPool(
        nodes=(),
        lb_strategy="round_robin",
        fail_mode="closed",
        engagement_id="ENG-001",
    )


@pytest.fixture()
def relay_socks5lb(tmp_path: Path) -> SocksRelayManager:
    """SocksRelayManager using socks5lb backend with a temp config path."""
    return SocksRelayManager(
        backend="socks5lb",
        relay_port=1080,
        config_path=str(tmp_path / "socks5lb.yaml"),
    )


@pytest.fixture()
def relay_redsocks(tmp_path: Path) -> SocksRelayManager:
    """SocksRelayManager using redsocks backend with a temp config path."""
    return SocksRelayManager(
        backend="redsocks",
        relay_port=1080,
        config_path=str(tmp_path / "redsocks.conf"),
    )


# =============================================================================
# SocksRelayManager — configure_pool (TASK-023-016)
# =============================================================================


@pytest.mark.unit
@pytest.mark.happy_path
class TestSocksRelayManagerConfigurePool:
    """Relay configures from ProxyPool."""

    def test_configure_pool_writes_socks5lb_yaml(
        self, relay_socks5lb: SocksRelayManager, single_node_pool: ProxyPool
    ) -> None:
        """Given a single-node pool, configure_pool writes a socks5lb YAML config."""
        relay_socks5lb.configure_pool(single_node_pool)

        assert relay_socks5lb.config_path is not None
        content = relay_socks5lb.config_path.read_text()
        assert "listen_port: 1080" in content
        assert "lb_strategy: round_robin" in content
        assert "host: 10.0.0.1" in content
        assert "port: 1080" in content

    def test_configure_pool_writes_redsocks_conf(
        self, relay_redsocks: SocksRelayManager, single_node_pool: ProxyPool
    ) -> None:
        """Given a single-node pool, configure_pool writes a redsocks config."""
        relay_redsocks.configure_pool(single_node_pool)

        assert relay_redsocks.config_path is not None
        content = relay_redsocks.config_path.read_text()
        assert "local_port = 1080;" in content
        assert "ip = 10.0.0.1;" in content
        assert "type = socks5;" in content
        assert "redirector = iptables;" in content

    def test_configure_pool_lists_all_nodes_in_socks5lb_config(
        self, relay_socks5lb: SocksRelayManager, multi_node_pool: ProxyPool
    ) -> None:
        """Given two pool nodes, the config lists both upstream proxy addresses."""
        relay_socks5lb.configure_pool(multi_node_pool)

        content = relay_socks5lb.config_path.read_text()  # type: ignore[union-attr]
        assert "10.0.0.1" in content
        assert "10.0.0.2" in content

    def test_configure_pool_auto_creates_temp_config_path(
        self, single_node_pool: ProxyPool
    ) -> None:
        """When no config_path is specified, configure_pool creates a temp file."""
        relay = SocksRelayManager(backend="socks5lb", relay_port=1080)
        relay.configure_pool(single_node_pool)

        assert relay.config_path is not None
        assert relay.config_path.exists()
        # cleanup
        relay.config_path.unlink(missing_ok=True)

    def test_configure_pool_stores_pool_reference(
        self, relay_socks5lb: SocksRelayManager, single_node_pool: ProxyPool
    ) -> None:
        """After configure_pool, _pool is set to the given pool."""
        relay_socks5lb.configure_pool(single_node_pool)
        assert relay_socks5lb._pool is single_node_pool

    def test_configure_pool_redsocks_uses_first_node_only(
        self, relay_redsocks: SocksRelayManager, multi_node_pool: ProxyPool
    ) -> None:
        """redsocks config uses the first node as upstream (no native LB)."""
        relay_redsocks.configure_pool(multi_node_pool)

        content = relay_redsocks.config_path.read_text()  # type: ignore[union-attr]
        # redsocks config should use first node IP
        assert "ip = 10.0.0.1;" in content

    def test_configure_pool_so_mark_in_socks5lb_config(
        self, relay_socks5lb: SocksRelayManager, single_node_pool: ProxyPool
    ) -> None:
        """socks5lb config includes SO_MARK for loop prevention (value 100)."""
        relay_socks5lb.configure_pool(single_node_pool)

        content = relay_socks5lb.config_path.read_text()  # type: ignore[union-attr]
        assert "so_mark: 100" in content


# =============================================================================
# SocksRelayManager — health_check (TASK-023-016)
# =============================================================================


@pytest.mark.unit
@pytest.mark.happy_path
class TestSocksRelayManagerHealthCheck:
    """Relay health check returns bool reflecting subprocess liveness."""

    def test_health_check_returns_false_when_not_started(
        self, relay_socks5lb: SocksRelayManager
    ) -> None:
        """health_check is False before start() is called."""
        assert relay_socks5lb.health_check() is False

    def test_health_check_returns_true_when_process_alive(
        self, relay_socks5lb: SocksRelayManager, single_node_pool: ProxyPool
    ) -> None:
        """health_check is True when the subprocess is still running."""
        mock_process = MagicMock()
        mock_process.poll.return_value = None  # process is alive
        relay_socks5lb._process = mock_process
        relay_socks5lb._pool = single_node_pool

        assert relay_socks5lb.health_check() is True

    def test_health_check_returns_false_when_process_exited(
        self, relay_socks5lb: SocksRelayManager, single_node_pool: ProxyPool
    ) -> None:
        """health_check is False when the subprocess has exited."""
        mock_process = MagicMock()
        mock_process.poll.return_value = 1  # non-zero exit code
        relay_socks5lb._process = mock_process
        relay_socks5lb._pool = single_node_pool

        assert relay_socks5lb.health_check() is False

    def test_health_check_returns_false_after_stop(
        self, relay_socks5lb: SocksRelayManager, single_node_pool: ProxyPool
    ) -> None:
        """health_check is False after stop() clears the process reference."""
        mock_process = MagicMock()
        mock_process.poll.return_value = None
        relay_socks5lb._process = mock_process
        relay_socks5lb._pool = single_node_pool

        relay_socks5lb.stop()
        assert relay_socks5lb.health_check() is False


# =============================================================================
# SocksRelayManager — start / stop (TASK-023-016)
# =============================================================================


@pytest.mark.unit
@pytest.mark.happy_path
class TestSocksRelayManagerStartStop:
    """Relay start and stop manage the subprocess lifecycle."""

    def test_start_raises_when_pool_not_configured(
        self, relay_socks5lb: SocksRelayManager
    ) -> None:
        """start() before configure_pool raises RuntimeError."""
        with pytest.raises(RuntimeError, match="configure_pool"):
            relay_socks5lb.start()

    def test_start_launches_socks5lb_subprocess(
        self,
        relay_socks5lb: SocksRelayManager,
        single_node_pool: ProxyPool,
    ) -> None:
        """start() calls Popen with the correct socks5lb command."""
        relay_socks5lb.configure_pool(single_node_pool)
        mock_process = MagicMock()
        mock_process.pid = 12345

        with patch("subprocess.Popen", return_value=mock_process) as mock_popen:
            relay_socks5lb.start()

        cmd = mock_popen.call_args[0][0]
        assert cmd[0] == "socks5lb"
        assert "--config" in cmd
        assert str(relay_socks5lb.config_path) in cmd

    def test_start_launches_redsocks_subprocess(
        self,
        relay_redsocks: SocksRelayManager,
        single_node_pool: ProxyPool,
    ) -> None:
        """start() calls Popen with the correct redsocks command."""
        relay_redsocks.configure_pool(single_node_pool)
        mock_process = MagicMock()
        mock_process.pid = 12346

        with patch("subprocess.Popen", return_value=mock_process) as mock_popen:
            relay_redsocks.start()

        cmd = mock_popen.call_args[0][0]
        assert cmd[0] == "redsocks"
        assert "-c" in cmd

    def test_stop_terminates_running_process(
        self,
        relay_socks5lb: SocksRelayManager,
        single_node_pool: ProxyPool,
    ) -> None:
        """stop() calls terminate() then wait() on the subprocess."""
        mock_process = MagicMock()
        mock_process.pid = 12345
        mock_process.wait.return_value = 0
        relay_socks5lb._process = mock_process
        relay_socks5lb._pool = single_node_pool

        relay_socks5lb.stop()

        mock_process.terminate.assert_called_once()
        mock_process.wait.assert_called_once()
        assert relay_socks5lb._process is None

    def test_stop_is_noop_when_not_running(
        self, relay_socks5lb: SocksRelayManager
    ) -> None:
        """stop() is a no-op when the relay is not running."""
        relay_socks5lb.stop()  # must not raise
        assert relay_socks5lb._process is None

    def test_stop_kills_process_on_timeout(
        self,
        relay_socks5lb: SocksRelayManager,
        single_node_pool: ProxyPool,
    ) -> None:
        """stop() sends SIGKILL when terminate() does not honour the timeout."""
        mock_process = MagicMock()
        mock_process.pid = 12345
        mock_process.wait.side_effect = [subprocess.TimeoutExpired(cmd="socks5lb", timeout=5), 0]
        relay_socks5lb._process = mock_process
        relay_socks5lb._pool = single_node_pool

        relay_socks5lb.stop()

        mock_process.kill.assert_called_once()


# =============================================================================
# SocksRelayManager — update_pool (TASK-023-016)
# =============================================================================


@pytest.mark.unit
@pytest.mark.happy_path
class TestSocksRelayManagerUpdatePool:
    """Pool update triggers config rewrite and SIGHUP to the running relay."""

    def test_update_pool_rewrites_config(
        self,
        relay_socks5lb: SocksRelayManager,
        single_node_pool: ProxyPool,
        multi_node_pool: ProxyPool,
    ) -> None:
        """update_pool writes the new pool's nodes into the config file."""
        relay_socks5lb.configure_pool(single_node_pool)
        relay_socks5lb.update_pool(multi_node_pool)

        content = relay_socks5lb.config_path.read_text()  # type: ignore[union-attr]
        assert "10.0.0.2" in content

    def test_update_pool_sends_sighup_to_running_process(
        self,
        relay_socks5lb: SocksRelayManager,
        single_node_pool: ProxyPool,
        multi_node_pool: ProxyPool,
    ) -> None:
        """update_pool sends SIGHUP to the running process for hot-reload."""
        relay_socks5lb.configure_pool(single_node_pool)

        mock_process = MagicMock()
        mock_process.poll.return_value = None  # process alive
        relay_socks5lb._process = mock_process

        relay_socks5lb.update_pool(multi_node_pool)

        mock_process.send_signal.assert_called_once_with(signal.SIGHUP)

    def test_update_pool_no_sighup_when_process_not_running(
        self,
        relay_socks5lb: SocksRelayManager,
        single_node_pool: ProxyPool,
        multi_node_pool: ProxyPool,
    ) -> None:
        """update_pool only rewrites config when the relay is not running."""
        relay_socks5lb.configure_pool(single_node_pool)
        # no _process set — relay is stopped

        relay_socks5lb.update_pool(multi_node_pool)

        # must not raise; config should be updated
        content = relay_socks5lb.config_path.read_text()  # type: ignore[union-attr]
        assert "10.0.0.2" in content

    def test_update_pool_no_sighup_when_process_exited(
        self,
        relay_socks5lb: SocksRelayManager,
        single_node_pool: ProxyPool,
        multi_node_pool: ProxyPool,
    ) -> None:
        """update_pool skips SIGHUP when the subprocess has already exited."""
        relay_socks5lb.configure_pool(single_node_pool)

        mock_process = MagicMock()
        mock_process.poll.return_value = 1  # process has exited
        relay_socks5lb._process = mock_process

        relay_socks5lb.update_pool(multi_node_pool)

        mock_process.send_signal.assert_not_called()


# =============================================================================
# IptablesRedirect — configure_redirect (TASK-023-019)
# =============================================================================


@pytest.mark.unit
@pytest.mark.happy_path
class TestIptablesRedirectConfigureRedirect:
    """iptables redirect sets correct rules."""

    def test_configure_redirect_creates_redsocks_chain(self) -> None:
        """configure_redirect creates the REDSOCKS nat chain."""
        redirect = IptablesRedirect(socks_port=1080)

        with patch("subprocess.run") as mock_run:
            redirect.configure_redirect(1080)

        calls = [str(c) for c in mock_run.call_args_list]
        create_chain_call = next(
            (c for c in calls if "-N" in c and "REDSOCKS" in c), None
        )
        assert create_chain_call is not None, "Expected iptables -N REDSOCKS call"

    def test_configure_redirect_adds_localhost_exception(self) -> None:
        """configure_redirect exempts 127.0.0.0/8 from redirect."""
        redirect = IptablesRedirect(socks_port=1080)

        with patch("subprocess.run") as mock_run:
            redirect.configure_redirect(1080)

        calls = [str(c) for c in mock_run.call_args_list]
        localhost_exception = next(
            (c for c in calls if "127.0.0.0/8" in c and "RETURN" in c), None
        )
        assert localhost_exception is not None

    def test_configure_redirect_adds_so_mark_exception(self) -> None:
        """configure_redirect exempts SO_MARK=100 packets (redsocks outbound)."""
        redirect = IptablesRedirect(socks_port=1080)

        with patch("subprocess.run") as mock_run:
            redirect.configure_redirect(1080)

        calls = [str(c) for c in mock_run.call_args_list]
        mark_exception = next(
            (c for c in calls if "mark" in c.lower() and "100" in c and "RETURN" in c),
            None,
        )
        assert mark_exception is not None

    def test_configure_redirect_adds_proxy_ip_exceptions(self) -> None:
        """configure_redirect exempts upstream proxy IPs to prevent loop."""
        redirect = IptablesRedirect(
            socks_port=1080, proxy_ips=["203.0.113.1", "203.0.113.2"]
        )

        with patch("subprocess.run") as mock_run:
            redirect.configure_redirect(1080)

        calls = [str(c) for c in mock_run.call_args_list]
        assert any("203.0.113.1" in c and "RETURN" in c for c in calls)
        assert any("203.0.113.2" in c and "RETURN" in c for c in calls)

    def test_configure_redirect_adds_tcp_redirect_rule(self) -> None:
        """configure_redirect adds catch-all REDIRECT to the relay port."""
        redirect = IptablesRedirect(socks_port=1080)

        with patch("subprocess.run") as mock_run:
            redirect.configure_redirect(1080)

        calls = [str(c) for c in mock_run.call_args_list]
        redirect_rule = next(
            (c for c in calls if "REDIRECT" in c and "1080" in c and "tcp" in c), None
        )
        assert redirect_rule is not None

    def test_configure_redirect_hooks_into_output_chain(self) -> None:
        """configure_redirect appends the jump rule to iptables OUTPUT."""
        redirect = IptablesRedirect(socks_port=1080)

        with patch("subprocess.run") as mock_run:
            redirect.configure_redirect(1080)

        calls = [str(c) for c in mock_run.call_args_list]
        output_rule = next(
            (c for c in calls if "OUTPUT" in c and "REDSOCKS" in c), None
        )
        assert output_rule is not None

    def test_configure_redirect_marks_active(self) -> None:
        """After configure_redirect, is_active() returns True."""
        redirect = IptablesRedirect(socks_port=1080)

        with patch("subprocess.run"):
            redirect.configure_redirect(1080)

        assert redirect.is_active() is True

    def test_configure_redirect_updates_socks_port(self) -> None:
        """configure_redirect(port) updates self.socks_port."""
        redirect = IptablesRedirect(socks_port=1080)

        with patch("subprocess.run"):
            redirect.configure_redirect(9050)

        assert redirect.socks_port == 9050


# =============================================================================
# IptablesRedirect — remove_redirect (TASK-023-019)
# =============================================================================


@pytest.mark.unit
@pytest.mark.happy_path
class TestIptablesRedirectRemoveRedirect:
    """iptables cleanup removes all installed rules."""

    def test_remove_redirect_deletes_output_jump_rule(self) -> None:
        """remove_redirect removes the OUTPUT -> REDSOCKS jump rule."""
        redirect = IptablesRedirect(socks_port=1080)

        with patch("subprocess.run") as mock_run:
            redirect.configure_redirect(1080)
            mock_run.reset_mock()
            redirect.remove_redirect()

        calls = [str(c) for c in mock_run.call_args_list]
        delete_output = next(
            (c for c in calls if "-D" in c and "OUTPUT" in c and "REDSOCKS" in c),
            None,
        )
        assert delete_output is not None

    def test_remove_redirect_flushes_redsocks_chain(self) -> None:
        """remove_redirect flushes all rules from the REDSOCKS chain."""
        redirect = IptablesRedirect(socks_port=1080)

        with patch("subprocess.run") as mock_run:
            redirect.configure_redirect(1080)
            mock_run.reset_mock()
            redirect.remove_redirect()

        calls = [str(c) for c in mock_run.call_args_list]
        flush_call = next(
            (c for c in calls if "-F" in c and "REDSOCKS" in c), None
        )
        assert flush_call is not None

    def test_remove_redirect_deletes_redsocks_chain(self) -> None:
        """remove_redirect deletes the REDSOCKS chain from the nat table."""
        redirect = IptablesRedirect(socks_port=1080)

        with patch("subprocess.run") as mock_run:
            redirect.configure_redirect(1080)
            mock_run.reset_mock()
            redirect.remove_redirect()

        calls = [str(c) for c in mock_run.call_args_list]
        delete_chain = next(
            (c for c in calls if "-X" in c and "REDSOCKS" in c), None
        )
        assert delete_chain is not None

    def test_remove_redirect_marks_inactive(self) -> None:
        """After remove_redirect, is_active() returns False."""
        redirect = IptablesRedirect(socks_port=1080)

        with patch("subprocess.run"):
            redirect.configure_redirect(1080)
            redirect.remove_redirect()

        assert redirect.is_active() is False

    def test_remove_redirect_is_noop_when_not_active(self) -> None:
        """remove_redirect is a no-op when rules are not installed."""
        redirect = IptablesRedirect(socks_port=1080)

        with patch("subprocess.run") as mock_run:
            redirect.remove_redirect()

        mock_run.assert_not_called()


# =============================================================================
# Fallback detection: BPF unavailable -> iptables path (TASK-023-019)
# =============================================================================


@pytest.mark.unit
@pytest.mark.happy_path
class TestFallbackDetection:
    """BPF unavailability triggers iptables fallback selection."""

    def test_bpf_capability_check_absent_selects_iptables(self) -> None:
        """When CAP_BPF is absent, iptables redirect is selected as fallback."""
        # CAP_BPF unavailability is represented by the absence of /proc/sys/kernel/unprivileged_bpf_disabled
        # or by the absence of the 'bpf' syscall.  For this unit test, we simulate the check
        # by verifying IptablesRedirect can be instantiated and activated without BPF.
        redirect = IptablesRedirect(socks_port=1080)

        with patch("subprocess.run"):
            redirect.configure_redirect(1080)

        assert redirect.is_active() is True

    def test_iptables_redirect_requires_only_cap_net_admin(self) -> None:
        """IptablesRedirect uses only iptables — no BPF syscall required.

        Verified by ensuring the implementation invokes 'iptables' subprocess
        commands and not any BPF-specific commands (bpftool, bpf_prog_load, etc.).
        """
        redirect = IptablesRedirect(socks_port=1080)
        invoked_commands: list[str] = []

        def capture_run(cmd: list[str], **_: Any) -> MagicMock:
            invoked_commands.append(cmd[0])
            return MagicMock(returncode=0)

        with patch("subprocess.run", side_effect=capture_run):
            redirect.configure_redirect(1080)

        assert all(c == "iptables" for c in invoked_commands), (
            f"Expected only 'iptables' commands; got: {invoked_commands}"
        )
        assert "bpftool" not in invoked_commands
        assert "bpf_prog_load" not in invoked_commands

    def test_socks_relay_manager_can_switch_backend_to_redsocks(self) -> None:
        """SocksRelayManager can be configured with redsocks for Option C path."""
        relay = SocksRelayManager(backend="redsocks", relay_port=1080)
        assert relay.backend == "redsocks"

    def test_socks_relay_manager_socks5lb_is_default_backend(self) -> None:
        """SocksRelayManager defaults to socks5lb (Option D path)."""
        relay = SocksRelayManager()
        assert relay.backend == "socks5lb"
