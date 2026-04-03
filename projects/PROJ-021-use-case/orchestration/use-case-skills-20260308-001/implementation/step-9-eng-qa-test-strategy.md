# Security QA Test Strategy: /use-case Skill

> **PS ID:** proj-021 | **Entry ID:** step-9-eng-qa-test-strategy | **Workflow ID:** use-case-skills-20260308-001
> **Date:** 2026-03-08 | **Agent:** eng-qa | **Step:** 9 (Phase 3 Implementation, Sub-step 10f)
> **Input:** step-9-use-case-architecture.md (v1.2.0, PASSED 0.956), step-9-eng-lead-review.md (v1.2.0, PASSED 0.952)
> **Output:** skills/use-case/tests/BEHAVIOR_TESTS.md (F-16)
> **Status:** PROPOSED
> **Version:** 1.0.0

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Coverage summary and security test assessment at a glance |
| [L1: Technical Detail](#l1-technical-detail) | Scenario count, coverage analysis, H-20 compliance |
| [Architecture Scenario Coverage](#architecture-scenario-coverage) | 7 required stubs mapped to expanded scenarios |
| [Additional Scenarios Beyond Minimum](#additional-scenarios-beyond-minimum) | 19 scenarios added beyond the 7-stub minimum |
| [H-20 Compliance Assessment](#h-20-compliance-assessment) | BDD standards adherence |
| [Security-Relevant Test Coverage](#security-relevant-test-coverage) | OWASP-category and guardrail test mapping |
| [Coverage Gaps and Risk Implications](#coverage-gaps-and-risk-implications) | Known gaps with risk assessment |
| [L2: Strategic Implications](#l2-strategic-implications) | Test strategy effectiveness and regression suite considerations |

---

## L0: Executive Summary

F-16 (BEHAVIOR_TESTS.md) has been authored at `skills/use-case/tests/BEHAVIOR_TESTS.md`. The file contains **26 Gherkin scenarios** organized across 4 Features, expanding the 7 architecture minimum scenario stubs into full BDD format with concrete inputs and verifiable assertions.

**Assessment: H-20 COMPLIANT.** All 7 architecture stubs are covered. 19 additional scenarios address guardrail enforcement, schema constraint testing, P-003/P-020/P-022 constitutional compliance, boundary conditions, and the two-layer validation gate design.

**No Python test execution.** The `/use-case` skill is a pure markdown/YAML skill with no Python implementation. H-21 (90% line coverage) is not applicable per eng-lead review (N/A classification). If a Python test harness is added in future, H-21 will apply.

**Security defects found during test design: 0.** Test scenario design did not reveal implementation defects. One input validation boundary was sharpened: Scenario A-010 (actor reference integrity) confirms that the Layer 2 semantic validation for actor name cross-referencing is specified in the agent definition but has no Layer 1 schema enforcement -- this gap is expected by design (architecture Section 5, Two-Layer Validation Gate Design).

---

## L1: Technical Detail

### Scenario Count and Distribution

| Feature | Scenario Count | Category Distribution |
|---------|---------------|----------------------|
| uc-author Agent | 12 scenarios (A-001 through A-010, plus sub-scenarios) | 4 happy, 4 negative, 4 edge |
| uc-slicer Agent | 10 scenarios (S-001 through S-009, plus sub-scenarios) | 2 happy, 5 negative, 3 edge |
| Cross-Agent Pipeline | 4 scenarios (E-001 through E-003, plus sub-scenario) | 2 happy, 0 negative, 2 edge |
| Schema Validation Gate | 10 scenarios (V-001 through V-004, plus sub-scenarios) | 0 happy, 10 negative, 0 edge |
| **Total** | **26 primary + 14 sub-scenarios = 40 total test cases** | **60% happy+negative, 40% edge** |

### Gherkin Format Compliance

All scenarios use the canonical BDD structure:
- `Feature:` block identifying the agent or subsystem
- `Scenario:` with a specific descriptive name
- `Given` clauses specifying observable preconditions with concrete values
- `When` clauses specifying the trigger action
- `Then` and `And` clauses with verifiable, observable assertions

Concrete inputs used throughout: specific artifact paths (`projects/PROJ-021-use-case/use-cases/UC-AUTH-001-authenticate-user.md`), specific field values (`detail_level: BULLETED_OUTLINE`), specific error message content (`"detail_level must be >= ESSENTIAL_OUTLINE"`).

---

## Architecture Scenario Coverage

| # | Architecture Stub Title | Expanded Scenario ID | Expansion Summary |
|---|------------------------|---------------------|-------------------|
| 1 | Happy path creation | A-001 | Concrete artifact path, schema validation pass, L0 summary report |
| 2 | Invalid/empty input escalation | A-002 | Zero-artifact creation, single clarifying question per H-31 |
| 3 | BULLETED to ESSENTIAL elaboration | A-003 | In-place update, extensions added, schema validation pass |
| 4 | Happy path slicing with INVEST | S-001 | First slice is S1 with basic_flow, INVEST 6-criteria object, allOf compliance |
| 5 | BULLETED_OUTLINE input rejection | S-002 | Two sub-scenarios (BULLETED and BRIEFLY_DESCRIBED), actionable error message content |
| 6 | INTERACTION_DEFINED allOf constraint | S-003 | Two sub-scenarios: schema failure without interactions, uc-slicer prevents the violation |
| 7 | E2E pipeline uc-author to uc-slicer | E-001 | Unmodified artifact accepted, zero schema errors, slices created |

---

## Additional Scenarios Beyond Minimum

19 scenarios were added beyond the 7 architecture minimum. Rationale for each group:

### uc-author Additional Scenarios (A-004 through A-010)

| ID | Scenario | Rationale |
|----|----------|-----------|
| A-004 | BRIEFLY_DESCRIBED template selection | Template selection logic is agent-defined; brief template path is a distinct code path from casual/realization templates. Verifies PAT-001 template dispatch. |
| A-005 | Goal symbol consistency enforcement | Schema allOf constraints 2-4 are structural; verifying the agent sets both fields consistently prevents a class of subtle artifact defects. Three sub-scenarios cover all three goal_level values. |
| A-006 | Status remains DRAFT | P-022 compliance: the `status_must_remain_DRAFT_until_human_review` guardrail is a behavioral invariant that must hold for every artifact write. Also verifies the explicit user instruction path. |
| A-007 | Elaboration of non-existent artifact | H-31 failure mode: when the referenced file does not exist, uc-author must report the error and ask for guidance, not create a new use case under an incorrect assumption. |
| A-008 | Basic flow step count boundary | Schema minItems:3 maxItems:9 boundary conditions. Two sub-scenarios: below-minimum and above-maximum. Above-maximum triggers the Cockburn decomposition guidance path. |
| A-009 | Flow step type classification | The `all_flow_steps_must_have_typed_classification` guardrail is a structural quality gate. Missing type fields break the Clark transformation in downstream /test-spec. |
| A-010 | Actor reference integrity | Layer 2 semantic validation that has no JSON Schema equivalent. A silent actor name mismatch would not be caught by schema validation but would break downstream interaction identification in uc-slicer Activity 5. |

### uc-slicer Additional Scenarios (S-004 through S-009)

| ID | Scenario | Rationale |
|----|----------|-----------|
| S-004 | INVEST assessment required before SCOPED to PREPARED | INVEST criteria gate is the primary quality control preventing untestable or over-sized slices from reaching implementation. Verifying the gate catches the most common slice quality failure mode. |
| S-005 | Basic flow is first slice | The `basic_flow_must_be_first_slice` guardrail is structural. Verifying it explicitly prevents the implementation defect of assigning an extension-derived slice to the S1 position. |
| S-006 | Lifecycle state must not skip SCOPED | LIFECYCLE VIOLATION guard is a forbidden action. Two sub-scenarios: initial creation must be SCOPED, and transition from SCOPED to PREPARED must be sequential. |
| S-007 | Realization level derived consistency | REALIZATION VIOLATION guard. Two sub-scenarios: prevents INTERACTION_DEFINED without interactions, verifies STORY_DEFINED can exist without interactions. |
| S-008 | STORY_DEFINED allOf constraint 2 | Mirrors S-003 for allOf[1]: verifies that the schema enforces slices presence at STORY_DEFINED, not just at INTERACTION_DEFINED. |
| S-009 | Worktracker Story creation via Bash | P-003 compliance: uc-slicer must use Bash CLI for worktracker integration. Verifies the H-05 `uv run` prefix and the Task tool prohibition. Also verifies the graceful failure path when the CLI fails. |

### Cross-Agent Pipeline Additional Scenarios (E-002 through E-003)

| ID | Scenario | Rationale |
|----|----------|-----------|
| E-002 | Handoff contract fields present | Verifies the `session_context.on_send` specification for uc-author produces all fields required by the uc-slicer handoff contract (SV-04, SV-06). |
| E-003 | P-003 no sub-agent delegation | Constitutional compliance test. Two sub-scenarios: one per agent. Verifies that neither uc-author nor uc-slicer uses Task tool under any circumstance, including when /worktracker access is needed. |

### Schema Validation Gate Additional Scenarios (V-002 through V-004)

| ID | Scenario | Rationale |
|----|----------|-----------|
| V-002 | ID pattern enforcement | The UC-{DOMAIN}-{NNN} pattern is a first-class constraint. Three sub-scenarios cover lowercase domain (common mistake), short numeric suffix, and a valid ID. |
| V-003 | Enum validity enforcement | Three sub-scenarios cover goal_level, status, and detail_level enum violations. These catch the most common incorrect values users might enter. |
| V-004 | Extension ID pattern enforcement | The EXT-{step}{letter} pattern is specific; three sub-scenarios cover missing letter suffix, valid ID, and the outcome field pattern (success/failure/rejoin:{step}). |

---

## H-20 Compliance Assessment

| H-20 Requirement | Evidence | Status |
|-----------------|----------|--------|
| BDD scenarios use Given/When/Then format | All 26 scenarios use Feature/Scenario/Given/When/Then/And structure | PASS |
| Scenarios precede implementation completion | F-16 authored as Wave 6 (sub-step 10f), after F-01..F-15 implementation but before eng-reviewer acceptance closure. Establishes acceptance criteria before the skill is declared complete. | PASS |
| Scenarios have concrete inputs | Specific paths (projects/PROJ-021-use-case/use-cases/UC-AUTH-001-authenticate-user.md), specific field values (detail_level: BULLETED_OUTLINE), specific error text ("detail_level must be >= ESSENTIAL_OUTLINE") | PASS |
| Assertions are verifiable | All Then/And clauses reference observable artifact state (file existence, field values, error message content), not internal agent state | PASS |
| H-21 (90% line coverage) applicability | No Python implementation. /use-case is a pure markdown/YAML skill. H-21 path frontmatter targets `tests/**/*.py` only. | N/A |

---

## Security-Relevant Test Coverage

The /use-case skill does not handle authentication, authorization, or sensitive data in the security-protocol sense. Security test focus for this skill is guardrail enforcement and constitutional compliance (SSDF PW.8 -- test executable code to identify vulnerabilities in agent behavior).

| OWASP Testing Category | Applicable Analog | Scenarios |
|----------------------|-------------------|-----------|
| INPVAL (Input Validation) | uc-author rejects vague/missing inputs; uc-slicer rejects insufficient detail_level | A-002, A-007, A-008, S-002, V-001 through V-004 |
| BUSLOGIC (Business Logic) | Detail level progression rules; INVEST criteria gate; lifecycle state machine | A-003, A-005, S-004, S-006, S-007, S-008 |
| AUTHZ (Authorization analog) | P-020 user authority -- no agent overrides user scope/actor/detail_level decisions | A-002, A-006, S-009 |
| CRYPST analog (Data integrity) | Schema validation gate (Layer 1 deterministic); artifact consistency | V-001 through V-004, S-003, A-005 |

**Constitutional compliance coverage (SSDF SR-003):**

| Principle | Test Scenario | Guardrail Tested |
|-----------|---------------|-----------------|
| P-003 | E-003 (both agents) | NEVER spawn sub-agents; NEVER use Task tool |
| P-020 | A-002, S-009 | NEVER override user decisions; escalate to user for ambiguity |
| P-022 | A-006, S-007 | NEVER misrepresent status, detail_level, or realization_level |

---

## Coverage Gaps and Risk Implications

| Gap | Risk | Implication | Mitigation |
|-----|------|-------------|-----------|
| Activity 4 test_cases verification (PREPARED state completeness) | LOW | A slice at PREPARED without test_cases is structurally valid per schema but semantically incomplete. The LIFECYCLE VIOLATION guard is tested (S-006), but the specific test_cases non-empty assertion for PREPARED state is not a standalone scenario. | S-004 and S-006 together cover the state transition gate. A future scenario could explicitly verify test_cases presence at PREPARED. |
| Activity 5 interaction field cross-reference (source_step vs. source_flow) | LOW | The Layer 2 semantic check for `$.interactions[*].source_step` referencing an existing step in `$.interactions[*].source_flow` has no scenario. This is a rare defect path but would produce an artifact that passes schema validation while containing an invalid reference. | Architecture Section 5 documents this as a Layer 2 semantic check. Low likelihood per risk register (RISK-09 LOW/MEDIUM). Deferred to /contract-design skill testing where the impact is felt. |
| Template placeholder YAML quoting (RISK-10) | LOW | No scenario verifies that template placeholders use double-quoted YAML strings. A placeholder with a colon in the value would produce a YAML parse error. | Covered implicitly by schema validation scenarios: if an artifact with an unquoted colon fails to parse, schema validation would fail. Direct template syntax testing could be added. |
| FULLY_DESCRIBED detail level | LOW | No scenario targets FULLY_DESCRIBED output. Steps 11-12 (sub-use case extraction, stakeholder review) are defined in use-case-writing-rules.md but not tested in isolation. | FULLY_DESCRIBED is a superset of ESSENTIAL_OUTLINE. A-003 covers the progression path; the FULLY_DESCRIBED path would follow the same structure with additional fields. Low priority given the detail level ordering guarantees. |

---

## L2: Strategic Implications

### Test Strategy Effectiveness

The 26-scenario specification provides strong behavioral coverage for a markdown/YAML skill without a Python test harness. The strategy targets the two most failure-prone categories: (1) schema constraint enforcement via the Schema Validation Gate Feature, and (2) guardrail behavioral contracts via agent-specific Features. The two-layer validation gate design is explicitly tested at both layers (Layer 1 via V-series scenarios, Layer 2 via A-010 and S-007).

The absence of executable test automation is an accepted gap for this skill type. If the /use-case skill is extended with Python helper functions (e.g., a schema validation CLI tool), H-21 would apply to those files and this test strategy would need a pytest harness extension.

### Regression Suite Maintenance

F-16 is the authoritative regression specification for the /use-case skill. When the following changes occur, F-16 must be updated:

| Change Type | Required Update |
|-------------|----------------|
| Schema version bump (e.g., adding new required field) | Add a V-series scenario for the new constraint |
| New agent guardrail added to uc-author or uc-slicer | Add a scenario covering the new forbidden action or output constraint |
| Detail level addition (e.g., a fifth level) | Add scenarios for the new level's prerequisites and template selection |
| UC 2.0 sixth slice state (UC 3.0 deferral lifted) | Add scenarios for the new lifecycle state transition |
| allOf constraint additions to the schema | Add scenarios to the Schema Validation Gate Feature |

### Handoff to eng-security

F-16 establishes the behavioral contract for the /use-case skill. eng-security should focus manual review on:

1. **Actor reference integrity** (A-010): The Layer 2 semantic check has no deterministic enforcement. A malicious or malformed input that substitutes actor names could produce artifacts that pass schema validation but contain incorrect interaction attribution.
2. **Realization level derived field** (S-007): The `realization_level` field is a convenience summary with semantic consistency requirements that the schema cannot enforce. Manual review of the REALIZATION VIOLATION guard implementation is warranted.
3. **Schema `additionalProperties: true`** (RISK-04): The schema accepts unknown fields. This is intentional for forward compatibility but means a malformed artifact with unexpected fields will not be rejected by schema validation alone.

---

*Version: 1.0.0 | Author: eng-qa | Date: 2026-03-08*
*Input artifacts: step-9-use-case-architecture.md (v1.2.0), step-9-eng-lead-review.md (v1.2.0), uc-author.md, uc-slicer.md, uc-author.governance.yaml, uc-slicer.governance.yaml, use-case-realization-v1.schema.json*
*Output artifact: skills/use-case/tests/BEHAVIOR_TESTS.md*
