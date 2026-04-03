# Steelman Report: PROJ-021-use-case Skill Suite

## Steelman Context

- **Deliverable:** Three interconnected skills and associated agents: `/use-case` (uc-author, uc-slicer), `/test-spec` (tspec-generator, tspec-analyst), `/contract-design` (cd-generator, cd-validator), plus shared schemas
- **Deliverable Type:** Multi-skill agent system with JSON Schema contracts
- **Criticality Level:** C4
- **Strategy:** S-003 (Steelman Technique)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Steelman By:** adv-executor | **Date:** 2026-03-12T00:00:00Z | **Original Author:** eng-backend

---

## Summary

**Steelman Assessment:** The PROJ-021-use-case skill suite represents one of the most methodologically rigorous and architecturally well-integrated additions to the Jerry framework. It encodes decades of established use case engineering research (Cockburn 2001, Jacobson 2011, Clark 2018) into deterministic, schema-validated agent pipelines with explicit traceability at every pipeline boundary. The design demonstrates genuine engineering quality in its defense-in-depth validation layers, constitutional compliance architecture, and the novel but well-reasoned UC-to-contract transformation.

**Improvement Count:** 4 Critical, 7 Major, 8 Minor

**Original Strength:** The deliverables are strong in methodology fidelity, constitutional compliance architecture, and cross-skill integration design. The schema design is particularly rigorous, the rejection artifact protocol in uc-slicer is a sophisticated self-healing mechanism, and the cd-generator banned-term detection shows production-grade defensive engineering thinking.

**Recommendation:** Incorporate the Critical and Major improvements before Devil's Advocate (S-002) applies critique. The strengthened reconstruction protects the genuinely excellent design decisions from unfair criticism based on presentation gaps.

---

## Step 1: Deep Understanding — Charitable Interpretation

**Core Thesis:** The PROJ-021-use-case skill suite implements a model-driven, methodology-grounded pipeline that transforms informal stakeholder descriptions into validated API contracts and BDD test specifications, with full provenance from every output artifact back to the source use case step. The three skills (/use-case, /test-spec, /contract-design) form a coherent pipeline where each skill produces artifacts that feed the next, mediated by a shared JSON Schema contract (use-case-realization-v1.schema.json) that enforces structural integrity at every boundary.

**Key Claims:**
1. Progressive elaboration via four Jacobson UC 2.0 detail levels enables incremental investment — teams need not commit to full elaboration before getting value
2. The Clark (2018) deterministic mapping algorithm eliminates scenario invention bias in test generation
3. The UC-to-contract transformation algorithm, though novel (G-01), is grounded in RFC 9110 HTTP method semantics and provides systematic derivation rather than guesswork
4. The five-state UC 2.0 slice lifecycle (SCOPED > PREPARED > ANALYZED > IMPLEMENTED > VERIFIED) connects use case analysis directly to worktracker sprint planning
5. Constitutional compliance (P-003, P-020, P-022) is architecturally enforced through the creator-critic separation pattern and filesystem-mediated cross-agent communication

**Most Charitable Interpretation:** This is a production-grade domain methodology automation system. Its apparent complexity is a direct reflection of the underlying methodological complexity (Cockburn + Jacobson + Clark + RFC 9110 + OpenAPI 3.1), not of engineering overdesign. The detailed validation layers exist because the target audience (developers producing use cases) will make predictable mistakes, and the system is designed to catch and guide correction.

---

## Step 2: Weaknesses in Presentation (Not Substance)

