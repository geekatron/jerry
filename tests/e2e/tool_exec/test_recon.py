# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""TASK-039: Recon family E2E tests (subfinder, httpx, dnsx, naabu, katana, nuclei).

Tests that recon tools resolve through the rainbow family and the
rainbow-recon recon-pipeline service.  All recon tools are Zone 2 —
active reconnaissance — and require an initialized engagement scope.

Zone 2 policy (OWASP A01:2021):
- Engagement must be initialized with --init-engagement before use.
- Without --engagement-id, the CLI returns ENGAGEMENT_NOT_INIT (5).
- strict_mode=true requires an explicit --mode flag; omitting it on a
  Zone 2 tool returns MODE_UNSET (6).

Execution strategy:
- Recon tools are typically only available inside the recon-pipeline container.
- All resolution tests use --health-check or --list-tools (no PATH requirement).
- Engagement lifecycle tests use --init-engagement and verify exit codes.
- When subfinder is on the host PATH, a local execution test is included.

Exit code reference:
    0  SUCCESS
    1  UNKNOWN_TOOL
    2  TOOL_ERROR
    5  ENGAGEMENT_NOT_INIT  -- Zone 2: engagement required
    6  MODE_UNSET           -- strict mode: explicit mode required for Zone 2/3

References:
    - TASK-039: Recon E2E tests
    - ADR-PROJ023-001: UC-002 Zone 2 path
    - tool-exec.yaml: subfinder, httpx, dnsx, naabu, katana, nuclei (recon-pipeline)
