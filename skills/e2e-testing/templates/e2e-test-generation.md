---
template: e2e-test-generation.md
version: 1.0.0
operationalizes_principles: [P-E2E-01, P-E2E-02, P-E2E-08, P-E2E-10]
produced_by: eng-qa (Phase 4 Step B)
consumed_by: e2e-author
inputs:
  - BLOCK_SCOPE_DOC
  - RISK_LEVEL
  - CRITICALITY
  - LIST_BASIS_REFS
  - SUT_URL
  - EXECUTION_MODE
  - AUTONOMY_TIER
  - ISO29119_ARTIFACTS
outputs:
  - "{scenario}.feature"
  - "author-plan.json"
  - "author-rationale.md"
---

# Template: E2E Test Generation

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

Drive the `e2e-author` agent through its primary workflow: receive a risk-classified scenario scope and produce a complete Gherkin `.feature` file with `@basis:` tags, a structured `author-plan.json` for downstream executor consumption, and WSTG-tagged security scenarios for the mandatory six categories. Risk classification MUST precede any scenario authoring step.

---

## When to Use

Invoke this template when:
- A `git diff` or `scope-document.json` is available and test authoring must begin
- A user story or risk item requires Gherkin scenario coverage for a web application flow
- WSTG security scenario generation is required for any flow involving authentication, session, business logic, or API access
- `e2e-author` receives a `failure-diagnostic.json` escalation from `e2e-verifier` and must replan

Do NOT invoke when the subject under test is itself an LLM agent requiring trajectory assertions -- use `e2e-agentic-flow.md` instead.

---

## Input Parameters

| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| `BLOCK_SCOPE_DOC` | JSON block or raw diff text | YES | `scope-document.json` from e2e-analyst, or raw `git diff` when analyst absent | none -- must be supplied |
| `RISK_LEVEL` | enum | YES | Risk classification for the flow under test: `HIGH`, `MEDIUM`, or `LOW` | none -- must be supplied before any Gherkin step |
| `CRITICALITY` | enum | YES | Jerry criticality tier: `C1`, `C2`, `C3`, or `C4` | `C2` (governance-config default) |
| `LIST_BASIS_REFS` | array of strings | YES | Story IDs, WSTG test IDs, or risk item references cited in `@basis:` tags | none -- at least one required per P-E2E-02 |
| `SUT_URL` | string | YES | URL or description of the system under test | none |
| `EXECUTION_MODE` | enum | YES | `codegen` or `explorer` | `codegen` |
| `AUTONOMY_TIER` | enum | YES | `AUTONOMOUS`, `SUPERVISED`, or `MANAGED-EQUIVALENT` | `SUPERVISED` (conservative) |
| `ISO29119_ARTIFACTS` | boolean | NO | Generate ISO 29119-3 compatible test case specification alongside Gherkin | `false` |
| `TESTRUN_ID` | string | YES | Run identifier matching `^E2E-\d{4}$` | none -- must be supplied |
| `FAILURE_DIAGNOSTIC` | JSON block | NO | Populated only on replanning; `failure-diagnostic.json` from e2e-verifier | empty |

---

## Template Body

