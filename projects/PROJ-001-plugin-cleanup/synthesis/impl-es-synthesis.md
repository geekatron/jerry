# Event Sourcing Infrastructure Synthesis

**PS ID:** impl-es
**Entry ID:** synthesis
**Date:** 2026-01-09
**Author:** ps-synthesizer agent (v2.0.0)
**Methodology:** Braun & Clarke Thematic Analysis
**Status:** Complete

---

## Input Sources

| Doc ID | Title | Key Focus |
|--------|-------|-----------|
| e-001 | Event Sourcing Patterns | IEventStore, ISnapshotStore, AggregateRoot patterns |
| e-002 | TOON Serialization | Token-Oriented Object Notation for LLM efficiency |
| e-003 | BDD/TDD Patterns | Testing patterns for Event-Sourced systems |
| e-004 | Distinguished Review | Code review patterns from Google/Microsoft |
| e-005 | Concurrent Access | File locking and concurrency patterns |
| e-006 | Work Item Schema | Domain model and domain events |

---

## L0: Executive Summary (ELI5)

### What We Discovered

When building a system that needs to remember everything that happened (like a smart notebook that never forgets), we found six important ideas that keep appearing across all our research:

**1. Events Are Sacred** - Once something happens, we write it down and never change it. Like a diary entry, we can add new pages but never erase old ones. This creates a perfect history of what happened.

**2. Smart Boundaries** - We organize work into groups (called "aggregates") where everything inside the group stays consistent. Think of it like departments in a company - each department manages its own stuff, and they talk to each other through memos (events).

**3. Optimistic Thinking** - Instead of locking things when someone wants to make changes, we let everyone try and check at the end if there was a conflict. Like multiple people editing a shared document - we merge changes if we can, or ask for help if we cannot.

**4. Token Efficiency** - When talking to AI assistants, we use a compact format (TOON) that says the same thing with fewer words. This saves money and makes the AI work better.

**5. Test Everything** - We test happy paths (when things work), sad paths (when things fail), and edge cases (unusual situations). The ratio should be roughly 60-70% happy, 20-30% sad, 10-15% edge.

**6. Layer Discipline** - The core business logic (domain) should know nothing about databases or files. It just focuses on the rules. Other layers handle the messy details.

### Top Cross-Cutting Pattern

**Event-Driven Aggregate Design with Optimistic Concurrency** emerged as the dominant architectural pattern. All six documents converge on this approach:
- Domain events capture state changes (e-001, e-003, e-006)
- Aggregates enforce boundaries and invariants (e-001, e-004, e-006)
- Optimistic concurrency with version checks prevents conflicts (e-001, e-005)
- Testing follows Given-Events/When-Command/Then-Events pattern (e-003)

### Key Insight

The filesystem can be treated as a durable event store when proper file locking (filelock library) and optimistic concurrency (version checking) are combined. This eliminates the need for external databases while maintaining full audit trails and crash recovery capability.

---

## L1: Technical Synthesis (Software Engineer)

### Cross-Reference Matrix

The following matrix shows concept agreement across all six source documents. A checkmark indicates the document addresses the concept; bold indicates primary treatment.

| Concept | e-001 | e-002 | e-003 | e-004 | e-005 | e-006 | Agreement |
|---------|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:---------:|
| Domain Events | **X** | | X | X | | **X** | HIGH (4/6) |
| Aggregate Boundaries | **X** | | X | **X** | | **X** | HIGH (4/6) |
| Optimistic Concurrency | **X** | | X | X | **X** | | HIGH (4/6) |
| Event Versioning | **X** | | | X | | **X** | MEDIUM (3/6) |
| File Locking | X | | | | **X** | | MEDIUM (2/6) |
| Hexagonal Architecture | X | X | X | **X** | | | HIGH (4/6) |
| BDD/TDD Patterns | | | **X** | X | | | MEDIUM (2/6) |
| Token Optimization | | **X** | | | | | LOW (1/6) |
| Snapshot Strategies | **X** | | X | | | | MEDIUM (2/6) |
| Idempotency | X | | | **X** | X | | MEDIUM (3/6) |
| Quality Gates | | | **X** | X | | **X** | MEDIUM (3/6) |
| State Machines | | | | X | | **X** | MEDIUM (2/6) |

