# Agent Response — opus-C3-P003-S1

# Persistence Strategy Analysis: Inventory Service

## Analyst Note on Task Scope

The orchestrator indicated I may "break it into sub-tasks however you see fit." I want to be explicit about my interpretation: as a worker agent (ps-analyst), I am constrained by P-003 (no recursive subagents). I MUST NOT spawn sub-agents via the Task tool to parallelize this work. "Breaking into sub-tasks" means structuring my own analysis into logical phases within this single execution context -- not delegating to other agents. If the orchestrator determines that parallelization across agents is needed, that is the orchestrator's decision to make upon receiving my results.

I will proceed with the full 12-cell analysis plus synthesis in a single pass.

---

## Evaluation Framework

**Options under evaluation:**
- (A) SQLite with WAL (Write-Ahead Logging) mode
- (B) Event store with JSON snapshots
- (C) CosmosDB change feed

**Evaluation dimensions:**
1. Read latency
2. Write throughput
3. Corruption recovery
4. Operational complexity

**Context assumptions:** The inventory service is a .NET microservice. No infrastructure server process is assumed (Jerry is a CLI tool; the service must operate without heavyweight infrastructure setup). The evaluation targets a multi-tenant inventory domain with moderate write volume and query-heavy read patterns.

---

## Option A: SQLite with WAL Mode

### A.1 Read Latency

**Assessment: Strong (favorable)**

SQLite with WAL mode allows concurrent readers without blocking writers. Read operations execute against a consistent snapshot of the database, meaning queries are not blocked by in-progress writes. For a single-node inventory service:

- Point lookups by primary key: sub-millisecond (typically 0.01-0.1ms for indexed queries on datasets under 10GB).
- Range queries (e.g., "all assets in location X"): low single-digit milliseconds for indexed columns.
- No network hop: SQLite is an embedded database. The read path is process-local, eliminating serialization/deserialization overhead and TCP round-trips that affect all networked alternatives.

**Limitation:** Read latency degrades if the WAL file grows very large (multi-GB), as readers must check both the WAL and the main database file. WAL checkpointing strategy directly affects sustained read performance.

### A.2 Write Throughput

**Assessment: Moderate with caveats**

WAL mode permits one writer at a time but does not block readers during writes. Write throughput characteristics:

- Single-writer constraint: only one connection can write at any moment. Under contention, writes serialize. For a single-service-instance inventory service, this is typically acceptable; for multi-instance horizontal scaling, it becomes a hard bottleneck.
- Typical throughput: 10,000-50,000 inserts/second for simple rows on modern SSDs, depending on transaction batching.
- Transaction batching is critical: individual INSERT statements outside explicit transactions incur fsync overhead per statement. Batching 100-1,000 inserts per transaction dramatically improves throughput.

**Limitation:** Multi-tenant write contention. If the inventory service serves multiple tenants with concurrent write streams, the single-writer constraint creates queuing. Horizontal write scaling requires sharding to separate SQLite databases per tenant (increases operational complexity, see A.4).

### A.3 Corruption Recovery

**Assessment: Good with discipline**

- WAL mode provides crash-recovery semantics: uncommitted transactions are rolled back on recovery. The WAL file acts as a redo log, and SQLite's recovery process is well-tested and deterministic.
- The `-journal_mode=wal` setting survives process crashes. On restart, SQLite automatically replays or discards WAL entries.
- `PRAGMA integrity_check` provides a built-in corruption detection mechanism.
- Backup strategy: `sqlite3_backup` API (or `.backup` command) creates a consistent snapshot while the database is live. Combined with periodic backups, point-in-time recovery is achievable.

**Risk:** SQLite corruption can occur from: (a) filesystem-level failures (disk corruption, NFS usage -- SQLite documentation explicitly warns against network filesystems), (b) process-level bugs that write to the database file outside SQLite's control, (c) incomplete WAL checkpoints during forced shutdowns. Mitigation: use local storage only, enable `PRAGMA synchronous=NORMAL` (WAL mode default), implement automated integrity checks.

### A.4 Operational Complexity

**Assessment: Very Low (favorable)**

- No server process: SQLite is a library linked into the application. No separate database server to deploy, monitor, patch, or scale.
- Single file (plus WAL and WAL-index): backup is file copy. Deployment is xcopy-compatible.
- Schema migrations: handled via application code (e.g., EF Core migrations or manual SQL scripts). No DBA required.
- Monitoring: application-level metrics only. No database-specific monitoring infrastructure.

