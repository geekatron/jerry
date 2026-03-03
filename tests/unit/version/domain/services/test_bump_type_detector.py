# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for BumpTypeDetector domain service.

Includes regression tests for the BUG-002 case sensitivity issue.

References:
    - BUG-002: Version bump regex rejects uppercase scopes
"""

from __future__ import annotations

import pytest

from src.version.domain.services.bump_type_detector import BumpTypeDetector
from src.version.domain.value_objects.bump_type import BumpType


@pytest.fixture()
def detector() -> BumpTypeDetector:
    """Create a fresh BumpTypeDetector instance."""
    return BumpTypeDetector()


class TestBumpTypeDetectorHappy:
    """Happy path tests for BumpTypeDetector."""

    @pytest.mark.happy_path
    def test_feat_returns_minor(self, detector: BumpTypeDetector) -> None:
        result = detector.detect(["feat: add feature"])
        assert result == BumpType.MINOR

    @pytest.mark.happy_path
    def test_fix_returns_patch(self, detector: BumpTypeDetector) -> None:
        result = detector.detect(["fix: fix bug"])
        assert result == BumpType.PATCH

    @pytest.mark.happy_path
    def test_perf_returns_patch(self, detector: BumpTypeDetector) -> None:
        result = detector.detect(["perf: optimize query"])
        assert result == BumpType.PATCH

    @pytest.mark.happy_path
    def test_breaking_returns_major(self, detector: BumpTypeDetector) -> None:
        result = detector.detect(["feat!: remove API"])
        assert result == BumpType.MAJOR

    @pytest.mark.happy_path
    def test_docs_returns_none(self, detector: BumpTypeDetector) -> None:
        result = detector.detect(["docs: update README"])
        assert result == BumpType.NONE

    @pytest.mark.happy_path
    def test_highest_severity_wins(self, detector: BumpTypeDetector) -> None:
        result = detector.detect(
            [
                "docs: update README",
                "fix: fix bug",
                "feat: add feature",
            ]
        )
        assert result == BumpType.MINOR

    @pytest.mark.happy_path
    def test_breaking_in_mixed_commits(self, detector: BumpTypeDetector) -> None:
        result = detector.detect(
            [
                "docs: update README",
                "fix: fix bug",
                "feat!: breaking change",
            ]
        )
        assert result == BumpType.MAJOR

    @pytest.mark.happy_path
    def test_single_commit_feat(self, detector: BumpTypeDetector) -> None:
        result = detector.detect(["feat(auth): add OAuth"])
        assert result == BumpType.MINOR

    @pytest.mark.happy_path
    def test_multiple_fixes_returns_patch(self, detector: BumpTypeDetector) -> None:
        result = detector.detect(
            [
                "fix: first fix",
                "fix: second fix",
            ]
        )
        assert result == BumpType.PATCH

    @pytest.mark.happy_path
    def test_feat_overrides_fix(self, detector: BumpTypeDetector) -> None:
        result = detector.detect(
            [
                "fix: fix bug",
                "feat: add feature",
            ]
        )
        assert result == BumpType.MINOR


class TestBumpTypeDetectorBUG002Regression:
    """Regression tests for BUG-002: case-insensitive detection."""

    @pytest.mark.happy_path
    def test_uppercase_scope_gh_122(self, detector: BumpTypeDetector) -> None:
        """THE BUG: feat(GH-122) was classified as 'none'."""
        result = detector.detect(["feat(GH-122): add version detection"])
        assert result == BumpType.MINOR

    @pytest.mark.happy_path
    def test_uppercase_type_feat(self, detector: BumpTypeDetector) -> None:
        result = detector.detect(["FEAT(scope): add feature"])
        assert result == BumpType.MINOR

    @pytest.mark.happy_path
    def test_mixed_case_fix(self, detector: BumpTypeDetector) -> None:
        result = detector.detect(["Fix(Mixed-CASE): fix something"])
        assert result == BumpType.PATCH

    @pytest.mark.happy_path
    def test_breaking_with_uppercase_scope(self, detector: BumpTypeDetector) -> None:
        result = detector.detect(["feat(GH-NNN)!: breaking change"])
        assert result == BumpType.MAJOR

    @pytest.mark.happy_path
    def test_all_uppercase(self, detector: BumpTypeDetector) -> None:
        result = detector.detect(["FIX(CI): fix pipeline"])
        assert result == BumpType.PATCH

    @pytest.mark.happy_path
    def test_uppercase_perf(self, detector: BumpTypeDetector) -> None:
        result = detector.detect(["PERF(DB): optimize"])
        assert result == BumpType.PATCH

    @pytest.mark.happy_path
    def test_mixed_case_subjects(self, detector: BumpTypeDetector) -> None:
        result = detector.detect(
            [
                "docs(GH-100): update docs",
                "feat(GH-122): add feature",
                "fix(GH-123): fix bug",
            ]
        )
        assert result == BumpType.MINOR

    @pytest.mark.happy_path
    def test_uppercase_breaking_overrides_all(self, detector: BumpTypeDetector) -> None:
        result = detector.detect(
            [
                "FEAT(GH-100): add feature",
                "FIX(GH-101)!: breaking fix",
            ]
        )
        assert result == BumpType.MAJOR


class TestBumpTypeDetectorBreakingChangeFooter:
    """Tests for BREAKING CHANGE footer detection."""

    @pytest.mark.happy_path
    def test_breaking_change_footer_in_body(self, detector: BumpTypeDetector) -> None:
        result = detector.detect(
            subjects=["fix: fix API"],
            bodies=["BREAKING CHANGE: removed old endpoint"],
        )
        assert result == BumpType.MAJOR

    @pytest.mark.happy_path
    def test_breaking_change_with_hyphen(self, detector: BumpTypeDetector) -> None:
        result = detector.detect(
            subjects=["fix: fix API"],
            bodies=["BREAKING-CHANGE: removed old endpoint"],
        )
        assert result == BumpType.MAJOR

    @pytest.mark.happy_path
    def test_breaking_change_lowercase(self, detector: BumpTypeDetector) -> None:
        result = detector.detect(
            subjects=["fix: fix API"],
            bodies=["breaking change: removed old endpoint"],
        )
        assert result == BumpType.MAJOR

    @pytest.mark.happy_path
    def test_no_breaking_change_footer(self, detector: BumpTypeDetector) -> None:
        result = detector.detect(
            subjects=["fix: fix API"],
            bodies=["This is a normal fix body."],
        )
        assert result == BumpType.PATCH

    @pytest.mark.happy_path
    def test_breaking_change_footer_not_at_start(self, detector: BumpTypeDetector) -> None:
        result = detector.detect(
            subjects=["fix: fix API"],
            bodies=["Some context.\n\nBREAKING CHANGE: removed old endpoint"],
        )
        assert result == BumpType.MAJOR


class TestBumpTypeDetectorNegative:
    """Negative tests for BumpTypeDetector."""

    @pytest.mark.negative
    def test_empty_subjects_returns_none(self, detector: BumpTypeDetector) -> None:
        result = detector.detect([])
        assert result == BumpType.NONE

    @pytest.mark.negative
    def test_non_conventional_commits_returns_none(self, detector: BumpTypeDetector) -> None:
        result = detector.detect(
            [
                "Merge pull request #123",
                "Update README.md",
                "v0.22.1",
            ]
        )
        assert result == BumpType.NONE

    @pytest.mark.negative
    def test_mixed_conventional_and_non_conventional(self, detector: BumpTypeDetector) -> None:
        result = detector.detect(
            [
                "Merge pull request #123",
                "feat: add feature",
                "Update README.md",
            ]
        )
        assert result == BumpType.MINOR

    @pytest.mark.negative
    def test_only_non_bump_types(self, detector: BumpTypeDetector) -> None:
        result = detector.detect(
            [
                "docs: update README",
                "chore: cleanup",
                "test: add tests",
                "ci: update workflow",
                "style: format code",
                "refactor: simplify",
            ]
        )
        assert result == BumpType.NONE

    @pytest.mark.negative
    def test_bodies_none_no_crash(self, detector: BumpTypeDetector) -> None:
        result = detector.detect(["fix: fix bug"], bodies=None)
        assert result == BumpType.PATCH

    @pytest.mark.negative
    def test_empty_bodies_list(self, detector: BumpTypeDetector) -> None:
        result = detector.detect(["fix: fix bug"], bodies=[])
        assert result == BumpType.PATCH


class TestBumpTypeDetectorEdgeCases:
    """Edge case tests for BumpTypeDetector."""

    @pytest.mark.edge_case
    def test_short_circuit_on_major(self, detector: BumpTypeDetector) -> None:
        """Major bump should short-circuit and not scan remaining commits."""
        result = detector.detect(
            [
                "feat!: breaking change",
                "feat: add feature",
                "fix: fix bug",
            ]
        )
        assert result == BumpType.MAJOR

    @pytest.mark.edge_case
    def test_single_commit_non_conventional(self, detector: BumpTypeDetector) -> None:
        result = detector.detect(["just a random message"])
        assert result == BumpType.NONE

    @pytest.mark.edge_case
    def test_skip_bump_commits(self, detector: BumpTypeDetector) -> None:
        """Commits with [skip-bump] are still parsed (filtering is CI's job)."""
        result = detector.detect(["feat(ci): add detection [skip-bump]"])
        assert result == BumpType.MINOR
