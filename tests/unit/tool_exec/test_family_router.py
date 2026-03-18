# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for FamilyRouterService."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from src.shared_kernel.exceptions import NotFoundError
from src.tool_exec.domain.ports.tool_family_resolver_port import (
    ToolFamilyResolverPort,
)
from src.tool_exec.domain.services.family_router import FamilyRouterService
from src.tool_exec.domain.value_objects.tool_resolution_entry import (
    ToolResolutionEntry,
)


def _make_resolver(
    name: str,
    can_resolve_commands: list[str],
) -> ToolFamilyResolverPort:
    """Create a mock resolver that handles specific commands.

    Args:
        name: Family name.
        can_resolve_commands: Tool commands this resolver can handle.

    Returns:
        Mock resolver implementing ToolFamilyResolverPort.
    """
    resolver = MagicMock(spec=ToolFamilyResolverPort)
    # FM-006: FAMILY_NAME is accessed by FamilyRouterService logger during auto-detect.
    resolver.FAMILY_NAME = name

    def can_resolve(cmd: str) -> bool:
        return cmd in can_resolve_commands

    def resolve(cmd: str) -> ToolResolutionEntry:
        if cmd not in can_resolve_commands:
            raise NotFoundError(entity_type="Tool", entity_id=cmd)
        return ToolResolutionEntry(
            tool_name=cmd,
            binary_path=None,
            container_service=f"{name}-service",
            default_mode="container",
            family=name,
        )

    resolver.can_resolve.side_effect = can_resolve
    resolver.resolve.side_effect = resolve
    return resolver


class TestFamilyRouterExplicitDispatch:
    """Tests for explicit --family dispatch."""

    def test_explicit_family_routes_correctly(self) -> None:
        """Explicit family routes to the specified resolver."""
        resolver = _make_resolver("rainbow", ["nuclei"])
        router = FamilyRouterService({"rainbow": resolver})

        result = router.resolve("nuclei", family="rainbow")
        assert result.family == "rainbow"
        assert result.tool_name == "nuclei"

    def test_explicit_unknown_family_raises(self) -> None:
        """Explicit family that is not registered raises NotFoundError."""
        resolver = _make_resolver("rainbow", ["nuclei"])
        router = FamilyRouterService({"rainbow": resolver})

        with pytest.raises(NotFoundError, match="ToolFamily"):
            router.resolve("nuclei", family="unknown-family")

    def test_explicit_family_unknown_tool_raises(self) -> None:
        """Known family that cannot resolve the tool raises NotFoundError."""
        resolver = _make_resolver("rainbow", ["nuclei"])
        router = FamilyRouterService({"rainbow": resolver})

        with pytest.raises(NotFoundError):
            router.resolve("nonexistent-tool", family="rainbow")


class TestFamilyRouterAutoDetect:
    """Tests for auto-detect dispatch via can_resolve()."""

    def test_auto_detect_single_family(self) -> None:
        """Auto-detect routes to the only family that can resolve."""
        resolver = _make_resolver("rainbow", ["nuclei", "trivy"])
        router = FamilyRouterService({"rainbow": resolver})

        result = router.resolve("nuclei")
        assert result.family == "rainbow"

    def test_auto_detect_multiple_families(self) -> None:
        """Auto-detect routes to the first family that can resolve."""
        rainbow = _make_resolver("rainbow", ["nuclei"])
        blue_team = _make_resolver("blue-team", ["yara"])
        router = FamilyRouterService({"rainbow": rainbow, "blue-team": blue_team})

        result = router.resolve("yara")
        assert result.family == "blue-team"

    def test_auto_detect_no_match_raises(self) -> None:
        """Auto-detect raises NotFoundError when no family can resolve."""
        resolver = _make_resolver("rainbow", ["nuclei"])
        router = FamilyRouterService({"rainbow": resolver})

        with pytest.raises(NotFoundError, match="Tool"):
            router.resolve("completely-unknown-tool")


class TestFamilyRouterListFamilies:
    """Tests for listing registered families."""

    def test_list_families_empty(self) -> None:
        """Empty router returns empty list."""
        router = FamilyRouterService({})
        assert router.list_families() == []

    def test_list_families_sorted(self) -> None:
        """Families are returned in sorted order."""
        router = FamilyRouterService(
            {
                "zebra": MagicMock(spec=ToolFamilyResolverPort),
                "alpha": MagicMock(spec=ToolFamilyResolverPort),
            }
        )
        assert router.list_families() == ["alpha", "zebra"]
