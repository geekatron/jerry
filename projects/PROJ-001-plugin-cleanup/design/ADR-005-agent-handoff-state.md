# ADR-005: Agent Handoff State Format

**Status**: Proposed
**Date**: 2026-01-09
**Deciders**: Development Team
**Technical Story**: INIT-DEV-SKILL

---

## Context

The Jerry Framework development skill employs a multi-agent architecture where specialized agents (dev-engineer, dev-qa, dev-reviewer) collaborate to complete development tasks. These agents need to pass state between each other as work progresses through phases: planning, implementing, testing, and reviewing.

### Problem Statement

When Agent A completes its work and hands off to Agent B, both agents need a shared understanding of:
- What work has been completed
- What artifacts were generated (files, tests, configurations)
- What decisions were made and why
- What issues remain unresolved
- What context is needed for the next phase

Without a standardized handoff format, agents risk:
1. **Information loss**: Critical context dropped between phases
2. **Context rot**: Passing too much data degrades subsequent agent performance
3. **Inconsistent behavior**: Different agents interpreting state differently
4. **Debugging difficulty**: No clear audit trail of agent decisions

### Current State

The Jerry Framework does not currently have a formalized agent handoff mechanism. Agents operate independently with ad-hoc context sharing through CLAUDE.md files and work tracker updates.

### Relevant Research Findings

From the research synthesis (e-001, e-006, e-007), the following patterns directly inform this decision:

| Pattern ID | Name | Key Insight |
|------------|------|-------------|
| PAT-003-e001 | Handle Pattern for Large Data | Store large artifacts externally; keep only references/summaries in context |
| PAT-004-e001 | Pre-Rot Threshold Compaction | Proactively summarize at ~25% of context limit, not at 100% |
| PAT-005-e001 | Explicit State Handoff | Use typed Command objects with explicit state updates rather than implicit sharing |
| PAT-003-e006 | Agent Task Schema | Structured inputs, outputs, dependencies, and success criteria |

---

## Decision Drivers

1. **Context Engineering Best Practices (e-001)**
   - Context rot degrades AI performance even within advertised limits
   - Effective systems compact at ~25% of limit
   - Large artifacts should be offloaded to files with only summaries in context

2. **Task Schema Requirements (e-006)**
   - Agents need structured, machine-readable specifications
   - Inputs, outputs, and success criteria must be explicit
   - Dependencies should be encoded as DAGs

3. **Multi-Agent Coordination (e-001)**
   - LangGraph uses `Command` objects for explicit handoffs
   - Google ADK provides hierarchical state scopes (app, user, session, temp)
   - AutoGen requires explicit `handoffs` declarations

4. **Jerry Framework Constraints**
   - c-002: Knowledge must be persisted to files
   - c-004: Reasoning must be documented
   - c-005: File-based persistence required
   - c-007: Operations must be finite (bounded)

5. **Debugging and Auditability**
   - State transitions must be traceable
   - Handoff history enables debugging and replay
   - Clear format enables human inspection

---

## Considered Options

### Option 1: In-Context State (Full)

Pass all state directly in the agent prompt without file persistence.

**Implementation:**
```python
# All state embedded in prompt
system_prompt = f"""
Previous agent completed planning phase.
Files created: {list_of_files}
Decisions made: {list_of_decisions}
Full context: {full_context_dump}
"""
```

**Pros:**
- Simple implementation
- Immediate access without I/O
- No file management overhead

**Cons:**
- Context rot at scale (Chroma Research shows degradation at ~25% of advertised limit)
- Token limits constrain state size
- No persistence across sessions
- Violates Jerry constraint c-005 (file persistence)

**Risk Level:** High - Does not scale beyond simple tasks

### Option 2: File-Based State (Fully Offloaded)

Store all state in `.jerry/state/{task_id}.json` files with agents reading/writing state exclusively through files.

**Implementation:**
```python
# State file: .jerry/state/TASK-001.json
{
    "task_id": "TASK-001",
    "phase": "implementing",
    "artifacts": [
        {"path": "src/module.py", "hash": "abc123"},
        {"path": "tests/test_module.py", "hash": "def456"}
    ],
    "context": "Full multi-paragraph context...",
    "decisions": ["Chose approach A because...", "..."],
    "blocking_issues": []
}
```

