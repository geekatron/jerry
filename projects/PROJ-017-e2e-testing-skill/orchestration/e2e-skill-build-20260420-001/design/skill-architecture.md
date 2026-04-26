---
agent: eng-architect
phase: "3B"
workflow: e2e-skill-build-20260420-001
project: PROJ-017-e2e-testing-skill
inputs:
  - projects/PROJ-017-e2e-testing-skill/orchestration/e2e-skill-build-20260420-001/design/implementation-plan.md
  - projects/PROJ-017-e2e-testing-skill/orchestration/e2e-skill-build-20260420-001/synthesis/e2e-skill-requirements.md
  - projects/PROJ-017-e2e-testing-skill/orchestration/e2e-skill-build-20260420-001/research/deep-engteam/eng-team-testing-baseline.md
date: 2026-04-21
version: "1.0"
quality_threshold: 0.94
gate_upstream: "Phase 3A eng-lead implementation plan"
---

# Skill Architecture — skills/e2e-testing/

> Eng-architect output for Phase 3B. This document specifies HOW the skill works operationally.
> Every Phase 4 build agent consumes this as the authoritative design reference for their step.
> Gate 3 scores this at 0.94 against C3 strategies (S-007, S-002, S-014, S-004, S-012, S-013).

## Document Sections

| Section | Purpose |
|---------|---------|
| [1. Agent Responsibility Matrix](#1-agent-responsibility-matrix) | Principle ownership table: agent x P-E2E-01..10 with explicit owners |
| [2. Agent Interaction Sequences](#2-agent-interaction-sequences) | Per-agent state read/write, triggers, failure modes, core pipeline diagram |
| [3. Prompt Template Structure](#3-prompt-template-structure) | Section skeleton, placeholders, validation rules for each of 5 templates |
| [4. Validation Check Strategy](#4-validation-check-strategy-architectural-design) | CRITICAL — mechanism, metrics, escalation, orthogonality disclosure |
| [5. State Passing Between Agents](#5-state-passing-between-agents) | Handoff artifact schemas |
| [6. Tool Integration Architecture](#6-tool-integration-architecture) | Playwright MCP, AD-010 degradation, AGPL enforcement |
| [7. Failure Mode Catalogue](#7-failure-mode-catalogue) | Failure x agent x detection x response table |
| [8. Autonomy Tier Architecture](#8-autonomy-tier-architecture) | Tier definitions, selection, defaults, forbidden tiers |
| [9. Security and Governance Design](#9-security-and-governance-design) | Tool allowlist, secrets, exfiltration boundary, STRIDE-lite threat model |
| [10. Cross-Skill Integration Design](#10-cross-skill-integration-design) | Concrete integration seams with 5 sibling skills |
| [11. Acceptance Criteria for Phase 4](#11-acceptance-criteria-for-phase-4-build-agents) | Per-builder checklists |
| [Source References](#source-references) | Design-decision-to-source traceability |

---

## 1. Agent Responsibility Matrix

The matrix below assigns exactly one **owner** to each of the ten principles P-E2E-01 through P-E2E-10. Collaborators and read-only consumers are also named, so Phase 4 build agents know whose Methodology section must cite each principle as primary vs. referenced.

Legend: **OWN** = authoritative for principle enforcement; **COL** = collaborating producer of evidence; **RO** = reads the principle's artifacts but does not produce them; blank = unused.

| Principle | e2e-author | e2e-executor | e2e-verifier | e2e-analyst | e2e-reporter |
|-----------|-----------|--------------|--------------|-------------|--------------|
| P-E2E-01 Risk-First Ordering | COL | | | **OWN** | RO |
| P-E2E-02 Declarative Gherkin + `@basis:` | **OWN** | | COL (lint check) | | RO |
| P-E2E-03 Diff-Scoped Entry | COL | | | **OWN** | RO |
| P-E2E-04 Planner-Executor-Verifier + Supervisor Loop | COL | COL | **OWN** | | RO |
| P-E2E-05 Dual Execution Mode (codegen/explorer) | COL (mode-declared-in-plan) | **OWN** | RO | | RO |
| P-E2E-06 Live-DOM-Grounded Locators | | **OWN** | COL (sensitivity check) | | |
| P-E2E-07 gTAA Layer Architecture | | **OWN** (Adaptation layer exclusivity) | COL (import-graph audit) | | |
| P-E2E-08 WSTG Security Coverage | **OWN** | | COL (coverage verification) | COL (gap identification) | RO |
| P-E2E-09 Published Quality Gate + Metrics | | | **OWN** | COL (corpus maintenance) | RO |
| P-E2E-10 Autonomy-Tier Declaration | COL (declares at plan creation) | | COL (emits in verdict) | | **OWN** (enforces L0 presence) |

**Ownership-assignment rationale (Phase 4 builders cite these in agent Methodology sections):**

- **e2e-analyst owns P-E2E-01 and P-E2E-03.** Risk classification is the output of change-impact analysis; both principles are analyst deliverables, not author deliverables. e2e-author consumes the classification; it does not produce it (implementation-plan Section 2). This is a departure from the requirements §4 text which lists P-E2E-01 and P-E2E-03 as author principles — eng-architect resolves the ambiguity here by pinning ownership to analyst because **principle ownership = production, not consumption**. Where analyst is absent, e2e-author inherits ownership as a fallback (see Section 2.5 failure mode).

- **e2e-verifier owns P-E2E-04.** The principle's testable assertion is "Validator escalates to Planner." The enforcement point is the Validator's behaviour, not the Planner's or Actor's (requirements §2 P-E2E-04 testable assertion).

- **e2e-executor owns P-E2E-05, P-E2E-06, P-E2E-07.** All three are browser-interaction-layer principles. No other agent touches the browser (implementation-plan Section 2 — only executor holds Playwright MCP tools).

- **e2e-author owns P-E2E-02 and P-E2E-08.** Both are authoring-time principles (Gherkin style, WSTG tag generation). The verifier checks them but does not produce them.

- **e2e-verifier owns P-E2E-09.** The published quality gate is the verifier's measurement and threshold-comparison output. e2e-analyst maintains the eval corpus (a COL role) but does not compute the metric verdict.

- **e2e-reporter owns P-E2E-10.** The autonomy-tier declaration is an L0 output-format requirement. The reporter is the L0 owner. Author and verifier emit `autonomy_tier` as a COL input, but the reporter enforces its presence in the surfaced L0 output (see Section 8 for the dual-enforcement safety net for the three-agent-minimum invocation path).

---

## 2. Agent Interaction Sequences

### 2.1 Core Pipeline (ASCII sequence)

```
User                              e2e-analyst       e2e-author       e2e-executor      e2e-verifier      e2e-reporter
 |                                    |                  |                  |                  |                  |
 | /e2e-testing generate-tests       |                  |                  |                  |                  |
 |---- git-diff, --risk, --mode ---->|                  |                  |                  |                  |
 |                                    |                  |                  |                  |                  |
 |                                    | scope-document.json                 |                  |                  |
 |                                    |----------------->|                  |                  |                  |
 | <-- [P-E2E-03 gate] confirm scope -|                  |                  |                  |                  |
 |-------- confirmation ------------>|                  |                  |                  |                  |
 |                                    |                  |                  |                  |                  |
 |                                    |                  | author-plan.json + Gherkin.feature  |                  |
 |                                    |                  |----------------->|                  |                  |
 |                                    |                  |                  | [browser_snapshot + execution]      |
 |                                    |                  |                  |                  |                  |
 |                                    |                  |                  | executor-trace.json + artifacts     |
 |                                    |                  |                  |----------------->|                  |
 |                                    |                  |                  |                  | [validation 6-step]
 |                                    |                  |                  |                  |                  |
 |                                    |                  |                  |                  |--- /adversary -->|
 |                                    |                  |                  |                  |    adv-scorer    |
 |                                    |                  |                  |                  |<---- score ------|
 |                                    |                  |                  |                  |                  |
 |                                    |                  |<---- FAIL escalation (via verifier->author ONLY) ------|
 |                                    |                  | [replan loop; max 3 iterations per H-14]               |
 |                                    |                  |                  |                  |                  |
 |                                    |                  |                  |                  | PASS verdict.json|
 |                                    |                  |                  |                  |----------------->|
 |                                    |                  |                  |                  |                  | L0/L1/L2 assembly
 |                                    |                  |                  |                  |                  |
 | <-------------- L0 report (with autonomy_tier, functional-score, S-014 score) ----------------------------------|
```

**Handoff artifacts named on arrows (see Section 5 for full schemas):**
1. `scope-document.json` (analyst -> author)
2. `author-plan.json` + `{scenario}.feature` (author -> executor)
3. `executor-trace.json` + `screenshots/` + `dom-snapshots/` (executor -> verifier)
4. `failure-diagnostic.json` (verifier -> author, on FAIL)
5. `verifier-verdict.json` (verifier -> reporter)
6. `report-L0.md` + `report-L1.md` + `report-L2.md` (reporter -> user)

### 2.2 e2e-author (Planner)

| Aspect | Specification |
|--------|--------------|
| **State read on invocation** | `scope-document.json` from analyst (if present); OR raw `git diff` text; existing `.feature` inventory; `e2e-governance-config.yaml` (authoritative run parameters); on escalation: `failure-diagnostic.json` from verifier |
| **State written** | `author-plan.json` (structured scenario decomposition), `{scenario}.feature` (Gherkin), `.spec.ts` scaffold in codegen mode, `author-rationale.md` for reporter |
| **Invocation triggers** | (1) User slash command `/e2e-testing generate-tests`; (2) upstream analyst completion; (3) verifier FAIL escalation (replanning trigger per P-E2E-04); (4) manual invocation with `--basis` and `--risk` parameters |
| **Failure modes** | *Missing diff input* -> prompts user (P-E2E-03 HARD requirement); *analyst absent* -> author performs change-impact analysis itself and flags output as "analyst-absent mode" for reporter; *LLM refuses to generate* (content policy) -> emits `refusal.json` citing the specific policy and escalates to user (not to executor); *replanning exhausts 3 iterations per H-14* -> triggers AE-006 escalation |
| **Principles invoked** | P-E2E-02 (own), P-E2E-08 (own); cites P-E2E-01, P-E2E-03 (consume); P-E2E-10 (collaborate — declares tier in plan header) |

### 2.3 e2e-executor (Actor)

| Aspect | Specification |
|--------|--------------|
| **State read on invocation** | `author-plan.json`; `{scenario}.feature` or `.spec.ts` from author; `e2e-governance-config.yaml` (browser choice, viewport, timeouts); **no** escalation artifacts (executor never receives escalation — it is the actor, not the planner) |
| **State written** | `executor-trace.json` (per-step outcomes), `screenshots/{step}-{status}.png`, `dom-snapshots/{step}.json` (browser_snapshot outputs preserved for verifier), `.spec.ts` committed artifact (codegen mode), `browser-errors.json` (WebDriver error codes) |
| **Invocation triggers** | (1) e2e-author signals plan ready; (2) manual CLI invocation for replay of an existing `.spec.ts` with trace collection |
| **Failure modes** | *Playwright MCP unreachable* -> AD-010 degradation to Level 1 (emit test specifications without execution); *SUT unreachable* -> emits `sut-unreachable.json` diagnostic with retry-exhaustion note, no replanning triggered (not verifier's domain); *tool allowlist violated by LLM attempt* -> governance YAML blocks call, logs to `allowlist-violation.json`; *browser_snapshot returns empty tree* (a11y-hostile SUT) -> emits diagnostic; verifier may escalate to author for vision-LLM fallback declaration |
| **Principles invoked** | P-E2E-05, P-E2E-06, P-E2E-07 (all own) |

### 2.4 e2e-verifier (Validator)

| Aspect | Specification |
|--------|--------------|
| **State read on invocation** | `executor-trace.json`, `{scenario}.feature`, `author-plan.json`, `screenshots/`, `dom-snapshots/`, `browser-errors.json`; existing eval corpus for metric baseline comparison |
| **State written** | `verifier-verdict.json` (PASS/REVISE/FAIL + metrics), `assertion-inventory.json` (VERIFIED/RAN-ONLY/ABSENT classification per assertion), `failure-diagnostic.json` (on FAIL, routed to author), `adv-scorer-result.json` (S-014 process score), `metrics-snapshot.json` (execution_recall, element_precision, MMR persisted for eval corpus) |
| **Invocation triggers** | (1) executor signals trace ready; (2) verifier re-run triggered after author replanning; (3) manual invocation for historical verdict replay against updated corpus |
| **Failure modes** | *Trace malformed or absent* -> emits `trace-invalid.json`, escalates to author (executor failure is author's problem because executor only responds to author-directed plans); *adv-scorer fails* (MCP unavailable) -> emits warning and proceeds with functional-correctness verdict only, flagging "S-014 score UNAVAILABLE" per AD-010 Level 1 behaviour; *>=3 consecutive FAIL verdicts* -> AE-006 escalation per quality-enforcement.md |
| **Principles invoked** | P-E2E-04, P-E2E-09 (both own); cites P-E2E-02 (declarative lint), P-E2E-06 (locator sensitivity) as COL checks |

### 2.5 e2e-analyst (Optional but Recommended)

| Aspect | Specification |
|--------|--------------|
| **State read on invocation** | `git diff` text, `.feature` file inventory (glob), `wstg-coverage-history.json` (prior coverage state), optional call-graph JSON |
| **State written** | `scope-document.json` (prioritised flow list with risk classifications), `coverage-gap-report.json`, eval corpus entries (`eval-corpus/scenario-NNNN.json`) |
| **Invocation triggers** | (1) User command `/e2e-testing scope`; (2) upstream of author pipeline invocation (auto-triggered if `--diff` is provided without `--full-suite`) |
| **Failure modes** | *Diff empty* -> emits `no-changes-detected.json`; does not proceed (P-E2E-03 HARD requirement — no silent full-suite fallback); *call-graph tool unavailable* (e.g., `npx madge` fails) -> AD-010 Level 1 fallback: semantic similarity heuristic on filename + content only, flags output as "call-graph absent"; *flow adjacency ambiguous* -> emits options to user via AskUserQuestion pattern |
| **Principles invoked** | P-E2E-01, P-E2E-03 (both own), P-E2E-09 (COL — corpus maintenance) |

### 2.6 e2e-reporter (Optional but Recommended)

| Aspect | Specification |
|--------|--------------|
| **State read on invocation** | All upstream artifacts: `author-plan.json`, `author-rationale.md`, `executor-trace.json`, `verifier-verdict.json`, `assertion-inventory.json`, `coverage-gap-report.json`, `metrics-snapshot.json`, `adv-scorer-result.json` |
| **State written** | `report-L0.md` (executive — GO/NO-GO, autonomy_tier, headline metrics), `report-L1.md` (per-scenario pass/fail table, WSTG coverage matrix, quality metric grid, WebDriver error classification), `report-L2.md` (coverage gap analysis, threshold trend, maintenance recommendations, eval corpus delta) |
| **Invocation triggers** | (1) verifier signals PASS (or FAIL-but-report-requested via `--always-report`); (2) manual invocation after historical test run for re-assembly |
| **Failure modes** | *Missing autonomy_tier field in upstream artifacts* -> HALT with P-022 violation notice; emits `p022-enforcement-halt.json`; user must supply tier before report is produced (see Section 8 dual-enforcement safety net); *partial upstream artifacts* -> assembles report with "PARTIAL" marker and lists absent inputs in L0 |
| **Principles invoked** | P-E2E-10 (own); cites L0/L1/L2 output contract (eng-team baseline §7.3) |

---

## 3. Prompt Template Structure

Each template below specifies its section skeleton, placeholder conventions, consumer/producer agents, and validation rules that Phase 4 Step B (eng-qa) must satisfy.

### 3.1 `templates/e2e-test-generation.md`

**Producer:** eng-qa writes the template. **Consumer:** e2e-author invokes the template at scenario-authoring time.

**Section skeleton:**
1. Frontmatter placeholder block (`{{TESTRUN_ID}}`, `{{SUT_URL}}`, `{{CRITICALITY}}`, `{{AUTONOMY_TIER}}`, `{{EXECUTION_MODE}}`)
2. Role framing: "You are e2e-author in test-generation mode"
3. Constitutional reference injection (P-003, P-020, P-022)
4. Risk classification block (MUST be populated before any Gherkin step)
5. Feature/Rule decomposition instruction (produce tree first, steps later)
6. Gherkin authoring section with declarative-style enforcement
7. `@basis:` tag population rule
8. WSTG mandatory-six-categories generator section
9. Self-review checklist (H-15)
10. Persistence instruction (P-002)

**Placeholder conventions:**
- `{{UPPER_SNAKE}}` for scalar values (e.g., `{{AUTONOMY_TIER}}`, `{{SUT_URL}}`)
- `{{LIST_*}}` for lists (e.g., `{{LIST_BASIS_REFS}}`)
- `{{BLOCK_*}}` for multi-line prose blocks (e.g., `{{BLOCK_SCOPE_DOC}}`)

**Parameter defaults (from e2e-governance-config.yaml):**
- `{{EXECUTION_MODE}}` defaults to `codegen`
- `{{AUTONOMY_TIER}}` defaults to `SUPERVISED` (conservative — Section 8)
- `{{CRITICALITY}}` defaults to `C2`
- `{{ISO29119_ARTIFACTS}}` defaults to `false`

**Validation rules for populated template (eng-qa must encode these in the linter for Phase 4 Step B):**
- Every scenario MUST have a Given-When-Then clause (P-E2E-02).
- Every scenario MUST include a `@basis:` tag with a non-empty value.
- No `When` step may contain UI verbs (`click`, `type`, `enter`, `navigate to`, `fill in`, `select`) — P-E2E-02 linting rule.
- `risk_level` and `criticality` fields MUST be present before any `Scenario:` keyword.
- For any feature involving authentication or sensitive data, at least one WSTG-tagged scenario per mandatory category MUST be present (P-E2E-08).

### 3.2 `templates/e2e-agentic-flow.md`

**Producer:** eng-qa. **Consumer:** e2e-author (agentic-flow authoring mode) and e2e-verifier (trajectory validation).

**Section skeleton:**
1. Frontmatter: `{{AGENT_UNDER_TEST}}`, `{{SKILL_NAME}}`, `{{AUTONOMY_TIER}}`, `{{DIVERGENCE_TOLERANCE}}`
2. Role framing: "You are e2e-author in agentic-flow mode"
3. Trajectory decomposition: expected tool-call sequence with intermediate state predicates
4. Non-determinism budget specification
5. Gherkin extension syntax block (resolves OQ-E2E-001; depends on SKILL.md Phase 4 Step A resolution)
6. Tool-call schema validation assertions
7. Golden-transcript generation (codegen mode)
8. Self-review checklist (H-15)
9. Persistence instruction (P-002)

**Placeholder conventions:** Same as 3.1 plus `{{TOOL_CALLS_EXPECTED}}` as an ordered list of `(tool_name, json_schema, position_constraint)`.

**Parameter defaults:**
- `{{DIVERGENCE_TOLERANCE}}` defaults to `strict` (no tool-ordering variation permitted); relaxation is explicit opt-in.
- `{{EXECUTION_MODE}}` defaults to `codegen` (golden transcript).

**Validation rules:**
- Every `When an agentic actor...` clause MUST have at least one trajectory-level `Then` assertion (not just final-state).
- Tool-call schemas MUST be JSON-parseable.
- Negative assertions (`Then the agent did not call X`) MUST include rationale citing a P-E2E-08 category where applicable.

### 3.3 `templates/e2e-validation-check.md`

**Producer:** eng-qa. **Consumer:** e2e-verifier. **This is the most architecturally load-bearing template — see Section 4.**

**Section skeleton:**
1. Frontmatter: `{{TRACE_PATH}}`, `{{PLAN_PATH}}`, `{{CORPUS_PATH}}`, `{{THRESHOLD_QUALITY}}`
2. Role framing: "You are e2e-verifier in validation mode"
3. Six-step validation procedure (Section 4.1 of this document — must be encoded verbatim in the template)
4. Assertion sensitivity classification rubric (VERIFIED / RAN-ONLY / ABSENT)
5. Metric computation formulas (from P-E2E-09)
6. Verdict decision tree (PASS / REVISE / FAIL with threshold comparison)
7. Escalation payload structure (for FAIL verdicts, routed to e2e-author)
8. Orthogonality disclosure block (S-014 vs functional correctness — must be emitted in verdict)
9. Self-review checklist (H-15) and S-014 self-score invocation
10. Persistence instruction (P-002) — both `verifier-verdict.json` AND `adv-scorer-result.json`

**Placeholder conventions:**
- `{{THRESHOLD_*}}` for numeric thresholds (`{{THRESHOLD_EXECUTION_RECALL}}`, `{{THRESHOLD_ELEMENT_PRECISION}}`, `{{THRESHOLD_MMR}}`, `{{THRESHOLD_QUALITY}}`)
- All thresholds source from `e2e-governance-config.yaml`, not hardcoded in the template.

**Validation rules:**
- The template MUST emit both scores as distinct fields — never averaged (Section 4.4 orthogonality requirement).
- Every assertion in the trace MUST be classified (no assertion left unclassified).
- FAIL verdicts MUST include a `replan_recommendation` field for author consumption.

### 3.4 `templates/e2e-diff-scope.md`

**Producer:** eng-qa. **Consumer:** e2e-analyst (primary), e2e-author (fallback when analyst absent).

**Section skeleton:**
1. Frontmatter: `{{GIT_DIFF_PATH}}`, `{{FEATURE_INVENTORY_GLOB}}`, `{{WSTG_COVERAGE_PATH}}`
2. Role framing: "You are e2e-analyst in scope-analysis mode"
3. Changed-file classification (UI | API | business logic | infra | test)
4. Flow adjacency mapping
5. Coverage gap identification
6. WSTG gap check against six mandatory categories
7. Prioritisation by `risk_level × change_proximity`
8. Confirmation-prompt emission (P-E2E-03 HARD — no auto-full-suite)
9. Persistence instruction (P-002)

**Placeholder conventions:** Same as prior templates.

**Parameter defaults:**
- `{{FULL_SUITE_FLAG}}` defaults to `false` (opt-in only).
- `{{CALL_GRAPH_REQUIRED}}` defaults to `false` (semantic heuristic if absent).

**Validation rules:**
- If `{{FULL_SUITE_FLAG}}` is false AND no diff is present, template MUST emit an interactive prompt, not a scope document.
- Every changed file MUST receive a classification (no file unclassified).
- Output MUST include `wstg_gap_categories: []` field, even if empty.

### 3.5 `templates/e2e-governance-config.md`

**Producer:** eng-qa. **Consumer:** all agents at invocation (YAML parsed and passed to every prompt).

**Section skeleton:**
1. Role framing: "This template produces a validated per-run governance YAML block"
2. Default values block (from implementation-plan §3)
3. Override declaration section (user can override any default with justification)
4. Field validation rules (regex, enum, range per field)
5. Persistence instruction: write to `output/{testrun-id}/governance-config.yaml`

**Placeholder conventions:** YAML field names are the "placeholders" — template emits a parameterised YAML block with user-supplied or default values.

**Validation rules (enforced at governance-config load time by every agent):**
- `execution_mode` MUST be `codegen` or `explorer`.
- `autonomy_tier` MUST be one of `AUTONOMOUS | SUPERVISED | MANAGED-EQUIVALENT`.
- `testrun_id_format` MUST match `^E2E-\d{4}$`.
- `quality_threshold` MUST be >= 0.92 (SSOT floor) and <= 0.99 (upper-bound sanity check).
- `wstg_mandatory_categories` MUST include at minimum the six defaults (ATHN, ATHZ, SESS, INPV, BUSL, APIT).

---

## 4. Validation Check Strategy — Architectural Design

This section operationalises requirements §6. It is the architectural heart of the skill. All four sub-sections are mandatory; Phase 4 Step B (eng-qa) must instantiate each sub-section verbatim in `validation/validation-strategy.md`.

### 4.1 Mechanism — Six-Step Decision Procedure

**Input contract** (what e2e-verifier receives):
- `execution_trace.json` — from e2e-executor, containing per-step pass/fail, WebDriver error codes, timing, DOM-snapshot references
- `author-plan.json` — from e2e-author, containing the original scenario intent, expected assertions, expected outcomes per step, `@basis:` tag references
- `{scenario}.feature` file — Gherkin source
- `screenshots/*.png` and `dom-snapshots/*.json` — visual and structural evidence
- `governance-config.yaml` — thresholds and mode declarations

**Step-by-step decision procedure** (must be encoded verbatim in `e2e-validation-check.md` template per Section 3.3):

**Step 1: Parse Gherkin feature -> extract all `Then` assertion statements.**
For each scenario, enumerate every assertion and map it to the `@basis:` tag's stated purpose. Outcome: an `assertion_list` with one entry per `Then` clause.

**Step 2: Map each assertion to a P-E2E principle.**
Is the assertion a security check (P-E2E-08)? A functional check (P-E2E-02)? A trajectory check (agentic — P-E2E-06 boundary)? This mapping informs which sensitivity rubric applies.

**Step 3: Score each assertion on sensitivity (VERIFIED / RAN-ONLY / ABSENT).**
Apply the decision criteria from requirements §6.3 Step 2:
- Navigation-only (URL check without state content) -> `RAN-ONLY`
- Element visibility without content -> `RAN-ONLY` for content-dependent, `VERIFIED` for existence
- Visibility + content/text match -> `VERIFIED`
- Absence of sensitive data -> `VERIFIED` for isolation
- No assertion for stated purpose -> `ABSENT`

The sensitivity rubric must include at least one worked example per classification (see Risk 3 in implementation plan — examples/auth-journey.feature is the calibration reference).

**Step 4: Compute coverage across five dimensions.**
Verify the test suite covers happy path, failure path, boundary, security, and agentic-divergence (requirements §6.2). Coverage failure on a first-tier dimension is a REVISE or FAIL trigger depending on feature-under-test classification.

**Step 5: Compute metrics per P-E2E-09 formulas.**
- `element_precision = C/G` (correctly generated locators / total generated locators)
- `element_recall = C/E` (correct locators / expected locators)
- `execution_precision = CS/GS` (generated steps that ran / total generated steps)
- `execution_recall = CS/ES` (generated steps that ran / expected steps)
- `manual_modification_rate = (steps_requiring_human_edit) / (total_generated_steps)`

**Step 6: Emit verdict.**
Apply decision tree:
- **PASS:** All thresholds met, no ABSENT, <30% RAN-ONLY
- **REVISE:** Any metric between threshold and (threshold - 0.05); OR 30-50% RAN-ONLY
- **FAIL:** Any metric below (threshold - 0.05); OR >50% RAN-ONLY; OR any ABSENT assertion

**Output contract** (what the verifier returns):

```json
{
  "testrun_id": "E2E-0001",
  "scenario": "auth-journey/login-happy-path",
  "verdict": "PASS | REVISE | FAIL",
  "functional_correctness": {
    "element_precision": 0.78,
    "element_recall": 0.82,
    "execution_precision": 0.95,
    "execution_recall": 0.88,
    "manual_modification_rate": 0.09,
    "thresholds_met": true
  },
  "assertion_inventory": [
    {"step": "Then I see the dashboard", "class": "RAN-ONLY", "rationale": "..."},
    {"step": "Then I do not see another user's data", "class": "VERIFIED", "rationale": "..."}
  ],
  "coverage_dimensions": {
    "happy_path": true,
    "failure_path": true,
    "boundary": false,
    "security": true,
    "agentic_divergence": "N/A"
  },
  "process_quality_score_s014": 0.945,
  "process_quality_thresholds_met": true,
  "failure_category": null,
  "webdriver_error_class": null,
  "escalation_to": null,
  "replan_recommendation": null,
  "autonomy_tier": "SUPERVISED",
  "orthogonality_note": "process_quality_score_s014 and functional_correctness are measured independently; neither substitutes for the other."
}
```

### 4.2 Metrics — Concrete Thresholds

All thresholds source from `e2e-governance-config.yaml`, not hardcoded in agent definitions. Initial-release values (per P-E2E-09 and requirements §6.4):

| Metric | Threshold | Source | Flag |
|--------|-----------|--------|------|
| `execution_recall` | >= 0.80 | P-E2E-09 initial release | [SINGLE-STUDY — based on GenIA-E2ETest n=12] |
| `element_precision` | >= 0.70 | P-E2E-09 initial release | [SINGLE-STUDY] |
| `element_recall` | >= 0.70 | P-E2E-09 initial release | [SINGLE-STUDY] |
| `manual_modification_rate` | <= 0.15 | P-E2E-09 initial release | [SINGLE-STUDY] |
| WSTG category coverage | 6/6 | P-E2E-08 (eng-architect judgment) | mandatory at first-tier |
| Assertion sensitivity | <30% RAN-ONLY | eng-architect derivation from requirements §6.3 | new metric — not sourced from GenIA-E2ETest |
| S-014 process score | >= 0.94 | RT-004 triangulation | triangulated, not empirically optimal |

**New metric introduced by this architecture:** `assertion_sensitivity_rate` = (count VERIFIED) / (total assertions). Threshold: >= 0.70. This is an eng-architect-introduced metric (P-022 disclosure: not sourced from requirements; derived from §6.3 sensitivity rubric as a measurable summary). It complements execution_recall (which measures "did it run") by measuring "did it verify."

### 4.3 Escalation

When e2e-verifier emits FAIL:

1. **First failure** -> Return to e2e-author with `failure-diagnostic.json` containing: failure category (from the six-category flake taxonomy: selector/timing/runtime/data/visual/interaction); WebDriver error class; relevant DOM snapshot at failure point; replan recommendation. Author replans and re-submits plan. This is the H-14 creator-critic-revision cycle (minimum 3 iterations).

2. **Second failure** (same scenario, second iteration) -> Return to e2e-author with strengthened diagnostic and cite requirements §6.1 three-level escalation (navigation -> identity -> isolation) for missing assertion levels. Author must add assertions, not merely adjust selectors.

3. **Third failure** -> AE-006 escalation (mandatory human escalation per quality-enforcement.md). Reporter emits report with FAIL verdict and AE-006 flag.

**Relationship to adv-scorer:** adv-scorer is a skill-internal gate that runs in parallel with the functional-correctness gate (not before or after). The verifier invokes `/adversary (adv-scorer)` per H-17 for C2+ deliverables. The S-014 score and the functional-correctness metrics are computed in the same verdict step but emitted as orthogonal fields (Section 4.4). When e2e-testing is invoked **externally** by `/adversary` (e.g., user runs `/adversary score-this-deliverable` against an e2e artifact), adv-scorer governs the scoring; the verifier's internal gate is bypassed. **Cross-skill invocation path priority is documented in Section 10.**

**Max iterations before AE-006:** 3 iterations (H-14 minimum). The `e2e-governance-config.yaml` `retry_count` field is for browser-level retries in codegen mode (unrelated to the replanning loop — that field stays at 0 for determinism).

### 4.4 Orthogonality Disclosure

**Architectural statement (MUST be included verbatim in e2e-verifier.md identity block and in every verdict.json output):**

> The S-014 six-dimension process quality score measures whether the skill followed its methodology (document completeness, internal consistency, methodological rigor, evidence quality, actionability, traceability). The GenIA-E2ETest functional-correctness metrics (execution_recall, element_precision, MMR, assertion_sensitivity_rate) measure whether the generated test actually verifies application correctness. These are orthogonal concerns. A deliverable can score 0.96 on S-014 and 0.65 on execution_recall (well-documented but fragile); or 0.95 on execution_recall and 0.88 on S-014 (reliable but undocumented). Both are failures. Neither score substitutes for the other. The e2e-verifier MUST emit both scores as distinct fields and MUST NOT average or combine them for a single pass/fail signal.

This mirrors requirements §6.5 and eng-team baseline §4 (eng-reviewer S-014 orthogonality to functional correctness).

---

## 5. State Passing Between Agents

All inter-agent state is persisted to disk (P-002). In-memory passing is forbidden — this is a P-E2E-07 requirement (persistence enables replay support and AD-010 Level 1 degradation). Every handoff artifact has a schema below.

### 5.1 analyst -> author: `scope-document.json`

```json
{
  "testrun_id": "E2E-0001",
  "diff_ref": "HEAD~1..HEAD",
  "changed_files": [
    {"path": "src/auth/login.ts", "classification": "business_logic"},
    {"path": "src/pages/LoginPage.tsx", "classification": "ui_component"}
  ],
  "flow_adjacency": [
    {"flow": "auth-journey/login", "adjacent_files": ["src/auth/login.ts", "src/pages/LoginPage.tsx"], "proximity_score": 0.95}
  ],
  "coverage_gaps": [
    {"flow": "auth-journey/password-reset", "reason": "no existing .feature"}
  ],
  "wstg_gaps": ["BUSL"],
  "prioritised_scope": [
    {"flow": "auth-journey/login", "risk_level": "HIGH", "criticality": "C2", "priority_rank": 1}
  ],
  "full_suite_requested": false,
  "confirmation_received": true
}
```

### 5.2 author -> executor: `author-plan.json` + `{scenario}.feature`

**`author-plan.json`:**
```json
{
  "testrun_id": "E2E-0001",
  "scenario_id": "auth-journey/login-happy-path",
  "risk_level": "HIGH",
  "criticality": "C2",
  "execution_mode": "codegen",
  "autonomy_tier": "SUPERVISED",
  "basis_refs": ["STORY-042", "WSTG-v42-ATHN-01"],
  "scenario_steps": [
    {"keyword": "Given", "text": "a registered user with valid credentials", "expected_state": {...}},
    {"keyword": "When", "text": "the user submits the login form", "expected_state": {...}},
    {"keyword": "Then", "text": "the user is redirected to the dashboard", "expected_sensitivity": "VERIFIED"}
  ],
  "expected_locators": [
    {"selector": "[data-testid=login-email]", "role": "email_input"}
  ]
}
```

**`{scenario}.feature`:** Standard Gherkin with `@basis:`, `@risk:`, `@wstg:` tags.

### 5.3 executor -> verifier: `executor-trace.json` + artifacts

```json
{
  "testrun_id": "E2E-0001",
  "scenario_id": "auth-journey/login-happy-path",
  "execution_mode": "codegen",
  "browser": "chromium",
  "steps": [
    {
      "index": 0,
      "step_text": "Given a registered user...",
      "status": "pass",
      "duration_ms": 420,
      "dom_snapshot_ref": "dom-snapshots/step-00.json",
      "screenshot_ref": null,
      "webdriver_error": null
    },
    {
      "index": 1,
      "step_text": "When the user submits the login form",
      "status": "pass",
      "generated_locator": "[data-testid=login-email]",
      "manual_modification": false
    },
    {
      "index": 2,
      "step_text": "Then the user is redirected to the dashboard",
      "status": "pass",
      "assertion_executed": "expect(page.url()).toContain('/dashboard')"
    }
  ],
  "raw_counts": {
    "C": 8, "G": 10, "E": 9, "CS": 9, "GS": 10, "ES": 10
  },
  "manual_modifications": 1,
  "artifacts": {
    "spec_ts_path": "output/E2E-0001/auth-journey-login.spec.ts",
    "screenshots_dir": "output/E2E-0001/screenshots/",
    "dom_snapshots_dir": "output/E2E-0001/dom-snapshots/"
  }
}
```

### 5.4 verifier -> reporter: `verifier-verdict.json`

Schema in Section 4.1 output contract (above).

### 5.5 verifier -> author (escalation only): `failure-diagnostic.json`

```json
{
  "testrun_id": "E2E-0001",
  "scenario_id": "auth-journey/login-happy-path",
  "iteration": 2,
  "failure_category": "data",
  "webdriver_error_class": "no such element",
  "metrics_at_failure": {...},
  "dom_snapshot_ref": "dom-snapshots/step-01-failure.json",
  "replan_recommendation": "Add live browser_snapshot before email-locator generation. Use data-testid anchor rather than text match. Add negative assertion on alice@example.com.",
  "max_iterations_remaining": 1
}
```

### 5.6 reporter -> user: `report-L0.md` / `report-L1.md` / `report-L2.md`

Multi-level markdown outputs. `report-L0.md` MUST begin with:

```markdown
# E2E-0001 — auth-journey/login-happy-path

**Verdict:** PASS
**Autonomy Tier:** SUPERVISED — human reviewed each generated scenario before execution.
**Functional Correctness:** execution_recall 0.88, element_precision 0.78, MMR 0.09
**Process Quality (S-014):** 0.945

(Both scores are orthogonal — see Section 4.4.)
```

---

## 6. Tool Integration Architecture

### 6.1 Playwright MCP Integration

**Which agent uses it:** **e2e-executor only.** No other agent has Playwright MCP tools in its allowlist (implementation-plan Section 2).

**Which tools (core-8 + 2 file ops = 10):**
```
mcp__playwright__browser_snapshot
mcp__playwright__browser_click
mcp__playwright__browser_type
mcp__playwright__browser_navigate
mcp__playwright__browser_verify_element_visible
mcp__playwright__browser_take_screenshot
mcp__playwright__browser_wait_for
mcp__playwright__browser_evaluate
file_write
file_read
```

**MCP server invocation:**
- The `@playwright/mcp` MCP server is registered in the agent's `mcpServers` frontmatter field with a pinned version (per implementation-plan Risk 1 mitigation).
- The SKILL.md Phase 4 Step A product specifies the exact pinned version; Phase 4 Step C (eng-architect authoring agents) propagates the version to `e2e-executor.governance.yaml` `mcp_servers.playwright.version`.
- Launch is managed by the Claude Code MCP runtime; no manual server start required.

**Fallback if unavailable:** AD-010 Level 1 degradation (Section 6.3).

### 6.2 Browser Control as Security Boundary

The skill's tool allowlist enforces a security boundary: **only e2e-executor may touch a browser.** This is architecturally significant because:

1. A browser-controlling agent has direct access to the SUT, including any secrets the SUT handles (session tokens, PII, credentials).
2. Separating the planner (e2e-author) from the actor (e2e-executor) prevents plan-level prompt injection from escalating to browser actions without passing through the executor's allowlist.
3. The analyst, verifier, and reporter are deliberately file-only — they cannot be tricked by a malicious trace file into driving a browser.

This boundary is enforced at three layers:
- **Governance YAML** `capabilities.allowed_tools` — file-level allowlist.
- **Agent MD `## Tool Integration`** section — identity-level disclosure.
- **Runtime tool dispatcher** — rejects calls outside allowlist (Claude Code's built-in enforcement).

### 6.3 AD-010 Three-Level Degradation

Adopted from eng-team baseline §7.2. Explicitly named levels:

| Level | Name | Tool availability | Skill behaviour |
|-------|------|-------------------|-----------------|
| **Level 0** | Full Tools | Playwright MCP available + file ops + shell (analyst only) | Full pipeline: real browser driven against real SUT; live traces; functional + process quality both scored |
| **Level 1** | Partial Tools | Playwright MCP unavailable; file ops only | e2e-executor downgrades to plan-validation-only mode: emits `.spec.ts` scaffold and a dry-run trace (no browser actions); verifier computes process quality (S-014) but cannot compute functional metrics; verdict marked "FUNCTIONAL METRICS UNAVAILABLE" |
| **Level 2** | Standalone | No MCP, no shell, no web; pure methodology | Skill emits templates + Gherkin scaffolds + page-object stubs only. All outputs flagged "requires validation against live SUT." Verifier emits advisory-only verdict. e2e-analyst falls back to semantic-similarity heuristic (no call-graph). |

Detection: each agent checks tool availability at invocation and emits a `degradation_level` field in its L0 output. Reporter aggregates to top-level L0 degradation banner.

### 6.4 AGPL-3.0 Boundary Enforcement

Mechanism for `no_skyvern_source_code` governance guardrail:

1. **Declaration layer:** Every agent governance YAML includes `output_filtering: - no_skyvern_source_code`.
2. **Prompt-level guardrail:** Every agent MD identity section includes: "Skyvern's AGPL-3.0 applies to source code and derived works; architectural blueprints and design principles are not covered. You may adopt pattern and role decomposition; you may not copy verbatim prompt text from Skyvern's open-source repo."
3. **Verification:** e2e-verifier includes an AGPL check in its post-completion checklist — grep generated artifacts for distinctive Skyvern prompt phrases (PLAYBOOK.md maintains a small reference list). If a match is found, verifier emits an AGPL boundary alert and escalates to eng-lead.
4. **Build-time reminder:** PLAYBOOK.md includes the boundary note from requirements §8 verbatim; Phase 4 builders receive it as context.

This is a best-effort enforcement. Perfect detection is out of scope (P-022 honesty flag); the mechanism is a deterrent plus a review gate, not a provable boundary.

---

## 7. Failure Mode Catalogue

Failure mode x agent x detection mechanism x response. Phase 4 Step C (eng-architect agents) must reference this table in each agent's "Failure Modes" methodology section.

| Failure Mode | Primary Agent | Detection | Response |
|--------------|---------------|-----------|----------|
| Playwright MCP unavailable | e2e-executor | MCP server init timeout or tool call 404 | AD-010 Level 1 degradation; emit plan-validation-only output; flag `degradation_level: 1` |
| SUT unreachable (network, auth fail) | e2e-executor | HTTP 5xx / timeout / DNS failure on first navigate | Emit `sut-unreachable.json`; halt pipeline; no retries in codegen mode (retry_count=0) |
| LLM refuses to generate (content policy) | e2e-author | Model refusal response detected in completion | Emit `refusal.json` with cited policy; escalate to user per P-020; do NOT attempt workaround prompts |
| Generated test has no assertions | e2e-verifier | Assertion inventory Step 1 returns empty list | Emit FAIL verdict with `assertion_inventory: []`; escalate to author; replan recommendation: "Add at least one Then clause with sensitivity VERIFIED" |
| False positive — test passes but app broken | e2e-verifier | Sensitivity rubric: all assertions RAN-ONLY; no VERIFIED | Emit REVISE verdict; escalate to author citing three-level model (navigation -> identity -> isolation) |
| Agent exceeds tool allowlist | any agent | Runtime tool dispatcher blocks the call | Log `allowlist-violation.json`; emit agent-level error; eng-lead review triggered (cross-skill escalation) |
| AGPL-3.0 boundary violation attempted | any authoring agent | Output filter grep against Skyvern reference phrases matches | Emit `agpl-boundary-alert.json`; block artifact persistence; escalate to eng-lead |
| Adversary gate fails 3 iterations | e2e-verifier | Iteration counter on failed adv-scorer invocations | AE-006 mandatory human escalation; reporter emits AE-006 flag in L0 |
| a11y-tree empty (a11y-hostile SUT) | e2e-executor | browser_snapshot returns empty or malformed tree | Emit `a11y-empty.json` diagnostic; verifier may escalate to author for vision-LLM fallback declaration (declaration, not implementation — vision-LLM fallback is Phase 4+ work per OQ-E2E-004) |
| Diff empty but no --full-suite flag | e2e-analyst | scope-document would have empty `prioritised_scope` | Emit `no-changes-detected.json`; halt with user prompt; P-E2E-03 enforcement |
| autonomy_tier missing from upstream | e2e-reporter | verifier-verdict.json lacks `autonomy_tier` field | HALT with P-022 violation notice; `p022-enforcement-halt.json`; user supplies tier before report |
| Call-graph tool unavailable | e2e-analyst | shell_execute returns non-zero or timeout | AD-010 Level 1 fallback: semantic similarity heuristic; flag output "call-graph absent" |
| Version mismatch on pinned Playwright MCP | e2e-executor (at init) | Tool signature mismatch against expected schema | Emit `mcp-version-mismatch.json`; block run; require PLAYBOOK.md upgrade SOP (implementation-plan Risk 1) |

---

## 8. Autonomy Tier Architecture

P-E2E-10 introduces tier declaration as a novel gap-driven principle. Eng-architect defines the tier semantics here.

### 8.1 Tier Definitions

| Tier | Human Role | Use Case | Default? | Requires Opt-In? |
|------|-----------|----------|----------|------------------|
| **AUTONOMOUS** | No human review of individual steps; reviews L0 report only | Trusted SUT, well-established test patterns, low-risk flows, large-batch regression | **YES** (for e2e-governance-config default per implementation-plan §3) — BUT see note below | No (default) |
| **SUPERVISED** | Human reviews every generated scenario before execution | Developing new coverage, uncertain SUT behaviour, security-critical flows | No | No |
| **MANAGED-EQUIVALENT** | Human engineers backstop AI failures post-run (QA Wolf model) | Production SUT, compliance-regulated environments | No | YES — explicit user opt-in required; external process commitment implied |
| **FULLY-AUTONOMOUS-PROD** | No human in the loop; runs against production SUT | Forbidden by default | No | **FORBIDDEN** without governance escalation — requires C4 quality gate per AE-005 (security-relevant) |

**Eng-architect judgment call (P-022 disclosure):** Implementation-plan §3 defaults `autonomy_tier: AUTONOMOUS`. Eng-architect **overrides that default to `SUPERVISED`** in the `e2e-test-generation.md` template's `{{AUTONOMY_TIER}}` default parameter (see Section 3.1). Rationale: at initial release with [SINGLE-STUDY] metric backing and an eval corpus still below the 20-scenario threshold (Risk 5), the conservative default is `SUPERVISED`. `AUTONOMOUS` remains a valid value the user can set, but it is opt-in at template invocation. The governance-config's `autonomy_tier: AUTONOMOUS` stays as the skill-level maximum (values above AUTONOMOUS require explicit escalation), not the workflow-invocation default. This is a defensible conservative posture that does not violate the implementation plan (the plan declares the governance-config default; the template default is an architecture-level decision by eng-architect).

### 8.2 Tier Selection

Caller selects tier via three mechanisms, in priority order:

1. **Template parameter** at invocation: `--autonomy SUPERVISED` (highest precedence)
2. **Governance config override:** `autonomy_tier: SUPERVISED` in per-run `e2e-governance-config.yaml`
3. **Skill-level default:** `AUTONOMOUS` as governance-config schema default — but overridden to `SUPERVISED` at template level (Section 3.1)

**Selection rule:** Template parameter > per-run config > skill default.

### 8.3 Enforcement Points (dual safety net for three-agent-minimum path)

P-022 requires no run be surfaced without autonomy tier. Because e2e-reporter is optional, there are two enforcement points:

- **Primary:** e2e-reporter blocks L0 emission if `autonomy_tier` is absent from upstream artifacts (Section 2.6 failure mode).
- **Secondary (safety net for reporter-absent path):** e2e-verifier emits `autonomy_tier` as a distinct field in `verifier-verdict.json`; verifier's governance YAML includes `autonomy_tier_in_l0: required` as a post-completion check (implementation-plan Risk 7 mitigation). If reporter is absent and verifier output is surfaced directly, the tier is still present.

### 8.4 Forbidden Tiers

`FULLY-AUTONOMOUS-PROD` (fully autonomous runs against production SUT) is **forbidden by default governance**. A caller attempting this tier value triggers:
1. Governance YAML `input_validation` rejects the value (it is not in the enum).
2. Escalation to eng-lead for governance review.
3. If approved (rare), requires a documented C4 review per AE-005 (security-relevant change) before the tier is added to the enum.

---

## 9. Security and Governance Design

### 9.1 Tool Allowlist Enforcement

Three-layer enforcement:

1. **Governance YAML layer** (`agents/{agent}.governance.yaml` `capabilities.allowed_tools`): enforced by Claude Code's runtime dispatcher. Calls outside the allowlist are blocked at dispatch.
2. **Agent MD disclosure layer** (`## Tool Integration`): human-readable statement of what tools the agent expects. Any drift between MD and YAML is a Phase 4 post-build verification failure (implementation-plan Risk 4 mitigation).
3. **Prompt-level reminder layer** (agent `## Constitutional Compliance` block): "You MUST NOT attempt tool calls outside your allowlist. Agent delegation is forbidden per P-003."

### 9.2 Secrets Handling

- **Credentials for SUT:** NEVER stored in generated artifacts (screenshots, traces, Gherkin). Secrets are injected via environment variables at executor runtime, not persisted.
- **Governance YAML guardrail:** `output_filtering: - no_secrets_in_output` (inherited from eng-qa.governance.yaml pattern).
- **Trace redaction:** `executor-trace.json` passes through a redaction filter before persistence. Values matching `password|secret|api_key|bearer|jwt` patterns are replaced with `[REDACTED]`.
- **Screenshot PII handling:** Screenshots are retained in `output/{E2E-NNNN}/screenshots/` with a retention policy (Section 9.3).

### 9.3 Data Exfiltration Boundary and Retention

- **Retention:** Test run artifacts are retained for 30 days by default. `e2e-governance-config.yaml` includes `retention_days: 30` (new field added by this architecture; eng-qa Phase 4 Step B must add to the governance schema).
- **Exfiltration risk:** Screenshots and DOM snapshots from an authenticated SUT may contain PII or business-sensitive data. The skill MUST NOT transmit these artifacts outside the local filesystem (no cloud upload, no email, no webhook). This is a negative capability — enforced by the allowlist (no `web_fetch`, no `shell_execute` on executor beyond Playwright).
- **Cleanup:** PLAYBOOK.md documents the cleanup SOP: after 30 days, run `jerry cleanup e2e-outputs`. Scripted cleanup is out of scope for initial release.

### 9.4 STRIDE-Lite Threat Model

| Threat | Attacker | Target | Control |
|--------|----------|--------|---------|
| **Spoofing** | Malicious diff input | e2e-analyst | Input validation in governance YAML; user confirmation on scope (P-E2E-03) prevents unreviewed scope acceptance |
| **Tampering** | Modified trace file injected between executor and verifier | e2e-verifier | Trace integrity check — verifier validates trace schema; mismatched schema triggers `trace-invalid.json` (Section 2.4 failure mode) |
| **Repudiation** | User claims they did not approve a scope | e2e-analyst, reporter | `scope-document.json` persists `confirmation_received: true` with testrun_id; reporter L0 includes autonomy tier declaration |
| **Information Disclosure** | Secrets leaked into artifacts | e2e-executor | Redaction filter (Section 9.2); negative capability on network egress tools |
| **Denial of Service** | Malicious SUT forces infinite wait | e2e-executor | `journey_timeout_seconds: 30` in governance; Playwright MCP `browser_wait_for` has internal timeout |
| **Elevation of Privilege** | Prompt injection in Gherkin scenario attempts to escalate e2e-author to tool delegation | e2e-author | `agent_delegate` in forbidden_tools (P-003 enforcement); author has no shell or browser access |
| **Prompt Injection via DOM** | SUT contains adversarial content designed to hijack e2e-executor via `browser_snapshot` output | e2e-executor | System prompt quarantine frame (requirements §8 Playwright MCP posture); snapshot content treated as data, not instructions |
| **AGPL boundary violation** | LLM reproduces Skyvern prompt text verbatim | any authoring agent | Output filter (Section 6.4); prompt-level guardrail |

---

## 10. Cross-Skill Integration Design

### 10.1 /problem-solving (ps-critic in creator-critic loops)

- **H-14 enforcement:** For C2+ deliverables, the creator-critic-revision cycle pairs e2e-author (creator) with ps-critic (external critic). Minimum 3 iterations. The e2e-verifier's S-014 self-score is self-review (H-15) — not a substitute for the ps-critic cycle.
- **Integration trigger:** e2e-author invokes `/problem-solving ps-critic` after producing its first draft of `author-plan.json`. ps-critic reviews against Jerry's quality dimensions and returns critique. Author revises.
- **ps-investigator as upstream consultant:** When e2e-author receives a replanning request that hypothesises a deep application bug (e.g., "this flow always fails because of intermittent race condition"), author consults `/problem-solving ps-investigator` before drafting the replan. Research informs the replan; it does not replace it.

### 10.2 /adversary (adv-scorer at skill-internal 0.94 gate)

- **When triggered:** e2e-verifier invokes `/adversary adv-scorer` for C2+ deliverables per H-17. Trigger is the verifier's verdict-emission step — adv-scorer runs in parallel with functional-correctness scoring.
- **What is scored:** The deliverable bundle (plan, feature, trace, report draft). adv-scorer applies S-014 six-dimension rubric and returns score + dimension-level feedback.
- **Threshold:** 0.94 for skill-internal gate. Score below 0.94 -> REVISE band; verifier escalates to author for revision.
- **External /adversary invocation:** When a user runs `/adversary` directly against an e2e-testing artifact (outside the verifier's invocation), adv-scorer governs. The skill's internal gate is not re-run. This matches the skill-routing decision table in quality-enforcement.md.
- **Escalation ladder:** mirrors eng-team three-failure pattern. 1st fail -> revise + resubmit; 2nd fail -> eng-lead; 3rd fail -> eng-architect; persistent -> user notification per P-020.

### 10.3 /eng-team (three seams)

**Seam 1 — Security Scope (eng-qa):**
- Routing rule (from requirements §9 Seam 1): browser+user-journey security -> /e2e-testing; input-validation fuzz / property invariants / SSDF PW.8 -> /eng-team eng-qa.
- Tag attribution: `@wstg:` on e2e-testing; `@owasp-tg:` on eng-qa. Reporter includes both tag classes in L1 coverage matrix for audit.

**Seam 2 — Quality Scoring (eng-reviewer):**
- Internal gate (e2e-verifier): 0.94 S-014 process score + GenIA-E2ETest functional metrics. MUST pass before escalation.
- Engagement-level gate (eng-reviewer): 0.95 for security-focused engagements. Only deliverables that passed the 0.94 gate are eligible.
- Sequential, not competing.

**Seam 3 — CI/CD (eng-devsecops):**
- Out of scope for this skill. e2e-testing produces artifacts; eng-devsecops wires them into gates.
- `e2e-governance-config.yaml` thresholds are the contract.

### 10.4 /nasa-se (optional — requirements traceability)

- Invoked only if `iso29119_artifacts: true` in governance config (RT-001 opt-in).
- When invoked: /nasa-se consumes the Gherkin `.feature` files and produces ISO 29119-3-compatible test-case specifications alongside them.
- No hard dependency. Skill functions fully without /nasa-se.

### 10.5 /red-team (optional — security scenario generation)

- /red-team produces threat intel that feeds eng-architect (eng-team baseline §7.4).
- Integration with /e2e-testing: if /red-team identifies a user-journey-level attack (e.g., BUSL abuse), the intel is a direct input to e2e-author's WSTG-BUSL scenario generation.
- Pattern: /red-team -> (threat intel) -> e2e-author -> `@wstg:WSTG-v42-BUSL-NN` scenario -> e2e-executor.
- No hard dependency. Without /red-team, security scenarios default to WSTG taxonomy alone.

---

## 11. Acceptance Criteria for Phase 4 Build Agents

### 11.1 eng-lead (Phase 4 Step A — SKILL.md + PLAYBOOK.md)

- [ ] `skills/e2e-testing/SKILL.md` exists with exact casing (H-25).
- [ ] Frontmatter `name: e2e-testing` matches folder name exactly (H-26).
- [ ] No `README.md` anywhere in `skills/e2e-testing/` (H-27).
- [ ] Description field satisfies WHAT + WHEN + triggers, under 1024 chars, no XML (H-28) — use draft candidate from implementation-plan §5.
- [ ] All file references in SKILL.md use full repo-relative paths (H-29).
- [ ] SKILL.md declares pinned Playwright MCP version in frontmatter.
- [ ] SKILL.md declares tool allowlist summary at skill level (not per-agent — that is governance YAML's job).
- [ ] PLAYBOOK.md resolves OQ-E2E-001 (agentic-flow Gherkin syntax) — consumed by Phase 4 Step B template authoring.
- [ ] PLAYBOOK.md resolves OQ-E2E-002 (SPA hardening wait chain).
- [ ] PLAYBOOK.md enumerates PG-1..PG-7 with Pass Criteria and Fail Actions.
- [ ] PLAYBOOK.md documents six-category flake taxonomy.
- [ ] PLAYBOOK.md documents AGPL-3.0 boundary note verbatim from requirements §8.

### 11.2 eng-qa (Phase 4 Step B — templates/ + validation/ + examples/)

- [ ] Five templates exist per Section 3 of this document, each with: section skeleton, placeholders, defaults, consumer/producer agents, validation rules.
- [ ] `validation/validation-strategy.md` instantiates Section 4 of this architecture verbatim (six-step procedure, metrics, escalation, orthogonality disclosure).
- [ ] Three example `.feature` files exist under `examples/`:
  - `auth-journey.feature` with at least one VERIFIED and one RAN-ONLY assertion (calibration reference per Risk 3)
  - `security-wstg-busl.feature` with `@wstg:WSTG-v42-BUSL-NN` tag
  - `agentic-flow-example.feature` instantiating OQ-E2E-001 syntax resolution
- [ ] Every template populated with defaults passes the validation rules in Section 3.
- [ ] `e2e-governance-config.md` template emits the default YAML block from implementation-plan §3 + this architecture's additions (`retention_days`).
- [ ] Five template defaults align with implementation-plan §3 governance-config, with `{{AUTONOMY_TIER}}: SUPERVISED` override noted (eng-architect judgment, Section 8.1).

### 11.3 eng-architect (Phase 4 Step C — agents/ + governance yaml + composition/)

- [ ] All five agent `.md` files exist with the eng-team skeleton (identity + methodology + workflow integration + L0/L1/L2 + AD-010 + constitutional compliance) per eng-team baseline §7.1.
- [ ] Each agent's Methodology section cites the principle it owns (Section 1 matrix) as primary.
- [ ] Each agent's "Failure Modes" subsection references Section 7 failure mode catalogue.
- [ ] All five `.governance.yaml` files exist with the schema from implementation-plan §4, with per-agent overrides.
- [ ] e2e-executor governance YAML declares pinned Playwright MCP version (propagated from SKILL.md).
- [ ] Agent tool allowlist in MD matches governance YAML `capabilities.allowed_tools` field-for-field (Risk 4 mitigation — verification step required).
- [ ] All ten composition files exist (`.agent.yaml` + `.prompt.md` per agent) following ADR-PROJ010-003 38-field portable schema.
- [ ] Governance YAML `output_filtering` includes `no_skyvern_source_code` and `no_secrets_in_output` on all five agents.
- [ ] Orthogonality disclosure (Section 4.4) appears verbatim in e2e-verifier.md identity block.
- [ ] Autonomy-tier dual enforcement (Section 8.3) appears in both e2e-verifier.governance.yaml AND e2e-reporter.governance.yaml `validation.post_completion_checks`.

---

## Source References

| Design Decision | Source |
|-----------------|--------|
| Agent responsibility matrix (Section 1) | requirements §2 principle traceability; implementation-plan §2 integration points |
| P-E2E-01/03 ownership moves to e2e-analyst | eng-architect judgment (P-022 disclosure); implementation-plan §2 states analyst is invoked for change-impact analysis |
| Six-step validation procedure (Section 4.1) | requirements §6.3 |
| Thresholds execution_recall>=0.80, element_precision>=0.70, MMR<=0.15 | requirements §6.4; P-E2E-09 |
| New metric `assertion_sensitivity_rate` | eng-architect derivation from requirements §6.3 (P-022 disclosure — new metric, not sourced) |
| Orthogonality disclosure (Section 4.4) | requirements §6.5 |
| S-014 six-dimension rubric | quality-enforcement.md; eng-team baseline §4 |
| Handoff artifact schemas (Section 5) | requirements §4 outputs; implementation-plan §2 integration points |
| Playwright MCP core-8 tool list | implementation-plan §2 e2e-executor; innovators baseline inn-2 §7.1 (max 10 tools) |
| AD-010 three-level degradation names | eng-team baseline §7.2; implementation-plan §1 |
| AGPL-3.0 boundary enforcement mechanism | requirements §8 (Skyvern MIRROR posture); implementation-plan Risk 2 |
| STRIDE-lite threat model (Section 9.4) | eng-architect methodology (standard threat modeling practice); P-E2E-08 adjacency |
| Autonomy tier definitions (Section 8.1) | requirements §2 P-E2E-10; eng-architect judgment for tier-level FORBIDDEN semantics (P-022 disclosure) |
| Autonomy default override to SUPERVISED in template | eng-architect judgment (P-022 disclosure — departs from implementation-plan §3 AUTONOMOUS default at template level for initial release conservatism); Risk 5 calibration |
| Failure mode catalogue (Section 7) | implementation-plan Risks 1-7; requirements §6.3 failure classification |
| Three eng-team integration seams | requirements §9; implementation-plan §6 |
| ps-critic in creator-critic loops | implementation-plan §6; quality-enforcement.md H-14 |
| AE-002/AE-005/AE-006 escalation | quality-enforcement.md |
| Three-failure escalation ladder | eng-team baseline §4 (adversary-integration.md) |
| Retention policy (retention_days: 30) | eng-architect judgment (P-022 disclosure — new field not in implementation plan; added for exfiltration boundary) |
| Template placeholder conventions | eng-architect derivation from eng-team templates §7.6 R-011 pattern |
| SUPERVISED as conservative default at template layer | eng-architect judgment (P-022 disclosure — departs from governance-config AUTONOMOUS default); Risk 5 |
| P-022 dual-enforcement safety net (verifier + reporter) | implementation-plan Risk 7 mitigation |
| WSTG six mandatory categories | P-E2E-08; requirements §7 |
| Gherkin extension syntax for agentic flows | OQ-E2E-001 (to be resolved by Phase 4 Step A) |
| SPA hardening wait chain | OQ-E2E-002 (to be resolved by Phase 4 Step A); implementation-plan Risk 6 |
| L0/L1/L2 output contract | eng-team baseline §7.3 |
| Quality threshold 0.94 triangulation | requirements §9 RT-004; requirements §3 RT-004 |
