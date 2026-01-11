"""
System Tests: Full Grep Validation

Tests that verify no old path patterns exist anywhere in the project artifacts.
These tests execute system-level validation across the entire project.

Test Categories:
- Happy Path: Zero matches for old patterns
- Comprehensive: Full directory scan
- Regression: Ensure fix is complete

Migration History:
    Originally: projects/PROJ-001-plugin-cleanup/tests/system/test_grep_validation.py
    Migrated: 2026-01-10 (TD-005)
    Commit: a911859 (original creation for BUG-001)
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
    """Verify no old docs/ paths exist in project artifacts."""

    def test_zero_old_paths_via_grep(self, proj_root: Path, project_id: str) -> None:
        """
        CRITICAL: grep for old path pattern should return zero matches in artifact files.

        This is the primary validation that BUG-001-like issues are prevented.
        Excludes: test files (which intentionally contain old patterns for testing)
        """
        proj_num = project_id.split("-")[1]
        pattern = rf"docs/(research|synthesis|analysis|decisions)/PROJ-{proj_num}"

        # Use grep to search recursively, excluding test directory
        result = subprocess.run(
            ["grep", "-r", "-E", "--exclude-dir=tests", pattern, str(proj_root)],
            capture_output=True,
            text=True,
        )

        # Filter out lines that are documenting the old pattern (e.g., in bug analysis)
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            real_violations = [
                line
                for line in lines
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

    def test_zero_old_paths_in_research(self, proj_root: Path, project_id: str) -> None:
        """No old paths in research directory."""
        research_dir = proj_root / "research"
        self._assert_no_old_paths_in_dir(research_dir, project_id)

    def test_zero_old_paths_in_synthesis(self, proj_root: Path, project_id: str) -> None:
        """No old paths in synthesis directory."""
        synthesis_dir = proj_root / "synthesis"
        self._assert_no_old_paths_in_dir(synthesis_dir, project_id)

    def test_zero_old_paths_in_analysis(self, proj_root: Path, project_id: str) -> None:
        """No old paths in analysis directory."""
        analysis_dir = proj_root / "analysis"
        self._assert_no_old_paths_in_dir(analysis_dir, project_id)

    def test_zero_old_paths_in_reports(self, proj_root: Path, project_id: str) -> None:
        """No old paths in reports directory."""
        reports_dir = proj_root / "reports"
        self._assert_no_old_paths_in_dir(reports_dir, project_id)

    def test_zero_old_paths_in_decisions(self, proj_root: Path, project_id: str) -> None:
        """No old paths in decisions directory."""
        decisions_dir = proj_root / "decisions"
        self._assert_no_old_paths_in_dir(decisions_dir, project_id)

    def _assert_no_old_paths_in_dir(self, directory: Path, project_id: str) -> None:
        """Helper to assert no old paths in a directory."""
        if not directory.exists():
            return  # Directory doesn't exist, nothing to check

        proj_num = project_id.split("-")[1]
        pattern = re.compile(rf"docs/(research|synthesis|analysis|decisions)/PROJ-{proj_num}")

        for md_file in directory.glob("*.md"):
            content = md_file.read_text()
            matches = pattern.findall(content)
            assert len(matches) == 0, (
                f"Found {len(matches)} old path reference(s) in {md_file.name}:\nMatches: {matches}"
            )


class TestAllPathsAreProjectCentric:
    """Verify all project paths use project-centric format."""

    def test_all_project_refs_are_project_centric(
        self,
        proj_root: Path,
        project_id: str,
    ) -> None:
        """
        All references to project artifacts should use projects/ prefix.
        """
        proj_num = project_id.split("-")[1]
        project_centric_pattern = re.compile(
            rf"projects/PROJ-{proj_num}-[a-z0-9-]+/(research|synthesis|analysis|decisions|reports)"
        )
        old_pattern = re.compile(rf"docs/(research|synthesis|analysis|decisions)/PROJ-{proj_num}")

        for md_file in proj_root.rglob("*.md"):
            # Skip test files
            if "tests" in str(md_file):
                continue

            content = md_file.read_text()

            # Find all path references
            old_matches = old_pattern.findall(content)

            # Should have zero old matches
            assert len(old_matches) == 0, f"Old paths in {md_file}: {old_matches}"


class TestGrepCommandEquivalence:
    """Verify our Python validation matches grep behavior."""

    def test_python_validation_matches_grep(self, proj_root: Path, project_id: str) -> None:
        """
        Python regex validation should produce same results as grep for ARTIFACT files.

        This ensures our test logic is correct.
        Excludes: test files, bug documentation
        """
        proj_num = project_id.split("-")[1]
        pattern = rf"docs/(research|synthesis|analysis|decisions)/PROJ-{proj_num}"

        # Count via grep (excluding tests)
        grep_result = subprocess.run(
            ["grep", "-r", "-c", "-E", "--exclude-dir=tests", pattern, str(proj_root)],
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
        for md_file in proj_root.rglob("*.md"):
            # Skip test files
            if "tests" in str(md_file):
                continue
            # Skip bug documentation
            if "BUG-ANALYSIS" in md_file.name or "BUG-" in md_file.name:
                continue

            content = md_file.read_text()
            matches = python_pattern.findall(content)
            python_total += len(matches)

        # Counts should be equal
        assert grep_total == python_total, (
            f"grep ({grep_total}) and Python ({python_total}) counts should match"
        )
