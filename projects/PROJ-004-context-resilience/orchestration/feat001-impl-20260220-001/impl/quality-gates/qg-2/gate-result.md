# QG-2 Gate Result: Bounded Context + Services Review

<!-- VERSION: 1.0.0 | DATE: 2026-02-20 | GATE: QG-2 | AGENT: adv-scorer -->

> **Gate:** QG-2 (after Phase 3, before Phase 4)
> **Criticality:** C3
> **Threshold:** >= 0.92 weighted composite
> **Outcome:** REVISE (see Section 6)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Gate outcome and key findings |
| [S-003 Steelman](#s-003-steelman) | Strongest design aspects |
| [S-007 Constitutional AI](#s-007-constitutional-ai) | Hard rule compliance |
| [S-002 Devil's Advocate](#s-002-devils-advocate) | Challenges to design decisions |
| [S-004 Pre-Mortem](#s-004-pre-mortem) | Production failure scenarios |
| [S-012 FMEA](#s-012-fmea) | Systematic failure mode analysis |
| [S-013 Inversion](#s-013-inversion) | Fragile assumptions |
| [EN-003 Scoring](#en-003-bounded-context-foundation-scoring) | Dimension scores |
| [EN-004 Scoring](#en-004-application-services-scoring) | Dimension scores |
| [EN-005 Scoring](#en-005-staleness-detection-scoring) | Dimension scores |
| [Overall Composite](#overall-composite-score) | Weighted score and outcome |
| [Defect Report](#defect-report) | All defects with severity |

---

## Executive Summary

QG-2 review covers EN-003 (Bounded Context Foundation), EN-004 (Application Services), and EN-005 (Staleness Detection) across 168 passing unit tests and 25 source files.

**Gate Outcome: REVISE (0.88 composite)**

Two blocking defects prevent a PASS:

1. **DEF-001 [REQUIRED]:** `StalenessDetector` in the application layer imports `yaml` (a third-party library), violating architecture rule H-08. The application layer may only import from the domain layer. YAML parsing must be moved to the infrastructure layer.

2. **DEF-002 [REQUIRED]:** `JsonlTranscriptReader._read_last_line` fails silently when the last JSONL entry exceeds 4096 bytes (one `_READ_BLOCK_SIZE` block). The backward-seek logic returns a partial line fragment as the "last nonempty line," which then fails JSON parsing. In production, this causes `ContextFillEstimator` to silently fall back to NOMINAL fill=0.0, rendering monitoring invisible for large transcript entries. This is confirmed by live test execution.

The remaining five defects are RECOMMENDED or INFORMATIONAL and do not block Phase 4.

Overall test quality is excellent: 168 tests pass, coverage of scenarios is thorough, and the fail-open design philosophy is well-executed throughout.

---

## S-003 Steelman

*Identifying the strongest design decisions before critique (H-16 compliance).*

**Architecture discipline is exemplary.** The hexagonal layer separation is clean across EN-003 and EN-004: value objects contain no business logic leakage, ports are pure Protocol definitions with zero coupling to implementations, and bootstrap.py is the sole composition root. The EN-003 bounded context mirrors the `session_management` and `work_tracking` patterns exactly, making it immediately navigable by any contributor.

**Fail-open philosophy is consistently applied.** `ContextFillEstimator.estimate()` catches all exceptions from the transcript reader. `CheckpointService._build_resumption_state()` catches `OSError` and `PermissionError`. `StalenessDetector._evaluate_staleness()` wraps the entire evaluation in a bare `except Exception`. The LLM monitoring system cannot disrupt the main workflow under any read failure — this is the right design priority.

**Test specificity is strong.** The parametrized tier boundary tests in `test_context_fill_estimator.py` cover all 5 tiers including the exact boundary values (0.55, 0.70, 0.80, 0.88). The `test_staleness_detector.py` covers 15+ edge cases including null values, binary content, missing keys, and absolute vs relative paths. This level of scenario coverage exceeds what would be minimally required.

**Value object immutability is rigorously enforced and tested.** All six value objects (`ThresholdTier`, `FillEstimate`, `CheckpointData`, `ContextState`, `StalenessResult`, and the three domain events) use `@dataclass(frozen=True)`, and each has at least one immutability test with `pytest.raises(AttributeError)`.

**Backward-seek strategy in `JsonlTranscriptReader` is correct in design intent.** For the common case (last line < 4096 bytes), the O(1) seek from the end is an elegant, performant approach that avoids loading potentially multi-megabyte transcripts into memory. The design intent is sound; only the edge-case implementation has a defect.

**Bootstrap wiring is complete and well-organized.** All EN-002/EN-003/EN-004 components are wired with clear comment anchors, singleton factories, and a `reset_singletons()` function for test isolation. The factory chain (`get_transcript_reader()` -> `get_context_fill_estimator()` -> `get_checkpoint_service()`) is navigable and correct.

---

## S-007 Constitutional AI

*Checking compliance with HARD architectural rules H-07 through H-12, H-20.*

### H-07: Domain Layer — No External Imports

**STATUS: PASS**

All five domain value objects (`threshold_tier.py`, `fill_estimate.py`, `checkpoint_data.py`, `context_state.py`, `staleness_result.py`) and all three domain events import only: `__future__`, `dataclasses`, `enum`, `datetime`, `typing`, and `src.context_monitoring.domain.*` or `src.shared_kernel.*`. No third-party or application-layer imports. Domain events import `src.shared_kernel.domain_event` which is explicitly permitted by architecture standards.

### H-08: Application Layer — No Infrastructure Imports

**STATUS: FAIL — DEF-001**

`src/context_monitoring/application/services/staleness_detector.py` imports `yaml` at line 31:

```python
import yaml
```

The architecture standards table states: application/ can import `domain` only. The `yaml` library is a third-party dependency and does not belong in the application layer. The YAML parsing logic (`yaml.safe_load`) must be moved to the infrastructure layer. See DEF-001 for the resolution path.

All other application-layer files comply: `checkpoint_service.py`, `context_fill_estimator.py`, `resumption_context_generator.py`, `checkpoint_repository.py`, `transcript_reader.py`, and `threshold_configuration.py` import only domain types, stdlib (`pathlib`, `datetime`, `logging`, `typing`), and same-layer ports.

### H-09: Composition Root Exclusivity

**STATUS: PASS**

Infrastructure adapters (`FilesystemCheckpointRepository`, `JsonlTranscriptReader`, `ConfigThresholdAdapter`) are instantiated exclusively in `bootstrap.py`. No service or handler instantiates its own dependencies. Verified by inspection.

### H-10: One Class Per File

**STATUS: PASS**

Every source file contains exactly one public class or Protocol:
- `threshold_tier.py`: `ThresholdTier`
- `fill_estimate.py`: `FillEstimate`
- `checkpoint_data.py`: `CheckpointData`
- `context_state.py`: `ContextState`
- `staleness_result.py`: `StalenessResult`
- `context_threshold_reached.py`: `ContextThresholdReached`
- `compaction_detected.py`: `CompactionDetected`
- `checkpoint_created.py`: `CheckpointCreated`
- `checkpoint_repository.py`: `ICheckpointRepository`
- `transcript_reader.py`: `ITranscriptReader`
- `checkpoint_service.py`: `CheckpointService`
- `context_fill_estimator.py`: `ContextFillEstimator`
- `resumption_context_generator.py`: `ResumptionContextGenerator`
- `staleness_detector.py`: `StalenessDetector`
- `filesystem_checkpoint_repository.py`: `FilesystemCheckpointRepository`
- `jsonl_transcript_reader.py`: `JsonlTranscriptReader`

Module-level constants (`_FAIL_OPEN_ESTIMATE`, `_PASSTHROUGH`, `_TIER_ACTION_TEXT`) do not count as classes.

### H-11: Type Hints Required on Public Functions

**STATUS: PASS (with minor observation)**

All public method signatures have type hints. Private methods (`_classify_tier`, `_build_resumption_state`, `_read_last_line`, `_extract_last_nonempty_line`, etc.) are exempt from H-11 by definition. One minor observation: `_serialize_recovery_state(self, state: dict)` uses an unparameterized `dict` — not a H-11 violation (private method) but noted as INFORMATIONAL in DEF-007.

### H-12: Docstrings Required on Public Functions

**STATUS: PASS**

All public methods have docstrings with Args, Returns, and where appropriate Raises sections. Private methods also carry docstrings. Example docstrings are provided in most classes.

### H-20: Test-First BDD Approach

**STATUS: PASS**

All tests are structured around BDD scenarios from the entity acceptance criteria. Test class names reference specific BDD scenarios (`TestTierClassification`, `TestFailOpen`, `TestStaleOrchestrationWarning`). Parametrized tests cover all boundary values from EN-004 BDD examples.

---

## S-002 Devil's Advocate

*Challenging design decisions.*

### Tier Boundary Values

**Challenge:** Are the tier boundaries (NOMINAL<0.55, LOW 0.55-0.70, WARNING 0.70-0.80, CRITICAL 0.80-0.88, EMERGENCY>0.88) correct and verified?

**Finding:** The `_classify_tier` implementation correctly implements these boundaries. The `get_threshold()` calls fetch "nominal", "warning", "critical", "emergency" — notably there is no `get_threshold("low")` call. The LOW tier is inferred as the range between nominal and warning thresholds. This is correct but subtle: if a future configuration author expected `low_threshold` to be configurable separately, they would be disappointed. The tier classification logic (checking emergency first, cascading down) is correct.

The test coverage at 0.55 exactly (`110_000/200_000`) correctly maps to LOW. All five boundaries are tested including exact boundary values.

**Verdict:** Boundaries are correct and verified. No defect.

### Fail-Open Appropriateness

**Challenge:** Is fail-open appropriate for ALL failure modes?

**Finding:** For `ContextFillEstimator`, fail-open returning NOMINAL is correct: context monitoring must never disrupt the main workflow. For `CheckpointService`, fail-open (missing ORCHESTRATION.yaml) returning `None` resumption state is correct. For `StalenessDetector`, fail-open (corrupted YAML) returning passthrough is correct.

However: `JsonlTranscriptReader._read_last_line` has an implementation bug that causes it to ALWAYS fail silently for transcript entries > 4096 bytes (see DEF-002). The fail-open behavior in `ContextFillEstimator` means this is operationally recoverable, but it creates a systematic blind spot: any session with large tool responses will always show NOMINAL fill regardless of actual context use.

**Verdict:** Fail-open philosophy is correct. Implementation has a defect (DEF-002).

### JSONL Seek-to-End for Edge Cases

**Challenge:** Can the backward-seek approach fail?

**Finding:** Confirmed failure mode. When the last JSONL line is larger than `_READ_BLOCK_SIZE` (4096 bytes), the reader returns the TAIL fragment of that line (the bytes in the last block), which is not valid JSON. The `_extract_last_nonempty_line` function returns this fragment as soon as it finds any non-empty content in the accumulated bytes — it does not check whether it has found a complete line starting from a newline boundary. See DEF-002.

Claude Code transcript entries routinely exceed 4096 bytes when tool results include file reads, command output, or search results. This is not a rare edge case.

**Verdict:** Defect confirmed (DEF-002, REQUIRED).

### Missing Error Paths

**Finding:** `FilesystemCheckpointRepository._load_all_sorted` catches `json.JSONDecodeError, KeyError, ValueError` but not `OSError`. If `AtomicFileAdapter.read_with_lock()` raises `OSError` (e.g., permission denied mid-scan), it propagates uncaught to the caller. `get_latest_unacknowledged()` would raise unexpectedly. See DEF-004 (RECOMMENDED).

---

## S-004 Pre-Mortem

*Imagining production failures.*

### Scenario: Transcript file corrupted mid-write

**Analysis:** Claude Code writes transcript JSONL entries as the session progresses. If the last entry is partially written (power loss, disk full), the last line would be truncated JSON. `JsonlTranscriptReader.read_latest_tokens()` would raise `ValueError` ("Last line of transcript is not valid JSON"). `ContextFillEstimator` catches this and returns NOMINAL. The session continues. This is correct behavior: corrupted transcript is handled gracefully.

**Risk Level:** Low — fail-open handles this correctly.

### Scenario: Token counts overflow int

**Analysis:** Python integers are arbitrary precision — there is no overflow. The `token_count: int | None` field in `FillEstimate` uses Python's native int. Even if token counts grew beyond 32-bit or 64-bit ranges (impossible in practice for LLM context windows), Python handles it. `fill_percentage = token_count / context_window` uses float division, capped by the 200K context window.

**Risk Level:** None — Python integers do not overflow.

### Scenario: Checkpoint files locked by concurrent process

**Analysis:** `FilesystemCheckpointRepository` uses `AtomicFileAdapter.write_atomic()` for checkpoint writes and `.read_with_lock()` for reads. If a lock cannot be acquired (another process holds it), `PermissionError` is raised from `write_atomic()`. This propagates through `CheckpointService.create_checkpoint()` to the caller (session-start hook). The hook would fail, but the main session would continue. This is acceptable but not explicitly documented as a known failure mode.

**Risk Level:** Medium — concurrent access during hook execution could cause checkpoint loss. No test covers this scenario. See DEF-005 (RECOMMENDED).

### Scenario: Checkpoint directory has 1000+ checkpoints

**Analysis:** `next_checkpoint_id()` calls `max()` on a list of parsed IDs. With 1000 checkpoints (`cx-001` through `cx-1000`), `_parse_id_number` parses `int("1000")` correctly. The `cx-{n:03d}` format would produce `cx-1000` (4 digits, not 3), which is fine. However, the glob `cx-*.json` would return all 1000 files, all would be sorted and iterated. Performance degrades linearly with checkpoint count. No cleanup mechanism exists.

**Risk Level:** Low-Medium — no correctness issue, but operational debt. See DEF-006 (RECOMMENDED).

---

## S-012 FMEA

*Systematic failure mode analysis.*

### ContextFillEstimator Failure Modes

| Failure Mode | Effect | Mitigation | Residual Risk |
|---|---|---|---|
| Transcript file missing | NOMINAL returned (fail-open) | Exception caught | None — by design |
| Transcript file empty | NOMINAL returned (fail-open) | Exception caught | None — by design |
| Last JSONL entry > 4096 bytes | NOMINAL returned silently | Exception caught | HIGH — systematic monitoring blind spot |
| context_window = 0 | ZeroDivisionError -> NOMINAL (fail-open) | Exception caught | Low — uncommon, handled |
| `get_threshold()` raises ValueError | Propagates uncaught | Not caught | Medium — bad tier name crashes estimate() |
| Monitoring disabled | NOMINAL returned | is_enabled() check | None — by design |

**Finding:** The `get_threshold()` call in `_classify_tier` is NOT wrapped in exception handling. If a bad tier key is passed (impossible via the current implementation since keys are hardcoded, but possible via future misconfiguration of `get_threshold`), the exception propagates out of `estimate()`. The `estimate()` docstring says "Fail-open: Any exception from the reader..." — but exceptions from `_classify_tier` are NOT caught. This is a narrow gap. See DEF-003 (RECOMMENDED).

### JsonlTranscriptReader Failure Modes

| Failure Mode | Effect | Mitigation | Residual Risk |
|---|---|---|---|
| File not found | FileNotFoundError raised | Documented, caller fail-open | None |
| Empty file | ValueError raised | Documented, caller fail-open | None |
| Only whitespace | ValueError raised | Documented, caller fail-open | None |
| Last line truncated (< 4096 B) | ValueError raised | Caller fail-open | None |
| Last line > 4096 B (complete) | ValueError raised | Caller fail-open | HIGH — systematic blind spot |
| Unicode decode error | Replaced chars, likely JSON parse failure | `errors="replace"` in decode | Low |
| `input_tokens` field missing | ValueError raised | Documented, caller fail-open | None |
| `input_tokens` not int-castable | ValueError raised | Caller fail-open | None |

### CheckpointService Failure Modes

| Failure Mode | Effect | Mitigation | Residual Risk |
|---|---|---|---|
| ORCHESTRATION.yaml absent | None resumption_state | Fail-open, documented | None |
| ORCHESTRATION.yaml unreadable | None resumption_state | OSError caught | None |
| ORCHESTRATION.yaml very large | Memory usage, slow read | None mitigated | Low |
| repository.save() raises | Exception propagates | Not caught | Medium — checkpoint lost |
| repository.next_checkpoint_id() raises | Exception propagates | Not caught | Medium — checkpoint not created |

### FilesystemCheckpointRepository Failure Modes

| Failure Mode | Effect | Mitigation | Residual Risk |
|---|---|---|---|
| Checkpoint dir unwritable | OSError from mkdir() | Not caught | Medium |
| AtomicFileAdapter.read_with_lock() raises OSError | Propagates from _load_all_sorted | Not caught | Medium — DEF-004 |
| Checkpoint JSON corrupted | Logged, skipped | json.JSONDecodeError caught | None |
| Malformed checkpoint filename | _parse_id_number fails | Not caught | Low — glob pattern limits this |
| Concurrent write during next_checkpoint_id | Race condition, duplicate IDs | Atomic writes help but don't fully prevent | Low — sessions are generally sequential |

---

## S-013 Inversion

*What would make this architecture FAIL?*

### Most Fragile Assumption: Last JSONL Line is Always < 4096 Bytes

The entire transcript reading mechanism assumes that the last line of a Claude Code JSONL file fits within a single 4096-byte read block. This assumption fails whenever a tool result, file content, or search result is included in the last entry. Claude Code regularly produces entries with multi-kilobyte tool results. This is the single most fragile assumption in the entire implementation. **It is already broken** (DEF-002).

### Fragile Assumption: ORCHESTRATION.yaml Stored as Raw Text

`CheckpointService._build_resumption_state()` stores the ORCHESTRATION.yaml content as a raw text string: `{"orchestration": <yaml_text>}`. `ResumptionContextGenerator._serialize_recovery_state()` then renders this as:

```xml
<orchestration>current_phase: implementation
entity_id: EN-003
</orchestration>
```

This is functional but the YAML content embedded in XML could confuse an LLM parsing the resumption context, since the YAML structure (colons, indentation) is not XML-escaped. It works, but is semantically ambiguous.

### Fragile Assumption: StalenessDetector Can Parse YAML in Application Layer

The `StalenessDetector` currently uses `yaml.safe_load()` directly in the application layer. This violates H-08. Moving it to infrastructure requires a port (e.g., `IOrchestrationReader` port) or simply relocating the file to `infrastructure/adapters/`. The current placement will fail CI if architecture tests are enforced (H-08).

### Fragile Assumption: XML Key Safety in ResumptionContextGenerator

`_serialize_recovery_state()` sanitizes keys only by replacing spaces with underscores. Keys containing `<`, `>`, `&`, or `"` characters would produce malformed XML. If the ORCHESTRATION.yaml text is passed through as a dict value (e.g., if the format changes from raw text to parsed dict), XML injection becomes possible. See DEF-007 (INFORMATIONAL).

### Dependency That Could Break: AtomicFileAdapter FileLock

The `FilesystemCheckpointRepository` depends on `AtomicFileAdapter`, which uses `filelock.FileLock`. If the `filelock` package is unavailable or if the lock directory is on a filesystem that doesn't support file locks (e.g., certain NFS mounts), all checkpoint operations would fail. No fallback exists.

---

## EN-003: Bounded Context Foundation Scoring

| Dimension | Weight | Score | Evidence |
|-----------|--------|-------|---------|
| Completeness | 0.20 | 0.93 | All 4 value objects, 3 events, 1 service, 1 port, 1 adapter, all wired in bootstrap. Minor gap: DEF-004 (missing OSError in _load_all_sorted). Entity checklist nearly complete; DEF-005 acknowledgment timing not tested at integration level. |
| Internal Consistency | 0.20 | 0.88 | H-08 violation (yaml in application) is an internal consistency failure. Otherwise perfectly consistent: all value objects are frozen, all ports are Protocol, all adapters use AtomicFileAdapter. The marker file naming in EN-003 BDD scenario (`cx-001-checkpoint.json.acknowledged`) differs from implementation (`cx-001.acknowledged`) — minor doc inconsistency. |
| Methodological Rigor | 0.20 | 0.90 | BDD scenarios properly structured, boundary conditions tested. Missing: OSError test in _load_all_sorted, no test for malformed checkpoint filenames, no integration-level DEF-005 test. |
| Evidence Quality | 0.15 | 0.92 | 168 tests pass. All EN-003 BDD scenarios covered by tests (save/retrieve, sequential IDs, acknowledged filtering, fail-open, directory autocreation). |
| Actionability | 0.15 | 0.88 | H-08 violation is actionable but blocks. DEF-004 (OSError) is easy to fix. Acknowledge timing (DEF-005) requires integration test in Phase 4 hook handler. |
| Traceability | 0.10 | 0.93 | Every source file references EN-003 in module docstring. Bootstrap.py has EN-003 comment anchors. Test files reference entity and project. ICheckpointRepository.next_checkpoint_id() is not mentioned in EN-003 acceptance checklist (minor gap). |

**EN-003 Weighted Score:** (0.93×0.20) + (0.88×0.20) + (0.90×0.20) + (0.92×0.15) + (0.88×0.15) + (0.93×0.10)

= 0.186 + 0.176 + 0.180 + 0.138 + 0.132 + 0.093 = **0.905**

---

## EN-004: Application Services Scoring

| Dimension | Weight | Score | Evidence |
|-----------|--------|-------|---------|
| Completeness | 0.20 | 0.88 | ContextFillEstimator, ResumptionContextGenerator, ITranscriptReader, JsonlTranscriptReader all implemented and wired. DEF-002 (large last-line) is a functional completeness gap: the service cannot correctly read token counts for entries > 4096 bytes. Missing: context_window=0 guard, XML escaping in ResumptionContextGenerator. |
| Internal Consistency | 0.20 | 0.87 | ContextFillEstimator.estimate() docstring says "Any exception from the reader" is caught, but _classify_tier exceptions are not covered by this claim (DEF-003). generate_context_monitor_tag is on ContextFillEstimator but feels like a formatting concern that could be separate. Overall design is consistent with ports-and-adapters. |
| Methodological Rigor | 0.20 | 0.86 | 10-case parametrized tier tests, fail-open tests for 3+ exception types, XML structure tests, token budget test. Missing: test for last line > 4096 bytes (the confirmed bug), test for context_window=0, test for XML injection in recovery state. |
| Evidence Quality | 0.15 | 0.87 | All EN-004 BDD scenarios pass. The confirmed bug (DEF-002) is not caught by any test — an evidence quality gap: the tests do not discover the real-world failure mode. |
| Actionability | 0.15 | 0.85 | DEF-002 fix is well-defined (accumulate full line before returning). DEF-003 fix is one try/except. XML escaping (DEF-007) is standard. All defects have clear resolution paths. |
| Traceability | 0.10 | 0.93 | Source files reference EN-004. Bootstrap references EN-004 comment anchors. Test files reference entity. All 5 BDD scenarios from EN-004 are tested. |

**EN-004 Weighted Score:** (0.88×0.20) + (0.87×0.20) + (0.86×0.20) + (0.87×0.15) + (0.85×0.15) + (0.93×0.10)

= 0.176 + 0.174 + 0.172 + 0.131 + 0.128 + 0.093 = **0.874**

---

## EN-005: Staleness Detection Scoring

| Dimension | Weight | Score | Evidence |
|-----------|--------|-------|---------|
| Completeness | 0.20 | 0.92 | All 4 EN-005 BDD scenarios covered (passthrough, stale warning, fresh passthrough, unparseable fail-open). Path matching handles absolute paths, relative paths, nested paths. StalenessResult value object is correct. Missing: integration with `jerry hooks pre-tool-use` (EN-006 dependency, acceptable at this gate). |
| Internal Consistency | 0.20 | 0.82 | H-08 violation: `yaml` import in application layer is a direct architectural inconsistency. The service correctly belongs in application but its dependency on yaml is an infrastructure concern. The `_PASSTHROUGH` module-level singleton is a minor style concern (frozen dataclass, safe to share). |
| Methodological Rigor | 0.20 | 0.91 | 20+ test cases including binary content, null values, empty strings, absolute paths, nested paths, equal timestamps. The BDD test structure is comprehensive. |
| Evidence Quality | 0.15 | 0.93 | All test classes directly map to BDD scenarios. Boundary condition (updated_at == reference_time) is tested. Multiple fail-open conditions independently tested. |
| Actionability | 0.15 | 0.88 | H-08 fix is well-scoped: either move the file to infrastructure/adapters/ or introduce an IOrchestrationReader port. The `yaml` import is the only violation. The EN-005 acceptance criterion says "appropriate layer" — infrastructure is clearly more appropriate. |
| Traceability | 0.10 | 0.93 | Source files reference EN-005. StalenessResult references EN-005. Test file references entity and scenario names. EN-006 dependency noted in comments. |

**EN-005 Weighted Score:** (0.92×0.20) + (0.82×0.20) + (0.91×0.20) + (0.93×0.15) + (0.88×0.15) + (0.93×0.10)

= 0.184 + 0.164 + 0.182 + 0.140 + 0.132 + 0.093 = **0.895**

---

## Overall Composite Score

| Deliverable | Score | Equal Weight |
|-------------|-------|-------------|
| EN-003 Bounded Context Foundation | 0.905 | 0.302 |
| EN-004 Application Services | 0.874 | 0.291 |
| EN-005 Staleness Detection | 0.895 | 0.298 |

**Overall Composite: (0.905 + 0.874 + 0.895) / 3 = 0.891**

| Band | Score Range | Outcome |
|------|------------|---------|
| PASS | >= 0.92 | -- |
| **REVISE** | **0.85 - 0.91** | **SELECTED** |
| REJECTED | < 0.85 | -- |

**Gate Outcome: REVISE**

Score is 0.891, placing this in the REVISE band. The two REQUIRED defects (DEF-001, DEF-002) are the primary score depressors across Internal Consistency and Methodological Rigor dimensions. Fixing both defects is expected to bring the composite above 0.92.

---

## Defect Report

### DEF-001: REQUIRED — H-08 Violation: yaml Import in Application Layer

```
DEF-001: REQUIRED
File: src/context_monitoring/application/services/staleness_detector.py
Line: 31
Issue: `import yaml` in application/services/ violates H-08. The application
       layer must not import infrastructure or external libraries. YAML parsing
       is an infrastructure concern. This will cause CI failure if architecture
       tests enforce H-08.
Fix: Option A (preferred): Move staleness_detector.py to
     src/context_monitoring/infrastructure/adapters/staleness_detector.py.
     Update all imports and bootstrap wiring accordingly.
     Option B: Introduce IOrchestrationReader port in application/ports/,
     implement YamlOrchestrationReader in infrastructure/adapters/,
     inject via constructor. This adds a port-adapter pair for one method.
     Option A is simpler and sufficient since StalenessDetector has no
     domain-layer contract — it is a pure infrastructure adapter.
```

### DEF-002: REQUIRED — JsonlTranscriptReader Fails for Last Line > 4096 Bytes

```
DEF-002: REQUIRED
File: src/context_monitoring/infrastructure/adapters/jsonl_transcript_reader.py
Lines: 103-164
Issue: _read_last_line returns a PARTIAL LINE when the last JSONL entry
       exceeds _READ_BLOCK_SIZE (4096 bytes). The _extract_last_nonempty_line
       method returns immediately upon finding any non-empty content in the
       accumulated bytes, but the content may be only the tail fragment of the
       last JSON object. This causes json.JSONDecodeError -> ValueError in
       read_latest_tokens(). ContextFillEstimator silently falls back to
       NOMINAL, rendering monitoring invisible for sessions with large tool
       results. Confirmed by live test with a 5KB last-line entry.
Fix: Replace _extract_last_nonempty_line early-return logic with a check
     that the candidate line is preceded by a newline (or is at file position 0).
     The accumulated buffer must contain the COMPLETE last line before returning.
     Specifically: after splitting on newlines, the "last" line is only valid
     if there is a newline BEFORE it in the accumulated data. If the accumulated
     data does not contain at least one newline before the last non-empty content,
     continue accumulating. Pseudocode:
       lines = text.splitlines()
       # At least 2 lines means we've crossed a newline boundary before the last
       if len(lines) >= 2:
           for line in reversed(lines):
               if line.strip():
                   return line.strip()
       return None  # need more data
     Also add a regression test: a single-line JSONL file where the entry
     is > 4096 bytes must return the correct input_tokens value.
```

### DEF-003: RECOMMENDED — _classify_tier Exceptions Not Caught by Fail-Open

```
DEF-003: RECOMMENDED
File: src/context_monitoring/application/services/context_fill_estimator.py
Lines: 135-152
Issue: estimate() wraps only the reader.read_latest_tokens() call in a
       try/except. The subsequent _classify_tier() call (which calls
       get_threshold() four times) is not covered. If get_threshold()
       raises an unexpected exception (e.g., due to configuration corruption),
       it propagates out of estimate() despite the docstring claiming
       "Fail-open: Any exception from the reader." This is a documentation
       inconsistency and a narrow but real failure path.
Fix: Either extend the try/except to cover token_count / context_window
     and _classify_tier(), or add a top-level try/except around the
     entire method body. The fail-open sentinel _FAIL_OPEN_ESTIMATE should
     be returned for any exception, not just reader exceptions.
     The docstring should be updated to reflect the actual scope.
```

### DEF-004: RECOMMENDED — FilesystemCheckpointRepository Missing OSError in _load_all_sorted

```
DEF-004: RECOMMENDED
File: src/context_monitoring/infrastructure/adapters/filesystem_checkpoint_repository.py
Lines: 182-192
Issue: _load_all_sorted catches json.JSONDecodeError, KeyError, ValueError
       but NOT OSError (or its subclass PermissionError). AtomicFileAdapter
       .read_with_lock() raises OSError if the file cannot be read.
       An OSError propagates to get_latest_unacknowledged() and list_all(),
       which would raise unexpectedly. The repository has no explicit
       contract about this behavior.
Fix: Add OSError to the except tuple in _load_all_sorted:
       except (json.JSONDecodeError, KeyError, ValueError, OSError) as exc:
     Add a test: mock AtomicFileAdapter.read_with_lock to raise OSError
     and verify that get_latest_unacknowledged() skips the file and
     continues (or returns None gracefully).
```

### DEF-005: RECOMMENDED — No Test for Concurrent Checkpoint Access Failure

```
DEF-005: RECOMMENDED
File: src/context_monitoring/infrastructure/adapters/filesystem_checkpoint_repository.py
Issue: No test covers the case where FileLock cannot be acquired during
       checkpoint save or read (e.g., another process holds the lock).
       PermissionError would propagate from write_atomic() or read_with_lock()
       through save() and get_latest_unacknowledged() without being caught.
       The session-start hook would fail, potentially preventing checkpoint
       recovery.
Fix: Add a test that mocks AtomicFileAdapter.write_atomic to raise
     PermissionError and verifies that the caller (CheckpointService) handles
     it gracefully. Document the expected failure behavior in the service
     docstring. Consider whether CheckpointService should catch repository
     exceptions and log them without re-raising.
```

### DEF-006: RECOMMENDED — No Checkpoint Cleanup Mechanism

```
DEF-006: RECOMMENDED
File: src/context_monitoring/infrastructure/adapters/filesystem_checkpoint_repository.py
Issue: next_checkpoint_id() and _load_all_sorted() scan ALL checkpoint files
       on every call. With no cleanup mechanism, checkpoint directories grow
       unboundedly. A long-running project could accumulate hundreds of
       checkpoint files, degrading performance linearly. The BDD scenario
       "cx-003" assumes at most a handful of checkpoints.
Fix (Phase 4+): Add a prune_acknowledged(keep_last: int = 10) method that
     deletes old acknowledged checkpoints and their marker files. Call it
     after acknowledge() if total checkpoint count exceeds a threshold.
     This is Phase 4 work (not blocking QG-2) but should be tracked.
```

### DEF-007: INFORMATIONAL — XML Injection Risk in ResumptionContextGenerator

```
DEF-007: INFORMATIONAL
File: src/context_monitoring/application/services/resumption_context_generator.py
Lines: 108-111
Issue: _serialize_recovery_state only sanitizes keys (spaces -> underscores).
       Keys or values containing XML special characters (<, >, &, ", ') would
       produce malformed XML. Current usage routes ORCHESTRATION.yaml raw text
       as a single string value, which contains colons and indentation but no
       angle brackets. Risk is low with current data, but would increase if the
       format changes to parsed YAML dicts with arbitrary keys.
Fix: Apply XML escaping to both keys and values using html.escape() or
     a minimal custom escaper:
       safe_value = str(value).replace("&", "&amp;").replace("<", "&lt;")
                              .replace(">", "&gt;")
     Keys with special characters are less likely but should also be sanitized.
     No immediate action required (INFORMATIONAL).
```

### DEF-008: INFORMATIONAL — BDD Scenario Naming Mismatch in EN-003

```
DEF-008: INFORMATIONAL
File: projects/.../EN-003-bounded-context-foundation.md
Line: 124
Issue: EN-003 BDD scenario states the acknowledged marker file should be at
       ".jerry/checkpoints/cx-001-checkpoint.json.acknowledged" but the
       implementation creates "cx-001.acknowledged" (without the checkpoint.json
       infix). The test at line 252 of test_filesystem_checkpoint_repository.py
       correctly asserts "cx-001.acknowledged". The entity document has the
       wrong filename. The implementation is correct; the entity doc needs a fix.
Fix: Update the EN-003 BDD scenario to say ".jerry/checkpoints/cx-001.acknowledged".
     No code change required.
```

---

## Resolution Path to PASS

To bring this gate to PASS (>= 0.92), the following must be done before Phase 4 proceeds:

1. **Fix DEF-001** (H-08 violation): Move `staleness_detector.py` to `infrastructure/adapters/` (recommended Option A). Update `bootstrap.py` wiring. Update all test imports.

2. **Fix DEF-002** (large last-line): Fix `_extract_last_nonempty_line` to only return a complete line (one preceded by a newline in the accumulated buffer). Add regression test.

3. **Re-run QG-2 scoring** after fixes are applied. Expected composite: ~0.93–0.95.

RECOMMENDED fixes (DEF-003 through DEF-006) should be tracked for Phase 4 or Phase 5. They do not block Phase 4 start.

---

*Gate result produced by adv-scorer agent | 2026-02-20 | PROJ-004-context-resilience QG-2*