```
---
TESTRUN_ID: {{TESTRUN_ID}}
SUT_URL: {{SUT_URL}}
CRITICALITY: {{CRITICALITY}}
AUTONOMY_TIER: {{AUTONOMY_TIER}}
EXECUTION_MODE: {{EXECUTION_MODE}}
RISK_LEVEL: {{RISK_LEVEL}}
---

You are e2e-author in test-generation mode.

CONSTITUTIONAL REFERENCE:
- P-003: You MUST NOT spawn sub-agents or delegate to other agents. Your outputs are Gherkin files and JSON plans only.
- P-020: If the scope requires a full-suite run without explicit user confirmation, STOP and prompt the user.
- P-022: You MUST NOT claim test coverage for flows not in the scope document. Declare analyst-absent mode in output header if no scope-document.json is present.

INPUTS:
- Scope document or diff: {{BLOCK_SCOPE_DOC}}
- Basis references: {{LIST_BASIS_REFS}}
- Replanning context (if applicable): {{FAILURE_DIAGNOSTIC}}

---

STEP 1 — RISK CLASSIFICATION (MANDATORY BEFORE ANY GHERKIN STEP)

Before writing a single Gherkin keyword, populate the risk classification block:

risk_classification:
  flow: <name of user flow under test>
  risk_level: {{RISK_LEVEL}}
  criticality: {{CRITICALITY}}
  justification: <1-2 sentences: why this risk_level and criticality given the changed code and test basis>
  basis_refs: {{LIST_BASIS_REFS}}

DO NOT proceed to Step 2 if risk_level or criticality are absent.

---

STEP 2 — FEATURE / RULE DECOMPOSITION

Produce the Feature → Rule → Scenario tree BEFORE writing any Given-When-Then steps.
This is the scenario modularization step (GenIA-E2ETest Level 1 pattern).

Format:
Feature: <Capability name>
  Rule: <Business rule 1>
    Scenario: <scenario name 1>
    Scenario: <scenario name 2>
  Rule: <Business rule 2>
    Scenario: <scenario name 3>

Do NOT write step text yet. Only names and structure. Get this structure confirmed before proceeding.

---

STEP 3 — GHERKIN AUTHORING (DECLARATIVE STYLE REQUIRED)

For each Scenario in the tree above, write the complete Given-When-Then steps.

MANDATORY RULES (P-E2E-02 HARD enforcement):
1. Tags MUST appear before each Scenario header: @basis:<ref> @risk:{{RISK_LEVEL}} @criticality:{{CRITICALITY}}
2. Every Scenario MUST have at least one @basis: tag with a non-empty, parseable reference value from {{LIST_BASIS_REFS}}.
3. WHEN steps MUST NOT contain UI verbs. Forbidden tokens: "click", "type", "enter", "navigate to", "fill in", "select", "scroll", "hover". Use declarative phrasing ("the user submits", "the user provides", "the system receives").
4. GIVEN steps establish preconditions only. No imperative action verbs.
5. THEN steps are assertions about application state, not about element presence alone.

EXAMPLE of correct declarative When: "When the user submits login credentials"
EXAMPLE of REJECTED imperative When: "When the user clicks the login button and types their password"

---

STEP 4 — WSTG SECURITY SCENARIO GENERATION (P-E2E-08 HARD)

For any feature involving {{SUT_URL}} that touches authentication, session management, authorization, input validation, business logic, or API access, generate AT MINIMUM one scenario per applicable WSTG v4.2 mandatory category:

| Category | Tag format | Scenario focus |
|----------|-----------|----------------|
| ATHN | @wstg:WSTG-v42-ATHN-01 | Authentication bypass, credential exposure, brute-force |
| ATHZ | @wstg:WSTG-v42-ATHZ-01 | Horizontal/vertical privilege escalation, IDOR |
| SESS | @wstg:WSTG-v42-SESS-01 | Session fixation, token expiry, cookie flags |
| INPV | @wstg:WSTG-v42-INPV-01 | Input boundary, XSS, injection at UI layer |
| BUSL | @wstg:WSTG-v42-BUSL-01 | Business rule abuse, workflow bypass, price manipulation |
| APIT | @wstg:WSTG-v42-APIT-01 | API endpoint authentication, rate limiting at browser layer |

Each WSTG scenario MUST include both the @wstg: tag AND a @basis: tag referencing a WSTG test ID.

If a category is genuinely inapplicable to the feature under test, document the exclusion rationale in author-rationale.md -- do not silently omit.

---

STEP 5 — SELF-REVIEW CHECKLIST (H-15 REQUIRED BEFORE OUTPUT)

Complete this checklist. Do NOT emit output artifacts until all items are PASS.

[ ] risk_level field is populated (HIGH/MEDIUM/LOW) -- P-E2E-01
[ ] criticality field is populated (C1-C4) -- P-E2E-01
[ ] Every Scenario has at least one @basis: tag -- P-E2E-02
[ ] No When step contains UI-verb tokens -- P-E2E-02
[ ] At least one @wstg: scenario per applicable mandatory category -- P-E2E-08
[ ] autonomy_tier: {{AUTONOMY_TIER}} is declared in author-plan.json header -- P-E2E-10
[ ] execution_mode: {{EXECUTION_MODE}} is declared in author-plan.json -- P-E2E-05
[ ] If replanning: revised plan differs substantively from prior failed plan -- P-E2E-04

---

STEP 6 — OUTPUT PERSISTENCE (P-002 REQUIRED)

Write the following artifacts to disk:
1. `skills/e2e-testing/output/{{TESTRUN_ID}}/{scenario-slug}.feature` -- the Gherkin file
2. `skills/e2e-testing/output/{{TESTRUN_ID}}/author-plan.json` -- structured plan for e2e-executor
3. `skills/e2e-testing/output/{{TESTRUN_ID}}/author-rationale.md` -- authoring decisions and WSTG exclusion rationale

After writing, emit: "ARTIFACTS PERSISTED: [list file paths]"

If ISO 29119 artifacts are requested ({{ISO29119_ARTIFACTS}} = true), also write:
4. `skills/e2e-testing/output/{{TESTRUN_ID}}/test-case-spec-iso29119.md`
```

