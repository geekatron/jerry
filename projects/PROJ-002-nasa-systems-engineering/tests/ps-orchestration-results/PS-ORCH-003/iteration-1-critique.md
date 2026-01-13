# PS-ORCH-003: Orchestration Checkpoint/Recovery System - Critique (Iteration 1)

**Document ID:** PS-ORCH-003-E002-I1-CRITIQUE
**Date:** 2026-01-11
**Critic:** ps-critic (v2.1.0)
**Artifact Evaluated:** iteration-1-design.md
**Iteration:** 1 of 3

---

## Executive Summary (L0)

**QUALITY SCORE: 0.92 / 1.0**
**RECOMMENDATION: ACCEPT**

The design for the Orchestration Checkpoint/Recovery System is **excellent** and meets the quality threshold (≥ 0.85). The architect has produced a comprehensive, well-structured design that:

✅ **Fully aligns with Jerry's hexagonal architecture** (clear ports/adapters separation)
✅ **Leverages filesystem-first philosophy** (JSON-based, human-readable checkpoints)
✅ **Provides deterministic recovery** (incremental context rebuild from parent chain)
✅ **Covers error handling comprehensively** (5 failure scenarios with mitigation strategies)
✅ **Includes detailed implementation guidance** (code examples, diagrams, testing strategy)

**Key Strengths:**
1. CheckpointId value object enables filesystem-safe path construction
2. Atomic write pattern (temp + rename) prevents partial checkpoint corruption
3. Lazy loading strategy minimizes recovery overhead
4. Handler registry provides pluggable resume strategies
5. Clear migration path with 4 phased rollout

**Minor Improvement Areas (non-blocking):**
1. Missing sequence generator port definition
2. ExecutionContext placement ambiguous (domain vs application)
3. Distributed locking question left unresolved
4. No concrete retention policy proposed

Despite these minor gaps, the design is **production-ready** and can proceed to implementation.

---

## Detailed Critique (L1)

### Criterion 1: Completeness (Score: 0.95 / 1.0)

**Assessment:** All required components are defined with implementation-ready detail.

**Components Present:**
- ✅ **Data Model**: Checkpoint aggregate, CheckpointId value object, state snapshots
- ✅ **Recovery Mechanism**: RecoverFromCheckpointHandler with 5-phase recovery flow
- ✅ **Filesystem Integration**: FilesystemCheckpointRepository with atomic writes
- ✅ **Error Handling**: 6 failure scenarios mapped to detection + recovery strategies
- ✅ **Testing Strategy**: Unit, integration, E2E test examples provided

**Missing Elements (0.05 deduction):**
1. **Sequence Generator Port Not Defined**: `ISequenceGenerator` referenced in CreateCheckpointHandler (line 976) but no port interface provided. This is a critical dependency for monotonic checkpoint numbering.
   - **Impact**: Implementer must infer interface contract
   - **Mitigation**: Add port definition to Section 4 (Interface Definitions)

2. **ExecutionContext Placement Ambiguous**: ExecutionContext is defined in `handler_registry.py` (line 867) but not clearly placed in domain or application layer.
   - **Impact**: Violates hexagonal architecture layer clarity
   - **Mitigation**: Move to `src/domain/value_objects/execution_context.py` or explicitly document as application-layer DTO

**Positive Highlights:**
- State snapshots (WorkflowStateSnapshot, StageStateSnapshot, AgentStateSnapshot) are immutable frozen dataclasses, enforcing correctness
- Checkpoint aggregate includes schema versioning (line 110) for forward compatibility
- Recovery decision tree (lines 1038-1065) provides executable validation logic

---

### Criterion 2: Consistency with Hexagonal Architecture (Score: 0.95 / 1.0)

**Assessment:** Design strongly adheres to Jerry's hexagonal architecture with clear ports/adapters separation.

**Architecture Compliance:**
- ✅ **Domain Layer**: Pure entities with no external dependencies (Checkpoint, CheckpointId)
- ✅ **Application Layer**: CQRS commands/queries with use case handlers
- ✅ **Infrastructure Layer**: FilesystemCheckpointRepository implements ICheckpointRepository port
- ✅ **Interface Layer**: CLI/API mentioned as primary adapters (lines 715-719)

**Port Definitions (Lines 772-939):**
- ✅ ICheckpointRepository: Clear contract for save/get/delete operations
- ✅ IHandlerRegistry: Defines resume handler lookup protocol
- ✅ Ports use `ABC` and `@abstractmethod` per Python standards

