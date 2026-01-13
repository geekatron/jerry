# State Checkpointing System for Multi-Agent Orchestration

> **Document ID:** PS-ORCH-006-DESIGN-001
> **Author:** ps-architect v2.1.0
> **Date:** 2026-01-11
> **Status:** Draft for Validation

---

## L0: Executive Summary

A state checkpointing system that enables resilient multi-agent orchestration through persistent snapshots, enabling failure recovery, session resumption, and compliance auditing.

**Key Capabilities:**
- Atomic checkpoint creation with rollback guarantees
- Cross-context session continuity via filesystem persistence
- Immutable audit trail for regulatory compliance
- Sub-second checkpoint/restore operations for minimal workflow disruption

---

## L1: Solution Overview

### Problem Statement

Multi-agent orchestration workflows face three critical challenges:

1. **Failure Recovery**: Agent failures mid-workflow lose accumulated state
2. **Context Exhaustion**: LLM context windows fill, requiring session handoff
3. **Compliance**: Regulated environments require auditable decision trails

### Solution Approach

Implement a **Write-Ahead Logging (WAL)** pattern with **Event Sourcing** to create an append-only checkpoint stream that can reconstruct any workflow state.

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ORCHESTRATION LAYER                                   │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐                │
│  │ Conductor │  │  Worker   │  │  Worker   │  │  Worker   │                │
│  │  (Opus)   │  │ (Sonnet)  │  │ (Sonnet)  │  │ (Sonnet)  │                │
│  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘                │
│        │              │              │              │                       │
│        └──────────────┴──────────────┴──────────────┘                       │
│                              │                                              │
│                              ▼                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                    CHECKPOINT COORDINATOR                              │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐  │ │
│  │  │  Snapshot   │  │   State     │  │   Audit     │  │   Recovery   │  │ │
│  │  │   Manager   │  │  Serializer │  │   Logger    │  │   Engine     │  │ │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬───────┘  │ │
│  │         │                │                │                │          │ │
│  └─────────┴────────────────┴────────────────┴────────────────┴──────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PERSISTENCE LAYER                                    │
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────────┐ │
│  │   Checkpoint    │  │    Event        │  │        Audit                │ │
│  │     Store       │  │    Journal      │  │        Archive              │ │
│  │  (.checkpoint/) │  │  (.events/)     │  │  (.audit/)                  │ │
│  │                 │  │                 │  │                             │ │
│  │  checkpoint_    │  │  events_        │  │  audit_                     │ │
│  │  {seq}.json     │  │  {timestamp}    │  │  {session}                  │ │
│  │                 │  │  .jsonl         │  │  .jsonl                     │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | SLA |
|-----------|---------------|-----|
| Snapshot Manager | Create/restore atomic checkpoints | < 100ms |
| State Serializer | Marshal/unmarshal workflow state | < 50ms |
| Audit Logger | Append compliance events | < 10ms |
| Recovery Engine | Reconstruct state from checkpoints | < 500ms |

---

## L2: Detailed Design

### 1. Component Specifications

#### 1.1 Snapshot Manager

**Purpose:** Coordinates atomic checkpoint creation with crash consistency guarantees.

```
┌──────────────────────────────────────────────────────┐
│                  SNAPSHOT MANAGER                     │
├──────────────────────────────────────────────────────┤
│                                                      │
│  create_checkpoint(workflow_id, state) → CheckpointID│
│  restore_checkpoint(checkpoint_id) → WorkflowState   │
│  list_checkpoints(workflow_id) → List[CheckpointMeta]│
│  prune_checkpoints(retention_policy) → PruneResult   │
│                                                      │
│  Internal:                                           │
│  - checkpoint_sequence: AtomicCounter                │
│  - active_checkpoints: Dict[WorkflowID, Checkpoint]  │
│  - write_lock: ReentrantLock                         │
│                                                      │
└──────────────────────────────────────────────────────┘
```

**Atomicity Protocol:**
1. Write checkpoint to temp file: `checkpoint_{seq}.tmp`
2. Compute SHA-256 checksum
3. fsync() the file
4. Atomic rename to: `checkpoint_{seq}.json`
5. Append to manifest with checksum

#### 1.2 State Serializer

**Purpose:** Transforms workflow state to/from persistent format with schema versioning.

