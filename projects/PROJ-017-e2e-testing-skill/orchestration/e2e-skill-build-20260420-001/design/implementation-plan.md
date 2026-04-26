---
agent: eng-lead
phase: "3A"
workflow: e2e-skill-build-20260420-001
project: PROJ-017-e2e-testing-skill
inputs:
  - projects/PROJ-017-e2e-testing-skill/orchestration/e2e-skill-build-20260420-001/synthesis/e2e-skill-requirements.md
  - projects/PROJ-017-e2e-testing-skill/orchestration/e2e-skill-build-20260420-001/synthesis/lane-standards.md
  - projects/PROJ-017-e2e-testing-skill/orchestration/e2e-skill-build-20260420-001/synthesis/lane-innovators.md
  - projects/PROJ-017-e2e-testing-skill/orchestration/e2e-skill-build-20260420-001/research/deep-engteam/eng-team-testing-baseline.md
date: 2026-04-21
version: "1.0"
gate_upstream: Gate-2 PASS (0.9485)
quality_threshold: 0.94
---

# Implementation Plan — skills/e2e-testing/

> Eng-lead output for Phase 3A. Authoritative implementation specification for Phase 3B
> (eng-architect skill architecture) and Phase 4 (build agents). Every decision cites a
> source requirement; judgment-call decisions are explicitly flagged.

## Document Sections