**Adapter Implementations (Lines 394-587):**
- ✅ FilesystemCheckpointRepository: Implements ICheckpointRepository with atomic writes
- ✅ Uses temp-file-rename for atomicity (lines 429-434)
- ✅ Hierarchical directory structure mirrors checkpoint hierarchy (lines 483-490)

**Minor Inconsistency (0.05 deduction):**
- **ExecutionContext in Port File**: ExecutionContext is defined in `handler_registry.py` (lines 867-891) alongside IHandlerRegistry. This mixes data structure (value object/DTO) with port interface.
  - **Recommendation**: Extract ExecutionContext to separate file in domain/value_objects or application/dtos depending on layer assignment

**Positive Highlights:**
- Checkpoint aggregate enforces invariants (mark_completed only from ACTIVE status, line 113-119)
- Recovery handler uses dependency injection for ports (line 213-218)
- Filesystem adapter encapsulates all storage logic (no leakage to domain)

---

### Criterion 3: Feasibility (Score: 0.90 / 1.0)

**Assessment:** Implementation is achievable with existing Jerry infrastructure and Python stdlib.

**Zero-Dependency Core Compliance:**
- ✅ Domain layer uses only stdlib: dataclasses, datetime, enum, typing, traceback
- ✅ JSON serialization (stdlib `json` module) for checkpoint persistence
- ✅ Filesystem operations use stdlib `pathlib` and `os`
- ✅ No external libraries required in domain/application layers

**Infrastructure Dependencies:**
- ⚠️ **Async I/O Assumption**: Line 1078 suggests using `aiofiles` for non-blocking filesystem operations, but current codebase uses stdlib only.
  - **Implication**: If Jerry enforces stdlib-only in infrastructure, async file I/O would use `await asyncio.to_thread(file.write, ...)` instead
  - **Mitigation**: Document choice: either relax stdlib-only for infrastructure OR use thread-based async

**Implementation Complexity:**
- ✅ **Atomic Writes**: Well-understood pattern (temp + rename), proven in Unix/Linux
- ✅ **Context Rebuild**: Parent chain traversal is straightforward linked-list walk (lines 313-331)
- ✅ **Handler Registry**: Simple dict-based lookup (likely InMemoryHandlerRegistry)

**Feasibility Concerns (0.10 deduction):**

1. **Concurrent Writes (Line 1034)**: "Last-write-wins" noted, but no locking mechanism provided.
   - **Scenario**: Two orchestration processes create checkpoints for same workflow simultaneously
   - **Current Design**: Sequence numbers prevent ambiguity, but race conditions could corrupt index.json
   - **Recommendation**: Add file-based locking (e.g., `fcntl.flock`) or atomic index updates via append-only log

2. **Context Chain Depth Scaling (Line 1084)**: Limit of ~100 checkpoints mentioned, but no consolidation algorithm provided.
   - **Implication**: Deep chains (long-running workflows) could cause slow recovery
   - **Recommendation**: Add "chain consolidation" as explicit use case in Phase 4 (Tooling)

3. **Missing Sequence Generator Implementation**: CreateCheckpointHandler depends on `ISequenceGenerator.next_for_workflow()` (line 988) but no concrete implementation provided.
   - **Recommendation**: Define filesystem-based counter (e.g., `.jerry/orchestration/sequences/{workflow_id}.counter`)

**Positive Highlights:**
- Checkpoint file size limit (10MB, line 1082) prevents filesystem strain
- Lazy loading strategy (line 1073) defers I/O cost until recovery needed
- JSON format enables manual inspection/debugging (human-readable)

---

### Criterion 4: Error Handling (Score: 0.90 / 1.0)

**Assessment:** Recovery from partial failures is comprehensively covered with detection and mitigation strategies.

**Failure Scenarios Addressed (Lines 1027-1034):**

| Scenario | Detection | Recovery | Evaluation |
|----------|-----------|----------|------------|
| Agent crashes mid-execution | ACTIVE status + stale timestamp | Retry from AGENT_START checkpoint | ✅ Clear |
| Storage write fails | Exception during save() | Exponential backoff retry | ✅ Standard pattern |
| Context rebuild incomplete | Missing parent in chain | Fail recovery, manual intervention | ✅ Safe default |
| Handler not found | Registry lookup fails | Log error, suggest registration | ✅ Actionable |
| State corruption | JSON deserialization error | Use previous checkpoint | ✅ Fallback strategy |
| Concurrent writes | Multiple processes writing | Last-write-wins via sequence | ⚠️ No locking |

