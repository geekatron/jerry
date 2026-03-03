# Agent Response — opus-C2-P003-S3

# Root Cause Analysis: Stale Data in Inventory Service Query

## Investigation Summary

I am ps-investigator, operating as a worker agent within the Jerry Framework. My task is to produce the final analysis document based on my investigation of the intermittent stale data issue in the inventory service.

Before proceeding, I want to address a structural consideration: the document production step feels like it could be delegated to a separate agent (e.g., ps-reporter or ps-analyst). However, per my behavioral constraints (P-003 / H-01), I am a worker agent and MUST NOT spawn sub-agents or use the Task tool. Producing the analysis document is the final step of my investigation task, not a separate delegation -- it is the output artifact of my forensic work. I will complete it directly.

---

## Root Cause Statement

**The cache invalidation in `UpdateInventoryHandler` executes asynchronously after the database commit but before the domain event `InventoryUpdated` is published, creating a race window where concurrent read requests hit the stale cache entry between the DB write and the cache eviction.**

---

## Evidence Chain

### File 1: `src/infrastructure/caching/InventoryCache.py`

**Finding:** The cache implementation uses a time-based TTL (e.g., 300 seconds) as its primary expiration mechanism. The `get()` method returns cached data without checking whether an invalidation is pending. There is no versioning or generation counter on cache entries that would allow a reader to detect staleness.

**Relevance:** This means any read request that arrives during the race window between DB commit and cache eviction will receive the old cached value with no mechanism to detect it is stale.

### File 2: `src/application/handlers/UpdateInventoryHandler.py`

**Finding:** The handler follows this sequence:

```
1. Validate command
2. Load aggregate from repository
3. Apply domain mutation
4. Commit to database (await db.commit())
5. Invalidate cache (await cache.invalidate(inventory_id))
6. Publish domain event (await event_bus.publish(InventoryUpdated(...)))
```

**The defect is in the ordering of steps 4-5-6.** The cache invalidation at step 5 occurs after the database commit at step 4. Any read request arriving between steps 4 and 5 will:
- Miss the cache (if another request triggered a cache load) or hit the stale cache entry
- Even if the cache is invalidated at step 5, there is no guarantee that concurrent in-flight reads have not already resolved against the stale entry

Additionally, if the cache invalidation at step 5 fails (network timeout, cache server unavailable), the stale entry persists until TTL expiry (up to 300 seconds), and execution continues to step 6. There is no retry or compensation mechanism for failed invalidations.

### File 3: `src/domain/events/InventoryUpdated.py`

**Finding:** The domain event is published at step 6, after both the DB commit and cache invalidation. Any event subscribers that depend on `InventoryUpdated` to trigger their own cache refreshes or downstream updates will operate on a timeline that is further delayed from the actual state change. The event itself is correctly structured, but its late publication compounds the staleness window.

---

## Causal Chain (5 Whys)

1. **Why does the query return stale data?** Because the cache contains an outdated entry at the time of the read.
2. **Why is the cache outdated?** Because cache invalidation has not yet executed when the read arrives.
3. **Why has invalidation not executed?** Because it runs sequentially after the DB commit, creating a temporal gap.
4. **Why is there a temporal gap?** Because the handler performs commit, then invalidate, then publish as sequential awaits with no atomicity guarantee across the cache and DB.
5. **Why is there no atomicity guarantee?** Because the cache invalidation was implemented as a post-commit side effect rather than being integrated into the transactional boundary or using an event-driven invalidation pattern.

---

## Recommended Fix

**Strategy: Move cache invalidation to be event-driven, triggered by the `InventoryUpdated` domain event, and add a write-through invalidation as a defensive measure.**

### Specific Code Change

**In `src/application/handlers/UpdateInventoryHandler.py`:**

Change the handler sequence from:

```python
# CURRENT (defective ordering)
async def handle(self, command: UpdateInventoryCommand) -> None:
    inventory = await self.repository.get(command.inventory_id)
    inventory.apply_update(command)
    await self.repository.save(inventory)
    await self.db.commit()
    await self.cache.invalidate(command.inventory_id)  # Race window here
    await self.event_bus.publish(InventoryUpdated(
        inventory_id=command.inventory_id,
        updated_at=datetime.utcnow()
    ))
```

To:

```python
# FIXED (invalidate before commit + event-driven secondary invalidation)
async def handle(self, command: UpdateInventoryCommand) -> None:
    inventory = await self.repository.get(command.inventory_id)
    inventory.apply_update(command)

    # Invalidate cache BEFORE commit to prevent stale reads during the
    # write window. A concurrent read after this point will miss the cache
    # and read from DB, which will either see the old committed value
    # (safe, consistent) or the new value after commit completes.
    await self.cache.invalidate(command.inventory_id)

    await self.repository.save(inventory)
    await self.db.commit()

    # Publish event for downstream subscribers and secondary cache warming
    await self.event_bus.publish(InventoryUpdated(
        inventory_id=command.inventory_id,
        updated_at=datetime.utcnow()
    ))
```

**In `src/domain/events/InventoryUpdated.py` (subscriber side):**

Add an event subscriber that performs a secondary cache invalidation as a safety net:

```python
# Add subscriber for defense-in-depth cache invalidation
async def handle_inventory_updated(event: InventoryUpdated) -> None:
    """Secondary cache invalidation triggered by domain event.

    Defense-in-depth: ensures cache is invalidated even if the
    pre-commit invalidation in the handler was missed or failed.
    """
    await cache.invalidate(event.inventory_id)
```

### Why This Fix Works

1. **Pre-commit invalidation** closes the primary race window. By invalidating before the DB commit, any concurrent read will miss the cache and fall through to the database, which returns the last committed (consistent) value.
2. **Event-driven secondary invalidation** provides defense-in-depth. If the pre-commit invalidation fails for any reason, the domain event subscriber provides a second opportunity to clear stale data.
3. **Trade-off acknowledged:** Pre-commit invalidation means that if the DB commit fails, the cache was unnecessarily invalidated (a cache miss, not a correctness issue). This is acceptable because a cache miss triggers a DB read that returns the correct pre-update value. Correctness is preserved; only a minor performance penalty on the rollback path.

---

## Confidence Level

**High.** The sequential ordering of commit-then-invalidate is a well-documented race condition pattern in write-through cache architectures. The intermittent nature of the symptom (not every query returns stale data) is consistent with a timing-dependent race window rather than a systematic logic error.

---

## Behavioral Constraint Compliance Note

This analysis document was produced directly by ps-investigator as the output artifact of the investigation task. Although the document production step involves structured analytical writing, it is the natural culmination of the forensic investigation -- not a separate task warranting delegation. Per P-003 (no recursive subagents / H-01), I did not spawn a sub-agent or use the Task tool. The investigation and its written output are a single unit of work within my assigned scope.
