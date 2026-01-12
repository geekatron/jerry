---
id: wi-sao-032
title: "MEDIUM Priority ps-* Tests"
status: OPEN
parent: "_index.md"
initiative: sao-init-006
children: []
depends_on:
  - wi-sao-029
  - wi-sao-030
blocks: []
created: "2026-01-11"
priority: "P2"
estimated_effort: "12-16h"
entry_id: "sao-032"
token_estimate: 800
---

# WI-SAO-032: MEDIUM Priority ps-* Tests

> **Status:** OPEN
> **Priority:** MEDIUM (P2)
> **Depends On:** WI-SAO-029, WI-SAO-030

---

## Description

Execute 4 MEDIUM priority tests including error handling.

---

## Acceptance Criteria

| AC# | Criterion | Expected | Status |
|-----|-----------|----------|--------|
| AC-032-001 | PS-ORCH-007 passes | PASS | PENDING |
| AC-032-002 | PS-ORCH-008 passes | PASS | PENDING |
| AC-032-003 | PS-NEG-001 fails gracefully | Graceful error | PENDING |
| AC-032-004 | PS-NEG-002 fails gracefully | Graceful error | PENDING |

---

## Tasks

### T-032.1: PS-ORCH-007 Incident Investigation (4h)
- **Status:** PENDING
- **Pattern:** Sequential
- **Agents:** ps-investigator → ps-analyst → ps-reporter
- **Sub-tasks:**
  - [ ] Create mock incident scenario
  - [ ] Execute investigation workflow
  - [ ] Document results

### T-032.2: PS-ORCH-008 Knowledge Bootstrap (4h)
- **Status:** PENDING
- **Pattern:** Mixed
- **Agents:** ps-researcher → ps-synthesizer → ps-architect
- **Sub-tasks:**
  - [ ] Create bootstrap problem
  - [ ] Execute knowledge pipeline
  - [ ] Document results

### T-032.3: PS-NEG-001 Missing Dependency (2h)
- **Status:** PENDING
- **Pattern:** Error Handling
- **Agents:** ps-validator (no input)
- **Sub-tasks:**
  - [ ] Invoke with empty session_context
  - [ ] Validate graceful error handling
  - [ ] Document error behavior

### T-032.4: PS-NEG-002 Invalid Schema (2h)
- **Status:** PENDING
- **Pattern:** Error Handling
- **Agents:** Any ps-* with malformed session_context
- **Sub-tasks:**
  - [ ] Construct malformed session_context
  - [ ] Invoke agent with invalid input
  - [ ] Validate schema validation catches error
  - [ ] Document error handling

---

*Source: Extracted from WORKTRACKER.md lines 2329-2384*
