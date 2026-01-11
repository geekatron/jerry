"""Unit tests for shared_kernel.snowflake_id module.

These tests complement the BDD scenarios with additional edge cases
and technical validations.
"""

from __future__ import annotations

import threading
import time
from datetime import UTC, datetime

import pytest

# Import will fail until implemented - this is RED phase
from src.shared_kernel.snowflake_id import SnowflakeIdGenerator


class TestSnowflakeIdGeneratorCreation:
    """Tests for SnowflakeIdGenerator initialization."""

    def test_create_with_valid_worker_id(self) -> None:
        """Generator accepts valid worker ID."""
        generator = SnowflakeIdGenerator(worker_id=1)
        assert generator.worker_id == 1

    def test_create_with_min_worker_id(self) -> None:
        """Generator accepts minimum worker ID (0)."""
        generator = SnowflakeIdGenerator(worker_id=0)
        assert generator.worker_id == 0

    def test_create_with_max_worker_id(self) -> None:
        """Generator accepts maximum worker ID (1023)."""
        generator = SnowflakeIdGenerator(worker_id=1023)
        assert generator.worker_id == 1023

    def test_negative_worker_id_rejected(self) -> None:
        """Generator rejects negative worker ID."""
        with pytest.raises(ValueError, match="Worker ID"):
            SnowflakeIdGenerator(worker_id=-1)

    def test_worker_id_too_large_rejected(self) -> None:
        """Generator rejects worker ID > 1023."""
        with pytest.raises(ValueError, match="Worker ID"):
            SnowflakeIdGenerator(worker_id=1024)


class TestSnowflakeIdGeneration:
    """Tests for Snowflake ID generation."""

    def test_generate_returns_positive_int(self) -> None:
        """Generate returns a positive integer."""
        generator = SnowflakeIdGenerator(worker_id=1)
        id_value = generator.generate()
        assert isinstance(id_value, int)
        assert id_value > 0

    def test_generate_returns_64_bit_int(self) -> None:
        """Generated ID fits in 64 bits."""
        generator = SnowflakeIdGenerator(worker_id=1)
        id_value = generator.generate()
        assert id_value < 2**63  # Signed 64-bit max

    def test_generate_unique_ids_same_worker(self) -> None:
        """IDs from same worker are unique."""
        generator = SnowflakeIdGenerator(worker_id=1)
        ids = [generator.generate() for _ in range(10000)]
        assert len(ids) == len(set(ids))

    def test_generate_unique_ids_different_workers(self) -> None:
        """IDs from different workers are unique."""
        gen1 = SnowflakeIdGenerator(worker_id=1)
        gen2 = SnowflakeIdGenerator(worker_id=2)
        ids1 = [gen1.generate() for _ in range(1000)]
        ids2 = [gen2.generate() for _ in range(1000)]
        all_ids = ids1 + ids2
        assert len(all_ids) == len(set(all_ids))

    def test_time_sortable(self) -> None:
        """IDs generated later are larger."""
        generator = SnowflakeIdGenerator(worker_id=1)
        id1 = generator.generate()
        time.sleep(0.01)  # 10ms
        id2 = generator.generate()
        assert id2 > id1

    def test_thread_safety(self) -> None:
        """Multiple threads can generate IDs concurrently."""
        generator = SnowflakeIdGenerator(worker_id=1)
        results: list[int] = []
        lock = threading.Lock()

        def worker() -> None:
            for _ in range(100):
                id_value = generator.generate()
                with lock:
                    results.append(id_value)

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(results) == 1000
        assert len(set(results)) == 1000  # All unique


class TestSnowflakeIdParsing:
    """Tests for Snowflake ID parsing."""

    def test_parse_extracts_worker_id(self) -> None:
        """Parse extracts correct worker ID."""
        generator = SnowflakeIdGenerator(worker_id=742)
        id_value = generator.generate()
        parsed = SnowflakeIdGenerator.parse(id_value)
        assert parsed["worker_id"] == 742

    def test_parse_extracts_sequence(self) -> None:
        """Parse extracts sequence number."""
        generator = SnowflakeIdGenerator(worker_id=1)
        id_value = generator.generate()
        parsed = SnowflakeIdGenerator.parse(id_value)
        assert 0 <= parsed["sequence"] <= 4095

    def test_parse_extracts_timestamp(self) -> None:
        """Parse extracts timestamp as datetime."""
        generator = SnowflakeIdGenerator(worker_id=1)
        id_value = generator.generate()
        parsed = SnowflakeIdGenerator.parse(id_value)
        assert isinstance(parsed["timestamp"], datetime)
        assert parsed["timestamp"].tzinfo == UTC

    def test_parse_roundtrip(self) -> None:
        """Parsed components match generation parameters."""
        worker_id = 500
        generator = SnowflakeIdGenerator(worker_id=worker_id)
        id_value = generator.generate()
        parsed = SnowflakeIdGenerator.parse(id_value)

        assert parsed["worker_id"] == worker_id
        assert parsed["raw"] == id_value
        assert "hex" in parsed

    def test_parse_includes_hex(self) -> None:
        """Parse includes hex representation."""
        generator = SnowflakeIdGenerator(worker_id=1)
        id_value = generator.generate()
        parsed = SnowflakeIdGenerator.parse(id_value)
        assert parsed["hex"].startswith("0x")


