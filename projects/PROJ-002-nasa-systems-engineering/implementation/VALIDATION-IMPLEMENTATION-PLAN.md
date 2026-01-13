# Validation System Implementation Plan

> **Document ID:** IMPL-NEG-001
> **Version:** 2.0
> **Date:** 2026-01-09
> **Status:** ✅ COMPLETE
> **Author:** Claude Code
> **Completion Date:** 2026-01-09

---

## Executive Summary

This document defines the implementation plan for fixing 8 validation gaps (3 MEDIUM, 5 LOW) following architectural best practices: DDD, Hexagonal Architecture, CQRS, and TDD Red/Green/Refactor methodology.

---

## 1. Architectural Design

### 1.1 Domain Model (DDD)

```
┌─────────────────────────────────────────────────────────────────┐
│                    DOMAIN LAYER                                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │ ValidationRule  │  │ ValidationResult│  │ ValidationError │  │
│  │ (Value Object)  │  │ (Entity)        │  │ (Value Object)  │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
│                                                                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │ ReviewGateType  │  │ CrossReference  │  │ SessionState    │  │
│  │ (Enum/VO)       │  │ (Entity)        │  │ (Aggregate)     │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Hexagonal Architecture (Ports & Adapters)

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRIMARY ADAPTERS                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │ AgentValidator  │  │ CLIValidator    │  │ APIValidator    │  │
│  │ (Markdown)      │  │ (Commands)      │  │ (REST)          │  │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘  │
│           │                    │                    │           │
│           ▼                    ▼                    ▼           │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              PORTS (Interfaces)                              ││
│  │  ┌───────────────────┐  ┌───────────────────────────────┐   ││
│  │  │ IInputValidator   │  │ ICrossReferenceChecker        │   ││
│  │  │ IReviewGateValidator │  │ ISessionStateValidator     │   ││
│  │  └───────────────────┘  └───────────────────────────────┘   ││
│  └─────────────────────────────────────────────────────────────┘│
│           │                    │                    │           │
│           ▼                    ▼                    ▼           │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              APPLICATION LAYER (Use Cases)                   ││
│  │  ┌───────────────────┐  ┌───────────────────────────────┐   ││
│  │  │ ValidateInputCmd  │  │ CheckCrossReferencesQuery    │   ││
│  │  │ ValidateGateCmd   │  │ ValidateSessionStateCmd      │   ││
│  │  └───────────────────┘  └───────────────────────────────┘   ││
│  └─────────────────────────────────────────────────────────────┘│
│           │                    │                    │           │
│           ▼                    ▼                    ▼           │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              SECONDARY ADAPTERS                              ││
│  │  ┌───────────────────┐  ┌───────────────────────────────┐   ││
│  │  │ FileSystemRepo    │  │ MarkdownArtifactRepo          │   ││
│  │  │ StateFileRepo     │  │ ConfigurationRepo             │   ││
│  │  └───────────────────┘  └───────────────────────────────┘   ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

### 1.3 CQRS Pattern

| Type | Name | Description |
|------|------|-------------|
| Command | ValidateInputCommand | Validates input against rules |
| Command | ValidateReviewGateCommand | Validates review gate type |
| Command | ValidateSessionStateCommand | Validates session state |
| Query | CheckCrossReferencesQuery | Checks artifact references |
| Query | DetectCircularDependenciesQuery | Detects cycles |
| Event | ValidationPassedEvent | Emitted on pass |
| Event | ValidationFailedEvent | Emitted on fail with errors |

---

## 2. Implementation Strategy

### 2.1 Implementation Order (Priority)

| Phase | Work ID | Priority | Complexity | Dependencies |
|-------|---------|----------|------------|--------------|
| 1 | FIX-NEG-003 | MEDIUM | Low | None |
| 2 | FIX-NEG-008 | MEDIUM | Medium | None |
| 3 | FIX-NEG-005 | MEDIUM | High | Repository pattern |
| 4 | FIX-NEG-001 | LOW | Low | None |
| 5 | FIX-NEG-002 | LOW | Low | None |
| 6 | FIX-NEG-004 | LOW | Low | File system check |
| 7 | FIX-NEG-006 | LOW | Medium | Graph algorithm |
| 8 | FIX-NEG-007 | LOW | Low | FIX-NEG-005 |

### 2.2 TDD Red/Green/Refactor Cycle

For each fix:
1. **RED:** Write failing BDD test in BEHAVIOR_TESTS.md
2. **GREEN:** Implement minimal code in agent template to pass
3. **REFACTOR:** Optimize while keeping tests green
4. **VALIDATE:** Run full test suite for regression

---

## 3. Domain Model Specifications

### 3.1 ReviewGateType (Enum)

```yaml
# Domain Value Object
ReviewGateType:
  valid_values:
    - SRR   # System Requirements Review
    - MDR   # Mission Definition Review
    - PDR   # Preliminary Design Review
    - CDR   # Critical Design Review
    - TRR   # Test Readiness Review
    - SAR   # System Acceptance Review
    - ORR   # Operational Readiness Review
    - FRR   # Flight Readiness Review
  validation:
    case_insensitive: true
    suggest_on_typo: true
    max_levenshtein_distance: 2
