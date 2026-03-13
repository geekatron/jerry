# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""IFrontmatterReader Domain Port.

Defines the interface that all frontmatter-reading adapters must satisfy.
The domain layer depends on this Protocol; infrastructure adapters implement it.
This keeps the domain free from any subprocess, JSON, or YAML concerns.

Location: src/docs/domain/ports/frontmatter_reader.py
Reference: doc-module-spec.md Section: Input Parsing
           H-33: AST-based parsing REQUIRED for worktracker entity ops
"""

from typing import Any, Protocol


class IFrontmatterReader(Protocol):
    """Port for reading YAML frontmatter from markdown files.

    Implementations:
        - YamlFrontmatterReader: primary implementation; parses ``---``-delimited
          YAML frontmatter directly using ``yaml.safe_load`` (no subprocess).
          (src/docs/infrastructure/adapters/yaml_frontmatter_reader.py)
        - AstFrontmatterReader: legacy implementation; delegates to
          ``jerry ast frontmatter`` subprocess (H-33 compliance for worktracker
          entity operations).
          (src/docs/infrastructure/adapters/ast_frontmatter_reader.py)

    Security note (M-5): The returned dict contains *raw* field values.
    Callers are responsible for schema validation before using the data.
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
            ValueError: If the frontmatter block is present but malformed
                (e.g., invalid YAML syntax).
            RuntimeError: If the underlying parser process fails unexpectedly.
        """
        ...
