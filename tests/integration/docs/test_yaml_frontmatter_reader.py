# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Integration tests for YamlFrontmatterReader against real skill and agent files.

Tests verify that YamlFrontmatterReader correctly parses YAML frontmatter from
real SKILL.md and agent definition files in the skills/ directory without mocks.

Test methodology:
    - All tests use real files from the repository; no mocks.
    - Covers the two primary file types: SKILL.md and agents/*.md.
    - Covers the ``>-`` block scalar YAML path (DA-003).
    - Covers error paths: FileNotFoundError and empty-frontmatter files.

Security note:
    YamlFrontmatterReader uses ``yaml.safe_load`` exclusively.  These tests
    confirm that real-world frontmatter does not require ``yaml.load`` or
    arbitrary-code-execution paths (OWASP A03/Injection).

References:
    - BUG-001: YamlFrontmatterReader replaces AstFrontmatterReader in bootstrap
    - DA-001: Validates agent extraction path (agents/*.md frontmatter reading)
    - DA-003: Validates complex ``>-`` block scalar YAML (contract-design skill)
    - PROJ-0037-doc-module: Phase 2 integration tests
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

# Mark all tests in this module as integration tests.
pytestmark = [
    pytest.mark.integration,
]

# ---------------------------------------------------------------------------
# Project root discovery (same pattern as test_adversary_skill.py)
# ---------------------------------------------------------------------------

_PROJECT_ROOT = Path(__file__).parent.parent.parent.parent


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _reader():
    """Return a fresh YamlFrontmatterReader instance."""
    from src.docs.infrastructure.adapters.yaml_frontmatter_reader import (
        YamlFrontmatterReader,
    )

    return YamlFrontmatterReader()


# ---------------------------------------------------------------------------
# Happy-path: SKILL.md frontmatter
# ---------------------------------------------------------------------------


class TestSkillMdFrontmatter:
    """Tests for reading frontmatter from SKILL.md files."""

    @pytest.mark.happy_path
    def test_adversary_skill_md_when_read_then_has_name_adversary(self) -> None:
        """SKILL.md frontmatter for adversary skill contains name == 'adversary'.

        DA-001 baseline: the primary SKILL.md path must return a dict with
        a 'name' key so that SkillExtractor can identify the skill.
        """
        reader = _reader()
        skill_path = str(_PROJECT_ROOT / "skills" / "adversary" / "SKILL.md")

        result = reader.read_frontmatter(skill_path)

        assert isinstance(result, dict), "Expected a dict from read_frontmatter"
        assert "name" in result, "Frontmatter dict must contain 'name' key"
        assert result["name"] == "adversary"

    @pytest.mark.happy_path
    def test_contract_design_skill_md_when_read_then_has_correct_name_and_description(
        self,
    ) -> None:
        """contract-design SKILL.md uses a ``>-`` block scalar; must parse correctly.

        DA-003: Validates the complex block scalar YAML path.  The description
        field in skills/contract-design/SKILL.md uses the YAML ``>-`` folded
        block scalar syntax.  YamlFrontmatterReader must parse this without
        truncation or error.
        """
        reader = _reader()
        skill_path = str(_PROJECT_ROOT / "skills" / "contract-design" / "SKILL.md")

        result = reader.read_frontmatter(skill_path)

        assert isinstance(result, dict)
        assert result.get("name") == "contract-design"
        description = result.get("description", "")
        assert isinstance(description, str)
        assert len(description) > 50, (
            f"description length {len(description)} must exceed 50 chars; "
            f"'>' block scalar may have been truncated or empty"
        )


# ---------------------------------------------------------------------------
# Happy-path: agent file frontmatter
# ---------------------------------------------------------------------------


class TestAgentFileFrontmatter:
    """Tests for reading frontmatter from agents/*.md files."""

    @pytest.mark.happy_path
    def test_adv_executor_agent_when_read_then_has_name_adv_executor(self) -> None:
        """agents/*.md frontmatter for adv-executor contains name == 'adv-executor'.

        DA-001: Validates the agent extraction path.  Agent files live at
        skills/{skill}/agents/{agent}.md and must return a dict with 'name'
        so that SkillExtractor._extract_agent can identify the agent.
        """
        reader = _reader()
        agent_path = str(_PROJECT_ROOT / "skills" / "adversary" / "agents" / "adv-executor.md")

        result = reader.read_frontmatter(agent_path)

        assert isinstance(result, dict), "Expected a dict from read_frontmatter"
        assert "name" in result, "Agent frontmatter dict must contain 'name' key"
        assert result["name"] == "adv-executor"


# ---------------------------------------------------------------------------
# Error paths
# ---------------------------------------------------------------------------


class TestErrorPaths:
    """Tests for error and edge-case frontmatter reading behaviour."""

    @pytest.mark.negative
    def test_nonexistent_file_when_read_then_raises_file_not_found_error(
        self,
    ) -> None:
        """Reading a nonexistent file raises FileNotFoundError.

        The contract defined in IFrontmatterReader requires FileNotFoundError
        when the target file does not exist.  SkillExtractor depends on this to
        distinguish 'file missing' from 'no frontmatter'.
        """
        reader = _reader()
        nonexistent = str(_PROJECT_ROOT / "skills" / "__nonexistent__" / "SKILL.md")

        with pytest.raises(FileNotFoundError):
            reader.read_frontmatter(nonexistent)

    @pytest.mark.edge_case
    def test_file_without_frontmatter_when_read_then_returns_empty_dict(
        self,
    ) -> None:
        """Reading a file with no ``---`` frontmatter block returns an empty dict.

        The contract defined in IFrontmatterReader requires an empty dict (not
        None, not an error) when the file has no frontmatter.  SkillExtractor
        calls ``frontmatter.get('name')`` and relies on this behaviour to
        detect and skip skills with missing required fields.
        """
        reader = _reader()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as tmp:
            tmp.write("# A Markdown File\n\nThis file has no frontmatter block.\n")
            tmp_path = tmp.name

        try:
            result = reader.read_frontmatter(tmp_path)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

        assert result == {}, f"Expected empty dict, got {result!r}"