**Pros:**
- Unlimited state size
- Persistent across sessions
- Full audit trail
- Complies with c-005

**Cons:**
- I/O overhead on every access
- Agent must read file before acting
- No immediate context for quick decisions
- File locking complexity (PAT-002-e005)

**Risk Level:** Medium - Works but adds latency

### Option 3: Hybrid (Summary + File Reference)

Keep a compressed summary in context with detailed state in files. Agents receive enough context to make decisions with file references for details.

**Implementation:**
```python
# In-context summary (lightweight)
handoff_summary = """
Task: TASK-001 (Implement user login)
Phase: implementing (was: planning)
Artifacts: 2 files created (see .jerry/state/TASK-001.json)
Key decisions: TDD approach, JWT auth
Blocking: None
State file: .jerry/state/TASK-001.json
"""

# Full state in file (heavyweight)
# .jerry/state/TASK-001.json contains complete details
```

**Pros:**
- Balanced context usage
- Immediate context for decisions
- Full details available on-demand
- Persistent and auditable
- Aligns with PAT-003-e001 (Handle Pattern)

**Cons:**
- More complex implementation
- Requires summary generation logic
- Two sources of truth to keep synchronized

**Risk Level:** Low - Industry best practice

### Option 4: Event Log (Append-Only)

Model state as a sequence of events that can be replayed to reconstruct current state.

**Implementation:**
```python
# Event log: .jerry/events/TASK-001.jsonl
{"ts": "2026-01-09T10:00:00Z", "type": "task_created", "data": {...}}
{"ts": "2026-01-09T10:05:00Z", "type": "tests_generated", "data": {"files": [...]}}
{"ts": "2026-01-09T10:10:00Z", "type": "decision_made", "data": {"decision": "..."}}
{"ts": "2026-01-09T10:15:00Z", "type": "phase_changed", "data": {"from": "planning", "to": "implementing"}}
```

**Pros:**
- Complete audit trail
- Time-travel debugging
- Event-driven architecture alignment
- Natural for distributed systems

**Cons:**
- Reconstruction overhead (must replay events)
- Growing log size over time
- More complex state queries
- Overkill for single-session workflows

**Risk Level:** Medium - Adds complexity without proportional benefit for Jerry's use case

---

## Decision Outcome

**Chosen Option:** Option 3 - Hybrid (Summary + File Reference)

### Rationale

1. **Aligns with PAT-003-e001 (Handle Pattern)**: Store large artifacts externally; keep only references/summaries in context. This is the industry standard from Google ADK's ArtifactService pattern.

2. **Addresses Context Rot (PAT-004-e001)**: By keeping only summaries in context, we avoid the performance degradation documented in Chroma Research's context rot findings.

3. **Enables PAT-005-e001 (Explicit State Handoff)**: Typed state schema with clear structure enables reliable handoff similar to LangGraph's Command pattern.

4. **Complies with Jerry Constraints**:
   - c-002: Citations in state file
   - c-004: Reasoning captured in decisions_made
   - c-005: File-based persistence
   - c-007: Bounded state size

5. **Supports Debugging**: State files provide audit trail; summaries enable quick inspection.

### Consequences

**Positive:**
- Predictable context usage (~500 tokens for summary)
- Full state available for complex queries
- Persistent across sessions
- Human-readable for debugging
- Supports incremental refinement

**Negative:**
- Synchronization overhead between summary and file
- Implementation complexity vs. simpler options
- Summary generation may lose nuance

**Neutral:**
- Learning curve for developers
- File I/O for detailed access

---

## Implementation

### State Schema

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum

class HandoffPhase(Enum):
    """Development workflow phases."""
    PLANNING = "planning"
    IMPLEMENTING = "implementing"
    TESTING = "testing"
    REVIEWING = "reviewing"
    COMPLETED = "completed"

@dataclass(frozen=True)
class ArtifactRef:
    """Reference to a generated artifact."""
    path: str           # Relative path from project root
    artifact_type: str  # "source", "test", "config", "doc"
    content_hash: str   # SHA-256 for change detection
    size_bytes: int     # For context budget decisions

