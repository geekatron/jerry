# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""SkillData Value Object.

Extracted skill metadata assembled from a SKILL.md frontmatter block and its
associated agent directory.

Location: src/docs/domain/value_objects/skill_data.py
Reference: doc-module-spec.md Section: Data Models
"""

from __future__ import annotations

from dataclasses import dataclass, field

from src.docs.domain.value_objects.agent_data import AgentData


@dataclass(frozen=True)
class SkillData:
    """Immutable value object carrying extracted skill metadata plus agent roster.

    Attributes:
        name: Skill identifier (e.g., ``eng-team``).  Must match
            ``^[a-zA-Z][a-zA-Z0-9-]*$`` per spec validation rules.
        description: Human-readable purpose description (max 1024 chars,
            HTML stripped).
        version: Semantic version string (e.g., ``1.0.0``).  Must match
            ``^\\d+\\.\\d+\\.\\d+$``.
        agent_count: Number of invokable agents (TEMPLATE/EXTENSION files
            excluded).  Equals ``len(agents)``.
        agents: Ordered list of :class:`AgentData` instances for this skill.
            Files matching ``*TEMPLATE*`` and ``*EXTENSION*`` are excluded.
        file_path: Absolute or repo-relative path to the ``SKILL.md`` file.
            Used for diagnostic messages and golden-file traceability.
    """

    name: str
    description: str
    version: str
    agent_count: int
    agents: list[AgentData] = field(default_factory=list)
    file_path: str = ""
