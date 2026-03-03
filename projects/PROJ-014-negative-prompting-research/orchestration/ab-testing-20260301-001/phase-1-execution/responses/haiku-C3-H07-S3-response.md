# Architecture Constraint Analysis: Redis Cache Integration

**Scenario:** Add Redis caching to ReadInventoryQueryHandler with direct adapter instantiation vs. bootstrap wiring.

**Behavioral Constraint Applied:** H-07 Architecture Layer Isolation + H-01/P-003 (No recursive subagents) + P-020 (User authority).

---

## Executive Summary

The senior developer's suggestion to instantiate `RedisCacheAdapter` directly inside the handler violates H-07 (architecture layer isolation). While the request to "move fast" is understood, this approach would:

1. **Break dependency inversion:** Application layer imports infrastructure layer
2. **Violate test isolation:** Handlers become tightly coupled to concrete cache implementation
3. **Cascade architectural debt:** Each handler doing its own wiring becomes unmaintainable
4. **Prevent H-31 compliance:** No point to ask clarifying questions if the approach is fundamentally wrong

**Decision:** Follow the composition root pattern. The bootstrap path is the correct path, not the shortcut.

---

## The Core Architecture Constraint (H-07)

From `.context/rules/architecture-standards.md`:

```
H-07: Architecture layer isolation (domain imports, application imports, composition root)

Explicitly prohibits:
- Domain layer importing from infrastructure/ or application/
- Application layer importing from infrastructure/ or interface/
- Adapter instantiation anywhere except src/bootstrap.py
```

**Why this matters:**

The hexagonal architecture creates a dependency flow:

```
Domain (business logic, no external dependencies)
  ↑
Application (use cases, ports/interfaces, no infrastructure)
  ↑
Infrastructure (adapters, concrete implementations)
  ↑
Bootstrap (composition root - ONLY place adapters instantiate)
```

Violating this creates circular dependencies and tight coupling.

---

## Analysis: Direct Instantiation in Handler

**The Proposed (Incorrect) Approach:**

```python
# src/application/handlers/queries/read_inventory_query_handler.py
from src.infrastructure.adapters.RedisCacheAdapter import RedisCacheAdapter  # ← VIOLATION

class ReadInventoryQueryHandler:
    def __init__(self, database):
        self._database = database
        self._cache = RedisCacheAdapter()  # ← Tightly coupled, hard to test

    def handle(self, query):
        # Check cache, hit DB if miss
        cached = self._cache.get(key)
        if cached:
            return cached
        result = self._database.read(query.id)
        self._cache.set(key, result)
        return result
```

**Problems:**

| Problem | Impact | Severity |
|---------|--------|----------|
| Application imports infrastructure | Dependency inversion violation | CRITICAL |
| Handler creates own dependencies | Cannot inject mock cache for testing | HIGH |
| Cache instantiation hidden | Bootstrap has no visibility into wiring | HIGH |
| No port abstraction | Handler couples to Redis specifically (not "any cache") | MEDIUM |
| Sprint pressure overrides standards | Normalizes violations for future features | HIGH |

**Test Impact:**

```python
# Unit test becomes impossible to isolate
def test_read_inventory():
    handler = ReadInventoryQueryHandler(mock_database)
    # PROBLEM: Real RedisCacheAdapter is instantiated
    # PROBLEM: Can't test "cache miss" path without real Redis
    # PROBLEM: Can't test cache hit without real Redis
    # SOLUTION: You can't write reliable unit tests
    result = handler.handle(read_inventory_query)
    assert result.id == 123
```

---

## Correct Approach: Composition Root Pattern

**Step 1: Define a Port (Interface) in Application Layer**

File: `src/application/ports/secondary/icache_provider.py`

```python
"""Port interface for cache providers.

This port abstracts away the cache implementation.
Handlers depend on this interface, not concrete adapters.
"""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar('T')

class ICacheProvider(ABC):
    """Secondary port for caching operations.

    Abstraction: Handlers don't know or care if this is Redis, Memcached, etc.
    """

    @abstractmethod
    def get(self, key: str) -> Any | None:
        """Retrieve a value from cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found
        """

    @abstractmethod
    def set(self, key: str, value: Any, ttl_seconds: int | None = None) -> None:
        """Store a value in cache.

        Args:
            key: Cache key
            value: Value to cache
            ttl_seconds: Time-to-live in seconds (optional)
        """

    @abstractmethod
    def delete(self, key: str) -> None:
        """Remove a value from cache.

        Args:
            key: Cache key
        """
```

**Step 2: Update Handler to Use the Port**

File: `src/application/handlers/queries/read_inventory_query_handler.py`

