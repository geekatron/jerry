---
document: PLAYBOOK.md
skill: e2e-testing
version: 1.0.0
produced_by: eng-qa (Phase 4 Step D)
workflow: e2e-skill-build-20260420-001
project: PROJ-017-e2e-testing-skill
date: 2026-04-21
resolves: [OQ-E2E-001, OQ-E2E-002, OQ-E2E-003, OQ-E2E-004, OQ-E2E-005, OQ-E2E-006, OQ-E2E-007]
---

# /e2e-testing Playbook

> Operational how-to for users invoking the /e2e-testing skill. This is the non-reference complement to
> skills/e2e-testing/SKILL.md. Read SKILL.md first for the principles, quality gate, and agent roster.
> Read this document when you need to know how to actually run the skill.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Quick Start](#quick-start) | Minimal invocation in 3-5 minutes |
| [Workflow Walkthrough](#workflow-walkthrough) | End-to-end example through all 5 agents |
| [Autonomy Tier Guidance](#autonomy-tier-guidance) | Choosing and declaring AUTONOMOUS / SUPERVISED / MANAGED-EQUIVALENT |
| [Playwright MCP Version Pin](#playwright-mcp-version-pin) | Exact pin, verification, upgrade SOP |
| [Eval Corpus Bootstrap](#eval-corpus-bootstrap) | Pre-corpus ADVISORY-ONLY mode and how to seed the corpus |
| [AGPL-3.0 Boundary Notice](#agpl-30-boundary-notice) | What you can and cannot reuse from Skyvern's published designs |
| [Agentic-Flow Gherkin Extension Syntax](#agentic-flow-gherkin-extension-syntax) | OQ-E2E-001 resolution: canonical agentic actor clause format |
| [SPA Hardening Wait-Chain](#spa-hardening-wait-chain) | OQ-E2E-002 resolution: SPA-safe execution wait strategy |
| [Contract Testing Routing](#contract-testing-routing) | OQ-E2E-003 resolution: when to route to /eng-team instead |
| [Troubleshooting](#troubleshooting) | 5 failure modes with diagnostics |
| [When NOT to Use This Skill](#when-not-to-use-this-skill) | Routing table with consequences |
| [Registration Step](#registration-step) | Human-gated C3 registration reminder |
| [References](#references) | Authoritative source files |

---

## Quick Start

**Time to first test: 3-5 minutes.**

You need: an active Jerry project (`JERRY_PROJECT` set), a git diff or user story, and the Playwright MCP server running at the pinned version (see [Playwright MCP Version Pin](#playwright-mcp-version-pin)).

**Step 1 — Provide scope.** Give the analyst (or author directly) a git diff or a user story ID:

```
/e2e-testing generate-tests
  --diff HEAD~1..HEAD
  --risk HIGH
  --mode codegen
  --autonomy SUPERVISED
```

Or in natural language: "Generate E2E tests for the changes in the last commit. Risk is HIGH. Use codegen mode with SUPERVISED autonomy."

**Step 2 — Confirm scope (P-E2E-03).** The e2e-analyst emits a `scope-document.json` listing which flows are in scope. You must confirm before authoring begins. Full-suite generation (all flows, not just diff-scoped) requires explicit confirmation at this step.

**Step 3 — Artifacts land automatically.**

| Artifact | Location | Consuming agent |
|----------|----------|-----------------|
| `scope-document.json` | `skills/e2e-testing/output/E2E-NNNN/` | e2e-author |
| `{scenario}.feature` | `skills/e2e-testing/output/E2E-NNNN/` | e2e-executor, e2e-verifier |
| `author-plan.json` | `skills/e2e-testing/output/E2E-NNNN/` | e2e-executor |
| `executor-trace.json` | `skills/e2e-testing/output/E2E-NNNN/` | e2e-verifier |
| `verifier-verdict.json` | `skills/e2e-testing/output/E2E-NNNN/` | e2e-reporter |
| `report-L0.md` | `skills/e2e-testing/output/E2E-NNNN/` | User |

**Step 4 — Read the L0 report.** The L0 report is the user-facing output: GO/NO-GO, autonomy tier, headline metrics in plain language. If the verdict is FAIL, the L0 report will include the AE-006 escalation notice and next steps.

---

## Workflow Walkthrough

This example traces E2E test run `E2E-0012` for a login flow change. The SUT is `https://app.acme.com`.

### Stage 1: e2e-analyst produces scope-document.json

The analyst receives the git diff showing `src/auth/login.ts` was modified. It produces:

```json
{
  "testrun_id": "E2E-0012",
  "changed_files": [
    {"path": "src/auth/login.ts", "classification": "business_logic", "risk_level": "HIGH"}
  ],
  "prioritised_scope": [
    {"flow": "auth-journey/login", "risk_level": "HIGH", "basis_refs": ["STORY-042", "WSTG-v42-ATHN-01"]}
  ],
  "wstg_gaps": ["SESS"]
}
```

The analyst also flags that the existing SESS coverage is absent and recommends session-expiry and logout scenarios.

### Stage 2: e2e-author produces {scenario}.feature and author-plan.json

The author receives `scope-document.json`, performs risk classification, and authors Gherkin scenarios. Mandatory self-review checklist (H-15) runs before any artifact is emitted. Output excerpt:

```gherkin
Feature: User Authentication Journey
  Background:
    Given the application is accessible at "https://app.acme.com"
    Given no active session exists

  @basis:STORY-042 @wstg:WSTG-v42-ATHN-01 @risk:HIGH @criticality:C2
  Scenario: Successful login with valid credentials
    Given a registered user with username "alice@acme.com" and a known valid password
    When the user submits login credentials
    Then the user is redirected to the dashboard
    Then the dashboard displays "Welcome, alice@acme.com"
    Then the page does not display any content attributed to "bob@acme.com"
```

The `author-plan.json` declares `autonomy_tier: SUPERVISED` and `execution_mode: codegen` at top level (P-E2E-10, P-E2E-05).

### Stage 3: e2e-executor runs the test

The executor calls `mcp__playwright__browser_navigate` to reach the SUT, then `mcp__playwright__browser_snapshot` before every locator generation step (P-E2E-06 HARD). No selector is written without a preceding snapshot. On completion, it writes `executor-trace.json` and Playwright `.spec.ts` files (codegen mode).

### Stage 4: e2e-verifier validates

The verifier runs the six-step procedure from `skills/e2e-testing/validation/validation-strategy.md`. It classifies each assertion in the feature:

| Assertion | Class | Rationale |
|-----------|-------|-----------|
| `Then the user is redirected to the dashboard` | RAN-ONLY | Navigation only; no content verified |
| `Then the dashboard displays "Welcome, alice@acme.com"` | VERIFIED | Identity-level check |
| `Then the page does not display any content attributed to "bob@acme.com"` | VERIFIED | Isolation; negative assertion |

`assertion_sensitivity_rate` = 2/3 = 0.67. This is below the 0.70 threshold, triggering a REVISE verdict. The verifier routes `failure-diagnostic.json` to e2e-author (not to e2e-executor). The author replans by adding an identity-level assertion for the navigation step.

### Stage 5: e2e-reporter assembles the report

After a PASS verdict on iteration 2, the reporter emits three levels:

- `report-L0.md`: GO. SUPERVISED. execution_recall: 0.88. element_precision: 0.79. S-014: 0.95. 2 scenarios generated; 2 passed.
- `report-L1.md`: Per-scenario pass/fail, assertion inventory, WSTG coverage matrix.
- `report-L2.md`: Coverage gap analysis, threshold trend against corpus, maintenance recommendations.

---

## Autonomy Tier Guidance

The autonomy tier is not cosmetic. It is a P-022 (no deception) mechanism -- it tells users exactly how much human oversight was involved in a test run. The tier is declared in `skills/e2e-testing/templates/e2e-governance-config.md` and surfaces as the first field in every L0 report.

### Choosing a Tier

| Tier | Choose when | Declare how |
|------|-------------|-------------|
| `AUTONOMOUS` | Test results are informational or for internal tooling; you accept that the quality gate is the only backstop; you have explicitly confirmed you understand the limitations | Set `autonomy_tier: AUTONOMOUS` in governance config. The skill requires explicit user confirmation of capability limitations at this tier. |
| `SUPERVISED` | A human will review each generated test before execution begins; recommended for any flow involving authentication, session, or business logic | Set `autonomy_tier: SUPERVISED` in governance config |
| `MANAGED-EQUIVALENT` | Human engineers backstop AI failures post-run, similar to a managed QA service model; used in enterprise or regulated contexts | Set `autonomy_tier: MANAGED-EQUIVALENT` in governance config; document the human review process in the engagement notes alongside the L0 report |

### FULLY-AUTONOMOUS-PROD Is Forbidden

There is no `FULLY-AUTONOMOUS-PROD` tier and there never will be. The guardrail is structural: the skill's quality gate (P-E2E-09) is calibrated against a single study (GenIA-E2ETest, n=12) with limited statistical power, and the eval corpus must reach 20+ scenarios before production-grade quality guarantees apply. Until both conditions are met, declaring any tier as "production-autonomous" would violate P-022 (no deception). The skill will not emit a tier label that implies production safety guarantees it cannot substantiate.

If `autonomy_tier` is absent from the governance config, all agents block invocation and emit: "BLOCKED: autonomy_tier is required in governance config. Set to AUTONOMOUS, SUPERVISED, or MANAGED-EQUIVALENT."

---

## Playwright MCP Version Pin

### Pinned Version

The skill requires `@playwright/mcp` at version **`0.0.28`**. This is the version tested during Phase 4 Step B validation. The version is pre-release (`v0.0.x`) and has observed instability across bumps.

The pin is declared in:
- `skills/e2e-testing/agents/e2e-executor.governance.yaml` (`playwright_mcp_version: "0.0.28"`)
- `skills/e2e-testing/agents/e2e-author.governance.yaml` (for governance reference during planning)
- All five agent governance YAML files propagate this pin for traceability.

### Verifying MCP Availability

Before invoking the skill, confirm the Playwright MCP server is running:

1. Check `.claude/settings.local.json` for the `@playwright/mcp` server entry.
2. Run a test snapshot call: `mcp__playwright__browser_navigate` to `https://example.com`. If the call returns a DOM snapshot, the server is live.
3. Confirm the version: `npm list @playwright/mcp` in the project root should show `0.0.28`.

### Version Drift and AD-010 Level 1 Fallback

If the Playwright MCP version drifts (e.g., auto-updated by a package manager), e2e-executor will detect the drift when tool calls return unexpected schemas. The executor emits a `version-drift-detected.json` diagnostic and falls back to AD-010 Level 1 degraded mode:

- e2e-executor cannot run browser actions.
- e2e-verifier receives `EXECUTION-UNAVAILABLE` and emits null functional-correctness metrics.
- S-014 process quality scoring against planning artifacts still proceeds.
- The L0 report emits: "DEGRADED: Playwright MCP version drift detected. Functional execution suspended. Restore pinned version to resume."
- This failure does NOT count toward the H-14 iteration limit (infrastructure failure, not test quality failure).

### Upgrade SOP

To upgrade the Playwright MCP version pin:

1. Read the `@playwright/mcp` changelog for the target version. Identify breaking changes to tool schemas (especially `browser_snapshot`, `browser_navigate`, `browser_click`).
2. Run the examples in `skills/e2e-testing/examples/` against the new version in a throwaway test run.
3. If the examples produce valid executor traces: update `playwright_mcp_version` in all five agent governance YAML files simultaneously.
4. If any example fails: diagnose the breaking change, update the affected template or agent file, then update the version pin.
5. Add a version-bump entry to the worktracker for the active project.
6. The upgrade is a C2 operation (3-10 files touched). Apply H-14 creator-critic-revision cycle.

---

## Eval Corpus Bootstrap

### Why the Corpus Matters

The skill's quality gate (P-E2E-09) requires functional-correctness metrics (execution_recall, element_precision, MMR, assertion_sensitivity_rate) to be computed against a named eval corpus. The initial-release thresholds (0.80, 0.70, 0.15) are directional reference points derived from a single study (GenIA-E2ETest, n=12). They are not empirically validated against Jerry's own test suite.

### Pre-Corpus Mode: ADVISORY-ONLY

Until the eval corpus reaches 20 scenarios, the skill operates in ADVISORY-ONLY mode. All metric outputs in `verifier-verdict.json` are flagged:

```
[UNVALIDATED -- corpus n<20; metrics are informational only, not production-grade quality guarantees]
```

This flag appears in every L0, L1, and L2 report. Users should not treat PASS verdicts as production-safe until the corpus threshold is met. This is a P-022 enforcement: the skill must not imply it has validated its own thresholds before it actually has.

### Seeding the Corpus

To seed the eval corpus and exit ADVISORY-ONLY mode:

1. Run the skill against 20 or more real project flows (not examples). Each run produces a `verifier-verdict.json` in `skills/e2e-testing/output/E2E-NNNN/`.
2. Designate a corpus directory: `skills/e2e-testing/corpus/`. Move the `verifier-verdict.json` files you want to count as corpus entries into `skills/e2e-testing/corpus/E2E-NNNN.json`.
3. Update the `CORPUS_PATH` in `skills/e2e-testing/templates/e2e-governance-config.md` to point to `skills/e2e-testing/corpus/`.
4. Once the corpus directory contains 20 or more entries, the verifier will detect this and remove the `[UNVALIDATED]` flag from subsequent runs.
5. At corpus size 50+, revisit the thresholds against the maturity targets in `skills/e2e-testing/validation/validation-strategy.md` Section 4.

The examples in `skills/e2e-testing/examples/` are calibration references, not corpus entries. Do not count them toward the 20-scenario threshold.

---

## AGPL-3.0 Boundary Notice

### What the Boundary Is

The /e2e-testing skill's architecture adopts the Planner-Executor-Verifier pattern and diff-scoped discipline derived from Skyvern's published architectural designs. Skyvern is licensed under AGPL-3.0. The AGPL-3.0 license requires that any software incorporating Skyvern source code also be released under AGPL-3.0, which is incompatible with Jerry's private repository model.

The boundary is:

| Permitted | Forbidden |
|-----------|-----------|
| Adopting the architectural pattern (Planner-Executor-Verifier triad as a concept) | Copying verbatim text or code from Skyvern source files |
| Referencing Skyvern's published design documentation | Importing Skyvern modules or functions into agent code |
| Writing new code that implements the same pattern independently | Distributing any derivative that incorporates Skyvern source code without AGPL-3.0 compliance |

### How the Guardrail Enforces This

Every agent governance YAML file contains:

```yaml
no_skyvern_source_code: true
```

This field is an output-filtering guardrail. When `no_skyvern_source_code: true` is set, any agent output that contains verbatim Skyvern source code (identified by copyright headers, file paths, or distinctive code signatures) is rejected before persistence. The agent must produce its own independent implementation.

If you are uncertain whether a code fragment crosses the boundary, treat it as forbidden and write an independent equivalent.

---

## Agentic-Flow Gherkin Extension Syntax

**OQ-E2E-001 Resolution.**

For flows where the subject under test is itself an LLM agent, standard Gherkin When/Then clauses are insufficient: they cannot express tool-call ordering, intermediate state checkpoints, or negative trajectory assertions. Jerry's /e2e-testing skill resolves this with canonical agentic-actor clauses.

### Canonical Patterns

```gherkin
# WHEN: agent invocation
When an agentic actor invoked as /skill-name processes [input description]

# THEN: positive tool-call assertion (schema must distinguish correct from incorrect call)
Then the agent called [tool_name] with schema matching {"type": "object", "required": ["field"]}

# THEN: negative tool-call assertion (must include rationale comment)
Then the agent did not call [tool_name]
# Rationale: [P-E2E-08 category or constraint motivating the prohibition]

# THEN: intermediate state checkpoint
Then at the checkpoint after [tool_name], [state predicate]

# THEN: final state assertion
Then the agent's final output contains [required content]
```

### Classification Rules

| Assertion | Class |
|-----------|-------|
| `Then the agent called web_search with schema {}` | RAN-ONLY (empty schema validates nothing) |
| `Then the agent called web_search with schema {"type": "object", "required": ["query"]}` | VERIFIED (schema distinguishes correct from incorrect call) |
| `Then the agent did not call shell_execute` | VERIFIED (negative assertion with rationale) |
| `Then at the checkpoint after web_search, at least one URL is present` | VERIFIED (testable predicate on intermediate state) |
| `Then the agent's final output contains "recommendation"` | VERIFIED (specific content check) |

See `skills/e2e-testing/examples/agentic-flow-example.feature` for a complete worked example.

---

## SPA Hardening Wait-Chain

**OQ-E2E-002 Resolution.**

Single-Page Applications (SPAs) present a unique challenge for browser automation: a navigation event completes (the URL changes) before the application has finished rendering its data. Asserting immediately after navigation produces RAN-ONLY verdicts at best and false failures at worst.

### Standard Wait Chain

For any SPA flow, e2e-executor MUST use this wait chain before asserting application state:

```
1. await page.waitForLoadState('networkidle')
   -- waits until there are no more than 0 network requests for 500ms

2. await page.waitForSelector('[data-testid=app-ready]', { timeout: 10000 })
   -- waits for the application's own readiness signal

3. Only then: snapshot and assert
```

If the SUT does not expose a `[data-testid=app-ready]` signal, request that the development team add one before generating tests for that flow. A test that asserts without this signal is asserting against an intermediate render state.

### Angular-Specific Addition

For Angular applications, add after step 1:

```
await page.waitForFunction(() => window.getAllAngularTestabilities().every(t => t.isStable()))
```

This waits for Angular's zone stability, which is separate from network idle.

### Declaring SPA Mode in Governance Config

Set `spa_mode: true` in `skills/e2e-testing/templates/e2e-governance-config.md`. When `spa_mode: true`, e2e-executor automatically applies the full wait chain before every assertion step. When `spa_mode: false` (default), the standard `waitForLoadState('load')` is used.

---

## Contract Testing Routing

**OQ-E2E-003 Resolution.**

The /e2e-testing skill covers browser-layer user journeys. It does not cover API contract testing (OpenAPI schema validation, Pact consumer-driven contracts). These are separate concerns.

**Decision rule:** If the question is "does the API return the schema the client expects?", route to `/eng-team` (eng-qa). If the question is "does the browser-based user flow produce the correct visible outcome for the user?", route to `/e2e-testing`.

| Scenario | Route |
|----------|-------|
| Validate that `/api/users/{id}` returns the schema declared in openapi.yaml | `/eng-team` (eng-qa) |
| Verify that the user profile page displays the correct name after login | `/e2e-testing` |
| Check that the shopping cart API enforces item quantity limits | `/eng-team` (eng-qa) |
| Verify that the shopping cart UI prevents adding more than the allowed quantity | `/e2e-testing` |

When a flow involves both: run `/eng-team` for the contract check first, then `/e2e-testing` for the browser layer. They are complementary, not overlapping.

---

## Troubleshooting

### Failure Mode 1: MCP Unavailable

**Symptom:** e2e-executor emits `EXECUTION-UNAVAILABLE` in `verifier-verdict.json`. All functional metrics are null.

**Diagnosis steps:**
1. Check `.claude/settings.local.json` for the `@playwright/mcp` entry. If missing, the server was never configured.
2. Run `npm list @playwright/mcp` in the project root. If the version is not `0.0.28`, the pin has drifted -- follow the upgrade SOP in reverse (downgrade to the pinned version).
3. Attempt a direct test call: invoke `mcp__playwright__browser_navigate` with `url: "https://example.com"`. If it times out, the MCP server process is not running.
4. Restart the MCP server per the Claude Code MCP configuration documentation.

**Resolution:** Restore the pinned version and restart. This does not count toward the H-14 iteration limit.

### Failure Mode 2: SUT Unreachable

**Symptom:** e2e-executor emits `sut-unreachable.json`. Executor trace is absent or incomplete.

**Diagnosis steps:**
1. Confirm the `SUT_ENTRY_URL` in the governance config is correct and the application is running.
2. If testing against a staging environment, confirm the environment is healthy and accessible from the machine running Claude Code.
3. If the SUT requires VPN or a specific network context, confirm that network context is active.

**Resolution:** Fix the SUT or the URL. This does not count toward the H-14 iteration limit.

### Failure Mode 3: Verifier Reports All-Pass But Application Is Broken

**Symptom:** `verifier-verdict.json` shows PASS, but manual inspection reveals the application is in an incorrect state (e.g., a privilege escalation bug is not caught).

**Diagnosis:** The test suite has RAN-ONLY assertions where VERIFIED assertions are required. The application is broken in a way the tests do not check.

**Diagnosis steps:**
1. Open the `assertion-inventory.json` in `skills/e2e-testing/output/E2E-NNNN/`. Look for assertions classified as RAN-ONLY at Level 1 (navigation only) for security-critical flows.
2. For any authentication or authorisation flow, confirm that Level 2 (identity) and Level 3 (isolation) assertions are present per the three-level escalation model in `skills/e2e-testing/validation/validation-strategy.md` Section 1.2.
3. If `assertion_sensitivity_rate` is above 0.70 but the failure is still not caught: the specific defect class is not represented in any assertion. Add a targeted VERIFIED assertion that would fail if the defect were present.

**Resolution:** Route the affected scenario to e2e-author for replanning. Cite the specific missing assertion depth in the replan request.

### Failure Mode 4: Generated Test Has No Assertions

**Symptom:** The Gherkin feature file has Given/When steps but no Then steps. The verifier emits FAIL immediately with `assertion_sensitivity_rate: null`.

**Diagnosis:** e2e-author failed its H-15 self-review checklist. The then-step was either dropped in a partial edit or the author template was not followed.

**Diagnosis steps:**
1. Open the `.feature` file in `skills/e2e-testing/output/E2E-NNNN/`. Count Then steps. If zero, the file is malformed.
2. Open `author-plan.json`. Check `scenario_steps` array. If scenario_steps are present but the feature file lacks Then steps, there was a write error.
3. If `scenario_steps` in the plan also lack Then entries, the author template (Step 3 in `skills/e2e-testing/templates/e2e-test-generation.md`) was not followed correctly.

**Resolution:** Escalate to e2e-author as Iteration 1 FAIL with `failure_category: runtime`. The author must add at least one VERIFIED Then assertion per scenario. Counts toward H-14 iteration limit.

### Failure Mode 5: LLM Refuses to Generate

**Symptom:** e2e-author returns a refusal or empty output when asked to generate a security scenario (e.g., WSTG-BUSL-01 authorization bypass).

**Diagnosis:** The security scenario description may have triggered safety filters. Adversarial security test scenarios (testing what happens when an attacker manipulates parameters) can look like instructions for attacking a system.

**Diagnosis steps:**
1. Confirm the scenario is testing defence (the application correctly rejects the attack), not offence (instructions for performing the attack).
2. Rephrase the scenario to emphasize the application behaviour being verified: "the server responds with 403 Forbidden" rather than "the attacker accesses the resource."
3. Add the `@basis:` tag referencing the WSTG test ID to provide clear context that this is a security test specification.

**Resolution:** Reframe the scenario description using declarative, defence-first language per P-E2E-02. The e2e-author should focus on what the application MUST do, not on what the attacker does.

---

## When NOT to Use This Skill

| Situation | Correct Route | Consequence of Misrouting |
|-----------|--------------|--------------------------|
| Unit tests, property-based tests, fuzzing | `/eng-team` (eng-qa) | Skill refuses: no browser, no scope |
| API contract testing (OpenAPI, Pact) | `/eng-team` (eng-qa) | Out of scope; browser-journey-only |
| SAST, DAST, load testing | `/eng-team` (eng-devsecops or eng-qa) | Non-goals declared in P-E2E-02; skill will not proceed |
| Security threat modeling | `/eng-team` (eng-architect) | Skill consumes threat model output; does not produce it |
| Backend security review | `/eng-team` (eng-security) | Skill produces browser-layer tests only |
| Red team / penetration testing | Contact eng-security or a dedicated red-team engagement | Skill is a test-generation tool, not a penetration tester |
| Requirements traceability (ISO 29119 test basis) | `/nasa-se` | Skill optionally produces ISO 29119-3 artifacts when `iso29119_artifacts: true` is set; but requirements definition is /nasa-se scope |
| CI/CD pipeline configuration | `/eng-team` (eng-devsecops) | Skill produces artifacts consumed by the pipeline; it does not configure the pipeline |

---

## Registration Step

The /e2e-testing skill requires three registration entries to be fully discoverable:

1. `CLAUDE.md` Quick Reference Skills table: add `/e2e-testing` row.
2. `AGENTS.md`: add all five agents with file paths and role summaries.
3. `.context/rules/mandatory-skill-usage.md` Trigger Map: add the e2e keyword set.

These registrations are a combined C3 operation per AE-002 (modifying `.context/rules/` triggers auto-C3 minimum). They require the C3 strategy set: H-14 minimum 3 iterations, S-004 pre-mortem, S-012 FMEA, S-013 inversion. They are NOT routine file writes.

**This step requires human approval.** Do not commit registration changes without explicit user sign-off. The implementation plan (`projects/PROJ-017-e2e-testing-skill/orchestration/e2e-skill-build-20260420-001/design/implementation-plan.md`) tracks this as a human-gated Phase 4 Step D action.

---

## References

| File | Content |
|------|---------|
| `skills/e2e-testing/SKILL.md` | Authoritative skill definition: 10 principles, agent roster, quality gate, constitutional compliance |
| `skills/e2e-testing/validation/validation-strategy.md` | Six-step verifier procedure, three-level escalation model, assertion taxonomy, metric formulas |
| `skills/e2e-testing/templates/e2e-test-generation.md` | e2e-author primary workflow template (conventional E2E) |
| `skills/e2e-testing/templates/e2e-agentic-flow.md` | e2e-author agentic-flow template; golden transcript generation |
| `skills/e2e-testing/templates/e2e-validation-check.md` | e2e-verifier correctness assessment template |
| `skills/e2e-testing/templates/e2e-diff-scope.md` | e2e-analyst change-impact analysis template |
| `skills/e2e-testing/templates/e2e-governance-config.md` | Per-run governance YAML block; autonomy tier and version pin declaration |
| `skills/e2e-testing/agents/e2e-analyst.md` | Change-Impact Analyst agent definition |
| `skills/e2e-testing/agents/e2e-author.md` | Test Scenario Planner and Gherkin Author agent definition |
| `skills/e2e-testing/agents/e2e-executor.md` | Browser Driver and Test Runner agent definition |
| `skills/e2e-testing/agents/e2e-verifier.md` | Correctness Validator and Escalation Supervisor agent definition |
| `skills/e2e-testing/agents/e2e-reporter.md` | Multi-Level Report Assembler agent definition |
| `skills/e2e-testing/examples/auth-journey.feature` | Conventional E2E example: authentication journey (P-E2E-02 calibration) |
| `skills/e2e-testing/examples/security-wstg-busl.feature` | WSTG BUSL business-logic abuse example (P-E2E-08 calibration) |
| `skills/e2e-testing/examples/agentic-flow-example.feature` | Agentic-flow trajectory assertion example (OQ-E2E-001 calibration) |
| `projects/PROJ-017-e2e-testing-skill/orchestration/e2e-skill-build-20260420-001/design/implementation-plan.md` | File tree, agent roster, H-25..H-30 compliance, Phase 4 build sequence |
| `projects/PROJ-017-e2e-testing-skill/orchestration/e2e-skill-build-20260420-001/synthesis/e2e-skill-requirements.md` | Full principle definitions P-E2E-01..P-E2E-10, OQ-E2E-001..OQ-E2E-007 |
