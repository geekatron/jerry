"""
Architecture Tests: Path Convention Enforcement

Tests that verify architectural constraints around path conventions.
These tests enforce the project isolation principle (ADR-003).

Test Categories:
- Happy Path: Paths follow conventions
- Architectural Constraints: Layer boundaries respected
- Regression Prevention: Old patterns blocked

Migration History:
    Originally: projects/PROJ-001-plugin-cleanup/tests/architecture/test_path_conventions.py
    Migrated: 2026-01-10 (TD-005)
    Commit: a911859 (original creation for BUG-001)
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest


# =============================================================================
# ARCHITECTURE TESTS - PROJECT ISOLATION
# =============================================================================


class TestProjectIsolation:
    """Test that project isolation principle is enforced."""

    def test_all_project_artifacts_in_project_directory(
        self,
        proj_root: Path,
        project_root: Path,
        project_id: str,
    ) -> None:
        """
        ARCHITECTURE: All project artifacts must be in projects/{project_id}/.

        This enforces the project isolation principle from ADR-003.
        """
        # Extract project number from ID (e.g., "001" from "PROJ-001-plugin-cleanup")
        proj_num = project_id.split("-")[1]

        # Check that no project artifacts exist in docs/
        docs_dir = project_root / "docs"

        if docs_dir.exists():
            for category in ["research", "synthesis", "analysis", "decisions"]:
                category_dir = docs_dir / category
                if category_dir.exists():
                    proj_files = list(category_dir.glob(f"PROJ-{proj_num}-*.md"))
                    assert len(proj_files) == 0, (
                        f"Project artifacts found outside project directory: {proj_files}\n"
                        f"Architecture violation: Should be in projects/{project_id}/{category}/"
                    )

    def test_no_cross_project_references(self, proj_root: Path, project_id: str) -> None:
        """
        ARCHITECTURE: Project documents should not reference other project directories.

        This prevents coupling between projects.
        """
        # Get current project number
        proj_num = project_id.split("-")[1]

        # Pattern to find references to OTHER projects
        cross_ref_pattern = re.compile(rf"projects/PROJ-(?!{proj_num})\d{{3}}")

        for md_file in proj_root.rglob("*.md"):
            content = md_file.read_text()
            matches = cross_ref_pattern.findall(content)

            assert len(matches) == 0, (
                f"Cross-project reference found in {md_file.name}: {matches}\n"
                f"Architecture violation: Projects should be isolated"
            )

    def test_project_has_required_structure(self, proj_root: Path) -> None:
        """
        ARCHITECTURE: Project directory must have required structure.

        Required: PLAN.md, WORKTRACKER.md, and standard category directories.
        """
        # Required files
        required_files = ["PLAN.md", "WORKTRACKER.md"]
        for filename in required_files:
            file_path = proj_root / filename
            assert file_path.exists(), f"Missing required file: {filename}"

        # Required directories (at least some should exist)
        expected_dirs = ["research", "synthesis", "analysis", "decisions", "reports"]
        existing_dirs = [d for d in expected_dirs if (proj_root / d).exists()]

        assert len(existing_dirs) >= 3, (
            f"Project should have at least 3 category directories, found: {existing_dirs}"
        )


# =============================================================================
# ARCHITECTURE TESTS - NO DEPRECATED PATTERNS
# =============================================================================


class TestNoDeprecatedPatterns:
    """Test that deprecated architectural patterns are not used."""

    @pytest.mark.parametrize("pattern,message", [
        (r"docs/research/PROJ-", "Research should be in projects/{PROJ-ID}/research/"),
        (r"docs/synthesis/PROJ-", "Synthesis should be in projects/{PROJ-ID}/synthesis/"),
        (r"docs/analysis/PROJ-", "Analysis should be in projects/{PROJ-ID}/analysis/"),
        (r"docs/decisions/PROJ-", "Decisions should be in projects/{PROJ-ID}/decisions/"),
    ])
    def test_no_deprecated_pattern(
        self,
        proj_root: Path,
        pattern: str,
        message: str,
    ) -> None:
        """
        ARCHITECTURE: Deprecated path patterns should not appear in documents.
        """
        regex = re.compile(pattern)

        for md_file in proj_root.rglob("*.md"):
            # Skip test files and bug documentation
            if "tests" in str(md_file) or "BUG-" in md_file.name:
                continue

            content = md_file.read_text()
            matches = regex.findall(content)

            assert len(matches) == 0, (
                f"Deprecated pattern in {md_file.name}: {pattern}\n"
                f"Violation: {message}\n"
                f"Matches: {matches}"
            )

    def test_no_hardcoded_absolute_paths(self, proj_root: Path) -> None:
        """
        ARCHITECTURE: Documents should not contain hardcoded absolute paths.

        Paths should be relative to repository root.
        """
        absolute_path_pattern = re.compile(r"/Users/|/home/|C:\\|D:\\")

        for md_file in proj_root.rglob("*.md"):
            content = md_file.read_text()

            # Skip files with code blocks (which might contain examples)
            if "```" in content:
                continue

            matches = absolute_path_pattern.findall(content)

            assert len(matches) == 0, (
                f"Hardcoded absolute path in {md_file.name}: {matches}\n"
                f"Architecture violation: Use relative paths from repository root"
            )


# =============================================================================
# ARCHITECTURE TESTS - CATEGORY CONVENTIONS
# =============================================================================


class TestCategoryConventions:
    """Test that category directory conventions are followed."""

    def test_only_valid_categories_used(
        self,
        proj_root: Path,
        valid_categories: set[str],
    ) -> None:
        """
        ARCHITECTURE: Only valid category directories should exist.
        """
        # Also allow hidden directories and special directories
        allowed_extras = {"tests", ".jerry", "work"}
        all_allowed = valid_categories | allowed_extras

        for item in proj_root.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                assert item.name in all_allowed, (
                    f"Invalid category directory: {item.name}\n"
                    f"Valid categories: {valid_categories}"
                )

    def test_research_contains_extraction_docs(self, proj_root: Path) -> None:
        """
        ARCHITECTURE: Research directory should contain extraction documents.
        """
        research_dir = proj_root / "research"
        if research_dir.exists():
            extraction_docs = list(research_dir.glob("*extraction*.md"))
            # Only check if research dir has files
            if list(research_dir.glob("*.md")):
                assert len(extraction_docs) >= 1, (
                    "Research directory should contain extraction documents"
                )

    def test_synthesis_contains_canon_doc(self, proj_root: Path) -> None:
        """
        ARCHITECTURE: Synthesis directory should contain canon/unified document.
        """
        synthesis_dir = proj_root / "synthesis"
        if synthesis_dir.exists():
            canon_docs = list(synthesis_dir.glob("*canon*.md")) + list(synthesis_dir.glob("*unified*.md"))
            # Only check if synthesis dir has files
            if list(synthesis_dir.glob("*.md")):
                assert len(canon_docs) >= 1, (
                    "Synthesis directory should contain canon/unified document"
                )

    def test_decisions_contains_adr_docs(self, proj_root: Path) -> None:
        """
        ARCHITECTURE: Decisions directory should contain ADR documents.
        """
        decisions_dir = proj_root / "decisions"
        if decisions_dir.exists():
            adr_docs = list(decisions_dir.glob("ADR-*.md")) + list(decisions_dir.glob("*-adr-*.md"))
            # Only check if decisions dir has files
            if list(decisions_dir.glob("*.md")):
                assert len(adr_docs) >= 1, (
                    "Decisions directory should contain ADR documents"
                )


# =============================================================================
# ARCHITECTURE TESTS - REGRESSION PREVENTION
# =============================================================================


class TestRegressionPrevention:
    """Tests specifically designed to prevent BUG-001 regression."""

    def test_bug001_fix_holds(self, proj_root: Path, project_id: str) -> None:
        """
        REGRESSION: BUG-001 fix must not regress.

        BUG-001: Phase 7 artifacts were referencing old docs/ paths.
        This test ensures the fix remains in place.
        """
        # Get project number for pattern
        proj_num = project_id.split("-")[1]
        bug001_pattern = re.compile(rf"docs/(research|synthesis|analysis|decisions)/PROJ-{proj_num}")

        # Check synthesis, analysis, reports directories
        for category in ["synthesis", "analysis", "reports"]:
            category_dir = proj_root / category
            if not category_dir.exists():
                continue

            for file_path in category_dir.glob("*.md"):
                content = file_path.read_text()
                matches = bug001_pattern.findall(content)

                assert len(matches) == 0, (
                    f"BUG-001 REGRESSION in {file_path.name}!\n"
                    f"Found old docs/ path references: {matches}\n"
                    f"This was fixed. DO NOT REINTRODUCE."
                )

    def test_new_documents_use_correct_paths(self, proj_root: Path) -> None:
        """
        REGRESSION: New documents must use project-centric paths from the start.

        Any document created after BUG-001 fix should not contain old patterns.
        """
        old_pattern = re.compile(r"docs/(research|synthesis|analysis|decisions)/PROJ-")

        # Check all markdown files
        for md_file in proj_root.rglob("*.md"):
            # Skip test files and bug documentation
            if "tests" in str(md_file) or "BUG-" in md_file.name:
                continue

            content = md_file.read_text()
            matches = old_pattern.findall(content)

            assert len(matches) == 0, (
                f"Document {md_file.name} uses old path convention!\n"
                f"Matches: {matches}\n"
                f"Use: projects/{{PROJ-ID}}/{{category}}/ instead"
            )
