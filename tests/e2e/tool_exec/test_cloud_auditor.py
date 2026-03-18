# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""TASK-037: Cloud auditor family E2E tests (checkov, prowler, kubescape).

Tests that the cloud auditor tools (checkov, prowler, kubescape) resolve
through the rainbow family and the rainbow-cloud cloud-auditor service.

All three tools are Zone 1 — passive IaC/cloud audit/analysis — and do
not require an engagement ID.

Execution strategy:
- checkov may be installed locally via pip in some environments.
- prowler and kubescape are typically only available inside the cloud-auditor
  container.
- Tool resolution tests (--list-tools, --health-check) are always executed
  and do not require the binaries on the host PATH.
- Local execution tests are skipped when the binary is absent from PATH.

Zone 1 policy (OWASP A05:2021):
- No engagement ID required.
- No per-operation approval gate.
- Network mode may be restricted at container runtime.

Exit code reference:
    0  SUCCESS
    1  UNKNOWN_TOOL
    2  TOOL_ERROR    (tool executed but returned non-zero)
    5  ENGAGEMENT_NOT_INIT  (must NOT fire for Zone 1 tools)

References:
    - TASK-037: Cloud auditor E2E tests
    - ADR-PROJ023-001: UC-001 Zone 1 path
    - tool-exec.yaml: checkov / prowler / kubescape entries under cloud-auditor service
"""

from __future__ import annotations

import shutil

import pytest

pytestmark = pytest.mark.e2e


class TestCloudAuditorToolRegistry:
    """checkov, prowler, and kubescape appear in the tool registry."""

    def test_checkov_appears_in_list_tools(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """--list-tools output includes 'checkov'."""
        exit_code, stdout, stderr = cli_run("--list-tools")
        assert exit_code == 0, f"--list-tools failed. stderr={stderr!r}"
        assert "checkov" in stdout, f"Expected 'checkov' in --list-tools output. stdout={stdout!r}"

    def test_prowler_appears_in_list_tools(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """--list-tools output includes 'prowler'."""
        exit_code, stdout, stderr = cli_run("--list-tools")
        assert exit_code == 0
        assert "prowler" in stdout, f"Expected 'prowler' in --list-tools output. stdout={stdout!r}"

    def test_kubescape_appears_in_list_tools(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """--list-tools output includes 'kubescape'."""
        exit_code, stdout, stderr = cli_run("--list-tools")
        assert exit_code == 0
        assert "kubescape" in stdout, (
            f"Expected 'kubescape' in --list-tools output. stdout={stdout!r}"
        )


class TestCloudAuditorFamilyResolution:
    """Cloud auditor tools resolve to the rainbow family without execution."""

    def test_checkov_resolves_to_rainbow_family(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """checkov resolves via auto-detection to rainbow / cloud-auditor service.

        --health-check confirms family resolution and compose-file discovery
        without spawning a container process.  'version' is a positional tool
        arg (not a dash-prefixed flag) so that jerry's own argparse does not
        intercept it as the top-level --version flag.
        """
        exit_code, stdout, stderr = cli_run("--health-check", "checkov", "version")
        assert exit_code == 0, (
            f"Health check failed for checkov. stdout={stdout!r} stderr={stderr!r}"
        )

    def test_checkov_no_engagement_required(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """checkov health check does not require --engagement-id (Zone 1).

        ENGAGEMENT_NOT_INIT (5) must not fire for a Zone 1 tool.
        """
        exit_code, stdout, stderr = cli_run("--health-check", "checkov", "version")
        assert exit_code != 5, (
            f"Unexpected ENGAGEMENT_NOT_INIT for Zone 1 checkov. stderr={stderr!r}"
        )

    def test_prowler_resolves_to_rainbow_family(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """prowler resolves via auto-detection to rainbow / cloud-auditor service."""
        exit_code, stdout, stderr = cli_run("--health-check", "prowler", "version")
        assert exit_code == 0, (
            f"Health check failed for prowler. stdout={stdout!r} stderr={stderr!r}"
        )

    def test_kubescape_resolves_to_rainbow_family(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """kubescape resolves via auto-detection to rainbow / cloud-auditor service."""
        exit_code, stdout, stderr = cli_run("--health-check", "kubescape", "version")
        assert exit_code == 0, (
            f"Health check failed for kubescape. stdout={stdout!r} stderr={stderr!r}"
        )


class TestCheckovLocalExecution:
    """checkov executes in local mode when the binary is on the host PATH."""

    @pytest.mark.skipif(
        not shutil.which("checkov"),
        reason="checkov not on PATH -- skipping local execution test",
    )
    def test_checkov_version_exit_0(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """checkov --version returns exit code 0 in local mode."""
        exit_code, stdout, stderr = cli_run("--mode", "local", "checkov", "version")
        assert exit_code == 0, (
            f"Expected exit 0 from 'checkov --version'. stdout={stdout!r} stderr={stderr!r}"
        )

    @pytest.mark.skipif(
        not shutil.which("checkov"),
        reason="checkov not on PATH -- skipping version content test",
    )
    def test_checkov_version_output_contains_checkov(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """checkov --version output contains 'checkov' in the combined output."""
        exit_code, stdout, stderr = cli_run("--mode", "local", "checkov", "version")
        assert exit_code == 0
        combined = (stdout + stderr).lower()
        assert "checkov" in combined, (
            f"Expected 'checkov' in output. stdout={stdout!r} stderr={stderr!r}"
        )

    @pytest.mark.skipif(
        not shutil.which("checkov"),
        reason="checkov not on PATH -- skipping no-credential-leak test",
    )
    def test_checkov_version_no_credential_leak(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """checkov --version does not trigger the credential filter (exit 4).

        Zone 1 version commands carry no credentials.
        """
        exit_code, stdout, stderr = cli_run("--mode", "local", "checkov", "version")
        assert exit_code != 4, (
            f"Unexpected CREDENTIAL_DETECTED on 'checkov --version'. "
            f"stdout={stdout!r} stderr={stderr!r}"
        )


class TestCloudAuditorNotOnPath:
    """When cloud auditor tools are absent from PATH, the CLI reports TOOL_ERROR."""

    def test_checkov_not_on_path_returns_error(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """checkov absent from PATH with local mode returns a non-zero exit code.

        LocalExecutor.execute() catches FileNotFoundError and returns exit_code=1
        (which the CLI surfaces as the "Tool not found" error path).  The test
        verifies that execution is blocked — the tool is in the registry, so
        this is a binary-absent failure, not a registry-absent failure.
        """
        if shutil.which("checkov"):
            pytest.skip("checkov is on PATH — skipping not-on-PATH test")
        exit_code, stdout, stderr = cli_run("--mode", "local", "checkov", "version")
        assert exit_code != 0, (
            f"Expected non-zero exit for checkov not on PATH. Got {exit_code}. "
            f"stdout={stdout!r} stderr={stderr!r}"
        )
