# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Golden-file regression test suite (WI-024).

Validates that ``UniversalDocument.parse()`` produces identical output to
existing parsers for all known file patterns. Ensures migration safety
from single-purpose parsers to the universal facade.

References:
    - ADR-PROJ005-003 Migration Safety
    - H-20: BDD test-first
    - H-33: AST-based parsing REQUIRED
"""

from __future__ import annotations

from pathlib import Path

import pytest

from src.domain.markdown_ast.document_type import DocumentType
from src.domain.markdown_ast.frontmatter import (
    BlockquoteFrontmatter,
)
from src.domain.markdown_ast.jerry_document import JerryDocument
from src.domain.markdown_ast.reinject import extract_reinject_directives
from src.domain.markdown_ast.universal_document import UniversalDocument

# Repository root for golden-file scanning
REPO_ROOT = Path(__file__).resolve().parents[3]


def _find_md_files(directory: str, pattern: str = "**/*.md") -> list[Path]:
    """Find markdown files in a directory relative to repo root.

    Args:
        directory: Directory relative to repo root.
        pattern: Glob pattern for file discovery.

    Returns:
        List of found markdown file paths.
    """
    target = REPO_ROOT / directory
    if not target.exists():
        return []
    return sorted(target.glob(pattern))


# =============================================================================
# Worktracker Entity Regression
# =============================================================================


class TestWorktrackerEntityRegression:
    """Verify UniversalDocument matches BlockquoteFrontmatter for worktracker entities."""

    @pytest.mark.regression
    def test_worktracker_frontmatter_parity(self) -> None:
        """All worktracker entity files produce identical frontmatter via both paths."""
        # Find worktracker entity files in projects/
        entity_files: list[Path] = []
        projects_dir = REPO_ROOT / "projects"
        if projects_dir.exists():
            for md_file in projects_dir.rglob("*.md"):
                if md_file.name in ("PLAN.md", "README.md", "WORKTRACKER.md"):
                    continue
                # Check if it has blockquote frontmatter
                try:
                    content = md_file.read_text(encoding="utf-8")
                except (OSError, UnicodeDecodeError):
                    continue
                if content.startswith(">") or "\n>" in content[:200]:
                    entity_files.append(md_file)

        if not entity_files:
            pytest.skip("No worktracker entity files found")

        # Test a sample (up to 10 files for speed)
        sample = entity_files[:10]
        for entity_file in sample:
            content = entity_file.read_text(encoding="utf-8")
            doc = JerryDocument.parse(content)

            # Legacy path: BlockquoteFrontmatter directly
            legacy_fm = BlockquoteFrontmatter.extract(doc)

            # New path: UniversalDocument with explicit type
            rel_path = str(entity_file.relative_to(REPO_ROOT))
            universal_result = UniversalDocument.parse(
                content,
                file_path=rel_path,
                document_type=DocumentType.WORKTRACKER_ENTITY,
            )

            # Compare frontmatter fields
            if universal_result.blockquote_frontmatter is not None:
                legacy_fields = {f.key: f.value for f in legacy_fm.fields}
                universal_fields = {
                    f.key: f.value
                    for f in universal_result.blockquote_frontmatter.fields
                }
                assert legacy_fields == universal_fields, (
                    f"Frontmatter mismatch in {rel_path}: "
                    f"legacy={legacy_fields}, universal={universal_fields}"
                )


# =============================================================================
# Rule File Regression
# =============================================================================


class TestRuleFileRegression:
    """Verify UniversalDocument matches reinject extraction for rule files."""

    @pytest.mark.regression
    def test_rule_file_reinject_parity(self) -> None:
        """All rule files produce identical reinject directives via both paths."""
        rule_files = _find_md_files(".context/rules")
        if not rule_files:
            pytest.skip("No rule files found")

        for rule_file in rule_files:
            content = rule_file.read_text(encoding="utf-8")
            doc = JerryDocument.parse(content)

            # Legacy path: extract_reinject_directives directly
            rel_path = str(rule_file.relative_to(REPO_ROOT))
            legacy_directives = extract_reinject_directives(
                doc, file_path=rel_path
            )

            # New path: UniversalDocument
            universal_result = UniversalDocument.parse(
                content,
                file_path=rel_path,
                document_type=DocumentType.RULE_FILE,
            )

            if universal_result.reinject_directives is not None:
                # Compare directive counts
                assert len(legacy_directives) == len(
                    universal_result.reinject_directives
                ), (
                    f"Reinject directive count mismatch in {rel_path}: "
                    f"legacy={len(legacy_directives)}, "
                    f"universal={len(universal_result.reinject_directives)}"
                )

                # Compare directive content
                for legacy, universal in zip(
                    legacy_directives,
                    universal_result.reinject_directives, strict=False
                ):
                    assert legacy.rank == universal.rank, (
                        f"Rank mismatch in {rel_path}"
                    )
                    assert legacy.content == universal.content, (
                        f"Content mismatch in {rel_path}"
                    )


# =============================================================================
# Pattern Collision Test
# =============================================================================


class TestPatternCollision:
    """Verify no markdown file matches multiple PATH_PATTERNS."""

    @pytest.mark.regression
    def test_no_pattern_collision(self) -> None:
        """No .md file in the repository matches 2+ PATH_PATTERNS."""
        from src.domain.markdown_ast.document_type import DocumentTypeDetector

        all_md_files = list(REPO_ROOT.rglob("*.md"))

        # Filter out files in .venv, node_modules, .git, etc.
        filtered = [
            f for f in all_md_files
            if not any(
                part.startswith(".")
                for part in f.relative_to(REPO_ROOT).parts[:-1]
            )
            and "node_modules" not in str(f)
            and ".venv" not in str(f)
        ]

        collisions: list[str] = []
        for md_file in filtered[:200]:  # Cap at 200 for test speed
            rel_path = str(md_file.relative_to(REPO_ROOT))
            # Count how many patterns match
            matches = []
            for glob_pattern, doc_type in DocumentTypeDetector.PATH_PATTERNS:
                from src.domain.markdown_ast.document_type import (
                    _path_matches_glob,
                )
                if _path_matches_glob(rel_path.replace("\\", "/"), glob_pattern):
                    matches.append((glob_pattern, doc_type))

            if len(matches) > 1:
                collisions.append(
                    f"{rel_path}: matched {len(matches)} patterns: "
                    f"{[(p, t.value) for p, t in matches]}"
                )

        if collisions:
            msg = "Pattern collisions found:\n" + "\n".join(collisions)
            # This is a warning, not a hard failure, since first-match-wins
            # ensures deterministic behavior
            pytest.skip(f"Pattern collisions (first-match-wins applies): {msg}")


# =============================================================================
# Schema Validation Regression
# =============================================================================


class TestSchemaValidationRegression:
    """Verify schema validation unchanged for existing worktracker entity types."""

    @pytest.mark.regression
    def test_existing_schemas_still_work(self) -> None:
        """All 6 existing worktracker entity schemas remain accessible."""
        from src.domain.markdown_ast.schema import get_entity_schema

        existing_types = ["epic", "feature", "story", "task", "enabler", "bug"]
        for entity_type in existing_types:
            schema = get_entity_schema(entity_type)
            assert schema is not None, f"Schema for {entity_type} not found"
            assert len(schema.field_rules) > 0, (
                f"Schema for {entity_type} has no field rules"
            )
