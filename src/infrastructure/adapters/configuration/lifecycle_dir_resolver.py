# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Lifecycle directory resolver with 3-tier precedence.

Resolves the directory used for cross-invocation lifecycle files
(subagent-lifecycle.json, context-state.json) that must be shared
between hook processes and CLI commands regardless of their CWD.

Resolution order:
    1. JERRY_LIFECYCLE_DIR env var — developer/CI override
    2. Config value — context_monitor.lifecycle_dir via LayeredConfigAdapter
    3. Platform default — ~/.jerry/local/ (macOS/Linux) or %APPDATA%/jerry/local/ (Windows)

References:
    - PROJ-004: Context Resilience — lifecycle file location mismatch fix
    - EnvConfigAdapter pattern for env var handling
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

_ENV_VAR = "JERRY_LIFECYCLE_DIR"


def resolve_lifecycle_dir(config_value: str | None = None) -> Path:
    """Resolve lifecycle directory with 3-tier precedence.

    Args:
        config_value: Optional config-provided path (tier 2).

    Returns:
        Resolved absolute Path for lifecycle storage.
    """
    # Tier 1: env var
    env_val = os.environ.get(_ENV_VAR)
    if env_val:
        return Path(env_val).expanduser().resolve()

    # Tier 2: config
    if config_value:
        return Path(config_value).expanduser().resolve()

    # Tier 3: platform default
    return _platform_default_lifecycle_dir()


def _platform_default_lifecycle_dir() -> Path:
    """Return platform-appropriate Jerry lifecycle directory.

    Returns:
        ~/.jerry/local/ on macOS/Linux, %APPDATA%/jerry/local/ on Windows.
    """
    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA", "")
        if appdata:
            return Path(appdata) / "jerry" / "local"
    return Path.home() / ".jerry" / "local"