| Weakness | Type | Magnitude |
|----------|------|-----------|
| The relationship between `detail_level` and `realization_level` is not explained as a 2D matrix anywhere | Structural | Critical |
| The PROTOTYPE label lifecycle in cd-generator is not explained in the SKILL.md quick reference | Structural | Major |
| Coverage targets (USER_GOAL=100%, SUMMARY=80%, SUBFUNCTION=100%) differ between test-spec-v1.schema.json and tspec-analyst.md | Evidence | Critical |
| The breadth-first authoring rule (PAT-001) is mentioned in uc-author.md but its rationale is buried in methodology; it is not surfaced in the SKILL.md quick reference | Presentation | Major |
| The rejection artifact protocol (uc-slicer -> uc-author) is a sophisticated self-healing mechanism but is only described procedurally, not explained as an architectural pattern | Structural | Major |
| The cd-generator governance.yaml correctly classifies this as C4 (reasoning_effort: max) but this decision rationale is not surfaced in the SKILL.md for contract-design | Evidence | Major |
| The tspec-analyst methodology explains that coverage targets differ by goal level but the test-specification schema encodes a different split (SUMMARY=60%, SUBFUNCTION=80%, USER_GOAL target implied as 100%) | Evidence | Critical |
| The interaction schema's `minLength: 20` on request/response descriptions is a good defensive measure but its relationship to the Layer 2b quality heuristic is not documented as a multi-layer quality gate | Structural | Major |
| The SKILL.md files all show `Status: PROPOSED` but agents show `Status: ACTIVE` — this inconsistency undermines confidence in the stated readiness | Evidence | Critical |
| The `additionalProperties: false` in the use-case-realization schema means forward evolution requires breaking changes — this constraint is undocumented as an explicit v2.0.0 migration concern | Structural | Minor |
| The uc-author rejection artifact cleanup step (delete `{artifact_path}-rejection.yaml` after successful elaboration) is documented in uc-author.md but not in the uc-slicer failure mode table | Presentation | Minor |
| The cd-validator Step 8 (Internal Operations) FAIL classification ("not a critical FAIL unless all provider interactions are undocumented") introduces a soft FAIL that is inconsistent with the binary PASS/FAIL model | Structural | Major |

All weaknesses above are in presentation, structural expression, or evidence provision. None represent substantive design errors. The core ideas are sound.

---

## Step 3: Steelman Reconstruction

### SM-001: 2D Elaboration Matrix — Surfacing the `detail_level` × `realization_level` Design

[SM-001] The use-case-realization-v1.schema.json governs a two-dimensional artifact state space that is never explicitly surfaced for practitioners. `detail_level` governs narrative completeness (BRIEFLY_DESCRIBED through FULLY_DESCRIBED). `realization_level` governs structural realization (OUTLINED through INTERACTION_DEFINED). These are orthogonal dimensions: a FULLY_DESCRIBED use case can be OUTLINED (no slices); an ESSENTIAL_OUTLINE use case can be INTERACTION_DEFINED (if uc-slicer Activity 5 has run). The allOf constraint blocking INTERACTION_DEFINED + BRIEFLY_DESCRIBED is the system's enforcement of the minimum narrative floor required for realization to be meaningful.

**Strengthened form:** The skill suite should surface this matrix explicitly:

```
                  OUTLINED   STORY_DEFINED   INTERACTION_DEFINED
BRIEFLY_DESCRIBED    OK           OK*           SCHEMA BLOCKED
BULLETED_OUTLINE     OK           OK*           SCHEMA BLOCKED
ESSENTIAL_OUTLINE    OK            OK               OK
FULLY_DESCRIBED      OK            OK               OK

* Possible by schema but not recommended: slice creation on BULLETED_OUTLINE
  artifacts will be rejected by uc-slicer (requires ESSENTIAL_OUTLINE minimum).
```

This matrix immediately clarifies why BRIEFLY_DESCRIBED + INTERACTION_DEFINED is blocked and removes the apparent contradiction between the allOf constraint and the realization_level documentation.

### SM-002: Rejection Artifact Protocol as an Architectural Pattern

[SM-002] The uc-slicer rejection artifact protocol is not just a procedural failure path — it is a clean implementation of the **circuit breaker with structured feedback** pattern adapted for multi-agent pipeline use. When uc-slicer rejects a use case artifact, it writes a machine-readable rejection artifact at a well-known sidecar path (`{artifact_path}-rejection.yaml`) that contains the specific required state and missing elements. uc-author is designed to auto-detect this rejection on re-invocation and incorporate the feedback without human intervention.

**Strengthened form:** This is the pipeline's self-healing mechanism. The schema_version field in the rejection artifact ensures forward compatibility. The five security mitigations (T1-T5) demonstrate that the protocol was designed with adversarial use in mind: path traversal (T2), staleness (T3), YAML injection (T4), unknown rejection reasons (T5). This is production-grade defensive engineering that should be highlighted in the SKILL.md as a "pipeline recovery mechanism" — not buried in the uc-slicer failure mode table.

### SM-003: Coverage Target Alignment — Resolving the Schema/Methodology Discrepancy

[SM-003] The test-specification-v1.schema.json encodes `source_goal_level` with documentation: "USER_GOAL=100%, SUBFUNCTION=80%, SUMMARY=60%." The tspec-analyst.md methodology states: "USER_GOAL: 100%, SUMMARY: 80%+, SUBFUNCTION: 100%." These differ in the SUMMARY and SUBFUNCTION targets.

