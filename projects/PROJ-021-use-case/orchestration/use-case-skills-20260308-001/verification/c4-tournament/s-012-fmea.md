# Strategy Execution Report: FMEA (Failure Mode and Effects Analysis)

## Execution Context

- **Strategy:** S-012 (FMEA -- Failure Mode and Effects Analysis)
- **Template:** `.context/templates/adversarial/s-012-fmea.md`
- **Deliverable:** All 6 agent pairs + 3 SKILL.md files + 2 JSON schemas across `skills/use-case/`, `skills/test-spec/`, `skills/contract-design/`, and `docs/schemas/`
- **Executed:** 2026-03-12T00:00:00Z
- **Criticality:** C4
- **H-16 Compliance:** S-003 Steelman applied in prior tournament phases (confirmed)
- **Elements Analyzed:** 18 | **Failure Modes Identified:** 34 | **Total RPN:** 4,858

---

## Summary

The six-agent pipeline (uc-author -> uc-slicer -> tspec-generator -> tspec-analyst -> cd-generator -> cd-validator) was decomposed into 18 analyzable elements and subjected to systematic bottom-up FMEA across 5 failure mode lenses (Missing, Incorrect, Ambiguous, Inconsistent, Insufficient). Thirty-four failure modes were identified with a combined total RPN of 4,858. Seven findings are Critical (RPN >= 200), eighteen are Major, and nine are Minor. The highest-risk area is the **uc-slicer -> cd-generator handoff boundary**: the interactions block produced by uc-slicer Activity 5 is the sole input path to contract generation, yet no automated schema enforcement gate exists for the 7-field interaction completeness requirement at that boundary. The second highest-risk area is the **tspec-generator input validation gate**: the two-layer validation approach is LLM-evaluated for semantic checks, making false-negative rejections possible when detail_level flags are set incorrectly. The pipeline is **conditionally accepted** pending mandatory corrective actions for the seven Critical findings.

---

## Element Inventory

The pipeline was decomposed into 18 elements across 6 agents:

| EL# | Agent | Element | Description |
|-----|-------|---------|-------------|
| EL-01 | uc-author | Rejection Artifact Protocol | Logic to read, validate, and consume `{artifact_path}-rejection.yaml` |
| EL-02 | uc-author | Cockburn 12-Step Process | Steps 1-12 progression and detail level gate enforcement |
| EL-03 | uc-author | Schema Post-Creation Verification | allOf constraint verification after artifact write |
| EL-04 | uc-slicer | Step 1 Input Validation Gate | Rejection of artifacts below ESSENTIAL_OUTLINE |
| EL-05 | uc-slicer | Rejection Artifact Write Protocol | Construction and persistence of rejection YAML |
| EL-06 | uc-slicer | Activity 5 Interaction Sequence Production | Deriving `$.interactions[]` for downstream consumption |
| EL-07 | uc-slicer | INVEST Criteria Verification | Per-slice INVEST check before SCOPED -> PREPARED transition |
| EL-08 | tspec-generator | Clark Transformation Step 4 (Happy Path) | basic_flow -> single Scenario mapping |
| EL-09 | tspec-generator | Clark Transformation Step 6 (Extensions) | extension -> error/success/rejoin Scenario by outcome type |
| EL-10 | tspec-generator | Input Validation Layer 2 (Semantic) | Agent-side rejection of semantic violations |
| EL-11 | tspec-generator | Traceability Matrix Generation | Source annotation and Clark Step 7 matrix |
| EL-12 | tspec-analyst | Coverage Formula (Full-UC) | total_mappable_flows computation and C1 metric |
| EL-13 | tspec-analyst | 7 Cs Quality Assessment | C2-C7 criterion evaluation per Feature file |
| EL-14 | cd-generator | Input Validation Layer 2a (Banned-Term) | Placeholder text detection and REJECT |
| EL-15 | cd-generator | HTTP Method Inference (Steps 2-4) | Request semantics to HTTP method via RULE-HM series |
| EL-16 | cd-generator | Extension-to-Error-Response Mapping (Step 7) | anchor_step cross-reference and 4xx/5xx derivation |
| EL-17 | cd-generator | PROTOTYPE Label Enforcement | `x-prototype: true` mandatory presence |
| EL-18 | cd-validator | 9-Step Validation Protocol | Per-check PASS/FAIL verdicts and verdict composition |

---

