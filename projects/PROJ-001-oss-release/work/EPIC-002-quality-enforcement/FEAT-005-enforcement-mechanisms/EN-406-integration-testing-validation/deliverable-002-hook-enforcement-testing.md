# TASK-002: Hook Enforcement End-to-End Testing

<!--
TEMPLATE: Task Deliverable
VERSION: 1.1.0
ENABLER: EN-406
AC: AC-2
CREATED: 2026-02-13 (ps-validator-406)
REVISED: 2026-02-14 (ps-revision-406) -- Iteration 1 critique fixes (F-004, F-005, F-006)
PURPOSE: End-to-end test specifications for all hook-based enforcement mechanisms
-->

> **Type:** deliverable
> **Status:** complete
> **Parent:** EN-406-integration-testing-validation
> **AC Mapping:** AC-2 (Hook enforcement mechanisms pass end-to-end testing)
> **Agent:** ps-validator-406
> **Created:** 2026-02-13

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | Test scope for hook enforcement |
| [UserPromptSubmit Hook Tests](#userpromptsubmit-hook-tests) | L2 per-prompt reinforcement tests |
| [PreToolUse Hook Tests](#pretooluse-hook-tests) | L3 pre-action gating tests |
| [SessionStart Hook Tests](#sessionstart-hook-tests) | L1 enhancement tests |
| [Error Handling Tests](#error-handling-tests) | Fail-open and resilience tests |
| [Requirements Traceability](#requirements-traceability) | Test-to-requirement mapping |
| [Test Execution Notes](#test-execution-notes) | Execution guidance |
| [References](#references) | Source documents |

---

## Overview

This document specifies end-to-end test cases for all three hook-based enforcement mechanisms defined in EN-403. Each test case includes preconditions, input, execution steps, expected output, and the requirement(s) it validates. Tests are organized by hook type: UserPromptSubmit (L2), PreToolUse (L3), and SessionStart (L1 enhancement).

### Test Summary

| Hook | Layer | Test Count | Critical Tests |
|------|-------|------------|----------------|
| UserPromptSubmit | L2 | 14 | TC-UPS-001 through TC-UPS-014 |
| PreToolUse | L3 | 16 | TC-PTU-001 through TC-PTU-016 |
| SessionStart | L1 | 10 | TC-SS-001 through TC-SS-010 |
| Error Handling (cross-hook) | All | 3 | TC-ERR-001 through TC-ERR-003 |
| **Total** | | **43** | |

---

## UserPromptSubmit Hook Tests

### Architecture Reference

- **Entry Point:** `hooks/user-prompt-submit.py`
- **Engine:** `src/infrastructure/internal/enforcement/prompt_reinforcement_engine.py`
- **Class:** `PromptReinforcementEngine`
- **Token Budget:** 600 tokens per prompt
- **Output Format:** `<enforcement-context criticality="Cx">...</enforcement-context>`

### TC-UPS-001: Nominal Prompt Reinforcement

| Field | Value |
|-------|-------|
| **ID** | TC-UPS-001 |
| **Objective** | Verify that UserPromptSubmit hook produces enforcement context for a standard prompt |
| **Preconditions** | Hook file exists at `hooks/user-prompt-submit.py`; PromptReinforcementEngine importable |
| **Input** | Standard user prompt: "Add a new method to the WorkItem class" |
| **Steps** | 1. Invoke hook with prompt text. 2. Capture output. 3. Parse XML output. |
| **Expected Output** | XML block `<enforcement-context criticality="C2">` containing quality-gate, constitutional-principles, self-review, scoring-requirement blocks |
| **Pass Criteria** | Output is well-formed XML; criticality attribute present; at least 4 content blocks present |
| **Requirements** | REQ-403-010, REQ-403-011 |
| **Verification** | Inspection + Test |

### TC-UPS-002: C1 Routine Decision - Minimal Reinforcement

| Field | Value |
|-------|-------|
| **ID** | TC-UPS-002 |
| **Objective** | Verify minimal reinforcement for routine (C1) prompts |
| **Preconditions** | PromptReinforcementEngine configured with criticality detection |
| **Input** | Low-criticality prompt: "Fix the typo in the README" |
| **Steps** | 1. Invoke hook with low-criticality prompt. 2. Measure output token count. |
| **Expected Output** | Reduced enforcement content (~200 tokens); criticality="C1" |
| **Pass Criteria** | Output tokens <= 300; criticality correctly identified as C1 |
| **Requirements** | REQ-403-060, REQ-403-061 |
| **Verification** | Test |

### TC-UPS-003: C2 Standard Decision - Standard Reinforcement

| Field | Value |
|-------|-------|
| **ID** | TC-UPS-003 |
| **Objective** | Verify standard reinforcement for C2 prompts |
| **Preconditions** | PromptReinforcementEngine configured |
| **Input** | Standard development prompt: "Implement the repository adapter" |
| **Steps** | 1. Invoke hook. 2. Verify content blocks. 3. Measure tokens. |
| **Expected Output** | Standard enforcement content (~400 tokens); criticality="C2" |
| **Pass Criteria** | Contains quality-gate, constitutional-principles, self-review, scoring-requirement; tokens 200-500 |
| **Requirements** | REQ-403-060, REQ-403-011 |
| **Verification** | Test |

### TC-UPS-004: C3 Significant Decision - Enhanced Reinforcement

| Field | Value |
|-------|-------|
| **ID** | TC-UPS-004 |
| **Objective** | Verify enhanced reinforcement for significant (C3) prompts |
| **Preconditions** | Keyword detection configured for C3 triggers |
| **Input** | Significant prompt: "Modify the .claude/rules/coding-standards.md file" |
| **Steps** | 1. Invoke hook with rules-modifying prompt. 2. Verify enhanced content. |
| **Expected Output** | Enhanced content (~500 tokens); criticality="C3"; steelman and deep-review blocks included |
| **Pass Criteria** | All 7 content blocks present; criticality correctly escalated to C3 |
| **Requirements** | REQ-403-060, REQ-403-061, REQ-403-062 |
| **Verification** | Test |

### TC-UPS-005: C4 Critical Decision - Full Reinforcement

| Field | Value |
|-------|-------|
| **ID** | TC-UPS-005 |
| **Objective** | Verify full reinforcement for critical (C4) prompts |
| **Preconditions** | Keyword detection configured for C4 triggers |
| **Input** | Critical prompt: "Update the JERRY_CONSTITUTION.md governance document" |
| **Steps** | 1. Invoke hook with governance-critical prompt. 2. Verify maximum content. |
| **Expected Output** | Maximum enforcement content (~600 tokens); criticality="C4"; all 7 blocks present with maximum detail |
| **Pass Criteria** | Token count at budget ceiling (~600); all content blocks at maximum detail; criticality="C4" |
| **Requirements** | REQ-403-060, REQ-403-062 |
| **Verification** | Test |

### TC-UPS-006: Token Budget Enforcement

| Field | Value |
|-------|-------|
| **ID** | TC-UPS-006 |
| **Objective** | Verify that output never exceeds 600 token budget |
| **Preconditions** | PromptReinforcementEngine with TOKEN_BUDGET = 600 |
| **Input** | 10 prompts across all criticality levels (see test data below) |
| **Steps** | 1. Run hook for each prompt. 2. Measure output tokens using chars/4 approximation. |
| **Expected Output** | All outputs <= 600 tokens |
| **Pass Criteria** | No output exceeds 600 tokens; average output within expected range per criticality |
| **Requirements** | REQ-403-012, REQ-403-013 |
| **Verification** | Test |

**Test Data (10 prompts):**

| # | Prompt | Expected Criticality | Expected Token Range |
|---|--------|---------------------|---------------------|
| 1 | "Fix the typo in README.md" | C1 | <= 300 |
| 2 | "Update the docstring on this function" | C1 | <= 300 |
| 3 | "Add a unit test for the Priority value object" | C1 | <= 300 |
| 4 | "Implement the repository adapter for WorkItem" | C2 | 200-500 |
| 5 | "Refactor the command handler to use dependency injection" | C2 | 200-500 |
| 6 | "Add a new domain event for task completion" | C2 | 200-500 |
| 7 | "Modify the .claude/rules/coding-standards.md file" | C3 | 400-600 |
| 8 | "Update the architecture-standards.md with new layer rules" | C3 | 400-600 |
| 9 | "Update the JERRY_CONSTITUTION.md governance document" | C4 | 500-600 |
| 10 | "Modify docs/governance/JERRY_CONSTITUTION.md to add a new principle" | C4 | 500-600 |

### TC-UPS-007: Adaptive Content Selection

| Field | Value |
|-------|-------|
| **ID** | TC-UPS-007 |
| **Objective** | Verify content blocks are selected adaptively based on prompt keywords |
| **Preconditions** | Keyword-to-content mapping configured |
| **Input** | Prompt mentioning "architecture": "Design the hexagonal architecture for the new module" |
| **Steps** | 1. Invoke hook. 2. Verify architecture-relevant blocks prioritized. 3. Cross-reference against keyword-to-content mapping below. |
| **Expected Output** | Architecture-relevant content blocks (e.g., steelman, deep-review) included before generic blocks |
| **Pass Criteria** | Content selection demonstrates keyword sensitivity per mapping table |
| **Requirements** | REQ-403-014, REQ-403-015 |
| **Verification** | Inspection |

**Keyword-to-Content Block Mapping:**

| Keyword Category | Example Keywords | Expected Content Blocks |
|-----------------|------------------|------------------------|
| Architecture | "hexagonal", "architecture", "layer", "boundary" | steelman, deep-review, constitutional-principles |
| Governance | "constitution", "governance", "principle" | constitutional-principles, scoring-requirement, deep-review |
| Testing | "test", "coverage", "pytest" | quality-gate, scoring-requirement |
| Refactoring | "refactor", "restructure", "reorganize" | steelman, quality-gate, self-review |
| Rules/Config | "rules", "standards", "configuration" | constitutional-principles, leniency-calibration, deep-review |
| General Development | (default, no specific keywords) | quality-gate, self-review, scoring-requirement |

### TC-UPS-008: Empty Prompt Handling

| Field | Value |
|-------|-------|
| **ID** | TC-UPS-008 |
| **Objective** | Verify graceful handling of empty or whitespace-only prompts |
| **Preconditions** | Hook deployed |
| **Input** | Empty string "" and whitespace "   " |
| **Steps** | 1. Invoke hook with empty/whitespace prompt. 2. Observe behavior. |
| **Expected Output** | Minimal reinforcement or no-op; no crash; no error |
| **Pass Criteria** | Hook returns valid output (possibly empty); exit code 0 |
| **Requirements** | REQ-403-070, REQ-403-071 |
| **Verification** | Test |

### TC-UPS-009: Very Long Prompt Handling

| Field | Value |
|-------|-------|
| **ID** | TC-UPS-009 |
| **Objective** | Verify handling of extremely long prompts |
| **Preconditions** | Hook deployed |
| **Input** | Prompt with 10,000+ characters |
| **Steps** | 1. Invoke hook with long prompt. 2. Verify output and performance. |
| **Expected Output** | Normal enforcement output; no truncation errors; output still <= 600 tokens |
| **Pass Criteria** | Correct output; no timeout; no crash |
| **Requirements** | REQ-403-070, REQ-403-012 |
| **Verification** | Test |

### TC-UPS-010: V-024 Content Block Integrity

| Field | Value |
|-------|-------|
| **ID** | TC-UPS-010 |
| **Objective** | Verify all 7 V-024 content blocks are well-formed |
| **Preconditions** | PromptReinforcementEngine with all content blocks configured |
| **Input** | C4 prompt (to trigger all blocks) |
| **Steps** | 1. Invoke hook with C4 prompt. 2. Parse XML output. 3. Validate each block. |
| **Expected Output** | 7 blocks present: quality-gate, constitutional-principles, self-review, scoring-requirement, steelman, leniency-calibration, deep-review |
| **Pass Criteria** | All 7 blocks are valid XML elements with non-empty content |
| **Requirements** | REQ-403-011, REQ-403-016 |
| **Verification** | Inspection |

### TC-UPS-011: Criticality Detection Accuracy

| Field | Value |
|-------|-------|
| **ID** | TC-UPS-011 |
| **Objective** | Verify criticality level detection accuracy across prompt types |
| **Preconditions** | Criticality keyword mapping configured |
| **Input** | 4 prompts, one per criticality level (C1 through C4) |
| **Steps** | 1. Invoke hook for each prompt. 2. Extract criticality attribute. 3. Compare to expected. |
| **Expected Output** | C1: routine tasks. C2: standard development. C3: rule/config changes. C4: governance/constitution. |
| **Pass Criteria** | All 4 criticality levels correctly detected |
| **Requirements** | REQ-403-060, REQ-403-061, REQ-403-062 |
| **Verification** | Test |

### TC-UPS-012: XML Output Well-formedness

| Field | Value |
|-------|-------|
| **ID** | TC-UPS-012 |
| **Objective** | Verify all output is well-formed XML parseable by standard parsers |
| **Preconditions** | Hook deployed |
| **Input** | 5 diverse prompts |
| **Steps** | 1. Invoke hook for each prompt. 2. Parse output with XML parser. |
| **Expected Output** | All outputs parse successfully as XML |
| **Pass Criteria** | Zero XML parsing errors |
| **Requirements** | REQ-403-017 |
| **Verification** | Test |

### TC-UPS-013: Concurrent Prompt Handling

| Field | Value |
|-------|-------|
| **ID** | TC-UPS-013 |
| **Objective** | Verify hook handles rapid sequential invocations |
| **Preconditions** | Hook deployed |
| **Input** | 5 prompts submitted in rapid succession |
| **Steps** | 1. Invoke hook 5 times with minimal delay. 2. Verify each output is correct. |
| **Expected Output** | Each invocation produces independent, correct output |
| **Pass Criteria** | No state leakage between invocations; all outputs valid |
| **Requirements** | REQ-403-018 |
| **Verification** | Test |

### TC-UPS-014: Adversarial Strategy Encoding in L2

| Field | Value |
|-------|-------|
| **ID** | TC-UPS-014 |
| **Objective** | Verify L2 output includes relevant adversarial strategy references |
| **Preconditions** | Content blocks include strategy references |
| **Input** | C3+ prompt triggering strategy-relevant content |
| **Steps** | 1. Invoke hook with C3 prompt. 2. Check for strategy references. |
| **Expected Output** | At least one adversarial strategy reference (S-xxx) in output |
| **Pass Criteria** | Strategy references present and correctly formatted |
| **Requirements** | REQ-403-090, REQ-403-091 |
| **Verification** | Inspection |

---

## PreToolUse Hook Tests

### Architecture Reference

- **Entry Point:** `hooks/pre-tool-use.py`
- **Engine:** `src/infrastructure/internal/enforcement/pre_tool_enforcement_engine.py`
- **Class:** `PreToolEnforcementEngine`
- **Methods:** `evaluate_write()`, `evaluate_edit()`
- **Performance Budget:** < 87ms total
- **Output:** `EnforcementDecision` dataclass (action, reason, violations, criticality_escalation)

### TC-PTU-001: Valid Write to Domain Layer

| Field | Value |
|-------|-------|
| **ID** | TC-PTU-001 |
| **Objective** | Verify approval of valid write operations to domain layer |
| **Input** | Write to `src/domain/entities/task.py` with valid domain-only imports |
| **Expected Output** | EnforcementDecision(action="approve") |
| **Requirements** | REQ-403-030, REQ-403-031 |
| **Verification** | Test |

### TC-PTU-002: Import Boundary Violation (V-038)

| Field | Value |
|-------|-------|
| **ID** | TC-PTU-002 |
| **Objective** | Verify blocking of import boundary violations |
| **Input** | Write to `src/domain/entities/task.py` with `from src.infrastructure.adapters import X` |
| **Expected Output** | EnforcementDecision(action="block", violations=["V-038: domain imports infrastructure"]) |
| **Requirements** | REQ-403-032, REQ-403-033 |
| **Verification** | Test |

### TC-PTU-003: One-Class-Per-File Violation (V-041)

| Field | Value |
|-------|-------|
| **ID** | TC-PTU-003 |
| **Objective** | Verify blocking of files with multiple public classes |
| **Input** | Write to `src/domain/entities/task.py` with 2 public class definitions |
| **Expected Output** | EnforcementDecision(action="block", violations=["V-041: multiple public classes"]) |
| **Requirements** | REQ-403-034, REQ-403-035 |
| **Verification** | Test |

### TC-PTU-004: Governance File Escalation - Constitution

| Field | Value |
|-------|-------|
| **ID** | TC-PTU-004 |
| **Objective** | Verify criticality escalation to C4 for governance files |
| **Input** | Write to `docs/governance/JERRY_CONSTITUTION.md` |
| **Expected Output** | EnforcementDecision(action="approve", criticality_escalation="C4") or block depending on content |
| **Requirements** | REQ-403-036, REQ-403-062 |
| **Verification** | Test |

### TC-PTU-005: Governance File Escalation - Rules

| Field | Value |
|-------|-------|
| **ID** | TC-PTU-005 |
| **Objective** | Verify criticality escalation to C3 for rule files |
| **Input** | Write to `.claude/rules/coding-standards.md` |
| **Expected Output** | EnforcementDecision(criticality_escalation="C3") |
| **Requirements** | REQ-403-036, REQ-403-061 |
| **Verification** | Test |

### TC-PTU-006: Phase Execution Order

| Field | Value |
|-------|-------|
| **ID** | TC-PTU-006 |
| **Objective** | Verify 5 phases execute in correct order |
| **Input** | Any write operation with logging enabled |
| **Expected Output** | Phases execute: P1 (security) -> P2 (patterns) -> P3 (AST) -> P4 (governance) -> P5 (approve) |
| **Requirements** | REQ-403-037 |
| **Verification** | Inspection |

### TC-PTU-007: Performance Budget - Single Evaluation

| Field | Value |
|-------|-------|
| **ID** | TC-PTU-007 |
| **Objective** | Verify total evaluation time < 87ms |
| **Input** | Write to domain file with valid content |
| **Steps** | 1. Time evaluate_write() call. 2. Repeat 100 times. 3. Compute p95 latency. |
| **Expected Output** | p95 latency < 87ms |
| **Requirements** | REQ-403-038 |
| **Verification** | Test |

### TC-PTU-008: Performance Budget - Complex AST

| Field | Value |
|-------|-------|
| **ID** | TC-PTU-008 |
| **Objective** | Verify performance with complex Python file requiring full AST parsing |
| **Input** | Write with 500+ line Python file |
| **Steps** | 1. Time evaluation. 2. Verify still < 87ms. |
| **Expected Output** | Total time < 87ms even for complex files |
| **Requirements** | REQ-403-038 |
| **Verification** | Test |

### TC-PTU-009: Edit Operation - Valid Modification

| Field | Value |
|-------|-------|
| **ID** | TC-PTU-009 |
| **Objective** | Verify evaluate_edit() approves valid edits |
| **Input** | Edit to `src/application/handlers/commands/create_task_handler.py` with valid imports |
| **Expected Output** | EnforcementDecision(action="approve") |
| **Requirements** | REQ-403-030 |
| **Verification** | Test |

### TC-PTU-010: Edit Operation - Introducing Violation

| Field | Value |
|-------|-------|
| **ID** | TC-PTU-010 |
| **Objective** | Verify evaluate_edit() blocks edits that introduce violations |
| **Input** | Edit adding `from src.interface.cli import main` to `src/domain/entities/task.py` |
| **Expected Output** | EnforcementDecision(action="block", violations=["V-038"]) |
| **Requirements** | REQ-403-032 |
| **Verification** | Test |

### TC-PTU-011: Non-Python File - Pass Through

| Field | Value |
|-------|-------|
| **ID** | TC-PTU-011 |
| **Objective** | Verify non-Python files bypass AST validation |
| **Input** | Write to `README.md` |
| **Expected Output** | EnforcementDecision(action="approve") - AST phases skipped |
| **Requirements** | REQ-403-039 |
| **Verification** | Test |

### TC-PTU-012: File Outside Source Tree

| Field | Value |
|-------|-------|
| **ID** | TC-PTU-012 |
| **Objective** | Verify files outside `src/` bypass architecture validation |
| **Input** | Write to `scripts/helper.py` |
| **Expected Output** | EnforcementDecision(action="approve") - architecture validation skipped |
| **Requirements** | REQ-403-039 |
| **Verification** | Test |

### TC-PTU-013: Multiple Violations in Single File

| Field | Value |
|-------|-------|
| **ID** | TC-PTU-013 |
| **Objective** | Verify all violations are reported, not just the first |
| **Input** | Write to domain file with both import violation AND multiple public classes |
| **Expected Output** | EnforcementDecision(action="block", violations=["V-038", "V-041"]) |
| **Requirements** | REQ-403-032, REQ-403-034 |
| **Verification** | Test |

### TC-PTU-014: Error Resilience - Malformed Python

| Field | Value |
|-------|-------|
| **ID** | TC-PTU-014 |
| **Objective** | Verify fail-open on unparseable Python |
| **Input** | Write with syntax error in content |
| **Expected Output** | EnforcementDecision(action="approve") with warning about parse failure |
| **Requirements** | REQ-403-070 |
| **Verification** | Test |

### TC-PTU-015: Error Resilience - Missing Engine Module

| Field | Value |
|-------|-------|
| **ID** | TC-PTU-015 |
| **Objective** | Verify fail-open when engine module cannot be imported |
| **Input** | Hook invoked but engine module missing |
| **Expected Output** | Fail-open: tool use approved with no enforcement |
| **Requirements** | REQ-403-070, REQ-403-071 |
| **Verification** | Test |

### TC-PTU-016: Zero Token Cost Verification

| Field | Value |
|-------|-------|
| **ID** | TC-PTU-016 |
| **Objective** | Verify PreToolUse adds zero tokens to context |
| **Input** | Any tool use |
| **Steps** | 1. Capture conversation context size before PreToolUse invocation. 2. Invoke PreToolUse hook. 3. Capture conversation context size after invocation. 4. Compute delta. |
| **Expected Output** | No text appended to conversation context; enforcement is side-channel only; context size delta = 0 tokens |
| **Pass Criteria** | Measured token cost delta is 0; PreToolUse hook returns EnforcementDecision via side-channel (not context injection) |
| **Requirements** | REQ-403-031 |
| **Verification** | Test |

---

## SessionStart Hook Tests

### Architecture Reference

- **Entry Point:** `scripts/session_start_hook.py`
- **Generator:** `src/infrastructure/internal/enforcement/session_quality_context.py`
- **Class:** `SessionQualityContextGenerator`
- **Token Budget:** ~435 calibrated tokens (~2,096 characters)
- **Integration Point:** After `format_hook_output()`, before `output_json()`

### TC-SS-001: Nominal Preamble Generation

| Field | Value |
|-------|-------|
| **ID** | TC-SS-001 |
| **Objective** | Verify SessionQualityContextGenerator produces complete preamble |
| **Input** | Call `SessionQualityContextGenerator.generate()` |
| **Expected Output** | 4-section XML: `<quality-gate>`, `<constitutional-principles>`, `<adversarial-strategies>`, `<decision-criticality>` |
| **Pass Criteria** | All 4 sections present; well-formed XML |
| **Requirements** | FR-405-001, FR-405-002, FR-405-003, FR-405-004 |
| **Verification** | Test |

### TC-SS-002: Quality Gate Section Content

| Field | Value |
|-------|-------|
| **ID** | TC-SS-002 |
| **Objective** | Verify quality-gate section contains required content |
| **Input** | Generated preamble |
| **Expected Output** | Contains: scoring criteria, >= 0.92 threshold, mandatory self-review instruction |
| **Pass Criteria** | All required content elements present |
| **Requirements** | FR-405-005, FR-405-006 |
| **Verification** | Inspection |

### TC-SS-003: Constitutional Principles Section Content

| Field | Value |
|-------|-------|
| **ID** | TC-SS-003 |
| **Objective** | Verify constitutional-principles section contains P-003, P-020, P-022 |
| **Input** | Generated preamble |
| **Expected Output** | Contains references to all 3 hard constraints: P-003 (No Recursive Subagents), P-020 (User Authority), P-022 (No Deception) |
| **Pass Criteria** | All 3 principles referenced with correct descriptions |
| **Requirements** | FR-405-007, FR-405-008 |
| **Verification** | Inspection |

### TC-SS-004: Adversarial Strategies Section Content

| Field | Value |
|-------|-------|
| **ID** | TC-SS-004 |
| **Objective** | Verify adversarial-strategies section contains 10 strategies with context rot awareness |
| **Input** | Generated preamble |
| **Expected Output** | 10 strategies from S-001 through S-014 subset; context rot mitigation guidance |
| **Pass Criteria** | Strategy count = 10; context rot awareness included |
| **Requirements** | FR-405-009, FR-405-010, SR-405-001 |
| **Verification** | Inspection |

### TC-SS-005: Decision Criticality Section Content

| Field | Value |
|-------|-------|
| **ID** | TC-SS-005 |
| **Objective** | Verify decision-criticality section contains C1-C4 levels and auto-escalate rules |
| **Input** | Generated preamble |
| **Expected Output** | C1 (Routine), C2 (Standard), C3 (Significant), C4 (Critical); AE-001 through AE-004 |
| **Pass Criteria** | All 4 levels defined; all 4 auto-escalate rules present |
| **Requirements** | FR-405-011, FR-405-012 |
| **Verification** | Inspection |

### TC-SS-006: Token Budget Compliance

| Field | Value |
|-------|-------|
| **ID** | TC-SS-006 |
| **Objective** | Verify preamble stays within token budget |
| **Input** | Generated preamble |
| **Steps** | 1. Measure character count. 2. Apply chars/4 approximation. 3. Apply 0.83x XML calibration. |
| **Expected Output** | Characters <= ~2,096; conservative tokens <= ~524; calibrated tokens <= ~435 |
| **Pass Criteria** | Within budget at all measurement levels |
| **Requirements** | PR-405-001, PR-405-002 |
| **Verification** | Test |

### TC-SS-007: Integration with SessionStart Output

| Field | Value |
|-------|-------|
| **ID** | TC-SS-007 |
| **Objective** | Verify preamble integrates correctly with existing SessionStart hook output |
| **Input** | Full session start execution |
| **Steps** | 1. Execute session_start_hook.py. 2. Verify output contains both project context AND quality preamble. |
| **Expected Output** | Output contains `<project-context>` tags AND quality preamble XML sections |
| **Pass Criteria** | Both existing and new content present; no corruption of existing output |
| **Requirements** | IR-405-001, IR-405-002 |
| **Verification** | Test + Inspection |

### TC-SS-008: Graceful Degradation - Missing Module

| Field | Value |
|-------|-------|
| **ID** | TC-SS-008 |
| **Objective** | Verify session starts normally when quality module unavailable |
| **Input** | Session start with quality module import failing |
| **Steps** | 1. Simulate import failure (rename module). 2. Execute session start. 3. Verify QUALITY_CONTEXT_AVAILABLE = False. |
| **Expected Output** | Session starts successfully; existing functionality unaffected; QUALITY_CONTEXT_AVAILABLE = False |
| **Pass Criteria** | No crash; existing output intact; quality preamble absent but session functional |
| **Requirements** | EH-405-001, EH-405-002 |
| **Verification** | Test |

### TC-SS-009: Preamble Content Accuracy

| Field | Value |
|-------|-------|
| **ID** | TC-SS-009 |
| **Objective** | Verify generated preamble matches specification in EN-405 TASK-006 |
| **Input** | Generated preamble vs. TASK-006 reference content |
| **Steps** | 1. Generate preamble. 2. Compare against TASK-006 exact content. |
| **Expected Output** | Content matches or is semantically equivalent to TASK-006 specification |
| **Pass Criteria** | All key phrases, values, and structure match specification |
| **Requirements** | FR-405-013 |
| **Verification** | Inspection |

### TC-SS-010: L1-L2 Coordination Verification

| Field | Value |
|-------|-------|
| **ID** | TC-SS-010 |
| **Objective** | Verify SessionStart (comprehensive, once) complements UserPromptSubmit (compact, per-prompt) |
| **Input** | Session start output + subsequent prompt reinforcement output |
| **Steps** | 1. Capture session start output. 2. Invoke UserPromptSubmit. 3. Compare content overlap. |
| **Expected Output** | Session start provides comprehensive quality context; UserPromptSubmit provides compact reinforcement without redundant duplication |
| **Pass Criteria** | Content is complementary, not duplicative; L2 is compact subset of L1 themes |
| **Requirements** | IR-405-003, IR-405-004 |
| **Verification** | Inspection |

---

## Error Handling Tests

### TC-ERR-001: Hook Crash Recovery

| Field | Value |
|-------|-------|
| **ID** | TC-ERR-001 |
| **Objective** | Verify all hooks fail-open on unexpected exceptions |
| **Scope** | All 3 hooks |
| **Input** | Force each hook to raise an unhandled exception |
| **Expected Output** | Each hook allows the operation to proceed; no user-facing error |
| **Requirements** | REQ-403-070, REQ-403-071 |

### TC-ERR-002: Timeout Handling

| Field | Value |
|-------|-------|
| **ID** | TC-ERR-002 |
| **Objective** | Verify hooks handle timeout gracefully |
| **Scope** | UserPromptSubmit and PreToolUse |
| **Input** | Simulate slow operation exceeding timeout |
| **Expected Output** | Fail-open; operation proceeds without enforcement |
| **Requirements** | REQ-403-072, REQ-403-073 |

### TC-ERR-003: Invalid Input Handling

| Field | Value |
|-------|-------|
| **ID** | TC-ERR-003 |
| **Objective** | Verify hooks handle invalid/unexpected input formats |
| **Scope** | All 3 hooks |
| **Input** | Malformed JSON, binary data, null values |
| **Expected Output** | Fail-open; no crash; appropriate logging |
| **Requirements** | REQ-403-070 |

---

## Requirements Traceability

| Test ID | Requirements Verified |
|---------|----------------------|
| TC-UPS-001 | REQ-403-010, REQ-403-011 |
| TC-UPS-002 | REQ-403-060, REQ-403-061 |
| TC-UPS-003 | REQ-403-060, REQ-403-011 |
| TC-UPS-004 | REQ-403-060, REQ-403-061, REQ-403-062 |
| TC-UPS-005 | REQ-403-060, REQ-403-062 |
| TC-UPS-006 | REQ-403-012, REQ-403-013 |
| TC-UPS-007 | REQ-403-014, REQ-403-015 |
| TC-UPS-008 | REQ-403-070, REQ-403-071 |
| TC-UPS-009 | REQ-403-070, REQ-403-012 |
| TC-UPS-010 | REQ-403-011, REQ-403-016 |
| TC-UPS-011 | REQ-403-060, REQ-403-061, REQ-403-062 |
| TC-UPS-012 | REQ-403-017 |
| TC-UPS-013 | REQ-403-018 |
| TC-UPS-014 | REQ-403-090, REQ-403-091 |
| TC-PTU-001 | REQ-403-030, REQ-403-031 |
| TC-PTU-002 | REQ-403-032, REQ-403-033 |
| TC-PTU-003 | REQ-403-034, REQ-403-035 |
| TC-PTU-004 | REQ-403-036, REQ-403-062 |
| TC-PTU-005 | REQ-403-036, REQ-403-061 |
| TC-PTU-006 | REQ-403-037 |
| TC-PTU-007 | REQ-403-038 |
| TC-PTU-008 | REQ-403-038 |
| TC-PTU-009 | REQ-403-030 |
| TC-PTU-010 | REQ-403-032 |
| TC-PTU-011 | REQ-403-039 |
| TC-PTU-012 | REQ-403-039 |
| TC-PTU-013 | REQ-403-032, REQ-403-034 |
| TC-PTU-014 | REQ-403-070 |
| TC-PTU-015 | REQ-403-070, REQ-403-071 |
| TC-PTU-016 | REQ-403-031 |
| TC-SS-001 | FR-405-001 through FR-405-004 |
| TC-SS-002 | FR-405-005, FR-405-006 |
| TC-SS-003 | FR-405-007, FR-405-008 |
| TC-SS-004 | FR-405-009, FR-405-010, SR-405-001 |
| TC-SS-005 | FR-405-011, FR-405-012 |
| TC-SS-006 | PR-405-001, PR-405-002 |
| TC-SS-007 | IR-405-001, IR-405-002 |
| TC-SS-008 | EH-405-001, EH-405-002 |
| TC-SS-009 | FR-405-013 |
| TC-SS-010 | IR-405-003, IR-405-004 |
| TC-ERR-001 | REQ-403-070, REQ-403-071 |
| TC-ERR-002 | REQ-403-072, REQ-403-073 |
| TC-ERR-003 | REQ-403-070 |

---

## Test Execution Notes

1. **Design Phase:** These are test SPECIFICATIONS, not executable test scripts. They define what must be tested when enforcement mechanisms are implemented.
2. **Priority:** TC-PTU tests are highest priority as L3 is the most critical enforcement layer (context-rot immune, deterministic blocking).
3. **Automation Target:** All TC-PTU tests should be automated as pytest tests in `tests/integration/test_pre_tool_enforcement.py`.
4. **Manual Verification:** TC-UPS and TC-SS tests requiring inspection of Claude Code behavior will require manual verification or mock-based testing.
5. **Fail-Open Principle:** All error handling tests (TC-ERR) validate the fail-open requirement (REQ-403-070).

---

## References

| Document | Path | Relevance |
|----------|------|-----------|
| EN-403 TASK-001 | `../EN-403-hook-based-enforcement/TASK-001-hook-requirements.md` | 44 hook requirements |
| EN-403 TASK-002 | `../EN-403-hook-based-enforcement/TASK-002-userpromptsubmit-design.md` | UserPromptSubmit design |
| EN-403 TASK-003 | `../EN-403-hook-based-enforcement/TASK-003-pretooluse-design.md` | PreToolUse design |
| EN-403 TASK-004 | `../EN-403-hook-based-enforcement/TASK-004-sessionstart-design.md` | SessionStart design |
| EN-405 TASK-001 | `../EN-405-session-context-enforcement/TASK-001-requirements.md` | Session context requirements |
| EN-405 TASK-006 | `../EN-405-session-context-enforcement/TASK-006-preamble-content.md` | Exact preamble content |
| TASK-001 Integration Test Plan | `TASK-001-integration-test-plan.md` | Master test plan |

---

*Generated by ps-validator-406 | 2026-02-13 | EN-406 AC-2*
