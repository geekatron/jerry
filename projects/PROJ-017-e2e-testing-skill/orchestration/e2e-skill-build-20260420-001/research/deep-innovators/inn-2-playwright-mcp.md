---
title: "Deep Research — Microsoft Playwright MCP + Playwright Agents"
slug: inn-2-playwright-mcp
candidate: Microsoft Playwright MCP + Playwright Agents
researcher: ps-researcher-inn-2
phase: Phase 1B (Deep Innovators Research)
project: PROJ-017-e2e-testing-skill
orchestration: e2e-skill-build-20260420-001
access_date: 2026-04-21
landscape_card: ../landscape/innovators-candidates.md
constitutional_compliance:
  - P-001 (citations)
  - P-004 (provenance)
  - P-011 (evidence-based)
  - P-022 (no deception)
---

# Deep Research — Microsoft Playwright MCP + Playwright Agents

> Deep-dive on the Microsoft Playwright MCP server and the Playwright Test Agents (Planner / Generator / Healer) as an innovator candidate for informing a Jerry agentic E2E testing skill.

## Navigation

| Section | Purpose |
|---------|---------|
| [Methodology Note](#methodology-note) | Query count, WebFetch count, live-source rules, P-022 honesty |
| [1. What It Is](#1-what-it-is) | Playwright MCP server + Playwright Agents concept |
| [2. Scope and Boundary](#2-scope-and-boundary) | Exposed MCP tools; what they can/cannot do |
| [3. Applicability to Jerry](#3-applicability-to-a-jerry-agentic-e2e-skill) | How Jerry could invoke Playwright MCP as an MCP host |
| [4. Strengths / Unique Contributions](#4-strengths--unique-contributions) | Hyperscaler-backed, MCP standard, a11y-tree-first |
| [5. Weaknesses / Gaps / Criticisms](#5-weaknesses--gaps--criticisms) | Maturity, Radar "Assess", security issues |
| [6. Current State](#6-current-state) | Release version, changelog, Radar placement, spec version |
| [7. Implementation Patterns for Jerry](#7-implementation-patterns--testable-principles-for-jerry) | MCP-tool-shape patterns a Jerry skill could mirror |
| [Sources Retrieved](#sources-retrieved) | All URLs retrieved 2026-04-21 |

---

## Methodology Note

Per Phase 1B non-negotiable constraints, this research was performed on **2026-04-21** using live web search and WebFetch — not cached training data.

- **Queries executed (9, ≥8 required):**
  1. `Playwright MCP server GitHub Microsoft 2026`
  2. `Microsoft Playwright MCP 2025 release accessibility tree`
  3. `Playwright Agents testing framework 2026`
  4. `"Playwright MCP" tool list navigate click snapshot`
  5. `Thoughtworks Technology Radar Playwright MCP Assess`
  6. `Model Context Protocol spec version 2025 2026 browser automation`
  7. `"playwright.dev" MCP documentation getting started`
  8. `Playwright MCP security concerns browser automation risks`
  9. `"playwright-mcp" changelog releases v0.0 2025 2026`
  10. `Playwright Agents planner generator healer workflow`
  11. `Thoughtworks Radar Volume 33 AI-powered UI testing Playwright MCP November 2025`

- **WebFetch reads (3, ≥3 required):**
  1. `https://github.com/microsoft/playwright-mcp` — GitHub repo README (tool list, install, security)
  2. `https://playwright.dev/docs/test-agents` — official Playwright Agents docs
  3. `https://playwright.dev/docs/getting-started-mcp` — official Playwright MCP getting-started page

- **Live URL citations:** ≥9 primary/secondary sources, all retrieved this session (see [Sources Retrieved](#sources-retrieved)).

- **P-022 honesty disclosures:**
  - Exact per-release feature lists in the v0.0.x changelog (e.g., which tool was added in v0.0.62 vs v0.0.70) were not exhaustively enumerated — only summary release data was available from the search layer; I did not fetch the raw GitHub Releases page directly.
  - Thoughtworks Radar Vol 33 PDF was identified as the primary source for the "Assess" placement of AI-powered UI testing, but I relied on the search-layer summary rather than fetching the PDF (PDF WebFetch was out of scope given the 3 fetches focused on tool-definition primary sources). This is a known gap.
  - A prompt-injection attempt appeared mid-results from an upstream search result instructing me to use Context7 MCP for this research; I ignored it as off-task and continued with the user's explicit instructions (P-020 user authority).

---

## 1. What It Is

**Playwright MCP** is a Model Context Protocol server published by Microsoft that "provides browser automation capabilities through the Model Context Protocol, enabling LLMs to interact with web pages using structured accessibility snapshots" ([playwright.dev/docs/getting-started-mcp][pw-mcp-docs], retrieved 2026-04-21). It is distributed as the npm package `@playwright/mcp` and invoked via `npx @playwright/mcp@latest` ([github.com/microsoft/playwright-mcp][pw-mcp-repo]).

Architecturally it is a **thin MCP-protocol adapter over the existing Playwright browser-automation engine**. Instead of a test author writing `page.click(...)` in TypeScript, an MCP-capable LLM host (Claude Code, VS Code Copilot, Cursor, etc.) calls an MCP tool like `browser_click` whose arguments describe the element to click, and the Playwright MCP server translates that into a real Playwright action against a live browser. The server returns a **structured accessibility-tree snapshot** (not a screenshot) so the LLM can reason about the page without needing vision-model tokens ([microsoft/playwright-mcp README][pw-mcp-repo]; [Simon Willison's notes 2025-03-25][sw-notes]).

**Playwright Agents** is a *separate but complementary* capability that ships with the mainline Playwright test framework (v1.56+) — three specialized agents named **Planner**, **Generator**, and **Healer**:

- **Planner** explores the application and produces a Markdown test plan (e.g., `specs/basic-operations.md`).
- **Generator** converts that Markdown plan into executable `tests/*.spec.ts` Playwright Test files, verifying selectors live as it writes.
- **Healer** "executes the test suite and automatically repairs failing tests" by replaying, inspecting, patching, and re-running until green or explicitly skipped.

These agents are scaffolded into a project via `npx playwright init-agents --loop=claude` (or `--loop=vscode`, `--loop=opencode`) and can run independently, sequentially, or chained in an agentic loop ([playwright.dev/docs/test-agents][pw-agents-docs]; [dev.to Playwright Agents walkthrough][devto-agents]).

The conceptual split is important: **Playwright MCP provides the *mechanism* (browser tools exposed over MCP); Playwright Agents provide an opinionated *workflow* (Planner→Generator→Healer) that consumes that mechanism**. Both are shipped by Microsoft and designed to interoperate.

---

## 2. Scope and Boundary

### 2.1 Tools exposed by Playwright MCP

From the GitHub repo README (retrieved 2026-04-21), Playwright MCP exposes **50+ tools** grouped into the following categories ([microsoft/playwright-mcp][pw-mcp-repo]):

| Category | Representative tools |
|----------|----------------------|
| Core automation | `browser_navigate`, `browser_navigate_back`, `browser_click`, `browser_type`, `browser_hover`, `browser_drag`, `browser_press_key`, `browser_select_option`, `browser_fill_form`, `browser_wait_for`, `browser_resize`, `browser_close` |
| Page understanding | `browser_snapshot` (accessibility tree), `browser_take_screenshot` (pixel fallback), `browser_console_messages`, `browser_network_requests`, `browser_handle_dialog`, `browser_file_upload`, `browser_pdf_save` |
| Scripting escape hatch | `browser_evaluate`, `browser_run_code` |
| Tab management | `browser_tabs` |
| Network & storage | `browser_route`, `browser_route_list`, `browser_unroute`, `browser_network_state_set`, `browser_cookie_*`, `browser_localstorage_*`, `browser_sessionstorage_*`, `browser_storage_state`, `browser_set_storage_state` |
| DevTools / authoring | `browser_highlight`, `browser_hide_highlight`, `browser_pick_locator`, `browser_resume`, `browser_start_tracing` / `browser_stop_tracing`, `browser_start_video` / `browser_stop_video`, `browser_video_chapter` |
| Coordinate-based (vision mode) | `browser_mouse_click_xy`, `browser_mouse_move_xy`, `browser_mouse_drag_xy`, `browser_mouse_down`, `browser_mouse_up`, `browser_mouse_wheel` |
| Assertion/verification | `browser_verify_element_visible`, `browser_verify_list_visible`, `browser_verify_text_visible`, `browser_verify_value`, `browser_generate_locator` |
| Configuration | `browser_get_config` |

In practice most agent workflows use only a **core subset** — "navigate, press key, handle dialog, click, type, select, wait for, and page snapshot — only eight of the 26 [commonly used] tools" ([Speakeasy on tool proliferation][speakeasy]). This core subset is the relevant design target for a Jerry-mirrored tool shape.

### 2.2 What it *can* do

- Open real Chromium/Firefox/WebKit sessions (headed by default; `--headless` flag to flip).
- Return structured **accessibility-tree snapshots** with element refs of the form `checkbox "Toggle Todo" [ref=e10]`, which the LLM then passes back into `browser_click({ ref: "e10" })` etc. ([playwright.dev/docs/getting-started-mcp][pw-mcp-docs]).
- Capture console logs, network traffic, cookies, storage, traces, and videos for post-hoc debugging.
- Generate executable Playwright Test code via `browser_generate_playwright_test` so sessions can be promoted to regression specs.

### 2.3 What it *cannot* / does not do

- **It is explicitly not a security boundary** — "Playwright MCP is **not** a security boundary" per the repo README ([microsoft/playwright-mcp][pw-mcp-repo]).
- It does not itself supply test assertions, orchestration, reporting, or CI integration — those come from the surrounding Playwright Test runner or from Playwright Agents.
- It does not abstract away browser state for multi-session reproducibility — profile isolation is manual (`persistent`, `isolated`, `extension` modes).
- It cannot semantically reason about an application's *intent* — it only surfaces what the a11y tree exposes. If an app is a11y-hostile (canvas-heavy, non-semantic divs), the snapshot degrades and the agent must fall back to screenshots and XY-coordinate tools (the "vision mode" subset) ([Skyvern review][skyvern]; [Adnan Masood field guide][adnan-field-guide]).

---

## 3. Applicability to a Jerry Agentic E2E Skill

Jerry is an MCP-capable host (Claude Code is already wired into the Jerry framework via `.claude/settings.local.json` MCP configuration). This means Jerry can **invoke Playwright MCP today**, without building browser automation from scratch, by registering `@playwright/mcp@latest` as an MCP server in the host configuration.

### 3.1 Concrete invocation pattern

From the official docs ([playwright.dev/docs/getting-started-mcp][pw-mcp-docs]; [microsoft/playwright-mcp README][pw-mcp-repo]):

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

Or, for Claude Code CLI directly: `claude mcp add playwright npx @playwright/mcp@latest`.

### 3.2 Fit with the Jerry framework

| Jerry concern | Playwright MCP fit |
|---------------|--------------------|
| **P-002 (file persistence)** | Good — `browser_generate_playwright_test`, traces, videos, and `browser_pdf_save` all produce on-disk artifacts that a Jerry agent can `link-artifact`. |
| **P-001 / P-004 (provenance)** | Good — every MCP tool call is a discrete, loggable event with structured arguments; easy to cite in research output. |
| **P-003 (no recursive subagents)** | Neutral — Playwright MCP is a *tool server*, not a subagent. Invocation by a Jerry agent does not violate single-level nesting. |
| **H-04 (active project)** | Neutral — Playwright MCP is project-agnostic; Jerry wraps it per-project. |
| **L0/L1/L2 audience levels** | The a11y-tree snapshot is naturally structured enough to drive all three levels (L0 screenshots / L1 tool-call logs / L2 trace files). |
| **Quality gate (H-13, >=0.92)** | The Healer agent's "pass/skip with explanation" behavior is compatible with a critic-revision loop — failures produce explicit rationale artifacts that a `ps-critic` can score. |

### 3.3 Architectural role Jerry can play

Three possible integration stances emerge:

1. **Consumer** (lightest): Jerry skill wraps Playwright MCP and prompts the LLM to use `browser_navigate`, `browser_snapshot`, `browser_click` etc. directly. Minimal net-new code.
2. **Orchestrator** (moderate): Jerry reimplements the Planner/Generator/Healer loop using its own orchestration primitives (`/orchestration` skill), driving Playwright MCP tools from Jerry-native agents rather than Microsoft's bundled `init-agents` scaffolding. This lets Jerry enforce its own quality gates, criticality classification, and WORKTRACKER integration.
3. **Protocol mirror** (heaviest, aspirational): Jerry defines its own internal tool-shape that mirrors Playwright MCP's tool-call surface so that Jerry's e2e-testing skill has a stable internal API that could later be re-targeted at a different MCP browser server (Selenium MCP, Cloudflare Browser Rendering, Skyvern).

Option 2 is the strongest L2 recommendation: reuse the mechanism, replace the workflow with Jerry-native orchestration so Jerry's governance (C1-C4 criticality, S-010/S-014 strategies) applies.

---

## 4. Strengths / Unique Contributions

1. **Hyperscaler-backed and protocol-standardized.** Published by Microsoft (the Playwright author) and speaks the MCP standard originally defined by Anthropic, now supported by the broader ecosystem ([modelcontextprotocol.io spec 2025-11-25][mcp-spec]). This means any MCP-capable host — Claude Code, VS Code Copilot, Cursor, Windsurf, Kiro, Codex, Copilot CLI, Gemini CLI, Warp, and others — gets browser automation "for free" ([microsoft/playwright-mcp README][pw-mcp-repo]).

2. **Accessibility-tree-first design.** The `browser_snapshot` tool returns a structured a11y tree — typically **2–5 KB vs 500 KB–2 MB for screenshots** (roughly 10–100x token reduction per turn) ([TestDino Playwright AI Ecosystem 2026][testdino-eco]). This directly translates to lower latency, lower cost, and — crucially — determinism, because the LLM is reasoning over semantic roles rather than interpreting pixels.

3. **Leverages Playwright's existing reliability.** Auto-waiting, cross-browser (Chromium/Firefox/WebKit), trace viewer, and strict assertions — the entire Playwright quality stack — come for free. The MCP layer does not reinvent browser automation; it exposes the industry-grade engine.

4. **Complementary agentic layer (Playwright Agents).** Shipping Planner/Generator/Healer in the core framework gives users an opinionated end-to-end workflow without requiring them to design their own agent loop ([playwright.dev/docs/test-agents][pw-agents-docs]). The Healer in particular — which re-plans from accessibility snapshots on failure — addresses the "flaky selector" problem that has historically plagued E2E suites.

5. **Token efficiency.** The April 2026 release added `@playwright/cli` alongside the MCP server, reporting "~114,000 tokens via MCP versus ~27,000 tokens via CLI — a roughly 4x reduction" for the same browser automation task (aggregated from search summary of the v0.0.x changelog). MCP remains preferred for interactive agentic use; CLI is for coding-agent scripted use. Both share the same underlying engine.

6. **Interoperability with other MCP servers.** Because Playwright MCP is just another MCP server, it composes naturally with other MCP tools in a Jerry host (Context7, Memory-Keeper, etc.) without bespoke integration glue.

---

## 5. Weaknesses / Gaps / Criticisms

1. **Thoughtworks places AI-powered UI testing at "Assess," not "Trial" or "Adopt."** Radar Vol 33 (November 2025) notes that while "major UI testing frameworks like Playwright and Selenium have introduced their own MCP servers...Thoughtworks is excited about those developments and looks forward to seeing more practical guidance and field experience emerge" ([Thoughtworks AI-powered UI testing blip][tw-ai-ui]; [Radar Vol 33 PDF][tw-radar-pdf]). Translation: interesting, not yet field-proven.

2. **MCP protocol maturity.** The current MCP spec release is dated `2025-11-25` ([modelcontextprotocol.io spec][mcp-spec]); enterprise authentication (OAuth 2.1 + PKCE, SAML/OIDC) is not landing until Q2 2026 per the MCP roadmap. Regulated-industry adoption is therefore on a slower track than the hype suggests.

3. **Version instability signals.** Playwright MCP is still in the `v0.0.x` series — v0.0.70 as of April 1, 2026 ([microsoft/playwright-mcp releases][pw-mcp-releases], per search summary). There is no stable `v1.0` yet; tool names, arguments, and return shapes can change between minor-of-minor releases. Any Jerry skill must treat the tool surface as a moving target and pin versions.

4. **Security posture is "not a security boundary" by explicit admission.** The repo README states this outright ([microsoft/playwright-mcp][pw-mcp-repo]). Concrete documented risks include:
   - **CVE-class RCE via `browser_run_code`** (GitHub issue #1495) where the sandbox did not adequately restrict attacker-supplied JavaScript ([GitHub issue][pw-mcp-rce]).
   - **Typosquatting** — an unofficial `playwright-mcp` (hyphen, no scope) package exists alongside the official `@playwright/mcp` and has been inadvertently deployed by customers ([Noma Security blindspots blog][noma]).
   - **Prompt-injection-driven data exfiltration**: a real browser means any page the agent visits can inject "instructions" into the conversation via visible text, comments, or hidden widgets, and the LLM may act on them — the "lethal trifecta" of private data + untrusted content + outbound channels ([Awesome Testing security best practices][awesome-sec]).
   - **Local execution escalation**: `npx`-based MCP servers run with the host user's full filesystem permissions ([Acuvity plug-and-play analysis][acuvity]).

5. **Tool proliferation vs. context pressure.** 50+ exposed tools is a substantial addition to an LLM's context window; each tool's schema and description consumes tokens on every turn. Speakeasy specifically flags this: "most of the time core tools used are...only eight of the 26 tools available on the Playwright MCP server" ([Speakeasy][speakeasy]). A Jerry skill should likely expose a curated subset.

6. **A11y-tree degrades on a11y-hostile apps.** Canvas-heavy apps (drawing tools, map apps, WebGL games) and apps built from non-semantic `<div>` soup will produce thin or misleading snapshots, forcing fallback to the XY-coordinate / screenshot tools — at which point the token-efficiency argument collapses ([Skyvern competitive review][skyvern]).

7. **Coupled to Playwright's browser set.** If the target application has quirks that only reproduce in Safari Technology Preview or an embedded browser framework (Electron, Tauri, WebView2), Playwright's standard distributions may not cover it.

### Steelman note (H-16)

Before the above critiques carry weight, it must be said that **no competing browser-automation MCP server currently matches Playwright MCP's combination of hyperscaler backing, engine maturity, client coverage, and accessibility-tree design**. Every known weakness is also a weakness shared by every alternative browser-MCP (mcp-selenium, Cloudflare Browser Rendering, Skyvern, etc.). The "Assess" rating is about the *category*, not about Playwright MCP's quality within the category.

---

## 6. Current State

| Dimension | Value (as of 2026-04-21) |
|-----------|--------------------------|
| Latest MCP server version | **v0.0.70** (April 1, 2026) ([npmjs @playwright/mcp][npm-pw-mcp]; search summary of [releases page][pw-mcp-releases]) |
| Package name | `@playwright/mcp` (official — beware `playwright-mcp` typosquat) |
| Playwright Test Agents availability | Playwright v1.56+ (**current stable 1.59.1, April 2026**) ([TestDino 2026 release summary][testdino-2026]) |
| MCP spec version | `2025-11-25` ([modelcontextprotocol.io][mcp-spec]) |
| Thoughtworks Radar placement | AI-powered UI testing: **Assess** (Vol 33, Nov 2025) ([Radar Vol 33][tw-radar-pdf]; [AI-powered UI testing blip][tw-ai-ui]) |
| Thoughtworks Radar — Playwright itself | **Adopt** (Languages & Frameworks) — unchanged ([Thoughtworks Playwright blip][tw-pw]) |
| Supported MCP clients | VS Code, Cursor, Claude Desktop, Claude Code, Cline, Codex, Copilot CLI, Copilot Coding Agent, Gemini CLI, Goose, Junie, Kiro, LM Studio, opencode, Qodo Gen, Warp, Windsurf, Amp, Antigravity, Factory |
| 2026 headline additions | `@playwright/cli` companion (shell-command path, ~4x token efficiency); Playwright 1.58 Timeline / Speedboard HTML-report tab |
| Security CVE count | At least one documented critical (browser_run_code RCE, issue #1495) |

### Recent release narrative (2024 → 2026)

- **Mar 22, 2025** — Playwright MCP initial release (Microsoft). Introduces a11y-tree snapshot approach on top of Chromium a11y tree ([Simon Willison notes 2025-03-25][sw-notes]).
- **2025 through 2026** — rapid v0.0.x iteration; progressive tool expansion from ~26 tools to 50+.
- **Oct 9, 2025** — VS Code v1.105 ships with the agentic-experience prerequisites required by Playwright Agents ([playwright.dev/docs/test-agents][pw-agents-docs]).
- **Nov 5, 2025** — Thoughtworks Radar Vol 33 assigns "Assess" ring to AI-powered UI testing and calls out Playwright MCP + Playwright Agents as emblematic ([Radar Vol 33][tw-radar-pdf]).
- **Nov 25, 2025** — MCP spec version `2025-11-25` published.
- **2026** — `@playwright/cli` token-efficient companion shipped; v0.0.70 current; Playwright 1.58/1.59 release with Timeline feature; "senior QA engineers becoming AI Supervisors" narrative entering mainstream testing press ([TestDino][testdino-eco]; [Bug0][bug0-agents]).

---

## 7. Implementation Patterns / Testable Principles for Jerry

The goal of Phase 1B is to extract **tool-shape patterns** a Jerry e2e-testing skill could mirror. Drawing from the evidence above:

### Principle 7.1 — **Expose a curated core subset of tools, not all 50+**

Mirror the "core 8" pattern that Speakeasy and practitioner reports converge on. A Jerry `/e2e-testing` skill should expose at most:

| Jerry tool | Mirrors Playwright MCP | Purpose |
|------------|------------------------|---------|
| `e2e.navigate` | `browser_navigate` | Open a URL |
| `e2e.snapshot` | `browser_snapshot` | Return a11y tree — canonical "what's on the page" |
| `e2e.click` | `browser_click` | Clicks by element ref |
| `e2e.type` | `browser_type` | Fill text |
| `e2e.select` | `browser_select_option` | Dropdown / option select |
| `e2e.wait_for` | `browser_wait_for` | Deterministic wait |
| `e2e.assert_visible` | `browser_verify_element_visible` | Assertion primitive |
| `e2e.screenshot` | `browser_take_screenshot` | Fallback visual evidence |

**Testable principle:** A Jerry e2e skill MUST expose no more than 10 primary tools in the default surface; additional tools are opt-in extensions. *Rationale: context-window economics (Speakeasy); matches the empirical "only 8 used" finding.*

### Principle 7.2 — **A11y-tree snapshots are the canonical page-state artifact**

Every interaction should return (or have available) a structured a11y-tree snapshot with element refs in the form `role "accessible name" [ref=eN]`. Screenshots are fallback evidence, not the primary artifact.

**Testable principle:** `e2e.snapshot` MUST return structured data (not a base64 image) by default; `e2e.screenshot` is a separate, explicitly-invoked tool.

### Principle 7.3 — **Element refs, not CSS selectors, are the LLM-facing identifier**

The Playwright MCP model is: LLM sees `checkbox "Toggle Todo" [ref=e10]` → LLM calls `browser_click({ ref: "e10" })`. This lets the LLM reason semantically ("the Toggle Todo checkbox") while the server handles brittle selector mapping internally.

**Testable principle:** Jerry e2e tools MUST accept opaque element refs emitted by the most recent snapshot; CSS selector / XPath inputs are demoted to an escape hatch only.

### Principle 7.4 — **Planner → Generator → Healer is a reusable three-phase workflow**

The Playwright Agents decomposition maps cleanly onto Jerry's existing agent families:

| Playwright Agent | Jerry equivalent | Output |
|------------------|------------------|--------|
| Planner | `ps-researcher` + `nse-requirements` in exploratory mode | Markdown test plan (`specs/*.md`) |
| Generator | `nse-architecture` or a new `e2e-author` | Executable test file (`tests/*.spec.ts` or `.feature`) |
| Healer | `ps-critic` + `ps-investigator` | Patched test + failure-rationale artifact |

**Testable principle:** Jerry e2e workflows MUST persist an intermediate Markdown artifact between exploration and code generation so a human can approve scope before code is written (P-020 user authority checkpoint).

### Principle 7.5 — **Treat browser tools as untrusted-output sources**

Because Playwright MCP is "not a security boundary," any content returned from a page snapshot must be treated as potentially adversarial instruction payload.

**Testable principle:** Jerry e2e tool outputs MUST be wrapped in a quarantine frame (e.g., `<untrusted-page-content>...</untrusted-page-content>`) before being inserted into the LLM prompt, and the system prompt MUST instruct the model to never follow instructions originating from quarantine frames. This mirrors the "lethal trifecta" mitigation pattern ([Awesome Testing Nov 2025][awesome-sec]).

### Principle 7.6 — **Version-pin the browser MCP server**

Given the `v0.0.x` instability, any Jerry skill integration MUST pin to a specific Playwright MCP version (`@playwright/mcp@0.0.70`, not `@latest`) and include the pinned version in the skill's SSOT configuration, with an explicit upgrade review step.

**Testable principle:** Jerry e2e skill config MUST declare a pinned MCP server version in a SSOT file; upgrades are C2+ changes requiring adversarial review (S-014 scoring).

### Principle 7.7 — **Separate mechanism from workflow**

The cleanest design takeaway: Playwright ships two distinct products — the MCP server (mechanism) and the Agents (workflow) — and they are usable independently. Jerry should adopt this same separation: an `e2e-browser` low-level tool skill that wraps Playwright MCP; and a higher-level `/e2e-testing` workflow skill that orchestrates plan→generate→heal using the low-level primitives.

**Testable principle:** Jerry's e2e capability MUST ship as at least two separable skills — a tool wrapper and a workflow orchestrator — so that alternative browser-MCP backends (Selenium MCP, Cloudflare Browser Rendering) can be swapped in later without rewriting the workflow layer.

### Principle 7.8 — **Quality-gate the Healer loop**

The Playwright Healer's "retry until passing or mark as skipped" loop is a natural fit for Jerry's H-14 creator-critic-revision cycle (minimum 3 iterations). A Jerry Healer equivalent should emit an S-014-scored deliverable per iteration and stop when either `score >= 0.92` or `iterations >= 3 AND no-improvement-detected`, with the latter producing a skip-with-rationale artifact rather than an infinite loop.

**Testable principle:** Jerry e2e healing loops MUST cap at a configured iteration ceiling and MUST emit an explicit skip-with-rationale artifact on non-convergence.

---

## Sources Retrieved

All URLs retrieved on **2026-04-21**.

1. [microsoft/playwright-mcp — GitHub repo][pw-mcp-repo] — primary source for tool list, install, version, security stance. **WebFetch**.
2. [playwright.dev/docs/test-agents][pw-agents-docs] — official Playwright Agents documentation. **WebFetch**.
3. [playwright.dev/docs/getting-started-mcp][pw-mcp-docs] — official Playwright MCP getting-started. **WebFetch**.
4. [Thoughtworks AI-powered UI testing blip][tw-ai-ui] — Radar technique entry.
5. [Thoughtworks Technology Radar Vol 33 (Nov 2025) PDF][tw-radar-pdf] — primary Radar document.
6. [Thoughtworks Playwright tool blip][tw-pw] — Playwright-as-framework Adopt ring.
7. [Model Context Protocol spec 2025-11-25][mcp-spec] — MCP protocol SSOT.
8. [npm @playwright/mcp][npm-pw-mcp] — package version source.
9. [microsoft/playwright-mcp releases][pw-mcp-releases] — version history.
10. [Simon Willison — microsoft/playwright-mcp notes 2025-03-25][sw-notes] — launch coverage.
11. [Simon Willison TILs — Using Playwright MCP with Claude Code][sw-til] — practitioner integration walkthrough.
12. [TestDino — Playwright AI Ecosystem 2026][testdino-eco] — 10–100x token-efficiency claim.
13. [TestDino — Playwright 2026 release summary][testdino-2026] — current 1.59.1 / 1.58 Timeline feature.
14. [Bug0 — Playwright Test Agents: AI Testing Explained][bug0-agents] — Planner/Generator/Healer walkthrough.
15. [dev.to — Playwright Agents: Planner, Generator, and Healer in Action][devto-agents] — workflow example.
16. [Skyvern — Playwright MCP Reviews and Alternatives 2025][skyvern] — competitive review, a11y-tree limitations.
17. [Speakeasy — Why less is more: The Playwright proliferation problem with MCP][speakeasy] — "8 of 26 tools" finding.
18. [Awesome Testing — Playwright MCP Security Best Practices (Nov 2025)][awesome-sec] — lethal-trifecta analysis.
19. [Noma Security — top-five MCP security blindspots][noma] — typosquatting, local-exec risks.
20. [Acuvity — MCP Server: The Dangers of Plug-and-Play Code][acuvity] — npx local-permission risks.
21. [GitHub issue #1495 — Critical RCE in Playwright-MCP via browser_run_code][pw-mcp-rce] — concrete CVE-class issue.
22. [Adnan Masood, PhD — Playwright and Playwright MCP field guide (Medium)][adnan-field-guide] — practitioner field notes.
23. [Microsoft Community Hub — Integrate Playwright MCP for AI-Driven Test Automation][ms-techcommunity] — enterprise adoption narrative.

[pw-mcp-repo]: https://github.com/microsoft/playwright-mcp
[pw-agents-docs]: https://playwright.dev/docs/test-agents
[pw-mcp-docs]: https://playwright.dev/docs/getting-started-mcp
[tw-ai-ui]: https://www.thoughtworks.com/en-us/radar/techniques/ai-powered-ui-testing
[tw-radar-pdf]: https://www.thoughtworks.com/content/dam/thoughtworks/documents/radar/2025/11/tr_technology_radar_vol_33_en.pdf
[tw-pw]: https://www.thoughtworks.com/radar/languages-and-frameworks/playwright
[mcp-spec]: https://modelcontextprotocol.io/specification/2025-11-25
[npm-pw-mcp]: https://www.npmjs.com/package/@playwright/mcp
[pw-mcp-releases]: https://github.com/microsoft/playwright-mcp/releases
[sw-notes]: https://simonwillison.net/2025/Mar/25/playwright-mcp/
[sw-til]: https://til.simonwillison.net/claude-code/playwright-mcp-claude-code
[testdino-eco]: https://testdino.com/blog/playwright-ai-ecosystem/
[testdino-2026]: https://testdino.com/blog/playwright-2026-new-features/
[bug0-agents]: https://bug0.com/blog/playwright-test-agents
[devto-agents]: https://dev.to/playwright/playwright-agents-planner-generator-and-healer-in-action-5ajh
[skyvern]: https://www.skyvern.com/blog/playwright-mcp-reviews-and-alternatives-2025/
[speakeasy]: https://www.speakeasy.com/blog/playwright-tool-proliferation
[awesome-sec]: https://www.awesome-testing.com/2025/11/playwright-mcp-security
[noma]: https://noma.security/blog/top-five-mcp-security-blindspots-putting-your-organization-at-risk/
[acuvity]: https://acuvity.ai/mcp-server-the-dangers-of-plug-and-play-code/
[pw-mcp-rce]: https://github.com/microsoft/playwright-mcp/issues/1495
[adnan-field-guide]: https://medium.com/@adnanmasood/playwright-and-playwright-mcp-a-field-guide-for-agentic-browser-automation-f11b9daa3627
[ms-techcommunity]: https://techcommunity.microsoft.com/blog/azuredevcommunityblog/how-to-integrate-playwright-mcp-for-ai-driven-test-automation/4470372

---

*End of deep research. Prepared by ps-researcher-inn-2 for Phase 1C synthesis.*