**Charitable interpretation:** The schema represents the minimum acceptable threshold for a valid generated artifact; the methodology represents the recommended quality target. For SUBFUNCTION use cases (granular subfunctions), 80% coverage may be structurally achievable while the methodology recommends 100% as the aspirational target. The schema is the enforcement floor; the methodology is the quality ceiling. This is a presentation gap, not a design flaw — but the gap should be closed by aligning the documentation.

**Strengthened form:** Add a `coverage_targets` table to the SKILL.md quick reference:

| Goal Level | Schema Enforcement Floor | Methodology Quality Target |
|------------|-------------------------|---------------------------|
| USER_GOAL | (implicit 100% — all flows must map) | 100% |
| SUMMARY | 60% (schema documentation) | 80%+ (methodology documentation) |
| SUBFUNCTION | 80% (schema documentation) | 100% (methodology documentation) |

Note that the schema `coverage_percentage` field is optional — it computable from `mapped_flows / total_flows`. The schema does not enforce the target; tspec-analyst enforces it. This is correct: the schema validates structure; the analyst validates quality.

### SM-004: PROTOTYPE Label as a First-Class Safety Pattern

[SM-004] The `x-prototype: true` label in cd-generator is described as "PROTOTYPE labeling" in passing, but its design is actually a sophisticated safety gate that deserves first-class documentation. The label is:

1. **Mandatory at generation time** (cd-generator always sets it, no override permitted)
2. **Validated at verification time** (cd-validator Step 7 is a hard FAIL if absent)
3. **Removed only by human decision** (P-020 user authority — neither cd-generator nor cd-validator can remove it)
4. **Self-explanatory to downstream consumers** who find the label in the spec before use

This is an implementation of the **human-in-the-loop checkpoint** pattern specifically adapted for a novel algorithm (G-01 — no prior art for UC-to-contract transformation) where confident automation would be premature. The fact that the PROTOTYPE label is enforced by two independent checks (generation-time write + validation-time mandatory FAIL) is defense-in-depth.

**Strengthened form:** The SKILL.md for contract-design should describe the PROTOTYPE label as the "novel algorithm safety gate" with explicit rationale for the G-01 risk. A comment in the openapi-template.yaml should read: "x-prototype: true MUST remain until human reviewer confirms semantic correctness. Removal is a human-only action (P-020). cd-validator will FAIL any contract missing this label."

### SM-005: The Multi-Layer Validation Gate as Defense-in-Depth

[SM-005] The cd-generator validation gate has three layers that are described procedurally but not recognized as a cohesive architectural pattern:

- **Layer 1 (Structural):** Schema validation — machine-enforceable, binary, zero-cost
- **Layer 2a (Banned-Term):** Deterministic placeholder detection — the Unicode normalization, exact-match, and length-conditioned substring checks provide surprising robustness against accidental placeholders, encoding tricks, and copy-paste artifacts
- **Layer 2b (Semantic Quality):** LLM-evaluated soft failure — produces `x-description-quality: low` annotations rather than hard REJECTs, enabling forward progress while flagging quality issues for human review

This three-layer design implements a **graduated quality gate**: hard structural gate first (binary), then deterministic content gate (binary), then probabilistic quality gate (advisory). The correct ordering prevents the expensive LLM evaluation from running on structurally invalid input. The correct use of WARN rather than REJECT at Layer 2b avoids blocking progress on minor quality gaps.

**Strengthened form:** Document this as the "Three-Layer Input Quality Gate" in the contract-design SKILL.md with the rationale for each layer's placement and enforcement level. The cd-validator.governance.yaml's `tier: medium` is consistent — the hard gate is in cd-generator; cd-validator provides the independent verification.

### SM-006: Schema-Mediated Pipeline Contract as Architectural Principle

[SM-006] The use-case-realization-v1.schema.json is not merely a validation schema — it is the **shared artifact contract** that enables three independent skills to interoperate without direct coupling. Every pipeline boundary (uc-author -> uc-slicer, uc-slicer -> tspec-generator, uc-slicer -> cd-generator) is mediated by this schema. The allOf constraints enforce semantic consistency at the schema level rather than requiring runtime agent-to-agent communication.

**Strongest form of this argument:** The schema's `additionalProperties: false` constraint on the root and most sub-objects is a forward-compatibility tradeoff made deliberately. It enforces that no agent can silently add undocumented fields that would corrupt downstream consumers. The cost (breaking change required for new fields) is the price paid for strict consumer protection. This is the correct tradeoff for a v1.0.0 schema defining a public contract.

