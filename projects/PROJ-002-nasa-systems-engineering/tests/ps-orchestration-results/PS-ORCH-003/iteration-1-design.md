# PS-ORCH-003: Orchestration Checkpoint/Recovery System Design

**Document ID:** PS-ORCH-003-E001-I1
**Date:** 2026-01-11
**Author:** ps-architect (v2.1.0)
**Iteration:** 1 of 3
**Status:** Generator Output (Awaiting Critique)

---

## Executive Summary (L0)

This design proposes a **filesystem-first checkpoint/recovery system** for multi-agent orchestration workflows that enables:

1. **Granular state persistence** at workflow, stage, and agent execution levels
2. **Deterministic recovery** from any checkpoint with full context restoration
3. **Zero-dependency core** using only Python stdlib and JSON serialization
4. **Hexagonal architecture** compliance with clear ports and adapters

**Key Design Decisions:**
- Checkpoint format: JSON with versioned schema
- Storage: Filesystem hierarchy mirroring workflow structure
- Recovery strategy: Lazy loading with incremental context rebuild
- Atomicity: Write-to-temp + atomic rename pattern

---

## Detailed Design (L1)

### 1. Checkpoint Data Model

#### 1.1 Core Entities

```python
# src/domain/aggregates/checkpoint.py

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

class CheckpointType(Enum):
    """Types of checkpoints in orchestration."""
    WORKFLOW_START = "workflow_start"
    STAGE_COMPLETE = "stage_complete"
    AGENT_START = "agent_start"
    AGENT_COMPLETE = "agent_complete"
    SYNC_BARRIER = "sync_barrier"
    ERROR_STATE = "error_state"
    WORKFLOW_COMPLETE = "workflow_complete"

class CheckpointStatus(Enum):
    """Status of checkpoint execution."""
    ACTIVE = "active"          # Currently executing
    COMPLETED = "completed"    # Successfully finished
    FAILED = "failed"         # Execution failed
    RECOVERING = "recovering" # In recovery process

@dataclass(frozen=True)
class CheckpointId:
    """Value object for checkpoint identification."""
    workflow_id: str
    stage_id: str | None
    agent_id: str | None
    sequence: int  # Monotonic counter

    def to_path_segment(self) -> str:
        """Convert to filesystem-safe path segment."""
        parts = [self.workflow_id]
        if self.stage_id:
            parts.append(self.stage_id)
        if self.agent_id:
            parts.append(self.agent_id)
        parts.append(f"seq-{self.sequence:05d}")
        return "/".join(parts)

@dataclass
class Checkpoint:
    """
    Aggregate root for orchestration checkpoint state.

    Represents a point-in-time snapshot of workflow execution state
    that can be used to resume from interruption.
    """
    id: CheckpointId
    checkpoint_type: CheckpointType
    status: CheckpointStatus
    created_at: datetime
    updated_at: datetime

    # Execution context
    workflow_state: dict[str, Any]  # Workflow-level variables
    stage_state: dict[str, Any]     # Current stage state
    agent_state: dict[str, Any]     # Current agent state

    # Lineage and dependencies
    parent_checkpoint_id: CheckpointId | None
    dependent_checkpoint_ids: list[CheckpointId] = field(default_factory=list)

    # Metadata for recovery
    resume_handler: str  # Fully qualified function name
    retry_count: int = 0
    max_retries: int = 3

    # Error tracking
    error_message: str | None = None
    error_stacktrace: str | None = None

    # Schema versioning
    schema_version: str = "1.0.0"

    def mark_completed(self) -> None:
        """Transition checkpoint to completed status."""
        if self.status != CheckpointStatus.ACTIVE:
            raise InvalidStateError(
                f"Cannot complete checkpoint in {self.status} status"
            )
        self.status = CheckpointStatus.COMPLETED
        self.updated_at = datetime.utcnow()

    def mark_failed(self, error: Exception) -> None:
        """Record failure state with error details."""
        self.status = CheckpointStatus.FAILED
        self.error_message = str(error)
        self.error_stacktrace = "".join(
            traceback.format_exception(type(error), error, error.__traceback__)
        )
        self.updated_at = datetime.utcnow()

    def can_retry(self) -> bool:
        """Check if checkpoint can be retried."""
        return (
            self.status == CheckpointStatus.FAILED
            and self.retry_count < self.max_retries
        )
```

#### 1.2 State Snapshots

