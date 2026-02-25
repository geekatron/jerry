# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for Agent Configuration Query Handlers.

Tests handler delegation to AgentConfigResolver.
No resolver internals are tested -- only that handlers
correctly delegate and transform results.

References:
    - PROJ-012: Agent Configuration Extraction & Schema Enforcement
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from src.application.handlers.queries.agent_config_query_handlers import (
    ListAgentConfigsQueryHandler,
    ShowAgentConfigQueryHandler,
    ValidateAgentConfigQueryHandler,
)
from src.application.queries.agent_config_queries import (
    ListAgentConfigsQuery,
    ShowAgentConfigQuery,
    ValidateAgentConfigQuery,
)
from src.infrastructure.adapters.configuration.agent_config_resolver import (
    AgentConfigResolver,
    AgentInfo,
    ValidationResult,
)

# === Fixtures ===


@pytest.fixture()
def mock_resolver() -> MagicMock:
    """Create a MagicMock of AgentConfigResolver."""
    return MagicMock(spec=AgentConfigResolver)


@pytest.fixture()
def sample_agent_info() -> AgentInfo:
    """Create a sample AgentInfo for test assertions."""
    return AgentInfo(
        name="ps-researcher",
        skill="problem-solving",
        file_path="/skills/problem-solving/agents/ps-researcher.md",
        model="opus",
        cognitive_mode="divergent",
        version="1.0.0",
    )


@pytest.fixture()
def sample_validation_result_valid() -> ValidationResult:
    """Create a passing ValidationResult."""
    return ValidationResult(
        agent_name="ps-researcher",
        file_path="/skills/problem-solving/agents/ps-researcher.md",
        is_valid=True,
        errors=[],
    )


@pytest.fixture()
def sample_validation_result_invalid() -> ValidationResult:
    """Create a failing ValidationResult."""
    return ValidationResult(
        agent_name="ps-researcher",
        file_path="/skills/problem-solving/agents/ps-researcher.md",
        is_valid=False,
        errors=["name: 'name' is a required property"],
    )


# === ValidateAgentConfigQueryHandler Tests ===


class TestValidateAgentConfigQueryHandlerHappyPath:
    """Happy path tests for ValidateAgentConfigQueryHandler."""

    def test_should_construct_with_resolver(self, mock_resolver: MagicMock) -> None:
        """Handler accepts an AgentConfigResolver at construction."""
        handler = ValidateAgentConfigQueryHandler(resolver=mock_resolver)
        assert handler._resolver is mock_resolver

    def test_should_delegate_validate_all_when_no_agent_name(
        self,
        mock_resolver: MagicMock,
        sample_validation_result_valid: ValidationResult,
    ) -> None:
        """Handler delegates to resolver.validate_all when agent_name is None."""
        mock_resolver.validate_all.return_value = [sample_validation_result_valid]

        handler = ValidateAgentConfigQueryHandler(resolver=mock_resolver)
        query = ValidateAgentConfigQuery(
            skills_dir="/skills",
            schema_path="/schema.json",
            defaults_path="/defaults.yaml",
            agent_name=None,
        )

        result = handler.handle(query)

        mock_resolver.validate_all.assert_called_once_with(
            "/skills", "/schema.json", "/defaults.yaml"
        )
        assert result == [sample_validation_result_valid]

    def test_should_delegate_validate_single_when_agent_name_given(
        self,
        mock_resolver: MagicMock,
        sample_validation_result_valid: ValidationResult,
    ) -> None:
        """Handler delegates to resolver.validate_single when agent_name specified."""
        mock_resolver.validate_single.return_value = [sample_validation_result_valid]

        handler = ValidateAgentConfigQueryHandler(resolver=mock_resolver)
        query = ValidateAgentConfigQuery(
            skills_dir="/skills",
            schema_path="/schema.json",
            defaults_path="/defaults.yaml",
            agent_name="ps-researcher",
        )

        result = handler.handle(query)

        mock_resolver.validate_single.assert_called_once_with(
            "/skills", "ps-researcher", "/schema.json", "/defaults.yaml"
        )
        assert len(result) == 1
        assert result[0] is sample_validation_result_valid

    def test_should_return_multiple_results_for_validate_all(
        self, mock_resolver: MagicMock
    ) -> None:
        """Handler returns all ValidationResults from validate_all."""
        results = [
            ValidationResult(
                agent_name="ps-researcher",
                file_path="/skills/problem-solving/agents/ps-researcher.md",
                is_valid=True,
                errors=[],
            ),
            ValidationResult(
                agent_name="ps-analyst",
                file_path="/skills/problem-solving/agents/ps-analyst.md",
                is_valid=False,
                errors=["missing field: name"],
            ),
        ]
        mock_resolver.validate_all.return_value = results

        handler = ValidateAgentConfigQueryHandler(resolver=mock_resolver)
        query = ValidateAgentConfigQuery(
            skills_dir="/skills",
            schema_path="/schema.json",
            defaults_path="/defaults.yaml",
        )

        result = handler.handle(query)

        assert len(result) == 2
        assert result[0].is_valid is True
        assert result[1].is_valid is False


