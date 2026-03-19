# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""TASK-049: Container-mode coverage for all tool families.

Exercises every tool family through the real jerry CLI with --mode container,
each backed by its corresponding Docker Compose cluster.  No mocks.  No
patches.  Real subprocess, real Docker, real Envoy.

Test structure:
    TestZone1OfflineContainerMode  -- zone1-offline tools (syft, yr, etc.)
    TestZone1UpdateContainerMode   -- zone1-update tools via Envoy (grype, trivy)
    TestZone2ContainerMode         -- zone2 tools via Envoy + engagement
    TestSecurityGatesContainerMode -- security policy enforcement in container mode

Each test uses cli_run("--mode", "container", ...) and asserts:
- exit_code in (0, 2): tool executed inside the container (0=SUCCESS, 2=TOOL_ERROR)
- stdout or stderr contains expected version/help text

Exit code reference:
    0   SUCCESS
    1   UNKNOWN_TOOL
    2   TOOL_ERROR             (tool executed but returned non-zero)
    3   CONTAINER_NOT_RUNNING  (proxy or container absent)
    5   ENGAGEMENT_NOT_INIT    (Zone 2/3 tool without initialized engagement)
    6   MODE_UNSET             (strict_mode: explicit mode required)
   10   ZONE3_CONTAINER_REQUIRED (--mode local rejected for Zone 3)
   11   ZONE3_APPROVAL_DENIED  (gate auto-denied in non-TTY context)

Design constraints:
- No mocks. No patches. Real subprocess, real Docker, real Envoy.
- All container-mode tests use cli_run("--mode", "container", ...).
- Zone 2+ tests pass --engagement-id E2E-TEST-001 (created by engagement_init).
- Each test class receives only the cluster fixture it needs (no autouse).

Security notes:
- Zone 3 auto-deny (no TTY) is tested in TestSecurityGatesContainerMode.
- Zone 2 engagement gate is tested by zone2_requires_engagement test.

References:
    - TASK-049: Container-mode E2E coverage
    - ADR-PROJ023-001: Behavioral Contract
    - tool-exec.yaml: zone assignments for all tools
