# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for VendorTarget value object.

Tests enum membership and from_string() parsing across all happy paths,
negative cases, and edge cases (case normalisation, whitespace stripping).
"""

from __future__ import annotations

import pytest

from src.agents.domain.value_objects.vendor_target import VendorTarget

# =============================================================================
# Tests: Enum membership and values
# =============================================================================


class TestVendorTargetEnum:
    """Verify all four vendor members and their string values."""

    @pytest.mark.happy_path
    def test_claude_code_value(self) -> None:
        """CLAUDE_CODE has the canonical string value."""
        assert VendorTarget.CLAUDE_CODE.value == "claude_code"

    @pytest.mark.happy_path
    def test_openai_value(self) -> None:
        """OPENAI has the canonical string value."""
        assert VendorTarget.OPENAI.value == "openai"

    @pytest.mark.happy_path
    def test_google_adk_value(self) -> None:
        """GOOGLE_ADK has the canonical string value."""
        assert VendorTarget.GOOGLE_ADK.value == "google_adk"

    @pytest.mark.happy_path
    def test_ollama_value(self) -> None:
        """OLLAMA has the canonical string value."""
        assert VendorTarget.OLLAMA.value == "ollama"

    @pytest.mark.happy_path
    def test_exactly_four_members(self) -> None:
        """Enum contains exactly four members."""
        assert len(list(VendorTarget)) == 4

    @pytest.mark.happy_path
    def test_all_values_unique(self) -> None:
        """All vendor values are distinct strings."""
        values = [v.value for v in VendorTarget]
        assert len(values) == len(set(values))


# =============================================================================
# Tests: from_string() — happy paths
# =============================================================================


class TestFromString:
    """VendorTarget.from_string() parsing tests."""

    @pytest.mark.happy_path
    def test_claude_code_exact(self) -> None:
        """Exact 'claude_code' parses to CLAUDE_CODE."""
        # Arrange / Act / Assert
        assert VendorTarget.from_string("claude_code") is VendorTarget.CLAUDE_CODE

    @pytest.mark.happy_path
    def test_openai_exact(self) -> None:
        """Exact 'openai' parses to OPENAI."""
        assert VendorTarget.from_string("openai") is VendorTarget.OPENAI

    @pytest.mark.happy_path
    def test_google_adk_exact(self) -> None:
        """Exact 'google_adk' parses to GOOGLE_ADK."""
        assert VendorTarget.from_string("google_adk") is VendorTarget.GOOGLE_ADK

    @pytest.mark.happy_path
    def test_ollama_exact(self) -> None:
        """Exact 'ollama' parses to OLLAMA."""
        assert VendorTarget.from_string("ollama") is VendorTarget.OLLAMA

    # ------------------------------------------------------------------
    # Edge cases: case normalisation
    # ------------------------------------------------------------------

    @pytest.mark.edge_case
    def test_claude_code_uppercase(self) -> None:
        """Uppercase 'CLAUDE_CODE' is normalised and parses correctly."""
        assert VendorTarget.from_string("CLAUDE_CODE") is VendorTarget.CLAUDE_CODE

    @pytest.mark.edge_case
    def test_openai_uppercase(self) -> None:
        """Uppercase 'OPENAI' is normalised and parses correctly."""
        assert VendorTarget.from_string("OPENAI") is VendorTarget.OPENAI

    @pytest.mark.edge_case
    def test_google_adk_uppercase(self) -> None:
        """Uppercase 'GOOGLE_ADK' is normalised and parses correctly."""
        assert VendorTarget.from_string("GOOGLE_ADK") is VendorTarget.GOOGLE_ADK

    @pytest.mark.edge_case
    def test_ollama_uppercase(self) -> None:
        """Uppercase 'OLLAMA' is normalised and parses correctly."""
        assert VendorTarget.from_string("OLLAMA") is VendorTarget.OLLAMA

    @pytest.mark.edge_case
    def test_mixed_case_claude_code(self) -> None:
        """Mixed-case 'Claude_Code' is normalised correctly."""
        assert VendorTarget.from_string("Claude_Code") is VendorTarget.CLAUDE_CODE

    # ------------------------------------------------------------------
    # Edge cases: whitespace stripping
    # ------------------------------------------------------------------

    @pytest.mark.edge_case
    def test_leading_whitespace_stripped(self) -> None:
        """Leading whitespace is stripped before matching."""
        assert VendorTarget.from_string("  claude_code") is VendorTarget.CLAUDE_CODE

    @pytest.mark.edge_case
    def test_trailing_whitespace_stripped(self) -> None:
        """Trailing whitespace is stripped before matching."""
        assert VendorTarget.from_string("ollama  ") is VendorTarget.OLLAMA

    @pytest.mark.edge_case
    def test_whitespace_and_case_combined(self) -> None:
        """Both whitespace stripping and case normalisation apply together."""
        assert VendorTarget.from_string("  OPENAI  ") is VendorTarget.OPENAI

    # ------------------------------------------------------------------
    # Negative cases
    # ------------------------------------------------------------------

    @pytest.mark.negative
    def test_unknown_vendor_raises_value_error(self) -> None:
        """Unknown vendor name raises ValueError with a descriptive message."""
        with pytest.raises(ValueError, match="Invalid vendor target"):
            VendorTarget.from_string("anthropic")

    @pytest.mark.negative
    def test_empty_string_raises_value_error(self) -> None:
        """Empty string is not a valid vendor target."""
        with pytest.raises(ValueError, match="Invalid vendor target"):
            VendorTarget.from_string("")

    @pytest.mark.negative
    def test_whitespace_only_raises_value_error(self) -> None:
        """Whitespace-only string normalises to empty and raises ValueError."""
        with pytest.raises(ValueError, match="Invalid vendor target"):
            VendorTarget.from_string("   ")

    @pytest.mark.negative
    def test_partial_name_raises_value_error(self) -> None:
        """Partial vendor name ('claude') is not accepted."""
        with pytest.raises(ValueError, match="Invalid vendor target"):
            VendorTarget.from_string("claude")

    @pytest.mark.negative
    def test_hyphenated_variant_raises_value_error(self) -> None:
        """Hyphenated variant ('claude-code') is not accepted (expects underscore)."""
        with pytest.raises(ValueError, match="Invalid vendor target"):
            VendorTarget.from_string("claude-code")

    @pytest.mark.negative
    def test_error_message_lists_all_valid_targets(self) -> None:
        """ValueError message includes all valid vendor target names."""
        with pytest.raises(ValueError) as exc_info:
            VendorTarget.from_string("cohere")
        message = str(exc_info.value)
        assert "claude_code" in message
        assert "openai" in message
        assert "google_adk" in message
        assert "ollama" in message

    @pytest.mark.negative
    def test_numeric_string_raises_value_error(self) -> None:
        """Numeric string is not a valid vendor target."""
        with pytest.raises(ValueError, match="Invalid vendor target"):
            VendorTarget.from_string("42")
