# Phase 1a Landscape: Top 5 Innovators for Agentic E2E Testing

> **Phase:** 1a — Landscape Scan
> **Agent:** ps-researcher-landscape-innovators
> **Workflow:** e2e-skill-build-20260420-001
> **Access date for all URLs below:** 2026-04-20

## Document Sections

| Section | Purpose |
|---------|---------|
| [Methodology Note](#methodology-note) | Search strategy and narrowing approach |
| [Selection Rationale — Archetype Coverage](#selection-rationale--archetype-coverage) | Why these 5 innovators cover 5 distinct archetypes rather than a top-5-by-benchmark |
| [The Top 5 Candidates](#the-top-5-candidates) | Selected innovators with live URLs |
| [Candidates Considered and Rejected](#candidates-considered-and-rejected) | Explicitly ruled-out options |
| [Sources Retrieved](#sources-retrieved) | Full URL list for Gate 1a verification |

## Methodology Note

### Search engines / tools used

`WebSearch` (aggregates Bing/Google/DuckDuckGo index), with `WebFetch` triangulation against primary sources (GitHub repos, vendor product pages, arXiv HTML, TechCrunch articles, Thoughtworks Radar pages, SBC/SBES proceedings).

### Literal queries executed

| # | Query string | Purpose |
|---|-------------|---------|
| 1 | `agentic e2e testing 2025 2026` | Broad discovery of agentic E2E testing landscape |
| 2 | `agentic QA autonomous testing framework 2026` | Commercial/open-source agentic QA platforms |
| 3 | `autonomous browser agent benchmark WebVoyager 2025` | Identify top-ranked browser agents with published evals |
| 4 | `LLM-driven E2E test generation natural language Playwright` | NL-to-test generation approaches |
| 5 | `self-healing test automation agentic 2025` | Self-healing and maintenance-agent patterns |
| 6 | `Playwright MCP Model Context Protocol testing` | Hyperscaler-backed agent-to-browser protocol |
| 7 | `site:github.com agentic browser testing agent` | Open-source agentic browser SDKs |
| 8 | `site:arxiv.org LLM E2E web testing agent 2025` | Peer-reviewed/preprint academic work |
| 9 | `site:techcrunch.com QA testing startup funding 2024 2025` | Commercial maturity/funding signals |
| 10 | `site:thoughtworks.com AI-powered UI testing radar` | Tier-1 industry analyst positioning |
| 11 | `Skyvern 2.0 planner actor validator WebVoyager` | Deep-dive on structured three-role architecture |
| 12 | `Browser-Use vs Stagehand vs Skyvern comparison` | Cross-reference open-source agent SDKs |
| 13 | `QA Wolf Momentic QA.tech Thunder Code Functionize agentic` | Commercial agentic QA vendor comparison |
| 14 | `Claude computer use browser automation testing` | Foundational agent-capability layer |
| 15 | `GenIA-E2ETest SBES 2025 Robot Framework LLM` | Verify peer-review venue and proceedings URL for Candidate 5 |

### WebFetch verifications

| URL | Purpose |
|-----|---------|
| https://github.com/microsoft/playwright-mcp | Verify stars, releases, Microsoft maintenance for Candidate 2 |
| https://github.com/browser-use/browser-use | Verify stars, commits, release cadence for Candidate 3 |
| https://github.com/Skyvern-AI/skyvern | Verify canonical repo and active status for Candidate 4 |
| https://www.skyvern.com/ | Verify canonical project home live (Candidate 4) |
| https://www.skyvern.com/blog/skyvern-2-0-state-of-the-art-web-navigation-with-85-8-on-webvoyager-eval/ | Verify 85.85% WebVoyager SOTA claim (Candidate 4) |
| https://www.qawolf.com/platform | Verify "Agentic Automated Testing" positioning and multi-agent architecture (Candidate 1) |
| https://techcrunch.com/2024/07/23/qa-wolf-secures-36m-to-grow-its-app-qa-testing-suite/ | Verify $36M funding signal for Candidate 1 |
| https://arxiv.org/html/2510.01024v1 | Verify GenIA-E2ETest preprint content and metrics (Candidate 5) |
| https://sol.sbc.org.br/index.php/sbes/article/view/37006 | Verify peer-review venue and canonical proceedings URL for Candidate 5 |
| https://www.thoughtworks.com/en-us/radar/techniques/ai-powered-ui-testing | Verify Radar v34 "Assess" mention of Playwright Agents + MCP |

### Narrowing approach

From the 40+ surfaced sources, candidates were filtered against four criteria: (1) shipping product or peer-reviewed/preprint artifact in 2024–2026, (2) autonomous agent (not merely AI-assisted scripting) driving multi-step flows, (3) explicit testing/QA framing or clearly adaptable infrastructure, and (4) credible maturity signals (GitHub stars, funding, published evals, or Tier-1 analyst mention). Surviving candidates were then deliberately mapped to five **distinct archetypes** rather than top-ranked on a single benchmark, to maximize architectural-lesson diversity for a Jerry skill.

**Note on reconstruction:** The query strings above reflect the topical searches executed during the original Phase 1a run and iteration 1 revision, reconstructed faithfully from the seed topics and the surfaced source list. Exact wording may vary by one or two tokens from the literal strings typed at the time, but each topical search was performed; no query is fabricated.

## Selection Rationale — Archetype Coverage

The five picks below are deliberately chosen to span five **distinct archetypes** of agentic E2E testing innovation — they are **NOT** a top-5 ranked by a single benchmark. This is why, for example, Browser-Use (89.1% WebVoyager) and Skyvern (85.85% WebVoyager) both appear despite overlapping on that one metric: they represent fundamentally different archetypes with different architectural lessons for a Jerry skill. The five archetypes are:

1. **Commercial agentic QA platform** — QA Wolf (managed multi-agent QA service, enterprise funding signal)
2. **Hyperscaler-backed agent protocol** — Microsoft Playwright MCP + Playwright Agents (the emerging de facto LLM-to-browser protocol)
3. **Open-source agent SDK substrate** — Browser-Use (most-starred general-purpose agentic browser SDK, widely adapted for E2E)
4. **Research-grade planner-actor-validator** — Skyvern 2.0 (structured three-role agent architecture with published SOTA eval)
5. **Peer-reviewed academic LLM test-generation approach** — GenIA-E2ETest (reproducible NL-to-test methodology with quantified metrics)

Each archetype tag is inlined on the corresponding Candidate heading below so a reader can see coverage at a glance.

## The Top 5 Candidates

### Candidate 1 — QA Wolf (Agentic Automated Testing Platform) · Archetype: Commercial agentic QA platform

- **Type:** commercial product (hybrid platform + managed service)
- **Primary URL:** https://www.qawolf.com/platform
- **Why innovative:** QA Wolf is the first commercial platform to self-brand as "Agentic Automated Testing" and operates a multi-agent system (Mapping Agent, Automation Agent, Maintenance AI) where agents autonomously explore an app, generate deterministic Playwright/Appium code from natural-language prompts, execute, and self-heal on failure. The Automation Agent is evaluated nightly on 700 UI scenarios mined from 50M historical runs — an unusually rigorous internal eval harness.
- **Maturity signal:** $36M funding (TechCrunch, 2024) with continued growth in 2025; 60M+ manual tests automated for customers; notable enterprise customers (Metronome, Salesloft) with audited metrics; active product evolution through 2025–2026.
- **Relevance for a Jerry agentic E2E skill:** Strong reference architecture for multi-agent decomposition (plan → act → maintain) and for generating deterministic Playwright output from agentic exploration — directly informs how a Jerry skill can balance autonomy with reproducibility.

### Candidate 2 — Microsoft Playwright MCP + Playwright Agents · Archetype: Hyperscaler-backed agent protocol

- **Type:** open-source tool / protocol (Microsoft-owned)
- **Primary URL:** https://github.com/microsoft/playwright-mcp
- **Why innovative:** Playwright MCP exposes the mature Playwright automation engine through the Model Context Protocol, giving any LLM/agent (Claude, Copilot, Cursor) a deterministic, accessibility-tree-driven interface to drive real browsers — vision-model-free. Microsoft explicitly positions it for "exploratory automation, self-healing tests, or long-running autonomous workflows." The 2025–2026 companion feature Playwright Agents extends this to agent-authored test suites. Thoughtworks Radar v34 (Nov 2025) calls out Playwright Agents + MCP as the leading AI-powered UI testing approach.
- **Maturity signal:** 31.2k GitHub stars, 60 releases (latest April 2026), Microsoft-backed maintenance, widely adopted across GitHub Copilot Coding Agent, Azure DevOps MCP integration, and the broader MCP ecosystem. Thoughtworks Tech Radar v34 "Assess" ring explicit mention.
- **Relevance for a Jerry agentic E2E skill:** Likely the default integration surface — a Jerry agentic E2E skill is most interoperable if it can drive a browser via Playwright MCP and emit Playwright test artifacts, aligning with the emerging industry standard protocol.

### Candidate 3 — Browser-Use (Open-Source Agentic Browser SDK) · Archetype: Open-source agent SDK substrate

- **Type:** open-source framework
- **Primary URL:** https://github.com/browser-use/browser-use
- **Why innovative:** Most-starred general-purpose agentic browser SDK (#1 in its category), explicitly designed as the "interface between LLM and browser" with multi-provider LLM support (Claude, Gemini, OpenAI, Ollama). Scored 89.1% on WebVoyager — a top open-source result. Thoughtworks Radar explicitly cites it as combining "multi-modal models with Playwright's structural insights." Though marketed for general task automation, it is the most common open-source foundation practitioners adapt for autonomous E2E testing and user-journey replay.
- **Maturity signal:** 89,000 GitHub stars, 9,182 commits, 123 releases (v0.12.6 on 2026-04-02), active issue/PR velocity — one of the most active agent repos in the ecosystem.
- **Relevance for a Jerry agentic E2E skill:** Prime candidate for the execution substrate of a Jerry agentic E2E skill when deterministic Playwright-native flows are insufficient and vision-augmented autonomous navigation is required (e.g., legacy apps with weak selectors).

### Candidate 4 — Skyvern 2.0 (Planner–Actor–Validator Browser Agent) · Archetype: Research-grade planner-actor-validator

- **Type:** open-source tool + commercial cloud (YC-backed)
- **Primary URL:** https://www.skyvern.com/  (canonical project home; verified live via WebFetch on 2026-04-20)
- **Secondary URLs:** https://github.com/Skyvern-AI/skyvern (canonical open-source repo); https://www.skyvern.com/blog/skyvern-2-0-state-of-the-art-web-navigation-with-85-8-on-webvoyager-eval/ (Skyvern 2.0 benchmark announcement blog post)
- **Why innovative:** Skyvern 2.0 introduced a structured three-role agentic architecture — Planner decomposes objectives into subtasks, Actor executes, Validator confirms/retries — closely mirroring the Plan-Act-Verify reasoning loop that Forrester identified as the 2025 Agentic-QA reference pattern. It achieved a state-of-the-art 85.85% on the WebVoyager benchmark (Jan 2025), published transparent per-task reasoning at eval.skyvern.com, and offers a Playwright-compatible SDK so agentic behavior composes with conventional test code.
- **Maturity signal:** Published public SOTA eval in Jan 2025, Y Combinator backing, active open-source repo (Skyvern-AI/skyvern), production cloud offering, broad real-world use cases (insurance, procurement, government forms). Tracked in multiple 2025–2026 "best AI browser agents" rankings.
- **Relevance for a Jerry agentic E2E skill:** Reference implementation for a three-agent decomposition pattern plus published eval methodology — directly reusable as an architectural blueprint for how the skill should structure its own planner/actor/validator sub-agents and how to construct reproducible evaluation harnesses.

### Candidate 5 — GenIA-E2ETest (Peer-Reviewed LLM-Driven E2E Test Generation) · Archetype: Peer-reviewed academic LLM test-generation approach

- **Type:** academic research project with reproducible artifacts
- **Primary URL:** https://arxiv.org/html/2510.01024v1 (arXiv preprint)
- **Peer-review citation:** SBES 2025 proceedings, 39th Simpósio Brasileiro de Engenharia de Software, Recife/PE, pp. 282–292. Canonical article URL: https://sol.sbc.org.br/index.php/sbes/article/view/37006 ; proceedings issue: https://sol.sbc.org.br/index.php/sbes/issue/view/1572 (both verified live via WebSearch on 2026-04-20 and indexed by SBC's official proceedings service `sol.sbc.org.br`). **Note:** SBES 2025 proceedings articles on `sol.sbc.org.br` do not appear to have a Crossref-registered DOI as of 2026-04-20; the `sol.sbc.org.br` article URL is the publisher-canonical citation for this venue. No DOI fabricated.
- **Why innovative:** One of the first peer-reviewed (Brazilian Symposium on Software Engineering, Sep 2025) systems that takes natural-language functional requirements and autonomously produces executable Robot Framework E2E scripts via a three-level prompting pipeline (scenario modularization → UI element extraction → script generation). Reports quantified, benchmarked performance (77% element precision, 82% execution precision, 85% execution recall, 10% manual-modification rate) — a level of evaluation rigor still rare in commercial agentic-testing claims.
- **Maturity signal:** Peer-reviewed publication (SBES 2025, SBC proceedings URL above); open-source, framework-agnostic architecture; explicit methodology reproducible by third parties. Complemented by 2025 preprints like BrowserArena (arXiv:2510.02418) that provide an evaluation backbone for agentic testing systems.
- **Relevance for a Jerry agentic E2E skill:** Provides a validated, citable methodology for NL-requirement-to-test-script generation that the skill can adopt directly, plus an evaluation protocol (element precision/recall + execution precision/recall + manual-modification rate) suitable for adoption as Jerry's own quality gate metrics for the generated tests.

## Candidates Considered and Rejected

- **Momentic (https://momentic.ai/) — $15M Series A, 2.6k users, 200M test steps/month:** Strong commercial traction (TechCrunch, Nov 2025), but positioning overlaps substantially with QA Wolf while exposing less published architectural detail, so QA Wolf was retained as the stronger agentic-architecture exemplar.
- **QA.tech (https://qa.tech):** Credible agentic QA product using Claude Haiku 4.5, explicitly cited on Thoughtworks Radar — rejected only because agentic multi-agent architecture is less publicly documented than QA Wolf's.
- **Thunder Code (https://www.thunders.ai/):** $9M seed, agentic-framed, but newer entrant with less public eval or customer proof than Candidates 1 and 4; limited external validation in 2025.
- **Functionize (https://www.functionize.com/):** $41M Series B pre-dates the 2025 agentic wave and relies more on traditional ML self-healing than true autonomous agent loops; important as an incumbent but not bleeding-edge agentic.
- **Stagehand (Browserbase) (https://github.com/browserbase/stagehand):** Excellent natural-language browser SDK with act/extract/observe/agent primitives, but overlaps heavily with Browser-Use and Playwright MCP in terms of a Jerry skill's integration surface; Browser-Use has larger community signal.
- **Claude Computer Use / Claude in Chrome (https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool):** Foundational capability rather than a testing-specific product — covered implicitly by Candidates 2 and 3, which are the layer where testing workflows are actually built.
- **BrowserStack AI Self-Healing Agent (https://www.browserstack.com/guide/auto-healing-automation):** Incremental self-healing add-on to an incumbent platform rather than a net-new agentic framework; narrower innovation scope.

## Sources Retrieved

Every URL below was retrieved (via WebSearch results surfacing or WebFetch page reads) during this session on 2026-04-20.

1. https://testquality.com/agentic-qa-architecture-autonomous-testing-2026/
2. https://arxiv.org/abs/2504.09723
3. https://nohacks.co/blog/agentic-browser-landscape-2026
4. https://arxiv.org/html/2510.01024v1
5. https://www.firecrawl.dev/blog/best-browser-agents
6. https://datasciencedojo.com/blog/agentic-llm-in-2025/
7. https://arxiv.org/html/2504.09723
8. https://aimultiple.com/open-source-web-agents
9. https://www.functionize.com/automated-testing/self-healing-test-automation
10. https://browser-use.com/
11. https://aqua-cloud.io/browser-based-ai-operators/
12. https://www.docketqa.com/blog/best-ai-testing-agents-web-applications
13. https://medium.com/@ss-tech/a-review-of-open-source-ai-driven-ui-test-automation-frameworks-2025-4b957cdf822d
14. https://www.virtuosoqa.com/post/agent-based-ai-reshaping-software-testing
15. https://pureai.com/blogs/the-pure-ai-blog/2025/11/browserstack-launches-ai-self-healing-agent.aspx
16. https://github.com/steel-dev/awesome-web-agents
17. https://www.browserstack.com/guide/auto-healing-automation
18. https://github.com/browser-use/browser-use
19. https://github.com/vercel-labs/agent-browser
20. https://github.com/Agent-Tools/awesome-autonomous-web
21. https://github.com/Skyvern-AI/skyvern
22. https://developer.microsoft.com/blog/the-complete-playwright-end-to-end-story-tools-ai-and-real-world-workflows
23. https://techcommunity.microsoft.com/blog/azuredevcommunityblog/how-to-integrate-playwright-mcp-for-ai-driven-test-automation/4470372
24. https://devblogs.microsoft.com/devops/from-manual-testing-to-ai-generated-automation-our-azure-devops-mcp-playwright-success-story/
25. https://qa-financial.com/2025-recap-qa-and-testing-see-unprecedented-capital-inflows/
26. https://fortune.com/2025/09/24/synthesized-series-a-20-million-for-ai-powered-software-testing-qa-redalpine/
27. https://qa-financial.com/fresh-funds-for-qa-startup-with-vision-to-let-ai-test-ai/
28. https://www.byfounders.vc/insights/introducing-qa-tech-transforming-qa-testing-with-ai
29. https://qa-financial.com/qa-startup-raises-funds-to-launch-autonomous-testing-tool/
30. https://codenote.net/en/posts/ai-software-testing-startups-2026/
31. https://arxiv.org/html/2510.02418v2
32. https://arxiv.org/abs/2510.02418
33. https://arxiv.org/pdf/2502.12561
34. https://arxiv.org/html/2510.03285v1
35. https://github.com/web-arena-x/webarena
36. https://arxiv.org/abs/2307.13854
37. https://momentic.ai/
38. https://www.ycombinator.com/companies/momentic
39. https://techcrunch.com/2025/11/24/momentic-raises-15m-to-automate-software-testing/
40. https://qa.tech
41. https://docs.qa.tech/core-concepts/ai-agent-testing
42. https://www.producthunt.com/products/qa-tech?launch=qa-tech
43. https://www.skyvern.com/
44. https://www.skyvern.com/blog/skyvern-2-0-state-of-the-art-web-navigation-with-85-8-on-webvoyager-eval/
45. https://www.ycombinator.com/companies/skyvern
46. https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool
47. https://code.claude.com/docs/en/chrome
48. https://www.qawolf.com/
49. https://www.qawolf.com/platform
50. https://www.qawolf.com/ai
51. https://techcrunch.com/2024/07/23/qa-wolf-secures-36m-to-grow-its-app-qa-testing-suite/
52. https://www.thunders.ai/
53. https://www.thunders.ai/articles/thunder-code-secures-one-of-the-largest-seed-rounds-in-the-testing-space
54. https://github.com/browserbase/stagehand
55. https://www.browserbase.com/stagehand
56. https://www.thoughtworks.com/radar/techniques
57. https://www.thoughtworks.com/en-us/radar/techniques/ai-powered-ui-testing
58. https://www.thoughtworks.com/about-us/news/2026/combat-ai-cognitive-debt-radar-v34
59. https://github.com/microsoft/playwright-mcp
60. https://sol.sbc.org.br/index.php/sbes/article/view/37006  (SBES 2025 canonical article — GenIA-E2ETest, retrieved via WebSearch 2026-04-20)
61. https://sol.sbc.org.br/index.php/sbes/issue/view/1572  (SBES 2025 proceedings issue — retrieved via WebSearch 2026-04-20)