```
┌──────────────────────────────────────────────────────┐
│                  STATE SERIALIZER                     │
├──────────────────────────────────────────────────────┤
│                                                      │
│  serialize(state: WorkflowState) → bytes             │
│  deserialize(data: bytes) → WorkflowState            │
│  migrate(data: bytes, target_version) → bytes        │
│                                                      │
│  Supported Formats:                                  │
│  - JSON (human-readable, default)                    │
│  - MessagePack (compact, performance mode)           │
│  - CBOR (binary, compliance mode)                    │
│                                                      │
└──────────────────────────────────────────────────────┘
```

**Schema Evolution Strategy:**
- Embed schema version in checkpoint header
- Forward-compatible additions (new optional fields)
- Backward-compatible reads (unknown fields ignored)
- Breaking changes require migration transformers

#### 1.3 Audit Logger

**Purpose:** Provides tamper-evident, append-only audit trail for compliance.

```
┌──────────────────────────────────────────────────────┐
│                   AUDIT LOGGER                        │
├──────────────────────────────────────────────────────┤
│                                                      │
│  log_event(event: AuditEvent) → EventID              │
│  query_events(filter: AuditFilter) → List[AuditEvent]│
│  verify_chain(session_id) → VerificationResult       │
│  export_report(session_id, format) → Report          │
│                                                      │
│  Integrity:                                          │
│  - Hash chain linking (prev_hash in each entry)      │
│  - Periodic merkle root checkpoints                  │
│  - Immutable storage (append-only, no updates)       │
│                                                      │
└──────────────────────────────────────────────────────┘
```

#### 1.4 Recovery Engine

**Purpose:** Reconstructs workflow state from checkpoints and replays pending events.

```
┌──────────────────────────────────────────────────────┐
│                  RECOVERY ENGINE                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│  recover_workflow(workflow_id) → RecoveryResult      │
│  resume_session(session_id) → SessionState           │
│  validate_checkpoint(checkpoint_id) → ValidationRes  │
│                                                      │
│  Recovery Modes:                                     │
│  - FULL: Restore from oldest checkpoint, replay all  │
│  - LATEST: Restore from most recent valid checkpoint │
│  - POINT_IN_TIME: Restore to specific checkpoint seq │
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

### 2. Interface Contracts

#### 2.1 Primary Port: ICheckpointService

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from enum import Enum


class RecoveryMode(Enum):
    FULL = "full"
    LATEST = "latest"
    POINT_IN_TIME = "point_in_time"


@dataclass(frozen=True)
class CheckpointID:
    workflow_id: str
    sequence: int
    timestamp: datetime
    checksum: str


@dataclass(frozen=True)
class CheckpointMeta:
    id: CheckpointID
    size_bytes: int
    schema_version: str
    agent_id: str
    created_at: datetime


@dataclass
class WorkflowState:
    workflow_id: str
    session_id: str
    current_step: int
    total_steps: int
    agent_states: dict[str, dict]
    pending_events: list[dict]
    context_summary: str
    metadata: dict


@dataclass
class RecoveryResult:
    success: bool
    state: Optional[WorkflowState]
    checkpoint_used: Optional[CheckpointID]
    events_replayed: int
    recovery_time_ms: float
    warnings: list[str]


class ICheckpointService(ABC):
    """Primary port for checkpoint operations."""

    @abstractmethod
    def create_checkpoint(
        self,
        workflow_id: str,
        state: WorkflowState,
        force: bool = False
    ) -> CheckpointID:
        """Create atomic checkpoint of workflow state.

        Args:
            workflow_id: Unique workflow identifier
            state: Current workflow state to checkpoint
            force: Bypass duplicate detection

        Returns:
            CheckpointID with sequence number and checksum

        Raises:
            CheckpointWriteError: If persistence fails
            CheckpointConflictError: If concurrent write detected
        """
        ...

    @abstractmethod
    def restore_checkpoint(
        self,
        checkpoint_id: CheckpointID
    ) -> WorkflowState:
        """Restore workflow state from checkpoint.

        Args:
            checkpoint_id: Target checkpoint to restore

        Returns:
            Reconstructed WorkflowState

        Raises:
            CheckpointNotFoundError: If checkpoint doesn't exist
            CheckpointCorruptError: If checksum validation fails
            SchemaMigrationError: If schema incompatible
        """
        ...

    @abstractmethod
    def recover_workflow(
        self,
        workflow_id: str,
        mode: RecoveryMode = RecoveryMode.LATEST,
        target_sequence: Optional[int] = None
    ) -> RecoveryResult:
        """Full workflow recovery with event replay.

        Args:
            workflow_id: Workflow to recover
            mode: Recovery strategy
            target_sequence: For POINT_IN_TIME mode

        Returns:
            RecoveryResult with state and diagnostics
        """
        ...

    @abstractmethod
    def list_checkpoints(
        self,
        workflow_id: str,
        limit: int = 100,
        after: Optional[datetime] = None
    ) -> List[CheckpointMeta]:
        """List available checkpoints for workflow."""
        ...

    @abstractmethod
    def prune_checkpoints(
        self,
        workflow_id: str,
        retain_count: int = 10,
        retain_days: int = 30
    ) -> int:
        """Remove old checkpoints per retention policy.

        Returns:
            Number of checkpoints removed
        """
        ...
```

