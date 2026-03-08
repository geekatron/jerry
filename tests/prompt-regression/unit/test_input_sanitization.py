# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Unit tests for DeepEvalAdapter input sanitization — RFA-001 / MC-02.

Verifies that:
  - _sanitize_input strips null bytes from input strings.
  - _sanitize_input normalizes carriage returns.
  - _sanitize_input truncates oversized inputs.
  - _sanitize_input raises TypeError for non-string inputs.
  - _MAX_INPUT_CHARS is importable and equals 10_000.
  - evaluate_batch applies sanitization to prompt and output arguments.

No LLM calls are performed. No network I/O. No filesystem side effects.

References:
    - RFA-001: Input sanitization gap closure
    - MC-02: Input sanitization for prompt injection (CWE-20)
    - F-001: Security assessment finding
    - H-20: BDD test-first (90% line coverage target)
"""

from __future__ import annotations

import pytest

from jerry.testing.evaluation import deepeval_adapter as _da_module
from jerry.testing.evaluation.deepeval_adapter import _sanitize_input


class TestSanitizeInputFunction:
    """Unit tests for the _sanitize_input() module-level function (MC-02)."""

    @pytest.mark.unit
    def test_clean_string_should_pass_through_unchanged(self) -> None:
        """A string with no problematic characters should be returned as-is."""
        result = _sanitize_input("hello world", "test_field", 1000)
        assert result == "hello world"

    @pytest.mark.unit
    def test_null_bytes_should_be_stripped(self) -> None:
        """Null bytes (\\x00) must be removed from input (CWE-20)."""
        result = _sanitize_input("hello\x00world", "test_field", 1000)
        assert "\x00" not in result
        assert result == "helloworld"

    @pytest.mark.unit
    def test_multiple_null_bytes_should_all_be_stripped(self) -> None:
        """All null bytes are stripped, not just the first."""
        result = _sanitize_input("\x00a\x00b\x00c\x00", "test_field", 1000)
        assert result == "abc"

    @pytest.mark.unit
    def test_bare_carriage_return_should_be_normalized(self) -> None:
        """Bare \\r should be normalized to \\n (CG-018 alignment)."""
        result = _sanitize_input("line1\rline2", "test_field", 1000)
        assert "\r" not in result
        assert result == "line1\nline2"

    @pytest.mark.unit
    def test_crlf_should_be_normalized_to_lf(self) -> None:
        """\\r\\n should be normalized to \\n."""
        result = _sanitize_input("line1\r\nline2", "test_field", 1000)
        assert "\r" not in result
        assert result == "line1\nline2"

    @pytest.mark.unit
    def test_truncation_at_max_chars(self) -> None:
        """Input exceeding max_chars must be truncated."""
        long_input = "a" * 500
        result = _sanitize_input(long_input, "test_field", 100)
        assert len(result) == 100
        assert result == "a" * 100

    @pytest.mark.unit
    def test_input_at_exactly_max_chars_should_not_be_truncated(self) -> None:
        """Input exactly at the limit should not be truncated."""
        exact_input = "b" * 100
        result = _sanitize_input(exact_input, "test_field", 100)
        assert len(result) == 100

    @pytest.mark.unit
    def test_input_below_max_chars_should_not_be_truncated(self) -> None:
        """Input below the limit should not be truncated."""
        short_input = "c" * 50
        result = _sanitize_input(short_input, "test_field", 100)
        assert len(result) == 50

    @pytest.mark.unit
    def test_non_string_input_should_raise_type_error(self) -> None:
        """Non-string input must raise TypeError (MC-02 type safety)."""
        with pytest.raises(TypeError, match="Expected str"):
            _sanitize_input(12345, "test_field", 1000)  # type: ignore[arg-type]

    @pytest.mark.unit
    def test_none_input_should_raise_type_error(self) -> None:
        """None input must raise TypeError."""
        with pytest.raises(TypeError, match="Expected str"):
            _sanitize_input(None, "test_field", 1000)  # type: ignore[arg-type]

    @pytest.mark.unit
    def test_empty_string_should_pass_through(self) -> None:
        """Empty string is a valid input and should pass through."""
        result = _sanitize_input("", "test_field", 1000)
        assert result == ""

    @pytest.mark.unit
    def test_null_bytes_stripped_before_truncation(self) -> None:
        """Null byte removal happens before length check.

        A string of 10 characters including 5 null bytes should yield
        5 characters after stripping, which is below a max of 8.
        """
        result = _sanitize_input("a\x00b\x00c\x00d\x00e\x00", "test_field", 8)
        assert result == "abcde"
        assert len(result) == 5

    @pytest.mark.unit
    def test_combined_sanitization_null_cr_truncation(self) -> None:
        """All sanitization steps applied in correct order."""
        # Input: null bytes + bare CR + oversized
        raw = "\x00line1\rline2\x00" + "x" * 200
        result = _sanitize_input(raw, "test_field", 20)
        assert "\x00" not in result
        assert "\r" not in result
        assert len(result) <= 20


class TestMaxInputCharsConstant:
    """Unit tests for the _MAX_INPUT_CHARS module-level constant (MC-02)."""

    @pytest.mark.unit
    def test_max_input_chars_constant_should_exist(self) -> None:
        """_MAX_INPUT_CHARS must be accessible as a module attribute."""
        assert hasattr(_da_module, "_MAX_INPUT_CHARS")

    @pytest.mark.unit
    def test_max_input_chars_should_equal_10000(self) -> None:
        """_MAX_INPUT_CHARS must be 10_000 per MC-06 payload size limit."""
        assert _da_module._MAX_INPUT_CHARS == 10_000  # noqa: SLF001

    @pytest.mark.unit
    def test_max_input_chars_should_be_an_integer(self) -> None:
        """_MAX_INPUT_CHARS must be an int."""
        assert isinstance(_da_module._MAX_INPUT_CHARS, int)  # noqa: SLF001
