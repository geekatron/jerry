"""
Integration Tests: File System Resolution

Tests that document references resolve to actual files on the filesystem.
These tests interact with the real filesystem.

Test Categories:
- Happy Path: All referenced files exist
- Edge Cases: File existence edge cases
- Negative: Missing or broken references
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest


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
# HAPPY PATH TESTS - Phase 7 Artifacts Exist
# =============================================================================

class TestPhase7ArtifactsExist:
    """Verify all Phase 7 artifacts exist on filesystem."""

    def test_e001_research_exists(self, proj_001_root: Path):
        """e-001 research document should exist."""
        path = proj_001_root / "research" / "PROJ-001-e-001-worktracker-proposal-extraction.md"
        assert path.exists(), f"Missing: {path}"
        assert path.is_file(), f"Not a file: {path}"

    def test_e002_research_exists(self, proj_001_root: Path):
        """e-002 research document should exist."""
        path = proj_001_root / "research" / "PROJ-001-e-002-plan-graph-model.md"
        assert path.exists(), f"Missing: {path}"

    def test_e003_research_exists(self, proj_001_root: Path):
        """e-003 research document should exist."""
        path = proj_001_root / "research" / "PROJ-001-e-003-revised-architecture-foundation.md"
        assert path.exists(), f"Missing: {path}"

    def test_e004_research_exists(self, proj_001_root: Path):
        """e-004 research document should exist."""
        path = proj_001_root / "research" / "PROJ-001-e-004-strategic-plan-v3.md"
        assert path.exists(), f"Missing: {path}"

    def test_e005_research_exists(self, proj_001_root: Path):
        """e-005 research document should exist."""
        path = proj_001_root / "research" / "PROJ-001-e-005-industry-best-practices.md"
        assert path.exists(), f"Missing: {path}"

    def test_e006_synthesis_exists(self, proj_001_root: Path):
        """e-006 synthesis document should exist."""
        path = proj_001_root / "synthesis" / "PROJ-001-e-006-unified-architecture-canon.md"
        assert path.exists(), f"Missing: {path}"

    def test_e007_analysis_exists(self, proj_001_root: Path):
        """e-007 analysis document should exist."""
        path = proj_001_root / "analysis" / "PROJ-001-e-007-implementation-gap-analysis.md"
        assert path.exists(), f"Missing: {path}"

    def test_e009_analysis_exists(self, proj_001_root: Path):
        """e-009 analysis document should exist."""
        path = proj_001_root / "analysis" / "PROJ-001-e-009-alignment-validation.md"
        assert path.exists(), f"Missing: {path}"

    def test_e010_report_exists(self, proj_001_root: Path):
        """e-010 report document should exist."""
        path = proj_001_root / "reports" / "PROJ-001-e-010-synthesis-status-report.md"
        assert path.exists(), f"Missing: {path}"

    def test_adr_impl_001_exists(self, proj_001_root: Path):
        """ADR-IMPL-001 decisions document should exist."""
        path = proj_001_root / "decisions" / "ADR-IMPL-001-unified-alignment.md"
        assert path.exists(), f"Missing: {path}"


# =============================================================================
# HAPPY PATH TESTS - References Resolve
# =============================================================================

class TestReferencesResolve:
    """Verify document cross-references resolve to existing files."""

    def test_e006_references_resolve(self, proj_001_root: Path, project_root: Path):
        """All references in e-006 should resolve to existing files."""
        doc_path = proj_001_root / "synthesis" / "PROJ-001-e-006-unified-architecture-canon.md"
        content = doc_path.read_text()

        paths = extract_markdown_paths(content)
        project_paths = [p for p in paths if p.startswith("projects/PROJ-001")]

        for ref in project_paths:
            resolved = resolve_path(ref, project_root)
            assert resolved is not None, f"Could not resolve: {ref}"
            assert resolved.exists(), f"Reference does not exist: {ref} -> {resolved}"

    def test_e007_references_resolve(self, proj_001_root: Path, project_root: Path):
        """All references in e-007 should resolve to existing files."""
        doc_path = proj_001_root / "analysis" / "PROJ-001-e-007-implementation-gap-analysis.md"
        content = doc_path.read_text()

        paths = extract_markdown_paths(content)
        project_paths = [p for p in paths if p.startswith("projects/PROJ-001")]

        for ref in project_paths:
            resolved = resolve_path(ref, project_root)
            assert resolved is not None, f"Could not resolve: {ref}"
            assert resolved.exists(), f"Reference does not exist: {ref} -> {resolved}"

    def test_e009_references_resolve(self, proj_001_root: Path, project_root: Path):
        """All references in e-009 should resolve to existing files."""
        doc_path = proj_001_root / "analysis" / "PROJ-001-e-009-alignment-validation.md"
        content = doc_path.read_text()

        paths = extract_markdown_paths(content)
        project_paths = [p for p in paths if p.startswith("projects/PROJ-001")]

        for ref in project_paths:
            resolved = resolve_path(ref, project_root)
            assert resolved is not None, f"Could not resolve: {ref}"
            assert resolved.exists(), f"Reference does not exist: {ref} -> {resolved}"

    def test_e010_references_resolve(self, proj_001_root: Path, project_root: Path):
        """All references in e-010 should resolve to existing files."""
        doc_path = proj_001_root / "reports" / "PROJ-001-e-010-synthesis-status-report.md"
        content = doc_path.read_text()

        paths = extract_markdown_paths(content)
        project_paths = [p for p in paths if p.startswith("projects/PROJ-001")]

        for ref in project_paths:
            resolved = resolve_path(ref, project_root)
            assert resolved is not None, f"Could not resolve: {ref}"
            assert resolved.exists(), f"Reference does not exist: {ref} -> {resolved}"


# =============================================================================
# EDGE CASE TESTS
# =============================================================================

class TestEdgeCases:
    """Tests for edge cases in file resolution."""

    def test_worktracker_exists(self, proj_001_root: Path):
        """WORKTRACKER.md should exist."""
        path = proj_001_root / "WORKTRACKER.md"
        assert path.exists(), f"Missing WORKTRACKER.md: {path}"

    def test_plan_exists(self, proj_001_root: Path):
        """PLAN.md should exist."""
        path = proj_001_root / "PLAN.md"
        assert path.exists(), f"Missing PLAN.md: {path}"

    def test_bug_analysis_exists(self, proj_001_root: Path):
        """Bug analysis document should exist."""
        path = proj_001_root / "analysis" / "PROJ-001-BUG-ANALYSIS-5W1H-NASA-SE.md"
        assert path.exists(), f"Missing bug analysis: {path}"

    def test_directory_structure_complete(self, proj_001_root: Path):
        """All required directories should exist."""
        required_dirs = ["research", "synthesis", "analysis", "decisions", "reports", "design"]
        for dir_name in required_dirs:
            dir_path = proj_001_root / dir_name
            assert dir_path.exists(), f"Missing directory: {dir_path}"
            assert dir_path.is_dir(), f"Not a directory: {dir_path}"


# =============================================================================
# NEGATIVE TESTS
# =============================================================================

class TestNegativeCases:
    """Tests that verify old paths do NOT exist (proving migration)."""

    def test_old_docs_research_does_not_exist(self, project_root: Path):
        """Old docs/research/PROJ-001-* files should NOT exist."""
        old_path = project_root / "docs" / "research"
        if old_path.exists():
            proj_files = list(old_path.glob("PROJ-001-*.md"))
            assert len(proj_files) == 0, f"Old research files still exist: {proj_files}"

    def test_old_docs_synthesis_does_not_exist(self, project_root: Path):
        """Old docs/synthesis/PROJ-001-* files should NOT exist."""
        old_path = project_root / "docs" / "synthesis"
        if old_path.exists():
            proj_files = list(old_path.glob("PROJ-001-*.md"))
            assert len(proj_files) == 0, f"Old synthesis files still exist: {proj_files}"

    def test_old_docs_analysis_does_not_exist(self, project_root: Path):
        """Old docs/analysis/PROJ-001-* files should NOT exist."""
        old_path = project_root / "docs" / "analysis"
        if old_path.exists():
            proj_files = list(old_path.glob("PROJ-001-*.md"))
            assert len(proj_files) == 0, f"Old analysis files still exist: {proj_files}"

    def test_old_docs_decisions_does_not_exist(self, project_root: Path):
        """Old docs/decisions/PROJ-001-* or ADR-IMPL-001* files should NOT exist."""
        old_path = project_root / "docs" / "decisions"
        if old_path.exists():
            proj_files = list(old_path.glob("PROJ-001-*.md"))
            adr_files = list(old_path.glob("ADR-IMPL-001*.md"))
            all_files = proj_files + adr_files
            assert len(all_files) == 0, f"Old decisions files still exist: {all_files}"