### Consolidated Implementation Patterns

#### Pattern 1: Event Store Interface (HIGH agreement)

All relevant sources agree on this interface shape:

```python
class IEventStore(Protocol):
    def append(
        self,
        stream_id: str,
        events: Sequence[StoredEvent],
        expected_version: int
    ) -> None: ...

    def read(
        self,
        stream_id: str,
        from_version: int = 0,
        to_version: int | None = None
    ) -> Sequence[StoredEvent]: ...

    def get_version(self, stream_id: str) -> int: ...
```

**Sources:** e-001 (primary), e-003 (contract tests), e-005 (file implementation)

#### Pattern 2: Aggregate Root with Event Emission (HIGH agreement)

```python
class AggregateRoot(ABC):
    def _raise_event(self, event: DomainEvent) -> None:
        self._version += 1
        self._apply(event)
        self._pending_events.append(event)

    def collect_events(self) -> Sequence[DomainEvent]: ...

    @abstractmethod
    def _apply(self, event: DomainEvent) -> None: ...

    @classmethod
    def load_from_history(cls, events: Sequence[DomainEvent]) -> Self: ...
```

**Sources:** e-001 (primary), e-003 (testing), e-004 (review), e-006 (WorkItem)

#### Pattern 3: File-Based Concurrency (MEDIUM agreement)

```python
from filelock import FileLock

def append(self, stream_id: str, events: list, expected_version: int) -> int:
    with FileLock(f"{stream_id}.lock"):
        current_version = self._get_version(stream_id)
        if current_version != expected_version:
            raise ConcurrencyConflictError(...)

        # Append with fsync for durability
        with open(stream_path, 'a') as f:
            for event in events:
                f.write(json.dumps(event) + '\n')
            f.flush()
            os.fsync(f.fileno())
```

**Sources:** e-001 (json adapter), e-005 (primary)

#### Pattern 4: Given-When-Then Testing (MEDIUM agreement)

```gherkin
Scenario: Successfully complete work item
  Given the following events have occurred:
    | event_type        | item_id   | status      |
    | WorkItemCreated   | WORK-001  | pending     |
    | StatusChanged     | WORK-001  | in_progress |
  When the command "CompleteItem" is executed
  Then the following events should be raised:
    | event_type        | final_status |
    | WorkItemCompleted | done         |
```

**Sources:** e-003 (primary), e-004 (review focus)

#### Pattern 5: TOON for LLM Context (SPECIALIZED)

```python
# JSON (320 tokens):
[{"item_id":"WORK-001","title":"Task 1","status":"done"},...]

# TOON (180 tokens, 44% reduction):
[2]{item_id,title,status}:
  WORK-001,Task 1,done
  WORK-002,Task 2,in_progress
```

**Source:** e-002 (primary, specialized for LLM interface)

### Implementation Recommendations

| Priority | Component | Location | Pattern Source |
|----------|-----------|----------|----------------|
| P0 | IEventStore port | domain/ports/ | e-001 |
| P0 | FileSystemEventStore | infrastructure/persistence/ | e-001, e-005 |
| P0 | AggregateRoot base | domain/aggregates/ | e-001, e-006 |
| P0 | DomainEvent base | domain/events/ | e-001, e-006 |
| P1 | WorkItem aggregate | domain/aggregates/ | e-006 |
| P1 | Event contract tests | tests/contracts/ | e-003 |
| P1 | Value objects | domain/value_objects/ | e-006 |
| P2 | ISnapshotStore port | domain/ports/ | e-001 |
| P2 | ToonSerializer | infrastructure/adapters/ | e-002 |
| P2 | BDD step definitions | tests/bdd/ | e-003 |

### Contradictions and Resolutions

