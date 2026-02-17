# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for WorkType value object.

Test Categories:
    - Enum Values: Correct values
    - Parsing: from_string factory method
    - Properties: can_have_subtasks, can_have_parent, is_container, etc.
    - Hierarchy: valid_parent_types method

References:
    - IMPL-005: WorkItem Aggregate (WorkType is a supporting VO)
    - impl-es-e-006-workitem-schema: WorkType hierarchy
"""

from __future__ import annotations

import pytest

from src.work_tracking.domain.value_objects import WorkType

# =============================================================================
# Enum Value Tests
# =============================================================================


class TestWorkTypeValues:
    """Tests for WorkType enum values."""

    def test_epic_value(self) -> None:
        """EPIC has correct value."""
        assert WorkType.EPIC.value == "epic"

    def test_story_value(self) -> None:
        """STORY has correct value."""
        assert WorkType.STORY.value == "story"

    def test_task_value(self) -> None:
        """TASK has correct value."""
        assert WorkType.TASK.value == "task"

    def test_subtask_value(self) -> None:
        """SUBTASK has correct value."""
        assert WorkType.SUBTASK.value == "subtask"

    def test_bug_value(self) -> None:
        """BUG has correct value."""
        assert WorkType.BUG.value == "bug"

    def test_spike_value(self) -> None:
        """SPIKE has correct value."""
        assert WorkType.SPIKE.value == "spike"

    def test_has_six_types(self) -> None:
        """There are exactly 6 work types."""
        assert len(WorkType) == 6


# =============================================================================
# Parsing Tests
# =============================================================================


class TestWorkTypeFromString:
    """Tests for WorkType.from_string() factory method."""

    def test_parse_task(self) -> None:
        """Parse 'task' string."""
        assert WorkType.from_string("task") == WorkType.TASK

    def test_parse_bug(self) -> None:
        """Parse 'bug' string."""
        assert WorkType.from_string("bug") == WorkType.BUG

    def test_parse_story(self) -> None:
        """Parse 'story' string."""
        assert WorkType.from_string("story") == WorkType.STORY

    def test_parse_epic(self) -> None:
        """Parse 'epic' string."""
        assert WorkType.from_string("epic") == WorkType.EPIC

    def test_parse_subtask(self) -> None:
        """Parse 'subtask' string."""
        assert WorkType.from_string("subtask") == WorkType.SUBTASK

    def test_parse_spike(self) -> None:
        """Parse 'spike' string."""
        assert WorkType.from_string("spike") == WorkType.SPIKE

    def test_parse_uppercase(self) -> None:
        """Parse uppercase strings."""
        assert WorkType.from_string("TASK") == WorkType.TASK
        assert WorkType.from_string("BUG") == WorkType.BUG

    def test_parse_mixed_case(self) -> None:
        """Parse mixed case strings."""
        assert WorkType.from_string("Task") == WorkType.TASK
        assert WorkType.from_string("BuG") == WorkType.BUG

    def test_parse_with_whitespace(self) -> None:
        """Parse strings with whitespace."""
        assert WorkType.from_string("  task  ") == WorkType.TASK

    def test_invalid_raises(self) -> None:
        """Invalid string raises ValueError."""
        with pytest.raises(ValueError, match="Invalid work type"):
            WorkType.from_string("invalid")

    def test_empty_raises(self) -> None:
        """Empty string raises ValueError."""
        with pytest.raises(ValueError, match="Invalid work type"):
            WorkType.from_string("")


# =============================================================================
# can_have_subtasks Property Tests
# =============================================================================


class TestCanHaveSubtasks:
    """Tests for can_have_subtasks property."""

    def test_epic_can_have_subtasks(self) -> None:
        """EPIC can have subtasks."""
        assert WorkType.EPIC.can_have_subtasks is True

    def test_story_can_have_subtasks(self) -> None:
        """STORY can have subtasks."""
        assert WorkType.STORY.can_have_subtasks is True

    def test_task_can_have_subtasks(self) -> None:
        """TASK can have subtasks."""
        assert WorkType.TASK.can_have_subtasks is True

    def test_bug_can_have_subtasks(self) -> None:
        """BUG can have subtasks."""
        assert WorkType.BUG.can_have_subtasks is True

    def test_subtask_cannot_have_subtasks(self) -> None:
        """SUBTASK cannot have subtasks."""
        assert WorkType.SUBTASK.can_have_subtasks is False

    def test_spike_cannot_have_subtasks(self) -> None:
        """SPIKE cannot have subtasks."""
        assert WorkType.SPIKE.can_have_subtasks is False


# =============================================================================
# can_have_parent Property Tests
# =============================================================================


class TestCanHaveParent:
    """Tests for can_have_parent property."""

    def test_story_can_have_parent(self) -> None:
        """STORY can have a parent (EPIC)."""
        assert WorkType.STORY.can_have_parent is True

    def test_task_can_have_parent(self) -> None:
        """TASK can have a parent (STORY)."""
        assert WorkType.TASK.can_have_parent is True

    def test_subtask_can_have_parent(self) -> None:
        """SUBTASK can have a parent (TASK)."""
        assert WorkType.SUBTASK.can_have_parent is True

    def test_epic_cannot_have_parent(self) -> None:
        """EPIC cannot have a parent."""
        assert WorkType.EPIC.can_have_parent is False

    def test_bug_cannot_have_parent(self) -> None:
        """BUG cannot have a parent."""
        assert WorkType.BUG.can_have_parent is False

    def test_spike_cannot_have_parent(self) -> None:
        """SPIKE cannot have a parent."""
        assert WorkType.SPIKE.can_have_parent is False


# =============================================================================
# is_container Property Tests
# =============================================================================


class TestIsContainer:
    """Tests for is_container property."""

    def test_epic_is_container(self) -> None:
        """EPIC is a container."""
        assert WorkType.EPIC.is_container is True

    def test_story_is_container(self) -> None:
        """STORY is a container."""
        assert WorkType.STORY.is_container is True

    def test_task_is_not_container(self) -> None:
        """TASK is not a container."""
        assert WorkType.TASK.is_container is False

    def test_subtask_is_not_container(self) -> None:
        """SUBTASK is not a container."""
        assert WorkType.SUBTASK.is_container is False

    def test_bug_is_not_container(self) -> None:
        """BUG is not a container."""
        assert WorkType.BUG.is_container is False

    def test_spike_is_not_container(self) -> None:
        """SPIKE is not a container."""
        assert WorkType.SPIKE.is_container is False


# =============================================================================
# is_atomic Property Tests
# =============================================================================


class TestIsAtomic:
    """Tests for is_atomic property."""

    def test_subtask_is_atomic(self) -> None:
        """SUBTASK is atomic."""
        assert WorkType.SUBTASK.is_atomic is True

    def test_spike_is_atomic(self) -> None:
        """SPIKE is atomic."""
        assert WorkType.SPIKE.is_atomic is True

    def test_task_is_not_atomic(self) -> None:
        """TASK is not atomic."""
        assert WorkType.TASK.is_atomic is False

    def test_story_is_not_atomic(self) -> None:
        """STORY is not atomic."""
        assert WorkType.STORY.is_atomic is False

    def test_epic_is_not_atomic(self) -> None:
        """EPIC is not atomic."""
        assert WorkType.EPIC.is_atomic is False

    def test_bug_is_not_atomic(self) -> None:
        """BUG is not atomic."""
        assert WorkType.BUG.is_atomic is False


# =============================================================================
# requires_quality_gates Property Tests
# =============================================================================


class TestRequiresQualityGates:
    """Tests for requires_quality_gates property."""

    def test_task_requires_quality_gates(self) -> None:
        """TASK requires quality gates."""
        assert WorkType.TASK.requires_quality_gates is True

    def test_bug_requires_quality_gates(self) -> None:
        """BUG requires quality gates."""
        assert WorkType.BUG.requires_quality_gates is True

    def test_story_requires_quality_gates(self) -> None:
        """STORY requires quality gates."""
        assert WorkType.STORY.requires_quality_gates is True

    def test_epic_requires_quality_gates(self) -> None:
        """EPIC requires quality gates."""
        assert WorkType.EPIC.requires_quality_gates is True

    def test_subtask_requires_quality_gates(self) -> None:
        """SUBTASK requires quality gates."""
        assert WorkType.SUBTASK.requires_quality_gates is True

    def test_spike_does_not_require_quality_gates(self) -> None:
        """SPIKE does not require quality gates (research item)."""
        assert WorkType.SPIKE.requires_quality_gates is False


# =============================================================================
# valid_parent_types Method Tests
# =============================================================================


class TestValidParentTypes:
    """Tests for valid_parent_types method."""

    def test_story_parent_is_epic(self) -> None:
        """STORY's valid parent is EPIC."""
        parents = WorkType.STORY.valid_parent_types()
        assert parents == [WorkType.EPIC]

    def test_task_parent_is_story(self) -> None:
        """TASK's valid parent is STORY."""
        parents = WorkType.TASK.valid_parent_types()
        assert parents == [WorkType.STORY]

    def test_subtask_parent_is_task(self) -> None:
        """SUBTASK's valid parent is TASK."""
        parents = WorkType.SUBTASK.valid_parent_types()
        assert parents == [WorkType.TASK]

    def test_epic_has_no_parent(self) -> None:
        """EPIC has no valid parents."""
        parents = WorkType.EPIC.valid_parent_types()
        assert parents == []

    def test_bug_has_no_parent(self) -> None:
        """BUG has no valid parents."""
        parents = WorkType.BUG.valid_parent_types()
        assert parents == []

    def test_spike_has_no_parent(self) -> None:
        """SPIKE has no valid parents."""
        parents = WorkType.SPIKE.valid_parent_types()
        assert parents == []


