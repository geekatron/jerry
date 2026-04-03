# Strategy Execution Report: S-013 Inversion Technique

## Execution Context

- **Strategy:** S-013 (Inversion Technique)
- **Template:** `.context/templates/adversarial/s-013-inversion.md`
- **Deliverable:** `/use-case`, `/test-spec`, `/contract-design` skills -- 6 agent pairs (.md + .governance.yaml), 3 SKILL.md files, 2 JSON schemas
- **Executed:** 2026-03-12T00:00:00Z
- **Criticality:** C4 (tournament mode)
- **H-16 Compliance:** C4 tournament -- S-003 Steelman is required in the sequence prior to S-013; applying in tournament mode per quality-enforcement.md

---

## Inversion Header

**Strategy:** S-013 Inversion Technique
**Deliverable:** PROJ-021 use-case/test-spec/contract-design skills suite (6 agents + 3 SKILL.md + 2 schemas)
**Criticality:** C4
**Date:** 2026-03-12
**Reviewer:** adv-executor
**Goals Analyzed:** 7 | **Assumptions Mapped:** 22 | **Vulnerable Assumptions:** 14

---

## Summary

Systematic inversion of the pipeline's goals reveals 4 Critical and 7 Major vulnerable assumptions clustered around three anti-goal conditions: (1) valid-looking artifacts can be produced that silently pass schema validation while carrying semantically broken content, causing downstream pipeline stages to produce garbage outputs with no warnings; (2) edge case inputs at array boundaries (minimum 3, maximum 9 basic flow steps; empty vs. single-element arrays) expose untested behavior gaps in rejection logic and coverage calculations; (3) conflicting user instructions versus methodological rules create undefined agent behavior with no explicit resolution protocol. The PROTOTYPE label assumption (that cd-generator is the only path to production contracts) is the most critical finding: a user who understands the internal format can construct a valid-schema artifact that bypasses the entire pipeline. Targeted mitigations exist for all Critical findings.

---

## Step 1: Goals Inventory

The deliverable suite has the following primary goals:

| # | Goal | Measurable Form |
|---|------|----------------|
| G-1 | Produce structured use case artifacts that are schema-valid and ready for downstream consumption | `$.detail_level >= ESSENTIAL_OUTLINE`, `extensions[] non-empty`, `basic_flow[*].type` present; validated by `use-case-realization-v1.schema.json` |
| G-2 | Decompose use cases into implementation-ready slices with verified INVEST compliance | All slices at `slice_state >= SCOPED`, each with `invest_assessment{}` populated; `realization_level = INTERACTION_DEFINED` for Activity 5 output |
| G-3 | Generate BDD test specifications with 100% deterministic traceability to source flows | Every Gherkin scenario carries a `**Source:**` annotation; coverage percentage = mapped/total flows; no invented scenarios |
| G-4 | Produce OpenAPI 3.1 contracts that trace every operation to a source interaction | `x-source-interaction` annotation on every operation; `x-prototype: true` in `info`; mapping document exists |
| G-5 | Maintain pipeline integrity through schema validation gates | All agents reject invalid input with actionable error messages; rejection artifacts written for downstream recovery |
| G-6 | Produce outputs that correctly reflect the actual quality/completeness achieved (P-022) | `detail_level`, `realization_level`, `coverage_percentage`, PASS/FAIL verdicts accurately reflect actual content |
| G-7 | Protect the pipeline from invalid or malicious input injection | Banned-term checks, path-traversal mitigation, staleness detection, Unicode normalization in cd-generator |

---

## Step 2: Anti-Goals (Inverted Goals)

For each goal, asking "what would guarantee failure?":

**G-1 Inverted (AG-1):** To guarantee schema-invalid artifacts reach downstream agents, craft input that passes JSON Schema structural validation (correct field names, types) while carrying semantically broken content (e.g., `goal_level: USER_GOAL` with `goal_symbol: +` -- violates allOf constraint 1, but ONLY if the allOf check fires). If the allOf constraint is validated by the LLM agent rather than a deterministic validator, inconsistency could silently survive.

**G-2 Inverted (AG-2):** To guarantee slices are never actually implementation-ready, set `realization_level: INTERACTION_DEFINED` without populating `interactions[]` -- the schema allOf constraint catches this, but only if uc-slicer explicitly runs the allOf check. If uc-slicer sets the field via in-context text generation rather than a verification step, the check may be skipped. Alternatively, populate INVEST fields with all-`true` values without actual assessment.

**G-3 Inverted (AG-3):** To guarantee untraceable BDD scenarios, generate a Feature file where some Scenario blocks lack `**Source:**` annotations but the YAML frontmatter `scenario_count` is inflated to match. The tspec-analyst coverage formula counts scenarios by block parsing, not annotation counting -- a scenario without a Source annotation is "untraceable" but still counted as mapped.

**G-4 Inverted (AG-4):** To guarantee an OpenAPI contract reaches production without human review, remove `x-prototype: true` from the generated YAML after generation but before validation. cd-validator Step 7 catches this -- but only if the contract file is validated before distribution. Nothing prevents manual removal. Also: construct a UC artifact with `realization_level = INTERACTION_DEFINED` manually (without running uc-slicer) and feed it to cd-generator, bypassing the slice lifecycle and INVEST verification entirely.

**G-5 Inverted (AG-5):** To guarantee rejection artifacts are never written or noticed, provide an artifact at BRIEFLY_DESCRIBED to uc-slicer, which writes a rejection artifact -- but the orchestrator or user may not check `{artifact_path}-rejection.yaml` before re-invoking uc-author. The rejection artifact writing protocol assumes the orchestrator or user monitors the rejection file path.

**G-6 Inverted (AG-6):** To guarantee misleading quality signals, populate the test-specification schema `coverage.mapped_flows` value independently of the actual scenario count. The schema requires `scenario_count` to "equal coverage.mapped_flows" (per description) but does NOT enforce this with a schema constraint -- only via documentation. The `scenario_count` and `coverage.mapped_flows` fields can diverge silently.

**G-7 Inverted (AG-7):** To bypass the banned-term check in cd-generator, pad the `request_description` with sufficient non-banned characters to exceed the 60-character length threshold, then include a banned term that does not trigger the word-boundary match (e.g., embedding "TODO" as a substring of a longer word). The check applies word-boundary matching only for SUBSTRING_TERMS when `description.length < 60` -- a long description with embedded placeholder content passes Layer 2a.

