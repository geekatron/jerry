# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""E2E tests for Zone 3 vulnerable target network isolation.

TASK-023-117: Verify that z3-targets network (internal: true) prevents
target containers from reaching the internet while still allowing Zone 3
exploit containers to reach them.

Design:
    - Uses docker compose exec to run commands inside containers
    - Negative tests: DNS and ping from targets to internet MUST fail
    - Positive test: exploit-ops can reach targets on z3-targets network
    - Both compose files are passed so exec resolves the correct project
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest


@pytest.mark.e2e
@pytest.mark.e2e_targets
class TestTargetNetworkIsolation:
    """Verify z3-targets network isolation prevents egress."""

    def test_dvwa_cannot_resolve_external_dns(
        self,
        project_root: Path,
        exploit_cluster: str,
        vulnerable_targets: str,
    ) -> None:
        """DVWA container cannot resolve external domain names.

        The z3-targets network has internal: true and no DNS server, so
        nslookup/dig to an external domain must fail.
        """
        result = subprocess.run(
            [
                "docker",
                "compose",
                "-f",
                exploit_cluster,
                "-f",
                vulnerable_targets,
                "exec",
                "-T",
                "dvwa",
                "sh",
                "-c",
                "nslookup example.com 2>&1 || true",
            ],
            capture_output=True,
            text=True,
            cwd=str(project_root),
            timeout=15,
        )
        # nslookup should fail (no DNS server on internal network)
        # Accept: non-zero exit OR output containing "can't resolve" / "SERVFAIL" / "timed out"
        output = (result.stdout + result.stderr).lower()
        assert result.returncode != 0 or any(
            indicator in output
            for indicator in ["can't resolve", "servfail", "timed out", "no servers", "nxdomain"]
        ), f"DVWA unexpectedly resolved external DNS. stdout: {result.stdout}"

    def test_dvwa_cannot_ping_external_ip(
        self,
        project_root: Path,
        exploit_cluster: str,
        vulnerable_targets: str,
    ) -> None:
        """DVWA container cannot reach public IP addresses.

        The z3-targets network has no default gateway, so ping to 8.8.8.8
        must fail with "network unreachable" or timeout.
        """
        result = subprocess.run(
            [
                "docker",
                "compose",
                "-f",
                exploit_cluster,
                "-f",
                vulnerable_targets,
                "exec",
                "-T",
                "dvwa",
                "ping",
                "-c1",
                "-W2",
                "8.8.8.8",
            ],
            capture_output=True,
            text=True,
            cwd=str(project_root),
            timeout=15,
        )
        assert result.returncode != 0, f"DVWA unexpectedly reached 8.8.8.8. stdout: {result.stdout}"

    def test_vuln_api_cannot_reach_internet(
        self,
        project_root: Path,
        exploit_cluster: str,
        vulnerable_targets: str,
    ) -> None:
        """Vulnerable API container cannot make outbound HTTP requests.

        Curl to an external URL must fail (no route, no DNS).
        """
        result = subprocess.run(
            [
                "docker",
                "compose",
                "-f",
                exploit_cluster,
                "-f",
                vulnerable_targets,
                "exec",
                "-T",
                "vuln-api",
                "python",
                "-c",
                "import urllib.request; urllib.request.urlopen('http://example.com', timeout=3)",
            ],
            capture_output=True,
            text=True,
            cwd=str(project_root),
            timeout=15,
        )
        assert result.returncode != 0, (
            f"Vulnerable API unexpectedly reached the internet. stdout: {result.stdout}"
        )

    def test_exploit_ops_can_reach_dvwa(
        self,
        project_root: Path,
        exploit_cluster: str,
        vulnerable_targets: str,
    ) -> None:
        """Zone 3 exploit-ops container CAN reach DVWA on z3-targets network.

        This is the positive connectivity test: exploit containers must be
        able to reach vulnerable targets for E2E exploit testing to work.
        """
        result = subprocess.run(
            [
                "docker",
                "compose",
                "-f",
                exploit_cluster,
                "-f",
                vulnerable_targets,
                "exec",
                "-T",
                "exploit-ops",
                "curl",
                "-sf",
                "--max-time",
                "5",
                "http://dvwa/",
            ],
            capture_output=True,
            text=True,
            cwd=str(project_root),
            timeout=15,
        )
        assert result.returncode == 0, f"exploit-ops cannot reach DVWA. stderr: {result.stderr}"

    def test_exploit_ops_can_reach_vuln_api(
        self,
        project_root: Path,
        exploit_cluster: str,
        vulnerable_targets: str,
    ) -> None:
        """Zone 3 exploit-ops container CAN reach vulnerable API health endpoint."""
        result = subprocess.run(
            [
                "docker",
                "compose",
                "-f",
                exploit_cluster,
                "-f",
                vulnerable_targets,
                "exec",
                "-T",
                "exploit-ops",
                "curl",
                "-sf",
                "--max-time",
                "5",
                "http://vuln-api:5000/health",
            ],
            capture_output=True,
            text=True,
            cwd=str(project_root),
            timeout=15,
        )
        assert result.returncode == 0, f"exploit-ops cannot reach vuln-api. stderr: {result.stderr}"
        assert '"status"' in result.stdout and '"ok"' in result.stdout
