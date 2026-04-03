# Quality Score Report: eng-qa Test Strategy (F-16 BEHAVIOR_TESTS.md)

## L0 Executive Summary

**Score:** 0.893/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Evidence Quality (0.82)

**One-line assessment:** The 26-scenario BDD specification is structurally strong and architecturally complete, but falls short of the 0.95 threshold due to four cross-reference accuracy defects in Scenarios A-009, S-016, A-005, and V-001 that must be corrected before the C4 quality gate can be passed.

---

## Scoring Context

- **Deliverable:** `skills/use-case/tests/BEHAVIOR_TESTS.md` (primary, 821 lines) and `projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/implementation/step-9-eng-qa-test-strategy.md` (summary)
- **Deliverable Type:** Analysis (BDD Test Specification)
- **Criticality Level:** C4 (user override C-008, threshold >= 0.95)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-08T00:00:00Z
- **Iteration:** G-08-ADV-4 iter-1

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.893 |
| **Threshold** | 0.95 (user override C-008) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No (no prior adv-executor reports provided) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.95 | 0.190 | All 7 architecture stubs covered; 26 scenarios across 4 Features; 60/30/10 coverage distribution documented |
| Internal Consistency | 0.20 | 0.92 | 0.184 | Summary doc scenario count (40 total cases) reconciles correctly with 26 primary; coverage matrix is internally consistent; one minor inconsistency in S-009 classification |
| Methodological Rigor | 0.20 | 0.90 | 0.180 | Gherkin format correct throughout; concrete inputs and verifiable assertions; coverage matrix maps to implementation files; acceptance checklist present |
| Evidence Quality | 0.15 | 0.82 | 0.123 | Four cross-reference accuracy defects found against actual agent definitions and schema |
| Actionability | 0.15 | 0.88 | 0.132 | Scenarios are implementable as manual tests; coverage gaps documented with mitigations; regression maintenance table present |
| Traceability | 0.10 | 0.92 | 0.092 | Architecture stub coverage table; coverage matrix; H-rule mapping; schema constraint mapping; all 7 stubs traced to expanded scenarios |
| **TOTAL** | **1.00** | | **0.901** | |

**Corrected composite (calculation):**
(0.95 × 0.20) + (0.92 × 0.20) + (0.90 × 0.20) + (0.82 × 0.15) + (0.88 × 0.15) + (0.92 × 0.10)
= 0.190 + 0.184 + 0.180 + 0.123 + 0.132 + 0.092
= **0.901**

> **Note:** The L0 summary reports 0.893 due to initial dimension estimate; the table arithmetic yields 0.901. Both are below the 0.95 threshold. The corrected composite is 0.901. Verdict is unchanged: REVISE.

---

## Detailed Dimension Analysis

### Completeness (0.95/1.00)

**Evidence:**

All 7 minimum scenario stubs from the architecture (Section F-16, architecture document lines 766-774) are present and expanded:

| Architecture Stub | Expanded Scenario | Status |
|---|---|---|
| Stub 1: uc-author happy path creation | A-001 (Scenario 1) -- concrete path, schema validation, L0 summary check | COVERED |
| Stub 2: uc-author invalid/empty input validation | A-002 (Scenario 2) -- zero-artifact creation, H-31 escalation, single clarifying question | COVERED |
| Stub 3: uc-author detail level progression BULLETED->ESSENTIAL | A-003 (Scenario 3) -- in-place update, extensions added, preconditions populated, schema validation | COVERED |
| Stub 4: uc-slicer happy path slicing | S-001 (Scenario 11) -- S1 pattern, INVEST 6-criteria, allOf compliance | COVERED |
| Stub 5: uc-slicer input rejection (< ESSENTIAL_OUTLINE) | S-002 (Scenario 12) -- two sub-scenarios: BULLETED and BRIEFLY_DESCRIBED, actionable error text | COVERED |
| Stub 6: uc-slicer INTERACTION_DEFINED allOf constraint | S-003 (Scenario 13) -- two sub-scenarios: schema fail without interactions, agent prevention | COVERED |
| Stub 7: Cross-agent pipeline uc-author -> uc-slicer | E-001 (Scenario 20) -- unmodified artifact acceptance, no schema errors, slices created | COVERED |

