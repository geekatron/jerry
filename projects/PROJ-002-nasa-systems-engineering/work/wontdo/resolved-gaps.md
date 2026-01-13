---
id: archive-resolved-gaps
title: "Resolved Gaps from Negative Testing (NEG-GAP-* and FIX-NEG-*)"
type: archive
status: RESOLVED
parent: "../WORKTRACKER.md"
related_work_items: []
created: "2026-01-09"
last_updated: "2026-01-09"
token_estimate: 3200
---

# Resolved Gaps from Negative Testing (Archived)

This archive contains all NEG-GAP-* gaps identified during negative testing and their corresponding FIX-NEG-* resolution work items. All items are RESOLVED.

---

## Gap Summary

| Gap ID | Severity | Agent | Status |
|--------|----------|-------|--------|
| NEG-GAP-001 | LOW | nse-requirements | ✅ RESOLVED |
| NEG-GAP-002 | LOW | nse-requirements | ✅ RESOLVED |
| NEG-GAP-003 | MEDIUM | nse-reviewer | ✅ RESOLVED |
| NEG-GAP-004 | LOW | nse-integration | ✅ RESOLVED |
| NEG-GAP-005 | MEDIUM | nse-verification, nse-risk | ✅ RESOLVED |
| NEG-GAP-006 | LOW | nse-requirements | ✅ RESOLVED |
| NEG-GAP-007 | LOW | nse-integration | ✅ RESOLVED |
| NEG-GAP-008 | MEDIUM | Orchestration state | ✅ RESOLVED |

---

## NEG-GAP-001: Empty Input Handling (LOW)

- **Status:** RESOLVED
- **Affected:** nse-requirements
- **Test:** TEST-NEG-001
- **Fix:** Added `min_requirements: 1` validation with guidance
- **Evidence:** `skills/nasa-se/agents/nse-requirements.md` lines 66-75

---

## NEG-GAP-002: Maximum Limit Guidance (LOW)

- **Status:** RESOLVED
- **Affected:** nse-requirements
- **Test:** TEST-NEG-003, 004
- **Fix:** Added `max_recommended: 100` with warning and suggestions
- **Evidence:** `skills/nasa-se/agents/nse-requirements.md` lines 77-85

---

## NEG-GAP-003: Review Gate Enum Validation (MEDIUM)

- **Status:** RESOLVED
- **Affected:** nse-reviewer
- **Test:** TEST-NEG-010
- **Fix:** Added `review_type_enum` with Levenshtein distance typo detection
- **Evidence:** `skills/nasa-se/agents/nse-reviewer.md` lines 60-70

---

## NEG-GAP-004: TSR Soft Dependency Enforcement (LOW)

- **Status:** RESOLVED
- **Affected:** nse-integration
- **Test:** TEST-NEG-014
- **Fix:** Added `soft_prerequisites.architecture_tsr` with warning and options
- **Evidence:** `skills/nasa-se/agents/nse-integration.md` lines 65-82

---

## NEG-GAP-005: Cross-Reference Validation (MEDIUM)

- **Status:** RESOLVED
- **Affected:** nse-verification, nse-risk
- **Test:** TEST-NEG-016, 017
- **Fix:** Added `cross_reference_validation` with orphan/stale detection
- **Evidence:** `skills/nasa-se/agents/nse-verification.md` lines 65-87, `nse-risk.md` lines 65-80

---

## NEG-GAP-006: Circular Dependency Detection (LOW)

- **Status:** RESOLVED
- **Affected:** nse-requirements
- **Test:** TEST-NEG-018
- **Fix:** Added `dependency_validation.circular_dependency_check` with DFS algorithm
- **Evidence:** `skills/nasa-se/agents/nse-requirements.md` lines 86-94

---

## NEG-GAP-007: Interface System Validation (LOW)

- **Status:** RESOLVED
- **Affected:** nse-integration
- **Test:** TEST-NEG-019
- **Fix:** Added `system_validation.validate_systems_in_tsr` with external system support
- **Evidence:** `skills/nasa-se/agents/nse-integration.md` lines 83-98

---

## NEG-GAP-008: Session Mismatch Handling (MEDIUM)

- **Status:** RESOLVED
- **Affected:** Orchestration state
- **Test:** TEST-NEG-021
- **Fix:** Added `Session Validation (FIX-NEG-008)` section with safe defaults
- **Evidence:** `skills/nasa-se/docs/ORCHESTRATION.md` lines 436-494

---

# Gap Fix Work Items

---

