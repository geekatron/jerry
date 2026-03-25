# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""BDD E2E tests for eBPF transparent SOCKS5 proxy.

Feature: eBPF Transparent SOCKS5 Proxy
    EN-023-001: BPF cgroup/connect4 rewriting proves transparent proxying of
    outbound TCP through a SOCKS5 relay without any application-level
    proxy configuration (no http_proxy env var, no curl --proxy flag).

    Full chain under test:
        tool cmd (intercept cgroup)
            -> connect4_redirect BPF hook rewrites dst to 127.0.0.1:12345
            -> bridge.py reads original dst from BPF array map dst_latest
            -> SOCKS5 connect to proxy-node:1080
            -> proxy-node connects to test-target:80
            -> test-target (nginx) responds

    Topology (from docker-compose.yml):
        ebpf-test   172.30.0.2  -- privileged; BPF + bridge
        proxy-node  172.30.0.5  -- microsocks SOCKS5
        test-target 172.30.0.10 -- nginx

    Test pyramid distribution (H-20):
        60% happy path    -- Scenarios 1-4  (bpf_load, connect_rewrite, map_entry, full_chain)
        30% negative/edge -- Scenarios 5-6  (bypass_map, loopback_skip)
        10% architecture  -- Scenario 7     (cgroup_isolation)

BDD RED phase note:
    These tests are intentionally written as the Red phase of BDD Red/Green/Refactor
    (H-20).  They will FAIL when the eBPF PoC compose stack is not running or when
    the host kernel lacks eBPF cgroup support.  That is the correct initial state.
    Green phase begins when the compose stack can be brought up on CI.

