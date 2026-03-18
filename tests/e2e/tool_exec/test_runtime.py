# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""TASK-040: Runtime family E2E tests (mitmproxy, mitmdump, mitmweb, frida).

Tests that runtime tools resolve through the rainbow family and the
rainbow-runtime mitmproxy / frida services.  Runtime tools are Zone 2
(active traffic interception / process instrumentation) and require an
initialized engagement scope.

Services:
    mitmproxy  -- mitmproxy, mitmdump, mitmweb
    frida      -- frida, frida-trace, frida-ps

Zone 2 policy (OWASP A01:2021):
- Engagement must be initialized before use.
- Without --engagement-id, the CLI returns ENGAGEMENT_NOT_INIT (5).
- strict_mode=true requires explicit --mode for Zone 2/3 tools.

Execution strategy:
- mitmproxy/frida tools live inside their containers, not typically on the
  host PATH.
- All resolution tests use --health-check or --list-tools.
- Engagement gate tests verify exit code 5 fires before any container access.

Exit code reference:
    0  SUCCESS
    1  UNKNOWN_TOOL
    2  TOOL_ERROR
    5  ENGAGEMENT_NOT_INIT
    6  MODE_UNSET

References:
    - TASK-040: Runtime E2E tests
    - ADR-PROJ023-001: UC-002 Zone 2 path
    - tool-exec.yaml: mitmproxy, mitmdump, mitmweb, frida entries
