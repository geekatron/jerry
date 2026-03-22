# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""Unit tests for the engagement scope to Envoy config translator.

Task: T13-015
Tests the security-critical scope_translator.py module:
- Domain extraction from scope targets
- Cloud account mapping
- IP validation
- URL host extraction
- ip_range rejection
- Virtual host generation
- Full config generation with deny-all preservation
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from src.tool_exec.infrastructure.envoy.scope_translator import (
    ScopeTranslationError,
    generate_envoy_config,
    translate_scope_to_envoy,
)


@pytest.fixture()
def scope_dir(tmp_path: Path) -> Path:
    """Create a temporary directory for scope files."""
    return tmp_path / "scopes"


@pytest.fixture()
def basic_scope(scope_dir: Path) -> Path:
    """Create a basic engagement scope with domain targets."""
    scope_dir.mkdir(parents=True, exist_ok=True)
    scope_path = scope_dir / "scope.yaml"
    scope_data = {
        "engagement": {
            "engagement_id": "RBW-0001",
            "authorized_targets": [
                {"type": "domain", "value": "target.example.com"},
                {"type": "domain", "value": "api.example.com"},
            ],
        }
    }
    scope_path.write_text(yaml.dump(scope_data))
    return scope_path


@pytest.fixture()
def mixed_scope(scope_dir: Path) -> Path:
    """Create a scope with multiple target types."""
    scope_dir.mkdir(parents=True, exist_ok=True)
    scope_path = scope_dir / "mixed-scope.yaml"
    scope_data = {
        "engagement": {
            "engagement_id": "RBW-0002",
            "authorized_targets": [
                {"type": "domain", "value": "target.example.com"},
                {"type": "ip", "value": "203.0.113.42"},
                {"type": "url", "value": "https://app.example.com/api/v1"},
                {"type": "cloud_account", "value": "aws:123456789012"},
            ],
            "c2_infrastructure": [
                {"type": "ip", "value": "198.51.100.10"},
                {"type": "domain", "value": "c2.attacker.com"},
            ],
        }
    }
    scope_path.write_text(yaml.dump(scope_data))
    return scope_path


@pytest.fixture()
def zone2_base_config(tmp_path: Path) -> Path:
    """Create a minimal Zone 2 base Envoy config."""
    config_path = tmp_path / "envoy-zone2-base.yaml"
    config_data = {
        "admin": {"address": {"socket_address": {"address": "0.0.0.0", "port_value": 9901}}},
        "static_resources": {
            "listeners": [
                {
                    "name": "egress_proxy",
                    "address": {"socket_address": {"address": "0.0.0.0", "port_value": 3128}},
                    "filter_chains": [
                        {
                            "filters": [
                                {
                                    "name": "envoy.filters.network.http_connection_manager",
                                    "typed_config": {
                                        "@type": "type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager",
                                        "stat_prefix": "zone2_test",
                                        "upgrade_configs": [{"upgrade_type": "CONNECT"}],
                                        "access_log": [
                                            {
                                                "name": "envoy.access_loggers.file",
                                                "typed_config": {
                                                    "@type": "type.googleapis.com/envoy.extensions.access_loggers.file.v3.FileAccessLog",
                                                    "path": "/var/log/envoy/access.log",
                                                    "log_format": {
                                                        "json_format": {"zone": "zone2-test"}
                                                    },
                                                },
                                            }
                                        ],
                                        "http_filters": [
                                            {
                                                "name": "envoy.filters.http.router",
                                                "typed_config": {},
                                            },
                                        ],
                                        "route_config": {
                                            "name": "zone2_test_routes",
                                            "virtual_hosts": [
                                                {
                                                    "name": "deny_all",
                                                    "domains": ["*"],
                                                    "routes": [
                                                        {
                                                            "match": {"prefix": "/"},
                                                            "direct_response": {
                                                                "status": 403,
                                                                "body": {"inline_string": "DENIED"},
                                                            },
                                                        }
                                                    ],
                                                }
                                            ],
                                        },
                                    },
                                }
                            ]
                        }
                    ],
                }
            ],
            "clusters": [
                {
                    "name": "dynamic_forward_proxy_cluster",
                    "lb_policy": "CLUSTER_PROVIDED",
                }
            ],
        },
    }
    config_path.write_text(yaml.dump(config_data, default_flow_style=False))
    return config_path


