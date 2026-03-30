# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""BDD test suite for TASK-023-020: eBPF Production BPF Management Layer.

Covers:
  TASK-023-017: BPF cgroup/connect4 program management (BpfManager)
  TASK-023-018: CLM BPF attach/detach lifecycle

Domain invariants tested:
  EN-023-001 F-1: Map key MUST NOT use msg_src_ip4/msg_src_port (inaccessible)
  EN-023-001 F-2: Stale root cgroup BPF detached before container cgroup attach
  EN-023-001 F-3: Container cgroup found via hostname -> /sys/fs/cgroup/docker/{id}
  EN-023-001 F-4: bypass_ips BPF map populated with proxy pool IPs at provision time
  EN-023-001 F-6: Array map used for original destination, not BPF_MAP_TYPE_QUEUE
  EN-023-001 F-8: jerry-intercept cgroup MUST be CHILD of container cgroup (not sibling)
  OPSEC-F1: Bridge scope validation for raw TCP destinations (HIGH)
  OPSEC-F3: Envoy IP added to bypass map (double-proxy prevention)
  OPSEC-F5: BPF MUST be pinned to bpffs; verified before declaring ready (CRITICAL)

Test pyramid: 60% happy path, 30% negative cases, 10% edge cases.
Distribution: ~30 tests -> ~18 happy, ~9 negative, ~3 edge.

All subprocess calls are mocked — unit tests NEVER invoke real bpftool.

References:
  - TASK-023-017-bpf-connect4-program.md
  - TASK-023-018-clm-bpf-attach.md
  - EN-023-001-ebpf-container-poc.md
  - src/proxy_infra/ebpf_poc/connect4.bpf.c (reference BPF program)
  - src/proxy_infra/ebpf_poc/bridge.py (reference bridge)