@dataclass(frozen=True)
class DecisionRecord:
    """Record of a decision made during the phase."""
    decision: str       # What was decided
    rationale: str      # Why (supports c-004)
    timestamp: datetime
    agent: str          # Which agent made the decision
    alternatives: list[str] = field(default_factory=list)  # Considered alternatives

@dataclass(frozen=True)
class BlockingIssue:
    """Issue blocking progress."""
    issue: str          # Description
    severity: str       # "blocker", "high", "medium", "low"
    suggested_action: str
    requires_human: bool = False  # Triggers PAT-006-e001 gate

@dataclass
class AgentHandoffState:
    """
    Complete state for agent handoff.

    This is the full state stored in .jerry/state/{task_id}.json.
    A compressed summary is generated for in-context use.
    """
    # Identity
    task_id: str
    task_title: str

    # Phase tracking
    phase: HandoffPhase
    previous_phase: Optional[HandoffPhase] = None
    phase_started_at: datetime = field(default_factory=datetime.utcnow)

    # Artifacts (file references, not content)
    artifacts: list[ArtifactRef] = field(default_factory=list)

    # Context and decisions
    context_summary: str = ""  # Compressed context (~500 tokens max)
    decisions_made: list[DecisionRecord] = field(default_factory=list)

    # Issues and blockers
    blocking_issues: list[BlockingIssue] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    # Quality gate results
    quality_gates_passed: list[str] = field(default_factory=list)
    quality_gates_failed: list[str] = field(default_factory=list)

    # Handoff metadata
    source_agent: str = ""
    target_agent: str = ""
    handoff_timestamp: datetime = field(default_factory=datetime.utcnow)

    # Version for optimistic concurrency (PAT-003-e005)
    version: int = 1

    def generate_summary(self, max_tokens: int = 500) -> str:
        """
        Generate compressed summary for in-context use.

        This implements PAT-003-e001 (Handle Pattern): keep lightweight
        reference in context, full details in file.
        """
        artifact_summary = f"{len(self.artifacts)} files"
        if self.artifacts:
            types = set(a.artifact_type for a in self.artifacts)
            artifact_summary = f"{len(self.artifacts)} files ({', '.join(types)})"

        blocking_summary = "None"
        if self.blocking_issues:
            blockers = [i for i in self.blocking_issues if i.severity == "blocker"]
            if blockers:
                blocking_summary = f"{len(blockers)} blocker(s): {blockers[0].issue[:50]}..."

        recent_decisions = ""
        if self.decisions_made:
            recent = self.decisions_made[-2:]  # Last 2 decisions
            recent_decisions = "; ".join(d.decision[:50] for d in recent)

        return f"""## Agent Handoff State
Task: {self.task_id} - {self.task_title}
Phase: {self.phase.value} (from: {self.previous_phase.value if self.previous_phase else 'start'})
Artifacts: {artifact_summary}
Decisions: {recent_decisions or 'None'}
Blocking: {blocking_summary}
Gates: {len(self.quality_gates_passed)} passed, {len(self.quality_gates_failed)} failed
State file: .jerry/state/{self.task_id}.json"""
```

### State Persistence

State is persisted using atomic writes with file locking (PAT-001-e005, PAT-002-e005).

```python
import json
from pathlib import Path
from filelock import FileLock
from typing import Optional