#### 2.2 Secondary Port: ICheckpointRepository

```python
class ICheckpointRepository(ABC):
    """Secondary port for checkpoint persistence."""

    @abstractmethod
    def write(
        self,
        path: str,
        data: bytes,
        checksum: str
    ) -> None:
        """Atomic write with checksum verification."""
        ...

    @abstractmethod
    def read(self, path: str) -> tuple[bytes, str]:
        """Read with checksum. Returns (data, checksum)."""
        ...

    @abstractmethod
    def exists(self, path: str) -> bool:
        """Check if checkpoint exists."""
        ...

    @abstractmethod
    def list_files(
        self,
        prefix: str,
        pattern: str = "*"
    ) -> List[str]:
        """List checkpoint files matching pattern."""
        ...

    @abstractmethod
    def delete(self, path: str) -> bool:
        """Delete checkpoint file."""
        ...

    @abstractmethod
    def atomic_rename(self, src: str, dst: str) -> None:
        """Atomic file rename for crash consistency."""
        ...
```

#### 2.3 Audit Port: IAuditLogger

```python
@dataclass(frozen=True)
class AuditEvent:
    event_id: str
    session_id: str
    workflow_id: str
    event_type: str  # CHECKPOINT_CREATED, STATE_RESTORED, AGENT_DECISION
    agent_id: str
    timestamp: datetime
    payload: dict
    prev_hash: str  # Hash chain linking


class IAuditLogger(ABC):
    """Port for compliance audit logging."""

    @abstractmethod
    def log_event(self, event: AuditEvent) -> str:
        """Append event to audit trail. Returns event_id."""
        ...

    @abstractmethod
    def query_events(
        self,
        session_id: str,
        event_types: Optional[List[str]] = None,
        after: Optional[datetime] = None,
        before: Optional[datetime] = None
    ) -> List[AuditEvent]:
        """Query audit events with filters."""
        ...

    @abstractmethod
    def verify_chain_integrity(
        self,
        session_id: str
    ) -> tuple[bool, Optional[str]]:
        """Verify hash chain. Returns (valid, first_invalid_event_id)."""
        ...
```

---

### 3. Data Model / Schema

#### 3.1 Checkpoint File Format

```json
{
  "$schema": "checkpoint-schema-v1.0.0",
  "header": {
    "version": "1.0.0",
    "checkpoint_id": {
      "workflow_id": "WF-2026-001",
      "sequence": 42,
      "timestamp": "2026-01-11T14:30:00Z",
      "checksum": "sha256:a1b2c3d4..."
    },
    "created_by": {
      "agent_id": "orchestrator",
      "agent_version": "2.1.0",
      "session_id": "ps-orch-006-test"
    },
    "compression": "none",
    "encoding": "utf-8"
  },
  "state": {
    "workflow_id": "WF-2026-001",
    "session_id": "ps-orch-006-test",
    "current_step": 5,
    "total_steps": 12,
    "status": "IN_PROGRESS",
    "started_at": "2026-01-11T14:00:00Z",
    "last_activity": "2026-01-11T14:30:00Z",
    "agent_states": {
      "conductor": {
        "last_decision": "DISPATCH_TO_WORKER",
        "pending_responses": ["worker-1", "worker-2"],
        "context_usage_pct": 45.2
      },
      "worker-1": {
        "task_id": "TASK-001",
        "progress": 0.75,
        "artifacts": ["design-doc.md"]
      }
    },
    "pending_events": [
      {
        "event_type": "TASK_COMPLETED",
        "source": "worker-2",
        "payload": {"task_id": "TASK-002"}
      }
    ],
    "context_summary": "Completed design phase, starting implementation...",
    "metadata": {
      "project_id": "PROJ-002",
      "work_item": "WI-SAO-030",
      "priority": "high"
    }
  },
  "footer": {
    "prev_checkpoint": {
      "sequence": 41,
      "checksum": "sha256:e5f6g7h8..."
    },
    "events_since_prev": 15,
    "size_bytes": 2048
  }
}
```

