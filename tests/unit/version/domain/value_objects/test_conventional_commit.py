# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for ConventionalCommit value object.

These tests verify case-insensitive parsing — the core fix for BUG-002.

References:
    - BUG-002: Version bump regex rejects uppercase scopes
    - Conventional Commits v1.0.0 specification
"""

from __future__ import annotations

import pytest

from src.version.domain.exceptions import CommitParseError
from src.version.domain.value_objects.bump_type import BumpType
from src.version.domain.value_objects.conventional_commit import ConventionalCommit


class TestConventionalCommitParsing:
    """Tests for ConventionalCommit.parse() happy path."""

    @pytest.mark.happy_path
    def test_parse_feat_with_scope(self) -> None:
        commit = ConventionalCommit.parse("feat(auth): add login")
        assert commit.commit_type == "feat"
        assert commit.scope == "auth"
        assert commit.is_breaking is False
        assert commit.description == "add login"

    @pytest.mark.happy_path
    def test_parse_fix_without_scope(self) -> None:
        commit = ConventionalCommit.parse("fix: correct typo")
        assert commit.commit_type == "fix"
        assert commit.scope is None
        assert commit.is_breaking is False
        assert commit.description == "correct typo"

    @pytest.mark.happy_path
    def test_parse_feat_with_breaking_indicator(self) -> None:
        commit = ConventionalCommit.parse("feat!: remove deprecated API")
        assert commit.commit_type == "feat"
        assert commit.is_breaking is True
        assert commit.description == "remove deprecated API"

    @pytest.mark.happy_path
    def test_parse_feat_with_scope_and_breaking(self) -> None:
        commit = ConventionalCommit.parse("feat(api)!: remove endpoint")
        assert commit.commit_type == "feat"
        assert commit.scope == "api"
        assert commit.is_breaking is True

    @pytest.mark.happy_path
    def test_parse_docs_type(self) -> None:
        commit = ConventionalCommit.parse("docs: update README")
        assert commit.commit_type == "docs"
        assert commit.bump_type == BumpType.NONE

    @pytest.mark.happy_path
    def test_parse_perf_type(self) -> None:
        commit = ConventionalCommit.parse("perf(db): optimize query")
        assert commit.commit_type == "perf"
        assert commit.bump_type == BumpType.PATCH

    @pytest.mark.happy_path
    def test_parse_chore_type(self) -> None:
        commit = ConventionalCommit.parse("chore: update deps")
        assert commit.commit_type == "chore"
        assert commit.bump_type == BumpType.NONE

    @pytest.mark.happy_path
    def test_parse_refactor_type(self) -> None:
        commit = ConventionalCommit.parse("refactor(core): simplify logic")
        assert commit.commit_type == "refactor"
        assert commit.bump_type == BumpType.NONE

    @pytest.mark.happy_path
    def test_parse_test_type(self) -> None:
        commit = ConventionalCommit.parse("test: add unit tests")
        assert commit.commit_type == "test"
        assert commit.bump_type == BumpType.NONE

    @pytest.mark.happy_path
    def test_parse_ci_type(self) -> None:
        commit = ConventionalCommit.parse("ci(github): update workflow")
        assert commit.commit_type == "ci"
        assert commit.bump_type == BumpType.NONE

    @pytest.mark.happy_path
    def test_description_with_extra_whitespace(self) -> None:
        commit = ConventionalCommit.parse("feat:   add feature   ")
        assert commit.description == "add feature"

    @pytest.mark.happy_path
    def test_scope_with_hyphen(self) -> None:
        commit = ConventionalCommit.parse("feat(my-scope): add feature")
        assert commit.scope == "my-scope"

    @pytest.mark.happy_path
    def test_scope_with_underscore(self) -> None:
        commit = ConventionalCommit.parse("feat(my_scope): add feature")
        assert commit.scope == "my_scope"

    @pytest.mark.happy_path
    def test_scope_with_numbers(self) -> None:
        commit = ConventionalCommit.parse("feat(v2): add feature")
        assert commit.scope == "v2"

    @pytest.mark.happy_path
    def test_commit_type_stored_as_lowercase(self) -> None:
        commit = ConventionalCommit.parse("FEAT(scope): description")
        assert commit.commit_type == "feat"


class TestConventionalCommitCaseInsensitive:
    """Tests for case-insensitive parsing — THE BUG FIX for BUG-002."""

    @pytest.mark.happy_path
    def test_uppercase_scope_gh_nnn(self) -> None:
        """THE BUG: feat(GH-122) was classified as 'none' instead of 'minor'."""
        commit = ConventionalCommit.parse("feat(GH-122): add feature")
        assert commit.commit_type == "feat"
        assert commit.scope == "GH-122"
        assert commit.bump_type == BumpType.MINOR

    @pytest.mark.happy_path
    def test_uppercase_type_feat(self) -> None:
        commit = ConventionalCommit.parse("FEAT(scope): add feature")
        assert commit.commit_type == "feat"
        assert commit.bump_type == BumpType.MINOR

    @pytest.mark.happy_path
    def test_mixed_case_type(self) -> None:
        commit = ConventionalCommit.parse("Feat(scope): add feature")
        assert commit.commit_type == "feat"
        assert commit.bump_type == BumpType.MINOR

    @pytest.mark.happy_path
    def test_mixed_case_fix(self) -> None:
        commit = ConventionalCommit.parse("Fix(Mixed-CASE): fix something")
        assert commit.commit_type == "fix"
        assert commit.bump_type == BumpType.PATCH

    @pytest.mark.happy_path
    def test_uppercase_breaking_with_scope(self) -> None:
        commit = ConventionalCommit.parse("feat(GH-NNN)!: breaking change")
        assert commit.commit_type == "feat"
        assert commit.scope == "GH-NNN"
        assert commit.is_breaking is True
        assert commit.bump_type == BumpType.MAJOR

    @pytest.mark.happy_path
    def test_all_uppercase_type_and_scope(self) -> None:
        commit = ConventionalCommit.parse("FIX(CI): fix pipeline")
        assert commit.commit_type == "fix"
        assert commit.scope == "CI"
        assert commit.bump_type == BumpType.PATCH

    @pytest.mark.happy_path
    def test_uppercase_perf(self) -> None:
        commit = ConventionalCommit.parse("PERF(DB): optimize")
        assert commit.commit_type == "perf"
        assert commit.bump_type == BumpType.PATCH

    @pytest.mark.happy_path
    def test_scope_with_dots(self) -> None:
        commit = ConventionalCommit.parse("feat(v1.2.3): add feature")
        assert commit.scope == "v1.2.3"


class TestConventionalCommitNegative:
    """Tests for invalid commit subjects."""

    @pytest.mark.negative
    def test_empty_string_raises(self) -> None:
        with pytest.raises(CommitParseError, match="empty commit subject"):
            ConventionalCommit.parse("")

    @pytest.mark.negative
    def test_whitespace_only_raises(self) -> None:
        with pytest.raises(CommitParseError, match="empty commit subject"):
            ConventionalCommit.parse("   ")

    @pytest.mark.negative
    def test_no_colon_raises(self) -> None:
        with pytest.raises(CommitParseError, match="does not match"):
            ConventionalCommit.parse("feat add login")

    @pytest.mark.negative
    def test_no_type_raises(self) -> None:
        with pytest.raises(CommitParseError, match="does not match"):
            ConventionalCommit.parse(": add login")

    @pytest.mark.negative
    def test_number_prefix_raises(self) -> None:
        with pytest.raises(CommitParseError, match="does not match"):
            ConventionalCommit.parse("123: add login")

    @pytest.mark.negative
    def test_merge_commit_raises(self) -> None:
        with pytest.raises(CommitParseError, match="does not match"):
            ConventionalCommit.parse("Merge pull request #123 from branch")

    @pytest.mark.negative
    def test_empty_description_raises(self) -> None:
        with pytest.raises(CommitParseError, match="does not match"):
            ConventionalCommit.parse("feat: ")

    @pytest.mark.negative
    def test_unclosed_scope_raises(self) -> None:
        with pytest.raises(CommitParseError, match="does not match"):
            ConventionalCommit.parse("feat(unclosed: add login")


class TestConventionalCommitBumpType:
    """Tests for bump_type property."""

    @pytest.mark.happy_path
    def test_feat_is_minor(self) -> None:
        assert ConventionalCommit.parse("feat: add").bump_type == BumpType.MINOR

    @pytest.mark.happy_path
    def test_fix_is_patch(self) -> None:
        assert ConventionalCommit.parse("fix: fix").bump_type == BumpType.PATCH

    @pytest.mark.happy_path
    def test_perf_is_patch(self) -> None:
        assert ConventionalCommit.parse("perf: optimize").bump_type == BumpType.PATCH

    @pytest.mark.happy_path
    def test_breaking_is_major(self) -> None:
        assert ConventionalCommit.parse("feat!: break").bump_type == BumpType.MAJOR

    @pytest.mark.happy_path
    def test_docs_is_none(self) -> None:
        assert ConventionalCommit.parse("docs: update").bump_type == BumpType.NONE

    @pytest.mark.happy_path
    def test_chore_is_none(self) -> None:
        assert ConventionalCommit.parse("chore: cleanup").bump_type == BumpType.NONE

    @pytest.mark.happy_path
    def test_breaking_overrides_type(self) -> None:
        """Breaking change always produces MAJOR regardless of type."""
        assert ConventionalCommit.parse("fix!: breaking fix").bump_type == BumpType.MAJOR
        assert ConventionalCommit.parse("docs!: breaking docs").bump_type == BumpType.MAJOR


class TestConventionalCommitEdgeCases:
    """Tests for edge cases."""

    @pytest.mark.edge_case
    def test_leading_whitespace_stripped(self) -> None:
        commit = ConventionalCommit.parse("  feat: add feature  ")
        assert commit.commit_type == "feat"
        assert commit.description == "add feature"

    @pytest.mark.edge_case
    def test_frozen_dataclass(self) -> None:
        commit = ConventionalCommit.parse("feat: add feature")
        with pytest.raises(AttributeError):
            commit.commit_type = "fix"  # type: ignore[misc]
