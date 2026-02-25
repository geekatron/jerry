# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for AgentConfigResolver.

Tests verify:
- Agent discovery: finds agents in skills/*/agents/ structure
- Deep merge: scalar override, deep object merge, array replacement
- Config variable substitution: ${jerry.*} token replacement
- Frontmatter extraction: YAML parsing from markdown frontmatter
- Full composition pipeline: defaults + agent frontmatter + config vars
- Schema validation: validates composed config against JSON Schema
- Validate all: batch validation of discovered agents
- Agent file lookup: find agent by name

References:
    - PROJ-012: Agent Configuration Extraction & Schema Enforcement
    - H-05: Uses uv run for all Python execution
    - H-20: BDD test-first, 90% line coverage
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest
import yaml
from jsonschema import Draft202012Validator

from src.infrastructure.adapters.configuration.agent_config_resolver import (
    AgentConfigResolver,
    AgentInfo,
    ValidationResult,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

MINIMAL_FRONTMATTER: dict[str, Any] = {
    "name": "test-agent",
    "version": "1.0.0",
    "description": "A test agent for unit testing.",
    "model": "sonnet",
    "identity": {
        "role": "Test Agent",
        "expertise": ["unit testing", "fixtures"],
        "cognitive_mode": "systematic",
    },
    "capabilities": {
        "allowed_tools": ["Read", "Grep"],
        "forbidden_actions": [
            "Spawn recursive subagents (P-003)",
            "Override user decisions (P-020)",
            "Misrepresent capabilities or confidence (P-022)",
        ],
    },
    "guardrails": {
        "input_validation": [{"field_format": "^.*$"}],
        "output_filtering": [
            "no_secrets_in_output",
            "no_executable_code_without_confirmation",
            "all_claims_must_have_citations",
        ],
        "fallback_behavior": "warn_and_retry",
    },
}


BASE_DEFAULTS: dict[str, Any] = {
    "permissionMode": "default",
    "background": False,
    "version": "1.0.0",
    "persona": {
        "tone": "professional",
        "communication_style": "consultative",
        "audience_level": "adaptive",
    },
    "capabilities": {
        "forbidden_actions": [
            "Spawn recursive subagents (P-003)",
            "Override user decisions (P-020)",
            "Misrepresent capabilities or confidence (P-022)",
        ],
    },
    "guardrails": {
        "output_filtering": [
            "no_secrets_in_output",
            "no_executable_code_without_confirmation",
            "all_claims_must_have_citations",
        ],
        "fallback_behavior": "warn_and_retry",
    },
    "output": {
        "required": False,
        "levels": ["L0", "L1", "L2"],
    },
    "constitution": {
        "reference": "docs/governance/JERRY_CONSTITUTION.md",
        "principles_applied": [
            "P-002: File Persistence (Medium)",
            "P-003: No Recursive Subagents (Hard)",
            "P-020: User Authority (Hard)",
            "P-022: No Deception (Hard)",
        ],
    },
    "enforcement": {
        "tier": "medium",
    },
}


MINIMAL_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "required": [
        "name",
        "version",
        "description",
        "model",
        "identity",
        "capabilities",
        "guardrails",
    ],
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^[a-z]+-[a-z]+(-[a-z]+)*$",
        },
        "version": {
            "type": "string",
            "pattern": r"^\d+\.\d+\.\d+$",
        },
        "description": {
            "type": "string",
            "maxLength": 1024,
        },
        "model": {
            "type": "string",
            "enum": ["opus", "sonnet", "haiku"],
        },
        "identity": {
            "type": "object",
            "required": ["role", "expertise", "cognitive_mode"],
            "properties": {
                "role": {"type": "string", "minLength": 1},
                "expertise": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 2,
                },
                "cognitive_mode": {
                    "type": "string",
                    "enum": [
                        "divergent",
                        "convergent",
                        "integrative",
                        "systematic",
                        "forensic",
                        "strategic",
                        "mixed",
                        "divergent-then-convergent",
                    ],
                },
            },
        },
        "capabilities": {
            "type": "object",
            "required": ["allowed_tools", "forbidden_actions"],
            "properties": {
                "allowed_tools": {"type": "array", "items": {"type": "string"}},
                "forbidden_actions": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 3,
                },
            },
        },
        "guardrails": {
            "type": "object",
            "required": ["input_validation", "output_filtering", "fallback_behavior"],
            "properties": {
                "input_validation": {
                    "oneOf": [
                        {"type": "array", "minItems": 1},
                        {"type": "object", "minProperties": 1},
                    ]
                },
                "output_filtering": {"type": "array", "minItems": 1},
                "fallback_behavior": {
                    "type": "string",
                    "pattern": "^[a-z][a-z0-9_-]*$",
                },
            },
        },
    },
    "additionalProperties": True,
}


def _write_agent_md(path: Path, frontmatter: dict[str, Any]) -> None:
    """Helper to write an agent markdown file with YAML frontmatter."""
    yaml_str = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
    path.write_text(f"---\n{yaml_str}---\n\n# Agent Body\n", encoding="utf-8")


def _make_mock_config(mapping: dict[str, str] | None = None) -> MagicMock:
    """Create a mock LayeredConfigAdapter with a get() method.

    Args:
        mapping: Dictionary of config keys to values. Defaults to empty.

    Returns:
        MagicMock mimicking LayeredConfigAdapter.
    """
    mapping = mapping or {}
    mock = MagicMock()
    mock.get.side_effect = lambda key: mapping.get(key)
    return mock


def _create_skills_structure(
    tmp_path: Path,
    agents: dict[str, dict[str, Any]],
) -> Path:
    """Create a skills directory with agent files.

    Args:
        tmp_path: Temporary directory.
        agents: Mapping of "skill/agent_name" to frontmatter dict.

    Returns:
        Path to the skills directory.
    """
    skills_dir = tmp_path / "skills"
    for agent_key, frontmatter in agents.items():
        skill_name, agent_name = agent_key.split("/")
        agent_dir = skills_dir / skill_name / "agents"
        agent_dir.mkdir(parents=True, exist_ok=True)
        agent_file = agent_dir / f"{agent_name}.md"
        _write_agent_md(agent_file, frontmatter)
    return skills_dir


# ---------------------------------------------------------------------------
# Tests: discover_agents()
# ---------------------------------------------------------------------------


class TestDiscoverAgents:
    """Tests for agent discovery in skills directory structure."""

    def test_should_discover_agents_in_skills_subdirectories(self, tmp_path: Path) -> None:
        """Given a skills directory with agent files, discover_agents returns AgentInfo list."""
        fm = {**MINIMAL_FRONTMATTER, "name": "ps-researcher"}
        skills_dir = _create_skills_structure(tmp_path, {"problem-solving/ps-researcher": fm})

        resolver = AgentConfigResolver()
        agents = resolver.discover_agents(str(skills_dir))

        assert len(agents) == 1
        assert agents[0].name == "ps-researcher"
        assert agents[0].skill == "problem-solving"
        assert agents[0].model == "sonnet"
        assert agents[0].cognitive_mode == "systematic"
        assert agents[0].version == "1.0.0"

    def test_should_return_empty_list_when_skills_dir_missing(self, tmp_path: Path) -> None:
        """Given a nonexistent skills directory, discover_agents returns empty list."""
        resolver = AgentConfigResolver()
        agents = resolver.discover_agents(str(tmp_path / "nonexistent"))

        assert agents == []

    def test_should_skip_readme_and_agents_md(self, tmp_path: Path) -> None:
        """Given README.md and AGENTS.md in agents dir, they are excluded."""
        fm = {**MINIMAL_FRONTMATTER, "name": "ps-analyst"}
        skills_dir = _create_skills_structure(tmp_path, {"problem-solving/ps-analyst": fm})
        # Add files that should be skipped
        agents_dir = skills_dir / "problem-solving" / "agents"
        _write_agent_md(agents_dir / "README.md", MINIMAL_FRONTMATTER)
        _write_agent_md(agents_dir / "AGENTS.md", MINIMAL_FRONTMATTER)

        resolver = AgentConfigResolver()
        agents = resolver.discover_agents(str(skills_dir))

        assert len(agents) == 1
        assert agents[0].name == "ps-analyst"

    def test_should_skip_template_and_extension_files(self, tmp_path: Path) -> None:
        """Given TEMPLATE or EXTENSION files, they are excluded."""
        fm = {**MINIMAL_FRONTMATTER, "name": "ps-critic"}
        skills_dir = _create_skills_structure(tmp_path, {"problem-solving/ps-critic": fm})
        agents_dir = skills_dir / "problem-solving" / "agents"
        _write_agent_md(agents_dir / "TEMPLATE-base.md", MINIMAL_FRONTMATTER)
        _write_agent_md(agents_dir / "EXTENSION-tools.md", MINIMAL_FRONTMATTER)

        resolver = AgentConfigResolver()
        agents = resolver.discover_agents(str(skills_dir))

        assert len(agents) == 1
        assert agents[0].name == "ps-critic"

    def test_should_skip_files_without_valid_frontmatter(self, tmp_path: Path) -> None:
        """Given a .md file without YAML frontmatter, it is excluded."""
        skills_dir = tmp_path / "skills" / "my-skill" / "agents"
        skills_dir.mkdir(parents=True)
        (skills_dir / "broken-agent.md").write_text(
            "# No frontmatter here\nJust markdown.", encoding="utf-8"
        )

        resolver = AgentConfigResolver()
        agents = resolver.discover_agents(str(tmp_path / "skills"))

        assert agents == []

    def test_should_discover_multiple_agents_across_skills(self, tmp_path: Path) -> None:
        """Given multiple skills, all agents are discovered and sorted."""
        fm_a = {**MINIMAL_FRONTMATTER, "name": "adv-scorer", "model": "opus"}
        fm_b = {**MINIMAL_FRONTMATTER, "name": "ps-researcher", "model": "sonnet"}
        skills_dir = _create_skills_structure(
            tmp_path,
            {
                "adversary/adv-scorer": fm_a,
                "problem-solving/ps-researcher": fm_b,
            },
        )

        resolver = AgentConfigResolver()
        agents = resolver.discover_agents(str(skills_dir))

        assert len(agents) == 2
        # Sorted by file path -- adversary comes before problem-solving
        assert agents[0].name == "adv-scorer"
        assert agents[1].name == "ps-researcher"

    def test_should_use_stem_as_name_when_frontmatter_has_no_name(self, tmp_path: Path) -> None:
        """Given frontmatter without a name field, the file stem is used."""
        fm = {
            "version": "1.0.0",
            "model": "haiku",
            "identity": {
                "role": "Worker",
                "expertise": ["a", "b"],
                "cognitive_mode": "convergent",
            },
            "capabilities": {
                "allowed_tools": [],
                "forbidden_actions": ["P-003", "P-020", "P-022"],
            },
            "guardrails": {
                "input_validation": [{"x": "y"}],
                "output_filtering": ["a"],
                "fallback_behavior": "warn_and_retry",
            },
        }
        skills_dir = _create_skills_structure(tmp_path, {"my-skill/fallback-name": fm})

        resolver = AgentConfigResolver()
        agents = resolver.discover_agents(str(skills_dir))

        assert len(agents) == 1
        assert agents[0].name == "fallback-name"


# ---------------------------------------------------------------------------
# Tests: _deep_merge()
# ---------------------------------------------------------------------------


class TestDeepMerge:
    """Tests for deep merge behavior: scalar override, deep objects, array replace."""

    def test_should_override_scalar_values(self) -> None:
        """Given overlapping scalar keys, the override value wins."""
        resolver = AgentConfigResolver()
        base = {"key": "base_value", "other": 42}
        override = {"key": "override_value"}

        result = resolver._deep_merge(base, override)

        assert result["key"] == "override_value"
        assert result["other"] == 42

    def test_should_deep_merge_nested_dicts(self) -> None:
        """Given nested dicts, keys are merged recursively."""
        resolver = AgentConfigResolver()
        base = {"persona": {"tone": "professional", "style": "consultative"}}
        override = {"persona": {"tone": "technical"}}

        result = resolver._deep_merge(base, override)

        assert result["persona"]["tone"] == "technical"
        assert result["persona"]["style"] == "consultative"

    def test_should_replace_arrays_entirely(self) -> None:
        """Given array values, the override array replaces the base array."""
        resolver = AgentConfigResolver()
        base = {"tools": ["Read", "Write", "Grep"]}
        override = {"tools": ["Bash"]}

        result = resolver._deep_merge(base, override)

        assert result["tools"] == ["Bash"]

    def test_should_add_new_keys_from_override(self) -> None:
        """Given a key only in override, it is added to the result."""
        resolver = AgentConfigResolver()
        base = {"existing": "value"}
        override = {"new_key": "new_value"}

        result = resolver._deep_merge(base, override)

        assert result["existing"] == "value"
        assert result["new_key"] == "new_value"

    def test_should_handle_deeply_nested_merge(self) -> None:
        """Given three levels of nesting, all levels merge correctly."""
        resolver = AgentConfigResolver()
        base = {"a": {"b": {"c": 1, "d": 2}}}
        override = {"a": {"b": {"c": 99}}}

        result = resolver._deep_merge(base, override)

        assert result["a"]["b"]["c"] == 99
        assert result["a"]["b"]["d"] == 2

    def test_should_handle_override_replacing_dict_with_scalar(self) -> None:
        """Given a dict in base and scalar in override, the scalar wins."""
        resolver = AgentConfigResolver()
        base = {"key": {"nested": "value"}}
        override = {"key": "flat_value"}

        result = resolver._deep_merge(base, override)

        assert result["key"] == "flat_value"

    def test_should_handle_empty_dicts(self) -> None:
        """Given empty dicts, merge works without error."""
        resolver = AgentConfigResolver()
        assert resolver._deep_merge({}, {}) == {}
        assert resolver._deep_merge({"a": 1}, {}) == {"a": 1}
        assert resolver._deep_merge({}, {"a": 1}) == {"a": 1}


# ---------------------------------------------------------------------------
# Tests: _substitute_config_vars()
# ---------------------------------------------------------------------------


class TestSubstituteConfigVars:
    """Tests for ${jerry.*} config variable substitution."""

    def test_should_replace_jerry_token_with_config_value(self) -> None:
        """Given a string with ${jerry.foo}, it is replaced with the config value."""
        mock_config = _make_mock_config({"jerry.agents.default_model": "opus"})
        resolver = AgentConfigResolver(config=mock_config)

        result = resolver._substitute_config_vars({"model": "${jerry.agents.default_model}"})

        assert result["model"] == "opus"

    def test_should_leave_unresolved_tokens_as_is(self) -> None:
        """Given a token with no config match, it remains unchanged."""
        mock_config = _make_mock_config({})
        resolver = AgentConfigResolver(config=mock_config)

        result = resolver._substitute_config_vars({"model": "${jerry.missing.key}"})

        assert result["model"] == "${jerry.missing.key}"

    def test_should_substitute_in_nested_dicts(self) -> None:
        """Given nested dicts with tokens, all are substituted."""
        mock_config = _make_mock_config({"jerry.persona.tone": "technical"})
        resolver = AgentConfigResolver(config=mock_config)

        result = resolver._substitute_config_vars({"persona": {"tone": "${jerry.persona.tone}"}})

        assert result["persona"]["tone"] == "technical"

    def test_should_substitute_in_arrays(self) -> None:
        """Given an array with tokens, each element is substituted."""
        mock_config = _make_mock_config({"jerry.tool.primary": "Read"})
        resolver = AgentConfigResolver(config=mock_config)

        result = resolver._substitute_config_vars({"tools": ["${jerry.tool.primary}", "Write"]})

        assert result["tools"] == ["Read", "Write"]

    def test_should_not_modify_non_string_values(self) -> None:
        """Given non-string values (int, bool, None), they pass through unchanged."""
        mock_config = _make_mock_config({})
        resolver = AgentConfigResolver(config=mock_config)

        result = resolver._substitute_config_vars({"count": 42, "enabled": True, "nothing": None})

        assert result["count"] == 42
        assert result["enabled"] is True
        assert result["nothing"] is None

    def test_should_skip_substitution_when_config_is_none(self) -> None:
        """Given no config adapter, ${jerry.*} tokens remain unchanged."""
        resolver = AgentConfigResolver(config=None)

        result = resolver._substitute_config_vars({"model": "${jerry.agents.default_model}"})

        assert result["model"] == "${jerry.agents.default_model}"

    def test_should_handle_multiple_tokens_in_one_string(self) -> None:
        """Given a string with multiple tokens, all are substituted."""
        mock_config = _make_mock_config(
            {"jerry.project.name": "proj-012", "jerry.project.version": "v1"}
        )
        resolver = AgentConfigResolver(config=mock_config)

        result = resolver._substitute_config_vars(
            {"label": "${jerry.project.name}-${jerry.project.version}"}
        )

        assert result["label"] == "proj-012-v1"


# ---------------------------------------------------------------------------
# Tests: _extract_frontmatter()
# ---------------------------------------------------------------------------


class TestExtractFrontmatter:
    """Tests for YAML frontmatter extraction from markdown files."""

    def test_should_extract_valid_yaml_frontmatter(self, tmp_path: Path) -> None:
        """Given a file with valid YAML frontmatter, a dict is returned."""
        agent_file = tmp_path / "agent.md"
        _write_agent_md(agent_file, {"name": "test-agent", "model": "opus"})

        resolver = AgentConfigResolver()
        result = resolver._extract_frontmatter(agent_file)

        assert result is not None
        assert result["name"] == "test-agent"
        assert result["model"] == "opus"

    def test_should_return_none_when_no_frontmatter(self, tmp_path: Path) -> None:
        """Given a file without --- delimiters, None is returned."""
        agent_file = tmp_path / "agent.md"
        agent_file.write_text("# Just Markdown\nNo frontmatter.", encoding="utf-8")

        resolver = AgentConfigResolver()
        result = resolver._extract_frontmatter(agent_file)

        assert result is None

    def test_should_return_none_when_frontmatter_not_closed(self, tmp_path: Path) -> None:
        """Given a file with opening --- but no closing ---, None is returned."""
        agent_file = tmp_path / "agent.md"
        agent_file.write_text("---\nname: broken\n# No closing delimiter", encoding="utf-8")

        resolver = AgentConfigResolver()
        result = resolver._extract_frontmatter(agent_file)

        assert result is None

    def test_should_return_none_when_yaml_is_invalid(self, tmp_path: Path) -> None:
        """Given malformed YAML between --- delimiters, None is returned."""
        agent_file = tmp_path / "agent.md"
        agent_file.write_text("---\n: : : bad yaml [[\n---\n", encoding="utf-8")

        resolver = AgentConfigResolver()
        result = resolver._extract_frontmatter(agent_file)

        assert result is None

    def test_should_return_none_when_yaml_is_not_a_dict(self, tmp_path: Path) -> None:
        """Given YAML that parses to a non-dict (e.g., a list), None is returned."""
        agent_file = tmp_path / "agent.md"
        agent_file.write_text("---\n- item1\n- item2\n---\n", encoding="utf-8")

        resolver = AgentConfigResolver()
        result = resolver._extract_frontmatter(agent_file)

        assert result is None

    def test_should_return_none_when_file_does_not_exist(self, tmp_path: Path) -> None:
        """Given a nonexistent file path, None is returned."""
        resolver = AgentConfigResolver()
        result = resolver._extract_frontmatter(tmp_path / "nonexistent.md")

        assert result is None


# ---------------------------------------------------------------------------
# Tests: compose_agent_config()
# ---------------------------------------------------------------------------


class TestComposeAgentConfig:
    """Tests for full composition pipeline: defaults + frontmatter + config vars."""

    def test_should_merge_defaults_with_frontmatter(self, tmp_path: Path) -> None:
        """Given defaults and frontmatter, the composed config merges both."""
        agent_file = tmp_path / "agent.md"
        _write_agent_md(agent_file, MINIMAL_FRONTMATTER)

        resolver = AgentConfigResolver()
        result = resolver.compose_agent_config(agent_file, BASE_DEFAULTS)

        # Frontmatter value overrides default
        assert result["name"] == "test-agent"
        assert result["model"] == "sonnet"
        # Default value inherited where frontmatter has no override
        assert result["permissionMode"] == "default"
        assert result["background"] is False
        assert result["output"]["required"] is False

    def test_should_deep_merge_nested_persona(self, tmp_path: Path) -> None:
        """Given persona in both defaults and frontmatter, they deep merge."""
        fm = {
            **MINIMAL_FRONTMATTER,
            "persona": {"tone": "technical"},
        }
        agent_file = tmp_path / "agent.md"
        _write_agent_md(agent_file, fm)

        resolver = AgentConfigResolver()
        result = resolver.compose_agent_config(agent_file, BASE_DEFAULTS)

        assert result["persona"]["tone"] == "technical"
        assert result["persona"]["communication_style"] == "consultative"

    def test_should_substitute_config_vars_when_config_provided(self, tmp_path: Path) -> None:
        """Given a config adapter, ${jerry.*} tokens are substituted."""
        fm = {**MINIMAL_FRONTMATTER, "description": "Agent for ${jerry.project.name}"}
        agent_file = tmp_path / "agent.md"
        _write_agent_md(agent_file, fm)

        mock_config = _make_mock_config({"jerry.project.name": "PROJ-012"})
        resolver = AgentConfigResolver(config=mock_config)
        result = resolver.compose_agent_config(agent_file, BASE_DEFAULTS)

        assert result["description"] == "Agent for PROJ-012"

    def test_should_skip_config_var_substitution_when_no_config(self, tmp_path: Path) -> None:
        """Given no config adapter, tokens remain in the composed config."""
        fm = {**MINIMAL_FRONTMATTER, "description": "Agent for ${jerry.project.name}"}
        agent_file = tmp_path / "agent.md"
        _write_agent_md(agent_file, fm)

        resolver = AgentConfigResolver(config=None)
        result = resolver.compose_agent_config(agent_file, BASE_DEFAULTS)

        assert result["description"] == "Agent for ${jerry.project.name}"

    def test_should_raise_value_error_when_no_frontmatter(self, tmp_path: Path) -> None:
        """Given a file without frontmatter, ValueError is raised."""
        agent_file = tmp_path / "agent.md"
        agent_file.write_text("# No frontmatter", encoding="utf-8")

        resolver = AgentConfigResolver()

        with pytest.raises(ValueError, match="No valid YAML frontmatter"):
            resolver.compose_agent_config(agent_file, BASE_DEFAULTS)

    def test_should_not_mutate_original_defaults(self, tmp_path: Path) -> None:
        """Given defaults passed to compose, the original dict is not mutated."""
        import copy

        defaults_copy = copy.deepcopy(BASE_DEFAULTS)
        agent_file = tmp_path / "agent.md"
        _write_agent_md(agent_file, MINIMAL_FRONTMATTER)

        resolver = AgentConfigResolver()
        resolver.compose_agent_config(agent_file, BASE_DEFAULTS)

        assert BASE_DEFAULTS == defaults_copy


# ---------------------------------------------------------------------------
# Tests: validate_agent()
# ---------------------------------------------------------------------------


class TestValidateAgent:
    """Tests for single agent validation against JSON Schema."""

    def test_should_return_valid_result_for_conforming_agent(self, tmp_path: Path) -> None:
        """Given a valid agent config, validation passes with no errors."""
        agent_file = tmp_path / "test-agent.md"
        _write_agent_md(agent_file, MINIMAL_FRONTMATTER)
        validator = Draft202012Validator(MINIMAL_SCHEMA)

        resolver = AgentConfigResolver()
        result = resolver.validate_agent(agent_file, BASE_DEFAULTS, validator)

        assert result.is_valid is True
        assert result.errors == []
        assert result.agent_name == "test-agent"
        assert result.yaml_error is None

    def test_should_return_errors_for_invalid_agent(self, tmp_path: Path) -> None:
        """Given a config missing required fields, validation fails with errors."""
        # Missing 'model' and 'capabilities' -- will fail schema
        bad_fm = {"name": "bad-agent", "version": "1.0.0"}
        agent_file = tmp_path / "bad-agent.md"
        _write_agent_md(agent_file, bad_fm)
        validator = Draft202012Validator(MINIMAL_SCHEMA)

        resolver = AgentConfigResolver()
        result = resolver.validate_agent(agent_file, {}, validator)

        assert result.is_valid is False
        assert len(result.errors) > 0

    def test_should_return_yaml_error_when_no_frontmatter(self, tmp_path: Path) -> None:
        """Given a file without frontmatter, result has yaml_error."""
        agent_file = tmp_path / "no-fm.md"
        agent_file.write_text("# No frontmatter", encoding="utf-8")
        validator = Draft202012Validator(MINIMAL_SCHEMA)

        resolver = AgentConfigResolver()
        result = resolver.validate_agent(agent_file, BASE_DEFAULTS, validator)

        assert result.is_valid is False
        assert result.yaml_error == "No valid YAML frontmatter found"
        assert result.agent_name == "no-fm"

    def test_should_use_composed_name_in_result(self, tmp_path: Path) -> None:
        """Given frontmatter with name, the ValidationResult uses that name."""
        fm = {**MINIMAL_FRONTMATTER, "name": "adv-scorer"}
        agent_file = tmp_path / "adv-scorer.md"
        _write_agent_md(agent_file, fm)
        validator = Draft202012Validator(MINIMAL_SCHEMA)

        resolver = AgentConfigResolver()
        result = resolver.validate_agent(agent_file, BASE_DEFAULTS, validator)

        assert result.agent_name == "adv-scorer"


# ---------------------------------------------------------------------------
# Tests: validate_all()
# ---------------------------------------------------------------------------


class TestValidateAll:
    """Tests for batch validation of all discovered agents."""

    def test_should_validate_all_agents_in_skills_dir(self, tmp_path: Path) -> None:
        """Given multiple agent files, validate_all returns results for each."""
        fm_a = {**MINIMAL_FRONTMATTER, "name": "adv-executor"}
        fm_b = {**MINIMAL_FRONTMATTER, "name": "ps-analyst"}
        skills_dir = _create_skills_structure(
            tmp_path,
            {
                "adversary/adv-executor": fm_a,
                "problem-solving/ps-analyst": fm_b,
            },
        )

        schema_path = tmp_path / "schema.json"
        schema_path.write_text(json.dumps(MINIMAL_SCHEMA), encoding="utf-8")
        defaults_path = tmp_path / "defaults.yaml"
        defaults_path.write_text(
            yaml.dump(BASE_DEFAULTS, default_flow_style=False), encoding="utf-8"
        )

        resolver = AgentConfigResolver()
        results = resolver.validate_all(str(skills_dir), str(schema_path), str(defaults_path))

        assert len(results) == 2
        assert all(r.is_valid for r in results)

    def test_should_skip_files_without_frontmatter(self, tmp_path: Path) -> None:
        """Given a mix of valid and non-frontmatter files, only valid ones are validated."""
        fm = {**MINIMAL_FRONTMATTER, "name": "ps-critic"}
        skills_dir = _create_skills_structure(tmp_path, {"problem-solving/ps-critic": fm})
        # Add a file without frontmatter
        no_fm_file = skills_dir / "problem-solving" / "agents" / "broken.md"
        no_fm_file.write_text("# No frontmatter", encoding="utf-8")

        schema_path = tmp_path / "schema.json"
        schema_path.write_text(json.dumps(MINIMAL_SCHEMA), encoding="utf-8")
        defaults_path = tmp_path / "defaults.yaml"
        defaults_path.write_text(
            yaml.dump(BASE_DEFAULTS, default_flow_style=False), encoding="utf-8"
        )

        resolver = AgentConfigResolver()
        results = resolver.validate_all(str(skills_dir), str(schema_path), str(defaults_path))

        # Only ps-critic should be validated (broken.md has no frontmatter)
        assert len(results) == 1
        assert results[0].agent_name == "ps-critic"

    def test_should_return_empty_list_for_empty_skills_dir(self, tmp_path: Path) -> None:
        """Given an empty skills directory, validate_all returns empty list."""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        schema_path = tmp_path / "schema.json"
        schema_path.write_text(json.dumps(MINIMAL_SCHEMA), encoding="utf-8")
        defaults_path = tmp_path / "defaults.yaml"
        defaults_path.write_text("{}", encoding="utf-8")

        resolver = AgentConfigResolver()
        results = resolver.validate_all(str(skills_dir), str(schema_path), str(defaults_path))

        assert results == []


# ---------------------------------------------------------------------------
# Tests: find_agent_file()
# ---------------------------------------------------------------------------


class TestFindAgentFile:
    """Tests for finding agent files by name."""

    def test_should_find_agent_file_by_stem_name(self, tmp_path: Path) -> None:
        """Given an agent name matching a file stem, the path is returned."""
        fm = {**MINIMAL_FRONTMATTER, "name": "ps-researcher"}
        skills_dir = _create_skills_structure(tmp_path, {"problem-solving/ps-researcher": fm})

        resolver = AgentConfigResolver()
        result = resolver.find_agent_file(str(skills_dir), "ps-researcher")

        assert result is not None
        assert result.name == "ps-researcher.md"

    def test_should_return_none_when_agent_not_found(self, tmp_path: Path) -> None:
        """Given an agent name that does not exist, None is returned."""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        resolver = AgentConfigResolver()
        result = resolver.find_agent_file(str(skills_dir), "nonexistent-agent")

        assert result is None

    def test_should_find_agent_across_multiple_skills(self, tmp_path: Path) -> None:
        """Given agents in different skills, the correct one is found."""
        fm_a = {**MINIMAL_FRONTMATTER, "name": "adv-scorer"}
        fm_b = {**MINIMAL_FRONTMATTER, "name": "ps-researcher"}
        skills_dir = _create_skills_structure(
            tmp_path,
            {
                "adversary/adv-scorer": fm_a,
                "problem-solving/ps-researcher": fm_b,
            },
        )

        resolver = AgentConfigResolver()
        result = resolver.find_agent_file(str(skills_dir), "adv-scorer")

        assert result is not None
        assert result.name == "adv-scorer.md"
        assert "adversary" in str(result)


# ---------------------------------------------------------------------------
# Tests: Edge cases and integration
# ---------------------------------------------------------------------------


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_should_handle_empty_frontmatter_dict(self, tmp_path: Path) -> None:
        """Given frontmatter that parses to an empty dict, it is treated as valid but empty."""
        agent_file = tmp_path / "empty-fm.md"
        # Write file with empty YAML frontmatter (parses to None with safe_load,
        # but yaml.dump({}) produces '{}\n')
        agent_file.write_text("---\n{}\n---\n# Body\n", encoding="utf-8")

        resolver = AgentConfigResolver()
        result = resolver._extract_frontmatter(agent_file)

        assert result == {}

    def test_should_handle_defaults_yaml_load_failure_gracefully(self, tmp_path: Path) -> None:
        """Given a corrupt defaults YAML, _load_yaml returns empty dict."""
        bad_yaml = tmp_path / "bad.yaml"
        bad_yaml.write_text(": : : bad yaml\n", encoding="utf-8")

        result = AgentConfigResolver._load_yaml(str(bad_yaml))

        assert result == {}

    def test_should_handle_nonexistent_defaults_yaml_gracefully(self) -> None:
        """Given a nonexistent defaults path, _load_yaml returns empty dict."""
        result = AgentConfigResolver._load_yaml("/nonexistent/path.yaml")

        assert result == {}

    def test_should_load_valid_json_schema(self, tmp_path: Path) -> None:
        """Given a valid JSON schema file, _load_json returns parsed dict."""
        schema_file = tmp_path / "schema.json"
        schema_file.write_text(json.dumps(MINIMAL_SCHEMA), encoding="utf-8")

        result = AgentConfigResolver._load_json(str(schema_file))

        assert result["type"] == "object"
        assert "name" in result["required"]

    def test_should_produce_validation_result_dataclass_correctly(self) -> None:
        """Given ValidationResult construction, all fields are accessible."""
        result = ValidationResult(
            agent_name="test-agent",
            file_path="/path/to/agent.md",
            is_valid=False,
            errors=["missing field: model"],
            yaml_error=None,
        )

        assert result.agent_name == "test-agent"
        assert result.file_path == "/path/to/agent.md"
        assert result.is_valid is False
        assert result.errors == ["missing field: model"]
        assert result.yaml_error is None

    def test_should_produce_agent_info_dataclass_correctly(self) -> None:
        """Given AgentInfo construction, all fields are accessible and it is frozen."""
        info = AgentInfo(
            name="ps-researcher",
            skill="problem-solving",
            file_path="/skills/problem-solving/agents/ps-researcher.md",
            model="opus",
            cognitive_mode="divergent",
            version="2.1.0",
        )

        assert info.name == "ps-researcher"
        assert info.skill == "problem-solving"
        assert info.model == "opus"
        assert info.cognitive_mode == "divergent"
        assert info.version == "2.1.0"

        # AgentInfo is frozen
        with pytest.raises(AttributeError):
            info.name = "changed"  # type: ignore[misc]
