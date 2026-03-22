# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""Worktree isolation functions for CLM-002.

Derives Docker Compose project names and session state file paths
from the git worktree path to prevent concurrent worktree collisions.
"""

from __future__ import annotations

import hashlib
import logging
import os
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)


def derive_compose_project_name(project_root: Path | None = None) -> str:
    """Derive a worktree-isolated Docker Compose project name.

    Uses CLAUDE_PROJECT_DIR environment variable (set by Claude Code) or
    falls back to git rev-parse --show-toplevel. Hashes the path to create
    a short, filesystem-safe identifier.

    Args:
        project_root: Override for the project root path. If None, auto-detect.

    Returns:
        Compose project name in the format ``rainbow-{hash8}``.
    """
    if project_root is not None:
        worktree_path = str(project_root)
    else:
        # Try CLAUDE_PROJECT_DIR first (set by Claude Code)
        worktree_path = os.environ.get("CLAUDE_PROJECT_DIR", "")
        if not worktree_path:
            # Fall back to git
            try:
                result = subprocess.run(
                    ["git", "rev-parse", "--show-toplevel"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                worktree_path = result.stdout.strip() if result.returncode == 0 else ""
            except (FileNotFoundError, subprocess.TimeoutExpired):
                worktree_path = ""

    if not worktree_path:
        logger.warning("Cannot determine worktree path; using default compose project name")
        return "rainbow"

    # 8-char hash is enough for local worktree disambiguation
    path_hash = hashlib.sha256(worktree_path.encode()).hexdigest()[:8]
    return f"rainbow-{path_hash}"


def session_state_path(project_root: Path) -> Path:
    """Return the session state file path, isolated per worktree.

    Args:
        project_root: Project root directory.

    Returns:
        Path to the session state YAML file.
    """
    compose_name = derive_compose_project_name(project_root)
    suffix = compose_name.replace("rainbow-", "") if "-" in compose_name else "default"
    return project_root / "work" / f".rainbow-session-state-{suffix}.yaml"
