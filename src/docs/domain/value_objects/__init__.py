# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Docs Domain Value Objects.

Exports:
    - AgentData: Extracted agent metadata from YAML frontmatter.
    - SkillData: Extracted skill metadata with agent inventory.

Reference: doc-module-spec.md Section: Data Models
"""

from src.docs.domain.value_objects.agent_data import AgentData
from src.docs.domain.value_objects.skill_data import SkillData

__all__ = ["AgentData", "SkillData"]
