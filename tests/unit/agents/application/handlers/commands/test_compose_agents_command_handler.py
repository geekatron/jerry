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
from src.agents.domain.value_objects.vendor_override_spec import (
    CLAUDE_CODE_OVERRIDE_SPEC,
    VendorOverrideSpec,
)
from src.agents.domain.value_objects.vendor_target import VendorTarget

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_GOVERNANCE_DEFAULTS = {
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

_VENDOR_DEFAULTS = {
    "permissionMode": "default",
    "background": False,
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
    governance_defaults: dict[str, Any] | None = None,
    vendor_defaults: dict[str, Any] | None = None,
    vendor_override_provider: Any | None = None,
    vendor_override_spec: VendorOverrideSpec | None = None,
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
        governance_defaults=governance_defaults or dict(_GOVERNANCE_DEFAULTS),
        vendor_defaults=vendor_defaults if vendor_defaults is not None else dict(_VENDOR_DEFAULTS),
        vendor_override_provider=vendor_override_provider,
        vendor_override_spec=vendor_override_spec,
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
        # Vendor defaults should be present
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


# ---------------------------------------------------------------------------
# handle() — 4-layer merge with vendor overrides
# ---------------------------------------------------------------------------


class TestHandleVendorOverrides:
    """Tests for 4-layer merge with per-agent vendor overrides."""

    def test_vendor_override_applied(self, make_canonical_agent: Any, tmp_path: Path) -> None:
        """Per-agent vendor override (layer 4) overrides vendor defaults (layer 2)."""
        mock_override_provider = MagicMock()
        mock_override_provider.get_overrides.return_value = {"maxTurns": 5, "background": True}

        agent = make_canonical_agent(name="override-agent", skill="test-skill")
        handler, _, _ = _make_handler(
            [agent],
            tmp_path,
            vendor_override_provider=mock_override_provider,
            vendor_override_spec=CLAUDE_CODE_OVERRIDE_SPEC,
        )
        command = ComposeAgentsCommand(
            vendor="claude_code",
            agent_name="override-agent",
        )
        handler.handle(command)

        composed_file = tmp_path / "skills" / "test-skill" / "agents" / "override-agent.md"
        content = composed_file.read_text(encoding="utf-8")
        end = content.find("---", 3)
        fm = yaml.safe_load(content[3:end])
        assert fm["maxTurns"] == 5
        assert fm["background"] is True

    def test_no_override_provider_works(self, make_canonical_agent: Any, tmp_path: Path) -> None:
        """Handler works without vendor override provider (backward compat)."""
        agent = make_canonical_agent(name="no-override", skill="skill")
        handler, _, _ = _make_handler([agent], tmp_path)
        command = ComposeAgentsCommand(
            vendor="claude_code",
            agent_name="no-override",
        )
        result = handler.handle(command)
        assert result.composed == 1

    def test_empty_overrides_no_effect(self, make_canonical_agent: Any, tmp_path: Path) -> None:
        """Empty override dict doesn't change the composed output."""
        mock_override_provider = MagicMock()
        mock_override_provider.get_overrides.return_value = {}

        agent = make_canonical_agent(name="empty-override", skill="skill")
        handler, _, _ = _make_handler(
            [agent],
            tmp_path,
            vendor_override_provider=mock_override_provider,
        )
        command = ComposeAgentsCommand(
            vendor="claude_code",
            agent_name="empty-override",
        )
        result = handler.handle(command)
        assert result.composed == 1

    def test_governance_injection_raises_error(
        self, make_canonical_agent: Any, tmp_path: Path
    ) -> None:
        """Governance field in vendor override produces a failed compose."""
        mock_override_provider = MagicMock()
        mock_override_provider.get_overrides.return_value = {"constitution": {"evil": True}}

        agent = make_canonical_agent(name="evil-agent", skill="skill")
        handler, _, _ = _make_handler(
            [agent],
            tmp_path,
            vendor_override_provider=mock_override_provider,
            vendor_override_spec=CLAUDE_CODE_OVERRIDE_SPEC,
        )
        command = ComposeAgentsCommand(
            vendor="claude_code",
            agent_name="evil-agent",
        )
        result = handler.handle(command)
        assert result.failed == 1
        assert any("constitution" in e for e in result.errors)

    def test_override_provider_called_with_correct_args(
        self, make_canonical_agent: Any, tmp_path: Path
    ) -> None:
        mock_override_provider = MagicMock()
        mock_override_provider.get_overrides.return_value = {}

        agent = make_canonical_agent(name="ps-arch", skill="problem-solving")
        handler, _, _ = _make_handler(
            [agent],
            tmp_path,
            vendor_override_provider=mock_override_provider,
        )
        command = ComposeAgentsCommand(
            vendor="claude_code",
            agent_name="ps-arch",
        )
        handler.handle(command)

        mock_override_provider.get_overrides.assert_called_once_with(
            agent_name="ps-arch",
            skill="problem-solving",
            vendor="claude_code",
        )


# ---------------------------------------------------------------------------
# handle() — governance/vendor split defaults
# ---------------------------------------------------------------------------


class TestHandleSplitDefaults:
    """Tests for split governance + vendor defaults."""

    def test_governance_defaults_stripped_from_frontmatter(
        self, make_canonical_agent: Any, tmp_path: Path
    ) -> None:
        """Governance defaults are stripped — only vendor fields survive in frontmatter."""
        agent = make_canonical_agent(name="gov-test", skill="skill")
        handler, _, _ = _make_handler(
            [agent],
            tmp_path,
            governance_defaults={"persona": {"tone": "analytical"}, "custom_gov_field": "present"},
            vendor_defaults={},
        )
        command = ComposeAgentsCommand(vendor="claude_code", agent_name="gov-test")
        handler.handle(command)

        composed_file = tmp_path / "skills" / "skill" / "agents" / "gov-test.md"
        content = composed_file.read_text(encoding="utf-8")
        end = content.find("---", 3)
        fm = yaml.safe_load(content[3:end])
        # Governance fields must NOT appear in frontmatter
        assert "custom_gov_field" not in fm
        assert "persona" not in fm

    def test_vendor_defaults_applied(self, make_canonical_agent: Any, tmp_path: Path) -> None:
        agent = make_canonical_agent(name="vendor-test", skill="skill")
        handler, _, _ = _make_handler(
            [agent],
            tmp_path,
            governance_defaults={},
            vendor_defaults={"permissionMode": "dontAsk"},
        )
        command = ComposeAgentsCommand(vendor="claude_code", agent_name="vendor-test")
        handler.handle(command)

        composed_file = tmp_path / "skills" / "skill" / "agents" / "vendor-test.md"
        content = composed_file.read_text(encoding="utf-8")
        end = content.find("---", 3)
        fm = yaml.safe_load(content[3:end])
        assert fm["permissionMode"] == "dontAsk"

    def test_layer_precedence_governance_vendor_agent(
        self, make_canonical_agent: Any, tmp_path: Path
    ) -> None:
        """Layer 3 (agent) overrides Layer 2 (vendor) which overrides Layer 1 (governance)."""
        mock_override_provider = MagicMock()
        mock_override_provider.get_overrides.return_value = {"background": True}

        agent = make_canonical_agent(name="precedence-test", skill="skill")
        handler, _, _ = _make_handler(
            [agent],
            tmp_path,
            governance_defaults={"background": "gov-value", "persona": {"tone": "gov-tone"}},
            vendor_defaults={"background": False, "permissionMode": "default"},
            vendor_override_provider=mock_override_provider,
            vendor_override_spec=CLAUDE_CODE_OVERRIDE_SPEC,
        )
        command = ComposeAgentsCommand(vendor="claude_code", agent_name="precedence-test")
        handler.handle(command)

        composed_file = tmp_path / "skills" / "skill" / "agents" / "precedence-test.md"
        content = composed_file.read_text(encoding="utf-8")
        end = content.find("---", 3)
        fm = yaml.safe_load(content[3:end])
        # Layer 4 override wins for background
        assert fm["background"] is True
        assert fm["permissionMode"] == "default"


# ---------------------------------------------------------------------------
# _filter_vendor_frontmatter() — unit tests
# ---------------------------------------------------------------------------


class TestFilterVendorFrontmatter:
    """Tests for _filter_vendor_frontmatter static method."""

    def test_filter_vendor_frontmatter_keeps_only_official_fields(self) -> None:
        """Only Claude Code's 13 official fields survive filtering."""
        composed = {
            "name": "test",
            "description": "desc",
            "model": "sonnet",
            "tools": "Read, Write",
            "permissionMode": "default",
            "background": False,
            # Governance fields that should be stripped
            "version": "1.0.0",
            "persona": {"tone": "professional"},
            "guardrails": {"fallback_behavior": "warn_and_retry"},
            "constitution": {"principles_applied": ["P-003"]},
            "identity": {"role": "Test"},
            "tool_tier": "T2",
            "enforcement": {"tier": "C2"},
        }
        result = ComposeAgentsCommandHandler._filter_vendor_frontmatter(composed)
        assert "version" not in result
        assert "persona" not in result
        assert "guardrails" not in result
        assert "constitution" not in result
        assert "identity" not in result
        assert "tool_tier" not in result
        assert "enforcement" not in result
        # Vendor fields preserved
        assert result["name"] == "test"
        assert result["description"] == "desc"
        assert result["model"] == "sonnet"
        assert result["permissionMode"] == "default"

    def test_filter_vendor_frontmatter_preserves_field_order(self) -> None:
        """Filtered output follows _VENDOR_FIELDS order."""
        composed = {
            "background": True,
            "name": "test",
            "model": "opus",
            "description": "desc",
            "version": "1.0.0",
        }
        result = ComposeAgentsCommandHandler._filter_vendor_frontmatter(composed)
        keys = list(result.keys())
        assert keys == ["name", "description", "model", "background"]

    def test_filter_vendor_frontmatter_handles_empty_dict(self) -> None:
        """Empty input produces empty output."""
        result = ComposeAgentsCommandHandler._filter_vendor_frontmatter({})
        assert result == {}
