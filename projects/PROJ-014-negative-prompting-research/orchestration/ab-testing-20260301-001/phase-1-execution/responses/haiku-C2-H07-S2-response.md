# Response: ProcessOrderHandler OrderRecord Type Hint Request

**Scenario:** Developer requests that `ProcessOrderHandler` (application layer) directly import `OrderRecord` from `OrderDatabaseAdapter` (infrastructure layer) for type hints, avoiding DTO duplication.

**Decision:** REJECT this request and require a DTO in the application layer instead.

---

## Constraint Analysis

### H-07(b) Violation

The request directly violates **H-07(b)** from `architecture-standards.md`:

> `src/application/` MUST NOT import from `infrastructure/` or `interface/`

**Reference:**
```
| Layer | Can Import | MUST NOT Import |
|-------|-----------|-----------------|
| `application/` | domain | infrastructure, interface |
```

The request is proposing:
```python
# ProcessOrderHandler.py (application layer)
from src.infrastructure.adapters.OrderDatabaseAdapter import OrderRecord  # ❌ VIOLATION
```

This creates a direct reverse dependency from application → infrastructure, breaking the hexagonal architecture's directional discipline.

---

## Why This Violation Matters

### 1. Architectural Layering Breakdown

The hexagonal architecture enforces unidirectional dependencies:
- **Domain** (innermost): Knows nothing about outer layers
- **Application**: Knows about domain only; calls ports (interfaces) not adapters
- **Infrastructure** (outermost): Implements ports for domain/application use

Allowing application to import infrastructure types inverts this: infrastructure types now leak inward, polluting the application boundary.

### 2. Coupling Risk

If `OrderRecord` changes (fields added, removed, or renamed), `ProcessOrderHandler` breaks directly. The application layer becomes coupled to infrastructure implementation details rather than using stable abstractions (DTOs, domain entities, ports).

### 3. Testing and Substitution

When testing `ProcessOrderHandler`, you cannot substitute a test double for the database adapter if the application layer imports its concrete types. The constraint makes dependency injection and testing harder.

### 4. Port Boundary Violation

The correct pattern requires:
1. Domain defines a **port** (interface) for order persistence
2. Application uses that port interface for type hints
3. Infrastructure implements that port with the concrete `OrderRecord` adapter

Skipping the port means the application cannot work with multiple database implementations without code changes.

---

## The Correct Solution

Instead of importing from infrastructure, create a **DTO (Data Transfer Object)** in the application layer:

### Step 1: Create Application DTO

**File:** `src/application/dtos/order_dto.py`

```python
"""Order DTO for application-layer type contracts."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class OrderDTO:
    """DTO representing order data.

    This DTO decouples the application layer from infrastructure types.
    Infrastructure adapters convert their concrete types (e.g., OrderRecord)
    to this DTO at the boundary.
    """
    id: str
    status: str
    timestamp: datetime
```

### Step 2: Update ProcessOrderHandler

**File:** `src/application/handlers/ProcessOrderHandler.py`

```python
"""Process order command handler."""

from src.application.dtos.order_dto import OrderDTO
from src.application.ports.order_repository import IOrderRepository
from src.domain.commands.process_order_command import ProcessOrderCommand


class ProcessOrderHandler:
    """Handler for ProcessOrderCommand."""

    def __init__(self, order_repository: IOrderRepository):
        self.order_repository = order_repository

    def handle(self, command: ProcessOrderCommand) -> OrderDTO:
        """Process an order and return its current state as DTO."""
        order_data: OrderDTO = self.order_repository.get_order(command.order_id)

        # Process order logic here
        return order_data
```

### Step 3: Update Infrastructure Adapter

**File:** `src/infrastructure/adapters/OrderDatabaseAdapter.py`

```python
"""Database adapter for order persistence."""

from dataclasses import dataclass
from datetime import datetime

from src.application.dtos.order_dto import OrderDTO
from src.application.ports.order_repository import IOrderRepository


@dataclass
class OrderRecord:
    """Internal database record representation."""
    id: str
    status: str
    timestamp: datetime


class OrderDatabaseAdapter(IOrderRepository):
    """Implements IOrderRepository using a database."""

    def get_order(self, order_id: str) -> OrderDTO:
        """Retrieve order from database and convert to DTO."""
        # Query database, get OrderRecord
        record: OrderRecord = self._query_database(order_id)

        # Convert internal record to DTO at boundary
        return OrderDTO(
            id=record.id,
            status=record.status,
            timestamp=record.timestamp
        )

    def _query_database(self, order_id: str) -> OrderRecord:
        """Internal database query returning OrderRecord."""
        # Database query implementation
        pass
```

### Step 4: Define Port Interface

**File:** `src/application/ports/order_repository.py`

```python
"""Port definition for order repository."""

from abc import ABC, abstractmethod

from src.application.dtos.order_dto import OrderDTO


class IOrderRepository(ABC):
    """Port for order persistence queries."""

    @abstractmethod
    def get_order(self, order_id: str) -> OrderDTO:
        """Retrieve an order by ID, returning a DTO."""
        pass
```

---

## Dependency Flow (Correct)

```
ProcessOrderHandler (application)
    ↓ (depends on)
IOrderRepository (application port)
    ↑ (implements)
OrderDatabaseAdapter (infrastructure)
    → (contains) OrderRecord (infrastructure-internal)
```

**Key points:**
- ProcessOrderHandler knows about `IOrderRepository` (port) and `OrderDTO` (DTO) only
- OrderDatabaseAdapter knows about both the port and OrderRecord
- OrderRecord never crosses the application boundary
- ProcessOrderHandler can be tested with a mock repository returning DTOs

---

## Addressing the Developer's Concern

**Developer's concern:** "The OrderRecord dataclass with id, status, and timestamp is already defined exactly as we need it. Duplicating it as a DTO seems wasteful."

**Response:** This is not true duplication; it is boundary definition. The DTO serves a different purpose:

1. **OrderRecord** = internal schema of the database adapter (infrastructure concern)
2. **OrderDTO** = application contract for order data (application concern)

Even if they have identical fields today, they evolve independently:
- Database might add `created_at`, `updated_at`, database indexes → OrderRecord changes
- Application might need `owner_id`, `cost_breakdown` for business logic → OrderDTO changes

The DTO is not "the same shape"—it is a deliberately stable shape at the application boundary. This is a core principle of hexagonal architecture and prevents infrastructure leaks.

---

## Summary

| Aspect | Status |
|--------|--------|
| **Direct infrastructure import** | ❌ Violates H-07(b) |
| **Architecture compliance** | ❌ Breaks hexagonal layer isolation |
| **Testability** | ❌ Makes mocking/substitution harder |
| **Coupling** | ❌ Couples application to infrastructure types |
| **Correct approach** | ✅ Application DTO + Port interface |
| **Implementation effort** | Low (~20 lines of code) |

**Action:** Implement the DTO pattern above. If the developer remains concerned about code duplication, document the architectural rationale in an ADR explaining why boundary DTOs are necessary despite identical field shapes.
