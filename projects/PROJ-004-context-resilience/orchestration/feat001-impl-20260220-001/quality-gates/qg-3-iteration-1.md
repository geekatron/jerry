# QG-3: Integration Review — Iteration 1

<!-- VERSION: 1.0.0 | DATE: 2026-02-20 | GATE: QG-3 | CRITICALITY: C3 | AGENT: adv-scorer -->

> Quality Gate 3 — Integration Review (after Phase 4+5, before Phase 6)
> Deliverables: EN-006, ST-002, SPIKE-003, EN-007
> Threshold: >= 0.92 weighted composite (C3 Significant)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Gate Metadata](#gate-metadata) | Gate context, threshold, iteration |
| [Strategy Application](#strategy-application) | S-003, S-002, S-007, S-004, S-012, S-013 results |
| [Per-Deliverable Analysis](#per-deliverable-analysis) | EN-006, ST-002, SPIKE-003, EN-007 |
| [Dimensional Scoring](#dimensional-scoring) | S-014 LLM-as-Judge with 6 dimensions |
| [Defect Catalogue](#defect-catalogue) | REQUIRED and RECOMMENDED findings |
| [Verdict](#verdict) | PASS / REVISE / REJECTED with composite score |

---

## Gate Metadata

| Field | Value |
|-------|-------|
| Gate | QG-3 — Integration Review |
| Criticality | C3 (Significant) |
| Date | 2026-02-20 |
| Iteration | 1 of minimum 3 |
| Deliverables | EN-006, ST-002, SPIKE-003, EN-007 |
| Threshold | >= 0.92 weighted composite |
| Agent | adv-scorer |
| Strategies Applied | S-003, S-002, S-007, S-004, S-012, S-013, S-014 |

---

## Strategy Application

### S-003: Steelman Technique

> Strengthen the strongest arguments for each deliverable before critique.

**EN-006 (Hooks CLI Namespace):**
The strongest case for EN-006 is its design coherence. All 4 handlers share a uniform interface contract: `handle(stdin_json: str) -> int`, with identical fail-open semantics, always exiting 0, always emitting valid JSON. This design is precisely correct for Claude Code hook handlers, which must never block Claude's operation regardless of internal failures. The step-numbered try/except blocks with structured stderr logging provide excellent operational observability without sacrificing resilience. The `_add_hooks_namespace()` function cleanly encapsulates parser registration, and bootstrap wiring is explicit and readable. 41 tests provide strong behavioral coverage.

**ST-002 (AE-006 Graduated Sub-Rules):**
The strongest case for ST-002 is its semantic precision. The original monolithic AE-006 ("token exhaustion at C3+") conflated threshold-based tiers with the compaction event itself. The graduated AE-006a-e model correctly separates continuous monitoring from discrete event response. Threshold percentages (0.70 / 0.80 / 0.88) align with the `ConfigThresholdAdapter` defaults in bootstrap.py, achieving SSOT coherence. The L2-REINJECT annotation on quality-enforcement.md at rank=9 ensures context-rot immunity for these rules. 17 tests confirm the specification changes.

**SPIKE-003 (JsonlTranscriptReader Validation):**
The strongest case for SPIKE-003 is that it fixed a critical semantic error. Using top-level `input_tokens` instead of `message.usage.input_tokens` would have produced wildly incorrect fill estimates — likely underestimates that would cause missed AE-006 escalations at critical fill levels. The backward-seek strategy is algorithmically correct and memory-efficient: it avoids reading multi-MB transcripts into memory for a single read. The three-field sum (`input_tokens + cache_creation_input_tokens + cache_read_input_tokens`) correctly captures cumulative context window usage as defined by the Claude API. The 14 tests use realistic Claude Code JSONL structure.

**EN-007 (Hook Wrapper Scripts):**
The strongest case for EN-007 is its thin-wrapper architecture. Delegating to `jerry --json hooks <event>` via subprocess keeps the wrappers minimal (14 lines each), testable independently of Claude Code, and immune to Python environment issues since `uv run` resolves the environment at invocation time. The `hooks.json` configuration correctly uses `${CLAUDE_PLUGIN_ROOT}` for portability. Fixing SessionStartHandler to use `SessionQualityContextGenerator` (L1 XML) instead of `PromptReinforcementEngine` (L2 text) is architecturally correct: L1 is session-scoped, L2 is per-prompt-scoped. The 224 hook tests with 3647 total passing tests demonstrates integration breadth.

---

### S-002: Devil's Advocate

> What are the strongest counterarguments against each deliverable?

**EN-006 Counterarguments:**

1. **Incomplete timeout propagation:** `session-start.py` and `pre-compact.py` use a `timeout=9` second subprocess timeout, while `hooks.json` allocates `timeout: 10000` ms (10 seconds). This 1-second gap means the wrapper could be killed by the plugin system before the subprocess timeout fires, leaving the subprocess orphaned. The 1-second difference may also be insufficient for cold-start of a `uv run` process on a slow or loaded system.

2. **`abandon_handler: Any` type erasure:** `HooksPreCompactHandler.__init__` accepts `abandon_handler: Any` rather than a typed port interface. This is the only parameter typed as `Any` across all 4 handlers. It violates H-11 semantically — the type hint exists but conveys no type information. There is no `IAbandonSessionCommandHandler` interface.

3. **`get_projects_directory()` inline import:** `HooksSessionStartHandler.handle()` performs a deferred import of `get_projects_directory` from `src.bootstrap` inside the try/except block (line 118). This breaks the composition root pattern (H-09) — the handler is reaching back into bootstrap at runtime rather than receiving the value at construction time. If bootstrap is unavailable or raises during import, the error is silently swallowed as a step failure.

4. **UserPromptSubmit missing `matcher` field:** In `hooks.json`, the `UserPromptSubmit` entry has no `matcher` field, unlike `SessionStart` (matcher: `"*"`) and `PreToolUse` (matcher: `"Write|Edit|MultiEdit|Bash"`). If the Claude Code plugin system requires explicit matchers for UserPromptSubmit, the hook may not fire. This is at minimum inconsistent and deserves explicit documentation of intent.

5. **`_run_enforcement` returns `Any`:** The private method `_run_enforcement` in `HooksPreToolUseHandler` has return type `Any` (line 172). Combined with duck-type access on `.action`, `.reason`, `.violations`, and `.criticality_escalation`, there is no compile-time guarantee that `EnforcementDecision` is the type actually returned. A mismatched return type would fail silently at runtime.

**ST-002 Counterarguments:**

1. **No `AbandonSessionCommand` triggering for AE-006c/d:** AE-006c specifies "auto-checkpoint + reduce verbosity" and AE-006d specifies "mandatory checkpoint + warn user + prepare handoff". The `HooksPromptSubmitHandler` only generates a `context-monitor` tag — it does not create checkpoints or trigger session state changes at these tiers. The AE-006c and AE-006d specifications exist in `.context/rules/` but have no corresponding enforcement implementation in `HooksPromptSubmitHandler`.

2. **L2-REINJECT AE-006 rule text inconsistency:** The L2-REINJECT at rank=9 says "WARNING=log+checkpoint" but AE-006b states "Log warning + consider checkpoint" (SHOULD, not mandatory). The L2 text implies "log AND checkpoint" as a definitive action, while the actual rule only mandates logging. This is a specification inconsistency that may confuse future implementors.

**SPIKE-003 Counterarguments:**

1. **No explicit test for concurrent file access:** The backward-seek strategy opens the file in binary read mode (`rb`) without any locking. In a production environment where Claude Code is actively writing to the transcript while jerry reads it, a partial write at the end of the file could result in `_extract_usage` receiving a truncated JSON line. The reader returns `None` for malformed lines (correct), but if the last complete assistant entry happens to be at a block boundary and the partial line appears to be an assistant entry with incomplete JSON, the reader might scan further back than necessary.

2. **Empty file returns None, not ValueError:** `_find_latest_usage` returns `None` for empty files (line 167), which is then caught at the `read_latest_tokens` level and raises `ValueError`. This is correct behavior. However, the error message says "No entries with message.usage found" for both the empty file case and the case where the file has content but no assistant entries — these are semantically different failure modes that may complicate debugging.

**EN-007 Counterarguments:**

1. **`hooks.json` references `${CLAUDE_PLUGIN_ROOT}/scripts/pre_tool_use.py` for PreToolUse:** The PreToolUse hook has two commands: the new `hooks/pre-tool-use.py` wrapper and a pre-existing `scripts/pre_tool_use.py`. This means architecture enforcement runs twice for Write/Edit/MultiEdit/Bash operations — once from each handler. If `scripts/pre_tool_use.py` produces a `block` decision, the `hooks/pre-tool-use.py` wrapper never runs. If the legacy script produces a `warn` that the new handler would block, the system may be under-enforced. There is no documented intent for this dual-execution order.

2. **`result.stderr` is silently discarded in all wrappers:** The subprocess call uses `capture_output=True` but only writes `result.stdout`. Any stderr output from the jerry CLI (including step failure warnings) is silently discarded by the wrapper. Operational debugging of live hook failures is impossible without wrapper-level stderr propagation.

3. **Exception handler in wrappers catches ALL exceptions with `pass`:** The `except Exception: pass` in every wrapper means that any exception — including `FileNotFoundError`, `PermissionError`, `subprocess.TimeoutExpired` — is swallowed silently. The wrapper always exits 0. This is intentionally fail-open, but `TimeoutExpired` specifically should be distinguishable (it indicates a performance problem) from a generic exception.

---

### S-007: Constitutional Compliance Check

> Check against constitutional constraints: P-003, P-002, H-07/H-08/H-09, H-10, H-11/H-12.

| Rule | Assessment | Status |
|------|-----------|--------|
| P-003: No recursive subagents | Hook wrappers invoke `jerry` CLI via subprocess — this is a single-level delegation (orchestrator calls CLI tool), not a recursive subagent invocation. Compliant. | PASS |
| P-002: File persistence | Checkpoint creation in `HooksPreCompactHandler` persists state to filesystem. `FilesystemCheckpointRepository` is wired in bootstrap. Compliant. | PASS |
| H-07: Domain layer clean | `jsonl_transcript_reader.py` is in infrastructure layer, uses stdlib only. No domain layer violations observed in reviewed files. | PASS |
| H-08: Application layer clean | Reviewed application-layer files (`ITranscriptReader`, `ContextFillEstimator`) import only from domain and application layers. Compliant. | PASS |
| H-09: Composition root exclusivity | VIOLATION (MINOR): `HooksSessionStartHandler.handle()` performs a deferred import of `get_projects_directory` from `src.bootstrap` inside a try/except block at runtime (line 118). Infrastructure adapter instantiation is meant to occur only in bootstrap, not in handler methods. The value should be injected at construction time. | FAIL (minor) |
| H-10: One class per file | `hooks_pre_compact_handler.py` contains a module-level constant `_FALLBACK_FILL_ESTIMATE` that is a `FillEstimate` instance — this is not a class, so H-10 is technically satisfied. All 4 handler files contain exactly one public class. | PASS |
| H-11: Type hints on public functions | VIOLATION: `HooksPreCompactHandler.__init__` has `abandon_handler: Any` — the type annotation exists but uses `Any`, providing no type safety. This is a degraded type hint rather than absence, but it defeats the purpose of H-11 for that parameter. | FAIL (minor) |
| H-12: Docstrings on public functions | All 4 handler files have module docstrings, class docstrings, and method docstrings on all public methods. `__init__` methods have docstrings with Args sections. | PASS |
| H-21: 90% line coverage | 41 tests for EN-006, 17 for ST-002, 14 for SPIKE-003, 224 total hook tests — reported passing. Specific coverage percentage not independently verified in this review. | UNVERIFIED |

---

### S-004: Pre-Mortem Analysis

> Imagine the system failed in production. What went wrong?

**Failure Scenario 1: Silent AE-006c/d Non-Enforcement (HIGH PROBABILITY)**
The graduated AE-006 rules define escalation actions (auto-checkpoint, user warning, handoff preparation) for WARNING and CRITICAL tiers. In production, when context fill reaches 0.80 (CRITICAL tier), `HooksPromptSubmitHandler` generates only a context-monitor XML tag. It does not create a checkpoint, does not warn the user via any mechanism, and does not trigger session state changes. The system has a specification (AE-006c/d) that is not implemented. Users experience context rot without the protective checkpoints that the governance documentation promises.

**Failure Scenario 2: Wrapper Timeout Race (MEDIUM PROBABILITY)**
On a cold system (first `uv run` of the day, PyPI cache empty, slow disk), `uv run jerry --json hooks session-start` takes longer than 9 seconds. The subprocess in `session-start.py` raises `TimeoutExpired`, caught by `except Exception: pass`. Claude starts the session with no additional context — no project context, no quality reinforcement, no resumption checkpoint. From Claude's perspective, it is a fresh session with no JERRY_PROJECT, no AE rules, no governance constraints. The entire L1 reinforcement layer fails silently.

**Failure Scenario 3: Dual PreToolUse Block Decision Conflict (MEDIUM PROBABILITY)**
The `scripts/pre_tool_use.py` (legacy) and `hooks/pre-tool-use.py` (new) both run on Write/Edit/MultiEdit/Bash. If the legacy script emits `{"decision": "block", "reason": "..."}` and the new script emits `{}` (approve), Claude Code combines both hook results — the final decision depends on Claude Code's multi-hook merge semantics (typically first block wins). If the new enforcement engine has different rule coverage than the legacy script, one may block while the other approves the same operation, causing inconsistent behavior that is difficult to debug because both wrappers discard stderr.

**Failure Scenario 4: Bootstrap Runtime Import Failure (LOW-MEDIUM PROBABILITY)**
`HooksSessionStartHandler.handle()` imports `get_projects_directory` from `src.bootstrap` inside a try/except at runtime. If bootstrap fails to import (e.g., missing dependency, circular import introduced by future changes), the exception is caught and logged to stderr — but the stderr output is discarded by the wrapper (`result.stderr` is not propagated). The session starts with empty project context, and the failure is invisible in production logs.

**Failure Scenario 5: Concurrent Compaction + Active Session (LOW PROBABILITY)**
`HooksPreCompactHandler` calls `AbandonSessionCommand(reason="compaction")` which attempts to find and abandon the active session. If no session is currently active in the session repository (e.g., session was never started, or was already abandoned), the `AbandonSessionCommandHandler` may return an empty events list or raise. The handler is fail-open, so it logs to stderr (discarded by wrapper) and emits `{}` without a `session_id`. The checkpoint was created, but the session state is not updated — leaving the repository in an inconsistent state.

---

### S-012: FMEA (Failure Mode and Effects Analysis)

> Systematic failure mode enumeration for each handler.

#### HooksSessionStartHandler

| # | Component | Failure Mode | Effect | Severity | Detection | Current Mitigation |
|---|-----------|-------------|--------|----------|-----------|-------------------|
| 1 | `bootstrap` deferred import | Import fails silently | No project context injected | HIGH | None (stderr discarded) | try/except |
| 2 | `RetrieveProjectContextQuery` dispatch | Query raises for missing project | No project-context XML tag | MEDIUM | None | try/except |
| 3 | `SessionQualityContextGenerator.generate()` | Returns empty preamble | No quality rules in L1 | HIGH | None | if quality_context.preamble check |
| 4 | `checkpoint_repository.load_latest()` | DB/filesystem error | No resumption context | MEDIUM | None | try/except |
| 5 | Subprocess timeout | uv cold start > 9s | ALL context missing | CRITICAL | None | except Exception: pass in wrapper |
| 6 | JERRY_PROJECT env not set | Query returns empty context | No project context | MEDIUM | Logs to stderr | try/except |

#### HooksPromptSubmitHandler

| # | Component | Failure Mode | Effect | Severity | Detection | Current Mitigation |
|---|-----------|-------------|--------|----------|-----------|-------------------|
| 1 | `transcript_path` empty | Context fill skipped | No AE-006 threshold check | HIGH | None | `if transcript_path` guard |
| 2 | `JsonlTranscriptReader` file not found | ValueError/FileNotFoundError | No fill estimate | HIGH | None | try/except |
| 3 | AE-006c not implemented | Fill >= 0.80, no checkpoint created | Context rot continues unguarded | HIGH | None (by design gap) | None |
| 4 | AE-006d not implemented | Fill >= 0.88, no user warning | User unaware of approaching compaction | HIGH | None (by design gap) | None |
| 5 | `PromptReinforcementEngine.generate_reinforcement()` raises | No L2 quality rules injected | Quality degradation | HIGH | None | try/except |

#### HooksPreCompactHandler

| # | Component | Failure Mode | Effect | Severity | Detection | Current Mitigation |
|---|-----------|-------------|--------|----------|-----------|-------------------|
| 1 | `checkpoint_service.create_checkpoint()` fails | No checkpoint created | State lost on compaction | CRITICAL | Logs to stderr | try/except |
| 2 | `abandon_handler.handle()` raises | Session not abandoned | Repository inconsistency | HIGH | Logs to stderr | try/except |
| 3 | `events[0].aggregate_id` fails (empty list) | No session_id in response | Incomplete response | LOW | None | `if events` guard |
| 4 | `context_fill_estimator.estimate()` fails | Uses FALLBACK (0.0, NOMINAL) | Checkpoint created with wrong fill state | MEDIUM | Logs to stderr | Fallback constant |
| 5 | No session active when abandon called | AbandonSession finds nothing | Silent no-op | LOW | None | fail-open |

#### HooksPreToolUseHandler

| # | Component | Failure Mode | Effect | Severity | Detection | Current Mitigation |
|---|-----------|-------------|--------|----------|-----------|-------------------|
| 1 | `_run_enforcement` returns unexpected type | AttributeError on `.action` | Enforcement skipped | HIGH | None | try/except outer |
| 2 | `evaluate_write` raises for large content | Architecture enforcement skipped | Potential H-07/H-08 violation through | HIGH | Logs to stderr | try/except |
| 3 | Staleness check runs after block decision | Redundant: staleness skipped if blocked | Correct by design | LOW | N/A | `"decision" not in response` guard |
| 4 | `MultiEdit` tool_name not in `_WRITE_TOOLS` or `_EDIT_TOOLS` | No enforcement for MultiEdit | Architecture violations slip through | MEDIUM | None | hooks.json matcher includes MultiEdit |
| 5 | Legacy script blocks, new script approves | Conflicting enforcement decisions | Unpredictable enforcement | HIGH | None | Documented dual-execution design |
| 6 | `result.stderr` discarded in wrapper | Enforcement failures invisible in ops | Silent degradation | HIGH | None | None |

---

### S-013: Inversion Technique

> What would make this design terrible? Are any of those present?

The inversion principle: if any of the following were true, the design would be maximally bad. Check which are present.

| Inversion: What Would Be Terrible | Present? | Evidence |
|-----------------------------------|----------|----------|
| Handlers that can block Claude Code operation | NO | All handlers exit 0 always; fail-open everywhere |
| Handlers that emit invalid JSON | NO | All handlers always print `json.dumps(response)` |
| No test coverage for failure paths | NO | Fail-open scenarios are all tested |
| Infrastructure adapters instantiated inside handlers | PARTIAL | `get_projects_directory()` deferred import in SessionStart handler (minor) |
| Type-unsafe composition causing AttributeError silences | YES | `abandon_handler: Any` and `_run_enforcement() -> Any` are type-unsafe; failures swallowed silently |
| AE-006 escalation rules with no enforcement implementation | YES | AE-006c (CRITICAL, auto-checkpoint) and AE-006d (EMERGENCY, mandatory checkpoint) have no enforcement code in PromptSubmitHandler |
| Silent discard of subprocess stderr in production | YES | All 4 wrappers do `capture_output=True` but never write `result.stderr` anywhere |
| Duplicate enforcement with undefined conflict semantics | YES | PreToolUse runs both legacy script and new handler; merge semantics undocumented |
| Governance documentation describes behavior that doesn't exist | YES | AE-006c "auto-checkpoint" and AE-006d "mandatory checkpoint" are in quality-enforcement.md but PromptSubmitHandler does not implement them |

**S-013 finding:** Three non-trivial inversion conditions are present: (1) AE-006c/d specification-implementation gap, (2) silent stderr discard in wrappers, (3) dual PreToolUse enforcement with undefined conflict semantics. None of these prevent the system from functioning, but they represent meaningful divergence from stated design intent.

---

## Per-Deliverable Analysis

### EN-006: jerry hooks CLI Command Namespace

**Summary:** 4 handlers implement a consistent, well-structured CLI namespace for Claude Code hook events. The fail-open design is correct and complete. All handlers follow the same structural pattern, simplifying maintenance.

**Strengths:**
- Uniform `handle(stdin_json) -> int` interface across all 4 handlers
- Step-numbered try/except blocks with named log prefixes (`[hooks/session-start]`, etc.) for operational triage
- Bootstrap wiring is explicit: each dependency is named and constructed at the composition root
- `HooksPreToolUseHandler._run_enforcement()` correctly routes Write vs Edit to different evaluation methods
- Constant set definitions (`_WRITE_TOOLS`, `_EDIT_TOOLS`, `_FILE_TARGET_TOOLS`) at module level for efficiency

**Defects:**
- D-001 (REQUIRED): `abandon_handler: Any` type annotation in `HooksPreCompactHandler` violates type-safety intent of H-11
- D-002 (REQUIRED): Deferred `from src.bootstrap import get_projects_directory` inside `handle()` violates H-09 composition root pattern
- D-003 (RECOMMENDED): `_run_enforcement() -> Any` return type on private method; use `EnforcementDecision | None` for correctness
- D-004 (RECOMMENDED): `MultiEdit` is in `hooks.json` PreToolUse matcher but not in `_WRITE_TOOLS` or `_EDIT_TOOLS` — `MultiEdit` operations receive no architecture enforcement from the new handler

**Test Coverage Assessment:** 41 tests across handler and integration tests. Fail-open paths are tested. Session start checkpoint coverage tested with fixture checkpoint. Verdict: adequate for current phase.

---

### ST-002: AE-006 Graduated Sub-Rules

**Summary:** The specification change is well-executed. The 5 sub-rules correctly model the continuous monitoring lifecycle. The L2-REINJECT annotation ensures the new rules are context-rot immune. The threshold values are correctly aligned with `ConfigThresholdAdapter` defaults.

**Strengths:**
- Clear separation between continuous monitoring tiers (AE-006a-d) and discrete compaction event (AE-006e)
- Threshold values (0.70, 0.80, 0.88) match `ConfigThresholdAdapter` defaults in bootstrap.py — SSOT alignment
- L2-REINJECT at rank=9 provides context-rot immunity
- 17 tests validate the specification

**Defects:**
- D-005 (REQUIRED): AE-006c specifies "auto-checkpoint" and AE-006d specifies "mandatory checkpoint + warn user + prepare handoff" — these actions have no corresponding implementation in `HooksPromptSubmitHandler`. The specification is ahead of the implementation. As written, AE-006b/c/d only produce a context-monitor XML tag, which does not create a checkpoint or warn the user.
- D-006 (RECOMMENDED): L2-REINJECT text for AE-006 (rank=9) reads "WARNING=log+checkpoint" but AE-006b actual rule says "Log warning + consider checkpoint". The L2 text over-commits — "log+checkpoint" implies mandatory checkpoint, but the actual rule uses SHOULD-level language ("consider checkpoint"). Correct L2 text to accurately reflect rule strength.

---

### SPIKE-003: JsonlTranscriptReader Validation

**Summary:** The critical blocker (wrong field path) is correctly identified and fixed. The semantic fix (three-field sum) is correct. The backward-seek implementation is memory-efficient and handles the JSONL format accurately. This is the highest-quality deliverable in this gate.

**Strengths:**
- Correct extraction path: `data["message"]["usage"]` rather than top-level `data["input_tokens"]`
- Correct semantics: sum of `input_tokens + cache_creation_input_tokens + cache_read_input_tokens`
- Backward-seek strategy avoids reading entire large transcript into memory
- Graceful handling of malformed lines (returns None, not raises)
- `ITranscriptReader` Protocol is clean and minimal
- Test helpers build realistic Claude Code JSONL structure

**Defects:**
- D-007 (RECOMMENDED): `ValueError` message does not distinguish between "file is empty" and "file has content but no assistant entries" — these are different failure modes with different debugging implications. Consider separate messages or a typed exception hierarchy.
- D-008 (RECOMMENDED): No test for concurrent file read scenario (partial line at EOF due to active write). The current implementation handles this gracefully (malformed line returns None, scan continues), but this behavior is not documented and not tested.

---

### EN-007: Hook Wrapper Scripts

**Summary:** The thin-wrapper architecture is correct. The SessionStartHandler fix (L1 vs L2 generator) is architecturally important. Merge conflict resolution is complete. 224 tests pass.

**Strengths:**
- 14-line wrapper scripts are minimal and auditable
- `uv run --directory $root` correctly ensures the right Python environment
- `except Exception: pass` is intentionally fail-open (correct for hooks)
- `hooks.json` uses `${CLAUDE_PLUGIN_ROOT}` for deployment portability
- SessionQualityContextGenerator (L1) correctly used for SessionStart; PromptReinforcementEngine (L2) correctly used for UserPromptSubmit

**Defects:**
- D-009 (REQUIRED): All 4 wrappers discard `result.stderr`. When `jerry hooks` handler steps fail, those failures log to stderr internally — but stderr is captured and never propagated. Operational debugging of hook failures is impossible without this output. At minimum, stderr should be written to a log file or propagated to the wrapper's own stderr.
- D-010 (REQUIRED): `hooks.json` PreToolUse has two commands — `scripts/pre_tool_use.py` (legacy) and `hooks/pre-tool-use.py` (new). There is no documentation of the intended execution order, conflict semantics, or migration plan. This creates undefined behavior when the two handlers disagree on enforcement decisions.
- D-011 (RECOMMENDED): Subprocess timeouts in wrappers (9s for session-start/pre-compact, 4s for prompt-submit/pre-tool-use) are 1 second less than `hooks.json` timeouts (10000ms / 5000ms). The gap is intentional (leave buffer for the wrapper process itself) but is undocumented. Document the timeout budget calculation.
- D-012 (RECOMMENDED): `UserPromptSubmit` hook in `hooks.json` has no `matcher` field. Other hooks use explicit matchers. Verify whether the Claude Code plugin system applies the hook to all prompts by default when no matcher is present, and document this explicitly.

---

## Dimensional Scoring

**Scoring Basis:** S-014 (LLM-as-Judge). Active leniency bias counteraction applied. 0.92 means genuinely excellent.

### Completeness (weight: 0.20)

**Definition:** All required deliverables present and all specified requirements addressed.

**Evidence for:**
- All 4 EN-006 handlers implemented (SessionStart, PromptSubmit, PreCompact, PreToolUse)
- All 4 EN-007 wrappers present with hooks.json configuration
- ST-002 AE-006a-e all specified in quality-enforcement.md
- SPIKE-003 critical blocker found, diagnosed, and fixed
- Bootstrap wiring for all 4 handlers

**Evidence against:**
- AE-006c action "auto-checkpoint" not implemented in `HooksPromptSubmitHandler` (D-005)
- AE-006d action "mandatory checkpoint + warn user + prepare handoff" not implemented (D-005)
- `MultiEdit` tool has no enforcement coverage in `HooksPreToolUseHandler` (D-004)
- `result.stderr` discarded in all wrappers — observability requirement unmet (D-009)

**Score:** 0.82 — The core handlers are present but two AE-006 sub-rule actions are specified without implementation, and the observability gap is significant.

---

### Internal Consistency (weight: 0.20)

**Definition:** Deliverables are mutually consistent and do not contradict each other.

**Evidence for:**
- Threshold values in AE-006 sub-rules match `ConfigThresholdAdapter` defaults in bootstrap.py
- SessionQualityContextGenerator (L1) and PromptReinforcementEngine (L2) are correctly assigned to their respective handlers
- Fail-open semantics are consistent across all 4 handlers
- `ITranscriptReader` Protocol correctly matches `JsonlTranscriptReader.read_latest_tokens` signature

**Evidence against:**
- L2-REINJECT rank=9 text ("WARNING=log+checkpoint") contradicts AE-006b rule text ("consider checkpoint" — SHOULD level) (D-006)
- `hooks.json` PreToolUse matcher includes `MultiEdit` but handler has no code for it (D-004)
- `hooks.json` timeout (10000ms) and wrapper subprocess timeout (9000ms) are inconsistent without documented rationale (D-011)
- AE-006c/d governance text describes checkpoint creation behavior that PromptSubmitHandler does not implement (D-005)

**Score:** 0.81 — The L2-REINJECT vs rule text contradiction, the MultiEdit gap, and the AE-006c/d specification-implementation divergence are meaningful consistency failures.

---

### Methodological Rigor (weight: 0.20)

**Definition:** Correct methods applied, design decisions justified, alternatives considered.

**Evidence for:**
- Fail-open pattern is the correct method for Claude Code hooks (hooks must never block)
- Backward-seek strategy is the efficient method for large JSONL files
- Three-field token sum is the correct semantic for context window usage
- Deferred import in `HooksSessionStartHandler` is isolated to try/except (acceptable workaround)
- `_FALLBACK_FILL_ESTIMATE` constant is a clean fallback for unavailable estimation
- `QualityContext.preamble` guard prevents empty string injection

**Evidence against:**
- `abandon_handler: Any` type erasure is a methodological shortcut that should use a port interface (D-001)
- The deferred bootstrap import violates H-09 — the correct method is constructor injection, not runtime import (D-002)
- No typed port interface for `abandon_handler` creates architectural debt
- `_run_enforcement() -> Any` return type lacks rigor — the method should declare its return type (D-003)

**Score:** 0.86 — Strong overall, but the type-unsafe `abandon_handler: Any` and the H-09 violation are methodological weaknesses that should be resolved, not deferred.

---

### Evidence Quality (weight: 0.15)

**Definition:** Claims are substantiated by tests, passing suites, and concrete artifacts.

**Evidence for:**
- 41 handler tests for EN-006 (reported passing)
- 17 specification tests for ST-002 (reported passing)
- 14 reader tests for SPIKE-003 using realistic Claude Code JSONL format
- 224 total hook tests, 3647 total (reported passing)
- Tests use `capsys` to capture and assert JSON structure
- Test fixtures use realistic domain objects (`CheckpointData`, `FillEstimate`, `ThresholdTier`)
- BDD test class structure maps to scenarios

**Evidence against:**
- Coverage percentage not independently verified in this review
- No integration test verifying end-to-end wrapper -> CLI -> handler chain
- AE-006c/d enforcement absence is not tested (no test asserting that checkpoint is NOT created at WARNING tier — absence of test for a gap)
- `MultiEdit` enforcement gap (D-004) has no test coverage

**Score:** 0.88 — Test quality is good; BDD structure, realistic fixtures, and fail-open coverage are strong. Deductions for unverified coverage percentage and lack of end-to-end integration tests.

---

### Actionability (weight: 0.15)

**Definition:** Defects identified are clear, actionable, and traceable to specific code locations.

**Evidence for:**
- All defects include specific file paths, line numbers, and rule references
- REQUIRED defects have unambiguous fixes (type annotation, constructor injection, stderr propagation, dual-hook documentation)
- ST-002 gap (D-005) has a clear remediation path: add checkpoint creation and user notification logic to `HooksPromptSubmitHandler` at tier thresholds
- SPIKE-003 RECOMMENDED defects are non-blocking improvements

**Evidence against:**
- D-010 (dual PreToolUse hooks) requires a design decision about migration path — the "action" is not purely technical but requires a product decision
- D-005 remediation requires non-trivial implementation (adding AbandonSession/checkpoint logic to PromptSubmitHandler) that could introduce new failures

**Score:** 0.91 — High actionability. Most defects have straightforward fixes; the dual-hook migration decision adds modest complexity.

---

### Traceability (weight: 0.10)

**Definition:** Deliverables trace to requirements, ADRs, and governance documents.

**Evidence for:**
- All 4 handlers reference EN-006 in module docstring
- SPIKE-003 references "SPIKE-003: Validation" in `jsonl_transcript_reader.py` docstring
- EN-007 wrappers reference `EN-006: jerry hooks CLI Command Namespace` and `PROJ-004`
- AE-006a-e sub-rules in quality-enforcement.md include L2-REINJECT for context-rot immunity
- `ITranscriptReader` references EN-004 and SPIKE-003

**Evidence against:**
- No ADR for dual-hook architecture decision (legacy + new PreToolUse handlers)
- No documented rationale for why `HooksSessionStartHandler` uses deferred bootstrap import instead of constructor injection
- `hooks.json` timeout values have no traceability to any requirement or design document

**Score:** 0.88 — Solid traceability to EN requirements; gaps for architectural decisions that need ADRs.

---

## Composite Score Calculation

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|---------|
| Completeness | 0.20 | 0.82 | 0.164 |
| Internal Consistency | 0.20 | 0.81 | 0.162 |
| Methodological Rigor | 0.20 | 0.86 | 0.172 |
| Evidence Quality | 0.15 | 0.88 | 0.132 |
| Actionability | 0.15 | 0.91 | 0.137 |
| Traceability | 0.10 | 0.88 | 0.088 |
| **Total** | **1.00** | | **0.855** |

**Weighted Composite Score: 0.855**

---

## Defect Catalogue

### REQUIRED Defects (must be resolved before PASS)

| ID | Deliverable | File | Description | Rule |
|----|------------|------|-------------|------|
| D-001 | EN-006 | `src/interface/cli/hooks/hooks_pre_compact_handler.py:82` | `abandon_handler: Any` provides no type safety. Create an `IAbandonSessionCommandHandler` port interface and use it here. | H-11 |
| D-002 | EN-006 | `src/interface/cli/hooks/hooks_session_start_handler.py:118` | `from src.bootstrap import get_projects_directory` deferred import inside `handle()` violates composition root exclusivity. Inject `projects_dir: Path` at construction time. | H-09 |
| D-005 | ST-002 | `src/interface/cli/hooks/hooks_prompt_submit_handler.py` | AE-006c (CRITICAL tier, >= 0.80) specifies "auto-checkpoint" and AE-006d (EMERGENCY tier, >= 0.88) specifies "mandatory checkpoint + warn user + prepare handoff". Neither action is implemented. `HooksPromptSubmitHandler` must trigger checkpoint creation and user notification at these tiers. | AE-006c, AE-006d |
| D-009 | EN-007 | `hooks/session-start.py`, `hooks/user-prompt-submit.py`, `hooks/pre-compact.py`, `hooks/pre-tool-use.py` | `result.stderr` is captured but never written anywhere. Operational debugging of hook failures is impossible. Propagate stderr to wrapper's own stderr or write to a log file. | H-03 (deception by omission about failures) |
| D-010 | EN-007 | `hooks/hooks.json:39-53` | PreToolUse has two commands (legacy `scripts/pre_tool_use.py` + new `hooks/pre-tool-use.py`) with undefined conflict semantics when enforcement decisions disagree. Document the migration plan and conflict resolution strategy, or remove the legacy hook. | H-03 |

### RECOMMENDED Defects (should be addressed before next gate)

| ID | Deliverable | File | Description |
|----|------------|------|-------------|
| D-003 | EN-006 | `hooks_pre_tool_use_handler.py:172` | `_run_enforcement() -> Any` should return `EnforcementDecision | None` for correctness and IDE support. |
| D-004 | EN-006 | `hooks_pre_tool_use_handler.py:46-52` | `MultiEdit` is in `hooks.json` PreToolUse matcher but absent from `_WRITE_TOOLS` and `_EDIT_TOOLS`. Add `MultiEdit` to the appropriate set or document why it should not be enforced. |
| D-006 | ST-002 | `.context/rules/quality-enforcement.md:39` | L2-REINJECT rank=9 text "WARNING=log+checkpoint" contradicts AE-006b rule ("consider checkpoint" — SHOULD). Correct L2 text to "WARNING=log+consider-checkpoint" to accurately reflect rule strength. |
| D-007 | SPIKE-003 | `jsonl_transcript_reader.py:93-95` | `ValueError` message does not distinguish empty file from no-usage-entries cases. Consider distinct error messages or typed exception subclasses. |
| D-008 | SPIKE-003 | `jsonl_transcript_reader.py` | No test for partial line at EOF (concurrent write scenario). Add a test and document the behavior in the docstring. |
| D-011 | EN-007 | `hooks/*.py`, `hooks/hooks.json` | Subprocess timeout (9s/4s) vs hooks.json timeout (10s/5s) gap is undocumented. Add a comment explaining the 1-second buffer rationale. |
| D-012 | EN-007 | `hooks/hooks.json:16-25` | `UserPromptSubmit` has no `matcher` field; verify Claude Code behavior when matcher is absent and document intent. |

---

## Verdict

**Weighted Composite Score: 0.855**

**Band: REVISE** (0.85 - 0.91)

### REVISE

The score of 0.855 falls in the REVISE band, which is below the 0.92 threshold required for C3 deliverables per H-13. This is not a REJECTED outcome — the core implementation is structurally sound, tests are passing, and the fundamental fail-open architecture is correct. However, there are two blocking issues that prevent acceptance:

1. **Specification-implementation gap (D-005):** AE-006c and AE-006d are the core governance specification for context resilience — the primary purpose of PROJ-004. Having these rules documented without enforcement implementation means the system does not deliver on its stated purpose at critical fill levels.

2. **Silent failure in production (D-009, D-010):** The combination of stderr discard in wrappers and undefined dual-hook conflict semantics creates a system that fails silently and unpredictably, making the hooks operationally unmaintainable.

### Required Actions for Iteration 2

1. **D-005:** Implement AE-006c and AE-006d enforcement in `HooksPromptSubmitHandler`. At CRITICAL tier (>= 0.80): trigger checkpoint creation. At EMERGENCY tier (>= 0.88): trigger checkpoint + emit user warning in `additionalContext` + include handoff state in response. Wire new dependencies in `create_hooks_handlers()`.

2. **D-001:** Replace `abandon_handler: Any` with a proper port interface (create `IAbandonSessionCommandHandler` or use the concrete type `AbandonSessionCommandHandler`).

3. **D-002:** Move `get_projects_directory()` call from `HooksSessionStartHandler.handle()` into constructor or bootstrap wiring.

4. **D-009:** Propagate `result.stderr` in all 4 wrapper scripts (write to wrapper's own stderr, or log to `.jerry/logs/hook-errors.log`).

5. **D-010:** Either document the dual-PreToolUse hook conflict semantics with an ADR, or remove the legacy hook from `hooks.json` if `hooks/pre-tool-use.py` provides equivalent coverage.

### Iteration 2 Target

Resolving D-001 through D-005 and D-009/D-010 should raise:
- Completeness from 0.82 to ~0.92 (AE-006c/d implemented, MultiEdit covered)
- Internal Consistency from 0.81 to ~0.90 (L2-REINJECT fixed, MultiEdit gap closed)
- Methodological Rigor from 0.86 to ~0.92 (type safety restored, H-09 fixed)
- Traceability from 0.88 to ~0.92 (ADR for dual-hook, constructor injection documented)

Projected composite after iteration 2 resolutions: **~0.93** (PASS threshold reached).