| Contradiction | Sources | Resolution |
|---------------|---------|------------|
| Snapshot necessity | e-001 recommends snapshots; e-005 focuses on append-only | **Defer snapshots** until event counts exceed 50 per stream (e-001 threshold). Jerry's typical work items have <20 events. |
| Lock granularity | e-001 uses fcntl; e-005 recommends filelock | **Use filelock** for cross-platform compatibility. fcntl is POSIX-only. |
| Event format | e-001 uses JSON; e-002 recommends TOON | **Use JSON for persistence** (human-debuggable, e-001), **TOON for LLM context** (token-efficient, e-002). Both approaches serve different layers. |
| Test distribution | e-003: 60-70% positive; e-004: varies by risk | **Follow e-003 for aggregates** (60-70/20-30/10-15 positive/negative/edge). **Follow e-004 tiered review** for change risk assessment. |

---

## L2: Strategic Synthesis (Principal Architect)

### Emergent Architectural Themes

#### Theme 1: Domain-Centric Event Sourcing

The synthesis reveals a consistent architectural vision where:

1. **Domain layer is pure** - No external dependencies (e-001, e-004)
2. **Events are the source of truth** - State is derived from event replay (e-001, e-003, e-006)
3. **Aggregates enforce invariants** - Transaction boundaries match consistency boundaries (e-001, e-004, e-006)

This aligns with hexagonal architecture principles where the domain is isolated from infrastructure concerns.

#### Theme 2: Filesystem as Infrastructure

The research validates filesystem-based persistence for Jerry's use case:

- **e-001** provides the event store interface pattern
- **e-005** validates file locking and concurrency patterns
- **e-002** optimizes for LLM context windows

This approach eliminates external database dependencies while maintaining ACID-like guarantees through file locking and atomic operations.

#### Theme 3: Testing as Specification

BDD patterns from e-003 and review patterns from e-004 converge on:

- **Given-When-Then** matches event sourcing naturally
- **Contract tests** verify adapter implementations
- **Quality gates** enforce test distribution (e-003, e-006)

Testing becomes a specification mechanism, not just verification.

### Long-Term Implications

| Implication | Impact | Mitigation |
|-------------|--------|------------|
| Event schema evolution | Breaking changes are extremely expensive | Version all events from day one (e-001, e-004, e-006) |
| Storage growth | Events accumulate indefinitely | Implement snapshot strategy when needed (e-001) |
| Cross-agent consistency | Multiple agents may conflict | Optimistic concurrency with retry (e-005) |
| Context window limits | Event history may exceed limits | TOON serialization for summaries (e-002) |
| Aggregate boundary changes | Requires data migration | Define boundaries carefully upfront (e-004) |

### Strategic Tensions and Trade-offs

#### Tension 1: Simplicity vs Completeness

- **e-001** recommends full ES infrastructure (snapshots, projections)
- **e-005** focuses on minimal viable implementation

**Resolution:** Start with append-only events, add snapshots when performance requires. Jerry's initial workload is low-volume.

#### Tension 2: Token Efficiency vs Debuggability

- **e-002** optimizes for LLM token reduction
- **e-001, e-005** emphasize human-readable JSON

**Resolution:** Layer-appropriate formats. JSON for persistence (infrastructure), TOON for LLM interface (interface layer).

#### Tension 3: Strict Typing vs Flexibility

- **e-006** defines precise value objects with validation
- **e-001** uses generic dict-based events

**Resolution:** Strong typing in domain layer (e-006 value objects), serialize to dicts at persistence boundary.

### ADR Recommendations

Based on this synthesis, the following ADRs should be created:

| ADR | Title | Key Decision |
|-----|-------|--------------|
| ADR-010 | Event Store Implementation | Filesystem-based with filelock + optimistic concurrency |
| ADR-011 | Event Schema Strategy | Versioned events with additive-only evolution |
| ADR-012 | Snapshot Policy | Event-count-based (50 threshold), deferred implementation |
| ADR-013 | Serialization Strategy | JSON for persistence, TOON for LLM context |
| ADR-014 | Test Distribution | 60-70% positive, 20-30% negative, 10-15% edge |

---

## Knowledge Items Generated

### Patterns (PAT-XXX)

---

### PAT-001: Event Store Interface Pattern

**Context:** When implementing event sourcing with append-only storage and optimistic concurrency.

**Problem:** Need a standard interface for persisting and retrieving domain events that works across different storage backends (file, database, cloud).