class TestValidateAgentConfigQueryHandlerNegative:
    """Negative tests for ValidateAgentConfigQueryHandler."""

    def test_should_return_not_found_result_when_agent_missing(
        self, mock_resolver: MagicMock
    ) -> None:
        """Handler returns a not-found ValidationResult when agent file is missing."""
        not_found_result = ValidationResult(
            agent_name="nonexistent-agent",
            file_path="(not found)",
            is_valid=False,
            errors=["Agent 'nonexistent-agent' not found"],
        )
        mock_resolver.validate_single.return_value = [not_found_result]

        handler = ValidateAgentConfigQueryHandler(resolver=mock_resolver)
        query = ValidateAgentConfigQuery(
            skills_dir="/skills",
            schema_path="/schema.json",
            defaults_path="/defaults.yaml",
            agent_name="nonexistent-agent",
        )

        result = handler.handle(query)

        assert len(result) == 1
        assert result[0].is_valid is False
        assert result[0].agent_name == "nonexistent-agent"
        assert result[0].file_path == "(not found)"


# === ListAgentConfigsQueryHandler Tests ===


class TestListAgentConfigsQueryHandlerHappyPath:
    """Happy path tests for ListAgentConfigsQueryHandler."""

    def test_should_construct_with_resolver(self, mock_resolver: MagicMock) -> None:
        """Handler accepts an AgentConfigResolver at construction."""
        handler = ListAgentConfigsQueryHandler(resolver=mock_resolver)
        assert handler._resolver is mock_resolver

    def test_should_delegate_discover_agents(
        self, mock_resolver: MagicMock, sample_agent_info: AgentInfo
    ) -> None:
        """Handler delegates discovery to resolver.discover_agents."""
        mock_resolver.discover_agents.return_value = [sample_agent_info]

        handler = ListAgentConfigsQueryHandler(resolver=mock_resolver)
        query = ListAgentConfigsQuery(skills_dir="/skills")

        result = handler.handle(query)

        mock_resolver.discover_agents.assert_called_once_with("/skills")
        assert result == [sample_agent_info]

    def test_should_filter_agents_by_skill(self, mock_resolver: MagicMock) -> None:
        """Handler filters agents by skill_filter when specified."""
        agents = [
            AgentInfo(
                name="ps-researcher",
                skill="problem-solving",
                file_path="/skills/problem-solving/agents/ps-researcher.md",
                model="opus",
                cognitive_mode="divergent",
                version="1.0.0",
            ),
            AgentInfo(
                name="adv-scorer",
                skill="adversary",
                file_path="/skills/adversary/agents/adv-scorer.md",
                model="sonnet",
                cognitive_mode="convergent",
                version="1.0.0",
            ),
        ]
        mock_resolver.discover_agents.return_value = agents

        handler = ListAgentConfigsQueryHandler(resolver=mock_resolver)
        query = ListAgentConfigsQuery(skills_dir="/skills", skill_filter="problem-solving")

        result = handler.handle(query)

        assert len(result) == 1
        assert result[0].name == "ps-researcher"
        assert result[0].skill == "problem-solving"

    def test_should_return_all_agents_when_no_filter(self, mock_resolver: MagicMock) -> None:
        """Handler returns all agents when skill_filter is None."""
        agents = [
            AgentInfo(
                name="ps-researcher",
                skill="problem-solving",
                file_path="/a.md",
                model="opus",
                cognitive_mode="divergent",
                version="1.0.0",
            ),
            AgentInfo(
                name="adv-scorer",
                skill="adversary",
                file_path="/b.md",
                model="sonnet",
                cognitive_mode="convergent",
                version="1.0.0",
            ),
        ]
        mock_resolver.discover_agents.return_value = agents

        handler = ListAgentConfigsQueryHandler(resolver=mock_resolver)
        query = ListAgentConfigsQuery(skills_dir="/skills", skill_filter=None)

        result = handler.handle(query)

        assert len(result) == 2


class TestListAgentConfigsQueryHandlerNegative:
    """Negative tests for ListAgentConfigsQueryHandler."""

    def test_should_return_empty_list_when_no_agents_discovered(
        self, mock_resolver: MagicMock
    ) -> None:
        """Handler returns empty list when resolver discovers no agents."""
        mock_resolver.discover_agents.return_value = []

        handler = ListAgentConfigsQueryHandler(resolver=mock_resolver)
        query = ListAgentConfigsQuery(skills_dir="/empty-skills")

        result = handler.handle(query)

        assert result == []

    def test_should_return_empty_list_when_filter_matches_nothing(
        self, mock_resolver: MagicMock, sample_agent_info: AgentInfo
    ) -> None:
        """Handler returns empty list when skill_filter matches no agents."""
        mock_resolver.discover_agents.return_value = [sample_agent_info]

        handler = ListAgentConfigsQueryHandler(resolver=mock_resolver)
        query = ListAgentConfigsQuery(skills_dir="/skills", skill_filter="nonexistent-skill")

        result = handler.handle(query)

        assert result == []