---

## Expected Output

**`{scenario-slug}.feature`** -- Gherkin feature file with:
- `Feature:` header with description
- `Rule:` groupings per business rule
- `Scenario:` entries with `@basis:`, `@risk:`, `@criticality:`, and `@wstg:` (security) tags
- Declarative Given-When-Then steps (no UI-verb tokens in When)

**`author-plan.json`** -- Machine-readable plan consumed by e2e-executor containing:
- `testrun_id`, `scenario_id`, `risk_level`, `criticality`, `execution_mode`, `autonomy_tier`
- `basis_refs` array
- `scenario_steps` array with `keyword`, `text`, `expected_state`, `expected_sensitivity` per step
- `expected_locators` array with `selector` and `role` per locator hint

**`author-rationale.md`** -- Prose rationale for authoring decisions, WSTG category exclusions, and replanning changes.

**Validation rules applied to output before downstream consumption:**
- Every Scenario has a `@basis:` tag -- P-E2E-02
- No When step contains forbidden UI-verb tokens -- P-E2E-02
- At least one `@wstg:` scenario for each applicable mandatory WSTG category -- P-E2E-08
- `author-plan.json` contains `autonomy_tier` at top level -- P-E2E-10
- `author-plan.json` contains `execution_mode` at top level -- P-E2E-05

---

## Validation Rules

| Rule | Principle | Check |
|------|-----------|-------|
| risk_level present in author-plan.json | P-E2E-01 | Reject if absent or not HIGH/MEDIUM/LOW |
| criticality present in author-plan.json | P-E2E-01 | Reject if absent or not C1/C2/C3/C4 |
| No UI verbs in When steps | P-E2E-02 | Regex: reject if "click|type|enter|navigate to|fill in|select|scroll|hover" appears in any When clause |
| @basis: tag on every Scenario | P-E2E-02 | Reject if any Scenario lacks @basis: with non-empty value |
| WSTG mandatory six-category coverage | P-E2E-08 | Reject if any applicable category lacks a @wstg: tagged scenario |
| autonomy_tier declared in plan | P-E2E-10 | Reject if missing from author-plan.json top-level |
| execution_mode declared in plan | P-E2E-05 | Reject if not "codegen" or "explorer" |

---

## Example

**Invocation context:**
- Testrun: E2E-0003
- SUT: https://app.acme.com (user authentication flow, login page changed in diff)
- Risk level: HIGH
- Criticality: C2
- Basis refs: STORY-042, WSTG-v42-ATHN-01, WSTG-v42-SESS-02
- Mode: codegen
- Autonomy: SUPERVISED

