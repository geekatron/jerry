# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Integration Tests: File System Resolution

Tests that document references resolve to actual files on the filesystem.
These tests interact with the real filesystem.

Test Categories:
- Happy Path: All referenced files exist
- Edge Cases: File existence edge cases
- Negative: Missing or broken references

Migration History:
    Originally: projects/PROJ-001-plugin-cleanup/tests/integration/test_file_resolution.py
    Migrated: 2026-01-10 (TD-005)
    Commit: a911859 (original creation for BUG-001)
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from tests.project_validation.conftest import REQUIRED_PROJECT_DIRS

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


def extract_markdown_paths(content: str) -> list[str]:
    """Extract all markdown file references from content."""
    # Match paths in backticks that end in .md
    pattern = r"`([^`]*\.md)`"
    matches = re.findall(pattern, content)
    return [m for m in matches if "/" in m]  # Only paths, not filenames


def resolve_path(reference: str, project_root: Path) -> Path | None:
    """Resolve a document reference to an absolute path."""
    # Handle both relative and absolute-style paths
    if reference.startswith("projects/"):
        return project_root / reference
    elif reference.startswith("docs/"):
        return project_root / reference
    return None


# =============================================================================
# HAPPY PATH TESTS - Core Files Exist
# =============================================================================


class TestCoreFilesExist:
    """Verify core project files exist on filesystem."""

    def test_worktracker_exists(self, proj_root: Path) -> None:
        """WORKTRACKER.md should exist."""
        path = proj_root / "WORKTRACKER.md"
        assert path.exists(), f"Missing WORKTRACKER.md: {path}"

    def test_plan_exists(self, proj_root: Path) -> None:
        """PLAN.md should exist."""
        path = proj_root / "PLAN.md"
        assert path.exists(), f"Missing PLAN.md: {path}"

    def test_directory_structure_complete(self, proj_root: Path) -> None:
        """Required directories should exist per worktracker spec."""
        for dirname in REQUIRED_PROJECT_DIRS:
            dir_path = proj_root / dirname
            assert dir_path.exists(), (
                f"Missing required directory: {dirname} in {proj_root.name}. "
                f"Per worktracker-directory-structure.md, work/ is required. "
                f"Create it with: mkdir {proj_root}/{dirname}"
            )


# =============================================================================
# HAPPY PATH TESTS - Research Documents
# =============================================================================


class TestResearchDocumentsExist:
    """Verify research documents exist on filesystem."""

    def test_research_directory_has_documents(self, proj_root: Path) -> None:
        """Research directory should contain at least one document."""
        research_dir = proj_root / "research"
        if research_dir.exists():
            docs = list(research_dir.glob("*.md"))
            assert len(docs) >= 1, "Research directory should contain documents"

    def test_research_documents_are_readable(self, proj_root: Path) -> None:
        """All research documents should be readable."""
        research_dir = proj_root / "research"
        if not research_dir.exists():
            pytest.skip("No research directory")

        for doc in research_dir.glob("*.md"):
            content = doc.read_text()
            assert len(content) > 0, f"Research document is empty: {doc.name}"


# =============================================================================
# HAPPY PATH TESTS - Reference Resolution
# =============================================================================


class TestReferencesResolve:
    """Verify document cross-references resolve to existing files."""

    def test_synthesis_references_resolve(
        self,
        proj_root: Path,
        project_root: Path,
        project_id: str,
    ) -> None:
        """All references in synthesis documents should resolve to existing files."""
        synthesis_dir = proj_root / "synthesis"
        if not synthesis_dir.exists():
            pytest.skip("No synthesis directory")

        for doc_path in synthesis_dir.glob("*.md"):
            content = doc_path.read_text()
            paths = extract_markdown_paths(content)
            project_paths = [p for p in paths if p.startswith(f"projects/{project_id}")]

            for ref in project_paths:
                resolved = resolve_path(ref, project_root)
                assert resolved is not None, f"Could not resolve: {ref}"
                assert resolved.exists(), f"Reference does not exist: {ref} -> {resolved}"

    def test_analysis_references_resolve(
        self,
        proj_root: Path,
        project_root: Path,
        project_id: str,
    ) -> None:
        """All references in analysis documents should resolve to existing files."""
        analysis_dir = proj_root / "analysis"
        if not analysis_dir.exists():
            pytest.skip("No analysis directory")

        for doc_path in analysis_dir.glob("*.md"):
            content = doc_path.read_text()
            paths = extract_markdown_paths(content)
            project_paths = [p for p in paths if p.startswith(f"projects/{project_id}")]

            for ref in project_paths:
                resolved = resolve_path(ref, project_root)
                assert resolved is not None, f"Could not resolve: {ref}"
                assert resolved.exists(), f"Reference does not exist: {ref} -> {resolved}"


# =============================================================================
# NEGATIVE TESTS
# =============================================================================


class TestNegativeCases:
    """Tests that verify old paths do NOT exist (proving migration)."""

    def test_old_docs_research_does_not_exist(
        self,
        project_root: Path,
        project_id: str,
    ) -> None:
        """Old docs/research/PROJ-* files should NOT exist."""
        proj_num = project_id.split("-")[1]
        old_path = project_root / "docs" / "research"
        if old_path.exists():
            proj_files = list(old_path.glob(f"PROJ-{proj_num}-*.md"))
            assert len(proj_files) == 0, f"Old research files still exist: {proj_files}"

    def test_old_docs_synthesis_does_not_exist(
        self,
        project_root: Path,
        project_id: str,
    ) -> None:
        """Old docs/synthesis/PROJ-* files should NOT exist."""
        proj_num = project_id.split("-")[1]
        old_path = project_root / "docs" / "synthesis"
        if old_path.exists():
            proj_files = list(old_path.glob(f"PROJ-{proj_num}-*.md"))
            assert len(proj_files) == 0, f"Old synthesis files still exist: {proj_files}"

    def test_old_docs_analysis_does_not_exist(
        self,
        project_root: Path,
        project_id: str,
    ) -> None:
        """Old docs/analysis/PROJ-* files should NOT exist."""
        proj_num = project_id.split("-")[1]
        old_path = project_root / "docs" / "analysis"
        if old_path.exists():
            proj_files = list(old_path.glob(f"PROJ-{proj_num}-*.md"))
            assert len(proj_files) == 0, f"Old analysis files still exist: {proj_files}"

    def test_old_docs_decisions_does_not_exist(
        self,
        project_root: Path,
        project_id: str,
    ) -> None:
        """Old docs/decisions/PROJ-* files should NOT exist."""
        proj_num = project_id.split("-")[1]
        old_path = project_root / "docs" / "decisions"
        if old_path.exists():
            proj_files = list(old_path.glob(f"PROJ-{proj_num}-*.md"))
            adr_files = list(old_path.glob(f"ADR-IMPL-{proj_num}*.md"))
            all_files = proj_files + adr_files
            assert len(all_files) == 0, f"Old decisions files still exist: {all_files}"
