# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Integration tests for the compose pipeline.

End-to-end test: real repository, real adapter, real defaults, real filesystem.
Uses temp directories to avoid polluting the workspace.

Compose writes to skill-scoped paths (skills/{skill}/agents/{agent}.md),
the same directories as the build command.
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
from src.agents.domain.value_objects.vendor_override_spec import CLAUDE_CODE_OVERRIDE_SPEC
from src.agents.infrastructure.adapters.claude_code_adapter import ClaudeCodeAdapter
from src.agents.infrastructure.persistence.filesystem_agent_repository import (
    FilesystemAgentRepository,
)
from src.agents.infrastructure.persistence.filesystem_vendor_override_provider import (
    FilesystemVendorOverrideProvider,
)


def _create_canonical_source(
    skills_dir: Path,
    skill: str,
    agent_name: str,
    model_tier: str = "reasoning_standard",
    native_tools: list[str] | None = None,
) -> None:
    """Create canonical .jerry.yaml + .jerry.prompt.md files for a test agent."""
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
    yaml_path = composition_dir / f"{agent_name}.jerry.yaml"
    yaml_content = yaml.dump(yaml_data, default_flow_style=False, sort_keys=False)
    yaml_path.write_text(
        f"# Canonical Agent Definition\n# Schema: docs/schemas/agent-canonical-v1.schema.json\n\n{yaml_content}",
        encoding="utf-8",
    )

    prompt_path = composition_dir / f"{agent_name}.jerry.prompt.md"
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
    """Integration test: canonical source -> compose -> composed output in skill dirs."""

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

        governance_defaults = {
            "version": "1.0.0",
            "persona": {"tone": "professional"},
        }
        vendor_defaults = {
            "permissionMode": "default",
            "background": False,
        }

        handler = ComposeAgentsCommandHandler(
            repository=repository,
            adapters={"claude_code": adapter},
            defaults_composer=DefaultsComposer(),
            governance_defaults=governance_defaults,
            vendor_defaults=vendor_defaults,
        )

        command = ComposeAgentsCommand(
            vendor="claude_code",
            agent_name="test-agent",
        )

        # Act
        result = handler.handle(command)

        # Assert
        assert result.composed == 1
        assert result.failed == 0

        # Composed file should be in the skill's agents directory
        composed_file = skills_dir / "test-skill" / "agents" / "test-agent.md"
        assert composed_file.exists()

        content = composed_file.read_text(encoding="utf-8")
        assert content.startswith("---\n")

        # Parse and verify frontmatter has only vendor fields
        end = content.find("---", 3)
        fm = yaml.safe_load(content[3:end])
        assert fm["name"] == "test-agent"
        assert fm["permissionMode"] == "default"
        assert fm["background"] is False

        # Governance fields must NOT appear in frontmatter
        assert "persona" not in fm
        assert "version" not in fm, "Governance 'version' leaked into frontmatter"

        # Body must be non-empty (prompt content after closing ---)
        body = content[end + 3 :].strip()
        assert len(body) > 0, "Composed output has no prompt body"
        assert "identity" in body, "Prompt body missing identity section"

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

        handler = ComposeAgentsCommandHandler(
            repository=repository,
            adapters={"claude_code": adapter},
            defaults_composer=DefaultsComposer(),
            governance_defaults={"permissionMode": "default"},
        )

        command = ComposeAgentsCommand(vendor="claude_code")

        result = handler.handle(command)

        assert result.composed == 2
        assert result.failed == 0
        # Each agent in its own skill directory
        assert (skills_dir / "skill-a" / "agents" / "agent-one.md").exists()
        assert (skills_dir / "skill-b" / "agents" / "agent-two.md").exists()

    def test_clean_removes_existing_agent_files(self, tmp_path: Path) -> None:
        """Clean flag removes pre-existing files at agent paths before composing."""
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

        # Pre-existing file at the agent's expected output path
        agents_dir = skills_dir / "skill" / "agents"
        agents_dir.mkdir(parents=True)
        (agents_dir / "fresh-agent.md").write_text("old content")

        handler = ComposeAgentsCommandHandler(
            repository=repository,
            adapters={"claude_code": adapter},
            defaults_composer=DefaultsComposer(),
            governance_defaults={},
        )

        command = ComposeAgentsCommand(
            vendor="claude_code",
            clean=True,
        )

        handler.handle(command)

        # File should exist with NEW content (clean removed old, compose wrote new)
        composed_file = agents_dir / "fresh-agent.md"
        assert composed_file.exists()
        content = composed_file.read_text(encoding="utf-8")
        assert content.startswith("---\n")
        assert "old content" not in content

    def test_compose_with_vendor_override_file(self, tmp_path: Path) -> None:
        """End-to-end: vendor override file in composition dir applies layer 4."""
        skills_dir = tmp_path / "skills"
        _create_canonical_source(skills_dir, "test-skill", "test-agent")

        # Create a vendor override file
        comp_dir = skills_dir / "test-skill" / "composition"
        (comp_dir / "test-agent.claude-code.yaml").write_text(
            yaml.dump({"maxTurns": 5, "background": True}),
            encoding="utf-8",
        )

        infra_dir = tmp_path / "infra"
        infra_dir.mkdir()
        _create_mappings_yaml(infra_dir)
        mappings = yaml.safe_load((infra_dir / "mappings.yaml").read_text(encoding="utf-8"))

        tool_mapper = ToolMapper.from_mappings(mappings)
        prompt_transformer = PromptTransformer()
        adapter = ClaudeCodeAdapter(tool_mapper, prompt_transformer, skills_dir)
        repository = FilesystemAgentRepository(skills_dir)
        vendor_override_provider = FilesystemVendorOverrideProvider(skills_dir)

        handler = ComposeAgentsCommandHandler(
            repository=repository,
            adapters={"claude_code": adapter},
            defaults_composer=DefaultsComposer(),
            governance_defaults={"version": "1.0.0"},
            vendor_defaults={"permissionMode": "default", "background": False},
            vendor_override_provider=vendor_override_provider,
            vendor_override_spec=CLAUDE_CODE_OVERRIDE_SPEC,
        )

        command = ComposeAgentsCommand(
            vendor="claude_code",
            agent_name="test-agent",
        )

        result = handler.handle(command)

        assert result.composed == 1
        assert result.failed == 0

        composed_file = skills_dir / "test-skill" / "agents" / "test-agent.md"
        content = composed_file.read_text(encoding="utf-8")
        end = content.find("---", 3)
        fm = yaml.safe_load(content[3:end])

        # Layer 4 overrides
        assert fm["maxTurns"] == 5
        assert fm["background"] is True
        # Layer 2 default
        assert fm["permissionMode"] == "default"

    def test_compose_governance_injection_blocked(self, tmp_path: Path) -> None:
        """Governance field in vendor override file causes compose failure."""
        skills_dir = tmp_path / "skills"
        _create_canonical_source(skills_dir, "test-skill", "evil-agent")

        comp_dir = skills_dir / "test-skill" / "composition"
        (comp_dir / "evil-agent.claude-code.yaml").write_text(
            yaml.dump({"constitution": {"principles_applied": []}}),
            encoding="utf-8",
        )

        infra_dir = tmp_path / "infra"
        infra_dir.mkdir()
        _create_mappings_yaml(infra_dir)
        mappings = yaml.safe_load((infra_dir / "mappings.yaml").read_text(encoding="utf-8"))

        tool_mapper = ToolMapper.from_mappings(mappings)
        prompt_transformer = PromptTransformer()
        adapter = ClaudeCodeAdapter(tool_mapper, prompt_transformer, skills_dir)
        repository = FilesystemAgentRepository(skills_dir)
        vendor_override_provider = FilesystemVendorOverrideProvider(skills_dir)

        handler = ComposeAgentsCommandHandler(
            repository=repository,
            adapters={"claude_code": adapter},
            defaults_composer=DefaultsComposer(),
            governance_defaults={},
            vendor_defaults={},
            vendor_override_provider=vendor_override_provider,
            vendor_override_spec=CLAUDE_CODE_OVERRIDE_SPEC,
        )

        command = ComposeAgentsCommand(
            vendor="claude_code",
            agent_name="evil-agent",
        )

        result = handler.handle(command)

        assert result.failed == 1
        assert any("constitution" in e for e in result.errors)

    def test_composed_output_has_all_required_components(self, tmp_path: Path) -> None:
        """Composed output must contain vendor frontmatter, governance frontmatter, and prompt body."""
        # Arrange
        skills_dir = tmp_path / "skills"
        _create_canonical_source(
            skills_dir,
            "test-skill",
            "complete-agent",
            model_tier="reasoning_high",
            native_tools=["file_read", "file_write", "file_search", "file_glob"],
        )

        infra_dir = tmp_path / "infra"
        infra_dir.mkdir()
        _create_mappings_yaml(infra_dir)
        mappings = yaml.safe_load((infra_dir / "mappings.yaml").read_text(encoding="utf-8"))

        tool_mapper = ToolMapper.from_mappings(mappings)
        prompt_transformer = PromptTransformer()
        adapter = ClaudeCodeAdapter(tool_mapper, prompt_transformer, skills_dir)
        repository = FilesystemAgentRepository(skills_dir)

        governance_defaults = {
            "version": "1.0.0",
            "persona": {"tone": "professional", "communication_style": "consultative"},
        }
        vendor_defaults = {
            "permissionMode": "default",
            "background": False,
        }

        handler = ComposeAgentsCommandHandler(
            repository=repository,
            adapters={"claude_code": adapter},
            defaults_composer=DefaultsComposer(),
            governance_defaults=governance_defaults,
            vendor_defaults=vendor_defaults,
        )

        command = ComposeAgentsCommand(
            vendor="claude_code",
            agent_name="complete-agent",
        )

        # Act
        result = handler.handle(command)

        # Assert — compose succeeded
        assert result.composed == 1
        assert result.failed == 0

        composed_file = skills_dir / "test-skill" / "agents" / "complete-agent.md"
        assert composed_file.exists()
        content = composed_file.read_text(encoding="utf-8")

        # --- Frontmatter structure ---
        assert content.startswith("---\n"), "Missing opening frontmatter delimiter"
        end = content.find("---", 3)
        assert end > 3, "Missing closing frontmatter delimiter"
        fm = yaml.safe_load(content[3:end])

        # Vendor fields present
        assert fm["name"] == "complete-agent"
        assert fm["model"] == "opus"  # reasoning_high maps to opus
        assert isinstance(fm["tools"], str)
        assert "Read" in fm["tools"]
        assert fm["permissionMode"] == "default"
        assert fm["background"] is False

        # Governance fields must NOT appear in frontmatter
        governance_fields = {
            "version",
            "persona",
            "guardrails",
            "constitution",
            "identity",
            "tool_tier",
            "enforcement",
            "capabilities",
        }
        leaked = set(fm.keys()) & governance_fields
        assert leaked == set(), f"Governance fields leaked into frontmatter: {leaked}"

        # Only vendor fields present
        vendor_fields = set(ComposeAgentsCommandHandler._VENDOR_FIELDS)
        assert set(fm.keys()).issubset(vendor_fields), (
            f"Non-vendor fields in frontmatter: {set(fm.keys()) - vendor_fields}"
        )

        # --- Prompt body ---
        body = content[end + 3 :].strip()
        assert len(body) > 0, "Composed output has empty prompt body"
        assert "<agent>" in body, "Prompt body missing <agent> wrapper"
        assert "<identity>" in body, "Prompt body missing <identity> section"
        assert "complete-agent" in body, "Prompt body missing agent name"