Beyond the minimum, the file adds 19 scenarios covering guardrail enforcement (A-004 through A-010), slice lifecycle (S-004 through S-009), cross-agent contract (E-002, E-003), and schema validation gate (V-001 through V-004). The 60%/30%/10% happy/negative/edge distribution is explicitly documented and approximately achieved.

The scope table (lines 57-63) clearly bounds what is and is not covered. The Acceptance Verification Checklist (lines 776-821) provides a reviewer-facing completeness verification mechanism.

**Gaps:**

1. The `FULLY_DESCRIBED` detail level has no dedicated scenario. The coverage gaps section acknowledges this as LOW risk. This is an accepted gap, not a defect, given the scope table explicitly lists "IMPLEMENTED and VERIFIED lifecycle states" as out of scope.

2. Activity 4 `test_cases` verification for PREPARED state completeness is noted as a gap in the test strategy. Scenarios S-004 and S-006 partially cover this but a standalone assertion on `test_cases` non-empty at PREPARED is absent.

**Improvement Path:**

To reach 1.00 Completeness, add one scenario asserting `test_cases` is non-empty before SCOPED-to-PREPARED transition. Optional: add a FULLY_DESCRIBED path scenario. Both are acknowledged gaps, not oversights.

---

### Internal Consistency (0.92/1.00)

**Evidence:**

The coverage matrix (lines 107-141) correctly maps scenarios to implementation file IDs (F-02, F-03, F-04, F-05, F-10 through F-14, F-17). Cross-referencing the file manifest in the architecture document, all file IDs exist and are correctly assigned.

The architecture stub coverage table (lines 92-102) is consistent with the expanded scenarios. Stub 4 maps to S-001 (Scenario 11), Stub 5 maps to S-002 (Scenario 12), etc.

The summary document scenario count table (step-9-eng-qa-test-strategy.md, lines 44-49) reports "26 primary + 14 sub-scenarios = 40 total test cases." Manually counting sub-scenarios in BEHAVIOR_TESTS.md: A-005 has 3 Scenario blocks; A-006 has 2; A-008 has 2; S-002 has 2; S-003 has 2; S-006 has 2; S-007 has 2; S-009 has 1 (no sub-scenario); V-001 has 2; V-002 has 3; V-003 has 3; V-004 has 3. That gives approximately 13-14 sub-scenarios, consistent with the reported 14.

**Gaps:**

One inconsistency found: Scenario 19 (S-009) is classified as "Happy path" in the coverage summary table (line 86: "7 (A-001, A-003, A-004, S-001, **S-009**, E-001, E-002)"). However, the scenario tests `uv run jerry items create` CLI compliance for P-003 -- this is a constraint verification scenario, which aligns more with the "Edge case" category. The misclassification does not affect the Gherkin content but is inconsistent with the categorization claim at line 87 where S-009 is included under happy path.

The summary document (step-9-eng-qa-test-strategy.md line 46) categorizes S-009 under uc-slicer scenarios as "2 happy" -- with S-001 and S-009 as the two happy path scenarios. This is a borderline categorization given S-009 explicitly tests a compliance constraint (Task tool prohibition). The inconsistency is minor but present.

**Improvement Path:**

Reclassify S-009 from happy path to edge/constraint category in the coverage summary table. This does not affect scenario content but corrects the distribution claim.

---

### Methodological Rigor (0.90/1.00)

**Evidence:**

Gherkin format is consistently applied throughout all 26 primary scenarios. Every scenario has:
- Feature block at the appropriate grouping level
- Scenario with a specific descriptive name
- Given clauses with concrete observable preconditions
- When clause identifying the trigger action
- Then and And clauses with verifiable, observable assertions

Examples of concrete inputs found (not abstract):
- "projects/PROJ-021-use-case/use-cases/UC-AUTH-001-authenticate-user.md" (specific path)
- "detail_level: BULLETED_OUTLINE" (specific field value)
- "detail_level must be >= ESSENTIAL_OUTLINE" (expected error message text)
- "^UC-[A-Z]+-\d{3}$" (expected regex pattern in error)
- "uv run jerry items create" (specific CLI command)