## Findings Summary

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Affected Dimension |
|----|---------|-------------|---|---|---|-----|----------|--------------------|
| FM-001-20260312 | EL-06 (uc-slicer Activity 5) | interactions[] missing required fields pass silently to cd-generator | 9 | 6 | 7 | 378 | Critical | Completeness |
| FM-002-20260312 | EL-04 (uc-slicer Step 1 gate) | detail_level set incorrectly by uc-author passes validation gate | 8 | 5 | 8 | 320 | Critical | Methodological Rigor |
| FM-003-20260312 | EL-15 (cd-generator HTTP inference) | Low-confidence HTTP method cascades into production contract without blocking | 8 | 6 | 7 | 336 | Critical | Evidence Quality |
| FM-004-20260312 | EL-09 (Clark Step 6) | Extension with unknown `outcome` value halts generation silently | 8 | 5 | 8 | 320 | Critical | Completeness |
| FM-005-20260312 | EL-01 (rejection artifact) | Stale rejection artifact causes uc-author to over-elaborate to wrong target level | 7 | 6 | 7 | 294 | Critical | Internal Consistency |
| FM-006-20260312 | EL-16 (cd-generator Step 7) | anchor_step mismatch suppresses all error responses for affected interaction | 8 | 5 | 7 | 280 | Critical | Completeness |
| FM-007-20260312 | EL-12 (tspec-analyst coverage) | Slice-scoped coverage formula denominates against wrong slice when slice_id is null | 7 | 5 | 8 | 280 | Critical | Internal Consistency |
| FM-008-20260312 | EL-10 (tspec-generator Layer 2) | LLM-evaluated semantic gate produces false-negative for BULLETED_OUTLINE detail_level | 7 | 5 | 6 | 210 | Major | Methodological Rigor |
| FM-009-20260312 | EL-02 (Cockburn 12-step) | Basic flow exceeds 9 steps accepted without decomposition | 7 | 4 | 7 | 196 | Major | Completeness |
| FM-010-20260312 | EL-06 (uc-slicer Activity 5) | realization_level set to INTERACTION_DEFINED before interactions[] is populated | 8 | 4 | 6 | 192 | Major | Methodological Rigor |
| FM-011-20260312 | EL-14 (cd-generator banned-term) | Unicode normalization gap allows NBSP-padded placeholders to bypass Layer 2a | 7 | 4 | 7 | 196 | Major | Evidence Quality |
| FM-012-20260312 | EL-11 (traceability matrix) | Feature file written without Source annotations; tspec-analyst marks all as untraceable | 7 | 4 | 6 | 168 | Major | Traceability |
| FM-013-20260312 | EL-18 (cd-validator protocol) | Step 7 PROTOTYPE check bypassed when info section is malformed YAML | 8 | 3 | 7 | 168 | Major | Methodological Rigor |
| FM-014-20260312 | EL-13 (7 Cs assessment) | C3-C7 criteria applied without formal rubric; assessments are narrative, not binary | 5 | 7 | 5 | 175 | Major | Methodological Rigor |
| FM-015-20260312 | EL-07 (INVEST verification) | Slice fails E (Estimable) but INVEST assessment recorded as partial pass | 6 | 5 | 6 | 180 | Major | Evidence Quality |
| FM-016-20260312 | EL-03 (uc-author verification) | Post-creation allOf check is LLM-evaluated, not schema-validated | 6 | 6 | 5 | 180 | Major | Methodological Rigor |
| FM-017-20260312 | EL-08 (Clark Step 4) | Multiple basic_flow steps generate multiple Scenarios instead of one | 7 | 4 | 6 | 168 | Major | Internal Consistency |
| FM-018-20260312 | EL-05 (rejection artifact write) | Rejection artifact overwrites valid prior rejection with wrong fields | 6 | 5 | 6 | 180 | Major | Internal Consistency |
| FM-019-20260312 | EL-15 (cd-generator HTTP inference) | PUT vs PATCH ambiguity produces wrong idempotency semantics | 5 | 7 | 5 | 175 | Major | Evidence Quality |
| FM-020-20260312 | EL-17 (PROTOTYPE label) | cd-generator produces contract with x-prototype: true but cd-validator Step 7 fails due to case mismatch | 6 | 4 | 7 | 168 | Major | Internal Consistency |
| FM-021-20260312 | EL-12 (tspec-analyst coverage) | Untraceable scenarios counted toward mapped_flows inflating coverage | 6 | 5 | 5 | 150 | Major | Evidence Quality |
| FM-022-20260312 | EL-02 (Cockburn 12-step) | Steps 7-8 (extensions, alternative flows) skipped when user requests BULLETED_OUTLINE | 5 | 6 | 5 | 150 | Major | Completeness |
| FM-023-20260312 | EL-18 (cd-validator protocol) | Steps 8-9 (internal ops, IC-05) produce only documentation gaps, not FAIL verdicts | 4 | 8 | 4 | 128 | Major | Actionability |
| FM-024-20260312 | EL-16 (cd-generator Step 7) | Extension outcome=success generates 2xx variant but response code not disambiguated from primary | 5 | 5 | 5 | 125 | Major | Internal Consistency |
| FM-025-20260312 | EL-10 (tspec-generator Layer 2) | preconditions absence produces WARN but Generated Given clauses may still be incorrect | 4 | 6 | 5 | 120 | Major | Evidence Quality |
| FM-026-20260312 | EL-06 (uc-slicer Activity 5) | interactions[] produced with non-unique ids across slices | 5 | 4 | 6 | 120 | Major | Internal Consistency |
| FM-027-20260312 | EL-04 (uc-slicer gate) | basic_flow step count edge case: exactly 3 steps accepted, extensions empty | 5 | 4 | 5 | 100 | Major | Completeness |
| FM-028-20260312 | EL-11 (traceability matrix) | Scenario names do not include source step reference; CI check cannot verify | 4 | 5 | 5 | 100 | Minor | Traceability |
| FM-029-20260312 | EL-07 (INVEST verification) | INVEST N (Negotiable) fails silently without blocking state transition | 3 | 6 | 5 | 90 | Minor | Completeness |
| FM-030-20260312 | EL-03 (uc-author verification) | goal_symbol inconsistency with goal_level not detected in post-creation check | 5 | 3 | 6 | 90 | Minor | Internal Consistency |
| FM-031-20260312 | EL-13 (7 Cs assessment) | C4 (consistent abstraction) requires cross-scenario comparison not explicitly performed | 3 | 5 | 5 | 75 | Minor | Completeness |
| FM-032-20260312 | EL-08 (Clark Step 4) | $.trigger absent produces missing first When clause without rejection | 3 | 5 | 5 | 75 | Minor | Completeness |
| FM-033-20260312 | EL-17 (PROTOTYPE label) | PROTOTYPE label narrative explanation absent from L0 summary in some paths | 3 | 5 | 4 | 60 | Minor | Actionability |
| FM-034-20260312 | EL-19 (all agents: output path) | JERRY_PROJECT not set causes all agents to fall back to work/ silently | 3 | 4 | 5 | 60 | Minor | Actionability |

