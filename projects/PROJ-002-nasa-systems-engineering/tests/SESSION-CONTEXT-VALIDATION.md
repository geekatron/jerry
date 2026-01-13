# Session Context Validation Test Suite

> **Document ID:** PROJ-002-SCV-001
> **Date:** 2026-01-11
> **Status:** DEFINED - Pending Execution
> **Method:** Schema Validation Testing
> **Work Item:** WI-SAO-002

---

## Executive Summary

**Target: 24 tests across 4 categories**

This test suite validates the session_context schema implementation per WI-SAO-002.
Tests verify that agent handoffs conform to `docs/schemas/session_context.json`.

---

## Test Categories

| Category | Tests | Description |
|----------|-------|-------------|
| Input Validation (IV) | 8 | On Receive validation rules |
| Output Validation (OV) | 6 | On Send validation rules |
| Cross-Skill Handoff (CS) | 5 | ps ↔ nse handoff validation |
| Error Handling (EH) | 5 | Validation failure behavior |
| **TOTAL** | **24** | |

---

## Detailed Test Cases

### Input Validation Tests (IV)

#### IV-001: Valid Session Context Accepted
- **Objective:** Verify that a fully valid session_context passes validation
- **Input:**
  ```yaml
  session_context:
    schema_version: "1.0.0"
    session_id: "sess-2026-01-11-test001"
    source_agent:
      id: "ps-researcher"
      family: "ps"
    target_agent:
      id: "nse-requirements"
      family: "nse"
    payload:
      key_findings:
        - id: "F-001"
          summary: "Test finding"
      confidence:
        overall: 0.85
    timestamp: "2026-01-11T12:00:00Z"
  ```
- **Expected:** Validation PASS, processing continues
- **Status:** [ ] PENDING

#### IV-002: Missing schema_version Rejected
- **Objective:** Verify missing required field is rejected
- **Input:** session_context without schema_version field
- **Expected:** Validation FAIL with "Invalid handoff: missing schema_version"
- **Status:** [ ] PENDING

#### IV-003: Invalid schema_version Warning
- **Objective:** Verify unknown schema version triggers warning but continues
- **Input:** schema_version: "2.0.0" (future version)
- **Expected:** Validation WARN "Potential schema mismatch", processing continues
- **Status:** [ ] PENDING

#### IV-004: Missing session_id Rejected
- **Objective:** Verify missing session_id is rejected
- **Input:** session_context without session_id field
- **Expected:** Validation FAIL with "Invalid handoff: missing session_id"
- **Status:** [ ] PENDING

#### IV-005: Session Mismatch Prompts User (FIX-NEG-008)
- **Objective:** Verify different session_id triggers user prompt
- **Input:** session_id from a previous session
- **Expected:** Validation WARN "State from different session" + user prompt
- **Status:** [ ] PENDING

#### IV-006: Invalid Source Agent ID Rejected
- **Objective:** Verify malformed agent ID is rejected
- **Input:** source_agent.id: "invalid-agent-format"
- **Expected:** Validation FAIL "Invalid source agent ID format"
- **Status:** [ ] PENDING

#### IV-007: Valid Agent ID Pattern Accepted
- **Objective:** Verify all valid agent ID patterns work
- **Input:** Test with ps-*, nse-*, orch-* patterns
- **Expected:** Validation PASS for all valid patterns
- **Status:** [ ] PENDING

#### IV-008: Malformed Payload Rejected
- **Objective:** Verify payload structure violations are rejected
- **Input:** payload.key_findings as string instead of array
- **Expected:** Validation FAIL "Malformed payload"
- **Status:** [ ] PENDING

---

### Output Validation Tests (OV)

#### OV-001: Key Findings Populated
- **Objective:** Verify source agent populates key_findings
- **Validation:** key_findings array has at least one finding with summary
- **Expected:** Validation PASS when findings present
- **Status:** [ ] PENDING

#### OV-002: Confidence Score Valid Range
- **Objective:** Verify confidence.overall is between 0.0 and 1.0
- **Input:** confidence.overall values: 0.0, 0.5, 1.0 (valid), 1.5, -0.1 (invalid)
- **Expected:** PASS for 0.0-1.0, FAIL for out-of-range
- **Status:** [ ] PENDING

#### OV-003: Artifacts Include File Paths (P-002)
- **Objective:** Verify artifacts array references created files
- **Validation:** Each artifact has path field with valid path
- **Expected:** Validation PASS when artifacts present for persisted output
- **Status:** [ ] PENDING

#### OV-004: Timestamp Is ISO-8601
- **Objective:** Verify timestamp format is valid ISO-8601
- **Input:** "2026-01-11T12:00:00Z" (valid), "Jan 11, 2026" (invalid)
- **Expected:** PASS for ISO-8601, FAIL for other formats
- **Status:** [ ] PENDING

#### OV-005: Target Agent Matches Expectation
- **Objective:** Verify target_agent.id matches expected downstream agent
- **Validation:** target_agent.id follows agent ID pattern
- **Expected:** Validation PASS when target is valid agent
- **Status:** [ ] PENDING

