# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for CompactionResult value object."""

from __future__ import annotations

import pytest

from src.context_monitoring.domain.value_objects.compaction_result import (
    CompactionResult,
)


class TestCompactionResult:
    """Test CompactionResult creation and factory methods."""

    def test_compaction_detected(self) -> None:
        """Direct construction for detected compaction."""
        result = CompactionResult(
            detected=True,
            from_tokens=180000,
            to_tokens=46000,
            session_id_changed=False,
        )
        assert result.detected is True
        assert result.from_tokens == 180000
        assert result.to_tokens == 46000
        assert result.session_id_changed is False

    def test_no_compaction_factory(self) -> None:
        """no_compaction factory sets detected=False."""
        result = CompactionResult.no_compaction(current_tokens=150000)
        assert result.detected is False
        assert result.from_tokens == 150000
        assert result.to_tokens == 150000
        assert result.session_id_changed is False

    def test_new_session_factory(self) -> None:
        """new_session factory indicates /clear event."""
        result = CompactionResult.new_session(current_tokens=5000)
        assert result.detected is False
        assert result.from_tokens == 0
        assert result.to_tokens == 5000
        assert result.session_id_changed is True

    def test_frozen_immutability(self) -> None:
        """CompactionResult is frozen/immutable."""
        result = CompactionResult.no_compaction(current_tokens=100)
        with pytest.raises(AttributeError):
            result.detected = True  # type: ignore[misc]