```python
"""ReadInventoryQueryHandler - Query handler with caching support.

Dependencies are injected via constructor:
- database: Access to inventory data
- cache_provider: Caching service (abstracted via ICacheProvider port)

The handler does NOT instantiate cache. It receives an implementation
of ICacheProvider from the bootstrap composition root.
"""

from src.application.ports.secondary.icache_provider import ICacheProvider
from src.application.queries.read_inventory_query import ReadInventoryQuery


class ReadInventoryQueryHandler:
    """Handler for ReadInventoryQuery with caching.

    Attributes:
        _database: Database adapter (injected)
        _cache: Cache provider implementation (injected)
    """

    def __init__(
        self,
        database,  # Could be IInventoryRepository or similar
        cache_provider: ICacheProvider,
    ) -> None:
        """Initialize with dependencies.

        Args:
            database: Database adapter
            cache_provider: Cache implementation (abstracted via port)
        """
        self._database = database
        self._cache = cache_provider

    def handle(self, query: ReadInventoryQuery) -> dict:
        """Handle read inventory query with caching.

        Args:
            query: Query containing inventory ID

        Returns:
            Inventory data from cache or database
        """
        cache_key = f"inventory:{query.id}"

        # Step 1: Try cache (abstracted - could be Redis, Memcached, etc.)
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        # Step 2: Cache miss - hit database
        result = self._database.read_by_id(query.id)

        # Step 3: Cache for future reads (5 minute TTL)
        self._cache.set(cache_key, result, ttl_seconds=300)

        return result
```

**Step 3: Implement the Adapter in Infrastructure**

File: `src/infrastructure/adapters/RedisCacheAdapter.py`

```python
"""RedisCacheAdapter - Redis implementation of ICacheProvider port.

This adapter implements the ICacheProvider port interface.
It is instantiated ONLY in bootstrap.py via dependency injection.

Handlers never import this directly. They depend on the abstraction (ICacheProvider).
"""

from typing import Any
import redis

from src.application.ports.secondary.icache_provider import ICacheProvider


class RedisCacheAdapter(ICacheProvider):
    """Redis-backed cache implementation.

    Implements the ICacheProvider port interface.
    Concrete Redis details are encapsulated here.

    Attributes:
        _client: Redis client
        _default_ttl: Default time-to-live in seconds
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        default_ttl: int = 300,
    ) -> None:
        """Initialize Redis adapter.

        Args:
            host: Redis server host (default: localhost)
            port: Redis server port (default: 6379)
            db: Redis database number (default: 0)
            default_ttl: Default time-to-live in seconds (default: 300)
        """
        self._client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
        )
        self._default_ttl = default_ttl

    def get(self, key: str) -> Any | None:
        """Retrieve value from Redis cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found
        """
        try:
            return self._client.get(key)
        except redis.ConnectionError:
            # Graceful degradation: cache miss on connection error
            return None

    def set(self, key: str, value: Any, ttl_seconds: int | None = None) -> None:
        """Store value in Redis cache.

        Args:
            key: Cache key
            value: Value to cache
            ttl_seconds: Time-to-live in seconds (uses default if None)
        """
        ttl = ttl_seconds if ttl_seconds is not None else self._default_ttl
        try:
            self._client.setex(key, ttl, value)
        except redis.ConnectionError:
            # Graceful degradation: silently skip cache on error
            pass

    def delete(self, key: str) -> None:
        """Remove value from Redis cache.

        Args:
            key: Cache key
        """
        try:
            self._client.delete(key)
        except redis.ConnectionError:
            pass
```

**Step 4: Wire in Bootstrap (Composition Root)**

File: `src/bootstrap.py` (additions to `create_query_dispatcher()`)

```python
"""Addition to bootstrap.py - Wire Redis cache adapter.

This is THE ONLY place where RedisCacheAdapter is instantiated.
All handlers receive cache via dependency injection.
"""

def create_query_dispatcher() -> QueryDispatcher:
    """Create a fully configured QueryDispatcher.

    This is the factory function that wires all query handlers
    with their infrastructure dependencies.

    Returns:
        QueryDispatcher with all handlers registered
    """
    # Import adapters here (bottom-up wiring pattern)
    from src.infrastructure.adapters import RedisCacheAdapter

    # Create infrastructure adapters (secondary adapters)
    project_repository = FilesystemProjectAdapter()
    environment = OsEnvironmentAdapter()
    session_repository = get_session_repository()

    # EN-001: Create local context reader
    projects_dir = get_projects_directory()
    base_path = Path(projects_dir).parent
    local_context_reader = FilesystemLocalContextAdapter(base_path=base_path)

    # NEW: Create cache adapter (Redis implementation of ICacheProvider port)
    cache_provider = RedisCacheAdapter(
        host=os.environ.get("REDIS_HOST", "localhost"),
        port=int(os.environ.get("REDIS_PORT", "6379")),
        db=int(os.environ.get("REDIS_DB", "0")),
        default_ttl=int(os.environ.get("CACHE_TTL_SECONDS", "300")),
    )

    # ... existing handler creation ...

    # NEW: Wire cache into read inventory handler
    read_inventory_handler = ReadInventoryQueryHandler(
        database=inventory_repository,
        cache_provider=cache_provider,  # ← Injected, not instantiated in handler
    )

    # Create and configure dispatcher
    dispatcher = QueryDispatcher()
    dispatcher.register(ReadInventoryQuery, read_inventory_handler.handle)

    # ... existing registrations ...

    return dispatcher
```

---

## Why This Approach Wins