**Solution:** Define a Protocol/interface with three core methods:
- `append(stream_id, events, expected_version)` - Atomic append with concurrency check
- `read(stream_id, from_version, to_version)` - Retrieve events from stream
- `get_version(stream_id)` - Current stream version for concurrency

**Consequences:**
(+) Storage-agnostic domain layer
(+) Easy to swap implementations (file, PostgreSQL, CosmosDB)
(+) Clear contract for testing
(-) Additional abstraction layer
(-) Version tracking overhead

**Quality:** HIGH (4/6 source agreement: e-001, e-003, e-004, e-005)
**Sources:** e-001 (primary), e-003, e-004, e-005

---

### PAT-002: Aggregate Root Event Emission

**Context:** When implementing event-sourced domain aggregates that must record all state changes.

**Problem:** Aggregates need to track pending events, apply them to internal state, and provide them for persistence, all while maintaining encapsulation.

**Solution:** Base class with:
- `_raise_event(event)` - Records event, increments version, applies to state
- `_apply(event)` - Abstract method for state mutation (must be overridden)
- `collect_events()` - Returns and clears pending events
- `load_from_history(events)` - Factory to reconstitute from event stream

**Consequences:**
(+) Consistent event emission across all aggregates
(+) Built-in versioning for concurrency
(+) Deterministic state reconstruction
(-) All aggregates must inherit from base
(-) Apply method must be implemented for each event type

**Quality:** HIGH (4/6 source agreement: e-001, e-003, e-004, e-006)
**Sources:** e-001 (primary), e-003, e-004, e-006

---

### PAT-003: Optimistic Concurrency with File Locking

**Context:** When multiple agents/processes may modify the same event stream concurrently.

**Problem:** Need to prevent lost updates and detect conflicts without holding locks during business logic processing.

**Solution:** Two-phase approach:
1. Acquire file lock (using filelock library for cross-platform)
2. Check expected_version matches current version
3. If match: append events, release lock
4. If mismatch: raise ConcurrencyConflictError, retry with exponential backoff

**Consequences:**
(+) Cross-platform (Windows, Linux, macOS)
(+) No long-held locks during processing
(+) Conflicts detected at commit time
(-) Retry logic required at caller
(-) File lock overhead on every write

**Quality:** HIGH (4/6 source agreement: e-001, e-003, e-004, e-005)
**Sources:** e-001, e-005 (primary), e-003, e-004

---

### PAT-004: Given-When-Then Event Testing

**Context:** When testing event-sourced aggregates using BDD style.

**Problem:** Traditional state-based assertions don't capture the full behavior of event-sourced systems.

**Solution:** Test pattern:
- **Given:** Historical events that establish aggregate state
- **When:** Command execution
- **Then:** Expected events raised (not state assertions)

Use pytest-bdd with DataTables for event specifications.

**Consequences:**
(+) Tests are specifications of behavior
(+) Natural mapping to event sourcing semantics
(+) Easy to understand for domain experts
(-) Requires fixture infrastructure
(-) More verbose than simple unit tests

**Quality:** MEDIUM (2/6 primary agreement, 4/6 mention: e-003, e-004)
**Sources:** e-003 (primary), e-004

---

### PAT-005: TOON for LLM Context Serialization

**Context:** When formatting structured data (arrays of objects) for LLM consumption.

**Problem:** JSON is token-heavy, wasting context window space and increasing costs.

**Solution:** Use TOON (Token-Oriented Object Notation) for uniform arrays:
- Tabular format: `[N]{field1,field2}:\n  val1,val2`
- 40-60% token reduction for typical work item lists
- 4-6% accuracy improvement on structured extraction

**Consequences:**
(+) Significant token savings
(+) Improved LLM accuracy on structured data
(+) Human-readable format
(-) Limited ecosystem support
(-) Not suitable for nested/heterogeneous data

**Quality:** LOW (1/6 source, specialized use case: e-002)
**Sources:** e-002 (primary)

---

### PAT-006: Hybrid Identity (Snowflake + Display ID)

**Context:** When work items need both machine-friendly uniqueness and human-friendly references.

**Problem:** UUIDs are unique but unmemorable; sequential IDs require coordination.