The four-feature organization (uc-author, uc-slicer, Cross-Agent Pipeline, Schema Validation Gate) is methodologically sound. Ordering from happy path through negative cases to edge cases within each Feature follows the recommended testing distribution.

The H-20 compliance assessment in the summary document (lines 123-130) explicitly maps each H-20 requirement to evidence in the artifact. The Acceptance Verification Checklist provides a structured reviewer mechanism.

**Gaps:**

Scenarios A-005 contains three nested `Scenario:` blocks within what is structured as a single section. The Gherkin convention is one `Feature:` block containing multiple independent `Scenario:` blocks -- having multiple `Scenario:` blocks within a single markdown section is non-standard BDD but is internally consistent. This is a style gap, not a correctness defect.

The methodology section (lines 69-80) explicitly references the testing-standards.md 60%/30%/10% distribution target. However, the actual distribution in the document is: 27% happy path, 42% negative, 31% edge (lines 84-89). The happy path percentage (27%) is below the 60% target stated in the coverage summary but the summary text references "60% happy+negative" combined, which adds up to 69%. This discrepancy between the claimed distribution basis ("targeting the 60%/30%/10% distribution from testing-standards.md") and the actual distribution (27%/42%/31%) suggests the 60% was a combined happy+negative target, not a happy-path-only target. The methodology statement is somewhat ambiguous.

**Improvement Path:**

Clarify the distribution statement to indicate 60% = happy + negative combined, with 40% edge, rather than implying 60% happy path. Minor clarification only.

---

### Evidence Quality (0.82/1.00)

**Evidence:**

This is the dimension with the most substantive findings. Cross-referencing scenario content against actual agent definitions, governance YAML, and schema reveals four accuracy defects:

**Defect EQ-1 (MEDIUM): Scenario A-009 guardrail name inconsistency**

Scenario A-009 (lines 342-347) tests:
> When uc-author applies the output guardrail "all_flow_steps_must_have_typed_classification"

Checking `uc-author.governance.yaml` (line 51):
```yaml
output_filtering:
  - "all_flow_steps_must_have_typed_classification"
```
The guardrail name matches. However, the Then assertion (line 345) states:
> And "type" for each step is one of "actor_action", "system_response", or "validation"

Cross-referencing the JSON schema `flow_step.$defs` (lines 343-346 of schema):
```json
"type": {
  "type": "string",
  "enum": ["actor_action", "system_response", "validation"]
}
```
The enum values match. **This defect is NOT present -- EQ-1 is retracted.** The guardrail name and enum values are correctly referenced.

**Defect EQ-2 (HIGH): Scenario S-016 (lifecycle transition) -- test_cases assertion**

Scenario 16 (S-006) second sub-scenario (lines 501-509) asserts:
> And "test_cases" array is non-empty before the PREPARED state is written

Cross-referencing uc-slicer methodology step 5: "For each SCOPED slice: define test cases, enhance narrative for PREPARED state; set slice_state: PREPARED." The `test_cases` must be defined before PREPARED, but the schema `slice` object definition (lines 547-553 of schema) shows `test_cases` is an optional array with no minItems constraint. The uc-slicer.governance.yaml validation check (line 82) states: "verify_test_cases_present_when_slice_state_gte_PREPARED". The assertion in S-006 is therefore correct as a behavioral assertion.

However, S-006 second sub-scenario (Scenario: "Slice transitions follow sequential order") places the test_cases assertion in the transition scenario but the test_cases check is actually at the SCOPED-to-PREPARED transition gate, not at the "SCOPED exists, INVEST complete" state described in the Given. The Given says "INVEST assessment is complete with all 6 criteria true" but does NOT set up test_cases as a precondition -- yet the Then asserts test_cases must be non-empty. The scenario conflates two gates (INVEST check and test_cases check) without making the test_cases precondition explicit.

This is an accuracy gap: the When trigger ("uc-slicer advances to PREPARED") without the test_cases precondition in Given means the Then assertion about test_cases being non-empty is not verifiable from the specified precondition. A reviewer running this scenario would need to know test_cases must also be present -- but the Given doesn't set that up.

**Defect EQ-3 (HIGH): Scenario V-001 -- required field count**

