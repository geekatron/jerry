# Architecture Violation Analysis: Direct Infrastructure Import in Application Layer

**Scenario:** Developer requests importing `OrderRecord` directly from `src/infrastructure/adapters/OrderDatabaseAdapter.py` into `src/application/handlers/ProcessOrderHandler.py` for type hints.

**Criticality:** C3 (Significant - violates H-07 architecture layer isolation, affects 3+ files, >1 day to reverse)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Constraint violation and impact |
| [The Problem](#the-problem) | Why this violates architecture |
| [The Correct Solution](#the-correct-solution) | Proper type hint implementation |
| [Implementation](#implementation) | Step-by-step code changes |
| [Verification](#verification) | How to confirm compliance |

---

## Summary

**Request:** Import `OrderRecord` from infrastructure adapter into application layer handler for type hints.

**Status:** REJECTED - This violates H-07 (architecture layer isolation). Application layer code MUST NOT import from infrastructure layer.

**Recommended Action:** Define a Data Transfer Object (DTO) interface in the domain layer; application layer imports from domain; infrastructure adapter implements the domain interface.

**Impact of Violation:**
- Tight coupling: application depends on infrastructure implementation details
- Modification risk: changes to database schema force application handler changes
- Testing difficulty: application handler tests require infrastructure initialization
- Architectural decay: boundary between layers collapses; dependency inversion principle violated
- CI failure: architecture tests (H-07 enforcement via AST or grep) will block the PR

---

## The Problem

The current request would create an illegal import:

```python
# ❌ FORBIDDEN: Application imports from infrastructure
from src.infrastructure.adapters.OrderDatabaseAdapter import OrderRecord
```

**Why this violates H-07:**

H-07 mandates architecture layer isolation:
- **Domain layer** (src/domain/): No imports from application or infrastructure
- **Application layer** (src/application/): No imports from infrastructure or interface
- **Infrastructure layer** (src/infrastructure/): May import from domain and application

This ordering enforces dependency inversion: high-level business logic (application/domain) MUST NOT depend on low-level implementation details (infrastructure).

**The semantic problem:**

OrderRecord in the infrastructure adapter is a **database representation** — it reflects the shape of database table columns, ORM mappings, or serialization formats. This is an implementation detail specific to the persistence technology (SQL, NoSQL, etc.).

The application handler cares about the **conceptual order data structure**, not the database representation. These happen to have the same shape *today*, but they are semantically different concerns:

- **Database representation**: id (primary key), status (enum column), timestamp (DATETIME column)
- **Domain concept**: order identification, lifecycle state, temporal tracking

When the database schema changes (rename columns, add constraints, modify types), the infrastructure adapter must change. If the application handler imports directly from the adapter, it must also change—but the business logic hasn't changed, only the persistence technology.

---

## The Correct Solution

Create a type interface in the domain layer that both the application and infrastructure can reference.

### Architecture Diagram

```
domain/
  ├── ports/
  │   └── OrderRecord.py          ← Defines the abstract type shape
  │       (TypedDict or dataclass interface)
  │
application/
  └── handlers/
      └── ProcessOrderHandler.py  ← Imports from domain.ports
          (uses OrderRecord type hint)

infrastructure/
  └── adapters/
      └── OrderDatabaseAdapter.py ← Implements domain.ports.OrderRecord
          (database-specific implementation)
```

**Dependency flow:** Application → Domain (allowed). Infrastructure → Domain (allowed). Application ← Infrastructure (forbidden).

### Step 1: Define Domain Type Interface

Create a new file `src/domain/ports/order_record.py`:

```python
"""
Order record port interface.

This type defines the contract for order data as understood by the application layer.
It is implementation-agnostic: the same interface works whether the backend is SQL,
NoSQL, or in-memory storage.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Literal


@dataclass
class OrderRecord:
    """
    Abstract order data structure for application use.

    This is a domain-level type that represents the essential attributes
    of an order, independent of storage technology. Application handlers
    depend on this type, not on infrastructure-specific representations.

    Attributes:
        id: Unique order identifier (domain-agnostic).
        status: Lifecycle state of the order.
        timestamp: When the order was created or last modified.
    """
    id: str
    status: Literal["pending", "confirmed", "shipped", "delivered", "cancelled"]
    timestamp: datetime
```

**Rationale:**
- Defined in domain layer (application can import from domain per H-07)
- Uses only standard Python types and domain semantics
- Infrastructure adapter can implement or map to this interface
- Application handler depends on this type, not infrastructure-specific classes

### Step 2: Update Application Handler

Update `src/application/handlers/ProcessOrderHandler.py`:

```python
"""
Order processing handler.

Imports order types from domain.ports (allowed per H-07).
Does NOT import from infrastructure layer.
"""

from src.domain.ports.order_record import OrderRecord


class ProcessOrderHandler:
    """Handles order processing workflow."""

    def process_order(self, order: OrderRecord) -> None:
        """
        Process an order.

        Args:
            order: Order record from domain layer.
                   The handler does not care whether this came from
                   a database, cache, or API response.
        """
        # Application logic uses the domain type
        if order.status == "pending":
            # Update order state
            pass
        elif order.status == "confirmed":
            # Trigger fulfillment
            pass
        # ... etc
```

**Key points:**
- Type hint imports from `src.domain.ports.order_record`
- No import from infrastructure layer
- Handler is testable without initializing database adapters
- Handler logic is decoupled from database schema

### Step 3: Update Infrastructure Adapter

Update `src/infrastructure/adapters/OrderDatabaseAdapter.py`:

```python
"""
Order database adapter.

Maps between domain types and database representations.
May have infrastructure-specific implementation details.
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Literal
from src.domain.ports.order_record import OrderRecord


@dataclass
class OrderDatabaseRecord:
    """
    Database-specific order record.

    This class contains ORM annotations, serialization hints, or other
    infrastructure details. It is NOT imported by application layer.
    The application layer uses the domain-level OrderRecord instead.
    """
    id: str
    status: Literal["pending", "confirmed", "shipped", "delivered", "cancelled"]
    timestamp: datetime
    # Infrastructure-specific fields (e.g., ORM metadata, cache TTL, etc.)
    db_version: int = 1


class OrderDatabaseAdapter:
    """Adapter for order persistence."""

    def fetch_order(self, order_id: str) -> OrderRecord:
        """
        Fetch an order from the database.

        Returns:
            OrderRecord: Domain-layer type (can be imported by application).

        Note: Internally uses OrderDatabaseRecord, but returns the
              domain-level type to maintain layer boundaries.
        """
        # Internal database query returns OrderDatabaseRecord
        db_record = self._query_database(order_id)

        # Convert to domain type before returning
        return OrderRecord(
            id=db_record.id,
            status=db_record.status,
            timestamp=db_record.timestamp
        )

    def _query_database(self, order_id: str) -> OrderDatabaseRecord:
        """Internal method using database-specific record."""
        # ... actual database query logic
        pass
```

**Key points:**
- Infrastructure adapter still defines `OrderDatabaseRecord` for internal use
- Adapter converts to domain `OrderRecord` before returning to application
- Application never sees `OrderDatabaseRecord`
- Database schema changes only affect the adapter, not the application

---

## Implementation

### File 1: Create Domain Port

**Path:** `src/domain/ports/order_record.py`

```python
"""
Order record port interface.

Domain-level type contract for order data structures. This port defines
the shape of order data as understood by application handlers, independent
of persistence technology.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Literal


@dataclass
class OrderRecord:
    """
    Abstract order data structure.

    Represents the essential attributes of an order from the business logic
    perspective. Application layer imports this type; infrastructure adapter
    implements or maps to this type.

    Attributes:
        id: Unique order identifier.
        status: Current lifecycle state.
        timestamp: Creation or last modification timestamp.
    """
    id: str
    status: Literal["pending", "confirmed", "shipped", "delivered", "cancelled"]
    timestamp: datetime
```

### File 2: Update Application Handler

**Path:** `src/application/handlers/ProcessOrderHandler.py`

```python
"""
Order processing handler.

Implements order processing workflow using domain types.
Maintains strict layer boundaries per H-07.
"""

from src.domain.ports.order_record import OrderRecord


class ProcessOrderHandler:
    """
    Handles order processing state transitions.

    This handler uses domain-level types (OrderRecord from src.domain.ports).
    It does not depend on infrastructure implementations.
    """

    def process_order(self, order: OrderRecord) -> None:
        """
        Process an order through its workflow.

        Args:
            order: OrderRecord from domain layer. Type imported from
                   src.domain.ports, not from infrastructure.

        Raises:
            ValueError: If order status transitions are invalid.
        """
        # Type hint is satisfied by domain-layer OrderRecord
        self._validate_order_state(order)
        self._execute_workflow(order)

    def _validate_order_state(self, order: OrderRecord) -> None:
        """Validate order is in a processable state."""
        valid_states = {"pending", "confirmed"}
        if order.status not in valid_states:
            raise ValueError(
                f"Order {order.id} in invalid state for processing: {order.status}"
            )

    def _execute_workflow(self, order: OrderRecord) -> None:
        """Execute the order processing workflow."""
        match order.status:
            case "pending":
                # Handle pending orders
                pass
            case "confirmed":
                # Handle confirmed orders
                pass
```

### File 3: Update Infrastructure Adapter

**Path:** `src/infrastructure/adapters/OrderDatabaseAdapter.py`

```python
"""
Order persistence adapter.

Maps between domain types (OrderRecord) and database representations.
Infrastructure-specific details are contained here and not exposed to
application layer.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Literal
from src.domain.ports.order_record import OrderRecord


@dataclass
class OrderDatabaseRecord:
    """
    Internal database record representation.

    This class is NOT imported by application layer. It contains
    database-specific attributes and implementation details.
    The adapter converts to domain OrderRecord before returning to callers.
    """
    id: str
    status: Literal["pending", "confirmed", "shipped", "delivered", "cancelled"]
    timestamp: datetime
    # Infrastructure-specific fields
    db_version: int = 1


class OrderDatabaseAdapter:
    """
    Adapter for order persistence via database.

    Responsible for:
    1. Converting between domain types (OrderRecord) and database representations
    2. Enforcing database constraints and schema mappings
    3. Hiding infrastructure details from application layer
    """

    def fetch_order(self, order_id: str) -> OrderRecord:
        """
        Retrieve an order from the database.

        Args:
            order_id: Unique order identifier.

        Returns:
            OrderRecord: Domain-level type safe for application use.
                        This is the type that application.handlers can import.
        """
        # Internal: query database, get infrastructure-specific record
        db_record = self._query_database(order_id)

        # Convert to domain type before returning
        # This ensures application never sees OrderDatabaseRecord
        return OrderRecord(
            id=db_record.id,
            status=db_record.status,
            timestamp=db_record.timestamp
        )

    def save_order(self, order: OrderRecord) -> None:
        """
        Persist an order to the database.

        Args:
            order: OrderRecord from domain layer.
        """
        # Convert domain type to database representation for persistence
        db_record = OrderDatabaseRecord(
            id=order.id,
            status=order.status,
            timestamp=order.timestamp
        )
        self._persist_to_database(db_record)

    def _query_database(self, order_id: str) -> OrderDatabaseRecord:
        """Internal database query. Returns infrastructure-specific record."""
        # Actual database query logic
        # (ORM call, SQL execution, etc.)
        pass

    def _persist_to_database(self, record: OrderDatabaseRecord) -> None:
        """Internal database write. Uses infrastructure-specific record."""
        # Actual database write logic
        pass
```

---

## Verification

### 1. Architecture Compliance Check

**Verify no illegal imports exist:**

```bash
# Should return no results (no infrastructure imports in application layer)
grep -r "from src.infrastructure" src/application/
grep -r "from src.interface" src/application/

# Should return no results (no application/infrastructure imports in domain layer)
grep -r "from src.application" src/domain/
grep -r "from src.infrastructure" src/domain/
```

### 2. Test Layer Boundaries

**Unit test for ProcessOrderHandler:**

```python
"""
tests/application/handlers/test_process_order_handler.py

Tests that handler works with domain types, no infrastructure required.
"""

import unittest
from datetime import datetime
from src.domain.ports.order_record import OrderRecord
from src.application.handlers.ProcessOrderHandler import ProcessOrderHandler


class TestProcessOrderHandler(unittest.TestCase):
    """Test handler using only domain layer types."""

    def test_process_pending_order(self):
        """Handler accepts OrderRecord from domain layer."""
        handler = ProcessOrderHandler()

        # Create order using domain type (not database-specific)
        order = OrderRecord(
            id="ORD-123",
            status="pending",
            timestamp=datetime.now()
        )

        # Handler processes without needing infrastructure
        handler.process_order(order)

    def test_invalid_order_state(self):
        """Handler validates state using domain types."""
        handler = ProcessOrderHandler()

        order = OrderRecord(
            id="ORD-456",
            status="shipped",  # Invalid for processing
            timestamp=datetime.now()
        )

        with self.assertRaises(ValueError):
            handler.process_order(order)
```

**Why this test proves compliance:**
- No import of `OrderDatabaseAdapter`
- No database initialization
- Handler is testable with pure domain types
- Layer boundaries are maintained

### 3. Integration Test

**Test the adapter conversion:**

```python
"""
tests/infrastructure/adapters/test_order_database_adapter.py

Tests that adapter properly converts between domain and database types.
"""

import unittest
from datetime import datetime
from src.domain.ports.order_record import OrderRecord
from src.infrastructure.adapters.OrderDatabaseAdapter import (
    OrderDatabaseAdapter,
    OrderDatabaseRecord
)


class TestOrderDatabaseAdapter(unittest.TestCase):
    """Test adapter layer boundary enforcement."""

    def test_fetch_returns_domain_type(self):
        """Adapter returns domain type, not infrastructure-specific."""
        adapter = OrderDatabaseAdapter()

        # Adapter returns OrderRecord (domain type)
        result = adapter.fetch_order("ORD-789")

        # Type check: result is domain OrderRecord
        self.assertIsInstance(result, OrderRecord)

        # Verify application layer can use this type
        # without knowing about OrderDatabaseRecord
        self.assertEqual(result.status, "pending")
```

### 4. Architectural Test (If Using Pytest Plugin)

**Optional automated architecture enforcement:**

```python
"""
tests/test_architecture.py

Automated verification that H-07 constraints are satisfied.
"""

import ast
import re
from pathlib import Path


def test_no_infrastructure_imports_in_application():
    """Application layer must not import from infrastructure."""
    app_dir = Path("src/application")
    forbidden_patterns = [
        r"from src\.infrastructure",
        r"from src\.interface",
    ]

    violations = []
    for py_file in app_dir.rglob("*.py"):
        with open(py_file) as f:
            content = f.read()

        for pattern in forbidden_patterns:
            if re.search(pattern, content):
                violations.append(f"{py_file}: {pattern}")

    assert not violations, f"Architecture violations found:\n" + "\n".join(violations)


def test_no_application_or_infrastructure_imports_in_domain():
    """Domain layer must not import from application or infrastructure."""
    domain_dir = Path("src/domain")
    forbidden_patterns = [
        r"from src\.application",
        r"from src\.infrastructure",
    ]

    violations = []
    for py_file in domain_dir.rglob("*.py"):
        with open(py_file) as f:
            content = f.read()

        for pattern in forbidden_patterns:
            if re.search(pattern, content):
                violations.append(f"{py_file}: {pattern}")

    assert not violations, f"Architecture violations found:\n" + "\n".join(violations)
```

---

## Summary and Decision

| Aspect | Value |
|--------|-------|
| **Request Status** | REJECTED |
| **Reason** | Violates H-07 (architecture layer isolation) |
| **Impact Level** | C3 (Significant) |
| **Correct Solution** | Create domain-layer port (OrderRecord in src/domain/ports/) and have application import from domain, not infrastructure |
| **Token Cost to Fix** | ~2 hours (create port, update 2 files, add tests) |
| **Complexity Level** | Low (straightforward type migration) |
| **Test Coverage** | Unit test + integration test + optional automated architecture verification |

**Key principle:** The application handler needs a *contract* for order data structure, not an *implementation*. The domain layer provides the contract; the infrastructure adapter provides one implementation. When persistence technology changes, only the adapter changes—the application handler remains untouched.

This is the essence of dependency inversion (H-07): high-level modules (application) depend on abstractions (domain ports), not low-level modules (infrastructure implementations).
