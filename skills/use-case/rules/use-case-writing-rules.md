# Use Case Writing Rules

> Operational rules for `uc-author` and `uc-slicer` agents encoding Cockburn's 12-step use case writing
> process and Jacobson UC 2.0 lifecycle management. Load progressively per CB-05:
> Steps 1-4 for BRIEFLY_DESCRIBED, Steps 1-10 for ESSENTIAL_OUTLINE, full file for FULLY_DESCRIBED.

<!-- L2-REINJECT: rank=5, content="Cockburn 12-step process: Steps 1-4 (scope first, breadth before depth). Goal levels: SUMMARY(+), USER_GOAL(!), SUBFUNCTION(-). Detail levels: BRIEFLY_DESCRIBED < BULLETED_OUTLINE < ESSENTIAL_OUTLINE < FULLY_DESCRIBED. UC 2.0 lifecycle: Scoped > Prepared > Analyzed > Implemented > Verified." -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [Progressive Loading Guide](#progressive-loading-guide) | Which steps to load at each detail level |
| [Steps 1-4: Foundation Phase](#steps-1-4-foundation-phase) | Scope, actors, goals, brief -- always required |
| [Steps 5-10: Elaboration Phase](#steps-5-10-elaboration-phase) | MSS, extensions, alternatives -- required for ESSENTIAL_OUTLINE+ |
| [Steps 11-12: Completion Phase](#steps-11-12-completion-phase) | Full description, stakeholder review -- required for FULLY_DESCRIBED |
| [Goal Level Rules](#goal-level-rules) | SUMMARY, USER_GOAL, SUBFUNCTION classification |
| [Detail Level Prerequisites](#detail-level-prerequisites) | What each level requires before it can be declared |
| [UC 2.0 Slice Lifecycle Rules](#uc-20-slice-lifecycle-rules) | Five-state lifecycle and transition conditions |
| [INVEST Criteria Rules](#invest-criteria-rules) | Slice quality verification |
| [Activity 5 Realization Rules](#activity-5-realization-rules) | Interaction sequence production for /contract-design |
| [Output Guardrails](#output-guardrails) | Non-negotiable constraints on all output |

---

## Progressive Loading Guide

Load this file selectively using Read offset/limit per CB-05 to prevent context exhaustion.

| Target Detail Level | Load Lines | Sections Covered |
|--------------------|------------|-----------------|
| BRIEFLY_DESCRIBED | Lines 1-120 | Steps 1-4 (Foundation Phase) + Goal Level Rules |
| BULLETED_OUTLINE | Lines 1-180 | Steps 1-6 (MSS added) |
| ESSENTIAL_OUTLINE | Lines 1-300 | Steps 1-10 (Extensions + Alternatives added) |
| FULLY_DESCRIBED | Full file | All 12 steps + Slice Lifecycle + Realization |

---

## Steps 1-4: Foundation Phase

> Always load. Required for every use case at any detail level.

### Step 1: Identify the Goal Level (PAT-001 -- Breadth First)

**Rule 1.1:** Determine goal level BEFORE writing any narrative. Never write the basic flow before classifying the goal.

**Classification rules:**

| Goal Level | Symbol | Cockburn Definition | When to Use |
|-----------|--------|---------------------|-------------|
| SUMMARY | + | Cloud/Kite -- organizational workflow spanning multiple user goals | System scope document, high-level capability map |
| USER_GOAL | ! | Sea Level -- actor achieves a measurable, valuable outcome in one session | Default; most use cases |
| SUBFUNCTION | - | Fish/Clam -- supporting step within a user goal, callable from multiple goals | Shared sub-process (e.g., "Validate User Session") |

**Rule 1.2:** The `goal_level` enum value and `goal_symbol` MUST be consistent per schema allOf constraints 3-5. Set both together.

**Rule 1.3:** Default to USER_GOAL (!) unless the use case clearly spans multiple sessions (use SUMMARY) or is clearly a supporting step never invoked standalone (use SUBFUNCTION).

---

### Step 2: Identify the Scope

**Rule 2.1:** Set `scope` to the system boundary: Enterprise, System, or Subsystem.

**Rule 2.2:** Set `domain` to the uppercase domain code (AUTH, KM, INV, etc.) that groups related use cases. Use the same domain code in the `id` field.

**Rule 2.3:** Set the `id` field to `UC-{DOMAIN}-{NNN}` format. The NNN is a sequential 3-digit number within the domain.

---

### Step 3: Identify the Primary Actor and Supporting Actors

**Rule 3.1:** The primary actor is the entity whose goal the use case satisfies. Record in `primary_actor`.

**Rule 3.2:** Supporting actors are entities that participate but do not own the goal. Record each in `supporting_actors[]` with `name` and `type` (human, system, timer, external).

**Rule 3.3:** Every `actor` field in `basic_flow[*]` steps MUST match either `primary_actor`, a `supporting_actors[*].name` entry, or the literal value "System".

**Rule 3.4:** Stakeholders (not actors) are entities with interests in the outcome. Record in `stakeholders[]` with `name` and `interest`. Stakeholders are optional at BRIEFLY_DESCRIBED; SHOULD be populated at ESSENTIAL_OUTLINE+.

---

### Step 4: Write the Brief

**Rule 4.1:** At BRIEFLY_DESCRIBED level, the use case consists of: `title` (verb-noun-context form), `primary_actor`, `goal_level`, `scope`, and a minimal `basic_flow` with 3 steps minimum.

**Rule 4.2:** The `title` MUST follow Cockburn naming: actor goal as title, verb-noun-context form (e.g., "Validate User Credentials", "Purchase Product", "Register Device").

**Rule 4.3:** Set `detail_level: BRIEFLY_DESCRIBED` and `status: DRAFT`.

**Rule 4.4:** Produce the artifact using the brief template (`skills/use-case/templates/use-case-brief.template.md`).

---

## Steps 5-10: Elaboration Phase

> Load for BULLETED_OUTLINE and above. Required for ESSENTIAL_OUTLINE and FULLY_DESCRIBED.

### Step 5: Write the Basic Flow (Main Success Scenario)

**Rule 5.1:** The basic flow is the happy path -- the sequence of steps when everything goes right.

**Rule 5.2:** The basic flow MUST have between 3 and 9 steps (Cockburn Guideline 6). Fewer than 3 indicates the use case is too small to be valuable; more than 9 indicates it needs decomposition.

**Rule 5.3:** Each step MUST have `step` (integer), `actor` (string matching Rule 3.3), `action` (verb-object form), and `type` (actor_action | system_response | validation).

**Rule 5.4:** Step type classification:
- `actor_action`: A human or external actor performs an action (maps to Gherkin When)
- `system_response`: The system processes input and produces output (maps to Gherkin Then)
- `validation`: The system validates state or input without producing new output (maps to Gherkin Then with assertion)

**Rule 5.5:** Write steps at the user-goal abstraction level. Avoid implementation-level detail (HTTP requests, database calls). Avoid too-abstract level (generic "user interacts with system").

**Rule 5.6:** After writing the basic flow, set `detail_level: BULLETED_OUTLINE`. Produce the artifact using the casual template (`skills/use-case/templates/use-case-casual.template.md`).

---

### Step 6: Identify Preconditions and Postconditions

**Rule 6.1:** `preconditions[]` are conditions assumed true when the use case begins. The system does not check these -- they are asserted by the calling context.

**Rule 6.2:** `postconditions.success[]` (success guarantees) are conditions guaranteed to be true when the basic flow completes successfully.

**Rule 6.3:** `postconditions.failure[]` (minimal guarantees) are conditions guaranteed to be true even when the use case fails at any point.

**Rule 6.4:** Set `trigger` to the event that initiates the use case (e.g., "User selects login from the navigation menu", "Timer fires at midnight UTC").

---

### Step 7: Write Extensions (Exception and Error Handling)

**Rule 7.1:** Extensions are step-anchored exception handling flows. Each extension is triggered by an exception condition at a specific basic_flow step.

**Rule 7.2:** Extension `id` format: `EXT-{step}{letter}` (e.g., EXT-3a for the first extension at step 3, EXT-3b for the second). The `anchor_step` integer MUST match the step number in the id.

**Rule 7.3:** Extension `outcome` MUST be one of:
- `success`: The extension reaches a separate successful end state
- `failure`: The use case fails (this extension becomes a negative test scenario in /test-spec)
- `rejoin:{step}`: The extension returns to the basic flow at the specified step number

**Rule 7.4:** Identify at minimum the following extension categories:
- Validation failures (invalid input at any actor_action step)
- System unavailability (system_response steps that depend on external services)
- Authorization failures (steps where access may be denied)
- Timeout conditions (long-running system_response steps)

**Rule 7.5:** Non-empty `extensions[]` is required before declaring `detail_level: FULLY_DESCRIBED`. Having zero extensions at Fully Described level is a semantic error indicating incomplete analysis.

---

### Step 8: Write Alternative Flows (AF)

**Rule 8.1:** Alternative flows are paths that branch from the basic flow and optionally rejoin it. They represent different ways to achieve the same goal (not error handling, which belongs in extensions).

**Rule 8.2:** Alternative flow `id` format: `AF-{NN}` (e.g., AF-01, AF-02).

**Rule 8.3:** `branches_from_step` is the basic_flow step where the alternative diverges. `rejoins_at_step` is the basic_flow step where it rejoins (null if separate exit).

**Rule 8.4:** Alternative flows are optional at ESSENTIAL_OUTLINE but SHOULD be populated when there are distinct user paths through the use case.

---

### Step 9: Verify Cockburn's Six Quality Indicators

Before advancing from BULLETED_OUTLINE to ESSENTIAL_OUTLINE, verify all six quality indicators:

| # | Indicator | Check |
|---|-----------|-------|
| 1 | Goal level appropriate | Use case is at the right abstraction (not too high, not too low) |
| 2 | Title is actor-goal | Title names the actor and what they accomplish |
| 3 | 3-9 basic flow steps | Step count within the Cockburn Guideline 6 range |
| 4 | Primary actor achieves goal | Basic flow ends with actor achieving their goal |
| 5 | Extensions cover exceptions | At least one extension per external dependency |
| 6 | No design decisions in flow | No implementation-level detail in step actions |

---

### Step 10: Advance to ESSENTIAL_OUTLINE

**Rule 10.1:** Set `detail_level: ESSENTIAL_OUTLINE` when:
- `basic_flow` has 3-9 steps
- `extensions[]` is non-empty (at least one exception documented)
- `preconditions[]` and `postconditions.success[]` are populated
- All six quality indicators from Step 9 pass

**Rule 10.2:** ESSENTIAL_OUTLINE is the MINIMUM level required for downstream `/test-spec` and `/contract-design` consumption. Artifacts at BRIEFLY_DESCRIBED or BULLETED_OUTLINE will be rejected by uc-slicer input validation.

**Rule 10.3:** Produce the artifact using the full realization template (`skills/use-case/templates/use-case-realization.template.md`).

---

## Steps 11-12: Completion Phase

> Load for FULLY_DESCRIBED only. Skip for ESSENTIAL_OUTLINE deliverables.

### Step 11: Extract Sub-Use Cases

**Rule 11.1:** Identify steps in the basic flow that represent reusable subfunctions invoked from multiple use cases. Each such step is a candidate for a separate SUBFUNCTION use case.

**Rule 11.2:** If a subfunction is extracted, replace the basic_flow step with a reference step (e.g., "System invokes UC-AUTH-002 Validate Session Token"). Record the extracted use case's `id` in `related_use_cases[]` and set its `parent_id` to this use case's `id`.

**Rule 11.3:** Extracted subfunctions change the primary use case's step count. Verify the 3-9 step constraint still holds after extraction.

---

### Step 12: Declare FULLY_DESCRIBED

**Rule 12.1:** Set `detail_level: FULLY_DESCRIBED` ONLY when ALL of the following are true:
- `extensions[]` is non-empty (Rule 7.5 satisfied)
- All known exception conditions at each basic_flow step are documented
- `stakeholders[]` is populated
- Sub-use cases are identified and extracted where appropriate
- All six quality indicators from Step 9 pass
- Human stakeholder review has been requested (status may still be DRAFT until review complete)

**Rule 12.2:** Do NOT advance to FULLY_DESCRIBED until extensions are complete. Declaring FULLY_DESCRIBED with empty extensions causes downstream /test-spec to produce incomplete test coverage.

---

## Goal Level Rules

| Rule | Description |
|------|-------------|
| GL-01 | `goal_symbol` and `goal_level` MUST be consistent: SUMMARY=(+), USER_GOAL=(!), SUBFUNCTION=(-) |
| GL-02 | A SUMMARY use case MUST reference child USER_GOAL use cases in `related_use_cases[]` |
| GL-03 | A SUBFUNCTION use case MUST set `parent_id` to a USER_GOAL use case id |
| GL-04 | Default to USER_GOAL when goal level is ambiguous |
| GL-05 | Do NOT write extensions for SUMMARY-level use cases -- they have no detailed flows |

---

## Detail Level Prerequisites

Violating these prerequisites causes downstream agent rejection.

| Level | Required Fields | Required Conditions |
|-------|----------------|---------------------|
| BRIEFLY_DESCRIBED | id, title, work_type, version, status, goal_level, scope, primary_actor, basic_flow (min 3 steps), created_at, created_by | goal_symbol consistent with goal_level |
| BULLETED_OUTLINE | + preconditions, postconditions.success, trigger | basic_flow steps all have type field |
| ESSENTIAL_OUTLINE | + extensions (non-empty), stakeholders | All 6 quality indicators pass (Step 9) |
| FULLY_DESCRIBED | + alternative_flows where applicable, sub-UC extraction complete | Extensions complete for all exception paths |

---

## UC 2.0 Slice Lifecycle Rules

> Load for uc-slicer operations (Activity 2, 4, 5).

### Slice State Machine

```
SCOPED --> PREPARED --> ANALYZED --> IMPLEMENTED --> VERIFIED
```

| State | Entry Condition | What Exists at This State |
|-------|----------------|--------------------------|
| SCOPED | Slice identified from flows | `slice_id`, `title`, `steps_included`, `invest_assessment` |
| PREPARED | INVEST criteria verified, test cases defined | + `test_cases[]` (non-empty) |
| ANALYZED | Activity 5 complete | + `realization_level: STORY_DEFINED` or `INTERACTION_DEFINED`, `interactions[]` for INTERACTION_DEFINED |
| IMPLEMENTED | Software built | External tracker (worktracker Story entity) |
| VERIFIED | Acceptance tests passed | External tracker update |

### Slice Transition Rules

**SL-01:** The basic flow MUST be the first slice (slice_id ending in -S1). This slice contains the happy path and is always the highest priority.

**SL-02:** NEVER create a slice at PREPARED state without non-empty `test_cases[]`. The test cases define the acceptance criteria for the implementer.

**SL-03:** NEVER advance `slice_state` without explicitly setting the new state value. The state field is not auto-derived.

**SL-04:** When creating a worktracker Story entity for a slice, use `uv run jerry items create` (H-05 compliant). NEVER invoke `/worktracker` via Task tool (P-003 violation for T2 worker).

---

## INVEST Criteria Rules

Verify all six INVEST criteria before allowing a slice to transition from SCOPED to PREPARED.

| Criterion | Test Question | Action if FAIL |
|-----------|---------------|----------------|
| **I**ndependent | Can this slice be implemented without requiring another slice first? | Redefine slice boundaries to remove dependency |
| **N**egotiable | Can the scope of this slice be negotiated with stakeholders? | Remove implementation commitments from scope |
| **V**aluable | Does this slice deliver end-to-end value to a real user? | Merge with adjacent slices until value is visible |
| **E**stimable | Can the team estimate effort for this slice? | Add more detail to `steps_included` or split further |
| **S**mall | Can this slice be implemented in one sprint? | Split into smaller slices |
| **T**estable | Can the acceptance criteria be verified? | Add test cases before advancing |

**IC-01:** Record the assessment in `invest_assessment{}` as boolean fields. A slice with any `false` INVEST value MUST NOT advance to PREPARED state without explicit user approval of the exception.

---

## Activity 5 Realization Rules

> Load for full FULLY_DESCRIBED + INTERACTION_DEFINED work only.

### Identifying Interactions from Flows

**R5-01:** An interaction is identified at every `system_response` step that implies an API boundary crossing. Not every `system_response` step is an interaction -- only those where the system calls or receives calls from an external actor or system component.

**R5-02:** Each interaction MUST have `id` (INT-{NN}), `source_step`, `source_flow`, `actor_role` (consumer|provider), `system_role` (receiver|provider), `request_description`, and `response_description`.

**R5-03:** `source_step` MUST reference a valid step number in the flow referenced by `source_flow`. `source_flow` value must match: `basic_flow`, `AF-{NN}`, or `EXT-{step}{letter}`.

**R5-04:** `actor_role = consumer` means the actor initiates the request (maps to API caller). `actor_role = provider` means the actor provides a service (maps to API server).

**R5-05:** NEVER set `realization_level: INTERACTION_DEFINED` without verifying that `interactions[]` is non-empty and every interaction in the array is complete with all required fields. This is enforced by schema allOf constraint 1.

**R5-06:** After populating `interactions[]`, explicitly set `realization_level: INTERACTION_DEFINED` on the artifact. This is the signal consumed by `/contract-design`.

---

## Output Guardrails

These rules apply to all output from both `uc-author` and `uc-slicer`. Non-negotiable.

| Guardrail | Rule |
|-----------|------|
| OG-01 | NEVER write an artifact with `status` other than `DRAFT` without explicit user approval. Human review is required before REVIEW or APPROVED. |
| OG-02 | NEVER declare a `detail_level` higher than what the artifact content actually supports. Downgrade the declared level to match content if necessary. |
| OG-03 | NEVER produce an artifact that fails validation against `docs/schemas/use-case-realization-v1.schema.json`. Fix the artifact before persisting. |
| OG-04 | NEVER include secrets, passwords, tokens, or personally identifiable information in use case artifact content. |
| OG-05 | NEVER advance `slice_state` or `realization_level` without verifying the required content blocks are populated (SL-03, R5-05). |
| OG-06 | ALWAYS set `created_at` to the current ISO-8601 datetime at artifact creation. Set `updated_at` on every subsequent modification. |
| OG-07 | ALWAYS set `created_by` to the agent name (uc-author or uc-slicer) at creation. Set `last_modified_by` on every subsequent modification. |

---

*Rules Version: 1.0.0*
*Source: Cockburn (2001) Writing Effective Use Cases, Jacobson et al. (2011) Use-Case 2.0*
*Applied by: uc-author, uc-slicer*
*Schema SSOT: docs/schemas/use-case-realization-v1.schema.json*
*Last Updated: 2026-03-08*
