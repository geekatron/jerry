# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for CanonicalAgent entity and GeneratedArtifact entity.

Tests CanonicalAgent property accessors (has_mcp, has_delegation,
cognitive_mode, role, expertise) and GeneratedArtifact.filename across
all happy paths, negative/edge cases, and boundary values.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from src.agents.domain.entities.canonical_agent import CanonicalAgent
from src.agents.domain.entities.generated_artifact import GeneratedArtifact
from src.agents.domain.value_objects.body_format import BodyFormat
from src.agents.domain.value_objects.model_tier import ModelTier
from src.agents.domain.value_objects.tool_tier import ToolTier
from src.agents.domain.value_objects.vendor_target import VendorTarget

# =============================================================================
# Helpers / local factory
# =============================================================================


_DEFAULT_IDENTITY: dict[str, Any] = {
    "role": "Test Specialist",
    "expertise": ["unit testing", "integration testing"],
    "cognitive_mode": "systematic",
}

_SENTINEL = object()  # Sentinel distinguishes "not supplied" from an explicit empty dict.


def _make_agent(
    name: str = "test-agent",
    skill: str = "test-skill",
    identity: dict[str, Any] | object = _SENTINEL,
    native_tools: list[str] | None = None,
    mcp_servers: list[str] | None = None,
    **extra: Any,
) -> CanonicalAgent:
    """Construct a minimal valid CanonicalAgent for test use.

    Pass ``identity={}`` to get an explicitly empty identity dict;
    omit it to receive the default test identity.
    """
    constitution: dict[str, Any] = {
        "reference": "docs/governance/JERRY_CONSTITUTION.md",
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
    }
    guardrails: dict[str, Any] = {
        "input_validation": [{"field_format": "^test$"}],
        "output_filtering": ["no_secrets_in_output"],
        "fallback_behavior": "warn_and_retry",
    }
    resolved_identity: dict[str, Any] = (
        _DEFAULT_IDENTITY if identity is _SENTINEL else identity  # type: ignore[assignment]
    )
    return CanonicalAgent(
        name=name,
        version="1.0.0",
        description="Test agent",
        skill=skill,
        identity=resolved_identity,
        tool_tier=ToolTier.T2,
        native_tools=native_tools if native_tools is not None else ["file_read", "file_write"],
        prompt_body="## Identity\n\nTest.\n",
        constitution=constitution,
        guardrails=guardrails,
        mcp_servers=mcp_servers if mcp_servers is not None else [],
        model_tier=ModelTier.REASONING_STANDARD,
        body_format=BodyFormat.XML,
        **extra,
    )


# =============================================================================
# Tests: make_canonical_agent fixture integration
# =============================================================================


class TestCanonicalAgentConstruction:
    """Verify the factory fixture produces a valid CanonicalAgent."""

    @pytest.mark.happy_path
    def test_agent_created_from_fixture(self, make_canonical_agent: Any) -> None:
        """make_canonical_agent fixture returns a CanonicalAgent instance."""
        # Arrange / Act
        agent = make_canonical_agent()
        # Assert
        assert isinstance(agent, CanonicalAgent)

    @pytest.mark.happy_path
    def test_fixture_default_name(self, make_canonical_agent: Any) -> None:
        """Default agent name from fixture is 'test-agent'."""
        agent = make_canonical_agent()
        assert agent.name == "test-agent"

    @pytest.mark.happy_path
    def test_fixture_custom_name(self, make_canonical_agent: Any) -> None:
        """Custom name override is applied correctly."""
        agent = make_canonical_agent(name="my-agent")
        assert agent.name == "my-agent"

    @pytest.mark.happy_path
    def test_frozen_dataclass_immutable(self, make_canonical_agent: Any) -> None:
        """CanonicalAgent is frozen; direct attribute assignment raises FrozenInstanceError."""
        agent = make_canonical_agent()
        with pytest.raises(
            Exception
        ):  # dataclasses.FrozenInstanceError (subclass of AttributeError)
            agent.name = "mutated"  # type: ignore[misc]


# =============================================================================
# Tests: has_mcp property
# =============================================================================


