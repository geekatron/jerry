# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""FullEngagementConfigParser — parses full v1.0.0 engagement config YAML.

Parses the rich 8-section engagement config consumed by ``/cyber-ops`` and
extracts the narrow ``EngagementConfig`` consumed by the proxy pipeline.

Design constraints:
    H-07: Application layer — imports domain only.
    H-10: One public class per file.
    H-11: All public methods have type annotations.

References:
    - TASK-023-098: FullEngagementConfig value object
    - TASK-023-099: from_full_config() bridge + backward compat
    - ADR-PROJ023-010: Engagement config schema v1.0.0
"""

from __future__ import annotations

import logging
from pathlib import Path

import yaml

from src.proxy_infra.domain.value_objects.engagement_config import EngagementConfig
from src.proxy_infra.domain.value_objects.full_engagement_config import (
    CredentialsConfig,
    EngagementMetadata,
    FullEngagementConfig,
    InfrastructureConfig,
    OutputConfig,
    ProxyInfraConfig,
    PurpleTeamConfig,
    RulesOfEngagementConfig,
    ScopeConfig,
    TeamsConfig,
)

logger = logging.getLogger(__name__)


class FullEngagementConfigParser:
    """Parses full v1.0.0 engagement config YAML into FullEngagementConfig.

    Also provides ``extract_proxy_config()`` to bridge the full config
    into the narrow ``EngagementConfig`` consumed by the proxy pipeline.
    """

    def parse(self, config_path: Path) -> FullEngagementConfig:
        """Parse a full engagement config YAML file.

        Args:
            config_path: Path to the YAML engagement config.

        Returns:
            Validated FullEngagementConfig value object.

        Raises:
            FileNotFoundError: If config_path does not exist.
            ValueError: If required fields are missing or invalid.
        """
        if not config_path.exists():
            raise FileNotFoundError(f"Engagement config not found: {config_path}")

        data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError(f"Engagement config must be a YAML mapping, got {type(data).__name__}")

        eng_data = data.get("engagement", {})
        scope_data = data.get("scope", {})
        infra_data = data.get("infrastructure", {})
        proxy_data = infra_data.get("proxy", {})

        metadata = EngagementMetadata(
            id=str(eng_data.get("id", "")),
            name=str(eng_data.get("name", "")),
            type=str(eng_data.get("type", "penetration_test")),
            mode=str(eng_data.get("mode", "single")),
            start_date=str(eng_data.get("start_date", "")),
            end_date=str(eng_data.get("end_date", "")),
            classification=str(eng_data.get("classification", "confidential")),
        )

        scope = ScopeConfig(
            targets=scope_data.get("targets", []),
            authorized_techniques=scope_data.get("authorized_techniques", []),
            excluded_techniques=scope_data.get("excluded_techniques", []),
            exclusions=scope_data.get("exclusions", []),
        )

        proxy = ProxyInfraConfig(
            enabled=bool(proxy_data.get("enabled", False)),
            provider=str(proxy_data.get("provider", "digitalocean")),
            region=str(proxy_data.get("region", "nyc1")),
            count=int(proxy_data.get("count", 1)),
            proxy_type=str(proxy_data.get("proxy_type", "direct_socks5")),
            socks_port=int(proxy_data.get("socks_port", 1080)),
            image=str(proxy_data.get("image", "ubuntu-24-04-x64")),
            size=str(proxy_data.get("size", "s-1vcpu-1gb")),
        )

        infrastructure = InfrastructureConfig(proxy=proxy)

        # Instantiate typed sections 4-8
        teams_data = data.get("teams", {})
        teams = TeamsConfig(
            red=teams_data.get("red", {}),
            blue=teams_data.get("blue", {}),
        )

        creds_data = data.get("credentials", {})
        credentials = CredentialsConfig(
            proxy_api_key=creds_data.get("proxy_api_key", {}),
        )

        roe_data = data.get("rules_of_engagement", {})
        rules_of_engagement = RulesOfEngagementConfig(
            authorization=str(roe_data.get("authorization", "")),
            escalation_contact=str(roe_data.get("escalation_contact", "")),
            emergency_stop=bool(roe_data.get("emergency_stop", True)),
            notification_required=bool(roe_data.get("notification_required", False)),
            data_handling=str(roe_data.get("data_handling", "no_exfil")),
        )

        pt_data = data.get("purple_team", {})
        purple_team = PurpleTeamConfig(
            technique_approval=str(pt_data.get("technique_approval", "per_technique")),
            pivot_mode=str(pt_data.get("pivot_mode", "sequential")),
            correlation_mode=str(pt_data.get("correlation_mode", "real_time")),
        )

        out_data = data.get("output", {})
        output = OutputConfig(
            report_format=str(out_data.get("report_format", "markdown")),
            report_template=str(out_data.get("report_template", "default")),
            archive_location=str(out_data.get("archive_location", "")),
            retention_days=int(out_data.get("retention_days", 90)),
        )

        return FullEngagementConfig(
            engagement=metadata,
            scope=scope,
            infrastructure=infrastructure,
            teams=teams,
            credentials=credentials,
            rules_of_engagement=rules_of_engagement,
            purple_team=purple_team,
            output=output,
        )

    def extract_proxy_config(self, config_path: Path) -> EngagementConfig:
        """Extract the proxy-relevant EngagementConfig from a full config.

        Bridge method: reads the full v1.0.0 schema and extracts the
        infrastructure.proxy section into the narrow EngagementConfig
        consumed by the proxy provisioning pipeline.

        Args:
            config_path: Path to the full engagement config YAML.

        Returns:
            EngagementConfig with proxy-relevant fields.

        Raises:
            ValueError: If infrastructure.proxy.enabled is false.
        """
        full = self.parse(config_path)

        if not full.infrastructure.proxy.enabled:
            raise ValueError(
                "infrastructure.proxy is not enabled in this engagement config. "
                "Set infrastructure.proxy.enabled: true to use the proxy pipeline."
            )

        proxy = full.infrastructure.proxy

        # Resolve operator_ip: check infrastructure.proxy.operator_ip first,
        # then teams.red.operator_ip, then raise if neither is set.
        operator_ip = (
            proxy_data.get("operator_ip", "")
            if (proxy_data := full.infrastructure.proxy.__dict__) and False
            else ""
        )
        # Try the raw YAML data — operator_ip may be in the proxy section
        raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))
        raw_proxy = raw.get("infrastructure", {}).get("proxy", {})
        operator_ip = str(raw_proxy.get("operator_ip", ""))

        if not operator_ip:
            # teams can be TeamsConfig or dict (backward compat)
            if isinstance(full.teams, dict):
                red_team = full.teams.get("red", {})
            else:
                red_team = full.teams.red
            operator_ip = str(red_team.get("operator_ip", "") if isinstance(red_team, dict) else "")

        if not operator_ip:
            raise ValueError(
                "operator_ip could not be resolved from the engagement config. "
                "Set infrastructure.proxy.operator_ip or teams.red.operator_ip "
                "to your public egress IP for firewall allowlisting."
            )

        return EngagementConfig(
            engagement_id=full.engagement.id,
            provider=proxy.provider,
            region=proxy.region,
            count=proxy.count,
            proxy_type=proxy.proxy_type,
            socks_port=proxy.socks_port,
            operator_ip=operator_ip,
            image=proxy.image,
            size=proxy.size,
        )
