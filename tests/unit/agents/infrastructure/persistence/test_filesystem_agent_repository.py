# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for FilesystemAgentRepository."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from src.agents.domain.value_objects.body_format import BodyFormat
from src.agents.domain.value_objects.model_tier import ModelTier
from src.agents.domain.value_objects.tool_tier import ToolTier
from src.agents.infrastructure.persistence.filesystem_agent_repository import (
    FilesystemAgentRepository,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_MINIMAL_AGENT_YAML: dict[str, Any] = {
    "name": "test-agent",
    "version": "1.0.0",
    "description": "A test agent",
    "skill": "test-skill",
    "tool_tier": "T2",
    "identity": {
        "role": "Test Specialist",
        "expertise": ["testing", "verification"],
        "cognitive_mode": "systematic",
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
    "guardrails": {
        "input_validation": [{"field_format": "^test$"}],
        "output_filtering": ["no_secrets_in_output"],
        "fallback_behavior": "warn_and_retry",
    },
    "model": {
        "tier": "reasoning_standard",
        "preferences": [],
    },
    "tools": {
        "native": ["file_read", "file_write"],
        "mcp": [],
        "forbidden": [],
    },
    "portability": {
        "body_format": "xml",
    },
}


def _write_agent_pair(
    comp_dir: Path,
    agent_name: str,
    yaml_data: dict[str, Any] | None = None,
    prompt_content: str | None = None,
) -> None:
    """Write a .jerry.yaml + .jerry.prompt.md pair to comp_dir."""
    comp_dir.mkdir(parents=True, exist_ok=True)
    data = yaml_data if yaml_data is not None else dict(_MINIMAL_AGENT_YAML)
    data["name"] = agent_name

    yaml_path = comp_dir / f"{agent_name}.jerry.yaml"
    yaml_path.write_text(yaml.dump(data), encoding="utf-8")

    if prompt_content is not None:
        prompt_path = comp_dir / f"{agent_name}.jerry.prompt.md"
        prompt_path.write_text(prompt_content, encoding="utf-8")


# ---------------------------------------------------------------------------
# get()
# ---------------------------------------------------------------------------


class TestGet:
    """Tests for FilesystemAgentRepository.get()."""

    def test_get_found_returns_agent(self, tmp_path: Path) -> None:
        # Arrange
        comp_dir = tmp_path / "test-skill" / "composition"
        _write_agent_pair(comp_dir, "my-agent")
        repo = FilesystemAgentRepository(tmp_path)

        # Act
        agent = repo.get("my-agent")

        # Assert
        assert agent is not None
        assert agent.name == "my-agent"

    def test_get_not_found_returns_none(self, tmp_path: Path) -> None:
        # Arrange — skills dir exists but target agent does not
        (tmp_path / "some-skill" / "composition").mkdir(parents=True)
        repo = FilesystemAgentRepository(tmp_path)

        # Act
        agent = repo.get("nonexistent-agent")

        # Assert
        assert agent is None

    def test_get_searches_all_skill_dirs(self, tmp_path: Path) -> None:
        # Arrange — agent lives in second skill directory
        (tmp_path / "skill-a" / "composition").mkdir(parents=True)
        comp_dir = tmp_path / "skill-b" / "composition"
        _write_agent_pair(comp_dir, "target-agent")
        repo = FilesystemAgentRepository(tmp_path)

        # Act
        agent = repo.get("target-agent")

        # Assert
        assert agent is not None
        assert agent.name == "target-agent"

    def test_get_skips_dirs_without_composition_subdir(self, tmp_path: Path) -> None:
        # Arrange — skill directory has no composition/ subdirectory
        (tmp_path / "bare-skill").mkdir(parents=True)
        repo = FilesystemAgentRepository(tmp_path)

        # Act — must not raise
        agent = repo.get("any-agent")

        # Assert
        assert agent is None


# ---------------------------------------------------------------------------
# list_all()
# ---------------------------------------------------------------------------


class TestListAll:
    """Tests for FilesystemAgentRepository.list_all()."""

    def test_list_all_returns_all_agents_across_skills(self, tmp_path: Path) -> None:
        # Arrange — two skills, two agents each
        for skill in ("skill-a", "skill-b"):
            for i in range(2):
                comp_dir = tmp_path / skill / "composition"
                _write_agent_pair(comp_dir, f"{skill}-agent-{i}")
        repo = FilesystemAgentRepository(tmp_path)

        # Act
        agents = repo.list_all()

        # Assert
        assert len(agents) == 4

    def test_list_all_empty_skills_dir_returns_empty(self, tmp_path: Path) -> None:
        # Arrange — skills dir with no skill subdirectories
        repo = FilesystemAgentRepository(tmp_path)

        # Act
        agents = repo.list_all()

        # Assert
        assert agents == []

    def test_list_all_skips_failed_loads(self, tmp_path: Path) -> None:
        # Arrange — one valid agent, one broken YAML
        comp_dir = tmp_path / "skill" / "composition"
        comp_dir.mkdir(parents=True)
        _write_agent_pair(comp_dir, "good-agent")
        (comp_dir / "bad-agent.jerry.yaml").write_text(": invalid: yaml: [\n", encoding="utf-8")
        repo = FilesystemAgentRepository(tmp_path)

        # Act
        agents = repo.list_all()

        # Assert — only the valid agent loaded; broken one silently skipped
        assert len(agents) == 1
        assert agents[0].name == "good-agent"


# ---------------------------------------------------------------------------
# list_by_skill()
# ---------------------------------------------------------------------------


class TestListBySkill:
    """Tests for FilesystemAgentRepository.list_by_skill()."""

    def test_list_by_skill_returns_only_matching_agents(self, tmp_path: Path) -> None:
        # Arrange
        for skill in ("alpha", "beta"):
            comp_dir = tmp_path / skill / "composition"
            _write_agent_pair(comp_dir, f"{skill}-agent")
        repo = FilesystemAgentRepository(tmp_path)

        # Act
        agents = repo.list_by_skill("alpha")

        # Assert
        assert len(agents) == 1
        assert agents[0].name == "alpha-agent"

    def test_list_by_skill_nonexistent_skill_returns_empty(self, tmp_path: Path) -> None:
        # Arrange
        repo = FilesystemAgentRepository(tmp_path)

        # Act
        agents = repo.list_by_skill("ghost-skill")

        # Assert
        assert agents == []

    def test_list_by_skill_composition_dir_not_found_returns_empty(self, tmp_path: Path) -> None:
        # Arrange — skill dir exists but has no composition/ subdirectory
        (tmp_path / "bare-skill").mkdir(parents=True)
        repo = FilesystemAgentRepository(tmp_path)

        # Act
        agents = repo.list_by_skill("bare-skill")

        # Assert
        assert agents == []

    def test_list_by_skill_sorted_alphabetically(self, tmp_path: Path) -> None:
        # Arrange — create agents out of alphabetical order
        comp_dir = tmp_path / "my-skill" / "composition"
        for name in ("zzz-agent", "aaa-agent", "mmm-agent"):
            _write_agent_pair(comp_dir, name)
        repo = FilesystemAgentRepository(tmp_path)

        # Act
        agents = repo.list_by_skill("my-skill")

        # Assert — sorted by filename (glob("*.jerry.yaml") is sorted)
        names = [a.name for a in agents]
        assert names == sorted(names)


# ---------------------------------------------------------------------------
# _load_agent()
# ---------------------------------------------------------------------------


class TestLoadAgent:
    """Tests for FilesystemAgentRepository._load_agent()."""

    def test_load_agent_valid_pair_returns_agent(self, tmp_path: Path) -> None:
        # Arrange
        comp_dir = tmp_path / "skill" / "composition"
        _write_agent_pair(
            comp_dir,
            "load-agent",
            prompt_content="# load-agent System Prompt\n\n## Identity\n\nRole content.\n",
        )
        repo = FilesystemAgentRepository(tmp_path)
        yaml_path = comp_dir / "load-agent.jerry.yaml"

        # Act
        agent = repo._load_agent(yaml_path)

        # Assert
        assert agent is not None
        assert agent.name == "load-agent"

    def test_load_agent_strips_header_line_from_prompt(self, tmp_path: Path) -> None:
        # Arrange — prompt.md has a "# agent-name System Prompt" header
        comp_dir = tmp_path / "skill" / "composition"
        _write_agent_pair(
            comp_dir,
            "my-agent",
            prompt_content="# my-agent System Prompt\n\n## Identity\n\nRole.\n",
        )
        repo = FilesystemAgentRepository(tmp_path)
        yaml_path = comp_dir / "my-agent.jerry.yaml"

        # Act
        agent = repo._load_agent(yaml_path)

        # Assert — header line stripped; body starts from ## Identity
        assert agent is not None
        assert "# my-agent System Prompt" not in agent.prompt_body
        assert "Identity" in agent.prompt_body

    def test_load_agent_missing_prompt_uses_empty_body(self, tmp_path: Path) -> None:
        # Arrange — .jerry.yaml only, no .jerry.prompt.md
        comp_dir = tmp_path / "skill" / "composition"
        _write_agent_pair(comp_dir, "no-prompt-agent")
        # Do not write prompt.md
        repo = FilesystemAgentRepository(tmp_path)
        yaml_path = comp_dir / "no-prompt-agent.jerry.yaml"

        # Act
        agent = repo._load_agent(yaml_path)

        # Assert
        assert agent is not None
        assert agent.prompt_body == ""

    def test_load_agent_invalid_yaml_returns_none(self, tmp_path: Path) -> None:
        # Arrange — broken YAML content
        comp_dir = tmp_path / "skill" / "composition"
        comp_dir.mkdir(parents=True)
        bad_yaml = comp_dir / "bad-agent.jerry.yaml"
        bad_yaml.write_text(": broken: yaml: [unclosed\n", encoding="utf-8")
        repo = FilesystemAgentRepository(tmp_path)

        # Act
        result = repo._load_agent(bad_yaml)

        # Assert
        assert result is None

    def test_load_agent_non_dict_yaml_returns_none(self, tmp_path: Path) -> None:
        # Arrange — YAML that parses to a list, not a dict
        comp_dir = tmp_path / "skill" / "composition"
        comp_dir.mkdir(parents=True)
        list_yaml = comp_dir / "list-agent.jerry.yaml"
        list_yaml.write_text("- item1\n- item2\n", encoding="utf-8")
        repo = FilesystemAgentRepository(tmp_path)

        # Act
        result = repo._load_agent(list_yaml)

        # Assert
        assert result is None


# ---------------------------------------------------------------------------
# _parse_agent()
# ---------------------------------------------------------------------------


class TestParseAgent:
    """Tests for FilesystemAgentRepository._parse_agent()."""

    def test_parse_agent_uses_defaults_for_missing_optional_fields(self, tmp_path: Path) -> None:
        # Arrange — minimal required-only data
        repo = FilesystemAgentRepository(tmp_path)
        data: dict[str, Any] = {
            "name": "min-agent",
            "version": "1.0.0",
            "description": "Minimal",
            "skill": "min-skill",
            "identity": {
                "role": "Minimalist",
                "expertise": ["a", "b"],
                "cognitive_mode": "convergent",
            },
            "constitution": {},
            "guardrails": {},
        }

        # Act
        agent = repo._parse_agent(data, "")

        # Assert — optional fields default correctly
        assert agent.persona == {}
        assert agent.model_tier == ModelTier.REASONING_STANDARD
        assert agent.native_tools == []
        assert agent.mcp_servers == []
        assert agent.forbidden_tools == []
        assert agent.tool_tier == ToolTier.T1

    def test_parse_agent_reads_model_tier_from_dict(self, tmp_path: Path) -> None:
        # Arrange
        repo = FilesystemAgentRepository(tmp_path)
        data = dict(_MINIMAL_AGENT_YAML)
        data["model"] = {"tier": "reasoning_high", "preferences": ["claude-opus-4"]}

        # Act
        agent = repo._parse_agent(data, "")

        # Assert
        assert agent.model_tier == ModelTier.REASONING_HIGH
        assert agent.model_preferences == ["claude-opus-4"]

    def test_parse_agent_non_dict_model_uses_standard(self, tmp_path: Path) -> None:
        # Arrange — model is a bare string, not a dict
        repo = FilesystemAgentRepository(tmp_path)
        data = dict(_MINIMAL_AGENT_YAML)
        data["model"] = "sonnet"  # type: ignore[assignment]

        # Act
        agent = repo._parse_agent(data, "")

        # Assert
        assert agent.model_tier == ModelTier.REASONING_STANDARD

    def test_parse_agent_body_format_from_portability(self, tmp_path: Path) -> None:
        # Arrange
        repo = FilesystemAgentRepository(tmp_path)
        data = dict(_MINIMAL_AGENT_YAML)
        data["portability"] = {"body_format": "markdown"}

        # Act
        agent = repo._parse_agent(data, "prompt body")

        # Assert
        assert agent.body_format == BodyFormat.MARKDOWN

    def test_parse_agent_extra_yaml_collected(self, tmp_path: Path) -> None:
        # Arrange — include a field not in the known_keys set
        repo = FilesystemAgentRepository(tmp_path)
        data = dict(_MINIMAL_AGENT_YAML)
        data["custom_extension"] = {"key": "value"}

        # Act
        agent = repo._parse_agent(data, "")

        # Assert — extra field captured in extra_yaml
        assert "custom_extension" in agent.extra_yaml
        assert agent.extra_yaml["custom_extension"] == {"key": "value"}

    def test_parse_agent_known_keys_not_in_extra_yaml(self, tmp_path: Path) -> None:
        # Arrange
        repo = FilesystemAgentRepository(tmp_path)
        data = dict(_MINIMAL_AGENT_YAML)

        # Act
        agent = repo._parse_agent(data, "")

        # Assert — standard fields not duplicated in extra_yaml
        assert "name" not in agent.extra_yaml
        assert "version" not in agent.extra_yaml
        assert "tools" not in agent.extra_yaml

    def test_parse_agent_tools_from_dict_structure(self, tmp_path: Path) -> None:
        # Arrange
        repo = FilesystemAgentRepository(tmp_path)
        data = dict(_MINIMAL_AGENT_YAML)
        data["tools"] = {
            "native": ["file_read", "shell_execute"],
            "mcp": ["context7"],
            "forbidden": ["agent_delegate"],
        }

        # Act
        agent = repo._parse_agent(data, "")

        # Assert
        assert agent.native_tools == ["file_read", "shell_execute"]
        assert agent.mcp_servers == ["context7"]
        assert agent.forbidden_tools == ["agent_delegate"]

    def test_parse_agent_non_dict_tools_uses_empty_lists(self, tmp_path: Path) -> None:
        # Arrange — tools is a bare list, not the expected dict structure
        repo = FilesystemAgentRepository(tmp_path)
        data = dict(_MINIMAL_AGENT_YAML)
        data["tools"] = ["file_read"]  # type: ignore[assignment]

        # Act
        agent = repo._parse_agent(data, "")

        # Assert
        assert agent.native_tools == []
        assert agent.mcp_servers == []
        assert agent.forbidden_tools == []