class TestHasMcp:
    """CanonicalAgent.has_mcp property tests."""

    @pytest.mark.happy_path
    def test_no_mcp_servers_returns_false(self) -> None:
        """Agent with empty mcp_servers list returns False."""
        # Arrange
        agent = _make_agent(mcp_servers=[])
        # Act / Assert
        assert agent.has_mcp is False

    @pytest.mark.happy_path
    def test_single_mcp_server_returns_true(self) -> None:
        """Agent with one MCP server returns True."""
        agent = _make_agent(mcp_servers=["context7"])
        assert agent.has_mcp is True

    @pytest.mark.happy_path
    def test_multiple_mcp_servers_returns_true(self) -> None:
        """Agent with multiple MCP servers returns True."""
        agent = _make_agent(mcp_servers=["context7", "memory-keeper"])
        assert agent.has_mcp is True

    @pytest.mark.edge_case
    def test_default_mcp_servers_is_empty(self) -> None:
        """CanonicalAgent defaults mcp_servers to [] when not supplied."""
        agent = _make_agent()
        assert agent.has_mcp is False

    @pytest.mark.edge_case
    def test_fixture_default_no_mcp(self, make_canonical_agent: Any) -> None:
        """Default fixture agent has no MCP servers."""
        agent = make_canonical_agent()
        assert agent.has_mcp is False

    @pytest.mark.edge_case
    def test_fixture_with_mcp_servers(self, make_canonical_agent: Any) -> None:
        """Fixture agent with mcp_servers override has_mcp True."""
        agent = make_canonical_agent(mcp_servers=["memory-keeper"])
        assert agent.has_mcp is True


# =============================================================================
# Tests: has_delegation property
# =============================================================================


class TestHasDelegation:
    """CanonicalAgent.has_delegation property tests."""

    @pytest.mark.happy_path
    def test_no_delegate_tool_returns_false(self) -> None:
        """Agent without agent_delegate tool returns False."""
        # Arrange
        agent = _make_agent(native_tools=["file_read", "file_write"])
        # Act / Assert
        assert agent.has_delegation is False

    @pytest.mark.happy_path
    def test_agent_delegate_in_tools_returns_true(self) -> None:
        """Agent with agent_delegate in native_tools returns True."""
        agent = _make_agent(native_tools=["file_read", "agent_delegate"])
        assert agent.has_delegation is True

    @pytest.mark.happy_path
    def test_only_delegate_tool_returns_true(self) -> None:
        """Agent with only agent_delegate returns True."""
        agent = _make_agent(native_tools=["agent_delegate"])
        assert agent.has_delegation is True

    @pytest.mark.edge_case
    def test_empty_native_tools_returns_false(self) -> None:
        """Agent with empty tool list cannot delegate."""
        agent = _make_agent(native_tools=[])
        assert agent.has_delegation is False

    @pytest.mark.edge_case
    def test_partial_name_does_not_match(self) -> None:
        """Substring 'delegate' (without prefix) does not trigger delegation."""
        agent = _make_agent(native_tools=["delegate", "agent_delegat"])
        assert agent.has_delegation is False

    @pytest.mark.edge_case
    def test_fixture_default_no_delegation(self, make_canonical_agent: Any) -> None:
        """Default fixture agent does not include agent_delegate."""
        agent = make_canonical_agent()
        assert agent.has_delegation is False

    @pytest.mark.edge_case
    def test_fixture_with_delegate_tool(self, make_canonical_agent: Any) -> None:
        """Fixture agent with agent_delegate has delegation."""
        agent = make_canonical_agent(native_tools=["file_read", "agent_delegate"])
        assert agent.has_delegation is True


# =============================================================================
# Tests: cognitive_mode property
# =============================================================================


