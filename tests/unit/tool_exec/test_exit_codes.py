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

    def test_exit_code_is_int(self) -> None:
        """ExitCode values can be used as integers."""
        assert isinstance(ExitCode.SUCCESS, int)
        assert ExitCode.TOOL_ERROR + 1 == 3

    def test_core_codes_below_ten(self) -> None:
        """All core exit codes are below 10 (10+ reserved for families)."""
        for code in ExitCode:
            assert code.value < 10
