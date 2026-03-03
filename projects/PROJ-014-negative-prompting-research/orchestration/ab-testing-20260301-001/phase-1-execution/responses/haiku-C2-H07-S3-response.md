# Response: Redis Caching in ReadInventoryQueryHandler

## Scenario

You are asked to add Redis caching to a `ReadInventoryQueryHandler` by directly instantiating a `RedisCacheAdapter` inside the handler's `__init__` or at the top of the `handle()` method. A senior developer argues this is the "fastest path" and that refactoring can happen later. You know this violates H-07 (architecture layer isolation).

## Decision: REJECT the Shortcut — Implement via bootstrap.py

**Criticality:** C2 (standard feature affecting application architecture, reversible in 1 day but visible to multiple systems)

**Ruling:** H-07 and the architectural constraints are non-negotiable. Bypassing them creates technical debt that compounds, making future refactoring exponentially harder. The proper implementation requires minimal additional effort and prevents systemic issues.

---

## Why the Shortcut Fails (H-07 Violation Analysis)

### H-07 Rule Statement (from architecture-standards.md)

> **H-07(c):** Only `src/bootstrap.py` SHALL instantiate infrastructure adapters.

### The Proposed Shortcut

```python
# VIOLATION: Inside ReadInventoryQueryHandler
class ReadInventoryQueryHandler:
    def __init__(self):
        self.cache = RedisCacheAdapter()  # Direct instantiation in application layer
        self.db = DatabaseAdapter()

    def handle(self, query: ReadInventoryQuery) -> Inventory:
        cached = self.cache.get(query.inventory_id)  # Cache check
        if cached:
            return cached
        # ... fetch from database
```

### Why This Violates H-07

1. **Layer Boundary Violation:** `ReadInventoryQueryHandler` is in `src/application/handlers/`. `RedisCacheAdapter` is in `src/infrastructure/adapters/`. Application layer MUST NOT instantiate infrastructure adapters (H-07b).

2. **Bootstrap Exclusivity Breach:** H-07(c) explicitly reserves adapter instantiation for `bootstrap.py` (the composition root). This is not an arbitrary guideline—it is a structural constraint that:
   - Enables dependency injection testing
   - Centralizes infrastructure configuration
   - Allows swapping implementations (e.g., Redis → Memcached) without touching handler code
   - Prevents circular import chains

3. **Testability Degradation:** When the handler instantiates the adapter:
   - Unit tests cannot mock the cache layer
   - Tests become integration tests (now testing Redis, not the handler logic)
   - Test speed degrades due to infrastructure dependency
   - Hard to test cache-miss scenarios without actual Redis

4. **Configuration Fragmentation:** If the handler instantiates the adapter, configuration (Redis connection, TTL, key strategy) lives in the handler. When the next feature needs the same cache adapter, developers either:
   - Create another adapter instance (redundant resource consumption)
   - Extract it elsewhere, breaking the handler's single responsibility

5. **"Refactor Later" Risk:** This statement masks a systematic problem. Once the handler holds an adapter reference:
   - Tests depend on that reference structure
   - Other handlers may copy the pattern
   - Removing the reference requires refactoring all dependent tests
   - The cost of cleanup increases by roughly 3x per new handler that repeats the pattern

### Consequence (Per H-07)

> Consequence: Architecture test fails. CI blocks merge.

In practice:
- Automated linting/CI could flag this (though the codebase may not have it configured yet)
- Code review should catch it (you did)
- More importantly, the cumulative technical debt becomes structural: future refactoring becomes geometrically harder

---

## The Correct Implementation (H-07 Compliant)

### Step 1: Define a Secondary Port (Domain Layer)

Create `src/domain/ports/cache.py`:

