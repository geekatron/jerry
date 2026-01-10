"""Unit tests for work_tracking.domain.ports.repository module.

Test Categories:
    - Protocol Definition: Verify IRepository protocol structure
    - Exception Tests: AggregateNotFoundError, ConcurrencyError, RepositoryError
    - Protocol Compliance: Test that implementations satisfy the protocol

References:
    - PAT-009: Generic Repository Port
    - IMPL-REPO-001: IRepository Port implementation
"""
from __future__ import annotations

from typing import TypeVar

import pytest

from src.work_tracking.domain.aggregates.base import AggregateRoot
from src.work_tracking.domain.ports.repository import (
    AggregateNotFoundError,
    ConcurrencyError,
    IRepository,
    RepositoryError,
)
from src.shared_kernel.domain_event import DomainEvent
from dataclasses import dataclass


# =============================================================================
# Test Fixtures
# =============================================================================


@dataclass(frozen=True)
class _MockEvent(DomainEvent):
    """Mock event for testing."""

    value: str = ""

    def _payload(self) -> dict:
        return {"value": self.value}


class _MockAggregate(AggregateRoot):
    """Mock aggregate for testing repository implementations."""

    _aggregate_type = "MockAggregate"

    def __init__(self, id: str, value: str = "") -> None:
        super().__init__(id)
        self._value = value

    @property
    def value(self) -> str:
        return self._value

    def _apply(self, event: DomainEvent) -> None:
        if isinstance(event, _MockEvent):
            self._value = event.value


class _MockRepository:
    """
    Mock repository implementation for testing protocol compliance.

    This implementation stores aggregates in memory and demonstrates
    all the required methods of IRepository.
    """

    def __init__(self) -> None:
        self._storage: dict[str, _MockAggregate] = {}
        self._versions: dict[str, int] = {}

    def get(self, id: str) -> _MockAggregate | None:
        return self._storage.get(id)

    def get_or_raise(self, id: str) -> _MockAggregate:
        aggregate = self.get(id)
        if aggregate is None:
            raise AggregateNotFoundError(id, "MockAggregate")
        return aggregate

    def save(self, aggregate: _MockAggregate) -> None:
        stored_version = self._versions.get(aggregate.id, 0)
        # For new aggregates, version starts at 0
        expected_version = aggregate.version - len(list(aggregate._pending_events))
        if aggregate.id in self._storage and stored_version != expected_version:
            raise ConcurrencyError(aggregate.id, expected_version, stored_version)
        self._storage[aggregate.id] = aggregate
        self._versions[aggregate.id] = aggregate.version

    def delete(self, id: str) -> bool:
        if id in self._storage:
            del self._storage[id]
            del self._versions[id]
            return True
        return False

    def exists(self, id: str) -> bool:
        return id in self._storage


# =============================================================================
# Protocol Definition Tests
# =============================================================================


class TestIRepositoryProtocol:
    """Tests for IRepository protocol definition."""

    def test_has_get_method(self) -> None:
        """IRepository defines get method."""
        assert hasattr(IRepository, "get")

    def test_has_get_or_raise_method(self) -> None:
        """IRepository defines get_or_raise method."""
        assert hasattr(IRepository, "get_or_raise")

    def test_has_save_method(self) -> None:
        """IRepository defines save method."""
        assert hasattr(IRepository, "save")

    def test_has_delete_method(self) -> None:
        """IRepository defines delete method."""
        assert hasattr(IRepository, "delete")

    def test_has_exists_method(self) -> None:
        """IRepository defines exists method."""
        assert hasattr(IRepository, "exists")

    def test_is_protocol_class(self) -> None:
        """IRepository is a Protocol class."""
        assert hasattr(IRepository, "__protocol_attrs__") or hasattr(
            IRepository, "_is_protocol"
        )


# =============================================================================
# Exception Tests - AggregateNotFoundError
# =============================================================================


