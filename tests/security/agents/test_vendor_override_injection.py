# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Security tests for vendor override injection prevention.

Ensures that per-agent vendor override files cannot inject governance
fields (constitution, guardrails, enforcement) that would bypass
Jerry's security model. Also ensures composed frontmatter contains
ONLY Claude Code official fields — no governance leakage.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

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
from src.agents.infrastructure.persistence.filesystem_vendor_override_provider import (
    FilesystemVendorOverrideProvider,
)


class TestGovernanceFieldInjection:
    """Tests that governance fields are blocked in vendor overrides."""

    def test_constitution_injection_blocked(self) -> None:
        """Constitution override would remove P-003/P-020/P-022 compliance."""
        overrides = {
            "constitution": {
                "principles_applied": [],
                "forbidden_actions": [],
            }
        }
        errors = CLAUDE_CODE_OVERRIDE_SPEC.validate(overrides)
        assert len(errors) == 1
        assert "constitution" in errors[0]

    def test_guardrails_injection_blocked(self) -> None:
        """Guardrails override would disable output filtering."""
        overrides = {
            "guardrails": {
                "output_filtering": [],
                "fallback_behavior": "ignore",
            }
        }
        errors = CLAUDE_CODE_OVERRIDE_SPEC.validate(overrides)
        assert len(errors) == 1
        assert "guardrails" in errors[0]

    def test_enforcement_injection_blocked(self) -> None:
        """Enforcement override would change quality tier."""
        overrides = {"enforcement": {"tier": "none"}}
        errors = CLAUDE_CODE_OVERRIDE_SPEC.validate(overrides)
        assert len(errors) == 1
        assert "enforcement" in errors[0]

    def test_capabilities_injection_blocked(self) -> None:
        """Capabilities override would remove forbidden_actions."""
        overrides = {"capabilities": {"forbidden_actions": []}}
        errors = CLAUDE_CODE_OVERRIDE_SPEC.validate(overrides)
        assert len(errors) == 1

    def test_nested_key_injection_via_top_level(self) -> None:
        """Even valid-looking nested structures under blocked keys are rejected."""
        overrides = {"constitution": {"reference": "harmless-looking"}}
        errors = CLAUDE_CODE_OVERRIDE_SPEC.validate(overrides)
        assert len(errors) == 1

    def test_multiple_governance_fields_all_blocked(self) -> None:
        """Multiple governance fields in one override are all rejected."""
        overrides = {
            "constitution": {},
            "guardrails": {},
            "enforcement": {},
            "capabilities": {},
            "persona": {},
            "version": "evil",
        }
        errors = CLAUDE_CODE_OVERRIDE_SPEC.validate(overrides)
        assert len(errors) == 6

    def test_mixed_valid_and_governance_fields(self) -> None:
        """Valid vendor keys pass; governance keys are still rejected."""
        overrides = {
            "maxTurns": 5,
            "constitution": {"evil": True},
        }
        errors = CLAUDE_CODE_OVERRIDE_SPEC.validate(overrides)
        assert len(errors) == 1
        assert "constitution" in errors[0]


class TestPathTraversal:
    """Tests that path traversal in agent names doesn't escape skill dirs."""

    def test_dotdot_in_agent_name(self, tmp_path: Path) -> None:
        """Agent name with ../ should resolve within skills dir (no escape)."""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()
        provider = FilesystemVendorOverrideProvider(skills_dir)
        result = provider.get_overrides("../../etc/passwd", "skill", "claude_code")
        assert result == {}

    def test_absolute_path_in_agent_name(self, tmp_path: Path) -> None:
        """Absolute path in agent name just produces a non-existent path."""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()
        provider = FilesystemVendorOverrideProvider(skills_dir)
        result = provider.get_overrides("/etc/passwd", "skill", "claude_code")
        assert result == {}

    def test_dotdot_in_skill_name(self, tmp_path: Path) -> None:
        """Skill name with ../ should resolve within skills dir."""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()
        provider = FilesystemVendorOverrideProvider(skills_dir)
        result = provider.get_overrides("agent", "../../etc", "claude_code")
        assert result == {}


class TestYamlSafety:
    """Tests that YAML parsing is safe."""

    def test_yaml_bomb_handled(self, tmp_path: Path) -> None:
        """Large YAML document doesn't crash; safe_load handles it."""
        skills_dir = tmp_path / "skills"
        comp_dir = skills_dir / "skill" / "composition"
        comp_dir.mkdir(parents=True)
        (comp_dir / "agent.claude-code.yaml").write_text("a: " + "x" * 100_000, encoding="utf-8")
        provider = FilesystemVendorOverrideProvider(skills_dir)
        result = provider.get_overrides("agent", "skill", "claude_code")
        assert isinstance(result, dict)

    def test_empty_file_returns_empty_dict(self, tmp_path: Path) -> None:
        skills_dir = tmp_path / "skills"
        comp_dir = skills_dir / "skill" / "composition"
        comp_dir.mkdir(parents=True)
        (comp_dir / "agent.claude-code.yaml").write_text("", encoding="utf-8")
        provider = FilesystemVendorOverrideProvider(skills_dir)
        result = provider.get_overrides("agent", "skill", "claude_code")
        assert result == {}


