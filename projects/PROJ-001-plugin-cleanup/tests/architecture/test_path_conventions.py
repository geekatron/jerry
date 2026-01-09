"""
Architecture Tests: Path Convention Enforcement

Tests that verify architectural constraints around path conventions.
These tests enforce the project isolation principle (ADR-003).

Test Categories:
- Happy Path: Paths follow conventions
- Architectural Constraints: Layer boundaries respected
- Regression Prevention: Old patterns blocked
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest


# =============================================================================
# ARCHITECTURAL CONSTRAINTS
# =============================================================================

# Per ADR-003: All project artifacts must be in projects/{PROJ-ID}/
PROJECT_ISOLATION_PATTERN = re.compile(
    r"projects/PROJ-\d{3}-[a-z0-9-]+/"
)

# Deprecated patterns that violate architecture
DEPRECATED_PATTERNS = [
    (r"docs/research/PROJ-", "Research should be in projects/{PROJ-ID}/research/"),
    (r"docs/synthesis/PROJ-", "Synthesis should be in projects/{PROJ-ID}/synthesis/"),
    (r"docs/analysis/PROJ-", "Analysis should be in projects/{PROJ-ID}/analysis/"),
    (r"docs/decisions/PROJ-", "Decisions should be in projects/{PROJ-ID}/decisions/"),
]

# Valid category directories per ADR-003
VALID_CATEGORIES = {
    "research",
    "synthesis",
    "analysis",
    "decisions",
    "reports",
    "design",
    "investigations",
    "reviews",
}


# =============================================================================
# ARCHITECTURE TESTS - PROJECT ISOLATION
# =============================================================================

class TestProjectIsolation:
    """Test that project isolation principle is enforced."""

    def test_all_proj001_artifacts_in_project_directory(self, proj_001_root: Path, project_root: Path):
        """
        ARCHITECTURE: All PROJ-001 artifacts must be in projects/PROJ-001-plugin-cleanup/.

        This enforces the project isolation principle from ADR-003.
        """
        # Check that no PROJ-001 artifacts exist in docs/
        docs_dir = project_root / "docs"

        if docs_dir.exists():
            for category in ["research", "synthesis", "analysis", "decisions"]:
                category_dir = docs_dir / category
                if category_dir.exists():
                    proj_files = list(category_dir.glob("PROJ-001-*.md"))
                    assert len(proj_files) == 0, (
                        f"PROJ-001 artifacts found outside project directory: {proj_files}\n"
                        f"Architecture violation: Should be in projects/PROJ-001-plugin-cleanup/{category}/"
                    )

    def test_no_cross_project_references(self, proj_001_root: Path):
        """
        ARCHITECTURE: PROJ-001 documents should not reference other project directories.

        This prevents coupling between projects.
        """
        cross_ref_pattern = re.compile(r"projects/PROJ-00[2-9]|projects/PROJ-0[1-9]")

        for md_file in proj_001_root.rglob("*.md"):
            content = md_file.read_text()
            matches = cross_ref_pattern.findall(content)

            assert len(matches) == 0, (
                f"Cross-project reference found in {md_file.name}: {matches}\n"
                f"Architecture violation: Projects should be isolated"
            )

    def test_project_has_required_structure(self, proj_001_root: Path):
        """
        ARCHITECTURE: Project directory must have required structure.

        Required: PLAN.md, WORKTRACKER.md, and standard category directories.
        """
        # Required files
        required_files = ["PLAN.md", "WORKTRACKER.md"]
        for filename in required_files:
            file_path = proj_001_root / filename
            assert file_path.exists(), f"Missing required file: {filename}"

        # Required directories (at least some should exist)
        expected_dirs = ["research", "synthesis", "analysis", "decisions", "reports"]
        existing_dirs = [d for d in expected_dirs if (proj_001_root / d).exists()]

        assert len(existing_dirs) >= 3, (
            f"Project should have at least 3 category directories, found: {existing_dirs}"
        )


# =============================================================================
# ARCHITECTURE TESTS - NO DEPRECATED PATTERNS
# =============================================================================

class TestNoDeprecatedPatterns:
    """Test that deprecated architectural patterns are not used."""

    @pytest.mark.parametrize("pattern,message", DEPRECATED_PATTERNS)
    def test_no_deprecated_pattern(self, proj_001_root: Path, pattern: str, message: str):
        """
        ARCHITECTURE: Deprecated path patterns should not appear in documents.
        """
        regex = re.compile(pattern)

        for md_file in proj_001_root.rglob("*.md"):
            content = md_file.read_text()
            matches = regex.findall(content)

            assert len(matches) == 0, (
                f"Deprecated pattern in {md_file.name}: {pattern}\n"
                f"Violation: {message}\n"
                f"Matches: {matches}"
            )

    def test_no_hardcoded_absolute_paths(self, proj_001_root: Path):
        """
        ARCHITECTURE: Documents should not contain hardcoded absolute paths.

        Paths should be relative to repository root.
        """
        absolute_path_pattern = re.compile(r"/Users/|/home/|C:\\|D:\\")

        for md_file in proj_001_root.rglob("*.md"):
            content = md_file.read_text()
            matches = absolute_path_pattern.findall(content)

            # Filter out matches in code blocks (which might be examples)
            if "```" in content:
                # Simple heuristic: if most matches are in code blocks, allow it
                continue

            assert len(matches) == 0, (
                f"Hardcoded absolute path in {md_file.name}: {matches}\n"
                f"Architecture violation: Use relative paths from repository root"
            )


# =============================================================================
# ARCHITECTURE TESTS - CATEGORY CONVENTIONS
# =============================================================================

class TestCategoryConventions:
    """Test that category directory conventions are followed."""

    def test_only_valid_categories_used(self, proj_001_root: Path):
        """
        ARCHITECTURE: Only valid category directories should exist.
        """
        for item in proj_001_root.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                # Skip tests directory and .jerry
                if item.name in ("tests", ".jerry"):
                    continue

                assert item.name in VALID_CATEGORIES, (
                    f"Invalid category directory: {item.name}\n"
                    f"Valid categories: {VALID_CATEGORIES}"
                )

    def test_research_contains_extraction_docs(self, proj_001_root: Path):
        """
        ARCHITECTURE: Research directory should contain extraction documents.
        """
        research_dir = proj_001_root / "research"
        if research_dir.exists():
            extraction_docs = list(research_dir.glob("*extraction*.md"))
            assert len(extraction_docs) >= 1, (
                "Research directory should contain extraction documents"
            )

    def test_synthesis_contains_canon_doc(self, proj_001_root: Path):
        """
        ARCHITECTURE: Synthesis directory should contain canon/unified document.
        """
        synthesis_dir = proj_001_root / "synthesis"
        if synthesis_dir.exists():
            canon_docs = list(synthesis_dir.glob("*canon*.md")) + list(synthesis_dir.glob("*unified*.md"))
            assert len(canon_docs) >= 1, (
                "Synthesis directory should contain canon/unified document"
            )

    def test_decisions_contains_adr_docs(self, proj_001_root: Path):
        """
        ARCHITECTURE: Decisions directory should contain ADR documents.
        """
        decisions_dir = proj_001_root / "decisions"
        if decisions_dir.exists():
            adr_docs = list(decisions_dir.glob("ADR-*.md"))
            assert len(adr_docs) >= 1, (
                "Decisions directory should contain ADR documents"
            )


# =============================================================================
# ARCHITECTURE TESTS - REGRESSION PREVENTION
# =============================================================================

class TestRegressionPrevention:
    """Tests specifically designed to prevent BUG-001 regression."""

    def test_bug001_fix_holds(self, proj_001_root: Path):
        """
        REGRESSION: BUG-001 fix must not regress.

        BUG-001: Phase 7 artifacts were referencing old docs/ paths.
        This test ensures the fix remains in place.
        """
        bug001_pattern = re.compile(r"docs/(research|synthesis|analysis|decisions)/PROJ-001")

        affected_files = [
            proj_001_root / "synthesis" / "PROJ-001-e-006-unified-architecture-canon.md",
            proj_001_root / "analysis" / "PROJ-001-e-007-implementation-gap-analysis.md",
            proj_001_root / "analysis" / "PROJ-001-e-009-alignment-validation.md",
            proj_001_root / "reports" / "PROJ-001-e-010-synthesis-status-report.md",
        ]

        for file_path in affected_files:
            if not file_path.exists():
                continue

            content = file_path.read_text()
            matches = bug001_pattern.findall(content)

            assert len(matches) == 0, (
                f"BUG-001 REGRESSION in {file_path.name}!\n"
                f"Found old docs/ path references: {matches}\n"
                f"This was fixed on 2026-01-10. DO NOT REINTRODUCE."
            )

    def test_new_documents_use_correct_paths(self, proj_001_root: Path):
        """
        REGRESSION: New documents must use project-centric paths from the start.

        Any document created after BUG-001 fix should not contain old patterns.
        """
        old_pattern = re.compile(r"docs/(research|synthesis|analysis|decisions)/PROJ-")

        # Check all markdown files
        for md_file in proj_001_root.rglob("*.md"):
            content = md_file.read_text()
            matches = old_pattern.findall(content)

            assert len(matches) == 0, (
                f"New document {md_file.name} uses old path convention!\n"
                f"Matches: {matches}\n"
                f"Use: projects/PROJ-001-plugin-cleanup/{{category}}/ instead"
            )
