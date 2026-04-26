# Deep Dive: W3C WebDriver (Level 2) Specification

> Phase 1b Deep Research for PROJ-017 E2E Testing Skill — Lane STD-1.

| Field | Value |
|-------|-------|
| Topic | W3C WebDriver (Level 2) Specification |
| Slug | `std-1-w3c-webdriver` |
| Agent | ps-researcher-std-1 |
| Workflow | `e2e-skill-build-20260420-001` |
| Phase | 1b — Deep standards research |
| Access Date (all URLs) | 2026-04-21 |
| Upstream Landscape Card | `research/landscape/standards-candidates.md` (Candidate 1) |

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Methodology Note](#methodology-note) | Live query and WebFetch verification tables |
| [1. What It Specifies](#1-what-it-specifies) | Authoritative summary of the standard itself |
| [2. Scope and Boundary](#2-scope-and-boundary) | What WebDriver covers and explicitly doesn't |
| [3. Applicability to a Jerry E2E Testing Skill](#3-applicability-to-a-jerry-e2e-testing-skill) | How the standard maps into Jerry |
| [4. Strengths / Unique Contributions](#4-strengths--unique-contributions) | Why the standard still matters |
| [5. Weaknesses / Gaps / Criticisms](#5-weaknesses--gaps--criticisms) | Known limitations and critique |
| [6. Current State](#6-current-state) | Level 1 vs Level 2, CR/REC status, vendor conformance, BiDi advances |
| [7. Key Implementation Patterns / Testable Principles](#7-key-implementation-patterns--testable-principles) | What a Jerry skill would operationalize |
| [Sources Retrieved](#sources-retrieved) | All live URLs with access dates |

---

## Methodology Note

All evidence below was collected via live WebSearch and WebFetch on **2026-04-21**. Training-data-only claims are explicitly marked *(uncertain / not live-verified)* per P-022. Where a claim is contingent on secondary reporting (e.g., blog posts referencing vendor shipping dates), it is flagged as secondary.

### Live Query Table (WebSearch)

| # | Query | Purpose |
|---|-------|---------|
| 1 | `W3C WebDriver Level 2 specification 2026` | Confirm Level 2 document identity, URL, status |
| 2 | `W3C WebDriver BiDi 2025 2026 specification status` | Get BiDi spec status and vendor cadence |
| 3 | `WebDriver spec editor's draft w3.org 2026` | Confirm current editor's draft / TR mapping |
| 4 | `WebDriver vs WebDriver BiDi differences protocol` | Identify protocol model differences |
| 5 | `WebDriver conformance browser vendors Chrome Firefox Safari 2025` | Vendor conformance posture 2024–2026 |
| 6 | `Selenium WebDriver W3C spec compliance endpoints JSON` | Confirm HTTP/JSON endpoint model and Selenium 4+ alignment |
| 7 | `WebDriver specification recommendation status 2026 Level 1 Level 2` | Level 1 = REC, Level 2 = WD confirmation |
| 8 | `WebDriver BiDi browser support Chrome Firefox Safari implementation progress 2025 2026` | BiDi per-browser implementation status |
| 9 | `WebDriver Classic criticism limitations automation flaky` | Weaknesses / critiques of the classic protocol |
| 10 | `Browser Testing and Tools Working Group charter 2024 2025` | Working Group governance and remit |
| 11 | `wpt.fyi WebDriver BiDi test results Chrome Firefox 2025` | Web Platform Tests as conformance evidence |
| 12 | `Playwright Puppeteer WebDriver BiDi adoption 2025 Selenium 5` | Client-library adoption trajectory |

### WebFetch Verification Table (Primary Sources)

| URL | Purpose |
|-----|---------|
| https://www.w3.org/TR/webdriver2/ | Primary — Level 2 Working Draft (2026-04-01); editors, sections, conformance language |
| https://www.w3.org/TR/webdriver-bidi/ | Primary — BiDi Working Draft (2026-03-19); modules, transport, editors |
| https://developer.chrome.com/blog/webdriver-bidi | Primary-secondary — Chrome team positioning of BiDi vs Classic vs CDP |

---

## 1. What It Specifies

The W3C WebDriver (Level 2) specification defines **a remote control interface that enables introspection and control of user agents** via a *platform- and language-neutral wire protocol* so out-of-process programs can instruct browser behavior deterministically ([W3C WD 2026-04-01](https://www.w3.org/TR/webdriver2/)). Editors are **Simon Stewart (Apple)** and **David Burns (BrowserStack)**; work is produced by the **Browser Testing and Tools Working Group** ([BTT WG](https://www.w3.org/groups/wg/browser-tools-testing/)).

The protocol is **synchronous command/response over HTTP/JSON**: every command is one HTTP method + path mapping, requests and responses are UTF-8 JSON objects, and responses put payloads under a top-level `"value"` key (verified via the spec's request/response algorithm text; cf. also the [LambdaTest Selenium-4 W3C overview](https://www.lambdatest.com/blog/selenium4-w3c-webdriver-protocol/)). Path segments prefixed with `:` are variables (e.g., `:sessionId`, `:elementId`).

Major endpoint families in the Level 2 editor table (as summarized from the spec fetch):

| Family | Representative commands |
|--------|------------------------|
| Sessions | New Session, Delete Session, Status |
| Navigation | Navigate To, Back, Forward, Refresh, Get Current URL, Get Title |
| Contexts | Window handles, switch frame, get/set window rect, fullscreen, minimize, maximize |
| Elements | Find Element(s), Get Attribute/Property/CSS Value/Text, Is Selected/Enabled, Click, Clear, Send Keys |
| Document | Get Page Source, Execute Script (sync/async) |
| Cookies | Get, Get Named, Add, Delete, Delete All |
| Actions | Keyboard, pointer (mouse/touch/pen), wheel input sequences; Release Actions |
| User Prompts | Dismiss/Accept Alert, Get Alert Text, Send Alert Text |
| Capture | Take Screenshot (page / element) |
| Print | Print Page (PDF) |

Conformance is phrased as algorithmic steps: **"Conformance requirements phrased as algorithms or specific steps may be implemented in any manner, so long as the end result is equivalent"** (direct excerpt from [WD 2026-04-01](https://www.w3.org/TR/webdriver2/)). The spec separates **endpoint nodes** (final remote ends — the browser's driver) from **intermediary nodes** (proxies/hubs such as Selenium Grid).

## 2. Scope and Boundary

**In scope (verified from the spec fetch):**
- HTTP/JSON wire protocol: endpoints, error codes, timeouts, capabilities negotiation.
- Session lifecycle and capabilities matching.
- Element location strategies (CSS, link text, partial link text, tag name, XPath) and element reference identity.
- Synthetic input primitives (pointer, keyboard, wheel) at a level intended to approximate a real user.
- Cookie jar, navigation, window/frame context switching, and JavaScript execution.
- Screenshots, page print (PDF), and user-prompt handling.

**Explicitly out of scope / non-goals (from the spec fetch and WG charter):**
- Language-specific client libraries (Selenium, WebdriverIO, etc., implement *bindings* to the wire protocol — bindings are not normative) ([W3C TR/webdriver2](https://www.w3.org/TR/webdriver2/)).
- Browser binary startup, driver installation, OS-specific details.
- **Bidirectional / event-driven communication** — this is delegated to the separate **[WebDriver BiDi](https://www.w3.org/TR/webdriver-bidi/)** specification (see §6).
- Accessibility-technology remote control — scoped to the separate **AT Driver** deliverable of the same Working Group ([BTT WG charter draft](https://w3c.github.io/charter-drafts/2024/btt-wg.html)).
- Network interception, request mocking, CDP-style low-level instrumentation — **not in Classic WebDriver**; these features are why BiDi exists ([Chrome Developers blog](https://developer.chrome.com/blog/webdriver-bidi)).
- Visual/DOM diffing, assertion frameworks, test runners, reporting — consistently cited as a gap ([BrowserStack: disadvantages of Selenium](https://www.browserstack.com/guide/disadvantages-of-selenium)).

The boundary with **WebDriver BiDi** is explicit: BiDi *extends* (does not replace) Classic by adding a WebSocket-based duplex channel; the Classic HTTP endpoints remain authoritative for command/response semantics ([W3C TR/webdriver-bidi](https://www.w3.org/TR/webdriver-bidi/)).

## 3. Applicability to a Jerry E2E Testing Skill

Applicability is **high and foundational**. A Jerry E2E testing skill targeting browser UIs is building — directly or transitively — on top of WebDriver. Concretely:

1. **Portable protocol as a cross-tool abstraction.** Whether the skill ultimately wraps Selenium, WebdriverIO, or Playwright, the underlying cross-browser guarantees are anchored by WebDriver conformance. This is exactly why Selenium 4 is "only using W3C standard" and deprecated the legacy JSON Wire Protocol ([Selenium docs](https://www.selenium.dev/documentation/webdriver/); [LambdaTest](https://www.lambdatest.com/blog/selenium4-w3c-webdriver-protocol/)).
2. **Deterministic command vocabulary.** The Level 2 endpoint taxonomy (sessions, navigation, elements, actions, cookies, prompts, screenshots) gives Jerry a stable **testable-principle checklist** against which skill-provided operations can be traced (e.g., every skill-level "click" maps to the spec's `Element Click` algorithm with implicit scroll-into-view and event firing semantics).
3. **Error model.** WebDriver's standardized error codes (e.g., `no such element`, `stale element reference`, `element click intercepted`, `invalid session id`) give Jerry a ready-made **fault taxonomy** for flake diagnosis rules.
4. **Conformance as a vendor-neutrality argument.** Because Chrome, Firefox, Edge, and Safari all ship conforming drivers ([Selenium Supported Browsers](https://www.selenium.dev/documentation/webdriver/browsers/); [BrowserStack architecture](https://www.browserstack.com/guide/architecture-of-selenium-webdriver)), a WebDriver-grounded skill inherits cross-browser parity without Chromium lock-in (the key risk with CDP-only tools).
5. **Evolution hedge.** Any Jerry skill needs a migration story to **WebDriver BiDi** for features the business will demand next (network interception, console logs, real-time events). Because BiDi extends Classic, authoring against the WebDriver contract is forward-compatible.

**Implication for skill design:** Jerry's E2E skill should expose a **protocol-aware layer** whose operations cite WebDriver commands (for traceability and conformance) but whose *execution* can transparently upgrade to BiDi when the capability is needed and the vendor supports it.

## 4. Strengths / Unique Contributions

| Strength | Evidence |
|----------|----------|
| **True cross-browser interop** — only automation protocol endorsed by all four major engines (Blink, Gecko, WebKit, Chromium-Edge). | [Selenium Supported Browsers](https://www.selenium.dev/documentation/webdriver/browsers/); [BrowserStack architecture](https://www.browserstack.com/guide/architecture-of-selenium-webdriver); Level-1 REC status ([W3C TR/webdriver1](https://www.w3.org/TR/webdriver1/)). |
| **W3C REC-backed stability** (Level 1 is Recommendation; Level 2 is the continuously updated successor). | Level 1 REC status per W3C process; Level 2 WD dated 2026-04-01 ([W3C TR/webdriver2](https://www.w3.org/TR/webdriver2/)). |
| **Language-neutral wire protocol** — HTTP/JSON is implementable in any language; bindings exist for Java, Python, JS, C#, Ruby, Go, Rust, etc. | [W3C TR/webdriver2 §Protocol](https://www.w3.org/TR/webdriver2/); [Selenium docs](https://www.selenium.dev/documentation/webdriver/). |
| **Hub/grid friendly** — the "intermediary node" concept bakes proxying into the spec, enabling Selenium Grid, Sauce Labs, BrowserStack, LambdaTest scaling out-of-the-box. | [W3C TR/webdriver2 conformance](https://www.w3.org/TR/webdriver2/); [Sauce W3C capabilities](https://docs.saucelabs.com/dev/w3c-webdriver-capabilities/). |
| **Realistic user-input model** — the Actions API specifies keyboard, pointer (mouse/touch/pen) and wheel tick chains, enabling gestures Classic CDP-only tools handled inconsistently. | Actions family in [W3C TR/webdriver2](https://www.w3.org/TR/webdriver2/). |
| **Web Platform Tests as conformance evidence** — WPT is the shared source of truth across vendors. | [BTT WG charter](https://w3c.github.io/charter-drafts/2024/btt-wg.html); [Chrome Developers blog](https://developer.chrome.com/blog/webdriver-bidi). |

## 5. Weaknesses / Gaps / Criticisms

| Weakness | Evidence |
|----------|----------|
| **Strictly request/response.** No server-initiated events; clients must poll for state changes. This is the central motivation for BiDi. | [W3C TR/webdriver-bidi intro](https://www.w3.org/TR/webdriver-bidi/); [Chrome Developers blog](https://developer.chrome.com/blog/webdriver-bidi). |
| **No network interception, request mocking, or response stubbing.** Out of scope for Classic; developers either fake at the app layer or move to CDP / BiDi. | [Chrome Developers blog](https://developer.chrome.com/blog/webdriver-bidi); [Substack: WebDriver vs CDP vs BiDi](https://substack.thewebscraping.club/p/webdriver-vs-cdp-vs-bidi). |
| **No console/log streaming or uncaught-exception events.** Classic has historically exposed `/log` endpoints only in non-standard extensions that were dropped. | [Mozilla Wiki: WebDriver BiDi](https://wiki.mozilla.org/WebDriver/RemoteProtocol/WebDriver_BiDi); [Chrome Developers blog](https://developer.chrome.com/blog/webdriver-bidi). |
| **Flakiness with modern SPAs.** Polling-based waits interact poorly with AJAX/streaming/rendering; multiple practitioner sources report ~36% of teams flagging flakiness as top challenge. *(secondary-source aggregation)* | [AccelQ](https://www.accelq.com/blog/selenium-webdriver/); [BrowserStack top limitations](https://www.browserstack.com/guide/top-limitations-of-selenium-automation); [LambdaTest challenges](https://www.lambdatest.com/blog/common-challenges-in-selenium-automation-how-to-fix-them/). |
| **Latency overhead of HTTP-per-command.** High command counts amplify per-hop latency, a pain for long interaction chains. | [Substack: WebDriver vs CDP vs BiDi](https://substack.thewebscraping.club/p/webdriver-vs-cdp-vs-bidi); [BrowserStack disadvantages](https://www.browserstack.com/guide/disadvantages-of-selenium). |
| **No built-in reporting, assertions, visual diffing, or test structure.** Consumers must bring a test framework. | [BrowserStack disadvantages](https://www.browserstack.com/guide/disadvantages-of-selenium). |
| **Capability negotiation surface is loose.** Vendor-specific keys (`goog:chromeOptions`, `moz:firefoxOptions`, `ms:edgeOptions`) proliferate despite standard capabilities. | [Sauce W3C capabilities](https://docs.saucelabs.com/dev/w3c-webdriver-capabilities/); [WebdriverIO Capabilities](https://webdriver.io/docs/capabilities/). |
| **Non-goal gaps for E2E realism.** No device emulation, geolocation override, CPU/network throttling, or timezone/locale emulation in Classic — delegated to BiDi's Emulation module. | [W3C TR/webdriver-bidi §Emulation](https://www.w3.org/TR/webdriver-bidi/). |

## 6. Current State

### Level 1 vs Level 2

| Attribute | Level 1 | Level 2 |
|-----------|---------|---------|
| Status | **Recommendation (REC)** | **Working Draft** (latest WD dated **2026-04-01**) |
| URL | https://www.w3.org/TR/webdriver1/ | https://www.w3.org/TR/webdriver2/ |
| WG trajectory | Stable / archival | "Continuously updated" once it reaches CR; WG intends CR but no declared advancement to REC milestone ([verified from WD 2026-04-01 status](https://www.w3.org/TR/webdriver2/)) |
| Editors (Level 2) | — | Simon Stewart (Apple), David Burns (BrowserStack) |

Search result 7 surfaces the explicit status text: *"WebDriver Level 1 is a Recommendation, while Level 2 is a Working Draft… The Working Group intends to publish the latest state of their work as Candidate Recommendation and does not intend to advance their documents to Recommendation with no explicit milestones. The Group expects to continuously update the Candidate Recommendation once it reaches that stage."*

### Browser-Vendor Conformance (2024–2026)

| Vendor | Classic (Level 1/2) | BiDi (2025–2026) |
|--------|--------------------|------------------|
| Chrome / Edge (Chromium) | ChromeDriver and EdgeDriver ship W3C-conforming endpoints; Selenium 4+ exclusively uses W3C protocol. | BiDi implemented via the [`chromium-bidi`](https://github.com/GoogleChromeLabs/chromium-bidi) JavaScript mapper atop CDP; shipping since Chrome/ChromeDriver 106 (2022). BiDi is default-on for newer features; Classic still the default launcher protocol *(per Chrome Developers; secondary)*. |
| Firefox | geckodriver implements W3C Classic. | Native BiDi implementation; Firefox announced **CDP deprecation starting v129** (2024). Cypress 14.1 (Feb 2025) made Firefox automation run over BiDi by default; Cypress 15 (Aug 2025) dropped CDP for Firefox entirely *(secondary: [Boni García blog](https://medium.com/@boni.gg/webdriver-bidi-the-future-of-browser-automation-is-now-1ca0d5ee74dd))*. |
| Safari | SafariDriver ships with Safari; conforms to Classic. | BiDi support **not yet available** as of 2026-04-21 per multiple secondary sources. *(uncertain / not live-verified against Apple primary docs)* |

Sources: [Selenium Supported Browsers](https://www.selenium.dev/documentation/webdriver/browsers/); [ChromeDriver docs](https://developer.chrome.com/docs/chromedriver); [Chromium BiDi repo](https://github.com/GoogleChromeLabs/chromium-bidi); [Mozilla Wiki: WebDriver BiDi](https://wiki.mozilla.org/WebDriver/RemoteProtocol/WebDriver_BiDi); [Puppeteer BiDi support](https://pptr.dev/webdriver-bidi); [BrowserStack architecture](https://www.browserstack.com/guide/architecture-of-selenium-webdriver).

### BiDi Advances (as of 2026-04-21)

The [W3C WebDriver BiDi WD dated 2026-03-19](https://www.w3.org/TR/webdriver-bidi/) (editors: James Graham / Mozilla, Alex Rudenko, Maksim Sadym / Google) specifies modules for:

- **Session / Browser / Browsing Context / Script / Network / Storage / Emulation / Input / Log / Web Extension.**
- **Transport:** WebSocket (RFC 6455). Clients request a `webSocketUrl` capability and receive a WebSocket endpoint; messages are JSON objects with `method` + `params` (commands) or `type: "event"` (events).
- **Extension model:** colon-prefixed custom module names allow vendor-specific extensions without forking the core.
- **Conformance:** CDDL-specified message formats + WPT BiDi test tree serves as the conformance dashboard ([wpt.fyi WebDriver BiDi results](https://wpt.fyi/results/webdriver/tests/bidi?label=master&label=stable&product=chrome-124.0.6367.207)).

Working-group cadence is visible in minutes from [12 March 2025](https://www.w3.org/2025/03/12-webdriver-minutes.html), [09 July 2025](https://www.w3.org/2025/07/09-webdriver-minutes.html), and [10 December 2025](https://www.w3.org/2025/12/10-webdriver-minutes.html). Client-library adoption 2025–2026:

| Tool | BiDi posture |
|------|-------------|
| Selenium 4 | BiDi low-level APIs available. |
| Selenium 5 | BiDi is the marquee re-architecture (secondary reporting; not yet GA-verified on 2026-04-21). |
| Puppeteer | BiDi default protocol for Firefox since Puppeteer 24; cross-browser via BiDi. |
| Playwright | BiDi integration experimental; transition expected when parity reached. |
| WebdriverIO | Exposes BiDi API directly ([docs](https://webdriver.io/docs/api/webdriverBidi/)). |
| Cypress | Firefox default BiDi since 14.1 (Feb 2025). |

## 7. Key Implementation Patterns / Testable Principles

These are the WebDriver-derived principles a Jerry E2E skill should operationalize. Each principle is traceable to the normative text above; the skill's rules, templates, and validators should cite the section referenced.

1. **P-WD-1 — Protocol layer isolation.** Skill operations MUST be specified in WebDriver command vocabulary (e.g., `navigate`, `findElement`, `performActions`, `getElementProperty`) with an implementation-agnostic binding. Rationale: language-neutral wire protocol is the durable abstraction ([W3C TR/webdriver2](https://www.w3.org/TR/webdriver2/)).
2. **P-WD-2 — Explicit session lifecycle.** Sessions MUST be created via `New Session` with declared capabilities, terminated via `Delete Session`, and leaked sessions MUST be detectable. Capabilities MUST document vendor-prefixed keys separately from standard capabilities.
3. **P-WD-3 — Waits, not sleeps.** Because the protocol is command/response, tests MUST use explicit/fluent waits keyed on WebDriver predicates (`isDisplayed`, `isEnabled`, `findElement`) rather than arbitrary `sleep`. Rationale: flakiness is the dominant criticism of Classic.
4. **P-WD-4 — Action sequences as user intent.** Complex gestures MUST be built using the Actions API (pointer/keyboard/wheel tick chains), not composed scroll + click hacks. The spec's Actions model is the authoritative source for realism.
5. **P-WD-5 — Deterministic error taxonomy.** Skill-level diagnostics MUST map failures to WebDriver error codes (`no such element`, `stale element reference`, `element click intercepted`, `timeout`, `invalid session id`), with remediation guidance per class.
6. **P-WD-6 — Screenshot + page source artifacts on every failure.** Capture is part of the spec; failure artifacts MUST include at minimum a full-page screenshot and page source to enable post-hoc triage.
7. **P-WD-7 — Cross-browser conformance by default.** The skill's test matrix MUST include at least two engines (Blink + Gecko minimum; Blink + Gecko + WebKit for public-facing product). Anything CDP-specific MUST be quarantined as a non-portable adapter.
8. **P-WD-8 — Intermediary-aware design.** The skill MUST assume runs may go through a Selenium Grid / cloud provider intermediary; session IDs, capability negotiation, and trailers MUST be treated as remote and potentially proxied.
9. **P-WD-9 — Forward-compatible to BiDi.** When a feature needs server-push events (network interception, console logs, exceptions, response bodies), the skill MUST switch to BiDi *for that feature only* and gate availability on capability negotiation (`webSocketUrl`). Rationale: BiDi extends, not replaces, Classic.
10. **P-WD-10 — WPT as conformance evidence.** The skill's CI MUST be able to consult [wpt.fyi](https://wpt.fyi) for the tested command/browser pair to distinguish "skill bug" from "vendor nonconformance," per the WG's WPT-as-source-of-truth model.

---

## Sources Retrieved

All URLs retrieved **2026-04-21** this session.

| # | URL | Type | Used For |
|---|-----|------|----------|
| 1 | https://www.w3.org/TR/webdriver2/ | Primary (WebFetch) | Level 2 WD text, editors, status, endpoint families, conformance language |
| 2 | https://www.w3.org/TR/webdriver-bidi/ | Primary (WebFetch) | BiDi WD text, modules, transport, editors |
| 3 | https://developer.chrome.com/blog/webdriver-bidi | Primary vendor (WebFetch) | Chrome's positioning of BiDi vs Classic vs CDP |
| 4 | https://www.w3.org/TR/webdriver1/ | Primary (search result) | Level 1 REC status comparator |
| 5 | https://w3c.github.io/webdriver-bidi/ | Primary (search result) | BiDi editor's draft (living) |
| 6 | https://www.w3.org/groups/wg/browser-tools-testing/ | Primary (search result) | Working Group identity |
| 7 | https://w3c.github.io/charter-drafts/2024/btt-wg.html | Primary (search result) | WG charter scope / deliverables |
| 8 | https://www.w3.org/2025/03/12-webdriver-minutes.html | Primary (search result) | WG activity cadence 2025 |
| 9 | https://www.w3.org/2025/07/09-webdriver-minutes.html | Primary (search result) | WG activity cadence 2025 |
| 10 | https://www.w3.org/2025/12/10-webdriver-minutes.html | Primary (search result) | WG activity cadence late-2025 |
| 11 | https://www.w3.org/wiki/WebDriver/2025-02-BiDi | Primary (search result) | W3C wiki BiDi milestone page |
| 12 | https://github.com/w3c/webdriver | Primary (search result) | Classic spec repo |
| 13 | https://github.com/w3c/webdriver-bidi | Primary (search result) | BiDi spec repo |
| 14 | https://github.com/GoogleChromeLabs/chromium-bidi | Primary (search result) | Chromium BiDi mapper implementation |
| 15 | https://www.selenium.dev/documentation/webdriver/ | Secondary (search result) | Selenium's conformance statement |
| 16 | https://www.selenium.dev/documentation/webdriver/browsers/ | Secondary (search result) | Vendor driver coverage |
| 17 | https://www.selenium.dev/documentation/webdriver/bidi/ | Secondary (search result) | BiDi in Selenium |
| 18 | https://developer.chrome.com/docs/chromedriver | Primary vendor (search result) | ChromeDriver W3C + BiDi conformance |
| 19 | https://docs.saucelabs.com/dev/w3c-webdriver-capabilities/ | Secondary (search result) | Capabilities landscape (std + vendor) |
| 20 | https://wiki.mozilla.org/WebDriver/RemoteProtocol/WebDriver_BiDi | Primary vendor (search result) | Firefox BiDi implementation posture |
| 21 | https://pptr.dev/webdriver-bidi | Secondary (search result) | Puppeteer BiDi defaults |
| 22 | https://webdriver.io/docs/api/webdriverBidi/ | Secondary (search result) | WebdriverIO BiDi API |
| 23 | https://webdriver.io/docs/capabilities/ | Secondary (search result) | Capability key proliferation |
| 24 | https://www.lambdatest.com/blog/selenium4-w3c-webdriver-protocol/ | Secondary (search result) | Selenium-4 W3C compliance narrative |
| 25 | https://www.browserstack.com/guide/architecture-of-selenium-webdriver | Secondary (search result) | Architecture + vendor driver coverage |
| 26 | https://www.browserstack.com/guide/top-limitations-of-selenium-automation | Secondary (search result) | Weaknesses / flakiness |
| 27 | https://www.browserstack.com/guide/disadvantages-of-selenium | Secondary (search result) | Weaknesses / reporting gaps |
| 28 | https://www.accelq.com/blog/selenium-webdriver/ | Secondary (search result) | Practitioner criticisms |
| 29 | https://www.lambdatest.com/blog/common-challenges-in-selenium-automation-how-to-fix-them/ | Secondary (search result) | Flakiness numbers (36%) |
| 30 | https://substack.thewebscraping.club/p/webdriver-vs-cdp-vs-bidi | Secondary (search result) | WebDriver vs CDP vs BiDi comparison |
| 31 | https://medium.com/@boni.gg/webdriver-bidi-the-future-of-browser-automation-is-now-1ca0d5ee74dd | Secondary (search result) | Cypress/Firefox BiDi timeline |
| 32 | https://wpt.fyi/results/webdriver/tests/bidi?label=master&label=stable&product=chrome-124.0.6367.207 | Primary infra (search result) | WPT BiDi dashboard |
| 33 | https://github.com/jlipps/simple-wd-spec | Tertiary (search result) | Plain-English WD spec guide |

### Honesty Note (P-022)

- **Uncertain / not live-verified:** Safari BiDi support ("not yet available") is aggregated from Chrome Developers + Mozilla + secondary blog sources; no Apple primary documentation was retrieved this session.
- **Uncertain / not live-verified:** Selenium 5 GA status — secondary sources describe BiDi as "the defining feature" of Selenium 5; no Selenium release-notes page was fetched live this session.
- **Secondary-source aggregation:** The "36% of teams" flakiness figure originates from practitioner blogs (AccelQ, LambdaTest) and is reported as a community-survey-style datum; methodology is not independently verifiable.
- **Document-date note:** `TR/webdriver2/` shows a publication date of **2026-04-01** and `TR/webdriver-bidi/` shows **2026-03-19** as returned by WebFetch this session; both remain Working Drafts.
