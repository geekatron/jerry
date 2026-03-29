# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""FullEngagementConfig value object — v1.0.0 engagement config schema (8 sections).

Represents the complete engagement configuration as defined in ADR-PROJ023-010.
This is the rich schema consumed by ``/cyber-ops``; the narrow ``EngagementConfig``
(proxy-only fields) is extracted via ``FullEngagementConfigParser.extract_proxy_config()``.

Design constraints:
    H-07: Domain layer — stdlib only, no infrastructure imports.
    H-10: One public class per file.
"""

from __future__ import annotations

from dataclasses import dataclass, field

_VALID_MODES = ("purple", "split", "single")
_VALID_TYPES = ("penetration_test", "red_team", "purple_team", "blue_team", "threat_hunt")


@dataclass(frozen=True)
class EngagementMetadata:
    """Section 1: Engagement metadata."""

    id: str
    name: str
    type: str
    mode: str
    start_date: str
    end_date: str = ""
    classification: str = "confidential"
    e2e_mode: bool = False


@dataclass(frozen=True)
class ProxyInfraConfig:
    """Infrastructure.proxy subsection."""

    enabled: bool = False
    provider: str = "digitalocean"
    region: str = "nyc1"
    count: int = 1
    proxy_type: str = "direct_socks5"
    socks_port: int = 1080
    image: str = "ubuntu-24-04-x64"
    size: str = "s-1vcpu-1gb"


@dataclass(frozen=True)
class InfrastructureConfig:
    """Section 3: Infrastructure configuration."""

    proxy: ProxyInfraConfig = field(default_factory=ProxyInfraConfig)


@dataclass(frozen=True)
class ScopeConfig:
    """Section 2: Engagement scope."""

    targets: list = field(default_factory=list)
    authorized_techniques: list = field(default_factory=list)
    excluded_techniques: list = field(default_factory=list)
    exclusions: list = field(default_factory=list)


@dataclass(frozen=True)
class TeamsConfig:
    """Section 4: Team operator assignments."""

    red: dict = field(default_factory=dict)
    blue: dict = field(default_factory=dict)


@dataclass(frozen=True)
class CredentialsConfig:
    """Section 5: Credential references (NOT values — keyring key names only)."""

    proxy_api_key: dict = field(default_factory=dict)


@dataclass(frozen=True)
class RulesOfEngagementConfig:
    """Section 6: Authorization, escalation, and data handling rules."""

    authorization: str = ""
    escalation_contact: str = ""
    emergency_stop: bool = True
    notification_required: bool = False
    data_handling: str = "no_exfil"


@dataclass(frozen=True)
class PurpleTeamConfig:
    """Section 7: Purple-mode-specific configuration."""

    technique_approval: str = "per_technique"
    pivot_mode: str = "sequential"
    correlation_mode: str = "real_time"


@dataclass(frozen=True)
class OutputConfig:
    """Section 8: Report format and retention settings."""

    report_format: str = "markdown"
    report_template: str = "default"
    archive_location: str = ""
    retention_days: int = 90


@dataclass(frozen=True)
class FullEngagementConfig:
    """Complete v1.0.0 engagement configuration (8 sections).

    Attributes:
        engagement: Section 1 — metadata (id, name, type, mode, dates)
        scope: Section 2 — targets, techniques, exclusions
        infrastructure: Section 3 — proxy and sensor configuration
        teams: Section 4 — operator assignments (typed)
        credentials: Section 5 — credential references (typed)
        rules_of_engagement: Section 6 — authorization and data handling (typed)
        purple_team: Section 7 — purple-mode-specific config (typed)
        output: Section 8 — report format and retention (typed)
    """

    engagement: EngagementMetadata
    scope: ScopeConfig
    infrastructure: InfrastructureConfig = field(default_factory=InfrastructureConfig)
    teams: TeamsConfig | dict = field(default_factory=dict)
    credentials: CredentialsConfig | dict = field(default_factory=dict)
    rules_of_engagement: RulesOfEngagementConfig | dict = field(default_factory=dict)
    purple_team: PurpleTeamConfig | dict = field(default_factory=dict)
    output: OutputConfig | dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Enforce domain invariants.

        Raises:
            ValueError: If required fields are empty or mode is invalid.
        """
        if not self.engagement.id or not self.engagement.id.strip():
            raise ValueError("engagement.id must not be empty")
        if self.engagement.mode not in _VALID_MODES:
            raise ValueError(
                f"engagement.mode must be one of {_VALID_MODES}, got '{self.engagement.mode}'"
            )
        if not self.scope.targets:
            raise ValueError("scope.targets must contain at least one target")
        if self.engagement.mode == "split":
            # teams can be TeamsConfig or dict (backward compat)
            if isinstance(self.teams, dict):
                blue = self.teams.get("blue", {})
            else:
                blue = self.teams.blue
            if not blue or not blue.get("operator", ""):
                raise ValueError(
                    "teams.blue.operator is required for split mode — "
                    "blue team operator must be assigned"
                )
