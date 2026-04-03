# Agent Decomposition Architecture: /use-case, /test-spec, /contract-design

> **PS ID:** proj-021 | **Entry ID:** architecture-agent-decomposition-final | **Workflow ID:** use-case-skills-20260308-001
> **Date:** 2026-03-08 | **Agent:** ps-architect | **Execution Group:** Phase 2 Architecture (Step 8-final, G-06)
> **Quality Threshold:** >= 0.95 (C4, user override C-008)
> **Status:** PROPOSED (per P-020 -- user authority required for acceptance)
> **Version:** 1.0.0
> **Lineage:** Integrates agent-decomposition-draft.md (v1.2.0, 0.957 PASS), frontmatter-schema.md (v1.0.0, 0.955 PASS), file-organization.md (v2.1.0, 0.951 PASS), shared-schema.json (v1.0.0)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | What changed from draft to final; schema integration overview |
| [L1: Technical Specifications](#l1-technical-specifications) | Per-agent specs with schema-integrated I/O, validation rules |
| [Agent Inventory Summary](#agent-inventory-summary) | Quick-reference table with schema responsibilities |
| [Skill 1: /use-case](#skill-1-use-case) | 2 agents: uc-author, uc-slicer -- with schema field ownership |
| [Skill 2: /test-spec](#skill-2-test-spec) | 1 agent: tspec-generator -- with schema input requirements |
| [Skill 3: /contract-design](#skill-3-contract-design) | 1 agent: cd-generator -- with schema input requirements |
| [Progressive Realization Matrix](#progressive-realization-matrix) | How each agent advances artifacts through realization levels |
| [Schema Constraint Responsibility Map](#schema-constraint-responsibility-map) | Which agents satisfy which allOf constraints |
| [Agent Interaction Model](#agent-interaction-model) | Intra-skill and cross-skill interaction with schema validation gates |
| [Trigger Map Extensions](#trigger-map-extensions) | New keywords, negative keywords, compound triggers for all 3 skills |
| [L2: Architectural Rationale](#l2-architectural-rationale) | Schema traceability, progressive realization design, evolution path |
| [Options Evaluated](#options-evaluated) | Alternatives considered per P-011 |
| [Risk Assessment](#risk-assessment) | Per-skill risk analysis with mitigations |
| [Traceability Matrix](#traceability-matrix) | Map to synthesis DI-01 through DI-12 and R-01 through R-10 |
| [Self-Review Checklist](#self-review-checklist) | H-15, S-010 pre-submission verification |

---

## L0: Executive Summary

This is the final agent decomposition document for three new Jerry skills that implement Ivar Jacobson's Use Case 2.0 methodology as a pipeline: `/use-case` creates use case artifacts, `/test-spec` derives BDD test specifications, and `/contract-design` generates API contracts.

**What changed from draft to final.** The draft document (v1.2.0, scored 0.957 PASS) established the agent count, cognitive modes, tool tiers, methodologies, and routing design. This final version integrates the formal JSON Schema specification (`shared-schema.json`) that was designed after the draft. Every agent now has:

1. **Schema-referenced input/output tables** -- each input and output field is identified by its JSON path in `shared-schema.json`, not just by name. Phase 3 implementers know exactly which schema fields each agent reads and writes.

2. **Schema validation guardrails** -- each agent declares the minimum realization level it requires and produces. The guardrails reference specific schema `allOf` conditional constraints by number.

3. **Progressive realization ownership** -- a new matrix shows how each agent advances a use case document through the three realization levels (OUTLINED, STORY_DEFINED, INTERACTION_DEFINED), with the specific schema fields added at each transition.

**What did not change.** The agent count (4 agents: uc-author, uc-slicer, tspec-generator, cd-generator), cognitive modes, tool tiers, model selections, trigger map extensions, and all risk/steelman/pre-mortem analyses from the draft are preserved exactly. This document does not rewrite the draft -- it enhances it with schema integration.

**Pipeline architecture.** The three skills form a unidirectional pipeline driven by `shared-schema.json` validation. `/use-case` produces the artifact (OUTLINED or STORY_DEFINED level). `/test-spec` consumes it at STORY_DEFINED minimum. `/contract-design` consumes it at INTERACTION_DEFINED. Schema validation at each boundary prevents invalid handoffs.

---

## L1: Technical Specifications

### Agent Inventory Summary

| # | Agent Name | Skill | Role | Cognitive Mode | Model | Tool Tier | Schema Responsibility | Traceability |
|---|-----------|-------|------|---------------|-------|-----------|----------------------|--------------|
| 1 | `uc-author` | `/use-case` | Use Case Author | integrative | sonnet | T2 (Read-Write) | Produces: Identity, Classification, Actors, Conditions, Flows blocks. Output realization: OUTLINED minimum. | DI-01, DI-02, DI-11, R-04 |
| 2 | `uc-slicer` | `/use-case` | Use Case Slicer | systematic | sonnet | T2 (Read-Write) | Produces: Slicing, Interactions blocks. Advances realization: STORY_DEFINED or INTERACTION_DEFINED. Responsible for allOf constraints 1+2. | DI-03, R-04, R-09 |
| 3 | `tspec-generator` | `/test-spec` | BDD Test Spec Generator | systematic | sonnet | T2 (Read-Write) | Reads: Flows, Conditions, Classification blocks. Requires STORY_DEFINED minimum input. Produces external `.feature.md` files. | DI-05, DI-06, R-05 |
| 4 | `cd-generator` | `/contract-design` | API Contract Generator | convergent | opus | T2 (Read-Write) | Reads: Interactions, Actors blocks. Requires INTERACTION_DEFINED input. Produces external `.openapi.yaml` + `-mapping.md` files. | DI-07, DI-08, R-06 |

---

### Skill 1: /use-case

#### Agent 1.1: `uc-author`

**Identity**

| Field | Value | Source |
|-------|-------|--------|
| Role | Use Case Author -- creates and elaborates use case artifacts using Cockburn's 12-step writing process and Jacobson's UC 2.0 progressive narrative levels | DI-01, DI-11 |
| Expertise (1) | Cockburn use case writing methodology (12-step process, goal levels, precision levels, template formats Brief/Casual/Fully-Dressed) | S-02 (Cockburn research) |
| Expertise (2) | Jacobson UC 2.0 narrative levels (Briefly Described, Bulleted Outline, Essential Outline, Fully Described) and use-case modeling (actors, goals, use-case model) | S-01 (Jacobson research) |
| Expertise (3) | Stakeholder elicitation and goal decomposition using Cockburn's sea-metaphor classification (Cloud/Kite/Sea Level/Fish/Clam) | S-02, DI-02 |
| Cognitive Mode | **Integrative** -- combines inputs from multiple sources (stakeholder descriptions, existing system context, domain knowledge) into unified use case artifacts. Authoring requires cross-source correlation and gap filling. | AD-M-009 taxonomy, R-09 |

**Model Selection: Sonnet (AD-M-009 MEDIUM Override Documented)**

Standard being overridden: `agent-development-standards.md` Mode-to-Design Implications table recommends Opus for integrative cognitive mode ("opus (complex synthesis)").

Justification for override: The `uc-author` agent's integrative reasoning operates within a tightly constrained procedural framework -- Cockburn's 12-step writing process. Unlike general integrative tasks (e.g., cross-pipeline merging, open-ended taxonomy building), use case authoring has well-defined inputs (stakeholder descriptions, actor-goal lists), well-defined outputs (structured YAML frontmatter + narrative), and a named step-by-step process that bounds the reasoning space. Sonnet's strength with "structured criteria and named frameworks" is a better match for this constrained integrative pattern than Opus's broad reasoning capability. If quality scores fall below 0.92 threshold during Phase 3 prototyping, Opus is the first escalation path.

**Tool Tier: T2 (Read-Write)**

Justification: Reads existing project context (use case templates, existing use cases, shared schema) and writes use case artifact files. No external research (T3) -- methodology is embedded. No cross-session state (T4). No delegation (T5) -- worker agent.

Tools: Read, Write, Edit, Glob, Grep, Bash

**Methodology Outline (Key Steps)**

The methodology implements Cockburn's 12-step writing process (S-02: Reminders pp. ii-iii, Ch. 22 Reminder 18 p. 223) with UC 2.0 progressive narrative levels:

| Step | Cockburn 12-Step | Agent Action | Schema Fields Produced |
|------|-----------------|--------------|----------------------|
| 1 | Determine system scope and boundaries | Read project context; identify system boundary; set design scope | `$.scope`, `$.domain` |
| 2 | Brainstorm and list primary actors | Enumerate human and non-human actors over system lifecycle | `$.primary_actor`, `$.supporting_actors[*]` |
| 3 | Brainstorm and exhaustively list user goals | Create actor-goal list; classify each goal by level | `$.goal_level`, `$.goal_symbol` |
| 4 | Write outer use case brief for each | Create use case artifacts at Briefly Described level | `$.id`, `$.title`, `$.work_type`, `$.version`, `$.status`, `$.detail_level`, `$.created_at`, `$.created_by` |
| 5 | Review and adjust scope | Validate actor-goal list against stakeholder input | Updated `$.primary_actor`, `$.supporting_actors[*]`, `$.related_use_cases[*]` |
| 6 | Select a use case to expand | User selects or agent recommends based on value | `$.priority` |
| 7 | Capture stakeholders, interests, preconditions, guarantees | Elaborate stakeholder contract per Cockburn Ch. 2 | `$.stakeholders[*]`, `$.preconditions[*]`, `$.postconditions`, `$.trigger` |
| 8 | Write Main Success Scenario (3-9 steps) | Apply Guideline 6 step-count rule; meet all interests and guarantees | `$.basic_flow[*]` (each: `$defs/flow_step` with `.step`, `.actor`, `.action`, `.type`) |
| 9 | Brainstorm extension conditions exhaustively | Anchor extensions to MSS step numbers | `$.extensions[*].condition`, `$.extensions[*].anchor_step` |
| 10 | Write extension handling steps | Each extension terminates by rejoin, separate success, or failure | `$.extensions[*]` (each: `$defs/extension` with `.id`, `.name`, `.anchor_step`, `.condition`, `.steps[*]`, `.outcome`), `$.alternative_flows[*]` (each: `$defs/alternative_flow`) |
| 11 | Extract sub-use-cases if needed | Refactor repeated sequences into subordinate use cases | `$.parent_id`, `$.related_use_cases[*]` |
| 12 | Review for readability, completeness, stakeholder interests | Quality check against 7 Cs framework | `$.updated_at`, `$.last_modified_by`, `$.detail_level` (upgraded to reflect actual completeness) |

**Progressive Detail Levels:** The agent supports 4 output detail levels as discrete modes (DI-01, PAT-001):

| Level | UC 2.0 Name | Cockburn Mapping | Steps Active | Schema `$.detail_level` Value | Minimum Schema Fields |
|-------|------------|-----------------|--------------|-------------------------------|----------------------|
| 1 | Briefly Described | Name + goal + brief | Steps 1-4 | `BRIEFLY_DESCRIBED` | `$.id`, `$.title`, `$.work_type`, `$.version`, `$.status`, `$.goal_level`, `$.scope`, `$.primary_actor`, `$.basic_flow` (3+ steps), `$.created_at`, `$.created_by` |
| 2 | Bulleted Outline | Brief + MSS bullets | Steps 1-8 | `BULLETED_OUTLINE` | Level 1 fields + populated `$.basic_flow` with typed steps |
| 3 | Essential Outline | + Extensions | Steps 1-10 | `ESSENTIAL_OUTLINE` | Level 2 fields + `$.extensions[*]`, `$.alternative_flows[*]`, `$.preconditions`, `$.postconditions` |
| 4 | Fully Described | + Handling + Sub-UCs | Steps 1-12 | `FULLY_DESCRIBED` | Level 3 fields + `$.stakeholders[*]`, `$.parent_id`, `$.related_use_cases[*]` |

Default: Level 2 (Bulleted Outline). Upgrade on demand per PAT-001 (progressive elaboration).

**Schema-Integrated Input/Output**

| Direction | Content | Schema Fields (JSON Path) | Validation |
|-----------|---------|--------------------------|------------|
| Input | User request describing a system capability or existing use case to elaborate. Optionally: project context files, existing actor-goal list, system boundary description. | N/A (natural language + optional file paths) | N/A |
| Output | Use case artifact file with YAML frontmatter and Markdown narrative body | `$.id`, `$.title`, `$.work_type` (const: `USE_CASE`), `$.version`, `$.status`, `$.goal_level`, `$.goal_symbol`, `$.detail_level`, `$.scope`, `$.domain`, `$.primary_actor`, `$.supporting_actors[*]` ({`.name`, `.type`}), `$.stakeholders[*]` ({`.name`, `.interest`}), `$.preconditions[*]`, `$.postconditions` ({`.success[*]`, `.failure[*]`}), `$.trigger`, `$.basic_flow[*]` (`$defs/flow_step`), `$.alternative_flows[*]` (`$defs/alternative_flow`), `$.extensions[*]` (`$defs/extension`), `$.parent_id`, `$.related_use_cases[*]`, `$.requirements[*]`, `$.priority`, `$.created_at`, `$.updated_at`, `$.created_by`, `$.last_modified_by` | Output MUST validate against `shared-schema.json` top-level `required` array. `$.basic_flow` MUST have 3-9 items (schema `minItems: 3, maxItems: 9`). Each `$.basic_flow[*].type` MUST be one of `actor_action`, `system_response`, `validation`. |

Output path: `projects/${JERRY_PROJECT}/use-cases/{UC-NNN}-{slug}.md` (per R-02)

**Guardrails (Beyond Constitutional Triplet)**

| Guardrail | Schema Enforcement | Source |
|-----------|-------------------|--------|
| MUST classify every use case by goal level (Cloud/Kite/Sea Level/Fish/Clam) | `$.goal_level` is in schema `required` array. Enum: `SUMMARY`, `USER_GOAL`, `SUBFUNCTION`. When `$.goal_symbol` is set, allOf constraints 3/4/5 enforce consistency. | DI-02, PAT-007 |
| MUST enforce 3-9 steps in Main Success Scenario | `$.basic_flow`: schema `minItems: 3, maxItems: 9` | S-02 (Cockburn Guideline 6) |
| MUST NOT advance to Fully Described without complete extension conditions | Agent guardrail (not schema-enforced): `$.detail_level` = `FULLY_DESCRIBED` requires `$.extensions` to be non-empty | S-02, DI-05 |
| MUST write breadth-first: scope actors and goals before elaborating individual use cases | Agent guardrail (procedural, not schema-enforced) | S-02, PAT-001 |
| MUST set `$.detail_level` in YAML frontmatter matching actual narrative completeness | Agent guardrail: `$.detail_level` enum must reflect actual content depth | AI-02, DI-01 |
| MUST NOT bypass human review for generated use case content | Agent guardrail: `$.status` remains `DRAFT` until human review | CF-03 |
| Output MUST validate against `shared-schema.json` at the top-level `required` fields | Schema validation: all 11 required fields must be present | R-01, R-03 |

---

#### Agent 1.2: `uc-slicer`

**Identity**

| Field | Value | Source |
|-------|-------|--------|
| Role | Use Case Slicer -- decomposes use cases into implementation-ready slices following Jacobson UC 2.0 Activity 2 (Slice the Use Cases), Activity 4 (Prepare a Use-Case Slice), and Activity 5 (Analyze a Use-Case Slice: produce the realization interaction sequence) | DI-03, S-01 Activities 2+4+5 |
| Expertise (1) | Jacobson UC 2.0 slicing patterns (end-to-end slice selection, INVEST criteria application, slice state lifecycle management) | S-01 (Jacobson research, Activities 2+4) |
| Expertise (2) | Use case slice lifecycle management (Scoped > Prepared > Analyzed > Implemented > Verified) with worktracker integration | S-01 (slice lifecycle), PAT-006 |
| Cognitive Mode | **Systematic** -- applies step-by-step slicing procedures: identify basic flow as first slice, identify additional slices from alternatives and extensions, verify INVEST criteria, assign slice states. Activity 5 introduces bounded convergent sub-decisions (e.g., which system element handles a responsibility) within the systematic lifecycle framework; these do not constitute a second cognitive mode per Pattern 1 criterion (b) analysis. | AD-M-009 taxonomy, R-09 |

**Model Selection: Sonnet**

Justification (AD-M-009): Slicing is a procedural, systematic activity. The agent follows a defined protocol (identify flows, create slices, verify INVEST). Sonnet's balanced capability handles the structured decision-making without requiring Opus-level reasoning. Haiku would be insufficient because slice identification requires understanding of use case flow dependencies.

**Tool Tier: T2 (Read-Write)**

Justification: Reads existing use case artifacts; writes slice definitions back into the artifact (slice sections in YAML frontmatter) and optionally creates worktracker Story entities for each slice.

Tools: Read, Write, Edit, Glob, Grep, Bash

**Methodology Outline (Key Steps)**

| Step | UC 2.0 Activity | Agent Action | Schema Fields Produced |
|------|-----------------|--------------|----------------------|
| 1 | Activity 2: Identify first slice | Select the basic flow as the first slice (end-to-end through the concept) | `$.slices[0]` (`$defs/slice`: `.slice_id`, `.title`, `.steps_included[*]`) |
| 2 | Activity 2: Identify additional slices | Each alternative flow becomes a candidate slice; each significant extension becomes a candidate slice | `$.slices[1..N]` |
| 3 | Activity 2: Verify INVEST criteria | Each slice must be Independent, Negotiable, Valuable, Estimable, Small, Testable | `$.slices[*].invest_assessment` ({`.independent`, `.negotiable`, `.valuable`, `.estimable`, `.small`, `.testable`}) |
| 4 | Activity 2: Order slices | Rank by value; basic flow first; dependent slices after their dependencies | `$.slice_ids[*]` (ordered reference list in traceability block) |
| 5 | Activity 4: Prepare selected slice | Enhance narrative detail for the selected slice; define acceptance test cases | `$.slices[*].realization_level` -> `STORY_DEFINED` |
| 6 | Activity 4: Define test cases | Each slice must have at least one test case before it is "Prepared" | `$.slices[*].test_cases[*]` |
| 7 | Activity 5: Analyze slice (produce realization) | Identify system elements involved in the slice; allocate responsibilities; produce the interaction sequence section | `$.interactions[*]` (each: `$defs/interaction` with `.id`, `.source_step`, `.source_flow`, `.actor_role`, `.system_role`, `.request_description`, `.response_description`, `.preconditions[*]`, `.postconditions[*]`), `$.slices[*].realization_level` -> `INTERACTION_DEFINED` |
| 8 | State transition | Set `$.slice_state` in YAML frontmatter and `$.realization_level` | `$.slice_state` (enum: `SCOPED` -> `PREPARED` -> `ANALYZED`), `$.realization_level` (enum: `OUTLINED` -> `STORY_DEFINED` -> `INTERACTION_DEFINED`) |

**Slice State Machine (UC 2.0 lifecycle mapped to worktracker):**

| UC 2.0 State | `$.slice_state` Value | Worktracker Status | Entry Criteria | Exit Criteria |
|-------------|----------------------|-------------------|----------------|---------------|
| Scoped | `SCOPED` | `draft` | Slice identified from use case flows | INVEST criteria verified |
| Prepared | `PREPARED` | `ready` | Test cases defined; narrative enhanced | Stakeholder approval for implementation |
| Analyzed | `ANALYZED` | `in-progress` | System elements identified (Activity 5, realization) | Realization artifact produced (`$.interactions` block) |
| Implemented | `IMPLEMENTED` | `review` | Software built and unit tested | Integration test passed |
| Verified | `VERIFIED` | `done` | Acceptance tests passed | Regression tests passed |

Source: S-01 (UC 2.0 slice lifecycle, pp. 15-16); PAT-006 (Jerry entity mapping).

**Schema-Integrated Input/Output**

| Direction | Content | Schema Fields (JSON Path) | Validation |
|-----------|---------|--------------------------|------------|
| Input | Use case artifact at `$.detail_level` >= `ESSENTIAL_OUTLINE`. Must have: `$.basic_flow[*]`, `$.extensions[*]` (at minimum). Optionally: existing `$.slices[*]` for iterative refinement. | Reads: `$.basic_flow[*]`, `$.alternative_flows[*]`, `$.extensions[*]`, `$.primary_actor`, `$.supporting_actors[*]`, `$.detail_level`, `$.preconditions[*]`, `$.postconditions` | Input must satisfy schema `required` array. Agent guardrail rejects if `$.detail_level` < `ESSENTIAL_OUTLINE`. |
| Output | Updated use case artifact with `$.slices[*]` section and optionally `$.interactions[*]` section. Sets `$.slice_state`, `$.realization_level`, `$.slice_ids[*]`. | Writes: `$.slices[*]` (`$defs/slice`), `$.interactions[*]` (`$defs/interaction`), `$.slice_state`, `$.realization_level`, `$.slice_ids[*]`, `$.updated_at`, `$.last_modified_by` | Output MUST validate against `shared-schema.json`. When `$.realization_level` is set to `STORY_DEFINED` or `INTERACTION_DEFINED`, allOf constraint 2 requires `$.slices` with minItems: 1. When `$.realization_level` is set to `INTERACTION_DEFINED`, allOf constraint 1 requires `$.interactions` with minItems: 1. |

**Guardrails (Beyond Constitutional Triplet)**

| Guardrail | Schema Enforcement | Source |
|-----------|-------------------|--------|
| MUST NOT slice a use case at `$.detail_level` < `ESSENTIAL_OUTLINE` | Agent guardrail (not schema-enforced): rejects input where `$.detail_level` is `BRIEFLY_DESCRIBED` or `BULLETED_OUTLINE` | DI-01 |
| MUST include basic flow as the first slice | Agent guardrail: `$.slices[0].steps_included` must reference `basic_flow` | S-01 p. 8 |
| MUST verify each slice has at least one test case before marking as "Prepared" | Agent guardrail: `$.slices[*].test_cases` must be non-empty when `$.slice_state` >= `PREPARED` | S-01 Activity 4 |
| MUST map `$.slice_state` to worktracker entity status | Agent guardrail (procedural) | PAT-006 |
| MUST produce `$.interactions[*]` block when advancing a slice to Analyzed state | Schema conditional enforcement: allOf constraint 1 requires `$.interactions` (minItems: 1) when `$.realization_level` = `INTERACTION_DEFINED`. Each `$defs/interaction` must include all 7 required fields: `.id`, `.source_step`, `.source_flow`, `.actor_role`, `.system_role`, `.request_description`, `.response_description`. | S-01 Activity 5, DI-08, AI-05 |
| MUST satisfy allOf constraints 1 and 2 when setting `$.realization_level` | Schema validation: constraint 1 (interactions at INTERACTION_DEFINED), constraint 2 (slices at STORY_DEFINED+) | shared-schema.json allOf |

---

### Skill 2: /test-spec

#### Agent 2.1: `tspec-generator`

**Identity**

| Field | Value | Source |
|-------|-------|--------|
| Role | BDD Test Specification Generator -- transforms use case artifacts into Gherkin BDD scenarios using Clark's (2018) UC2.0-to-Gherkin mapping | DI-05, PAT-008 |
| Expertise (1) | Clark (2018) UC2.0-to-Gherkin transformation algorithm (basic flow to happy path, alternative flow to additional scenario, extension to error scenario) | S-03 (Clark mapping table) |
| Expertise (2) | BDD/Gherkin specification writing (Feature/Scenario/Given-When-Then structure, declarative style, Cucumber best practices) | S-03 (Adzic 2016 data, Cucumber principles) |
| Expertise (3) | 7 Cs quality framework application to generated test specifications (C1 Coverage as primary criterion) | S-03, DI-06, PAT-004 |
| Cognitive Mode | **Systematic** -- applies Clark's mapping algorithm as a deterministic lookup table. Each use case flow maps to a specific scenario type. The transformation is a step-by-step procedure, not creative generation. | AD-M-009 taxonomy, R-09 |

**Model Selection: Sonnet**

Justification (AD-M-009): The Clark transformation is a structured mapping with well-defined rules. Sonnet handles procedural, checklist-style work effectively. Opus is unnecessary because the mapping does not require complex reasoning. Haiku would be insufficient because the agent needs to correctly interpret use case flow semantics.

**Tool Tier: T2 (Read-Write)**

Justification: Reads use case artifacts (shared format); writes BDD feature files (`.feature.md`) and optional test plan documents (`.md`). No external research needed. No cross-session state. No delegation.

Tools: Read, Write, Edit, Glob, Grep, Bash

**Methodology Outline (Key Steps)**

The Clark (2018) UC2.0-to-Gherkin transformation algorithm:

| Step | Action | Clark Mapping Rule | Schema Fields Read |
|------|--------|--------------------|-------------------|
| 1 | **Validate input** | Check `$.detail_level` >= `ESSENTIAL_OUTLINE`; reject if insufficient | `$.detail_level`, `$.extensions` (presence check) |
| 2 | **Extract Feature** | Use case title becomes Feature title; use case goal becomes Feature description; primary actor becomes scenario subject | `$.title`, `$.goal_level`, `$.primary_actor` |
| 3 | **Map basic flow to happy path** | Basic flow steps become a single Scenario: Given (`$.preconditions[*]`), When (`$.trigger` + `$.basic_flow[*]` where `.type` = `actor_action`), Then (`$.postconditions.success[*]` + `$.basic_flow[*]` where `.type` = `system_response` or `validation`) | `$.basic_flow[*]` (`.step`, `.actor`, `.action`, `.type`), `$.preconditions[*]`, `$.postconditions.success[*]`, `$.trigger` |
| 4 | **Map each alternative flow to additional scenario** | Each `$.alternative_flows[*]` becomes its own Scenario: Given (preconditions + `$.alternative_flows[*].condition`), When (`.steps[*]`), Then (outcome based on `.rejoins_at_step`) | `$.alternative_flows[*]` (`.id`, `.name`, `.branches_from_step`, `.condition`, `.steps[*]`, `.rejoins_at_step`) |
| 5 | **Map each extension to error scenario** | Each `$.extensions[*]` condition becomes a negative test Scenario, with scenario type determined by `.outcome` (`failure` -> negative, `success` -> alternate positive, `rejoin:{N}` -> additional with merge) | `$.extensions[*]` (`.id`, `.name`, `.anchor_step`, `.condition`, `.steps[*]`, `.outcome`) |
| 6 | **Apply Cockburn step-anchor naming** | Scenario names reference source step numbers for traceability | `$.extensions[*].anchor_step`, `$.alternative_flows[*].branches_from_step` |
| 7 | **Quality check against 7 Cs** | Verify C1 Coverage (all flows mapped), C4 Consistent Abstraction, C5/C6 Consistent Structure | All flow fields |

**Clark Mapping Table (Deterministic):**

| Use Case Element | Schema Source | Gherkin Element | Cardinality |
|-----------------|--------------|-----------------|-------------|
| `$.title` | Identity block | Feature title | 1:1 |
| `$.goal_level` description | Classification block | Feature description | 1:1 |
| `$.basic_flow[*]` | Flows block | Happy path Scenario | 1:1 |
| `$.alternative_flows[*]` | Flows block | Additional Scenario | 1:1 per alternative |
| `$.extensions[*]` | Flows block | Error/negative Scenario | 1:1 per extension |
| `$.preconditions[*]` | Conditions block | Given clauses | 1:N |
| `$.postconditions.success[*]` | Conditions block | Then clauses | 1:N |
| `$.primary_actor` | Actors block | Scenario subject ("As a {actor}") | 1:1 |

**Slice-Scoped Generation:**

When `$.slices[*]` are present, `tspec-generator` can generate feature files scoped to a specific slice rather than the entire use case:

| Input | Behavior | Schema Fields |
|-------|----------|---------------|
| Full use case (no slice specified) | Generate Feature covering all flows | `$.basic_flow`, `$.alternative_flows`, `$.extensions` |
| Specific slice ID | Generate Feature covering only the steps in `$.slices[N].steps_included[*]` | `$.slices[N].steps_included[*].flow`, `$.slices[N].steps_included[*].steps[*]` -> cross-referenced against `$.basic_flow`, `$.alternative_flows`, `$.extensions` to extract matching steps |

**Output Cardinality (G-03 Resolution):**

- 1 Feature file per use case (or per slice when slice-scoped)
- 1 Scenario per flow (basic flow, each alternative, each extension)
- Feature file path: `projects/${JERRY_PROJECT}/test-specs/{UC-NNN}-{slug}.feature.md`
- Optional test plan document: `projects/${JERRY_PROJECT}/test-specs/{UC-NNN}-{slug}-test-plan.md`

**Schema-Integrated Input/Output**

| Direction | Content | Schema Fields (JSON Path) | Validation |
|-----------|---------|--------------------------|------------|
| Input | Use case artifact at `$.detail_level` >= `ESSENTIAL_OUTLINE` | Reads: `$.id`, `$.title`, `$.goal_level`, `$.primary_actor`, `$.basic_flow[*]` (each: `.step`, `.actor`, `.action`, `.type`), `$.alternative_flows[*]` (each: `.id`, `.name`, `.branches_from_step`, `.condition`, `.steps[*]`, `.rejoins_at_step`), `$.extensions[*]` (each: `.id`, `.name`, `.anchor_step`, `.condition`, `.steps[*]`, `.outcome`), `$.preconditions[*]`, `$.postconditions` (`.success[*]`, `.failure[*]`), `$.trigger`, `$.slices[*]` (optional, for slice-scoped generation) | Agent guardrail rejects if: (a) `$.detail_level` < `ESSENTIAL_OUTLINE`, (b) `$.extensions` is absent or empty, (c) `$.basic_flow` has < 3 items. Schema `required` array provides base validation. |
| Output | (1) Gherkin Feature file (`.feature.md`). (2) Optional: test plan document with coverage matrix. | External files -- not written back to the use case artifact's YAML frontmatter. No schema fields modified. | Feature file structure validated by agent self-review (7 Cs). |

**Guardrails (Beyond Constitutional Triplet)**

| Guardrail | Schema Enforcement | Source |
|-----------|-------------------|--------|
| MUST NOT generate scenarios from use cases at `$.detail_level` < `ESSENTIAL_OUTLINE` | Agent guardrail: rejects input where `$.detail_level` in [`BRIEFLY_DESCRIBED`, `BULLETED_OUTLINE`] | PAT-008, DI-05 |
| MUST include traceability from each Scenario to source step number | Uses `$.extensions[*].anchor_step`, `$.alternative_flows[*].branches_from_step`, `$.basic_flow[*].step` | S-03 (Clark step-anchor naming) |
| MUST verify C1 Coverage: every flow produces at least one Scenario | Coverage verified against: count(`$.basic_flow`) = 1 happy path + count(`$.alternative_flows`) + count(`$.extensions`) scenarios | DI-06, PAT-004 |
| MUST use declarative Given-When-Then style (what, not how) | Agent guardrail (style, not schema-enforced) | S-03 (Cucumber declarative principle) |
| MUST reject use cases without at least one `$.extensions[*]` entry | Agent guardrail: rejects when `$.extensions` is absent or empty | PAT-002 |
| `$.basic_flow[*].type` determines Gherkin clause mapping | Schema-enforced enum: `actor_action` -> When, `system_response` -> Then, `validation` -> Then (assertion) per SD-07 | PAT-008, SD-07 |
| `$.extensions[*].outcome` determines Scenario type | Schema-enforced pattern: `failure` -> negative scenario, `success` -> alternate success, `rejoin:{N}` -> additional with merge per SD-08 | PAT-008, SD-08 |

---

### Skill 3: /contract-design

#### Agent 3.1: `cd-generator`

**Identity**

| Field | Value | Source |
|-------|-------|--------|
| Role | API Contract Generator -- transforms use case realization artifacts into OpenAPI 3.x contract specifications using a novel UC-to-contract transformation algorithm | DI-07, DI-08, R-06 |
| Expertise (1) | Use case realization interpretation (Activity 5 "Interaction Defined" level: system elements, responsibilities, interaction sequences) | S-01 (Activity 5 Expanded) |
| Expertise (2) | OpenAPI 3.x specification authoring (paths, operations, request/response schemas, component reuse) | DI-07 (REST-only initial scope) |
| Expertise (3) | Actor-role-to-contract-role mapping (primary actor as consumer, system as provider, interaction steps as operations) | R-06 (novel algorithm), G-01 |
| Cognitive Mode | **Convergent** -- evaluates interaction steps in the realization artifact and converges on the optimal contract structure. Each interaction step presents options (operation granularity, path structure, schema design) that must be resolved through focused evaluation and criteria-based selection. | AD-M-009 taxonomy |

**Model Selection: Opus**

Justification (AD-M-009): This is the highest-risk skill (G-01 gap -- no prior art). The transformation algorithm is novel and requires complex reasoning to map use case interaction semantics to API contract structures. Unlike the Clark mapping (deterministic lookup), the UC-to-contract mapping requires judgment about operation granularity, resource identification, and schema structure. Opus is warranted for complex reasoning tasks with no established procedural template.

**Tool Tier: T2 (Read-Write)**

Justification: Reads use case realization artifacts (shared format); writes OpenAPI 3.x YAML files. No external research needed for the transformation itself (the algorithm is embedded in the agent definition). No cross-session state. No delegation.

Tools: Read, Write, Edit, Glob, Grep, Bash

**Methodology Outline (Key Steps)**

The novel UC-to-contract transformation algorithm (R-06, DI-08, G-01):

| Step | Action | Mapping Rule | Schema Fields Read |
|------|--------|-------------|-------------------|
| 1 | **Validate input** | Check `$.realization_level` = `INTERACTION_DEFINED` or `$.interactions[*]` present; check `$.detail_level` >= `ESSENTIAL_OUTLINE` | `$.realization_level`, `$.interactions`, `$.detail_level` |
| 2 | **Identify resources** | Each system element that receives messages in the realization becomes a candidate API resource | `$.interactions[*].system_role` (where = `receiver`), `$.interactions[*].request_description` |
| 3 | **Map interaction steps to operations** | Each `$.interactions[*]` where `$.interactions[*].actor_role` = `consumer` maps to an HTTP operation. Interactions where actor is provider document internal operations. | `$.interactions[*].actor_role`, `$.interactions[*].system_role`, `$.interactions[*].source_step`, `$.interactions[*].source_flow` |
| 4 | **Derive HTTP methods** | Operation semantics from `$.interactions[*].request_description` determine HTTP method: read/query -> GET; create -> POST; update -> PUT/PATCH; delete -> DELETE | `$.interactions[*].request_description` |
| 5 | **Extract request schemas** | Interaction preconditions + request description become request body/query parameter schemas | `$.interactions[*].preconditions[*]`, `$.interactions[*].request_description` |
| 6 | **Extract response schemas** | Interaction postconditions + response description become response schemas | `$.interactions[*].postconditions[*]`, `$.interactions[*].response_description` |
| 7 | **Map extensions to error responses** | Cross-reference `$.interactions[*].source_step` and `$.interactions[*].source_flow` against `$.extensions[*].anchor_step` to identify extension conditions that become 4xx/5xx responses | `$.extensions[*]` (`.anchor_step`, `.condition`, `.outcome`), `$.interactions[*].source_step`, `$.interactions[*].source_flow` |
| 8 | **Resolve supporting actor roles (IC-05)** | Cross-reference `$.interactions[*].actor_role` = `provider` against `$.supporting_actors[*]` to identify external dependencies. Map to OpenAPI `components/schemas` descriptions. | `$.supporting_actors[*]` (`.name`, `.type`), `$.interactions[*].actor_role` |
| 9 | **Compose and validate OpenAPI document** | Assemble paths, operations, components/schemas, info section. Validate against OpenAPI 3.x specification. | All read fields assembled into external `.openapi.yaml` |

**Actor-to-Contract-Role Mapping:**

| Use Case Schema Field | Schema Path | Contract Element | Source |
|----------------------|-------------|-----------------|--------|
| Primary actor | `$.primary_actor` | API consumer (the caller) | R-06 |
| System (receiving) | `$.interactions[*].system_role` = `receiver` | API provider (the server) | R-06 |
| Supporting actor | `$.supporting_actors[*]` cross-referenced with `$.interactions[*].actor_role` = `provider` | External dependency (documented in `components/schemas`) | R-06, IC-05 |
| Interaction step (actor -> system) | `$.interactions[*]` where `.actor_role` = `consumer` | Path + Operation (external endpoint) | R-06 |
| Interaction step (system -> system) | `$.interactions[*]` where `.actor_role` = `provider` and `.system_role` = `provider` | Internal operation (documented in `x-internal-operations`, not exposed as path) | R-06 |
| Interaction precondition | `$.interactions[*].preconditions[*]` | Request validation (required fields, format constraints) | R-06 |
| Interaction postcondition | `$.interactions[*].postconditions[*]` | Response schema (success payload) | R-06 |
| Extension condition | `$.extensions[*].condition` (where `.outcome` = `failure`) | Error response (4xx/5xx with error detail schema) | R-06 |

**Scope Constraint (DI-07, ASM-005):**

- **Initial release:** REST (OpenAPI 3.x) only
- **Deferred:** AsyncAPI, CloudEvents, event-driven contracts
- **Reason:** G-02 gap (multi-actor pub/sub behavior mapping) unresolved.

**Schema-Integrated Input/Output**

| Direction | Content | Schema Fields (JSON Path) | Validation |
|-----------|---------|--------------------------|------------|
| Input | Use case artifact with realization at `INTERACTION_DEFINED` level | Reads: `$.interactions[*]` (each: `.id`, `.source_step`, `.source_flow`, `.actor_role`, `.system_role`, `.request_description`, `.response_description`, `.preconditions[*]`, `.postconditions[*]`), `$.primary_actor`, `$.supporting_actors[*]` (`.name`, `.type`), `$.extensions[*]` (`.anchor_step`, `.condition`, `.outcome`), `$.detail_level`, `$.realization_level`, `$.id`, `$.title`, `$.scope` | Agent guardrail rejects if: (a) `$.interactions` is absent or empty, (b) `$.detail_level` < `ESSENTIAL_OUTLINE`. Schema allOf constraint 1 enforces `$.interactions` presence when `$.realization_level` = `INTERACTION_DEFINED`. Agent performs cross-reference validation: each `$.interactions[*].source_step` must reference an existing step in the flow identified by `$.interactions[*].source_flow`. |
| Output | (1) OpenAPI 3.x YAML file. (2) Mapping document showing traceability from each `$.interactions[*].id` to each API operation. | External files -- not written back to the use case artifact. No schema fields modified. | OpenAPI output validated against OpenAPI 3.x specification schema. Mapping document traces every `$.interactions[*].id` to an API path+operation. |

Output paths:
- Contract: `projects/${JERRY_PROJECT}/contracts/{UC-NNN}-{slug}-api.yaml`
- Mapping: `projects/${JERRY_PROJECT}/contracts/{UC-NNN}-{slug}-mapping.md`

**Guardrails (Beyond Constitutional Triplet)**

| Guardrail | Schema Enforcement | Source |
|-----------|-------------------|--------|
| MUST NOT generate contracts from use cases without `$.interactions[*]` block | Schema allOf constraint 1: `$.interactions` required (minItems: 1) at `INTERACTION_DEFINED`. Agent guardrail also rejects if `$.interactions` absent regardless of `$.realization_level` setting. | S-01 Activity 5 |
| MUST label generated contracts as "PROTOTYPE" until validated by human review | Agent guardrail: adds `x-prototype: true` to OpenAPI info section | G-01, LES-001 |
| MUST include traceability from each API operation to `$.interactions[*].id` | Agent guardrail: mapping document required alongside OpenAPI | R-06 |
| MUST NOT generate AsyncAPI or event-driven contracts in initial release | Agent guardrail: rejects requests mentioning async/event-driven patterns | DI-07, ASM-005 |
| MUST validate generated OpenAPI against OpenAPI 3.x specification schema | Agent guardrail: runs Bash validation step | DI-08 |
| MUST flag `$.interactions[*]` where `.actor_role` = `provider` as internal operations | Agent guardrail: maps to `x-internal-operations`, not exposed as external paths | R-06 |
| MUST resolve supporting actor roles via IC-05 cross-reference | Agent guardrail: cross-references `$.interactions[*].actor_role` with `$.supporting_actors[*]` | IC-05 |

---

### Progressive Realization Matrix

This matrix shows how each agent advances a use case document through the three realization levels defined in `shared-schema.json` (`$.realization_level` enum), with the specific schema fields added at each transition.

| Agent | Input Realization Level | Output Realization Level | Schema Fields Added at Transition | allOf Constraints Activated |
|-------|------------------------|-------------------------|----------------------------------|---------------------------|
| `uc-author` (Level 1-2) | None (new artifact) | `OUTLINED` | `$.id`, `$.title`, `$.work_type`, `$.version`, `$.status`, `$.goal_level`, `$.scope`, `$.primary_actor`, `$.basic_flow[*]`, `$.created_at`, `$.created_by` + optional: `$.goal_symbol`, `$.detail_level`, `$.domain`, `$.supporting_actors[*]`, `$.trigger` | Constraints 3/4/5 (goal_symbol consistency) if `$.goal_symbol` is set |
| `uc-author` (Level 3-4) | `OUTLINED` | `OUTLINED` (enriched) | `$.extensions[*]`, `$.alternative_flows[*]`, `$.preconditions[*]`, `$.postconditions`, `$.stakeholders[*]`, `$.detail_level` upgraded to `ESSENTIAL_OUTLINE` or `FULLY_DESCRIBED` | None (realization_level remains OUTLINED until slicing) |
| `uc-slicer` (Activities 2+4) | `OUTLINED` (with `$.detail_level` >= `ESSENTIAL_OUTLINE`) | `STORY_DEFINED` | `$.slices[*]` (each: `.slice_id`, `.title`, `.steps_included[*]`, `.invest_assessment`, `.test_cases[*]`, `.realization_level` = `STORY_DEFINED`), `$.slice_state`, `$.slice_ids[*]`, `$.realization_level` = `STORY_DEFINED` | Constraint 2: `$.slices` required with minItems: 1 |
| `uc-slicer` (Activity 5) | `STORY_DEFINED` | `INTERACTION_DEFINED` | `$.interactions[*]` (each: `.id`, `.source_step`, `.source_flow`, `.actor_role`, `.system_role`, `.request_description`, `.response_description` + optional: `.preconditions[*]`, `.postconditions[*]`), `$.slices[*].realization_level` -> `INTERACTION_DEFINED`, `$.realization_level` = `INTERACTION_DEFINED` | Constraint 1: `$.interactions` required with minItems: 1. Constraint 2: `$.slices` still required. |
| `tspec-generator` | `STORY_DEFINED` minimum (reads `$.basic_flow`, `$.extensions`, `$.alternative_flows`) | N/A (external output) | No schema fields modified -- produces external `.feature.md` files | N/A (read-only consumer) |
| `cd-generator` | `INTERACTION_DEFINED` (reads `$.interactions[*]`, `$.supporting_actors[*]`) | N/A (external output) | No schema fields modified -- produces external `.openapi.yaml` files | N/A (read-only consumer) |

**Key design property:** Only `/use-case` agents (uc-author, uc-slicer) write to the shared artifact's YAML frontmatter. Downstream skills (`/test-spec`, `/contract-design`) are read-only consumers that produce separate output files. This prevents downstream skills from corrupting the shared artifact.

---

### Schema Constraint Responsibility Map

The five `allOf` conditional constraints in `shared-schema.json` and the agents responsible for satisfying each:

| # | Constraint | `if` Condition | `then` Requirement | Responsible Agent | When Triggered |
|---|-----------|---------------|-------------------|-------------------|----------------|
| 1 | Interactions required at INTERACTION_DEFINED | `$.realization_level` = `INTERACTION_DEFINED` | `$.interactions` required, minItems: 1 | `uc-slicer` (Activity 5, methodology step 7) | When `uc-slicer` advances a slice through Activity 5 and sets `$.realization_level` = `INTERACTION_DEFINED` |
| 2 | Slices required at STORY_DEFINED+ | `$.realization_level` in [`STORY_DEFINED`, `INTERACTION_DEFINED`] | `$.slices` required, minItems: 1 | `uc-slicer` (Activities 2+4, methodology steps 1-6) | When `uc-slicer` creates slices and sets `$.realization_level` = `STORY_DEFINED` or higher |
| 3 | Goal symbol matches SUMMARY | `$.goal_level` = `SUMMARY` AND `$.goal_symbol` present | `$.goal_symbol` = `+` | `uc-author` (methodology step 3) | When `uc-author` sets both `$.goal_level` and `$.goal_symbol` |
| 4 | Goal symbol matches USER_GOAL | `$.goal_level` = `USER_GOAL` AND `$.goal_symbol` present | `$.goal_symbol` = `!` | `uc-author` (methodology step 3) | When `uc-author` sets both fields |
| 5 | Goal symbol matches SUBFUNCTION | `$.goal_level` = `SUBFUNCTION` AND `$.goal_symbol` present | `$.goal_symbol` = `-` | `uc-author` (methodology step 3) | When `uc-author` sets both fields |

**Constraints not encoded in schema (enforced by agent guardrails):**

| Constraint | Why Not in Schema | Responsible Agent |
|-----------|-------------------|-------------------|
| `$.detail_level` >= `ESSENTIAL_OUTLINE` for `/test-spec` input | Schema validates structure, not agent-specific preconditions | `tspec-generator` input validation (SR-002) |
| `$.detail_level` >= `ESSENTIAL_OUTLINE` for `/contract-design` input | Same rationale | `cd-generator` input validation (SR-002) |
| `$.extensions` non-empty for `/test-spec` input | Having 0 extensions is structurally valid; the agent decides completeness | `tspec-generator` guardrail |
| `$.interactions[*].source_step` references existing step in `$.interactions[*].source_flow` | Cross-array referential integrity beyond JSON Schema capability | `cd-generator` input validation |
| `$.basic_flow[*].actor` matches `$.primary_actor` or `$.supporting_actors[*].name` | Cross-field reference validation beyond JSON Schema practical capability | `uc-author` output validation |

---

### Agent Interaction Model

#### Intra-Skill Interaction: `/use-case` (2 agents)

```
Main Context (Orchestrator)
    |
    +-- uc-author (creates/elaborates use case artifact)
    |       |
    |       v  [artifact file on disk, validated against shared-schema.json]
    |
    +-- uc-slicer (reads artifact, adds slices + interactions)
            |
            v  [updated artifact file, re-validated against shared-schema.json]
```

**Interaction Pattern:** Sequential file-mediated handoff with schema validation at each boundary. The orchestrator invokes `uc-author` first. Once the artifact reaches `$.detail_level` >= `ESSENTIAL_OUTLINE`, the orchestrator invokes `uc-slicer`. Both agents validate their output against `shared-schema.json` before writing. The two agents never communicate directly -- all coordination flows through the main context and the shared artifact file on disk. P-003 compliant (single-level nesting: main context -> worker).

**Within-Skill Agent Selection Criterion:**

| User Intent | Agent | Decision Signal |
|-------------|-------|----------------|
| Creating, writing, or elaborating a use case | `uc-author` | Keywords: "write", "create", "author", "elaborate", "expand", "describe", "draft", "refine" a use case. Note: "refine" is ambiguous -- default to `uc-author`; switch to `uc-slicer` if user clarifies decomposition intent. |
| Decomposing into slices, managing lifecycle, producing realization | `uc-slicer` | Keywords: "slice", "decompose", "break down", "split into stories", "prepare slice", "analyze slice", "realize" |
| Ambiguous or combined request | `uc-author` first, then `uc-slicer` | Default pipeline order: authoring precedes slicing |

**Handoff Data (uc-author -> uc-slicer, via orchestrator):**

| Field | Value |
|-------|-------|
| artifact_path | `projects/${JERRY_PROJECT}/use-cases/{UC-NNN}-{slug}.md` |
| detail_level | `$.detail_level` >= `ESSENTIAL_OUTLINE` |
| key_findings | Actor-goal list, basic flow summary, extension count |
| success_criteria | At least 1 slice identified; basic flow is first slice; each slice has INVEST assessment |
| schema_validation | Artifact passes `shared-schema.json` validation before handoff |

#### Cross-Skill Interaction: Pipeline with Schema Validation Gates

```
/use-case           /test-spec          /contract-design
    |                   |                    |
uc-author ---+     tspec-generator         cd-generator
             |          ^                    ^
uc-slicer ---+          |                    |
             |          |                    |
             v          |                    |
    [UC Artifact]-------+--------------------+
    (shared-schema.json validated)
         |
    Schema Gates:
    - /test-spec requires: $.detail_level >= ESSENTIAL_OUTLINE
    - /contract-design requires: $.realization_level = INTERACTION_DEFINED
```

**Cross-Skill Handoff Data:**

| From | To | Key Data | Schema Pre-Condition |
|------|----|----------|---------------------|
| `/use-case` | `/test-spec` | artifact_path, `$.detail_level` >= `ESSENTIAL_OUTLINE`, `$.extensions` present | Artifact validates against `shared-schema.json`. Agent guardrail: `$.detail_level` not in [`BRIEFLY_DESCRIBED`, `BULLETED_OUTLINE`]. |
| `/use-case` (via `uc-slicer` Activity 5) | `/contract-design` | artifact_path, `$.realization_level` = `INTERACTION_DEFINED`, `$.interactions[*]` populated | Artifact validates against `shared-schema.json` including allOf constraint 1 (`$.interactions` required at INTERACTION_DEFINED). Agent guardrail: cross-reference validation on `$.interactions[*].source_step`. |

**Parallel execution:** Steps to `/test-spec` and `/contract-design` can run in parallel (both read the same artifact; neither modifies it). The orchestrator decides sequencing based on user request.

---

### Trigger Map Extensions

New entries for `mandatory-skill-usage.md` trigger map. Priority >= 13 per synthesis recommendation R-07, DI-10 (above current maximum of 12 for `/user-experience`).

**Routing 2-level gap analysis:** Per `agent-routing-standards.md` routing algorithm Step 3, a 2-level gap between priority values is needed for unambiguous resolution. The gap between existing `/user-experience` (priority 12) and the new `/use-case` (priority 13) is only 1 level. This is acceptable because: (a) the compound triggers for `/use-case` require "use case" co-occurrence, which is semantically distinct from `/user-experience` keywords; (b) the negative keywords on both skills suppress cross-matches; (c) in the unlikely event of a residual collision, Layer 2 escalation provides the appropriate resolution path.

#### `/use-case` -- Priority 13

| Column | Value |
|--------|-------|
| **Detected Keywords** | use case, use-case, write use case, create use case, author use case, use case model, actor goal list, basic flow, main success scenario, alternative flow, extension, extension handling, fully dressed, casual use case, briefly described, sea level goal, goal level, use case slice, slice use case, UC 2.0, cockburn, jacobson |
| **Negative Keywords** | requirements specification, V&V, technical review, trade study, compliance, test spec, BDD, Gherkin, scenario, OpenAPI, contract, API design, schema, adversarial, tournament, transcript, penetration, exploit, code review, documentation, tutorial |
| **Priority** | 13 |
| **Compound Triggers** | "write use case" OR "create use case" OR "author use case" OR "use case model" OR "actor goal" OR "basic flow" OR "main success scenario" OR "use case slice" (phrase match) |
| **Skill** | `/use-case` |

#### `/test-spec` -- Priority 14

| Column | Value |
|--------|-------|
| **Detected Keywords** | test spec, test specification, BDD, BDD scenario, Gherkin, feature file, Given When Then, happy path, error scenario, negative test, test case from use case, Clark mapping, scenario mapping, test coverage, acceptance test, specification by example |
| **Negative Keywords** | requirements, V&V, compliance, use case model, actor goal, write use case, create use case, OpenAPI, contract, API design, adversarial, tournament, transcript, penetration, exploit, code review, unit test, integration test, pytest, jest |
| **Priority** | 14 |
| **Compound Triggers** | "test specification" OR "BDD scenario" OR "Gherkin scenario" OR "Given When Then" OR "test case from use case" OR "specification by example" (phrase match) |
| **Skill** | `/test-spec` |

#### `/contract-design` -- Priority 15

| Column | Value |
|--------|-------|
| **Detected Keywords** | contract design, API contract, OpenAPI, API spec, API specification, generate contract, contract from use case, API schema, endpoint design, operation mapping, request response schema, API generation, REST contract, swagger |
| **Negative Keywords** | requirements, V&V, compliance, use case model, actor goal, write use case, BDD, Gherkin, scenario, test spec, adversarial, tournament, transcript, penetration, exploit, code review, pricing model, cloud pricing |
| **Priority** | 15 |
| **Compound Triggers** | "API contract" OR "contract design" OR "OpenAPI" OR "generate contract" OR "contract from use case" OR "API specification" (phrase match) |
| **Skill** | `/contract-design` |

**Collision Analysis:** See `agent-decomposition-draft.md` Trigger Map Extensions section for detailed per-skill collision analysis against existing skills (`/nasa-se`, `/eng-team`, `/problem-solving`, `/pm-pmm`).

---

## L2: Architectural Rationale

### Schema Traceability: From Methodology to Validation

The progressive realization model creates a traceable chain from methodology source through schema field to agent validation:

```
Cockburn 12-Step (S-02)         Jacobson UC 2.0 (S-01)        Clark 2018 (S-03)
        |                              |                            |
        v                              v                            v
  uc-author produces           uc-slicer produces           tspec-generator reads
  Identity/Classification/     Slicing/Interactions         Flows/Conditions
  Actors/Conditions/Flows      blocks                       blocks
        |                              |                            |
        v                              v                            v
  shared-schema.json           shared-schema.json            shared-schema.json
  required[] validation        allOf constraints 1+2         agent guardrail
  (11 required fields)         (conditional requirements)    (detail_level check)
        |                              |                            |
        v                              v                            v
  OUTLINED artifact            STORY_DEFINED /               .feature.md output
                               INTERACTION_DEFINED artifact
```

**Why the schema is the integration contract.** Before the schema, the pipeline relied on narrative descriptions ("the use case must be at Essential Outline level"). With the schema, the pipeline has machine-checkable validation at every boundary:

1. `uc-author` output is validated against the `required` array (11 fields) and basic_flow constraints (3-9 steps) by JSON Schema.
2. `uc-slicer` output activates allOf constraints 1 and 2, which enforce the presence of `$.slices` and `$.interactions` blocks at the appropriate realization levels.
3. `tspec-generator` and `cd-generator` input validation is split between schema enforcement (structural validity) and agent guardrails (semantic prerequisites like detail_level thresholds).

This two-layer validation (schema + agent guardrail) is deliberate per the constraint analysis in `frontmatter-schema.md`: JSON Schema handles structural validation (field presence, type, pattern, enum), while agent guardrails handle semantic validation (cross-field referential integrity, prerequisite logic).

### Design Rationale: Agent Count Decision

The agent count is the most consequential design decision. See `agent-decomposition-draft.md` L2 section for the full Pattern 1 split criteria analysis:

- `/use-case`: 2 agents (uc-author, uc-slicer) -- both methodology size (~2,100 tokens combined) and cognitive mode (integrative vs. systematic) criteria trigger the split.
- `/test-spec`: 1 agent -- neither criterion triggers (~800 tokens, systematic only).
- `/contract-design`: 1 agent -- neither criterion triggers (~1,000 tokens, convergent only).

**Steelman analyses** (S-003, H-16), **pre-mortem analyses** (S-004), and **4 alternative options** (A-D with scored trade-offs) are documented in `agent-decomposition-draft.md` Options Evaluated and L2 sections. These are not duplicated here.

### Schema Version Evolution Path

| Version | Trigger | Scope | Breaking? |
|---------|---------|-------|-----------|
| **1.0.0** (current) | Phase 2 design | Full schema as designed | N/A |
| **1.1.0** | Phase 3 prototype needs additional optional field(s) | Add fields to top-level properties. Add enum values. | No -- `additionalProperties: true` at top level ensures forward compatibility |
| **1.1.0** (alt) | UC 3.0 sixth slice state needed | Add `IDENTIFIED` to `$.slice_state` enum | No -- additive change |
| **2.0.0** | Phase 3 validation gate triggers MAJOR REVISION for interactions block | Redesign `$defs/interaction` structure | **Yes** -- requires updates to `uc-slicer` and `cd-generator` |

**Interactions Block Validation Gate** (cross-reference to `frontmatter-schema.md` and `file-organization.md`):

Validation criterion: 3 representative use cases (spanning 2+ domains, including 1+ with supporting actors) must produce valid OpenAPI from the `$.interactions[*]` block alone, without `cd-generator` inferring unstated structure.

| Outcome | Condition | Schema Action |
|---------|-----------|---------------|
| VALIDATED | All 3 UCs -> valid OpenAPI from interactions alone | Schema remains at v1.0.0 |
| MINOR REVISION | 2/3 succeed; 1 requires missing optional field | Add field; bump to v1.1.0 |
| MAJOR REVISION | 1 or fewer succeed; structural model inadequate | Redesign interactions block; bump to v2.0.0 (requires user approval per P-020) |

**Bootstrap dependency:** The validation gate requires a minimum viable `cd-generator` implementation. Phase 3 sequencing: build minimum viable `cd-generator`, run validation gate, then complete full agent.

### Evolution Path

| Phase | Agent Count | Trigger |
|-------|-----------|---------|
| **Initial (Phase 3)** | 4 (2+1+1) | Current design |
| **Split trigger 1** | 5 | `/use-case` Activity 5 methodology within `uc-slicer` exceeds 1,500 tokens when combined with Activities 2+4 -> split `uc-realizer` from `uc-slicer` |
| **Split trigger 2** | 6 | `/contract-design` AsyncAPI support adds a second cognitive mode -> add `cd-async-generator` |
| **Split trigger 3** | 7 | `/test-spec` adds performance/load test generation -> add `tspec-perf-generator` |
| **Ceiling** | 8-10 | Per ORCHESTRATION_PLAN.md Phase 3 target. Only if validated by usage data. |

---

## Options Evaluated

The full 4-option analysis with scored trade-offs is documented in `agent-decomposition-draft.md` Options Evaluated section. Summary:

| Option | Description | Score | Outcome |
|--------|-------------|-------|---------|
| A | 1 Agent Per Skill (3 Total) | 6/10 | Rejected -- violates Pattern 1 split criteria for `/use-case` |
| **B** | **2 for /use-case, 1 Each for Others (4 Total)** | **8/10** | **RECOMMENDED** -- justified complexity matching framework standards |
| C | Full Decomposition per Phase 3 Target (8+ Total) | 4/10 | Rejected -- premature complexity without validation |
| D | 3 for /use-case (Author + Slicer + Reviewer) (5 Total) | 5/10 | Rejected -- duplicates `/adversary` quality capability |

---

## Risk Assessment

| Risk ID | Skill | Risk | Severity | Likelihood | Mitigation | Source |
|---------|-------|------|----------|------------|------------|--------|
| RISK-01 | `/contract-design` | Novel algorithm produces incorrect or unusable OpenAPI contracts | HIGH | MEDIUM | (1) Opus model. (2) "PROTOTYPE" label. (3) Human review mandatory. (4) Validation gate at 0.85 floor. | G-01, LES-001 |
| RISK-02 | `/use-case` | 2-agent split creates unnecessary handoff overhead | LOW | LOW | File-mediated handoff is a single Read. Revert to 1 agent if metrics show no benefit. | CF-04 |
| RISK-03 | `/test-spec` | Clark mapping produces trivially simple scenarios | MEDIUM | LOW | 7 Cs quality gate (C1 Coverage). Extension exhaustiveness enforced by `uc-author`. | DI-06, PAT-002 |
| RISK-04 | All | Shared schema proves insufficient for downstream transformations | HIGH | LOW | Schema designed with `additionalProperties: true` for forward compatibility. Validation gate catches structural inadequacy early. Version evolution path documented. | AI-01, ASM-001 |
| RISK-05 | All | Routing collisions with existing skills | MEDIUM | LOW | Negative keywords and compound triggers per PAT-005. Priority >= 13. | T-07, DI-10 |
| RISK-06 | `/contract-design` | AsyncAPI requirement surfaces after initial release | LOW | MEDIUM | Scope explicitly deferred per DI-07. Architecture supports extension. | G-02 |
| RISK-07 | `/test-spec` | Agent prefix routing collision if `tspec-` not adopted consistently | MEDIUM | LOW | Resolved: `tspec-` prefix adopted per file-organization.md AP-02 analysis. | AP-02 |
| RISK-08 | `/use-case` -> `/contract-design` | Activity 5 realization unassigned | HIGH | LOW | Resolved: Activity 5 explicitly assigned to `uc-slicer` (methodology step 7, guardrail, schema constraint 1). | S-01 Activity 5 |
| RISK-09 | All | Schema validation fails on artifacts missing optional-but-expected fields (e.g., `$.detail_level` not set) | LOW | MEDIUM | `$.detail_level` has `default: "BULLETED_OUTLINE"` in schema. Agent guardrails validate semantic prerequisites independently of schema-level enforcement. Two-layer validation (schema + guardrail) is the designed mitigation. | New (schema integration) |

---

## Traceability Matrix

### Synthesis Recommendations (R-01 through R-10)

| R-ID | Priority | Recommendation | Addressed? | How |
|------|----------|---------------|------------|-----|
| R-01 | P0 | Design shared artifact format first | **YES** (this deliverable) | `shared-schema.json` is the machine-readable realization; agent I/O tables reference schema fields by JSON path |
| R-02 | P1 | Design file organization | **YES** (via `file-organization.md`) | Agent output paths per `file-organization.md` directory structure |
| R-03 | P1 | Design frontmatter schema + shared-schema.json | **YES** (via `frontmatter-schema.md`) | Schema integrated into all agent specifications in this document |
| R-04 | P1 | Start with 1 agent per skill; split at threshold | **YES** | `/use-case` split justified by Pattern 1; others start with 1 |
| R-05 | P1 | Design Clark transformation as decision tree | **YES** | `tspec-generator` methodology: Clark mapping with schema field traceability |
| R-06 | P1 | Design UC-to-contract transformation algorithm | **YES** | `cd-generator` methodology: 9-step algorithm with schema field traceability |
| R-07 | P1 | Design trigger map entries with compound triggers | **YES** | Trigger map extensions section with collision analysis |
| R-08 | P2 | Confirm AsyncAPI scope | Documented as deferred | `cd-generator` scope constraint: REST-only initial release |
| R-09 | P2 | Confirm worktracker entity compatibility | **YES** | `uc-slicer` methodology: `$.slice_state` to worktracker status mapping |
| R-10 | P2 | Design quality gate integration (7 Cs + S-014) | **YES** | `tspec-generator` guardrails: 7 Cs mapped to S-014 dimensions per ET-03 |

### Synthesis Design Implications (DI-01 through DI-12)

| DI ID | Requirement | How Addressed | Agent(s) | Schema Integration |
|-------|-------------|---------------|----------|-------------------|
| DI-01 | 4 narrative detail levels | `uc-author`: 4 levels mapped to Cockburn 12-step subsets | uc-author | `$.detail_level` enum: 4 values |
| DI-02 | Goal level classification | `uc-author` guardrail: MUST classify every use case | uc-author | `$.goal_level` (required), `$.goal_symbol` + allOf constraints 3/4/5 |
| DI-03 | Slice lifecycle representation | `uc-slicer`: 5-state lifecycle + Activity 5 realization | uc-slicer | `$.slice_state` enum, `$.slices[*]`, `$.interactions[*]`, allOf constraints 1+2 |
| DI-04 | Shared artifact format | All agents use schema-validated shared format | All | `shared-schema.json` validates all artifacts |
| DI-05 | Clark transformation | `tspec-generator`: deterministic Clark mapping | tspec-generator | Reads `$.basic_flow[*].type`, `$.extensions[*].outcome` for mechanical mapping |
| DI-06 | 7 Cs quality framework | `tspec-generator` guardrail: C1 Coverage check | tspec-generator | Coverage verified against flow counts |
| DI-07 | REST-only initial scope | `cd-generator` scope constraint | cd-generator | Reads `$.interactions[*]` only (no async patterns) |
| DI-08 | Novel algorithm prototyping | `cd-generator`: PROTOTYPE label, Opus model | cd-generator | Reads from `$defs/interaction` structure |
| DI-09 | Start with 1, split at threshold | 4 agents; `/use-case` split justified | All | N/A |
| DI-10 | Compound triggers + negative keywords | Trigger map extensions designed | All | N/A |
| DI-11 | Cockburn 12-step backbone | `uc-author` methodology | uc-author | 12 steps mapped to schema fields |
| DI-12 | H-34 dual-file architecture | All agents require `.md` + `.governance.yaml` | All | N/A |

### Gap Closures

| Gap ID | Status | How Addressed |
|--------|--------|---------------|
| G-01 | **MITIGATED** | `cd-generator` methodology with schema-traceable I/O. Opus model. PROTOTYPE label. Validation gate. |
| G-02 | **DEFERRED** | AsyncAPI scoped out. Architecture supports future extension. |
| G-03 | **RESOLVED** | Cardinality: 1 Feature per use case, 1 Scenario per flow. |
| G-04 | **RESOLVED** | `uc-slicer` uses existing worktracker entity types. |
| G-05 | **OUT OF SCOPE** | Stale downstream artifacts noted as known limitation. |

---

## Self-Review Checklist (H-15, S-010)

### Constitutional Compliance

- [x] **P-001 (Truth/Accuracy):** Every schema field reference verified against `shared-schema.json`. All JSON paths are real paths in the schema file.
- [x] **P-002 (File Persistence):** Document persisted to `architecture/agent-decomposition.md`.
- [x] **P-004 (Provenance):** Every design decision traces to synthesis (DI-xx, R-xx), framework standards (AD-M-xxx, Pattern 1), or methodology sources (Cockburn, Jacobson, Clark).
- [x] **P-011 (Evidence-Based):** 4 alternatives evaluated in draft; preserved by reference.
- [x] **P-020 (User Authority):** Status PROPOSED; no decision finalized without user approval.
- [x] **P-022 (No Deception):** Interactions block clearly marked as architecturally speculative. Validation gate cross-referenced. Risk RISK-09 added for schema integration edge case. Bootstrap dependency acknowledged.

### Structural Compliance

- [x] **H-23 (Navigation):** Navigation table present with anchor links.
- [x] **L0/L1/L2:** All three output levels present with appropriate audience depth.
- [x] **DI-01 through DI-12:** All 12 design implications addressed with schema integration column.
- [x] **R-01 through R-10:** All 10 recommendations addressed. R-01/R-03 now fully satisfied (were "not in scope" in draft; schema integration completes them).

### Schema Integration Verification

- [x] **Every agent has schema-referenced I/O table:** All 4 agents have input/output tables with JSON path references to `shared-schema.json`.
- [x] **Progressive Realization Matrix present:** Shows agent -> realization level -> schema fields -> allOf constraints chain.
- [x] **Schema Constraint Responsibility Map present:** All 5 allOf constraints mapped to responsible agents.
- [x] **No invented schema fields:** Every `$.field` reference verified against `shared-schema.json` properties and `$defs`.
- [x] **Agent guardrails reference schema constraints by number:** Constraints 1-5 cited where relevant.
- [x] **Two-layer validation design documented:** Schema validation (structural) + agent guardrails (semantic) documented in L2.
- [x] **$defs references accurate:** `$defs/flow_step`, `$defs/alternative_flow`, `$defs/extension`, `$defs/interaction`, `$defs/slice` all reference actual $defs entries in `shared-schema.json`.

### Draft Preservation Verification

- [x] **Agent count preserved:** 4 agents (2+1+1) unchanged from draft.
- [x] **Cognitive modes preserved:** integrative (uc-author), systematic (uc-slicer, tspec-generator), convergent (cd-generator).
- [x] **Tool tiers preserved:** All T2 (Read-Write).
- [x] **Model selections preserved:** Sonnet (uc-author with AD-M-009 override, uc-slicer, tspec-generator), Opus (cd-generator).
- [x] **Trigger map preserved:** Priorities 13/14/15, all keywords and compound triggers unchanged.
- [x] **Risk register preserved:** RISK-01 through RISK-08 unchanged; RISK-09 added for schema integration.
- [x] **Steelman, pre-mortem, options analyses:** Referenced in draft; not duplicated.

### Adversarial Self-Check (S-002: Devil's Advocate)

**Challenge 1: "Is the Progressive Realization Matrix a new abstraction layer that adds complexity without proportional benefit?"**
The matrix makes explicit what was implicit in the draft: which agent produces which fields at which stage. Without it, Phase 3 implementers must reverse-engineer the flow from methodology step tables. The matrix is a documentation enhancement (one table, ~20 rows), not an architectural addition.

**Challenge 2: "Do the schema validation guardrails create brittle coupling between agents and schema version?"**
The agents reference schema fields by stable JSON paths (`$.basic_flow`, `$.interactions`). If a field is renamed in a schema version bump, the agent definitions must update. This is the intended design: the schema is the integration contract. Renaming a field is a breaking change (major version bump, v2.0.0), which already requires user approval (P-020). The coupling is deliberate and managed.

**Challenge 3: "RISK-09 (optional-but-expected fields missing) is listed as LOW severity -- is that justified?"**
Yes. The schema `default` mechanism handles `$.detail_level` (defaults to `BULLETED_OUTLINE`). Agent guardrails handle other expected-but-optional fields (e.g., `$.extensions` for tspec-generator). The two-layer validation design means no single missing optional field creates a silent failure. The worst case is an agent rejecting input with an actionable error message, which is the correct behavior.

---

*Architecture Version: 1.0.0*
*Lineage: agent-decomposition-draft.md v1.2.0 (0.957 PASS) + frontmatter-schema.md v1.0.0 (0.955 PASS) + file-organization.md v2.1.0 (0.951 PASS) + shared-schema.json v1.0.0*
*Constitutional Compliance: P-001 (truth), P-002 (file persistence), P-003 (no recursive subagents), P-004 (provenance), P-011 (evidence-based alternatives), P-020 (user authority -- PROPOSED status), P-022 (no deception -- speculative block warnings, risks documented)*
*Adversary Review Required: YES -- C4 all-10-strategy review at >= 0.95 threshold*
*Next Agent: adv-scorer (initial scoring)*
*Workflow ID: use-case-skills-20260308-001*