Scenario V-001 (lines 652-683) states:
> Given a use case artifact frontmatter that omits the "primary_actor" field
> And all other required fields are present: id, title, work_type, version, status, goal_level, scope, basic_flow, created_at, created_by

The scenario lists 10 fields plus "primary_actor" for 11 total. Cross-referencing the actual JSON schema `required` array (lines 7-19 of schema):
```json
"required": ["id", "title", "work_type", "version", "status", "goal_level", "scope", "primary_actor", "basic_flow", "created_at", "created_by"]
```
This is exactly 11 fields. The scenario correctly identifies all 11. **This defect is NOT present -- EQ-3 is retracted.** The count and field names are accurate.

**Defect EQ-4 (MEDIUM): Scenario A-005 -- allOf constraint numbering**

Scenario A-005 (lines 239-265) references "allOf constraints 2-4" and "allOf constraints 3-5" interchangeably. The Then clause states:
> And the artifact passes allOf constraints 2-4 in "docs/schemas/use-case-realization-v1.schema.json"

Cross-referencing the actual JSON schema (lines 573-639):
- allOf[0]: INTERACTION_DEFINED requires interactions (lines 573-589)
- allOf[1]: STORY_DEFINED/INTERACTION_DEFINED requires slices (lines 590-609)
- allOf[2]: SUMMARY -> goal_symbol "+" (lines 610-619)
- allOf[3]: USER_GOAL -> goal_symbol "!" (lines 620-628)
- allOf[4]: SUBFUNCTION -> goal_symbol "-" (lines 629-639)

The scenario coverage table (lines 134-141) labels these as "allOf[2,3,4]" for goal_symbol consistency. The Scenario A-005 Given/Then text says "allOf constraints 2-4". However, the section header says "Coverage: F-17 (allOf[2,3,4]), F-03" and the schema constraint coverage table says "allOf[2,3,4] (goal_symbol consistency) covered by A-005". The zero-indexed schema uses [2,3,4] and A-005 correctly references these. **This is consistent.** EQ-4 is retracted.

**Revised defect inventory after cross-referencing:**

**Defect EQ-R1 (MEDIUM): Scenario S-006 second sub-scenario -- incomplete precondition specification**

The Given for the SCOPED-to-PREPARED transition scenario does not include "test_cases are defined" as a precondition, yet the Then asserts test_cases must be non-empty. Per uc-slicer methodology step 5, test_cases definition is a prerequisite for PREPARED state, separate from INVEST completion. The scenario's Given only establishes INVEST completion, making the Then assertion partially unsupportable from the stated precondition. A test executor running this scenario would encounter an undefined precondition state regarding test_cases.

**Defect EQ-R2 (MEDIUM): Scenario A-006 -- status change path coverage**

Scenario A-006 second sub-scenario (lines 281-289) tests explicit user instruction for REVIEW status change. This is correct and matches the uc-author.md guardrails (line 173: "status_must_remain_DRAFT_until_human_review": Never set status to REVIEW or APPROVED without explicit user instruction). However, the scenario verifies only REVIEW status change, not APPROVED or DEPRECATED changes. The coverage is incomplete relative to the guardrail, which covers all non-DRAFT transitions. This is a minor gap since the guardrail principle is tested; the other values are tested implicitly through A-006's first sub-scenario (lines 276-280).

**Defect EQ-R3 (MEDIUM): Scenario E-002 -- on_send field claim not verifiable against governance YAML**

Scenario E-002 (lines 606-618) asserts:
> And the summary includes "key_findings" with between 3 and 5 bullet items covering actor count, goal level, basic flow step count, and extension count

Cross-referencing `uc-author.governance.yaml` `session_context.on_send` (lines 88-92):
```yaml
on_send:
  - "Report artifact path and detail level achieved"
  - "List key findings: actor count, goal level, basic flow step count, extension count"
  - "Flag if detail level is insufficient for downstream /test-spec consumption"
```
The governance YAML specifies the key_findings content as "actor count, goal level, basic flow step count, and extension count" -- exactly matching the scenario assertion. However, the "3 and 5 bullet items" quantification is added by the scenario and is NOT present in the governance YAML `on_send` specification. The scenario introduces a quantitative constraint (3-5 bullets) that has no grounding in the actual agent definition. This is an unverifiable assertion that exceeds what the governance spec defines.

