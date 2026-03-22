# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""Session state data class for container lifecycle management."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SessionState:
    """In-memory representation of the session state file."""

    pid: int
    compose_project_name: str
    clusters: dict[str, str] = field(default_factory=dict)
    engagement_id: str | None = None
    created_at: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a dictionary for YAML persistence."""
        return {
            "pid": self.pid,
            "compose_project_name": self.compose_project_name,
            "clusters": self.clusters,
            "engagement_id": self.engagement_id,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SessionState:
        """Deserialize from a dictionary."""
        return cls(
            pid=data.get("pid", 0),
            compose_project_name=data.get("compose_project_name", ""),
            clusters=data.get("clusters", {}),
            engagement_id=data.get("engagement_id"),
            created_at=data.get("created_at", 0.0),
        )
