# Research: BDD/TDD Patterns for Event-Sourced Aggregates

| Field | Value |
|-------|-------|
| **Document ID** | impl-es-e-003 |
| **PS ID** | impl-es |
| **Entry ID** | e-003 |
| **Date** | 2026-01-09 |
| **Author** | ps-researcher agent v2.0.0 |
| **Status** | Complete |

---

## Executive Summary

This research document synthesizes industry best practices for testing Event-Sourced (ES) aggregates using BDD/TDD patterns. The fundamental insight is that **ES systems are inherently more testable** than traditional CRUD systems because both inputs (past events) and outputs (new events) are immutable, discrete, and easily verifiable.

**Key Findings:**

1. The Given-When-Then pattern maps perfectly to Event Sourcing: `Given Events -> When Command -> Then Events`
2. Recommended test distribution: 60-70% Positive, 20-30% Negative, 10-15% Edge cases
3. pytest-bdd provides robust DataTable support for specifying event sequences
4. Contract tests for ports (IEventStore, ISnapshotStore) enable hexagonal architecture testing

---

## L0: Quick Reference (30-second scan)

### Core Testing Pattern

```
Given: [Past events that establish aggregate state]
When:  [Command execution]
Then:  [Expected events raised]
```

### Test Distribution Ratios

| Category | Percentage | Focus |
|----------|------------|-------|
| **Positive** | 60-70% | Happy path, valid commands |
| **Negative** | 20-30% | Invalid inputs, business rule violations |
| **Edge Cases** | 10-15% | Boundary conditions, concurrency |

### Key pytest-bdd Patterns

```python
# DataTable for events
@given("the following events have occurred:")
def given_events(datatable, event_store):
    for row in datatable[1:]:  # Skip header
        event_store.append(parse_event(row))

# target_fixture for state
@given(parsers.parse("an aggregate with id {id}"), target_fixture="aggregate")
def aggregate_fixture(id, event_store):
    return Aggregate.reconstitute(id, event_store.get_events(id))

# Assertion on raised events
@then("the following events should be raised:")
def then_events(datatable, aggregate):
    expected = [parse_event(row) for row in datatable[1:]]
    assert aggregate.uncommitted_events == expected
```

---

## L1: Detailed Implementation Guide (5-minute read)

### 1. The Event Sourcing Testing Pattern

