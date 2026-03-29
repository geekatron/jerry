# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""RED phase tests for TASK-023-102: State Parser.

Tests verify:
1. Extraction of droplet_ip, droplet_id, ssh_key_id, firewall_id from terraform output JSON
2. ProxyNode construction from parsed output
3. chmod 600 applied to state files after write

All tests MUST FAIL before implementation (H-20 RED phase).
"""

from __future__ import annotations

import json
from pathlib import Path


class TestStateParserOutputJson:
    """Tests for parsing terraform output -json responses."""

    def test_parse_output_json_extracts_droplet_ip(self) -> None:
        """State parser must extract droplet IP from terraform output JSON."""
        from src.proxy_infra.infrastructure.terraform.state_parser import (
            StateParser,
        )

        output_json = {
            "droplet_ip": {"value": "104.131.1.1", "type": "string"},
            "droplet_id": {"value": "123456", "type": "string"},
            "ssh_key_id": {"value": "42424242", "type": "string"},
            "firewall_id": {"value": "fw-abcdef", "type": "string"},
        }

        parser = StateParser()
        result = parser.parse_output(output_json)

        assert result["droplet_ip"] == "104.131.1.1"

    def test_parse_output_json_extracts_droplet_id(self) -> None:
        """State parser must extract droplet ID from terraform output JSON."""
        from src.proxy_infra.infrastructure.terraform.state_parser import (
            StateParser,
        )

        output_json = {
            "droplet_ip": {"value": "104.131.1.1", "type": "string"},
            "droplet_id": {"value": "123456", "type": "string"},
            "ssh_key_id": {"value": "42424242", "type": "string"},
            "firewall_id": {"value": "fw-abcdef", "type": "string"},
        }

        parser = StateParser()
        result = parser.parse_output(output_json)

        assert result["droplet_id"] == "123456"

    def test_parse_output_json_extracts_ssh_key_id(self) -> None:
        """State parser must extract SSH key ID from terraform output JSON."""
        from src.proxy_infra.infrastructure.terraform.state_parser import (
            StateParser,
        )

        output_json = {
            "droplet_ip": {"value": "104.131.1.1", "type": "string"},
            "droplet_id": {"value": "123456", "type": "string"},
            "ssh_key_id": {"value": "42424242", "type": "string"},
            "firewall_id": {"value": "fw-abcdef", "type": "string"},
        }

        parser = StateParser()
        result = parser.parse_output(output_json)

        assert result["ssh_key_id"] == "42424242"

    def test_parse_output_json_extracts_firewall_id(self) -> None:
        """State parser must extract firewall ID from terraform output JSON."""
        from src.proxy_infra.infrastructure.terraform.state_parser import (
            StateParser,
        )

        output_json = {
            "droplet_ip": {"value": "104.131.1.1", "type": "string"},
            "droplet_id": {"value": "123456", "type": "string"},
            "ssh_key_id": {"value": "42424242", "type": "string"},
            "firewall_id": {"value": "fw-abcdef", "type": "string"},
        }

        parser = StateParser()
        result = parser.parse_output(output_json)

        assert result["firewall_id"] == "fw-abcdef"


class TestStateParserProxyNode:
    """Tests for ProxyNode construction from parsed output."""

    def test_parse_output_json_constructs_proxy_node(self) -> None:
        """State parser must construct a ProxyNode from terraform output."""
        from src.proxy_infra.infrastructure.terraform.state_parser import (
            StateParser,
        )

        output_json = {
            "droplet_ip": {"value": "104.131.1.1", "type": "string"},
            "droplet_id": {"value": "123456", "type": "string"},
            "ssh_key_id": {"value": "42424242", "type": "string"},
            "firewall_id": {"value": "fw-abcdef", "type": "string"},
        }

        parser = StateParser()
        node = parser.to_proxy_node(
            output_json,
            engagement_id="RED-TEST-001",
            region="nyc3",
            socks_port=1080,
        )

        assert node.id == "123456"
        assert node.ip == "104.131.1.1"
        assert node.provider == "digitalocean"
        assert node.region == "nyc3"
        assert node.ssh_key_id == "42424242"
        assert node.engagement_id == "RED-TEST-001"
        assert node.socks_port == 1080


class TestStateParserFilePermissions:
    """Tests for state file permission enforcement."""

    def test_state_file_chmod_600_after_write(self, tmp_path: Path) -> None:
        """chmod 600 must be applied to state files after write."""
        from src.proxy_infra.infrastructure.terraform.state_parser import (
            StateParser,
        )

        state_file = tmp_path / "terraform.tfstate"
        state_content = json.dumps({"version": 4, "resources": []})

        parser = StateParser()
        parser.write_state(state_file, state_content)

        file_mode = oct(state_file.stat().st_mode)[-3:]
        assert file_mode == "600", f"Expected chmod 600, got {file_mode}"
