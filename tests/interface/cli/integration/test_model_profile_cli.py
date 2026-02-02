"""Integration tests for model profile CLI usage.

Tests the end-to-end model profile selection via CLI arguments,
ensuring correct resolution from profile to final adapter call.

References:
    - TASK-423: Implement Model Profiles - Track B
    - EN-031: Model Selection Capability
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from src.interface.cli.main import main


class TestProfileCLIIntegration:
    """Test model profile selection via CLI."""

    @pytest.fixture(autouse=True)
    def mock_adapter(self) -> MagicMock:
        """Mock the CLIAdapter to capture method calls."""
        with patch("src.interface.cli.main.CLIAdapter") as mock_class:
            mock_instance = MagicMock()
            mock_instance.cmd_transcript_parse.return_value = 0
            mock_class.return_value = mock_instance
            yield mock_instance

    @pytest.fixture(autouse=True)
    def mock_args(self) -> None:
        """Mock sys.argv to avoid test runner args interference."""
        with patch("sys.argv", ["jerry"]):
            yield

    def test_no_profile_uses_balanced_default(self, mock_adapter: MagicMock) -> None:
        """No --profile flag should use balanced profile."""
        with patch(
            "sys.argv",
            ["jerry", "transcript", "parse", "test.vtt"],
        ):
            main()

        # Should use balanced profile defaults
        call_args = mock_adapter.cmd_transcript_parse.call_args
        assert call_args.kwargs["model_parser"] == "haiku"
        assert call_args.kwargs["model_extractor"] == "sonnet"
        assert call_args.kwargs["model_formatter"] == "haiku"
        assert call_args.kwargs["model_mindmap"] == "sonnet"
        assert call_args.kwargs["model_critic"] == "sonnet"

    def test_economy_profile(self, mock_adapter: MagicMock) -> None:
        """Economy profile should use haiku for all agents."""
        with patch(
            "sys.argv",
            ["jerry", "transcript", "parse", "test.vtt", "--profile", "economy"],
        ):
            main()

        call_args = mock_adapter.cmd_transcript_parse.call_args
        assert call_args.kwargs["model_parser"] == "haiku"
        assert call_args.kwargs["model_extractor"] == "haiku"
        assert call_args.kwargs["model_formatter"] == "haiku"
        assert call_args.kwargs["model_mindmap"] == "haiku"
        assert call_args.kwargs["model_critic"] == "haiku"

    def test_quality_profile(self, mock_adapter: MagicMock) -> None:
        """Quality profile should use opus for critical agents."""
        with patch(
            "sys.argv",
            ["jerry", "transcript", "parse", "test.vtt", "--profile", "quality"],
        ):
            main()

        call_args = mock_adapter.cmd_transcript_parse.call_args
        assert call_args.kwargs["model_parser"] == "sonnet"
        assert call_args.kwargs["model_extractor"] == "opus"
        assert call_args.kwargs["model_formatter"] == "sonnet"
        assert call_args.kwargs["model_mindmap"] == "sonnet"
        assert call_args.kwargs["model_critic"] == "opus"

    def test_speed_profile(self, mock_adapter: MagicMock) -> None:
        """Speed profile should use haiku for all agents."""
        with patch(
            "sys.argv",
            ["jerry", "transcript", "parse", "test.vtt", "--profile", "speed"],
        ):
            main()

        call_args = mock_adapter.cmd_transcript_parse.call_args
        assert call_args.kwargs["model_parser"] == "haiku"
        assert call_args.kwargs["model_extractor"] == "haiku"
        assert call_args.kwargs["model_formatter"] == "haiku"
        assert call_args.kwargs["model_mindmap"] == "haiku"
        assert call_args.kwargs["model_critic"] == "haiku"

    def test_explicit_flag_overrides_profile(self, mock_adapter: MagicMock) -> None:
        """Individual --model-* flag should override profile."""
        with patch(
            "sys.argv",
            [
                "jerry",
                "transcript",
                "parse",
                "test.vtt",
                "--profile",
                "economy",
                "--model-extractor",
                "opus",
            ],
        ):
            main()

        call_args = mock_adapter.cmd_transcript_parse.call_args
        assert call_args.kwargs["model_parser"] == "haiku"  # From economy
        assert call_args.kwargs["model_extractor"] == "opus"  # Override
        assert call_args.kwargs["model_formatter"] == "haiku"  # From economy
        assert call_args.kwargs["model_mindmap"] == "haiku"  # From economy
        assert call_args.kwargs["model_critic"] == "haiku"  # From economy

    def test_multiple_overrides(self, mock_adapter: MagicMock) -> None:
        """Multiple --model-* flags should all override profile."""
        with patch(
            "sys.argv",
            [
                "jerry",
                "transcript",
                "parse",
                "test.vtt",
                "--profile",
                "economy",
                "--model-parser",
                "sonnet",
                "--model-extractor",
                "opus",
                "--model-critic",
                "sonnet",
            ],
        ):
            main()

        call_args = mock_adapter.cmd_transcript_parse.call_args
        assert call_args.kwargs["model_parser"] == "sonnet"  # Override
        assert call_args.kwargs["model_extractor"] == "opus"  # Override
        assert call_args.kwargs["model_formatter"] == "haiku"  # From economy
        assert call_args.kwargs["model_mindmap"] == "haiku"  # From economy
        assert call_args.kwargs["model_critic"] == "sonnet"  # Override

    def test_override_without_profile_uses_default(self, mock_adapter: MagicMock) -> None:
        """Override without --profile should use balanced default."""
        with patch(
            "sys.argv",
            [
                "jerry",
                "transcript",
                "parse",
                "test.vtt",
                "--model-extractor",
                "opus",
            ],
        ):
            main()

        call_args = mock_adapter.cmd_transcript_parse.call_args
        assert call_args.kwargs["model_parser"] == "haiku"  # From balanced
        assert call_args.kwargs["model_extractor"] == "opus"  # Override
        assert call_args.kwargs["model_formatter"] == "haiku"  # From balanced
        assert call_args.kwargs["model_mindmap"] == "sonnet"  # From balanced
        assert call_args.kwargs["model_critic"] == "sonnet"  # From balanced