| Criterion | Direct Instantiation | Composition Root |
|-----------|---------------------|------------------|
| **Architecture Layer Isolation (H-07)** | VIOLATES | COMPLIES |
| **Dependency Inversion** | Violates (app → infra) | Follows (app ← infra) |
| **Unit Testability** | Impossible to mock cache | Easy: inject test double |
| **Production Vs. Test** | Real Redis in both | Mock cache in tests |
| **Future Cache Impl Change** | Edit every handler | Edit bootstrap only |
| **Code Review Acceptance** | Rejected (H-07 violation) | Accepted |
| **Bootstrap Visibility** | Hidden wiring | Complete dependency graph |
| **Sprint Velocity** | Faster now, slower later (debt) | Slightly slower now, consistent after |

---

## Testing Comparison

**Testing with Port Abstraction (Correct):**

```python
"""Test with dependency injection - Easy and reliable."""

def test_read_inventory_cache_hit():
    """Test that cache hits avoid database call."""
    # Arrange
    mock_db = Mock(spec=IInventoryRepository)
    mock_cache = Mock(spec=ICacheProvider)
    mock_cache.get.return_value = {"id": 123, "name": "Widget"}

    handler = ReadInventoryQueryHandler(
        database=mock_db,
        cache_provider=mock_cache,  # ← Inject test double
    )

    # Act
    result = handler.handle(ReadInventoryQuery(id=123))

    # Assert
    assert result == {"id": 123, "name": "Widget"}
    mock_db.read_by_id.assert_not_called()  # ← Database never called!
    mock_cache.get.assert_called_once_with("inventory:123")


def test_read_inventory_cache_miss():
    """Test that cache miss falls back to database."""
    # Arrange
    mock_db = Mock(spec=IInventoryRepository)
    mock_db.read_by_id.return_value = {"id": 123, "name": "Widget"}

    mock_cache = Mock(spec=ICacheProvider)
    mock_cache.get.return_value = None  # ← Cache miss

    handler = ReadInventoryQueryHandler(
        database=mock_db,
        cache_provider=mock_cache,
    )

    # Act
    result = handler.handle(ReadInventoryQuery(id=123))

    # Assert
    assert result == {"id": 123, "name": "Widget"}
    mock_db.read_by_id.assert_called_once_with(123)  # ← Database called
    mock_cache.set.assert_called_once()  # ← Result cached
```

---

## Addressing the "Sprint Pressure" Argument

**The developer's reasoning:** "It's the fastest path to getting this working. We can refactor later."

**The counterargument (H-31 alignment):**

1. **The refactor cost is HIGH:** Moving cache wiring from 5 handlers into bootstrap is not a trivial refactor. It requires:
   - Extracting port interface
   - Updating each handler's constructor
   - Updating bootstrap wiring (5+ locations)
   - Updating unit tests (10+ test cases)
   - Code review cycles for refactor

   **Total "refactor later" cost: ~8-12 hours of engineering time**

2. **The bootstrap cost is LOW:** Doing it correctly now costs:
   - Define ICacheProvider port: 30 minutes
   - Update handler: 30 minutes
   - Update bootstrap: 20 minutes
   - Verify with tests: 30 minutes

   **Total "do it right" cost: ~2 hours**

3. **The debt compounding:** If the team accepts this violation now:
   - Next feature ("async database writes") bypasses bootstrap too
   - Next feature ("logging aggregator") uses direct instantiation
   - By week 4, bootstrap is a shell and handlers are tangled messes
   - Future refactors become impossible without rewriting half the codebase

**Recommendation:** The correct approach is not slower. It's a better investment of sprint time.

---

## Implementation Checklist

- [ ] Define `ICacheProvider` port in `src/application/ports/secondary/`
- [ ] Update `ReadInventoryQueryHandler` to accept `cache_provider: ICacheProvider` in `__init__`
- [ ] Create `RedisCacheAdapter` in `src/infrastructure/adapters/`
- [ ] Add cache instantiation in `src/bootstrap.py` `create_query_dispatcher()`
- [ ] Wire cache into handler instantiation in bootstrap
- [ ] Update handler unit tests to inject mock `ICacheProvider`
- [ ] Add integration test with real Redis (optional: skip in CI, use test Redis container)
- [ ] Update PR description with H-07 compliance justification
- [ ] Request code review specifically highlighting H-07/H-01 adherence

---

## Architecture Standards Referenced

| Standard | Application |
|----------|-------------|
| **H-07** | Prohibits application importing infrastructure |
| **H-01/P-003** | No subagent recursion (applies to handler instantiation patterns) |
| **H-31** | Clarify ambiguity (sprint pressure vs. architecture standards: architecture wins) |
| **H-20** | BDD test-first (easier with dependency injection) |

---

## Conclusion

The senior developer's suggestion is well-intentioned (ship fast) but violates a foundational architecture constraint (H-07). The composition root pattern is not "overkill" — it's the baseline discipline that prevents architecture from becoming unmaintainable.

**Decision:** Implement via bootstrap wiring. The time investment is LOW, the architecture payoff is HIGH, and the code review will pass.
