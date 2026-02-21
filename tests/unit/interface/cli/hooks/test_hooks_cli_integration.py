# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for hooks CLI integration (parser and adapter).

BDD scenarios:
    - jerry hooks --help shows hooks subcommands
    - jerry hooks prompt-submit is registered in parser
    - jerry hooks session-start is registered in parser
    - jerry hooks pre-compact is registered in parser
    - jerry hooks pre-tool-use is registered in parser
    - Adapter routes hooks_command to correct handler

References:
    - EN-006: jerry hooks CLI Command Namespace
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

import json
import sys
from unittest.mock import MagicMock

import pytest

from src.interface.cli.parser import create_parser


# =============================================================================
# Tests: CLI Parser
# =============================================================================


class TestHooksNamespaceRegisteredInParser:
    """BDD: hooks subcommands registered in CLI parser."""

    def test_hooks_namespace_parseable(self) -> None:
        """jerry hooks can be parsed without error."""
        parser = create_parser()
        args = parser.parse_args(["hooks", "prompt-submit"])
        assert args.namespace == "hooks"
        assert args.hooks_command == "prompt-submit"

    def test_hooks_prompt_submit_registered(self) -> None:
        """jerry hooks prompt-submit is a valid command."""
        parser = create_parser()
        args = parser.parse_args(["hooks", "prompt-submit"])
        assert args.hooks_command == "prompt-submit"

    def test_hooks_session_start_registered(self) -> None:
        """jerry hooks session-start is a valid command."""
        parser = create_parser()
        args = parser.parse_args(["hooks", "session-start"])
        assert args.hooks_command == "session-start"

    def test_hooks_pre_compact_registered(self) -> None:
        """jerry hooks pre-compact is a valid command."""
        parser = create_parser()
        args = parser.parse_args(["hooks", "pre-compact"])
        assert args.hooks_command == "pre-compact"

    def test_hooks_pre_tool_use_registered(self) -> None:
        """jerry hooks pre-tool-use is a valid command."""
        parser = create_parser()
        args = parser.parse_args(["hooks", "pre-tool-use"])
        assert args.hooks_command == "pre-tool-use"


# =============================================================================
# Tests: CLI Adapter hooks routing
# =============================================================================


class TestAdapterHooksRouting:
    """BDD: CLIAdapter routes hooks namespace to correct handler."""

    def test_adapter_routes_prompt_submit(
        self,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Adapter routes hooks prompt-submit to prompt_submit_handler."""
        from src.interface.cli.adapter import CLIAdapter

        mock_dispatcher = MagicMock()
        mock_prompt_submit = MagicMock()
        mock_prompt_submit.handle.return_value = 0

        hooks_handlers = {
            "prompt-submit": mock_prompt_submit,
            "session-start": MagicMock(),
            "pre-compact": MagicMock(),
            "pre-tool-use": MagicMock(),
        }

        adapter = CLIAdapter(
            dispatcher=mock_dispatcher,
            hooks_handlers=hooks_handlers,
        )

        result = adapter.cmd_hooks("prompt-submit", "")
        assert result == 0
        mock_prompt_submit.handle.assert_called_once_with("")

    def test_adapter_routes_pre_compact(
        self,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Adapter routes hooks pre-compact to pre_compact_handler."""
        from src.interface.cli.adapter import CLIAdapter

        mock_dispatcher = MagicMock()
        mock_pre_compact = MagicMock()
        mock_pre_compact.handle.return_value = 0

        hooks_handlers = {
            "prompt-submit": MagicMock(),
            "session-start": MagicMock(),
            "pre-compact": mock_pre_compact,
            "pre-tool-use": MagicMock(),
        }

        adapter = CLIAdapter(
            dispatcher=mock_dispatcher,
            hooks_handlers=hooks_handlers,
        )

        result = adapter.cmd_hooks("pre-compact", "")
        assert result == 0
        mock_pre_compact.handle.assert_called_once_with("")

    def test_adapter_returns_error_when_no_hooks_handlers(
        self,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Adapter returns 1 when hooks_handlers not configured."""
        from src.interface.cli.adapter import CLIAdapter

        mock_dispatcher = MagicMock()
        adapter = CLIAdapter(dispatcher=mock_dispatcher)

        result = adapter.cmd_hooks("prompt-submit", "")
        assert result == 1

    def test_adapter_returns_error_for_unknown_hooks_command(
        self,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Adapter returns 1 for unknown hooks command."""
        from src.interface.cli.adapter import CLIAdapter

        mock_dispatcher = MagicMock()
        hooks_handlers = {
            "prompt-submit": MagicMock(),
            "session-start": MagicMock(),
            "pre-compact": MagicMock(),
            "pre-tool-use": MagicMock(),
        }

        adapter = CLIAdapter(
            dispatcher=mock_dispatcher,
            hooks_handlers=hooks_handlers,
        )

        result = adapter.cmd_hooks("unknown-command", "")
        assert result == 1
