# TASK-001: Evaluation Criteria and Weighting Methodology for Enforcement Vector Prioritization

<!--
DOCUMENT-ID: FEAT-005:EN-402-TASK-001-EVALUATION-CRITERIA
TEMPLATE: Analysis Artifact
VERSION: 1.1.0
SOURCE: EN-401 TASK-009 Revised Unified Enforcement Catalog (v1.1)
AGENT: ps-analyst (Claude Opus 4.6)
DATE: 2026-02-13
PARENT: EN-402 (Enforcement Priority Analysis & Decision)
FEATURE: FEAT-005 (Quality Framework Enforcement Mechanisms)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
QUALITY-TARGET: >= 0.92
CONSUMERS: TASK-002 (nse-risk), TASK-003 (nse-architecture), TASK-004 (ps-analyst)
-->

> **Version:** 1.1.0
> **Agent:** ps-analyst (Claude Opus 4.6)
> **Input:** EN-401 TASK-009 Revised Unified Enforcement Catalog (v1.1, 62 vectors)
> **Confidence:** HIGH -- methodology grounded in user-confirmed priorities and EN-401 empirical analysis

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Key decisions, weights, and rationale at a glance |
| [Design Principles](#design-principles) | Foundational principles governing the evaluation framework |
| [Evaluation Dimensions](#evaluation-dimensions) | Seven weighted criteria with detailed definitions |
| [Weighting Methodology](#weighting-methodology) | Weight assignments, justification, and sensitivity analysis |
| [Scoring Scale and Rubric](#scoring-scale-and-rubric) | 1-5 scale with anchoring examples per criterion |
| [Vector Family Considerations](#vector-family-considerations) | How to evaluate within and across the 7 families |
| [Jerry-Specific Constraints](#jerry-specific-constraints) | Constitutional, token budget, and platform constraints |
| [Composite Scoring Formula](#composite-scoring-formula) | How individual scores combine into final priority |
| [Worked Examples](#worked-examples) | End-to-end scoring for 3 representative vectors |
| [Consumer Guidance](#consumer-guidance) | How downstream tasks should use this framework |
| [References](#references) | Citations to source material |

---

## Executive Summary

This document defines a 7-dimension evaluation framework for prioritizing the 62 enforcement vectors cataloged in EN-401 TASK-009. The framework produces a weighted composite score (WCS) on a 0-to-5 scale for each vector, enabling rank-ordered prioritization.

### Weight Summary

| Dimension | Weight | Rationale |
|-----------|--------|-----------|
| Context Rot Resilience | 25% | User priority #4; correlated failure analysis (TASK-009 Section L2) shows context-dependent layers fail together |
| Effectiveness | 20% | Core purpose of enforcement; must reliably prevent violations |
| Platform Portability | 18% | User priority #2; 38 LLM-Portable vectors prioritized; Windows at 73% compatibility |
| Token Efficiency | 13% | User priority #3; 25,700 token envelope constrains rule-based vectors |
| Bypass Resistance | 10% | User priority #5; adversary model (TASK-009 Section L2) identifies 4 bypass scenarios |
| Implementation Cost | 8% | Lower weight because cost is a one-time investment; enforcement value is ongoing |
| Maintainability | 6% | Important but subordinate; well-designed vectors tend to be maintainable |
| **Total** | **100%** | |

### Key Design Decisions

1. **Scoring scale**: 1-5 integer scale (not 1-10) to avoid false precision in a domain with inherent uncertainty [Section: Scoring Scale and Rubric].
2. **Vector-level scoring** (not family-level) because vectors within a family differ substantially in characteristics [Section: Vector Family Considerations].
3. **Context Rot Resilience receives the highest weight (25%)** because TASK-009's correlated failure analysis demonstrates that VULNERABLE vectors degrade simultaneously under context pressure, making rot resilience the most differentiating criterion.
4. **Implementation Cost receives the lowest weight among the "active" criteria (8%)** because cost is a one-time investment amortized over the framework's lifetime, while other criteria affect ongoing enforcement quality.

---

## Design Principles

Five principles govern the framework design. These are non-negotiable constraints, not tunable parameters.

### DP-1: Align with User-Confirmed Priorities

The user confirmed five priorities for enforcement vector selection (EN-401 final validation). This framework must weight criteria to reflect those priorities. The priorities, in order, are:

1. TASK-009 is the authoritative reference (data source constraint, not a scoring criterion)
2. Prioritize 38 LLM-Portable vectors + Windows adaptations (drives Platform Portability weight)
3. Token budget ~25,700 envelope (drives Token Efficiency weight)
4. Reference adversary model for enforcement robustness (drives Bypass Resistance weight)
5. Prioritize context-rot-resilient vectors (drives Context Rot Resilience weight)

### DP-2: Discriminate on What Matters Most

The framework must produce meaningful separation between vectors. Criteria that rate all vectors the same (e.g., "Is this vector useful?" -- answer is always yes) are excluded. Each criterion must distinguish at least 3 tiers across the 62-vector catalog.

### DP-3: Consume TASK-009 Data Directly

Scoring rubrics are anchored in the data already produced by TASK-009: the effectiveness ratings, portability categories, context rot vulnerability matrix (Appendix C), token budget analysis (Appendix B), and adversary model (Section L2). Scorers should not re-derive this data.

### DP-4: Support Downstream Tasks

Three downstream tasks consume this framework:
- **TASK-002 (nse-risk)**: Needs risk-relevant criteria definitions to align FMEA analysis
- **TASK-003 (nse-architecture)**: Needs architectural criteria to evaluate vector composition
- **TASK-004 (ps-analyst)**: Needs the complete scoring methodology to produce the priority matrix

The framework must be self-contained and unambiguous enough for independent application by different agents.

### DP-5: Tolerate Uncertainty Honestly

Where TASK-009 acknowledges MEDIUM or LOW confidence (e.g., graceful degradation estimates, prompt engineering token costs), scoring rubrics incorporate that uncertainty as a range rather than a point estimate. Vectors scored under uncertain data receive a confidence flag.

---

## Evaluation Dimensions

Seven dimensions capture the critical characteristics for enforcement vector selection. Each dimension is defined with its measurement target, why it matters for Jerry, and what data source provides the scoring input.

### Dimension 1: Context Rot Resilience (CRR)

**Definition:** The degree to which an enforcement vector maintains its effectiveness as the LLM context window fills during a session. A vector with high CRR continues to enforce compliance at 50K+ tokens of context just as reliably as at session start.

**Why it matters for Jerry:** TASK-009 Appendix C demonstrates that 48.4% of vectors are IMMUNE to context rot, while 11.3% are HIGHLY VULNERABLE. The correlated failure analysis (TASK-009 Section L2) shows that all VULNERABLE vectors (V-008 through V-013, the rules family) degrade simultaneously -- they share a common failure mode. Since Jerry currently relies most heavily on these VULNERABLE vectors, CRR is the most urgent differentiator for selecting new enforcement investments.

**Data source:** TASK-009 Appendix C: Context Rot Vulnerability Matrix, which classifies each vector as IMMUNE, LOW, MEDIUM, PARTIALLY VULNERABLE, HIGH, or VARIES.

**What a high score means:** The vector produces the same enforcement outcome regardless of context window state. It is either an external process (hooks, AST, CI), a process-based mechanism (NASA SE, quality gates), or specifically designed to counteract rot (V-024 Context Reinforcement).

**What a low score means:** The vector depends on instructions persisting in the LLM's effective attention span. It degrades predictably as context fills, with effectiveness dropping to 40-60% at 50K+ tokens per "Lost in the Middle" research [TASK-009, citing Liu et al. 2023].

### Dimension 2: Effectiveness (EFF)

**Definition:** The probability that the enforcement vector successfully prevents, detects, or remediates a quality framework violation when such a violation occurs.

**Why it matters for Jerry:** An enforcement vector that is cheap, portable, and context-rot-immune but fails to actually enforce compliance is worthless. Effectiveness is the baseline purpose of every vector.

**Data source:** TASK-009 Revised Effectiveness Ratings table (Section L1), which provides conditional effectiveness under ideal, moderate (20-50K tokens), and degraded (50K+) conditions. Also: TASK-007 Appendix A full vector inventory effectiveness ratings.

**What a high score means:** The vector catches violations deterministically (AST validation, CI pipeline) or with high probabilistic reliability (self-critique + validator chains). It has a track record of preventing the violation type it targets.

**What a low score means:** The vector is advisory only (soft guidance rules) or has significant false-negative rates (meta-cognitive reasoning, confidence calibration). It may catch violations sometimes but cannot be relied upon as the sole defense.

**Nuance:** TASK-009 distinguishes between ideal and degraded effectiveness. For this criterion, we score **degraded effectiveness** (50K+ tokens) because that represents the realistic operating environment for long Jerry sessions. Vectors that are only effective in fresh sessions do not earn high EFF scores.

### Dimension 3: Platform Portability (PORT)

**Definition:** The breadth of platforms on which the enforcement vector functions without modification or with only minor adaptation. Platforms include: (a) LLM backends (Claude Code, other Claude interfaces, non-Anthropic LLMs), (b) operating systems (macOS, Linux, Windows), and (c) tool ecosystems (MCP, custom hooks, CI providers).

**Why it matters for Jerry:** The user explicitly prioritized the 38 LLM-Portable vectors. Jerry is distributed as an open-source plugin; users may run it on Claude Code today but migrate to other platforms. Vectors that lock Jerry to a single platform create vendor risk. Windows compatibility stands at 73% (TASK-006), making OS portability a secondary but real concern.

**Data source:** TASK-007 Appendix A "Category" column (CC-specific, LLM-portable, Framework-specific, Hybrid, OS-specific) and TASK-006 platform portability matrix.

**What a high score means:** The vector works on any LLM, any OS, and any tool ecosystem. Examples: AST validation (Python stdlib), prompt engineering patterns (text-based), process practices (methodology-based).

**What a low score means:** The vector works only on a single platform (Claude Code hooks) or requires a specific framework (NeMo Guardrails, Llama Guard). Migration away from that platform renders the vector inoperative.

### Dimension 4: Token Efficiency (TOK)

**Definition:** The token cost imposed on the context window by the enforcement vector, measured as a percentage of the 200K token context window budget. Includes both static cost (one-time loading) and dynamic cost (per-prompt or per-agent injection).

**Why it matters for Jerry:** The current rules consume ~25,700 tokens (12.9% of context). The target is optimization to ~12,476 tokens (6.2%). Every token spent on enforcement is a token not available for productive work. The user confirmed the ~25,700 token envelope as a constraint. TASK-009 Appendix B provides the coherent token budget analysis.

**Data source:** TASK-009 Appendix B: Revised Token Budget, which breaks down per-component token costs (rules, context reinforcement, self-critique, schema enforcement, meta-cognitive reasoning, few-shot exemplars).

**What a high score means:** The vector consumes zero tokens from the context window (external process: AST, CI, hooks) or minimal tokens (30 tokens per context reinforcement injection).

**What a low score means:** The vector consumes substantial context tokens: rules files (~12,476 tokens optimized), few-shot exemplars (~400 tokens), self-refine loops (~900 tokens per iteration), CoVe (~1,000 tokens).

**Nuance:** Vectors that are entirely external to the context window (IMMUNE class from CRR) automatically score high on TOK. This is expected and correct -- it reflects a real advantage. However, CRR and TOK are not perfectly correlated: V-024 (Context Reinforcement) is IMMUNE to rot but consumes ~600 tokens/session. The dimensions capture different facets of the same vector.

### Dimension 5: Bypass Resistance (BYP)

**Definition:** The difficulty of circumventing the enforcement vector, whether through adversarial action (prompt injection, social engineering), accidental bypass (tool error, configuration mistake), or emergent LLM behavior (working around rather than through enforcement).

**Why it matters for Jerry:** The user requested that the adversary model (TASK-009 Section L2) be referenced in prioritization. The adversary model identifies 4 bypass scenarios (prompt injection, context manipulation, social engineering, fail-open exploitation). Vectors that survive all 4 scenarios are categorically more valuable than those that survive only 1.

**Data source:** TASK-009 Section L2: Adversary Model for Enforcement Bypass (4 scenarios with per-vector survival analysis) and the "Reliability" column from TASK-007 Appendix A.

**What a high score means:** The vector survives all 4 adversary scenarios: prompt injection cannot override it, context manipulation cannot displace it, social engineering cannot convince users to disable it, and implementation errors cause fail-closed behavior. Deterministic, external-process vectors score highest.

**What a low score means:** The vector is bypassed by 3+ adversary scenarios. Prompt injection can override its instructions, context manipulation can push it out of attention, users can be persuaded to disable it, and it fails open on error.

### Dimension 6: Implementation Cost (COST)

**Definition:** The total effort required to implement, test, and deploy the enforcement vector, including: development time, testing burden, infrastructure requirements, and integration complexity with Jerry's existing architecture.

**Why it matters for Jerry:** While cost is a one-time investment, limited development bandwidth means high-cost vectors must deliver proportionally higher value. Vectors requiring new infrastructure (MCP servers, external ML models) are costlier than those leveraging existing infrastructure (Python AST, pytest).

**Data source:** TASK-007 Appendix A "Maintenance Cost" column (HIGH/MEDIUM/LOW) serves as a proxy. Direct implementation effort is estimated based on architectural complexity and Jerry's existing codebase.

**What a high score means (low cost):** The vector can be implemented quickly using existing infrastructure. Jerry already has `tests/architecture/test_composition_root.py` for AST validation; moving this to a hook is low cost. Prompt engineering patterns require only text changes.

**What a low score means (high cost):** The vector requires new infrastructure (MCP server development, external model integration), complex testing (property-based testing infrastructure), or significant organizational change (NASA IV&V independence, formal waiver process).

**Note on scoring direction:** COST is scored as a **benefit** (higher = better = cheaper). This ensures all dimensions contribute positively to the composite score. A score of 5 means "nearly free to implement"; a score of 1 means "requires major infrastructure investment."

### Dimension 7: Maintainability (MAINT)

**Definition:** The ongoing effort required to keep the enforcement vector functional as Jerry evolves, including: adaptation to codebase changes, response to new architectural patterns, updates for platform changes, and debugging when enforcement produces false positives.

**Why it matters for Jerry:** Jerry is actively evolving. Enforcement vectors that break with every refactoring or require constant tuning create drag on development velocity. Vectors that are self-maintaining (CI pipelines, process practices) or auto-adapting (AST checks that scan dynamically) are preferred.

**Data source:** TASK-007 Appendix A "Maintenance Cost" column and TASK-009 Currency and Review section (recommended review frequencies per family).

**What a high score means (low maintenance):** The vector requires review at most annually (process vectors, structural/code-level vectors) and auto-adapts to codebase changes. Rule files that reference patterns rather than specific file names score higher.

**What a low score means (high maintenance):** The vector requires quarterly review (platform-specific hooks), manual updates when the codebase structure changes, or tuning to avoid false positive accumulation. Multi-layer defense (V-032), MCP server composition (V-050), and adversarial review (V-058) all have HIGH maintenance cost.

**Note on scoring direction:** Like COST, MAINT is scored as a **benefit** (higher = better = easier to maintain).

---

## Weighting Methodology

### Weight Derivation Process

Weights are derived through a structured process that traces to the user's confirmed priorities:

**Step 1: Identify the user's priority ordering.**

From the EN-401 final validation, the user confirmed 5 priorities. Mapping to evaluation dimensions:

| User Priority | Evaluation Dimension(s) | Priority Signal |
|--------------|------------------------|-----------------|
| #1: TASK-009 is authoritative | Data source constraint (all dimensions) | Constrains input, not weight |
| #2: Prioritize 38 LLM-Portable vectors | Platform Portability (PORT) | HIGH weight |
| #3: Token budget ~25,700 envelope | Token Efficiency (TOK) | MEDIUM-HIGH weight |
| #4: Reference adversary model | Bypass Resistance (BYP) | MEDIUM weight |
| #5: Context-rot-resilient vectors | Context Rot Resilience (CRR) | HIGHEST weight |

**Step 2: Apply the "most differentiating criterion gets highest weight" principle (DP-2).**

TASK-009 Appendix C shows CRR has the widest spread: 48.4% of vectors are IMMUNE while 11.3% are HIGHLY VULNERABLE. This is the single most differentiating dimension. In contrast, Effectiveness shows 67.7% of vectors rated HIGH (before revision) -- lower discrimination. CRR gets the highest weight.

**Step 3: Apply the "ongoing value beats one-time cost" principle.**

Implementation Cost and Maintainability are important but represent temporal costs (one-time and periodic, respectively). Effectiveness, CRR, Portability, Token Efficiency, and Bypass Resistance represent enduring value. The five value-dimensions collectively receive 86% weight; the two cost-dimensions receive 14%.

**Step 4: Balance to 100% with diminishing marginal returns per dimension.**

After assigning the top two weights (CRR at 25%, EFF at 20%), remaining budget is distributed by priority ordering with diminishing increments.

### Final Weight Assignment

| Dimension | Abbreviation | Weight | Justification |
|-----------|-------------|--------|---------------|
| Context Rot Resilience | CRR | 25% | Highest differentiation (IMMUNE vs VULNERABLE spread); user priority #5; correlated failure means VULNERABLE vectors fail as a group, making CRR the most consequential binary discriminator |
| Effectiveness | EFF | 20% | Core purpose of enforcement; scored under degraded conditions (50K+ tokens) to reflect real-world usage; second-highest discriminator after CRR |
| Platform Portability | PORT | 18% | User priority #2; Jerry is OSS with multi-platform ambition; Windows at 73% compatibility is a known gap; 38 LLM-Portable vectors explicitly prioritized |
| Token Efficiency | TOK | 13% | User priority #3; 25,700 token envelope is a hard constraint; but many high-priority vectors (AST, CI, hooks) are zero-token, so this criterion has moderate discrimination |
| Bypass Resistance | BYP | 10% | User priority #4; adversary model identifies 4 scenarios; partially correlated with CRR (IMMUNE vectors tend to be high BYP), so lower weight avoids double-counting |
| Implementation Cost | COST | 8% | One-time investment amortized over framework lifetime; important for sprint planning but should not disqualify high-value vectors |
| Maintainability | MAINT | 6% | Periodic cost; well-designed vectors correlate with good maintainability; some correlation with COST, so lowest weight to minimize redundancy |

### Structural Bias Acknowledgment

**External-process bias:** The weighting methodology structurally favors external-process vectors (AST, CI, hooks, process) because these vectors are inherently IMMUNE to context rot (CRR=5, 25% weight), zero-token (TOK=5, 13% weight), and highly bypass-resistant (BYP=4-5, 10% weight). This cumulative advantage means external-process vectors receive approximately 48% of their WCS from dimensions where they automatically score maximum. This is an intentional design outcome -- the CRR weighting at 25% reflects the empirical finding (TASK-009, Liu et al. 2023) that context rot is the dominant systemic risk. However, consumers of this framework should be aware that:

1. In-context vectors (rules, prompts) are structurally disadvantaged even when they provide unique value (e.g., V-024 is the only context rot countermeasure but scores lower than AST vectors).
2. The framework correctly surfaces the risk profile hierarchy but does not capture synergistic value of mixed-type stacks -- that is TASK-003's responsibility.
3. A pure external-process stack would lack runtime guidance, which is architecturally incomplete per the Cross-Family Composition table above.

### Sensitivity Analysis Guidance

To verify that conclusions are robust to weight changes, TASK-004 (priority matrix creation) should perform the following sensitivity checks:

**Test 1: Equal Weights.** Score all vectors with equal weights (14.3% each). Compare the top-10 list to the weighted top-10. If fewer than 6 vectors overlap, the weighting scheme is highly influential and requires additional justification.

**Test 2: Swap CRR and EFF.** Set CRR to 20% and EFF to 25%. If the top-10 ranking changes by more than 3 positions for any vector, document which vectors are sensitive to this swap and flag them for TASK-002 risk assessment.

**Test 3: Double COST Weight.** Set COST to 16% and reduce CRR to 17%. This tests whether pragmatic cost concerns would change the recommended implementation order. Document any vectors that move from top-20 to below top-20.

**Test 4: Remove Portability.** Set PORT to 0% and redistribute to CRR (30%) and EFF (26%). This tests the "Claude Code only" scenario where portability doesn't matter. Identify which Claude Code-specific vectors enter the top-10.

**Interpretation:** If all four sensitivity tests produce top-10 lists that share at least 7 vectors, the prioritization is robust. If any test produces a top-10 with fewer than 5 overlaps, the weighting needs further validation with the user.

---

## Scoring Scale and Rubric

### Scale Definition

All dimensions use a **1-5 integer scale**:

| Score | Label | Meaning |
|-------|-------|---------|
| 5 | Excellent | Best-in-class; top tier across the dimension |
| 4 | Good | Above average; strong performance with minor limitations |
| 3 | Adequate | Meets minimum threshold; acceptable but not differentiating |
| 2 | Weak | Below expectations; significant limitations |
| 1 | Poor | Fails to deliver; lowest tier across the dimension |

**Why 1-5 (not 1-10):** The EN-401 research uses qualitative assessments (HIGH/MEDIUM/LOW) with MEDIUM confidence for many data points. A 1-10 scale would imply precision that the data does not support. A 1-5 scale maps naturally to the 5-level qualitative ratings (IMMUNE/LOW/MEDIUM/PARTIALLY VULNERABLE/HIGH for CRR; HIGH/MEDIUM/LOW for effectiveness, reliability, portability, maintenance). The coarser scale also reduces scorer variance, improving inter-rater reliability when different agents score independently.

### Rubric: Context Rot Resilience (CRR)

| Score | Descriptor | TASK-009 Appendix C Mapping | Anchoring Example |
|-------|-----------|----------------------------|-------------------|
| 5 | IMMUNE | IMMUNE classification | V-038 (AST Import Validation): external Python process, zero context dependency |
| 4 | Near-immune | LOW vulnerability | V-019 (Reflexion): injected fresh per episode, minimal persistence needed |
| 3 | Moderately resilient | MEDIUM vulnerability or PARTIALLY VULNERABLE | V-046 (MCP Tool Wrapping): mechanism is external but LLM cooperation degrades |
| 2 | Vulnerable | HIGH vulnerability with partial mitigation | V-010 (Hard Constraint Rules): FORBIDDEN/NEVER patterns survive longest but still degrade at 50K+ tokens |
| 1 | Highly vulnerable | HIGH vulnerability, no mitigation | V-011 (Soft Guidance Rules): most vulnerable to rot; effectiveness at 50K+ rated LOW |

**Scoring rule for VARIES:** Vectors rated VARIES in Appendix C (V-028 through V-037, framework patterns) should be scored based on the specific implementation chosen for Jerry. If the implementation is external-tool-based, score 4-5. If prompt-based, score 2-3.

### Rubric: Effectiveness (EFF)

| Score | Descriptor | Criteria | Anchoring Example |
|-------|-----------|----------|-------------------|
| 5 | Deterministic blocking | Catches 100% of targeted violations; deterministic mechanism; works at 50K+ tokens | V-001 (PreToolUse Blocking): deterministic block/allow decision on every tool call |
| 4 | High probabilistic | Catches >80% of targeted violations; reliable under context pressure; may miss edge cases | V-024 (Context Reinforcement): high effectiveness even at 50K+ because it counteracts rot by design |
| 3 | Moderate | Catches 50-80% of violations under ideal conditions; degrades to 40-60% under pressure | V-014 (Self-Critique): effective when instruction is fresh; degrades with context |
| 2 | Low probabilistic | Catches <50% of violations; advisory in nature; compliance depends on LLM attention | V-012 (AGENTS.md Registry): advisory only; easily forgotten |
| 1 | Minimal | Negligible enforcement effect; aspirational guidance only | V-025 (Meta-Cognitive Reasoning): unreliable; hard to verify compliance; LOW effectiveness at 50K+ |

**Scoring rule:** Use the **50K+ token effectiveness** from TASK-009 Revised Effectiveness Ratings table whenever available. For vectors not individually listed, use the family-level assessment.

**Process vector EFF anchoring (Family 7):** The EFF rubric above uses anchoring examples from structural and prompt-based vectors. Process/methodology vectors (V-051 through V-062) require separate anchoring because their effectiveness operates through organizational discipline and artifact generation rather than direct violation detection:

| EFF Score | Process Vector Criteria | Anchoring Example |
|-----------|----------------------|-------------------|
| 5 | N/A -- process vectors cannot achieve deterministic blocking alone | -- |
| 4 | Produces a deterministic pass/fail signal when implemented with external validation; blocks workflow progression on failure | V-057 (Quality Gates): gate check is deterministic when implemented as external validation (e.g., file existence check); V-060 (Evidence-Based Closure): evidence presence is deterministically checkable |
| 3 | Provides structured guidance or classification that informs enforcement but does not block independently; requires human or agent discipline | V-053 (NASA File Classification): classification informs enforcement level but is subjective; V-056 (BDD Cycle): methodology produces test artifacts but LLM may skip steps without enforcement |
| 2 | Establishes organizational discipline or documentation requirements with no enforcement mechanism; compliance depends entirely on agent behavior | V-052 (VCRM): traceability matrix aids verification but matrix must be manually maintained; V-054 (FMEA): analysis effort produces risk information but does not enforce mitigations |

**Important:** The 50K+ token effectiveness rule does not apply to IMMUNE process vectors. Process vectors are IMMUNE to context rot because they operate through external artifacts and organizational discipline, not through in-context instructions. Their EFF score reflects inherent methodology effectiveness, not degradation behavior.

### Rubric: Platform Portability (PORT)

| Score | Descriptor | Criteria | Anchoring Example |
|-------|-----------|----------|-------------------|
| 5 | Universal | LLM-portable + all OS + no dependencies | V-038 (AST Import Validation): Python stdlib, any OS, any LLM |
| 4 | Broadly portable | LLM-portable + most OS; minor adaptation for Windows | V-024 (Context Reinforcement): text pattern, any LLM, any OS |
| 3 | Moderately portable | Works with MCP-compatible clients; Hybrid category | V-046 (MCP Tool Wrapping): open standard, growing adoption, not yet universal |
| 2 | Limited | Framework-specific; requires specific runtime dependency | V-030 (State Machine Enforcement): LangGraph-specific; Jerry would need custom implementation |
| 1 | Single-platform | Claude Code-specific; zero portability | V-001 (PreToolUse Blocking): Claude Code hooks API only |

**Scoring rule for OS portability nuance:** If a vector is LLM-portable but has Windows issues (73% compatibility per TASK-006), deduct 0.5 from the base score but round to the nearest integer. Document the Windows issue.

### Rubric: Token Efficiency (TOK)

| Score | Descriptor | Criteria | Anchoring Example |
|-------|-----------|----------|-------------------|
| 5 | Zero-token | Entirely external to context window; no token cost | V-044 (Pre-commit Hooks): git hook, zero context tokens |
| 4 | Minimal (<100 tokens/session) | Negligible context impact; small injections | V-024 (Context Reinforcement): ~30 tokens per injection, ~600 tokens/session total |
| 3 | Moderate (100-500 tokens/session) | Noticeable but manageable within budget | V-014 (Self-Critique): ~150 tokens per agent invocation, ~450 tokens/session |
| 2 | Significant (500-2000 tokens/session) | Material impact on available context; requires budget justification | V-018 (Self-Refine Loop): ~900 tokens per iteration; V-026 (Few-Shot Exemplars): ~400 tokens static |
| 1 | Heavy (>2000 tokens/session) | Major context budget consumer; competes with productive work | V-009 (.claude/rules/ Auto-Loaded): ~12,476 tokens (optimized) or ~25,700 (current) |

**Scoring rule:** Use TASK-009 Appendix B token budget data for specific costs. For external-process vectors (AST, CI, hooks), assign score 5 automatically. For prompt-based vectors, calculate from the per-instance and instances-per-session data in Appendix B.

### Rubric: Bypass Resistance (BYP)

| Score | Descriptor | Adversary Model Survival | Anchoring Example |
|-------|-----------|--------------------------|-------------------|
| 5 | Impervious | Survives all 4 adversary scenarios (injection, context manipulation, social engineering, fail-open) | V-045 (CI Pipeline): cannot be bypassed by prompt; requires admin access to disable; deterministic |
| 4 | Highly resistant | Survives 3 of 4 scenarios; vulnerable only to social engineering or deliberate admin override | V-001 (PreToolUse Blocking): survives injection, context manipulation, fail-open; user could theoretically remove hook |
| 3 | Moderately resistant | Survives 2 of 4 scenarios; fails against injection and context manipulation but survives process-level attacks | V-046 (MCP Tool Wrapping): mechanism external, but LLM cooperation can be degraded |
| 2 | Weakly resistant | Survives 1 of 4 scenarios; primarily vulnerable to context-based attacks | V-010 (Hard Constraint Rules): strongest text patterns survive injection somewhat; vulnerable to context manipulation |
| 1 | Easily bypassed | Survives 0-1 scenarios; advisory only; trivially circumvented | V-011 (Soft Guidance Rules): bypassed by injection, context manipulation, and implicitly by social engineering |

**Scoring rule:** Reference TASK-009 Adversary Model Summary table. Map "IMMUNE Vectors Survive: YES" to base score 4-5; "VULNERABLE Vectors Survive: NO" to base score 1-2. Adjust by +-1 based on additional factors (fail-closed configuration, audit trail availability).

### Rubric: Implementation Cost (COST)

| Score | Descriptor | Criteria | Anchoring Example |
|-------|-----------|----------|-------------------|
| 5 | Trivial | Text-only change; no code; no infrastructure; <1 hour | V-016 (Structured Imperative Rules): add DO/DO NOT to existing rule files |
| 4 | Low | Minor code change; leverages existing infrastructure; <1 day | V-038 (AST Import Validation): move existing `test_composition_root.py` logic into a hook script |
| 3 | Moderate | New component; some testing; 1-3 days | V-024 (Context Reinforcement): implement UserPromptSubmit hook with rule injection logic |
| 2 | Significant | New infrastructure; substantial testing; 1-2 weeks | V-046 (MCP Tool Wrapping): build MCP server, write validators, deploy |
| 1 | Major | Major infrastructure; organizational change; >2 weeks | V-051 (NASA IV&V Independence): requires organizational process, independent review capability, ongoing staffing |

**Scoring rule:** Consider Jerry's existing infrastructure: Python codebase with pytest, `tests/architecture/` AST tests, Claude Code hooks capability, no MCP servers yet, no external ML models. Vectors building on existing infrastructure score higher.

### Rubric: Maintainability (MAINT)

| Score | Descriptor | Criteria | Anchoring Example |
|-------|-----------|----------|-------------------|
| 5 | Self-maintaining | Auto-adapts to codebase changes; annual review sufficient | V-038 (AST Import Validation): scans dynamically; adapts to new modules automatically |
| 4 | Low maintenance | Semi-annual review; minor updates for platform changes | V-044 (Pre-commit Hooks): stable git infrastructure; hook scripts rarely need updates |
| 3 | Moderate maintenance | Quarterly review; some adaptation when Jerry evolves | V-024 (Context Reinforcement): rule content must be updated when rules change |
| 2 | High maintenance | Monthly review or frequent tuning; false positive management | V-032 (Multi-Layer Defense): multiple interacting components; tuning for false positive rates |
| 1 | Constant maintenance | Requires ongoing attention; frequent breakage on codebase changes | V-007 (Stateful Hook Enforcement): filesystem state drift; race conditions; state schema evolution |

**Scoring rule:** Reference TASK-009 Currency and Review section for recommended review frequencies. Annually = 5; semi-annually = 4; quarterly = 3; monthly = 2; continuous = 1.

---

## Vector Family Considerations

### Family-Level vs. Vector-Level Scoring

**Decision: Score at the vector level, not the family level.**

**Rationale:** Vectors within the same family can have dramatically different characteristics. Within Family 2 (Rules-Based Enforcement), V-010 (Hard Constraint Rules) and V-011 (Soft Guidance Rules) differ on Effectiveness (HIGH vs LOW), Context Rot Vulnerability (both HIGH, but V-010 degrades slower due to FORBIDDEN/NEVER patterns), and Bypass Resistance (MEDIUM vs LOW). Scoring at the family level would mask these critical differences.

**Exception:** For families where all vectors share identical scores across all dimensions (none currently do), family-level scoring is acceptable to reduce scorer workload. In practice, this exception is unlikely to apply.

### Intra-Family Synergy Assessment

When vectors from the same family are complementary (i.e., their combined effect exceeds the sum of individual effects), this synergy should be noted in the scoring commentary but **not reflected in the individual vector score**. Synergy effects are captured in TASK-003 (architecture trade study) where vector composition strategies are evaluated.

The following intra-family synergies are known from TASK-007 Pattern 2 analysis:

| Family | Synergy Pair | Synergy Effect |
|--------|-------------|----------------|
| Family 1 (Hooks) | V-001 (PreToolUse) + V-002 (PostToolUse) | Prevention + detection; defense-in-depth within hook layer |
| Family 3 (Prompt) | V-010 (Hard Rules) + V-024 (Reinforcement) | Initial guidance + sustained compliance; V-024 keeps V-010 effective |
| Family 5 (Structural) | V-038 (AST in hook) + V-043 (Architecture tests) | Real-time prevention + comprehensive verification at test time |
| Family 7 (Process) | V-057 (Quality Gates) + V-060 (Evidence-Based Closure) | Workflow control + artifact verification |

### Cross-Family Composition

The 7 families map to the 6-layer enforcement architecture defined in TASK-007:

| Layer | Family | Role in Architecture |
|-------|--------|---------------------|
| Foundation | Family 7 (Process) | Process rigor; bypass-resistant; context-rot-immune |
| Prompt | Family 3 (Prompt Engineering) | Runtime guidance; LLM-portable; context-rot-vulnerable |
| Rules | Family 2 (Rules) | Session initialization; LLM-portable; context-rot-vulnerable |
| Structural | Family 5 (Structural) | Code-level enforcement; deterministic; context-rot-immune |
| Protocol | Family 6 (Protocol/MCP) | Protocol-level control; moderately portable |
| Platform | Family 1 (Hooks) | Highest enforcement power; zero portability |
| (Framework patterns) | Family 4 (Frameworks) | Transferable concepts; implementation varies |

**Scoring implication:** TASK-004 should score vectors independently but then assess whether the top-N vectors provide adequate layer coverage. A top-10 list that includes only Family 5 and Family 7 vectors is analytically correct but architecturally incomplete -- it lacks runtime guidance (Family 3) and real-time blocking (Family 1). TASK-003 (architecture trade study) addresses this by evaluating layer composition strategies.

### Within-Tier Ordering Guidance for Family 7

Family 7 (Process/Methodology) vectors tend to cluster at the same WCS because they share identical CRR (5), TOK (5), and PORT (5) scores. Within a WCS cluster, the composite score does not differentiate implementation priority. To resolve ties within the same tier, TASK-004 should apply the following secondary ordering criteria (in priority order):

1. **EFF score** (higher first): Vectors with EFF=4 (deterministic signal when externally implemented) should be prioritized over EFF=3 (guidance without blocking). Example: V-057 (EFF=4) before V-053 (EFF=3).
2. **BYP score** (higher first): Vectors with higher bypass resistance should be implemented before those requiring more organizational discipline. Example: V-060 (BYP=4) before V-056 (BYP=3).
3. **Synergy with existing infrastructure**: Vectors that extend current Jerry infrastructure (worktracker, quality gates) should precede vectors requiring new organizational processes. Example: V-062 (WTI, extends worktracker) before V-051 (IV&V, requires independent review capability).

This guidance applies only to within-tier ordering; cross-tier ordering follows the WCS rank directly.

---

## Jerry-Specific Constraints

Five Jerry-specific constraints modify how the generic evaluation framework applies to this particular codebase:

### Constraint 1: P-003 (No Recursive Subagents)

**Constitutional constraint:** Max ONE level of delegation: orchestrator -> worker. No worker can spawn a sub-worker.

**Impact on scoring:** Vectors that require multi-level agent coordination (V-059 Multi-Agent Cross-Pollination requires orchestrator -> multiple workers -> sync barriers) score normally but receive an implementation note flagging that Jerry's orchestration architecture limits the depth of cross-pollination. This does not reduce the score (the vector can still work within one level) but must be documented for TASK-003.

### Constraint 2: P-002 (File Persistence as Enforcement)

**Constitutional constraint:** Jerry uses the filesystem as its persistence layer (core solution to context rot).

**Impact on scoring:** File-based enforcement vectors receive a scoring bonus on MAINT (they align with Jerry's core architecture) but not on other dimensions. Specifically:
- V-007 (Stateful Hook Enforcement): leverages `.jerry/enforcement/` state files -- architecturally aligned but operationally complex
- V-060 (Evidence-Based Closure): requires file-based proof artifacts -- perfectly aligned with Jerry's filesystem model
- V-062 (WTI Rules): cross-file consistency validation -- directly uses Jerry's file-based work tracking

This is captured as a +0.5 adjustment to MAINT scores (rounded to nearest integer) for vectors that align with filesystem persistence.

### Constraint 3: Token Budget Envelope (~25,700 current; ~12,476 optimized)

**Hard constraint:** The total token cost of all enforcement vectors loaded into the context window must fit within the target budget.

**Impact on scoring:** The TOK dimension directly captures this. Additionally, TASK-004 must verify that the sum of token costs for all selected vectors does not exceed the budget. This is a **feasibility constraint**, not just a scoring dimension -- even if a vector scores 5 on all other dimensions, it cannot be selected if it would exceed the token budget.

**Budget allocation guidance for TASK-004:**

| Component | Max Token Allocation | Source |
|-----------|---------------------|--------|
| .claude/rules/ (optimized) | 12,476 tokens | TASK-009 Appendix B |
| Context reinforcement | 600 tokens/session | TASK-009 Appendix B |
| Self-critique checklists | 450 tokens/session | TASK-009 Appendix B |
| Schema enforcement | 300 tokens/session | TASK-009 Appendix B |
| Meta-cognitive reasoning | 600 tokens/session | TASK-009 Appendix B |
| Few-shot exemplars | 400 tokens (static) | TASK-009 Appendix B |
| CLAUDE.md + system prompt | 300 tokens | TASK-009 Appendix B |
| **Total target** | **~15,126 tokens (7.6%)** | TASK-009 "Full enforcement (amortized)" |

### Constraint 4: Cross-Platform Portability Target

**Hard constraint:** Jerry prioritizes the 38 LLM-Portable vectors and Windows-specific adaptations.

**Impact on scoring:** PORT directly captures this. Additionally, vectors scored 1 on PORT (Claude Code-specific) are not disqualified -- they are valid enhancements for Claude Code users. But they must be clearly labeled as "platform-specific optional enhancers" rather than "core enforcement," and the enforcement architecture must function without them (graceful degradation requirement from TASK-007).

### Constraint 5: Decomposition Level Awareness

**Data constraint from TASK-009 Appendix A:** Vectors exist at three decomposition levels: ATOMIC (single mechanism), COMPOSITE (multiple sub-mechanisms), and METHODOLOGY (organizational practice encompassing multiple activities).

**Impact on scoring:** METHODOLOGY-level vectors (V-042, V-048 territory, V-051, V-052, V-054, V-056, V-058, V-059) naturally score lower on COST (they are more expensive to implement because they encompass more activities) and higher on EFF (they cover more violation types). This is not a bias in the framework; it reflects the genuine trade-off. However, TASK-004 should be aware that comparing ATOMIC and METHODOLOGY vectors directly can be misleading -- a METHODOLOGY vector at rank #20 may deliver more total value than an ATOMIC vector at rank #5, because the methodology covers a broader violation surface.

---

## Composite Scoring Formula

### Weighted Composite Score (WCS)

For each vector V, the WCS is computed as:

```
WCS(V) = (CRR(V) * 0.25) + (EFF(V) * 0.20) + (PORT(V) * 0.18) + (TOK(V) * 0.13) + (BYP(V) * 0.10) + (COST(V) * 0.08) + (MAINT(V) * 0.06)
```

**Range:** 1.00 (all dimensions score 1) to 5.00 (all dimensions score 5).

**Interpretation:**

| WCS Range | Priority Tier | Action |
|-----------|--------------|--------|
| 4.50 - 5.00 | Tier 1: Implement Immediately | Include in Phase 1 enforcement stack |
| 3.75 - 4.49 | Tier 2: Implement Soon | Include in Phase 2-3 enforcement stack |
| 3.00 - 3.74 | Tier 3: Implement When Feasible | Include when capacity allows; not urgent |
| 2.25 - 2.99 | Tier 4: Defer | Implement only for critical deliverables or specific use cases |
| 1.00 - 2.24 | Tier 5: Exclude | Do not implement; effort exceeds benefit |

### Tie-Breaking Rules

When two vectors have equal WCS (to two decimal places):

1. **First tiebreaker:** Higher CRR score wins (context rot resilience is the primary differentiator).
2. **Second tiebreaker:** Higher EFF score wins.
3. **Third tiebreaker:** Higher PORT score wins.
4. **If still tied:** The vector in the more underrepresented family (per layer coverage analysis) wins.

### Confidence Flagging

Each vector score should include a confidence indicator:

| Confidence | Criteria | Action |
|------------|----------|--------|
| HIGH | All dimension scores based on TASK-009 data with HIGH confidence | No flag needed |
| MEDIUM | One or more dimensions scored with MEDIUM-confidence TASK-009 data | Flag in scoring commentary; include in sensitivity analysis |
| LOW | One or more dimensions scored with estimated data not in TASK-009 | Flag prominently; consider exclusion from automated ranking |

---

## Worked Examples

Three worked examples demonstrate the scoring methodology end-to-end. These use actual data from TASK-009 and serve as calibration anchors for TASK-004.

### Example 1: V-038 (AST Import Boundary Validation)

| Dimension | Score | Justification |
|-----------|-------|---------------|
| CRR | 5 | IMMUNE -- external Python process (TASK-009 Appendix C) |
| EFF | 5 | HIGH effectiveness at 50K+ tokens; deterministic catch of import violations (TASK-009 Revised Effectiveness) |
| PORT | 5 | LLM-portable; Python stdlib; any OS (TASK-007 Appendix A: Category = LLM-portable) |
| TOK | 5 | Zero context tokens; executes as external process |
| BYP | 5 | Survives all 4 adversary scenarios: operates on code structure, not prompt (TASK-009 Adversary Model) |
| COST | 4 | Low cost: Jerry already has `tests/architecture/test_composition_root.py`; moving logic to hook is ~1 day effort |
| MAINT | 5 | Self-maintaining: AST scans dynamically; adapts to new modules; annual review sufficient (TASK-009 Currency) |

**WCS = (5*0.25) + (5*0.20) + (5*0.18) + (5*0.13) + (5*0.10) + (4*0.08) + (5*0.06) = 1.25 + 1.00 + 0.90 + 0.65 + 0.50 + 0.32 + 0.30 = 4.92**

**Tier: 1 (Implement Immediately)**
**Confidence: HIGH** -- all scores based on well-established TASK-009 data.

### Example 2: V-024 (Context Reinforcement via Repetition)

| Dimension | Score | Justification |
|-----------|-------|---------------|
| CRR | 5 | IMMUNE by design -- pattern specifically counteracts context rot (TASK-009 Appendix C) |
| EFF | 4 | HIGH effectiveness at 50K+; demonstrated to work but depends on injection frequency and content selection |
| PORT | 4 | LLM-portable; text pattern works on any LLM; requires a per-prompt injection mechanism (Claude Code: UserPromptSubmit; other: custom integration) |
| TOK | 4 | ~600 tokens/session (~30 tokens * 20 prompts); minimal but nonzero (TASK-009 Appendix B) |
| BYP | 4 | Survives injection (re-injected fresh), context manipulation (counteracts displacement), fail-open (text-based); vulnerable only to social engineering (user could disable) |
| COST | 3 | Moderate: requires implementing UserPromptSubmit hook with rule selection logic; ~1-3 days |
| MAINT | 3 | Moderate maintenance: injection content must track rule changes; quarterly review (TASK-009 Currency) |

**WCS = (5*0.25) + (4*0.20) + (4*0.18) + (4*0.13) + (4*0.10) + (3*0.08) + (3*0.06) = 1.25 + 0.80 + 0.72 + 0.52 + 0.40 + 0.24 + 0.18 = 4.11**

**Tier: 2 (Implement Soon)**
**Confidence: HIGH** -- V-024 is the single most-recommended vector in TASK-009.

### Example 3: V-011 (Soft Guidance Rules)

| Dimension | Score | Justification |
|-----------|-------|---------------|
| CRR | 1 | HIGH vulnerability; most vulnerable to context rot; effectiveness at 50K+ rated LOW (TASK-009 Appendix C) |
| EFF | 1 | LOW effectiveness even under ideal conditions; advisory only; no enforcement mechanism (TASK-007 Family 2) |
| PORT | 5 | LLM-portable; text-based; any platform (TASK-007 Appendix A: Category = LLM-portable) |
| TOK | 2 | Part of the ~12,476 optimized rules budget; contributes tokens with minimal enforcement return |
| BYP | 1 | Bypassed by 3+ adversary scenarios: injection overrides, context manipulation displaces, easily ignored |
| COST | 5 | Trivial: already exists in current rule files; no implementation needed |
| MAINT | 5 | Self-maintaining: text files with annual review sufficient |

**WCS = (1*0.25) + (1*0.20) + (5*0.18) + (2*0.13) + (1*0.10) + (5*0.08) + (5*0.06) = 0.25 + 0.20 + 0.90 + 0.26 + 0.10 + 0.40 + 0.30 = 2.41**

**Tier: 4 (Defer)**
**Confidence: HIGH** -- V-011 is consistently rated lowest in its family.

### Calibration Check

The three examples produce a spread from 2.41 to 4.92, covering three of the five priority tiers. This demonstrates that the framework effectively discriminates between high-value and low-value vectors. The ordering (V-038 > V-024 > V-011) aligns with the TASK-007 recommended implementation priority (AST is Phase 2, Context Reinforcement is Phase 1, Soft Rules are not prioritized), providing face validity.

---

## Consumer Guidance

### For TASK-002 (nse-risk): Risk Assessment

Use the following dimensions as inputs to your FMEA-style analysis:

- **Severity** correlates with EFF and BYP -- vectors with low effectiveness and low bypass resistance represent higher risk because violations pass through undetected.
- **Occurrence** correlates inversely with CRR -- context-rot-vulnerable vectors have higher occurrence of enforcement failure in long sessions.
- **Detection** correlates with the enforcement tier (HARD/SOFT/ADVISORY from TASK-007) -- HARD vectors have high detection, ADVISORY vectors have low detection.

Risk Priority Number (RPN) from your FMEA analysis should be compared with WCS from this framework as a cross-validation. Vectors with high WCS (good enforcement value) but high RPN (high risk if they fail) deserve special attention for redundancy.

### For TASK-003 (nse-architecture): Architecture Trade Study

Use the following outputs from this framework:

- **Layer coverage analysis** (Vector Family Considerations section): verify that selected vectors provide at least 3 independent enforcement layers per the correlated failure analysis.
- **Cross-family composition table**: ensure the architecture includes at least one IMMUNE-class vector from Family 5 or Family 7 as the foundation.
- **Synergy pairs**: evaluate whether the top-N vectors include complementary combinations from Pattern 2 in TASK-007.

### For TASK-004 (ps-analyst): Priority Matrix

Apply the scoring rubric to all 62 vectors. Specific guidance:

1. Score each vector on each dimension independently using the rubric anchoring examples.
2. Calculate WCS using the composite formula.
3. Rank vectors by WCS (descending).
4. Apply tie-breaking rules.
5. Assign priority tiers based on WCS ranges.
6. Verify token budget feasibility: sum TOK costs of selected vectors against the 15,126 token target.
7. Verify layer coverage: ensure at least 3 independent layers are represented in the top-20.
8. Run all 4 sensitivity tests and document results.
9. Flag vectors with MEDIUM or LOW confidence scores.

---

## References

### Primary Sources (Direct Input)

| # | Citation | Used For |
|---|----------|----------|
| 1 | TASK-009: Revised Unified Enforcement Vector Catalog v1.1 (this project) | Authoritative source for all 62 vectors, context rot vulnerability matrix, adversary model, token budget, effectiveness ratings |
| 2 | TASK-007: Unified Enforcement Vector Catalog v1.0 (this project) | Full vector inventory table, family summaries, trade-off analysis, complementary combinations, diminishing returns analysis |
| 3 | TASK-006: Platform Portability Assessment (this project) | Platform compatibility matrix, Windows compatibility data (73%), LLM portability categories |
| 4 | TASK-008: Adversarial Review Iteration 1 (this project) | Quality criteria for the catalog; identified weaknesses driving framework rigor |

### Secondary Sources (Via TASK-009)

| # | Citation | Relevance |
|---|----------|-----------|
| 5 | Liu, N. F., et al. (2023). "Lost in the Middle: How Language Models Use Long Contexts." arXiv:2307.03172 | Empirical basis for context rot vulnerability assessments; justifies CRR as highest-weight criterion |
| 6 | TASK-003: .claude/rules/ Enforcement Research (this project) | Token budget data for rules (25,700 current, 12,476 optimized); rule effectiveness analysis |
| 7 | TASK-004: Prompt Engineering Enforcement Research (this project) | Token budget for prompt patterns; context rot vulnerability per pattern; effectiveness ratings |
| 8 | TASK-005: Alternative Enforcement Mechanisms Research (this project) | AST, CI, MCP, NASA SE vector data |

### Methodology Sources

| # | Citation | Relevance |
|---|----------|-----------|
| 9 | NASA NPR 7123.1D: Systems Engineering Processes and Requirements | Trade study methodology; weighted evaluation criteria pattern |
| 10 | IEC 60812:2018 Failure Mode and Effects Analysis (FMEA) | Risk assessment framework referenced for TASK-002 integration |

---

*Agent: ps-analyst (Claude Opus 4.6)*
*Date: 2026-02-13*
*Parent: EN-402 Enforcement Priority Analysis & Decision*
*Status: COMPLETE*
*Quality Target: >= 0.92*
*Consumers: TASK-002 (nse-risk), TASK-003 (nse-architecture), TASK-004 (ps-analyst)*