class HandoffStateStore:
    """
    Persistent storage for agent handoff state.

    Uses atomic writes and file locking for concurrent access safety.
    """

    def __init__(self, project_dir: Path):
        self.state_dir = project_dir / ".jerry" / "state"
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.lock_timeout = 30  # seconds (PAT-002-e005)

    def _state_path(self, task_id: str) -> Path:
        return self.state_dir / f"{task_id}.json"

    def _lock_path(self, task_id: str) -> Path:
        return self.state_dir / f"{task_id}.lock"

    def save(self, state: AgentHandoffState) -> None:
        """
        Save state with atomic write and file locking.

        Implements PAT-001-e005 (Atomic Write with Durability) and
        PAT-002-e005 (File-Based Mutual Exclusion).
        """
        state_path = self._state_path(state.task_id)
        lock_path = self._lock_path(state.task_id)

        with FileLock(lock_path, timeout=self.lock_timeout):
            # Check version for optimistic concurrency
            existing = self._load_raw(state.task_id)
            if existing and existing.get("version", 0) >= state.version:
                if existing.get("version", 0) > state.version:
                    raise ConcurrencyError(
                        f"State version conflict: file={existing['version']}, "
                        f"trying to save={state.version}"
                    )

            # Atomic write: temp file + rename
            temp_path = state_path.with_suffix(".tmp")
            try:
                with open(temp_path, "w") as f:
                    json.dump(self._to_dict(state), f, indent=2, default=str)
                    f.flush()
                    import os
                    os.fsync(f.fileno())  # Ensure durability
                temp_path.rename(state_path)
            except Exception:
                temp_path.unlink(missing_ok=True)
                raise

    def load(self, task_id: str) -> Optional[AgentHandoffState]:
        """Load state from file."""
        data = self._load_raw(task_id)
        if data:
            return self._from_dict(data)
        return None

    def _load_raw(self, task_id: str) -> Optional[dict]:
        state_path = self._state_path(task_id)
        if state_path.exists():
            with open(state_path) as f:
                return json.load(f)
        return None

    def _to_dict(self, state: AgentHandoffState) -> dict:
        """Convert state to dictionary for JSON serialization."""
        return {
            "task_id": state.task_id,
            "task_title": state.task_title,
            "phase": state.phase.value,
            "previous_phase": state.previous_phase.value if state.previous_phase else None,
            "phase_started_at": state.phase_started_at.isoformat(),
            "artifacts": [
                {
                    "path": a.path,
                    "artifact_type": a.artifact_type,
                    "content_hash": a.content_hash,
                    "size_bytes": a.size_bytes,
                }
                for a in state.artifacts
            ],
            "context_summary": state.context_summary,
            "decisions_made": [
                {
                    "decision": d.decision,
                    "rationale": d.rationale,
                    "timestamp": d.timestamp.isoformat(),
                    "agent": d.agent,
                    "alternatives": d.alternatives,
                }
                for d in state.decisions_made
            ],
            "blocking_issues": [
                {
                    "issue": b.issue,
                    "severity": b.severity,
                    "suggested_action": b.suggested_action,
                    "requires_human": b.requires_human,
                }
                for b in state.blocking_issues
            ],
            "warnings": state.warnings,
            "quality_gates_passed": state.quality_gates_passed,
            "quality_gates_failed": state.quality_gates_failed,
            "source_agent": state.source_agent,
            "target_agent": state.target_agent,
            "handoff_timestamp": state.handoff_timestamp.isoformat(),
            "version": state.version,
        }

    def _from_dict(self, data: dict) -> AgentHandoffState:
        """Reconstruct state from dictionary."""
        # Implementation details omitted for brevity
        pass

class ConcurrencyError(Exception):
    """Raised when optimistic concurrency check fails."""
    pass
```

### State Loading and Handoff Protocol

```python
from typing import Protocol

class AgentHandoffProtocol(Protocol):
    """
    Protocol for agent-to-agent state handoff.

    Implements PAT-005-e001 (Explicit State Handoff).
    """

    def prepare_handoff(
        self,
        task_id: str,
        target_agent: str,
        phase: HandoffPhase,
    ) -> HandoffCommand:
        """
        Prepare handoff to next agent.

        Returns a command object with explicit state delta,
        similar to LangGraph's Command pattern.
        """
        ...

    def receive_handoff(
        self,
        command: HandoffCommand,
    ) -> AgentHandoffState:
        """
        Receive handoff from previous agent.

        Loads full state from file, validates, and returns
        for agent processing.
        """
        ...

@dataclass
class HandoffCommand:
    """
    Command object for explicit agent handoff.

    Based on LangGraph Command pattern (PAT-005-e001).
    """
    task_id: str
    target_agent: str
    phase: HandoffPhase
    state_delta: dict  # Changes made by source agent
    context_summary: str  # Compressed for target agent's context
    state_file: str  # Path to full state file