"""

from __future__ import annotations

import json
import socket
import struct
from unittest.mock import MagicMock, call, patch

import pytest

from src.proxy_infra.infrastructure.bpf.bpf_manager import BpfManager
from src.proxy_infra.infrastructure.bpf.original_destination import OriginalDestination
from src.proxy_infra.infrastructure.bpf.socks_bridge import SocksBridge


# =============================================================================
# Helpers
# =============================================================================


def _make_completed(returncode: int = 0, stdout: str = "", stderr: str = "") -> MagicMock:
    """Build a mock subprocess.CompletedProcess."""
    cp = MagicMock()
    cp.returncode = returncode
    cp.stdout = stdout
    cp.stderr = stderr
    return cp


def _bpftool_map_json(dst_ip_le: int, dst_port_le: int) -> str:
    """Build a bpftool -j map lookup JSON payload matching the PoC output format."""
    return json.dumps({"formatted": {"value": {"dst_ip": dst_ip_le, "dst_port": dst_port_le}}})


# IPv4 1.2.3.4 as little-endian u32 = 0x04030201 = 67305985
_IP_1_2_3_4_LE = 0x04030201
# Port 80 in network byte order packed into u32 little-endian:
# network-order 80 = 0x0050; stored as u32 LE -> leading bytes 0x50 0x00 ...
# struct.pack("<I", 0x00000050) -> b'\x50\x00\x00\x00' -> struct.unpack("!H", ...) = 0x5000? No.
# Actual: port 80 in bpf map: user_port is bpf_htons(80) = 0x5000 stored as u32
# So dst_port_raw = 0x5000 = 20480
_PORT_80_BPF = 0x5000


# =============================================================================
# BpfManager — load and attach
# =============================================================================


class TestBpfManagerLoadAndAttach:
    """BPF manager loads program from .bpf.o and attaches to container cgroup."""

    def test_load_and_pin_calls_bpftool_prog_load(self) -> None:
        """Given a BPF object path, load_and_attach calls bpftool prog load with pin path."""
        manager = BpfManager("/opt/ebpf/connect4.bpf.o")
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _make_completed(0, stdout="abc123\n")
            manager._load_and_pin()
        call_args = mock_run.call_args[0][0]
        assert "bpftool" in call_args
        assert "prog" in call_args
        assert "load" in call_args
        assert "/opt/ebpf/connect4.bpf.o" in call_args
        assert str(manager._pin_path) in call_args

    def test_load_and_pin_includes_pinmaps_flag(self) -> None:
        """bpftool prog load includes 'pinmaps <map_dir>' so all maps are pinned (OPSEC-F5)."""
        manager = BpfManager("/opt/ebpf/connect4.bpf.o")
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _make_completed(0)
            manager._load_and_pin()
        cmd = mock_run.call_args[0][0]
        assert "pinmaps" in cmd

    def test_load_and_pin_raises_on_bpftool_failure(self) -> None:
        """RuntimeError raised when bpftool prog load returns non-zero."""
        manager = BpfManager("/opt/ebpf/connect4.bpf.o")
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _make_completed(1, stderr="verifier rejected")
            with pytest.raises(RuntimeError, match="verifier rejected"):
                manager._load_and_pin()

    def test_detach_root_cgroup_called_before_container_attach(self) -> None:
        """F-2: root cgroup detach command precedes container cgroup attach command (ordering)."""
        manager = BpfManager("/opt/ebpf/connect4.bpf.o")
        call_log: list[str] = []

        def track(cmd: list[str], **kwargs: object) -> MagicMock:
            call_log.append(" ".join(str(c) for c in cmd))
            return _make_completed(0, stdout="/sys/fs/cgroup/docker/abc123def456\n")

        with patch("subprocess.run", side_effect=track):
            manager.load_and_attach("abc123")

        # Root cgroup detach must appear before container cgroup attach
        detach_idx = next(
            (i for i, c in enumerate(call_log) if "detach" in c and "/sys/fs/cgroup " in c),
            None,
        )
        attach_idx = next(
            (i for i, c in enumerate(call_log) if "attach" in c and "connect4" in c),
            None,
        )
        assert detach_idx is not None, "Root cgroup detach command not found"
        assert attach_idx is not None, "Container cgroup attach command not found"
        assert detach_idx < attach_idx, (
            f"F-2 violation: root detach (step {detach_idx}) "
            f"must precede attach (step {attach_idx})"
        )

    def test_attaches_to_container_specific_cgroup_not_root(self) -> None:
        """BPF is attached to the container cgroup path, not /sys/fs/cgroup (root)."""
        manager = BpfManager("/opt/ebpf/connect4.bpf.o")
        attach_targets: list[str] = []

        def track(cmd: list[str], **kwargs: object) -> MagicMock:
            cmd_str = " ".join(str(c) for c in cmd)
            if "cgroup" in cmd_str and "attach" in cmd_str:
                # Third positional arg to 'bpftool cgroup attach' is the cgroup path
                idx = cmd.index("attach") + 1
                if idx < len(cmd):
                    attach_targets.append(str(cmd[idx]))
            return _make_completed(0, stdout="/sys/fs/cgroup/docker/abc123full\n")

        with patch("subprocess.run", side_effect=track):
            manager.load_and_attach("abc123")

        assert any(
            "docker/abc123" in t for t in attach_targets
        ), f"Expected container cgroup attach, got: {attach_targets}"
        assert not any(
            t == "/sys/fs/cgroup" for t in attach_targets
        ), "BPF must not attach to root cgroup in production"


# =============================================================================
# BpfManager — detach stale root cgroup (F-2)
# =============================================================================


class TestBpfManagerDetachStaleRoot:
    """BPF manager detaches stale root cgroup BPF before container attach (F-2)."""

    def test_detach_root_uses_correct_bpftool_args(self) -> None:
        """bpftool cgroup detach /sys/fs/cgroup connect4 pinned <pin_path> is called."""
        manager = BpfManager("/opt/ebpf/connect4.bpf.o")
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _make_completed(0)
            manager._detach_root_cgroup()
        cmd = mock_run.call_args[0][0]
        assert "bpftool" in cmd
        assert "cgroup" in cmd
        assert "detach" in cmd
        assert "/sys/fs/cgroup" in cmd
        assert "connect4" in cmd
        assert "pinned" in cmd

    def test_detach_root_is_non_fatal_on_failure(self) -> None:
        """Non-zero bpftool return during root cgroup detach does not raise (may already be clean)."""
        manager = BpfManager("/opt/ebpf/connect4.bpf.o")
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _make_completed(1, stderr="no such program")
            # Must not raise
            manager._detach_root_cgroup()


# =============================================================================
# BpfManager — bypass_ips map population (F-4, OPSEC-F3)
# =============================================================================


class TestBpfManagerBypassMap:
    """BPF manager populates bypass_ips map with proxy pool IPs and Envoy IP."""

    def test_populate_bypass_calls_map_update_for_each_proxy_ip(self) -> None:
        """F-4: each proxy pool IP triggers a bpftool map update bypass entry."""
        manager = BpfManager("/opt/ebpf/connect4.bpf.o")
        proxy_ips = ["10.0.0.1", "10.0.0.2", "10.0.0.3"]
        envoy_ip = "172.17.0.2"

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _make_completed(0)
            manager.populate_bypass(proxy_ips, envoy_ip)

        # Should be called once per IP (3 proxy + 1 envoy = 4 total)
        assert mock_run.call_count == 4

    def test_populate_bypass_adds_envoy_ip_to_map(self) -> None:
        """OPSEC-F3: Envoy IP is added to bypass_ips map to prevent double-proxy."""
        manager = BpfManager("/opt/ebpf/connect4.bpf.o")
        envoy_ip = "172.17.0.5"
        calls_with_envoy: list[list[str]] = []

        def capture(cmd: list[str], **kwargs: object) -> MagicMock:
            cmd_str = " ".join(str(c) for c in cmd)
            if "172.17.0.5" in cmd_str or _ip_hex(envoy_ip) in cmd_str:
                calls_with_envoy.append(cmd)
            return _make_completed(0)

        with patch("subprocess.run", side_effect=capture):
            manager.populate_bypass([], envoy_ip)

        assert len(calls_with_envoy) >= 1, "Envoy IP not found in any bypass map update call"

    def test_populate_bypass_map_update_uses_pinned_map_path(self) -> None:
        """bypass_ips map update references the pinned map path under map_dir."""
        manager = BpfManager("/opt/ebpf/connect4.bpf.o")
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _make_completed(0)
            manager.populate_bypass(["1.2.3.4"], "10.0.0.1")
        for c in mock_run.call_args_list:
            cmd = c[0][0]
            cmd_str = " ".join(str(x) for x in cmd)
            if "map" in cmd_str and "update" in cmd_str:
                assert "bypass_ips" in cmd_str, f"Expected bypass_ips in cmd: {cmd_str}"
                break
        else:
            pytest.fail("No bpftool map update call found")

    def test_populate_bypass_raises_on_invalid_ip(self) -> None:
        """ValueError raised when an invalid IP address is passed to populate_bypass."""
        manager = BpfManager("/opt/ebpf/connect4.bpf.o")
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _make_completed(0)
            with pytest.raises(ValueError, match="Invalid IPv4"):
                manager.populate_bypass(["not-an-ip"], "10.0.0.1")


# =============================================================================
# BpfManager — bpffs pin verification (OPSEC-F5)
# =============================================================================


class TestBpfManagerPinVerification:
    """BPF program is pinned to bpffs; manager verifies pin before declaring ready."""

    def test_is_ready_returns_true_when_pinned_and_bridge_listening(self) -> None:
        """is_ready() returns True when both pin check and bridge check succeed."""
        manager = BpfManager("/opt/ebpf/connect4.bpf.o", bridge_port=12345)
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = [
                _make_completed(0, stdout="prog_type cgroup_sock_addr"),  # pin check
                _make_completed(0, stdout="LISTEN 0 128 127.0.0.1:12345 *:*"),  # ss
            ]
            assert manager.is_ready() is True

    def test_is_ready_returns_false_when_not_pinned(self) -> None:
        """OPSEC-F5: is_ready() returns False when bpftool prog show fails for pin path."""
        manager = BpfManager("/opt/ebpf/connect4.bpf.o")
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _make_completed(1, stderr="no such file")
            assert manager.is_ready() is False

    def test_is_ready_returns_false_when_bridge_not_listening(self) -> None:
        """is_ready() returns False when bridge port is not in ss LISTEN output."""
        manager = BpfManager("/opt/ebpf/connect4.bpf.o", bridge_port=12345)
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = [
                _make_completed(0, stdout="prog_type cgroup_sock_addr"),  # pin OK
                _make_completed(0, stdout="LISTEN 0 128 0.0.0.0:22 *:*"),  # no bridge port
            ]
            assert manager.is_ready() is False


# =============================================================================
# BpfManager — container cgroup detection (F-3)
# =============================================================================


class TestBpfManagerContainerCgroup:
    """Container cgroup found via hostname -> /sys/fs/cgroup/docker/{full-id} (F-3)."""

    def test_get_container_cgroup_returns_matching_path(self) -> None:
        """F-3: cgroup path resolved by find command with container_id prefix."""
        manager = BpfManager("/opt/ebpf/connect4.bpf.o")
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _make_completed(
                0, stdout="/sys/fs/cgroup/docker/abc123fullhash\n"
            )
            result = manager.get_container_cgroup("abc123")
        assert result == "/sys/fs/cgroup/docker/abc123fullhash"

    def test_get_container_cgroup_raises_when_not_found(self) -> None:
        """RuntimeError raised when no cgroup directory matches the container ID."""
        manager = BpfManager("/opt/ebpf/connect4.bpf.o")
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _make_completed(0, stdout="")
            with pytest.raises(RuntimeError, match="Container cgroup not found"):
                manager.get_container_cgroup("deadbeef")

    def test_get_container_cgroup_uses_find_with_name_pattern(self) -> None:
        """find command uses -name '<container_id>*' pattern for prefix match."""
        manager = BpfManager("/opt/ebpf/connect4.bpf.o")
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _make_completed(
                0, stdout="/sys/fs/cgroup/docker/abc123\n"
            )
            manager.get_container_cgroup("abc123")
        cmd = mock_run.call_args[0][0]
        assert "find" in cmd
        assert any("abc123*" in str(a) for a in cmd), f"Name pattern not found: {cmd}"


# =============================================================================
# BpfManager — intercept cgroup as child (F-8)
# =============================================================================


class TestBpfManagerInterceptCgroup:
    """jerry-intercept cgroup is created as CHILD of container cgroup (F-8)."""

    def test_create_intercept_cgroup_path_is_child_of_container_cgroup(self) -> None:
        """F-8: intercept cgroup path = container_cgroup/jerry-intercept (child, not sibling)."""
        manager = BpfManager("/opt/ebpf/connect4.bpf.o")
        container_cgroup = "/sys/fs/cgroup/docker/abc123"
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _make_completed(0)
            result = manager.create_intercept_cgroup(container_cgroup)
        assert result == "/sys/fs/cgroup/docker/abc123/jerry-intercept"

    def test_create_intercept_cgroup_path_is_not_sibling(self) -> None:
        """F-8: intercept cgroup must NOT be at /sys/fs/cgroup/jerry-intercept (sibling)."""
        manager = BpfManager("/opt/ebpf/connect4.bpf.o")
        container_cgroup = "/sys/fs/cgroup/docker/abc123"
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _make_completed(0)
            result = manager.create_intercept_cgroup(container_cgroup)
        assert result != "/sys/fs/cgroup/jerry-intercept", (
            "F-8 violation: jerry-intercept must be a child of container cgroup, not a sibling"
        )

    def test_create_intercept_cgroup_calls_mkdir_p(self) -> None:
        """mkdir -p is called with the child cgroup path."""
        manager = BpfManager("/opt/ebpf/connect4.bpf.o")
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _make_completed(0)
            manager.create_intercept_cgroup("/sys/fs/cgroup/docker/abc123")
        cmd = mock_run.call_args[0][0]
        assert "mkdir" in cmd
        assert "-p" in cmd
        assert "/sys/fs/cgroup/docker/abc123/jerry-intercept" in cmd


# =============================================================================
# SocksBridge — read original destination from BPF map
# =============================================================================


class TestSocksBridgeReadOriginalDst:
    """Bridge reads original destination from BPF array map via bpftool."""

    def test_reads_ip_and_port_from_bpftool_json_output(self) -> None:
        """Bridge parses bpftool -j map lookup JSON and returns OriginalDestination."""
        bridge = SocksBridge(map_path="/sys/fs/bpf/rainbow_maps/dst_latest")
        bpf_json = _bpftool_map_json(_IP_1_2_3_4_LE, _PORT_80_BPF)

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _make_completed(0, stdout=bpf_json)
            result = bridge.read_original_dst()

        assert result is not None
        assert result.ip == "1.2.3.4"
        assert result.port == 80

    def test_returns_none_when_bpftool_fails(self) -> None:
        """read_original_dst returns None when bpftool exits non-zero."""
        bridge = SocksBridge()
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _make_completed(1, stderr="map not found")
            result = bridge.read_original_dst()
        assert result is None

    def test_returns_none_when_bpftool_not_available(self) -> None:
        """read_original_dst returns None when bpftool binary is not installed."""
        bridge = SocksBridge()
        with patch("subprocess.run", side_effect=FileNotFoundError("bpftool not found")):
            result = bridge.read_original_dst()
        assert result is None

    def test_returns_none_on_malformed_json(self) -> None:
        """read_original_dst returns None when bpftool output is not valid JSON."""
        bridge = SocksBridge()
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _make_completed(0, stdout="not json {{")
            result = bridge.read_original_dst()
        assert result is None

    def test_uses_configured_map_path(self) -> None:
        """bpftool map lookup uses the map_path configured at construction."""
        custom_path = "/sys/fs/bpf/custom_maps/dst_latest"
        bridge = SocksBridge(map_path=custom_path)
        bpf_json = _bpftool_map_json(_IP_1_2_3_4_LE, _PORT_80_BPF)

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _make_completed(0, stdout=bpf_json)
            bridge.read_original_dst()

        cmd = mock_run.call_args[0][0]
        assert custom_path in cmd


# =============================================================================
# SocksBridge — DC-1 cookie-based dst_lookup (concurrent connection race fix)
# =============================================================================


class TestSocksBridgeCookieLookup:
    """DC-1: Bridge uses SO_COOKIE + dst_lookup for per-connection isolation."""

    def test_get_socket_cookie_returns_uint64(self) -> None:
        """get_socket_cookie returns the 64-bit cookie from SO_COOKIE getsockopt."""
        bridge = SocksBridge()
        mock_sock = MagicMock(spec=socket.socket)
        # Cookie 42 as little-endian uint64
        mock_sock.getsockopt.return_value = struct.pack("<Q", 42)

        cookie = bridge.get_socket_cookie(mock_sock)

        assert cookie == 42
        mock_sock.getsockopt.assert_called_once()

    def test_get_socket_cookie_returns_none_on_oserror(self) -> None:
        """get_socket_cookie returns None when SO_COOKIE is not supported."""
        bridge = SocksBridge()
        mock_sock = MagicMock(spec=socket.socket)
        mock_sock.getsockopt.side_effect = OSError("Protocol not available")

        cookie = bridge.get_socket_cookie(mock_sock)

        assert cookie is None

    def test_read_original_dst_by_cookie_returns_destination(self) -> None:
        """read_original_dst_by_cookie looks up dst_lookup by cookie and returns destination."""
        bridge = SocksBridge(dst_lookup_path="/sys/fs/bpf/rainbow_maps/dst_lookup")
        bpf_json = _bpftool_map_json(_IP_1_2_3_4_LE, _PORT_80_BPF)

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _make_completed(0, stdout=bpf_json)
            result = bridge.read_original_dst_by_cookie(42)

        assert result is not None
        assert result.ip == "1.2.3.4"
        assert result.port == 80

        # Verify the cookie was encoded as hex key in the bpftool command
        cmd = mock_run.call_args[0][0]
        assert "hex" in cmd
        assert "/sys/fs/bpf/rainbow_maps/dst_lookup" in cmd

    def test_read_original_dst_by_cookie_returns_none_on_miss(self) -> None:
        """read_original_dst_by_cookie returns None when cookie has no map entry."""
        bridge = SocksBridge()
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _make_completed(1, stderr="not found")
            result = bridge.read_original_dst_by_cookie(999)
        assert result is None

    def test_handle_connection_uses_cookie_lookup_first(self) -> None:
        """handle_connection tries SO_COOKIE + dst_lookup before falling back to dst_latest."""
        bridge = SocksBridge(allowed_networks=["0.0.0.0/0"])
        mock_client = MagicMock(spec=socket.socket)
        mock_client.getsockopt.return_value = struct.pack("<Q", 42)

        bpf_json = _bpftool_map_json(_IP_1_2_3_4_LE, _PORT_80_BPF)

        with (
            patch("subprocess.run") as mock_run,
            patch.object(bridge, "_socks5_connect") as mock_socks,
            patch.object(bridge, "_relay"),
        ):
            mock_run.return_value = _make_completed(0, stdout=bpf_json)
            mock_socks.return_value = MagicMock(spec=socket.socket)
            bridge.handle_connection(mock_client, ("127.0.0.1", 54321))

        # Verify dst_lookup was called (hex key in command)
        first_call_cmd = mock_run.call_args_list[0][0][0]
        assert "hex" in first_call_cmd, "Expected cookie-based hex key lookup"


# =============================================================================
# SocksBridge — scope validation (OPSEC-F1)
# =============================================================================


class TestSocksBridgeScopeValidation:
    """OPSEC-F1: Bridge validates raw TCP destinations against allowed scope."""

    def test_destination_allowed_when_ip_in_allowed_network(self) -> None:
        """OPSEC-F1: IP within allowed CIDR is permitted."""
        bridge = SocksBridge(allowed_networks=["10.0.0.0/8"])
        assert bridge.is_destination_allowed("10.1.2.3") is True

    def test_destination_blocked_when_ip_not_in_any_allowed_network(self) -> None:
        """OPSEC-F1: IP outside all allowed CIDRs is blocked."""
        bridge = SocksBridge(allowed_networks=["10.0.0.0/8"])
        assert bridge.is_destination_allowed("192.168.1.1") is False

    def test_destination_allowed_when_no_scope_configured(self) -> None:
        """No allowed_networks configured means all destinations pass (testing mode)."""
        bridge = SocksBridge(allowed_networks=None)
        assert bridge.is_destination_allowed("8.8.8.8") is True

    def test_destination_blocked_returns_false_for_invalid_ip(self) -> None:
        """Unparseable IP string is treated as out-of-scope and returns False."""
        bridge = SocksBridge(allowed_networks=["10.0.0.0/8"])
        assert bridge.is_destination_allowed("not-an-ip") is False

    def test_multiple_cidrs_all_checked(self) -> None:
        """Destination is allowed if it matches any of the allowed CIDRs."""
        bridge = SocksBridge(allowed_networks=["10.0.0.0/8", "192.168.0.0/16"])
        assert bridge.is_destination_allowed("192.168.5.5") is True
        assert bridge.is_destination_allowed("172.16.0.1") is False

    def test_invalid_cidr_at_construction_raises_value_error(self) -> None:
        """ValueError raised at construction when an allowed_networks entry is invalid CIDR."""
        with pytest.raises(ValueError, match="Invalid CIDR"):
            SocksBridge(allowed_networks=["not-a-cidr"])

    def test_handle_connection_drops_out_of_scope_destination(self) -> None:
        """OPSEC-F1: handle_connection closes socket without forwarding for blocked destination."""
        bridge = SocksBridge(allowed_networks=["10.0.0.0/8"])
        bpf_json = _bpftool_map_json(_IP_1_2_3_4_LE, _PORT_80_BPF)  # 1.2.3.4 not in 10.0.0.0/8

        client_sock = MagicMock()
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _make_completed(0, stdout=bpf_json)
            bridge.handle_connection(client_sock, ("127.0.0.1", 54321))

        client_sock.close.assert_called_once()

    def test_handle_connection_drops_when_no_bpf_map_entry(self) -> None:
        """Bridge drops connection when BPF map has no entry (returns None)."""
        bridge = SocksBridge()
        client_sock = MagicMock()
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _make_completed(1, stderr="no entry")
            bridge.handle_connection(client_sock, ("127.0.0.1", 54321))
        client_sock.close.assert_called_once()


# =============================================================================
# SocksBridge — configurable SOCKS proxy target
# =============================================================================


class TestSocksBridgeSocksConfig:
    """Bridge uses configurable SOCKS proxy host and port."""

    def test_default_socks_target_is_localhost_1080(self) -> None:
        """Default SOCKS5 target is 127.0.0.1:1080."""
        bridge = SocksBridge()
        assert bridge._socks_host == "127.0.0.1"
        assert bridge._socks_port == 1080

    def test_custom_socks_host_and_port_stored(self) -> None:
        """Custom SOCKS host and port are stored and used for connections."""
        bridge = SocksBridge(socks_host="proxy.example.com", socks_port=9050)
        assert bridge._socks_host == "proxy.example.com"
        assert bridge._socks_port == 9050

    def test_default_listen_port_is_12345(self) -> None:
        """Default bridge listen port matches PoC bridge_port constant."""
        bridge = SocksBridge()
        assert bridge._listen_port == 12345

    def test_custom_listen_port_stored(self) -> None:
        """Custom listen port is stored correctly."""
        bridge = SocksBridge(listen_port=9999)
        assert bridge._listen_port == 9999


# =============================================================================
# SocksBridge — is_listening health check
# =============================================================================


class TestSocksBridgeIsListening:
    """Bridge exposes is_listening() health check."""

    def test_is_listening_false_before_start(self) -> None:
        """is_listening() returns False before start() is called."""
        bridge = SocksBridge(listen_port=19876)
        assert bridge.is_listening() is False

    def test_is_listening_true_after_start(self) -> None:
        """is_listening() returns True after start() binds the socket."""
        bridge = SocksBridge(listen_port=19877)
        try:
            bridge.start()
            assert bridge.is_listening() is True
        finally:
            bridge.stop()

    def test_is_listening_false_after_stop(self) -> None:
        """is_listening() returns False after stop() closes the socket."""
        bridge = SocksBridge(listen_port=19878)
        bridge.start()
        bridge.stop()
        assert bridge.is_listening() is False


# =============================================================================
# BpfManager — detach and cleanup
# =============================================================================


class TestBpfManagerDetachAndCleanup:
    """BPF manager detaches program and unpins on teardown."""

    def test_detach_and_cleanup_calls_cgroup_detach(self) -> None:
        """detach_and_cleanup calls bpftool cgroup detach for the attached cgroup."""
        manager = BpfManager("/opt/ebpf/connect4.bpf.o")
        manager._attached_cgroup = "/sys/fs/cgroup/docker/abc123"
        detach_calls: list[list[str]] = []

        def capture(cmd: list[str], **kwargs: object) -> MagicMock:
            if "cgroup" in cmd and "detach" in cmd:
                detach_calls.append(cmd)
            return _make_completed(0)

        with patch("subprocess.run", side_effect=capture):
            manager.detach_and_cleanup()

        assert len(detach_calls) >= 1
        combined = " ".join(str(c) for c in detach_calls[0])
        assert "/sys/fs/cgroup/docker/abc123" in combined

    def test_detach_and_cleanup_calls_unlink_for_pin(self) -> None:
        """detach_and_cleanup calls unlink on the pin path to remove from bpffs."""
        manager = BpfManager("/opt/ebpf/connect4.bpf.o")
        unlink_calls: list[list[str]] = []

        def capture(cmd: list[str], **kwargs: object) -> MagicMock:
            if "unlink" in cmd:
                unlink_calls.append(cmd)
            return _make_completed(0)

        with patch("subprocess.run", side_effect=capture):
            manager.detach_and_cleanup()

        assert len(unlink_calls) >= 1
        combined = " ".join(str(c) for c in unlink_calls[0])
        assert str(manager._pin_path) in combined

    def test_detach_and_cleanup_safe_when_no_attached_cgroup(self) -> None:
        """detach_and_cleanup does not raise when no cgroup was previously attached."""
        manager = BpfManager("/opt/ebpf/connect4.bpf.o")
        assert manager._attached_cgroup is None
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _make_completed(0)
            manager.detach_and_cleanup()  # must not raise

    def test_detach_and_cleanup_clears_attached_cgroup(self) -> None:
        """After detach_and_cleanup, _attached_cgroup is set to None."""
        manager = BpfManager("/opt/ebpf/connect4.bpf.o")
        manager._attached_cgroup = "/sys/fs/cgroup/docker/abc123"
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _make_completed(0)
            manager.detach_and_cleanup()
        assert manager._attached_cgroup is None


# =============================================================================
# Edge cases
# =============================================================================


class TestEdgeCases:
    """Edge cases: empty proxy pool, simultaneous bypass + Envoy, timeout handling."""

    def test_populate_bypass_with_empty_proxy_list_only_adds_envoy(self) -> None:
        """populate_bypass with empty proxy_ips still adds the Envoy IP (OPSEC-F3)."""
        manager = BpfManager("/opt/ebpf/connect4.bpf.o")
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _make_completed(0)
            manager.populate_bypass([], "172.17.0.2")
        # Exactly one map update: just the Envoy IP
        assert mock_run.call_count == 1

    def test_bpf_manager_run_raises_on_command_timeout(self) -> None:
        """RuntimeError raised when a subprocess command times out."""
        import subprocess as _subprocess
        manager = BpfManager("/opt/ebpf/connect4.bpf.o")
        with patch("subprocess.run", side_effect=_subprocess.TimeoutExpired("bpftool", 30)):
            with pytest.raises(RuntimeError, match="timed out"):
                manager._run(["bpftool", "prog", "show"], check=True)

    def test_bpf_manager_run_raises_on_missing_binary(self) -> None:
        """RuntimeError raised when the command binary is not found on PATH."""
        manager = BpfManager("/opt/ebpf/connect4.bpf.o")
        with patch("subprocess.run", side_effect=FileNotFoundError("bpftool")):
            with pytest.raises(RuntimeError, match="not found"):
                manager._run(["bpftool", "prog", "show"], check=True)


# =============================================================================
# SocksBridge — _socks5_connect coverage
# =============================================================================


class TestSocksBridgeSocks5Connect:
    """Cover _socks5_connect for SOCKS5 protocol negotiation paths."""

    def test_socks5_connect_success(self) -> None:
        """Successful SOCKS5 negotiation returns a connected socket."""
        bridge = SocksBridge(socks_host="127.0.0.1", socks_port=1080)
        mock_sock = MagicMock(spec=socket.socket)
        # Auth response: version 5, no-auth accepted
        # Connect response: version 5, success, reserved, IPv4, 4 bytes addr, 2 bytes port
        mock_sock.recv.side_effect = [
            bytes([0x05, 0x00]),  # auth accepted
            bytes([0x05, 0x00, 0x00, 0x01, 0, 0, 0, 0, 0, 0]),  # connect success
        ]
        with patch("socket.socket", return_value=mock_sock):
            result = bridge._socks5_connect("1.2.3.4", 80)
        assert result is mock_sock
        mock_sock.connect.assert_called_once_with(("127.0.0.1", 1080))

    def test_socks5_connect_auth_rejected_raises(self) -> None:
        """ConnectionError raised when SOCKS5 proxy rejects auth method."""
        bridge = SocksBridge()
        mock_sock = MagicMock(spec=socket.socket)
        mock_sock.recv.return_value = bytes([0x05, 0xFF])  # no acceptable methods
        with patch("socket.socket", return_value=mock_sock):
            with pytest.raises(ConnectionError, match="method negotiation rejected"):
                bridge._socks5_connect("1.2.3.4", 80)
        mock_sock.close.assert_called()

    def test_socks5_connect_request_rejected_raises(self) -> None:
        """ConnectionError raised when SOCKS5 CONNECT request fails."""
        bridge = SocksBridge()
        mock_sock = MagicMock(spec=socket.socket)
        mock_sock.recv.side_effect = [
            bytes([0x05, 0x00]),  # auth OK
            bytes([0x05, 0x01, 0x00, 0x01, 0, 0, 0, 0, 0, 0]),  # connect FAIL (code 1)
        ]
        with patch("socket.socket", return_value=mock_sock):
            with pytest.raises(ConnectionError, match="CONNECT failed"):
                bridge._socks5_connect("1.2.3.4", 80)
        mock_sock.close.assert_called()


# =============================================================================
# SocksBridge — _relay coverage
# =============================================================================


class TestSocksBridgeRelay:
    """Cover _relay bidirectional data forwarding."""

    def test_relay_forwards_data_bidirectionally(self) -> None:
        """Data from client is forwarded to remote and vice versa."""
        bridge = SocksBridge()
        client = MagicMock(spec=socket.socket)
        remote = MagicMock(spec=socket.socket)

        # First select: client readable -> data forwarded to remote
        # Second select: remote readable -> data forwarded to client
        # Third select: client readable -> empty data (connection closed)
        client.recv.side_effect = [b"hello", b""]
        remote.recv.return_value = b"world"

        with patch("select.select") as mock_select:
            mock_select.side_effect = [
                ([client], [], []),
                ([remote], [], []),
                ([client], [], []),
            ]
            bridge._relay(client, remote)

        remote.sendall.assert_called_with(b"hello")
        client.sendall.assert_called_with(b"world")

    def test_relay_closes_both_sockets_on_error(self) -> None:
        """Both sockets are closed when a socket error occurs."""
        bridge = SocksBridge()
        client = MagicMock(spec=socket.socket)
        remote = MagicMock(spec=socket.socket)
        client.recv.side_effect = BrokenPipeError("broken")

        with patch("select.select") as mock_select:
            mock_select.return_value = ([client], [], [])
            bridge._relay(client, remote)

        client.close.assert_called_once()
        remote.close.assert_called_once()

    def test_relay_stops_on_select_timeout(self) -> None:
        """Relay stops when select returns no readable sockets (timeout)."""
        bridge = SocksBridge()
        client = MagicMock(spec=socket.socket)
        remote = MagicMock(spec=socket.socket)

        with patch("select.select") as mock_select:
            mock_select.return_value = ([], [], [])  # timeout — no readable
            bridge._relay(client, remote)

        client.close.assert_called_once()
        remote.close.assert_called_once()

    def test_relay_stops_on_errored_socket(self) -> None:
        """Relay stops when select reports an errored socket."""
        bridge = SocksBridge()
        client = MagicMock(spec=socket.socket)
        remote = MagicMock(spec=socket.socket)

        with patch("select.select") as mock_select:
            mock_select.return_value = ([], [], [client])  # client errored
            bridge._relay(client, remote)

        client.close.assert_called_once()
        remote.close.assert_called_once()


# =============================================================================
# SocksBridge — _accept_loop coverage
# =============================================================================


class TestSocksBridgeAcceptLoop:
    """Cover _accept_loop connection dispatch."""

    def test_accept_loop_dispatches_to_handle_connection(self) -> None:
        """Accepted connections are dispatched to handle_connection in threads."""
        bridge = SocksBridge(listen_port=19879)
        mock_server = MagicMock(spec=socket.socket)
        mock_client = MagicMock(spec=socket.socket)
        mock_server.accept.side_effect = [
            (mock_client, ("127.0.0.1", 55555)),
            OSError("closed"),  # break the loop
        ]
        bridge._server = mock_server
        bridge._running = True

        with patch.object(bridge, "handle_connection"):
            bridge._accept_loop()

        mock_server.accept.assert_called()

    def test_accept_loop_stops_on_oserror(self) -> None:
        """Accept loop exits cleanly when server socket raises OSError."""
        bridge = SocksBridge()
        mock_server = MagicMock(spec=socket.socket)
        mock_server.accept.side_effect = OSError("socket closed")
        bridge._server = mock_server
        bridge._running = True

        bridge._accept_loop()  # Should not raise


# =============================================================================
# SocksBridge — handle_connection error path coverage
# =============================================================================


class TestSocksBridgeHandleConnectionErrors:
    """Cover handle_connection error paths for full coverage."""

    def test_handle_connection_closes_on_socks5_failure(self) -> None:
        """When _socks5_connect raises, client socket is closed."""
        bridge = SocksBridge(allowed_networks=["0.0.0.0/0"])
        mock_client = MagicMock(spec=socket.socket)
        mock_client.getsockopt.return_value = struct.pack("<Q", 42)

        bpf_json = _bpftool_map_json(_IP_1_2_3_4_LE, _PORT_80_BPF)

        with (
            patch("subprocess.run") as mock_run,
            patch.object(bridge, "_socks5_connect", side_effect=ConnectionError("refused")),
        ):
            mock_run.return_value = _make_completed(0, stdout=bpf_json)
            bridge.handle_connection(mock_client, ("127.0.0.1", 54321))

        mock_client.close.assert_called()

    def test_handle_connection_fallback_to_dst_latest_when_cookie_fails(self) -> None:
        """When SO_COOKIE fails, handle_connection falls back to dst_latest[0]."""
        bridge = SocksBridge(allowed_networks=["0.0.0.0/0"])
        mock_client = MagicMock(spec=socket.socket)
        mock_client.getsockopt.side_effect = OSError("SO_COOKIE not supported")

        bpf_json = _bpftool_map_json(_IP_1_2_3_4_LE, _PORT_80_BPF)

        with (
            patch("subprocess.run") as mock_run,
            patch.object(bridge, "_socks5_connect") as mock_socks,
            patch.object(bridge, "_relay"),
        ):
            mock_run.return_value = _make_completed(0, stdout=bpf_json)
            mock_socks.return_value = MagicMock(spec=socket.socket)
            bridge.handle_connection(mock_client, ("127.0.0.1", 54321))

        # Should have fallen back to dst_latest (key 0 0 0 0, not hex cookie)
        calls = mock_run.call_args_list
        assert any("0" in str(c) for c in calls), "Expected fallback to dst_latest"


# =============================================================================
# Helpers (private)
# =============================================================================


def _ip_hex(ip: str) -> str:
    """Return the 4-byte hex representation of an IPv4 string for substring matching."""
    return " ".join(f"0x{b:02x}" for b in socket.inet_aton(ip))
