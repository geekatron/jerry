# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Round-trip regression tests for the compose pipeline.

Verifies that compose → extract → compose produces idempotent output
for representative agents covering all body formats, tool tiers, and
MCP configurations.

References:
    - PROJ-012: Agent Configuration Extraction & Schema Enforcement
    - P-022: No Deception (silent pass-through violates this)
    - H-20: BDD test-first, 60/30/10 scenario distribution
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

import pytest
import yaml

from src.agents.application.commands.compose_agents_command import ComposeAgentsCommand
from src.agents.application.handlers.commands.compose_agents_command_handler import (
    ComposeAgentsCommandHandler,
)
from src.agents.domain.services.compose_validator import ComposeValidator
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

# Project root for sourcing real canonical files
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_SKILLS_DIR = _PROJECT_ROOT / "skills"
_SCHEMAS_DIR = _PROJECT_ROOT / "docs" / "schemas"
_MAPPINGS_PATH = _PROJECT_ROOT / "src" / "agents" / "infrastructure" / "mappings.yaml"

# Representative agents covering different body formats, tool tiers, MCP configs
REPRESENTATIVE_AGENTS: list[tuple[str, str]] = [
    ("worktracker", "wt-auditor"),  # T2, CLI commands
    ("problem-solving", "ps-validator"),  # T2, CLI commands
    ("problem-solving", "ps-architect"),  # T4, has MCP servers
    ("adversary", "adv-executor"),  # T2, strategy templates
    ("diataxis", "diataxis-howto"),  # T2, DESC formatting
]


def _copy_canonical_sources(
    src_skills: Path,
    dst_skills: Path,
    skill: str,
    agent_name: str,
) -> None:
    """Copy canonical source files for a single agent to the destination.

    Args:
        src_skills: Source skills/ directory.
        dst_skills: Destination skills/ directory.
        skill: Skill name (directory).
        agent_name: Agent name (file prefix).
    """
    src_composition = src_skills / skill / "composition"
    dst_composition = dst_skills / skill / "composition"
    dst_composition.mkdir(parents=True, exist_ok=True)

    for suffix in (".jerry.yaml", ".jerry.prompt.md", ".claude-code.yaml"):
        src_file = src_composition / f"{agent_name}{suffix}"
        if src_file.exists():
            shutil.copy2(src_file, dst_composition / src_file.name)


def _create_compose_handler(
    skills_dir: Path,
    schemas_dir: Path | None = None,
) -> ComposeAgentsCommandHandler:
    """Create a fully wired compose handler for testing.

    Uses the real mappings.yaml and defaults from the project,
    pointing at the given skills_dir for canonical sources and output.

    Args:
        skills_dir: Path to the skills/ directory.
        schemas_dir: Path to schemas/ directory. Defaults to project schemas.

    Returns:
        Configured ComposeAgentsCommandHandler.
    """
    schemas = schemas_dir or _SCHEMAS_DIR

    mappings_content = _MAPPINGS_PATH.read_text(encoding="utf-8")
    mappings = yaml.safe_load(mappings_content)
    tool_mapper = ToolMapper.from_mappings(mappings)
    prompt_transformer = PromptTransformer()
    adapter = ClaudeCodeAdapter(tool_mapper, prompt_transformer, skills_dir)
    repository = FilesystemAgentRepository(skills_dir)

    # Load governance defaults (Layer 1)
    governance_path = schemas / "jerry-agent-defaults.yaml"
    governance_defaults: dict[str, Any] = {}
    if governance_path.exists():
        governance_defaults = yaml.safe_load(governance_path.read_text(encoding="utf-8")) or {}

    # Load vendor defaults (Layer 2)
    vendor_defaults_path = schemas / "jerry-claude-code-defaults.yaml"
    vendor_defaults: dict[str, Any] = {}
    if vendor_defaults_path.exists():
        vendor_defaults = yaml.safe_load(vendor_defaults_path.read_text(encoding="utf-8")) or {}

    vendor_override_provider = FilesystemVendorOverrideProvider(skills_dir)
    defaults_composer = DefaultsComposer()

    # ComposeValidator for post-composition checks
    anthropic_schema_path = schemas / "jerry-claude-agent-definition-v1.schema.json"
    validator = ComposeValidator(
        anthropic_schema_path=anthropic_schema_path if anthropic_schema_path.exists() else None,
    )

    return ComposeAgentsCommandHandler(
        repository=repository,
        adapters={"claude_code": adapter},
        defaults_composer=defaults_composer,
        governance_defaults=governance_defaults,
        vendor_defaults=vendor_defaults,
        vendor_override_provider=vendor_override_provider,
        vendor_override_spec=CLAUDE_CODE_OVERRIDE_SPEC,
        validator=validator,
    )


