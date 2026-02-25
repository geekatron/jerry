# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Tests for AgentConfigResolver compose methods.

Covers:
- _extract_frontmatter_and_body extraction
- compose_agent_to_file format and content
- compose_all_to_dir batch write, clean behavior, single agent filter
- Defaults merge into composed output

References:
    - PROJ-012 Phase 5: jerry agents compose CLI
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from src.infrastructure.adapters.configuration.agent_config_resolver import (
    AgentConfigResolver,
)

# === Fixtures ===


@pytest.fixture()
def resolver() -> AgentConfigResolver:
    """Create an AgentConfigResolver without config adapter."""
    return AgentConfigResolver(config=None)


@pytest.fixture()
def tmp_skills(tmp_path: Path) -> Path:
    """Create a minimal skills directory with agent files."""
    skill_dir = tmp_path / "skills" / "test-skill" / "agents"
    skill_dir.mkdir(parents=True)

    # Agent with frontmatter + body
    (skill_dir / "test-agent.md").write_text(
        "---\n"
        "name: test-agent\n"
        "version: '1.0.0'\n"
        "model: sonnet\n"
        "identity:\n"
        "  role: Test Agent\n"
        "  expertise:\n"
        "    - testing\n"
        "  cognitive_mode: systematic\n"
        "---\n"
        "# Test Agent\n\n"
        "This is the body.\n",
        encoding="utf-8",
    )

    # Second agent
    (skill_dir / "test-analyst.md").write_text(
        "---\n"
        "name: test-analyst\n"
        "version: '2.0.0'\n"
        "model: opus\n"
        "identity:\n"
        "  role: Test Analyst\n"
        "  expertise:\n"
        "    - analysis\n"
        "  cognitive_mode: convergent\n"
        "---\n"
        "# Test Analyst\n\n"
        "Analyst body.\n",
        encoding="utf-8",
    )

    # File without frontmatter (should be skipped)
    (skill_dir / "README.md").write_text("# Agents\n", encoding="utf-8")

    return tmp_path / "skills"


@pytest.fixture()
def defaults() -> dict:
    """Create minimal defaults dict."""
    return {
        "permissionMode": "default",
        "background": False,
        "version": "1.0.0",
        "constitution": {
            "principles_applied": ["P-003", "P-020", "P-022"],
        },
    }


@pytest.fixture()
def defaults_file(tmp_path: Path, defaults: dict) -> Path:
    """Write defaults to a YAML file."""
    path = tmp_path / "defaults.yaml"
    path.write_text(yaml.dump(defaults), encoding="utf-8")
    return path


@pytest.fixture()
def output_dir(tmp_path: Path) -> Path:
    """Create an output directory."""
    out = tmp_path / "output"
    out.mkdir()
    return out


# === _extract_frontmatter_and_body Tests ===


class TestExtractFrontmatterAndBody:
    """Tests for _extract_frontmatter_and_body."""

    def test_should_extract_frontmatter_and_body(
        self, resolver: AgentConfigResolver, tmp_skills: Path
    ) -> None:
        """Extracts YAML dict and markdown body from a valid agent file."""
        agent_file = tmp_skills / "test-skill" / "agents" / "test-agent.md"
        result = resolver._extract_frontmatter_and_body(agent_file)

        assert result is not None
        fm, body = result
        assert fm["name"] == "test-agent"
        assert fm["model"] == "sonnet"
        assert "# Test Agent" in body
        assert "This is the body." in body

    def test_should_return_none_for_no_frontmatter(
        self, resolver: AgentConfigResolver, tmp_path: Path
    ) -> None:
        """Returns None when file has no YAML frontmatter."""
        no_fm = tmp_path / "no-fm.md"
        no_fm.write_text("# No Frontmatter\n", encoding="utf-8")
        assert resolver._extract_frontmatter_and_body(no_fm) is None

    def test_should_return_none_for_missing_file(
        self, resolver: AgentConfigResolver, tmp_path: Path
    ) -> None:
        """Returns None when file does not exist."""
        assert resolver._extract_frontmatter_and_body(tmp_path / "nonexistent.md") is None

    def test_should_return_none_for_unclosed_frontmatter(
        self, resolver: AgentConfigResolver, tmp_path: Path
    ) -> None:
        """Returns None when closing --- is missing."""
        bad = tmp_path / "unclosed.md"
        bad.write_text("---\nname: test\n# oops no closing\n", encoding="utf-8")
        assert resolver._extract_frontmatter_and_body(bad) is None


# === compose_agent_to_file Tests ===