#### 3.2 Event Journal Format (JSONL)

```jsonl
{"seq":1,"ts":"2026-01-11T14:00:00Z","type":"WORKFLOW_STARTED","wf":"WF-2026-001","data":{}}
{"seq":2,"ts":"2026-01-11T14:01:00Z","type":"AGENT_SPAWNED","wf":"WF-2026-001","agent":"worker-1","data":{}}
{"seq":3,"ts":"2026-01-11T14:05:00Z","type":"CHECKPOINT_CREATED","wf":"WF-2026-001","cp_seq":1,"data":{}}
{"seq":4,"ts":"2026-01-11T14:10:00Z","type":"TASK_ASSIGNED","wf":"WF-2026-001","agent":"worker-1","data":{"task":"TASK-001"}}
```

#### 3.3 Audit Trail Format (JSONL with Hash Chain)

```jsonl
{"id":"AE-001","ts":"2026-01-11T14:00:00Z","type":"SESSION_STARTED","session":"ps-orch-006-test","agent":"orchestrator","prev_hash":"GENESIS","hash":"sha256:abc123"}
{"id":"AE-002","ts":"2026-01-11T14:05:00Z","type":"CHECKPOINT_CREATED","session":"ps-orch-006-test","agent":"orchestrator","prev_hash":"sha256:abc123","hash":"sha256:def456","data":{"cp_seq":1}}
{"id":"AE-003","ts":"2026-01-11T14:10:00Z","type":"AGENT_DECISION","session":"ps-orch-006-test","agent":"ps-architect","prev_hash":"sha256:def456","hash":"sha256:ghi789","data":{"decision":"approve_design","confidence":0.92}}
```

#### 3.4 Directory Structure

```
.jerry/
├── checkpoints/
│   └── {workflow_id}/
│       ├── manifest.json           # Checkpoint index with checksums
│       ├── checkpoint_001.json     # Full checkpoint
│       ├── checkpoint_002.json
│       └── checkpoint_042.json
├── events/
│   └── {workflow_id}/
│       ├── events_2026-01-11.jsonl # Daily event journals
│       └── events_2026-01-12.jsonl
└── audit/
    └── {session_id}/
        ├── audit_trail.jsonl       # Hash-chained audit log
        └── merkle_roots.json       # Periodic merkle checkpoints
```

---

### 4. Error Handling Strategy

#### 4.1 Error Taxonomy

```
CheckpointError (base)
├── CheckpointWriteError
│   ├── DiskFullError
│   ├── PermissionDeniedError
│   └── AtomicRenameFailedError
├── CheckpointReadError
│   ├── CheckpointNotFoundError
│   ├── CheckpointCorruptError
│   └── ChecksumMismatchError
├── CheckpointRecoveryError
│   ├── NoValidCheckpointError
│   ├── EventReplayFailedError
│   └── StateReconstructionError
└── CheckpointSchemaError
    ├── UnsupportedVersionError
    └── MigrationFailedError
```

#### 4.2 Error Recovery Matrix

| Error Type | Recovery Strategy | Fallback |
|------------|-------------------|----------|
| DiskFullError | Prune old checkpoints, retry | Alert, pause workflow |
| ChecksumMismatchError | Try previous checkpoint | Full recovery from oldest |
| EventReplayFailedError | Skip event, log warning | Restore checkpoint only |
| UnsupportedVersionError | Run migration chain | Fail with clear message |
| NoValidCheckpointError | Start fresh workflow | Require user intervention |

#### 4.3 Retry Policy

```python
@dataclass
class RetryPolicy:
    max_attempts: int = 3
    base_delay_ms: int = 100
    max_delay_ms: int = 5000
    exponential_base: float = 2.0
    jitter: bool = True

    retryable_errors: tuple = (
        DiskFullError,  # After pruning
        AtomicRenameFailedError,  # Transient FS issue
    )

    non_retryable_errors: tuple = (
        PermissionDeniedError,
        ChecksumMismatchError,
        UnsupportedVersionError,
    )
```

