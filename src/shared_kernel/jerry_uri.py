# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
JerryUri - URI-based entity reference format.

Provides cross-system identification using jerry:// scheme.
Format: jerry://{entity_type}/{id}[/{sub_entity}/{sub_id}]

References:
    - Canon PAT-003 (L167-220)

Exports:
    JerryUri (value object)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class JerryUri:
    """
    URI-based entity reference for cross-system identification.

    Invariants:
        - Scheme is always "jerry"
        - Path segments alternate: entity_type/id/sub_type/sub_id
        - Valid entity types: task, phase, plan, knowledge, actor, event

    Examples:
        jerry://task/TASK-a1b2c3d4
        jerry://plan/PLAN-12345678
        jerry://plan/PLAN-12345678/phase/PHASE-e5f6g7h8
        jerry://knowledge/pattern/KNOW-xyz98765
    """

    path_segments: tuple[str, ...]

    VALID_ENTITY_TYPES: ClassVar[frozenset[str]] = frozenset(
        {"task", "phase", "plan", "knowledge", "actor", "event", "subtask"}
    )
    SCHEME: ClassVar[str] = "jerry"

    def __post_init__(self) -> None:
        if len(self.path_segments) < 2:
            raise ValueError("JerryUri requires at least entity_type and id")
        if len(self.path_segments) % 2 != 0:
            raise ValueError("JerryUri path segments must be pairs of type/id")
        # Validate entity types
        for i in range(0, len(self.path_segments), 2):
            entity_type = self.path_segments[i]
            if entity_type not in self.VALID_ENTITY_TYPES:
                raise ValueError(f"Invalid entity type: {entity_type}")

    @classmethod
    def parse(cls, uri: str) -> JerryUri:
        """Parse jerry:// URI string."""
        prefix = f"{cls.SCHEME}://"
        if not uri.startswith(prefix):
            raise ValueError(f"Invalid JerryUri scheme: {uri}")
        path = uri[len(prefix) :]
        if not path:
            raise ValueError("JerryUri path cannot be empty")
        segments = tuple(path.split("/"))
        return cls(segments)

    @classmethod
    def for_entity(cls, entity_type: str, entity_id: str) -> JerryUri:
        """Create JerryUri for a single entity."""
        return cls((entity_type, entity_id))

    @classmethod
    def for_nested(
        cls, parent_type: str, parent_id: str, child_type: str, child_id: str
    ) -> JerryUri:
        """Create JerryUri for a nested entity."""
        return cls((parent_type, parent_id, child_type, child_id))

    def __str__(self) -> str:
        return f"{self.SCHEME}://{'/'.join(self.path_segments)}"

    @property
    def entity_type(self) -> str:
        """Primary entity type (first path segment)."""
        return self.path_segments[0]

    @property
    def entity_id(self) -> str:
        """Primary entity ID (second path segment)."""
        return self.path_segments[1]

    @property
    def is_nested(self) -> bool:
        """True if this URI references a nested entity."""
        return len(self.path_segments) > 2

    @property
    def leaf_type(self) -> str:
        """Innermost entity type (last type segment)."""
        return self.path_segments[-2]

    @property
    def leaf_id(self) -> str:
        """Innermost entity ID (last id segment)."""
        return self.path_segments[-1]
