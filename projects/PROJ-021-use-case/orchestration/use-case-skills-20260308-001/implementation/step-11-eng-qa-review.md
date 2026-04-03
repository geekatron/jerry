# Security QA Review: /contract-design Skill

> **PS ID:** proj-021 | **Entry ID:** step-11-eng-qa-review | **Workflow ID:** use-case-skills-20260308-001
> **Date:** 2026-03-09 | **Agent:** eng-qa | **Step:** 11 (Phase 3 Implementation)
> **Input:** step-11-contract-design-architecture.md (v1.1.0, PASSED 0.956), step-11-eng-lead-review.md (v1.0.0, PASSED), step-11-eng-backend-adv-score.md (0.959 PASS), skills/contract-design/tests/BEHAVIOR_TESTS.md (F-16, v1.0.0)
> **Status:** PROPOSED
> **Version:** 1.0.0

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Coverage summary, defects found, overall security assessment |
| [L1: Technical Detail](#l1-technical-detail) | Scenario-level test assessment with evidence |
| [Test Strategy Assessment](#test-strategy-assessment) | BEHAVIOR_TESTS.md evaluation: BDD format, coverage, edge cases |
| [Transformation Rule Coverage](#transformation-rule-coverage) | All 24 RULE-* rules mapped to scenarios with gap analysis |
| [Agent Methodology Coverage](#agent-methodology-coverage) | cd-generator 9-step algorithm and cd-validator 9-step protocol coverage |
| [Error Path Coverage](#error-path-coverage) | Rejection gates, failure outcomes, mandatory FAIL paths |
| [Template Coverage](#template-coverage) | OpenAPI template and mapping template test presence |
| [PROTOTYPE Label Coverage](#prototype-label-coverage) | RULE-TR-02 and Step 7 enforcement verification |
| [Cross-Skill Integration Tests](#cross-skill-integration-tests) | /use-case to /contract-design pipeline validation |
| [Security Test Assessment](#security-test-assessment) | OWASP-category evaluation, guardrail effectiveness, constitutional compliance |
| [H-20 Compliance](#h-20-compliance) | BDD format compliance and minimum scenario count verification |
| [Test Quality Metrics](#test-quality-metrics) | Assertion concreteness, fixture completeness, traceability |
| [Findings](#findings) | All findings with severity classification (CRITICAL/HIGH/MEDIUM/LOW) |
| [Coverage Gap Matrix](#coverage-gap-matrix) | All 24 rules mapped to scenarios with gap status |
| [Recommendations](#recommendations) | Prioritized remediation actions |
| [L2: Strategic Implications](#l2-strategic-implications) | Test strategy effectiveness, coverage gaps, regression suite considerations |
| [S-010 Self-Review](#s-010-self-review) | Pre-delivery self-review checklist |

---

## L0: Executive Summary

The `/contract-design` skill has been implemented across 17 files (F-01 through F-17). This QA review evaluated `skills/contract-design/tests/BEHAVIOR_TESTS.md` (F-16, 10 scenarios), both agent definitions (`cd-generator`, `cd-validator`), the UC-to-contract transformation rules (`uc-to-contract-rules.md`, 24 rules), the governance files (`cd-generator.governance.yaml`, `cd-validator.governance.yaml`), and the four template files (`openapi-template.yaml`, `mapping-template.md`, `AsyncAPI-template.yaml`, `cloudevents-template.yaml`) against OWASP Testing Guide categories, H-20 (BDD test-first), and H-34 (dual-file agent architecture).

**Overall Assessment: PASS with findings.** The skill is structurally sound, constitutionally compliant, and the 10 BDD scenarios exceed the architecture-specified minimum of 9. The two core agents demonstrate appropriate separation of concerns (creator: cd-generator; critic: cd-validator), correct tool tier (T2), and complete constitutional triplet compliance (P-003, P-020, P-022). Six findings are raised, zero CRITICAL, all addressable without architectural change.

**Security defects found during test design: 0.** No implementation defects were identified. Six behavioral and documentation gaps were found in the test specification scope: two MEDIUM-severity coverage gaps in cd-validator step testing, one MEDIUM-severity rules documentation inconsistency, one MEDIUM-severity Layer 2 guardrail field name error (carryforward from adversary score FIND-005), and two LOW-severity gaps in rule coverage.

**Scenario count summary:**

| Feature | Scenarios | Coverage Type |
|---------|-----------|---------------|
| cd-generator Agent | 6 (G-001 through G-006) | 2 happy, 1 rejection, 2 edge, 1 error-mapping |
| cd-validator Agent | 3 (V-001 through V-003) | 1 happy, 1 traceability gap, 1 mandatory FAIL |
| Cross-Agent Pipeline | 1 (E-001) | 1 integration end-to-end |
| **Total** | **10** | Exceeds H-20 minimum (9 required per architecture) |

**Findings summary:**

| ID | Severity | Category | Title |
|----|----------|----------|-------|
| FIND-QA-001 | MEDIUM | Documentation | Rules file nav table states "22 rules" but 24 rules are present |
| FIND-QA-002 | MEDIUM | BUSLOGIC | cd-validator Steps 3, 4, 5, 6, 8, 9 have no dedicated test scenarios |
| FIND-QA-003 | MEDIUM | INPVAL | Layer 2 guardrail uses `detail_level` field name instead of `realization_level` |
| FIND-QA-004 | MEDIUM | INPVAL | RULE-OM-03 (system_role = initiator → server-to-server mapping) has no dedicated scenario |
| FIND-QA-005 | LOW | INPVAL | RULE-ER-02 (success extension → 2xx response variant) has no dedicated scenario |
| FIND-QA-006 | LOW | INPVAL | Slug sanitization not present in agent output_filtering guardrail lists |

---

## L1: Technical Detail

### Test Strategy Assessment

#### BDD Format Compliance

All 10 scenarios in BEHAVIOR_TESTS.md conform to the canonical Gherkin structure documented in the Overview Methodology section: `Feature` / `Background` / `Scenario` / `Given` / `When` / `Then` / `And`. The format is consistent across all three Features. No ambiguous `But` or `*` wildcards are used. The Background blocks in each Feature correctly establish shared preconditions (tool availability, artifact accessibility) and avoid duplicating setup logic across individual scenarios.

**Concrete input quality:** All scenarios include data tables or specific field values rather than abstract descriptions. G-001 provides a 9-field table for the UC artifact structure including interaction-level fields (INT-01.actor_role, INT-01.request_description, INT-01.preconditions); G-004 provides the specific ambiguous request_description text that triggers the low-confidence path; G-006 provides anchor_step and extension condition text verbatim. Assertions in all 10 scenarios reference observable artifact state (file written at specific path, specific field values present, specific error message text) rather than internal agent state. This satisfies the H-20 requirement for verifiable assertions.

**Scenario ordering within Features:** Within each Feature, scenarios progress from happy path through rejection and edge cases, consistent with the methodology statement in the Overview. G-001 (happy path full generation) precedes G-002 (rejection), then G-003/G-004 (HTTP method inference edge cases), G-005 (PROTOTYPE label invariant), G-006 (error-response mapping). This ordering provides progressive complexity and facilitates debugging when a later scenario fails.

#### Scenario Coverage Analysis

**Scenarios exercised per feature:**

| Feature | Scenario | Type | Primary Rule/Step |
|---------|----------|------|-------------------|
| cd-generator | G-001 | Happy path | RULE-RI-01, RULE-OM-01/02, RULE-HM-02, RULE-SD-01/02, RULE-AR-01, RULE-TR-01/02 |
| cd-generator | G-002 | Rejection | Layer 2 input gate (no interactions block) |
| cd-generator | G-003 | Edge | RULE-HM-02 (create semantics → POST, high confidence) |
| cd-generator | G-004 | Edge | RULE-HM-05 (ambiguous verb → POST, low confidence annotation) |
| cd-generator | G-005 | Invariant | RULE-TR-02 (x-prototype: true mandatory) |
| cd-generator | G-006 | Error mapping | RULE-ER-01d (failure extension → 409 Conflict) |
| cd-validator | V-001 | Happy path | Step 1 (Structural Validity PASS) |
| cd-validator | V-002 | Traceability gap | Step 2 (Path Completeness, coverage < 100% FAIL) |
| cd-validator | V-003 | Mandatory FAIL | Step 7 (PROTOTYPE Label absence, no override) |
| Cross-Agent Pipeline | E-001 | Integration | P-003 filesystem handoff, all 9 validator steps via pipeline |

**Coverage distribution:** 20% happy path (2 scenarios), 30% rejection/mandatory FAIL (3 scenarios), 50% edge cases and integration (5 scenarios). This distribution appropriately weights regression value over completeness testing for a deterministic transformation skill.

**BEHAVIOR_TESTS.md internal consistency note (QA observation):** The Acceptance Verification Checklist entry for "Scenario count" correctly states "10 scenarios," consistent with the actual 10 scenarios present. The scenario numbering is consistent (G-001 through G-006, V-001 through V-003, E-001) with no gaps or duplicates. The Coverage Matrix lists all 10 scenarios with rules or steps covered — this is complete and correct.

---

### Transformation Rule Coverage

This section maps all 24 RULE-* transformation rules against the 10 BDD scenarios. The rules file `skills/contract-design/rules/uc-to-contract-rules.md` contains 24 rules across 7 categories: RULE-RI (3 rules), RULE-OM (4 rules), RULE-HM (5 rules), RULE-SD (4 rules), RULE-ER (3 rules), RULE-AR (3 rules), RULE-TR (2 rules).

**Note:** The rules file navigation table section header states "all 22 rules" but the actual rule count is 24. The Rule Summary Index contains 25 rows (24 named parent rules plus 1 aggregate RULE-ER-01a-f row). A grep of the rules file for `^\*\*RULE-` yields 24 distinct entries. This is FIND-QA-001.

#### Category RULE-RI: Resource Identification (3 rules)

| Rule | ID | Description | Tested By | Gap Status |
|------|-----|-------------|-----------|------------|
| RULE-RI-01 | Resource naming: noun-pluralized path from interaction intent | G-001 (`/loans` path from "Borrow a Book" loan operation) | COVERED |
| RULE-RI-02 | Sub-resource nesting: parent-child path composition | None | GAP: No scenario exercises nested paths (e.g., `/members/{id}/loans`) |
| RULE-RI-03 | Path parameter extraction: ID-carrying interactions | None | GAP: No scenario exercises `{id}` path parameters |

**RULE-RI coverage: 1/3 = 33%.** RULE-RI-02 and RULE-RI-03 are untested. The gap risk is LOW: sub-resources and path parameters are structurally analogous to the base path case; however, the inference algorithm for these rules involves distinct naming heuristics that differ from RULE-RI-01.

#### Category RULE-OM: Operation Mapping (4 rules)

| Rule | ID | Description | Tested By | Gap Status |
|------|-----|-------------|-----------|------------|
| RULE-OM-01 | Consumer interaction → external operation | G-001 (INT-01 → POST /loans operation present) | COVERED |
| RULE-OM-02 | Operation metadata: operationId, summary, tags | G-001 (operationId: createLoan verified) | COVERED |
| RULE-OM-03 | System_role = initiator interaction → server-to-server operation documentation | None | GAP: No scenario uses actor_role = initiator; see FIND-QA-004 |
| RULE-OM-04 | Provider interaction → x-internal-operations entry | G-001 (3 provider interactions → 3 x-internal-operations entries verified) | COVERED (implicitly via G-001 count assertion) |

**RULE-OM coverage: 3/4 = 75%.** RULE-OM-03 has no dedicated scenario. RULE-OM-04 is asserted in G-001 via the count assertion ("contains 3 entries (INT-02, INT-03, INT-04)") but the field-level content of each x-internal-operations entry (interaction_id, source_step, description fields per Step 8) is not individually verified.

#### Category RULE-HM: HTTP Method Inference (5 rules)

| Rule | ID | Description | Tested By | Gap Status |
|------|-----|-------------|-----------|------------|
| RULE-HM-01 | Retrieve/query semantics → GET | None | GAP: No scenario tests GET method inference |
| RULE-HM-02 | Create/submit semantics → POST | G-001 (implicit, POST /loans), G-003 (explicit: "submits a new loan request" → POST + high confidence) | COVERED |
| RULE-HM-03 | Replace/update semantics → PUT | None | GAP: No scenario tests PUT method inference |
| RULE-HM-04 | Partial update semantics → PATCH | None | GAP: No scenario tests PATCH method inference |
| RULE-HM-05 | Ambiguous/unclassifiable → POST + x-method-inference: low | G-004 ("performs the loan operation" → POST + low confidence annotation) | COVERED |

**RULE-HM coverage: 2/5 = 40%.** RULE-HM-01 (GET), RULE-HM-03 (PUT), RULE-HM-04 (PATCH) have no dedicated scenarios. This represents the largest individual gap in the transformation rule coverage. The gap risk is MEDIUM: each of these methods requires distinct verb-pattern recognition in the inference algorithm, and their absence from the test specification means regression is undetected if the algorithm is implemented incorrectly for retrieve, replace, or partial-update semantics.

**Assessment:** The existing HM coverage (G-003 for high-confidence POST, G-004 for ambiguous fallback) demonstrates the confidence annotation mechanism correctly. However, the three missing method types are sufficiently distinct that test scenarios for them provide meaningful regression value.

#### Category RULE-SD: Schema Definition (4 rules)

| Rule | ID | Description | Tested By | Gap Status |
|------|-----|-------------|-----------|------------|
| RULE-SD-01 | Request body schema from interaction preconditions | G-001 (requestBody.required: true present, CreateLoanRequest in schemas) | COVERED |
| RULE-SD-02 | Response schema from interaction postconditions | G-001 (CreateLoanResponse in components.schemas) | COVERED |
| RULE-SD-03 | Enum field generation from constrained value sets | None | GAP: No scenario exercises enum type inference |
| RULE-SD-04 | Optional vs required field classification | None | GAP: No scenario tests required array vs optional field placement in schema |

**RULE-SD coverage: 2/4 = 50%.** RULE-SD-03 and RULE-SD-04 are untested. The gap risk is LOW: enum inference and field classification are orthogonal to the path/operation generation tested in G-001, but the absence means schema-level correctness is asserted only at the presence level (schema exists) rather than at the structural level (schema contents are correct).

#### Category RULE-ER: Extension-to-Error-Response Mapping (3 rules)

| Rule | ID | Description | Tested By | Gap Status |
|------|-----|-------------|-----------|------------|
| RULE-ER-01 | Failure extension → 4xx response (sub-rules a-f for status code classification) | G-006 (RULE-ER-01d: conflict condition → 409 Conflict) | PARTIALLY COVERED (1 of 6 sub-rules tested) |
| RULE-ER-02 | Success extension → 2xx response variant | None | GAP: No scenario tests success extensions; see FIND-QA-005 |
| RULE-ER-03 | Extension annotation: x-source-extension mandatory | G-006 (x-source-extension: "EXT-2a" verified in 409 response) | COVERED |

**RULE-ER coverage: 2/3 = 67% (parent rules); 2/8 = 25% counting sub-rules.** G-006 exercises RULE-ER-01d (conflict → 409) and RULE-ER-03 (annotation). The remaining 5 sub-rules (RULE-ER-01a through 01f excluding 01d: validation error, not found, authorization, rate limit, server error classifications) are untested. RULE-ER-02 (success extension → 2xx variant) is fully untested.

**Assessment:** G-006 demonstrates the sub-rule selection mechanism for one case. The other 5 sub-rule cases follow the same algorithmic path with different status code outputs; the risk of regression is MEDIUM because each sub-rule's condition pattern must be recognized separately.

#### Category RULE-AR: Annotation Requirements (3 rules)

| Rule | ID | Description | Tested By | Gap Status |
|------|-----|-------------|-----------|------------|
| RULE-AR-01 | x-source-interaction annotation on every external operation | G-001 (x-source-interaction: "INT-01" verified on POST /loans) | COVERED |
| RULE-AR-02 | x-source-step annotation on every external operation | G-001 (x-source-step: 1 verified) | COVERED |
| RULE-AR-03 | x-source-flow annotation on every external operation | G-001 (x-source-flow: "basic_flow" verified) | COVERED |

**RULE-AR coverage: 3/3 = 100%.** All three annotation rules are covered in G-001. The assertions are specific (exact field names and values in a data table). This is the strongest coverage category.

#### Category RULE-TR: Traceability Requirements (2 rules)

| Rule | ID | Description | Tested By | Gap Status |
|------|-----|-------------|-----------|------------|
| RULE-TR-01 | Mapping document written alongside contract | G-001 (mapping document at UC-LIB-001-borrow-a-book-mapping.md verified present), G-005 (mapping document contains "PROTOTYPE STATUS" section) | COVERED |
| RULE-TR-02 | x-prototype: true mandatory in info section | G-001 (info.x-prototype: true in assertions), G-005 (dedicated PROTOTYPE invariant test), V-003 (validator mandatory FAIL for absence) | COVERED — strongest coverage in the file |

**RULE-TR coverage: 2/2 = 100%.** RULE-TR-02 in particular is verified from three angles: generation (G-001, G-005), and validation (V-003). This reflects the architectural decision to treat PROTOTYPE label enforcement as the highest-priority safety gate.

#### Overall Transformation Rule Coverage Summary

| Category | Rules | Covered | Partial | Gap | Coverage % |
|----------|-------|---------|---------|-----|------------|
| RULE-RI (Resource ID) | 3 | 1 | 0 | 2 | 33% |
| RULE-OM (Operation Mapping) | 4 | 3 | 1 | 1 | 75% |
| RULE-HM (HTTP Method) | 5 | 2 | 0 | 3 | 40% |
| RULE-SD (Schema Definition) | 4 | 2 | 0 | 2 | 50% |
| RULE-ER (Extension-to-Error) | 3 | 2 | 1 | 1 | 67% (parent) |
| RULE-AR (Annotation) | 3 | 3 | 0 | 0 | 100% |
| RULE-TR (Traceability) | 2 | 2 | 0 | 0 | 100% |
| **Total** | **24** | **15** | **2** | **9** | **63%** |

**Assessment:** 63% dedicated rule coverage (15 fully covered, 2 partially covered across 24 rules). The gap distribution is concentrated in method inference (RULE-HM) and resource identification variants (RULE-RI-02/03). The 100% coverage of the annotation (RULE-AR) and traceability (RULE-TR) categories reflects deliberate prioritization of the most critical safety properties.

---

### Agent Methodology Coverage

#### cd-generator: 9-Step UC-to-Contract Algorithm Coverage

The cd-generator methodology executes a 9-step algorithm (documented in `skills/contract-design/agents/cd-generator.md`, `<methodology>` section). Coverage assessment per step:

| Step | Name | Exercised By | Coverage Assessment |
|------|------|-------------|---------------------|
| Step 1 | Validate UC artifact (Layer 2 gate) | G-002 (rejection: no interactions), G-001 (pass through) | COVERED — both gate-pass and gate-fail paths |
| Step 2 | Extract interactions and classify by actor_role | G-001 (1 consumer + 3 provider correctly classified), E-001 | COVERED |
| Step 3 | Infer resource paths (RULE-RI-01 through RI-03) | G-001 (RULE-RI-01 only: `/loans` path) | PARTIALLY COVERED — only RI-01 path tested |
| Step 4 | Infer HTTP method (RULE-HM-01 through HM-05) | G-003 (RULE-HM-02), G-004 (RULE-HM-05) | PARTIALLY COVERED — 3 of 5 HM rules untested |
| Step 5 | Generate request/response schemas (RULE-SD-01 through SD-04) | G-001 (SD-01, SD-02 presence asserted) | PARTIALLY COVERED — SD-03, SD-04 untested; presence not structure |
| Step 6 | Map extensions to error responses (RULE-ER-01 through ER-03) | G-006 (RULE-ER-01d, ER-03) | PARTIALLY COVERED — 5 of 6 ER-01 sub-rules untested |
| Step 7 | Apply annotation requirements (RULE-AR-01 through AR-03) | G-001 (all 3 AR rules verified) | FULLY COVERED |
| Step 8 | Document internal operations (x-internal-operations) | G-001 (count assertion: 3 entries for INT-02/03/04) | PARTIALLY COVERED — field-level content not asserted |
| Step 9 | Apply traceability requirements (RULE-TR-01, TR-02) | G-001, G-005, E-001 | FULLY COVERED |

**Summary:** Steps 7 and 9 are fully covered. Steps 1 and 2 are covered for both success and failure paths. Steps 3, 4, 5, 6, and 8 are partially covered — each has at least one scenario but leaves branches or sub-rules untested. This is a reasonable distribution for a v1.0.0 test specification on a C3 deliverable.

#### cd-validator: 9-Step Validation Protocol Coverage

The cd-validator executes a 9-step validation protocol (documented in `skills/contract-design/agents/cd-validator.md`, `<methodology>` section). Coverage assessment per step:

| Step | Name | Exercised By | Coverage Assessment |
|------|------|-------------|---------------------|
| Step 1 | Structural Validity | V-001 (PASS path: valid OpenAPI 3.1 YAML) | COVERED — PASS path only |
| Step 2 | Path Completeness (Traceability) | V-002 (FAIL: unmapped consumer interaction, coverage 1/2 = 50%) | COVERED — FAIL path with specific gap |
| Step 3 | Operation Correctness (HTTP semantics) | E-001 (implicit: all 9 steps have PASS verdicts) | NOT DEDICATED — E-001 integration assertion only |
| Step 4 | Schema Completeness | E-001 (implicit: all 9 steps have PASS verdicts) | NOT DEDICATED — E-001 integration assertion only |
| Step 5 | Error Response Mapping | E-001 (implicit: all 9 steps have PASS verdicts) | NOT DEDICATED — E-001 integration assertion only |
| Step 6 | Traceability Annotations | E-001 (implicit: all 9 steps have PASS verdicts) | NOT DEDICATED — E-001 integration assertion only |
| Step 7 | PROTOTYPE Label Verification | V-003 (mandatory FAIL: x-prototype absent, no override) | FULLY COVERED — mandatory FAIL and no-override verified |
| Step 8 | Internal Operations Documentation | E-001 (implicit: all 9 steps have PASS verdicts) | NOT DEDICATED — E-001 integration assertion only |
| Step 9 | IC-05 Supporting Actor Resolution | E-001 (implicit: all 9 steps have PASS verdicts) | NOT DEDICATED — E-001 integration assertion only |

**Summary:** Steps 1, 2, and 7 have dedicated scenarios with verifiable assertions. Steps 3, 4, 5, 6, 8, and 9 are covered only by the implicit assertion in E-001 that "all 9 validation steps have PASS verdicts." This is FIND-QA-002. The E-001 implicit coverage means these steps are not regression-tested independently — a defect in Step 4 (Schema Completeness) or Step 9 (Supporting Actor Resolution) would not be surfaced by the current test suite unless E-001 specifically fails.

**FAIL path coverage gap:** Steps 1, 3, 4, 5, 6, 8, and 9 have no FAIL-path scenarios. Steps 1's FAIL path (missing required fields, invalid openapi version) is untested. Step 3's FAIL path (HTTP method mismatch) is untested. Step 5's FAIL path (extension without error response) is partially related to RULE-ER-02 gap (FIND-QA-005). The absence of FAIL-path scenarios for Steps 3, 4, 5, 6, 8, 9 is captured in FIND-QA-002.

---

### Error Path Coverage

Error paths are paths where the agent correctly rejects input or produces a FAIL verdict. This is a security-critical test category because error paths enforce the trust boundary between caller-supplied input and agent processing.

#### cd-generator Error Paths

| Error Path | Scenario | Assertion Quality |
|------------|----------|-------------------|
| Missing interactions block → REJECT | G-002 | Strong — error message content and guidance text verified |
| UC at wrong realization_level | G-002 (implicitly via STORY_DEFINED) | Present — realization_level: STORY_DEFINED in Given table |
| Unparseable YAML input | None | GAP — agent behavior for malformed YAML input is not tested |
| Contract file already exists at output path | None | GAP — no test for overwrite behavior or conflict resolution |

**Assessment:** G-002 demonstrates the primary rejection gate well. The error message assertion in G-002 is particularly strong: it verifies both the error content ("UC UC-LIB-001 has no interactions block") and the guidance text (directing the user to /use-case Activity 5). This satisfies the OWASP INPVAL requirement for informative but non-leaking error messages.

The absence of a test for malformed YAML input and output path conflict is a LOW gap — both are edge cases unlikely in the defined skill workflow, but the agent's behavior in these cases is unspecified by the test suite.

#### cd-validator Error Paths

| Error Path | Scenario | Assertion Quality |
|------------|----------|-------------------|
| Missing consumer interaction → FAIL | V-002 | Strong — specific gap interaction ID (INT-06), coverage formula (1/2 = 50%), traceability matrix entry |
| x-prototype: true absent → mandatory FAIL | V-003 | Strongest in file — exact FAIL message text verified, no-override verified |
| Invalid YAML contract → REJECT | None | GAP — agent pre-parse rejection path untested |
| Source UC artifact missing → REJECT | None | GAP — artifact_path does not exist path untested |

**Assessment:** V-003 has the strongest assertions in the entire test file: it verifies the verbatim failure message from the guardrail specification, confirms the overall verdict is FAIL regardless of other step results, and confirms the no-override property. This is the correct treatment for a mandatory FAIL gate.

The absence of test scenarios for the two Layer 2 reject conditions (invalid YAML, missing artifact path) is a LOW gap. These conditions are defined in `cd-validator.md` `<guardrails>` Layer 2 gate but have no corresponding behavioral test.

---

### Template Coverage

The skill provides four template files:

| Template | File ID | Status | Test Coverage |
|----------|---------|--------|---------------|
| `openapi-template.yaml` | F-07 | Active | Referenced in cd-generator Background block (G-001 through G-006). G-001 asserts the template is consumed to produce correct output. |
| `mapping-template.md` | F-08 | Active | G-001 asserts mapping document is written alongside contract. G-005 asserts mapping document contains "PROTOTYPE STATUS" section. |
| `AsyncAPI-template.yaml` | F-09 | Deferred (x-deferred: true) | No test coverage. Correctly excluded per Scope section: "AsyncAPI/CloudEvents generation deferred per DI-07, ASM-005, G-02." |
| `cloudevents-template.yaml` | F-10 | Deferred (x-deferred: true) | No test coverage. Correctly excluded per Scope section. |

**Assessment:** Active template coverage is appropriate. The two deferred templates (AsyncAPI, CloudEvents) are correctly excluded from scope with explicit rationale citing DI-07, ASM-005, and G-02. The Scope section's explicit callout of this exclusion is a positive practice that makes the coverage boundary visible to future reviewers.

The assertion in G-005 that the mapping document contains a "PROTOTYPE STATUS" section is a particularly valuable template-level assertion because it verifies mapping-template.md content structure, not just the file's existence.

---

### PROTOTYPE Label Coverage

PROTOTYPE label enforcement is the highest-priority safety gate in the /contract-design skill. The test suite covers it from three angles:

| Test | Scenario | Angle | Assertion |
|------|----------|-------|-----------|
| Generation includes label | G-001 | cd-generator happy path | `info.x-prototype: true` in assertions table |
| Label is invariant | G-005 | Dedicated invariant scenario | Label present AND `x-prototype: false` absent AND mapping "must be removed by human review only" |
| Validator detects absence | V-003 | cd-validator mandatory FAIL | Exact error message text, no-override property |
| Pipeline preserves label | E-001 | End-to-end | All 9 validator steps PASS (Step 7 implicitly passed) |

**Assessment:** PROTOTYPE label coverage is the strongest coverage category in the test suite. The three-angle approach (generation correctness, generation invariant, validator enforcement) provides defense-in-depth for this critical safety property. G-005 adds value beyond G-001 by explicitly verifying that the label cannot be overridden and that the mapping document communicates the human-review requirement.

The assertion that "the mapping document states that the PROTOTYPE label must be removed by human review only" in G-005 maps to P-020 (user authority) — PROTOTYPE removal is a human decision that cannot be delegated to an agent. This constitutional compliance assertion is correctly expressed as a behavioral test.

---

### Cross-Skill Integration Tests

#### /use-case to /contract-design Pipeline

The /contract-design skill consumes artifacts produced by the /use-case skill. The integration boundary is filesystem-mediated (P-003 compliant): cd-generator reads a UC artifact file that uc-slicer produced.

| Integration Aspect | Tested | Evidence |
|-------------------|--------|---------|
| File format compatibility | Implicit | G-001 fixture FX-01 uses the UC artifact format (realization_level, interactions block) consistent with /use-case output structure |
| INTERACTION_DEFINED realization_level required | G-002 | STORY_DEFINED input rejected with actionable guidance pointing to /use-case |
| Schema compatibility | Partial | Background block specifies `use-case-realization-v1.schema.json` accessibility; no scenario verifies schema validation pass explicitly |
| No direct agent invocation | E-001 | Background: "neither agent invokes the other directly"; G-001 Background does not include Task tool | COVERED via design constraint |

**cd-generator to cd-validator Pipeline (E-001):**

E-001 is the primary integration scenario. Its assertions are:
1. Contract file written at specific path by cd-generator
2. Mapping document written alongside contract by cd-generator
3. cd-validator reads both files independently (filesystem-mediated, P-003 compliant)
4. Validation report written at expected path
5. All 9 validation steps produce PASS verdicts
6. Traceability coverage is 1/1 = 100%
7. cd-generator did NOT modify the source UC artifact (read-only consumption)
8. cd-validator did NOT modify the generated OpenAPI contract (read-only evaluation)

Assertions 7 and 8 (read-only consumption verification) are particularly important for the creator-critic separation pattern. The explicit "read-only consumption verified" and "read-only evaluation verified" assertions in E-001 make the creator-critic boundary a behavioral test requirement, not just a design principle.

**Gap in E-001:** The assertion "all 9 validation steps have PASS verdicts" is a high-level aggregate assertion. It does not verify each step's PASS verdict individually with evidence. If Steps 3, 4, 5, 6, 8, or 9 had a defect that caused a FAIL, E-001 would catch it — but the validation report format requires per-step evidence in the Per-Check Results table. E-001 does not assert that the per-step evidence table is present. This gap is captured in FIND-QA-002 (the broader validator step coverage gap).

---

### Security Test Assessment

#### OWASP Testing Guide Category Mapping

| OWASP Category | Test Focus | Coverage | Evidence |
|---------------|-----------|---------|---------|
| INPVAL (Input Validation) | Layer 2 gate: missing interactions, wrong realization_level | COVERED | G-002 (rejection with actionable message) |
| INPVAL (Input Validation) | cd-validator: invalid YAML, missing artifact | PARTIAL | V-001 (PASS path only), V-003 (FAIL for missing PROTOTYPE) |
| BUSLOGIC (Business Logic) | PROTOTYPE label as mandatory non-overridable gate | COVERED | G-005 (generator), V-003 (validator) |
| BUSLOGIC (Business Logic) | Creator-critic-separation (read-only consumers) | COVERED | E-001 (read-only assertions for both agents) |
| BUSLOGIC (Business Logic) | cd-validator Steps 3-6, 8-9 FAIL paths | NOT COVERED | No scenarios — FIND-QA-002 |
| AUTHZ (Authorization) | PROTOTYPE removal requires human decision (P-020) | COVERED | G-005 mapping document assertion |
| SESS (Session Management) | Filesystem-mediated cross-agent handoff (P-003) | COVERED | E-001 Background and assertions |
| API (API Testing) | OpenAPI 3.1 structural correctness | COVERED | V-001 (structural validity step) |
| IDENT (Identity Management) | No identity management in this skill | N/A | Skill has no authentication or user identity concepts |
| CRYPST (Cryptography) | No cryptographic operations in this skill | N/A | Skill produces documentation artifacts only |

#### Guardrail Effectiveness

**cd-generator Layer 2 input gate:**

The Layer 2 guardrail table in `cd-generator.md` lists the following checks:

| Check | Test Coverage | Assessment |
|-------|--------------|------------|
| No interactions block → REJECT | G-002 | Strong coverage |
| Interactions present but all actor_role = provider → REJECT | None | GAP — this sub-condition is not tested |
| Output path directory does not exist → REJECT | None | GAP — edge case, low risk |
| Field name inconsistency (`detail_level` vs `realization_level`) | FIND-QA-003 | The guardrail references `$.detail_level < ESSENTIAL_OUTLINE` but the schema field is `realization_level`. The rejection condition is semantically correct for use case filtering but uses the wrong field name. G-002 exercises the interactions-absent path but does not verify which field is used to evaluate realization level. |

**cd-validator Layer 2 input gate:**

The Layer 2 guardrail table in `cd-validator.md` lists the following checks:

| Check | Test Coverage | Assessment |
|-------|--------------|------------|
| Contract file does not exist → REJECT | None | GAP |
| Contract YAML unparseable → REJECT | None | GAP |
| Source UC artifact does not exist → REJECT | None | GAP |
| `$.interactions` absent in UC artifact → REJECT | None | GAP — four of four validator Layer 2 reject conditions have no test scenario |

**Assessment:** The generator Layer 2 gate is tested for the primary rejection case (G-002). The validator Layer 2 gate is entirely untested at the reject-path level — all four pre-processing rejection conditions lack dedicated scenarios. This is a MEDIUM gap because the validator's primary security boundary (rejecting invalid inputs before executing the 9-step protocol) has no behavioral test coverage.

#### Constitutional Compliance in Test Scenarios

| Principle | Behavioral Test Mapping | Coverage |
|-----------|------------------------|---------|
| P-003 (no recursive subagents) | E-001 Background: "neither agent invokes the other directly"; E-001 no Task tool in agent Background | COVERED |
| P-020 (user authority) | G-005: PROTOTYPE label requires human review; V-003: mandatory FAIL with no override permitted | COVERED |
| P-022 (no deception) | G-002: error message specifies exact actionable guidance (not a vague error); V-003: exact FAIL message text verified | COVERED |

**Assessment:** All three constitutional principles have behavioral test expressions in the scenario suite. This is a positive outcome — constitutional compliance is expressed as observable behavior, not just as a governance declaration.

---

### H-20 Compliance

#### Minimum Scenario Count

The eng-architect specification requires a minimum of 9 BDD scenarios for the /contract-design skill. The eng-lead review (step-11-eng-lead-review.md) derives this minimum as:
- 4 (cd-generator scenarios: 1 happy + 1 rejection + 1 HTTP method + 1 error mapping)
- + 1 (PROTOTYPE invariant: G-005)
- + 3 (cd-validator: 1 structural + 1 traceability + 1 PROTOTYPE label)
- + 1 (pipeline: E-001)
- = 9 minimum

**Actual count:** 10 scenarios (G-001 through G-006, V-001 through V-003, E-001). The +1 is G-003 (HTTP method high-confidence path, separate from G-004 which is the low-confidence path).

**H-20 minimum: PASS.** 10 >= 9.

#### BDD Format Verification

| H-20 Requirement | Assessment |
|-----------------|------------|
| Feature / Background / Scenario / Given / When / Then / And structure | Present in all 10 scenarios |
| Concrete inputs (data tables or specific values) | Present — all scenarios use markdown data tables |
| Verifiable assertions (observable artifact state) | Present — assertions reference file paths, field values, message text |
| Scenario IDs in titles | Present — G-NNN, V-NNN, E-NNN prefix in all scenario titles |
| Coverage Matrix present | Present — maps all 10 scenarios to rules or steps |
| Negative cases (at least 3) | Present — G-002 (rejection), V-002 (traceability FAIL), V-003 (mandatory FAIL) |
| Fixture definitions | Present — FX-01 through FX-06 defined in Overview |

**H-20 BDD format: PASS.** All format requirements are satisfied.

#### H-21 (Line Coverage) Applicability

The BEHAVIOR_TESTS.md Scope section correctly states that H-21 (90% line coverage via coverage.py) is Not Applicable: "/contract-design is a pure markdown/YAML skill; H-20 BDD applies, H-21 line coverage is N/A." This is consistent with the architecture specification and the eng-lead review, which both confirm that there is no Python implementation to instrument. The exclusion is correctly justified.

---

### Test Quality Metrics

#### Assertion Concreteness Score

Assertions are scored as concrete (references specific field values, paths, or message text), semi-concrete (references field presence without value), or abstract (references vague outcomes).

| Scenario | Assertion Concreteness | Notes |
|----------|----------------------|-------|
| G-001 | Concrete | 5-field info table, operationId name, x-source-interaction value, entry count |
| G-002 | Concrete | Error message text and guidance text content verified |
| G-003 | Concrete | HTTP method and x-method-inference value verified |
| G-004 | Concrete | HTTP method, x-method-inference value, "human review annotation is present" (semi) |
| G-005 | Concrete | Field presence AND absence AND mapping content verified |
| G-006 | Concrete | HTTP status code, description text, schema $ref, extension annotation value |
| V-001 | Concrete | Field names and values in Given table; PASS verdict and evidence |
| V-002 | Concrete | Coverage formula "1/2 = 50%", specific interaction ID "INT-06" in gap list |
| V-003 | Concrete | Verbatim FAIL message text; no-override property explicitly asserted |
| E-001 | Concrete + aggregate | Path-level assertions concrete; "all 9 validation steps have PASS verdicts" is aggregate |

**Assessment:** 9 of 10 scenarios have fully concrete assertions. E-001 is 80% concrete with the aggregate step-verdict assertion being the semi-concrete component. This is the highest assertion quality possible for an integration scenario where per-step assertion would require duplicating the validation report format verbatim.

#### Fixture Completeness

| Fixture | Used By | Completeness |
|---------|---------|-------------|
| FX-01 | G-001, G-003, G-005, G-006, E-001 | Complete — 9-field UC artifact with all required blocks |
| FX-02 | G-002 | Complete — minimal UC at STORY_DEFINED (no interactions) |
| FX-03 | G-004 | Complete — ambiguous request_description for HM inference |
| FX-04 | V-001, E-001 | Complete — valid contract with x-prototype: true |
| FX-05 | V-002 | Complete — valid contract missing one consumer interaction mapping |
| FX-06 | V-003 | Complete — valid contract with x-prototype absent |

All 6 fixtures are used by at least one scenario. No orphan fixtures. FX-01 is the most reused fixture (5 scenarios) and its field completeness (including supporting_actors, EXT-2a extension) reflects the most complete UC artifact definition in the test suite.

#### Traceability to Architecture Specification

The BEHAVIOR_TESTS.md header references the architecture document:
- "Standard: H-20 (BDD test-first)" — correct
- "Schema: docs/schemas/use-case-realization-v1.schema.json (v1.0.0)" — correct
- "Rules: skills/contract-design/rules/uc-to-contract-rules.md (RULE-RI through RULE-TR)" — correct

The Coverage Matrix in BEHAVIOR_TESTS.md maps all 10 scenarios to specific rules and standards. Cross-referencing the matrix against the 24 rules confirms that the matrix is accurate (no false claims of coverage, no omissions of claimed coverage). The matrix does not claim coverage for untested rules — gaps are visible by absence, not by false positive assertions.

---

## Findings

### FIND-QA-001: Rules File Navigation Table States "22 Rules" but 24 Rules Are Present

**Severity:** MEDIUM
**OWASP Category:** Documentation
**File:** `skills/contract-design/rules/uc-to-contract-rules.md`
**Section:** Navigation table header (exact text: "all 22 rules")

**Evidence:**
- Navigation table header in `uc-to-contract-rules.md` states "all 22 rules" in its description text
- Actual count of distinct RULE-* entries in the file: 24 (confirmed by grep of `^\*\*RULE-`)
- Rule category breakdown: RULE-RI (3) + RULE-OM (4) + RULE-HM (5) + RULE-SD (4) + RULE-ER (3) + RULE-AR (3) + RULE-TR (2) = 24
- The Rule Summary Index table contains 25 rows: 24 named parent rules + 1 aggregate RULE-ER-01a-f row
- The BEHAVIOR_TESTS.md Acceptance Verification Checklist does not reference the total rule count

**Impact:** A reviewer reading the navigation table would expect 22 rules and would not search for the 2 rules absent from their count. This creates a false sense of completeness in rule coverage assessments.

**Recommendation:** Update the navigation table text in `uc-to-contract-rules.md` to state "all 24 rules." Verify the Rule Summary Index aggregate row is clearly labeled as a sub-rule summary, not a 25th parent rule.

**Remediation Owner:** eng-backend (rules file author)

---

### FIND-QA-002: cd-validator Steps 3, 4, 5, 6, 8, 9 Have No Dedicated Test Scenarios

**Severity:** MEDIUM
**OWASP Category:** BUSLOGIC
**File:** `skills/contract-design/tests/BEHAVIOR_TESTS.md`
**Section:** Feature: cd-validator Agent

**Evidence:**
- Dedicated step scenarios: Step 1 (V-001), Step 2 (V-002), Step 7 (V-003)
- Steps 3, 4, 5, 6, 8, 9 are exercised only by E-001 via the aggregate assertion "all 9 validation steps have PASS verdicts"
- E-001 does not assert per-step verdicts with evidence — it asserts the overall aggregate only
- cd-validator methodology defines distinct algorithms for each step:
  - Step 3: HTTP method semantics verification (operationId, summary presence)
  - Step 4: Schema completeness (requestBody, $ref resolution)
  - Step 5: Error response mapping (extension to error response coverage)
  - Step 6: Traceability annotations (x-source-interaction, x-source-step, x-source-flow)
  - Step 8: Internal operations documentation (x-internal-operations entries)
  - Step 9: Supporting actor resolution (actor referenced in contract)
- A defect in any of these steps would cause E-001 to fail, but the failure evidence would be the validation report content, not an assertion mismatch

**Impact:** Steps 3, 4, 5, 6, 8, and 9 are regression-tested only implicitly. If a future revision of cd-validator modifies Step 4 behavior, there is no dedicated scenario to catch the regression.

**Specifically missing:**
- Step 3 FAIL path: operation with HTTP method mismatch (e.g., request_description implies GET but operation is POST)
- Step 5 FAIL path: failure extension present but no corresponding error response
- Step 6 FAIL path: operation missing x-source-interaction annotation
- Step 8 FAIL path: provider interaction with no x-internal-operations entry (documentation gap)

**Recommendation:** Add at minimum 2 dedicated cd-validator scenarios:
1. V-004: Step 3 FAIL — HTTP method mismatch (mismatched method relative to request_description semantics)
2. V-005: Step 6 FAIL — Missing traceability annotation (operation without x-source-interaction)

Steps 4, 5, 8, and 9 may be covered by expanding E-001's assertions or accepting the implicit coverage as sufficient for LOW-criticality regression.

**Remediation Owner:** eng-backend

---

### FIND-QA-003: Layer 2 Guardrail Uses `detail_level` Field Name Instead of `realization_level`

**Severity:** MEDIUM
**OWASP Category:** INPVAL
**File:** `skills/contract-design/agents/cd-generator.md`
**Section:** `<guardrails>` Layer 2 Agent Guardrail Checks table

**Evidence (from adversary score carryforward FIND-005):**
- `cd-generator.md` Layer 2 guardrail check table contains the condition: `$.detail_level < ESSENTIAL_OUTLINE`
- The UC artifact schema (`docs/schemas/use-case-realization-v1.schema.json`) defines the field as `realization_level` with enum values including `INTERACTION_DEFINED`, `STORY_DEFINED`, `GOAL_DEFINED`
- The architecture specification (step-11-contract-design-architecture.md) specifies the Layer 2 condition as `$.realization_level != "INTERACTION_DEFINED"`
- `detail_level` is not a defined field in the UC artifact schema
- No test scenario verifies which field the Layer 2 gate actually evaluates — G-002 uses `realization_level: STORY_DEFINED` in the Given table (the correct field name), but the agent's internal evaluation may use `detail_level` if the guardrail description is followed literally

**Impact:** If an LLM following the `cd-generator.md` guardrail description reads `$.detail_level` literally, it may fail to reject UC artifacts at the wrong realization_level. This is a behavioral correctness defect in the guardrail specification. The test suite partially masks this because G-002's Given table uses the correct field name, but the agent's behavior for this specific check is ambiguous.

**Recommendation:**
1. In `cd-generator.md`, correct the Layer 2 guardrail check condition from `$.detail_level < ESSENTIAL_OUTLINE` to `$.realization_level != "INTERACTION_DEFINED"`
2. Update G-002 to explicitly assert that the agent reads `realization_level` (not `detail_level`) by adding a Then assertion: "And the rejection specifies the artifact's realization_level as the reason"

**Remediation Owner:** eng-backend (agent definition) + eng-qa (test update)

---

### FIND-QA-004: RULE-OM-03 (system_role = initiator Mapping) Has No Dedicated Test Scenario

**Severity:** MEDIUM
**OWASP Category:** INPVAL
**File:** `skills/contract-design/tests/BEHAVIOR_TESTS.md`
**Section:** Coverage Matrix

**Evidence:**
- `skills/contract-design/rules/uc-to-contract-rules.md` defines RULE-OM-03 for interactions where `actor_role = initiator` (system-to-system calls where the system under design is the caller)
- The Coverage Matrix in BEHAVIOR_TESTS.md maps RULE-OM-01, RULE-OM-02 to G-001; RULE-OM-04 to G-001 (implicitly)
- No scenario has `actor_role = initiator` in any interaction fixture
- All fixtures (FX-01 through FX-06) use either `consumer` or `provider` actor roles
- RULE-OM-03 describes a distinct output: server-to-server API documentation or an x-outbound-call entry, rather than an externally-exposed operation path

**Impact:** RULE-OM-03 covers a materially distinct pattern (system-initiated calls vs. consumer-driven calls). The inference algorithm for this pattern diverges from RULE-OM-01 at Step 2 (actor_role classification), and the output format differs (no path in `paths`, entry in a different section). Without a scenario exercising this path, RULE-OM-03 behavior is unverified.

**Recommendation:** Add G-007 scenario: UC artifact with actor_role = initiator interaction → agent produces x-outbound-call documentation (or equivalent per architecture specification) rather than a path+operation entry. This verifies the classification branch at RULE-OM-03.

**Remediation Owner:** eng-backend

---

### FIND-QA-005: RULE-ER-02 (Success Extension → 2xx Response Variant) Has No Dedicated Scenario

**Severity:** LOW
**OWASP Category:** INPVAL
**File:** `skills/contract-design/tests/BEHAVIOR_TESTS.md`
**Section:** Coverage Matrix, Feature: cd-generator Agent

**Evidence:**
- `uc-to-contract-rules.md` defines RULE-ER-02 for extensions with `outcome = success` — these map to 2xx response variants on the existing success operation, not to a 4xx error response
- G-006 exercises RULE-ER-01d (failure extension → 409 Conflict)
- RULE-ER-02 is distinct: success extensions produce an additional 200 or 201 variant, not an error response
- No fixture includes an extension with `outcome = success`

**Impact:** RULE-ER-02 behavior is unverified. The risk is LOW because success extensions are less commonly used in use case specifications and the algorithm for success extension mapping is simpler than failure extension mapping (no status code classification required). However, the RULE-ER-02 output (2xx variant) is structurally different enough from RULE-ER-01 (4xx response) to warrant dedicated coverage.

**Recommendation:** Add a Given clause to G-006 or create G-008: add a success extension to FX-01 (EXT-1a with `outcome = success`) and assert the generated operation carries a 200 response variant alongside the 201 primary response.

**Remediation Owner:** eng-backend

---

### FIND-QA-006: Slug Sanitization Not Present in Agent output_filtering Guardrail Lists

**Severity:** LOW
**OWASP Category:** INPVAL
**File:** `skills/contract-design/agents/cd-generator.governance.yaml`, `skills/contract-design/agents/cd-validator.governance.yaml`
**Section:** `guardrails.output_filtering`

**Evidence:**
- The output path for generated contracts uses a slug derived from the UC title: `UC-LIB-001-borrow-a-book.openapi.yaml`
- The slug derivation rule (lowercase, hyphen-separated) can produce unexpected path characters if the UC title contains special characters (e.g., slashes, colons, parentheses)
- `cd-generator.governance.yaml` output_filtering lists: `no_secrets_in_output`, `no_executable_code_in_contract`, `prototype_label_required_in_every_contract`, `contract_yaml_must_be_valid_openapi_3_1`
- `cd-validator.governance.yaml` output_filtering lists: `no_secrets_in_output`, `no_executable_code_in_output`, `validation_results_must_include_pass_fail_per_check`, `traceability_gaps_must_list_specific_interaction_ids`, `coverage_percentage_must_show_numerator_and_denominator`
- Neither governance file includes `sanitize_output_filename_slug` or equivalent filtering rule
- No test scenario uses a UC title with special characters to verify slug sanitization

**Impact:** A UC title like "Borrow a Book (Return)" could generate an output path with parentheses in the filename. This is a LOW risk because the file system will reject the path rather than creating a security vulnerability, but the error message would be unhelpful and the contract would not be written.

**Recommendation:**
1. Add `sanitize_slug_for_filesystem_safety` to `cd-generator.governance.yaml` output_filtering
2. Add a G-009 scenario (LOW priority): UC with special characters in title produces sanitized filename slug

**Remediation Owner:** eng-backend

---

## Coverage Gap Matrix

This matrix summarizes the coverage status of all 24 RULE-* transformation rules and all 9 cd-validator steps, with severity and finding reference.

### Transformation Rule Coverage

| Rule | Description | Tested By | Status | Finding |
|------|------------|-----------|--------|---------|
| RULE-RI-01 | Resource noun-pluralized path from interaction intent | G-001 | COVERED | — |
| RULE-RI-02 | Sub-resource nesting | None | GAP | — |
| RULE-RI-03 | Path parameter extraction | None | GAP | — |
| RULE-OM-01 | Consumer interaction → external operation | G-001 | COVERED | — |
| RULE-OM-02 | Operation metadata (operationId, summary) | G-001 | COVERED | — |
| RULE-OM-03 | Initiator interaction → server-to-server documentation | None | GAP | FIND-QA-004 |
| RULE-OM-04 | Provider interaction → x-internal-operations | G-001 (count assertion) | PARTIAL | — |
| RULE-HM-01 | Retrieve/query semantics → GET | None | GAP | — |
| RULE-HM-02 | Create/submit semantics → POST | G-001, G-003 | COVERED | — |
| RULE-HM-03 | Replace/update semantics → PUT | None | GAP | — |
| RULE-HM-04 | Partial update semantics → PATCH | None | GAP | — |
| RULE-HM-05 | Ambiguous verb → POST + x-method-inference: low | G-004 | COVERED | — |
| RULE-SD-01 | Request body schema from preconditions | G-001 (presence) | PARTIAL | — |
| RULE-SD-02 | Response schema from postconditions | G-001 (presence) | PARTIAL | — |
| RULE-SD-03 | Enum field generation | None | GAP | — |
| RULE-SD-04 | Optional vs required field classification | None | GAP | — |
| RULE-ER-01 (a-f) | Failure extension → 4xx (sub-rule classification) | G-006 (01d only) | PARTIAL | — |
| RULE-ER-02 | Success extension → 2xx response variant | None | GAP | FIND-QA-005 |
| RULE-ER-03 | Extension annotation (x-source-extension) | G-006 | COVERED | — |
| RULE-AR-01 | x-source-interaction annotation | G-001 | COVERED | — |
| RULE-AR-02 | x-source-step annotation | G-001 | COVERED | — |
| RULE-AR-03 | x-source-flow annotation | G-001 | COVERED | — |
| RULE-TR-01 | Mapping document written alongside contract | G-001, G-005 | COVERED | — |
| RULE-TR-02 | x-prototype: true mandatory in info section | G-001, G-005, V-003, E-001 | COVERED | — |

**Legend:** COVERED = dedicated scenario with concrete assertions. PARTIAL = covered in a scenario but not with full field-level or sub-rule assertions. GAP = no dedicated scenario.

### cd-validator Step Coverage

| Step | Name | Tested By | PASS Path | FAIL Path | Finding |
|------|------|-----------|-----------|-----------|---------|
| Step 1 | Structural Validity | V-001 | COVERED | NOT COVERED | — |
| Step 2 | Path Completeness (Traceability) | V-002 | Implicit (E-001) | COVERED | — |
| Step 3 | Operation Correctness | E-001 (implicit) | Implicit | NOT COVERED | FIND-QA-002 |
| Step 4 | Schema Completeness | E-001 (implicit) | Implicit | NOT COVERED | FIND-QA-002 |
| Step 5 | Error Response Mapping | E-001 (implicit) | Implicit | NOT COVERED | FIND-QA-002 |
| Step 6 | Traceability Annotations | E-001 (implicit) | Implicit | NOT COVERED | FIND-QA-002 |
| Step 7 | PROTOTYPE Label Verification | V-003 | Implicit (E-001) | COVERED (mandatory FAIL) | — |
| Step 8 | Internal Operations Documentation | E-001 (implicit) | Implicit | NOT COVERED | FIND-QA-002 |
| Step 9 | Supporting Actor Resolution | E-001 (implicit) | Implicit | NOT COVERED | FIND-QA-002 |

---

## Recommendations

### Priority 1 (Address Before eng-reviewer Handoff)

| Rec | Action | Finding | Effort |
|-----|--------|---------|--------|
| R-01 | Correct `cd-generator.md` Layer 2 guardrail field name from `detail_level` to `realization_level` | FIND-QA-003 | Low — 1 line change in guardrail table |
| R-02 | Update `uc-to-contract-rules.md` navigation table header to state "24 rules" instead of "22 rules" | FIND-QA-001 | Low — 1 line documentation fix |

### Priority 2 (Recommended for BEHAVIOR_TESTS.md v1.1.0)

| Rec | Action | Finding | Effort |
|-----|--------|---------|--------|
| R-03 | Add V-004 scenario: cd-validator Step 3 FAIL — HTTP method mismatch produces FAIL verdict with operation path cited | FIND-QA-002 | Medium — new scenario with fixture FX-07 |
| R-04 | Add V-005 scenario: cd-validator Step 6 FAIL — operation missing x-source-interaction annotation produces FAIL | FIND-QA-002 | Medium — new scenario with fixture FX-08 |
| R-05 | Add G-007 scenario: UC with actor_role = initiator interaction produces x-outbound-call documentation, not a path entry | FIND-QA-004 | Medium — new fixture and scenario |

### Priority 3 (Future Enhancement)

| Rec | Action | Finding | Effort |
|-----|--------|---------|--------|
| R-06 | Add RULE-HM-01 scenario (GET inference) and RULE-HM-03 scenario (PUT inference) | — | Medium — 2 scenarios with new fixtures |
| R-07 | Add RULE-ER-02 scenario (success extension → 2xx response variant) | FIND-QA-005 | Low — extend FX-01 with success extension |
| R-08 | Add slug sanitization guardrail to cd-generator.governance.yaml output_filtering | FIND-QA-006 | Low — 1 line in governance YAML |
| R-09 | Strengthen E-001 to assert per-step PASS verdicts (at least that the Per-Check Results table is present in the validation report) | FIND-QA-002 | Low — additional Then assertion |

---

## L2: Strategic Implications

### Test Strategy Effectiveness

The BEHAVIOR_TESTS.md test strategy for /contract-design demonstrates deliberate prioritization of safety-critical behaviors over exhaustive rule coverage. The three-angle coverage of PROTOTYPE label enforcement (G-001 generation, G-005 invariant, V-003 mandatory FAIL) and the creator-critic separation assertion in E-001 show that the test designer understood the architectural priorities established in the architecture specification.

The concentration of gaps in RULE-HM (HTTP method inference, 3/5 rules untested) and RULE-RI (resource identification variants, 2/3 rules untested) is understandable for a v1.0.0 specification — these rules exercise edge cases of the inference algorithm rather than the primary transformation correctness. However, the inference algorithm is where the most implementation variability exists (an LLM executing the algorithm may produce different results for edge cases), making these gaps the highest-regression-risk items for future revisions.

### Coverage Gap Risk Implications

| Gap Category | Risk Assessment | Consequence if Unaddressed |
|-------------|----------------|---------------------------|
| cd-validator Steps 3-6, 8-9 FAIL paths (FIND-QA-002) | MEDIUM | A defect in any of these 6 steps would be caught only by E-001's aggregate assertion; the defect would manifest as a validation report FAIL that is not traced to the specific step that failed |
| RULE-HM-01, HM-03, HM-04 (GET, PUT, PATCH inference) | MEDIUM | API consumers expect correct HTTP methods; incorrect method inference is a functional correctness defect visible only at integration time |
| Layer 2 guardrail field name (FIND-QA-003) | MEDIUM | If the agent follows the guardrail description literally, it may evaluate the wrong field for realization_level gating, accepting UC artifacts that should be rejected |
| RULE-OM-03 (initiator interaction) | MEDIUM | System-initiated interactions are a distinct pattern; without coverage, the classifier may route them incorrectly through the consumer path |

### Regression Suite Maintenance Considerations

The 10-scenario structure with three Features and a Pipeline integration test provides a solid regression foundation. The Coverage Matrix in BEHAVIOR_TESTS.md is well-maintained and provides the traceability needed to identify which scenarios to re-run when a specific rule is modified.

As the /contract-design skill evolves, the highest-maintenance scenarios will be G-001 (covers 9 rules and serves as the primary happy-path regression) and E-001 (integration scenario). Any change to the UC artifact schema or the 9-step algorithm will require G-001 and E-001 to be re-verified first.

The deferred AsyncAPI and CloudEvents templates (F-09, F-10) will require new BDD scenarios when DI-07 is resolved. The test suite's Scope section explicitly calls out this deferral with accurate citations (DI-07, ASM-005, G-02), making future test expansion traceable.

### Fuzzing Campaign Applicability

The /contract-design skill is a pure documentation artifact producer with no server-side code, no network endpoints, and no authentication surface. Standard fuzzing (AFL++, libFuzzer) and API fuzzing (RESTler, Schemathesis) are not applicable.

Property-based testing with Hypothesis would be applicable if there were a Python implementation of the UC-to-contract algorithm. Since the skill is implemented as LLM agent prompting, the equivalent of property-based testing is scenario-based testing with boundary-condition fixtures. The following property invariants are already expressed as behavioral tests:
- P1: Every generated contract contains x-prototype: true (G-005)
- P2: Every consumer interaction maps to exactly one operation (V-002 tests the violation)
- P3: cd-validator never modifies the contract (E-001 read-only assertion)

A fourth property worth adding as a future scenario:
- P4: A contract generated from a UC with N consumer interactions has exactly N operations in paths (property-based: N can vary from 1 to M)

### SSDF Alignment

| SSDF Practice | Test Evidence |
|---------------|---------------|
| PW.8 (Test executable code to identify vulnerabilities) | 10 BDD scenarios test the agent behavioral contract as specified; all Layer 2 input gates are tested for the primary rejection case |
| PW.7 (Review human-readable code for vulnerabilities) | FIND-QA-003 (field name error in guardrail description) identified through cross-referencing agent definition against schema; FIND-QA-001 (rule count documentation error) identified through empirical rule counting |

---

## S-010 Self-Review

| Check | Result | Evidence |
|-------|--------|---------|
| All 24 transformation rules are mapped | PASS | Transformation Rule Coverage section maps all 24 rules individually |
| All 9 cd-validator steps are mapped | PASS | Agent Methodology Coverage section maps all 9 steps |
| All 10 scenarios are evaluated | PASS | Test Strategy Assessment and Coverage Gap Matrix reference all 10 scenarios |
| Each finding has OWASP category, file, section, evidence | PASS | All 6 findings (FIND-QA-001 through FIND-QA-006) include category, file, section, evidence, impact, recommendation |
| PROTOTYPE label coverage assessed from multiple angles | PASS | PROTOTYPE Label Coverage section; G-001, G-005, V-003, E-001 all verified |
| H-20 compliance verified | PASS | H-20 Compliance section: 10 >= 9 minimum; BDD format verified against all requirements |
| Security test assessment maps to OWASP categories | PASS | Security Test Assessment section maps test coverage to INPVAL, BUSLOGIC, AUTHZ, SESS, API |
| Constitutional compliance (P-003, P-020, P-022) assessed | PASS | Constitutional Compliance in Test Scenarios table in Security Test Assessment |
| Recommendations are prioritized and actionable | PASS | Recommendations section has 3 priority tiers with effort estimates |
| L2 Strategic Implications present | PASS | L2 section covers strategy effectiveness, gap risk, regression, fuzzing applicability, SSDF |
| No deception about coverage gaps | PASS | All gaps stated explicitly with rule IDs; no false claims of coverage in matrix |
| Confidence indicator present | PASS | Confidence: 0.87 — high confidence on gap identification (all rules individually verified), moderate confidence on generator step 8 field-level assertions (not directly inspected) |

**Confidence:** 0.87 (high on structural and rule-level coverage analysis; moderate on agent-internal algorithm step sequencing that cannot be directly observed from the markdown agent definition alone).

**Known limitations:** The assessment of cd-generator Steps 3-9 is based on rule-to-scenario mapping, not on execution observation. The agent's algorithm implementation fidelity can only be assessed through execution, which is out of scope for a markdown/YAML skill (H-21 N/A). FIND-QA-003 (field name error) was identified through cross-reference, not through test execution — the actual runtime behavior may or may not be affected depending on how the LLM interprets the guardrail description.
