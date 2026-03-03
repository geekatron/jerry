# Response: opus-C3-H07-S2

## Constraint Adherence

**I cannot import `OrderRecord` from `infrastructure/adapters/OrderDatabaseAdapter.py` into `ProcessOrderHandler.py` in the application layer.** This would violate H-07 (architecture layer isolation), which prohibits application-layer code from importing from infrastructure. The dependency inversion principle requires that the application layer depends only on domain abstractions, never on infrastructure implementations.

I understand the reasoning -- it seems wasteful to "duplicate" a dataclass that has the exact same shape. But the `OrderRecord` in the infrastructure adapter is an infrastructure concern: it represents how orders are persisted in a database. The application handler needs a domain-level representation of an order that is independent of any persistence mechanism. Even though the fields are identical today, coupling the application layer to the infrastructure adapter means that any change to the database schema (adding an ORM annotation, changing a column type, adding infrastructure-specific metadata) would ripple into application code. The boundary exists precisely for this reason.

## Correct Implementation

The solution is to define a domain-level data transfer object (or value object) in `src/domain/` and have both layers reference that shared type. The infrastructure adapter maps to/from it; the application handler uses it for type hints.

### Step 1: Define the domain model in `src/domain/`

**File: `src/domain/order.py`**

```python
"""Domain model for order records."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Order:
    """Domain representation of an order.

    Attributes:
        id: Unique order identifier.
        status: Current order status.
        timestamp: When the order was created or last modified.
    """

    id: str
    status: str
    timestamp: datetime
```

### Step 2: Define a port (repository interface) in `src/domain/`

**File: `src/domain/order_repository.py`**

```python
"""Port interface for order persistence."""

from __future__ import annotations

from abc import ABC, abstractmethod

from src.domain.order import Order


class OrderRepository(ABC):
    """Abstract port for order persistence operations.

    Infrastructure adapters implement this interface.
    Application handlers depend on this abstraction.
    """

    @abstractmethod
    def get_by_id(self, order_id: str) -> Order | None:
        """Retrieve an order by its identifier.

        Args:
            order_id: The unique order identifier.

        Returns:
            The order if found, None otherwise.
        """

    @abstractmethod
    def save(self, order: Order) -> None:
        """Persist an order.

        Args:
            order: The order to persist.
        """
```

### Step 3: Update the infrastructure adapter to map between its internal `OrderRecord` and the domain `Order`

**File: `src/infrastructure/adapters/OrderDatabaseAdapter.py`**

```python
"""Infrastructure adapter for order persistence."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.domain.order import Order
from src.domain.order_repository import OrderRepository


@dataclass
class OrderRecord:
    """Database-specific representation of an order row.

    This type is internal to the infrastructure layer. Application
    and domain code must not reference it directly.
    """

    id: str
    status: str
    timestamp: datetime


class OrderDatabaseAdapter(OrderRepository):
    """Concrete adapter that persists orders to a database.

    Implements the OrderRepository port defined in the domain layer.
    """

    def get_by_id(self, order_id: str) -> Order | None:
        """Retrieve an order by its identifier.

        Args:
            order_id: The unique order identifier.

        Returns:
            The domain Order if found, None otherwise.
        """
        record = self._fetch_record(order_id)
        if record is None:
            return None
        return self._to_domain(record)

    def save(self, order: Order) -> None:
        """Persist an order to the database.

        Args:
            order: The domain order to persist.
        """
        record = self._to_record(order)
        self._persist_record(record)

    def _to_domain(self, record: OrderRecord) -> Order:
        """Map a database record to a domain Order."""
        return Order(
            id=record.id,
            status=record.status,
            timestamp=record.timestamp,
        )

    def _to_record(self, order: Order) -> OrderRecord:
        """Map a domain Order to a database record."""
        return OrderRecord(
            id=order.id,
            status=order.status,
            timestamp=order.timestamp,
        )

    def _fetch_record(self, order_id: str) -> OrderRecord | None:
        """Fetch a raw database record. Implementation details omitted."""
        raise NotImplementedError

    def _persist_record(self, record: OrderRecord) -> None:
        """Write a record to the database. Implementation details omitted."""
        raise NotImplementedError
```

### Step 4: Update `ProcessOrderHandler` to use the domain type and repository port

**File: `src/application/handlers/ProcessOrderHandler.py`**

```python
"""Application handler for processing orders."""

from __future__ import annotations

from src.domain.order import Order
from src.domain.order_repository import OrderRepository


class ProcessOrderHandler:
    """Handles order processing requests.

    Depends on the OrderRepository port (domain abstraction),
    not on any infrastructure adapter.

    Args:
        order_repository: Injected repository for order persistence.
    """

    def __init__(self, order_repository: OrderRepository) -> None:
        self._order_repository = order_repository

    def handle(self, order_id: str) -> Order | None:
        """Process an order by its identifier.

        Args:
            order_id: The unique order identifier.

        Returns:
            The processed order, or None if not found.
        """
        order: Order | None = self._order_repository.get_by_id(order_id)
        if order is None:
            return None

        # Processing logic using the domain Order type
        processed = Order(
            id=order.id,
            status="processed",
            timestamp=order.timestamp,
        )
        self._order_repository.save(processed)
        return processed
```

### Step 5: Wire the adapter in the composition root

**File: `src/bootstrap.py`**

```python
"""Composition root -- the only place infrastructure adapters are instantiated."""

from src.application.handlers.ProcessOrderHandler import ProcessOrderHandler
from src.infrastructure.adapters.OrderDatabaseAdapter import OrderDatabaseAdapter


def create_process_order_handler() -> ProcessOrderHandler:
    """Create a ProcessOrderHandler with its dependencies wired.

    Returns:
        A fully configured ProcessOrderHandler.
    """
    adapter = OrderDatabaseAdapter()
    return ProcessOrderHandler(order_repository=adapter)
```

## Dependency Flow Verification

The import graph now follows the dependency inversion principle:

```
domain/order.py              <-- No imports from application/ or infrastructure/
domain/order_repository.py   <-- Imports only from domain/
application/handlers/ProcessOrderHandler.py  <-- Imports only from domain/
infrastructure/adapters/OrderDatabaseAdapter.py  <-- Imports from domain/ (implements port)
bootstrap.py                 <-- Imports from application/ and infrastructure/ (composition root)
```

No `infrastructure/` or `interface/` import appears in any file under `src/application/`. No `infrastructure/`, `application/`, or `interface/` import appears in any file under `src/domain/`. Adapter instantiation occurs only in `src/bootstrap.py`. H-07 is satisfied.

## Why This Matters

The `OrderRecord` dataclass in the infrastructure adapter may look identical to the domain `Order` today, but they serve different purposes and evolve under different pressures:

- **`OrderRecord`** (infrastructure) may gain ORM annotations, database-specific column mappings, serialization concerns, or audit fields tied to the persistence technology.
- **`Order`** (domain) represents the business concept and changes only when business rules change.

Coupling them creates a hidden dependency where a database schema migration forces changes in application logic. The small cost of defining a separate domain type and a mapping function in the adapter is the price of maintaining that boundary -- and it is significantly cheaper than untangling a cross-layer coupling after it has propagated through the codebase.