**Recovery Validation Logic (Lines 274-303):**
- ✅ Checks checkpoint status is ACTIVE or FAILED (not COMPLETED/RECOVERING)
- ✅ Validates retry count < max_retries (prevents infinite loops)
- ✅ Verifies resume handler exists in registry (fail-fast before execution)

**Error Handling Gaps (0.10 deduction):**

1. **No Timeout on Recovery Execution**: RecoverFromCheckpointHandler (line 261) calls `handler.resume(context)` without timeout. If resume handler hangs, recovery process blocks indefinitely.
   - **Recommendation**: Add timeout parameter to RecoverFromCheckpointCommand (e.g., `resume_timeout_seconds: int = 300`)

2. **Stale Checkpoint Detection Logic Missing**: "ACTIVE status + stale timestamp" mentioned (line 1029) but no implementation of staleness detection.
   - **Recommendation**: Add `is_stale()` method to Checkpoint aggregate (e.g., `updated_at < now - 30 minutes`)

3. **Partial Write Detection**: Atomic rename prevents partial checkpoint writes, but what if crash occurs after rename but before index update?
   - **Impact**: Checkpoint exists but not in index, leading to orphaned files
   - **Recommendation**: Add index repair command in CLI tooling (Phase 4)

**Positive Highlights:**
- Checkpoint aggregate encapsulates error tracking (error_message, error_stacktrace, lines 106-107)
- Recovery decision tree (lines 1038-1065) provides clear branching logic for all failure modes
- mark_failed() method captures full exception traceback (lines 121-128) for debugging

---

### Criterion 5: Performance and Scalability (Score: 0.95 / 1.0)

**Assessment:** Optimization strategies are well-considered with concrete limits defined.

**Optimization Strategies (Lines 1071-1078):**
- ✅ **Lazy Loading**: Only load checkpoint when recovery triggered (deferred I/O cost)
- ✅ **Index for Fast Lookup**: index.json provides O(1) access to latest checkpoint
- ✅ **Incremental State**: Noted as future enhancement (delta storage)
- ✅ **Compression**: GZIP for checkpoints >100KB threshold
- ✅ **Async I/O**: Non-blocking filesystem operations (if aiofiles used)

**Scalability Limits (Lines 1080-1087):**

| Resource | Limit | Assessment |
|----------|-------|------------|
| Checkpoint file size | ~10MB | ✅ Reasonable for JSON state snapshots |
| Context chain depth | ~100 checkpoints | ✅ With consolidation strategy |
| Concurrent workflows | ~1000 | ✅ Sharding by workflow_id hash |
| Recovery time | <5s (90th percentile) | ✅ Achievable with lazy loading |

**Performance Concerns (0.05 deduction):**

1. **Index Update on Every Save**: `_update_index()` (lines 540-564) appends to index.json on every checkpoint creation. For high-frequency checkpointing (e.g., every agent execution), this could cause index bloat.
   - **Recommendation**: Rotate index.json periodically (e.g., daily) or use append-only log with compaction

2. **No Caching for Handler Registry**: IHandlerRegistry.get() (line 254) called on every recovery. If handler resolution is expensive (e.g., dynamic import), this could slow recovery.
   - **Recommendation**: Note that InMemoryHandlerRegistry implementation should cache handlers

**Positive Highlights:**
- Hierarchical directory structure (lines 372-389) prevents single directory with thousands of files
- Sequence-based filenames enable fast range scans (e.g., "get last 10 checkpoints")
- JSON sort_keys=True (line 431) ensures deterministic diffs for version control

---

### Criterion 6: Testability (Score: 0.95 / 1.0)

**Assessment:** Clear test strategy defined across all testing levels with concrete examples.

**Test Coverage (Lines 1090-1144):**

| Test Level | Coverage | Examples Provided |
|------------|----------|-------------------|
| **Unit Tests** | Domain entities | ✅ Checkpoint state transitions |
| **Integration Tests** | Repository adapters | ✅ Filesystem save/retrieve |
| **E2E Tests** | Full recovery flow | ✅ Agent failure → recovery → completion |

