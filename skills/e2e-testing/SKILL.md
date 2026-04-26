---
name: e2e-testing
description: "Provides LLM-orchestrated end-to-end testing for web applications and agentic flows. Generates, executes, and verifies browser-driven user-journey tests using a Planner-Executor-Verifier triad. Defaults to diff-scoped test generation (git diff in, Gherkin scenarios out); full-suite requires explicit opt-in. Two execution modes: codegen (committed Playwright .spec.ts files, CI-safe without LLM) and explorer (LLM in loop for self-healing). Every scenario includes a @basis: tag, risk classification, and WSTG v4.2 security tags. Quality gate: execution_recall >= 0.80, element_precision >= 0.70, MMR <= 0.15, S-014 score >= 0.94. Non-goals: unit tests, API contract tests, SAST, DAST, fuzzing, load tests. Trigger keywords: e2e test, end-to-end test, browser test, user journey, playwright, generate test, agentic flow test, WSTG coverage, diff scope test, regression test, codegen test, explorer mode."
version: "1.0.0"
criticality: C3
quality_threshold: 0.94
constitutional_compliance: Jerry Constitution v1.0
activation_keywords:
  - "e2e test"
  - "end-to-end test"
  - "browser test"
  - "user journey"
  - "playwright"
  - "generate test"
  - "test this flow"
  - "agentic flow test"
  - "WSTG coverage"
  - "diff scope test"
  - "regression test"
  - "smoke test"
  - "codegen test"
  - "explorer mode"
  - "visual regression"
allowed_tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - WebSearch
  - WebFetch
  - mcp__playwright__browser_snapshot
  - mcp__playwright__browser_click
  - mcp__playwright__browser_type
  - mcp__playwright__browser_navigate
  - mcp__playwright__browser_verify_element_visible
  - mcp__playwright__browser_take_screenshot
  - mcp__playwright__browser_wait_for
  - mcp__playwright__browser_evaluate
---

# /e2e-testing -- End-to-End Testing for Web Services with Agentic Flow Support

> LLM-orchestrated browser test generation, execution, and verification. Diff in. Verified Gherkin out.

---

## Document Audience (Triple-Lens)

This SKILL.md serves multiple audiences:

| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0 (Stakeholder)** | Project owners, team leads | [Purpose](#purpose), [When to Use](#when-to-use-this-skill), [When NOT to Use](#when-not-to-use-this-skill), [Autonomy Tiers](#autonomy-tiers) |
| **L1 (Engineer)** | Developers invoking agents | [Core Capabilities](#core-capabilities), [Available Agents](#available-agents), [Workflow / Pipeline](#workflow--pipeline), [Templates](#templates), [Playbook and Examples](#playbook-and-examples) |
| **L2 (Architect)** | Workflow and integration designers | [The 10 Principles](#the-10-principles-p-e2e-01p-e2e-10), [Quality Gates](#quality-gates), [Cross-Skill Integration](#cross-skill-integration), [Validation Strategy](#validation-strategy), [Governance](#governance) |

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Document Audience (Triple-Lens)](#document-audience-triple-lens) | Audience routing table |
| [Purpose](#purpose) | What the skill does (L0) |
| [When to Use This Skill](#when-to-use-this-skill) | Activation conditions |
| [When NOT to Use This Skill](#when-not-to-use-this-skill) | Routing disambiguation with consequences |
| [Core Capabilities](#core-capabilities) | Five-agent pipeline summary |
| [The 10 Principles](#the-10-principles-p-e2e-01p-e2e-10) | P-E2E-01 through P-E2E-10 with tier and ownership |
| [Available Agents](#available-agents) | Agent roster with role, principle ownership, primary artifact |
| [Workflow / Pipeline](#workflow--pipeline) | ASCII pipeline diagram |
| [Autonomy Tiers](#autonomy-tiers) | Four tiers with default and opt-in requirements |
| [Quality Gates](#quality-gates) | Skill-internal 0.94 gate and creator-critic loop |
| [Cross-Skill Integration](#cross-skill-integration) | Integration seams with sibling skills |
| [Templates](#templates) | Five templates with purpose |
| [Validation Strategy](#validation-strategy) | Six-step mechanism and orthogonality disclosure |
| [Governance](#governance) | Governance YAML pointers, AGPL boundary, secret handling |
| [Playbook and Examples](#playbook-and-examples) | PLAYBOOK.md and examples/ pointers |
| [Constitutional Compliance](#constitutional-compliance) | Principle-by-principle compliance table |
| [Evidence Confidence Register](#evidence-confidence-register) | Consolidated confidence flag registry with scope and location |
| [Registration](#registration) | CLAUDE.md, AGENTS.md, mandatory-skill-usage.md entries |
| [References](#references) | Authoritative standards with URLs |
| [Footer](#footer) | Version, date, compliance statement |

---

## Purpose

The `/e2e-testing` skill gives the Jerry framework the ability to write, run, and verify end-to-end tests for web applications -- the kind of tests that interact with a real browser the way a real user would. Jerry's `/eng-team` skill handles security and code-quality testing at the unit and API level; it has zero coverage of anything that requires a browser. This skill fills that gap.

It operates in two named modes:

- **Codegen mode** -- The skill generates committed Playwright `.spec.ts` files that run in CI without any LLM in the loop. Use this for regression-critical, stable flows.
- **Explorer mode** -- The LLM stays in the loop during execution, enabling self-healing and exploratory runs on flows where the application keeps changing.

Every test generated traces back to a requirement, a risk item, or a security concern via a `@basis:` tag. Security scenarios carry WSTG v4.2 category tags. Every test run declares its autonomy tier so users know exactly how much human oversight was involved.

---

## When to Use This Skill

Activate this skill when:

- A `git diff` has landed and you want test coverage scoped to the changed flows
- You need browser-driven user-journey tests for a web application
- You want WSTG-tagged security scenarios (authentication, authorisation, session, input validation, business logic, API) at the browser layer
- An LLM agent is the system under test and you need trajectory assertions (tool-call ordering, intermediate state checks)
- You want to regenerate broken Playwright tests after a UI drift (explorer mode self-healing)
- You need a committed `.spec.ts` file that CI can run without an LLM present (codegen mode)
- You need a Gherkin `.feature` file with traceable `@basis:` tags for a new user story

---

## When NOT to Use This Skill

| Situation | Correct Route | Consequence of Misrouting |
|-----------|--------------|--------------------------|
| Unit tests or property-based tests | `/eng-team` (eng-qa) | This skill will refuse: no browser = no scope |
| API contract testing (OpenAPI, Pact) | `/eng-team` (eng-qa) | Out of scope; skill is browser-journey-only |
| SAST, DAST, fuzzing, or load testing | `/eng-team` (eng-devsecops or eng-qa) | Non-goals declared in P-002; skill will not proceed |
| Threat modeling or architecture review | `/eng-team` (eng-architect) | Skill is a test-generation consumer, not a design producer |
| Securing the CI/CD pipeline itself | `/eng-team` (eng-devsecops) | e2e-testing feeds pipeline artifacts; it does not configure gates |
| Code review | `/eng-team` (eng-security, eng-reviewer) | Skill produces tests, not review findings |
| Input validation fuzzing | `/eng-team` (eng-qa) | Browser-journey scope excludes protocol-level fuzzing |

---

## Core Capabilities

The skill uses a five-agent pipeline. Three agents are the minimum required core; two are optional but recommended.

| Agent | Role | Status |
|-------|------|--------|
| `e2e-analyst` | Change-Impact Analyst -- maps git diffs to user flows, identifies WSTG coverage gaps, produces prioritised scope document | Optional (recommended) |
| `e2e-author` | Test Scenario Planner and Gherkin Author -- risk classification, declarative scenario authoring, WSTG security scenario generation | Core (required) |
| `e2e-executor` | Browser Driver and Test Runner -- DOM snapshot acquisition, Playwright MCP-based execution, codegen and explorer modes | Core (required) |
| `e2e-verifier` | Correctness Validator and Escalation Supervisor -- six-step validation, metric computation, failure escalation to author | Core (required) |
| `e2e-reporter` | Multi-Level Report Assembler -- L0/L1/L2 assembly with mandatory autonomy-tier declaration | Optional (recommended) |

The pipeline defaults to: analyst (if diff provided) → author → executor → verifier → reporter.

---

## The 10 Principles (P-E2E-01..P-E2E-10)

All principles are defined in full in `projects/PROJ-017-e2e-testing-skill/orchestration/e2e-skill-build-20260420-001/synthesis/e2e-skill-requirements.md`.

| ID | Name | Tier | Primary Owner | One-Line Description |
|----|------|------|--------------|---------------------|
| P-E2E-01 | Risk-First Test Ordering | HARD | e2e-analyst | Classify risk (HIGH/MEDIUM/LOW) and criticality (C1-C4) before authoring any scenario step |
| P-E2E-02 | Declarative Gherkin + `@basis:` Tag | HARD | e2e-author | All scenarios in declarative Given-When-Then with a traceable basis reference; UI verbs in When steps are rejected |
| P-E2E-03 | Diff-Scoped Entry | HARD | e2e-analyst | Default invocation requires a git diff; full-suite generation requires explicit user confirmation |
| P-E2E-04 | Planner-Executor-Verifier Triad + Supervisor Loop | HARD | e2e-verifier | Verifier escalates failures to Author for replanning; Executor never receives escalation or retry decisions |
| P-E2E-05 | Dual Execution Mode | HARD | e2e-executor | Mode (codegen/explorer) must be declared before execution begins; codegen is default for C2+ flows |
| P-E2E-06 | Live-DOM-Grounded Locator Generation | HARD | e2e-executor | `browser_snapshot` must precede every locator generation step; no hallucinated selectors |
| P-E2E-07 | gTAA-Conformant Layer Architecture | HARD | e2e-executor | Four-layer separation (Generation/Definition/Execution/Adaptation); only Adaptation layer touches browser driver |
| P-E2E-08 | WSTG Security Coverage | HARD | e2e-author | Minimum one scenario per WSTG v4.2 category: ATHN, ATHZ, SESS, INPV, BUSL, APIT |
| P-E2E-09 | Published Quality Gate with Exact Metrics | HARD | e2e-verifier | execution_recall >= 0.80, element_precision >= 0.70, MMR <= 0.15, computed against named eval corpus |
| P-E2E-10 | Explicit Autonomy-Tier Declaration | HARD | e2e-reporter | Every test run L0 output declares AUTONOMOUS, SUPERVISED, or MANAGED-EQUIVALENT with one-sentence explanation |

All 10 principles are HARD tier. Overriding any principle requires a documented ADR and C3 auto-escalation per AE-003.

---

## Available Agents

Full agent definitions are at the paths listed. Governance YAML files are the authoritative tool allowlist source for each agent.

| Agent | File | Role | Primary Principle Ownership | Primary Artifact |
|-------|------|------|----------------------------|-----------------|
| `e2e-analyst` | `skills/e2e-testing/agents/e2e-analyst.md` | Change-Impact Analyst | P-E2E-01, P-E2E-03 | `scope-document.json` |
| `e2e-author` | `skills/e2e-testing/agents/e2e-author.md` | Test Scenario Planner and Gherkin Author | P-E2E-02, P-E2E-08 | `{scenario}.feature`, `author-plan.json` |
| `e2e-executor` | `skills/e2e-testing/agents/e2e-executor.md` | Browser Driver and Test Runner | P-E2E-05, P-E2E-06, P-E2E-07 | `executor-trace.json`, `.spec.ts` (codegen) |
| `e2e-verifier` | `skills/e2e-testing/agents/e2e-verifier.md` | Correctness Validator and Escalation Supervisor | P-E2E-04, P-E2E-09 | `verifier-verdict.json` |
| `e2e-reporter` | `skills/e2e-testing/agents/e2e-reporter.md` | Multi-Level Report Assembler | P-E2E-10 | `report-L0.md`, `report-L1.md`, `report-L2.md` |

All agent outputs are persisted to `skills/e2e-testing/output/{E2E-NNNN}/` per P-002. The `E2E-NNNN` test run ID format is `^E2E-\d{4}$`.

Output levels for every agent:
- **L0 (Executive):** GO/NO-GO, autonomy tier, headline metrics in plain language.
- **L1 (Technical):** Per-scenario pass/fail, WSTG coverage matrix, quality metric grid.
- **L2 (Strategic):** Coverage gap analysis, threshold trend, maintenance recommendations.

---

## Workflow / Pipeline

```
User
 |
 | /e2e-testing generate-tests --diff HEAD~1..HEAD --risk HIGH --mode codegen --autonomy SUPERVISED
 |
 v
e2e-analyst -------> scope-document.json (P-E2E-01, P-E2E-03)
 |                        |
 | [P-E2E-03 gate]        |
 | confirm scope          |
 |<--(user confirm)       |
                          v
                    e2e-author -------> author-plan.json + {scenario}.feature (P-E2E-02, P-E2E-08)
                          |
                          v
                    e2e-executor -----> executor-trace.json + screenshots/ + dom-snapshots/ (P-E2E-05/06/07)
                          |
                          v
                    e2e-verifier -----> verifier-verdict.json (P-E2E-04, P-E2E-09)
                          |
                     FAIL |------------> failure-diagnostic.json ---------> e2e-author (replan)
                          |                                                       |
                     PASS |                                               [max 3 iterations per H-14]
                          |
                          |----> /adversary (adv-scorer) ---> S-014 score
                          v
                    e2e-reporter -----> report-L0.md / report-L1.md / report-L2.md (P-E2E-10)
                          |
                          v
                         User (receives report with autonomy_tier in L0)
```

**Escalation ladder on repeated FAIL:**
1. First FAIL: author receives `failure-diagnostic.json` and replans (H-14 iteration 1).
2. Second FAIL: author replans again with strengthened diagnostic (H-14 iteration 2).
3. Third FAIL: AE-006 mandatory human escalation. Reporter emits FAIL verdict with AE-006 flag.

---

## Autonomy Tiers

Every invocation must declare one of four autonomy tiers (per RT-003 resolution). The tier is set in `skills/e2e-testing/templates/e2e-governance-config.md` (default: `SUPERVISED` for initial release) and surfaces as the first field in every L0 report.

| Tier | Purpose | Default? | Permitted | Opt-in required | Forbidden |
|------|---------|----------|-----------|-----------------|-----------|
| `AUTONOMOUS` | Full batch without human review of individual steps; quality gate is the only backstop | No | Yes (SUPERVISED preferred for initial release) | No | No |
| `SUPERVISED` | Per-step human confirmation before execution proceeds | YES (initial-release default) | Yes | No | No |
| `MANAGED-EQUIVALENT` | Human engineers review and backstop AI failures post-run, similar to a managed QA service model | No | Yes | Yes -- caller must document human review process in engagement notes | No |
| `FULLY-AUTONOMOUS-PROD` | Autonomous execution against real production SUT with no human gate | -- | No | N/A | YES -- governance guardrail forbids; see RT-003 |

**P-022 enforcement:** The tier declaration is a no-deception mechanism (H-03). The skill MUST NOT promise outcomes associated with a higher tier than declared. If `autonomy_tier` is absent from the governance config, all agents block invocation. If e2e-reporter is absent from the pipeline, e2e-verifier is responsible for emitting `autonomy_tier` in its own PASS/FAIL verdict (dual-enforcement safety net).

---

## Quality Gates

### Skill-Internal Gate (0.94)

The skill operates a two-track quality gate per P-E2E-09:

**Track 1 -- Functional Correctness (GenIA-E2ETest metrics):**

| Metric | Formula | Initial-Release Threshold | Confidence Flag |
|--------|---------|--------------------------|-----------------|
| `execution_recall` | CS / ES | >= 0.80 | [SINGLE-STUDY -- GenIA-E2ETest n=12] |
| `element_precision` | C / G | >= 0.70 | [SINGLE-STUDY] |
| `element_recall` | C / E | >= 0.70 | [SINGLE-STUDY] |
| `manual_modification_rate` | edits / generated steps | <= 0.15 | [SINGLE-STUDY] |
| `assertion_sensitivity_rate` | VERIFIED / total assertions | >= 0.70 | [eng-architect derived metric] |

Thresholds are initial-release conservative targets, explicitly intended to tighten as Jerry's eval corpus grows beyond the single-study baseline (P-022 disclosure).

**Track 2 -- Process Quality (S-014 via adv-scorer):**

e2e-verifier invokes `/adversary` (adv-scorer) for all C2+ deliverables per H-17. The S-014 six-dimension rubric (completeness, internal consistency, methodological rigor, evidence quality, actionability, traceability) is scored against the 0.94 threshold. This is a triangulated threshold, not an empirically optimal value -- see RT-004 in the requirements specification for derivation rationale.

**Orthogonality:** Track 1 and Track 2 measure distinct concerns. A test suite can score well on S-014 process quality (well-documented methodology) while failing functional correctness (fragile selectors). Both tracks must pass independently. They are never averaged.

### Creator-Critic Loop (H-14)

All C2+ deliverables require a minimum 3-iteration creator-critic-revision cycle per H-14. e2e-author is the creator; ps-critic (from `/problem-solving`) is the external critic for planning artifacts. e2e-verifier's self-review (H-15) is the self-review step before the external critic cycle, not a substitute for it.

---

## Cross-Skill Integration

| Integrated Skill | Integration Point | Activation Trigger |
|-----------------|------------------|--------------------|
| `/eng-team` (eng-qa) | Security test scope boundary: WSTG-tagged `@wstg:` scenarios (browser-layer, user-journey) vs `@owasp-tg:` scenarios (unit/API-layer, threat-model-derived) | Any security scenario spanning authentication, session management, or business logic abuse at the browser layer |
| `/eng-team` (eng-reviewer) | Engagement-level quality gate at 0.95 (sequential after e2e-testing's internal 0.94 gate passes) | Engagement close; e2e-verifier PASS verdict feeds eng-reviewer evidence package |
| `/eng-team` (eng-devsecops) | CI/CD gate wiring: e2e-testing produces WSTG-coverage reports and quality metric artifacts; eng-devsecops configures the pipeline gate that consumes them | Post-skill-completion pipeline integration |
| `/problem-solving` (ps-critic) | H-14 creator-critic-revision loop: e2e-author (creator) paired with ps-critic (external critic) for C2+ deliverables | Any C2+ test plan requiring formal quality review |
| `/problem-solving` (ps-investigator) | Upstream failure research: e2e-author consults ps-investigator when a failure hypothesis requires research before replanning | Replanning triggered by verifier FAIL with unknown failure category |
| `/adversary` (adv-scorer) | S-014 process quality scoring at the skill-internal gate (Track 2 of the dual-track gate) | e2e-verifier invokes per H-17 for all C2+ deliverables |
| `/nasa-se` | Optional ISO 29119-3 test case specification artifacts when `iso29119_artifacts: true` in governance config (RT-001 opt-in) | Regulated or enterprise contexts requiring formal test documentation |

---

## Templates

All templates are in `skills/e2e-testing/templates/`. They are parameterised workflow prompts consumed by the agents listed. Phase 4 Step B (eng-qa) authors these files.

| Template File | Consuming Agent | Purpose |
|--------------|----------------|---------|
| `skills/e2e-testing/templates/e2e-test-generation.md` | `e2e-author` | Primary test authoring workflow: risk classification, declarative Gherkin with `@basis:` tags, WSTG six-category security scenario generation |
| `skills/e2e-testing/templates/e2e-agentic-flow.md` | `e2e-author`, `e2e-verifier` | Agentic-flow test authoring: trajectory assertions (tool-call ordering, intermediate state checkpoints), non-determinism budget, golden transcript generation in codegen mode |
| `skills/e2e-testing/templates/e2e-validation-check.md` | `e2e-verifier` | Correctness validation: six-step decision procedure, VERIFIED/RAN-ONLY/ABSENT assertion classification, metric computation, PASS/REVISE/FAIL verdict, escalation payload construction |
| `skills/e2e-testing/templates/e2e-diff-scope.md` | `e2e-analyst`, `e2e-author` (fallback) | Change-impact analysis: changed-file classification, flow adjacency mapping, WSTG gap check, prioritised scope document construction |
| `skills/e2e-testing/templates/e2e-governance-config.md` | All agents (at invocation) | Per-run governance YAML block: execution mode, autonomy tier, WSTG categories, quality thresholds, SPA wait strategy, Playwright MCP version pin |

---

## Validation Strategy

The full validation specification is in `skills/e2e-testing/validation/validation-strategy.md` (authored in Phase 4 Step B). The following summary governs what build agents may assume.

The validation mechanism is a **six-step decision procedure** applied by e2e-verifier to every scenario:

1. Parse Gherkin feature to extract all `Then` assertion statements.
2. Map each assertion to a P-E2E principle (security check, functional check, trajectory check).
3. Score each assertion on sensitivity: VERIFIED (assertion tests correctness), RAN-ONLY (assertion tests only that execution occurred), or ABSENT (no assertion for stated purpose).
4. Compute coverage across five dimensions: happy path, failure path, boundary, security, agentic-divergence.
5. Compute functional-correctness metrics using P-E2E-09 formulas (element_precision, element_recall, execution_precision, execution_recall, manual_modification_rate).
6. Emit PASS, REVISE, or FAIL verdict with threshold comparison and full assertion inventory.

**Orthogonality disclosure (P-022):** The S-014 process quality score and the GenIA-E2ETest functional-correctness metrics measure orthogonal concerns. A deliverable can score well on S-014 (well-documented methodology) and fail on execution_recall (fragile selectors), or vice versa. The 0.94 S-014 threshold is a triangulated value (see RT-004 in the requirements specification), not an independently evidenced empirically optimal threshold. Both scores are emitted as distinct fields in every `verifier-verdict.json`; they are never averaged or combined into a single signal. A test run that passes one track but fails the other is a failed test run.

---

## Governance

### Agent Governance Files

Each agent has a paired governance YAML that is the authoritative source for that agent's tool allowlist, quality thresholds, input validation guardrails, and post-completion checks. Phase 4 build agents MUST write governance YAML before the corresponding agent `.md` file.

| Governance File | Agent Governed |
|----------------|----------------|
| `skills/e2e-testing/agents/e2e-analyst.governance.yaml` | `e2e-analyst` |
| `skills/e2e-testing/agents/e2e-author.governance.yaml` | `e2e-author` |
| `skills/e2e-testing/agents/e2e-executor.governance.yaml` | `e2e-executor` |
| `skills/e2e-testing/agents/e2e-verifier.governance.yaml` | `e2e-verifier` |
| `skills/e2e-testing/agents/e2e-reporter.governance.yaml` | `e2e-reporter` |

### AGPL-3.0 Boundary (Skyvern)

This skill's architecture adopts the Planner-Executor-Verifier pattern and diff-scoped discipline derived from Skyvern's published architectural designs. Skyvern source code is excluded under AGPL-3.0. The boundary is enforced via a `no_skyvern_source_code` output-filtering guardrail in `e2e-author.governance.yaml` and `e2e-executor.governance.yaml`. Phase 4 build agents receive a boundary statement: adopt pattern; do not copy verbatim text.

### Secret and Credential Handling

`e2e-executor` is the only agent that interacts with a live browser and may encounter session tokens, PII, or credentials during test execution. Its governance YAML includes `no_secrets_in_output` as a mandatory output filter. Screenshots and DOM snapshots are written to `skills/e2e-testing/output/{E2E-NNNN}/` -- these directories must be added to `.gitignore` for runs against production or staging systems that handle real credentials. Governance config includes `screenshot_on_failure: true` (enabled for diagnostic value) and `trace_on_failure: true` (enabled for replay support). Users operating against production systems should review the output directory for sensitive content before committing.

### Playwright MCP Version Pin

`@playwright/mcp` is at a pre-release version (`v0.0.x`) with observed instability across version bumps. The exact version pin is declared in the PLAYBOOK.md MCP upgrade SOP section. All five agent governance YAML files propagate this version pin. To upgrade, follow the SOP in `skills/e2e-testing/PLAYBOOK.md` before updating the pin.

---

## Playbook and Examples

### PLAYBOOK.md

`skills/e2e-testing/PLAYBOOK.md` is a required operational reference, not optional documentation. It resolves the seven open questions from the requirements specification (OQ-E2E-001 through OQ-E2E-007) that SKILL.md cannot contain without violating H-28. Phase 4 build agents for templates and agent definitions depend on it.

Key resolutions in PLAYBOOK.md:
- OQ-E2E-001: Agentic-flow Gherkin extension syntax (canonical `When an agentic actor...` / `Then the agent called...` format)
- OQ-E2E-002: SPA hardening wait-chain rule (`networkidle` + `waitForSelector('[data-testid=app-ready]')` for SPAs; Angular-specific additions)
- OQ-E2E-003: Contract testing routing decision rule
- OQ-E2E-004 through OQ-E2E-007: Vision-LLM fallback trigger (RT-003: a11y-tree-first is the primary locator strategy; vision-LLM is a supervised fallback only -- see RT-003 for the tension resolution between locator reliability and LLM-vision cost), dual-mode invocation contract, eval corpus governance (>= 20 scenarios before production quality guarantees apply), ISO 29119 opt-in depth

### Examples

`skills/e2e-testing/examples/` contains three required reference scenarios that serve as calibration references for build agents and linting validation (not eval corpus entries):

| File | Purpose |
|------|---------|
| `skills/e2e-testing/examples/auth-journey.feature` | Worked declarative Gherkin example covering P-E2E-02 style; includes both VERIFIED and RAN-ONLY assertion examples with classification rationale in comments |
| `skills/e2e-testing/examples/security-wstg-busl.feature` | WSTG BUSL-tagged scenario demonstrating business-logic abuse coverage (P-E2E-08) |
| `skills/e2e-testing/examples/agentic-flow-example.feature` | Trajectory assertion syntax example using OQ-E2E-001 resolved extension (canonical reference for linting validation) |

---

## Constitutional Compliance

| Principle | How This Skill Complies |
|-----------|------------------------|
| P-003: No Recursive Subagents | No agent in the skill spawns sub-agents. The pipeline is sequential and linear: analyst -> author -> executor -> verifier -> reporter. Each agent is invoked by the user or orchestrator, not by another agent. `agent_delegate` is a forbidden tool for all five agents. |
| P-020: User Authority | P-E2E-03 (diff-scoped entry) implements a mandatory user confirmation gate before any test scope is committed to. Full-suite runs and each autonomy-tier selection are user-declared. The skill does not override user decisions about scope, mode, or tier. |
| P-022: No Deception | P-E2E-10 (autonomy-tier declaration) is a first-class P-022 enforcement mechanism. The 0.94 quality threshold is disclosed as a triangulated value, not an empirically optimal one. Functional-correctness metric thresholds are flagged as [SINGLE-STUDY -- LIMITED STATISTICAL POWER on GenIA-E2ETest n=12]. Eval corpus size is disclosed in every quality report. |
| H-04: Active Project Required | Skill operates within a Jerry project context. Test run artifacts are scoped to `skills/e2e-testing/output/{E2E-NNNN}/` within the active project workspace. |
| H-13: Quality Threshold >= 0.92 | Skill internal gate is 0.94, above the SSOT H-13 floor of 0.92. |
| H-14: Creator-Critic-Revision Cycle | e2e-author (creator) / ps-critic (external critic) / revision loop applies to all C2+ test plans. Minimum 3 iterations. e2e-verifier's supervisor-loop escalation ladder implements the same pattern for functional correctness. |
| H-25: SKILL.md exact casing | This file is `skills/e2e-testing/SKILL.md` -- exact case per H-25. |
| H-26: Folder name matches `name` field | Folder `skills/e2e-testing/` matches frontmatter `name: e2e-testing` character-for-character. |
| H-27: No README.md in skill folder | No README.md exists in `skills/e2e-testing/`. This SKILL.md serves the registration role; PLAYBOOK.md serves the operational depth role. |
| H-28: description field compliant | WHAT + WHEN + trigger keywords. Character count: 904. No XML tags. Under 1024 chars. |
| H-29: Full repo-relative paths | All file references in this document use full repo-relative paths from the repository root. No relative paths beginning with `./` or bare filenames without directory prefix. |
| H-30: Registration in CLAUDE.md, AGENTS.md, mandatory-skill-usage.md | See [Registration](#registration) section. All three registrations are required and treated as C3 per AE-002. |
| AE-002: .context/rules/ modification triggers C3 | Registration changes to `CLAUDE.md` and `.context/rules/mandatory-skill-usage.md` are human-gated C3 operations. They require C3 strategy set: H-14 minimum 3 iterations, S-004 pre-mortem, S-012 FMEA, S-013 inversion. |

---

## Evidence Confidence Register

This register consolidates every confidence flag used across the skill and its associated files. It is a P-022 transparency artifact. Listing a flag here does NOT upgrade its evidentiary status -- each flag retains the limitation described in the Meaning column.

| Flag | Applied to | Meaning | Where to find |
|------|-----------|---------|---------------|
| `[SINGLE-STUDY]` | GenIA-E2ETest metrics (execution_recall, element_precision, element_recall, MMR) | Thresholds derived from one peer-reviewed paper with n=12 scenarios; not an industry benchmark and not statistically powered for generalisation | `skills/e2e-testing/validation/validation-strategy.md` §Metrics, `skills/e2e-testing/templates/e2e-validation-check.md`, Quality Gates section of this file |
| `[RT-004 triangulation; not empirically optimal]` | 0.94 skill-internal S-014 quality threshold | Triangulated between SSOT H-13 floor (0.92) and eng-team maximum (0.95); midpoint rounded up; no independent empirical evidence that 0.94 is optimal for this domain | This file frontmatter and footer, every agent governance YAML, `skills/e2e-testing/validation/validation-strategy.md` |
| `[UNVALIDATED -- corpus n<20]` | Runtime verifier verdicts during pre-corpus ADVISORY mode | Skill has not yet seeded an eval corpus of >= 20 scenarios per P-E2E-09; quality guarantees are advisory until that threshold is reached | `skills/e2e-testing/validation/validation-strategy.md`, example `.feature` files in `skills/e2e-testing/examples/` |
| `[eng-architect-derived; NOT sourced from GenIA-E2ETest; no external validation]` | assertion_sensitivity_rate >= 0.70 metric | Novel metric introduced by eng-architect during Phase 3 design; no upstream paper or benchmark defines this metric or its threshold | `skills/e2e-testing/validation/validation-strategy.md` §Metrics, `skills/e2e-testing/agents/e2e-verifier.md` |
| `[VENDOR BLOG -- architectural claim, not independently verified]` | QA Wolf architectural claims (e.g., self-healing, CI-safe batch execution characteristics) | Source is a vendor blog post, not peer-reviewed literature; architectural pattern is plausible but not independently reproduced | `projects/PROJ-017-e2e-testing-skill/orchestration/e2e-skill-build-20260420-001/synthesis/e2e-skill-requirements.md` §8, `lane-innovators.md` in the same synthesis directory |
| `[SKYVERN SELF-REPORTED]` | Skyvern 50% QA-loop reduction and 2.3x PR-success lift figures | Vendor self-reported metrics, not independently reproduced; used as directional evidence only, not as a benchmark target | `projects/PROJ-017-e2e-testing-skill/orchestration/e2e-skill-build-20260420-001/synthesis/e2e-skill-requirements.md` §8, `lane-innovators.md` in the same synthesis directory |
| `[VENDOR CLAIM]` | Quantitative metrics from commercial QA platform marketing materials (general category) | Vendor-sourced figures; cite the specific vendor and claim; do not treat as an established industry benchmark | `projects/PROJ-017-e2e-testing-skill/orchestration/e2e-skill-build-20260420-001/synthesis/e2e-skill-requirements.md` §8 |

---

## Registration

This section documents the registration targets required by H-30. The actual registrations are authored in a dedicated human-gated Phase 4 Step D, treated as C3 per AE-002.

### CLAUDE.md Skills Table Entry

Add to the Skills quick-reference table in `CLAUDE.md`:

| Skill | Purpose |
|-------|---------|
| `/e2e-testing` | E2E browser test generation, execution, and verification for user journeys and agentic flows |

### AGENTS.md Entry

Add all five agents to the agent registry in `AGENTS.md` with file paths and role summaries:

- `skills/e2e-testing/agents/e2e-analyst.md` -- Change-Impact Analyst
- `skills/e2e-testing/agents/e2e-author.md` -- Test Scenario Planner and Gherkin Author
- `skills/e2e-testing/agents/e2e-executor.md` -- Browser Driver and Test Runner
- `skills/e2e-testing/agents/e2e-verifier.md` -- Correctness Validator and Escalation Supervisor
- `skills/e2e-testing/agents/e2e-reporter.md` -- Multi-Level Report Assembler

### mandatory-skill-usage.md Trigger Map Entry

Add to `.context/rules/mandatory-skill-usage.md` Trigger Map:

| Detected Keywords | Skill |
|-------------------|-------|
| e2e test, browser test, user journey, playwright, generate test, agentic flow test, WSTG, end-to-end test, diff scope test | `/e2e-testing` |

Note: `.context/rules/mandatory-skill-usage.md` is inside `.context/rules/` and triggers AE-002 (auto-C3 minimum). The registration commit for this file and `CLAUDE.md` must be a combined C3-grade operation, not a routine file write.

---

## References

| Standard / Source | Relevance | URL |
|-------------------|-----------|-----|
| W3C WebDriver Level 2 | Protocol constraint for browser automation; stale element reference error taxonomy | https://www.w3.org/TR/webdriver2/ |
| ISO/IEC/IEEE 29119-2 | Risk-based test design (P-E2E-01); test strategy specification | https://www.iso.org/standard/79428.html |
| ISO/IEC/IEEE 29119-3 | Test documentation structure (opt-in via RT-001 flag) | https://www.iso.org/standard/79429.html |
| ISTQB Certified Tester Foundation Level (CTFL) | Risk-based prioritisation (P-E2E-01); gTAA four-layer model (P-E2E-07) | https://www.istqb.org/certifications/certified-tester-foundation-level |
| OWASP Web Security Testing Guide (WSTG) v4.2 | WSTG six mandatory categories (P-E2E-08); BUSL as highest-applicability category | https://owasp.org/www-project-web-security-testing-guide/ |
| Cucumber / Gherkin Reference | Declarative scenario format (P-E2E-02); Feature-Rule-Scenario structure | https://cucumber.io/docs/gherkin/reference/ |
| GenIA-E2ETest (Giulini et al.) | Metric formulas (P-E2E-09): element_precision, element_recall, execution_recall, MMR | Peer-reviewed; [SINGLE-STUDY -- LIMITED STATISTICAL POWER on n=12] |

---

## Footer

**Version:** 1.0.0
**Last Updated:** 2026-04-21
**Constitutional Compliance:** Jerry Constitution v1.0
**Quality Threshold:** 0.94 (triangulated -- RT-004; above SSOT H-13 floor of 0.92; not empirically optimal)
**Workflow:** PROJ-017-e2e-testing-skill / e2e-skill-build-20260420-001 Phase 4 Step A
**Phase Gate Upstream:** Gate 3 PASS (skill-architecture.md quality score 0.94)
**SSOT References:** `projects/PROJ-017-e2e-testing-skill/orchestration/e2e-skill-build-20260420-001/synthesis/e2e-skill-requirements.md` (principles), `projects/PROJ-017-e2e-testing-skill/orchestration/e2e-skill-build-20260420-001/design/implementation-plan.md` (file tree, agent roster, H-25..H-30 compliance)
