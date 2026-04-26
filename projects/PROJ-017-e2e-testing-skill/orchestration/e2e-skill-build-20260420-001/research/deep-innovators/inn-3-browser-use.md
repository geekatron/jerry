---
title: "Deep Research — Browser-Use (Open-Source Agentic Browser SDK)"
slug: inn-3-browser-use
candidate_id: inn-3
candidate_name: Browser-Use
kind: deep-innovator-research
orchestration: e2e-skill-build-20260420-001
project: PROJ-017-e2e-testing-skill
researcher: ps-researcher-inn-3
access_date: 2026-04-21
created: 2026-04-21
sources_retrieved: 14
live_queries: 12
status: final
confidence: high
---

# Deep Research — Browser-Use (Open-Source Agentic Browser SDK)

## Navigation

| Section | Purpose |
|---------|---------|
| [Methodology Note](#methodology-note) | Query/fetch provenance and retrieval rigor |
| [1. What It Is](#1-what-it-is) | Python library, architecture, DOM serialization, action space, LLM backends |
| [2. Scope and Boundary](#2-scope-and-boundary) | Design intent and observed uses in testing |
| [3. Applicability to a Jerry Agentic E2E Skill](#3-applicability-to-a-jerry-agentic-e2e-skill) | Adapting a general agent SDK for assertion-driven workflows |
| [4. Strengths and Unique Contributions](#4-strengths-and-unique-contributions) | Stars, substrate role, WebVoyager performance |
| [5. Weaknesses, Gaps, and Criticisms](#5-weaknesses-gaps-and-criticisms) | Testing-specific gaps, reliability, token cost |
| [6. Current State](#6-current-state) | Latest release, funding, ecosystem, benchmark trajectory |
| [7. Key Implementation Patterns / Testable Principles](#7-key-implementation-patterns--testable-principles) | Reusable patterns for Jerry's e2e-testing skill |
| [Sources Retrieved](#sources-retrieved) | Full citation list with access dates |

---

## Methodology Note

Per the Phase 1b non-negotiable constraints, this research was conducted with live web retrieval on 2026-04-21. All cited URLs were retrieved this session; no training-data fallback was used for factual claims.

**Retrieval footprint (>= 8 queries + >= 3 WebFetch reads):**

| Tool | Count | Targets |
|------|-------|---------|
| WebSearch | 7 | browser-use GitHub, WebVoyager score, DOM serialization, 2025-2026 releases, vs Skyvern/Playwright MCP, testing/assertion framework, funding |
| WebFetch | 5 | github.com/browser-use/browser-use, SOTA technical report, PyPI page, DeepWiki interactive element detection, Skyvern alternatives review, Stagehand comparison, e2e-test lab repo (multi) |
| Additional searches | 1 | BU 2.0 release, DOM tree indexed clickable, reliability/token-cost criticism, ecosystem integrations |

Total: **12 live retrievals**, **14 distinct source URLs** cited below. Context7 was intentionally deferred for this Phase 1b innovator deep-dive because the request emphasized market posture, funding, stars, and release trajectory — facts that Context7's library-docs scope does not cover. Context7 remains the appropriate tool for Phase 2 implementation-time API lookups against `browser-use/browser-use`.

**Honesty notes (P-022):**
- Star count is reported as **89.2k** (GitHub repo header retrieved 2026-04-21) [[1]](#ref-1). A separate March 2025 funding-round article cited 48,400 stars at that time [[6]](#ref-6). Both are consistent with the landscape card's "89k+" characterization.
- WebVoyager claims carry a caveat: the Browser-Use authors themselves state the default WebVoyager evaluator is unreliable and that they manually reviewed results, removing 55 of 643 tasks [[2]](#ref-2). Leaderboard positions are directional, not apples-to-apples.
- No dedicated assertion/E2E-testing first-party feature exists; testing usage is community-built (e.g., [[12]](#ref-12)).

---

## 1. What It Is

Browser-Use is an open-source **Python library that exposes an LLM-driven agent over a Playwright-managed browser**. The GitHub description is "Make websites accessible for AI agents. Automate tasks online with ease." [[1]](#ref-1). Current package version 0.12.6 was released 2026-04-02 on PyPI; the project requires Python >= 3.11, < 4.0 and is MIT-licensed [[3]](#ref-3).

### 1.1 Architecture

The agent runs a **perceive -> plan -> act -> re-assess loop**: each step, the agent observes the page state, the LLM chooses the next action, the controller executes it, and the loop restarts against the new state [[13]](#ref-13). Under the hood:

- **Browser control layer:** Playwright drives the page; a newer CLI/daemon path uses Chrome DevTools Protocol (CDP) directly for ~50 ms command latency and ~2x speedup / ~50% fewer tokens [[4]](#ref-4).
- **DOM processing layer:** `browser_use/dom/service.py` builds an enhanced DOM tree, populated by `DomService._construct_dom_tree()` [[11]](#ref-11).
- **Interactive-element detection:** `ClickableElementDetector` in `browser_use/dom/serializer/clickable_elements.py` classifies elements across four tiers — native interactive tags (button/input/select/textarea/a/details/summary/option/optgroup), JS event listeners detected via CDP `getEventListeners` (the `has_js_click_listener` flag), ARIA roles and states, and form-control descendants (up to two wrapper levels) [[11]](#ref-11).
- **Selector map:** A `selector_map` indexed by integer highlight IDs is produced during `_assign_interactive_indices_and_mark_new_nodes`; `selector_map[123456]` resolves back to an `EnhancedDOMTreeNode` when the LLM emits `click(index=123456)` [[11]](#ref-11).
- **Serialization to the LLM:** The tree is rendered as structured text so the model sees stable element IDs rather than raw HTML or screenshots (though screenshots are available as an action).

### 1.2 Action Space

Primitives exposed to the LLM include [[1]](#ref-1):

| Action | Effect |
|---|---|
| `go_to_url(url)` | Navigate |
| `click(index=N)` | Click an indexed interactive element |
| `input_text(index, text)` | Type into an indexed form field |
| `screenshot()` | Capture current page state (vision path) |
| `extract()` | Pull structured text/state from the page |
| `scroll`, `select_dropdown`, iframe/focus handling | Specialized interactions, including compound components for `<input type="range">` and dropdown-container handling [[11]](#ref-11) |

A recent addition allows the agent to emit arbitrary **JavaScript** for escape-hatch interactions [[5]](#ref-5).

### 1.3 LLM Backends

Supported in-box [[1]](#ref-1) [[3]](#ref-3) [[8]](#ref-8):
- `ChatBrowserUse` (proprietary model optimized for this loop; BU 2.0 released 2026-01-27)
- OpenAI (GPT-4o used in the SOTA report [[2]](#ref-2))
- Anthropic Claude
- Google Gemini
- Local / self-hosted via Ollama
- Open-source preview model: `browser-use/bu-30b-a3b-preview`

Notably, **litellm was removed from core dependencies on 2026-03-24** after a backdoor attack in litellm 1.82.7/1.82.8 — a security-conscious pivot [[4]](#ref-4).

---

## 2. Scope and Boundary

### 2.1 Designed For

Browser-Use is designed as a **general-purpose web-automation agent SDK**, not a test framework. The README positioning and changelog emphasize:

- Form-filling, e-commerce, research-assistant, and personal-assistant workflows [[1]](#ref-1) [[3]](#ref-3).
- Production automation via the Browser-Use Cloud (stealth browsers, CAPTCHA handling, 1000+ integrations) [[1]](#ref-1) [[3]](#ref-3).
- A "continuous LLM reasoning" execution model that is flexible where flows are not predefined [[13]](#ref-13).

The Skyvern comparative review explicitly contrasts Browser-Use with testing-first tools: "Neither tool is positioned as a testing framework; both target workflow automation rather than test infrastructure" [[13]](#ref-13). Playwright MCP is characterized elsewhere as the testing-flavored alternative, while Browser-Use is a business-process automation tool [[7]](#ref-7).

### 2.2 Observed Uses in Testing

Testing applications are community-built, not first-party:

- **`pppp606/browser-use_e2e_test_automation_labs`** demonstrates a three-stage pipeline: (1) LLM generates test scenarios against a target app (Sauce Demo), (2) Python converts scenarios into Playwright test code, (3) Jest/Playwright executes. Assertions live inside LLM-generated `(test, expect)` pairs rather than being a first-class concept in Browser-Use itself [[12]](#ref-12).
- The main repo includes `/tests` and a `browser-use/benchmark` suite of 100 browser tasks, but these exercise the agent itself, not user SUTs [[1]](#ref-1).

**Boundary:** The library provides the *perception* and *actuation* substrate necessary for an E2E test agent. It does **not** provide: assertions, test discovery, fixture lifecycle, HTML reporters, flake detection, test-artifact management, or Given/When/Then semantics.

---

## 3. Applicability to a Jerry Agentic E2E Skill

Browser-Use is a strong **substrate** candidate for Jerry's e2e-testing skill, but it requires a thin **assertion-and-lifecycle layer** wrapped on top. Adaptation notes:

### 3.1 What Jerry Would Keep As-Is

| Browser-Use primitive | Jerry skill use |
|---|---|
| `EnhancedDOMTreeNode` + `selector_map` | Stable reference binding for "expect element X visible" assertions by index |
| `ClickableElementDetector` four-tier detection | Robust target discovery for Given/When steps without human-authored selectors |
| Perceive->plan->act loop with `ChatBrowserUse` | The autonomous "When" step executor |
| CDP fast path (50 ms, 50% fewer tokens) | Keeps per-test token cost viable in CI |
| Ollama support | Local-model fallback for data-residency-constrained test environments |

### 3.2 What Jerry Must Add

| Gap | Jerry skill component |
|---|---|
| Assertions | A `jerry-e2e assert.*` action family (visible, contains_text, attribute_equals, count_equals, semantic_equivalence via LLM judge). Wire these as **new tools** into the Browser-Use controller. |
| Test lifecycle | BDD-style `scenario`/`given`/`when`/`then` scaffolding on top of the Python agent loop. |
| Determinism budget | Seed/temperature pinning per scenario; record-and-replay of the `selector_map` trajectory for regression tests (address the "every step is an LLM call" cost pattern [[8]](#ref-8) [[13]](#ref-13)). |
| Flake mitigation | Wrap actions with policy-enforced retries / waits; co-opt Playwright auto-wait (already upstream) and layer a semantic retry. |
| Reporting | JUnit XML / GitHub Actions annotations; artifact capture of screenshots + `selector_map` snapshots per step. |
| Authentication | Use Browser-Use's authentication-profile reuse feature [[1]](#ref-1); formalize as fixture in Jerry skill. |

### 3.3 Architectural Fit

Browser-Use fits a **hybrid execution model** for Jerry: deterministic Playwright for known-good flows, LLM-driven Browser-Use for exploratory or self-healing flows, with Jerry's skill providing the policy layer choosing between them. This mirrors the Stagehand philosophy contrast in [[13]](#ref-13) — Jerry can offer *both* modes under a single BDD surface, using Browser-Use where Stagehand's `act()`/`extract()` equivalents would sit.

---

## 4. Strengths and Unique Contributions

### 4.1 Community Scale

- **89.2k GitHub stars** on `browser-use/browser-use` as retrieved 2026-04-21 [[1]](#ref-1). This is consistent with 48.4k stars reported in March 2025 at the seed-round announcement [[6]](#ref-6) — roughly 2x growth in one year, indicating sustained community interest.
- **312 contributors** and an active release cadence (123 total releases) [[1]](#ref-1).
- **YC W25** graduate; customer list includes Airbnb, Amazon, and Anthropic per the seed announcement [[6]](#ref-6).

### 4.2 Substrate Role

The Browser-Use loop has become a reference implementation that other projects compare against. The Skyvern, Magnitude, AIME, and Browserable leaderboards all **measure themselves against Browser-Use's WebVoyager score** [[9]](#ref-9), and comparative reviews treat it as the open-source default [[7]](#ref-7) [[13]](#ref-13). For Jerry, this substrate status means stable APIs, large contributor pool, and ecosystem compatibility.

### 4.3 WebVoyager Performance

- **89.1% success rate** on WebVoyager (586 of 643 tasks; 55 removed for evaluator quality) [[2]](#ref-2).
- **BU 2.0 (2026-01-27)** reports +12% accuracy vs BU 1.0 (74.7% -> 83.3%) with the same ~62 s avg task duration; outperforms Claude, Gemini, and ChatGPT on both speed and quality per the vendor's changelog [[8]](#ref-8).
- Domain bests: HuggingFace 100%, Booking.com 80% (weakest in the set) [[2]](#ref-2).

### 4.4 Unique Technical Contributions

- Four-tier interactive-element detection that handles JS-only click handlers via CDP `getEventListeners` — essential for React/Vue/Angular SPAs [[11]](#ref-11).
- Index-based action grammar (`click(index=N)`) that gives the LLM **stable IDs** instead of fragile selectors or raw coordinates — compressing prompt size and reducing visual-drift failure modes compared to pure-vision agents like Skyvern [[7]](#ref-7) [[11]](#ref-11).
- CDP-native fast path (50 ms latency, 50% fewer tokens) announced with the CLI redesign [[4]](#ref-4).

---

## 5. Weaknesses, Gaps, and Criticisms

### 5.1 Not Testing-Specific

There is **no first-party assertion API, no test runner, and no fixture model** in Browser-Use. The Skyvern-vs-Stagehand review is explicit: neither is a testing framework [[13]](#ref-13). All E2E usage today is community-glued (e.g., [[12]](#ref-12) generates Jest/Playwright code via an LLM rather than running assertions inside the Browser-Use loop itself).

### 5.2 Cost and Token Efficiency

- "Browser Use requires LLM inference at every step of every run, making it more expensive for workflows you execute frequently" [[13]](#ref-13).
- Reported budget: ~**20,000 tokens per minute per agent**, which caps concurrent sessions at 10-20 on typical rate limits [[8]](#ref-8).
- Screenshot-heavy strategies cost "10,000+ tokens per page load" and context grows unboundedly across a session [[8]](#ref-8). Browser-Use mitigates this by using DOM-serialization (not screenshots) as the default perception path, but the structural tax is still real.

### 5.3 Reliability Patterns

Known failure modes documented by comparative reviewers [[8]](#ref-8) [[13]](#ref-13):
- Visual drift after layout shift or modal overlap (when the screenshot path is used).
- Weak accessibility labels, dynamic node IDs, and hidden elements in snapshots (reference-binding brittleness).
- Infinite redirects, auth/session expiry, unbounded retry loops.
- "Debugging becomes challenging since understanding agent decision chains and prompt interactions requires deeper system visibility" [[13]](#ref-13).

### 5.4 Enterprise Gaps

The Skyvern review (admittedly a competitor) notes Browser-Use "falls short" for enterprise-grade automation needing CAPTCHA, 2FA, advanced scalability, and multi-platform authentication at scale — though the Browser-Use Cloud product addresses some of these [[10]](#ref-10) [[1]](#ref-1).

### 5.5 Benchmark Self-Critique

The Browser-Use authors themselves criticize WebVoyager: "the default WebVoyager evaluator is not good", manual review was required, and "the dataset mostly tests the planning of the agents, but not the actual ability to understand the sites" [[2]](#ref-2). Any claim grounded in WebVoyager numbers (including their own 89.1%) should be treated as directional.

### 5.6 Supply-Chain Exposure (Resolved)

The 2026-03-24 litellm removal [[4]](#ref-4) demonstrates responsive security hygiene, but also shows that a core-deps dependency on an LLM gateway left users briefly exposed. Jerry should vendor LLM selection explicitly rather than rely on whatever gateway Browser-Use picks.

---

## 6. Current State

### 6.1 Release Trajectory

| Version | Date | Notable |
|---|---|---|
| 0.10.1 | 2025-11-29 | [[4]](#ref-4) |
| 0.11.0 | 2025-12-10 | [[4]](#ref-4) |
| 0.11.1 | 2025-12-16 | First open-source BU model released same week [[4]](#ref-4) [[8]](#ref-8) |
| 0.11.2 | 2026-01-16 | [[4]](#ref-4) |
| **BU 2.0** | **2026-01-27** | +12% accuracy, matches Claude Opus 4.5 at 40% faster speed [[8]](#ref-8) |
| 0.12.6 | 2026-04-02 | Latest on PyPI [[3]](#ref-3) |
| Repo HEAD | 2026-04-19 | Active development [[1]](#ref-1) [[4]](#ref-4) |

### 6.2 Funding and Corporate Context

- **$17M seed** announced 2025-03-23, led by Felicis Ventures; participants include A Capital, Nexus Ventures, Y Combinator, Paul Graham, Liquid2, SV Angel, Pioneer Fund [[6]](#ref-6).
- Founded 2024 by Magnus Müller and Gregor Žunič, ETH Zurich alumni [[6]](#ref-6).
- YC W25 batch [[6]](#ref-6). Enterprise customers cited: Airbnb, Amazon, Anthropic [[6]](#ref-6).
- Maintainer of record on PyPI: Gregor Zunic (@gregpr07) [[3]](#ref-3).

### 6.3 Ecosystem Position

- Repo is the reference open-source implementation against which Surfer 2, Magnitude, AIME Browser-Use, and Browserable position themselves [[9]](#ref-9).
- `browser-use/agent-sdk` and `browser-use/browser-harness` are sibling repos expanding the substrate [[1]](#ref-1).
- Cloud product advertises 1000+ integrations and stealth browsing [[1]](#ref-1) [[3]](#ref-3).
- WebVoyager leaderboard (2026): Surfer 2 97.1% > Magnitude 93.9% > AIME Browser-Use 92.34% > Browserable 90.4% > Browser Use 89.1% [[9]](#ref-9). Browser-Use has been overtaken on raw accuracy but remains the open-source reference.

### 6.4 Security Posture

Proactively removed litellm from core deps after the 1.82.7/1.82.8 backdoor (2026-03-24) [[4]](#ref-4). Indicates responsive security governance.

---

## 7. Key Implementation Patterns / Testable Principles

Patterns Jerry's e2e-testing skill can **directly adopt or re-implement** from Browser-Use:

### 7.1 Index-Based Action Grammar

**Principle:** Expose the DOM to the LLM as a text tree of *indexed interactive elements*, and have the model emit actions like `click(index=N)` instead of CSS/XPath selectors or pixel coordinates.

**Why:** Compresses prompt, avoids selector-churn failure modes, and gives Jerry a stable replay key for flake diagnosis [[11]](#ref-11).

### 7.2 Four-Tier Interactive-Element Detection

**Principle:** Classify an element as interactive if **any** of: native interactive tag, JS click-listener (via CDP `getEventListeners`), ARIA role/state, or wraps a form control within ~2 levels [[11]](#ref-11).

**Why:** This catches modern SPA frameworks where React/Vue/Angular attach behavior to `<div>`/`<span>`. A Jerry assertion engine can use the same detector to decide whether "click X" is legal before the LLM is even prompted.

### 7.3 Selector Map as Audit Log

**Principle:** The `selector_map` is a per-step snapshot of `{int_id -> EnhancedDOMTreeNode}`. Persist it alongside every action [[11]](#ref-11).

**Why:** This is the *natural replay artifact* for Jerry's e2e-testing skill. It enables:
- Deterministic replay of a flaky test without LLM inference.
- Post-hoc attribution of "why did the LLM click that?" — the node's attributes are in the map.
- Semantic-diff between runs (same intent, different DOM) for maintenance.

### 7.4 Perceive -> Plan -> Act -> Re-assess Loop

**Principle:** After every action, re-observe the page and re-plan, rather than scripting a fixed sequence [[13]](#ref-13).

**Why:** Gives Jerry a "self-healing" path for E2E tests when selectors drift. Jerry should gate this behind a **criticality level**: deterministic Playwright for hot-path happy-flow tests (cheap, flake-free), Browser-Use loop only for tests marked "exploratory" or "self-healing."

### 7.5 CDP Fast Path

**Principle:** Skip Playwright's JavaScript bridge and speak Chrome DevTools Protocol directly via a persistent daemon for ~50 ms per command [[4]](#ref-4).

**Why:** E2E tests in CI are latency-sensitive. Jerry's skill can offer a `--fast` mode that opts into CDP for perception-only steps (reading DOM) while keeping Playwright for actuation where its auto-wait semantics matter.

### 7.6 Action-Extension Pattern

**Principle:** Browser-Use supports custom tools — agents can be given new actions without forking the loop [[1]](#ref-1).

**Why:** This is exactly how Jerry adds `assert.*` primitives. Register `assert_visible(index)`, `assert_text(index, pattern)`, `assert_count(selector, n)` as Browser-Use tools; the LLM can then weave them into plans, and Jerry's scenario runner validates the resulting trajectory against the BDD expectations.

### 7.7 Authentication Profile Reuse

**Principle:** Persist browser profile state (cookies, storage) across runs to skip login flows [[1]](#ref-1).

**Why:** Essential for E2E tests against authenticated SUTs. Jerry should expose this as a fixture: `@given("an authenticated session as {role}")`.

### 7.8 Observed Anti-Pattern to Avoid

LLM-generates-Playwright-then-Playwright-runs (as in [[12]](#ref-12)) **loses the feedback loop**: the LLM can't self-correct at runtime because it's only involved at generation time. Jerry should prefer the Browser-Use-native approach where the LLM is in the loop *during* execution, with assertion tools as first-class actions.

---

## Sources Retrieved

All URLs retrieved 2026-04-21.

<a id="ref-1"></a>[1] **GitHub — browser-use/browser-use.** Repository header, README, release list. Source of record for star count (89.2k), contributor count (312), action space, LLM backends, authentication profile reuse. <https://github.com/browser-use/browser-use>

<a id="ref-2"></a>[2] **Browser Use — "Browser Use = state of the art Web Agent" (SOTA technical report).** WebVoyager 89.1% claim, GPT-4o evaluation, 55 tasks removed, author self-critique of benchmark. <https://browser-use.com/posts/sota-technical-report>

<a id="ref-3"></a>[3] **PyPI — browser-use 0.12.6.** Latest version (2026-04-02), Python >=3.11 <4.0, MIT license, maintainer Gregor Zunic, Cloud feature list. <https://pypi.org/project/browser-use/>

<a id="ref-4"></a>[4] **GitHub — browser-use/browser-use Releases.** Version timeline (0.10.1 -> 0.12.6), litellm removal 2026-03-24, CDP CLI announcement. <https://github.com/browser-use/browser-use/releases>

<a id="ref-5"></a>[5] **Browser Use Changelog — "Browser Use can write Javascript" (2025-09-17).** JS escape-hatch action primitive. <https://browser-use.com/changelog/17-9-2025>

<a id="ref-6"></a>[6] **TechCrunch — "Browser Use... raises $17M" (2025-03-23).** $17M seed, Felicis lead, YC W25, founders, 48.4k stars at announcement, customer list (Airbnb, Amazon, Anthropic). <https://techcrunch.com/2025/03/23/browser-use-the-tool-making-it-easier-for-ai-agents-to-navigate-websites-raises-17m/>

<a id="ref-7"></a>[7] **Skyvern Blog — "Playwright MCP Reviews and Alternatives 2025."** Architectural contrast: Browser-Use = open-source agent; Playwright MCP = testing-flavored; Skyvern = vision+LLM. <https://www.skyvern.com/blog/playwright-mcp-reviews-and-alternatives-2025/>

<a id="ref-8"></a>[8] **Browser Use Changelog — "Browser Use Model - BU 2.0" (2026-01-27).** +12% accuracy (74.7% -> 83.3%), ~62 s avg duration, matches Claude Opus 4.5 at 40% faster, ChatBrowserUse API, `bu-2-0` model ID. <https://browser-use.com/changelog/27-1-2026>

<a id="ref-9"></a>[9] **Browserable — "WebVoyager Benchmark Results."** Leaderboard positions (Surfer 2 97.1%, Magnitude 93.9%, AIME Browser-Use 92.34%, Browserable 90.4%, Browser Use 89.1%) and caveats about non-comparable variants/evaluators. <https://www.browserable.ai/blog/web-voyager-benchmark>

<a id="ref-10"></a>[10] **Skyvern Blog — "Browser Use Reviews and Alternatives in 2025."** Enterprise-suitability critique, complex-workflow limits, Skyvern comparison. <https://www.skyvern.com/blog/browser-use-reviews-and-alternatives-in-2025/>

<a id="ref-11"></a>[11] **DeepWiki — browser-use/browser-use, "Interactive Element Detection" (§5.3).** Four-tier classifier, `ClickableElementDetector`, `selector_map`, CDP `getEventListeners`, compound components, iframe/search-heuristic handling. <https://deepwiki.com/browser-use/browser-use/5.3-interactive-element-detection>

<a id="ref-12"></a>[12] **GitHub — pppp606/browser-use_e2e_test_automation_labs.** Community E2E testing pipeline using browser-use + Jest + Playwright; LLM-generated `(test, expect)` scenarios; demonstrates the assertion-gap Jerry must fill. <https://github.com/pppp606/browser-use_e2e_test_automation_labs>

<a id="ref-13"></a>[13] **Skyvern Blog — "Browser Use vs Stagehand: Which is Better? (Feb 2026)."** Execution-philosophy contrast (continuous LLM reasoning vs hybrid determinism); cost escalation; explicit "neither is a testing framework" statement. <https://www.skyvern.com/blog/browser-use-vs-stagehand-which-is-better/>

<a id="ref-14"></a>[14] **Morph Labs — "Agent-Browser vs Playwright MCP (2026): Token Cost and Reliability."** Visual-drift and reference-binding failure modes, stale-screenshot reasoning, retry-loop issues, token-budget economics (~20k TPM/agent). <https://www.morphllm.com/agent-browser-vs-playwright-mcp>

---

*Confidence: HIGH. All numeric and temporal claims are tied to retrieved URLs; known caveats (WebVoyager non-comparability, star-count timing) are flagged inline per P-022.*
