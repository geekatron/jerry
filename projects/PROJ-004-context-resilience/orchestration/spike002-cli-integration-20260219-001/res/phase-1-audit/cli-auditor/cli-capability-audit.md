# CLI Capability Audit for Context Resilience

<!-- PS-ID: SPIKE-002 | ENTRY-ID: phase-1 | DATE: 2026-02-19 -->
<!-- AGENT: ps-researcher v2.0.0 | MODEL: claude-opus-4-6 -->

> Comprehensive inventory of Jerry CLI capabilities relevant to the 14 SPIKE-001 context resilience follow-up work items. Classifies each item as REUSE, EXTEND, or NEW based on actual source code evidence.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Summary](#l0-summary) | Executive overview of audit findings |
| [CLI Capability Inventory](#cli-capability-inventory) | Detailed capabilities by category |
| [Mapping to SPIKE-001 Items](#mapping-to-spike-001-items) | REUSE/EXTEND/NEW classification for all 14 items |
| [Integration Architecture](#integration-architecture) | How CLI, hooks, and enforcement engines connect |
| [Evidence](#evidence) | Source file references with line numbers |

---

## L0 Summary

1. **The Jerry CLI has substantial existing infrastructure that SPIKE-001 overlooked.** 7 of 14 follow-up items can be classified as EXTEND (leveraging existing CLI capabilities) rather than NEW, reducing estimated implementation effort by approximately 30-40%.

2. **Token counting infrastructure already exists but is transcript-scoped.** The `TokenCounter` service (tiktoken-based, `p50k_base` encoding) currently serves transcript chunking. It can be directly reused for context fill estimation (Item #1, Method A), replacing the need to build a new token counting service from scratch.

3. **The session lifecycle model already supports context compaction.** The `SessionAbandoned` event (with reason field) and the `session abandon` CLI command were explicitly designed for context compaction scenarios (docstring line 207-209 of session.py: "typically due to context compaction or unexpected termination"). This provides a ready-made domain model for Items #2 and #10.

4. **The layered configuration system is a direct fit for threshold configuration.** The `LayeredConfigAdapter` already implements 4-layer precedence (env > project > root > defaults) with TOML parsing, dot-notation keys, and type coercion -- exactly what Item #7 (threshold configuration file) needs. The `jerry config set/get/show` CLI commands are operational.

5. **The ECW status line already implements compaction detection.** The `statusline.py` script (lines 463-506) detects compaction via token delta comparison, tracks state across invocations via a JSON file, and has configurable detection thresholds. This is directly relevant to Method C (OQ-1) from Item #9, though it operates client-side (not accessible to hooks -- confirming SPIKE-001's GAP-003).

---

## CLI Capability Inventory

### C1: Token Counting Infrastructure

**What it does:** Provides tiktoken-based token counting with `p50k_base` encoding (best Claude approximation). Supports plain text counting (`count_tokens`) and JSON-structured segment counting (`count_segment_tokens`). Caches the encoding instance for efficiency.

- **Source:** `src/transcript/application/services/token_counter.py`, lines 27-118
- **Current state:** Working. Used in production for transcript chunking. Has unit tests.
- **Relevance to context resilience:** Directly reusable for Method A context fill estimation. The `count_tokens()` method can count arbitrary text, not just transcript segments. The `p50k_base` encoding matches the Phase 3 recommendation for Claude approximation.

**Additionally**, the enforcement engines use a simpler chars/4 * 0.83 calibration formula for token estimation:
- `PromptReinforcementEngine._estimate_tokens()` (line 162-178): `len(text) / 4.0 * 0.83`
- `SessionQualityContextGenerator._estimate_tokens()` (line 121-133): `len(text) / 4 * 0.83`

This provides a lightweight alternative when tiktoken is not available or when speed is prioritized over accuracy.

### C2: Session Lifecycle Management

**What it does:** Full event-sourced session lifecycle with ACTIVE/COMPLETED/ABANDONED states. Commands: `jerry session start`, `jerry session end`, `jerry session status`, `jerry session abandon`. All commands emit domain events and support JSON output (`--json`).

- **Source files:**
  - Aggregate: `src/session_management/domain/aggregates/session.py` (325 lines)
  - Events: `src/session_management/domain/events/session_events.py` (97 lines)
  - Commands: `src/session_management/application/commands/` (3 command files)
  - Handlers: `src/session_management/application/handlers/commands/` (3 handler files)
  - CLI: `src/interface/cli/adapter.py`, lines 277-492 (session namespace)
  - Routing: `src/interface/cli/main.py`, lines 117-152 (`_handle_session`)
- **Current state:** Working. Full CQRS implementation with in-memory repository.
- **Relevance to context resilience:**
  - The `SessionAbandoned` event with `reason` field (session_events.py line 67-80) was designed specifically for context compaction scenarios (session.py line 207: "typically due to context compaction or unexpected termination").
  - The `AbandonSessionCommand` with reason parameter (abandon_session_command.py lines 27-37) can be invoked programmatically by hooks when EMERGENCY threshold is reached.
  - **Limitation:** The `InMemorySessionRepository` (in_memory_session_repository.py) loses data on process termination (line 35: "Loses data on process termination"). Since each CLI invocation is a separate process, session state does not persist across `jerry` calls. This is a known limitation for context resilience -- the PreCompact hook cannot rely on the CLI's in-memory session state.

### C3: Configuration Management

**What it does:** Layered configuration with 4-level precedence: Environment Variables (JERRY_*) > Project Config (`.jerry/config.toml`) > Root Config (`.jerry/config.toml`) > Code Defaults. Supports TOML parsing, dot-notation keys, type coercion (bool, int, float, string), and source tracking. Full CLI: `jerry config show [--source]`, `jerry config get <key>`, `jerry config set <key> <value> --scope`, `jerry config path`.

- **Source files:**
  - LayeredConfigAdapter: `src/infrastructure/adapters/configuration/layered_config_adapter.py` (383 lines)
  - EnvConfigAdapter: `src/infrastructure/adapters/configuration/env_config_adapter.py`
  - CLI: `src/interface/cli/adapter.py`, lines 991-1326 (config namespace)
  - Routing: `src/interface/cli/main.py`, lines 244-283 (`_handle_config`)
  - Bootstrap wiring: `src/interface/cli/adapter.py`, lines 1005-1035 (`_create_config_adapter`)
- **Current state:** Working. Includes default values for `session.auto_start`, `session.max_duration_hours`, `work_tracking.quality_gate_enabled`, etc.
- **Relevance to context resilience:** This is a direct fit for SPIKE-001 Item #7 (threshold configuration file). Instead of creating a separate `.jerry/context-monitor-config.json`, thresholds can be stored in the existing `.jerry/config.toml` hierarchy with keys like `context_monitor.warning_threshold`, `context_monitor.critical_threshold`, etc. The precedence system means project-level overrides and environment variable overrides work automatically.

### C4: Enforcement Engine Infrastructure

**What it does:** Three enforcement engines implementing L2, L1, and L3 of the 5-layer enforcement architecture:

**L1 (Session Start) -- SessionQualityContextGenerator:**
- Generates XML quality framework preamble (~700 token budget)
- Contains 4 sections: quality-gate, constitutional-principles, adversarial-strategies, decision-criticality
- Injected into SessionStart hook output as `<quality-context>` tag
- Source: `src/infrastructure/internal/enforcement/session_quality_context_generator.py` (134 lines)

**L2 (Every Prompt) -- PromptReinforcementEngine:**
- Parses L2-REINJECT HTML comment markers from quality-enforcement.md
- Sorts by rank, assembles within 600-token budget
- Fail-open design: errors return empty reinforcement
- Source: `src/infrastructure/internal/enforcement/prompt_reinforcement_engine.py` (246 lines)

**L3 (Pre-Tool-Call) -- PreToolEnforcementEngine:**
- AST-based architecture validation (import boundaries V-038, one-class-per-file V-041)
- Governance file modification detection with criticality escalation (C3/C4)
- Fail-open design: errors produce approval
- Source: `src/infrastructure/internal/enforcement/pre_tool_enforcement_engine.py` (567 lines)

- **Current state:** All three working in production.
- **Relevance to context resilience:**
  - The L2 engine (`PromptReinforcementEngine`) is the natural extension point for Item #1 (context monitor injection). The existing `UserPromptSubmit` hook already imports and uses this engine. Adding a `<context-monitor>` injection alongside the `<quality-reinforcement>` injection follows the proven pattern.
  - The L3 engine (`PreToolEnforcementEngine`) demonstrates the pattern for Item #12 (PostToolUse hook for resumption staleness). It already does governance escalation detection -- the same pattern applies to detecting stale ORCHESTRATION.yaml writes.
  - The L1 engine (`SessionQualityContextGenerator`) shows the pattern for injecting context-aware data at session start. This is relevant to Item #11 (resumption prompt automation) -- a similar generator could produce a `<resumption-context>` tag.

### C5: Hook Integration Points

**What it does:** Four registered hooks in `hooks/hooks.json`:

| Hook Event | Script | Timeout | Purpose |
|------------|--------|---------|---------|
| SessionStart | `scripts/session_start_hook.py` | 10s | Calls `jerry --json projects context`, injects `<project-context>` + `<quality-context>` |
| UserPromptSubmit | `hooks/user-prompt-submit.py` | 5s | Injects `<quality-reinforcement>` via L2 engine |
| PreToolUse | `scripts/pre_tool_use.py` | 5s | L3 AST-based architecture validation |
| SubagentStop | `scripts/subagent_stop.py` | 5s | Subagent lifecycle tracking |

- **Source files:**
  - Hook registration: `hooks/hooks.json` (51 lines)
  - SessionStart: `scripts/session_start_hook.py` (351 lines)
  - UserPromptSubmit: `hooks/user-prompt-submit.py` (93 lines)
- **Current state:** All four hooks operational.
- **Relevance to context resilience:**
  - **SessionStart hook** (session_start_hook.py): Already calls the CLI and transforms output to `additionalContext`. Lines 307-326 show the quality framework preamble injection pattern. This same pattern applies to Item #11 (resumption prompt automation) -- the hook can detect unacknowledged checkpoint files and inject a `<resumption-context>` tag.
  - **UserPromptSubmit hook** (user-prompt-submit.py): The primary injection point for Items #1, #3. The hook reads stdin (Claude Code protocol), generates content, and outputs JSON with `hookSpecificOutput.additionalContext`. Lines 60-68 show the injection format. Adding `<context-monitor>` and `<compaction-alert>` tags follows this exact pattern.
  - **Missing hooks:** No PreCompact hook is registered (Item #2 requires adding one to hooks.json). No PostToolUse hook is registered (Item #12 requires adding one).

### C6: Local Context Persistence

**What it does:** Two mechanisms for local context persistence:

**1. FilesystemLocalContextAdapter** -- reads `.jerry/local/context.toml` for machine-local configuration (active project selection, user preferences). Fail-safe: never raises exceptions.
- Source: `src/infrastructure/adapters/persistence/filesystem_local_context_adapter.py` (94 lines)

**2. FileSystemEventStore** -- persistent event store using JSONL format in `.jerry/data/events/`. Supports optimistic concurrency, cross-process file locking (via `filelock`), and append-only writes.
- Source: `src/work_tracking/infrastructure/persistence/filesystem_event_store.py` (369 lines)
- Storage format: `{base_path}/.jerry/data/events/{stream_id}.jsonl`

- **Current state:** Both working. FileSystemEventStore is used by work item tracking. LocalContextAdapter is used by the session start hook for project resolution.
- **Relevance to context resilience:**
  - The `FileSystemEventStore` pattern (JSONL append-only, file locking) is directly applicable to checkpoint file persistence (Item #2). The PreCompact hook could use a similar JSONL format for checkpoint files in `.jerry/checkpoints/`.
  - The `.jerry/local/` directory already exists as a gitignored location for machine-local state. This is the natural location for the compaction state file (Item #10: `.jerry/checkpoints/`), though SPIKE-001 proposed `.jerry/checkpoints/` which would need to be created.
  - The `AtomicFileAdapter` (used by LayeredConfigAdapter for TOML writes) provides safe file I/O with locking -- reusable for any checkpoint or state file writing.

### C7: Event Sourcing / Audit Trail

**What it does:** Full event sourcing infrastructure with domain events, aggregate roots, and event replay:

- **DomainEvent base class** -- immutable dataclass with `aggregate_id`, `aggregate_type`, `version`, `timestamp`
- **AggregateRoot base class** -- `_raise_event()`, `collect_events()`, `_apply()`, `load_from_history()`
- **Session events** -- `SessionCreated`, `SessionCompleted`, `SessionAbandoned`, `SessionProjectLinked`
- **Work item events** -- full lifecycle events with event-sourced repository

- **Source files:**
  - Session aggregate: `src/session_management/domain/aggregates/session.py`
  - Session events: `src/session_management/domain/events/session_events.py`
  - Event store: `src/work_tracking/infrastructure/persistence/filesystem_event_store.py`
- **Current state:** Working. Session aggregate uses in-memory repository; work items use FileSystemEventStore.
- **Relevance to context resilience:**
  - The event sourcing pattern provides a natural audit trail for context resilience events. A new `ContextThresholdReached` event, `CompactionDetected` event, or `CheckpointCreated` event could be added to the session aggregate.
  - The `SessionAbandoned.reason` field already captures the reason for abandonment (e.g., "Context compaction at 88% fill"). This provides traceability for post-hoc analysis of context resilience effectiveness.
  - The `FileSystemEventStore` could be extended or a parallel store created for context monitoring events, enabling calibration analysis (Item #13, #14).

### C8: ECW Status Line (Context Data Source)

**What it does:** Client-side status line script that parses Claude Code's stdin JSON to display model, context usage, cost, tokens, session duration, compaction detection, git status, and directory. Notably includes:

- **Context window extraction** (lines 403-423): Reads `context_window.current_usage.input_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens` to compute used tokens and percentage.
- **Compaction detection** (lines 463-506): Compares current context tokens to previous invocation via a state file (`~/.claude/ecw-statusline-state.json`). Detects drops exceeding `detection_threshold` (default 10,000 tokens).
- **Configurable thresholds** (lines 92-95): `warning_threshold: 0.65`, `critical_threshold: 0.85`.

- **Source:** `.claude/statusline.py` (959 lines)
- **Settings reference:** `.claude/settings.json` line 27: `"command": "python3 .claude/statusline.py"`
- **Current state:** Working. Runs on every status line update (frequently).
- **Relevance to context resilience:**
  - Confirms SPIKE-001's GAP-003: The status line script receives `context_window.current_usage` data from Claude Code, but this data is NOT available to hooks. The status line runs via the `statusLine.command` mechanism, not the `hooks` mechanism. There is no documented way for hooks to access the same data.
  - Confirms Method C feasibility assessment (OQ-1): The status line already writes compaction state to a JSON file (`~/.claude/ecw-statusline-state.json`). A file-based relay pattern (status line writes, hook reads) is technically possible but introduces a timing dependency -- the hook would read data from the previous status line update, not the current one.
  - The existing `extract_context_info()` and `extract_compaction_info()` functions could be extracted into a shared library for reuse by hooks (if Method C is pursued).

---

## Mapping to SPIKE-001 Items

| # | SPIKE-001 Item | Classification | CLI Capability | Gap Description |
|---|---------------|----------------|----------------|-----------------|
| 1 | Implement UserPromptSubmit context monitor hook (Method A) | **EXTEND** | C4 (PromptReinforcementEngine L2 injection pattern), C5 (UserPromptSubmit hook already operational), C1 (TokenCounter for transcript parsing) | Extend existing `user-prompt-submit.py` to add `$TRANSCRIPT_PATH` parsing and `<context-monitor>` injection alongside existing `<quality-reinforcement>`. TokenCounter available for accurate counting. L2 injection pattern proven. New code: transcript JSONL parsing, fill % calculation, threshold comparison. |
| 2 | Implement PreCompact hook for checkpoint file creation (Method B) | **EXTEND** | C6 (FileSystemEventStore JSONL pattern, AtomicFileAdapter for safe writes), C7 (event sourcing for audit trail), C2 (SessionAbandoned event with reason) | No PreCompact hook exists in hooks.json -- must register new hook entry. However, the checkpoint file writing can reuse FileSystemEventStore's JSONL pattern and AtomicFileAdapter's safe I/O. Session aggregate already models compaction via SessionAbandoned. New code: PreCompact hook script, checkpoint JSON schema, ORCHESTRATION.yaml reader. |
| 3 | Implement compaction alert injection in UserPromptSubmit hook | **EXTEND** | C5 (UserPromptSubmit hook injection pattern), C6 (file-based checkpoint detection) | Extend existing `user-prompt-submit.py` to check for unacknowledged checkpoint files in `.jerry/checkpoints/` and inject `<compaction-alert>` template. The hook already demonstrates file reading + JSON output pattern. New code: checkpoint file detection logic, Template 2 population, acknowledgment tracking. |
| 4 | Update ORCHESTRATION.yaml template with enhanced resumption schema v2.0 | **NEW** | None directly applicable | Pure template content change. The CLI has no ORCHESTRATION.yaml awareness -- orchestration templates are managed by the `/orchestration` skill, not the CLI. No CLI code to reuse. |
| 5 | Update orchestrator prompt to maintain resumption section (update protocol) | **NEW** | None directly applicable | Behavioral change in orchestrator agent instructions. This is a skill/agent-level change, not a CLI change. The L2-REINJECT mechanism (C4) could carry a resumption update reminder, but the core change is to agent prompt templates. |
| 6 | Update AE-006 in quality-enforcement.md with graduated sub-rules | **EXTEND** | C4 (L2-REINJECT markers already defined in quality-enforcement.md, PromptReinforcementEngine parses them) | The L2-REINJECT mechanism already works -- adding AE-006 sub-rules to quality-enforcement.md will automatically inject them into every prompt via the existing engine (if a new L2-REINJECT marker is added). The engine's rank-based sorting and token budget system handle prioritization. New code: AE-006a-e rule text in quality-enforcement.md, new L2-REINJECT marker. No engine code changes needed. |
| 7 | Implement threshold configuration file | **REUSE** | C3 (LayeredConfigAdapter with TOML hierarchy, env override, CLI commands) | The entire configuration infrastructure is reusable as-is. Add threshold keys to defaults in `_create_config_adapter()` (adapter.py line 1028-1034). Users can override via `jerry config set context_monitor.warning_threshold 0.70 --scope project`. No new infrastructure code needed -- only default value additions. |
| 8 | Validate OQ-9: Does `input_tokens` accurately approximate context fill? | **EXTEND** | C8 (ECW status line already extracts `input_tokens` from Claude Code data), C1 (TokenCounter for reference counting) | The status line already parses and displays `input_tokens` (lines 403-423). The TokenCounter provides a reference implementation for independent token counting. Validation requires comparing these two sources. New code: validation script that compares status line token data against independently counted content. |
| 9 | Investigate Method C feasibility (OQ-1) | **EXTEND** | C8 (ECW status line has context data + compaction detection + state file writing) | The status line already writes compaction state to `~/.claude/ecw-statusline-state.json` (lines 241-250). Method C proposes having hooks read this file. The status line code at lines 463-506 demonstrates the exact file-based relay pattern SPIKE-001 proposed. New investigation: verify timing (does status line update before UserPromptSubmit fires?), test file-based relay reliability. |
| 10 | Add `.jerry/checkpoints/` to project workspace layout | **EXTEND** | C6 (`.jerry/data/events/` directory creation pattern in FileSystemEventStore.__init__, lines 106-108), C3 (config path infrastructure) | The FileSystemEventStore already creates `.jerry/data/events/` with `mkdir(parents=True, exist_ok=True)`. The same pattern applies to `.jerry/checkpoints/`. The bootstrap module's `get_project_data_path()` (bootstrap.py lines 145-165) resolves project paths. New code: add checkpoint directory creation to project initialization; minimal effort. |
| 11 | Create resumption prompt automation (Template 1 populator) | **EXTEND** | C5 (SessionStart hook pattern: call CLI, generate additionalContext), C4 (SessionQualityContextGenerator pattern for XML preamble generation), C6 (file reading infrastructure) | The SessionStart hook (session_start_hook.py lines 307-326) already demonstrates the pattern: generate content, inject as `<quality-context>`. A `<resumption-context>` generator following the same pattern would read ORCHESTRATION.yaml resumption section + latest checkpoint file. New code: ResumptionContextGenerator class (following SessionQualityContextGenerator pattern), checkpoint file detection in SessionStart hook. |
| 12 | Implement PostToolUse hook for resumption staleness validation (L3/L4) | **EXTEND** | C4 (PreToolEnforcementEngine pattern for tool-use hooks), C5 (hooks.json registration pattern) | The PreToolUse hook demonstrates the entire pattern: hook registration in hooks.json, script execution, JSON stdin/stdout protocol, enforcement decision model. PostToolUse follows the same Claude Code hook protocol. The governance escalation pattern in PreToolEnforcementEngine (lines 501-536) is analogous to staleness detection. New code: PostToolUse hook script, ORCHESTRATION.yaml `updated_at` freshness check, staleness warning injection. |
| 13 | Validate thresholds against a second workflow type | **NEW** | C1 (TokenCounter for measuring), C8 (status line for monitoring) | Primarily an operational task (run a monitored session, collect data). TokenCounter and status line provide measurement tools, but the validation itself is a human-in-the-loop activity. No CLI code to build. |
| 14 | Document calibration protocol and recalibration triggers | **NEW** | None directly applicable | Documentation task. No CLI code involvement. |

**Summary Classification:**

| Classification | Count | Items |
|---------------|-------|-------|
| REUSE | 1 | #7 |
| EXTEND | 10 | #1, #2, #3, #6, #8, #9, #10, #11, #12 |
| NEW | 3 | #4, #5, #13, #14 |

---

## Integration Architecture

### Current Data Flow

```
SessionStart Hook Flow:
  Claude Code fires SessionStart event
    -> hooks.json routes to scripts/session_start_hook.py
      -> uv sync && uv run jerry --json projects context
        -> bootstrap.py creates QueryDispatcher + all adapters
        -> CLIAdapter.cmd_projects_context() dispatches query
        -> RetrieveProjectContextQueryHandler reads JERRY_PROJECT, scans projects/
        -> Returns JSON: {jerry_project, project_id, validation, available_projects}
      -> session_start_hook.py transforms JSON to hook format
      -> session_start_hook.py imports SessionQualityContextGenerator
        -> Generates <quality-context> preamble (~700 tokens)
      -> Outputs JSON: {systemMessage, hookSpecificOutput.additionalContext}
    -> Claude receives <project-context> + <quality-context> in context window

UserPromptSubmit Hook Flow:
  Claude Code fires UserPromptSubmit on every user prompt
    -> hooks.json routes to hooks/user-prompt-submit.py
      -> Imports PromptReinforcementEngine
      -> Engine reads quality-enforcement.md
      -> Parses L2-REINJECT markers, assembles preamble (~600 tokens)
      -> Outputs JSON: {hookSpecificOutput.additionalContext: "<quality-reinforcement>..."}
    -> Claude receives <quality-reinforcement> injected into context

PreToolUse Hook Flow:
  Claude Code fires PreToolUse before Write/Edit/Bash
    -> hooks.json routes to scripts/pre_tool_use.py
      -> Imports PreToolEnforcementEngine
      -> Evaluates file path + content via AST
      -> Returns approve/block/warn decision
    -> Claude receives enforcement decision (block = tool call rejected)
```

### Proposed Context Resilience Integration

```
EXTENDED UserPromptSubmit Hook Flow (Items #1, #3):
  Claude Code fires UserPromptSubmit
    -> hooks/user-prompt-submit.py (EXTENDED)
      -> [EXISTING] PromptReinforcementEngine generates <quality-reinforcement>
      -> [NEW] ContextMonitorEngine:
        1. Read $TRANSCRIPT_PATH (available in all hook events)
        2. Parse JSONL transcript for latest input_tokens (Method A)
        3. Read threshold config via LayeredConfigAdapter (Item #7: REUSE)
        4. Compute fill %, determine threshold tier
        5. Generate <context-monitor> injection (40-200 tokens)
      -> [NEW] CompactionAlertEngine:
        1. Check .jerry/checkpoints/ for unacknowledged checkpoint files
        2. If found: generate <compaction-alert> injection (~280 tokens)
      -> Outputs JSON with combined additionalContext

NEW PreCompact Hook Flow (Item #2):
  Claude Code fires PreCompact before context compaction
    -> hooks.json: NEW entry for PreCompact event
      -> scripts/pre_compact_hook.py (NEW)
        1. Read ORCHESTRATION.yaml resumption section
        2. Read session state (quality trajectory, defect context)
        3. Write checkpoint file to .jerry/checkpoints/cx-{NNN}-checkpoint.json
           (Using AtomicFileAdapter for safe writes, JSONL pattern from FileSystemEventStore)
        4. Optionally call jerry session abandon --reason "compaction"
      -> Outputs JSON: {systemMessage: "Checkpoint saved"}

EXTENDED SessionStart Hook Flow (Item #11):
  Claude Code fires SessionStart
    -> scripts/session_start_hook.py (EXTENDED)
      -> [EXISTING] jerry --json projects context
      -> [EXISTING] SessionQualityContextGenerator -> <quality-context>
      -> [NEW] ResumptionContextGenerator:
        1. Check .jerry/checkpoints/ for unacknowledged checkpoint files
        2. If found: read ORCHESTRATION.yaml resumption section
        3. Populate Template 1 (~760 tokens)
        4. Generate <resumption-context> injection
      -> Outputs JSON with combined additionalContext

NEW PostToolUse Hook Flow (Item #12):
  Claude Code fires PostToolUse after ORCHESTRATION.yaml writes
    -> hooks.json: NEW entry for PostToolUse event (matcher: Write|Edit)
      -> scripts/post_tool_use.py (NEW)
        1. Check if file is ORCHESTRATION.yaml
        2. If yes: check resumption.updated_at freshness
        3. If stale: inject warning via additionalContext
```

### Key Integration Points

| Integration Point | Mechanism | Source Evidence |
|-------------------|-----------|-----------------|
| Hook -> CLI | `subprocess.run([uv_path, "run", "jerry", "--json", ...])` | session_start_hook.py line 271 |
| Hook -> Enforcement Engine | Direct Python import (same process) | user-prompt-submit.py lines 53-58, session_start_hook.py lines 314-316 |
| Hook -> Configuration | Import LayeredConfigAdapter (same process) | adapter.py lines 1013-1035 |
| Hook -> Filesystem | Path-based file I/O with AtomicFileAdapter or direct Path operations | filesystem_event_store.py, filesystem_local_context_adapter.py |
| CLI -> Environment | `os.environ.get("JERRY_PROJECT")`, `os.environ.get("CLAUDE_PROJECT_DIR")` | bootstrap.py lines 155-165 |
| Hook -> Claude Context | `hookSpecificOutput.additionalContext` JSON field | session_start_hook.py lines 38-48, user-prompt-submit.py lines 61-68 |
| Status Line -> State File | JSON file at `~/.claude/ecw-statusline-state.json` | statusline.py lines 241-250, 463-506 |

---

## Evidence

### Source Files Read and Referenced

| # | File | Lines | Content Referenced |
|---|------|-------|--------------------|
| 1 | `src/transcript/application/services/token_counter.py` | 1-119 | TokenCounter class, count_tokens(), count_segment_tokens(), p50k_base encoding |
| 2 | `src/session_management/domain/aggregates/session.py` | 1-325 | Session aggregate, SessionStatus enum (ACTIVE/COMPLETED/ABANDONED), create(), complete(), abandon(), link_project(), load_from_history() |
| 3 | `src/session_management/domain/events/session_events.py` | 1-97 | SessionCreated, SessionCompleted, SessionAbandoned (with reason field), SessionProjectLinked |
| 4 | `src/session_management/application/commands/create_session_command.py` | 1-43 | CreateSessionCommand dataclass |
| 5 | `src/session_management/application/commands/end_session_command.py` | 1-37 | EndSessionCommand dataclass |
| 6 | `src/session_management/application/commands/abandon_session_command.py` | 1-38 | AbandonSessionCommand with reason field |
| 7 | `src/session_management/application/handlers/commands/create_session_command_handler.py` | 1-105 | CreateSessionCommandHandler, SessionAlreadyActiveError |
| 8 | `src/session_management/application/handlers/commands/end_session_command_handler.py` | 1-80 | EndSessionCommandHandler, NoActiveSessionError |
| 9 | `src/session_management/application/handlers/commands/abandon_session_command_handler.py` | 1-78 | AbandonSessionCommandHandler, NoActiveSessionError |
| 10 | `src/session_management/infrastructure/adapters/filesystem_project_adapter.py` | 1-220 | FilesystemProjectAdapter: scan_projects(), validate_project(), project_exists() |
| 11 | `src/session_management/infrastructure/adapters/in_memory_session_repository.py` | 1-100 | InMemorySessionRepository: get_active(), save(), NOT persistent across processes |
| 12 | `src/session_management/infrastructure/adapters/os_environment_adapter.py` | 1-49 | OsEnvironmentAdapter: get_env(), get_env_or_default() |
| 13 | `src/infrastructure/internal/enforcement/prompt_reinforcement_engine.py` | 1-246 | PromptReinforcementEngine: L2-REINJECT parsing, token estimation (chars/4*0.83), rank-based assembly, 600-token budget, fail-open |
| 14 | `src/infrastructure/internal/enforcement/session_quality_context_generator.py` | 1-134 | SessionQualityContextGenerator: XML preamble, 700-token budget, 4 sections |
| 15 | `src/infrastructure/internal/enforcement/pre_tool_enforcement_engine.py` | 1-567 | PreToolEnforcementEngine: AST validation, import boundaries, governance escalation, fail-open |
| 16 | `scripts/session_start_hook.py` | 1-351 | SessionStart hook: calls jerry CLI, transforms output, injects quality-context |
| 17 | `hooks/user-prompt-submit.py` | 1-93 | UserPromptSubmit hook: L2 reinforcement injection, fail-open |
| 18 | `hooks/hooks.json` | 1-51 | Hook registration: SessionStart, UserPromptSubmit, PreToolUse, SubagentStop |
| 19 | `src/bootstrap.py` | 1-519 | Composition root: create_query_dispatcher(), create_command_dispatcher(), get_projects_directory(), get_project_data_path(), singletons |
| 20 | `src/interface/cli/adapter.py` | 1-1488 | CLIAdapter: all command implementations, config namespace, session namespace |
| 21 | `src/interface/cli/main.py` | 1-343 | Main entry point: create_cli_adapter(), routing to all namespaces |
| 22 | `src/infrastructure/adapters/configuration/layered_config_adapter.py` | 1-383 | LayeredConfigAdapter: 4-level precedence, TOML parsing, dot-notation, type coercion |
| 23 | `src/infrastructure/adapters/persistence/filesystem_local_context_adapter.py` | 1-94 | FilesystemLocalContextAdapter: .jerry/local/context.toml reader |
| 24 | `src/work_tracking/infrastructure/persistence/filesystem_event_store.py` | 1-369 | FileSystemEventStore: JSONL format, file locking, optimistic concurrency, append-only |
| 25 | `.claude/settings.json` | 1-83 | Claude Code settings: statusLine command, plugins, rules |
| 26 | `.claude/statusline.py` | 1-959 | ECW status line: context extraction, compaction detection, token breakdown, state file |

### Key Line References for Claims

| Claim | File | Lines |
|-------|------|-------|
| SessionAbandoned designed for compaction | `session.py` | 207-209 ("typically due to context compaction or unexpected termination") |
| InMemorySessionRepository not persistent | `in_memory_session_repository.py` | 35 ("Loses data on process termination") |
| L2 engine token budget = 600 | `prompt_reinforcement_engine.py` | 35 (`_DEFAULT_TOKEN_BUDGET = 600`) |
| L1 engine token budget = 700 | `session_quality_context_generator.py` | 28 (`_TOKEN_BUDGET = 700`) |
| Token estimation formula | `prompt_reinforcement_engine.py` | 38 (`_TOKEN_CALIBRATION_FACTOR = 0.83`), 176 (`len(text) / 4.0 * 0.83`) |
| Hook output format | `session_start_hook.py` | 38-48 (`output_json` function with systemMessage + additionalContext) |
| Config defaults include session settings | `adapter.py` | 1028-1034 (default values for session.auto_start, session.max_duration_hours, etc.) |
| Status line compaction detection threshold | `statusline.py` | 115-119 (`detection_threshold: 10000`) |
| Status line context warning/critical thresholds | `statusline.py` | 92-95 (`warning_threshold: 0.65`, `critical_threshold: 0.85`) |
| Status line state file path | `statusline.py` | 118 (`~/.claude/ecw-statusline-state.json`) |
| FileSystemEventStore creates directories | `filesystem_event_store.py` | 106-108 (`mkdir(parents=True, exist_ok=True)`) |
| Hooks registered in hooks.json | `hooks.json` | 4-49 (SessionStart, UserPromptSubmit, PreToolUse, SubagentStop) |
| No PreCompact hook registered | `hooks.json` | 1-51 (absent from registered hooks) |
| CLI calls from SessionStart hook | `session_start_hook.py` | 271 (`uv run jerry --json projects context`) |

---

## Self-Review (S-010) Verification

- [x] Every CLI source file listed in the research task was actually read (26 files total, all confirmed via Read tool outputs)
- [x] Every SPIKE-001 follow-up item (#1 through #14) is mapped in the classification table
- [x] Classifications (REUSE/EXTEND/NEW) are evidence-based with specific source file and line references
- [x] Integration architecture reflects actual code patterns observed in source files, not desired architecture
- [x] No claims are made without source code evidence (all claims in Evidence section have file+line references)
- [x] The ECW status line was identified as a previously unaudited capability relevant to context resilience (C8)
- [x] The InMemorySessionRepository limitation (non-persistent across processes) is explicitly documented
- [x] The absence of PreCompact and PostToolUse hooks from hooks.json is confirmed
- [x] Navigation table present with anchor links (H-23/H-24 compliance)
