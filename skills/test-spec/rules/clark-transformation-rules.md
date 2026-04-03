# Clark Transformation Rules

> **File ID:** F-12 | **Skill:** /test-spec | **Version:** 1.0.0
> **Author:** eng-backend | **Date:** 2026-03-09 | **Criticality:** C3
> **Source:** Clark, T. D. (2018). Generating BDD Test Scenarios from Use Case Specifications.
> **Standard:** H-23 (navigation table required), CB-05 (< 500 lines)
> **Used by:** tspec-generator (loaded via Read tool during transformation)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [1. Input Validation Rules](#1-input-validation-rules) | Pre-transformation guards (RULE-IV-01 through RULE-IV-04) |
| [2. Clark Mapping Rules (Steps 1-7)](#2-clark-mapping-rules-steps-1-7) | Core UC2.0-to-Gherkin algorithm (RULE-C1-01 through RULE-C7-01) |
| [3. Step-Type-to-Clause Rules (SD-07)](#3-step-type-to-clause-rules-sd-07) | actor_action/system_response/validation lookup (RULE-ST-01 through RULE-ST-03) |
| [4. Outcome-Type-to-Scenario Rules (SD-08)](#4-outcome-type-to-scenario-rules-sd-08) | failure/success/rejoin lookup (RULE-OT-01 through RULE-OT-03) |
| [5. Slice-Scoped Generation Rules](#5-slice-scoped-generation-rules) | Slice-filtered scenario generation (RULE-SL-01 through RULE-SL-02) |
| [6. Post-Generation Quality Assurance Rules](#6-post-generation-quality-assurance-rules) | Verification after generation (RULE-QA-01 through RULE-QA-04) |

---

## 1. Input Validation Rules

Apply ALL input validation rules BEFORE beginning any Clark transformation. If any RULE-IV rule fails, halt and produce the specified rejection message. Do NOT generate partial output.

**RULE-IV-01: detail_level gate.**
WHEN `$.detail_level` is `BRIEFLY_DESCRIBED` or `BULLETED_OUTLINE`, REJECT the input with the message: "UC {$.id} is at {$.detail_level}. Clark transformation requires ESSENTIAL_OUTLINE or FULLY_DESCRIBED. Use /use-case to elaborate the use case first." Do NOT proceed to Clark Steps 1-7. Rationale: ESSENTIAL_OUTLINE is the minimum structural completeness for Clark transformation -- it guarantees typed flow steps and at least one extension are present.

**RULE-IV-02: extensions presence gate.**
WHEN `$.extensions` is absent or empty (zero entries), REJECT the input with the message: "UC {$.id} has no extensions. BDD test specifications require at least one extension to generate error scenarios. Use /use-case to add extension conditions." Rationale: A Feature file without error scenarios omits the highest-risk test paths. Clark Step 5 requires at least one extension to generate a meaningful test specification.

**RULE-IV-03: basic_flow step count gate.**
WHEN `$.basic_flow` has fewer than 3 steps, REJECT with: "UC {$.id} basic_flow has {N} steps (minimum 3). The basic flow is insufficient for scenario generation. Use /use-case to elaborate the basic flow." Rationale: The schema enforces a 3-step minimum; a basic_flow with fewer steps cannot produce a meaningful happy path scenario with Given, When, and Then clauses.

**RULE-IV-04: basic_flow step type completeness gate.**
WHEN any `$.basic_flow[*]` step is missing the `.type` field (actor_action, system_response, or validation), REJECT with: "UC {$.id} basic_flow step {N} is missing the type field. Clark transformation requires typed steps. Use /use-case to add step types." Check EVERY step. Rationale: SD-07 maps step types to Gherkin clause types; without the type field, the mapping is undefined and the generated scenario would be ambiguous.

---

## 2. Clark Mapping Rules (Steps 1-7)

Execute these rules in order after all RULE-IV checks pass.

**RULE-C1-01: Identify the Feature from the use case.**
WHEN beginning transformation, map `$.title` to the Gherkin Feature name. The Feature name is verbatim: `Feature: {$.title}`. Do NOT modify or shorten the title. Rationale: Clark Step 1 establishes the 1:1 correspondence between a use case and a Feature file. One use case always produces exactly one Feature block.

**RULE-C2-01: Generate the Feature header with role, goal, and benefit.**
WHEN generating the Feature block header, produce a user story narrative following this format:
```
Feature: {$.title}

  As a {$.primary_actor}
  I want to {goal_verb_phrase}
  So that {benefit_statement}
```
Derive `goal_verb_phrase` from the title (e.g., title "Borrow a Book" -> "borrow a book from the library"). Derive `benefit_statement` from `$.stakeholders[0].interest` if present; otherwise from `$.postconditions.success[0]`. If neither is present, use: "I can complete the {$.title} workflow." Rationale: Clark Step 2 grounds the Feature file in stakeholder value; the As/I want/So that format is standard Gherkin practice for communicating intent.

**RULE-C3-01: Map basic_flow to exactly ONE happy path Scenario.**
WHEN generating the happy path scenario from `$.basic_flow`, combine ALL basic_flow steps into a SINGLE Scenario. Do NOT generate one Scenario per step. The basic flow represents one end-to-end success path; Clark Step 3 produces exactly 1 Scenario from the complete basic flow sequence. Each step maps to a Given/When/Then clause based on its `.type` field (see RULE-ST-01 through RULE-ST-03). Preconditions (if present) map to Given clauses. The trigger (if present) maps to the first When clause. Postconditions.success (if present) map to final Then clauses. Rationale: Clark's algorithm treats the basic flow as an atomic success narrative, not as independent testable units. One end-to-end scenario establishes the happy path as a single verifiable acceptance test.

**RULE-C3-02: Annotate happy path scenario with Source reference.**
WHEN writing the happy path Scenario, add immediately after the Scenario title line:
`**Source:** basic_flow (steps 1-{N})` where N is the count of basic_flow steps.
Rationale: Source annotations enable tspec-analyst to cross-reference every scenario against its source flow element, which is the basis of the C1 Coverage computation.

**RULE-C4-01: Map each alternative_flow to exactly ONE additional Scenario.**
WHEN `$.alternative_flows` contains entries, generate ONE Scenario per alternative flow. For each `$.alternative_flows[N]`:
- Title: `Scenario: {$.title} - {$.alternative_flows[N].name or "Alternative path branches from step {branches_from_step}"}`
- Given clauses: derive from the preconditions PLUS the alternative flow's branching condition (`$.alternative_flows[N].condition`)
- When clauses: derive from the alternative flow's steps
- Then clause: the alternative flow's outcome (whether it rejoins the basic flow or completes separately)
- Source annotation: `**Source:** AF-{NN} (branches_from_step: {N}, condition: "{condition}")`
Rationale: Clark Step 4 maps each alternative flow to a distinct scenario, preserving the distinct path identity while linking it back to the source flow via the branches_from_step reference.

**RULE-C5-01: Map each extension to exactly ONE Scenario using SD-08 outcome lookup.**
WHEN `$.extensions` contains entries, generate ONE Scenario per extension using the outcome-type-to-scenario lookup (see RULE-OT-01 through RULE-OT-03). Do NOT merge multiple extensions into a single Scenario. For each extension, include:
- Title: `Scenario: {$.title} - {$.extensions[N].name or "Error at step {anchor_step}"}`
- Given clauses: preconditions PLUS the extension condition (`$.extensions[N].condition`)
- When clauses: the steps preceding the extension trigger (from basic_flow up to anchor_step)
- Then clauses: derived from the extension's outcome type (see RULE-OT-01 through RULE-OT-03)
- Source annotation: `**Source:** {$.extensions[N].id} (anchor_step: {anchor_step}, outcome: {outcome})`
Rationale: Clark Step 5 mandates one scenario per extension to ensure every exception condition has an explicit acceptance test. Merging extensions would obscure individual error path coverage.

**RULE-C6-01: Derive Given clauses from preconditions and trigger.**
WHEN generating Given clauses for any Scenario, use ONLY `$.preconditions[*]` entries as Given clauses. Format each precondition as: `Given {precondition_text}`. If multiple preconditions exist, use `And {precondition_text}` for subsequent entries. The trigger (`$.trigger`) maps to the FIRST When clause, not a Given clause. If `$.preconditions` is absent, produce a single generic Given clause: `Given the system is in a state where {$.title} can be initiated`. Rationale: Clark Step 6 grounds scenarios in observable preconditions; Given clauses represent system state, not actions.

**RULE-C7-01: Append a Traceability Matrix at the end of the Feature file.**
WHEN all Scenarios have been generated, append a Traceability Matrix section:
```
## Traceability Matrix

| Scenario | Source Flow | Source Step | Type |
|----------|-------------|-------------|------|
| {scenario_name} | {basic_flow / AF-NN / EXT-NN} | {step_number(s)} | {happy_path / alternative / error} |
```
Include one row per Scenario. The Traceability Matrix is the machine-parseable cross-reference that tspec-analyst uses for coverage computation. Rationale: Clark Step 7 establishes the audit trail connecting every scenario to its source, enabling automated coverage verification without requiring parsers to read Gherkin scenario text.

---

## 3. Step-Type-to-Clause Rules (SD-07)

Apply within RULE-C3-01 (basic flow mapping) and RULE-C4-01 (alternative flow mapping). These rules are deterministic lookup entries.

**RULE-ST-01: actor_action step type maps to When clause.**
WHEN a `$.basic_flow[*]` step has `.type = actor_action`, map it to a When clause using the step's `.actor` and `.action` text. Format: `When {$.basic_flow[N].actor} {$.basic_flow[N].action}`. If this is not the first When clause in the scenario, use `And {actor} {action}`. Rationale: SD-07 designates actor_action as the trigger type -- these are user-initiated or external actor actions that drive the scenario forward.

**RULE-ST-02: system_response step type maps to Then clause.**
WHEN a `$.basic_flow[*]` step has `.type = system_response`, map it to a Then clause using the step's `.action` text. Format: `Then the system {$.basic_flow[N].action}`. If this is not the first Then clause in the scenario, use `And the system {action}`. Rationale: SD-07 designates system_response as the observable output type -- these are system-initiated responses that represent the "observable outcome" in Given-When-Then format.

**RULE-ST-03: validation step type maps to Then assertion clause.**
WHEN a `$.basic_flow[*]` step has `.type = validation`, map it to a Then assertion clause. Format: `Then {$.basic_flow[N].action}` (use the action text directly as the assertion). If the action does not already read as an assertion, prepend "the system verifies that" -- for example: step action "checks that the book copy is available" -> `Then the system verifies that the book copy is available`. Rationale: SD-07 designates validation as the assertion type -- these are system checks whose success or failure drives scenario outcome; they must appear as Then clauses to be verifiable.

---

## 4. Outcome-Type-to-Scenario Rules (SD-08)

Apply within RULE-C5-01 (extension mapping). These rules determine the Scenario type and structure based on extension outcome.

**RULE-OT-01: Extension with outcome=failure generates a negative test scenario.**
WHEN an extension has `$.extensions[*].outcome = "failure"`, generate a Scenario that:
- Is titled to indicate failure (e.g., "Borrow a Book - Member card invalid at step 2")
- Has Given clauses from preconditions PLUS the extension condition
- Has When clauses leading to the point where the failure is triggered (basic_flow steps up to anchor_step, plus the extension trigger)
- Has Then clauses asserting the failure outcome: "Then the system rejects the request" AND any specific failure postconditions
- Is annotated as type: `error (failure)` in the Traceability Matrix
Do NOT use the word "fails" in the Scenario title -- use specific domain language ("card invalid", "insufficient funds", "timeout"). Rationale: Failure extensions represent the highest-risk test gaps (P0 priority); they must produce dedicated negative test scenarios that verify error handling is correct.

**RULE-OT-02: Extension with outcome=success generates an alternate success scenario.**
WHEN an extension has `$.extensions[*].outcome = "success"`, generate a Scenario that:
- Is titled to indicate the alternate success path (e.g., "Borrow a Book - Self-service checkout at step 3")
- Has Given clauses from preconditions PLUS the extension condition
- Has When clauses for the extension's steps
- Has Then clauses asserting the alternate success outcome from the extension
- Is annotated as type: `error (alternate success)` in the Traceability Matrix
Rationale: Success extensions represent alternate business paths to goal completion; they require distinct scenarios to verify that the alternate success path produces valid outcomes.

**RULE-OT-03: Extension with outcome=rejoin:{N} generates a rejoin scenario.**
WHEN an extension has `$.extensions[*].outcome` matching the pattern `rejoin:{N}`, generate a Scenario that:
- Is titled to indicate error recovery (e.g., "Borrow a Book - Member provides alternate ID and rejoins at step 1")
- Has Given clauses from preconditions PLUS the extension condition
- Has When clauses for the extension's steps (error recovery actions)
- Has Then clauses asserting: (a) the error recovery completes, (b) "the use case rejoins at step {N} of the main flow"
- Has additional Then clauses for the remaining basic_flow steps from step N onward (mapped using RULE-ST-01 through RULE-ST-03)
- Is annotated as type: `error (rejoin:N)` in the Traceability Matrix
Do NOT treat rejoin outcomes identically to success outcomes. A rejoin scenario must demonstrate both the deviation handling AND the successful resumption from step N. Rationale: The rejoin:{N} pattern encodes error-recovery paths where the system handles a deviation and resumes the main flow at a known point; the generated scenario must demonstrate both the deviation handling and the successful resumption.

---

## 5. Slice-Scoped Generation Rules

Apply ONLY when `slice_id` is provided as an input parameter. When `slice_id = null`, skip these rules and generate a full-UC Feature file.

**RULE-SL-01: Filter flows to slice scope before applying Clark mapping rules.**
WHEN `slice_id` is specified and `$.realization_level >= STORY_DEFINED`, load `$.slices` and identify `$.slices[slice_id].steps_included`. Before applying RULE-C3-01 through RULE-C5-01, filter:
- basic_flow: generate happy path scenario ONLY if any basic_flow step is in `steps_included`
- alternative_flows: include ONLY flows where `branches_from_step` is in `steps_included`
- extensions: include ONLY extensions where `anchor_step` is in `steps_included`
Set the Feature file YAML frontmatter field `slice_id` to the provided slice_id value. Rationale: Slice-scoped generation produces a Feature file targeting a specific implementation increment; only flows relevant to that increment's steps are included, preventing scope creep in the generated test specification.

**RULE-SL-02: Scope coverage denominator to slice flows.**
WHEN generating a slice-scoped Feature file (slice_id != null), set the Feature file YAML frontmatter fields:
- `coverage.total_flows`: count of flow elements WITHIN the slice scope (not the full UC total)
- `coverage.slice_id`: the slice_id value
Do NOT use the full UC flow count as the denominator in the frontmatter. The coverage percentage reported in L0 summary must be computed as: `mapped_scenarios / slice_scoped_total_flows`. Rationale: Coverage computed against the full UC flow count would always appear low for a slice-scoped Feature file, misleading users into thinking coverage is inadequate when it is in fact complete for the targeted implementation increment.

---

## 6. Post-Generation Quality Assurance Rules

Apply AFTER completing Clark Steps 1-7. These rules verify the generated Feature file before it is written to disk.

**RULE-QA-01: Verify 1:1 cardinality between flow elements and Scenarios.**
WHEN all Clark mapping steps are complete, count:
- Expected happy path scenarios: 1 (always -- from basic_flow)
- Expected alternative flow scenarios: count(`$.alternative_flows`) within scope
- Expected extension scenarios: count(`$.extensions`) within scope
- Total expected: 1 + alt_count + ext_count
- Actual generated Scenario count in Feature file: N

IF actual_count != expected_count: FLAG the discrepancy with specific details on which flow elements were not mapped. Do NOT write the Feature file until the discrepancy is resolved or documented with a reason (e.g., extension with invalid outcome was flagged and user was notified). Rationale: The 1:1 cardinality guarantee is the core contract of Clark transformation; violation means some flow elements have no test coverage.

**RULE-QA-02: Verify every Scenario has a Source annotation.**
WHEN verifying the generated Feature file, check that every Gherkin Scenario block contains a `**Source:**` annotation line immediately after the Scenario title. If any Scenario is missing a Source annotation, add it before writing the file. Rationale: Source annotations are the machine-parseable traceability markers that tspec-analyst uses for coverage computation; missing annotations degrade coverage report accuracy.

**RULE-QA-03: Verify Traceability Matrix completeness.**
WHEN verifying the Feature file, confirm the Traceability Matrix has exactly one row per Scenario. If any Scenario is missing from the matrix, add it. Rationale: The Traceability Matrix provides the audit trail; gaps in the matrix break the tspec-analyst coverage cross-reference algorithm.

**RULE-QA-04: Report generation summary before writing file.**
WHEN all verification checks pass, report:
- Feature file path (where it will be written)
- Scenario count breakdown: happy_path=1, alternative_flows=N, extensions=M, total=1+N+M
- Coverage ratio: (1+N+M) / total_mappable_flows (should be 1.0 if no flows were skipped)
- Any warnings (absent preconditions, absent postconditions, unmappable extensions)
Then write the file. Rationale: Reporting before writing gives the user an opportunity to abort if the summary reveals unexpected content (e.g., zero extensions mapped means no error scenarios).

---

*Rules Version: 1.0.0*
*Author: eng-backend | Date: 2026-03-09*
*Minimum rule count satisfied: 20 rules (4 IV + 7 C + 3 ST + 3 OT + 2 SL + 4 QA = 23, exceeding minimum of 19)*
*Target file size: < 500 lines (CB-05 compliant)*
*Reference: Clark (2018) UC2.0-to-Gherkin mapping algorithm, SD-07, SD-08*
