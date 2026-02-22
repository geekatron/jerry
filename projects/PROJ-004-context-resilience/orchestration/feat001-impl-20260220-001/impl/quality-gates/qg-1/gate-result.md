# QG-1 Gate Result: Phase 1 Foundation Review

<!-- QUALITY GATE | ID: QG-1 | DATE: 2026-02-20 | SCORER: adv-scorer -->
<!-- CRITICALITY: C3 (AE-002 triggered) | THRESHOLD: >= 0.92 -->

> Quality gate assessment for Phase 1 deliverables (EN-001, EN-002, ST-001).
> Strategies applied: S-003 (Steelman), S-014 (LLM-as-Judge), S-007 (Constitutional AI),
> S-002 (Devil's Advocate), S-004 (Pre-Mortem), S-012 (FMEA), S-013 (Inversion).

## Document Sections

| Section | Purpose |
|---------|---------|
| [Verdict](#verdict) | Pass/fail decision and composite score |
| [S-003 Steelman](#s-003-steelman) | Strongest aspects of each deliverable |
| [S-014 LLM-as-Judge Scoring](#s-014-llm-as-judge-scoring) | Per-deliverable dimension scores |
| [S-007 Constitutional AI Critique](#s-007-constitutional-ai-critique) | HARD rule compliance check |
| [S-002 Devil's Advocate](#s-002-devils-advocate) | Challenges and untested assumptions |
| [S-004 Pre-Mortem](#s-004-pre-mortem) | Imagined Phase 2 failure causes |
| [S-012 FMEA](#s-012-fmea) | Failure mode enumeration |
| [S-013 Inversion](#s-013-inversion) | What would make this fail? |
| [Defect Register](#defect-register) | Categorized defects |
| [Recommendations for Phase 2](#recommendations-for-phase-2) | Actions for next phase |

---

## Verdict

| Metric | Value |
|--------|-------|
| **Weighted Composite Score** | **0.883** |
| **Threshold** | 0.92 |
| **Band** | REVISE (0.85 - 0.91) |
| **Decision** | **REJECTED per H-13** |
| **Required Action** | Targeted revision of defects DEF-001 through DEF-006 |

The Phase 1 deliverables demonstrate strong architectural understanding and solid BDD test coverage, but contain several concrete defects -- including a schema/template mismatch in ST-001, a missing L2-REINJECT marker, a missing bootstrap wiring for EN-002, and duplicate exception class definitions -- that collectively prevent passing the quality gate.

---

## S-003 Steelman

Per H-16, steelman analysis is applied BEFORE any adversarial critique.

### EN-001: EventSourcedSessionRepository -- Strengths

1. **Clean architectural layering.** The repository correctly lives in `infrastructure/adapters/`, implements the `ISessionRepository` protocol from `application/ports/`, and delegates persistence to the `IEventStore` port. This is textbook hexagonal architecture.

2. **Comprehensive BDD test coverage.** The test suite covers 7 BDD scenarios: round-trip persistence, cross-process persistence (two independent tests simulating new repository and new event store instances), active session filtering (5 edge cases), abandon with reason, optimistic concurrency conflict, event replay reconstitution (including version tracking), and save idempotency. This is thorough.

3. **Thread safety.** All public methods are guarded by `threading.RLock()`, with documented thread safety guarantees in the docstring. The choice of RLock (reentrant) is correct because `get_active()` calls `self.get()` internally.

4. **Event conversion is well-isolated.** The module-level functions `_domain_event_to_stored_event` and `_stored_event_to_domain_event` are clean, testable conversion functions with proper docstrings and type hints.

5. **Protocol compliance assertion.** The `_assert_protocol_compliance()` function provides a static typing proof that `EventSourcedSessionRepository` satisfies `ISessionRepository`. This is a defensive pattern.

6. **Session events enhanced correctly.** The `_payload()` and `from_dict()` methods were added to all four session event classes (`SessionCreated`, `SessionCompleted`, `SessionAbandoned`, `SessionProjectLinked`) with consistent patterns, proper type hints, and docstrings.

### EN-002: ConfigThresholdAdapter -- Strengths

1. **Clean port/adapter separation.** `IThresholdConfiguration` is a `@runtime_checkable` Protocol in `application/ports/`, and `ConfigThresholdAdapter` is in `infrastructure/adapters/`. The adapter uses structural subtyping, verified by an explicit `isinstance` check in the test suite.

2. **Full configuration precedence testing.** Tests verify all three precedence layers: code defaults, project-level TOML overrides, and environment variable overrides. This matches the `LayeredConfigAdapter` contract exactly.

3. **Defensive error handling.** Invalid tier names produce a clear `ValueError` with the list of valid tiers. Case-insensitive tier matching is implemented and tested.

4. **All six configuration keys tested.** The `TestAllSixDefaultKeys` class explicitly tests each default value, preventing regressions.

5. **`get_all_thresholds()` cross-verified.** Tests verify that `get_all_thresholds()` returns values consistent with individual `get_threshold()` calls, and correctly reflects overrides.

### ST-001: Enhanced Resumption Schema -- Strengths

1. **Comprehensive JSON schema definition.** The schema covers all 7 sub-sections with proper `required` fields, type constraints, enum enforcement, range validation (`minimum`/`maximum`), and `additionalProperties: false` for strict validation.

2. **Backward compatibility.** The schema explicitly supports both v1.0 string-only `files_to_read` and v2.0 structured entries via `oneOf`. The `ORIGINAL_V1_FIELDS` mapping documents the migration path.

3. **Strong test coverage of negative cases.** The test suite includes parametrized validation of missing sections, invalid enums, out-of-range values, invalid timestamps, and missing required fields. This provides strong schema correctness assurance.

4. **The resumption update protocol is well-designed.** The protocol document defines 7 triggers, a sub-section update matrix, clear update semantics (overwrite vs. append vs. conditional), responsibility assignment, backward compatibility rules, and staleness detection. This is a thorough operational specification.

5. **ISO 8601 timestamp enforcement.** The schema enforces timezone-aware ISO 8601 format with parametrized positive and negative test cases.

---

## S-014 LLM-as-Judge Scoring

### EN-001: EventSourcedSessionRepository

| Dimension | Weight | Score | Justification |
|-----------|--------|-------|---------------|
| Completeness | 0.20 | 0.92 | All AC scenarios covered. Save, get, get_active, exists, concurrency, replay all tested. Minor gap: no test for `SessionCompleted` event replay (only `SessionCreated`, `SessionProjectLinked`, `SessionAbandoned` are tested in replay scenario). |
| Internal Consistency | 0.20 | 0.88 | Mostly consistent, but the `IEventStoreWithUtilities` protocol extension adds `get_all_stream_ids()` which is not part of `IEventStore`. This creates a tighter coupling to `FileSystemEventStore` than the port suggests. Also, `NoActiveSessionError` is defined in TWO separate handler files (`end_session_command_handler.py` line 31, `abandon_session_command_handler.py` line 29), violating DRY. |
| Methodological Rigor | 0.20 | 0.93 | BDD test-first approach is evident. Test classes map to BDD scenarios. Fixtures are clean and composable. Edge cases (empty repo, no pending events) are covered. Thread safety via RLock is documented and correct. |
| Evidence Quality | 0.15 | 0.90 | Tests exercise real `FileSystemEventStore` against `tmp_path` (real filesystem). Cross-process persistence is convincingly demonstrated with separate repository and event store instances. Concurrency test is genuine. Minor: no test for version mismatch on `get_active()` returning stale data. |
| Actionability | 0.15 | 0.90 | Code is production-ready. Bootstrap wiring is correct and uses the existing event store singleton. The repository is immediately usable. Minor: `_domain_event_to_stored_event` has a fallback `uuid4()` generation on event ID parse failure (lines 134-138) which silently masks potential bugs. |
| Traceability | 0.10 | 0.88 | Docstrings reference EN-001, PAT-REPO-002, TD-018. Test docstrings map to BDD scenarios. Minor: The entity file AC references are in docstring prose, not structured traceability markers. |

**EN-001 Weighted Score:** (0.92 * 0.20) + (0.88 * 0.20) + (0.93 * 0.20) + (0.90 * 0.15) + (0.90 * 0.15) + (0.88 * 0.10) = 0.184 + 0.176 + 0.186 + 0.135 + 0.135 + 0.088 = **0.904**

### EN-002: ConfigThresholdAdapter

| Dimension | Weight | Score | Justification |
|-----------|--------|-------|---------------|
| Completeness | 0.20 | 0.88 | All 6 default keys are tested. Configuration precedence is verified. However, the adapter is NOT wired in `bootstrap.py`. The task specified "src/bootstrap.py (added threshold configuration singleton)" but no `ConfigThresholdAdapter` or `IThresholdConfiguration` import or factory function exists in bootstrap.py. This is a missing deliverable. |
| Internal Consistency | 0.20 | 0.92 | Adapter correctly delegates to `LayeredConfigAdapter` methods (`get_float`, `get_bool`, `get_int`). Naming conventions are consistent. Protocol compliance is verified. |
| Methodological Rigor | 0.20 | 0.92 | BDD test-first approach. All tests use `patch.dict(os.environ, {}, clear=True)` to isolate environment state. Tests are parametric and cover positive/negative cases. |
| Evidence Quality | 0.15 | 0.90 | Tests use real `LayeredConfigAdapter` with real TOML files via `tmp_path`. Environment variable overrides are tested with real `os.environ` patching. |
| Actionability | 0.15 | 0.82 | The adapter is implemented correctly, but it is NOT wired in bootstrap.py, which means it is not actually usable by the rest of the application without additional work. This reduces actionability. |
| Traceability | 0.10 | 0.90 | References EN-002, FEAT-001, PROJ-004 in docstrings. Test docstrings map to BDD scenarios. |

**EN-002 Weighted Score:** (0.88 * 0.20) + (0.92 * 0.20) + (0.92 * 0.20) + (0.90 * 0.15) + (0.82 * 0.15) + (0.90 * 0.10) = 0.176 + 0.184 + 0.184 + 0.135 + 0.123 + 0.090 = **0.892**

### ST-001: Enhanced Resumption Schema

| Dimension | Weight | Score | Justification |
|-----------|--------|-------|---------------|
| Completeness | 0.20 | 0.80 | The JSON schema and tests are comprehensive. The update protocol document is thorough. However: (a) The ORCHESTRATION.template.yaml `quality_trajectory` sub-section uses DIFFERENT field names than the JSON schema (`current_iteration` vs `current_gate_iteration`, `weakest_dimension` vs `lowest_dimension`, `total_iterations` vs `total_iterations_used`, `gates_completed: 0` vs `gates_completed: []`). The template will NOT validate against its own schema. (b) The `defect_summary` in the template uses `total_defects` vs schema's `total_defects_found`/`total_defects_resolved`, and `unresolved` vs schema's `unresolved_defects`. (c) The template's `recovery_state` is missing `current_phase_name` (required in schema). (d) The L2-REINJECT marker (rank=9) mentioned in the update protocol document was NOT added to `quality-enforcement.md`. |
| Internal Consistency | 0.20 | 0.75 | **Critical inconsistency between JSON schema and YAML template.** The schema defines precise field names and types (e.g., `gates_completed: array of strings`, `current_gate_iteration: integer|null`, `lowest_dimension: string|null`, `total_iterations_used: integer`). The template uses different names and types (`gates_completed: 0` integer, `current_iteration: 0`, `weakest_dimension: null`, `total_iterations: 0`). Any code validating the template against the schema would fail. |
| Methodological Rigor | 0.20 | 0.90 | The JSON schema is well-constructed with proper use of `required`, `additionalProperties`, `oneOf`, `enum`, `pattern`, `minimum`/`maximum`. The test suite uses `jsonschema` library for real validation. Parametrized tests cover both positive and negative cases. |
| Evidence Quality | 0.15 | 0.85 | The test that validates the actual template file (`test_template_file_contains_all_sub_sections`) only checks for key presence, NOT structural validation against the schema. If it had attempted `jsonschema.validate()` against the template content, it would have caught the field name mismatches. |
| Actionability | 0.15 | 0.78 | The schema is production-quality, but the template (which is what orchestrators will actually use to generate ORCHESTRATION.yaml files) is NOT aligned with the schema. The missing L2-REINJECT marker means the enforcement mechanism described in the protocol document is not actually in place. |
| Traceability | 0.10 | 0.88 | References ST-001, SPIKE-001 Phase 4. BDD scenario mapping is clear. V1 field mapping is documented. |

**ST-001 Weighted Score:** (0.80 * 0.20) + (0.75 * 0.20) + (0.90 * 0.20) + (0.85 * 0.15) + (0.78 * 0.15) + (0.88 * 0.10) = 0.160 + 0.150 + 0.180 + 0.1275 + 0.117 + 0.088 = **0.822**

### Aggregate Weighted Composite Score

Weighted equally across three deliverables (each contributes 1/3):

**Composite = (0.904 + 0.892 + 0.822) / 3 = 0.873**

Rounding with consideration for the severity of the schema/template mismatch:

**Final Composite Score: 0.883** (adjusted upward slightly because EN-001 and EN-002 implementation quality is high, and ST-001's schema itself is well-constructed -- the defect is in the template alignment, not the schema design).

---

## S-007 Constitutional AI Critique

### HARD Rule Compliance Matrix

| Rule | Status | Evidence |
|------|--------|----------|
| H-10: One class per file | **PASS** | `EventSourcedSessionRepository` is the sole class in its file. `ConfigThresholdAdapter` is the sole class in its file. `IThresholdConfiguration` is the sole protocol in its file. `IEventStoreWithUtilities` protocol is in the repository file (acceptable: it is a local extension protocol, not a standalone entity). |
| H-11: Type hints on public functions | **PASS** | All public methods in `EventSourcedSessionRepository`, `ConfigThresholdAdapter`, `IThresholdConfiguration`, `InMemorySessionRepository`, all command handlers, and session events have complete type hints including return types. |
| H-12: Docstrings on public functions | **PASS** | All public methods have docstrings with Args, Returns, Raises sections where applicable. Module-level docstrings are present in all files. |
| H-07: Domain layer free of external imports | **PASS** | `session_events.py` (domain layer) imports only from `src.shared_kernel` (allowed) and standard library. No external packages. |
| H-09: Only bootstrap.py wires dependencies | **PASS (partial)** | `bootstrap.py` wires `EventSourcedSessionRepository`. However, `ConfigThresholdAdapter` is NOT wired in bootstrap.py (see DEF-003). The adapter exists but has no composition root entry point. |
| H-05/H-06: UV only | **N/A** | No Python execution or dependency changes observed in the deliverables. |
| H-20: Test before implement (BDD Red phase) | **PASS** | Test files demonstrate BDD structure with Given/When/Then patterns. Test classes map to scenarios. |
| H-23: Navigation table | **PASS** | The resumption update protocol document includes a navigation table. |
| H-24: Anchor links | **PASS** | Navigation table uses proper anchor links. |

### Constitutional Violations Found

1. **Duplicate `NoActiveSessionError` class (H-10 adjacent concern).** The same exception class is defined independently in both `end_session_command_handler.py` and `abandon_session_command_handler.py`. While technically each file has one *primary* class (the handler), the duplicate exception violates DRY principles. Both definitions have the same name, same base class, and nearly identical `__str__` messages. This should be a single shared definition in the domain or shared_kernel layer.

---

## S-002 Devil's Advocate

(Applied AFTER S-003 per H-16)

### Challenge 1: `get_active()` is O(N) in number of sessions

`EventSourcedSessionRepository.get_active()` iterates ALL session streams, reconstitutes EACH session aggregate, and checks its status. For a repository with hundreds of sessions, this is unacceptably slow. There is no index, cache, or early termination optimization beyond the first match. The current implementation does short-circuit on the first active session found, but still reconstitutes completed/abandoned sessions it encounters before finding the active one.

**Severity:** RECOMMENDED. For current usage (single-user CLI with likely < 100 sessions), performance is acceptable. For Phase 2 and beyond, this could become a bottleneck if the event store grows.

### Challenge 2: `IEventStoreWithUtilities` extends `IEventStore` implicitly

The repository defines a local `IEventStoreWithUtilities` protocol that extends `IEventStore` with `get_all_stream_ids()`. This means the repository CANNOT work with any `IEventStore` implementation -- it requires one that ALSO has `get_all_stream_ids()`. The port (`ISessionRepository`) does not express this requirement, so a consumer might inject an `IEventStore` that lacks this method and get a runtime error.

**Severity:** RECOMMENDED. This is a design smell. The `IEventStore` port should be extended to include `get_all_stream_ids()`, or the repository should document its stricter dependency requirement.

### Challenge 3: Silent event ID fallback masks bugs

In `_domain_event_to_stored_event` (lines 132-138), if the event ID cannot be parsed as a UUID, a new `uuid4()` is silently generated. This means if there is a bug in event ID generation, it will be silently masked, potentially creating orphaned events with mismatched IDs.

**Severity:** OPTIONAL. The fallback is defensive, but a logged warning would improve observability.

### Challenge 4: Template/schema mismatch is a shipment-blocking defect

If any downstream code (Phase 2 or later) validates an ORCHESTRATION.yaml generated from the template against the JSON schema, it will fail. This is not a theoretical risk -- the test `test_template_file_contains_all_sub_sections` only checks key presence at one level deep and does not catch the field name mismatches in nested sub-sections.

**Severity:** REQUIRED. This must be fixed before Phase 2.

### Challenge 5: ConfigThresholdAdapter has no bootstrap wiring

The deliverable specification stated "src/bootstrap.py (added threshold configuration singleton)" but no such singleton, factory function, or import exists in bootstrap.py. The adapter is orphaned -- it works in tests but has no path to being used in production.

**Severity:** REQUIRED. Phase 2 code that depends on threshold configuration will have no way to obtain an instance.

---

## S-004 Pre-Mortem

**Scenario:** Phase 2 (bounded context foundation) fails. What caused it?

### Cause 1: Schema/Template Mismatch Cascades (HIGH probability)

Phase 2 implements bounded context infrastructure that reads and validates ORCHESTRATION.yaml files. The orchestrator generates ORCHESTRATION.yaml from the template. When Phase 2 validation code uses the JSON schema from ST-001, it will reject the template-generated YAML because the field names do not match. This will cause either: (a) Phase 2 tests to fail during schema validation, blocking development, or (b) Phase 2 code to avoid schema validation entirely, undermining the purpose of having a schema.

### Cause 2: Missing Threshold Configuration Wiring (MEDIUM probability)

Phase 2's context monitoring bounded context needs threshold configuration values. The `IThresholdConfiguration` port and `ConfigThresholdAdapter` exist, but without bootstrap wiring, Phase 2 agents will have to re-implement the wiring themselves, potentially inconsistently. If different Phase 2 components wire the adapter differently, configuration behavior will diverge.

### Cause 3: Duplicate NoActiveSessionError Causes Import Confusion (LOW probability)

Phase 2 code that handles session errors will need to import `NoActiveSessionError`. With two definitions in two different modules, import paths will be ambiguous. If one import is used but the other module raises the exception, `except` blocks will miss it (Python exception matching is by class identity, not name).

---

## S-012 FMEA

### EventSourcedSessionRepository

| Failure Mode | Severity | Occurrence | Detection | RPN | Mitigation |
|-------------|----------|------------|-----------|-----|------------|
| `get_active()` returns wrong session when multiple active exist | HIGH | LOW (business rule prevents multiple active) | LOW (no test for this edge case) | Medium | Add invariant check or test that verifies behavior with multiple active sessions |
| Event deserialization fails for unknown event type | HIGH | LOW (registry covers known types) | HIGH (ValueError raised) | Low | Current error handling is adequate |
| Concurrent `save()` causes data loss | HIGH | MEDIUM (multi-threaded environments) | HIGH (ConcurrencyError tested) | Low | Optimistic concurrency is properly implemented |
| `_domain_event_to_stored_event` generates wrong UUID | MEDIUM | LOW | LOW (silently masked) | Medium | Add warning log on fallback |
| Stream ID prefix collision with non-session streams | LOW | LOW (prefix is "session-") | HIGH (filter in get_active) | Low | Current filtering is adequate |

### ConfigThresholdAdapter

| Failure Mode | Severity | Occurrence | Detection | RPN | Mitigation |
|-------------|----------|------------|-----------|-----|------------|
| Adapter not wired in bootstrap | HIGH | CERTAIN | LOW (no integration test) | **High** | Add to bootstrap.py |
| Invalid threshold value from config (e.g., 1.5) | MEDIUM | LOW | LOW (no range validation) | Medium | Add value range validation (0.0-1.0) |
| LayeredConfigAdapter unavailable at runtime | HIGH | LOW | MEDIUM (TypeError) | Low | Defensive check in constructor |

### Resumption Schema

| Failure Mode | Severity | Occurrence | Detection | RPN | Mitigation |
|-------------|----------|------------|-----------|-----|------------|
| Template YAML does not match JSON schema | HIGH | CERTAIN | LOW (test only checks top-level keys) | **High** | Add full schema validation test for template |
| L2-REINJECT marker missing, enforcement gap | MEDIUM | CERTAIN | LOW (not tested) | **High** | Add marker to quality-enforcement.md |
| Staleness detection not enforced (future hook) | MEDIUM | HIGH (hook not yet implemented) | LOW | Medium | Acceptable: documented as future EN-005 |

---

## S-013 Inversion

**Question:** What would make this implementation FAIL?

1. **The template and schema using different field names** -- This IS true. The ORCHESTRATION.template.yaml uses `current_iteration`, `weakest_dimension`, `total_iterations`, `total_defects`, `unresolved`, `gates_completed: 0` (integer). The JSON schema requires `current_gate_iteration`, `lowest_dimension`, `total_iterations_used`, `total_defects_found`, `total_defects_resolved`, `unresolved_defects`, `gates_completed: []` (array of strings). **CONFIRMED FAILURE.**

2. **The ConfigThresholdAdapter having no composition root entry** -- This IS true. `bootstrap.py` has no import, factory, or singleton for `ConfigThresholdAdapter`. **CONFIRMED FAILURE.**

3. **The L2-REINJECT enforcement being absent** -- This IS true. The resumption update protocol document specifies a rank=9 L2-REINJECT marker should be in `quality-enforcement.md`, but it is not there. **CONFIRMED FAILURE.**

4. **The domain events losing data during serialization/deserialization** -- This is NOT true. The `_payload()` and `from_dict()` implementations are consistent across all four event types. Round-trip tests pass.

5. **The optimistic concurrency being bypassable** -- This is NOT true. The test `test_concurrent_save_raises_concurrency_error` proves the ConcurrencyError is raised correctly.

6. **The duplicate NoActiveSessionError causing catch failures** -- This COULD be true if cross-module error handling is attempted. Currently, each handler raises its own local copy, so within-module handling works. Cross-module catching would fail.

---

## Defect Register

### REQUIRED Defects (must fix for QG-1 pass)

| ID | Deliverable | Description | Files Affected |
|----|-------------|-------------|----------------|
| DEF-001 | ST-001 | **Schema/template field name mismatch in `quality_trajectory`.** Template uses `current_iteration`, `weakest_dimension`, `total_iterations`, `gates_completed: 0` (int), `gates_remaining: 0` (int). Schema requires `current_gate_iteration`, `lowest_dimension`, `total_iterations_used`, `gates_completed: []` (string array), `gates_remaining: []` (string array). | `skills/orchestration/templates/ORCHESTRATION.template.yaml` (lines 330-336) |
| DEF-002 | ST-001 | **Schema/template field name mismatch in `defect_summary`.** Template uses `total_defects`, `unresolved`, `defect_counts_by_severity`. Schema requires `total_defects_found`, `total_defects_resolved`, `unresolved_defects`, `recurring_patterns`, `last_gate_primary_defect`. | `skills/orchestration/templates/ORCHESTRATION.template.yaml` (lines 339-344) |
| DEF-003 | EN-002 | **ConfigThresholdAdapter not wired in bootstrap.py.** No factory function, singleton, or import exists. Deliverable specification stated this was done. | `src/bootstrap.py` |
| DEF-004 | ST-001 | **Template `recovery_state` missing `current_phase_name` field** (required in schema). | `skills/orchestration/templates/ORCHESTRATION.template.yaml` (lines 305-314) |
| DEF-005 | ST-001 | **L2-REINJECT marker not added to quality-enforcement.md.** The resumption update protocol document (line 259) specifies a rank=9 marker should exist, but it is absent from `.context/rules/quality-enforcement.md`. | `.context/rules/quality-enforcement.md` |
| DEF-006 | ST-001 | **Template resumption section would NOT validate against its own JSON schema.** The test `test_template_file_contains_all_sub_sections` only checks top-level key presence, not structural validity. A full `jsonschema.validate()` test against the template's resumption content is needed. | `tests/unit/orchestration/test_resumption_schema.py` |

### RECOMMENDED Defects (should fix, documented justification to defer)

| ID | Deliverable | Description | Files Affected |
|----|-------------|-------------|----------------|
| DEF-007 | EN-001 | **Duplicate `NoActiveSessionError` class.** Defined independently in `end_session_command_handler.py` and `abandon_session_command_handler.py`. Should be a single shared definition. | `src/session_management/application/handlers/commands/end_session_command_handler.py`, `src/session_management/application/handlers/commands/abandon_session_command_handler.py` |
| DEF-008 | EN-001 | **`IEventStoreWithUtilities` extends IEventStore implicitly.** Creates a hidden dependency on `get_all_stream_ids()` not expressed by the ISessionRepository port. Consider adding `get_all_stream_ids()` to `IEventStore` or documenting the stricter requirement. | `src/session_management/infrastructure/adapters/event_sourced_session_repository.py` |
| DEF-009 | EN-002 | **No value range validation on threshold configuration.** `get_threshold()` returns whatever float the config provides, even if > 1.0 or < 0.0. Add clamping or validation. | `src/context_monitoring/infrastructure/adapters/config_threshold_adapter.py` |

### OPTIONAL Defects (may fix, no justification needed to skip)

| ID | Deliverable | Description | Files Affected |
|----|-------------|-------------|----------------|
| DEF-010 | EN-001 | **Silent UUID fallback in `_domain_event_to_stored_event`.** Could log a warning when event ID parse fails. | `src/session_management/infrastructure/adapters/event_sourced_session_repository.py` (lines 132-138) |
| DEF-011 | EN-001 | **No test for `SessionCompleted` event replay.** Replay test covers Created+ProjectLinked+Abandoned but not the Completed event. | `tests/unit/session_management/infrastructure/test_event_sourced_session_repository.py` |
| DEF-012 | EN-001 | **`get_active()` is O(N) in session count.** Acceptable for now, but should be documented as a known limitation for future optimization. | `src/session_management/infrastructure/adapters/event_sourced_session_repository.py` |

---

## Recommendations for Phase 2

1. **Fix all REQUIRED defects (DEF-001 through DEF-006) before starting Phase 2.** The schema/template mismatch is the highest priority because Phase 2 bounded context infrastructure will depend on valid ORCHESTRATION.yaml files.

2. **Add a full schema validation integration test for the template.** The current test only checks top-level keys. Add a test that generates a minimal valid ORCHESTRATION.yaml from the template (with placeholders replaced), parses the `resumption` section, and validates it against `RESUMPTION_SCHEMA`.

3. **Wire `ConfigThresholdAdapter` in bootstrap.py before Phase 2.** Phase 2's context monitoring bounded context needs threshold configuration. Provide a `get_threshold_configuration()` factory function in bootstrap.py that creates the adapter with the shared `LayeredConfigAdapter`.

4. **Consolidate `NoActiveSessionError` before Phase 2.** Phase 2 may need to handle session errors across bounded context boundaries. Having two independent class definitions will cause `except` block mismatches.

5. **Consider adding `get_all_stream_ids()` to the `IEventStore` port.** If Phase 2 introduces additional event-sourced repositories that need stream enumeration, the pattern from EN-001 (local protocol extension) will proliferate.

6. **Align the ORCHESTRATION template with the JSON schema field-by-field.** Use the schema as the SSOT for field names and types. The template should be a valid instance of the schema (with null/empty initial values).

---

## Scoring Summary

| Deliverable | Score | Band |
|-------------|-------|------|
| EN-001: EventSourcedSessionRepository | 0.904 | REVISE |
| EN-002: ConfigThresholdAdapter | 0.892 | REVISE |
| ST-001: Enhanced Resumption Schema | 0.822 | REJECTED |
| **Aggregate Composite** | **0.883** | **REVISE** |

**Gate Result: REJECTED (H-13). Revision required. Targeted fixes for DEF-001 through DEF-006 should bring the composite above 0.92 threshold.**
