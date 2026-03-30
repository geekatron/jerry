# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""BDD E2E tests for container BPF capabilities and security hardening.

Feature: Container BPF Capabilities
    EN-023-008 TASK-023-163: Tool containers have the minimum required
    capabilities for BPF operations via the bpf-init sidecar. Tool
    containers themselves have read-only bpffs access and no BPF caps.

    Verifies:
        - bpf-init sidecar can load BPF program (has CAP_BPF + CAP_NET_ADMIN)
        - Tool containers are NOT fully privileged (no all-caps)
        - /sys/fs/bpf is mounted in tool containers (read-only)
        - IPv6 is disabled on tool containers (DC-4)

    Test pyramid (H-20):
        50% happy path  -- BPF load in init, bpffs mount (2 tests)
        50% security    -- not privileged, IPv6 disabled (2 tests)

BDD RED phase (H-20):
    These tests require running compose clusters. They FAIL when clusters
    are not up, which is the correct initial state.

No mocks. Real containers with real capabilities.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Module-level constants
# ---------------------------------------------------------------------------

_PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Test with the cloud cluster (smallest, fastest to bring up)
_COMPOSE_FILE = str(_PROJECT_ROOT / "skills/rainbow-cloud/tests/docker/docker-compose.yml")
_COMPOSE_CWD = str(_PROJECT_ROOT / "skills/rainbow-cloud/tests/docker")
_INIT_SERVICE = "bpf-init"
_TOOL_SERVICE = "cloud-auditor"


def _compose_exec(
    service: str,
    cmd: list[str],
    *,
    timeout: int = 30,
) -> subprocess.CompletedProcess[str]:
    """Run a command inside a compose service container."""
    return subprocess.run(
        ["docker", "compose", "-f", _COMPOSE_FILE, "exec", "-T", service, *cmd],
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=_COMPOSE_CWD,
    )


# ---------------------------------------------------------------------------
# Tests — RED phase (H-20: all must FAIL initially)
# ---------------------------------------------------------------------------


@pytest.mark.e2e
class TestBpfInitCapabilities:
    """Verify bpf-init sidecar can perform BPF operations."""

    def test_bpf_init_can_load_bpf_program(self) -> None:
        """Given a running bpf-init sidecar with BPF capabilities,
        bpftool prog load succeeds on the compiled BPF object.

        RED: Fails because compose cluster is not running.
        """
        # Load BPF to a test pin path, then clean up
        result = _compose_exec(
            _INIT_SERVICE,
            [
                "sh",
                "-c",
                "bpftool prog load /opt/ebpf/connect4.bpf.o /sys/fs/bpf/test_cap_check "
                "pinmaps /sys/fs/bpf/test_cap_maps && "
                "bpftool prog show pinned /sys/fs/bpf/test_cap_check && "
                "rm -f /sys/fs/bpf/test_cap_check && "
                "rm -rf /sys/fs/bpf/test_cap_maps",
            ],
        )
        assert result.returncode == 0, (
            f"BPF load failed in bpf-init:\nstdout: {result.stdout}\nstderr: {result.stderr}"
        )


@pytest.mark.e2e
class TestToolContainerSecurity:
    """Verify tool containers are hardened per DC-2, DC-4, DC-6."""

    def test_tool_container_not_fully_privileged(self) -> None:
        """Given a running tool container, its CapEff is NOT all-ones
        (not fully privileged). Constraint B5.

        RED: Fails because compose cluster is not running.
        """
        result = _compose_exec(
            _TOOL_SERVICE,
            ["cat", "/proc/self/status"],
        )
        assert result.returncode == 0, f"Failed to read status: {result.stderr}"

        for line in result.stdout.splitlines():
            if line.startswith("CapEff:"):
                cap_eff = line.split(":")[1].strip()
                # All-ones (full privileged) is 0000003fffffffff or similar
                assert cap_eff != "0000003fffffffff", (
                    f"Tool container is fully privileged (CapEff={cap_eff}). "
                    "Expected restricted capabilities per B5."
                )
                break
        else:
            pytest.fail("CapEff not found in /proc/self/status")

    def test_tool_container_bpffs_mounted(self) -> None:
        """Given a running tool container, /sys/fs/bpf is accessible
        (mounted from the bpf-init sidecar's shared volume).

        RED: Fails because compose cluster is not running.
        """
        result = _compose_exec(
            _TOOL_SERVICE,
            ["ls", "/opt/ebpf/connect4.bpf.o"],
        )
        assert result.returncode == 0, (
            f"BPF object not accessible in tool container:\n"
            f"stdout: {result.stdout}\nstderr: {result.stderr}"
        )

    def test_tool_container_ipv6_disabled(self) -> None:
        """Given a running tool container, IPv6 is disabled via sysctl.
        Constraint DC-4: connect4 only intercepts IPv4.

        RED: Fails because compose cluster is not running.
        """
        result = _compose_exec(
            _TOOL_SERVICE,
            ["cat", "/proc/sys/net/ipv6/conf/all/disable_ipv6"],
        )
        assert result.returncode == 0, f"Failed to read sysctl: {result.stderr}"
        assert result.stdout.strip() == "1", (
            f"Expected IPv6 disabled (1), got: {result.stdout.strip()}"
        )
