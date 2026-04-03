---
# === IDENTITY BLOCK ===
id: UC-{DOMAIN}-{NNN}
title: "{TITLE}"
work_type: USE_CASE
version: "1.0.0"
status: DRAFT

# === CLASSIFICATION BLOCK ===
goal_level: {GOAL_LEVEL}
goal_symbol: "{GOAL_SYMBOL}"
detail_level: {DETAIL_LEVEL}
scope: "{SCOPE}"
domain: {DOMAIN}

# === ACTORS BLOCK ===
primary_actor: "{PRIMARY_ACTOR}"
supporting_actors:
  - name: "{SUPPORTING_ACTOR_NAME}"
    type: {SUPPORTING_ACTOR_TYPE}
stakeholders:
  - name: "{STAKEHOLDER_NAME}"
    interest: "{STAKEHOLDER_INTEREST}"

# === CONDITIONS BLOCK ===
preconditions:
  - "{PRECONDITION}"
postconditions:
  success:
    - "{SUCCESS_GUARANTEE}"
  failure:
    - "{MINIMUM_GUARANTEE}"
trigger: "{TRIGGER_EVENT}"

# === FLOWS BLOCK ===
basic_flow:
  - step: 1
    actor: "{ACTOR}"
    action: "{ACTION_VERB_OBJECT}"
    type: {STEP_TYPE}
  - step: 2
    actor: "System"
    action: "{SYSTEM_RESPONSE}"
    type: system_response
  - step: 3
    actor: "{ACTOR}"
    action: "{COMPLETION_ACTION}"
    type: actor_action

# === EXTENSIONS BLOCK ===
extensions:
  - id: EXT-{STEP}{LETTER}
    name: "{EXTENSION_NAME}"
    anchor_step: {ANCHOR_STEP}
    condition: "{CONDITION}"
    steps:
      - step: 1
        actor: "System"
        action: "{HANDLING_ACTION}"
        type: system_response
    outcome: "{OUTCOME}"

# === ALTERNATIVE FLOWS BLOCK ===
alternative_flows:
  - id: AF-{NN}
    name: "{ALT_FLOW_NAME}"
    branches_from_step: {BRANCH_STEP}
    condition: "{CONDITION}"
    steps:
      - step: 1
        actor: "{ACTOR}"
        action: "{ALT_ACTION}"
        type: {STEP_TYPE}
    rejoins_at_step: {REJOIN_STEP}

# === SLICE LIFECYCLE BLOCK ===
# Populated by uc-slicer (Activity 2, 4, 5)
# slice_state: {SLICE_STATE}
# slices: []
# slice_ids: []

# === INTERACTIONS BLOCK ===
# Populated by uc-slicer (Activity 5) -- ARCHITECTURALLY SPECULATIVE
# interactions: []

# === TRACEABILITY BLOCK ===
parent_id: null
related_use_cases: []
requirements: []
slice_ids: []

# === METADATA BLOCK ===
priority: {PRIORITY}
created_at: "{ISO_8601_DATETIME}"
created_by: "{AUTHOR}"
realization_level: {REALIZATION_LEVEL}
---

# {TITLE}

> **ID:** UC-{DOMAIN}-{NNN} | **Goal Level:** {GOAL_LEVEL} ({GOAL_SYMBOL}) | **Detail:** {DETAIL_LEVEL}
> **Actor:** {PRIMARY_ACTOR} | **Scope:** {SCOPE}

## Goal

{ONE_SENTENCE_GOAL_DESCRIPTION}

## Context

{SYSTEM_SCOPE_AND_CONTEXT_TWO_TO_THREE_SENTENCES}

## Stakeholders and Interests

| Stakeholder | Interest |
|-------------|---------|
| {STAKEHOLDER_NAME} | {STAKEHOLDER_INTEREST} |

## Preconditions

- {PRECONDITION}

## Main Success Scenario

1. {ACTOR} {ACTION}.
2. System {RESPONSE}.
3. {ACTOR} {COMPLETION_ACTION}.

## Postconditions

**Success guarantees:**
- {SUCCESS_GUARANTEE}

**Minimal guarantees (even on failure):**
- {MINIMUM_GUARANTEE}

## Extensions

**{STEP}a. {CONDITION}:**
1. {HANDLING_STEP}.
2. Use case {OUTCOME}.

## Alternative Flows

### AF-{NN}: {ALT_FLOW_NAME}

At step {BRANCH_STEP}, when {CONDITION}:

1. {ALT_STEP}.
2. Resume at step {REJOIN_STEP} (or: use case ends successfully / use case fails).

## Notes

{ADDITIONAL_CONTEXT_OR_OPEN_QUESTIONS}

---

*Template Version: 1.0.0 | Schema: docs/schemas/use-case-realization-v1.schema.json*
*Instructions: Replace all {PLACEHOLDER} values. Remove commented-out YAML blocks when populating.*
*Progressive realization: For BRIEFLY_DESCRIBED use use-case-brief.template.md; for BULLETED_OUTLINE use use-case-casual.template.md.*
