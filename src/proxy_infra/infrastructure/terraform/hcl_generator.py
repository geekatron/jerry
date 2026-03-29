# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""HCL generator for Terraform-based proxy provisioning.

Generates a main.tf file from engagement config parameters using a Jinja2
SandboxedEnvironment template. Input values are validated against allowlist
regexes before rendering to prevent template injection (C-04).

References:
    - TASK-023-101: HCL generator with DO Jinja2 template
    - ADR-EN023-003: Infrastructure provisioning (Option C: Hybrid)
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

# --- Input validation regexes (C-04: Jinja2 injection prevention) ---

_ENGAGEMENT_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")
_REGION_PATTERN = re.compile(r"^[a-z0-9-]+$")
_SIZE_PATTERN = re.compile(r"^[a-z0-9-]+$")
_IMAGE_PATTERN = re.compile(r"^[a-z0-9.-]+$")
_IPV4_PATTERN = re.compile(
    r"^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$"
)
_IPV6_PATTERN = re.compile(r"^[0-9a-fA-F:]+$")
_SSH_PUBKEY_PATTERN = re.compile(r"^ssh-(?:rsa|ed25519|ecdsa)[- ]\S+")
_PORT_RANGE = range(1, 65536)


class HclGenerator:
    """Generates HCL main.tf files from engagement config using Jinja2 templates.

    Uses Jinja2 SandboxedEnvironment to prevent template injection. All
    config values are validated against allowlist regexes before rendering.

    Attributes:
        template_dir: Path to the directory containing provider-specific
            Jinja2 templates (e.g., templates/digitalocean/main.tf.j2).
    """

    def __init__(self, template_dir: Path) -> None:
        """Initialise the HCL generator with a template directory.

        Args:
            template_dir: Path to the templates directory containing
                provider-specific subdirectories with .tf.j2 files.
        """
        self._template_dir = template_dir

    def generate(self, config: dict[str, Any], work_dir: Path) -> Path:
        """Generate a main.tf file from engagement config parameters.

        Validates all config values against allowlist regexes, then renders
        the Jinja2 template to produce HCL.

        Args:
            config: Engagement config dict with keys: engagement_id, region,
                size, image, ssh_public_key, operator_ip, socks_port.
            work_dir: Directory to write main.tf into.

        Returns:
            Path to the generated main.tf file.

        Raises:
            ValueError: If any required config field is missing or invalid.
        """
        self._validate_config(config)

        from jinja2.sandbox import SandboxedEnvironment

        env = SandboxedEnvironment(
            loader=self._make_loader(),
            autoescape=False,
            keep_trailing_newline=True,
        )
        template = env.get_template("digitalocean/main.tf.j2")

        rendered = template.render(
            engagement_id=config["engagement_id"],
            region=config["region"],
            size=config["size"],
            image=config["image"],
            ssh_public_key=config["ssh_public_key"],
            operator_ip=config["operator_ip"],
            socks_port=config["socks_port"],
        )

        main_tf = work_dir / "main.tf"
        main_tf.write_text(rendered)
        return main_tf

    def _make_loader(self) -> Any:
        """Create a Jinja2 FileSystemLoader for the template directory.

        Returns:
            Jinja2 FileSystemLoader instance.
        """
        from jinja2 import FileSystemLoader

        return FileSystemLoader(str(self._template_dir))

    @staticmethod
    def _validate_config(config: dict[str, Any]) -> None:
        """Validate engagement config values against allowlist regexes.

        Prevents Jinja2 template injection by ensuring all values conform
        to expected patterns before rendering (C-04).

        Args:
            config: Engagement config dict to validate.

        Raises:
            ValueError: If any field is missing, empty, or fails validation.
        """
        # Required string fields
        for field in ("engagement_id", "region", "size", "image", "ssh_public_key", "operator_ip"):
            value = config.get(field, "")
            if not value or (isinstance(value, str) and not value.strip()):
                raise ValueError(f"{field} must not be empty — required for HCL generation")

        # Pattern validation
        engagement_id = str(config["engagement_id"])
        if not _ENGAGEMENT_ID_PATTERN.match(engagement_id):
            raise ValueError(
                f"engagement_id '{engagement_id}' contains invalid characters — "
                f"only alphanumeric, hyphens, and underscores allowed"
            )

        region = str(config["region"])
        if not _REGION_PATTERN.match(region):
            raise ValueError(
                f"region '{region}' contains invalid characters — "
                f"only lowercase alphanumeric and hyphens allowed"
            )

        size = str(config["size"])
        if not _SIZE_PATTERN.match(size):
            raise ValueError(
                f"size '{size}' contains invalid characters — "
                f"only lowercase alphanumeric and hyphens allowed"
            )

        image = str(config["image"])
        if not _IMAGE_PATTERN.match(image):
            raise ValueError(
                f"image '{image}' contains invalid characters — "
                f"only lowercase alphanumeric, hyphens, and dots allowed"
            )

        operator_ip = str(config["operator_ip"])
        if not (_IPV4_PATTERN.match(operator_ip) or _IPV6_PATTERN.match(operator_ip)):
            raise ValueError(f"operator_ip '{operator_ip}' is not a valid IPv4 or IPv6 address")

        ssh_public_key = str(config["ssh_public_key"])
        if not _SSH_PUBKEY_PATTERN.match(ssh_public_key):
            raise ValueError("ssh_public_key does not match expected OpenSSH public key format")

        socks_port = config.get("socks_port", 0)
        if not isinstance(socks_port, int) or socks_port not in _PORT_RANGE:
            raise ValueError(f"socks_port={socks_port} must be an integer between 1 and 65535")
