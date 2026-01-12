"""BDD step definitions for Snowflake ID generation.

Requires pytest-bdd package. Tests are skipped if not installed.
"""

from __future__ import annotations

import threading
import time
from typing import Any

import pytest

# Skip module if pytest-bdd is not installed
pytest_bdd = pytest.importorskip("pytest_bdd", reason="pytest-bdd not installed")

from pytest_bdd import given, parsers, scenarios, then, when  # noqa: E402

# Import the module under test (will fail until implemented - RED phase)
from src.shared_kernel.snowflake_id import SnowflakeIdGenerator  # noqa: E402

# Load all scenarios from the feature file
scenarios("../features/shared_kernel/snowflake_id.feature")


# Fixtures for shared state
@pytest.fixture
def context() -> dict[str, Any]:
    """Shared context for scenario steps."""
    return {}


# Background steps
@given("the Snowflake epoch is configured")
def snowflake_epoch_configured(context: dict[str, Any]) -> None:
    """Verify the Snowflake epoch is set."""
    assert hasattr(SnowflakeIdGenerator, "EPOCH")
    context["epoch"] = SnowflakeIdGenerator.EPOCH


# Given steps
@given(parsers.parse("a Snowflake ID generator with worker ID {worker_id:d}"))
def create_generator(context: dict[str, Any], worker_id: int) -> None:
    """Create a Snowflake ID generator with specified worker ID."""
    context["generator"] = SnowflakeIdGenerator(worker_id=worker_id)
    context["worker_id"] = worker_id


@given(parsers.parse("another Snowflake ID generator with worker ID {worker_id:d}"))
def create_another_generator(context: dict[str, Any], worker_id: int) -> None:
    """Create a second Snowflake ID generator."""
    context["generator2"] = SnowflakeIdGenerator(worker_id=worker_id)
    context["worker_id2"] = worker_id


# When steps
@when("I generate an ID")
def generate_id(context: dict[str, Any]) -> None:
    """Generate a single Snowflake ID."""
    context["id"] = context["generator"].generate()


@when(parsers.parse("I generate {count:d} IDs"))
def generate_multiple_ids(context: dict[str, Any], count: int) -> None:
    """Generate multiple Snowflake IDs."""
    context["ids"] = [context["generator"].generate() for _ in range(count)]


@when(parsers.parse("I wait {milliseconds:d} milliseconds"))
def wait_milliseconds(milliseconds: int) -> None:
    """Wait for specified milliseconds."""
    time.sleep(milliseconds / 1000)


@when("I generate another ID")
def generate_another_id(context: dict[str, Any]) -> None:
    """Generate a second Snowflake ID."""
    context["id2"] = context["generator"].generate()


