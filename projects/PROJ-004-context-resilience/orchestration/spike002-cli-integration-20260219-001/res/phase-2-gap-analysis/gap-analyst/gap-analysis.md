# Gap Analysis: SPIKE-001 to CLI-Integrated Context Resilience

<!-- PS-ID: SPIKE-002 | ENTRY-ID: phase-2 | DATE: 2026-02-19 -->
<!-- AGENT: ps-analyst v2.0.0 | MODEL: claude-opus-4-6 -->

> Deep gap analysis mapping the 14 SPIKE-001 follow-up work items against the Jerry CLI capability audit (Phase 1). Produces a revised, consolidated work item set that supersedes the original 14 by leveraging existing CLI infrastructure.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Summary](#l0-summary) | Executive overview: consolidation result and key architectural decisions |
| [L1: Per-Item Deep Analysis](#l1-per-item-deep-analysis) | Item-by-item analysis of all 14 SPIKE-001 work items |
| [L2: Consolidation Analysis](#l2-consolidation-analysis) | Which items merge and why |
| [L2: Architectural Integration](#l2-architectural-integration) | Hexagonal placement, bounded context decisions |
| [L2: Risk Analysis](#l2-risk-analysis) | CLI integration risks, process boundary issues |
| [Revised Work Item Proposal](#revised-work-item-proposal) | Consolidated, prioritized work item list (supersedes SPIKE-001 14 items) |
| [Evidence](#evidence) | References to Phase 1 audit and SPIKE-001 synthesis |

---

## L0 Summary

1. **The original 14 items consolidate to 9 work items when built on CLI infrastructure.** Items #1 and #3 merge (both extend `user-prompt-submit.py`). Items #4 and #5 merge (template change + behavioral update protocol are inseparable). Item #7 collapses to a configuration-only task using the existing `LayeredConfigAdapter` (REUSE). Items #10 and #2 merge (checkpoint directory creation is a sub-task of checkpoint hook implementation). Item #14 is absorbed into Item #13 (calibration documentation accompanies validation).

2. **Estimated effort drops from 25-37 hours to 18-26 hours (30% reduction).** The reduction comes from three sources: eliminating duplicate work across merged items, reusing existing infrastructure instead of building new code, and removing the need to design new configuration systems.

3. **A new bounded context (`context_monitoring`) is the recommended architectural placement.** Context monitoring introduces distinct domain concepts (ContextThreshold, CompactionEvent, FillEstimate) that do not belong in `session_management`. However, the two contexts interact: `context_monitoring` raises events that `session_management` consumes (e.g., triggering `SessionAbandoned`). Communication via domain events follows the hexagonal architecture standard (architecture-standards.md: "Bounded contexts SHOULD communicate via domain events or shared kernel only").

4. **The InMemorySessionRepository limitation is the single most significant architectural risk.** Each CLI invocation and each hook execution runs as a separate Python process. The session aggregate's in-memory state is lost between processes. This means the PreCompact hook cannot call `jerry session abandon` and expect it to find the active session. The mitigation is to use file-based state exclusively for cross-process communication (checkpoints, config files) and defer session integration until a persistent repository is implemented.

5. **Process boundary isolation between hooks and CLI is a design feature, not a bug.** Hooks importing CLI modules (e.g., `PromptReinforcementEngine`) works because those modules are stateless utilities. The new `ContextMonitorEngine` must follow the same pattern: stateless computation with file-based persistence for cross-invocation state.

---

## L1: Per-Item Deep Analysis

### Item #1: Implement UserPromptSubmit Context Monitor Hook (Method A)

**Original framing (hook-only):** Create a new context monitoring capability in the `UserPromptSubmit` hook that parses `$TRANSCRIPT_PATH` to read `input_tokens` from the JSONL transcript, computes fill percentage, compares against thresholds, and injects a `<context-monitor>` tag into `additionalContext`.

**CLI-integrated framing:** Extend the existing `hooks/user-prompt-submit.py` to add a `ContextMonitorEngine` alongside the existing `PromptReinforcementEngine`. The new engine follows the same pattern: stateless class, instantiated per hook invocation, reads file input (transcript JSONL instead of quality-enforcement.md), produces injection content. The `TokenCounter` service (C1, `src/transcript/application/services/token_counter.py`) provides accurate token counting if needed as a validation reference, though the primary mechanism reads `input_tokens` directly from transcript entries. Threshold configuration is loaded via `LayeredConfigAdapter` (C3) with keys like `context_monitor.warning_threshold`.

**Classification:** EXTEND (Phase 1 audit: C4 injection pattern + C5 hook + C1 token counting + C3 configuration)

**Specific code changes:**

| Action | File | Description |
|--------|------|-------------|
| CREATE | `src/infrastructure/internal/enforcement/context_monitor_engine.py` | New engine class. Reads `$TRANSCRIPT_PATH` JSONL, extracts latest `input_tokens`, computes fill %, determines threshold tier (NOMINAL/LOW/WARNING/CRITICAL/EMERGENCY). Outputs `<context-monitor>` XML tag (40-200 tokens depending on tier). Follows `PromptReinforcementEngine` pattern: stateless, fail-open, token-budgeted. |
| MODIFY | `hooks/user-prompt-submit.py` | Import `ContextMonitorEngine`. Instantiate alongside `PromptReinforcementEngine`. Combine outputs in `additionalContext`. |
| CREATE | `tests/unit/infrastructure/enforcement/test_context_monitor_engine.py` | Unit tests for threshold logic, JSONL parsing, fill calculation, tag generation, fail-open behavior. |

**Effort estimate:**
- Original (hook-only): 2-4 hours
- Revised (CLI-integrated): 2-3 hours (saves time: threshold config via LayeredConfigAdapter eliminates custom config parsing; engine pattern is proven and copy-able)

**Dependencies:**
- Depends on: Item #7 (threshold configuration) for config keys -- but can use hardcoded defaults initially.
- Depended on by: Item #6 (AE-006 sub-rules reference context-monitor signals), Item #8 (OQ-9 validation uses this hook).

---

### Item #2: Implement PreCompact Hook for Checkpoint File Creation (Method B)

**Original framing (hook-only):** Register a new PreCompact hook in `hooks.json`. The hook reads the ORCHESTRATION.yaml resumption section, captures session state, and writes a checkpoint file to `.jerry/checkpoints/cx-{NNN}-checkpoint.json`.

**CLI-integrated framing:** The hook registration follows the existing `hooks.json` pattern (C5). Checkpoint file writing reuses the `AtomicFileAdapter` (C6, `src/infrastructure/adapters/persistence/atomic_file_adapter.py`) for safe atomic writes with file locking. The checkpoint directory creation follows the `FileSystemEventStore` pattern (C6, `mkdir(parents=True, exist_ok=True)`). The `SessionAbandoned` event with reason field (C2, C7) provides the domain model for recording compaction events, though the InMemorySessionRepository limitation means this cannot be invoked cross-process.

**Classification:** EXTEND (Phase 1 audit: C5 hook registration + C6 file I/O patterns + C7 event model)

**Specific code changes:**

| Action | File | Description |
|--------|------|-------------|
| MODIFY | `hooks/hooks.json` | Add `PreCompact` hook entry. Matcher: `*`. Command: `uv run --directory ${CLAUDE_PLUGIN_ROOT} ${CLAUDE_PLUGIN_ROOT}/scripts/pre_compact_hook.py`. Timeout: 10000 (needs time for file I/O). |
| CREATE | `scripts/pre_compact_hook.py` | New hook script. Reads stdin (Claude Code hook protocol). Finds ORCHESTRATION.yaml in project directory. Reads resumption section. Reads latest context-monitor state. Writes checkpoint file to `.jerry/checkpoints/cx-{NNN}-checkpoint.json` using AtomicFileAdapter. Outputs JSON with `systemMessage: "Checkpoint saved at cx-{NNN}"`. |
| CREATE | `src/infrastructure/internal/enforcement/checkpoint_writer.py` | Stateless engine for checkpoint file creation. Accepts resumption data + context state, produces checkpoint JSON. Handles directory creation, checkpoint ID sequencing, atomic writes. |
| CREATE | `tests/unit/infrastructure/enforcement/test_checkpoint_writer.py` | Unit tests for checkpoint creation, ID sequencing, atomic write behavior, directory creation. |

**Effort estimate:**
- Original (hook-only): 4-6 hours
- Revised (CLI-integrated): 3-5 hours (saves time: AtomicFileAdapter for safe writes, hook registration pattern is documented)

**Dependencies:**
- Depends on: Item #10 (checkpoint directory) -- but this is now absorbed into this item (see Consolidation Analysis).
- Depended on by: Item #3 (compaction alert reads checkpoint files), Item #11 (resumption prompt reads checkpoint files).

---

### Item #3: Implement Compaction Alert Injection in UserPromptSubmit Hook

**Original framing (hook-only):** Extend the `UserPromptSubmit` hook to detect unacknowledged checkpoint files in `.jerry/checkpoints/` and inject Template 2 (`<compaction-alert>`, ~280 tokens) into `additionalContext`.

**CLI-integrated framing:** This is a second extension to the same `hooks/user-prompt-submit.py` file as Item #1. Both add new injection logic to the same hook. The checkpoint file detection uses standard `pathlib.Path` operations (following the `FilesystemLocalContextAdapter` pattern from C6). The compaction alert is injected alongside `<quality-reinforcement>` and `<context-monitor>` tags in the same `additionalContext` output.

**Classification:** EXTEND (Phase 1 audit: C5 hook injection pattern + C6 file reading)

**Specific code changes:**

| Action | File | Description |
|--------|------|-------------|
| CREATE | `src/infrastructure/internal/enforcement/compaction_alert_engine.py` | New engine class. Scans `.jerry/checkpoints/` for unacknowledged checkpoint files (no corresponding `.acknowledged` marker). Reads most recent checkpoint. Populates Template 2. Outputs `<compaction-alert>` XML tag (~280 tokens). Marks checkpoint as acknowledged after injection. |
| MODIFY | `hooks/user-prompt-submit.py` | Import `CompactionAlertEngine`. Instantiate alongside `PromptReinforcementEngine` and `ContextMonitorEngine`. Combine outputs. |
| CREATE | `tests/unit/infrastructure/enforcement/test_compaction_alert_engine.py` | Unit tests for checkpoint detection, acknowledgment tracking, template population, no-checkpoint-found behavior. |

**Effort estimate:**
- Original (hook-only): 2-3 hours
- Revised (CLI-integrated): 1-2 hours (saves time: injection pattern is identical to Item #1; both are coded in the same session)

**Dependencies:**
- Depends on: Item #2 (PreCompact hook creates the checkpoint files this reads).
- Depended on by: Nothing directly.

**Consolidation note:** Items #1 and #3 both modify `hooks/user-prompt-submit.py`. They should be implemented together. See Consolidation Analysis.

---

### Item #4: Update ORCHESTRATION.yaml Template with Enhanced Resumption Schema v2.0

**Original framing (hook-only):** Pure template content change. Replace the current 5-field resumption section in `skills/orchestration/templates/ORCHESTRATION.template.yaml` with the 7-sub-section, 23-field v2.0 schema.

**CLI-integrated framing:** The Phase 1 audit confirmed no CLI code is involved -- orchestration templates are managed by the `/orchestration` skill, not the CLI (Phase 1: Item #4 classification = NEW). The template change itself is unchanged. However, the enhanced schema must be consistent with the checkpoint file format (Item #2) and the resumption prompt template variables (Item #11).

**Classification:** NEW (Phase 1 audit: no CLI capability applicable)

**Specific code changes:**

| Action | File | Description |
|--------|------|-------------|
| MODIFY | `skills/orchestration/templates/ORCHESTRATION.template.yaml` | Replace `resumption:` section with v2.0 schema: Recovery State (8 fields), Files to Read (structured), Quality Trajectory (7 fields), Defect Summary (5 fields), Decision Log (N entries), Agent Summaries (N entries), Compaction Events (2 + N entries). |

**Effort estimate:**
- Original (hook-only): 2-3 hours
- Revised (CLI-integrated): 2-3 hours (no change -- this is pure template work)

**Dependencies:**
- Depends on: Nothing (schema is defined by SPIKE-001 Phase 4).
- Depended on by: Item #5 (update protocol requires the schema to exist), Item #2 (checkpoint writer references schema fields), Item #11 (resumption prompt reads schema fields).

**Consolidation note:** Items #4 and #5 are inseparable -- the template schema is useless without the update protocol, and the update protocol cannot be defined without the schema. See Consolidation Analysis.

---

### Item #5: Update Orchestrator Prompt to Maintain Resumption Section (Update Protocol)

**Original framing (hook-only):** Behavioral change in orchestrator agent instructions. The orchestrator MUST update the resumption section at every state transition (phase start/complete, QG iteration, compaction event, cross-phase decision, agent completion). Add L2-REINJECT tag for resumption update reminders.

**CLI-integrated framing:** The Phase 1 audit confirmed this is a skill/agent-level change (Phase 1: Item #5 classification = NEW). However, the L2-REINJECT mechanism (C4) can carry a resumption update reminder. Adding a new L2-REINJECT marker to quality-enforcement.md would inject a reminder on every prompt. The `PromptReinforcementEngine` already parses, ranks, and assembles these markers within a 600-token budget -- no engine changes needed.

**Classification:** NEW (agent behavioral change) + EXTEND (L2-REINJECT mechanism for reminder)

**Specific code changes:**

| Action | File | Description |
|--------|------|-------------|
| MODIFY | `skills/orchestration/agents/orchestrator.md` | Add explicit resumption update protocol: when to update, what to update, required fields. |
| MODIFY | `.context/rules/quality-enforcement.md` | Add L2-REINJECT marker for resumption update reminder (~25 tokens, rank ~9). |

**Effort estimate:**
- Original (hook-only): 2-3 hours
- Revised (CLI-integrated): 1-2 hours (L2-REINJECT marker is a one-line addition; orchestrator prompt is the main work)

**Dependencies:**
- Depends on: Item #4 (schema must exist before protocol can reference it).
- Depended on by: Item #12 (staleness validation enforces this protocol).

---

### Item #6: Update AE-006 in quality-enforcement.md with Graduated Sub-Rules

**Original framing (hook-only):** Replace the single AE-006 rule with AE-006a through AE-006e. Add L2-REINJECT tag.

**CLI-integrated framing:** The Phase 1 audit confirmed this is an EXTEND operation (C4). The L2-REINJECT mechanism already works -- adding a new marker for AE-006 sub-rules will automatically inject it via the `PromptReinforcementEngine` (Phase 1 evidence: `prompt_reinforcement_engine.py` parses L2-REINJECT HTML comment markers, sorts by rank, assembles within 600-token budget). No engine code changes needed. The existing 600-token budget can accommodate an additional ~35-token AE-006 injection because the current L2-REINJECT markers total approximately 400-450 tokens (Phase 1 audit: 8 existing L2-REINJECT markers at an average of ~50 tokens each).

**Classification:** EXTEND (Phase 1 audit: C4 L2-REINJECT mechanism)

**Specific code changes:**

| Action | File | Description |
|--------|------|-------------|
| MODIFY | `.context/rules/quality-enforcement.md` | Replace AE-006 single rule with AE-006a through AE-006e in the Auto-Escalation Rules table. Add L2-REINJECT marker with rank ~8 and ~35-token content summarizing the graduated escalation protocol. |

**Effort estimate:**
- Original (hook-only): 1-2 hours
- Revised (CLI-integrated): 1 hour (confirmed: no engine changes needed, L2-REINJECT is a marker addition)

**Dependencies:**
- Depends on: Item #1 (context monitor must exist for AE-006a-c to reference `<context-monitor>` signals).
- Depended on by: Nothing directly -- AE-006 rules are consumed by L2 injection.

**Auto-escalation:** AE-002 applies -- touching `.context/rules/` = auto-C3 minimum.

---

### Item #7: Implement Threshold Configuration File

**Original framing (hook-only):** Create a configurable threshold file (`.jerry/context-monitor-config.json` or similar) with default and criticality-adjusted thresholds. Avoid hardcoding thresholds in hook scripts.

**CLI-integrated framing:** This is the strongest REUSE case in the entire analysis. The Phase 1 audit demonstrated that the `LayeredConfigAdapter` (C3) already implements exactly this requirement: 4-layer precedence (env > project > root > defaults), TOML parsing, dot-notation keys, type coercion, and CLI management via `jerry config show/get/set`. The implementation reduces to adding default values to the `_create_config_adapter()` defaults dictionary in `src/interface/cli/adapter.py` (lines 1028-1034).

**Classification:** REUSE (Phase 1 audit: C3 LayeredConfigAdapter -- entire infrastructure reusable as-is)

**Specific code changes:**

| Action | File | Description |
|--------|------|-------------|
| MODIFY | `src/interface/cli/adapter.py` | Add default threshold values to `_create_config_adapter()`: `context_monitor.nominal_threshold: 0.55`, `context_monitor.low_threshold: 0.55`, `context_monitor.warning_threshold: 0.70`, `context_monitor.critical_threshold: 0.80`, `context_monitor.emergency_threshold: 0.88`, `context_monitor.compaction_detection_threshold: 10000`. |

**Effort estimate:**
- Original (hook-only): 1-2 hours
- Revised (CLI-integrated): 0.5 hours (adding 6 default values to an existing dictionary)

**Dependencies:**
- Depends on: Nothing.
- Depended on by: Item #1 (ContextMonitorEngine reads threshold config).

**Note:** Users can override thresholds at any level:
- Environment: `JERRY_CONTEXT_MONITOR_WARNING_THRESHOLD=0.75`
- Project: `jerry config set context_monitor.warning_threshold 0.75 --scope project`
- Root: `jerry config set context_monitor.warning_threshold 0.75 --scope root`

---

### Item #8: Validate OQ-9 -- Does `input_tokens` Accurately Approximate Context Fill?

**Original framing (hook-only):** Critical validation for Method A reliability. Compare `input_tokens` from transcript against actual context fill.

**CLI-integrated framing:** The Phase 1 audit identified two token estimation sources for comparison: (1) the `TokenCounter` service (C1, tiktoken `p50k_base` encoding) for independent reference counting, and (2) the ECW status line (C8) which reads actual `context_window.current_usage.input_tokens` from Claude Code. A validation script can compare transcript `input_tokens` values against status line data captured at the same time, and optionally against `TokenCounter` calculations on known content.

**Classification:** EXTEND (Phase 1 audit: C1 TokenCounter + C8 status line data)

**Specific code changes:**

| Action | File | Description |
|--------|------|-------------|
| CREATE | `scripts/validate_input_tokens.py` | Validation script. Reads `$TRANSCRIPT_PATH` JSONL, extracts `input_tokens` history. Reads `~/.claude/ecw-statusline-state.json` for status line data. Compares values, reports divergence. Optionally uses `TokenCounter` on known content as a third reference. |

**Effort estimate:**
- Original (hook-only): 2 hours (timebox)
- Revised (CLI-integrated): 1.5 hours (status line state file provides comparison data without building new infrastructure)

**Dependencies:**
- Depends on: Item #1 (provides the transcript parsing code this validates).
- Depended on by: Nothing directly -- validation result informs threshold confidence.

---

### Item #9: Investigate Method C Feasibility (OQ-1)

**Original framing (hook-only):** Can the ECW status line share context data with hooks via a shared state file? If feasible, Method C replaces Method A with exact (not heuristic) context data.

**CLI-integrated framing:** The Phase 1 audit comprehensively documented the status line's capabilities (C8). The status line already writes compaction state to `~/.claude/ecw-statusline-state.json` (lines 241-250). The investigation reduces to: (1) verify timing -- does the status line update its state file before `UserPromptSubmit` fires on the next prompt? (2) extend the state file to include `context_fill_percentage` alongside the existing compaction detection data. This is a spike with a controlled test.

**Classification:** EXTEND (Phase 1 audit: C8 status line state file mechanism)

**Specific code changes:**

| Action | File | Description |
|--------|------|-------------|
| MODIFY | `.claude/statusline.py` | Extend the state file write (lines 241-250) to include `context_fill_percentage`, `input_tokens`, `timestamp`. This makes the data available for hooks to read. |
| CREATE | `scripts/method_c_feasibility_test.py` | Test script. Runs as a UserPromptSubmit hook, reads state file, logs timing data. Determines if state file data is from the current prompt or previous. |

**Effort estimate:**
- Original (hook-only): 2 hours (timebox)
- Revised (CLI-integrated): 1.5 hours (status line already writes state file; investigation scope is narrower)

**Dependencies:**
- Depends on: Nothing (this is an independent investigation).
- Depended on by: Item #1 (if Method C is feasible, ContextMonitorEngine can use state file instead of transcript parsing).

---

### Item #10: Add `.jerry/checkpoints/` to Project Workspace Layout

**Original framing (hook-only):** Update project creation automation and workspace layout documentation. Create `.jerry/checkpoints/` directory.

**CLI-integrated framing:** The Phase 1 audit identified the `FileSystemEventStore` pattern (C6) for directory creation: `mkdir(parents=True, exist_ok=True)`. The `bootstrap.py` module's `get_project_data_path()` (lines 145-165) resolves project paths. Adding checkpoint directory creation to the project initialization follows the same pattern.

**Classification:** EXTEND (Phase 1 audit: C6 directory creation pattern)

**Specific code changes:**

| Action | File | Description |
|--------|------|-------------|
| MODIFY | `src/bootstrap.py` | Add `.jerry/checkpoints/` to project directory creation in `get_project_data_path()` or its callers. |
| MODIFY | `.context/rules/project-workflow.md` | Add `.jerry/checkpoints/` to the Project Structure diagram. |

**Effort estimate:**
- Original (hook-only): 1 hour
- Revised (CLI-integrated): 0.5 hours (single line addition to existing directory creation)

**Dependencies:**
- Depends on: Nothing.
- Depended on by: Item #2 (PreCompact hook writes to this directory).

**Consolidation note:** This item is absorbed into Item #2 -- the PreCompact hook implementation naturally creates the checkpoint directory as part of its initialization (following the FileSystemEventStore pattern). See Consolidation Analysis.

---

### Item #11: Create Resumption Prompt Automation (Template 1 Populator)

**Original framing (hook-only):** Script or tool that reads ORCHESTRATION.yaml resumption section and latest checkpoint file, populates Template 1 (~760 tokens), and outputs the resumption prompt for operator use. Future: integrate with SessionStart hook.

**CLI-integrated framing:** The Phase 1 audit identified the `SessionStart` hook pattern (C5) and the `SessionQualityContextGenerator` pattern (C4) as direct models. The hook already calls `jerry --json projects context` and injects `<quality-context>` (session_start_hook.py lines 307-326). A `ResumptionContextGenerator` following the same pattern would: (1) check `.jerry/checkpoints/` for unacknowledged checkpoint files, (2) if found, read ORCHESTRATION.yaml resumption section, (3) populate Template 1, (4) inject `<resumption-context>` tag into `additionalContext`.

**Classification:** EXTEND (Phase 1 audit: C5 SessionStart hook pattern + C4 context generator pattern)

**Specific code changes:**

| Action | File | Description |
|--------|------|-------------|
| CREATE | `src/infrastructure/internal/enforcement/resumption_context_generator.py` | New generator class following `SessionQualityContextGenerator` pattern. Reads checkpoint files + ORCHESTRATION.yaml. Populates Template 1. Outputs `<resumption-context>` XML tag (~760 tokens). |
| MODIFY | `scripts/session_start_hook.py` | Import `ResumptionContextGenerator`. After existing quality context generation, check for checkpoints and inject `<resumption-context>` if applicable. |
| CREATE | `tests/unit/infrastructure/enforcement/test_resumption_context_generator.py` | Unit tests for checkpoint detection, YAML parsing, template population, no-checkpoint behavior. |

**Effort estimate:**
- Original (hook-only): 3-4 hours
- Revised (CLI-integrated): 2-3 hours (generator pattern is well-established; SessionStart hook extension is proven)

**Dependencies:**
- Depends on: Item #2 (checkpoint files must exist), Item #4 (resumption schema must be defined).
- Depended on by: Nothing directly.

---

### Item #12: Implement PostToolUse Hook for Resumption Staleness Validation (L3/L4)

**Original framing (hook-only):** Hook fires after ORCHESTRATION.yaml writes. Checks `resumption.updated_at` freshness. Injects warning if stale.

**CLI-integrated framing:** The Phase 1 audit identified the `PreToolEnforcementEngine` (C4) as the direct pattern. The governance escalation detection in that engine (lines 501-536) is architecturally analogous to staleness detection: both inspect a file write and produce a decision (approve/warn/block). The `hooks.json` registration pattern (C5) is identical -- add a new `PostToolUse` entry. Note: PostToolUse is a different hook event from PreToolUse, but Claude Code's hook protocol is the same JSON stdin/stdout format.

**Classification:** EXTEND (Phase 1 audit: C4 PreToolEnforcementEngine pattern + C5 hooks.json)

**Specific code changes:**

| Action | File | Description |
|--------|------|-------------|
| MODIFY | `hooks/hooks.json` | Add `PostToolUse` hook entry. Matcher: `Write\|Edit\|MultiEdit`. Command: `uv run --directory ${CLAUDE_PLUGIN_ROOT} ${CLAUDE_PLUGIN_ROOT}/scripts/post_tool_use.py`. Timeout: 5000. |
| CREATE | `scripts/post_tool_use.py` | New hook script. Reads stdin. Checks if written file is ORCHESTRATION.yaml. If yes: parses `resumption.updated_at`, compares against current time. If stale (> threshold, e.g., 5 phase transitions without update): injects staleness warning via `additionalContext`. |
| CREATE | `tests/unit/scripts/test_post_tool_use.py` | Unit tests for ORCHESTRATION.yaml detection, staleness calculation, non-ORCHESTRATION passthrough. |

**Effort estimate:**
- Original (hook-only): 2-3 hours
- Revised (CLI-integrated): 2-3 hours (no savings -- the hook is new; the pattern helps but the logic is unique)

**Dependencies:**
- Depends on: Item #5 (update protocol defines when `updated_at` should change).
- Depended on by: Nothing directly.

---

### Item #13: Validate Thresholds Against a Second Workflow Type

**Original framing (hook-only):** Operational task. Run a monitored session with the detection system active against a different workflow profile. Collect per-operation token costs and fill trajectory.

**CLI-integrated framing:** The Phase 1 audit confirmed this is primarily operational (Phase 1: Item #13 classification = NEW). The `TokenCounter` (C1) and status line (C8) provide measurement tools but the validation itself requires a human running a real workflow. No CLI code to build.

**Classification:** NEW (Phase 1 audit: no CLI code involvement)

**Specific code changes:**

| Action | File | Description |
|--------|------|-------------|
| CREATE | `docs/knowledge/context-resilience/calibration-protocol.md` | Document the calibration protocol from SPIKE-001 Phase 6. Define workflow selection criteria, measurement methodology, data collection format, recalibration triggers. |

**Effort estimate:**
- Original (hook-only): 4 hours (timebox)
- Revised (CLI-integrated): 4 hours (no change -- operational activity)

**Dependencies:**
- Depends on: Items #1, #2 (detection system must be operational to validate).
- Depended on by: Nothing directly.

**Consolidation note:** Item #14 (documentation) is absorbed into this item. See Consolidation Analysis.

---

### Item #14: Document Calibration Protocol and Recalibration Triggers

**Original framing (hook-only):** Documentation task. Persist the calibration protocol from SPIKE-001 Phase 6 as operational documentation.

**CLI-integrated framing:** No CLI involvement. Pure documentation.

**Classification:** NEW (Phase 1 audit: no CLI involvement)

**Specific code changes:**

| Action | File | Description |
|--------|------|-------------|
| CREATE | `docs/knowledge/context-resilience/calibration-protocol.md` | Same as Item #13 output. |

**Effort estimate:**
- Original (hook-only): 1-2 hours
- Revised (CLI-integrated): 0 hours (absorbed into Item #13)

**Dependencies:**
- Depends on: Item #13 (written during/after threshold validation).
- Depended on by: Nothing.

**Consolidation note:** Absorbed into Item #13. The calibration protocol documentation is a natural output of the threshold validation activity. Separating them creates an artificial boundary.

---

## L2: Consolidation Analysis

### Consolidation Decisions

Five consolidation opportunities were identified. Each eliminates duplicate work, reduces context-switching overhead, and produces a more cohesive work item.

#### Merge 1: Items #1 + #3 --> CWI-03 (Context-Aware UserPromptSubmit Hook)

**Rationale:** Both items modify `hooks/user-prompt-submit.py`. Both create new engine classes in `src/infrastructure/internal/enforcement/`. Both inject XML tags into `additionalContext`. Implementing them separately means modifying the same hook file twice, duplicating the injection pattern, and risking integration conflicts.

**What changes when merged:**
- Single hook modification with both `ContextMonitorEngine` and `CompactionAlertEngine` integrated simultaneously.
- Shared utility code: checkpoint directory scanning logic, fail-open error handling, combined output assembly.
- Single test suite for the hook integration (individual engine tests remain separate).

**Effort savings:** 0.5-1 hour (eliminated: second round of hook modification, duplicate integration testing)

#### Merge 2: Items #4 + #5 --> CWI-04 (Enhanced Resumption Schema + Update Protocol)

**Rationale:** The template schema (Item #4) and the update protocol (Item #5) are inseparable. A schema without a protocol is dead content -- the orchestrator will not know to populate the new fields. A protocol without a schema has nothing to reference. They form a single logical deliverable: "the orchestrator maintains an enhanced resumption section."

**What changes when merged:**
- Single work item covers: template YAML changes + orchestrator prompt changes + L2-REINJECT marker addition.
- The acceptance criteria include both schema correctness AND protocol enforcement.
- Testing validates that an orchestration run using the updated template produces populated resumption fields.

**Effort savings:** 0.5 hours (eliminated: separate review cycles, duplicate context loading)

#### Merge 3: Items #2 + #10 --> CWI-02 (PreCompact Hook + Checkpoint Infrastructure)

**Rationale:** Item #10 (create `.jerry/checkpoints/` directory) is a sub-task of Item #2 (PreCompact hook that writes to that directory). The `FileSystemEventStore` pattern shows that directory creation is a single line in `__init__()`: `Path(dir).mkdir(parents=True, exist_ok=True)`. Making this a separate work item creates artificial overhead (separate review, separate testing, separate deployment) for what is effectively one line of code.

**What changes when merged:**
- The `CheckpointWriter` engine creates the directory in its constructor (following `FileSystemEventStore` pattern).
- The project-workflow.md documentation update is included in the same work item.
- Acceptance criteria include: directory creation, checkpoint file writing, and workspace documentation.

**Effort savings:** 0.5 hours (eliminated: separate work item overhead for a one-line change)

#### Merge 4: Items #13 + #14 --> CWI-09 (Threshold Validation + Calibration Documentation)

**Rationale:** The calibration documentation (Item #14) is a natural output of the threshold validation activity (Item #13). The person running the validation workflow will observe threshold behavior, collect data, and then document the protocol -- these are sequential steps in a single activity, not independent deliverables.

**What changes when merged:**
- Single work item covers: run monitored workflow + collect data + document protocol.
- The documentation is produced during/after the validation, not as a separate follow-up.
- Acceptance criteria include both: threshold validation data AND written calibration protocol.

**Effort savings:** 0.5 hours (eliminated: duplicate context loading, separate review)

#### Non-Merge: Items #8 + #9 (Kept Separate)

**Considered and rejected.** Items #8 (validate OQ-9) and #9 (investigate Method C) both involve comparing token counting approaches. However, they have different objectives: #8 validates Method A's reliability (is `input_tokens` accurate?), while #9 investigates a potential replacement for Method A (can Method C provide exact data?). They could proceed in parallel with different investigators. Merging would create an overly broad spike with unclear success criteria.

### Summary

| Original Items | Merged Into | Savings |
|----------------|-------------|---------|
| #1 + #3 | CWI-03 | 0.5-1 hr |
| #4 + #5 | CWI-04 | 0.5 hr |
| #2 + #10 | CWI-02 | 0.5 hr |
| #13 + #14 | CWI-09 | 0.5 hr |
| Total | 14 items --> 9 items | 2-2.5 hr |

---

## L2: Architectural Integration

### Hexagonal Architecture Placement

The context resilience system introduces new domain concepts that must be placed within the hexagonal architecture. The key question is: does this belong in the existing `session_management` bounded context, or does it warrant a new bounded context?

#### Decision: New Bounded Context -- `context_monitoring`

**Rationale:**

1. **Distinct domain language.** Context monitoring introduces concepts that do not exist in session management: `ContextThreshold`, `FillEstimate`, `CompactionEvent`, `CheckpointFile`, `ThresholdTier` (NOMINAL/LOW/WARNING/CRITICAL/EMERGENCY). These are not session concepts -- a session can be active, completed, or abandoned regardless of context fill level.

2. **Different lifecycle.** Context monitoring operates per-prompt (via `UserPromptSubmit`), while session management operates per-session (via `SessionStart`). The monitoring state changes every prompt; the session state changes at session boundaries.

3. **Independent evolution.** Threshold calibration, detection methods (Method A vs. C), and injection formats will evolve independently of session lifecycle management.

4. **Architecture standards compliance.** Per `architecture-standards.md`: "Bounded contexts SHOULD communicate via domain events or shared kernel only." Context monitoring can raise a `ContextThresholdReached` event that session management consumes to trigger `SessionAbandoned`, maintaining clean boundaries.

**However**, for the initial implementation, the new domain concepts are placed in the infrastructure enforcement layer rather than a full bounded context. The rationale:

- The enforcement engines (`PromptReinforcementEngine`, `SessionQualityContextGenerator`, `PreToolEnforcementEngine`) are not in any bounded context -- they are internal infrastructure components.
- Context monitoring follows the same pattern: stateless engines that read files and produce injection content.
- A full bounded context (domain/application/infrastructure layers) is premature until the domain model stabilizes.
- The migration path is clear: once the domain model proves stable, extract from `infrastructure/internal/enforcement/` into `src/context_monitoring/{domain,application,infrastructure}/`.

#### Proposed Directory Structure (Phase 1: Infrastructure Placement)

```
src/infrastructure/internal/enforcement/
  prompt_reinforcement_engine.py          # EXISTING - L2 quality reinforcement
  session_quality_context_generator.py    # EXISTING - L1 quality context
  pre_tool_enforcement_engine.py          # EXISTING - L3 architecture validation
  context_monitor_engine.py              # NEW - L2 context fill monitoring
  compaction_alert_engine.py             # NEW - L2 post-compaction alert
  checkpoint_writer.py                   # NEW - PreCompact checkpoint creation
  resumption_context_generator.py        # NEW - L1 resumption context

scripts/
  session_start_hook.py                  # EXISTING - extended with resumption
  pre_tool_use.py                        # EXISTING - unchanged
  subagent_stop.py                       # EXISTING - unchanged
  pre_compact_hook.py                    # NEW - checkpoint creation
  post_tool_use.py                       # NEW - staleness validation

hooks/
  hooks.json                             # EXISTING - extended with PreCompact, PostToolUse
  user-prompt-submit.py                  # EXISTING - extended with context monitor + compaction alert
```

#### Proposed Directory Structure (Phase 2: Bounded Context Extraction)

```
src/context_monitoring/
  domain/
    value_objects/
      context_threshold.py               # ThresholdTier enum + threshold configuration
      fill_estimate.py                   # FillEstimate value object (percentage, tokens, method)
    events/
      context_monitoring_events.py       # ContextThresholdReached, CompactionDetected
  application/
    services/
      context_fill_estimator.py          # Application service: compute fill from transcript
      checkpoint_service.py              # Application service: create/read/acknowledge checkpoints
    ports/
      transcript_reader.py               # Port: read transcript data
      checkpoint_repository.py           # Port: persist checkpoint files
      threshold_configuration.py         # Port: read threshold configuration
  infrastructure/
    adapters/
      jsonl_transcript_reader.py         # Adapter: parse JSONL transcript
      filesystem_checkpoint_repository.py # Adapter: .jerry/checkpoints/ file I/O
      config_threshold_adapter.py        # Adapter: LayeredConfigAdapter integration
```

This Phase 2 structure follows the same hexagonal pattern as `session_management` and `work_tracking`. The migration from Phase 1 to Phase 2 is deferred until the domain model is validated through FEAT-001 implementation.

#### Domain Concept Placement

| Concept | Phase 1 Location | Phase 2 Location | Justification |
|---------|-----------------|-----------------|---------------|
| ThresholdTier (enum) | `context_monitor_engine.py` (inline) | `context_monitoring/domain/value_objects/context_threshold.py` | Value object: immutable, no identity, defines threshold levels |
| FillEstimate | `context_monitor_engine.py` (inline) | `context_monitoring/domain/value_objects/fill_estimate.py` | Value object: immutable data structure (percentage, tokens, method, timestamp) |
| ContextThresholdReached | Not implemented (engine returns tag directly) | `context_monitoring/domain/events/context_monitoring_events.py` | Domain event: signals boundary crossing, consumed by session management |
| CompactionDetected | Not implemented (checkpoint written directly) | `context_monitoring/domain/events/context_monitoring_events.py` | Domain event: signals compaction occurrence |
| CheckpointFile | `checkpoint_writer.py` (inline JSON schema) | `context_monitoring/domain/value_objects/checkpoint.py` | Value object: immutable snapshot of session state at compaction |

#### Hook-to-Domain Interaction Model

```
UserPromptSubmit Hook (hooks/user-prompt-submit.py)
  |
  |-- [EXISTING] PromptReinforcementEngine
  |     reads: .context/rules/quality-enforcement.md
  |     produces: <quality-reinforcement> tag
  |
  |-- [NEW] ContextMonitorEngine
  |     reads: $TRANSCRIPT_PATH (JSONL), LayeredConfigAdapter (thresholds)
  |     produces: <context-monitor> tag
  |     note: Stateless. No domain events in Phase 1.
  |
  |-- [NEW] CompactionAlertEngine
  |     reads: .jerry/checkpoints/ (filesystem scan)
  |     produces: <compaction-alert> tag
  |     side effect: marks checkpoint as acknowledged
  |     note: Acknowledgment is a file-system operation, not a domain event in Phase 1.
  |
  --> combined additionalContext output

PreCompact Hook (scripts/pre_compact_hook.py)
  |
  |-- [NEW] CheckpointWriter
  |     reads: ORCHESTRATION.yaml (resumption section), context-monitor state
  |     writes: .jerry/checkpoints/cx-{NNN}-checkpoint.json
  |     note: Uses AtomicFileAdapter for safe writes. No domain events in Phase 1.
  |
  --> systemMessage output

SessionStart Hook (scripts/session_start_hook.py)
  |
  |-- [EXISTING] jerry --json projects context
  |-- [EXISTING] SessionQualityContextGenerator
  |-- [NEW] ResumptionContextGenerator
  |     reads: .jerry/checkpoints/ (most recent unacknowledged), ORCHESTRATION.yaml
  |     produces: <resumption-context> tag
  |
  --> combined additionalContext output
```

### Bounded Context Communication

In Phase 2 (when `context_monitoring` is extracted as a full bounded context), communication with `session_management` follows the architecture standard:

| From | To | Mechanism | Event |
|------|-----|-----------|-------|
| `context_monitoring` | `session_management` | Domain event | `ContextThresholdReached(tier=EMERGENCY)` triggers `AbandonSessionCommand` |
| `session_management` | `context_monitoring` | Shared kernel | `SessionId` value object used in checkpoint files |
| `context_monitoring` | orchestrator (skill) | L2 injection | `<context-monitor>` tag carries threshold signals |

---

## L2: Risk Analysis

### R1: InMemorySessionRepository Limitation (HIGH)

**Risk:** The `InMemorySessionRepository` (Phase 1 evidence: `in_memory_session_repository.py` line 35: "Loses data on process termination") means session state does not persist across CLI invocations or hook executions. The PreCompact hook cannot call `jerry session abandon --reason "compaction"` and expect it to find the active session, because the session was created in a different process.

**Impact:** The original SPIKE-001 design assumed the PreCompact hook could trigger `SessionAbandoned` via the CLI. This is not possible with the current repository implementation.

**Mitigation:**
1. **Immediate:** Use file-based state exclusively for cross-process communication. Checkpoint files serve as the compaction record. The `SessionAbandoned` event is not triggered by the hook; instead, compaction is recorded in checkpoint files and in the ORCHESTRATION.yaml `compaction_events` section.
2. **Future:** When a persistent session repository is implemented (e.g., `FileSystemSessionRepository` using the existing `FileSystemEventStore` pattern), the PreCompact hook can trigger session domain events.

**Residual risk after mitigation:** LOW. File-based state is sufficient for all context resilience operations. Session event integration is a nice-to-have, not a functional requirement.

### R2: Process Boundary Isolation (MEDIUM)

**Risk:** Each hook execution is a separate Python process. Hooks import CLI modules (e.g., `PromptReinforcementEngine`) but cannot share in-memory state between invocations.

**Impact:** Any state that must persist across prompts (e.g., "was a WARNING injected on the previous prompt?") must be persisted to the filesystem.

**Mitigation:** All new engines follow the existing pattern: stateless computation with file-based state.

| Engine | State Mechanism | File |
|--------|----------------|------|
| ContextMonitorEngine | Reads transcript JSONL (already persistent) | `$TRANSCRIPT_PATH` |
| CompactionAlertEngine | Reads checkpoint files + `.acknowledged` markers | `.jerry/checkpoints/` |
| CheckpointWriter | Writes checkpoint files | `.jerry/checkpoints/cx-{NNN}-checkpoint.json` |
| ResumptionContextGenerator | Reads checkpoint files + ORCHESTRATION.yaml | `.jerry/checkpoints/`, `ORCHESTRATION.yaml` |

**Residual risk after mitigation:** LOW. The pattern is proven by existing hooks.

### R3: Hook Import Latency (MEDIUM)

**Risk:** The `UserPromptSubmit` hook has a 5000ms timeout (Phase 1 evidence: `hooks.json`). Adding `ContextMonitorEngine` and `CompactionAlertEngine` imports adds Python import time and file I/O for transcript parsing.

**Impact:** If the hook exceeds 5000ms, Claude Code silently drops the hook output. The user receives no context monitoring.

**Mitigation:**
1. **Lazy imports:** Import engines only when needed. The `PromptReinforcementEngine` is already imported at module level (user-prompt-submit.py line 53), but new engines can be imported inside `try` blocks.
2. **Fail-open design:** Both existing engines use fail-open error handling (Phase 1 evidence: `prompt_reinforcement_engine.py` fail-open design). New engines must follow the same pattern -- if any operation fails or times out, the hook still produces output (possibly without the monitoring tag).
3. **Performance budget:** Budget 1000ms for existing reinforcement, 1500ms for context monitoring (transcript read + parse), 500ms for compaction alert (directory scan). Total: 3000ms out of 5000ms timeout, leaving 2000ms headroom.

**Residual risk after mitigation:** LOW. The 5000ms budget is generous for file I/O operations. Transcript files are local filesystem reads.

### R4: Transcript JSONL Size Growth (LOW)

**Risk:** The `$TRANSCRIPT_PATH` JSONL file grows with every turn. For long sessions (50+ prompts), the file could be large. Parsing the entire file to find the latest `input_tokens` value is O(n) where n is the number of turns.

**Impact:** Performance degradation of `ContextMonitorEngine` in long sessions.

**Mitigation:** Read the JSONL file from the end (tail). The most recent entry contains the latest `input_tokens`. Python's `seek()` to end of file + reverse read is O(1) for finding the last entry.

**Residual risk after mitigation:** NEGLIGIBLE.

### R5: Timing Dependency for Method C (MEDIUM)

**Risk:** Method C relies on the ECW status line writing context data to a state file before the `UserPromptSubmit` hook reads it. The execution order is: (status line updates) -> (user types prompt) -> (UserPromptSubmit fires). The state file data is always from the previous prompt, not the current one.

**Impact:** Method C data has a one-prompt lag. At high fill rates where context changes rapidly (e.g., 29K tokens per QG iteration), a one-prompt lag could mean the difference between detecting WARNING and missing CRITICAL.

**Mitigation:**
1. Method A (transcript-based) is the primary detection mechanism. Method C is an accuracy upgrade, not a replacement.
2. The one-prompt lag is acceptable because thresholds have margin: WARNING at 70% provides headroom before CRITICAL at 80%.
3. Method C data can be used as a calibration reference (compare against Method A) rather than as the primary signal.

**Residual risk after mitigation:** LOW. Method A remains primary; Method C is supplementary.

### R6: AE-002 Auto-Escalation for Rule File Changes (LOW)

**Risk:** Item #6 (AE-006 update) touches `.context/rules/quality-enforcement.md`, which triggers AE-002 (auto-C3 minimum). This means the rule change requires a full C3 review process (all tiers, S-004 Pre-Mortem, S-012 FMEA, S-013 Inversion).

**Impact:** Higher review overhead for what is conceptually a documentation/rule update.

**Mitigation:** This is the correct behavior -- AE-002 exists to prevent unreviewed changes to governance files. The C3 review is appropriate because AE-006 sub-rules define escalation behavior that affects all future sessions. Accept the overhead.

**Residual risk after mitigation:** NONE. The escalation is intentional.

---

## Revised Work Item Proposal

The following 9 work items supersede the original 14 SPIKE-001 follow-up items. They are ordered by dependency (items needed first appear first) and scoped for independent deployment and testing.

---

### CWI-01: Threshold Configuration via LayeredConfigAdapter

| Field | Value |
|-------|-------|
| **ID** | CWI-01 |
| **Title** | Add context monitoring threshold defaults to CLI configuration |
| **Type** | Enabler |
| **Priority** | P1 - Critical |
| **Effort** | 0.5 hours |
| **Supersedes** | SPIKE-001 Item #7 |
| **Description** | Add default threshold values to the existing `LayeredConfigAdapter` configuration system. Six keys: `context_monitor.nominal_threshold` (0.55), `context_monitor.warning_threshold` (0.70), `context_monitor.critical_threshold` (0.80), `context_monitor.emergency_threshold` (0.88), `context_monitor.compaction_detection_threshold` (10000), `context_monitor.enabled` (true). Users can override at any level via `jerry config set`. |
| **CLI Integration Points** | `src/interface/cli/adapter.py` `_create_config_adapter()` defaults dictionary (lines 1028-1034). `LayeredConfigAdapter` provides env > project > root > defaults precedence automatically. |
| **Acceptance Criteria** | 1. `jerry config get context_monitor.warning_threshold` returns `0.70`. 2. `jerry config set context_monitor.warning_threshold 0.75 --scope project` persists override. 3. `JERRY_CONTEXT_MONITOR_WARNING_THRESHOLD=0.75` overrides project config. 4. All 6 threshold keys have defaults. 5. Unit test covers default retrieval and override precedence. |

---

### CWI-02: PreCompact Hook + Checkpoint Infrastructure

| Field | Value |
|-------|-------|
| **ID** | CWI-02 |
| **Title** | Implement PreCompact hook for checkpoint file creation with checkpoint directory |
| **Type** | Enabler |
| **Priority** | P1 - Critical |
| **Effort** | 3-5 hours |
| **Supersedes** | SPIKE-001 Items #2 + #10 |
| **Description** | Register a new `PreCompact` hook in `hooks.json`. Create a `CheckpointWriter` engine that reads the ORCHESTRATION.yaml resumption section and writes a checkpoint file to `.jerry/checkpoints/cx-{NNN}-checkpoint.json` using `AtomicFileAdapter` for safe atomic writes. The checkpoint directory is created by the engine's constructor (following `FileSystemEventStore` pattern: `mkdir(parents=True, exist_ok=True)`). Update `project-workflow.md` to include `.jerry/checkpoints/` in the workspace layout. |
| **CLI Integration Points** | `hooks/hooks.json` (new PreCompact entry). `AtomicFileAdapter` (`src/infrastructure/adapters/persistence/atomic_file_adapter.py`) for safe writes. `FileSystemEventStore` directory creation pattern (`src/work_tracking/infrastructure/persistence/filesystem_event_store.py` lines 106-108). |
| **Acceptance Criteria** | 1. `hooks.json` contains a `PreCompact` entry. 2. When PreCompact fires, checkpoint file is created at `.jerry/checkpoints/cx-001-checkpoint.json`. 3. Checkpoint file contains: resumption state, context fill %, timestamp, compaction sequence number. 4. `.jerry/checkpoints/` directory is auto-created if missing. 5. Sequential checkpoint IDs (cx-001, cx-002, etc.). 6. Fail-open: if ORCHESTRATION.yaml is not found, checkpoint contains partial data (context state only). 7. `project-workflow.md` updated with checkpoint directory. 8. Unit tests for CheckpointWriter covering: creation, ID sequencing, missing ORCHESTRATION.yaml, directory creation. |

---

### CWI-03: Context-Aware UserPromptSubmit Hook

| Field | Value |
|-------|-------|
| **ID** | CWI-03 |
| **Title** | Extend UserPromptSubmit hook with context monitoring and compaction alerts |
| **Type** | Enabler |
| **Priority** | P1 - Critical |
| **Effort** | 3-4 hours |
| **Supersedes** | SPIKE-001 Items #1 + #3 |
| **Description** | Extend the existing `hooks/user-prompt-submit.py` with two new engines: (1) `ContextMonitorEngine` -- reads `$TRANSCRIPT_PATH` JSONL, extracts latest `input_tokens`, computes fill %, determines threshold tier (NOMINAL/LOW/WARNING/CRITICAL/EMERGENCY), produces `<context-monitor>` tag (40-200 tokens). (2) `CompactionAlertEngine` -- scans `.jerry/checkpoints/` for unacknowledged checkpoint files, populates Template 2 (`<compaction-alert>`, ~280 tokens), marks checkpoint as acknowledged. Both engines are stateless, fail-open, and follow the `PromptReinforcementEngine` pattern. Threshold configuration is loaded from `LayeredConfigAdapter`. |
| **CLI Integration Points** | `hooks/user-prompt-submit.py` (extend existing hook). `PromptReinforcementEngine` pattern (`src/infrastructure/internal/enforcement/prompt_reinforcement_engine.py`). `LayeredConfigAdapter` for threshold reading. `$TRANSCRIPT_PATH` environment variable (available in all hook events). |
| **Acceptance Criteria** | 1. `<context-monitor>` tag injected on every prompt with: fill %, threshold tier, recommended action. 2. `<compaction-alert>` tag injected on first prompt after compaction (when unacknowledged checkpoint exists). 3. Compaction alert injected only once (checkpoint marked as acknowledged after injection). 4. Fail-open: if transcript parsing fails, hook still outputs quality reinforcement (existing behavior preserved). 5. Combined injection overhead <= 500 tokens per prompt (context monitor + compaction alert). 6. Hook execution within 5000ms timeout budget. 7. Unit tests for ContextMonitorEngine: threshold calculation, tier determination, tag generation, JSONL parsing. 8. Unit tests for CompactionAlertEngine: checkpoint detection, acknowledgment, template population. |

---

### CWI-04: Enhanced Resumption Schema + Update Protocol

| Field | Value |
|-------|-------|
| **ID** | CWI-04 |
| **Title** | Update ORCHESTRATION.yaml template with v2.0 resumption schema and orchestrator update protocol |
| **Type** | Story |
| **Priority** | P1 - Critical |
| **Effort** | 2-3 hours |
| **Supersedes** | SPIKE-001 Items #4 + #5 |
| **Description** | Replace the current 5-field resumption section in `skills/orchestration/templates/ORCHESTRATION.template.yaml` with the v2.0 schema: Recovery State (8 fields), Files to Read (structured with priority/purpose/sections), Quality Trajectory (7 fields), Defect Summary (5 fields), Decision Log (N entries), Agent Summaries (N entries), Compaction Events (2 + N entries). Update the orchestrator agent prompt (`skills/orchestration/agents/orchestrator.md`) with an explicit resumption update protocol defining when and what to update. Add an L2-REINJECT marker to `quality-enforcement.md` for resumption update reminders. |
| **CLI Integration Points** | `.context/rules/quality-enforcement.md` (new L2-REINJECT marker, rank ~9, ~25 tokens). No direct CLI code changes -- template and agent prompt are skill-level artifacts. |
| **Acceptance Criteria** | 1. ORCHESTRATION.yaml template contains v2.0 resumption schema with all 7 sub-sections. 2. Backward compatible: existing 5 fields preserved as part of Recovery State. 3. Orchestrator prompt includes explicit update protocol with triggers: phase start, phase complete, QG iteration, compaction event, cross-phase decision, agent completion. 4. L2-REINJECT marker present in quality-enforcement.md. 5. Resumption section includes `updated_at` timestamp field. |

---

### CWI-05: AE-006 Graduated Sub-Rules

| Field | Value |
|-------|-------|
| **ID** | CWI-05 |
| **Title** | Replace AE-006 with graduated sub-rules (AE-006a through AE-006e) |
| **Type** | Story |
| **Priority** | P2 - High |
| **Effort** | 1 hour |
| **Supersedes** | SPIKE-001 Item #6 |
| **Description** | Replace the single AE-006 rule in `quality-enforcement.md` with 5 graduated sub-rules mapping detection thresholds to escalation actions by criticality level. Add an L2-REINJECT marker (rank ~8, ~35 tokens) summarizing the graduated escalation protocol. The `PromptReinforcementEngine` automatically picks up the new marker without code changes (Phase 1 evidence: engine parses L2-REINJECT HTML comments, sorts by rank, assembles within 600-token budget). |
| **CLI Integration Points** | `.context/rules/quality-enforcement.md` (rule text + L2-REINJECT marker). No engine code changes. |
| **Acceptance Criteria** | 1. AE-006a through AE-006e defined in Auto-Escalation Rules table. 2. Each sub-rule specifies: trigger condition, escalation action, enforcement mechanism. 3. L2-REINJECT marker present with rank and content. 4. Total L2-REINJECT budget remains within 600 tokens (current + new marker). 5. Quality gate: C3 minimum per AE-002 (touches `.context/rules/`). |

---

### CWI-06: Resumption Prompt Automation (SessionStart Integration)

| Field | Value |
|-------|-------|
| **ID** | CWI-06 |
| **Title** | Create ResumptionContextGenerator and integrate with SessionStart hook |
| **Type** | Story |
| **Priority** | P2 - High |
| **Effort** | 2-3 hours |
| **Supersedes** | SPIKE-001 Item #11 |
| **Description** | Create a `ResumptionContextGenerator` class following the `SessionQualityContextGenerator` pattern. The generator checks `.jerry/checkpoints/` for unacknowledged checkpoint files, reads the latest checkpoint and ORCHESTRATION.yaml resumption section, populates Template 1 (~760 tokens), and produces a `<resumption-context>` XML tag. Integrate into `scripts/session_start_hook.py` after the existing quality context generation. |
| **CLI Integration Points** | `SessionQualityContextGenerator` pattern (`src/infrastructure/internal/enforcement/session_quality_context_generator.py`). `session_start_hook.py` (lines 307-326 show existing injection pattern). |
| **Acceptance Criteria** | 1. When a new session starts with unacknowledged checkpoint files, `<resumption-context>` tag is injected. 2. Tag contains: recovery state, quality trajectory, key decisions, agent summaries, file read instructions. 3. When no checkpoint files exist, no `<resumption-context>` tag is injected (existing behavior unchanged). 4. Template 1 variables sourced correctly from checkpoint file and ORCHESTRATION.yaml. 5. Total injection <= 800 tokens. 6. Unit tests for ResumptionContextGenerator: checkpoint detection, template population, no-checkpoint behavior. |

---

### CWI-07: PostToolUse Hook for Resumption Staleness Validation

| Field | Value |
|-------|-------|
| **ID** | CWI-07 |
| **Title** | Implement PostToolUse hook for ORCHESTRATION.yaml resumption staleness detection |
| **Type** | Enabler |
| **Priority** | P3 - Medium |
| **Effort** | 2-3 hours |
| **Supersedes** | SPIKE-001 Item #12 |
| **Description** | Register a new `PostToolUse` hook in `hooks.json` with matcher for `Write\|Edit\|MultiEdit`. The hook detects ORCHESTRATION.yaml writes, parses the `resumption.updated_at` field, and injects a staleness warning if the field is stale (threshold: has not been updated in the current phase). Follows the `PreToolEnforcementEngine` governance escalation pattern. |
| **CLI Integration Points** | `hooks/hooks.json` (new PostToolUse entry). `PreToolEnforcementEngine` governance detection pattern (`src/infrastructure/internal/enforcement/pre_tool_enforcement_engine.py` lines 501-536). |
| **Acceptance Criteria** | 1. `hooks.json` contains a `PostToolUse` entry. 2. Hook fires only on `Write\|Edit\|MultiEdit` tool calls. 3. Hook detects ORCHESTRATION.yaml writes (path matching). 4. If `resumption.updated_at` is stale, warning injected via `additionalContext`. 5. Non-ORCHESTRATION.yaml writes pass through silently. 6. Fail-open: if parsing fails, no warning injected. 7. Unit tests covering: ORCHESTRATION.yaml detection, staleness calculation, passthrough behavior. |

---

### CWI-08: Validation Spikes (OQ-9 + Method C)

| Field | Value |
|-------|-------|
| **ID** | CWI-08 |
| **Title** | Validate input_tokens accuracy (OQ-9) and investigate Method C feasibility (OQ-1) |
| **Type** | Spike |
| **Priority** | P2 - High |
| **Effort** | 3 hours (timebox) |
| **Supersedes** | SPIKE-001 Items #8 + #9 |
| **Description** | Two focused investigations: (1) OQ-9 validation -- compare `input_tokens` from transcript JSONL against ECW status line data (`~/.claude/ecw-statusline-state.json`) and optionally against `TokenCounter` calculations on known content. (2) Method C feasibility -- extend status line state file to include `context_fill_percentage`, implement a test hook that reads the state file, verify timing (does state file update before `UserPromptSubmit` fires?). Both produce a finding report with data and recommendation. |
| **CLI Integration Points** | `TokenCounter` (`src/transcript/application/services/token_counter.py`). ECW status line state file (`~/.claude/ecw-statusline-state.json`). `.claude/statusline.py` (extend state file write, lines 241-250). |
| **Acceptance Criteria** | 1. OQ-9: Report documenting `input_tokens` accuracy with measured divergence from reference sources. 2. Method C: Report documenting timing test results (does status line update before UserPromptSubmit?). 3. Method C: If feasible, prototype status line extension committed. 4. Both reports include recommendation: proceed/defer/abandon. 5. Total timebox: 3 hours. |

**Note on consolidation:** Items #8 and #9 are kept as a single spike because both are timeboxed investigations that can share a single session and produce a combined findings report. However, they investigate different questions and could be split if needed.

---

### CWI-09: Threshold Validation + Calibration Documentation

| Field | Value |
|-------|-------|
| **ID** | CWI-09 |
| **Title** | Validate thresholds against second workflow type and document calibration protocol |
| **Type** | Story |
| **Priority** | P3 - Medium |
| **Effort** | 4 hours (timebox) |
| **Supersedes** | SPIKE-001 Items #13 + #14 |
| **Description** | Run a monitored session with the detection system active (CWI-03) against a workflow with a different profile than PROJ-001 FEAT-015 (e.g., deep research spike or multi-file refactoring). Collect per-operation token costs and fill trajectory. Compare against PROJ-001 calibration. Document the calibration protocol: workflow selection criteria, measurement methodology, data collection format, recalibration triggers. Persist to `docs/knowledge/context-resilience/calibration-protocol.md`. |
| **CLI Integration Points** | CWI-03 (context monitoring must be operational). `TokenCounter` and status line for measurement tools. |
| **Acceptance Criteria** | 1. Monitored session completed against a non-PROJ-001 workflow. 2. Per-operation token cost data collected. 3. Fill trajectory compared against PROJ-001 baseline. 4. Threshold adjustment recommendations (if any) documented. 5. Calibration protocol document created at `docs/knowledge/context-resilience/calibration-protocol.md`. 6. Document includes: when to recalibrate, how to collect data, how to interpret results. |

---

### Dependency Graph

```
CWI-01 (Config)
  |
  v
CWI-03 (UserPromptSubmit: Context Monitor + Compaction Alert)
  ^
  |
CWI-02 (PreCompact Hook + Checkpoints)
  |
  v
CWI-06 (Resumption Prompt Automation)

CWI-04 (Resumption Schema + Protocol) ---> CWI-07 (PostToolUse Staleness)
                                      \--> CWI-02 (schema fields in checkpoint)
                                      \--> CWI-06 (schema fields in resumption prompt)

CWI-05 (AE-006 Sub-Rules) ---> depends on CWI-03 for context-monitor signals

CWI-08 (Validation Spikes) ---> depends on CWI-03 for Method A code
                            \--> may upgrade CWI-03 if Method C is feasible

CWI-09 (Threshold Validation) ---> depends on CWI-01, CWI-02, CWI-03 (system operational)
```

### Implementation Order

| Phase | Items | Rationale |
|-------|-------|-----------|
| Phase A (Foundation) | CWI-01, CWI-04 | Config and schema are prerequisites with no dependencies. Can be done in parallel. |
| Phase B (Core Detection) | CWI-02, CWI-03 | Core detection mechanisms. CWI-02 depends on CWI-04 (schema). CWI-03 depends on CWI-01 (config) and CWI-02 (checkpoint files for compaction alert). |
| Phase C (Integration) | CWI-05, CWI-06, CWI-07 | Framework integration. All depend on Phase B outputs. Can be partially parallelized. |
| Phase D (Validation) | CWI-08, CWI-09 | Validation and calibration. Require Phase B operational system. |

### Effort Summary

| Phase | Items | Effort (hours) |
|-------|-------|----------------|
| Phase A | CWI-01, CWI-04 | 2.5-3.5 |
| Phase B | CWI-02, CWI-03 | 6-9 |
| Phase C | CWI-05, CWI-06, CWI-07 | 5-7 |
| Phase D | CWI-08, CWI-09 | 7 |
| **Total** | **9 items** | **20.5-26.5 hours** |

**Comparison to SPIKE-001:** 14 items at 25-37 hours --> 9 items at 20.5-26.5 hours. Reduction: 5 fewer items, 4.5-10.5 hours saved (18-28% reduction).

---

## Evidence

### Phase 1 Audit References

All claims in this analysis reference specific findings from the Phase 1 CLI Capability Audit (`projects/PROJ-004-context-resilience/orchestration/spike002-cli-integration-20260219-001/res/phase-1-audit/cli-auditor/cli-capability-audit.md`).

| Claim | Audit Section | Evidence |
|-------|--------------|----------|
| `LayeredConfigAdapter` is direct fit for threshold config | C3: Configuration Management | 4-level precedence, TOML parsing, dot-notation, CLI commands operational |
| `PromptReinforcementEngine` pattern for context injection | C4: Enforcement Engine Infrastructure | L2 engine reads quality-enforcement.md, parses L2-REINJECT markers, 600-token budget |
| `SessionQualityContextGenerator` pattern for resumption | C4: Enforcement Engine Infrastructure | L1 engine generates XML preamble, ~700 token budget, injected at session start |
| `UserPromptSubmit` hook is primary extension point | C5: Hook Integration Points | Hook operational, injection pattern proven, `additionalContext` field |
| `FileSystemEventStore` JSONL pattern for checkpoints | C6: Local Context Persistence | JSONL append-only, file locking, directory creation pattern |
| `AtomicFileAdapter` for safe checkpoint writes | C6: Local Context Persistence | Safe file I/O with locking, reusable for checkpoint writing |
| `InMemorySessionRepository` not persistent | C2: Session Lifecycle Management | Line 35: "Loses data on process termination" |
| ECW status line has context data unavailable to hooks | C8: ECW Status Line | Confirms GAP-003; status line reads `context_window.current_usage` but hooks cannot |
| Item classifications (REUSE/EXTEND/NEW) | Mapping to SPIKE-001 Items | 1 REUSE, 10 EXTEND, 3 NEW |

### SPIKE-001 Synthesis References

All SPIKE-001 follow-up items referenced from the SPIKE-001 Research Synthesis (`projects/PROJ-004-context-resilience/orchestration/spike001-ctxres-20260219-001/res/phase-7-synthesis/spike-synthesizer/spike-synthesis.md`).

| Reference | Synthesis Section | Content |
|-----------|------------------|---------|
| 14 follow-up work items | Follow-Up Work Items | Priority-ordered list with type, priority, rationale, effort estimates |
| Five-tier threshold model | L1 Detailed Findings, Hypothesis 2 | NOMINAL/LOW/WARNING/CRITICAL/EMERGENCY + COMPACTION |
| Enhanced resumption schema v2.0 | L1 Detailed Findings, Hypothesis 3 | 7 sub-sections, 23 fields |
| Template 1 and Template 2 | L1 Detailed Findings, Hypothesis 4 | Resumption prompt (~760 tokens), Compaction alert (~280 tokens) |
| AE-006 sub-rules | L2 Architecture Implications | AE-006a through AE-006e with trigger/escalation/enforcement |
| Open questions OQ-1, OQ-9 | Open Questions | Method C feasibility, input_tokens accuracy |
| InMemorySessionRepository limitation | L1 Detailed Findings | Session state not persistent across processes |

### Architecture Standards References

Hexagonal architecture placement decisions reference `.context/rules/architecture-standards.md`:

| Decision | Standard | Reference |
|----------|----------|-----------|
| New bounded context for context_monitoring | "Bounded contexts SHOULD communicate via domain events or shared kernel only" | Standards (MEDIUM), Pattern Guidance |
| Phase 1 infrastructure placement | Directory structure: `infrastructure/internal/enforcement/` | Directory Structure |
| Phase 2 extraction to full bounded context | Layer dependencies: domain/application/infrastructure | Layer Dependencies |
| One class per file for new engines | H-10: "Each Python file SHALL contain exactly ONE public class or protocol" | HARD Rules |

---

## Self-Review (S-010) Verification

- [x] Every SPIKE-001 item (#1 through #14) is covered in the per-item analysis (14 sub-sections in L1)
- [x] Consolidation decisions are justified with clear rationale (4 merges with specific reasons, 1 non-merge with rejection rationale)
- [x] Architectural placement follows hexagonal architecture principles from `.context/rules/architecture-standards.md` (new bounded context decision with Phase 1/Phase 2 migration path)
- [x] Risk analysis addresses the InMemorySessionRepository limitation (R1, rated HIGH, with immediate and future mitigations)
- [x] Revised work items are independently testable and deployable (each CWI has acceptance criteria with test requirements)
- [x] Effort estimates are defensible (each revised estimate includes savings rationale relative to original)
- [x] All claims reference Phase 1 audit evidence (Evidence section maps claims to audit sections)
- [x] Dependency graph provided with implementation order
- [x] Navigation table present with anchor links (H-23/H-24 compliance)
- [x] Process boundary risk documented (R2, R3, R5)
- [x] Auto-escalation implications noted (CWI-05: AE-002 applies to quality-enforcement.md changes)