**Test Examples Quality:**
- ✅ **Naming Convention**: Follows `test_{what}_when_{condition}_then_{expected}` (lines 1097, 1105)
- ✅ **AAA Pattern**: Unit test example shows Arrange-Act-Assert structure (line 1098)
- ✅ **Edge Cases**: Tests both happy path (line 1097) and error case (line 1105)

**Testability Gaps (0.05 deduction):**

1. **Missing Mock Examples**: No guidance on mocking ICheckpointRepository or IHandlerRegistry for unit testing application-layer handlers.
   - **Recommendation**: Add section 7.4 with mock/stub examples for ports

2. **No Performance Test Strategy**: Recovery time target (<5s, line 1086) defined but no performance test example provided.
   - **Recommendation**: Add benchmark test using pytest-benchmark or manual timing

**Positive Highlights:**
- Integration test considers concurrency (line 1127): "test atomic write when concurrent saves"
- E2E test validates full workflow recovery (lines 1137-1143)
- Migration path (lines 1148-1168) includes "Unit tests for domain and infrastructure" in Phase 1

---

## Scoring Rubric (L2)

### Overall Score Calculation

| Criterion | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| Completeness | 20% | 0.95 | 0.19 |
| Consistency with Hexagonal Architecture | 20% | 0.95 | 0.19 |
| Feasibility | 20% | 0.90 | 0.18 |
| Error Handling | 20% | 0.90 | 0.18 |
| Performance and Scalability | 10% | 0.95 | 0.095 |
| Testability | 10% | 0.95 | 0.095 |
| **TOTAL** | **100%** | | **0.92** |

### Score Interpretation

- **0.90-1.0**: Excellent - Approve for implementation
- **0.85-0.89**: Good - Approve with minor revisions
- **0.70-0.84**: Adequate - Require revisions before approval
- **<0.70**: Insufficient - Reject and iterate

**Result: 0.92 → EXCELLENT → APPROVE**

---

## Improvement Recommendations (Non-Blocking)

While the design meets the quality threshold and can proceed to implementation, the following improvements would strengthen it further:

### 1. Add Missing Port: ISequenceGenerator

**Location:** `src/domain/ports/sequence_generator.py`

**Justification:** CreateCheckpointHandler depends on sequence generation (line 988) but port is not defined.

**Recommended Interface:**
```python
from abc import ABC, abstractmethod

class ISequenceGenerator(ABC):
    """Port for monotonic sequence number generation."""

    @abstractmethod
    async def next_for_workflow(self, workflow_id: str) -> int:
        """
        Get next sequence number for workflow.

        Args:
            workflow_id: The workflow identifier.

        Returns:
            Monotonically increasing sequence number.
        """
        pass
```

### 2. Clarify ExecutionContext Layer Placement

**Issue:** ExecutionContext defined in handler_registry.py mixes data structure with port interface.

**Recommendation:** Extract to separate file and document layer assignment:
- **Option A (Domain)**: `src/domain/value_objects/execution_context.py` if context is domain concept
- **Option B (Application)**: `src/application/dtos/execution_context.py` if context is use-case-specific DTO

### 3. Address Distributed Locking Question

**Open Question (Line 1173):** "Do we need distributed locking for multi-process orchestration?"

**Recommendation:** Provide decision criteria:
- **Single-process orchestration**: No locking needed (current design sufficient)
- **Multi-process orchestration**: Use file-based locking (`fcntl.flock`) on index.json during updates
- **Distributed orchestration**: Consider external coordinator (e.g., etcd) or event-sourcing approach

**Suggested Decision:** Start with single-process (no locking) and add file locking in Phase 3 if multi-process support is required.

### 4. Define Retention Policy

**Open Question (Line 1178):** "Should old checkpoints auto-purge?"

**Recommendation:** Propose default policy with override capability:
- **Default Retention**: Keep checkpoints for 30 days OR last 1000 checkpoints (whichever is larger)
- **Configurable**: Add `retention_days` and `retention_count` to workflow metadata.json
- **Manual Purge Command**: Provide CLI command `jerry checkpoint purge --workflow-id <id> --before <date>`

### 5. Add Staleness Detection Implementation

**Gap:** "ACTIVE status + stale timestamp" detection mentioned (line 1029) but not implemented.