"""

from __future__ import annotations

import shutil

import pytest

pytestmark = pytest.mark.e2e


class TestReconToolRegistry:
    """Recon tools appear in the tool registry."""

    def test_subfinder_appears_in_list_tools(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """--list-tools output includes 'subfinder'."""
        exit_code, stdout, stderr = cli_run("--list-tools")
        assert exit_code == 0, f"--list-tools failed. stderr={stderr!r}"
        assert "subfinder" in stdout, (
            f"Expected 'subfinder' in --list-tools output. stdout={stdout!r}"
        )

    def test_httpx_appears_in_list_tools(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """--list-tools output includes 'httpx'."""
        exit_code, stdout, stderr = cli_run("--list-tools")
        assert exit_code == 0
        assert "httpx" in stdout, f"Expected 'httpx' in --list-tools output. stdout={stdout!r}"

    def test_nuclei_appears_in_list_tools(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """--list-tools output includes 'nuclei'."""
        exit_code, stdout, stderr = cli_run("--list-tools")
        assert exit_code == 0
        assert "nuclei" in stdout, f"Expected 'nuclei' in --list-tools output. stdout={stdout!r}"

    def test_dnsx_appears_in_list_tools(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """--list-tools output includes 'dnsx'."""
        exit_code, stdout, stderr = cli_run("--list-tools")
        assert exit_code == 0
        assert "dnsx" in stdout, f"Expected 'dnsx' in --list-tools output. stdout={stdout!r}"


class TestReconFamilyResolution:
    """Recon tools resolve to the rainbow family via --health-check."""

    def test_subfinder_resolves_to_rainbow_family(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """subfinder resolves via auto-detection to rainbow / recon-pipeline service.

        Zone 2 strict mode requires explicit --mode for health checks.
        """
        exit_code, stdout, stderr = cli_run(
            "--health-check", "--mode", "container", "subfinder", "version"
        )
        assert exit_code == 0, (
            f"Health check failed for subfinder. stdout={stdout!r} stderr={stderr!r}"
        )

    def test_httpx_resolves_to_rainbow_family(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """httpx resolves via auto-detection to rainbow / recon-pipeline service.

        Zone 2 strict mode requires explicit --mode for health checks.
        """
        exit_code, stdout, stderr = cli_run(
            "--health-check", "--mode", "container", "httpx", "version"
        )
        assert exit_code == 0, f"Health check failed for httpx. stdout={stdout!r} stderr={stderr!r}"

    def test_nuclei_resolves_to_rainbow_family(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """nuclei resolves via auto-detection to rainbow / recon-pipeline service.

        Zone 2 strict mode requires explicit --mode for health checks.
        """
        exit_code, stdout, stderr = cli_run(
            "--health-check", "--mode", "container", "nuclei", "version"
        )
        assert exit_code == 0, (
            f"Health check failed for nuclei. stdout={stdout!r} stderr={stderr!r}"
        )


class TestReconZone2EngagementGate:
    """Zone 2 recon tools require an initialized engagement scope."""

    def test_subfinder_without_engagement_returns_engagement_not_init(
        self,
        cli_run,  # type: ignore[no-untyped-def]
    ) -> None:
        """subfinder with --mode container but no --engagement-id returns ENGAGEMENT_NOT_INIT (5).

        Zone 2 tools must verify that an engagement has been initialized
        before any execution.  This tests the security gate — the tool must
        not execute without a valid engagement scope.
        """
        exit_code, stdout, stderr = cli_run(
            "--mode",
            "container",
            "subfinder",
            "version",
        )
        assert exit_code == 5, (
            f"Expected ENGAGEMENT_NOT_INIT (5) for subfinder without engagement. "
            f"Got {exit_code}. stdout={stdout!r} stderr={stderr!r}"
        )

    def test_httpx_without_engagement_returns_engagement_not_init(
        self,
        cli_run,  # type: ignore[no-untyped-def]
    ) -> None:
        """httpx without --engagement-id returns ENGAGEMENT_NOT_INIT (5)."""
        exit_code, stdout, stderr = cli_run(
            "--mode",
            "container",
            "httpx",
            "version",
        )
        assert exit_code == 5, (
            f"Expected ENGAGEMENT_NOT_INIT (5) for httpx without engagement. "
            f"Got {exit_code}. stdout={stdout!r} stderr={stderr!r}"
        )

    def test_nuclei_without_engagement_returns_engagement_not_init(
        self,
        cli_run,  # type: ignore[no-untyped-def]
    ) -> None:
        """nuclei without --engagement-id returns ENGAGEMENT_NOT_INIT (5)."""
        exit_code, stdout, stderr = cli_run(
            "--mode",
            "container",
            "nuclei",
            "version",
        )
        assert exit_code == 5, (
            f"Expected ENGAGEMENT_NOT_INIT (5) for nuclei without engagement. "
            f"Got {exit_code}. stdout={stdout!r} stderr={stderr!r}"
        )


class TestReconWithEngagementInitialized:
    """Zone 2 recon tools proceed past the engagement gate when scope is initialized."""

    def test_subfinder_with_valid_engagement_passes_gate(
        self,
        cli_run,  # type: ignore[no-untyped-def]
        engagement_cleanup: list[str],
    ) -> None:
        """subfinder with a valid --engagement-id does not return ENGAGEMENT_NOT_INIT (5).

        The engagement gate is satisfied; subsequent failure (exit 2 or 3)
        is acceptable because the container may not be running.  The critical
        assertion is that exit code 5 must not fire when an engagement is
        provided.

        Steps:
        1. Initialize engagement E2E-TEST-RECON-001.
        2. Run subfinder -version with --engagement-id.
        3. Assert exit code is not 5 (engagement gate passed).
        """
        eng_id = "E2E-TEST-RECON-001"
        engagement_cleanup.append(eng_id)

        init_code, _out, _err = cli_run("--init-engagement", eng_id)
        assert init_code == 0, f"Init failed. stderr={_err!r}"

        exit_code, stdout, stderr = cli_run(
            "--mode",
            "container",
            "--engagement-id",
            eng_id,
            "subfinder",
            "version",
        )
        assert exit_code != 5, (
            f"ENGAGEMENT_NOT_INIT fired despite initialized engagement. "
            f"exit_code={exit_code} stderr={stderr!r}"
        )

    def test_httpx_with_valid_engagement_passes_gate(
        self,
        cli_run,  # type: ignore[no-untyped-def]
        engagement_cleanup: list[str],
    ) -> None:
        """httpx with a valid --engagement-id does not return ENGAGEMENT_NOT_INIT (5)."""
        eng_id = "E2E-TEST-RECON-002"
        engagement_cleanup.append(eng_id)

        init_code, _out, _err = cli_run("--init-engagement", eng_id)
        assert init_code == 0

        exit_code, stdout, stderr = cli_run(
            "--mode",
            "container",
            "--engagement-id",
            eng_id,
            "httpx",
            "version",
        )
        assert exit_code != 5, (
            f"ENGAGEMENT_NOT_INIT fired despite initialized engagement for httpx. "
            f"exit_code={exit_code} stderr={stderr!r}"
        )


class TestSubfinderLocalExecution:
    """subfinder executes in local mode when the binary is on the host PATH."""

    @pytest.mark.skipif(
        not shutil.which("subfinder"),
        reason="subfinder not on PATH -- skipping local execution test",
    )
    def test_subfinder_version_exit_0(
        self,
        cli_run,  # type: ignore[no-untyped-def]
        engagement_cleanup: list[str],
    ) -> None:
        """subfinder -version returns exit 0 in local mode with a valid engagement."""
        eng_id = "E2E-TEST-RECON-LOCAL-001"
        engagement_cleanup.append(eng_id)

        cli_run("--init-engagement", eng_id)
        exit_code, stdout, stderr = cli_run(
            "--mode",
            "local",
            "--engagement-id",
            eng_id,
            "subfinder",
            "version",
        )
        assert exit_code == 0, (
            f"Expected exit 0 from 'subfinder -version'. stdout={stdout!r} stderr={stderr!r}"
        )

    @pytest.mark.skipif(
        not shutil.which("subfinder"),
        reason="subfinder not on PATH -- skipping version content test",
    )
    def test_subfinder_version_output_contains_version(
        self,
        cli_run,  # type: ignore[no-untyped-def]
        engagement_cleanup: list[str],
    ) -> None:
        """subfinder -version output contains a version identifier."""
        eng_id = "E2E-TEST-RECON-LOCAL-002"
        engagement_cleanup.append(eng_id)

        cli_run("--init-engagement", eng_id)
        exit_code, stdout, stderr = cli_run(
            "--mode",
            "local",
            "--engagement-id",
            eng_id,
            "subfinder",
            "version",
        )
        assert exit_code == 0
        combined = (stdout + stderr).lower()
        assert "subfinder" in combined or "v2" in combined, (
            f"Expected version info in output. stdout={stdout!r} stderr={stderr!r}"
        )
