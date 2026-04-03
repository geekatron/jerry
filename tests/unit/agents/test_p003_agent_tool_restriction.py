# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""Tests for P-003 Agent tool restriction in CLI frontmatter validation.

Verifies that the ValidateFrontmatterCommandHandler enforces P-003:
Agent/Task tool access is restricted to T5 orchestrator agents only.

References:
    - STORY-022: P-003 Agent tool restriction (original)
    - STORY-025: Port from scripts/validate-agent-frontmatter.py to CLI handler
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from src.agents.application.commands.validate_frontmatter_command_handler import (
    ValidateFrontmatterCommandHandler,
)


def _repo_root() -> Path:
    """Find repo root by walking up to pyproject.toml."""
    p = Path(__file__).resolve().parent
    while p != p.parent:
        if (p / "pyproject.toml").exists():
            return p
        p = p.parent
    return Path.cwd()


REPO_ROOT = _repo_root()
AGENT_SCHEMA_PATH = REPO_ROOT / "docs" / "schemas" / "claude-code-frontmatter-v1.schema.json"
SKILL_SCHEMA_PATH = REPO_ROOT / "docs" / "schemas" / "claude-code-skill-frontmatter-v1.schema.json"


@pytest.fixture()
def handler() -> ValidateFrontmatterCommandHandler:
    """Create handler with real schemas."""
    return ValidateFrontmatterCommandHandler(
        repo_root=REPO_ROOT,
        agent_schema_path=AGENT_SCHEMA_PATH,
        skill_schema_path=SKILL_SCHEMA_PATH,
    )


@pytest.fixture()
def tmp_agent(tmp_path: Path):
    """Factory for creating temp agent .md + .governance.yaml pairs."""

    def _create(
        name: str = "test-agent",
        tools: list[str] | str | None = None,
        tool_tier: str = "T2",
        create_governance: bool = True,
    ) -> Path:
        fm: dict = {"name": name, "description": f"Test agent {name}"}
        if tools is not None:
            fm["tools"] = tools
        md_path = tmp_path / f"{name}.md"
        md_content = f"---\n{yaml.dump(fm, default_flow_style=False)}---\n\nBody text.\n"
        md_path.write_text(md_content, encoding="utf-8")

        if create_governance:
            gov = {"version": "1.0.0", "tool_tier": tool_tier}
            gov_path = tmp_path / f"{name}.governance.yaml"
            gov_path.write_text(yaml.dump(gov), encoding="utf-8")

        return md_path

    return _create


class TestP003AgentToolCheck:
    """STORY-022/025: Error if non-T5 agent has Agent in tools."""

    def test_non_t5_agent_with_agent_tool_produces_error(
        self, handler: ValidateFrontmatterCommandHandler, tmp_agent
    ) -> None:
        """Non-T5 agent with Agent in tools list MUST produce an error."""
        md_path = tmp_agent(tools=["Read", "Write", "Agent"], tool_tier="T2")
        result = handler._validate_agent_file(md_path, md_path.parent)
        p003_errors = [e for e in result.errors if "p003" in e[1].lower()]
        assert len(p003_errors) >= 1, f"Expected P-003 error, got: {result.errors}"

    def test_non_t5_agent_with_task_alias_produces_error(
        self, handler: ValidateFrontmatterCommandHandler, tmp_agent
    ) -> None:
        """Non-T5 agent with Task (alias) in tools list MUST produce an error."""
        md_path = tmp_agent(tools=["Read", "Write", "Task"], tool_tier="T2")
        result = handler._validate_agent_file(md_path, md_path.parent)
        p003_errors = [e for e in result.errors if "p003" in e[1].lower()]
        assert len(p003_errors) >= 1, f"Expected P-003 error for Task alias, got: {result.errors}"

    def test_t5_agent_with_agent_tool_no_error(
        self, handler: ValidateFrontmatterCommandHandler, tmp_agent
    ) -> None:
        """T5 orchestrator with Agent in tools MUST NOT produce a P-003 error."""
        md_path = tmp_agent(
            name="ux-orchestrator",
            tools=["Read", "Write", "Agent"],
            tool_tier="T5",
        )
        result = handler._validate_agent_file(md_path, md_path.parent)
        p003_errors = [e for e in result.errors if "p003" in e[1].lower()]
        assert len(p003_errors) == 0, f"T5 agent should NOT get P-003 error: {p003_errors}"

    def test_agent_without_agent_tool_no_error(
        self, handler: ValidateFrontmatterCommandHandler, tmp_agent
    ) -> None:
        """Agent without Agent/Task in tools produces no P-003 error."""
        md_path = tmp_agent(tools=["Read", "Write", "Grep"], tool_tier="T2")
        result = handler._validate_agent_file(md_path, md_path.parent)
        p003_errors = [e for e in result.errors if "p003" in e[1].lower()]
        assert len(p003_errors) == 0, f"Should have no P-003 errors: {p003_errors}"

    def test_string_format_tools_with_agent_produces_error(
        self, handler: ValidateFrontmatterCommandHandler, tmp_path: Path
    ) -> None:
        """Comma-separated string tools format MUST also be caught."""
        md_path = tmp_path / "string-tools-agent.md"
        md_content = "---\nname: string-tools-agent\ndescription: Test\ntools: Read, Write, Agent\n---\n\nBody.\n"
        md_path.write_text(md_content, encoding="utf-8")
        gov_path = tmp_path / "string-tools-agent.governance.yaml"
        gov_path.write_text("version: 1.0.0\ntool_tier: T2\n", encoding="utf-8")
        result = handler._validate_agent_file(md_path, tmp_path)
        p003_errors = [e for e in result.errors if "p003" in e[1].lower()]
        assert len(p003_errors) >= 1, f"String-format tools should catch Agent: {result.errors}"

    def test_missing_governance_yaml_defaults_to_error(
        self, handler: ValidateFrontmatterCommandHandler, tmp_agent
    ) -> None:
        """If governance.yaml is missing, Agent in tools MUST still error (fail-closed)."""
        md_path = tmp_agent(
            name="no-gov-agent",
            tools=["Read", "Agent"],
            create_governance=False,
        )
        result = handler._validate_agent_file(md_path, md_path.parent)
        p003_errors = [e for e in result.errors if "p003" in e[1].lower()]
        assert len(p003_errors) >= 1, "Missing governance should fail closed"

    def test_t1_agent_with_both_agent_and_task_produces_error(
        self, handler: ValidateFrontmatterCommandHandler, tmp_agent
    ) -> None:
        """T1 agent with both Agent and Task in tools should produce P-003 error."""
        md_path = tmp_agent(tools=["Read", "Agent", "Task"], tool_tier="T1")
        result = handler._validate_agent_file(md_path, md_path.parent)
        p003_errors = [e for e in result.errors if "p003" in e[1].lower()]
        assert len(p003_errors) >= 1

    def test_p003_error_message_includes_fix_guidance(
        self, handler: ValidateFrontmatterCommandHandler, tmp_agent
    ) -> None:
        """P-003 error message should include remediation guidance."""
        md_path = tmp_agent(tools=["Read", "Agent"], tool_tier="T2")
        result = handler._validate_agent_file(md_path, md_path.parent)
        p003_errors = [e for e in result.errors if "p003" in e[1].lower()]
        assert len(p003_errors) >= 1
        error_msg = p003_errors[0][2]
        assert "T5" in error_msg
        assert "remove" in error_msg.lower() or "fix" in error_msg.lower()
