# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for DetectBumpTypeQuery."""

from __future__ import annotations

import pytest

from src.version.application.queries.detect_bump_type_query import DetectBumpTypeQuery


class TestDetectBumpTypeQuery:
    """Tests for DetectBumpTypeQuery value object."""

    @pytest.mark.happy_path
    def test_default_values(self) -> None:
        query = DetectBumpTypeQuery()
        assert query.since_tag is False
        assert query.range_spec is None
        assert query.commits_from_stdin is False

    @pytest.mark.happy_path
    def test_since_tag_flag(self) -> None:
        query = DetectBumpTypeQuery(since_tag=True)
        assert query.since_tag is True

    @pytest.mark.happy_path
    def test_range_spec(self) -> None:
        query = DetectBumpTypeQuery(range_spec="v0.22.1..HEAD")
        assert query.range_spec == "v0.22.1..HEAD"

    @pytest.mark.negative
    def test_frozen_dataclass(self) -> None:
        query = DetectBumpTypeQuery()
        with pytest.raises(AttributeError):
            query.since_tag = True  # type: ignore[misc]

    @pytest.mark.edge_case
    def test_commits_from_stdin(self) -> None:
        query = DetectBumpTypeQuery(commits_from_stdin=True)
        assert query.commits_from_stdin is True
