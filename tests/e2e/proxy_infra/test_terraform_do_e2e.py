# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""E2E test: Real DigitalOcean droplet via TerraformProvisionerAdapter.

This test provisions a real DO droplet via terraform, waits for SSH,
verifies the node, and destroys it. It requires:
- DO API key in macOS Keychain (service=jerry, account=proxy.digitalocean.api-key)
- terraform >= 1.0.0 in PATH
- age + age-keygen in PATH
- Internet connectivity

Marks Go/No-Go criterion #2: "Real DO droplet provisioned and destroyed
via production adapter."

Run with: uv run pytest tests/e2e/proxy_infra/test_terraform_do_e2e.py -v -s --timeout=300

WARNING: This test creates real cloud resources that cost money.
It includes teardown in a finally block, but operator should verify
cleanup via `doctl compute droplet list --tag-name jerry-proxy`.
"""

from __future__ import annotations

import json
import os
import shutil
import socket
import subprocess
import time
from pathlib import Path

import pytest

# Skip entire module if terraform is not available
_has_terraform = shutil.which("terraform") is not None
_has_age = shutil.which("age") is not None

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.skipif(not _has_terraform, reason="terraform not in PATH"),
    pytest.mark.skipif(not _has_age, reason="age not in PATH"),
]


def _get_do_api_key() -> str:
    """Retrieve DO API key from Keychain or env var."""
    key = os.environ.get("JERRY_PROXY_DO_API_KEY", "")
    if key:
        return key
    try:
        result = subprocess.run(
            [
                "security",
                "find-generic-password",
                "-s",
                "jerry",
                "-a",
                "proxy.digitalocean.api-key",
                "-w",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def _wait_for_ssh(ip: str, timeout: int = 180) -> bool:
    """Poll until SSH port 22 is open."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            sock = socket.create_connection((ip, 22), timeout=5)
            sock.close()
            return True
        except (OSError, TimeoutError):
            time.sleep(3)
    return False


@pytest.fixture(autouse=True)
def _do_token_env(request: pytest.FixtureRequest) -> None:
    """Set DIGITALOCEAN_TOKEN env var from Keychain. Never returns the key.

    The secret is resolved inside the fixture and injected directly into
    os.environ where terraform reads it. The raw value never appears as a
    fixture parameter, test argument, or pytest traceback variable.

    OPSEC: pytest displays fixture return values and test method parameters
    in failure tracebacks. A fixture that returns a secret string will leak
    the secret into any system that captures test output (CI logs, LLM API
    calls, developer terminals). By setting the env var internally and
    returning None, the secret stays in-process only.
    """
    key = _get_do_api_key()
    if not key:
        pytest.skip("DO API key not available (Keychain or JERRY_PROXY_DO_API_KEY)")
    os.environ["DIGITALOCEAN_TOKEN"] = key
    yield
    os.environ.pop("DIGITALOCEAN_TOKEN", None)


class TestTerraformDigitalOceanE2E:
    """Real E2E: provision DO droplet via Terraform, verify, destroy."""

    def test_provision_and_destroy_real_droplet(self, tmp_path: Path) -> None:
        """Go/No-Go #2: Real DO droplet provisioned and destroyed via production adapter."""
        from src.proxy_infra.domain.value_objects.provision_config import ProvisionConfig
        from src.proxy_infra.domain.value_objects.proxy_role import ProxyRole
        from src.proxy_infra.domain.value_objects.proxy_type import ProxyType
        from src.proxy_infra.infrastructure.adapters.terraform_provisioner_adapter import (
            TerraformProvisionerAdapter,
        )

        # DIGITALOCEAN_TOKEN already set by _do_token_env fixture

        adapter = TerraformProvisionerAdapter(engagement_dir=tmp_path)

        config = ProvisionConfig(
            provider="digitalocean",
            region="nyc3",
            engagement_id="E2E-TF-001",
            engagement_tag="jerry-e2e-tf-001",
            count=1,
            role=ProxyRole.ACTIVE,
            proxy_type=ProxyType.DIRECT_SOCKS5,
            ssh_public_key=_generate_ssh_key(tmp_path),
            operator_ip=_get_operator_ip(),
            image="ubuntu-24-04-x64",
            size="s-1vcpu-1gb",
            socks_port=1080,
        )

        nodes = None
        try:
            # --- PROVISION ---
            nodes = adapter.provision(config)

            assert len(nodes) == 1, "Expected exactly 1 node"
            node = nodes[0]

            # Verify node has an IP
            assert node.ip, "Node must have a public IP"
            assert node.id, "Node must have a provider ID"
            assert node.provider == "digitalocean"
            assert node.region == "nyc3"
            assert node.engagement_id == "E2E-TF-001"

            # Verify terraform state was created
            state_file = tmp_path / "terraform" / "terraform.tfstate"
            assert state_file.exists(), "terraform.tfstate must exist after apply"

            # Verify state contains expected resources
            state = json.loads(state_file.read_text())
            resource_types = [r["type"] for r in state.get("resources", [])]
            assert "digitalocean_droplet" in resource_types
            assert "digitalocean_ssh_key" in resource_types
            assert "digitalocean_firewall" in resource_types

            # --- SSH READINESS ---
            ssh_ready = _wait_for_ssh(node.ip, timeout=180)
            assert ssh_ready, f"SSH not ready on {node.ip} within 180s"

        finally:
            # --- DESTROY (always, even on assertion failure) ---
            if nodes:
                result = adapter.destroy(
                    node_ids=[n.id for n in nodes],
                    engagement_id="E2E-TF-001",
                )
                assert result.is_all_successful, f"Destroy failed for nodes: {result.failed}"


def _generate_ssh_key(work_dir: Path) -> str:
    """Generate a temporary SSH keypair for the E2E test."""
    key_path = work_dir / "e2e_key"
    subprocess.run(
        [
            "ssh-keygen",
            "-t",
            "ed25519",
            "-f",
            str(key_path),
            "-N",
            "",
            "-C",
            "e2e-test@jerry",
        ],
        capture_output=True,
        check=True,
    )
    return (key_path.with_suffix(".pub")).read_text().strip()


def _get_operator_ip() -> str:
    """Get operator's public IPv4 for firewall allowlisting."""
    try:
        result = subprocess.run(
            ["curl", "-4", "-s", "https://ifconfig.me"],
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return "0.0.0.0"