---

## Step 3: Assumption Map

| # | Assumption | Type | Category | Confidence | Validation Status |
|---|-----------|------|----------|------------|-------------------|
| A-01 | LLM agents (uc-author, uc-slicer) will perform allOf constraint verification accurately via in-context reasoning | Implicit | Technical | Medium | Unvalidated -- LLM self-check |
| A-02 | `scenario_count` in Feature file frontmatter equals the actual count of Gherkin Scenario blocks | Implicit | Technical | Medium | Unvalidated -- self-reported |
| A-03 | `coverage.mapped_flows` and `scenario_count` in Feature file frontmatter are consistent with each other | Implicit | Technical | Low | No schema enforcement |
| A-04 | Users/orchestrators will check for rejection artifacts at `{artifact_path}-rejection.yaml` | Implicit | Process | Low | Unvalidated |
| A-05 | cd-generator's Unicode normalization prevents all encoding bypass attempts of banned-term check | Implicit | Technical | Medium | Tested for specified cases; Unicode space variants documented |
| A-06 | The PROTOTYPE label on OpenAPI contracts prevents premature production use | Implicit | Process | Low | Human-dependent; no enforcement |
| A-07 | `detail_level` field accurately reflects the actual content depth of the artifact | Implicit | Technical | Medium | LLM self-assessment |
| A-08 | `realization_level` as a "derived convenience field" is always populated after content | Explicit | Technical | Medium | Protocol exists; LLM adherence unvalidated |
| A-09 | Extension outcome field always contains a recognizable value from the enum pattern | Implicit | Technical | High | Schema pattern enforced |
| A-10 | Basic flow step `type` field is always set before tspec-generator is invoked | Implicit | Process | Medium | Enforced by tspec-generator rejection; uc-author behavioral rule |
| A-11 | The `source_step` cross-reference in interactions always resolves to an existing flow step | Explicit | Technical | Medium | Validated by cd-generator Layer 1 |
| A-12 | A use case artifact cannot be manually constructed to bypass uc-author/uc-slicer pipeline stages | Implicit | Security | Low | No enforcement -- schema validation only |
| A-13 | The 3-9 step constraint on `basic_flow` prevents both trivial single-step and overly complex UCs | Explicit | Methodological | High | Schema enforced (minItems: 3, maxItems: 9) |
| A-14 | Error scenario classification (400 vs. 401 vs. 404) by cd-generator is accurate | Implicit | Technical | Low | LLM heuristic -- no deterministic mapping |
| A-15 | tspec-analyst's coverage formula counts only Scenarios that have Source annotations | Implicit | Technical | Medium | Methodology states "counted but flagged" for unannotated |
| A-16 | The `slice_id` parameter in tspec-generator correctly scopes coverage to the specified slice | Implicit | Technical | Medium | Unvalidated edge case: slice with steps_included=[] |
| A-17 | Conflicting user instructions (e.g., "skip extensions") do not override methodology-required content | Implicit | Process | Low | P-020 + domain guardrails; no explicit conflict resolution |
| A-18 | The `preconditions` array with minItems: 1 (required field) means every UC has at least one precondition | Explicit | Schema | High | Schema enforced |
| A-19 | Rejection artifacts written by uc-slicer are not processed by uc-author when the path does not match `rejected_artifact` | Explicit | Security | High | Path-traversal mitigation documented |
| A-20 | `alternative_flow` absence is explicitly handled -- no extensions means no AF scenarios | Implicit | Technical | High | tspec-generator warns; proceeds without AF scenarios |
| A-21 | The `branches_from_step` field referenced in coverage formula exists on alternative_flow objects | Implicit | Technical | Low | NOT in schema -- `alternative_flow` has no `branches_from_step` field |
| A-22 | `slice_state` is set to SCOPED before PREPARED -- the lifecycle order is enforced | Explicit | Methodological | Medium | Agent behavioral rule; no state-machine enforcement in schema |

---

## Step 4: Stress-Test Results