"""

from __future__ import annotations

import shutil

import pytest

pytestmark = pytest.mark.e2e


class TestRuntimeToolRegistry:
    """Runtime tools appear in the tool registry."""

    def test_mitmproxy_appears_in_list_tools(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """--list-tools output includes 'mitmproxy'."""
        exit_code, stdout, stderr = cli_run("--list-tools")
        assert exit_code == 0, f"--list-tools failed. stderr={stderr!r}"
        assert "mitmproxy" in stdout, (
            f"Expected 'mitmproxy' in --list-tools output. stdout={stdout!r}"
        )

    def test_mitmdump_appears_in_list_tools(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """--list-tools output includes 'mitmdump'."""
        exit_code, stdout, stderr = cli_run("--list-tools")
        assert exit_code == 0
        assert "mitmdump" in stdout, (
            f"Expected 'mitmdump' in --list-tools output. stdout={stdout!r}"
        )

    def test_frida_appears_in_list_tools(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """--list-tools output includes 'frida'."""
        exit_code, stdout, stderr = cli_run("--list-tools")
        assert exit_code == 0
        assert "frida" in stdout, f"Expected 'frida' in --list-tools output. stdout={stdout!r}"

    def test_frida_trace_appears_in_list_tools(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """--list-tools output includes 'frida-trace'."""
        exit_code, stdout, stderr = cli_run("--list-tools")
        assert exit_code == 0
        assert "frida-trace" in stdout, (
            f"Expected 'frida-trace' in --list-tools output. stdout={stdout!r}"
        )


class TestRuntimeFamilyResolution:
    """Runtime tools resolve to the rainbow family via --health-check."""

    def test_mitmproxy_resolves_to_rainbow_family(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """mitmproxy resolves via auto-detection to rainbow / mitmproxy service.

        Zone 2 strict mode requires explicit --mode for health checks.
        """
        exit_code, stdout, stderr = cli_run(
            "--health-check", "--mode", "container", "mitmproxy", "version"
        )
        assert exit_code == 0, (
            f"Health check failed for mitmproxy. stdout={stdout!r} stderr={stderr!r}"
        )

    def test_mitmdump_resolves_to_rainbow_family(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """mitmdump resolves via auto-detection to rainbow / mitmproxy service.

        Zone 2 strict mode requires explicit --mode for health checks.
        """
        exit_code, stdout, stderr = cli_run(
            "--health-check", "--mode", "container", "mitmdump", "version"
        )
        assert exit_code == 0, (
            f"Health check failed for mitmdump. stdout={stdout!r} stderr={stderr!r}"
        )

    def test_frida_resolves_to_rainbow_family(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """frida resolves via auto-detection to rainbow / frida service.

        Zone 2 strict mode requires explicit --mode for health checks.
        """
        exit_code, stdout, stderr = cli_run(
            "--health-check", "--mode", "container", "frida", "version"
        )
        assert exit_code == 0, f"Health check failed for frida. stdout={stdout!r} stderr={stderr!r}"


class TestRuntimeZone2EngagementGate:
    """Zone 2 runtime tools require an initialized engagement scope."""

    def test_mitmproxy_without_engagement_returns_engagement_not_init(
        self,
        cli_run,  # type: ignore[no-untyped-def]
    ) -> None:
        """mitmproxy with --mode container but no --engagement-id returns ENGAGEMENT_NOT_INIT (5).

        Zone 2 tools must not execute without a valid engagement scope.
        This test verifies that the security gate fires before any container
        interaction occurs.
        """
        exit_code, stdout, stderr = cli_run(
            "--mode",
            "container",
            "mitmproxy",
            "version",
        )
        assert exit_code == 5, (
            f"Expected ENGAGEMENT_NOT_INIT (5) for mitmproxy without engagement. "
            f"Got {exit_code}. stdout={stdout!r} stderr={stderr!r}"
        )

    def test_mitmdump_without_engagement_returns_engagement_not_init(
        self,
        cli_run,  # type: ignore[no-untyped-def]
    ) -> None:
        """mitmdump without --engagement-id returns ENGAGEMENT_NOT_INIT (5)."""
        exit_code, stdout, stderr = cli_run(
            "--mode",
            "container",
            "mitmdump",
            "version",
        )
        assert exit_code == 5, (
            f"Expected ENGAGEMENT_NOT_INIT (5) for mitmdump without engagement. "
            f"Got {exit_code}. stdout={stdout!r} stderr={stderr!r}"
        )

    def test_frida_without_engagement_returns_engagement_not_init(
        self,
        cli_run,  # type: ignore[no-untyped-def]
    ) -> None:
        """frida without --engagement-id returns ENGAGEMENT_NOT_INIT (5)."""
        exit_code, stdout, stderr = cli_run(
            "--mode",
            "container",
            "frida",
            "version",
        )
        assert exit_code == 5, (
            f"Expected ENGAGEMENT_NOT_INIT (5) for frida without engagement. "
            f"Got {exit_code}. stdout={stdout!r} stderr={stderr!r}"
        )


class TestRuntimeWithEngagementInitialized:
    """Zone 2 runtime tools proceed past the engagement gate when scope is set."""

    def test_mitmproxy_with_valid_engagement_passes_gate(
        self,
        cli_run,  # type: ignore[no-untyped-def]
        engagement_cleanup: list[str],
    ) -> None:
        """mitmproxy with --engagement-id does not return ENGAGEMENT_NOT_INIT (5).

        The engagement gate is satisfied; subsequent failure (container not
        running: exit 3, or TOOL_ERROR: exit 2) is acceptable.  The critical
        assertion is that exit code 5 must not fire when a valid engagement
        is provided.

        Steps:
        1. Initialize engagement E2E-TEST-RT-001.
        2. Run mitmproxy --version with --engagement-id.
        3. Assert exit code is not 5.
        """
        eng_id = "E2E-TEST-RT-001"
        engagement_cleanup.append(eng_id)

        init_code, _out, _err = cli_run("--init-engagement", eng_id)
        assert init_code == 0, f"Init failed. stderr={_err!r}"

        exit_code, stdout, stderr = cli_run(
            "--mode",
            "container",
            "--engagement-id",
            eng_id,
            "mitmproxy",
            "version",
        )
        assert exit_code != 5, (
            f"ENGAGEMENT_NOT_INIT fired despite initialized engagement. "
            f"exit_code={exit_code} stderr={stderr!r}"
        )

    def test_frida_with_valid_engagement_passes_gate(
        self,
        cli_run,  # type: ignore[no-untyped-def]
        engagement_cleanup: list[str],
    ) -> None:
        """frida with --engagement-id does not return ENGAGEMENT_NOT_INIT (5)."""
        eng_id = "E2E-TEST-RT-002"
        engagement_cleanup.append(eng_id)

        init_code, _out, _err = cli_run("--init-engagement", eng_id)
        assert init_code == 0

        exit_code, stdout, stderr = cli_run(
            "--mode",
            "container",
            "--engagement-id",
            eng_id,
            "frida",
            "version",
        )
        assert exit_code != 5, (
            f"ENGAGEMENT_NOT_INIT fired despite initialized engagement for frida. "
            f"exit_code={exit_code} stderr={stderr!r}"
        )


class TestMitmproxyLocalExecution:
    """mitmproxy executes in local mode when the binary is on the host PATH."""

    @pytest.mark.skipif(
        not shutil.which("mitmproxy"),
        reason="mitmproxy not on PATH -- skipping local execution test",
    )
    def test_mitmproxy_version_exit_0(
        self,
        cli_run,  # type: ignore[no-untyped-def]
        engagement_cleanup: list[str],
    ) -> None:
        """mitmproxy --version returns exit 0 in local mode with a valid engagement."""
        eng_id = "E2E-TEST-RT-LOCAL-001"
        engagement_cleanup.append(eng_id)

        cli_run("--init-engagement", eng_id)
        exit_code, stdout, stderr = cli_run(
            "--mode",
            "local",
            "--engagement-id",
            eng_id,
            "mitmproxy",
            "version",
        )
        assert exit_code == 0, (
            f"Expected exit 0 from 'mitmproxy --version'. stdout={stdout!r} stderr={stderr!r}"
        )

    @pytest.mark.skipif(
        not shutil.which("mitmproxy"),
        reason="mitmproxy not on PATH -- skipping version content test",
    )
    def test_mitmproxy_version_output_contains_mitmproxy(
        self,
        cli_run,  # type: ignore[no-untyped-def]
        engagement_cleanup: list[str],
    ) -> None:
        """mitmproxy --version output contains 'mitmproxy' identifier."""
        eng_id = "E2E-TEST-RT-LOCAL-002"
        engagement_cleanup.append(eng_id)

        cli_run("--init-engagement", eng_id)
        exit_code, stdout, stderr = cli_run(
            "--mode",
            "local",
            "--engagement-id",
            eng_id,
            "mitmproxy",
            "version",
        )
        assert exit_code == 0
        combined = (stdout + stderr).lower()
        assert "mitmproxy" in combined, (
            f"Expected 'mitmproxy' in output. stdout={stdout!r} stderr={stderr!r}"
        )
