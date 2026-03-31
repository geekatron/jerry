# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""BDD tests for connect4.bpf.c modifications -- Envoy redirect + SO_MARK.

TASK-023-171 RED phase: These tests MUST fail before modifications.
GREEN phase: Modify connect4.bpf.c to make them pass.

Modifications under test:
    - Redirect target changed from bridge:12345 to Envoy:15001
    - SO_MARK=100 check added to skip Envoy's own upstream connections
    - bypass_ips map removed (no more mutable allow-list)
    - Loopback bypass preserved (127.0.0.0/8)
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

_PROJECT_ROOT = Path(__file__).resolve().parents[5]
_EBPF_POC_DIR = _PROJECT_ROOT / "src/proxy_infra/ebpf_poc"
_CONNECT4_SRC = _EBPF_POC_DIR / "connect4.bpf.c"
_BPF_BUILDER_DOCKERFILE = (
    _PROJECT_ROOT / "src/proxy_infra/infrastructure/bpf/Dockerfile.bpf-builder"
)
_BUILDER_IMAGE = "jerry-bpf-builder-test"


def _docker_available() -> bool:
    """Check if Docker is available and running.

    Returns:
        True if ``docker info`` exits 0 within 10 seconds.

    Raises:
        No exceptions raised; all errors return False.
    """
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


_requires_docker = pytest.mark.skipif(
    not _docker_available(),
    reason="Docker not available",
)


@pytest.fixture(scope="module")
def bpf_builder_image() -> str:
    """Build the BPF builder Docker image and return the image tag.

    Builds once per test module. Requires Docker.

    Returns:
        Docker image tag string for the built BPF builder image.

    Raises:
        pytest.Failed: If Docker build exits non-zero.
    """
    result = subprocess.run(
        [
            "docker", "build",
            "-f", str(_BPF_BUILDER_DOCKERFILE),
            "-t", _BUILDER_IMAGE,
            str(_EBPF_POC_DIR),
        ],
        capture_output=True,
        text=True,
        timeout=300,
    )
    if result.returncode != 0:
        pytest.fail(
            f"Docker build failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
        )
    return _BUILDER_IMAGE


@pytest.mark.unit
class TestConnect4EnvoyRedirect:
    """Tests for connect4.bpf.c modifications (TASK-023-171)."""

    @_requires_docker
    def test_connect4_redirects_to_envoy_port(
        self, bpf_builder_image: str
    ) -> None:
        """connect4 source uses ENVOY_PORT (15001), not BRIDGE_PORT (12345)."""
        source = _CONNECT4_SRC.read_text()
        assert "ENVOY_PORT" in source or "15001" in source, (
            "connect4.bpf.c does not reference ENVOY_PORT or 15001"
        )
        assert "BRIDGE_PORT" not in source, (
            "connect4.bpf.c still references BRIDGE_PORT (should redirect to Envoy)"
        )
        assert "12345" not in source, (
            "connect4.bpf.c still contains bridge port 12345"
        )

    @_requires_docker
    def test_connect4_skips_marked_connections(
        self, bpf_builder_image: str
    ) -> None:
        """connect4 source checks SO_MARK for Envoy bypass."""
        source = _CONNECT4_SRC.read_text()
        assert "ENVOY_MARK" in source or "SO_MARK" in source, (
            "connect4.bpf.c does not check SO_MARK for Envoy upstream bypass"
        )
        assert "bpf_getsockopt" in source, (
            "connect4.bpf.c does not call bpf_getsockopt to read SO_MARK"
        )

    def test_connect4_no_bypass_ips_map(self) -> None:
        """grep bypass_ips connect4.bpf.c returns no matches."""
        source = _CONNECT4_SRC.read_text()
        assert "bypass_ips" not in source, (
            "connect4.bpf.c still contains bypass_ips map "
            "(must be removed per Option C architecture)"
        )

    @_requires_docker
    def test_connect4_loopback_still_bypassed(
        self, bpf_builder_image: str
    ) -> None:
        """connect4 source still contains loopback bypass check."""
        source = _CONNECT4_SRC.read_text()
        assert "LOOPBACK" in source or "0x7f000000" in source or "127" in source, (
            "connect4.bpf.c loopback bypass check was removed "
            "(must be preserved)"
        )
        assert "LOOPBACK_PREFIX" in source or "LOOPBACK_MASK" in source, (
            "connect4.bpf.c loopback constants missing"
        )
