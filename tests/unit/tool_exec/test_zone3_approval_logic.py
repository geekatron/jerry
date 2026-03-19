# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""TASK-045: Unit tests for Zone 3 confirmation-phrase matching logic.

These tests exercise the exact-match behaviour of the updated
``_prompt_zone3_approval()`` function without spawning a subprocess or PTY.
The matching predicate is:

    approved = response.strip() == f"APPROVE: {tool_command}"

Key invariants:
- Exact match on the full phrase passes.
- Any deviation — wrong tool, extra whitespace, wrong case, legacy "yes" /
  "y", or empty string — is denied.
- No startswith(), no lower() normalisation.

Tests are pure logic tests: they patch ``builtins.input`` and
``sys.stdin.isatty`` so no I/O or filesystem interaction occurs.

References:
    - TASK-045: Confirmation phrase hardening
    - TASK-046: Audit source field
    - src/interface/cli/tool_exec_commands.py: _prompt_zone3_approval()
    - OWASP A01:2021 Broken Access Control
    - OWASP A07:2021 Identification and Authentication Failures
"""

from __future__ import annotations

from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest

from src.interface.cli.tool_exec_commands import _prompt_zone3_approval

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def mock_engagement_init() -> MagicMock:
    """A minimal EngagementInitializer double that satisfies audit write paths."""
    mock = MagicMock()
    # global_audit_dir() must return a Path-like object whose mkdir() succeeds.
    # We point it at a temp directory supplied by the individual test or a
    # throwaway MagicMock (the audit write is also patched away below).
    mock.global_audit_dir.return_value = MagicMock()
    mock.global_audit_dir.return_value.resolve.return_value = mock.global_audit_dir.return_value
    return mock


@pytest.fixture()
def patch_audit() -> Generator[MagicMock, None, None]:
    """Patch _write_approval_audit so tests never touch the filesystem."""
    with patch(
        "src.interface.cli.tool_exec_commands._write_approval_audit",
        return_value=True,
    ) as mock_audit:
        yield mock_audit


@pytest.fixture()
def patch_tty_interactive() -> Generator[None, None, None]:
    """Make sys.stdin appear to be a real TTY (interactive path)."""
    with patch("sys.stdin") as mock_stdin:
        mock_stdin.isatty.return_value = True
        yield


# ---------------------------------------------------------------------------
# Helper: call the function with a specific input string
# ---------------------------------------------------------------------------


def _call_with_input(
    input_str: str,
    tool_command: str,
    mock_engagement_init: MagicMock,
) -> bool:
    """Invoke _prompt_zone3_approval() with a controlled input() return value.

    Patches sys.stdin.isatty() to return True (interactive) and
    builtins.input to return ``input_str``.

    Args:
        input_str: The string the simulated operator types.
        tool_command: The tool command passed to the gate.
        mock_engagement_init: Audit double from the fixture.

    Returns:
        The bool returned by _prompt_zone3_approval().
    """
    with patch("sys.stdin") as mock_stdin, patch("builtins.input", return_value=input_str):
        mock_stdin.isatty.return_value = True
        return _prompt_zone3_approval(
            tool_command=tool_command,
            zone="Zone 3",
            engagement_id=None,
            engagement_init=mock_engagement_init,
        )


# ---------------------------------------------------------------------------
# TASK-045: Exact-match acceptance
# ---------------------------------------------------------------------------


class TestConfirmationPhraseExactMatch:
    """The gate MUST approve when the operator types the exact phrase."""

    def test_exact_phrase_msfconsole_approved(
        self,
        mock_engagement_init: MagicMock,
        patch_audit: MagicMock,
    ) -> None:
        """'APPROVE: msfconsole' -> approved (exact match, no trailing space)."""
        result = _call_with_input("APPROVE: msfconsole", "msfconsole", mock_engagement_init)
        assert result is True

    def test_exact_phrase_impacket_approved(
        self,
        mock_engagement_init: MagicMock,
        patch_audit: MagicMock,
    ) -> None:
        """'APPROVE: impacket-GetADUsers' -> approved."""
        result = _call_with_input(
            "APPROVE: impacket-GetADUsers", "impacket-GetADUsers", mock_engagement_init
        )
        assert result is True


# ---------------------------------------------------------------------------
# TASK-045: Denial cases
# ---------------------------------------------------------------------------


class TestConfirmationPhraseDenied:
    """Any deviation from the exact phrase MUST result in denial."""

    def test_wrong_tool_name_denied(
        self,
        mock_engagement_init: MagicMock,
        patch_audit: MagicMock,
    ) -> None:
        """'APPROVE: wrong' does not match 'APPROVE: msfconsole' -> denied."""
        result = _call_with_input("APPROVE: wrong", "msfconsole", mock_engagement_init)
        assert result is False

    def test_legacy_yes_denied(
        self,
        mock_engagement_init: MagicMock,
        patch_audit: MagicMock,
    ) -> None:
        """Legacy 'yes' response MUST be denied after TASK-045 hardening."""
        result = _call_with_input("yes", "msfconsole", mock_engagement_init)
        assert result is False

    def test_legacy_y_denied(
        self,
        mock_engagement_init: MagicMock,
        patch_audit: MagicMock,
    ) -> None:
        """Legacy 'y' response MUST be denied (was previously accepted)."""
        result = _call_with_input("y", "msfconsole", mock_engagement_init)
        assert result is False

    def test_internal_space_after_colon_denied(
        self,
        mock_engagement_init: MagicMock,
        patch_audit: MagicMock,
    ) -> None:
        """Extra internal space ('APPROVE:  msfconsole') is NOT an exact match -> denied.

        response.strip() only removes leading/trailing whitespace from the raw
        operator input.  Internal whitespace differences (e.g., double space
        after the colon) are NOT collapsed, so the phrase does not match.
        """
        result = _call_with_input("APPROVE:  msfconsole", "msfconsole", mock_engagement_init)
        assert result is False

    def test_case_variation_lowercase_approve_denied(
        self,
        mock_engagement_init: MagicMock,
        patch_audit: MagicMock,
    ) -> None:
        """'approve: msfconsole' (lowercase) MUST be denied — case-sensitive."""
        result = _call_with_input("approve: msfconsole", "msfconsole", mock_engagement_init)
        assert result is False

    def test_empty_string_denied(
        self,
        mock_engagement_init: MagicMock,
        patch_audit: MagicMock,
    ) -> None:
        """Empty string MUST be denied."""
        result = _call_with_input("", "msfconsole", mock_engagement_init)
        assert result is False

    def test_approve_prefix_only_denied(
        self,
        mock_engagement_init: MagicMock,
        patch_audit: MagicMock,
    ) -> None:
        """'APPROVE:' without the tool name MUST be denied."""
        result = _call_with_input("APPROVE:", "msfconsole", mock_engagement_init)
        assert result is False

    def test_no_tty_auto_denied(
        self,
        mock_engagement_init: MagicMock,
        patch_audit: MagicMock,
    ) -> None:
        """Non-interactive stdin (no TTY) auto-denies without calling input()."""
        with patch("sys.stdin") as mock_stdin, patch("builtins.input") as mock_input:
            mock_stdin.isatty.return_value = False
            result = _prompt_zone3_approval(
                tool_command="msfconsole",
                zone="Zone 3",
                engagement_id=None,
                engagement_init=mock_engagement_init,
            )
        assert result is False
        mock_input.assert_not_called()


# ---------------------------------------------------------------------------
# TASK-045: Audit record contains confirmation_input and expected_phrase
# ---------------------------------------------------------------------------


class TestConfirmationPhraseAuditFields:
    """Audit records must include the operator's raw input and the expected phrase."""

    def test_approved_audit_includes_confirmation_fields(
        self,
        mock_engagement_init: MagicMock,
    ) -> None:
        """On approval, audit receives confirmation_input and expected_phrase."""
        with (
            patch(
                "src.interface.cli.tool_exec_commands._write_approval_audit",
                return_value=True,
            ) as mock_audit,
            patch("sys.stdin") as mock_stdin,
            patch("builtins.input", return_value="APPROVE: msfconsole"),
        ):
            mock_stdin.isatty.return_value = True
            _prompt_zone3_approval(
                tool_command="msfconsole",
                zone="Zone 3",
                engagement_id=None,
                engagement_init=mock_engagement_init,
            )

        mock_audit.assert_called_once()
        call_kwargs = mock_audit.call_args.kwargs
        assert call_kwargs["confirmation_input"] == "APPROVE: msfconsole"
        assert call_kwargs["expected_phrase"] == "APPROVE: msfconsole"

    def test_denied_audit_includes_confirmation_fields(
        self,
        mock_engagement_init: MagicMock,
    ) -> None:
        """On denial (wrong phrase), audit still receives both fields."""
        with (
            patch(
                "src.interface.cli.tool_exec_commands._write_approval_audit",
                return_value=True,
            ) as mock_audit,
            patch("sys.stdin") as mock_stdin,
            patch("builtins.input", return_value="yes"),
        ):
            mock_stdin.isatty.return_value = True
            _prompt_zone3_approval(
                tool_command="msfconsole",
                zone="Zone 3",
                engagement_id=None,
                engagement_init=mock_engagement_init,
            )

        mock_audit.assert_called_once()
        call_kwargs = mock_audit.call_args.kwargs
        assert call_kwargs["confirmation_input"] == "yes"
        assert call_kwargs["expected_phrase"] == "APPROVE: msfconsole"
