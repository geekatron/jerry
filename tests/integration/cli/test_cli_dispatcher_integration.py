"""
Integration tests for CLI dispatcher integration.

Tests that CLI commands route through the dispatcher.

Test Distribution per impl-es-e-003:
- Happy Path (60%): 3 tests - init dispatches, handler result returned, projects list works
- Negative (30%): 2 tests - missing dispatcher raises, handler error propagates
- Edge (10%): 1 test - empty result handling
"""

from __future__ import annotations

from unittest.mock import Mock

import pytest

# === Happy Path Tests (60%) ===


class TestCLIDispatcherIntegrationHappyPath:
    """Happy path tests for CLI dispatcher integration."""

    def test_cli_adapter_is_importable(self) -> None:
        """CLIAdapter class can be imported."""
        from src.interface.cli.adapter import CLIAdapter

        assert CLIAdapter is not None

    def test_cli_adapter_accepts_dispatcher(self) -> None:
        """CLIAdapter constructor accepts IQueryDispatcher."""
        from src.application.dispatchers.query_dispatcher import QueryDispatcher
        from src.interface.cli.adapter import CLIAdapter

        dispatcher = QueryDispatcher()
        adapter = CLIAdapter(dispatcher=dispatcher)

        assert adapter is not None

    def test_cmd_init_dispatches_query(self) -> None:
        """cmd_init routes through dispatcher."""
        from src.application.handlers import GetProjectContextQueryData
        from src.interface.cli.adapter import CLIAdapter

        # Arrange
        mock_dispatcher = Mock()
        mock_dispatcher.dispatch.return_value = {
            "jerry_project": None,
            "project_id": None,
            "validation": None,
            "available_projects": [],
            "next_number": 1,
        }

        adapter = CLIAdapter(dispatcher=mock_dispatcher)

        # Act
        adapter.cmd_init(json_output=False)

        # Assert - dispatcher was called with correct query type
        mock_dispatcher.dispatch.assert_called_once()
        call_args = mock_dispatcher.dispatch.call_args[0][0]
        assert isinstance(call_args, GetProjectContextQueryData)


# === Negative Tests (30%) ===


class TestCLIDispatcherIntegrationNegative:
    """Negative tests for CLI dispatcher integration."""

    def test_cli_adapter_requires_dispatcher(self) -> None:
        """CLIAdapter raises if dispatcher is None."""
        from src.interface.cli.adapter import CLIAdapter

        with pytest.raises((TypeError, ValueError)):
            CLIAdapter(dispatcher=None)

    def test_handler_error_propagates(self) -> None:
        """Handler exceptions propagate through adapter."""
        from src.interface.cli.adapter import CLIAdapter

        # Arrange
        mock_dispatcher = Mock()
        mock_dispatcher.dispatch.side_effect = RuntimeError("Handler failed")

        adapter = CLIAdapter(dispatcher=mock_dispatcher)

        # Act & Assert
        with pytest.raises(RuntimeError) as exc_info:
            adapter.cmd_init(json_output=False)

        assert "Handler failed" in str(exc_info.value)


# === Edge Case Tests (10%) ===


class TestCLIDispatcherIntegrationEdgeCases:
    """Edge case tests for CLI dispatcher integration."""

    def test_empty_projects_handled(self) -> None:
        """Empty project list is handled gracefully."""
        from src.interface.cli.adapter import CLIAdapter

        # Arrange
        mock_dispatcher = Mock()
        mock_dispatcher.dispatch.return_value = {
            "jerry_project": None,
            "project_id": None,
            "validation": None,
            "available_projects": [],
            "next_number": 1,
        }

        adapter = CLIAdapter(dispatcher=mock_dispatcher)

        # Act - should not raise
        result = adapter.cmd_init(json_output=True)

        # Assert - returns formatted output
        assert result is not None or result == 0  # Either returns dict or exit code