**BLOCK_SCOPE_DOC (abbreviated):**
```json
{
  "changed_files": [{"path": "src/auth/login.ts", "classification": "business_logic"}],
  "prioritised_scope": [{"flow": "auth-journey/login", "risk_level": "HIGH"}],
  "wstg_gaps": ["SESS"]
}
```

**Step 1 output:**
```
risk_classification:
  flow: auth-journey/login
  risk_level: HIGH
  criticality: C2
  justification: >
    Login business logic was modified. Authentication failures at this layer expose user
    credentials and bypass security controls. HIGH risk per ISO 29119-2 likelihood × impact.
  basis_refs: [STORY-042, WSTG-v42-ATHN-01, WSTG-v42-SESS-02]
```

**Step 2 output:**
```gherkin
Feature: User Authentication Journey
  Rule: Valid credentials grant access
    Scenario: Successful login with valid credentials
    Scenario: Login form preserves redirect destination
  Rule: Invalid credentials are rejected
    Scenario: Login fails with incorrect password
    Scenario: Login fails after 5 consecutive failures
  Rule: Session properties are secure
    Scenario: Session token expires after inactivity
```

**Step 3 output (excerpt):**
```gherkin
Feature: User Authentication Journey
  Background:
    Given the application is accessible at "https://app.acme.com"
    Given no active session exists

  @basis:STORY-042 @risk:HIGH @criticality:C2
  Scenario: Successful login with valid credentials
    Given a registered user with username "alice@acme.com" and a known valid password
    When the user submits login credentials
    Then the user is redirected to the dashboard
    Then the dashboard displays content belonging to alice@acme.com
    Then no other user's data is visible on the dashboard
```

**Step 4 WSTG output (excerpt):**
```gherkin
  @basis:WSTG-v42-ATHN-01 @wstg:WSTG-v42-ATHN-01 @risk:HIGH @criticality:C2
  Scenario: Authentication fails with malformed credentials
    Given an unauthenticated user
    When the user submits a login request with an empty password field
    Then the application returns an authentication error
    Then no session token is issued
    Then the error message does not reveal whether the username exists

  @basis:WSTG-v42-SESS-02 @wstg:WSTG-v42-SESS-02 @risk:HIGH @criticality:C2
  Scenario: Session token expires after configured inactivity period
    Given an authenticated user with an active session
    When the session has been idle for longer than the configured timeout
    Then any subsequent request is rejected with a session-expired response
    Then the user is redirected to the login page
```

**Self-review checklist result:** All 8 items PASS.

**Artifacts persisted:**
- `skills/e2e-testing/output/E2E-0003/auth-journey-login.feature`
- `skills/e2e-testing/output/E2E-0003/author-plan.json`
- `skills/e2e-testing/output/E2E-0003/author-rationale.md`

---

## Source

| Item | Source |
|------|--------|
| Risk classification before authoring | P-E2E-01 (HARD); requirements §2 P-E2E-01; skill-architecture Section 3.1 |
| Declarative Gherkin + @basis: | P-E2E-02 (HARD); requirements §2 P-E2E-02; skill-architecture Section 3.1 validation rules |
| WSTG six mandatory categories | P-E2E-08 (HARD); requirements §2 P-E2E-08; skill-architecture Section 3.1 |
| Autonomy-tier declaration in plan header | P-E2E-10 (HARD); requirements §2 P-E2E-10; skill-architecture Section 8 |
| Execution mode declaration | P-E2E-05 (HARD); requirements §2 P-E2E-05 |
| Section skeleton and placeholder conventions | skill-architecture Section 3.1 |
| BLOCK_/LIST_/UPPER_SNAKE_ placeholder convention | skill-architecture Section 3.1 placeholder conventions |
| GenIA-E2ETest scenario modularization (Level 1) | requirements §8 Innovator Posture; implementation-plan Section 3 |
