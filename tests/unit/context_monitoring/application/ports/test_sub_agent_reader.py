# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for ISubAgentReader port.

BDD scenarios:
    - Protocol is runtime-checkable
    - TranscriptSubAgentReader satisfies the protocol

References:
    - EN-018: Sub-Agent Transcript Parser
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

from pathlib import Path

from src.context_monitoring.application.ports.sub_agent_reader import (
    ISubAgentReader,
)
from src.context_monitoring.infrastructure.adapters.transcript_sub_agent_reader import (
    TranscriptSubAgentReader,
)


class TestSubAgentReaderProtocol:
    """BDD: ISubAgentReader is a runtime-checkable protocol."""

    def test_protocol_is_runtime_checkable(self, tmp_path: Path) -> None:
        """TranscriptSubAgentReader satisfies ISubAgentReader."""
        reader = TranscriptSubAgentReader(lifecycle_path=tmp_path / "lifecycle.json")
        assert isinstance(reader, ISubAgentReader)
