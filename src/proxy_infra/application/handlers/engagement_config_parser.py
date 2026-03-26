# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""EngagementConfigParser — parses YAML engagement config files.

Reads a YAML file, validates all required fields, and returns an
``EngagementConfig`` value object.  Produces actionable error messages
naming the specific missing or invalid field.

Design constraints:
    H-07: Application layer — imports domain only, no infrastructure.
    H-10: One public class per file.
    H-11: All public methods have type annotations.

References:
    - TASK-023-050: Engagement config YAML schema, parser, and validator
    - FEAT-023-004: Hands-Free Engagement Pipeline Automation
"""

from __future__ import annotations

import logging
from pathlib import Path

import yaml

from src.proxy_infra.domain.value_objects.engagement_config import EngagementConfig

logger = logging.getLogger(__name__)

#: Required fields in the engagement YAML config.
_REQUIRED_FIELDS: tuple[str, ...] = (
    "engagement_id",
    "provider",
    "region",
    "count",
    "proxy_type",
    "socks_port",
    "operator_ip",
)


class EngagementConfigParser:
    """Parses YAML engagement config files into EngagementConfig value objects.

    Validates that all required fields are present and delegates domain
    invariant enforcement to ``EngagementConfig.__post_init__``.
    """

    def parse(self, config_path: Path) -> EngagementConfig:
        """Parse a YAML engagement config file.

        Args:
            config_path: Path to the YAML engagement config file.

        Returns:
            Validated EngagementConfig value object.

        Raises:
            FileNotFoundError: If config_path does not exist.
            ValueError: If required fields are missing or values are invalid.
            yaml.YAMLError: If the file is not valid YAML.
        """
        if not config_path.exists():
            raise FileNotFoundError(
                f"Engagement config file not found: {config_path}"
            )

        raw_text = config_path.read_text(encoding="utf-8")
        data = yaml.safe_load(raw_text)

        if not isinstance(data, dict):
            raise ValueError(
                f"Engagement config must be a YAML mapping, got {type(data).__name__}"
            )

        # Check for missing required fields with actionable messages
        for field in _REQUIRED_FIELDS:
            if field not in data:
                raise ValueError(
                    f"Missing required field '{field}' in engagement config. "
                    f"Required fields: {', '.join(_REQUIRED_FIELDS)}"
                )

        logger.debug("Parsed engagement config: engagement_id=%r", data.get("engagement_id"))

        # EngagementConfig.__post_init__ enforces domain invariants
        return EngagementConfig(
            engagement_id=str(data["engagement_id"]),
            provider=str(data["provider"]),
            region=str(data["region"]),
            count=int(data["count"]),
            proxy_type=str(data["proxy_type"]),
            socks_port=int(data["socks_port"]),
            operator_ip=str(data["operator_ip"]),
            image=str(data.get("image", "ubuntu-24-04-x64")),
            size=str(data.get("size", "s-1vcpu-1gb")),
        )