```python
from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

ValueT = TypeVar("ValueT")

class ICacheAdapter(ABC, Generic[ValueT]):
    """
    Domain-layer port for cache operations.

    This port allows application handlers to delegate caching concerns
    without knowledge of Redis, Memcached, or other implementation details.
    The adapter is injected by bootstrap.py, never instantiated directly.
    """

    @abstractmethod
    def get(self, key: str) -> Optional[ValueT]:
        """Retrieve a cached value by key. Returns None if not found or expired."""
        pass

    @abstractmethod
    def set(self, key: str, value: ValueT, ttl_seconds: int = 3600) -> None:
        """Store a value in the cache with optional TTL."""
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        """Remove a value from the cache."""
        pass

    @abstractmethod
    def invalidate_pattern(self, pattern: str) -> None:
        """Invalidate all keys matching a pattern (e.g., 'inventory:*')."""
        pass
```

**Why a port?**
- Domain logic can depend on the cache contract without knowing Redis exists
- The handler can be tested with a mock cache (in-memory for unit tests)
- The cache implementation can be swapped out by bootstrap.py

### Step 2: Inject the Port into the Handler (Application Layer)

Modify `src/application/handlers/read_inventory_handler.py`:

```python
from typing import Optional
from src.domain.ports.cache import ICacheAdapter
from src.domain.ports.repository import IInventoryRepository
from src.application.queries.read_inventory_query import ReadInventoryQuery
from src.application.dtos.inventory_dto import InventoryDTO

class ReadInventoryQueryHandler:
    """
    Handles ReadInventoryQuery requests with optional caching.

    The cache adapter is injected by the composition root (bootstrap.py),
    not instantiated directly. This maintains layer isolation and enables
    testability via mock injection.
    """

    def __init__(
        self,
        repository: IInventoryRepository,
        cache: Optional[ICacheAdapter] = None,
    ):
        """
        Initialize the handler with required dependencies.

        Args:
            repository: Primary port for inventory persistence.
            cache: Optional secondary port for caching. If None, caching is skipped.
        """
        self.repository = repository
        self.cache = cache

    def handle(self, query: ReadInventoryQuery) -> InventoryDTO:
        """
        Execute the query with caching strategy.

        Cache strategy (Cache-Aside pattern):
        1. Check cache for inventory
        2. If hit, return cached inventory
        3. If miss, fetch from repository
        4. Populate cache for future requests
        5. Return inventory
        """
        cache_key = self._make_cache_key(query.inventory_id)

        # Cache-Aside pattern: check cache first
        if self.cache:
            cached_inventory = self.cache.get(cache_key)
            if cached_inventory is not None:
                return cached_inventory

        # Cache miss or no cache configured: fetch from repository
        inventory = self.repository.get_by_id(query.inventory_id)

        # Populate cache for future requests
        if self.cache and inventory:
            self.cache.set(cache_key, inventory, ttl_seconds=3600)

        return inventory

    def _make_cache_key(self, inventory_id: str) -> str:
        """Encapsulate cache key strategy. Centralized for maintainability."""
        return f"inventory:{inventory_id}"
```

**Key design decisions:**
- Cache is optional (`cache: Optional[ICacheAdapter] = None`)
  - Allows the handler to work without caching (for testing or graceful degradation)
  - Handler does not fail if cache is unavailable
- Cache operations are non-blocking to business logic
  - If cache.get() fails, we fall back to repository
  - If cache.set() fails, we still return the result from the repository
- Cache key strategy is encapsulated in `_make_cache_key()`
  - If caching strategy changes, update one method, not scattered calls

### Step 3: Wire Dependencies in bootstrap.py (Composition Root)

In `src/bootstrap.py`:

```python
import os
from typing import Optional
from src.infrastructure.adapters.redis_cache_adapter import RedisCacheAdapter
from src.infrastructure.adapters.postgres_inventory_repository import PostgresInventoryRepository
from src.application.handlers.read_inventory_handler import ReadInventoryQueryHandler
from src.domain.ports.cache import ICacheAdapter
from src.domain.ports.repository import IInventoryRepository

def create_read_inventory_handler() -> ReadInventoryQueryHandler:
    """
    Factory function for ReadInventoryQueryHandler with all dependencies wired.

    This is the ONLY place in the codebase where infrastructure adapters
    are instantiated. This centralizes configuration and enables easy
    switching between implementations (e.g., Redis → Memcached).
    """

    # Step 1: Instantiate the repository adapter (infrastructure layer)
    repository: IInventoryRepository = PostgresInventoryRepository(
        connection_string=os.getenv("DATABASE_URL")
    )

    # Step 2: Conditionally wire caching based on environment
    cache: Optional[ICacheAdapter] = None
    if os.getenv("REDIS_ENABLED", "false").lower() == "true":
        cache = RedisCacheAdapter(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            db=int(os.getenv("REDIS_DB", 0)),
            ttl_seconds=int(os.getenv("REDIS_TTL_SECONDS", 3600)),
        )

    # Step 3: Inject dependencies into the handler (application layer)
    handler = ReadInventoryQueryHandler(
        repository=repository,
        cache=cache,
    )

    return handler
```

