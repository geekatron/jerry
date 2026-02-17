# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for shared_kernel.entity_base module."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from src.shared_kernel.auditable import IAuditable
from src.shared_kernel.entity_base import EntityBase
from src.shared_kernel.versioned import IVersioned
from src.shared_kernel.vertex_id import TaskId


class TestEntityBase:
    """Tests for EntityBase."""

    def test_create_with_task_id(self) -> None:
        """EntityBase can be created with TaskId."""
        task_id = TaskId.generate()
        entity = EntityBase(_id=task_id)
        assert entity.id == task_id

    def test_default_version_is_zero(self) -> None:
        """EntityBase starts with version 0."""
        task_id = TaskId.generate()
        entity = EntityBase(_id=task_id)
        assert entity.version == 0

    def test_default_created_by_is_system(self) -> None:
        """EntityBase defaults created_by to 'System'."""
        task_id = TaskId.generate()
        entity = EntityBase(_id=task_id)
        assert entity.created_by == "System"

    def test_created_at_is_set(self) -> None:
        """EntityBase sets created_at to current time."""
        task_id = TaskId.generate()
        before = datetime.now(UTC)
        entity = EntityBase(_id=task_id)
        after = datetime.now(UTC)
        assert before <= entity.created_at <= after

    def test_implements_iauditable(self) -> None:
        """EntityBase satisfies IAuditable protocol."""
        task_id = TaskId.generate()
        entity = EntityBase(_id=task_id)
        assert isinstance(entity, IAuditable)

    def test_implements_iversioned(self) -> None:
        """EntityBase satisfies IVersioned protocol."""
        task_id = TaskId.generate()
        entity = EntityBase(_id=task_id)
        assert isinstance(entity, IVersioned)

    def test_get_expected_version(self) -> None:
        """get_expected_version returns current version."""
        task_id = TaskId.generate()
        entity = EntityBase(_id=task_id, _version=5)
        assert entity.get_expected_version() == 5

    def test_touch_updates_metadata(self) -> None:
        """_touch() updates updated_by and updated_at."""
        task_id = TaskId.generate()
        entity = EntityBase(_id=task_id, _updated_by="System")
        original_time = entity.updated_at

        entity._touch("Claude")

        assert entity.updated_by == "Claude"
        assert entity.updated_at >= original_time

    def test_increment_version(self) -> None:
        """_increment_version() increments version by 1."""
        task_id = TaskId.generate()
        entity = EntityBase(_id=task_id, _version=0)

        entity._increment_version()

        assert entity.version == 1

    def test_custom_created_by(self) -> None:
        """EntityBase accepts custom created_by."""
        task_id = TaskId.generate()
        entity = EntityBase(_id=task_id, _created_by="Claude")
        assert entity.created_by == "Claude"


class TestEntityBaseSubclass:
    """Tests for EntityBase subclassing."""

    def test_subclass_with_additional_fields(self) -> None:
        """EntityBase can be subclassed with additional fields."""

        @dataclass
        class Task(EntityBase):
            title: str = ""
            description: str = ""

        task_id = TaskId.generate()
        task = Task(_id=task_id, title="Test Task", description="A test")

        assert task.id == task_id
        assert task.title == "Test Task"
        assert task.description == "A test"
        assert isinstance(task, IAuditable)
        assert isinstance(task, IVersioned)