```python
# src/domain/value_objects/state_snapshot.py

@dataclass(frozen=True)
class WorkflowStateSnapshot:
    """Immutable snapshot of workflow-level state."""
    workflow_id: str
    workflow_name: str
    active_stage_id: str | None
    completed_stage_ids: list[str]
    pending_stage_ids: list[str]
    global_context: dict[str, Any]  # Shared variables across stages

@dataclass(frozen=True)
class StageStateSnapshot:
    """Immutable snapshot of stage-level state."""
    stage_id: str
    stage_name: str
    stage_type: str  # sequential, parallel, barrier
    active_agent_ids: list[str]
    completed_agent_ids: list[str]
    stage_context: dict[str, Any]  # Stage-scoped variables

@dataclass(frozen=True)
class AgentStateSnapshot:
    """Immutable snapshot of agent execution state."""
    agent_id: str
    agent_name: str
    agent_family: str  # ps, nse, sao
    input_payload: dict[str, Any]
    output_payload: dict[str, Any] | None
    execution_start: datetime | None
    execution_end: datetime | None
```

### 2. Recovery Mechanism

#### 2.1 Recovery Strategy

```python
# src/application/use_cases/orchestration/recover_from_checkpoint.py

from dataclasses import dataclass
from src.domain.aggregates.checkpoint import Checkpoint, CheckpointId
from src.domain.ports.checkpoint_repository import ICheckpointRepository

@dataclass
class RecoverFromCheckpointCommand:
    """Command to resume workflow from checkpoint."""
    checkpoint_id: CheckpointId
    override_handler: str | None = None  # For testing/debugging
    skip_validation: bool = False

@dataclass
class RecoveryResult:
    """Result of recovery operation."""
    success: bool
    recovered_checkpoint: Checkpoint
    resumed_workflow_id: str
    validation_errors: list[str] = field(default_factory=list)

class RecoverFromCheckpointHandler:
    """
    Use case handler for checkpoint recovery.

    Implements lazy loading strategy:
    1. Load checkpoint from storage
    2. Validate checkpoint state is recoverable
    3. Rebuild execution context incrementally
    4. Resume workflow at designated handler
    """

    def __init__(
        self,
        checkpoint_repo: ICheckpointRepository,
        handler_registry: IHandlerRegistry,
    ):
        self._checkpoint_repo = checkpoint_repo
        self._handler_registry = handler_registry

    async def handle(
        self,
        command: RecoverFromCheckpointCommand
    ) -> RecoveryResult:
        """Execute recovery from checkpoint."""

        # Phase 1: Load checkpoint
        checkpoint = await self._checkpoint_repo.get_by_id(
            command.checkpoint_id
        )
        if checkpoint is None:
            raise CheckpointNotFoundError(
                f"Checkpoint {command.checkpoint_id} not found"
            )

        # Phase 2: Validate recoverability
        if not command.skip_validation:
            validation_errors = self._validate_checkpoint(checkpoint)
            if validation_errors:
                return RecoveryResult(
                    success=False,
                    recovered_checkpoint=checkpoint,
                    resumed_workflow_id="",
                    validation_errors=validation_errors
                )

        # Phase 3: Rebuild context chain
        context = await self._rebuild_context(checkpoint)

        # Phase 4: Resolve resume handler
        handler_name = (
            command.override_handler
            or checkpoint.resume_handler
        )
        handler = self._handler_registry.get(handler_name)

        # Phase 5: Resume execution
        checkpoint.status = CheckpointStatus.RECOVERING
        await self._checkpoint_repo.update(checkpoint)

        try:
            workflow_id = await handler.resume(context)
            checkpoint.mark_completed()
            return RecoveryResult(
                success=True,
                recovered_checkpoint=checkpoint,
                resumed_workflow_id=workflow_id
            )
        except Exception as e:
            checkpoint.mark_failed(e)
            raise
        finally:
            await self._checkpoint_repo.update(checkpoint)

    def _validate_checkpoint(
        self,
        checkpoint: Checkpoint
    ) -> list[str]:
        """Validate checkpoint can be recovered."""
        errors = []

        # Check status is valid for recovery
        if checkpoint.status not in [
            CheckpointStatus.ACTIVE,
            CheckpointStatus.FAILED
        ]:
            errors.append(
                f"Cannot recover from {checkpoint.status} checkpoint"
            )

        # Check retry limits
        if not checkpoint.can_retry():
            errors.append(
                f"Checkpoint exceeded max retries "
                f"({checkpoint.retry_count}/{checkpoint.max_retries})"
            )

        # Check handler exists
        if not self._handler_registry.has(checkpoint.resume_handler):
            errors.append(
                f"Resume handler '{checkpoint.resume_handler}' not found"
            )

        return errors

    async def _rebuild_context(
        self,
        checkpoint: Checkpoint
    ) -> ExecutionContext:
        """Incrementally rebuild execution context from checkpoint chain."""

        # Walk parent chain to root
        chain = []
        current = checkpoint
        while current is not None:
            chain.append(current)
            if current.parent_checkpoint_id:
                current = await self._checkpoint_repo.get_by_id(
                    current.parent_checkpoint_id
                )
            else:
                current = None

        # Replay state changes from root to target
        chain.reverse()
        context = ExecutionContext()
        for cp in chain:
            context.apply_workflow_state(cp.workflow_state)
            context.apply_stage_state(cp.stage_state)
            context.apply_agent_state(cp.agent_state)

        return context
```

