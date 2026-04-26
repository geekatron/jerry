---
template: e2e-validation-check.md
version: 1.0.0
operationalizes_principles: [P-E2E-04, P-E2E-09]
produced_by: eng-qa (Phase 4 Step B)
consumed_by: e2e-verifier
inputs:
  - TRACE_PATH
  - PLAN_PATH
  - CORPUS_PATH
  - THRESHOLD_EXECUTION_RECALL
  - THRESHOLD_ELEMENT_PRECISION
  - THRESHOLD_MMR
  - THRESHOLD_QUALITY
  - TESTRUN_ID
  - AUTONOMY_TIER
outputs:
  - "verifier-verdict.json"
  - "assertion-inventory.json"
  - "failure-diagnostic.json (FAIL only)"
  - "adv-scorer-result.json"
  - "metrics-snapshot.json"
---

# Template: E2E Validation Check

## Document Sections

| Section | Purpose |
|---------|---------|
| [Purpose](#purpose) | What this template drives |
| [When to Use](#when-to-use) | Trigger conditions |
| [Input Parameters](#input-parameters) | All parameters with types and defaults |
| [Template Body](#template-body) | Prompt template with placeholders |
| [Expected Output](#expected-output) | Output format and structure |
| [Validation Rules](#validation-rules) | Pre-flight checks on populated template |
| [Example](#example) | Complete worked example |
| [Source](#source) | Principle and architecture traceability |

---

## Purpose

Drive `e2e-verifier` through the six-step correctness validation procedure. This template is the architectural heart of the skill: it defines whether a generated test has merely run or has actually verified application correctness. It computes functional-correctness metrics (GenIA-E2ETest formulas [SINGLE-STUDY]), classifies each assertion as VERIFIED/RAN-ONLY/ABSENT, emits a PASS/REVISE/FAIL verdict, and triggers structured escalation to `e2e-author` on failure. It also invokes the S-014 process quality self-score (H-15, H-17) and emits both scores as orthogonal fields -- never combined.

---

## When to Use

Invoke this template after every `executor-trace.json` is received from `e2e-executor`. Also invoke on verifier re-run triggered by e2e-author replanning. Do not invoke before an execution trace exists -- there is nothing to validate.

---

## Input Parameters

| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| `TRACE_PATH` | file path | YES | Path to `executor-trace.json` from e2e-executor | none |
| `PLAN_PATH` | file path | YES | Path to `author-plan.json` from e2e-author | none |
| `CORPUS_PATH` | file path | YES | Path to named eval corpus JSON; used for metric baseline comparison | none -- flag [UNVALIDATED] if corpus < 20 scenarios |
| `THRESHOLD_EXECUTION_RECALL` | float | NO | Minimum execution_recall | 0.80 [SINGLE-STUDY] |
| `THRESHOLD_ELEMENT_PRECISION` | float | NO | Minimum element_precision | 0.70 [SINGLE-STUDY] |
| `THRESHOLD_MMR` | float | NO | Maximum manual_modification_rate | 0.15 [SINGLE-STUDY] |
| `THRESHOLD_QUALITY` | float | NO | Minimum S-014 process quality score | 0.94 (RT-004 triangulation) |
| `TESTRUN_ID` | string | YES | Run identifier matching `^E2E-\d{4}$` | none |
| `AUTONOMY_TIER` | enum | YES | `AUTONOMOUS`, `SUPERVISED`, or `MANAGED-EQUIVALENT` | none -- block if absent |

All thresholds source from `e2e-governance-config.yaml`, not hardcoded in agent definitions. The values above are defaults; governance config overrides take precedence.

---

## Template Body

```
---
TESTRUN_ID: {{TESTRUN_ID}}
TRACE_PATH: {{TRACE_PATH}}
PLAN_PATH: {{PLAN_PATH}}
AUTONOMY_TIER: {{AUTONOMY_TIER}}
THRESHOLD_EXECUTION_RECALL: {{THRESHOLD_EXECUTION_RECALL}}
THRESHOLD_ELEMENT_PRECISION: {{THRESHOLD_ELEMENT_PRECISION}}
THRESHOLD_MMR: {{THRESHOLD_MMR}}
THRESHOLD_QUALITY: {{THRESHOLD_QUALITY}}
---

You are e2e-verifier in validation mode.

CONSTITUTIONAL REFERENCE:
- P-003: You MUST NOT spawn sub-agents. You invoke /adversary (adv-scorer) as a tool, not as a sub-agent delegation.
- P-022: You MUST emit both quality scores as distinct fields and MUST NOT combine them. State evidence confidence flags ([SINGLE-STUDY]) wherever thresholds derive from GenIA-E2ETest.
- P-E2E-04: On FAIL, escalate ONLY to e2e-author. NEVER escalate to e2e-executor. The executor is an actor, not a decision-maker.
- P-E2E-09: All metric computations MUST cite the corpus they are computed against.

GUARD: If AUTONOMY_TIER is absent from governance-config.yaml, HALT and emit:
  {"error": "P-022 ENFORCEMENT HALT", "reason": "autonomy_tier absent from governance config", "action": "user must supply tier before validation proceeds"}

---

## SIX-STEP VALIDATION PROCEDURE

### STEP 1: PARSE GHERKIN -- EXTRACT ASSERTION INVENTORY

Read the Gherkin feature file at {{PLAN_PATH}} and the execution trace at {{TRACE_PATH}}.

For each Scenario in the feature file:
1. Enumerate every "Then" clause and record it in an assertion list.
2. Map each assertion to its stated verification purpose from the @basis: tag and scenario description.
3. In codegen mode: cross-reference each "Then" clause against its Playwright `expect()` call in the .spec.ts artifact; record whether the expect() call matches the intent.
4. In explorer mode: cross-reference against the execution trace's per-step assertion records.

Produce: `assertion_list` with one entry per Then clause:
  { "step_text": "...", "basis_ref": "...", "mode_artifact_ref": "...", "scenario_id": "..." }

DO NOT classify assertions yet. Only enumerate.

---

### STEP 2: MAP EACH ASSERTION TO A P-E2E PRINCIPLE

For each entry in assertion_list, determine which principle category governs the assertion:
- Security check (P-E2E-08): involves WSTG category -- ATHN, ATHZ, SESS, INPV, BUSL, APIT
- Functional check (P-E2E-02): declarative business rule verification
- Trajectory check: agentic-flow tool-call assertion (P-E2E-04 boundary)
- Locator check (P-E2E-06): element selection precision

The principle category determines which sensitivity rubric applies in Step 3.

---

### STEP 3: SCORE EACH ASSERTION -- SENSITIVITY CLASSIFICATION

For each assertion, apply the classification rubric. Every assertion MUST receive a class. No assertion may be left unclassified.

CLASSIFICATION RUBRIC:

VERIFIED (assertion is sensitive to the defect it targets):
  - Checks both element visibility AND content/text match
  - Verifies ABSENCE of sensitive data (e.g., another user's email is not visible)
  - Checks element existence for an existence concern
  - Verifies a security property: token not issued, error message does not leak user enumeration data
  - Trajectory: tool called with correct schema AND position constraint met

RAN-ONLY (assertion present but insensitive -- would pass even if the application were in the wrong state):
  - URL navigation check only (URL changed, but content not verified)
  - Element visibility check without content check for a content-dependent concern
  - HTTP 200 status without response body verification
  - Trajectory: tool called, schema not validated (schema is empty or `{}`)

ABSENT (no assertion for the scenario's stated purpose):
  - Scenario description states a security property but no Then clause tests it
  - @basis: tag references a WSTG category but no @wstg: tagged assertion is present
  - Author-plan.json lists an expected_sensitivity = "VERIFIED" but Gherkin has no matching Then clause

WORKED EXAMPLES (calibration reference):

Example A -- VERIFIED:
  Gherkin: "Then I do not see alice@example.com on the dashboard"
  Playwright: expect(page.getByText('alice@example.com')).not.toBeVisible()
  Classification: VERIFIED (isolation concern; assertion would fail if alice's email appeared)

Example B -- RAN-ONLY for content, VERIFIED for existence:
  Gherkin: "Then the error message is displayed"
  Playwright: expect(page.locator('[data-testid=error-msg]')).toBeVisible()
  Classification: RAN-ONLY for content-dependent concern (text not checked); VERIFIED for existence
  Guidance: If the scenario requires verifying the ERROR MESSAGE TEXT, this is RAN-ONLY. Add text assertion.

Example C -- ABSENT:
  Scenario basis: @basis:WSTG-v42-ATHN-01 (tests authentication bypass)
  Gherkin: "Then I see the login page again"
  Classification: ABSENT for the authentication bypass concern.
  Rationale: Seeing the login page again only verifies navigation (RAN-ONLY), not that no session was created.
  Required: "Then no session cookie is set" or "Then the response does not contain a Set-Cookie header with session scope"

THREE-LEVEL ESCALATION MODEL (navigation -> identity -> isolation):
  Level 1 (navigation): URL changed -- RAN-ONLY
  Level 2 (identity): Correct user's content visible -- VERIFIED for identity
  Level 3 (isolation): Other user's content NOT visible -- VERIFIED for isolation
  The security test is only FULLY VERIFIED when all three levels are asserted.

---

### STEP 4: COMPUTE COVERAGE DIMENSIONS

Check the test suite (not just the current scenario) against the five required dimensions.
A dimension is COVERED if at least one scenario targets it with a VERIFIED (not RAN-ONLY) assertion.
A dimension is PARTIAL if covered only by RAN-ONLY assertions.
A dimension is ABSENT if no scenario addresses it.

| Dimension | Definition | First-tier? |
|-----------|------------|-------------|
| happy_path | Nominal flow succeeds; expected output confirmed | YES |
| failure_path | Application handles errors gracefully; error state verified | YES |
| boundary | Input limits tested (empty, max-length, special characters) | Second-tier |
| security | WSTG-tagged scenarios present for applicable categories | YES (if auth/session/biz-logic involved) |
| agentic_divergence | Trajectory assertions present (tool calls, intermediate state) | YES (if SUT is LLM agent) |

Coverage gaps are REVISE triggers for first-tier dimensions and informational flags for second-tier.

---

### STEP 5: COMPUTE METRICS (P-E2E-09 FORMULAS)

Using counts from execution trace and author plan:

Let:
  C  = number of generated locators accepted without human modification
  G  = total number of locators generated by e2e-executor
  E  = number of locators expected per author-plan.json expected_locators
  CS = number of generated test steps that ran to completion without WebDriver error
  GS = total number of test steps generated by e2e-executor
  ES = number of test steps expected per author-plan.json scenario_steps
  edits = number of generated steps that required human modification before passing

Formulas [SINGLE-STUDY -- GenIA-E2ETest n=12; thresholds are directional reference points]:
  element_precision = C / G      (target: >= {{THRESHOLD_ELEMENT_PRECISION}})
  element_recall = C / E         (target: >= {{THRESHOLD_ELEMENT_PRECISION}})
  execution_precision = CS / GS  (informational; not a threshold gate at initial release)
  execution_recall = CS / ES     (target: >= {{THRESHOLD_EXECUTION_RECALL}})
  manual_modification_rate = edits / GS  (target: <= {{THRESHOLD_MMR}})

Also compute:
  assertion_sensitivity_rate = (count VERIFIED) / (total assertions)
  Target: >= 0.70
  [NOTE: assertion_sensitivity_rate is an eng-architect-derived metric introduced in skill-architecture Section 4.2.
   It is NOT sourced from GenIA-E2ETest. No external validation. Disclosed per P-022.]

If eval corpus at {{CORPUS_PATH}} has fewer than 20 scenarios, flag all metric results:
  [UNVALIDATED -- corpus below 20-scenario threshold required by P-E2E-09]

---

### STEP 6: EMIT VERDICT

Apply the decision tree:

PASS (all of the following):
  - execution_recall >= {{THRESHOLD_EXECUTION_RECALL}}
  - element_precision >= {{THRESHOLD_ELEMENT_PRECISION}}
  - manual_modification_rate <= {{THRESHOLD_MMR}}
  - assertion_sensitivity_rate >= 0.70
  - zero ABSENT assertions
  - RAN-ONLY assertions < 30% of total

REVISE (escalate to e2e-author for targeted revision; any one of):
  - Any metric between threshold and (threshold - 0.05)
  - RAN-ONLY assertions 30-50% of total
  - First-tier coverage dimension PARTIAL (covered only by RAN-ONLY assertions)

FAIL (escalate to e2e-author with full diagnostic; any one of):
  - Any metric more than 0.05 below its threshold
  - RAN-ONLY assertions > 50% of total
  - Any ABSENT assertion
  - First-tier coverage dimension ABSENT

ESCALATION ROUTING:
  All FAIL and REVISE verdicts route ONLY to e2e-author (P-E2E-04 HARD).
  NEVER route to e2e-executor.
  NEVER retry without a revised plan.

FAILURE CATEGORY (classify per six-category flake taxonomy):
  - selector: WebDriver error "no such element" or "stale element reference" -- locator failed
  - timing: WebDriver error "element click intercepted" or timeout -- SPA not ready
  - runtime: uncaught exception in test code or executor trace
  - data: assertion failed because test data state was incorrect (not a locator issue)
  - visual: visual diff threshold exceeded (visual_diff_threshold in governance config)
  - interaction: element found but action failed (e.g., element obscured, disabled)

---

### S-014 PROCESS QUALITY SELF-SCORE (H-15, H-17)

Invoke /adversary (adv-scorer) for C2+ deliverables:
  Input: this validation verdict and the test artifacts
  Scoring dimensions: Completeness, Internal Consistency, Methodological Rigor, Evidence Quality, Actionability, Traceability
  Threshold: {{THRESHOLD_QUALITY}} (RT-004 triangulation; not empirically optimal -- disclosed per P-022)

Record result in adv-scorer-result.json.

If adv-scorer MCP tool is unavailable (AD-010 Level 1 fallback):
  Emit: {"s014_score": null, "s014_note": "S-014 score UNAVAILABLE -- adv-scorer MCP unreachable; functional-correctness verdict still valid"}
  Do NOT block the functional-correctness verdict.

---

### ORTHOGONALITY DECLARATION (MANDATORY IN EVERY VERDICT OUTPUT)

Include verbatim in every verifier-verdict.json:

"orthogonality_note": "The S-014 process quality score and the GenIA-E2ETest functional-correctness metrics are orthogonal concerns. A deliverable can score well on S-014 (well-documented methodology) and fail on execution_recall (fragile selectors), or vice versa. Both tracks must pass independently. Neither score substitutes for the other. They are never averaged or combined for a single pass/fail signal."

---

### OUTPUT PERSISTENCE (P-002 REQUIRED)

Write ALL of the following artifacts to disk regardless of verdict:
1. `skills/e2e-testing/output/{{TESTRUN_ID}}/verifier-verdict.json` -- full verdict with both scores
2. `skills/e2e-testing/output/{{TESTRUN_ID}}/assertion-inventory.json` -- per-assertion VERIFIED/RAN-ONLY/ABSENT
3. `skills/e2e-testing/output/{{TESTRUN_ID}}/metrics-snapshot.json` -- raw metric values for eval corpus
4. `skills/e2e-testing/output/{{TESTRUN_ID}}/adv-scorer-result.json` -- S-014 score (or UNAVAILABLE notice)

On FAIL or REVISE, additionally write:
5. `skills/e2e-testing/output/{{TESTRUN_ID}}/failure-diagnostic.json` -- escalation payload for e2e-author

Emit: "ARTIFACTS PERSISTED: [file paths]"
```

---

## Expected Output

**`verifier-verdict.json`** -- Top-level verdict containing both quality tracks as distinct fields:

```json
{
  "testrun_id": "E2E-NNNN",
  "scenario": "<scenario-id>",
  "verdict": "PASS | REVISE | FAIL",
  "autonomy_tier": "AUTONOMOUS | SUPERVISED | MANAGED-EQUIVALENT",
  "functional_correctness": {
    "element_precision": 0.78,
    "element_recall": 0.82,
    "execution_precision": 0.95,
    "execution_recall": 0.88,
    "manual_modification_rate": 0.09,
    "assertion_sensitivity_rate": 0.75,
    "thresholds_met": true,
    "corpus_flag": "[SINGLE-STUDY]"
  },
  "coverage_dimensions": {
    "happy_path": "COVERED",
    "failure_path": "COVERED",
    "boundary": "ABSENT",
    "security": "COVERED",
    "agentic_divergence": "N/A"
  },
  "process_quality_score_s014": 0.945,
  "process_quality_thresholds_met": true,
  "failure_category": null,
  "webdriver_error_class": null,
  "escalation_to": null,
  "replan_recommendation": null,
  "orthogonality_note": "..."
}
```

**`assertion-inventory.json`** -- Per-assertion classification list.

**`failure-diagnostic.json`** (FAIL/REVISE only) -- Escalation payload for e2e-author containing: failure_category, webdriver_error_class, dom_snapshot_ref, replan_recommendation.

---

## Validation Rules

| Rule | Principle | Check |
|------|-----------|-------|
| Both quality scores emitted as distinct fields | P-E2E-09, P-022 | Reject verdict if process_quality_score_s014 and functional_correctness are absent or averaged |
| Every assertion classified | P-E2E-09 | Reject if any Then clause has no VERIFIED/RAN-ONLY/ABSENT classification |
| FAIL/REVISE escalates to e2e-author only | P-E2E-04 | Reject escalation payload if escalation_to != "e2e-author" |
| autonomy_tier in verdict | P-E2E-10 | Reject if field absent from verifier-verdict.json |
| Corpus flag on metrics if < 20 scenarios | P-022 | Flag [UNVALIDATED] if corpus size < 20 |
| Orthogonality note present | P-022 | Reject if orthogonality_note field absent |
| FAIL includes replan_recommendation | P-E2E-04 | Reject FAIL verdict without replan_recommendation field |

---

## Example

**Invocation context:**
- Testrun: E2E-0003
- Scenario: auth-journey/login-happy-path
- Trace: 8 steps, 7 completed, 1 WebDriver error "no such element" on dashboard locator
- Locators: 4 generated, 3 accepted without edit, 4 expected
- Manual edits: 0
- Assertions: 4 Then clauses

**Step 1 -- assertion list:**
```json
[
  {"step_text": "Then the user is redirected to the dashboard", "basis_ref": "STORY-042"},
  {"step_text": "Then the dashboard displays content belonging to alice@acme.com", "basis_ref": "STORY-042"},
  {"step_text": "Then no other user's data is visible on the dashboard", "basis_ref": "STORY-042"},
  {"step_text": "Then no session token is issued for an unauthenticated path", "basis_ref": "WSTG-v42-ATHN-01"}
]
```

**Step 3 -- sensitivity classification:**
```json
[
  {"step_text": "Then the user is redirected to the dashboard", "class": "RAN-ONLY", "rationale": "URL navigation check only; no content verification"},
  {"step_text": "Then the dashboard displays content belonging to alice@acme.com", "class": "VERIFIED", "rationale": "Identity-level check; text match to specific user's name"},
  {"step_text": "Then no other user's data is visible on the dashboard", "class": "VERIFIED", "rationale": "Isolation-level check; negative assertion sensitive to authorization failure"},
  {"step_text": "Then no session token is issued for an unauthenticated path", "class": "VERIFIED", "rationale": "Security property check; would fail if Set-Cookie issued without auth"}
]
```

**Step 5 -- metrics:**
- element_precision: 3/4 = 0.75 (>= 0.70 PASS)
- element_recall: 3/4 = 0.75 (>= 0.70 PASS)
- execution_recall: 7/8 = 0.875 (>= 0.80 PASS)
- manual_modification_rate: 0/4 = 0.00 (<= 0.15 PASS)
- assertion_sensitivity_rate: 3/4 = 0.75 (>= 0.70 PASS)
- RAN-ONLY rate: 1/4 = 25% (< 30% PASS)

**Step 6 -- verdict: PASS**

**verifier-verdict.json (abbreviated):**
```json
{
  "testrun_id": "E2E-0003",
  "scenario": "auth-journey/login-happy-path",
  "verdict": "PASS",
  "autonomy_tier": "SUPERVISED",
  "functional_correctness": {
    "element_precision": 0.75,
    "element_recall": 0.75,
    "execution_recall": 0.875,
    "manual_modification_rate": 0.00,
    "assertion_sensitivity_rate": 0.75,
    "thresholds_met": true,
    "corpus_flag": "[SINGLE-STUDY -- GenIA-E2ETest n=12]"
  },
  "process_quality_score_s014": 0.946,
  "process_quality_thresholds_met": true,
  "failure_category": null,
  "escalation_to": null,
  "orthogonality_note": "The S-014 process quality score and the GenIA-E2ETest functional-correctness metrics are orthogonal concerns. A deliverable can score well on S-014 and fail on execution_recall, or vice versa. Both tracks must pass independently. Neither score substitutes for the other. They are never averaged or combined for a single pass/fail signal."
}
```

---

## Source

| Item | Source |
|------|--------|
| Six-step validation procedure | skill-architecture Section 4.1 (must be encoded verbatim); requirements §6.3 |
| VERIFIED/RAN-ONLY/ABSENT classification rubric | requirements §6.1, §6.3 |
| Three-level escalation model (navigation-identity-isolation) | requirements §6.1 |
| GenIA-E2ETest metric formulas | P-E2E-09 (HARD); requirements §2 P-E2E-09; requirements §6.4 [SINGLE-STUDY] |
| assertion_sensitivity_rate metric | skill-architecture Section 4.2 (eng-architect derivation; no external validation -- P-022 disclosure) |
| PASS/REVISE/FAIL decision tree | skill-architecture Section 4.1 Step 6; requirements §6.3 Step 5 |
| Six-category flake taxonomy | requirements §8 QA Wolf MIRROR posture [VENDOR BLOG] |
| Escalation to e2e-author only | P-E2E-04 (HARD); skill-architecture Section 4.3 |
| Orthogonality disclosure | skill-architecture Section 4.4 (verbatim requirement); requirements §6.5 |
| S-014 self-score requirement | H-15, H-17; skill-architecture Section 3.3 |
| Five coverage dimensions | requirements §6.2; skill-architecture Section 4.1 Step 4 |
| AD-010 Level 1 adv-scorer fallback | skill-architecture Section 2.4 failure modes |
