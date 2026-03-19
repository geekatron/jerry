# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""AstFrontmatterReader Infrastructure Adapter.

Implements IFrontmatterReader by delegating to ``jerry ast frontmatter``
via subprocess, ensuring H-33 compliance (AST-based parsing, never regex).

Location: src/docs/infrastructure/adapters/ast_frontmatter_reader.py
Reference: doc-module-spec.md Section: Input Parsing
           H-05: UV-only Python execution
           H-33: AST-based parsing REQUIRED
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from src.docs.domain.ports.frontmatter_reader import IFrontmatterReader


class AstFrontmatterReader(IFrontmatterReader):
    """Frontmatter reader that delegates to ``jerry ast frontmatter``.

    Uses ``uv run jerry ast frontmatter {file_path}`` to parse YAML
    frontmatter via the AST-based parser (H-33 compliance).  The subprocess
    uses list-form arguments (never ``shell=True``) to prevent command
    injection.

    H-05 compliance: Uses ``uv run`` for Python execution.
    H-33 compliance: Uses ``jerry ast frontmatter`` (AST-based), never regex.
    """

    def read_frontmatter(self, file_path: str) -> dict[str, Any]:
        """Read and return the YAML frontmatter of a markdown file.

        Args:
            file_path: Absolute or repo-relative path to the ``.md`` file.

        Returns:
            Mapping of frontmatter field names to their parsed values.
            Returns an empty dict when the file has no YAML frontmatter.

        Raises:
            FileNotFoundError: If the file does not exist at ``file_path``.
            ValueError: If the frontmatter block is present but malformed.
            RuntimeError: If the subprocess fails unexpectedly.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            result = subprocess.run(
                ["uv", "run", "jerry", "ast", "frontmatter", str(file_path)],
                capture_output=True,
                text=True,
                timeout=30,
            )
        except subprocess.TimeoutExpired as e:
            raise RuntimeError(f"Frontmatter extraction timed out for {file_path}") from e
        except OSError as e:
            raise RuntimeError(f"Failed to run jerry ast frontmatter: {e}") from e

        if result.returncode != 0:
            stderr = result.stderr.strip()
            if "parse error" in stderr.lower() or "malformed" in stderr.lower():
                raise ValueError(f"Malformed frontmatter in {file_path}: {stderr}")
            raise RuntimeError(
                f"jerry ast frontmatter failed for {file_path} "
                f"(exit code {result.returncode}): {stderr}"
            )

        stdout = result.stdout.strip()
        if not stdout or stdout == "{}":
            return {}

        try:
            data = json.loads(stdout)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON from jerry ast frontmatter for {file_path}: {e}") from e

        if not isinstance(data, dict):
            raise ValueError(
                f"Expected dict from frontmatter, got {type(data).__name__} for {file_path}"
            )

        return data