#### 2.2 Handler Registry

```python
# src/domain/ports/handler_registry.py

from abc import ABC, abstractmethod
from typing import Callable, Awaitable

class IHandlerRegistry(ABC):
    """Port for looking up resume handlers by name."""

    @abstractmethod
    def register(
        self,
        name: str,
        handler: Callable[[ExecutionContext], Awaitable[str]]
    ) -> None:
        """Register a resume handler."""
        pass

    @abstractmethod
    def get(
        self,
        name: str
    ) -> Callable[[ExecutionContext], Awaitable[str]]:
        """Retrieve handler by fully qualified name."""
        pass

    @abstractmethod
    def has(self, name: str) -> bool:
        """Check if handler exists."""
        pass
```

### 3. Integration with Jerry's Filesystem-First Approach

#### 3.1 Storage Structure

```
projects/{PROJECT_ID}/.jerry/orchestration/
├── checkpoints/
│   ├── {workflow_id}/
│   │   ├── metadata.json          # Workflow-level metadata
│   │   ├── seq-00001.json         # Checkpoint: workflow start
│   │   ├── {stage_id}/
│   │   │   ├── seq-00002.json     # Checkpoint: stage start
│   │   │   ├── {agent_id}/
│   │   │   │   ├── seq-00003.json # Checkpoint: agent start
│   │   │   │   └── seq-00004.json # Checkpoint: agent complete
│   │   │   └── seq-00005.json     # Checkpoint: stage complete
│   │   └── seq-00006.json         # Checkpoint: workflow complete
│   └── index.json                 # Fast lookup index
└── recovery/
    ├── latest.json                # Points to most recent checkpoint
    └── failures.json              # Failed checkpoint audit log
```

#### 3.2 Filesystem Adapter

