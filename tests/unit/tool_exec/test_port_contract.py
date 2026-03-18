# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Port contract tests for ToolFamilyResolverPort.

Validates that any concrete implementation of ToolFamilyResolverPort
satisfies the behavioral contract defined by the abstract port interface.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from src.shared_kernel.exceptions import NotFoundError
from src.tool_exec.domain.ports.tool_family_resolver_port import (
    ToolFamilyResolverPort,
)
from src.tool_exec.domain.value_objects.security_policy import SecurityPolicy
from src.tool_exec.domain.value_objects.tool_resolution_entry import (
    ToolResolutionEntry,
)
from src.tool_exec.infrastructure.adapters.rainbow_tool_resolver import (
    RainbowToolResolver,
)


@pytest.fixture()
def rainbow_resolver() -> RainbowToolResolver:
    """Create a RainbowToolResolver with the real config."""
    repo_root = Path(__file__).resolve().parents[3]
    config_path = repo_root / "skills" / "rainbow" / "config" / "tool-exec.yaml"
    if not config_path.exists():
        pytest.skip(f"Config not found: {config_path}")
    return RainbowToolResolver(config_path=str(config_path))


class TestPortContractCompliance:
    """Verify RainbowToolResolver implements ToolFamilyResolverPort."""

    def test_is_subclass(self) -> None:
        """RainbowToolResolver is a subclass of ToolFamilyResolverPort."""
        assert issubclass(RainbowToolResolver, ToolFamilyResolverPort)

    def test_can_resolve_returns_bool(self, rainbow_resolver: RainbowToolResolver) -> None:
        """can_resolve returns a boolean."""
        result = rainbow_resolver.can_resolve("nuclei")
        assert isinstance(result, bool)

    def test_resolve_returns_entry(self, rainbow_resolver: RainbowToolResolver) -> None:
        """resolve returns a ToolResolutionEntry."""
        result = rainbow_resolver.resolve("nuclei")
        assert isinstance(result, ToolResolutionEntry)

    def test_resolve_entry_has_required_fields(self, rainbow_resolver: RainbowToolResolver) -> None:
        """Resolved entry has all required fields populated."""
        entry = rainbow_resolver.resolve("nuclei")
        assert entry.tool_name == "nuclei"
        assert entry.family == "rainbow"
        assert entry.zone in {"Zone 1", "Zone 2", "Zone 3"}
        assert entry.default_mode in {"local", "container"}

    def test_security_policy_returns_policy(self, rainbow_resolver: RainbowToolResolver) -> None:
        """security_policy returns a SecurityPolicy."""
        result = rainbow_resolver.security_policy("nuclei")
        assert isinstance(result, SecurityPolicy)

    def test_security_policy_has_required_fields(
        self, rainbow_resolver: RainbowToolResolver
    ) -> None:
        """Security policy has all required fields."""
        policy = rainbow_resolver.security_policy("nuclei")
        assert isinstance(policy.requires_engagement, bool)
        assert isinstance(policy.requires_approval, bool)
        assert isinstance(policy.credential_filter_enabled, bool)
        assert policy.network_access in {"none", "restricted", "full"}

    def test_load_config_returns_dict(self, rainbow_resolver: RainbowToolResolver) -> None:
        """load_config returns a dictionary."""
        repo_root = Path(__file__).resolve().parents[3]
        config_path = repo_root / "skills" / "rainbow" / "config" / "tool-exec.yaml"
        result = rainbow_resolver.load_config(str(config_path))
        assert isinstance(result, dict)

    def test_resolve_unknown_tool_raises_not_found(
        self, rainbow_resolver: RainbowToolResolver
    ) -> None:
        """resolve raises NotFoundError for unknown tools."""
        with pytest.raises(NotFoundError):
            rainbow_resolver.resolve("completely-unknown-tool-xyz")

    def test_security_policy_unknown_tool_raises_not_found(
        self, rainbow_resolver: RainbowToolResolver
    ) -> None:
        """security_policy raises NotFoundError for unknown tools."""
        with pytest.raises(NotFoundError):
            rainbow_resolver.security_policy("completely-unknown-tool-xyz")

    def test_can_resolve_false_for_unknown(self, rainbow_resolver: RainbowToolResolver) -> None:
        """can_resolve returns False for unknown tools."""
        assert rainbow_resolver.can_resolve("completely-unknown-tool-xyz") is False
