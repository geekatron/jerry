# Security QA Review: /test-spec Skill

> **PS ID:** proj-021 | **Entry ID:** step-10-eng-qa-review | **Workflow ID:** use-case-skills-20260308-001
> **Date:** 2026-03-09 | **Agent:** eng-qa | **Step:** 10 (Phase 3 Implementation)
> **Input:** step-10-test-spec-architecture.md (v1.1.0, PASSED 0.952), step-10-eng-lead-review.md (v1.1.0, PASSED 0.9615), step-10-eng-backend-implementation.md (v1.1.0, PASSED 0.960)
> **Status:** PROPOSED
> **Version:** 1.0.0
> **GitHub Issue:** #109

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Coverage summary, defects found, overall security assessment |
| [L1: Technical Detail](#l1-technical-detail) | Scenario-level test assessment with evidence |
| [Test Strategy Assessment](#test-strategy-assessment) | BEHAVIOR_TESTS.md evaluation: BDD format, coverage, edge cases |
| [Security Test Assessment](#security-test-assessment) | OWASP-category evaluation, guardrail effectiveness, constitutional compliance |
| [Quality Gate Verification](#quality-gate-verification) | H-20, H-34, coverage matrix analysis |
| [Cross-Skill Integration Testing](#cross-skill-integration-testing) | /use-case to /test-spec pipeline validation |
| [Findings](#findings) | All findings with severity classification (CRITICAL/HIGH/MEDIUM/LOW) |
| [L2: Strategic Implications](#l2-strategic-implications) | Test strategy effectiveness, coverage gaps, regression suite |
| [S-010 Self-Review](#s-010-self-review) | Pre-delivery self-review checklist |

---

## L0: Executive Summary

The `/test-spec` skill has been implemented across 15 files. This QA review evaluated `skills/test-spec/tests/BEHAVIOR_TESTS.md` (F-15, 8 scenarios), the agent definitions (`tspec-generator`, `tspec-analyst`), the Clark transformation rules (`clark-transformation-rules.md`, 24 rules), the JSON schema (`test-specification-v1.schema.json`), and the sample output (`sample-test-specification.md`) against OWASP Testing Guide categories, H-20 (BDD test-first), and H-34 (agent definition architecture).

**Overall Assessment: PASS with findings.** The skill is structurally sound and constitutionally compliant. The 8 BDD scenarios meet the H-20 minimum and cover the primary Clark transformation paths. Four findings are raised, none CRITICAL, all addressable without architectural change. The skill's attack surface is minimal: no server-side code, no authentication, no network access, filesystem-only write operations scoped to `projects/`.

**Security defects found during test design: 0.** No implementation defects were identified. Three behavioral gaps were found in the test specification scope (MEDIUM severity) and one specification ambiguity was found in the schema (LOW severity).

**Scenario count summary:**

| Feature | Scenarios | Coverage Type |
|---------|-----------|---------------|
| tspec-generator Agent | 5 (G-001 through G-005) | 2 happy, 2 negative, 1 edge |
| tspec-analyst Agent | 2 (A-001 through A-002) | 1 happy, 1 negative |
| Cross-Agent Pipeline | 1 (E-001) | 1 integration |
| **Total** | **8** | Meets H-20 minimum (7 required) |

**Findings summary:**

| ID | Severity | Category | Title |
|----|----------|----------|-------|
| FIND-QA-001 | MEDIUM | INPVAL | RULE-IV-02 missing test scenario (extensions empty gate) |
| FIND-QA-002 | MEDIUM | INPVAL | RULE-IV-04 missing test scenario (basic_flow step type missing) |
| FIND-QA-003 | MEDIUM | BUSLOGIC | No scenario for rejoin outcome type (RULE-OT-03) |
| FIND-QA-004 | LOW | CRYPST | Schema coverage.mapped_flows can exceed total_flows -- no validation constraint |

---

## L1: Technical Detail

### Test Strategy Assessment

#### BDD Format Compliance

All 8 scenarios in BEHAVIOR_TESTS.md conform to the canonical Gherkin structure defined in the Overview Methodology section: `Feature` / `Background` / `Scenario` / `Given` / `When` / `Then` / `And`. The format is consistent and correct. No `But` or `*` wildcards are used, maintaining unambiguous clause semantics.

**Concrete input quality:** All scenarios include data tables or specific field values rather than abstract descriptions. G-001 uses a full 5-field table for the UC artifact; G-003 provides a 5-row basic_flow table with typed steps and actor/action text; A-002 provides the specific coverage frontmatter values. Assertions reference observable artifact state (file written at path, specific field values, specific text content) rather than internal agent state. This satisfies the H-20 requirement for verifiable assertions.

**Background blocks:** The two agent Features and the cross-agent Pipeline Feature each carry a Background block that establishes shared preconditions (tool availability, artifact accessibility). This is structurally correct and reduces repetition across scenarios within each Feature.

#### Scenario Coverage Analysis

**Clark rules exercised per scenario:**

| Scenario | Rules Tested | Rules NOT Tested |
|----------|-------------|------------------|
| G-001 | RULE-C1-01, C2-01, C3-01, C5-01, C7-01, QA-01, QA-04 | RULE-C4-01, C6-01, OT-02, OT-03, SL-01, SL-02, QA-02, QA-03 |
| G-002 | RULE-IV-01 (rejection) | RULE-IV-02, IV-03, IV-04 |
| G-003 | RULE-C3-01, C3-02, ST-01, ST-02, ST-03 | -- (full basic_flow mapping coverage) |
| G-004 | RULE-C5-01, OT-01, QA-02 | RULE-OT-02, OT-03 |
| G-005 | RULE-SL-01, SL-02 | -- (full slice-scope coverage) |
| A-001 | 7 Cs C1 (coverage formula: mapped/total) | C2-C7 quality criteria |
| A-002 | Gap identification, failure extension prioritization | P1/P2/P3 gap priority types |
| E-001 | P-003 filesystem handoff, frontmatter contract | Schema validation of generated frontmatter |

**Coverage distribution (per BEHAVIOR_TESTS.md overview):** 22% happy path (2 scenarios), 34% negative (3 scenarios), 44% edge cases (4 scenarios). This distribution is appropriate for a deterministic transformation skill where the happy path is well-defined. The edge cases (G-005 slice-scoped, A-002 gap analysis) provide the highest regression value.

**Rules without dedicated scenarios:**

| Untested Rule | Risk Level | Justification Assessment |
|---------------|-----------|--------------------------|
| RULE-IV-02 (extensions empty gate) | MEDIUM | No scenario -- FIND-QA-001 |
| RULE-IV-03 (basic_flow step count gate) | LOW | Step count boundary is JSON Schema-enforced (Layer 1); behavioral assertion is redundant but beneficial |
| RULE-IV-04 (step type missing gate) | MEDIUM | No scenario -- FIND-QA-002 |
| RULE-C4-01 (alternative flows) | LOW | Alternative flows are structurally identical to basic_flow mapping; RULE-C4-01 coverage is implicit in G-001 which uses empty alternative_flows; explicitly absent is an alternative_flows non-empty scenario |
| RULE-C6-01 (Given clause derivation) | LOW | G-003 tests Given clause production via precondition mapping; no standalone RULE-C6-01 scenario but the behavior is observable through G-001 and G-003 combined |
| RULE-OT-02 (success outcome) | LOW | Alternate success scenarios are structurally similar to failure; the absence is documented in sample scope notes |
| RULE-OT-03 (rejoin outcome) | MEDIUM | No scenario for rejoin:{N} pattern -- FIND-QA-003 |
| RULE-QA-03 (Traceability Matrix completeness) | LOW | QA-03 is partially covered by G-001 (Traceability Matrix present assertion), but no scenario for the QA-03 add-missing-row repair path |
| 7 Cs C2-C7 | LOW | C1 Coverage is the primary criterion; C2-C7 are assessed by A-001 implicitly but have no dedicated scenarios |

#### Edge Case and Error Scenario Coverage

The test suite addresses the primary rejection gate (RULE-IV-01 in G-002) and the slice-scoped generation edge case (G-005). The gap coverage scenario (A-002) tests the analyst's gap detection correctly. The following edge cases are absent:

- UC with zero alternative_flows AND zero extensions (contradicted by RULE-IV-02 which rejects this, but the rejection path itself is untested -- FIND-QA-001)
- UC with basic_flow having an unknown step type (not actor_action, system_response, or validation) -- the tspec-generator failure mode table describes this as "flag step; map to closest semantic type; report the mapping decision" but no BDD scenario tests this path
- Rejoin extension type (RULE-OT-03) -- structurally distinct from failure and success outcomes -- FIND-QA-003
- Malformed Source annotations in the Feature file (tspec-analyst failure mode: scenarios flagged as "untraceable") -- no scenario covers this analyst recovery path

#### Integration Scenarios (tspec-generator to tspec-analyst)

Scenario E-001 tests the filesystem handoff contract between the two agents. It covers:
- P-003 compliance (no direct agent-to-agent invocation)
- Schema-valid frontmatter production (validation assertion present)
- Source lookup via `source_use_case` field
- Coverage report cites the Feature file provenance
- Scenario count consistency between frontmatter and coverage report

E-001 does not cover the case where the Feature file frontmatter is schema-invalid (e.g., missing required field or wrong `generated_by` value). The schema's `const: "tspec-generator"` constraint for `generated_by` is a security control that would prevent analyst consumption of manually-authored Feature files that lack proper provenance. This path is not tested.

---

### Security Test Assessment

#### OWASP Testing Categories

**INPVAL (Input Validation Testing) -- Partial PASS**

The two-layer validation gate is the primary security boundary for this skill. Layer 1 (JSON Schema RULE-IV structural) and Layer 2 (agent guardrail semantic) are both present. Security assessment:

| Check | Scenario Coverage | Status |
|-------|------------------|--------|
| RULE-IV-01: detail_level gate (Layer 2) | G-002 -- TESTED | PASS |
| RULE-IV-02: extensions presence gate (Layer 2) | None | GAP -- FIND-QA-001 |
| RULE-IV-03: basic_flow step count gate (Layer 1+2) | None (schema enforces; no behavioral scenario) | LOW RISK |
| RULE-IV-04: step type completeness gate (Layer 2) | None | GAP -- FIND-QA-002 |
| Malformed YAML frontmatter (corrupted input) | None | LOW RISK -- schema validation upstream |
| Malicious UC content (injection in action field) | None | LOW RISK -- assessed below |

**Injection attack surface (A03):** tspec-generator derives Gherkin from UC artifact field values using `$.` path lookups (RULE-C3-01, RULE-ST-01 through ST-03). The transformation produces Markdown-formatted output, not executable code. A malicious actor inserting `'; DROP TABLE scenarios; --` or `<script>alert(1)</script>` into a `$.basic_flow[N].action` field would have it reproduced verbatim in the Gherkin When/Then clause. This is not an injection vulnerability in the classical sense (no code execution) but it is a content integrity concern: generated Feature files would contain unexpected content that could mislead test runners or confuse human reviewers. The guardrail `all_then_clauses_must_derive_from_postconditions_or_system_responses` partially addresses this by bounding the derivation source, but does not sanitize the content itself. This is assessed as LOW risk given the threat model (markdown/YAML skill, no code execution surface). No BDD scenario covers this content integrity path.

**Path traversal (A05 -- Security Misconfiguration):** The output location pattern `projects/${JERRY_PROJECT}/test-specs/UC-{DOMAIN}-{NNN}-{slug}.feature.md` scopes writes to the project directory. There is no scenario testing a path traversal attempt (e.g., `slice_id = "../../../etc/secrets"`). The risk is low because the agent operates as an LLM reasoning about file paths rather than directly evaluating user-controlled strings as filesystem operations. The guardrails section does not explicitly prohibit writing outside `projects/`, which is a minor specification gap (LOW).

**BUSLOGIC (Business Logic Testing) -- PASS**

| Check | Scenario Coverage | Status |
|-------|------------------|--------|
| Clark 1:1 cardinality contract | G-001, G-003 | PASS |
| detail_level gate enforcement | G-002 | PASS |
| Slice-scoped denominator accuracy | G-005 | PASS |
| Alternative flow isolation | No dedicated scenario | LOW RISK (structurally identical to extension mapping) |
| Rejoin outcome completeness | None | MEDIUM RISK -- FIND-QA-003 |
| Coverage computation formula accuracy | A-001 | PASS |
| Gap priority classification (failure=P0) | A-002 | PASS |

**CRYPST analog (Data Integrity / Schema Validation) -- PARTIAL PASS**

The `test-specification-v1.schema.json` schema enforces the output contract. Security assessment:

| Schema Constraint | Enforcement | Notes |
|------------------|-------------|-------|
| `source_use_case` pattern `^UC-[A-Z]+-\d{3}$` | JSON Schema | Valid constraint; lowercase domain codes rejected |
| `source_detail_level` enum `[ESSENTIAL_OUTLINE, FULLY_DESCRIBED]` | JSON Schema | Defense-in-depth: BRIEFLY_DESCRIBED files cannot masquerade as valid Feature files |
| `generated_by: const: tspec-generator` | JSON Schema immutable const | Strong provenance control; prevents fabricated Feature files from passing as tspec-generator output |
| `scenario_count minimum: 1` | JSON Schema | Prevents empty Feature files from passing schema validation |
| `coverage.total_flows minimum: 1` | JSON Schema | Correct |
| `coverage.mapped_flows >= coverage.total_flows` | NOT enforced | Schema gap -- FIND-QA-004 |
| `additionalProperties: true` | JSON Schema | Forward-compatible but accepts unknown fields; potential for schema pollution |

**AUTHZ analog (User Authority -- P-020) -- PASS**

tspec-generator's forbidden actions include explicit P-020 prohibition: "NEVER override user decisions about scenario scope, test priority, or feature file organization." The failure mode table correctly routes to H-31 (ask user) for unknown extension outcome values. tspec-analyst analogously defers coverage threshold decisions to the user. Scenario A-002 verifies that the analyst reports gaps without deciding for the user whether the coverage is acceptable (reports FAIL status and gap list, does not suppress or override).

**Constitutional Compliance (P-003, P-020, P-022) -- PASS**

| Principle | Verification | Evidence |
|-----------|-------------|---------|
| P-003 | E-001 asserts no direct agent-to-agent invocation; tspec-generator lacks Task tool in both .md frontmatter and .governance.yaml | PASS |
| P-020 | A-002 asserts FAIL status reported without suppression; failure mode table routes ambiguous extension outcomes to H-31 | PASS |
| P-022 | G-001 asserts specific coverage ratio report (scenario_count=4, coverage=100%, 4/4 flows mapped); A-001 asserts mathematically verifiable percentage (N/M = X%); RULE-QA-04 mandates reporting before writing | PASS |

**SESS (Session / State Management) -- N/A**

No session management. Both agents are T2 stateless workers. Each invocation is independent. Cross-session state is explicitly declared out of scope (no MCP persistent store).

---

### Quality Gate Verification

#### H-20 Compliance (BDD Test-First)

| H-20 Requirement | Evidence | Status |
|-----------------|----------|--------|
| BDD scenarios use Given/When/Then format | All 8 scenarios use Feature/Scenario/Given/When/Then structure | PASS |
| Scenarios have concrete inputs | Data tables with field names and values; specific paths; specific error messages | PASS |
| Assertions are verifiable and observable | All Then clauses reference file state, field values, or report content -- not internal agent state | PASS |
| Minimum 7 scenarios | 8 scenarios present (G-001 through G-005, A-001, A-002, E-001) | PASS |
| H-21 (90% line coverage) applicability | No Python implementation. /test-spec is a pure markdown/YAML skill. | N/A |

#### H-34 Compliance (Dual-File Architecture)

Both agent definitions were examined directly.

**tspec-generator.md frontmatter:**
- Official fields only: `name`, `description`, `model: sonnet`, `tools: [Read, Write, Edit, Glob, Grep, Bash]`
- No unofficial governance fields in frontmatter
- Status: PASS

**tspec-generator.governance.yaml:**
- `version: "1.0.0"` present
- `tool_tier: "T2"` present
- `identity.role` present (specific, not generic)
- `identity.expertise` has 3 entries (minimum 2 satisfied)
- `identity.cognitive_mode: "systematic"` is valid enum
- `reasoning_effort: high` at root level with documented schema compatibility rationale
- `forbidden_actions` has 5 entries; first 3 are P-003, P-020, P-022 in NPT-009-complete format
- `forbidden_action_format: "NPT-009-complete"` declared
- `constitution.principles_applied` includes P-003, P-020, P-022 (plus P-001, P-002, P-004)
- Status: PASS

**tspec-analyst.md frontmatter:**
- Official fields only: `name`, `description`, `model: sonnet`, `tools: [Read, Write, Edit, Glob, Grep, Bash]`
- No unofficial governance fields in frontmatter
- Status: PASS

**tspec-analyst.governance.yaml:**
- All required fields present and valid
- `identity.cognitive_mode: "convergent"` is valid enum (appropriate for coverage evaluation)
- `forbidden_actions` has 5 entries; all in NPT-009-complete format
- `constitution.principles_applied` includes P-003, P-020, P-022
- Tool tier note comment explains T2 vs T1 selection (write requirement)
- Status: PASS

**Worker-no-Task compliance (H-35 sub-item):**
- Neither `tspec-generator.md` nor `tspec-analyst.md` includes `Task` in the `tools` array
- Neither `.governance.yaml` includes `Task` in any tool list
- Status: PASS

#### Coverage Matrix Analysis

The BEHAVIOR_TESTS.md Coverage Matrix maps 8 scenarios to the implementation files and rules they exercise. Assessment of coverage matrix completeness:

| Coverage Matrix Entry | Accurate | Notes |
|-----------------------|---------|-------|
| G-001: RULE-C1-01, C2-01, C3-01, C5-01, C7-01, QA-01, QA-04 | Accurate | RULE-C6-01 is also exercised (preconditions -> Given clauses) but not listed |
| G-002: RULE-IV-01, guardrails.input_validation | Accurate | Scope is correct |
| G-003: RULE-C3-01, C3-02, ST-01, ST-02, ST-03 | Accurate | Full basic_flow type mapping coverage |
| G-004: RULE-C5-01, OT-01, QA-02 | Accurate | |
| G-005: RULE-SL-01, SL-02, frontmatter slice_id field | Accurate | |
| A-001: 7 Cs C1, coverage formula | Accurate | C2-C7 not individually exercised |
| A-002: gap identification, failure extension prioritization | Accurate | P1/P2/P3 priority types not exercised |
| E-001: cross-agent frontmatter contract, YAML traceability, P-003 | Accurate | Schema validation not explicitly verified |

One minor coverage matrix undercount: G-001 exercises RULE-C6-01 (Given clauses from preconditions) but the matrix does not list it. This is a documentation gap, not a functional gap.

#### Acceptance Criteria Checklist

| Check | Criterion | Status |
|-------|-----------|--------|
| H-20-01 | Minimum 7 scenarios present in Given/When/Then format | PASS (8 scenarios) |
| H-20-02 | Clark transformation happy path (basic_flow -> 1 Scenario) | PASS -- G-001, G-003 |
| H-20-03 | Clark transformation rejection gate (detail_level < ESSENTIAL_OUTLINE) | PASS -- G-002 |
| H-20-04 | Extension failure mapping (RULE-OT-01) | PASS -- G-004 |
| H-20-05 | Slice-scoped generation (RULE-SL-01, SL-02) | PASS -- G-005 |
| H-20-06 | tspec-analyst coverage computation | PASS -- A-001 |
| H-20-07 | tspec-analyst gap identification | PASS -- A-002 |
| H-20-08 | Cross-agent pipeline P-003 compliance | PASS -- E-001 |
| H-34-01 | Both agents dual-file architecture (.md + .governance.yaml) | PASS |
| H-34-02 | Constitutional triplet in forbidden_actions and principles_applied | PASS |
| FIND-QA-001 | RULE-IV-02 scenario present | FAIL -- extensions empty gate untested |
| FIND-QA-002 | RULE-IV-04 scenario present | FAIL -- step type completeness gate untested |
| FIND-QA-003 | RULE-OT-03 rejoin scenario present | FAIL -- rejoin outcome type untested |
| FIND-QA-004 | Schema enforces mapped_flows <= total_flows | FAIL -- no invariant constraint |

---

### Cross-Skill Integration Testing

#### /use-case to /test-spec Pipeline

The integration point between the two skills is the use case artifact file. The `/use-case` skill produces `.md` files with YAML frontmatter validated against `use-case-realization-v1.schema.json`. The `/test-spec` skill consumes these files via tspec-generator's RULE-IV gates.

**Pre-condition verification (RULE-IV-01 detail_level gate):**

The detail_level gate `$.detail_level >= ESSENTIAL_OUTLINE` is correctly specified and tested in G-002. The gate rejects `BRIEFLY_DESCRIBED` explicitly. The gate text in RULE-IV-01 also rejects `BULLETED_OUTLINE` but this rejection path has no BDD scenario. Given that the /use-case QA strategy (step-9-eng-qa-test-strategy.md) tested `BULLETED_OUTLINE` rejection in scenario S-002 for the uc-slicer input gate, consistency suggests a corresponding scenario should exist in BEHAVIOR_TESTS.md for tspec-generator. The absence is LOW risk because the rejection message in RULE-IV-01 is consistent: it covers both `BRIEFLY_DESCRIBED` and `BULLETED_OUTLINE` in a single conditional.

**Use case artifact detail_level gate assessment:**

| detail_level | tspec-generator behavior | Tested |
|--------------|--------------------------|--------|
| BULLETED_OUTLINE | REJECT (RULE-IV-01) | No scenario |
| BRIEFLY_DESCRIBED | REJECT (RULE-IV-01) | G-002 -- PASS |
| ESSENTIAL_OUTLINE | PASS (happy path) | G-001, G-003, G-004, G-005 -- PASS |
| FULLY_DESCRIBED | PASS (happy path superset) | No dedicated scenario |

**Clark transformation input/output mapping verification:**

The SKILL.md Core Mapping Table and the clark-transformation-rules.md rules are consistent. The sample-test-specification.md demonstrates a correct transformation from UC-LIB-001 using RULE-C1-01, C2-01, C3-01, ST-01, ST-02, ST-03, C5-01, OT-01, and C7-01. The sample output was cross-referenced against the rules and is factually correct.

One consistency check: the sample output's happy path scenario includes validation steps 2 and 3 from basic_flow mapped as When clauses (`And the system verifies that...`) rather than Then clauses. RULE-ST-03 states validation steps map to `Then assertion clause` not `When`. The sample produces `And the system verifies that member card status is valid...` inside the When block (after the actor_action step 1), which appears to be a step ordering artifact -- the sample lists step 2 (validation) after step 1 (actor_action) in the When block rather than correctly placing it in the Then block. This is a minor sample output consistency issue (LOW severity), documented as FIND-QA-005 below.

**Schema compatibility between skills:**

The `source_use_case` pattern `^UC-[A-Z]+-\d{3}$` in `test-specification-v1.schema.json` is compatible with the UC ID pattern in `use-case-realization-v1.schema.json`. The `source_detail_level` enum `[ESSENTIAL_OUTLINE, FULLY_DESCRIBED]` correctly encodes only the levels that pass the RULE-IV-01 gate. The `generated_by: const: tspec-generator` immutability constraint is a strong provenance control.

**Filesystem handoff (P-003 compliance):**

E-001 verifies the P-003 filesystem-only communication pattern. The Feature file's `source_use_case` field enables tspec-analyst to locate the source UC artifact without direct communication with tspec-generator. This design is correct and consistent with the /use-case precedent established in step-9-eng-qa-test-strategy.md (E-003 scenario).

---

## Findings

### FIND-QA-001: RULE-IV-02 Missing Test Scenario (Extensions Empty Gate)

**Severity:** MEDIUM
**OWASP Category:** INPVAL
**File:** `skills/test-spec/tests/BEHAVIOR_TESTS.md`

**Description:**
RULE-IV-02 states: "WHEN `$.extensions` is absent or empty (zero entries), REJECT the input..." This is a security-relevant input validation gate that prevents tspec-generator from producing Feature files without error scenarios. Feature files without error scenarios create a false sense of complete test coverage for high-risk paths. The gate is present in the implementation (clark-transformation-rules.md, tspec-generator.md guardrails) but has no corresponding BDD scenario in BEHAVIOR_TESTS.md.

**Evidence:**
- `clark-transformation-rules.md` RULE-IV-02: present and correctly specified
- `tspec-generator.md` `<guardrails>` Layer 2 check: "`$.extensions` absent or empty -> REJECT"
- `skills/test-spec/tests/BEHAVIOR_TESTS.md` Coverage Matrix: no scenario references RULE-IV-02
- Scenario G-002 covers RULE-IV-01 only

**Recommended Fix:**
Add scenario G-006 to BEHAVIOR_TESTS.md:

```gherkin
Scenario: G-006 -- UC with empty extensions array is rejected before Clark transformation begins

  Given a use case artifact UC-LIB-002 exists with:
    | Field        | Value             |
    | id           | UC-LIB-002        |
    | detail_level | ESSENTIAL_OUTLINE |
    | basic_flow   | 5 typed steps     |
    | extensions   | [] (empty array)  |
  And the output path is projects/${JERRY_PROJECT}/test-specs/UC-LIB-002-return-a-book.feature.md

  When tspec-generator is invoked with input UC-LIB-002

  Then tspec-generator rejects the input with the message:
    "UC UC-LIB-002 has no extensions. BDD test specifications require at least one extension to generate error scenarios. Use /use-case to add extension conditions."
  And no Feature file is written at the output path
  And no partial Gherkin content is produced
```

**Risk if unaddressed:** A UC artifact with no extensions could be passed to tspec-generator and the rejection behavior would be unverified by the test suite. This creates a regression risk: if RULE-IV-02 is accidentally removed or weakened in a future update, the test suite would not catch the regression.

---

### FIND-QA-002: RULE-IV-04 Missing Test Scenario (Step Type Completeness Gate)

**Severity:** MEDIUM
**OWASP Category:** INPVAL
**File:** `skills/test-spec/tests/BEHAVIOR_TESTS.md`

**Description:**
RULE-IV-04 states: "WHEN any `$.basic_flow[*]` step is missing the `.type` field, REJECT with..." This gate is the upstream validation that ensures Clark transformation can proceed with complete type information. Missing step type fields would produce ambiguous Gherkin (undefined When/Then clause assignment). The gate is present in both the rules file and the agent guardrails but has no BDD scenario.

**Evidence:**
- `clark-transformation-rules.md` RULE-IV-04: present and correctly specified
- `tspec-generator.md` `<guardrails>` Layer 2 check: "`$.basic_flow[*].type` missing on any step -> REJECT"
- `skills/test-spec/tests/BEHAVIOR_TESTS.md`: no scenario references RULE-IV-04
- Step-9 QA strategy precedent (A-009): the /use-case skill had a dedicated scenario for the `all_flow_steps_must_have_typed_classification` guardrail, establishing the pattern for /test-spec

**Recommended Fix:**
Add scenario G-007 to BEHAVIOR_TESTS.md:

```gherkin
Scenario: G-007 -- UC basic_flow step missing type field is rejected before Clark transformation begins

  Given a use case artifact UC-LIB-001 exists at ESSENTIAL_OUTLINE with basic_flow:
    | Step | Type         | Actor          | Action                                           |
    | 1    | actor_action | Library Member | presents library card                            |
    | 2    | (absent)     | System         | validates member card status                     |
    | 3    | validation   | System         | checks that the requested book copy is available |
  And the UC has 1 extension and 3-step basic_flow

  When tspec-generator is invoked with input UC-LIB-001

  Then tspec-generator rejects the input with the message:
    "UC UC-LIB-001 basic_flow step 2 is missing the type field. Clark transformation requires typed steps (actor_action, system_response, validation). Use /use-case to add step types."
  And no Feature file is written at the output path
```

**Risk if unaddressed:** A UC artifact where a step is missing the `.type` field could be consumed without triggering the RULE-IV-04 gate if the gate is accidentally weakened. The downstream Clark transformation would produce undefined Gherkin with no deterministic clause assignment, resulting in a Feature file that silently omits When or Then clauses for the untyped step.

---

### FIND-QA-003: No Scenario for Rejoin Outcome Type (RULE-OT-03)

**Severity:** MEDIUM
**OWASP Category:** BUSLOGIC
**File:** `skills/test-spec/tests/BEHAVIOR_TESTS.md`

**Description:**
RULE-OT-03 defines the rejoin outcome type (`outcome = "rejoin:{N}"`) which generates a structurally distinct scenario type: it must demonstrate both the deviation handling AND the successful resumption from step N of the main flow. This is the most complex scenario type in the Clark algorithm and the most likely to be incorrectly implemented. The failure outcome (RULE-OT-01) is tested in G-004, the success outcome (RULE-OT-02) is explicitly noted as out of scope in the BEHAVIOR_TESTS.md scope table, but the rejoin outcome is not covered and not scoped out with documented rationale.

**Evidence:**
- `clark-transformation-rules.md` RULE-OT-03: present with specific distinction: "Do NOT treat rejoin outcomes identically to success outcomes. A rejoin scenario must demonstrate both the deviation handling AND the successful resumption from step N."
- `tspec-generator.md` `<methodology>` Step 6: "outcome = 'rejoin:{N}' -> Additional scenario that merges back to basic flow at step N"
- `skills/test-spec/tests/BEHAVIOR_TESTS.md` scope table: "Alternative flow mapping (no alternative_flows in sample UC)" is out of scope with rationale, but rejoin outcome is not mentioned
- G-004 only covers `outcome = "failure"`; RULE-OT-02 and RULE-OT-03 are not exercised

**Recommended Fix:**
Add scenario G-008 to BEHAVIOR_TESTS.md covering the rejoin outcome type. The rejoin scenario is structurally distinct from failure and success because it requires the generated Scenario to contain: (a) extension trigger handling, AND (b) continuation of basic_flow steps from step N onward.

Additionally, update the scope table to explicitly include or exclude RULE-OT-02 (success outcome) with documented rationale to match the pattern established for alternative_flows.

**Risk if unaddressed:** RULE-OT-03 produces the most complex Clark-generated scenario. An incorrect rejoin scenario would omit the resumption steps, creating a scenario that verifies error handling but not successful error recovery. For systems with retry/recovery flows, this gap would leave the recovery path untested.

---

### FIND-QA-004: Schema coverage.mapped_flows Can Exceed total_flows

**Severity:** LOW
**OWASP Category:** CRYPST analog (Data Integrity)
**File:** `docs/schemas/test-specification-v1.schema.json`

**Description:**
The `test-specification-v1.schema.json` schema does not enforce the mathematical invariant `coverage.mapped_flows <= coverage.total_flows`. The schema defines `total_flows` minimum: 1 and `mapped_flows` minimum: 0, but no relational constraint between the two fields. A tspec-generator defect or a manually constructed Feature file could set `mapped_flows: 10` and `total_flows: 4`, producing a coverage percentage > 100% that would pass schema validation.

JSON Schema Draft 2020-12 supports relational constraints via `if/then` conditional schemas or custom keywords, but these are not used here. The `additionalProperties: true` setting also allows undeclared fields to pass without validation.

**Evidence:**
- `docs/schemas/test-specification-v1.schema.json` lines 89-97: `mapped_flows` minimum: 0, no maximum, no relational constraint to `total_flows`
- `tspec-generator.md` RULE-QA-04 mandates reporting `coverage ratio: (1+N+M) / total_mappable_flows` before writing, which provides a behavioral check, but no schema-level enforcement
- Step-9 precedent: `use-case-realization-v1.schema.json` `additionalProperties: true` was noted in the step-9 QA as a schema pollution risk (RISK-04)

**Recommended Fix:**
Consider adding a documentation comment or custom validation note to the schema clarifying the expected invariant. Full relational constraint enforcement would require `if/then` schema constructs or a JSON Schema validator that supports Draft 2020-12 format assertions. At minimum, add a `$comment` to the `coverage` object:

```json
"$comment": "Invariant: mapped_flows <= total_flows. Schema validation does not enforce this relational constraint; tspec-generator RULE-QA-01 enforces it behaviorally. A mapped_flows value exceeding total_flows indicates a tspec-generator defect."
```

This is LOW severity because RULE-QA-01 enforces the 1:1 cardinality guarantee behaviorally, and the relational schema constraint would require significant schema complexity for marginal gain.

---

### FIND-QA-005: Sample Output Has Validation Steps in When Block (Minor Consistency)

**Severity:** LOW
**OWASP Category:** Documentation / Template Fidelity
**File:** `skills/test-spec/samples/sample-test-specification.md`

**Description:**
In the sample output for UC-LIB-001, basic_flow steps 2 and 3 are typed as `validation` steps. Per RULE-ST-03, validation steps should map to `Then assertion clauses` (not When). However, in the sample-test-specification.md happy path scenario, the validation content appears inline with the When block:

```gherkin
When Library Member presents library card and requests a specific book copy at the circulation desk
  And the system verifies that member card status is valid and no overdue loans exist
  And the system verifies that the requested book copy is available for loan
  And Library Member confirms the loan and accepts the due date
Then the system creates a loan record...
```

Steps 2 and 3 (validation) are rendered as `And` clauses in the When block rather than as `Then` assertion clauses. The BEHAVIOR_TESTS.md Scenario G-003 assertion at line 208-210 states: "steps 2 and 3 (validation) produce Then assertion clauses containing 'the system verifies that'" -- which is the correct behavior per RULE-ST-03. The sample output thus demonstrates behavior that contradicts the BDD test assertion G-003 specifies.

**Evidence:**
- `sample-test-specification.md` lines 44-52: validation steps appear as `And` in When block
- `BEHAVIOR_TESTS.md` G-003 assertion lines 208-210: asserts validation steps produce `Then` assertion clauses
- `clark-transformation-rules.md` RULE-ST-03: "validation step type maps to Then assertion clause"

**Risk if unaddressed:** Users consulting the sample output as reference will learn incorrect clause placement for validation steps. This creates a feedback loop where manually-authored Feature files (not generated by tspec-generator) place validation steps in the wrong clause position, potentially confusing human reviewers.

**Recommended Fix:** Update the sample-test-specification.md happy path scenario to correctly place validation steps as Then clauses per RULE-ST-03. The corrected scenario would be:

```gherkin
Given Library Member holds a valid, active library card
  And Library Member has no outstanding overdue books
When Library Member presents library card and requests a specific book copy at the circulation desk
  And Library Member confirms the loan and accepts the due date
Then the system verifies that member card status is valid and no overdue loans exist
  And the system verifies that the requested book copy is available for loan
  And the system creates a loan record, updates the book copy status to CHECKED_OUT, and prints a due-date slip
  And loan record is created linking the member to the book copy
  And book copy status is changed to CHECKED_OUT
  And due date is issued to the member
```

---

## L2: Strategic Implications

### Test Strategy Effectiveness Assessment

The 8-scenario BDD specification represents an appropriate baseline for a new skill. Compared to the /use-case skill's QA strategy (26 primary scenarios), the /test-spec strategy is leaner (8 scenarios) but targets the highest-risk paths correctly: the Clark mapping algorithm, the rejection gates, and the pipeline integration. The minimum-viable test suite philosophy is acceptable given that:

1. The transformation is deterministic (Clark algorithm), not probabilistic, reducing the combinatorial test space
2. The schema provides a complementary validation layer (Layer 1) that catches structural defects independently of BDD scenarios
3. The sample output provides additional validation of the expected transformation result

The three MEDIUM findings (FIND-QA-001, -002, -003) represent regression risks for the three input validation gates and the most complex outcome type. Addressing these would bring the scenario count to 11 (still lean by /use-case standards) while closing the most significant behavioral gaps.

**Coverage ROI estimate by finding:**

| Finding | Effort to Fix | Regression Risk if Unfixed |
|---------|--------------|---------------------------|
| FIND-QA-001 (RULE-IV-02) | Low (1 scenario, ~15 lines) | Medium (extensions gate could regress silently) |
| FIND-QA-002 (RULE-IV-04) | Low (1 scenario, ~15 lines) | Medium (step type gate is critical for downstream Clark) |
| FIND-QA-003 (RULE-OT-03) | Medium (1 scenario, ~25 lines; rejoin is complex) | Medium (most complex Clark scenario type) |
| FIND-QA-004 (schema invariant) | Low ($comment only) | Low (RULE-QA-01 behavioral check is present) |
| FIND-QA-005 (sample fidelity) | Low (reorder clauses in sample) | Low (only affects human readers, not generator behavior) |

### Coverage Gaps and Risk Implications

| Gap | Risk Level | Implication | Mitigation Path |
|-----|-----------|-------------|-----------------|
| RULE-IV-02 scenario absent | MEDIUM | Extensions empty gate unverified; regression possible | Add G-006 per FIND-QA-001 |
| RULE-IV-04 scenario absent | MEDIUM | Step type gate unverified; downstream Clark undefined if regressed | Add G-007 per FIND-QA-002 |
| RULE-OT-03 rejoin scenario absent | MEDIUM | Most complex outcome type unverified; error recovery paths untested | Add G-008 per FIND-QA-003 |
| RULE-C4-01 (alternative flows) scenario absent | LOW | Structurally identical to extension mapping; low risk | Add as optional future scenario |
| FULLY_DESCRIBED detail level path | LOW | Superset of ESSENTIAL_OUTLINE; schema and gates are identical | Not a gap -- ESSENTIAL_OUTLINE tests exercise the same code path |
| BULLETED_OUTLINE rejection path | LOW | RULE-IV-01 covers both BRIEFLY_DESCRIBED and BULLETED_OUTLINE in one gate | Not a critical gap; G-002 exercises the gate |
| 7 Cs C2-C7 quality criteria | LOW | C1 Coverage is the primary criterion; C2-C7 are structural quality checks | Acceptable deferral; add in future iteration |
| Unknown step type handling | LOW | Agent failure mode table covers this via H-31 escalation; no schema enforcement possible | Document in scope table; LOW risk |

### Regression Suite Maintenance

BEHAVIOR_TESTS.md (F-15) is the authoritative regression specification for the /test-spec skill. Required updates when the following changes occur:

| Change Type | Required Update |
|-------------|----------------|
| Clark rule additions (e.g., new outcome type beyond failure/success/rejoin) | Add scenario for new outcome type mapping |
| New RULE-IV rejection gate (e.g., new structural prerequisite for Clark) | Add negative scenario for new rejection path |
| Schema version bump (new required field in test-specification-v1.schema.json) | Add E-series scenario for new schema constraint |
| 7 Cs framework extension (new quality criterion) | Add A-series scenario for new criterion |
| Slice-scoped generation expansion (multi-slice coverage) | Add G-series scenario for multi-slice edge case |
| tspec-analyst worktracker integration (future P-003 Bash path) | Add E-series scenario mirroring /use-case S-009 pattern |

### Handoff to eng-security

For manual security review, the three behavioral areas warranting the most attention are:

1. **Content integrity of generated Gherkin** (injection analog): tspec-generator derives all Gherkin text from UC artifact field values via `$.` path lookups. A UC artifact with adversarially crafted field values (e.g., Gherkin control characters, Markdown injection in action fields) would be reproduced verbatim in the Feature file. The manual review should verify whether the `all_then_clauses_must_derive_from_postconditions_or_system_responses` output filter is sufficient to bound this risk.

2. **RULE-OT-03 rejoin scenario complexity** (FIND-QA-003): The rejoin outcome type produces the most complex Gherkin output. Manual review should trace the rejoin scenario generation path in tspec-generator.md methodology Step 6 against RULE-OT-03 in clark-transformation-rules.md to verify that the "additional Then clauses for remaining basic_flow steps from step N onward" (RULE-OT-03) are correctly applied.

3. **tspec-analyst modification prohibition** (ANALYSIS VIOLATION forbidden action): The forbidden action "NEVER modify Feature files or use case artifacts during analysis" is critical for provenance integrity. Manual review should verify that the tspec-analyst guardrails section and output constraints section both explicitly prohibit writes to input files, and that the post_completion_checks do not inadvertently permit edit operations.

---

## S-010 Self-Review

> Pre-delivery self-review per H-15 (S-010 required before presenting any deliverable).

| Check | Question | Result |
|-------|----------|--------|
| Evidence-based | Are all findings backed by specific file and line citations? | PASS -- all 5 findings cite exact file names, sections, and behavioral descriptions |
| No fabrication | Were any findings invented without evidence? | PASS -- all findings trace to identified gaps in BEHAVIOR_TESTS.md or schema |
| Coverage completeness | Are all 8 required assessment areas addressed? | PASS -- test strategy, security, quality gate, cross-skill integration all present |
| L0/L1/L2 structure | All three levels present? | PASS |
| Severity calibration | Are severities appropriate per OWASP risk assessment? | PASS -- no CRITICAL (no executable code, no auth surface), 3 MEDIUM (behavioral gaps), 2 LOW |
| H-34 evidence | Was H-34 dual-file architecture actually examined? | PASS -- both .md and .governance.yaml files read and field-by-field verified |
| Step-9 structural consistency | Does structure follow step-9-eng-qa-test-strategy.md pattern? | PASS -- L0/L1/L2, OWASP categories, security assessment, gap table, regression suite |
| No scope creep | Are findings limited to QA domain (not production code rewrite requests)? | PASS -- all findings are behavioral test gaps or spec clarifications |
| Actionability | Does each finding include a recommended fix? | PASS -- FIND-QA-001 through FIND-QA-005 each include recommended fix or code sample |
| P-002 compliance | Output persisted to file at correct path? | PASS -- written to `projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/implementation/step-10-eng-qa-review.md` |

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-03-09 | eng-qa | Initial security QA review |

---

*QA Review Version: 1.0.0 | Agent: eng-qa | Date: 2026-03-09*
*Input artifacts: step-10-test-spec-architecture.md (v1.1.0), step-10-eng-lead-review.md (v1.1.0), step-10-eng-backend-implementation.md (v1.1.0)*
*Key files examined: BEHAVIOR_TESTS.md, tspec-generator.md, tspec-generator.governance.yaml, tspec-analyst.md, tspec-analyst.governance.yaml, clark-transformation-rules.md, test-specification-v1.schema.json, sample-test-specification.md*
*Next step: step-10-eng-security-review.md (manual security review)*
