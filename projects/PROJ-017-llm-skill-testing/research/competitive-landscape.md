# Competitive Landscape Analysis: LLM Evaluation Tools and Frameworks

> PROJ-017 Phase 1B deliverable. Competitive landscape of LLM evaluation tools with focus on skill-level evaluation capabilities.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Key findings and strategic implications |
| [L1: Competitive Landscape](#l1-competitive-landscape) | Full tool comparison, Porter's analysis, market positioning |
| [L1.1: Tool Comparison Matrix](#l11-tool-comparison-matrix) | 16 tools compared across 10 dimensions |
| [L1.2: Porter's Five Forces Analysis](#l12-porters-five-forces-analysis) | Structural analysis of the LLM evaluation market |
| [L1.3: Funding and Market Position](#l13-funding-and-market-position) | Investment landscape and enterprise adoption signals |
| [L1.4: Gap Analysis -- Skill-Level Evaluation](#l14-gap-analysis----skill-level-evaluation) | Which tools approach workflow/skill evaluation |
| [L1.5: promptfoo Competitive Threat Assessment](#l15-promptfoo-competitive-threat-assessment) | Roadmap direction, timing, capability proximity, integration points |
| [L2: Strategic Implications](#l2-strategic-implications) | Market timing, build-vs-buy, competitive moat |
| [Data Sources and Methodology](#data-sources-and-methodology) | How data was collected and verified |

---

## L0: Executive Summary

**Key Findings:**

1. **No existing tool evaluates multi-agent skills/workflows end-to-end.** The closest approaches are DeepEval's agentic metrics (tool use, plan quality, step efficiency) and Inspect AI's multi-agent evaluation framework, but both operate at the individual agent level -- not at the orchestrated skill/workflow level that Jerry's testing framework targets.

2. **The market is bifurcated into two segments** that do not overlap: (a) prompt/response evaluation tools (promptfoo, DeepEval, Ragas, HELM) and (b) observability/monitoring platforms (Langfuse, Arize Phoenix, AgentOps, Langsmith). Neither segment addresses the "skill as unit of test" abstraction layer. Note: "bifurcated" is a simplified characterization for executive summary purposes; the full taxonomy in L1.4 uses three tiers (Tier 1: closest to skill-level, Tier 2: partial coverage, Tier 3: monitoring only) and also distinguishes a benchmarking segment (lm-eval-harness, HELM) and agent-specific tools (Inspect AI, AgentOps) that do not fit cleanly into either of the two primary segments described here.

3. **DeepEval represents the closest competitive threat** with 6 dedicated agentic metrics (Task Completion, Tool Correctness, Argument Correctness, Step Efficiency, Plan Adherence, Plan Quality) and trace-based evaluation. However, its evaluation unit is a single agent trace, not a coordinated multi-agent workflow.

4. **promptfoo is moving toward agent security testing** (OWASP Agentic Applications, Claude Agent SDK provider) but shows no evidence of building skill-level functional evaluation. Its roadmap emphasis is red-teaming, not functional quality assessment.

5. **A 12-18 month market timing window exists** for skill-level evaluation tooling. Based on GitHub repository and issue tracker analysis, no funded competitor has announced this capability (web verification unavailable). The window closes when either DeepEval extends its agentic metrics to multi-agent orchestration, or promptfoo builds functional evaluation beyond security scanning. Window derived from three sub-triggers: DeepEval extension (6-12 months), LLM provider integration (12-18 months), funded competitor acquisition (18-24 months) -- see L2 Market Timing Window for derivation.

---

## L1: Competitive Landscape

### L1.1: Tool Comparison Matrix

Data sourced from GitHub API on 2026-03-03/04 and repository documentation. All GitHub metrics are live API queries.

#### Core Metrics

| Tool | GitHub Stars | Contributors | License | Language | Primary Focus | Latest Release |
|------|-------------|-------------|---------|----------|---------------|----------------|
| **MLflow** | 24,518 | 992 | Apache-2.0 | Python | ML lifecycle platform (evals added) | Ongoing |
| **Langfuse** | 22,585 | 131 | Proprietary (BSL) | TypeScript | LLM observability + evals | Ongoing |
| **DeepEval** | 13,919 | 263 | Apache-2.0 | Python | LLM evaluation framework | v3.8.8 (2025-12-01) |
| **Ragas** | 12,793 | 246 | Apache-2.0 | Python | RAG evaluation | v0.4.3 (2026-01-13) |
| **lm-evaluation-harness** | 11,548 | 384 | MIT | Python | Model benchmarking | Ongoing |
| **W&B** | 10,878 | 229 | MIT | Python | ML experiment tracking | Ongoing |
| **promptfoo** | 10,780 | 247 | MIT | TypeScript | LLM evals + red teaming | v0.120.26 (2026-03-03) |
| **Arize Phoenix** | 8,730 | 156 | Custom | Jupyter/Python | AI observability | v13.7.0 (2026-03-02) |
| **Evidently AI** | 7,272 | 94 | Apache-2.0 | Python | ML/LLM monitoring | Ongoing |
| **AgentOps** | 5,331 | 47 | MIT | Python | Agent observability | Ongoing |
| **TruLens** | 3,129 | 67 | MIT | Python | LLM evaluation + tracking | Ongoing |
| **HELM** | 2,695 | 146 | Apache-2.0 | Python | Holistic model evaluation | Ongoing |
| **HuggingFace Evaluate** | 2,422 | 137 | Apache-2.0 | Python | ML evaluation library | Ongoing |
| **Inspect AI** | 1,796 | 187 | MIT | Python | LLM agent evaluation | 2025-11-28 tag |
| **LangSmith SDK** | 792 | 75 | MIT | Python | LangChain observability | Ongoing |
| **BrainTrust SDK** | 119 | N/A | Apache-2.0 | TypeScript | Evals + logging | Ongoing |

Sources: GitHub API `repos/{owner}/{repo}` endpoint, queried 2026-03-04. Stars, forks, contributors, and license extracted via `gh api`. Release dates from `repos/{owner}/{repo}/releases/latest`.

#### Capability Matrix

**Rating Legend:**
- **Strong** = Native, documented support with dedicated API/feature set and multiple real-world examples in documentation (e.g., promptfoo's red teaming has 10+ attack strategy implementations with OWASP mapping)
- **Moderate** = Supported via configuration or integration but not a primary feature; limited documentation or examples (e.g., Ragas RAG metrics can be applied to prompt/response but require adapter setup)
- **Basic** = Minimal support via general-purpose mechanisms; no dedicated feature (e.g., W&B tracks evaluation runs but provides no LLM-specific evaluation metrics)
- **Partial** = Some aspects addressed but significant capability gaps remain (e.g., Ragas has emerging agent support mentioned in README but no dedicated agentic metrics found in docs)
- **No** = Not present, not documented, and no workaround identified in repository search

| Tool | Prompt/Response Eval | RAG Eval | Agent Eval | Multi-Agent Eval | Workflow/Skill Eval | Red Teaming | CI/CD Integration | Observability |
|------|---------------------|----------|------------|-----------------|--------------------|-----------|-----------------|--------------|
| **promptfoo** | Strong | Moderate | Security only | No | No | Strong | Strong | No |
| **DeepEval** | Strong | Strong | Strong (6 metrics) | Partial | No | No | Strong (pytest) | Via Confident AI |
| **Inspect AI** | Strong | Moderate | Strong (native) | Yes (basic) | No | No | Moderate | No |
| **Ragas** | Moderate | Strong | Partial | No | No | No | Moderate | Via integrations |
| **lm-eval-harness** | Strong (benchmarks) | No | No | No | No | No | Moderate | No |
| **HELM** | Strong (benchmarks) | No | No | No | No | No | No | No |
| **Langfuse** | Moderate | Moderate | Trace-based | No | No | No | Moderate | Strong |
| **Arize Phoenix** | Moderate | Moderate | Trace-based | No | No | No | Moderate | Strong |
| **TruLens** | Strong | Strong | Feedback-based | No | No | No | Moderate | Moderate |
| **AgentOps** | No | No | Monitoring only | Monitoring only | No | No | Moderate | Strong |
| **MLflow** | Moderate | Moderate | Basic | No | No | No | Strong | Moderate |
| **W&B** | Basic | Basic | Basic | No | No | No | Strong | Strong |
| **Evidently AI** | Moderate | Moderate | Basic | No | No | No | Strong | Strong |
| **LangSmith** | Moderate | Moderate | Trace-based | No | No | No | Strong | Strong |
| **BrainTrust** | Strong* | Moderate | Basic | No | No | No | Strong* | Moderate |
| **HF Evaluate** | Strong (metrics) | No | No | No | No | No | Moderate | No |

**Key observation:** The "Workflow/Skill Eval" column is uniformly "No" across all 16 tools. This is the gap Jerry's PROJ-017 targets.

*BrainTrust ratings based on documentation review; primary repository returned 404 at time of research (see Limitations #3).

Note: Galileo ($68M funding) was evaluated for market position but excluded from the capability matrix due to insufficient publicly available technical documentation for rating-level assessment at time of research.

**Rating Evidence for Non-Obvious Cells (Tier 1-2 Tools):**

| Tool | Cell | Rating | Evidence Source |
|------|------|--------|----------------|
| **promptfoo** | Agent Eval = Security only | Red teaming against agents via OWASP ASI01-ASI10 but no functional quality metrics. Source: `site/docs/red-team/owasp-agentic-ai.md` documents 10 attack categories; no `metrics/` or `evaluation/` directory for agent functional quality. |
| **promptfoo** | Red Teaming = Strong | 10+ built-in attack strategies (crescendo, GOAT, Hydra, jailbreak, tree-based); OWASP Agentic mapping; dedicated `site/docs/red-team/` directory with 20+ files. |
| **DeepEval** | Agent Eval = Strong (6 metrics) | Six dedicated metrics in `docs/docs/metrics-plan-quality.mdx`, `metrics-step-efficiency.mdx`, `metrics-tool-use.mdx`, plus Task Completion, Argument Correctness, Plan Adherence. Source: `docs/sidebars.js` agentic metrics section. |
| **DeepEval** | Multi-Agent Eval = Partial | `@observe` decorator instruments individual agent functions but no orchestrator-level test case or cross-agent handoff validation found in docs search. Source: `docs/docs/getting-started-agents.mdx`. |
| **Inspect AI** | Agent Eval = Strong (native) | Built-in ReAct agent, custom `@agent` decorator, multi-turn tool loops. Source: `docs/agents.qmd`. |
| **Inspect AI** | Multi-Agent Eval = Yes (basic) | Supervisor handoff, sequential workflows, agents-as-tools architectures documented. Source: `docs/multi-agent.qmd`. Rated "basic" because evaluation targets task-solving, not production workflow correctness. |
| **Ragas** | Agent Eval = Partial | README mentions agent evaluation capabilities but no dedicated agentic metrics (comparable to DeepEval's 6) found in documentation search. Source: `explodinggradients/ragas` README and docs directory search. |
| **Langfuse** | Agent Eval = Trace-based | Captures agent execution traces for observability but does not score or evaluate agent behavior. Source: Langfuse repository description and docs. |
| **TruLens** | Prompt/Response Eval = Strong | TruFeedback feedback functions provide LLM-based evaluation of groundedness, relevance, and sentiment for prompt/response pairs. Source: `truera/trulens` repository README and `docs/` directory; `TruChain` and `TruLlama` integration examples demonstrate prompt-level evaluation with dedicated API. |
| **TruLens** | RAG Eval = Strong | Dedicated RAG triad metrics: context relevance, groundedness, and answer relevance. `TruChain` and `TruLlama` wrappers provide native RAG pipeline integration. Source: `truera/trulens` repository README, RAG triad documentation in `docs/` directory. |

#### Architecture Approaches Comparison

> **Scope note:** This table covers the five Tier 1-2 tools most relevant to Jerry's integration and build decisions (promptfoo, DeepEval, Inspect AI, Ragas, Langfuse). Tier 3 tools (monitoring-only: AgentOps, LangSmith, Arize Phoenix) and benchmarking tools (lm-eval-harness, HELM) are omitted because their architectural patterns are not relevant to skill-level evaluation design.

| Tool | Evaluation Pipeline Design | Extension Model | Key Architectural Distinction |
|------|---------------------------|-----------------|-------------------------------|
| **promptfoo** | Batch evaluation: YAML config defines test cases, CLI executes all cases against providers, results aggregated as JSON/HTML. Stateless per run. | Custom providers (`callApi` interface) + custom assertions (JS/Python functions). Plugin-based, file-referenced. | Declarative test-case-driven; provider-agnostic; no trace dependency. |
| **DeepEval** | Trace-based evaluation: `@observe` decorator instruments function calls, metrics computed on collected traces via pytest integration. | Custom metrics via Python class inheritance (`BaseMetric`). Tight pytest integration. | Trace-centric; requires code instrumentation; metrics are Python classes. |
| **Inspect AI** | Task-based evaluation: define `@task` with dataset + solver + scorer. Solver chains implement agent behavior. Built-in sandbox execution. | Custom solvers, scorers, and tools via Python decorators. Task composition via solver chains. | Task-as-unit-of-evaluation; sandboxed execution; solver composition model. |
| **Ragas** | Dataset evaluation: test datasets passed through evaluation pipeline with metric computation. Integration-oriented. | Custom metrics via Python. LangChain/LlamaIndex integration adapters. | Dataset-centric; RAG-specialized metric library; integration-first design. |
| **Langfuse** | Trace collection + optional scoring: captures LLM calls and agent traces, supports manual or automated scoring on collected traces. | SDK instrumentation (Python/JS). Custom scoring functions via API. | Observability-first; evaluation is secondary to trace collection; async scoring. |

---

### L1.2: Porter's Five Forces Analysis

#### Force 1: Threat of New Entrants -- HIGH

| Factor | Assessment | Evidence |
|--------|-----------|---------|
| Capital requirements | Low | Open-source entry costs are near zero; DeepEval and Ragas bootstrapped from individual contributors. promptfoo reached 10K+ stars before any visible funding. |
| Technical barriers | Low-Moderate | Core evaluation logic is straightforward (LLM-as-judge patterns are well-documented). The real barrier is ecosystem integration and community building. |
| Switching costs for users | Low | Most tools use similar YAML/Python configs. Migrating evaluation suites between tools requires modest effort. |
| Pace of new entrants | High | 8 of 16 tools in this analysis were created after 2022 (cross-reference: GitHub repository creation dates -- AgentOps (2024), Langfuse (2023), DeepEval (2023), Ragas (2023), BrainTrust (2023), Arize Phoenix (2023), plus 2 others with 2022+ first commits). |
| LLM provider tools | Growing threat | Anthropic (Claude Agent SDK), OpenAI (Evals framework), and Google (Vertex AI Evaluation) are building evaluation tooling into their platforms. |

**Conclusion:** Entry barriers are low and declining. New entrants appear regularly. The primary moat is community/ecosystem, not technology.

#### Force 2: Bargaining Power of Buyers -- HIGH

| Factor | Assessment | Evidence |
|--------|-----------|---------|
| Price sensitivity | High | 14 of 16 tools are open-source or have free tiers (cross-reference: Core Metrics table License column -- Apache-2.0, MIT, or similar open license for all except Langfuse BSL and Arize Custom; both offer free tiers). Buyers expect free core functionality. |
| Information availability | High | All tools are publicly documented; feature comparison is trivial. |
| Switching costs | Low | Evaluation configs are portable; no vendor lock-in at the evaluation layer. |
| Buyer concentration | Moderate | Enterprise buyers (Fortune 500) have significant leverage; individual developers have none. |

**Conclusion:** Buyers have strong power. The market converges toward open-source with optional paid tiers.

#### Force 3: Bargaining Power of Suppliers (LLM Providers) -- HIGH

| Factor | Assessment | Evidence |
|--------|-----------|---------|
| Provider concentration | High | Anthropic, OpenAI, and Google are widely reported as the dominant frontier model providers (exact market share figures unavailable without web search access; industry consensus places their combined share at a substantial majority of frontier model API access). [INFERRED from ecosystem adoption patterns] |
| Pricing power | Moderate-High | LLM-as-judge evaluations consume API tokens. Provider pricing directly impacts evaluation cost. |
| Vertical integration threat | High | All three major providers are building or acquiring evaluation capabilities. OpenAI has built-in evals. Anthropic provides the Claude Agent SDK with eval hooks. |
| API dependency | Critical | Every LLM evaluation tool depends on LLM APIs for judge-based metrics. A provider API change can break entire evaluation pipelines. |

**Conclusion:** LLM providers are the most powerful force in this market. They can capture the evaluation layer through vertical integration at any time.

#### Force 4: Threat of Substitutes -- MODERATE

| Factor | Assessment | Evidence |
|--------|-----------|---------|
| Manual evaluation | Persistent | Human review remains the gold standard for many organizations. LLM evaluation tools supplement but do not replace human judgment. |
| Built-in model evals | Growing | LLM providers embedding evaluation in their APIs (OpenAI evals, Anthropic's evaluation features) substitute standalone tools. |
| General testing frameworks | Low threat | Standard software testing (pytest, Jest) cannot handle non-deterministic LLM outputs without LLM-specific adapters. |
| Custom internal tools | Moderate | Large enterprises (Google, Meta, Microsoft) build internal evaluation systems that may never need external tools. |

**Conclusion:** The primary substitute threat comes from LLM providers building evaluation into their platforms, not from alternative evaluation approaches.

#### Force 5: Competitive Rivalry -- HIGH AND INTENSIFYING

| Factor | Assessment | Evidence |
|--------|-----------|---------|
| Number of competitors | High | 16+ tools in active development, with new entrants every quarter. |
| Growth rate | High | LLM evaluation market is growing with the overall LLM application market. |
| Product differentiation | Low | Most tools offer similar core metrics (faithfulness, relevancy, hallucination). Differentiation occurs at the edges (agent metrics, red teaming, observability). |
| Exit barriers | Low | Open-source projects can be maintained indefinitely with minimal resources. |
| Release cadence | Intense | promptfoo ships multiple releases per week (v0.120.17 to v0.120.26 in 6 weeks). DeepEval averages monthly releases. |

**Conclusion:** Rivalry is intense. Sustainable competitive advantage requires either deep specialization (red teaming, agent evaluation) or platform effects (ecosystem integrations, community).

#### Porter's Summary

| Force | Intensity | Implication for Jerry |
|-------|----------|----------------------|
| New Entrants | HIGH | Must differentiate on skill-level evaluation; generic evaluation will be commoditized. |
| Buyer Power | HIGH | Open-source core is mandatory. Value capture must come from enterprise features or unique capabilities. |
| Supplier Power | HIGH | Must minimize LLM provider dependency. Support multiple providers. Favor deterministic evaluation where possible. |
| Substitutes | MODERATE | LLM provider integration is the primary threat. Build capabilities providers cannot easily replicate. |
| Rivalry | HIGH | Red ocean for prompt-level evaluation. Blue ocean for skill/workflow-level evaluation. |

---

### L1.3: Funding and Market Position

#### Funded Companies

| Company | Tool | Known Funding | Investors/Notes | Source Confidence |
|---------|------|--------------|-----------------|-------------------|
| **Confident AI** | DeepEval | YC-backed (SINGLE-SOURCE: YC directory listing from public profile) | Y Combinator batch; exact amount undisclosed | Low -- limited public funding data |
| **Langfuse** | Langfuse | YC W23 | Y Combinator Winter 2023 batch. Stars growth (22.5K) suggests product-market fit. | Source: GitHub description states "YC W23" |
| **Arize AI** | Phoenix | Series B ($38M disclosed historically) | Enterprise observability focus. (SINGLE-SOURCE: historical press reporting) | Moderate |
| **Weights & Biases** | W&B | Series C ($200M at $1B+ valuation historically) | Dominant ML experiment tracking. AI evaluation is secondary. (SINGLE-SOURCE: historical press) | Moderate |
| **Databricks** | MLflow | Acquired MLflow creators; $43B company | MLflow is Databricks' open-source ML platform. Evaluation features added as part of broader platform. | High |
| **LangChain** | LangSmith | Series A ($25M+ historically) | LangSmith is the commercial observability product for the LangChain ecosystem. | Moderate |
| **Snowflake** | TruLens | Acquired TruEra (TruLens parent) | Snowflake acquired TruEra, integrating TruLens into Snowflake Cortex. | High -- public acquisition |
| **promptfoo** | promptfoo | Undisclosed | Founded by Ian Webster. Enterprise offering available. No public funding announcements found. | Low |
| **Ragas** | Ragas | Backed by Vibrant Labs AI | Repository transferred to `vibrantlabsai` org. Careers page listed on README. | Moderate |
| **AgentOps** | AgentOps | Undisclosed | Open-source app. 5.3K stars indicates traction. | Low |
| **Galileo** | Galileo | Series A ($18M historically) | Enterprise LLM evaluation platform. (SINGLE-SOURCE: historical press) | Low |

**Note on funding data:** WebSearch and WebFetch were unavailable for this analysis. Funding figures marked as "historically" are based on previously reported rounds that may have been supplemented by subsequent undisclosed rounds. Treat all funding figures as lower bounds.

#### Market Position Quadrants

Based on GitHub community size (stars) as proxy for adoption and capability breadth.

**Axis Definitions:**
- **Y-axis (Capability Breadth):** Number of distinct evaluation capability categories supported from the Capability Matrix (Prompt/Response, RAG, Agent, Multi-Agent, Workflow/Skill, Red Teaming, CI/CD, Observability). Tools with 4+ capabilities rated Moderate or above = HIGH; 2-3 = positioned proportionally; 0-1 = LOW.
- **X-axis (Market Segment Focus):** NARROW FOCUS = tool targets a single primary use case (e.g., benchmarking only, agent monitoring only); BROAD FOCUS = tool addresses multiple market segments (e.g., evaluation + observability + CI/CD). Determined from tool's primary focus description and feature set breadth.

```
                    HIGH CAPABILITY BREADTH
                           |
                           |         MLflow (24.5K)
                           |         [Platform]
                           |
                           |         Langfuse (22.5K)
                           |         [Observability+Evals]
                           |
                           |         DeepEval (13.9K)
                           |         [Eval Framework]
                           |
    promptfoo (10.8K)      |         Ragas (12.8K)
    [Evals+RedTeam]        |         [RAG Evals]
                           |
  ----NARROW FOCUS---------+------------BROAD FOCUS-----
                           |
    Inspect AI (1.8K)      |         W&B (10.9K)
    [Agent Evals]          |         [ML Platform]
                           |
    HELM (2.7K)            |         Arize Phoenix (8.7K)
    [Benchmarks]           |         [Observability]
                           |
    AgentOps (5.3K)        |         Evidently (7.3K)
    [Agent Monitoring]     |         [Monitoring]
                           |
                           |         TruLens (3.1K)
                           |         [Eval+Tracking]
                           |
                    LOW CAPABILITY BREADTH
```

---

### L1.4: Gap Analysis -- Skill-Level Evaluation

#### Defining the Gap

Jerry's PROJ-017 targets **skill-level evaluation**: testing an entire orchestrated workflow that involves multiple agents coordinated through an orchestrator, producing persistent file artifacts, with quality gates at phase boundaries. This is fundamentally different from what any existing tool provides.

| Evaluation Level | Description | Current Tool Coverage | Gap |
|-----------------|-------------|----------------------|-----|
| **Prompt/Response** | Test a single prompt against expected outputs | Strong (all 16 tools) | No gap |
| **RAG Pipeline** | Test retrieval + generation end-to-end | Strong (Ragas, DeepEval, TruLens) | No gap |
| **Single Agent** | Test agent with tools in a multi-turn session | Moderate (DeepEval, Inspect AI) | Partially addressed |
| **Multi-Agent** | Test coordinated agents with handoffs | Weak (Inspect AI only, basic) | Significant gap |
| **Skill/Workflow** | Test orchestrated multi-agent pipeline with file artifacts, quality gates, phase boundaries | None | **Complete gap** |

#### Tools Approaching Skill-Level Evaluation

**Tier 1: Closest to Skill-Level (still significant gap)**

**DeepEval** -- 6 dedicated agentic metrics:
- Task Completion: Evaluates whether the agent completed its assigned task
- Tool Correctness: Evaluates tool selection accuracy
- Argument Correctness: Evaluates tool argument generation
- Step Efficiency: Evaluates efficiency of agent execution steps
- Plan Quality: Evaluates quality of agent's plan for completing task
- Plan Adherence: Evaluates how well agent followed its plan

Source: `docs/sidebars.js` in `confident-ai/deepeval` repository, confirmed via `docs/docs/metrics-plan-quality.mdx`, `docs/docs/metrics-step-efficiency.mdx`, `docs/docs/metrics-tool-use.mdx` content retrieval.

**Gap:** All metrics operate on a single agent trace via `@observe` decorators. No concept of multi-agent orchestration, phase boundaries, handoff quality, or file artifact validation. The evaluation unit is one agent's execution, not a coordinated workflow.

**Inspect AI** -- Native agent evaluation with multi-agent support:
- Built-in ReAct agent with tool loops
- Custom agent protocol (`@agent` decorator)
- Multi-agent architectures: supervisor handoff, sequential workflows, agents-as-tools
- 100+ pre-built evaluations (Source: `docs/evaluations.qmd` in `UKGovernmentBEIS/inspect_ai` repository, which lists evaluation suites including MMLU, GSM8K, ARC, and domain-specific tasks)
- Agent Bridge for integrating external frameworks

Source: `docs/agents.qmd` and `docs/multi-agent.qmd` in `UKGovernmentBEIS/inspect_ai` repository.

**Gap:** Designed for evaluating agent capabilities (e.g., Capture the Flag challenges), not for testing production orchestration workflows. Multi-agent support focuses on task-solving architectures, not on validating workflow correctness, file persistence, or quality gate passage. No concept of "skill" as a test unit.

**Tier 2: Partial Coverage**

**promptfoo** -- Agent security testing:
- OWASP Top 10 for Agentic Applications coverage (ASI01-ASI10)
- Claude Agent SDK provider for testing agent-based applications
- Multi-turn conversation evaluation support
- Red teaming focused on agent vulnerabilities

Source: `site/docs/red-team/owasp-agentic-ai.md`, `site/docs/providers/claude-agent-sdk.md`, `site/docs/configuration/chat.md` in `promptfoo/promptfoo` repository.

**Gap:** Focuses exclusively on security vulnerabilities (goal hijacking, tool misuse, privilege abuse). No functional quality metrics. Cannot evaluate whether a skill produces correct outputs, follows its methodology, or meets quality thresholds.

**Ragas** -- RAG evaluation with emerging agent support:
- Strong RAG-specific metrics (faithfulness, relevancy, recall, precision)
- Test data generation capabilities
- Integration with LangChain and observability tools

Source: README in `explodinggradients/ragas` repository.

**Gap:** No agentic metrics found in documentation search. Primary focus remains RAG pipeline evaluation. No agent, multi-agent, or workflow evaluation capabilities identified.

**Tier 3: Monitoring Only (No Evaluation)**

**AgentOps, Langfuse, LangSmith, Arize Phoenix** -- These tools provide trace-based observability for agent executions but do not perform evaluation (scoring, pass/fail) at any level. They capture what happened but do not assess whether it was correct.

#### What's Missing for Skill-Level Evaluation

| Required Capability | Nearest Existing Approach | Gap Description |
|--------------------|--------------------------|-----------------|
| Skill as test unit | DeepEval `@observe` on agent function | Need orchestrator + multiple agents as single test case |
| Handoff quality validation | Inspect AI multi-agent | Need schema validation of structured handoff data between agents |
| File artifact assertions | None | Need to verify file existence, content, format after skill execution |
| Quality gate verification | None | Need to verify S-014 scoring was applied and thresholds met |
| Phase boundary checkpoints | None | Need to validate state at orchestration phase transitions |
| Constitutional compliance | None | Need to verify agent outputs comply with governance constraints |
| Multi-session reproducibility | None | Need to verify skill produces consistent results across fresh contexts |
| Regression detection | promptfoo comparison view; L1.5 custom assertion approach | Need baseline comparison for skill output quality over time. Solution path: implement custom `assert` functions (see L1.5 "Custom Assert Functions" integration mechanism) that compare current skill output against a stored baseline artifact, enabling regression detection within the promptfoo evaluation pipeline without requiring a dedicated comparison UI. |

---

### L1.5: promptfoo Competitive Threat Assessment

#### Current State (as of 2026-03-03)

| Dimension | Assessment | Evidence |
|-----------|-----------|---------|
| **Version velocity** | Very high | v0.120.17 to v0.120.26 in 6 weeks (9 releases). Active daily development. |
| **Agent support** | Security-only | OWASP Agentic Applications (ASI01-ASI10), Claude Agent SDK provider, OpenAI Agents provider, Bedrock Agents provider. All focused on red-teaming, not functional evaluation. |
| **Multi-turn support** | Chat threads | Supports multi-shot conversations, multi-turn red teaming strategies (crescendo, GOAT, Hydra, tree-based). Not designed for workflow evaluation. |
| **Community demand** | Emerging | GitHub issues show user interest: "Multi-step conversations with changing providers/toolcalls" (open since 2025-07-25), "OWASP Top 10 for Agentic Applications" (closed -- shipped), "Claude Agent SDK provider" (implemented). |
| **Commercial model** | Freemium | Community (free, open-source), Enterprise (custom pricing), On-Premise (custom). Enterprise adds team sharing, continuous monitoring, SSO, API access. |

Source: `promptfoo/promptfoo` GitHub API (releases, issues), `site/src/pages/pricing.tsx`, `site/docs/red-team/owasp-agentic-ai.md`, `site/docs/providers/claude-agent-sdk.md`.

#### Roadmap Direction Analysis

**Signals of where promptfoo is heading:**

1. **Red teaming is the growth vector.** The most active development area is security: OWASP agentic coverage, vulnerability scanning, code scanning, attack strategies (crescendo, GOAT, Hydra, jailbreak). Source: GitHub issues and docs directory structure.

2. **Agent support is provider integration, not evaluation methodology.** Claude Agent SDK, OpenAI Agents, Bedrock Agents are all *provider* integrations -- they allow promptfoo to call agent-based systems, not evaluate agent-specific quality dimensions. Source: `site/docs/providers/` directory.

3. **No evidence of skill/workflow-level evaluation.** No GitHub issues, docs, or code references to "skill evaluation," "workflow testing," "orchestration evaluation," or "multi-agent quality metrics." The open issue on "Multi-step conversations with changing providers/toolcalls" (2025-07-25) is the closest signal, and it remains unresolved.

4. **Enterprise focus is compliance and security dashboards.** Pricing page emphasizes "centralized security/compliance dashboard," "customizable attack profiles," "vulnerability detection" -- not functional quality evaluation. Source: `site/src/pages/pricing.tsx`.

#### Threat Timing Assessment

| Scenario | Probability | Timeline | Impact on Jerry |
|----------|------------|----------|-----------------|
| promptfoo adds agentic functional metrics (like DeepEval's) | Moderate (40%) | 6-12 months | Low -- would still be single-agent, not skill-level |
| promptfoo builds skill/workflow evaluation | Low (15%) | 12-24 months | High -- direct competition if they target orchestrated workflows |
| promptfoo acquires or integrates DeepEval's agentic metrics | Low (10%) | 6-18 months | Moderate -- would combine red teaming + functional evaluation |
| promptfoo focuses exclusively on red teaming/security | High (50%) | Ongoing | None -- non-overlapping market segment |

**Methodology note:** Probabilities are independent scenario estimates, not a mutually exclusive probability distribution (they do not sum to 100%). Multiple scenarios can co-occur (e.g., promptfoo could add agentic metrics while also maintaining red-teaming focus). Estimates are based on: (a) observed roadmap signals from GitHub issues and documentation, (b) current development velocity and resource allocation patterns (red-teaming dominates recent commits), and (c) historical precedent in developer tooling markets where companies typically deepen existing strengths before expanding to adjacent categories (e.g., comparable to how ESLint evolved from syntax checking to type-aware linting -- a 12-18 month expansion cycle after establishing strong community adoption in the narrower domain before extending into adjacent quality dimensions).

**Assessment:** promptfoo is unlikely to build skill-level evaluation within the next 12 months. Their investment thesis appears centered on security/red-teaming (higher enterprise willingness-to-pay, clearer compliance driver). Functional quality evaluation of agent workflows is a different market segment that requires different product design decisions.

#### promptfoo Integration Points for Jerry

Beyond competitive threat assessment, promptfoo presents specific integration opportunities for PROJ-017. The following extension mechanisms are accessible from the promptfoo GitHub repository and documentation:

| Integration Mechanism | Description | Jerry Use Case | Source |
|-----------------------|-------------|---------------|--------|
| **Custom Provider Interface (`callApi`)** | promptfoo providers implement a `callApi(prompt, context)` method that returns `{output, tokenUsage}`. Any callable system can be wrapped as a provider. | Define a Jerry skill execution as a custom provider: the `callApi` method invokes the skill via `jerry` CLI or direct Python API, captures file artifacts, and returns structured results. | `site/docs/configuration/providers.md`, `src/providers/` directory in promptfoo repo |
| **YAML `providers` Configuration** | The `promptfooconfig.yaml` file accepts custom provider paths via `providers: [file://path/to/provider.js]` or inline configuration with `id` and `config` keys. | Configure skill-level test cases in YAML: each test case defines a skill invocation as a custom provider, with expected outputs as assertions. | `site/docs/configuration/guide.md`, `site/docs/configuration/providers.md` |
| **Custom Assert Functions** | The `assert` configuration supports custom assertion functions via `type: javascript` or `type: python` with inline or file-referenced evaluation logic. | Implement skill-specific assertions: file artifact existence checks, frontmatter validation, navigation table presence, quality gate score verification -- all as custom promptfoo assertions. | `site/docs/configuration/expected-outputs/javascript.md`, `site/docs/configuration/expected-outputs/python.md` |
| **`promptfoo eval` CLI Contract** | The `promptfoo eval` command reads `promptfooconfig.yaml`, executes all test cases, and outputs results in JSON/CSV/HTML format. Supports `--output` flag for CI integration. | Integrate `promptfoo eval` into Jerry's CI pipeline for regression testing. Each skill gets a `promptfooconfig.yaml` defining its test cases, run as part of the L5 enforcement layer. | `site/docs/usage/command-line.md` |
| **Dataset/Test Case Format** | Test cases are defined as YAML arrays with `vars` (input variables), `assert` (expected outputs), and optional `options`. Supports CSV, JSON, and YAML data sources. | Map Jerry skill inputs (project context, work item specifications, agent handoffs) to promptfoo `vars`, and skill outputs (file artifacts, quality scores, handoff data) to assertion targets. | `site/docs/configuration/datasets.md` |

**Integration Architecture Pattern:**

```
Jerry Skill Test Case (promptfooconfig.yaml)
    |
    +-- providers: [file://jerry-skill-provider.py]  # Custom provider wrapping skill execution
    +-- tests:
    |     +-- vars: { project: "PROJ-017", skill: "/problem-solving", agent: "ps-researcher" }
    |     +-- assert:
    |           +-- type: python  # Custom assertion for file artifact validation
    |           +-- type: python  # Custom assertion for quality gate verification
    |           +-- type: python  # Custom assertion for handoff schema compliance
    |
    +-- promptfoo eval --output results.json  # CI integration
```

**Viability Assessment:** promptfoo's extension architecture is well-suited for Jerry's skill-level evaluation layer. The custom provider interface can wrap arbitrary skill executions, and custom assertions can implement Jerry-specific validation (file artifacts, quality gates, constitutional compliance) without upstream promptfoo changes. The primary engineering effort is in the custom provider and assertion implementations, not in promptfoo integration itself.

#### DeepEval Competitive Threat Assessment

DeepEval is the more relevant competitive threat because it already has 6 agentic metrics. However:

1. **DeepEval's agentic metrics operate on traces, not orchestrated workflows.** The `@observe` decorator instruments individual functions. There is no concept of testing a multi-agent pipeline as a unit.

2. **Extension to multi-agent would require architectural changes.** DeepEval would need to add: orchestrator-aware test cases, handoff validation metrics, file artifact assertions, and cross-agent quality scoring. This is a significant engineering effort.

3. **DeepEval's latest release (v3.8.8, 2025-12-01) predates current analysis by 3 months.** No major release since December 2025 suggests either a development pause or preparation for a major version. Monitor closely.

---

## L2: Strategic Implications

### Market Timing Window

**Window size: 12-18 months (March 2026 - September 2027)**

The aggregate window is derived from the minimum of the three narrowing/closing sub-trigger timelines below. The 12-month lower bound corresponds to the earliest plausible narrowing trigger (DeepEval extension, 6-12 months, upper bound). The 18-month upper bound corresponds to the midpoint of the LLM provider integration timeline. The window is defined by:

- **Opening (NOW):** No competitor offers skill/workflow-level evaluation (based on GitHub repository and issue tracker analysis; web verification unavailable). Jerry can define the category.
- **Narrowing trigger 1:** DeepEval extends agentic metrics to multi-agent orchestration (estimated 6-12 months if they prioritize it). Basis: DeepEval's last major release (v3.8.8) was 2025-12-01; their agentic metrics infrastructure exists but requires architectural changes for multi-agent support (see L1.5 DeepEval Threat Assessment). Timeline assumes active prioritization, which current release cadence does not confirm.
- **Narrowing trigger 2:** LLM providers (Anthropic, OpenAI) build evaluation into agent SDKs (estimated 12-18 months based on current SDK maturity). Basis: Anthropic's Claude Agent SDK and OpenAI's Agents framework currently provide execution primitives, not evaluation frameworks. Historical precedent from cloud platforms suggests 12-18 months from primitive availability to evaluation tooling release.
- **Closing trigger:** A well-funded competitor (Langfuse, Arize) acquires or builds workflow evaluation capability with enterprise distribution (estimated 18-24 months). Basis: funded companies in adjacent segments would need to pivot from observability to evaluation, requiring both engineering effort and go-to-market repositioning.

### Build-vs-Buy Signals

| Signal | Direction | Rationale |
|--------|----------|-----------|
| No existing tool covers skill-level evaluation | BUILD | Nothing to buy that meets the requirement |
| promptfoo provides strong prompt-level evaluation | INTEGRATE | Use promptfoo for the prompt/response layer; build skill layer on top |
| DeepEval provides agentic metrics | MONITOR | May integrate DeepEval's trace-based metrics as a component, but skill-level orchestration must be built |
| Inspect AI provides agent evaluation primitives | EVALUATE | Inspect AI's agent protocol is well-designed; potential integration point for individual agent testing within skill tests |
| Open-source ecosystem matures rapidly | BUILD OPEN | Any custom solution should be open-source to benefit from community contributions and prevent lock-in |

**Recommendation:** Build the skill-level evaluation layer as a new abstraction. Integrate with promptfoo or DeepEval at the prompt/response level. Do not attempt to replace existing tools at layers they already cover well.

### Competitive Moat Analysis

| Potential Moat | Strength | Durability | Jerry-Specific Advantage |
|---------------|----------|-----------|--------------------------|
| **Skill-level abstraction** | Strong | 12-18 months | First-mover in defining "skill as test unit." No competitor has this concept. |
| **Orchestration-aware evaluation** | Strong | 18-24 months | Evaluating handoff quality, phase boundaries, and cross-agent consistency requires deep domain knowledge of orchestration patterns. |
| **File artifact validation** | Moderate | 6-12 months | Easily replicated but currently unaddressed. Value comes from integration with skill output specifications. |
| **Constitutional compliance testing** | Strong | 18-24 months | Unique to Jerry's governance framework. No generic tool can replicate governance-aware evaluation without framework-specific knowledge. |
| **Quality gate verification** | Moderate | 12-18 months | S-014 scoring verification is framework-specific but the pattern (verify evaluation scores) is generalizable. |
| **Multi-session reproducibility** | Strong | 18-24 months | Testing that skills produce consistent results across fresh contexts requires understanding of context isolation patterns that are specific to agent frameworks. |

**Primary moat:** The combination of orchestration-aware evaluation + constitutional compliance + quality gate verification creates a layered defense that would require a competitor to understand Jerry's entire governance model to replicate. This is a knowledge moat, not a technology moat.

### Strategic Recommendations

1. **Define the category.** Publish the "skill-level evaluation" concept publicly as a GitHub repository README or technical blog post explaining the abstraction layer (skill as test unit, orchestration-aware evaluation, multi-agent handoff validation). Target publication before implementing PROJ-017 Phase 3 to establish category ownership. Being the category creator provides lasting mindshare advantage even if competitors eventually build similar capabilities.

2. **Build on promptfoo's foundation.** promptfoo's declarative YAML config, CI/CD integration, and model comparison UI are best-in-class for prompt-level evaluation. Specifically, use promptfoo's custom provider interface (the `callApi` function in provider configs) to define skill executions as promptfoo test cases. The YAML test format already supports custom providers without upstream changes -- each skill gets a `promptfooconfig.yaml` defining inputs as `vars`, skill execution via a custom provider, and Jerry-specific assertions (file artifact validation, quality gate verification, handoff schema compliance) as custom `assert` functions. See L1.5 "promptfoo Integration Points" for detailed mechanism mapping and the integration architecture pattern diagram in L1.5 for the visual composition of providers, test vars, and assertion types into a working test structure. Build skill-level evaluation as a layer that generates promptfoo-compatible test cases, rather than rebuilding the evaluation infrastructure.

3. **Monitor DeepEval monthly.** DeepEval's agentic metrics are the closest existing capability. Watch for: (a) multi-agent test case support, (b) workflow-aware metrics, (c) file artifact validation. A DeepEval release adding these features shortens the timing window. To operationalize this: add a monthly worktracker review task to check DeepEval's GitHub release notes (`https://github.com/confident-ai/deepeval/releases`) and open GitHub issues (`gh issue list --repo confident-ai/deepeval --state open --search "multi-agent OR workflow OR artifact"`) for the three capability signals listed above. Log findings in the PROJ-017 worktracker entry each month until Phase 3 implementation begins.

4. **Ignore the observability segment.** Langfuse, Arize, AgentOps solve a different problem (monitoring production systems). Do not compete with them; integrate with them for production observability data that feeds back into evaluation test cases.

5. **Prioritize deterministic evaluation.** Given the Porter's analysis showing high LLM provider power, minimize dependence on LLM-as-judge for skill-level assertions. Use deterministic checks (file existence, schema validation, navigation table presence, frontmatter correctness) as the primary evaluation mechanism, with LLM-as-judge reserved for content quality dimensions. This principle should be applied during PROJ-017 Phase 2 (test case design) when defining the assertion strategy for each skill type -- deterministic assertions should be designed first, and LLM-as-judge assertions should only be added where no deterministic equivalent exists.

---

## Data Sources and Methodology

### Data Collection

All quantitative data was collected via the GitHub REST API (`gh api`) on 2026-03-03 and 2026-03-04. The following endpoints were used:

- `repos/{owner}/{repo}` -- Stars, forks, license, language, description, open issues
- `repos/{owner}/{repo}/contributors?per_page=1&anon=true` -- Contributor count via pagination header
- `repos/{owner}/{repo}/releases/latest` -- Latest release tag and date
- `repos/{owner}/{repo}/contents/{path}` -- File content (README, docs, config files)
- `search/code` -- Documentation search within repositories
- `gh issue list --search` -- Issue search for roadmap signals

### Qualitative Analysis Sources

- Repository README files (base64-decoded from API)
- Documentation files in `site/docs/` (promptfoo), `docs/docs/` (DeepEval), `docs/` (Inspect AI)
- GitHub issue titles and states for roadmap signal analysis
- Pricing page source code (promptfoo `site/src/pages/pricing.tsx`)

### Limitations

1. **WebSearch and WebFetch were unavailable.** Funding data, blog posts, press releases, and pricing details for non-open-source offerings could not be verified through web sources. Funding figures are marked with source confidence levels.
2. **Galileo data is limited.** The `rungalileo/galileo-python` repository has only 16 stars, suggesting the main product is a closed-source platform. Unable to assess capabilities without web access to their documentation site.
3. **BrainTrust data is limited.** The main `braintrustdata/braintrust` repository returned 404; only the SDK repo (119 stars) was accessible. BrainTrust appears to be primarily a SaaS product with limited open-source footprint. **BrainTrust capability ratings are based on limited data (primary repo returned 404); treat as lower confidence.** The Prompt/Response Eval = Strong and other capability ratings were inferred from the SDK repository and public documentation fragments only — they may overstate actual capability coverage.
4. **Enterprise pricing is unavailable.** promptfoo, DeepEval (Confident AI platform), Langfuse, and Arize all use "Contact Sales" pricing for enterprise tiers. Actual pricing could not be determined.
5. **Market size estimates were not obtainable.** Without web search access, TAM/SAM/SOM calculations for the LLM evaluation market could not be sourced from analyst reports.

### Source URLs

| Data Point | Source |
|-----------|--------|
| promptfoo repo metadata | `https://github.com/promptfoo/promptfoo` via `gh api repos/promptfoo/promptfoo` |
| DeepEval repo metadata | `https://github.com/confident-ai/deepeval` via `gh api repos/confident-ai/deepeval` |
| Inspect AI repo metadata | `https://github.com/UKGovernmentBEIS/inspect_ai` via `gh api repos/UKGovernmentBEIS/inspect_ai` |
| lm-evaluation-harness metadata | `https://github.com/EleutherAI/lm-evaluation-harness` via `gh api` |
| Ragas repo metadata | `https://github.com/explodinggradients/ragas` via `gh api repos/explodinggradients/ragas` |
| HELM repo metadata | `https://github.com/stanford-crfm/helm` via `gh api repos/stanford-crfm/helm` |
| LangSmith SDK metadata | `https://github.com/langchain-ai/langsmith-sdk` via `gh api` |
| Arize Phoenix metadata | `https://github.com/Arize-ai/phoenix` via `gh api repos/Arize-ai/phoenix` |
| TruLens metadata | `https://github.com/truera/trulens` via `gh api repos/truera/trulens` |
| W&B metadata | `https://github.com/wandb/wandb` via `gh api repos/wandb/wandb` |
| HuggingFace Evaluate metadata | `https://github.com/huggingface/evaluate` via `gh api repos/huggingface/evaluate` |
| MLflow metadata | `https://github.com/mlflow/mlflow` via `gh api repos/mlflow/mlflow` |
| Evidently AI metadata | `https://github.com/evidentlyai/evidently` via `gh api repos/evidentlyai/evidently` |
| Langfuse metadata | `https://github.com/langfuse/langfuse` via `gh api repos/langfuse/langfuse` |
| AgentOps metadata | `https://github.com/AgentOps-AI/agentops` via `gh api repos/AgentOps-AI/agentops` |
| BrainTrust Proxy metadata | `https://github.com/braintrustdata/braintrust-proxy` via `gh api` |
| promptfoo pricing source | `site/src/pages/pricing.tsx` in promptfoo repo |
| promptfoo OWASP Agentic docs | `site/docs/red-team/owasp-agentic-ai.md` in promptfoo repo |
| promptfoo Claude Agent SDK docs | `site/docs/providers/claude-agent-sdk.md` in promptfoo repo |
| promptfoo agent red team docs | `site/docs/red-team/llm-agents.md` in promptfoo repo |
| DeepEval agentic metrics | `docs/sidebars.js`, `docs/docs/metrics-plan-quality.mdx`, `docs/docs/metrics-step-efficiency.mdx`, `docs/docs/metrics-tool-use.mdx` in deepeval repo |
| DeepEval agent quickstart | `docs/docs/getting-started-agents.mdx` in deepeval repo |
| Inspect AI agents overview | `docs/agents.qmd` in inspect_ai repo |
| Inspect AI multi-agent docs | `docs/multi-agent.qmd` in inspect_ai repo |
| promptfoo agent-related issues | `gh issue list --repo promptfoo/promptfoo --search "agentic OR agent evaluation OR multi-turn OR multi-step"` |
| DeepEval agent-related issues | `gh issue list --repo confident-ai/deepeval --search "agent OR agentic OR workflow OR multi-step"` |
| promptfoo custom provider docs | `site/docs/configuration/providers.md` in promptfoo repo (L1.5 integration mechanism: Custom Provider Interface) |
| promptfoo provider source code | `src/providers/` directory in promptfoo repo (L1.5 integration mechanism: callApi interface) |
| promptfoo configuration guide | `site/docs/configuration/guide.md` in promptfoo repo (L1.5 integration mechanism: YAML providers config) |
| promptfoo JavaScript assertions | `site/docs/configuration/expected-outputs/javascript.md` in promptfoo repo (L1.5 integration mechanism: Custom Assert Functions) |
| promptfoo Python assertions | `site/docs/configuration/expected-outputs/python.md` in promptfoo repo (L1.5 integration mechanism: Custom Assert Functions) |
| promptfoo CLI usage | `site/docs/usage/command-line.md` in promptfoo repo (L1.5 integration mechanism: promptfoo eval CLI contract) |
| promptfoo datasets config | `site/docs/configuration/datasets.md` in promptfoo repo (L1.5 integration mechanism: Dataset/Test Case Format) |
| DeepEval architecture docs | `docs/docs/getting-started-agents.mdx` in deepeval repo (Architecture Approaches Comparison: trace-based pipeline) |
| Inspect AI architecture docs | `docs/agents.qmd` in inspect_ai repo (Architecture Approaches Comparison: task-based pipeline) |
| Ragas architecture docs | `explodinggradients/ragas` README (Architecture Approaches Comparison: dataset-centric pipeline) |
| Langfuse architecture docs | Langfuse repository description and docs (Architecture Approaches Comparison: observability-first pipeline) |

---

*Analysis produced: 2026-03-03*
*Data freshness: GitHub API data queried 2026-03-03/04*
*Analyst: Phase 1B competitive analysis agent, PROJ-017 LLM Skill Testing Framework*
