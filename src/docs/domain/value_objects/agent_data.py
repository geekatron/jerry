# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""AgentData Value Object.

Extracted agent metadata from a skills/*/agents/*.md YAML frontmatter block.

Location: src/docs/domain/value_objects/agent_data.py
Reference: doc-module-spec.md Section: Data Models
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class AgentData:
    """Immutable value object carrying extracted agent metadata.

    Attributes:
        name: Agent identifier (e.g., ``eng-backend``).  Must match
            ``^[a-z][a-z0-9-]*$`` per spec validation rules.
        description: Human-readable purpose description (max 1024 chars,
            HTML stripped).
        model: Declared model tier (``sonnet``, ``opus``, or ``haiku``).
            Empty string when the field is absent from frontmatter.
        file_path: Absolute or repo-relative path to the agent ``.md`` file.
            Used for diagnostic messages and golden-file traceability.
    """

    name: str
    description: str
    model: str
    file_path: str
