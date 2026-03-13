# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""YamlFrontmatterReader Infrastructure Adapter.

Implements IFrontmatterReader by parsing ``---``-delimited YAML frontmatter
directly from markdown files using ``yaml.safe_load`` (stdlib-only, no
subprocess dependency).

This replaces AstFrontmatterReader as the primary implementation wired in
create_docs_generator(). AstFrontmatterReader is retained for worktracker
entity operations that require H-33 AST-based subprocess parsing.

Location: src/docs/infrastructure/adapters/yaml_frontmatter_reader.py
Reference: doc-module-spec.md Section: Input Parsing
           BUG-001: YamlFrontmatterReader fix for SKILL.md / agent file parsing
           H-07: Infrastructure adapter — only imports from domain ports
           H-10: One class per file
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from src.docs.domain.ports.frontmatter_reader import IFrontmatterReader


class YamlFrontmatterReader(IFrontmatterReader):
    """Frontmatter reader that parses ``---``-delimited YAML directly.

    Reads YAML frontmatter from markdown files without spawning a subprocess.
    Uses ``yaml.safe_load`` exclusively — never ``yaml.load`` — to prevent
    arbitrary-code-execution via untrusted YAML tags (OWASP A03/Injection).

    Correctly handles:
    - Multi-line block scalars (``>-``, ``|``, ``>``).
    - Files with no frontmatter (returns empty dict).
    - Empty frontmatter blocks (returns empty dict).
    - ``---`` delimiters followed immediately by EOF.

    H-07 compliance: imports only from ``src.docs.domain.ports``.
    H-10 compliance: one class per file.
    """

    def read_frontmatter(self, file_path: str) -> dict[str, Any]:
        """Read and return the YAML frontmatter of a markdown file.

        The method locates the first ``---\\n`` delimiter, reads content up to
        the second ``---\\n`` (or ``---`` at EOF), and parses the enclosed
        block with ``yaml.safe_load``.

        Args:
            file_path: Absolute or repo-relative path to the ``.md`` file.

        Returns:
            Mapping of frontmatter field names to their parsed values.
            Returns an empty dict when the file has no YAML frontmatter.

        Raises:
            FileNotFoundError: If the file does not exist at ``file_path``.
            ValueError: If the frontmatter block is present but contains
                invalid YAML syntax.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        content = path.read_text(encoding="utf-8")

        # A file must start with "---\n" (or "---\r\n") to have frontmatter.
        if not (content.startswith("---\n") or content.startswith("---\r\n")):
            return {}

        # Strip the opening "---\n" and search for the closing "---" boundary.
        after_open = content[4:]  # skip "---\n"

        # Find the closing delimiter: "---" on its own line.
        # The closing delimiter may be "---\n" (mid-file) or "---" at EOF.
        close_index = _find_closing_delimiter(after_open)
        if close_index == -1:
            # Opening "---" exists but no closing delimiter — treat as no frontmatter.
            return {}

        frontmatter_block = after_open[:close_index]

        if not frontmatter_block.strip():
            return {}

        try:
            data = yaml.safe_load(frontmatter_block)
        except yaml.YAMLError as exc:
            raise ValueError(f"Malformed YAML frontmatter in {file_path}: {exc}") from exc

        if data is None:
            return {}

        if not isinstance(data, dict):
            raise ValueError(
                f"Expected mapping at top of YAML frontmatter, "
                f"got {type(data).__name__} in {file_path}"
            )

        return data


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _find_closing_delimiter(text: str) -> int:
    """Return the start index of the closing ``---`` delimiter in *text*.

    *text* is the file content after the opening ``---\\n`` has been stripped.
    The closing delimiter must appear at the start of a line.

    Args:
        text: Content following the opening ``---\\n``.

    Returns:
        Character index of the start of the closing ``---`` sequence, or
        ``-1`` if no closing delimiter is found.
    """
    # Search for "\n---\n" (mid-file) or "\n---" at exact EOF.
    # We scan line by line to avoid false positives inside block scalars.
    lines = text.splitlines(keepends=True)
    pos = 0
    for line in lines:
        stripped = line.rstrip("\r\n")
        if stripped == "---":
            return pos
        pos += len(line)

    return -1
