# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Tests for ToolMapper domain service.

Coverage targets:
- map_tool(): happy path (vendor name returned), None for unsupported vendor,
  ValueError for unknown abstract name
- map_tools(): filters None entries, preserves order
- map_model(): all three tiers across vendors, unknown tier returns None
- reverse_map_tool(): found and not-found
- reverse_map_tools(): filters unrecognized, preserves order
- substitute_tool_names_in_text(): forward and reverse substitution
- from_mappings(): factory constructor, missing keys default to empty dicts
- Edge cases: empty tool_map, tool entry with all-None vendors
"""

from __future__ import annotations

import pytest

from src.agents.domain.services.tool_mapper import ToolMapper
from src.agents.domain.value_objects.model_tier import ModelTier
from src.agents.domain.value_objects.vendor_target import VendorTarget

# ---------------------------------------------------------------------------
# map_tool()
# ---------------------------------------------------------------------------


class TestMapTool:
    """Tests for ToolMapper.map_tool()."""

    def test_known_tool_claude_code_returns_vendor_name(self, tool_mapper: ToolMapper) -> None:
        # Arrange / Act
        result = tool_mapper.map_tool("file_read", VendorTarget.CLAUDE_CODE)

        # Assert
        assert result == "Read"

    def test_known_tool_openai_returns_vendor_name(self, tool_mapper: ToolMapper) -> None:
        # Arrange / Act
        result = tool_mapper.map_tool("shell_execute", VendorTarget.OPENAI)

        # Assert
        assert result == "code_interpreter"

    def test_tool_not_supported_by_vendor_returns_none(self, tool_mapper: ToolMapper) -> None:
        # Arrange – file_write has openai=None in the fixture
        result = tool_mapper.map_tool("file_write", VendorTarget.OPENAI)

        # Assert
        assert result is None

    def test_tool_not_supported_by_ollama_returns_none(self, tool_mapper: ToolMapper) -> None:
        # Arrange – all tools have ollama=None in the fixture
        result = tool_mapper.map_tool("file_read", VendorTarget.OLLAMA)

        # Assert
        assert result is None

    def test_unknown_abstract_tool_raises_value_error(self, tool_mapper: ToolMapper) -> None:
        # Arrange / Act / Assert
        with pytest.raises(ValueError, match="Unknown abstract tool"):
            tool_mapper.map_tool("nonexistent_tool", VendorTarget.CLAUDE_CODE)

    def test_error_message_includes_known_tools_list(self, tool_mapper: ToolMapper) -> None:
        # Arrange / Act
        with pytest.raises(ValueError) as exc_info:
            tool_mapper.map_tool("no_such_tool", VendorTarget.CLAUDE_CODE)

        # Assert – error message lists known tool names
        assert "file_read" in str(exc_info.value)

    def test_agent_delegate_maps_to_task_for_claude(self, tool_mapper: ToolMapper) -> None:
        # Arrange / Act
        result = tool_mapper.map_tool("agent_delegate", VendorTarget.CLAUDE_CODE)

        # Assert
        assert result == "Task"

    def test_web_search_maps_to_web_search_openai(self, tool_mapper: ToolMapper) -> None:
        # Arrange / Act
        result = tool_mapper.map_tool("web_search", VendorTarget.OPENAI)

        # Assert
        assert result == "web_search"


# ---------------------------------------------------------------------------
# map_tools()
# ---------------------------------------------------------------------------


class TestMapTools:
    """Tests for ToolMapper.map_tools()."""

    def test_supported_tools_all_mapped(self, tool_mapper: ToolMapper) -> None:
        # Arrange
        abstract_names = ["file_read", "file_write", "file_edit"]

        # Act
        result = tool_mapper.map_tools(abstract_names, VendorTarget.CLAUDE_CODE)

        # Assert
        assert result == ["Read", "Write", "Edit"]

    def test_unsupported_tools_filtered_out(self, tool_mapper: ToolMapper) -> None:
        # Arrange – file_write and file_edit have openai=None; file_read maps to file_search
        abstract_names = ["file_read", "file_write", "file_edit"]

        # Act
        result = tool_mapper.map_tools(abstract_names, VendorTarget.OPENAI)

        # Assert – only file_read (maps to "file_search") survives
        assert result == ["file_search"]

    def test_empty_list_returns_empty_list(self, tool_mapper: ToolMapper) -> None:
        # Arrange / Act
        result = tool_mapper.map_tools([], VendorTarget.CLAUDE_CODE)

        # Assert
        assert result == []

    def test_all_none_vendor_returns_empty_list(self, tool_mapper: ToolMapper) -> None:
        # Arrange – all tools in the fixture have ollama=None
        abstract_names = ["file_read", "file_write", "shell_execute"]

        # Act
        result = tool_mapper.map_tools(abstract_names, VendorTarget.OLLAMA)

        # Assert
        assert result == []

    def test_preserves_order_of_supported_tools(self, tool_mapper: ToolMapper) -> None:
        # Arrange
        abstract_names = ["shell_execute", "web_search", "file_read"]

        # Act
        result = tool_mapper.map_tools(abstract_names, VendorTarget.CLAUDE_CODE)

        # Assert – Bash, WebSearch, Read in that order
        assert result == ["Bash", "WebSearch", "Read"]

    def test_unknown_tool_propagates_value_error(self, tool_mapper: ToolMapper) -> None:
        # Arrange / Act / Assert
        with pytest.raises(ValueError, match="Unknown abstract tool"):
            tool_mapper.map_tools(["file_read", "bogus"], VendorTarget.CLAUDE_CODE)


# ---------------------------------------------------------------------------
# map_model()
# ---------------------------------------------------------------------------


class TestMapModel:
    """Tests for ToolMapper.map_model()."""

    def test_reasoning_high_maps_to_opus_for_claude(self, tool_mapper: ToolMapper) -> None:
        # Arrange / Act
        result = tool_mapper.map_model(ModelTier.REASONING_HIGH, VendorTarget.CLAUDE_CODE)

        # Assert
        assert result == "opus"

    def test_reasoning_standard_maps_to_sonnet_for_claude(self, tool_mapper: ToolMapper) -> None:
        # Arrange / Act
        result = tool_mapper.map_model(ModelTier.REASONING_STANDARD, VendorTarget.CLAUDE_CODE)

        # Assert
        assert result == "sonnet"

    def test_fast_maps_to_haiku_for_claude(self, tool_mapper: ToolMapper) -> None:
        # Arrange / Act
        result = tool_mapper.map_model(ModelTier.FAST, VendorTarget.CLAUDE_CODE)

        # Assert
        assert result == "haiku"

    def test_reasoning_high_maps_to_gpt4o_for_openai(self, tool_mapper: ToolMapper) -> None:
        # Arrange / Act
        result = tool_mapper.map_model(ModelTier.REASONING_HIGH, VendorTarget.OPENAI)

        # Assert
        assert result == "gpt-4o"

    def test_reasoning_high_maps_for_ollama(self, tool_mapper: ToolMapper) -> None:
        # Arrange / Act
        result = tool_mapper.map_model(ModelTier.REASONING_HIGH, VendorTarget.OLLAMA)

        # Assert
        assert result == "llama3.1:70b"

    def test_unknown_vendor_returns_none(self, tool_mapper: ToolMapper) -> None:
        # Arrange – google_adk is not in the model_map fixture
        result = tool_mapper.map_model(ModelTier.REASONING_HIGH, VendorTarget.GOOGLE_ADK)

        # Assert
        assert result is None

    def test_model_map_missing_tier_returns_none(self) -> None:
        # Arrange – ToolMapper with empty model_map
        mapper = ToolMapper(tool_map={}, model_map={})

        # Act
        result = mapper.map_model(ModelTier.FAST, VendorTarget.CLAUDE_CODE)

        # Assert
        assert result is None


# ---------------------------------------------------------------------------
# reverse_map_tool()
# ---------------------------------------------------------------------------


class TestReverseMapTool:
    """Tests for ToolMapper.reverse_map_tool()."""

    def test_vendor_name_found_returns_abstract_name(self, tool_mapper: ToolMapper) -> None:
        # Arrange / Act
        result = tool_mapper.reverse_map_tool("Read", VendorTarget.CLAUDE_CODE)

        # Assert
        assert result == "file_read"

    def test_task_maps_back_to_agent_delegate(self, tool_mapper: ToolMapper) -> None:
        # Arrange / Act
        result = tool_mapper.reverse_map_tool("Task", VendorTarget.CLAUDE_CODE)

        # Assert
        assert result == "agent_delegate"

    def test_unknown_vendor_name_returns_none(self, tool_mapper: ToolMapper) -> None:
        # Arrange / Act
        result = tool_mapper.reverse_map_tool("NonExistentTool", VendorTarget.CLAUDE_CODE)

        # Assert
        assert result is None

    def test_vendor_name_for_different_vendor_not_found(self, tool_mapper: ToolMapper) -> None:
        # Arrange – "Read" is claude_code only; searching openai should return None
        result = tool_mapper.reverse_map_tool("Read", VendorTarget.OPENAI)

        # Assert
        assert result is None

    def test_openai_code_interpreter_maps_to_shell_execute(self, tool_mapper: ToolMapper) -> None:
        # Arrange / Act
        result = tool_mapper.reverse_map_tool("code_interpreter", VendorTarget.OPENAI)

        # Assert
        assert result == "shell_execute"

    def test_empty_tool_map_returns_none(self) -> None:
        # Arrange
        mapper = ToolMapper(tool_map={}, model_map={})

        # Act
        result = mapper.reverse_map_tool("Read", VendorTarget.CLAUDE_CODE)

        # Assert
        assert result is None


# ---------------------------------------------------------------------------
# reverse_map_tools()
# ---------------------------------------------------------------------------


class TestReverseMapTools:
    """Tests for ToolMapper.reverse_map_tools()."""

    def test_known_vendor_names_all_mapped(self, tool_mapper: ToolMapper) -> None:
        # Arrange
        vendor_names = ["Read", "Write", "Edit"]

        # Act
        result = tool_mapper.reverse_map_tools(vendor_names, VendorTarget.CLAUDE_CODE)

        # Assert
        assert result == ["file_read", "file_write", "file_edit"]

    def test_unrecognized_names_filtered_out(self, tool_mapper: ToolMapper) -> None:
        # Arrange
        vendor_names = ["Read", "SomeUnknownTool", "Bash"]

        # Act
        result = tool_mapper.reverse_map_tools(vendor_names, VendorTarget.CLAUDE_CODE)

        # Assert – only recognized names returned
        assert "file_read" in result
        assert "shell_execute" in result
        assert len(result) == 2

    def test_empty_list_returns_empty_list(self, tool_mapper: ToolMapper) -> None:
        # Arrange / Act
        result = tool_mapper.reverse_map_tools([], VendorTarget.CLAUDE_CODE)

        # Assert
        assert result == []

    def test_all_unrecognized_returns_empty_list(self, tool_mapper: ToolMapper) -> None:
        # Arrange
        vendor_names = ["Alpha", "Beta", "Gamma"]

        # Act
        result = tool_mapper.reverse_map_tools(vendor_names, VendorTarget.CLAUDE_CODE)

        # Assert
        assert result == []

    def test_openai_vendor_names_reverse_mapped(self, tool_mapper: ToolMapper) -> None:
        # Arrange
        vendor_names = ["file_search", "code_interpreter", "web_search"]

        # Act
        result = tool_mapper.reverse_map_tools(vendor_names, VendorTarget.OPENAI)

        # Assert – file_search matches both file_read and file_search_content;
        # reverse_map_tool returns the first match found during dict iteration.
        # We assert at least some matches are returned.
        assert len(result) >= 2

    def test_preserves_order(self, tool_mapper: ToolMapper) -> None:
        # Arrange
        vendor_names = ["Bash", "Glob", "Grep"]

        # Act
        result = tool_mapper.reverse_map_tools(vendor_names, VendorTarget.CLAUDE_CODE)

        # Assert
        assert result == ["shell_execute", "file_search_glob", "file_search_content"]


# ---------------------------------------------------------------------------
# substitute_tool_names_in_text()
# ---------------------------------------------------------------------------


class TestSubstituteToolNamesInText:
    """Tests for ToolMapper.substitute_tool_names_in_text()."""

    def test_forward_substitution_replaces_abstract_with_vendor(
        self, tool_mapper: ToolMapper
    ) -> None:
        # Arrange
        text = "Use file_read to load content."

        # Act
        result = tool_mapper.substitute_tool_names_in_text(text, VendorTarget.CLAUDE_CODE)

        # Assert
        assert "Read" in result
        assert "file_read" not in result

    def test_reverse_substitution_replaces_vendor_with_abstract(
        self, tool_mapper: ToolMapper
    ) -> None:
        # Arrange
        text = "Use Read to load content."

        # Act
        result = tool_mapper.substitute_tool_names_in_text(
            text, VendorTarget.CLAUDE_CODE, reverse=True
        )

        # Assert
        assert "file_read" in result
        assert "Read" not in result

    def test_text_with_no_tool_names_unchanged(self, tool_mapper: ToolMapper) -> None:
        # Arrange
        text = "This text has no tool references at all."

        # Act
        result = tool_mapper.substitute_tool_names_in_text(text, VendorTarget.CLAUDE_CODE)

        # Assert
        assert result == text

    def test_empty_text_returns_empty_string(self, tool_mapper: ToolMapper) -> None:
        # Arrange / Act
        result = tool_mapper.substitute_tool_names_in_text("", VendorTarget.CLAUDE_CODE)

        # Assert
        assert result == ""

    def test_unsupported_vendor_tools_not_substituted(self, tool_mapper: ToolMapper) -> None:
        # Arrange – ollama has no tool mappings, so nothing should be replaced
        text = "Use file_read to load."

        # Act
        result = tool_mapper.substitute_tool_names_in_text(text, VendorTarget.OLLAMA)

        # Assert – no substitution happens because all ollama mappings are None
        assert result == text

    def test_multiple_tool_names_all_substituted(self, tool_mapper: ToolMapper) -> None:
        # Arrange
        text = "Use file_read then file_write then shell_execute."

        # Act
        result = tool_mapper.substitute_tool_names_in_text(text, VendorTarget.CLAUDE_CODE)

        # Assert
        assert "Read" in result
        assert "Write" in result
        assert "Bash" in result

    def test_longer_names_replaced_before_shorter_to_avoid_partials(
        self, tool_mapper: ToolMapper
    ) -> None:
        # Arrange – file_search_content is longer than file_search_glob;
        # both start with "file_search". Longest-first ordering prevents
        # "file_search" prefix from matching inside "file_search_content".
        text = "Use file_search_glob and file_search_content."

        # Act
        result = tool_mapper.substitute_tool_names_in_text(text, VendorTarget.CLAUDE_CODE)

        # Assert – both replaced; no leftover "file_search_*" fragments
        assert "file_search_glob" not in result
        assert "file_search_content" not in result

    def test_forward_default_reverse_false(self, tool_mapper: ToolMapper) -> None:
        # Arrange – default should be forward substitution (reverse=False)
        text = "agent_delegate is used for orchestration."

        # Act
        result = tool_mapper.substitute_tool_names_in_text(text, VendorTarget.CLAUDE_CODE)

        # Assert – agent_delegate replaced with Task
        assert "Task" in result
        assert "agent_delegate" not in result


# ---------------------------------------------------------------------------
# from_mappings() factory constructor
# ---------------------------------------------------------------------------


class TestFromMappings:
    """Tests for ToolMapper.from_mappings() factory class method."""

    def test_from_mappings_with_full_dict(
        self,
        sample_tool_map: dict,
        sample_model_map: dict,
    ) -> None:
        # Arrange
        mappings = {"tool_map": sample_tool_map, "model_map": sample_model_map}

        # Act
        mapper = ToolMapper.from_mappings(mappings)

        # Assert – created mapper functions correctly
        assert mapper.map_tool("file_read", VendorTarget.CLAUDE_CODE) == "Read"

    def test_from_mappings_missing_tool_map_defaults_to_empty(self) -> None:
        # Arrange
        mappings: dict = {"model_map": {"reasoning_high": {"claude_code": "opus"}}}

        # Act
        mapper = ToolMapper.from_mappings(mappings)

        # Assert – no crash; tool lookup raises ValueError for unknown tool
        with pytest.raises(ValueError):
            mapper.map_tool("file_read", VendorTarget.CLAUDE_CODE)

    def test_from_mappings_missing_model_map_defaults_to_empty(self, sample_tool_map: dict) -> None:
        # Arrange
        mappings = {"tool_map": sample_tool_map}

        # Act
        mapper = ToolMapper.from_mappings(mappings)

        # Assert – model lookup returns None for unknown tier (empty model_map)
        result = mapper.map_model(ModelTier.FAST, VendorTarget.CLAUDE_CODE)
        assert result is None

    def test_from_mappings_empty_dict_creates_empty_mapper(self) -> None:
        # Arrange / Act
        mapper = ToolMapper.from_mappings({})

        # Assert – no crash; empty mapper returns None on model lookup
        result = mapper.map_model(ModelTier.FAST, VendorTarget.CLAUDE_CODE)
        assert result is None

    def test_from_mappings_returns_tool_mapper_instance(
        self, sample_tool_map: dict, sample_model_map: dict
    ) -> None:
        # Arrange
        mappings = {"tool_map": sample_tool_map, "model_map": sample_model_map}

        # Act
        result = ToolMapper.from_mappings(mappings)

        # Assert
        assert isinstance(result, ToolMapper)


# ---------------------------------------------------------------------------
# Edge cases: empty tool_map / all-None vendor entries
# ---------------------------------------------------------------------------


class TestEdgeCases:
    """Edge case tests for ToolMapper."""

    def test_empty_tool_map_map_tools_returns_empty(self) -> None:
        # Arrange
        mapper = ToolMapper(tool_map={}, model_map={})

        # Act – map_tools on empty list should trivially work
        result = mapper.map_tools([], VendorTarget.CLAUDE_CODE)

        # Assert
        assert result == []

    def test_empty_tool_map_reverse_map_tools_returns_empty(self) -> None:
        # Arrange
        mapper = ToolMapper(tool_map={}, model_map={})

        # Act
        result = mapper.reverse_map_tools(["Read", "Write"], VendorTarget.CLAUDE_CODE)

        # Assert
        assert result == []

    def test_tool_with_all_none_vendors_map_tool_returns_none(self) -> None:
        # Arrange – a tool with every vendor set to None
        tool_map: dict[str, dict[str, str | None]] = {
            "headless_tool": {
                "claude_code": None,
                "openai": None,
                "ollama": None,
            }
        }
        mapper = ToolMapper(tool_map=tool_map, model_map={})

        # Act
        result = mapper.map_tool("headless_tool", VendorTarget.CLAUDE_CODE)

        # Assert
        assert result is None

    def test_tool_with_all_none_vendors_excluded_from_map_tools(self) -> None:
        # Arrange
        tool_map: dict[str, dict[str, str | None]] = {
            "headless_tool": {
                "claude_code": None,
                "openai": None,
                "ollama": None,
            }
        }
        mapper = ToolMapper(tool_map=tool_map, model_map={})

        # Act
        result = mapper.map_tools(["headless_tool"], VendorTarget.CLAUDE_CODE)

        # Assert
        assert result == []

    def test_tool_with_all_none_vendors_not_reverse_mapped(self) -> None:
        # Arrange
        tool_map: dict[str, dict[str, str | None]] = {
            "headless_tool": {
                "claude_code": None,
            }
        }
        mapper = ToolMapper(tool_map=tool_map, model_map={})

        # Act
        result = mapper.reverse_map_tool("anything", VendorTarget.CLAUDE_CODE)

        # Assert
        assert result is None

    def test_substitute_text_with_empty_tool_map_returns_unchanged(self) -> None:
        # Arrange
        mapper = ToolMapper(tool_map={}, model_map={})
        text = "Use file_read to load data."

        # Act
        result = mapper.substitute_tool_names_in_text(text, VendorTarget.CLAUDE_CODE)

        # Assert – nothing to substitute; text unchanged
        assert result == text