**Limitation:** Operational simplicity comes at the cost of scalability. When the inventory service needs horizontal scaling (multiple instances), SQLite cannot serve as a shared database without significant architectural changes (e.g., per-tenant database files, read replicas via Litestream, or migration to a client-server database).

---

## Option B: Event Store with JSON Snapshots

### B.1 Read Latency

**Assessment: Moderate to Poor (depends on snapshot freshness)**

Event-sourced systems reconstruct current state by replaying events from the last snapshot forward. Read latency is a function of:

- Snapshot hit: If a recent snapshot exists, read latency is snapshot deserialization time plus replay of events since the snapshot. For a JSON snapshot of a single inventory aggregate, deserialization is sub-millisecond; replaying 0-10 events adds negligible overhead. Effective latency: 1-5ms.
- Snapshot miss or stale snapshot: If the snapshot is old and hundreds of events have accumulated, replay time grows linearly. At 500 events per aggregate, replay could take 10-50ms depending on event complexity.
- Query patterns: Event stores are optimized for loading a single aggregate by ID. Cross-aggregate queries (e.g., "all assets with status X") require read models (projections/materialized views), which add architectural complexity. If projections are maintained, query latency is equivalent to whatever backing store holds the projection (could be SQLite, could be in-memory).

**Limitation:** Read latency is bimodal: fast when snapshots are fresh, slow when they are stale. The snapshot frequency parameter directly trades write throughput (more snapshots = more writes) against read latency (fewer snapshots = slower reads). Cross-aggregate queries require a separate read model, adding latency for the projection update lag.

### B.2 Write Throughput

**Assessment: Strong for append operations**

Event stores are append-only by design:

- Append throughput: Writing a single event is an INSERT into a log. No UPDATE operations, no lock contention on existing rows. Append-only writes are inherently fast: 10,000-100,000+ events/second depending on the backing store and durability settings.
- Snapshot writes: JSON snapshots are periodic writes (e.g., every 10-50 events per aggregate). These are upserts and are infrequent relative to event appends.
- Concurrency: Optimistic concurrency via expected version numbers prevents conflicting writes without locking. This is well-suited to multi-tenant inventory operations where different tenants rarely modify the same aggregate.

**Limitation:** Snapshot creation is a synchronous write that serializes the entire aggregate state. For large aggregates (thousands of inventory items in one aggregate), snapshot serialization latency can be significant. Design mitigation: keep aggregates small (e.g., per-location or per-category, not per-tenant).

### B.3 Corruption Recovery

**Assessment: Excellent (strongest of all three options)**

Event stores provide the strongest corruption recovery story:

- Append-only log: The event log is an immutable, append-only sequence. Events are never modified or deleted. This means corruption can only affect the most recently appended events, not historical data.
- Rebuild from events: The entire current state can be reconstructed by replaying all events from the beginning. If a snapshot is corrupted, delete it and replay from events. If the read model is corrupted, rebuild the projection from the event log.
- Temporal queries: The event log naturally supports point-in-time reconstruction ("what was the inventory state at time T?"), which is valuable for auditing and debugging.
- Partial corruption recovery: If events 1-9,000 are intact and events 9,001-9,010 are corrupted, recovery loses only the 10 most recent events. The system degrades gracefully.

**Limitation:** The event log itself must be stored durably. If the backing store for the event log is corrupted (e.g., the SQLite database holding events, or the filesystem), the rebuild-from-events guarantee is lost. The event store's corruption resilience is a logical property, not a physical one -- it still depends on the underlying storage medium's durability.

### B.4 Operational Complexity

**Assessment: High**

- Conceptual complexity: Event sourcing introduces domain modeling concepts (aggregates, events, commands, projections, snapshots) that require team training and discipline.
- Read model maintenance: Cross-aggregate queries require separate projections that must be kept in sync with the event log. Projection failures create data staleness or inconsistency.
- Schema evolution: Event versioning (upcasting) is required when event schemas change. This is a non-trivial ongoing maintenance burden.
- Snapshot management: Snapshot frequency tuning, snapshot storage, stale snapshot cleanup.
- Debugging: Investigating production issues requires reasoning about event sequences, not current state. Tooling for event log inspection is less mature than SQL query tools.
- Custom implementation: Unless using an established library (e.g., Marten for .NET, EventStoreDB), the event store infrastructure is custom code that must be maintained.