```python
# src/infrastructure/adapters/checkpoint_repository_fs.py

import json
import os
from pathlib import Path
from typing import Optional
from src.domain.aggregates.checkpoint import Checkpoint, CheckpointId
from src.domain.ports.checkpoint_repository import ICheckpointRepository

class FilesystemCheckpointRepository(ICheckpointRepository):
    """
    Filesystem-based checkpoint storage adapter.

    Implements atomic writes via temp file + rename pattern.
    Uses JSON for human-readable, diffable checkpoints.
    """

    def __init__(self, base_path: Path):
        self._base_path = base_path
        self._checkpoints_dir = base_path / "checkpoints"
        self._recovery_dir = base_path / "recovery"
        self._ensure_directories()

    async def save(self, checkpoint: Checkpoint) -> None:
        """Atomically save checkpoint to filesystem."""

        # Build checkpoint file path
        checkpoint_dir = self._get_checkpoint_dir(checkpoint.id)
        checkpoint_dir.mkdir(parents=True, exist_ok=True)
        checkpoint_file = checkpoint_dir / f"seq-{checkpoint.id.sequence:05d}.json"

        # Serialize to JSON
        checkpoint_data = self._serialize(checkpoint)

        # Write to temp file
        temp_file = checkpoint_file.with_suffix(".tmp")
        with temp_file.open("w") as f:
            json.dump(checkpoint_data, f, indent=2, sort_keys=True)

        # Atomic rename
        temp_file.replace(checkpoint_file)

        # Update index
        await self._update_index(checkpoint)

        # Update latest pointer
        await self._update_latest(checkpoint)

    async def get_by_id(
        self,
        checkpoint_id: CheckpointId
    ) -> Optional[Checkpoint]:
        """Load checkpoint by ID."""

        checkpoint_dir = self._get_checkpoint_dir(checkpoint_id)
        checkpoint_file = (
            checkpoint_dir / f"seq-{checkpoint_id.sequence:05d}.json"
        )

        if not checkpoint_file.exists():
            return None

        with checkpoint_file.open("r") as f:
            data = json.load(f)

        return self._deserialize(data)

    async def get_latest(self, workflow_id: str) -> Optional[Checkpoint]:
        """Get most recent checkpoint for workflow."""

        latest_file = self._recovery_dir / "latest.json"
        if not latest_file.exists():
            return None

        with latest_file.open("r") as f:
            data = json.load(f)

        if data.get("workflow_id") != workflow_id:
            return None

        checkpoint_id = CheckpointId(
            workflow_id=data["workflow_id"],
            stage_id=data.get("stage_id"),
            agent_id=data.get("agent_id"),
            sequence=data["sequence"]
        )

        return await self.get_by_id(checkpoint_id)

    def _get_checkpoint_dir(self, checkpoint_id: CheckpointId) -> Path:
        """Build directory path for checkpoint."""
        path = self._checkpoints_dir / checkpoint_id.workflow_id
        if checkpoint_id.stage_id:
            path = path / checkpoint_id.stage_id
        if checkpoint_id.agent_id:
            path = path / checkpoint_id.agent_id
        return path

    def _serialize(self, checkpoint: Checkpoint) -> dict:
        """Convert checkpoint to JSON-serializable dict."""
        return {
            "schema_version": checkpoint.schema_version,
            "id": {
                "workflow_id": checkpoint.id.workflow_id,
                "stage_id": checkpoint.id.stage_id,
                "agent_id": checkpoint.id.agent_id,
                "sequence": checkpoint.id.sequence,
            },
            "checkpoint_type": checkpoint.checkpoint_type.value,
            "status": checkpoint.status.value,
            "created_at": checkpoint.created_at.isoformat(),
            "updated_at": checkpoint.updated_at.isoformat(),
            "workflow_state": checkpoint.workflow_state,
            "stage_state": checkpoint.stage_state,
            "agent_state": checkpoint.agent_state,
            "parent_checkpoint_id": (
                {
                    "workflow_id": checkpoint.parent_checkpoint_id.workflow_id,
                    "stage_id": checkpoint.parent_checkpoint_id.stage_id,
                    "agent_id": checkpoint.parent_checkpoint_id.agent_id,
                    "sequence": checkpoint.parent_checkpoint_id.sequence,
                }
                if checkpoint.parent_checkpoint_id
                else None
            ),
            "dependent_checkpoint_ids": [
                {
                    "workflow_id": cid.workflow_id,
                    "stage_id": cid.stage_id,
                    "agent_id": cid.agent_id,
                    "sequence": cid.sequence,
                }
                for cid in checkpoint.dependent_checkpoint_ids
            ],
            "resume_handler": checkpoint.resume_handler,
            "retry_count": checkpoint.retry_count,
            "max_retries": checkpoint.max_retries,
            "error_message": checkpoint.error_message,
            "error_stacktrace": checkpoint.error_stacktrace,
        }

    def _deserialize(self, data: dict) -> Checkpoint:
        """Convert JSON dict to Checkpoint aggregate."""
        # Implementation details omitted for brevity
        pass

    async def _update_index(self, checkpoint: Checkpoint) -> None:
        """Update fast lookup index."""
        index_file = self._checkpoints_dir / "index.json"

        # Load existing index
        if index_file.exists():
            with index_file.open("r") as f:
                index = json.load(f)
        else:
            index = {"checkpoints": []}

        # Add/update entry
        entry = {
            "checkpoint_id": checkpoint.id.to_path_segment(),
            "checkpoint_type": checkpoint.checkpoint_type.value,
            "status": checkpoint.status.value,
            "created_at": checkpoint.created_at.isoformat(),
        }
        index["checkpoints"].append(entry)

        # Atomic write
        temp_file = index_file.with_suffix(".tmp")
        with temp_file.open("w") as f:
            json.dump(index, f, indent=2)
        temp_file.replace(index_file)

    async def _update_latest(self, checkpoint: Checkpoint) -> None:
        """Update pointer to latest checkpoint."""
        latest_file = self._recovery_dir / "latest.json"

        data = {
            "workflow_id": checkpoint.id.workflow_id,
            "stage_id": checkpoint.id.stage_id,
            "agent_id": checkpoint.id.agent_id,
            "sequence": checkpoint.id.sequence,
            "updated_at": checkpoint.updated_at.isoformat(),
        }

        temp_file = latest_file.with_suffix(".tmp")
        with temp_file.open("w") as f:
            json.dump(data, f, indent=2)
        temp_file.replace(latest_file)

    def _ensure_directories(self) -> None:
        """Create directory structure if not exists."""
        self._checkpoints_dir.mkdir(parents=True, exist_ok=True)
        self._recovery_dir.mkdir(parents=True, exist_ok=True)
```

---

## Architecture Diagrams (L2)

### 3.1 Checkpoint Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    Orchestration Workflow                        │
│                                                                   │
│  ┌──────────┐      ┌──────────┐      ┌──────────┐              │
│  │ Stage 1  │─────▶│ Stage 2  │─────▶│ Stage 3  │              │
│  └──────────┘      └──────────┘      └──────────┘              │
│       │                  │                  │                    │
│       │                  │                  │                    │
│       ▼                  ▼                  ▼                    │
│  ┌─────────────────────────────────────────────────┐            │
│  │          Checkpoint Creation Events              │            │
│  └─────────────────────────────────────────────────┘            │
│       │                  │                  │                    │
└───────┼──────────────────┼──────────────────┼────────────────────┘
        │                  │                  │
        │                  │                  │
        ▼                  ▼                  ▼
