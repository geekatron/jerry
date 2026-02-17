# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for shared_kernel.jerry_uri module."""

from __future__ import annotations

import pytest

from src.shared_kernel.jerry_uri import JerryUri


class TestJerryUri:
    """Tests for JerryUri."""

    def test_parse_simple_uri(self) -> None:
        """JerryUri.parse() handles simple entity URI."""
        uri = JerryUri.parse("jerry://task/TASK-a1b2c3d4")
        assert uri.entity_type == "task"
        assert uri.entity_id == "TASK-a1b2c3d4"
        assert not uri.is_nested

    def test_parse_nested_uri(self) -> None:
        """JerryUri.parse() handles nested entity URI."""
        uri = JerryUri.parse("jerry://plan/PLAN-12345678/phase/PHASE-e5f6g7h8")
        assert uri.entity_type == "plan"
        assert uri.entity_id == "PLAN-12345678"
        assert uri.is_nested
        assert uri.leaf_type == "phase"
        assert uri.leaf_id == "PHASE-e5f6g7h8"

    def test_for_entity(self) -> None:
        """JerryUri.for_entity() creates simple URI."""
        uri = JerryUri.for_entity("task", "TASK-a1b2c3d4")
        assert str(uri) == "jerry://task/TASK-a1b2c3d4"

    def test_for_nested(self) -> None:
        """JerryUri.for_nested() creates nested URI."""
        uri = JerryUri.for_nested("plan", "PLAN-12345678", "phase", "PHASE-e5f6g7h8")
        assert str(uri) == "jerry://plan/PLAN-12345678/phase/PHASE-e5f6g7h8"

    def test_invalid_scheme_rejected(self) -> None:
        """JerryUri rejects non-jerry scheme."""
        with pytest.raises(ValueError, match="Invalid JerryUri scheme"):
            JerryUri.parse("http://task/TASK-a1b2c3d4")

    def test_empty_path_rejected(self) -> None:
        """JerryUri rejects empty path."""
        with pytest.raises(ValueError, match="cannot be empty"):
            JerryUri.parse("jerry://")

    def test_odd_segments_rejected(self) -> None:
        """JerryUri rejects odd number of path segments."""
        with pytest.raises(ValueError, match="pairs of type/id"):
            JerryUri(("task", "TASK-a1b2c3d4", "orphan"))

    def test_invalid_entity_type_rejected(self) -> None:
        """JerryUri rejects invalid entity types."""
        with pytest.raises(ValueError, match="Invalid entity type"):
            JerryUri.for_entity("invalid_type", "ID-12345678")

    def test_valid_entity_types(self) -> None:
        """JerryUri accepts all valid entity types."""
        valid_types = ["task", "phase", "plan", "knowledge", "actor", "event", "subtask"]
        for entity_type in valid_types:
            uri = JerryUri.for_entity(entity_type, "ID-12345678")
            assert uri.entity_type == entity_type

    def test_immutable(self) -> None:
        """JerryUri is immutable (frozen)."""
        uri = JerryUri.for_entity("task", "TASK-a1b2c3d4")
        with pytest.raises(AttributeError):
            uri.path_segments = ("modified",)  # type: ignore
