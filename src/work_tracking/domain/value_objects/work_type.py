# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
WorkType - Work item type classification value object.

Represents the type/category of a work item in the work tracking system.
Different work types have different semantics and allowed operations.

References:
    - impl-es-e-006-workitem-schema: Work type hierarchy
    - WORKTRACKER: Work item categorization
"""

from __future__ import annotations

from enum import Enum


class WorkType(Enum):
    """
    Work item type classification.

    Work types categorize items and determine their behavior:
    - EPICs contain STORYs, which contain TASKs
    - SUBTASKs are atomic units within TASKs
    - BUGs represent defects to fix
    - SPIKEs are timeboxed research items

    Type Hierarchy:
        ```
        EPIC
          └── STORY
                └── TASK
                      └── SUBTASK
        BUG (any level)
        SPIKE (timeboxed research)
        ```

    Attributes:
        EPIC: Large initiative spanning sprints/weeks
        STORY: User-valuable feature, 1-5 days
        TASK: Specific work unit, hours to days
        SUBTASK: Atomic work item, hours
        BUG: Defect or problem to fix
        SPIKE: Timeboxed research/learning

    Example:
        >>> WorkType.TASK.can_have_subtasks
        True
        >>> WorkType.SUBTASK.can_have_subtasks
        False
        >>> WorkType.from_string("bug")
        <WorkType.BUG: 'bug'>
    """

    EPIC = "epic"
    STORY = "story"
    TASK = "task"
    SUBTASK = "subtask"
    BUG = "bug"
    SPIKE = "spike"

    @classmethod
    def from_string(cls, value: str) -> WorkType:
        """
        Parse case-insensitive work type string.

        Args:
            value: Work type name (case-insensitive)

        Returns:
            Matching WorkType enum value

        Raises:
            ValueError: If value is not a valid work type

        Example:
            >>> WorkType.from_string("TASK")
            <WorkType.TASK: 'task'>
            >>> WorkType.from_string("Bug")
            <WorkType.BUG: 'bug'>
        """
        normalized = value.lower().strip()
        for work_type in cls:
            if work_type.value == normalized:
                return work_type
        valid = [wt.value for wt in cls]
        raise ValueError(f"Invalid work type: {value!r}. Valid types: {', '.join(valid)}")

    @property
    def can_have_subtasks(self) -> bool:
        """
        Check if this work type can have subtasks.

        Returns:
            True if TASKs can be created as children

        Example:
            >>> WorkType.EPIC.can_have_subtasks
            True
            >>> WorkType.SUBTASK.can_have_subtasks
            False
        """
        return self in (WorkType.EPIC, WorkType.STORY, WorkType.TASK, WorkType.BUG)

    @property
    def can_have_parent(self) -> bool:
        """
        Check if this work type can have a parent.

        Returns:
            True if this item can be a child of another

        Example:
            >>> WorkType.SUBTASK.can_have_parent
            True
            >>> WorkType.EPIC.can_have_parent
            False
        """
        return self in (WorkType.STORY, WorkType.TASK, WorkType.SUBTASK)

    @property
    def is_container(self) -> bool:
        """
        Check if this is a container type (EPIC or STORY).

        Container types are meant to group related work items.

        Returns:
            True if this is EPIC or STORY

        Example:
            >>> WorkType.EPIC.is_container
            True
            >>> WorkType.TASK.is_container
            False
        """
        return self in (WorkType.EPIC, WorkType.STORY)

    @property
    def is_atomic(self) -> bool:
        """
        Check if this is an atomic work type (SUBTASK or SPIKE).

        Atomic types represent indivisible work units.

        Returns:
            True if this is SUBTASK or SPIKE

        Example:
            >>> WorkType.SUBTASK.is_atomic
            True
            >>> WorkType.TASK.is_atomic
            False
        """
        return self in (WorkType.SUBTASK, WorkType.SPIKE)

    @property
    def requires_quality_gates(self) -> bool:
        """
        Check if this work type requires quality gate validation.

        SPIKEs are research items and don't require quality gates.
        All other work types require quality validation before completion.

        Returns:
            True if quality gates apply to this work type

        Example:
            >>> WorkType.TASK.requires_quality_gates
            True
            >>> WorkType.SPIKE.requires_quality_gates
            False
        """
        return self != WorkType.SPIKE

    def valid_parent_types(self) -> list[WorkType]:
        """
        Get valid parent work types for this type.

        Returns:
            List of work types that can be parents

        Example:
            >>> WorkType.TASK.valid_parent_types()
            [<WorkType.STORY: 'story'>]
            >>> WorkType.SUBTASK.valid_parent_types()
            [<WorkType.TASK: 'task'>]
        """
        parent_map: dict[WorkType, list[WorkType]] = {
            WorkType.STORY: [WorkType.EPIC],
            WorkType.TASK: [WorkType.STORY],
            WorkType.SUBTASK: [WorkType.TASK],
        }
        return parent_map.get(self, [])

    def __str__(self) -> str:
        """Return the work type value."""
        return self.value

    def __repr__(self) -> str:
        """Return detailed representation for debugging."""
        return f"WorkType.{self.name}"
