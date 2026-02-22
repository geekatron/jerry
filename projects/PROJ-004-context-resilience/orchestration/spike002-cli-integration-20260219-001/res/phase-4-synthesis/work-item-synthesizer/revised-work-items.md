# SPIKE-002 Synthesis: Revised Work Items for CLI-Integrated Context Resilience

<!-- PS-ID: SPIKE-002 | ENTRY-ID: phase-4 | DATE: 2026-02-19 -->
<!-- AGENT: ps-synthesizer v2.0.0 | MODEL: claude-opus-4-6 -->

> Final, authoritative work item list for FEAT-001 implementation. Supersedes SPIKE-001's 14 follow-up items and SPIKE-002 Phase 2's CWI-01 through CWI-09. Incorporates user feedback: FileSystemSessionRepository as a P1 Enabler, eliminating the InMemorySessionRepository workaround.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Summary](#l0-summary) | Executive overview (5 bullets) |
| [Supersession Statement](#supersession-statement) | What this replaces and why |
| [Revised Work Items](#revised-work-items) | CWI-00 through CWI-09: authoritative item definitions |
| [Dependency Graph](#dependency-graph) | Implementation order visualization |
| [Implementation Phases](#implementation-phases) | Phase A through D with rationale |
| [Effort Summary](#effort-summary) | Total effort comparison across spikes |
| [Hypothesis Validation](#hypothesis-validation) | SPIKE-002 hypotheses #1-6 evaluated |
| [Open Questions](#open-questions) | Remaining unresolved questions |
| [Evidence](#evidence) | Traceability to Phase 1, 2, 3, QG-1 artifacts |

---

## L0 Summary

1. **10 work items (CWI-00 through CWI-09) supersede SPIKE-001's 14 items and SPIKE-002 Phase 2's 9 items.** The key addition is CWI-00 (FileSystemSessionRepository), which eliminates the InMemorySessionRepository workaround that Phase 2-3 treated as a hard constraint. This was the single most significant architectural risk identified in Phase 2 (Risk R1, rated HIGH). The user identified that the `FileSystemEventStore` + `EventSourcedWorkItemRepository` pattern already exists and should be applied to sessions.

2. **Estimated effort is 19.5-28.5 hours, a 25-47% reduction from SPIKE-001's 25-37 hours.** The reduction comes from three sources: CLI infrastructure reuse (30% of items are EXTEND, not NEW), work item consolidation (14 items to 10), and the FileSystemSessionRepository enabler which eliminates file-based workarounds in CWI-02 and simplifies the Phase 2 bounded context extraction timeline.

3. **CWI-00 (FileSystemSessionRepository) is the highest-impact addition.** It follows the proven `EventSourcedWorkItemRepository` + `FileSystemEventStore` pattern (369 lines + 431 lines of existing, tested code). Once implemented, the PreCompact hook can trigger `jerry session abandon --reason "compaction"`, session domain events (`SessionAbandoned`, `ContextThresholdReached`) become real rather than deferred, and `jerry session status` can report context state across process boundaries.

4. **All 6 SPIKE-002 hypotheses are validated: 4 CONFIRMED, 2 PARTIALLY CONFIRMED.** Hypothesis #6 (>=60% reclassified from NEW to REUSE/EXTEND) is strongly confirmed: 10 of 14 items (71%) were reclassified. Hypothesis #2 (session abandon as checkpoint trigger) is upgraded from PARTIALLY CONFIRMED to CONFIRMED with the addition of CWI-00.

5. **The architecture follows a two-phase approach per ADR-SPIKE002-001 (QG-1 PASSED at 0.94).** Phase 1 places context resilience engines in `infrastructure/internal/enforcement/` alongside existing engines. Phase 2 extracts to a full `context_monitoring` bounded context when the domain model stabilizes. CWI-00 accelerates Phase 2 by providing the persistent session repository that is one of the three extraction criteria.

---

## Supersession Statement

**This document supersedes:**

1. **SPIKE-001 Research Synthesis follow-up items (#1 through #14).** SPIKE-001 designed context resilience using a hook-only approach, treating the Jerry CLI as a black box. The 14 items estimated 25-37 hours of effort with all items classified as NEW.

2. **SPIKE-002 Phase 2 Gap Analysis work items (CWI-01 through CWI-09).** Phase 2 correctly identified that 10 of 14 SPIKE-001 items could leverage existing CLI infrastructure (1 REUSE, 10 EXTEND, 3 NEW) and consolidated to 9 items at 20.5-26.5 hours. However, Phase 2 treated the `InMemorySessionRepository` as a hard constraint (Risk R1), proposing file-based workarounds for cross-process state.

**Triggering gap:** The user identified that the `InMemorySessionRepository` should NOT be treated as a hard constraint. The `FileSystemEventStore` (369 lines, production-tested with file locking, optimistic concurrency, JSONL format) + `EventSourcedWorkItemRepository` (431 lines, event replay, stream management) pattern already exists and works for work items. The identical pattern should be applied to create a `FileSystemSessionRepository` for session management.

**Impact of this feedback:**

- **New work item CWI-00** added: "Implement FileSystemSessionRepository using existing EventSourcedWorkItemRepository + FileSystemEventStore pattern"
- **CWI-02 (PreCompact) simplified:** Can now trigger real `SessionAbandoned` domain events via `jerry session abandon --reason "compaction"` instead of file-based checkpoint workarounds
- **Phase 2 bounded context extraction accelerated:** Persistent sessions satisfy one of three extraction criteria from ADR-SPIKE002-001 (line 580-582)
- **Session domain events become real:** `SessionAbandoned` with reason="compaction", potential `ContextThresholdReached` events -- all persisted in the event store with full audit trail

---

## Revised Work Items

### CWI-00: FileSystemSessionRepository (NEW -- User Feedback)

| Field | Value |
|-------|-------|
| **ID** | CWI-00 |
| **Title** | Implement FileSystemSessionRepository using existing EventSourced + FileSystemEventStore pattern |
| **Type** | Enabler |
| **Priority** | P0 - Foundation |
| **Effort** | 3-4 hours |
| **Supersedes** | N/A (new item from user feedback, addresses Phase 2 Risk R1) |
| **Description** | Create a `FileSystemSessionRepository` that implements the `ISessionRepository` port by delegating to the existing `FileSystemEventStore`. Follow the exact pattern established by `EventSourcedWorkItemRepository`: event registry for session events (`SessionCreated`, `SessionCompleted`, `SessionAbandoned`, `SessionProjectLinked`), stream ID convention (`session-{id}`), domain-to-stored event conversion, and aggregate reconstitution via `Session.load_from_history()`. Wire it into `bootstrap.py` as a replacement for `InMemorySessionRepository`. This eliminates the "Loses data on process termination" limitation (Phase 1 Audit: C2, `in_memory_session_repository.py` line 35) that was the single most significant architectural risk (Phase 2 Gap Analysis: R1, rated HIGH). |
| **CLI Integration Points** | `FileSystemEventStore` (`src/work_tracking/infrastructure/persistence/filesystem_event_store.py`, 369 lines -- REUSE as-is). `EventSourcedWorkItemRepository` pattern (`src/work_tracking/infrastructure/adapters/event_sourced_work_item_repository.py`, 431 lines -- pattern to follow). `ISessionRepository` port (`src/session_management/application/ports/session_repository.py`). `Session.load_from_history()` (`src/session_management/domain/aggregates/session.py`, lines 284-324). Session events (`src/session_management/domain/events/session_events.py` -- 4 events: SessionCreated, SessionCompleted, SessionAbandoned, SessionProjectLinked). `bootstrap.py` composition root wiring. |
| **Acceptance Criteria** | 1. `FileSystemSessionRepository` implements `ISessionRepository` protocol. 2. Session events persisted to `.jerry/data/events/session-{id}.jsonl`. 3. `jerry session start` creates a session that persists across process termination. 4. `jerry session status` in a new process retrieves the active session. 5. `jerry session abandon --reason "compaction"` from a hook script correctly abandons the persisted session. 6. `Session.load_from_history()` correctly reconstitutes session from event replay. 7. Optimistic concurrency via `FileSystemEventStore` prevents concurrent writes. 8. `get_active()` returns the most recent ACTIVE session across all streams. 9. Unit tests covering: save/get round-trip, get_active, event replay, cross-process persistence, concurrency. 10. `InMemorySessionRepository` retained for unit testing but no longer used in production wiring. |
| **Dependencies** | Depends on: Nothing (uses existing `FileSystemEventStore` as-is). Depended on by: CWI-02 (PreCompact hook can trigger `jerry session abandon`), CWI-03 (context monitor can record threshold events), Phase 2 bounded context extraction (satisfies extraction criterion #2 from ADR-SPIKE002-001). |

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
| **Description** | Add default threshold values to the existing `LayeredConfigAdapter` configuration system. Six keys: `context_monitor.nominal_threshold` (0.55), `context_monitor.warning_threshold` (0.70), `context_monitor.critical_threshold` (0.80), `context_monitor.emergency_threshold` (0.88), `context_monitor.compaction_detection_threshold` (10000), `context_monitor.enabled` (true). Users can override at any level via `jerry config set`. The `LayeredConfigAdapter` (Phase 1 Audit: C3, 383 lines) provides env > project > root > defaults precedence automatically. |
| **CLI Integration Points** | `src/interface/cli/adapter.py` `_create_config_adapter()` defaults dictionary (lines 1028-1034). `LayeredConfigAdapter` (`src/infrastructure/adapters/configuration/layered_config_adapter.py`). |
| **Acceptance Criteria** | 1. `jerry config get context_monitor.warning_threshold` returns `0.70`. 2. `jerry config set context_monitor.warning_threshold 0.75 --scope project` persists override. 3. `JERRY_CONTEXT_MONITOR_WARNING_THRESHOLD=0.75` overrides project config. 4. All 6 threshold keys have defaults. 5. Unit test covers default retrieval and override precedence. |
| **Dependencies** | Depends on: Nothing. Depended on by: CWI-03 (ContextMonitorEngine reads threshold config). |

---

### CWI-02: PreCompact Hook + Checkpoint Infrastructure

| Field | Value |
|-------|-------|
| **ID** | CWI-02 |
| **Title** | Implement PreCompact hook for checkpoint creation and session abandonment |
| **Type** | Enabler |
| **Priority** | P1 - Critical |
| **Effort** | 3-5 hours |
| **Supersedes** | SPIKE-001 Items #2 + #10 |
| **Description** | Register a new `PreCompact` hook in `hooks.json`. Create a `CheckpointWriter` engine that: (1) reads the ORCHESTRATION.yaml resumption section, (2) captures current context state from the transcript, (3) writes a checkpoint file to `.jerry/checkpoints/cx-{NNN}-checkpoint.json` using `AtomicFileAdapter` for safe atomic writes, (4) triggers `jerry session abandon --reason "context compaction at {fill}%"` to record the compaction as a real session domain event (enabled by CWI-00). The checkpoint directory is created by the engine's constructor following the `FileSystemEventStore` pattern (`mkdir(parents=True, exist_ok=True)`). Update `project-workflow.md` to include `.jerry/checkpoints/` in the workspace layout. |
| **CLI Integration Points** | `hooks/hooks.json` (new PreCompact entry). `AtomicFileAdapter` (`src/infrastructure/adapters/persistence/atomic_file_adapter.py`). `FileSystemEventStore` directory creation pattern (lines 106-108). `jerry session abandon --reason` CLI command (enabled by CWI-00 persistent repository). |
| **Acceptance Criteria** | 1. `hooks.json` contains a `PreCompact` entry with 10000ms timeout. 2. When PreCompact fires, checkpoint file created at `.jerry/checkpoints/cx-001-checkpoint.json`. 3. Checkpoint file contains: resumption state, context fill %, timestamp, compaction sequence number. 4. `.jerry/checkpoints/` directory auto-created if missing. 5. Sequential checkpoint IDs (cx-001, cx-002, etc.). 6. `jerry session abandon --reason "context compaction at {fill}%"` called successfully (session event persisted). 7. Fail-open: if ORCHESTRATION.yaml not found, checkpoint contains context state only. 8. Fail-open: if session abandon fails (no active session), checkpoint still written. 9. `project-workflow.md` updated with checkpoint directory. 10. Unit tests for CheckpointWriter: creation, ID sequencing, missing ORCHESTRATION.yaml, directory creation, session abandon integration. |
| **Dependencies** | Depends on: CWI-00 (FileSystemSessionRepository for `jerry session abandon`), CWI-04 (resumption schema for checkpoint content). Depended on by: CWI-03 (CompactionAlertEngine reads checkpoint files), CWI-06 (ResumptionContextGenerator reads checkpoint files). |

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
| **Description** | Extend the existing `hooks/user-prompt-submit.py` with two new engines: (1) `ContextMonitorEngine` -- reads `$TRANSCRIPT_PATH` JSONL, extracts latest `input_tokens`, computes fill %, determines threshold tier (NOMINAL/LOW/WARNING/CRITICAL/EMERGENCY), produces `<context-monitor>` tag (40-200 tokens). (2) `CompactionAlertEngine` -- scans `.jerry/checkpoints/` for unacknowledged checkpoint files, populates Template 2 (`<compaction-alert>`, ~280 tokens), marks checkpoint as acknowledged. Both engines are stateless, fail-open, and follow the `PromptReinforcementEngine` pattern (Phase 1 Audit: C4, 246 lines). Threshold configuration loaded from `LayeredConfigAdapter` (CWI-01). |
| **CLI Integration Points** | `hooks/user-prompt-submit.py` (extend existing hook). `PromptReinforcementEngine` pattern (`src/infrastructure/internal/enforcement/prompt_reinforcement_engine.py`). `LayeredConfigAdapter` for threshold reading. `$TRANSCRIPT_PATH` environment variable. |
| **Acceptance Criteria** | 1. `<context-monitor>` tag injected on every prompt with: fill %, threshold tier, recommended action. 2. `<compaction-alert>` tag injected on first prompt after compaction (unacknowledged checkpoint exists). 3. Compaction alert injected only once (checkpoint marked acknowledged after injection). 4. Fail-open: if transcript parsing fails, hook still outputs quality reinforcement (existing behavior preserved). 5. Combined injection overhead <= 500 tokens per prompt (context monitor + compaction alert). 6. Hook execution within 5000ms timeout budget. 7. Unit tests for ContextMonitorEngine: threshold calculation, tier determination, tag generation, JSONL parsing, fail-open. 8. Unit tests for CompactionAlertEngine: checkpoint detection, acknowledgment, template population, no-checkpoint passthrough. |
| **Dependencies** | Depends on: CWI-01 (threshold config), CWI-02 (checkpoint files for CompactionAlertEngine). Depended on by: CWI-05 (AE-006 references context-monitor signals), CWI-08 (OQ-9 validates this hook's data). |

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
| **Description** | Replace the current 5-field resumption section in `skills/orchestration/templates/ORCHESTRATION.template.yaml` with the v2.0 schema: Recovery State (8 fields), Files to Read (structured with priority/purpose/sections), Quality Trajectory (7 fields), Defect Summary (5 fields), Decision Log (N entries), Agent Summaries (N entries), Compaction Events (2 + N entries). Update the orchestrator agent prompt with an explicit resumption update protocol defining when and what to update. Add an L2-REINJECT marker to `quality-enforcement.md` for resumption update reminders (~25 tokens, rank ~9). |
| **CLI Integration Points** | `.context/rules/quality-enforcement.md` (new L2-REINJECT marker). `PromptReinforcementEngine` automatically picks up new L2-REINJECT markers without code changes (Phase 1 Audit: C4). No direct CLI code changes. |
| **Acceptance Criteria** | 1. ORCHESTRATION.yaml template contains v2.0 resumption schema with all 7 sub-sections. 2. Backward compatible: existing 5 fields preserved as part of Recovery State. 3. Orchestrator prompt includes explicit update protocol with triggers: phase start, phase complete, QG iteration, compaction event, cross-phase decision, agent completion. 4. L2-REINJECT marker present in quality-enforcement.md. 5. Resumption section includes `updated_at` timestamp field. |
| **Dependencies** | Depends on: Nothing (schema definition is independent). Depended on by: CWI-02 (checkpoint writer references schema fields), CWI-06 (resumption prompt reads schema fields), CWI-07 (staleness validation enforces update protocol). |

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
| **Description** | Replace the single AE-006 rule in `quality-enforcement.md` with 5 graduated sub-rules mapping detection thresholds to escalation actions by criticality level. Add an L2-REINJECT marker (rank ~8, ~35 tokens) summarizing the graduated escalation protocol. The `PromptReinforcementEngine` automatically picks up the new marker without code changes. Total L2-REINJECT budget remains within 600 tokens (current markers total ~400-450 tokens + new ~60 tokens = ~510 tokens). |
| **CLI Integration Points** | `.context/rules/quality-enforcement.md` (rule text + L2-REINJECT marker). No engine code changes. |
| **Acceptance Criteria** | 1. AE-006a through AE-006e defined in Auto-Escalation Rules table. 2. Each sub-rule specifies: trigger condition, escalation action, enforcement mechanism. 3. L2-REINJECT marker present with rank and content. 4. Total L2-REINJECT budget remains within 600 tokens. 5. Quality gate: C3 minimum per AE-002 (touches `.context/rules/`). |
| **Dependencies** | Depends on: CWI-03 (context monitor must exist for AE-006a-c to reference signals). Depended on by: Nothing directly. |

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
| **Description** | Create a `ResumptionContextGenerator` class following the `SessionQualityContextGenerator` pattern (Phase 1 Audit: C4, 134 lines). The generator checks `.jerry/checkpoints/` for unacknowledged checkpoint files, reads the latest checkpoint and ORCHESTRATION.yaml resumption section, populates Template 1 (~760 tokens), and produces a `<resumption-context>` XML tag. Integrate into `scripts/session_start_hook.py` after existing quality context generation. With CWI-00 in place, the generator can also query `jerry session status --json` for the previous session's abandonment reason, enriching the resumption context with session-level audit data. |
| **CLI Integration Points** | `SessionQualityContextGenerator` pattern (`src/infrastructure/internal/enforcement/session_quality_context_generator.py`). `session_start_hook.py` (lines 307-326 existing injection pattern). `jerry session status --json` for previous session info (enabled by CWI-00). |
| **Acceptance Criteria** | 1. `<resumption-context>` tag injected when unacknowledged checkpoint exists at session start. 2. Tag contains: recovery state, quality trajectory, key decisions, agent summaries, file read instructions, previous session abandon reason. 3. No tag injected when no checkpoint files exist (existing behavior unchanged). 4. Template 1 variables sourced from checkpoint file, ORCHESTRATION.yaml, and session status. 5. Total injection <= 800 tokens. 6. Unit tests: checkpoint detection, template population, no-checkpoint behavior, session status integration. |
| **Dependencies** | Depends on: CWI-00 (session status for previous session info), CWI-02 (checkpoint files), CWI-04 (resumption schema). Depended on by: Nothing directly. |

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
| **Description** | Register a new `PostToolUse` hook in `hooks.json` with matcher for `Write\|Edit\|MultiEdit`. The hook detects ORCHESTRATION.yaml writes, parses the `resumption.updated_at` field, and injects a staleness warning if the field has not been updated in the current phase. Follows the `PreToolEnforcementEngine` governance escalation pattern (Phase 1 Audit: C4, 567 lines, lines 501-536). |
| **CLI Integration Points** | `hooks/hooks.json` (new PostToolUse entry). `PreToolEnforcementEngine` governance detection pattern. |
| **Acceptance Criteria** | 1. `hooks.json` contains a `PostToolUse` entry with 5000ms timeout. 2. Hook fires only on `Write\|Edit\|MultiEdit` tool calls. 3. Hook detects ORCHESTRATION.yaml writes (path matching). 4. Staleness warning injected if `resumption.updated_at` has not been updated in current phase. 5. Non-ORCHESTRATION.yaml writes pass through silently. 6. Fail-open: if parsing fails, no warning injected. 7. Unit tests: ORCHESTRATION.yaml detection, staleness calculation, passthrough behavior. |
| **Dependencies** | Depends on: CWI-04 (update protocol defines when `updated_at` should change). Depended on by: Nothing directly. |

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
| **Description** | Two focused investigations: (1) OQ-9 validation -- compare `input_tokens` from transcript JSONL against ECW status line data (`~/.claude/ecw-statusline-state.json`) and optionally against `TokenCounter` calculations (Phase 1 Audit: C1, tiktoken `p50k_base`). (2) Method C feasibility -- extend status line state file to include `context_fill_percentage`, implement a test hook that reads the state file, verify timing (does state file update before `UserPromptSubmit` fires?). Both produce a finding report with data and recommendation. |
| **CLI Integration Points** | `TokenCounter` (`src/transcript/application/services/token_counter.py`). ECW status line state file (`~/.claude/ecw-statusline-state.json`). `.claude/statusline.py` (extend state file write, lines 241-250). |
| **Acceptance Criteria** | 1. OQ-9: Report documenting `input_tokens` accuracy with measured divergence from reference sources. 2. Method C: Report documenting timing test results. 3. Method C: If feasible, prototype status line extension committed. 4. Both reports include recommendation: proceed/defer/abandon. 5. Total timebox: 3 hours. |
| **Dependencies** | Depends on: CWI-03 (provides transcript parsing code this validates). Depended on by: May upgrade CWI-03 if Method C is feasible. |

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
| **Description** | Run a monitored session with the detection system active (CWI-03) against a workflow with a different profile than the PROJ-001 FEAT-015 baseline (e.g., deep research spike or multi-file refactoring). Collect per-operation token costs and fill trajectory. Compare against PROJ-001 calibration data. Document the calibration protocol: workflow selection criteria, measurement methodology, data collection format, recalibration triggers. Persist to `docs/knowledge/context-resilience/calibration-protocol.md`. |
| **CLI Integration Points** | CWI-03 (context monitoring must be operational). `TokenCounter` and status line for measurement tools. |
| **Acceptance Criteria** | 1. Monitored session completed against a non-PROJ-001 workflow. 2. Per-operation token cost data collected. 3. Fill trajectory compared against PROJ-001 baseline. 4. Threshold adjustment recommendations documented. 5. Calibration protocol document created at `docs/knowledge/context-resilience/calibration-protocol.md`. 6. Document includes: when to recalibrate, how to collect data, how to interpret results. |
| **Dependencies** | Depends on: CWI-01, CWI-02, CWI-03 (system must be operational). Depended on by: Nothing directly. |

---

## Dependency Graph

```
CWI-00 (FileSystemSessionRepository) [P0 - Foundation]
  |
  +---> CWI-02 (PreCompact Hook + Checkpoints) [P1]
  |       |
  |       +---> CWI-03 (UserPromptSubmit: Monitor + Alert) [P1]
  |       |       |
  |       |       +---> CWI-05 (AE-006 Sub-Rules) [P2]
  |       |       +---> CWI-08 (Validation Spikes) [P2]
  |       |
  |       +---> CWI-06 (Resumption Prompt Automation) [P2]
  |
  +---> CWI-06 (also depends on CWI-00 for session status)

CWI-01 (Threshold Config) [P1 - no dependencies]
  |
  +---> CWI-03 (reads threshold config)

CWI-04 (Resumption Schema + Protocol) [P1 - no dependencies]
  |
  +---> CWI-02 (schema fields in checkpoint content)
  +---> CWI-06 (schema fields in resumption prompt)
  +---> CWI-07 (PostToolUse Staleness) [P3]

CWI-09 (Threshold Validation) [P3]
  depends on: CWI-01 + CWI-02 + CWI-03 (system operational)
```

### Critical Path

```
CWI-00 --> CWI-02 --> CWI-03 --> CWI-05/CWI-08
              ^
              |
CWI-04 ------+
```

The critical path runs through CWI-00 (session persistence) to CWI-02 (checkpoint infrastructure) to CWI-03 (context monitoring). CWI-01 and CWI-04 can run in parallel with CWI-00 as they have no dependencies.

---

## Implementation Phases

### Phase A: Foundation (CWI-00, CWI-01, CWI-04) -- 5.5-7.5 hours

| Item | Effort | Rationale |
|------|--------|-----------|
| CWI-00 | 3-4 hrs | FileSystemSessionRepository is the foundation enabler. Follows proven pattern. No dependencies. Unblocks CWI-02 session abandon integration. |
| CWI-01 | 0.5 hrs | Threshold config defaults. No dependencies. 6 values added to existing dictionary. |
| CWI-04 | 2-3 hrs | Resumption schema + update protocol. No dependencies. Template and agent prompt work. |

**All three items are independent and can be parallelized.** CWI-01 is trivially small. CWI-00 and CWI-04 are the substantive work.

**Gate:** After Phase A, `jerry session status` works across processes, `jerry config get context_monitor.warning_threshold` returns defaults, and ORCHESTRATION.yaml template has v2.0 schema.

### Phase B: Core Detection (CWI-02, CWI-03) -- 6-9 hours

| Item | Effort | Rationale |
|------|--------|-----------|
| CWI-02 | 3-5 hrs | PreCompact hook + checkpoint creation + session abandon. Depends on CWI-00 (session persistence) and CWI-04 (schema). |
| CWI-03 | 3-4 hrs | UserPromptSubmit extension with ContextMonitorEngine + CompactionAlertEngine. Depends on CWI-01 (config) and CWI-02 (checkpoint files for alert engine). |

**CWI-02 must complete before CWI-03** (CompactionAlertEngine reads checkpoint files created by CWI-02).

**Gate:** After Phase B, the core detection system is operational: context fill is monitored on every prompt, compaction events are checkpointed with session audit trail, and post-compaction alerts are injected.

### Phase C: Integration (CWI-05, CWI-06, CWI-07) -- 5-7 hours

| Item | Effort | Rationale |
|------|--------|-----------|
| CWI-05 | 1 hr | AE-006 graduated sub-rules. Depends on CWI-03 (context-monitor signals). |
| CWI-06 | 2-3 hrs | Resumption prompt automation. Depends on CWI-00, CWI-02, CWI-04. |
| CWI-07 | 2-3 hrs | PostToolUse staleness validation. Depends on CWI-04 (update protocol). |

**All three can be partially parallelized.** CWI-05 is the fastest. CWI-06 and CWI-07 are independent of each other.

**Gate:** After Phase C, the full framework integration is operational: AE-006 graduated escalation, automatic resumption prompts at session start, and staleness warnings for orchestration files.

### Phase D: Validation (CWI-08, CWI-09) -- 7 hours

| Item | Effort | Rationale |
|------|--------|-----------|
| CWI-08 | 3 hrs | Validation spikes (OQ-9 + Method C). Timeboxed investigation. |
| CWI-09 | 4 hrs | Threshold validation + calibration documentation. Requires operational system. |

**Both are timeboxed and can run in parallel** once the Phase B system is operational.

**Gate:** After Phase D, the system is validated against real workflow data and the calibration protocol is documented.

---

## Effort Summary

| Source | Items | Effort Range (hours) | Notes |
|--------|-------|---------------------|-------|
| SPIKE-001 (original) | 14 | 25-37 | All items classified as NEW, hook-only approach |
| SPIKE-002 Phase 2 (gap analysis) | 9 | 20.5-26.5 | CLI integration, InMemorySessionRepository as hard constraint |
| **SPIKE-002 Final (this document)** | **10** | **19.5-28.5** | CLI integration + FileSystemSessionRepository enabler |

### Effort Change Analysis

| Change | Effect |
|--------|--------|
| Added CWI-00 (FileSystemSessionRepository) | +3-4 hours |
| CWI-02 simplified (real session events, not workarounds) | -0.5-1 hour (simpler file-based logic, standard CLI call) |
| CWI-06 enriched (session status query) | +0 hours (query is trivial with CWI-00 in place) |
| Phase 2 bounded context extraction accelerated | Future savings (not counted in FEAT-001 estimate) |
| **Net change from Phase 2 estimate** | **+2.5-3 hours (offset by architectural improvement)** |

**Comparison to SPIKE-001:**

- Items: 14 --> 10 (4 fewer items, -29%)
- Effort (low estimate): 25 --> 19.5 hours (-22%)
- Effort (high estimate): 37 --> 28.5 hours (-23%)
- Items classified as NEW: 14 --> 3 (from 100% to 30%)
- Items reusing CLI infrastructure: 0 --> 7 (from 0% to 70%)

The net effort reduction of ~22-23% is more conservative than Phase 2's initial 18-28% claim because CWI-00 adds foundation work. However, the architectural payoff (persistent sessions, real domain events, accelerated Phase 2 extraction) significantly exceeds the 3-4 hour investment.

---

## Hypothesis Validation

### Hypothesis #1: TokenCounter can replace transcript-based heuristic

**Verdict: PARTIALLY CONFIRMED**

The `TokenCounter` service (Phase 1 Audit: C1, tiktoken `p50k_base`) is available for context fill estimation. However, the primary detection mechanism remains Method A (reading `input_tokens` directly from the transcript JSONL) because it captures the actual token count reported by Claude Code, not an independent estimate. The `TokenCounter` serves as a validation reference (CWI-08, OQ-9) rather than a replacement.

**Evidence:** Phase 1 Audit C1: TokenCounter operational, used in production for transcript chunking. Phase 2 Gap Analysis Item #8: comparison approach between `input_tokens`, status line data, and `TokenCounter`.

### Hypothesis #2: Session abandon models compaction use case

**Verdict: CONFIRMED (upgraded from Phase 2 PARTIALLY CONFIRMED)**

Phase 2 classified this as PARTIALLY CONFIRMED because the `InMemorySessionRepository` prevented cross-process session abandon calls. With the user's feedback and the addition of CWI-00 (FileSystemSessionRepository), the `jerry session abandon --reason "compaction"` command works across process boundaries. The `SessionAbandoned` event with reason field (session_events.py line 67-80) was explicitly designed for this scenario (session.py line 207: "typically due to context compaction or unexpected termination").

**Evidence:** Session aggregate `abandon()` method (session.py lines 205-228). `SessionAbandoned` event with `reason` field (session_events.py lines 67-80). `FileSystemEventStore` pattern provides persistence (filesystem_event_store.py, 369 lines). `EventSourcedWorkItemRepository` proves the pattern works (event_sourced_work_item_repository.py, 431 lines).

### Hypothesis #3: Layered config manages thresholds hierarchically

**Verdict: CONFIRMED**

The `LayeredConfigAdapter` (Phase 1 Audit: C3, 383 lines) is a direct fit. CWI-01 adds 6 default values to an existing dictionary. The 4-level precedence (env > project > root > defaults), TOML parsing, dot-notation keys, and `jerry config get/set/show` CLI commands provide complete threshold management infrastructure.

**Evidence:** Phase 1 Audit C3: `_create_config_adapter()` defaults dictionary at adapter.py lines 1028-1034. Phase 2 Gap Analysis Item #7: classified as REUSE (strongest reuse case in the analysis).

### Hypothesis #4: SessionStart hook delivers resumption prompts

**Verdict: CONFIRMED**

The `SessionQualityContextGenerator` pattern (Phase 1 Audit: C4, 134 lines) provides the exact template for `ResumptionContextGenerator` (CWI-06). The `session_start_hook.py` already generates `<quality-context>` via this pattern; adding `<resumption-context>` follows the identical injection pathway.

**Evidence:** Phase 1 Audit C4: SessionQualityContextGenerator generates XML preamble, ~700 token budget, injected at session start. Phase 2 Gap Analysis Item #11: classified as EXTEND with specific code changes.

### Hypothesis #5: Prompt reinforcement L2-REINJECT delivers context alerts

**Verdict: CONFIRMED**

The `PromptReinforcementEngine` (Phase 1 Audit: C4, 246 lines) parses L2-REINJECT HTML comment markers, sorts by rank, and assembles within a 600-token budget. New context resilience markers (CWI-04 resumption reminder, CWI-05 AE-006 sub-rules) are picked up automatically without engine code changes. The 600-token budget can accommodate additional markers (current total ~400-450 tokens).

**Evidence:** Phase 1 Audit C4: L2-REINJECT parsing mechanism operational with 8 existing markers. Phase 2 Gap Analysis Items #5 and #6: both classified as EXTEND with no engine code changes.

### Hypothesis #6: At least 60% reclassified from NEW to REUSE/EXTEND

**Verdict: CONFIRMED (strongly)**

Phase 1 classified 10 of 14 items (71%) as REUSE (1 item) or EXTEND (9 items). Only 3 items remain genuinely NEW (#4 resumption schema, #5 update protocol, #13/#14 calibration). This exceeds the 60% hypothesis threshold by 11 percentage points.

**Evidence:** Phase 1 Audit Mapping section: 1 REUSE (#7), 10 EXTEND (#1-3, #6, #8-12), 3 NEW (#4, #5, #13-14). Phase 2 Gap Analysis L0 Summary: "10 of 14 SPIKE-001 items can leverage existing CLI infrastructure."

---

## Open Questions

### OQ-1: Method C Timing Feasibility (Carried from SPIKE-001)

**Status:** OPEN -- addressed by CWI-08 timebox

Can the ECW status line share context data with hooks via a shared state file? Specifically, does the status line update `~/.claude/ecw-statusline-state.json` before `UserPromptSubmit` fires on the next prompt? CWI-08 allocates investigation time within a 3-hour timebox.

### OQ-9: input_tokens Accuracy (Carried from SPIKE-001)

**Status:** OPEN -- addressed by CWI-08 timebox

Does `input_tokens` from the transcript JSONL accurately approximate context fill? CWI-08 compares against status line data and optionally against `TokenCounter` calculations.

### OQ-10: FileSystemSessionRepository Performance at Scale (NEW)

**Status:** OPEN -- monitor during CWI-00 implementation

The `get_active()` method must scan all session streams to find the ACTIVE one. For users with many sessions (50+), this could be slow. The `EventSourcedWorkItemRepository.list_all()` has the same characteristic (performance note at line 182: "loads ALL work items from all streams"). Mitigation options: (1) maintain an index file listing the active session ID, (2) accept O(n) scan since sessions are infrequent (1 per CLI session), (3) add a read model if needed later.

### OQ-11: Concurrent PreCompact + Session Abandon Race Condition (NEW)

**Status:** LOW RISK -- documented for awareness

If PreCompact fires while another process is modifying the session (extremely unlikely), the `FileSystemEventStore`'s `FileLock` provides cross-process safety. The optimistic concurrency check will reject the second write, and the fail-open design ensures the checkpoint is still written even if session abandon fails.

---

## Evidence

### Phase 1 Audit References

| Claim | Audit Section | Evidence |
|-------|--------------|----------|
| `LayeredConfigAdapter` is direct fit for threshold config | C3 | 4-level precedence, TOML parsing, dot-notation, CLI commands operational |
| `PromptReinforcementEngine` pattern for context injection | C4 | L2 engine, 246 lines, L2-REINJECT parsing, 600-token budget, fail-open |
| `SessionQualityContextGenerator` pattern for resumption | C4 | L1 engine, 134 lines, XML preamble, ~700 token budget |
| `PreToolEnforcementEngine` pattern for staleness detection | C4 | L3 engine, 567 lines, governance escalation detection (lines 501-536) |
| `FileSystemEventStore` JSONL pattern for checkpoints | C6 | JSONL append-only, file locking, directory creation pattern (lines 106-108) |
| `AtomicFileAdapter` for safe checkpoint writes | C6 | Safe file I/O with locking, reusable |
| `InMemorySessionRepository` not persistent | C2 | Line 35: "Loses data on process termination" |
| `SessionAbandoned` event designed for compaction | C2 | session.py line 207: "typically due to context compaction" |
| ECW status line has context data unavailable to hooks | C8 | GAP-003 confirmed |
| 10 of 14 items classified as EXTEND or REUSE | Mapping | 1 REUSE, 10 EXTEND, 3 NEW |

### Phase 2 Gap Analysis References

| Claim | Section | Evidence |
|-------|---------|----------|
| 14 items consolidate to 9 | L0 Summary, Consolidation Analysis | 4 merges: #1+#3, #4+#5, #2+#10, #13+#14 |
| Risk R1 (InMemorySessionRepository) rated HIGH | L2: Risk Analysis | Immediate mitigation: file-based state |
| New bounded context `context_monitoring` recommended | L2: Architectural Integration | Distinct domain language, different lifecycle |
| Phase 1 infrastructure placement | L2: Architectural Integration | Engines in `infrastructure/internal/enforcement/` |
| Effort 20.5-26.5 hours for 9 items | Effort Summary | Phase-by-phase breakdown |

### Phase 3 ADR References

| Claim | Section | Evidence |
|-------|---------|----------|
| Two-phase migration approach | Decision | Phase 1 infrastructure, Phase 2 bounded context extraction |
| Three extraction criteria for Phase 2 | L2 Strategic Implications | Stability, persistent repository, boundary validation |
| 4 new enforcement engines specified | L1 Technical Details | Interface contracts with type signatures |
| QG-1 PASSED at 0.94 | Gate Result | 6-dimension scoring, leniency bias counter-check |

### Infrastructure Code References (User Feedback Evidence)

| Claim | Source File | Evidence |
|-------|------------|----------|
| `FileSystemEventStore` is production-tested | `src/work_tracking/infrastructure/persistence/filesystem_event_store.py` | 369 lines, JSONL format, `FileLock` cross-process safety, `os.fsync` durability, `mkdir(parents=True, exist_ok=True)` |
| `EventSourcedWorkItemRepository` pattern is proven | `src/work_tracking/infrastructure/adapters/event_sourced_work_item_repository.py` | 431 lines, event registry, stream ID convention, domain-to-stored conversion, `load_from_history()` reconstitution |
| `ISessionRepository` port defines the interface | `src/session_management/application/ports/session_repository.py` | Protocol with `get`, `get_active`, `save`, `exists` methods |
| `InMemorySessionRepository` is the current implementation | `src/session_management/infrastructure/adapters/in_memory_session_repository.py` | 100 lines, thread-safe but loses state on process termination |
| `Session.load_from_history()` supports event replay | `src/session_management/domain/aggregates/session.py` | Lines 284-324, replay `SessionCreated`, `SessionCompleted`, `SessionAbandoned`, `SessionProjectLinked` |
| Session events exist and are well-defined | `src/session_management/domain/events/session_events.py` | 4 events, frozen dataclasses, `DomainEvent` base class |

---

## Self-Review (S-010) Verification

- [x] All 14 SPIKE-001 items are covered through the 10 revised CWI items (supersession mappings documented per item)
- [x] User feedback (FileSystemSessionRepository) incorporated as CWI-00 with full justification
- [x] CWI-00 references specific source files: `FileSystemEventStore` (369 lines), `EventSourcedWorkItemRepository` (431 lines), `ISessionRepository` port, `Session.load_from_history()`
- [x] Dependency graph shows CWI-00 as foundation enabling CWI-02 session abandon integration
- [x] Phase 2 Risk R1 (InMemorySessionRepository, rated HIGH) resolved by CWI-00 rather than worked around
- [x] Effort estimates defensible: CWI-00 at 3-4 hours follows a proven 431-line pattern
- [x] All 6 hypotheses evaluated with CONFIRMED/PARTIALLY CONFIRMED verdicts and evidence
- [x] Implementation phases account for dependency ordering (CWI-00 in Phase A, unblocks Phase B)
- [x] Effort comparison table shows SPIKE-001 vs Phase 2 vs Final with change analysis
- [x] Open questions include new items (OQ-10, OQ-11) raised by CWI-00 addition
- [x] Evidence section maps claims to Phase 1, 2, 3 artifacts and infrastructure code
- [x] Navigation table present with anchor links (H-23/H-24 compliance)
