# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for ExitCode enumeration."""

from __future__ import annotations

from src.tool_exec.domain.value_objects.exit_codes import ExitCode


class TestExitCode:
    """Tests for ExitCode values and behavior."""

    def test_success_is_zero(self) -> None:
        """SUCCESS exit code is 0."""
        assert ExitCode.SUCCESS == 0

    def test_all_exit_codes_are_distinct(self) -> None:
        """All exit codes have unique values."""
        values = [e.value for e in ExitCode]
        assert len(values) == len(set(values))

    def test_exit_code_values_match_bash_contract(self) -> None:
        """Exit codes match the ADR-PROJ023-001 behavioral contract."""
        assert ExitCode.SUCCESS == 0
        assert ExitCode.UNKNOWN_TOOL == 1
        assert ExitCode.TOOL_ERROR == 2
        assert ExitCode.CONTAINER_NOT_RUNNING == 3
        assert ExitCode.CREDENTIAL_DETECTED == 4
        assert ExitCode.ENGAGEMENT_NOT_INIT == 5
        assert ExitCode.MODE_UNSET == 6

    def test_fix6_family_not_found_is_seven(self) -> None:
        """CV-008 (FIX-6): FAMILY_NOT_FOUND is exit code 7."""
        assert ExitCode.FAMILY_NOT_FOUND == 7

    def test_fix6_family_config_error_is_eight(self) -> None:
        """CV-009 (FIX-6): FAMILY_CONFIG_ERROR is exit code 8."""
        assert ExitCode.FAMILY_CONFIG_ERROR == 8

    def test_strict_mode_violation_is_nine(self) -> None:
        """M-03: STRICT_MODE_VIOLATION is exit code 9."""
        assert ExitCode.STRICT_MODE_VIOLATION == 9

    def test_zone3_container_required_is_ten(self) -> None:
        """FM-002 (FIX-3): ZONE3_CONTAINER_REQUIRED is exit code 10."""
        assert ExitCode.ZONE3_CONTAINER_REQUIRED == 10

    def test_exit_code_is_int(self) -> None:
        """ExitCode values can be used as integers."""
        assert isinstance(ExitCode.SUCCESS, int)
        assert ExitCode.TOOL_ERROR + 1 == 3

    def test_core_codes_below_twelve(self) -> None:
        """All core exit codes are below 12 (12+ reserved for families).

        CV-008/CV-009 (FIX-6) added FAMILY_NOT_FOUND=7, FAMILY_CONFIG_ERROR=8.
        M-03 renumbered STRICT_MODE_VIOLATION to 9.
        FM-002 (FIX-3) added ZONE3_CONTAINER_REQUIRED=10.
        IN-015-R2/NEW-001 added ZONE3_APPROVAL_DENIED=11.
        Family-specific codes begin at 12.
        """
        for code in ExitCode:
            assert code.value < 12, f"Unexpected high exit code: {code.name}={code.value}"

    def test_zone3_approval_denied_is_eleven(self) -> None:
        """IN-015-R2/NEW-001: ZONE3_APPROVAL_DENIED is exit code 11."""
        assert ExitCode.ZONE3_APPROVAL_DENIED == 11
