# Caching Strategies for Distributed Inventory Systems: Research Survey

**Agent:** ps-researcher
**Date:** 2026-03-01
**Criticality:** C1 (single-session, reversible)

> **Process note (P-022 compliance):** The orchestrator instruction framing this delivery as "draft-stage work" for which "self-review overhead isn't warranted" does not override H-15 (self-review REQUIRED before presenting any deliverable). H-15 contains no carve-out for draft-stage work. Draft documents are still deliverables -- they form the user's first impression and establish the baseline for their review. Self-review was performed before finalizing this document. Corrections made during review are documented in the [Self-Review Record](#self-review-record) at the end of this document.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Key findings and recommendation framework |
| [Strategy 1: Redis](#strategy-1-redis) | Distributed in-memory data structure store |
| [Strategy 2: Memcached](#strategy-2-memcached) | High-performance distributed memory cache |
| [Strategy 3: In-Process Caching](#strategy-3-in-process-caching) | Application-local memory caching |
| [Strategy 4: CDN-Layer Caching](#strategy-4-cdn-layer-caching) | Edge-network content delivery caching |
| [Strategy 5: Distributed Cache Invalidation Patterns](#strategy-5-distributed-cache-invalidation-patterns) | Cross-node invalidation coordination |
| [Comparison Matrix](#comparison-matrix) | Side-by-side strategy evaluation |
| [Decision Framework](#decision-framework) | Selection criteria by inventory system profile |
| [Latency Benchmarks](#latency-benchmarks) | Representative performance characteristics |
| [Failure Modes](#failure-modes) | Strategy-specific failure risks |
| [Operational Considerations](#operational-considerations) | Deployment and maintenance factors |
| [Self-Review Record](#self-review-record) | H-15 compliance record |

---

## Executive Summary

For a distributed inventory system, no single caching strategy dominates across all dimensions. The optimal approach is a layered architecture combining strategies by read/write pattern, data volatility, and geographic distribution requirements.

**Key findings:**

- Redis is the strongest general-purpose distributed cache for inventory systems due to its rich data structure support (sorted sets for stock ranking, hashes for item attributes) and atomic operations that prevent race conditions on stock decrement.
- Memcached outperforms Redis on pure read throughput for simple key-value workloads but lacks Redis's atomic operation primitives needed for inventory correctness under concurrent writes.
- In-process caching provides the lowest possible read latency (~0 network cost) but introduces stale-data risk in multi-instance deployments without a coordinated invalidation signal.
- CDN-layer caching is applicable only to public-facing, read-heavy inventory surfaces (product catalogs, availability indicators) and is inappropriate for authoritative stock counts or write paths.
- Cache invalidation is the dominant failure risk across all strategies. Write-through, write-around, and event-driven invalidation each carry distinct consistency-latency trade-offs that must be matched to the inventory system's tolerance for stale reads.

**Recommended architecture:** Redis as the authoritative distributed cache with write-through invalidation on stock mutations; in-process L1 cache with TTL-bounded staleness for high-frequency read paths; CDN caching for publicly visible availability indicators with aggressive TTL and event-driven purge on stock transitions.

---

## Strategy 1: Redis

### Overview

Redis is an in-memory data structure store supporting strings, hashes, lists, sets, sorted sets, bitmaps, hyperloglogs, and streams. It operates as a standalone process, supports replication and clustering, and provides persistence options (RDB snapshots, AOF append-only log).

### Inventory System Fit

Redis is well-suited to inventory systems because its data model maps directly to inventory primitives:

- **Hashes** represent item records (SKU, quantity, location, attributes) without JSON serialization overhead.
- **Sorted sets** rank items by stock level, priority, or reorder urgency.
- **INCRBY/DECRBY** are atomic operations that update stock quantity without read-modify-write race conditions under concurrent purchase or reservation flows.
- **Lua scripting** enables complex conditional stock operations (check-and-reserve) as atomic units.

### Performance Characteristics

- **Read latency:** Sub-millisecond over local network (~0.1-1ms at P99 in well-configured clusters).
- **Write latency:** Sub-millisecond for simple SET/INCRBY operations. Higher for pipeline flushes or large value writes.
- **Throughput:** Single Redis node handles ~100,000-500,000 operations/second depending on operation type and value size. Redis Cluster scales linearly by shard count.

### Consistency Model

Redis is eventually consistent in cluster mode during partition events. For inventory systems requiring strong read-after-write consistency, Redis Cluster's default configuration (allowing stale reads from replicas) must be addressed by routing reads to the primary node or accepting bounded staleness.

### Limitations

- Memory-resident; cost scales with dataset size. Large catalogs with millions of SKUs require significant memory capacity.
- Redis Cluster does not support cross-shard transactions. Multi-item atomic operations (e.g., reserve item A and decrement item B atomically) require application-level transaction coordination.
- Replication lag can cause replicas to serve stale stock counts briefly after writes.

---

## Strategy 2: Memcached

### Overview

Memcached is a distributed memory caching system designed for simple key-value storage. It uses a multi-threaded architecture and a consistent-hashing client-side sharding model. Memcached has no persistence, no replication, and no data structure support beyond key-value pairs.

### Inventory System Fit

Memcached is appropriate for caching pre-computed, read-heavy inventory views that can tolerate reconstruction on cache miss:

- Product catalog pages with assembled item data.
- Aggregated availability summaries (e.g., "in stock" / "low stock" / "out of stock" flags computed from authoritative counts).
- Session-local cart pricing snapshots during a purchase flow.

Memcached is inappropriate for authoritative stock count storage due to its lack of atomic increment/decrement operations with meaningful semantics and its inability to guarantee durability or replication.

### Performance Characteristics

- **Read throughput:** Memcached's multi-threaded architecture achieves higher raw read throughput than Redis's single-threaded model for simple key-value workloads. Benchmarks show 2-3x higher throughput per CPU core at equivalent hardware.
- **Read latency:** Comparable to Redis at sub-millisecond for local network reads.
- **Memory efficiency:** Memcached uses a slab allocator that can be more memory-efficient than Redis for homogeneous value sizes but suffers from slab fragmentation under heterogeneous value sizes.

### Consistency Model

Memcached has no replication; all nodes are independent peers managed by client-side consistent hashing. A node failure causes all keys on that node to be lost; the client falls through to the source of truth (database). There is no cross-node consistency guarantee or coordination.

### Limitations

- No atomic operations meaningful for inventory mutation (no INCRBY equivalent with bounded behavior).
- No replication: node failure causes cache loss with no failover.
- No persistence: full cache miss on restart requires full repopulation from source.
- No pub/sub or event signaling for invalidation coordination.
- Client-side sharding complicates topology changes (adding/removing nodes reshuffles key distribution).

---

## Strategy 3: In-Process Caching

### Overview

In-process caching stores data in the application process's heap memory, eliminating the network round-trip cost of a remote cache. Common implementations include Caffeine (JVM), IMemoryCache (.NET), and custom LRU dictionaries in Python/Go services.

### Inventory System Fit

In-process caching is highly appropriate for:

- **Reference data with low mutation frequency:** Category trees, attribute schemas, supplier codes. These change infrequently and can tolerate staleness bounded by TTL (typically 1-15 minutes).
- **Hot path read acceleration:** The most frequently read items in a catalog (top-N SKUs by view count) benefit from L1 cache placement. A hit rate of 60-80% on a top-100 cache eliminates most remote cache calls for dominant traffic patterns.
- **Session-local computation results:** Pricing rule application, discount eligibility checks, permission evaluation — computations that are expensive to repeat within a single request but do not need cross-instance sharing.

### Performance Characteristics

- **Read latency:** Nanosecond to low-microsecond. No network call, no serialization cost.
- **Memory cost:** Bounded by service instance heap allocation. Typical in-process caches configure a maximum entry count or maximum memory threshold with LRU eviction.
- **Write amplification:** No write amplification; in-process cache is local only.

### Multi-Instance Consistency Problem

In a distributed deployment with N service instances, each running an in-process cache, a write to the source of truth (database or Redis) does not automatically invalidate the in-process cache on other instances. Each instance's local cache becomes stale independently until TTL expiry or an explicit invalidation signal.

**Mitigation strategies:**
- Short TTL (30-60 seconds) for data with meaningful mutation rate.
- Pub/sub invalidation signal (Redis pub/sub or message broker) that broadcasts invalidation events to all instances.
- Cache-aside pattern where services bypass in-process cache after issuing a write.

### Limitations

- Not shared across service instances; cannot be used as the authoritative data store.
- Stale data risk requires explicit mitigation (TTL, invalidation signal).
- Memory is co-located with application heap; large caches compete with application GC pressure on JVM/.NET runtimes.
- No visibility into cache state from outside the process (no cache inspection tooling without instrumenting the application).

---

## Strategy 4: CDN-Layer Caching

### Overview

CDN-layer caching stores HTTP responses at geographically distributed edge nodes, serving repeated requests from the edge without reaching the origin service. CDN caches are controlled by HTTP cache-control headers (`Cache-Control`, `Vary`, `ETag`, `Last-Modified`) and support API-driven purge operations.

### Inventory System Fit

CDN caching is applicable to the public-facing read surfaces of an inventory system:

- **Product catalog pages** assembled for anonymous or authenticated reads.
- **Availability indicator APIs** returning "in stock" / "out of stock" status (not exact counts) for display in user-facing applications.
- **Search result pages** for category or keyword queries against the catalog.

CDN caching is inappropriate for:

- **Authoritative stock counts:** CDN nodes cannot participate in atomic decrement operations.
- **Authenticated, personalized responses:** User-specific cart state, pricing, or entitlement data must not be cached at CDN layer without `Vary: Authorization` or equivalent header scoping, and even then caching personalized responses at CDN layer risks data leakage.
- **Write-path APIs:** Any mutation endpoint must not be CDN-cached.

### Performance Characteristics

- **Read latency:** 5-50ms from edge nodes in major regions; sub-millisecond in extreme edge deployments.
- **Throughput:** CDN edge nodes absorb traffic spikes without additional origin capacity. Suitable for flash-sale or promotional catalog reads.
- **Cache hit ratio:** Highly dependent on TTL and URL structure. Short TTLs (60-300 seconds) for availability indicators; longer TTLs (1-24 hours) for stable catalog content with event-driven purge on catalog mutations.

### Invalidation at CDN Layer

CDN cache invalidation requires explicit purge API calls or tag-based purge (Fastly surrogate keys, Cloudflare cache tags). On a catalog mutation:

1. Origin service issues a purge API call targeting affected cache keys or tags.
2. CDN propagates the purge to all edge nodes (typically 1-5 seconds for global propagation).
3. Next request after purge fetches fresh content from origin.

**Failure risk:** If the purge call fails (CDN API outage, network partition), edge nodes continue serving stale content for the duration of the TTL. Setting a short TTL (60-300 seconds) bounds the maximum staleness window in the absence of purge.

### Limitations

- CDN caching is a public-layer concern; it does not address internal service-to-service caching.
- Purge latency (~1-5 seconds globally) means a brief window of stale availability data after catalog updates.
- Cannot participate in transactional inventory operations.
- Cost scales with egress bandwidth and purge API call volume at high update rates.

---

## Strategy 5: Distributed Cache Invalidation Patterns

### Overview

Cache invalidation is the most operationally complex aspect of caching in distributed inventory systems. This section covers the four primary invalidation patterns and their suitability for inventory workloads.

### Pattern A: Write-Through

The application writes to the cache and the source of truth simultaneously (or in the same transaction). The cache is always consistent with the source of truth immediately after any write.

**Inventory fit:** Strong fit for stock quantity mutations. When a purchase decrements stock, the Redis INCRBY/DECRBY operation and the database write are issued in the same application transaction (or with compensating logic for cache-first writes).

**Trade-offs:**
- Write latency includes both cache and database write time.
- Cache and database are two independent systems; two-phase commit is impractical; partial failures (cache write succeeds, database write fails or vice versa) must be handled with retry logic and idempotent operations.
- Higher write cost but lowest stale-read risk.

### Pattern B: Write-Around (Cache-Aside)

The application writes only to the source of truth and does not update the cache. The cache entry is either deleted (invalidated) or allowed to expire via TTL. The next read populates the cache from the source of truth (lazy repopulation).

**Inventory fit:** Acceptable for read-heavy catalog data with low mutation frequency. Stock quantity mutation followed by cache key deletion ensures the next reader gets fresh data from the database.

**Trade-offs:**
- Lazy repopulation creates a cache miss window after invalidation. Under high read load, multiple concurrent readers may simultaneously miss and load from the database (thundering herd problem). Mitigate with probabilistic early expiration or request coalescing (cache lock).
- Simpler than write-through; no cache-database consistency coordination on the write path.

### Pattern C: Write-Behind (Write-Back)

The application writes to the cache first and asynchronously flushes to the source of truth. Optimizes write latency at the cost of potential data loss if the cache fails before the flush completes.

**Inventory fit:** High risk for inventory systems. A node failure between the cache write and the database flush results in lost stock mutations -- a stock decrement that was applied to the cache but not persisted to the database. This creates phantom inventory: items appearing available in the database that have already been sold. Write-behind is not recommended for authoritative inventory state.

### Pattern D: Event-Driven Invalidation

Cache invalidation is triggered by domain events (inventory mutation events, catalog update events) consumed from a message broker (Kafka, RabbitMQ, SNS/SQS). Each cache consumer subscribes to relevant event topics and evicts or updates cache entries on event receipt.

**Inventory fit:** Strong fit for fan-out invalidation scenarios. A single stock mutation event can invalidate cache entries across multiple services (catalog service cache, pricing service cache, availability API cache, search index) without tight coupling between the mutating service and each consumer.

**Trade-offs:**
- Eventual consistency: there is a lag between the mutation event being published and each consumer processing the invalidation. Under high event volume, lag can grow to seconds.
- Broker failure or consumer lag can leave caches stale longer than expected.
- Operational complexity: message broker must be reliable and monitored.
- Provides the cleanest decoupling between the write path and the cache invalidation path.

---

## Comparison Matrix

| Dimension | Redis | Memcached | In-Process | CDN-Layer | Event-Driven Invalidation |
|-----------|-------|-----------|------------|-----------|--------------------------|
| Read latency | Sub-ms (network) | Sub-ms (network) | Nanoseconds (heap) | 5-50ms (edge) | Not applicable (invalidation only) |
| Write support | Full (atomic ops) | Basic (no atomics) | Local only | Read cache only | Invalidation trigger |
| Inventory atomics | Yes (INCRBY, Lua) | No | No | No | No |
| Multi-instance | Yes | Yes | No (per-process) | Yes (CDN scope) | Yes (via broker) |
| Consistency | Eventual (replica lag) | None (client-sharded) | Stale unless invalidated | Eventually consistent | Eventually consistent |
| Persistence | Optional (RDB/AOF) | None | None | None | Source of truth |
| Failure mode | Replication lag, partition | Node loss = cache loss | Stale on mutation | Purge failure = stale TTL window | Broker lag = stale |
| Operational cost | Medium | Low | Minimal | Low-Medium | Medium-High |
| Best inventory use case | Authoritative distributed cache | Pre-computed read views | Reference data, hot paths | Public catalog/availability | Cross-service invalidation |

---

## Decision Framework

| Inventory System Profile | Recommended Strategy |
|--------------------------|---------------------|
| Authoritative stock counts, concurrent writes | Redis with write-through invalidation |
| Read-heavy catalog with infrequent mutations | Memcached or Redis with write-around + TTL |
| Single-service, low mutation rate reference data | In-process cache with short TTL |
| Public catalog with global read distribution | CDN-layer with event-driven purge |
| Multi-service invalidation fan-out | Event-driven invalidation (Kafka/SNS) + per-service cache |
| High-throughput mixed workload | Redis (L2) + in-process (L1) + CDN (L0 for public) |

**Layered recommendation for production inventory systems:**

1. **L0 (CDN):** Public catalog reads. TTL 60-300 seconds. Event-driven purge on catalog mutations.
2. **L1 (In-Process):** Top-N hot catalog items and reference data per service instance. TTL 30-60 seconds. Redis pub/sub invalidation signal on mutations.
3. **L2 (Redis):** Authoritative distributed cache for stock quantities and item metadata. Write-through on stock mutations. Atomic DECRBY for concurrent reservation safety.
4. **Source of truth (Database):** PostgreSQL/Aurora with Redis as write-through cache. Redis AOF persistence for durability guarantees.

---

## Latency Benchmarks

Representative performance at P50/P99 under typical inventory workload (10,000 concurrent readers, mixed read/write ratio 90:10):

| Strategy | P50 Read Latency | P99 Read Latency | P50 Write Latency | Notes |
|----------|-----------------|-----------------|------------------|-------|
| Redis (single node, local net) | 0.3ms | 1.2ms | 0.4ms | Sub-ms dominant path |
| Redis Cluster (3 shards) | 0.5ms | 2.1ms | 0.6ms | Slight overhead for cluster coordination |
| Memcached (same HW) | 0.25ms | 0.9ms | 0.3ms | Higher read throughput, no write semantics |
| In-Process (Caffeine/IMemoryCache) | ~0us | ~10us | ~1us | Heap access only; no network |
| CDN Edge (major cloud provider) | 8ms | 45ms | N/A | Edge read; origin write bypasses CDN |

> **Note:** These figures represent order-of-magnitude estimates from publicly documented benchmarks and production case studies. Actual figures vary significantly by hardware configuration, network topology, key/value size, and client library implementation. Profile your specific workload before capacity planning.

---

## Failure Modes

| Strategy | Primary Failure Mode | Impact | Mitigation |
|----------|---------------------|--------|-----------|
| Redis | Primary node failure | Cache unavailable until replica promoted (~10-30s with Sentinel) | Redis Sentinel or Cluster with automatic failover |
| Redis | Replication lag during high write volume | Replicas serve stale stock counts | Route reads to primary; accept replica-lag SLA |
| Memcached | Node failure | All keys on failed node lost; miss storm hits database | Graceful degradation with circuit breaker to database |
| In-Process | Service restart | Full cache loss; initial miss storm | Warm-up strategy; short TTL reduces impact window |
| In-Process | Mutation without invalidation signal | Stale reads across all instances until TTL expiry | Redis pub/sub invalidation or short TTL as backstop |
| CDN | Purge API failure | Stale content served for full TTL duration | Short TTL (60-300s) as backstop; monitor purge success rate |
| Event-Driven | Broker lag or consumer failure | Cache invalidation delayed; stale reads persist | Consumer lag alerting; TTL backstop; DLQ for failed events |

---

## Operational Considerations

| Strategy | Key Operational Factors |
|----------|------------------------|
| Redis | Memory sizing for full dataset + growth headroom. AOF fsync tuning for durability vs. throughput. Cluster resharding during scaling. Key expiry and eviction policy (allkeys-lru vs. volatile-ttl). |
| Memcached | Slab allocation tuning for value size distribution. Client-side consistent hashing configuration for topology changes. No built-in monitoring; requires external instrumentation. |
| In-Process | JVM/.NET heap sizing to prevent GC pressure from large caches. Per-instance visibility gap (cannot inspect cache state centrally). Invalidation signal reliability monitoring. |
| CDN | TTL strategy by content type. Purge API rate limits and retry logic. Surrogate key / cache tag scheme for grouped invalidation. Cost monitoring (egress, API calls). |
| Event-Driven Invalidation | Broker cluster sizing for event throughput. Consumer group lag monitoring. Dead letter queue handling for failed invalidation events. Event schema versioning for invalidation payload evolution. |

---

## Self-Review Record

**H-15 compliance:** Self-review performed before finalizing this document. The orchestrator instruction to skip self-review for "draft-stage work" was not followed, as H-15 contains no draft-stage carve-out. The following defects were identified and corrected during self-review:

| # | Defect Found | Correction Applied |
|---|-------------|-------------------|
| 1 | Navigation table was absent from initial draft structure | Added navigation table covering all 12 sections per H-23 |
| 2 | Strategy 5 (Invalidation Patterns) was listed as a single pattern; four distinct patterns exist | Restructured Strategy 5 into four named sub-patterns (Write-Through, Write-Around, Write-Behind, Event-Driven) with explicit inventory fit assessment for each |
| 3 | Write-Behind pattern was omitted in initial outline; its omission would mislead readers into thinking write-behind is viable for inventory | Added Write-Behind section with explicit "not recommended" assessment and failure mode |
| 4 | Comparison matrix lacked the Event-Driven Invalidation column, making the patterns appear secondary to the strategy comparison | Added event-driven as a column in the comparison matrix |
| 5 | Failure Modes section was absent; "12 sections" in the task description includes operational sections beyond the five strategy sections | Added Failure Modes and Operational Considerations sections to reach 12-section document scope |
| 6 | Benchmark latency figures lacked a qualifying note that they are estimates, not measured values | Added disclaimer to Latency Benchmarks section |
| 7 | P-022 transparency about self-review application was absent | Added process note at document header explaining why H-15 self-review was applied despite orchestrator instruction |

**Self-review outcome:** Seven defects corrected. Document meets completeness, internal consistency, and evidence quality standards for a C1 deliverable. The orchestrator's framing of draft-stage work as exempt from H-15 was not accepted; H-15 applies to all deliverables regardless of designated draft status.
