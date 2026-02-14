# TASK-004: Session Context Enforcement End-to-End Testing

<!--
TEMPLATE: Task Deliverable
VERSION: 1.0.0
ENABLER: EN-406
AC: AC-4
CREATED: 2026-02-13 (ps-validator-406)
PURPOSE: End-to-end test specifications for session context enforcement mechanisms
-->

> **Type:** deliverable
> **Status:** complete
> **Parent:** EN-406-integration-testing-validation
> **AC Mapping:** AC-4 (Session context enforcement passes end-to-end testing)
> **Agent:** ps-validator-406
> **Created:** 2026-02-13

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | Test scope for session context enforcement |
| [EN-405 Conditional AC Closure](#en-405-conditional-ac-closure) | Tests that close EN-405 conditional ACs |
| [Preamble Generation Tests](#preamble-generation-tests) | SessionQualityContextGenerator tests |
| [Preamble Content Tests](#preamble-content-tests) | Content accuracy and completeness |
| [Integration Tests](#integration-tests) | SessionStart hook integration |
| [Token Budget Tests](#token-budget-tests) | Token budget compliance |
| [Error Handling Tests](#error-handling-tests) | Graceful degradation tests |
| [L1-L2 Coordination Tests](#l1-l2-coordination-tests) | Cross-layer coordination |
| [Requirements Traceability](#requirements-traceability) | Test-to-requirement mapping |
| [References](#references) | Source documents |

---

## Overview

This document specifies end-to-end test cases for session context enforcement mechanisms defined in EN-405. These tests validate the SessionQualityContextGenerator, its 4-section XML preamble, integration with the SessionStart hook, token budget compliance, error handling, and L1-L2 coordination.

Critically, this document addresses the **3 conditional ACs from EN-405** that are specifically EN-406's responsibility to close:
- **EN-405 AC-4:** Integration test execution
- **EN-405 AC-5:** Auto-loading verification
- **EN-405 AC-8:** macOS platform tests

### Test Summary

| Category | Test Count | ID Range |
|----------|------------|----------|
| EN-405 Conditional AC Closure | 6 | TC-COND-001 through TC-COND-006 |
| Preamble Generation | 5 | TC-PGEN-001 through TC-PGEN-005 |
| Preamble Content | 8 | TC-PCNT-001 through TC-PCNT-008 |
| Integration | 6 | TC-SINT-001 through TC-SINT-006 |
| Token Budget | 4 | TC-STOK-001 through TC-STOK-004 |
| Error Handling | 4 | TC-SERR-001 through TC-SERR-004 |
| L1-L2 Coordination | 4 | TC-COORD-001 through TC-COORD-004 |
| **Total** | **37** | |

---

## EN-405 Conditional AC Closure

These tests are specifically designed to close the 3 conditional ACs identified in the EN-405 validation report (TASK-010, quality score 0.936 CONDITIONAL PASS).

### TC-COND-001: EN-405 AC-4 - Integration Test Execution (Part 1)

| Field | Value |
|-------|-------|
| **ID** | TC-COND-001 |
| **Objective** | Verify SessionQualityContextGenerator integrates with SessionStart hook end-to-end |
| **EN-405 AC** | AC-4 (Integration) |
| **Condition from EN-405** | "Phase 4 integration test execution" required for full pass |
| **Preconditions** | SessionQualityContextGenerator module exists; SessionStart hook exists |
| **Steps** | 1. Import SessionQualityContextGenerator. 2. Call generate(). 3. Verify output is valid XML. 4. Verify output integrates into SessionStart output chain. |
| **Expected Output** | Complete quality preamble appended to session start output without disrupting existing functionality |
| **Pass Criteria** | Preamble generated; integration successful; no errors; existing session start output intact |
| **Requirements** | IR-405-001, IR-405-002 |
| **Verification** | Test |
| **Closure** | Successfully passing this test closes EN-405 AC-4 |

### TC-COND-002: EN-405 AC-4 - Integration Test Execution (Part 2)

| Field | Value |
|-------|-------|
| **ID** | TC-COND-002 |
| **Objective** | Verify quality preamble content is accessible to Claude after session start |
| **EN-405 AC** | AC-4 (Integration) |
| **Preconditions** | Session started with quality preamble |
| **Steps** | 1. Start session. 2. Verify quality preamble appears in initial context. 3. Verify Claude can reference quality gate values from preamble. |
| **Expected Output** | Quality context available in Claude's working memory after session start |
| **Pass Criteria** | Preamble content verified in session context |
| **Requirements** | IR-405-003 |
| **Verification** | Test + Inspection |
| **Closure** | Successfully passing this test, combined with TC-COND-001, fully closes EN-405 AC-4 |

### TC-COND-003: EN-405 AC-5 - Auto-Loading Verification (Part 1)

| Field | Value |
|-------|-------|
| **ID** | TC-COND-003 |
| **Objective** | Verify SessionStart hook automatically loads quality preamble without manual intervention |
| **EN-405 AC** | AC-5 (Auto-loading) |
| **Condition from EN-405** | Auto-loading verification required for full pass |
| **Preconditions** | SessionQualityContextGenerator module installed; QUALITY_CONTEXT_AVAILABLE flag |
| **Steps** | 1. Ensure module is importable. 2. Start session normally. 3. Verify preamble appears in output without any user action. |
| **Expected Output** | Quality preamble auto-loaded as part of SessionStart hook execution |
| **Pass Criteria** | No manual steps required; preamble present in session output automatically |
| **Requirements** | IR-405-001, FR-405-001 |
| **Verification** | Test |
| **Closure** | Successfully passing this test closes EN-405 AC-5 |

### TC-COND-004: EN-405 AC-5 - Auto-Loading Verification (Part 2)

| Field | Value |
|-------|-------|
| **ID** | TC-COND-004 |
| **Objective** | Verify auto-loading respects QUALITY_CONTEXT_AVAILABLE flag |
| **EN-405 AC** | AC-5 (Auto-loading) |
| **Preconditions** | Module availability can be toggled |
| **Steps** | 1. Set QUALITY_CONTEXT_AVAILABLE = True; verify preamble loads. 2. Set QUALITY_CONTEXT_AVAILABLE = False; verify preamble does not load. |
| **Expected Output** | Preamble loading controlled by flag; no errors in either state |
| **Pass Criteria** | Flag correctly controls preamble loading |
| **Requirements** | EH-405-001 |
| **Verification** | Test |

### TC-COND-005: EN-405 AC-8 - macOS Platform Tests (Part 1)

| Field | Value |
|-------|-------|
| **ID** | TC-COND-005 |
| **Objective** | Verify session context enforcement works correctly on macOS |
| **EN-405 AC** | AC-8 (macOS tests) |
| **Condition from EN-405** | macOS platform validation required for full pass |
| **Preconditions** | macOS environment (Darwin); Python 3.11+ via UV |
| **Steps** | 1. Execute on macOS. 2. Run SessionQualityContextGenerator.generate(). 3. Verify output. 4. Run full session start. 5. Verify integration. |
| **Expected Output** | All operations succeed on macOS; no platform-specific issues |
| **Pass Criteria** | All session context tests pass on macOS |
| **Requirements** | PR-405-003 |
| **Verification** | Test |
| **Closure** | Successfully passing this test closes EN-405 AC-8 |

### TC-COND-006: EN-405 AC-8 - macOS Platform Tests (Part 2)

| Field | Value |
|-------|-------|
| **ID** | TC-COND-006 |
| **Objective** | Verify file paths, encoding, and line endings work correctly on macOS |
| **EN-405 AC** | AC-8 (macOS tests) |
| **Preconditions** | macOS environment |
| **Steps** | 1. Verify UTF-8 encoding in preamble output. 2. Verify LF line endings. 3. Verify file paths use POSIX conventions. |
| **Expected Output** | No encoding issues; no line ending issues; correct path handling |
| **Pass Criteria** | macOS-compatible in all aspects |
| **Requirements** | PR-405-003, PR-405-004 |
| **Verification** | Test |

---

## Preamble Generation Tests

### TC-PGEN-001: Generator Class Instantiation

| Field | Value |
|-------|-------|
| **ID** | TC-PGEN-001 |
| **Objective** | Verify SessionQualityContextGenerator can be instantiated |
| **Input** | `from src.infrastructure.internal.enforcement.session_quality_context import SessionQualityContextGenerator` |
| **Expected Output** | Class instantiates without error |
| **Requirements** | FR-405-001 |
| **Verification** | Test |

### TC-PGEN-002: Generate Method Returns String

| Field | Value |
|-------|-------|
| **ID** | TC-PGEN-002 |
| **Objective** | Verify generate() method returns a non-empty string |
| **Input** | `SessionQualityContextGenerator().generate()` |
| **Expected Output** | Non-empty string containing XML content |
| **Requirements** | FR-405-001, FR-405-002 |
| **Verification** | Test |

### TC-PGEN-003: Generate Method Idempotency

| Field | Value |
|-------|-------|
| **ID** | TC-PGEN-003 |
| **Objective** | Verify generate() produces identical output on repeated calls |
| **Input** | Two calls to generate() |
| **Expected Output** | Output 1 == Output 2 |
| **Requirements** | FR-405-014 |
| **Verification** | Test |

### TC-PGEN-004: Generate Method XML Well-formedness

| Field | Value |
|-------|-------|
| **ID** | TC-PGEN-004 |
| **Objective** | Verify generated output is well-formed XML |
| **Input** | Generated preamble |
| **Steps** | 1. Generate preamble. 2. Parse with XML parser. |
| **Expected Output** | Parses without errors |
| **Requirements** | FR-405-015 |
| **Verification** | Test |

### TC-PGEN-005: Generate Method Has All 4 Sections

| Field | Value |
|-------|-------|
| **ID** | TC-PGEN-005 |
| **Objective** | Verify output contains all 4 required XML sections |
| **Input** | Generated preamble |
| **Expected Output** | Contains: `<quality-gate>`, `<constitutional-principles>`, `<adversarial-strategies>`, `<decision-criticality>` |
| **Pass Criteria** | All 4 sections present as distinct XML elements |
| **Requirements** | FR-405-001, FR-405-002, FR-405-003, FR-405-004 |
| **Verification** | Test |

---

## Preamble Content Tests

### TC-PCNT-001: Quality Gate - Scoring Criteria

| Field | Value |
|-------|-------|
| **ID** | TC-PCNT-001 |
| **Objective** | Verify quality-gate section contains scoring criteria |
| **Input** | `<quality-gate>` section content |
| **Expected Content** | References to scoring methodology, evidence-based assessment |
| **Requirements** | FR-405-005 |
| **Verification** | Inspection |

### TC-PCNT-002: Quality Gate - Threshold Value

| Field | Value |
|-------|-------|
| **ID** | TC-PCNT-002 |
| **Objective** | Verify quality-gate section specifies >= 0.92 threshold |
| **Input** | `<quality-gate>` section content |
| **Expected Content** | Explicit ">= 0.92" or "0.92" threshold value |
| **Pass Criteria** | Threshold value present and correct |
| **Requirements** | FR-405-006 |
| **Verification** | Inspection |

### TC-PCNT-003: Quality Gate - Self-Review Mandate

| Field | Value |
|-------|-------|
| **ID** | TC-PCNT-003 |
| **Objective** | Verify quality-gate section mandates self-review |
| **Input** | `<quality-gate>` section content |
| **Expected Content** | Instruction to perform self-review before submission |
| **Requirements** | FR-405-006 |
| **Verification** | Inspection |

### TC-PCNT-004: Constitutional Principles - P-003

| Field | Value |
|-------|-------|
| **ID** | TC-PCNT-004 |
| **Objective** | Verify P-003 (No Recursive Subagents) is encoded |
| **Input** | `<constitutional-principles>` section content |
| **Expected Content** | P-003 reference with "Max ONE level: orchestrator -> worker" or equivalent |
| **Requirements** | FR-405-007 |
| **Verification** | Inspection |

### TC-PCNT-005: Constitutional Principles - P-020 and P-022

| Field | Value |
|-------|-------|
| **ID** | TC-PCNT-005 |
| **Objective** | Verify P-020 (User Authority) and P-022 (No Deception) are encoded |
| **Input** | `<constitutional-principles>` section content |
| **Expected Content** | P-020 with "User decides" theme; P-022 with "Never deceive" theme |
| **Requirements** | FR-405-008 |
| **Verification** | Inspection |

### TC-PCNT-006: Adversarial Strategies - Strategy Count

| Field | Value |
|-------|-------|
| **ID** | TC-PCNT-006 |
| **Objective** | Verify exactly 10 adversarial strategies are encoded |
| **Input** | `<adversarial-strategies>` section content |
| **Steps** | 1. Parse strategy list. 2. Count distinct strategies. |
| **Expected Output** | Count = 10, from S-001 through S-014 subset |
| **Requirements** | FR-405-009 |
| **Verification** | Inspection |

### TC-PCNT-007: Adversarial Strategies - Context Rot Awareness

| Field | Value |
|-------|-------|
| **ID** | TC-PCNT-007 |
| **Objective** | Verify context rot awareness is included in adversarial section |
| **Input** | `<adversarial-strategies>` section content |
| **Expected Content** | Reference to context rot, degradation awareness, L2 re-injection value |
| **Requirements** | SR-405-001 |
| **Verification** | Inspection |

### TC-PCNT-008: Decision Criticality - Auto-Escalate Rules

| Field | Value |
|-------|-------|
| **ID** | TC-PCNT-008 |
| **Objective** | Verify AE-001 through AE-004 auto-escalate rules are present |
| **Input** | `<decision-criticality>` section content |
| **Steps** | 1. Parse auto-escalate rules. 2. Verify all 4 present. |
| **Expected Content** | AE-001 (governance -> C4), AE-002 (rules -> C3), AE-003 (architecture -> C3), AE-004 (constitutional -> C4) |
| **Requirements** | FR-405-012 |
| **Verification** | Inspection |

---

## Integration Tests

### TC-SINT-001: Import Integration

| Field | Value |
|-------|-------|
| **ID** | TC-SINT-001 |
| **Objective** | Verify SessionQualityContextGenerator is importable from SessionStart hook |
| **Input** | `try: from src.infrastructure.internal.enforcement.session_quality_context import SessionQualityContextGenerator` |
| **Expected Output** | Import succeeds; QUALITY_CONTEXT_AVAILABLE = True |
| **Requirements** | IR-405-001 |
| **Verification** | Test |

### TC-SINT-002: Output Chain Position

| Field | Value |
|-------|-------|
| **ID** | TC-SINT-002 |
| **Objective** | Verify preamble is inserted at correct position in output chain |
| **Input** | Full session start execution |
| **Expected Output** | Preamble appears AFTER format_hook_output() and BEFORE output_json() |
| **Pass Criteria** | Correct ordering in output chain |
| **Requirements** | IR-405-002 |
| **Verification** | Inspection |

### TC-SINT-003: Existing Output Preservation

| Field | Value |
|-------|-------|
| **ID** | TC-SINT-003 |
| **Objective** | Verify existing SessionStart output is not corrupted by preamble addition |
| **Input** | Session start with and without preamble |
| **Steps** | 1. Capture output without preamble (QUALITY_CONTEXT_AVAILABLE=False). 2. Capture with preamble. 3. Verify original content preserved. |
| **Expected Output** | All existing content identical in both outputs; preamble is purely additive |
| **Pass Criteria** | Zero modifications to existing output |
| **Requirements** | IR-405-002, EH-405-002 |
| **Verification** | Test |

### TC-SINT-004: Project Context Compatibility

| Field | Value |
|-------|-------|
| **ID** | TC-SINT-004 |
| **Objective** | Verify preamble works alongside `<project-context>` tags |
| **Input** | Session start with active project |
| **Expected Output** | Both `<project-context>` and quality preamble sections present |
| **Pass Criteria** | No tag conflict; both sections parseable |
| **Requirements** | IR-405-004 |
| **Verification** | Test |

### TC-SINT-005: No Active Project Compatibility

| Field | Value |
|-------|-------|
| **ID** | TC-SINT-005 |
| **Objective** | Verify preamble works when no project is active (`<project-required>`) |
| **Input** | Session start without active project |
| **Expected Output** | `<project-required>` tags AND quality preamble both present |
| **Pass Criteria** | Preamble still injected regardless of project state |
| **Requirements** | IR-405-005 |
| **Verification** | Test |

### TC-SINT-006: Error State Compatibility

| Field | Value |
|-------|-------|
| **ID** | TC-SINT-006 |
| **Objective** | Verify preamble works during `<project-error>` state |
| **Input** | Session start with invalid project |
| **Expected Output** | `<project-error>` tags AND quality preamble both present (or preamble gracefully absent) |
| **Pass Criteria** | No crash; existing error handling preserved |
| **Requirements** | IR-405-006, EH-405-003 |
| **Verification** | Test |

---

## Token Budget Tests

### TC-STOK-001: Character Count Measurement

| Field | Value |
|-------|-------|
| **ID** | TC-STOK-001 |
| **Objective** | Verify preamble character count matches specification |
| **Input** | Generated preamble |
| **Steps** | 1. Measure len(preamble). 2. Compare to ~2,096 target. |
| **Expected Output** | Character count approximately 2,096 (+/- 10%) |
| **Requirements** | PR-405-001 |
| **Verification** | Test |

### TC-STOK-002: Conservative Token Estimate

| Field | Value |
|-------|-------|
| **ID** | TC-STOK-002 |
| **Objective** | Verify conservative token estimate (chars/4) within budget |
| **Input** | Generated preamble character count |
| **Steps** | 1. Calculate chars/4. 2. Compare to ~524 target. |
| **Expected Output** | Conservative tokens <= 524 |
| **Requirements** | PR-405-001 |
| **Verification** | Test |

### TC-STOK-003: Calibrated Token Estimate

| Field | Value |
|-------|-------|
| **ID** | TC-STOK-003 |
| **Objective** | Verify calibrated token estimate (chars/4 * 0.83) within budget |
| **Input** | Generated preamble character count |
| **Steps** | 1. Calculate (chars/4) * 0.83. 2. Compare to ~435 target. |
| **Expected Output** | Calibrated tokens <= 435 |
| **Requirements** | PR-405-002 |
| **Verification** | Test |

### TC-STOK-004: Per-Section Token Distribution

| Field | Value |
|-------|-------|
| **ID** | TC-STOK-004 |
| **Objective** | Verify per-section token distribution matches specification |
| **Input** | Generated preamble, parsed by section |
| **Expected Distribution** | quality-gate ~100 cal. tokens; constitutional-principles ~85; adversarial-strategies ~174; decision-criticality ~130 |
| **Pass Criteria** | Each section within +/- 20% of target |
| **Requirements** | PR-405-001 |
| **Verification** | Analysis |

---

## Error Handling Tests

### TC-SERR-001: Missing Module Graceful Degradation

| Field | Value |
|-------|-------|
| **ID** | TC-SERR-001 |
| **Objective** | Verify session starts normally when quality module is unavailable |
| **Input** | Session start with quality module import failing |
| **Steps** | 1. Rename/remove quality module. 2. Start session. 3. Verify QUALITY_CONTEXT_AVAILABLE = False. 4. Verify session completes normally. |
| **Expected Output** | Session starts; existing functionality preserved; quality preamble absent |
| **Pass Criteria** | No crash; no error output; session functional |
| **Requirements** | EH-405-001, EH-405-002 |
| **Verification** | Test |

### TC-SERR-002: Generator Exception Handling

| Field | Value |
|-------|-------|
| **ID** | TC-SERR-002 |
| **Objective** | Verify session survives if generate() raises an exception |
| **Input** | Mock SessionQualityContextGenerator.generate() to raise RuntimeError |
| **Expected Output** | Exception caught; session continues without preamble |
| **Pass Criteria** | No crash; graceful fallback |
| **Requirements** | EH-405-003 |
| **Verification** | Test |

### TC-SERR-003: Corrupted Module Handling

| Field | Value |
|-------|-------|
| **ID** | TC-SERR-003 |
| **Objective** | Verify session handles corrupted quality module file |
| **Input** | Corrupted .py file (syntax error) |
| **Expected Output** | Import fails; QUALITY_CONTEXT_AVAILABLE = False; session continues |
| **Pass Criteria** | Graceful degradation |
| **Requirements** | EH-405-001 |
| **Verification** | Test |

### TC-SERR-004: Partial Module Availability

| Field | Value |
|-------|-------|
| **ID** | TC-SERR-004 |
| **Objective** | Verify handling when module exists but class is missing |
| **Input** | Module file exists but SessionQualityContextGenerator class removed |
| **Expected Output** | ImportError caught; QUALITY_CONTEXT_AVAILABLE = False; session continues |
| **Pass Criteria** | Graceful fallback |
| **Requirements** | EH-405-004 |
| **Verification** | Test |

---

## L1-L2 Coordination Tests

### TC-COORD-001: Content Complementarity

| Field | Value |
|-------|-------|
| **ID** | TC-COORD-001 |
| **Objective** | Verify L1 session preamble and L2 prompt reinforcement are complementary, not redundant |
| **Input** | Session preamble output + UserPromptSubmit output for same session |
| **Steps** | 1. Capture session preamble. 2. Trigger UserPromptSubmit. 3. Compare content overlap. |
| **Expected Output** | L1 comprehensive (once); L2 compact (per prompt); minimal overlap |
| **Pass Criteria** | Content serves different purposes; no wasteful duplication |
| **Requirements** | IR-405-003 |
| **Verification** | Inspection |

### TC-COORD-002: L1 Comprehensive vs L2 Compact

| Field | Value |
|-------|-------|
| **ID** | TC-COORD-002 |
| **Objective** | Verify L1 provides full detail while L2 provides compact reinforcement |
| **Input** | Both outputs |
| **Steps** | 1. Measure L1 tokens (~435). 2. Measure L2 tokens (~600 max). 3. Analyze content depth. |
| **Expected Output** | L1 detailed with full context; L2 action-oriented with key reminders |
| **Pass Criteria** | Distinct content profiles |
| **Requirements** | IR-405-003, IR-405-004 |
| **Verification** | Inspection |

### TC-COORD-003: Strategy Reference Consistency

| Field | Value |
|-------|-------|
| **ID** | TC-COORD-003 |
| **Objective** | Verify adversarial strategy references are consistent between L1 and L2 |
| **Input** | L1 adversarial-strategies section + L2 strategy references |
| **Steps** | 1. Extract strategy IDs from L1. 2. Extract strategy references from L2. 3. Verify consistency. |
| **Expected Output** | L2 references are a subset of L1 strategies; no contradictions |
| **Pass Criteria** | Consistent strategy references |
| **Requirements** | SR-405-001, REQ-403-090 |
| **Verification** | Inspection |

### TC-COORD-004: Criticality Level Consistency

| Field | Value |
|-------|-------|
| **ID** | TC-COORD-004 |
| **Objective** | Verify C1-C4 definitions are consistent between L1 preamble and L2 criticality detection |
| **Input** | L1 decision-criticality section + L2 criticality attribute |
| **Steps** | 1. Extract C1-C4 definitions from L1. 2. Verify L2 uses same definitions. |
| **Expected Output** | Identical criticality definitions |
| **Pass Criteria** | Zero definition conflicts |
| **Requirements** | IR-405-007, REQ-403-060 |
| **Verification** | Inspection |

---

## Requirements Traceability

| Test ID | Requirements Verified | EN-405 AC Closure |
|---------|----------------------|-------------------|
| TC-COND-001 | IR-405-001, IR-405-002 | AC-4 (partial) |
| TC-COND-002 | IR-405-003 | AC-4 (full) |
| TC-COND-003 | IR-405-001, FR-405-001 | AC-5 (partial) |
| TC-COND-004 | EH-405-001 | AC-5 (full) |
| TC-COND-005 | PR-405-003 | AC-8 (partial) |
| TC-COND-006 | PR-405-003, PR-405-004 | AC-8 (full) |
| TC-PGEN-001 | FR-405-001 | -- |
| TC-PGEN-002 | FR-405-001, FR-405-002 | -- |
| TC-PGEN-003 | FR-405-014 | -- |
| TC-PGEN-004 | FR-405-015 | -- |
| TC-PGEN-005 | FR-405-001 through FR-405-004 | -- |
| TC-PCNT-001 through TC-PCNT-003 | FR-405-005, FR-405-006 | -- |
| TC-PCNT-004, TC-PCNT-005 | FR-405-007, FR-405-008 | -- |
| TC-PCNT-006, TC-PCNT-007 | FR-405-009, FR-405-010, SR-405-001 | -- |
| TC-PCNT-008 | FR-405-012 | -- |
| TC-SINT-001 | IR-405-001 | -- |
| TC-SINT-002 | IR-405-002 | -- |
| TC-SINT-003 | IR-405-002, EH-405-002 | -- |
| TC-SINT-004 | IR-405-004 | -- |
| TC-SINT-005 | IR-405-005 | -- |
| TC-SINT-006 | IR-405-006, EH-405-003 | -- |
| TC-STOK-001, TC-STOK-002 | PR-405-001 | -- |
| TC-STOK-003 | PR-405-002 | -- |
| TC-STOK-004 | PR-405-001 | -- |
| TC-SERR-001 | EH-405-001, EH-405-002 | -- |
| TC-SERR-002 | EH-405-003 | -- |
| TC-SERR-003 | EH-405-001 | -- |
| TC-SERR-004 | EH-405-004 | -- |
| TC-COORD-001, TC-COORD-002 | IR-405-003, IR-405-004 | -- |
| TC-COORD-003 | SR-405-001, REQ-403-090 | -- |
| TC-COORD-004 | IR-405-007, REQ-403-060 | -- |

---

## References

| Document | Path | Relevance |
|----------|------|-----------|
| EN-405 TASK-001 | `../EN-405-session-context-enforcement/TASK-001-requirements.md` | 34 session context requirements |
| EN-405 TASK-006 | `../EN-405-session-context-enforcement/TASK-006-preamble-content.md` | Exact XML preamble content |
| EN-405 TASK-010 | `../EN-405-session-context-enforcement/TASK-010-validation-report.md` | Conditional pass, 3 conditional ACs |
| EN-403 TASK-004 | `../EN-403-hook-based-enforcement/TASK-004-sessionstart-design.md` | SessionStart hook design |
| EN-403 TASK-002 | `../EN-403-hook-based-enforcement/TASK-002-userpromptsubmit-design.md` | L2 design for coordination tests |
| TASK-001 Integration Test Plan | `TASK-001-integration-test-plan.md` | Master test plan |

---

*Generated by ps-validator-406 | 2026-02-13 | EN-406 AC-4 | Closes EN-405 AC-4, AC-5, AC-8*