**Total RPN: 4,858 | Critical (RPN >= 200): 7 | Major (80-199): 18 | Minor (< 80): 9**

---

## Detailed Findings

### FM-001-20260312: interactions[] Missing Required Fields Pass Silently to cd-generator

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Element** | EL-06 -- uc-slicer Activity 5 Interaction Sequence Production |
| **S / O / D** | 9 / 6 / 7 = RPN 378 |
| **Strategy Step** | Step 2 (Enumerate Failure Modes) + Step 3 (Rate) |

**Evidence:**

uc-slicer.governance.yaml `guardrails.input_validation` specifies that each `$.interactions[*]` must have all 7 required fields, but this constraint is enforced at the cd-generator input gate (Layer 2), not at uc-slicer output. The uc-slicer post-update verification (`post_completion_checks`) lists `verify_interactions_present_when_realization_level_INTERACTION_DEFINED` but does NOT list `verify_each_interaction_has_all_7_required_fields`. The cd-generator agent definition (cd-generator.md, Layer 2) enforces the 7-field check, but this is LLM-evaluated at consumption time. If uc-slicer produces an interaction with 5 of 7 fields (e.g., missing `source_flow` and `system_role`), the artifact writes successfully and `realization_level: INTERACTION_DEFINED` is set. The artifact passes uc-slicer's own post-completion checks. The defect is silent until cd-generator encounters it.

**Analysis:**

This is a producer-consumer gap at the highest-severity inter-agent boundary. The producer (uc-slicer) does not verify field completeness per interaction; the consumer (cd-generator) rejects. The gap means an entire Activity 5 run can complete, with Story entities created in worktracker, with the artifact marked INTERACTION_DEFINED, with the full pipeline appearing to succeed -- and the failure only surfaces when cd-generator executes. This is a "late detection" failure: Severity=9 because the artifact appears fully produced; Occurrence=6 because Activity 5 is the most complex step in the pipeline and partial interaction objects are a realistic output; Detection=7 because uc-slicer's own checks don't catch it.

**Recommendation:**

Add a per-interaction field completeness check to uc-slicer's Step 8 and post-update verification: before setting `realization_level: INTERACTION_DEFINED`, verify each interaction in `$.interactions[*]` has all 7 required fields (id, source_step, source_flow, actor_role, system_role, request_description, response_description). If any interaction fails, HALT and report the specific failing interaction ID and missing field(s). This check should be added to `post_completion_checks` in uc-slicer.governance.yaml as `verify_each_interaction_has_all_7_required_fields`.

**Acceptance Criteria:** uc-slicer HALTS before writing INTERACTION_DEFINED when any interaction lacks a required field. Post-correction RPN estimate: 9 x 2 x 2 = 36 (S unchanged, O drops from 6 to 2 with early detection, D drops to 2 with explicit check).

---

### FM-002-20260312: detail_level Set Incorrectly by uc-author Passes uc-slicer Validation Gate

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Element** | EL-04 -- uc-slicer Step 1 Input Validation Gate |
| **S / O / D** | 8 / 5 / 8 = RPN 320 |
| **Strategy Step** | Step 2 (Enumerate Failure Modes) + Step 3 (Rate) |

**Evidence:**

