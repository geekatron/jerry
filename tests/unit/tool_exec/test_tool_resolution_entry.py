# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for ToolResolutionEntry value object."""

from __future__ import annotations

import pytest

from src.tool_exec.domain.value_objects.tool_resolution_entry import (
    ToolResolutionEntry,
)


class TestToolResolutionEntry:
    """Tests for ToolResolutionEntry immutability and validation."""

    def test_create_minimal_entry(self) -> None:
        """ToolResolutionEntry can be created with required fields."""
        entry = ToolResolutionEntry(
            tool_name="nuclei",
            binary_path=None,
            container_service="recon-pipeline",
            default_mode="container",
        )
        assert entry.tool_name == "nuclei"
        assert entry.binary_path is None
        assert entry.container_service == "recon-pipeline"
        assert entry.default_mode == "container"
        assert entry.zone == "Zone 1"
        assert entry.family == ""

    def test_create_full_entry(self) -> None:
        """ToolResolutionEntry can be created with all fields."""
        entry = ToolResolutionEntry(
            tool_name="impacket-GetNPUsers",
            binary_path=None,
            container_service="exploit-ops",
            default_mode="container",
            supported_modes=["container"],
            zone="Zone 3",
            family="rainbow",
            compose_file="skills/rainbow-exploit/tests/docker/docker-compose.yml",
            sub_skill="rainbow-exploit",
        )
        assert entry.zone == "Zone 3"
        assert entry.family == "rainbow"
        assert entry.sub_skill == "rainbow-exploit"

    def test_frozen_immutability(self) -> None:
        """ToolResolutionEntry is immutable."""
        entry = ToolResolutionEntry(
            tool_name="nuclei",
            binary_path=None,
            container_service="recon-pipeline",
            default_mode="container",
        )
        with pytest.raises(AttributeError):
            entry.tool_name = "changed"  # type: ignore[misc]

    def test_invalid_default_mode_raises(self) -> None:
        """ToolResolutionEntry rejects invalid default_mode."""
        with pytest.raises(ValueError, match="Invalid default_mode"):
            ToolResolutionEntry(
                tool_name="nuclei",
                binary_path=None,
                container_service=None,
                default_mode="hybrid",
            )

    def test_invalid_zone_raises(self) -> None:
        """ToolResolutionEntry rejects invalid zone."""
        with pytest.raises(ValueError, match="Invalid zone"):
            ToolResolutionEntry(
                tool_name="nuclei",
                binary_path=None,
                container_service=None,
                default_mode="local",
                zone="Zone 4",
            )

    @pytest.mark.parametrize(
        "zone",
        ["Zone 1", "Zone 2", "Zone 3"],
    )
    def test_valid_zones(self, zone: str) -> None:
        """ToolResolutionEntry accepts all three valid zone values."""
        entry = ToolResolutionEntry(
            tool_name="test",
            binary_path=None,
            container_service=None,
            default_mode="local",
            zone=zone,
        )
        assert entry.zone == zone
