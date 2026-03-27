# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""EngagementArtifactManager — manages engagement directory structure and artifacts.

Creates the canonical engagement directory structure and provides methods
for persisting handoff artifacts between skills.

Design constraints:
    H-07: Application layer — no infrastructure imports.
    H-10: One public class per file.
    H-11: All public methods have type annotations.

References:
    - TASK-023-103: Engagement artifact directory structure + persistence
    - ADR-PROJ023-010: Cross-skill handoff contracts
"""

from __future__ import annotations

import logging
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)

#: Canonical subdirectory structure for engagement artifacts.
_ENGAGEMENT_SUBDIRS: tuple[str, ...] = (
    "red-team/findings",
    "red-team/logs",
    "blue-team/detections",
    "blue-team/logs",
    "analysis",
    "config",
    "credentials",
    "reports",
    "archive",
)


class EngagementArtifactManager:
    """Manages engagement directory structure and cross-skill artifact persistence.

    Creates the canonical directory layout consumed by ``/cyber-ops`` agents
    and provides methods for writing handoff artifacts to the correct subdirectory.

    Args:
        base_dir: Base directory under which engagement directories are created.
    """

    def __init__(self, base_dir: Path) -> None:
        """Initialise with a base directory.

        Args:
            base_dir: Parent directory for all engagement directories.
        """
        self._base_dir = base_dir

    def create_engagement_directory(self, engagement_id: str) -> Path:
        """Create the canonical engagement directory structure.

        Args:
            engagement_id: Engagement identifier (e.g., "ENG-0001").

        Returns:
            Path to the engagement root directory.
        """
        eng_dir = self._base_dir / engagement_id
        for subdir in _ENGAGEMENT_SUBDIRS:
            (eng_dir / subdir).mkdir(parents=True, exist_ok=True)

        logger.debug("Created engagement directory: %s", eng_dir)
        return eng_dir

    def persist_config(self, engagement_id: str, config_path: Path) -> Path:
        """Copy the engagement config YAML to the engagement config directory.

        Args:
            engagement_id: Engagement identifier.
            config_path: Source path to the engagement config YAML.

        Returns:
            Path to the persisted config file.
        """
        eng_dir = self._base_dir / engagement_id
        dest = eng_dir / "config" / "engagement.yaml"
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(config_path, dest)
        logger.debug("Persisted engagement config: %s → %s", config_path, dest)
        return dest

    def write_artifact(
        self,
        engagement_id: str,
        team: str,
        category: str,
        filename: str,
        content: str,
    ) -> Path:
        """Write a handoff artifact to the engagement directory.

        Args:
            engagement_id: Engagement identifier.
            team: Team subdirectory (e.g., "red-team", "blue-team").
            category: Category subdirectory (e.g., "findings", "detections").
            filename: Artifact filename.
            content: Artifact content.

        Returns:
            Path to the written artifact.
        """
        artifact_path = self._base_dir / engagement_id / team / category / filename
        artifact_path.parent.mkdir(parents=True, exist_ok=True)
        artifact_path.write_text(content, encoding="utf-8")
        logger.debug("Wrote artifact: %s", artifact_path)
        return artifact_path
