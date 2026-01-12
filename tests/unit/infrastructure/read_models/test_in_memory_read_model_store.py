"""
Unit tests for InMemoryReadModelStore.

Test Distribution per impl-es-e-003:
- Happy Path (60%): 6 tests - save, load, load_all, delete, exists, count
- Negative (30%): 3 tests - load missing, delete missing, invalid types
- Edge (10%): 2 tests - empty store, clear, overwrite
"""

from __future__ import annotations

import pytest

from src.infrastructure.read_models import InMemoryReadModelStore


# === Happy Path Tests (60%) ===


class TestInMemoryReadModelStoreHappyPath:
    """Happy path tests for InMemoryReadModelStore."""

    def test_store_is_importable(self) -> None:
        """InMemoryReadModelStore can be imported."""
        from src.infrastructure.read_models import InMemoryReadModelStore

        assert InMemoryReadModelStore is not None

    def test_save_and_load_returns_data(self) -> None:
        """Save then load returns the saved data."""
        # Arrange
        store = InMemoryReadModelStore()
        data = {"name": "Test Project", "status": "active"}

        # Act
        store.save("project_dashboard", "proj-001", data)
        result = store.load("project_dashboard", "proj-001")

        # Assert
        assert result == data

    def test_load_all_returns_all_instances(self) -> None:
        """load_all returns all instances of a model type."""
        # Arrange
        store = InMemoryReadModelStore()
        store.save("project_dashboard", "proj-001", {"name": "Project 1"})
        store.save("project_dashboard", "proj-002", {"name": "Project 2"})
        store.save("project_dashboard", "proj-003", {"name": "Project 3"})

        # Act
        result = store.load_all("project_dashboard")

        # Assert
        assert len(result) == 3
        names = {item["name"] for item in result}
        assert names == {"Project 1", "Project 2", "Project 3"}

    def test_delete_removes_instance(self) -> None:
        """Delete removes the instance and returns True."""
        # Arrange
        store = InMemoryReadModelStore()
        store.save("project_dashboard", "proj-001", {"name": "Test"})

        # Act
        result = store.delete("project_dashboard", "proj-001")

        # Assert
        assert result is True
        assert store.load("project_dashboard", "proj-001") is None

    def test_exists_returns_true_for_saved_data(self) -> None:
        """exists returns True for saved data."""
        # Arrange
        store = InMemoryReadModelStore()
        store.save("project_dashboard", "proj-001", {"name": "Test"})

        # Act & Assert
        assert store.exists("project_dashboard", "proj-001") is True

    def test_count_returns_number_of_instances(self) -> None:
        """count returns correct number of instances."""
        # Arrange
        store = InMemoryReadModelStore()
        store.save("project_dashboard", "proj-001", {"name": "1"})
        store.save("project_dashboard", "proj-002", {"name": "2"})

        # Act & Assert
        assert store.count("project_dashboard") == 2


# === Negative Tests (30%) ===


class TestInMemoryReadModelStoreNegative:
    """Negative tests for InMemoryReadModelStore."""

    def test_load_missing_returns_none(self) -> None:
        """Load returns None for non-existent key."""
        # Arrange
        store = InMemoryReadModelStore()

        # Act
        result = store.load("project_dashboard", "nonexistent")

        # Assert
        assert result is None

    def test_delete_missing_returns_false(self) -> None:
        """Delete returns False for non-existent key."""
        # Arrange
        store = InMemoryReadModelStore()

        # Act
        result = store.delete("project_dashboard", "nonexistent")

        # Assert
        assert result is False

    def test_exists_returns_false_for_missing(self) -> None:
        """exists returns False for non-existent key."""
        # Arrange
        store = InMemoryReadModelStore()

        # Act & Assert
        assert store.exists("project_dashboard", "nonexistent") is False


# === Edge Case Tests (10%) ===


class TestInMemoryReadModelStoreEdgeCases:
    """Edge case tests for InMemoryReadModelStore."""

    def test_empty_store_load_all_returns_empty_list(self) -> None:
        """load_all returns empty list for empty store."""
        # Arrange
        store = InMemoryReadModelStore()

        # Act
        result = store.load_all("project_dashboard")

        # Assert
        assert result == []

    def test_clear_removes_all_data(self) -> None:
        """clear removes all stored data."""
        # Arrange
        store = InMemoryReadModelStore()
        store.save("project_dashboard", "proj-001", {"name": "1"})
        store.save("task_list", "task-001", {"title": "T1"})

        # Act
        store.clear()

        # Assert
        assert store.load("project_dashboard", "proj-001") is None
        assert store.load("task_list", "task-001") is None
        assert store.count("project_dashboard") == 0

    def test_save_overwrites_existing_data(self) -> None:
        """Save with same key overwrites existing data."""
        # Arrange
        store = InMemoryReadModelStore()
        store.save("project_dashboard", "proj-001", {"name": "Old"})

        # Act
        store.save("project_dashboard", "proj-001", {"name": "New"})
        result = store.load("project_dashboard", "proj-001")

        # Assert
        assert result == {"name": "New"}

    def test_different_model_types_are_isolated(self) -> None:
        """Different model types don't interfere with each other."""
        # Arrange
        store = InMemoryReadModelStore()
        store.save("project_dashboard", "key-001", {"type": "project"})
        store.save("task_list", "key-001", {"type": "task"})

        # Act & Assert
        project = store.load("project_dashboard", "key-001")
        task = store.load("task_list", "key-001")

        assert project == {"type": "project"}
        assert task == {"type": "task"}
