# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""Unit tests for Envoy configuration file validation.

Task: T13-005
Validates that all Envoy config files are:
1. Valid YAML
2. Have required structure (admin, static_resources, listeners, clusters)
3. Have deny-by-default catch-all in virtual_hosts
4. Listen on port 3128 (forward proxy)
5. Have admin on port 9901
6. Have access logging configured
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

# Config directory relative to project root
ENVOY_CONFIG_DIR = Path(__file__).parents[4] / "skills" / "rainbow" / "config" / "envoy"

ZONE_CONFIGS = [
    "envoy-zone1-update.yaml",
    "envoy-zone2-active.yaml",
    "envoy-zone3-exploit.yaml",
]


@pytest.fixture(params=ZONE_CONFIGS)
def envoy_config(request: pytest.FixtureRequest) -> dict:
    """Load and parse an Envoy config file."""
    config_path = ENVOY_CONFIG_DIR / request.param
    assert config_path.exists(), f"Config file not found: {config_path}"
    with config_path.open() as f:
        config = yaml.safe_load(f)
    assert config is not None, f"Empty config: {config_path}"
    return config


@pytest.fixture(params=ZONE_CONFIGS)
def config_name(request: pytest.FixtureRequest) -> str:
    """Return the config file name."""
    return request.param


class TestEnvoyConfigStructure:
    """Validate Envoy config file structure."""

    def test_has_admin_section(self, envoy_config: dict) -> None:
        """Admin interface must be configured for health checks."""
        assert "admin" in envoy_config
        admin = envoy_config["admin"]
        assert "address" in admin

    def test_admin_port_9901(self, envoy_config: dict) -> None:
        """Admin must listen on port 9901 (matches Docker HEALTHCHECK)."""
        admin = envoy_config["admin"]
        port = admin["address"]["socket_address"]["port_value"]
        assert port == 9901

    def test_has_static_resources(self, envoy_config: dict) -> None:
        """Static resources must be present (listeners + clusters)."""
        assert "static_resources" in envoy_config
        sr = envoy_config["static_resources"]
        assert "listeners" in sr
        assert "clusters" in sr

    def test_listener_port_3128(self, envoy_config: dict) -> None:
        """Proxy listener must be on port 3128 (standard forward proxy port)."""
        listener = envoy_config["static_resources"]["listeners"][0]
        port = listener["address"]["socket_address"]["port_value"]
        assert port == 3128

    def test_listener_binds_all_interfaces(self, envoy_config: dict) -> None:
        """Proxy listener must bind 0.0.0.0 for Docker internal network access."""
        listener = envoy_config["static_resources"]["listeners"][0]
        addr = listener["address"]["socket_address"]["address"]
        assert addr == "0.0.0.0"


class TestDenyByDefault:
    """Validate deny-by-default catch-all behavior."""

    def test_has_deny_all_virtual_host(self, envoy_config: dict) -> None:
        """Every config must have a deny_all catch-all virtual_host."""
        hcm = _get_hcm(envoy_config)
        virtual_hosts = hcm["route_config"]["virtual_hosts"]
        deny_all = [
            vh for vh in virtual_hosts if vh.get("name") == "deny_all" or vh.get("domains") == ["*"]
        ]
        assert len(deny_all) >= 1, "Missing deny_all virtual_host"

    def test_deny_all_returns_403(self, envoy_config: dict) -> None:
        """deny_all must return HTTP 403."""
        hcm = _get_hcm(envoy_config)
        virtual_hosts = hcm["route_config"]["virtual_hosts"]
        deny_all = next(
            (vh for vh in virtual_hosts if vh.get("name") == "deny_all"),
            None,
        )
        assert deny_all is not None
        route = deny_all["routes"][0]
        assert route["direct_response"]["status"] == 403

    def test_deny_all_is_last(self, envoy_config: dict) -> None:
        """deny_all must be the last virtual_host (catch-all order matters)."""
        hcm = _get_hcm(envoy_config)
        virtual_hosts = hcm["route_config"]["virtual_hosts"]
        last_vh = virtual_hosts[-1]
        assert last_vh.get("name") == "deny_all" or last_vh.get("domains") == ["*"], (
            "deny_all must be the last virtual_host"
        )


class TestAccessLogging:
    """Validate access logging configuration."""

    def test_has_access_log(self, envoy_config: dict) -> None:
        """Access logging must be configured for forensic evidence."""
        hcm = _get_hcm(envoy_config)
        assert "access_log" in hcm
        access_logs = hcm["access_log"]
        assert len(access_logs) >= 1

    def test_access_log_json_format(self, envoy_config: dict) -> None:
        """Access log must use JSON format for structured parsing."""
        hcm = _get_hcm(envoy_config)
        log_config = hcm["access_log"][0]["typed_config"]
        assert "json_format" in log_config["log_format"]

    def test_access_log_has_zone_field(self, envoy_config: dict) -> None:
        """Access log must include zone identifier for multi-zone forensics."""
        hcm = _get_hcm(envoy_config)
        log_config = hcm["access_log"][0]["typed_config"]
        json_format = log_config["log_format"]["json_format"]
        assert "zone" in json_format

    def test_access_log_path(self, envoy_config: dict) -> None:
        """Access log path must be /var/log/envoy/access.log (volume-mounted)."""
        hcm = _get_hcm(envoy_config)
        log_config = hcm["access_log"][0]["typed_config"]
        assert log_config["path"] == "/var/log/envoy/access.log"