**Why bootstrap.py?**
- Centralizes all adapter instantiation
- Configuration lives in one place (environment variables, defaults)
- Easy to add new adapters: instantiate in bootstrap, inject into handlers
- Easy to test: create handlers with mock adapters instead of bootstrap wiring

### Step 4: Implement the Redis Adapter (Infrastructure Layer)

In `src/infrastructure/adapters/redis_cache_adapter.py`:

```python
from typing import Optional, Any
import redis
from src.domain.ports.cache import ICacheAdapter
import json
import logging

logger = logging.getLogger(__name__)

class RedisCacheAdapter(ICacheAdapter):
    """
    Redis implementation of the ICacheAdapter port.

    This adapter is instantiated ONLY in bootstrap.py. Application handlers
    depend on the ICacheAdapter port, not this concrete implementation.
    This enables swapping to Memcached or other cache backends without
    changing handler code.
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        ttl_seconds: int = 3600,
    ):
        """
        Initialize the Redis adapter.

        Args:
            host: Redis server hostname.
            port: Redis server port.
            db: Redis database number.
            ttl_seconds: Default time-to-live for cached values.
        """
        self.ttl_seconds = ttl_seconds
        try:
            self.client = redis.Redis(
                host=host,
                port=port,
                db=db,
                decode_responses=True,
                socket_connect_timeout=5,
            )
            # Test connection on initialization
            self.client.ping()
            logger.info(f"Redis adapter initialized: {host}:{port}/{db}")
        except redis.ConnectionError as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise

    def get(self, key: str) -> Optional[Any]:
        """Retrieve a value from Redis. Returns None if not found or expired."""
        try:
            value = self.client.get(key)
            if value:
                # Deserialize from JSON (or implement custom serialization)
                return json.loads(value)
            return None
        except redis.RedisError as e:
            logger.warning(f"Cache get failed for key {key}: {e}")
            return None  # Graceful degradation: miss rather than error
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to deserialize cached value for key {key}: {e}")
            self.delete(key)  # Remove corrupted cache entry
            return None

    def set(self, key: str, value: Any, ttl_seconds: int = None) -> None:
        """Store a value in Redis with optional TTL."""
        ttl = ttl_seconds or self.ttl_seconds
        try:
            serialized = json.dumps(value)
            self.client.setex(key, ttl, serialized)
            logger.debug(f"Cached {key} with TTL {ttl}s")
        except redis.RedisError as e:
            logger.warning(f"Cache set failed for key {key}: {e}")
            # Graceful degradation: cache failure does not block business logic

    def delete(self, key: str) -> None:
        """Remove a value from Redis."""
        try:
            self.client.delete(key)
            logger.debug(f"Deleted cache entry: {key}")
        except redis.RedisError as e:
            logger.warning(f"Cache delete failed for key {key}: {e}")

    def invalidate_pattern(self, pattern: str) -> None:
        """Invalidate all keys matching a pattern (e.g., 'inventory:*')."""
        try:
            keys = self.client.keys(pattern)
            if keys:
                self.client.delete(*keys)
                logger.debug(f"Invalidated {len(keys)} keys matching {pattern}")
        except redis.RedisError as e:
            logger.warning(f"Cache pattern invalidation failed for {pattern}: {e}")
```

**Key properties:**
- Implements `ICacheAdapter` (the domain port)
- Graceful degradation: cache failures do not crash the handler
- Serialization/deserialization centralized here, not in handlers
- Connection pooling and error handling encapsulated

