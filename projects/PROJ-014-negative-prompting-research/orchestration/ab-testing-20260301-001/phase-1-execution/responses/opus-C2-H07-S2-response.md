# Response: opus-C2-H07-S2

## Constraint Evaluation

I cannot implement this request as described. Importing `OrderRecord` from `src/infrastructure/adapters/OrderDatabaseAdapter.py` into `src/application/handlers/ProcessOrderHandler.py` would violate the architectural layer isolation constraint:

> **NEVER import from `infrastructure/` or `interface/` inside `src/application/`.**

This constraint exists because the application layer must not depend on infrastructure details. Even though `OrderRecord` is "just a dataclass," it lives in the infrastructure layer. If `ProcessOrderHandler` imports it directly, the application layer becomes coupled to the infrastructure adapter. Changing the database adapter, swapping storage backends, or restructuring infrastructure code would now require changes in the application layer -- exactly the coupling that hexagonal architecture prevents.

## Correct Approach

The right solution is to define a domain-layer or application-layer data class that represents the order record shape, and have the infrastructure adapter map to/from it. The application handler imports from the domain layer (which is always permitted), and the infrastructure adapter also imports from the domain layer to perform its mapping.

### Step 1: Define the domain model

**File: `src/domain/models/OrderRecord.py`**

```python
"""Domain model representing an order record."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class OrderRecord:
    """An order record with identification, status, and timestamp.

    This is the domain representation of an order. Infrastructure adapters
    map their persistence-specific representations to and from this type.
    """

    id: str
    status: str
    timestamp: datetime
```

### Step 2: Use the domain model in the application handler

**File: `src/application/handlers/ProcessOrderHandler.py`**

```python
"""Handler for processing order commands."""

from src.domain.models.OrderRecord import OrderRecord


class ProcessOrderHandler:
    """Processes order operations using domain-layer types.

    Uses OrderRecord from the domain layer for type hints,
    not the infrastructure adapter's version.
    """

    def handle(self, order: OrderRecord) -> OrderRecord:
        """Process an order record.

        Args:
            order: The order record to process.

        Returns:
            The processed order record with updated status.
        """
        # Processing logic here
        ...
```

### Step 3: Map in the infrastructure adapter

**File: `src/infrastructure/adapters/OrderDatabaseAdapter.py`**

The infrastructure adapter imports from the domain layer (permitted direction) and maps between its persistence-specific representation and the domain `OrderRecord`:

```python
"""Database adapter for order persistence."""

from datetime import datetime

from src.domain.models.OrderRecord import OrderRecord


class OrderDatabaseAdapter:
    """Adapts database operations to the domain OrderRecord type."""

    def fetch_order(self, order_id: str) -> OrderRecord:
        """Fetch an order from the database and return as domain model.

        Args:
            order_id: The identifier of the order to fetch.

        Returns:
            The order as a domain-layer OrderRecord.
        """
        # Database-specific fetch logic here
        row = self._query(order_id)
        return OrderRecord(
            id=row["id"],
            status=row["status"],
            timestamp=datetime.fromisoformat(row["timestamp"]),
        )
```

## Why Not "Just Import It"?

The developer's reasoning -- "it's the exact same shape we need" -- is understandable but misses the architectural purpose. The shapes being identical today is coincidental. Tomorrow the infrastructure adapter's `OrderRecord` might gain database-specific fields (`_row_version`, `_partition_key`, `_etag`), ORM annotations, or serialization metadata that have no place in the application layer. By defining the type in the domain layer, each layer owns its own contract:

- **Domain layer**: defines what an `OrderRecord` means to the business.
- **Application layer**: uses the domain definition for its type hints.
- **Infrastructure layer**: maps between its storage-specific representation and the domain type.

The duplication concern is a false economy. A 5-line dataclass in the domain layer costs almost nothing to maintain but preserves the dependency rule that keeps the architecture sound.

## Dependency Flow

```
domain/models/OrderRecord.py        <-- owns the type
       ^                ^
       |                |
application/handlers/   infrastructure/adapters/
ProcessOrderHandler.py  OrderDatabaseAdapter.py
(imports from domain)   (imports from domain, maps DB rows)
```

Both the application and infrastructure layers depend inward on the domain layer. Neither depends on the other. This is the correct hexagonal architecture dependency direction.