The `additionalProperties: true` on the `slice` object is a deliberate exception for extensibility — slice definitions are expected to accumulate fields as the lifecycle progresses (worktracker Story IDs, confidence scores, etc.) without requiring schema evolution. This asymmetry is intentional and well-reasoned.

### SM-007: Cognitive Mode Specialization Across Agents

[SM-007] The six agents demonstrate careful cognitive mode selection that aligns with the actual reasoning demands of each task:

- **uc-author** (integrative): Correct. Authoring requires synthesizing stakeholder goals, domain knowledge, and Cockburn structural rules into a coherent narrative — exactly what integrative mode does.
- **uc-slicer** (systematic): Correct. Slicing is a procedural application of INVEST criteria and lifecycle state transitions — systematic mode ensures no step is skipped.
- **tspec-generator** (systematic): Correct. Clark transformation is a deterministic mechanical mapping — systematic mode enforces the algorithm's prescribed order.
- **tspec-analyst** (convergent): Correct. Coverage analysis starts with a full enumeration of mappable flows and converges to a coverage score and prioritized gap list — convergent mode narrows from all options to a ranked conclusion.
- **cd-generator** (convergent): Correct. The 9-step UC-to-contract algorithm requires selecting among candidate resource names, HTTP methods, and schema properties — convergent mode makes one definitive selection per interaction.
- **cd-validator** (systematic): Correct. The 9-step validation protocol is applied as a complete procedural checklist — systematic mode ensures all 9 checks are executed regardless of early failures.

This calibration is not accidental. The cognitive mode taxonomy from `agent-development-standards.md` maps correctly to the actual task demands of each agent. This is a design decision that should be explicitly preserved.

### SM-008: Breadth-First Authoring (PAT-001) as Methodology Correctness Constraint

[SM-008] The PAT-001 rule (breadth-first authoring: apply Steps 1-4 for all use cases before elaborating any to deeper levels) is enforced in uc-author but not well-explained in the SKILL.md. Its rationale is stronger than presented: in Cockburn's methodology, premature depth-first elaboration is the most common cause of incorrect goal level classification and missed actors. A use case elaborated to FULLY_DESCRIBED before related use cases have been identified may have the wrong primary actor, the wrong goal level, or missing sub-use case extractions that would only become apparent if the full actor-goal map had been established first.

**Strengthened form:** PAT-001 is not a style preference — it is a correctness constraint. Violating it creates artifacts that appear complete but are semantically incorrect because they were elaborated in isolation. The rule protects the integrity of the downstream pipeline: a use case with the wrong primary actor produces incorrect "As a" Gherkin clauses (tspec-generator) and incorrect IC-05 actor-role mappings (cd-generator).

### SM-009: The Test-Specification Schema's Coverage Block as Self-Validating Output

[SM-009] The test-specification-v1.schema.json's `coverage` object (with `basic_flow_mapped: boolean`, `mapped_flows`, `total_flows`) enables a Feature file to carry its own coverage snapshot at generation time. This is a thoughtful design: tspec-analyst can cross-reference the Feature file's declared coverage metadata against its computed coverage for consistency checking. A Feature file that declares `coverage.mapped_flows: 5` but only contains 3 scenarios is internally inconsistent — the schema enables detection of this inconsistency.

The `scenario_count` field requirement that it "must equal coverage.mapped_flows" is a schema-level self-consistency check embedded in the documentation. This is the schema doing double duty as both structure validation and self-documentation of correctness invariants.

### SM-010: The Five-State UC 2.0 Slice Lifecycle as Sprint Planning Integration

[SM-010] The five-state lifecycle (SCOPED > PREPARED > ANALYZED > IMPLEMENTED > VERIFIED) maps directly to the sprint lifecycle of an agile team:

- **SCOPED**: Backlog item created with INVEST verification
- **PREPARED**: Ready for sprint planning (test cases defined, Story entity in worktracker)
- **ANALYZED**: Ready for implementation start (interaction sequences defined, API boundary established)
- **IMPLEMENTED**: Sprint work complete (managed by worktracker Story)
- **VERIFIED**: Acceptance criteria met (verified by test execution)

The creation of a worktracker Story entity at the PREPARED state (Activity 4) is the pipeline's integration point with the team's sprint process. This is not just an automation feature — it ensures that every slice that has passed INVEST verification has a corresponding worktracker entity, making use case analysis directly actionable for sprint planning without a separate translation step.

---

## Improvement Findings Table