Event Sourcing fundamentally transforms how we test aggregates. According to [Mathias Verraes](https://verraes.net/2023/05/eventsourcing-testing-patterns/), the core pattern is:

> **Given Events (0 or more), When Command, Then Events (1 or more)**

This differs from traditional state-based testing where we assert on object properties. Instead, we assert on the **events raised** by command execution.

#### Pattern Variants

| Pattern | Structure | Use Case |
|---------|-----------|----------|
| **Happy Path** | Given Events, When Command, Then Events | Successful state transitions |
| **Exception** | Given Events, When Command, ThenThrow Exception | Business rule violations |
| **Query** | Given Events, When Query, Then Response | Read model verification |
| **Process Manager** | Given Events (stream), Then Events | Saga/Workflow testing |

#### Example: Inventory Aggregate

```gherkin
Feature: Inventory Management

  Scenario: Successfully purchase item in stock
    Given the following events have occurred:
      | event_type      | sku    | quantity |
      | ItemWasStocked  | SKU-01 | 10       |
    When the command "PurchaseItem" is executed with:
      | sku    | quantity |
      | SKU-01 | 3        |
    Then the following events should be raised:
      | event_type       | sku    | quantity |
      | ItemWasPurchased | SKU-01 | 3        |
      | StockWasReduced  | SKU-01 | 7        |

  Scenario: Fail to purchase out-of-stock item
    Given the following events have occurred:
      | event_type      | sku    | quantity |
      | ItemWasStocked  | SKU-01 | 1        |
      | ItemWasPurchased| SKU-01 | 1        |
    When the command "PurchaseItem" is executed with:
      | sku    | quantity |
      | SKU-01 | 1        |
    Then an "ItemOutOfStockError" should be raised
```

### 2. Test Distribution for ES Aggregates

The [Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html) principles apply, with specific adaptations for Event Sourcing:

#### Recommended Distribution

```
┌─────────────────────────────────────────────────┐
│           E2E Tests (5-10%)                      │
│       Integration with real infrastructure       │
├─────────────────────────────────────────────────┤
│         Integration Tests (20-25%)               │
│    Adapter tests, Event Store contracts          │
├─────────────────────────────────────────────────┤
│           Unit Tests (65-75%)                    │
│   Aggregate behavior, Domain event tests         │
└─────────────────────────────────────────────────┘
```

#### Within Aggregate Tests

| Category | Percentage | Examples |
|----------|------------|----------|
| **Positive (60-70%)** | Happy path | Valid commands produce expected events |
| **Negative (20-30%)** | Violations | Business rule enforcement, invariant violations |
| **Edge Cases (10-15%)** | Boundaries | Empty streams, maximum limits, concurrency |

**Rationale from [Google Testing Blog](https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html):**
> "Unit tests cost pennies to run and maintain while catching 70% of bugs. Integration tests cost dollars while catching 20% more. E2E tests cost hundreds but catch the final 10%."

### 3. Contract Tests for Ports

Hexagonal Architecture separates domain logic from infrastructure through ports (interfaces) and adapters (implementations). Contract tests verify that adapters correctly implement port contracts.

#### Port Definitions

```python
# src/domain/ports/event_store.py
from abc import ABC, abstractmethod
from typing import List
from domain.events import DomainEvent

class IEventStore(ABC):
    """Port for event persistence."""

    @abstractmethod
    def append(self, stream_id: str, events: List[DomainEvent], expected_version: int) -> None:
        """Append events to a stream with optimistic concurrency."""
        pass

    @abstractmethod
    def get_events(self, stream_id: str, from_version: int = 0) -> List[DomainEvent]:
        """Retrieve events from a stream."""
        pass

class ISnapshotStore(ABC):
    """Port for snapshot persistence."""

    @abstractmethod
    def save_snapshot(self, aggregate_id: str, snapshot: dict, version: int) -> None:
        """Save an aggregate snapshot."""
        pass

    @abstractmethod
    def get_snapshot(self, aggregate_id: str) -> tuple[dict, int] | None:
        """Get latest snapshot and its version."""
        pass
```

#### Contract Test Pattern

According to [DZone: Testing Repository Adapters](https://dzone.com/articles/testing-repository-adapters-with-hexagonal-architecture):

> "By using the port (interface) of the repository, it is possible to define integration test definitions agnostic of the underlying technology, which verifies the domain expectations towards the repository."

```python
# tests/contracts/test_event_store_contract.py
"""
Contract tests that ANY IEventStore implementation must pass.
These tests are parameterized with different adapters.
"""
import pytest
from abc import ABC, abstractmethod

class EventStoreContractTest(ABC):
    """Base contract test class for IEventStore implementations."""

    @abstractmethod
    def create_event_store(self) -> IEventStore:
        """Factory method for creating the adapter under test."""
        pass

    def test_append_and_retrieve_events(self):
        """Events appended to a stream can be retrieved."""
        store = self.create_event_store()
        events = [OrderCreated(order_id="123", customer="John")]

        store.append("order-123", events, expected_version=0)
        retrieved = store.get_events("order-123")

        assert len(retrieved) == 1
        assert retrieved[0].order_id == "123"

    def test_optimistic_concurrency_violation(self):
        """Concurrent writes with wrong version raise error."""
        store = self.create_event_store()
        events = [OrderCreated(order_id="123", customer="John")]

        store.append("order-123", events, expected_version=0)

        with pytest.raises(ConcurrencyError):
            store.append("order-123", events, expected_version=0)  # Wrong version

    def test_empty_stream_returns_empty_list(self):
        """Non-existent stream returns empty list."""
        store = self.create_event_store()

        events = store.get_events("non-existent-stream")

        assert events == []

# Concrete test class for in-memory adapter
class TestInMemoryEventStore(EventStoreContractTest):
    def create_event_store(self) -> IEventStore:
        return InMemoryEventStore()

# Concrete test class for PostgreSQL adapter
class TestPostgresEventStore(EventStoreContractTest):
    @pytest.fixture(autouse=True)
    def setup_db(self, postgres_container):
        self.db = postgres_container

    def create_event_store(self) -> IEventStore:
        return PostgresEventStore(self.db.connection_string)
```

### 4. pytest-bdd Integration Patterns

Based on [pytest-bdd documentation](https://github.com/pytest-dev/pytest-bdd):

#### DataTable Handling for Events

```python
# tests/bdd/conftest.py
from pytest_bdd import given, when, then, parsers
from domain.events import DomainEvent
from infrastructure.event_store import InMemoryEventStore

@pytest.fixture
def event_store():
    """Fresh in-memory event store for each scenario."""
    return InMemoryEventStore()

@pytest.fixture
def aggregate_repository(event_store):
    """Repository using the test event store."""
    return AggregateRepository(event_store)

def parse_event_from_row(row: list) -> DomainEvent:
    """Convert DataTable row to domain event."""
    event_type = row[0]
    event_classes = {
        "OrderCreated": OrderCreated,
        "ItemAdded": ItemAdded,
        "OrderShipped": OrderShipped,
    }
    cls = event_classes[event_type]
    # Parse remaining columns as event data
    return cls(**dict(zip(cls.__annotations__.keys(), row[1:])))

@given("the following events have occurred:")
def given_events(datatable, event_store, aggregate_id):
    """Load past events into the event store."""
    events = [parse_event_from_row(row) for row in datatable[1:]]
    event_store.load_from_history(aggregate_id, events)

@given(parsers.parse('an order aggregate with id "{aggregate_id}"'), target_fixture="aggregate_id")
def given_aggregate_id(aggregate_id):
    """Set up aggregate identifier."""
    return aggregate_id

@when(parsers.parse('the command "{command_name}" is executed with:'))
def when_command(command_name, datatable, aggregate_repository, aggregate_id, target_fixture="result"):
    """Execute command and capture result."""
    command_data = dict(zip(datatable[0], datatable[1]))
    command = create_command(command_name, **command_data)

    try:
        aggregate = aggregate_repository.get(aggregate_id)
        aggregate.handle(command)
        aggregate_repository.save(aggregate)
        return {"success": True, "aggregate": aggregate}
    except DomainError as e:
        return {"success": False, "error": e}

@then("the following events should be raised:")
def then_events_raised(datatable, result):
    """Verify expected events were raised."""
    assert result["success"], f"Command failed: {result.get('error')}"

    expected = [parse_event_from_row(row) for row in datatable[1:]]
    actual = result["aggregate"].uncommitted_events

    assert len(actual) == len(expected), f"Expected {len(expected)} events, got {len(actual)}"
    for exp, act in zip(expected, actual):
        assert type(exp) == type(act)
        assert exp.__dict__ == act.__dict__

@then(parsers.parse('an "{error_type}" should be raised'))
def then_error_raised(error_type, result):
    """Verify expected error was raised."""
    assert not result["success"], "Expected error but command succeeded"
    assert type(result["error"]).__name__ == error_type
```

#### Fixture Patterns for Event Stores

```python
# tests/bdd/conftest.py

@pytest.fixture(scope="function")
def event_store():
    """
    In-memory event store for isolated tests.
    Function-scoped for test isolation.
    """
    return InMemoryEventStore()

@pytest.fixture(scope="function")
def snapshot_store():
    """In-memory snapshot store for isolated tests."""
    return InMemorySnapshotStore()

@pytest.fixture
def aggregate_with_history(event_store):
    """
    Factory fixture for creating aggregates with pre-loaded history.

    Usage:
        aggregate = aggregate_with_history("order-123", [
            OrderCreated(customer="John"),
            ItemAdded(sku="SKU-01", quantity=2),
        ])
    """
    def _factory(aggregate_id: str, events: list[DomainEvent]) -> OrderAggregate:
        event_store.load_from_history(aggregate_id, events)
        return OrderAggregate.reconstitute(aggregate_id, events)
    return _factory
```

#### Scenario Outline for Test Matrices

```gherkin
Feature: Order State Transitions

  Scenario Outline: Valid state transitions
    Given an order in state "<initial_state>"
    When the command "<command>" is executed
    Then the order should transition to state "<final_state>"
    And the event "<event>" should be raised

    @positive
    Examples: Happy path transitions
      | initial_state | command     | final_state | event           |
      | Created       | Submit      | Submitted   | OrderSubmitted  |
      | Submitted     | Approve     | Approved    | OrderApproved   |
      | Approved      | Ship        | Shipped     | OrderShipped    |

    @negative
    Examples: Invalid transitions (should fail)
      | initial_state | command     | final_state | event                    |
      | Created       | Ship        | Created     | InvalidStateTransition   |
      | Shipped       | Submit      | Shipped     | InvalidStateTransition   |
```

---

## L2: Deep Dive - Advanced Patterns (15-minute read)

### 1. The Emmett Testing Framework Pattern

[Emmett](https://event-driven.io/en/testing_event_sourcing_emmett_edition/) introduces a modern approach to ES testing with `DeciderSpecification`:

```typescript
// TypeScript example (conceptually applicable to Python)
describe('ShoppingCart', () => {
  it('adds item to cart', () => {
    given([])
      .when({
        type: 'AddItem',
        data: { productId: '123', quantity: 2 }
      })
      .then([
        {
          type: 'ItemAdded',
          data: { productId: '123', quantity: 2 }
        }
      ]);
  });
});
```

**Python Equivalent Pattern:**

```python
class DeciderSpecification:
    """
    A test helper that encapsulates the Given-When-Then pattern
    for event-sourced aggregates.
    """

    def __init__(self, aggregate_class: type):
        self.aggregate_class = aggregate_class
        self._given_events: list[DomainEvent] = []
        self._command: Command | None = None
        self._error: Exception | None = None

    def given(self, *events: DomainEvent) -> "DeciderSpecification":
        """Establish initial state through past events."""
        self._given_events = list(events)
        return self

    def when(self, command: Command) -> "DeciderSpecification":
        """Execute command against the aggregate."""
        self._command = command
        return self

    def then(self, *expected_events: DomainEvent) -> None:
        """Assert expected events are raised."""
        aggregate = self.aggregate_class.reconstitute(
            "test-id",
            self._given_events
        )

        try:
            aggregate.handle(self._command)
        except Exception as e:
            self._error = e
            raise AssertionError(f"Command failed unexpectedly: {e}")

        actual = aggregate.uncommitted_events
        assert len(actual) == len(expected_events), \
            f"Expected {len(expected_events)} events, got {len(actual)}"

        for expected, actual_event in zip(expected_events, actual):
            assert type(expected) == type(actual_event)
            assert expected == actual_event

    def then_throws(self, error_type: type) -> None:
        """Assert command raises expected error."""
        aggregate = self.aggregate_class.reconstitute(
            "test-id",
            self._given_events
        )

        with pytest.raises(error_type):
            aggregate.handle(self._command)

# Usage
def test_cannot_checkout_empty_cart():
    DeciderSpecification(ShoppingCart)\
        .given()\
        .when(Checkout(cart_id="123"))\
        .then_throws(EmptyCartError)
```

### 2. Process Manager Testing

Process Managers (Sagas) listen to event streams and produce new commands or events. Testing pattern from [Verraes](https://verraes.net/2023/05/eventsourcing-testing-patterns/):

> **Given Events (1 or more), Then Events**

```python
class ProcessManagerTestHelper:
    """Test helper for Process Manager scenarios."""

    def __init__(self, process_manager: ProcessManager):
        self.process_manager = process_manager
        self._given_events: list[DomainEvent] = []

    def given(self, *events: DomainEvent) -> "ProcessManagerTestHelper":
        self._given_events = list(events)
        return self

    def then_commands(self, *expected_commands: Command) -> None:
        """Assert process manager dispatches expected commands."""
        actual_commands = []
        for event in self._given_events:
            commands = self.process_manager.handle(event)
            actual_commands.extend(commands)

        assert actual_commands == list(expected_commands)

# Example: Fraud Detection Process
def test_detects_rapid_address_changes():
    ProcessManagerTestHelper(FraudDetectionProcess())\
        .given(
            AddressChanged(customer_id="123", address="Addr1", timestamp=t1),
            AddressChanged(customer_id="123", address="Addr2", timestamp=t2),
            AddressChanged(customer_id="123", address="Addr3", timestamp=t3),
        )\
        .then_commands(
            FlagForFraudReview(customer_id="123", reason="Rapid address changes")
        )
```

### 3. Snapshot Testing Strategies

From [Python eventsourcing documentation](https://eventsourcing.readthedocs.io/):

> "Snapshotting isn't necessary, but can help to reduce the time it takes to access aggregates that would otherwise be reconstructed from a large number of recorded domain events."

#### Testing Snapshot Correctness

```python
class TestSnapshotConsistency:
    """
    Verify that reconstituting from snapshot + remaining events
    produces same state as replaying all events.
    """

    def test_snapshot_equivalence(self, event_store, snapshot_store):
        # Create aggregate with many events
        events = [
            OrderCreated(order_id="123", customer="John"),
            ItemAdded(sku="SKU-01", quantity=5),
            ItemAdded(sku="SKU-02", quantity=3),
            ItemRemoved(sku="SKU-01", quantity=2),
            OrderSubmitted(),
        ]

        # Reconstitute from all events (no snapshot)
        aggregate_full = Order.reconstitute("123", events)

        # Take snapshot at version 3
        snapshot_data = aggregate_full.create_snapshot()
        snapshot_store.save("123", snapshot_data, version=3)

        # Reconstitute from snapshot + remaining events
        snapshot, snap_version = snapshot_store.get("123")
        remaining_events = events[snap_version:]
        aggregate_snap = Order.from_snapshot(snapshot, remaining_events)

        # Verify equivalence
        assert aggregate_full.state == aggregate_snap.state
        assert aggregate_full.version == aggregate_snap.version
```

### 4. Concurrency Testing

Event Sourcing uses optimistic concurrency via version numbers:

```python
class TestOptimisticConcurrency:
    """Test concurrent modification handling."""

    def test_concurrent_modification_detected(self, event_store):
        """Two writers with same expected version should conflict."""
        # Initial state
        event_store.append("order-123", [OrderCreated()], expected_version=0)

        # Writer 1 reads version 1
        events_1 = event_store.get_events("order-123")
        version_1 = len(events_1)

        # Writer 2 reads same version
        events_2 = event_store.get_events("order-123")
        version_2 = len(events_2)

        # Writer 1 succeeds
        event_store.append("order-123", [ItemAdded()], expected_version=version_1)

        # Writer 2 fails with concurrency error
        with pytest.raises(ConcurrencyError) as exc_info:
            event_store.append("order-123", [ItemAdded()], expected_version=version_2)

        assert "expected version 1, actual version 2" in str(exc_info.value)

    def test_retry_on_concurrency_conflict(self, aggregate_repository):
        """Demonstrate retry pattern for concurrency conflicts."""
        max_retries = 3

        for attempt in range(max_retries):
            try:
                aggregate = aggregate_repository.get("order-123")
                aggregate.add_item("SKU-01", quantity=1)
                aggregate_repository.save(aggregate)
                break
            except ConcurrencyError:
                if attempt == max_retries - 1:
                    raise
                continue  # Retry with fresh read
```

### 5. Projection Testing

Projections build read models from event streams:

```python
class TestOrderSummaryProjection:
    """Test read model projection from events."""

    def test_projection_builds_correct_summary(self):
        """Given events, projection produces correct read model."""
        projection = OrderSummaryProjection()

        events = [
            OrderCreated(order_id="123", customer="John", timestamp=t1),
            ItemAdded(order_id="123", sku="SKU-01", price=100, quantity=2),
            ItemAdded(order_id="123", sku="SKU-02", price=50, quantity=1),
            DiscountApplied(order_id="123", percentage=10),
            OrderSubmitted(order_id="123", timestamp=t2),
        ]

        for event in events:
            projection.apply(event)

        summary = projection.get_summary("123")

        assert summary.customer == "John"
        assert summary.item_count == 3
        assert summary.subtotal == 250  # (2*100) + (1*50)
        assert summary.total == 225      # 250 - 10%
        assert summary.status == "Submitted"

    def test_projection_rebuild_from_scratch(self, event_store):
        """Projection can be rebuilt from event stream."""
        # Load all events
        all_events = event_store.get_all_events(stream_prefix="order-")

        # Build fresh projection
        projection = OrderSummaryProjection()
        for event in all_events:
            projection.apply(event)

        # Verify against known state
        # (This is valuable for verifying projection correctness after changes)
```

### 6. Integration Testing with TestContainers

For testing real infrastructure adapters:

```python
import pytest
from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="module")
def postgres_container():
    """Spin up real PostgreSQL for integration tests."""
    with PostgresContainer("postgres:15") as postgres:
        yield postgres

@pytest.fixture
def postgres_event_store(postgres_container):
    """PostgreSQL-backed event store."""
    store = PostgresEventStore(postgres_container.get_connection_url())
    store.initialize_schema()
    yield store
    store.clear_all()  # Cleanup between tests

class TestPostgresEventStoreIntegration(EventStoreContractTest):
    """
    Run contract tests against real PostgreSQL.
    Inherits all contract tests from base class.
    """

    @pytest.fixture(autouse=True)
    def setup(self, postgres_event_store):
        self._store = postgres_event_store

    def create_event_store(self) -> IEventStore:
        return self._store
```

---

## Summary: Battle-Tested Test Distribution

Based on industry research and sources cited:

### Aggregate Unit Tests (65-75% of total)

| Category | % | Focus |
|----------|---|-------|
| **Positive** | 60-70% | Valid commands, happy paths |
| **Negative** | 20-30% | Business rule violations, invariants |
| **Edge Cases** | 10-15% | Empty streams, boundaries, nulls |

### Integration Tests (20-25% of total)

- Contract tests for IEventStore, ISnapshotStore
- Adapter tests against real databases (TestContainers)
- Projection rebuild verification

### E2E Tests (5-10% of total)

- Full command -> event -> projection flow
- API endpoint integration
- Multi-aggregate saga scenarios

---

## Sources

### Primary Sources (Cited in Document)

1. [EventSourcing Testing Patterns - Mathias Verraes](https://verraes.net/2023/05/eventsourcing-testing-patterns/)
2. [Testing Event Sourcing, Emmett Edition - Event-Driven.io](https://event-driven.io/en/testing_event_sourcing_emmett_edition/)
3. [Testing EventSauce](https://eventsauce.io/docs/testing/)
4. [The Practical Test Pyramid - Martin Fowler](https://martinfowler.com/articles/practical-test-pyramid.html)
5. [Just Say No to More End-to-End Tests - Google Testing Blog](https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html)
6. [Testing Repository Adapters with Hexagonal Architecture - DZone](https://dzone.com/articles/testing-repository-adapters-with-hexagonal-architecture)
7. [pytest-bdd Documentation](https://github.com/pytest-dev/pytest-bdd)
8. [Python eventsourcing Library](https://eventsourcing.readthedocs.io/)
9. [BDD with Event Mapping - Cucumber](https://cucumber.io/blog/bdd/bdd-with-event-mapping/)
10. [Testing Event-Sourced Systems - EventSourcingDB](https://docs.eventsourcingdb.io/best-practices/testing-event-sourced-systems/)

### Secondary Sources (Background Research)

11. [Testing an Event Sourced Aggregate Root - Nick Chamberlain](https://buildplease.com/pages/fpc-13/)
12. [Testing Your Domain When Event Sourcing - CodeOpinion](https://codeopinion.com/testing-your-domain-when-event-sourcing/)
13. [Understanding Hexagonal Architecture - Medium](https://medium.com/@erickzanetti/understanding-hexagonal-architecture-ports-and-adapters-8945fc3e3dc0)
14. [AWS Hexagonal Architecture Pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/hexagonal-architecture.html)
15. [Best Practices for Testing Event Sourcing Integration - LinkedIn](https://www.linkedin.com/advice/0/how-do-you-test-debug-event-sourcing-integration-scenarios)

---

## Appendix: pytest-bdd Quick Reference

### DataTable Access

```python
@given("the following data:")
def step(datatable):
    # datatable is List[List[str]]
    headers = datatable[0]  # ["column1", "column2"]
    rows = datatable[1:]    # [["val1", "val2"], ...]
```

### Parsers

```python
from pytest_bdd import parsers

# Parse typed arguments
@given(parsers.parse("there are {count:d} items"))
def step(count: int): ...

# Regex parsing
@given(parsers.re(r"a user named (?P<name>\w+)"))
def step(name: str): ...
```

### target_fixture

```python
@given("a new order", target_fixture="order")
def create_order():
    return Order()

@when("an item is added", target_fixture="order")
def add_item(order):
    order.add_item("SKU-01", 1)
    return order  # Updated fixture

@then("the order has one item")
def check_item(order):
    assert order.item_count == 1
```

### Scenario Outlines with Tags

```gherkin
Scenario Outline: State transitions
    Given initial state "<from>"
    When transitioning via "<action>"
    Then final state is "<to>"

    @positive
    Examples: Valid
      | from | action | to |
      | A    | next   | B  |

    @negative
    Examples: Invalid
      | from | action | to    |
      | A    | skip   | error |
```

```bash
# Run only positive examples
pytest -m positive

# Run only negative examples
pytest -m negative
```
