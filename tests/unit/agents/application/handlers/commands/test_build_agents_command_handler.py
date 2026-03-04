# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for BuildAgentsCommandHandler."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest

from src.agents.application.commands.build_agents_command import BuildAgentsCommand
from src.agents.application.handlers.commands.build_agents_command_handler import (
    BuildAgentsCommandHandler,
)
from src.agents.domain.entities.generated_artifact import GeneratedArtifact
from src.agents.domain.value_objects.vendor_target import VendorTarget

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_artifact(
    name: str, path: Path, artifact_type: str = "agent_definition"
) -> GeneratedArtifact:
    """Create a minimal GeneratedArtifact for test use."""
    return GeneratedArtifact(
        path=path / f"{name}.md",
        content=f"content for {name}",
        vendor=VendorTarget.CLAUDE_CODE,
        source_agent=name,
        artifact_type=artifact_type,
    )


def _make_handler(
    agents: list[Any],
    adapter_generate_return: list[GeneratedArtifact] | None = None,
    adapter_name: str = "claude_code",
) -> tuple[BuildAgentsCommandHandler, MagicMock, MagicMock]:
    """Build handler with mocked repository and adapter."""
    mock_repo = MagicMock()
    mock_adapter = MagicMock()

    if agents:
        mock_repo.get.return_value = agents[0]
    else:
        mock_repo.get.return_value = None
    mock_repo.list_all.return_value = agents

    if adapter_generate_return is not None:
        mock_adapter.generate.return_value = adapter_generate_return
    else:
        mock_adapter.generate.return_value = []

    handler = BuildAgentsCommandHandler(
        repository=mock_repo,
        adapters={adapter_name: mock_adapter},
    )
    return handler, mock_repo, mock_adapter


# ---------------------------------------------------------------------------
# handle() — unknown adapter
# ---------------------------------------------------------------------------


class TestHandleUnknownAdapter:
    """Tests for BuildAgentsCommandHandler.handle() with unknown adapter."""

    def test_raises_value_error_for_unknown_adapter(self) -> None:
        # Arrange
        handler, _, _ = _make_handler([])
        command = BuildAgentsCommand(vendor="openai")

        # Act / Assert
        with pytest.raises(ValueError, match="Unknown vendor: 'openai'"):
            handler.handle(command)

    def test_error_message_lists_available_adapters(self) -> None:
        # Arrange
        mock_repo = MagicMock()
        mock_adapter = MagicMock()
        handler = BuildAgentsCommandHandler(
            repository=mock_repo,
            adapters={"claude_code": mock_adapter, "ollama": mock_adapter},
        )
        command = BuildAgentsCommand(vendor="unknown")

        # Act / Assert
        with pytest.raises(ValueError, match="claude_code"):
            handler.handle(command)


# ---------------------------------------------------------------------------
# handle() — agent not found
# ---------------------------------------------------------------------------


class TestHandleAgentNotFound:
    """Tests for BuildAgentsCommandHandler.handle() when a named agent is missing."""

    def test_returns_result_with_failed_count_when_agent_not_found(self) -> None:
        # Arrange — repo returns None for any get()
        mock_repo = MagicMock()
        mock_repo.get.return_value = None
        mock_adapter = MagicMock()
        handler = BuildAgentsCommandHandler(
            repository=mock_repo,
            adapters={"claude_code": mock_adapter},
        )
        command = BuildAgentsCommand(vendor="claude_code", agent_name="ghost-agent")

        # Act
        result = handler.handle(command)

        # Assert
        assert result.failed == 1
        assert result.built == 0
        assert any("ghost-agent" in e for e in result.errors)

    def test_no_artifacts_generated_when_agent_not_found(self) -> None:
        # Arrange
        mock_repo = MagicMock()
        mock_repo.get.return_value = None
        mock_adapter = MagicMock()
        handler = BuildAgentsCommandHandler(
            repository=mock_repo,
            adapters={"claude_code": mock_adapter},
        )
        command = BuildAgentsCommand(vendor="claude_code", agent_name="missing")

        # Act
        result = handler.handle(command)

        # Assert
        assert result.artifacts == []
        mock_adapter.generate.assert_not_called()


# ---------------------------------------------------------------------------
# handle() — successful build (single agent)
# ---------------------------------------------------------------------------


class TestHandleSuccessfulBuildSingleAgent:
    """Tests for BuildAgentsCommandHandler.handle() with a single agent build."""

    def test_builds_single_agent_by_name(self, make_canonical_agent: Any, tmp_path: Path) -> None:
        # Arrange
        agent = make_canonical_agent(name="ps-analyst", skill="problem-solving")
        artifacts = [
            _make_artifact("ps-analyst", tmp_path),
            _make_artifact("ps-analyst", tmp_path, "governance"),
        ]
        handler, mock_repo, _ = _make_handler([agent], adapter_generate_return=artifacts)
        command = BuildAgentsCommand(vendor="claude_code", agent_name="ps-analyst")

        # Act
        result = handler.handle(command)

        # Assert
        assert result.built == 1
        assert result.failed == 0
        assert len(result.artifacts) == 2
        mock_repo.get.assert_called_once_with("ps-analyst")

    def test_files_written_on_non_dry_run(self, make_canonical_agent: Any, tmp_path: Path) -> None:
        # Arrange — write artifacts to tmp_path/agents/
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        agent = make_canonical_agent(name="my-agent", skill="my-skill")
        artifact_path = agents_dir / "my-agent.md"
        artifacts = [
            GeneratedArtifact(
                path=artifact_path,
                content="---\nname: my-agent\n---\nbody\n",
                vendor=VendorTarget.CLAUDE_CODE,
                source_agent="my-agent",
                artifact_type="agent_definition",
            )
        ]
        mock_repo = MagicMock()
        mock_repo.get.return_value = agent
        mock_adapter = MagicMock()
        mock_adapter.generate.return_value = artifacts
        handler = BuildAgentsCommandHandler(
            repository=mock_repo,
            adapters={"claude_code": mock_adapter},
        )
        command = BuildAgentsCommand(vendor="claude_code", agent_name="my-agent", dry_run=False)

        # Act
        handler.handle(command)

        # Assert — file was written to disk
        assert artifact_path.exists()
        assert "my-agent" in artifact_path.read_text()


