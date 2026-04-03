# Behavior Tests: /contract-design Skill

> **File ID:** F-16 | **Skill:** /contract-design | **Version:** 1.0.0
> **Author:** eng-backend | **Date:** 2026-03-09 | **Criticality:** C3
> **Status:** PROPOSED
> **Standard:** H-20 (BDD test-first), H-23 (navigation table required)
> **Schema:** `docs/schemas/use-case-realization-v1.schema.json` (v1.0.0)
> **Rules:** `skills/contract-design/rules/uc-to-contract-rules.md` (RULE-RI through RULE-TR)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | Scope, methodology, test fixtures, coverage summary |
| [Coverage Matrix](#coverage-matrix) | Implementation files and rules covered per scenario |
| [Feature: cd-generator Agent](#feature-cd-generator-agent) | UC-to-contract transformation and generation scenarios |
| [Scenario G-001: Happy Path Generation](#scenario-g-001-happy-path-generation) | Full UC with 1 consumer interaction → OpenAPI contract |
| [Scenario G-002: Missing Interactions Rejection](#scenario-g-002-missing-interactions-rejection) | Layer 2 gate: no interactions block |
| [Scenario G-003: HTTP Method Inference High Confidence](#scenario-g-003-http-method-inference-high-confidence) | RULE-HM-02: create verb → POST |
| [Scenario G-004: HTTP Method Inference Low Confidence](#scenario-g-004-http-method-inference-low-confidence) | RULE-HM-05: ambiguous verb → POST + x-method-inference: low |
| [Scenario G-005: PROTOTYPE Label Enforcement](#scenario-g-005-prototype-label-enforcement) | RULE-TR-02: x-prototype: true mandatory |
| [Scenario G-006: Extension to Error Response Mapping](#scenario-g-006-extension-to-error-response-mapping) | RULE-ER-01d: failure extension → 409 Conflict |
| [Feature: cd-validator Agent](#feature-cd-validator-agent) | Contract validation and traceability verification scenarios |
| [Scenario V-001: Structural Validity PASS](#scenario-v-001-structural-validity-pass) | Step 1: valid OpenAPI 3.1 YAML passes |
| [Scenario V-002: Traceability Coverage Gap Detection](#scenario-v-002-traceability-coverage-gap-detection) | Step 2: unmapped consumer interaction → FAIL |
| [Scenario V-003: PROTOTYPE Label Absence FAIL](#scenario-v-003-prototype-label-absence-fail) | Step 7: missing x-prototype: true → mandatory FAIL |
| [Feature: Cross-Agent Pipeline](#feature-cross-agent-pipeline) | End-to-end generator → validator integration scenario |
| [Scenario E-001: Generator to Validator Pipeline](#scenario-e-001-generator-to-validator-pipeline) | cd-generator output consumed by cd-validator, 100% coverage |
| [Acceptance Verification Checklist](#acceptance-verification-checklist) | Reviewer checklist for F-16 completeness |

---

## Overview

This file defines the BDD behavior test specifications for the `/contract-design` skill per H-20 (BDD test-first) and the architecture specification (Section 11 step-11-contract-design-architecture.md). All scenarios are written in full Gherkin format (Feature / Scenario / Given / When / Then) with concrete inputs and verifiable assertions.

### Scope

| In Scope | Out of Scope | Rationale for Out of Scope |
|----------|-------------|---------------------------|
| cd-generator UC-to-contract transformation correctness (RULE-RI through RULE-TR) | /use-case skill (uc-slicer) | Separate skill with separate test file |
| cd-generator input validation gate (Layer 2 guardrail checks) | Python pytest execution (no Python implementation) | /contract-design is a pure markdown/YAML skill; H-20 BDD applies, H-21 line coverage is N/A |
| cd-validator 9-step validation protocol | Network/MCP integration | Both agents are T2 with no network access by design |
| PROTOTYPE label enforcement (RULE-TR-02) | SAST/DAST scanning | /contract-design produces documentation artifacts, not deployable code |
| HTTP method inference (RULE-HM-01 through RULE-HM-05) | AsyncAPI/CloudEvents generation | Deferred per DI-07, ASM-005, G-02 |
| Extension-to-error-response mapping (RULE-ER-01) | Registration in CLAUDE.md / AGENTS.md | That is eng-reviewer scope (FIND-005/006/007 carryforward) |
| Cross-agent filesystem-mediated pipeline (P-003 compliance) | OpenAPI 3.1 spec runner execution | OpenAPI files are documentation artifacts; execution toolchain is out of scope |

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

Scenarios are organized into three Features: `cd-generator Agent`, `cd-validator Agent`, and `Cross-Agent Pipeline`. Within each Feature, scenarios are ordered from happy path through negative cases. Total: 10 scenarios (minimum 9 per architecture requirement).

### Test Fixtures

| Fixture ID | Description | Defined In |
|-----------|-------------|------------|
| FX-01 | UC-LIB-001 at INTERACTION_DEFINED with 1 consumer interaction INT-01 (borrow a book), 3 internal interactions INT-02 through INT-04, and extension EXT-2a (failure, anchor_step=2) | Inline in G-001, G-003, G-005, G-006, E-001 |
| FX-02 | UC-LIB-001 at STORY_DEFINED (no interactions block) | Inline in G-002 |
| FX-03 | UC-LIB-001 at INTERACTION_DEFINED with INT-05 where request_description uses an ambiguous verb ("performs the loan operation") | Inline in G-004 |
| FX-04 | Valid OpenAPI 3.1 contract generated from FX-01 with x-prototype: true and correct traceability annotations | Inline in V-001, E-001 |
| FX-05 | Valid OpenAPI 3.1 contract from FX-01 but missing one consumer interaction mapping (INT-01 unmapped) | Inline in V-002 |
| FX-06 | Valid OpenAPI 3.1 contract from FX-01 but info.x-prototype absent | Inline in V-003 |

---

## Coverage Matrix

| Scenario | File Under Test | Rules / Standards Covered |
|----------|----------------|---------------------------|
| G-001 | cd-generator.md, uc-to-contract-rules.md, openapi-template.yaml | RULE-RI-01, RULE-OM-01, RULE-HM-02, RULE-SD-01, RULE-SD-02, RULE-AR-01, RULE-TR-01, RULE-TR-02 |
| G-002 | cd-generator.md | Layer 2 input validation: missing interactions block rejection |
| G-003 | cd-generator.md, uc-to-contract-rules.md | RULE-HM-02: create/submit semantics → POST, confidence: high |
| G-004 | cd-generator.md, uc-to-contract-rules.md | RULE-HM-05: ambiguous verb → POST + x-method-inference: low annotation |
| G-005 | cd-generator.md, uc-to-contract-rules.md | RULE-TR-02: x-prototype: true mandatory in info section |
| G-006 | cd-generator.md, uc-to-contract-rules.md | RULE-ER-01d: failure extension (conflict) → 409, x-source-extension annotation |
| V-001 | cd-validator.md | Step 1 (Structural Validity): valid YAML + openapi 3.1.x + info/paths/components |
| V-002 | cd-validator.md | Step 2 (Path Completeness): unmapped consumer interaction → coverage < 100% → FAIL |
| V-003 | cd-validator.md | Step 7 (PROTOTYPE Label): missing x-prototype: true → mandatory FAIL |
| E-001 | cd-generator.md, cd-validator.md, uc-to-contract-rules.md | Cross-agent P-003 compliance, filesystem-mediated handoff, full pipeline coverage |

---

## Feature: cd-generator Agent

```gherkin
Feature: cd-generator Agent -- UC-to-Contract Transformation

  Background:
    Given the cd-generator agent is available with tools: Read, Write, Edit, Glob, Grep, Bash
    And uc-to-contract-rules.md is accessible at skills/contract-design/rules/uc-to-contract-rules.md
    And openapi-template.yaml is accessible at skills/contract-design/templates/openapi-template.yaml
    And use-case-realization-v1.schema.json is accessible at docs/schemas/use-case-realization-v1.schema.json
```

---

### Scenario G-001: Happy Path Generation

**Rules exercised:** RULE-RI-01, RULE-OM-01, RULE-OM-02, RULE-HM-02, RULE-SD-01, RULE-SD-02, RULE-AR-01, RULE-TR-01, RULE-TR-02

**Assertion rationale:** Verifies the full UC-to-contract transformation pipeline from a valid INTERACTION_DEFINED UC artifact to an OpenAPI 3.1 contract with correct traceability annotations, x-prototype: true label, and mapping document.

```gherkin
Scenario: G-001 -- Full UC with consumer interaction generates OpenAPI contract

  Given a use case artifact UC-LIB-001 exists at the input path with:
    | Field              | Value                                             |
    | id                 | UC-LIB-001                                        |
    | title              | Borrow a Book                                     |
    | realization_level  | INTERACTION_DEFINED                               |
    | detail_level       | ESSENTIAL_OUTLINE                                 |
    | primary_actor      | Library Member                                    |
    | interactions       | [INT-01 (consumer), INT-02 (provider), INT-03 (provider), INT-04 (provider)] |
    | INT-01.actor_role  | consumer                                          |
    | INT-01.request_description | "presents library card and requests a specific book copy for borrowing" |
    | INT-01.response_description | "creates a loan record, updates book copy status to CHECKED_OUT, and returns a due-date slip" |
    | INT-01.preconditions | ["valid library card", "no overdue books", "book copy available"] |
    | INT-01.postconditions | ["Loan record created", "status CHECKED_OUT", "Due date issued"] |
    | supporting_actors  | [{ name: "ILS System" }]                         |
  And the output path is projects/${JERRY_PROJECT}/contracts/UC-LIB-001-borrow-a-book.openapi.yaml

  When cd-generator is invoked with the artifact path and output path

  Then an OpenAPI contract is written at the output path
  And the contract info section contains:
    | Field           | Expected Value     |
    | openapi         | "3.1.0"            |
    | info.x-prototype | true              |
    | info.x-source-use-case | "UC-LIB-001" |
    | info.x-primary-actor | "Library Member" |
  And the contract paths section contains exactly 1 path (/loans)
  And POST /loans operation has:
    | Field                | Expected Value |
    | operationId          | createLoan     |
    | x-source-interaction | "INT-01"       |
    | x-source-step        | 1              |
    | x-source-flow        | "basic_flow"   |
    | requestBody.required | true           |
    | responses.201        | present        |
  And the contract components.schemas section contains CreateLoanRequest and CreateLoanResponse
  And the contract x-internal-operations array contains 3 entries (INT-02, INT-03, INT-04)
  And a mapping document is written at UC-LIB-001-borrow-a-book-mapping.md alongside the contract
  And cd-generator reports: "operation_count=1, x_prototype_status=true, verdict=COMPLETE"
```

---

### Scenario G-002: Missing Interactions Rejection

**Rules exercised:** Layer 2 input validation gate (guardrails.input_validation)

**Assertion rationale:** Verifies that cd-generator rejects UC artifacts without an interactions block with an actionable error message directing the user to /use-case.

```gherkin
Scenario: G-002 -- UC artifact without interactions block is rejected

  Given a use case artifact UC-LIB-001 exists at the input path with:
    | Field              | Value            |
    | id                 | UC-LIB-001       |
    | title              | Borrow a Book    |
    | realization_level  | STORY_DEFINED    |
    | detail_level       | ESSENTIAL_OUTLINE |
    | interactions       | (absent)         |

  When cd-generator is invoked with the artifact path

  Then cd-generator does NOT write any OpenAPI contract file
  And cd-generator returns an error message containing:
    | Field    | Expected Content                                                    |
    | error    | "UC UC-LIB-001 has no interactions block"                          |
    | guidance | "Use /use-case (uc-slicer Activity 5) to identify system boundaries and interaction points first" |
  And cd-generator reports: "verdict=REJECTED"
```

---

### Scenario G-003: HTTP Method Inference High Confidence

**Rules exercised:** RULE-HM-02 (create/submit → POST, confidence: high)

**Assertion rationale:** Verifies that a request_description containing creation semantics ("requests...for borrowing" implying resource creation) produces a POST operation with x-method-inference: high annotation.

```gherkin
Scenario: G-003 -- Create verb in request_description produces POST with high confidence

  Given a use case artifact UC-LIB-001 at INTERACTION_DEFINED with:
    | Field                      | Value                                               |
    | INT-01.request_description | "submits a new loan request for a specific book copy" |
    | INT-01.actor_role          | consumer                                            |
    | INT-01.response_description | "loan record created and due date issued"          |

  When cd-generator applies the HTTP method inference algorithm to INT-01

  Then the generated POST /loans operation contains:
    | Field                | Expected Value |
    | HTTP method          | POST           |
    | x-method-inference   | "high"         |
  And no warning annotation is present on the operation
```

---

### Scenario G-004: HTTP Method Inference Low Confidence

**Rules exercised:** RULE-HM-05 (ambiguous verb → POST default + x-method-inference: low)

**Assertion rationale:** Verifies that an ambiguous request_description produces a POST operation with x-method-inference: low annotation and a warning, requiring human review.

```gherkin
Scenario: G-004 -- Ambiguous verb in request_description produces POST with low confidence annotation

  Given a use case artifact UC-LIB-001 at INTERACTION_DEFINED with:
    | Field                      | Value                                     |
    | INT-05.request_description | "performs the loan operation on the system" |
    | INT-05.actor_role          | consumer                                  |
    | INT-05.response_description | "operation acknowledged by the system"   |

  When cd-generator applies the HTTP method inference algorithm to INT-05

  Then the generated POST operation for INT-05 contains:
    | Field              | Expected Value |
    | HTTP method        | POST           |
    | x-method-inference | "low"          |
  And a human review annotation is present indicating method confidence is low
```

---

### Scenario G-005: PROTOTYPE Label Enforcement

**Rules exercised:** RULE-TR-02 (x-prototype: true mandatory, non-negotiable)

**Assertion rationale:** Verifies that cd-generator always includes x-prototype: true in the info section regardless of the number of interactions or request parameters, and that the label cannot be overridden.

```gherkin
Scenario: G-005 -- Generated contract always carries x-prototype: true in info section

  Given a valid use case artifact UC-LIB-001 at INTERACTION_DEFINED with FX-01 interactions

  When cd-generator generates the OpenAPI contract

  Then the contract info section contains x-prototype: true
  And the contract info section does NOT contain x-prototype: false
  And the mapping document contains a "PROTOTYPE STATUS" section
  And the mapping document states that the PROTOTYPE label must be removed by human review only
```

---

### Scenario G-006: Extension to Error Response Mapping

**Rules exercised:** RULE-ER-01d (failure extension with conflict condition → 409 Conflict)

**Assertion rationale:** Verifies that a failure extension with anchor_step matching an interaction's source_step produces a 4xx error response on that operation with x-source-extension annotation.

```gherkin
Scenario: G-006 -- Failure extension anchored to interaction step produces 409 error response

  Given a use case artifact UC-LIB-001 at INTERACTION_DEFINED with:
    | Field                  | Value                                          |
    | INT-01.source_step     | 1                                              |
    | INT-01.actor_role      | consumer                                       |
    | EXT-2a.outcome         | failure                                        |
    | EXT-2a.anchor_step     | 2                                              |
    | EXT-2a.condition       | "Member has outstanding overdue books"         |

  When cd-generator applies the extension-to-error-response mapping algorithm

  Then the POST /loans operation has a 409 response containing:
    | Field                | Expected Value                              |
    | description          | "Member has outstanding overdue books"      |
    | schema.$ref          | "#/components/schemas/ErrorResponse"        |
    | x-source-extension   | "EXT-2a"                                    |
  And components.schemas.ErrorResponse is defined with error and code properties
```

---

## Feature: cd-validator Agent

```gherkin
Feature: cd-validator Agent -- Contract Validation and Traceability Verification

  Background:
    Given the cd-validator agent is available with tools: Read, Write, Edit, Glob, Grep, Bash
    And uc-to-contract-rules.md is accessible at skills/contract-design/rules/uc-to-contract-rules.md
    And the source use case artifact is accessible at the specified artifact_path
```

---

### Scenario V-001: Structural Validity PASS

**Rules exercised:** Step 1 (Structural Validity check)

**Assertion rationale:** Verifies that a well-formed OpenAPI 3.1 contract passes Step 1 with PASS verdict and that all required top-level sections are present.

```gherkin
Scenario: V-001 -- Well-formed OpenAPI 3.1 contract passes structural validity check

  Given a generated OpenAPI contract at the contract_path with:
    | Field               | Value    |
    | openapi             | "3.1.0"  |
    | info.title          | present  |
    | info.version        | present  |
    | info.x-prototype    | true     |
    | paths               | present (1 path with 1 operation) |
    | components.schemas  | present (with at least 1 schema)  |
  And the source UC artifact is at the artifact_path with interactions block present

  When cd-validator executes Step 1 (Structural Validity)

  Then Step 1 verdict is PASS
  And the evidence states all required fields are present
  And cd-validator proceeds to Step 2
```

---

### Scenario V-002: Traceability Coverage Gap Detection

**Rules exercised:** Step 2 (Path Completeness), traceability coverage formula

**Assertion rationale:** Verifies that when a consumer interaction has no corresponding operation in the contract, cd-validator reports FAIL with the specific missing interaction ID and coverage < 100%.

```gherkin
Scenario: V-002 -- Missing consumer interaction mapping produces FAIL with specific gap

  Given a UC artifact UC-LIB-001 at artifact_path with:
    | Field      | Value                              |
    | interactions | [INT-01 (consumer), INT-06 (consumer)] |
  And a contract at contract_path with:
    | Field  | Value                                        |
    | paths  | POST /loans with x-source-interaction: "INT-01" |
    | (INT-06 is NOT mapped to any operation)    |

  When cd-validator executes Step 2 (Path Completeness)

  Then Step 2 verdict is FAIL
  And the traceability coverage is reported as "1/2 = 50%"
  And the unmapped interaction list contains "INT-06"
  And the overall verdict is FAIL
  And the validation report Traceability Matrix shows INT-06 as "unmapped"
```

---

### Scenario V-003: PROTOTYPE Label Absence -- Mandatory FAIL

**Rules exercised:** Step 7 (PROTOTYPE Label Verification -- mandatory FAIL, no override)

**Assertion rationale:** Verifies that the absence of info.x-prototype: true produces a mandatory FAIL on Step 7 with the specific error message from the guardrail, and that no override is possible.

```gherkin
Scenario: V-003 -- Contract missing x-prototype: true produces mandatory Step 7 FAIL

  Given a contract at contract_path that is otherwise structurally valid but:
    | Field             | Value                                          |
    | info.x-prototype  | (absent -- field not present in info section) |
  And the contract has 100% consumer interaction coverage

  When cd-validator executes Step 7 (PROTOTYPE Label Verification)

  Then Step 7 verdict is FAIL
  And the failure message contains:
    "Contract is missing info.x-prototype: true. This label is required until a human reviewer validates the contract's semantic correctness. Do not distribute this contract without the PROTOTYPE label."
  And the overall verdict is FAIL regardless of other step results
  And the validation report states this is a mandatory FAIL with no override permitted
```

---

## Feature: Cross-Agent Pipeline

```gherkin
Feature: Cross-Agent Pipeline -- Generator to Validator Integration

  Background:
    Given cd-generator and cd-validator agents are available
    And both agents communicate only through shared files on the filesystem (P-003 compliant)
    And neither agent invokes the other directly
```

---

### Scenario E-001: Generator to Validator Pipeline

**Rules exercised:** P-003 compliance, filesystem-mediated handoff, full UC-to-contract-to-validation pipeline

**Assertion rationale:** Verifies the end-to-end pipeline: cd-generator writes the OpenAPI contract and mapping document, cd-validator reads them independently via the filesystem, and the pipeline produces a PASS validation report with 100% traceability coverage.

```gherkin
Scenario: E-001 -- Generator output consumed by validator produces PASS with 100% coverage

  Given a valid UC artifact UC-LIB-001 at INTERACTION_DEFINED with FX-01 content (1 consumer interaction INT-01)
  And the output path is projects/${JERRY_PROJECT}/contracts/UC-LIB-001-borrow-a-book.openapi.yaml

  When cd-generator is invoked with the artifact path and output path
  And the OpenAPI contract is written at the output path
  And the mapping document is written at UC-LIB-001-borrow-a-book-mapping.md

  And cd-validator is invoked with:
    | Field          | Value                                                               |
    | contract_path  | projects/${JERRY_PROJECT}/contracts/UC-LIB-001-borrow-a-book.openapi.yaml |
    | artifact_path  | projects/${JERRY_PROJECT}/use-cases/UC-LIB-001-borrow-a-book.md   |
    | mapping_path   | projects/${JERRY_PROJECT}/contracts/UC-LIB-001-borrow-a-book-mapping.md |

  Then a validation report is written at UC-LIB-001-borrow-a-book-validation.md
  And the overall validation verdict is PASS
  And the traceability coverage is "1/1 = 100%"
  And all 9 validation steps have PASS verdicts
  And the validation report contains a Traceability Matrix with 1 row (INT-01 → POST /loans)
  And cd-generator did NOT modify the source UC artifact (read-only consumption verified)
  And cd-validator did NOT modify the generated OpenAPI contract (read-only evaluation verified)
```

---

## Acceptance Verification Checklist

> For use by eng-reviewer during F-16 review.

| Check | Pass Criteria | Status |
|-------|--------------|--------|
| Scenario count | At least 9 scenarios present | 10 scenarios |
| H-20 compliance | All scenarios in Gherkin Given/When/Then format | Present |
| H-23 compliance | Navigation table with anchor links present | Present |
| Scenario IDs | Each scenario has a unique ID (G-NNN, V-NNN, E-NNN) in title | Present |
| Coverage Matrix | All scenarios listed with rules/files covered | Present |
| Rule coverage | RULE-RI-01, RULE-OM-01, RULE-HM-02, RULE-HM-05, RULE-SD-01, RULE-SD-02, RULE-ER-01d, RULE-TR-01, RULE-TR-02 all covered | Present |
| Negative cases | At least 3 negative/rejection scenarios | G-002, V-002, V-003 |
| Mandatory FAIL | Step 7 PROTOTYPE absence covered as mandatory FAIL | V-003 |
| P-003 coverage | Cross-agent filesystem-mediated handoff verified | E-001 |
| Fixture definitions | All FX-NN fixtures defined in Overview | FX-01 through FX-06 |
| Concrete assertions | Assertions reference specific field values, not vague outcomes | Present |
| Input rejection messages | Rejection error messages specify actionable guidance | G-002 |
