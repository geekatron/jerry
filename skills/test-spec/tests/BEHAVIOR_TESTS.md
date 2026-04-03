# Behavior Tests: /test-spec Skill

> **File ID:** F-15 | **Skill:** /test-spec | **Version:** 1.0.0
> **Author:** eng-backend | **Date:** 2026-03-09 | **Criticality:** C3
> **Status:** PROPOSED
> **Standard:** H-20 (BDD test-first), H-23 (navigation table required)
> **Schema:** `docs/schemas/test-specification-v1.schema.json` (v1.0.0)
> **Rules:** `skills/test-spec/rules/clark-transformation-rules.md` (RULE-IV through RULE-QA)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | Scope, methodology, test fixtures, coverage summary |
| [Coverage Matrix](#coverage-matrix) | Implementation files and rules covered per scenario |
| [Feature: tspec-generator Agent](#feature-tspec-generator-agent) | Clark transformation and Feature file generation scenarios |
| [Scenario G-001: Happy Path Generation](#scenario-g-001-happy-path-generation) | Full UC → Feature file, 100% coverage |
| [Scenario G-002: detail_level Rejection Gate](#scenario-g-002-detail_level-rejection-gate) | RULE-IV-01: BRIEFLY_DESCRIBED rejected |
| [Scenario G-003: Basic Flow Happy Path Mapping](#scenario-g-003-basic-flow-happy-path-mapping) | RULE-C3-01: All steps → single Scenario |
| [Scenario G-004: Extension Failure Scenario Mapping](#scenario-g-004-extension-failure-scenario-mapping) | RULE-C5-01 + RULE-OT-01: outcome=failure → negative scenario |
| [Scenario G-005: Slice-Scoped Generation](#scenario-g-005-slice-scoped-generation) | RULE-SL-01: slice_id filters flows |
| [Feature: tspec-analyst Agent](#feature-tspec-analyst-agent) | Coverage computation and gap identification scenarios |
| [Scenario A-001: Coverage Computation Happy Path](#scenario-a-001-coverage-computation-happy-path) | 7 Cs C1: Coverage = mapped / total |
| [Scenario A-002: Gap Identification for Unmapped Extension](#scenario-a-002-gap-identification-for-unmapped-extension) | Analyst detects and prioritizes unmapped flows |
| [Feature: Cross-Agent Pipeline](#feature-cross-agent-pipeline) | End-to-end pipeline integration scenario |
| [Scenario E-001: Generator-to-Analyst Pipeline](#scenario-e-001-generator-to-analyst-pipeline) | Feature file consumed by analyst, frontmatter parsed |
| [Acceptance Verification Checklist](#acceptance-verification-checklist) | Reviewer checklist for F-15 completeness |

---

## Overview

This file defines the BDD behavior test specifications for the `/test-spec` skill per H-20 (BDD test-first) and the architecture specification. All scenarios are written in full Gherkin format (Feature / Scenario / Given / When / Then) with concrete inputs and verifiable assertions, covering the minimum 7 scenario requirement from the architecture document.

### Scope

| In Scope | Out of Scope | Rationale for Out of Scope |
|----------|-------------|---------------------------|
| tspec-generator Clark transformation correctness | /use-case skill (uc-author) | Separate skill with separate test file |
| tspec-generator input validation gate (RULE-IV-01 through RULE-IV-04) | Python pytest execution (no Python implementation) | /test-spec is a pure markdown/YAML skill; H-20 BDD applies, H-21 line coverage is N/A |
| tspec-analyst coverage computation (7 Cs, C1 primary) | Network/MCP integration | Both agents are T2 with no network access by design |
| tspec-analyst gap identification and prioritization | SAST/DAST scanning | /test-spec produces documentation artifacts, not deployable code |
| Slice-scoped Feature file generation (RULE-SL-01, RULE-SL-02) | Cucumber/Gherkin runner execution | Feature files are Markdown containers; execution toolchain is out of scope |
| Cross-agent pipeline: generator output → analyst input | Registration in CLAUDE.md / AGENTS.md | That is eng-reviewer scope (FIND-003 carryforward) |
| JSON Schema validation of Feature file frontmatter | Alternative flow mapping (no alternative_flows in sample UC) | Clark alternative flow mapping is structurally identical to extension mapping; verified via RULE-C4-01 review |

### Methodology

All scenarios follow Gherkin BDD format:

```
Feature: [agent or subsystem]
  Background: [shared setup for all scenarios in feature, if applicable]
  Scenario: [concrete scenario name -- Scenario ID in title for traceability]
    Given [precondition -- observable system state or artifact state]
    When  [trigger -- agent invocation or validation action]
    Then  [assertion -- observable verifiable outcome]
    And   [additional assertion]
```

Scenarios are organized into three Features: `tspec-generator Agent`, `tspec-analyst Agent`, and `Cross-Agent Pipeline`. Within each Feature, scenarios are ordered from happy path through negative cases to edge cases. Coverage distribution: 22% happy path (2 scenarios), 34% negative (3 scenarios), 44% edge cases (4 scenarios).

### Test Fixtures

| Fixture ID | Description | Defined In |
|-----------|-------------|------------|
| FX-01 | UC-LIB-001 at ESSENTIAL_OUTLINE with 5 basic_flow steps (typed) + 3 extensions (EXT-2A failure, EXT-2B failure, EXT-3A failure) | Inline in G-001 |
| FX-02 | UC-LIB-001 at BRIEFLY_DESCRIBED (insufficient for Clark transformation) | Inline in G-002 |
| FX-03 | Feature file produced from FX-01 with 4 scenarios and correct YAML frontmatter | Inline in A-001, E-001 |
| FX-04 | UC-LIB-001 at ESSENTIAL_OUTLINE with slice-001 scoping steps 1-3 only (1 basic_flow, 1 extension) | Inline in G-005 |
| FX-05 | Feature file with only 1 scenario (basic_flow) -- missing 3 extension mappings | Inline in A-002 |

---

## Coverage Matrix

| Scenario | File Under Test | Rules / Standards Covered |
|----------|----------------|---------------------------|
| G-001 | tspec-generator.md, clark-transformation-rules.md | RULE-C1-01, RULE-C2-01, RULE-C3-01, RULE-C5-01, RULE-C7-01, RULE-QA-01, RULE-QA-04 |
| G-002 | tspec-generator.md | RULE-IV-01, guardrails.input_validation |
| G-003 | tspec-generator.md, clark-transformation-rules.md | RULE-C3-01, RULE-C3-02, RULE-ST-01, RULE-ST-02, RULE-ST-03 |
| G-004 | tspec-generator.md, clark-transformation-rules.md | RULE-C5-01, RULE-OT-01, RULE-QA-02 |
| G-005 | tspec-generator.md, clark-transformation-rules.md | RULE-SL-01, RULE-SL-02, frontmatter slice_id field |
| A-001 | tspec-analyst.md | 7 Cs C1 (Coverage), coverage formula: mapped/total |
| A-002 | tspec-analyst.md | Gap identification, failure extension prioritization |
| E-001 | tspec-generator.md, tspec-analyst.md, test-specification-v1.schema.json | Cross-agent frontmatter contract, YAML traceability, P-003 compliance |

---

## Feature: tspec-generator Agent

```gherkin
Feature: tspec-generator Agent -- Clark UC2.0-to-Gherkin Transformation

  Background:
    Given the tspec-generator agent is available with tools: Read, Write, Edit, Glob, Grep, Bash
    And clark-transformation-rules.md is accessible at skills/test-spec/rules/clark-transformation-rules.md
    And bdd-scenario.template.md is accessible at skills/test-spec/templates/bdd-scenario.template.md
```

---

### Scenario G-001: Happy Path Generation

**Clark rules exercised:** RULE-IV-01 (pass), RULE-C1-01, RULE-C2-01, RULE-C3-01, RULE-C5-01, RULE-C7-01, RULE-QA-01, RULE-QA-04

**Assertion rationale:** Verifies the full Clark transformation pipeline from a valid ESSENTIAL_OUTLINE UC to a Feature file with correct frontmatter, 4 scenarios (1 happy path + 3 extensions), Source annotations, and Traceability Matrix.

```gherkin
Scenario: G-001 -- Full UC generates Feature file with 100% coverage

  Given a use case artifact UC-LIB-001 exists with:
    | Field          | Value                        |
    | id             | UC-LIB-001                   |
    | title          | Borrow a Book                |
    | detail_level   | ESSENTIAL_OUTLINE            |
    | goal_level     | USER_GOAL                    |
    | primary_actor  | Library Member               |
    | basic_flow     | 5 steps (typed: actor_action, validation, validation, actor_action, system_response) |
    | alternative_flows | [] (empty)                |
    | extensions     | EXT-2A (failure), EXT-2B (failure), EXT-3A (failure) |
  And the output path is projects/${JERRY_PROJECT}/test-specs/UC-LIB-001-borrow-a-book.feature.md

  When tspec-generator is invoked with input UC-LIB-001 and no slice_id

  Then a Feature file is written at the output path
  And the Feature file YAML frontmatter contains:
    | Field                | Expected Value        |
    | source_use_case      | UC-LIB-001            |
    | source_title         | Borrow a Book         |
    | source_detail_level  | ESSENTIAL_OUTLINE     |
    | source_goal_level    | USER_GOAL             |
    | generated_by         | tspec-generator       |
    | scenario_count       | 4                     |
    | slice_id             | null                  |
    | coverage.basic_flow_mapped | true            |
    | coverage.extensions_mapped | 3               |
    | coverage.total_flows | 4                     |
    | coverage.mapped_flows | 4                    |
  And the Feature file contains exactly 1 scenario in the Happy Path section
  And the Feature file contains exactly 3 scenarios in the Error Scenarios section
  And each scenario contains a "**Source:**" annotation line immediately after the Scenario title
  And a Traceability Matrix section is present with 4 rows (1 happy_path + 3 error rows)
  And tspec-generator reports: "scenario_count=4, coverage=100%, 4/4 flows mapped"
```

---

### Scenario G-002: detail_level Rejection Gate

**Clark rule exercised:** RULE-IV-01 (rejection path)

**Assertion rationale:** Verifies that RULE-IV-01 halts processing when the source UC is at BRIEFLY_DESCRIBED level, producing an informative rejection message and NO partial output.

```gherkin
Scenario: G-002 -- UC at BRIEFLY_DESCRIBED is rejected before Clark transformation begins

  Given a use case artifact UC-LIB-001 exists with:
    | Field        | Value             |
    | id           | UC-LIB-001        |
    | detail_level | BRIEFLY_DESCRIBED |
  And the output path is projects/${JERRY_PROJECT}/test-specs/UC-LIB-001-borrow-a-book.feature.md

  When tspec-generator is invoked with input UC-LIB-001

  Then tspec-generator rejects the input with the message:
    "UC UC-LIB-001 is at BRIEFLY_DESCRIBED. Clark transformation requires ESSENTIAL_OUTLINE or FULLY_DESCRIBED. Use /use-case to elaborate the use case first."
  And no Feature file is written at the output path
  And no partial Gherkin content is produced
```

---

### Scenario G-003: Basic Flow Happy Path Mapping

**Clark rules exercised:** RULE-C3-01 (single Scenario from all basic_flow steps), RULE-C3-02 (Source annotation), RULE-ST-01 (actor_action → When), RULE-ST-02 (system_response → Then), RULE-ST-03 (validation → Then assertion)

**Assertion rationale:** Verifies that the happy path Scenario is generated from ALL basic_flow steps combined into a single scenario, with correct Given/When/Then clause assignment per step type.

```gherkin
Scenario: G-003 -- All basic_flow steps combined into exactly one happy path Scenario

  Given a use case artifact UC-LIB-001 exists at ESSENTIAL_OUTLINE with basic_flow:
    | Step | Type            | Actor          | Action                                                                       |
    | 1    | actor_action    | Library Member | presents library card and requests a specific book copy at the circulation desk |
    | 2    | validation      | System         | validates member card status and checks that no overdue loans exist          |
    | 3    | validation      | System         | checks that the requested book copy is available for loan                    |
    | 4    | actor_action    | Library Member | confirms the loan and accepts the due date                                   |
    | 5    | system_response | System         | creates a loan record, updates the book copy status to CHECKED_OUT, and prints a due-date slip |
  And the UC has preconditions: ["Member holds a valid, active library card", "Member has no outstanding overdue books"]

  When tspec-generator applies the Clark transformation to basic_flow

  Then exactly ONE Scenario is produced for the happy path (not one per step)
  And the scenario title is "Borrow a Book - Main Success Scenario"
  And the Source annotation reads "**Source:** basic_flow (steps 1-5)"
  And the Gherkin block contains Given clauses derived from preconditions:
    """
    Given Member holds a valid, active library card
      And Member has no outstanding overdue books
    """
  And steps 1 and 4 (actor_action) produce When clauses:
    """
    When Library Member presents library card and requests a specific book copy at the circulation desk
      And Library Member confirms the loan and accepts the due date
    """
  And steps 2 and 3 (validation) produce Then assertion clauses containing "the system verifies that"
  And step 5 (system_response) produces a Then clause starting with "Then the system"
```

---

### Scenario G-004: Extension Failure Scenario Mapping

**Clark rules exercised:** RULE-C5-01 (one Scenario per extension), RULE-OT-01 (outcome=failure → negative test), RULE-QA-02 (Source annotation present)

**Assertion rationale:** Verifies that extensions with outcome=failure are each mapped to a distinct negative test scenario with "Then the system rejects the request" assertion, and that each scenario carries a Source annotation.

```gherkin
Scenario: G-004 -- Each extension with outcome=failure generates a distinct negative test scenario

  Given a use case artifact UC-LIB-001 exists at ESSENTIAL_OUTLINE with 5 basic_flow steps
  And the UC has extensions:
    | ID    | anchor_step | condition                            | outcome |
    | EXT-2A | 2          | Member card is expired or suspended  | failure |
    | EXT-2B | 2          | Member has overdue loans             | failure |
    | EXT-3A | 3          | Requested book copy is not available | failure |

  When tspec-generator applies Clark transformation to extensions

  Then exactly 3 Scenarios are produced for extensions (one per extension, no merging)
  And each scenario title does NOT contain the word "fails" (domain language required per RULE-OT-01)
  And each scenario contains a "**Source:**" annotation citing the extension ID and anchor_step
  And each scenario Given block includes both the base preconditions AND the extension condition
  And each scenario Then block contains "the system rejects the request" as the primary assertion
  And each scenario Then block includes "the system notifies Library Member of the reason the loan was refused"
  And no two extensions are merged into the same Scenario block
```

---

### Scenario G-005: Slice-Scoped Generation

**Clark rules exercised:** RULE-SL-01 (filter flows to slice scope), RULE-SL-02 (coverage denominator = slice flows only)

**Assertion rationale:** Verifies that when slice_id is provided, only flows with anchor_step or branches_from_step within the slice's steps_included are mapped, and the coverage denominator reflects the slice scope.

```gherkin
Scenario: G-005 -- Slice-scoped generation produces Feature file scoped to slice steps only

  Given a use case artifact UC-LIB-001 exists at ESSENTIAL_OUTLINE with:
    | basic_flow | 5 steps (steps 1-5)                                       |
    | extensions | EXT-2A (anchor_step: 2), EXT-2B (anchor_step: 2), EXT-3A (anchor_step: 3) |
  And the UC has a slice "slice-001" with steps_included: [1, 2]
  And tspec-generator is invoked with slice_id = "slice-001"

  When tspec-generator applies RULE-SL-01 to filter flows to slice-001 scope

  Then the Feature file YAML frontmatter contains slice_id = "slice-001" (not null)
  And the Feature file includes the happy path scenario (basic_flow step 1 is in steps_included)
  And the Feature file includes scenarios for EXT-2A and EXT-2B (anchor_step 2 is in steps_included)
  And the Feature file does NOT include a scenario for EXT-3A (anchor_step 3 is outside steps_included)
  And the coverage frontmatter reflects the slice scope:
    | Field                         | Expected Value |
    | coverage.total_flows          | 3              |
    | coverage.mapped_flows         | 3              |
    | coverage.extensions_mapped    | 2              |
  And coverage percentage is computed as 3/3 = 100% (not 3/4 = 75%)
```

---

## Feature: tspec-analyst Agent

```gherkin
Feature: tspec-analyst Agent -- BDD Coverage Analysis

  Background:
    Given the tspec-analyst agent is available with tools: Read, Write, Edit, Glob, Grep, Bash
    And the source use case artifact and generated Feature file are both accessible
```

---

### Scenario A-001: Coverage Computation Happy Path

**Quality framework:** 7 Cs C1 (Coverage) -- primary criterion, coverage formula: mapped_scenarios / total_mappable_flows

**Assertion rationale:** Verifies that tspec-analyst correctly computes coverage from the Feature file (FX-03) against the source UC (FX-01), producing a coverage report at the expected output path with L0/L1/L2 sections.

```gherkin
Scenario: A-001 -- tspec-analyst computes 100% coverage from a complete Feature file

  Given a Feature file UC-LIB-001-borrow-a-book.feature.md exists at projects/${JERRY_PROJECT}/test-specs/
  And the Feature file was generated from UC-LIB-001 (ESSENTIAL_OUTLINE, 5 basic_flow steps, 3 extensions)
  And the Feature file contains 4 scenarios with correct Source annotations
  And the Traceability Matrix has 4 rows mapping all flow elements
  And the source use case artifact UC-LIB-001 exists with the same 3 extensions

  When tspec-analyst is invoked with the Feature file and source UC as inputs

  Then a coverage report is written at:
    projects/${JERRY_PROJECT}/test-specs/UC-LIB-001-borrow-a-book-coverage.md
  And the report L0 section contains:
    | Metric              | Value |
    | Coverage            | 100%  |
    | Total Flows         | 4     |
    | Mapped Flows        | 4     |
    | Gap Count           | 0     |
    | Coverage Status     | PASS  |
  And the report L1 section contains a per-flow mapping table with 4 rows
  And the report L2 section contains a risk assessment for uncovered paths
  And the report states "All use case flows are mapped to test scenarios. No coverage gaps identified."
```

---

### Scenario A-002: Gap Identification for Unmapped Extension

**Quality framework:** 7 Cs C1 (Coverage) -- gap prioritization: outcome=failure extensions are highest priority

**Assertion rationale:** Verifies that tspec-analyst detects unmapped extensions, cites them by their specific ID (e.g., EXT-2B), assigns priority based on outcome type (failure = P0), and includes an estimated effort for remediation.

```gherkin
Scenario: A-002 -- tspec-analyst identifies and prioritizes unmapped failure extension as P0 gap

  Given a Feature file UC-LIB-001-borrow-a-book.feature.md exists at projects/${JERRY_PROJECT}/test-specs/
  And the Feature file contains only 1 scenario (the happy path)
  And the Feature file YAML frontmatter shows:
    | coverage.extensions_mapped | 0 |
    | coverage.total_flows       | 4 |
    | coverage.mapped_flows      | 1 |
  And the source use case artifact UC-LIB-001 has 3 extensions:
    EXT-2A (failure), EXT-2B (failure), EXT-3A (failure)

  When tspec-analyst is invoked with the Feature file and source UC as inputs

  Then the coverage report L0 section contains:
    | Metric              | Value |
    | Coverage            | 25%   |
    | Total Flows         | 4     |
    | Mapped Flows        | 1     |
    | Gap Count           | 3     |
    | Coverage Status     | FAIL  |
  And the report identifies 3 coverage gaps: EXT-2A, EXT-2B, EXT-3A
  And each gap entry cites the specific unmapped flow element ID (not a generic description)
  And each gap entry includes a priority field: P0 (because outcome=failure is the highest-risk classification)
  And each gap entry includes a recommended scenario title and effort estimate
  And the report L1 section includes a per-flow mapping table showing these 3 flows as "UNMAPPED"
```

---

## Feature: Cross-Agent Pipeline

```gherkin
Feature: Cross-Agent Pipeline -- tspec-generator to tspec-analyst Integration

  Background:
    Given tspec-generator and tspec-analyst are independent T2 worker agents
    And they communicate exclusively via filesystem (Feature file and UC artifact)
    And neither agent invokes the other directly (P-003 compliance)
```

---

### Scenario E-001: Generator-to-Analyst Pipeline

**Standards covered:** P-003 (no direct agent-to-agent invocation), test-specification-v1.schema.json (frontmatter contract), 7 Cs C1 pipeline handoff

**Assertion rationale:** Verifies the complete pipeline: tspec-generator writes a Feature file with valid YAML frontmatter matching the schema; tspec-analyst reads the frontmatter (without requiring the source UC frontmatter fields to be re-parsed) and produces a coverage report that cites the Feature file's `source_use_case` field for cross-reference.

```gherkin
Scenario: E-001 -- Feature file produced by generator is consumed by analyst via filesystem handoff

  Given tspec-generator has produced UC-LIB-001-borrow-a-book.feature.md with valid YAML frontmatter
  And the frontmatter validates against docs/schemas/test-specification-v1.schema.json
  And the frontmatter contains source_use_case = "UC-LIB-001" enabling tspec-analyst to locate the source
  And tspec-generator has NOT directly invoked tspec-analyst (P-003: no agent-to-agent invocation)

  When tspec-analyst is invoked independently from MAIN CONTEXT with the Feature file path

  Then tspec-analyst reads the Feature file YAML frontmatter to obtain source_use_case = "UC-LIB-001"
  And tspec-analyst locates the source UC artifact using the source_use_case identifier
  And tspec-analyst produces a coverage report that cites "source_use_case: UC-LIB-001" in its header
  And the coverage report is written at the expected output path without any agent-to-agent communication
  And the pipeline produces no errors related to missing frontmatter fields
  And the scenario count in the coverage report matches the scenario_count field in the Feature file frontmatter
```

---

## Acceptance Verification Checklist

> For use by eng-reviewer when verifying this file against the architecture specification (F-15).

| Check | Criterion | Status |
|-------|-----------|--------|
| BDD-01 | Minimum 7 scenarios present | 8 scenarios (G-001 through G-005, A-001, A-002, E-001) -- PASS |
| BDD-02 | All scenarios in Given/When/Then format | All 8 scenarios use Gherkin format -- PASS |
| BDD-03 | tspec-generator happy path covered | G-001 -- PASS |
| BDD-04 | tspec-generator input rejection (detail_level < ESSENTIAL_OUTLINE) | G-002 (RULE-IV-01) -- PASS |
| BDD-05 | Clark mapping correctness: basic_flow → single happy path Scenario | G-003 (RULE-C3-01, RULE-ST-01 through RULE-ST-03) -- PASS |
| BDD-06 | Clark mapping correctness: extension → error Scenario | G-004 (RULE-C5-01, RULE-OT-01) -- PASS |
| BDD-07 | Slice-scoped generation coverage denominator scoping | G-005 (RULE-SL-01, RULE-SL-02) -- PASS |
| BDD-08 | tspec-analyst coverage computation | A-001 (7 Cs C1, coverage formula) -- PASS |
| BDD-09 | tspec-analyst gap identification with specific flow citation | A-002 (gap prioritization) -- PASS |
| BDD-10 | Cross-agent pipeline integration (P-003 filesystem-only) | E-001 -- PASS |
| BDD-11 | Navigation table present (H-23) | Document Sections table present -- PASS |
| BDD-12 | Coverage matrix present | Coverage Matrix table with 8 rows -- PASS |
| BDD-13 | Fixtures defined | 5 fixtures (FX-01 through FX-05) defined in Overview -- PASS |
| BDD-14 | File ID header present | F-15 header present -- PASS |
| BDD-15 | P-003 constitutional compliance verified | E-001 asserts no direct agent-to-agent invocation -- PASS |

---

*Tests Version: 1.0.0 | Audience: eng-qa (implementation), eng-reviewer (verification)*
*Companion: skills/test-spec/rules/clark-transformation-rules.md (rule-level traceability)*
*Reference: Clark (2018) UC2.0-to-Gherkin mapping algorithm, SD-07, SD-08*
