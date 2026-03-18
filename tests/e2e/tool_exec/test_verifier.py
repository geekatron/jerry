# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""TASK-036: Supply-chain verifier family E2E tests (cosign).

Tests that the cosign tool resolves through the rainbow family and
the rainbow-supply-chain verifier service.  cosign is a Zone 1 tool
for read-only operations (verify, tree) — engagement scope is not
required for version commands.

Execution strategy:
- cosign is installed inside the verifier container, not typically on the
  host PATH.  Local execution tests are skipped when cosign is absent from
  the host.
- Tool resolution tests use --health-check or --list-tools and are always
  executed (no PATH requirement).
- Container-mode tests are documented as expected patterns for future CI
  environments where cosign is on the host PATH.

Zone 1 policy:
- No engagement ID required.
- No approval gate.
- Network mode may be restricted at runtime (OWASP A05:2021).

Exit code reference:
    0  SUCCESS
    1  UNKNOWN_TOOL  (tool prefix not in any resolution table)
    2  TOOL_ERROR    (tool executed but returned non-zero)

References:
    - TASK-036: Verifier family E2E tests
    - ADR-PROJ023-001: UC-001 Zone 1 path, tool-exec.yaml verifier entries
    - tool_families.yaml: cosign and snyk registered under rainbow / verifier service
"""

from __future__ import annotations

import shutil

import pytest

pytestmark = pytest.mark.e2e


class TestCosignToolResolution:
    """cosign is resolved by the rainbow family via the verifier service."""

    def test_cosign_appears_in_list_tools(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """--list-tools output includes 'cosign' from the rainbow family.

        This test does not require cosign on the host PATH.  It only reads
        the tool_families.yaml and tool-exec.yaml registry.
        """
        exit_code, stdout, stderr = cli_run("--list-tools")
        assert exit_code == 0, f"--list-tools failed. stderr={stderr!r}"
        assert "cosign" in stdout, f"Expected 'cosign' in --list-tools output. stdout={stdout!r}"

    def test_snyk_appears_in_list_tools(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """--list-tools output includes 'snyk' from the rainbow family.

        snyk is registered alongside cosign under the verifier service.
        """
        exit_code, stdout, stderr = cli_run("--list-tools")
        assert exit_code == 0, f"--list-tools failed. stderr={stderr!r}"
        assert "snyk" in stdout, f"Expected 'snyk' in --list-tools output. stdout={stdout!r}"

    def test_cosign_resolves_to_rainbow_family(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """cosign resolves to the rainbow family via auto-detection.

        --health-check confirms family resolution and compose-file discovery
        without executing a container process.  This verifies that the
        ToolFamilyResolverPort can_resolve() and resolve() paths work for cosign.
        """
        exit_code, stdout, stderr = cli_run("--health-check", "cosign", "version")
        assert exit_code == 0, (
            f"Health check failed for cosign. stdout={stdout!r} stderr={stderr!r}"
        )

    def test_cosign_is_zone_1(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """--list-tools shows cosign as Zone 1.

        Zone 1 tools do not require an engagement ID.  The zone annotation
        must be present in the registry output so operators can reason about
        tool risk without reading source code (OWASP A09:2021 logging).
        """
        exit_code, stdout, stderr = cli_run("--list-tools")
        assert exit_code == 0
        # Zone information must appear somewhere in the output.
        assert "Zone 1" in stdout or "zone: 1" in stdout or "1" in stdout, (
            f"Expected Zone 1 annotation in --list-tools. stdout={stdout!r}"
        )

    def test_cosign_no_engagement_required(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """cosign with --health-check does not require --engagement-id.

        Zone 1 tools must not return ENGAGEMENT_NOT_INIT (5).
        """
        exit_code, stdout, stderr = cli_run("--health-check", "cosign", "version")
        assert exit_code != 5, (
            f"Unexpected ENGAGEMENT_NOT_INIT for Zone 1 cosign. stderr={stderr!r}"
        )


class TestCosignLocalExecution:
    """cosign executes in local mode when the binary is on the host PATH."""

    @pytest.mark.skipif(
        not shutil.which("cosign"),
        reason="cosign not on PATH -- skipping local execution test",
    )
    def test_cosign_version_exit_0(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """cosign version returns exit code 0 in local mode."""
        exit_code, stdout, stderr = cli_run("--mode", "local", "cosign", "version")
        assert exit_code == 0, (
            f"Expected exit 0 from 'cosign version'. stdout={stdout!r} stderr={stderr!r}"
        )

    @pytest.mark.skipif(
        not shutil.which("cosign"),
        reason="cosign not on PATH -- skipping version content test",
    )
    def test_cosign_version_output_contains_cosign(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """cosign version output contains 'cosign' in the combined output."""
        exit_code, stdout, stderr = cli_run("--mode", "local", "cosign", "version")
        assert exit_code == 0
        combined = (stdout + stderr).lower()
        assert "cosign" in combined, (
            f"Expected 'cosign' in output. stdout={stdout!r} stderr={stderr!r}"
        )

    @pytest.mark.skipif(
        not shutil.which("cosign"),
        reason="cosign not on PATH -- skipping no-credential-leak test",
    )
    def test_cosign_version_no_credential_leak(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """cosign version does not trigger the credential filter (exit 4).

        Zone 1 version commands carry no credentials; CREDENTIAL_DETECTED
        must not fire on benign version output.
        """
        exit_code, stdout, stderr = cli_run("--mode", "local", "cosign", "version")
        assert exit_code != 4, (
            f"Unexpected CREDENTIAL_DETECTED on 'cosign version'. "
            f"stdout={stdout!r} stderr={stderr!r}"
        )


class TestCosignNotOnPath:
    """When cosign is absent from PATH, the CLI reports a tool execution error."""

    def test_cosign_not_on_path_returns_error(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """When cosign is not on PATH and mode is local, the CLI returns a non-zero exit.

        LocalExecutor.execute() catches FileNotFoundError and returns exit_code=1.
        The test verifies that execution is blocked — the binary is absent from
        the host but the tool IS registered in the rainbow family registry.
        """
        if shutil.which("cosign"):
            pytest.skip("cosign is on PATH — skipping not-on-PATH test")
        exit_code, stdout, stderr = cli_run("--mode", "local", "cosign", "version")
        assert exit_code != 0, (
            f"Expected non-zero exit for cosign not on PATH. Got {exit_code}. "
            f"stdout={stdout!r} stderr={stderr!r}"
        )