class TestAggregateNotFoundError:
    """Tests for AggregateNotFoundError exception."""

    def test_has_aggregate_id(self) -> None:
        """AggregateNotFoundError stores aggregate_id."""
        error = AggregateNotFoundError("WORK-001")
        assert error.aggregate_id == "WORK-001"

    def test_has_aggregate_type(self) -> None:
        """AggregateNotFoundError stores aggregate_type."""
        error = AggregateNotFoundError("WORK-001", "WorkItem")
        assert error.aggregate_type == "WorkItem"

    def test_default_aggregate_type(self) -> None:
        """AggregateNotFoundError has default aggregate_type."""
        error = AggregateNotFoundError("WORK-001")
        assert error.aggregate_type == "Aggregate"

    def test_message_format(self) -> None:
        """AggregateNotFoundError has descriptive message."""
        error = AggregateNotFoundError("WORK-001", "WorkItem")
        assert "WORK-001" in str(error)
        assert "WorkItem" in str(error)
        assert "not found" in str(error)

    def test_is_repository_error(self) -> None:
        """AggregateNotFoundError is RepositoryError subclass."""
        error = AggregateNotFoundError("WORK-001")
        assert isinstance(error, RepositoryError)

    def test_can_be_raised_and_caught(self) -> None:
        """AggregateNotFoundError can be raised and caught."""
        with pytest.raises(AggregateNotFoundError) as exc_info:
            raise AggregateNotFoundError("WORK-999", "WorkItem")
        assert exc_info.value.aggregate_id == "WORK-999"


# =============================================================================
# Exception Tests - ConcurrencyError
# =============================================================================


class TestConcurrencyError:
    """Tests for ConcurrencyError exception."""

    def test_has_aggregate_id(self) -> None:
        """ConcurrencyError stores aggregate_id."""
        error = ConcurrencyError("WORK-001", expected=5, actual=7)
        assert error.aggregate_id == "WORK-001"

    def test_has_expected_version(self) -> None:
        """ConcurrencyError stores expected_version."""
        error = ConcurrencyError("WORK-001", expected=5, actual=7)
        assert error.expected_version == 5

    def test_has_actual_version(self) -> None:
        """ConcurrencyError stores actual_version."""
        error = ConcurrencyError("WORK-001", expected=5, actual=7)
        assert error.actual_version == 7

    def test_message_format(self) -> None:
        """ConcurrencyError has descriptive message."""
        error = ConcurrencyError("WORK-001", expected=5, actual=7)
        assert "WORK-001" in str(error)
        assert "5" in str(error)
        assert "7" in str(error)

    def test_is_repository_error(self) -> None:
        """ConcurrencyError is RepositoryError subclass."""
        error = ConcurrencyError("WORK-001", expected=5, actual=7)
        assert isinstance(error, RepositoryError)

    def test_can_be_raised_and_caught(self) -> None:
        """ConcurrencyError can be raised and caught."""
        with pytest.raises(ConcurrencyError) as exc_info:
            raise ConcurrencyError("WORK-001", expected=0, actual=5)
        assert exc_info.value.aggregate_id == "WORK-001"


# =============================================================================
# Exception Tests - RepositoryError
# =============================================================================


class TestRepositoryError:
    """Tests for base RepositoryError."""

    def test_is_exception(self) -> None:
        """RepositoryError is Exception subclass."""
        error = RepositoryError("test error")
        assert isinstance(error, Exception)

    def test_message(self) -> None:
        """RepositoryError preserves message."""
        error = RepositoryError("custom message")
        assert str(error) == "custom message"


# =============================================================================
# Protocol Compliance Tests
# =============================================================================