| ID | Assumption | Inversion | Plausibility | Severity | Affected Dimension |
|----|-----------|-----------|-------------|---------|-------------------|
| IN-001 | A-12: Manual artifact bypasses pipeline | Actor manually crafts schema-valid artifact with `realization_level: INTERACTION_DEFINED` and arbitrary interactions[], feeding cd-generator without uc-author or uc-slicer | High -- any developer with the schema can do this | Critical | Methodological Rigor |
| IN-002 | A-03: scenario_count / mapped_flows inconsistency | Feature file reports `scenario_count: 5` and `coverage.mapped_flows: 5` but actually has 3 Scenario blocks; tspec-analyst counts blocks not frontmatter | High -- LLM generation drift common | Critical | Internal Consistency |
| IN-003 | A-21: branches_from_step field does not exist | tspec-analyst coverage formula references `$.alternative_flows where branches_from_step in slice_steps` but `alternative_flow` schema has no `branches_from_step` property | Certain -- schema confirmed this field is absent | Critical | Completeness |
| IN-004 | A-17: Conflicting user instructions | User says "Write a use case but skip the extensions, I just need the basic flow" -- P-020 (user authority) and domain guardrail (extensions required at ESSENTIAL_OUTLINE) conflict; agent has no explicit conflict resolution protocol | High -- common user request pattern | Critical | Methodological Rigor |
| IN-005 | A-07: detail_level misrepresentation | uc-author produces artifact with empty `extensions[]` and sets `detail_level: ESSENTIAL_OUTLINE`; allOf schema constraint would catch this, but LLM self-check may fail | Medium -- LLM accuracy on allOf constraint check ~80% | Major | Evidence Quality |
| IN-006 | A-04: Rejection artifact not monitored | uc-slicer writes `{artifact_path}-rejection.yaml` then halts; user or orchestrator invokes uc-author again without reading the rejection artifact; missing elements are not addressed | High -- orchestrator must implement active polling | Major | Actionability |
| IN-007 | A-14: HTTP status code misclassification | cd-generator classifies "resource is locked" extension condition as 422 (fallback) instead of 409 (conflict state); downstream implementers implement wrong error handling | High -- LLM semantic heuristics have known error rates | Major | Evidence Quality |
| IN-008 | A-16: Empty steps_included slice | uc-slicer creates a slice with `steps_included: []` (empty array) -- schema allows this (minItems: 1 on steps_included); tspec-generator tries to filter basic_flow steps by steps_included and gets empty result; generates Feature file with 0 scenarios | Low -- schema has minItems: 1 | Major | Completeness |
| IN-009 | A-08: realization_level set before interactions | LLM sets `realization_level: INTERACTION_DEFINED` in the artifact text but then fails to populate `interactions[]` before write; allOf constraint fires at next schema read but artifact is on disk with violation | Medium -- LLM token generation can produce field before array | Major | Internal Consistency |
| IN-010 | A-01: allOf verification via LLM | uc-author/uc-slicer verifies allOf constraints "by systematically checking each constraint" via LLM reasoning -- but the 6th allOf constraint (INTERACTION_DEFINED incompatible with BRIEFLY_DESCRIBED/BULLETED_OUTLINE) is evaluated by LLM, not a deterministic parser | Medium -- complex conditional allOf hard for LLMs | Major | Methodological Rigor |
| IN-011 | A-06: PROTOTYPE label removal | Developer reviews OpenAPI contract, is satisfied, and manually removes `x-prototype: true` before running cd-validator -- cd-validator Step 7 now fails on the user-edited file, creating a validation obstacle rather than a safety gate | Medium -- developers may not understand the label semantics | Minor | Traceability |
| IN-012 | A-22: Slice lifecycle skipping | User instructs uc-slicer to "create a fully realized slice immediately" -- uc-slicer's agent definition says "NEVER skip SCOPED state" as a forbidden action, but the agent cannot reject user instructions per P-020; explicit conflict | Low -- similar to IN-004 | Minor | Methodological Rigor |
| IN-013 | A-02: scenario_count self-reported | tspec-generator writes `scenario_count: 4` based on its own counting logic during generation, but the actual Feature file has 3 Scenario blocks due to a generation error; self-reported count not verified | Medium -- LLM counting errors in long outputs | Minor | Internal Consistency |
| IN-014 | A-05: Unicode bypass of banned-term check | Actor crafts `request_description` with `\u0054\u004F\u0044\u004F` (Unicode for "TODO") -- cd-generator's NFC normalization applies but NFC does not convert individual code points to ASCII; "TODO" composed of individual Unicode escaped characters would pass NFC but pattern-match against the literal string "TODO" | Low -- normalization handles documented variants | Minor | Evidence Quality |

---

## Step 5: Detailed Findings

### IN-001: Schema-Valid Artifact Bypasses Entire Pipeline [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Type** | Anti-Goal |
| **Section** | Pipeline Architecture / cd-generator input validation |
| **Strategy Step** | Step 2 (Anti-Goals) + Step 4 (Stress-Test) |

**Original Assumption:** A use case artifact that reaches cd-generator has passed through uc-author (Cockburn methodology) and uc-slicer (INVEST criteria, Activity 5 interaction production), guaranteeing that the pipeline's behavioral quality controls have been applied.

**Inversion:** Nothing in the schema or agent definitions prevents a developer from manually authoring a YAML+Markdown file that satisfies `use-case-realization-v1.schema.json` structural requirements (correct field names, types, patterns) while bypassing all behavioral quality controls. Such an artifact with arbitrary `interactions[]` (even interactions that do not correspond to real system behavior) would pass cd-generator's Layer 1 structural validation and proceed to OpenAPI generation.

**Plausibility:** High. Any developer who reads the schema can craft a compliant artifact. INVEST assessment values, `slice_state` transitions, and Cockburn quality indicators exist only in agent behavioral rules -- they have zero schema enforcement.

**Consequence:** The generated OpenAPI contract carries `x-prototype: true` and the traceability annotations are present, satisfying cd-validator's 9 checks. A human reviewer might not detect that the underlying use case was never properly authored. The PROTOTYPE label is the only safety gate, and it is human-removable per P-020.

**Evidence:** `use-case-realization-v1.schema.json` has `additionalProperties: false` for most objects, but the `slice` definition has `additionalProperties: true`. The `invest_assessment` properties are all `boolean` with no minimum-true-count enforcement. `basic_flow` steps require `actor`, `action`, `type` but do not validate that `actor` matches a declared `primary_actor` or `supporting_actors[*].name` -- an actor named "Attacker" is schema-valid. The schema's `allOf` constraints enforce derived-field consistency but not behavioral pipeline adherence.

**Mitigation:** (1) Add a pipeline provenance field to the schema: `created_by_pipeline: {uc-author|uc-slicer|manual}` with validation warnings for `manual`. (2) Document in SKILL.md that artifacts not created via uc-author lack Cockburn methodology assurance -- the PROTOTYPE label is insufficient as the sole protection. (3) Consider a `pipeline_signature` field populated by each agent that downstream agents can verify.

**Acceptance Criteria:** Documentation added to cd-generator input validation guidance stating that the PROTOTYPE label must remain until human reviewer confirms the source artifact was produced by the intended pipeline. Alternatively, a `created_by` field audit is performed during cd-validator Step 2.

---

### IN-002: Feature File Frontmatter scenario_count / mapped_flows Divergence [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Type** | Anti-Goal |
| **Section** | tspec-generator output / test-specification-v1.schema.json |
| **Strategy Step** | Step 2 (Anti-Goals) + Step 4 (Stress-Test) |

**Original Assumption:** `scenario_count` in Feature file YAML frontmatter equals the actual count of Gherkin `Scenario:` blocks in the file body, and `coverage.mapped_flows` equals `scenario_count`.

**Inversion:** The schema description states `scenario_count` "Must equal coverage.mapped_flows" but this is documentation-only -- there is no schema constraint (e.g., a JSON Schema `if/then` or a cross-field equality assertion) enforcing this. A tspec-generator that experiences a token-truncated generation could write `scenario_count: 5` in the frontmatter after counting expected scenarios, but only produce 3 Scenario blocks in the body due to context limit exhaustion or output truncation.

**Plausibility:** High. LLM output truncation is a known failure mode for long Feature files. The tspec-generator's post-creation verification checklist includes "Exactly 1 happy path scenario is present" but does not explicitly verify scenario body count against frontmatter `scenario_count`.

