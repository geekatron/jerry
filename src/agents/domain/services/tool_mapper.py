# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ToolMapper - Maps abstract tool/model names to vendor-specific names.

Reads from mappings.yaml to translate between canonical abstract tool
names (e.g., file_read) and vendor-specific names (e.g., Read for Claude Code).

References:
    - ADR-PROJ010-003: LLM Portability Architecture
    - agent-development-standards.md: Tool Security Tiers
"""

from __future__ import annotations

from typing import Any

from src.agents.domain.value_objects.model_tier import ModelTier
from src.agents.domain.value_objects.vendor_target import VendorTarget


class ToolMapper:
    """Maps abstract tool and model names to vendor-specific equivalents.

    Attributes:
        _tool_map: Abstract tool name -> vendor -> vendor tool name.
        _model_map: Abstract model tier -> vendor -> vendor model name.
    """

    def __init__(
        self,
        tool_map: dict[str, dict[str, str | None]],
        model_map: dict[str, dict[str, str | None]],
    ) -> None:
        """Initialize with mapping dictionaries.

        Args:
            tool_map: Tool name mappings from mappings.yaml.
            model_map: Model name mappings from mappings.yaml.
        """
        self._tool_map = tool_map
        self._model_map = model_map

    def map_tool(self, abstract_name: str, vendor: VendorTarget) -> str | None:
        """Map an abstract tool name to a vendor-specific tool name.

        Args:
            abstract_name: Abstract tool name (e.g., 'file_read').
            vendor: Target vendor.

        Returns:
            Vendor-specific tool name, or None if not supported by this vendor.

        Raises:
            ValueError: If abstract_name is not recognized.
        """
        tool_entry = self._tool_map.get(abstract_name)
        if tool_entry is None:
            raise ValueError(
                f"Unknown abstract tool: {abstract_name!r}. "
                f"Known tools: {', '.join(sorted(self._tool_map.keys()))}"
            )
        return tool_entry.get(vendor.value)

    def map_tools(
        self,
        abstract_names: list[str],
        vendor: VendorTarget,
    ) -> list[str]:
        """Map a list of abstract tool names to vendor-specific names.

        Filters out tools that are None (not supported by vendor).

        Args:
            abstract_names: Abstract tool names.
            vendor: Target vendor.

        Returns:
            List of vendor-specific tool names (unsupported tools excluded).
        """
        result = []
        for name in abstract_names:
            mapped = self.map_tool(name, vendor)
            if mapped is not None:
                result.append(mapped)
        return result

    def map_model(self, tier: ModelTier, vendor: VendorTarget) -> str | None:
        """Map an abstract model tier to a vendor-specific model name.

        Args:
            tier: Abstract model tier.
            vendor: Target vendor.

        Returns:
            Vendor-specific model name, or None if not supported.
        """
        model_entry = self._model_map.get(tier.value, {})
        return model_entry.get(vendor.value)

    def reverse_map_tool(self, vendor_name: str, vendor: VendorTarget) -> str | None:
        """Reverse-map a vendor-specific tool name to abstract name.

        Args:
            vendor_name: Vendor-specific tool name (e.g., 'Read').
            vendor: Source vendor.

        Returns:
            Abstract tool name, or None if not found.
        """
        for abstract_name, vendor_map in self._tool_map.items():
            if vendor_map.get(vendor.value) == vendor_name:
                return abstract_name
        return None

    def reverse_map_tools(
        self,
        vendor_names: list[str],
        vendor: VendorTarget,
    ) -> list[str]:
        """Reverse-map a list of vendor-specific tool names to abstract names.

        Args:
            vendor_names: Vendor-specific tool names.
            vendor: Source vendor.

        Returns:
            List of abstract tool names (unrecognized tools excluded).
        """
        result = []
        for name in vendor_names:
            abstract = self.reverse_map_tool(name, vendor)
            if abstract is not None:
                result.append(abstract)
        return result

    def substitute_tool_names_in_text(
        self,
        text: str,
        vendor: VendorTarget,
        *,
        reverse: bool = False,
    ) -> str:
        """Substitute tool names in prompt body text.

        Replaces abstract tool names with vendor-specific names (or vice versa)
        in prose text. Uses word-boundary-aware replacement.

        Args:
            text: Text containing tool names.
            vendor: Target vendor.
            reverse: If True, replace vendor names with abstract names.

        Returns:
            Text with tool names substituted.
        """
        if reverse:
            replacements = self._build_reverse_replacements(vendor)
        else:
            replacements = self._build_forward_replacements(vendor)

        # Sort by length (longest first) to avoid partial replacements
        sorted_replacements = sorted(replacements.items(), key=lambda x: -len(x[0]))

        result = text
        for old, new in sorted_replacements:
            result = result.replace(old, new)
        return result

    def _build_forward_replacements(self, vendor: VendorTarget) -> dict[str, str]:
        """Build abstract -> vendor replacement map."""
        replacements: dict[str, str] = {}
        for abstract_name, vendor_map in self._tool_map.items():
            vendor_name = vendor_map.get(vendor.value)
            if vendor_name is not None:
                replacements[abstract_name] = vendor_name
        return replacements

    def _build_reverse_replacements(self, vendor: VendorTarget) -> dict[str, str]:
        """Build vendor -> abstract replacement map."""
        replacements: dict[str, str] = {}
        for abstract_name, vendor_map in self._tool_map.items():
            vendor_name = vendor_map.get(vendor.value)
            if vendor_name is not None:
                replacements[vendor_name] = abstract_name
        return replacements

    @classmethod
    def from_mappings(cls, mappings: dict[str, Any]) -> ToolMapper:
        """Create a ToolMapper from parsed mappings.yaml content.

        Args:
            mappings: Parsed YAML dict with 'tool_map' and 'model_map' keys.

        Returns:
            Configured ToolMapper instance.
        """
        return cls(
            tool_map=mappings.get("tool_map", {}),
            model_map=mappings.get("model_map", {}),
        )
