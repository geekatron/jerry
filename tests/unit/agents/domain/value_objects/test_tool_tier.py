# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for ToolTier value object.

Tests enum membership, from_string() parsing, and calculate_from_tools()
least-privilege inference for all tool combinations.
"""

from __future__ import annotations

import pytest

from src.agents.domain.value_objects.tool_tier import ToolTier

# =============================================================================
# Tests: Enum membership and values
# =============================================================================


class TestToolTierEnum:
    """Verify all five tier members and their string values."""

    @pytest.mark.happy_path
    def test_t1_value(self) -> None:
        """T1 has the canonical string value."""
        assert ToolTier.T1.value == "T1"

    @pytest.mark.happy_path
    def test_t2_value(self) -> None:
        """T2 has the canonical string value."""
        assert ToolTier.T2.value == "T2"

    @pytest.mark.happy_path
    def test_t3_value(self) -> None:
        """T3 has the canonical string value."""
        assert ToolTier.T3.value == "T3"

    @pytest.mark.happy_path
    def test_t4_value(self) -> None:
        """T4 has the canonical string value."""
        assert ToolTier.T4.value == "T4"

    @pytest.mark.happy_path
    def test_t5_value(self) -> None:
        """T5 has the canonical string value."""
        assert ToolTier.T5.value == "T5"

    @pytest.mark.happy_path
    def test_exactly_five_members(self) -> None:
        """Enum contains exactly five members."""
        assert len(list(ToolTier)) == 5

    @pytest.mark.happy_path
    def test_all_values_unique(self) -> None:
        """All tier values are distinct strings."""
        values = [t.value for t in ToolTier]
        assert len(values) == len(set(values))


# =============================================================================
# Tests: from_string() — happy paths and edge cases
# =============================================================================


class TestFromString:
    """ToolTier.from_string() parsing tests."""

    @pytest.mark.happy_path
    def test_t1_exact(self) -> None:
        """Exact 'T1' parses to T1."""
        # Arrange / Act / Assert
        assert ToolTier.from_string("T1") is ToolTier.T1

    @pytest.mark.happy_path
    def test_t2_exact(self) -> None:
        """Exact 'T2' parses to T2."""
        assert ToolTier.from_string("T2") is ToolTier.T2

    @pytest.mark.happy_path
    def test_t3_exact(self) -> None:
        """Exact 'T3' parses to T3."""
        assert ToolTier.from_string("T3") is ToolTier.T3

    @pytest.mark.happy_path
    def test_t4_exact(self) -> None:
        """Exact 'T4' parses to T4."""
        assert ToolTier.from_string("T4") is ToolTier.T4

    @pytest.mark.happy_path
    def test_t5_exact(self) -> None:
        """Exact 'T5' parses to T5."""
        assert ToolTier.from_string("T5") is ToolTier.T5

    @pytest.mark.edge_case
    def test_lowercase_input_normalised(self) -> None:
        """Lowercase input is upper-cased before matching."""
        assert ToolTier.from_string("t1") is ToolTier.T1

    @pytest.mark.edge_case
    def test_mixed_case_input_normalised(self) -> None:
        """Mixed-case input is normalised before matching."""
        assert ToolTier.from_string("t5") is ToolTier.T5

    @pytest.mark.edge_case
    def test_leading_trailing_whitespace_stripped(self) -> None:
        """Leading/trailing whitespace is stripped before matching."""
        assert ToolTier.from_string("  T3  ") is ToolTier.T3

    @pytest.mark.edge_case
    def test_whitespace_and_lowercase_combined(self) -> None:
        """Both stripping and case normalisation apply together."""
        assert ToolTier.from_string("  t4  ") is ToolTier.T4

    # ------------------------------------------------------------------
    # Negative cases
    # ------------------------------------------------------------------

    @pytest.mark.negative
    def test_invalid_string_raises_value_error(self) -> None:
        """Unknown tier name raises ValueError."""
        with pytest.raises(ValueError, match="Invalid tool tier"):
            ToolTier.from_string("T6")

    @pytest.mark.negative
    def test_empty_string_raises_value_error(self) -> None:
        """Empty string is not a valid tier."""
        with pytest.raises(ValueError, match="Invalid tool tier"):
            ToolTier.from_string("")

    @pytest.mark.negative
    def test_whitespace_only_raises_value_error(self) -> None:
        """Whitespace-only string normalises to empty and raises ValueError."""
        with pytest.raises(ValueError, match="Invalid tool tier"):
            ToolTier.from_string("   ")

    @pytest.mark.negative
    def test_numeric_only_raises_value_error(self) -> None:
        """A bare digit is not a valid tier name."""
        with pytest.raises(ValueError, match="Invalid tool tier"):
            ToolTier.from_string("1")

    @pytest.mark.negative
    def test_error_message_lists_valid_tiers(self) -> None:
        """ValueError message includes all valid tier names."""
        with pytest.raises(ValueError) as exc_info:
            ToolTier.from_string("INVALID")
        message = str(exc_info.value)
        for tier in ToolTier:
            assert tier.value in message


# =============================================================================
# Tests: calculate_from_tools() — least-privilege inference
# =============================================================================


class TestCalculateFromTools:
    """ToolTier.calculate_from_tools() minimum tier inference."""

    # --- T1 (read-only) ---------------------------------------------------

    @pytest.mark.happy_path
    def test_no_tools_returns_t1(self) -> None:
        """Empty tool list resolves to T1 (read-only baseline)."""
        # Arrange / Act
        result = ToolTier.calculate_from_tools([])
        # Assert
        assert result is ToolTier.T1

    @pytest.mark.happy_path
    def test_read_only_tools_return_t1(self) -> None:
        """Pure read tools (file_read, file_search_glob, etc.) resolve to T1."""
        result = ToolTier.calculate_from_tools(
            ["file_read", "file_search_glob", "file_search_content"]
        )
        assert result is ToolTier.T1

    # --- T2 (read-write) --------------------------------------------------

    @pytest.mark.happy_path
    def test_file_write_returns_t2(self) -> None:
        """Presence of file_write tool triggers T2."""
        result = ToolTier.calculate_from_tools(["file_read", "file_write"])
        assert result is ToolTier.T2

    @pytest.mark.happy_path
    def test_file_edit_returns_t2(self) -> None:
        """Presence of file_edit tool triggers T2."""
        result = ToolTier.calculate_from_tools(["file_read", "file_edit"])
        assert result is ToolTier.T2

    @pytest.mark.happy_path
    def test_shell_execute_returns_t2(self) -> None:
        """Presence of shell_execute tool triggers T2."""
        result = ToolTier.calculate_from_tools(["shell_execute"])
        assert result is ToolTier.T2

    # --- T3 (external) ----------------------------------------------------

    @pytest.mark.happy_path
    def test_web_search_returns_t3(self) -> None:
        """Presence of web_search triggers T3."""
        result = ToolTier.calculate_from_tools(["file_read", "web_search"])
        assert result is ToolTier.T3

    @pytest.mark.happy_path
    def test_web_fetch_returns_t3(self) -> None:
        """Presence of web_fetch triggers T3."""
        result = ToolTier.calculate_from_tools(["web_fetch"])
        assert result is ToolTier.T3

    @pytest.mark.happy_path
    def test_context7_mcp_server_returns_t3(self) -> None:
        """context7 MCP server triggers T3."""
        result = ToolTier.calculate_from_tools([], mcp_servers=["context7"])
        assert result is ToolTier.T3

    @pytest.mark.edge_case
    def test_write_plus_web_search_returns_t3(self) -> None:
        """T3 (external) dominates T2 (write) when both apply."""
        result = ToolTier.calculate_from_tools(["file_write", "web_search"])
        assert result is ToolTier.T3

    # --- T4 (persistent) --------------------------------------------------

    @pytest.mark.happy_path
    def test_memory_keeper_mcp_returns_t4(self) -> None:
        """memory-keeper MCP server without external tools resolves to T4."""
        result = ToolTier.calculate_from_tools([], mcp_servers=["memory-keeper"])
        assert result is ToolTier.T4

    @pytest.mark.happy_path
    def test_memory_keeper_with_write_tools_returns_t4(self) -> None:
        """memory-keeper plus write tools (but no external) resolves to T4."""
        result = ToolTier.calculate_from_tools(
            ["file_write"],
            mcp_servers=["memory-keeper"],
        )
        assert result is ToolTier.T4

    # --- T5 (full / delegation) -------------------------------------------

    @pytest.mark.happy_path
    def test_agent_delegate_returns_t5(self) -> None:
        """agent_delegate tool always resolves to T5 regardless of others."""
        result = ToolTier.calculate_from_tools(["agent_delegate"])
        assert result is ToolTier.T5

    @pytest.mark.happy_path
    def test_agent_delegate_with_other_tools_returns_t5(self) -> None:
        """T5 when agent_delegate is combined with arbitrary other tools."""
        result = ToolTier.calculate_from_tools(
            ["file_read", "file_write", "web_search", "agent_delegate"],
        )
        assert result is ToolTier.T5

    @pytest.mark.happy_path
    def test_memory_keeper_plus_external_returns_t5(self) -> None:
        """memory-keeper + context7 MCP together resolve to T5."""
        result = ToolTier.calculate_from_tools(
            [],
            mcp_servers=["memory-keeper", "context7"],
        )
        assert result is ToolTier.T5

    @pytest.mark.happy_path
    def test_memory_keeper_plus_web_search_returns_t5(self) -> None:
        """memory-keeper MCP + web_search native tool resolves to T5."""
        result = ToolTier.calculate_from_tools(
            ["web_search"],
            mcp_servers=["memory-keeper"],
        )
        assert result is ToolTier.T5

    # --- Edge cases -------------------------------------------------------

    @pytest.mark.edge_case
    def test_mcp_servers_none_defaults_to_empty(self) -> None:
        """Passing mcp_servers=None is equivalent to an empty list."""
        result_none = ToolTier.calculate_from_tools([], mcp_servers=None)
        result_empty = ToolTier.calculate_from_tools([], mcp_servers=[])
        assert result_none is result_empty

    @pytest.mark.edge_case
    def test_unknown_tool_names_return_t1(self) -> None:
        """Unrecognised tool names do not bump the tier above T1."""
        result = ToolTier.calculate_from_tools(["some_future_tool", "another_tool"])
        assert result is ToolTier.T1

    @pytest.mark.edge_case
    def test_unknown_mcp_server_does_not_bump_tier(self) -> None:
        """Unrecognised MCP server names do not contribute to tier elevation."""
        result = ToolTier.calculate_from_tools([], mcp_servers=["some-future-mcp"])
        assert result is ToolTier.T1

    @pytest.mark.edge_case
    def test_agent_delegate_overrides_everything(self) -> None:
        """agent_delegate in native_tools always wins over MCP servers."""
        result = ToolTier.calculate_from_tools(
            ["agent_delegate"],
            mcp_servers=["memory-keeper", "context7"],
        )
        assert result is ToolTier.T5