**Solution:** Two-part identity:
- `internal_id`: Snowflake 64-bit ID (unique, time-sortable, no coordination)
- `display_id`: `WORK-nnn` format (human-readable, sequential per project)

**Consequences:**
(+) Collision-free across distributed agents
(+) Human-friendly references in UI/logs
(+) Time-based sorting from Snowflake
(-) Two IDs to manage
(-) Display ID gaps if items deleted

**Quality:** MEDIUM (2/6 source agreement: e-006 primary, e-001 mentions)
**Sources:** e-006 (primary), e-001

---

### PAT-007: Tiered Code Review for ES Systems

**Context:** When reviewing changes to event-sourced systems.

**Problem:** Not all changes carry equal risk; event schema changes are especially dangerous.

**Solution:** Risk-based review tiers:
- **Critical** (event schemas): Senior + Architect, ADR required
- **High** (aggregate boundaries): Senior reviewer, domain expert
- **Medium** (command handlers): Standard 2-reviewer
- **Low** (projections/read models): 1 reviewer

**Consequences:**
(+) Appropriate review effort for risk level
(+) Prevents expensive post-deployment fixes
(+) Documents rationale for high-risk changes
(-) Slower velocity for critical changes
(-) Requires risk classification discipline

**Quality:** MEDIUM (2/6 source agreement: e-004 primary, e-003)
**Sources:** e-004 (primary), e-003

---

### PAT-008: Value Object Quality Gates

**Context:** When enforcing quality metrics (test coverage, test ratios) on work items.

**Problem:** Quality metrics need validation, comparison operations, and integration with completion gates.

**Solution:** Self-validating value objects:
- `TestCoverage`: Validates 0-100%, provides `meets_threshold()`
- `TestRatio`: Validates positive/negative/edge counts, provides `meets_level(L0/L1/L2)`
- Immutable (frozen dataclass) for safety

**Consequences:**
(+) Invalid values rejected at creation
(+) Business logic encapsulated in value object
(+) Thread-safe, hashable
(-) More classes to maintain
(-) New instance for each value change

**Quality:** MEDIUM (3/6 source agreement: e-003, e-004, e-006)
**Sources:** e-006 (primary), e-003, e-004

---

### Lessons (LES-XXX)

---

### LES-001: Event Schemas Are Forever

**Context:** Discovered when analyzing event versioning strategies across e-001, e-004, and e-006.

**Lesson:** Once an event is published to the store, its schema becomes a permanent contract. Breaking changes are extremely expensive because:
1. Old events must remain readable forever
2. Upcasting code accumulates
3. Multiple consumers may depend on the schema

**Evidence:**
- e-001: "Include event version in event type, use upcasters"
- e-004: "Events are immutable contracts - review as carefully as public APIs"
- e-006: "Additive changes only - new fields optional with defaults"

**Recommendation:** Invest heavily in upfront event design. Version from day one. Never remove or rename fields.

---

### LES-002: Layer Violations Compound

**Context:** Discovered from hexagonal architecture guidance in e-001, e-002, e-004.

**Lesson:** A single import of infrastructure concerns into the domain layer creates a crack that widens over time. What starts as "just one import" leads to:
1. Tighter coupling to specific technologies
2. Harder testing (need to mock infrastructure)
3. Reduced portability

**Evidence:**
- e-004: "Domain layer must never depend on infrastructure"
- e-001: "Ports defined in domain, adapters in infrastructure"
- e-002: "TOON serializer lives in infrastructure adapters"

**Recommendation:** Use static analysis (ArchUnit, custom linters) to enforce layer boundaries in CI. Prevention is cheaper than correction.

---

### LES-003: Retry is Not Optional

**Context:** Discovered from concurrency handling patterns in e-005.

**Lesson:** In any optimistic concurrency system, conflicts WILL happen. Systems that don't implement retry with backoff will fail under concurrent load.

**Evidence:**
- e-005: "Exponential backoff + jitter prevents thundering herd"
- e-005: Provides tenacity-based retry implementation

**Recommendation:** Always implement retry at the command handler level. Use exponential backoff with jitter (not linear or fixed delays).

---

### Assumptions (ASM-XXX)

---

### ASM-001: Low Event Volume

