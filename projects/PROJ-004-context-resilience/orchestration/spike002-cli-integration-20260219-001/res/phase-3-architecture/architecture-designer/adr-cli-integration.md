# ADR-SPIKE002-001: CLI-Integrated Context Resilience Architecture

<!-- PS-ID: SPIKE-002 | ENTRY-ID: phase-3 | DATE: 2026-02-19 -->
<!-- AGENT: ps-architect v2.0.0 | MODEL: claude-opus-4-6 -->

> Architecture Decision Record for integrating context resilience with the Jerry CLI infrastructure rather than building parallel hook-only implementations.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Status](#status) | Decision lifecycle state |
| [Context](#context) | Problem background and forces |
| [Decision](#decision) | Chosen architectural approach |
| [Alternatives Considered](#alternatives-considered) | Four options analyzed with pros/cons |
| [Consequences](#consequences) | Positive, negative, and neutral outcomes |
| [L0 Summary](#l0-summary) | Executive summary (5 bullets) |
| [L1 Technical Details](#l1-technical-details) | Component diagrams, data flows, interface contracts |
| [L2 Strategic Implications](#l2-strategic-implications) | Future bounded context extraction, enforcement architecture impact |
| [Evidence](#evidence) | Traceability to Phase 1 audit and Phase 2 gap analysis |

---

## Status

**PROPOSED** -- Pending review. This ADR was produced during SPIKE-002 Phase 3 (Architecture Design) as part of the PROJ-004 context resilience project.

---

## Context

### Problem Statement

SPIKE-001 designed a context resilience system (context fill monitoring, pre-compaction checkpointing, post-compaction resumption) using a hook-only approach. The design produced 14 follow-up work items estimated at 25-37 hours. The SPIKE-001 design treated the Jerry CLI as a black box and proposed building all detection, checkpointing, and injection logic from scratch within hook scripts.

SPIKE-002 Phase 1 (CLI Capability Audit) discovered that the Jerry CLI has substantial existing infrastructure directly relevant to context resilience:

- **LayeredConfigAdapter** (C3): 4-level hierarchical configuration with TOML parsing, dot-notation keys, and CLI management -- a direct replacement for the proposed threshold configuration file (Phase 1 Audit: C3, `layered_config_adapter.py`, 383 lines).
- **PromptReinforcementEngine** (C4): L2 per-prompt injection engine with L2-REINJECT marker parsing, rank-based sorting, and 600-token budget -- the proven pattern for context monitor injection (Phase 1 Audit: C4, `prompt_reinforcement_engine.py`, 246 lines).
- **SessionQualityContextGenerator** (C4): L1 session-start XML preamble generator with ~700 token budget -- the pattern for resumption context injection (Phase 1 Audit: C4, `session_quality_context_generator.py`, 134 lines).
- **PreToolEnforcementEngine** (C4): L3 AST-based validation with governance escalation detection -- the pattern for resumption staleness detection (Phase 1 Audit: C4, `pre_tool_enforcement_engine.py`, 567 lines).
- **AtomicFileAdapter** (C6): Safe file I/O with locking -- reusable for checkpoint writes (Phase 1 Audit: C6, `atomic_file_adapter.py`).
- **FileSystemEventStore** (C6): JSONL append-only store with file locking and directory creation patterns -- applicable to checkpoint infrastructure (Phase 1 Audit: C6, `filesystem_event_store.py`, 369 lines).

SPIKE-002 Phase 2 (Gap Analysis) confirmed that 10 of 14 SPIKE-001 items can leverage existing CLI infrastructure (1 REUSE, 10 EXTEND, 3 NEW), reducing the work from 14 items to 9 consolidated items and saving an estimated 18-28% effort.

### Forces

1. **Effort efficiency.** Building from scratch ignores proven, tested infrastructure. Reusing existing engines, adapters, and patterns reduces both development time and defect risk.

2. **Pattern consistency.** The CLI enforcement engines follow a common architecture: stateless classes, file-based I/O, fail-open error handling, token-budgeted output. New context resilience components that follow this pattern integrate naturally. Deviating creates maintenance burden.

3. **Process boundary isolation.** Each hook execution and each CLI invocation is a separate Python process. The `InMemorySessionRepository` loses state on process termination (Phase 1 Audit: `in_memory_session_repository.py` line 35: "Loses data on process termination"). This constrains any design that assumes shared in-memory state.

4. **Domain maturity.** Context monitoring introduces new domain concepts (ContextThreshold, FillEstimate, CompactionEvent) that do not yet have proven boundaries. Premature bounded context extraction risks misplaced abstractions.

5. **5-layer enforcement architecture integrity.** The existing L1-L5 enforcement layers (ADR-EPIC002-002) define where detection and injection happen. Context resilience must fit within this architecture, not bypass it.

---

## Decision

**Integrate context resilience with the existing CLI infrastructure** using a two-phase approach:

### Phase 1: Infrastructure Placement (Immediate -- FEAT-001 scope)

Place new context resilience engines in `src/infrastructure/internal/enforcement/` alongside existing enforcement engines. New engines follow the same stateless, fail-open, token-budgeted pattern established by `PromptReinforcementEngine`, `SessionQualityContextGenerator`, and `PreToolEnforcementEngine`.

**Specific placements:**

| Component | Location | Pattern Source |
|-----------|----------|----------------|
| `ContextMonitorEngine` | `src/infrastructure/internal/enforcement/context_monitor_engine.py` | `PromptReinforcementEngine` (L2 injection) |
| `CompactionAlertEngine` | `src/infrastructure/internal/enforcement/compaction_alert_engine.py` | `PromptReinforcementEngine` (L2 injection) |
| `CheckpointWriter` | `src/infrastructure/internal/enforcement/checkpoint_writer.py` | `FileSystemEventStore` (file persistence) |
| `ResumptionContextGenerator` | `src/infrastructure/internal/enforcement/resumption_context_generator.py` | `SessionQualityContextGenerator` (L1 injection) |
| Threshold configuration | `LayeredConfigAdapter` defaults in `adapter.py` | Existing config infrastructure (REUSE) |

**Cross-process state is file-based.** All state that must persist across hook invocations uses filesystem persistence:
- Transcript JSONL (`$TRANSCRIPT_PATH`) -- already persistent, read by `ContextMonitorEngine`.
- Checkpoint files (`.jerry/checkpoints/cx-{NNN}-checkpoint.json`) -- written by `CheckpointWriter`, read by `CompactionAlertEngine` and `ResumptionContextGenerator`.
- Configuration (`.jerry/config.toml`) -- managed by `LayeredConfigAdapter`, read by all engines.
- Acknowledgment markers (`.jerry/checkpoints/cx-{NNN}-checkpoint.json.acknowledged`) -- written by `CompactionAlertEngine`.

**Session domain events are deferred.** The `SessionAbandoned` event with reason field exists (Phase 1 Audit: C2, `session.py` line 207) but cannot be triggered cross-process due to `InMemorySessionRepository`. Compaction is recorded in checkpoint files, not as session events.

### Phase 2: Bounded Context Extraction (Deferred -- post-FEAT-001)

When the context monitoring domain model stabilizes through FEAT-001 implementation, extract from `infrastructure/internal/enforcement/` into a full `src/context_monitoring/` bounded context with domain, application, and infrastructure layers. The extraction criteria are:

1. Domain concepts (ThresholdTier, FillEstimate, CheckpointFile) have proven stable through at least one full implementation cycle.
2. A persistent session repository is available, enabling domain event integration.
3. The boundary between `context_monitoring` and `session_management` is empirically validated.

---

## Alternatives Considered

### Alternative 1: Hook-Only Implementation (SPIKE-001 Original)

**Description:** Build all context resilience logic from scratch within hook scripts. Each hook self-contains its own configuration parsing, state management, threshold logic, and injection formatting. No imports from the Jerry CLI codebase.

**Pros:**
- Complete isolation from CLI internals -- hooks are standalone scripts with no coupling.
- Simpler mental model: each hook script is self-contained and readable without understanding the CLI architecture.
- No risk of breaking existing CLI behavior through new imports or modifications.
- Faster initial prototyping -- no need to understand existing engine patterns.

**Cons:**
- Duplicates configuration management (custom JSON config vs. `LayeredConfigAdapter` with env/project/root/defaults precedence and CLI commands already operational).
- Duplicates file I/O patterns (custom writes vs. `AtomicFileAdapter` with file locking already tested).
- Duplicates token estimation logic (custom counting vs. existing `chars/4 * 0.83` calibration or tiktoken `p50k_base` `TokenCounter`).
- 14 work items at 25-37 hours vs. 9 items at 18-26 hours (Phase 2 Gap Analysis: Effort Summary).
- Inconsistent patterns: new hook logic would not follow the established enforcement engine architecture, creating two parallel systems.
- No path to bounded context extraction: standalone scripts cannot evolve into a structured domain.

**Why rejected:** The evidence from Phase 1 Audit shows that 10 of 14 items either directly reuse or extend existing infrastructure. Building from scratch wastes proven, tested code and creates a maintenance burden of two parallel systems.

### Alternative 2: CLI-Integrated (CHOSEN)

**Description:** Integrate with existing CLI infrastructure. New engines follow the `PromptReinforcementEngine` / `SessionQualityContextGenerator` / `PreToolEnforcementEngine` patterns. Configuration uses `LayeredConfigAdapter`. File I/O uses `AtomicFileAdapter`. Placement in `src/infrastructure/internal/enforcement/`. Two-phase migration to bounded context when domain stabilizes.

**Pros:**
- 18-28% effort reduction (Phase 2 Gap Analysis: 9 items at 18-26 hours vs. 14 items at 25-37 hours).
- Consistent enforcement engine patterns: stateless, fail-open, token-budgeted.
- `LayeredConfigAdapter` provides hierarchical overrides (env > project > root > defaults) for free, including `jerry config get/set` CLI commands.
- Proven fail-open patterns reduce reliability risk (Phase 1 Audit: all three existing engines use fail-open design).
- Clear migration path from infrastructure placement to bounded context extraction.
- Single hook modification per extension point (e.g., `user-prompt-submit.py` extended once with both engines).

**Cons:**
- Coupling to enforcement layer internals. If `PromptReinforcementEngine` changes its interface, `ContextMonitorEngine` may need updates.
- `InMemorySessionRepository` limitation prevents session domain event integration in Phase 1 (Phase 1 Audit: C2, line 35).
- Hook import latency risk: adding engine imports to `user-prompt-submit.py` increases Python startup overhead within the 5000ms timeout (Phase 2 Gap Analysis: R3).
- Phase 2 extraction requires a migration effort that would not exist if the bounded context were built from the start.

**Why chosen:** The Phase 1 Audit evidence demonstrates that the CLI infrastructure is a direct fit. The effort savings, pattern consistency, and reduced defect risk outweigh the coupling concerns. The two-phase approach defers bounded context complexity until the domain model is validated.

### Alternative 3: New CLI Module (`jerry context`)

**Description:** Add a new `context` namespace to the Jerry CLI with commands like `jerry context status`, `jerry context checkpoint`, `jerry context thresholds`. Hooks would call the CLI (like `session_start_hook.py` calls `jerry --json projects context`) instead of importing engines directly.

**Pros:**
- Clean separation: hooks are thin scripts that call CLI commands, keeping logic in the CLI.
- Full CQRS pattern: context monitoring gets its own commands, queries, and handlers within the CLI architecture.
- CLI commands are independently testable via `jerry --json context status`.
- Natural CLI discoverability: users can inspect context state via command line.

**Cons:**
- Each CLI invocation spawns a new Python process with full `uv run` overhead. The `UserPromptSubmit` hook already has a 5000ms timeout (Phase 1 Audit: `hooks.json`). Adding a subprocess call for every prompt would consume significant budget. The `SessionStart` hook's `uv sync && uv run jerry --json projects context` call takes measurable time (Phase 1 Audit: C5, `session_start_hook.py` line 271).
- The `InMemorySessionRepository` limitation means CLI context state is lost between invocations, requiring file-based state regardless. The CLI module would read/write the same files as the direct-import approach, adding subprocess overhead for no state benefit.
- Premature full CQRS implementation for domain concepts that are not yet validated.
- Higher implementation effort than Alternative 2: requires new CLI adapter methods, routing, command/query classes, and handlers in addition to the core engines.

**Why rejected:** The subprocess overhead per prompt is prohibitive within the 5000ms timeout budget. The `InMemorySessionRepository` limitation means the CLI module cannot offer state benefits over direct engine imports. The added implementation complexity is not justified when direct imports work (proven by `user-prompt-submit.py` importing `PromptReinforcementEngine`).

### Alternative 4: Status Line Integration (Method C as Primary)

**Description:** Use the ECW status line (`statusline.py`) as the primary context data source. Extend the status line's state file (`~/.claude/ecw-statusline-state.json`) to include `context_fill_percentage`, `input_tokens`, and `timestamp`. Hooks read this state file instead of parsing the transcript JSONL. The status line has direct access to `context_window.current_usage.input_tokens` (Phase 1 Audit: C8, lines 403-423), providing exact (not heuristic) context data.

**Pros:**
- Exact context fill data rather than heuristic estimation from transcript `input_tokens`.
- Status line already writes state to a JSON file (Phase 1 Audit: C8, `~/.claude/ecw-statusline-state.json`), so the relay mechanism exists.
- Minimal hook logic: hooks simply read a JSON file rather than parsing JSONL transcripts.
- Compaction detection already implemented in status line (Phase 1 Audit: C8, lines 463-506).

**Cons:**
- **Timing dependency (R5):** The status line updates its state file based on Claude Code's stdin updates. The `UserPromptSubmit` hook fires when the user submits a prompt. The status line data reflects the state _before_ the current prompt, not after. This one-prompt lag means at high fill rates (e.g., 29K tokens per quality gate iteration, per SPIKE-001 calibration), the hook could miss a threshold crossing by one prompt.
- **Unvalidated feasibility:** Whether the status line state file reliably updates before `UserPromptSubmit` fires is an open question (SPIKE-001 OQ-1). Building the entire system on an unvalidated assumption violates engineering rigor.
- **Single point of failure:** If the status line script errors, crashes, or is disabled, all context monitoring fails. Method A (transcript-based) uses a different data path (`$TRANSCRIPT_PATH`), providing redundancy.
- **Coupling to client-side mechanism:** The status line runs via `statusLine.command` in Claude Code settings, not via the hooks mechanism. Changes to Claude Code's status line protocol could silently break context monitoring.
- **User customization risk:** The status line script is user-facing and may be customized, replaced, or disabled. The enforcement engines are framework-internal and under Jerry's control.

**Why rejected:** The timing dependency is a fundamental reliability concern for a system whose purpose is to detect critical thresholds before context exhaustion. Method C should be investigated as a supplementary accuracy upgrade (CWI-08) but not adopted as the primary detection mechanism until OQ-1 is resolved. Alternative 2 uses Method A (transcript-based) as primary, which is proven reliable (each turn's `input_tokens` is captured in the transcript JSONL) even if slightly less precise.

---

## Consequences

### Positive

1. **18-28% effort reduction.** The consolidated work plan reduces from 14 items at 25-37 hours to 9 items at 18-26 hours. The largest savings come from threshold configuration (REUSE: 0.5 hours vs. 1-2 hours), merged work items (5 consolidations saving 2-2.5 hours), and engine pattern reuse (Phase 2 Gap Analysis: Effort Summary).

2. **Consistent enforcement engine patterns.** All four new engines follow the established pattern: stateless class, file-based I/O, fail-open error handling, token-budgeted output. This means the existing test infrastructure, error handling conventions, and performance budgets apply without adaptation. Developers familiar with `PromptReinforcementEngine` can immediately understand `ContextMonitorEngine`.

3. **LayeredConfigAdapter provides hierarchical overrides for free.** Threshold configuration inherits 4-level precedence (env > project > root > defaults), TOML parsing, dot-notation keys, type coercion, and full CLI management (`jerry config get/set/show`) without writing any configuration infrastructure code. Users can override thresholds at any scope (Phase 2 Gap Analysis: Item #7, CWI-01).

4. **Proven fail-open patterns reduce reliability risk.** All three existing enforcement engines use fail-open design where errors return empty/passthrough responses rather than blocking user work (Phase 1 Audit: C4). Context resilience engines inherit this reliability characteristic.

5. **Clear migration path to bounded context.** Phase 1 infrastructure placement allows domain concepts to stabilize empirically before committing to bounded context boundaries. The extraction from `infrastructure/internal/enforcement/` to `src/context_monitoring/{domain,application,infrastructure}/` is a well-defined refactoring step when criteria are met.

### Negative

1. **Coupling to enforcement layer internals.** New engines import from and follow patterns established by existing engines. If the enforcement engine interface changes (e.g., `PromptReinforcementEngine` restructures its output format), context resilience engines may require corresponding updates. This coupling is accepted because the engines share a common architectural purpose (injection into Claude Code hooks).

2. **InMemorySessionRepository limitation constrains session integration.** The `SessionAbandoned` event with reason field (Phase 1 Audit: C2) exists but cannot be triggered from hooks because the session aggregate lives in a different process. Context compaction is recorded in checkpoint files rather than as session domain events. This limits traceability: there is no domain event trail linking compaction events to session lifecycle. The workaround (file-based checkpoint records) is functional but architecturally inferior to domain event integration.

3. **Hook import latency risk (R3).** Adding `ContextMonitorEngine` and `CompactionAlertEngine` imports to `user-prompt-submit.py` increases Python import time within the 5000ms timeout. The mitigation (performance budget: 3000ms for all engines, 2000ms headroom) is based on estimation, not measurement. If the budget is exceeded, Claude Code silently drops the hook output, resulting in no context monitoring for that prompt.

4. **Phase 2 extraction carries future migration cost.** When domain concepts stabilize, extracting from `infrastructure/internal/enforcement/` into a full bounded context requires refactoring inline domain concepts (ThresholdTier enum, FillEstimate data structure) into domain value objects, creating application services, and establishing port/adapter interfaces. This cost would not exist if the bounded context were built from the start -- but the risk of premature abstraction is judged higher than the migration cost.

### Neutral

1. **Two-phase migration path.** The decision to place engines in infrastructure first and extract to a bounded context later is a deliberate deferral, not an oversight. The extraction criteria (domain stability, persistent repository, validated boundaries) are explicit and measurable.

2. **Process boundary isolation remains a design constraint.** All state that crosses process boundaries (hook-to-hook, hook-to-CLI) must be file-based. This is not new -- the existing enforcement architecture already operates under this constraint. Context resilience simply adds more files to the same pattern.

3. **File-based acknowledgment for compaction alerts.** The `CompactionAlertEngine` marks checkpoint files as acknowledged via filesystem markers (`.acknowledged` file) rather than domain events. This is a pragmatic choice given the `InMemorySessionRepository` limitation. When a persistent repository is available, acknowledgment can be modeled as a domain event.

---

## L0 Summary

1. **Context resilience integrates with existing CLI infrastructure rather than building parallel systems.** The Phase 1 Audit discovered 7 directly applicable CLI capabilities; 10 of 14 SPIKE-001 items extend or reuse existing code.

2. **Four new enforcement engines are placed in `infrastructure/internal/enforcement/` alongside existing engines.** `ContextMonitorEngine` (L2 context fill monitoring), `CompactionAlertEngine` (L2 post-compaction alert), `CheckpointWriter` (PreCompact checkpoint creation), and `ResumptionContextGenerator` (L1 resumption context). All follow the established stateless, fail-open, token-budgeted pattern.

3. **Effort reduces from 14 items / 25-37 hours to 9 items / 18-26 hours (18-28% savings).** Savings come from configuration reuse (`LayeredConfigAdapter`), work item consolidation (5 merges), and engine pattern reuse.

4. **All cross-process state uses file-based persistence.** The `InMemorySessionRepository` limitation prevents session domain event integration. Checkpoint files, transcript JSONL, and configuration TOML serve as the state carriers across process boundaries.

5. **A two-phase migration path defers bounded context extraction until the domain model stabilizes.** Phase 1 (infrastructure placement) ships with FEAT-001. Phase 2 (extract `context_monitoring` bounded context) triggers when domain concepts prove stable, a persistent session repository exists, and bounded context boundaries are empirically validated.

---

## L1 Technical Details

### Component Integration Diagram

The following diagram shows how new context resilience engines integrate with existing CLI infrastructure. Components marked `[EXISTING]` are unchanged; components marked `[NEW]` are created by this decision.

```
                          Claude Code
                              |
                 +------------+------------+
                 |            |            |
           SessionStart  UserPromptSubmit  PreCompact        PostToolUse
           (hook event)   (hook event)    (hook event)       (hook event)
                 |            |            |                      |
                 v            v            v                      v
        +-----------------+  +-----------------+  +-------------+  +-------------+
        | session_start_  |  | user-prompt-    |  | pre_compact_|  | post_tool_  |
        | hook.py         |  | submit.py       |  | hook.py     |  | use.py      |
        | [EXISTING+EXT]  |  | [EXISTING+EXT]  |  | [NEW]       |  | [NEW]       |
        +-----------------+  +-----------------+  +-------------+  +-------------+
          |       |              |    |    |           |                 |
          |       |              |    |    |           |                 |
          v       v              v    |    v           v                 v
   [EXISTING]  [NEW]      [EXISTING] | [NEW]        [NEW]          Staleness
   SessionQual Resumption  PromptRe  | Context     Checkpoint     Detection
   ityContext  Context     inforce-  | Monitor     Writer         Logic
   Generator   Generator   ment      | Engine                     (inline)
                           Engine    |
                                     v
                                   [NEW]
                                   Compaction
                                   Alert
                                   Engine
                                     |
          +----------+----------+----+
          |          |          |
          v          v          v
   $TRANSCRIPT   .jerry/     .jerry/
   _PATH         checkpoints/ config.toml
   (JSONL)       (JSON files) (LayeredConfig)
```

### Data Flow: UserPromptSubmit Hook (Extended)

This is the primary extension point, handling both context monitoring (Method A) and compaction alerts.

```
1. Claude Code fires UserPromptSubmit event
2. hooks.json routes to hooks/user-prompt-submit.py (5000ms timeout)
3. Hook reads JSON from stdin (Claude Code protocol)
4. Hook adds project root to sys.path

5. [EXISTING] Import and instantiate PromptReinforcementEngine
   5a. Engine reads .context/rules/quality-enforcement.md
   5b. Engine parses L2-REINJECT HTML comments
   5c. Engine sorts by rank, assembles within 600-token budget
   5d. Engine returns ReinforcementResult(preamble, items_included, token_estimate)

6. [NEW] Import and instantiate ContextMonitorEngine
   6a. Engine reads $TRANSCRIPT_PATH environment variable
   6b. Engine reads JSONL file from end (seek to last entry -- O(1))
   6c. Engine extracts input_tokens from latest transcript entry
   6d. Engine reads threshold config via LayeredConfigAdapter:
       - context_monitor.warning_threshold  (default: 0.70)
       - context_monitor.critical_threshold (default: 0.80)
       - context_monitor.emergency_threshold (default: 0.88)
   6e. Engine computes fill_percentage = input_tokens / context_window_size
   6f. Engine determines ThresholdTier: NOMINAL | LOW | WARNING | CRITICAL | EMERGENCY
   6g. Engine generates <context-monitor> XML tag (40-200 tokens based on tier)
       - NOMINAL/LOW: minimal tag (~40 tokens)
       - WARNING: tag with recommended actions (~120 tokens)
       - CRITICAL: tag with urgent actions + checkpoint reminder (~160 tokens)
       - EMERGENCY: tag with immediate preservation protocol (~200 tokens)

7. [NEW] Import and instantiate CompactionAlertEngine
   7a. Engine scans .jerry/checkpoints/ for cx-{NNN}-checkpoint.json files
   7b. Engine checks for corresponding .acknowledged marker files
   7c. If unacknowledged checkpoint found:
       7c-i.   Read most recent unacknowledged checkpoint
       7c-ii.  Populate Template 2 (<compaction-alert>, ~280 tokens)
       7c-iii. Create .acknowledged marker for checkpoint
   7d. If no unacknowledged checkpoint: return empty (no tag)

8. Combine outputs:
   additionalContext = join([
     <quality-reinforcement>...</quality-reinforcement>,   # [EXISTING] ~600 tokens
     <context-monitor>...</context-monitor>,               # [NEW] 40-200 tokens
     <compaction-alert>...</compaction-alert>,              # [NEW] 0 or ~280 tokens
   ])

9. Output JSON to stdout: {hookSpecificOutput: {additionalContext: combined}}
10. Exit 0 (always -- fail-open)

Error handling at each step:
- Step 6 fails: log to stderr, skip <context-monitor> tag, proceed to step 7
- Step 7 fails: log to stderr, skip <compaction-alert> tag, proceed to step 8
- Both fail: output contains only <quality-reinforcement> (existing behavior preserved)
```

### Data Flow: PreCompact Hook (New)

```
1. Claude Code fires PreCompact event (before context compaction)
2. hooks.json routes to scripts/pre_compact_hook.py (10000ms timeout)
3. Hook reads JSON from stdin (Claude Code protocol)
4. Hook adds project root to sys.path

5. [NEW] Import and instantiate CheckpointWriter
   5a. Writer creates .jerry/checkpoints/ directory if missing
       (Path.mkdir(parents=True, exist_ok=True) -- FileSystemEventStore pattern)
   5b. Writer determines next checkpoint ID:
       - Scan existing cx-{NNN}-checkpoint.json files
       - Next ID = max(NNN) + 1 (or 001 if no files)
   5c. Writer reads ORCHESTRATION.yaml resumption section (if exists):
       - Recovery state fields
       - Quality trajectory
       - Decision log
       - Agent summaries
   5d. Writer reads latest context-monitor state:
       - Fill percentage from most recent transcript entry
       - Current threshold tier
   5e. Writer assembles checkpoint JSON:
       {
         checkpoint_id: "cx-{NNN}",
         timestamp: ISO 8601,
         compaction_sequence: NNN,
         context_state: { fill_percentage, input_tokens, threshold_tier },
         resumption_state: { ... from ORCHESTRATION.yaml ... },
         session_info: { project_id, branch, working_directory }
       }
   5f. Writer writes checkpoint file using AtomicFileAdapter:
       .jerry/checkpoints/cx-{NNN}-checkpoint.json

6. Output JSON to stdout: {systemMessage: "Checkpoint cx-{NNN} saved at {fill}% context fill"}
7. Exit 0 (always -- fail-open)

Error handling:
- ORCHESTRATION.yaml not found: checkpoint contains context_state only (partial data)
- Directory creation fails: log error, exit 0 with empty response
- AtomicFileAdapter write fails: log error, exit 0 with empty response
```

### Data Flow: SessionStart Hook (Extended)

```
1. Claude Code fires SessionStart event
2. hooks.json routes to scripts/session_start_hook.py (10000ms timeout)

3. [EXISTING] Run: uv sync && uv run jerry --json projects context
4. [EXISTING] Transform CLI output to <project-context> tag
5. [EXISTING] Generate <quality-context> via SessionQualityContextGenerator

6. [NEW] Import and instantiate ResumptionContextGenerator
   6a. Generator scans .jerry/checkpoints/ for unacknowledged files
   6b. If no unacknowledged checkpoints: return empty (no resumption needed)
   6c. If found: read most recent unacknowledged checkpoint
   6d. Read ORCHESTRATION.yaml resumption section (for latest state)
   6e. Populate Template 1 (<resumption-context>, ~760 tokens):
       - Recovery state summary
       - Quality trajectory (current QG score, iteration count)
       - Key decisions from decision log
       - Agent summary states
       - File read instructions (priority-ordered)
       - Compaction event history
   6f. Return <resumption-context> tag

7. Combine outputs:
   additionalContext = join([
     <project-context>...</project-context>,     # [EXISTING]
     <quality-context>...</quality-context>,      # [EXISTING] ~700 tokens
     <resumption-context>...</resumption-context> # [NEW] 0 or ~760 tokens
   ])

8. Output JSON to stdout
9. Exit 0
```

### Interface Contracts

#### ContextMonitorEngine

```python
@dataclass(frozen=True)
class ContextMonitorResult:
    """Result of context fill monitoring."""
    fill_percentage: float          # 0.0 to 1.0
    input_tokens: int               # Raw token count from transcript
    threshold_tier: str             # NOMINAL | LOW | WARNING | CRITICAL | EMERGENCY
    injection_tag: str              # XML tag content (or empty string)
    token_estimate: int             # Estimated tokens in injection_tag

class ContextMonitorEngine:
    """Stateless L2 context fill monitoring engine.

    Follows PromptReinforcementEngine pattern:
    - Instantiated per hook invocation
    - Reads file input (transcript JSONL)
    - Produces injection content
    - Fail-open: errors return empty result
    """
    def __init__(self, config_adapter: LayeredConfigAdapter | None = None) -> None: ...
    def generate_monitor_tag(self, transcript_path: str) -> ContextMonitorResult: ...
```

#### CompactionAlertEngine

```python
@dataclass(frozen=True)
class CompactionAlertResult:
    """Result of compaction alert check."""
    alert_needed: bool              # True if unacknowledged checkpoint exists
    checkpoint_id: str | None       # e.g., "cx-003"
    injection_tag: str              # XML tag content (or empty string)
    token_estimate: int             # Estimated tokens in injection_tag

class CompactionAlertEngine:
    """Stateless L2 compaction alert engine.

    Scans .jerry/checkpoints/ for unacknowledged checkpoint files.
    Produces <compaction-alert> injection on first prompt after compaction.
    Marks checkpoint as acknowledged after injection.
    """
    def __init__(self, checkpoints_dir: Path | None = None) -> None: ...
    def generate_alert_tag(self) -> CompactionAlertResult: ...
```

#### CheckpointWriter

```python
@dataclass(frozen=True)
class CheckpointData:
    """Immutable snapshot of session state at compaction."""
    checkpoint_id: str              # e.g., "cx-003"
    timestamp: str                  # ISO 8601
    compaction_sequence: int        # Sequential compaction number
    context_state: dict             # fill_percentage, input_tokens, threshold_tier
    resumption_state: dict | None   # From ORCHESTRATION.yaml (None if unavailable)
    session_info: dict              # project_id, branch, working_directory

class CheckpointWriter:
    """Stateless PreCompact checkpoint creation engine.

    Reads ORCHESTRATION.yaml resumption section and context state.
    Writes checkpoint file using AtomicFileAdapter.
    Follows FileSystemEventStore pattern for directory creation.
    """
    def __init__(self, checkpoints_dir: Path | None = None) -> None: ...
    def write_checkpoint(
        self,
        orchestration_path: Path | None,
        transcript_path: str | None,
    ) -> CheckpointData: ...
```

#### ResumptionContextGenerator

```python
@dataclass(frozen=True)
class ResumptionContextResult:
    """Result of resumption context generation."""
    resumption_needed: bool         # True if unacknowledged checkpoint exists
    checkpoint_id: str | None       # e.g., "cx-003"
    injection_tag: str              # XML tag content (or empty string)
    token_estimate: int             # Estimated tokens in injection_tag

class ResumptionContextGenerator:
    """Stateless L1 resumption context generator.

    Follows SessionQualityContextGenerator pattern:
    - Generates XML preamble for session start
    - Token-budgeted (~760 token target)
    - Reads checkpoint files and ORCHESTRATION.yaml
    """
    def __init__(self, checkpoints_dir: Path | None = None) -> None: ...
    def generate_resumption_tag(
        self,
        orchestration_path: Path | None = None,
    ) -> ResumptionContextResult: ...
```

### Token Budget Analysis

The combined injection budget must be managed to avoid overwhelming the context window with framework content.

| Hook | Component | Budget (tokens) | Frequency |
|------|-----------|----------------|-----------|
| SessionStart | `<project-context>` [EXISTING] | ~200 | Once per session |
| SessionStart | `<quality-context>` [EXISTING] | ~700 | Once per session |
| SessionStart | `<resumption-context>` [NEW] | ~760 | Once per session (if checkpoint exists) |
| UserPromptSubmit | `<quality-reinforcement>` [EXISTING] | ~600 | Every prompt |
| UserPromptSubmit | `<context-monitor>` [NEW] | 40-200 | Every prompt |
| UserPromptSubmit | `<compaction-alert>` [NEW] | 0 or ~280 | Once after compaction |

**Worst-case per-prompt injection (UserPromptSubmit):** 600 + 200 + 280 = 1,080 tokens. This occurs only on the first prompt after a compaction event. Normal operation: 600 + 40 = 640 tokens (NOMINAL tier).

**Session start injection:** 200 + 700 + 760 = 1,660 tokens (with resumption). Without resumption: 900 tokens (existing behavior).

---

## L2 Strategic Implications

### Impact on the 5-Layer Enforcement Architecture

This decision adds context resilience to three of the five enforcement layers defined in ADR-EPIC002-002:

| Layer | Current Function | Added Function |
|-------|-----------------|----------------|
| L1 (Session Start) | Quality framework preamble (`<quality-context>`) | Resumption context (`<resumption-context>`) via `ResumptionContextGenerator` |
| L2 (Every Prompt) | Quality reinforcement (`<quality-reinforcement>`) | Context monitoring (`<context-monitor>`) via `ContextMonitorEngine`. Compaction alert (`<compaction-alert>`) via `CompactionAlertEngine` |
| L3 (Pre-Tool-Call) | AST architecture validation, governance escalation | Resumption staleness detection via PostToolUse hook (L3/L4 hybrid) |
| L4 (After Tool Calls) | Unchanged | PostToolUse staleness warning injection (L4 output) |
| L5 (Commit/CI) | Unchanged | Unchanged |

The enforcement architecture is extended, not modified. The existing layers gain additional capabilities without changing their core function. The total enforcement token budget increases from ~15,100 to ~16,960 tokens (additional ~1,860 tokens for worst-case context resilience injection across all layers).

### Future Bounded Context Extraction

When Phase 2 extraction criteria are met, the migration follows this path:

**From (Phase 1 -- Infrastructure Placement):**
```
src/infrastructure/internal/enforcement/
  context_monitor_engine.py         # Contains inline ThresholdTier, FillEstimate
  compaction_alert_engine.py        # Contains inline checkpoint scanning
  checkpoint_writer.py              # Contains inline CheckpointData
  resumption_context_generator.py   # Contains inline template population
```

**To (Phase 2 -- Bounded Context):**
```
src/context_monitoring/
  domain/
    value_objects/
      context_threshold.py          # ThresholdTier enum, threshold config
      fill_estimate.py              # FillEstimate value object
      checkpoint.py                 # CheckpointData value object
    events/
      context_monitoring_events.py  # ContextThresholdReached, CompactionDetected
  application/
    services/
      context_fill_estimator.py     # Orchestrates fill estimation
      checkpoint_service.py         # Orchestrates checkpoint lifecycle
    ports/
      transcript_reader.py          # Port: read transcript data
      checkpoint_repository.py      # Port: persist/read checkpoints
      threshold_configuration.py    # Port: read threshold config
  infrastructure/
    adapters/
      jsonl_transcript_reader.py    # Adapter: JSONL parsing
      filesystem_checkpoint_repository.py  # Adapter: .jerry/checkpoints/
      config_threshold_adapter.py   # Adapter: LayeredConfigAdapter bridge
```

**Extraction triggers:**
1. Domain concepts have proven stable through FEAT-001 implementation (no major refactoring of ThresholdTier, FillEstimate, or CheckpointData in at least 2 feature cycles).
2. A persistent session repository (`FileSystemSessionRepository`) is available, enabling `ContextThresholdReached` domain events to trigger `AbandonSessionCommand`.
3. The boundary between `context_monitoring` and `session_management` is validated: they communicate via domain events (`ContextThresholdReached`) and shared kernel (`SessionId`), with no bidirectional dependencies.

### Implications for FEAT-001 Implementation Approach

FEAT-001 (the implementation feature following this spike) should follow the revised 9-item work plan (CWI-01 through CWI-09) from the Phase 2 Gap Analysis. Key architectural guidelines for FEAT-001:

1. **Start with CWI-01 (configuration) and CWI-04 (resumption schema).** These are foundation items with no dependencies and can be parallelized.
2. **Build core detection (CWI-02, CWI-03) before integration (CWI-05, CWI-06, CWI-07).** The dependency graph requires operational detection before integration items can be tested.
3. **Keep all domain concepts inline in Phase 1.** `ThresholdTier`, `FillEstimate`, `CheckpointData` are defined within their respective engine files. Do not create separate domain value object files until Phase 2 extraction.
4. **Test each engine independently.** Unit tests target each engine class with mock file inputs. Integration tests verify the complete hook flow (stdin -> engines -> stdout JSON).
5. **Measure hook latency empirically.** After implementing CWI-03, measure actual `user-prompt-submit.py` execution time to validate the R3 risk mitigation (3000ms budget, 2000ms headroom).

### Dependencies on Persistent Session Repository

This decision explicitly defers session domain event integration. The following capabilities become available when a persistent session repository (e.g., `FileSystemSessionRepository`) is implemented:

| Capability | Current (InMemory) | Future (Persistent) |
|-----------|-------------------|---------------------|
| PreCompact hook triggers `SessionAbandoned` | Not possible -- session state lost across processes | Hook calls `jerry session abandon --reason "compaction"` |
| Compaction events in session audit trail | File-based checkpoint records only | `CompactionDetected` domain event in session event stream |
| Context threshold reaches trigger session actions | File-based state + L2 injection only | `ContextThresholdReached` event triggers `AbandonSessionCommand` at EMERGENCY tier |
| Post-session compaction analysis | Manual checkpoint file inspection | Event-sourced query: "How many compactions occurred in session X?" |

---

## Evidence

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
| UserPromptSubmit hook has 5000ms timeout | C5: Hook Integration Points | `hooks.json`: UserPromptSubmit timeout = 5000 |
| No PreCompact or PostToolUse hooks registered | C5: Hook Integration Points | `hooks.json` contains only SessionStart, UserPromptSubmit, PreToolUse, SubagentStop |
| ECW status line data unavailable to hooks (GAP-003 confirmed) | C8: ECW Status Line | Status line uses `statusLine.command` mechanism, not hooks mechanism |
| 10 of 14 items classified as EXTEND or REUSE | Mapping to SPIKE-001 Items | 1 REUSE (#7), 10 EXTEND (#1-3, #6, #8-12), 3 NEW (#4, #5, #13-14) |

### Phase 2 Gap Analysis Traceability

| ADR Claim | Gap Analysis Section | Specific Evidence |
|-----------|---------------------|-------------------|
| 14 items consolidate to 9 | L0 Summary, Consolidation Analysis | 4 merges: #1+#3, #4+#5, #2+#10, #13+#14 |
| Effort drops from 25-37 hours to 18-26 hours | Effort Summary | Phase-by-phase breakdown: A=2.5-3.5h, B=6-9h, C=5-7h, D=7h |
| New bounded context `context_monitoring` recommended | L2: Architectural Integration | Distinct domain language, different lifecycle, independent evolution |
| Phase 1 infrastructure placement before bounded context | L2: Architectural Integration | Engines are internal infrastructure, domain model premature |
| InMemorySessionRepository is highest architectural risk | L2: Risk Analysis, R1 | Rated HIGH, immediate mitigation: file-based state |
| File-based state for all cross-process communication | L2: Risk Analysis, R2 | State mechanism table for all 4 engines |
| 5000ms timeout budget analysis | L2: Risk Analysis, R3 | Budget: 1000ms + 1500ms + 500ms = 3000ms, 2000ms headroom |
| Method C timing dependency | L2: Risk Analysis, R5 | One-prompt lag, acceptable with Method A as primary |
| CWI-01 through CWI-09 work items | Revised Work Item Proposal | 9 items with acceptance criteria, dependency graph, implementation phases |

### Architecture Standards Traceability

| ADR Decision | Architecture Standard | Reference |
|-------------|----------------------|-----------|
| New engines in `infrastructure/internal/enforcement/` | Directory structure | `infrastructure/` layer for adapters |
| One class per engine file | H-10 | "Each Python file SHALL contain exactly ONE public class or protocol" |
| Domain concepts inline in Phase 1 (not separate domain layer) | Guidance (SOFT) | Premature abstraction avoidance |
| Phase 2 bounded context with domain events | Pattern Guidance (MEDIUM) | "Bounded contexts SHOULD communicate via domain events or shared kernel only" |
| `@dataclass(frozen=True)` for result types | Pattern Guidance (MEDIUM) | "Value objects SHOULD use `@dataclass(frozen=True, slots=True)`" |

---

## Self-Review (S-010) Verification

- [x] All 4 alternatives are analyzed with honest pros/cons -- Alternative 1 (Hook-Only) has 4 genuine pros including isolation and simplicity; Alternative 4 (Status Line) has 4 genuine pros including exact data.
- [x] Consequences include genuine negatives -- 4 negative consequences documented: coupling, InMemorySessionRepository limitation, latency risk, future migration cost.
- [x] Technical details reference actual source code patterns from Phase 1 audit -- PromptReinforcementEngine (246 lines), SessionQualityContextGenerator (134 lines), PreToolEnforcementEngine (567 lines), AtomicFileAdapter, FileSystemEventStore (lines 106-108), hooks.json (5000ms timeout).
- [x] Strategic implications address the migration path from Phase 1 to Phase 2 -- explicit extraction triggers, directory structure for both phases, capability comparison table for persistent repository.
- [x] ADR follows Nygard format faithfully -- Status, Context, Decision, Alternatives Considered, Consequences sections present.
- [x] Navigation table present with anchor links (H-23/H-24).
- [x] All claims reference Phase 1/Phase 2 evidence (P-001 compliance) -- Evidence section maps every claim to specific audit section and gap analysis section.
- [x] Interface contracts specified for all 4 new engines with type hints and docstrings.
- [x] Token budget analysis quantifies worst-case and normal injection overhead.
- [x] 5-layer enforcement architecture impact table shows which layers are affected and how.
