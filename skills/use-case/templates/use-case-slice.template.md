---
slice_id: UC-{DOMAIN}-{NNN}-S{N}
parent_use_case: UC-{DOMAIN}-{NNN}
title: "{SLICE_TITLE}"
slice_state: {SLICE_STATE}
realization_level: {REALIZATION_LEVEL}
steps_included:
  - flow: basic_flow
    steps: [{STEP_NUMBERS}]
  - flow: "{ALT_OR_EXT_ID}"
    steps: [{STEP_NUMBERS}]
invest_assessment:
  independent: {BOOL}
  negotiable: {BOOL}
  valuable: {BOOL}
  estimable: {BOOL}
  small: {BOOL}
  testable: {BOOL}
test_cases:
  - "{TEST_CASE_DESCRIPTION}"
---

# Slice: {SLICE_TITLE}

**Parent Use Case:** [{PARENT_TITLE}](../UC-{DOMAIN}-{NNN}-{slug}.md)
**Slice ID:** UC-{DOMAIN}-{NNN}-S{N}
**State:** {SLICE_STATE}
**INVEST:** {PASS_FAIL_SUMMARY}

## Included Steps

| Flow | Steps |
|------|-------|
| basic_flow | {STEP_NUMBERS} |
| {ALT_OR_EXT_ID} | {STEP_NUMBERS} |

## INVEST Assessment

| Criterion | Pass? | Notes |
|-----------|-------|-------|
| Independent | {BOOL} | {NOTES} |
| Negotiable | {BOOL} | {NOTES} |
| Valuable | {BOOL} | {NOTES} |
| Estimable | {BOOL} | {NOTES} |
| Small | {BOOL} | {NOTES} |
| Testable | {BOOL} | {NOTES} |

## Test Cases

1. {TEST_CASE_1}
2. {TEST_CASE_2}

## Realization (Activity 5)

> Only present at ANALYZED state (slice_state = ANALYZED, realization_level = INTERACTION_DEFINED).

{INTERACTION_SEQUENCE_NARRATIVE}

---

*Template: use-case-slice.template.md v1.0.0 | UC 2.0 Activity 2/4/5*
*Lifecycle: SCOPED -> PREPARED (add test_cases) -> ANALYZED (add interactions) -> IMPLEMENTED -> VERIFIED*
*Synchronization: This file is a copy of the slice entry in the parent use case artifact. Keep in sync.*
