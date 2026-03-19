# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""E2E tests proving Zone 2 and Zone 3 traffic flows through Envoy proxy.

TASK-050: Every zone that touches the network must prove traffic routes
through Envoy and is subject to deny-by-default enforcement.

These tests make REAL HTTP requests from inside containers, through the
Envoy proxy, and verify allow/deny behavior + access log entries.

No mocks. No fakes. Real containers. Real Envoy. Real network calls.
"""

from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path

import pytest

_PROJECT_ROOT = Path(__file__).resolve().parents[3]

_RECON_COMPOSE = str(_PROJECT_ROOT / "skills/rainbow-recon/tests/docker/docker-compose.yml")
_EXPLOIT_COMPOSE = str(_PROJECT_ROOT / "skills/rainbow-exploit/tests/docker/docker-compose.yml")
_CLOUD_COMPOSE = str(_PROJECT_ROOT / "skills/rainbow-cloud/tests/docker/docker-compose.yml")


def _compose_exec(
    compose_file: str,
    service: str,
    cmd: list[str],
    *,
    timeout: int = 30,
) -> tuple[int, str, str]:
    """Execute a command inside a running compose service."""
    result = subprocess.run(
        ["docker", "compose", "-f", compose_file, "exec", "-T", service, *cmd],
        capture_output=True,
        text=True,
        cwd=str(_PROJECT_ROOT),
        timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr


def _compose_exec_with_env(
    compose_file: str,
    service: str,
    env: dict[str, str],
    cmd: list[str],
    *,
    timeout: int = 30,
) -> tuple[int, str, str]:
    """Execute a command with injected env vars."""
    env_flags: list[str] = []
    for k, v in env.items():
        env_flags.extend(["-e", f"{k}={v}"])
    result = subprocess.run(
        [
            "docker",
            "compose",
            "-f",
            compose_file,
            "exec",
            "-T",
            *env_flags,
            service,
            *cmd,
        ],
        capture_output=True,
        text=True,
        cwd=str(_PROJECT_ROOT),
        timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr


def _get_envoy_logs(compose_file: str, service: str) -> list[dict]:
    """Read JSON access log entries from an Envoy container via docker logs."""
    result = subprocess.run(
        ["docker", "compose", "-f", compose_file, "logs", "--no-log-prefix", service],
        capture_output=True,
        text=True,
        cwd=str(_PROJECT_ROOT),
        timeout=10,
    )
    entries = []
    for line in result.stdout.strip().split("\n"):
        line = line.strip()
        if line.startswith("{"):
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


# ---------------------------------------------------------------------------
# Zone 2 Recon: recon-pipeline through envoy-z2
# ---------------------------------------------------------------------------


class TestZone2ReconEnvoyTraffic:
    """Prove Zone 2 recon traffic flows through envoy-z2.

    The recon-pipeline container has wget and httpx but no curl.
    Uses wget for HTTP proxy testing (wget respects http_proxy env var).
    """

    @pytest.mark.e2e
    def test_zone2_deny_all_blocks_http(self, recon_cluster: str) -> None:
        """Zone 2 proxy denies all HTTP traffic (no engagement scope)."""
        rc, stdout, stderr = _compose_exec_with_env(
            _RECON_COMPOSE,
            "recon-pipeline",
            {"http_proxy": "http://envoy-z2:3128"},
            ["wget", "-q", "-O-", "--timeout=10", "http://httpbin.org/get"],
        )
        assert rc != 0, f"Zone 2 proxy allowed HTTP traffic! stdout={stdout}"
        assert "403" in stderr, f"Expected 403 in stderr. Got: {stderr}"

    @pytest.mark.e2e
    def test_zone2_deny_all_blocks_httpx(self, recon_cluster: str) -> None:
        """Zone 2 proxy denies httpx traffic (the actual recon tool)."""
        rc, stdout, stderr = _compose_exec_with_env(
            _RECON_COMPOSE,
            "recon-pipeline",
            {"HTTP_PROXY": "http://envoy-z2:3128", "HTTPS_PROXY": "http://envoy-z2:3128"},
            ["httpx", "-silent", "-status-code", "-no-color", "-u", "http://example.com"],
        )
        # httpx produces no output when the proxy blocks the request
        assert stdout.strip() == "", f"httpx reached a host through Zone 2 proxy! stdout={stdout}"

    @pytest.mark.e2e
    def test_zone2_structural_isolation(self, recon_cluster: str) -> None:
        """Zone 2 container cannot reach internet directly (internal:true)."""
        rc, stdout, stderr = _compose_exec_with_env(
            _RECON_COMPOSE,
            "recon-pipeline",
            {"http_proxy": "", "HTTP_PROXY": ""},
            ["wget", "-q", "-O-", "--timeout=5", "http://httpbin.org/get"],
        )
        assert rc != 0, "Recon container reached internet directly!"
        assert "bad address" in stderr.lower() or "name resolution" in stderr.lower(), (
            f"Expected DNS failure. Got: {stderr}"
        )

    @pytest.mark.e2e
    def test_zone2_access_log_has_entries(self, recon_cluster: str) -> None:
        """Envoy-z2 access logs contain zone2-active entries."""
        # Make a request to generate a log entry
        _compose_exec_with_env(
            _RECON_COMPOSE,
            "recon-pipeline",
            {"http_proxy": "http://envoy-z2:3128"},
            ["wget", "-q", "-O-", "--timeout=5", "http://test-log-entry.example.com"],
        )
        time.sleep(2)
        entries = _get_envoy_logs(_RECON_COMPOSE, "envoy-z2")
        zone2_entries = [e for e in entries if e.get("zone") == "zone2-active"]
        assert len(zone2_entries) >= 1, "No zone2-active entries in Envoy access logs"


# ---------------------------------------------------------------------------
# Zone 2 Cloud: cloud-auditor through envoy-z2
# ---------------------------------------------------------------------------


class TestZone2CloudEnvoyTraffic:
    """Prove Zone 2 cloud traffic flows through envoy-z2.

    The cloud-auditor container has curl and python3.
    """

    @pytest.mark.e2e
    def test_cloud_deny_all_blocks_http(self, cloud_cluster: str) -> None:
        """Cloud proxy denies all HTTP traffic (no engagement scope)."""
        rc, stdout, stderr = _compose_exec(
            _CLOUD_COMPOSE,
            "cloud-auditor",
            [
                "curl",
                "-s",
                "--connect-timeout",
                "10",
                "--proxy",
                "http://envoy-z2:3128",
                "-o",
                "/dev/null",
                "-w",
                "%{http_code}",
                "http://example.com",
            ],
        )
        assert stdout.strip() == "403", f"Expected 403, got: {stdout.strip()}"

    @pytest.mark.e2e
    def test_cloud_structural_isolation(self, cloud_cluster: str) -> None:
        """Cloud container cannot reach internet directly (internal:true)."""
        rc, stdout, stderr = _compose_exec(
            _CLOUD_COMPOSE,
            "cloud-auditor",
            ["curl", "-sf", "--connect-timeout", "5", "--noproxy", "*", "http://example.com"],
        )
        assert rc != 0, "Cloud container reached internet directly!"


# ---------------------------------------------------------------------------
# Zone 3 Exploit: exploit-ops through envoy-z3
# ---------------------------------------------------------------------------


class TestZone3ExploitEnvoyTraffic:
    """Prove Zone 3 exploit traffic flows through envoy-z3.

    The exploit-ops container has python3 (no curl, no wget).
    Uses urllib for HTTP proxy testing.
    """

    @pytest.mark.e2e
    def test_zone3_deny_all_blocks_http(self, exploit_cluster: str) -> None:
        """Zone 3 proxy denies all HTTP traffic (no engagement scope)."""
        rc, stdout, stderr = _compose_exec(
            _EXPLOIT_COMPOSE,
            "exploit-ops",
            [
                "python3",
                "-c",
                "import urllib.request,os;"
                "os.environ['http_proxy']='http://envoy-z3:3128';"
                "r=urllib.request.urlopen('http://example.com',timeout=10);"
                "print(f'HTTP {r.status}')",
            ],
        )
        # urllib raises HTTPError on 403, which causes exit != 0
        assert rc != 0 or "403" in stdout + stderr, (
            f"Zone 3 allowed HTTP! rc={rc} stdout={stdout} stderr={stderr}"
        )

    @pytest.mark.e2e
    def test_zone3_structural_isolation(self, exploit_cluster: str) -> None:
        """Exploit container cannot reach internet — proxy or topology blocks it.

        The compose file bakes HTTP_PROXY into the container env. Even without
        explicitly setting the proxy, urllib reads it and routes through Envoy
        which returns 403. On top of that, internal:true has no external route.
        Either way the request fails — that's the proof.
        """
        rc, stdout, stderr = _compose_exec(
            _EXPLOIT_COMPOSE,
            "exploit-ops",
            [
                "python3",
                "-c",
                "import urllib.request;urllib.request.urlopen('http://httpbin.org/get',timeout=5)",
            ],
        )
        assert rc != 0, "Exploit container reached internet!"
        # Accept either DNS failure (no route) or 403 (proxy deny) — both prove isolation
        combined = (stdout + stderr).lower()
        assert "403" in combined or "name resolution" in combined or "errno" in combined, (
            f"Expected 403 or DNS failure. Got: {stderr}"
        )

    @pytest.mark.e2e
    def test_zone3_access_log_has_entries(self, exploit_cluster: str) -> None:
        """Envoy-z3 access logs contain zone3-exploit entries with user_agent."""
        _compose_exec(
            _EXPLOIT_COMPOSE,
            "exploit-ops",
            [
                "python3",
                "-c",
                "import urllib.request,os;"
                "os.environ['http_proxy']='http://envoy-z3:3128';"
                "try: urllib.request.urlopen('http://log-test.example.com',timeout=5)\n"
                "except: pass",
            ],
        )
        time.sleep(2)
        entries = _get_envoy_logs(_EXPLOIT_COMPOSE, "envoy-z3")
        zone3_entries = [e for e in entries if e.get("zone") == "zone3-exploit"]
        assert len(zone3_entries) >= 1, "No zone3-exploit entries in Envoy access logs"
        # Zone 3 logs must include user_agent (forensic requirement)
        has_user_agent = any("user_agent" in e for e in zone3_entries)
        assert has_user_agent, "Zone 3 log entries missing user_agent field"
