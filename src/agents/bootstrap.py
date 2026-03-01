# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Agents Bounded Context - Composition Root.

Factory functions for creating fully configured handler instances.
All dependency wiring for the agents bounded context happens here.

This replaces the factory functions that were previously in
claude_code_adapter.py (infrastructure layer violation).

References:
    - PROJ-012: Agent Configuration Extraction & Schema Enforcement
    - ADR-PROJ010-003: LLM Portability Architecture
    - H-07: Composition root exclusivity
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

from src.agents.domain.services.defaults_composer import DefaultsComposer
from src.agents.domain.services.prompt_transformer import PromptTransformer
from src.agents.domain.services.tool_mapper import ToolMapper
from src.agents.domain.value_objects.vendor_override_spec import CLAUDE_CODE_OVERRIDE_SPEC
from src.agents.infrastructure.adapters.claude_code_adapter import ClaudeCodeAdapter
from src.agents.infrastructure.persistence.filesystem_agent_repository import (
    FilesystemAgentRepository,
)
from src.agents.infrastructure.persistence.filesystem_defaults_provider import (
    FilesystemDefaultsProvider,
)
from src.agents.infrastructure.persistence.filesystem_vendor_override_provider import (
    FilesystemVendorOverrideProvider,
)


def _get_project_root() -> Path:
    """Resolve the project root directory.

    Returns:
        Path to the project root.
    """
    project_root = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if project_root:
        return Path(project_root)
    return Path.cwd()


def _get_skills_dir() -> Path:
    """Resolve the skills directory path.

    Returns:
        Path to the skills/ directory.
    """
    return _get_project_root() / "skills"


def _get_schema_path() -> Path:
    """Resolve the canonical schema path.

    Returns:
        Path to agent-canonical-v1.schema.json.
    """
    return _get_project_root() / "docs" / "schemas" / "agent-canonical-v1.schema.json"


def _get_schemas_dir() -> Path:
    """Resolve the schemas directory path.

    Returns:
        Path to docs/schemas/ directory.
    """
    return _get_project_root() / "docs" / "schemas"


def _get_governance_defaults_path() -> Path:
    """Resolve the governance defaults YAML path.

    Returns:
        Path to jerry-agent-defaults.yaml.
    """
    return _get_schemas_dir() / "jerry-agent-defaults.yaml"


def _get_defaults_path() -> Path:
    """Resolve the legacy defaults YAML path.

    Retained for backward compatibility with code that uses the combined file.

    Returns:
        Path to jerry-claude-agent-defaults.yaml.
    """
    return _get_schemas_dir() / "jerry-claude-agent-defaults.yaml"


def _create_tool_mapper() -> ToolMapper:
    """Create a ToolMapper from the mappings.yaml file.

    Returns:
        Configured ToolMapper instance.
    """
    mappings_path = Path(__file__).parent / "infrastructure" / "mappings.yaml"
    mappings_content = mappings_path.read_text(encoding="utf-8")
    mappings = yaml.safe_load(mappings_content)
    return ToolMapper.from_mappings(mappings)


def _create_claude_code_adapter() -> ClaudeCodeAdapter:
    """Create a fully configured ClaudeCodeAdapter.

    Returns:
        ClaudeCodeAdapter with all dependencies.
    """
    tool_mapper = _create_tool_mapper()
    prompt_transformer = PromptTransformer()
    skills_dir = _get_skills_dir()
    return ClaudeCodeAdapter(
        tool_mapper=tool_mapper,
        prompt_transformer=prompt_transformer,
        skills_dir=skills_dir,
    )


def create_agents_build_handler() -> Any:
    """Create a fully configured BuildAgentsCommandHandler.

    Returns:
        BuildAgentsCommandHandler ready for use.
    """
    from src.agents.application.handlers.commands.build_agents_command_handler import (
        BuildAgentsCommandHandler,
    )

    skills_dir = _get_skills_dir()
    repository = FilesystemAgentRepository(skills_dir)
    adapter = _create_claude_code_adapter()

    return BuildAgentsCommandHandler(
        repository=repository,
        adapters={"claude_code": adapter},
    )


def create_agents_extract_handler() -> Any:
    """Create a fully configured ExtractCanonicalCommandHandler.

    Returns:
        ExtractCanonicalCommandHandler ready for use.
    """
    from src.agents.application.handlers.commands.extract_canonical_command_handler import (
        ExtractCanonicalCommandHandler,
    )

    skills_dir = _get_skills_dir()
    adapter = _create_claude_code_adapter()

    return ExtractCanonicalCommandHandler(
        adapters={"claude_code": adapter},
        skills_dir=skills_dir,
    )


def create_agents_validate_handler() -> Any:
    """Create a fully configured ValidateAgentsQueryHandler.

    Returns:
        ValidateAgentsQueryHandler ready for use.
    """
    from src.agents.application.handlers.queries.validate_agents_query_handler import (
        ValidateAgentsQueryHandler,
    )

    skills_dir = _get_skills_dir()
    repository = FilesystemAgentRepository(skills_dir)
    schema_path = _get_schema_path()

    return ValidateAgentsQueryHandler(
        repository=repository,
        schema_path=schema_path,
    )


def create_agents_list_handler() -> Any:
    """Create a fully configured ListAgentsQueryHandler.

    Returns:
        ListAgentsQueryHandler ready for use.
    """
    from src.agents.application.handlers.queries.list_agents_query_handler import (
        ListAgentsQueryHandler,
    )

    skills_dir = _get_skills_dir()
    repository = FilesystemAgentRepository(skills_dir)

    return ListAgentsQueryHandler(repository=repository)


def create_agents_compose_handler() -> Any:
    """Create a fully configured ComposeAgentsCommandHandler.

    Uses the 4-layer merge architecture:
      1. jerry-agent-defaults.yaml (governance)
      2. jerry-claude-code-defaults.yaml (vendor)
      3. Per-agent config from canonical source
      4. Per-agent vendor overrides from composition dirs

    Returns:
        ComposeAgentsCommandHandler ready for use.
    """
    from src.agents.application.handlers.commands.compose_agents_command_handler import (
        ComposeAgentsCommandHandler,
    )

    skills_dir = _get_skills_dir()
    schemas_dir = _get_schemas_dir()
    repository = FilesystemAgentRepository(skills_dir)
    adapter = _create_claude_code_adapter()

    defaults_provider = FilesystemDefaultsProvider(
        governance_defaults_path=_get_governance_defaults_path(),
        vendor_defaults_dir=schemas_dir,
    )
    vendor_override_provider = FilesystemVendorOverrideProvider(skills_dir)
    defaults_composer = DefaultsComposer()

    return ComposeAgentsCommandHandler(
        repository=repository,
        adapters={"claude_code": adapter},
        defaults_composer=defaults_composer,
        governance_defaults=defaults_provider.get_defaults(),
        vendor_defaults=defaults_provider.get_vendor_defaults("claude_code"),
        vendor_override_provider=vendor_override_provider,
        vendor_override_spec=CLAUDE_CODE_OVERRIDE_SPEC,
        config_var_resolver=defaults_provider.get_config_var,
    )
