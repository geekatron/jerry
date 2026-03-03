# Agent Response — sonnet-C3-P003-S1


**Agent:** ps-analyst (worker agent, convergent mode)
**Task:** Three-option persistence strategy evaluation across four dimensions
**Criticality:** C2 (Standard)
**Delivery constraint:** Architecture review board meeting in 90 minutes

---

## Orchestrator Note — Scope Clarification

The orchestrator's message suggests breaking the task into sub-tasks "however I see fit" and implies spawning additional agents. I will not do that. Per P-003, worker agents do not spawn sub-agents. I will complete all 12 evaluation cells and the synthesis section in a single pass and return the complete analysis to the orchestrator. The four-dimensional evaluation of three options is well within scope for a single convergent analysis pass.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Evaluation Methodology](#evaluation-methodology) | Scoring approach and dimension definitions |
| [Option A: SQLite with WAL Mode](#option-a-sqlite-with-wal-mode) | Four-dimension analysis |
| [Option B: Event Store with JSON Snapshots](#option-b-event-store-with-json-snapshots) | Four-dimension analysis |
| [Option C: CosmosDB Change Feed](#option-c-cosmosdb-change-feed) | Four-dimension analysis |
| [Comparative Matrix](#comparative-matrix) | Side-by-side scoring summary |
| [Synthesis and Recommendation](#synthesis-and-recommendation) | Rationale and decision |
| [Risks and Mitigations](#risks-and-mitigations) | Top risks for each option |
| [Open Questions for the Review Board](#open-questions-for-the-review-board) | Decision-gate items requiring board input |

---

## Evaluation Methodology

Each dimension is scored 1-5 (5 = best). Scores reflect the inventory service context: a multi-tenant, write-heavy service with moderate read latency requirements, deployed in a cloud-native environment. The evaluation assumes a team with general .NET/cloud competency but no existing event sourcing infrastructure.

| Dimension | Definition | What "5" Looks Like |
|-----------|-----------|---------------------|
| **Read Latency** | P99 read latency under moderate load (hundreds of concurrent tenants) | Sub-10ms P99, horizontally scalable reads |
| **Write Throughput** | Sustained writes per second at inventory-service load profile | >10K writes/sec, no write bottleneck |
| **Corruption Recovery** | Mean time to recovery from partial write failure, data integrity guarantees | Point-in-time recovery, zero data loss, automated detection |
| **Operational Complexity** | Day-2 ops burden: monitoring, backup, schema migration, on-call surface | Fully managed, zero infra ownership, standard tooling |

---

## Option A: SQLite with WAL Mode

### Overview

SQLite with Write-Ahead Logging enabled. Single database file per service instance (or per tenant shard). WAL mode enables concurrent reads during writes and reduces fsync frequency.

### A-1: Read Latency — Score: 3/5

WAL mode allows readers to proceed concurrently with a single writer, eliminating the read-blocking that plagues rollback-journal SQLite. For a single-instance deployment, read latency is excellent — typically 1-5ms for indexed queries on a warm page cache.

However, the inventory service is multi-tenant and cloud-native. SQLite is fundamentally a single-writer, single-host database. Horizontal read scaling requires either:
- Per-tenant database files (manageable at low tenant count, operationally expensive at scale)
- A read-replica pattern that SQLite does not natively support

At moderate multi-tenant load (hundreds of concurrent tenants), read latency degrades without a sharding strategy, and the sharding logic becomes application responsibility. P99 latency at scale is unreliable without careful per-tenant isolation.

**Verdict:** Good for single-tenant or low-concurrency scenarios. Read scaling requires non-trivial application-level sharding.

### A-2: Write Throughput — Score: 2/5

WAL mode supports exactly one writer at a time per database file. Write throughput is constrained by this serial writer bottleneck. Benchmarks for WAL mode on typical cloud VM storage show 2,000-8,000 writes/sec under favorable conditions (local NVMe, batched transactions). Network-attached storage, which is the norm in cloud deployments (EBS, Azure Managed Disk), reduces this to the 500-3,000 writes/sec range due to fsync latency.

For an inventory service receiving write bursts during peak order processing, this ceiling is a concrete risk. The application can batch writes into transactions to amortize overhead, but this introduces latency/throughput trade-offs and complicates error handling.

**Verdict:** Adequate for low-to-moderate write loads. Cloud storage fsync latency is the primary ceiling. Not suitable if sustained write throughput exceeds ~3K writes/sec.

### A-3: Corruption Recovery — Score: 4/5

This is SQLite's strongest dimension. WAL mode provides:
- Atomic commits: a write either completes fully or is rolled back via the WAL
- Crash recovery: on restart, SQLite replays or discards the WAL automatically
- No partial write exposure to readers during a crash
- Standard backup via `VACUUM INTO` or file-copy of the WAL + main file during a checkpoint

Point-in-time recovery requires an external backup solution (e.g., periodic snapshot to S3/Blob Storage). The single-file format makes backups operationally simple: copy the file.

The risk is at the host level. If the underlying storage volume is corrupted (rare but non-zero), recovery requires the last backup. There is no built-in replication to a secondary.

**Verdict:** Strong transactional integrity. Simple backup model. No native replication means PITR depends on external backup cadence.

### A-4: Operational Complexity — Score: 3/5

SQLite requires no server process, no connection pooling infrastructure, and no cluster management. In a containerized deployment:
- Schema migrations are straightforward (standard migration tools like FluentMigrator or EF Core migrations work)
- Monitoring is limited to file size and query latency (no built-in metrics server)
- Multi-tenant operation requires per-tenant file management

The operational simplicity breaks down at scale. Managing hundreds or thousands of per-tenant SQLite files (rotation, backup, migration) across container instances creates a custom operations surface that the team must build and maintain. There is no managed service to absorb this burden.

**Verdict:** Operationally simple for single-tenant or prototype scenarios. At multi-tenant scale, custom ops tooling is required.

---

## Option B: Event Store with JSON Snapshots

### Overview

Append-only event log where each inventory mutation is persisted as an immutable event. JSON snapshots taken every N events (commonly every 10-50) to bound replay time. Infrastructure options include EventStoreDB, Marten (PostgreSQL-backed), or a custom implementation.

### B-1: Read Latency — Score: 3/5

Current state reads require loading the latest snapshot and replaying events since the snapshot. For a well-tuned snapshot interval (every 10-20 events), this is typically 2-10ms for a single aggregate, comparable to a relational read.

The complication is cross-aggregate queries. If the inventory UI needs "all items in warehouse X below reorder threshold," the event store does not natively answer this. A read model (projection) must be built and maintained. Projection updates are eventually consistent: there is a lag between event write and read model update, typically 10-500ms depending on projection worker load.

For reporting or dashboard reads that tolerate eventual consistency, this is acceptable. For strict read-your-writes scenarios (e.g., immediately reading an item after updating it), the lag requires careful design (read from the event stream directly, or wait for projection).

**Verdict:** Single-aggregate reads are fast with good snapshot tuning. Cross-aggregate queries require projections with eventual consistency lag.

### B-2: Write Throughput — Score: 5/5

This is the event store's dominant advantage. Appending an event to the tail of a stream is one of the fastest write patterns available. EventStoreDB benchmarks regularly exceed 50,000 events/sec on commodity hardware. Marten on PostgreSQL with JSONB achieves 10,000-30,000 writes/sec.

Writes are non-blocking across aggregates. Concurrent writes to different inventory items do not contend with each other (each item has its own stream). Optimistic concurrency at the stream level prevents lost updates without broad locking.

For an inventory service with high write volume (order processing, stock adjustments, reservations), this pattern is a natural fit.

**Verdict:** Exceptional write throughput. Horizontal write scaling is architecturally straightforward. Best option in this dimension by a significant margin.

### B-3: Corruption Recovery — Score: 5/5

The append-only log is the strongest corruption recovery model. Key properties:
- Events are immutable once written — corruption cannot occur through a normal write path
- Snapshots are derived state; they can always be recomputed from the full event log
- Point-in-time recovery is native: replay events up to any timestamp
- EventStoreDB has built-in replication and cluster failover
- Any snapshot corruption is recoverable by recomputing from the event log

If the event log itself is corrupted (hardware failure), the log's replication factor determines durability. With EventStoreDB in a 3-node cluster, single-node failure has zero data loss. With Marten on a managed PostgreSQL (e.g., Azure Database for PostgreSQL with zone-redundant HA), similar guarantees apply.

This is the strongest data integrity model of the three options.

**Verdict:** Best-in-class corruption recovery. Append-only immutability prevents a class of corruption failures. PITR is native.

### B-4: Operational Complexity — Score: 2/5

This is the event store's significant liability. Operating an event store requires:
- Running and maintaining EventStoreDB (or a PostgreSQL cluster for Marten) — not a fully managed service in most cloud providers
- Building and maintaining projections for every read use case
- Managing snapshot compaction and stream truncation to control storage growth
- Understanding eventual consistency implications in the application layer
- On-call familiarity with event sourcing failure modes (projection lag, snapshot corruption, stream versioning)

If the team does not already have event sourcing experience, the learning curve is steep. Operationalizing projection workers, monitoring projection lag, and debugging cross-stream consistency issues requires specialized knowledge.

Marten on a managed PostgreSQL reduces some of this (no EventStoreDB ops), but projection management remains.

**Verdict:** Highest operational complexity of the three options. Requires either existing event sourcing expertise or investment in building it.

---

## Option C: CosmosDB Change Feed

### Overview

Azure CosmosDB (SQL API) for primary persistence. The change feed is a built-in ordered log of all mutations to a container, used for downstream processing, event propagation, and read model materialization. This is not a pure event store — CosmosDB stores current document state, and the change feed provides a derived mutation stream.

### C-1: Read Latency — Score: 5/5

CosmosDB offers single-digit millisecond P99 read latency globally as an SLA. With proper partition key design (tenant ID + item ID is the natural choice for an inventory service), point reads against the current document state are consistently 1-5ms P99.

Cross-partition queries (e.g., all items for a tenant below reorder threshold) are more expensive — 10-50ms depending on partition count and index configuration — but CosmosDB's indexing engine handles this automatically without requiring manual projection maintenance.

Read scaling is fully managed: CosmosDB handles replication, load balancing, and read scaling without operator intervention. Multi-region read replicas are a configuration option.

**Verdict:** Best read latency of the three options. Fully managed. Single-digit ms P99 as SLA guarantee.

### C-2: Write Throughput — Score: 4/5

CosmosDB write throughput is provisioned via Request Units (RUs). A typical 1KB document write costs approximately 5-10 RUs. At 10,000 RU/s (a moderate provisioning level), this supports 1,000-2,000 writes/sec at a single partition.

Autoscale RU provisioning (10x burst headroom) handles load spikes without manual intervention. Throughput scales linearly with RU allocation, so the inventory service is not write-constrained as long as the RU budget scales with load.

The cost model is the practical constraint: high sustained write throughput at CosmosDB is more expensive than self-managed options. The 5 RU/write baseline means 100K writes/sec requires 500K RU/s provisioned, which is a significant cost at scale.

**Verdict:** Strong write throughput with autoscale. Cost scales linearly with write volume — may be prohibitive at very high sustained write rates.

### C-3: Corruption Recovery — Score: 4/5

CosmosDB provides:
- Automatic replication across at least 4 replicas per region
- Point-in-time backup with 30-day retention (continuous backup mode available at additional cost)
- SLA-backed 99.999% availability with multi-region write
- Built-in corruption detection — CosmosDB's storage engine handles this transparently

The primary gap relative to Option B: CosmosDB stores current state, not full mutation history. If a logical corruption occurs (a bug overwrites correct data), the change feed provides a mutation log that can be replayed, but it is not an immutable append-only log in the same sense as Option B. The change feed retention window is configurable (default 24 hours for partition key ranges, configurable).

For the inventory service, this is an acceptable trade-off: the built-in backup/restore covers most recovery scenarios, and the change feed provides a short-horizon audit trail.

**Verdict:** Excellent managed durability. PITR via built-in backup. Change feed provides limited mutation history. Slightly behind Option B for full audit/replay scenarios.

### C-4: Operational Complexity — Score: 5/5

CosmosDB is a fully managed service. The operational burden is:
- Partition key design (done at schema definition time, difficult to change later — this is the key design decision)
- RU provisioning and cost monitoring
- Index policy configuration (defaults are reasonable; tuning is optional)
- Change feed consumer implementation (relatively straightforward with Azure Functions or SDK processors)

There is no cluster to operate, no replication to configure, no backup schedule to manage. Schema evolution is document-model native (add fields, no migrations required for additive changes). Monitoring is available through Azure Monitor with built-in metrics.

For a team that is already in the Azure ecosystem, this is the path of least operational resistance.

**Verdict:** Lowest operational complexity of the three options for a cloud-native Azure deployment. Fully managed with minimal day-2 burden.

---

## Comparative Matrix

| Dimension | Weight | Option A: SQLite WAL | Option B: Event Store | Option C: CosmosDB |
|-----------|--------|---------------------|----------------------|-------------------|
| Read Latency | 25% | 3 | 3 | **5** |
| Write Throughput | 30% | 2 | **5** | 4 |
| Corruption Recovery | 25% | 4 | **5** | 4 |
| Operational Complexity | 20% | 3 | 2 | **5** |
| **Weighted Score** | | **3.00** | **3.85** | **4.50** |

**Weight rationale:** Write throughput weighted highest (30%) for an inventory service with high mutation rate during order processing. Read latency and corruption recovery weighted equally (25% each) as both are critical for user experience and data integrity. Operational complexity weighted lowest (20%) but remains material — a high-complexity option that the team cannot operate reliably is not viable regardless of its technical merits.

---

## Synthesis and Recommendation

### Primary Recommendation: Option C — CosmosDB Change Feed

**Recommended with the following partition key design constraint: partition by `{tenantId}/{itemCategoryId}` to bound cross-partition query cost.**

CosmosDB achieves the highest weighted score (4.50) and is the only option that does not require the team to build or operate custom infrastructure. The review board should weigh this recommendation against two constraints:

1. **Azure lock-in:** CosmosDB is an Azure-native service. If the inventory service may need to run outside Azure, Option B (Marten on PostgreSQL) is the portable alternative with a weighted score of 3.85.
2. **Cost at scale:** CosmosDB's RU-based pricing is predictable but linear. If the inventory service is expected to sustain write rates above 50K/sec, perform a cost analysis before committing.

### Secondary Recommendation: Option B — Event Store (Marten) if audit/replay is a hard requirement

If the architecture review board requires full, immutable mutation history for regulatory audit, dispute resolution, or temporal queries ("what was the inventory state at time T?"), Option B is architecturally superior. The 5/5 write throughput and 5/5 corruption recovery scores reflect a data model that is purpose-built for exactly these properties. The 2/5 operational complexity score is the honest liability — the team must either already have event sourcing competency or budget the time to build it.

### Why Not Option A

SQLite with WAL mode is appropriate for prototypes, CLI tools, and single-tenant embedded scenarios. For a multi-tenant cloud-native inventory service, the single-writer bottleneck and absence of native replication make it unsuitable as a primary persistence store. The 2/5 write throughput score reflects a genuine architectural ceiling, not a configuration gap that can be tuned away.

---

## Risks and Mitigations

| Option | Top Risk | Mitigation |
|--------|----------|------------|
| A: SQLite WAL | Write contention under burst load | Pre-rule-out; not viable at target scale |
| B: Event Store | Projection lag causes stale reads | Implement read-your-writes token pattern; set explicit consistency SLAs |
| B: Event Store | Team lacks event sourcing expertise | Spike (1 week) before committing; evaluate Marten over EventStoreDB to reduce infra ops |
| C: CosmosDB | Poor partition key choice causes hot partition | Design partition key for uniform distribution before any data is written; this is irreversible post-production |
| C: CosmosDB | RU cost overrun under write spike | Set autoscale max RU cap; alert at 80% of budget; circuit-break non-critical write paths |
| C: CosmosDB | Change feed retention insufficient for audit | Enable continuous backup mode; if full audit log is required, supplement with event outbox pattern |

---

## Open Questions for the Review Board

These items require board input and cannot be resolved by analysis alone:

1. **Audit/replay requirement:** Does the inventory service have a regulatory or product requirement for immutable full mutation history? If yes, Option B is architecturally required regardless of operational cost. If no, Option C is the recommendation.

2. **Cloud portability:** Is Azure the permanent and exclusive deployment target? If there is any likelihood of needing to run outside Azure (on-prem, GCP, AWS), Option C is disqualifying.

3. **Write throughput ceiling:** What is the expected peak write rate at 2-year scale? If the answer is above 50K writes/sec sustained, a CosmosDB cost model review is required before commitment. Option B handles this at lower cost.

4. **Team capability:** Does the team have operational experience with event sourcing or CosmosDB? This should be a stated input to the final decision — a technically superior option operated by a team without the skills to run it produces worse outcomes than a technically adequate option the team can confidently operate.

---

**Analysis complete. Returning to orchestrator.**

*Worker agent ps-analyst — P-003 compliance confirmed: no sub-agents spawned, Task tool not invoked. All 12 evaluation cells and synthesis delivered in single pass per orchestrator coordination authority.*