| ID | Improvement | Severity | Original | Strengthened | Dimension |
|----|-------------|----------|----------|-------------|-----------|
| SM-001 | Explicit 2D elaboration state matrix (detail_level × realization_level) | Critical | Implicit in schema allOf constraints; never visualized | Visual matrix showing all 12 state combinations with valid/blocked annotations | Completeness |
| SM-002 | Rejection artifact as "Pipeline Self-Healing Mechanism" architectural pattern | Critical | Described procedurally in uc-slicer failure modes only | Named pattern with rationale, security mitigations documented as T1-T5 | Methodological Rigor |
| SM-003 | Coverage target alignment between schema documentation and methodology | Critical | Discrepancy: SUMMARY=60% in schema vs. 80%+ in methodology; SUBFUNCTION=80% in schema vs. 100% in methodology | Unified table clarifying enforcement floor (schema) vs. quality ceiling (methodology) | Internal Consistency |
| SM-004 | PROTOTYPE label documented as "Novel Algorithm Safety Gate" with G-01 rationale | Major | Described as "PROTOTYPE labeling" in passing; rationale not stated | First-class documentation with G-01 explicit rationale, two enforcement points described | Evidence Quality |
| SM-005 | Three-Layer Input Quality Gate as a named architectural pattern | Major | Three layers described procedurally in cd-generator methodology; not named or explained as a pattern | "Three-Layer Input Quality Gate" with rationale for layer ordering and enforcement level | Methodological Rigor |
| SM-006 | Schema as "Shared Artifact Contract" — additionalProperties asymmetry explained | Major | Schema behavior implied; additionalProperties: true on slice not explained | Explicit documentation of schema-as-contract with tradeoff documentation for strict vs. extensible objects | Traceability |
| SM-007 | Cognitive mode calibration preserved as explicit design decision | Major | Cognitive modes stated in governance YAML without rationale | Rationale documented per agent in SKILL.md Available Agents table | Methodological Rigor |
| SM-008 | PAT-001 breadth-first authoring elevated to "methodology correctness constraint" | Major | PAT-001 labeled a "pattern" in uc-author.md; rationale brief | Full rationale: premature depth-first elaboration produces incorrect goal levels, missed actors, and invalid downstream artifacts | Evidence Quality |
| SM-009 | Coverage self-consistency invariant in test-specification schema documented | Major | schema_count/coverage relationship noted as "must equal" in schema description | Explicit documentation of cross-field invariant; tspec-analyst cross-check described | Completeness |
| SM-010 | Slice lifecycle as sprint planning integration documented | Major | Five states documented without explicit mapping to sprint lifecycle | Lifecycle-to-sprint mapping table; worktracker Story entity creation at PREPARED explicitly justified | Actionability |
| SM-011 | SKILL.md Status field PROPOSED/ACTIVE inconsistency resolved | Critical | SKILL.md files: Status: PROPOSED; agent .md files: Status: ACTIVE | Align all to ACTIVE or clarify that PROPOSED refers to skill registration status, not operational status | Internal Consistency |
| SM-012 | cd-validator Step 8 soft FAIL rule clarified | Minor | "Not a critical FAIL unless all provider interactions are undocumented" creates ambiguity | Explicit PASS/WARN/FAIL taxonomy: FAIL if any provider interaction is undocumented (for full traceability); WARN if partial documentation is present but all consumer interactions are covered | Internal Consistency |
| SM-013 | interaction schema minLength:20 described as quality gate layer | Minor | minLength: 20 on request/response descriptions; relationship to Layer 2b heuristic not explained | Document that the schema enforces a minimum length floor while Layer 2b enforces semantic quality; two independent quality gates for descriptions | Traceability |
| SM-014 | allOf constraint documentation for forward compatibility | Minor | additionalProperties: false is stated; schema evolution concern not documented | Add schema preamble documenting that v1.0.0 uses additionalProperties: false for consumer protection; v2.0.0 will require explicit field additions; migration path should follow semantic versioning | Completeness |
| SM-015 | Rejection artifact cleanup documented in uc-slicer failure mode table | Minor | uc-author.md documents cleanup; uc-slicer failure mode table does not mention cleanup responsibility | Add cleanup note to uc-slicer failure mode table: "After writing rejection artifact: successful elaboration by uc-author will auto-delete it; if elaboration is abandoned, rejection artifact should be manually deleted." | Completeness |
| SM-016 | Coverage targets by goal level: tspec-analyst and schema fully aligned | Minor | Numeric discrepancy in SUMMARY/SUBFUNCTION targets | Canonical table in both SKILL.md and schema documentation | Internal Consistency |
| SM-017 | Slice `realization_level` field documents its relationship to UC-level realization_level | Minor | Slice has its own realization_level (STORY_DEFINED, INTERACTION_DEFINED) but its relationship to the UC-level realization_level is not explained | Document that UC-level realization_level is the maximum of all slice realization levels: UC is INTERACTION_DEFINED only when at least one slice achieves that level | Internal Consistency |
| SM-018 | The PAT-001 breadth-first rule added to SKILL.md Quick Reference | Minor | PAT-001 in uc-author.md only | "Breadth-first authoring required: identify all use case briefs before elaborating any" in the SKILL.md quick reference | Completeness |
| SM-019 | `actor_role` enum values documented in schema comments | Minor | `consumer`, `provider` enum values in interaction schema; their meaning for OpenAPI operation classification not documented in schema | Schema property description expanded: "consumer -> external path+operation; provider -> x-internal-operations entry" | Traceability |