# === ShowAgentConfigQueryHandler Tests ===


class TestShowAgentConfigQueryHandlerHappyPath:
    """Happy path tests for ShowAgentConfigQueryHandler."""

    def test_should_construct_with_resolver(self, mock_resolver: MagicMock) -> None:
        """Handler accepts an AgentConfigResolver at construction."""
        handler = ShowAgentConfigQueryHandler(resolver=mock_resolver)
        assert handler._resolver is mock_resolver

    def test_should_delegate_compose_agent_config_for_composed_show(
        self, mock_resolver: MagicMock
    ) -> None:
        """Handler delegates to compose_agent_config when raw=False."""
        agent_file = Path("/skills/problem-solving/agents/ps-researcher.md")
        composed_config = {
            "name": "ps-researcher",
            "model": "opus",
            "version": "1.0.0",
        }
        mock_resolver.find_agent_file.return_value = agent_file
        mock_resolver.load_defaults.return_value = {"model": "sonnet"}
        mock_resolver.compose_agent_config.return_value = composed_config

        handler = ShowAgentConfigQueryHandler(resolver=mock_resolver)
        query = ShowAgentConfigQuery(
            agent_name="ps-researcher",
            skills_dir="/skills",
            defaults_path="/defaults.yaml",
            raw=False,
        )

        result = handler.handle(query)

        mock_resolver.find_agent_file.assert_called_once_with("/skills", "ps-researcher")
        mock_resolver.load_defaults.assert_called_once_with("/defaults.yaml")
        mock_resolver.compose_agent_config.assert_called_once_with(agent_file, {"model": "sonnet"})
        assert result == composed_config

    def test_should_delegate_extract_frontmatter_for_raw_show(
        self, mock_resolver: MagicMock
    ) -> None:
        """Handler delegates to _extract_frontmatter when raw=True."""
        agent_file = Path("/skills/problem-solving/agents/ps-researcher.md")
        raw_frontmatter = {"name": "ps-researcher", "model": "opus"}
        mock_resolver.find_agent_file.return_value = agent_file
        mock_resolver._extract_frontmatter.return_value = raw_frontmatter

        handler = ShowAgentConfigQueryHandler(resolver=mock_resolver)
        query = ShowAgentConfigQuery(
            agent_name="ps-researcher",
            skills_dir="/skills",
            defaults_path="/defaults.yaml",
            raw=True,
        )

        result = handler.handle(query)

        mock_resolver._extract_frontmatter.assert_called_once_with(agent_file)
        mock_resolver.compose_agent_config.assert_not_called()
        assert result == raw_frontmatter

    def test_should_pass_loaded_defaults_to_compose(self, mock_resolver: MagicMock) -> None:
        """Handler loads defaults via load_defaults and passes them to compose."""
        agent_file = Path("/skills/problem-solving/agents/ps-researcher.md")
        mock_resolver.find_agent_file.return_value = agent_file
        mock_resolver.load_defaults.return_value = {"model": "haiku"}
        mock_resolver.compose_agent_config.return_value = {"name": "ps-researcher"}

        handler = ShowAgentConfigQueryHandler(resolver=mock_resolver)
        query = ShowAgentConfigQuery(
            agent_name="ps-researcher",
            skills_dir="/skills",
            defaults_path="/custom/defaults.yaml",
            raw=False,
        )

        result = handler.handle(query)

        mock_resolver.load_defaults.assert_called_once_with("/custom/defaults.yaml")
        mock_resolver.compose_agent_config.assert_called_once_with(agent_file, {"model": "haiku"})
        assert result == {"name": "ps-researcher"}


class TestShowAgentConfigQueryHandlerNegative:
    """Negative tests for ShowAgentConfigQueryHandler."""

    def test_should_return_error_when_agent_not_found(self, mock_resolver: MagicMock) -> None:
        """Handler returns error dict when agent file is not found."""
        mock_resolver.find_agent_file.return_value = None

        handler = ShowAgentConfigQueryHandler(resolver=mock_resolver)
        query = ShowAgentConfigQuery(
            agent_name="nonexistent-agent",
            skills_dir="/skills",
            defaults_path="/defaults.yaml",
        )

        result = handler.handle(query)

        assert "error" in result
        assert "nonexistent-agent" in result["error"]
        mock_resolver.compose_agent_config.assert_not_called()

    def test_should_return_error_when_raw_has_no_frontmatter(
        self, mock_resolver: MagicMock
    ) -> None:
        """Handler returns error dict when raw mode finds no frontmatter."""
        agent_file = Path("/skills/problem-solving/agents/ps-researcher.md")
        mock_resolver.find_agent_file.return_value = agent_file
        mock_resolver._extract_frontmatter.return_value = None

        handler = ShowAgentConfigQueryHandler(resolver=mock_resolver)
        query = ShowAgentConfigQuery(
            agent_name="ps-researcher",
            skills_dir="/skills",
            defaults_path="/defaults.yaml",
            raw=True,
        )

        result = handler.handle(query)

        assert "error" in result
        assert "frontmatter" in result["error"].lower() or "No YAML" in result["error"]