class TestCustomSpec:
    """Tests for custom VendorOverrideSpec instances."""

    def test_empty_allowlist_blocks_everything(self) -> None:
        spec = VendorOverrideSpec(vendor="strict", allowed_keys=frozenset())
        errors = spec.validate({"anything": "value"})
        assert len(errors) == 1

    def test_single_key_allowlist(self) -> None:
        spec = VendorOverrideSpec(vendor="minimal", allowed_keys=frozenset({"onlyThis"}))
        assert spec.validate({"onlyThis": "ok"}) == []
        assert len(spec.validate({"onlyThis": "ok", "other": "bad"})) == 1


# ---------------------------------------------------------------------------
# Governance field exclusion from composed frontmatter
# ---------------------------------------------------------------------------


def _make_md_artifact(name: str, agents_dir: Path) -> GeneratedArtifact:
    """Create a .md GeneratedArtifact with frontmatter + body."""
    fm = {"name": name, "description": f"Test agent {name}", "model": "sonnet"}
    fm_str = yaml.dump(fm, default_flow_style=False, sort_keys=False)
    content = f"---\n{fm_str}---\n<agent>\n<identity>\nTest body\n</identity>\n</agent>\n"
    return GeneratedArtifact(
        path=agents_dir / f"{name}.md",
        content=content,
        vendor=VendorTarget.CLAUDE_CODE,
        source_agent=name,
        artifact_type="agent_definition",
    )


def _make_gov_artifact(name: str, agents_dir: Path) -> GeneratedArtifact:
    """Create a .governance.yaml GeneratedArtifact with governance fields."""
    gov = {
        "version": "1.0.0",
        "tool_tier": "T2",
        "identity": {"role": "Test Role", "cognitive_mode": "convergent"},
        "persona": {"tone": "professional"},
        "guardrails": {"fallback_behavior": "warn_and_retry"},
        "constitution": {"principles_applied": ["P-003", "P-020", "P-022"]},
    }
    content = yaml.dump(gov, default_flow_style=False, sort_keys=False)
    return GeneratedArtifact(
        path=agents_dir / f"{name}.governance.yaml",
        content=content,
        vendor=VendorTarget.CLAUDE_CODE,
        source_agent=name,
        artifact_type="governance",
    )


def _build_handler(
    agents: list[Any],
    tmp_path: Path,
    governance_defaults: dict[str, Any] | None = None,
) -> tuple[ComposeAgentsCommandHandler, MagicMock]:
    """Build handler with mocked repo/adapter for governance exclusion tests."""
    mock_repo = MagicMock()
    mock_adapter = MagicMock()

    if agents:
        mock_repo.get.return_value = agents[0]
    mock_repo.list_all.return_value = agents

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
        governance_defaults=governance_defaults
        or {
            "version": "1.0.0",
            "persona": {"tone": "professional"},
            "guardrails": {"fallback_behavior": "warn_and_retry"},
        },
        vendor_defaults={"permissionMode": "default", "background": False},
    )
    return handler, mock_repo


class TestGovernanceFieldExclusion:
    """Tests that composed frontmatter contains ONLY Claude Code official fields.

    This is the inverse of TestGovernanceFieldInjection (which blocks governance
    via overrides); this tests that governance is stripped from the default merge path.
    """

    _GOVERNANCE_FIELDS = {
        "version",
        "persona",
        "guardrails",
        "constitution",
        "identity",
        "tool_tier",
        "output",
        "validation",
        "enforcement",
        "capabilities",
    }

    def test_composed_frontmatter_excludes_governance_when_defaults_contain_governance_then_only_vendor_fields(
        self, make_canonical_agent: Any, tmp_path: Path
    ) -> None:
        """Governance fields from defaults/governance.yaml must not leak into frontmatter."""
        agent = make_canonical_agent(name="gov-strip-test", skill="test-skill")
        handler, _ = _build_handler(
            [agent],
            tmp_path,
            governance_defaults={
                "version": "1.0.0",
                "persona": {"tone": "professional"},
                "guardrails": {"fallback_behavior": "warn_and_retry"},
                "enforcement": {"tier": "C2"},
            },
        )
        command = ComposeAgentsCommand(vendor="claude_code", agent_name="gov-strip-test")
        handler.handle(command)

        composed_file = tmp_path / "skills" / "test-skill" / "agents" / "gov-strip-test.md"
        content = composed_file.read_text(encoding="utf-8")
        end = content.find("---", 3)
        fm = yaml.safe_load(content[3:end])

        fm_keys = set(fm.keys())
        leaked = fm_keys & self._GOVERNANCE_FIELDS
        assert leaked == set(), f"Governance fields leaked into frontmatter: {leaked}"

    def test_composed_frontmatter_preserves_all_vendor_when_agent_has_all_official_fields_then_all_present(
        self, make_canonical_agent: Any, tmp_path: Path
    ) -> None:
        """All Claude Code official fields present in merge should survive filtering."""
        agent = make_canonical_agent(
            name="all-vendor-test",
            skill="test-skill",
            extra_yaml={"maxTurns": 10, "isolation": True, "background": True},
        )
        handler, _ = _build_handler([agent], tmp_path)
        command = ComposeAgentsCommand(vendor="claude_code", agent_name="all-vendor-test")
        handler.handle(command)

        composed_file = tmp_path / "skills" / "test-skill" / "agents" / "all-vendor-test.md"
        content = composed_file.read_text(encoding="utf-8")
        end = content.find("---", 3)
        fm = yaml.safe_load(content[3:end])

        # These vendor fields should be present
        assert "name" in fm
        assert "description" in fm
        assert "model" in fm
        assert "permissionMode" in fm
        assert "maxTurns" in fm
        assert "isolation" in fm
        assert "background" in fm