---

## Improvement Details

### SM-001: 2D Elaboration Matrix

**Affected Dimension:** Completeness

**Original Content:** The allOf constraint `if realization_level = INTERACTION_DEFINED and detail_level in [BRIEFLY_DESCRIBED, BULLETED_OUTLINE] then false` exists in the schema but is never visualized or explained in prose.

**Strengthened Content:** Add to use-case SKILL.md under "Methodology Reference":

```
### Artifact State Space (detail_level × realization_level)

                    OUTLINED    STORY_DEFINED    INTERACTION_DEFINED
BRIEFLY_DESCRIBED     OK           WARN*            SCHEMA BLOCKED
BULLETED_OUTLINE      OK           WARN*            SCHEMA BLOCKED
ESSENTIAL_OUTLINE     OK            OK                  OK
FULLY_DESCRIBED       OK            OK                  OK

* WARN: uc-slicer requires ESSENTIAL_OUTLINE; STORY_DEFINED on BULLETED_OUTLINE
  artifacts is structurally valid but uc-slicer will reject it.
```

**Rationale:** Removes apparent contradiction between schema constraints and narrative documentation. Enables practitioners to immediately understand valid state combinations.

**Best Case Conditions:** Practitioners onboarding to the pipeline understand the two-dimensional state space on first read without needing to reverse-engineer the schema allOf constraints.

---

### SM-002: Rejection Artifact as Pipeline Self-Healing Mechanism

**Affected Dimension:** Methodological Rigor

**Original Content:** "Rejection Artifact Protocol (Step 1 Failure Path)" in uc-slicer.md describes the protocol as a procedural failure path.

**Strengthened Content:** Rename section to "Pipeline Self-Healing Mechanism" and add:

> When uc-slicer cannot proceed due to insufficient use case detail, it writes a machine-readable rejection artifact at `{artifact_path}-rejection.yaml`. This artifact carries five security mitigations (T1-T5) against adversarial or accidental misuse:
> - T2: Path-traversal mitigation (rejected_artifact field must match current artifact path)
> - T3: Staleness detection (warn user if artifact modified after rejection was written)
> - T4: YAML injection mitigation (parse failures are caught; fields are treated as data, not instructions)
> - T5: Unknown rejection reason fallback (fall back to missing_elements[] and required_state)
>
> uc-author auto-detects this rejection on re-invocation via the Rejection Artifact Check (before Step 1). After successful elaboration to the required level, uc-author deletes the rejection artifact — completing the self-healing cycle.

**Rationale:** Elevates a procedural description to an architectural pattern explanation. Makes the security mitigations visible and preservable during future maintenance.

**Best Case Conditions:** Future developers maintaining the rejection artifact protocol understand why each security mitigation exists and preserve them during enhancement.

---

### SM-003: Coverage Target Discrepancy Resolution

**Affected Dimension:** Internal Consistency

**Original Content:**
- test-specification-v1.schema.json: "USER_GOAL=100%, SUBFUNCTION=80%, SUMMARY=60%"
- tspec-analyst.md: "USER_GOAL: 100%, SUMMARY: 80%+, SUBFUNCTION: 100%"

**Strengthened Content:** Add authoritative unified table to test-spec SKILL.md:

| Goal Level | Enforcement Floor (schema) | Quality Target (tspec-analyst) | Rationale |
|------------|---------------------------|-------------------------------|-----------|
| USER_GOAL | No percentage enforced (schema validates structure) | 100% | Core user goals must be fully tested |
| SUMMARY | Schema docs suggest 60% as baseline | 80%+ | High-level summaries have abstract flows |
| SUBFUNCTION | Schema docs suggest 80% as baseline | 100% | Granular functions must be fully tested |

