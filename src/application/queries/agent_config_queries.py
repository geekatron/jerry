# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Agent Configuration Queries - Query data objects for agent config operations.

These are pure data objects - no dependencies, no behavior.
Used by the dispatcher to route to handlers.

References:
    - PROJ-012: Agent Configuration Extraction & Schema Enforcement
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ValidateAgentConfigQuery:
    """Query for validating agent configuration against schema.

    Validates a single agent or all agents.

    Attributes:
        agent_name: Specific agent name to validate, or None for all agents.
        skills_dir: Path to the skills directory.
        schema_path: Path to the JSON Schema file.
        defaults_path: Path to the base defaults YAML file.
    """

    skills_dir: str
    schema_path: str
    defaults_path: str
    agent_name: str | None = None


@dataclass(frozen=True)
class ListAgentConfigsQuery:
    """Query for listing all agent configurations.

    Attributes:
        skills_dir: Path to the skills directory.
        skill_filter: Optional skill name to filter by.
    """

    skills_dir: str
    skill_filter: str | None = None


@dataclass(frozen=True)
class ShowAgentConfigQuery:
    """Query for showing a fully composed agent configuration.

    Runs the full composition pipeline: defaults + agent frontmatter + config substitution.

    Attributes:
        agent_name: Name of the agent to show.
        skills_dir: Path to the skills directory.
        defaults_path: Path to the base defaults YAML file.
        raw: If True, show raw frontmatter without composition.
    """

    agent_name: str
    skills_dir: str
    defaults_path: str
    raw: bool = False


@dataclass(frozen=True)
class ComposeAgentConfigQuery:
    """Query for composing agent configs and writing to output directory.

    Composes one or all agents (defaults + frontmatter + config vars) and writes
    the resulting .md files to the output directory.

    Attributes:
        skills_dir: Path to the skills directory.
        defaults_path: Path to the base defaults YAML file.
        output_dir: Directory to write composed files.
        clean: If True, remove existing .md files before writing.
        agent_name: If specified, compose only this agent. Use 'all' for all agents.
    """

    skills_dir: str
    defaults_path: str
    output_dir: str
    clean: bool = False
    agent_name: str | None = None
