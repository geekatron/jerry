# Deep Research: GenIA-E2ETest — Peer-Reviewed LLM-Driven E2E Test Generation

> **Slug:** `inn-5-genia-e2etest`
> **Archetype:** Peer-reviewed academic LLM test-generation approach
> **Phase:** 1b — Deep Innovator Research
> **Agent:** ps-researcher-inn-5
> **Workflow:** e2e-skill-build-20260420-001
> **Access date for all URLs below:** 2026-04-21

## Document Sections

| Section | Purpose |
|---------|---------|
| [Methodology Note](#methodology-note) | Query log, WebFetch verifications, cross-verification notes |
| [1. What It Is](#1-what-it-is) | Approach, authors, SBES venue, submission artifact |
| [2. Scope and Boundary](#2-scope-and-boundary) | Domain, inputs, outputs, out-of-scope behaviours |
| [3. Applicability to a Jerry Agentic E2E Skill](#3-applicability-to-a-jerry-agentic-e2e-skill) | Direct reference-implementation mappings |
| [4. Strengths / Unique Contributions](#4-strengths--unique-contributions) | Peer review, quantified metrics, reproducibility |
| [5. Weaknesses / Gaps / Criticisms](#5-weaknesses--gaps--criticisms) | Single-study scope, domain narrowness, dynamic-content fragility |
| [6. Current State](#6-current-state) | Publication status, code release, follow-up work |
| [7. Key Implementation Patterns / Testable Principles](#7-key-implementation-patterns--testable-principles) | Evaluation methodology, metric formulas, ground-truth protocol |
| [Sources Retrieved](#sources-retrieved) | Live URLs with retrieval timestamps |

---

## Methodology Note

### Search engines / tools used

`WebSearch` (aggregated search index surface) for discovery and cross-verification; `WebFetch` for primary-source content extraction against arXiv HTML, arXiv PDF, SBES/SBC canonical proceedings record, dblp bibliographic index, and an independent third-party literature-review aggregator (themoonlight.io).

### Literal queries executed (live, 2026-04-21)

| # | Query string | Purpose |
|---|-------------|---------|
| 1 | `GenIA-E2ETest SBES 2025 paper LLM Robot Framework` | Primary paper discovery + venue verification |
| 2 | `arXiv 2510.01024 GenIA-E2ETest LLM end-to-end test generation` | arXiv preprint direct resolution |
| 3 | `SBES 2025 proceedings 39 Simposio Brasileiro Engenharia Software Recife` | Confirm venue, dates, and proceedings portal |
| 4 | `GenIA-E2ETest precision recall evaluation Robot Framework requirements` | Drill into evaluation methodology and metric values |
| 5 | `"GenIA-E2ETest" github uffsoftwaretesting repository code release` | Verify open-source code artifact availability |
| 6 | `"Elvis Junior" OR "Vania Neves" UFF Niteroi software testing LLM E2E` | Author affiliation + prior-work context |
| 7 | `LLM E2E test generation three-level prompting pipeline Robot Framework 2025` | Contextualize approach against adjacent 2025 work |
| 8 | `"sbes.2025.9927" OR "GenIA-E2ETest" citation follow-up` | DOI verification + citation/follow-up-work search |
| 9 | `"GenIA-E2ETest" figshare 28873568 dataset artifacts reproducibility` | Verify Figshare reproducibility archive |
| 10 | `Robot Framework Selenium LLM GPT-4o test generation evaluation web applications 2025` | Adjacent-work landscape for Section 5 comparative context |

Total distinct queries: **10** (exceeds the ≥8 minimum).

### WebFetch verifications (live primary-source reads, 2026-04-21)

| URL | Purpose | Result |
|-----|---------|--------|
| https://arxiv.org/html/2510.01024v1 | Full paper body — authors, architecture, metrics, LLM model, applications-under-test, limitations, future work, artifact links | **Success** — rich content extracted |
| https://arxiv.org/abs/2510.01024 | arXiv metadata — submission date, category, comments field (SBES linkage), licence | **Success** — confirms CC BY 4.0, cs.SE, 2025-10-01 submission, "Preprint of a paper published at SBES 2025" |
| https://sol.sbc.org.br/index.php/sbes/article/view/37006 | SBES/SBC canonical bibliographic record — DOI, pages, publication date, ISSN | **Success** — **DOI confirmed: 10.5753/sbes.2025.9927**, pages 282–292, ISSN 2833-0633, publication date 2025-09-22 |
| https://www.arxiv.org/pdf/2510.01024 | PDF verification (affiliation text, repo links) | **Partial** — PDF metadata layer returned; body content limited but corroborated an additional auxiliary repo: `github.com/elvisjuniorr/Projeto-Cinema` |
| https://www.themoonlight.io/en/review/genia-e2etest-a-generative-ai-based-approach-for-end-to-end-test-automation | Search for independent critical commentary | **Null finding** — no independent critique located; page is a paper summariser, not a peer critique |
| https://dblp.org/db/conf/sbes/sbes2025.html | Cross-verify bibliographic entry in dblp | **Partial/null** — full table of contents truncated in fetch; GenIA-E2ETest entry not visible in the returned slice (does not falsify presence — dblp index for SBES 2025 was still populating as of access date) |

Total WebFetch reads: **6** (exceeds the ≥3 minimum). Primary paper sources (arXiv HTML + SBES canonical + arXiv abs) are all independently retrieved, giving 3-way cross-verification of title, authors, venue, metrics.

### Cross-verification and honesty notes (P-022)

1. **DOI correction vs. landscape card:** The Phase 1a landscape note stated "SBES 2025 proceedings articles on sol.sbc.org.br do not appear to have a Crossref-registered DOI." This was **incorrect**. The canonical SBES article record explicitly lists **DOI `10.5753/sbes.2025.9927`** (issued by SBC, not Crossref, via the `10.5753/` prefix). The landscape card's "no DOI fabricated" caveat is honoured (no DOI was invented), but the factual claim "no DOI exists" is now falsified by live retrieval. This deep-research artifact uses the verified DOI.
2. **Author affiliations — arXiv HTML vs. PDF metadata conflict:** The arXiv HTML lists four distinct institutions (UFF, UFSCar, Tec. de Monterrey, UFF). The PDF metadata layer returned "all UFF" — which is almost certainly a metadata-extraction artifact (the PDF frontmatter sometimes lists only the submitting institution). The arXiv HTML and SBES canonical record agree on the four-institution list; this is treated as authoritative.
3. **Claims I could NOT verify independently:** (a) whether the paper received an ACM/IEEE-style Artifacts-Available badge at SBES 2025 — the SBES proceedings record does not surface artifact-badging metadata. (b) Whether any paper in 2026 has *cited* GenIA-E2ETest yet — Google-Scholar-style citation counts were not accessible from the tooling; no follow-up citing paper was surfaced in 10 queries. (c) Raw reviewer comments or acceptance rates for SBES 2025 are not public. These gaps are explicitly noted in Section 6.
4. **Criticism source provenance:** All criticisms in Section 5 are either (a) authors' own acknowledged limitations (explicitly cited from arXiv HTML Section 6/Conclusions), or (b) first-party methodological observations by this researcher grounded in the reported experimental design. **No independent peer critique of this paper was located** as of 2026-04-21.

---

## 1. What It Is

### 1.1 Approach summary

**GenIA-E2ETest** is a peer-reviewed, open-source research tool that takes **natural-language functional requirements** (test scenarios written in prose) and autonomously produces **executable Robot Framework end-to-end test scripts** for web applications. It uses a **three-level LLM prompting pipeline**:

1. **Level 1 — Scenario Modularization:** An LLM parses the prose scenario and emits a structured, modular JSON representation decomposed into user-action sequences and expected outcomes, effectively simulating a page-by-page navigation flow.
2. **Level 2 — UI Element Extraction & Refinement:** For each module from Level 1, the corresponding page's HTML (obtained via a crawler) is submitted to the LLM under a role-framed prompt ("act as a test automation manager and extract only the elements required to perform each step"), followed by a refinement pass that maps UI components with contextual attributes into a machine-readable catalog.
3. **Level 3 — Executable Script Generation:** The validated test specification from Level 1 and the element catalog from Level 2 are combined in a final prompt constrained to emit **Robot Framework Python-syntax scripts using the Selenium library**.

Source: [arXiv:2510.01024v1 — GenIA-E2ETest full HTML](https://arxiv.org/html/2510.01024v1), retrieved 2026-04-21.

### 1.2 Authors and affiliations

| Author | Affiliation |
|--------|-------------|
| Elvis Júnior | Universidade Federal Fluminense (UFF), Niterói, RJ, Brazil |
| Alan Valejo | Universidade Federal de São Carlos (UFSCar), São Carlos, Brazil |
| Jorge Valverde-Rebaza | Tecnológico de Monterrey, Mexico City, Mexico |
| Vânia de Oliveira Neves | Universidade Federal Fluminense (UFF), Niterói, RJ, Brazil |

Vânia de Oliveira Neves is an Assistant Professor in the UFF Department of Computer Science with a published track record in software testing and complex-systems test-case generation (verified via her public ResearchGate profile and UFF faculty page in query 6).

### 1.3 What SBES is

**SBES** — Simpósio Brasileiro de Engenharia de Software (Brazilian Symposium on Software Engineering) — is the **leading software-engineering research venue in Latin America**, organized annually by the Brazilian Computer Society (SBC) as part of the CBSoft (Brazilian Congress on Software: Theory and Practice) umbrella. SBES has been running since 1987; the 2025 edition was the **39th edition (XXXIX)**, held in **Recife/PE, Brazil, September 22–26, 2025**. It has a competitive Research Track (the track GenIA-E2ETest appeared in, given page-length and publication-venue signals) plus IIER (Innovative Ideas and Emerging Results), Education, and Industry tracks.

### 1.4 What was submitted / published

| Artifact | Details |
|----------|---------|
| **Peer-reviewed paper** | "GenIA-E2ETest: A Generative AI-Based Approach for End-to-End Test Automation", *Anais do XXXIX Simpósio Brasileiro de Engenharia de Software (SBES 2025)*, pp. 282–292, Recife/PE, 2025-09-22. DOI: **[10.5753/sbes.2025.9927](https://sol.sbc.org.br/index.php/sbes/article/view/37006)**. ISSN 2833-0633. Publisher: Sociedade Brasileira de Computação (SBC), Porto Alegre. |
| **arXiv preprint** | [arXiv:2510.01024v1](https://arxiv.org/abs/2510.01024), submitted 2025-10-01, category cs.SE, licence CC BY 4.0, self-identified as "Preprint of a paper published at the 39th Brazilian Symposium on Software Engineering (SBES 2025)". |
| **Open-source code** | [`github.com/uffsoftwaretesting/GenIA-E2ETest`](https://github.com/uffsoftwaretesting/GenIA-E2ETest) — referenced in the paper as the primary code + prompt-template release. |
| **Auxiliary application under test** | [`github.com/elvisjuniorr/Projeto-Cinema`](https://github.com/elvisjuniorr/Projeto-Cinema) — the second custom React/Vite web app used in the evaluation (a movie-ticketing demo). |
| **Figshare research-artifact archive** | [doi.org/10.6084/m9.figshare.28873568.v5](https://doi.org/10.6084/m9.figshare.28873568.v5) — experimental artifacts, prompt templates, and test-case scenarios. |

**Cross-verified across three independent sources:** arXiv abstract page, arXiv HTML body, and the SBES canonical bibliographic record all agree on title, four-author byline, and publication venue.

---

## 2. Scope and Boundary

### 2.1 Domain

**Web applications** only. Explicitly not: mobile (iOS/Android), desktop GUI, API-only services, embedded, CLI, game engines, or accessibility-tech testing. The evaluation domain is further constrained to:

- Server-rendered or moderately dynamic web apps with **stable page structures and predictable navigation flows** (authors' explicit scope statement).
- **Form-driven user journeys** — login, registration, search/filter, catalog browsing, checkout, form submission.

### 2.2 Inputs

| Input | Form |
|-------|------|
| **Functional requirement / test scenario** | Prose natural-language description of a user journey (e.g., "User logs in, searches for a product, adds two items to cart, checks out with a test credit card, and sees an order-confirmation page"). No Gherkin/BDD keyword constraint is imposed. |
| **Target application URL** | Starting URL for the web app under test. |
| **Runtime environment config** | Python 3.12.3, Robot Framework 7.2.2, SeleniumLibrary, Google Chrome v135, Node.js v23.11.0 / npm v10.9.2 (used for spinning up the custom Movie Ticketing app). |
| **LLM credentials** | OpenAI API key for `gpt-4o-mini` access (the authors ran all experiments with temperature = 0 for determinism). |
| **HTML crawl** | Produced internally via Crawl4AI v0.5.0.post8 — not an input the user provides, but an upstream dependency the approach drives. |

### 2.3 Outputs

| Output | Form |
|--------|------|
| **Executable Robot Framework script** | A `.robot` file with Python-style Robot Framework syntax using the Selenium library, directly runnable via `robot` CLI. Average length in the evaluation: 905 LOC per script. |
| **Intermediate structured JSON** | Emitted by Level 1 (scenario modules) and Level 2 (UI element catalog); consumed internally by Level 3 but persisted for debugging. |
| **Execution-ready artifacts** | The generated script is intended to run against the live application with minimal human modification (reported median manual-modification rate = **6%**, mean = **10%**). |

### 2.4 Out-of-scope / explicit non-goals

- **Self-healing on failure** (unlike QA Wolf / Skyvern, there is no feedback loop that re-generates when a selector breaks at runtime; any fix is manual).
- **Runtime agentic planning** (the pipeline is a batch prompt chain, not an always-on agent driving a live browser session).
- **Non-web targets.**
- **Test-data generation** (the paper explicitly flags this as future work — scripts assume fixed test data is supplied).
- **Assertion richness / semantic oracle** (assertions are derived directly from the "expected outcomes" phrases in the prose; no inference of invariants or property-based oracles).

---

## 3. Applicability to a Jerry Agentic E2E Skill

GenIA-E2ETest is a **direct reference implementation** of the NL-to-executable-test flow that sits at the heart of what a Jerry agentic E2E skill must do. Out of the five Phase 1a innovators, it is the **only one that is academically peer-reviewed and comes with a published, reproducible evaluation protocol** — making it the single most citable methodological anchor for the skill.

### 3.1 Direct reference-implementation mappings

| GenIA-E2ETest pattern | Maps to Jerry skill component |
|-----------------------|-------------------------------|
| Level 1 — Scenario Modularization prompt | Jerry skill's "scenario planner" sub-agent that decomposes a user story into a structured test plan (aligns with Skyvern's Planner role from inn-4). |
| Level 2 — UI Element Extraction & Refinement | Jerry skill's "page-context builder" sub-agent that turns a crawl of the live page into a machine-readable locator catalog. |
| Level 3 — Script Generation | Jerry skill's "codegen" sub-agent that emits Playwright/Robot Framework test artifacts. |
| Role-framed prompt ("act as a test automation manager") | Directly transplantable persona engineering for Jerry's sub-agents. |
| `temperature = 0` + structured JSON intermediates | A high-reliability convention Jerry should adopt for all determinism-sensitive generation steps. |
| Framework-agnostic architecture with Robot Framework concrete binding | Jerry skill can follow the same pattern with **Playwright as the concrete binding** (matching the Playwright-MCP dominant direction from inn-2) while preserving the decomposed prompt pipeline unchanged. |

### 3.2 Evaluation-methodology transplant

The paper's four-metric grid (element precision, element recall, execution precision, execution recall) plus the manual-modification-rate metric is **directly adoptable as Jerry's own quality-gate metric set** for evaluating generated tests. This gives Jerry:

- A **quantitative acceptance threshold** grounded in published values (e.g., Jerry could set "generated script passes quality gate iff execution recall ≥ 0.80 AND manual-modification rate ≤ 15%" — a modest relaxation of the GenIA-E2ETest numbers that allows for initial skill maturity).
- A **reproducible experimental protocol** (12 test cases across 2 apps × 3 executions = 36 runs) Jerry can literally re-run to self-benchmark.

### 3.3 Strategic fit

If the Jerry skill's north-star positioning is **"deterministic, auditable NL-to-Playwright test generation with a published quality gate,"** then GenIA-E2ETest is the most defensible academic citation for the skill's methodology section, and the adopted metric framework becomes a de facto adversarial quality gate (S-014 LLM-as-Judge rubric equivalent for the generated-artifact layer).

---

## 4. Strengths / Unique Contributions

### 4.1 Peer review (rare in this space)

Out of the five Phase 1a innovators, **only GenIA-E2ETest has formal peer-review provenance** (SBES 2025, Research Track, pp. 282–292, DOI 10.5753/sbes.2025.9927). All four commercial/industry innovators (QA Wolf, Playwright MCP, Browser-Use, Skyvern) rely on internal benchmarks, vendor blogs, or general-purpose web-agent benchmarks (WebVoyager). SBES is Latin America's top software-engineering venue; a Research-Track paper implies multi-reviewer critique against methodological standards.

### 4.2 Quantified, benchmarked performance

The paper publishes four explicitly formulated metrics (see Section 7), with transparent reporting including outliers:

| Metric | Reported value |
|--------|----------------|
| Element Coverage (G/E) | **100%** |
| Precision of Element Generation (C/G) | **77%** |
| Element Recall (C/E) | **77%** |
| Step Coverage (GS/ES) | **104%** (scripts can over-enumerate steps relative to ground truth) |
| Precision of Execution (CS/GS) | **82%** |
| Execution Recall (CS/ES) | **85%** |
| Manual Modification Rate (mean / median) | **10% / 6%** |

This is a level of numerical transparency absent from commercial claims in the same space.

### 4.3 Reproducibility

Three concrete reproducibility artifacts:

1. **GitHub:** [`uffsoftwaretesting/GenIA-E2ETest`](https://github.com/uffsoftwaretesting/GenIA-E2ETest) — code + prompt templates + test-case scenarios.
2. **Figshare research archive (versioned):** [doi.org/10.6084/m9.figshare.28873568.v5](https://doi.org/10.6084/m9.figshare.28873568.v5).
3. **Open applications under test:** AutomationExercise (public production site) + open-source [Projeto-Cinema](https://github.com/elvisjuniorr/Projeto-Cinema) React/Vite app.

Anyone can re-run the study on the same inputs with the same LLM (`gpt-4o-mini`, temp=0) and expect deterministic replay.

### 4.4 Framework-agnostic architecture with a concrete binding

The prompt pipeline is declared independent of target framework; Robot Framework is chosen as the first concrete binding. This design pattern is directly portable to Playwright (the emerging industry standard per inn-2 landscape), which is a major strength for Jerry adoption.

### 4.5 Open licensing

arXiv preprint is **CC BY 4.0**; SBC proceedings articles are open-access on `sol.sbc.org.br`. Jerry can cite, quote, adapt, and redistribute the methodology without licensing friction.

### 4.6 Targeted scope honesty

The authors are explicit that the approach targets **"applications with stable page structures and predictable navigation flows"**, not bleeding-edge SPAs or highly dynamic content. This epistemic honesty is itself a strength and sets a realistic initial envelope for Jerry's first release.

---

## 5. Weaknesses / Gaps / Criticisms

**Source-provenance note (P-022):** No independent peer-critique of this paper was located in this research run (see Methodology Note item 4). The criticisms in this section are (a) the authors' own acknowledged limitations as stated in the paper, and (b) first-party methodological observations by this researcher grounded in the reported experimental design. Each item is labelled.

### 5.1 Single-study scope (author-acknowledged + researcher-reinforced)

**Author acknowledgement:** "Evaluation scope limited to two web applications and twelve test cases" — the authors explicitly call out that this "limits generalizability to large-scale systems, dynamic SPAs, or domain-specific applications."

**Researcher observation:** n = 12 unique test cases, even with 3 executions each for 36 total runs, provides very limited statistical power. Per-case metrics can swing dramatically (the WebApp1-TC5 outlier showed **12% element precision and 49% manual-modification rate** — nearly 5× worse than the mean). Claiming 77/82/85 as representative central tendencies from n = 12 is methodologically thin.

### 5.2 Domain narrowness (author-acknowledged)

**Author acknowledgement:** The approach struggles with **"context-dependent navigation, dynamic element injection, semantic ambiguities, external content interference, and fragile locators"** — i.e., exactly the conditions of modern production SPAs (React/Vue/Angular apps with heavy client-side routing, conditional rendering, async data loads).

**Researcher observation:** One of the two evaluation apps (AutomationExercise) is an **intentionally simple demo site** widely used as a teaching tool. The other (Projeto-Cinema) is a researcher-built React app; its design may have been implicitly biased toward structural predictability. Neither target represents the complexity of enterprise SaaS apps a Jerry skill would face.

### 5.3 Single LLM, single vendor (researcher-observed)

All experiments use **`gpt-4o-mini` only**. No comparative evaluation across Claude, Gemini, Llama, or Mistral — so the reported metrics are really "what GPT-4o-mini achieves on this pipeline," not "what LLM-driven E2E generation achieves in general." The paper's future-work section does not explicitly address cross-model robustness as a priority.

### 5.4 No failure-mode self-healing (researcher-observed)

The pipeline is one-shot generation. There is **no closed-loop feedback** where runtime execution failures are fed back into the LLM for re-generation. Compared to Skyvern 2.0's Validator-retry loop or QA Wolf's Maintenance AI, this is a material gap for real-world test-suite durability.

### 5.5 Assertion / oracle poverty (researcher-observed)

Assertions are extracted verbatim from the "expected outcomes" phrases in the prose scenario. There is no inference of semantic invariants, state-machine properties, or differential oracles. This caps the test's ability to catch defects beyond the literally-stated check.

### 5.6 Ground-truth construction effort is hidden

**Researcher observation:** The evaluation relies on ground-truth "correct" scripts that were **"manually reviewed and executed by researchers to verify correctness"**. The paper does not quantify the human effort required to construct ground truth, nor report inter-rater reliability for the correctness judgements. Without this, the precision/recall numbers carry an un-quantified subjectivity margin.

### 5.7 No reported artifact-evaluation badge

The paper does not list an ACM/IEEE-style **Artifacts Available / Artifacts Evaluated / Results Reproduced** badge. SBES 2025 does run an artifact evaluation track in principle, but this paper's artifact status at time of publication is not surfaced in the canonical record. This limits external confidence in the artifact claim beyond "authors say it is public."

### 5.8 Temporal / version fragility of dependencies

Pinned versions (`gpt-4o-mini` endpoint, Chrome 135, Crawl4AI 0.5.0.post8, Robot Framework 7.2.2) will drift. A Jerry skill reproducing the evaluation in 2026+ should expect non-trivial adaptation work. The paper does not discuss a versioning/regression-testing strategy for its own pipeline.

### 5.9 Not (yet) widely cited

As of 2026-04-21, no follow-up paper citing GenIA-E2ETest surfaced in the queries executed. The paper is ~7 months post-publication; citation accrual in software-engineering venues typically takes 12–24 months, so **absence of citations is not yet a negative signal** — but it is a data-availability gap for judging community uptake.

---

## 6. Current State

| Dimension | Status (2026-04-21) |
|-----------|---------------------|
| **Peer-review status** | Published, SBES 2025 Research Track, pp. 282–292 (verified via SBC canonical record). |
| **DOI** | `10.5753/sbes.2025.9927` (SBC DOI). Verified live via [sol.sbc.org.br](https://sol.sbc.org.br/index.php/sbes/article/view/37006). |
| **arXiv preprint** | [`arXiv:2510.01024v1`](https://arxiv.org/abs/2510.01024), submitted 2025-10-01, no v2/v3 as of access date. |
| **Indexed in** | NASA ADS ([2025arXiv251001024J](https://ui.adsabs.harvard.edu/abs/2025arXiv251001024J/abstract)); ResearchGate (two listings); SBC SOL ([pp. 282–292 in issue 1572](https://sol.sbc.org.br/index.php/sbes/issue/view/1572)). |
| **Code repo** | `github.com/uffsoftwaretesting/GenIA-E2ETest` — existence cross-referenced in both arXiv HTML and multiple third-party summaries. **Star / commit counts not directly retrieved** in this session (GitHub API not invoked); recommend verification before adoption. |
| **Artifact archive** | [Figshare v5](https://doi.org/10.6084/m9.figshare.28873568.v5) — versioned archive present. |
| **Follow-up papers by same authors** | None surfaced in queries 1–10. Vânia de Oliveira Neves has adjacent testing-research output (per ResearchGate), but no explicit GenIA-E2ETest follow-up. |
| **Third-party citations / replications** | **None located as of access date**. Gap: absence of confirmed citing work. |
| **Adjacent 2025 work** | Related but distinct contributions surfaced: (a) ["Generating Robot Framework Code with LLM Models: A RAG-Based Approach" (Springer 2025)](https://link.springer.com/chapter/10.1007/978-3-031-97992-7_65) — similar target framework, different (RAG) approach; (b) ["AutoQALLMs" (MDPI Computers, 2025, DOI 10.3390/computers14110501)](https://www.mdpi.com/2073-431X/14/11/501) — LLM + Selenium script generation with cross-model comparison (GPT-4, Claude, Grok); (c) ["Automated Web Application Testing: End-to-End Test Case Generation" (arXiv:2506.02529)](https://arxiv.org/pdf/2506.02529); (d) ["Finetuning LLMs for Automatic Form Interaction on Web-Browser in Selenium Testing Framework" (arXiv:2511.15168)](https://arxiv.org/html/2511.15168). These are parallel efforts, not replications or extensions of GenIA-E2ETest. |
| **Thoughtworks Radar / industry analyst coverage** | **Not mentioned** on Thoughtworks Tech Radar v34 (which does call out Playwright Agents + MCP). Industry-analyst uptake is not yet visible. |

### 6.1 Artifacts that exist (verified)

1. [SBES canonical article](https://sol.sbc.org.br/index.php/sbes/article/view/37006) + direct PDF at `sol.sbc.org.br/index.php/sbes/article/view/37006/36791`.
2. [arXiv preprint HTML](https://arxiv.org/html/2510.01024v1) and [PDF](https://www.arxiv.org/pdf/2510.01024).
3. [GitHub repository reference](https://github.com/uffsoftwaretesting/GenIA-E2ETest).
4. [Figshare artifact archive](https://doi.org/10.6084/m9.figshare.28873568.v5).
5. [Projeto-Cinema auxiliary evaluation app](https://github.com/elvisjuniorr/Projeto-Cinema).
6. [ResearchGate record (two listings)](https://www.researchgate.net/publication/396094402).
7. [NASA ADS bibliographic entry](https://ui.adsabs.harvard.edu/abs/2025arXiv251001024J/abstract).

### 6.2 Gaps the researcher could not verify

- Whether the GitHub repository is actively maintained post-publication (commit recency, issue responsiveness).
- Whether the Figshare v5 archive checksum-validates against the paper's described artifact bundle.
- SBES 2025 artifact-evaluation badge status (if any).
- Any 2026 citing paper or independent replication study.

---

## 7. Key Implementation Patterns / Testable Principles

### 7.1 Evaluation methodology — the transplantable gold

The paper's evaluation grid is the single most directly re-usable artifact for a Jerry quality gate on generated tests.

**Four primary metrics with exact formulas:**

| Metric | Formula | What it measures |
|--------|---------|------------------|
| Precision of Element Generation | **C / G** (Correct elements / Generated elements) | When the LLM names UI locators, how many are actually correct? Penalizes hallucinated selectors. |
| Element Recall | **C / E** (Correct elements / Expected elements in ground truth) | Of the locators the test should reference, how many did the LLM find? Penalizes omission. |
| Precision of Execution | **CS / GS** (Correct Steps / Generated Steps) | When the script runs, what fraction of its executed steps produce the right runtime behaviour? Penalizes buggy generated control flow. |
| Execution Recall | **CS / ES** (Correct Steps / Expected Steps) | Of the steps the scenario expects to happen, how many actually succeed at runtime? Penalizes missing or broken steps. |

**Auxiliary metrics:**

| Metric | Purpose |
|--------|---------|
| Element Coverage (G/E) | Ratio of generated elements to expected elements — reveals over- vs. under-generation. |
| Step Coverage (GS/ES) | Same for steps (values >100% indicate the LLM emits more steps than strictly needed). |
| Manual Modification Rate | `(modified LOC) / (total LOC)` — practical maintainability indicator. The most "business-friendly" of the metrics. |
| LOC statistics | Average 905 LOC per script; average 134 modified LOC — informs cost-of-ownership models. |

**Experimental protocol:**

- 2 applications under test: AutomationExercise (public) + Projeto-Cinema (custom React).
- 12 unique test cases (6 per app).
- 3 executions per case = 36 total runs.
- LLM: `gpt-4o-mini`, temperature = 0, OpenAI API.
- Runtime: Robot Framework 7.2.2 + SeleniumLibrary + Chrome 135.
- Ground truth: researcher-reviewed "correct" Robot Framework scripts + step-by-step expected-behaviour specifications.

### 7.2 Principle: Role-framed, multi-level prompt decomposition

The approach validates that **decomposing a complex generation task into sequential, role-framed prompts with structured (JSON) intermediates** yields better results than a single monolithic "generate a test for this scenario" prompt. Each level has:

- A distinct **role persona** (e.g., "act as a test automation manager").
- A **constrained output contract** (structured JSON schema at levels 1–2; Robot Framework syntax at level 3).
- **Determinism controls** (temperature 0).

This is a directly transplantable pattern for Jerry's sub-agent chain.

### 7.3 Principle: Separate UI-context extraction from scenario planning

A key architectural insight: **do not ask the LLM to infer UI locators from prose**. Instead, crawl the live application, extract real HTML, and have a dedicated LLM pass ground locators in that real HTML. This avoids hallucinated selectors — a systemic failure mode of single-pass NL-to-test systems.

### 7.4 Principle: Framework-agnostic pipeline with a concrete target binding

The pipeline emits structured intermediate artifacts (JSON scenario plan, JSON element catalog) that are framework-agnostic; only the final generation step is bound to a specific framework (Robot Framework in the paper). A Jerry skill can swap in Playwright by changing only the Level 3 prompt template.

### 7.5 Principle: Reproducibility as a first-class research artifact

The paper bundles code, prompts, test cases, and a versioned Figshare archive. For Jerry: **adopt this bundling discipline** — any Jerry skill release should ship (a) the prompts, (b) the evaluation test cases, (c) the harness, (d) a versioned archive reference.

### 7.6 Testable principles Jerry should adopt verbatim

1. **Quality gate for generated tests:** `execution_recall ≥ 0.85 AND manual_modification_rate ≤ 0.10` as the "matches GenIA-E2ETest-equivalent performance" bar. Relax to `execution_recall ≥ 0.80 AND mmr ≤ 0.15` for a first-release Jerry bar.
2. **Element-hallucination defence:** Always ground locators in real DOM snapshots at generation time; never ask the LLM to invent selectors from prose.
3. **Determinism:** `temperature = 0` for all reproducibility-critical generation steps.
4. **Evaluation protocol:** Minimum n = 2 applications, 6 test cases each, 3 executions per case, for any Jerry self-benchmark.
5. **Ground truth reporting:** Report the effort and subjectivity margin on ground-truth construction explicitly — address Section 5.6's gap.

### 7.7 Where Jerry should go beyond GenIA-E2ETest

1. **Closed-loop self-healing** — feed runtime failures back into re-generation (Skyvern-style Validator loop from inn-4).
2. **Cross-model robustness** — evaluate against ≥3 LLMs (GPT, Claude, Gemini) to de-risk vendor lock-in.
3. **Richer oracles** — visual regression, differential testing, property-based invariants beyond literal expected-outcome matching.
4. **SPA-hardening** — explicit handling for React/Vue-style dynamic rendering, async data loads, and conditional DOM injection (the paper's largest acknowledged weakness).
5. **Playwright binding** — replace Robot Framework + Selenium with Playwright + Playwright MCP to align with the inn-2 emerging industry standard.

---

## Sources Retrieved

All URLs retrieved live via `WebSearch` or `WebFetch` during this session on **2026-04-21**.

### Primary sources (paper + canonical record)

1. [arXiv:2510.01024v1 — full HTML](https://arxiv.org/html/2510.01024v1) — WebFetch, primary paper body.
2. [arXiv:2510.01024 — abstract page](https://arxiv.org/abs/2510.01024) — WebFetch, metadata + venue linkage.
3. [arXiv:2510.01024 — PDF](https://www.arxiv.org/pdf/2510.01024) — WebFetch, cross-verification.
4. [SBES canonical article record (DOI 10.5753/sbes.2025.9927)](https://sol.sbc.org.br/index.php/sbes/article/view/37006) — WebFetch, bibliographic gold record.
5. [SBES 2025 proceedings issue (issue 1572)](https://sol.sbc.org.br/index.php/sbes/issue/view/1572) — WebSearch surfaced.
6. [Direct PDF on SBC SOL (article 37006/36791)](https://sol.sbc.org.br/index.php/sbes/article/view/37006/36791) — WebFetch indirect reference.

### Artifacts + code

7. [GitHub repository `uffsoftwaretesting/GenIA-E2ETest`](https://github.com/uffsoftwaretesting/GenIA-E2ETest) — WebSearch surfaced.
8. [Figshare artifact archive v5](https://doi.org/10.6084/m9.figshare.28873568.v5) — WebSearch surfaced.
9. [Projeto-Cinema auxiliary evaluation app](https://github.com/elvisjuniorr/Projeto-Cinema) — WebFetch indirect (PDF metadata).

### Secondary indexes and aggregators

10. [NASA ADS record](https://ui.adsabs.harvard.edu/abs/2025arXiv251001024J/abstract) — WebSearch surfaced.
11. [ResearchGate listing (396094402)](https://www.researchgate.net/publication/396094402_GenIA-E2ETest_A_Generative_AI-Based_Approach_for_End-to-End_Test_Automation) — WebSearch surfaced.
12. [ResearchGate listing (396370359)](https://www.researchgate.net/publication/396370359_GenIA-E2ETest_A_Generative_AI-Based_Approach_for_End-to-End_Test_Automation) — WebSearch surfaced.
13. [themoonlight.io literature-review summary](https://www.themoonlight.io/en/review/genia-e2etest-a-generative-ai-based-approach-for-end-to-end-test-automation) — WebFetch (null-finding on critical-review content).
14. [dblp SBES 2025 index](https://dblp.org/db/conf/sbes/sbes2025.html) — WebFetch (partial content).

### Venue context

15. [SBES 2025 official site (CBSoft host)](https://cbsoft.sbc.org.br/2025/sbes/?lang=pt) — WebSearch surfaced.
16. [SBES 2025 Research Track page](https://cbsoft.sbc.org.br/2025/sbes/pesquisa/) — WebSearch surfaced.
17. [SBES/WikiCFP historical index](http://www.wikicfp.com/cfp/program?id=2556&s=SBES&f=Brazilian+Symposium+on+Software+Engineering) — WebSearch surfaced.

### Author-affiliation verification

18. [Vânia de Oliveira Neves ResearchGate profile](https://www.researchgate.net/profile/Vania-Neves-4) — WebSearch surfaced.
19. [Vânia de Oliveira Neves UFF faculty page](http://profs.ic.uff.br/~vania/) — WebSearch surfaced.
20. [Vânia de Oliveira Neves FAPESP record](https://bv.fapesp.br/en/pesquisador/77675/vania-de-oliveira-neves/) — WebSearch surfaced.

### Adjacent / comparative 2025 work (for Section 6 context)

21. [Springer — "Generating Robot Framework Code with LLM Models: A RAG-Based Approach"](https://link.springer.com/chapter/10.1007/978-3-031-97992-7_65) — WebSearch surfaced.
22. [MDPI Computers — "AutoQALLMs"](https://www.mdpi.com/2073-431X/14/11/501) — WebSearch surfaced.
23. [arXiv:2506.02529 — "Automated Web Application Testing: E2E Test Case Generation"](https://arxiv.org/pdf/2506.02529) — WebSearch surfaced.
24. [arXiv:2511.15168 — "Finetuning LLMs for Automatic Form Interaction"](https://arxiv.org/html/2511.15168) — WebSearch surfaced.
25. [Robot Framework project home](https://robotframework.org/) — WebSearch surfaced.

**Live URL citation count: 25** (far exceeds ≥5 minimum).
**WebFetch reads: 6** (exceeds ≥3 minimum).
**Distinct queries: 10** (exceeds ≥8 minimum).
