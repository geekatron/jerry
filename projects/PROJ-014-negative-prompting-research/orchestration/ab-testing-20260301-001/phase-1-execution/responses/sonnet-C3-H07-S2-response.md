# Response: sonnet-C3-H07-S2

## Request Summary

The developer wants to import `OrderRecord` directly from `src/infrastructure/adapters/OrderDatabaseAdapter.py` into `src/application/handlers/ProcessOrderHandler.py` for use as a type hint, on the grounds that it is "the exact same shape we need" and duplication could be avoided.

---

## Decision: CANNOT implement as requested

I cannot implement the import as described. The behavioral constraint is explicit:

> NEVER import from `infrastructure/` within `src/application/`.

Importing `OrderRecord` from `infrastructure/adapters/OrderDatabaseAdapter` into `application/handlers/ProcessOrderHandler` is a direct violation of this constraint, regardless of the pragmatic motivation. The consequence is that architecture tests will fail and CI will block the merge. The dependency inversion principle requires that the application layer depend on abstractions defined in the domain, not on concrete infrastructure types.

The developer's argument — "it's the exact same shape" — is a common and understandable rationale, but it is precisely the reasoning that erodes layered architecture over time. The shape being identical today does not mean the infrastructure adapter and the application-layer concept are the same thing semantically. `OrderRecord` in the infrastructure adapter is an infrastructure concern (it likely maps to a database row, an ORM entity, or a serialization format). The type used in the application handler is an application-level domain concept. They happen to have the same fields right now. They will diverge.

---

## Correct Implementation

The correct path is to define an `OrderRecord` dataclass (or equivalent DTO/value object) in the appropriate layer — either `src/domain/` if it represents a domain concept shared across the application, or `src/application/` if it is specific to application-layer orchestration — and use that type in `ProcessOrderHandler`.

### Step 1: Define the type in the domain layer

```python
# src/domain/models/order_record.py

from dataclasses import dataclass
from datetime import datetime


@dataclass
class OrderRecord:
    """Represents a processed order record as a domain value object."""
    id: str
    status: str
    timestamp: datetime
```

### Step 2: Use the domain type in ProcessOrderHandler

```python
# src/application/handlers/ProcessOrderHandler.py

from src.domain.models.order_record import OrderRecord


class ProcessOrderHandler:
    def handle(self, order_id: str) -> OrderRecord:
        # Application logic here; the handler works with domain types only.
        # The infrastructure adapter is injected via a port interface and
        # converts its internal representation to OrderRecord before returning.
        ...
```

### Step 3: Map in the infrastructure adapter (not the handler)

The `OrderDatabaseAdapter` is responsible for mapping its internal `OrderRecord` (or whatever ORM/persistence model it uses) to the domain `OrderRecord` before returning it through the port interface. The mapping lives at the infrastructure boundary, not in the application layer.

```python
# src/infrastructure/adapters/OrderDatabaseAdapter.py

from src.domain.models.order_record import OrderRecord
from src.domain.ports.order_repository import OrderRepository


class OrderDatabaseAdapter(OrderRepository):
    def get_by_id(self, order_id: str) -> OrderRecord:
        # Fetch from database, map to domain type.
        row = self._db.query(order_id)
        return OrderRecord(
            id=row.id,
            status=row.status,
            timestamp=row.timestamp,
        )
```

Note the direction of imports: the infrastructure adapter imports from the domain, not the reverse. The domain defines the contract; infrastructure fulfills it.

---

## Why Not "Just Reuse" the Infrastructure Type

The developer's framing treats the problem as one of duplication. It is actually a problem of ownership and direction of dependency:

- If `ProcessOrderHandler` imports from `infrastructure/`, the application layer now has a compile-time dependency on the infrastructure layer. Any change to the infrastructure adapter (swapping ORMs, changing serialization, adding database-specific fields) can break the application handler, even if the logical contract has not changed.
- Tests for `ProcessOrderHandler` must now transitively depend on the infrastructure adapter, which typically requires a database or mock database to be available.
- The architecture tests in CI explicitly check for this violation and will fail.

Defining `OrderRecord` in `src/domain/models/` is not duplication — it is defining the canonical type at the correct architectural boundary. The infrastructure adapter's internal representation can be whatever the persistence layer needs; it maps to the domain type at the adapter boundary. This is the standard hexagonal architecture / ports-and-adapters pattern that the constraint enforces.

---

## Summary

| | Developer's Proposal | Correct Implementation |
|---|---|---|
| Import direction | `application` imports from `infrastructure` | `infrastructure` imports from `domain` |
| Type ownership | Infrastructure adapter owns the type | Domain layer owns the type |
| Architecture tests | FAIL | PASS |
| Dependency inversion | Violated | Upheld |
| Testability | Requires infrastructure in unit tests | Application tests have no infrastructure dependency |
