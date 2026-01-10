"""Unit tests for IWorkItemIdGenerator domain service.

Test Categories:
    - Protocol Compliance: Interface adherence
    - ID Generation: Creating valid WorkItemIds
    - Sequence Management: Sequential and custom IDs
    - Thread Safety: Concurrent generation

References:
    - IMPL-009: Domain Services
    - ADR-007: ID Generation Strategy
    - PAT-006: Hybrid Identity (Snowflake + Display ID)
"""
from __future__ import annotations

import pytest

from src.work_tracking.domain.services.id_generator import (
    IWorkItemIdGenerator,
    WorkItemIdGenerator,
)
from src.work_tracking.domain.value_objects import WorkItemId


# =============================================================================
# IWorkItemIdGenerator Protocol Tests
# =============================================================================


class TestIWorkItemIdGeneratorProtocol:
    """Tests for IWorkItemIdGenerator protocol compliance."""

    def test_generator_implements_protocol(self) -> None:
        """WorkItemIdGenerator implements IWorkItemIdGenerator."""
        generator = WorkItemIdGenerator()
        assert isinstance(generator, IWorkItemIdGenerator)

    def test_protocol_has_create_method(self) -> None:
        """Protocol requires create() method."""
        assert hasattr(IWorkItemIdGenerator, "create")

    def test_protocol_has_create_with_sequence_method(self) -> None:
        """Protocol requires create_with_sequence() method."""
        assert hasattr(IWorkItemIdGenerator, "create_with_sequence")


# =============================================================================
# WorkItemIdGenerator Creation Tests
# =============================================================================


class TestWorkItemIdGeneratorCreation:
    """Tests for WorkItemIdGenerator instantiation."""

    def test_create_default(self) -> None:
        """Create generator with default settings."""
        generator = WorkItemIdGenerator()
        assert generator is not None

    def test_create_with_worker_id(self) -> None:
        """Create generator with specific worker ID."""
        generator = WorkItemIdGenerator(worker_id=5)
        assert generator._worker_id == 5

    def test_invalid_worker_id_raises(self) -> None:
        """Negative worker ID raises ValueError."""
        with pytest.raises(ValueError, match="worker_id"):
            WorkItemIdGenerator(worker_id=-1)

    def test_worker_id_too_large_raises(self) -> None:
        """Worker ID > 1023 raises ValueError."""
        with pytest.raises(ValueError, match="worker_id"):
            WorkItemIdGenerator(worker_id=1024)


# =============================================================================
# ID Generation Tests - Happy Path
# =============================================================================


class TestIdGenerationHappyPath:
    """Tests for successful ID generation."""

    def test_create_returns_work_item_id(self) -> None:
        """create() returns WorkItemId."""
        generator = WorkItemIdGenerator()
        id = generator.create()
        assert isinstance(id, WorkItemId)

    def test_create_auto_increments_sequence(self) -> None:
        """Sequential creates have incrementing display numbers."""
        generator = WorkItemIdGenerator()
        id1 = generator.create()
        id2 = generator.create()
        assert id2.display_number == id1.display_number + 1

    def test_create_generates_unique_internal_ids(self) -> None:
        """Each create generates unique internal ID."""
        generator = WorkItemIdGenerator()
        ids = [generator.create() for _ in range(100)]
        internal_ids = [id.internal_id for id in ids]
        assert len(set(internal_ids)) == 100

    def test_create_with_sequence_uses_provided_number(self) -> None:
        """create_with_sequence uses provided display number."""
        generator = WorkItemIdGenerator()
        id = generator.create_with_sequence(42)
        assert id.display_number == 42

    def test_create_with_sequence_still_increments(self) -> None:
        """create_with_sequence doesn't affect auto-increment."""
        generator = WorkItemIdGenerator()
        generator.create_with_sequence(100)
        id = generator.create()
        # Next auto-increment should be 1 (generator starts fresh)
        assert id.display_number == 1


# =============================================================================
# ID Generation Tests - Edge Cases
# =============================================================================


class TestIdGenerationEdgeCases:
    """Edge case tests for ID generation."""

    def test_sequence_starts_at_one(self) -> None:
        """First generated ID has display_number 1."""
        generator = WorkItemIdGenerator()
        id = generator.create()
        assert id.display_number == 1

    def test_create_with_sequence_zero_raises(self) -> None:
        """Sequence number 0 raises ValueError."""
        generator = WorkItemIdGenerator()
        with pytest.raises(ValueError, match="sequence"):
            generator.create_with_sequence(0)

    def test_create_with_sequence_negative_raises(self) -> None:
        """Negative sequence number raises ValueError."""
        generator = WorkItemIdGenerator()
        with pytest.raises(ValueError, match="sequence"):
            generator.create_with_sequence(-1)

    def test_many_sequential_creates(self) -> None:
        """Can generate many sequential IDs."""
        generator = WorkItemIdGenerator()
        ids = [generator.create() for _ in range(1000)]
        assert ids[-1].display_number == 1000

    def test_reset_sequence(self) -> None:
        """Can reset sequence counter."""
        generator = WorkItemIdGenerator()
        generator.create()
        generator.create()
        generator.reset_sequence()
        id = generator.create()
        assert id.display_number == 1


# =============================================================================
# Thread Safety Tests
# =============================================================================


class TestIdGeneratorThreadSafety:
    """Tests for thread-safe ID generation."""

    def test_concurrent_creates_are_unique(self) -> None:
        """Concurrent creates produce unique IDs."""
        import threading
        from collections import Counter

        generator = WorkItemIdGenerator()
        ids: list[WorkItemId] = []
        lock = threading.Lock()

        def generate_ids(count: int) -> None:
            for _ in range(count):
                id = generator.create()
                with lock:
                    ids.append(id)

        threads = [
            threading.Thread(target=generate_ids, args=(100,))
            for _ in range(10)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # All internal IDs should be unique
        internal_ids = [id.internal_id for id in ids]
        assert len(set(internal_ids)) == 1000

        # Display numbers should be unique (1-1000)
        display_numbers = [id.display_number for id in ids]
        assert len(set(display_numbers)) == 1000


# =============================================================================
# Initialization with State Tests
# =============================================================================


class TestIdGeneratorStateInitialization:
    """Tests for initializing generator with existing state."""

    def test_initialize_with_last_sequence(self) -> None:
        """Can initialize with last known sequence number."""
        generator = WorkItemIdGenerator(last_sequence=50)
        id = generator.create()
        assert id.display_number == 51

    def test_initialize_with_zero_sequence(self) -> None:
        """Initialize with 0 starts at 1."""
        generator = WorkItemIdGenerator(last_sequence=0)
        id = generator.create()
        assert id.display_number == 1