class AgentHandoffService:
    """
    Service for managing agent handoffs.
    """

    def __init__(self, store: HandoffStateStore):
        self.store = store

    def handoff(
        self,
        source_agent: str,
        target_agent: str,
        task_id: str,
        new_phase: HandoffPhase,
        artifacts: list[ArtifactRef],
        decisions: list[DecisionRecord],
        blocking_issues: list[BlockingIssue],
    ) -> HandoffCommand:
        """
        Execute handoff from source to target agent.

        1. Load current state
        2. Apply updates
        3. Increment version
        4. Save atomically
        5. Generate command for target
        """
        # Load existing state or create new
        state = self.store.load(task_id)
        if state is None:
            raise ValueError(f"Task {task_id} not found")

        # Update state
        updated_state = AgentHandoffState(
            task_id=state.task_id,
            task_title=state.task_title,
            phase=new_phase,
            previous_phase=state.phase,
            phase_started_at=datetime.utcnow(),
            artifacts=state.artifacts + artifacts,
            context_summary=self._compress_context(state, artifacts, decisions),
            decisions_made=state.decisions_made + decisions,
            blocking_issues=blocking_issues,  # Replace, not append
            warnings=state.warnings,
            quality_gates_passed=state.quality_gates_passed,
            quality_gates_failed=state.quality_gates_failed,
            source_agent=source_agent,
            target_agent=target_agent,
            handoff_timestamp=datetime.utcnow(),
            version=state.version + 1,
        )

        # Save with optimistic concurrency
        self.store.save(updated_state)

        # Generate command for target agent
        return HandoffCommand(
            task_id=task_id,
            target_agent=target_agent,
            phase=new_phase,
            state_delta={
                "artifacts_added": len(artifacts),
                "decisions_made": len(decisions),
                "blocking_issues": len(blocking_issues),
            },
            context_summary=updated_state.generate_summary(),
            state_file=str(self.store._state_path(task_id)),
        )

    def _compress_context(
        self,
        state: AgentHandoffState,
        new_artifacts: list[ArtifactRef],
        new_decisions: list[DecisionRecord],
    ) -> str:
        """
        Compress context to stay within token budget.

        Implements PAT-004-e001 (Pre-Rot Threshold Compaction).
        """
        # Keep recent context, summarize older
        max_decisions = 5
        max_context_chars = 2000

        recent_decisions = (state.decisions_made + new_decisions)[-max_decisions:]
        decision_text = "\n".join(
            f"- {d.decision}: {d.rationale[:100]}"
            for d in recent_decisions
        )

        context = f"""
Task: {state.task_title}
Current phase: {state.phase.value}
Total artifacts: {len(state.artifacts) + len(new_artifacts)}
Recent decisions:
{decision_text}
"""

        if len(context) > max_context_chars:
            context = context[:max_context_chars] + "\n[truncated]"

        return context
```

### Agent Integration Example

```python
# Example: dev-engineer agent receiving handoff from planner
class DevEngineerAgent:
    """Development engineer agent."""

    def __init__(self, handoff_service: AgentHandoffService):
        self.handoff_service = handoff_service

    async def execute(self, command: HandoffCommand) -> HandoffCommand:
        """
        Execute development phase and handoff to QA.
        """
        # 1. Load full state if needed
        state = self.handoff_service.store.load(command.task_id)

        # 2. Read context summary (in-context, lightweight)
        print(f"Received task: {command.context_summary}")

        # 3. Perform development work
        # ... generate tests (PAT-001-e003: test-first)
        # ... generate code
        # ... run quality gates

        artifacts_created = [
            ArtifactRef(
                path="src/login.py",
                artifact_type="source",
                content_hash="abc123",
                size_bytes=1024,
            ),
            ArtifactRef(
                path="tests/test_login.py",
                artifact_type="test",
                content_hash="def456",
                size_bytes=512,
            ),
        ]

        decisions = [
            DecisionRecord(
                decision="Implemented JWT-based authentication",
                rationale="Stateless, scalable, industry standard",
                timestamp=datetime.utcnow(),
                agent="dev-engineer",
                alternatives=["Session-based auth", "OAuth only"],
            ),
        ]

        # 4. Handoff to QA agent
        return self.handoff_service.handoff(
            source_agent="dev-engineer",
            target_agent="dev-qa",
            task_id=command.task_id,
            new_phase=HandoffPhase.TESTING,
            artifacts=artifacts_created,
            decisions=decisions,
            blocking_issues=[],
        )
