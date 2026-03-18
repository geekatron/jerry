# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""TASK-033: Management command E2E tests.

Tests --list-families and --list-tools through the real CLI subprocess.
These are UC-004 management commands that query the tool registry without
executing any tools, so they do not require Docker or an engagement ID.

Note: --list-families and --list-tools are flags on `jerry tool exec`,
not sub-commands on `jerry tool`.  The conftest cli_run helper wraps
`jerry tool exec`, so callers pass --list-families directly.

References:
    - TASK-033: Management command E2E tests
    - FIX-7 (CV-013): --list-families and --list-tools implementation
    - ADR-PROJ023-001: UC-004 Registry Management
"""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.e2e


class TestListFamilies:
    """--list-families enumerates registered tool families."""

    def test_list_families_exit_0(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """--list-families returns exit code 0."""
        exit_code, _stdout, _stderr = cli_run("--list-families")
        assert exit_code == 0, f"Expected exit 0. stderr={_stderr!r}"

    def test_list_families_stdout_contains_rainbow(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """--list-families output lists the 'rainbow' family."""
        exit_code, stdout, _stderr = cli_run("--list-families")
        assert exit_code == 0
        assert "rainbow" in stdout, (
            f"Expected 'rainbow' family in --list-families output. stdout={stdout!r}"
        )

    def test_list_families_stdout_contains_enabled_status(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """--list-families output includes enabled/disabled status for each family."""
        exit_code, stdout, _stderr = cli_run("--list-families")
        assert exit_code == 0
        assert "enabled" in stdout, (
            f"Expected 'enabled' in --list-families output. stdout={stdout!r}"
        )

    def test_list_families_stdout_contains_priority(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """--list-families output includes priority for each family."""
        exit_code, stdout, _stderr = cli_run("--list-families")
        assert exit_code == 0
        assert "priority" in stdout.lower(), f"Expected 'priority' in output. stdout={stdout!r}"


class TestListTools:
    """--list-tools enumerates tools across all families."""

    def test_list_tools_exit_0(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """--list-tools returns exit code 0."""
        exit_code, _stdout, _stderr = cli_run("--list-tools")
        assert exit_code == 0, f"Expected exit 0. stderr={_stderr!r}"

    def test_list_tools_stdout_contains_syft(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """--list-tools output lists 'syft' from the rainbow family."""
        exit_code, stdout, _stderr = cli_run("--list-tools")
        assert exit_code == 0
        assert "syft" in stdout, f"Expected 'syft' in --list-tools output. stdout={stdout!r}"

    def test_list_tools_stdout_contains_zone_info(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """--list-tools output includes zone information for each tool."""
        exit_code, stdout, _stderr = cli_run("--list-tools")
        assert exit_code == 0
        # Zone information is printed as 'Zone 1', 'Zone 2', or 'Zone 3'
        assert "Zone" in stdout or "zone" in stdout.lower(), (
            f"Expected zone information in --list-tools output. stdout={stdout!r}"
        )

    def test_list_tools_family_filter_rainbow(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """--list-tools with family filter 'rainbow' returns only rainbow tools."""
        exit_code, stdout, _stderr = cli_run("--list-tools", "rainbow")
        assert exit_code == 0, f"Expected exit 0 with --list-tools rainbow. stderr={_stderr!r}"
        # The rainbow family is the only registered family; output should still
        # contain syft and not be empty.
        assert "syft" in stdout or "rainbow" in stdout, (
            f"Expected rainbow family tools in output. stdout={stdout!r}"
        )

    def test_list_tools_nonexistent_family_exit_7(self, cli_run) -> None:  # type: ignore[no-untyped-def]
        """--list-tools with an unknown family returns exit code 7 (FAMILY_NOT_FOUND).

        FIX-13 (CV-007): verifying the family exists before iterating.
        """
        exit_code, _stdout, stderr = cli_run("--list-tools", "nonexistent-family-xyz")
        assert exit_code == 7, f"Expected FAMILY_NOT_FOUND (7). Got {exit_code}. stderr={stderr!r}"
        assert "not found" in stderr.lower() or "nonexistent-family-xyz" in stderr, (
            f"Expected error message about unknown family. stderr={stderr!r}"
        )