class TestTranslateScopeToEnvoy:
    """Test translate_scope_to_envoy function."""

    def test_basic_domain_targets(self, basic_scope: Path) -> None:
        """Domain targets produce virtual_host with exact domains only (CLM-004: no auto-wildcard)."""
        vhosts = translate_scope_to_envoy(basic_scope, zone=2)
        assert len(vhosts) == 1
        domains = vhosts[0]["domains"]
        # Bare domain and :443 variant present
        assert "target.example.com" in domains
        assert "target.example.com:443" in domains
        assert "api.example.com" in domains
        assert "api.example.com:443" in domains
        # CLM-004: No auto-expanded wildcards
        assert "*.target.example.com" not in domains
        assert "*.target.example.com:443" not in domains
        assert "*.api.example.com" not in domains
        assert "*.api.example.com:443" not in domains

    def test_explicit_wildcard_domain_preserved(self, scope_dir: Path) -> None:
        """Explicit wildcard domain input (*.target.example.com) is preserved (CLM-004)."""
        scope_dir.mkdir(parents=True, exist_ok=True)
        scope_path = scope_dir / "wildcard.yaml"
        scope_data = {
            "engagement": {
                "engagement_id": "RBW-CLM004",
                "authorized_targets": [
                    {"type": "domain", "value": "*.target.example.com"},
                ],
            }
        }
        scope_path.write_text(yaml.dump(scope_data))
        vhosts = translate_scope_to_envoy(scope_path, zone=2)
        domains = vhosts[0]["domains"]
        assert "*.target.example.com" in domains
        assert "*.target.example.com:443" in domains

    def test_ip_target(self, mixed_scope: Path) -> None:
        """IP targets produce virtual_host with exact IP."""
        vhosts = translate_scope_to_envoy(mixed_scope, zone=2)
        domains = vhosts[0]["domains"]
        assert "203.0.113.42" in domains

    def test_url_target_extracts_host(self, mixed_scope: Path) -> None:
        """URL targets extract hostname for virtual_host domain."""
        vhosts = translate_scope_to_envoy(mixed_scope, zone=2)
        domains = vhosts[0]["domains"]
        assert "app.example.com" in domains

    def test_cloud_account_target(self, mixed_scope: Path) -> None:
        """cloud_account targets map to provider API domains."""
        vhosts = translate_scope_to_envoy(mixed_scope, zone=2)
        domains = vhosts[0]["domains"]
        aws_domains = [d for d in domains if "amazonaws" in d or "aws.amazon" in d]
        assert len(aws_domains) >= 1

    def test_c2_not_included_without_flag(self, mixed_scope: Path) -> None:
        """C2 infrastructure NOT included when include_c2=False."""
        vhosts = translate_scope_to_envoy(mixed_scope, zone=3, include_c2=False)
        domains = vhosts[0]["domains"]
        assert "c2.attacker.com" not in domains
        assert "198.51.100.10" not in domains

    def test_c2_included_with_flag(self, mixed_scope: Path) -> None:
        """C2 infrastructure included when include_c2=True and zone=3."""
        vhosts = translate_scope_to_envoy(mixed_scope, zone=3, include_c2=True)
        domains = vhosts[0]["domains"]
        assert "c2.attacker.com" in domains
        assert "198.51.100.10" in domains

    def test_zone1_rejected(self, basic_scope: Path) -> None:
        """Zone 1 is not supported (uses static allowlist)."""
        with pytest.raises(ScopeTranslationError, match="zones 2 and 3"):
            translate_scope_to_envoy(basic_scope, zone=1)

    def test_deduplicates_domains(self, scope_dir: Path) -> None:
        """Duplicate domains are removed."""
        scope_dir.mkdir(parents=True, exist_ok=True)
        scope_path = scope_dir / "dupe.yaml"
        scope_data = {
            "engagement": {
                "engagement_id": "RBW-0003",
                "authorized_targets": [
                    {"type": "domain", "value": "example.com"},
                    {"type": "domain", "value": "example.com"},
                ],
            }
        }
        scope_path.write_text(yaml.dump(scope_data))
        vhosts = translate_scope_to_envoy(scope_path, zone=2)
        domains = vhosts[0]["domains"]
        assert domains.count("example.com") == 1

    def test_virtual_host_routes_to_dynamic_cluster(self, basic_scope: Path) -> None:
        """Generated virtual_host must route to dynamic_forward_proxy_cluster."""
        vhosts = translate_scope_to_envoy(basic_scope, zone=2)
        route = vhosts[0]["routes"][0]
        assert route["route"]["cluster"] == "dynamic_forward_proxy_cluster"


