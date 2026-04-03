# Pre-Mortem Report: /use-case, /test-spec, and /contract-design Skills

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverable:** Three linked skill definitions -- /use-case (uc-author, uc-slicer), /test-spec (tspec-generator, tspec-analyst), /contract-design (cd-generator, cd-validator)
**Criticality:** C4
**Date:** 2026-03-12T00:00:00Z
**Reviewer:** adv-executor (S-004)
**H-16 Compliance:** S-003 Steelman output confirmed at `projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/verification/adversary-skill-findings.md` (prior tournament round)
**Failure Scenario:** It is September 2026. The /use-case, /test-spec, and /contract-design skills have been in the Jerry framework for six months. Adoption is near zero. Teams that attempted the pipeline abandoned it within two sessions. The framework council is reviewing whether to deprecate all three skills. The post-mortem team meets to determine exactly what went wrong.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall risk assessment and recommendation |
| [Findings Table](#findings-table) | All failure causes with priority ranking |
| [Detailed Findings](#detailed-findings) | Evidence and mitigation for each Critical and Major finding |
| [Recommendations](#recommendations) | P0/P1/P2 mitigation plan |
| [Scoring Impact](#scoring-impact) | S-014 dimension assessment |
| [Execution Statistics](#execution-statistics) | Finding counts and protocol completion |

---

## Summary

The three-skill pipeline (/use-case -> /test-spec -> /contract-design) has sophisticated internal methodology but twelve concrete failure causes that would combine to produce near-zero adoption in production. The most critical failure is the pipeline's dependency chain: each skill has strict input prerequisites that the prior skill must satisfy, but there is no orchestrator-level health check or graceful guidance when a user enters the pipeline in the middle. The second most critical failure is the accumulation of LLM behavioral drift across the six-agent pipeline -- each agent makes probabilistic decisions about schema fields, step types, and interaction roles; small early errors compound to rejection at every downstream gate. A systemic failure mode exists across all three skills: the shared `use-case-realization-v1.schema.json` schema is a single point of failure -- any schema change breaks all three skills' input validators simultaneously, and there is no versioning or migration path. Users would abandon the skills because the effort-to-reward ratio is punishing: a use case that should take five minutes requires mastering Cockburn 12-step + Jacobson UC 2.0 + Clark transformation + OpenAPI 3.1, with each gate capable of blocking the entire pipeline. The overall recommendation is **REVISE**: the skills require targeted mitigation of P0 findings (particularly the inter-skill failure propagation mechanism and the rejection artifact design) before production confidence can be justified.

---

## Findings Table

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-001-20260312 | Pipeline entry-point blindness: users invoke tspec-generator or cd-generator directly without knowing uc-author must run first at ESSENTIAL_OUTLINE; each downstream agent rejects with actionable error but offers no guided path back up the chain | Process | High | Critical | P0 | Completeness |
| PM-002-20260312 | LLM semantic drift in step type classification: uc-author's `type` field (actor_action, system_response, validation) is an LLM judgment call with no external ground truth; wrong classifications propagate directly into tspec-generator Clark mapping and break Given/When/Then generation | Technical | High | Critical | P0 | Internal Consistency |
| PM-003-20260312 | Shared schema single point of failure: `use-case-realization-v1.schema.json` is consumed by all three skills; breaking change in one part of the schema (e.g., adding a required field) forces simultaneous update of all six agents and all existing artifacts | Assumption | High | Critical | P0 | Methodological Rigor |
| PM-004-20260312 | Rejection artifact protocol creates silent pipeline stalls: uc-slicer writes a rejection artifact to `{artifact_path}-rejection.yaml` and halts, but if the orchestrator (or user) does not check for this file, the pipeline appears to have completed successfully with no output -- zero-output sessions are indistinguishable from incomplete sessions | Technical | High | Major | P1 | Internal Consistency |
| PM-005-20260312 | The cd-generator's `x-prototype: true` PROTOTYPE label has no automated removal path -- it is explicitly a human-only action (P-020), but the skill documentation provides no ceremony for the handoff review; in practice PROTOTYPE labels will be left in place indefinitely, making every generated contract permanently marked as unreviewed | Process | High | Major | P1 | Actionability |
| PM-006-20260312 | uc-slicer Activity 5 is prerequisite to cd-generator but Activity 5 is not the default activity -- most slicing invocations stop at Activity 4 (PREPARED state); the result is that cd-generator receives STORY_DEFINED artifacts and rejects them, sending users back through uc-slicer with a non-obvious error about `realization_level = INTERACTION_DEFINED` | Process | High | Major | P1 | Completeness |
| PM-007-20260312 | tspec-analyst's coverage target for SUBFUNCTION goal level is 80% in the SKILL.md but the test-specification-v1.schema.json comment says "SUBFUNCTION=80%" while the agent methodology says "SUBFUNCTION: 100%"; this contradiction means coverage reports will show PASS or FAIL depending on which source the LLM loads first | Technical | Medium | Major | P1 | Internal Consistency |
| PM-008-20260312 | The banned-term check in cd-generator (Layer 2a) uses a substring match against a hard-coded list, but `request_description` has only a 20-character minimum; legitimate short descriptions (e.g., "Member submits book return") are 29 characters and may contain words like "pending" in context that trigger false-positive REJECT | Technical | Medium | Major | P1 | Evidence Quality |
| PM-009-20260312 | No skill supports iterative refinement: if a user produces an ESSENTIAL_OUTLINE UC artifact and then edits it to fix an error, uc-slicer must re-run Activities 2, 4, and 5 from scratch; the skill specifications do not define an idempotent update path -- partial re-runs corrupt the `$.slices[]` and `$.interactions[]` arrays | Process | Medium | Major | P1 | Methodological Rigor |
| PM-010-20260312 | The JERRY_PROJECT environment variable fallback path (`work/...`) is silently invoked when JERRY_PROJECT is not set, but JERRY_PROJECT is defined as a HARD constraint (H-04) in the framework; the existence of a fallback contradicts the HARD rule and will cause artifacts to land in `work/` when the skill is invoked without a session -- discovered only when users cannot find their output | Assumption | Medium | Minor | P2 | Traceability |
| PM-011-20260312 | The five-state slice lifecycle (SCOPED > PREPARED > ANALYZED > IMPLEMENTED > VERIFIED) mixes UC authoring states with worktracker implementation states; IMPLEMENTED and VERIFIED are documented as "managed via external worktracker Story entity" -- but the SKILL.md contains no guidance on when or how to transition slices from ANALYZED to IMPLEMENTED, leaving users with slices permanently stuck at ANALYZED | Process | Low | Minor | P2 | Completeness |
| PM-012-20260312 | The cd-generator uses `model: opus` for a C4-classified novel algorithm but the cognitive_mode in governance YAML is "systematic" (not "convergent" as stated in the agent .md file) -- this inconsistency between `.md` and `.governance.yaml` cognitive_mode fields means routing decisions based on governance YAML will misclassify the agent's reasoning style | Technical | Low | Minor | P2 | Traceability |

---

## Detailed Findings

### PM-001-20260312: Pipeline Entry-Point Blindness [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | /use-case SKILL.md Integration Points; /test-spec Input Requirements; /contract-design Input Requirements |
| **Strategy Step** | Step 3 -- Process failures lens |

**Evidence:**

The /use-case SKILL.md documents downstream consumption readiness:
```
| /test-spec (tspec-generator) | detail_level >= ESSENTIAL_OUTLINE | $.basic_flow[*].type, $.extensions[] |
| /contract-design (cd-generator) | realization_level = INTERACTION_DEFINED | $.interactions[] |
```

The /test-spec Input Requirements section states: "Use case artifact must satisfy ALL of the following." The /contract-design skill states: "NEVER invoke this skill when: Use case artifact does not have an interactions block."

The /contract-design SKILL.md "When to Use" section specifies exactly which pre-condition uc-slicer Activity 5 must satisfy. However, none of the three SKILL.md files document a unified onboarding path that describes what a brand-new user should do first, second, and third. The trigger map entry in mandatory-skill-usage.md for `/contract-design` contains the negative keyword "write use case" -- so a user who types "write a use case and generate an API contract" would have the contract routing suppressed, but then when they invoke `/contract-design` directly, they receive a REJECT with no indication that uc-author must have run first.

**Analysis:**

The pipeline is designed in producer-consumer fashion (shared schema, filesystem-mediated artifacts) which is architecturally clean but user-hostile. When a user enters at any downstream skill, they receive a well-structured REJECT message -- but that message terminates their session. There is no skill-level "wizard mode" that guides the user through the pipeline from the beginning. The error messages say "use /use-case to elaborate first" but do not invoke or offer to invoke /use-case. In production, users who encounter two sequential REJECT sessions typically abandon the skill rather than re-read documentation.

**Recommendation:**

Add a "Pipeline Quick Check" section to each downstream skill's SKILL.md that lists the exact verification commands to confirm upstream prerequisites are met before invoking the skill. More critically: modify the REJECT messages in tspec-generator and cd-generator to include a two-sentence offer: "Would you like me to invoke /use-case to produce the prerequisite artifact first? If yes, provide the actor goal and domain." This requires no architectural change -- just message content revision in the agent guardrails sections.

**Acceptance Criteria:** Each REJECT message in tspec-generator and cd-generator includes a specific proactive offer to invoke the upstream skill, with the exact information needed.

---

### PM-002-20260312: LLM Semantic Drift in Step Type Classification [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | uc-author agent `<methodology>` Step 5; use-case-realization-v1.schema.json `$defs.flow_step.type` |
| **Strategy Step** | Step 3 -- Technical failures lens |

**Evidence:**

The `flow_step` schema defines `type` as:
```json
"enum": ["actor_action", "system_response", "validation"]
```

The uc-author methodology Step 5 says "Write the full basic flow (3-9 steps, typed)" with the three type values. The Clark transformation (tspec-generator Step 4) maps these mechanically:
```
$.basic_flow[*].type = actor_action -> When {$.actor} {$.action}
$.basic_flow[*].type = system_response -> Then {$.action}
$.basic_flow[*].type = validation -> Then {$.action} (as assertion)
```

The tspec-generator guardrails include: "REJECT: 'UC {id} basic_flow step {N} is missing the type field.'" -- but there is no REJECT for semantically wrong type values. A step like "System confirms the loan is recorded" labeled as `actor_action` instead of `system_response` will generate `When System confirms the loan is recorded` (a When clause) instead of `Then the loan is confirmed` (a Then clause) -- producing a grammatically valid but semantically inverted BDD scenario.

**Analysis:**

Type classification is a judgment call by uc-author at authoring time, performed by an LLM. There is no external ground truth. The schema validates that a `type` value is present and is one of the three enums -- it cannot validate semantic correctness. Across a six-step use case, even one misclassified step produces a Gherkin scenario that violates Given-When-Then conventions. The tspec-analyst 7 Cs framework checks "C5: Consistent Structure -- All scenarios follow Given-When-Then" but does so by examining the Feature file, not by cross-referencing against step types in the source UC. A systematically wrong step type will produce a consistently wrong structure that passes C5.

**Recommendation:**

Add a post-output verification step to uc-author that pattern-checks each flow step's type against the action's grammatical subject: if the `actor` is "System" and `type` is `actor_action`, emit a warning (not a REJECT, since the user may intend a system-as-actor action). Add a complementary check in tspec-generator that validates the generated Given/When/Then sequence follows the expected actor-system-actor alternation pattern and warns when consecutive When or Then clauses appear.

**Acceptance Criteria:** uc-author warns when `type = actor_action` is combined with `actor = System`. tspec-generator warns when the generated scenario has two consecutive When clauses or two consecutive Then clauses from different source steps.

---

### PM-003-20260312: Shared Schema Single Point of Failure [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | All three skills SKILL.md Integration Points; `docs/schemas/use-case-realization-v1.schema.json` |
| **Strategy Step** | Step 3 -- Assumption failures lens |

**Evidence:**

The schema `$id` is `https://jerry-framework.dev/schemas/use-case-realization/v1.0.0`. The `additionalProperties: false` constraint at the root level means any field added to the schema becomes a breaking change for all existing artifacts. Both uc-author and uc-slicer reference the schema for validation. tspec-generator references it for input validation. cd-generator references it for input validation. The schema defines `"required": ["id", "title", "work_type", "version", "status", "goal_level", "goal_symbol", "primary_actor", "detail_level", "trigger", "preconditions", "postconditions", "basic_flow", "created_at", "created_by"]` -- 15 required fields.

No schema version negotiation mechanism is documented. The uc-author `<output>` section says: "When `jerry schema validate` becomes available (GH #193), use it for deterministic validation. Until then, verify each constraint explicitly." GH #193 is an open issue -- the deterministic validation tool does not exist.

**Analysis:**

The three skills share `use-case-realization-v1.schema.json` as a coordination contract. The schema is frozen at v1.0.0 by its `$id`. Any extension -- a new required field, a modified enum, a changed pattern -- breaks: (1) all existing UC artifacts, (2) all three skills' input validators, (3) the test-specification-v1.schema.json (which derives `source_detail_level` from UC schema enum values). The `additionalProperties: false` constraint prevents forward-compatible extension -- adding any new field to a UC artifact in a newer version causes all older consumers to reject it. The combination of no validation tooling (GH #193 open), frozen schema, and additionalProperties: false creates a brittle coordination point that will fracture under the first schema evolution requirement.

**Recommendation:**

Establish a documented schema evolution policy: (1) `additionalProperties: false` should be `additionalProperties: true` (or a specific allowance for vendor extensions prefixed with `x-`) to permit forward-compatible addition without breaking consumers; (2) define a schema version negotiation protocol (e.g., artifacts carry `schema_version: "1.0.0"` and agents validate `schema_version` against their supported range); (3) prioritize GH #193 (`jerry schema validate`) as a prerequisite to production confidence.

**Acceptance Criteria:** Schema allows forward-compatible field additions without breaking existing consumers. Schema version negotiation is documented with supported version ranges per agent. GH #193 timeline is defined.

---

### PM-004-20260312: Rejection Artifact Protocol Creates Silent Pipeline Stalls [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | uc-slicer `<methodology>` Rejection Artifact Protocol; uc-author `<methodology>` Rejection Artifact Check |
| **Strategy Step** | Step 3 -- Technical failures lens |

**Evidence:**

From uc-slicer methodology:
```
4. HALT -- do not proceed to Step 2 under any circumstances.
```

The rejection artifact is written to `{artifact_path}-rejection.yaml`. The uc-slicer reports to the user: "The path where the rejection artifact was written: {artifact_path}-rejection.yaml." However, in an automated orchestration context (where uc-slicer is invoked via Task tool), the orchestrator checks the artifact's output path for a `.md` file -- the rejection artifact is a `.yaml` file at a different path. There is no structured handoff mechanism that signals "rejection occurred" through the `on_send` session context -- the `on_send` section says "Report artifact path, slice count, and realization level achieved" and "On input validation rejection: write structured rejection artifact..." but the latter is documentation of the side effect, not a machine-readable failure signal in the handoff schema.

**Analysis:**

The rejection artifact is a machine-readable correction mechanism between uc-slicer and uc-author. This is architecturally sound for the two-agent case. The failure mode is in multi-turn or orchestrated scenarios: if the orchestrator invokes uc-slicer, uc-slicer halts and writes a rejection artifact, and the orchestrator's success check looks at "did a `.md` file appear at the expected output path?" -- the answer is no, but the check may also report no error because uc-slicer technically completed its run. The orchestrator sees a completed agent invocation with no output file, which it may interpret as "no slice needed" rather than "slice was rejected." The distinction is observable only by reading the agent's human-readable output or checking for the `-rejection.yaml` file explicitly.

**Recommendation:**

Add an explicit failure signal to the `on_send` session context for rejection cases: e.g., `rejection_occurred: true`, `rejection_artifact_path: "{path}"`, `rejection_reason: "{code}"`. This enables orchestrators to detect rejection programmatically without parsing human-readable output. Update the handoff schema documentation to declare this as a structured field.

**Acceptance Criteria:** uc-slicer on_send includes a machine-readable rejection indicator when input validation fails. Orchestration composition files document how to check for and handle rejection signals.

---

### PM-005-20260312: PROTOTYPE Label Has No Automated Removal Path [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | /contract-design SKILL.md "Output Quality Gate"; cd-generator `<output>` section |
| **Strategy Step** | Step 3 -- Process failures lens |

**Evidence:**

From /contract-design SKILL.md:
```
The PROTOTYPE label (x-prototype: true) remains on all contracts until:
1. cd-validator produces a PASS verdict on all 9 checks
2. A human reviewer confirms semantic correctness of the contract
3. The reviewer explicitly removes the x-prototype: true label

Neither cd-generator nor cd-validator removes the PROTOTYPE label. That action is a human decision (P-020 user authority).
```

There is no documented procedure for how a human reviewer performs step 3, no review checklist, no record-keeping mechanism for when the label was removed and by whom. The validation report (`-validation.md`) documents that cd-validator PASS was achieved but does not record the reviewer's identity or the date of human review sign-off.

**Analysis:**

The PROTOTYPE label is a safety gate that prevents production use of unreviewed contracts. The gate is justified (G-01: novel algorithm, no prior art). However, the removal ceremony is entirely undocumented. In practice, organizations that encounter a `x-prototype: true` label without an established removal process will do one of two things: (1) remove the label immediately upon cd-validator PASS without human review, defeating the safety gate, or (2) never remove the label, keeping all contracts permanently marked as prototypes. Both outcomes are failures. The absence of a review checklist and sign-off record means the human review step has no enforcement mechanism and no audit trail.

**Recommendation:**

Add a "PROTOTYPE Review Checklist" section to the /contract-design SKILL.md that defines: (a) what a human reviewer must verify (semantic correctness of HTTP method inference, resource naming, error response semantics), (b) the format for recording sign-off (e.g., a comment block in the OpenAPI YAML: `x-prototype-reviewed-by: {name}`, `x-prototype-reviewed-at: {ISO-8601}`), and (c) the procedure for removing `x-prototype: true` after sign-off.

**Acceptance Criteria:** A PROTOTYPE Review Checklist exists in /contract-design SKILL.md. The sign-off format is documented and produces a reviewable audit record.

---

### PM-006-20260312: Activity 5 Prerequisite Is Non-Default and Non-Obvious [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | /use-case SKILL.md "Downstream Consumption Readiness"; cd-generator Input Requirements |
| **Strategy Step** | Step 3 -- Process failures lens |

**Evidence:**

From /use-case SKILL.md:
```
| /contract-design (cd-generator) | realization_level = INTERACTION_DEFINED | $.interactions[] |
```

From uc-slicer methodology, Activities 2 and 4 bring the artifact to STORY_DEFINED (slices created, test cases defined). Activity 5 is "Analyze a Slice" and produces the `$.interactions[]` block, advancing to INTERACTION_DEFINED. The default invocation in common workflows is "Slice use case into increments" which maps to Activities 2+4 only. Activity 5 is listed separately as part of the "Full realization pipeline" workflow.

From the /use-case SKILL.md Quick Reference:
```
| Slice use case into increments | uc-slicer (Activities 2+4) | 2-4 minutes |
| Full realization pipeline | uc-author (ESSENTIAL_OUTLINE) -> uc-slicer (Activities 2+4+5) | 5-10 minutes |
```

The typical "slice" workflow produces STORY_DEFINED, not INTERACTION_DEFINED. cd-generator explicitly REJECTs STORY_DEFINED input with: "Use /use-case (uc-slicer Activity 5) to identify system boundaries first."

**Analysis:**

A user who follows the natural progression -- write use case, slice it, generate contract -- will invoke uc-slicer with Activities 2+4 (the default), obtain a STORY_DEFINED artifact, then invoke cd-generator and receive a REJECT. The REJECT message is correct and actionable, but it requires a third uc-slicer invocation specifically for Activity 5. Most users will not know Activity 5 exists until they hit this error. This creates a predictable friction point that produces a three-step correction cycle: (1) invoke uc-slicer (Activities 2+4), (2) receive REJECT from cd-generator, (3) invoke uc-slicer again (Activity 5 only). None of the Natural Language Invocation examples in the SKILL.md demonstrate Activity 5.

**Recommendation:**

Add a Natural Language Invocation example for Activity 5 specifically in the /use-case SKILL.md. Add a warning to the "Slice use case into increments" quick reference entry: "(Activities 2+4 only -- run Activity 5 additionally if /contract-design consumption is needed)". In cd-generator's REJECT message for STORY_DEFINED input, include the exact invocation: `Use uc-slicer with activity: 5 on the existing artifact.`

**Acceptance Criteria:** The /use-case SKILL.md includes at least one Activity 5 Natural Language Invocation example. The cd-generator REJECT message for STORY_DEFINED input includes the exact corrective command.

---

### PM-007-20260312: Coverage Target Contradiction Between SKILL.md and Agent Methodology [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | /test-spec SKILL.md "7 Cs Quality Framework"; tspec-analyst `<methodology>` Step 5 |
| **Strategy Step** | Step 3 -- Technical failures lens |

**Evidence:**

From /test-spec SKILL.md, the 7 Cs Quality Framework table:
```
| C1: Coverage | Primary -- mapped_scenarios / total_mappable_flows |
```
No coverage targets by goal level are listed in the SKILL.md.

From tspec-analyst `<methodology>` Step 5:
```
Coverage targets by goal level:
- USER_GOAL: 100% (core use cases must have complete BDD coverage)
- SUMMARY: 80%+ (summary-level UCs may have abstract flows not directly BDD-mappable)
- SUBFUNCTION: 100% (granular functions; complete coverage achievable and expected)
```

From the `test-specification-v1.schema.json` property `source_goal_level` description:
```
"Determines coverage target: USER_GOAL=100%, SUBFUNCTION=80%, SUMMARY=60%."
```

The tspec-analyst methodology says SUBFUNCTION=100%; the schema documentation says SUBFUNCTION=80%. Additionally, the schema says SUMMARY=60% but the methodology says SUMMARY=80%+. Two of the three targets differ between documents.

**Analysis:**

Coverage target contradictions between the agent methodology (what the LLM loads at runtime) and the schema documentation (the authoritative data contract) mean that tspec-analyst will apply different thresholds depending on which source it encounters first or prioritizes. A SUBFUNCTION use case that achieves 85% coverage will PASS per the schema documentation (80% threshold) but FAIL per the agent methodology (100% threshold). Coverage reports for SUMMARY use cases will similarly flip based on whether the 60% (schema) or 80% (methodology) threshold applies. This is an unresolvable ambiguity until the source of truth is designated and the contradiction is corrected.

**Recommendation:**

Designate the tspec-analyst `<methodology>` section as the authoritative source of truth for coverage targets, update the schema description field to match, and add the explicit coverage targets to the /test-spec SKILL.md. The targets themselves should be reviewed for consistency with industry norms (100% for SUBFUNCTION is appropriate; 80%+ for SUMMARY is appropriate).

**Acceptance Criteria:** Coverage targets match exactly between tspec-analyst methodology, test-specification schema descriptions, and /test-spec SKILL.md. A single authoritative table exists.

---

### PM-008-20260312: Banned-Term Check May False-Reject Legitimate Short Descriptions [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | cd-generator `<methodology>` Step 1 Layer 2a; use-case-realization-v1.schema.json `$defs.interaction.request_description` |
| **Strategy Step** | Step 3 -- Technical failures lens |

**Evidence:**

From the schema, `request_description` has `"minLength": 20`. The banned-term check Layer 2a rule:
```
2. If any SUBSTRING_TERMS appears as a word-boundary match in description
   AND description total length < 60 characters:
   REJECT -- short description dominated by placeholder language.
```

SUBSTRING_TERMS includes `"pending"`. A legitimate description such as "Member submits a loan request for a pending return item" (55 characters) would match the pattern: "pending" appears as a word-boundary match, and the description is under 60 characters. The description is semantically meaningful but would be REJECTED.

Additionally, SUBSTRING_TERMS includes `"execute"` (from the broader verb list context) -- though not explicitly in the banned list shown, the banned list includes terms that overlap with legitimate domain vocabulary in some domains (e.g., "process", "handle", "perform" if they appeared in the list). The combination of substring matching with a short-description threshold creates false positive risk for concise but legitimate descriptions.

**Analysis:**

The 60-character cutoff for substring matching was designed to catch descriptions like "pending" (7 characters -- clearly a placeholder). However, 60 characters is under the threshold for many valid short descriptions that happen to contain banned-adjacent words. The check has no mechanism to distinguish "pending" as a standalone placeholder from "pending" as a domain noun (e.g., "pending approval"). The word-boundary match (`\bpending\b`) would match both. A false REJECT at this layer forces the user back to uc-slicer Activity 5 to rewrite a description that was substantively correct.

**Recommendation:**

Raise the short-description threshold from 60 to 40 characters (making it catch only very short descriptions), and add domain-context exclusions: if the substring match term appears adjacent to a domain noun (identifiable by POS tagging or a whitelist of prepositions like "for", "in", "of", "with"), reclassify as a WARN rather than REJECT. Alternatively, limit REJECT to EXACT_MATCH_TERMS only, and reclassify all SUBSTRING_TERM matches as WARN with the `x-description-quality: low` annotation (already defined in Layer 2b).

**Acceptance Criteria:** The banned-term REJECT threshold is revised with documented rationale. At least one test case in BEHAVIOR_TESTS.md covers the false-positive case (e.g., "pending" in a meaningful context).

---

### PM-009-20260312: No Idempotent Update Path for Artifacts Under Iteration [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | uc-slicer `<methodology>` 8-Step Slicing Methodology; uc-author `<methodology>` Rejection Artifact Check |
| **Strategy Step** | Step 3 -- Process failures lens |

**Evidence:**

uc-slicer Step 4 says: "Create slice definitions: `slice_id` (UC-{DOMAIN}-{NNN}-S{N}), `title`, `steps_included`, `invest_assessment`; set `slice_state: SCOPED`." The methodology does not define behavior when `$.slices` already contains entries from a prior uc-slicer invocation. Step 2 says "Identify slice candidates" without specifying whether to merge with, replace, or extend existing slices.

uc-author's methodology defines the rejection artifact check for elaboration scenarios. However, the methodology also says: "Load `skills/use-case/rules/use-case-writing-rules.md` progressively per detail level target" -- but does not define what happens when re-running uc-author against an already-ESSENTIAL_OUTLINE artifact that the user wants to modify.

**Analysis:**

The three-skill pipeline produces artifacts that accumulate fields over multiple agent invocations. When a user needs to fix an error in the basic flow after uc-slicer has already produced slices, they must: (1) edit the artifact manually or via uc-author, (2) re-run uc-slicer -- but uc-slicer does not define whether it replaces existing slices or appends new ones. Appending produces duplicate slices; replacing loses slice state metadata (INVEST assessments, test cases). Neither outcome is correct. The schema `additionalProperties: false` on the interaction object further constrains updates -- a user who needs to fix an interaction description must understand YAML editing conventions.

**Recommendation:**

Define an explicit re-invocation protocol for uc-slicer: when `$.slices` is non-empty at invocation time, prompt the user: "Existing slices detected (SCOPED: N, PREPARED: M, ANALYZED: P). Re-run from scratch (replaces all) or add new slices for flow changes since last run?" Document this in the uc-slicer `<methodology>` section. Add a corresponding section to the /use-case SKILL.md under "Common Workflows" for "Updating an existing use case after slicing."

**Acceptance Criteria:** uc-slicer explicitly handles the re-invocation case with user-guided options. The /use-case SKILL.md documents the update workflow.

---

## Recommendations

### P0 Findings (Critical -- MUST mitigate before acceptance)

| ID | Mitigation | Acceptance Criteria |
|----|-----------|---------------------|
| PM-001-20260312 | Add proactive upstream skill invocation offers to all downstream REJECT messages | Each REJECT in tspec-generator and cd-generator offers to invoke upstream skill |
| PM-002-20260312 | Add step type semantic validation warnings to uc-author and structural pattern warnings to tspec-generator | uc-author warns on system-as-actor with actor_action; tspec-generator warns on consecutive same-type clauses |
| PM-003-20260312 | Relax schema additionalProperties to allow forward-compatible extension; add schema version negotiation; prioritize GH #193 | Schema allows field additions without breaking consumers; version ranges documented |

### P1 Findings (Important -- SHOULD mitigate)

| ID | Mitigation | Acceptance Criteria |
|----|-----------|---------------------|
| PM-004-20260312 | Add machine-readable rejection signal to uc-slicer on_send session context | on_send includes rejection_occurred, rejection_artifact_path, rejection_reason fields |
| PM-005-20260312 | Document PROTOTYPE Review Checklist and sign-off format in /contract-design SKILL.md | Checklist exists; sign-off format produces audit record |
| PM-006-20260312 | Add Activity 5 invocation example to /use-case SKILL.md; enhance cd-generator REJECT message | Activity 5 example present; REJECT message includes exact corrective command |
| PM-007-20260312 | Reconcile coverage targets across tspec-analyst methodology, schema description, and SKILL.md | Single consistent coverage target table exists across all three sources |
| PM-008-20260312 | Revise banned-term REJECT threshold and add BEHAVIOR_TESTS.md false-positive test case | 40-character threshold with domain-context exception; test case in BEHAVIOR_TESTS.md |
| PM-009-20260312 | Define re-invocation protocol for uc-slicer when slices already exist | Re-invocation protocol documented in uc-slicer methodology and SKILL.md |

### P2 Findings (Monitor -- MAY mitigate; acknowledge risk)

| ID | Risk Acknowledgment | Monitoring Approach |
|----|---------------------|---------------------|
| PM-010-20260312 | JERRY_PROJECT fallback path contradicts H-04 HARD rule; resolve by removing fallback or adding explicit deprecation notice | Document in SKILL.md as "fallback for non-project contexts"; add H-04 enforcement reminder |
| PM-011-20260312 | IMPLEMENTED/VERIFIED slice states have no defined transition mechanism | Add note in uc-slicer SKILL.md: "IMPLEMENTED and VERIFIED states are managed in worktracker; no agent transition defined" |
| PM-012-20260312 | cd-generator cognitive_mode inconsistency between .md (convergent) and .governance.yaml (systematic) | Resolve to systematic (matches 9-step deterministic protocol) in both files |

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | PM-001, PM-006, PM-011: Pipeline entry guidance missing; Activity 5 obscured; IMPLEMENTED/VERIFIED lifecycle transition undefined. Three findings affect completeness. |
| Internal Consistency | 0.20 | Negative | PM-002, PM-007, PM-012: Step type semantic drift corrupts downstream transformation; coverage target contradiction between documents; cognitive_mode disagreement between governance files. Three consistency failures. |
| Methodological Rigor | 0.20 | Negative | PM-003, PM-009: Shared schema has no evolution policy or version negotiation; no idempotent re-invocation protocol defined. Schema brittleness undermines the methodology's reproducibility claim. |
| Evidence Quality | 0.15 | Negative | PM-008: Banned-term check creates false-positive rejections based on substring matching without domain context, undermining cd-generator's evidence that placeholder detection is reliable. |
| Actionability | 0.15 | Negative | PM-004, PM-005: Rejection artifact creates silent pipeline stalls with no machine-readable signal; PROTOTYPE removal has no ceremony or audit trail. Users cannot act on these gaps without guessing. |
| Traceability | 0.10 | Mixed | PM-010, PM-012: JERRY_PROJECT fallback path produces artifacts at unpredictable locations; cognitive_mode field inconsistency breaks governance traceability. Positive: every agent carries detailed provenance fields (created_by, updated_at, source citations) that support traceability. Net: Slightly negative. |

**Net Assessment:** Pre-Mortem analysis finds 3 Critical, 6 Major, and 3 Minor failure causes. Five of six S-014 dimensions are negatively impacted. The skills require targeted revision addressing P0 and P1 findings before production confidence can be justified. The core methodology (Cockburn 12-step, Clark transformation, UC-to-contract algorithm) is sound; the failure modes are concentrated in inter-skill coordination, schema governance, and user guidance -- all correctable without architectural changes.

---

## Execution Statistics
- **Total Findings:** 12
- **Critical:** 3
- **Major:** 6
- **Minor:** 3
- **Protocol Steps Completed:** 6 of 6

---

*Report produced by: adv-executor (S-004 Pre-Mortem Analysis)*
*Template: .context/templates/adversarial/s-004-pre-mortem.md v1.0.0*
*Execution ID: 20260312*
*H-16 Compliance: Confirmed (S-003 output present in prior tournament rounds)*
*Finding Prefix: PM-NNN-20260312*
