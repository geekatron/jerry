# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""BDD test suite for engagement config parsing and SSH keypair generation.

STORY-023-007: Engagement Config File Bootstrap
Tasks covered:
  - TASK-023-049: BDD tests for engagement config parsing and keypair generation (RED)
  - TASK-023-050: Engagement config YAML schema, parser, and validator
  - TASK-023-051: SSH keypair generation infrastructure adapter
  - TASK-023-052: jerry proxy engage CLI command

RED PHASE (H-20): All tests MUST FAIL before implementation exists.

Covers:
  - EngagementConfig value object: valid construction, field validation, invariants
  - EngagementConfigParser: YAML parsing, missing fields, invalid values
  - SshKeygenAdapter: Ed25519 keypair generation, file permissions, comment format
  - engage_command: CLI composition root wiring config → keygen → provision

Test pyramid: 60% happy path / 30% negative / 10% edge cases
Naming convention: test_{scenario}_when_{condition}_then_{expected}
"""

from __future__ import annotations

import os
import stat
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import yaml


# =============================================================================
# EngagementConfig value object tests
# =============================================================================


class TestEngagementConfigValueObject:
    """Tests for the EngagementConfig frozen dataclass."""

    def test_valid_config_when_all_required_fields_then_constructs(self) -> None:
        """Happy path: valid YAML fields produce a valid config object."""
        from src.proxy_infra.domain.value_objects.engagement_config import EngagementConfig

        config = EngagementConfig(
            engagement_id="ENG-001",
            provider="digitalocean",
            region="nyc1",
            count=3,
            proxy_type="direct_socks5",
            socks_port=1080,
            operator_ip="174.7.155.69",
        )
        assert config.engagement_id == "ENG-001"
        assert config.provider == "digitalocean"
        assert config.region == "nyc1"
        assert config.count == 3
        assert config.socks_port == 1080

    def test_config_when_missing_engagement_id_then_raises(self) -> None:
        """Empty engagement_id must be rejected."""
        from src.proxy_infra.domain.value_objects.engagement_config import EngagementConfig

        with pytest.raises(ValueError, match="engagement_id"):
            EngagementConfig(
                engagement_id="",
                provider="digitalocean",
                region="nyc1",
                count=3,
                proxy_type="direct_socks5",
                socks_port=1080,
                operator_ip="174.7.155.69",
            )

    def test_config_when_count_exceeds_limit_then_raises(self) -> None:
        """Count > 10 must be rejected per RATELIMIT-006."""
        from src.proxy_infra.domain.value_objects.engagement_config import EngagementConfig

        with pytest.raises(ValueError, match="count"):
            EngagementConfig(
                engagement_id="ENG-001",
                provider="digitalocean",
                region="nyc1",
                count=11,
                proxy_type="direct_socks5",
                socks_port=1080,
                operator_ip="174.7.155.69",
            )

    def test_config_when_empty_operator_ip_then_raises(self) -> None:
        """Empty operator_ip must be rejected — firewall needs this."""
        from src.proxy_infra.domain.value_objects.engagement_config import EngagementConfig

        with pytest.raises(ValueError, match="operator_ip"):
            EngagementConfig(
                engagement_id="ENG-001",
                provider="digitalocean",
                region="nyc1",
                count=3,
                proxy_type="direct_socks5",
                socks_port=1080,
                operator_ip="",
            )

    def test_config_when_empty_provider_then_raises(self) -> None:
        """Empty provider must be rejected."""
        from src.proxy_infra.domain.value_objects.engagement_config import EngagementConfig

        with pytest.raises(ValueError, match="provider"):
            EngagementConfig(
                engagement_id="ENG-001",
                provider="",
                region="nyc1",
                count=3,
                proxy_type="direct_socks5",
                socks_port=1080,
                operator_ip="174.7.155.69",
            )

    def test_config_when_zero_count_then_raises(self) -> None:
        """Count must be at least 1."""
        from src.proxy_infra.domain.value_objects.engagement_config import EngagementConfig

        with pytest.raises(ValueError, match="count"):
            EngagementConfig(
                engagement_id="ENG-001",
                provider="digitalocean",
                region="nyc1",
                count=0,
                proxy_type="direct_socks5",
                socks_port=1080,
                operator_ip="174.7.155.69",
            )

    def test_config_is_frozen(self) -> None:
        """EngagementConfig must be immutable."""
        from src.proxy_infra.domain.value_objects.engagement_config import EngagementConfig

        config = EngagementConfig(
            engagement_id="ENG-001",
            provider="digitalocean",
            region="nyc1",
            count=3,
            proxy_type="direct_socks5",
            socks_port=1080,
            operator_ip="174.7.155.69",
        )
        with pytest.raises(AttributeError):
            config.count = 5  # type: ignore[misc]

    def test_config_generates_engagement_tag(self) -> None:
        """Config should derive engagement_tag from engagement_id for ISOLATION-001."""
        from src.proxy_infra.domain.value_objects.engagement_config import EngagementConfig

        config = EngagementConfig(
            engagement_id="ENG-001",
            provider="digitalocean",
            region="nyc1",
            count=3,
            proxy_type="direct_socks5",
            socks_port=1080,
            operator_ip="174.7.155.69",
        )
        assert config.engagement_tag
        assert "ENG-001" in config.engagement_tag.lower() or "eng-001" in config.engagement_tag.lower()

    def test_config_defaults_when_optional_fields_omitted(self) -> None:
        """Optional fields (image, size) should have sensible defaults."""
        from src.proxy_infra.domain.value_objects.engagement_config import EngagementConfig

        config = EngagementConfig(
            engagement_id="ENG-001",
            provider="digitalocean",
            region="nyc1",
            count=1,
            proxy_type="direct_socks5",
            socks_port=1080,
            operator_ip="174.7.155.69",
        )
        assert config.image == "ubuntu-24-04-x64"
        assert config.size == "s-1vcpu-1gb"


# =============================================================================
# EngagementConfigParser tests
# =============================================================================


class TestEngagementConfigParser:
    """Tests for YAML file parsing into EngagementConfig."""

    def _write_yaml(self, tmp_path: Path, data: dict) -> Path:
        """Helper: write a dict as YAML to a temp file."""
        config_file = tmp_path / "engagement.yaml"
        config_file.write_text(yaml.dump(data), encoding="utf-8")
        return config_file

    def test_parse_when_valid_yaml_then_returns_config(self, tmp_path: Path) -> None:
        """Happy path: valid YAML produces EngagementConfig."""
        from src.proxy_infra.application.handlers.engagement_config_parser import (
            EngagementConfigParser,
        )

        config_file = self._write_yaml(tmp_path, {
            "engagement_id": "ENG-001",
            "provider": "digitalocean",
            "region": "nyc1",
            "count": 3,
            "proxy_type": "direct_socks5",
            "socks_port": 1080,
            "operator_ip": "174.7.155.69",
        })
        parser = EngagementConfigParser()
        config = parser.parse(config_file)
        assert config.engagement_id == "ENG-001"
        assert config.count == 3

    def test_parse_when_missing_required_field_then_raises_with_field_name(
        self, tmp_path: Path
    ) -> None:
        """Missing engagement_id should produce an actionable error."""
        from src.proxy_infra.application.handlers.engagement_config_parser import (
            EngagementConfigParser,
        )

        config_file = self._write_yaml(tmp_path, {
            "provider": "digitalocean",
            "region": "nyc1",
            "count": 3,
            "proxy_type": "direct_socks5",
            "socks_port": 1080,
            "operator_ip": "174.7.155.69",
        })
        parser = EngagementConfigParser()
        with pytest.raises(ValueError, match="engagement_id"):
            parser.parse(config_file)

    def test_parse_when_file_not_found_then_raises(self, tmp_path: Path) -> None:
        """Non-existent file should raise FileNotFoundError."""
        from src.proxy_infra.application.handlers.engagement_config_parser import (
            EngagementConfigParser,
        )

        parser = EngagementConfigParser()
        with pytest.raises(FileNotFoundError):
            parser.parse(tmp_path / "nonexistent.yaml")

    def test_parse_when_invalid_yaml_then_raises(self, tmp_path: Path) -> None:
        """Malformed YAML should raise a clear error."""
        from src.proxy_infra.application.handlers.engagement_config_parser import (
            EngagementConfigParser,
        )

        config_file = tmp_path / "engagement.yaml"
        config_file.write_text("{ broken yaml: [", encoding="utf-8")
        parser = EngagementConfigParser()
        with pytest.raises((ValueError, yaml.YAMLError)):
            parser.parse(config_file)

    def test_parse_when_count_exceeds_limit_then_raises(self, tmp_path: Path) -> None:
        """Count > 10 in YAML should be rejected at parse time."""
        from src.proxy_infra.application.handlers.engagement_config_parser import (
            EngagementConfigParser,
        )

        config_file = self._write_yaml(tmp_path, {
            "engagement_id": "ENG-001",
            "provider": "digitalocean",
            "region": "nyc1",
            "count": 15,
            "proxy_type": "direct_socks5",
            "socks_port": 1080,
            "operator_ip": "174.7.155.69",
        })
        parser = EngagementConfigParser()
        with pytest.raises(ValueError, match="count"):
            parser.parse(config_file)


# =============================================================================
# SshKeygenAdapter tests
# =============================================================================


class TestSshKeygenAdapter:
    """Tests for SSH Ed25519 keypair generation infrastructure adapter."""

    def test_generate_when_valid_engagement_then_produces_keypair(self, tmp_path: Path) -> None:
        """Happy path: generates Ed25519 private + public key files."""
        from src.proxy_infra.infrastructure.keygen.ssh_keygen_adapter import SshKeygenAdapter

        adapter = SshKeygenAdapter()
        result = adapter.generate(
            engagement_id="ENG-001",
            credential_dir=tmp_path,
        )
        assert result.private_key_path.exists()
        assert result.public_key_path.exists()

    def test_generate_when_valid_then_private_key_has_0600_permissions(
        self, tmp_path: Path
    ) -> None:
        """Private key must be 0600 (owner read/write only)."""
        from src.proxy_infra.infrastructure.keygen.ssh_keygen_adapter import SshKeygenAdapter

        adapter = SshKeygenAdapter()
        result = adapter.generate(
            engagement_id="ENG-001",
            credential_dir=tmp_path,
        )
        mode = stat.S_IMODE(os.stat(result.private_key_path).st_mode)
        assert mode == 0o600

    def test_generate_when_valid_then_public_key_readable_as_string(
        self, tmp_path: Path
    ) -> None:
        """Public key content must be a valid OpenSSH public key string."""
        from src.proxy_infra.infrastructure.keygen.ssh_keygen_adapter import SshKeygenAdapter

        adapter = SshKeygenAdapter()
        result = adapter.generate(
            engagement_id="ENG-001",
            credential_dir=tmp_path,
        )
        pub_content = result.public_key_path.read_text(encoding="utf-8").strip()
        assert pub_content.startswith("ssh-ed25519 ")

    def test_generate_when_valid_then_key_comment_contains_engagement_id(
        self, tmp_path: Path
    ) -> None:
        """SSH key comment should contain the engagement ID for traceability."""
        from src.proxy_infra.infrastructure.keygen.ssh_keygen_adapter import SshKeygenAdapter

        adapter = SshKeygenAdapter()
        result = adapter.generate(
            engagement_id="ENG-001",
            credential_dir=tmp_path,
        )
        pub_content = result.public_key_path.read_text(encoding="utf-8").strip()
        assert "ENG-001" in pub_content

    def test_generate_when_credential_dir_missing_then_raises(self) -> None:
        """Non-existent credential directory should raise."""
        from src.proxy_infra.infrastructure.keygen.ssh_keygen_adapter import SshKeygenAdapter

        adapter = SshKeygenAdapter()
        with pytest.raises((NotADirectoryError, FileNotFoundError)):
            adapter.generate(
                engagement_id="ENG-001",
                credential_dir=Path("/nonexistent/path"),
            )

    def test_generate_returns_keygen_result_with_both_paths(self, tmp_path: Path) -> None:
        """Result object must expose both private_key_path and public_key_path."""
        from src.proxy_infra.infrastructure.keygen.ssh_keygen_adapter import SshKeygenAdapter

        adapter = SshKeygenAdapter()
        result = adapter.generate(
            engagement_id="ENG-001",
            credential_dir=tmp_path,
        )
        assert hasattr(result, "private_key_path")
        assert hasattr(result, "public_key_path")
        assert result.private_key_path != result.public_key_path


# =============================================================================
# engage_command CLI tests
# =============================================================================


class TestEngageCommand:
    """Tests for the jerry proxy engage CLI composition root."""

    def _write_valid_yaml(self, tmp_path: Path) -> Path:
        """Helper: write a valid engagement YAML config."""
        config_file = tmp_path / "engagement.yaml"
        config_file.write_text(yaml.dump({
            "engagement_id": "ENG-001",
            "provider": "digitalocean",
            "region": "nyc1",
            "count": 3,
            "proxy_type": "direct_socks5",
            "socks_port": 1080,
            "operator_ip": "174.7.155.69",
        }), encoding="utf-8")
        return config_file

    def test_engage_when_valid_config_then_provisions_nodes(self, tmp_path: Path) -> None:
        """Happy path: engage parses config, generates keys, provisions."""
        from src.proxy_infra.interface.cli.proxy_commands import engage_command

        config_file = self._write_valid_yaml(tmp_path)
        adapter = MagicMock()
        adapter.provision.return_value = [MagicMock(id="node-1", ip="1.2.3.4")]
        audit = MagicMock()

        result = engage_command(
            config_path=config_file,
            adapter=adapter,
            audit_store=audit,
            credential_dir=tmp_path / "credentials",
        )
        assert len(result) >= 1
        adapter.provision.assert_called_once()

    def test_engage_when_valid_config_then_creates_credential_dir(self, tmp_path: Path) -> None:
        """Credential directory should be created with 0700 permissions."""
        from src.proxy_infra.interface.cli.proxy_commands import engage_command

        config_file = self._write_valid_yaml(tmp_path)
        cred_dir = tmp_path / "credentials"
        adapter = MagicMock()
        adapter.provision.return_value = [MagicMock(id="node-1", ip="1.2.3.4")]
        audit = MagicMock()

        engage_command(
            config_path=config_file,
            adapter=adapter,
            audit_store=audit,
            credential_dir=cred_dir,
        )
        assert cred_dir.exists()
        mode = stat.S_IMODE(os.stat(cred_dir).st_mode)
        assert mode == 0o700

    def test_engage_when_valid_config_then_ssh_keypair_generated(self, tmp_path: Path) -> None:
        """SSH keypair files should exist in credential directory after engage."""
        from src.proxy_infra.interface.cli.proxy_commands import engage_command

        config_file = self._write_valid_yaml(tmp_path)
        cred_dir = tmp_path / "credentials"
        adapter = MagicMock()
        adapter.provision.return_value = [MagicMock(id="node-1", ip="1.2.3.4")]
        audit = MagicMock()

        engage_command(
            config_path=config_file,
            adapter=adapter,
            audit_store=audit,
            credential_dir=cred_dir,
        )
        # Private key and public key files should exist
        key_files = list(cred_dir.glob("id_ed25519_*"))
        assert len(key_files) >= 2  # private + public

    def test_engage_when_invalid_config_then_raises_before_provision(
        self, tmp_path: Path
    ) -> None:
        """Invalid config should fail before provisioning — no cloud API call."""
        from src.proxy_infra.interface.cli.proxy_commands import engage_command

        config_file = tmp_path / "engagement.yaml"
        config_file.write_text(yaml.dump({"provider": "digitalocean"}), encoding="utf-8")
        adapter = MagicMock()
        audit = MagicMock()

        with pytest.raises((ValueError, KeyError)):
            engage_command(
                config_path=config_file,
                adapter=adapter,
                audit_store=audit,
                credential_dir=tmp_path / "credentials",
            )
        adapter.provision.assert_not_called()

    def test_engage_when_valid_then_public_key_passed_to_provision_config(
        self, tmp_path: Path
    ) -> None:
        """The generated public key content must be in the ProvisionConfig."""
        from src.proxy_infra.interface.cli.proxy_commands import engage_command

        config_file = self._write_valid_yaml(tmp_path)
        adapter = MagicMock()
        adapter.provision.return_value = [MagicMock(id="node-1", ip="1.2.3.4")]
        audit = MagicMock()

        engage_command(
            config_path=config_file,
            adapter=adapter,
            audit_store=audit,
            credential_dir=tmp_path / "credentials",
        )
        # The provision call should receive a ProvisionConfig with a non-empty ssh_public_key
        call_args = adapter.provision.call_args
        provision_config = call_args[0][0] if call_args[0] else call_args[1].get("config")
        assert provision_config.ssh_public_key
        assert provision_config.ssh_public_key.startswith("ssh-ed25519 ")