```

### 3.2 ValidationResult (Entity)

```yaml
# Domain Entity
ValidationResult:
  properties:
    id: string (UUID)
    timestamp: datetime
    rule_id: string
    status: PASS | FAIL | WARN
    errors: list[ValidationError]
    suggestions: list[string]
  invariants:
    - status == FAIL implies errors.length > 0
    - status == PASS implies errors.length == 0
```

### 3.3 CrossReference (Entity)

```yaml
# Domain Entity
CrossReference:
  properties:
    source_artifact: string (path)
    source_id: string (e.g., VCRM-001)
    target_artifact: string (path)
    target_id: string (e.g., REQ-001)
    reference_type: TRACE | DEPENDS | IMPLEMENTS
  validation:
    - target must exist in target_artifact
    - no circular dependencies allowed
```

### 3.4 SessionState (Aggregate Root)

```yaml
# Aggregate Root
SessionState:
  properties:
    session_id: string (UUID)
    agent_id: string
    created_at: datetime
    last_modified: datetime
    workflow_phase: string
    artifacts_produced: list[string]
  commands:
    - ValidateSessionCommand
    - ResumeSessionCommand
  invariants:
    - session_id must match current session
    - created_at <= last_modified
```

---

## 4. Test Specifications

### 4.1 Test Categories Required

| Category | Purpose | Location |
|----------|---------|----------|
| Unit | Domain logic | BEHAVIOR_TESTS.md |
| Integration | Port/adapter | BEHAVIOR_TESTS.md |
| System | Full workflow | ORCHESTRATION-TEST-RESULTS.md |
| E2E | User scenario | NEGATIVE-TEST-SUITE.md |
| Contract | Schema validation | BEHAVIOR_TESTS.md |
| Architecture | Pattern compliance | BEHAVIOR_TESTS.md |

### 4.2 Test Naming Convention

```
BHV-{PRINCIPLE}-{TYPE}-{NUMBER}

Types:
  HP  = Happy Path
  EC  = Edge Case
  NEG = Negative/Failure
  ADV = Adversarial
  CNT = Contract
  ARC = Architecture

Example: BHV-VAL-NEG-001 (Validation Negative Test 001)
```

---

## 5. Phase 1: FIX-NEG-003 (Review Gate Enum)

### 5.1 Sub-Tasks

| Task | Description | Type | Status |
|------|-------------|------|--------|
| 5.1.1 | Write RED test for invalid gate type | BDD Test | ⬜ |
| 5.1.2 | Write RED test for typo suggestion | BDD Test | ⬜ |
| 5.1.3 | Write RED test for case insensitivity | BDD Test | ⬜ |
| 5.1.4 | Define ReviewGateType enum in template | Domain | ⬜ |
| 5.1.5 | Implement validation in guardrails | Adapter | ⬜ |
| 5.1.6 | GREEN: Pass all tests | Verify | ⬜ |
| 5.1.7 | REFACTOR: Optimize suggestions | Code | ⬜ |
| 5.1.8 | Regression test existing artifacts | Verify | ⬜ |

### 5.2 BDD Tests (RED Phase)

```yaml
# Test 1: Invalid Gate Type
id: BHV-VAL-NEG-003-001
category: Validation
agent: nse-reviewer
scenario: User provides invalid review gate type
input:
  review_type: "XYZ"
