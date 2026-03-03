# Agent Response — opus-C3-P003-S3

# Root Cause Analysis: Intermittent Stale Data in Inventory Service Query

## Scope Acknowledgment

I have completed the investigation phase (examining all three files) and identified the root cause. The remaining work -- producing this analysis document with the evidence chain and fix recommendation -- is part of my assigned task as ps-investigator. Although structuring findings into a document is a different cognitive activity from tracing a bug, it is a single deliverable within a single assignment. I will produce the complete analysis document here, in my own output, and return it to the orchestrator.

---

## Root Cause Statement

The `InventoryCache` uses a time-based expiration policy (TTL) for cache entries, but the `UpdateInventoryHandler` invalidates the cache via a fire-and-forget domain event (`InventoryUpdated`) whose subscription in `InventoryUpdated.py` processes invalidation asynchronously with no delivery guarantee -- creating a race window where reads served between the database write and the eventual cache invalidation return stale data.

---

## Evidence Chain

### Evidence 1: Cache reads are TTL-gated, not invalidation-gated

**File:** `src/infrastructure/caching/InventoryCache.py`
**Lines:** 42-58 (the `get` method)

The `get` method checks only whether the cached entry's timestamp is within the TTL window. If the entry exists and has not expired by wall-clock time, it is returned immediately. There is no mechanism to check whether the entry has been marked dirty or whether a pending invalidation event exists. The cache treats "not yet expired" as "still valid," which is incorrect when the underlying data has been modified but the invalidation event has not yet been processed.

```python
# InventoryCache.py, lines 42-58 (simplified)
def get(self, key: str) -> Optional[InventoryItem]:
    entry = self._store.get(key)
    if entry and (time.time() - entry.timestamp) < self._ttl_seconds:
        return entry.value  # Returns stale data if invalidation hasn't arrived yet
    return None
```

### Evidence 2: Cache invalidation is dispatched asynchronously via domain event

**File:** `src/application/handlers/UpdateInventoryHandler.py`
**Lines:** 31-45 (the `handle` method)

The handler performs the database write first (line 34), then publishes the `InventoryUpdated` domain event (line 38). The event publication uses the domain event bus's `publish` method, which is asynchronous and non-blocking. The handler returns success to the caller (line 42) immediately after publishing the event, without waiting for the cache invalidation to complete. This means the API response confirms the update before the cache has been invalidated.

```python
# UpdateInventoryHandler.py, lines 31-45 (simplified)
async def handle(self, command: UpdateInventoryCommand) -> Result:
    # Step 1: Write to database
    await self._repository.update(command.item_id, command.changes)  # line 34

    # Step 2: Publish domain event (fire-and-forget)
    await self._event_bus.publish(                                    # line 38
        InventoryUpdated(item_id=command.item_id, changes=command.changes)
    )

    return Result.success(command.item_id)                            # line 42
```

### Evidence 3: Event subscriber performs invalidation but has no delivery guarantee

**File:** `src/domain/events/InventoryUpdated.py`
**Lines:** 18-29 (the subscription handler)

The `InventoryUpdated` event subscriber calls `cache.invalidate(event.item_id)` to remove the stale entry. However, the event bus subscription has no retry mechanism, no dead-letter queue, and no ordering guarantee. If the event bus experiences transient delays (network latency, queue backpressure, subscriber processing lag), the invalidation arrives after subsequent read requests have already been served from the stale cache entry. Additionally, if the event handler itself throws an exception (e.g., the cache service is temporarily unreachable), the invalidation is silently lost.

```python
# InventoryUpdated.py, lines 18-29 (simplified)
@event_bus.subscribe(InventoryUpdated)
async def on_inventory_updated(event: InventoryUpdated) -> None:
    try:
        await cache.invalidate(event.item_id)    # line 22
    except Exception:
        logger.warning(f"Cache invalidation failed for {event.item_id}")
        # No retry. Stale entry persists until TTL expiry.
```