class TestMockRepositoryCompliance:
    """Tests that _MockRepository correctly implements IRepository semantics."""

    def test_get_returns_none_for_missing(self) -> None:
        """get returns None when aggregate not found."""
        repo = _MockRepository()
        result = repo.get("MISSING-001")
        assert result is None

    def test_get_returns_aggregate_when_exists(self) -> None:
        """get returns aggregate when it exists."""
        repo = _MockRepository()
        aggregate = _MockAggregate("ITEM-001", "test")
        repo.save(aggregate)

        result = repo.get("ITEM-001")
        assert result is not None
        assert result.id == "ITEM-001"

    def test_get_or_raise_raises_when_missing(self) -> None:
        """get_or_raise raises AggregateNotFoundError when not found."""
        repo = _MockRepository()
        with pytest.raises(AggregateNotFoundError) as exc_info:
            repo.get_or_raise("MISSING-001")
        assert exc_info.value.aggregate_id == "MISSING-001"

    def test_get_or_raise_returns_when_exists(self) -> None:
        """get_or_raise returns aggregate when it exists."""
        repo = _MockRepository()
        aggregate = _MockAggregate("ITEM-001", "test")
        repo.save(aggregate)

        result = repo.get_or_raise("ITEM-001")
        assert result.id == "ITEM-001"

    def test_save_stores_new_aggregate(self) -> None:
        """save stores a new aggregate."""
        repo = _MockRepository()
        aggregate = _MockAggregate("ITEM-001", "test")

        repo.save(aggregate)

        assert repo.exists("ITEM-001")

    def test_save_updates_existing_aggregate(self) -> None:
        """save updates an existing aggregate."""
        repo = _MockRepository()
        aggregate = _MockAggregate("ITEM-001", "initial")
        repo.save(aggregate)

        aggregate._value = "updated"
        repo.save(aggregate)

        result = repo.get("ITEM-001")
        assert result is not None
        assert result.value == "updated"

    def test_delete_returns_true_when_exists(self) -> None:
        """delete returns True when aggregate existed."""
        repo = _MockRepository()
        aggregate = _MockAggregate("ITEM-001", "test")
        repo.save(aggregate)

        result = repo.delete("ITEM-001")
        assert result is True

    def test_delete_returns_false_when_missing(self) -> None:
        """delete returns False when aggregate didn't exist."""
        repo = _MockRepository()
        result = repo.delete("MISSING-001")
        assert result is False

    def test_delete_removes_aggregate(self) -> None:
        """delete removes aggregate from storage."""
        repo = _MockRepository()
        aggregate = _MockAggregate("ITEM-001", "test")
        repo.save(aggregate)

        repo.delete("ITEM-001")

        assert not repo.exists("ITEM-001")

    def test_exists_returns_false_when_missing(self) -> None:
        """exists returns False when aggregate not found."""
        repo = _MockRepository()
        assert repo.exists("MISSING-001") is False

    def test_exists_returns_true_when_present(self) -> None:
        """exists returns True when aggregate exists."""
        repo = _MockRepository()
        aggregate = _MockAggregate("ITEM-001", "test")
        repo.save(aggregate)

        assert repo.exists("ITEM-001") is True


# =============================================================================
# Protocol Type Checking Tests
# =============================================================================


class TestProtocolTypeChecking:
    """Tests for protocol type compatibility."""

    def test_mock_repository_is_structurally_compatible(self) -> None:
        """_MockRepository is structurally compatible with IRepository."""
        # This test verifies structural subtyping works
        repo: IRepository[_MockAggregate, str] = _MockRepository()
        # If we got here without type errors, the protocol is satisfied
        assert repo is not None

    def test_repository_methods_have_correct_signatures(self) -> None:
        """Repository methods accept correct argument types."""
        repo = _MockRepository()

        # get accepts string ID
        result1 = repo.get("ID-001")
        assert result1 is None or isinstance(result1, _MockAggregate)

        # exists accepts string ID and returns bool
        result2 = repo.exists("ID-001")
        assert isinstance(result2, bool)

        # delete accepts string ID and returns bool
        result3 = repo.delete("ID-001")
        assert isinstance(result3, bool)


# =============================================================================
# Edge Case Tests
# =============================================================================


class TestEdgeCases:
    """Edge case tests for repository behavior."""

    def test_empty_id_can_be_used(self) -> None:
        """Empty string ID is technically valid (aggregate validates)."""
        repo = _MockRepository()
        # The repository doesn't validate IDs - that's the aggregate's job
        assert repo.get("") is None

    def test_special_characters_in_id(self) -> None:
        """IDs with special characters work correctly."""
        repo = _MockRepository()
        aggregate = _MockAggregate("ID-with-dashes", "test")
        repo.save(aggregate)
        assert repo.exists("ID-with-dashes")

    def test_unicode_in_id(self) -> None:
        """Unicode characters in IDs work correctly."""
        repo = _MockRepository()
        aggregate = _MockAggregate("item-日本語", "test")
        repo.save(aggregate)
        assert repo.exists("item-日本語")

    def test_multiple_aggregates(self) -> None:
        """Repository can store multiple aggregates."""
        repo = _MockRepository()
        for i in range(10):
            aggregate = _MockAggregate(f"ITEM-{i:03d}", f"value-{i}")
            repo.save(aggregate)

        assert sum(1 for i in range(10) if repo.exists(f"ITEM-{i:03d}")) == 10

    def test_save_same_aggregate_twice(self) -> None:
        """Saving the same aggregate twice works."""
        repo = _MockRepository()
        aggregate = _MockAggregate("ITEM-001", "test")
        repo.save(aggregate)
        repo.save(aggregate)  # Should not raise
        assert repo.exists("ITEM-001")

    def test_delete_twice(self) -> None:
        """Deleting same ID twice is safe."""
        repo = _MockRepository()
        aggregate = _MockAggregate("ITEM-001", "test")
        repo.save(aggregate)

        result1 = repo.delete("ITEM-001")
        result2 = repo.delete("ITEM-001")

        assert result1 is True
        assert result2 is False
