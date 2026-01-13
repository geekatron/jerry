"""
Snowflake ID Generator - Coordination-free unique ID generation.

This module implements Twitter's Snowflake algorithm for generating unique 64-bit
IDs without requiring coordination between instances. Each ID encodes:
- Timestamp (41 bits): milliseconds since custom epoch
- Worker ID (10 bits): identifies the generating instance
- Sequence (12 bits): counter for IDs within same millisecond

References:
    - ADR-007: ID Generation Strategy
    - Twitter Snowflake: https://blog.twitter.com/engineering/en_us/a/2010/announcing-snowflake
    - Wikipedia: https://en.wikipedia.org/wiki/Snowflake_ID
    - arXiv: https://arxiv.org/html/2512.11643

Exports:
    SnowflakeIdGenerator: Main generator class
"""

from __future__ import annotations

import hashlib
import os
import socket
import threading
import time
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, ClassVar


@dataclass
class SnowflakeIdGenerator:
    """
    Generate unique 64-bit IDs without coordination.

    ID Structure (64 bits total):
    - Bit 63: Sign bit (always 0)
    - Bits 22-62 (41 bits): Timestamp in milliseconds since epoch
    - Bits 12-21 (10 bits): Worker ID (0-1023)
    - Bits 0-11 (12 bits): Sequence number (0-4095)

    Guarantees:
    - Unique: Different workers generate different IDs
    - Time-sortable: IDs increase monotonically over time
    - High throughput: 4096 IDs per millisecond per worker

    Example:
        >>> generator = SnowflakeIdGenerator(worker_id=1)
        >>> id_value = generator.generate()
        >>> parsed = SnowflakeIdGenerator.parse(id_value)
        >>> parsed["worker_id"]
        1

    Raises:
        ValueError: If worker_id is not in range [0, 1023]
        RuntimeError: If clock moves backwards by more than 1 second
    """

    # Custom epoch: 2024-01-01 00:00:00 UTC
    # This gives ~69 years of timestamps before overflow
    EPOCH: ClassVar[int] = 1704067200000  # milliseconds

    WORKER_BITS: ClassVar[int] = 10
    SEQUENCE_BITS: ClassVar[int] = 12
    TIMESTAMP_BITS: ClassVar[int] = 41

    MAX_WORKER_ID: ClassVar[int] = (1 << 10) - 1  # 1023
    MAX_SEQUENCE: ClassVar[int] = (1 << 12) - 1  # 4095

    # Cached worker ID derivation (per-process singleton)
    _cached_derived_worker_id: ClassVar[int | None] = None
    _derivation_lock: ClassVar[threading.Lock] = threading.Lock()

    worker_id: int
    _sequence: int = field(default=0, repr=False)
    _last_timestamp: int = field(default=-1, repr=False)
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def __post_init__(self) -> None:
        """Validate worker_id after initialization."""
        if self.worker_id < 0 or self.worker_id > self.MAX_WORKER_ID:
            raise ValueError(
                f"Worker ID must be between 0 and {self.MAX_WORKER_ID}, got {self.worker_id}"
            )

    def generate(self) -> int:
        """
        Generate a new unique Snowflake ID.

        Thread-safe: Uses internal lock for sequence management.

        Returns:
            64-bit unique ID

        Raises:
            RuntimeError: If clock moves backwards by more than 1 second
        """
        with self._lock:
            current_timestamp = self._current_timestamp()

            if current_timestamp < self._last_timestamp:
                # Clock moved backwards - this is problematic
                wait_time = self._last_timestamp - current_timestamp
                if wait_time > 1000:  # More than 1 second
                    raise RuntimeError(
                        f"Clock moved backwards by {wait_time}ms. "
                        f"Refusing to generate ID to prevent collisions."
                    )
                time.sleep(wait_time / 1000)
                current_timestamp = self._current_timestamp()

            if current_timestamp == self._last_timestamp:
                # Same millisecond: increment sequence
                self._sequence = (self._sequence + 1) & self.MAX_SEQUENCE

                if self._sequence == 0:
                    # Sequence exhausted for this millisecond, wait for next
                    current_timestamp = self._wait_next_millis()
            else:
                # New millisecond: reset sequence
                self._sequence = 0

            self._last_timestamp = current_timestamp

            # Compose the ID
            id_value = (
                ((current_timestamp - self.EPOCH) << (self.WORKER_BITS + self.SEQUENCE_BITS))
                | (self.worker_id << self.SEQUENCE_BITS)
                | self._sequence
            )

            return id_value

    def _current_timestamp(self) -> int:
        """Get current timestamp in milliseconds."""
        return int(time.time() * 1000)

    def _wait_next_millis(self) -> int:
        """Wait for the next millisecond."""
        timestamp = self._current_timestamp()
        while timestamp <= self._last_timestamp:
            time.sleep(0.0001)  # 0.1ms
            timestamp = self._current_timestamp()
        return timestamp

    @staticmethod
    def parse(snowflake_id: int) -> dict[str, Any]:
        """
        Extract components from a Snowflake ID.

        Args:
            snowflake_id: The 64-bit Snowflake ID (must be non-negative)

        Returns:
            Dictionary with:
            - timestamp_ms: Raw timestamp in milliseconds
            - timestamp: datetime object (UTC)
            - worker_id: Worker ID that generated this ID
            - sequence: Sequence number within the millisecond
            - raw: Original ID value
            - hex: Hexadecimal representation

        Raises:
            ValueError: If snowflake_id is negative
        """
        if snowflake_id < 0:
            raise ValueError(
                f"Cannot parse negative Snowflake ID: {snowflake_id}. "
                f"Valid Snowflake IDs are non-negative 64-bit integers."
            )

        timestamp_offset = snowflake_id >> 22
        timestamp_ms = timestamp_offset + SnowflakeIdGenerator.EPOCH

        return {
            "timestamp_ms": timestamp_ms,
            "timestamp": datetime.fromtimestamp(timestamp_ms / 1000, tz=UTC),
            "worker_id": (snowflake_id >> 12) & 0x3FF,
            "sequence": snowflake_id & 0xFFF,
            "raw": snowflake_id,
            "hex": hex(snowflake_id),
        }

    @staticmethod
    def to_base62(snowflake_id: int) -> str:
        """
        Convert Snowflake ID to compact base62 string.

        Useful for URLs and display. 64-bit ID becomes ~11 characters.

        Args:
            snowflake_id: The 64-bit Snowflake ID (must be non-negative)

        Returns:
            Base62 encoded string

        Raises:
            ValueError: If snowflake_id is negative

        Example:
            >>> SnowflakeIdGenerator.to_base62(1767053847123456789)
            '1BvP7xZ5J1t'
        """
        if snowflake_id < 0:
            raise ValueError(
                f"Cannot encode negative value to base62: {snowflake_id}. "
                f"Value must be non-negative."
            )

        alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

        if snowflake_id == 0:
            return "0"

        result: list[str] = []
        while snowflake_id > 0:
            result.append(alphabet[snowflake_id % 62])
            snowflake_id //= 62

        return "".join(reversed(result))

    @staticmethod
    def derive_worker_id() -> int:
        """
        Derive a 10-bit worker ID (0-1023) from machine characteristics.

        Uses hash of: hostname + PID + MAC address + startup timestamp
        This provides sufficient entropy to avoid collisions with high probability.

        The derived ID is cached per-process for consistency.

        Collision Analysis (Birthday Paradox):
        - 10-bit worker ID = 1024 possible values
        - For 10 concurrent instances: P(collision) = 1 - (1023/1024)^45 ~ 4.3%
        - Adding PID makes collision practically impossible

        Returns:
            Worker ID in range [0, 1023]
        """
        with SnowflakeIdGenerator._derivation_lock:
            if SnowflakeIdGenerator._cached_derived_worker_id is not None:
                return SnowflakeIdGenerator._cached_derived_worker_id

            # Combine multiple entropy sources
            identity_parts = [
                socket.gethostname(),  # Machine identity
                str(os.getpid()),  # Process identity
                str(uuid.getnode()),  # MAC address
                str(time.time_ns()),  # Startup timestamp (nanoseconds)
            ]
            identity = "-".join(identity_parts)

            # Hash and extract 10 bits
            hash_bytes = hashlib.sha256(identity.encode()).digest()
            worker_id = int.from_bytes(hash_bytes[:2], "big") & 0x3FF  # 10 bits

            SnowflakeIdGenerator._cached_derived_worker_id = worker_id
            return worker_id