#### OV-006: Traceability Included for NSE (P-040)
- **Objective:** Verify nse-* agents include traceability links
- **Validation:** finding.traceability references REQ-*, RISK-*, TSR-*, ICD-*
- **Expected:** Validation WARN if traceability missing, PASS if present
- **Status:** [ ] PENDING

---

### Cross-Skill Handoff Tests (CS)

#### CS-001: ps → nse Handoff Valid
- **Objective:** Verify Problem-Solving to NASA SE handoff works
- **Input:**
  ```yaml
  source_agent:
    id: "ps-researcher"
    family: "ps"
  target_agent:
    id: "nse-requirements"
    family: "nse"
  ```
- **Expected:** Validation PASS, cross-skill noted in logs
- **Status:** [ ] PENDING

#### CS-002: nse → ps Handoff Valid
- **Objective:** Verify NASA SE to Problem-Solving handoff works
- **Input:**
  ```yaml
  source_agent:
    id: "nse-requirements"
    family: "nse"
  target_agent:
    id: "ps-analyst"
    family: "ps"
  ```
- **Expected:** Validation PASS, cross-skill noted in logs
- **Status:** [ ] PENDING

#### CS-003: Cognitive Mode Mismatch Logged
- **Objective:** Verify divergent → convergent handoff is logged
- **Input:** source divergent, target convergent
- **Expected:** Validation PASS with info log about mode translation
- **Status:** [ ] PENDING

#### CS-004: Lifecycle Context Preserved
- **Objective:** Verify SE lifecycle context passes to ps-* agents
- **Input:** payload.context.se_lifecycle_phase: "Phase B"
- **Expected:** Context available in target agent
- **Status:** [ ] PENDING

#### CS-005: Traceability Format Cross-Skill
- **Objective:** Verify nse traceability format understood by ps agents
- **Input:** traceability: ["REQ-SYS-042", "TSR-001"]
- **Expected:** ps-* agents can read NASA SE traceability IDs
- **Status:** [ ] PENDING

---

### Error Handling Tests (EH)

#### EH-001: Critical Rejection Halts Workflow
- **Objective:** Verify CRITICAL errors stop workflow execution
- **Trigger:** Missing required field (schema_version, session_id)
- **Expected:** Orchestrator alerted, workflow halted, user notified
- **Status:** [ ] PENDING

#### EH-002: Warning Logged But Continues
- **Objective:** Verify WARNING errors are logged but processing continues
- **Trigger:** Unknown schema_version, missing traceability
- **Expected:** Warning logged, workflow continues
- **Status:** [ ] PENDING

#### EH-003: Retry Requested on Malformed Payload
- **Objective:** Verify malformed payload triggers retry request
- **Trigger:** payload.key_findings is not an array
- **Expected:** Orchestrator requests source agent to retry
- **Status:** [ ] PENDING

#### EH-004: Session Mismatch Safe Default
- **Objective:** Verify timeout on session mismatch defaults to fresh start
- **Trigger:** Session mismatch + 30s user timeout
- **Expected:** Old state backed up, fresh session started
- **Status:** [ ] PENDING

#### EH-005: Validation Error Context Preserved
- **Objective:** Verify validation errors include diagnostic context
- **Trigger:** Any validation failure
- **Expected:** Error includes: field name, expected value, actual value, agent ID
- **Status:** [ ] PENDING

---

## Test Execution Procedure

### Prerequisites
1. All 16 agents have session_context sections (T-002.1, T-002.2 complete)
2. Both ORCHESTRATION.md files have Session Context Validation sections (T-002.3 complete)
3. Schema at `docs/schemas/session_context.json` is accessible

### Execution Steps
1. For each test case:
   - Prepare input matching test specification
   - Invoke agent or orchestrator with input
   - Capture validation output
   - Verify expected behavior
   - Record result (PASS/FAIL/SKIP)
2. Document evidence for each test
3. Update status in this file
4. Report aggregate results to WORKTRACKER

### Evidence Requirements
- Each test requires documented evidence of execution
- Screenshots or log excerpts for validation messages
- File paths for any artifacts created during testing

---

## Traceability

| Test ID | Schema Field | Agent Sections | Work Item |
|---------|-------------|----------------|-----------|
| IV-001 to IV-008 | All required fields | On Receive | WI-SAO-002 |
| OV-001 to OV-006 | All output fields | On Send | WI-SAO-002 |
| CS-001 to CS-005 | source_agent, target_agent, family | Cross-Skill Handoff | WI-SAO-002 |
| EH-001 to EH-005 | Error handling | Validation Error Handling | WI-SAO-002 |

---

## References

1. **Schema:** `docs/schemas/session_context.json`
2. **PS ORCHESTRATION.md:** `skills/problem-solving/docs/ORCHESTRATION.md` (Session Context Validation section)
3. **NSE ORCHESTRATION.md:** `skills/nasa-se/docs/ORCHESTRATION.md` (Session Context Validation section)
4. **FIX-NEG-008:** Session mismatch handling from Gap Fix Backlog
5. **P-040:** Traceability requirement from Jerry Constitution

---

*Document Version: 1.0.0*
*Created: 2026-01-11*
*Work Item: WI-SAO-002 (T-002.4)*
