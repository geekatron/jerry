# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Integration tests for the compose pipeline.

End-to-end test: real repository, real adapter, real defaults, real filesystem.
Uses temp directories to avoid polluting the workspace.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from src.agents.application.commands.compose_agents_command import ComposeAgentsCommand
from src.agents.application.handlers.commands.compose_agents_command_handler import (
    ComposeAgentsCommandHandler,
)
from src.agents.domain.services.defaults_composer import DefaultsComposer
from src.agents.domain.services.prompt_transformer import PromptTransformer
from src.agents.domain.services.tool_mapper import ToolMapper
from src.agents.infrastructure.adapters.claude_code_adapter import ClaudeCodeAdapter
from src.agents.infrastructure.persistence.filesystem_agent_repository import (
    FilesystemAgentRepository,
)


def _create_canonical_source(
    skills_dir: Path,
    skill: str,
    agent_name: str,
    model_tier: str = "reasoning_standard",
    native_tools: list[str] | None = None,
) -> None:
    """Create canonical .agent.yaml + .prompt.md files for a test agent."""
    composition_dir = skills_dir / skill / "composition"
    composition_dir.mkdir(parents=True, exist_ok=True)

    yaml_data: dict[str, Any] = {
        "name": agent_name,
        "version": "1.0.0",
        "description": f"Test agent {agent_name}",
        "skill": skill,
        "identity": {
            "role": "Test Role",
            "expertise": ["testing", "validation"],
            "cognitive_mode": "convergent",
        },
        "model": {"tier": model_tier},
        "tools": {
            "native": native_tools or ["file_read", "file_write"],
        },
        "tool_tier": "T2",
        "guardrails": {
            "input_validation": [{"field_format": "^.+$"}],
            "output_filtering": [
                "no_secrets_in_output",
                "no_executable_code_without_confirmation",
                "all_claims_must_have_citations",
            ],
            "fallback_behavior": "warn_and_retry",
        },
        "constitution": {
            "principles_applied": [
                "P-003: No Recursive Subagents (Hard)",
                "P-020: User Authority (Hard)",
                "P-022: No Deception (Hard)",
            ],
            "forbidden_actions": [
                "Spawn recursive subagents (P-003)",
                "Override user decisions (P-020)",
                "Misrepresent capabilities or confidence (P-022)",
            ],
        },
    }
    yaml_path = composition_dir / f"{agent_name}.agent.yaml"
    yaml_content = yaml.dump(yaml_data, default_flow_style=False, sort_keys=False)
    yaml_path.write_text(
        f"# Canonical Agent Definition\n# Schema: docs/schemas/agent-canonical-v1.schema.json\n\n{yaml_content}",
        encoding="utf-8",
    )

    prompt_path = composition_dir / f"{agent_name}.prompt.md"
    prompt_path.write_text(
        f"# {agent_name} System Prompt\n\n## Identity\n\nYou are {agent_name}.\n\n## Purpose\n\nTesting.\n",
        encoding="utf-8",
    )


def _create_mappings_yaml(infra_dir: Path) -> None:
    """Create a minimal mappings.yaml for the adapter."""
    mappings = {
        "tool_map": {
            "file_read": {"claude_code": "Read"},
            "file_write": {"claude_code": "Write"},
            "file_search": {"claude_code": "Grep"},
            "file_glob": {"claude_code": "Glob"},
        },
        "model_map": {
            "reasoning_high": {"claude_code": "opus"},
            "reasoning_standard": {"claude_code": "sonnet"},
            "fast": {"claude_code": "haiku"},
        },
    }
    mappings_path = infra_dir / "mappings.yaml"
    mappings_path.write_text(
        yaml.dump(mappings, default_flow_style=False),
        encoding="utf-8",
    )


