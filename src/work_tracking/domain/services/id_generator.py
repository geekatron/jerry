# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
WorkItem ID Generator Domain Service.

Domain service for generating unique WorkItemIds using the Snowflake algorithm
for internal IDs and sequential numbering for display IDs.

Design:
    - Thread-safe ID generation
    - Hybrid identity: Snowflake internal + sequential display
    - Configurable worker ID and sequence initialization

References:
    - IMPL-009: Domain Services
    - ADR-007: ID Generation Strategy
    - PAT-006: Hybrid Identity (Snowflake + Display ID)
    - IMPL-001: SnowflakeIdGenerator implementation

Exports:
    IWorkItemIdGenerator: Protocol for ID generation
    WorkItemIdGenerator: Concrete implementation
"""

from __future__ import annotations

import threading
from typing import Protocol, runtime_checkable

from src.shared_kernel.snowflake_id import SnowflakeIdGenerator
from src.work_tracking.domain.value_objects import WorkItemId


@runtime_checkable
class IWorkItemIdGenerator(Protocol):
    """
    Protocol for WorkItem ID generation.

    Implementations must provide thread-safe ID generation with
    unique internal IDs (Snowflake) and sequential display numbers.

    Example:
        >>> def create_item(gen: IWorkItemIdGenerator) -> WorkItem:
        ...     id = gen.create()
        ...     return WorkItem.create(id=id, title="New Task")
    """

    def create(self) -> WorkItemId:
        """
        Create a new WorkItemId with auto-incremented display number.

        Returns:
            WorkItemId with unique internal ID and next sequential display number

        Thread Safety:
            This method is thread-safe. Concurrent calls will produce
            unique IDs with sequential display numbers.
        """
        ...

    def create_with_sequence(self, sequence: int) -> WorkItemId:
        """
        Create a WorkItemId with a specific display number.

        Use when importing or restoring items with known sequence numbers.
        Does not affect the auto-increment counter.

        Args:
            sequence: Display number to use (must be positive)

        Returns:
            WorkItemId with unique internal ID and specified display number

        Raises:
            ValueError: If sequence is not positive
        """
        ...


class WorkItemIdGenerator(IWorkItemIdGenerator):
    """
    Snowflake-based WorkItem ID generator.

    Generates WorkItemIds with:
    - Unique 64-bit Snowflake internal IDs
    - Sequential display numbers for human readability

    Thread Safety:
        All methods are thread-safe via internal locking.

    Example:
        >>> generator = WorkItemIdGenerator(worker_id=1)
        >>> id1 = generator.create()  # WORK-1
        >>> id2 = generator.create()  # WORK-2
        >>> id3 = generator.create_with_sequence(100)  # WORK-100
        >>> id4 = generator.create()  # WORK-3 (sequence not affected)

    Attributes:
        _worker_id: Worker ID for Snowflake (0-1023)
        _snowflake: Underlying Snowflake generator
        _sequence: Current auto-increment counter
        _lock: Thread safety lock
    """

    def __init__(
        self,
        worker_id: int | None = None,
        last_sequence: int = 0,
    ) -> None:
        """
        Initialize the ID generator.

        Args:
            worker_id: Worker ID for Snowflake (0-1023). If None, derives
                       from system properties (hostname, PID).
            last_sequence: Last used sequence number. Next create() will
                          use last_sequence + 1.

        Raises:
            ValueError: If worker_id is negative or > 1023
        """
        if worker_id is not None:
            if worker_id < 0:
                raise ValueError(f"worker_id must be non-negative, got {worker_id}")
            if worker_id > 1023:
                raise ValueError(f"worker_id must be <= 1023, got {worker_id}")
            self._worker_id = worker_id
        else:
            self._worker_id = SnowflakeIdGenerator.derive_worker_id()

        self._snowflake = SnowflakeIdGenerator(self._worker_id)
        self._sequence = last_sequence
        self._lock = threading.Lock()

    def create(self) -> WorkItemId:
        """
        Create a new WorkItemId with auto-incremented display number.

        Returns:
            WorkItemId with unique internal ID and next sequential display number

        Thread Safety:
            This method is thread-safe. Concurrent calls will produce
            unique IDs with sequential display numbers.
        """
        with self._lock:
            self._sequence += 1
            internal_id = self._snowflake.generate()
            return WorkItemId.create(
                internal_id=internal_id,
                display_number=self._sequence,
            )

    def create_with_sequence(self, sequence: int) -> WorkItemId:
        """
        Create a WorkItemId with a specific display number.

        Does not affect the auto-increment counter.

        Args:
            sequence: Display number to use (must be positive)

        Returns:
            WorkItemId with unique internal ID and specified display number

        Raises:
            ValueError: If sequence is not positive
        """
        if sequence <= 0:
            raise ValueError(f"sequence must be positive, got {sequence}")

        internal_id = self._snowflake.generate()
        return WorkItemId.create(
            internal_id=internal_id,
            display_number=sequence,
        )

    def reset_sequence(self) -> None:
        """
        Reset the sequence counter to 0.

        Next create() will produce display_number 1.

        Thread Safety:
            This method is thread-safe.
        """
        with self._lock:
            self._sequence = 0

    @property
    def current_sequence(self) -> int:
        """Current sequence number (last used)."""
        return self._sequence
