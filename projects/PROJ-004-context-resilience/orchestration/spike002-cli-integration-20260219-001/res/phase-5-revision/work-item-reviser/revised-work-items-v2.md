# SPIKE-002 Synthesis: Revised Work Items v2 — Bounded Context + CLI-First Architecture

<!-- PS-ID: SPIKE-002 | ENTRY-ID: phase-5c | DATE: 2026-02-19 -->
<!-- AGENT: ps-synthesizer v2.3.0 | MODEL: claude-sonnet-4-6 -->
<!-- SUPERSEDES: revised-work-items.md (phase-4-synthesis) -->

> Revised authoritative work item list for FEAT-001 implementation. Supersedes v1 (phase-4-synthesis). Redesigned to align with ADR-SPIKE002-002 (QG-2 PASS at 0.92): proper bounded context at `src/context_monitoring/` with domain/application/infrastructure layers, and `jerry hooks <event>` CLI commands as the single execution path for all hook logic.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Summary](#l0-summary) | Executive overview (5 bullets) |
| [Supersession Statement](#supersession-statement) | What this replaces and why |
| [Revised Work Items](#revised-work-items) | CWI-00 through CWI-11: authoritative item definitions |
| [Dependency Graph](#dependency-graph) | Implementation order visualization |
| [Implementation Phases](#implementation-phases) | Phase A through D with rationale |
| [Effort Summary](#effort-summary) | Total effort comparison across versions |
| [Evidence](#evidence) | Traceability to ADR-SPIKE002-002, DISC-001, DEC-001, QG-2 |
| [Self-Review](#self-review) | S-010 verification checklist |

---

## L0 Summary

1. **12 work items (CWI-00 through CWI-11) supersede the v1 10-item list.** The v1 items (CWI-00 through CWI-09) were designed for ADR-SPIKE002-001's infrastructure placement approach. This v2 redesigns them for ADR-SPIKE002-002's proper bounded context + CLI-first architecture. CWI-00 is unchanged (architecture-independent). Two new items are added: CWI-10 (`jerry hooks` CLI command namespace registration) and CWI-11 (hook wrapper scripts), addressing DEF-004 from QG-2.

2. **The central architectural shift: code moves from `src/infrastructure/internal/enforcement/` to `src/context_monitoring/` with proper hexagonal layers.** Domain value objects (ThresholdTier, FillEstimate, CheckpointData, ContextState), domain events (ContextThresholdReached, CompactionDetected, CheckpointCreated), application services (ContextFillEstimator, CheckpointService, ResumptionContextGenerator), ports (ITranscriptReader, ICheckpointRepository, IThresholdConfiguration), and infrastructure adapters (JsonlTranscriptReader, FilesystemCheckpointRepository, ConfigThresholdAdapter) all reside in the bounded context. No code is placed in the enforcement folder.

3. **Hook integration shifts from direct imports to CLI-first subprocess calls.** CWI-02, CWI-03, CWI-06, and CWI-07 are substantially redesigned: instead of engines in the enforcement folder called by extended hook scripts, all hook logic flows through `jerry hooks <event>` CLI commands (CWI-10) that dispatch to bounded context application services. Hook scripts (CWI-11) become thin wrappers (~10 lines) that pipe stdin to the CLI command and pipe stdout back.

4. **Two new work items are required by the architecture.** CWI-10 creates the `jerry hooks` CLI namespace with four commands (`prompt-submit`, `session-start`, `pre-compact`, `pre-tool-use`), including CLI parser registration, dispatcher routing, and composition root wiring. CWI-11 creates the four thin hook wrapper scripts (`hooks/user-prompt-submit.py`, `hooks/session-start.py`, `hooks/pre-compact.py`, `hooks/pre-tool-use.py`) and updates `hooks/hooks.json` registration.

5. **Residual QG-2 deficiencies DEF-004 and DEF-005 are addressed by this redesign.** DEF-004 (CLI command registration underspecified) is resolved by CWI-10, which explicitly specifies CLI adapter routing, parser registration, and the stdin payload delivery mechanism for `HooksPromptSubmitHandler`. DEF-005 (acknowledgment timing undocumented) is resolved by an explicit design decision in CWI-02 acceptance criteria.

---

## Supersession Statement

**This document supersedes:**

1. **SPIKE-002 Phase 4 Synthesis work items v1 (`phase-4-synthesis/work-item-synthesizer/revised-work-items.md`).** The v1 items (CWI-00 through CWI-09) were designed for ADR-SPIKE002-001's Alternative 2 (infrastructure placement in `src/infrastructure/internal/enforcement/`). DISC-001 identified four violations invalidating that approach (F1: two execution paths, F2: enforcement folder is tech debt, F3: invalid rejection reasoning, F4: scripts/hooks split). DEC-001 captured four corrective decisions (D-001 through D-004). ADR-SPIKE002-002 chose Alternative 3 (proper bounded context + CLI-first hooks) and passed QG-2 at 0.92.

**Impact of architectural change on each v1 item:**

| CWI | v1 Disposition | v2 Action | Reason |
|-----|----------------|-----------|--------|
| CWI-00 | FileSystemSessionRepository | Unchanged | Architecture-independent; foundation enabler |
| CWI-01 | Threshold config via LayeredConfigAdapter | Updated (minor) | Reference `ConfigThresholdAdapter` + `IThresholdConfiguration` port; same 6 defaults |
| CWI-02 | PreCompact hook + CheckpointWriter engine in enforcement/ | Major redesign | `CheckpointService` in `application/services/`; `FilesystemCheckpointRepository` in `infrastructure/adapters/`; hook becomes thin wrapper via CWI-11 |
| CWI-03 | UserPromptSubmit extension with ContextMonitorEngine + CompactionAlertEngine in enforcement/ | Major redesign | `ContextFillEstimator` + `CheckpointService` in bounded context; hook delegates to `jerry hooks prompt-submit` via CWI-10 |
| CWI-04 | Resumption schema + update protocol | Updated (minor) | No code placement change; reference `CheckpointData.resumption_state` field |
| CWI-05 | AE-006 graduated sub-rules | Updated (minor) | No code placement change; L2-REINJECT picked up by existing engine |
| CWI-06 | ResumptionContextGenerator in enforcement/; integration into session_start_hook.py | Major redesign | `ResumptionContextGenerator` in `application/services/`; delegates to `jerry hooks session-start` via CWI-10; old 300+ line session_start_hook.py retired |
| CWI-07 | PostToolUse hook for staleness detection | Redesign | Now part of `jerry hooks pre-tool-use` via CWI-10; uses `PreToolUse` hook (not PostToolUse) per ADR-SPIKE002-002 |
| CWI-08 | Validation spikes | Updated (minor) | Reference `JsonlTranscriptReader` adapter instead of inline engine code |
| CWI-09 | Threshold validation + calibration | Updated (minor) | Reference bounded context path for system operational check |
| CWI-10 | (new) | Added | `jerry hooks` CLI namespace registration and routing (DEF-004 resolution) |
| CWI-11 | (new) | Added | Hook wrapper scripts and hooks.json registration |

---

## Revised Work Items

### CWI-00: FileSystemSessionRepository (UNCHANGED)

| Field | Value |
|-------|-------|
| **ID** | CWI-00 |
| **Title** | Implement FileSystemSessionRepository using existing EventSourced + FileSystemEventStore pattern |
| **Type** | Enabler |
| **Priority** | P0 - Foundation |
| **Effort** | 3-4 hours |
| **Supersedes** | N/A (new item from user feedback; addresses Phase 2 Risk R1) |
| **v2 Change** | None. Architecture-independent. Content identical to v1. |

**Description:** Create a `FileSystemSessionRepository` that implements the `ISessionRepository` port by delegating to the existing `FileSystemEventStore`. Follow the exact pattern established by `EventSourcedWorkItemRepository`: event registry for session events (`SessionCreated`, `SessionCompleted`, `SessionAbandoned`, `SessionProjectLinked`), stream ID convention (`session-{id}`), domain-to-stored event conversion, and aggregate reconstitution via `Session.load_from_history()`. Wire it into `bootstrap.py` as a replacement for `InMemorySessionRepository`. This eliminates the "Loses data on process termination" limitation (Phase 1 Audit C2, `in_memory_session_repository.py` line 35) that was the single most significant architectural risk (Phase 2 Risk R1, rated HIGH).

**CLI Integration Points:** `FileSystemEventStore` (`src/work_tracking/infrastructure/persistence/filesystem_event_store.py`, 369 lines -- REUSE as-is). `EventSourcedWorkItemRepository` pattern (`src/work_tracking/infrastructure/adapters/event_sourced_work_item_repository.py`, 431 lines -- pattern to follow). `ISessionRepository` port (`src/session_management/application/ports/session_repository.py`). `Session.load_from_history()` (`src/session_management/domain/aggregates/session.py`, lines 284-324). Session events (`src/session_management/domain/events/session_events.py` -- 4 events: SessionCreated, SessionCompleted, SessionAbandoned, SessionProjectLinked). `bootstrap.py` composition root wiring.

**Acceptance Criteria:**
1. `FileSystemSessionRepository` implements `ISessionRepository` protocol.
2. Session events persisted to `.jerry/data/events/session-{id}.jsonl`.
3. `jerry session start` creates a session that persists across process termination.
4. `jerry session status` in a new process retrieves the active session.
5. `jerry session abandon --reason "compaction"` from a hook script correctly abandons the persisted session.
6. `Session.load_from_history()` correctly reconstitutes session from event replay.
7. Optimistic concurrency via `FileSystemEventStore` prevents concurrent writes.
8. `get_active()` returns the most recent ACTIVE session across all streams.
9. Unit tests covering: save/get round-trip, get_active, event replay, cross-process persistence, concurrency.
10. `InMemorySessionRepository` retained for unit testing but no longer used in production wiring.

**Dependencies:** Depends on: Nothing (uses existing `FileSystemEventStore` as-is). Depended on by: CWI-02 (CheckpointService can trigger `jerry session abandon`), CWI-10 (session-start and pre-compact CLI commands use session domain events).

---

### CWI-01: Threshold Configuration via ConfigThresholdAdapter (UPDATED -- MINOR)

| Field | Value |
|-------|-------|
| **ID** | CWI-01 |
| **Title** | Add context monitoring threshold defaults and wire ConfigThresholdAdapter |
| **Type** | Enabler |
| **Priority** | P1 - Critical |
| **Effort** | 1 hour |
| **Supersedes** | SPIKE-001 Item #7; v1 CWI-01 |
| **v2 Change** | Minor. Adds creation of `ConfigThresholdAdapter` in `src/context_monitoring/infrastructure/adapters/config_threshold_adapter.py` and the `IThresholdConfiguration` port in `src/context_monitoring/application/ports/threshold_configuration.py`. Effort increases from 0.5h to 1h to account for bounded context setup. |

**Description:** Add default threshold values to the existing `LayeredConfigAdapter` configuration system. Six keys: `context_monitor.nominal_threshold` (0.55), `context_monitor.warning_threshold` (0.70), `context_monitor.critical_threshold` (0.80), `context_monitor.emergency_threshold` (0.88), `context_monitor.compaction_detection_threshold` (10000), `context_monitor.enabled` (true). Create the `IThresholdConfiguration` port (Protocol) in the bounded context application layer. Create `ConfigThresholdAdapter` in the bounded context infrastructure layer as a bridge to `LayeredConfigAdapter`, reading `context_monitor.*` configuration keys. Wire `ConfigThresholdAdapter` into `bootstrap.py` as the implementation of `IThresholdConfiguration`. Users can override thresholds at any level via `jerry config set`.

**Bounded Context Components:**
- `src/context_monitoring/application/ports/threshold_configuration.py` -- `IThresholdConfiguration` Protocol with `get_threshold(tier: str) -> float` and `is_enabled() -> bool`
- `src/context_monitoring/infrastructure/adapters/config_threshold_adapter.py` -- `ConfigThresholdAdapter` implementing `IThresholdConfiguration`, bridging to `LayeredConfigAdapter`

**CLI Integration Points:** `src/interface/cli/adapter.py` `_create_config_adapter()` defaults dictionary (lines 1028-1034). `LayeredConfigAdapter` (`src/infrastructure/adapters/configuration/layered_config_adapter.py`). `bootstrap.py` composition root (wire `ConfigThresholdAdapter` -> `IThresholdConfiguration`).

**Acceptance Criteria:**
1. `jerry config get context_monitor.warning_threshold` returns `0.70`.
2. `jerry config set context_monitor.warning_threshold 0.75 --scope project` persists override.
3. `JERRY_CONTEXT_MONITOR_WARNING_THRESHOLD=0.75` overrides project config.
4. All 6 threshold keys have defaults.
5. `IThresholdConfiguration` Protocol defined with type hints and docstrings (H-11/H-12).
6. `ConfigThresholdAdapter` implements `IThresholdConfiguration` and delegates to `LayeredConfigAdapter`.
7. `bootstrap.py` wires `ConfigThresholdAdapter` as `IThresholdConfiguration` implementation.
8. Unit tests: default retrieval, override precedence, `is_enabled()` flag.

**Dependencies:** Depends on: Nothing. Depended on by: CWI-02 (CheckpointService reads `is_enabled()`), CWI-03 / CWI-10 (ContextFillEstimator reads threshold config via port).

---

### CWI-02: Bounded Context Foundation + CheckpointService (MAJOR REDESIGN)

| Field | Value |
|-------|-------|
| **ID** | CWI-02 |
| **Title** | Create `src/context_monitoring/` bounded context with domain layer and CheckpointService |
| **Type** | Enabler |
| **Priority** | P1 - Critical |
| **Effort** | 4-6 hours |
| **Supersedes** | SPIKE-001 Items #2 + #10; v1 CWI-02 |
| **v2 Change** | Major redesign. v1 created a `CheckpointWriter` engine in `src/infrastructure/internal/enforcement/`. v2 creates the full `src/context_monitoring/` bounded context directory structure, domain layer (value objects + events), and `CheckpointService` application service with `ICheckpointRepository` port and `FilesystemCheckpointRepository` adapter. Hook registration and wrapper scripts are separated into CWI-10 and CWI-11. |

**Description:** Create the `src/context_monitoring/` bounded context as a proper hexagonal architecture following the `session_management` and `work_tracking` patterns. This item establishes the foundation: directory structure, domain value objects, domain events, CheckpointService, and checkpoint persistence infrastructure.

**Domain Layer -- Value Objects** (`src/context_monitoring/domain/value_objects/`):

| File | Class | Description |
|------|-------|-------------|
| `threshold_tier.py` | `ThresholdTier` | Enum: NOMINAL, LOW, WARNING, CRITICAL, EMERGENCY |
| `fill_estimate.py` | `FillEstimate` | Frozen dataclass: fill_percentage, input_tokens, context_window_size, threshold_tier |
| `checkpoint_data.py` | `CheckpointData` | Frozen dataclass: checkpoint_id, timestamp, compaction_sequence, context_state (FillEstimate), resumption_state (dict or None), session_info (dict) |
| `context_state.py` | `ContextState` | Frozen dataclass: fill_estimate (FillEstimate), active_checkpoint (CheckpointData or None), compaction_count (int) |

**Domain Layer -- Events** (`src/context_monitoring/domain/events/`):

| File | Class | Description |
|------|-------|-------------|
| `context_threshold_reached.py` | `ContextThresholdReached` | session_id, fill_estimate, previous_tier, new_tier, timestamp |
| `compaction_detected.py` | `CompactionDetected` | session_id, checkpoint_id, fill_percentage, compaction_sequence, timestamp |
| `checkpoint_created.py` | `CheckpointCreated` | checkpoint_id, checkpoint_path, timestamp |

**Application Layer** (`src/context_monitoring/application/`):

- Port: `ICheckpointRepository` in `ports/checkpoint_repository.py` -- Protocol with `save(data: CheckpointData) -> Path`, `get_latest_unacknowledged() -> CheckpointData | None`, `acknowledge(checkpoint_id: str) -> None`, `list_all() -> list[CheckpointData]`
- Service: `CheckpointService` in `services/checkpoint_service.py` -- orchestrates checkpoint lifecycle. On pre-compact: determines next checkpoint ID via `ICheckpointRepository.list_all()`, reads ORCHESTRATION.yaml resumption section, reads context state via `ContextFillEstimator`, assembles `CheckpointData`, calls `ICheckpointRepository.save()`. On session-start: calls `ICheckpointRepository.get_latest_unacknowledged()`. Acknowledgment design decision: `acknowledge()` is called during session-start, NOT during prompt-submit, ensuring the alert is delivered at session context before being marked acknowledged (resolves DEF-005).

**Infrastructure Layer** (`src/context_monitoring/infrastructure/adapters/`):

- `FilesystemCheckpointRepository` in `filesystem_checkpoint_repository.py` -- implements `ICheckpointRepository`. Reads/writes `.jerry/checkpoints/cx-{NNN}-checkpoint.json` using `AtomicFileAdapter`. Acknowledgment via `.jerry/checkpoints/cx-{NNN}-checkpoint.json.acknowledged` marker files. Sequential ID generation via `list_all()`. Creates `.jerry/checkpoints/` directory via `mkdir(parents=True, exist_ok=True)` pattern from `FileSystemEventStore`.

**Composition Root:** Wire `FilesystemCheckpointRepository` -> `ICheckpointRepository` in `bootstrap.py`. Wire `CheckpointService` receiving `ICheckpointRepository` via constructor injection.

**Acknowledgment Timing Design Decision (DEF-005 resolution):** Unacknowledged checkpoints are acknowledged by `CheckpointService` during `jerry hooks session-start` processing (step 6 in data flow), AFTER the `<resumption-context>` XML is assembled and returned to the caller. This guarantees delivery: the checkpoint data is read, formatted, and included in `additionalContext` before `acknowledge()` is called. If `jerry hooks session-start` times out, the checkpoint remains unacknowledged and will be re-delivered at the next session start. This is an intentional at-least-once delivery pattern. The trade-off (possible double-delivery on repeated session starts without compaction) is acceptable because `ResumptionContextGenerator` output is idempotent.

**Acceptance Criteria:**
1. `src/context_monitoring/` directory structure created with `__init__.py` files at each level.
2. All 4 value objects defined as frozen dataclasses with type hints and docstrings (H-10, H-11, H-12). One class per file (H-10).
3. All 3 domain events defined as frozen dataclasses with type hints and docstrings. One class per file (H-10).
4. `ICheckpointRepository` Protocol defined with 4 methods, type hints, and docstrings (H-11/H-12).
5. `FilesystemCheckpointRepository` implements `ICheckpointRepository`. Checkpoint files written atomically via `AtomicFileAdapter`. Directory auto-created if missing.
6. Sequential checkpoint IDs (cx-001, cx-002, ...) generated correctly.
7. Acknowledgment creates `.acknowledged` marker file. `get_latest_unacknowledged()` excludes acknowledged checkpoints.
8. `CheckpointService` orchestrates checkpoint creation: reads ORCHESTRATION.yaml (fail-open if absent), assembles `CheckpointData`, calls repository.
9. Acknowledgment timing: `acknowledge()` called AFTER checkpoint data included in response, not before (DEF-005).
10. `bootstrap.py` wires `FilesystemCheckpointRepository` -> `ICheckpointRepository` and `CheckpointService` receiving port.
11. `project-workflow.md` updated to include `.jerry/checkpoints/` in workspace layout.
12. Unit tests: value object immutability, event construction, checkpoint CRUD, sequential IDs, directory creation, acknowledged filtering, fail-open for missing ORCHESTRATION.yaml.
13. `H-07` compliance: domain layer imports only `src/context_monitoring/domain/` -- no external imports.
14. `H-08` compliance: application layer imports only domain and port interfaces -- no infrastructure imports.

**Dependencies:** Depends on: CWI-00 (FileSystemSessionRepository for session domain events), CWI-01 (ConfigThresholdAdapter for threshold reading), CWI-04 (resumption schema for `CheckpointData.resumption_state` fields). Depended on by: CWI-03 / CWI-10 (ContextFillEstimator + CompactionAlert use CheckpointService), CWI-06 / CWI-10 (session-start uses CheckpointService + ResumptionContextGenerator).

---

### CWI-03: ContextFillEstimator + ResumptionContextGenerator (MAJOR REDESIGN)

| Field | Value |
|-------|-------|
| **ID** | CWI-03 |
| **Title** | Create ContextFillEstimator, ResumptionContextGenerator, JsonlTranscriptReader in bounded context |
| **Type** | Enabler |
| **Priority** | P1 - Critical |
| **Effort** | 3-5 hours |
| **Supersedes** | SPIKE-001 Items #1 + #3 + #11; v1 CWI-03 + v1 CWI-06 (merged) |
| **v2 Change** | Major redesign. v1 CWI-03 created `ContextMonitorEngine` + `CompactionAlertEngine` in the enforcement folder, extending `hooks/user-prompt-submit.py` directly. v1 CWI-06 created `ResumptionContextGenerator` in the enforcement folder, extending `scripts/session_start_hook.py`. v2 places both application services in `src/context_monitoring/application/services/` with proper ports and adapters. Hook integration is handled by CWI-10 and CWI-11. v1 CWI-06 is merged into this item since both services share the `ITranscriptReader` port and `JsonlTranscriptReader` adapter. |

**Description:** Complete the remaining application services and infrastructure adapters for the `context_monitoring` bounded context. This item builds on CWI-02's domain and checkpoint foundation.

**Application Layer -- Services** (continuing in `src/context_monitoring/application/services/`):

| File | Class | Description |
|------|-------|-------------|
| `context_fill_estimator.py` | `ContextFillEstimator` | Orchestrates context fill estimation. Reads transcript via `ITranscriptReader` port. Reads thresholds via `IThresholdConfiguration` port. Computes `FillEstimate` and determines `ThresholdTier`. Generates `<context-monitor>` XML tag (40-200 tokens based on tier). |
| `resumption_context_generator.py` | `ResumptionContextGenerator` | Generates `<resumption-context>` XML for session-start injection. Receives `CheckpointData` from `CheckpointService`. Reads ORCHESTRATION.yaml resumption fields. Composes structured XML within ~760 token budget. Follows the same generator pattern as existing `SessionQualityContextGenerator` (134 lines). |

**Application Layer -- Port** (new port for transcript reading):

- `ITranscriptReader` in `src/context_monitoring/application/ports/transcript_reader.py` -- Protocol with `read_latest_tokens(transcript_path: str) -> int`

**Infrastructure Layer -- Adapter**:

- `JsonlTranscriptReader` in `src/context_monitoring/infrastructure/adapters/jsonl_transcript_reader.py` -- implements `ITranscriptReader`. Reads `$TRANSCRIPT_PATH` JSONL file. Extracts `input_tokens` from the latest entry using seek-to-end for O(1) reads. Raises `FileNotFoundError` if path does not exist; raises `ValueError` if file is empty or unparseable.

**`ResumptionContextGenerator.generate()` output fields** (from ADR-SPIKE002-002 data flow step 6d):
- Recovery state summary (checkpoint_id, compaction_sequence, fill_percentage)
- Quality trajectory (QG score, iteration count) from `resumption_state`
- Key decisions from decision log in `resumption_state`
- Agent summary states from `resumption_state`
- File read instructions (priority-ordered) from `resumption_state`
- Previous session abandon reason from `session_info`
- Compaction event history

**Composition Root additions:** Wire `JsonlTranscriptReader` -> `ITranscriptReader`. Wire `ContextFillEstimator` receiving `ITranscriptReader` and `IThresholdConfiguration` via constructor injection. Wire `ResumptionContextGenerator` receiving `CheckpointService` via constructor injection.

**Acceptance Criteria:**
1. `ContextFillEstimator.estimate(transcript_path: str) -> FillEstimate` defined with type hints and docstring (H-11/H-12).
2. Fill estimation reads `input_tokens` from JSONL transcript via `ITranscriptReader` port (no direct filesystem access in service).
3. Threshold tier determined correctly: NOMINAL (<0.55), LOW (0.55-0.70), WARNING (0.70-0.80), CRITICAL (0.80-0.88), EMERGENCY (>0.88).
4. `<context-monitor>` XML tag generated with fill %, tier, and recommended action appropriate to tier.
5. Fail-open: if `ITranscriptReader` raises, `ContextFillEstimator` returns NOMINAL tier estimate (not exception).
6. `ResumptionContextGenerator.generate(checkpoint: CheckpointData) -> str` defined with type hints and docstring (H-11/H-12).
7. Returns empty string if `checkpoint.resumption_state` is None (no ORCHESTRATION.yaml at checkpoint time).
8. Returns `<resumption-context>` XML within ~760 token budget when resumption data is present.
9. `ITranscriptReader` Protocol defined with type hints and docstring (H-11/H-12).
10. `JsonlTranscriptReader` implements `ITranscriptReader`. Reads from tail of JSONL efficiently. Correct exceptions on missing file / empty file.
11. `bootstrap.py` wires `JsonlTranscriptReader` -> `ITranscriptReader`, `ContextFillEstimator` with its two ports, `ResumptionContextGenerator` with `CheckpointService`.
12. Unit tests for `ContextFillEstimator`: all 5 tier boundaries, fill calculation, tag generation, fail-open behavior, port stubbing via `ITranscriptReader` in-memory implementation.
13. Unit tests for `ResumptionContextGenerator`: with resumption data, without resumption data (None), token budget adherence.
14. Unit tests for `JsonlTranscriptReader`: valid JSONL, empty file, missing file, seek-to-end behavior.
15. H-07 compliance: no external imports in domain layer. H-08 compliance: no infrastructure imports in application services.

**Dependencies:** Depends on: CWI-02 (domain value objects, CheckpointService, ICheckpointRepository), CWI-01 (IThresholdConfiguration port). Depended on by: CWI-10 (CLI commands use these services), CWI-05 (AE-006 sub-rules reference context-monitor signals), CWI-08 (OQ-9 validates JsonlTranscriptReader accuracy).

---

### CWI-04: Enhanced Resumption Schema + Update Protocol (UPDATED -- MINOR)

| Field | Value |
|-------|-------|
| **ID** | CWI-04 |
| **Title** | Update ORCHESTRATION.yaml template with v2.0 resumption schema and orchestrator update protocol |
| **Type** | Story |
| **Priority** | P1 - Critical |
| **Effort** | 2-3 hours |
| **Supersedes** | SPIKE-001 Items #4 + #5; v1 CWI-04 |
| **v2 Change** | Minor. Content unchanged. Updated references: the schema fields now map to `CheckpointData.resumption_state` (the dict captured from ORCHESTRATION.yaml at compaction time) and `CheckpointData.session_info`. The `updated_at` field is used by `CheckpointService` when assembling `CheckpointData`. |

**Description:** Replace the current 5-field resumption section in `skills/orchestration/templates/ORCHESTRATION.template.yaml` with the v2.0 schema: Recovery State (8 fields), Files to Read (structured with priority/purpose/sections), Quality Trajectory (7 fields), Defect Summary (5 fields), Decision Log (N entries), Agent Summaries (N entries), Compaction Events (2 + N entries). Update the orchestrator agent prompt with an explicit resumption update protocol defining when and what to update. Add an L2-REINJECT marker to `quality-enforcement.md` for resumption update reminders (~25 tokens, rank ~9). The `PromptReinforcementEngine` picks up new L2-REINJECT markers automatically without code changes.

**Bounded Context Relevance:** The ORCHESTRATION.yaml resumption section is the source of `CheckpointData.resumption_state`. `CheckpointService` reads this section at compaction time (CWI-02). `ResumptionContextGenerator` reads it from the checkpoint to generate `<resumption-context>` XML (CWI-03). The `updated_at` field is checked by `jerry hooks pre-tool-use` for staleness detection (CWI-07 / CWI-10).

**Acceptance Criteria:**
1. ORCHESTRATION.yaml template contains v2.0 resumption schema with all 7 sub-sections.
2. Backward compatible: existing 5 fields preserved as part of Recovery State.
3. Orchestrator prompt includes explicit update protocol with triggers: phase start, phase complete, QG iteration, compaction event, cross-phase decision, agent completion.
4. L2-REINJECT marker present in `quality-enforcement.md` with rank and token budget within 600-token total.
5. Resumption section includes `updated_at` ISO 8601 timestamp field.
6. Quality gate: C3 minimum per AE-002 (touches `.context/rules/`).

**Dependencies:** Depends on: Nothing (schema definition is independent). Depended on by: CWI-02 (`CheckpointData.resumption_state` maps to this schema), CWI-03 (`ResumptionContextGenerator` reads schema fields from checkpoint), CWI-10 (pre-tool-use command checks `updated_at`).

---

### CWI-05: AE-006 Graduated Sub-Rules (UPDATED -- MINOR)

| Field | Value |
|-------|-------|
| **ID** | CWI-05 |
| **Title** | Replace AE-006 with graduated sub-rules (AE-006a through AE-006e) |
| **Type** | Story |
| **Priority** | P2 - High |
| **Effort** | 1 hour |
| **Supersedes** | SPIKE-001 Item #6; v1 CWI-05 |
| **v2 Change** | Minor. Content unchanged. Updated reference: AE-006a through AE-006c reference signals from `jerry hooks prompt-submit` (the `<context-monitor>` XML tag generated by `ContextFillEstimator` in the bounded context). The L2-REINJECT marker is unchanged. No code changes required. |

**Description:** Replace the single AE-006 rule in `quality-enforcement.md` with 5 graduated sub-rules mapping detection thresholds to escalation actions by criticality level. Add an L2-REINJECT marker (rank ~8, ~35 tokens) summarizing the graduated escalation protocol. The `PromptReinforcementEngine` automatically picks up the new marker without code changes. Total L2-REINJECT budget remains within 600 tokens (current markers total ~400-450 tokens + new ~60 tokens = ~510 tokens).

**Acceptance Criteria:**
1. AE-006a through AE-006e defined in Auto-Escalation Rules table of `quality-enforcement.md`.
2. Each sub-rule specifies: trigger condition (referencing ThresholdTier values from `context_monitoring` bounded context), escalation action, enforcement mechanism.
3. L2-REINJECT marker present with rank and token count within budget.
4. Total L2-REINJECT budget remains within 600 tokens.
5. Quality gate: C3 minimum per AE-002 (touches `.context/rules/`).

**Dependencies:** Depends on: CWI-03 (ContextFillEstimator and ThresholdTier must exist for AE-006a-c to reference). Depended on by: Nothing directly.

---

### CWI-06: Resumption Prompt Automation -- Merged into CWI-03 (SUPERSEDED)

| Field | Value |
|-------|-------|
| **ID** | CWI-06 |
| **Title** | [MERGED INTO CWI-03] |
| **Type** | N/A |
| **v2 Change** | This item is fully merged into CWI-03. In v1, CWI-06 created `ResumptionContextGenerator` in the enforcement folder and integrated it into `scripts/session_start_hook.py`. In v2, `ResumptionContextGenerator` is created as an application service in `src/context_monitoring/application/services/` (CWI-03), and the session-start integration is handled by `jerry hooks session-start` CLI command (CWI-10) via the new `hooks/session-start.py` thin wrapper (CWI-11). The old `scripts/session_start_hook.py` is retired as part of CWI-11. No standalone CWI-06 item is needed. |

> This slot is intentionally kept as a supersession record. All CWI-06 acceptance criteria from v1 are covered by CWI-03 (ResumptionContextGenerator service) and CWI-10 (session-start CLI command integration). Item numbering continues at CWI-07.

---

### CWI-07: Resumption Staleness Detection in PreToolUse (REDESIGN)

| Field | Value |
|-------|-------|
| **ID** | CWI-07 |
| **Title** | Add ORCHESTRATION.yaml staleness detection to `jerry hooks pre-tool-use` |
| **Type** | Enabler |
| **Priority** | P3 - Medium |
| **Effort** | 1.5-2.5 hours |
| **Supersedes** | SPIKE-001 Item #12; v1 CWI-07 |
| **v2 Change** | Redesign. v1 registered a new `PostToolUse` hook for staleness detection. v2 incorporates staleness detection into the existing `PreToolUse` hook event, handled by `jerry hooks pre-tool-use` CLI command (CWI-10). This aligns with ADR-SPIKE002-002 data flow (section: Data Flow: `jerry hooks pre-tool-use`) where step 5 performs staleness detection alongside existing `PreToolEnforcementEngine` validation. The hook registration is already handled by CWI-11 (no new hook entry needed). Effort reduced from 2-3h to 1.5-2.5h because the PostToolUse hook registration is no longer needed. |

**Description:** Add ORCHESTRATION.yaml resumption staleness detection to the `jerry hooks pre-tool-use` CLI command handler (implemented in CWI-10). When the tool call targets a Write/Edit/MultiEdit operation on ORCHESTRATION.yaml, the handler checks whether `resumption.updated_at` has been updated in the current phase. If stale, a staleness warning is injected into the enforcement decision response. This follows the `PreToolEnforcementEngine` governance escalation pattern (Phase 1 Audit C4, 567 lines, lines 501-536) for the warning injection mechanism.

**Implementation Note:** This item specifies the staleness detection logic. The CLI command plumbing (registering `jerry hooks pre-tool-use`, routing to the handler, wiring `PreToolEnforcementEngine` alongside the new staleness check) is handled by CWI-10. The hook script that calls `jerry hooks pre-tool-use` is handled by CWI-11.

**Staleness Logic:**
1. Parse the tool call's target path from stdin JSON.
2. If path does not match `ORCHESTRATION.yaml`: return empty staleness result (passthrough).
3. If path matches: read `resumption.updated_at` from the ORCHESTRATION.yaml file being targeted.
4. Compare `updated_at` against current phase start timestamp (from active session or ORCHESTRATION.yaml header).
5. If stale (updated_at predates current phase): inject staleness warning into enforcement response.
6. Fail-open: if ORCHESTRATION.yaml is unparseable, return empty staleness result.

**Acceptance Criteria:**
1. Staleness detection logic implemented as a function or class in `src/context_monitoring/` (appropriate layer TBD by implementer -- likely application service or infrastructure utility).
2. Correct passthrough for non-ORCHESTRATION.yaml tool calls.
3. Correct staleness detection when `updated_at` predates current phase.
4. Staleness warning formatted consistently with `PreToolEnforcementEngine` warning output format.
5. Fail-open on parse errors.
6. Unit tests: path matching, staleness calculation, passthrough, fail-open.
7. Integration with `jerry hooks pre-tool-use` command handler (CWI-10) verified by integration test.

**Dependencies:** Depends on: CWI-04 (update protocol defines when `updated_at` should change), CWI-10 (pre-tool-use CLI command exists). Depended on by: Nothing directly.

---

### CWI-08: Validation Spikes -- OQ-9 + Method C (UPDATED -- MINOR)

| Field | Value |
|-------|-------|
| **ID** | CWI-08 |
| **Title** | Validate input_tokens accuracy (OQ-9) and investigate Method C feasibility (OQ-1) |
| **Type** | Spike |
| **Priority** | P2 - High |
| **Effort** | 3 hours (timebox) |
| **Supersedes** | SPIKE-001 Items #8 + #9; v1 CWI-08 |
| **v2 Change** | Minor. References updated: instead of validating `ContextMonitorEngine` JSONL parsing (enforcement engine), this validates `JsonlTranscriptReader` (`src/context_monitoring/infrastructure/adapters/jsonl_transcript_reader.py`) accuracy. The investigation approach is unchanged. |

**Description:** Two focused investigations: (1) OQ-9 validation -- compare `input_tokens` from transcript JSONL (read by `JsonlTranscriptReader`) against ECW status line data (`~/.claude/ecw-statusline-state.json`) and optionally against `TokenCounter` calculations (Phase 1 Audit C1, tiktoken `p50k_base`). (2) Method C feasibility -- extend status line state file to include `context_fill_percentage`, implement a test hook that reads the state file, verify timing (does state file update before `UserPromptSubmit` fires?). Both produce a finding report with data and recommendation.

**Acceptance Criteria:**
1. OQ-9: Report documenting `JsonlTranscriptReader` accuracy with measured divergence from reference sources.
2. Method C: Report documenting timing test results.
3. Method C: If feasible, prototype status line extension committed.
4. Both reports include recommendation: proceed/defer/abandon.
5. Total timebox: 3 hours.

**Dependencies:** Depends on: CWI-03 (JsonlTranscriptReader must exist to validate). Depended on by: May upgrade `JsonlTranscriptReader` to use Method C data if OQ-1 is resolved.

---

### CWI-09: Threshold Validation + Calibration Documentation (UPDATED -- MINOR)

| Field | Value |
|-------|-------|
| **ID** | CWI-09 |
| **Title** | Validate thresholds against second workflow type and document calibration protocol |
| **Type** | Story |
| **Priority** | P3 - Medium |
| **Effort** | 4 hours (timebox) |
| **Supersedes** | SPIKE-001 Items #13 + #14; v1 CWI-09 |
| **v2 Change** | Minor. System operational check references `jerry hooks prompt-submit` (via `ContextFillEstimator` in the bounded context) rather than `ContextMonitorEngine` in the enforcement folder. Calibration data paths unchanged. |

**Description:** Run a monitored session with the detection system active (`jerry hooks prompt-submit` operational, via CWI-10 + CWI-11) against a workflow with a different profile than the PROJ-001 FEAT-015 baseline (e.g., deep research spike or multi-file refactoring). Collect per-operation token costs and fill trajectory. Compare against PROJ-001 calibration data. Document the calibration protocol: workflow selection criteria, measurement methodology, data collection format, recalibration triggers. Persist to `docs/knowledge/context-resilience/calibration-protocol.md`.

**Acceptance Criteria:**
1. Monitored session completed against a non-PROJ-001 workflow.
2. Per-operation token cost data collected.
3. Fill trajectory compared against PROJ-001 baseline.
4. Threshold adjustment recommendations documented.
5. Calibration protocol document created at `docs/knowledge/context-resilience/calibration-protocol.md`.
6. Document includes: when to recalibrate, how to collect data, how to interpret results.

**Dependencies:** Depends on: CWI-01, CWI-02, CWI-03, CWI-10, CWI-11 (system must be operational). Depended on by: Nothing directly.

---

### CWI-10: `jerry hooks` CLI Command Namespace Registration (NEW -- DEF-004 Resolution)

| Field | Value |
|-------|-------|
| **ID** | CWI-10 |
| **Title** | Register `jerry hooks` CLI command namespace with four event commands |
| **Type** | Enabler |
| **Priority** | P1 - Critical |
| **Effort** | 3-5 hours |
| **Supersedes** | N/A (new item; resolves QG-2 DEF-004 -- CLI command registration underspecified) |
| **v2 Change** | New item required by ADR-SPIKE002-002 Decision D-003 and to resolve DEF-004 from QG-2. |

**Description:** Register the `jerry hooks` subcommand group in the CLI adapter and parser. Create four command handlers that consolidate all hook event logic, dispatching to bounded context application services. This is the central integration item that makes hook scripts work.

**CLI Commands to Register:**

| Command | Handler Class | Responsibilities |
|---------|--------------|-----------------|
| `jerry hooks prompt-submit` | `HooksPromptSubmitHandler` | Context fill monitoring (`ContextFillEstimator`), compaction alert check (`CheckpointService.get_latest_unacknowledged()`), quality reinforcement (existing `PromptReinforcementEngine`). Returns `{hookSpecificOutput: {additionalContext: combined}}` JSON. |
| `jerry hooks session-start` | `HooksSessionStartHandler` | Project context query (existing `RetrieveProjectContextQuery`), quality context (existing `SessionQualityContextGenerator`), resumption context (`CheckpointService` + `ResumptionContextGenerator`). Returns `{hookSpecificOutput: {additionalContext: combined}}` JSON. |
| `jerry hooks pre-compact` | `HooksPreCompactHandler` | Checkpoint creation (`CheckpointService`), session abandon (`AbandonSessionCommand` with reason="context compaction at {fill}%"). Returns `{systemMessage: "Checkpoint cx-{NNN} saved..."}` JSON. |
| `jerry hooks pre-tool-use` | `HooksPreToolUseHandler` | Architecture validation (existing `PreToolEnforcementEngine`), resumption staleness detection (CWI-07 logic). Returns enforcement decision JSON. |

**CLI Registration Details (DEF-004 resolution):**

The `jerry hooks` command group follows the same registration pattern as `jerry session` and `jerry items`. Specifically:

1. **Parser registration:** Add `hooks` as a subparser group in `src/interface/cli/parser.py`. Each of the four commands (`prompt-submit`, `session-start`, `pre-compact`, `pre-tool-use`) is registered as a subcommand of `hooks`. Each command accepts `--stdin-data` (or reads from stdin via `sys.stdin.buffer.read()`) for the hook payload JSON.

2. **Adapter routing:** In `src/interface/cli/adapter.py`, add routing for `hooks` commands to their respective handlers. The handler classes are constructed with injected services from `bootstrap.py`.

3. **Stdin payload delivery:** Each hook command reads the Claude Code hook payload from stdin as a JSON blob. The handler parses it to extract relevant fields (e.g., `env.TRANSCRIPT_PATH` for `prompt-submit`, `tool_use.input` for `pre-tool-use`). Stdin is read once at command start and passed to handlers via constructor or parameter.

4. **Handler construction in `bootstrap.py`:** Each handler receives its services via constructor injection:
   - `HooksPromptSubmitHandler` receives: `ContextFillEstimator`, `CheckpointService`, `PromptReinforcementEngine`
   - `HooksSessionStartHandler` receives: query dispatcher (existing), `SessionQualityContextGenerator` (existing), `CheckpointService`, `ResumptionContextGenerator`
   - `HooksPreCompactHandler` receives: `CheckpointService`, command dispatcher (for `AbandonSessionCommand`)
   - `HooksPreToolUseHandler` receives: `PreToolEnforcementEngine` (existing), staleness detection logic (CWI-07)

5. **Output format:** All handlers return JSON to stdout matching Claude Code's hook response schema. `--json` flag behavior follows existing CLI adapter pattern.

**Error handling:** Each handler step is wrapped in try/except. Step failures log to stderr and continue to the next step (fail-open). If all steps fail, an empty `additionalContext` is returned. Handler exits 0 always.

**Acceptance Criteria:**
1. `jerry hooks prompt-submit` callable from terminal. Accepts JSON on stdin, returns JSON on stdout.
2. `jerry hooks session-start` callable from terminal.
3. `jerry hooks pre-compact` callable from terminal.
4. `jerry hooks pre-tool-use` callable from terminal.
5. All four commands registered in CLI parser with correct subcommand group.
6. All four handlers constructed via dependency injection in `bootstrap.py`. No ad-hoc instantiation.
7. Stdin payload read and parsed correctly by each handler.
8. `jerry --json hooks prompt-submit` returns valid JSON matching Claude Code `additionalContext` schema.
9. `ContextFillEstimator`, `CheckpointService`, `ResumptionContextGenerator` called correctly within `HooksSessionStartHandler`.
10. `jerry hooks pre-compact` triggers `AbandonSessionCommand` via command dispatcher (CWI-00 required).
11. `jerry hooks pre-tool-use` calls both `PreToolEnforcementEngine` (existing) and staleness check (CWI-07).
12. Fail-open: any handler step failure logs to stderr and continues; handler always exits 0 returning valid JSON.
13. Integration tests: end-to-end `jerry --json hooks prompt-submit` with sample stdin payload; `jerry --json hooks pre-compact` with mock checkpoint data.
14. H-08 compliance: CLI adapter does not import `src/context_monitoring/` infrastructure directly -- only application services via `bootstrap.py`.

**Dependencies:** Depends on: CWI-00 (session abandon command), CWI-02 (CheckpointService, FilesystemCheckpointRepository), CWI-03 (ContextFillEstimator, ResumptionContextGenerator, JsonlTranscriptReader), CWI-07 (staleness detection logic). Depended on by: CWI-11 (wrapper scripts call these commands), CWI-09 (system operational check).

---

### CWI-11: Hook Wrapper Scripts and hooks.json Registration (NEW)

| Field | Value |
|-------|-------|
| **ID** | CWI-11 |
| **Title** | Create thin hook wrapper scripts and update hooks.json registration |
| **Type** | Enabler |
| **Priority** | P1 - Critical |
| **Effort** | 1.5-2 hours |
| **Supersedes** | N/A (new item; previously implicit in CWI-02, CWI-03, CWI-06, CWI-07 in v1) |
| **v2 Change** | New item. In v1, hook integration was embedded within each CWI (extending existing scripts or registering new hooks inline). v2 separates hook script creation and registration as a dedicated item following D-001 (hooks call CLI, not import modules) and ADR-SPIKE002-002 wrapper specification. |

**Description:** Create the four thin hook wrapper scripts and update `hooks/hooks.json` to register all hook events. Each wrapper script is ~10 lines, reads stdin from Claude Code, calls the corresponding `jerry hooks <event>` CLI command via subprocess, and pipes stdout back. All logic lives in the bounded context (CWI-02, CWI-03) and CLI commands (CWI-10). Scripts contain NO imports from `src/`.

**Wrapper Script Pattern** (from ADR-SPIKE002-002 Interface Contracts section):

```python
#!/usr/bin/env python3
"""<HookEvent> hook wrapper. Delegates to jerry hooks <event>."""
import subprocess
import sys

result = subprocess.run(
    ["uv", "run", "--directory", "${CLAUDE_PLUGIN_ROOT}", "jerry", "--json", "hooks", "<event>"],
    input=sys.stdin.buffer.read(),
    capture_output=True,
    timeout=<N>,  # N seconds: 4 for 5s hooks, 9 for 10s hooks
)
sys.stdout.buffer.write(result.stdout)
sys.exit(0)  # Always exit 0 (fail-open)
```

**Files to Create:**

| Script | Hook Event | Subprocess Timeout | hooks.json Timeout |
|--------|-----------|-------------------|-------------------|
| `hooks/user-prompt-submit.py` | UserPromptSubmit | 4s | 5000ms |
| `hooks/session-start.py` | SessionStart | 9s | 10000ms |
| `hooks/pre-compact.py` | PreCompact | 9s | 10000ms |
| `hooks/pre-tool-use.py` | PreToolUse | 4s | 5000ms |

**hooks.json Changes:**
- Update existing `UserPromptSubmit` entry to point to `hooks/user-prompt-submit.py` (verify current path matches -- may already be correct).
- Update existing `SessionStart` entry: change `command` from `scripts/session_start_hook.py` to `hooks/session-start.py`.
- Add new `PreCompact` entry: command = `hooks/pre-compact.py`, timeout = 10000ms.
- Update existing `PreToolUse` entry: change `command` from `scripts/pre_tool_use.py` to `hooks/pre-tool-use.py`.

**Session Start Hook Retirement:**
- `scripts/session_start_hook.py` (300+ lines) is retired -- its logic is now in `jerry hooks session-start` (CWI-10), wired through `bootstrap.py`.
- The old file is removed or archived (add comment `# RETIRED: see hooks/session-start.py + jerry hooks session-start`).
- Similarly, `scripts/pre_tool_use.py` logic moves to `jerry hooks pre-tool-use`.

**Acceptance Criteria:**
1. `hooks/user-prompt-submit.py` created as thin wrapper (<=15 lines). No `src/` imports. Always exits 0.
2. `hooks/session-start.py` created as thin wrapper (<=15 lines). Calls `jerry hooks session-start`. Always exits 0.
3. `hooks/pre-compact.py` created as thin wrapper (<=15 lines). Calls `jerry hooks pre-compact`. Always exits 0.
4. `hooks/pre-tool-use.py` created as thin wrapper (<=15 lines). Calls `jerry hooks pre-tool-use`. Always exits 0.
5. `hooks/hooks.json` updated: SessionStart points to `hooks/session-start.py`; PreCompact entry added; PreToolUse points to `hooks/pre-tool-use.py`.
6. `scripts/session_start_hook.py` retired: file removed or clearly marked as retired with reference to replacement.
7. Subprocess timeout set 1 second below hook timeout budget for each wrapper.
8. All wrappers correctly pipe stdin to CLI subprocess and stdout back to Claude Code.
9. End-to-end test: run each wrapper script manually with sample JSON stdin; verify expected JSON output from CLI (requires CWI-10 to be complete).
10. `hooks.json` validation: all registered hooks have correct paths, timeouts, and matchers.

**Dependencies:** Depends on: CWI-10 (CLI commands must exist before wrappers can call them). Depended on by: CWI-09 (system operational end-to-end).

---

## Dependency Graph

```
CWI-00 (FileSystemSessionRepository) [P0 - Foundation]
  |
  +---> CWI-02 (Bounded Context + CheckpointService) [P1]
  |       |
  |       +---> CWI-03 (ContextFillEstimator + ResumptionContextGenerator) [P1]
  |               |
  |               +---> CWI-10 (jerry hooks CLI commands) [P1]
  |               |       |
  |               |       +---> CWI-11 (Hook Wrappers + hooks.json) [P1]
  |               |               |
  |               |               +---> CWI-05 (AE-006 Sub-Rules) [P2]
  |               |               +---> CWI-08 (Validation Spikes) [P2]
  |               |               +---> CWI-09 (Threshold Validation) [P3]
  |               |
  |               +---> CWI-08 (validates JsonlTranscriptReader)
  |
  +---> CWI-10 (session-start and pre-compact use AbandonSessionCommand)

CWI-01 (Threshold Config + ConfigThresholdAdapter) [P1 - no dependencies]
  |
  +---> CWI-02 (CheckpointService reads is_enabled())
  +---> CWI-03 (ContextFillEstimator reads thresholds via port)

CWI-04 (Resumption Schema + Protocol) [P1 - no dependencies]
  |
  +---> CWI-02 (CheckpointData.resumption_state maps to schema)
  +---> CWI-03 (ResumptionContextGenerator reads schema fields from checkpoint)
  +---> CWI-07 (staleness detection checks updated_at from schema)

CWI-07 (Staleness Detection Logic) [P3]
  depends on: CWI-04 (update protocol), CWI-10 (pre-tool-use command exists)
```

### Critical Path

```
CWI-00 --> CWI-02 --> CWI-03 --> CWI-10 --> CWI-11
              ^
              |
CWI-01 ------+
CWI-04 ------+
```

The critical path runs through CWI-00 (session persistence) to CWI-02 (bounded context foundation + CheckpointService) to CWI-03 (ContextFillEstimator + ResumptionContextGenerator) to CWI-10 (CLI commands) to CWI-11 (hook wrappers). CWI-01 and CWI-04 can run in parallel with CWI-00 as they have no dependencies.

---

## Implementation Phases

### Phase A: Foundation (CWI-00, CWI-01, CWI-04) -- 6-8 hours

| Item | Effort | Rationale |
|------|--------|-----------|
| CWI-00 | 3-4 hrs | FileSystemSessionRepository is the foundation enabler. No dependencies. Unblocks CWI-02 session abandon integration and CWI-10 pre-compact command. |
| CWI-01 | 1 hr | Threshold config defaults + IThresholdConfiguration port + ConfigThresholdAdapter. No dependencies. Unblocks CWI-03. |
| CWI-04 | 2-3 hrs | Resumption schema + update protocol. No dependencies. Template and agent prompt work. Unblocks CWI-02 (schema fields). |

All three items are independent and can be parallelized.

**Phase A Gate:** `jerry session status` works across processes. `jerry config get context_monitor.warning_threshold` returns `0.70`. `IThresholdConfiguration` port and `ConfigThresholdAdapter` exist in bounded context. ORCHESTRATION.yaml template has v2.0 schema.

### Phase B: Bounded Context Build (CWI-02, CWI-03) -- 7-11 hours

| Item | Effort | Rationale |
|------|--------|-----------|
| CWI-02 | 4-6 hrs | Creates the full `src/context_monitoring/` directory structure, domain layer, CheckpointService, ICheckpointRepository, FilesystemCheckpointRepository. Depends on CWI-00, CWI-01, CWI-04. |
| CWI-03 | 3-5 hrs | Creates ContextFillEstimator, ResumptionContextGenerator, ITranscriptReader, JsonlTranscriptReader. Depends on CWI-02 domain layer. |

CWI-02 must complete (domain layer created) before CWI-03 can start (ContextFillEstimator uses FillEstimate, ThresholdTier; ResumptionContextGenerator uses CheckpointData).

**Phase B Gate:** `src/context_monitoring/` bounded context is structurally complete with all domain, application, and infrastructure components. All unit tests passing. `bootstrap.py` wired. No CLI commands yet -- services are testable directly via Python, not yet via `jerry hooks`.

### Phase C: CLI Integration + Hook Wiring (CWI-10, CWI-11, CWI-05, CWI-07) -- 6-9.5 hours

| Item | Effort | Rationale |
|------|--------|-----------|
| CWI-10 | 3-5 hrs | Registers `jerry hooks` namespace, four handlers, stdin routing, composition root wiring. Depends on CWI-02 + CWI-03. |
| CWI-11 | 1.5-2 hrs | Creates thin wrapper scripts, updates hooks.json, retires old session_start_hook.py. Depends on CWI-10. |
| CWI-07 | 1.5-2.5 hrs | Staleness detection logic, integrated into pre-tool-use handler. Can proceed after CWI-04 + CWI-10. |
| CWI-05 | 1 hr | AE-006 sub-rules in quality-enforcement.md. Can proceed after CWI-03. |

CWI-10 then CWI-11 must be sequential (wrappers require commands). CWI-07 and CWI-05 can run in parallel with each other after their respective dependencies.

**Phase C Gate:** The full system is operational end-to-end. `jerry hooks prompt-submit`, `session-start`, `pre-compact`, `pre-tool-use` all callable via CLI with `--json` flag. Hook scripts registered in hooks.json. Context monitoring, checkpointing, and resumption work through the CLI path. AE-006 graduated escalation rules documented.

### Phase D: Validation (CWI-08, CWI-09) -- 7 hours

| Item | Effort | Rationale |
|------|--------|-----------|
| CWI-08 | 3 hrs | Validation spikes (OQ-9 + Method C). Timeboxed. Validates JsonlTranscriptReader accuracy. |
| CWI-09 | 4 hrs | Threshold validation + calibration documentation. Requires operational system. |

Both are timeboxed and can run in parallel once Phase C is complete.

**Phase D Gate:** JsonlTranscriptReader accuracy validated. Method C feasibility determined. Threshold calibration documented for second workflow type.

---

## Effort Summary

| Source | Items | Effort Range (hours) | Notes |
|--------|-------|---------------------|-------|
| SPIKE-001 (original) | 14 | 25-37 | All items classified as NEW, hook-only approach |
| SPIKE-002 Phase 2 (gap analysis) | 9 | 20.5-26.5 | CLI integration, InMemorySessionRepository as hard constraint |
| SPIKE-002 Phase 4 v1 (superseded) | 10 | 19.5-28.5 | CLI integration + FileSystemSessionRepository; enforcement folder placement |
| **SPIKE-002 Phase 5c v2 (this document)** | **12** | **26-35.5** | Bounded context + CLI-first; DEF-004/DEF-005 resolved; two new items |

### Effort Change Analysis: v1 to v2

| Change | Effect |
|--------|--------|
| CWI-01: Added ConfigThresholdAdapter + port creation | +0.5 hrs |
| CWI-02: Bounded context structure setup instead of flat enforcement engine | +1-1.5 hrs (domain + events + port definitions additional) |
| CWI-03: Merged v1 CWI-06 (ResumptionContextGenerator) into CWI-03; bounded context placement | +0-1 hr |
| CWI-06: Retired (merged into CWI-03) | -2-3 hrs removed |
| CWI-07: Redesign to PreToolUse (not PostToolUse) saves hook registration work | -0.5-1 hr |
| CWI-10: New item (jerry hooks CLI namespace) | +3-5 hrs |
| CWI-11: New item (hook wrappers + hooks.json) | +1.5-2 hrs |
| Net | +3.5-7 hrs above v1 |

**Architectural cost rationale:** The 3.5-7 hour premium above v1 is the cost of building correctly from the start rather than placing code in the enforcement tech debt folder. This investment:
- Eliminates the need for a Phase 2 bounded context extraction (estimated 5-10 hours had v1 been implemented)
- Provides port-based testability (no filesystem mocking in unit tests)
- Creates a single CLI execution path (all hook behavior testable via `jerry --json hooks <event>`)
- Satisfies DEC-001 D-001 through D-004 completely

The net lifetime cost (v2 implementation + zero extraction) is approximately equal to or less than (v1 implementation + Phase 2 extraction).

---

## Evidence

### Traceability to ADR-SPIKE002-002

| CWI | ADR-SPIKE002-002 Component | Evidence |
|-----|---------------------------|----------|
| CWI-00 | Composition Root section: "FileSystemSessionRepository eliminates InMemorySessionRepository limitation" | ADR-SPIKE002-002 Context: Forces section, Force 4 |
| CWI-01 | `ConfigThresholdAdapter` in infrastructure/adapters/; `IThresholdConfiguration` in application/ports/ | ADR-SPIKE002-002 Bounded Context tables |
| CWI-02 | Full domain layer (value objects + events), `CheckpointService`, `ICheckpointRepository`, `FilesystemCheckpointRepository` | ADR-SPIKE002-002 Bounded Context: Domain Layer, Application Layer, Infrastructure Layer tables |
| CWI-03 | `ContextFillEstimator`, `ResumptionContextGenerator`, `ITranscriptReader`, `JsonlTranscriptReader` | ADR-SPIKE002-002 Bounded Context tables; Interface Contracts section (lines 707-739) |
| CWI-04 | `CheckpointData.resumption_state` field; ORCHESTRATION.yaml as checkpoint source | ADR-SPIKE002-002 Data Flow: pre-compact step 4b |
| CWI-05 | AE-006 sub-rules reference ThresholdTier from context_monitoring domain | ADR-SPIKE002-002 L2: Impact on 5-Layer Enforcement Architecture |
| CWI-07 | Data Flow: `jerry hooks pre-tool-use`, step 5 (staleness detection) | ADR-SPIKE002-002 Data Flow: pre-tool-use |
| CWI-10 | CLI Commands table: four `jerry hooks <event>` commands; Composition Root Wiring section | ADR-SPIKE002-002 Decision section: CLI Commands |
| CWI-11 | Hook Wrapper Scripts section; `hooks/user-prompt-submit.py` example (lines 159-175) | ADR-SPIKE002-002 Decision section: Hook Wrapper Scripts |

### Traceability to DISC-001

| CWI | DISC-001 Finding Addressed | How |
|-----|---------------------------|-----|
| CWI-02 | F2: Enforcement folder is tech debt (flat, no domain layer) | Bounded context has domain/application/infrastructure layers |
| CWI-03 | F2: No ports/adapters in enforcement folder | ITranscriptReader port + JsonlTranscriptReader adapter |
| CWI-10 | F1: 3 of 4 hooks bypass CLI | All hook logic routes through `jerry hooks <event>` commands |
| CWI-11 | F1: two execution paths; F4: scripts/hooks split | All hooks become thin wrappers in hooks/; scripts/session_start_hook.py retired |
| CWI-07 | F4: scripts/pre_tool_use.py in scripts/ | Logic moves to `jerry hooks pre-tool-use` via hooks/pre-tool-use.py wrapper |

### Traceability to DEC-001

| CWI | DEC-001 Decision | Implementation |
|-----|-----------------|----------------|
| CWI-10, CWI-11 | D-001: Hooks call CLI, not import modules | CWI-11 creates thin wrappers; CWI-10 creates CLI commands they call |
| CWI-02, CWI-03 | D-002: Context monitoring is a proper bounded context | Full `src/context_monitoring/` with domain/application/infrastructure layers |
| CWI-10 | D-003: CLI gets `jerry hooks` command namespace | CWI-10 registers `jerry hooks prompt-submit`, `session-start`, `pre-compact`, `pre-tool-use` |
| All CWIs | D-004: Enforcement tech debt tracked separately | No CWI modifies `src/infrastructure/internal/enforcement/`; existing engines called via bootstrap.py from CWI-10 handlers |

### Traceability to QG-2 Residual Deficiencies

| Deficiency | Resolution |
|------------|------------|
| DEF-004: CLI command registration underspecified | CWI-10 specifies: parser registration, adapter routing, stdin payload delivery mechanism, handler construction via bootstrap.py |
| DEF-005: Acknowledgment timing undocumented | CWI-02 Acceptance Criteria #9 and Description (DEF-005 resolution section): acknowledge() called AFTER checkpoint data included in response; at-least-once delivery pattern documented |
| DEF-008: ContextState no code contract | CWI-02 Acceptance Criteria #2: ContextState frozen dataclass with type hints and docstring required |

---

## Self-Review

- [x] All 14 SPIKE-001 items covered through revised CWIs (supersession mappings documented in Supersession Statement table and per-item v2 Change fields).
- [x] All v1 CWI-00 through CWI-09 items are accounted for: CWI-00 unchanged, CWI-01/04/05/08/09 minor updates, CWI-02/03/07 major redesigns, CWI-06 merged into CWI-03, CWI-10/11 new.
- [x] CWI-06 slot retained as a supersession record per DISC-001 recommendation to track architecture changes.
- [x] Bounded context file paths are explicit and consistent with ADR-SPIKE002-002 component diagram (lines 325-360 of ADR).
- [x] DEF-004 (CLI registration) addressed by CWI-10 with specific parser, adapter routing, and stdin delivery mechanism.
- [x] DEF-005 (acknowledgment timing) addressed by CWI-02 with explicit at-least-once delivery design decision and rationale.
- [x] DEF-008 (ContextState code contract) addressed by CWI-02 Acceptance Criteria #2.
- [x] H-10 compliance: all domain classes specified as one class per file (value objects and events explicitly separate files).
- [x] H-07/H-08 layer isolation: domain no external imports (CWI-02 AC #13); application no infrastructure imports (CWI-02 AC #14); CLI adapter no bounded context infrastructure imports (CWI-10 AC #14).
- [x] H-11/H-12 type hints and docstrings: required in acceptance criteria for all Protocol definitions and application service signatures.
- [x] Dependency graph shows correct ordering: domain layer (CWI-02) before application services (CWI-03) before CLI commands (CWI-10) before hook wrappers (CWI-11).
- [x] Effort premium for v2 over v1 is documented and justified (bounded context setup cost vs. future extraction savings).
- [x] CWI-07 correctly redesigned from PostToolUse (v1) to PreToolUse (v2) per ADR-SPIKE002-002 data flow specification.
- [x] scripts/session_start_hook.py retirement documented in CWI-11 (D-001, F4 resolution).
- [x] Navigation table present with anchor links (H-23/H-24 compliance).
- [x] No deception: effort comparison table honestly shows v2 costs more upfront than v1 (H-03/P-022), with rationale for why this is correct.
- [x] Self-review completed before finalizing (H-15, S-010).