**Consequence:** tspec-analyst parses Gherkin Scenario blocks to compute coverage but also reads the frontmatter `scenario_count` for a "sanity check." If the check passes due to trusting frontmatter, incomplete coverage is reported as complete. Downstream implementers receive a Feature file that appears to have full coverage (per frontmatter) but is missing error scenarios.

**Evidence:** `test-specification-v1.schema.json` lines 48-51: `scenario_count` described as "Must equal coverage.mapped_flows" -- but `additionalProperties: false` and no cross-field constraint enforces this. `coverage.mapped_flows` (`minimum: 1`) and `scenario_count` (`minimum: 1`) are independent integer fields. tspec-analyst methodology Step 3 says "Parse each Gherkin Scenario block from the Feature file" -- this is correct behavior, but tspec-analyst also reads `scenario_count` for its Step 1 "quick sanity check" which can create a misleading baseline.

**Mitigation:** (1) Add schema enforcement: within `allOf`, assert `scenario_count == coverage.mapped_flows` using a JSON Schema numeric equality pattern (or at least add `maximum: coverage.mapped_flows` cross-reference). (2) tspec-analyst should always derive coverage from Scenario block counting, never from frontmatter values. (3) Add a tspec-generator post-creation check: "Verify scenario body count equals scenario_count frontmatter value."

**Acceptance Criteria:** `test-specification-v1.schema.json` updated with cross-field equality constraint OR tspec-analyst explicitly documents "frontmatter scenario_count is treated as informational only; coverage is computed from Scenario block parsing."

---

### IN-003: branches_from_step Field Referenced But Not in Schema [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Type** | Assumption Failure |
| **Section** | tspec-analyst methodology Step 2 / use-case-realization-v1.schema.json |
| **Strategy Step** | Step 3 (Assumption Map) + Step 4 (Stress-Test) |

**Original Assumption:** tspec-analyst's slice-scoped coverage formula correctly references `$.alternative_flows where branches_from_step in slice_steps` -- implying that `alternative_flow` objects have a `branches_from_step` property.

**Inversion:** The `use-case-realization-v1.schema.json` `$defs.alternative_flow` object requires only `id`, `condition`, and `steps`. No `branches_from_step` property exists. The slice-scoped coverage formula in tspec-analyst's methodology references a field (`branches_from_step`) that does not exist in the schema.

**Plausibility:** Certain. Verified by reading `use-case-realization-v1.schema.json` lines 324-348: `alternative_flow` `required: ["id", "condition", "steps"]` -- no `branches_from_step`. The tspec-analyst Step 2 formula `count($.alternative_flows where branches_from_step in slice_steps)` will produce a runtime error or silently return 0 for all alternative flows when used in slice-scoped coverage mode.

**Consequence:** Slice-scoped BDD generation for use cases with alternative flows will either: (a) silently exclude all alternative flows from coverage computation (reporting lower coverage than actual), or (b) cause tspec-analyst to crash/error when attempting to access the non-existent field. Either outcome breaks the slice-scoped generation feature -- which is a documented capability (tspec-generator methodology Step 7: "Slice-Scoped Generation Mode").

**Evidence:** `tspec-analyst.md` methodology Step 2, Slice-scoped coverage formula: `count($.alternative_flows where branches_from_step in slice_steps)`. `use-case-realization-v1.schema.json` `$defs.alternative_flow` properties: `id`, `condition`, `steps` only -- confirmed, no `branches_from_step`.

**Mitigation:** Either (1) add `branches_from_step` as an optional field to `$defs.alternative_flow` in the schema (analogous to `anchor_step` on `extension`), OR (2) revise tspec-analyst's slice-scoped formula to use the `condition` field text for step association (inferring scope from condition content). Option 1 is preferred for schema consistency with `extension.anchor_step`.

**Acceptance Criteria:** Schema updated with `branches_from_step: {type: integer, minimum: 1}` on `alternative_flow` definition, OR tspec-analyst methodology updated with a revised slice-scoped formula that does not reference `branches_from_step`.

---

### IN-004: P-020 vs. Domain Guardrail Conflict Resolution Undefined [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Type** | Anti-Goal |
| **Section** | uc-author and uc-slicer guardrails / SKILL.md |
| **Strategy Step** | Step 2 (Anti-Goals) + Step 4 (Stress-Test) |

**Original Assumption:** When a user explicitly requests an action that violates a domain guardrail (e.g., "skip extensions," "set detail_level to ESSENTIAL_OUTLINE even without extensions"), the agent correctly refuses per domain guardrails and P-022 (no deception about detail level).

**Inversion:** P-020 states "NEVER override user decisions." Domain guardrails state "detail_level_must_match_actual_content_depth: Do not declare ESSENTIAL_OUTLINE if extensions are empty." These two imperatives conflict when the user explicitly instructs "set detail_level to ESSENTIAL_OUTLINE." Neither agent definition nor SKILL.md provides an explicit conflict resolution protocol: which principle takes precedence when the user's explicit instruction contradicts a domain guardrail?

**Plausibility:** High. This is a common user pattern ("just mark it as essential outline, I'll add exceptions later"). Similar conflicts arise for: "set slice_state to PREPARED without test cases," "skip the INVEST assessment," "set realization_level to INTERACTION_DEFINED -- I'll add the interactions manually."

**Consequence:** Inconsistent behavior across sessions. One invocation may refuse and explain the conflict; another may comply and produce an artifact that fails schema validation (allOf constraint: `detail_level ESSENTIAL_OUTLINE requires extensions[] minItems: 1`). If the agent complies, downstream agents (tspec-generator, uc-slicer) receive an artifact that passes structural schema validation but fails allOf semantic validation.

**Evidence:** uc-author guardrails: `detail_level_must_match_actual_content_depth: "Do not declare ESSENTIAL_OUTLINE if extensions are incomplete"` (output_filtering). P-020 forbidden action: `NEVER override user decisions about use case scope, detail level, or actor classification`. H-31: "MUST ask when: (3) destructive or irreversible action implied" -- but setting an incorrect detail_level is not obviously "destructive" from the user's perspective. There is no explicit resolution rule in any document.