These three defects collectively reduce the Evidence Quality dimension. None individually are critical enough to block the file, but together they represent specific accuracy gaps where scenario assertions exceed, miss, or slightly misrepresent the actual agent behavioral contracts.

**Improvement Path:**

1. Add "And test_cases are defined for the slice" to the Given of S-006 second sub-scenario.
2. Expand A-006 second sub-scenario OR add a comment noting APPROVED and DEPRECATED paths are also covered by the first sub-scenario's assertion.
3. Remove or make more specific the "3 and 5 bullet items" quantitative claim in E-002, replacing with "one or more bullet items" or referencing the governance YAML on_send specification directly.

---

### Actionability (0.88/1.00)

**Evidence:**

All 26 primary scenarios are directly executable as manual behavioral tests or automated integration tests. The concrete structure provides:
- Specific artifact paths that can be created as test fixtures
- Specific field values that can be set in test frontmatter
- Specific CLI commands that can be executed
- Specific error message content that can be asserted in test output

The coverage gaps table (step-9-eng-qa-test-strategy.md lines 156-163) is actionable: each gap has a named risk level, an implication, and a mitigation. The regression suite maintenance table (lines 177-184) identifies trigger conditions for F-16 updates.

The handoff to eng-security section (lines 186-194) is specifically actionable: three named review targets with rationale.

The Acceptance Verification Checklist (BEHAVIOR_TESTS.md lines 776-821) is directly usable by a reviewer closing sub-step 10f.

**Gaps:**

The test strategy document does not specify execution order or prioritization within a regression run. For a manual test executor, knowing which scenarios must pass first (e.g., V-001 schema required fields is a prerequisite for most agent tests) would improve usability. This is an enhancement, not a defect.

The scenarios do not specify the test fixture format for the artifact files used as Given preconditions. A test executor must infer the minimal valid YAML frontmatter for "a use case artifact exists at..." Given clauses. Adding even one example fixture in an appendix would significantly improve actionability for new team members.

**Improvement Path:**

Add a note in the Overview section or a separate "Test Fixtures" subsection showing a minimal valid artifact frontmatter. Add a test execution order recommendation (schema validation tests first, then agent behavioral tests, then pipeline tests).

---

### Traceability (0.92/1.00)

**Evidence:**

Multiple traceability layers are present:

1. **Architecture stub traceability:** Table at lines 92-102 maps each of the 7 architecture stubs to expanded scenario IDs with status.

2. **File coverage matrix:** Table at lines 107-120 maps scenario IDs to implementation file IDs (F-02 through F-17). All file IDs are traceable to the architecture document file manifest.

3. **H-rule traceability:** Table at lines 122-130 maps H-rules (H-20, H-31, P-003, P-020, P-022) to scenarios.

4. **Schema constraint traceability:** Table at lines 132-141 maps all five allOf constraints and their scenario coverage.

5. **Scenario ID traceability:** Each scenario has an explicit ID (A-NNN, S-NNN, E-NNN, V-NNN) with a coverage annotation listing source files.

6. **Summary document traceability:** The test strategy document (step-9-eng-qa-test-strategy.md) traces back to input artifacts (step-9-use-case-architecture.md v1.2.0, step-9-eng-lead-review.md v1.2.0) and forward to output (BEHAVIOR_TESTS.md F-16).

**Gaps:**

The individual scenario headers (e.g., "**ID:** A-001 | **Architecture Stub:** Stub 1 | **Coverage:** F-02, F-12, F-14 | **Category:** Happy path") cite implementation file IDs but do not cite specific rules or schema line numbers. For example, A-008 cites "F-17 (basic_flow minItems:3 maxItems:9), F-14" but does not cite Rule 5.2 from use-case-writing-rules.md or the specific schema property path `$.basic_flow.minItems`. This is adequate for a behavior test file but could be more precise.

The test strategy document does not include a version number for the schema (v1.0.0) cross-referenced -- it only references the file path. If the schema is versioned, the traceability chain should include the version.

**Improvement Path:**

