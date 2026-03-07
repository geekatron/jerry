# Test Harness Research — Orchestration Prompt

> **Project:** PROJ-035-skill-optimization
> **Template:** Template 3 (Multi-Skill Orchestration)
> **Skills:** /orchestration + /problem-solving + /adversary
> **Quality Gate:** >= 0.92 S-014 weighted composite at every phase boundary
> **pe-scorer assessment:** 93/100 (Exemplary tier)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Prompt](#prompt) | Complete ready-to-execute orchestration prompt |
| [5-Element Analysis](#5-element-analysis) | pe-builder element verification |
| [Quality Score](#quality-score) | pe-scorer 7-criterion rubric assessment |

---

## Prompt

```
Use /worktracker to create a Feature titled "Test Harness for LLM Prompt Evaluation
and Safe Refactoring" under PROJ-035.

Use /orchestration with orch-planner to sequence the following 8-phase pipeline.

All agents MUST use jerry:{agent-name} subagent_type format.
Do NOT use generic general-purpose or Explore agents.

---

### Phase 1 — Parallel Research (4 concurrent streams)

All Phase 1 streams use jerry:ps-researcher.
All research MUST use Context7 MCP (resolve-library-id then query-docs) and
WebSearch/WebFetch exclusively.
NEVER cite LLM training knowledge as a source — all claims require external
URLs or Context7 query citations.
ONLY include frameworks, SDKs, and tools with verified open-source licenses
(MIT, Apache 2.0, BSD, MPL, LGPL, or similar OSI-approved licenses).
Exclude any tool or SDK where the license is proprietary, source-available-only,
or where research usage could create legal liability.

#### 1A: Historical Testing Methodologies
Agent: jerry:ps-researcher

Discover and catalog the most influential code testing methodologies from their
earliest academic origins through present day.
Data sources: WebSearch for academic papers, conference proceedings, and historical
surveys. WebFetch for specific cited sources.

Research directives:
- Search for "history of software testing methodologies" and "evolution of testing
  practices" to identify the foundational methodologies and their originators
- Search for "software testing taxonomy" and "testing strategy classification" to
  discover how the field organizes testing approaches
- Identify minimum 8 distinct methodologies that the external sources themselves
  rank as most influential or widely adopted
- For each methodology discovered: document its origin (who, when, where published),
  core mechanism, effectiveness evidence cited in the sources, known limitations
  per the literature, and assess applicability to LLM prompt testing
- Do NOT pre-assume which methodologies will appear — let the search results
  determine what is historically significant

Completeness check: If fewer than 8 methodologies are discovered, broaden search
terms (e.g., "testing paradigms", "verification approaches", "quality assurance
methods in software engineering").

Output: projects/PROJ-035-skill-optimization/research/historical-testing-methodologies.md
with L0/L1/L2 sections.


#### 1B: Industry Top Frameworks (minimum 10 total)
Agent: jerry:ps-researcher

Discover the current industry-leading testing frameworks across two categories.
Data sources: Context7 (resolve discovered frameworks), WebSearch for rankings
and adoption data.

Discovery approach for Traditional Code Testing (minimum 5):
- Search for "most popular testing frameworks 2025 2026" across multiple languages
- Search for "best testing frameworks by language" and "testing tool comparison"
- Use Context7 to resolve and query documentation for each framework discovered
- Let external rankings, adoption metrics, and community size determine which
  frameworks are "top" — do not pre-select

Discovery approach for LLM/AI-Specific Testing (minimum 5):
- Search for "LLM evaluation frameworks", "prompt testing tools",
  "AI testing frameworks comparison"
- Search for "LLM evaluation open source tools" and "prompt regression testing"
- Use Context7 to resolve and query documentation for each framework discovered
- Include frameworks the sources themselves rank by stars, downloads, or citations

For each framework discovered include: architecture, key capabilities, CI/CD
integration, community adoption evidence (sourced from GitHub, package registries,
or published benchmarks — not assumed), and suitability for LLM prompt regression
testing.

Completeness check: If fewer than 5 are found in either category, broaden search
terms (e.g., "AI quality assurance tools", "end-to-end testing tools ranking").

Output: projects/PROJ-035-skill-optimization/research/industry-frameworks-survey.md
with L0/L1/L2 sections.


#### 1C: Agent SDK Evaluation
Agent: jerry:ps-researcher

Discover and evaluate current Agent SDKs for their testing capabilities and
harness integration potential.
Data sources: Context7 (resolve discovered SDKs), WebSearch.

Discovery approach:
- Search for "AI agent frameworks 2025 2026", "agent SDK comparison",
  "multi-agent framework testing capabilities"
- Search for "LLM agent development kit" and "agentic AI frameworks"
- Use Context7 resolve-library-id for each SDK discovered to access its
  official documentation
- Identify minimum 6 SDKs that external sources rank as actively maintained
  and widely adopted — let the search results determine which SDKs matter

For each SDK discovered include: testing API surface, mocking/stubbing
capabilities, determinism controls, CI/CD patterns, evaluation framework
integration points, and gaps relevant to LLM prompt regression testing.

Completeness check: If fewer than 6 SDKs are discovered, broaden search
(e.g., "orchestration frameworks for LLM agents", "agent building tools").

Output: projects/PROJ-035-skill-optimization/research/agent-sdk-evaluation.md
with L0/L1/L2 sections.


#### 1D: Innovation Frameworks for Code Quality Measurement
Agent: jerry:ps-researcher

Discover emerging and innovative frameworks for measuring and ensuring code quality,
with emphasis on LLM/AI-specific innovations.
Data sources: WebSearch, WebFetch, Context7 where applicable.

Discovery approach:
- Search for "LLM evaluation methodology 2025 2026", "AI code quality measurement",
  "prompt quality assurance techniques"
- Search for "novel approaches to LLM testing", "automated evaluation of language
  model outputs", "LLMOps testing innovation"
- Search for "statistical methods for LLM evaluation" and "behavioral testing
  for AI systems"
- Search for academic sources: "arxiv LLM evaluation framework",
  "NeurIPS ICML testing methodology"
- Identify minimum 8 distinct innovation areas that external sources describe
  as active research or emerging practice — let the literature determine what
  is innovative, not pre-assumed categories

For each innovation discovered include: maturity level
(experimental/emerging/production-ready) as assessed by the sources themselves,
adoption evidence with citations, statistical rigor of the approach, and
integration feasibility for a Jerry Framework test harness.

Completeness check: If fewer than 8 innovations are discovered, broaden search
(e.g., "software quality measurement innovation", "next generation testing tools",
"AI-assisted code quality").

Output: projects/PROJ-035-skill-optimization/research/innovation-frameworks.md
with L0/L1/L2 sections.


---

### Phase 2 — Quality Gate 1 (Barrier 1)

Agent: jerry:adv-scorer
Score each Phase 1 output (1A, 1B, 1C, 1D) against S-014 LLM-as-Judge rubric.
Quality threshold: >= 0.92 weighted composite.

Dimensions and weights:
- Completeness (0.20)
- Internal Consistency (0.20)
- Methodological Rigor (0.20)
- Evidence Quality (0.15)
- Actionability (0.15)
- Traceability (0.10)

Below threshold: Return to producing jerry:ps-researcher for targeted revision.
Maximum 3 revision iterations per deliverable.

Score reports: projects/PROJ-035-skill-optimization/work/test-harness/adv/phase-1-scores/


---

### Phase 3 — Cross-Pollination Synthesis

Agent: jerry:ps-synthesizer
Cross-pollinate all 4 Phase 1 research outputs.

Input artifacts:
- research/historical-testing-methodologies.md
- research/industry-frameworks-survey.md
- research/agent-sdk-evaluation.md
- research/innovation-frameworks.md

Synthesis tasks:
1. Map historical testing methodologies to LLM testing equivalents
   (use mappings discovered in Phase 1 research, not pre-assumed analogies)
2. Framework capability matrix — which frameworks cover which evaluation needs
3. SDK testing gap analysis — what testing capabilities are missing from
   current Agent SDKs for prompt regression testing
4. Innovation readiness assessment — which innovation frameworks are
   production-ready vs. experimental, with evidence
5. Convergence patterns — themes appearing across 3+ research streams
6. Identify the optimal combination of approaches for an LLM prompt test harness
   that enables safe refactoring and migration

Output: projects/PROJ-035-skill-optimization/analysis/cross-pollination-synthesis.md
with L0/L1/L2 sections.


---

### Phase 4 — Quality Gate 2 (Barrier 2)

Agent: jerry:adv-scorer
Score Phase 3 synthesis against S-014 rubric.
Quality threshold: >= 0.92 weighted composite.
Below threshold: Return to jerry:ps-synthesizer for revision. Maximum 3 iterations.

Score report: projects/PROJ-035-skill-optimization/work/test-harness/adv/phase-3-score.md


---

### Phase 5 — Analytical Evaluation

Agent: jerry:ps-analyst
Analyze the synthesized findings to evaluate what combination of approaches would be
most effective for building an LLM prompt test harness for safe refactoring and migration.

Evaluation dimensions:
1. Refactoring safety — ability to detect prompt behavioral regressions after changes
2. Migration confidence — ability to validate prompt behavior across model versions/providers
3. Determinism coverage — percentage of evaluations producing consistent results
4. Statistical rigor — confidence interval support, significance testing, sample size guidance
5. Integration feasibility — effort to integrate with Jerry Framework's existing architecture
6. Evidence basis — strength of external research evidence supporting effectiveness

Apply FMEA to identify failure risks in the proposed test harness approach.
Apply comparative analysis across the 6 dimensions for the top candidate approaches.

Context: Jerry Framework architecture and PROJ-017 ADR-002 (which recommended promptfoo
extension architecture — see ADR-002-quality-framework-selection in PROJ-017
for prior evaluation context that this analysis should build upon, not duplicate).

Input: analysis/cross-pollination-synthesis.md + all Phase 1 research outputs.

Output: projects/PROJ-035-skill-optimization/analysis/test-harness-evaluation.md
with L0/L1/L2 sections.


---

### Phase 6 — Quality Gate 3 (Barrier 3)

Agent: jerry:adv-scorer
Score Phase 5 analysis against S-014 rubric.
Quality threshold: >= 0.92 weighted composite.
Below threshold: Return to jerry:ps-analyst for revision. Maximum 3 iterations.

Score report: projects/PROJ-035-skill-optimization/work/test-harness/adv/phase-5-score.md


---

### Phase 7 — Architecture Decision

Agent: jerry:ps-architect
Synthesize all findings into a test harness architecture recommendation.

Evaluate 3 options (derived from Phase 5 analysis — do not predetermine options;
let the research evidence drive option generation):
- Option A: [Research-derived approach 1]
- Option B: [Research-derived approach 2]
- Option C: [Research-derived approach 3]

Evaluation dimensions: refactoring safety, migration confidence, determinism coverage,
statistical rigor, integration feasibility, time to first value.

Prior art context: PROJ-017 ADR-002 recommended promptfoo extension architecture
for skill-level evaluation. This ADR should address the complementary question:
how to build the test harness for prompt refactoring safety, which may leverage,
extend, or diverge from the PROJ-017 recommendation based on research evidence.

Input: all Phase 1 research + Phase 3 synthesis + Phase 5 analysis.

Output: projects/PROJ-035-skill-optimization/decisions/ADR-001-test-harness-architecture.md
in Nygard ADR format with L0/L1/L2 sections.


---

### Phase 8 — Final Quality Gate + Human Review (Barrier 4)

Dual quality gate:

Gate 1 — Agent: jerry:adv-scorer
S-014 rubric scoring >= 0.92 on ADR-001.
Below threshold: Return to jerry:ps-architect for revision. Maximum 3 iterations.

Gate 2 — Agent: jerry:nse-reviewer
Technical review gate with entrance/exit criteria per NPR 7123.1D Appendix G.
Verify: requirements traceability, evidence basis, risk coverage, implementation feasibility.

Both gates MUST pass before presenting to human.
PASS: Present full pipeline results to human for review and ADR acceptance per P-020.

Score reports: projects/PROJ-035-skill-optimization/work/test-harness/adv/phase-7-scores/


---

### Orchestration Configuration

Use /orchestration and orch-planner to sequence the above pipeline with:

- Parallel execution: Phase 1 streams (1A, 1B, 1C, 1D) run concurrently
- Sync barrier after Phase 1: all 4 must pass Quality Gate 1 before Phase 3
- Sequential: Phase 3 → Phase 5 → Phase 7 (each depends on prior output)
- Quality gates at every phase boundary (Phases 2, 4, 6, 8)
- All agent invocations use jerry:{agent-name} subagent_type format
- Include self-review (S-010) within each research phase before quality gate scoring
- Cross-pollination between research streams happens at Phase 3 barrier

Output orchestration plan:
projects/PROJ-035-skill-optimization/orchestration/test-harness-research-20260306-001/ORCHESTRATION_PLAN.md


### Constraints

<forbidden_actions>
  <constraint format="NPT-013">
    NEVER use generic general-purpose or Explore subagent_type — Consequence: bypasses
    Jerry's declared agent definitions, loses governance YAML guardrails, and produces
    unauditable output. Instead: use jerry:{agent-name} format
    (e.g., jerry:ps-researcher, jerry:ps-synthesizer, jerry:adv-scorer).
  </constraint>
  <constraint format="NPT-013">
    NEVER cite LLM training knowledge as a source for research claims — Consequence:
    introduces unverifiable bias and undermines the unbiased market research requirement.
    Instead: all claims must cite Context7 query results, WebSearch results, or WebFetch
    page content with URLs.
  </constraint>
  <constraint format="NPT-013">
    NEVER proceed past a quality gate with score below 0.92 — Consequence: low-quality
    research propagates through synthesis and analysis phases, compounding errors per
    error amplification patterns. Instead: return to the producing agent for targeted
    revision, maximum 3 iterations per deliverable.
  </constraint>
  <constraint format="NPT-013">
    NEVER present the final ADR to the user without passing both adv-scorer AND
    nse-reviewer gates — Consequence: deliverable bypasses dual quality assurance,
    violating H-13 and H-14. Instead: complete both gates and present only after
    both pass.
  </constraint>
  <constraint format="NPT-013">
    NEVER include frameworks, SDKs, or tools without verified open-source licenses
    (OSI-approved: MIT, Apache 2.0, BSD, MPL, LGPL, or equivalent) — Consequence:
    proprietary or source-available-only tools create legal liability for research
    evaluation and downstream implementation. Instead: verify the license via the
    project's repository or official site during research, and exclude any tool
    where the license cannot be confirmed as open-source.
  </constraint>
  <constraint format="NPT-013">
    NEVER pre-populate research coverage lists with specific tool or methodology
    names from LLM training data — Consequence: biases the research toward the
    model's training distribution rather than current market reality, defeating the
    purpose of unbiased external research. Instead: use discovery-oriented search
    queries and let external sources (WebSearch, Context7) determine what is
    relevant and highly ranked.
  </constraint>
</forbidden_actions>
```

---

## 5-Element Analysis

| Element | Present | Content |
|---------|---------|---------|
| **1. Skill Routing** | Yes | `/orchestration` with orch-planner, `/problem-solving` with jerry:ps-researcher / jerry:ps-synthesizer / jerry:ps-analyst / jerry:ps-architect, `/adversary` with jerry:adv-scorer, jerry:nse-reviewer |
| **2. Scope** | Yes | Domain: LLM prompt test harness for safe refactoring/migration. Historical origins through present (2026). Minimum 8 methodologies, 10+ frameworks, 6 SDKs, 8+ innovation areas — all discovered via external research, not pre-populated. Open-source licensed only. |
| **3. Data Source** | Yes | Context7 MCP (resolve-library-id + query-docs) for framework documentation. WebSearch for research papers, adoption metrics, comparison data. WebFetch for specific URLs. NPT-013 constraints: NEVER cite LLM training data; NEVER pre-populate lists from training knowledge; NEVER include non-OSI-licensed tools. |
| **4. Quality Gate** | Yes | >= 0.92 S-014 weighted composite at every phase boundary. jerry:adv-scorer at Phases 2, 4, 6, 8. jerry:nse-reviewer dual gate at Phase 8. Maximum 3 revision iterations per deliverable. |
| **5. Output Path** | Yes | All outputs under `projects/PROJ-035-skill-optimization/` with explicit paths per phase. L0/L1/L2 sections on all research/analysis artifacts. Nygard ADR format for architecture decision. |

---

## Quality Score

**pe-scorer 7-criterion rubric assessment:**

| # | Criterion | Weight | Raw (0-3) | Weighted | Notes |
|---|-----------|--------|-----------|----------|-------|
| C1 | Task Specificity | 20% | 3.0 | 20.0 | Discovery directives explicit. Minimum counts specified. Search terms provided. Completeness checks included. Zero undefined terms. |
| C2 | Skill Routing | 18% | 3.0 | 18.0 | Three skills with /slash syntax. Seven distinct jerry:{agent} names. P-003 compliant topology. |
| C3 | Context Provision | 15% | 3.0 | 15.0 | PROJ-017 ADR-002 referenced as prior art. Jerry Framework architecture cited. No redundant padding. |
| C4 | Quality Specification | 15% | 3.0 | 15.0 | Numeric threshold (0.92), named mechanism (adv-scorer + nse-reviewer), iteration bounds (max 3), 6 S-014 dimensions with weights. |
| C5 | Decomposition | 12% | 3.0 | 12.0 | 8 phases, 4 parallel streams, 4 sync barriers, named agents per phase, sequential dependency chain. |
| C6 | Output Specification | 12% | 3.0 | 12.0 | Explicit file path per phase. L0/L1/L2 format. Nygard ADR. Score report directories. Orchestration plan path. |
| C7 | Positive Framing | 8% | 2.5 | 6.7 | Main body positive. NPT-013 constraints use structured negation with "Instead:" alternatives (intentional per NPT-013 format). |

**Composite Score: 98.7 / 100 — Exemplary Tier**

> Exemplary (90-100): Completes without clarification. Artifacts at correct paths. Quality gates fire at specified threshold.

---

*Generated by pe-builder (5-element assembly) + pe-scorer (7-criterion rubric)*
*Template: Template 3 (Multi-Skill Orchestration) from `.context/rules/prompt-templates.md`*
*Constraints: NPT-013 structured negation per PROJ-014 findings*
