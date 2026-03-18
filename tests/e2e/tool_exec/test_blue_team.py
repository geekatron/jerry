# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""TASK-038: Blue-team family E2E tests (yr, sigma, trivy, hayabusa, chainsaw).

Tests that blue-team tools resolve through the rainbow family and the
blue-team detection / compliance services.

All blue-team tools registered in tool-exec.yaml are Zone 1 (read-only
defensive analysis).  They do not require an engagement ID.

Services:
    detection  -- yr, sigma, hayabusa, chainsaw
    compliance -- trivy

Execution strategy:
- trivy may be available on the host PATH via Homebrew (macOS developers).
- yr, sigma, hayabusa, chainsaw are typically only in the detection container.
- Tool resolution tests are always executed (no PATH requirement).
- Local execution tests are skipped when the binary is absent from PATH.

Zone 1 policy (OWASP A05:2021):
- No engagement ID required.
- No per-operation approval gate.

Exit code reference:
    0  SUCCESS
    1  UNKNOWN_TOOL
    2  TOOL_ERROR
    5  ENGAGEMENT_NOT_INIT  (must NOT fire for Zone 1 tools)

References:
    - TASK-038: Blue-team E2E tests
    - ADR-PROJ023-001: UC-001 Zone 1 path
    - tool-exec.yaml: yr, sigma, hayabusa, chainsaw (detection), trivy (compliance)