class TestConnectSupport:
    """Validate HTTPS CONNECT tunnel support."""

    def test_connect_upgrade_configured(self, envoy_config: dict) -> None:
        """CONNECT upgrade must be configured for HTTPS proxying."""
        hcm = _get_hcm(envoy_config)
        upgrades = hcm.get("upgrade_configs", [])
        connect_upgrades = [u for u in upgrades if u.get("upgrade_type") == "CONNECT"]
        assert len(connect_upgrades) >= 1, "CONNECT upgrade not configured"


class TestDynamicForwardProxy:
    """Validate dynamic forward proxy filter and cluster."""

    def test_has_dynamic_forward_proxy_filter(self, envoy_config: dict) -> None:
        """HTTP filters must include dynamic_forward_proxy."""
        hcm = _get_hcm(envoy_config)
        filters = hcm["http_filters"]
        dfp_filters = [f for f in filters if "dynamic_forward_proxy" in f.get("name", "")]
        assert len(dfp_filters) >= 1

    def test_has_dynamic_forward_proxy_cluster(self, envoy_config: dict) -> None:
        """Clusters must include dynamic_forward_proxy cluster."""
        clusters = envoy_config["static_resources"]["clusters"]
        dfp_clusters = [c for c in clusters if c.get("name") == "dynamic_forward_proxy_cluster"]
        assert len(dfp_clusters) >= 1


class TestZone1UpdateAllowlist:
    """Zone 1 specific: static allowlist validation."""

    @pytest.fixture()
    def zone1_config(self) -> dict:
        """Load Zone 1 update config."""
        config_path = ENVOY_CONFIG_DIR / "envoy-zone1-update.yaml"
        with config_path.open() as f:
            return yaml.safe_load(f)

    def test_has_allowed_db_hosts(self, zone1_config: dict) -> None:
        """Zone 1 must have the allowed_db_hosts virtual_host."""
        hcm = _get_hcm(zone1_config)
        virtual_hosts = hcm["route_config"]["virtual_hosts"]
        allowed = [vh for vh in virtual_hosts if vh.get("name") == "allowed_db_hosts"]
        assert len(allowed) == 1

    def test_github_in_allowlist(self, zone1_config: dict) -> None:
        """github.com must be in Zone 1 allowlist (release assets)."""
        domains = _get_zone1_domains(zone1_config)
        assert "github.com" in domains

    def test_nvd_in_allowlist(self, zone1_config: dict) -> None:
        """nvd.nist.gov must be in Zone 1 allowlist (vulnerability DB)."""
        domains = _get_zone1_domains(zone1_config)
        assert "nvd.nist.gov" in domains

    def test_osv_in_allowlist(self, zone1_config: dict) -> None:
        """osv.dev must be in Zone 1 allowlist (OSV API)."""
        domains = _get_zone1_domains(zone1_config)
        assert "osv.dev" in domains

    def test_pypi_in_allowlist(self, zone1_config: dict) -> None:
        """pypi.org must be in Zone 1 allowlist (package registry)."""
        domains = _get_zone1_domains(zone1_config)
        assert "pypi.org" in domains

    def test_sigstore_in_allowlist(self, zone1_config: dict) -> None:
        """Sigstore domains must be in Zone 1 allowlist (cosign TUF)."""
        domains = _get_zone1_domains(zone1_config)
        sigstore_domains = [d for d in domains if "sigstore" in d]
        assert len(sigstore_domains) >= 1

    def test_grype_db_in_allowlist(self, zone1_config: dict) -> None:
        """Anchore toolbox must be in Zone 1 allowlist (grype DB)."""
        domains = _get_zone1_domains(zone1_config)
        assert "toolbox-data.anchore.io" in domains


class TestZone3ExploitLogging:
    """Zone 3 specific: enhanced logging validation."""

    @pytest.fixture()
    def zone3_config(self) -> dict:
        """Load Zone 3 exploit config."""
        config_path = ENVOY_CONFIG_DIR / "envoy-zone3-exploit.yaml"
        with config_path.open() as f:
            return yaml.safe_load(f)

    def test_logs_user_agent(self, zone3_config: dict) -> None:
        """Zone 3 must log User-Agent header for forensic evidence."""
        hcm = _get_hcm(zone3_config)
        json_format = hcm["access_log"][0]["typed_config"]["log_format"]["json_format"]
        assert "user_agent" in json_format

    def test_logs_auth_presence(self, zone3_config: dict) -> None:
        """Zone 3 must log Authorization header presence for credential detection."""
        hcm = _get_hcm(zone3_config)
        json_format = hcm["access_log"][0]["typed_config"]["log_format"]["json_format"]
        assert "auth_present" in json_format


# --- Helpers ---


def _get_hcm(config: dict) -> dict:
    """Extract the HttpConnectionManager typed_config from an Envoy config."""
    listener = config["static_resources"]["listeners"][0]
    hcm_filter = listener["filter_chains"][0]["filters"][0]
    return hcm_filter["typed_config"]


def _get_zone1_domains(config: dict) -> list[str]:
    """Get the domains from the Zone 1 allowed_db_hosts virtual_host."""
    hcm = _get_hcm(config)
    virtual_hosts = hcm["route_config"]["virtual_hosts"]
    allowed = next(vh for vh in virtual_hosts if vh.get("name") == "allowed_db_hosts")
    return allowed["domains"]
