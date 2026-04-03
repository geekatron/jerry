# Web Access Analysis: ux-heart-analyst and ux-kano-analyst

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Plain-language answer |
| [L1: Technical Analysis](#l1-technical-analysis) | Methodology-level evidence |
| [L2: Architectural Implications](#l2-architectural-implications) | Systemic patterns and strategic implications |
| [Evidence Summary](#evidence-summary) | All evidence cited |
| [Conclusion and Recommendation](#conclusion-and-recommendation) | Final verdict |

---

## L0: Executive Summary

Both agents were intentionally designed as T2 (no web access) because their methodologies operate entirely on data the user brings to the session. The decision was not an oversight -- it was a principled application of the "least privilege" rule: don't give tools you won't use.

The short answer to "why wouldn't they require external data" is this: **their methodologies are closed-loop**. They take user-supplied inputs and run deterministic or semi-deterministic processes on them. They do not need to look things up.

However, reading the agent definitions carefully reveals this T2 classification is **partially defensible but not fully correct**. There are specific, legitimate uses for web access in both agents that the original design overlooked. The recommendation is to upgrade both to T3.

---

## L1: Technical Analysis

### What HEART and Kano Actually Do

Before assessing what they need, it helps to be precise about what they do.

**ux-heart-analyst** applies Google's Goals-Signals-Metrics (GSM) process to a user-supplied product and feature description. Its five phases are:

1. Context gathering from input fields and upstream artifacts (all file-based)
2. Dimension selection against a self-contained 5-dimension decision table
3. GSM execution -- translating goals to signals to metrics using the built-in framework
4. Threshold and baseline setting using a "graduated fallback methodology"
5. Dashboard specification for the resulting metrics

**ux-kano-analyst** applies the Kano Model to a user-supplied feature list and optional survey data. Its five phases are:

1. Scope definition from input fields and upstream artifacts
2. Survey design using the built-in functional/dysfunctional question format
3. Response analysis using the 5x5 evaluation table (fully deterministic arithmetic)
4. Priority synthesis computing Better/Worse CS coefficients (arithmetic formulas)
5. Synthesis and handoff preparation

Both agents process structured inputs through well-defined frameworks. The core algorithm in both cases is **inward-looking**: classify these features, generate these metrics, apply this formula. Neither agent needs to crawl the web to do that core work.

This is the correct intuition behind their T2 classification. The question is whether that covers the complete picture.

### Where the T2 Reasoning Breaks Down

Reading the agent definitions carefully, three legitimate web-access use cases emerge for each agent that the original design did not address.

#### For ux-heart-analyst

**Use case 1: Industry benchmark lookup for threshold setting.**

The Threshold Fallback Methodology (Phase 4) explicitly instructs the agent:

> "Use industry benchmarks from published studies as starting point (e.g., Baymard Institute for e-commerce, Bain & Company NPS benchmarks by industry)"

The agent names specific external research organizations (Baymard Institute, Bain & Company) as benchmark sources. But with T2 access, the agent cannot reach these sources. It must hallucinate benchmark values from training data or acknowledge it cannot retrieve them.

This is a significant gap. The agent's own methodology describes a dependency on external benchmark data for the primary threshold-setting step, but the tool tier denies access to that data.

**Use case 2: Verifying metric definitions against current Google HEART research.**

The agent cites Rodden, Hutchinson & Fu (2010) as the authoritative source. The HEART framework has evolved since 2010, and Google has published updated guidance. With T3, the agent could verify that its GSM process reflects current Google recommendations. Without it, the agent operates on its training-data snapshot of a 2010 paper, which may or may not be current.

**Use case 3: Product-type context lookup.**

The Dimension Selection phase provides guidance like "Content/social: Engagement and Retention" and "Transactional (e-commerce): Task Success and Happiness." These are heuristics. For unusual product categories (healthcare SaaS, developer tools, B2B workflows), an agent with web access could look up HEART application patterns for that specific domain rather than extrapolating from generic categories.

#### For ux-kano-analyst

**Use case 1: Kano survey best practices and sample size guidance.**

The agent cites Berger et al. (1993) for sample size thresholds. That paper is 33 years old. Contemporary Kano practitioners (Walden et al., 2019 and others) have published refined guidance on sample size adequacy, question framing, and split classification resolution. With T3, the agent could verify its guidance against current practitioner literature.

The agent already acknowledges this gap implicitly:

> "50+ respondents: 'Enables segment analysis' (practitioner recommendation; Berger et al. 1993 covers thresholds up to 20+ but does not specify segment analysis minimums)"

That parenthetical is the agent disclosing it is filling in a gap with inference because it cannot look it up.

**Use case 2: Competitive context for feature lifecycle assessment.**

Phase 4 includes feature lifecycle dynamics: the Attractive -> Performance -> Must-be migration driven by competitive pressure. The agent's methodology notes:

> "Competitive dynamics the agent cannot observe"

This is precisely what WebSearch provides. If a team is classifying features for a SaaS product, the agent could search for whether competitors have recently commoditized those features (making Attractive features migrate toward Must-be). Without web access, the agent must either ask the user to provide this context or acknowledge it cannot assess lifecycle trajectory.

**Use case 3: Verifying CS coefficient formulas and academic citations.**

The agent cites the CS coefficient formulas from Berger et al. (1993) and Matzler & Hinterhuber (1998). With Context7 or WebFetch, the agent could confirm it has the correct formula (particularly the R/Q exclusion rule, which is sometimes applied differently in newer literature). This is a low-frequency but high-accuracy use case.

### Why the 7 T3 Agents Have Web Access

Mapping what T3 UX agents actually use web access for:

| Agent | Primary Web Access Use |
|-------|----------------------|
| ux-jtbd-analyst | Secondary research: competitive analysis, product reviews, industry reports, app store reviews, social media mentions. Web is the primary evidence source for job discovery when no interview transcripts are available. |
| ux-heuristic-evaluator | Nielsen heuristic definitions, WCAG references, platform design guideline documentation (Material Design, HIG). |
| ux-lean-ux-facilitator | Lean UX methodology references, A/B testing framework documentation, experiment design best practices. |
| ux-ai-design-guide | Current AI SDK documentation, AI interaction design guidelines, platform-specific AI design patterns. The agent explicitly discloses a "Degraded Mode" when web access is unavailable. |
| ux-atomic-architect | Component library documentation, design system specifications, Storybook API references. |
| ux-inclusive-evaluator | WCAG 2.2 criteria, accessibility guidelines, assistive technology documentation. |
| ux-sprint-facilitator | Design sprint methodology references, workshop facilitation techniques, competitive examples. |

The pattern across all seven T3 agents: they access the web because **their methodology requires external inputs the user cannot reasonably supply**. The JTBD analyst needs competitive product data. The heuristic evaluator needs up-to-date accessibility standards. The AI design guide needs current SDK documentation.

The T2 classification of HEART and Kano rests on the claim that their methodologies require no such external inputs. That claim holds for the core algorithmic steps (the 5x5 table, the CS formulas, the GSM process). It does not hold for the calibration and validation steps (benchmarks, current practitioner guidance, competitive context for lifecycle assessment).

### The Steelman Case for Keeping T2

Applying S-003 (Steelman) before recommending upgrade:

**The strongest argument for T2:** The HEART and Kano frameworks are internally consistent and self-contained. Every decision the agent makes can be justified from the framework itself without external reference. The benchmarks mentioned in HEART's threshold methodology are examples, not requirements -- the agent can apply the "baseline + 10-15% improvement" fallback without ever fetching a Baymard Institute report. The Kano agent can produce correct CS coefficient calculations without verifying Berger et al. (1993) online.

This argument is genuinely strong. Both agents would produce correct, methodologically sound outputs without web access. The issue is not correctness -- it is completeness and calibration quality.

**Why the steelman fails the threshold test:** The HEART agent's methodology explicitly names external sources (Baymard Institute, Bain & Company) as step 1 of the threshold-setting process. When the agent cannot reach those sources, step 1 collapses to step 2 (2-week baseline measurement) or step 3 (baseline + 10-15%). The agent degrades silently without disclosing it skipped step 1. This is a P-022 concern: the agent presents a threshold recommendation without disclosing that it bypassed its own step 1 due to tool tier constraints.

---

## L2: Architectural Implications

### The Calibration vs. Core Algorithm Distinction

The T2/T3 boundary in the UX skill tracks an important architectural pattern: **Core Algorithm vs. Calibration Data**.

Core algorithm = the deterministic steps that transform inputs to outputs. This is self-contained and needs no external data. The 5x5 evaluation table, CS coefficient formulas, and GSM process are core algorithms.

Calibration data = the external reference points that make the core algorithm's outputs meaningful in context. Industry benchmarks, current practitioner guidance, competitive context for lifecycle assessment. This requires external access.

T2 is appropriate when the agent's entire value comes from its core algorithm. T3 is appropriate when the agent's output quality depends meaningfully on calibration data.

Both HEART and Kano have deterministic core algorithms (strong T2 signal) AND calibration steps that name external sources (T3 signal). The original T2 classification weighted the core algorithm too heavily and did not account for the calibration steps.

### Consistency Across the UX Skill

Seven of ten UX sub-skill agents are T3. The three T2 agents (ux-heart-analyst, ux-kano-analyst, ux-behavior-diagnostician) share a common characteristic: their core algorithms are more deterministic than the T3 agents.

But this is a matter of degree, not kind. The ux-behavior-diagnostician applies Fogg's B=MAP model, which is also a self-contained framework. Yet it was found (per the question context) to warrant T3 review as well.

A consistent design principle across the UX skill would classify agents as T3 unless they are read-only validators (T1) or pure computation agents with no calibration step. Both HEART and Kano exceed that threshold.

### Risk of Silent Degradation

The more significant architectural concern is not capability but transparency. When a T2 agent's methodology references external sources it cannot reach, the agent must either:
(a) Acknowledge it cannot complete step 1 (requires the agent to know and disclose the tool constraint -- it currently does not)
(b) Silently skip to the fallback step without disclosing why
(c) Hallucinate the benchmark value from training data

Option (b) is the current behavior. Option (c) is a P-001 (evidence) and P-022 (deception) violation. Option (a) requires the agent to be aware of its own tool tier, which is not how agent definitions work.

Upgrading to T3 eliminates this class of failure by letting the agent actually execute its step 1 rather than silently degrading to step 2.

---

## Evidence Summary

| Evidence ID | Type | Source | Relevance |
|-------------|------|--------|-----------|
| E-001 | Agent definition | `skills/ux-heart-metrics/agents/ux-heart-analyst.md` line 229 | Threshold Fallback Methodology step 1 names Baymard Institute and Bain & Company as benchmark sources |
| E-002 | Agent definition | `skills/ux-heart-metrics/agents/ux-heart-analyst.md` line 96-98 | Capabilities section explicitly states "no external web research is required" as T2 rationale |
| E-003 | Governance YAML | `skills/ux-heart-metrics/agents/ux-heart-analyst.governance.yaml` line 6 | `tool_tier: T2` confirmed |
| E-004 | Agent definition | `skills/ux-kano-model/agents/ux-kano-analyst.md` line 109-112 | Capabilities section states "no external research is required (T2 principle of least privilege)" |
| E-005 | Agent definition | `skills/ux-kano-model/agents/ux-kano-analyst.md` line 210-213 | Phase 4 notes "competitive dynamics the agent cannot observe" -- explicit acknowledgment of web access gap |
| E-006 | Agent definition | `skills/ux-kano-model/agents/ux-kano-analyst.md` line 183-186 | 50+ respondent threshold is marked "practitioner recommendation; Berger et al. 1993 does not specify" -- agent is filling a gap without a source |
| E-007 | Governance YAML | `skills/ux-kano-model/agents/ux-kano-analyst.governance.yaml` line 8 | `tool_tier: T2` confirmed |
| E-008 | Agent definition | `skills/ux-jtbd/agents/ux-jtbd-analyst.md` line 100 | JTBD uses web for "competitive job solutions, market context, product reviews, domain literature" -- parallel to Kano competitive context need |
| E-009 | Agent definition | `skills/ux-heuristic-eval/agents/ux-heuristic-evaluator.md` line 97-98 | Heuristic evaluator uses web for Nielsen definitions, WCAG references, platform guidelines -- analogous to HEART framework updates |
| E-010 | Agent definition | `skills/ux-lean-ux/agents/ux-lean-ux-facilitator.md` line 114-115 | Lean UX uses web for methodology references and experiment design best practices -- analogous to Kano practitioner guidance |
| E-011 | Agent definition | `skills/ux-ai-first-design/agents/ux-ai-design-guide.md` line 92-101 | AI design guide has explicit "Degraded Mode" disclosure when web tools unavailable -- the correct pattern for T3 agents |
| E-012 | Governance YAMLs | Seven UX governance files | All seven T3 UX agents declare WebSearch, WebFetch, and Context7 in `allowed_tools` |

---

## Conclusion and Recommendation

### Verdict: Both Should Be T3

The original T2 classification was not wrong -- it correctly identified that the core algorithms of HEART and Kano are self-contained. But it was incomplete. Both agents have calibration steps that explicitly reference external sources, and without web access those steps either silently degrade or produce unverifiable outputs.

**The specific uses that justify T3:**

**ux-heart-analyst:**
- Phase 4 step 1: fetch industry benchmarks from Baymard Institute, Bain & Company, and sector-specific published studies for threshold calibration
- Verify current Google HEART guidance against the 2010 Rodden et al. paper via Context7
- Look up domain-specific HEART application patterns for unusual product categories

**ux-kano-analyst:**
- Verify current Kano practitioner guidance on sample size and split classification resolution
- Search for competitive product context to assess feature lifecycle trajectories (Attractive -> Must-be migration driven by competitor moves)
- Confirm CS coefficient formula variants in post-1998 literature

### What to Change

1. Add WebSearch, WebFetch, and Context7 MCP to both agents' `.md` frontmatter `tools` array
2. Update both governance YAMLs: change `tool_tier: T2` to `tool_tier: T3` and add the three web tools to `allowed_tools`
3. Add a Context7 usage protocol section to both agent `<capabilities>` sections, following the pattern in `ux-heuristic-evaluator.md` lines 104-105
4. Add source authority tiers to both agents' output filtering guardrails, following the `ux-jtbd-analyst.md` pattern (lines 397-401)
5. Add "Degraded Mode" disclosure to both agents for when web tools are unavailable, following the `ux-ai-design-guide.md` pattern (lines 92-101)

### Confidence Assessment

- Conclusion that both should be T3: **HIGH** -- the evidence from their own methodology text is explicit and unambiguous
- Specific web access uses enumerated above: **MEDIUM** -- these are the most evident cases; there may be additional uses that emerge during actual agent invocations
- Risk of not upgrading: **MEDIUM** -- both agents produce valid outputs at T2, but the calibration step silent degradation is a P-022 concern that accrues over time as users receive threshold recommendations without knowing step 1 was skipped

---

*Analysis Version: 1.0.0*
*Method: Evidence-based trade-off analysis with S-003 Steelman*
*Agent: ps-analyst*
*Project: PROJ-024-tactical-work*
*STORY: STORY-013-fix-tier-tool-mismatches*
*Date: 2026-03-28*
