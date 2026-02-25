# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Integration tests: validate ALL 58 agent definitions against the JSON Schema.

Uses the real AgentConfigResolver to discover, compose (with defaults), and
validate every agent file under skills/*/agents/*.md.  This is the key
verification that Phase 1+2+3 of PROJ-012 produced schema-compliant agents.

References:
    - PROJ-012: Agent Configuration Extraction & Schema Enforcement
    - H-34: Agent definition YAML frontmatter MUST validate against JSON Schema
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator

from src.infrastructure.adapters.configuration.agent_config_resolver import (
    AgentConfigResolver,
    AgentInfo,
    ValidationResult,
)

# Mark entire module as integration tests
pytestmark = [pytest.mark.integration]


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def repo_root() -> Path:
    """Locate the repository root by finding pyproject.toml."""
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "pyproject.toml").exists():
            return parent
    msg = "Could not find repository root (no pyproject.toml in parent directories)"
    raise FileNotFoundError(msg)


@pytest.fixture
def skills_dir(repo_root: Path) -> str:
    """Return the absolute path to the skills/ directory."""
    path = repo_root / "skills"
    assert path.is_dir(), f"skills directory not found: {path}"
    return str(path)


@pytest.fixture
def schema_path(repo_root: Path) -> str:
    """Return the absolute path to the agent definition JSON Schema."""
    path = repo_root / "docs" / "schemas" / "jerry-claude-agent-definition-v1.schema.json"
    assert path.is_file(), f"schema file not found: {path}"
    return str(path)


@pytest.fixture
def defaults_path(repo_root: Path) -> str:
    """Return the absolute path to the agent defaults YAML."""
    path = repo_root / "docs" / "schemas" / "jerry-claude-agent-defaults.yaml"
    assert path.is_file(), f"defaults file not found: {path}"
    return str(path)


@pytest.fixture
def resolver() -> AgentConfigResolver:
    """Create an AgentConfigResolver without config variable substitution."""
    return AgentConfigResolver(config=None)


@pytest.fixture
def defaults(defaults_path: str) -> dict:
    """Load the base defaults YAML."""
    with open(defaults_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert isinstance(data, dict), "defaults file must contain a YAML mapping"
    return data


@pytest.fixture
def schema_validator(schema_path: str) -> Draft202012Validator:
    """Create a JSON Schema Draft 2020-12 validator."""
    with open(schema_path, encoding="utf-8") as f:
        schema = json.load(f)
    return Draft202012Validator(schema)


# =============================================================================
# Tests
# =============================================================================


class TestAllAgentsValidateAgainstSchema:
    """Validate every agent definition against the canonical JSON Schema."""

    def test_all_agents_validate_against_schema(
        self,
        resolver: AgentConfigResolver,
        skills_dir: str,
        schema_path: str,
        defaults_path: str,
    ) -> None:
        """Discover all agents, compose each with defaults, validate against schema.

        This is the primary PROJ-012 acceptance test: all 58 agents MUST
        pass schema validation when composed with base defaults.
        """
        results: list[ValidationResult] = resolver.validate_all(
            skills_dir=skills_dir,
            schema_path=schema_path,
            defaults_path=defaults_path,
        )

        # Collect failures for a clear error report
        failures: list[str] = []
        for r in results:
            if not r.is_valid:
                error_detail = r.yaml_error or "; ".join(r.errors)
                failures.append(f"  {r.agent_name} ({r.file_path}): {error_detail}")

        assert len(failures) == 0, (
            f"{len(failures)} agent(s) failed schema validation:\n" + "\n".join(failures)
        )

        # Sanity check: we actually validated a meaningful number of agents
        assert len(results) >= 58, (
            f"Expected at least 58 agents, but only discovered {len(results)}. "
            "Agent files may have been removed or the discovery pattern changed."
        )

    def test_all_agents_have_required_base_fields(
        self,
        resolver: AgentConfigResolver,
        skills_dir: str,
        defaults: dict,
        schema_validator: Draft202012Validator,
    ) -> None:
        """All composed agents have the required base fields.

        After merging with defaults, every agent MUST contain at minimum:
        name, version, description, model, identity, capabilities, guardrails.
        """
        required_fields = [
            "name",
            "version",
            "description",
            "model",
            "identity",
            "capabilities",
            "guardrails",
        ]

        agents: list[AgentInfo] = resolver.discover_agents(skills_dir)
        assert len(agents) >= 58, f"Expected at least 58 agents, discovered {len(agents)}"

        missing_report: list[str] = []
        for agent in agents:
            agent_file = Path(agent.file_path)
            composed = resolver.compose_agent_config(agent_file, defaults)

            missing = [f for f in required_fields if f not in composed]
            if missing:
                missing_report.append(f"  {agent.name}: missing {missing}")

        assert len(missing_report) == 0, (
            f"{len(missing_report)} agent(s) missing required fields:\n" + "\n".join(missing_report)
        )
