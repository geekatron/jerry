# Behavior Tests: /use-case Skill

> **File ID:** F-16 | **Skill:** /use-case | **Version:** 1.0.0
> **Author:** eng-qa | **Date:** 2026-03-08 | **Criticality:** C3
> **Status:** PROPOSED
> **Standard:** H-20 (BDD test-first), H-23 (navigation table required)
> **Schema:** `docs/schemas/use-case-realization-v1.schema.json`

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | Scope, methodology, coverage summary |
| [Coverage Matrix](#coverage-matrix) | Implementation files and H-rules covered |
| [Feature: uc-author Agent](#feature-uc-author-agent) | All uc-author behavioral scenarios |
| [Scenario 1: Happy Path Creation](#scenario-1-happy-path-creation) | A-001 -- system capability to artifact |
| [Scenario 2: Input Validation Rejection](#scenario-2-input-validation-rejection) | A-002 -- vague request escalation |
| [Scenario 3: Detail Level Progression](#scenario-3-detail-level-progression) | A-003 -- BULLETED to ESSENTIAL elaboration |
| [Scenario 4: BRIEFLY_DESCRIBED Output](#scenario-4-brieflydescribed-output) | A-004 -- brief template selection |
| [Scenario 5: Goal Symbol Consistency Enforcement](#scenario-5-goal-symbol-consistency-enforcement) | A-005 -- schema allOf constraints 3-5 |
| [Scenario 6: Status Remains DRAFT](#scenario-6-status-remains-draft) | A-006 -- guardrail status_must_remain_DRAFT |
| [Scenario 7: Elaboration of Non-Existent Artifact](#scenario-7-elaboration-of-non-existent-artifact) | A-007 -- missing artifact error path |
| [Scenario 8: Basic Flow Step Count Boundary](#scenario-8-basic-flow-step-count-boundary) | A-008 -- 3-min 9-max schema constraint |
| [Scenario 9: Flow Step Type Classification Required](#scenario-9-flow-step-type-classification-required) | A-009 -- all_flow_steps_must_have_typed_classification |
| [Scenario 10: Actor Reference Integrity](#scenario-10-actor-reference-integrity) | A-010 -- Layer 2 actor cross-field check |
| [Feature: uc-slicer Agent](#feature-uc-slicer-agent) | All uc-slicer behavioral scenarios |
| [Scenario 11: Happy Path Slicing](#scenario-11-happy-path-slicing) | S-001 -- ESSENTIAL_OUTLINE to STORY_DEFINED |
| [Scenario 12: BULLETED_OUTLINE Input Rejection](#scenario-12-bulletedoutline-input-rejection) | S-002 -- detail_level guard |
| [Scenario 13: INTERACTION_DEFINED Schema Constraint](#scenario-13-interactiondefined-schema-constraint) | S-003 -- allOf constraint 1 |
| [Scenario 14: INVEST Assessment Required per Slice](#scenario-14-invest-assessment-required-per-slice) | S-004 -- slice quality gate |
| [Scenario 15: Basic Flow Is First Slice](#scenario-15-basic-flow-is-first-slice) | S-005 -- basic_flow_must_be_first_slice guardrail |
| [Scenario 16: Lifecycle State Must Not Skip SCOPED](#scenario-16-lifecycle-state-must-not-skip-scoped) | S-006 -- LIFECYCLE VIOLATION guard |
| [Scenario 17: Realization Level Derived Consistency](#scenario-17-realization-level-derived-consistency) | S-007 -- REALIZATION VIOLATION guard |
| [Scenario 18: STORY_DEFINED allOf Constraint 2](#scenario-18-story_defined-allof-constraint-2) | S-008 -- slices required at STORY_DEFINED |
| [Scenario 19: Worktracker Story Creation via Bash](#scenario-19-worktracker-story-creation-via-bash) | S-009 -- P-003 Bash-only integration |
| [Feature: Cross-Agent Pipeline](#feature-cross-agent-pipeline) | E2E pipeline and handoff contract scenarios |
| [Scenario 20: uc-author Output Consumed by uc-slicer](#scenario-20-uc-author-output-consumed-by-uc-slicer) | E-001 -- end-to-end pipeline |
| [Scenario 21: Handoff Contract Fields Present](#scenario-21-handoff-contract-fields-present) | E-002 -- SV-04 SV-06 handoff validation |
| [Scenario 22: P-003 No Sub-Agent Delegation](#scenario-22-p-003-no-sub-agent-delegation) | E-003 -- constitutional compliance |
| [Feature: Schema Validation Gate](#feature-schema-validation-gate) | JSON Schema Layer 1 deterministic validation |
| [Scenario 23: Required Fields Presence](#scenario-23-required-fields-presence) | V-001 -- 11 required fields |
| [Scenario 24: ID Pattern Enforcement](#scenario-24-id-pattern-enforcement) | V-002 -- UC-{DOMAIN}-{NNN} pattern |
| [Scenario 25: Enum Validity Enforcement](#scenario-25-enum-validity-enforcement) | V-003 -- all enum fields |
| [Scenario 26: Extension ID Pattern Enforcement](#scenario-26-extension-id-pattern-enforcement) | V-004 -- EXT-{step}{letter} pattern |
| [Acceptance Verification Checklist](#acceptance-verification-checklist) | Reviewer checklist for F-16 completeness |

---

## Overview

This file defines the BDD behavior test specifications for the `/use-case` skill per H-20 (BDD test-first) and architecture specification F-16. All scenarios are written in full Gherkin format (Feature / Scenario / Given / When / Then) with concrete inputs and verifiable assertions, expanding the 7 architecture scenario stubs into 26 complete scenarios.

### Scope

| In Scope | Out of Scope |
|----------|-------------|
| uc-author behavioral correctness | /test-spec skill (tspec-generator) |
| uc-slicer behavioral correctness | /contract-design skill (cd-generator) |
| JSON Schema Layer 1 validation | Python pytest execution (no Python implementation) |
| Agent guardrail Layer 2 validation | Network/MCP integration |
| uc-author to uc-slicer handoff contract | IMPLEMENTED and VERIFIED lifecycle states |
| P-003 constitutional compliance | External worktracker CLI correctness |

### Methodology

All scenarios follow Gherkin BDD format:

```
Feature: [agent or subsystem]
  Background: [shared setup for all scenarios in feature, if applicable]
  Scenario: [concrete scenario name]
    Given [precondition -- observable system state or artifact state]
    When  [trigger -- agent invocation or validation action]
    Then  [assertion -- observable verifiable outcome]
    And   [additional assertion]
```

Scenarios are organized into four Features: `uc-author Agent`, `uc-slicer Agent`, `Cross-Agent Pipeline`, and `Schema Validation Gate`. Within each Feature, scenarios are ordered from happy path through negative cases to edge cases, targeting the 60%/30%/10% distribution from testing-standards.md.

### Coverage Summary

| Category | Scenario Count | Percentage |
|----------|---------------|-----------|
| Happy path | 7 (A-001, A-003, A-004, S-001, S-009, E-001, E-002) | 27% |
| Negative / rejection | 11 (A-002, A-007, A-008, S-002, S-006, S-007, S-008, V-001 through V-004) | 42% |
| Edge / boundary | 8 (A-005, A-006, A-009, A-010, S-003, S-004, S-005, E-003) | 31% |
| **Total** | **26** | 100% |

### Architecture Scenario Stubs Coverage

| Architecture Stub | Expanded Into | Status |
|------------------|---------------|--------|
| Stub 1: Happy path creation | Scenario 1 (A-001) | COVERED |
| Stub 2: Invalid/empty input escalation | Scenario 2 (A-002) | COVERED |
| Stub 3: BULLETED to ESSENTIAL elaboration | Scenario 3 (A-003) | COVERED |
| Stub 4: Happy path slicing with INVEST | Scenario 11 (S-001) | COVERED |
| Stub 5: BULLETED_OUTLINE input rejection | Scenario 12 (S-002) | COVERED |
| Stub 6: INTERACTION_DEFINED allOf constraint | Scenario 13 (S-003) | COVERED |
| Stub 7: E2E pipeline uc-author to uc-slicer | Scenario 20 (E-001) | COVERED |

---

## Coverage Matrix

### Implementation Files Covered

| File ID | File | Scenarios |
|---------|------|-----------|
| F-02 | `skills/use-case/agents/uc-author.md` | A-001 through A-010, E-001, E-002, E-003 |
| F-03 | `skills/use-case/agents/uc-author.governance.yaml` | A-005, A-006, A-009, E-003 |
| F-04 | `skills/use-case/agents/uc-slicer.md` | S-001 through S-009, E-001, E-002, E-003 |
| F-05 | `skills/use-case/agents/uc-slicer.governance.yaml` | S-003, S-005, S-006, S-007, E-003 |
| F-11 | `skills/use-case/templates/use-case-brief.template.md` | A-004 |
| F-12 | `skills/use-case/templates/use-case-casual.template.md` | A-001, A-003 |
| F-10 | `skills/use-case/templates/use-case-realization.template.md` | A-003, S-001 |
| F-13 | `skills/use-case/templates/use-case-slice.template.md` | S-001, S-004 |
| F-14 | `skills/use-case/rules/use-case-writing-rules.md` | A-001, A-003, A-004, A-005, A-008, A-009, S-001, S-006 |
| F-17 | `docs/schemas/use-case-realization-v1.schema.json` | V-001 through V-004, S-003, S-008, A-005, A-008 |

### HARD Rules Covered

| Rule | Description | Scenarios |
|------|-------------|-----------|
| H-20 | BDD test-first -- this file is the H-20 deliverable | All 26 |
| H-31 | Clarify when ambiguous -- escalate to user for vague requests | A-002, A-007 |
| P-003 | No recursive sub-agents -- T2 worker, no Task tool | E-003, A-002 |
| P-020 | User authority -- never override scope/actor/goal-level decisions | A-002, S-009 |
| P-022 | No deception -- never misrepresent detail_level or slice_state | A-006, S-007 |

### Schema Constraints Covered

| allOf Constraint | Description | Scenarios |
|-----------------|-------------|-----------|
| allOf[0] | interactions minItems:1 when realization_level=INTERACTION_DEFINED | S-003, E-001 |
| allOf[1] | slices minItems:1 when realization_level=STORY_DEFINED or INTERACTION_DEFINED | S-008 |
| allOf[2] | goal_symbol="+" when goal_level=SUMMARY | A-005 |
| allOf[3] | goal_symbol="!" when goal_level=USER_GOAL | A-005 |
| allOf[4] | goal_symbol="-" when goal_level=SUBFUNCTION | A-005 |

---

## Feature: uc-author Agent

The uc-author agent creates and elaborates use case artifacts using Cockburn's 12-step writing process and Jacobson UC 2.0 progressive narrative levels. These scenarios verify uc-author behavioral contracts, guardrail enforcement, and schema compliance.

### Scenario 1: Happy Path Creation

**ID:** A-001 | **Architecture Stub:** Stub 1 | **Coverage:** F-02, F-12, F-14 | **Category:** Happy path

```gherkin
Feature: uc-author Agent

  Scenario: Happy path creation of a use case artifact from a system capability description
    Given the user provides the request "Write a use case for user authentication in the AUTH domain"
    And no existing artifact exists at "projects/PROJ-021-use-case/use-cases/"
    And the JERRY_PROJECT environment variable is set to "PROJ-021-use-case"

    When uc-author is invoked with the request

    Then a file is created at "projects/PROJ-021-use-case/use-cases/UC-AUTH-001-authenticate-user.md"
    And the file contains YAML frontmatter delimited by "---"
    And the frontmatter field "work_type" equals "USE_CASE"
    And the frontmatter field "id" matches the pattern "^UC-[A-Z]+-\d{3}$"
    And the frontmatter field "status" equals "DRAFT"
    And the frontmatter field "goal_level" is one of "SUMMARY", "USER_GOAL", "SUBFUNCTION"
    And the frontmatter field "basic_flow" contains between 3 and 9 step objects
    And each step object in "basic_flow" has a non-empty "type" field
    And the artifact validates against "docs/schemas/use-case-realization-v1.schema.json" with zero errors
    And uc-author reports the use case ID, title, goal level, and detail level achieved in its L0 summary
```

### Scenario 2: Input Validation Rejection

**ID:** A-002 | **Architecture Stub:** Stub 2 | **Coverage:** F-02, F-03 | **Category:** Negative case

```gherkin
  Scenario: Vague user request triggers H-31 escalation with actionable guidance
    Given the user provides the request "make a use case"
    And the request does not identify any actor, system capability, or domain

    When uc-author is invoked with the request

    Then uc-author does NOT create any artifact file
    And uc-author asks exactly one clarifying question directed at identifying the actor goal
    And the clarifying question uses phrasing equivalent to "What does the actor achieve?"
    And uc-author does NOT proceed to Steps 1-4 until the user responds
    And the response contains no use case artifact output
```

### Scenario 3: Detail Level Progression

**ID:** A-003 | **Architecture Stub:** Stub 3 | **Coverage:** F-02, F-10, F-14 | **Category:** Happy path

```gherkin
  Scenario: Elaboration of an existing BULLETED_OUTLINE artifact to ESSENTIAL_OUTLINE
    Given a use case artifact exists at "projects/PROJ-021-use-case/use-cases/UC-AUTH-001-authenticate-user.md"
    And the artifact has YAML frontmatter with "detail_level: BULLETED_OUTLINE"
    And the artifact has a "basic_flow" with 5 step objects
    And the artifact has an empty "extensions" array
    And the user requests "Elaborate UC-AUTH-001 to Essential Outline"

    When uc-author is invoked with the elaboration request

    Then the artifact at "projects/PROJ-021-use-case/use-cases/UC-AUTH-001-authenticate-user.md" is updated in place
    And the frontmatter field "detail_level" equals "ESSENTIAL_OUTLINE"
    And the frontmatter field "extensions" is a non-empty array containing at least 1 extension object
    And each extension object has the fields "id", "name", "anchor_step", "condition", "steps", "outcome"
    And the frontmatter field "preconditions" is present and non-empty
    And the frontmatter field "postconditions" is present with at least "success" sub-array
    And the artifact validates against "docs/schemas/use-case-realization-v1.schema.json" with zero errors
    And uc-author confirms in its L0 summary that detail_level was advanced from BULLETED_OUTLINE to ESSENTIAL_OUTLINE
```

### Scenario 4: BRIEFLY_DESCRIBED Output

**ID:** A-004 | **Coverage:** F-02, F-11, F-14 | **Category:** Happy path

```gherkin
  Scenario: Brief template is selected when user requests BRIEFLY_DESCRIBED level
    Given the user provides the request "Write a brief use case for placing an order in the ORD domain"
    And the user specifies target detail level "BRIEFLY_DESCRIBED"

    When uc-author is invoked with the request

    Then a file is created at a path matching "projects/PROJ-021-use-case/use-cases/UC-ORD-\d{3}-.*\.md"
    And the frontmatter field "detail_level" equals "BRIEFLY_DESCRIBED"
    And the frontmatter field "basic_flow" contains at least 3 step objects
    And the frontmatter field "extensions" is absent or empty
    And the artifact validates against "docs/schemas/use-case-realization-v1.schema.json" with zero errors
    And the output file is structurally consistent with the brief template at "skills/use-case/templates/use-case-brief.template.md"
```

### Scenario 5: Goal Symbol Consistency Enforcement

**ID:** A-005 | **Coverage:** F-17 (allOf[2,3,4]), F-03 | **Category:** Edge case

```gherkin
  Scenario: goal_symbol is set consistently with goal_level per schema allOf constraints
    Given the user requests a SUMMARY-level use case
    And uc-author is invoked

    When uc-author writes the artifact

    Then the frontmatter field "goal_level" equals "SUMMARY"
    And the frontmatter field "goal_symbol" equals "+"
    And the artifact passes allOf constraints 2-4 in "docs/schemas/use-case-realization-v1.schema.json"

  Scenario: USER_GOAL symbol consistency
    Given the user requests a sea-level user goal use case

    When uc-author writes the artifact

    Then "goal_level" equals "USER_GOAL"
    And "goal_symbol" equals "!"

  Scenario: SUBFUNCTION symbol consistency
    Given the user requests a subfunction use case

    When uc-author writes the artifact

    Then "goal_level" equals "SUBFUNCTION"
    And "goal_symbol" equals "-"
```

### Scenario 6: Status Remains DRAFT

**ID:** A-006 | **Coverage:** F-02, F-03 | **Category:** Edge case -- guardrail enforcement

```gherkin
  Scenario: uc-author never sets status to REVIEW or APPROVED without explicit user instruction
    Given uc-author creates or elaborates any use case artifact

    When the artifact is written to disk

    Then the frontmatter field "status" equals "DRAFT"
    And "status" is NOT "REVIEW"
    And "status" is NOT "APPROVED"
    And "status" is NOT "DEPRECATED"

  Scenario: uc-author changes status to REVIEW only when user explicitly instructs it
    Given a use case artifact at "DRAFT" status
    And the user explicitly says "Mark UC-AUTH-001 as ready for review"

    When uc-author processes the instruction

    Then the frontmatter field "status" equals "REVIEW"
    And uc-author confirms the status change in its L0 summary
```

### Scenario 7: Elaboration of Non-Existent Artifact

**ID:** A-007 | **Coverage:** F-02, F-03 | **Category:** Negative case

```gherkin
  Scenario: Elaboration request for a file that does not exist triggers actionable error
    Given the user requests "Elaborate UC-AUTH-999 to ESSENTIAL_OUTLINE"
    And no file exists matching "projects/PROJ-021-use-case/use-cases/UC-AUTH-999-*.md"

    When uc-author attempts to load the artifact

    Then uc-author does NOT create a new use case artifact
    And uc-author reports the specific error: the referenced artifact path does not exist
    And uc-author asks whether the user wants to create a new use case or correct the artifact path
    And uc-author does NOT proceed with elaboration
```

### Scenario 8: Basic Flow Step Count Boundary

**ID:** A-008 | **Coverage:** F-17 (basic_flow minItems:3 maxItems:9), F-14 | **Category:** Negative case

```gherkin
  Scenario: Basic flow with fewer than 3 steps is rejected at validation
    Given uc-author has drafted a basic_flow with only 2 step objects

    When uc-author attempts to validate the artifact against the schema

    Then schema validation fails with an error referencing "basic_flow" and "minItems: 3"
    And uc-author does NOT write the invalid artifact to disk
    And uc-author requests that the user provide at least one additional flow step

  Scenario: Basic flow with more than 9 steps triggers user guidance
    Given uc-author encounters a use case whose basic_flow draft contains 10 step objects

    When uc-author identifies the step count exceeds 9

    Then uc-author does NOT write a basic_flow with 10 steps
    And uc-author asks the user whether to decompose into sub-use cases or reduce abstraction level
    And uc-author explains that Cockburn Guideline 6 constrains basic_flow to 3-9 steps
```

### Scenario 9: Flow Step Type Classification Required

**ID:** A-009 | **Coverage:** F-03 (all_flow_steps_must_have_typed_classification), F-14 | **Category:** Edge case

```gherkin
  Scenario: Every flow step object must have a non-empty type field
    Given uc-author is creating a use case with a 5-step basic_flow
    And step 3 is drafted without a "type" field

    When uc-author applies the output guardrail "all_flow_steps_must_have_typed_classification"

    Then the artifact is not written to disk without all steps having a "type" field
    And "type" for each step is one of "actor_action", "system_response", or "validation"
    And uc-author assigns a type to the missing step or asks the user to confirm the classification
```

### Scenario 10: Actor Reference Integrity

**ID:** A-010 | **Coverage:** F-02 (Layer 2 guardrail), F-14 Rule 3.3 | **Category:** Edge case

```gherkin
  Scenario: Actor name in a flow step must match primary_actor or supporting_actors[*].name
    Given a use case with "primary_actor: User" and "supporting_actors: [{name: Auth Service, type: system}]"
    And uc-author drafts a basic_flow step with "actor: AuthenticationService"

    When uc-author applies the Layer 2 semantic validation guardrail

    Then uc-author detects that "AuthenticationService" does not match "User", "Auth Service", or "System"
    And uc-author either corrects the actor name to the nearest valid match
    Or escalates to the user per H-31 if the correct name is ambiguous
    And the artifact is NOT written with an unresolved actor reference
```

---

## Feature: uc-slicer Agent

The uc-slicer agent decomposes use case artifacts into implementation-ready slices following Jacobson UC 2.0 Activities 2, 4, and 5. These scenarios verify uc-slicer behavioral contracts, the five-state lifecycle, schema allOf constraints, and INVEST enforcement.

### Scenario 11: Happy Path Slicing

**ID:** S-001 | **Architecture Stub:** Stub 4 | **Coverage:** F-04, F-13, F-14 | **Category:** Happy path

```gherkin
Feature: uc-slicer Agent

  Scenario: Happy path slicing of an ESSENTIAL_OUTLINE artifact to STORY_DEFINED
    Given a use case artifact exists at "projects/PROJ-021-use-case/use-cases/UC-AUTH-001-authenticate-user.md"
    And the artifact has "detail_level: ESSENTIAL_OUTLINE"
    And the artifact has a "basic_flow" with exactly 5 step objects
    And the artifact has "extensions" with at least 2 extension objects
    And the artifact has "work_type: USE_CASE"

    When uc-slicer is invoked on the artifact

    Then the artifact is updated in place at the same path
    And the frontmatter field "slices" is a non-empty array with at least 1 slice object
    And the first slice object has a "slice_id" matching "^UC-AUTH-001-S1$"
    And the first slice's "steps_included" references "basic_flow" steps
    And each slice object has an "invest_assessment" object with all 6 boolean fields present
    And each slice object has "slice_state" set to "SCOPED" or higher
    And the artifact validates against "docs/schemas/use-case-realization-v1.schema.json" including all allOf constraints with zero errors
    And uc-slicer reports slice count, slice IDs, and INVEST pass/fail summary in its L0 summary
```

### Scenario 12: BULLETED_OUTLINE Input Rejection

**ID:** S-002 | **Architecture Stub:** Stub 5 | **Coverage:** F-04, F-05 | **Category:** Negative case

```gherkin
  Scenario: uc-slicer rejects input artifact at BULLETED_OUTLINE with actionable error message
    Given a use case artifact exists at "projects/PROJ-021-use-case/use-cases/UC-AUTH-001-authenticate-user.md"
    And the artifact has "detail_level: BULLETED_OUTLINE"

    When uc-slicer is invoked on the artifact

    Then uc-slicer does NOT create any slice objects
    And uc-slicer does NOT modify the artifact
    And uc-slicer returns an error message containing the text "detail_level must be >= ESSENTIAL_OUTLINE"
    And the error message identifies the current detail_level as "BULLETED_OUTLINE"
    And the error message instructs the user to invoke uc-author to elaborate the use case first

  Scenario: uc-slicer rejects input artifact at BRIEFLY_DESCRIBED
    Given a use case artifact exists with "detail_level: BRIEFLY_DESCRIBED"

    When uc-slicer is invoked on the artifact

    Then uc-slicer rejects with an error message containing "detail_level must be >= ESSENTIAL_OUTLINE"
    And uc-slicer identifies "BRIEFLY_DESCRIBED" as the current level in the error message
```

### Scenario 13: INTERACTION_DEFINED Schema Constraint

**ID:** S-003 | **Architecture Stub:** Stub 6 | **Coverage:** F-17 (allOf[0]), F-04 | **Category:** Edge case

```gherkin
  Scenario: Setting realization_level=INTERACTION_DEFINED without interactions array fails allOf constraint 1
    Given a use case artifact with "realization_level: INTERACTION_DEFINED"
    And the artifact does NOT have an "interactions" array in its frontmatter

    When schema validation runs against "docs/schemas/use-case-realization-v1.schema.json"

    Then schema validation FAILS
    And the validation error references the allOf[0] constraint
    And the error indicates that "interactions" is required when "realization_level" is "INTERACTION_DEFINED"
    And the error indicates that "interactions" must have at least 1 item

  Scenario: uc-slicer prevents REALIZATION VIOLATION by populating interactions before setting INTERACTION_DEFINED
    Given uc-slicer has completed Activity 5 and has a non-empty interactions array ready to write
    And "realization_level" is currently "STORY_DEFINED"

    When uc-slicer writes the artifact update

    Then "interactions" is written to the artifact before "realization_level: INTERACTION_DEFINED" is set
    And the final artifact has "interactions" with at least 1 interaction object
    And each interaction object has all required fields: "id", "source_step", "source_flow", "actor_role", "system_role", "request_description", "response_description"
    And the artifact passes allOf constraint 1 validation
```

### Scenario 14: INVEST Assessment Required per Slice

**ID:** S-004 | **Coverage:** F-04, F-13 | **Category:** Edge case

```gherkin
  Scenario: Each slice must have a complete INVEST assessment before state transition from SCOPED to PREPARED
    Given uc-slicer has identified 2 slice candidates from the use case flows
    And slice "UC-AUTH-001-S2" has been created with "slice_state: SCOPED"
    And slice "UC-AUTH-001-S2" does NOT yet have an "invest_assessment" object

    When uc-slicer attempts to transition "UC-AUTH-001-S2" to "slice_state: PREPARED"

    Then the transition is NOT made without an invest_assessment
    And uc-slicer applies all 6 INVEST criteria (independent, negotiable, valuable, estimable, small, testable)
    And each criterion is recorded as a boolean in the "invest_assessment" object
    And if any criterion is false, uc-slicer reports the failing criteria to the user
    And uc-slicer asks whether to redefine slice boundaries or proceed with documented exceptions
```

### Scenario 15: Basic Flow Is First Slice

**ID:** S-005 | **Coverage:** F-04, F-05 (basic_flow_must_be_first_slice) | **Category:** Edge case

```gherkin
  Scenario: The slice containing the basic_flow happy path must be the first slice created (S1)
    Given a use case artifact with a 5-step basic_flow and 2 extension branches

    When uc-slicer identifies slice candidates and creates slice definitions

    Then the first slice object has "slice_id" ending in "-S1"
    And the first slice's "steps_included" array includes at least one entry referencing "basic_flow"
    And extension-derived slices have "slice_id" values ending in "-S2", "-S3", etc. (never "-S1")
    And uc-slicer does NOT assign a non-basic-flow slice to the "-S1" position
```

### Scenario 16: Lifecycle State Must Not Skip SCOPED

**ID:** S-006 | **Coverage:** F-04, F-05 (LIFECYCLE VIOLATION guard) | **Category:** Negative case

```gherkin
  Scenario: uc-slicer never creates a slice directly at PREPARED state, bypassing SCOPED
    Given uc-slicer is executing Activity 2 slice identification

    When uc-slicer creates a new slice definition

    Then the slice is initially written with "slice_state: SCOPED"
    And the slice is NOT created with "slice_state: PREPARED" or "slice_state: ANALYZED" on first creation
    And the INVEST assessment is completed before any state transition to PREPARED

  Scenario: Slice transitions follow sequential order SCOPED > PREPARED > ANALYZED
    Given a slice exists with "slice_state: SCOPED"
    And the INVEST assessment is complete with all 6 criteria true

    When uc-slicer advances the slice to PREPARED state

    Then "slice_state" transitions to "PREPARED"
    And "test_cases" array is non-empty before the PREPARED state is written
    And "slice_state" does NOT jump from SCOPED to ANALYZED
```

### Scenario 17: Realization Level Derived Consistency

**ID:** S-007 | **Coverage:** F-04, F-05 (REALIZATION VIOLATION guard) | **Category:** Negative case

```gherkin
  Scenario: uc-slicer never sets realization_level without verifying the corresponding blocks are populated
    Given a use case artifact with "slices" populated and "interactions" empty
    And uc-slicer has NOT completed Activity 5

    When uc-slicer prepares to write "realization_level: INTERACTION_DEFINED"

    Then uc-slicer verifies that "interactions" is non-empty before writing the field
    And uc-slicer does NOT write "realization_level: INTERACTION_DEFINED" when interactions is empty
    And if interactions is empty, uc-slicer sets "realization_level: STORY_DEFINED" instead

  Scenario: realization_level=STORY_DEFINED requires slices but not interactions
    Given uc-slicer has completed Activity 2 and has SCOPED slices

    When uc-slicer writes the updated artifact with "realization_level: STORY_DEFINED"

    Then "slices" is non-empty in the artifact
    And "interactions" may be absent without triggering a validation error
    And the artifact passes allOf constraint 1 (which only fires for INTERACTION_DEFINED)
```

### Scenario 18: STORY_DEFINED allOf Constraint 2

**ID:** S-008 | **Coverage:** F-17 (allOf[1]) | **Category:** Negative case

```gherkin
  Scenario: Setting realization_level=STORY_DEFINED without slices array fails allOf constraint 2
    Given a use case artifact with "realization_level: STORY_DEFINED"
    And the artifact does NOT have a "slices" array in its frontmatter

    When schema validation runs against "docs/schemas/use-case-realization-v1.schema.json"

    Then schema validation FAILS
    And the validation error references the allOf[1] constraint
    And the error indicates that "slices" is required when "realization_level" is "STORY_DEFINED" or "INTERACTION_DEFINED"
    And the error indicates that "slices" must have at least 1 item
```

### Scenario 19: Worktracker Story Creation via Bash

**ID:** S-009 | **Coverage:** F-04 | **Category:** Happy path

```gherkin
  Scenario: uc-slicer creates worktracker Story entities via Bash CLI, not via Task tool
    Given a slice "UC-AUTH-001-S1" has reached "slice_state: PREPARED"
    And test cases have been defined for the slice

    When uc-slicer creates the worktracker Story entity for the slice

    Then uc-slicer uses the Bash tool to execute "uv run jerry items create" (not the Task tool)
    And the command is invoked with H-05: "uv run jerry items create" prefix (never bare "jerry items create")
    And uc-slicer does NOT invoke any /worktracker agent via the Task tool
    And if the Bash command fails, uc-slicer reports the error and persists slice definitions to the artifact file
    And uc-slicer notes in its L0 summary that Story entity creation failed and must be retried
```

---

## Feature: Cross-Agent Pipeline

These scenarios verify the end-to-end handoff contract between uc-author and uc-slicer, P-003 constitutional compliance, and the orchestration pattern.

### Scenario 20: uc-author Output Consumed by uc-slicer

**ID:** E-001 | **Architecture Stub:** Stub 7 | **Coverage:** F-02, F-04, F-17 | **Category:** Happy path

```gherkin
Feature: Cross-Agent Pipeline

  Scenario: End-to-end pipeline -- uc-author artifact passes uc-slicer input validation without modification
    Given uc-author has created a use case artifact at "projects/PROJ-021-use-case/use-cases/UC-AUTH-001-authenticate-user.md"
    And uc-author's post-creation verification reported schema validation PASS
    And the artifact has "detail_level: ESSENTIAL_OUTLINE"
    And the artifact has "work_type: USE_CASE"
    And the artifact has a "basic_flow" with 5 steps
    And the artifact has a non-empty "extensions" array

    When uc-slicer is invoked on the artifact path without any manual modification to the file

    Then uc-slicer accepts the artifact and proceeds to Activity 2 slice identification
    And uc-slicer does NOT report a schema validation error on input
    And uc-slicer does NOT report a detail_level insufficiency error
    And uc-slicer creates at least 1 slice with "slice_state: SCOPED"
    And the final artifact validates against "docs/schemas/use-case-realization-v1.schema.json" including all allOf constraints
```

### Scenario 21: Handoff Contract Fields Present

**ID:** E-002 | **Coverage:** F-02, F-04 | **Category:** Happy path

```gherkin
  Scenario: uc-author session_context.on_send produces the fields required by the uc-slicer handoff contract
    Given uc-author has completed creating a use case artifact

    When uc-author delivers its session completion summary (on_send)

    Then the summary includes "artifact_path" pointing to the created file
    And the summary includes "detail_level" reporting the achieved level
    And the summary includes "key_findings" with between 3 and 5 bullet items covering actor count, goal level, basic flow step count, and extension count
    And "detail_level" in the summary is >= "ESSENTIAL_OUTLINE" before uc-slicer invocation is triggered
    And the "artifact_path" resolves to an existing file on disk (SV-04 check)
    And uc-author explicitly flags whether the detail_level is sufficient for /test-spec consumption
```

### Scenario 22: P-003 No Sub-Agent Delegation

**ID:** E-003 | **Coverage:** F-03, F-05 (P-003 forbidden action) | **Category:** Edge case

```gherkin
  Scenario: Neither uc-author nor uc-slicer uses the Task tool for any operation
    Given uc-author is executing any operation (creating, elaborating, or validating an artifact)

    When the operation requires accessing the worktracker or another agent

    Then uc-author does NOT invoke the Task tool
    And uc-author uses "uv run jerry items create" via Bash for any worktracker operations
    And uc-author is NOT classified as a T5 agent

  Scenario: uc-slicer does not delegate to uc-author or any other agent via Task
    Given uc-slicer is executing Activity 2, 4, or 5

    When uc-slicer encounters a condition that might benefit from uc-author elaboration

    Then uc-slicer does NOT invoke uc-author via Task tool
    And uc-slicer reports the condition to the user and asks for explicit guidance
    And uc-slicer does NOT spawn any sub-agent under any circumstance
```

---

## Feature: Schema Validation Gate

These scenarios verify the JSON Schema Layer 1 deterministic validation constraints from `docs/schemas/use-case-realization-v1.schema.json`. These are structural tests that verify the schema enforces required fields, patterns, and enums independently of agent behavior.

### Scenario 23: Required Fields Presence

**ID:** V-001 | **Coverage:** F-17 (required array) | **Category:** Negative case

```gherkin
Feature: Schema Validation Gate

  Scenario: An artifact missing any required field fails schema validation
    Given a use case artifact frontmatter that omits the "primary_actor" field
    And all other required fields are present: id, title, work_type, version, status, goal_level, scope, basic_flow, created_at, created_by

    When the artifact is validated against "docs/schemas/use-case-realization-v1.schema.json"

    Then schema validation FAILS
    And the error identifies "primary_actor" as the missing required field

  Scenario: An artifact with all 11 required fields passes required-field validation
    Given a use case artifact frontmatter with all 11 required fields populated with valid values:
      | Field       | Example Value                      |
      | id          | UC-AUTH-001                        |
      | title       | Authenticate User                  |
      | work_type   | USE_CASE                           |
      | version     | 1.0.0                              |
      | status      | DRAFT                              |
      | goal_level  | USER_GOAL                          |
      | scope       | System                             |
      | primary_actor | User                             |
      | basic_flow  | [3 valid flow_step objects]        |
      | created_at  | 2026-03-08T00:00:00Z               |
      | created_by  | uc-author                          |

    When the artifact is validated against the schema

    Then schema validation PASSES with zero errors
```

### Scenario 24: ID Pattern Enforcement

**ID:** V-002 | **Coverage:** F-17 ("id" pattern constraint) | **Category:** Negative case

```gherkin
  Scenario: An artifact with a malformed "id" field fails the pattern constraint
    Given a use case artifact with "id: UC-auth-001" (lowercase domain)

    When the artifact is validated against the schema

    Then schema validation FAILS
    And the error references the "id" field and the pattern "^UC-[A-Z]+-\d{3}$"

  Scenario: A valid id passes pattern validation
    Given a use case artifact with "id: UC-AUTH-001"

    When the artifact is validated against the schema

    Then the "id" field passes pattern validation

  Scenario: id pattern with numeric suffix boundary -- exactly 3 digits required
    Given a use case artifact with "id: UC-AUTH-01" (only 2-digit numeric suffix)

    When the artifact is validated against the schema

    Then schema validation FAILS with a pattern mismatch on the "id" field
```

### Scenario 25: Enum Validity Enforcement

**ID:** V-003 | **Coverage:** F-17 (enum arrays for goal_level, status, detail_level, slice_state) | **Category:** Negative case

```gherkin
  Scenario: An artifact with an invalid goal_level enum value fails validation
    Given a use case artifact with "goal_level: SEA_LEVEL" (not in the valid enum)

    When the artifact is validated against the schema

    Then schema validation FAILS
    And the error references "goal_level" and the valid enum values "SUMMARY", "USER_GOAL", "SUBFUNCTION"

  Scenario: An artifact with an invalid status enum value fails validation
    Given a use case artifact with "status: IN_PROGRESS" (not in the valid enum)

    When the artifact is validated against the schema

    Then schema validation FAILS
    And the error references "status" and the valid enum values "DRAFT", "REVIEW", "APPROVED", "DEPRECATED"

  Scenario: An artifact with an invalid detail_level enum value fails validation
    Given a use case artifact with "detail_level: PARTIAL" (not in the valid enum)

    When the artifact is validated against the schema

    Then schema validation FAILS
    And the error references "detail_level" and the valid enum values
```

### Scenario 26: Extension ID Pattern Enforcement

**ID:** V-004 | **Coverage:** F-17 ("extension" $def id pattern) | **Category:** Negative case

```gherkin
  Scenario: An extension object with a malformed id fails the pattern constraint
    Given a use case artifact with an extension object having "id: EXT-3" (missing the letter suffix)

    When the artifact is validated against the schema

    Then schema validation FAILS
    And the error references the "id" field within the extensions array
    And the error cites the pattern "^EXT-\d+[a-z]$"

  Scenario: A valid extension id passes pattern validation
    Given a use case artifact with an extension object having "id: EXT-3a"

    When the artifact is validated against the schema

    Then the extension "id" field passes pattern validation

  Scenario: extension outcome field pattern enforcement
    Given a use case artifact with an extension object having "outcome: error" (not a valid pattern)

    When the artifact is validated against the schema

    Then schema validation FAILS on the "outcome" field
    And the error indicates valid patterns are "success", "failure", or "rejoin:{step}"
```

---

## Acceptance Verification Checklist

Use this checklist when reviewing F-16 for completeness and H-20 compliance before closing sub-step 10f.

### H-20 BDD Compliance

- [ ] All 26 scenarios are written in Gherkin format with Feature / Scenario / Given / When / Then structure
- [ ] All 7 architecture scenario stubs (Stubs 1-7) are expanded with concrete inputs and verifiable assertions
- [ ] Concrete input values are used (specific paths, specific field values) not abstract descriptions
- [ ] All Then assertions are observable (file state, field values, error messages) not internal agent state

### Architecture Stub Coverage

- [ ] Stub 1 (Happy path creation) covered by A-001
- [ ] Stub 2 (Input validation escalation) covered by A-002
- [ ] Stub 3 (BULLETED to ESSENTIAL elaboration) covered by A-003
- [ ] Stub 4 (Happy path slicing with INVEST) covered by S-001
- [ ] Stub 5 (BULLETED_OUTLINE rejection) covered by S-002
- [ ] Stub 6 (INTERACTION_DEFINED allOf constraint) covered by S-003
- [ ] Stub 7 (E2E pipeline) covered by E-001

### Schema Constraint Coverage

- [ ] allOf[0] (interactions at INTERACTION_DEFINED) covered by S-003 and E-001
- [ ] allOf[1] (slices at STORY_DEFINED+) covered by S-008
- [ ] allOf[2,3,4] (goal_symbol consistency) covered by A-005
- [ ] All 11 required fields tested by V-001
- [ ] ID pattern tested by V-002
- [ ] Enum enforcement tested by V-003 and V-004

### Guardrail Coverage

- [ ] P-003 no-sub-agent guardrail tested by E-003 and S-009
- [ ] P-020 user authority tested by A-002 (no proceeding without clarification)
- [ ] P-022 no deception tested by A-006 (status honesty) and S-007 (realization level honesty)
- [ ] H-31 escalation tested by A-002 and A-007
- [ ] H-05 `uv run` prefix tested by S-009

### Navigation and Format

- [ ] Navigation table present (H-23 -- this file is > 30 lines)
- [ ] All navigation table entries use anchor links (H-24)
- [ ] Scenario IDs follow pattern: A-NNN (uc-author), S-NNN (uc-slicer), E-NNN (E2E), V-NNN (validation)
- [ ] Coverage matrix maps scenarios to implementation files and H-rules
- [ ] No emojis in file content
- [ ] No secrets, passwords, tokens, or PII in any scenario input