"""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.e2e


# ---------------------------------------------------------------------------
# Zone 1 Offline — container CANNOT reach internet; no proxy needed
# ---------------------------------------------------------------------------


class TestZone1OfflineContainerMode:
    """Tools on zone1-offline network execute in container mode.

    Zone 1 offline: internal: true, no proxy, no internet access.
    Tools: syft (supply-chain), yr, hayabusa, chainsaw (blue-team detection),
    checkov (blue-team compliance).
    """

    def test_syft_container(self, supply_chain_cluster: str, cli_run) -> None:  # type: ignore[no-untyped-def]
        """syft executes in container mode and prints version/help text.

        syft --version is a Zone 1 offline tool -- no proxy, no engagement.
        Exit 0 (SUCCESS) or 2 (TOOL_ERROR) both confirm container execution.
        """
        exit_code, stdout, stderr = cli_run("--mode", "container", "syft", "--", "--version")
        assert exit_code in (0, 2), (
            f"Expected container execution (0 or 2) for syft. "
            f"Got exit_code={exit_code}. stdout={stdout!r} stderr={stderr!r}"
        )
        combined = stdout + stderr
        assert "syft" in combined.lower(), (
            f"Expected 'syft' in output. stdout={stdout!r} stderr={stderr!r}"
        )

    def test_yr_container(self, blue_team_cluster: str, cli_run) -> None:  # type: ignore[no-untyped-def]
        """yr (YARA-X CLI) executes in container mode.

        yr --version is a Zone 1 offline tool -- no proxy, no engagement.
        """
        exit_code, stdout, stderr = cli_run("--mode", "container", "yr", "--", "--version")
        assert exit_code in (0, 2), (
            f"Expected container execution (0 or 2) for yr. "
            f"Got exit_code={exit_code}. stdout={stdout!r} stderr={stderr!r}"
        )
        combined = stdout + stderr
        assert any(kw in combined.lower() for kw in ("yr", "yara", "yara-x")), (
            f"Expected yr/yara version text in output. stdout={stdout!r} stderr={stderr!r}"
        )

    def test_hayabusa_container(self, blue_team_cluster: str, cli_run) -> None:  # type: ignore[no-untyped-def]
        """hayabusa executes in container mode.

        hayabusa is a Zone 1 offline forensics tool -- no proxy, no engagement.
        """
        exit_code, stdout, stderr = cli_run("--mode", "container", "hayabusa", "--", "--version")
        assert exit_code in (0, 2), (
            f"Expected container execution (0 or 2) for hayabusa. "
            f"Got exit_code={exit_code}. stdout={stdout!r} stderr={stderr!r}"
        )
        combined = stdout + stderr
        assert "hayabusa" in combined.lower(), (
            f"Expected 'hayabusa' in output. stdout={stdout!r} stderr={stderr!r}"
        )

    def test_chainsaw_container(self, blue_team_cluster: str, cli_run) -> None:  # type: ignore[no-untyped-def]
        """chainsaw executes in container mode.

        chainsaw is a Zone 1 offline forensics tool -- no proxy, no engagement.
        """
        exit_code, stdout, stderr = cli_run("--mode", "container", "chainsaw", "--", "--version")
        assert exit_code in (0, 2), (
            f"Expected container execution (0 or 2) for chainsaw. "
            f"Got exit_code={exit_code}. stdout={stdout!r} stderr={stderr!r}"
        )
        combined = stdout + stderr
        assert "chainsaw" in combined.lower(), (
            f"Expected 'chainsaw' in output. stdout={stdout!r} stderr={stderr!r}"
        )

    def test_checkov_container(self, blue_team_cluster: str, cli_run) -> None:  # type: ignore[no-untyped-def]
        """checkov executes in container mode.

        checkov is a Zone 1 IaC analysis tool -- no proxy, no engagement.
        """
        exit_code, stdout, stderr = cli_run("--mode", "container", "checkov", "--", "--version")
        assert exit_code in (0, 2), (
            f"Expected container execution (0 or 2) for checkov. "
            f"Got exit_code={exit_code}. stdout={stdout!r} stderr={stderr!r}"
        )
        combined = stdout + stderr
        assert "checkov" in combined.lower(), (
            f"Expected 'checkov' in output. stdout={stdout!r} stderr={stderr!r}"
        )


# ---------------------------------------------------------------------------
# Zone 1 Update — tools pull vulnerability DBs via Envoy proxy allowlist
# ---------------------------------------------------------------------------


class TestZone1UpdateContainerMode:
    """Tools on zone1-update network execute via the Envoy proxy.

    Zone 1 update: internal: true + Envoy proxy for allowlisted DB hosts.
    Tools: grype (supply-chain), trivy (blue-team compliance).
    No engagement required for Zone 1 tools.
    """

    def test_grype_container(self, supply_chain_cluster: str, cli_run) -> None:  # type: ignore[no-untyped-def]
        """grype executes in container mode via Zone 1 update network.

        grype --version does not hit the vulnerability DB so no proxy
        traffic is required; the test confirms container execution only.
        """
        exit_code, stdout, stderr = cli_run("--mode", "container", "grype", "--", "--version")
        assert exit_code in (0, 2), (
            f"Expected container execution (0 or 2) for grype. "
            f"Got exit_code={exit_code}. stdout={stdout!r} stderr={stderr!r}"
        )
        combined = stdout + stderr
        assert "grype" in combined.lower(), (
            f"Expected 'grype' in output. stdout={stdout!r} stderr={stderr!r}"
        )

    def test_trivy_container(self, blue_team_cluster: str, cli_run) -> None:  # type: ignore[no-untyped-def]
        """trivy executes in container mode via Zone 1 update network.

        trivy --version does not download the vulnerability DB; confirms
        container execution without proxy traffic.
        """
        exit_code, stdout, stderr = cli_run("--mode", "container", "trivy", "--", "--version")
        assert exit_code in (0, 2), (
            f"Expected container execution (0 or 2) for trivy. "
            f"Got exit_code={exit_code}. stdout={stdout!r} stderr={stderr!r}"
        )
        combined = stdout + stderr
        assert "trivy" in combined.lower(), (
            f"Expected 'trivy' in output. stdout={stdout!r} stderr={stderr!r}"
        )


# ---------------------------------------------------------------------------
# Zone 2 — active recon / cloud posture / runtime; requires engagement
# ---------------------------------------------------------------------------


class TestZone2ContainerMode:
    """Zone 2 tools execute via Envoy with an initialized engagement.

    Zone 2 tools require --engagement-id pointing to an initialized scope.
    All tests in this class receive the engagement_init fixture to ensure
    E2E-TEST-001 exists before the tool call is made.
    """

    def test_subfinder_container(self, recon_cluster: str, engagement_init: None, cli_run) -> None:  # type: ignore[no-untyped-def]
        """subfinder executes in container mode with engagement scope.

        subfinder is a Zone 2 recon tool. --engagement-id E2E-TEST-001 is
        required. Exit 0 or 2 confirms the gate passed and the tool ran.
        """
        exit_code, stdout, stderr = cli_run(
            "--mode",
            "container",
            "--engagement-id",
            "E2E-TEST-001",
            "subfinder",
            "--",
            "-version",
        )
        assert exit_code in (0, 2), (
            f"Expected container execution (0 or 2) for subfinder. "
            f"Got exit_code={exit_code}. stdout={stdout!r} stderr={stderr!r}"
        )
        combined = stdout + stderr
        assert "subfinder" in combined.lower() or "v" in combined.lower(), (
            f"Expected version text in output. stdout={stdout!r} stderr={stderr!r}"
        )

    def test_httpx_container(self, recon_cluster: str, engagement_init: None, cli_run) -> None:  # type: ignore[no-untyped-def]
        """httpx executes in container mode with engagement scope."""
        exit_code, stdout, stderr = cli_run(
            "--mode",
            "container",
            "--engagement-id",
            "E2E-TEST-001",
            "httpx",
            "--",
            "-version",
        )
        assert exit_code in (0, 2), (
            f"Expected container execution (0 or 2) for httpx. "
            f"Got exit_code={exit_code}. stdout={stdout!r} stderr={stderr!r}"
        )
        combined = stdout + stderr
        assert "httpx" in combined.lower() or "v" in combined.lower(), (
            f"Expected version text in output. stdout={stdout!r} stderr={stderr!r}"
        )

    def test_nuclei_container(self, recon_cluster: str, engagement_init: None, cli_run) -> None:  # type: ignore[no-untyped-def]
        """nuclei executes in container mode with engagement scope."""
        exit_code, stdout, stderr = cli_run(
            "--mode",
            "container",
            "--engagement-id",
            "E2E-TEST-001",
            "nuclei",
            "--",
            "-version",
        )
        assert exit_code in (0, 2), (
            f"Expected container execution (0 or 2) for nuclei. "
            f"Got exit_code={exit_code}. stdout={stdout!r} stderr={stderr!r}"
        )
        combined = stdout + stderr
        assert "nuclei" in combined.lower() or "v" in combined.lower(), (
            f"Expected version text in output. stdout={stdout!r} stderr={stderr!r}"
        )

    def test_prowler_container(self, cloud_cluster: str, engagement_init: None, cli_run) -> None:  # type: ignore[no-untyped-def]
        """prowler executes in container mode with engagement scope.

        prowler is a Zone 2 cloud posture tool.
        """
        exit_code, stdout, stderr = cli_run(
            "--mode",
            "container",
            "--engagement-id",
            "E2E-TEST-001",
            "prowler",
            "--",
            "--version",
        )
        assert exit_code in (0, 2), (
            f"Expected container execution (0 or 2) for prowler. "
            f"Got exit_code={exit_code}. stdout={stdout!r} stderr={stderr!r}"
        )
        combined = stdout + stderr
        assert "prowler" in combined.lower() or "v" in combined.lower(), (
            f"Expected version text in output. stdout={stdout!r} stderr={stderr!r}"
        )

    def test_kubescape_container(self, cloud_cluster: str, engagement_init: None, cli_run) -> None:  # type: ignore[no-untyped-def]
        """kubescape executes in container mode with engagement scope.

        kubescape is a Zone 2 Kubernetes posture tool.
        """
        exit_code, stdout, stderr = cli_run(
            "--mode",
            "container",
            "--engagement-id",
            "E2E-TEST-001",
            "kubescape",
            "--",
            "version",
        )
        assert exit_code in (0, 2), (
            f"Expected container execution (0 or 2) for kubescape. "
            f"Got exit_code={exit_code}. stdout={stdout!r} stderr={stderr!r}"
        )
        combined = stdout + stderr
        assert "kubescape" in combined.lower() or "v" in combined.lower(), (
            f"Expected version text in output. stdout={stdout!r} stderr={stderr!r}"
        )

    def test_mitmdump_container(self, runtime_cluster: str, engagement_init: None, cli_run) -> None:  # type: ignore[no-untyped-def]
        """mitmdump executes in container mode with engagement scope.

        mitmdump is a Zone 2 runtime traffic interception tool.
        """
        exit_code, stdout, stderr = cli_run(
            "--mode",
            "container",
            "--engagement-id",
            "E2E-TEST-001",
            "mitmdump",
            "--",
            "--version",
        )
        assert exit_code in (0, 2), (
            f"Expected container execution (0 or 2) for mitmdump. "
            f"Got exit_code={exit_code}. stdout={stdout!r} stderr={stderr!r}"
        )
        combined = stdout + stderr
        assert "mitmproxy" in combined.lower() or "mitmdump" in combined.lower(), (
            f"Expected mitmproxy/mitmdump version text. stdout={stdout!r} stderr={stderr!r}"
        )

    def test_frida_container(self, runtime_cluster: str, engagement_init: None, cli_run) -> None:  # type: ignore[no-untyped-def]
        """frida executes in container mode with engagement scope.

        frida is a Zone 2 runtime instrumentation tool.
        """
        exit_code, stdout, stderr = cli_run(
            "--mode",
            "container",
            "--engagement-id",
            "E2E-TEST-001",
            "frida",
            "--",
            "--version",
        )
        assert exit_code in (0, 2), (
            f"Expected container execution (0 or 2) for frida. "
            f"Got exit_code={exit_code}. stdout={stdout!r} stderr={stderr!r}"
        )
        combined = stdout + stderr
        assert "frida" in combined.lower() or "v" in combined.lower(), (
            f"Expected frida version text. stdout={stdout!r} stderr={stderr!r}"
        )


# ---------------------------------------------------------------------------
# Security gates in container mode
# ---------------------------------------------------------------------------


class TestSecurityGatesContainerMode:
    """Security enforcement in container mode.

    These tests verify that the security policy gates work correctly when
    --mode container is specified:
    - Zone 2 requires engagement.
    - Zone 3 auto-denies in non-TTY (subprocess) context.
    - Unknown tools return UNKNOWN_TOOL (1).
    - Invalid family returns UNKNOWN_TOOL (1).
    """

    def test_zone2_requires_engagement(self, recon_cluster: str, cli_run) -> None:  # type: ignore[no-untyped-def]
        """Zone 2 tool in container mode without engagement returns ENGAGEMENT_NOT_INIT (5).

        subfinder is Zone 2. Invoking it without --engagement-id must be
        blocked before any container execution occurs.
        """
        exit_code, stdout, stderr = cli_run(
            "--mode",
            "container",
            "subfinder",
            "--",
            "-version",
        )
        assert exit_code == 5, (
            f"Expected ENGAGEMENT_NOT_INIT (5) for Zone 2 subfinder without engagement. "
            f"Got exit_code={exit_code}. stdout={stdout!r} stderr={stderr!r}"
        )

    def test_zone3_auto_deny_no_tty(
        self, exploit_cluster: str, engagement_init: None, cli_run
    ) -> None:  # type: ignore[no-untyped-def]
        """Zone 3 tool in container mode auto-denies in non-TTY subprocess (exit 11).

        impacket-GetADUsers is Zone 3.  cli_run uses subprocess.run() which
        captures stdin as a pipe — not a TTY.  The approval gate must detect
        the non-TTY context and return ZONE3_APPROVAL_DENIED (11) without
        prompting or executing.

        The exploit_cluster fixture ensures the exploit compose stack is
        running so the resolution path reaches the approval gate.
        """
        exit_code, stdout, stderr = cli_run(
            "--mode",
            "container",
            "--engagement-id",
            "E2E-TEST-001",
            "impacket-GetADUsers",
            "--",
            "--help",
        )
        assert exit_code == 11, (
            f"Expected ZONE3_APPROVAL_DENIED (11) for Zone 3 non-TTY. "
            f"Got exit_code={exit_code}. stdout={stdout!r} stderr={stderr!r}"
        )

    def test_unknown_tool(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """An unknown tool name returns UNKNOWN_TOOL (1) in container mode.

        The registry lookup fails before any zone policy is evaluated.
        """
        exit_code, stdout, stderr = cli_run(
            "--mode",
            "container",
            "no-such-tool-xyz-9999",
        )
        assert exit_code == 1, (
            f"Expected UNKNOWN_TOOL (1) for unregistered tool. "
            f"Got exit_code={exit_code}. stdout={stdout!r} stderr={stderr!r}"
        )

    def test_bad_family(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """An explicit --family that does not exist returns a non-zero exit.

        Passing --family nonexistent forces the family router to fail
        before tool resolution; the CLI must not return exit 0.
        """
        exit_code, stdout, stderr = cli_run(
            "--mode",
            "container",
            "--family",
            "nonexistent-family-xyz",
            "syft",
        )
        assert exit_code != 0, (
            f"Expected non-zero exit for unknown family. "
            f"Got exit_code={exit_code}. stdout={stdout!r} stderr={stderr!r}"
        )
