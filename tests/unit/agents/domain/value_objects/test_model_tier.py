# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for ModelTier value object.

Tests enum membership, from_string() parsing, and from_vendor_model()
reverse-mapping across all happy paths, negative cases, and edge cases.
"""

from __future__ import annotations

import pytest

from src.agents.domain.value_objects.model_tier import ModelTier

# =============================================================================
# Tests: Enum membership and values
# =============================================================================


class TestModelTierEnum:
    """Verify the three enum members have expected string values."""

    @pytest.mark.happy_path
    def test_reasoning_high_value(self) -> None:
        """REASONING_HIGH has the canonical string value."""
        # Arrange / Act / Assert
        assert ModelTier.REASONING_HIGH.value == "reasoning_high"

    @pytest.mark.happy_path
    def test_reasoning_standard_value(self) -> None:
        """REASONING_STANDARD has the canonical string value."""
        assert ModelTier.REASONING_STANDARD.value == "reasoning_standard"

    @pytest.mark.happy_path
    def test_fast_value(self) -> None:
        """FAST has the canonical string value."""
        assert ModelTier.FAST.value == "fast"

    @pytest.mark.happy_path
    def test_exactly_three_members(self) -> None:
        """Enum contains exactly the three expected members."""
        members = list(ModelTier)
        assert len(members) == 3

    @pytest.mark.happy_path
    def test_members_are_unique(self) -> None:
        """All enum values are distinct strings."""
        values = [t.value for t in ModelTier]
        assert len(values) == len(set(values))


# =============================================================================
# Tests: from_string() — happy paths
# =============================================================================


class TestFromString:
    """ModelTier.from_string() parsing tests."""

    @pytest.mark.happy_path
    def test_reasoning_high_exact(self) -> None:
        """Exact lowercase string parses to REASONING_HIGH."""
        # Arrange
        raw = "reasoning_high"
        # Act
        result = ModelTier.from_string(raw)
        # Assert
        assert result is ModelTier.REASONING_HIGH

    @pytest.mark.happy_path
    def test_reasoning_standard_exact(self) -> None:
        """Exact lowercase string parses to REASONING_STANDARD."""
        result = ModelTier.from_string("reasoning_standard")
        assert result is ModelTier.REASONING_STANDARD

    @pytest.mark.happy_path
    def test_fast_exact(self) -> None:
        """Exact lowercase string parses to FAST."""
        result = ModelTier.from_string("fast")
        assert result is ModelTier.FAST

    @pytest.mark.edge_case
    def test_uppercase_input(self) -> None:
        """Upper-case input is normalised and parses correctly."""
        result = ModelTier.from_string("REASONING_HIGH")
        assert result is ModelTier.REASONING_HIGH

    @pytest.mark.edge_case
    def test_mixed_case_input(self) -> None:
        """Mixed-case input is normalised and parses correctly."""
        result = ModelTier.from_string("Reasoning_Standard")
        assert result is ModelTier.REASONING_STANDARD

    @pytest.mark.edge_case
    def test_leading_trailing_whitespace(self) -> None:
        """Leading/trailing whitespace is stripped before matching."""
        result = ModelTier.from_string("  fast  ")
        assert result is ModelTier.FAST

    @pytest.mark.edge_case
    def test_whitespace_and_uppercase_combined(self) -> None:
        """Both whitespace stripping and case normalisation apply together."""
        result = ModelTier.from_string("  FAST  ")
        assert result is ModelTier.FAST

    # ------------------------------------------------------------------
    # Negative cases
    # ------------------------------------------------------------------

    @pytest.mark.negative
    def test_invalid_string_raises_value_error(self) -> None:
        """Unknown tier name raises ValueError."""
        with pytest.raises(ValueError, match="Invalid model tier"):
            ModelTier.from_string("ultra")

    @pytest.mark.negative
    def test_empty_string_raises_value_error(self) -> None:
        """Empty string is not a valid tier and raises ValueError."""
        with pytest.raises(ValueError, match="Invalid model tier"):
            ModelTier.from_string("")

    @pytest.mark.negative
    def test_whitespace_only_raises_value_error(self) -> None:
        """Whitespace-only string normalises to empty and raises ValueError."""
        with pytest.raises(ValueError, match="Invalid model tier"):
            ModelTier.from_string("   ")

    @pytest.mark.negative
    def test_partial_match_raises_value_error(self) -> None:
        """Partial tier name is not accepted."""
        with pytest.raises(ValueError, match="Invalid model tier"):
            ModelTier.from_string("reasoning")

    @pytest.mark.negative
    def test_error_message_lists_valid_tiers(self) -> None:
        """ValueError message includes all valid tier names."""
        with pytest.raises(ValueError) as exc_info:
            ModelTier.from_string("bogus")
        message = str(exc_info.value)
        assert "reasoning_high" in message
        assert "reasoning_standard" in message
        assert "fast" in message


# =============================================================================
# Tests: from_vendor_model() — happy paths
# =============================================================================


class TestFromVendorModel:
    """ModelTier.from_vendor_model() reverse-mapping tests."""

    @pytest.mark.happy_path
    def test_claude_code_opus_maps_to_reasoning_high(self) -> None:
        """claude_code / opus resolves to REASONING_HIGH."""
        # Arrange
        vendor, model = "claude_code", "opus"
        # Act
        result = ModelTier.from_vendor_model(vendor, model)
        # Assert
        assert result is ModelTier.REASONING_HIGH

    @pytest.mark.happy_path
    def test_claude_code_sonnet_maps_to_reasoning_standard(self) -> None:
        """claude_code / sonnet resolves to REASONING_STANDARD."""
        result = ModelTier.from_vendor_model("claude_code", "sonnet")
        assert result is ModelTier.REASONING_STANDARD

    @pytest.mark.happy_path
    def test_claude_code_haiku_maps_to_fast(self) -> None:
        """claude_code / haiku resolves to FAST."""
        result = ModelTier.from_vendor_model("claude_code", "haiku")
        assert result is ModelTier.FAST

    @pytest.mark.edge_case
    def test_model_name_uppercase_normalised(self) -> None:
        """Model name is case-normalised before lookup."""
        result = ModelTier.from_vendor_model("claude_code", "OPUS")
        assert result is ModelTier.REASONING_HIGH

    @pytest.mark.edge_case
    def test_model_name_with_whitespace(self) -> None:
        """Model name is whitespace-stripped before lookup."""
        result = ModelTier.from_vendor_model("claude_code", "  sonnet  ")
        assert result is ModelTier.REASONING_STANDARD

    # ------------------------------------------------------------------
    # Negative cases
    # ------------------------------------------------------------------

    @pytest.mark.negative
    def test_unknown_vendor_raises_value_error(self) -> None:
        """Completely unknown vendor raises ValueError."""
        with pytest.raises(ValueError, match="Unknown model"):
            ModelTier.from_vendor_model("openai", "gpt-4o")

    @pytest.mark.negative
    def test_known_vendor_unknown_model_raises_value_error(self) -> None:
        """Known vendor but unrecognised model name raises ValueError."""
        with pytest.raises(ValueError, match="Unknown model"):
            ModelTier.from_vendor_model("claude_code", "claude-3-unknown")

    @pytest.mark.negative
    def test_empty_vendor_raises_value_error(self) -> None:
        """Empty vendor string resolves to empty map and raises ValueError."""
        with pytest.raises(ValueError, match="Unknown model"):
            ModelTier.from_vendor_model("", "opus")

    @pytest.mark.negative
    def test_empty_model_raises_value_error(self) -> None:
        """Empty model name after normalisation is not in the map."""
        with pytest.raises(ValueError, match="Unknown model"):
            ModelTier.from_vendor_model("claude_code", "")

    @pytest.mark.negative
    def test_error_message_mentions_vendor_and_model(self) -> None:
        """ValueError message contains both the vendor and model identifiers."""
        with pytest.raises(ValueError) as exc_info:
            ModelTier.from_vendor_model("claude_code", "nonexistent")
        message = str(exc_info.value)
        assert "nonexistent" in message
        assert "claude_code" in message

    @pytest.mark.edge_case
    def test_future_vendor_unknown_raises_value_error(self) -> None:
        """A vendor not yet in the reverse-map raises ValueError."""
        with pytest.raises(ValueError, match="Unknown model"):
            ModelTier.from_vendor_model("ollama", "llama3.1:70b")