def _parse_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    """Parse YAML frontmatter and body from composed .md content.

    Args:
        content: Full .md file content.

    Returns:
        Tuple of (frontmatter_dict, body_string).
    """
    if not content.startswith("---"):
        return {}, content
    end = content.find("---", 3)
    if end == -1:
        return {}, content
    fm_text = content[3:end].strip()
    body = content[end + 3 :].lstrip("\n")
    fm_data = yaml.safe_load(fm_text) or {}
    return fm_data, body


def _normalize_content(content: str) -> str:
    """Normalize composed content for semantic comparison.

    Strips trailing whitespace from each line and normalizes line endings.

    Args:
        content: Raw composed .md content.

    Returns:
        Normalized content string.
    """
    lines = content.splitlines()
    return "\n".join(line.rstrip() for line in lines).strip() + "\n"


@pytest.mark.regression
class TestComposeRoundTrip:
    """Round-trip regression: compose → extract → compose must be idempotent."""

    @pytest.mark.parametrize(
        "skill,agent_name",
        REPRESENTATIVE_AGENTS,
        ids=[a[1] for a in REPRESENTATIVE_AGENTS],
    )
    def test_round_trip_when_compose_twice_then_output_identical(
        self, skill: str, agent_name: str, tmp_path: Path
    ) -> None:
        """GIVEN canonical sources for an agent
        WHEN composed twice from the same canonical sources
        THEN both composed outputs are byte-identical.
        """
        # Arrange: copy canonical sources to temp
        skills_dir = tmp_path / "skills"
        _copy_canonical_sources(_SKILLS_DIR, skills_dir, skill, agent_name)

        handler = _create_compose_handler(skills_dir)
        command = ComposeAgentsCommand(vendor="claude_code", agent_name=agent_name)

        # Act: compose twice
        result_1 = handler.handle(command)
        assert result_1.composed == 1, f"First compose failed: {result_1.errors}"
        assert result_1.failed == 0, f"First compose had failures: {result_1.errors}"

        composed_file = skills_dir / skill / "agents" / f"{agent_name}.md"
        assert composed_file.exists(), f"Composed file not found: {composed_file}"
        content_1 = composed_file.read_text(encoding="utf-8")

        result_2 = handler.handle(command)
        assert result_2.composed == 1, f"Second compose failed: {result_2.errors}"
        content_2 = composed_file.read_text(encoding="utf-8")

        # Assert: idempotent
        assert _normalize_content(content_1) == _normalize_content(content_2), (
            f"Compose is not idempotent for {agent_name}: "
            f"outputs differ between first and second compose"
        )

    @pytest.mark.parametrize(
        "skill,agent_name",
        REPRESENTATIVE_AGENTS,
        ids=[a[1] for a in REPRESENTATIVE_AGENTS],
    )
    def test_round_trip_when_composed_then_validator_passes(
        self, skill: str, agent_name: str, tmp_path: Path
    ) -> None:
        """GIVEN canonical sources for an agent
        WHEN composed from canonical sources
        THEN composed output passes ComposeValidator with 0 errors.
        """
        # Arrange
        skills_dir = tmp_path / "skills"
        _copy_canonical_sources(_SKILLS_DIR, skills_dir, skill, agent_name)

        handler = _create_compose_handler(skills_dir)
        command = ComposeAgentsCommand(vendor="claude_code", agent_name=agent_name)

        # Act
        result = handler.handle(command)

        # Assert
        assert result.composed == 1, f"Compose failed: {result.errors}"
        assert result.failed == 0, f"Validation failed: {result.errors}"
        assert len(result.errors) == 0, f"Unexpected errors: {result.errors}"

    @pytest.mark.parametrize(
        "skill,agent_name",
        REPRESENTATIVE_AGENTS,
        ids=[a[1] for a in REPRESENTATIVE_AGENTS],
    )
    def test_round_trip_when_extract_then_governance_preserved(
        self, skill: str, agent_name: str, tmp_path: Path
    ) -> None:
        """GIVEN canonical sources with governance fields
        WHEN composed and then extracted
        THEN governance fields (version, tool_tier) survive the round-trip.
        """
        # Arrange
        skills_dir = tmp_path / "skills"
        _copy_canonical_sources(_SKILLS_DIR, skills_dir, skill, agent_name)

        mappings = yaml.safe_load(_MAPPINGS_PATH.read_text(encoding="utf-8"))
        tool_mapper = ToolMapper.from_mappings(mappings)
        prompt_transformer = PromptTransformer()
        adapter = ClaudeCodeAdapter(tool_mapper, prompt_transformer, skills_dir)

        handler = _create_compose_handler(skills_dir)
        command = ComposeAgentsCommand(vendor="claude_code", agent_name=agent_name)

        # Read original canonical YAML for expected values
        canonical_yaml_path = skills_dir / skill / "composition" / f"{agent_name}.jerry.yaml"
        canonical_data = yaml.safe_load(canonical_yaml_path.read_text(encoding="utf-8"))
        expected_version = canonical_data.get("version", "1.0.0")
        expected_tool_tier = canonical_data.get("tool_tier", "T1")

        # Act: compose
        result = handler.handle(command)
        assert result.composed == 1, f"Compose failed: {result.errors}"

        composed_file = skills_dir / skill / "agents" / f"{agent_name}.md"
        extracted = adapter.extract(str(composed_file))

        # Assert: governance fields preserved
        assert extracted.version == expected_version, (
            f"Version degraded from {expected_version!r} to {extracted.version!r}"
        )
        assert extracted.tool_tier.value == expected_tool_tier, (
            f"Tool tier degraded from {expected_tool_tier!r} to {extracted.tool_tier.value!r}"
        )

    def test_round_trip_when_body_has_jerry_plugin_root_then_compose_fails(
        self, tmp_path: Path
    ) -> None:
        """GIVEN canonical sources with JERRY_PLUGIN_ROOT injected
        WHEN composed with validator wired in
        THEN compose fails with CV-001 error.
        """
        # Arrange: copy and inject regression
        skill, agent_name = "worktracker", "wt-auditor"
        skills_dir = tmp_path / "skills"
        _copy_canonical_sources(_SKILLS_DIR, skills_dir, skill, agent_name)

        # Inject JERRY_PLUGIN_ROOT into prompt body
        prompt_path = skills_dir / skill / "composition" / f"{agent_name}.jerry.prompt.md"
        original_content = prompt_path.read_text(encoding="utf-8")
        injected = original_content + "\nUse $JERRY_PLUGIN_ROOT/scripts/run.sh\n"
        prompt_path.write_text(injected, encoding="utf-8")

        handler = _create_compose_handler(skills_dir)
        command = ComposeAgentsCommand(vendor="claude_code", agent_name=agent_name)

        # Act
        result = handler.handle(command)

        # Assert: compose reports failure
        assert result.failed > 0, "Expected compose to fail with CV-001"
        assert any("CV-001" in e for e in result.errors), (
            f"Expected CV-001 error, got: {result.errors}"
        )

    def test_round_trip_when_body_has_python_import_then_compose_fails(
        self, tmp_path: Path
    ) -> None:
        """GIVEN canonical sources with Python API import injected
        WHEN composed with validator wired in
        THEN compose fails with CV-002 error.
        """
        # Arrange: copy and inject regression
        skill, agent_name = "problem-solving", "ps-validator"
        skills_dir = tmp_path / "skills"
        _copy_canonical_sources(_SKILLS_DIR, skills_dir, skill, agent_name)

        prompt_path = skills_dir / skill / "composition" / f"{agent_name}.jerry.prompt.md"
        original_content = prompt_path.read_text(encoding="utf-8")
        injected = original_content + "\nfrom skills.problem_solving.scripts import validate\n"
        prompt_path.write_text(injected, encoding="utf-8")

        handler = _create_compose_handler(skills_dir)
        command = ComposeAgentsCommand(vendor="claude_code", agent_name=agent_name)

        # Act
        result = handler.handle(command)

        # Assert
        assert result.failed > 0, "Expected compose to fail with CV-002"
        assert any("CV-002" in e for e in result.errors), (
            f"Expected CV-002 error, got: {result.errors}"
        )

    @pytest.mark.parametrize(
        "skill,agent_name",
        [a for a in REPRESENTATIVE_AGENTS if a[1] == "ps-architect"],
        ids=["ps-architect"],
    )
    def test_round_trip_when_agent_has_mcp_servers_then_config_preserved(
        self, skill: str, agent_name: str, tmp_path: Path
    ) -> None:
        """GIVEN an agent with mcpServers in vendor overrides
        WHEN composed and verified
        THEN mcpServers configuration is present in frontmatter.
        """
        # Arrange
        skills_dir = tmp_path / "skills"
        _copy_canonical_sources(_SKILLS_DIR, skills_dir, skill, agent_name)

        handler = _create_compose_handler(skills_dir)
        command = ComposeAgentsCommand(vendor="claude_code", agent_name=agent_name)

        # Act
        result = handler.handle(command)
        assert result.composed == 1, f"Compose failed: {result.errors}"

        composed_file = skills_dir / skill / "agents" / f"{agent_name}.md"
        content = composed_file.read_text(encoding="utf-8")
        frontmatter, _ = _parse_frontmatter(content)

        # Assert: mcpServers present (ps-architect is T4 with MCP)
        assert "mcpServers" in frontmatter, (
            f"mcpServers missing from {agent_name} frontmatter: {list(frontmatter.keys())}"
        )