class TestSnowflakeIdBase62:
    """Tests for base62 conversion."""

    def test_to_base62_returns_string(self) -> None:
        """to_base62 returns a string."""
        generator = SnowflakeIdGenerator(worker_id=1)
        id_value = generator.generate()
        base62 = SnowflakeIdGenerator.to_base62(id_value)
        assert isinstance(base62, str)

    def test_to_base62_alphanumeric(self) -> None:
        """to_base62 result is alphanumeric."""
        generator = SnowflakeIdGenerator(worker_id=1)
        id_value = generator.generate()
        base62 = SnowflakeIdGenerator.to_base62(id_value)
        assert base62.isalnum()

    def test_to_base62_compact(self) -> None:
        """to_base62 result is at most 11 characters."""
        generator = SnowflakeIdGenerator(worker_id=1)
        id_value = generator.generate()
        base62 = SnowflakeIdGenerator.to_base62(id_value)
        assert len(base62) <= 11

    def test_to_base62_zero(self) -> None:
        """to_base62 handles zero."""
        base62 = SnowflakeIdGenerator.to_base62(0)
        assert base62 == "0"


class TestWorkerIdDerivation:
    """Tests for worker ID derivation."""

    def test_derive_worker_id_in_range(self) -> None:
        """Derived worker ID is in valid range."""
        worker_id = SnowflakeIdGenerator.derive_worker_id()
        assert 0 <= worker_id <= 1023

    def test_derive_worker_id_deterministic(self) -> None:
        """Derived worker ID is deterministic per process."""
        id1 = SnowflakeIdGenerator.derive_worker_id()
        id2 = SnowflakeIdGenerator.derive_worker_id()
        assert id1 == id2

    def test_derive_worker_id_returns_int(self) -> None:
        """Derived worker ID is an integer."""
        worker_id = SnowflakeIdGenerator.derive_worker_id()
        assert isinstance(worker_id, int)


class TestSnowflakeIdNegative:
    """Negative tests for SnowflakeIdGenerator.

    These tests verify proper error handling for invalid inputs.
    Per battle-tested ratios: 20-30% of tests should be negative.
    """

    def test_parse_negative_snowflake_id(self) -> None:
        """Parse rejects negative Snowflake ID.

        Negative IDs cannot exist in valid Snowflake generation, so
        attempting to parse them should fail clearly rather than
        producing undefined results.
        """
        with pytest.raises(ValueError, match="negative|invalid"):
            SnowflakeIdGenerator.parse(-1)

    def test_parse_large_negative_snowflake_id(self) -> None:
        """Parse rejects large negative Snowflake ID."""
        with pytest.raises(ValueError, match="negative|invalid"):
            SnowflakeIdGenerator.parse(-9223372036854775808)  # Min int64

    def test_to_base62_negative_input(self) -> None:
        """to_base62 rejects negative input.

        Negative values cannot be represented in base62 encoding
        without a sign convention, which we do not support.
        """
        with pytest.raises(ValueError, match="negative|non-negative"):
            SnowflakeIdGenerator.to_base62(-1)

    def test_to_base62_large_negative_input(self) -> None:
        """to_base62 rejects large negative input."""
        with pytest.raises(ValueError, match="negative|non-negative"):
            SnowflakeIdGenerator.to_base62(-9999999999)

    def test_generate_overflow_protection(self) -> None:
        """Generator produces valid IDs under high throughput.

        Generates many IDs to test sequence rollover handling.
        All IDs must remain positive and within 64-bit bounds.
        """
        generator = SnowflakeIdGenerator(worker_id=1023)
        for _ in range(5000):
            id_val = generator.generate()
            assert id_val > 0, "Generated ID must be positive"
            assert id_val < 2**63, "Generated ID must fit in signed 64-bit"


class TestSnowflakeIdConstants:
    """Tests for Snowflake ID constants."""

    def test_epoch_is_set(self) -> None:
        """EPOCH constant is defined."""
        assert hasattr(SnowflakeIdGenerator, "EPOCH")
        assert SnowflakeIdGenerator.EPOCH > 0

    def test_worker_bits_is_10(self) -> None:
        """WORKER_BITS is 10."""
        assert SnowflakeIdGenerator.WORKER_BITS == 10

    def test_sequence_bits_is_12(self) -> None:
        """SEQUENCE_BITS is 12."""
        assert SnowflakeIdGenerator.SEQUENCE_BITS == 12

    def test_max_worker_id(self) -> None:
        """MAX_WORKER_ID is 1023."""
        assert SnowflakeIdGenerator.MAX_WORKER_ID == 1023

    def test_max_sequence(self) -> None:
        """MAX_SEQUENCE is 4095."""
        assert SnowflakeIdGenerator.MAX_SEQUENCE == 4095