# ---------------------------------------------------------------------------
# handle() — successful build (all agents)
# ---------------------------------------------------------------------------


class TestHandleSuccessfulBuildAllAgents:
    """Tests for BuildAgentsCommandHandler.handle() building all agents."""

    def test_builds_all_agents_when_no_name_filter(
        self, make_canonical_agent: Any, tmp_path: Path
    ) -> None:
        # Arrange — three agents
        agents = [make_canonical_agent(name=f"agent-{i}", skill="skill") for i in range(3)]
        artifacts_per_agent = [_make_artifact(f"agent-{i}", tmp_path) for i in range(3)]
        mock_repo = MagicMock()
        mock_repo.list_all.return_value = agents
        mock_adapter = MagicMock()
        # Each generate() call returns one artifact
        mock_adapter.generate.side_effect = [[a] for a in artifacts_per_agent]
        handler = BuildAgentsCommandHandler(
            repository=mock_repo,
            adapters={"claude_code": mock_adapter},
        )
        command = BuildAgentsCommand(vendor="claude_code")

        # Act
        result = handler.handle(command)

        # Assert
        assert result.built == 3
        assert result.failed == 0
        assert mock_adapter.generate.call_count == 3


# ---------------------------------------------------------------------------
# handle() — dry run
# ---------------------------------------------------------------------------


class TestHandleDryRun:
    """Tests for BuildAgentsCommandHandler.handle() in dry-run mode."""

    def test_dry_run_does_not_write_files(self, make_canonical_agent: Any, tmp_path: Path) -> None:
        # Arrange
        artifact_path = tmp_path / "dry-agent.md"
        agent = make_canonical_agent(name="dry-agent", skill="skill")
        artifacts = [
            GeneratedArtifact(
                path=artifact_path,
                content="content",
                vendor=VendorTarget.CLAUDE_CODE,
                source_agent="dry-agent",
                artifact_type="agent_definition",
            )
        ]
        mock_repo = MagicMock()
        mock_repo.get.return_value = agent
        mock_adapter = MagicMock()
        mock_adapter.generate.return_value = artifacts
        handler = BuildAgentsCommandHandler(
            repository=mock_repo,
            adapters={"claude_code": mock_adapter},
        )
        command = BuildAgentsCommand(vendor="claude_code", agent_name="dry-agent", dry_run=True)

        # Act
        result = handler.handle(command)

        # Assert — artifacts produced but file NOT written
        assert result.built == 1
        assert result.dry_run is True
        assert not artifact_path.exists()

    def test_dry_run_flag_propagated_to_result(self) -> None:
        # Arrange
        mock_repo = MagicMock()
        mock_repo.list_all.return_value = []
        mock_adapter = MagicMock()
        handler = BuildAgentsCommandHandler(
            repository=mock_repo,
            adapters={"claude_code": mock_adapter},
        )
        command = BuildAgentsCommand(vendor="claude_code", dry_run=True)

        # Act
        result = handler.handle(command)

        # Assert
        assert result.dry_run is True


# ---------------------------------------------------------------------------
# handle() — build failure / partial failure
# ---------------------------------------------------------------------------


class TestHandleBuildFailure:
    """Tests for BuildAgentsCommandHandler.handle() when adapter raises."""

    def test_adapter_exception_is_captured_not_raised(self, make_canonical_agent: Any) -> None:
        # Arrange — adapter raises on generate()
        agent = make_canonical_agent(name="fail-agent")
        mock_repo = MagicMock()
        mock_repo.get.return_value = agent
        mock_adapter = MagicMock()
        mock_adapter.generate.side_effect = RuntimeError("adapter exploded")
        handler = BuildAgentsCommandHandler(
            repository=mock_repo,
            adapters={"claude_code": mock_adapter},
        )
        command = BuildAgentsCommand(vendor="claude_code", agent_name="fail-agent")

        # Act — must not propagate
        result = handler.handle(command)

        # Assert
        assert result.failed == 1
        assert result.built == 0
        assert any("adapter exploded" in e for e in result.errors)

    def test_partial_failure_counts_both_built_and_failed(
        self, make_canonical_agent: Any, tmp_path: Path
    ) -> None:
        # Arrange — two agents; second one fails
        agents = [
            make_canonical_agent(name="good-agent"),
            make_canonical_agent(name="bad-agent"),
        ]
        mock_repo = MagicMock()
        mock_repo.list_all.return_value = agents
        mock_adapter = MagicMock()
        mock_adapter.generate.side_effect = [
            [_make_artifact("good-agent", tmp_path)],  # first succeeds
            RuntimeError("bad build"),  # second fails
        ]
        handler = BuildAgentsCommandHandler(
            repository=mock_repo,
            adapters={"claude_code": mock_adapter},
        )
        command = BuildAgentsCommand(vendor="claude_code")

        # Act
        result = handler.handle(command)

        # Assert
        assert result.built == 1
        assert result.failed == 1
