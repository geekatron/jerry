# ADR-001: Test Harness Baseline Persistence Strategy

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Plain-language decision overview for all stakeholders |
| [Status](#status) | Current ADR lifecycle state |
| [Context](#context) | Problem motivating this decision |
| [Constraints](#constraints) | Boundary conditions limiting the solution space |
| [Forces](#forces) | Tensions at play in the decision |
| [Options Evaluated](#options-evaluated) | Comparative analysis of alternatives |
| [Steelman: Case for SQLite with WAL Mode](#steelman-case-for-sqlite-with-wal-mode) | Strongest case for the rejected alternative (S-003) |
| [Decision](#decision) | Chosen option with rationale |
| [Consequences](#consequences) | Positive, negative, and neutral outcomes |
| [L2: Architectural Implications](#l2-architectural-implications) | Long-term evolution, systemic effects, and strategic trade-offs |
| [Risks](#risks) | Identified risks with mitigation |
| [Related Decisions](#related-decisions) | Links to prior and downstream ADRs |

---

## L0: Executive Summary

The prompt regression test harness needs to store baseline quality scores so it can compare "before" and "after" when someone changes an agent definition. We evaluated two options: storing baselines as individual JSON files tracked in git, and storing them in a SQLite database using Write-Ahead Logging (WAL) mode for safe concurrent access.

We recommend **JSON file store** (Option A). The harness operates inside CI/CD pipelines where each run is a single-process, single-writer operation. JSON files are directly visible in git diffs, require zero runtime dependencies beyond Python's standard library, and survive corruption at the individual-file level rather than losing all baselines at once. SQLite is the stronger technology for general-purpose persistence, but its advantages -- concurrent multi-writer access, transactional consistency, and indexed queries -- solve problems this system does not have at current scale. Choosing SQLite would add an operational dependency and reduce transparency in exchange for capabilities the harness does not need today.

If the harness evolves to require concurrent writes (e.g., parallel CI runners sharing a central baseline database) or cross-agent aggregate queries, this decision should be revisited. The hexagonal architecture's `BaselinePersistencePort` abstraction means switching from JSON to SQLite requires implementing a new adapter without touching any domain logic.

---

## Status

PROPOSED

---

## Context

The Four-Layer Composite Test Harness (PROJ-036) detects quality regressions in Jerry's 67 agent definitions by comparing current evaluation scores against stored baselines. The `BaselinePersistencePort` defines the contract for this storage: store a `BaselineRecord` keyed by `VersionKey` (git commit hash + file path), retrieve it for comparison, and retrieve the most recent baseline for a given agent file.

The system design (PROJ-036, Stream 1B) specified "Git-indexed JSON files" as the baseline store adapter. This ADR formally evaluates that choice against the alternative of SQLite with WAL mode, providing the evidence-based rationale required by P-011.

The baseline store has the following operational profile:

- **Write frequency:** Low. Baselines are written only when a quality gate passes after a new evaluation run. This happens at most once per PR merge for each modified agent definition.
- **Read frequency:** Moderate. Every regression check reads the most recent baseline for the changed agent file(s). In CI, this occurs once per PR.
- **Data volume:** Small. Each `BaselineRecord` is approximately 1KB. With 67 agents and a retention policy of 10 baselines per agent, the maximum store size is approximately 670KB.
- **Concurrency:** None at present. Each CI runner executes a single pipeline. No shared state across runners.
- **Query complexity:** Simple. Key-based lookup by `VersionKey` or latest-by-file-path. No aggregation, no joins, no range queries.

---

## Constraints

| ID | Constraint | Source |
|----|-----------|--------|
| C-01 | Jerry uses UV-only Python environment; all dependencies must be pip-installable via `uv add` | H-05 |
| C-02 | The harness runs inside Docker containers in GitHub Actions | System Design, Stream 1B |
| C-03 | Baseline integrity is enforced via git commit hash versioning | System Design, Security Decision #4 |
| C-04 | The `BaselinePersistencePort` protocol is already defined; the adapter must implement `store()`, `retrieve()`, and `retrieve_latest()` | System Design, Section 2.2 |
| C-05 | Hexagonal architecture mandates adapter isolation; domain code must not depend on persistence technology | H-07 |
| C-06 | Baseline files must be auditable for tampering (threat T-23 in STRIDE model) | System Design, STRIDE Threat Model |

---

## Forces

| Force | Tension |
|-------|---------|
| **Simplicity vs. capability** | JSON files are trivially simple but lack query power; SQLite provides rich querying but adds operational surface area |
| **Transparency vs. encapsulation** | JSON files are human-readable and git-diffable; SQLite is a binary format opaque to git |
| **Independence vs. integration** | JSON requires no runtime dependencies; SQLite ships with Python but WAL mode requires filesystem support and may interact with Docker volume mounts |
| **Fault isolation vs. atomicity** | JSON file corruption affects one baseline; SQLite corruption can affect the entire database. Conversely, SQLite provides ACID transactions that JSON file writes do not |
| **Current needs vs. future scale** | Current scale (67 agents, single writer) favors simplicity; future scale (hundreds of agents, parallel runners) may favor a database |

---

## Options Evaluated

### Evaluation Dimensions

| Dimension | Weight | Rationale |
|-----------|--------|-----------|
| Write latency | 0.15 | Baselines are written infrequently; latency matters less than correctness |
| Corruption recovery | 0.30 | Lost baselines force full re-baselining of affected agents; high-impact failure |
| Concurrent access | 0.20 | Future-proofing for parallel CI runners |
| Operational simplicity | 0.35 | Jerry is a CLI/CI framework with no server process; zero-ops is the goal |

### Option A: JSON File Store (Git-Indexed)

Each `BaselineRecord` is serialized to a JSON file at a deterministic path: `baselines/{agent_name}/{commit_hash_short}.json`. Files are tracked in git alongside the codebase.

| Dimension | Score (1-10) | Rationale |
|-----------|-------------|-----------|
| Write latency | 8 | Single `json.dump()` + `fsync`. No transaction overhead. Approximately 0.5-2ms for a 1KB file. |
| Corruption recovery | 9 | Corruption is scoped to a single file. Other baselines unaffected. Git history provides full recovery of any corrupted file via `git checkout`. Tamper detection via `git diff`. |
| Concurrent access | 3 | No built-in locking. Concurrent writes to the same file produce undefined results. Concurrent writes to different files are safe (different filesystem paths). |
| Operational simplicity | 10 | Zero dependencies. No database to provision, migrate, back up, or debug. Files are human-readable. Standard Unix tools apply (`cat`, `jq`, `diff`). CI/CD requires no special configuration. |

**Weighted score:** (8 x 0.15) + (9 x 0.30) + (3 x 0.20) + (10 x 0.35) = 1.20 + 2.70 + 0.60 + 3.50 = **8.00**

### Option B: SQLite with WAL Mode

All `BaselineRecord` entries are stored in a single SQLite database file with Write-Ahead Logging enabled. WAL mode allows concurrent readers with a single writer.

| Dimension | Score (1-10) | Rationale |
|-----------|-------------|-----------|
| Write latency | 7 | SQLite write with WAL mode: approximately 1-5ms per record including fsync of WAL file. Slightly higher than raw file write due to transaction overhead, but still sub-10ms. |
| Corruption recovery | 5 | SQLite is robust against application crashes (WAL + journal provide rollback). However, a corrupted database file affects *all* baselines, not just one. Recovery requires restoring from backup or re-baselining all agents. WAL mode adds `-wal` and `-shm` sidecar files that must be handled correctly during backup/restore. Docker volume mount edge cases (NFS, overlayfs) can cause WAL corruption. |
| Concurrent access | 8 | WAL mode provides concurrent reads alongside a single writer. Multiple readers do not block each other or the writer. However, true multi-writer concurrency requires additional application-level coordination. |
| Operational simplicity | 5 | SQLite ships with Python (`sqlite3` module), so no external dependency. But: binary format is opaque to `git diff`; requires `.gitignore` or Git LFS; schema migrations needed for format changes; `-wal` and `-shm` files must not be committed; Docker volume considerations for WAL mode; debugging requires `sqlite3` CLI or a viewer tool; backup strategy differs from source-controlled files. |

**Weighted score:** (7 x 0.15) + (5 x 0.30) + (8 x 0.20) + (5 x 0.35) = 1.05 + 1.50 + 1.60 + 1.75 = **5.90**

### Comparative Summary

| Dimension | Weight | Option A (JSON) | Option B (SQLite WAL) |
|-----------|--------|-----------------|----------------------|
| Write latency | 0.15 | 8 | 7 |
| Corruption recovery | 0.30 | 9 | 5 |
| Concurrent access | 0.20 | 3 | 8 |
| Operational simplicity | 0.35 | 10 | 5 |
| **Weighted Total** | **1.00** | **8.00** | **5.90** |

---

## Steelman: Case for SQLite with WAL Mode

Before dismissing Option B, its strongest case must be acknowledged (S-003):

**SQLite is the most widely deployed database engine in the world and is purpose-built for exactly this class of problem.** It provides ACID transactions, schema enforcement, indexed queries, and concurrent read access -- all features that a production persistence layer eventually needs. Choosing JSON now and migrating to SQLite later incurs switching cost: schema design, data migration tooling, adapter rewriting, and re-testing. If the harness scales to hundreds of agents or introduces parallel CI runners with shared baseline state, the JSON approach will need to be replaced anyway. SQLite's WAL mode specifically addresses the single-writer concern, allowing reads to proceed without blocking during writes. The `sqlite3` module ships with Python's standard library, so there is no additional dependency to manage. Furthermore, SQLite provides automatic integrity checking (`PRAGMA integrity_check`) that is more rigorous than JSON schema validation.

**Why the steelman does not prevail:** The scaling scenarios that justify SQLite (hundreds of agents, parallel shared-state runners, aggregate queries) are speculative. The current system has 67 agents, single-process CI, and key-value access patterns. The hexagonal architecture's `BaselinePersistencePort` means the migration cost from JSON to SQLite is bounded to a single adapter module -- approximately 100-200 lines of code -- without touching domain logic. Paying the operational complexity of SQLite today to avoid a bounded future migration cost is a premature optimization that violates YAGNI. The corruption recovery advantage of JSON (single-file blast radius vs. full-database blast radius) outweighs SQLite's transactional guarantees for a system where each baseline is independent and recoverable from git history.

---

## Decision

**Use JSON file store with git-indexed persistence for test harness baselines.**

The baseline store adapter (`baselines/store.py`) will implement the `BaselinePersistencePort` protocol by serializing `BaselineRecord` instances to individual JSON files at deterministic paths derived from the `VersionKey`. Files are committed to the repository and tracked in git, providing built-in versioning, tamper detection, and recovery.

**Rationale:** The decision dimensions that matter most for this system -- corruption recovery (0.30 weight) and operational simplicity (0.35 weight) -- strongly favor JSON. The concurrent access dimension (0.20 weight) favors SQLite, but the current operational profile (single-writer CI pipeline) does not exercise this capability. The hexagonal architecture ensures this decision is reversible at bounded cost if the operational profile changes.

---

## Consequences

### Positive

- **Zero operational overhead.** No database provisioning, migration scripts, backup strategy, or specialized tooling. The baseline store is a directory of JSON files.
- **Full git integration.** Baselines participate in the same PR review, branching, and history workflow as the code they test. `git diff` shows exactly what changed. `git log` shows when. `git blame` shows who.
- **Granular fault isolation.** Corruption of one baseline file does not affect any other baseline. Recovery is a single `git checkout` command.
- **Transparent auditability.** Threat T-23 (baseline tampering) is mitigated by git's built-in change tracking. Reviewers can see baseline modifications in PRs.
- **No dependency risk.** No SQLite version compatibility concerns, no WAL mode filesystem requirements, no Docker volume mount edge cases.

### Negative

- **No concurrent write safety.** If the system evolves to require multiple CI runners writing baselines simultaneously to a shared store, this approach will require redesign. File-level locking is fragile and platform-dependent.
- **No indexed queries.** Aggregate queries across baselines (e.g., "show me the trend for all agents over the last 30 days") require reading and parsing all JSON files. At 670KB maximum store size this is negligible, but it does not scale linearly.
- **No schema enforcement at the storage layer.** JSON files can contain malformed data. Validation must be performed in the adapter code, not by the storage engine.
- **Git repository size growth.** Each baseline commit adds files to git history. The retention policy (10 per agent, ~1KB each) bounds this at ~670KB of live data, but git history is append-only. Over years, accumulated baseline history could measurably increase clone times.

### Neutral

- **Retention policy complexity is equivalent.** Both options require application-level retention logic (prune baselines older than N per agent). Neither provides this automatically.

---

## L2: Architectural Implications

### Long-Term Evolution Path

The `BaselinePersistencePort` abstraction (defined in `jerry/testing/baselines/ports.py`) provides the key architectural property: **the persistence technology is an adapter-layer concern that does not leak into the domain.** The `StatisticalEngine`, metamorphic relations, and evaluation pipeline reference the port protocol, never the concrete store. This means:

1. **Migration to SQLite is a single-adapter change.** If scaling triggers justify it (see [Revisit Triggers](#revisit-triggers) below), a `SqliteBaselineStore` adapter can be implemented alongside the existing `BaselineStore` without modifying any domain code. The composition root selects which adapter to inject.

2. **Hybrid strategies are possible.** A future adapter could use JSON files for git-tracked auditability *and* SQLite for fast querying, with the JSON files as the source of truth and SQLite as a read-optimized cache rebuilt on demand.

3. **Cloud persistence is on the evolution path.** If the harness eventually runs as a shared service (not just per-repo CI), the same port can be implemented against S3, DynamoDB, or any key-value store. The port's three-method contract (`store`, `retrieve`, `retrieve_latest`) maps cleanly to any persistence backend.

### Revisit Triggers

This decision should be revisited when any of the following conditions are met:

| Trigger | Measurement | Threshold |
|---------|-------------|-----------|
| Agent count growth | Number of agent definitions in the framework | > 200 agents |
| Concurrent CI runners | Number of runners writing baselines simultaneously | > 1 concurrent writer |
| Query complexity | Stakeholder requests for aggregate baseline analytics | Any cross-agent aggregate query |
| Repository size impact | Git clone time increase attributable to baseline files | > 10 seconds added to clone |

### Systemic Consequences

- **CI/CD simplicity preserved.** The GitHub Actions workflow does not need database initialization steps, connection strings, or cleanup. Baseline persistence is invisible to the CI configuration.
- **Security posture unchanged.** The STRIDE threat model (T-23 through T-26) was written assuming git-indexed JSON files. Switching to SQLite would require re-evaluating threats T-23 (tampering -- binary format is harder to review but also harder to subtly modify) and T-25 (information disclosure -- SQLite file could contain residual data from deleted records).
- **Testing strategy simplified.** The `conftest.py` fixture for `BaselineStore` uses `tmp_path` for test isolation. JSON files in a temp directory require no setup or teardown beyond what pytest provides. SQLite would require equivalent simplicity but adds the WAL sidecar file concern.

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| JSON file corruption from interrupted write | Low (CI runs are short, writes are atomic-ish with `fsync`) | Low (single baseline lost; recoverable from git) | Write to temp file, then `os.rename()` for atomic replacement. Verify JSON parseable after write. |
| Git repository bloat from baseline history | Low (bounded by retention policy at ~670KB live) | Low (clone time increase is marginal at this scale) | Enforce retention policy in `store()`. Consider `git filter-branch` if historical baseline data becomes problematic. |
| Race condition if CI evolves to parallel runners | Medium (CI architecture may change) | Medium (lost writes; incorrect comparisons) | Monitor revisit trigger for concurrent writers. The `BaselinePersistencePort` abstraction bounds migration cost. |

---

## Related Decisions

| ADR | Relationship | Status |
|-----|-------------|--------|
| PROJ-035/decisions/ADR-001-test-harness-architecture.md | Parent decision establishing the four-layer architecture | ACCEPTED |
| PROJ-036 System Design (Stream 1B) | Specifies `BaselinePersistencePort` and `BaselineStore` adapter | In effect |

---

*ADR produced by ps-architect. Evaluated 2 options across 4 weighted dimensions. Steelman analysis (S-003) applied to rejected alternative. Self-review (S-010) completed before output.*