class TestComposeAgentToFile:
    """Tests for compose_agent_to_file."""

    def test_should_write_composed_file(
        self, resolver: AgentConfigResolver, tmp_skills: Path, defaults: dict, output_dir: Path
    ) -> None:
        """Writes a composed .md file with merged YAML + body."""
        agent_file = tmp_skills / "test-skill" / "agents" / "test-agent.md"
        result = resolver.compose_agent_to_file(agent_file, defaults, output_dir)

        assert result.success is True
        assert result.agent_name == "test-agent"
        assert (output_dir / "test-agent.md").exists()

    def test_composed_file_has_yaml_body_format(
        self, resolver: AgentConfigResolver, tmp_skills: Path, defaults: dict, output_dir: Path
    ) -> None:
        """Composed file starts with --- yaml --- then body."""
        agent_file = tmp_skills / "test-skill" / "agents" / "test-agent.md"
        resolver.compose_agent_to_file(agent_file, defaults, output_dir)

        content = (output_dir / "test-agent.md").read_text(encoding="utf-8")
        assert content.startswith("---\n")
        # Find closing ---
        second_delim = content.index("---", 4)
        assert second_delim > 4
        # Body follows
        after = content[second_delim + 3 :].lstrip("\n")
        assert "# Test Agent" in after

    def test_composed_yaml_includes_defaults(
        self, resolver: AgentConfigResolver, tmp_skills: Path, defaults: dict, output_dir: Path
    ) -> None:
        """Composed YAML includes merged defaults."""
        agent_file = tmp_skills / "test-skill" / "agents" / "test-agent.md"
        resolver.compose_agent_to_file(agent_file, defaults, output_dir)

        content = (output_dir / "test-agent.md").read_text(encoding="utf-8")
        end_idx = content.index("---", 4)
        yaml_str = content[4:end_idx]
        composed = yaml.safe_load(yaml_str)

        assert composed["permissionMode"] == "default"
        assert composed["background"] is False
        assert composed["constitution"]["principles_applied"] == ["P-003", "P-020", "P-022"]

    def test_agent_overrides_defaults(
        self, resolver: AgentConfigResolver, tmp_skills: Path, defaults: dict, output_dir: Path
    ) -> None:
        """Agent-specific fields override defaults."""
        agent_file = tmp_skills / "test-skill" / "agents" / "test-agent.md"
        resolver.compose_agent_to_file(agent_file, defaults, output_dir)

        content = (output_dir / "test-agent.md").read_text(encoding="utf-8")
        end_idx = content.index("---", 4)
        composed = yaml.safe_load(content[4:end_idx])

        # Agent has version 1.0.0 which overrides default 1.0.0 (same in this case)
        assert composed["model"] == "sonnet"
        assert composed["name"] == "test-agent"

    def test_should_return_failure_for_no_frontmatter(
        self, resolver: AgentConfigResolver, tmp_path: Path, defaults: dict, output_dir: Path
    ) -> None:
        """Returns failure ComposeResult for file without frontmatter."""
        bad_file = tmp_path / "bad.md"
        bad_file.write_text("# No frontmatter\n", encoding="utf-8")

        result = resolver.compose_agent_to_file(bad_file, defaults, output_dir)

        assert result.success is False
        assert result.error is not None
        assert "frontmatter" in result.error.lower()


# === compose_all_to_dir Tests ===


class TestComposeAllToDir:
    """Tests for compose_all_to_dir."""

    def test_should_compose_all_agents(
        self,
        resolver: AgentConfigResolver,
        tmp_skills: Path,
        defaults_file: Path,
        output_dir: Path,
    ) -> None:
        """Composes all agents found in skills directory."""
        results = resolver.compose_all_to_dir(
            skills_dir=str(tmp_skills),
            defaults_path=str(defaults_file),
            output_dir=str(output_dir),
        )

        succeeded = [r for r in results if r.success]
        assert len(succeeded) == 2
        assert (output_dir / "test-agent.md").exists()
        assert (output_dir / "test-analyst.md").exists()

    def test_should_compose_single_agent(
        self,
        resolver: AgentConfigResolver,
        tmp_skills: Path,
        defaults_file: Path,
        output_dir: Path,
    ) -> None:
        """Composes only the specified agent when agent_name is provided."""
        results = resolver.compose_all_to_dir(
            skills_dir=str(tmp_skills),
            defaults_path=str(defaults_file),
            output_dir=str(output_dir),
            agent_name="test-agent",
        )

        assert len(results) == 1
        assert results[0].success is True
        assert results[0].agent_name == "test-agent"
        assert (output_dir / "test-agent.md").exists()
        assert not (output_dir / "test-analyst.md").exists()

    def test_should_return_not_found_for_missing_agent(
        self,
        resolver: AgentConfigResolver,
        tmp_skills: Path,
        defaults_file: Path,
        output_dir: Path,
    ) -> None:
        """Returns error result when single agent is not found."""
        results = resolver.compose_all_to_dir(
            skills_dir=str(tmp_skills),
            defaults_path=str(defaults_file),
            output_dir=str(output_dir),
            agent_name="nonexistent",
        )

        assert len(results) == 1
        assert results[0].success is False
        assert "not found" in results[0].error

    def test_clean_removes_existing_md_files(
        self,
        resolver: AgentConfigResolver,
        tmp_skills: Path,
        defaults_file: Path,
        output_dir: Path,
    ) -> None:
        """--clean removes existing .md files before writing."""
        # Create a stale file
        stale = output_dir / "stale-agent.md"
        stale.write_text("stale", encoding="utf-8")

        resolver.compose_all_to_dir(
            skills_dir=str(tmp_skills),
            defaults_path=str(defaults_file),
            output_dir=str(output_dir),
            clean=True,
        )

        assert not stale.exists()
        assert (output_dir / "test-agent.md").exists()

    def test_should_create_output_dir_if_missing(
        self,
        resolver: AgentConfigResolver,
        tmp_skills: Path,
        defaults_file: Path,
        tmp_path: Path,
    ) -> None:
        """Creates output directory if it doesn't exist."""
        new_dir = tmp_path / "new" / "output"
        assert not new_dir.exists()

        results = resolver.compose_all_to_dir(
            skills_dir=str(tmp_skills),
            defaults_path=str(defaults_file),
            output_dir=str(new_dir),
        )

        assert new_dir.exists()
        assert len([r for r in results if r.success]) == 2