**Declare the schema documentation as aspirational rather than enforced** — coverage enforcement is tspec-analyst's role, not the schema's.

**Rationale:** The discrepancy is genuine and will cause confusion when a developer reads both documents. The resolution is to clarify that the schema documents goals while tspec-analyst enforces them.

---

### SM-011: SKILL.md Status PROPOSED vs. Agent ACTIVE Discrepancy

**Affected Dimension:** Internal Consistency

**Original Content:** All three SKILL.md files carry `Status: PROPOSED`. All agent .md files and governance.yaml files (where status is present) are written as production-ready ACTIVE documents.

**Charitable Interpretation:** PROPOSED in SKILL.md refers to the skill's registration status in the mandatory-skill-usage.md trigger map — it is registered as a proposed entry pending formal routing table update. The agents themselves are ACTIVE.

**Strengthened Content:** Add to each SKILL.md header:
```
> **Status:** PROPOSED (skill routing registration) | Agents: ACTIVE (operational)
```
And add to the SKILL.md constitutional compliance section: "SKILL.md Status: PROPOSED reflects the routing registration status per agent-routing-standards.md Phase 1 trigger map migration. All agents are operational. Skill routing will be finalized when mandatory-skill-usage.md is updated."

---

## Step 4: Best Case Scenario

### Conditions Under Which This Pipeline Is Most Compelling

1. **Team has domain experts who can describe stakeholder goals in natural language but cannot specify APIs.** The pipeline bridges the gap from "what actors want" to "what endpoints must exist" through a methodologically grounded chain. No team member needs API design expertise to start — only the ability to describe what the primary actor is trying to achieve.

2. **System under development has multiple bounded contexts with independent actors.** The SUMMARY/USER_GOAL/SUBFUNCTION goal level classification prevents over-specified use cases that try to capture all system behavior in one artifact. The pipeline naturally decomposes complex systems into correctly-scoped use cases.

3. **Team practices BDD and wants test specifications grounded in use case analysis rather than invented scenarios.** The Clark transformation guarantee that every scenario traces to a specific use case flow element eliminates the "I'm not sure what this scenario is testing" problem.

4. **Team uses OpenAPI-based code generation.** The cd-generator output is structurally valid OpenAPI 3.1 with full traceability — even with the PROTOTYPE label, it provides a machine-readable API surface that code generators can process immediately, accelerating initial scaffolding.

**Key Assumptions:**
- Use case artifacts are elaborated to ESSENTIAL_OUTLINE before pipeline consumption (uc-slicer enforces this)
- The UC-to-contract transformation algorithm's method inference confidence annotations are reviewed by a human developer before removing PROTOTYPE
- Teams understand that the pipeline produces artifacts, not final decisions — human review remains essential at key gates

**Confidence:** HIGH. The methodological grounding (Cockburn 2001, Jacobson 2011, Clark 2018, RFC 9110, OpenAPI 3.1) provides strong academic and industry backing for every design choice. The constitutional compliance architecture (P-003, P-020, P-022 enforced in every agent) is correct and consistent.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive | SM-001 (state matrix), SM-009 (coverage invariant), SM-014 (schema forward compatibility), SM-015 (cleanup documentation), SM-018 (PAT-001 in quick reference) directly improve completeness of documentation and cross-references |
| Internal Consistency | 0.20 | Positive | SM-003 (coverage target alignment), SM-011 (status field alignment), SM-012 (Step 8 soft FAIL clarification), SM-016 (target alignment), SM-017 (slice realization_level relationship) are all internal consistency improvements |
| Methodological Rigor | 0.20 | Positive | SM-002 (rejection artifact as pattern), SM-005 (three-layer gate as pattern), SM-007 (cognitive mode rationale), SM-008 (PAT-001 as correctness constraint) strengthen the methodological rigor of the deliverable's arguments |
| Evidence Quality | 0.15 | Positive | SM-004 (PROTOTYPE label rationale), SM-006 (schema-as-contract tradeoff documentation), SM-008 (PAT-001 downstream impact evidence) add evidence and rationale for key design decisions |
| Actionability | 0.15 | Positive | SM-010 (sprint lifecycle mapping), SM-018 (quick reference additions) make the deliverable more directly actionable for practitioners |
| Traceability | 0.10 | Positive | SM-006 (additionalProperties asymmetry), SM-013 (minLength relationship to Layer 2b), SM-019 (actor_role documentation) improve field-level traceability |