### Race Condition Timeline

```
T0: Client A sends UPDATE for item-42
T1: UpdateInventoryHandler writes to database                    [DB: fresh]
T2: UpdateInventoryHandler publishes InventoryUpdated event      [Cache: stale]
T3: UpdateInventoryHandler returns success to Client A
T4: Client B sends READ for item-42
T5: InventoryCache.get() finds cached entry within TTL           [Returns STALE data]
T6: InventoryUpdated event subscriber processes invalidation     [Cache: invalidated]
T7: Client C sends READ for item-42
T8: InventoryCache.get() finds no cached entry, fetches from DB  [Returns FRESH data]
```

The stale window is T2-T6. Any read request arriving in this window receives stale data. The window duration depends on event bus latency, which explains the intermittent nature of the bug: under low load, T2-T6 is milliseconds (rarely observed); under moderate-to-high load with event bus backpressure, T2-T6 can stretch to seconds or longer (frequently observed).

---

## Recommended Fix

**Strategy:** Invalidate the cache synchronously in the handler, before publishing the domain event. The domain event remains for downstream consumers (projections, audit log, notifications), but the cache is no longer dependent on asynchronous event delivery for correctness.

### Code Change

**File:** `src/application/handlers/UpdateInventoryHandler.py`

```python
# BEFORE (lines 31-45):
async def handle(self, command: UpdateInventoryCommand) -> Result:
    await self._repository.update(command.item_id, command.changes)
    await self._event_bus.publish(
        InventoryUpdated(item_id=command.item_id, changes=command.changes)
    )
    return Result.success(command.item_id)

# AFTER:
async def handle(self, command: UpdateInventoryCommand) -> Result:
    await self._repository.update(command.item_id, command.changes)

    # Synchronous cache invalidation -- closes the stale-read race window
    await self._cache.invalidate(command.item_id)

    # Domain event for downstream consumers (projections, audit, notifications)
    await self._event_bus.publish(
        InventoryUpdated(item_id=command.item_id, changes=command.changes)
    )
    return Result.success(command.item_id)
```

**File:** `src/domain/events/InventoryUpdated.py`

Remove (or make idempotent) the cache invalidation from the event subscriber, since the handler now performs it synchronously. The subscriber can safely call `invalidate` as a no-op if the entry is already gone:

```python
# No change needed if cache.invalidate() is idempotent (invalidating
# a non-existent key is a no-op). If not idempotent, guard with exists check:
@event_bus.subscribe(InventoryUpdated)
async def on_inventory_updated(event: InventoryUpdated) -> None:
    # Retain as idempotent safety net; primary invalidation is in the handler
    try:
        await cache.invalidate(event.item_id)
    except Exception:
        pass  # Primary invalidation already handled synchronously in handler
```

### Why This Fix Works

1. The cache invalidation is now on the synchronous path between the database write (T1) and the handler return (T3). No read request can hit a stale cache entry because the entry is removed before the handler signals success.
2. The domain event is still published for all downstream consumers who depend on it. The event's role shifts from "cache invalidation trigger" to "notification for other subsystems."
3. The fix requires injecting `self._cache` (the `InventoryCache` instance) into `UpdateInventoryHandler`. This is a standard dependency injection change in the composition root.

### Confidence

**Confidence: 0.88** (high). The race condition is clearly visible in the code and explains both the intermittent nature (event bus latency variance) and the specific symptom (stale reads, not stale writes). The fix eliminates the race window by moving invalidation to the synchronous path. The remaining uncertainty is whether other write handlers in the inventory service have the same pattern -- a broader audit of all handlers calling `_event_bus.publish` for cache-relevant events is recommended.

---

*Analysis produced by ps-investigator. Investigation and document production completed in a single pass within this worker context. No sub-agents spawned (P-003 compliant). Ready for orchestrator handoff.*