┌────────────────────────────────────────────────────────┐
│          Application Layer: Use Case Handlers           │
│  ┌──────────────────────────────────────────────────┐  │
│  │  CreateCheckpointHandler                         │  │
│  │  - Capture workflow/stage/agent state           │  │
│  │  - Create Checkpoint aggregate                  │  │
│  │  - Persist via ICheckpointRepository port       │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────┘
        │
        ▼
┌────────────────────────────────────────────────────────┐
│       Domain Layer: Checkpoint Aggregate                │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Checkpoint                                      │  │
│  │  + id: CheckpointId                             │  │
│  │  + workflow_state: dict                         │  │
│  │  + stage_state: dict                            │  │
│  │  + agent_state: dict                            │  │
│  │  + mark_completed()                             │  │
│  │  + mark_failed()                                │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────┘
        │
        ▼
┌────────────────────────────────────────────────────────┐
│     Infrastructure: Filesystem Adapter                  │
│  ┌──────────────────────────────────────────────────┐  │
│  │  FilesystemCheckpointRepository                  │  │
│  │  - JSON serialization                           │  │
│  │  - Atomic writes (temp + rename)                │  │
│  │  - Hierarchical directory structure             │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────┘
        │
        ▼
┌────────────────────────────────────────────────────────┐
│              Filesystem Storage                         │
│  projects/{PROJECT_ID}/.jerry/orchestration/            │
│    checkpoints/{workflow_id}/{stage_id}/{agent_id}/    │
│      seq-NNNNN.json                                    │
└────────────────────────────────────────────────────────┘
```

### 3.2 Recovery Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    Recovery Trigger                              │
│  (User command, automatic retry, failure detection)             │
└─────────────────────────────────────────────────────────────────┘
        │
        ▼
┌────────────────────────────────────────────────────────┐
│   Application Layer: RecoverFromCheckpointHandler       │
│                                                          │
│   Phase 1: Load Checkpoint                              │
│   ┌──────────────────────────────────────────────────┐ │
│   │  ICheckpointRepository.get_by_id()               │ │
│   └──────────────────────────────────────────────────┘ │
│                      │                                  │
│                      ▼                                  │
│   Phase 2: Validate Recoverability                      │
│   ┌──────────────────────────────────────────────────┐ │
│   │  - Check status (ACTIVE/FAILED)                  │ │
│   │  - Check retry count < max_retries               │ │
│   │  - Verify resume handler exists                  │ │
│   └──────────────────────────────────────────────────┘ │
│                      │                                  │
│                      ▼                                  │
│   Phase 3: Rebuild Context Chain                        │
│   ┌──────────────────────────────────────────────────┐ │
│   │  Walk parent_checkpoint_id chain to root         │ │
│   │  Replay state changes incrementally              │ │
│   │  Build ExecutionContext with full history        │ │
│   └──────────────────────────────────────────────────┘ │
│                      │                                  │
│                      ▼                                  │
│   Phase 4: Resolve Resume Handler                       │
│   ┌──────────────────────────────────────────────────┐ │
│   │  IHandlerRegistry.get(resume_handler)            │ │
│   └──────────────────────────────────────────────────┘ │
│                      │                                  │
│                      ▼                                  │
│   Phase 5: Resume Execution                             │
│   ┌──────────────────────────────────────────────────┐ │
│   │  handler.resume(ExecutionContext)                │ │
│   │  Mark checkpoint COMPLETED or FAILED             │ │
│   └──────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────┘
        │
        ▼
┌────────────────────────────────────────────────────────┐
│         Workflow Resumes at Checkpoint Point            │
└────────────────────────────────────────────────────────┘
```

### 3.3 Hexagonal Architecture View

```
┌─────────────────────────────────────────────────────────────────┐
│                         Interface Layer                          │
│  ┌───────────────────┐         ┌───────────────────────────┐   │
│  │  CLI Commands     │         │  Recovery HTTP API         │   │
│  │  - checkpoint     │         │  POST /recover             │   │
│  │  - recover        │         │  GET /checkpoints          │   │
│  └───────────────────┘         └───────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                │                              │
                ▼                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Application Layer (CQRS)                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Commands                   │  Queries                    │  │
│  │  - CreateCheckpointCommand  │  - GetCheckpointQuery       │  │
│  │  - RecoverFromCheckpoint    │  - ListCheckpointsQuery     │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                │                              │
                ▼                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Domain Layer                             │
│  ┌──────────────────────┐    ┌────────────────────────────┐    │
│  │  Aggregates          │    │  Value Objects              │    │
│  │  - Checkpoint        │    │  - CheckpointId             │    │
│  │                      │    │  - StateSnapshot            │    │
│  └──────────────────────┘    └────────────────────────────┘    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Ports (Interfaces - NO IMPLEMENTATIONS)                 │  │
│  │  - ICheckpointRepository                                 │  │
│  │  - IHandlerRegistry                                      │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                │                              │
                ▼                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Infrastructure Layer                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Adapters (Secondary - Outbound)                         │  │
│  │  - FilesystemCheckpointRepository                        │  │
│  │  - InMemoryHandlerRegistry                               │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────────┐
│                  External Systems                                │
│  - Filesystem (JSON files)                                       │
│  - Environment variables (config)                                │
└─────────────────────────────────────────────────────────────────┘
```