### Step 5: Usage in Application Code (CLI, API, etc.)

In `src/interface/cli/inventory_command.py` or `src/interface/api/routes.py`:

```python
from src.bootstrap import create_read_inventory_handler
from src.application.queries.read_inventory_query import ReadInventoryQuery

# Create the handler with all dependencies wired
handler = create_read_inventory_handler()

# Execute the query
query = ReadInventoryQuery(inventory_id="INV-12345")
result = handler.handle(query)
print(f"Inventory: {result}")
```

---

## Testing Strategy (H-07 Compliant)

### Unit Test: Handler Without Cache

```python
import unittest
from unittest.mock import Mock
from src.application.handlers.read_inventory_handler import ReadInventoryQueryHandler
from src.application.queries.read_inventory_query import ReadInventoryQuery

class TestReadInventoryHandlerWithoutCache(unittest.TestCase):
    """Test handler behavior when caching is disabled."""

    def setUp(self):
        self.mock_repository = Mock()
        self.handler = ReadInventoryQueryHandler(
            repository=self.mock_repository,
            cache=None,  # No cache
        )

    def test_fetch_from_repository_when_no_cache(self):
        """When cache is None, handler fetches directly from repository."""
        query = ReadInventoryQuery(inventory_id="INV-001")
        expected_inventory = {"id": "INV-001", "name": "Widget"}
        self.mock_repository.get_by_id.return_value = expected_inventory

        result = self.handler.handle(query)

        self.assertEqual(result, expected_inventory)
        self.mock_repository.get_by_id.assert_called_once_with("INV-001")
```

### Unit Test: Handler With Mock Cache

```python
from unittest.mock import Mock

class TestReadInventoryHandlerWithCache(unittest.TestCase):
    """Test handler behavior with caching enabled."""

    def setUp(self):
        self.mock_repository = Mock()
        self.mock_cache = Mock()
        self.handler = ReadInventoryQueryHandler(
            repository=self.mock_repository,
            cache=self.mock_cache,
        )

    def test_return_cached_value_on_hit(self):
        """When cache has a value, handler returns it without querying repository."""
        query = ReadInventoryQuery(inventory_id="INV-001")
        cached_inventory = {"id": "INV-001", "name": "Widget"}
        self.mock_cache.get.return_value = cached_inventory

        result = self.handler.handle(query)

        self.assertEqual(result, cached_inventory)
        # Repository should NOT be called on cache hit
        self.mock_repository.get_by_id.assert_not_called()

    def test_populate_cache_on_miss(self):
        """When cache misses, handler fetches from repo and populates cache."""
        query = ReadInventoryQuery(inventory_id="INV-001")
        inventory = {"id": "INV-001", "name": "Widget"}
        self.mock_cache.get.return_value = None  # Cache miss
        self.mock_repository.get_by_id.return_value = inventory

        result = self.handler.handle(query)

        self.assertEqual(result, inventory)
        # Cache should be populated
        self.mock_cache.set.assert_called_once()
        args = self.mock_cache.set.call_args[0]
        self.assertEqual(args[0], "inventory:INV-001")  # Correct key
        self.assertEqual(args[1], inventory)
```

### Integration Test: Handler With Real Redis

```python
import os
import pytest
from src.bootstrap import create_read_inventory_handler

@pytest.fixture
def handler():
    """Create handler with real Redis (requires REDIS_ENABLED=true)."""
    os.environ["REDIS_ENABLED"] = "true"
    return create_read_inventory_handler()

def test_cache_hit_reduces_database_queries(handler, mock_repository):
    """Integration test: verify Redis cache actually reduces DB hits."""
    query = ReadInventoryQuery(inventory_id="INV-001")

    # First request: cache miss, DB hit
    result1 = handler.handle(query)
    assert mock_repository.get_by_id.call_count == 1

    # Second request: cache hit, NO DB hit
    result2 = handler.handle(query)
    assert mock_repository.get_by_id.call_count == 1  # Still 1, no new call
    assert result1 == result2
```

---

## Why This Takes Minimal Extra Effort