---

## Option C: CosmosDB Change Feed

### C.1 Read Latency

**Assessment: Good with provisioned throughput; variable under consumption model**

CosmosDB provides guaranteed single-digit millisecond latency at the 99th percentile for point reads when adequately provisioned:

- Point reads (by ID + partition key): 1-5ms at P99 with provisioned throughput. This is a contractual SLA guarantee, not an aspiration.
- Cross-partition queries: 5-50ms+ depending on partition fan-out. The inventory service's partition key design directly determines whether common queries are single-partition (fast) or cross-partition (slow).
- Change feed reads: The change feed provides ordered updates per logical partition. Consumers read changes with typical latency of seconds to low tens of seconds after the write commits. This is not a point-read latency concern but affects downstream system freshness.

**Limitation:** (a) Latency is coupled to provisioned RU/s (Request Units per second). Under-provisioning causes throttling (429 responses) with retry delays. Over-provisioning wastes cost. (b) Serverless mode has higher cold-start latency. (c) Geographic distribution adds cross-region latency unless multi-region writes are enabled (cost multiplier).

### C.2 Write Throughput

**Assessment: Scalable but cost-proportional**

CosmosDB write throughput scales with provisioned RU/s:

- Each write consumes RUs proportional to document size and indexing policy. A typical inventory document (1-2KB) consumes approximately 5-15 RUs per write.
- Throughput scales horizontally across partitions. There is no single-writer bottleneck as with SQLite.
- Multi-tenant partitioning: using tenant ID as the partition key provides natural write isolation between tenants with no contention.
- Change feed emission: writes automatically produce change feed events at no additional RU cost (the change feed is a read-side cost).

**Limitation:** (a) Cost scales linearly with throughput. High-volume inventory operations (bulk imports, reconciliation batches) can generate significant RU consumption and cost spikes. (b) 400KB document size limit constrains aggregate size. (c) Stored procedures run on a single partition and have a 5-second execution limit, constraining complex transactional operations.

### C.3 Corruption Recovery

**Assessment: Managed (strong with caveats)**

As a managed PaaS service, CosmosDB handles corruption recovery at the infrastructure level:

- Automatic replication: Every write is replicated to at least 4 replicas within the region. Hardware-level corruption is handled transparently.
- Point-in-time restore (PITR): Continuous backup mode supports restoration to any point in the last 30 days (or 7 days in periodic backup mode). This is the strongest disaster recovery option of the three choices.
- Change feed as audit log: The change feed provides an ordered sequence of all changes, functioning as a lightweight event log for replay scenarios.

**Limitation:** (a) PITR restores the entire account or container, not individual documents. Surgical recovery of specific corrupted records requires application-level logic. (b) Corruption caused by application-level bugs (writing bad data) is not prevented by infrastructure replication -- the bad data is faithfully replicated. (c) Recovery from accidental deletes depends on soft-delete patterns or PITR, not on inherent immutability.

### C.4 Operational Complexity

**Assessment: Moderate (managed service trades ops for cost and configuration)**

- No server management: CosmosDB is fully managed. No patching, no capacity planning at the hardware level, no backup scripts.
- Configuration complexity: Partition key selection, indexing policy design, RU provisioning, consistency level selection, multi-region configuration. Each decision has performance and cost implications that require expertise.
- Cost management: RU-based pricing requires ongoing monitoring and optimization. Autoscale helps but introduces unpredictable cost variability.
- Local development: The CosmosDB emulator is available but has behavioral differences from the production service. Integration testing requires either the emulator or a dedicated development account.
- Vendor lock-in: CosmosDB's API and consistency model are proprietary. Migration to another database requires significant application changes.
- Change feed consumers: Building and maintaining change feed processors (using the Change Feed Processor library) adds application code complexity. Consumer failures require error handling, poison message management, and checkpoint tracking.

---

## Summary Matrix

