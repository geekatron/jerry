# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for ComposeAgentsCommandHandler."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest
import yaml

from src.agents.application.commands.compose_agents_command import ComposeAgentsCommand
from src.agents.application.handlers.commands.compose_agents_command_handler import (
    ComposeAgentsCommandHandler,
)
from src.agents.domain.entities.generated_artifact import GeneratedArtifact
from src.agents.domain.services.defaults_composer import DefaultsComposer
from src.agents.domain.value_objects.vendor_target import VendorTarget

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_DEFAULTS = {
    "permissionMode": "default",
    "background": False,
    "version": "1.0.0",
    "persona": {
        "tone": "professional",
        "communication_style": "consultative",
        "audience_level": "adaptive",
    },
    "guardrails": {
        "output_filtering": [
            "no_secrets_in_output",
            "no_executable_code_without_confirmation",
            "all_claims_must_have_citations",
        ],
        "fallback_behavior": "warn_and_retry",
    },
}


def _make_md_artifact(name: str, agents_dir: Path, model: str = "sonnet") -> GeneratedArtifact:
    """Create a .md GeneratedArtifact with frontmatter + body."""
    fm = {"name": name, "description": f"Test agent {name}", "model": model}
    fm_str = yaml.dump(fm, default_flow_style=False, sort_keys=False)
    content = (
        f"---\n{fm_str}---\n<agent>\n\n<identity>\nTest body for {name}\n</identity>\n\n</agent>\n"
    )
    return GeneratedArtifact(
        path=agents_dir / f"{name}.md",
        content=content,
        vendor=VendorTarget.CLAUDE_CODE,
        source_agent=name,
        artifact_type="agent_definition",
    )


def _make_gov_artifact(name: str, agents_dir: Path) -> GeneratedArtifact:
    """Create a .governance.yaml GeneratedArtifact."""
    gov = {
        "version": "1.0.0",
        "tool_tier": "T2",
        "identity": {"role": "Test Role", "cognitive_mode": "convergent"},
    }
    content = yaml.dump(gov, default_flow_style=False, sort_keys=False)
    return GeneratedArtifact(
        path=agents_dir / f"{name}.governance.yaml",
        content=content,
        vendor=VendorTarget.CLAUDE_CODE,
        source_agent=name,
        artifact_type="governance",
    )


def _make_handler(
    agents: list[Any],
    tmp_path: Path,
    defaults: dict[str, Any] | None = None,
) -> tuple[ComposeAgentsCommandHandler, MagicMock, MagicMock]:
    """Build handler with mocked repository and adapter.

    Artifacts are written to skill-scoped directories:
    tmp_path/skills/{skill}/agents/{name}.md
    """
    mock_repo = MagicMock()
    mock_adapter = MagicMock()

    if agents:
        mock_repo.get.return_value = agents[0]
    else:
        mock_repo.get.return_value = None
    mock_repo.list_all.return_value = agents

    # Adapter returns artifacts with skill-scoped paths
    def generate_side_effect(agent: Any) -> list[GeneratedArtifact]:
        agents_dir = tmp_path / "skills" / agent.skill / "agents"
        return [
            _make_md_artifact(agent.name, agents_dir),
            _make_gov_artifact(agent.name, agents_dir),
        ]

    mock_adapter.generate.side_effect = generate_side_effect

    handler = ComposeAgentsCommandHandler(
        repository=mock_repo,
        adapters={"claude_code": mock_adapter},
        defaults_composer=DefaultsComposer(),
        defaults=defaults or dict(_DEFAULTS),
    )
    return handler, mock_repo, mock_adapter


# ---------------------------------------------------------------------------
# handle() — unknown vendor
# ---------------------------------------------------------------------------


class TestHandleUnknownVendor:
    """Tests for ComposeAgentsCommandHandler.handle() with unknown vendor."""

    def test_raises_value_error_for_unknown_vendor(self, tmp_path: Path) -> None:
        handler, _, _ = _make_handler([], tmp_path)
        command = ComposeAgentsCommand(vendor="openai")
        with pytest.raises(ValueError, match="Unknown vendor: 'openai'"):
            handler.handle(command)


# ---------------------------------------------------------------------------
# handle() — agent not found
# ---------------------------------------------------------------------------


class TestHandleAgentNotFound:
    """Tests for ComposeAgentsCommandHandler.handle() when agent is missing."""

    def test_returns_failed_when_agent_not_found(self, tmp_path: Path) -> None:
        handler, _, _ = _make_handler([], tmp_path)
        command = ComposeAgentsCommand(
            vendor="claude_code",
            agent_name="ghost-agent",
        )
        result = handler.handle(command)
        assert result.failed == 1
        assert result.composed == 0
        assert any("ghost-agent" in e for e in result.errors)


# ---------------------------------------------------------------------------
# handle() — successful compose
# ---------------------------------------------------------------------------


