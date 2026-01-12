---
id: wi-sao-031
title: "Cross-Family Interoperability Tests"
status: OPEN
parent: "_index.md"
initiative: sao-init-006
children: []
depends_on:
  - wi-sao-029
blocks: []
created: "2026-01-11"
priority: "P1"
estimated_effort: "8-12h"
entry_id: "sao-031"
token_estimate: 900
---

# WI-SAO-031: Cross-Family Interoperability Tests

> **Status:** OPEN
> **Priority:** HIGH (P1)
> **Depends On:** WI-SAO-029 (establish ps-* baseline first)

---

## Description

Validate that ps-* and nse-* agents can interoperate using shared session_context schema.

---

## Rationale

Gap analysis identified this as untested territory:
> "Session context schema compatibility suggests YES, but no evidence exists."

---

## Acceptance Criteria

| AC# | Criterion | Expected | Status |
|-----|-----------|----------|--------|
| AC-031-001 | CROSS-ORCH-001 passes | PASS | PENDING |
| AC-031-002 | CROSS-ORCH-002 passes | PASS | PENDING |
| AC-031-003 | Schema compatible across families | No validation errors | PENDING |

---

## Tasks

### T-031.1: CROSS-ORCH-001 Cross-Family Handoff (4h)
- **Status:** PENDING
- **Pattern:** Sequential Cross-Family
- **Agents:** ps-researcher → nse-requirements
- **Sub-tasks:**
  - [ ] Invoke ps-researcher to research NASA SE topic
  - [ ] Construct cross-family session_context
  - [ ] Invoke nse-requirements with ps-researcher output
  - [ ] Validate successful consumption
  - [ ] Check schema compliance

### T-031.2: CROSS-ORCH-002 Mixed Fan-In (4h)
- **Status:** PENDING
- **Pattern:** Fan-In Mixed Family
- **Agents:** ps-analyst + nse-risk → ps-reporter
- **Sub-tasks:**
  - [ ] Invoke ps-analyst with problem
  - [ ] Invoke nse-risk with same problem (parallel)
  - [ ] Construct mixed-family session_context
  - [ ] Invoke ps-reporter to synthesize
  - [ ] Validate cross-family references

---

*Source: Extracted from WORKTRACKER.md lines 2279-2326*