uc-author.md Post-Creation Verification step 5 states: "verify `detail_level` matches the actual content depth." This check is LLM-evaluated (the agent is instructed to verify, but there is no deterministic schema enforcement for semantic prerequisites like "extensions must be non-empty for ESSENTIAL_OUTLINE"). uc-slicer Step 1 validates that `$.detail_level >= ESSENTIAL_OUTLINE` by reading the field value -- it does not re-verify the semantic prerequisites for that level. If uc-author sets `detail_level: ESSENTIAL_OUTLINE` with an empty `extensions[]` array (which violates the schema's `allOf` constraint 4), the uc-slicer gate reads the string value and may pass the artifact through if `extensions[]` is structurally present but empty.

**Analysis:**

The uc-slicer validation gate is a field-value check, not a prerequisite-content check. The schema enforces allOf constraints (e.g., `if detail_level is ESSENTIAL_OUTLINE then extensions must have minItems: 1`), but these allOf constraints require schema-based validation, which is explicitly noted as a gap in both agents: "When `jerry schema validate` becomes available (GH #193), use it for deterministic validation. Until then, verify each constraint explicitly." This means both producer and consumer rely on LLM self-assessment for semantic compliance. Severity=8: downstream Clark transformation requires extensions for error scenario generation; Occurrence=5: realistic that uc-author sets the level optimistically; Detection=8: no deterministic gate catches this.

**Recommendation:**

uc-slicer Step 1 should validate not just the `detail_level` string value but also the content prerequisites: (a) `extensions[]` must be non-empty when `detail_level >= ESSENTIAL_OUTLINE`, (b) `basic_flow` must have typed steps when `detail_level >= ESSENTIAL_OUTLINE`. These are already listed as input_validation entries in uc-slicer.governance.yaml (`"Input artifact must have $.extensions[] non-empty"`), but must be executed as distinct, sequential checks. Both the uc-author post-creation check and uc-slicer validation gate should be hardened to validate these prerequisites deterministically. Reference: GH #193 (`jerry schema validate`) -- this gap should be tracked against that ticket.

**Acceptance Criteria:** uc-slicer rejects artifacts where `detail_level = ESSENTIAL_OUTLINE` but `extensions[]` is empty or absent, triggering the rejection artifact protocol. Post-correction RPN estimate: 8 x 2 x 3 = 48.

---

### FM-003-20260312: Low-Confidence HTTP Method Cascades Without Blocking

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Element** | EL-15 -- cd-generator HTTP Method Inference |
| **S / O / D** | 8 / 6 / 7 = RPN 336 |
| **Strategy Step** | Step 2 (Enumerate Failure Modes) + Step 3 (Rate) |

**Evidence:**

cd-generator.md Step 4 states: "Ambiguous (no pattern match) -> POST + `x-method-inference: low` annotation (RULE-HM-05)". The agent annotates Low confidence operations and reports them in the L0 summary. cd-validator Step 3 flags operations with `x-method-inference: low` "for human review." However, neither agent **blocks** the contract generation or produces a FAIL verdict when Low confidence HTTP methods are present. The `x-prototype: true` label is the only safety gate. The SKILL.md output quality gate section confirms: "The PROTOTYPE label remains on all contracts until: (1) cd-validator produces a PASS verdict on all 9 checks, (2) a human reviewer confirms semantic correctness." But cd-validator Step 3's failure action on `x-method-inference: low` is only "flag for human review," not a FAIL. A contract with all Low-confidence operations can still receive a PASS verdict from cd-validator.

**Analysis:**

The safety gate (PROTOTYPE label + human review) is a soft gate dependent on human action. In automated pipelines or under time pressure, a contract with incorrect HTTP methods (e.g., POST where PUT is correct, violating RFC 9110 idempotency guarantees) can be promoted to production. Severity=8: wrong HTTP methods cause API clients to use incorrect semantics; Occurrence=6: interactions with ambiguous descriptions are common when uc-slicer Activity 5 is first executed; Detection=7: the annotation is present but no blocking mechanism exists.

**Recommendation:**

cd-validator Step 3 should treat operations with `x-method-inference: low` for all external operations as a **FAIL verdict, not merely a flag**. At minimum, if more than 20% of external operations have `x-method-inference: low`, the contract should fail validation. This forces cd-generator remediation (improving interaction descriptions) before the contract is consumed. Add to cd-validator Step 3 failure action: "If count(x-method-inference: low) / count(external_operations) > 0.20, FAIL Step 3 with message: 'More than 20% of operations have low-confidence HTTP method inference. Improve interaction descriptions via /use-case (uc-slicer Activity 5) before proceeding.'"

**Acceptance Criteria:** cd-validator FAIL verdicts on contracts where > 20% of operations have `x-method-inference: low`. Post-correction RPN estimate: 8 x 4 x 2 = 64.

---

### FM-004-20260312: Extension with Unknown `outcome` Value Halts Generation Silently

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Element** | EL-09 -- tspec-generator Clark Step 6 (Extension Scenarios) |
| **S / O / D** | 8 / 5 / 8 = RPN 320 |
| **Strategy Step** | Step 2 (Enumerate Failure Modes) + Step 3 (Rate) |

**Evidence:**

tspec-generator.md Failure Modes table: "If `$.extensions[*].outcome` does not match pattern `^(success|failure|rejoin:\d+)$` -- Flag specific extension ID; apply H-31: ask user how to classify this outcome before generating the scenario." This behavior (HALT and ask) is correct but creates a silent partial generation scenario: the generator has already written portions of the Feature file when it encounters an unrecognized outcome, resulting in a partially complete Feature file that may appear complete but is missing scenarios for the flagged extension(s). tspec-analyst's post-completion check `verify_every_extension_is_accounted_for` would catch this, but only after a second agent invocation. The tspec-generator does not document partial output clearly in the Feature file YAML frontmatter.

**Analysis:**

The failure mode is "partial completion with unclear state." The Feature file exists but is incomplete. Downstream tspec-analyst may compute coverage against a denominator that includes the unresolved extension, reporting < 100% coverage -- but the actual issue is an invalid outcome value upstream, not a coverage gap. Severity=8: a partially generated Feature file may be used as if complete; Occurrence=5: novel UC authors may write non-standard outcome values; Detection=8: no mechanism marks the Feature file as partial in its frontmatter.

**Recommendation:**

tspec-generator should: (a) validate ALL extension outcome values BEFORE beginning any scenario generation (not during), and (b) if any extension has an invalid outcome, produce the Feature file with ONLY the valid scenarios AND add a `generation_status: PARTIAL` field to the YAML frontmatter with `unresolved_extensions: [list of extension IDs]`. This makes the partial state machine-readable. The coverage field should reflect only the valid denominator (i.e., exclude invalid extensions from total_flows).

**Acceptance Criteria:** Feature file YAML frontmatter contains `generation_status: PARTIAL` when any extension outcome is unresolvable. Post-correction RPN estimate: 8 x 2 x 2 = 32.

---

### FM-005-20260312: Stale Rejection Artifact Causes uc-author to Elaborate to Wrong Target Level

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Element** | EL-01 -- uc-author Rejection Artifact Protocol |
| **S / O / D** | 7 / 6 / 7 = RPN 294 |
| **Strategy Step** | Step 2 (Enumerate Failure Modes) + Step 3 (Rate) |

**Evidence:**

uc-author.md Rejection Artifact Check step 2d: "Check staleness (T3 mitigation): If the artifact file's modification time is more recent than the rejection artifact's timestamp, warn the user: 'Rejection artifact may be stale...' Wait for user guidance before proceeding." This is a WARN+WAIT flow, which is correct, but the check relies on filesystem modification time comparison. In common CI/deployment scenarios, artifact modification times are not reliable (git checkout resets mtimes; containerized builds use build time). If `mtime` comparison returns false (artifact appears older than rejection), the agent will consume the stale rejection artifact, setting `target_detail_level` from the rejection even though the artifact has since been corrected by a different author. The consequence is uc-author elaborating to an incorrect level, potentially overwriting correct ESSENTIAL_OUTLINE content to reach FULLY_DESCRIBED.

**Analysis:**

The staleness detection depends on filesystem mtime, which is an unreliable signal in version-controlled environments. A more reliable staleness check would compare the rejection artifact's `current_state.detail_level` against the artifact's actual current `$.detail_level` -- if they differ, the rejection is stale. Severity=7: incorrect elaboration wastes work and may over-elaborate sub-use cases; Occurrence=6: CI environments commonly reset mtimes; Detection=7: the WARN+WAIT only fires if mtime comparison is accurate.

**Recommendation:**

Add a semantic staleness check alongside the mtime check: "If the rejection artifact's `current_state.detail_level` does not match the artifact's actual `$.detail_level`, the rejection artifact is semantically stale (the artifact has already been advanced)." This check is mtime-independent. If semantic staleness is detected, delete the rejection artifact and proceed with user-specified or default target_detail_level.

**Acceptance Criteria:** uc-author detects staleness via detail_level comparison when mtime comparison is unavailable or unreliable. Post-correction RPN estimate: 7 x 3 x 3 = 63.

---

### FM-006-20260312: anchor_step Mismatch Suppresses All Error Responses for Affected Interaction

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Element** | EL-16 -- cd-generator Extension-to-Error-Response Mapping (Step 7) |
| **S / O / D** | 8 / 5 / 7 = RPN 280 |
| **Strategy Step** | Step 2 (Enumerate Failure Modes) + Step 3 (Rate) |

**Evidence:**

cd-generator.md Step 7: "For each `$.extensions[*]` where `outcome = failure`: Cross-reference `$.extensions[*].anchor_step` with `$.interactions[*].source_step`... Failure action: 'Warn; document the unmatched extension in the mapping document; do not suppress the warning.'" The agent documents unmatched anchor steps in the mapping document with a WARNING, but the contract is still written without the error responses. cd-validator Step 5 then checks that error responses exist -- but only for extensions where anchor_step matches an interaction source_step. If the cross-reference produces zero matches (e.g., anchor_step=3 but all interactions have source_step=1, 2, 4), the contract is written with no 4xx/5xx responses at all, and cd-validator Step 5 passes because there are no unmatched extensions in the validator's view (the validator only checks extensions that can be cross-referenced to operations -- extensions with no matching operation are a generator gap, not a validator gap).

**Analysis:**

The validation coverage formula for error responses has a gap: cd-validator Step 5 checks "for each extension with outcome=failure, verify the corresponding operation has an error response." But if the anchor_step cross-reference produces zero matches (due to the extension having anchor_step referencing a step number that doesn't appear in interactions), neither the warning in the mapping document nor the validator check catches the net result: the entire API contract lacks error responses. Severity=8: contracts without 4xx/5xx responses are production safety risks; Occurrence=5: anchor_step mismatches are likely when uc-slicer Activity 5 uses subset of flow steps; Detection=7: mapping document warning is not surfaced in cd-validator verdict.

**Recommendation:**

cd-validator Step 5 should be amended: "For each `$.extensions[*]` with `outcome = failure` in the source UC artifact, check whether the extension is documented in the mapping document as an unmatched anchor_step warning. If so, count this as a FAIL (not a pass) with message: 'Extension {id} was not mapped to an error response due to anchor_step mismatch. Verify interaction source_step values match extension anchor_steps.'" This ensures the mapping document warning becomes a validator FAIL, not a silent gap.

**Acceptance Criteria:** cd-validator FAIL when any failure extension has no mapped error response, including anchor_step mismatch cases. Post-correction RPN estimate: 8 x 3 x 2 = 48.

---

### FM-007-20260312: Slice-Scoped Coverage Formula Denominates Against Wrong Slice

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Element** | EL-12 -- tspec-analyst Coverage Formula |
| **S / O / D** | 7 / 5 / 8 = RPN 280 |
| **Strategy Step** | Step 2 (Enumerate Failure Modes) + Step 3 (Rate) |

**Evidence:**

tspec-analyst.md Step 2 describes the slice-scoped coverage formula: `slice_mappable_flows = 1 if any basic_flow step is in slice_steps + count(alt_flows where branches_from_step in slice_steps) + count(extensions where anchor_step in slice_steps)`. The formula is computed from `$.slices[slice_id].steps_included[*]`. However, tspec-analyst.md Step 2 for full-UC coverage states: "slice_id = null" triggers full UC formula. The Feature file YAML frontmatter includes `slice_id` if slice-scoped generation was used. The failure mode occurs when: (a) tspec-generator was invoked without a slice_id (full UC generation), (b) the resulting Feature file has no `slice_id` in frontmatter (correct), but (c) the UC artifact has `$.realization_level = STORY_DEFINED` (slices exist), causing tspec-analyst to incorrectly infer that it should apply the slice formula rather than the full-UC formula. This is "Ambiguous" -- the disambiguation logic is not explicit in the tspec-analyst methodology.

**Analysis:**

The switch between full-UC and slice-scoped formulas depends on `slice_id` in the Feature file frontmatter. The tspec-analyst correctly reads this field. However, the documentation does not explicitly state: "if Feature file frontmatter.slice_id is absent or null, always use full-UC formula regardless of `$.realization_level`." Without this explicit rule, the agent may confuse "no slice_id in FF" with "this UC has slices, infer a slice ID." Severity=7: incorrect denominator produces wrong coverage percentage; Occurrence=5: slice-enabled UCs are common in the pipeline; Detection=8: the formula decision is LLM-evaluated with no deterministic disambiguation.

**Recommendation:**

tspec-analyst Step 2 should add explicit disambiguation: "If `slice_id` is absent, null, or not present in the Feature file YAML frontmatter, ALWAYS use the full-UC formula, regardless of `$.realization_level` or the presence of `$.slices[]` in the source UC artifact. The Feature file's `slice_id` field is the authoritative signal for formula selection."

**Acceptance Criteria:** tspec-analyst uses full-UC formula when Feature file slice_id is absent, even when source UC has STORY_DEFINED realization level. Post-correction RPN estimate: 7 x 2 x 2 = 28.

---

## Major Findings (Selected Detail)

### FM-010-20260312: realization_level Set to INTERACTION_DEFINED Before interactions[] Populated

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | EL-06 -- uc-slicer Activity 5 |
| **S / O / D** | 8 / 4 / 6 = RPN 192 |

**Evidence:** uc-slicer.governance.yaml `forbidden_actions` includes: "REALIZATION VIOLATION: NEVER set `$.realization_level` without verifying that the corresponding blocks are populated." However, uc-slicer.md Step 8 orders: "(8) Before setting `realization_level: INTERACTION_DEFINED`, verify the output artifact's YAML frontmatter satisfies the allOf constraints..." The risk is that an LLM agent executing Step 8 may update the YAML in multiple write operations, setting `realization_level` in one edit before `interactions[]` in a second edit. If the write sequence is interrupted (tool error, context limit), the artifact is left in an inconsistent state.

**Recommendation:** Step 8 should be a single atomic write: update interactions[], realization_level, and slice_state in one Write/Edit operation. The allOf constraint verification should occur in memory before any write, not after. Post-correction RPN estimate: 8 x 2 x 2 = 32.

---

### FM-014-20260312: C3-C7 Quality Criteria Applied Without Formal Rubric

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | EL-13 -- tspec-analyst 7 Cs Assessment |
| **S / O / D** | 5 / 7 / 5 = RPN 175 |

**Evidence:** tspec-analyst.md Step 5 defines C1-C7 criteria as qualitative checks ("Declarative language; no implementation specifics" for C3; "No duplicates; no redundant steps" for C7). The output format requires "7 Cs quality assessment: PASS/WARN/FAIL per criterion" but provides no numeric rubric or concrete examples differentiating PASS from WARN from FAIL. The coverage report section lists "7 Cs quality assessment: PASS/WARN/FAIL per criterion" in the L0 output, but the methodology section (Step 5) does not define the threshold between PASS and WARN for C3-C7.

**Recommendation:** Define concrete binary thresholds for each of C3-C7. Example: C3 FAIL = any Given/When/Then clause contains a UI element reference (button name, URL path) or programming term. C7 FAIL = two or more scenarios share identical Given+When sequences. Post-correction RPN estimate: 5 x 4 x 2 = 40.

---

### FM-016-20260312: uc-author Post-Creation allOf Check is LLM-Evaluated

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | EL-03 -- uc-author Post-Creation Verification |
| **S / O / D** | 6 / 6 / 5 = RPN 180 |

**Evidence:** uc-author.md Post-Creation Verification step 2: "Verify the output artifact's YAML frontmatter satisfies the allOf constraints defined in `docs/schemas/use-case-realization-v1.schema.json`. Check: (1) goal_symbol matches goal_level, (2) if realization_level is INTERACTION_DEFINED then interactions[] must have minItems: 1, (3) if realization_level is STORY_DEFINED then slices[] must have minItems: 1, (4) if detail_level is ESSENTIAL_OUTLINE or FULLY_DESCRIBED then extensions[] must have minItems: 1, (5) INTERACTION_DEFINED is not permitted with BRIEFLY_DESCRIBED or BULLETED_OUTLINE detail_level." Note: "When `jerry schema validate` becomes available (GH #193), use it for deterministic validation. Until then, verify each constraint explicitly." This is a documented gap: all 5 checks are LLM-evaluated.

**Recommendation:** Track GH #193 completion as a blocker for promoting all three skills from PROPOSED to ACTIVE status. Until the CLI gate is available, add a Bash-based validation step using `uv run python -c "import yaml; ..."` to at minimum verify the critical allOf constraints (goal_symbol consistency, extensions non-empty for ESSENTIAL_OUTLINE) deterministically. Post-correction RPN estimate: 6 x 3 x 2 = 36.

---

### FM-023-20260312: Steps 8-9 Produce Only Documentation Gaps, Not FAIL Verdicts

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | EL-18 -- cd-validator 9-Step Protocol |
| **S / O / D** | 4 / 8 / 4 = RPN 128 |

**Evidence:** cd-validator.md Steps 8 and 9 failure actions: "Report as a documentation gap (not a critical FAIL unless all provider interactions are undocumented)" (Step 8) and "Report any supporting actors with no contract presence. Report as a documentation gap." (Step 9). Both steps can produce findings with no effect on the overall PASS/FAIL verdict. A contract can receive a PASS verdict from cd-validator while missing all internal operations documentation and all supporting actor cross-references. The combined verdict rule "PASS only if all 9 steps pass" is stated in the overview but each step's failure action softens Steps 8-9 to documentation gaps.

**Recommendation:** Either (a) make Steps 8-9 produce FAIL verdicts consistently, aligned with the stated "all 9 steps must pass" rule, or (b) explicitly document Steps 8-9 as advisory (WARN, not FAIL) and update the verdict rule to "PASS if Steps 1-7 pass; Steps 8-9 produce WARNs." The current ambiguity between the verdict rule and the step-level failure actions is an Internal Consistency failure in the specification itself. Post-correction RPN estimate: 4 x 4 x 2 = 32.

---

## Recommendations Summary

### Critical Priority (RPN >= 200 -- Mandatory Corrective Actions)

| ID | Corrective Action | Acceptance Criteria | Est. Post-RPN |
|----|------------------|---------------------|---------------|
| FM-001 | Add per-interaction 7-field completeness check to uc-slicer Step 8 and post_completion_checks | uc-slicer HALTs before INTERACTION_DEFINED when any interaction lacks required fields | 36 |
| FM-002 | Add content-prerequisite checks to uc-slicer Step 1 gate: verify extensions[] non-empty when detail_level=ESSENTIAL_OUTLINE | uc-slicer triggers rejection artifact when extensions[] empty despite correct detail_level label | 48 |
| FM-003 | cd-validator Step 3: FAIL when > 20% of external operations have `x-method-inference: low` | cd-validator produces FAIL verdict for contracts with majority Low-confidence HTTP methods | 64 |
| FM-004 | tspec-generator: validate all extension outcomes before generating; add `generation_status: PARTIAL` to FF frontmatter when any extension unresolvable | Feature file frontmatter indicates partial state machine-readably | 32 |
| FM-005 | Add semantic staleness check to uc-author rejection artifact protocol: compare `current_state.detail_level` against actual artifact `$.detail_level` | uc-author detects stale rejections via detail_level comparison, mtime-independent | 63 |
| FM-006 | cd-validator Step 5: treat anchor_step mismatch warnings (from mapping document) as FAIL | cd-validator FAILs when any failure extension lacks a mapped error response | 48 |
| FM-007 | tspec-analyst Step 2: explicit rule that Feature file `slice_id` absence = full-UC formula always | tspec-analyst uses correct formula when Feature file slice_id absent regardless of UC realization_level | 28 |

### Major Priority (Targeted Corrections -- Strongly Recommended)

| ID | Corrective Action | Est. Post-RPN |
|----|------------------|---------------|
| FM-010 | uc-slicer Step 8: atomic write of interactions[], realization_level, and slice_state | 32 |
| FM-011 | cd-generator Layer 2a: document Unicode normalization scope for non-ASCII whitespace; add explicit NFC step to banned-term matching | 56 |
| FM-013 | cd-validator Step 7: verify info section parses before checking x-prototype; structural YAML parse is Step 1 prerequisite | 32 |
| FM-014 | tspec-analyst: define concrete binary thresholds for C3-C7 | 40 |
| FM-016 | uc-author: implement Bash-based allOf constraint checks pending GH #193 | 36 |
| FM-018 | uc-slicer: before overwriting rejection artifact, verify rejected_artifact field matches current artifact path | 60 |
| FM-023 | cd-validator: clarify Steps 8-9 as WARN or FAIL; align step-level failure actions with overall verdict rule | 32 |

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| **Completeness** | 0.20 | Negative | FM-001 (missing interaction fields), FM-002 (prerequisite content gap), FM-004 (partial FF generation), FM-006 (error response suppression), FM-009 (flow step limit bypassed), FM-022 (steps 7-8 skipped) collectively show gaps in completeness enforcement across the pipeline. Seven Critical and Major findings directly affect whether all required elements are produced. |
| **Internal Consistency** | 0.20 | Negative | FM-005 (stale rejection artifact), FM-007 (coverage formula disambiguation), FM-010 (non-atomic YAML write), FM-017 (multiple happy-path scenarios), FM-020 (PROTOTYPE case mismatch), FM-023 (Steps 8-9 vs. verdict rule) show internal contradictions between declared behavior and actual enforcement. |
| **Methodological Rigor** | 0.20 | Negative | FM-002 (LLM-evaluated gate), FM-008 (semantic gate false negatives), FM-013 (PROTOTYPE check precondition), FM-014 (7 Cs rubric absent), FM-016 (allOf LLM-evaluated) collectively show that the pipeline relies heavily on LLM self-evaluation for critical methodology enforcement, with no deterministic fallbacks until GH #193 is resolved. |
| **Evidence Quality** | 0.15 | Mixed | FM-003 (Low HTTP inference propagation), FM-011 (Unicode gap), FM-015 (INVEST partial pass), FM-019 (PUT/PATCH ambiguity), FM-021 (untraceable scenarios in denominator), FM-025 (Given clauses without preconditions) show evidence quality gaps. Partially mitigated by the extensive annotation system (x-method-inference, x-description-quality, Source annotations). |
| **Actionability** | 0.15 | Neutral | The pipeline's error messages and rejection artifacts are generally specific and actionable (REJECT messages include corrective directives, rejection YAML includes missing_elements[]). FM-023 (Step 8-9 gap) and FM-033-034 (PROTOTYPE explanation, JERRY_PROJECT fallback) are minor actionability gaps. |
| **Traceability** | 0.10 | Positive | All three skills implement explicit traceability mechanisms: Source annotations in Feature files, x-source-interaction/step/flow in contracts, rejection artifact provenance chain, YAML frontmatter provenance fields (created_by, generated_by, created_at). FM-012 (Source annotation absence) and FM-028 (scenario name gap) are isolated issues, not systemic. |

---

## Execution Statistics

- **Total Findings:** 34
- **Critical:** 7
- **Major:** 18
- **Minor:** 9
- **Protocol Steps Completed:** 5 of 5
- **Elements Analyzed:** 18 (MECE -- mutually exclusive across agents; collectively exhaustive across the pipeline)
- **Total RPN:** 4,858
- **Estimated Post-Correction RPN (Critical findings only):** 319 (94% RPN reduction for Critical findings)
- **Overall Assessment:** REVISE -- Significant pipeline with strong foundational design. Seven Critical findings require mandatory corrective actions before C4 approval. Eighteen Major findings represent hardening improvements. Nine Minor findings are improvement opportunities.

---

## H-15 Self-Review

Pre-persistence verification completed:

1. All 34 findings reference specific evidence from the agent definitions, governance YAML files, SKILL.md files, or schema files read during execution. No vague findings.
2. Severity classifications are justified: 7 Critical findings have RPN >= 200 with S >= 7; 18 Major findings have RPN 100-199 or S 5-8 with lower O/D; 9 Minor findings have RPN < 100.
3. Finding identifiers follow FM-NNN-20260312 format consistently.
4. Summary table (34 rows) matches detailed finding count (7 Critical detailed + summary rows for all 34 matches).
5. No findings were minimized. The six Critical boundary findings (FM-001 through FM-006) represent genuine pipeline risks at inter-agent handoff points. FM-007 was classified Critical due to formula error that produces incorrect quality metrics silently.

---

*Strategy Execution Report: S-012 FMEA*
*Generated: 2026-03-12*
*Template: `.context/templates/adversarial/s-012-fmea.md` v1.0.0*
*SSOT: `.context/rules/quality-enforcement.md`*
*Execution ID: 20260312*