class TestCognitiveMode:
    """CanonicalAgent.cognitive_mode property tests."""

    @pytest.mark.happy_path
    def test_systematic_mode_returned(self) -> None:
        """Identity with cognitive_mode='systematic' is returned correctly."""
        # Arrange
        agent = _make_agent(
            identity={
                "role": "Auditor",
                "expertise": ["compliance"],
                "cognitive_mode": "systematic",
            }
        )
        # Act / Assert
        assert agent.cognitive_mode == "systematic"

    @pytest.mark.happy_path
    def test_convergent_mode_returned(self) -> None:
        """Identity with cognitive_mode='convergent' is returned."""
        agent = _make_agent(
            identity={
                "role": "Analyst",
                "expertise": ["analysis"],
                "cognitive_mode": "convergent",
            }
        )
        assert agent.cognitive_mode == "convergent"

    @pytest.mark.happy_path
    def test_divergent_mode_returned(self) -> None:
        """Identity with cognitive_mode='divergent' is returned."""
        agent = _make_agent(
            identity={
                "role": "Researcher",
                "expertise": ["research"],
                "cognitive_mode": "divergent",
            }
        )
        assert agent.cognitive_mode == "divergent"

    @pytest.mark.happy_path
    def test_integrative_mode_returned(self) -> None:
        """Identity with cognitive_mode='integrative' is returned."""
        agent = _make_agent(
            identity={
                "role": "Synthesizer",
                "expertise": ["synthesis"],
                "cognitive_mode": "integrative",
            }
        )
        assert agent.cognitive_mode == "integrative"

    @pytest.mark.happy_path
    def test_forensic_mode_returned(self) -> None:
        """Identity with cognitive_mode='forensic' is returned."""
        agent = _make_agent(
            identity={
                "role": "Investigator",
                "expertise": ["root cause"],
                "cognitive_mode": "forensic",
            }
        )
        assert agent.cognitive_mode == "forensic"

    @pytest.mark.edge_case
    def test_missing_cognitive_mode_defaults_to_convergent(self) -> None:
        """When cognitive_mode key is absent, the default 'convergent' is returned."""
        # Arrange: identity without cognitive_mode key
        agent = _make_agent(
            identity={
                "role": "Worker",
                "expertise": ["tasks"],
            }
        )
        # Act / Assert
        assert agent.cognitive_mode == "convergent"

    @pytest.mark.edge_case
    def test_empty_identity_defaults_to_convergent(self) -> None:
        """Empty identity dict falls back to default 'convergent'."""
        agent = _make_agent(identity={})
        assert agent.cognitive_mode == "convergent"


# =============================================================================
# Tests: role property
# =============================================================================


class TestRole:
    """CanonicalAgent.role property tests."""

    @pytest.mark.happy_path
    def test_role_extracted_from_identity(self) -> None:
        """Role string from identity block is returned directly."""
        # Arrange
        agent = _make_agent(
            identity={
                "role": "Security QA Engineer",
                "expertise": ["fuzzing"],
                "cognitive_mode": "systematic",
            }
        )
        # Act / Assert
        assert agent.role == "Security QA Engineer"

    @pytest.mark.happy_path
    def test_role_preserves_exact_string(self) -> None:
        """Role is returned verbatim without normalisation."""
        agent = _make_agent(
            identity={
                "role": "  Lead Architect  ",
                "expertise": ["architecture"],
                "cognitive_mode": "convergent",
            }
        )
        assert agent.role == "  Lead Architect  "

    @pytest.mark.edge_case
    def test_missing_role_returns_empty_string(self) -> None:
        """When 'role' key is absent from identity, empty string is returned."""
        agent = _make_agent(identity={"expertise": ["testing"], "cognitive_mode": "systematic"})
        assert agent.role == ""

    @pytest.mark.edge_case
    def test_empty_identity_returns_empty_string(self) -> None:
        """Empty identity dict returns empty string for role."""
        agent = _make_agent(identity={})
        assert agent.role == ""

    @pytest.mark.edge_case
    def test_empty_role_string_returned(self) -> None:
        """Explicitly empty role string is returned as-is."""
        agent = _make_agent(
            identity={
                "role": "",
                "expertise": ["nothing"],
                "cognitive_mode": "convergent",
            }
        )
        assert agent.role == ""


# =============================================================================
# Tests: expertise property
# =============================================================================