**Mitigation:** Add an explicit conflict resolution rule to uc-author and uc-slicer guardrails: "When user instruction conflicts with schema-enforced quality gates (allOf constraints), domain guardrails take precedence over P-020 user authority for schema validity only. Apply H-31: explain the conflict and offer the highest achievable level, not the user-specified level. P-020 applies to scope decisions, not schema validity."

**Acceptance Criteria:** Both uc-author and uc-slicer agent definitions include an explicit "Conflict Resolution Rule" in their `<guardrails>` section that defines priority ordering between P-020 user authority and schema-enforced quality gates. The rule must distinguish scope decisions (P-020 governs) from schema validity decisions (domain guardrail governs).

---

### IN-005: LLM allOf Constraint Self-Verification Reliability [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Type** | Assumption |
| **Section** | uc-author/uc-slicer post-creation verification |
| **Strategy Step** | Step 4 (Stress-Test) |

**Original Assumption:** When uc-author and uc-slicer verify allOf constraints "by systematically checking each constraint," the LLM executes this verification reliably, catching violations before persisting the artifact to disk.

**Inversion:** LLM self-verification of complex conditional JSON Schema allOf constraints is non-deterministic. The 6th allOf constraint (`INTERACTION_DEFINED is not permitted with BRIEFLY_DESCRIBED or BULLETED_OUTLINE`) is a cross-field conditional. Under context pressure (large artifacts, long sessions), LLM self-verification accuracy degrades. An artifact could be written to disk with a violated allOf constraint that would be caught by a deterministic JSON Schema validator but missed by LLM self-review.