```

---

## Validation

### Validation Criteria

| Criterion | Validation Method | Expected Outcome |
|-----------|-------------------|------------------|
| Context stays within budget | Token counting in generate_summary() | < 500 tokens per summary |
| State persists across sessions | Integration test with restart | State recoverable |
| Concurrent access safety | Load test with multiple instances | No data corruption |
| Handoff completeness | Unit test with state diffing | No information loss |
| Human readability | Manual inspection of JSON files | Clear structure |

### Test Scenarios

```python
# tests/test_handoff_state.py
import pytest
from datetime import datetime

class TestAgentHandoffState:
    """Tests for agent handoff state management."""

    def test_summary_generation_within_token_limit(self):
        """Summary should stay within 500 token budget."""
        state = AgentHandoffState(
            task_id="TASK-001",
            task_title="Implement user login",
            phase=HandoffPhase.IMPLEMENTING,
            artifacts=[ArtifactRef(...) for _ in range(50)],
            decisions_made=[DecisionRecord(...) for _ in range(20)],
        )
        summary = state.generate_summary(max_tokens=500)
        # Rough token estimate: ~4 chars per token
        assert len(summary) < 2000

    def test_atomic_write_on_concurrent_access(self, tmp_path):
        """Concurrent writes should not corrupt state."""
        store = HandoffStateStore(tmp_path)
        state = AgentHandoffState(task_id="TASK-001", ...)

        # Simulate concurrent access
        # ... threading test ...

        loaded = store.load("TASK-001")
        assert loaded.version > 0

    def test_optimistic_concurrency_detection(self, tmp_path):
        """Version conflict should raise ConcurrencyError."""
        store = HandoffStateStore(tmp_path)
        state_v1 = AgentHandoffState(task_id="TASK-001", version=1)
        store.save(state_v1)

        state_v1_again = AgentHandoffState(task_id="TASK-001", version=1)
        with pytest.raises(ConcurrencyError):
            store.save(state_v1_again)

    def test_handoff_preserves_artifacts(self):
        """Handoff should not lose artifact references."""
        # ... test implementation ...
```

### Integration with Quality Gates

The handoff state integrates with quality gate enforcement:

1. **Pre-handoff gate**: Validate state completeness before handoff
2. **Phase gate**: Ensure required artifacts exist for phase transition
3. **Human gate**: Trigger human approval for blocking issues marked `requires_human=True`

---

## References

### Research Documents

1. **e-001**: Agent-Based Software Development Workflows
   - PAT-003-e001: Handle Pattern for Large Data
   - PAT-004-e001: Pre-Rot Threshold Compaction
   - PAT-005-e001: Explicit State Handoff
   - Google ADK ArtifactService pattern
   - LangGraph Command pattern

2. **e-006**: Task Template Schemas for Software Development
   - PAT-003-e006: Agent Task Schema
   - Structured inputs, outputs, dependencies

3. **e-007**: Research Synthesis
   - Theme 4: Context is Precious - Manage it Aggressively
   - Constraint mapping to Jerry principles

4. **e-008**: Architecture Analysis
   - Interface layer: AgentHandoffProtocol
   - Full pattern mapping table

### External Sources

1. LangGraph Multi-Agent Overview. https://docs.langchain.com/oss/python/langgraph/overview
2. Google ADK Multi-Agent Systems. https://google.github.io/adk-docs/agents/multi-agents/
3. Context Rot Research. Chroma Research. https://research.trychroma.com/context-rot
4. Effective Context Engineering. Anthropic. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-09 | ps-architect | Initial draft |

---

*ADR-005 created as part of PROJ-001-plugin-cleanup development skill design.*