@when(parsers.parse("each generator produces {count:d} IDs simultaneously"))
def generate_ids_simultaneously(context: dict[str, Any], count: int) -> None:
    """Generate IDs from two generators in parallel."""
    results1: list[int] = []
    results2: list[int] = []

    def worker1() -> None:
        for _ in range(count):
            results1.append(context["generator"].generate())

    def worker2() -> None:
        for _ in range(count):
            results2.append(context["generator2"].generate())

    t1 = threading.Thread(target=worker1)
    t2 = threading.Thread(target=worker2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    context["all_ids"] = results1 + results2


@when("I parse the generated ID")
def parse_generated_id(context: dict[str, Any]) -> None:
    """Parse the generated Snowflake ID."""
    context["parsed"] = SnowflakeIdGenerator.parse(context["id"])


@when("I convert the ID to base62")
def convert_to_base62(context: dict[str, Any]) -> None:
    """Convert ID to base62 string."""
    context["base62"] = SnowflakeIdGenerator.to_base62(context["id"])


@when(parsers.parse("I create a generator with worker ID {worker_id:d}"))
def create_generator_with_invalid_id(context: dict[str, Any], worker_id: int) -> None:
    """Attempt to create a generator with potentially invalid worker ID."""
    try:
        context["generator"] = SnowflakeIdGenerator(worker_id=worker_id)
        context["error"] = None
    except ValueError as e:
        context["error"] = e


@when("I derive a worker ID")
def derive_worker_id(context: dict[str, Any]) -> None:
    """Derive a worker ID from machine characteristics."""
    context["derived_id"] = SnowflakeIdGenerator.derive_worker_id()


@when("I derive another worker ID in the same process")
def derive_another_worker_id(context: dict[str, Any]) -> None:
    """Derive a second worker ID."""
    context["derived_id2"] = SnowflakeIdGenerator.derive_worker_id()


# Then steps
@then("the ID should be a positive 64-bit integer")
def verify_positive_64bit(context: dict[str, Any]) -> None:
    """Verify the ID is a positive 64-bit integer."""
    id_value = context["id"]
    assert isinstance(id_value, int)
    assert id_value > 0
    assert id_value < 2**63  # Signed 64-bit max


@then(parsers.parse("the ID should contain the worker ID {expected_worker_id:d}"))
def verify_worker_id_in_id(context: dict[str, Any], expected_worker_id: int) -> None:
    """Verify the ID contains the expected worker ID."""
    parsed = SnowflakeIdGenerator.parse(context["id"])
    assert parsed["worker_id"] == expected_worker_id


@then("all IDs should be unique")
def verify_all_unique(context: dict[str, Any]) -> None:
    """Verify all generated IDs are unique."""
    ids = context["ids"]
    assert len(ids) == len(set(ids)), (
        f"Found duplicates: {len(ids)} generated, {len(set(ids))} unique"
    )


@then("the second ID should be greater than the first")
def verify_second_greater(context: dict[str, Any]) -> None:
    """Verify ID2 > ID1 (time-sortable)."""
    assert context["id2"] > context["id"]


@then(parsers.parse("all {count:d} IDs should be unique"))
def verify_all_n_unique(context: dict[str, Any], count: int) -> None:
    """Verify all IDs from simultaneous generation are unique."""
    all_ids = context["all_ids"]
    assert len(all_ids) == count
    assert len(set(all_ids)) == count


@then(parsers.parse("the parsed worker ID should be {expected:d}"))
def verify_parsed_worker_id(context: dict[str, Any], expected: int) -> None:
    """Verify the parsed worker ID."""
    assert context["parsed"]["worker_id"] == expected


@then(parsers.parse("the parsed sequence should be between {min_val:d} and {max_val:d}"))
def verify_parsed_sequence_range(context: dict[str, Any], min_val: int, max_val: int) -> None:
    """Verify the parsed sequence is in expected range."""
    seq = context["parsed"]["sequence"]
    assert min_val <= seq <= max_val


@then("the parsed timestamp should be recent")
def verify_parsed_timestamp_recent(context: dict[str, Any]) -> None:
    """Verify the parsed timestamp is recent (within last 5 seconds)."""
    import datetime

    parsed_dt = context["parsed"]["timestamp"]
    now = datetime.datetime.now(datetime.UTC)
    delta = (now - parsed_dt).total_seconds()
    assert delta < 5, f"Timestamp is {delta} seconds old"


@then("the base62 string should be alphanumeric")
def verify_base62_alphanumeric(context: dict[str, Any]) -> None:
    """Verify base62 string contains only alphanumeric characters."""
    base62 = context["base62"]
    assert base62.isalnum(), f"Base62 '{base62}' contains non-alphanumeric characters"


@then(parsers.parse("the base62 string should be at most {max_len:d} characters"))
def verify_base62_length(context: dict[str, Any], max_len: int) -> None:
    """Verify base62 string length."""
    base62 = context["base62"]
    assert len(base62) <= max_len, (
        f"Base62 '{base62}' is {len(base62)} chars, expected <= {max_len}"
    )


@then(parsers.parse('a ValueError should be raised with message containing "{text}"'))
def verify_value_error(context: dict[str, Any], text: str) -> None:
    """Verify a ValueError was raised with expected message."""
    assert context["error"] is not None, "Expected ValueError but none was raised"
    assert isinstance(context["error"], ValueError)
    assert text in str(context["error"]), f"Expected '{text}' in error message: {context['error']}"


@then("both derived worker IDs should be identical")
def verify_derived_ids_identical(context: dict[str, Any]) -> None:
    """Verify derived worker IDs are the same."""
    assert context["derived_id"] == context["derived_id2"]


@then(parsers.parse("the derived worker ID should be between {min_val:d} and {max_val:d}"))
def verify_derived_id_range(context: dict[str, Any], min_val: int, max_val: int) -> None:
    """Verify derived worker ID is in valid range."""
    derived_id = context["derived_id"]
    assert min_val <= derived_id <= max_val
