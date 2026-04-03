---
source_use_case: UC-{DOMAIN}-{NNN}
source_title: "{USE_CASE_TITLE}"
source_detail_level: {DETAIL_LEVEL}
source_goal_level: {GOAL_LEVEL}
generated_by: tspec-generator
generated_at: "{ISO_8601_DATETIME}"
scenario_count: {TOTAL_SCENARIO_COUNT}
coverage:
  basic_flow_mapped: true
  alternative_flows_mapped: {ALT_FLOW_COUNT}
  extensions_mapped: {EXT_COUNT}
  total_flows: {TOTAL_FLOW_COUNT}
  mapped_flows: {MAPPED_FLOW_COUNT}
slice_id: null  # Populated when slice-scoped generation (RULE-SL-01)
version: "1.0.0"
---

# Feature: {USE_CASE_TITLE}

> As a {PRIMARY_ACTOR}, I want to {GOAL_VERB_PHRASE} so that {BENEFIT_STATEMENT}.

---

## Happy Path

### Scenario: {USE_CASE_TITLE} - Main Success Scenario

**Source:** basic_flow (steps 1-{N})

```gherkin
Given {PRECONDITION_1}
  And {PRECONDITION_2}
When {PRIMARY_ACTOR} {ACTOR_ACTION_STEP_1}
  And the system {SYSTEM_RESPONSE_STEP_2}
  And {PRIMARY_ACTOR} {ACTOR_ACTION_STEP_3}
  And the system verifies that {VALIDATION_STEP_4}
Then {POSTCONDITION_SUCCESS_1}
  And {POSTCONDITION_SUCCESS_2}
```

---

## Alternative Flows

### Scenario: {USE_CASE_TITLE} - {ALT_FLOW_NAME}

**Source:** AF-{NN} (branches_from_step: {N}, condition: "{ALT_CONDITION}")

```gherkin
Given {PRECONDITIONS}
  And {ALT_FLOW_CONDITION}
When {PRIMARY_ACTOR} {ALT_FLOW_ACTION}
  And the system {ALT_FLOW_SYSTEM_RESPONSE}
Then {ALT_FLOW_OUTCOME}
```

---

## Error Scenarios

### Scenario: {USE_CASE_TITLE} - {EXTENSION_NAME}

**Source:** EXT-{STEP}{LETTER} (anchor_step: {N}, outcome: failure)

```gherkin
Given {PRECONDITIONS}
  And {EXTENSION_CONDITION}
When {PRIMARY_ACTOR} {ACTION_AT_ANCHOR_STEP}
Then the system rejects the request
  And {FAILURE_POSTCONDITION}
  And the system notifies {PRIMARY_ACTOR} of the error
```

### Scenario: {USE_CASE_TITLE} - {EXTENSION_REJOIN_NAME}

**Source:** EXT-{STEP}{LETTER} (anchor_step: {N}, outcome: rejoin:{REJOIN_STEP})

```gherkin
Given {PRECONDITIONS}
  And {EXTENSION_CONDITION}
When {PRIMARY_ACTOR} {RECOVERY_ACTION}
  And the system {RECOVERY_SYSTEM_RESPONSE}
Then the use case rejoins at step {REJOIN_STEP} of the main flow
  And the system {STEP_N_SYSTEM_RESPONSE}
  And {POSTCONDITION_SUCCESS}
```

---

## Traceability Matrix

| Scenario | Source Flow | Source Step | Type |
|----------|-------------|-------------|------|
| {USE_CASE_TITLE} - Main Success Scenario | basic_flow | 1-{N} | happy_path |
| {USE_CASE_TITLE} - {ALT_FLOW_NAME} | AF-{NN} | {BRANCH_STEP} | alternative |
| {USE_CASE_TITLE} - {EXTENSION_NAME} | EXT-{STEP}{LETTER} | {ANCHOR_STEP} | error (failure) |
| {USE_CASE_TITLE} - {EXTENSION_REJOIN_NAME} | EXT-{STEP}{LETTER} | {ANCHOR_STEP} | error (rejoin:{N}) |

---

## Template Usage Notes

**Placeholders to replace (all `{UPPERCASE}` tokens):**

| Placeholder | Source Field | Notes |
|-------------|-------------|-------|
| `{DOMAIN}` | `$.domain` | Uppercase domain code (e.g., AUTH, LIB) |
| `{NNN}` | `$.id` suffix | 3-digit zero-padded number |
| `{USE_CASE_TITLE}` | `$.title` | Verbatim use case title |
| `{DETAIL_LEVEL}` | `$.detail_level` | Must be ESSENTIAL_OUTLINE or FULLY_DESCRIBED |
| `{GOAL_LEVEL}` | `$.goal_level` | USER_GOAL, SUMMARY, or SUBFUNCTION |
| `{PRIMARY_ACTOR}` | `$.primary_actor` | The actor whose goal this UC satisfies |
| `{PRECONDITION_N}` | `$.preconditions[N]` | One Given clause per precondition |
| `{ACTOR_ACTION_STEP_N}` | `$.basic_flow[N]` where type=actor_action | When clause from actor_action step |
| `{SYSTEM_RESPONSE_STEP_N}` | `$.basic_flow[N]` where type=system_response | Then clause from system_response step |
| `{VALIDATION_STEP_N}` | `$.basic_flow[N]` where type=validation | Then assertion from validation step |
| `{POSTCONDITION_SUCCESS_N}` | `$.postconditions.success[N]` | Final Then clause |
| `{ALT_FLOW_NAME}` | `$.alternative_flows[N].name` | Alternative flow identifier |
| `{ALT_CONDITION}` | `$.alternative_flows[N].condition` | Branching condition text |
| `{EXTENSION_NAME}` | `$.extensions[N].name` | Extension identifier |
| `{EXTENSION_CONDITION}` | `$.extensions[N].condition` | Extension trigger condition |

**Sections to include/exclude:**
- Include "Alternative Flows" section only if `$.alternative_flows` is non-empty
- Include "Error Scenarios" section only if `$.extensions` is non-empty
- Repeat scenario blocks within each section for each flow element
- Slice-scoped generation: set `slice_id` in frontmatter; scope flow elements to `$.slices[slice_id].steps_included`

*Template Version: 1.0.0 | Design decisions: TD-01 (YAML frontmatter), TD-02 (scenario grouping), TD-03 (Source citations), TD-04 (Traceability Matrix), TD-05 (.feature.md extension)*