---

## Interface Definitions

### 4.1 Repository Port

```python
# src/domain/ports/checkpoint_repository.py

from abc import ABC, abstractmethod
from typing import Optional
from src.domain.aggregates.checkpoint import Checkpoint, CheckpointId

class ICheckpointRepository(ABC):
    """
    Port for checkpoint persistence.

    Secondary port (outbound) - implemented by infrastructure layer.
    """

    @abstractmethod
    async def save(self, checkpoint: Checkpoint) -> None:
        """
        Persist checkpoint to storage.

        Args:
            checkpoint: The checkpoint aggregate to save.

        Raises:
            CheckpointStorageError: If persistence fails.
        """
        pass

    @abstractmethod
    async def get_by_id(
        self,
        checkpoint_id: CheckpointId
    ) -> Optional[Checkpoint]:
        """
        Retrieve checkpoint by ID.

        Args:
            checkpoint_id: The unique identifier of the checkpoint.

        Returns:
            The checkpoint if found, None otherwise.
        """
        pass

    @abstractmethod
    async def get_latest(self, workflow_id: str) -> Optional[Checkpoint]:
        """
        Get most recent checkpoint for a workflow.

        Args:
            workflow_id: The workflow identifier.

        Returns:
            The latest checkpoint for the workflow, or None if no checkpoints exist.
        """
        pass

    @abstractmethod
    async def list_by_workflow(
        self,
        workflow_id: str,
        limit: int = 100
    ) -> list[Checkpoint]:
        """
        List all checkpoints for a workflow.

        Args:
            workflow_id: The workflow identifier.
            limit: Maximum number of checkpoints to return.

        Returns:
            List of checkpoints ordered by sequence (newest first).
        """
        pass

    @abstractmethod
    async def delete(self, checkpoint_id: CheckpointId) -> bool:
        """
        Delete a checkpoint.

        Args:
            checkpoint_id: The checkpoint to delete.

        Returns:
            True if deleted, False if not found.
        """
        pass
```

### 4.2 Handler Registry Port

```python
# src/domain/ports/handler_registry.py

from abc import ABC, abstractmethod
from typing import Callable, Awaitable

class ExecutionContext:
    """
    Execution context rebuilt from checkpoint chain.

    Contains full state history needed to resume workflow execution.
    """

    def __init__(self):
        self.workflow_state: dict = {}
        self.stage_state: dict = {}
        self.agent_state: dict = {}
        self.checkpoint_chain: list[Checkpoint] = []

    def apply_workflow_state(self, state: dict) -> None:
        """Merge workflow state update."""
        self.workflow_state.update(state)

    def apply_stage_state(self, state: dict) -> None:
        """Merge stage state update."""
        self.stage_state.update(state)

    def apply_agent_state(self, state: dict) -> None:
        """Merge agent state update."""
        self.agent_state.update(state)

ResumeHandler = Callable[[ExecutionContext], Awaitable[str]]

class IHandlerRegistry(ABC):
    """
    Port for resume handler lookup.

    Maps fully qualified handler names to resumable functions.
    """

    @abstractmethod
    def register(self, name: str, handler: ResumeHandler) -> None:
        """
        Register a resume handler.

        Args:
            name: Fully qualified handler name
                  (e.g., "src.orchestration.handlers.resume_after_agent")
            handler: Async function that accepts ExecutionContext and returns
                     workflow_id
        """
        pass

    @abstractmethod
    def get(self, name: str) -> ResumeHandler:
        """
        Retrieve handler by name.

        Args:
            name: Fully qualified handler name.

        Returns:
            The resume handler function.

        Raises:
            HandlerNotFoundError: If handler not registered.
        """
        pass

    @abstractmethod
    def has(self, name: str) -> bool:
        """Check if handler exists."""
        pass

    @abstractmethod
    def list_handlers(self) -> list[str]:
        """List all registered handler names."""
        pass
```

### 4.3 Use Case Commands