class TestExpertise:
    """CanonicalAgent.expertise property tests."""

    @pytest.mark.happy_path
    def test_expertise_list_extracted(self) -> None:
        """Expertise list from identity block is returned correctly."""
        # Arrange
        agent = _make_agent(
            identity={
                "role": "QA",
                "expertise": ["unit testing", "fuzzing", "property-based testing"],
                "cognitive_mode": "systematic",
            }
        )
        # Act / Assert
        assert agent.expertise == ["unit testing", "fuzzing", "property-based testing"]

    @pytest.mark.happy_path
    def test_single_expertise_item(self) -> None:
        """Single-item expertise list is returned as a list."""
        agent = _make_agent(
            identity={
                "role": "Specialist",
                "expertise": ["OWASP testing"],
                "cognitive_mode": "convergent",
            }
        )
        assert agent.expertise == ["OWASP testing"]

    @pytest.mark.edge_case
    def test_missing_expertise_returns_empty_list(self) -> None:
        """When 'expertise' key is absent, empty list is returned."""
        agent = _make_agent(identity={"role": "Worker", "cognitive_mode": "convergent"})
        assert agent.expertise == []

    @pytest.mark.edge_case
    def test_empty_expertise_list_returned(self) -> None:
        """Explicitly empty expertise list is returned as-is."""
        agent = _make_agent(
            identity={
                "role": "Nobody",
                "expertise": [],
                "cognitive_mode": "systematic",
            }
        )
        assert agent.expertise == []

    @pytest.mark.edge_case
    def test_empty_identity_returns_empty_list(self) -> None:
        """Empty identity dict returns empty list for expertise."""
        agent = _make_agent(identity={})
        assert agent.expertise == []

    @pytest.mark.happy_path
    def test_expertise_reflects_identity_from_fixture(self, sample_identity: Any) -> None:
        """expertise property matches the fixture sample_identity content."""
        # Arrange
        agent = _make_agent(identity=sample_identity)
        # Act / Assert
        assert agent.expertise == ["unit testing", "integration testing"]


# =============================================================================
# Tests: optional field defaults on CanonicalAgent
# =============================================================================


class TestOptionalFieldDefaults:
    """Verify mutable defaults (field_factory) are distinct per instance."""

    @pytest.mark.happy_path
    def test_default_model_tier(self) -> None:
        """Default model_tier is REASONING_STANDARD."""
        agent = _make_agent()
        assert agent.model_tier is ModelTier.REASONING_STANDARD

    @pytest.mark.happy_path
    def test_default_body_format(self) -> None:
        """Default body_format is XML."""
        agent = _make_agent()
        assert agent.body_format is BodyFormat.XML

    @pytest.mark.happy_path
    def test_default_persona_is_empty_dict(self) -> None:
        """persona defaults to empty dict."""
        agent = _make_agent()
        assert agent.persona == {}

    @pytest.mark.happy_path
    def test_default_mcp_servers_is_empty_list(self) -> None:
        """mcp_servers defaults to empty list."""
        agent = _make_agent()
        assert agent.mcp_servers == []

    @pytest.mark.happy_path
    def test_default_model_preferences_is_empty_list(self) -> None:
        """model_preferences defaults to empty list."""
        agent = _make_agent()
        assert agent.model_preferences == []

    @pytest.mark.happy_path
    def test_default_forbidden_tools_is_empty_list(self) -> None:
        """forbidden_tools defaults to empty list."""
        agent = _make_agent()
        assert agent.forbidden_tools == []

    @pytest.mark.edge_case
    def test_two_instances_have_independent_list_defaults(self) -> None:
        """Two agents created without mcp_servers do not share the same list object."""
        agent_a = _make_agent(name="agent-a")
        agent_b = _make_agent(name="agent-b")
        assert agent_a.mcp_servers is not agent_b.mcp_servers


# =============================================================================
# Tests: GeneratedArtifact.filename property
# =============================================================================


