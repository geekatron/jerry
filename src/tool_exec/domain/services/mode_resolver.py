# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Mode resolver service for determining tool execution mode.

Implements a 4-level precedence hierarchy to determine whether a tool
should run locally or inside a container.

References:
    - ADR-PROJ023-001: Configuration Mechanism (L1: mode selection hierarchy)
    - TASK-003: ModeResolverService
"""

from __future__ import annotations

import os


class ModeResolverService:
    """Resolves the execution mode for a tool command.

    Mode selection follows a 4-level precedence hierarchy (highest first):
    1. CLI flag (--mode)
    2. Environment variable (RAINBOW_TOOL_MODE)
    3. Configuration file default (from tool-exec.yaml)
    4. Hardcoded default: 'local'

    The service is stateless and operates purely on the inputs provided
    to the resolve() method.
    """

    VALID_MODES = frozenset({"local", "container"})
    ENV_VAR_NAME = "RAINBOW_TOOL_MODE"
    DEFAULT_MODE = "local"

    def resolve(
        self,
        cli_mode: str | None = None,
        config_mode: str | None = None,
    ) -> str:
        """Determine the execution mode using 4-level precedence.

        Args:
            cli_mode: Mode specified via --mode CLI flag, or None.
            config_mode: Default mode from the tool-exec.yaml configuration
                file, or None.

        Returns:
            Resolved execution mode: 'local' or 'container'.

        Raises:
            ValueError: If the resolved mode is not a valid mode string.
        """
        # Level 1: CLI flag (highest precedence)
        if cli_mode is not None:
            return self._validate(cli_mode, source="CLI --mode flag")

        # Level 2: Environment variable
        env_mode = os.environ.get(self.ENV_VAR_NAME)
        if env_mode is not None:
            return self._validate(env_mode, source=f"env var {self.ENV_VAR_NAME}")

        # Level 3: Configuration file
        if config_mode is not None:
            return self._validate(config_mode, source="config file default_mode")

        # Level 4: Hardcoded default
        return self.DEFAULT_MODE

    def _validate(self, mode: str, source: str) -> str:
        """Validate that a mode string is a recognized value.

        Args:
            mode: The mode string to validate.
            source: Description of where the mode came from, for error messages.

        Returns:
            The validated mode string.

        Raises:
            ValueError: If the mode is not 'local' or 'container'.
        """
        if mode not in self.VALID_MODES:
            msg = (
                f"Invalid execution mode '{mode}' from {source}. "
                f"Must be one of: {', '.join(sorted(self.VALID_MODES))}"
            )
            raise ValueError(msg)
        return mode