expected:
  status: FAIL
  error_message: "Invalid review type 'XYZ'"
  valid_options_shown: true
  options: [SRR, MDR, PDR, CDR, TRR, SAR, ORR, FRR]
pass_criteria:
  - Validation rejects "XYZ"
  - Error message lists valid options
  - No partial output created

# Test 2: Typo Suggestion
id: BHV-VAL-NEG-003-002
category: Validation
agent: nse-reviewer
scenario: User provides close typo
input:
  review_type: "CDX"
expected:
  status: FAIL
  error_message: "Invalid review type 'CDX'. Did you mean 'CDR'?"
  suggestion: "CDR"
pass_criteria:
  - Suggests CDR for CDX
  - Levenshtein distance <= 2 triggers suggestion

# Test 3: Case Insensitivity
id: BHV-VAL-NEG-003-003
category: Validation
agent: nse-reviewer
scenario: User provides lowercase gate type
input:
  review_type: "cdr"
expected:
  status: PASS
  normalized_value: "CDR"
pass_criteria:
  - Accepts lowercase input
  - Normalizes to uppercase internally

# Test 4: Happy Path
id: BHV-VAL-HP-003-001
category: Validation
agent: nse-reviewer
scenario: User provides valid gate type
input:
  review_type: "CDR"
expected:
  status: PASS
pass_criteria:
  - Accepts valid gate type
  - No errors or warnings
```

### 5.3 Implementation Specification

```yaml
# nse-reviewer.md guardrails addition
guardrails:
  input_validation:
    review_type_enum:
      valid: [SRR, MDR, PDR, CDR, TRR, SAR, ORR, FRR]
      case_insensitive: true
      on_invalid:
        action: reject
        message_template: "Invalid review type '{input}'. Valid types: {valid_list}"
      on_typo:
        max_distance: 2
        suggest: true
        message_template: "Invalid review type '{input}'. Did you mean '{suggestion}'?"
```

---

## 6. Phase 2: FIX-NEG-008 (Session Mismatch)

### 6.1 Sub-Tasks

| Task | Description | Type | Status |
|------|-------------|------|--------|
| 6.1.1 | Write RED test for session mismatch detection | BDD Test | ⬜ |
| 6.1.2 | Write RED test for warning prompt | BDD Test | ⬜ |
| 6.1.3 | Write RED test for safe default behavior | BDD Test | ⬜ |
| 6.1.4 | Define SessionState validation in ORCHESTRATION | Domain | ⬜ |
| 6.1.5 | Implement session validation logic | Adapter | ⬜ |
| 6.1.6 | GREEN: Pass all tests | Verify | ⬜ |
| 6.1.7 | REFACTOR: Add session recovery options | Code | ⬜ |
| 6.1.8 | Regression test existing workflows | Verify | ⬜ |

### 6.2 BDD Tests (RED Phase)

```yaml
# Test 1: Session Mismatch Detection
id: BHV-VAL-NEG-008-001
category: State Management
agent: orchestration
scenario: State file has different session_id
input:
  current_session: "session-123"
  state_file_session: "session-456"
expected:
  status: WARN
  warning: "State from different session detected"
  prompt: "Continue with old state? / Start fresh?"
pass_criteria:
  - Detects session_id mismatch
  - Does not silently use old state
  - Prompts user for decision

# Test 2: Safe Default
id: BHV-VAL-NEG-008-002
category: State Management
agent: orchestration
scenario: Session mismatch with no user response
input:
  current_session: "session-123"
  state_file_session: "session-456"
  user_response: null (timeout)
expected:
  status: SAFE
  action: "Start fresh (default)"
  old_state_preserved: true
pass_criteria:
  - Defaults to starting fresh
  - Old state preserved in backup
  - No data loss

# Test 3: Same Session (Happy Path)
id: BHV-VAL-HP-008-001
category: State Management
agent: orchestration
scenario: State file matches current session
input:
  current_session: "session-123"
  state_file_session: "session-123"
