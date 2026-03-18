# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for RainbowToolResolver."""

from __future__ import annotations

from pathlib import Path

import pytest

from src.shared_kernel.exceptions import NotFoundError
from src.tool_exec.infrastructure.adapters.rainbow_tool_resolver import (
    RainbowToolResolver,
)


@pytest.fixture()
def config_path() -> str:
    """Return the path to the real tool-exec.yaml config."""
    path = Path(__file__).resolve().parents[3] / "skills" / "rainbow" / "config" / "tool-exec.yaml"
    if not path.exists():
        pytest.skip(f"Config file not found: {path}")
    return str(path)


@pytest.fixture()
def resolver(config_path: str) -> RainbowToolResolver:
    """Create a resolver with the real config loaded."""
    return RainbowToolResolver(config_path=config_path)


class TestRainbowToolResolverCanResolve:
    """Tests for can_resolve() prefix matching."""

    def test_exact_prefix_match(self, resolver: RainbowToolResolver) -> None:
        """Exact prefix like 'nuclei' is resolved."""
        assert resolver.can_resolve("nuclei") is True

    def test_wildcard_prefix_match(self, resolver: RainbowToolResolver) -> None:
        """Wildcard prefix 'impacket-*' matches 'impacket-GetNPUsers'."""
        assert resolver.can_resolve("impacket-GetNPUsers") is True

    def test_unknown_tool_not_resolved(self, resolver: RainbowToolResolver) -> None:
        """Unknown tool is not resolved."""
        assert resolver.can_resolve("completely-unknown-tool") is False

    def test_zone_1_tool(self, resolver: RainbowToolResolver) -> None:
        """Zone 1 tool (checkov) is resolvable."""
        assert resolver.can_resolve("checkov") is True

    def test_zone_2_tool(self, resolver: RainbowToolResolver) -> None:
        """Zone 2 tool (subfinder) is resolvable."""
        assert resolver.can_resolve("subfinder") is True

    def test_zone_3_tool(self, resolver: RainbowToolResolver) -> None:
        """Zone 3 tool (msfconsole) is resolvable."""
        assert resolver.can_resolve("msfconsole") is True


class TestRainbowToolResolverResolve:
    """Tests for resolve() resolution entry creation."""

    def test_resolve_returns_correct_zone(self, resolver: RainbowToolResolver) -> None:
        """Resolved entry has the correct zone."""
        entry = resolver.resolve("nuclei")
        assert entry.zone == "Zone 2"
        assert entry.family == "rainbow"

    def test_resolve_zone_3_tool(self, resolver: RainbowToolResolver) -> None:
        """Zone 3 tool has correct zone in resolution entry."""
        entry = resolver.resolve("msfconsole")
        assert entry.zone == "Zone 3"

    def test_resolve_zone_1_tool(self, resolver: RainbowToolResolver) -> None:
        """Zone 1 tool has correct zone in resolution entry."""
        entry = resolver.resolve("trivy")
        assert entry.zone == "Zone 1"

    def test_resolve_sets_container_service(self, resolver: RainbowToolResolver) -> None:
        """Resolved entry has a container service."""
        entry = resolver.resolve("nuclei")
        assert entry.container_service == "recon-pipeline"

    def test_resolve_sets_compose_file(self, resolver: RainbowToolResolver) -> None:
        """Resolved entry has a compose file path."""
        entry = resolver.resolve("nuclei")
        assert entry.compose_file is not None
        assert "docker-compose.yml" in entry.compose_file

    def test_resolve_unknown_tool_raises(self, resolver: RainbowToolResolver) -> None:
        """Unknown tool raises NotFoundError."""
        with pytest.raises(NotFoundError, match="RainbowTool"):
            resolver.resolve("completely-unknown-tool")

    def test_resolve_wildcard_impacket(self, resolver: RainbowToolResolver) -> None:
        """Wildcard impacket-* resolves correctly."""
        entry = resolver.resolve("impacket-secretsdump")
        assert entry.zone == "Zone 3"
        assert entry.container_service == "exploit-ops"
        assert entry.sub_skill == "rainbow-exploit"


class TestRainbowToolResolverSecurityPolicy:
    """Tests for security_policy() zone-based policy mapping."""

    def test_zone_1_policy(self, resolver: RainbowToolResolver) -> None:
        """Zone 1 tool has no engagement requirement."""
        policy = resolver.security_policy("checkov")
        assert policy.requires_engagement is False
        assert policy.requires_approval is False
        assert policy.credential_filter_enabled is True
        assert policy.network_access == "none"
        assert policy.family_zone_label == "Zone 1"

    def test_zone_2_policy(self, resolver: RainbowToolResolver) -> None:
        """Zone 2 tool requires engagement but not approval."""
        policy = resolver.security_policy("subfinder")
        assert policy.requires_engagement is True
        assert policy.requires_approval is False
        assert policy.network_access == "restricted"
        assert policy.family_zone_label == "Zone 2"

    def test_zone_3_policy(self, resolver: RainbowToolResolver) -> None:
        """Zone 3 tool requires engagement, approval, and container."""
        policy = resolver.security_policy("msfconsole")
        assert policy.requires_engagement is True
        assert policy.requires_approval is True
        assert policy.container_required is True
        assert policy.network_access == "full"
        assert policy.family_zone_label == "Zone 3"

    def test_policy_unknown_tool_raises(self, resolver: RainbowToolResolver) -> None:
        """Unknown tool raises NotFoundError."""
        with pytest.raises(NotFoundError):
            resolver.security_policy("unknown-tool")

    def test_policy_has_redacted_env_vars(self, resolver: RainbowToolResolver) -> None:
        """Security policy includes redacted environment variables."""
        policy = resolver.security_policy("nuclei")
        assert len(policy.redacted_env_vars) > 0


class TestRainbowToolResolverLoadConfig:
    """Tests for load_config()."""

    def test_load_config_returns_dict(self, config_path: str) -> None:
        """load_config returns a dictionary."""
        resolver = RainbowToolResolver()
        config = resolver.load_config(config_path)
        assert isinstance(config, dict)
        assert "tool_resolution" in config

    def test_load_config_missing_file_raises(self) -> None:
        """load_config raises FileNotFoundError for missing file."""
        resolver = RainbowToolResolver()
        with pytest.raises(FileNotFoundError):
            resolver.load_config("/nonexistent/path/config.yaml")