class TestComposePipeline:
    """Integration test: canonical source -> compose -> composed output."""

    def test_compose_single_agent_end_to_end(self, tmp_path: Path) -> None:
        """Compose a single agent from canonical source with defaults."""
        # Arrange
        skills_dir = tmp_path / "skills"
        _create_canonical_source(skills_dir, "test-skill", "test-agent")

        infra_dir = tmp_path / "infra"
        infra_dir.mkdir()
        _create_mappings_yaml(infra_dir)
        mappings = yaml.safe_load((infra_dir / "mappings.yaml").read_text(encoding="utf-8"))

        tool_mapper = ToolMapper.from_mappings(mappings)
        prompt_transformer = PromptTransformer()
        adapter = ClaudeCodeAdapter(tool_mapper, prompt_transformer, skills_dir)
        repository = FilesystemAgentRepository(skills_dir)

        defaults = {
            "permissionMode": "default",
            "background": False,
            "version": "1.0.0",
            "persona": {"tone": "professional"},
        }

        output_dir = tmp_path / "output"
        handler = ComposeAgentsCommandHandler(
            repository=repository,
            adapters={"claude_code": adapter},
            defaults_composer=DefaultsComposer(),
            defaults=defaults,
        )

        command = ComposeAgentsCommand(
            vendor="claude_code",
            output_dir=output_dir,
            agent_name="test-agent",
        )

        # Act
        result = handler.handle(command)

        # Assert
        assert result.composed == 1
        assert result.failed == 0

        composed_file = output_dir / "test-agent.md"
        assert composed_file.exists()

        content = composed_file.read_text(encoding="utf-8")
        assert content.startswith("---\n")

        # Parse and verify frontmatter has defaults merged in
        end = content.find("---", 3)
        fm = yaml.safe_load(content[3:end])
        assert fm["name"] == "test-agent"
        assert fm["permissionMode"] == "default"
        assert fm["background"] is False
        assert fm["persona"]["tone"] == "professional"

    def test_compose_multiple_agents(self, tmp_path: Path) -> None:
        """Compose all agents across multiple skills."""
        skills_dir = tmp_path / "skills"
        _create_canonical_source(skills_dir, "skill-a", "agent-one")
        _create_canonical_source(skills_dir, "skill-b", "agent-two")

        infra_dir = tmp_path / "infra"
        infra_dir.mkdir()
        _create_mappings_yaml(infra_dir)
        mappings = yaml.safe_load((infra_dir / "mappings.yaml").read_text(encoding="utf-8"))

        tool_mapper = ToolMapper.from_mappings(mappings)
        prompt_transformer = PromptTransformer()
        adapter = ClaudeCodeAdapter(tool_mapper, prompt_transformer, skills_dir)
        repository = FilesystemAgentRepository(skills_dir)

        output_dir = tmp_path / "output"
        handler = ComposeAgentsCommandHandler(
            repository=repository,
            adapters={"claude_code": adapter},
            defaults_composer=DefaultsComposer(),
            defaults={"permissionMode": "default"},
        )

        command = ComposeAgentsCommand(
            vendor="claude_code",
            output_dir=output_dir,
        )

        result = handler.handle(command)

        assert result.composed == 2
        assert result.failed == 0
        assert (output_dir / "agent-one.md").exists()
        assert (output_dir / "agent-two.md").exists()

    def test_clean_removes_stale_files(self, tmp_path: Path) -> None:
        """Clean flag removes pre-existing files before composing."""
        skills_dir = tmp_path / "skills"
        _create_canonical_source(skills_dir, "skill", "fresh-agent")

        infra_dir = tmp_path / "infra"
        infra_dir.mkdir()
        _create_mappings_yaml(infra_dir)
        mappings = yaml.safe_load((infra_dir / "mappings.yaml").read_text(encoding="utf-8"))

        tool_mapper = ToolMapper.from_mappings(mappings)
        prompt_transformer = PromptTransformer()
        adapter = ClaudeCodeAdapter(tool_mapper, prompt_transformer, skills_dir)
        repository = FilesystemAgentRepository(skills_dir)

        output_dir = tmp_path / "output"
        output_dir.mkdir()
        (output_dir / "stale.md").write_text("old content")

        handler = ComposeAgentsCommandHandler(
            repository=repository,
            adapters={"claude_code": adapter},
            defaults_composer=DefaultsComposer(),
            defaults={},
        )

        command = ComposeAgentsCommand(
            vendor="claude_code",
            output_dir=output_dir,
            clean=True,
        )

        handler.handle(command)

        assert not (output_dir / "stale.md").exists()
        assert (output_dir / "fresh-agent.md").exists()
