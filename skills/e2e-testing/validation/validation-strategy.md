---
document: validation-strategy.md
version: 1.0.0
skill: e2e-testing
phase: Phase 4 Step B
produced_by: eng-qa
workflow: e2e-skill-build-20260420-001
project: PROJ-017-e2e-testing-skill
source_section: skill-architecture.md Section 4 (all four sub-sections)
requirements_source: e2e-skill-requirements.md Section 6
quality_threshold: 0.94
---

# E2E Testing Validation Strategy

> The operative specification for how the /e2e-testing skill proves that generated tests
> actually verify application correctness -- not merely that they ran without error.

## Document Sections

| Section | Purpose |
|---------|---------|
| [1. Operational Definition](#1-operational-definition-test-ran-vs-test-verified-application-correctness) | The hard distinction between running and verifying |
| [2. Coverage Dimensions](#2-coverage-dimensions) | Five dimensions every test suite must address |
| [3. Six-Step Verifier Procedure](#3-six-step-verifier-procedure) | Executable runbook for e2e-verifier |
| [4. Metrics and Thresholds](#4-metrics-and-thresholds) | All metrics with formulas, thresholds, and confidence flags |
| [5. Escalation Procedure](#5-escalation-procedure) | Three-tier failure escalation and AE-006 trigger |
| [6. Orthogonality Disclosure](#6-orthogonality-disclosure) | Why adversary score and functional correctness are distinct |
| [7. Failure Mode Handling](#7-failure-mode-handling) | How each failure mode is diagnosed and resolved |
| [8. Verifier Verdict Schema](#8-verifier-verdict-schema) | Authoritative output contract for e2e-verifier |
| [References](#references) | Source traceability |

---

## 1. Operational Definition: "Test Ran" vs "Test Verified Application Correctness"

### 1.1 The Core Distinction

A test has **run** when it executes to completion without a test-runner error: exit code 0, no uncaught exceptions, no timeout, all steps reached. Running is a precondition for verification, not a substitute for it.

A test has **verified application correctness** when at least one of its `Then` assertions satisfies both of the following conditions simultaneously:

**Condition 1 -- Failure Sensitivity.** The assertion would fail if the application were in the wrong state for the specific defect class the scenario is meant to catch. An assertion that would pass regardless of whether the defect is present provides no verification value.

**Condition 2 -- Semantic Targeting.** The assertion targets a semantic application concern -- a business rule, a security property, or a user-observable behaviour -- rather than a technical execution artifact. Asserting that an HTTP 200 was returned, or that a DOM element exists, without also verifying its content or security implications, is not semantic targeting.

### 1.2 Three-Level Escalation Model (Navigation -> Identity -> Isolation)

Every security and correctness scenario should aspire to all three levels of assertion depth. Each level is progressively stronger evidence of verification:

**Level 1 (Navigation):** The application redirected to the expected URL or page state after the action.
- Example: `expect(page.url()).toBe('/dashboard')`
- Verification status: **RAN-ONLY** for correctness concerns. The URL changed, but nothing about whether the correct user's data is present has been verified.

**Level 2 (Identity):** The correct user's data is visible and confirms the right context.
- Example: `expect(page.getByText('Welcome, alice@acme.com')).toBeVisible()`
- Verification status: **VERIFIED** for the identity concern. This assertion would fail if the wrong user were logged in or if the session were corrupted.

**Level 3 (Isolation):** Another user's data is provably absent from the user's view.
- Example: `expect(page.getByText('bob@acme.com')).not.toBeVisible()`
- Verification status: **VERIFIED** for the isolation concern (authorization / data leakage). This assertion would fail if a horizontal privilege escalation were present.

A test is fully verified for an authentication flow only when all three levels are asserted. Navigation alone (Level 1 only) is the most common form of false confidence in generated E2E suites.

### 1.3 Assertion Classification Taxonomy

The `e2e-verifier` classifies every `Then` assertion in every scenario as one of three classes:

| Class | Definition | Action Required |
|-------|------------|-----------------|
| **VERIFIED** | The assertion is sensitive to the defect class it targets. It would fail if the application were in the wrong state for that defect. | None -- counts positively toward quality metrics |
| **RAN-ONLY** | The assertion is present but insensitive. It would pass even if the targeted defect were present. | Flag for escalation if rate exceeds 30%; mandatory escalation above 50% |
| **ABSENT** | No assertion is present for the scenario's stated purpose as declared in `@basis:` tags and scenario description. | Mandatory escalation; any ABSENT is a FAIL trigger |

---

## 2. Coverage Dimensions

The `e2e-verifier` checks that the test suite (not just a single scenario) provides coverage across five dimensions for every feature under test. Coverage dimensions are evaluated at the suite level, not the scenario level.

| Dimension | Definition | Priority | Coverage Standard |
|-----------|------------|----------|------------------|
| **Happy path** | The nominal flow succeeds: the user completes the intended action and the system returns the expected state. At least one VERIFIED assertion confirms correct output. | First-tier | Every flow must have at least one happy-path scenario with at least one VERIFIED assertion. A suite lacking happy-path coverage is not ready for production. |
| **Failure path** | The application handles expected errors gracefully: invalid input is rejected with a correct error message, network failures surface to the user with appropriate messaging, auth failures redirect correctly without leaking data. | First-tier | Each failure type defined in the test basis (`@basis:` tags) must have a corresponding scenario. Failure-path scenarios commonly produce RAN-ONLY assertions (error page displayed) when they should produce VERIFIED assertions (error message text correct AND no session data leaked). |
| **Boundary** | The application behaves correctly at input limits: empty values, maximum-length strings, negative numbers, special characters (XSS vectors), concurrent access patterns. | Second-tier | Apply to flows where boundary violations cause security or correctness risk. Not mandatory for all flows at initial release, but strongly recommended for any flow involving user-supplied input. |
| **Security** | The application enforces its security properties at the user-journey layer. At minimum, one WSTG-tagged scenario per applicable mandatory category (ATHN, ATHZ, SESS, INPV, BUSL, APIT). | First-tier for any flow involving authentication, session management, or sensitive data per P-E2E-08 | Security scenarios MUST carry `@wstg:WSTG-v42-<CAT>-<NN>` tags. Security assertions MUST be at Level 2 or Level 3 of the navigation-identity-isolation model (Level 1 alone is always RAN-ONLY for security concerns). |
| **Agentic divergence** | For flows where the subject under test is itself an LLM agent: the test asserts over the agent's trajectory (tool calls made, tool calls NOT made, intermediate state after each tool call), not only the final output state. | First-tier for any flow testing an AI-powered feature | Agentic-divergence coverage is unique to this skill. The standards lane provides no normative model for this dimension (Gap 1 in lane-standards). It is a Jerry supplement. An agentic flow test that only checks final output is RAN-ONLY at the trajectory level. |

### Coverage Assessment Decision

| Dimension | State | Verdict Trigger |
|-----------|-------|-----------------|
| First-tier dimension | COVERED (at least one VERIFIED assertion) | No action |
| First-tier dimension | PARTIAL (covered only by RAN-ONLY assertions) | REVISE trigger |
| First-tier dimension | ABSENT | FAIL trigger |
| Second-tier dimension | ABSENT | Informational flag in L1 report; no verdict change |

---

## 3. Six-Step Verifier Procedure

This is the executable runbook for `e2e-verifier`. Each step is imperative and contains explicit decision points. Steps must be executed in order. Do not skip steps.

### STEP 1: Parse Gherkin and Extract Assertion Inventory

**Action:** Read the Gherkin feature file and, if codegen mode, the `.spec.ts` file. Read the `executor-trace.json` from e2e-executor.

**Decision point:** If `executor-trace.json` is absent or malformed -- go to [7.4 Verifier Can't Parse Generated Artifact](#74-verifier-cant-parse-generated-artifact).

**Produce:** An `assertion_list` -- one entry per `Then` clause in the Gherkin feature:
- `step_text`: the full text of the Then clause
- `basis_ref`: the `@basis:` tag value on the parent Scenario
- `expected_sensitivity`: the `expected_sensitivity` field from `author-plan.json` for this step
- `mode_artifact_ref`: the Playwright `expect()` call (codegen) or trace step reference (explorer)
- `scenario_id`: the parent Scenario identifier

**Output check:** Every `Then` clause in the feature file must appear in `assertion_list`. If any Then clause has no corresponding entry, the feature file and the plan are out of sync -- emit a `plan-mismatch-warning` and continue with the available assertions.

### STEP 2: Map Each Assertion to a P-E2E Principle

**Action:** For each entry in `assertion_list`, classify by principle category:
- **Security check (P-E2E-08):** The Scenario carries a `@wstg:` tag referencing one of the six mandatory WSTG categories. Apply security sensitivity rubric.
- **Functional check (P-E2E-02):** Declarative business-rule verification. The Scenario has a `@basis:` pointing to a story ID or risk item. Apply functional sensitivity rubric.
- **Trajectory check (P-E2E-04):** The assertion uses agentic-actor Gherkin extension syntax (`Then the agent called...`, `Then the agent did not call...`). Apply trajectory sensitivity rubric.

The principle category determines the sensitivity rubric applied in Step 3. A Scenario can map to multiple principle categories (e.g., a security scenario may also have functional assertions).

### STEP 3: Score Each Assertion -- Sensitivity Classification

**Action:** Apply the classification rubric to every entry in `assertion_list`. Every assertion MUST receive a class. No assertion may be left unclassified.

**Decision criteria -- functional and security assertions:**

| What the assertion checks | Classification |
|---------------------------|----------------|
| URL navigation only (URL changed, no content verified) | RAN-ONLY |
| HTTP status code only | RAN-ONLY |
| Element visibility without content for a content-dependent concern | RAN-ONLY |
| Element visibility for an existence concern (element present/absent) | VERIFIED |
| Element visibility AND content/text match | VERIFIED |
| ABSENCE of sensitive data (negative assertion: other user's data NOT visible) | VERIFIED |
| Security property enforced (no session token issued, error message does not leak data) | VERIFIED |
| No assertion present for the scenario's stated purpose | ABSENT |

**Decision criteria -- trajectory assertions:**

| What the assertion checks | Classification |
|---------------------------|----------------|
| Tool called, schema not validated (schema is `{}` or absent) | RAN-ONLY |
| Tool called with schema that accepts any object | RAN-ONLY |
| Tool called with schema that distinguishes correct from incorrect invocation | VERIFIED |
| Tool NOT called (negative assertion with rationale) | VERIFIED |
| Intermediate state after tool call, with a testable predicate | VERIFIED |
| Final output only, no trajectory inspection | RAN-ONLY (at trajectory level) |

**Calibration examples (load `skills/e2e-testing/examples/auth-journey.feature` if available):**

- "Then I see the dashboard" -- RAN-ONLY (navigation/visibility only; no content verified)
- "Then the dashboard shows Welcome, alice@acme.com" -- VERIFIED (identity; specific content checked)
- "Then I do not see bob@acme.com on the dashboard" -- VERIFIED (isolation; negative assertion)
- "Then no session cookie is set" -- VERIFIED (security property; would fail if auth bypass occurred)
- "Then the agent called web_search with schema {}" -- RAN-ONLY (empty schema validates nothing)
- "Then the agent called web_search with schema {type: object, required: [query]}" -- VERIFIED (schema distinguishes correct from incorrect call)

### STEP 4: Compute Coverage Across Five Dimensions

**Action:** For the feature under test, evaluate coverage for all five dimensions defined in Section 2.

For each dimension:
1. Enumerate all scenarios in the feature tagged or described as targeting this dimension.
2. Determine if at least one scenario for this dimension has at least one VERIFIED assertion.
3. Assign dimension state: COVERED, PARTIAL, or ABSENT.

**Decision point:** If any first-tier dimension is PARTIAL or ABSENT -- record as a potential REVISE or FAIL trigger. Do not emit verdict yet; continue to Step 5.

### STEP 5: Compute Functional-Correctness Metrics

**Action:** Using the counts from `executor-trace.json` and `author-plan.json`, compute all five metrics.

Define:
- C = count of locators generated by e2e-executor that were accepted without human modification
- G = total count of locators generated by e2e-executor
- E = count of locators expected per `author-plan.json` `expected_locators`
- CS = count of test steps in the execution trace that completed without a WebDriver error
- GS = total count of test steps in the execution trace
- ES = count of test steps expected per `author-plan.json` `scenario_steps`
- edits = count of generated steps that required human modification before the test passed
- V = count of assertions classified as VERIFIED in Step 3
- T = total count of assertions classified in Step 3

Compute:

```
element_precision = C / G
  [SINGLE-STUDY -- GenIA-E2ETest n=12; threshold is directional reference point]

element_recall = C / E
  [SINGLE-STUDY]

execution_precision = CS / GS
  [SINGLE-STUDY; informational at initial release -- not a threshold gate]

execution_recall = CS / ES
  [SINGLE-STUDY]

manual_modification_rate = edits / GS
  [SINGLE-STUDY]

assertion_sensitivity_rate = V / T
  [eng-architect-derived metric; NOT sourced from GenIA-E2ETest; no external validation.
   Introduced in skill-architecture Section 4.2. Disclosed per P-022.]
```

**Division-by-zero guard:** If any denominator (G, E, ES, GS, T) is zero, flag the corresponding metric as `null` with reason `"denominator-zero: no {locators|steps|assertions} in trace"`. A null metric counts as a FAIL trigger for the dimensions it covers (a test with no assertions cannot pass).

**Corpus size check:** If the eval corpus at the configured `CORPUS_PATH` has fewer than 20 scenarios, flag all six metric results with: `[UNVALIDATED -- corpus below 20-scenario threshold required by P-E2E-09]`. All metrics are still computed; they are informational but not production-grade quality guarantees.

### STEP 6: Emit Verdict

**Action:** Apply the decision tree against all evidence collected in Steps 1-5.

**PASS -- requires ALL of the following:**
- `execution_recall >= THRESHOLD_EXECUTION_RECALL` (default: 0.80)
- `element_precision >= THRESHOLD_ELEMENT_PRECISION` (default: 0.70)
- `manual_modification_rate <= THRESHOLD_MMR` (default: 0.15)
- `assertion_sensitivity_rate >= 0.70`
- Zero ABSENT assertions
- RAN-ONLY assertion rate < 30% of all classified assertions
- No first-tier coverage dimension is ABSENT or PARTIAL

**REVISE -- escalate to e2e-author for targeted revision when any one of:**
- Any metric is between its threshold and (threshold - 0.05)
- RAN-ONLY assertion rate is 30-50% of all classified assertions
- Any first-tier coverage dimension is PARTIAL (covered only by RAN-ONLY assertions)

**FAIL -- escalate to e2e-author with full diagnostic when any one of:**
- Any metric is more than 0.05 below its threshold
- RAN-ONLY assertion rate exceeds 50% of all classified assertions
- Any ABSENT assertion is found
- Any first-tier coverage dimension is ABSENT
- Any assertion denominator is null (no assertions or no steps found)

**Escalation routing (P-E2E-04 HARD):** FAIL and REVISE verdicts route exclusively to `e2e-author`. NEVER route to `e2e-executor`. The executor is an actor; it does not make replanning decisions.

**S-014 process quality check:** After computing the functional-correctness verdict, invoke `/adversary` (adv-scorer) for C2+ deliverables per H-17. Compute the S-014 process quality score against the six-dimension rubric (Completeness, Internal Consistency, Methodological Rigor, Evidence Quality, Actionability, Traceability). Threshold: 0.94. If adv-scorer is unreachable, use the AD-010 Level 1 fallback (see Section 7.4).

**Emit both scores as distinct, non-combined fields.** See Section 6 for the mandatory orthogonality statement.

**Persist outputs (P-002 REQUIRED):** Write all verdict artifacts before signalling completion. See Section 8 for the schema.

---

## 4. Metrics and Thresholds

All metric thresholds source from `output/{testrun_id}/governance-config.yaml`. The values below are initial-release defaults. They are explicitly intended to be tightened as Jerry's own eval corpus matures beyond the single-study baseline.

| Metric | Formula | Initial Threshold | Direction | Confidence Flag |
|--------|---------|-------------------|-----------|-----------------|
| `element_precision` | C / G | >= 0.70 | higher is better | [SINGLE-STUDY -- GenIA-E2ETest n=12; threshold is directional reference point, not empirically validated against Jerry's corpus] |
| `element_recall` | C / E | >= 0.70 | higher is better | [SINGLE-STUDY] |
| `execution_recall` | CS / ES | >= 0.80 | higher is better | [SINGLE-STUDY] |
| `execution_precision` | CS / GS | informational | higher is better | [SINGLE-STUDY; not a threshold gate at initial release] |
| `manual_modification_rate` | edits / GS | <= 0.15 | lower is better | [SINGLE-STUDY] |
| `assertion_sensitivity_rate` | V / T | >= 0.70 | higher is better | [eng-architect-derived metric; NOT from GenIA-E2ETest; no external validation -- P-022 disclosure. This metric operationalises Section 1.3's classification taxonomy as a measurable summary statistic.] |
| `wstg_category_coverage` | count of covered categories | 6/6 mandatory | higher is better | [P-E2E-08 mandatory; eng-architect judgment on six-category minimum] |
| `s014_process_score` | S-014 six-dimension rubric | >= 0.94 | higher is better | [RT-004 triangulation; not empirically optimal; see requirements §3 RT-004 for derivation rationale] |

### Threshold Calibration Note

The GenIA-E2ETest study [SINGLE-STUDY -- LIMITED STATISTICAL POWER, n=12] reported 77% element precision and 85% execution recall as observed values. The initial-release thresholds (0.70, 0.80) are set conservatively below these reported values to account for the limited statistical power of the single study. As Jerry's own eval corpus grows beyond 20 scenarios, these thresholds should be revised upward on evidence, not convention.

The 0.94 S-014 threshold is a triangulated value anchored between the Jerry SSOT H-13 floor (0.92) and the eng-team-local maximum (0.95). It is not independently evidenced as an empirically optimal threshold. See requirements §3 RT-004 for the full triangulation rationale.

### Maturity Targets

| Metric | Initial Target | Maturity Target (corpus >= 50 scenarios) |
|--------|---------------|------------------------------------------|
| element_precision | 0.70 | 0.77 |
| element_recall | 0.70 | 0.77 |
| execution_recall | 0.80 | 0.85 |
| manual_modification_rate | 0.15 | 0.10 |
| assertion_sensitivity_rate | 0.70 | 0.80 |

---

## 5. Escalation Procedure

### 5.1 First Failure (Iteration 1 of H-14 Cycle)

**Trigger:** e2e-verifier emits FAIL or REVISE verdict.

**Action:**
1. Produce `failure-diagnostic.json` containing:
   - `failure_category`: one of selector | timing | runtime | data | visual | interaction (per six-category flake taxonomy [VENDOR BLOG -- QA Wolf])
   - `webdriver_error_class`: the WebDriver Level 2 error taxonomy value (e.g., "no such element", "stale element reference", "element click intercepted", "timeout")
   - `dom_snapshot_ref`: path to the `dom-snapshots/{step}.json` file at the failure point
   - `failing_assertions`: the ABSENT or RAN-ONLY assertions that triggered escalation
   - `coverage_dimension_gaps`: any first-tier dimensions that are ABSENT or PARTIAL
   - `replan_recommendation`: specific, actionable revision instruction for e2e-author (e.g., "Add live DOM snapshot before email locator generation. Replace text-match selector with data-testid anchor. Add negative isolation assertion for other user's email.")
2. Route `failure-diagnostic.json` exclusively to `e2e-author`. Do NOT route to `e2e-executor`.
3. e2e-author receives the diagnostic, produces a revised plan that substantively differs from the prior plan, and resubmits to e2e-executor.

**Constraint:** e2e-author MUST NOT re-submit the same plan unchanged. A revised plan must address the specific failure category and replan_recommendation. If the author cannot produce a different plan without research, it should consult ps-investigator before replanning.

### 5.2 Second Failure (Iteration 2)

**Trigger:** e2e-verifier emits FAIL on the same scenario after author's first replanning.

**Action:**
1. Produce strengthened `failure-diagnostic.json` with second-iteration annotations:
   - Include prior diagnostic for comparison
   - Cite requirements §6.1 three-level escalation model (navigation -> identity -> isolation) if assertion depth is insufficient
   - Require e2e-author to add assertions at a deeper level, not merely adjust selectors
   - `replan_recommendation` must specify which level (1/2/3) is missing and provide an example assertion at that level
2. Route to `e2e-author` only.

### 5.3 Third Failure (Iteration 3 -- AE-006 Escalation)

**Trigger:** e2e-verifier emits FAIL on the same scenario for the third time (H-14 minimum cycle exhausted).

**Action:**
1. Emit AE-006 mandatory human escalation notice in verifier verdict: `"ae006_escalation": true`
2. e2e-reporter emits FAIL verdict in L0 report with AE-006 flag and autonomy-tier declaration
3. Notify user via L0 report with plain-language explanation:
   - "This test scenario has failed validation 3 times. Human review is required before this scenario can be accepted."
   - Include the full failure diagnostic history
4. Do NOT attempt a fourth automated retry.

### 5.4 Escalation Routing Summary

| Verdict | Routes To | Routes Away From |
|---------|-----------|-----------------|
| PASS | e2e-reporter (for L0/L1/L2 assembly) | no escalation needed |
| REVISE | e2e-author (targeted revision) | NOT to e2e-executor |
| FAIL (iterations 1-2) | e2e-author (full diagnostic) | NOT to e2e-executor |
| FAIL (iteration 3) | user (AE-006) | all automated routes exhausted |

---

## 6. Orthogonality Disclosure

The following statement MUST be included verbatim in every `verifier-verdict.json` output as the `orthogonality_note` field:

> "The S-014 process quality score measures whether the skill followed its methodology: document completeness, internal consistency, methodological rigor, evidence quality, actionability, and traceability. The GenIA-E2ETest functional-correctness metrics (execution_recall, element_precision, manual_modification_rate, assertion_sensitivity_rate) measure whether the generated test actually verifies application correctness. These are orthogonal concerns. A deliverable can score 0.96 on S-014 (well-documented methodology) and 0.65 on execution_recall (fragile selectors that rarely find their targets). Conversely, a suite can achieve 0.95 execution_recall (tests run reliably) while scoring 0.88 on S-014 (missing @basis: tags, no WSTG coverage, poor documentation). Both are failures. Neither score substitutes for the other. The e2e-verifier MUST emit both scores as distinct fields and MUST NOT average or combine them for a single pass/fail signal. A test run that passes one track but fails the other is a failed test run."

### Why Orthogonality Matters

The S-014 process quality rubric was designed to evaluate whether an analytical or planning deliverable followed a rigorous methodology. Applied to E2E test artifacts, it captures whether the test plan is complete, traceable, and well-documented. But a well-documented test plan with `@basis:` tags on every scenario and WSTG coverage notes does not guarantee that the generated Playwright locators resolve correctly against the live DOM. Locator quality is a runtime concern; process quality is a design-time concern.

Conversely, a test that achieves high execution_recall (most steps run successfully) may have been authored without any `@basis:` traceability or WSTG security scenario coverage -- scoring poorly on S-014 even though its functional execution was reliable.

Conflating these two measurements produces false confidence. High S-014 scores do NOT imply high functional correctness. High functional correctness does NOT imply high S-014 scores. Users of the skill deserve clear reporting on both dimensions independently.

This orthogonality principle is a P-022 (no deception) enforcement mechanism: the skill must not create a single combined score that obscures the distinction between "did we follow the right process" and "does the test actually work."

---

## 7. Failure Mode Handling

### 7.1 No Assertions Found

**Condition:** Step 1 of the verifier procedure finds zero `Then` clauses in the Gherkin feature file.

**Diagnosis:** The feature file is either malformed, was authored with only Given-When steps, or all Then clauses were stripped during a failed edit.

**Response:**
1. Classify all assertions as ABSENT (division-by-zero guard: T=0 produces null assertion_sensitivity_rate).
2. Emit FAIL verdict immediately. Do not proceed to metric computation.
3. `failure_category`: runtime
4. `replan_recommendation`: "No Then assertions found in feature file. e2e-author must add at least one VERIFIED Then assertion per scenario before execution."
5. Escalate to e2e-author as a Iteration 1 FAIL. Counts toward H-14 iteration limit.

### 7.2 All Assertions Pass But Application is Broken

**Condition:** Functional-correctness metrics are acceptable (execution_recall >= 0.80, element_precision >= 0.70) and all assertions return green, but the application is demonstrably in an incorrect state (e.g., another user's data is visible, but the test did not assert its absence).

**Diagnosis:** This is the RAN-ONLY failure mode -- the test suite lacks VERIFIED assertions that would detect the defect. Metrics pass because the tests ran without error; the assertions simply do not test the right thing.

**Detection mechanism:** The `assertion_sensitivity_rate` metric and the ABSENT/RAN-ONLY classification are the primary detectors. If assertion_sensitivity_rate < 0.70 or any critical assertion is RAN-ONLY at a Level 1 (navigation only) depth for a security concern, escalate.

**Response:**
1. Emit REVISE verdict with assertion inventory showing RAN-ONLY classes for the insufficient assertions.
2. `replan_recommendation`: "Assertions present but insufficient depth. Apply three-level escalation model: add identity assertion (Level 2) and isolation assertion (Level 3) to cover the security property. Current assertions verify navigation only."
3. Escalate to e2e-author.

### 7.3 Verifier Can't Parse Generated Artifact

**Condition:** `executor-trace.json` is absent, malformed JSON, or its schema does not match the expected schema documented in skill-architecture Section 5.3.

**Diagnosis:** e2e-executor produced a malformed trace, or the trace was not written to disk (P-002 violation by executor).

**Response:**
1. Emit `trace-invalid.json` diagnostic with: path expected, error class (absent | malformed-json | schema-mismatch), and any partial content parsed.
2. Escalate to `e2e-author` (not to `e2e-executor` directly -- the author is responsible for the plan that drove the executor; a malformed trace may indicate the plan was ambiguous).
3. Include in `replan_recommendation`: "Executor trace is invalid. Verify executor ran to completion. Check output directory for partial artifacts. If trace was not written, executor may have encountered an unrecoverable browser error -- inspect browser-errors.json."
4. Counts as Iteration 1 FAIL toward H-14 limit.

### 7.4 Playwright MCP Unavailable

**Condition:** e2e-executor reports that the Playwright MCP server is unreachable (connection timeout, server not started, tool calls return empty or error).

**Diagnosis:** AD-010 Level 1 degradation condition. The browser execution substrate is unavailable; tests cannot be executed.

**Response (AD-010 Level 1 fallback):**
1. e2e-verifier does not receive a valid trace. Receives `sut-unreachable.json` or `allowlist-violation.json` from executor instead.
2. Emit partial verdict: functional-correctness metrics are all null with flag "EXECUTION-UNAVAILABLE -- Playwright MCP unreachable".
3. S-014 process quality assessment MAY still be computed against the planning artifacts (author-plan.json, {scenario}.feature) -- this is the Level 1 degraded output.
4. Do NOT escalate to e2e-author as a standard FAIL. Escalate to user with diagnostic:
   "Test execution is unavailable: Playwright MCP server unreachable. Check MCP server configuration in .claude/settings.local.json. Verify @playwright/mcp is installed at the pinned version documented in PLAYBOOK.md. Functional-correctness metrics are not available until execution is restored."
5. This failure mode does NOT count toward the H-14 iteration limit (it is an infrastructure failure, not a test quality failure).

### 7.5 SUT Unreachable

**Condition:** e2e-executor reports that the System Under Test URL is unreachable (network timeout, DNS failure, 5xx response on initial navigation).

**Diagnosis:** The application is not running or the configured `SUT_ENTRY_URL` is incorrect.

**Response:**
1. e2e-executor emits `sut-unreachable.json` with retry-exhaustion note.
2. e2e-verifier receives the diagnostic and emits partial verdict with null functional-correctness metrics and flag "EXECUTION-BLOCKED -- SUT unreachable".
3. Escalate to user with diagnostic:
   "The system under test at [SUT_ENTRY_URL] is unreachable. Verify the application is running and accessible. If testing against a staging environment, confirm environment is healthy. This is not a test quality failure; no H-14 iterations are consumed."
4. Does NOT count toward H-14 iteration limit.

---

## 8. Verifier Verdict Schema

The authoritative output contract for every `verifier-verdict.json`:

```json
{
  "testrun_id": "E2E-NNNN",
  "scenario": "<scenario-id from author-plan.json>",
  "verdict": "PASS | REVISE | FAIL",
  "iteration": 1,
  "autonomy_tier": "AUTONOMOUS | SUPERVISED | MANAGED-EQUIVALENT",

  "functional_correctness": {
    "element_precision": 0.75,
    "element_recall": 0.82,
    "execution_precision": 0.95,
    "execution_recall": 0.88,
    "manual_modification_rate": 0.09,
    "assertion_sensitivity_rate": 0.75,
    "thresholds_met": true,
    "corpus_size": 3,
    "corpus_flag": "[UNVALIDATED -- corpus below 20-scenario threshold]",
    "metric_confidence_flag": "[SINGLE-STUDY -- GenIA-E2ETest n=12; assertion_sensitivity_rate has no external validation]"
  },

  "assertion_inventory": [
    {"step_text": "Then I see the dashboard", "class": "RAN-ONLY", "rationale": "Navigation only; content not verified"},
    {"step_text": "Then the dashboard shows Welcome, alice@acme.com", "class": "VERIFIED", "rationale": "Identity-level check"}
  ],

  "coverage_dimensions": {
    "happy_path": "COVERED",
    "failure_path": "PARTIAL",
    "boundary": "ABSENT",
    "security": "COVERED",
    "agentic_divergence": "N/A"
  },

  "process_quality_score_s014": 0.945,
  "process_quality_thresholds_met": true,
  "s014_confidence_flag": "[RT-004 triangulation; not empirically optimal threshold]",

  "failure_category": null,
  "webdriver_error_class": null,
  "escalation_to": null,
  "replan_recommendation": null,
  "ae006_escalation": false,

  "orthogonality_note": "The S-014 process quality score measures whether the skill followed its methodology: document completeness, internal consistency, methodological rigor, evidence quality, actionability, and traceability. The GenIA-E2ETest functional-correctness metrics (execution_recall, element_precision, manual_modification_rate, assertion_sensitivity_rate) measure whether the generated test actually verifies application correctness. These are orthogonal concerns. A deliverable can score 0.96 on S-014 and 0.65 on execution_recall (fragile selectors). Both are failures. Neither score substitutes for the other. They are never averaged or combined for a single pass/fail signal. A test run that passes one track but fails the other is a failed test run.",

  "artifacts_persisted": [
    "skills/e2e-testing/output/E2E-NNNN/verifier-verdict.json",
    "skills/e2e-testing/output/E2E-NNNN/assertion-inventory.json",
    "skills/e2e-testing/output/E2E-NNNN/metrics-snapshot.json",
    "skills/e2e-testing/output/E2E-NNNN/adv-scorer-result.json"
  ]
}
```

**Required fields:** All fields in the schema above are required in every verdict. Fields that do not apply (e.g., `failure_category` on a PASS verdict) use `null`, not absent. The schema is intentionally explicit: a verifier that omits `orthogonality_note` or `autonomy_tier` is violating P-022.

---

## References

| Source | Content |
|--------|---------|
| `projects/PROJ-017-e2e-testing-skill/orchestration/e2e-skill-build-20260420-001/design/skill-architecture.md` Section 4 | Authoritative architectural design for all four sub-sections of this document |
| `projects/PROJ-017-e2e-testing-skill/orchestration/e2e-skill-build-20260420-001/synthesis/e2e-skill-requirements.md` Section 6 | Requirements-level validation strategy specification |
| P-E2E-09 (HARD) | Published quality gate with exact metric formulas |
| P-E2E-04 (HARD) | Planner-Executor-Verifier triad; escalation to author only |
| P-E2E-02 (HARD) | Declarative Gherkin with @basis: tags |
| P-E2E-08 (HARD) | WSTG six mandatory categories |
| P-E2E-10 (HARD) | Autonomy-tier declaration in every verdict |
| P-022 | No deception; confidence flags; orthogonality disclosure |
| GenIA-E2ETest (Giulini et al.) | Metric formulas: element_precision, element_recall, execution_recall, MMR [SINGLE-STUDY -- LIMITED STATISTICAL POWER, n=12] |
| skill-architecture Section 4.2 | `assertion_sensitivity_rate` introduced as eng-architect-derived metric [no external validation -- P-022 disclosure] |
| quality-enforcement.md H-14 | Creator-critic-revision cycle; minimum 3 iterations |
| quality-enforcement.md AE-006 | Mandatory human escalation after 3 consecutive failures at C3+ |
| QA Wolf six-category flake taxonomy | selector / timing / runtime / data / visual / interaction [VENDOR BLOG -- not independently validated] |
| RT-004 triangulation | 0.94 S-014 threshold: triangulated from SSOT floor (0.92) and eng-team max (0.95); not empirically optimal |
