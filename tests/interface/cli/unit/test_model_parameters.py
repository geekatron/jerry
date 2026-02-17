# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for CLI model parameter handling.

Tests that the jerry transcript parse command correctly accepts
and processes model selection parameters.

Note: TASK-423 changed defaults from argparse to profile resolution.
Default values are now None in args, and resolved via resolve_model_config().

References:
    - TASK-420: Add CLI parameters for model selection
    - TASK-423: Implement Model Profiles - Track B
    - EN-031: Model Selection Capability
"""

from __future__ import annotations

import pytest

from src.interface.cli.parser import create_parser


class TestModelParameterParsing:
    """Test model parameter parsing in CLI."""

    def test_default_model_values(self) -> None:
        """Default model values are None (resolved via profile)."""
        parser = create_parser()
        args = parser.parse_args(["transcript", "parse", "test.vtt"])

        # TASK-423: Defaults moved to profile resolution
        assert args.model_parser is None
        assert args.model_extractor is None
        assert args.model_formatter is None
        assert args.model_mindmap is None
        assert args.model_critic is None

    def test_custom_parser_model(self) -> None:
        """--model-parser accepts custom values."""
        parser = create_parser()
        args = parser.parse_args(["transcript", "parse", "test.vtt", "--model-parser", "opus"])

        assert args.model_parser == "opus"
        assert args.model_extractor is None  # Other params remain None

    def test_custom_extractor_model(self) -> None:
        """--model-extractor accepts custom values."""
        parser = create_parser()
        args = parser.parse_args(["transcript", "parse", "test.vtt", "--model-extractor", "haiku"])

        assert args.model_extractor == "haiku"

    def test_custom_formatter_model(self) -> None:
        """--model-formatter accepts custom values."""
        parser = create_parser()
        args = parser.parse_args(["transcript", "parse", "test.vtt", "--model-formatter", "opus"])

        assert args.model_formatter == "opus"

    def test_custom_mindmap_model(self) -> None:
        """--model-mindmap accepts custom values."""
        parser = create_parser()
        args = parser.parse_args(["transcript", "parse", "test.vtt", "--model-mindmap", "haiku"])

        assert args.model_mindmap == "haiku"

    def test_custom_critic_model(self) -> None:
        """--model-critic accepts custom values."""
        parser = create_parser()
        args = parser.parse_args(["transcript", "parse", "test.vtt", "--model-critic", "opus"])

        assert args.model_critic == "opus"

    def test_all_models_custom(self) -> None:
        """All model parameters can be customized simultaneously."""
        parser = create_parser()
        args = parser.parse_args(
            [
                "transcript",
                "parse",
                "test.vtt",
                "--model-parser",
                "opus",
                "--model-extractor",
                "haiku",
                "--model-formatter",
                "opus",
                "--model-mindmap",
                "sonnet",
                "--model-critic",
                "haiku",
            ]
        )

        assert args.model_parser == "opus"
        assert args.model_extractor == "haiku"
        assert args.model_formatter == "opus"
        assert args.model_mindmap == "sonnet"
        assert args.model_critic == "haiku"


class TestModelParameterValidation:
    """Test model parameter validation."""

    def test_invalid_parser_model_rejected(self) -> None:
        """Invalid --model-parser value causes error."""
        parser = create_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(["transcript", "parse", "test.vtt", "--model-parser", "gpt-4"])

    def test_invalid_extractor_model_rejected(self) -> None:
        """Invalid --model-extractor value causes error."""
        parser = create_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(["transcript", "parse", "test.vtt", "--model-extractor", "llama"])

    def test_invalid_formatter_model_rejected(self) -> None:
        """Invalid --model-formatter value causes error."""
        parser = create_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(["transcript", "parse", "test.vtt", "--model-formatter", "gemini"])

    def test_invalid_mindmap_model_rejected(self) -> None:
        """Invalid --model-mindmap value causes error."""
        parser = create_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(["transcript", "parse", "test.vtt", "--model-mindmap", "chatgpt"])

    def test_invalid_critic_model_rejected(self) -> None:
        """Invalid --model-critic value causes error."""
        parser = create_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(["transcript", "parse", "test.vtt", "--model-critic", "bard"])


class TestModelParameterChoices:
    """Test valid model choices for each parameter."""

    @pytest.mark.parametrize("model", ["opus", "sonnet", "haiku"])
    def test_parser_accepts_all_valid_models(self, model: str) -> None:
        """--model-parser accepts all valid model values."""
        parser = create_parser()
        args = parser.parse_args(["transcript", "parse", "test.vtt", "--model-parser", model])

        assert args.model_parser == model

    @pytest.mark.parametrize("model", ["opus", "sonnet", "haiku"])
    def test_extractor_accepts_all_valid_models(self, model: str) -> None:
        """--model-extractor accepts all valid model values."""
        parser = create_parser()
        args = parser.parse_args(["transcript", "parse", "test.vtt", "--model-extractor", model])

        assert args.model_extractor == model

    @pytest.mark.parametrize("model", ["opus", "sonnet", "haiku"])
    def test_formatter_accepts_all_valid_models(self, model: str) -> None:
        """--model-formatter accepts all valid model values."""
        parser = create_parser()
        args = parser.parse_args(["transcript", "parse", "test.vtt", "--model-formatter", model])

        assert args.model_formatter == model

    @pytest.mark.parametrize("model", ["opus", "sonnet", "haiku"])
    def test_mindmap_accepts_all_valid_models(self, model: str) -> None:
        """--model-mindmap accepts all valid model values."""
        parser = create_parser()
        args = parser.parse_args(["transcript", "parse", "test.vtt", "--model-mindmap", model])

        assert args.model_mindmap == model

    @pytest.mark.parametrize("model", ["opus", "sonnet", "haiku"])
    def test_critic_accepts_all_valid_models(self, model: str) -> None:
        """--model-critic accepts all valid model values."""
        parser = create_parser()
        args = parser.parse_args(["transcript", "parse", "test.vtt", "--model-critic", model])

        assert args.model_critic == model


class TestModelParameterHelp:
    """Test help text mentions model parameters."""

    def test_help_includes_all_model_parameters(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Help text includes all 5 model parameters."""
        parser = create_parser()

        # Parse to the transcript parse subcommand level to see its help
        with pytest.raises(SystemExit):
            parser.parse_args(["transcript", "parse", "--help"])

        captured = capsys.readouterr()
        help_text = captured.out

        assert "--model-parser" in help_text
        assert "--model-extractor" in help_text
        assert "--model-formatter" in help_text
        assert "--model-mindmap" in help_text
        assert "--model-critic" in help_text

    def test_help_shows_profile_information(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Help text explains profile and override behavior."""
        parser = create_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(["transcript", "parse", "--help"])

        captured = capsys.readouterr()
        help_text = captured.out.lower()

        # TASK-423: Should mention profile and override behavior
        assert "--profile" in help_text
        assert "overrides --profile" in help_text or "override profile" in help_text