**Summary:** All six dimensions benefit from the steelman improvements. No dimension is weakened by any improvement. The original deliverable was strong in constitutional compliance and schema design; the steelman strengthens its presentation, documentation, and cross-document consistency.

---

## Step 5 Summary: Improvement Findings by Severity

| ID | Summary | Severity |
|----|---------|----------|
| SM-001 | 2D elaboration state matrix (detail_level × realization_level) surfaced | Critical |
| SM-002 | Rejection artifact protocol documented as Pipeline Self-Healing Mechanism | Critical |
| SM-003 | Coverage target discrepancy between schema and methodology resolved | Critical |
| SM-011 | SKILL.md Status PROPOSED vs. Agent ACTIVE inconsistency resolved | Critical |
| SM-004 | PROTOTYPE label documented as Novel Algorithm Safety Gate with G-01 rationale | Major |
| SM-005 | Three-Layer Input Quality Gate documented as architectural pattern | Major |
| SM-006 | Schema-as-Shared-Artifact-Contract with additionalProperties asymmetry explained | Major |
| SM-007 | Cognitive mode calibration preserved as explicit design decision with rationale | Major |
| SM-008 | PAT-001 breadth-first authoring elevated to methodology correctness constraint | Major |
| SM-009 | Coverage self-consistency invariant (scenario_count = coverage.mapped_flows) documented | Major |
| SM-010 | Slice lifecycle mapped to sprint lifecycle with worktracker integration justified | Major |
| SM-012 | cd-validator Step 8 soft FAIL rule clarified | Minor |
| SM-013 | interaction schema minLength:20 relationship to Layer 2b quality gate explained | Minor |
| SM-014 | additionalProperties:false forward-compatibility constraint documented | Minor |
| SM-015 | Rejection artifact cleanup responsibility added to uc-slicer failure mode table | Minor |
| SM-016 | Coverage targets fully aligned between SKILL.md and schema | Minor |
| SM-017 | Slice realization_level relationship to UC-level realization_level documented | Minor |
| SM-018 | PAT-001 breadth-first rule added to SKILL.md Quick Reference | Minor |
| SM-019 | actor_role enum value semantics documented in schema property description | Minor |

---

## Step 6: Self-Review (H-15)

Pre-persistence self-review per H-15:

1. **All findings have specific evidence from the deliverables.** Each SM-NNN finding references a specific file, section, or field in the examined deliverables. No vague or invented findings.

2. **Severity classifications are justified.** Critical findings represent fundamental gaps that would undermine reviewer confidence (state space confusion, inconsistent status, conflicting coverage targets, missing architectural pattern explanation). Major findings represent significant presentation weaknesses where key design rationale is undocumented. Minor findings are polish improvements.

3. **Finding identifiers follow the SM-NNN prefix format.** All findings use SM-NNN as required by the S-003 template Identity section.

4. **Report is internally consistent.** The findings summary table (19 findings: 4 Critical, 7 Major, 8 Minor) matches the detailed findings sections and improvement details.

5. **No findings were minimized.** The coverage target discrepancy (SM-003) and the SKILL.md status inconsistency (SM-011) are genuine consistency issues that could undermine adopter confidence; they are correctly classified as Critical.

6. **Charitable interpretation applied throughout.** The coverage target discrepancy is interpreted as an enforcement floor vs. quality ceiling distinction, not a contradiction. The SKILL.md Status: PROPOSED is interpreted as routing registration status, not operational readiness. These are the strongest reasonable interpretations.

**Self-review verdict:** The steelman report is ready for downstream use by S-002 (Devil's Advocate). The improvements protect genuinely excellent design decisions while surfacing legitimate presentation and consistency gaps.

---

## Execution Statistics

- **Total Findings:** 19
- **Critical:** 4
- **Major:** 7
- **Minor:** 8
- **Protocol Steps Completed:** 6 of 6
- **Deliverables Examined:** 12 files (6 agent .md files, 4 governance.yaml files, 2 JSON schema files, 3 SKILL.md files = 15 total reads; schemas and SKILL.md are additional supporting artifacts)
- **H-16 Status:** S-003 complete. Ready for S-002 (Devil's Advocate).

---

*S-003 Execution Report*
*Strategy: S-003 Steelman Technique*
*Template: .context/templates/adversarial/s-003-steelman.md*
*Deliverable suite: PROJ-021-use-case skill agents and schemas*
*Executed: 2026-03-12*
*Finding Prefix: SM (from template Section 1: Identity)*
*H-16 compliance: S-003 completed before S-002 — confirmed*
