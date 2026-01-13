# PS-NEG-002: Invalid Schema Test - Validation Report

**Test ID:** PS-NEG-002
**Agent:** ps-analyst (v2.1.0)
**Test Type:** NEGATIVE TEST
**Execution Date:** 2026-01-12
**Status:** VALIDATION FAILED (Expected)

---

## Test Purpose

This negative test verifies that the ps-analyst agent properly validates incoming session_context and gracefully rejects malformed input according to WI-SAO-002 schema validation requirements.

---

## Received Context (Malformed Input)

```yaml
session_context:
  schema_version: "9.9.9"
  session_id: "not-a-uuid"
  source_agent:
    id: "unknown-agent"
  target_agent:
    id: "ps-wrong-target"
  payload:
    random_field: "unexpected data"
```

---

## Validation Analysis

### Schema Violations Identified

The following violations were detected in the malformed session_context:

| # | Field | Issue | Severity | Required Fix |
|---|-------|-------|----------|--------------|
| 1 | `schema_version` | Value `"9.9.9"` not supported | **CRITICAL** | Must be `"1.0.0"` |
| 2 | `session_id` | `"not-a-uuid"` invalid format | **CRITICAL** | Must be valid UUID v4 format |
| 3 | `source_agent.id` | `"unknown-agent"` not registered | **CRITICAL** | Must be known agent (e.g., "orchestrator") |
| 4 | `target_agent.id` | `"ps-wrong-target"` mismatch | **CRITICAL** | Must be `"ps-analyst"` for this agent |
| 5 | `payload.key_findings` | Missing required field | **CRITICAL** | Array of finding objects required |
| 6 | `payload.confidence` | Missing required field | **CRITICAL** | Number (0-100) required |
| 7 | `timestamp` | Missing required field | **CRITICAL** | ISO 8601 timestamp required |

---

## Required Schema Definition

Valid session_context MUST conform to this schema:

```yaml
session_context:
  # Schema version (immutable for this agent)
  schema_version: "1.0.0"

  # Session identifier (UUID v4)
  session_id: "550e8400-e29b-41d4-a716-446655440000"

  # Source agent identification
  source_agent:
    id: "orchestrator"  # Known agent name
    version: "1.0.0"

  # Target agent identification (must be ps-analyst)
  target_agent:
    id: "ps-analyst"
    version: "2.1.0"

  # Analysis payload (required fields)
  payload:
    # Array of findings to analyze
    key_findings:
      - id: "finding-001"
        description: "System observation or issue"
        impact: "high" | "medium" | "low"
        evidence: "supporting data"

    # Confidence level in analysis (0-100)
    confidence: 85

    # Optional context
    analysis_context:
      project_id: "PROJ-002"
      scope: "nasa-systems-engineering"
      focus_areas: ["architecture", "integration"]

    # Optional history
    prior_analyses: []

  # Execution timestamp (ISO 8601)
  timestamp: "2026-01-12T00:00:00Z"

  # Originating workflow (optional)
  orchestration_id: "orch-workflow-001"
```

---

## Validation Failure Details

### Detailed Error Messages

#### Error 1: Unsupported Schema Version
```
FIELD:      schema_version
RECEIVED:   "9.9.9"
EXPECTED:   "1.0.0"
MESSAGE:    Schema version 9.9.9 is not supported by ps-analyst v2.1.0
            (expected version 1.0.0)
ACTION:     Update schema_version to "1.0.0"
```

#### Error 2: Invalid Session ID Format
```
FIELD:      session_id
RECEIVED:   "not-a-uuid"
EXPECTED:   UUID v4 format (xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx)
MESSAGE:    Session ID must be a valid UUID v4
EXAMPLE:    "550e8400-e29b-41d4-a716-446655440000"
ACTION:     Generate valid UUID v4 for session_id
```

#### Error 3: Unknown Source Agent
```
FIELD:      source_agent.id
RECEIVED:   "unknown-agent"
EXPECTED:   One of: ["orchestrator", "conductor", "qa-engineer"]
MESSAGE:    Source agent "unknown-agent" is not recognized
ACTION:     Use a known agent ID as source_agent.id
```

#### Error 4: Target Agent Mismatch
```
FIELD:      target_agent.id
RECEIVED:   "ps-wrong-target"
EXPECTED:   "ps-analyst"
MESSAGE:    Target agent must be "ps-analyst" for session_context to be accepted
            (received "ps-wrong-target")
ACTION:     Ensure target_agent.id is "ps-analyst"
```

#### Error 5: Missing Required Payload Field
```
FIELD:      payload.key_findings
RECEIVED:   (missing)
EXPECTED:   Array of finding objects with: id, description, impact, evidence
MESSAGE:    payload.key_findings is required for analysis operations
ACTION:     Provide at least one finding object in payload.key_findings array
```

#### Error 6: Missing Required Payload Field
```
FIELD:      payload.confidence
RECEIVED:   (missing)
EXPECTED:   Number between 0 and 100
MESSAGE:    payload.confidence is required to assess analysis certainty
ACTION:     Provide confidence level (0-100) in payload.confidence
```

