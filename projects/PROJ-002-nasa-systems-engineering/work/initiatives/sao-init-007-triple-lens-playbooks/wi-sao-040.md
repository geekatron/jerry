---
id: wi-sao-040
title: "Validate session context schema v1.0.0"
status: OPEN
parent: "_index.md"
initiative: sao-init-007
children: []
depends_on: []
blocks: []
created: "2026-01-12"
last_updated: "2026-01-12"
priority: P3
estimated_effort: "1h"
entry_id: sao-040
token_estimate: 350
---

# WI-SAO-040: Validate session context schema v1.0.0

> **Status:** 📋 OPEN
> **Priority:** P3 (LOW)

---

## Description

Validate that the session context schema v1.0.0 documented in DISCOVERY-009 is correctly implemented across all agents and matches the formalized structure.

---

## Schema to Validate

```yaml
session_context:
  version: "1.0.0"
  session_id: "uuid-v4"
  source_agent: "agent-name"
  target_agent: "agent-name"
  handoff_timestamp: "ISO-8601"
  state_output_key: "key_name"
  cognitive_mode: "convergent|divergent"
  payload:
    findings: [ ... ]
    confidence: 0.0-1.0
    next_hint: "suggested_next_agent"
```

---

## Acceptance Criteria

1. [ ] Schema matches implementation in ps-* agents
2. [ ] Schema matches implementation in nse-* agents
3. [ ] state_output_key mapping is accurate for all 19 agents
4. [ ] Cross-skill handoffs validated

---

## Tasks

- [ ] **T-040.1:** Review ps-* agent schema usage
- [ ] **T-040.2:** Review nse-* agent schema usage
- [ ] **T-040.3:** Verify state_output_key mapping accuracy
- [ ] **T-040.4:** Document any discrepancies

---

## Verification

| Evidence ID | Type | Description | Status |
|-------------|------|-------------|--------|
| E-040-001 | Validation | ps-* agents use schema correctly | ⏳ |
| E-040-002 | Validation | nse-* agents use schema correctly | ⏳ |

---

*Source: DISCOVERY-009 in discoveries.md*
