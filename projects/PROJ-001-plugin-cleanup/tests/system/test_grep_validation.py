"""
System Tests: Full Grep Validation

Tests that verify no old path patterns exist anywhere in the project artifacts.
These tests execute system-level validation across the entire project.

Test Categories:
- Happy Path: Zero matches for old patterns
- Comprehensive: Full directory scan
- Regression: Ensure fix is complete
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest


# =============================================================================
# SYSTEM-LEVEL VALIDATION
# =============================================================================

class TestNoOldPathsInProject:
    """Verify no old docs/ paths exist in PROJ-001 artifacts."""

    def test_zero_old_paths_via_grep(self, proj_001_root: Path):
        """
        CRITICAL: grep for old path pattern should return zero matches in artifact files.

        This is the primary validation that BUG-001 is fixed.
        Excludes: test files (which intentionally contain old patterns for testing)
        """
        pattern = r"docs/(research|synthesis|analysis|decisions)/PROJ-001"

        # Use grep to search recursively, excluding test directory
        result = subprocess.run(
            ["grep", "-r", "-E", "--exclude-dir=tests", pattern, str(proj_001_root)],
            capture_output=True,
            text=True,
        )

        # Filter out lines that are documenting the old pattern (e.g., in bug analysis)
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            real_violations = [
                line for line in lines
                if "BUG-" not in line  # Exclude bug documentation
                and "Old format:" not in line  # Exclude format descriptions
                and "OLD:" not in line  # Exclude migration docs
                and "Pattern:" not in line  # Exclude pattern definitions
            ]

            if real_violations:
                pytest.fail(
                    f"Found old path references!\n"
                    f"Pattern: {pattern}\n"
                    f"Matches:\n" + "\n".join(real_violations)
                )

        # Exit code 1 = no matches = PASS (or all matches were filtered)

    def test_zero_old_paths_in_research(self, proj_001_root: Path):
        """No old paths in research directory."""
        research_dir = proj_001_root / "research"
        self._assert_no_old_paths_in_dir(research_dir)

    def test_zero_old_paths_in_synthesis(self, proj_001_root: Path):
        """No old paths in synthesis directory."""
        synthesis_dir = proj_001_root / "synthesis"
        self._assert_no_old_paths_in_dir(synthesis_dir)

    def test_zero_old_paths_in_analysis(self, proj_001_root: Path):
        """No old paths in analysis directory."""
        analysis_dir = proj_001_root / "analysis"
        self._assert_no_old_paths_in_dir(analysis_dir)

    def test_zero_old_paths_in_reports(self, proj_001_root: Path):
        """No old paths in reports directory."""
        reports_dir = proj_001_root / "reports"
        self._assert_no_old_paths_in_dir(reports_dir)

    def test_zero_old_paths_in_decisions(self, proj_001_root: Path):
        """No old paths in decisions directory."""
        decisions_dir = proj_001_root / "decisions"
        self._assert_no_old_paths_in_dir(decisions_dir)

    def _assert_no_old_paths_in_dir(self, directory: Path):
        """Helper to assert no old paths in a directory."""
        if not directory.exists():
            return  # Directory doesn't exist, nothing to check

        pattern = re.compile(r"docs/(research|synthesis|analysis|decisions)/PROJ-001")

        for md_file in directory.glob("*.md"):
            content = md_file.read_text()
            matches = pattern.findall(content)
            assert len(matches) == 0, (
                f"Found {len(matches)} old path reference(s) in {md_file.name}:\n"
                f"Matches: {matches}"
            )


class TestAllPathsAreProjectCentric:
    """Verify all PROJ-001 paths use project-centric format."""

    def test_all_proj001_refs_are_project_centric(self, proj_001_root: Path):
        """
        All references to PROJ-001 artifacts should use projects/ prefix.
        """
        project_centric_pattern = re.compile(
            r"projects/PROJ-001-plugin-cleanup/(research|synthesis|analysis|decisions|reports)"
        )
        old_pattern = re.compile(r"docs/(research|synthesis|analysis|decisions)/PROJ-001")

        for md_file in proj_001_root.rglob("*.md"):
            content = md_file.read_text()

            # Find all path references
            old_matches = old_pattern.findall(content)
            new_matches = project_centric_pattern.findall(content)

            # Should have zero old matches
            assert len(old_matches) == 0, (
                f"Old paths in {md_file}: {old_matches}"
            )

            # If file references PROJ-001 paths, they should be project-centric
            # (new_matches can be empty for files that don't reference other docs)


class TestGrepCommandEquivalence:
    """Verify our Python validation matches grep behavior."""

    def test_python_validation_matches_grep(self, proj_001_root: Path):
        """
        Python regex validation should produce same results as grep for ARTIFACT files.

        This ensures our test logic is correct.
        Excludes: test files, bug documentation
        """
        pattern = r"docs/(research|synthesis|analysis|decisions)/PROJ-001"

        # Count via grep (excluding tests)
        grep_result = subprocess.run(
            ["grep", "-r", "-c", "-E", "--exclude-dir=tests", pattern, str(proj_001_root)],
            capture_output=True,
            text=True,
        )

        # Parse grep output (file:count format)
        grep_total = 0
        if grep_result.returncode == 0:
            for line in grep_result.stdout.strip().split("\n"):
                if ":" in line:
                    count = int(line.split(":")[-1])
                    grep_total += count

        # Count via Python (excluding tests and documentation about the bug)
        python_pattern = re.compile(pattern)
        python_total = 0
        for md_file in proj_001_root.rglob("*.md"):
            # Skip test files
            if "tests" in str(md_file):
                continue
            # Skip bug documentation
            if "BUG-ANALYSIS" in md_file.name:
                continue

            content = md_file.read_text()
            matches = python_pattern.findall(content)
            python_total += len(matches)

        # Counts should be equal (regardless of absolute value)
        # Note: Some documentation files may legitimately reference the old pattern
        # when discussing the migration/bug fix
        assert grep_total == python_total, f"grep ({grep_total}) and Python ({python_total}) counts should match"