#### Error 7: Missing Required Timestamp
```
FIELD:      timestamp
RECEIVED:   (missing)
EXPECTED:   ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)
MESSAGE:    timestamp is required for audit trail and ordering
ACTION:     Add ISO 8601 timestamp to session_context root
```

---

## Recovery Path: Correcting the Schema

### Step 1: Fix Schema Version
Change `schema_version` to supported version:
```yaml
schema_version: "1.0.0"
```

### Step 2: Generate Valid Session ID
Create UUID v4 for session tracking:
```bash
python -c "import uuid; print(uuid.uuid4())"
# Output: 550e8400-e29b-41d4-a716-446655440000
```

### Step 3: Set Valid Agent References
Use known agents and match target to receiving agent:
```yaml
source_agent:
  id: "orchestrator"  # Known sender
target_agent:
  id: "ps-analyst"    # Receiving agent
```

### Step 4: Provide Required Payload Fields
Include at least one finding with confidence:
```yaml
payload:
  key_findings:
    - id: "finding-001"
      description: "Architecture review needed"
      impact: "high"
      evidence: "Review identified potential coupling issues"
  confidence: 75
```

### Step 5: Add Timestamp
Include ISO 8601 timestamp:
```yaml
timestamp: "2026-01-12T14:30:00Z"
```

### Complete Valid Example
```yaml
session_context:
  schema_version: "1.0.0"
  session_id: "550e8400-e29b-41d4-a716-446655440000"
  source_agent:
    id: "orchestrator"
    version: "1.0.0"
  target_agent:
    id: "ps-analyst"
    version: "2.1.0"
  payload:
    key_findings:
      - id: "finding-001"
        description: "System design requires review"
        impact: "high"
        evidence: "Initial assessment indicates potential issues"
    confidence: 75
    analysis_context:
      project_id: "PROJ-002"
  timestamp: "2026-01-12T14:30:00Z"
```

---

## Agent Response: Validation Rejection

As per WI-SAO-002 requirements, the ps-analyst agent **REJECTS** this invalid session_context and does NOT proceed with analysis.

```yaml
session_context:
  schema_version: "1.0.0"
  session_id: "ps-neg-002-test-550e8400-e29b-41d4-a716-446655440001"
  source_agent: "ps-analyst"
  target_agent: "orchestrator"
  payload:
    validation_status: "FAILED"
    error: true
    error_type: "SCHEMA_VALIDATION_FAILED"
    error_severity: "CRITICAL"
    validation_errors:
      - field: "schema_version"
        received: "9.9.9"
        expected: "1.0.0"
        message: "Unsupported schema version"
      - field: "session_id"
        received: "not-a-uuid"
        expected: "UUID v4 format"
        message: "Invalid session ID format"
      - field: "source_agent.id"
        received: "unknown-agent"
        expected: "Known agent name"
        message: "Unknown source agent"
      - field: "target_agent.id"
        received: "ps-wrong-target"
        expected: "ps-analyst"
        message: "Target agent mismatch"
      - field: "payload.key_findings"
        received: null
        expected: "Array of finding objects"
        message: "Required field missing"
      - field: "payload.confidence"
        received: null
        expected: "Number 0-100"
        message: "Required field missing"
      - field: "timestamp"
        received: null
        expected: "ISO 8601 timestamp"
        message: "Required field missing"
    total_errors: 7
    error_count_critical: 7
    error_count_warning: 0
    recovery_action: "Provide valid session_context conforming to schema v1.0.0"
    recovery_instructions:
      - "Use schema_version 1.0.0"
      - "Generate valid UUID v4 for session_id"
      - "Set source_agent.id to known agent"
      - "Set target_agent.id to ps-analyst"
      - "Include required payload.key_findings array"
      - "Include required payload.confidence number"
      - "Include ISO 8601 timestamp"
    next_steps:
      - "Fix identified schema violations"
      - "Resubmit session_context with valid schema"
      - "ps-analyst will resume analysis processing"
  timestamp: "2026-01-12T14:30:00Z"
  orchestration_id: "ps-neg-002-test"
```

---

## Test Validation Summary

| Requirement | Status | Evidence |
|------------|--------|----------|
| Schema validation performed | ✅ PASS | All 7 violations identified |
| Invalid context rejected | ✅ PASS | Analysis not executed |
| Errors documented | ✅ PASS | Detailed error messages provided |
| Recovery path provided | ✅ PASS | Correction steps documented |
| Session_context in response | ✅ PASS | Validation failure response included |

---

## Compliance with WI-SAO-002

This test validates that ps-analyst implements WI-SAO-002 requirements:

- ✅ **Validation:** Incoming session_context validated against schema
- ✅ **Identification:** All schema violations identified with specificity
- ✅ **Rejection:** Invalid input rejected before processing
- ✅ **Documentation:** Violations documented with recovery path
- ✅ **No Execution:** Analysis NOT performed on invalid context

---

## References

- **Requirement:** WI-SAO-002 - Session Context Schema Validation
- **Agent:** ps-analyst v2.1.0
- **Test Type:** Negative Test (Invalid Schema)
- **Execution:** 2026-01-12

---

**Test Status: PASSED (Expected Validation Failure Occurred)**