expected:
  status: PASS
  action: "Resume normally"
pass_criteria:
  - No warning shown
  - State loaded normally
  - Workflow continues
```

---

## 7. Phase 3: FIX-NEG-005 (Cross-Reference Validation)

### 7.1 Sub-Tasks

| Task | Description | Type | Status |
|------|-------------|------|--------|
| 7.1.1 | Write RED test for orphan reference detection | BDD Test | ⬜ |
| 7.1.2 | Write RED test for stale reference handling | BDD Test | ⬜ |
| 7.1.3 | Write RED test for valid reference pass | BDD Test | ⬜ |
| 7.1.4 | Define CrossReference entity | Domain | ⬜ |
| 7.1.5 | Define ICrossReferenceChecker port | Port | ⬜ |
| 7.1.6 | Implement MarkdownArtifactChecker adapter | Adapter | ⬜ |
| 7.1.7 | Add post_completion_check to agents | Integration | ⬜ |
| 7.1.8 | GREEN: Pass all tests | Verify | ⬜ |
| 7.1.9 | REFACTOR: Optimize file scanning | Code | ⬜ |
| 7.1.10 | Regression test existing VCRM/RISK | Verify | ⬜ |

### 7.2 BDD Tests (RED Phase)

```yaml
# Test 1: Orphan Reference
id: BHV-VAL-NEG-005-001
category: Cross-Reference
agent: nse-verification
scenario: VCRM references non-existent requirement
input:
  vcrm_content: |
    | REQ-NSE-FUN-001 | Pass | ...
    | REQ-NSE-FUN-099 | Pass | ...
  requirements_file:
    - REQ-NSE-FUN-001 (exists)
    # REQ-NSE-FUN-099 does NOT exist
expected:
  status: WARN
  warning: "Orphan reference: REQ-NSE-FUN-099 not found in requirements baseline"
  suggestions: ["Remove reference", "Create missing requirement"]
pass_criteria:
  - Detects missing REQ-NSE-FUN-099
  - Does not fail silently
  - Provides actionable suggestions

# Test 2: Stale Reference
id: BHV-VAL-NEG-005-002
category: Cross-Reference
agent: nse-risk
scenario: Risk references deleted requirement
input:
  risk_content: |
    | R-001 | If... | REQ-NSE-FUN-001 | ...
  requirements_file:
    # REQ-NSE-FUN-001 was deleted
expected:
  status: WARN
  warning: "Stale reference: REQ-NSE-FUN-001 no longer exists"
  action: "Flagged for human review"
  auto_delete: false
pass_criteria:
  - Detects deleted requirement
  - Preserves risk for review
  - Does NOT auto-delete

# Test 3: Valid References (Happy Path)
id: BHV-VAL-HP-005-001
category: Cross-Reference
agent: nse-verification
scenario: All VCRM references exist
input:
  vcrm_references: [REQ-NSE-FUN-001, REQ-NSE-FUN-002]
  requirements_file:
    - REQ-NSE-FUN-001 (exists)
    - REQ-NSE-FUN-002 (exists)
expected:
  status: PASS
  message: "All references validated"
pass_criteria:
  - All references found
  - No warnings
  - Validation passes
```

---

## 8. Phases 4-8: LOW Priority Fixes

### 8.1 FIX-NEG-001: Empty Input Handling

```yaml
tests:
  - id: BHV-VAL-NEG-001-001
    scenario: Zero requirements provided
    expected: Graceful rejection with guidance
  - id: BHV-VAL-HP-001-001
    scenario: Single requirement (min valid)
    expected: Accepts and processes

implementation:
  location: nse-requirements.md guardrails
  add:
    min_requirements: 1
    on_empty:
      action: reject
      message: "At least 1 requirement required. Provide stakeholder needs first."
```

### 8.2 FIX-NEG-002: Maximum Limit Guidance

```yaml
tests:
  - id: BHV-VAL-NEG-002-001
    scenario: 101 requirements (over max)
    expected: Warning with chunking suggestion
  - id: BHV-VAL-HP-002-001
    scenario: 100 requirements (at max)
    expected: Accepts normally

