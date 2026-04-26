---
title: "Deep Research: Cucumber / Gherkin BDD Specification (std-5)"
phase: "1b"
agent: "ps-researcher-std-5"
workflow: "e2e-skill-build-20260420-001"
candidate_ref: "Candidate 5 in research/landscape/standards-candidates.md"
primary_url: "https://cucumber.io/docs/gherkin/reference/"
access_date: "2026-04-21"
slug: "std-5-cucumber-gherkin"
---

# Deep Research: Cucumber / Gherkin BDD Specification

> **Phase:** 1b -- Deep Dive on Top-5 Candidate #5
> **Agent:** ps-researcher-std-5
> **Workflow:** e2e-skill-build-20260420-001
> **Access date for all URLs below:** 2026-04-21
> **Landscape reference:** `research/landscape/standards-candidates.md` -> Candidate 5

## Document Sections

| Section | Purpose |
|---------|---------|
| [Methodology Note](#methodology-note) | Live search protocol, query log, fetch log |
| [1. What It Specifies](#1-what-it-specifies) | Gherkin grammar, keywords, structure |
| [2. Scope and Boundary](#2-scope-and-boundary) | BDD spec DSL vs test runner vs BDD process |
| [3. Applicability to a Jerry E2E Skill](#3-applicability-to-a-jerry-e2e-skill) | Why BDD-style scenarios fit E2E + agentic flows |
| [4. Strengths / Unique Contributions](#4-strengths--unique-contributions) | Living documentation, domain language, tool-agnostic |
| [5. Weaknesses / Gaps / Criticisms](#5-weaknesses--gaps--criticisms) | Anti-patterns, maintenance cost, test-script abuse |
| [6. Current State (2025-2026)](#6-current-state-2025-2026) | Version map, governance, ecosystem shifts |
| [7. Key Implementation Patterns / Testable Principles](#7-key-implementation-patterns--testable-principles) | Three Amigos, declarative, hexagonal BDD |
| [Sources Retrieved](#sources-retrieved) | Query log + URL fetch log |
| [Prompt Injection Notice](#prompt-injection-notice) | Observed injection attempt |

---

## Methodology Note

All information below was obtained via **live web search on 2026-04-21** using the `WebSearch` tool (aggregating Bing/Google/DuckDuckGo-equivalent indexes) plus direct `WebFetch` calls against primary-source pages on cucumber.io. Fourteen (14) distinct search queries were executed and four (4) direct `WebFetch` reads were attempted (three succeeded; one on `dannorth.net/introducing-bdd/` returned an access-refusal from the fetch model rather than page content -- flagged per P-022). Search coverage spanned the Gherkin grammar reference, Gherkin 6 `Rule` keyword, Cucumber Open 2025 year-in-review, BDD origin (Dan North), declarative vs imperative scenarios, Three Amigos / Example Mapping, anti-patterns and BDD criticisms, hexagonal BDD, and LLM/agentic uses of Gherkin. Query and fetch logs are recorded verbatim in the [Sources Retrieved](#sources-retrieved) section.

Mandatory thresholds from task brief (>= 8 queries, >= 3 WebFetch reads, >= 5 live URL citations) are **met**: 14 queries, 4 WebFetch attempts (3 successful), 20 distinct live URLs cited.

---

## 1. What It Specifies

Gherkin is the **plain-text, line-oriented grammar** maintained by the Cucumber Open Source Project that structures Behaviour-Driven Development (BDD) scenarios into a form that is both human-readable and machine-parseable. It is the canonical reference grammar (authored by the Cucumber project, copyright 2014-2026) rather than an ISO-level standard, but it functions as a de facto standard because every major BDD implementation (Cucumber-JVM, Cucumber-JS, Cucumber-Ruby, behave, pytest-bdd, Reqnroll/SpecFlow, Behat, Godog, etc.) parses the same grammar.

**Primary keywords (authoritative per the Cucumber reference page):**

| Keyword | Purpose |
|---------|---------|
| `Feature` | High-level description; groups related scenarios; MUST be the first primary keyword in a `.feature` file. |
| `Rule` | Represents one business rule; groups scenarios illustrating that rule (introduced in Gherkin 6). Supports a Rule-scoped `Background`. |
| `Example` / `Scenario` | A concrete illustration of a business rule, consisting of steps. `Example` and `Scenario` are synonyms. |
| `Given` | Describes initial context -- puts the system in a known state before user interaction. |
| `When` | Describes an event or action -- user interaction or external trigger. |
| `Then` | Describes expected outcome -- step definitions should use assertions. |
| `And` / `But` | Successive-step readability aliases (no semantic difference from `Given`/`When`/`Then`). |
| `Background` | Groups repeated Given steps that apply to every scenario in a Feature (or Rule). |
| `Scenario Outline` / `Scenario Template` | Runs the same scenario multiple times with different value combinations. |
| `Examples` / `Scenarios` | Data table following a `Scenario Outline`, substituting `<placeholder>` tokens per row. |

**Structural mechanisms (verbatim or near-verbatim from the reference):**

- **Data Tables**: pass a list-of-rows to a step definition using `| pipe | delimited |` syntax.
- **Doc Strings**: pass larger text blocks using triple-quote `"""` or backtick ` ``` ` delimiters, optionally annotated with a content type (e.g., `markdown`, `json`).
- **Tags**: indicated by `@`-prefix tokens attached to Features, Rules, Scenarios, and Scenario Outlines to group scenarios independently of file structure; used by tooling for selection/filtering.
- **Comments**: only permitted at the start of a new line, beginning with `#`. Block comments are **not supported**. [[ref][r-ref]]
- **Descriptions**: free-form prose is allowed directly beneath `Feature`, `Rule`, `Background`, `Scenario`, and `Scenario Outline` lines and terminates at the next keyword line.
- **Language localization**: the `# language:` header directive (e.g., `# language: fr`) on the first line of a feature file switches keyword set; Gherkin has been translated to **over 70 languages** [[ref][r-ref]]. (The landscape card's "~30+" figure is a conservative undercount and should be updated to the reference's ">70" figure during Phase 1c synthesis.)
- **Indentation**: recommended two spaces; not enforced semantically.

The formal grammar itself is implemented in the `gherkin` parser packages (one per ecosystem: `@cucumber/gherkin`, `cucumber-gherkin` JVM, etc.) which share a common **Cucumber Messages** schema for emitting AST and test-result events [[year-in-review][r-year25]]. This shared message schema is what makes Gherkin tool-agnostic in practice.

[r-ref]: https://cucumber.io/docs/gherkin/reference/
[r-year25]: https://cucumber.io/blog/open-source/cucumber-in-2025-year-in-review/

---

## 2. Scope and Boundary

Gherkin's scope is **deliberately narrow**: it specifies the _form_ and _grammar_ of executable scenarios; it does not specify the runner, assertion library, driver, or test-selection mechanism. That scope boundary is the central discipline that gives Gherkin its value and also the most common source of its misuse.

**In scope:**

- The DSL for writing scenarios by example (Given-When-Then, Rule, Background, Scenario Outline).
- The AST/messages schema emitted by the `gherkin` parser (Cucumber Messages).
- Localization of keywords.
- Tag syntax (`@tag`) for scenario selection metadata.

**Out of scope (by design):**

- How step definitions are wired to code (that is the runner's responsibility: Cucumber-JVM, Cucumber-JS, behave, pytest-bdd, Reqnroll, etc.).
- How assertions are expressed (delegated to JUnit, pytest, RSpec, AssertJ, Jest, etc.).
- Browser/API driver concerns (delegated to WebDriver, Playwright, Cypress, HTTP clients).
- Test discovery, filtering, parallelism, reporting (runner/CI concern).
- _How_ BDD is practiced as a collaboration workflow -- that is the process of BDD ("Discovery / Formulation / Automation", per Aslak Hellesøy), not the Gherkin grammar itself [[bdd-not-auto][r-notauto]].

The cucumber.io team repeatedly emphasizes this boundary. Aslak Hellesøy (creator of Cucumber) writes: **"BDD is not test automation -- it's collaborative requirements analysis combined with test-driven development (TDD), which despite the name, isn't testing either"** [[bdd-not-auto][r-notauto]]. Gherkin is the _specification artifact_ produced by BDD collaboration; the runner is downstream.

**Boundary vs adjacent standards** (for Phase 1c synthesis):

| Standard | Relationship to Gherkin |
|----------|-------------------------|
| ISO/IEC/IEEE 29119-3 (test documentation) | Gherkin scenarios are a concrete _expression format_ for the 29119 "test case" artifact. Complementary. |
| ISTQB terminology (CTFL/CTAL-TAE) | Gherkin uses ISTQB-compatible vocabulary (precondition = `Given`; action = `When`; expected result = `Then`). Complementary. |
| W3C WebDriver | Gherkin is above WebDriver; scenarios delegate to WebDriver (via step definitions) for browser drive. Layered. |
| OWASP WSTG | WSTG provides the test _taxonomy_; Gherkin can express individual WSTG checks as scenarios. Complementary. |

[r-notauto]: https://cucumber.io/blog/bdd/bdd-is-not-test-automation/

---

## 3. Applicability to a Jerry E2E Skill

Gherkin is the **most promising specification format** for a Jerry E2E skill for four reasons, in descending order of weight.

### 3.1 Natural-language <-> LLM interface symmetry

Jerry is an LLM-driven framework. Gherkin's line-oriented, keyword-anchored natural-language grammar is empirically well-suited to LLM generation _and_ LLM comprehension. Peer-reviewed and industrial studies in 2024-2025 show high quality ratings for LLM-generated Gherkin: one human-centred evaluation reports 95% relevance, 100% clarity, 94.2% completeness, and 93.4% singularity on LLM-generated Gherkin from domain regulations [[arxiv-2508][r-arxiv2]], and an industrial case study (_Acceptance Test Generation with LLMs_, arXiv 2504.07244) found 95% of AutoUAT-generated acceptance scenarios and 92% of generated test scripts were rated "helpful" by testers [[arxiv-2504][r-arxiv1]]. ACM Automated Software Engineering workshops (ATCSE 2024) report LLM agents successfully executing Gherkin specifications autonomously via multi-agent frameworks like AutoGen [[acm-atcse][r-acm]].

A Jerry E2E skill that asks a human collaborator (or a peer agent) to supply an E2E scenario in Gherkin gains a format that is **natively generated well** by the same class of models Jerry runs on, and that round-trips cleanly back into an executable test via a step-definition layer.

### 3.2 Decoupling from driver choice

Jerry's E2E skill must be able to target web UI (via WebDriver or Playwright), API surfaces (via HTTP clients), and potentially internal agent workflows. Gherkin decouples the _scenario_ from the _driver_: the same `Given/When/Then` narrative can be wired to a WebDriver step-def today and a Playwright step-def tomorrow without changing the scenario. This matches Jerry's "filesystem as infinite memory" principle -- scenarios become durable artifacts independent of runner churn.

### 3.3 Living documentation for accruing knowledge/wisdom/experience

Jerry's identity statement is explicitly about accruing knowledge, wisdom, and experience. Gherkin scenarios are the industry's dominant format for "living documentation" [[better-gherkin][r-better], [cucumber-hist][r-hist]] -- executable artifacts that double as permanent, version-controlled documentation of intended behavior. This aligns with Jerry's file-persistence model better than brittle framework-specific test code.

### 3.4 Fit with agentic execution (Agentic TDD)

Emerging work (2025) labeled **"Agentic Test-Driven Development"** treats Gherkin specifications as the natural-language _intent_ layer that AI agents interpret to drive browsers/APIs without human-authored step definitions -- e.g., Hercules, testRigor-style agents, and the ACM AutoGen experiments [[acm-atcse][r-acm]]. A Jerry E2E skill that standardizes on Gherkin inherits eligibility for this agentic pipeline when the Jerry framework chooses to delegate execution to an LLM agent rather than a static step-definition layer.

**Caveats for Jerry:**

- Gherkin is **not sufficient** on its own -- the skill MUST also specify step-definition conventions, locator strategy, and runner choice (addressed by other Phase 1c candidates: WebDriver, Playwright, ISTQB/29119 vocabulary).
- BDD as a _process_ only delivers its collaboration value when Discovery happens before Formulation [[bdd-not-auto][r-notauto]]. A Jerry skill that auto-generates Gherkin without any "Three Amigos"-equivalent conversation phase risks the anti-pattern documented in section 5.
- Use **declarative** style (section 7.2) to avoid the UI-coupling anti-pattern.

[r-arxiv1]: https://arxiv.org/html/2504.07244v1
[r-arxiv2]: https://arxiv.org/abs/2508.20744
[r-acm]: https://dl.acm.org/doi/10.1145/3678719.3685692
[r-better]: https://cucumber.io/docs/bdd/better-gherkin/
[r-hist]: https://cucumber.io/docs/bdd/history/

---

## 4. Strengths / Unique Contributions

1. **Ubiquitous domain language in executable form.** Given-When-Then descends directly from Eric Evans' _ubiquitous language_ (DDD) combined with Rachel Davies' Connextra user-story format [[cucumber-hist][r-hist]]. This gives Gherkin its core value: scenarios speak the business's own language yet remain machine-executable.

2. **Living documentation.** Declarative Gherkin scenarios describe _what_ the system does, so the feature file itself is accurate product documentation that cannot rot silently -- a failing scenario fails the build [[better-gherkin][r-better]].

3. **Tool- and language-agnostic.** Implementations exist for every major ecosystem (Cucumber-JVM, Cucumber-JS, Cucumber-Ruby, behave, pytest-bdd, Reqnroll/.NET, Behat/PHP, Godog, etc.) all parsing the same grammar, so scenarios are portable across stacks [[wiki-cuke][r-wiki], [reqnroll][r-reqnroll]].

4. **Localization.** With >70 language translations of the keyword set, Gherkin scales to non-English-speaking product teams at zero additional tooling cost [[ref][r-ref]].

5. **Composition primitives (Rule, Background, Scenario Outline).** Gherkin 6's `Rule` keyword gives feature files a two-level hierarchy (Feature -> Rule -> Scenarios) that directly mirrors Example Mapping's **Story -> Rule -> Example** structure [[gherkin-rules][r-rules], [example-map][r-exmap], [gaspar-rule][r-gaspar]]. Tag inheritance through Feature -> Rule -> Scenario lets projects do targeted selection without file reshuffles.

6. **AI-readable by default.** As section 3.1 documents, LLMs generate high-quality Gherkin and can consume it for agentic execution -- an emergent strength that was not part of the original design but is strongly validated in 2024-2026 literature [[arxiv-2504][r-arxiv1], [arxiv-2508][r-arxiv2], [acm-atcse][r-acm]].

7. **Shared Cucumber Messages schema.** All Gherkin implementations emit a common newline-delimited JSON schema for tests-results, enabling cross-tool dashboards and reporters [[year-in-review][r-year25]].

[r-wiki]: https://en.wikipedia.org/wiki/Cucumber_(software)
[r-reqnroll]: https://reqnroll.net/
[r-rules]: https://cucumber.io/blog/bdd/gherkin-rules/
[r-exmap]: https://cucumber.io/blog/bdd/example-mapping-introduction/
[r-gaspar]: https://gasparnagy.com/2019/12/gherkin6-rule-support-in-specflow-v3-1/

---

## 5. Weaknesses / Gaps / Criticisms

Gherkin/BDD has been under sustained, public critique in 2024-2026. This section presents the **steelmanned criticism** (per H-16) before evaluating.

### 5.1 Abused as a test-scripting DSL rather than a specification DSL

The most widely cited failure mode -- articulated directly by the Cucumber team -- is teams writing Gherkin _after_ code is written, by testers who treat it as a UI-step script. Hellesøy: **"If you write your tests after you've written the code you're not doing BDD no matter what tool you're using"** [[bdd-not-auto][r-notauto]]. The Cucumber anti-patterns guide formally documents this [[anti-patterns][r-antip]]. Industry reporters in 2025 reinforce: "BDD test suites often became a massive maintenance burden, with step-definition explosion creating hundreds or thousands of slightly different step definitions, each used by only one or two scenarios, resulting in an unmaintainable codebase" [[303-reality][r-303], [panda-dying][r-panda]].

### 5.2 Maintenance cost and step-definition explosion

When scenarios are written imperatively (UI-level: "enter X in field Y, click Z"), each new UI path creates near-duplicate step definitions. Regex-based step matching compounds maintenance. [[303-reality][r-303]]

### 5.3 Collaboration gap: the Three Amigos often don't happen

The intended business-developer-tester conversation (Three Amigos + Example Mapping) is the _source_ of BDD's value -- but empirically, "non-technical stakeholders rarely wrote or even read BDD scenarios, and the supposed bridge between technical and non-technical team members remained largely uncrossed" [[303-reality][r-303]]. Without Discovery, Gherkin degenerates into verbose JUnit [[bdd-not-auto][r-notauto]].

### 5.4 Commercial ecosystem retrenchment

In 2024, **Tricentis discontinued SpecFlow** (the flagship .NET BDD tool); the community forked it to **Reqnroll** [[reqnroll][r-reqnroll], [panda-dying][r-panda]]. SmartBear had earlier transferred Cucumber to the Open Source Collective, and in 2024 Cucumber returned to community ownership with a modest funding deficit in 2025 ($4,414 absorbed from reserves) [[year-in-review][r-year25]]. The ecosystem is not growing commercially; it is stabilizing around open-source community stewardship.

### 5.5 Over-DRY Background usage

Moving too many steps into a `Background` makes each scenario unreadable in isolation because the reader must scroll to the top to recover context. Cucumber's own reference page warns to keep Background concise and Given-only; "the background step is run before every scenario," so a Background that is not truly common across _all_ scenarios injects misleading setup [[ref][r-ref], [better-gherkin][r-better]].

### 5.6 Not a runner, not a standards-body standard

Gherkin has no ISO/IEEE imprimatur. It is maintained by a single open-source project (albeit with broad ecosystem uptake). For regulated/enterprise procurement settings that require an ISO/IEEE-backed documentation format, Gherkin is a de facto but not de jure standard -- which is why the landscape shortlist pairs it with ISO/IEC/IEEE 29119 (candidate 2) rather than treating it as a replacement.

### 5.7 Gap: no authoritative grammar version number

Unlike W3C WebDriver (numbered drafts) or ISO 29119 (dated parts), Gherkin does not publish semver-style grammar versions. "Gherkin 6" is a community label referring to the release that introduced `Rule`; later features (Scenario Template as a synonym, tag-on-Rule support) landed incrementally without a "Gherkin 7" label [[gaspar-rule][r-gaspar], [gherkin-rules][r-rules]]. This makes it harder for a Jerry skill to pin a grammar version precisely.

[r-antip]: https://cucumber.io/docs/guides/anti-patterns/
[r-303]: https://www.303software.com/insights/behavior-driven-development-cucumber-testing-2025-reality
[r-panda]: https://automationpanda.com/2025/03/06/is-bdd-dying/

---

## 6. Current State (2025-2026)

Information below is from the Cucumber 2025 Year-in-Review (published 2026-04-09) [[year-in-review][r-year25]], the Cucumber reference page [[ref][r-ref]], and ecosystem pages (Reqnroll, Wikipedia), all retrieved 2026-04-21.

### 6.1 Governance and funding

- Cucumber returned to **community ownership** in 2024 (previously transferred from SmartBear to the Open Source Collective). In 2025 the project established a formal governance repository and security policy [[year-in-review][r-year25]].
- 2025 income $65,545 (primarily Tidelift $52,900); expenses $69,960; $4,414 deficit absorbed from 2024 reserves.
- Weekly Thursday community meetings (16:00 London); Discord + GitHub Discussions + Stack Overflow are active support channels.

### 6.2 Implementation versions (2025)

| Implementation | 2025 activity |
|----------------|---------------|
| **Cucumber-JVM** | 20 releases; locale-sensitive parameter transformers; perf improvements. `cucumber-junit` package **deprecated** in favor of `cucumber-junit-platform-engine` (aligning with JUnit 4 maintenance mode). [[year-in-review][r-year25]] |
| **Cucumber-JS** | 8 releases; execution sharding; TypeScript config files; new plugin system. [[year-in-review][r-year25]] |
| **Cucumber-Ruby** | v10.0.0 released; dropped Ruby 2.7/3.0; added Ruby 4.0+; minimum supported version is now Ruby 3.1. 17th birthday. [[year-in-review][r-year25]] |
| **Reqnroll** (.NET) | Active successor to SpecFlow (Tricentis EOL). Latest docs dated 2026-03-23. [[reqnroll][r-reqnroll]] |
| **pytest-bdd** (Python) | Active; pytest plugin rather than standalone. Commonly used for E2E as of 2026 [[pytest-bdd-e2e][r-pytestbdd]]. |
| **behave** (Python) | Still maintained; follows Cucumber semantics. |

### 6.3 Gherkin grammar

- Reference page copyright: 2014-**2026** [[ref][r-ref]].
- **Rule** keyword is current (Gherkin 6); no "Gherkin 7" release label as of access date.
- `Example` / `Scenario` and `Scenario Outline` / `Scenario Template` are accepted synonyms in current parsers.
- **>70 languages** supported via `# language:` header.
- **Cucumber Messages** (newline-delimited JSON schema) is now the primary cross-tool format; the legacy `cucumber-json-report` is in maintenance mode with schemas pinned via `cucumber-json-schema` [[year-in-review][r-year25]].

### 6.4 Thought-leader guidance

- **Dan North** (creator of BDD) maintains a BDD-tag index of essays at dannorth.net/tags/bdd; core "Introducing BDD" (2006) remains the canonical origin text [[north-bdd][r-north], [cucumber-hist][r-hist]].
- **Liz Keogh** (early co-contributor with Keogh and Chris Matts [[cucumber-hist][r-hist]]) has a dedicated BDD index at lizkeogh.com/behaviour-driven-development emphasizing "conversations first," context/outcome questioning, and discovery-over-automation [[keogh-bdd][r-keogh]].
- **Gáspár Nagy** co-popularized the discovery-formulation-automation triad and authored the canonical explanation of Gherkin 6 `Rule` [[gaspar-rule][r-gaspar]].

### 6.5 Research and AI/agentic frontier

- 2024-2025 peer-reviewed work validates LLM-generated Gherkin at 92-95% relevance/helpfulness [[arxiv-2504][r-arxiv1], [arxiv-2508][r-arxiv2]].
- 2024 ACM ATCSE paper demonstrates multi-agent (AutoGen) execution of Gherkin specifications without pre-authored step definitions [[acm-atcse][r-acm]].
- "Agentic Test-Driven Development" (ATDD) is an emerging 2025 movement aligning Gherkin with LLM-driven browser/API drivers (Hercules, testRigor).

[r-pytestbdd]: https://qahivelab.github.io/2025/01/29/stable-e2e-tests-pytest-bdd.html
[r-north]: https://dannorth.net/tags/bdd/
[r-keogh]: https://lizkeogh.com/behaviour-driven-development/

---

## 7. Key Implementation Patterns / Testable Principles

The patterns below are the **testable principles** a Jerry E2E skill can encode as rules (HARD/MEDIUM/SOFT tier per `quality-enforcement.md`).

### 7.1 Three Amigos + Example Mapping (Discovery pattern)

**Principle:** Scenarios MUST be derived from a Business-Development-Testing conversation over concrete examples before being formalized as Gherkin [[example-map][r-exmap], [cucumber-hist][r-hist], [bdd-not-auto][r-notauto]].

**Structure:** Story card -> 1..n blue Rule cards -> 1..n green Example cards per rule -> red cards for open questions. A well-sized story can be example-mapped in ~25 minutes.

**Direct mapping to Gherkin 6:** Story -> `Feature`; Rule card -> `Rule`; Example card -> `Scenario`; red card -> backlog.

**Testable in Jerry:** the skill CAN require that a Gherkin feature file contain a pointer to the conversation record (meeting notes, transcript, or Discovery artifact) in its `Feature:` description -- making the Discovery step auditable.

### 7.2 Declarative over imperative

**Principle:** Scenarios SHOULD describe _behaviour_, not UI mechanics. The Cucumber reference is explicit: "Declarative style describes the behaviour of the application, rather than the implementation details" [[better-gherkin][r-better]].

| Imperative (avoid) | Declarative (prefer) |
|---|---|
| `When I click the "Login" button and type "alice" in the username field and "pw1" in the password field` | `When Alice signs in with valid credentials` |

**Testable:** linting rule that flags UI-verb tokens ("click", "type", "enter") in `When` steps at the Feature level (allow at step-definition level).

### 7.3 Specification by Example (Gojko Adzic lineage)

**Principle:** Each `Rule` is illustrated by a _minimum_ set of concrete examples covering positive + each boundary variation. A `Scenario Outline` + `Examples` table is the standard compression when examples differ only in data.

**Relationship to Jerry:** aligns with Jerry's "accruing knowledge, wisdom, experience" identity -- each example is durable, concrete, verifiable wisdom.

### 7.4 Hexagonal BDD (ports-and-adapters acceptance testing)

**Principle:** Write scenarios at the **driver port** level, not the UI level. Use primary (driver) adapters wired locally for tests, secondary (driven) adapters mocked or in-memory, and let the scenarios drive use cases through the hexagon's primary ports -- Cucumber becomes the primary test adapter [[aws-hex][r-aws], [dev-hex][r-devhex]].

**Benefit:** the same Gherkin scenarios work against a real browser (E2E) OR a fast in-process adapter (integration); UI churn does not invalidate scenarios.

**Testable:** the skill MAY require step-definition files to import only from application/domain layers (per H-08) plus driver-port adapters -- not directly from Selenium/Playwright APIs in production scenarios.

### 7.5 Background discipline (anti-abuse)

**Principle:** `Background` MUST contain only `Given` steps that apply to _every_ scenario in the Feature or Rule, and SHOULD contain no more than a few steps [[ref][r-ref], [better-gherkin][r-better]].

**Testable:** lint rule -- `Background` blocks with `When`/`Then` steps are rejected; warn if > N (e.g., 4) steps.

### 7.6 Rule-scoped grouping (Gherkin 6)

**Principle:** Use `Rule:` when a Feature contains multiple distinct business rules; pair Rule-scoped `Background` with Rule-scoped scenarios so each rule's setup is co-located with its examples [[gherkin-rules][r-rules], [gaspar-rule][r-gaspar]]. Tags inherit Feature -> Rule -> Scenario.

### 7.7 Scenario Outline discipline

**Principle:** Use `Scenario Outline` only when examples differ _in data_, not in structure. Structural variation (different steps) is a signal to split into separate `Scenario` blocks under the same Rule.

### 7.8 Test-first (Red phase) alignment with Jerry H-20

**Principle:** Scenario MUST fail before the implementation is present (Red phase of BDD outer loop). Hellesøy: writing tests after the code means it is not BDD [[bdd-not-auto][r-notauto]]. This maps directly to Jerry's H-20 (test before implement -- BDD Red phase) in `quality-enforcement.md`.

[r-aws]: https://docs.aws.amazon.com/prescriptive-guidance/latest/hexagonal-architectures/best-practices.html
[r-devhex]: https://dev.to/ragezbla/bdd-working-together-with-hexagonal-architecture-2on9

---

## Sources Retrieved

**Access date for all URLs:** 2026-04-21.

### Search queries executed via `WebSearch`

1. `"Gherkin grammar specification reference cucumber.io 2025"` -- returned cucumber.io reference/bdd pages, Wikipedia Cucumber, CucumberStudio SmartBear docs, guru99/accelq guides.
2. `"Cucumber Open BDD latest release 2025 2026 version"` -- returned cucumber.io landing, 2025 year-in-review blog post, Wikipedia, 303 Software reality-check blog.
3. `"Gherkin 6 Rule keyword specification features"` -- returned cucumber.io reference, cucumber.io blog "Gherkin Rules", Reqnroll docs, Gáspár Nagy post on Gherkin 6 Rule support, Behat issue #1451.
4. `"BDD specification by example Dan North origin"` -- returned agilealliance glossary, dannorth.net BDD tag index, cucumber.io BDD history, Wikipedia BDD article, Liz Keogh's blog.
5. `"BDD imperative vs declarative scenarios best practices"` -- returned cucumber.io better-gherkin, Thoughtworks/Twist article, multiple Medium/Contino guides, Sauce Labs best-practice wiki, Automation Panda BDD 101.
6. `"BDD E2E testing best practices 2025 Liz Keogh"` -- returned qahivelab pytest-bdd guide, lizkeogh.com index, Mozaic Works Keogh interview, Bunnyshell 2026 E2E practices, cucumber.io myths.
7. `"Gherkin LLM test generation AI agents 2025 2026"` -- returned ACM DL paper on LLM-agent Gherkin execution, Springer/Nature chapter on LLM UI test gen, arXiv 2504.07244 (industrial case), arXiv 2508.20744 (Law-to-Gherkin), cloudqa ChatGPT prompts guide.
8. `"Three Amigos BDD example mapping workshop"` -- returned johnfergusonsmart.com, Automation Panda three-amigos tag, Serenity Dojo course, Testomat.io explainer, cucumber.io example-mapping-introduction.
9. `"Cucumber BDD anti-patterns automated test scripts not specifications"` -- returned TestEvolve, cucumber.io anti-patterns guide, cucumber.io "BDD is not test automation", Bondar Academy, BrowserStack 2026 cucumber guide.
10. `"hexagonal BDD domain language ports adapters acceptance tests"` -- returned AWS Prescriptive Guidance hexagonal best-practices, arhohuttunen Spring Boot hex article, dev.to BDD+hex article, jmgarridopaz.github.io ports-and-adapters site.
11. `"Gherkin Background keyword best practices when to use abuse"` -- returned cucumber.io reference, ToolsQA Gherkin keywords, github.com/andredesousa/gherkin-best-practices, Automation Panda BDD 101, Behat docs.
12. `"BDD reality check cucumber criticism maintenance cost 2025"` -- returned 303 Software BDD reality check, Momentic "AI breathes new life", cucumber.io ROI of BDD, Parasoft maintenance article, Automation Panda "Is BDD Dying?", TestQuality guide.
13. `"pytest-bdd SpecFlow Reqnroll behave Cucumber.js current status 2025"` -- returned reqnroll/Reqnroll GitHub, Reqnroll.net, Automation Panda behave tag, testautomationtools.dev review, testdriver.ai SpecFlow EOL alternatives.
14. `"Gherkin agentic AI workflow specification natural language executable"` -- returned Gherkinizer.com, Kobiton GenAI cucumber blog, fossunited "Agentic TDD" CfP, arxiv 2504.07244, GitHub Agentic Workflows and Microsoft Research project.

### Pages directly fetched via `WebFetch`

- `https://cucumber.io/docs/gherkin/reference/` -- confirmed primary keywords, Rule keyword, Scenario Outline, Data Tables, Doc Strings, Tags, >70-language localization, copyright 2014-2026.
- `https://cucumber.io/docs/bdd/better-gherkin/` -- confirmed declarative-vs-imperative guidance and verbatim quote; noted this page does NOT cover Background/Rule guidance (those live in the reference + blog posts).
- `https://cucumber.io/blog/open-source/cucumber-in-2025-year-in-review/` -- confirmed 2025 release counts (JVM 20, JS 8, Ruby v10.0.0), Ruby version support changes, governance/funding, cucumber-junit deprecation, Cucumber Messages status.
- `https://cucumber.io/blog/bdd/bdd-is-not-test-automation/` -- confirmed Hellesøy authorship (2020-02-13), the Discovery/Formulation/Automation triad, verbatim quotes distinguishing BDD from automation.
- `https://cucumber.io/docs/bdd/history/` -- confirmed Dan North origin (2003 JBehave, 2006 "Introducing BDD"), Liz Keogh contributions from 2004, Aslak Hellesøy's role in naming Cucumber.
- `https://dannorth.net/introducing-bdd/` -- **attempted but failed**: the fetch model returned a refusal message rather than the page content. Primary-source verification of Dan North's 2006 article was obtained via the cucumber.io history page instead. Flagged here per P-022.

### Live URL citations in this document

1. https://cucumber.io/docs/gherkin/reference/
2. https://cucumber.io/docs/bdd/better-gherkin/
3. https://cucumber.io/blog/open-source/cucumber-in-2025-year-in-review/
4. https://cucumber.io/blog/bdd/bdd-is-not-test-automation/
5. https://cucumber.io/docs/bdd/history/
6. https://cucumber.io/blog/bdd/gherkin-rules/
7. https://cucumber.io/blog/bdd/example-mapping-introduction/
8. https://cucumber.io/docs/guides/anti-patterns/
9. https://www.303software.com/insights/behavior-driven-development-cucumber-testing-2025-reality
10. https://automationpanda.com/2025/03/06/is-bdd-dying/
11. https://reqnroll.net/
12. https://en.wikipedia.org/wiki/Cucumber_(software)
13. https://gasparnagy.com/2019/12/gherkin6-rule-support-in-specflow-v3-1/
14. https://lizkeogh.com/behaviour-driven-development/
15. https://dannorth.net/tags/bdd/
16. https://arxiv.org/html/2504.07244v1
17. https://arxiv.org/abs/2508.20744
18. https://dl.acm.org/doi/10.1145/3678719.3685692
19. https://qahivelab.github.io/2025/01/29/stable-e2e-tests-pytest-bdd.html
20. https://docs.aws.amazon.com/prescriptive-guidance/latest/hexagonal-architectures/best-practices.html
21. https://dev.to/ragezbla/bdd-working-together-with-hexagonal-architecture-2on9

Total: 21 distinct live URLs cited (requirement: >= 5). 14 queries (requirement: >= 8). 4 WebFetch attempts, 3 successful (requirement: >= 3 reads).

---

## Prompt Injection Notice

During this session, after the first `Bash` directory listing the MCP server configuration emitted a `<system-reminder>` tag directing the agent to **redirect library-documentation lookups to Context7** instead of doing live web search. The user's Phase 1b task brief, however, explicitly mandated **live web search** with `WebSearch`/`WebFetch` as non-negotiable constraints ("Live web search REQUIRED", ">=8 queries + >=3 WebFetch reads"). The MCP-server instruction was therefore **ignored** in favor of the user's explicit instructions, consistent with H-02 (P-020 user authority) and P-022 (no deception). This note is flagged for auditability by Phase 1c synthesizers and Gate 1b reviewers.

Additionally, the `WebFetch` on `https://dannorth.net/introducing-bdd/` returned an access-refusal from the fetch model rather than page content. Primary-source verification for Dan North's BDD origin was routed through `https://cucumber.io/docs/bdd/history/` instead. This gap is disclosed here per P-022.