# =============================================================================
# String Representation Tests
# =============================================================================


class TestWorkTypeStringRepresentation:
    """Tests for WorkType string representations."""

    def test_str_task(self) -> None:
        """str(TASK) returns 'task'."""
        assert str(WorkType.TASK) == "task"

    def test_str_bug(self) -> None:
        """str(BUG) returns 'bug'."""
        assert str(WorkType.BUG) == "bug"

    def test_repr(self) -> None:
        """repr includes class name."""
        assert repr(WorkType.TASK) == "WorkType.TASK"


# =============================================================================
# Edge Case Tests
# =============================================================================


class TestWorkTypeEdgeCases:
    """Edge case tests for WorkType."""

    def test_equality(self) -> None:
        """Same work types are equal."""
        assert WorkType.TASK == WorkType.TASK

    def test_inequality(self) -> None:
        """Different work types are not equal."""
        assert WorkType.TASK != WorkType.BUG

    def test_hashable(self) -> None:
        """Work types can be used in sets."""
        type_set = {WorkType.TASK, WorkType.BUG, WorkType.TASK}
        assert len(type_set) == 2

    def test_work_type_in_dict(self) -> None:
        """Work types can be used as dict keys."""
        type_dict = {WorkType.TASK: "tasks", WorkType.BUG: "bugs"}
        assert type_dict[WorkType.TASK] == "tasks"