"""

from __future__ import annotations

import shutil

import pytest

pytestmark = pytest.mark.e2e


class TestBlueTeamToolRegistry:
    """yr, sigma, trivy, hayabusa, and chainsaw appear in the tool registry."""

    def test_yr_appears_in_list_tools(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """--list-tools output includes 'yr' (YARA-X CLI)."""
        exit_code, stdout, stderr = cli_run("--list-tools")
        assert exit_code == 0, f"--list-tools failed. stderr={stderr!r}"
        assert "yr" in stdout, f"Expected 'yr' in --list-tools output. stdout={stdout!r}"

    def test_sigma_appears_in_list_tools(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """--list-tools output includes 'sigma'."""
        exit_code, stdout, stderr = cli_run("--list-tools")
        assert exit_code == 0
        assert "sigma" in stdout, f"Expected 'sigma' in --list-tools output. stdout={stdout!r}"

    def test_trivy_appears_in_list_tools(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """--list-tools output includes 'trivy'."""
        exit_code, stdout, stderr = cli_run("--list-tools")
        assert exit_code == 0
        assert "trivy" in stdout, f"Expected 'trivy' in --list-tools output. stdout={stdout!r}"

    def test_hayabusa_appears_in_list_tools(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """--list-tools output includes 'hayabusa'."""
        exit_code, stdout, stderr = cli_run("--list-tools")
        assert exit_code == 0
        assert "hayabusa" in stdout, (
            f"Expected 'hayabusa' in --list-tools output. stdout={stdout!r}"
        )

    def test_chainsaw_appears_in_list_tools(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """--list-tools output includes 'chainsaw'."""
        exit_code, stdout, stderr = cli_run("--list-tools")
        assert exit_code == 0
        assert "chainsaw" in stdout, (
            f"Expected 'chainsaw' in --list-tools output. stdout={stdout!r}"
        )


class TestBlueTeamFamilyResolution:
    """Blue-team tools resolve to the rainbow family without execution."""

    def test_trivy_resolves_to_rainbow_family(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """trivy resolves via auto-detection to rainbow / compliance service."""
        exit_code, stdout, stderr = cli_run("--health-check", "trivy", "version")
        assert exit_code == 0, f"Health check failed for trivy. stdout={stdout!r} stderr={stderr!r}"

    def test_yr_resolves_to_rainbow_family(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """yr resolves via auto-detection to rainbow / detection service."""
        exit_code, stdout, stderr = cli_run("--health-check", "yr", "version")
        assert exit_code == 0, f"Health check failed for yr. stdout={stdout!r} stderr={stderr!r}"

    def test_hayabusa_resolves_to_rainbow_family(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """hayabusa resolves via auto-detection to rainbow / detection service."""
        exit_code, stdout, stderr = cli_run("--health-check", "hayabusa", "version")
        assert exit_code == 0, (
            f"Health check failed for hayabusa. stdout={stdout!r} stderr={stderr!r}"
        )

    def test_trivy_no_engagement_required(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """trivy health check does not require --engagement-id (Zone 1).

        ENGAGEMENT_NOT_INIT (5) must not fire for a Zone 1 blue-team tool.
        """
        exit_code, stdout, stderr = cli_run("--health-check", "trivy", "version")
        assert exit_code != 5, f"Unexpected ENGAGEMENT_NOT_INIT for Zone 1 trivy. stderr={stderr!r}"


class TestTrivyLocalExecution:
    """trivy executes in local mode when the binary is on the host PATH.

    trivy is available via Homebrew on macOS development machines and is the
    most likely blue-team tool to be present on the host PATH.
    """

    @pytest.mark.skipif(
        not shutil.which("trivy"),
        reason="trivy not on PATH -- skipping local execution test",
    )
    def test_trivy_version_exit_0(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """trivy --version returns exit code 0 in local mode."""
        exit_code, stdout, stderr = cli_run("--mode", "local", "trivy", "version")
        assert exit_code == 0, (
            f"Expected exit 0 from 'trivy --version'. stdout={stdout!r} stderr={stderr!r}"
        )

    @pytest.mark.skipif(
        not shutil.which("trivy"),
        reason="trivy not on PATH -- skipping version content test",
    )
    def test_trivy_version_output_contains_version_number(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """trivy version output contains a version number.

        'trivy version' outputs 'Version: 0.69.3' without the word 'trivy';
        we check for a semantic version number (x.y.z) instead.
        """
        import re

        exit_code, stdout, stderr = cli_run("--mode", "local", "trivy", "version")
        assert exit_code == 0
        combined = stdout + stderr
        assert re.search(r"\d+\.\d+\.\d+", combined), (
            f"Expected a version number in trivy output. stdout={stdout!r} stderr={stderr!r}"
        )

    @pytest.mark.skipif(
        not shutil.which("trivy"),
        reason="trivy not on PATH -- skipping no-credential-leak test",
    )
    def test_trivy_version_no_credential_leak(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """trivy --version does not trigger the credential filter (exit 4).

        Zone 1 version commands carry no credentials.
        """
        exit_code, stdout, stderr = cli_run("--mode", "local", "trivy", "version")
        assert exit_code != 4, (
            f"Unexpected CREDENTIAL_DETECTED on 'trivy --version'. "
            f"stdout={stdout!r} stderr={stderr!r}"
        )

    @pytest.mark.skipif(
        not shutil.which("trivy"),
        reason="trivy not on PATH -- skipping Zone 1 no-engagement test",
    )
    def test_trivy_zone_1_no_engagement_id_required(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """trivy version runs without --engagement-id (Zone 1 does not require it)."""
        exit_code, stdout, stderr = cli_run("--mode", "local", "trivy", "version")
        assert exit_code != 5, f"Unexpected ENGAGEMENT_NOT_INIT for Zone 1 trivy. stderr={stderr!r}"
        assert exit_code == 0


class TestBlueTeamToolsNotOnPath:
    """When blue-team tools are absent from PATH, the CLI reports TOOL_ERROR."""

    def test_trivy_not_on_path_returns_error(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """trivy absent from PATH with local mode returns a non-zero exit code.

        LocalExecutor.execute() catches FileNotFoundError and returns exit_code=1.
        The test verifies a non-zero response (execution blocked) — the tool
        is registered in the registry but the binary is absent from the host.
        """
        if shutil.which("trivy"):
            pytest.skip("trivy is on PATH — skipping not-on-PATH test")
        exit_code, stdout, stderr = cli_run("--mode", "local", "trivy", "version")
        assert exit_code != 0, (
            f"Expected non-zero exit for trivy not on PATH. Got {exit_code}. "
            f"stdout={stdout!r} stderr={stderr!r}"
        )

    def test_yr_not_on_path_returns_error(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """yr absent from PATH with local mode returns a non-zero exit code.

        LocalExecutor.execute() catches FileNotFoundError and returns exit_code=1.
        The test verifies a non-zero response (execution blocked).
        """
        if shutil.which("yr"):
            pytest.skip("yr is on PATH — skipping not-on-PATH test")
        exit_code, stdout, stderr = cli_run("--mode", "local", "yr", "version")
        assert exit_code != 0, (
            f"Expected non-zero exit for yr not on PATH. Got {exit_code}. "
            f"stdout={stdout!r} stderr={stderr!r}"
        )
