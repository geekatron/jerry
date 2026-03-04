# PROJ-017 Phase 2 Orchestration Plan: Deep Analysis Pipeline

<!-- VERSION: 2.3.0 | DATE: 2026-03-03 | SOURCE: ADR-001 + Addendum A bias corrections + expanded /nasa-se integration -->

> Eight-phase pipeline with expanded /nasa-se integration, adversarial quality gates (>= 0.92) at every stage, and bidirectional cross-pollination between /nasa-se and /adversary findings. Web-sourced research ONLY (no LLM training data). Cross-pollination across /pm-pmm, /problem-solving, /nasa-se (nse-requirements, nse-verification, nse-risk, nse-reviewer), and /adversary.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Pipeline Overview](#pipeline-overview) | Visual pipeline with parallel execution and quality gates |
| [Phase Definitions](#phase-definitions) | Summary table of all phases, agents, and gates |
| [Phase Details](#phase-details) | Detailed specification per phase |
| [Adversary Integration](#adversary-integration) | Quality gate specification at each phase boundary |
| [Cross-Pollination Protocol](#cross-pollination-protocol) | Forward flow, feedback flow, and bidirectional NSE-ADV integration |
| [Sync Barriers](#sync-barriers) | Barrier definitions and pass criteria |
| [State Schema](#state-schema) | Orchestration state tracking fields |
| [Execution Notes](#execution-notes) | Parallel groups, context isolation, session guidance |
| [NASA-SE Integration Summary](#nasa-se-integration-summary) | Agent placement and cross-pollination role |
| [NPT Constraints](#npt-constraints) | Behavioral constraints (FORBIDDEN + REQUIRED) |

---

## Pipeline Overview

```
                           PROJ-017 Phase 2: Deep Analysis Pipeline (v2.3.0)
                           ================================================

                                    ┌─── Barrier 1 ────────────────────────────┐
                                    │ (All 4 phases + ADV gates must pass)     │
                                    │                                          │
Phase 1A: Industry Standards ──────── ADV-1A ──────┐                          │
  (ps-researcher, /problem-solving)    (>=0.92)     │                          │
                                                    │                          │
Phase 1B: Competitive Landscape ───── ADV-1B ──────┤                          │
  (pm-competitive-analyst, /pm-pmm)    (>=0.92)     │                          │
                                                    ├── Barrier 1 ── Phase 2   │
Phase 1C: Jerry Integration ───────── ADV-1C ──────┤                          │
  (ps-researcher, /problem-solving)    (>=0.92)     │                          │
                                                    │                          │
Phase 1D: Evaluation Criteria ─────── ADV-1D ──────┘                          │
  (nse-requirements, /nasa-se)         (>=0.92)                                │
                                    └──────────────────────────────────────────┘

                                                      │
                                                      v
                                                Phase 2: Synthesis
                                                (ps-synthesizer, /problem-solving)
                                                      │
                                                   ADV-2
                                                   (>=0.92)
                                                      │
                                               ┌──────┴──────┐
                                               │             │
                                         Phase 3A: V&V   Phase 3B: Risk
                                         (nse-verif.)    (nse-risk)
                                         (/nasa-se)      (/nasa-se)
                                               │             │
                                           ADV-3A        ADV-3B
                                           (>=0.92)      (>=0.92)
                                               │             │
                                               └──────┬──────┘
                                                      │
                                               Barrier 3
                                                      │
                                                      v
                                                Phase 4: Cross-Pollination
                                                (ps-synthesizer, /problem-solving)
                                                      │
                                                   ADV-4
                                                   (>=0.92)
                                                      │
                                                      v
                                                Phase 5: Trade Study
                                                (ps-analyst, /problem-solving)
                                                      │
                                                   ADV-5
                                                   (>=0.92)
                                                      │
                                                      v
                                                Phase 6: Architecture
                                                Decision Record
                                                (ps-architect, /problem-solving)
                                                      │
                                                ┌─────┴─────┐
                                                │           │
                                             ADV-6     NSE-REV
                                             (>=0.92)  (nse-reviewer)
                                                │           │
                                                └─────┬─────┘
                                                      │
                                               Barrier 7 (Dual Gate)
                                                      │
                                                      v
                                                   COMPLETE
```

---

## Phase Definitions

| Phase | Primary Agent | Skill | Data Sources | Output Artifact | Quality Gate |
|-------|--------------|-------|-------------|-----------------|--------------|
| 1A | ps-researcher | /problem-solving | WebSearch, WebFetch, Context7 ONLY | `research/industry-standards-v2.md` | ADV-1A: >= 0.92 |
| 1B | pm-competitive-analyst | /pm-pmm | WebSearch, WebFetch ONLY | `research/competitive-landscape.md` | ADV-1B: >= 0.92 |
| 1C | ps-researcher | /problem-solving | WebSearch, WebFetch, Context7 ONLY | `research/jerry-integration-analysis.md` | ADV-1C: >= 0.92 |
| 1D | nse-requirements | /nasa-se | WebSearch, WebFetch ONLY | `research/evaluation-criteria.md` | ADV-1D: >= 0.92 |
| 2 | ps-synthesizer | /problem-solving | Phase 1A + 1B + 1C + 1D outputs | `analysis/synthesized-findings.md` | ADV-2: >= 0.92 |
| 3A | nse-verification | /nasa-se | Phase 2 + ADR-001 + Phase 1D criteria | `analysis/verification-report.md` | ADV-3A: >= 0.92 |
| 3B | nse-risk | /nasa-se | Phase 2 + ADR-001 | `analysis/risk-assessment.md` | ADV-3B: >= 0.92 |
| 4 | ps-synthesizer | /problem-solving | Phase 2 + 3A + 3B + all ADV findings + 1D criteria | `analysis/cross-pollination-synthesis.md` | ADV-4: >= 0.92 |
| 5 | ps-analyst | /problem-solving | Phase 4 + ADR-001 Addendum A | `analysis/trade-study.md` | ADV-5: >= 0.92 |
| 6 | ps-architect | /problem-solving | Phase 5 + user selection + all prior | `decisions/ADR-002-quality-framework-selection.md` | ADV-6 + NSE-REV (parallel) |

> All output paths are relative to `projects/PROJ-017-llm-skill-testing/`.

---

## Phase Details

### Phase 1A: Industry Standards Research

**Agent:** ps-researcher (divergent, /problem-solving)
**Data Sources:** WebSearch + WebFetch + Context7 ONLY (no LLM training data)

**Research Focus:**
- LLM evaluation approaches (deterministic, statistical, LLM-as-judge, hybrid)
- Evaluation frameworks and tools (promptfoo, DeepEval, Inspect AI, lm-eval-harness, Ragas)
- Statistical methods for paired LLM comparison (bootstrap, permutation, effect size)
- Determinism tier classification (T1 structural, T2 statistical, T3 hybrid, T4 LLM-judged)
- Skill-level evaluation gap verification

**Output:** `research/industry-standards-v2.md` with L0/L1/L2 sections

### Phase 1B: Competitive Landscape Analysis

**Agent:** pm-competitive-analyst (divergent, /pm-pmm)
**Data Sources:** WebSearch + WebFetch ONLY

**Analysis Focus:**
- Competitive landscape of LLM evaluation tools (15+ tools)
- Porter's Five Forces analysis of the evaluation tool market
- Funding and market position of key players
- Gap analysis: which tools approach skill-level evaluation
- promptfoo competitive threat assessment (timing, capability proximity)

**Output:** `research/competitive-landscape.md` with L0/L1/L2 sections

### Phase 1C: Jerry Integration Analysis

**Agent:** ps-researcher (divergent, /problem-solving)
**Data Sources:** WebSearch + WebFetch + Context7 ONLY + Jerry codebase

**Analysis Focus:**
- Jerry Framework quality gate integration points (6-dimension rubric, H-rules)
- Existing Jerry agent architecture and how skill evaluation maps to it
- CLI integration patterns (jerry CLI, promptfoo CLI interop)
- Governance compliance validator design (H-rule checks as assertions)
- Determinism-first architecture alignment with Jerry's quality enforcement

**Output:** `research/jerry-integration-analysis.md` with L0/L1/L2 sections

### Phase 1D: Evaluation Criteria Definition

**Agent:** nse-requirements (/nasa-se)
**Data Sources:** WebSearch + WebFetch ONLY + Jerry governance docs

**Requirements Areas:**

| Area | Focus |
|------|-------|
| Stakeholder needs | Who uses the framework, what decisions it informs |
| Quality attributes | Determinism, reproducibility, cost-efficiency, CI/CD readiness |
| Evaluation dimensions | What dimensions to measure when comparing frameworks |
| Acceptance criteria | Quantifiable thresholds for framework selection |
| Traceability matrix | Requirements traced to ADR-001 options and evaluation dimensions |

**Cross-Pollination Role:** Phase 1D criteria feed into Phase 2 (inform ranking), Phase 3A (verification scope), and all ADV gate focus areas.

**Output:** `research/evaluation-criteria.md`

### Phase 2: Research Synthesis

**Agent:** ps-synthesizer (integrative, /problem-solving)
**Inputs:** Phase 1A + 1B + 1C + 1D outputs

**Synthesis Tasks:**
1. Unified cross-reference table (all evaluation approaches x all dimensions)
2. Convergent findings (patterns confirmed by 2+ sources)
3. Divergent findings (contradictions between sources)
4. Gap analysis (what remains unknown after Phase 1 research)
5. Determinism tier classification of all approaches
6. Requirements alignment (Phase 1D criteria mapped to synthesis findings)

**Output:** `analysis/synthesized-findings.md` with L0/L1/L2 sections

### Phase 3A: Verification & Validation Report

**Agent:** nse-verification (/nasa-se)
**Inputs:** Phase 2 synthesis + ADR-001 + Phase 1D evaluation criteria

**Verification Dimensions:**

| Dimension | Focus |
|-----------|-------|
| Evidence completeness | Are all ADR-001 claims supported by Phase 2 evidence? |
| Source authority | Are cited sources primary, secondary, or tertiary? |
| Methodology soundness | Are evaluation approaches correctly characterized? |
| Statistical validity | Are statistical claims (N>=30, bootstrap) well-founded? |
| Requirements compliance | Do findings satisfy Phase 1D evaluation criteria? |

**Cross-Pollination:** V&V gaps feed Phase 4 cross-pollination; findings converge with ADV adversarial critique.

**Output:** `analysis/verification-report.md`

### Phase 3B: Risk Assessment

**Agent:** nse-risk (/nasa-se)
**Inputs:** Phase 2 synthesis + ADR-001

**Risk Dimensions:**

| Dimension | Focus |
|-----------|-------|
| Adoption risk | Developer friction, learning curve, ecosystem maturity |
| Integration risk | Jerry CLI compatibility, quality gate alignment, CI/CD complexity |
| Obsolescence risk | Competitive threat timeline, technology evolution |
| Measurement risk | Statistical validity, false positive/negative rates, N sensitivity |
| Gap risk | Unresolved research gaps that could invalidate conclusions |

**Assessment Method:** Likelihood x Impact scoring per framework option. Risk register with mitigation strategies.

**Cross-Pollination:** Risk register feeds Phase 4; risk quantifies adversary-identified weaknesses. NSE risk and ADV adversary findings converge during Phase 4 synthesis.

**Output:** `analysis/risk-assessment.md`

### Phase 4: Cross-Pollination Synthesis

**Agent:** ps-synthesizer (integrative, /problem-solving)
**Inputs:** Phase 2 + 3A + 3B + ADV-1A through ADV-3B findings + Phase 1D criteria

**Cross-Pollination Tasks:**
1. Technical vs. market convergence (where research and competitive data agree)
2. Jerry-specific integration opportunities (codebase patterns x market gaps)
3. Adversary critique integration (what did adversarial reviews challenge across all phases?)
4. Requirements compliance update (Phase 1D criteria satisfaction status)
5. NSE <-> ADV convergence analysis (V&V gaps that confirm adversary weaknesses; risk findings that quantify adversary attack vectors)
6. Gap resolution status (which Phase 2 gaps were resolved by Phase 3A/3B/ADV findings?)

**Output:** `analysis/cross-pollination-synthesis.md`

### Phase 5: Trade Study

**Agent:** ps-analyst (convergent, /problem-solving)
**Inputs:** Phase 4 cross-pollination synthesis + ADR-001 Addendum A

**Trade Study Dimensions:**
- Time to first value (weighted 0.25)
- Determinism coverage (0.15)
- Statistical rigor (0.15)
- Cost per evaluation suite (0.15)
- Extensibility (0.10)
- Adoption friction (0.10)
- Competitive defensibility (0.10)

**Analysis Method:** Quantitative trade matrix with evidence-based scoring per ADR-001 dimension weights. Sensitivity analysis on dimension weights. Bias-corrected scoring per Addendum A (tool-agnostic evaluation, not promptfoo-centric).

**Output:** `analysis/trade-study.md`

### Phase 6: Architecture Decision Record

**Agent:** ps-architect (convergent, /problem-solving)
**Inputs:** Phase 5 trade study + user selection + all prior artifacts

**ADR Structure:** Nygard format with:
- Context: Problem statement, forces, constraints
- Options evaluated: 3 options with steelman (S-003) for each
- Decision: Selected option with rationale
- Consequences: Positive, negative, neutral
- Risks: Risk register with mitigations
- L0/L1/L2 output levels

**Phase 6 Dual Gate:**

| Gate | Agent | Skill | Focus |
|------|-------|-------|-------|
| ADV-6 | adv-scorer | /adversary | S-014 rubric scoring (>= 0.92), constitutional compliance, steelman/devil's advocate |
| NSE-REV | nse-reviewer | /nasa-se | NPR 7123.1D technical review: entrance/exit criteria, requirements traceability, risk closure, V&V completeness |

Both gates execute in parallel. Both must pass for the ADR to be accepted.

**Output:** `decisions/ADR-002-quality-framework-selection.md`

---

## Adversary Integration

Each phase boundary includes an adversarial quality gate using /adversary (adv-scorer, S-014 rubric).

| Gate ID | Phase | Agent | Threshold | Focus Areas |
|---------|-------|-------|-----------|-------------|
| ADV-1A | After 1A | adv-scorer | >= 0.92 | Evidence quality, source authority, completeness of evaluation approach coverage |
| ADV-1B | After 1B | adv-scorer | >= 0.92 | Market data currency, competitive landscape completeness, Porter's analysis rigor |
| ADV-1C | After 1C | adv-scorer | >= 0.92 | Jerry integration feasibility, codebase analysis accuracy, CLI design soundness |
| ADV-1D | After 1D | adv-scorer | >= 0.92 | Requirements completeness, acceptance criteria measurability, traceability to ADR-001 |
| ADV-2 | After 2 | adv-scorer | >= 0.92 | Synthesis methodology, cross-reference accuracy, convergent/divergent finding classification |
| ADV-3A | After 3A | adv-scorer | >= 0.92 | V&V rigor, evidence chain completeness, requirements compliance assessment accuracy |
| ADV-3B | After 3B | adv-scorer | >= 0.92 | Risk identification completeness, likelihood/impact calibration, mitigation feasibility |
| ADV-4 | After 4 | adv-scorer | >= 0.92 | Cross-pollination depth, NSE-ADV convergence quality, gap resolution completeness |
| ADV-5 | After 5 | adv-scorer | >= 0.92 | Trade study methodology, dimension weight justification, bias correction per Addendum A |
| ADV-6 | After 6 | adv-scorer | >= 0.92 | ADR completeness, decision rationale strength, risk documentation, constitutional compliance |
| NSE-REV | After 6 | nse-reviewer | NPR 7123.1D | Technical review: entrance/exit criteria, requirements traceability, risk closure, V&V completeness |

**S-014 Rubric Dimensions (6-dimension weighted composite):**

| Dimension | Weight |
|-----------|--------|
| Completeness | 0.20 |
| Internal Consistency | 0.20 |
| Methodological Rigor | 0.20 |
| Evidence Quality | 0.15 |
| Actionability | 0.15 |
| Traceability | 0.10 |

---

## Cross-Pollination Protocol

### Forward Flow

```
Phase 1A (industry standards)  ──→  Phase 2 (synthesis: evaluation approaches)
Phase 1B (competitive landscape) ──→  Phase 2 (synthesis: market positioning)
Phase 1C (Jerry integration)    ──→  Phase 2 (synthesis: framework fit)
Phase 1D (evaluation criteria)  ──→  Phase 2 (synthesis: requirements alignment)
                                      │
                                      v
                              Phase 3A (V&V: evidence verification)
                              Phase 3B (risk: framework risk assessment)
                                      │
                                      v
                              Phase 4 (cross-pollination: unified findings)
                                      │
                                      v
                              Phase 5 (trade study: quantitative comparison)
                                      │
                                      v
                              Phase 6 (ADR: architecture decision)
```

### Feedback Flow

```
ADV-1A..1D findings  ──→  Phase 2 (address critique in synthesis)
ADV-2 findings       ──→  Phase 3A/3B (verification and risk scope informed by critique)
ADV-3A/3B findings   ──→  Phase 4 (adversary weaknesses feed cross-pollination)
ADV-4 findings       ──→  Phase 5 (critique of cross-pollination informs trade study)
ADV-5 findings       ──→  Phase 6 (trade study critique informs ADR)
ADV-6 + NSE-REV      ──→  COMPLETE or REVISE (dual gate determines acceptance)
```

### Bidirectional NSE <-> ADV Integration

```
/nasa-se (nse-requirements)  ──→  Evaluation criteria inform ADV scoring focus areas
/nasa-se (nse-verification)  ──→  V&V gaps become adversary attack vectors in Phase 4
/nasa-se (nse-risk)          ──→  Risk findings validate adversary-identified weaknesses
/adversary (ADV-1A..3B)      ──→  Adversary critiques feed NSE-ADV convergence in Phase 4
/nasa-se (nse-reviewer)      ──→  Independent technical review validates ADV-6 findings
```

Phase 4 is the convergence point where NSE and ADV findings are synthesized. The cross-pollination synthesis explicitly compares:
- V&V gaps (from nse-verification) against adversary critique findings
- Risk assessments (from nse-risk) against adversary-identified weaknesses
- Requirements compliance (from nse-requirements criteria) against actual coverage

---

## Sync Barriers

| Barrier | Location | Pass Criteria |
|---------|----------|--------------|
| 1 | After Phases 1A + 1B + 1C + 1D | All 4 phases complete. ADV-1A, ADV-1B, ADV-1C, ADV-1D all >= 0.92. |
| 2 | After Phase 2 | Phase 2 complete. ADV-2 >= 0.92. Hand off to Phase 3A AND 3B in parallel. |
| 3 | After Phases 3A + 3B | V&V + Risk complete. Both 3A and 3B complete. ADV-3A and ADV-3B >= 0.92. |
| 4 | After Phase 4 | Cross-pollination complete. ADV-4 >= 0.92. ADV-1A through ADV-3B findings addressed. |
| 5 | After Phase 5 | Trade study complete. ADV-5 >= 0.92. Addendum A bias corrections applied. |
| 6 | Before Phase 6 | User selection input received. All prior artifacts available. |
| 7 | After Phase 6 | Dual gate: ADV-6 >= 0.92 AND NSE-REV passes NPR 7123.1D review. Both must pass. |

---

## State Schema

```yaml
orchestration_state:
  plan_version: "2.3.0"
  project: "PROJ-017"
  pipeline: "promptfoo-deep-analysis-20260303"
  nasa_se_agents: ["nse-requirements", "nse-verification", "nse-risk", "nse-reviewer"]
  phases:
    1A:
      status: "complete"  # pending | in_progress | complete | failed
      agent: "ps-researcher"
      skill: "/problem-solving"
      output: "research/industry-standards-v2.md"
      adv_score: 0.934
      blocked_by: []
    1B:
      status: "complete"
      agent: "pm-competitive-analyst"
      skill: "/pm-pmm"
      output: "research/competitive-landscape.md"
      adv_score: 0.934
      blocked_by: []
    1C:
      status: "complete"
      agent: "ps-researcher"
      skill: "/problem-solving"
      output: "research/jerry-integration-analysis.md"
      adv_score: 0.934
      blocked_by: []
    1D:
      status: "complete"
      agent: "nse-requirements"
      skill: "/nasa-se"
      output: "research/evaluation-criteria.md"
      adv_score: 0.933
      blocked_by: []
    2:
      status: "complete"
      agent: "ps-synthesizer"
      skill: "/problem-solving"
      output: "analysis/synthesized-findings.md"
      adv_score: 0.934  # S-010 self-review; ADV-2 adversarial gate pending
      completed: "2026-03-03"
      blocked_by: []
    3A:
      status: "pending"
      agent: "nse-verification"
      skill: "/nasa-se"
      output: "analysis/verification-report.md"
      adv_score: null
      blocked_by: ["2"]
    3B:
      status: "pending"
      agent: "nse-risk"
      skill: "/nasa-se"
      output: "analysis/risk-assessment.md"
      adv_score: null
      blocked_by: ["2"]
    4:
      status: "pending"
      agent: "ps-synthesizer"
      skill: "/problem-solving"
      output: "analysis/cross-pollination-synthesis.md"
      adv_score: null
      blocked_by: ["3A", "3B"]
    5:
      status: "pending"
      agent: "ps-analyst"
      skill: "/problem-solving"
      output: "analysis/trade-study.md"
      adv_score: null
      blocked_by: ["4"]
    6:
      status: "pending"
      agent: "ps-architect"
      skill: "/problem-solving"
      output: "decisions/ADR-002-quality-framework-selection.md"
      adv_score: null
      nse_review: null
      blocked_by: ["5"]
```

---

## Execution Notes

### Parallel Execution Groups

| Group | Phases | Can Execute Simultaneously |
|-------|--------|--------------------------|
| 1 | 1A + 1B + 1C + 1D | Yes -- all 4 are independent research tasks with no shared dependencies |
| 2 | 3A + 3B | Yes -- V&V and Risk are independent assessments of Phase 2 output |
| 3 | ADV-6 + NSE-REV | Yes -- adversary scoring and technical review are independent evaluations of Phase 6 ADR |

### Context Isolation

Each agent executes in a fresh context (Task tool invocation per P-003). Cross-phase context is passed exclusively through:
- File artifacts (referenced by path, not inline content)
- Key findings (3-5 bullets per handoff)
- Phase 1D evaluation criteria (loaded by Phase 2, 3A, and 4 agents for requirements alignment)

### Session Guidance

Each phase can be executed in a separate session. Resumable components:
- **Phase 1A-1D:** Independent; any can be resumed without the others
- **Phase 2:** Requires all Phase 1 outputs; can be resumed from Phase 1 artifacts
- **Phase 3A/3B:** Independent of each other; both require Phase 2
- **Phase 4:** Requires Phase 2, 3A, 3B, and all ADV findings
- **Phase 5:** Requires Phase 4
- **Phase 6:** Requires Phase 5 + user framework selection input

### Web-Only Research Mandate

All Phase 1 agents MUST use WebSearch + WebFetch (+ Context7 where applicable) for research. NEVER rely on LLM training data for factual claims about tools, pricing, features, or market data. All claims must be web-sourced with URLs.

---

## NASA-SE Integration Summary

| Agent | Phase Placement | Role | Cross-Pollination |
|-------|----------------|------|-------------------|
| nse-requirements | 1D (parallel with 1A-1C) | Define evaluation criteria upfront | Criteria feed Phase 2 ranking, Phase 3A verification, and all ADV gate focus areas |
| nse-verification | 3A (parallel with 3B) | V&V of synthesis against criteria | V&V gaps feed Phase 4 cross-pollination; converge with ADV findings |
| nse-risk | 3B (parallel with 3A) | Risk assessment per framework | Risk register feeds Phase 4; risk quantifies adversary-identified weaknesses |
| nse-reviewer | Phase 6 (parallel with ADV-6) | Independent technical review of ADR | Requirements traceability, risk closure, V&V alignment; converge with ADV-6 |

---

## NPT Constraints

### FORBIDDEN (9 constraints)

1. NEVER use LLM training data as evidence for tool capabilities, pricing, or features -- Consequence: stale or hallucinated data invalidates research. Instead: use WebSearch/WebFetch with URL citations.
2. NEVER skip adversarial quality gates between phases -- Consequence: unreviewed output propagates errors through the pipeline. Instead: run adv-scorer at every phase boundary.
3. NEVER proceed past a sync barrier with ADV score < 0.92 -- Consequence: below-threshold work contaminates downstream phases. Instead: revise until threshold is met or escalate to user.
4. NEVER inline large content in handoffs -- Consequence: context window exhaustion. Instead: use file path references per CP-01.
5. NEVER spawn recursive subagents -- Consequence: P-003 violation, uncontrolled token consumption. Instead: return results to orchestrator.
6. NEVER override user framework selection in Phase 6 -- Consequence: P-020 violation. Instead: present trade study results and await user decision.
7. NEVER misrepresent confidence or evidence quality -- Consequence: P-022 violation. Instead: flag SINGLE-SOURCE findings, mark confidence levels explicitly.
8. NEVER use promptfoo-centric framing in evaluation -- Consequence: bias per Addendum A. Instead: evaluate all options on equal footing with tool-agnostic criteria.
9. NEVER skip the Phase 6 dual gate (both ADV-6 and NSE-REV must pass) -- Consequence: ADR accepted without independent technical review. Instead: execute both gates in parallel; both must pass.

### REQUIRED (7 constraints)

1. MUST cite web URLs for all factual claims about tools, pricing, features.
2. MUST include L0/L1/L2 sections in all research outputs.
3. MUST run adv-scorer (S-014 rubric, 6 dimensions) at every phase boundary.
4. MUST apply Addendum A bias corrections in Phase 5 trade study.
5. MUST load Phase 1D evaluation criteria in Phase 2, 3A, and 4 for requirements alignment.
6. MUST execute Phase 6 dual gate (ADV-6 + NSE-REV) in parallel before acceptance.
7. MUST persist all artifacts to `projects/PROJ-017-llm-skill-testing/` paths.

---

*Plan Version: 2.3.0*
*Source: ADR-001 + Addendum A bias corrections + expanded /nasa-se integration*
*Created: 2026-03-03*
*Skills: /problem-solving, /pm-pmm, /nasa-se, /adversary*
*Agents: ps-researcher, pm-competitive-analyst, ps-synthesizer, nse-requirements, nse-verification, nse-risk, ps-analyst, ps-architect, nse-reviewer, adv-scorer*