**Context:** Decision to defer snapshot implementation.

**Assumption:** Jerry's work items will typically have fewer than 50 events in their lifetime.

**Basis:**
- Typical work item lifecycle: Created -> Started -> (Blocked)? -> Completed
- Quality metrics updated 1-3 times
- Average event count: 5-15 per item

**Invalidation Trigger:** If event streams regularly exceed 50 events, implement snapshot strategy per e-001.

**Risk:** Medium - If invalidated, aggregate load times will degrade linearly with event count.

---

### ASM-002: Single-Machine Concurrency

**Context:** Choice of filelock over distributed locking.

**Assumption:** Jerry will run as a single-machine application (or with filesystem-based coordination only).

**Basis:**
- e-005 recommends filelock for cross-platform
- No distributed locking infrastructure (Redis, ZooKeeper) assumed

**Invalidation Trigger:** If Jerry needs multi-machine coordination, require distributed locking (Redis, etc.).

**Risk:** Low - Jerry's design targets single-developer workflow.

---

### ASM-003: LLM Token Costs Matter

**Context:** Investment in TOON serialization research (e-002).

**Assumption:** Token costs and context window limits are significant constraints for Jerry's LLM integration.

**Basis:**
- e-002: 40-60% token reduction with TOON
- Context window limits affect agent performance (context rot)

**Invalidation Trigger:** If LLM costs drop significantly or context windows expand dramatically, TOON may be unnecessary complexity.

**Risk:** Low - Token efficiency also improves accuracy, independent of cost.

---

### ASM-004: Test Distribution is Universal

**Context:** Adoption of 60-70/20-30/10-15 test ratio.

**Assumption:** This distribution applies to all aggregate testing regardless of domain.

**Basis:**
- e-003: Industry-standard test pyramid ratios
- e-004: Google/Microsoft engineering practices

**Invalidation Trigger:** If specific aggregates require different distributions (e.g., security-critical needs more negative tests).

**Risk:** Low - The ratio is a guideline, not a strict rule.

---

## Thematic Analysis Summary

### Phase 1: Familiarization
Read all 6 input documents, noting recurring concepts and terminology.

### Phase 2: Coding
Identified 12 key concepts: Domain Events, Aggregate Boundaries, Optimistic Concurrency, Event Versioning, File Locking, Hexagonal Architecture, BDD/TDD Patterns, Token Optimization, Snapshot Strategies, Idempotency, Quality Gates, State Machines.

### Phase 3: Theme Search
Grouped concepts into 3 candidate themes:
- Event-Centric Architecture (events, aggregates, versioning)
- Infrastructure Resilience (locking, concurrency, retries)
- Quality Assurance (testing, review, gates)

### Phase 4: Theme Review
Validated themes against data:
- Event-Centric Architecture: Supported by e-001, e-003, e-004, e-006
- Infrastructure Resilience: Supported by e-001, e-005
- Quality Assurance: Supported by e-003, e-004, e-006

### Phase 5: Theme Definition
Final themes:
1. **Domain-Centric Event Sourcing** - Pure domain, event-driven state
2. **Filesystem as Infrastructure** - File-based persistence with locking
3. **Testing as Specification** - BDD patterns, quality gates

### Phase 6: Report
This synthesis document captures findings with source citations and quality assessments.

---

## Compliance

| Principle | Status | Evidence |
|-----------|--------|----------|
| P-001 (Truth/Accuracy) | COMPLIANT | All patterns cite source documents |
| P-002 (File Persistence) | COMPLIANT | Document written to filesystem |
| P-004 (Reasoning) | COMPLIANT | Thematic analysis documented |
| P-010 (Task Tracking) | COMPLIANT | Synthesis complete as assigned |

---

## Document Metadata

- **Total Patterns:** 8 (PAT-001 through PAT-008)
- **Total Lessons:** 3 (LES-001 through LES-003)
- **Total Assumptions:** 4 (ASM-001 through ASM-004)
- **Source Documents:** 6
- **Methodology:** Braun & Clarke Thematic Analysis (6 phases)
- **Created:** 2026-01-09
- **Author:** ps-synthesizer agent v2.0.0