class TestScopeValidation:
    """Test scope file validation."""

    def test_missing_file_raises(self, tmp_path: Path) -> None:
        """Missing scope file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            translate_scope_to_envoy(tmp_path / "nonexistent.yaml", zone=2)

    def test_missing_engagement_key(self, scope_dir: Path) -> None:
        """Scope without 'engagement' key raises error."""
        scope_dir.mkdir(parents=True, exist_ok=True)
        scope_path = scope_dir / "bad.yaml"
        scope_path.write_text(yaml.dump({"not_engagement": {}}))
        with pytest.raises(ScopeTranslationError, match="missing 'engagement'"):
            translate_scope_to_envoy(scope_path, zone=2)

    def test_empty_targets_raises(self, scope_dir: Path) -> None:
        """Scope with empty authorized_targets raises error."""
        scope_dir.mkdir(parents=True, exist_ok=True)
        scope_path = scope_dir / "empty.yaml"
        scope_data = {
            "engagement": {
                "engagement_id": "RBW-0004",
                "authorized_targets": [],
            }
        }
        scope_path.write_text(yaml.dump(scope_data))
        with pytest.raises(ScopeTranslationError, match="No authorized_targets"):
            translate_scope_to_envoy(scope_path, zone=2)

    def test_ip_range_rejected(self, scope_dir: Path) -> None:
        """ip_range targets are rejected in Phase 1."""
        scope_dir.mkdir(parents=True, exist_ok=True)
        scope_path = scope_dir / "iprange.yaml"
        scope_data = {
            "engagement": {
                "engagement_id": "RBW-0005",
                "authorized_targets": [
                    {"type": "ip_range", "value": "10.0.0.0/24"},
                ],
            }
        }
        scope_path.write_text(yaml.dump(scope_data))
        with pytest.raises(ScopeTranslationError, match="ip_range.*not supported"):
            translate_scope_to_envoy(scope_path, zone=2)

    def test_invalid_domain_rejected(self, scope_dir: Path) -> None:
        """Invalid domain format is rejected."""
        scope_dir.mkdir(parents=True, exist_ok=True)
        scope_path = scope_dir / "baddom.yaml"
        scope_data = {
            "engagement": {
                "engagement_id": "RBW-0006",
                "authorized_targets": [
                    {"type": "domain", "value": "not a valid domain!"},
                ],
            }
        }
        scope_path.write_text(yaml.dump(scope_data))
        with pytest.raises(ScopeTranslationError, match="Invalid domain"):
            translate_scope_to_envoy(scope_path, zone=2)

    def test_invalid_ip_rejected(self, scope_dir: Path) -> None:
        """Invalid IP address is rejected."""
        scope_dir.mkdir(parents=True, exist_ok=True)
        scope_path = scope_dir / "badip.yaml"
        scope_data = {
            "engagement": {
                "engagement_id": "RBW-0007",
                "authorized_targets": [
                    {"type": "ip", "value": "999.999.999.999"},
                ],
            }
        }
        scope_path.write_text(yaml.dump(scope_data))
        with pytest.raises(ScopeTranslationError, match="Invalid IPv4"):
            translate_scope_to_envoy(scope_path, zone=2)

    def test_unknown_cloud_provider_rejected(self, scope_dir: Path) -> None:
        """Unknown cloud provider in cloud_account is rejected."""
        scope_dir.mkdir(parents=True, exist_ok=True)
        scope_path = scope_dir / "badcloud.yaml"
        scope_data = {
            "engagement": {
                "engagement_id": "RBW-0008",
                "authorized_targets": [
                    {"type": "cloud_account", "value": "oracle:12345"},
                ],
            }
        }
        scope_path.write_text(yaml.dump(scope_data))
        with pytest.raises(ScopeTranslationError, match="Unknown cloud provider"):
            translate_scope_to_envoy(scope_path, zone=2)


class TestGenerateEnvoyConfig:
    """Test full Envoy config generation."""

    def test_generates_valid_yaml(
        self, zone2_base_config: Path, basic_scope: Path, tmp_path: Path
    ) -> None:
        """Generated config is valid YAML."""
        output = tmp_path / "generated.yaml"
        generate_envoy_config(zone2_base_config, basic_scope, output, zone=2)
        assert output.exists()
        with output.open() as f:
            config = yaml.safe_load(f)
        assert config is not None

    def test_scope_hosts_before_deny_all(
        self, zone2_base_config: Path, basic_scope: Path, tmp_path: Path
    ) -> None:
        """Scope-derived virtual_hosts are inserted BEFORE deny_all."""
        output = tmp_path / "generated.yaml"
        generate_envoy_config(zone2_base_config, basic_scope, output, zone=2)
        with output.open() as f:
            config = yaml.safe_load(f)
        hcm = config["static_resources"]["listeners"][0]["filter_chains"][0]["filters"][0][
            "typed_config"
        ]
        virtual_hosts = hcm["route_config"]["virtual_hosts"]
        # deny_all must still be last
        assert virtual_hosts[-1]["name"] == "deny_all"
        # scope hosts must be before deny_all
        assert len(virtual_hosts) >= 2
        assert virtual_hosts[0]["name"] == "engagement_scope_zone2"

    def test_deny_all_preserved(
        self, zone2_base_config: Path, basic_scope: Path, tmp_path: Path
    ) -> None:
        """deny_all catch-all must be preserved after injection."""
        output = tmp_path / "generated.yaml"
        generate_envoy_config(zone2_base_config, basic_scope, output, zone=2)
        with output.open() as f:
            config = yaml.safe_load(f)
        hcm = config["static_resources"]["listeners"][0]["filter_chains"][0]["filters"][0][
            "typed_config"
        ]
        virtual_hosts = hcm["route_config"]["virtual_hosts"]
        deny_all = next((vh for vh in virtual_hosts if vh.get("name") == "deny_all"), None)
        assert deny_all is not None
        assert deny_all["routes"][0]["direct_response"]["status"] == 403

    def test_zone3_with_c2(
        self, zone2_base_config: Path, mixed_scope: Path, tmp_path: Path
    ) -> None:
        """Zone 3 config includes C2 infrastructure when flagged."""
        output = tmp_path / "generated-z3.yaml"
        generate_envoy_config(zone2_base_config, mixed_scope, output, zone=3, include_c2=True)
        with output.open() as f:
            config = yaml.safe_load(f)
        hcm = config["static_resources"]["listeners"][0]["filter_chains"][0]["filters"][0][
            "typed_config"
        ]
        virtual_hosts = hcm["route_config"]["virtual_hosts"]
        scope_vh = virtual_hosts[0]
        assert "c2.attacker.com" in scope_vh["domains"]
        assert "198.51.100.10" in scope_vh["domains"]

    def test_output_has_generation_header(
        self, zone2_base_config: Path, basic_scope: Path, tmp_path: Path
    ) -> None:
        """Generated config must have a header comment indicating source."""
        output = tmp_path / "generated.yaml"
        generate_envoy_config(zone2_base_config, basic_scope, output, zone=2)
        content = output.read_text()
        assert "GENERATED by scope_translator.py" in content
        assert "DO NOT EDIT MANUALLY" in content


class TestCloudAccountMapping:
    """Test cloud provider to API domain mapping."""

    def test_aws_mapping(self, scope_dir: Path) -> None:
        """AWS cloud_account produces AWS API domains."""
        scope_dir.mkdir(parents=True, exist_ok=True)
        scope_path = scope_dir / "aws.yaml"
        scope_data = {
            "engagement": {
                "engagement_id": "RBW-0010",
                "authorized_targets": [
                    {"type": "cloud_account", "value": "aws:123456789012"},
                ],
            }
        }
        scope_path.write_text(yaml.dump(scope_data))
        vhosts = translate_scope_to_envoy(scope_path, zone=2)
        domains = vhosts[0]["domains"]
        assert any("amazonaws" in d for d in domains)

    def test_azure_mapping(self, scope_dir: Path) -> None:
        """Azure cloud_account produces Azure API domains."""
        scope_dir.mkdir(parents=True, exist_ok=True)
        scope_path = scope_dir / "azure.yaml"
        scope_data = {
            "engagement": {
                "engagement_id": "RBW-0011",
                "authorized_targets": [
                    {"type": "cloud_account", "value": "azure:sub-id-12345"},
                ],
            }
        }
        scope_path.write_text(yaml.dump(scope_data))
        vhosts = translate_scope_to_envoy(scope_path, zone=2)
        domains = vhosts[0]["domains"]
        assert any("azure" in d for d in domains)

    def test_gcp_mapping(self, scope_dir: Path) -> None:
        """GCP cloud_account produces GCP API domains."""
        scope_dir.mkdir(parents=True, exist_ok=True)
        scope_path = scope_dir / "gcp.yaml"
        scope_data = {
            "engagement": {
                "engagement_id": "RBW-0012",
                "authorized_targets": [
                    {"type": "cloud_account", "value": "gcp:my-project-id"},
                ],
            }
        }
        scope_path.write_text(yaml.dump(scope_data))
        vhosts = translate_scope_to_envoy(scope_path, zone=2)
        domains = vhosts[0]["domains"]
        assert any("googleapis" in d for d in domains)