implementation:
  location: nse-requirements.md guardrails
  add:
    max_recommended: 100
    on_exceed:
      action: warn
      message: "Large requirement set (>100). Consider splitting into subsystems."
      allow_override: true
```

### 8.3 FIX-NEG-004: TSR Soft Dependency

```yaml
tests:
  - id: BHV-VAL-NEG-004-001
    scenario: ICD without TSR present
    expected: Warning with options
  - id: BHV-VAL-HP-004-001
    scenario: ICD with TSR present
    expected: Validates normally

implementation:
  location: nse-integration.md guardrails
  add:
    soft_prerequisites:
      - artifact: TSR
        on_missing:
          action: warn
          message: "Architecture (TSR) not found. Interfaces derive from architecture."
          options: ["Create without TSR (not recommended)", "Create TSR first"]
```

### 8.4 FIX-NEG-006: Circular Dependency Detection

```yaml
tests:
  - id: BHV-VAL-NEG-006-001
    scenario: Circular dependency in requirements
    expected: Warning with cycle path
  - id: BHV-VAL-HP-006-001
    scenario: Linear dependencies
    expected: No warning

implementation:
  location: nse-requirements.md guardrails + ORCHESTRATION.md
  add:
    validate_no_cycles:
      action: warn
      algorithm: DFS with visited tracking
      message_template: "Circular dependency detected: {cycle_path}"
      allow_override: true
```

### 8.5 FIX-NEG-007: Interface System Validation

```yaml
tests:
  - id: BHV-VAL-NEG-007-001
    scenario: Interface references undefined system
    expected: Warning with options
  - id: BHV-VAL-HP-007-001
    scenario: Interface references defined systems
    expected: Validates normally

implementation:
  location: nse-integration.md guardrails
  add:
    validate_systems_in_tsr:
      action: soft_validate
      on_undefined:
        message: "System '{system}' not found in architecture."
        options: ["Add to TSR", "Mark as External"]
      allow_external: true
```

---

## 9. Regression Test Matrix

| Artifact | Tests | Pass Criteria |
|----------|-------|---------------|
| REQ-NSE-SKILL-001.md | BHV-040-*, BHV-041-*, BHV-043-* | All existing tests pass |
| VCRM-NSE-SKILL-001.md | BHV-041-VER-*, BHV-TRACE-001 | All existing tests pass |
| RISK-NSE-SKILL-001.md | BHV-042-*, BHV-TRACE-002 | All existing tests pass |
| TSR-NSE-SKILL-001.md | BHV-TRACE-002 | All existing tests pass |
| ICD-NSE-SKILL-001.md | BHV-TRACE-003 | All existing tests pass |
| REVIEW-NSE-SKILL-001.md | BHV-043-* | All existing tests pass |
| STATUS-NSE-SKILL-001.md | BHV-043-* | All existing tests pass |

---

## 10. Acceptance Criteria Checklist

### Per Fix:
- [ ] RED: BDD tests written and failing
- [ ] GREEN: Implementation passes all tests
- [ ] REFACTOR: Code optimized, tests still pass
- [ ] Unit tests: Domain logic validated
- [ ] Integration tests: Ports/adapters work
- [ ] System tests: Full workflow passes
- [ ] E2E tests: User scenarios work
- [ ] Contract tests: Schema validated
- [ ] Architecture tests: Patterns followed
- [ ] Regression: Existing functionality unchanged

### Overall:
- [ ] All 8 fixes implemented
- [ ] All 10 partial tests now pass
- [ ] 0 regressions in existing tests
- [ ] WORKTRACKER updated
- [ ] Documentation complete

---

## References

1. Evans, Eric. *Domain-Driven Design*. Addison-Wesley, 2003.
2. Cockburn, Alistair. *Hexagonal Architecture*. https://alistair.cockburn.us/hexagonal-architecture/
3. Fowler, Martin. *CQRS*. https://martinfowler.com/bliki/CQRS.html
4. Beck, Kent. *Test-Driven Development*. Addison-Wesley, 2002.
5. ISTQB. *Boundary Value Analysis*. https://istqb.org/

---

*Document Status: READY FOR IMPLEMENTATION*
