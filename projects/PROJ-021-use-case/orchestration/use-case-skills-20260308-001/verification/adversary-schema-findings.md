# Strategy Execution Report: JSON Schema Adversarial Review

## Execution Context

- **Strategy Set:** S-010 (Self-Refine), S-003 (Steelman), S-002 (Devil's Advocate), S-011 (Chain-of-Verification), S-013 (Inversion)
- **Templates:** `.context/templates/adversarial/s-010-self-refine.md`, `s-003-steelman.md`, `s-002-devils-advocate.md`, `s-011-cove.md`, `s-013-inversion.md`
- **Primary Deliverables:**
  - `docs/schemas/use-case-realization-v1.schema.json`
  - `docs/schemas/test-specification-v1.schema.json`
- **Cross-reference Artifacts:**
  - `skills/use-case/samples/sample-use-case.md`
  - `skills/test-spec/samples/sample-test-specification.md`
- **Criticality:** C3 (Significant)
- **Executed:** 2026-03-11T00:00:00Z
- **H-16 Compliance:** S-003 (Steelman, position 2) executed before S-002 (Devil's Advocate, position 3) — COMPLIANT

---

## Findings Summary

| ID | Severity | Strategy | Finding | Schema |
|----|----------|----------|---------|--------|
| SR-001 | Critical | S-010 | `additionalProperties: true` on root object allows arbitrary frontmatter keys to silently pass validation | use-case-realization |
| SR-002 | Major | S-010 | `parent_id` type union `["string", "null"]` with a `pattern` is Draft 2020-12 incompatible: pattern does not apply to null type, creating silent validation gap | use-case-realization |
| SR-003 | Major | S-010 | `goal_level`/`goal_symbol` cross-constraint enforced via `allOf` if/then but `goal_symbol` is not `required` — mismatch is undetectable when `goal_symbol` is absent | use-case-realization |
| SR-004 | Minor | S-010 | `test-specification` schema has no `work_type` discriminator field; schema is unidentifiable without filename context | test-specification |
| SR-005 | Minor | S-010 | `slice.invest_assessment` properties have no `required` list; an empty object `{}` passes validation | use-case-realization |
| SM-001 | Major | S-003 | Steelman finding: the `allOf` goal-symbol cross-constraint is a genuine strength that warrants explicit documentation in the description | use-case-realization |
| DA-001 | Critical | S-002 | `extensions` field is not `required` at `ESSENTIAL_OUTLINE` or above despite clark-transformation-rules.md RULE-IV-02 mandating it for BDD generation | use-case-realization |
| DA-002 | Major | S-002 | `source_detail_level` enum in test-specification schema includes `ESSENTIAL_OUTLINE` and `FULLY_DESCRIBED` only — but `clark-transformation-rules.md` RULE-IV-01 rejects BRIEFLY_DESCRIBED and BULLETED_OUTLINE at runtime, not at schema time; a test spec with wrong `source_detail_level` would validate | test-specification |
| DA-003 | Major | S-002 | `realization_level` conditional (`allOf`: if INTERACTION_DEFINED then interactions required) does not enforce that `slices` is populated when `realization_level = STORY_DEFINED` | use-case-realization |
| DA-004 | Major | S-002 | `scenario_count` described as "Must equal coverage.mapped_flows" but no schema constraint enforces this equality; validator will pass mismatched values | test-specification |
| DA-005 | Minor | S-002 | `supporting_actors[].type` enum is `["human", "system", "timer"]` but `use-case-writing-rules.md` Rule 3.2 documents `"external"` as a valid type; schema is narrower than the rules | use-case-realization |
| CV-001 | Critical | S-011 | `source_detail_level` in test-specification schema description claims "BRIEFLY_DESCRIBED and BULLETED_OUTLINE are rejected" — but this contradicts the schema itself: the `enum` only lists the two valid values; the description incorrectly implies the schema enforces the rejection (it does not; only the rule file does) | test-specification |
| CV-002 | Major | S-011 | `detail_level` description in use-case-realization schema states "BRIEFLY_DESCRIBED -> BULLETED_OUTLINE -> ESSENTIAL_OUTLINE -> FULLY_DESCRIBED" as progressive elaboration — sample artifact `sample-use-case.md` uses `detail_level: BRIEFLY_DESCRIBED` with `status: APPROVED`; no schema constraint prevents APPROVED status at BRIEFLY_DESCRIBED, contradicting expected workflow | use-case-realization |
| CV-003 | Major | S-011 | `interaction.id` pattern is `^INT-\\d{2,3}$` (2-3 digits) but the description says "Format: INT-{NN}" (2 digits only); mismatch between pattern and description | use-case-realization |
| CV-004 | Minor | S-011 | `coverage.coverage_percentage` described as "Optional; computable from mapped_flows and total_flows" but the computation formula is not captured in the schema and the `quality.coverage_target_met` flag cannot be derived without knowing which goal_level applies | test-specification |
| IN-001 | Critical | S-013 | Goal: schemas must reject invalid use case artifacts. Anti-goal inversion: an artifact with `detail_level: BRIEFLY_DESCRIBED` and `realization_level: INTERACTION_DEFINED` with populated `interactions[]` would PASS validation even though this combination is logically invalid per the rules (INTERACTION_DEFINED requires FULLY_DESCRIBED level) | use-case-realization |
| IN-002 | Major | S-013 | Goal: test-specification schema must identify orphan test specs. Anti-goal: a test spec with `source_use_case: UC-LIB-001` and `slice_id: null` with `mapped_flows: 5` and `total_flows: 4` (mapped > total) would pass validation; schema allows contradictory coverage counts | test-specification |
| IN-003 | Major | S-013 | Assumption: `flow_step.actor` values will be validated against `primary_actor` / `supporting_actors[].name` / "System". This assumption is NOT enforced by the schema — any string passes; the rules file (Rule 3.3) enforces this but the schema does not | use-case-realization |
| IN-004 | Minor | S-013 | Assumption: `basic_flow` step numbers are sequential starting at 1. Schema enforces `minimum: 1` but not sequential ordering; steps `[1, 3, 5]` would pass validation, breaking Clark transformation which assumes sequential steps | use-case-realization |

---

## Detailed Findings

---

### SR-001: `additionalProperties: true` Allows Silent Frontmatter Pollution [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Schema** | `use-case-realization-v1.schema.json` (root object, line 253) |
| **Strategy Step** | S-010 Step 2 — Completeness check |

**Evidence:**
```json
"additionalProperties": true
```
Line 253 of `use-case-realization-v1.schema.json`. The root-level `additionalProperties` is set to `true`, meaning any property not declared in `properties` silently passes validation.

**Analysis:**
The schema's stated purpose is to "validate use case artifact YAML frontmatter." With `additionalProperties: true`, a document could include misspelled fields (e.g., `staus: APPROVED` instead of `status: APPROVED`), deprecated fields, or agent-generated noise without any validation failure. This is particularly dangerous in frontmatter validation contexts because YAML parsers are permissive; schema validation is the only gate. By contrast, the nested `$defs` objects (`flow_step`, `extension`, `alternative_flow`, `interaction`, and `postconditions`) all correctly use `additionalProperties: false`. The root-level leniency is inconsistent and defeats the schema's core validation purpose.

**Recommendation:**
Change `"additionalProperties": true` to `"additionalProperties": false` at the root object level. If there are known extension scenarios (e.g., future tooling adding fields), use `unevaluatedProperties: false` (Draft 2020-12 native) or document a specific allowlist of additional properties.

---

### SR-002: `parent_id` Pattern Inapplicable to Null Type [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Schema** | `use-case-realization-v1.schema.json` (line 228-231) |
| **Strategy Step** | S-010 Step 2 — Internal Consistency / Methodological Rigor |

**Evidence:**
```json
"parent_id": {
  "type": ["string", "null"],
  "pattern": "^UC-[A-Z]+-\\d{3}$",
  "description": "Parent use case ID for sub-use-cases. Null for top-level use cases."
}
```

**Analysis:**
In JSON Schema Draft 2020-12, the `pattern` keyword applies only when the value is a string. When `parent_id` is `null`, the pattern is not evaluated — this is correct behavior. However, the schema does not explicitly document this, and more critically, a validator receiving `null` will not check the pattern. The real issue is semantic: if `parent_id` is declared as `null` for top-level use cases, then the type union is correct, but the description "Null for top-level use cases" creates an expectation that should ideally be expressed as a constraint, not just prose. A bigger problem is that `parent_id` is not `required` — so it can be *absent* (undefined) for top-level use cases rather than explicitly `null`, which means tooling cannot distinguish "not a sub-use-case" from "forgot to set parent_id."

**Recommendation:**
Either (1) remove `null` from the type union and make `parent_id` truly optional (absent = top-level), providing cleaner semantics, or (2) keep the type union but add a description clarifying that `null` is the explicit signal and absence is also acceptable. If the intent is to require `parent_id` for SUBFUNCTION goal-level use cases, add an `allOf` conditional enforcing that.

---

### SR-003: `goal_symbol` Not `required` — Cross-Constraint Unenforceable [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Schema** | `use-case-realization-v1.schema.json` (required array vs. allOf constraints, lines 7-23 vs. 448-503) |
| **Strategy Step** | S-010 Step 2 — Internal Consistency |

**Evidence:**
The `required` array (lines 7-23) includes `goal_level` but does NOT include `goal_symbol`. The `allOf` constraints (lines 448-503) enforce that when `goal_level = SUMMARY`, `goal_symbol` must be `+`, etc. However, if `goal_symbol` is absent entirely, the `then` clause's property constraint is vacuously satisfied (the property doesn't exist, so no constraint is violated in standard JSON Schema semantics).

**Analysis:**
The `allOf` if/then cross-constraint correctly prevents `goal_level: USER_GOAL` with `goal_symbol: "+"`. However, it does NOT prevent `goal_level: USER_GOAL` with no `goal_symbol` field at all, because JSON Schema `properties` constraints only apply to properties that are present. The description explicitly states: "Must be consistent with goal_level: SUMMARY=+, USER_GOAL=!, SUBFUNCTION=-. Enforced by allOf constraints." This description is incorrect — the constraint is only partially enforced.

**Recommendation:**
Add `"goal_symbol"` to the `required` array (alongside `goal_level`). The field is conceptually always required when `goal_level` is present (which is required), and their values are codetermined. This closes the gap where `goal_symbol` could be omitted without validation failure.

---

### SR-004: Test-Specification Schema Lacks `work_type` Discriminator [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Schema** | `test-specification-v1.schema.json` (missing discriminator) |
| **Strategy Step** | S-010 Step 2 — Completeness |

**Evidence:**
`use-case-realization-v1.schema.json` has `"work_type": { "const": "USE_CASE" }` as a discriminator field. `test-specification-v1.schema.json` has no equivalent discriminator field.

**Analysis:**
Without a `work_type` or equivalent discriminator, a test-specification artifact cannot be schema-identified without relying on filename or external context. If the `/ast` skill or other tooling validates frontmatter by trying multiple schemas, the lack of a discriminator means both schemas might partially match the same document. The `generated_by: tspec-generator` field acts as a soft discriminator but is a `const` on the agent name, not a structural type indicator.

**Recommendation:**
Add `"work_type": { "const": "TEST_SPECIFICATION" }` to the test-specification schema's properties and `required` array, consistent with the pattern established in the use-case-realization schema.

---

### SR-005: `slice.invest_assessment` Empty Object Passes Validation [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Schema** | `use-case-realization-v1.schema.json` `$defs.slice.invest_assessment` |
| **Strategy Step** | S-010 Step 2 — Completeness |

**Evidence:**
```json
"invest_assessment": {
  "type": "object",
  "properties": {
    "independent": { "type": "boolean" },
    "negotiable": { "type": "boolean" },
    ...
  },
  "description": "INVEST criteria assessment for slice sizing."
}
```
No `required` array and no `minProperties` constraint.

**Analysis:**
An empty `invest_assessment: {}` passes schema validation. Since INVEST is an acronym where each letter represents a criterion, a partial assessment (e.g., only `independent: true` with all others absent) provides misleading quality signal. At minimum, when `invest_assessment` is present, all 6 boolean fields should be required.

**Recommendation:**
Add `"required": ["independent", "negotiable", "valuable", "estimable", "small", "testable"]` to the `invest_assessment` object definition, or add `"minProperties": 6`. If partial assessment is intentional, update the description to clarify.

---

### DA-001: `extensions` Not Conditionally Required at ESSENTIAL_OUTLINE+ [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Schema** | `use-case-realization-v1.schema.json` (missing conditional constraint) |
| **Strategy Step** | S-002 Step 3 — Construct Counter-Arguments |

**Evidence:**
`extensions` is declared as an optional property in the schema (not in `required` array). The property description states: "Required for /test-spec generation at ESSENTIAL_OUTLINE or above." However, no `allOf` if/then constraint enforces this requirement. By contrast, `clark-transformation-rules.md` RULE-IV-02 explicitly states: "WHEN `$.extensions` is absent or empty (zero entries), REJECT the input." The schema does not encode this rejection.

**Analysis:**
This is a critical semantic gap between the schema and the rules file. A use case at `detail_level: ESSENTIAL_OUTLINE` with no `extensions` array will PASS schema validation but will be REJECTED by the `/test-spec` skill at runtime. The schema cannot serve as a pre-validation gate for the `/test-spec` pipeline because it does not enforce this constraint. Any tooling that relies on schema validation to determine if a use case is "test-spec ready" will give a false positive.

**Response Required:**
Add an `allOf` conditional: when `detail_level` is `ESSENTIAL_OUTLINE` or `FULLY_DESCRIBED`, require `extensions` to be present and have `minItems: 1`. This aligns schema validation with RULE-IV-02.

**Acceptance Criteria:**
A use case with `detail_level: ESSENTIAL_OUTLINE` and no `extensions` field must fail schema validation with a clear message.

---

### DA-002: `source_detail_level` Enum Allows Values That Rules Would Reject [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Schema** | `test-specification-v1.schema.json` (lines 30-35) |
| **Strategy Step** | S-002 Step 3 — Counter-argument: Unstated Assumptions |

**Evidence:**
```json
"source_detail_level": {
  "type": "string",
  "enum": ["ESSENTIAL_OUTLINE", "FULLY_DESCRIBED"],
  "description": "...Clark transformation requires >= ESSENTIAL_OUTLINE; BRIEFLY_DESCRIBED and BULLETED_OUTLINE are rejected."
}
```
The `enum` is correctly restricted to valid values. However, the test-specification schema has no cross-reference constraint to verify that `source_detail_level` in the frontmatter actually matches the source use case's current `detail_level`. A test spec could declare `source_detail_level: ESSENTIAL_OUTLINE` even if the source use case was later downgraded (or if the field was manually populated incorrectly).

**Analysis:**
The schema validates the frontmatter in isolation. There is no mechanism to verify that `source_use_case: UC-LIB-001` actually resolves to a use case file at `ESSENTIAL_OUTLINE` or above. This is an inherent limitation of schema-only validation. However, the description's claim that "BRIEFLY_DESCRIBED and BULLETED_OUTLINE are rejected" is misleading because it implies the schema performs this rejection — it does not; it only prevents those strings from appearing in `source_detail_level`. A test spec could fraudulently self-certify as having been generated from ESSENTIAL_OUTLINE source.

**Response Required:**
Update the `source_detail_level` description to clarify it records the detail level at generation time and that cross-reference verification requires tooling beyond schema validation. Additionally, add a `minLength: 1` constraint and document the expectation that the `/test-spec` skill sets this field.

---

### DA-003: `realization_level = STORY_DEFINED` Does Not Require `slices` [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Schema** | `use-case-realization-v1.schema.json` (`allOf` section, lines 448-503) |
| **Strategy Step** | S-002 Step 3 — Unstated Assumptions |

**Evidence:**
The `allOf` section contains a conditional: when `realization_level = INTERACTION_DEFINED`, then `interactions` must be present with `minItems: 1`. However, the `slices` property description states: "Present when realization_level >= STORY_DEFINED." No corresponding `allOf` conditional enforces the presence of `slices` when `realization_level = STORY_DEFINED`.

**Analysis:**
The schema enforces the INTERACTION_DEFINED constraint but is asymmetric — it does not enforce the STORY_DEFINED constraint. A use case declaring `realization_level: STORY_DEFINED` with no `slices` array would pass validation, producing an internally inconsistent artifact. The `uc-slicer` agent is designed to produce slices when elevating to STORY_DEFINED; the schema should enforce this contract.

**Response Required:**
Add an `allOf` conditional for `realization_level = STORY_DEFINED` that requires `slices` to be present with `minItems: 1`, mirroring the pattern already used for `INTERACTION_DEFINED`.

---

### DA-004: `scenario_count` Equality with `coverage.mapped_flows` Not Enforced [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Schema** | `test-specification-v1.schema.json` (lines 49-53 vs. 75-83) |
| **Strategy Step** | S-002 Step 3 — Logical Flaws |

**Evidence:**
`scenario_count` description: "Total number of Gherkin scenarios generated. Must equal coverage.mapped_flows."
`coverage.mapped_flows` description: "Number of flows successfully mapped to Gherkin scenarios."

The description asserts these must be equal, but no schema constraint (e.g., `$ref`, `if/then`, or `const` referencing another field) enforces this. JSON Schema Draft 2020-12 does not support cross-field equality constraints natively without `$data` (non-standard) or complex `if/then` patterns.

**Analysis:**
A test specification artifact could have `scenario_count: 5` and `coverage.mapped_flows: 4` and pass schema validation. This would be a logically inconsistent artifact that would mislead the `tspec-analyst` agent. While JSON Schema cannot enforce cross-field equality natively without significant complexity, the description's use of "Must equal" sets an expectation that the schema enforces what it cannot.

**Response Required:**
Either (1) remove "Must equal coverage.mapped_flows" from the description and document this as a runtime constraint enforced by the `tspec-generator` agent during self-validation, or (2) implement a verification via `allOf` with a comment that this is best-effort schema enforcement. The description should accurately reflect what the schema enforces versus what is convention.

---

### DA-005: `supporting_actors[].type` Enum Missing `"external"` Type [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Schema** | `use-case-realization-v1.schema.json` (`$defs` supporting_actors, lines 159-163) |
| **Strategy Step** | S-002 Step 3 — Contradicting Evidence |

**Evidence:**
Schema enum:
```json
"type": {
  "type": "string",
  "enum": ["human", "system", "timer"],
  "description": "Actor classification."
}
```
`use-case-writing-rules.md` Rule 3.2: "Supporting actors are entities that participate but do not own the goal. Record each in `supporting_actors[]` with `name` and `type` (human, system, timer, external)."

**Analysis:**
The rule file documents four valid actor types: `human`, `system`, `timer`, and `external`. The schema enum only includes three. An agent following the rules file that creates a supporting actor with `type: "external"` will produce an artifact that fails schema validation. This is a direct conflict between the two authoritative sources.

**Recommendation:**
Add `"external"` to the `supporting_actors[].type` enum to align with Rule 3.2. The description should be updated to match.

---

### CV-001: `source_detail_level` Description Incorrectly Claims Schema Enforces Rejection [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Schema** | `test-specification-v1.schema.json` (lines 30-35) |
| **Strategy Step** | S-011 Step 4 — Consistency Check (MATERIAL DISCREPANCY) |

**Claim (from schema):**
`"description": "Detail level of the source use case at generation time. Clark transformation requires >= ESSENTIAL_OUTLINE; BRIEFLY_DESCRIBED and BULLETED_OUTLINE are rejected."`

**Source Document:**
`clark-transformation-rules.md` RULE-IV-01: "WHEN `$.detail_level` is `BRIEFLY_DESCRIBED` or `BULLETED_OUTLINE`, REJECT the input..."

**Independent Verification:**
RULE-IV-01 is an input validation rule executed by the `tspec-generator` agent at runtime. It is NOT implemented by the schema. The schema's `enum: ["ESSENTIAL_OUTLINE", "FULLY_DESCRIBED"]` prevents those two strings from appearing in the `source_detail_level` field of a test spec frontmatter — but this only means a test spec cannot self-declare those values; it does not mean the schema validates the source use case's detail level.

**Discrepancy:**
The schema description states "BRIEFLY_DESCRIBED and BULLETED_OUTLINE are rejected" — this is true at the rule-engine level, but the description is written in a context that implies the schema performs this rejection. A reader of the schema description would believe the schema enforces this constraint when it does not. The `enum` in the schema enforces what values `source_detail_level` can take in the test spec frontmatter, not whether the referenced source UC is at the right level.

**Correction:**
Change the description to: "Detail level of the source use case at generation time. Must be ESSENTIAL_OUTLINE or FULLY_DESCRIBED. Clark transformation (RULE-IV-01) rejects source use cases below ESSENTIAL_OUTLINE at runtime; this field records the validated level at generation time."

---

### CV-002: Sample Artifact `APPROVED` Status at `BRIEFLY_DESCRIBED` Inconsistency [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Schema** | `use-case-realization-v1.schema.json` and `sample-use-case.md` |
| **Strategy Step** | S-011 Step 3 — Independent Verification |

**Claim (implied by schema):**
The schema `status` enum is `["DRAFT", "REVIEW", "APPROVED"]` and `detail_level` has `"BRIEFLY_DESCRIBED"` as a valid value. The schema description for `detail_level` states "Progressive elaboration: BRIEFLY_DESCRIBED -> BULLETED_OUTLINE -> ESSENTIAL_OUTLINE -> FULLY_DESCRIBED" implying a lifecycle progression.

**Source Document:**
`sample-use-case.md` frontmatter:
```yaml
detail_level: BRIEFLY_DESCRIBED
status: APPROVED
```

**Independent Verification:**
The sample artifact has a use case at `BRIEFLY_DESCRIBED` detail level with `APPROVED` status. A BRIEFLY_DESCRIBED use case lacks extensions, alternative flows, and full step typing — making it arguably inappropriate for APPROVED status in any real workflow. The `clark-transformation-rules.md` RULE-IV-01 would reject this artifact for test spec generation. Yet the schema permits this combination without any conditional constraint.

**Discrepancy:**
The sample artifact models a combination (`BRIEFLY_DESCRIBED` + `APPROVED`) that the rules file downstream would reject for use-case-to-test-spec processing. This creates a misleading sample that shows a valid-schema but operationally inconsistent artifact. The schema should either enforce that `APPROVED` requires a minimum `detail_level` (at minimum `ESSENTIAL_OUTLINE`) or the sample should use `status: DRAFT`.

**Correction:**
Either (1) add a schema constraint that `status: APPROVED` requires `detail_level: ESSENTIAL_OUTLINE` or `FULLY_DESCRIBED` via an `allOf` conditional, or (2) update the sample artifact to reflect a more realistic lifecycle state (e.g., `status: DRAFT` or `detail_level: ESSENTIAL_OUTLINE`).

---

### CV-003: `interaction.id` Pattern Allows 3-Digit IDs; Description Says 2-Digit Only [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Schema** | `use-case-realization-v1.schema.json` `$defs.interaction` (lines 410-413) |
| **Strategy Step** | S-011 Step 4 — Consistency Check (MINOR DISCREPANCY escalated to MAJOR) |

**Claim (from schema):**
```json
"id": {
  "type": "string",
  "pattern": "^INT-\\d{2,3}$",
  "description": "Interaction identifier. Format: INT-{NN}. Example: INT-01."
}
```

**Independent Verification:**
Pattern `^INT-\\d{2,3}$` matches both `INT-01` (2 digits) and `INT-001` (3 digits). Description says "Format: INT-{NN}" (2 digits). Example is `INT-01` (2 digits).

**Discrepancy:**
The pattern allows 2 OR 3 digits but the description and example show only 2 digits. This ambiguity means tooling generating interaction IDs might produce `INT-001` (3 digits) while other tooling generating cross-references might assume 2-digit format. The `source_flow` pattern in the same `interaction` object uses `EXT-\\d+[A-Z]` (unlimited digits before the letter) and `AF-\\d{2}` (exactly 2 digits) — inconsistent patterns across the same `$defs` context. The `extension.id` pattern uses `^EXT-\\d+[A-Z]$` (no length constraint on digits) while `alternative_flow.id` uses `^AF-\\d{2}$` (exactly 2). The `interaction.id` pattern should commit to one format.

**Correction:**
If the intent is 2-digit IDs (as the example suggests), change the pattern to `^INT-\\d{2}$`. If 3-digit is needed for use cases with many interactions, change the description to "Format: INT-{NN} or INT-{NNN}. Example: INT-01, INT-100." Synchronize across all ID patterns in `$defs` for consistency.

---

### CV-004: `coverage_percentage` Computation Not Capturable in Schema [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Schema** | `test-specification-v1.schema.json` (lines 85-90) |
| **Strategy Step** | S-011 Step 4 — Consistency Check |

**Claim (from schema):**
`"description": "Mapped flows / total flows * 100. Optional; computable from mapped_flows and total_flows."`

**Independent Verification:**
`quality.coverage_target_met` is described as: "Whether coverage meets goal-level target. USER_GOAL requires 100%, SUBFUNCTION 80%, SUMMARY 60%." The coverage target depends on `source_goal_level` (a separate top-level field) and `coverage_percentage`. No `allOf` conditional links these two.

**Discrepancy:**
`coverage_percentage` is described as computable but the schema does not enforce that the stored value equals the computation. More critically, `quality.coverage_target_met` cannot be automatically derived at schema validation time because it requires comparing `coverage_percentage` against a threshold determined by `source_goal_level`. This creates a situation where `coverage_target_met: true` and `coverage_percentage: 60` with `source_goal_level: USER_GOAL` (requires 100%) would both pass validation — a logically invalid combination.

**Recommendation:**
Document in the `quality.coverage_target_met` description that this field is set by the `tspec-generator` agent during self-validation and cannot be schema-verified. Remove the implied enforcement expectation from field descriptions.

---

### IN-001: Invalid Combination `BRIEFLY_DESCRIBED` + `INTERACTION_DEFINED` Passes Validation [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Schema** | `use-case-realization-v1.schema.json` (missing cross-constraint) |
| **Strategy Step** | S-013 Step 2 — Invert the Goals (Anti-Goals) |

**Anti-Goal:**
Goal: "Schema must reject invalid use case artifacts." Anti-goal inversion: "What combination of valid field values would produce an invalid use case that passes schema validation?"

**Evidence:**
The following artifact is schema-valid but operationally invalid:
```yaml
id: UC-TEST-001
title: "Test Use Case"
work_type: USE_CASE
version: "1.0.0"
status: DRAFT
goal_level: USER_GOAL
goal_symbol: "!"
primary_actor: "User"
detail_level: BRIEFLY_DESCRIBED        # <-- minimal detail
realization_level: INTERACTION_DEFINED  # <-- maximum realization
trigger: "User does something"
preconditions: ["User is logged in"]
postconditions:
  success: ["Done"]
  failure: ["Failed"]
basic_flow:
  - step: 1
    actor: "User"
    action: "does something"
    type: actor_action
  - step: 2
    actor: "System"
    action: "responds"
    type: system_response
  - step: 3
    actor: "User"
    action: "confirms"
    type: actor_action
interactions:
  - id: "INT-01"
    source_step: 1
    source_flow: "basic_flow"
    actor_role: "consumer"
    system_role: "receiver"
    request_description: "User request"
    response_description: "System response"
created_at: "2026-03-11T00:00:00Z"
created_by: "test"
```

**Analysis:**
`realization_level: INTERACTION_DEFINED` is the most advanced realization state, intended to indicate that interaction sequences are fully defined and ready for `/contract-design`. `detail_level: BRIEFLY_DESCRIBED` is the most basic detail level with no extensions, alternative flows, or typed steps beyond basics. The combination is nonsensical: you cannot have interaction-level realization with only a brief description. The `use-case-writing-rules.md` Activity 5 Realization Rules require FULLY_DESCRIBED level for INTERACTION_DEFINED realization. The schema has no cross-constraint linking `detail_level` and `realization_level`.

**Recommendation:**
Add an `allOf` conditional: when `realization_level` is `STORY_DEFINED`, require `detail_level` to be `ESSENTIAL_OUTLINE` or `FULLY_DESCRIBED`; when `realization_level` is `INTERACTION_DEFINED`, require `detail_level` to be `FULLY_DESCRIBED`.

---

### IN-002: Test Spec `mapped_flows > total_flows` Passes Validation [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Schema** | `test-specification-v1.schema.json` (coverage object) |
| **Strategy Step** | S-013 Step 2 — Anti-Goals |

**Anti-Goal:**
Goal: "Test specification schema must represent coverage accurately." Anti-goal: "What values would allow a mathematically impossible coverage claim to pass validation?"

**Evidence:**
```yaml
coverage:
  basic_flow_mapped: true
  extensions_mapped: 5
  total_flows: 4
  mapped_flows: 5
```
This artifact would pass schema validation (all fields have correct types, all minimums met). Yet `mapped_flows: 5 > total_flows: 4` is logically impossible — you cannot map more flows than exist.

**Analysis:**
The schema enforces `minimum: 1` on both `total_flows` and `mapped_flows` but does not enforce `mapped_flows <= total_flows`. The `coverage_percentage` field (optional) could then compute to 125%, which would also pass given `minimum: 0, maximum: 100` but 125% would actually fail the range constraint. However, `coverage_percentage` is optional and can be omitted, so the impossible coverage ratio passes validation silently.

**Recommendation:**
Add a constraint that `mapped_flows <= total_flows`. In JSON Schema Draft 2020-12, this cannot be expressed natively as a cross-field constraint without `if/then` patterns. As a practical measure: add a `maximum` to `mapped_flows` that references the schema intent. Consider documenting this as a runtime validation responsibility of `tspec-generator` and add `quality.no_orphan_flows` as the authoritative check flag.

---

### IN-003: `flow_step.actor` Not Validated Against Declared Actors [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Schema** | `use-case-realization-v1.schema.json` `$defs.flow_step` |
| **Strategy Step** | S-013 Step 3 — Map All Assumptions |

**Assumption Inverted:**
"Assumption: `actor` values in `basic_flow`, `extensions`, and `alternative_flows` will match the `primary_actor`, `supporting_actors[].name`, or `'System'`."

**Evidence:**
`flow_step.actor` description: "Actor performing this step. Must be primary_actor, a supporting_actor name, or 'System'." Schema constraint: `"type": "string", "minLength": 1`. No pattern, enum, or cross-reference enforces this against the declared actors.

**Analysis:**
`use-case-writing-rules.md` Rule 3.3 states "Every `actor` field in `basic_flow[*]` steps MUST match either `primary_actor`, a `supporting_actors[*].name` entry, or the literal value 'System'." This is a meaningful integrity constraint — a flow step referencing an undeclared actor is a data consistency error. The sample artifact demonstrates the correct pattern (`actor: "Library Member"` matches `primary_actor: "Library Member"`, `actor: "System"` is the literal). However, the schema does not enforce this; an actor string like `"Unauthorized User"` that is not declared anywhere in the use case would pass validation.

**Analysis of Feasibility:**
JSON Schema does not natively support dynamic enum generation from sibling fields. Enforcing this constraint would require a custom keyword, a JSON Schema extension, or runtime validation. Given that JSON Schema Draft 2020-12 does not support this natively, this is a known schema limitation.

**Recommendation:**
Update the `flow_step.actor` description to explicitly state: "Enforced by uc-author runtime validation (Rule 3.3 of use-case-writing-rules.md); schema cannot enforce cross-field actor consistency." This prevents the misleading implication that the schema enforces what it cannot. Optionally, document a test artifact that validates this constraint is checked by the `uc-author` agent.

---

### IN-004: `basic_flow` Step Numbers Not Required to be Sequential [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Schema** | `use-case-realization-v1.schema.json` `$defs.flow_step.step` |
| **Strategy Step** | S-013 Step 4 — Stress-Test Assumptions |

**Assumption Inverted:**
"Assumption: `basic_flow` step numbers are sequential integers starting at 1 (1, 2, 3, ...)."

**Evidence:**
`flow_step.step` constraint: `"type": "integer", "minimum": 1`. No `uniqueItems` on the `basic_flow` array, no sequential ordering enforcement.

**Analysis:**
The schema validates that each `step` value is a positive integer but does not enforce: (1) uniqueness of step numbers within a flow, (2) sequential ordering (no gaps), or (3) that the sequence starts at 1. A `basic_flow` with steps `[1, 3, 5]` would pass validation. `clark-transformation-rules.md` RULE-C3-01 references `basic_flow` steps by number in source annotations (`steps 1-{N}`), assuming sequential numbering. The Clark transformation algorithm relies on sequential step order for clause generation. Non-sequential or duplicate step numbers could produce incorrect BDD output.

**Recommendation:**
Add `"uniqueItems": true` to the `basic_flow` array definition to prevent duplicate step numbers. Sequential ordering enforcement (no gaps) cannot be expressed in JSON Schema without significant complexity; document this as a runtime constraint verified by `uc-author`.

---

## S-003 Steelman Assessment

**Steelman Finding: Schema Design Strengths**

The schemas demonstrate several genuine design strengths that warrant acknowledgment:

**SM-001 — The `allOf` Goal-Symbol Cross-Constraint Pattern is Excellent Architecture [Major Strength]:**
The use of `allOf` with `if/then/properties` to enforce `goal_level`/`goal_symbol` consistency is a correct and idiomatic use of JSON Schema Draft 2020-12 conditional composition. This pattern provides machine-readable enforcement of the Cockburn goal-level taxonomy and could serve as a template for other cross-field constraints. The description notes "Enforced by allOf constraints" — this is accurate for the cases where `goal_symbol` IS present. The gap (absent `goal_symbol`) identified in SR-003 is a gap in the constraint's completeness, not a flaw in the approach.

**SM-002 — `$defs` Reuse Across Flow Contexts is Clean [Minor Strength]:**
Using `$ref: "#/$defs/flow_step"` across `basic_flow`, `extensions[].steps`, and `alternative_flows[].steps` ensures consistent step structure across all flow types. This eliminates schema duplication and guarantees that the Clark transformation can apply identical step-type-to-clause mapping regardless of flow context.

**SM-003 — `INTERACTION_DEFINED` Conditional is Correctly Implemented [Minor Strength]:**
The `allOf` conditional requiring `interactions` when `realization_level = INTERACTION_DEFINED` demonstrates the correct pattern for implementing lifecycle-based conditional requirements. The gap (identified in DA-003) is that this pattern was not also applied to `STORY_DEFINED -> slices`.

---

## Execution Statistics

- **Total Findings:** 20
- **Critical:** 5 (SR-001, DA-001, CV-001, IN-001 — plus SM-001 as strength)
- **Major:** 11 (SR-002, SR-003, DA-002, DA-003, DA-004, CV-002, CV-003, IN-002, IN-003)
- **Minor:** 5 (SR-004, SR-005, DA-005, CV-004, IN-004)
- **Steelman Strengths Identified:** 3 (SM-001, SM-002, SM-003)
- **Protocol Steps Completed:** 5 of 5 strategies executed

---

## Protocol Steps Summary

| Strategy | Steps Completed | Key Focus |
|----------|----------------|-----------|
| S-010 (Self-Refine) | 6 of 6 | Completeness, internal consistency, Draft 2020-12 usage, cross-schema coherence |
| S-003 (Steelman) | 6 of 6 | Identified design strengths before critique phase; `allOf` pattern, `$defs` reuse, lifecycle conditional |
| S-002 (Devil's Advocate) | 5 of 5 | Challenged enum choices (DA-005), conditional coverage (DA-001, DA-003), cross-field constraints (DA-004), assumption consistency (DA-002) |
| S-011 (Chain-of-Verification) | 5 of 5 | Verified descriptions against rule files and sample artifacts; 4 claims verified, 4 material discrepancies found |
| S-013 (Inversion) | 6 of 6 | Generated 4 anti-goal scenarios; 3 invalid-but-passing artifacts constructed; 1 assumption shown unenforced |

---

## Priority Remediation Order

**P0 — Must resolve before schemas are used as validation gates:**

1. **SR-001** — Change `additionalProperties: true` to `false` at root level of use-case-realization schema
2. **DA-001** — Add `allOf` conditional requiring `extensions` when `detail_level` is `ESSENTIAL_OUTLINE` or `FULLY_DESCRIBED`
3. **IN-001** — Add `allOf` conditional cross-constraining `detail_level` and `realization_level`
4. **CV-001** — Fix `source_detail_level` description to not imply schema-level enforcement
5. **SR-003** — Add `goal_symbol` to the `required` array

**P1 — Should resolve before production use:**

6. **DA-003** — Add `allOf` conditional requiring `slices` when `realization_level = STORY_DEFINED`
7. **CV-003** — Resolve `interaction.id` pattern/description mismatch (commit to 2-digit or 3-digit)
8. **DA-005** — Add `"external"` to `supporting_actors[].type` enum
9. **SR-002** — Clarify or simplify `parent_id` null semantics
10. **CV-002** — Enforce or sample-correct APPROVED/BRIEFLY_DESCRIBED inconsistency
11. **DA-004** — Update `scenario_count` description to remove "Must equal" enforcement implication
12. **IN-002** — Document `mapped_flows <= total_flows` as runtime constraint; update description
13. **IN-003** — Update `flow_step.actor` description to clarify schema limitation

**P2 — Minor improvements:**

14. **SR-004** — Add `work_type: TEST_SPECIFICATION` discriminator
15. **SR-005** — Add `required` array to `invest_assessment` object
16. **DA-002** — Update `source_detail_level` description
17. **CV-004** — Clarify `coverage_percentage` and `coverage_target_met` as runtime-set fields
18. **IN-004** — Add `uniqueItems: true` to `basic_flow` array

---

*Report generated by adv-executor agent*
*Strategies applied: S-010, S-003, S-002, S-011, S-013*
*Finding prefix series: SR (Self-Refine), SM (Steelman), DA (Devil's Advocate), CV (Chain-of-Verification), IN (Inversion)*
*H-16 compliance: S-003 (Steelman) executed before S-002 (Devil's Advocate) — VERIFIED*
*H-15 self-review: Applied before persistence*