## FIX-NEG-001: Add Empty Input Handling

- **Entry ID:** e-027
- **Status:** ✅ RESOLVED (2026-01-09)
- **Priority:** LOW
- **Gap:** NEG-GAP-001
- **Agent:** nse-requirements
- **Description:** Add explicit validation for zero requirements input.

### Acceptance Criteria

1. Agent detects `requirements_count: 0` or empty list
2. Returns clear message: "At least 1 requirement required"
3. Does not crash or produce malformed output
4. Suggests next action to user

---

## FIX-NEG-002: Add Maximum Limit Guidance

- **Entry ID:** e-028
- **Status:** ✅ RESOLVED (2026-01-09)
- **Priority:** LOW
- **Gap:** NEG-GAP-002
- **Agent:** nse-requirements
- **Description:** Add guidance for large requirement sets (>100).

### Acceptance Criteria

1. Agent warns when requirements_count > 100
2. Suggests: "Consider splitting into subsystems"
3. Proceeds if user confirms (soft limit)
4. Documents recommended max in agent template

---

## FIX-NEG-003: Add Review Gate Enum Validation

- **Entry ID:** e-029
- **Status:** ✅ RESOLVED (2026-01-09)
- **Priority:** MEDIUM
- **Gap:** NEG-GAP-003
- **Agent:** nse-reviewer
- **Description:** Add explicit enumeration validation for review gate types.

### Acceptance Criteria

1. Valid gates enumerated: SRR, MDR, PDR, CDR, TRR, SAR, ORR, FRR
2. Invalid gate type returns error with valid options
3. Close matches get suggestions (e.g., "CDX" → "Did you mean CDR?")
4. Regex pattern validates format

---

## FIX-NEG-004: Enforce TSR Soft Dependency

- **Entry ID:** e-030
- **Status:** ✅ RESOLVED (2026-01-09)
- **Priority:** LOW
- **Gap:** NEG-GAP-004
- **Agent:** nse-integration
- **Description:** Add soft prerequisite warning when creating ICD without TSR.

### Acceptance Criteria

1. Detect missing TSR-* file before ICD creation
2. Warn: "Architecture (TSR) not found"
3. Offer options: "Create without TSR? (not recommended)"
4. If user proceeds, note in output

---

## FIX-NEG-005: Implement Cross-Reference Validation

- **Entry ID:** e-031
- **Status:** ✅ RESOLVED (2026-01-09)
- **Priority:** MEDIUM
- **Gap:** NEG-GAP-005
- **Agent:** nse-verification, nse-risk
- **Description:** Implement runtime validation for cross-references.

### Acceptance Criteria

1. VCRM validates all REQ-* references exist
2. Risk register validates Affected Requirements exist
3. Orphan references flagged with warning
4. Stale references flagged for human review
5. No auto-deletion of references

---

## FIX-NEG-006: Add Circular Dependency Detection

- **Entry ID:** e-032
- **Status:** ✅ RESOLVED (2026-01-09)
- **Priority:** LOW
- **Gap:** NEG-GAP-006
- **Agent:** nse-requirements
- **Description:** Detect circular dependencies in requirement relationships.

### Acceptance Criteria

1. Detect cycles in depends_on relationships
2. Show cycle path: "REQ-001 → REQ-002 → REQ-003 → REQ-001"
3. Warn: "Circular dependency detected"
4. Allow user to accept with acknowledgment

---

## FIX-NEG-007: Add Interface System Validation

- **Entry ID:** e-033
- **Status:** ✅ RESOLVED (2026-01-09)
- **Priority:** LOW
- **Gap:** NEG-GAP-007
- **Agent:** nse-integration
- **Description:** Validate interface endpoints reference systems defined in TSR.

### Acceptance Criteria

1. Validate system_a and system_b against TSR component list
2. Unknown systems flagged with options
3. "External" classification allows undefined systems
4. Suggest: "Add to TSR or mark as External"

---

## FIX-NEG-008: Add Session Mismatch Handling

- **Entry ID:** e-034
- **Status:** ✅ RESOLVED (2026-01-09)
- **Priority:** MEDIUM
- **Gap:** NEG-GAP-008
- **Agent:** Orchestration state management
- **Description:** Detect and handle state files from different sessions.

### Acceptance Criteria

1. Validate session_id on state load
2. Mismatch triggers warning
3. Prompt user: "Continue with old state? / Start fresh?"
4. Default to safe behavior
5. Log session transitions

---

*Source: Extracted from WORKTRACKER.md lines 283-511*
