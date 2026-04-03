---
id: UC-{DOMAIN}-{NNN}
title: "{TITLE}"
work_type: USE_CASE
version: "1.0.0"
status: DRAFT
goal_level: {GOAL_LEVEL}
goal_symbol: "{GOAL_SYMBOL}"
detail_level: BULLETED_OUTLINE
scope: "{SCOPE}"
domain: {DOMAIN}
primary_actor: "{PRIMARY_ACTOR}"
preconditions:
  - "{PRECONDITION}"
postconditions:
  success:
    - "{SUCCESS_GUARANTEE}"
  failure:
    - "{MINIMUM_GUARANTEE}"
trigger: "{TRIGGER_EVENT}"
basic_flow:
  - step: 1
    actor: "{ACTOR}"
    action: "{ACTION}"
    type: {STEP_TYPE}
  - step: 2
    actor: "System"
    action: "{SYSTEM_RESPONSE}"
    type: system_response
  - step: 3
    actor: "{ACTOR}"
    action: "{ACTION}"
    type: {STEP_TYPE}
  # ... 3-9 steps total
created_at: "{ISO_8601_DATETIME}"
created_by: "{AUTHOR}"
---

# {TITLE}

**Primary Actor:** {PRIMARY_ACTOR}
**Goal Level:** {GOAL_LEVEL} ({GOAL_SYMBOL})
**Trigger:** {TRIGGER_EVENT}

## Main Success Scenario

1. {ACTOR} {ACTION}.
2. System {RESPONSE}.
3. {ACTOR} {COMPLETION_ACTION}.

## Possible Extensions

- At step {N}: {CONDITION} (not yet elaborated)
- At step {M}: {CONDITION} (not yet elaborated)

---

*Template: use-case-casual.template.md v1.0.0 | Detail level: BULLETED_OUTLINE*
*Next step: Use uc-author to elaborate to ESSENTIAL_OUTLINE (Steps 7-10) -- required for /test-spec and /contract-design.*
