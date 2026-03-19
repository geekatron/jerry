# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""Unit tests for T13-021/T13-022 proxy wiring.

Tests the _build_proxy_env helper and ContainerExecutor proxy_env injection.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from src.interface.cli.tool_exec_commands import _build_proxy_env
from src.tool_exec.infrastructure.adapters.container_executor import ContainerExecutor


class TestBuildProxyEnv:
    """Test the _build_proxy_env helper function."""

    def _resolution(self, service: str = "scanner", zone: str = "1") -> SimpleNamespace:
        """Create a mock resolution object."""
        return SimpleNamespace(container_service=service, zone=zone)

    def test_zone1_offline_returns_none(self) -> None:
        """Zone 1 offline services get no proxy env."""
        for service in ("scanner", "detection", "compliance", "forensics", "intel"):
            result = _build_proxy_env("1", self._resolution(service=service))
            assert result is None, f"{service} should have no proxy"

    def test_zone1_update_returns_z1_proxy(self) -> None:
        """Zone 1 update services get envoy-z1-update proxy."""
        result = _build_proxy_env("1", self._resolution(service="scanner-net"))
        assert result is not None
        assert result["HTTP_PROXY"] == "http://envoy-z1-update:3128"
        assert result["HTTPS_PROXY"] == "http://envoy-z1-update:3128"
        assert "localhost" in result["NO_PROXY"]

    def test_zone1_verifier_returns_z1_proxy(self) -> None:
        """Zone 1 verifier gets envoy-z1-update proxy (needs cosign/snyk access)."""
        result = _build_proxy_env("1", self._resolution(service="verifier"))
        assert result is not None
        assert "envoy-z1-update" in result["HTTP_PROXY"]

    def test_zone1_compliance_net_returns_z1_proxy(self) -> None:
        """Zone 1 compliance-net gets proxy (trivy DB downloads)."""
        result = _build_proxy_env("1", self._resolution(service="compliance-net"))
        assert result is not None
        assert "envoy-z1-update" in result["HTTP_PROXY"]

    def test_zone2_returns_z2_proxy(self) -> None:
        """Zone 2 services get envoy-z2 proxy."""
        result = _build_proxy_env("2", self._resolution(service="recon-pipeline"))
        assert result is not None
        assert result["HTTP_PROXY"] == "http://envoy-z2:3128"
        assert result["HTTPS_PROXY"] == "http://envoy-z2:3128"

    def test_zone3_returns_z3_proxy(self) -> None:
        """Zone 3 services get envoy-z3 proxy."""
        result = _build_proxy_env("3", self._resolution(service="exploit-ops"))
        assert result is not None
        assert result["HTTP_PROXY"] == "http://envoy-z3:3128"

    def test_zone3_msf_has_postgres_in_noproxy(self) -> None:
        """Metasploit needs postgres in NO_PROXY (separate internal network)."""
        result = _build_proxy_env("3", self._resolution(service="exploit-msf"))
        assert result is not None
        assert "postgres" in result["NO_PROXY"]

    def test_zone3_non_msf_no_postgres_in_noproxy(self) -> None:
        """Non-MSF Zone 3 services don't need postgres in NO_PROXY."""
        result = _build_proxy_env("3", self._resolution(service="exploit-ops"))
        assert result is not None
        assert "postgres" not in result["NO_PROXY"]

    def test_none_zone_returns_none(self) -> None:
        """No zone = no proxy env."""
        result = _build_proxy_env(None, self._resolution())
        assert result is None

    def test_unknown_zone_returns_none(self) -> None:
        """Unknown zone returns None (no matching proxy)."""
        result = _build_proxy_env("99", self._resolution(service="unknown"))
        assert result is None


class TestContainerExecutorProxyEnv:
    """Test that ContainerExecutor._build_command injects -e flags."""

    @pytest.fixture()
    def executor(self) -> ContainerExecutor:
        """Create executor with a mock credential filter."""
        mock_filter = type(
            "MockFilter",
            (),
            {
                "filter_output": lambda self, text, **kw: SimpleNamespace(
                    filtered_output=text, detected=False, match=None
                )
            },
        )()
        return ContainerExecutor(credential_filter=mock_filter)

    def test_no_proxy_env_no_e_flags(self, executor: ContainerExecutor) -> None:
        """Without proxy_env, no -e flags in command."""
        cmd = executor._build_command(
            tool_command="syft",
            tool_args=["version"],
            service="scanner",
            compose_file="/path/compose.yml",
            exec_flags=["-T"],
            proxy_env=None,
        )
        assert "-e" not in cmd

    def test_proxy_env_injects_e_flags(self, executor: ContainerExecutor) -> None:
        """proxy_env adds -e KEY=VALUE flags before the service name."""
        cmd = executor._build_command(
            tool_command="grype",
            tool_args=["version"],
            service="scanner-net",
            compose_file="/path/compose.yml",
            exec_flags=["-T"],
            proxy_env={
                "HTTP_PROXY": "http://envoy-z1-update:3128",
                "HTTPS_PROXY": "http://envoy-z1-update:3128",
                "NO_PROXY": "localhost,127.0.0.1",
            },
        )
        # -e flags must appear after exec_flags but before service name
        e_indices = [i for i, v in enumerate(cmd) if v == "-e"]
        service_idx = cmd.index("scanner-net")
        for idx in e_indices:
            assert idx < service_idx, f"-e at {idx} is after service at {service_idx}"

        # Verify all 3 proxy vars are present
        assert "-e" in cmd
        e_values = [cmd[i + 1] for i in e_indices]
        assert any("HTTP_PROXY=" in v for v in e_values)
        assert any("HTTPS_PROXY=" in v for v in e_values)
        assert any("NO_PROXY=" in v for v in e_values)

    def test_proxy_env_sorted_deterministic(self, executor: ContainerExecutor) -> None:
        """Proxy env vars are sorted for deterministic command output."""
        cmd = executor._build_command(
            tool_command="nuclei",
            tool_args=[],
            service="recon-pipeline",
            compose_file=None,
            exec_flags=["-T"],
            proxy_env={
                "HTTPS_PROXY": "http://envoy-z2:3128",
                "HTTP_PROXY": "http://envoy-z2:3128",
                "NO_PROXY": "localhost",
            },
        )
        e_indices = [i for i, v in enumerate(cmd) if v == "-e"]
        e_values = [cmd[i + 1] for i in e_indices]
        # Sorted alphabetically: HTTPS_PROXY, HTTP_PROXY, NO_PROXY
        assert e_values[0].startswith("HTTPS_PROXY=")
        assert e_values[1].startswith("HTTP_PROXY=")
        assert e_values[2].startswith("NO_PROXY=")
