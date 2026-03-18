# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""TASK-031: Zone 1 real tool execution E2E tests.

Tests that syft and grype execute through the real jerry tool exec pipeline.
Both tools are available on the host (installed via Homebrew) and also inside
the scanner container.

Execution strategy:
- Local mode tests: use `--mode local` (or omit --mode to accept the config
  default of 'local').  syft and grype are on the host PATH.
- Container mode tests: exercised via --health-check which confirms the
  family resolution and compose-file discovery logic without requiring a
  long-running container process.

Design:
- Zone 1 tools do not require an engagement ID.
- The credential filter must not trigger on version output.

OWASP A05:2021: Container runs with network_mode: none (Zone 1 enforcement).

References:
    - TASK-031: Zone 1 tool execution E2E tests
    - ADR-PROJ023-001: Behavioral Contract -- UC-001 Zone 1 path
"""

from __future__ import annotations

import re

import pytest

pytestmark = pytest.mark.e2e


class TestSyftLocalExecution:
    """syft runs in local mode (tool on host PATH) and returns version info."""

    def test_syft_version_exit_0(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """syft version returns exit code 0 via local mode."""
        exit_code, stdout, stderr = cli_run("--mode", "local", "syft", "version")
        assert exit_code == 0, (
            f"Expected exit 0 from 'syft version', got {exit_code}. "
            f"stdout={stdout!r} stderr={stderr!r}"
        )

    def test_syft_version_stdout_contains_syft(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """syft version output contains the word 'syft'."""
        exit_code, stdout, stderr = cli_run("--mode", "local", "syft", "version")
        assert exit_code == 0
        combined = (stdout + stderr).lower()
        assert "syft" in combined, f"Expected 'syft' in output. stdout={stdout!r} stderr={stderr!r}"

    def test_syft_version_stdout_contains_version_number(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """syft version output contains a semantic version string."""
        exit_code, stdout, stderr = cli_run("--mode", "local", "syft", "version")
        assert exit_code == 0
        combined = stdout + stderr
        assert re.search(r"\d+\.\d+\.\d+", combined), (
            f"Expected a version number (x.y.z) in output. stdout={stdout!r} stderr={stderr!r}"
        )

    def test_syft_version_no_credential_leak(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """syft version output does not trigger the credential filter.

        Zone 1 version commands carry no credentials; exit code 4
        (CREDENTIAL_DETECTED) must not fire.
        """
        exit_code, stdout, stderr = cli_run("--mode", "local", "syft", "version")
        assert exit_code == 0
        assert exit_code != 4, "Unexpected CREDENTIAL_DETECTED on `syft version`"


class TestGrypeLocalExecution:
    """grype runs in local mode and returns version info."""

    def test_grype_version_exit_0(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """grype version returns exit code 0 via local mode."""
        exit_code, stdout, stderr = cli_run("--mode", "local", "grype", "version")
        assert exit_code == 0, (
            f"Expected exit 0 from 'grype version', got {exit_code}. "
            f"stdout={stdout!r} stderr={stderr!r}"
        )

    def test_grype_version_stdout_contains_grype(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """grype version output contains the word 'grype'."""
        exit_code, stdout, stderr = cli_run("--mode", "local", "grype", "version")
        assert exit_code == 0
        combined = (stdout + stderr).lower()
        assert "grype" in combined, (
            f"Expected 'grype' in output. stdout={stdout!r} stderr={stderr!r}"
        )

    def test_grype_resolves_to_scanner_family(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """grype is resolved by the rainbow family without error.

        Using --health-check confirms that the family resolver finds grype and
        identifies its container service without actually running a container.
        """
        exit_code, stdout, stderr = cli_run("--health-check", "grype", "version")
        assert exit_code == 0, f"Health check failed for grype. stdout={stdout!r} stderr={stderr!r}"


class TestZone1NoEngagementRequired:
    """Zone 1 tools must not require an engagement ID."""

    def test_syft_without_engagement_id_exits_0(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """syft version runs without --engagement-id (Zone 1 does not require it)."""
        exit_code, stdout, stderr = cli_run("--mode", "local", "syft", "version")
        # Must not return ENGAGEMENT_NOT_INIT (5)
        assert exit_code != 5, (
            f"Unexpected ENGAGEMENT_NOT_INIT for a Zone 1 tool. stderr={stderr!r}"
        )
        assert exit_code == 0

    def test_grype_without_engagement_id_exits_0(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """grype version runs without --engagement-id."""
        exit_code, stdout, stderr = cli_run("--mode", "local", "grype", "version")
        assert exit_code != 5
        assert exit_code == 0
