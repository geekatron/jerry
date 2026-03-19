# Quality Score Report: Requirements Specification — Configurable Output Base Path

## L0 Executive Summary

**Score:** 0.857/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.78)

**One-line assessment:** The requirements document is structurally thorough and well-traced, but two concrete internal contradictions — a LayeredConfigAdapter/port naming conflict in REQ-OBP-003b vs. REQ-OBP-003d and a SHALL/Should mismatch on REQ-OBP-002d — must be resolved before eng-backend can implement without ambiguity; these plus minor completeness gaps on whitespace-only paths and directory-creation behavior keep the composite below the 0.93 threshold.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-021-output-base-path/orchestration/output-basepath-20260318-001/nse/phase-nse-1/requirements.md`
- **Deliverable Type:** Research / Formal Requirements Specification
- **Criticality Level:** C3
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Threshold:** 0.93 (user-specified for this engagement; base H-13 threshold is 0.92)
- **Scored:** 2026-03-18
- **C3 Strategies Applied:** S-007 (Constitutional AI Critique), S-002 (Devil's Advocate), S-004 (Pre-Mortem), S-012 (FMEA), S-013 (Inversion)
- **Prior Score:** N/A (first score)

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.857 |
| **Threshold** | 0.93 |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No (no adv-executor report provided) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.88 | 0.176 | All 5 ACs decomposed; 24-case edge catalog; 2 minor gaps (whitespace-only path, directory-creation on missing project dir) |
| Internal Consistency | 0.20 | 0.78 | 0.156 | Two genuine contradictions: REQ-OBP-003d names concrete class where 003b requires port; REQ-OBP-002d uses SHALL with Should priority |
| Methodological Rigor | 0.20 | 0.87 | 0.174 | ADIT V-Methods on all requirements; 4 oracle sets; OR-001 weaker than REQ-OBP-001c; import-analysis oracle absent |
| Evidence Quality | 0.15 | 0.87 | 0.1305 | 9 specific file/function references; env-var mapping contract cited; 6 YAML agents named without full paths |
| Actionability | 0.15 | 0.86 | 0.129 | Allocation matrix with exact file paths; "coerced" undefined in REQ-OBP-001c; str→Path conversion inference required |
| Traceability | 0.10 | 0.91 | 0.091 | Full ASCII traceability tree; AC-3c Won't explicitly traced; H-07 not formally registered as parent constraint |
| **TOTAL** | **1.00** | | **0.857** | |

---

## Detailed Dimension Analysis

### Completeness (0.88/1.00)

**Evidence:**
All five acceptance criteria from GH #192 are decomposed into primary requirements and sub-requirements: AC-1 → REQ-OBP-001 + 001a–001e (5 sub-reqs); AC-2 → REQ-OBP-002 + 002a–002d (4 sub-reqs); AC-3 → REQ-OBP-003 + 003a–003g + REQ-OBP-004 + 004a–004e with formal 3-part AC split (AC-3a/b/c); AC-4 → REQ-OBP-005 + 005a–005b; AC-5 → REQ-OBP-006 + 006a–006b. Cross-cutting requirements (REQ-OBP-007 bootstrap wiring, REQ-OBP-008 coverage) are included. The 24-entry edge case catalog covers null bytes, path traversal, TOML decode failure, missing config file, double-trailing-slash prevention, empty-string JERRY_PROJECT, and env var override. The AC-3 known gap is formally split into three sub-concerns with explicit Won't classification for AC-3c (runtime interpolation).

**Gaps:**
1. No requirement or edge case addresses a whitespace-only value (e.g., `output.base_path = "   "`). The resolver's non-empty check (`not None and != ""`) would pass this value and produce `"   /"` — a semantically invalid path. This is an unaddressed input class.
2. REQ-OBP-001b specifies that `--scope project` writes to `projects/${JERRY_PROJECT}/.jerry/config.toml` but does not specify whether the `.jerry/` directory must be created if absent. An implementer would need to decide this independently — a real ambiguity gap.
3. The AC-3 Won't is well-documented but there is no explicit requirement that the follow-up GitHub Issue be created with a specific title or linked to AC-3c in the issue body. The requirement says "SHALL be logged before merge" — sufficient for current purposes.

**Improvement Path:**
Add EC-025: whitespace-only `output.base_path` — define expected behavior (trim and treat as empty, or reject). Extend REQ-OBP-001b with a sub-requirement specifying directory-creation behavior for missing project config directories.

---

### Internal Consistency (0.78/1.00)

**Evidence:**
The trailing-slash guarantee (REQ-OBP-003a) is consistently referenced by 003e, 003f, 006a, and the resolver description — centralized rather than restated, which prevents contradiction. The non-empty check definition (not None, not "") is consistently applied across EC-005, EC-013, EC-014, OR-104, and REQ-OBP-003d.

**Gaps (genuine contradictions):**

**Contradiction 1 (Major):** REQ-OBP-003b: "OutputResolver SHALL import only from the configuration domain layer and the `IConfigurationProvider` port. `OutputResolver` SHALL NOT import from `LayeredConfigAdapter` directly." REQ-OBP-003d: "The `OutputResolver.resolve()` method SHALL check `LayeredConfigAdapter.get("output.base_path")` first." A developer reading both requirements literally would be unable to comply with both simultaneously: 003b forbids importing LayeredConfigAdapter; 003d instructs calling `LayeredConfigAdapter.get()`. The correct formulation for 003d should reference `IConfigurationProvider.get("output.base_path")` (the port), not the concrete adapter class. This is a concrete contradiction that will surface at implementation time.

**Contradiction 2 (Moderate):** REQ-OBP-002d carries `Priority: Should` in the MoSCoW table but the normative text reads "SHALL output a JSON object containing `key`, `value`, and `source` fields." A Should-priority item should use SHOULD language. As written, a developer following the normative SHALL would treat `--json` as mandatory even though the MoSCoW classification marks it as optional. During verification, an nse-verification agent checking compliance would find an ambiguous obligation level for this requirement.

**Minor inconsistency:** The Requirements Quality Checklist self-assessment claims requirements are "Implementation-Free" then immediately qualifies that REQ-OBP-003b specifies a file path — the justification offered (H-07 structural constraint) is reasonable but creates a minor self-assessment inconsistency.

**Improvement Path:**
- REQ-OBP-003d: Replace "`LayeredConfigAdapter.get("output.base_path")`" with "`IConfigurationProvider.get("output.base_path")`".
- REQ-OBP-002d: Change normative text from "SHALL output" to "SHOULD output" to align with the Should priority classification.

---

### Methodological Rigor (0.87/1.00)

**Evidence:**
Every primary requirement has an explicit V-Method field with ADIT classification (Test, Inspection, or combined). Sub-requirements inherit the V-Method through their parent context. Four oracle sets provide unambiguous input/output pairs: Oracle Set 1 (5 CLI round-trip entries with exact command sequences, expected stdout text, and exit codes), Oracle Set 2 (7 resolver state entries with exact return value strings), Oracle Set 3 (5 YAML inspection assertions), Oracle Set 4 (4 value object construction assertions). NASA-HDBK-1009A is cited and its 7 quality criteria are assessed. The risk implications table applies likelihood-consequence-RPN methodology consistent with FMEA (S-012). The allocation matrix provides component-level assignment enabling inspection-based verification.

**Gaps:**

**Gap 1 (Oracle weaker than requirement):** REQ-OBP-001c requires the command to print four fields: "key, coerced value, scope, and target config file path." Oracle OR-001 checks only that stdout "contains key and value" — two of the four specified fields. An implementation printing key+value but omitting scope and config path would pass OR-001 but fail REQ-OBP-001c. The oracle should be strengthened to assert all four fields.

**Gap 2 (Missing import oracle):** REQ-OBP-003b is verified by "Inspection (I) - import analysis" but no specific tool, command, or criterion is given for this inspection. The risk table mentions "H-07 import check in eng-reviewer phase; pre-tool AST enforcement" but does not provide the concrete `grep` or AST command. Without this, the inspection criterion is declared but not operationalized.

**Gap 3 (Minor oracle weakness):** Oracle OR-203 checks `Contains "${JERRY_OUTPUT_BASE}test-specs/"` — this string would match even if the YAML value were `${JERRY_OUTPUT_BASE}/test-specs/` (with an extra slash that REQ-OBP-004b explicitly prohibits). A tighter oracle would check for the absence of `${JERRY_OUTPUT_BASE}/` (with trailing slash before the subdirectory).

**Improvement Path:**
- Expand OR-001 to assert all four fields from REQ-OBP-001c: key, coerced value, scope, config file path.
- Add a concrete inspection command for REQ-OBP-003b (e.g., `grep -r "LayeredConfigAdapter" src/configuration/application/ --include="*.py"` must return empty).
- Tighten OR-203 to also assert absence of `${JERRY_OUTPUT_BASE}/` pattern.

---

### Evidence Quality (0.87/1.00)

**Evidence:**
Nine specific, locatable file references are given: `layered_config_adapter.py`, `env_config_adapter.py`, `bootstrap.py`, `adapter.py`, `agent-governance-v1.schema.json`, plus two new files to be created (`output_resolver.py`, `output_base_path.py`). Four specific functions are named with their current behavior described: `LayeredConfigAdapter.get()`, `cmd_config_set`, `cmd_config_get`, `get_project_data_path()`, `EnvConfigAdapter._env_to_config_key()`. The env variable naming convention (double-underscore: `output.base_path` → `JERRY_OUTPUT__BASE_PATH`) references the actual adapter contract. The existing layered precedence order (env > project > root > defaults) is stated as already implemented. The TOML error handling behavior (`_load_toml()` catches `TOMLDecodeError`) reflects knowledge of the actual implementation. Six specific governance YAML agents are named. Constitutional rules H-07, H-20, H-34 are cited with accuracy. S-007 constitutional review finds no governance violations.

**Gaps:**
1. The six governance YAML files are listed by agent name (`uc-author`, `uc-slicer`, etc.) but without full repository paths. A reviewer cannot confirm the file list or verify the scope of changes without knowing the directory containing these files. Full paths would strengthen the evidence.
2. The claim "No such framework currently exists" (for the agent invocation interpolation mechanism) is a factual assertion about codebase state that is not referenced to any file, function, or audit artifact. This is an unsupported negative claim.

**Improvement Path:**
- Add full paths for all six governance YAML files in REQ-OBP-004a and the allocation matrix.
- Add Evidence Gate 2 citation or a specific codebase reference (e.g., `grep -r "output.location" src/ --include="*.py"`) to substantiate the claim that no invocation interpolation framework exists.

---

### Actionability (0.86/1.00)

**Evidence:**
The allocation matrix provides exact file paths and layers for every requirement. New files are named with full paths (REQ-OBP-003b: `src/configuration/application/services/output_resolver.py`; REQ-OBP-003c: `src/configuration/domain/value_objects/output_base_path.py`). The `resolve() -> str` method signature is complete. The four-step fallback chain is ordered and numbered. Bootstrap wiring is specified at the function level (`get_project_data_path()` must delegate to `OutputResolver.resolve()`). The Won't classification for AC-3c explicitly bounds what eng-backend should not build and requires a follow-up issue before merge. Test oracles provide sufficient specificity for nse-verification to write BDD scenarios directly.

**Gaps:**

**Gap 1 (Type conversion ambiguity):** REQ-OBP-005b requires `get_project_data_path()` to "maintain the same `Path | None` return type contract" while delegating to `OutputResolver.resolve()` which returns `str`. How the `str` is converted to `Path` — specifically whether `Path(resolver.resolve())` is called, whether it must be wrapped in `Optional`, or whether `None` is still returned in any case — is not specified. An implementer must infer this.

**Gap 2 ("Coerced" undefined):** REQ-OBP-001c requires the command to print "the key, coerced value, scope, and target config file path." The word "coerced" has no definition in the document. Does it mean TOML-type coercion (converting string to Path type)? Path normalization? Type stringification? This is undefined terminology that will generate implementer questions.

**Gap 3 (Path traversal dependency):** EC-010 and REQ-OBP-003c note that path traversal (`..` segments) is "a security concern requiring eng-security review" but the VO does not validate or reject it. This creates an open dependency: eng-backend cannot finalize the VO implementation until eng-security determines the policy. The requirement does not specify a default behavior in the absence of that review (reject `..`? permit? normalize?).

**Improvement Path:**
- Add to REQ-OBP-005b: specify that the implementation returns `Path(resolver.resolve())` when not None, making the type conversion explicit.
- Define "coerced value" in REQ-OBP-001c or replace with the specific fields that must appear.
- Add a provisional policy statement for `..` segments pending eng-security review: either "VO permits `..` pending review" or "VO rejects `..` pending review" — either stance removes the implementer ambiguity.

---

### Traceability (0.91/1.00)

**Evidence:**
The L2 traceability tree provides a complete ASCII chain from GH #192 through each AC through requirements through implementation components through Evidence Gates. Every primary requirement has a `Parent` field. AC-3c (runtime interpolation, Won't) is explicitly included in the traceability tree with `[DEFERRED]` annotation and "Follow-up GitHub Issue required." The AC-3 Boundary Analysis section formalizes the three sub-concerns in a table with status and requirement columns. The MoSCoW summary lists the Won't as a separate entry with the "Won't (this release)" classification. REQ-OBP-007 and REQ-OBP-008 are flagged as "Cross-cutting" with multiple parents.

**Gaps:**
1. Sub-requirements trace to their parent requirement (e.g., REQ-OBP-001a → REQ-OBP-001) but not directly to the AC or stakeholder need. An auditor tracing REQ-OBP-001a to GH #192 must traverse two levels. This is minor but adds indirection in formal compliance audits.
2. REQ-OBP-003b cites H-07 in its rationale but H-07 is not registered as a formal parent in the `Parent` field. If the requirement is driven equally by the AC and by the governance rule, both should appear as parents. As written, H-07 is informational context rather than a formal traceability link.

**Improvement Path:**
- Consider adding `Source AC` as a column to sub-requirement tables for direct AC-level traceability.
- In REQ-OBP-003b, add H-07 to the Parent field alongside REQ-OBP-003 to formalize the governance constraint link.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.78 | 0.88+ | Fix REQ-OBP-003d: replace `LayeredConfigAdapter.get()` with `IConfigurationProvider.get()` to resolve the port vs. concrete class contradiction with REQ-OBP-003b |
| 2 | Internal Consistency | 0.78 | 0.88+ | Fix REQ-OBP-002d: change normative "SHALL output" to "SHOULD output" to align verb modality with Should MoSCoW classification |
| 3 | Completeness | 0.88 | 0.92+ | Add EC-025 for whitespace-only `output.base_path` values; define trim-and-treat-as-empty or reject behavior |
| 4 | Actionability | 0.86 | 0.90+ | Define "coerced value" in REQ-OBP-001c or replace the term with the specific four fields that must appear in stdout |
| 5 | Actionability | 0.86 | 0.90+ | Extend REQ-OBP-005b to specify the str→Path conversion: state that implementation returns `Path(resolver.resolve())` |
| 6 | Completeness | 0.88 | 0.92+ | Add a sub-requirement to REQ-OBP-001b specifying whether the `.jerry/` directory is created when absent |
| 7 | Methodological Rigor | 0.87 | 0.91+ | Expand Oracle OR-001 to assert all four fields from REQ-OBP-001c (key, coerced value, scope, config file path) |
| 8 | Methodological Rigor | 0.87 | 0.91+ | Add a concrete import-check command for REQ-OBP-003b verification (e.g., grep command with expected empty result) |
| 9 | Evidence Quality | 0.87 | 0.91+ | Add full repository paths for all six governance YAML files in REQ-OBP-004a and the allocation matrix |
| 10 | Actionability | 0.86 | 0.90+ | Add a provisional policy for `..` path segments in OutputBasePath VO pending eng-security review |

---

## Leniency Bias Check

- [x] Each dimension scored independently before composite was computed
- [x] Evidence documented for each score with specific requirement IDs, section names, and quoted text
- [x] Uncertain scores resolved downward (Internal Consistency: considered 0.80, resolved to 0.78 given two genuine contradictions; Completeness: considered 0.90, resolved to 0.88 given 2 real implementer gaps)
- [x] C3 calibration considered — this is not a first draft (it is a formally produced nse-1 output with structured sections, stakeholder needs, allocation matrix, risk table, and oracles), so the 0.65-0.80 first-draft anchor does not apply; strong first-pass NSE output typically scores 0.82-0.88; this result is consistent
- [x] No dimension scored above 0.95 — highest is Traceability at 0.91, justified by the explicit AC-3c tracing
- [x] S-002 (Devil's Advocate) applied: actively sought contradictions and requirement gaps rather than accepting document self-assessment at face value
- [x] S-013 (Inversion) applied to oracles: asked "what implementation would pass the oracle but fail the requirement?" — identified OR-001 gap
- [x] S-007 (Constitutional AI Critique) applied: verified H-07, H-20, H-34 citations are accurate; found no governance violations
- [x] S-004 (Pre-Mortem) applied: the most likely implementation failure is a developer reading REQ-OBP-003d and importing LayeredConfigAdapter directly, creating an H-07 violation — this confirms the Priority 1 recommendation

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.857
threshold: 0.93
weakest_dimension: Internal Consistency
weakest_score: 0.78
critical_findings_count: 0
iteration: 1
improvement_recommendations:
  - "Fix REQ-OBP-003d: replace LayeredConfigAdapter.get() with IConfigurationProvider.get() — resolves port/concrete contradiction with REQ-OBP-003b"
  - "Fix REQ-OBP-002d: change SHALL to SHOULD in normative text to align with Should MoSCoW priority"
  - "Add EC-025: define behavior for whitespace-only output.base_path values"
  - "Define 'coerced value' in REQ-OBP-001c or enumerate the four required stdout fields"
  - "Extend REQ-OBP-005b to specify str→Path conversion (Path(resolver.resolve()))"
  - "Add sub-requirement to REQ-OBP-001b for .jerry/ directory creation when absent"
  - "Expand Oracle OR-001 to assert all four fields from REQ-OBP-001c"
  - "Add concrete import-check command for REQ-OBP-003b (grep command, expected empty result)"
  - "Add full repo paths for all 6 governance YAML files in REQ-OBP-004a and allocation matrix"
  - "Add provisional path traversal policy for OutputBasePath VO pending eng-security review"
```

---

*Scored by adv-scorer v1.0.0*
*Strategy: S-014 (LLM-as-Judge) with C3 strategies S-007, S-002, S-004, S-012, S-013*
*SSOT: `.context/rules/quality-enforcement.md`*
*Date: 2026-03-18*