| Section | Purpose |
|---------|---------|
| [1. File Layout](#1-file-layout) | Complete directory tree with per-file purpose |
| [2. Agent Roster](#2-agent-roster) | File-name, role, principle ownership, integration points, tool allowlist |
| [3. Template Inventory](#3-template-inventory) | File-name, purpose, input/output structure, principle mapping |
| [4. Governance YAML Schema](#4-governance-yaml-schema) | Canonical schema with field definitions |
| [5. H-25..H-30 Compliance Checklist](#5-h-25h-30-compliance-checklist) | Hard rule commitment per rule |
| [6. Cross-Skill Integration Map](#6-cross-skill-integration-map) | Collaboration seams with other Jerry skills |
| [7. Phase 4 Build Sequence](#7-phase-4-build-sequence) | Ordered build steps with dependency rationale |
| [8. Risks and Mitigations](#8-risks-and-mitigations) | 7 implementation risks with likelihood, impact, mitigation |
| [9. Acceptance Criteria for Phase 3B Handoff](#9-acceptance-criteria-for-phase-3b-handoff) | Checklist for eng-architect |
| [Source References](#source-references) | Claim-to-source traceability |

---

## 1. File Layout

Complete canonical tree for `skills/e2e-testing/`. Every file is required unless marked OPTIONAL.

```
skills/e2e-testing/
├── SKILL.md                                  # Skill registration file (H-25, H-28, H-29, H-30)
├── PLAYBOOK.md                               # REQUIRED — see rationale below
│
├── agents/
│   ├── e2e-author.md                         # Planner agent: risk classification, Gherkin authoring
│   ├── e2e-author.governance.yaml            # Runtime governance for e2e-author
│   ├── e2e-executor.md                       # Actor agent: browser driver, DOM snapshot, test runner
│   ├── e2e-executor.governance.yaml          # Runtime governance for e2e-executor
│   ├── e2e-verifier.md                       # Validator agent: correctness gate, metrics, escalation
│   ├── e2e-verifier.governance.yaml          # Runtime governance for e2e-verifier
│   ├── e2e-analyst.md                        # OPTIONAL (adopted — see rationale): change-impact analyst
│   ├── e2e-analyst.governance.yaml           # Runtime governance for e2e-analyst
│   ├── e2e-reporter.md                       # OPTIONAL (adopted — see rationale): L0/L1/L2 assembler
│   └── e2e-reporter.governance.yaml          # Runtime governance for e2e-reporter
│
├── templates/
│   ├── e2e-test-generation.md                # e2e-author primary workflow template
│   ├── e2e-agentic-flow.md                   # Agentic-flow trajectory assertion template
│   ├── e2e-validation-check.md               # e2e-verifier correctness assessment template
│   ├── e2e-diff-scope.md                     # e2e-analyst change-impact analysis template
│   └── e2e-governance-config.md              # Per-run configuration YAML block (R-011 equivalent)
│
├── validation/
│   └── validation-strategy.md                # Operationalizes requirements §6: "ran" vs "verified", metrics, flake taxonomy
│
├── composition/
│   ├── e2e-author.agent.yaml                 # 38-field portable schema (AD-010, ADR-PROJ010-003 pattern)
│   ├── e2e-author.prompt.md                  # RCCF-assembled portable prompt body
│   ├── e2e-executor.agent.yaml               # Portable schema for executor
│   ├── e2e-executor.prompt.md                # Portable prompt body for executor
│   ├── e2e-verifier.agent.yaml               # Portable schema for verifier
│   ├── e2e-verifier.prompt.md                # Portable prompt body for verifier
│   ├── e2e-analyst.agent.yaml                # Portable schema for analyst
│   ├── e2e-analyst.prompt.md                 # Portable prompt body for analyst
│   ├── e2e-reporter.agent.yaml               # Portable schema for reporter
│   └── e2e-reporter.prompt.md                # Portable prompt body for reporter
│
├── examples/
│   ├── auth-journey.feature                  # REQUIRED — worked Gherkin example covering P-E2E-02 declarative style
│   ├── security-wstg-busl.feature            # REQUIRED — WSTG BUSL-tagged scenario example (P-E2E-08)
│   └── agentic-flow-example.feature          # REQUIRED — trajectory assertion syntax example (OQ-E2E-001 resolution)
│
└── output/
    └── .gitkeep                              # Directory placeholder; test run output lands at output/{E2E-NNNN}/
```

### PLAYBOOK.md — REQUIRED (not OPTIONAL)

Rationale (judgment call, explicitly disclosed per P-022): The requirements specification defines 7 open questions (OQ-E2E-001 through OQ-E2E-007) that require prose resolution for Phase 4 build agents to execute correctly. SKILL.md cannot contain this depth without violating H-28 (description field < 1024 chars, no XML). A PLAYBOOK.md is the appropriate place to encode: agentic-flow Gherkin extension syntax resolution (OQ-E2E-001), SPA hardening wait conditions (OQ-E2E-002), contract testing decision rule (OQ-E2E-003), phase gates PG-1..PG-7, the full six-category flake taxonomy, ISO 29119 opt-in procedure, and the dual-mode invocation contract. The eng-team baseline confirms the `engagement-playbook.md` pattern is load-bearing, not decorative (baseline §7.7). Marking this OPTIONAL would leave build agents without authoritative resolution of the open questions.

### e2e-analyst and e2e-reporter — OPTIONAL Agents Adopted

Both optional agents from requirements §4 are adopted in this plan for the following reasons:

- **e2e-analyst** (adopted): P-E2E-03 (diff-scoped entry) requires change-impact analysis as a distinct cognitive task. Requirements §4 states "without e2e-analyst, e2e-author must perform both change-impact analysis and scenario authoring — increasing the risk of shallow coverage analysis." The risk of shallow coverage is directly traceable to P-E2E-01 (risk-first ordering) — if the risk classification input is thin, downstream test ordering is wrong. Adopting e2e-analyst is a direct enforcement of P-E2E-01 + P-E2E-03 simultaneously.

- **e2e-reporter** (adopted): P-E2E-10 (autonomy-tier declaration in L0) and the L0/L1/L2 output contract (eng-team baseline §7.3) together require a distinct reporting step when multiple agents produce separate artifacts. Without e2e-reporter, the autonomy-tier declaration — a P-022 enforcement mechanism — has no dedicated owner and is at risk of being omitted or inconsistently formatted. Eng-team baseline §7.3 confirms the three-audience output contract is a non-negotiable Jerry convention.

### examples/ — REQUIRED (not OPTIONAL)

Rationale: OQ-E2E-001 (agentic-flow Gherkin extension syntax) is an open question whose answer is a design-phase artifact. The PLAYBOOK.md resolves it in prose; the `examples/agentic-flow-example.feature` file instantiates the resolution in a concrete, lintable artifact that build agents can validate against. Without at least one worked example per syntax innovation, the linting rule (P-E2E-02 testable assertion) cannot be validated during Phase 4. The `auth-journey.feature` example also provides the Phase 4 build agents with a reference for correct declarative style and `@basis:` tag format before they author any test-generation template.

---

## 2. Agent Roster

### e2e-author

**File:** `agents/e2e-author.md`

**Identity:** Test Scenario Planner and Gherkin Author — the Planner role in the Planner–Executor–Verifier triad, responsible for risk classification, declarative scenario authoring, and replanning on escalation.

**Primary Principle Ownership:** P-E2E-01 (risk classification before any scenario step), P-E2E-02 (declarative Gherkin with `@basis:` tag), P-E2E-03 (diff-scoped entry — rejects full-suite runs without explicit confirmation), P-E2E-08 (WSTG six-category security scenario generation), P-E2E-10 (autonomy-tier declaration declared at plan creation).

**Integration Points:**
- Receives diff-scope document from `e2e-analyst` (primary input path) or raw `git diff` when analyst is absent
- Receives structured failure diagnostic from `e2e-verifier` on escalation; MUST produce a revised plan, not re-submit unchanged
- Feeds `e2e-executor` with JSON scenario plan or `.spec.ts` scaffold
- Feeds `e2e-reporter` with test plan and authoring rationale
- Feeds `ps-investigator` (upstream consultation) when a failure hypothesis requires research before replanning
- Hands off to eng-reviewer at engagement close with Gherkin artifacts as evidence package

**Needs Web/Browser MCP Tools:** NO. e2e-author is a planning and authoring agent only; it reads diffs and produces structured documents. It does not interact with a live browser.

**Tool Allowlist:**
```
file_read, file_write, file_edit, file_search_glob, file_search_content, web_search
```
Web search is permitted for e2e-author because it may need to look up WSTG test case IDs (P-E2E-08) and Gherkin syntax references. Context7 is not included in the default allowlist because no external library SDK lookup is required at planning time; this is a judgment call that eng-architect may revise if the author template requires framework-specific API references.

**Forbidden Tools:** `agent_delegate` (P-003), `shell_execute` (no browser invocation from planner)

---

### e2e-executor

**File:** `agents/e2e-executor.md`

**Identity:** Browser Driver and Test Runner — the Actor role in the Planner–Executor–Verifier triad, responsible for DOM snapshot acquisition, locator generation against live DOM, and test execution in codegen or explorer mode.

**Primary Principle Ownership:** P-E2E-05 (declares execution mode, enforces codegen/explorer distinction), P-E2E-06 (live-DOM-grounded locator generation — browser_snapshot MUST precede any locator step), P-E2E-07 (gTAA Adaptation layer — exclusive integration point with the browser driver).

**Integration Points:**
- Receives JSON scenario plan or `.spec.ts` file from `e2e-author`
- Returns execution trace (JSON), pass/fail per step, WebDriver error codes, and screenshots to `e2e-verifier`
- In explorer mode: registers assertion tools via Browser-Use action-extension pattern
- In codegen mode: produces committed `.spec.ts` artifact that runs in CI without LLM in the loop (P-E2E-05)
- Hands execution trace to `e2e-reporter` for report assembly

**Needs Web/Browser MCP Tools:** YES — this is the only agent that requires Playwright MCP tools. The Playwright MCP server (`@playwright/mcp`) must be registered in the agent's MCP server configuration with an explicitly pinned version (version instability at v0.0.x per innovators baseline, inn-2).

**Tool Allowlist (Playwright MCP core-8):**
```
mcp__playwright__browser_snapshot
mcp__playwright__browser_click
mcp__playwright__browser_type
mcp__playwright__browser_navigate
mcp__playwright__browser_verify_element_visible
mcp__playwright__browser_take_screenshot
mcp__playwright__browser_wait_for
mcp__playwright__browser_evaluate
file_write, file_read, file_edit
```
Browser-Use tools are included only in explorer-mode configuration; they are not part of the default tool surface. Exposing no more than 10 primary tools in the default surface is the explicit constraint from innovators baseline (inn-2 §7.1), which the above list satisfies at exactly 10 (8 Playwright MCP + 2 file operations, with `browser_wait_for` and `browser_evaluate` replacing the 2 remaining slots).

**Forbidden Tools:** `agent_delegate` (P-003), `web_search` (executor interacts with the SUT only, not the open web)

---

### e2e-verifier

**File:** `agents/e2e-verifier.md`

**Identity:** Correctness Validator and Escalation Supervisor — the Validator role in the Planner–Executor–Verifier triad, responsible for the "ran vs verified" distinction, metric computation, and structured escalation to e2e-author on failure.

**Primary Principle Ownership:** P-E2E-04 (supervisor-loop escalation — escalates to e2e-author, NEVER to e2e-executor), P-E2E-09 (published quality gate — computes execution_recall, element_precision, MMR against thresholds and persists results).

**Integration Points:**
- Receives execution trace from `e2e-executor` and original scenario plan from `e2e-author`
- Escalates structured failure diagnostic to `e2e-author` on FAIL (never to `e2e-executor`)
- Invokes `/adversary` (adv-scorer) for C2+ deliverables per H-17 to compute S-014 process quality score
- Reports PASS verdict and both quality scores (S-014 + functional correctness) to `e2e-reporter`
- At engagement close, feeds quality evidence package to eng-reviewer for engagement-level scoring (0.95 gate per seam 2 of requirements §9)

**Needs Web/Browser MCP Tools:** NO. e2e-verifier operates on traces and artifacts already produced by e2e-executor; it does not interact with a live browser.

**Tool Allowlist:**
```
file_read, file_write, file_edit, file_search_glob, file_search_content
```
No web search or MCP browser tools. The verifier's work is entirely artifact-analysis and metric computation.

**Forbidden Tools:** `agent_delegate` (P-003), `shell_execute`, all Playwright MCP tools (P-E2E-07: only the Adaptation layer touches the driver)

---

### e2e-analyst

**File:** `agents/e2e-analyst.md`

**Identity:** Change-Impact Analyst and Coverage Gap Identifier — the optional pre-authoring agent that maps git diffs to affected user flows and produces the prioritised scope document consumed by e2e-author.

**Primary Principle Ownership:** P-E2E-01 (risk classification through change-proximity analysis), P-E2E-03 (diff-scoped entry — performs the flow-adjacency mapping that makes diff-scoping precise rather than heuristic), P-E2E-09 (corpus maintenance — updates the named eval corpus with each test run).

**Integration Points:**
- Receives `git diff` output and existing `.feature` file inventory
- Produces prioritised scope document (JSON) consumed by `e2e-author`
- Updates the named eval corpus for quality gate computation
- Informs eng-reviewer about coverage delta at engagement close

**Needs Web/Browser MCP Tools:** NO.

**Tool Allowlist:**
```
file_read, file_write, file_edit, file_search_glob, file_search_content, shell_execute
```
`shell_execute` is permitted for e2e-analyst because call-graph analysis of the changed code (to map files to user flows) may require running a static analysis command (e.g., `npx madge` for JS dependency graphs). This is the only non-browser agent that has shell access; the permission is scoped to read-only analysis commands.

**Forbidden Tools:** `agent_delegate` (P-003), all Playwright MCP tools

---

### e2e-reporter

**File:** `agents/e2e-reporter.md`

**Identity:** Multi-Level Report Assembler — the optional aggregation agent that assembles L0/L1/L2 structured reports from all agent artifacts, with the autonomy-tier declaration (P-E2E-10) as its first-class L0 field.

**Primary Principle Ownership:** P-E2E-10 (autonomy-tier declaration in L0 — the reporter is the enforcement point that ensures no test run is surfaced to the user without an explicit autonomy-tier field and one-sentence explanation).

**Integration Points:**
- Consumes outputs from all other agents (test plan, execution trace, quality metrics, WSTG coverage report)
- Feeds eng-reviewer with the structured evidence package for engagement-level scoring
- Does not produce new test artifacts; only assembles existing artifacts into the L0/L1/L2 output format

**Needs Web/Browser MCP Tools:** NO.

**Tool Allowlist:**
```
file_read, file_write, file_edit, file_search_glob
```

**Forbidden Tools:** `agent_delegate` (P-003), `shell_execute`, all Playwright MCP tools, `web_search`

---

## 3. Template Inventory

### `templates/e2e-test-generation.md`

**Purpose:** Parameterises the e2e-author agent's primary workflow — from a risk-classified scenario scope to a complete Gherkin `.feature` file with `@basis:` tags.

**Input Parameters:**
- `scope_document` — JSON from e2e-analyst, or raw `git diff` text when analyst absent
- `risk_level` — HIGH | MEDIUM | LOW (required before any authoring step per P-E2E-01)
- `criticality` — C1 | C2 | C3 | C4 (required per P-E2E-01)
- `test_basis_refs` — array of story IDs, WSTG IDs, or risk item references (P-E2E-02)
- `sut_url` — system under test URL or description
- `execution_mode` — codegen | explorer (P-E2E-05)
- `autonomy_tier` — AUTONOMOUS | SUPERVISED | MANAGED-EQUIVALENT (P-E2E-10)
- `iso29119_artifacts` — boolean (default false, RT-001 resolution)

**Output Structure:**
1. Risk classification block (risk_level, criticality, justification)
2. Feature decomposition (Feature → Rule → Scenario outline, before any Gherkin steps)
3. Gherkin `.feature` file with `@basis:` tags, `@risk:` tags, `@wstg:` tags where applicable
4. WSTG security scenarios for applicable mandatory categories (P-E2E-08)
5. Self-review checklist (H-15): risk_level set, @basis populated, no UI verbs in When steps, WSTG tags present for security flows
6. Persistence confirmation per P-002: file path where artifact is written

**Principles Operationalised:** P-E2E-01, P-E2E-02, P-E2E-08, P-E2E-10 (autonomy-tier declaration in output header)

**Example Invocation Stub:**
```
/e2e-testing generate-tests
  --diff path/to/git.diff
  --risk HIGH
  --criticality C2
  --basis STORY-042,WSTG-v42-ATHN-01
  --mode codegen
  --autonomy SUPERVISED
```

---

### `templates/e2e-agentic-flow.md`

**Purpose:** Parameterises authoring and execution of agentic-flow tests — scenarios where the subject under test is itself an LLM agent, requiring trajectory assertions (tool-call ordering, intermediate state checkpoints, constraint compliance) rather than single-state assertions.

**Input Parameters:**
- `agent_description` — what the agent under test should accomplish
- `skill_name` — Jerry skill name or agent ID being tested (e.g., `/problem-solving`)
- `expected_tool_calls` — ordered list of expected tool invocations with JSON schema
- `intermediate_checkpoints` — array of state assertions between tool calls
- `divergence_tolerance` — acceptable variation in path (e.g., "tool order may vary within Phase 1")
- `final_state_assertion` — what the agent's output must contain to pass
- `execution_mode` — codegen (golden transcript) | explorer (live run)

**Output Structure:**
1. Role framing: e2e-author in agentic-flow mode
2. Trajectory decomposition: expected tool-call sequence with intermediate state predicates
3. Non-determinism budget: explicit tolerance specification (what counts as a passing trajectory even if path varies)
4. Gherkin extension syntax for agentic actors: `When an agentic actor invoked as [skill-name] processes [input]` followed by trajectory assertions using `Then the agent called [tool] with schema matching [JSON-schema]` and `Then the agent did not call [tool]` for negative assertions (OQ-E2E-001 resolution)
5. Golden-transcript generation in codegen mode: reference JSON trace for replay-based regression
6. Tool-call schema validation assertions
7. Persistence confirmation per P-002

**Principles Operationalised:** P-E2E-04 (Verifier receives trajectory, not just final state), P-E2E-05 (codegen mode produces golden transcript; explorer keeps LLM in loop), P-E2E-06 (DOM snapshot before any locator step in UI-adjacent agentic flows)

**Example Invocation Stub:**
```
/e2e-testing agentic-flow
  --agent /problem-solving
  --description "Researcher analyzes a codebase for security vulnerabilities"
  --expected-tools web_search,file_read,file_search_content
  --mode codegen
```

---

### `templates/e2e-validation-check.md`

**Purpose:** Parameterises the e2e-verifier agent's correctness assessment procedure — the structured determination of whether a test verified application correctness (not just that it ran without error).

**Input Parameters:**
- `execution_trace` — JSON trace from e2e-executor
- `scenario_plan` — original Gherkin scenario and expected outcomes per step
- `webdriver_errors` — array of WebDriver error codes observed
- `element_precision_raw` — C (correct locators) and G (generated locators) counts
- `execution_recall_raw` — CS (steps that ran without error) and ES (expected steps) counts
- `manual_modifications` — count of generated steps requiring human edit before pass

**Output Structure:**
1. Assertion inventory: each `Then` step classified as VERIFIED | RAN-ONLY | ABSENT
2. Sensitivity check results: per-assertion sensitivity rationale
3. Coverage dimension check: which of the 5 dimensions (happy/failure/boundary/security/agentic) are present
4. Metric computation: element_precision (C/G), element_recall (C/E), execution_precision (CS/GS), execution_recall (CS/ES), MMR
5. Failure classification: one of six flake categories (selector/timing/runtime/data/visual/interaction) per QA Wolf taxonomy
6. Verdict: PASS | REVISE | FAIL with threshold comparison
7. Escalation payload to e2e-author on FAIL: failure type, WebDriver error class, DOM snapshot at failure point, replanning recommendation
8. S-014 self-score of the test artifact (H-15, H-17): process quality score separate from functional correctness score
9. Persistence confirmation per P-002: both score artifacts written to output directory

**Principles Operationalised:** P-E2E-04 (escalate to e2e-author, never to e2e-executor), P-E2E-09 (GenIA-E2ETest metric formulas computed and persisted)

**Example Invocation Stub:**
```
/e2e-testing validate
  --trace output/E2E-0001/executor-trace.json
  --plan output/E2E-0001/author-plan.json
  --scenario auth-journey
```

---

### `templates/e2e-diff-scope.md`

**Purpose:** Parameterises the e2e-analyst agent (or e2e-author when analyst is absent) to perform change-impact analysis on a `git diff` and produce a prioritised test-scope document.

**Input Parameters:**
- `git_diff` — raw diff text or path to diff file
- `feature_inventory` — glob result of existing `.feature` files
- `wstg_coverage_report` — JSON summary of current WSTG category coverage (may be empty on first run)
- `call_graph` — optional path to dependency map (JSON/dot format)

**Output Structure:**
1. Changed-file classification: each changed file categorised as UI component | API handler | business logic | infrastructure | test
2. Flow adjacency mapping: for each changed file, which Gherkin Features/Rules are adjacent
3. Coverage gap identification: flows not covered by existing `.feature` inventory
4. WSTG gap check: which of the six mandatory categories lack scenarios in existing suite
5. Prioritised scope document (JSON): flows ordered by risk_level × change_proximity
6. Confirmation prompt if `--full-suite` flag absent: display scope and wait for user confirmation (P-E2E-03 HARD requirement)
7. Persistence confirmation per P-002

**Principles Operationalised:** P-E2E-01 (risk × proximity ordering), P-E2E-03 (confirmation gate before any full-suite run)

**Example Invocation Stub:**
```
/e2e-testing scope
  --diff HEAD~1..HEAD
  --features skills/e2e-testing/output/E2E-0001/
  --wstg-report output/E2E-0001/wstg-coverage.json
```

---

### `templates/e2e-governance-config.md`

**Purpose:** Provides the R-011-equivalent per-run configuration YAML block allowing per-engagement parameter overrides. This is the canonical configuration interface for the skill (P-E2E-05 mode, P-E2E-08 WSTG categories, P-E2E-10 autonomy tier, RT-001 ISO opt-in, RT-004 threshold).

**Input Parameters:** User-provided overrides or defaults at invocation time.

**Output Structure:** A fully-populated `e2e_governance` YAML block (see schema in requirements §5) persisted to `output/{E2E-NNNN}/governance-config.yaml` for audit traceability.

**Principles Operationalised:** P-E2E-05, P-E2E-08, P-E2E-10, RT-001, RT-004

**Default governance block (definitive for Phase 4):**
```yaml
e2e_governance:
  version: "1.0"
  browsers: [chromium, firefox]
  viewports: [{width: 1280, height: 720}]
  execution_mode: codegen
  retry_count: 0
  screenshot_on_failure: true
  trace_on_failure: true
  visual_diff_threshold: 0.02
  journey_timeout_seconds: 30
  quality_threshold: 0.94
  iso29119_artifacts: false
  wstg_mandatory_categories: [ATHN, ATHZ, SESS, INPV, BUSL, APIT]
  autonomy_tier: AUTONOMOUS
  testrun_id_format: "^E2E-\\d{4}$"
  playwright_mcp_version: "pinned — see SKILL.md frontmatter"
  spa_wait_strategy: networkidle
```

---

## 4. Governance YAML Schema

Modelled on `eng-team/agents/eng-qa.governance.yaml` (eng-team baseline §5) with e2e-testing-specific field overrides. This schema is authoritative for all five agent governance YAML files.

```yaml
# skills/e2e-testing/agents/{agent-name}.governance.yaml
# Validated against: docs/schemas/agent-governance-v1.schema.json
version: 1.0.0
tool_tier: T3                                 # T3 = full tool access for executor; T2 = file-only for others
identity:
  role: <string>                              # One-sentence role description matching agent identity section
  expertise:
    - E2E Test Design (gTAA-conformant)
    - Gherkin / BDD Scenario Authoring
    - OWASP WSTG v4.2 Security Test Coverage
    - Playwright MCP Browser Automation        # executor-only; remove for other agents
    - GenIA-E2ETest Metric Computation         # verifier-only
    - Risk-Based Test Prioritisation (ISO 29119-2 / ISTQB CTFL)
  cognitive_mode: systematic                  # systematic for author/verifier; convergent for executor

persona:
  tone: professional
  communication_style: evidence-based
  audience_level: adaptive

guardrails:
  input_validation:
    - testrun_id_format: "^E2E-\\d{4}$"       # Replaces ^ENG-\d{4}$ from eng-team pattern
    - execution_mode_declared: required        # P-E2E-05: mode must be declared before execution
    - autonomy_tier_declared: required         # P-E2E-10: tier must be declared before any run
    - risk_level_declared: required            # P-E2E-01: risk classification before authoring
  output_filtering:
    - no_secrets_in_output
    - all_claims_must_have_citations
    - no_executable_code_without_confirmation
    - no_skyvern_source_code                  # AGPL-3.0 boundary enforcement; pattern reuse only
    - wstg_tags_required_on_security_scenarios # P-E2E-08
  fallback_behavior: warn_and_retry

quality:
  threshold: 0.94                            # RT-004: triangulated between SSOT 0.92 floor and eng-team 0.95
  metrics:
    execution_recall_min: 0.80               # P-E2E-09 initial release threshold
    element_precision_min: 0.70              # P-E2E-09 initial release threshold
    manual_modification_rate_max: 0.15       # P-E2E-09 initial release threshold
  scores_orthogonal: true                    # S-014 process quality and functional correctness are separate

criticality_default: C2                      # Judgment call: user-facing browser tests warrant C2 minimum

output:
  required: true
  location: "skills/e2e-testing/output/{testrun-id}/{agent}-{topic-slug}.md"
  levels: [L0, L1, L2]
  autonomy_tier_in_l0: required              # P-E2E-10 enforcement

constitution:
  reference: docs/governance/JERRY_CONSTITUTION.md
  principles_applied:
    - 'P-003: No Recursive Subagents (Hard)'
    - 'P-020: User Authority (Hard)'
    - 'P-022: No Deception (Hard) — autonomy-tier declaration is P-022 enforcement'

validation:
  file_must_exist: true
  link_artifact_required: true
  post_completion_checks:
    - verify_file_created
    - verify_artifact_linked
    - verify_l0_l1_l2_present
    - verify_citations_present
    - verify_testrun_id_format_matches
    - verify_wstg_six_categories_covered      # P-E2E-08 completeness check
    - verify_both_quality_scores_present      # Section 6.5 orthogonality enforcement

capabilities:
  allowed_tools:                             # Per-agent allowlists defined in Section 2 above
    - file_read
    - file_write
    - file_edit
    - file_search_glob
    - file_search_content
    # executor additionally: mcp__playwright__* (8 tools)
    # analyst additionally: shell_execute
    # author additionally: web_search
  forbidden_tools:
    - agent_delegate                         # P-003 hard enforcement
    # executor additionally: web_search
    # verifier/reporter additionally: shell_execute, all playwright MCP tools

phase_gates:                                 # Adapted from eng-team PG-N pattern (baseline §7.7)
  PG-1: diff_scope_approved                  # Scope document confirmed by user
  PG-2: fixtures_and_snapshots_ready         # DOM snapshots captured, test data fixtures confirmed
  PG-3: smoke_pass_codegen_mode              # At least one scenario passes in codegen mode
  PG-4: full_run_green                       # All scoped scenarios pass
  PG-5: wstg_six_categories_covered          # All six mandatory WSTG categories have at least one scenario
  PG-6: quality_metrics_meet_thresholds      # execution_recall >= 0.80, element_precision >= 0.70, MMR <= 0.15
  PG-7: e2e_quality_gate_at_094              # S-014 process score >= 0.94; eligible for eng-reviewer if requested

mcp_servers:
  playwright:                               # executor only
    package: "@playwright/mcp"
    version: pinned                         # version instability at v0.0.x requires explicit pin (innovators baseline inn-2)
    max_tools_exposed: 10                   # inn-2 §7.1 constraint
```

### Field Notes for eng-architect

- `tool_tier: T3` applies only to `e2e-executor`. All other agents are `T2` (file-only + web_search for author/analyst).
- `criticality_default: C2` is a judgment call (P-022 disclosure). User-facing browser tests are reversible within one day if a generated scenario is wrong, which is C2 by the Jerry criticality table. A specific engagement may override via `e2e-governance-config.md`.
- The `phase_gates` block is advisory metadata in the governance YAML; the authoritative gate definitions with Pass Criteria and Fail Actions live in `PLAYBOOK.md`.

---

## 5. H-25..H-30 Compliance Checklist

### H-25: SKILL.md file name — exact casing

**Commitment:** The file `skills/e2e-testing/SKILL.md` will be created with exactly that capitalisation. No `skill.md`, `Skill.md`, or `README.md` variant exists in the tree. This is a build-time verification requirement for Phase 4 Step A.

### H-26: Folder name kebab-case matches name frontmatter field

**Commitment:** The folder is `skills/e2e-testing/` (kebab-case). The SKILL.md frontmatter `name` field will be exactly `e2e-testing`. These two values must match character-for-character. Phase 4 Step A verifies this before writing any other file.

### H-27: No README.md inside skill folder

**Commitment:** No `README.md` file appears anywhere in `skills/e2e-testing/`. The roles of a README are distributed as follows:
- `SKILL.md` — skill registration, invocation, agent roster summary, tool declaration (H-29)
- `PLAYBOOK.md` — operational depth: phase gates, open question resolutions, dual-mode invocation contract, flake taxonomy, ISO 29119 opt-in procedure
- `validation/validation-strategy.md` — validation methodology depth
- `examples/*.feature` — worked examples for syntax and linting reference

### H-28: SKILL.md description field — candidate text

The description field must satisfy: WHAT + WHEN + trigger keywords, under 1024 characters, no XML.

**Draft candidate text (character count: ~820 — within limit):**

```
Provides LLM-orchestrated end-to-end testing for web applications and agentic flows.
Generates, executes, and verifies browser-driven user-journey tests using a
Planner-Executor-Verifier agent triad. Defaults to diff-scoped test generation (one
`git diff` in, test scenarios out); full-suite generation requires explicit opt-in.
Supports two execution modes: codegen (committed Playwright .spec.ts files that run
in CI without LLM in the loop) and explorer (LLM stays in loop for self-healing and
exploratory runs). Every generated scenario includes a @basis: traceability tag and
risk classification. Security scenarios are tagged with WSTG v4.2 category IDs.
Quality gate: execution_recall >= 0.80, element_precision >= 0.70, MMR <= 0.15,
S-014 process score >= 0.94.

Trigger keywords: e2e test, end-to-end test, browser test, user journey, playwright,
generate test, test this flow, agentic flow test, WSTG coverage, diff scope test,
regression test, smoke test, codegen test, explorer mode, visual regression.

Non-goals: unit testing, API contract testing, SAST, DAST, fuzzing, load testing.
```

### H-29: Full repo-relative paths in SKILL.md

**Commitment:** All agent file references, template paths, and example paths in SKILL.md will use full repo-relative paths from the repository root. No paths beginning with `./` or `../`. No bare filenames without directory prefix.

Specifically, every agent reference in SKILL.md will use the form:
`skills/e2e-testing/agents/e2e-author.md` (not `agents/e2e-author.md`).

### H-30: Registration plan

**Registration targets (all three required):**

1. **CLAUDE.md** — Add `/e2e-testing` to the Skills quick-reference table with purpose "E2E browser test generation, execution, and verification for user journeys and agentic flows". This touches `.context/rules/` via the rules symlink; AE-002 applies: auto-C3 minimum for this change. The CLAUDE.md registration commit must be treated as C3 per AE-002.

2. **AGENTS.md** — Add all five agents (e2e-author, e2e-executor, e2e-verifier, e2e-analyst, e2e-reporter) to the agent registry with file paths and role summaries.

3. **mandatory-skill-usage.md** — Add `/e2e-testing` to the Trigger Map with keywords: `e2e test, browser test, user journey, playwright, generate test, agentic flow test, WSTG, end-to-end`. This file is in `.context/rules/` — AE-002 applies, auto-C3 minimum. The registration changes to this file and CLAUDE.md must both be treated as C3 (C3 requires: H-14 minimum 3 revision cycles, S-004 pre-mortem, S-012 FMEA, S-013 inversion in addition to C2 strategies). A combined registration PR for both files will carry the C3 quality gate.

**AE-002 Escalation Note:** Both CLAUDE.md and mandatory-skill-usage.md live under paths resolved to `.context/rules/` (CLAUDE.md references the rules directory; mandatory-skill-usage.md is directly in `.context/rules/`). Any modification to `.context/rules/` triggers auto-C3 minimum per AE-002. The Phase 4 build sequence must include a dedicated C3-grade registration step — this is not a cosmetic change.

---

## 6. Cross-Skill Integration Map

### /eng-team (three seams from requirements §9)

**Seam 1 — Security Scope (eng-qa):**
- e2e-testing generates WSTG-tagged user-journey security scenarios (`@wstg:WSTG-v42-<CAT>-<NN>`)
- eng-qa generates threat-model-derived unit and API-level tests (`@owasp-tg:` tags)
- Routing rule: if a security scenario requires browser automation and involves a user journey (login, session, business logic abuse), route to /e2e-testing. If it requires input validation fuzzing, property-based invariants, or SSDF PW.8 coverage, route to eng-qa.
- Coordination mechanism: the `@wstg:` vs `@owasp-tg:` tag scheme makes attribution explicit and auditable.

**Seam 2 — Quality Scoring (eng-reviewer):**
- e2e-verifier owns the skill-internal quality gate (0.94 S-014 process score + GenIA-E2ETest functional correctness thresholds)
- eng-reviewer owns the engagement-level quality gate (0.95 for security-focused engagements)
- Sequential dependency: /e2e-testing artifacts MUST pass the 0.94 internal gate before being submitted to eng-reviewer. A deliverable scoring below 0.94 internally is not eligible for eng-reviewer scoring.
- The two gates are not competing; they are sequential quality layers.

**Seam 3 — CI/CD Wiring (eng-devsecops):**
- /e2e-testing produces WSTG-tagged test artifacts, quality metric reports, and per-category WSTG coverage reports
- eng-devsecops owns the CI/CD gate configuration that determines whether those artifacts gate a deployment
- The `e2e-governance-config.md` quality thresholds are the contract; eng-devsecops wires them into the pipeline gate
- /e2e-testing does not re-implement SAST/DAST gates (those remain with eng-devsecops)

### /problem-solving (ps-critic in creator-critic loops)

- H-14 requires a creator-critic-revision cycle with minimum 3 iterations for C2+ deliverables
- The creator-critic loop for e2e-testing deliverables pairs e2e-author (creator) with ps-critic (external critic)
- The e2e-verifier internally performs self-review (H-15) and S-014 scoring (H-17), but this is not a substitute for a ps-critic cycle on C2+ deliverables; it is the self-review step before the cycle begins
- ps-investigator is an upstream consultant for e2e-author when a failure hypothesis requires research (e.g., "why does this application always fail the auth flow?" before authoring a new scenario)

### /adversary (adv-scorer at quality gate)

- e2e-verifier invokes adv-scorer for C2+ deliverables per H-17
- The adv-scorer computes the S-014 six-dimension process quality score against the 0.94 threshold
- This is a skill-internal gate, not an engagement-level gate (engagement-level remains eng-reviewer at 0.95)
- Escalation from /adversary follows the eng-team three-failure ladder pattern: 1st failure → revise + resubmit to e2e-author; 2nd failure → escalate to eng-lead; 3rd failure → escalate to eng-architect; persistent failure → user notification per P-020

### /nasa-se (optional — requirements traceability)

- Integration is OPTIONAL but available when E2E test specs need formal requirements traceability in regulated contexts
- When `iso29119_artifacts: true` is set in governance config (RT-001 ISO opt-in), /nasa-se can be consulted to produce ISO 29119-3-compliant test case specifications alongside the Gherkin scenarios
- No hard dependency; the skill functions fully without /nasa-se

### /red-team (optional — security scenario overlap)

- /red-team produces threat intel that feeds eng-architect's threat model (eng-team baseline §7.4)
- If /red-team identifies a user-journey-level attack scenario (e.g., "attacker can abuse the purchase flow to obtain goods without payment"), this is a direct input to e2e-author's WSTG-BUSL scenario generation
- Routing: /red-team → (threat intel) → e2e-author → WSTG-tagged BUSL scenario → e2e-executor
- No hard dependency; the skill functions without /red-team. Security scenarios default to WSTG taxonomy without red-team input.

---

## 7. Phase 4 Build Sequence

### Step A — eng-lead: SKILL.md + PLAYBOOK.md

**Build:** Create `skills/e2e-testing/SKILL.md` and `skills/e2e-testing/PLAYBOOK.md`.

**Why first:** SKILL.md establishes the frontmatter `name: e2e-testing` field (H-26 verification gate), declares the Playwright MCP server version to be pinned (this version propagates to all agent governance YAML files), and registers the tool allowlist surface. PLAYBOOK.md resolves the seven open questions (OQ-E2E-001 through OQ-E2E-007) including the agentic-flow Gherkin extension syntax (OQ-E2E-001) — build agents authoring templates in Step B cannot produce the `e2e-agentic-flow.md` template without the OQ-E2E-001 syntax resolution.

**Dependency output consumed by Step B:** Playwright MCP version pin, agentic-flow Gherkin syntax spec, phase gate definitions PG-1..PG-7, SPA hardening wait strategy decision (OQ-E2E-002), ISO 29119 opt-in depth statement (OQ-E2E-006).

### Step B — eng-qa: templates/ + validation/ + examples/

**Build:** Create all five templates under `templates/`, create `validation/validation-strategy.md`, and create the three example `.feature` files under `examples/`.

**Why second:** Templates operationalise the principles from SKILL.md. They cannot be written before the agentic-flow syntax (OQ-E2E-001) is resolved (SKILL.md Step A dependency). The validation strategy instantiates Section 6 of the requirements spec — it is the operative reference that agent definitions in Step C cite in their Methodology sections.

**Dependency output consumed by Step C:** Template input/output contracts (agent definitions must reference specific template files), validation strategy procedure (e2e-verifier's Methodology section cites `validation/validation-strategy.md`), example Gherkin files (agent definitions cite them as worked examples in their identity sections).

### Step C — eng-architect: agents/ + composition/

**Build:** Create all ten agent `.md` files, all five `.governance.yaml` files, all ten composition files (`.agent.yaml` + `.prompt.md`).

**Why third:** Agent definitions are the highest-complexity artifacts. They reference SKILL.md (tool allowlists, mode declarations), templates (citing specific template files in their Methodology sections), and validation strategy (e2e-verifier cites the six-step procedure). Agent tool allowlists must match the governance YAML allowlists — this consistency check requires both artifacts to be written in the same step.

**Critical ordering constraint within Step C:** The e2e-executor's Playwright MCP tool list (from SKILL.md Step A, confirmed in Section 2 of this plan) must be declared in `e2e-executor.governance.yaml` before `e2e-executor.md` is authored, not after, to ensure the agent's "Tool Integration" section accurately describes its allowlist. In practice, write governance YAML files before agent MD files within Step C.

### Registration Step — Human-gated C3 commit

**Build:** Register in CLAUDE.md, AGENTS.md, mandatory-skill-usage.md.

**Why last and human-gated:** AE-002 (auto-C3 for `.context/rules/` touches) applies to CLAUDE.md and mandatory-skill-usage.md. These registrations require the C3 quality strategy set (H-14 minimum 3 iterations, S-004 pre-mortem, S-012 FMEA, S-013 inversion). This is not a mechanical file-write step; it requires adversarial review. It must occur after the skill is complete and verifiable, not during the build.

### Summary Build Order

| Step | Owner | Artifacts | Dependency Input |
|------|-------|-----------|-----------------|
| A | eng-lead | SKILL.md, PLAYBOOK.md | This implementation plan |
| B | eng-qa | templates/ (5 files), validation/ (1 file), examples/ (3 files) | SKILL.md (MCP version, OQ resolutions) |
| C | eng-architect | agents/ (10 files), composition/ (10 files) | SKILL.md, templates/, validation/ |
| D | human-gated | CLAUDE.md, AGENTS.md, mandatory-skill-usage.md | Complete skill (all of A, B, C) |

---

## 8. Risks and Mitigations

### Risk 1: Playwright MCP Version Instability

**Description:** `@playwright/mcp` is at `v0.0.70` (innovators baseline, inn-2). The `v0.0.x` version range signals active pre-release development. Tool names, parameter schemas, and return formats may change between patch versions. If e2e-executor's tool allowlist is hardcoded to tool names from a specific version and the version is updated, the agent will fail without a clear error.

**Likelihood:** HIGH — observed across multiple v0.0.x version bumps in the 12-month research window.

**Impact:** HIGH — e2e-executor is the only browser-interaction agent; Playwright MCP instability disables the skill's core execution capability.

**Mitigation:**
1. Pin `@playwright/mcp` version in SKILL.md frontmatter (exact version, not `latest` or caret range).
2. Document the pin alongside an upgrade SOP in PLAYBOOK.md: "To upgrade, run `npx @playwright/mcp@{new-version}` against `examples/auth-journey.feature` as a smoke test before updating the pin."
3. Constrain e2e-executor's tool allowlist to the stable core-8 (browser_snapshot, browser_click, browser_type, browser_navigate, browser_verify_element_visible, browser_take_screenshot, browser_wait_for, browser_evaluate) and treat any new tools as opt-in additions, not default-surface additions.

### Risk 2: AGPL-3.0 Boundary Drift (Skyvern)

**Description:** The requirements spec adopts Skyvern's architectural patterns (Planner→Actor→Validator, diff-scoped discipline, eval transparency) but explicitly excludes Skyvern source code under AGPL-3.0 (requirements §8). If Phase 4 build agents produce agent prompt language that closely mirrors Skyvern's verbatim prompt text (published in their open-source repo), the AGPL boundary may be violated — even if no source code files are copied.

**Likelihood:** MEDIUM — build agents have the Skyvern repository in training data and may reproduce language verbatim under pressure to match the pattern closely.

**Impact:** HIGH — AGPL-3.0 copyleft, if triggered by prompt-level copying, would require either a license exception negotiation with Skyvern or a skill redesign.

**Mitigation:**
1. Include an explicit guardrail in `e2e-executor.governance.yaml` and `e2e-author.governance.yaml`: `no_skyvern_source_code` (already included in the schema above).
2. Phase 4 build agents receive a boundary statement in their context: "Adopt pattern; do not copy verbatim text. Skyvern's AGPL-3.0 applies to source code and derived works; architectural blueprints and design principles are not covered."
3. PLAYBOOK.md includes the AGPL-3.0 boundary note from requirements §8 verbatim as a build-time reminder.

### Risk 3: Validation Strategy Operationalization Gap

**Description:** The requirements spec defines a six-step validation procedure in Section 6.3 and an assertion sensitivity classification (VERIFIED | RAN-ONLY | ABSENT). Translating this into a prompt template (`e2e-validation-check.md`) that consistently produces the correct classification for edge cases (e.g., an assertion that checks element visibility but not content — "VERIFIED for existence, RAN-ONLY for content") requires nuanced judgment calls that a single template iteration may not cover.

**Likelihood:** MEDIUM — the sensitivity check is the most subjective step in the validation procedure; automated classification of assertion quality is a known hard problem.

**Impact:** MEDIUM — if the verifier misclassifies assertions as VERIFIED when they are RAN-ONLY, the quality gate may pass tests that do not actually verify application correctness. This directly undermines P-E2E-09's published quality gate.

**Mitigation:**
1. The `examples/auth-journey.feature` example must include both VERIFIED and RAN-ONLY assertion examples, with classification rationale in comments, to give the verifier agent a calibration reference.
2. The `e2e-validation-check.md` template (Step B) must include the three-level escalation model from requirements §6.1 (navigation → identity → isolation) as concrete worked examples, not just abstract criteria.
3. The eval corpus (P-E2E-09, >= 20 scenarios) must be seeded in Phase 4 Step B with at least 5 scenarios that specifically test the RAN-ONLY vs VERIFIED edge cases.

### Risk 4: Tool-Allowlist Drift Across Agent Files

**Description:** The governance YAML files and the agent MD files each declare tool allowlists. With 5 agents and 10 files that reference tools, drift between the governance YAML allowlist and the agent MD "Tool Integration" section is a realistic consistency failure during Phase 4 authoring.

**Likelihood:** HIGH — manual consistency across 10 files is a known failure mode in multi-file specifications.

**Impact:** MEDIUM — tool-allowlist inconsistency is not a security vulnerability in this context (the governance YAML is the enforced reference), but it creates agent identity confusion and fails the post-completion check `verify_file_created` if the agent MD claims tools that the YAML does not permit.

**Mitigation:**
1. Phase 4 build sequence (Section 7) requires governance YAML to be authored before the agent MD within Step C. The agent MD cites the governance YAML as its tool authority: "See `agents/{agent}.governance.yaml` `capabilities.allowed_tools` for the authoritative tool list."
2. A Phase 4 post-build verification step: grep all `agents/*.md` for tool names and compare against corresponding `agents/*.governance.yaml` `allowed_tools` fields. Flag any mismatch before the skill is registered.

### Risk 5: eval Corpus Below 20-Scenario Threshold at Release (P-E2E-09)

**Description:** P-E2E-09 requires the quality gate metrics (execution_recall, element_precision, MMR) to be computed against a named eval corpus of >= 20 scenarios. The requirements spec notes that GenIA-E2ETest used n=12, which is "LIMITED STATISTICAL POWER." If Phase 4 only produces the 3 example scenarios (auth-journey, security-wstg-busl, agentic-flow-example), the initial eval corpus is n=3 — far below the stated requirement.

**Likelihood:** HIGH — Phase 4 build agents are scoped to produce skill files, not a 20-scenario corpus. The corpus cannot be generated without a target application to test against.

**Impact:** MEDIUM — the skill can be released without a validated corpus if the release is marked as "eval corpus pending" and the quality gate metrics are flagged as `[UNVALIDATED — corpus < 20 scenarios]`. The skill is usable; the quality guarantees are not yet evidenced.

**Mitigation:**
1. Phase 4 Step B seeds the `examples/` directory with 3 reference scenarios (the three planned example files). These are reference artifacts, not eval corpus entries.
2. PLAYBOOK.md defines the eval corpus governance (OQ-E2E-007 resolution): e2e-analyst is the corpus maintenance owner; the corpus grows as /e2e-testing is used on real projects; a skill release is blocked only if any metric falls below threshold on a corpus that has already reached >= 20 scenarios. The first release with n < 20 is explicitly classified as "pre-corpus release" with P-022-compliant disclosure.
3. An explicit WORKTRACKER task is opened at Phase 4 completion to track corpus growth to >= 20 scenarios before the first production engagement.

### Risk 6: SPA Hardening Strategy is Underspecified (OQ-E2E-002)

**Description:** OQ-E2E-002 asks for exact wait conditions for SPA-heavy applications. The requirements spec identifies `networkidle` as a candidate but does not resolve the question with framework-specific detail (React, Vue, Angular race conditions differ). The `e2e-executor` agent and the governance config both reference `spa_wait_strategy: networkidle` as a default, but Phase 4 build agents cannot produce specific SPA-hardening code without knowing the target SPA framework.

**Likelihood:** HIGH for React/Angular SPAs; MEDIUM for server-rendered applications.

**Impact:** MEDIUM — SPA-driven timing failures are the "timing" category in the six-category flake taxonomy. Underspecified wait strategies produce flaky tests that repeatedly fail the quality gate on element_precision (stale element references) without the test author understanding why.

**Mitigation:**
1. SKILL.md Phase A resolves OQ-E2E-002 with a decision rule: "For SPAs identified by `document.readyState !== 'complete'` after initial navigation, apply `networkidle` + `waitForSelector('[data-testid=app-ready]')` before DOM snapshot. For Angular specifically, also await `window.getAllAngularRootElements()` to resolve." This is documented in PLAYBOOK.md.
2. The `e2e-executor` agent's Methodology section cites the SPA wait-chain rule and applies it before every `browser_snapshot` invocation on an SPA target.

### Risk 7: Autonomy-Tier Declaration as a P-022 Enforcement Point

**Description:** P-E2E-10 (autonomy-tier declaration) is a P-022 (no deception) enforcement mechanism. If the e2e-reporter agent is absent or invoked incorrectly, the L0 output may be surfaced to the user without the `autonomy_tier` field. The three-agent minimum (author, executor, verifier) does not include reporter; without reporter, the autonomy-tier declaration has no dedicated owner.

**Likelihood:** MEDIUM — the three-agent minimum path is a legitimate invocation path that does not automatically include e2e-reporter.

**Impact:** HIGH — P-022 is a constitutional HARD rule (H-03). A test run surfaced to the user without autonomy-tier declaration is a P-022 violation. This is not a quality gap; it is a governance violation.

**Mitigation:**
1. The autonomy-tier declaration is not exclusively owned by e2e-reporter. It is also required in e2e-verifier's PASS/FAIL verdict output (requirements §4: "e2e-verifier MUST emit both scores as distinct fields"). The e2e-verifier's governance YAML includes `autonomy_tier_in_l0: required` as a validation post-completion check, ensuring the field is present in the verifier output even when e2e-reporter is absent.
2. e2e-governance-config.md includes `autonomy_tier: AUTONOMOUS` as a mandatory field with no default-omit option. If the field is absent from the governance config, the input validation guardrail in the governance YAML blocks the run.

---

## 9. Acceptance Criteria for Phase 3B Handoff

Phase 3 Step B (eng-architect) needs the following from this implementation plan to produce the skill architecture. Each item is a boolean PASS/FAIL checklist for the handoff gate.

- [ ] File tree is complete — every file in Section 1 has a one-line purpose statement and REQUIRED/OPTIONAL designation with rationale. eng-architect has a definitive file list to design against.
- [ ] Agent roster is definitive — all 5 agents have: identity sentence, principle ownership (P-E2E-NN citations), integration points (upstream and downstream), tool allowlist (canonical tool names), forbidden tool list. No "TBD" placeholders.
- [ ] Template inventory is actionable — all 5 templates have: input parameter list, output section outline, principle citations, example invocation stub. eng-architect can produce the gTAA layer diagram showing which template belongs to which layer.
- [ ] Governance YAML schema is complete — all fields defined, field types specified, e2e-testing-specific overrides from eng-qa baseline noted. eng-architect can author all 5 governance YAMLs from this schema without further research.
- [ ] H-25..H-30 compliance commitments are made explicitly — SKILL.md description candidate text is in this document; eng-architect does not need to draft it.
- [ ] Quality threshold is resolved — 0.94 (RT-004), with triangulation documented. No ambiguity for eng-architect.
- [ ] Phase 4 build sequence has explicit inter-step dependencies — eng-architect knows to deliver governance YAML schemas before agent MD skeletons within Step C, and to consume SKILL.md's Playwright MCP version pin before authoring agent tool allowlists.
- [ ] Open questions OQ-E2E-001 through OQ-E2E-007 have resolution assignments — eng-architect knows which open questions must be resolved in SKILL.md (Phase 4 Step A) before templates can be authored (Phase 4 Step B). Specifically: OQ-E2E-001 (agentic-flow syntax) and OQ-E2E-002 (SPA hardening) must be resolved in Phase 4 Step A.
- [ ] AGPL-3.0 boundary is documented — eng-architect knows to include the boundary note in SKILL.md and to enforce `no_skyvern_source_code` guardrail in governance YAMLs.
- [ ] AE-002 escalation flag is raised — eng-architect knows the CLAUDE.md and mandatory-skill-usage.md registration is auto-C3 and requires a separate human-gated step, not a routine file commit.
- [ ] Cross-skill integration seams are resolved — eng-architect can diagram the three eng-team seams, the ps-critic loop, and the adv-scorer integration without needing to re-research the requirements.
- [ ] Risks 1-7 are communicated — eng-architect is aware of Playwright MCP instability (Risk 1), AGPL boundary (Risk 2), eval corpus gap (Risk 5), and autonomy-tier P-022 enforcement (Risk 7) before authoring the skill architecture.

---

## Source References

| Claim | Source |
|-------|--------|
| Agent roster (author, executor, verifier) — confirmed minimum | requirements §4 |
| e2e-analyst adoption rationale | requirements §4 (analyst case for inclusion) + P-E2E-01 + P-E2E-03 |
| e2e-reporter adoption rationale | requirements §4 (reporter case for inclusion) + P-E2E-10 + eng-team baseline §7.3 |
| Five template names | requirements §5 |
| Governance YAML field schema | eng-team baseline §5 (`eng-qa.governance.yaml` + `eng-reviewer.governance.yaml`) |
| `^E2E-\d{4}$` testrun ID format | requirements §9 ("Reusable Patterns" table); eng-team baseline §7.5 |
| Output path `skills/e2e-testing/output/{testrun-id}/` | eng-team baseline §7.5 (ported pattern) |
| Quality threshold 0.94 | requirements §9 (RT-004 triangulation); requirements §1 L2 |
| Phase gates PG-1..PG-7 | requirements §9 ("Reusable Patterns" table); eng-team baseline §7.7 |
| Playwright MCP core-8 tools | requirements §4 (e2e-executor integration points); innovators baseline inn-2 §7.1 (max 10 tools) |
| Browser-Use in explorer mode only | requirements §8 (Skyvern-MIRROR posture table); innovators baseline inn-3 |
| `no_skyvern_source_code` guardrail | requirements §8 (AGPL-3.0 boundary note) |
| PLAYBOOK.md as REQUIRED | eng-team baseline §7.7; requirements §10 (7 open questions require prose resolution) |
| examples/ as REQUIRED | requirements §10 OQ-E2E-001 (agentic-flow syntax requires worked example); P-E2E-02 (linting rule requires reference scenario) |
| AE-002 auto-C3 for CLAUDE.md + mandatory-skill-usage.md | quality-enforcement.md AE-002 |
| H-14 creator-critic minimum 3 iterations | quality-enforcement.md H-14 |
| H-15 self-review before presenting | quality-enforcement.md H-15 |
| H-17 S-014 scoring required for C2+ | quality-enforcement.md H-17 |
| P-022 autonomy-tier as no-deception mechanism | requirements §2 P-E2E-10 traceability |
| Six-category flake taxonomy (QA Wolf) | requirements §8 (QA Wolf MIRROR posture); innovators baseline inn-1 §3.1 |
| Escalation three-failure ladder | eng-team baseline §4 (eng-reviewer escalation protocol) |
| GenIA-E2ETest metric formulas and thresholds | requirements §2 P-E2E-09; requirements §6.4 |
| Dual-mode codegen/explorer | requirements §2 P-E2E-05; requirements §3 RT-002 |
| WSTG six mandatory categories | requirements §2 P-E2E-08; requirements §7 (Standards Posture) |
| ISO 29119 opt-in via flag | requirements §3 RT-001 resolution |
| gTAA four-layer architecture | requirements §2 P-E2E-07; lane-standards §2 Theme 2 (SP-3) |
| Composition/ directory pattern | eng-team baseline §5 (composition/eng-qa.agent.yaml pattern) |
| AD-010 three-level degradation | requirements §9 ("Reusable Patterns" table); eng-team baseline §7.2 |
| SPA hardening: `networkidle` default | requirements §5 (e2e-governance-config.md default block) |
| criticality_default: C2 judgment call | quality-enforcement.md C2 definition (reversible within 1 day); P-022 honesty flag |
| eng-architect tool allowlist revision note (web_search for author) | P-022 honesty flag — judgment call disclosed |