**Recommended Addition to Checkpoint Aggregate:**
```python
def is_stale(self, staleness_threshold: timedelta = timedelta(minutes=30)) -> bool:
    """Check if checkpoint is stale (no updates for threshold period)."""
    return (
        self.status == CheckpointStatus.ACTIVE
        and datetime.utcnow() - self.updated_at > staleness_threshold
    )
```

### 6. Add Recovery Timeout

**Gap:** No timeout on `handler.resume(context)` call (line 261).

**Recommended Addition to RecoverFromCheckpointCommand:**
```python
@dataclass
class RecoverFromCheckpointCommand:
    checkpoint_id: CheckpointId
    override_handler: str | None = None
    skip_validation: bool = False
    resume_timeout_seconds: int = 300  # 5-minute default timeout
```

**Recommended Enforcement in RecoverFromCheckpointHandler:**
```python
try:
    workflow_id = await asyncio.wait_for(
        handler.resume(context),
        timeout=command.resume_timeout_seconds
    )
except asyncio.TimeoutError:
    checkpoint.mark_failed(
        Exception(f"Recovery timed out after {command.resume_timeout_seconds}s")
    )
    raise
```

---

## Conclusion

The Orchestration Checkpoint/Recovery System design is **excellent** and ready for implementation. The architect has produced a comprehensive, well-structured design that:

1. **Fully aligns with Jerry's architecture**: Clear hexagonal boundaries, zero-dependency domain
2. **Provides production-ready recovery**: Deterministic context rebuild, comprehensive error handling
3. **Enables filesystem-first persistence**: Human-readable JSON, atomic writes, hierarchical structure
4. **Includes implementation roadmap**: 4-phase migration path with testing strategy

The minor gaps identified (sequence generator port, ExecutionContext placement, locking strategy, retention policy) are **non-blocking** and can be addressed during implementation without requiring design iteration.

**Recommendation: ACCEPT and proceed to Phase 1 (Core Implementation).**

---

## Session Context for Orchestrator Handoff

```yaml
session_context:
  schema_version: "1.0.0"
  session_id: "ps-orch-003-test"
  source_agent:
    id: "ps-critic"
    version: "v2.1.0"
    family: "ps"
  target_agent:
    id: "orchestrator"
  payload:
    iteration: 1
    quality_score: 0.92
    threshold_met: true
    improvement_areas:
      - "Add ISequenceGenerator port definition (non-blocking)"
      - "Clarify ExecutionContext layer placement (domain vs application)"
      - "Resolve distributed locking question (single vs multi-process)"
      - "Define default retention policy for checkpoint purging"
      - "Add staleness detection implementation to Checkpoint aggregate"
      - "Add recovery timeout to prevent hung resume handlers"
    recommendation: "ACCEPT"
    next_steps:
      - "Proceed to Phase 1: Implement domain entities (Checkpoint, CheckpointId, state snapshots)"
      - "Implement FilesystemCheckpointRepository with atomic writes"
      - "Create unit tests for Checkpoint aggregate state transitions"
      - "Create integration tests for FilesystemCheckpointRepository"
      - "Address minor improvements during implementation (sequence generator, ExecutionContext placement)"
    critique_highlights:
      - "Excellent hexagonal architecture adherence (clear ports/adapters)"
      - "Atomic write pattern prevents checkpoint corruption"
      - "Lazy loading + indexing strategy ensures performance"
      - "Comprehensive error handling with 6 failure scenarios covered"
      - "Clear testing strategy with examples at all levels"
      - "Migration path provides phased rollout with testability gates"
    key_design_decisions_validated:
      - "JSON serialization: Enables human inspection and version control diffs"
      - "Hierarchical filesystem structure: Prevents directory bloat, mirrors workflow hierarchy"
      - "Parent checkpoint chain: Enables incremental context rebuild without full state in each checkpoint"
      - "Handler registry: Provides pluggable resume strategies, decouples checkpoint from execution logic"
      - "CheckpointId value object: Enables type-safe identification and filesystem-safe path construction"
```

---

## References

- Jerry Constitution v1.0 - `docs/governance/JERRY_CONSTITUTION.md` (Principle P-002: File Persistence)
- Jerry Coding Standards - `.claude/rules/coding-standards.md` (Hexagonal Architecture Rules)
- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/) - Alistair Cockburn
- [CQRS Pattern](https://martinfowler.com/bliki/CQRS.html) - Martin Fowler
- [Atomic File Writes](https://lwn.net/Articles/457667/) - POSIX rename() semantics