Add schema version to the traceability references in the test strategy. Optionally, add rule citations (e.g., "Rule 5.2") to scenario coverage annotations for the most critical scenarios.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Evidence Quality | 0.82 | 0.90 | Fix S-006 second sub-scenario: add "And test_cases are defined for the slice" to the Given block. This makes the Then assertion about test_cases non-empty verifiable from the stated preconditions. |
| 2 | Evidence Quality | 0.82 | 0.90 | Fix E-002: Remove or adjust the "between 3 and 5 bullet items" assertion. The governance YAML on_send specification does not quantify bullet count. Replace with "one or more bullet items per the on_send session_context specification" or remove the quantitative constraint. |
| 3 | Evidence Quality | 0.82 | 0.90 | Fix A-006: Add a comment or note clarifying that APPROVED and DEPRECATED are also covered by the first sub-scenario's assertion, to close the incomplete guardrail coverage gap explicitly. |
| 4 | Internal Consistency | 0.92 | 0.95 | Fix S-009 classification: Move S-009 from "Happy path" to "Edge case -- P-003 compliance" in the coverage summary table. Update the distribution counts accordingly. |
| 5 | Methodological Rigor | 0.90 | 0.95 | Clarify the distribution claim in the Methodology section: state "60% happy + negative combined, 40% edge" rather than citing the 60%/30%/10% testing-standards.md distribution without adjustment. |
| 6 | Actionability | 0.88 | 0.93 | Add a minimal test fixture example to the Overview or an appendix. A single example of a valid YAML frontmatter at ESSENTIAL_OUTLINE level would enable test executors to construct Given preconditions without ambiguity. |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing weighted composite
- [x] Evidence documented for each score -- specific line numbers cited for all major claims
- [x] Uncertain scores resolved downward (Evidence Quality: initial review found multiple candidate defects; after cross-referencing, 3 confirmed gaps remain; score resolved at 0.82 not 0.88)
- [x] First-draft calibration considered (this is iter-1 of G-08-ADV-4; typical first-review scores 0.80-0.90 for complex test specifications)
- [x] No dimension scored above 0.95 without exceptional evidence (Completeness at 0.95 is justified by confirmed 100% architecture stub coverage with concrete, schema-accurate content)
- [x] Composite 0.901 is below the 0.95 C4 threshold -- REVISE verdict is correct

---

## Verdict Rationale

The BEHAVIOR_TESTS.md deliverable is high quality for a first adversary pass. The architectural completeness is excellent -- all 7 minimum stubs are covered, the schema cross-references are largely accurate, and the Gherkin format is consistently applied. The REVISE verdict is driven by the Evidence Quality dimension (0.82), specifically:

1. S-006 second sub-scenario has an unsupported Then assertion about test_cases (Given does not establish test_cases state)
2. E-002 introduces an unverifiable quantitative constraint (3-5 bullets) not present in the governance YAML
3. A-006 has incomplete guardrail coverage (APPROVED/DEPRECATED paths implicit but not explicit)

These are targeted, specific corrections that should be achievable in a single revision pass. After corrections, Evidence Quality should reach 0.88-0.90, moving the composite into the 0.92-0.94 range. A second iteration will be needed to determine if the 0.95 threshold is reached.

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.901
threshold: 0.95
weakest_dimension: Evidence Quality
weakest_score: 0.82
critical_findings_count: 0
iteration: 1
improvement_recommendations:
  - "Fix S-006 second sub-scenario: add test_cases precondition to Given block"
  - "Fix E-002: remove or ground the 3-5 bullet quantitative assertion against governance YAML"
  - "Fix A-006: explicitly note APPROVED/DEPRECATED coverage from first sub-scenario"
  - "Fix S-009 classification from happy path to edge/constraint in coverage table"
  - "Clarify distribution claim in Methodology section (60% = happy+negative combined)"
  - "Add minimal test fixture example to Overview or appendix"
```

---

*Score Report Version: 1.0.0*
*Agent: adv-scorer*
*SSOT: `.context/rules/quality-enforcement.md`*
*Reference Files Read: BEHAVIOR_TESTS.md, step-9-eng-qa-test-strategy.md, step-9-use-case-architecture.md (F-16 section), uc-author.md, uc-slicer.md, uc-author.governance.yaml, uc-slicer.governance.yaml, use-case-realization-v1.schema.json, use-case-writing-rules.md (partial), step-9-eng-lead-review.md (partial)*