```python
# src/application/use_cases/orchestration/create_checkpoint.py

from dataclasses import dataclass
from datetime import datetime
from src.domain.aggregates.checkpoint import (
    Checkpoint,
    CheckpointId,
    CheckpointType,
    CheckpointStatus
)
from src.domain.ports.checkpoint_repository import ICheckpointRepository

@dataclass
class CreateCheckpointCommand:
    """Command to create a new checkpoint."""
    workflow_id: str
    stage_id: str | None
    agent_id: str | None
    checkpoint_type: CheckpointType
    workflow_state: dict
    stage_state: dict
    agent_state: dict
    resume_handler: str
    parent_checkpoint_id: CheckpointId | None = None
    max_retries: int = 3

class CreateCheckpointHandler:
    """Handler for checkpoint creation."""

    def __init__(
        self,
        checkpoint_repo: ICheckpointRepository,
        sequence_generator: ISequenceGenerator
    ):
        self._checkpoint_repo = checkpoint_repo
        self._sequence_gen = sequence_generator

    async def handle(
        self,
        command: CreateCheckpointCommand
    ) -> Checkpoint:
        """Create and persist a new checkpoint."""

        # Generate monotonic sequence number
        sequence = await self._sequence_gen.next_for_workflow(
            command.workflow_id
        )

        # Create checkpoint ID
        checkpoint_id = CheckpointId(
            workflow_id=command.workflow_id,
            stage_id=command.stage_id,
            agent_id=command.agent_id,
            sequence=sequence
        )

        # Create checkpoint aggregate
        checkpoint = Checkpoint(
            id=checkpoint_id,
            checkpoint_type=command.checkpoint_type,
            status=CheckpointStatus.ACTIVE,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            workflow_state=command.workflow_state,
            stage_state=command.stage_state,
            agent_state=command.agent_state,
            parent_checkpoint_id=command.parent_checkpoint_id,
            resume_handler=command.resume_handler,
            max_retries=command.max_retries
        )

        # Persist
        await self._checkpoint_repo.save(checkpoint)

        return checkpoint
```

---

## Error Handling and Edge Cases

### 5.1 Partial Failure Scenarios

| Scenario | Detection | Recovery Strategy |
|----------|-----------|-------------------|
| **Agent crashes mid-execution** | Checkpoint in ACTIVE status with stale timestamp | Retry from last AGENT_START checkpoint |
| **Storage write fails** | Exception during `save()` | Retry with exponential backoff |
| **Context rebuild incomplete** | Missing parent checkpoint in chain | Fail recovery, require manual intervention |
| **Handler not found** | Registry lookup fails | Log error, suggest handler registration |
| **State corruption** | JSON deserialization error | Mark checkpoint as corrupted, use previous checkpoint |
| **Concurrent writes** | Multiple processes writing same checkpoint | Last-write-wins (sequence number prevents ambiguity) |

### 5.2 Recovery Decision Tree

```
Start Recovery
    │
    ├─ Load Checkpoint
    │   ├─ Not Found → Error: Checkpoint does not exist
    │   └─ Found → Continue
    │
    ├─ Validate Status
    │   ├─ COMPLETED → Error: Cannot recover completed checkpoint
    │   ├─ RECOVERING → Error: Recovery already in progress
    │   ├─ ACTIVE/FAILED → Continue
    │
    ├─ Check Retry Limits
    │   ├─ Exceeded → Error: Max retries reached
    │   └─ Within Limit → Continue
    │
    ├─ Rebuild Context
    │   ├─ Missing Parent → Error: Context chain broken
    │   └─ Complete Chain → Continue
    │
    ├─ Resolve Handler
    │   ├─ Not Found → Error: Handler not registered
    │   └─ Found → Continue
    │
    └─ Resume Execution
        ├─ Success → Mark COMPLETED
        └─ Failure → Mark FAILED, increment retry_count
```

---

## Performance Considerations

### 6.1 Optimization Strategies

1. **Lazy Loading**: Only load checkpoint data when needed for recovery
2. **Index for Fast Lookup**: `index.json` provides O(1) latest checkpoint access
3. **Incremental State**: Store deltas instead of full state (future enhancement)
4. **Compression**: GZIP checkpoint JSON for large state (threshold: 100KB)
5. **Async I/O**: Use `aiofiles` for non-blocking filesystem operations

### 6.2 Scalability Limits

| Resource | Limit | Mitigation |
|----------|-------|------------|
| **Checkpoint file size** | ~10MB | Split large state into referenced files |
| **Context chain depth** | ~100 checkpoints | Periodic chain consolidation |
| **Concurrent workflows** | ~1000 | Shard by workflow_id hash |
| **Recovery time** | <5 seconds for 90th percentile | Parallel context rebuild |

---

## Testing Strategy

### 7.1 Unit Tests

```python
# tests/unit/domain/test_checkpoint.py

def test_checkpoint_mark_completed_when_active_then_status_becomes_completed():
    checkpoint = Checkpoint(...)
    checkpoint.status = CheckpointStatus.ACTIVE

    checkpoint.mark_completed()

    assert checkpoint.status == CheckpointStatus.COMPLETED

def test_checkpoint_mark_completed_when_already_completed_then_raises_error():
    checkpoint = Checkpoint(...)
    checkpoint.status = CheckpointStatus.COMPLETED

    with pytest.raises(InvalidStateError):
        checkpoint.mark_completed()
```

### 7.2 Integration Tests

