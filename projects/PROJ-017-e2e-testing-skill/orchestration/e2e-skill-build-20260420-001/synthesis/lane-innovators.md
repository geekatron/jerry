---
agent: ps-synthesizer
phase: 1C
workflow: e2e-skill-build-20260420-001
project: PROJ-017-e2e-testing-skill
inputs_count: 5
date: 2026-04-21
---

# Phase 1C Lane Synthesis — Innovators Lane

> Cross-file synthesis of 5 innovator deep-dives for the Jerry `/e2e-testing` skill.
> This document is the "innovators half" of the master synthesis; it will be combined with
> the standards lane and eng-team baseline in Phase 2.

## Document Sections

| Section | Purpose |
|---------|---------|
| [1. Cross-File Comparison Matrix](#1-cross-file-comparison-matrix) | Innovators on rows, key dimensions on columns |
| [2. Distilled Common Patterns](#2-distilled-common-patterns) | 5–7 patterns found across 2+ innovators |
| [3. Divergences and Tensions](#3-divergences-and-tensions) | Where innovators disagree and what the tradeoffs are |
| [4. Bleeding-Edge Signals](#4-bleeding-edge-signals) | What is new in the last 12–18 months |
| [4a. Innovators Lane Gaps](#4a-innovators-lane-gaps) | Gaps not addressed by any innovator in this lane |
| [5. Recommended Design Posture](#5-recommended-design-posture-for-e2e-testing-skill-agentic-support) | How the Jerry skill should relate to each innovator |
| [6. Proposed Top-5 Distilled Principles](#6-proposed-top-5-distilled-principles-from-the-innovators-lane) | The five principles the new skill should operationalize |
| [7. Open Questions for Master Synthesis](#7-open-questions-for-master-synthesis) | What the standards lane or eng-team baseline must resolve |
| [Source Files](#source-files) | Input files with coverage notes |

---

**Synthesis Method:** All five innovator input files (inn-1 through inn-5) were read in full before any pattern, theme, tension, or principle was written. Common patterns required evidence from at least two distinct source files to be included; tensions required contradictory positions explicitly surfaced in two or more files. Vendor and single-study claims are flagged inline with `[VENDOR CLAIM]`, `[VENDOR BLOG]`, `[SKYVERN SELF-REPORTED]`, or `[SINGLE-STUDY]` at the point of citation; these flags are preserved in downstream paragraphs (principles, posture, gap implications) that reference the same claims.

---

## 1. Cross-File Comparison Matrix

| Innovator | Archetype | License | Core Pattern | Maturity Signal | Benchmark Performance | Applicability to Jerry Agentic E2E | Cost / Adoption Friction |
|-----------|-----------|---------|--------------|-----------------|----------------------|-------------------------------------|--------------------------|
| **QA Wolf** (inn-1) | Commercial managed-service platform | Proprietary (closed) | Multi-agent roster (Orchestrator / Outliner / Code Writer / Verifier / Mapping / Automation Agent); design-time code generation; deterministic Playwright/Appium output | Series B $36M (2024); 130+ customers; named on G2 / Gartner Peer Insights; active through Mar 2026 blog cadence | No independent benchmark; 700 internal scenarios nightly (vendor-self-reported) `[VENDOR CLAIM]` | HIGH for architectural patterns (named agent roster, diagnosis-first flake taxonomy, eval gym concept); LOW for direct reuse (closed source) | High — minimum ~$8,000/month integration fee; managed-service SLA gaps on weekends `[THIRD-PARTY]` |
| **Playwright MCP + Agents** (inn-2) | MCP-backed open tooling (hyperscaler) | Apache 2.0 (Playwright); MIT / Apache 2.0 (MCP server) | A11y-tree-first MCP server + Planner / Generator / Healer agent triad; mechanism-workflow separation | Playwright v1.59.1 stable; MCP server v0.0.70; Thoughtworks Radar "Assess" (AI-powered UI testing, Vol 33, Nov 2025) | No published E2E-agent benchmark; Playwright-as-framework is Thoughtworks "Adopt" | VERY HIGH — Jerry is already an MCP host; `@playwright/mcp` registers as an MCP server in `.claude/settings.local.json`; Healer maps to H-14 critic loop | Low — `npx @playwright/mcp@latest`; no cost beyond LLM inference; version instability at v0.0.x requires explicit pinning |
| **Browser-Use** (inn-3) | OSS agent SDK (general automation) | MIT | Perceive→Plan→Act→Re-assess loop; index-based DOM action grammar; four-tier interactive-element detection via CDP; LLM inference at every step | 89.2k GitHub stars; 312 contributors; YC W25; $17M seed; v0.12.6 (Apr 2026) | 89.1% WebVoyager (self-reported; 55 tasks removed; authors self-critique benchmark) | MEDIUM for direct adoption (no first-party test assertions, reporter, or fixture model); HIGH as perception / actuation substrate behind a Jerry assertion layer | Medium — MIT, free, but ~20k tokens/min/agent; every step incurs LLM inference; token cost escalates in large CI suites |
| **Skyvern 2.0** (inn-4) | OSS agent product + hosted cloud | AGPL-3.0 (OSS); proprietary (Cloud) | Planner–Actor–Validator triad; vision-LLM-driven Actor; explicit Planner working memory; Validator loops failures back to Planner (not Actor); MCP server (33 tools) + Claude Code skills | 21.3k GitHub stars; v1.0.31 (Apr 14, 2026); active weekly changelog; YC-backed | 85.85% WebVoyager at Jan-2025 launch (SOTA then; now surpassed by Surfer 2 at 97.1%, Magnitude 93.9%, Browser-Use 89.1%) | HIGH for architectural pattern (Planner–Actor–Validator triad is directly portable); MEDIUM for direct adoption (AGPL-3.0 copyleft; vision-LLM cost; no native test-authoring constructs) | Medium — AGPL constrains code reuse (pattern reuse is fine); 4–5 min latency on 5-field workflows; per-step vision-LLM cost is high for large CI suites |
| **GenIA-E2ETest** (inn-5) | Peer-reviewed academic approach | CC BY 4.0 (paper); open-source code | Three-level prompting pipeline (Scenario Modularization → UI Element Extraction → Script Generation); role-framed prompts; temperature=0 determinism; structured JSON intermediates; NL→Robot Framework via Selenium | SBES 2025 Research Track, pp. 282–292, DOI 10.5753/sbes.2025.9927; arXiv:2510.01024; no citations located yet `[SINGLE-STUDY]` | 77% element precision/recall; 85% execution recall; 6–10% manual modification rate — on n=12 test cases across 2 apps `[SINGLE-STUDY — LIMITED STATISTICAL POWER]` | HIGH for evaluation methodology and quality-gate metric formulas; MEDIUM for direct adoption (no self-healing, no SPA support, Robot Framework binding; needs Playwright adaptation) | Very low — CC BY 4.0 paper; open-source code; no runtime cost beyond LLM API; adaptation effort to Playwright is the primary friction |

---

## 2. Distilled Common Patterns

The following patterns appear across two or more innovators. Each is a cross-file signal, not a per-innovator summary.

### CP-001: Structured-Serialization as the Agent's Window onto the Page

All five innovators converge on the idea that exposing raw HTML or pixel screenshots to an LLM is wasteful or unreliable. The preferred substrate is a **structured, indexed, semantic representation of the page**:

- inn-2 (Playwright MCP): a11y-tree snapshots with `role "name" [ref=eN]` — 2–5 KB vs 500 KB+ for screenshots.
- inn-3 (Browser-Use): integer-indexed DOM tree via `ClickableElementDetector`; model sees `click(index=N)`, not CSS selectors.
- inn-5 (GenIA-E2ETest): Level 2 prompt submits real crawled HTML to the LLM specifically to ground locators in real DOM rather than prose hallucination.
- inn-4 (Skyvern): uses vision-LLM on the rendered page as primary — the outlier here, and one explicitly cited as a cost/latency liability (P-SKY-7).
- inn-1 (QA Wolf): Mapping Agent crawls the app; Outliner processes DOM snapshots + video/audio; also avoids raw-HTML prompting at scale.

**Cross-file agreement: HIGH (4/5 sources).** Skyvern is the partial outlier but acknowledges the vision-LLM cost burden.
**Implication for Jerry:** `e2e.snapshot` must return structured data (not base64 image) by default. Ground all locator generation in real DOM state before any LLM generation step.
**Sources:** inn-2 §7.2, inn-3 §7.1, inn-5 §7.3, inn-4 §P-SKY-7.

---

### CP-002: Role-Specialization Yields Measurable Accuracy Gains

Every innovator that discloses multiple agents — rather than a monolithic "do everything" agent — either reports or argues for significant accuracy improvements from role separation:

- inn-4 (Skyvern): 45% → 68.7% → 85.85% WebVoyager progression by adding Planner, then Validator as distinct roles (P-SKY-1).
- inn-1 (QA Wolf): named Orchestrator / Outliner / Code Writer / Verifier quartet with single-responsibility contracts; blog articulates "distributed decision-making" as a design principle.
- inn-2 (Playwright MCP): Planner / Generator / Healer as a three-phase workflow with distinct output artifacts (Markdown plan → spec files → patched tests).
- inn-5 (GenIA-E2ETest): three-level prompting pipeline where each level has a distinct role persona and constrained output contract.
- inn-3 (Browser-Use): perceive→plan→act→re-assess loop is a single agent, but Browser-Use's strength is as a substrate; role separation emerges in community-built testing adaptations.

**Cross-file agreement: HIGH (4/5 sources with quantified or principled evidence).** Browser-Use is the partial outlier as a general SDK without prescribed roles.
**Implication for Jerry:** The `/e2e-testing` skill must decompose into at least three distinct agents: planner (intent→plan), executor (plan→browser actions), and verifier (post-action→pass/fail/replan). Folding these roles together is an anti-pattern.
**Sources:** inn-4 §P-SKY-1/P-SKY-2, inn-1 §3.1/P2, inn-2 §7.4, inn-5 §7.2.

---

### CP-003: Validator-as-Distinct-Role (Not Embedded Retry)

This is a refinement of CP-002 but warrants its own pattern because it is the most consequential single design decision across the innovator set. The distinction is between:

- **Embedded retry** (anti-pattern): executor fails → executor retries with the same approach → cascading failures.
- **Validator as separate role** (pattern): executor acts → validator inspects observable state → on failure, validator escalates to the planner for replanning, not to the executor for blind retry.

Evidence:
- inn-4 (Skyvern): Validator is explicitly a "supervisor function... reporting errors/tweaks back to the Planner" — not to the Actor (P-SKY-2). The ~40 percentage point WebVoyager gain is attributed specifically to this architectural decision.
- inn-1 (QA Wolf): The Verifier and the Automation Agent (maintainer) are distinct agents; the Verifier confirms semantic match to intent before the Automation Agent diagnoses and repairs.
- inn-2 (Playwright MCP): Healer replays, inspects, patches, and re-runs — structural separation from the Generator — and Jerry's quality-gate principle (§7.8) explicitly caps healing loops and requires skip-with-rationale artifacts.
- inn-5 (GenIA-E2ETest): Does NOT have this pattern (acknowledged as a gap in §5.4 "no failure-mode self-healing"). The absence here strengthens the signal from the other three.

**Cross-file agreement: HIGH (3/5 with explicit evidence; 1/5 notable absence).** GenIA-E2ETest explicitly acknowledges this gap.
**Implication for Jerry:** The `e2e-verifier` agent must escalate to `e2e-author` for replanning on failure — not loop back to `e2e-executor`. This mirrors Jerry's existing H-14 creator-critic-revision cycle.
**Sources:** inn-4 §P-SKY-2, inn-1 §P3/§3.2 `[VENDOR BLOG — architectural claim, not independently verified]`, inn-2 §7.8, inn-5 §5.4 (absence case).

---

### CP-004: Deterministic Code Artifacts as the Primary Test Output

Multiple innovators distinguish between agentic reasoning at design time and deterministic execution at CI time. The principle: **the agent's job is to produce a durable, human-readable, version-controlled test artifact; the artifact — not the agent — runs in CI**.

- inn-1 (QA Wolf): "agents generate code once, then the code runs deterministically in CI — the agent is not in the runtime loop" (§3.5, P1). Strongest articulation.
- inn-5 (GenIA-E2ETest): the three-level pipeline produces a `.robot` script with 905 LOC mean length; the agent's involvement ends at generation; execution is deterministic Robot Framework/Selenium.
- inn-2 (Playwright MCP): `browser_generate_playwright_test` promotes interactive sessions to committed regression specs; the Planner→Generator→Healer workflow ends with executable `.spec.ts` files.
- inn-3 (Browser-Use): explicitly argues AGAINST the "LLM-generates-Playwright-then-Playwright-runs" pattern (§7.8) in favor of in-loop LLM. This is the main dissenter and creates Tension T-002 below.
- inn-4 (Skyvern): does not emit deterministic test code by default — a noted weakness (§5.5); the `/qa` and `/smoke-test` Claude Code skills are the closest analog.

**Cross-file agreement: MEDIUM (3/5 clearly; 1/5 dissenting; 1/5 partial).** The tension between design-time code generation and runtime in-loop LLM is the deepest architectural fault line in this lane (see Tension T-002).
**Implication for Jerry:** For known-good, regression-critical flows: generate durable Playwright test artifacts. For exploratory and self-healing flows: use in-loop LLM (Browser-Use or Skyvern-pattern). Jerry should not force one model for all use cases.
**Sources:** inn-1 §3.5/P1 `[VENDOR BLOG — architectural claim, not independently verified]`, inn-5 §2.3, inn-2 §7.7, inn-3 §7.8 (dissent), inn-4 §5.5.

---

### CP-005: Evaluation Benchmark as a First-Class Skill Artifact

Across the innovator set, publishing evaluation methodology — not just marketing claims — is a differentiator between credible and non-credible quality stories:

- inn-4 (Skyvern): published the full WebVoyager eval run at `eval.skyvern.com` with per-task reasoning traces (P-SKY-4). The transparency is unusual for a commercial YC company.
- inn-5 (GenIA-E2ETest): the most rigorous — four-metric grid (element precision/recall, execution precision/recall, manual modification rate) with exact formulas, 36 controlled runs, open Figshare archive. The only peer-reviewed approach.
- inn-1 (QA Wolf): ships a 700-scenario nightly eval gym sourced from 50M historical runs — but the results are self-reported, not external (§6 / §4.2).
- inn-2 (Playwright MCP): no published benchmark; Thoughtworks Radar "Assess" is the closest third-party signal.
- inn-3 (Browser-Use): 89.1% WebVoyager — self-reported with a candid self-critique of the benchmark's limitations (§5.5).

**Cross-file agreement: MEDIUM (3/5 with substance; 2/5 limited).** The pattern is visible; quality varies widely.
**Implication for Jerry:** The `/e2e-testing` skill MUST ship with an evaluation corpus and nightly harness. Quality claims must have a published methodology (per inn-1 §P5, inn-5 §7.6).
**Sources:** inn-4 §P-SKY-4, inn-5 §7.1, inn-1 §3.3/P4, inn-3 §5.5.

---

### CP-006: Multi-Level Prompting with Structured JSON Intermediates

Where innovators disclose their LLM architecture, they all share the pattern of decomposing generation tasks into sequential, role-framed prompts with structured (JSON) intermediate outputs rather than single monolithic prompts:

- inn-5 (GenIA-E2ETest): three levels — Scenario Modularization (JSON) → UI Element Extraction (JSON) → Script Generation (Robot Framework). The most explicit articulation (§7.2).
- inn-1 (QA Wolf): Outliner produces an AAA plan before the Code Writer generates Playwright code; the Verifier then confirms semantics — a sequential, structured pipeline.
- inn-4 (Skyvern): Planner decomposes into ordered sub-steps with explicit working memory before the Actor executes — structured intermediate state is the "completed/pending" list (P-SKY-3).
- inn-2 (Playwright MCP): Planner produces a Markdown spec before the Generator produces code — the Markdown is a structural intermediate.
- inn-3 (Browser-Use): single perceive→act loop with in-browser re-assessment; no static intermediate artifacts persisted between steps.

**Cross-file agreement: HIGH (4/5; Browser-Use is the outlier by design).** The pattern is consistent wherever a generation pipeline is disclosed.
**Implication for Jerry:** Every sub-agent in the `/e2e-testing` skill should (a) consume a structured input artifact and (b) emit a structured output artifact before the next sub-agent starts. Intermediate artifacts must be persisted to disk (P-002 compliance and replay support).
**Sources:** inn-5 §7.2, inn-1 §3.1, inn-4 §P-SKY-3, inn-2 §7.4.

---

### CP-007: DOM-Grounded Locator Generation (Anti-Hallucination Defense)

Three innovators independently identify hallucinated selectors as a primary failure mode and converge on the same defense: ground locator generation in real, crawled DOM state before any LLM generation step.

- inn-5 (GenIA-E2ETest): Level 2 explicitly submits real HTML from a crawler to the LLM specifically to prevent selector hallucination (§7.3). The outlier case WebApp1-TC5 — which showed 12% element precision — is attributed to weak locator generation.
- inn-2 (Playwright MCP): the Healer agent re-plans from accessibility snapshots on failure; element refs come from live `browser_snapshot` calls, not from prose (§7.3).
- inn-3 (Browser-Use): `ClickableElementDetector` produces the `selector_map` from live DOM traversal before the LLM acts; the model sees stable integer IDs, not invented CSS (§7.1).
- inn-4 (Skyvern): vision-LLM on the rendered page sidesteps selector hallucination via a different mechanism — but the underlying principle is the same: ground in observable reality.
- inn-1 (QA Wolf): Mapping Agent "autonomously explores the application and documents workflows" before the Code Writer generates; the same anti-hallucination discipline, different implementation.

**Cross-file agreement: HIGH (5/5 with different implementations of the same principle).**
**Implication for Jerry:** Before any locator or action is generated by an LLM, a live DOM/a11y-tree snapshot must be taken and passed to the LLM. Jerry's `e2e-planner` must never invent selectors from prose alone.
**Sources:** inn-5 §7.3, inn-2 §7.3, inn-3 §7.1/§7.3, inn-4 §1. (vision path), inn-1 §3.1.

---

## 3. Divergences and Tensions

### T-001: Closed Commercial Platform vs Open-Source Agent SDK

**Positions:**
- inn-1 (QA Wolf): managed-service + closed platform; "you get the results, not the machinery."
- inn-2/inn-3/inn-4: open-source (Apache/MIT/AGPL); you control the agent logic, the prompts, the eval corpus.
- inn-5 (GenIA-E2ETest): fully open CC BY 4.0 academic approach.

**Tradeoff:** QA Wolf's managed-service model delivers coverage-as-a-service with human engineers backstopping AI failures — this is likely the actual source of its reliability `[THIRD-PARTY corroborated, inn-1 §4.5]`. However, it is opaque (no auditable benchmark, no open code), creates framework lock-in (Playwright/Appium only), and pricing is prohibitive for small teams. The open-source alternatives expose the machinery but place the operational burden on Jerry. **There is no free lunch here**: QA Wolf's human backstop is a genuine operational capability that an open-source skill must compensate for via quality gates, eval harnesses, and explicit autonomy-tier declarations.

**Relevance to Jerry:** Jerry must explicitly declare its autonomy tier (autonomous / supervised / managed-equivalent) per inn-1 §P8. The skill cannot implicitly promise QA Wolf-level outcomes without QA Wolf-level human supervision.

---

### T-002: Design-Time Code Generation vs Runtime In-Loop LLM

**Positions:**
- inn-1 (QA Wolf) and inn-5 (GenIA-E2ETest): design-time generation; the agent produces a durable artifact; the artifact runs without LLM in the CI loop.
- inn-3 (Browser-Use): argues explicitly against this — "LLM-generates-Playwright-then-Playwright-runs loses the feedback loop" (§7.8); prefers continuous LLM reasoning with assertion tools as first-class runtime actions.
- inn-4 (Skyvern): sits in the middle — its primary output is execution traces, not test code; the `/qa` skill adapts it closer to the test-generation model.
- inn-2 (Playwright MCP): both models are present — Generator emits code (design-time), Healer re-plans at runtime (in-loop) — the tension is unresolved even within a single innovator.

**Tradeoff:**
- Design-time generation: deterministic, reviewable, versionable, cheap to run in CI; but brittle to UI drift (every change requires re-generation).
- Runtime in-loop: adaptive, self-correcting, handles dynamic SPAs; but expensive (LLM inference per CI run), non-deterministic, hard to debug, raises P-003 concerns about agent recursion at scale.

**Relevance to Jerry:** This tension is the most consequential unresolved architectural question in the innovators lane. The recommended resolution (CP-004) is a hybrid: design-time code for known-good regression flows, runtime in-loop for exploratory and self-healing contexts. The skill must make this distinction explicit to the user and must not conflate the two modes.

---

### T-003: Accessibility-Tree-First vs Vision-LLM-First as the Actor Substrate

**Positions:**
- inn-2 (Playwright MCP): accessibility-tree-first; screenshots are a fallback; 2–5 KB per snapshot vs 500 KB+ for screenshots; 10–100x token reduction.
- inn-4 (Skyvern): vision-LLM-first; this enables handling of apps with weak a11y trees (canvas-heavy, non-semantic div soup, legacy enterprise apps) but incurs 4–5 minute latencies on simple 5-field forms.
- inn-3 (Browser-Use): DOM-serialization-first with screenshot as fallback — closest to Playwright MCP's approach.

**Tradeoff:** A11y-tree-first is more efficient and cheaper for well-structured modern apps. Vision-LLM-first handles accessibility-hostile targets better. The Thoughtworks Radar "Assess" placement covers both categories — neither is "Adopt"-grade. The practical resolution depends on the application under test: accessibility-hostile legacy apps need vision; modern SPAs with good semantic HTML do not.

**Relevance to Jerry:** The skill's default actor should be Playwright MCP (a11y-tree-first) with vision-LLM as an explicit escape hatch for weak-a11y targets, not as the default. This matches inn-4 §P-SKY-7.

---

### T-004: General Automation Substrate vs Testing-Specific Product

**Positions:**
- inn-3 (Browser-Use): explicitly not a testing framework; no assertions, no test runner, no fixture model; testing use is community-built.
- inn-4 (Skyvern): primarily RPA/automation-focused; testing adaptation (via `/qa`, `/smoke-test` skills) is a secondary use case.
- inn-1 (QA Wolf): purpose-built for testing; test lifecycle (Arrange-Act-Assert), coverage reporting, and CI integration are first-class concerns.
- inn-2 (Playwright MCP): testing-first (Playwright is a test framework); Planner/Generator/Healer are testing-specific workflow agents.
- inn-5 (GenIA-E2ETest): testing-only; no automation-beyond-testing concern.

**Tradeoff:** General-purpose agent substrates (Browser-Use, Skyvern) are more flexible and have broader community support, but lack the testing-specific primitives (assertions, fixtures, reporters, BDD semantics) that define a first-class testing skill. Testing-specific products (QA Wolf, Playwright MCP, GenIA-E2ETest) provide richer test infrastructure but narrower automation surface.

**Relevance to Jerry:** The skill requires a testing-specific layer on top of general automation substrates. The question for master synthesis is whether this layer is thin (wrapping Browser-Use with assertions) or thick (reimplementing test lifecycle from scratch using Playwright as the substrate).

---

### T-005: Peer-Reviewed Evidence vs Vendor-Reported Metrics

**Positions:**
- inn-5 (GenIA-E2ETest): the only peer-reviewed source; controlled evaluation; transparent metric formulas. `[SINGLE-STUDY — LIMITED STATISTICAL POWER]`
- inn-4 (Skyvern): published eval run at eval.skyvern.com with per-task traces — high transparency for a commercial actor, but not peer-reviewed.
- inn-1 (QA Wolf): 700 nightly scenarios, 50M historical runs — entirely self-reported with no external audit. `[VENDOR CLAIM]`
- inn-2/inn-3: no published benchmark for the agentic-E2E category specifically.

**Tradeoff:** Peer review provides methodological rigor but GenIA-E2ETest's n=12 is statistically thin. Vendor benchmarks are larger-scale but unaudited. The category lacks a neutral third-party benchmark — this is an industry-wide gap, not a failing of any individual innovator.

**Relevance to Jerry:** Jerry should adopt the GenIA-E2ETest metric formulas as the internal quality gate for generated tests (execution_recall, element_precision/recall, manual_modification_rate) while acknowledging the limited external evidence base — and should invest in building its own eval corpus to transcend the single-study limitation.

---

## 4. Bleeding-Edge Signals

The following capabilities have become tractable or visible in the **last 12–18 months** (mid-2024 to April 2026) and were not feasible or published before that window.

### Signal 1: MCP as a First-Class Browser Automation Protocol (March 2025 onward)

Playwright MCP launched in **March 2025** as the first hyperscaler-backed browser automation server implementing the Anthropic MCP protocol (inn-2 §6.1 "Release Trajectory"). By April 2026, it is supported by 20+ MCP clients including Claude Code, VS Code Copilot, Cursor, Gemini CLI, and Warp. This means any MCP-capable LLM host can acquire browser automation capabilities by registering a single npm package — without building custom browser integration. This was not possible before the MCP specification (`2025-11-25`) stabilized.

**What is new:** The MCP protocol creates a standardized, composable interface between LLM reasoning and browser actions. A Jerry skill can now invoke `browser_snapshot`, `browser_click`, and `browser_verify_element_visible` as first-class MCP tool calls rather than embedding Playwright directly. This is architecturally equivalent to what REST did for API integration in 2000–2010 — it creates a stable interface layer that decouples browser capability from LLM host implementation.

### Signal 2: Planner–Actor–Validator Triads Achieving 85%+ on WebVoyager (January 2025)

Skyvern 2.0's 85.85% WebVoyager score at launch (January 2025) was the first time an openly-published three-role agentic architecture achieved above 85% on a general web-navigation benchmark (inn-4 §4.1). The progression 45% (actor-only) → 68.7% (planner added) → 85.85% (validator added) provides the first published causal evidence that role decomposition — specifically the addition of a distinct Validator — drives large accuracy gains in web agents.

By April 2026, several systems have surpassed 85% (Surfer 2 at 97.1%, Magnitude at 93.9%), but the architectural template that enabled this jump — the three-role triad — is now an established design pattern, not an experimental one.

**What is new:** The Validator-as-supervisor concept has moved from theoretical proposal to empirically validated production architecture in less than 18 months. The architecture is now a concrete, citable reference.

### Signal 3: Peer-Reviewed LLM Test Generation with Quantified Quality Metrics (SBES 2025)

GenIA-E2ETest (SBES 2025, September 2025) is the first peer-reviewed publication to establish a reproducible metric framework for evaluating LLM-generated E2E tests — with exact formulas for element precision/recall, execution precision/recall, and manual modification rate (inn-5 §7.1). The 85% execution recall and 6% median manual modification rate on its evaluation corpus represent the first externally-reviewable quality bar for this category.

**What is new:** Before SBES 2025, all quality claims in the LLM E2E test generation space were either (a) vendor-self-reported or (b) informal practitioner reports. The paper establishes a reproducible experimental protocol that Jerry can re-run to benchmark its own skill.

### Signal 4: CDP-Native Fast Paths Reducing Per-Step LLM Cost by 50% (2026)

Browser-Use's CLI redesign (announced early 2026, inn-3 §7.5 "CDP Fast Path" / §1.1 "Architecture") introduced a Chrome DevTools Protocol direct path that reduces per-command latency to ~50 ms and cuts token consumption by ~50% vs the Playwright JavaScript-bridge path. Separately, Playwright MCP's `@playwright/cli` companion reduces token usage by 4x compared to the MCP server for scripted coding-agent workflows (inn-2 §4 "Token efficiency", strength #5: "~114,000 tokens via MCP versus ~27,000 tokens via CLI — a roughly 4x reduction").

**What is new:** The assumption that "LLM-in-the-loop" automatically means expensive, slow CI runs is being challenged. Optimized CDP paths make per-step LLM inference tractable in CI contexts at reasonable cost, which partially resolves the T-002 tension.

### Signal 5: Diff-Scoped Agentic Testing as Anti-Flakiness Strategy (2025–2026)

Skyvern's `/qa` and `/smoke-test` Claude Code skills (inn-4 §P-SKY-6) introduced the pattern of reading `git diff` as the primary input to an agentic testing skill — testing only flows adjacent to changed code rather than running comprehensive coverage. This is documented as directly achieving a ~50% reduction in QA-loop duration `[SKYVERN SELF-REPORTED]` and a 2.3× lift in first-attempt PR success `[SKYVERN SELF-REPORTED]`.

**What is new:** Diff-scoped agentic testing inverts the traditional E2E model (test everything, accept high flakiness) and instead treats test scope as a function of code change surface. This was conceptually possible before, but the published evidence of efficacy at a production scale is new and directly citable.

---

## 4a. Innovators Lane Gaps

The following gaps are not addressed by any innovator in this lane. They are consolidated here to inform the master synthesis and prevent false coverage assumptions.

**Gap 1: No native assertion or fixture primitives in general-automation substrates.**
Browser-Use (inn-3) and Skyvern (inn-4) provide perception and actuation but have no first-party assertion API, test-runner lifecycle, or fixture model — testing use is entirely community-built (gap evident in inn-3 §2.2 "Boundary" and inn-4 §5.5). Any Jerry skill built on these substrates must add an assertion-and-lifecycle layer from scratch. Implication: the `/e2e-testing` skill must contribute its own assertion DSL (or adopt Gherkin Given-When-Then from std-5) rather than inheriting one from the Browser-Use or Skyvern substrate; this layer is a first-class design deliverable, not an integration detail.

**Gap 2: No standardized neutral benchmark for agentic E2E quality.**
WebVoyager is a general web-navigation benchmark, not an E2E testing quality benchmark; it measures task-completion on public sites, not assertion correctness, flake rate, or selector stability on a controlled SUT. The innovators lane offers no neutral third-party alternative: inn-5 (GenIA-E2ETest) is the closest approximation but is peer-reviewed with n=12 test cases and a limited SUT set, not a community-maintained benchmark (evident in inn-5 §5.3 "External Validity" and inn-4 §P-SKY-4, inn-3 §5.5). Implication likely: the `/e2e-testing` skill must ship its own evaluation corpus and nightly harness as a first-party quality signal; without this, any quality gate threshold (INN-P-004) is asserted without an auditable external reference, weakening the claim at each iteration.

**Gap 3: No SPA-hardening in GenIA-E2ETest.**
GenIA-E2ETest explicitly scopes to "stable-page-structure web apps" and the authors acknowledge the approach is not validated for single-page applications with client-side state, dynamic routing, or deferred DOM hydration (gap evident in inn-5 §5.3 / §5.4 "Threats to Validity"). Modern SPA coverage requires additional adaptation before the pipeline can be treated as production-grade. Implication: before the `/e2e-testing` skill can treat GenIA-E2ETest's three-level pipeline as a production-grade pattern for Jerry's target applications, the skill design must explicitly add SPA-handling steps — likely explicit `networkidle`/`domcontentloaded` wait conditions in the DOM-snapshot phase and client-side navigation intercepts — to the Level 2 UI Element Extraction stage.

**Gap 4: AGPL-3.0 restricts code reuse from Skyvern.**
Skyvern's OSS repository is licensed AGPL-3.0, which carries copyleft obligations for derivative works distributed as software. Pattern-level borrowing (architectural blueprints, agent-role decomposition, design principles) is permissible without triggering AGPL; code-level reuse — importing Skyvern source, forking modules, embedding snippets in Jerry — requires careful legal review (gap evident in inn-4 §1 license table and §5 posture guidance). Implication: the `/e2e-testing` skill design must document a clear pattern-vs-code reuse boundary for Skyvern; agent role definitions (e2e-author, e2e-executor, e2e-verifier) may reference Skyvern's architectural pattern as prior art, but any implementation artifact generated by the skill must not contain Skyvern-derived source without legal review — the skill's SKILL.md should carry a visible AGPL boundary note.

**Gap 5: No WSTG or security-testing integration in any innovator.**
All five innovators are functionally oriented: they test user flows, UI correctness, and selector stability. None integrates OWASP Web Security Testing Guide (WSTG) patterns, fuzz-testing, or security-assertion primitives. Security-testing remains out of scope for the innovators lane and is handled separately by the standards lane (OWASP WSTG). This gap is consistent across inn-1 through inn-5; no single source flags it explicitly, but the absence is uniform. Implication: the master synthesis must establish which layer of the `/e2e-testing` skill is responsible for security scenarios — the innovators lane provides no substrate for WSTG-tagged assertions, so security scenario generation and tagging (`@wstg:WSTG-v42-<CAT>-<NN>`) must be implemented by the skill itself using the standards lane posture (SP-4) as the specification authority, not any innovator substrate.

---

## 5. Recommended Design Posture for `/e2e-testing` Skill Agentic Support

### Playwright MCP — Treat as First-Class Browser MCP Server

**Posture:** Register `@playwright/mcp@0.0.70` (pinned version) as a first-class MCP server in the Jerry skill's configuration. Jerry agents (`e2e-executor`) invoke `browser_snapshot`, `browser_click`, `browser_verify_element_visible`, and the other core-8 tools via the Jerry MCP tool layer — not via raw Playwright API calls.

**Rationale:** Jerry is already an MCP host. Playwright MCP provides 50+ browser tools for free; the core-8 subset is sufficient for most functional E2E flows. The a11y-tree-first design is token-efficient and semantically stable. The Planner/Generator/Healer workflow is adoptable as a Jerry-native orchestration pattern (replacing Microsoft's bundled `init-agents` with Jerry's `/orchestration` skill so Jerry's governance — criticality classification, S-014 scoring, WORKTRACKER integration — applies).

**Caveat:** Pin the version explicitly; treat all browser tool outputs as untrusted content (quarantine frame in system prompt); expose no more than 10 primary tools in the default surface (inn-2 §7.1).

### Browser-Use — Use as Perception/Actuation Substrate for Self-Healing Flows

**Posture:** Do NOT adopt Browser-Use as the primary test runner or assertion engine. DO use its index-based action grammar, four-tier interactive-element detection, and selector-map as the perception/actuation layer for the skill's "exploratory" and "self-healing" modes. Wire Jerry's own assertion tools into the Browser-Use controller as custom actions.

**Rationale:** Browser-Use's MIT license imposes no constraints. Its 89.2k star count and 312 contributors indicate a stable, well-maintained substrate. The CDP fast path makes it viable in CI contexts. However, it has no first-party assertions, reporter, or test lifecycle — Jerry must add those. The perceived anti-pattern (LLM-generates-Playwright-then-Playwright-runs) is the wrong model for Browser-Use; the right model is LLM-in-loop with assertion tools as first-class actions.

**Caveat:** Control LLM selection explicitly (do not rely on Browser-Use's internal gateway choice; the litellm incident of March 2026 is a concrete supply-chain risk — inn-3 §5.6). Token cost is real — restrict LLM-in-loop mode to exploratory/self-healing scenarios; use design-time Playwright code for known-good regression flows.

### Skyvern — Adopt the Planner–Actor–Validator Pattern, Not the Code

**Posture:** Do NOT import Skyvern source code (AGPL-3.0 copyleft). DO adopt the three-role decomposition — `e2e-author` (Planner), `e2e-executor` (Actor), `e2e-verifier` (Validator) — as the Jerry agent triad. DO adopt the diff-scoped testing discipline from Skyvern's `/qa` skill. DO adopt the "publish-the-eval-run-not-just-the-score" transparency principle.

**Rationale:** Skyvern provides the strongest causal evidence for the architectural value of role separation (45%→85.85% on WebVoyager from adding distinct Planner and Validator roles). The architectural blueprint is freely adaptable as prior art without triggering AGPL. The diff-scoped testing principle and the Validator-escalates-to-Planner pattern are directly usable in Jerry's agent definitions.

**Caveat:** Do NOT adopt Skyvern's vision-LLM-first Actor substrate as the default; prefer Playwright MCP (a11y-tree) with vision as fallback (P-SKY-7). Skyvern's SOTA benchmark claim is time-bounded (January 2025 state); cite with date qualification.

### QA Wolf — Extract Patterns, Avoid Vendor Dependency

**Posture:** Do NOT build on or integrate QA Wolf's platform (closed source, managed service, Playwright/Appium lock-in). DO adopt: (a) the diagnosis-first 6-category flake taxonomy as Jerry's failure classification rubric; (b) the eval gym concept — a scenario corpus with nightly CI runs; (c) the multi-level explainability requirement (L0 step summary for stakeholders, L1 Playwright code for engineers); (d) the explicit autonomy-tier declaration principle.

**Rationale:** QA Wolf's architectural patterns are well-documented in public sources (qawolf.com/ai, engineering blog). The 6-category taxonomy (selector/timing/runtime/data/visual/interaction with published failure-share percentages) is the most detailed publicly available flake classification framework. The nightly eval gym concept directly inspires Jerry's quality-gate infrastructure.

**Caveat:** All quantitative multipliers from QA Wolf (`[VENDOR CLAIM]`) are unaudited and should not be cited as benchmarks. The managed-service model's reliability advantage comes from human engineers backstopping AI failures — Jerry must be explicit that its skill does not replicate this without deliberate autonomy-tier design.

### GenIA-E2ETest — Adopt Evaluation Methodology and Pipeline Architecture

**Posture:** Adopt the four-metric quality gate (element_precision, element_recall, execution_precision, execution_recall) and the manual_modification_rate metric as Jerry's primary quality gate for generated test artifacts. Adopt the three-level prompt pipeline architecture (scenario modularization → UI element extraction → script generation) with Playwright as the concrete binding instead of Robot Framework + Selenium. Adopt the Figshare-style reproducibility bundling discipline.

**Rationale:** GenIA-E2ETest is the only peer-reviewed quality framework in the innovators lane. Its metric formulas are citable, reproducible, and directly applicable to any LLM test-generation system. The three-level pipeline architecture maps cleanly onto Jerry's sub-agent chain. The CC BY 4.0 license permits unrestricted adoption.

**Caveat:** All GenIA-E2ETest claims are `[SINGLE-STUDY]` with n=12 test cases. The metric values (77% element precision/recall, 85% execution recall, 6% median MMR) are directional reference points, not industry benchmarks. The approach is scoped to stable-page-structure web apps and must be hardened for modern SPAs before it characterizes production-grade performance.

---

## 6. Proposed Top-5 Distilled Principles from the Innovators Lane

These are the five principles the `/e2e-testing` skill must operationalize. Each is traceable to one or more innovator source files.

### INN-P-001: Planner–Executor–Verifier Triad with Supervisor-Loop Escalation

**Principle:** The `/e2e-testing` skill MUST decompose into three distinct agent roles: `e2e-author` (Planner), `e2e-executor` (Actor/Generator), and `e2e-verifier` (Validator). The Verifier MUST escalate failures to the Author for replanning — not to the Executor for retry. The Executor MUST NOT contain embedded verification logic.

**Evidence:** Skyvern 2.0 demonstrated 45%→85.85% WebVoyager accuracy progression by adding distinct Planner then Validator roles (inn-4 §P-SKY-1, §P-SKY-2). QA Wolf's Verifier and Automation Agent are structurally distinct (inn-1 §3.1). Playwright MCP's Planner/Generator/Healer map to the same three roles (inn-2 §7.4). GenIA-E2ETest's three-level pipeline embeds the same separation (inn-5 §7.2).

**Testable:** A/B an executor-only pipeline vs executor+verifier+author triad on a fixed scenario suite; expect meaningfully higher first-pass success rate with the full triad.

---

### INN-P-002: Live-DOM-Grounded Locator Generation (No Prose-to-Selector Hallucination)

**Principle:** Before any LLM step that generates UI locators, selectors, or element references, the skill MUST take a live DOM/a11y-tree snapshot of the page under test and pass it to the LLM. The LLM MUST NOT invent selectors from natural-language prose alone.

**Evidence:** GenIA-E2ETest Level 2 crawls the live page specifically to prevent hallucinated selectors (inn-5 §7.3). Playwright MCP's element-ref model (`role "name" [ref=eN]`) grounds all click/type actions in live snapshot output (inn-2 §7.3). Browser-Use's `ClickableElementDetector` produces the `selector_map` from live DOM traversal before the LLM acts (inn-3 §7.1). The WebApp1-TC5 outlier in inn-5 — 12% element precision — is attributed to locator generation without sufficient DOM grounding.

**Testable:** Compare element precision/recall on the same test scenarios with and without a live DOM snapshot in the LLM prompt; expect convergence toward GenIA-E2ETest's 77% benchmark (with further gains possible with a11y-tree over raw HTML).

---

### INN-P-003: Durable Artifact Emission for Regression-Critical Flows; In-Loop LLM for Exploratory/Healing Flows

**Principle:** The skill MUST support two execution modes. In **codegen mode**, the agent produces a committed Playwright test file that runs deterministically in CI without LLM in the loop. In **explorer mode**, the LLM remains in the loop during execution (Browser-Use-pattern), with assertion tools registered as first-class actions. The skill MUST make the mode explicit to the user and must not default to explorer mode for regression-critical flows.

**Evidence:** inn-1 (QA Wolf) §3.5/P1 `[VENDOR BLOG — architectural claim, not independently verified]`: "agents emit Playwright code; code runs in CI without an LLM in the loop." inn-5 (GenIA-E2ETest) §2.3: pipeline produces a `.robot` script; execution is deterministic. inn-3 (Browser-Use) §7.8 argues the opposite for in-loop mode but explicitly frames it as complementary, not exclusive. Tension T-002 is unresolved in the innovator lane and explicitly requires both modes.

**Testable:** Run the same regression suite in both modes over 30 CI runs; expect codegen mode to have lower per-run cost and lower flakiness rate on known-good flows; expect explorer mode to recover from selector drift that codegen mode cannot.

---

### INN-P-004: Published Quality Gate with Exact Metric Formulas

**Principle:** The skill MUST ship with a published quality gate for generated test artifacts using the GenIA-E2ETest metric framework: execution_recall ≥ 0.80, element_precision ≥ 0.70, manual_modification_rate ≤ 0.15 (first-release bar; tightening to 0.85/0.77/0.10 as the skill matures). The metric formulas (C/G, C/E, CS/GS, CS/ES) MUST be documented in the skill's SSOT. All quality claims MUST cite the corpus they are computed against.

**Evidence:** inn-5 (GenIA-E2ETest) §7.1 provides exact metric formulas and reported values (77%/77%/85%/6% median MMR). inn-4 (Skyvern) §P-SKY-4: "any claimed quality metric must be accompanied by a publishable per-task trace." inn-1 (QA Wolf) §P5: "coverage claim MUST cite the methodology and corpus it is computed against." The absence of a neutral third-party benchmark is an industry-wide gap (inn-1 §5.7); Jerry's own corpus is the compensating control.

**Testable:** At skill release, the quality gate is computed against the eval corpus; gate PASS/FAIL and per-metric values are persisted as artifacts and visible in the WORKTRACKER.

---

### INN-P-005: Diff-Scoped Test Generation as the Default Entry Point

**Principle:** The skill's primary invocation mode MUST accept a `git diff` as input and scope generated tests to flows adjacent to changed code — explicitly avoiding comprehensive coverage generation as the default. Comprehensive coverage generation is opt-in (with explicit user confirmation).

**Evidence:** inn-4 (Skyvern) §P-SKY-6: the `/qa` and `/smoke-test` Claude Code skills read git diffs and test only adjacent flows; Skyvern explicitly frames this as avoiding "the typical fate of end-to-end tests, which slowly turn into a giant flaky suite nobody trusts." The 50% QA-loop reduction `[SKYVERN SELF-REPORTED]` and 2.3× PR-success lift `[SKYVERN SELF-REPORTED]` are the evidence base. inn-3 (Browser-Use) §7.4: "gate in-loop LLM behind a criticality level" is the equivalent principle for the explorer mode.

**Testable:** Compare flakiness rate and suite maintenance cost over a 30-day window between diff-scoped suites and comprehensive suites on the same codebase; expect diff-scoped to win on both.

---

## 7. Open Questions for Master Synthesis

The following questions cannot be resolved from the innovators lane alone. They require input from the standards lane synthesis (ISTQB/gTAA/ISO standards), the eng-team baseline, or both.

### OQ-001: How does diff-scoped agentic testing (INN-P-005 / P-SKY-6) map onto ISTQB gTAA's layered test architecture?

The gTAA specifies Test Execution Layer, Test Adaptation Layer, Test Definition Layer, and Test Management Layer. Diff-scoped test generation is driven by a dynamic signal (git diff) that may not have a defined home in the gTAA layer model. Does it sit in the Test Management Layer (change-impact analysis)? Does it require a new "Test Scoping Agent" layer? The standards lane must clarify.

### OQ-002: How should the Planner's explicit working memory (P-SKY-3) be reconciled with ISTQB's test-design technique requirements?

Skyvern's Planner maintains a "completed/pending" list as working memory across steps. ISTQB gTAA's Test Definition Layer prescribes specific test-design techniques (equivalence partitioning, boundary value analysis, decision table testing). How does an agent's dynamic working memory relate to the structured test-design artifacts that standards require? Does the working memory partially fulfill traceability requirements, or must it be supplemented by a formal test-design artifact?

### OQ-003: Does the skill's dual-mode design (codegen + explorer) comply with ISTQB's "maintainable test suite" requirements?

Explorer mode (in-loop LLM) produces execution traces rather than durable code artifacts. ISTQB emphasizes maintainability of test suites. Are execution traces a compliant substitute for version-controlled test scripts in a standards-governed test process? Or must all "official" regression tests exist as code artifacts regardless of mode?

### OQ-004: What is the eng-team's actual SUT profile — a11y-tree-compatible or a11y-hostile?

The choice between Playwright MCP (a11y-tree-first) and Skyvern-pattern vision-LLM (for a11y-hostile apps) depends critically on the accessibility profile of the SUT. The innovators lane recommends Playwright MCP as default but cannot answer the SUT-specific question. The eng-team baseline must characterize the target applications: percentage of canvas/WebGL elements, SPA framework, accessibility-attribute coverage.

### OQ-005: How should agentic self-healing (inn-1/inn-4 Validator loop) reconcile with ISTQB's incident-reporting and defect-management requirements?

When the Validator triggers a replan and the Executor succeeds on the second attempt, has a defect been discovered and remediated automatically? ISTQB and IEEE 829 expect test incidents to be recorded. Does silent self-healing violate test-process integrity? The standards lane must advise.

### OQ-006: Is the GenIA-E2ETest quality gate metric set (execution_recall, element_precision/recall, MMR) compatible with the ISTQB coverage criteria used by the eng team?

The two metric systems may use different denominators (ground-truth test cases vs code coverage vs requirements-to-test traceability). If the eng team's existing coverage framework uses ISTQB-prescribed metrics, Jerry must either translate between them or adopt a unified metric set. The standards lane and eng-team baseline must jointly resolve this.

---

## Source Files

| Source | Type | Key Contribution | Patterns Contributed |
|--------|------|------------------|---------------------|
| `research/deep-innovators/inn-1-qa-wolf.md` | Commercial platform deep-dive | Named multi-agent roster (Orchestrator/Outliner/Code Writer/Verifier); 6-category flake taxonomy; eval gym concept; deterministic code emission principle; explicit P-022 honesty flags on all vendor claims | CP-001, CP-002, CP-003, CP-004, CP-005, CP-006, CP-007; INN-P-001, INN-P-004 |
| `research/deep-innovators/inn-2-playwright-mcp.md` | MCP-backed open tooling deep-dive | A11y-tree-first design; element-ref model; Planner/Generator/Healer triad; mechanism-workflow separation; curated core-8 tool set; security posture (quarantine frame, version pinning); 4x token efficiency of CLI vs MCP | CP-001, CP-002, CP-003, CP-004, CP-006, CP-007; INN-P-001, INN-P-002, INN-P-003 |
| `research/deep-innovators/inn-3-browser-use.md` | OSS agent SDK deep-dive | Index-based action grammar; four-tier interactive-element detection; `selector_map` as audit log; perceive→plan→act→re-assess loop; CDP fast path; action-extension pattern for assertions; LLM-in-loop vs code-generation tension (T-002 primary source) | CP-001, CP-002, CP-004 (dissent), CP-006 (outlier), CP-007; INN-P-002, INN-P-003 |
| `research/deep-innovators/inn-4-skyvern.md` | OSS agent product deep-dive | Planner–Actor–Validator triad with causal accuracy evidence (45%→85.85%); Validator-escalates-to-Planner pattern; Planner working memory; diff-scoped testing (/qa, /smoke-test); publish-eval-run principle; AGPL-3.0 pattern-vs-code reuse guidance | CP-001 (outlier), CP-002, CP-003, CP-004, CP-005, CP-006; INN-P-001, INN-P-003, INN-P-004, INN-P-005 |
| `research/deep-innovators/inn-5-genia-e2etest.md` | Academic/peer-reviewed deep-dive (SBES 2025) | Three-level prompting pipeline; role-framed prompts; temperature=0 determinism; DOM-grounded locator generation; four-metric quality gate (element precision/recall, execution precision/recall, manual modification rate) with exact formulas; Figshare reproducibility bundling. All quantitative claims marked `[SINGLE-STUDY]` | CP-001, CP-002, CP-004, CP-005, CP-006, CP-007; INN-P-002, INN-P-004 |
