# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Shared CLI project-root resolution (BUG-010, GH #337).

Single source of truth for resolving the USER'S project root across CLI
namespaces (``config``, ``ast``, ...). Never anchors to the Jerry
installation's own directory tree, so commands operate on the user's
repository regardless of where Jerry is installed (plugin checkout,
marketplace install, or development clone).
"""

from __future__ import annotations

import os
from pathlib import Path


def get_project_root() -> Path:
    """Resolve the user's project root directory.

    Resolution order:
        1. ``CLAUDE_PROJECT_DIR`` environment variable (set by Claude Code
           for the active workspace). An empty value is treated as unset.
        2. The current working directory.

    Returns:
        Path to the user's project root.
    """
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR")
    if project_dir:
        return Path(project_dir)
    return Path.cwd()