**Evidence:** uc-author.md output section: "When `jerry schema validate` becomes available (GH #193), use it for deterministic validation. Until then, verify each constraint explicitly." This explicitly acknowledges that deterministic validation is deferred (GH #193) and LLM self-checking is the current mechanism. uc-slicer.md Step 8: "Before setting `realization_level: INTERACTION_DEFINED`, verify the output artifact's YAML frontmatter satisfies the allOf constraints." This is a behavioral instruction to an LLM, not a deterministic gate.

**Mitigation:** Accelerate GH #193 (`jerry schema validate`) or add a Bash-based validation step: `uv run python -c "import jsonschema, yaml, sys; ..."` as a post-write verification command that agents execute. This converts the LLM self-check into a deterministic validation.

**Acceptance Criteria:** Either (a) GH #193 is implemented and integrated into uc-author/uc-slicer post-creation verification, OR (b) a `uv run`-based JSON Schema validation command is documented in both agent definitions as the preferred verification mechanism with LLM self-check as fallback only.

---

### IN-006: Rejection Artifact Discovery Dependency [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Type** | Assumption |
| **Section** | uc-slicer rejection artifact protocol / orchestration |
| **Strategy Step** | Step 4 (Stress-Test) |

**Original Assumption:** When uc-slicer writes a rejection artifact to `{artifact_path}-rejection.yaml` and halts, the orchestrator or user discovers and acts on the rejection artifact before re-invoking uc-author.

**Inversion:** The rejection artifact protocol is passive -- uc-slicer writes the file and halts. If the main context or orchestrator does not actively check for `{artifact_path}-rejection.yaml` after uc-slicer returns, the rejection information is silently ignored. The user may re-invoke uc-author with the same under-specified request, producing the same BULLETED_OUTLINE artifact, which causes uc-slicer to write the same rejection artifact in an infinite non-progressing loop.

**Evidence:** uc-slicer.md "Rejection Artifact Protocol Step 3: Report to user with both: (a) a human-readable message explaining the failure and the correction path, (b) the path where the rejection artifact was written." The protocol relies on the human-readable message reaching the user -- but in Task tool invocations (orchestrated pipeline), the message is buried in the agent's output. uc-slicer.governance.yaml `on_send`: "On input validation rejection: write structured rejection artifact..." -- but the `on_receive` of the next agent (uc-author) only reads the rejection artifact "if session context includes artifact_path with a corresponding {artifact_path}-rejection.yaml" -- it requires the orchestrator to pass `artifact_path` in the session context.

**Mitigation:** Add an orchestration-level recovery protocol to SKILL.md: "If uc-slicer returns with a rejection (detectable by uc-slicer output message OR by checking `{artifact_path}-rejection.yaml` existence), automatically re-invoke uc-author with `artifact_path` and `target_detail_level: ESSENTIAL_OUTLINE` in session context." The rejection artifact format is already machine-parseable -- the orchestration layer should actively poll and respond.

**Acceptance Criteria:** `/use-case` SKILL.md includes an explicit "Pipeline Recovery Protocol" describing how orchestrators should detect and respond to uc-slicer rejection artifacts, including the specific session context fields to pass to uc-author on recovery invocation.

---

### IN-007: HTTP Status Code Classification Ambiguity [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Type** | Assumption |
| **Section** | cd-generator Step 7 (Extension-to-Error-Response Mapping) |
| **Strategy Step** | Step 4 (Stress-Test) |

**Original Assumption:** cd-generator's semantic pattern analysis of extension condition text produces correct HTTP status code classification (400/401/403/404/409/422/500) for all realistic extension conditions.

**Inversion:** LLM-based semantic classification of extension conditions into HTTP status codes is heuristic and error-prone. Example ambiguities: "record already modified by another user" could map to 409 (conflict) or 422 (unprocessable content). "User does not have required permission" could map to 401 (unauthenticated) or 403 (authorized but forbidden). "Record not found" could map to 404 or 400 if the ID format is also invalid. The `x-error-inference: low` annotation exists for "Unclassified condition -> 422" but not for ambiguous multi-class conditions.

**Evidence:** cd-generator.md Step 7: classification rules list `Conflict/duplicate/state condition -> 409` and `System/internal error condition -> 500` -- these are the most ambiguous categories. No confidence annotation exists for 4xx codes other than the 422 fallback. cd-validator Step 3 checks "HTTP method is semantically consistent" but Step 5 only checks error response existence, not HTTP status code correctness.

**Mitigation:** Add a `x-status-inference: {confidence}` annotation (parallel to `x-method-inference`) to error responses classified with Medium or Low confidence. cd-validator Step 5 should flag responses with `x-status-inference: low` or `medium` for human review, consistent with Step 3's handling of `x-method-inference`.

**Acceptance Criteria:** cd-generator Step 7 updated to annotate ambiguous status code classifications with `x-status-inference: {confidence}`. cd-validator Step 5 updated to flag operations with `x-status-inference: low` or `medium` in the validation report.

---

### IN-008: Empty steps_included Array Edge Case [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Type** | Assumption |
| **Section** | uc-slicer slice creation / tspec-generator slice-scoped mode |
| **Strategy Step** | Step 4 (Stress-Test) |

**Original Assumption:** Slices always have at least one step in `steps_included`, preventing zero-scenario Feature file generation in slice-scoped mode.

**Inversion:** The `slice` definition in `use-case-realization-v1.schema.json` declares `steps_included: {type: array, items: {type: integer}, minItems: 1}` -- correctly enforces minimum 1 step. However, uc-slicer's INVEST assessment and slice creation steps (1-4) are LLM-executed -- an LLM could set `steps_included: [4]` (a single step), and if that step maps to no consumer interaction in Activity 5, tspec-generator in slice-scoped mode produces a Feature file with 0 scenarios for that slice (no basic flow step, no extensions anchored to step 4). The schema enforces minItems: 1 for the array, but does not enforce that the steps resolve to at least one interaction.

**Evidence:** tspec-generator Slice-Scoped Generation Mode: "Filter basic_flow, alternative_flows, and extensions to only those whose anchor step is in `steps_included`." If `steps_included: [4]` and no extensions have `anchor_step: 4`, the filtered result is empty extensions. The Feature file would have 1 scenario (basic flow if step 4 is in basic_flow) or 0 scenarios if step 4 is not in the basic flow at all. The post-creation verification does not check for minimum 1 scenario when in slice-scoped mode.

**Mitigation:** Add to tspec-generator post-creation verification: "If slice-scoped generation, verify that at least 1 Scenario was generated. If 0 scenarios generated, report as a slice definition gap and do not write an empty Feature file -- instead report to user with specific scenario missing guidance."

**Acceptance Criteria:** tspec-generator post-creation verification explicitly checks scenario count > 0 in slice-scoped mode and rejects (does not write) empty Feature files with an actionable error identifying the specific slice and the missing flow coverage.

---

### IN-009: realization_level Set Before interactions[] Populated [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Type** | Assumption |
| **Section** | uc-slicer realization_level derived field protocol |
| **Strategy Step** | Step 4 (Stress-Test) |

**Original Assumption:** uc-slicer always populates `interactions[]` before setting `realization_level: INTERACTION_DEFINED`, as mandated by the Realization Level Derived Field Rule.

**Inversion:** LLM text generation for YAML frontmatter may produce fields in the order the agent writes them -- if the agent writes `realization_level: INTERACTION_DEFINED` as a header field before generating the `interactions:` array content, and the write fails (e.g., context truncation) after writing the field but before writing the array, the artifact on disk has `realization_level: INTERACTION_DEFINED` with no `interactions[]`. This violates allOf constraint 4 but the violation is not detected until the artifact is read again.

**Evidence:** uc-slicer.md "REALIZATION VIOLATION: NEVER set `$.realization_level` without verifying that the corresponding blocks are populated." This is a behavioral instruction. The artifact is written to disk via the Write tool in a single operation -- if the LLM generates the YAML with `realization_level` before `interactions[]`, the allOf violation is in the generated content before the write. uc-slicer.governance.yaml `post_completion_checks`: "verify_interactions_present_when_realization_level_INTERACTION_DEFINED" -- this check fires after writing, so a violation would be detected, but the artifact on disk is already invalid.

**Mitigation:** Add an explicit ordering rule to uc-slicer methodology: "Always write `interactions[]` content BEFORE setting `realization_level: INTERACTION_DEFINED` in the artifact text. Verify `interactions[]` is non-empty BEFORE generating the `realization_level` field in the output YAML." Additionally, post_completion_checks should include a repair action if the verification fails: re-write the artifact with the violation corrected.

**Acceptance Criteria:** uc-slicer methodology updated with explicit YAML field ordering rule: `interactions[]` must be present and non-empty before `realization_level: INTERACTION_DEFINED` is written. Post-completion check failure triggers repair, not just a warning.

---

### IN-010: LLM Complex allOf Constraint Evaluation [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Type** | Assumption |
| **Section** | All agents using use-case-realization-v1.schema.json |
| **Strategy Step** | Step 4 (Stress-Test) |

**Original Assumption:** LLM agents can reliably evaluate all 6 allOf constraints in the schema via in-context reasoning, equivalent to a deterministic JSON Schema validator.

**Inversion:** The 6th allOf constraint uses `then: false` (a schema-level ALWAYS FAIL for the given condition). This pattern is non-trivial for LLMs: `if: {realization_level: INTERACTION_DEFINED} AND {detail_level: BRIEFLY_DESCRIBED or BULLETED_OUTLINE}` then `false`. This means "any artifact with INTERACTION_DEFINED realization and BRIEFLY_DESCRIBED detail level is invalid." An LLM evaluating this may apply forward logic ("if INTERACTION_DEFINED then extensions required") rather than the inverted pattern ("if BRIEFLY_DESCRIBED and INTERACTION_DEFINED then invalid").

**Evidence:** `use-case-realization-v1.schema.json` lines 544-554: the 6th allOf entry uses `"then": false` -- a standard JSON Schema 2020-12 construct for asserting impossibility, but one that requires the evaluator to understand that `false` as a schema means "no instance is valid." All 4 agents that verify allOf constraints (uc-author, uc-slicer, tspec-generator, cd-generator) use LLM in-context reasoning for this check.

**Mitigation:** Same as IN-005 mitigation -- deterministic validation via `jerry schema validate` (GH #193) or inline `uv run python` validation. This finding reinforces that IN-005 should be treated as a systemic issue, not just an uc-author concern.

**Acceptance Criteria:** As IN-005. Deterministic allOf validation is the primary mechanism; LLM self-check is documentation/guidance only.

---

### IN-011: PROTOTYPE Label Removal Creates Validation Obstacle [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Type** | Anti-Goal |
| **Section** | cd-validator Step 7 / contract-design SKILL.md |
| **Strategy Step** | Step 4 (Stress-Test) |

**Original Assumption:** The PROTOTYPE label remains until human review and then is cleanly removed before distribution.

**Inversion:** A developer who has reviewed the contract and is satisfied removes `x-prototype: true` from the YAML manually, then runs cd-validator to get a "clean" report. cd-validator Step 7 fails with a mandatory FAIL: "Contract is missing info.x-prototype: true." The developer is now in a Catch-22: the label must be present for cd-validator to pass, but the label should be removed when the contract is approved.

**Evidence:** cd-validator.md Step 7: "This is a mandatory FAIL -- no override permitted." contract-design SKILL.md: "Neither cd-generator nor cd-validator removes the PROTOTYPE label. That action is a human decision (P-020 user authority)." There is no documented workflow for "post-approval validation" (validation run after PROTOTYPE removal for production-readiness certification).

**Mitigation:** Add a `--skip-prototype-check` flag or a separate "post-approval validation" mode to cd-validator (or document that final production validation is performed by a different tool). Add a note in SKILL.md: "After removing x-prototype: true, use an OpenAPI linter (e.g., Spectral) for structural validation, not cd-validator."

**Acceptance Criteria:** SKILL.md and cd-validator agent definition clarify the expected workflow for post-approval contract validation, acknowledging that cd-validator is a pre-approval tool only.

---

### IN-012: Slice Lifecycle Skipping via User Instruction [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Type** | Anti-Goal |
| **Section** | uc-slicer guardrails / SKILL.md |
| **Strategy Step** | Step 4 (Stress-Test) |

**Original Assumption:** The LIFECYCLE VIOLATION forbidden action ("NEVER skip the SCOPED state") prevents users from requesting direct PREPARED or ANALYZED slice creation.

**Inversion:** This is the same structural conflict as IN-004 but at the slice lifecycle level. The forbidden action prevents agent self-initiated skipping, but does not clarify behavior when the user explicitly requests it. P-020 does not override the forbidden action -- the forbidden action wins -- but this creates an implicit refusal that is undocumented.

**Evidence:** uc-slicer.md forbidden actions: "LIFECYCLE VIOLATION: NEVER skip the SCOPED state." P-020: "NEVER override user decisions about slice boundaries, priority ordering, or lifecycle state transitions." These two can conflict when a user requests "create a PREPARED slice directly."

**Mitigation:** Clarify in the SKILL.md Quick Reference: "uc-slicer cannot skip lifecycle states regardless of user request. If a faster path is needed, INVEST assessment can be expedited but the SCOPED state must still be created."

**Acceptance Criteria:** SKILL.md Quick Reference includes a note about lifecycle state immutability under user instruction.

---

### IN-013: tspec-generator scenario_count Self-Reporting [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Type** | Assumption |
| **Section** | tspec-generator post-creation verification |
| **Strategy Step** | Step 4 (Stress-Test) |

**Original Assumption:** tspec-generator accurately counts Scenario blocks and reports the correct `scenario_count` in the Feature file frontmatter.

**Inversion:** For use cases with many extensions (say, 8 extensions + 3 alternative flows = 12 scenarios), the LLM may miscount during the generation process, especially if scenarios are generated in multiple passes. The post-creation verification checks "One scenario per alternative_flow entry" and "One scenario per extension entry" but does not verify the frontmatter `scenario_count` against the actual block count.

**Evidence:** tspec-generator.governance.yaml post_completion_checks: "verify_scenario_count_equals_coverage_mapped_flows" -- but this is frontmatter-to-frontmatter consistency, not body-to-frontmatter consistency. The actual Scenario block count in the body is not verified against `scenario_count` in the YAML frontmatter.

**Mitigation:** Add to post_completion_checks: "verify_scenario_body_count_equals_frontmatter_scenario_count." This requires parsing the generated file body to count actual Scenario blocks.

**Acceptance Criteria:** tspec-generator.governance.yaml post_completion_checks updated with body-count verification.

---

### IN-014: Unicode Escape Bypass of Banned-Term Check [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Type** | Assumption |
| **Section** | cd-generator Step 1 Layer 2a |
| **Strategy Step** | Step 4 (Stress-Test) |

**Original Assumption:** NFC Unicode normalization in cd-generator's banned-term check prevents all encoding bypass attempts.

**Inversion:** NFC normalization handles composed/decomposed Unicode equivalents (e.g., é as one vs. two code points) but does not translate full-width ASCII variants. "TODO" written as full-width characters `Ｔ` (U+FF34), `Ｏ` (U+FF2F), `Ｄ` (U+FF24), `Ｏ` (U+FF2F) would not be caught by a string match against "TODO" even after NFC normalization, because these are distinct Unicode characters that visually resemble ASCII letters. NFC does not fold ASCII-compatibility characters to ASCII.

**Evidence:** cd-generator.md Step 1 Layer 2a: "Apply NFC normalization and strip non-ASCII whitespace (U+00A0, U+200B, U+FEFF)." Only three specific non-ASCII whitespace variants are stripped. Full-width Latin characters are not addressed. The matching algorithm performs `case-insensitive` matching against the normalized string, but case-insensitivity does not help with character-set differences.

**Mitigation:** Add a Unicode normalization step that includes NFKC (compatibility normalization, which folds full-width and other compatibility variants to their ASCII equivalents) in addition to NFC. NFKC would convert `Ｔ` to `T`, catching full-width bypass attempts.

**Acceptance Criteria:** cd-generator Layer 2a normalization updated to include NFKC normalization before banned-term matching.

---

## Findings Summary

| ID | Assumption / Anti-Goal | Type | Confidence | Severity | Affected Dimension |
|----|------------------------|------|-----------|---------|-------------------|
| IN-001 | Schema-valid artifact bypasses pipeline behavioral controls | Anti-Goal | N/A | Critical | Methodological Rigor |
| IN-002 | scenario_count / mapped_flows frontmatter divergence | Anti-Goal | Low | Critical | Internal Consistency |
| IN-003 | branches_from_step field referenced but absent from schema | Assumption | Certain | Critical | Completeness |
| IN-004 | P-020 vs. domain guardrail conflict resolution undefined | Anti-Goal | N/A | Critical | Methodological Rigor |
| IN-005 | LLM allOf constraint verification reliability | Assumption | Medium | Major | Evidence Quality |
| IN-006 | Rejection artifact discovery dependency | Assumption | Low | Major | Actionability |
| IN-007 | HTTP status code classification ambiguity | Assumption | Low | Major | Evidence Quality |
| IN-008 | Empty steps_included slice edge case | Assumption | Medium | Major | Completeness |
| IN-009 | realization_level set before interactions populated | Assumption | Medium | Major | Internal Consistency |
| IN-010 | LLM complex allOf constraint evaluation | Assumption | Medium | Major | Methodological Rigor |
| IN-011 | PROTOTYPE label removal creates validation obstacle | Anti-Goal | N/A | Minor | Traceability |
| IN-012 | Slice lifecycle skipping via user instruction | Anti-Goal | N/A | Minor | Methodological Rigor |
| IN-013 | tspec-generator scenario_count self-reporting | Assumption | Medium | Minor | Internal Consistency |
| IN-014 | Unicode escape bypass of banned-term check | Assumption | Low | Minor | Evidence Quality |

---

## Step 6: Recommendations

### Critical (MUST Mitigate)

| Finding | Mitigation Action | Acceptance Criteria |
|---------|------------------|---------------------|
| IN-001 | Document pipeline bypass risk in SKILL.md and cd-generator/cd-validator; consider pipeline provenance field | cd-generator input validation guidance states PROTOTYPE label must be present; cd-validator Step 2 audits `created_by` field |
| IN-002 | Add schema cross-field equality constraint OR document tspec-analyst ignores frontmatter for coverage; add body-count post-creation check | `test-specification-v1.schema.json` updated OR tspec-analyst methodology explicitly states body-parsing primacy |
| IN-003 | Add `branches_from_step` field to `$defs.alternative_flow` OR revise slice-scoped formula | Schema updated with `branches_from_step: {type: integer, minimum: 1}` OR formula revised; slice-scoped coverage behavior verified |
| IN-004 | Add explicit conflict resolution rule to uc-author, uc-slicer guardrails distinguishing scope (P-020) from schema validity (domain guardrail) | Both agents include "Conflict Resolution Rule" with explicit priority ordering |

### Major (SHOULD Mitigate)

| Finding | Mitigation Action | Acceptance Criteria |
|---------|------------------|---------------------|
| IN-005 | Accelerate GH #193 (jerry schema validate) or add `uv run python` validation command | Deterministic schema validation integrated into post-creation verification |
| IN-006 | Add Pipeline Recovery Protocol to SKILL.md for rejection artifact discovery | SKILL.md documents orchestrator-side rejection detection and uc-author recovery invocation |
| IN-007 | Add `x-status-inference` confidence annotation; cd-validator Step 5 flags low confidence | cd-generator and cd-validator updated with parallel confidence annotation for error responses |
| IN-008 | Add post-creation check: verify scenario count > 0 in slice-scoped mode | tspec-generator refuses empty Feature files in slice-scoped mode with actionable error |
| IN-009 | Add YAML field ordering rule: interactions[] before realization_level; post-check triggers repair | uc-slicer methodology updated; post-check triggers repair on violation |
| IN-010 | As IN-005 -- deterministic allOf validation; applies to all 4 agents | All 4 agents (uc-author, uc-slicer, tspec-generator, cd-generator) use deterministic allOf validation |

### Minor (MAY Mitigate)

| Finding | Mitigation Action | Acceptance Criteria |
|---------|------------------|---------------------|
| IN-011 | Document post-approval validation workflow in SKILL.md | SKILL.md clarifies cd-validator is pre-approval only |
| IN-012 | Add lifecycle immutability note to SKILL.md Quick Reference | SKILL.md Quick Reference documents lifecycle state enforcement under user instruction |
| IN-013 | Add body-count verification to tspec-generator post_completion_checks | Governance YAML updated |
| IN-014 | Update NFC normalization to NFKC for banned-term check | cd-generator Layer 2a uses NFKC normalization |

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | **Negative** | IN-003 (branches_from_step missing from schema) is a structural completeness gap affecting slice-scoped coverage. IN-008 (empty slice edge case) creates uncovered edge in test generation. |
| Internal Consistency | 0.20 | **Negative** | IN-002 (scenario_count/mapped_flows divergence) and IN-009 (realization_level ordering) create internal consistency violations that can survive to downstream stages. |
| Methodological Rigor | 0.20 | **Negative** | IN-001 (pipeline bypass), IN-004 (P-020/guardrail conflict), IN-010 (allOf LLM evaluation) collectively undermine the methodological guarantees the pipeline claims. These are the most severe findings. |
| Evidence Quality | 0.15 | **Negative** | IN-005 and IN-010 (LLM self-verification) reduce confidence in artifact quality claims. IN-007 (HTTP status code ambiguity) reduces contract evidence quality. |
| Actionability | 0.15 | **Negative** | IN-006 (rejection artifact passive notification) reduces actionability of the pipeline recovery mechanism -- the rejection is written but not actively surfaced to orchestrators. |
| Traceability | 0.10 | **Neutral** | The traceability mechanisms (x-source-interaction, Source annotations, Traceability Matrix) are structurally sound. IN-011 is a minor workflow friction, not a traceability gap. |

**Overall Assessment: REVISE**

4 Critical findings require targeted mitigations before the pipeline can be considered production-ready. The methodology is sound and the assumption-level findings are addressable without architectural changes. The most urgent finding (IN-003: branches_from_step missing) is a schema bug that can be fixed in a single line. The most systemic finding (IN-001: pipeline bypass) requires documentation hardening, not code changes. The pipeline is structurally viable; these findings identify brittleness rather than fundamental design failure.

---

## Execution Statistics

- **Total Findings:** 14
- **Critical:** 4 (IN-001, IN-002, IN-003, IN-004)
- **Major:** 6 (IN-005, IN-006, IN-007, IN-008, IN-009, IN-010)
- **Minor:** 4 (IN-011, IN-012, IN-013, IN-014)
- **Goals Analyzed:** 7 (G-1 through G-7)
- **Anti-Goals Generated:** 7 (AG-1 through AG-7)
- **Assumptions Mapped:** 22 (A-01 through A-22)
- **Protocol Steps Completed:** 6 of 6
- **Assumption Categories Covered:** Technical (11), Process (4), Security (2), Methodological (3), Schema (2)
