# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Shared fixtures for agents bounded context tests."""

from __future__ import annotations

from typing import Any

import pytest

from src.agents.domain.entities.canonical_agent import CanonicalAgent
from src.agents.domain.services.prompt_transformer import PromptTransformer
from src.agents.domain.services.tool_mapper import ToolMapper
from src.agents.domain.value_objects.body_format import BodyFormat
from src.agents.domain.value_objects.model_tier import ModelTier
from src.agents.domain.value_objects.tool_tier import ToolTier


@pytest.fixture()
def sample_tool_map() -> dict[str, dict[str, str | None]]:
    """Minimal tool map for testing."""
    return {
        "file_read": {"claude_code": "Read", "openai": "file_search", "ollama": None},
        "file_write": {"claude_code": "Write", "openai": None, "ollama": None},
        "file_edit": {"claude_code": "Edit", "openai": None, "ollama": None},
        "file_search_glob": {"claude_code": "Glob", "openai": None, "ollama": None},
        "file_search_content": {"claude_code": "Grep", "openai": "file_search", "ollama": None},
        "shell_execute": {"claude_code": "Bash", "openai": "code_interpreter", "ollama": None},
        "web_search": {"claude_code": "WebSearch", "openai": "web_search", "ollama": None},
        "web_fetch": {"claude_code": "WebFetch", "openai": None, "ollama": None},
        "agent_delegate": {"claude_code": "Task", "openai": None, "ollama": None},
    }


@pytest.fixture()
def sample_model_map() -> dict[str, dict[str, str | None]]:
    """Minimal model map for testing."""
    return {
        "reasoning_high": {"claude_code": "opus", "openai": "gpt-4o", "ollama": "llama3.1:70b"},
        "reasoning_standard": {
            "claude_code": "sonnet",
            "openai": "gpt-4o-mini",
            "ollama": "llama3.2",
        },
        "fast": {"claude_code": "haiku", "openai": "gpt-4o-mini", "ollama": "llama3.2:3b"},
    }


@pytest.fixture()
def tool_mapper(
    sample_tool_map: dict[str, dict[str, str | None]],
    sample_model_map: dict[str, dict[str, str | None]],
) -> ToolMapper:
    """Configured ToolMapper instance."""
    return ToolMapper(tool_map=sample_tool_map, model_map=sample_model_map)


@pytest.fixture()
def prompt_transformer() -> PromptTransformer:
    """PromptTransformer instance."""
    return PromptTransformer()


@pytest.fixture()
def sample_constitution() -> dict[str, Any]:
    """Constitution with required triplet."""
    return {
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


@pytest.fixture()
def sample_identity() -> dict[str, Any]:
    """Identity block with required fields."""
    return {
        "role": "Test Specialist",
        "expertise": ["unit testing", "integration testing"],
        "cognitive_mode": "systematic",
    }


@pytest.fixture()
def make_canonical_agent(
    sample_constitution: dict[str, Any],
    sample_identity: dict[str, Any],
) -> Any:
    """Factory fixture for creating CanonicalAgent instances."""

    def _make(
        name: str = "test-agent",
        skill: str = "test-skill",
        **overrides: Any,
    ) -> CanonicalAgent:
        defaults: dict[str, Any] = {
            "name": name,
            "version": "1.0.0",
            "description": "A test agent for unit testing",
            "skill": skill,
            "identity": sample_identity,
            "tool_tier": ToolTier.T2,
            "native_tools": ["file_read", "file_write", "file_edit"],
            "prompt_body": "## Identity\n\nTest agent.\n\n## Purpose\n\nFor testing.\n",
            "constitution": sample_constitution,
            "guardrails": {
                "input_validation": [{"field_format": "^test$"}],
                "output_filtering": ["no_secrets_in_output"],
                "fallback_behavior": "warn_and_retry",
            },
            "model_tier": ModelTier.REASONING_STANDARD,
            "body_format": BodyFormat.XML,
        }
        defaults.update(overrides)
        return CanonicalAgent(**defaults)

    return _make