class TestHandleSuccessfulCompose:
    """Tests for ComposeAgentsCommandHandler.handle() with successful compose."""

    def test_composes_single_agent(self, make_canonical_agent: Any, tmp_path: Path) -> None:
        agent = make_canonical_agent(name="ps-analyst", skill="problem-solving")
        handler, _, _ = _make_handler([agent], tmp_path)
        command = ComposeAgentsCommand(
            vendor="claude_code",
            agent_name="ps-analyst",
        )
        result = handler.handle(command)
        assert result.composed == 1
        assert result.failed == 0
        assert len(result.output_paths) == 1

    def test_composed_file_written_to_skill_dir(
        self, make_canonical_agent: Any, tmp_path: Path
    ) -> None:
        agent = make_canonical_agent(name="ps-analyst", skill="problem-solving")
        handler, _, _ = _make_handler([agent], tmp_path)
        command = ComposeAgentsCommand(
            vendor="claude_code",
            agent_name="ps-analyst",
        )
        handler.handle(command)
        composed_file = tmp_path / "skills" / "problem-solving" / "agents" / "ps-analyst.md"
        assert composed_file.exists()
        content = composed_file.read_text(encoding="utf-8")
        assert content.startswith("---\n")
        assert "ps-analyst" in content

    def test_defaults_merged_into_composed(self, make_canonical_agent: Any, tmp_path: Path) -> None:
        agent = make_canonical_agent(name="test-agent", skill="test-skill")
        handler, _, _ = _make_handler([agent], tmp_path)
        command = ComposeAgentsCommand(
            vendor="claude_code",
            agent_name="test-agent",
        )
        handler.handle(command)

        composed_file = tmp_path / "skills" / "test-skill" / "agents" / "test-agent.md"
        content = composed_file.read_text(encoding="utf-8")
        # Parse frontmatter
        end = content.find("---", 3)
        fm = yaml.safe_load(content[3:end])
        # Defaults should be present
        assert fm["permissionMode"] == "default"
        assert fm["background"] is False
        # Agent-specific should override
        assert fm["name"] == "test-agent"

    def test_composes_all_agents(self, make_canonical_agent: Any, tmp_path: Path) -> None:
        agents = [make_canonical_agent(name=f"agent-{i}", skill="skill") for i in range(3)]
        handler, _, _ = _make_handler(agents, tmp_path)
        command = ComposeAgentsCommand(vendor="claude_code")
        result = handler.handle(command)
        assert result.composed == 3
        assert result.failed == 0


# ---------------------------------------------------------------------------
# handle() — dry run
# ---------------------------------------------------------------------------


class TestHandleDryRun:
    """Tests for ComposeAgentsCommandHandler.handle() in dry-run mode."""

    def test_dry_run_does_not_write_files(self, make_canonical_agent: Any, tmp_path: Path) -> None:
        agent = make_canonical_agent(name="dry-agent", skill="skill")
        handler, _, _ = _make_handler([agent], tmp_path)
        command = ComposeAgentsCommand(
            vendor="claude_code",
            agent_name="dry-agent",
            dry_run=True,
        )
        result = handler.handle(command)
        assert result.composed == 1
        assert result.dry_run is True
        assert not (tmp_path / "skills" / "skill" / "agents" / "dry-agent.md").exists()


# ---------------------------------------------------------------------------
# handle() — clean mode
# ---------------------------------------------------------------------------


class TestHandleClean:
    """Tests for ComposeAgentsCommandHandler.handle() with clean flag."""

    def test_clean_removes_existing_agent_files(
        self, make_canonical_agent: Any, tmp_path: Path
    ) -> None:
        agents_dir = tmp_path / "skills" / "skill" / "agents"
        agents_dir.mkdir(parents=True)
        # Pre-existing file at the agent's expected path
        (agents_dir / "new-agent.md").write_text("old content")

        agent = make_canonical_agent(name="new-agent", skill="skill")
        handler, _, _ = _make_handler([agent], tmp_path)
        command = ComposeAgentsCommand(
            vendor="claude_code",
            agent_name="new-agent",
            clean=True,
        )
        handler.handle(command)
        # File should exist with NEW content (clean removed old, compose wrote new)
        composed_file = agents_dir / "new-agent.md"
        assert composed_file.exists()
        content = composed_file.read_text(encoding="utf-8")
        assert content.startswith("---\n")
        assert "old content" not in content


# ---------------------------------------------------------------------------
# handle() — extra_yaml fields
# ---------------------------------------------------------------------------


class TestHandleExtraYaml:
    """Tests for extra_yaml field inclusion in composed output."""

    def test_extra_yaml_included_in_composed(self, tmp_path: Path) -> None:
        """Extra YAML fields like maxTurns should appear in composed frontmatter."""
        from src.agents.domain.entities.canonical_agent import CanonicalAgent
        from src.agents.domain.value_objects.tool_tier import ToolTier

        agent = CanonicalAgent(
            name="extra-agent",
            version="1.0.0",
            description="Agent with extra fields",
            skill="test-skill",
            identity={"role": "Tester", "cognitive_mode": "convergent", "expertise": ["testing"]},
            tool_tier=ToolTier.T2,
            native_tools=["file_read", "file_write"],
            prompt_body="<identity>\nTest\n</identity>",
            constitution={
                "principles_applied": ["P-003", "P-020", "P-022"],
                "forbidden_actions": ["FA1", "FA2", "FA3"],
            },
            guardrails={
                "input_validation": [{"field": "test"}],
                "output_filtering": ["a", "b", "c"],
                "fallback_behavior": "warn_and_retry",
            },
            extra_yaml={"maxTurns": 5, "isolation": True},
        )

        handler, _, _ = _make_handler([agent], tmp_path)
        command = ComposeAgentsCommand(
            vendor="claude_code",
            agent_name="extra-agent",
        )
        handler.handle(command)

        composed_file = tmp_path / "skills" / "test-skill" / "agents" / "extra-agent.md"
        content = composed_file.read_text(encoding="utf-8")
        end = content.find("---", 3)
        fm = yaml.safe_load(content[3:end])
        assert fm.get("maxTurns") == 5
        assert fm.get("isolation") is True
