# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for SecurityPolicy value object."""

from __future__ import annotations

import pytest

from src.tool_exec.domain.value_objects.security_policy import SecurityPolicy


class TestSecurityPolicy:
    """Tests for SecurityPolicy immutability and validation."""

    def test_create_minimal_policy(self) -> None:
        """SecurityPolicy can be created with required fields only."""
        policy = SecurityPolicy(
            requires_engagement=False,
            requires_approval=False,
            credential_filter_enabled=True,
        )
        assert policy.requires_engagement is False
        assert policy.requires_approval is False
        assert policy.credential_filter_enabled is True
        assert policy.credential_filter_patterns == []
        assert policy.container_required is False
        assert policy.network_access == "none"
        assert policy.redacted_env_vars == []
        assert policy.family_zone_label is None

    def test_create_full_policy(self) -> None:
        """SecurityPolicy can be created with all fields populated."""
        policy = SecurityPolicy(
            requires_engagement=True,
            requires_approval=True,
            credential_filter_enabled=True,
            credential_filter_patterns=[r"custom-[0-9]+"],
            container_required=True,
            network_access="full",
            redacted_env_vars=["SECRET_KEY"],
            family_zone_label="Zone 3",
        )
        assert policy.requires_engagement is True
        assert policy.container_required is True
        assert policy.network_access == "full"
        assert policy.family_zone_label == "Zone 3"

    def test_frozen_immutability(self) -> None:
        """SecurityPolicy is immutable (frozen dataclass)."""
        policy = SecurityPolicy(
            requires_engagement=False,
            requires_approval=False,
            credential_filter_enabled=True,
        )
        with pytest.raises(AttributeError):
            policy.requires_engagement = True  # type: ignore[misc]

    def test_invalid_network_access_raises(self) -> None:
        """SecurityPolicy rejects invalid network_access values."""
        with pytest.raises(ValueError, match="Invalid network_access"):
            SecurityPolicy(
                requires_engagement=False,
                requires_approval=False,
                credential_filter_enabled=True,
                network_access="unlimited",
            )

    @pytest.mark.parametrize(
        "network_access",
        ["none", "restricted", "full"],
    )
    def test_valid_network_access_values(self, network_access: str) -> None:
        """SecurityPolicy accepts all three valid network_access values."""
        policy = SecurityPolicy(
            requires_engagement=False,
            requires_approval=False,
            credential_filter_enabled=True,
            network_access=network_access,
        )
        assert policy.network_access == network_access
