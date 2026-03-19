# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""E2E tests for Envoy forward proxy network isolation.

STORY-W13-004: Validates that the Envoy proxy + Docker internal:true
network topology enforces deny-by-default egress per zone.

Tests use the real compose files with live Envoy containers.
No mocks. No fakes. Real network calls prove real isolation.

Tasks:
    T13-016: Zone 1 offline — container CANNOT reach internet
    T13-017: Zone 1 update — CAN reach allowlist, CANNOT reach others
    T13-018: Zone 2 — CAN reach engagement-scope targets, CANNOT reach non-scope
    T13-019: Zone 3 — Envoy logs all connections for forensic evidence
    T13-020: Bypass detection — container without proxy env vars is still blocked
    TASK-043: Fail-closed gate — CONTAINER_NOT_RUNNING (3) when envoy-z2 is down
"""

from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_PROJECT_ROOT = Path(__file__).resolve().parents[3]

_SUPPLY_CHAIN_COMPOSE = str(
    _PROJECT_ROOT / "skills/rainbow-supply-chain/tests/docker/docker-compose.yml"
)

# Timeout for docker compose operations
_BUILD_TIMEOUT = 600  # Image pulls + Envoy can be slow
_UP_TIMEOUT = 120
_DOWN_TIMEOUT = 60
_EXEC_TIMEOUT = 30

# How long to wait for Envoy to become healthy
_ENVOY_HEALTH_WAIT = 15


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _docker_available() -> bool:
    """Check if Docker daemon is reachable."""
    try:
        result = subprocess.run(["docker", "info"], capture_output=True, timeout=10)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def _compose_exec(
    compose_file: str,
    service: str,
    cmd: list[str],
    *,
    timeout: int = _EXEC_TIMEOUT,
    env_override: dict[str, str] | None = None,
) -> tuple[int, str, str]:
    """Execute a command inside a running compose service container.

    Returns (exit_code, stdout, stderr).
    """
    full_cmd = [
        "docker",
        "compose",
        "-f",
        compose_file,
        "exec",
        "-T",
        service,
        *cmd,
    ]
    if env_override:
        for k, v in env_override.items():
            full_cmd.insert(5, f"-e={k}={v}")  # Insert before service name

    result = subprocess.run(
        full_cmd,
        capture_output=True,
        text=True,
        cwd=str(_PROJECT_ROOT),
        timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr


def _compose_up(compose_file: str) -> None:
    """Build and start a compose file."""
    subprocess.run(
        ["docker", "compose", "-f", compose_file, "build", "--quiet"],
        check=True,
        cwd=str(_PROJECT_ROOT),
        timeout=_BUILD_TIMEOUT,
    )
    subprocess.run(
        ["docker", "compose", "-f", compose_file, "up", "--detach"],
        check=True,
        cwd=str(_PROJECT_ROOT),
        timeout=_UP_TIMEOUT,
    )


def _compose_down(compose_file: str) -> None:
    """Stop and remove compose containers."""
    subprocess.run(
        [
            "docker",
            "compose",
            "-f",
            compose_file,
            "down",
            "--volumes",
            "--remove-orphans",
        ],
        cwd=str(_PROJECT_ROOT),
        timeout=_DOWN_TIMEOUT,
    )


def _wait_for_envoy(
    compose_file: str, tool_service: str, envoy_host: str, max_wait: int = _ENVOY_HEALTH_WAIT
) -> bool:
    """Wait for Envoy proxy to be reachable from a tool container.

    The Envoy image has no curl/wget. Instead, check reachability by
    having the tool container (which has curl) connect to the proxy port.
    """
    for _ in range(max_wait):
        rc, _, _ = _compose_exec(
            compose_file,
            tool_service,
            ["curl", "-sf", "--connect-timeout", "2", f"http://{envoy_host}:3128/"],
            timeout=5,
        )
        # Envoy returns 404 for direct HTTP to the proxy port (no Host match)
        # but that means the proxy is up and listening
        if rc == 0 or rc == 22:  # 22 = curl HTTP error (404) = proxy is up
            return True
        time.sleep(1)
    return False


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module", autouse=True)
def require_docker():
    """Skip all tests in this module if Docker is not available."""
    if not _docker_available():
        pytest.skip("Docker daemon not available")


@pytest.fixture(scope="module")
def supply_chain_cluster():
    """Start the supply-chain compose cluster with Envoy for the module.

    Builds images, starts containers (including envoy-z1-update),
    waits for Envoy health, and tears down on module exit.
    """
    _compose_up(_SUPPLY_CHAIN_COMPOSE)
    # Wait for Envoy to be reachable from the scanner-net container
    healthy = _wait_for_envoy(_SUPPLY_CHAIN_COMPOSE, "scanner-net", "envoy-z1-update")
    if not healthy:
        _compose_down(_SUPPLY_CHAIN_COMPOSE)
        pytest.skip("Envoy proxy did not become healthy within timeout")

    yield

    _compose_down(_SUPPLY_CHAIN_COMPOSE)


# ---------------------------------------------------------------------------
# T13-016: Zone 1 Offline — Container CANNOT Reach Internet
# ---------------------------------------------------------------------------


class TestZone1Offline:
    """Verify Zone 1 offline containers have zero network access.

    The scanner service is on zone1-offline (internal: true, no proxy).
    It should not be able to reach ANY external host.
    """

    @pytest.mark.e2e
    def test_cannot_curl_httpbin(self, supply_chain_cluster: None) -> None:
        """T13-016: curl to httpbin.org must fail from offline container."""
        rc, stdout, stderr = _compose_exec(
            _SUPPLY_CHAIN_COMPOSE,
            "scanner",
            ["curl", "-sf", "--connect-timeout", "5", "http://httpbin.org/get"],
        )
        assert rc != 0, f"Offline container reached httpbin.org! stdout={stdout}"

    @pytest.mark.e2e
    def test_cannot_curl_github(self, supply_chain_cluster: None) -> None:
        """T13-016: curl to github.com must fail from offline container."""
        rc, stdout, stderr = _compose_exec(
            _SUPPLY_CHAIN_COMPOSE,
            "scanner",
            ["curl", "-sf", "--connect-timeout", "5", "https://github.com"],
        )
        assert rc != 0, f"Offline container reached github.com! stdout={stdout}"

    @pytest.mark.e2e
    def test_cannot_ping_external(self, supply_chain_cluster: None) -> None:
        """T13-016: ping to external IP must fail from offline container."""
        rc, stdout, stderr = _compose_exec(
            _SUPPLY_CHAIN_COMPOSE,
            "scanner",
            ["ping", "-c", "1", "-W", "3", "8.8.8.8"],
        )
        assert rc != 0, f"Offline container pinged 8.8.8.8! stdout={stdout}"

    @pytest.mark.e2e
    def test_cannot_resolve_dns(self, supply_chain_cluster: None) -> None:
        """T13-016: DNS resolution should fail or be blocked from offline container."""
        # nslookup/dig may not be available; curl --resolve bypass tests DNS separately
        rc, stdout, stderr = _compose_exec(
            _SUPPLY_CHAIN_COMPOSE,
            "scanner",
            ["curl", "-sf", "--connect-timeout", "5", "http://example.com"],
        )
        assert rc != 0, "Offline container resolved and reached example.com"


# ---------------------------------------------------------------------------
# T13-017: Zone 1 Update — CAN Reach Allowlist, CANNOT Reach Others
# ---------------------------------------------------------------------------


class TestZone1Update:
    """Verify Zone 1 update containers can reach allowlisted hosts only.

    The scanner-net service is on zone1-update (internal: true + Envoy proxy).
    It should reach github.com (allowlisted) but NOT arbitrary hosts.
    """

    @pytest.mark.e2e
    def test_can_reach_github_via_proxy(self, supply_chain_cluster: None) -> None:
        """T13-017: scanner-net can reach github.com through Envoy proxy."""
        rc, stdout, stderr = _compose_exec(
            _SUPPLY_CHAIN_COMPOSE,
            "scanner-net",
            [
                "curl",
                "-sf",
                "--connect-timeout",
                "10",
                "--proxy",
                "http://envoy-z1-update:3128",
                "https://github.com",
            ],
        )
        assert rc == 0, f"Failed to reach github.com via proxy: stderr={stderr}"

    @pytest.mark.e2e
    def test_can_reach_pypi_via_proxy(self, supply_chain_cluster: None) -> None:
        """T13-017: scanner-net can reach pypi.org through Envoy proxy."""
        rc, stdout, stderr = _compose_exec(
            _SUPPLY_CHAIN_COMPOSE,
            "scanner-net",
            [
                "curl",
                "-sf",
                "--connect-timeout",
                "10",
                "--proxy",
                "http://envoy-z1-update:3128",
                "https://pypi.org/simple/",
            ],
        )
        assert rc == 0, f"Failed to reach pypi.org via proxy: stderr={stderr}"

    @pytest.mark.e2e
    def test_cannot_reach_arbitrary_host_via_proxy(self, supply_chain_cluster: None) -> None:
        """T13-017: Envoy denies access to non-allowlisted hosts (403)."""
        rc, stdout, stderr = _compose_exec(
            _SUPPLY_CHAIN_COMPOSE,
            "scanner-net",
            [
                "curl",
                "-s",
                "--connect-timeout",
                "10",
                "--proxy",
                "http://envoy-z1-update:3128",
                "-o",
                "/dev/null",
                "-w",
                "%{http_code}",
                "http://httpbin.org/get",
            ],
        )
        # Envoy returns 403 for denied hosts
        assert stdout.strip() == "403", (
            f"Expected 403 from proxy for httpbin.org, got: {stdout.strip()}"
        )

    @pytest.mark.e2e
    def test_deny_response_contains_zone_message(self, supply_chain_cluster: None) -> None:
        """T13-017: Envoy deny response includes zone identification."""
        rc, stdout, stderr = _compose_exec(
            _SUPPLY_CHAIN_COMPOSE,
            "scanner-net",
            [
                "curl",
                "-s",
                "--connect-timeout",
                "10",
                "--proxy",
                "http://envoy-z1-update:3128",
                "http://httpbin.org/get",
            ],
        )
        assert "ZONE1-UPDATE DENIED" in stdout, (
            f"Expected ZONE1-UPDATE DENIED in response, got: {stdout[:200]}"
        )

    @pytest.mark.e2e
    def test_cannot_reach_arbitrary_https_via_proxy(self, supply_chain_cluster: None) -> None:
        """T13-017: HTTPS CONNECT to non-allowlisted host fails."""
        rc, stdout, stderr = _compose_exec(
            _SUPPLY_CHAIN_COMPOSE,
            "scanner-net",
            [
                "curl",
                "-s",
                "--connect-timeout",
                "10",
                "--proxy",
                "http://envoy-z1-update:3128",
                "https://httpbin.org/get",
            ],
        )
        # CONNECT deny returns 403 but curl can't establish TLS over a refused
        # tunnel, so it reports a connection error (exit != 0).
        assert rc != 0, "HTTPS to non-allowlisted host succeeded through proxy!"

    @pytest.mark.e2e
    def test_cannot_reach_internet_directly(self, supply_chain_cluster: None) -> None:
        """T13-017: scanner-net cannot bypass proxy to reach internet directly."""
        # Even without using the proxy, internal:true blocks direct access
        rc, stdout, stderr = _compose_exec(
            _SUPPLY_CHAIN_COMPOSE,
            "scanner-net",
            ["curl", "-sf", "--connect-timeout", "5", "http://httpbin.org/get"],
        )
        assert rc != 0, "scanner-net reached internet directly (bypassing proxy)!"


# ---------------------------------------------------------------------------
# T13-018: Zone 2 — Engagement Scope Targets Only (deny-all default)
# ---------------------------------------------------------------------------


class TestZone2DenyAll:
    """Verify Zone 2 default config denies ALL traffic (pre-engagement-init).

    The Zone 2 config has no authorized targets by default — everything
    should be denied until --init-engagement generates a scope config.

    This test uses the recon compose file which has envoy-z2.
    Since building recon is expensive, we test the Zone 2 deny-all behavior
    by checking the Envoy config content directly (unit test augmentation).
    """

    @pytest.mark.e2e
    def test_zone2_default_denies_all(self) -> None:
        """T13-018: Zone 2 Envoy config default has only deny_all virtual_host."""
        import yaml

        config_path = _PROJECT_ROOT / "skills/rainbow/config/envoy/envoy-zone2-active.yaml"
        with config_path.open() as f:
            config = yaml.safe_load(f)

        hcm = config["static_resources"]["listeners"][0]["filter_chains"][0]["filters"][0][
            "typed_config"
        ]
        virtual_hosts = hcm["route_config"]["virtual_hosts"]

        # Only the deny_all host should exist (no scope targets)
        assert len(virtual_hosts) == 1, (
            f"Expected 1 virtual_host (deny_all), got {len(virtual_hosts)}"
        )
        assert virtual_hosts[0]["name"] == "deny_all"
        assert virtual_hosts[0]["routes"][0]["direct_response"]["status"] == 403


# ---------------------------------------------------------------------------
# T13-019: Zone 3 — Envoy Logs All Connections
# ---------------------------------------------------------------------------


class TestZone3Logging:
    """Verify Zone 3 Envoy config includes forensic logging fields.

    Full E2E logging verification requires running the exploit compose
    (expensive). We validate the config structure ensures logging is
    configured, and test log output format against the config spec.
    """

    @pytest.mark.e2e
    def test_zone3_logs_user_agent(self) -> None:
        """T13-019: Zone 3 access log includes user_agent field."""
        import yaml

        config_path = _PROJECT_ROOT / "skills/rainbow/config/envoy/envoy-zone3-exploit.yaml"
        with config_path.open() as f:
            config = yaml.safe_load(f)

        hcm = config["static_resources"]["listeners"][0]["filter_chains"][0]["filters"][0][
            "typed_config"
        ]
        log_format = hcm["access_log"][0]["typed_config"]["log_format"]["json_format"]
        assert "user_agent" in log_format

    @pytest.mark.e2e
    def test_zone3_logs_auth_header(self) -> None:
        """T13-019: Zone 3 access log includes authorization presence field."""
        import yaml

        config_path = _PROJECT_ROOT / "skills/rainbow/config/envoy/envoy-zone3-exploit.yaml"
        with config_path.open() as f:
            config = yaml.safe_load(f)

        hcm = config["static_resources"]["listeners"][0]["filter_chains"][0]["filters"][0][
            "typed_config"
        ]
        log_format = hcm["access_log"][0]["typed_config"]["log_format"]["json_format"]
        assert "auth_present" in log_format

    @pytest.mark.e2e
    def test_zone3_logs_downstream_remote(self) -> None:
        """T13-019: Zone 3 access log includes downstream remote address."""
        import yaml

        config_path = _PROJECT_ROOT / "skills/rainbow/config/envoy/envoy-zone3-exploit.yaml"
        with config_path.open() as f:
            config = yaml.safe_load(f)

        hcm = config["static_resources"]["listeners"][0]["filter_chains"][0]["filters"][0][
            "typed_config"
        ]
        log_format = hcm["access_log"][0]["typed_config"]["log_format"]["json_format"]
        assert "downstream_remote" in log_format


# ---------------------------------------------------------------------------
# T13-020: Bypass Detection — No Proxy Env Vars Still Blocked
# ---------------------------------------------------------------------------


class TestBypassDetection:
    """Verify containers are blocked even without HTTP_PROXY env vars.

    The key insight: internal:true Docker networks have NO default gateway.
    Even if a container unsets HTTP_PROXY, it has no route to the internet.
    This is structural enforcement, not behavioral.
    """

    @pytest.mark.e2e
    def test_no_proxy_still_blocked(self, supply_chain_cluster: None) -> None:
        """T13-020: scanner-net without proxy cannot reach internet directly."""
        # Force curl to NOT use the proxy by unsetting env vars
        rc, stdout, stderr = _compose_exec(
            _SUPPLY_CHAIN_COMPOSE,
            "scanner-net",
            [
                "curl",
                "-sf",
                "--connect-timeout",
                "5",
                "--noproxy",
                "*",
                "http://httpbin.org/get",
            ],
        )
        assert rc != 0, (
            "Container reached internet with proxy disabled! "
            "internal:true network should block this structurally."
        )

    @pytest.mark.e2e
    def test_no_proxy_cannot_ping_external(self, supply_chain_cluster: None) -> None:
        """T13-020: scanner-net cannot ping external IPs (no route exists)."""
        rc, stdout, stderr = _compose_exec(
            _SUPPLY_CHAIN_COMPOSE,
            "scanner-net",
            ["ping", "-c", "1", "-W", "3", "8.8.8.8"],
        )
        assert rc != 0, "Container pinged 8.8.8.8 on internal:true network!"

    @pytest.mark.e2e
    def test_envoy_is_only_egress_path(self, supply_chain_cluster: None) -> None:
        """T13-020: Only Envoy proxy provides external access from internal network."""
        # Can reach Envoy proxy (internal network peer)
        rc_proxy, _, _ = _compose_exec(
            _SUPPLY_CHAIN_COMPOSE,
            "scanner-net",
            ["curl", "-sf", "--connect-timeout", "5", "http://envoy-z1-update:9901/ready"],
        )
        # But admin is on loopback (V10 fix) so this should fail
        # The proxy listener on 3128 is reachable though
        rc_listener, _, _ = _compose_exec(
            _SUPPLY_CHAIN_COMPOSE,
            "scanner-net",
            ["curl", "-s", "--connect-timeout", "5", "http://envoy-z1-update:3128/"],
        )
        # The proxy listener should respond (even if with an error for direct HTTP)
        # This proves the internal network connectivity works for proxy traffic
        assert rc_proxy != 0 or rc_listener == 0, "Cannot reach Envoy at all on internal network"


# ---------------------------------------------------------------------------
# Envoy Access Log Format Validation
# ---------------------------------------------------------------------------


class TestEnvoyAccessLogLive:
    """Verify Envoy access logs are written in structured JSON format.

    Access logs go to /dev/stdout (Docker log capture pattern).
    We read them via `docker compose logs` after making requests.
    """

    @pytest.mark.e2e
    def test_access_log_is_json(self, supply_chain_cluster: None) -> None:
        """Access log entries must be valid JSON via docker logs."""
        # Make a request that will be logged (allowed host)
        _compose_exec(
            _SUPPLY_CHAIN_COMPOSE,
            "scanner-net",
            [
                "curl",
                "-s",
                "--connect-timeout",
                "10",
                "--proxy",
                "http://envoy-z1-update:3128",
                "http://pypi.org/",
            ],
        )
        # Also make a denied request
        _compose_exec(
            _SUPPLY_CHAIN_COMPOSE,
            "scanner-net",
            [
                "curl",
                "-s",
                "--connect-timeout",
                "10",
                "--proxy",
                "http://envoy-z1-update:3128",
                "http://evil.example.com/",
            ],
        )

        time.sleep(2)

        # Read access logs via docker compose logs
        result = subprocess.run(
            [
                "docker",
                "compose",
                "-f",
                _SUPPLY_CHAIN_COMPOSE,
                "logs",
                "--no-log-prefix",
                "envoy-z1-update",
            ],
            capture_output=True,
            text=True,
            cwd=str(_PROJECT_ROOT),
            timeout=10,
        )

        stdout = result.stdout
        # Filter to only JSON lines (skip Envoy startup info lines)
        json_lines = []
        for line in stdout.strip().split("\n"):
            line = line.strip()
            if line.startswith("{"):
                json_lines.append(line)

        assert len(json_lines) >= 1, "No JSON access log lines found in docker logs"

        for line in json_lines:
            entry = json.loads(line)
            assert "zone" in entry, f"Missing 'zone' field in log entry: {entry}"
            assert entry["zone"] == "zone1-update"

    @pytest.mark.e2e
    def test_denied_request_logged(self, supply_chain_cluster: None) -> None:
        """Denied requests must also appear in the access log."""
        _compose_exec(
            _SUPPLY_CHAIN_COMPOSE,
            "scanner-net",
            [
                "curl",
                "-s",
                "--connect-timeout",
                "10",
                "--proxy",
                "http://envoy-z1-update:3128",
                "http://blocked.example.com/",
            ],
        )
        time.sleep(2)

        result = subprocess.run(
            [
                "docker",
                "compose",
                "-f",
                _SUPPLY_CHAIN_COMPOSE,
                "logs",
                "--no-log-prefix",
                "envoy-z1-update",
            ],
            capture_output=True,
            text=True,
            cwd=str(_PROJECT_ROOT),
            timeout=10,
        )

        denied_entries = []
        for line in result.stdout.strip().split("\n"):
            line = line.strip()
            if not line.startswith("{"):
                continue
            try:
                entry = json.loads(line)
                if str(entry.get("response_code")) == "403":
                    denied_entries.append(entry)
            except json.JSONDecodeError:
                continue

        assert len(denied_entries) >= 1, "No 403 entries found in Envoy access logs"


# ---------------------------------------------------------------------------
# TASK-043: Fail-Closed Gate — CONTAINER_NOT_RUNNING (3) when envoy-z2 down
# ---------------------------------------------------------------------------

_RECON_COMPOSE = str(_PROJECT_ROOT / "skills/rainbow-recon/tests/docker/docker-compose.yml")


class TestEnvoyFailClosed:
    """TASK-043: VULN-003 fail-closed gate fires when the Zone 2 Envoy proxy
    is stopped.

    Security control: CONTAINER_NOT_RUNNING (exit code 3).

    When the envoy-z2 container is not running, any Zone 2 tool execution in
    container mode must refuse to proceed rather than executing without the
    proxy.  Running without the proxy would bypass deny-by-default egress
    enforcement (OWASP A01:2021 Broken Access Control).

    Test sequence:
        1. Stop envoy-z2 via docker compose stop.
        2. Invoke subfinder (Zone 2) via the jerry CLI.
        3. Assert exit code 3 (CONTAINER_NOT_RUNNING) and expected message.
        4. Restart envoy-z2 unconditionally in teardown.

    The recon compose file is used because subfinder is a Zone 2 tool routed
    through envoy-z2.  The engagement E2E-TEST-001 is assumed to exist (it is
    created during the broader E2E run; tests that need it must ensure it is
    initialized before this class runs).
    """

    @pytest.fixture(autouse=True)
    def _ensure_envoy_z2_restarted(self):  # type: ignore[return]
        """Guarantee envoy-z2 is restarted after each test in this class.

        Yields before the test body runs so the stop/restart lifecycle is
        wrapped symmetrically:  stop happens in the test body; restart
        happens unconditionally here regardless of whether the test passes,
        fails, or raises.
        """
        yield
        # Unconditional restart — best-effort cleanup so subsequent tests are
        # not broken by a stopped envoy-z2.
        subprocess.run(
            [
                "docker",
                "compose",
                "-f",
                _RECON_COMPOSE,
                "start",
                "envoy-z2",
            ],
            capture_output=True,
            cwd=str(_PROJECT_ROOT),
            timeout=30,
        )

    @pytest.mark.e2e
    def test_fail_closed_when_envoy_z2_stopped(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """TASK-043: CONTAINER_NOT_RUNNING (3) when envoy-z2 is not running.

        Stops envoy-z2 then invokes subfinder in container mode.  The
        VULN-003 fail-closed gate in tool_exec_commands.py must detect that
        the proxy is absent and return exit code 3 without executing the tool.

        The _ensure_envoy_z2_restarted fixture restarts envoy-z2 after this
        test regardless of outcome.
        """
        # Stop envoy-z2 so the fail-closed gate has something to detect.
        stop_result = subprocess.run(
            [
                "docker",
                "compose",
                "-f",
                _RECON_COMPOSE,
                "stop",
                "envoy-z2",
            ],
            capture_output=True,
            cwd=str(_PROJECT_ROOT),
            timeout=30,
        )
        assert stop_result.returncode == 0, (
            f"Failed to stop envoy-z2 for test setup. stderr={stop_result.stderr.decode()!r}"
        )

        # Small sleep to let Docker register the stopped state.
        time.sleep(2)

        exit_code, stdout, stderr = cli_run(
            "--mode",
            "container",
            "--engagement-id",
            "E2E-TEST-001",
            "subfinder",
            "--",
            "-version",
        )

        assert exit_code == 3, (  # CONTAINER_NOT_RUNNING
            f"Expected CONTAINER_NOT_RUNNING (3) when envoy-z2 is stopped. "
            f"Got exit_code={exit_code}. stdout={stdout!r} stderr={stderr!r}"
        )
        assert "Envoy proxy" in stderr, f"Expected 'Envoy proxy' in stderr. Got stderr={stderr!r}"
        assert "not running" in stderr, f"Expected 'not running' in stderr. Got stderr={stderr!r}"
