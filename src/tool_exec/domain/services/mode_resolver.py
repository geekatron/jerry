# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Mode resolver service for determining tool execution mode.

Implements a 4-level precedence hierarchy to determine whether a tool
should run locally or inside a container.

References:
    - ADR-PROJ023-001: Configuration Mechanism (L1: mode selection hierarchy)
    - TASK-003: ModeResolverService
    - IN-009 (FIX-12): Accept family-specific env var prefix instead of
      hardcoding RAINBOW_TOOL_MODE
"""

from __future__ import annotations

import os


class ModeResolverService:
    """Resolves the execution mode for a tool command.

    Mode selection follows a 4-level precedence hierarchy (highest first):
    1. CLI flag (--mode)
    2. Environment variable (<ENV_PREFIX>_TOOL_MODE, e.g. RAINBOW_TOOL_MODE)
    3. Configuration file default (from tool-exec.yaml)
    4. Hardcoded default: 'local'

    IN-009 (FIX-12): The environment variable name is now parameterized via
    env_var_prefix so that each family provides its own prefix instead of the
    service hardcoding RAINBOW_TOOL_MODE. The FamilyRouterService provides the
    prefix during service construction in the composition root.

    IN-020-R2: The fallback default prefix was changed from "RAINBOW" to
    "JERRY". When env_var_prefix is None, the service reads JERRY_TOOL_MODE
    (prefix "JERRY" produces env var "JERRY_TOOL_MODE") -- a neutral
    framework-level variable -- rather than silently assuming a
    rainbow-specific variable.
    """

    VALID_MODES = frozenset({"local", "container"})
    DEFAULT_MODE = "local"
    # IN-020-R2: Default changed from "RAINBOW" to "JERRY" to avoid silently
    # coupling a generic service to a specific family. When no prefix is
    # supplied, JERRY_TOOL_MODE is read (prefix "JERRY" + "_TOOL_MODE" suffix),
    # which is a neutral framework-level variable rather than a family-specific
    # one. Family-specific usage (e.g., prefix="RAINBOW") produces RAINBOW_TOOL_MODE.
    _DEFAULT_ENV_PREFIX = "JERRY"

    def __init__(self, env_var_prefix: str | None = None) -> None:
        """Initialize the mode resolver with an optional env var prefix.

        Args:
            env_var_prefix: Family-specific prefix for the mode env var
                (e.g., 'RAINBOW' reads RAINBOW_TOOL_MODE). If None, falls back
                to the JERRY prefix (reads JERRY_TOOL_MODE) -- a neutral
                framework-level env var rather than a rainbow-specific one
                (IN-020-R2).
        """
        prefix = env_var_prefix if env_var_prefix is not None else self._DEFAULT_ENV_PREFIX
        self._env_var_name = f"{prefix}_TOOL_MODE"

    @property
    def env_var_name(self) -> str:
        """Return the environment variable name used for mode resolution.

        Returns:
            Fully qualified env var name, e.g. 'RAINBOW_TOOL_MODE'.
        """
        return self._env_var_name

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

        # Level 2: Environment variable (family-specific)
        env_mode = os.environ.get(self._env_var_name)
        if env_mode is not None:
            return self._validate(env_mode, source=f"env var {self._env_var_name}")

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