#### 4.4 Graceful Degradation

```
Normal Operation
      │
      ▼
┌─────────────┐     Checkpoint fails     ┌─────────────┐
│  Full       │ ─────────────────────────▶│  Event-Only │
│ Checkpoints │                           │   Mode      │
└─────────────┘                           └─────────────┘
      │                                         │
      │     Event logging fails                 │
      ▼                                         ▼
┌─────────────┐                           ┌─────────────┐
│  Memory-    │◀──────────────────────────│  In-Memory  │
│  Only Mode  │                           │  Events     │
└─────────────┘                           └─────────────┘
      │
      │     Memory pressure
      ▼
┌─────────────┐
│  Emergency  │  → Alert user, save what we can
│  Shutdown   │
└─────────────┘
```

---

### 5. Validation Criteria for Next Phase

The following criteria MUST be validated by `ps-validator` in step 2:

1. **Atomicity**: Checkpoint write protocol provides crash consistency
2. **Recoverability**: Any valid checkpoint can restore workflow state
3. **Integrity**: Hash chain provides tamper detection
4. **Performance**: Checkpoint/restore within SLA bounds
5. **Compatibility**: Schema versioning enables forward/backward compat
6. **Compliance**: Audit trail meets regulatory requirements (SOC2, GDPR)

---

## References

- [Write-Ahead Logging](https://www.sqlite.org/wal.html) - SQLite documentation
- [Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html) - Martin Fowler
- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/) - Alistair Cockburn
- [Jerry Constitution](../../docs/governance/JERRY_CONSTITUTION.md) - P-002 File Persistence

---

```yaml
session_context:
  schema_version: "1.0.0"
  session_id: "ps-orch-006-test"
  source_agent:
    id: "ps-architect"
    version: "2.1.0"
  target_agent:
    id: "ps-validator"
  payload:
    design_components:
      - name: "SnapshotManager"
        responsibility: "Atomic checkpoint creation/restoration"
        sla_ms: 100
      - name: "StateSerializer"
        responsibility: "State marshalling with schema versioning"
        sla_ms: 50
      - name: "AuditLogger"
        responsibility: "Tamper-evident compliance trail"
        sla_ms: 10
      - name: "RecoveryEngine"
        responsibility: "Workflow state reconstruction"
        sla_ms: 500
    interfaces:
      - name: "ICheckpointService"
        type: "primary_port"
        operations:
          - "create_checkpoint"
          - "restore_checkpoint"
          - "recover_workflow"
          - "list_checkpoints"
          - "prune_checkpoints"
      - name: "ICheckpointRepository"
        type: "secondary_port"
        operations:
          - "write"
          - "read"
          - "exists"
          - "list_files"
          - "delete"
          - "atomic_rename"
      - name: "IAuditLogger"
        type: "secondary_port"
        operations:
          - "log_event"
          - "query_events"
          - "verify_chain_integrity"
    validation_criteria:
      - id: "VC-001"
        name: "Atomicity"
        description: "Checkpoint write protocol provides crash consistency"
        test_approach: "Simulate crash during write, verify no partial checkpoints"
      - id: "VC-002"
        name: "Recoverability"
        description: "Any valid checkpoint can restore workflow state"
        test_approach: "Round-trip test: create checkpoint, restore, verify equality"
      - id: "VC-003"
        name: "Integrity"
        description: "Hash chain provides tamper detection"
        test_approach: "Modify audit entry, verify chain validation fails"
      - id: "VC-004"
        name: "Performance"
        description: "Checkpoint/restore within SLA bounds"
        test_approach: "Benchmark with representative state sizes"
      - id: "VC-005"
        name: "Compatibility"
        description: "Schema versioning enables migration"
        test_approach: "Create v1 checkpoint, migrate to v2, verify data"
      - id: "VC-006"
        name: "Compliance"
        description: "Audit trail meets SOC2/GDPR requirements"
        test_approach: "Verify immutability, completeness, queryability"
    data_models:
      - "CheckpointFile"
      - "EventJournal"
      - "AuditTrail"
    error_taxonomy:
      root: "CheckpointError"
      categories:
        - "CheckpointWriteError"
        - "CheckpointReadError"
        - "CheckpointRecoveryError"
        - "CheckpointSchemaError"
```