class TestGeneratedArtifact:
    """GeneratedArtifact entity tests — filename property and construction."""

    @pytest.mark.happy_path
    def test_filename_returns_path_name(self) -> None:
        """filename property returns only the file name portion of path."""
        # Arrange
        artifact = GeneratedArtifact(
            path=Path("skills/eng-team/agents/eng-qa.md"),
            content="---\nname: eng-qa\n---",
            vendor=VendorTarget.CLAUDE_CODE,
            source_agent="eng-qa",
            artifact_type="agent_definition",
        )
        # Act
        result = artifact.filename
        # Assert
        assert result == "eng-qa.md"

    @pytest.mark.happy_path
    def test_filename_deep_path(self) -> None:
        """filename ignores parent directories, returns only the leaf name."""
        artifact = GeneratedArtifact(
            path=Path("a/b/c/d/agent.governance.yaml"),
            content="version: 1.0.0",
            vendor=VendorTarget.CLAUDE_CODE,
            source_agent="some-agent",
            artifact_type="governance",
        )
        assert artifact.filename == "agent.governance.yaml"

    @pytest.mark.happy_path
    def test_filename_top_level_path(self) -> None:
        """filename works when path has no parent directory."""
        artifact = GeneratedArtifact(
            path=Path("agent.md"),
            content="content",
            vendor=VendorTarget.OPENAI,
            source_agent="flat-agent",
            artifact_type="agent_definition",
        )
        assert artifact.filename == "agent.md"

    @pytest.mark.happy_path
    def test_vendor_stored_correctly(self) -> None:
        """vendor attribute is stored and retrieved without modification."""
        artifact = GeneratedArtifact(
            path=Path("out/agent.md"),
            content="",
            vendor=VendorTarget.OLLAMA,
            source_agent="olly",
            artifact_type="agent_definition",
        )
        assert artifact.vendor is VendorTarget.OLLAMA

    @pytest.mark.happy_path
    def test_source_agent_stored_correctly(self) -> None:
        """source_agent attribute preserves the agent name string."""
        artifact = GeneratedArtifact(
            path=Path("out/eng-qa.md"),
            content="body",
            vendor=VendorTarget.CLAUDE_CODE,
            source_agent="eng-qa",
            artifact_type="agent_definition",
        )
        assert artifact.source_agent == "eng-qa"

    @pytest.mark.edge_case
    def test_frozen_artifact_immutable(self) -> None:
        """GeneratedArtifact is frozen; direct attribute assignment raises FrozenInstanceError."""
        artifact = GeneratedArtifact(
            path=Path("out/agent.md"),
            content="c",
            vendor=VendorTarget.CLAUDE_CODE,
            source_agent="x",
            artifact_type="agent_definition",
        )
        with pytest.raises(Exception):  # dataclasses.FrozenInstanceError
            artifact.content = "mutated"  # type: ignore[misc]

    @pytest.mark.edge_case
    def test_filename_with_dotfile(self) -> None:
        """Hidden files (dot-prefix) return full filename including leading dot."""
        artifact = GeneratedArtifact(
            path=Path("skills/.hidden-agent.md"),
            content="",
            vendor=VendorTarget.CLAUDE_CODE,
            source_agent="hidden",
            artifact_type="agent_definition",
        )
        assert artifact.filename == ".hidden-agent.md"

    @pytest.mark.edge_case
    def test_filename_no_extension(self) -> None:
        """Filename with no extension is returned as-is."""
        artifact = GeneratedArtifact(
            path=Path("output/agentfile"),
            content="raw",
            vendor=VendorTarget.GOOGLE_ADK,
            source_agent="bare",
            artifact_type="agent_definition",
        )
        assert artifact.filename == "agentfile"

    @pytest.mark.edge_case
    def test_empty_content_allowed(self) -> None:
        """Empty content string is a valid artifact."""
        artifact = GeneratedArtifact(
            path=Path("out/empty.md"),
            content="",
            vendor=VendorTarget.CLAUDE_CODE,
            source_agent="empty-agent",
            artifact_type="agent_definition",
        )
        assert artifact.content == ""
        assert artifact.filename == "empty.md"

    @pytest.mark.happy_path
    def test_governance_artifact_type(self) -> None:
        """artifact_type='governance' is stored without modification."""
        artifact = GeneratedArtifact(
            path=Path("skills/eng-team/agents/eng-qa.governance.yaml"),
            content="version: 1.0.0",
            vendor=VendorTarget.CLAUDE_CODE,
            source_agent="eng-qa",
            artifact_type="governance",
        )
        assert artifact.artifact_type == "governance"
        assert artifact.filename == "eng-qa.governance.yaml"