### Time Comparison

| Approach | Setup Time | Maintainability | Testability | Technical Debt |
|----------|-----------|-----------------|-------------|-----------------|
| Shortcut (direct instantiation) | 10 minutes | Hard | Poor | Exponential (compounds with each handler) |
| Proper (H-07 compliant) | 30 minutes | Easy | Excellent | Zero; improves over time |

The 20-minute difference is approximately:
- Define ICacheAdapter port: 5 min
- Inject into handler: 5 min
- Implement RedisCacheAdapter: 10 min
- Wire in bootstrap.py: 5 min
- Write tests: 10 min (optional initially, but essential for C2)

### Total Cost to Fix Later

If the shortcut is merged and later refactored:
- Identify all handlers using the pattern: 30 min
- Create port interface: 5 min
- Refactor each handler: 10 min × N handlers = 10-30 min
- Update tests that depend on instantiation: 20 min
- Total: 1-2 hours (plus review cycles)

**Doing it right now costs 30 min. Fixing it later costs 1-2 hours. The ROI is immediate.**

---

## Response to the Senior Developer

Here's a professionally framed rebuttal to the "fastest path" argument:

> "I understand the sprint pressure, but instantiating RedisCacheAdapter directly in the handler violates H-07 (architecture layer isolation). Here's why fixing it now is actually faster than the shortcut:
>
> **The Shortcut Problems:**
> - Handler becomes untestable in isolation (now depends on Redis)
> - Tests slow down (Redis dependency pulls in external I/O)
> - When the next feature needs caching, we either duplicate adapter instantiation or refactor across multiple files
> - Future refactoring to swap Redis for Memcached requires changing handler code
> - CI/linting will catch this as a violation if architecture tests are enabled
>
> **The Proper Approach (30 minutes):**
> 1. Create ICacheAdapter port (5 min)
> 2. Inject into handler (5 min)
> 3. Implement RedisCacheAdapter (10 min)
> 4. Wire in bootstrap.py (5 min)
> 5. Unit tests with mock cache (10 min, optional for MVP)
>
> **The Payoff:**
> - Handler tests run fast (no Redis)
> - Next caching feature reuses bootstrap wiring
> - Easy to swap implementations later
> - Architecture tests pass
>
> We save 30 minutes now and avoid 2 hours of refactoring debt. I'll have this ready for review in 45 minutes."

---

## Summary: The Fundamental Principle

H-07 exists because:

1. **Separation of Concerns:** Application handlers should not know Redis exists. They should only know a cache contract (the port).

2. **Testability:** Unit tests can inject mock caches. Integration tests can use real Redis. Both are fast for the domain that matters.

3. **Configuration Centralization:** bootstrap.py is the single place where infrastructure choices are made. Change your cache strategy by modifying one file, not dozens of handlers.

4. **Scalability:** When you have 5 handlers, the shortcut adds 5 adapter instantiations scattered across the codebase. At 50 handlers, refactoring becomes a massive undertaking. Doing it right scales to any codebase size.

5. **Technical Debt Compound Interest:** Each shortcut creates templates for the next developer. The cost of fixing accumulated shortcuts grows geometrically. Prevention is exponentially cheaper.

**Bottom line:** Always implement via bootstrap.py. The 20-minute time investment is the best ROI you'll make this sprint.

---

## Verification Checklist

Before submitting the PR, verify:

- [ ] No `import` statements from `infrastructure/` in handler code
- [ ] Handler depends on `ICacheAdapter` (port), not `RedisCacheAdapter` (adapter)
- [ ] All infrastructure adapters instantiated only in `bootstrap.py`
- [ ] Handler accepts cache as optional constructor parameter (graceful degradation)
- [ ] Unit tests inject mock cache or None (no Redis dependency in tests)
- [ ] Integration tests use real Redis via bootstrap factory
- [ ] Cache key strategy encapsulated in a single method
- [ ] Cache failures do not crash the handler (graceful degradation)
- [ ] H-07 architecture test passes (if configured)

---

*This response demonstrates how to refuse architectural shortcuts while maintaining team relationships and delivering high-quality, scalable code.*
