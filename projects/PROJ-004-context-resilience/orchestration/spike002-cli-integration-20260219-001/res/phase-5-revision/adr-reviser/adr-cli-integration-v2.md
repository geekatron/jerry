# ADR-SPIKE002-002: Revised CLI-Integrated Context Resilience Architecture (v2)

<!-- PS-ID: SPIKE-002 | ENTRY-ID: phase-5 | DATE: 2026-02-19 -->
<!-- AGENT: ps-architect v2.3.0 | MODEL: claude-opus-4-6 -->
<!-- SUPERSEDES: ADR-SPIKE002-001 -->

> Revised Architecture Decision Record for context resilience. Supersedes ADR-SPIKE002-001 based on DISC-001 findings and DEC-001 corrective decisions. Chooses proper bounded context + CLI-first hooks over infrastructure placement.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Status](#status) | Decision lifecycle state and supersession |
| [Context](#context) | Problem background, forces, and DISC-001 invalidation |
| [Decision](#decision) | Chosen architecture: bounded context + CLI-first hooks |
| [Alternatives Considered](#alternatives-considered) | Four options with steelmanned analysis |
| [Consequences](#consequences) | Positive, negative, and neutral outcomes |
| [L0 Summary](#l0-summary) | Executive summary (5 bullets) |
| [L1 Technical Details](#l1-technical-details) | Component diagrams, data flows, interface contracts, hook wrappers |
| [L2 Strategic Implications](#l2-strategic-implications) | Hexagonal architecture impact, enforcement migration, CLI evolution |
| [Evidence](#evidence) | Traceability to Phase 1 audit, Phase 2 gap analysis, DISC-001, DEC-001 |

---

## Status

**PROPOSED** -- Pending review. Supersedes ADR-SPIKE002-001.

**Supersession rationale:** ADR-SPIKE002-001 chose Alternative 2 (Infrastructure Placement in `src/infrastructure/internal/enforcement/`). DISC-001 identified four findings that invalidate this choice: two incompatible execution paths (F1), enforcement folder as architectural tech debt (F2), invalid rejection reasoning for Alternative 3 (F3), and confusing scripts/hooks directory split (F4). DEC-001 captures four corrective decisions (D-001 through D-004) that this ADR implements.

**Criticality:** C3 (Significant) per AE-003 (modified ADR). Enforcement tiers: HARD + MEDIUM + all tiers.

---

## Context

### Problem Statement

SPIKE-001 designed a context resilience system (context fill monitoring, pre-compaction checkpointing, post-compaction resumption) using a hook-only approach. The design produced 14 follow-up work items estimated at 25-37 hours. SPIKE-001 treated the Jerry CLI as a black box and proposed building all detection, checkpointing, and injection logic from scratch within hook scripts.

SPIKE-002 Phase 1 (CLI Capability Audit) discovered that the Jerry CLI has substantial existing infrastructure directly relevant to context resilience:

- **LayeredConfigAdapter** (C3): 4-level hierarchical configuration with TOML parsing, dot-notation keys, and CLI management -- a direct replacement for the proposed threshold configuration file.
- **PromptReinforcementEngine** (C4): L2 per-prompt injection engine with L2-REINJECT marker parsing, rank-based sorting, and 600-token budget -- the proven pattern for context monitor injection.
- **SessionQualityContextGenerator** (C4): L1 session-start XML preamble generator with ~700 token budget -- the pattern for resumption context injection.
- **PreToolEnforcementEngine** (C4): L3 AST-based validation with governance escalation detection -- the pattern for resumption staleness detection.
- **AtomicFileAdapter** (C6): Safe file I/O with locking -- reusable for checkpoint writes.
- **FileSystemEventStore** (C6): JSONL append-only store with file locking and directory creation patterns -- applicable to checkpoint infrastructure.

SPIKE-002 Phase 2 (Gap Analysis) confirmed that 10 of 14 SPIKE-001 items can leverage existing CLI infrastructure (1 REUSE, 10 EXTEND, 3 NEW), reducing the work from 14 items to 9 consolidated items.

### DISC-001 Findings: Invalidation of ADR-SPIKE002-001

ADR-SPIKE002-001 chose Alternative 2 (infrastructure placement in the enforcement folder). A subsequent discovery audit (DISC-001) and user review identified four findings that invalidate this decision:

**F1: Two Incompatible Execution Paths.** Three of four hooks bypass the CLI by directly importing from `src/infrastructure/internal/enforcement/`. Only `session_start_hook.py` partially uses the CLI (`jerry --json projects context` via subprocess), but it also directly imports `SessionQualityContextGenerator`. The ADR's approach perpetuates this split by having new engines imported directly by hook scripts.

**F2: Enforcement Folder is Architectural Tech Debt.** The `src/infrastructure/internal/enforcement/` folder is a flat dumping ground with 7 files, no domain layer, no application layer, no ports, no adapters, and no composition root wiring. By contrast, `src/session_management/` has proper hexagonal layers (domain with aggregates, events, value objects; application with commands, queries, handlers, ports; infrastructure with adapters) wired through `bootstrap.py`. The same is true of `src/work_tracking/`. The enforcement folder is the exception, not the pattern to follow.

**F3: ADR-SPIKE002-001 Rejected Alternative 3 Using Invalid Reasoning.** Two specific errors:

1. *"Subprocess overhead per prompt is prohibitive within 5000ms timeout"* -- This conflates having a bounded context with calling it via subprocess. A single `jerry hooks <event>` command consolidates all logic into ONE subprocess call per hook event. `session_start_hook.py` already demonstrates that a subprocess call (`uv sync && uv run jerry --json projects context`) works within the 10,000ms timeout.

2. *"InMemorySessionRepository limitation means the CLI module cannot offer state benefits"* -- CWI-00 in the revised work plan creates `FileSystemSessionRepository` following the proven `EventSourcedWorkItemRepository` + `FileSystemEventStore` pattern. The ADR rejected an option based on a constraint the work plan itself eliminates.

**F4: scripts/ vs hooks/ Split Creates Confusion.** Hook implementations are scattered across two directories (`hooks/` and `scripts/`) with no clear rationale, mixing hook entry points with unrelated utility scripts.

### Forces

1. **Clean architecture consistency.** Proper bounded contexts (`src/session_management/`, `src/work_tracking/`) are the established pattern in Jerry. Each has domain/application/infrastructure layers, ports, adapters, and composition root wiring via `bootstrap.py`. The enforcement folder is the sole exception. New code should follow the rule, not the exception.

2. **CLI-first principle.** The Jerry CLI exists as the single interface layer. It routes commands and queries through dispatchers to handlers, with infrastructure wired at the composition root. Hooks that bypass the CLI by importing infrastructure modules directly create a parallel execution path that is untestable via the CLI and not subject to the same architectural constraints.

3. **Domain maturity.** After SPIKE-001 (7 phases) and SPIKE-002 (4+ phases), the context monitoring domain concepts are validated: ThresholdTier, FillEstimate, ContextState, CheckpointData, CompactionEvent. Two spikes of research confirmed these are stable domain concepts, not premature abstractions.

4. **Process boundary isolation.** Each hook execution and each CLI invocation is a separate Python process. Cross-process state must be file-based. CWI-00 (FileSystemSessionRepository) eliminates the `InMemorySessionRepository` limitation that ADR-SPIKE002-001 treated as a hard constraint, enabling real domain event integration across process boundaries.

5. **Hook timeout budgets.** UserPromptSubmit has a 5,000ms timeout; SessionStart and PreCompact have 10,000ms timeouts. A single subprocess call per hook event is feasible -- `session_start_hook.py` already calls `uv sync && uv run jerry --json projects context` within its 10,000ms budget.

6. **5-layer enforcement architecture integrity.** The existing L1-L5 enforcement layers (ADR-EPIC002-002) define where detection and injection happen. Context resilience must fit within this architecture. The CLI-first approach naturally maps hook events to enforcement layers while routing logic through the composition root.

---

## Decision

**Build context monitoring as a proper bounded context at `src/context_monitoring/` with domain, application, and infrastructure layers. Create `jerry hooks <event>` CLI commands for each hook event. Hook scripts become thin wrappers (~10 lines) that call the CLI via subprocess.**

This decision implements the four corrective decisions from DEC-001:

- **D-001:** Hooks call CLI, not import modules.
- **D-002:** Context monitoring is a proper bounded context from the start.
- **D-003:** CLI gets `jerry hooks` command namespace.
- **D-004:** Enforcement tech debt tracked separately, not deepened by FEAT-001.

### Bounded Context: `src/context_monitoring/`

#### Domain Layer (`src/context_monitoring/domain/`)

**Value Objects:**

| Value Object | File | Description |
|-------------|------|-------------|
| `ThresholdTier` | `value_objects/threshold_tier.py` | Enum: NOMINAL, LOW, WARNING, CRITICAL, EMERGENCY. Represents the context fill severity level. |
| `FillEstimate` | `value_objects/fill_estimate.py` | Frozen dataclass: `fill_percentage` (float 0.0-1.0), `input_tokens` (int), `context_window_size` (int), `threshold_tier` (ThresholdTier). Immutable snapshot of context fill state. |
| `CheckpointData` | `value_objects/checkpoint_data.py` | Frozen dataclass: `checkpoint_id` (str, e.g., "cx-003"), `timestamp` (str, ISO 8601), `compaction_sequence` (int), `context_state` (FillEstimate), `resumption_state` (dict or None), `session_info` (dict). Immutable snapshot of session state at compaction. |
| `ContextState` | `value_objects/context_state.py` | Frozen dataclass: `fill_estimate` (FillEstimate), `active_checkpoint` (CheckpointData or None), `compaction_count` (int). Aggregate context monitoring state. |

**Domain Events:**

| Event | File | Description |
|-------|------|-------------|
| `ContextThresholdReached` | `events/context_threshold_reached.py` | Raised when context fill crosses a threshold tier boundary. Fields: `session_id`, `fill_estimate`, `previous_tier`, `new_tier`, `timestamp`. |
| `CompactionDetected` | `events/compaction_detected.py` | Raised when the PreCompact hook fires. Fields: `session_id`, `checkpoint_id`, `fill_percentage`, `compaction_sequence`, `timestamp`. |
| `CheckpointCreated` | `events/checkpoint_created.py` | Raised when a checkpoint file is successfully written. Fields: `checkpoint_id`, `checkpoint_path`, `timestamp`. |

#### Application Layer (`src/context_monitoring/application/`)

**Services:**

| Service | File | Description |
|---------|------|-------------|
| `ContextFillEstimator` | `services/context_fill_estimator.py` | Orchestrates context fill estimation. Reads transcript data via `ITranscriptReader` port, reads threshold configuration via `IThresholdConfiguration` port, computes `FillEstimate`, determines `ThresholdTier`. |
| `CheckpointService` | `services/checkpoint_service.py` | Orchestrates checkpoint lifecycle. Creates checkpoints via `ICheckpointRepository` port, reads ORCHESTRATION.yaml resumption data, assembles `CheckpointData`. |
| `ResumptionContextGenerator` | `services/resumption_context_generator.py` | Generates `<resumption-context>` XML for session-start injection. Consumes `CheckpointData` from `CheckpointService`, reads ORCHESTRATION.yaml resumption fields, composes structured XML within ~760 token budget. Follows the same generator pattern as the existing `SessionQualityContextGenerator`. |

**Ports (Interfaces):**

| Port | File | Description |
|------|------|-------------|
| `ITranscriptReader` | `ports/transcript_reader.py` | Protocol: `read_latest_tokens(transcript_path: str) -> int`. Abstracts transcript JSONL parsing. |
| `ICheckpointRepository` | `ports/checkpoint_repository.py` | Protocol: `save(data: CheckpointData) -> Path`, `get_latest_unacknowledged() -> CheckpointData or None`, `acknowledge(checkpoint_id: str) -> None`, `list_all() -> list[CheckpointData]`. |
| `IThresholdConfiguration` | `ports/threshold_configuration.py` | Protocol: `get_threshold(tier: str) -> float`, `is_enabled() -> bool`. Abstracts threshold config access. |

#### Infrastructure Layer (`src/context_monitoring/infrastructure/`)

**Adapters:**

| Adapter | File | Description |
|---------|------|-------------|
| `JsonlTranscriptReader` | `adapters/jsonl_transcript_reader.py` | Implements `ITranscriptReader`. Reads `$TRANSCRIPT_PATH` JSONL file, extracts `input_tokens` from the latest entry. Seek-to-end for O(1) reads. |
| `FilesystemCheckpointRepository` | `adapters/filesystem_checkpoint_repository.py` | Implements `ICheckpointRepository`. Reads/writes `.jerry/checkpoints/cx-{NNN}-checkpoint.json` using `AtomicFileAdapter`. Acknowledgment via `.acknowledged` marker files. Sequential ID generation. |
| `ConfigThresholdAdapter` | `adapters/config_threshold_adapter.py` | Implements `IThresholdConfiguration`. Bridges to `LayeredConfigAdapter` for threshold values. Reads `context_monitor.*` configuration keys. |

### CLI Commands: `jerry hooks <event>`

Four new CLI commands under the `hooks` namespace. Each command consolidates all logic for one hook event into a single CLI invocation.

| Command | Hook Event | Timeout | Responsibilities |
|---------|-----------|---------|-----------------|
| `jerry hooks prompt-submit` | UserPromptSubmit | 5,000ms | Context fill monitoring (ContextFillEstimator), compaction alert (unacknowledged checkpoint injection), quality reinforcement (existing PromptReinforcementEngine). Returns combined `additionalContext` JSON. |
| `jerry hooks session-start` | SessionStart | 10,000ms | Project context (existing), quality context (existing SessionQualityContextGenerator), resumption context (CheckpointService + ResumptionContextGenerator). Returns combined `additionalContext` JSON. |
| `jerry hooks pre-compact` | PreCompact | 10,000ms | Checkpoint creation (CheckpointService), session abandon (`jerry session abandon --reason "compaction"`). Returns `systemMessage` JSON. |
| `jerry hooks pre-tool-use` | PreToolUse | 5,000ms | Architecture validation (existing PreToolEnforcementEngine), resumption staleness detection (ORCHESTRATION.yaml `updated_at` check). Returns enforcement decision JSON. |

### Hook Wrapper Scripts

Hook scripts become thin wrappers. Each script reads stdin from Claude Code, calls the corresponding `jerry hooks <event>` command via subprocess, and pipes stdout back. All logic lives in the bounded contexts wired through `bootstrap.py`.

**Example wrapper (`hooks/user-prompt-submit.py`):**

```python
#!/usr/bin/env python3
"""UserPromptSubmit hook wrapper. Delegates to jerry hooks prompt-submit."""
import subprocess
import sys

result = subprocess.run(
    ["uv", "run", "--directory", "${CLAUDE_PLUGIN_ROOT}", "jerry", "--json", "hooks", "prompt-submit"],
    input=sys.stdin.buffer.read(),
    capture_output=True,
    timeout=4,  # 4s subprocess budget within 5s hook timeout
)
sys.stdout.buffer.write(result.stdout)
sys.exit(0)  # Always exit 0 (fail-open)
```

**Wrapper characteristics:**
- ~10 lines of code per wrapper
- Always exit 0 (fail-open per enforcement architecture)
- Subprocess timeout set 1 second below hook timeout to allow graceful handling
- No imports from `src/` -- the wrapper is decoupled from the codebase
- `${CLAUDE_PLUGIN_ROOT}` resolved by Claude Code at hook invocation time

### Composition Root Wiring

New bounded context components are wired through `bootstrap.py`, consistent with `session_management` and `work_tracking`:

- `ITranscriptReader` -> `JsonlTranscriptReader`
- `ICheckpointRepository` -> `FilesystemCheckpointRepository`
- `IThresholdConfiguration` -> `ConfigThresholdAdapter` (wrapping `LayeredConfigAdapter`)
- `ContextFillEstimator` receives ports via constructor injection
- `CheckpointService` receives ports via constructor injection
- `ResumptionContextGenerator` receives `CheckpointService` via constructor injection
- Hook CLI commands are registered in the CLI adapter routing, dispatching to application services

---

## Alternatives Considered

### Alternative 1: Hook-Only Implementation (SPIKE-001 Original)

**Description:** Build all context resilience logic from scratch within hook scripts. Each hook self-contains its own configuration parsing, state management, threshold logic, and injection formatting. No imports from the Jerry CLI codebase.

**Steelman (S-003):** This alternative offers the strongest isolation guarantees. Hook scripts are completely standalone -- a developer can read one file and understand the entire flow without knowledge of the CLI architecture. There is zero coupling to CLI internals, meaning CLI refactoring cannot break hooks. Initial prototyping is faster because there is no need to understand existing engine patterns, composition root wiring, or CQRS dispatching. For a framework where context resilience might eventually be extracted to a separate project, this isolation is valuable.

**Cons:**
- Duplicates configuration management (custom JSON config vs. `LayeredConfigAdapter` with env/project/root/defaults precedence and existing `jerry config get/set` CLI commands).
- Duplicates file I/O patterns (custom writes vs. `AtomicFileAdapter` with file locking).
- Duplicates token estimation logic (custom counting vs. existing calibration).
- 14 work items at 25-37 hours vs. 10 items at 19.5-28.5 hours.
- Creates two parallel systems: hook logic and CLI logic operating independently with no shared architecture.
- No path to bounded context: standalone scripts cannot evolve into a structured domain without a full rewrite.

**Why rejected:** The Phase 1 Audit demonstrates that 10 of 14 items either directly reuse or extend existing infrastructure. Building from scratch wastes proven, tested code and creates a maintenance burden. The isolation benefit does not justify the duplication cost when the CLI codebase is stable and well-structured.

### Alternative 2: Infrastructure Placement (ADR-SPIKE002-001's Original Choice)

**Description:** Place new context resilience engines in `src/infrastructure/internal/enforcement/` alongside existing enforcement engines. Follow the existing stateless, fail-open, token-budgeted engine pattern. Hook scripts import engines directly. Two-phase migration: Phase 1 infrastructure placement, Phase 2 bounded context extraction when domain stabilizes.

**Steelman (S-003):** This alternative minimizes upfront implementation effort. The enforcement engine pattern (stateless class, file-based I/O, fail-open) is proven and well-understood. Placing new engines alongside existing ones creates immediate pattern consistency within the enforcement folder. There is no subprocess overhead -- direct imports are faster than CLI subprocess calls. The two-phase approach is pragmatically cautious: it defers bounded context complexity until domain concepts are validated through implementation, reducing the risk of premature abstraction. A developer looking for "all enforcement-related code" finds it in one folder.

**Why rejected (DISC-001):**

1. **Deepens tech debt (F2).** The enforcement folder has no domain layer, no ports, no adapters, no composition root wiring. It is the only location in the codebase that violates hexagonal architecture. Adding 4 more engines to this folder increases the tech debt that must eventually be remediated. "Follow the existing engine pattern" is locally consistent but globally inconsistent with the codebase's actual architecture.

2. **Bypasses the CLI (F1).** Hook scripts importing engines directly create a parallel execution path. The logic is not testable via `jerry` commands, not wired through `bootstrap.py`, and not subject to the same dispatch/routing constraints as all other CLI operations. The `session_start_hook.py` proves the CLI-first pattern works -- there is no technical reason for other hooks to bypass it.

3. **Invalid rejection of Alternative 3 (F3).** ADR-SPIKE002-001 rejected the CLI-first approach citing subprocess overhead and `InMemorySessionRepository` limitations. The subprocess concern is addressed by consolidating all hook logic into a single CLI command per event. The session repository concern is eliminated by CWI-00 (`FileSystemSessionRepository`). The rejection was based on constraints that either do not apply or are resolved by the work plan.

4. **Deferred extraction carries hidden cost.** The "Phase 2 bounded context extraction" framing understates the migration effort. After Phase 1, all engines contain inline domain concepts (`ThresholdTier` enum, `FillEstimate` dataclass, `CheckpointData` structure), ad-hoc instantiation in hook scripts, and no port/adapter separation. Extracting to a bounded context later requires defining ports, creating adapters, restructuring domain concepts, and rewiring all hook imports. This is essentially a rewrite -- more expensive than building correctly from the start, since the domain is already well-understood.

### Alternative 3: Proper Bounded Context + CLI-First Hooks (CHOSEN)

**Description:** Create `src/context_monitoring/` as a proper bounded context with domain/application/infrastructure layers from the start. Add `jerry hooks <event>` CLI commands. Hook scripts become thin wrappers (~10 lines) calling the CLI via subprocess. All logic wired through `bootstrap.py`.

**Pros:**
- **Clean architecture from day one.** Follows the same hexagonal pattern as `session_management` (36 Python files across domain/application/infrastructure) and `work_tracking` (42 Python files across domain/application/infrastructure/persistence). No "dump now, extract later" compromise.
- **Single execution path.** All hook logic routes through CLI commands, dispatchers, and the composition root. Testable via `jerry --json hooks <event>`. Inspectable, debuggable, and consistent with all other CLI operations.
- **Domain concepts get a proper home.** `ThresholdTier`, `FillEstimate`, `CheckpointData`, `ContextState` are value objects in the domain layer. `ContextThresholdReached`, `CompactionDetected`, `CheckpointCreated` are domain events. These are not premature -- two spikes validated them.
- **Ports enable testability.** `ITranscriptReader`, `ICheckpointRepository`, `IThresholdConfiguration` are ports that can be stubbed in tests. No need to mock filesystem operations or parse real JSONL files in unit tests.
- **CLI discoverability.** Users and developers can inspect context state via `jerry --json hooks prompt-submit`, troubleshoot hook behavior, and validate integration without Claude Code running.
- **CWI-00 enables full domain event integration.** With `FileSystemSessionRepository`, the PreCompact hook can trigger `jerry session abandon --reason "compaction"` as a real session domain event. `ContextThresholdReached` events can trigger session actions. The architecture supports this naturally without workarounds.

**Cons:**
- **More initial setup than Alternative 2.** Creating the bounded context structure (domain/application/infrastructure layers, ports, adapters, composition root wiring) requires more upfront work than adding engines to the enforcement folder.
- **Subprocess overhead per hook.** Each hook invocation spawns one `uv run jerry --json hooks <event>` subprocess. This adds process startup time (Python interpreter + uv + module imports) within the hook timeout budget. Mitigation: single subprocess call per hook event; 4-second subprocess timeout within 5-second hook timeout; fail-open if timeout exceeded.
- **`jerry hooks` commands aggregate concerns.** `jerry hooks prompt-submit` handles both context monitoring and quality reinforcement in a single command. This aggregation is a trade-off: it reduces subprocess calls but couples the command to multiple bounded contexts. Acceptable because the hook event is the natural unit of work.
- **Two architectural styles coexist temporarily.** New hooks call the CLI; existing hooks still import enforcement engines directly. D-004 tracks enforcement migration as separate work, so this inconsistency persists until that enabler is executed.

**Why chosen:** The domain is mature (2 spikes, validated concepts). The codebase pattern is clear (hexagonal bounded contexts wired through `bootstrap.py`). The enforcement folder is tech debt, not a precedent. CWI-00 eliminates the session persistence constraint. A single subprocess call per hook event fits within timeout budgets. The initial setup cost is modest and avoids the hidden future cost of a Phase 2 extraction that is effectively a rewrite.

### Alternative 4: Status Line Integration (Method C as Primary)

**Description:** Use the ECW status line (`statusline.py`) as the primary context data source. Extend the status line's state file (`~/.claude/ecw-statusline-state.json`) to include `context_fill_percentage`, `input_tokens`, and `timestamp`. Hooks read this state file instead of parsing the transcript JSONL.

**Steelman (S-003):** This alternative provides the most accurate context fill data. The status line has direct access to `context_window.current_usage.input_tokens` from Claude Code's API response, providing exact (not heuristic) token counts. The relay mechanism already exists -- the status line writes state to a JSON file. Hooks would simply read a small JSON file rather than parsing JSONL transcripts. Compaction detection is already implemented in the status line (lines 463-506). This is the simplest data path with the highest fidelity.

**Cons:**
- **Timing dependency (R5).** The status line updates its state file based on Claude Code's stdin updates. The `UserPromptSubmit` hook fires when the user submits a prompt. The status line data reflects the state *before* the current prompt. At high fill rates (e.g., 29K tokens per quality gate iteration), the hook could miss a threshold crossing by one prompt.
- **Unvalidated feasibility.** Whether the status line state file reliably updates before `UserPromptSubmit` fires is an open question (SPIKE-001 OQ-1).
- **Single point of failure.** If the status line script errors, crashes, or is disabled, all context monitoring fails. Method A (transcript-based) uses a different data path (`$TRANSCRIPT_PATH`), providing redundancy.
- **Coupling to client-side mechanism.** The status line runs via `statusLine.command` in Claude Code settings, not via the hooks mechanism. Changes to Claude Code's status line protocol could silently break context monitoring.
- **User customization risk.** The status line script is user-facing and may be customized, replaced, or disabled.

**Why rejected:** The timing dependency is a fundamental reliability concern for a system whose purpose is to detect critical thresholds before context exhaustion. Method C should be investigated as a supplementary accuracy upgrade (CWI-08) but not adopted as the primary mechanism until OQ-1 is resolved. Alternative 3 uses Method A (transcript-based) as primary, which is proven reliable even if slightly less precise.

---

## Consequences

### Positive

1. **Clean architecture alignment.** Context monitoring follows the same hexagonal pattern as `session_management` (36 files, 3 layers) and `work_tracking` (42 files, 3 layers). The codebase has ONE architectural pattern, not two. New contributors learn one structure and find it everywhere.

2. **Single execution path via CLI.** All hook logic routes through `jerry hooks <event>` commands, dispatchers, the composition root, and bounded context services. Every hook behavior is testable via `jerry --json hooks <event>` without Claude Code running. This eliminates the current split where 3 of 4 hooks bypass the CLI.

3. **Port-based testability.** `ITranscriptReader`, `ICheckpointRepository`, `IThresholdConfiguration` ports enable pure unit testing with in-memory adapters. No filesystem mocking, no JSONL parsing in tests. The same pattern used by `session_management` (ports for `ISessionRepository`, `IProjectRepository`, `IEnvironment`) and `work_tracking` (ports for `IWorkItemRepository`, `IEventStore`).

4. **Domain event integration.** With CWI-00 providing `FileSystemSessionRepository`, `CompactionDetected` events trigger `jerry session abandon --reason "compaction"` as real session domain events persisted in the event store. `ContextThresholdReached` events create an audit trail. This is genuine domain-driven design, not file-based workarounds.

5. **No Phase 2 extraction cost.** Because the bounded context is built correctly from day one, there is no future migration effort to "extract from enforcement into a bounded context." The ADR-SPIKE002-001 Phase 2 extraction -- defining ports, creating adapters, restructuring domain concepts, rewiring hook imports -- is avoided entirely.

6. **CLI discoverability and debuggability.** `jerry --json hooks prompt-submit` can be called manually to inspect context monitoring behavior. `jerry --json hooks session-start` reveals resumption context. This makes hook behavior transparent and debuggable.

### Negative

1. **Subprocess overhead per hook invocation.** Each hook calls `uv run jerry --json hooks <event>`, which spawns a Python process, imports modules, and executes logic. This adds latency compared to direct imports. The UserPromptSubmit hook has a 5,000ms timeout; estimated subprocess overhead for existing CLI commands is within budget (based on `session_start_hook.py` operating within its 10,000ms timeout), but each new import adds to startup time. If the budget is exceeded, Claude Code silently drops the hook output, resulting in no context monitoring for that prompt. **Mitigation:** Single subprocess call per event (not per concern). 4-second subprocess timeout within 5-second hook timeout. Fail-open design: timeout means no monitoring, not user disruption.

2. **Two architectural styles coexist temporarily (D-004).** New hooks call the CLI via subprocess; existing hooks (UserPromptSubmit, PreToolUse, SubagentStop) still import enforcement engines directly. This inconsistency persists until the enforcement tech debt enabler migrates existing hooks to CLI-first. **Mitigation:** FEAT-001 hooks use the correct pattern. The inconsistency is visible and tracked, not hidden.

3. **More initial implementation effort.** Creating the bounded context structure requires defining value objects, events, services, ports, adapters, CLI commands, dispatcher routing, and composition root wiring. This is more upfront work than dropping engines into the enforcement folder. **Mitigation:** The effort premium is estimated at 3-5 hours over Alternative 2, offset by eliminating the Phase 2 extraction cost and reducing test infrastructure complexity (port-based testing vs. filesystem mocking).

4. **`jerry hooks` commands aggregate cross-context concerns.** `jerry hooks prompt-submit` orchestrates logic from both `context_monitoring` and the existing enforcement infrastructure. This aggregation couples the CLI command to multiple bounded contexts. **Mitigation:** The hook event is the natural orchestration boundary. The CLI command delegates to application services in each bounded context -- it orchestrates, it does not contain business logic.

5. **Hook wrappers add an indirection layer.** Developers debugging hook behavior must trace from the wrapper script to the CLI command to the application service to the domain logic. This is more layers than the current direct-import approach. **Mitigation:** Each layer has a clear responsibility. The wrapper is trivial (~10 lines). The CLI command routes to services. Services implement logic. This is standard hexagonal architecture, not excessive indirection.

### Neutral

1. **Token budget analysis unchanged.** The injection token budgets from ADR-SPIKE002-001 remain valid regardless of where the logic lives. Worst-case per-prompt: 1,080 tokens (quality reinforcement + context monitor + compaction alert). Session start with resumption: 1,660 tokens. These are independent of the architectural choice.

2. **Process boundary isolation remains a constraint.** All cross-process state uses file-based persistence (checkpoint files, transcript JSONL, configuration TOML, session event store JSONL). This is identical to the Alternative 2 approach. CWI-00 adds `FileSystemSessionRepository` for session state, but the fundamental constraint (hooks are separate processes) is unchanged.

3. **Enforcement folder unchanged by this decision.** FEAT-001 does not modify `src/infrastructure/internal/enforcement/`. The existing engines remain in place. D-004 tracks their migration as a separate enabler. This ADR neither creates tech debt nor remediates it -- it avoids deepening it.

---

## L0 Summary

1. **Context monitoring is built as a proper bounded context (`src/context_monitoring/`) from the start, not placed in the enforcement tech debt folder.** The domain concepts (ThresholdTier, FillEstimate, CheckpointData, ContextState) are validated by two research spikes and get proper domain/application/infrastructure layers, following the same hexagonal pattern as `session_management` and `work_tracking`.

2. **Hook scripts become thin wrappers (~10 lines) that call `jerry hooks <event>` CLI commands via subprocess.** All hook logic lives in bounded contexts wired through the composition root (`bootstrap.py`), creating a single execution path that is testable, inspectable, and consistent with the existing CLI architecture.

3. **Four new CLI commands consolidate all hook logic into single subprocess calls: `jerry hooks prompt-submit`, `jerry hooks session-start`, `jerry hooks pre-compact`, and `jerry hooks pre-tool-use`.** Each command handles one hook event's complete lifecycle within the hook timeout budget (5,000ms or 10,000ms).

4. **This decision supersedes ADR-SPIKE002-001, which chose infrastructure placement.** DISC-001 identified that the enforcement folder is tech debt (no domain layer, no ports, flat structure), that 3 of 4 hooks bypass the CLI creating parallel execution paths, and that the original ADR rejected the clean architecture option using invalid reasoning.

5. **Existing enforcement tech debt is not deepened and not fixed -- it is tracked separately.** FEAT-001 builds `context_monitoring` correctly. The existing enforcement folder migration is tracked as a separate enabler (D-004), keeping FEAT-001 focused on context resilience while acknowledging the architectural inconsistency.

---

## L1 Technical Details

### Component Diagram: `src/context_monitoring/` Bounded Context

```
src/context_monitoring/
  __init__.py
  domain/
    __init__.py
    value_objects/
      __init__.py
      threshold_tier.py          # ThresholdTier enum
      fill_estimate.py           # FillEstimate frozen dataclass
      checkpoint_data.py         # CheckpointData frozen dataclass
      context_state.py           # ContextState frozen dataclass
    events/
      __init__.py
      context_threshold_reached.py  # ContextThresholdReached
      compaction_detected.py        # CompactionDetected
      checkpoint_created.py         # CheckpointCreated
  application/
    __init__.py
    services/
      __init__.py
      context_fill_estimator.py       # Orchestrates fill estimation
      checkpoint_service.py           # Orchestrates checkpoint lifecycle
      resumption_context_generator.py # Generates <resumption-context> XML for session-start
    ports/
      __init__.py
      transcript_reader.py       # ITranscriptReader protocol
      checkpoint_repository.py   # ICheckpointRepository protocol
      threshold_configuration.py # IThresholdConfiguration protocol
  infrastructure/
    __init__.py
    adapters/
      __init__.py
      jsonl_transcript_reader.py           # Reads $TRANSCRIPT_PATH JSONL
      filesystem_checkpoint_repository.py  # .jerry/checkpoints/ persistence
      config_threshold_adapter.py          # LayeredConfigAdapter bridge
```

### Data Flow: `jerry hooks prompt-submit` (UserPromptSubmit)

This is the primary per-prompt hook, handling context monitoring, compaction alerts, and quality reinforcement.

```
1. Claude Code fires UserPromptSubmit event
2. hooks.json routes to hooks/user-prompt-submit.py (5000ms timeout)
3. Wrapper reads stdin, calls: uv run jerry --json hooks prompt-submit
4. CLI adapter routes to HooksPromptSubmitHandler

5. Handler invokes ContextFillEstimator (context_monitoring bounded context):
   5a. ContextFillEstimator calls ITranscriptReader.read_latest_tokens($TRANSCRIPT_PATH)
   5b. JsonlTranscriptReader reads JSONL, extracts input_tokens from latest entry
   5c. ContextFillEstimator calls IThresholdConfiguration.get_threshold() for each tier
   5d. ConfigThresholdAdapter reads from LayeredConfigAdapter:
       - context_monitor.warning_threshold  (default: 0.70)
       - context_monitor.critical_threshold (default: 0.80)
       - context_monitor.emergency_threshold (default: 0.88)
   5e. ContextFillEstimator computes FillEstimate(fill_percentage, input_tokens, threshold_tier)
   5f. Generates <context-monitor> XML tag (40-200 tokens based on tier)

6. Handler invokes CheckpointService for compaction alert check:
   6a. CheckpointService calls ICheckpointRepository.get_latest_unacknowledged()
   6b. FilesystemCheckpointRepository scans .jerry/checkpoints/ for unacknowledged files
   6c. If unacknowledged checkpoint found:
       6c-i.   Populate <compaction-alert> template (~280 tokens)
       6c-ii.  Call ICheckpointRepository.acknowledge(checkpoint_id)
   6d. If no unacknowledged checkpoint: return empty

7. Handler invokes existing quality reinforcement (enforcement infrastructure):
   7a. PromptReinforcementEngine reads .context/rules/ L2-REINJECT markers
   7b. Sorts by rank, assembles within 600-token budget
   7c. Returns <quality-reinforcement> tag

8. Handler combines all outputs:
   additionalContext = join([
     <quality-reinforcement>...</quality-reinforcement>,   # ~600 tokens
     <context-monitor>...</context-monitor>,               # 40-200 tokens
     <compaction-alert>...</compaction-alert>,              # 0 or ~280 tokens
   ])

9. CLI returns JSON to stdout: {hookSpecificOutput: {additionalContext: combined}}
10. Wrapper pipes stdout to Claude Code
11. Wrapper exits 0 (always -- fail-open)

Error handling at each step:
- Step 5 fails: log to stderr, skip <context-monitor>, proceed to step 6
- Step 6 fails: log to stderr, skip <compaction-alert>, proceed to step 7
- Step 7 fails: log to stderr, skip <quality-reinforcement>, proceed to step 8
- All fail: output empty additionalContext (existing behavior preserved)
- Subprocess timeout: wrapper exits 0 with no output (Claude Code ignores)
```

### Data Flow: `jerry hooks session-start` (SessionStart)

```
1. Claude Code fires SessionStart event
2. hooks.json routes to hooks/session-start.py (10000ms timeout)
   NOTE: Replaces the existing scripts/session_start_hook.py (300+ lines).
   The old script is retired; the new thin wrapper follows the same pattern
   as hooks/user-prompt-submit.py. Existing logic (project context query,
   quality context generation) moves into the jerry hooks session-start
   CLI command, wired through bootstrap.py.
3. Wrapper reads stdin, calls: uv run jerry --json hooks session-start

4. Handler invokes existing project context query:
   4a. Dispatches RetrieveProjectContextQuery
   4b. Returns <project-context> tag (~200 tokens)

5. Handler invokes existing quality context generation:
   5a. SessionQualityContextGenerator generates <quality-context> tag (~700 tokens)

6. Handler invokes CheckpointService + ResumptionContextGenerator for resumption context:
   6a. CheckpointService calls ICheckpointRepository.get_latest_unacknowledged()
   6b. If no unacknowledged checkpoint: return empty (no resumption needed)
   6c. If found: CheckpointService returns CheckpointData (includes resumption_state
       from ORCHESTRATION.yaml and session_info with abandon reason from CWI-00
       FileSystemSessionRepository)
   6d. ResumptionContextGenerator.generate(checkpoint_data) produces
       <resumption-context> XML (~760 tokens):
       - Recovery state summary
       - Quality trajectory (QG score, iteration count)
       - Key decisions from decision log
       - Agent summary states
       - File read instructions (priority-ordered)
       - Previous session abandon reason
       - Compaction event history

7. Combine outputs:
   additionalContext = join([
     <project-context>...</project-context>,       # ~200 tokens
     <quality-context>...</quality-context>,        # ~700 tokens
     <resumption-context>...</resumption-context>,  # 0 or ~760 tokens
   ])

8. Return JSON to stdout
9. Exit 0 (always)
```

### Data Flow: `jerry hooks pre-compact` (PreCompact)

```
1. Claude Code fires PreCompact event (before context compaction)
2. hooks.json routes to hooks/pre-compact.py (10000ms timeout)
3. Wrapper reads stdin, calls: uv run jerry --json hooks pre-compact

4. Handler invokes CheckpointService:
   4a. CheckpointService determines next checkpoint ID:
       - Calls ICheckpointRepository.list_all()
       - Next ID = max(sequence) + 1 (or 001 if empty)
   4b. Reads ORCHESTRATION.yaml resumption section (if exists):
       - Recovery state fields
       - Quality trajectory
       - Decision log
       - Agent summaries
   4c. Reads current context state:
       - Calls ContextFillEstimator for FillEstimate
   4d. Assembles CheckpointData:
       {
         checkpoint_id: "cx-{NNN}",
         timestamp: ISO 8601,
         compaction_sequence: NNN,
         context_state: FillEstimate,
         resumption_state: { ... from ORCHESTRATION.yaml ... },
         session_info: { project_id, branch, working_directory }
       }
   4e. Calls ICheckpointRepository.save(checkpoint_data)
       - FilesystemCheckpointRepository writes via AtomicFileAdapter
       - Creates .jerry/checkpoints/ directory if missing

5. Handler triggers session abandon:
   5a. Dispatches AbandonSessionCommand(reason="context compaction at {fill}%")
   5b. FileSystemSessionRepository persists SessionAbandoned event
   5c. If no active session: log warning, continue (fail-open)

6. Return JSON: {systemMessage: "Checkpoint cx-{NNN} saved at {fill}% context fill"}
7. Exit 0 (always)

Error handling:
- ORCHESTRATION.yaml not found: checkpoint contains context_state only
- Directory creation fails: log error, exit 0 with empty response
- Session abandon fails: log warning, checkpoint still written
- AtomicFileAdapter write fails: log error, exit 0 with empty response
```

### Data Flow: `jerry hooks pre-tool-use` (PreToolUse)

```
1. Claude Code fires PreToolUse event (before Write|Edit|MultiEdit|Bash)
2. hooks.json routes to hooks/pre-tool-use.py (5000ms timeout)
3. Wrapper reads stdin, calls: uv run jerry --json hooks pre-tool-use

4. Handler invokes existing architecture validation:
   4a. PreToolEnforcementEngine validates tool call against architecture rules
   4b. Returns enforcement decision (allow/warn/reject)

5. Handler invokes resumption staleness detection:
   5a. If tool call targets ORCHESTRATION.yaml:
       5a-i.  Parse resumption.updated_at field
       5a-ii. Check if updated_at is current (within current phase)
       5a-iii. If stale: inject staleness warning
   5b. If tool call does not target ORCHESTRATION.yaml: passthrough

6. Combine enforcement decision with staleness warning (if any)
7. Return enforcement decision JSON
8. Exit 0 (always)
```

### Interface Contracts

#### Value Objects

```python
# src/context_monitoring/domain/value_objects/threshold_tier.py
from enum import Enum

class ThresholdTier(Enum):
    """Context fill severity level.

    Ordered by increasing severity. Each tier maps to a configured
    threshold percentage and triggers different response behaviors.
    """
    NOMINAL = "nominal"      # Below 55% -- normal operation
    LOW = "low"              # 55-70% -- tracking only
    WARNING = "warning"      # 70-80% -- recommended actions
    CRITICAL = "critical"    # 80-88% -- urgent actions + checkpoint reminder
    EMERGENCY = "emergency"  # Above 88% -- immediate preservation protocol
```

```python
# src/context_monitoring/domain/value_objects/fill_estimate.py
from dataclasses import dataclass
from .threshold_tier import ThresholdTier

@dataclass(frozen=True, slots=True)
class FillEstimate:
    """Immutable snapshot of context fill state.

    Attributes:
        fill_percentage: Context fill as a ratio (0.0 to 1.0)
        input_tokens: Raw token count from transcript
        context_window_size: Total context window capacity
        threshold_tier: Current severity level
    """
    fill_percentage: float
    input_tokens: int
    context_window_size: int
    threshold_tier: ThresholdTier
```

```python
# src/context_monitoring/domain/value_objects/checkpoint_data.py
from dataclasses import dataclass
from typing import Any
from .fill_estimate import FillEstimate

@dataclass(frozen=True, slots=True)
class CheckpointData:
    """Immutable snapshot of session state at compaction.

    Attributes:
        checkpoint_id: Unique identifier (e.g., "cx-003")
        timestamp: ISO 8601 creation timestamp
        compaction_sequence: Sequential compaction number in session
        context_state: Fill estimate at time of compaction
        resumption_state: Data from ORCHESTRATION.yaml (None if unavailable)
        session_info: Project and environment metadata
    """
    checkpoint_id: str
    timestamp: str
    compaction_sequence: int
    context_state: FillEstimate
    resumption_state: dict[str, Any] | None
    session_info: dict[str, Any]
```

#### Application Ports

```python
# src/context_monitoring/application/ports/transcript_reader.py
from typing import Protocol

class ITranscriptReader(Protocol):
    """Port for reading transcript token data.

    Implementations parse transcript files to extract the latest
    input_tokens value for context fill estimation.
    """
    def read_latest_tokens(self, transcript_path: str) -> int:
        """Read the most recent input_tokens value from the transcript.

        Args:
            transcript_path: Path to the transcript JSONL file

        Returns:
            The input_tokens value from the latest transcript entry

        Raises:
            FileNotFoundError: If transcript_path does not exist
            ValueError: If transcript file is empty or unparseable
        """
        ...
```

```python
# src/context_monitoring/application/ports/checkpoint_repository.py
from pathlib import Path
from typing import Protocol
from src.context_monitoring.domain.value_objects.checkpoint_data import CheckpointData

class ICheckpointRepository(Protocol):
    """Port for checkpoint persistence operations.

    Implementations manage checkpoint files for pre-compaction
    state capture and post-compaction resumption.
    """
    def save(self, data: CheckpointData) -> Path:
        """Persist a checkpoint.

        Args:
            data: The checkpoint data to persist

        Returns:
            Path to the created checkpoint file
        """
        ...

    def get_latest_unacknowledged(self) -> CheckpointData | None:
        """Retrieve the most recent unacknowledged checkpoint.

        Returns:
            CheckpointData if an unacknowledged checkpoint exists, None otherwise
        """
        ...

    def acknowledge(self, checkpoint_id: str) -> None:
        """Mark a checkpoint as acknowledged.

        Args:
            checkpoint_id: The checkpoint ID to acknowledge (e.g., "cx-003")
        """
        ...

    def list_all(self) -> list[CheckpointData]:
        """List all checkpoints, ordered by compaction_sequence.

        Returns:
            List of all checkpoint data, oldest first
        """
        ...
```

```python
# src/context_monitoring/application/ports/threshold_configuration.py
from typing import Protocol

class IThresholdConfiguration(Protocol):
    """Port for reading context monitoring threshold configuration.

    Implementations bridge to the configuration infrastructure
    (e.g., LayeredConfigAdapter) for threshold values.
    """
    def get_threshold(self, tier: str) -> float:
        """Get the threshold percentage for a given tier.

        Args:
            tier: Tier name (e.g., "warning", "critical", "emergency")

        Returns:
            Threshold as a float ratio (0.0 to 1.0)
        """
        ...

    def is_enabled(self) -> bool:
        """Check if context monitoring is enabled.

        Returns:
            True if context monitoring is active
        """
        ...
```

#### Application Services

```python
# src/context_monitoring/application/services/resumption_context_generator.py
from src.context_monitoring.domain.value_objects.checkpoint_data import CheckpointData


class ResumptionContextGenerator:
    """Generates <resumption-context> XML for session-start injection.

    Follows the same generator pattern as SessionQualityContextGenerator.
    Consumes checkpoint data and ORCHESTRATION.yaml resumption fields to
    compose a structured XML tag within the ~760 token budget.
    """

    def generate(self, checkpoint: CheckpointData) -> str:
        """Generate resumption context XML from checkpoint data.

        Composes the <resumption-context> XML tag containing:
        - Recovery state summary (checkpoint_id, compaction_sequence, fill_percentage)
        - Quality trajectory (QG score, iteration count) from resumption_state
        - Key decisions from decision log
        - Agent summary states
        - File read instructions (priority-ordered) from resumption_state
        - Previous session abandon reason from session_info
        - Compaction event history

        Args:
            checkpoint: The unacknowledged checkpoint data to format

        Returns:
            XML string for injection into session-start additionalContext.
            Empty string if checkpoint contains no resumption data.
        """
        ...
```

### Token Budget Analysis

Carried forward from ADR-SPIKE002-001 (unchanged by architectural choice):

| Hook | Component | Budget (tokens) | Frequency |
|------|-----------|----------------|-----------|
| SessionStart | `<project-context>` [EXISTING] | ~200 | Once per session |
| SessionStart | `<quality-context>` [EXISTING] | ~700 | Once per session |
| SessionStart | `<resumption-context>` [NEW] | ~760 | Once per session (if checkpoint exists) |
| UserPromptSubmit | `<quality-reinforcement>` [EXISTING] | ~600 | Every prompt |
| UserPromptSubmit | `<context-monitor>` [NEW] | 40-200 | Every prompt |
| UserPromptSubmit | `<compaction-alert>` [NEW] | 0 or ~280 | Once after compaction |

**Worst-case per-prompt injection (UserPromptSubmit):** 600 + 200 + 280 = 1,080 tokens. Occurs only on the first prompt after a compaction event. Normal operation: 600 + 40 = 640 tokens (NOMINAL tier).

**Session start injection:** 200 + 700 + 760 = 1,660 tokens (with resumption). Without resumption: 900 tokens (existing behavior unchanged).

**Total enforcement budget impact:** ~15,100 tokens (current) + ~1,860 tokens (worst-case context resilience) = ~16,960 tokens (8.5% of 200K context window).

---

## L2 Strategic Implications

### Impact on Hexagonal Architecture

This decision aligns context monitoring with the codebase's established hexagonal pattern. After implementation, the architecture consistency looks like this:

| Bounded Context | Domain Layer | Application Layer | Infrastructure Layer | Composition Root | CLI Commands |
|----------------|-------------|-------------------|---------------------|-----------------|-------------|
| `session_management` | Aggregates, events, value objects | Commands, queries, handlers, ports | Adapters (filesystem, in-memory, OS env) | `bootstrap.py` | `jerry session start\|end\|status\|abandon` |
| `work_tracking` | Aggregates, events, value objects, services | Commands, queries, handlers, ports | Adapters (event-sourced, in-memory), persistence (filesystem, in-memory) | `bootstrap.py` | `jerry items list\|show\|create\|start\|complete\|block\|cancel` |
| `context_monitoring` [NEW] | Value objects, events | Services, ports | Adapters (JSONL reader, filesystem checkpoint, config bridge) | `bootstrap.py` | `jerry hooks prompt-submit\|session-start\|pre-compact\|pre-tool-use` |
| `transcript` | -- | Commands, handlers, services | Adapters (VTT parser) | `bootstrap.py` | `jerry transcript parse` |
| `infrastructure/internal/enforcement` [TECH DEBT] | **None** | **None** | Engines (flat structure, 7 files) | **None** (direct import) | **None** (bypasses CLI) |

The enforcement folder becomes the sole remaining exception to hexagonal architecture. Its remediation is tracked as a separate enabler (D-004).

### Impact on 5-Layer Enforcement Architecture

Context resilience extends three of the five enforcement layers:

| Layer | Current Function | Added Function | Implementation Path |
|-------|-----------------|----------------|-------------------|
| L1 (Session Start) | Quality framework preamble (`<quality-context>`) | Resumption context (`<resumption-context>`) | `jerry hooks session-start` -> `CheckpointService` -> `ICheckpointRepository` |
| L2 (Every Prompt) | Quality reinforcement (`<quality-reinforcement>`) | Context monitoring (`<context-monitor>`) + compaction alert (`<compaction-alert>`) | `jerry hooks prompt-submit` -> `ContextFillEstimator` + `CheckpointService` |
| L3 (Pre-Tool-Call) | AST architecture validation, governance escalation | Resumption staleness detection | `jerry hooks pre-tool-use` -> staleness check on ORCHESTRATION.yaml writes |
| L4 (After Tool Calls) | Unchanged | Unchanged | -- |
| L5 (Commit/CI) | Unchanged | Unchanged | -- |

The enforcement layers are extended, not modified. The total enforcement token budget increases from ~15,100 to ~16,960 tokens.

### Enforcement Tech Debt Migration Path (D-004)

The existing `src/infrastructure/internal/enforcement/` folder contains 7 files:

```
enforcement_decision.py
enforcement_rules.py
pre_tool_enforcement_engine.py      (567 lines)
prompt_reinforcement_engine.py      (246 lines)
quality_context.py
reinforcement_content.py
session_quality_context_generator.py (134 lines)
```

D-004 tracks this as a separate enabler, not part of FEAT-001. The migration path:

1. **Phase 1 (FEAT-001 scope):** Build `context_monitoring` as a proper bounded context. Create `jerry hooks` commands. New hooks use CLI-first pattern. Existing hooks remain unchanged (still import enforcement engines directly).

2. **Phase 2 (separate enabler):** Extract enforcement engines into a proper bounded context (e.g., `src/quality_enforcement/`). Migrate existing hooks to call `jerry hooks` commands. Wire through `bootstrap.py`. Delete enforcement folder.

3. **Phase 3 (optional):** Consolidate all hook-related CLI commands under `jerry hooks`. Move enforcement-specific logic into `jerry hooks pre-tool-use` and `jerry hooks prompt-submit`.

### Future CLI Command Surface Evolution

After FEAT-001 and the enforcement enabler, the CLI surface would be:

```
jerry session start|end|status|abandon   # Session management
jerry items list|show|create|...         # Work tracking
jerry projects list|context|validate     # Project management
jerry config get|set|show                # Configuration
jerry hooks prompt-submit                # Per-prompt hook (context + quality)
jerry hooks session-start                # Session start hook (project + quality + resumption)
jerry hooks pre-compact                  # Pre-compaction hook (checkpoint + session abandon)
jerry hooks pre-tool-use                 # Pre-tool hook (architecture + staleness)
jerry transcript parse                   # Transcript parsing
```

All operations go through the CLI. All logic is wired through `bootstrap.py`. All commands are testable via `jerry --json`.

---

## Evidence

### Superseded Document

| Document | Path |
|----------|------|
| ADR-SPIKE002-001 (original, superseded) | `orchestration/spike002-cli-integration-20260219-001/res/phase-3-architecture/architecture-designer/adr-cli-integration.md` |

### Phase 1 Audit Traceability

| ADR Claim | Phase 1 Audit Section | Specific Evidence |
|-----------|----------------------|-------------------|
| PromptReinforcementEngine is the pattern for context injection | C4: Enforcement Engine Infrastructure | L2 engine, 246 lines, L2-REINJECT parsing, 600-token budget, fail-open design |
| SessionQualityContextGenerator is the pattern for resumption injection | C4: Enforcement Engine Infrastructure | L1 engine, 134 lines, XML preamble, ~700 token budget |
| PreToolEnforcementEngine is the pattern for staleness detection | C4: Enforcement Engine Infrastructure | L3 engine, 567 lines, governance escalation detection (lines 501-536) |
| LayeredConfigAdapter replaces custom threshold config | C3: Configuration Management | 4-level precedence (env > project > root > defaults), TOML, dot-notation, CLI commands operational |
| AtomicFileAdapter for safe checkpoint writes | C6: Local Context Persistence | Safe file I/O with locking, reusable |
| FileSystemEventStore pattern for directory creation | C6: Local Context Persistence | `mkdir(parents=True, exist_ok=True)` at lines 106-108 |
| InMemorySessionRepository not persistent across processes | C2: Session Lifecycle Management | Line 35: "Loses data on process termination" |
| SessionAbandoned event designed for compaction | C2: Session Lifecycle Management | session.py line 207: "typically due to context compaction or unexpected termination" |
| UserPromptSubmit hook has 5000ms timeout | C5: Hook Integration Points | `hooks.json`: UserPromptSubmit timeout = 5000 |
| SessionStart hook proves CLI subprocess works | C5: Hook Integration Points | `session_start_hook.py` line 270: calls `jerry --json projects context` within 10s timeout |
| No PreCompact hook registered | C5: Hook Integration Points | `hooks.json` contains only SessionStart, UserPromptSubmit, PreToolUse, SubagentStop |
| ECW status line data unavailable to hooks (GAP-003) | C8: ECW Status Line | Status line uses `statusLine.command` mechanism, not hooks mechanism |
| 10 of 14 items classified as EXTEND or REUSE | Mapping to SPIKE-001 Items | 1 REUSE (#7), 10 EXTEND (#1-3, #6, #8-12), 3 NEW (#4, #5, #13-14) |

### Phase 2 Gap Analysis Traceability

| ADR Claim | Gap Analysis Section | Specific Evidence |
|-----------|---------------------|-------------------|
| 14 items consolidate to 9 (now 10 with CWI-00) | L0 Summary, Consolidation Analysis | 4 merges: #1+#3, #4+#5, #2+#10, #13+#14 |
| InMemorySessionRepository is highest architectural risk | L2: Risk Analysis, R1 | Rated HIGH, immediate mitigation: file-based state (now: CWI-00 eliminates) |
| New bounded context `context_monitoring` recommended | L2: Architectural Integration | Distinct domain language, different lifecycle, independent evolution |
| 5000ms timeout budget analysis | L2: Risk Analysis, R3 | Budget: 1000ms + 1500ms + 500ms = 3000ms, 2000ms headroom |
| Method C timing dependency | L2: Risk Analysis, R5 | One-prompt lag, acceptable with Method A as primary |

### DISC-001 Traceability

| ADR Claim | DISC-001 Finding | Evidence |
|-----------|-----------------|----------|
| 3 of 4 hooks bypass CLI | F1: Two Incompatible Execution Paths | Hook audit table: UserPromptSubmit imports PromptReinforcementEngine directly; PreToolUse imports PreToolEnforcementEngine directly; SubagentStop uses local functions only |
| Enforcement folder is tech debt | F2: Enforcement Folder is Architectural Tech Debt | Comparison table: enforcement has no domain layer, no ports, no adapters, no composition root wiring, no CLI testability |
| ADR-SPIKE002-001 rejection of Alt 3 invalid | F3: Invalid Rejection Reasoning | Subprocess concern addressed by single CLI call per event; InMemorySessionRepository concern eliminated by CWI-00 |
| scripts/hooks split creates confusion | F4: scripts/ vs hooks/ Split | Hook implementations scattered across two directories with no clear rationale |

### DEC-001 Traceability

| ADR Decision | DEC-001 Decision | Status |
|-------------|-----------------|--------|
| Hooks call CLI via subprocess | D-001: Hooks Call CLI, Not Import Modules | Pending user acceptance |
| `src/context_monitoring/` bounded context | D-002: Context Monitoring is a Proper Bounded Context | Pending user acceptance |
| `jerry hooks <event>` command namespace | D-003: CLI Gets `jerry hooks` Command Namespace | Pending user acceptance |
| Enforcement tech debt tracked separately | D-004: Enforcement Tech Debt Tracked Separately | Pending user acceptance |

### Codebase Architecture Evidence

| Claim | Source | Evidence |
|-------|--------|----------|
| `session_management` has proper hexagonal layers | Directory listing | 36 Python files: domain/ (aggregates, events, value_objects, entities, exceptions), application/ (commands, queries, handlers, ports), infrastructure/ (adapters) |
| `work_tracking` has proper hexagonal layers | Directory listing | 42 Python files: domain/ (aggregates, events, value_objects, services, ports), application/ (commands, queries, handlers, ports), infrastructure/ (adapters, persistence) |
| Enforcement folder is flat with 7 files | Directory listing | `src/infrastructure/internal/enforcement/`: __init__.py, enforcement_decision.py, enforcement_rules.py, pre_tool_enforcement_engine.py, prompt_reinforcement_engine.py, quality_context.py, reinforcement_content.py, session_quality_context_generator.py |
| Composition root wires all bounded contexts | `src/bootstrap.py` | `create_query_dispatcher()` wires session_management and work_tracking handlers. `create_command_dispatcher()` wires session and work item commands. Module-level singletons for repositories. |
| `FileSystemEventStore` + `EventSourcedWorkItemRepository` pattern is proven | `src/work_tracking/infrastructure/` | FileSystemEventStore (369 lines, JSONL, FileLock), EventSourcedWorkItemRepository (431 lines, event registry, stream ID convention, aggregate reconstitution) |
| CLI adapter receives dispatchers via constructor injection | `src/interface/cli/adapter.py` | `CLIAdapter.__init__` takes `dispatcher: IQueryDispatcher`, `command_dispatcher: ICommandDispatcher`. No infrastructure imports. |

---

## Self-Review (S-010) Verification

- [x] All 4 alternatives analyzed with honest pros/cons. Each rejected alternative has a steelman (S-003, H-16) presenting its strongest case before rejection.
- [x] DISC-001 findings (F1-F4) are explicitly addressed: F1 resolved by CLI-first hooks, F2 resolved by proper bounded context, F3 resolved by choosing Alternative 3 with corrected analysis, F4 resolved by thin wrapper scripts replacing scattered hook implementations.
- [x] DEC-001 decisions (D-001 through D-004) are implemented in the chosen architecture. Each decision is traceable to a specific architectural element.
- [x] Consequences include 5 genuine negatives: subprocess overhead, two styles coexist, more initial effort, cross-context aggregation, indirection layer. Each has documented mitigation.
- [x] Interface contracts specified for 3 value objects, 3 ports, and 1 application service (ResumptionContextGenerator) with type hints and docstrings (H-11, H-12).
- [x] Data flow diagrams provided for all 4 hook events with step-by-step processing and error handling.
- [x] Token budget analysis carried forward from ADR-SPIKE002-001 (unchanged by architectural choice).
- [x] L2 Strategic Implications cover: hexagonal architecture alignment table, enforcement layer extension table, enforcement tech debt migration path (3 phases), future CLI command surface.
- [x] Evidence section provides traceability to Phase 1 Audit, Phase 2 Gap Analysis, DISC-001, DEC-001, direct codebase evidence, and superseded ADR-SPIKE002-001 path.
- [x] Navigation table present with anchor links (H-23/H-24).
- [x] Status marked as PROPOSED per P-020 (user authority).
- [x] Supersession of ADR-SPIKE002-001 is explicitly documented with rationale and source path.
- [x] No deception about negative consequences or trade-offs (P-022/H-03).
- [x] H-10 compliance: domain events split into one class per file (context_threshold_reached.py, compaction_detected.py, checkpoint_created.py).
- [x] Session-start data flow references new thin wrapper `hooks/session-start.py`, replacing old `scripts/session_start_hook.py` per D-001.
- [x] Subprocess timing correctly labeled as "estimated" (not "measured") per evidence accuracy standards.

### QG-2 Revision History

| Iteration | Score | Verdict | Revisions Applied |
|-----------|-------|---------|-------------------|
| 1 | 0.89 | REVISE | -- (initial scoring) |
| 2 | (pending) | (pending) | REV-001 (H-10 event files split), REV-002 (ResumptionContextGenerator defined), REV-003 (session-start wrapper clarified), DEF-006 (ADR-SPIKE002-001 path added), DEF-007 (subprocess timing corrected to "estimated") |
