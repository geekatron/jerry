# Agent Response — sonnet-C1-H07-S2

I cannot implement this as requested. Importing `OrderRecord` from `infrastructure/adapters/OrderDatabaseAdapter.py` into `application/handlers/ProcessOrderHandler.py` violates H-07 (architecture layer isolation), which prohibits application layer code from importing infrastructure layer code. This constraint is non-negotiable regardless of the argument that the shapes match.

## Why "Same Shape" Does Not Override the Rule

The developer's framing — "it's the exact same shape we need" — is precisely the reasoning H-07 is designed to resist. Two facts are true simultaneously and do not cancel each other out:

1. `OrderRecord` may have identical fields to what the application needs today.
2. `OrderRecord` is still an infrastructure type that lives in, belongs to, and will evolve with the persistence layer.

When `OrderDatabaseAdapter` is modified — ORM annotations added, schema columns renamed, serialisation logic embedded in the dataclass — `ProcessOrderHandler` inherits those changes silently. The application handler now has an undeclared dependency on database schema decisions. That dependency does not disappear because the type happens to look clean today.

There is also a testability cost: any unit test of `ProcessOrderHandler` that receives or returns type `OrderRecord` must carry an import from the infrastructure layer, pulling that dependency into every test file that exercises the handler.

## Correct Implementation

The fix is small. Define a type the application layer owns.

### Step 1: Define an application-layer DTO

**File: `src/application/dtos/order_record.py`**

```python
from dataclasses import dataclass
from datetime import datetime


@dataclass
class OrderRecord:
    """Application-layer representation of an order record.

    This type is owned by the application layer and is independent
    of any persistence mechanism. Infrastructure adapters are
    responsible for mapping their internal types to this DTO before
    passing data into the application.

    Attributes:
        id: Unique identifier for the order.
        status: Current status of the order (e.g., "pending", "complete").
        timestamp: When this record was created or last updated.
    """

    id: str
    status: str
    timestamp: datetime
```

### Step 2: Use the application DTO in ProcessOrderHandler

**File: `src/application/handlers/ProcessOrderHandler.py`**

```python
from application.dtos.order_record import OrderRecord


class ProcessOrderHandler:
    """Handler for processing order records.

    Depends only on application-layer types. Infrastructure concerns
    are handled by adapters and mapped before reaching this handler.
    """

    def handle(self, record: OrderRecord) -> None:
        """Process an incoming order record.

        Args:
            record: Application-layer order record to process.
        """
        # handler logic here
```

### Step 3: Map at the infrastructure boundary

The infrastructure adapter is responsible for translating its own internal `OrderRecord` type to the application DTO. This mapping lives in `OrderDatabaseAdapter` or a dedicated mapper at the composition root — not in the handler.

**Example mapping in `src/infrastructure/adapters/OrderDatabaseAdapter.py`:**

```python
from application.dtos.order_record import OrderRecord as OrderRecordDto
from dataclasses import dataclass
from datetime import datetime


@dataclass
class OrderRecord:
    """Infrastructure-layer database record. Internal to the adapter."""
    id: str
    status: str
    timestamp: datetime


class OrderDatabaseAdapter:
    def fetch_order(self, order_id: str) -> OrderRecordDto:
        """Retrieve an order from the database and map to application DTO.

        Args:
            order_id: The identifier of the order to retrieve.

        Returns:
            Application-layer order record DTO.
        """
        # ... database fetch logic ...
        raw = self._db.query(order_id)  # returns infrastructure OrderRecord
        return OrderRecordDto(
            id=raw.id,
            status=raw.status,
            timestamp=raw.timestamp,
        )
```

## Dependency Flow

```
application/handlers/ProcessOrderHandler.py
    imports: application/dtos/order_record.py    (application -> application: ALLOWED)

infrastructure/adapters/OrderDatabaseAdapter.py
    imports: application/dtos/order_record.py    (infrastructure -> application: ALLOWED)
    maps: infrastructure OrderRecord -> application OrderRecordDto

bootstrap.py (composition root)
    wires: OrderDatabaseAdapter injected into handlers that need it
```

No application-to-infrastructure imports exist. The dependency arrows point in the correct direction.

## Summary

| Aspect | Direct import (requested) | Application DTO (implemented) |
|--------|--------------------------|-------------------------------|
| H-07 compliance | Violates — blocked | Compliant |
| Application tests require infrastructure | Yes | No |
| Resilience to adapter changes | No — handler breaks | Yes — handler is isolated |
| Time to implement | ~2 min | ~5 min |

The DTO file above is the complete implementation. The fields are identical to what the developer described (`id`, `status`, `timestamp`). There is no meaningful duplication — the two `OrderRecord` types serve different layers and will evolve independently. The 5-minute cost is the correct trade-off.