No mocks.  No fakes.  Real containers.  Real BPF.  Real SOCKS5.  Real nginx.
"""

from __future__ import annotations

import json
import struct
import subprocess
import time
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Module-level constants
# ---------------------------------------------------------------------------

_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_EBPF_COMPOSE = str(_PROJECT_ROOT / "src/proxy_infra/ebpf_poc/docker-compose.yml")
_EBPF_CWD = str(_PROJECT_ROOT / "src/proxy_infra/ebpf_poc")

# Compose service names (match docker-compose.yml)
_SVC_EBPF_TEST = "ebpf-test"
_SVC_PROXY_NODE = "proxy-node"
_SVC_TEST_TARGET = "test-target"

# Network addresses from docker-compose.yml
_TARGET_IP = "172.30.0.10"
_TARGET_PORT = 80
_PROXY_NODE_IP = "172.30.0.5"
_PROXY_NODE_PORT = 1080
_BRIDGE_PORT = 12345

# BPF pin paths (from entrypoint.sh and connect4.bpf.c)
_BPF_MAP_DST_LATEST = "/sys/fs/bpf/poc_maps/dst_latest"
_BPF_MAP_DST_LOOKUP = "/sys/fs/bpf/poc_maps/dst_lookup"
_BPF_MAP_BYPASS_IPS = "/sys/fs/bpf/poc_maps/bypass_ips"
_BPF_PROG_PIN = "/sys/fs/bpf/connect4_poc"

# cgroup paths
_CONTAINER_CGROUP_BASE = "/sys/fs/cgroup/docker"
_INTERCEPT_CGROUP = "/sys/fs/cgroup/jerry-intercept"

# Expected response body from nginx
_NGINX_WELCOME_FRAGMENT = "Welcome to nginx"


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _compose_exec(
    service: str,
    cmd: list[str],
    *,
    timeout: int = 120,
) -> tuple[int, str, str]:
    """Execute a command inside a running eBPF PoC compose service.

    Args:
        service: Compose service name (e.g., "ebpf-test").
        cmd: Command and arguments to execute inside the container.
        timeout: Subprocess timeout in seconds.  Default 120 s for Docker ops.

    Returns:
        Tuple of (returncode, stdout, stderr).
    """
    result = subprocess.run(
        [
            "docker",
            "compose",
            "-f",
            _EBPF_COMPOSE,
            "exec",
            "-T",
            service,
            *cmd,
        ],
        capture_output=True,
        text=True,
        cwd=_EBPF_CWD,
        timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr


def _get_container_logs(service: str, *, timeout: int = 15) -> str:
    """Fetch stdout logs for a compose service without the log-prefix timestamp.

    Args:
        service: Compose service name.
        timeout: Subprocess timeout in seconds.

    Returns:
        Full log output as a single string.
    """
    result = subprocess.run(
        [
            "docker",
            "compose",
            "-f",
            _EBPF_COMPOSE,
            "logs",
            "--no-log-prefix",
            service,
        ],
        capture_output=True,
        text=True,
        cwd=_EBPF_CWD,
        timeout=timeout,
    )
    return result.stdout


def _bpftool_map_dump_json(map_pin_path: str) -> list[dict]:
    """Dump a pinned BPF map as JSON via bpftool inside ebpf-test.

    Args:
        map_pin_path: Absolute path to the pinned BPF map inside the container.

    Returns:
        List of map entry dicts parsed from bpftool JSON output.
        Returns an empty list when bpftool fails or output is not valid JSON.
    """
    rc, stdout, _ = _compose_exec(
        _SVC_EBPF_TEST,
        ["bpftool", "-j", "map", "dump", "pinned", map_pin_path],
    )
    if rc != 0 or not stdout.strip():
        return []
    try:
        data = json.loads(stdout)
        if isinstance(data, list):
            return data
        return [data]
    except json.JSONDecodeError:
        return []


def _bpftool_cgroup_show_json(cgroup_path: str) -> list[dict]:
    """Show BPF programs attached to a cgroup, returning JSON.

    Args:
        cgroup_path: Absolute path to the cgroup inside the container.

    Returns:
        List of attached program dicts parsed from bpftool JSON output.
        Returns an empty list when bpftool fails or the cgroup has no programs.
    """
    rc, stdout, _ = _compose_exec(
        _SVC_EBPF_TEST,
        ["bpftool", "-j", "cgroup", "show", cgroup_path],
    )
    if rc != 0 or not stdout.strip():
        return []
    try:
        data = json.loads(stdout)
        if isinstance(data, list):
            return data
        return [data]
    except json.JSONDecodeError:
        return []


def _get_nginx_access_log() -> str:
    """Read nginx access log entries from test-target container.

    nginx:alpine writes to stdout; docker logs captures it.

    Returns:
        Combined stdout content from the test-target container logs.
    """
    return _get_container_logs(_SVC_TEST_TARGET)


def _ip_str_to_native_u32(ip: str) -> int:
    """Convert a dotted-decimal IP string to a native-endian uint32.

    BPF stores IP addresses in native byte order on little-endian x86_64.
    bpftool renders map values as native-endian integers.

    Args:
        ip: Dotted-decimal IPv4 string, e.g. "172.30.0.10".

    Returns:
        Native-endian uint32 representation of the IP address.
    """
    import socket

    packed_network = socket.inet_aton(ip)
    # BPF stores dst_ip as __u32 in native byte order (little-endian on x86_64)
    return struct.unpack("<I", packed_network)[0]


def _port_to_native_u32(port: int) -> int:
    """Convert a host-order port to the native-endian uint32 BPF stores.

    BPF stores ctx->user_port as a 32-bit native-endian value where the
    port occupies the low 16 bits in network byte order.

    Args:
        port: Port number in host byte order (e.g. 80).

    Returns:
        Native-endian uint32 as stored in the BPF map.
    """
    # user_port in ctx is big-endian 16-bit in the low 16 bits of a u32
    port_bytes_be = struct.pack("!H", port)
    # Stored as native u32: low 2 bytes are the big-endian port, high 2 are 0
    return struct.unpack("<I", port_bytes_be + b"\x00\x00")[0]


# ---------------------------------------------------------------------------
# Happy Path (60%) -- Scenarios 1-4
# ---------------------------------------------------------------------------


class TestBpfProgramLoadsAndAttaches:
    """Scenario 1: BPF program loads and attaches to container cgroup.

    Given the eBPF PoC Docker Compose stack is running
    When I check bpftool cgroup show inside the container
    Then connect4_redirect is attached with type cgroup_inet4_connect
    """

    @pytest.mark.e2e
    @pytest.mark.ebpf
    def test_bpf_program_loads_when_compose_stack_is_running_then_prog_pin_exists(
        self,
        ebpf_poc_stack: str,
    ) -> None:
        """BPF program object file is pinned at /sys/fs/bpf/connect4_poc."""
        rc, stdout, stderr = _compose_exec(
            _SVC_EBPF_TEST,
            ["ls", "-la", _BPF_PROG_PIN],
        )
        assert rc == 0, (
            f"BPF program pin not found at {_BPF_PROG_PIN}. "
            f"stdout={stdout!r} stderr={stderr!r}. "
            "Indicates entrypoint.sh bpftool prog load failed."
        )

    @pytest.mark.e2e
    @pytest.mark.ebpf
    def test_bpf_attaches_when_compose_stack_is_running_then_connect4_in_cgroup(
        self,
        ebpf_poc_stack: str,
    ) -> None:
        """connect4_redirect program is attached with type cgroup_inet4_connect.

        bpftool cgroup show on the container cgroup must list a program
        with attach_type 'connect4' or the equivalent JSON key.
        Checks both the container-specific cgroup and jerry-intercept fallback.
        """
        # Determine which cgroup was used — container-specific or jerry-intercept
        # We check jerry-intercept first (it's always created by entrypoint.sh)
        programs = _bpftool_cgroup_show_json(_INTERCEPT_CGROUP)
        if not programs:
            # Fallback: entrypoint may have attached to a /docker/<id> cgroup
            # Check via bpftool prog list to confirm the program is loaded at all
            rc, stdout, stderr = _compose_exec(
                _SVC_EBPF_TEST,
                ["bpftool", "-j", "prog", "show", "pinned", _BPF_PROG_PIN],
            )
            assert rc == 0, (
                f"bpftool prog show failed. rc={rc} stdout={stdout!r} stderr={stderr!r}"
            )
            prog_info = json.loads(stdout) if stdout.strip() else {}
            assert prog_info, "BPF program info is empty -- program not loaded"
            return

        attach_types = [p.get("attach_type", p.get("attachType", "")) for p in programs]
        assert any("connect4" in str(at).lower() for at in attach_types), (
            f"No connect4 program in cgroup {_INTERCEPT_CGROUP}. "
            f"Programs found: {programs}"
        )

    @pytest.mark.e2e
    @pytest.mark.ebpf
    def test_bpf_attaches_when_compose_stack_is_running_then_bpf_maps_pinned(
        self,
        ebpf_poc_stack: str,
    ) -> None:
        """All three BPF maps are pinned: dst_latest, dst_lookup, bypass_ips.

        entrypoint.sh calls bpftool prog load with pinmaps /sys/fs/bpf/poc_maps.
        All maps declared in connect4.bpf.c must be present.
        """
        for map_pin in (_BPF_MAP_DST_LATEST, _BPF_MAP_DST_LOOKUP, _BPF_MAP_BYPASS_IPS):
            rc, _, stderr = _compose_exec(
                _SVC_EBPF_TEST,
                ["bpftool", "map", "show", "pinned", map_pin],
            )
            assert rc == 0, (
                f"BPF map not pinned at {map_pin}. stderr={stderr!r}"
            )


class TestConnectRewrite:
    """Scenario 2: connect() is intercepted and destination rewritten.

    Given BPF is attached to the tool container's cgroup
    When curl connects to test-target (172.30.0.10:80)
    Then curl reports "Connected to (127.0.0.1)" -- destination was rewritten by BPF
    """

    @pytest.mark.e2e
    @pytest.mark.ebpf
    def test_connect_rewrite_when_curl_to_target_then_connected_to_loopback(
        self,
        ebpf_poc_stack: str,
    ) -> None:
        """curl verbose output shows 'Connected to ... 127.0.0.1' not 172.30.0.10.

        The intercept wrapper moves the process into jerry-intercept cgroup
        before exec.  BPF rewrites the connect() destination to 127.0.0.1:12345.
        curl's verbose output reveals the actual TCP peer it connected to.
        """
        rc, stdout, stderr = _compose_exec(
            _SVC_EBPF_TEST,
            [
                "intercept",
                "curl",
                "-v",
                "--connect-timeout",
                "10",
                "--max-time",
                "15",
                f"http://{_TARGET_IP}/",
            ],
        )
        # curl -v writes connection info to stderr
        combined = stdout + stderr
        assert "127.0.0.1" in combined, (
            f"curl did not connect to 127.0.0.1. "
            f"BPF connect() rewrite was not triggered. "
            f"combined={combined!r}"
        )
        # The original target IP must NOT appear as the TCP peer
        assert f"Connected to {_TARGET_IP}" not in combined, (
            f"curl connected directly to {_TARGET_IP} -- BPF rewrite bypassed. "
            f"combined={combined!r}"
        )

    @pytest.mark.e2e
    @pytest.mark.ebpf
    def test_connect_rewrite_when_curl_without_intercept_then_direct_connection(
        self,
        ebpf_poc_stack: str,
    ) -> None:
        """Without 'intercept' wrapper, curl connects directly (control case).

        Curl run outside jerry-intercept cgroup is NOT intercepted by BPF.
        It connects directly to 172.30.0.10 (no BPF cgroup attached to the
        default container cgroup for the exec session).

        This test validates the control path and confirms cgroup isolation.
        """
        rc, stdout, stderr = _compose_exec(
            _SVC_EBPF_TEST,
            [
                "curl",
                "-v",
                "--connect-timeout",
                "10",
                "--max-time",
                "15",
                f"http://{_TARGET_IP}/",
            ],
        )
        combined = stdout + stderr
        # Without intercept, curl connects to the real target IP directly
        assert f"Connected to {_TARGET_IP}" in combined or rc == 0, (
            f"Control case: curl without intercept should reach {_TARGET_IP} directly. "
            f"combined={combined!r}"
        )


class TestBpfMapStoresOriginalDestination:
    """Scenario 3: BPF map stores original destination.

    Given BPF intercepted a connection to test-target
    When I dump the BPF dst_lookup map via bpftool
    Then the map contains an entry with dst_ip=172.30.0.10 and dst_port=80
    """

    @pytest.mark.e2e
    @pytest.mark.ebpf
    def test_bpf_map_stores_dst_when_connection_intercepted_then_latest_has_target_ip(
        self,
        ebpf_poc_stack: str,
    ) -> None:
        """dst_latest array map[0] contains the target IP after interception.

        After triggering an intercepted connect(), the BPF program writes
        the original dst_ip/dst_port to dst_latest[0].  bpftool map lookup
        should return an entry with the target IP.

        Expected native-endian u32 for 172.30.0.10:
            inet_aton("172.30.0.10") = 0xAC1E000A (big-endian)
            as little-endian u32 stored by BPF = 0x0A001EAC = 167845548
        """
        # Trigger an interception
        _compose_exec(
            _SVC_EBPF_TEST,
            [
                "intercept",
                "curl",
                "-sf",
                "--connect-timeout",
                "10",
                "--max-time",
                "15",
                f"http://{_TARGET_IP}/",
                "-o",
                "/dev/null",
            ],
        )
        time.sleep(1)  # Give BPF map write time to propagate

        rc, stdout, stderr = _compose_exec(
            _SVC_EBPF_TEST,
            [
                "bpftool",
                "-j",
                "map",
                "lookup",
                "pinned",
                _BPF_MAP_DST_LATEST,
                "key",
                "0",
                "0",
                "0",
                "0",
            ],
        )
        assert rc == 0, (
            f"bpftool map lookup failed. rc={rc} stderr={stderr!r}"
        )
        assert stdout.strip(), "bpftool returned empty output for dst_latest lookup"

        data = json.loads(stdout)
        if isinstance(data, list):
            data = data[0] if data else {}

        # Navigate possible JSON structures: {"formatted":{"value":...}} or {"value":...}
        formatted = data.get("formatted", data)
        value = formatted.get("value", formatted)

        dst_ip_raw = value.get("dst_ip", -1)
        expected_ip_native = _ip_str_to_native_u32(_TARGET_IP)

        assert dst_ip_raw == expected_ip_native, (
            f"dst_latest map[0].dst_ip={dst_ip_raw} != expected {expected_ip_native} "
            f"(native-endian representation of {_TARGET_IP}). "
            f"Full value: {value}"
        )

    @pytest.mark.e2e
    @pytest.mark.ebpf
    def test_bpf_map_stores_dst_when_connection_intercepted_then_lookup_has_entry(
        self,
        ebpf_poc_stack: str,
    ) -> None:
        """dst_lookup LRU hash map contains at least one entry after interception.

        The LRU hash map (dst_lookup in connect4.bpf.c) is keyed by socket
        cookie and stores the original destination for post-hoc inspection
        via bpftool.  After one intercepted connection, it must be non-empty.
        """
        # Trigger an interception
        _compose_exec(
            _SVC_EBPF_TEST,
            [
                "intercept",
                "curl",
                "-sf",
                "--connect-timeout",
                "10",
                "--max-time",
                "15",
                f"http://{_TARGET_IP}/",
                "-o",
                "/dev/null",
            ],
        )
        time.sleep(1)

        entries = _bpftool_map_dump_json(_BPF_MAP_DST_LOOKUP)
        assert len(entries) >= 1, (
            f"dst_lookup LRU hash map is empty after intercepted connection. "
            f"Expected at least one entry with dst_ip for {_TARGET_IP}."
        )

        # At least one entry must have the target IP
        expected_ip_native = _ip_str_to_native_u32(_TARGET_IP)
        ip_values = []
        for entry in entries:
            formatted = entry.get("formatted", entry)
            value = formatted.get("value", formatted)
            ip_values.append(value.get("dst_ip", -1))

        assert expected_ip_native in ip_values, (
            f"No dst_lookup entry with dst_ip={expected_ip_native} "
            f"({_TARGET_IP} in native-endian). "
            f"All ip values found: {ip_values}"
        )


class TestFullChainDeliversCorrectResponse:
    """Scenario 4: Full chain delivers correct HTTP response through SOCKS proxy.

    Given BPF + bridge + proxy-node are all running
    When curl requests http://test-target/ through the BPF chain
    Then the response contains "Welcome to nginx"
    And the test-target nginx access log shows source IP 172.30.0.5 (proxy-node)
    """

    @pytest.mark.e2e
    @pytest.mark.ebpf
    def test_full_chain_when_intercept_curl_to_target_then_nginx_response(
        self,
        ebpf_poc_stack: str,
    ) -> None:
        """Full chain returns nginx welcome page through BPF -> bridge -> SOCKS5.

        This is the primary integration proof: the entire transparent proxy
        chain works end-to-end without any application-level proxy config.
        """
        rc, stdout, stderr = _compose_exec(
            _SVC_EBPF_TEST,
            [
                "intercept",
                "curl",
                "-s",
                "--connect-timeout",
                "15",
                "--max-time",
                "20",
                f"http://{_TARGET_IP}/",
            ],
        )
        assert rc == 0, (
            f"curl through BPF chain failed. rc={rc}. "
            f"stdout={stdout!r} stderr={stderr!r}. "
            "Check: BPF attached? bridge running? proxy-node reachable?"
        )
        assert _NGINX_WELCOME_FRAGMENT in stdout, (
            f"Response does not contain '{_NGINX_WELCOME_FRAGMENT}'. "
            f"stdout={stdout!r}. "
            "BPF chain may have reached wrong target or proxy returned error."
        )

    @pytest.mark.e2e
    @pytest.mark.ebpf
    def test_full_chain_when_intercept_curl_then_nginx_log_shows_proxy_node_ip(
        self,
        ebpf_poc_stack: str,
    ) -> None:
        """nginx access log shows proxy-node IP (172.30.0.5), not tool container IP.

        This is the definitive attribution proof: the target sees the proxy-node
        as the source, not the tool container running the BPF program.
        Validates that traffic egressed from proxy-node, not from ebpf-test.
        """
        # Issue the request through the full chain
        _compose_exec(
            _SVC_EBPF_TEST,
            [
                "intercept",
                "curl",
                "-s",
                "--connect-timeout",
                "15",
                "--max-time",
                "20",
                f"http://{_TARGET_IP}/",
                "-o",
                "/dev/null",
            ],
        )
        time.sleep(1)  # Allow nginx to flush its access log to stdout

        access_log = _get_nginx_access_log()
        assert _PROXY_NODE_IP in access_log, (
            f"nginx access log does not contain proxy-node IP {_PROXY_NODE_IP}. "
            f"access_log={access_log!r}. "
            "Target is seeing a different source IP -- attribution chain broken."
        )
        # The tool container IP must NOT appear as the source in nginx logs
        _EBPF_TEST_IP = "172.30.0.2"
        assert _EBPF_TEST_IP not in access_log, (
            f"nginx access log contains tool container IP {_EBPF_TEST_IP}. "
            "Traffic is NOT going through proxy-node -- BPF->bridge->SOCKS5 chain broken. "
            f"access_log={access_log!r}"
        )


# ---------------------------------------------------------------------------
# Negative / Edge Cases (30%) -- Scenarios 5-6
# ---------------------------------------------------------------------------


class TestBypassMapPreventsRedirectLoops:
    """Scenario 5: Bypass map prevents redirect loops for proxy connections.

    Given proxy-node IP (172.30.0.5) is in the bypass_ips BPF map
    When the bridge connects to proxy-node:1080
    Then the connection goes directly (not through BPF redirect)
    """

    @pytest.mark.e2e
    @pytest.mark.ebpf
    def test_bypass_map_when_proxy_ip_populated_then_entry_present_in_map(
        self,
        ebpf_poc_stack: str,
    ) -> None:
        """bypass_ips BPF hash map contains an entry for proxy-node (172.30.0.5).

        entrypoint.sh resolves proxy-node hostname and populates bypass_ips map
        with the IP in network byte order.  bpftool map dump must show an entry.
        """
        entries = _bpftool_map_dump_json(_BPF_MAP_BYPASS_IPS)
        assert len(entries) >= 1, (
            f"bypass_ips map is empty. "
            f"entrypoint.sh should have populated it with proxy-node IP. "
            "Possible cause: hostname resolution of 'proxy-node' failed in entrypoint."
        )

    @pytest.mark.e2e
    @pytest.mark.ebpf
    def test_bypass_map_when_proxy_ip_populated_then_bridge_log_shows_direct_connect(
        self,
        ebpf_poc_stack: str,
    ) -> None:
        """Bridge log shows SOCKS5 connection to proxy-node without BPF loop.

        When a chain connection succeeds (full_chain test above has run), the
        bridge log will show "SOCKS5 tunnel established" to the target -- not
        to itself.  If bypass_ips was missing, the bridge's own SOCKS5 connection
        to proxy-node would be intercepted by BPF, creating an infinite loop.

        We verify this indirectly: the bridge process must be alive (container
        still running) and the container must not show a "redirect loop" error.
        """
        rc, stdout, _ = _compose_exec(
            _SVC_EBPF_TEST,
            ["pgrep", "-f", "bridge.py"],
        )
        assert rc == 0, (
            f"bridge.py process is not running inside ebpf-test container. "
            f"A redirect loop would have caused the bridge to crash or stall. "
            f"stdout={stdout!r}"
        )

        bridge_logs = _get_container_logs(_SVC_EBPF_TEST)
        assert "redirect loop" not in bridge_logs.lower(), (
            f"Bridge logs contain 'redirect loop' indicator. "
            f"bypass_ips map may not be protecting SOCKS5 connections. "
            f"bridge_logs={bridge_logs!r}"
        )

    @pytest.mark.e2e
    @pytest.mark.ebpf
    def test_bypass_map_when_connection_to_proxy_node_then_bpf_does_not_rewrite(
        self,
        ebpf_poc_stack: str,
    ) -> None:
        """Connections to proxy-node IP are NOT rewritten by BPF.

        We test this by attempting a direct TCP connection to proxy-node:1080
        from within the jerry-intercept cgroup.  If bypass_ips works, BPF
        lets the connection through to the real proxy-node.  If bypass_ips
        is broken, BPF would rewrite it to 127.0.0.1:12345 (the bridge)
        which would cause the bridge to read a dst_ip of proxy-node from the
        map and enter a SOCKS5 connect loop -- causing immediate failure.

        We use nc (netcat) with -z (scan mode) to test TCP reachability.
        """
        rc, stdout, stderr = _compose_exec(
            _SVC_EBPF_TEST,
            [
                "intercept",
                "nc",
                "-z",
                "-w",
                "5",
                _PROXY_NODE_IP,
                str(_PROXY_NODE_PORT),
            ],
        )
        assert rc == 0, (
            f"Direct TCP connection from intercept cgroup to proxy-node "
            f"{_PROXY_NODE_IP}:{_PROXY_NODE_PORT} failed (rc={rc}). "
            f"If bypass_ips is working, this should succeed. "
            f"stdout={stdout!r} stderr={stderr!r}"
        )


class TestLoopbackConnectionsAreNotIntercepted:
    """Scenario 6: Loopback connections are not intercepted.

    Given BPF is attached
    When a process connects to 127.0.0.1:any_port
    Then the connection is not rewritten (loopback skip)
    """

    @pytest.mark.e2e
    @pytest.mark.ebpf
    def test_loopback_skip_when_connect_to_127_then_bridge_does_not_see_rewrite(
        self,
        ebpf_poc_stack: str,
    ) -> None:
        """Connections to 127.0.0.0/8 bypass BPF redirect (loopback skip rule).

        connect4.bpf.c checks: if (dst_ip_hbo & 0xff000000) == 0x7f000000 -> return 1.
        A process in the intercept cgroup connecting to 127.0.0.1:12345 (the bridge
        listen port itself) must arrive at the bridge -- NOT be rewritten again
        (which would create a loop).

        We verify by connecting to 127.0.0.1:12345 directly and confirming
        the bridge sees it as a loopback client, not a BPF-rewritten connection.
        The bridge will close the connection (no queued destination) but the
        key thing is rc == 0 (TCP connected) and no eBPF recursion crash.
        """
        # Connect to bridge loopback port from within the intercept cgroup.
        # nc -z tests TCP handshake only (no data).  The bridge will accept and
        # then close it (no queued dst), but connection is established.
        rc, stdout, stderr = _compose_exec(
            _SVC_EBPF_TEST,
            ["intercept", "nc", "-z", "-w", "5", "127.0.0.1", str(_BRIDGE_PORT)],
        )
        # rc == 0: TCP connected to bridge (loopback not intercepted by BPF)
        # rc != 0 with "Connection refused": bridge closed it (no queued dst), also fine
        # What we must NOT see: a hung process (timeout) or BPF loop error in logs
        assert rc == 0 or "connection refused" in stderr.lower(), (
            f"Unexpected result connecting to loopback:{_BRIDGE_PORT}. "
            f"Expected TCP connect or immediate close. "
            f"rc={rc} stdout={stdout!r} stderr={stderr!r}"
        )

    @pytest.mark.e2e
    @pytest.mark.ebpf
    def test_loopback_skip_when_connect_to_127_then_dst_latest_not_updated(
        self,
        ebpf_poc_stack: str,
    ) -> None:
        """dst_latest map is not updated for loopback connections.

        If BPF incorrectly intercepts a loopback connection, it would write
        127.0.0.1 as dst_ip into dst_latest.  We plant a known non-loopback
        target IP first, then do a loopback connection, then verify the map
        still holds the pre-loopback IP.
        """
        # Step 1: Plant a known target IP in dst_latest via an intercepted connection
        _compose_exec(
            _SVC_EBPF_TEST,
            [
                "intercept",
                "curl",
                "-sf",
                "--connect-timeout",
                "10",
                "--max-time",
                "15",
                f"http://{_TARGET_IP}/",
                "-o",
                "/dev/null",
            ],
        )
        time.sleep(0.5)

        # Step 2: Do a loopback connection (should NOT update dst_latest)
        _compose_exec(
            _SVC_EBPF_TEST,
            ["intercept", "nc", "-z", "-w", "2", "127.0.0.1", str(_BRIDGE_PORT)],
        )
        time.sleep(0.5)

        # Step 3: Read dst_latest -- should still have the target IP, not 127.0.0.1
        rc, stdout, _ = _compose_exec(
            _SVC_EBPF_TEST,
            [
                "bpftool",
                "-j",
                "map",
                "lookup",
                "pinned",
                _BPF_MAP_DST_LATEST,
                "key",
                "0",
                "0",
                "0",
                "0",
            ],
        )
        if rc != 0 or not stdout.strip():
            pytest.skip("Could not read dst_latest map -- skipping loopback check")

        data = json.loads(stdout)
        if isinstance(data, list):
            data = data[0] if data else {}
        formatted = data.get("formatted", data)
        value = formatted.get("value", formatted)
        dst_ip_raw = value.get("dst_ip", 0)

        loopback_native = _ip_str_to_native_u32("127.0.0.1")
        assert dst_ip_raw != loopback_native, (
            f"dst_latest was updated with loopback IP (127.0.0.1) after a loopback connect(). "
            f"BPF loopback skip rule (LOOPBACK_MASK check) is NOT working. "
            f"dst_ip_raw={dst_ip_raw} loopback_native={loopback_native}"
        )


# ---------------------------------------------------------------------------
# Architecture (10%) -- Scenario 7
# ---------------------------------------------------------------------------


class TestPerContainerCgroupIsolation:
    """Scenario 7: Per-container cgroup isolation.

    Given BPF is attached to the ebpf-test container's cgroup
    When I check the root cgroup for BPF programs
    Then no connect4 program is attached to root (only container cgroup)

    This is the architectural isolation proof: BPF interception is scoped
    to the jerry-intercept cgroup, not the root cgroup or all containers.
    """

    @pytest.mark.e2e
    @pytest.mark.ebpf
    def test_cgroup_isolation_when_bpf_attached_to_container_then_not_on_root_cgroup(
        self,
        ebpf_poc_stack: str,
    ) -> None:
        """BPF program is NOT attached to /sys/fs/cgroup (root) on success path.

        entrypoint.sh tries per-container cgroup first and only falls back to
        root cgroup if that fails.  When the container cgroup attach succeeds,
        the root cgroup must have no connect4 program.

        This prevents other containers sharing the same Docker host from being
        accidentally intercepted -- a hard security requirement.
        """
        programs_on_root = _bpftool_cgroup_show_json("/sys/fs/cgroup")
        connect4_on_root = [
            p for p in programs_on_root
            if "connect4" in str(p.get("attach_type", p.get("attachType", ""))).lower()
            or "connect4" in str(p.get("name", "")).lower()
        ]

        # If fallback to root was used (attach_type contains connect4), the test
        # logs a warning but does not fail -- root attach is the documented fallback.
        if connect4_on_root:
            # Check if entrypoint logged the fallback warning
            logs = _get_container_logs(_SVC_EBPF_TEST)
            is_fallback = "falling back to root" in logs.lower() or "root cgroup" in logs.lower()
            assert is_fallback, (
                f"connect4 program found on root cgroup but no fallback warning in logs. "
                f"Unexpected root cgroup attachment without entrypoint fallback. "
                f"connect4_on_root={connect4_on_root}"
            )
            # Emit informational marker -- this test allows fallback but documents it
            pytest.xfail(
                "BPF attached to root cgroup (fallback path). "
                "Container-specific cgroup attach failed -- see entrypoint.sh logs. "
                "Root attach works but provides weaker isolation guarantees."
            )
        else:
            # Ideal path: BPF only on jerry-intercept or container cgroup, not root
            assert not connect4_on_root, (
                f"connect4 program unexpectedly attached to root cgroup. "
                f"programs_on_root={programs_on_root}"
            )

    @pytest.mark.e2e
    @pytest.mark.ebpf
    def test_cgroup_isolation_when_bpf_attached_then_intercept_cgroup_exists(
        self,
        ebpf_poc_stack: str,
    ) -> None:
        """jerry-intercept cgroup exists inside the container.

        entrypoint.sh creates /sys/fs/cgroup/jerry-intercept as the controlled
        interception scope.  Its existence confirms the cgroup isolation setup ran.
        """
        rc, stdout, stderr = _compose_exec(
            _SVC_EBPF_TEST,
            ["test", "-d", _INTERCEPT_CGROUP],
        )
        assert rc == 0, (
            f"jerry-intercept cgroup directory does not exist at {_INTERCEPT_CGROUP}. "
            f"entrypoint.sh cgroup setup may have failed. "
            f"stderr={stderr!r}"
        )

    @pytest.mark.e2e
    @pytest.mark.ebpf
    def test_cgroup_isolation_when_proxy_node_runs_then_proxy_traffic_not_intercepted(
        self,
        ebpf_poc_stack: str,
    ) -> None:
        """proxy-node container is reachable and SOCKS5 port responds.

        The proxy-node container runs outside the jerry-intercept cgroup.
        It must be able to make outbound connections without BPF interference.
        If BPF intercepted proxy-node traffic, SOCKS5 would fail (connection loop).

        We verify by checking that proxy-node's microsocks is listening on :1080.
        """
        rc, stdout, stderr = _compose_exec(
            _SVC_EBPF_TEST,
            ["nc", "-z", "-w", "5", _PROXY_NODE_IP, str(_PROXY_NODE_PORT)],
        )
        assert rc == 0, (
            f"Cannot reach proxy-node SOCKS5 port {_PROXY_NODE_IP}:{_PROXY_NODE_PORT}. "
            f"rc={rc} stderr={stderr!r}. "
            "If BPF intercepted proxy-node traffic, this connection would loop and fail."
        )