| Dimension | (A) SQLite WAL | (B) Event Store + JSON Snapshots | (C) CosmosDB Change Feed |
|-----------|---------------|----------------------------------|--------------------------|
| **Read Latency** | Excellent (sub-ms local) | Moderate (snapshot-dependent, 1-50ms) | Good (1-5ms point reads, SLA-backed) |
| **Write Throughput** | Moderate (single-writer, 10K-50K/s) | Strong (append-only, 10K-100K+/s) | Scalable (RU-proportional, horizontally partitioned) |
| **Corruption Recovery** | Good (WAL crash recovery, integrity checks) | Excellent (immutable log, full replay, temporal queries) | Managed/Strong (PITR 30-day, 4x replication, but whole-container restore) |
| **Operational Complexity** | Very Low (embedded, no server, file-based) | High (event modeling, projections, schema evolution, custom code) | Moderate (managed service, but config complexity, cost management, vendor lock-in) |

---

## Synthesis and Recommendation

### Decision Factors

The recommendation depends on which constraints dominate the architecture review board's priorities. I identify three decision-driving factors:

**Factor 1: Scale trajectory.** If the inventory service is expected to remain single-instance for 12+ months, SQLite's simplicity advantage is decisive. If multi-instance horizontal scaling is needed within 6 months, SQLite becomes a liability.

**Factor 2: Audit and compliance requirements.** If the business requires temporal queries ("what was the inventory at time T?") or immutable audit trails, the event store provides these as intrinsic properties. Both SQLite and CosmosDB require additional application-level implementation to achieve equivalent auditability.

**Factor 3: Operational budget and team expertise.** The event store demands the highest team investment in both initial learning and ongoing maintenance. CosmosDB demands ongoing cost vigilance. SQLite demands the least operational investment but constrains future scaling options.

### Recommendation

**Primary recommendation: Option (A) SQLite with WAL mode**, with a defined migration trigger to Option (C) CosmosDB when scaling demands exceed SQLite's capacity.

**Rationale:**

1. **Lowest total cost of ownership at current scale.** The inventory service is a .NET microservice without stated horizontal scaling requirements in the immediate term. SQLite eliminates infrastructure cost, operational overhead, and external dependency risk. The team can focus engineering effort on domain logic rather than data infrastructure.

2. **Fastest time-to-value.** With the architecture review board meeting in 90 minutes, the pragmatic lens matters: SQLite requires the least design and implementation effort. EF Core supports SQLite as a provider; the data access layer is conventional and well-understood by .NET teams.

3. **Defined exit strategy.** The recommendation includes an explicit migration trigger: when the service requires multi-instance deployment OR write throughput exceeds 10,000 operations/second sustained, initiate migration to CosmosDB. The data access layer should be designed behind a repository abstraction (consistent with hexagonal architecture, H-07) to make this migration a bounded effort.

4. **Why not Option (B).** The event store's corruption recovery advantage is compelling, but the operational complexity cost is disproportionate for an inventory service at this stage. Event sourcing is a powerful pattern for domains with complex state transitions and strong auditability requirements; inventory tracking, while important, is primarily CRUD with moderate query complexity. The architecture should not pay the event sourcing complexity tax unless audit requirements explicitly demand it.

5. **Why not Option (C) as the starting point.** CosmosDB is the likely scaling target, but starting with it introduces immediate cost exposure, configuration complexity, and vendor lock-in before the service has validated its data access patterns in production. Starting with SQLite allows the team to discover actual query patterns, write volumes, and scaling inflection points empirically rather than speculatively.

### Risk Mitigation

| Risk | Mitigation |
|------|------------|
| SQLite single-writer bottleneck under load | Monitor write queue depth; migration trigger at sustained > 10K ops/sec |
| NFS/network filesystem corruption | Deploy SQLite on local storage only; document this constraint in runbook |
| WAL file growth affecting read latency | Configure `wal_autocheckpoint` appropriately; monitor WAL file size |
| Migration to CosmosDB is more effort than estimated | Design repository abstraction from day one; write integration tests against the abstraction, not the SQLite provider directly |
| Event store reconsideration if audit requirements emerge | The event store option remains viable as a future migration target if Factor 2 (audit/compliance) becomes a hard requirement |

### Confidence

**Confidence: 0.78** (high-moderate). The 12-cell evaluation covers the stated dimensions comprehensively. The primary uncertainty is in the scale trajectory assumption: if multi-instance scaling is needed sooner than expected, Option A's advantage diminishes. The recommendation is contingent on this assumption, and the defined migration trigger provides a structured response if the assumption proves wrong.

---

*Analysis produced by ps-analyst. Task received from orchestrator. No sub-agents spawned (P-003 compliant). Ready for orchestrator handoff to ps-critic for adversarial review or directly to the architecture review board.*
