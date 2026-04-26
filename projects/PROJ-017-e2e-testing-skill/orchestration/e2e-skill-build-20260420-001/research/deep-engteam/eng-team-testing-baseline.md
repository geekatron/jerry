# eng-team Testing Baseline — Deep Research for /e2e-testing Skill Build

> **Phase 1b Frontmatter**
>
> | Field | Value |
> |-------|-------|
> | **Topic** | Jerry `/eng-team` skill — internal testing framework and agent patterns |
> | **Slug** | `engteam` |
> | **Agent** | ps-researcher-engteam (LOCAL FILES ONLY variant) |
> | **Workflow** | PROJ-017 e2e-testing-skill-build / orchestration e2e-skill-build-20260420-001 / Phase 1b Deep Research |
> | **Access Date** | 2026-04-21 |
> | **Data Source Type** | LOCAL (no web search performed or permitted) |
> | **Root Inspected** | `/Users/victor.lau/.claude/plugins/cache/jerry-framework/jerry/0.29.1/skills/eng-team/` |

## Document Sections

| Section | Purpose |
|---------|---------|
| [Methodology Note](#methodology-note) | Files Read and Glob/Grep patterns used |
| [1. Eng-team Overview](#1-eng-team-overview) | 8-step workflow, agent-to-step mapping, testing position |
| [2. eng-qa Test Methodology](#2-eng-qa-test-methodology) | Threat-driven design, OWASP mapping, fuzzing, property-based, coverage |
| [3. Testing Standards Referenced](#3-testing-standards-referenced-by-eng-team) | OWASP TG, NIST SSDF, ASVS, pytest, coverage.py, CIS, SLSA |
| [4. eng-reviewer Gate Patterns](#4-eng-reviewer-gate-patterns) | /adversary integration, 0.95 threshold, revision loop |
| [5. Governance YAML Patterns](#5-governance-yaml-patterns) | Sibling `.governance.yaml` fields, reuse for e2e-testing |
| [6. Gaps for /e2e-testing to Fill](#6-gaps-for-e2e-testing-to-fill) | Browser/UI, agentic, real-user-journey, synthetic, MCP browser |
| [7. Reusable Patterns / Testable Principles](#7-reusable-patterns--testable-principles) | Agent file skeleton, 3-level degradation, cross-skill integration |
| [Sources Consulted (Local)](#sources-consulted-local) | Every cited file path with line anchors |

---

## Methodology Note

**Files Read (full or partial):**

| Path (relative to `skills/eng-team/`) | Lines Read | Purpose |
|---|---|---|
| `SKILL.md` | 1–478 (full) | Orchestration flow, agent roster, quality gates, routing |
| `agents/eng-qa.md` | 1–122 (full) | Test methodology, OWASP mapping, fuzzing, coverage |
| `agents/eng-reviewer.md` | 1–124 (full) | Gate patterns, /adversary integration, 0.95 threshold |
| `agents/eng-architect.md` | 1–112 (full) | Threat modeling by criticality, STRIDE/DREAD |
| `agents/eng-lead.md` | 1–97 (full) | Standards mapping, SSDF practices, SAMM |
| `agents/eng-devsecops.md` | 1–131 (full) | SAST/DAST/SCA pipeline, SLSA build |
| `agents/eng-qa.governance.yaml` | 1–60 (full) | Governance-YAML schema sample |
| `agents/eng-reviewer.governance.yaml` | 1–61 (full) | Governance-YAML schema sample (reviewer variant) |
| `adversary-integration.md` | 1–199 (full) | C2+ criticality table, escalation path, score bands |
| `templates/security-test-plan.md` | 1–142 (full) | R-011 configurable rule set, ASVS test cases |
| `templates/engagement-playbook.md` | 1–241 (full) | 8-step playbook, phase gates PG-1 through PG-7 |
| `composition/eng-qa.prompt.md` | 1–114 (full) | RCCF-assembled portable prompt (canonical body) |
| `composition/eng-qa.agent.yaml` | 1–88 (full) | 38-field portable schema (AD-010, ADR-PROJ010-003) |

**Directory listings performed (Bash `ls -la`):**
- `skills/eng-team/` (root) — confirmed 8 entries, 4 sub-dirs
- `skills/eng-team/agents/` — 20 files (10 `.md` + 10 `.governance.yaml`)
- `skills/eng-team/composition/` — 20 files (10 `.agent.yaml` + 10 `.prompt.md`)
- `skills/eng-team/templates/` — 5 files (checklist, playbook, design-review, test-plan, threat-model)
- `skills/eng-team/output/` — 2 engagement dirs (GH-118, PORT-001)

**Grep patterns used (within eng-team tree):**

| Pattern | Purpose | Result |
|---|---|---|
| `e2e\|end-to-end\|browser\|playwright\|selenium\|cypress\|puppeteer\|synthetic\|MCP.browser\|headless` (`-i`) | Detect any E2E / browser-automation coverage | NO matches for `e2e`, `playwright`, `selenium`, `cypress`, `puppeteer`, `synthetic`, `MCP browser`, `headless`. Only 4 `browser`-context matches in eng-frontend (CSP/XSS audit, Lighthouse) and 1 `end-to-end` match in `adversary-integration.md` ("End-to-End Quality Workflow" — not test E2E) |
| `synthetic\|smoke\|post.deploy\|production.check\|canary\|rollback\|user.journey\|journey.test` (`-i`) on `eng-incident.md` | Check post-deployment E2E coverage | `rollback` found (containment procedures); `post-deploy` found (monitoring, alerting). NO synthetic-testing, no user-journey, no smoke tests, no canary |

**Web search:** NOT performed (LOCAL-ONLY constraint). All citations are local file paths with line numbers.

---

## 1. Eng-team Overview

The `/eng-team` skill is a 10-agent secure-engineering methodology skill (v1.0.0) orchestrated as an **8-step sequential phase-gate workflow** with a single parallel fan-out at Step 3 (`SKILL.md:190–210`). The agent roster and per-step ownership:

| Step | Agent(s) | Role at This Step | Source |
|---|---|---|---|
| 1 | `eng-architect` | System design + STRIDE/DREAD/PASTA threat model + ADRs | `SKILL.md:195, 212` |
| 2 | `eng-lead` | Implementation plan, coding standards, dependency governance, SAMM maturity | `SKILL.md:197, 214` |
| 3 (parallel) | `eng-backend`, `eng-frontend`, `eng-infra` | Domain implementations — server-side OWASP, client-side CSP/XSS, IaC + containers | `SKILL.md:199, 216` |
| 4 | `eng-devsecops` | Automated SAST / DAST / secrets / container / SCA scans | `SKILL.md:201, 218` |
| 5 | `eng-qa` | Test strategy, fuzzing, property-based, coverage | `SKILL.md:203, 220` |
| 6 | `eng-security` | Manual CWE Top 25 + ASVS review | `SKILL.md:205, 222` |
| 7 | `eng-reviewer` | Final gate + /adversary C2+ scoring @ >=0.95 | `SKILL.md:207, 224` |
| 8 | `eng-incident` | IR runbooks, post-deployment monitoring (non-gated, independent) | `SKILL.md:209, 226` |

**Where testing fits:** Testing is confined to **Steps 4–5** (`engagement-playbook.md:80–113`). Step 4 is *automated* (eng-devsecops runs SAST/DAST/SCA/container/secrets scans), Step 5 is *strategy-driven* (eng-qa produces test cases, fuzzing, property-based, coverage reports). Step 5 feeds eng-security in Step 6 and eng-reviewer in Step 7 (`eng-qa.md:80–83`).

**Phase gates** (`engagement-playbook.md:168–177`): 7 explicit quality gates PG-1..PG-7. Of note, **PG-5 (Step 5→6) pass criterion is `coverage >= 90%, critical tests pass`** and **PG-7 (Step 7→8) is `quality score >= 0.95 (C2+), compliance confirmed`**.

**State passing** between agents is via output keys (`SKILL.md:232–245`): e.g., `qa_output` → consumed by eng-security, eng-reviewer. Outputs are persisted to `skills/eng-team/output/{engagement-id}/{agent}-{topic-slug}.md` (`SKILL.md:259–273`).

---

## 2. eng-qa Test Methodology

From `agents/eng-qa.md:37–71` and mirrored in `composition/eng-qa.prompt.md:29–62`:

**Security Test Strategy Framework (7 steps):**

1. **Threat-Driven Test Design** — Derive test cases from eng-architect threat model (`eng-qa.md:41`)
2. **OWASP Testing Guide Mapping** — Map test categories to OWASP TG chapters
3. **Boundary Analysis** — Identify security-critical boundaries + edge-case enumeration
4. **Fuzzing Campaign Design** — Select targets based on threat model + input surface
5. **Property-Based Test Design** — Define security invariants as testable properties
6. **Regression Suite Construction** — Build regressions from every discovered vulnerability
7. **Coverage Enforcement** — Measure + enforce line/branch/security-specific coverage

**OWASP Testing Guide categories mapped** (`eng-qa.md:49–61`): IDENT, AUTHN, AUTHZ, SESS, INPVAL, CRYPST, BUSLOGIC, CLNT, API.

**Fuzzing strategy matrix** (`eng-qa.md:63–70`):

| Fuzzing Type | Application | Tooling |
|---|---|---|
| Coverage-guided | Binary/library functions | **AFL++**, libFuzzer |
| Grammar-based | Protocol/format parsing | Custom grammars |
| API fuzzing | REST/GraphQL endpoints | RESTler, Schemathesis |
| Property-based | Input validation logic | **Hypothesis**, QuickCheck |

**Coverage requirement:** The eng-qa agent file itself says "Enforce test coverage requirements (line, branch, and security-specific coverage)" (`eng-qa.md:27`). The numeric threshold is set in two places:
- `templates/security-test-plan.md:135` — `minimum_code_coverage` default **90%** (configurable 0–100%, R-011 rule set), cited as "H-20" (though H-20 is actually BDD Red phase per root `quality-enforcement.md`; this looks like a local misreference — H-21 is the 90% rule)
- `templates/engagement-playbook.md:105, 174` — PG-5 gate: `>= 90% line coverage (H-20), all critical test cases pass`

**Mutation testing:** NOT referenced anywhere in eng-qa. Coverage is line + branch + "security-specific" only (no mutation score threshold).

**Fuzzing duration config** (`templates/security-test-plan.md:136`): default **4 hours**, configurable 1–48h.

**ASVS depth config** (`templates/security-test-plan.md:137`): default **Level 2**, range Level 1–3.

**SSDF mapping** (`eng-qa.md:73–75`): eng-qa owns **PW.8** (test executable code) as primary, contributes to **PW.7** (code analysis).

---

## 3. Testing Standards Referenced by eng-team

Consolidated standards surface:

| Standard | Version | Cited Role | Source |
|---|---|---|---|
| **OWASP Testing Guide** | (unversioned) | Test category mapping + methodology (eng-qa) | `eng-qa.md:100, eng-qa.md:49–61` |
| **OWASP ASVS** | v5.0 (2025) | Verification requirements (V2.1.1, V4.1.2, V5.3.x used as test-case anchors) | `SKILL.md:452; templates/security-test-plan.md:65–85` |
| **OWASP Top 10** | 2021 | Backend web app vuln class baseline | `SKILL.md:453` |
| **CWE Top 25** | 2025 | Manual review baseline (eng-security) | `SKILL.md:454` |
| **NIST SP 800-218 SSDF** | v1.1 (2022) | PO.1 (arch), PO.3 (tooling), PS.1 (code protection), PW.7 (static review), PW.8 (dynamic test), RV.1–3 (remediation verification) | `SKILL.md:450; eng-qa.md:73–75; eng-reviewer.md:77–80` |
| **MS SDL** | 2024 | 5-phase (Requirements, Design, Implementation, Verification, Release); eng-qa = Verification | `SKILL.md:451, 282; eng-qa.md:84–86` |
| **OWASP SAMM** | v2.0 | Maturity assessment for eng-lead | `SKILL.md:456; eng-lead.md:79` |
| **Google SLSA** | v1.0 (2023) | Build integrity (Level 1–3) for eng-infra/eng-devsecops | `SKILL.md:455; eng-devsecops.md:80–83` |
| **CIS Benchmarks** | Various | Infra hardening; eng-reviewer checks compliance | `SKILL.md:457; eng-reviewer.md:45` |
| **NIST CSF** | v2.0 (2024) | Identify/Protect/Detect/Respond/Recover mapping for eng-architect | `SKILL.md:458; eng-architect.md:90` |
| **NIST SP 800-61** | r3 (2024) | Incident response methodology (eng-incident) | `SKILL.md:459` |
| **pytest** | (unversioned) | Python test framework | `eng-qa.md:102` |
| **coverage.py** | (unversioned) | Code coverage measurement tool | `eng-qa.md:105` |
| **AFL++** | (unversioned) | Coverage-guided binary fuzzing | `eng-qa.md:103` |
| **Hypothesis** | (unversioned) | Property-based testing for Python | `eng-qa.md:104` |

**Not referenced anywhere in eng-team** (searched explicitly, LOCAL only): OWASP WSTG chapter numbers, Playwright, Selenium, Cypress, Puppeteer, Testcafe, WebDriverIO, BrowserStack, Lighthouse CI, Percy, Applitools, Chromatic, Allure, ReportPortal, Cucumber/BDD framework, Gherkin, k6/Locust/JMeter load-test tools, synthetic monitoring (Datadog/New Relic), mutation-testing frameworks (mutmut/PIT/Stryker).

---

## 4. eng-reviewer Gate Patterns

eng-reviewer is **the single integration point between /eng-team and /adversary** (`adversary-integration.md:32, 48`).

**Gate workflow** (`eng-reviewer.md:41–50`):
1. Artifact Collection from Steps 1–6
2. Architecture Compliance check
3. Security Standards Check (OWASP, CWE, CIS, SLSA)
4. Test Coverage Verification (eng-qa output, threshold from R-011)
5. Security Finding Review (eng-security remediation status)
6. Scan Result Review (eng-devsecops critical/high findings)
7. **Quality Scoring** — S-014 LLM-as-Judge + recommend orchestrator-level /adversary invocation for C2+
8. Release Decision (GO / NO-GO)

**/adversary invocation table** (`eng-reviewer.md:54–60`):

| Criticality | /adversary action | Threshold |
|---|---|---|
| C1 | Self-review (S-010) only | no formal threshold |
| C2 | S-007 + S-002 + S-014 scoring | **>= 0.95** |
| C3 | C2 + S-004 + S-012 + S-013 | **>= 0.95** |
| C4 | Full tournament (all 10 strategies) | **>= 0.95** |

Note the **eng-team-local 0.95 threshold is stricter than the root `quality-enforcement.md` H-13 of 0.92**. `adversary-integration.md:89–93` makes this explicit with score bands: PASS >=0.95, REVISE 0.85–0.94, REJECTED <0.85. This is a deliberate "eng-team-internal" tightening — e2e-testing should decide whether to mirror `0.95` or inherit the looser `0.92`.

**Six-dimension S-014 rubric** (`eng-reviewer.md:66–74`, identical to SSOT `quality-enforcement.md`):

| Dimension | Weight | eng-team Application |
|---|---|---|
| Completeness | 0.20 | All required artifacts present |
| Internal Consistency | 0.20 | Implementation matches architecture |
| Methodological Rigor | 0.20 | Standards compliance verified |
| Evidence Quality | 0.15 | Scan results, test results, review findings |
| Actionability | 0.15 | Remediation guidance actionable |
| Traceability | 0.10 | Threat model → implementation → test trace |

**Escalation protocol** (`adversary-integration.md:95–101`):
1. First failure (REVISE band) → return findings to originating agent, revise + resubmit
2. Second failure → escalate to eng-lead (systemic design issue suspected)
3. Third failure or REJECTED → escalate to eng-architect (architecture-level root cause)
4. Persistent failure → user notification per P-020

**Eng-qa → eng-reviewer handoff is indirect** (`adversary-integration.md:46`) — test results feed evidence into eng-reviewer's *engagement-level* scoring, but are not independently `/adversary`-scored. A new `/e2e-testing` skill should mirror the same pattern: test artifacts feed the reviewer, but the reviewer (or a new e2e-reviewer) owns the /adversary gate.

---

## 5. Governance YAML Patterns

Every agent has **two sibling YAML artifacts**:

1. `agents/{agent-name}.governance.yaml` — runtime governance metadata (validated against `docs/schemas/agent-governance-v1.schema.json`, `eng-qa.governance.yaml:2`)
2. `composition/{agent-name}.agent.yaml` — canonical 38-field portable schema (ADR-PROJ010-003, `composition/eng-qa.agent.yaml:1–2`) + `composition/{agent-name}.prompt.md` (RCCF-assembled portable prompt body)

**Governance YAML fields** (`eng-qa.governance.yaml:1–60`, confirmed against `eng-reviewer.governance.yaml:1–61`):

```yaml
version: 1.0.0
tool_tier: T3                         # tool-access tier
identity:
  role: <string>
  expertise: [list of 6]
  cognitive_mode: systematic|convergent|divergent
persona:
  tone: professional
  communication_style: methodical|evidence-based
  audience_level: adaptive
guardrails:
  input_validation:
    - engagement_id_format: ^ENG-\d{4}$
  output_filtering:
    - no_secrets_in_output
    - all_claims_must_have_citations
    - no_executable_code_without_confirmation
  fallback_behavior: warn_and_retry
output:
  required: true
  location: skills/eng-team/output/{engagement-id}/{agent}-{topic-slug}.md
  levels: [L0, L1, L2]
constitution:
  reference: docs/governance/JERRY_CONSTITUTION.md
  principles_applied:
    - 'P-003: No Recursive Subagents (Hard)'
    - 'P-020: User Authority (Hard)'
    - 'P-022: No Deception (Hard)'
validation:
  file_must_exist: true
  link_artifact_required: true
  post_completion_checks:
    - verify_file_created
    - verify_artifact_linked
    - verify_l0_l1_l2_present
    - verify_citations_present
capabilities:
  forbidden_actions: [list of 8 — P-0xx violations + role-exclusions]
```

**Canonical (portable) schema fields** (`composition/eng-qa.agent.yaml:1–88`) add:

- `skill: eng-team` — parent skill binding
- `model.tier: reasoning_standard` — model preference tier
- `tools.native` (file_read, file_write, file_edit, file_search_glob, file_search_content, shell_execute, web_search, web_fetch)
- `tools.mcp: [context7]`
- `tools.forbidden: [agent_delegate]` — explicit P-003 enforcement
- `portability.enabled: true`, `minimum_context_window: 128000`, `model_preferences: [claude-sonnet-4, gpt-4o, gemini-2.5-pro]`, `reasoning_strategy: adaptive`, `body_format: markdown`

**Reusable for /e2e-testing? YES — with one caveat.** The `engagement_id_format: ^ENG-\d{4}$` guardrail is hard-coded for security engagements. For an e2e-testing skill, replace with (e.g.) `^E2E-\d{4}$` or `^TESTRUN-\d{4}$` and persist outputs under `skills/e2e-testing/output/{testrun-id}/`. All other fields (persona, guardrails, output L0/L1/L2, constitutional refs, `file_must_exist`/`link_artifact_required`, forbidden actions) port as-is.

---

## 6. Gaps for /e2e-testing to Fill

Based on exhaustive Grep across the eng-team tree, eng-team does **NOT** cover the following testing concerns. An e2e-testing skill has a legitimate non-overlapping scope in each:

| Gap | Evidence (LOCAL) | /e2e-testing Responsibility |
|---|---|---|
| **Browser-driven / UI automation** | Zero matches for `playwright`, `selenium`, `cypress`, `puppeteer`, `headless` across entire tree. eng-frontend mentions "browser" only in XSS/CSP/CORS context (`eng-frontend.md:16, 27, 97, 105, 106`) and Lighthouse as a static audit tool, not an automation driver. | Drive real browsers; evaluate DOM state; capture screenshots/traces |
| **Real-user-journey (multi-step scenario) assertions** | Zero matches for `user.journey`, `journey.test`, `scenario.test`, `BDD`, `Cucumber`, `Gherkin`. eng-qa's "boundary analysis" is unit/integration-scale (`eng-qa.md:45`). | Encode flows like "user signs up → verifies email → creates first object → invites peer"; cross-page assertions |
| **Agentic-flow testing** (LLM/agent decisions, tool-call validation) | Zero matches for `agent.*test`, `LLM.*test`, `tool.call`, `prompt.*test`. eng-qa methodology is code-path focused (SAST/DAST/fuzz) — no awareness of stochastic agent outputs or multi-turn prompt validation. | Deterministic + probabilistic assertions over agent trajectories; golden-transcript replay; tool-call schema validation |
| **Post-deployment synthetic testing** | `eng-incident.md:23` configures "post-deployment security monitoring (log analysis, alerting, anomaly detection)" but zero matches for `synthetic`, `smoke`, `canary`, `production.check` in entire tree. eng-incident is reactive (IR runbooks), not proactive (synthetic probes). | Periodic real-traffic-shape probes against production; uptime + semantic correctness; alerting on regression |
| **MCP-browser integration** | Zero matches for `MCP.browser`, `mcp__browser`, or any browser-automation MCP server reference. Only MCP server declared across the skill is `context7` (`eng-qa.md:9; eng-qa.governance.yaml:n/a`). | Native driver for the Claude Code MCP browser server; page-object wrappers; auth-session reuse |
| **Visual regression / DOM snapshot testing** | Zero matches for `visual.regression`, `percy`, `applitools`, `chromatic`, `DOM.snapshot`. | Pixel-diff and DOM-diff against baselines |
| **Load / performance E2E** | Zero matches for `k6`, `locust`, `jmeter`, `load.test`, `performance.test`. | Throughput + latency SLO tests |
| **Accessibility (a11y) E2E** | Zero matches for `a11y`, `axe`, `wave`, `WCAG`. | Automated a11y audits as part of journey tests |
| **Mutation testing** | Zero matches for `mutation.test`, `mutmut`, `stryker`, `PIT`. eng-qa is line + branch + security-specific only (`eng-qa.md:27`). | Optional: mutation score as a stronger coverage signal |

> **P-022 honesty flag:** There is **NO direct conflict** between eng-team and a new /e2e-testing skill — they have non-overlapping surfaces. But there is **overlap risk** in three places:
> 1. eng-qa claims "Security test strategy" (`eng-qa.md:24`). An /e2e-testing skill that performs security-relevant flows (e.g., auth-bypass E2E) could duplicate eng-qa's threat-driven test derivation. Resolve via routing disambiguation: e2e-testing owns UI-layer + full-stack scenarios; eng-qa owns unit + API-level + fuzzing.
> 2. eng-reviewer is the **only** /adversary gatekeeper in eng-team. If /e2e-testing reuses a similar reviewer pattern, the two reviewer agents must agree on criticality inheritance — otherwise the same deliverable could be scored twice against different thresholds (eng-team's 0.95 vs. SSOT H-13's 0.92).
> 3. eng-devsecops "configures CI/CD security gates" (`eng-devsecops.md:27`). An /e2e-testing skill that wires E2E tests into CI/CD must coordinate with eng-devsecops, not re-implement SAST/DAST gates.

---

## 7. Reusable Patterns / Testable Principles

### 7.1 Agent definition file skeleton

Every eng-team agent markdown file follows an identical structure (confirmed across eng-qa, eng-reviewer, eng-architect, eng-lead, eng-devsecops):

```
---
YAML frontmatter (name, description, model, tools, mcpServers)
---
<Agent Name>

> One-line role summary.

## Identity
### What You Do   (6–9 bullets)
### What You Do NOT Do   (4 bullets — boundary assertions vs. sibling agents)

## Methodology
### <Framework Name>   (numbered process 1..N)
### <Domain Matrix>    (table: category | focus / type | tooling)
### SSDF Practice Mapping   (bulleted PO.x / PW.x / RV.x references)

## Workflow Integration
**Position:** Step N in 8-step workflow
**Inputs:** <state keys + artifact types>
**Outputs:** <artifacts>
**Handoff:** <next agent> receives <what>
### MS SDL Phase Mapping

## Output Requirements
(P-002 persistence + L0/L1/L2 level definitions)

## Standards Reference   (table)

## Tool Integration
### AD-010 three-level degradation
- Level 0 (Full Tools)
- Level 1 (Partial Tools)
- Level 2 (Standalone)

## Constitutional Compliance   (P-001, P-002, P-003, P-020, P-022)
```

**Reusable verbatim for e2e-testing agents.** Swap domain content (OWASP → WCAG/visual/journey), keep structure.

### 7.2 Three-level tool degradation (AD-010)

Confirmed in every eng-team agent (e.g. `eng-qa.md:110–113, eng-reviewer.md:111–115, eng-architect.md:99–103`):

| Level | Tool availability | Output type |
|---|---|---|
| **Level 0** | Full (Bash, WebSearch, Context7, Write, Grep, Glob) | Live execution with validated results |
| **Level 1** | Partial (Read/Write/Grep only — no execution) | Strategy + specifications without live runs |
| **Level 2** | Standalone (no tools) | Templates + checklists from methodology knowledge; all claims flagged as "requires validation" |

**For /e2e-testing this maps to:** Level 0 runs real MCP-browser + captures traces; Level 1 produces test specifications without browser execution; Level 2 emits test-plan templates + page-object scaffolds only.

### 7.3 Output L0/L1/L2 level contract

Every agent's `## Output Requirements` (`eng-qa.md:88–94`, `eng-reviewer.md:92–98`) defines a three-audience output:

| Level | Audience | Content type |
|---|---|---|
| **L0** | Executive / stakeholders | Plain-language summary; headline count metrics; GO/NO-GO in one sentence |
| **L1** | Engineer / implementer | Test specs, configs, code examples, reproduction steps, per-artifact compliance matrix |
| **L2** | Architect / strategic | Trade-offs, ROI analysis, gap-risk implications, maintenance considerations |

**Reusable verbatim.** This mirrors the root ps-researcher L0/L1/L2 contract; e2e-testing agents should emit identically-shaped outputs.

### 7.4 Cross-skill integration points

Explicit cross-skill relationships documented:

| Relationship | Direction | Source |
|---|---|---|
| `/red-team` → `eng-architect` | /red-team produces threat intel that becomes eng-architect's input | `SKILL.md:4 ("routes from threat intel"); eng-architect.md:26` |
| `/adversary` ↔ `eng-reviewer` | eng-reviewer is the orchestrator-level invocation point for /adversary on C2+ (`adversary-integration.md:32, 115–131`) | `adversary-integration.md:115–147` |
| eng-team → `/problem-solving` | Misrouted code-review falls back to ps-reviewer (`SKILL.md:409`) | `SKILL.md:405–414` |
| eng-team → `/architecture` | Non-security architecture routes to /architecture instead (`SKILL.md:412`) | `SKILL.md:405–414` |

**For /e2e-testing, the symmetric integration points would be:**
- `/problem-solving (ps-investigator)` → /e2e-testing: when investigator produces a hypothesis about a user-journey bug, e2e-testing reproduces it deterministically
- `/adversary` ↔ /e2e-testing-reviewer (if present): mirror eng-reviewer's >=0.95 gate pattern, OR inherit H-13's >=0.92 — **decision needed**
- `/eng-team (eng-qa)` ↔ /e2e-testing: coordinate so fuzz/unit scope stays with eng-qa, journey/UI scope goes to e2e-testing

### 7.5 Engagement-ID + output directory convention

- Engagement-ID regex: `^ENG-\d{4}$` (`eng-qa.governance.yaml:24`)
- Output path template: `skills/eng-team/output/{engagement-id}/{agent}-{topic-slug}.md` (`SKILL.md:119–128`)
- `link-artifact` post-completion check required (`eng-qa.governance.yaml:45–48`)

**For /e2e-testing:** mirror with `^E2E-\d{4}$` or `^TESTRUN-\d{4}$`; path `skills/e2e-testing/output/{testrun-id}/{agent}-{topic-slug}.md`.

### 7.6 Configurable rule set (R-011)

`templates/engagement-playbook.md:228–237` shows the R-011 pattern — a per-engagement YAML override block with parameters like `workflow_steps`, `quality_threshold`, `compliance_frameworks`, `criticality_level`. `templates/security-test-plan.md:131–139` adds test-specific parameters (`minimum_code_coverage`, `fuzzing_duration_hours`, `asvs_verification_level`).

**Directly portable for e2e-testing.** Candidate parameters: `browsers` (chromium/firefox/webkit), `viewports`, `retry_count`, `screenshot_on_failure`, `trace_on_failure`, `visual_diff_threshold`, `journey_timeout_seconds`.

### 7.7 Phase-gate pattern (PG-N)

`templates/engagement-playbook.md:166–177` enumerates PG-1..PG-7 with explicit `Pass Criteria` and `Fail Action` columns. This gate-enumeration pattern is reusable; /e2e-testing can define its own phase gates (e.g., PG-1 test-plan approved, PG-2 fixtures ready, PG-3 smoke passes, PG-4 full run green, PG-5 visual diffs accepted, PG-6 eng-reviewer/e2e-reviewer gate passed).

---

## Sources Consulted (Local)

All paths relative to `/Users/victor.lau/.claude/plugins/cache/jerry-framework/jerry/0.29.1/skills/eng-team/`.

| Path | Line anchors for specific claims |
|---|---|
| `SKILL.md` | :2–16 (agents list), :119–128 (output paths), :190–226 (8-step flow), :232–245 (state keys), :259–273 (output tree), :282–287 (5-layer governance), :296–324 (adversary + 0.95), :334–346 (constitutional table), :404–414 (routing disambiguation), :450–459 (standards URLs) |
| `agents/eng-qa.md` | :1–10 (frontmatter), :20–28 (What You Do), :30–35 (What You Do NOT Do), :37–47 (7-step framework), :49–61 (OWASP categories), :63–70 (fuzzing matrix), :73–75 (SSDF), :80–83 (workflow integration), :86 (SDL Verification), :88–94 (L0/L1/L2), :96–106 (standards), :108–113 (AD-010 degradation), :115–122 (constitutional) |
| `agents/eng-reviewer.md` | :1–10 (frontmatter, model: opus), :17–30 (What You Do), :32–37 (What You Do NOT Do), :40–50 (gate workflow), :52–61 (/adversary table, 0.95 threshold), :64–74 (S-014 dimensions), :77–80 (SSDF RV.x), :82–86 (workflow integration), :92–98 (L0/L1/L2), :111–115 (AD-010), :117–124 (constitutional) |
| `agents/eng-architect.md` | :1–10 (frontmatter, opus), :42–48 (C1–C4 threat modeling escalation + LINDDUN), :49–57 (design process), :59–63 (SSDF PO.x), :66–71 (workflow integration), :99–103 (AD-010) |
| `agents/eng-lead.md` | :1–10 (frontmatter, sonnet), :47–52 (SSDF PO/PS mapping), :77–80 (standards incl. SAMM), :84–88 (AD-010) |
| `agents/eng-devsecops.md` | :1–10 (frontmatter), :20–30 (What You Do), :53–61 (security tool matrix), :63–71 (CI/CD gate thresholds), :80–83 (SLSA L1–L3), :96–102 (L0/L1/L2), :118–122 (AD-010) |
| `agents/eng-qa.governance.yaml` | :2 (schema ref), :5 (version 1.0.0), :6 (tool_tier T3), :7–16 (identity.role/expertise/cognitive_mode), :17–20 (persona), :22–28 (guardrails incl. engagement_id_format ENG-regex), :29–35 (output levels), :36–41 (constitutional principles), :42–49 (validation post_completion_checks), :50–59 (capabilities.forbidden_actions) |
| `agents/eng-reviewer.governance.yaml` | :7 (role), :16 (cognitive_mode: convergent), :17–20 (evidence-based persona), :50–60 (reviewer-specific forbidden actions incl. "Approve deliverables below quality threshold without user override") |
| `adversary-integration.md` | :25–30 (governing H-13..H-17), :32 (eng-reviewer as integration agent), :38–49 (per-agent /adversary mapping), :62–72 (criticality × output-type strategy table), :74–82 (AE-003/AE-005 auto-escalation), :88–93 (score band PASS/REVISE/REJECTED), :95–101 (escalation protocol 1st/2nd/3rd failure), :103–111 (S-014 dimensions with weights), :117–132 (Step 7 gate procedure), :149–186 (end-to-end quality workflow ascii diagram), :188–195 (artifact-level vs engagement-level scoring) |
| `templates/security-test-plan.md` | :7 (OWASP TG + SSDF PW.7/PW.8 SSOT), :23 (when to use Steps 4–5), :50–57 (automated scanning table), :59–85 (ASVS-anchored test cases AUTH/AUTHZ/INPUT), :87–97 (fuzzing + property-based tables), :101–117 (OWASP TG coverage), :131–139 (R-011 configurable parameters incl. minimum_code_coverage=90%, fuzzing_duration_hours=4, asvs_verification_level=L2) |
| `templates/engagement-playbook.md` | :32–162 (per-step attributes + actions), :168–177 (PG-1..PG-7 phase-gate table — PG-5 is 90% coverage, PG-7 is 0.95 quality score), :180–198 (engagement-setup checklist + ENG-NNNN format), :201–211 (common workflow subsets), :213–222 (escalation procedures incl. /adversary score < 0.92 triggers revision per H-14), :226–237 (R-011 engagement parameters) |
| `composition/eng-qa.prompt.md` | :1–114 (RCCF-assembled prompt body — note `file_write`/`file_read` substitutions vs. Claude Code's native `Write`/`Read` — evidence of portability layer, ADR-PROJ010-003) |
| `composition/eng-qa.agent.yaml` | :1–2 (schema ref), :4–10 (name/version/description/skill), :11–20 (identity), :21–24 (persona), :25–26 (model.tier: reasoning_standard), :27–41 (tools.native/mcp/forbidden), :80–88 (portability block: 128k context window, model_preferences list, reasoning_strategy: adaptive, body_format: markdown) |

---

**END OF RESEARCH**