```python
# tests/integration/infrastructure/test_filesystem_checkpoint_repository.py

async def test_save_checkpoint_then_can_retrieve_by_id():
    repo = FilesystemCheckpointRepository(tmp_path)
    checkpoint = create_test_checkpoint()

    await repo.save(checkpoint)
    retrieved = await repo.get_by_id(checkpoint.id)

    assert retrieved == checkpoint

async def test_atomic_write_when_concurrent_saves_then_no_corruption():
    # Test atomic rename prevents partial writes
    pass
```

### 7.3 E2E Tests

```python
# tests/e2e/orchestration/test_checkpoint_recovery.py

async def test_recover_from_agent_failure_then_workflow_resumes():
    # Create workflow with 3 stages
    # Inject failure in stage 2, agent 1
    # Verify checkpoint created at failure
    # Recover from checkpoint
    # Verify workflow completes successfully
    pass
```

---

## Migration Path

### 8.1 Phase 1: Core Implementation
- Implement domain entities (Checkpoint, CheckpointId)
- Implement FilesystemCheckpointRepository
- Unit tests for domain and infrastructure

### 8.2 Phase 2: Recovery Mechanism
- Implement RecoverFromCheckpointHandler
- Implement HandlerRegistry
- Integration tests for recovery flow

### 8.3 Phase 3: Orchestration Integration
- Add checkpoint creation hooks to workflow stages
- Register resume handlers for all stage types
- E2E tests for full workflows

### 8.4 Phase 4: Tooling and Observability
- CLI commands for checkpoint inspection
- Recovery HTTP API endpoints
- Monitoring dashboards for checkpoint metrics

---

## Open Questions for Critique

1. **State Size Management**: Should we enforce maximum checkpoint size? If so, what threshold?
2. **Compression Strategy**: Should compression be opt-in or automatic above size threshold?
3. **Concurrency Model**: Do we need distributed locking for multi-process orchestration?
4. **Schema Evolution**: How to handle checkpoint format versioning across Jerry upgrades?
5. **Retention Policy**: Should old checkpoints auto-purge? If so, based on age or count?

---

## Session Context for ps-critic Handoff

```yaml
session_context:
  schema_version: "1.0.0"
  session_id: "ps-orch-003-test"
  source_agent:
    id: "ps-architect"
    version: "v2.1.0"
    family: "ps"
  target_agent:
    id: "ps-critic"
    family: "ps"
  payload:
    iteration: 1
    artifact_to_critique: "projects/PROJ-002-nasa-systems-engineering/tests/ps-orchestration-results/PS-ORCH-003/iteration-1-design.md"
    evaluation_criteria:
      - "Completeness: All required components defined (data model, recovery mechanism, filesystem integration)"
      - "Consistency: Interfaces align with Jerry hexagonal architecture (ports in domain, adapters in infrastructure)"
      - "Feasibility: Implementation is achievable with existing infrastructure (Python stdlib, JSON, filesystem)"
      - "Error handling: Recovery from partial failures covered (agent crash, storage failure, corruption)"
      - "Performance: Scalability considerations addressed (lazy loading, indexing, async I/O)"
      - "Testability: Clear test strategy defined (unit, integration, E2E)"
    key_findings:
      - "Designed hierarchical checkpoint model with CheckpointId value object for filesystem-safe paths"
      - "Recovery uses lazy loading with incremental context rebuild from parent chain"
      - "Atomic writes via temp-file-rename pattern prevents partial checkpoint corruption"
      - "Handler registry enables pluggable resume strategies per checkpoint type"
      - "JSON format provides human-readable, diffable, version-controllable checkpoints"
      - "Context rebuild walks parent_checkpoint_id chain to replay state deltas"
      - "Open question: Need distributed locking for multi-process orchestration?"
    design_constraints:
      - "Zero-dependency core: Python stdlib only in domain layer"
      - "Filesystem-first: No database dependencies"
      - "Hexagonal architecture: Clear port/adapter separation"
      - "CQRS pattern: Commands (CreateCheckpoint) and Queries (GetCheckpoint)"
    next_steps_if_approved:
      - "Phase 1: Implement domain entities and filesystem repository"
      - "Phase 2: Implement recovery handler and handler registry"
      - "Phase 3: Integrate checkpoint hooks into orchestration workflow"
      - "Phase 4: Build CLI/API tooling for checkpoint management"
```

---

## References

- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/) - Alistair Cockburn
- [Event Sourcing Pattern](https://martinfowler.com/eaaDev/EventSourcing.html) - Martin Fowler
- [Saga Pattern for Distributed Transactions](https://microservices.io/patterns/data/saga.html)
- [CQRS Pattern](https://martinfowler.com/bliki/CQRS.html) - Martin Fowler
- Jerry Constitution v1.0 - `docs/governance/JERRY_CONSTITUTION.md`
- Jerry Coding Standards - `.claude/rules/coding-standards.md`
