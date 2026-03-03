# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for DetectBumpTypeQueryHandler."""

from __future__ import annotations

import pytest

from src.version.application.handlers.queries.detect_bump_type_query_handler import (
    DetectBumpTypeQueryHandler,
)
from src.version.application.ports.commit_log_reader import CommitLogEntry
from src.version.domain.services.bump_type_detector import BumpTypeDetector
from src.version.domain.value_objects.bump_type import BumpType


class FakeCommitReader:
    """Fake commit reader for testing."""

    def __init__(self, entries: list[CommitLogEntry]) -> None:
        self.entries = entries
        self.last_since_tag: str | None = None
        self.last_range_spec: str | None = None

    def read_commits(
        self,
        since_tag: str | None = None,
        range_spec: str | None = None,
    ) -> list[CommitLogEntry]:
        self.last_since_tag = since_tag
        self.last_range_spec = range_spec
        return self.entries


class TestDetectBumpTypeQueryHandler:
    """Tests for DetectBumpTypeQueryHandler."""

    @pytest.mark.happy_path
    def test_handle_returns_minor_for_feat(self) -> None:
        reader = FakeCommitReader(
            [
                CommitLogEntry(subject="feat(GH-122): add feature", body=""),
            ]
        )
        handler = DetectBumpTypeQueryHandler(
            commit_reader=reader,
            detector=BumpTypeDetector(),
        )

        result = handler.handle(since_tag="v0.22.1")

        assert result == BumpType.MINOR
        assert reader.last_since_tag == "v0.22.1"

    @pytest.mark.happy_path
    def test_handle_returns_patch_for_fix(self) -> None:
        reader = FakeCommitReader(
            [
                CommitLogEntry(subject="fix: fix bug", body=""),
            ]
        )
        handler = DetectBumpTypeQueryHandler(
            commit_reader=reader,
            detector=BumpTypeDetector(),
        )

        result = handler.handle()
        assert result == BumpType.PATCH

    @pytest.mark.happy_path
    def test_handle_passes_range_spec(self) -> None:
        reader = FakeCommitReader(
            [
                CommitLogEntry(subject="feat: add", body=""),
            ]
        )
        handler = DetectBumpTypeQueryHandler(
            commit_reader=reader,
            detector=BumpTypeDetector(),
        )

        handler.handle(range_spec="v0.22.1..HEAD")
        assert reader.last_range_spec == "v0.22.1..HEAD"

    @pytest.mark.happy_path
    def test_handle_with_breaking_change_body(self) -> None:
        reader = FakeCommitReader(
            [
                CommitLogEntry(
                    subject="fix: fix API",
                    body="BREAKING CHANGE: removed old endpoint",
                ),
            ]
        )
        handler = DetectBumpTypeQueryHandler(
            commit_reader=reader,
            detector=BumpTypeDetector(),
        )

        result = handler.handle()
        assert result == BumpType.MAJOR

    @pytest.mark.happy_path
    def test_handle_multiple_commits(self) -> None:
        reader = FakeCommitReader(
            [
                CommitLogEntry(subject="docs: update", body=""),
                CommitLogEntry(subject="feat(GH-122): add", body=""),
                CommitLogEntry(subject="fix: fix", body=""),
            ]
        )
        handler = DetectBumpTypeQueryHandler(
            commit_reader=reader,
            detector=BumpTypeDetector(),
        )

        result = handler.handle()
        assert result == BumpType.MINOR

    @pytest.mark.happy_path
    def test_handle_filters_empty_bodies(self) -> None:
        reader = FakeCommitReader(
            [
                CommitLogEntry(subject="fix: fix", body=""),
                CommitLogEntry(subject="feat: add", body="Some body text"),
            ]
        )
        handler = DetectBumpTypeQueryHandler(
            commit_reader=reader,
            detector=BumpTypeDetector(),
        )

        result = handler.handle()
        assert result == BumpType.MINOR

    @pytest.mark.negative
    def test_handle_empty_commits(self) -> None:
        reader = FakeCommitReader([])
        handler = DetectBumpTypeQueryHandler(
            commit_reader=reader,
            detector=BumpTypeDetector(),
        )

        result = handler.handle()
        assert result == BumpType.NONE

    @pytest.mark.negative
    def test_handle_non_conventional_commits(self) -> None:
        reader = FakeCommitReader(
            [
                CommitLogEntry(subject="Merge PR #123", body=""),
                CommitLogEntry(subject="Update README", body=""),
            ]
        )
        handler = DetectBumpTypeQueryHandler(
            commit_reader=reader,
            detector=BumpTypeDetector(),
        )

        result = handler.handle()
        assert result == BumpType.NONE

    @pytest.mark.negative
    def test_handle_all_bodies_empty(self) -> None:
        reader = FakeCommitReader(
            [
                CommitLogEntry(subject="fix: fix", body=""),
            ]
        )
        handler = DetectBumpTypeQueryHandler(
            commit_reader=reader,
            detector=BumpTypeDetector(),
        )

        result = handler.handle()
        assert result == BumpType.PATCH

    @pytest.mark.edge_case
    def test_handle_passes_since_tag_to_reader(self) -> None:
        reader = FakeCommitReader([])
        handler = DetectBumpTypeQueryHandler(
            commit_reader=reader,
            detector=BumpTypeDetector(),
        )

        handler.handle(since_tag="__latest__")
        assert reader.last_since_tag == "__latest__"
