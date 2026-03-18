# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for ModeResolverService."""

from __future__ import annotations

import os

import pytest

from src.tool_exec.domain.services.mode_resolver import ModeResolverService


class TestModeResolverPrecedence:
    """Tests for the 4-level mode resolution precedence."""

    def setup_method(self) -> None:
        """Create a fresh resolver and clean env."""
        self.resolver = ModeResolverService()
        # Ensure env var is not set from previous tests
        os.environ.pop("RAINBOW_TOOL_MODE", None)

    def teardown_method(self) -> None:
        """Clean up env var."""
        os.environ.pop("RAINBOW_TOOL_MODE", None)

    def test_level_1_cli_flag_takes_precedence(self) -> None:
        """CLI --mode flag has highest precedence."""
        os.environ["RAINBOW_TOOL_MODE"] = "container"
        mode = self.resolver.resolve(cli_mode="local", config_mode="container")
        assert mode == "local"

    def test_level_2_env_var(self) -> None:
        """Environment variable is used when CLI flag is absent."""
        os.environ["RAINBOW_TOOL_MODE"] = "container"
        mode = self.resolver.resolve(cli_mode=None, config_mode="local")
        assert mode == "container"

    def test_level_3_config_file(self) -> None:
        """Config file default is used when CLI flag and env var are absent."""
        mode = self.resolver.resolve(cli_mode=None, config_mode="container")
        assert mode == "container"

    def test_level_4_hardcoded_default(self) -> None:
        """Hardcoded 'local' default is used when nothing else is set."""
        mode = self.resolver.resolve(cli_mode=None, config_mode=None)
        assert mode == "local"


class TestModeResolverValidation:
    """Tests for mode value validation."""

    def setup_method(self) -> None:
        """Create a fresh resolver."""
        self.resolver = ModeResolverService()
        os.environ.pop("RAINBOW_TOOL_MODE", None)

    def teardown_method(self) -> None:
        """Clean up."""
        os.environ.pop("RAINBOW_TOOL_MODE", None)

    def test_invalid_cli_mode_raises(self) -> None:
        """Invalid CLI mode raises ValueError."""
        with pytest.raises(ValueError, match="Invalid execution mode"):
            self.resolver.resolve(cli_mode="hybrid")

    def test_invalid_env_mode_raises(self) -> None:
        """Invalid env var mode raises ValueError."""
        os.environ["RAINBOW_TOOL_MODE"] = "invalid"
        with pytest.raises(ValueError, match="Invalid execution mode"):
            self.resolver.resolve()

    def test_invalid_config_mode_raises(self) -> None:
        """Invalid config mode raises ValueError."""
        with pytest.raises(ValueError, match="Invalid execution mode"):
            self.resolver.resolve(config_mode="invalid")

    @pytest.mark.parametrize("mode", ["local", "container"])
    def test_valid_modes(self, mode: str) -> None:
        """Valid mode values are accepted."""
        result = self.resolver.resolve(cli_mode=mode)
        assert result == mode
