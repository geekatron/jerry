# Frontmatter Schema Design: Use Case Realization Documents

> **PS ID:** proj-021 | **Entry ID:** architecture-frontmatter-schema | **Workflow ID:** use-case-skills-20260308-001
> **Date:** 2026-03-08 | **Agent:** ps-architect | **Execution Group:** G-03 (Phase 2 Architecture, Step 7)
> **Quality Threshold:** >= 0.95 (C4, user override C-008)
> **Status:** PROPOSED (P-020: user approval required before ACCEPTED)
> **Version:** 1.0.0

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | What the schema is, what it enables, why v1.0.0 |
| [L1: Technical Specification](#l1-technical-specification) | Full field reference, realization-level requirements, enum definitions, validation rules |
| [Schema Field Reference](#schema-field-reference) | Complete field-by-field specification with types and constraints |
| [Required vs. Optional by Realization Level](#required-vs-optional-by-realization-level) | Progressive requirement escalation matrix |
| [Enum Definitions with Sources](#enum-definitions-with-sources) | All enum values traced to methodology sources |
| [Cross-Field Constraints](#cross-field-constraints) | Conditional validation rules encoded in allOf |
| [Downstream Minimum Requirements](#downstream-minimum-requirements) | What /test-spec and /contract-design require to function |
| [L2: Architectural Rationale](#l2-architectural-rationale) | Traceability, schema version reasoning, speculative block analysis |
| [Traceability to R-01](#traceability-to-r-01) | Mapping from synthesis recommendation to schema realization |
| [Traceability to file-organization.md](#traceability-to-file-organizationmd) | Field-level mapping to Shared Artifact Format section |
| [Traceability to agent-decomposition-draft.md](#traceability-to-agent-decomposition-draftmd) | Activity 5, cd-generator input, and actor-role mapping |
| [Schema Version Rationale](#schema-version-rationale) | Why v1.0.0, not 0.x.0 |
| [Interactions Block Validation Gate](#interactions-block-validation-gate) | Cross-reference to concrete prototype criterion |
| [Bootstrap Dependency](#bootstrap-dependency) | Minimum viable cd-generator needed before gate |
| [Options Evaluated](#options-evaluated) | Alternative schema designs considered (P-011) |
| [Self-Review Checklist](#self-review-checklist) | H-15 / S-010 verification |

---

## L0: Executive Summary

This document defines the machine-readable contract that all three new skills -- `/use-case`, `/test-spec`, and `/contract-design` -- share. The contract takes the form of a JSON Schema (Draft 2020-12) that validates the YAML frontmatter of use case realization documents.

**What it is.** The schema file (`shared-schema.json`, co-located with this document) formalizes the YAML frontmatter structure that was defined narratively in the `file-organization.md` Shared Artifact Format section (R-01). Every field, enum, and constraint in the JSON Schema traces directly to a specific line in that document or to the source methodologies (Cockburn 2001, Jacobson 2011, Clark 2018).

**What it enables.** With this schema, three things become possible that were not possible before:

1. **CI validation.** Use case artifacts can be validated at the L5 enforcement layer (commit/CI) by running JSON Schema validation against the YAML frontmatter, the same way agent governance files are validated today against `agent-governance-v1.schema.json`.

2. **Pre-flight input validation.** When `/test-spec` or `/contract-design` receives a use case artifact, the agent can validate the frontmatter against the schema before attempting transformation. If the artifact is at the wrong detail level or missing required fields for that skill's transformation, the agent rejects with an actionable error message rather than producing incorrect output.

3. **Shared vocabulary.** The schema establishes a single vocabulary for use case concepts across all three skills. `detail_level` means the same thing in `/use-case`, `/test-spec`, and `/contract-design`. `actor_role` in the interactions block maps to contract roles via a defined mapping, not agent interpretation.

**Why v1.0.0.** The schema starts at version 1.0.0 (not 0.x.0) because the core blocks -- Identity, Classification, Actors, and Flows -- are grounded in methodology with 20+ years of industry validation. These blocks are not speculative. The one speculative block (Interactions) is acknowledged as such both in the schema descriptions and in the validation gate defined by `file-organization.md`. If the interactions block requires restructuring after Phase 3 prototyping, the schema receives a minor version bump (1.1.0) for backward-compatible changes or a major bump (2.0.0) for breaking changes. The version rationale is documented in detail in `file-organization.md` Schema Version Rationale section.

---

## L1: Technical Specification

### Schema File Location

| Item | Path |
|------|------|
| JSON Schema (this deliverable) | `projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/architecture/shared-schema.json` |
| Production schema (Phase 3 deliverable) | `docs/schemas/use-case-realization-v1.schema.json` |

The schema file produced with this document is the design-phase artifact. During Phase 3 implementation, it will be copied to `docs/schemas/use-case-realization-v1.schema.json` alongside existing Jerry schemas (`agent-governance-v1.schema.json`). The production copy is the CI validation target.

### Schema Structure Overview

The schema organizes fields into seven logical blocks, mirroring the YAML frontmatter structure defined in `file-organization.md` lines 59-158:

| Block | Purpose | Primary Consumer | Fields |
|-------|---------|-----------------|--------|
| **Identity** | Who and what this artifact is | All skills, worktracker, AST | `id`, `title`, `work_type`, `version`, `status` |
| **Classification** | How the use case is categorized | /use-case (authoring), /test-spec (scope gating) | `goal_level`, `goal_symbol`, `detail_level`, `scope`, `domain` |
| **Actors** | Who participates | /use-case, /contract-design (role mapping) | `primary_actor`, `supporting_actors`, `stakeholders` |
| **Conditions** | Pre/postconditions and trigger | /test-spec (Given/Then), /contract-design (request/response constraints) | `preconditions`, `postconditions`, `trigger` |
| **Flows** | Main success scenario + alternatives + extensions | /test-spec (primary input for Clark transformation) | `basic_flow`, `alternative_flows`, `extensions` |
| **Interactions** | System boundary crossings (speculative) | /contract-design (primary input for OpenAPI generation) | `interactions` |
| **Slicing** | Implementation-ready subsets | /use-case internal (uc-slicer), /test-spec (slice-scoped generation) | `slices`, `slice_state` |
| **Traceability** | Links to related entities | All skills, worktracker | `parent_id`, `related_use_cases`, `requirements`, `slice_ids` |
| **Metadata** | Audit and priority | All consumers | `priority`, `created_at`, `updated_at`, `created_by`, `last_modified_by`, `realization_level` |

### Schema Field Reference

Complete field-by-field specification. "Req" column indicates whether the field is in the top-level `required` array.

#### Identity Block

| Field | Type | Req | Constraint | Source |
|-------|------|-----|------------|--------|
| `id` | string | Yes | Pattern: `^UC-[A-Z]+-\d{3}$` | file-org line 61 |
| `title` | string | Yes | minLength: 1, maxLength: 200 | Cockburn Ch. 3 |
| `work_type` | string | Yes | Const: `USE_CASE` | file-org line 63 (H-33 AST) |
| `version` | string | Yes | Pattern: `^\d+\.\d+\.\d+$` | file-org line 64 |
| `status` | string | Yes | Enum: DRAFT, REVIEW, APPROVED, DEPRECATED | file-org line 65 |

#### Classification Block

| Field | Type | Req | Constraint | Source |
|-------|------|-----|------------|--------|
| `goal_level` | string | Yes | Enum: SUMMARY, USER_GOAL, SUBFUNCTION | Cockburn Ch. 5, SD-02 |
| `goal_symbol` | string | No | Enum: +, !, - (must match goal_level) | Cockburn Reminders, SD-02 |
| `detail_level` | string | No | Enum: BRIEFLY_DESCRIBED, BULLETED_OUTLINE, ESSENTIAL_OUTLINE, FULLY_DESCRIBED. Default: BULLETED_OUTLINE | S-01, SD-03, DI-01 |
| `scope` | string | Yes | Free text (system boundary name) | Cockburn Ch. 4, file-org line 72 |
| `domain` | string | No | Pattern: `^[A-Z]+$` | file-org line 73 |

#### Actors Block

| Field | Type | Req | Constraint | Source |
|-------|------|-----|------------|--------|
| `primary_actor` | string | Yes | minLength: 1 | Cockburn Ch. 2, file-org line 76 |
| `supporting_actors` | array of objects | No | Each: {name: string, type: enum} | file-org lines 77-80 |
| `supporting_actors[].type` | string | Yes (if present) | Enum: human, system, timer, external | file-org line 79 |
| `stakeholders` | array of objects | No | Each: {name: string, interest: string} | Cockburn Ch. 2 |

#### Conditions Block

| Field | Type | Req | Constraint | Source |
|-------|------|-----|------------|--------|
| `preconditions` | array of strings | No | Items: minLength 1 | Cockburn Ch. 6 |
| `postconditions` | object | No | Properties: success (array), failure (array) | Cockburn Ch. 6 |
| `trigger` | string | No | Free text | Cockburn Ch. 6 |

#### Slice Lifecycle

| Field | Type | Req | Constraint | Source |
|-------|------|-----|------------|--------|
| `slice_state` | string | No | Enum: SCOPED, PREPARED, ANALYZED, IMPLEMENTED, VERIFIED | S-01 pp. 15-16, SD-04 |

#### Flows Block

| Field | Type | Req | Constraint | Source |
|-------|------|-----|------------|--------|
| `basic_flow` | array of flow_step | Yes | minItems: 3, maxItems: 9 | Cockburn Guideline 6, file-org lines 89-98 |
| `alternative_flows` | array of alternative_flow | No | Each has id, name, branches_from_step, condition, steps | file-org lines 100-111 |
| `extensions` | array of extension | No | Each has id, name, anchor_step, condition, steps, outcome | file-org lines 113-124, SD-08 |

**Flow Step Definition (`flow_step`):**

| Field | Type | Req | Constraint | Source |
|-------|------|-----|------------|--------|
| `step` | integer | Yes | minimum: 1 | file-org line 90 |
| `actor` | string | Yes | minLength: 1 | file-org line 91 |
| `action` | string | Yes | minLength: 1 (verb-object form) | file-org line 92 |
| `type` | string | Yes | Enum: actor_action, system_response, validation | SD-07, PAT-008 |

**Alternative Flow Definition (`alternative_flow`):**

| Field | Type | Req | Constraint | Source |
|-------|------|-----|------------|--------|
| `id` | string | Yes | Pattern: `^AF-\d{2}$` | file-org line 101 |
| `name` | string | Yes | minLength: 1 | file-org line 102 |
| `branches_from_step` | integer | Yes | minimum: 1 | file-org line 103 |
| `condition` | string | Yes | minLength: 1 (Cockburn Guideline 11) | file-org line 104 |
| `steps` | array of flow_step | Yes | minItems: 1 | file-org lines 105-109 |
| `rejoins_at_step` | integer or null | No | minimum: 1 or null | file-org line 110 |

**Extension Definition (`extension`):**

| Field | Type | Req | Constraint | Source |
|-------|------|-----|------------|--------|
| `id` | string | Yes | Pattern: `^EXT-\d+[a-z]$` | Cockburn Ch. 8 numbering |
| `name` | string | Yes | minLength: 1 | file-org line 115 |
| `anchor_step` | integer | Yes | minimum: 1 | file-org line 116 |
| `condition` | string | Yes | minLength: 1 | file-org line 117, Cockburn Ch. 8 |
| `steps` | array of flow_step | Yes | minItems: 1 | file-org lines 118-122 |
| `outcome` | string | Yes | Pattern: `^(success\|failure\|rejoin:\d+)$` | SD-08, PAT-008 |

#### Interactions Block (Speculative)

| Field | Type | Req | Constraint | Source |
|-------|------|-----|------------|--------|
| `interactions` | array of interaction | No | Required when realization_level = INTERACTION_DEFINED | file-org lines 126-146 |

**Interaction Definition (`interaction`):**

| Field | Type | Req | Constraint | Source |
|-------|------|-----|------------|--------|
| `id` | string | Yes | Pattern: `^INT-\d{2}$` | file-org line 130 |
| `source_step` | integer | Yes | minimum: 1 | file-org line 131, DI-08 |
| `source_flow` | string | Yes | Pattern: `^(basic_flow\|AF-\d{2}\|EXT-\d+[a-z])$` | file-org line 132 |
| `actor_role` | string | Yes | Enum: consumer, provider | R-06, agent-decomp actor mapping |
| `system_role` | string | Yes | Enum: receiver, provider | file-org line 134 |
| `request_description` | string | Yes | minLength: 1 | file-org line 135 |
| `response_description` | string | Yes | minLength: 1 | file-org line 136 |
| `preconditions` | array of strings | No | Items: minLength 1 | file-org lines 137-138 |
| `postconditions` | array of strings | No | Items: minLength 1 | file-org lines 139-140 |

#### Slicing Block

| Field | Type | Req | Constraint | Source |
|-------|------|-----|------------|--------|
| `slices` | array of slice | No | Required when realization_level in [STORY_DEFINED, INTERACTION_DEFINED] | agent-decomp uc-slicer |

**Slice Definition (`slice`):**

| Field | Type | Req | Constraint | Source |
|-------|------|-----|------------|--------|
| `slice_id` | string | Yes | Pattern: `^UC-[A-Z]+-\d{3}-S\d+$` | file-org line 152 |
| `title` | string | Yes | minLength: 1 | -- |
| `steps_included` | array of objects | Yes | Each: {flow: string, steps: array of integers} | -- |
| `realization_level` | string | No | Enum: OUTLINED, STORY_DEFINED, INTERACTION_DEFINED | -- |
| `test_cases` | array of strings | No | Items: minLength 1 | S-01 Activity 4 |
| `invest_assessment` | object | No | Boolean fields: independent, negotiable, valuable, estimable, small, testable | agent-decomp step 3 |

#### Traceability Block

| Field | Type | Req | Constraint | Source |
|-------|------|-----|------------|--------|
| `parent_id` | string or null | No | Pattern: `^UC-[A-Z]+-\d{3}$` | file-org line 149 |
| `related_use_cases` | array of strings | No | Each: pattern `^UC-[A-Z]+-\d{3}$` | file-org line 150 |
| `requirements` | array of strings | No | Free-form references | file-org line 151 |
| `slice_ids` | array of strings | No | Each: pattern `^UC-[A-Z]+-\d{3}-S\d+$` | file-org line 152 |

#### Metadata Block

| Field | Type | Req | Constraint | Source |
|-------|------|-----|------------|--------|
| `priority` | string | No | Enum: P0, P1, P2, P3 | file-org line 155 |
| `created_at` | string | Yes | ISO-8601 datetime format | file-org line 156 |
| `updated_at` | string | No | ISO-8601 datetime format | file-org line 157 |
| `created_by` | string | Yes | minLength: 1 | file-org line 158 |
| `last_modified_by` | string | No | Free text | -- |
| `realization_level` | string | No | Enum: OUTLINED, STORY_DEFINED, INTERACTION_DEFINED | Convenience summary field |

---

### Required vs. Optional by Realization Level

The schema defines a base set of required fields. As the realization level increases, additional fields become necessary for downstream skills to function. This table documents which fields each realization level needs, beyond the schema-level `required` array.

| Field | OUTLINED | STORY_DEFINED | INTERACTION_DEFINED | Enforcement |
|-------|----------|---------------|---------------------|-------------|
| `id` | Required | Required | Required | Schema `required` |
| `title` | Required | Required | Required | Schema `required` |
| `work_type` | Required | Required | Required | Schema `required` |
| `version` | Required | Required | Required | Schema `required` |
| `status` | Required | Required | Required | Schema `required` |
| `goal_level` | Required | Required | Required | Schema `required` |
| `scope` | Required | Required | Required | Schema `required` |
| `primary_actor` | Required | Required | Required | Schema `required` |
| `basic_flow` | Required | Required | Required | Schema `required` |
| `created_at` | Required | Required | Required | Schema `required` |
| `created_by` | Required | Required | Required | Schema `required` |
| `detail_level` | Expected | Expected | Expected | Agent guardrail |
| `slice_state` | Optional | Expected | Expected | Agent guardrail |
| `extensions` | Optional | Expected | Expected | Agent guardrail (/test-spec rejects without) |
| `slices` | Optional | **Required** | **Required** | Schema `allOf` conditional |
| `interactions` | N/A | Optional | **Required** | Schema `allOf` conditional |
| `postconditions` | Optional | Expected | Expected | Agent guardrail (/test-spec uses for Then clauses) |
| `preconditions` | Optional | Expected | Expected | Agent guardrail (/test-spec uses for Given clauses) |
| `stakeholders` | Optional | Expected | Expected | Cockburn completeness |

**Enforcement distinction:**
- "Schema `required`" = JSON Schema validation fails without this field at any realization level.
- "Schema `allOf` conditional" = JSON Schema validation fails when the realization_level field triggers a conditional requirement.
- "Agent guardrail" = Not enforced by JSON Schema; enforced by individual agent input validation rules (SR-002). The downstream agent rejects with an actionable error message.
- "Expected" = The field should be present at this level for downstream skills to produce good output; not enforced by schema or agent guardrail but documented as a quality expectation.

### Enum Definitions with Sources

#### goal_level (3 values)

| Value | Cockburn Level(s) | Symbol | Description | Source |
|-------|-------------------|--------|-------------|--------|
| `SUMMARY` | Cloud, Kite | `+` | Organizational workflow involving multiple user goals. Too broad for direct implementation. | Cockburn Ch. 5 p. 61 |
| `USER_GOAL` | Sea Level | `!` | A single actor achieves one measurable outcome in one sitting. The standard unit for detailed use case writing. | Cockburn Ch. 5 p. 61 |
| `SUBFUNCTION` | Fish, Clam | `-` | A supporting step within a user goal. Not independently valuable; requires a parent user-goal use case. | Cockburn Ch. 5 p. 61 |

**Design decision SD-02:** Cockburn defines 5 metaphorical levels but only 3 named categories with distinct behavioral characteristics. Collapsing to 3 enums preserves classification power while keeping the schema simple. The `goal_symbol` field preserves the +/!/- compact notation for display purposes.

#### detail_level (4 values)

| Value | UC 2.0 Name | Cockburn Mapping | What Exists at This Level | Source |
|-------|------------|-----------------|--------------------------|--------|
| `BRIEFLY_DESCRIBED` | Narrative Level 1 | Name + goal + brief | Title, goal_level, primary_actor, 1-2 sentence description | S-01, S-02 |
| `BULLETED_OUTLINE` | Narrative Level 2 | Brief + MSS bullets | + basic_flow with 3-9 steps (default level) | S-01, S-02 |
| `ESSENTIAL_OUTLINE` | Narrative Level 3 | + Extensions | + alternative_flows, extensions. Minimum for /test-spec and /contract-design. | S-01, S-02 |
| `FULLY_DESCRIBED` | Narrative Level 4 | + Handling + Sub-UCs | + Complete extension handling, sub-use-case extraction, stakeholders populated | S-01, S-02 |

**Design decision SD-03:** Maps 1:1 to Jacobson UC 2.0 narrative levels. The 4 levels enable `/test-spec` to reject use cases that are too sparse (BRIEFLY_DESCRIBED and BULLETED_OUTLINE lack extension conditions required for Clark transformation).

#### status (4 values)

| Value | Meaning | Transition | Source |
|-------|---------|------------|--------|
| `DRAFT` | Initial creation, being authored | -> REVIEW (when author considers it complete) | file-org line 65 |
| `REVIEW` | Submitted for stakeholder review | -> APPROVED or -> DRAFT (if revisions needed) | file-org line 65 |
| `APPROVED` | Accepted for implementation | -> DEPRECATED (if superseded) | file-org line 65 |
| `DEPRECATED` | No longer active, superseded or abandoned | Terminal state | file-org line 65 |

#### slice_state (5 values)

| Value | UC 2.0 State | Worktracker Status | Entry Criteria | Exit Criteria | Source |
|-------|-------------|-------------------|----------------|---------------|--------|
| `SCOPED` | Scoped | `draft` | Slice identified from use case flows | INVEST criteria verified | S-01, SD-04 |
| `PREPARED` | Prepared | `ready` | Test cases defined; narrative enhanced | Stakeholder approval for implementation | S-01, SD-04 |
| `ANALYZED` | Analyzed | `in-progress` | System elements identified (Activity 5, realization) | Realization artifact produced (interactions block) | S-01, SD-04 |
| `IMPLEMENTED` | Implemented | `review` | Software built and unit tested | Integration test passed | S-01, SD-04 |
| `VERIFIED` | Verified | `done` | Acceptance tests passed | Regression tests passed | S-01, SD-04 |

**Design decision SD-04:** Uses UC 2.0 five states (not UC 3.0 six states). UC 3.0 adds a sixth state ("Identified" before "Defined"); this can be added via minor version bump (1.1.0) without breaking existing consumers.

#### flow_step.type (3 values)

| Value | Clark Mapping | Gherkin Element | Description | Source |
|-------|--------------|-----------------|-------------|--------|
| `actor_action` | When clause | `When {actor} {action}` | A human or external actor performs an action | SD-07, PAT-008 |
| `system_response` | Then clause | `Then {system} {response}` | The system processes and responds | SD-07, PAT-008 |
| `validation` | Then assertion | `Then {system} validates {assertion}` | The system validates input or state | SD-07, PAT-008 |

**Design decision SD-07:** Step types enable Clark's mechanical transformation without NLP interpretation. The `tspec-generator` agent maps step types directly to Gherkin clause types.

#### extension.outcome (3 patterns)

| Pattern | Clark Mapping | Gherkin Scenario Type | Source |
|---------|--------------|----------------------|--------|
| `success` | Additional positive scenario | `Scenario: {ext_name} - alternate success` | SD-08 |
| `failure` | Negative/error scenario | `Scenario: {ext_name} - error case` | SD-08, PAT-008 |
| `rejoin:{step}` | Additional scenario rejoining MSS | `Scenario: {ext_name} - returns to step {N}` | SD-08, PAT-008 |

**Design decision SD-08:** The outcome field enables mechanical mapping to Gherkin scenario types. Extensions with `outcome=failure` produce negative test scenarios. Extensions with `outcome=rejoin` produce additional scenarios that eventually merge back to the happy path.

#### actor_role and system_role (interactions block)

| Field | Values | Contract Mapping | Source |
|-------|--------|-----------------|--------|
| `actor_role` | consumer, provider | consumer -> API caller; provider -> API server | R-06, agent-decomp actor mapping |
| `system_role` | receiver, provider | receiver -> processes requests; provider -> returns data | file-org line 134 |

**Actor-to-contract-role mapping (from agent-decomposition-draft.md):**

| Use Case Element | actor_role | system_role | OpenAPI Contract Role | Source |
|------------------|-----------|-------------|----------------------|--------|
| Primary actor initiates | consumer | receiver | API consumer (the caller) | R-06 |
| System responds | provider | provider | API provider (the server) | R-06 |
| Supporting actor (external) | provider | N/A | External dependency (documented in components/schemas) | R-06 |

---

### Cross-Field Constraints

The schema encodes five conditional validation rules using the JSON Schema `allOf` + `if/then` pattern:

| # | Constraint | When | Then | Rationale |
|---|-----------|------|------|-----------|
| 1 | Interactions required at INTERACTION_DEFINED | `realization_level == "INTERACTION_DEFINED"` | `interactions` required with minItems: 1 | cd-generator cannot produce OpenAPI without interaction data |
| 2 | Slices required at STORY_DEFINED+ | `realization_level in ["STORY_DEFINED", "INTERACTION_DEFINED"]` | `slices` required with minItems: 1 | Slices are the decomposition that defines stories and interactions |
| 3 | Goal symbol matches SUMMARY | `goal_level == "SUMMARY"` and `goal_symbol` present | `goal_symbol == "+"` | Cockburn symbol consistency |
| 4 | Goal symbol matches USER_GOAL | `goal_level == "USER_GOAL"` and `goal_symbol` present | `goal_symbol == "!"` | Cockburn symbol consistency |
| 5 | Goal symbol matches SUBFUNCTION | `goal_level == "SUBFUNCTION"` and `goal_symbol` present | `goal_symbol == "-"` | Cockburn symbol consistency |

**Constraint activation note:** Constraints 1 and 2 only activate when the `realization_level` field is present. If `realization_level` is omitted (it is optional), these constraints do not fire. This is intentional: the `realization_level` field is a convenience summary, and agents may choose to determine completeness by inspecting the actual blocks rather than relying on this field. When agents do set `realization_level`, the schema enforces consistency between the declared level and the block presence.

**Constraints not encoded in schema (enforced by agent guardrails instead):**

| Constraint | Why Not in Schema | Enforced By |
|-----------|-------------------|-------------|
| `detail_level >= ESSENTIAL_OUTLINE` for /test-spec input | Schema validates structure, not agent-specific preconditions | tspec-generator input validation (SR-002) |
| `detail_level >= ESSENTIAL_OUTLINE` for /contract-design input | Same rationale | cd-generator input validation (SR-002) |
| `extensions` non-empty for /test-spec input | Having 0 extensions is structurally valid; the agent decides completeness | tspec-generator guardrail |
| `source_step` references a step that exists in `source_flow` | Cross-array referential integrity beyond JSON Schema's capability | cd-generator input validation |
| `actor` in flow_step matches primary_actor or supporting_actors[].name | Cross-field reference validation beyond JSON Schema's practical capability | uc-author output validation |

---

### Downstream Minimum Requirements

Each downstream skill has minimum field requirements that must be met before transformation can succeed. These requirements are documented in `file-organization.md` lines 209-216 and `agent-decomposition-draft.md` integration points.

#### /test-spec (tspec-generator) Minimum Input

| Requirement | Schema Field | Minimum Value | Enforcement | Source |
|-------------|-------------|---------------|-------------|--------|
| Detail level | `detail_level` | `>= ESSENTIAL_OUTLINE` | Agent guardrail (reject with message) | file-org line 209 |
| Slice state | `slice_state` | `>= ANALYZED` | Agent guardrail | file-org line 209 |
| Basic flow | `basic_flow` | 3-9 steps present (schema enforced) | Schema `minItems: 3, maxItems: 9` | Cockburn Guideline 6 |
| Step types | `basic_flow[].type` | All steps have type field (schema enforced) | Schema `required` in flow_step | SD-07, PAT-008 |
| Extensions | `extensions` | At least 1 extension present | Agent guardrail (rejects without) | PAT-002 |
| Preconditions | `preconditions` | Present (for Given clauses) | Agent guardrail (quality warning) | Clark mapping |
| Postconditions | `postconditions.success` | Present (for Then clauses) | Agent guardrail (quality warning) | Clark mapping |

#### /contract-design (cd-generator) Minimum Input

| Requirement | Schema Field | Minimum Value | Enforcement | Source |
|-------------|-------------|---------------|-------------|--------|
| Detail level | `detail_level` | `>= ESSENTIAL_OUTLINE` | Agent guardrail | file-org line 213 |
| Interactions | `interactions` | Non-empty array with all required fields | Schema conditional (when realization_level set) + agent guardrail | file-org line 213 |
| Source step validity | `interactions[].source_step` | References existing step in source_flow | Agent guardrail (cross-reference check) | agent-decomp lines 520-527 |
| Actor role | `interactions[].actor_role` | Present on every interaction | Schema `required` in interaction def | R-06 |
| System role | `interactions[].system_role` | Present on every interaction | Schema `required` in interaction def | R-06 |
| Request/response descriptions | `interactions[].request_description`, `interactions[].response_description` | Non-empty strings on every interaction | Schema `required` + `minLength: 1` | agent-decomp step 5-6 |
| Supporting actors | `supporting_actors` | Present (for external dependency mapping) | Agent guardrail (reads both interactions + actors per IC-05) | IC-05 |

---

## L2: Architectural Rationale

### Traceability to R-01

**R-01** (from `phase-1-synthesis.md` Phase 2 Recommendations, P0 priority): "Design the shared artifact format (use-case realization document) before designing any individual skill agents. Define JSON Schema for machine-readable fields (goal level, detail level, slice state, actor list, interaction steps). Design human-readable Markdown body structure."

This schema fulfills R-01. The traceability from R-01 to schema fields:

| R-01 Requirement | Schema Realization | Fields |
|------------------|-------------------|--------|
| "JSON Schema for machine-readable fields" | `shared-schema.json`, JSON Schema Draft 2020-12 | All fields |
| "goal level" | `goal_level` enum with 3 values from Cockburn | `goal_level`, `goal_symbol` |
| "detail level" | `detail_level` enum with 4 values from Jacobson UC 2.0 | `detail_level` |
| "slice state" | `slice_state` enum with 5 values from UC 2.0 lifecycle | `slice_state` |
| "actor list" | `primary_actor` string + `supporting_actors` array of typed objects | `primary_actor`, `supporting_actors` |
| "interaction steps" | `interactions` array with typed interaction objects | `interactions` array, `interaction` $def |

### Traceability to file-organization.md

Every field in the schema traces to a specific line or design decision in `file-organization.md` (v2.1.0, PASSED 0.951). The mapping:

| file-org Section | Schema Fields | Design Decisions Encoded |
|------------------|--------------|-------------------------|
| Shared Artifact Format (lines 59-158) | All property definitions | SD-01 through SD-08 |
| Schema Design Decisions (lines 161-172) | Enum definitions, type constraints | SD-01 (YAML), SD-02 (goal_level), SD-03 (detail_level), SD-04 (slice_state), SD-05 (flows/interactions separation), SD-06 (interactions derived from flows), SD-07 (step types), SD-08 (extension outcome) |
| Schema Validation (lines 174-179) | Schema $id, $schema, title | R-03 location and format |
| Schema Version Rationale (lines 181-189) | Version in $id: v1.0.0 | Justification for 1.0.0 not 0.x.0 |
| Interactions Block Validation Gate (lines 191-207) | Interactions block `description` field with speculative warning | Phase 3 validation criterion |
| Minimum Detail Level (lines 209-216) | Not in schema directly; documented in this design doc | Agent guardrail enforcement rationale |

### Traceability to agent-decomposition-draft.md

The agent decomposition document (v1.2.0, PASSED 0.957) defines how agents produce and consume schema fields:

| Agent | Produces | Consumes | Schema Fields |
|-------|----------|----------|---------------|
| `uc-author` | Identity, Classification, Actors, Conditions, Flows, Metadata | User input, project context | All fields except `interactions`, `slices`, `slice_state` |
| `uc-slicer` | Slicing, Interactions, slice_state updates | Flows (basic_flow, alternative_flows, extensions), Actors | `slices`, `interactions`, `slice_state`, `slice_ids` |
| `tspec-generator` | (external: .feature.md files) | Flows, Conditions, Classification | `basic_flow`, `alternative_flows`, `extensions`, `preconditions`, `postconditions`, `detail_level`, `goal_level` |
| `cd-generator` | (external: .openapi.yaml files) | Interactions, Actors, Classification | `interactions`, `primary_actor`, `supporting_actors`, `detail_level` |

**Activity 5 traceability chain:** `uc-slicer` (methodology step 7) produces the `interactions` block when transitioning a slice from Prepared to Analyzed state. Each `interaction` object in the array represents a system boundary crossing identified from the flows. The `source_step` and `source_flow` fields maintain traceability from the interaction back to the flow step that generated it. `cd-generator` reads this block and the `supporting_actors` array (IC-05 resolution) to map use case interaction semantics to OpenAPI operations.

**IC-05 resolution encoded in schema:** The `interaction` definition does NOT include a `supporting_actor` field. This is intentional per the IC-05 resolution documented in `file-organization.md` lines 142-146: `cd-generator` resolves supporting actor roles by cross-referencing `interaction.actor_role` with the top-level `supporting_actors` array. This avoids field duplication while maintaining traceability. The schema's `description` field on `supporting_actors` documents this cross-referencing behavior.

### Schema Version Rationale

The schema version is **v1.0.0**. This decision is grounded in `file-organization.md` Schema Version Rationale section (lines 181-189):

1. **Stable core blocks.** The Identity, Classification, Actors, Conditions, and Flows blocks are grounded in Cockburn (2001, 20+ years) and Jacobson (2011, 15+ years). The field names, enums, and structure map directly to published methodology concepts with well-defined semantics. These blocks are not speculative.

2. **Jerry convention.** All existing Jerry schemas start at v1: `agent-governance-v1.schema.json`, `handoff-v2.schema.json` (was v1, bumped to v2). Starting at 0.x.0 would be inconsistent with the framework's versioning convention and would incorrectly signal "not ready for use."

3. **Interactions block exception acknowledged.** The `interactions` block is architecturally speculative (G-01, no prior art for UC-to-contract transformation). The schema version covers the schema as a whole; the interactions block's stability is tracked separately via the validation gate. Schema version evolution path:
   - 1.0.0: Current design
   - 1.1.0: Minor backward-compatible additions (e.g., UC 3.0 sixth slice state, optional async_interactions block per G-02)
   - 2.0.0: Breaking changes to interactions block if Phase 3 validation gate triggers MAJOR REVISION outcome

### Interactions Block Validation Gate

Cross-reference to `file-organization.md` Interactions Block Validation Gate section (lines 191-207).

**Validation criterion:** 3 representative use cases (spanning 2+ domains, including 1+ with supporting actors) must produce valid OpenAPI from the `interactions` block alone, without `cd-generator` inferring unstated structure from the flows block or external context.

**Gate outcomes:**

| Outcome | Condition | Schema Action |
|---------|-----------|---------------|
| VALIDATED | All 3 UCs -> valid OpenAPI from interactions alone | Schema remains at v1.0.0 |
| MINOR REVISION | 2/3 succeed; 1 requires missing optional field | Add field; bump to v1.1.0 (backward compatible) |
| MAJOR REVISION | 1 or fewer succeed; structural model inadequate | Redesign interactions block; bump to v2.0.0 (requires user approval per P-020) |

**Timing:** Phase 3 prototyping, before `/test-spec` or `/contract-design` are built against the interactions block.

### Bootstrap Dependency

The validation gate requires a minimum viable `cd-generator` implementation to test the interactions-to-OpenAPI transformation. This is a bootstrap dependency documented in `file-organization.md` lines 206-207:

- The minimum viable implementation need only read the `interactions` block and attempt OpenAPI output.
- Full agent hardening (complete methodology, guardrails, quality scoring) occurs after the gate validates the schema design.
- This is distinct from the full `cd-generator` agent implementation defined in `agent-decomposition-draft.md`.

Phase 3 sequencing must account for this dependency: build minimum viable `cd-generator`, run validation gate, then complete the full agent.

---

## Options Evaluated

### Option A: Flat Field Structure (No Nested $defs)

| Dimension | Assessment |
|-----------|-----------|
| **Pros** | Simpler schema file. All fields at top level. No $ref indirection. Easier for humans to read the raw schema. |
| **Cons** | Flow steps, alternative flows, extensions, interactions, and slices all have internal structure that repeats. Without $defs, the flow_step schema would be duplicated 3 times (basic_flow, alternative_flow.steps, extension.steps). Schema becomes ~2x larger. Maintenance requires updating identical structures in multiple places. |
| **Score** | 4/10 -- DRY violation, maintenance burden |

### Option B: Separate Schema Files Per Block (6 schema files)

| Dimension | Assessment |
|-----------|-----------|
| **Pros** | Maximum modularity. Each block evolves independently. Smaller individual files. |
| **Cons** | JSON Schema $ref across files requires URL resolution or bundling. CI validation becomes complex (resolve 6 files to validate 1 artifact). Agent input validation must load multiple schemas. Overengineered for 1 consuming artifact type. No existing Jerry schema uses multi-file composition. |
| **Score** | 3/10 -- complexity without proportional benefit |

### Option C: Single Schema with $defs (Selected)

| Dimension | Assessment |
|-----------|-----------|
| **Pros** | DRY: shared definitions (flow_step) referenced via $ref. Single file for CI validation. Consistent with Jerry convention (agent-governance-v1.schema.json is a single file). All cross-field constraints in one allOf block. $defs section provides a clear vocabulary for the shared types. |
| **Cons** | $ref indirection requires understanding JSON Schema referencing. Schema file is larger (~400 lines). Future block additions must be integrated into the same file. |
| **Score** | 8/10 -- balanced DRY, consistency with Jerry conventions, single-file simplicity |

### Option D: Schema with External $vocabulary for Methodology-Specific Keywords

| Dimension | Assessment |
|-----------|-----------|
| **Pros** | JSON Schema 2020-12 supports custom vocabularies. Could define a "cockburn" vocabulary and a "jacobson" vocabulary with semantic validation rules beyond structural constraints. |
| **Cons** | Custom vocabularies require validator tooling that does not exist in the Jerry ecosystem. No existing JSON Schema validator supports custom $vocabulary out of the box. The benefit (semantic validation) is better handled by agent guardrails which already have methodology knowledge. Overengineered for the current scale. |
| **Score** | 2/10 -- technically interesting but impractical |

**Selected: Option C.** Single schema file with $defs for shared type definitions. Consistent with Jerry conventions, DRY, and single-file CI validation.

---

## Self-Review Checklist (H-15, S-010)

- [x] **P-001 (Truth/Accuracy):** Every field in the JSON Schema traces to a specific line in file-organization.md or a methodology source (Cockburn, Jacobson, Clark). Enum values cite primary sources.
- [x] **P-002 (File Persistence):** Both deliverables persisted: `frontmatter-schema.md` (this file) and `shared-schema.json` (JSON Schema file).
- [x] **P-004 (Provenance):** Source documents cited throughout. Traceability tables link schema fields to R-01, file-organization.md, and agent-decomposition-draft.md.
- [x] **P-011 (Evidence-Based):** 4 alternatives evaluated (Options A-D) with scored trade-off analysis per P-011.
- [x] **P-020 (User Authority):** Status is PROPOSED, not ACCEPTED.
- [x] **P-022 (No Deception):** Interactions block clearly marked as architecturally speculative in both schema descriptions and this document. Validation gate cross-referenced. Bootstrap dependency acknowledged. Constraints not enforceable by JSON Schema (agent-level) explicitly documented.
- [x] **H-23 (Navigation):** Navigation table present with anchor links.
- [x] **L0/L1/L2:** All three output levels present with appropriate audience depth.
- [x] **JSON Schema validity:** Schema file parses as valid JSON. All 7 $ref references resolve to $defs entries. 5 allOf conditional constraints encoded.
- [x] **JSON Schema Draft 2020-12:** $schema header present. Patterns use valid regex. Enum values are arrays of strings.
- [x] **Jerry schema conventions:** $schema, $id, title, description present (matching agent-governance-v1.schema.json style). additionalProperties: true at top level for forward compatibility.
- [x] **R-01 traceability:** Complete mapping from R-01 requirements to schema fields documented.
- [x] **file-organization.md traceability:** Field-level mapping to lines 59-158 documented.
- [x] **agent-decomposition-draft.md traceability:** Activity 5 -> interactions block -> cd-generator input chain complete. IC-05 supporting_actor resolution documented.
- [x] **Schema version rationale:** v1.0.0 justified with 3 reasons citing file-organization.md lines 181-189.
- [x] **Validation gate cross-reference:** Phase 3 criterion, gate outcomes, and bootstrap dependency documented.
- [x] **SD-01 through SD-08:** All 8 schema design decisions from file-organization.md traced and encoded.
- [x] **S-003 (Steelman):** Applied to rejected alternatives before dismissal (Options A, B, D each steelmanned in Options Evaluated section).
- [x] **basic_flow min/max:** Cockburn Guideline 6 (3-9 steps) encoded as minItems: 3, maxItems: 9 on basic_flow array.
- [x] **No fields without grounding:** Every field traces to input documents. No invented fields.

### Adversarial Self-Check (S-002: Devil's Advocate)

**Challenge 1: "Is the interactions block schema premature given that it is architecturally speculative?"**
The block is defined because `cd-generator` needs a concrete input contract to be implemented. Not defining it would mean `/contract-design` has no schema to validate against, which is worse than defining a speculative schema with a documented validation gate. The schema descriptions explicitly warn about the speculative status. The allOf conditional only enforces the block when `realization_level` is explicitly set to `INTERACTION_DEFINED`, so documents at lower realization levels are unaffected.

**Challenge 2: "Should additionalProperties be false at the top level to prevent schema drift?"**
Setting `additionalProperties: false` at the top level would reject any YAML field not in the schema. This would break forward compatibility -- if a future schema version adds a field, existing validators would reject documents from the new version. Jerry's existing `agent-governance-v1.schema.json` uses `additionalProperties: true` for the same reason. Sub-objects (flow_step, alternative_flow, extension, interaction, slice) use `additionalProperties: false` because they are tightly defined structures where unexpected fields indicate errors.

**Challenge 3: "The $comment fields pollute the properties namespace."**
The `$comment_*` properties are documentation aids that carry a `const` value (making them trivially validatable). They are not required fields and do not affect validation. They provide block boundary markers when reading the raw schema. However, if a CI validation policy later enforces strict property naming, these should be converted to `$comment` annotations (which JSON Schema 2020-12 supports but which appear outside `properties`). Current Jerry schemas do not use this pattern, so the `$comment_*` properties follow the pragmatic convention of inline documentation.

### Pre-Mortem (S-004): "It's 6 months later and this schema failed -- why?"

**Failure Mode 1: The interactions block required a complete redesign.**
Signal: Phase 3 validation gate triggers MAJOR REVISION. The `cd-generator` cannot produce valid OpenAPI from the interactions block for 2+ of the 3 representative use cases.
Mitigation: The validation gate is designed for exactly this scenario. Schema bumps to v2.0.0 with redesigned interactions block. The flows block (consumed by `/test-spec`) is unaffected per SD-05 (separate blocks). The cost is a schema major version bump and updates to `cd-generator` and `uc-slicer`.

**Failure Mode 2: The 3-9 step constraint on basic_flow is too rigid.**
Signal: Users consistently write use cases with 10-12 steps in the basic flow, and the schema validation rejects them.
Mitigation: Cockburn's Guideline 6 is a heuristic, not a hard rule. If real usage data shows that 10-12 step basic flows are common and well-formed, the maxItems constraint can be relaxed to 12 or removed entirely in a minor schema version bump (1.1.0). The agent guardrail in `uc-author` would still recommend 3-9 steps as a quality signal.

**Failure Mode 3: Downstream skills need fields not in the schema.**
Signal: During Phase 3 implementation, `tspec-generator` or `cd-generator` needs a field that does not exist in the schema (e.g., non-functional requirements, performance constraints, security classification).
Mitigation: `additionalProperties: true` at the top level means any extra fields are accepted without schema validation failure. The new field is added formally in a minor schema version bump (1.1.0). This is the designed evolution path per file-organization.md long-term evolution table.

---

*Schema Design Version: 1.0.0*
*JSON Schema Version: Draft 2020-12*
*Constitutional Compliance: P-001 (truth), P-002 (file persistence), P-003 (no recursive subagents), P-004 (provenance), P-011 (evidence-based alternatives), P-020 (user authority -- PROPOSED status), P-022 (no deception -- speculative block warnings, constraints limitations disclosed)*
*Adversary Review Required: YES -- C4 all-10-strategy review at >= 0.95 threshold*
*Next Agent: adv-scorer (initial scoring)*
*Workflow ID: use-case-skills-20260308-001*
