# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Security policy value object for tool execution.

Defines the security constraints applied to a tool family, including
engagement requirements, credential filtering, container isolation,
and network access controls.

References:
    - ADR-PROJ023-001: Rainbow Tool Executor Behavioral Contract
    - TASK-001C: Value Objects
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class SecurityPolicy:
    """Immutable security policy for a tool family or individual tool.

    Encapsulates all security constraints that govern how a tool may be
    executed, what filtering is applied to its output, and what engagement
    context is required.

    Attributes:
        requires_engagement: Whether an active engagement is required before execution.
        requires_approval: Whether per-operation user approval is required (Zone 3).
        credential_filter_enabled: Whether the credential filter pipeline is active.
        credential_filter_patterns: Family-specific regex patterns that extend the
            base 15 patterns from the credential filter service.
        container_required: Whether the tool must run inside a container.
        network_access: Network access level: 'none', 'restricted', or 'full'.
        redacted_env_vars: Environment variable names to redact from tool context.
        family_zone_label: Security zone label (e.g., 'Zone 1'), or None for
            non-security tool families.
    """

    requires_engagement: bool
    requires_approval: bool
    credential_filter_enabled: bool
    credential_filter_patterns: list[str] = field(default_factory=list)
    container_required: bool = False
    network_access: str = "none"
    redacted_env_vars: list[str] = field(default_factory=list)
    family_zone_label: str | None = None

    def __post_init__(self) -> None:
        """Validate security policy invariants."""
        valid_network_values = {"none", "restricted", "full"}
        if self.network_access not in valid_network_values:
            msg = (
                f"Invalid network_access '{self.network_access}'. "
                f"Must be one of: {', '.join(sorted(valid_network_values))}"
            )
            raise ValueError(msg)
