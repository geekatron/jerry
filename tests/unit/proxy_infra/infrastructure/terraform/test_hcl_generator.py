# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""RED phase tests for TASK-023-101: HCL Generator with DO Jinja2 Template.

Tests verify:
1. Generated HCL contains all required DigitalOcean resources
2. Cloud-init user_data matches spec
3. Firewall rules restrict to operator IP
4. Output blocks expose IP and IDs
5. Provider version pinned (not ~>)
6. Input validation raises on missing required fields
7. Output written to correct engagement directory

All tests MUST FAIL before implementation (H-20 RED phase).
"""

from __future__ import annotations

from pathlib import Path

import pytest


class TestHclGeneratorResources:
    """Tests for resource declarations in generated HCL."""

    def test_hcl_output_contains_digitalocean_ssh_key_resource(self, tmp_path: Path) -> None:
        """Generated HCL must include a digitalocean_ssh_key resource."""
        from src.proxy_infra.infrastructure.terraform.hcl_generator import (
            HclGenerator,
        )

        generator = HclGenerator(template_dir=_template_dir())
        config = _valid_config()

        result_path = generator.generate(config, work_dir=tmp_path)

        content = result_path.read_text()
        assert 'resource "digitalocean_ssh_key"' in content

    def test_hcl_output_contains_digitalocean_droplet_resource(self, tmp_path: Path) -> None:
        """Generated HCL must include a digitalocean_droplet resource."""
        from src.proxy_infra.infrastructure.terraform.hcl_generator import (
            HclGenerator,
        )

        generator = HclGenerator(template_dir=_template_dir())
        config = _valid_config()

        result_path = generator.generate(config, work_dir=tmp_path)

        content = result_path.read_text()
        assert 'resource "digitalocean_droplet"' in content

    def test_hcl_output_contains_digitalocean_firewall_resource(self, tmp_path: Path) -> None:
        """Generated HCL must include a digitalocean_firewall resource."""
        from src.proxy_infra.infrastructure.terraform.hcl_generator import (
            HclGenerator,
        )

        generator = HclGenerator(template_dir=_template_dir())
        config = _valid_config()

        result_path = generator.generate(config, work_dir=tmp_path)

        content = result_path.read_text()
        assert 'resource "digitalocean_firewall"' in content


class TestHclGeneratorContent:
    """Tests for content correctness of generated HCL."""

    def test_hcl_user_data_matches_cloud_init_spec(self, tmp_path: Path) -> None:
        """user_data field must contain cloud-init YAML with microsocks and ufw."""
        from src.proxy_infra.infrastructure.terraform.hcl_generator import (
            HclGenerator,
        )

        generator = HclGenerator(template_dir=_template_dir())
        config = _valid_config()

        result_path = generator.generate(config, work_dir=tmp_path)

        content = result_path.read_text()
        assert "user_data" in content
        assert "microsocks" in content
        assert "ufw" in content
        assert "#cloud-config" in content

    def test_hcl_firewall_rules_restrict_to_operator_ip(self, tmp_path: Path) -> None:
        """Firewall inbound rules must restrict to operator IP from config."""
        from src.proxy_infra.infrastructure.terraform.hcl_generator import (
            HclGenerator,
        )

        generator = HclGenerator(template_dir=_template_dir())
        config = _valid_config()

        result_path = generator.generate(config, work_dir=tmp_path)

        content = result_path.read_text()
        assert "198.51.100.1/32" in content

    def test_hcl_output_blocks_expose_ip_and_ids(self, tmp_path: Path) -> None:
        """Output blocks for droplet_ip, droplet_id, ssh_key_id, firewall_id must exist."""
        from src.proxy_infra.infrastructure.terraform.hcl_generator import (
            HclGenerator,
        )

        generator = HclGenerator(template_dir=_template_dir())
        config = _valid_config()

        result_path = generator.generate(config, work_dir=tmp_path)

        content = result_path.read_text()
        assert 'output "droplet_ip"' in content
        assert 'output "droplet_id"' in content
        assert 'output "ssh_key_id"' in content
        assert 'output "firewall_id"' in content

    def test_hcl_provider_version_pinned(self, tmp_path: Path) -> None:
        """required_providers must pin exact DO provider version (= not ~>)."""
        from src.proxy_infra.infrastructure.terraform.hcl_generator import (
            HclGenerator,
        )

        generator = HclGenerator(template_dir=_template_dir())
        config = _valid_config()

        result_path = generator.generate(config, work_dir=tmp_path)

        content = result_path.read_text()
        assert "digitalocean/digitalocean" in content
        # Must use exact pin (= "X.Y.Z") not approximate (~> X.Y)
        assert '= "' in content or '= "' in content


class TestHclGeneratorValidation:
    """Tests for input validation."""

    def test_invalid_config_missing_region_raises_validation_error(self, tmp_path: Path) -> None:
        """Missing region must raise ValidationError."""
        from src.proxy_infra.infrastructure.terraform.hcl_generator import (
            HclGenerator,
        )

        generator = HclGenerator(template_dir=_template_dir())
        config = _valid_config()
        config["region"] = ""

        with pytest.raises(ValueError, match="region"):
            generator.generate(config, work_dir=tmp_path)

    def test_invalid_config_missing_size_raises_validation_error(self, tmp_path: Path) -> None:
        """Missing size must raise ValidationError."""
        from src.proxy_infra.infrastructure.terraform.hcl_generator import (
            HclGenerator,
        )

        generator = HclGenerator(template_dir=_template_dir())
        config = _valid_config()
        config["size"] = ""

        with pytest.raises(ValueError, match="size"):
            generator.generate(config, work_dir=tmp_path)

    def test_hcl_written_to_engagement_dir(self, tmp_path: Path) -> None:
        """Output main.tf must be written to the specified work directory."""
        from src.proxy_infra.infrastructure.terraform.hcl_generator import (
            HclGenerator,
        )

        generator = HclGenerator(template_dir=_template_dir())
        config = _valid_config()

        result_path = generator.generate(config, work_dir=tmp_path)

        assert result_path == tmp_path / "main.tf"
        assert result_path.exists()


# --- Test helpers ---


def _template_dir() -> Path:
    """Return path to the production Jinja2 templates directory."""
    return Path("infra/terraform/modules")


def _valid_config() -> dict[str, str | int]:
    """Return a valid engagement config dict for testing."""
    return {
        "engagement_id": "RED-TEST-001",
        "region": "nyc3",
        "size": "s-1vcpu-1gb",
        "image": "ubuntu-24-04-x64",
        "ssh_public_key": "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA test@poc",
        "operator_ip": "198.51.100.1",
        "socks_port": 1080,
    }
