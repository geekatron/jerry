# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Golden file snapshot tests for composed agent output.

Frozen snapshots of composed agent output. When the compose pipeline
changes, tests fail — forcing explicit review and snapshot update.

Update golden files:
    uv run pytest tests/regression/test_compose_golden_files.py --update-golden

References:
    - PROJ-012: Agent Configuration Extraction & Schema Enforcement
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
_GOLDEN_DIR = Path(__file__).resolve().parent / "golden" / "agents"

# Same representative agents as round-trip tests
GOLDEN_AGENTS: list[tuple[str, str]] = [
    ("worktracker", "wt-auditor"),
    ("problem-solving", "ps-validator"),
    ("problem-solving", "ps-architect"),
    ("adversary", "adv-executor"),
    ("diataxis", "diataxis-howto"),
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
) -> ComposeAgentsCommandHandler:
    """Create a fully wired compose handler for testing.

    Args:
        skills_dir: Path to the skills/ directory.

    Returns:
        Configured ComposeAgentsCommandHandler.
    """
    mappings_content = _MAPPINGS_PATH.read_text(encoding="utf-8")
    mappings = yaml.safe_load(mappings_content)
    tool_mapper = ToolMapper.from_mappings(mappings)
    prompt_transformer = PromptTransformer()
    adapter = ClaudeCodeAdapter(tool_mapper, prompt_transformer, skills_dir)
    repository = FilesystemAgentRepository(skills_dir)

    governance_path = _SCHEMAS_DIR / "jerry-agent-defaults.yaml"
    governance_defaults: dict[str, Any] = {}
    if governance_path.exists():
        governance_defaults = yaml.safe_load(governance_path.read_text(encoding="utf-8")) or {}

    vendor_defaults_path = _SCHEMAS_DIR / "jerry-claude-code-defaults.yaml"
    vendor_defaults: dict[str, Any] = {}
    if vendor_defaults_path.exists():
        vendor_defaults = yaml.safe_load(vendor_defaults_path.read_text(encoding="utf-8")) or {}

    vendor_override_provider = FilesystemVendorOverrideProvider(skills_dir)
    defaults_composer = DefaultsComposer()

    anthropic_schema_path = _SCHEMAS_DIR / "jerry-claude-agent-definition-v1.schema.json"
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


def _compose_agent(skill: str, agent_name: str, tmp_path: Path) -> str:
    """Compose a single agent and return the composed content.

    Args:
        skill: Skill name.
        agent_name: Agent name.
        tmp_path: Temporary directory for compose output.

    Returns:
        Composed .md file content.
    """
    skills_dir = tmp_path / "skills"
    _copy_canonical_sources(_SKILLS_DIR, skills_dir, skill, agent_name)

    handler = _create_compose_handler(skills_dir)
    command = ComposeAgentsCommand(vendor="claude_code", agent_name=agent_name)
    result = handler.handle(command)

    assert result.composed == 1, f"Compose failed for {agent_name}: {result.errors}"
    assert result.failed == 0, f"Validation failed for {agent_name}: {result.errors}"

    composed_file = skills_dir / skill / "agents" / f"{agent_name}.md"
    return composed_file.read_text(encoding="utf-8")


@pytest.mark.regression
class TestComposeGoldenFiles:
    """Golden file regression: composed output must match frozen snapshots."""

    @pytest.mark.parametrize(
        "skill,agent_name",
        GOLDEN_AGENTS,
        ids=[a[1] for a in GOLDEN_AGENTS],
    )
    def test_compose_when_canonical_unchanged_then_output_matches_golden(
        self,
        skill: str,
        agent_name: str,
        tmp_path: Path,
        update_golden: bool,
    ) -> None:
        """GIVEN canonical sources and a frozen golden file
        WHEN composed from canonical sources
        THEN output matches the golden file exactly.
        """
        golden_file = _GOLDEN_DIR / f"{agent_name}.md"

        # Compose from canonical sources
        composed_content = _compose_agent(skill, agent_name, tmp_path)
        normalized = _normalize_content(composed_content)

        if update_golden or not golden_file.exists():
            # Create or update golden file
            _GOLDEN_DIR.mkdir(parents=True, exist_ok=True)
            golden_file.write_text(normalized, encoding="utf-8")
            if not update_golden:
                pytest.fail(
                    f"Golden file created for {agent_name}. "
                    f"Review {golden_file} and re-run tests to verify."
                )
            return

        # Compare against golden
        expected = golden_file.read_text(encoding="utf-8")
        assert normalized == expected, (
            f"Composed output for {agent_name} differs from golden file.\n"
            f"Golden: {golden_file}\n"
            f"Run 'uv run pytest tests/regression/test_compose_golden_files.py "
            f"--update-golden' to accept changes."
        )

    @pytest.mark.parametrize(
        "agent_name",
        [a[1] for a in GOLDEN_AGENTS],
        ids=[a[1] for a in GOLDEN_AGENTS],
    )
    def test_golden_frontmatter_when_validated_then_passes_anthropic_schema(
        self,
        agent_name: str,
    ) -> None:
        """GIVEN a golden file for a composed agent
        WHEN frontmatter is validated against jerry-claude-agent-definition-v1.schema.json
        THEN validation passes with zero errors.
        """
        golden_file = _GOLDEN_DIR / f"{agent_name}.md"
        if not golden_file.exists():
            pytest.skip(f"Golden file not yet created for {agent_name}")

        content = golden_file.read_text(encoding="utf-8")

        anthropic_schema_path = _SCHEMAS_DIR / "jerry-claude-agent-definition-v1.schema.json"
        validator = ComposeValidator(
            anthropic_schema_path=anthropic_schema_path if anthropic_schema_path.exists() else None,
        )
        result = validator.validate(content, agent_name=agent_name)

        assert result.is_valid, (
            f"Golden file for {agent_name} fails schema validation: "
            + "; ".join(f"[{f.check_id}] {f.message}" for f in result.errors)
        )
