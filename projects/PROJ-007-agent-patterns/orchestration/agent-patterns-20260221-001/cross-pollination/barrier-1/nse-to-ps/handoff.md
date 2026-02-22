# Barrier 1 Cross-Pollination: NSE Pipeline -> PS Pipeline

<!-- HANDOFF: barrier-1 | DIRECTION: nse-to-ps | DATE: 2026-02-21 -->

> Synthesized findings from NASA SE Phase 1 Research (nse-explorer-001 trade study) for consumption by Problem-Solving Phase 2 Analysis agents (ps-analyst-001, ps-analyst-002, ps-investigator-001).

## Document Sections

| Section | Purpose |
|---------|---------|
| [Key Findings Summary](#key-findings-summary) | Critical trade study outcomes |
| [Trade Study Results](#trade-study-results) | All 5 trade study winners and scoring |
| [Jerry Pattern Validation](#jerry-pattern-validation) | Where Jerry is already strong |
| [Improvement Opportunities](#improvement-opportunities) | Highest-value evolutionary enhancements |
| [Evaluation Criteria Used](#evaluation-criteria-used) | Weighted criteria per NPR 7123.1D |
| [PS Phase 2 Guidance](#ps-phase-2-guidance) | Specific inputs for each PS agent |

---

## Key Findings Summary

### Bottom Line

Jerry's existing agent patterns are **architecturally sound and ahead of industry norms** in several areas (quality assurance, agent definition richness). The trade studies recommend **evolutionary enhancements**, not architectural rewrites. The three highest-value improvements are:

1. **Schema validation** for agent definitions and outputs (TS-2, TS-4 winner deltas)
2. **Layered routing** with LLM fallback for ambiguous cases (TS-3 winner delta)
3. **Standardized state management** across agent handoffs (TS-1 recommendation)

### Trade Study Scope

5 trade studies covering 27 total alternatives evaluated across 6 weighted criteria per NPR 7123.1D Process 17 (Decision Analysis), with 34 referenced sources.

---

## Trade Study Results

### TS-1: Agent Architecture Alternatives (5 alternatives)

| Rank | Alternative | Score |
|------|------------|-------|
| 1 | **A3: Skill-Based Specialist (Jerry's current)** | **4.25** |
| 2 | A5: Hierarchical Agent Teams | 3.75 |
| 3 | A4: Event-Driven Reactive | 3.50 |
| 4 | A2: Microservice Agent | 3.25 |
| 5 | A1: Monolithic Agent | 2.45 |

**Verdict:** Jerry's skill-based specialist architecture **wins**. Enhancement opportunity: stronger state management between agents.

### TS-2: Agent Definition Format Alternatives (5 alternatives)

| Rank | Alternative | Score |
|------|------------|-------|
| 1 | **B5: Hybrid Schema-Validated Markdown** | **4.45** |
| 2 | B1: YAML Frontmatter + Markdown Body (Jerry's current) | 4.00 |
| 3 | B4: Custom DSL | 3.40 |
| 4 | B2: Pure YAML/JSON | 3.25 |
| 5 | B3: Code-First (Python classes) | 3.15 |

**Verdict:** Jerry's current YAML+MD format is strong (rank 2). Adding **schema validation** elevates it to the winner (B5). Delta: +0.45 points.

### TS-3: Agent Routing Architecture Alternatives (6 alternatives)

| Rank | Alternative | Score |
|------|------------|-------|
| 1 | **C5: Layered (Keyword + LLM fallback)** | **3.90** |
| 2 | C1: Keyword/Pattern (Jerry's current) | 3.85 |
| 3 | C4: Decision Tree with Scoring | 3.80 |
| 4 | C6: Intent Classification | 3.75 |
| 5 | C3: LLM-as-Router | 3.10 |
| 6 | C2: Semantic/Embedding | 2.90 |

**Verdict:** Jerry's keyword-based routing is competitive (rank 2). Adding **LLM fallback** for ambiguous cases yields best overall approach. Delta: +0.05 points. Small delta suggests keyword-first is a strong foundation.

### TS-4: Quality Assurance Architecture Alternatives (6 alternatives)

| Rank | Alternative | Score |
|------|------------|-------|
| 1 | **D6: Layered QA (Schema + Self-Review + Critic)** | **3.70** |
| 2 | D2: Creator-Critic (Jerry's current base) | 3.30 |
| 3 | D3: Tournament Multi-Strategy (Jerry's C4 mode) | 3.25 |
| 4 | D4: Statistical Sampling | 3.05 |
| 5 | D5: Schema-Based Output Validation | 2.80 |
| 6 | D1: Self-Review Only | 2.50 |

**Verdict:** Jerry's creator-critic + tournament system is strong. Adding **lightweight schema validation as a deterministic pre-check** before LLM-based QA creates the optimal layered approach. Delta: +0.40 points.

### TS-5: Tool Integration Architecture Alternatives (5 alternatives)

| Rank | Alternative | Score |
|------|------------|-------|
| 1 | **E1: Static Assignment (Jerry's current)** | **4.15** |
| 2 | E5: Hybrid (Static + Capability Discovery) | 3.90 |
| 3 | E3: Capability-Based Matching | 3.45 |
| 4 | E4: MCP Federation | 3.20 |
| 5 | E2: Dynamic Discovery | 2.80 |

**Verdict:** Jerry's static tool assignment **wins**. MCP provides the standard protocol layer. Dynamic discovery reserved for future evolution.

---

## Jerry Pattern Validation

The following Jerry patterns were validated as **architecturally optimal or near-optimal** by the trade studies:

| Jerry Pattern | Trade Study | Rank | Assessment |
|--------------|------------|------|------------|
| Skill-Based Specialist Architecture | TS-1 | 1st | Optimal |
| YAML+MD Agent Definitions | TS-2 | 2nd | Near-optimal (add schema validation) |
| Keyword-Based Routing | TS-3 | 2nd | Near-optimal (add LLM fallback) |
| Creator-Critic + Tournament QA | TS-4 | 2nd/3rd | Strong (add schema pre-check) |
| Static Tool Assignment | TS-5 | 1st | Optimal |
| Single-Level Nesting (P-003) | TS-1 | N/A | Validated by all industry leaders |
| Progressive Disclosure (Skills) | TS-2 | N/A | Validated by Anthropic, production-ready |
| Filesystem-as-Memory | TS-1 | N/A | Validated as context rot mitigation |

---

## Improvement Opportunities

Ranked by trade study score delta and implementation effort:

| Priority | Enhancement | Delta | Effort | Trade Study |
|----------|------------|-------|--------|-------------|
| **HIGH** | Schema validation for agent definitions | +0.45 | Medium | TS-2 |
| **HIGH** | Schema validation as QA pre-check | +0.40 | Medium | TS-4 |
| **MEDIUM** | LLM fallback for ambiguous routing | +0.05 | Low | TS-3 |
| **MEDIUM** | Standardized state management for handoffs | N/A | Medium | TS-1 |
| **LOW** | Capability discovery for dynamic tools | N/A | High | TS-5 |

---

## Evaluation Criteria Used

All trade studies used these 6 weighted criteria per NPR 7123.1D:

| ID | Criterion | Weight | Rationale |
|----|-----------|--------|-----------|
| C1 | Simplicity | 0.20 | Reduces cognitive load, fights context rot |
| C2 | Flexibility | 0.20 | Jerry serves 37 agents across 8 skills |
| C3 | Maintainability | 0.20 | Framework longevity |
| C4 | Quality Control | 0.15 | Core Jerry differentiator (H-13 to H-19) |
| C5 | Context Efficiency | 0.15 | Context rot is Jerry's core problem |
| C6 | P-003 Compliance | 0.10 | Constitutional hard constraint |

---

## PS Phase 2 Guidance

### For ps-analyst-001 (Pattern Categorization)

Use these trade study results to:
- **Categorize current Jerry patterns** against the 8 pattern families from ps-researcher-003, informed by trade study validation scores
- **Identify gaps** where Jerry lacks coverage vs. industry best practices, focusing on the 3 high-priority enhancements (schema validation x2, LLM routing fallback)
- **Map pattern maturity** using the trade study scoring as a quantitative baseline
- **Prioritize gap closure** by delta score -- larger deltas = higher impact improvements

### For ps-analyst-002 (Routing Trade-offs)

Use these trade study results to:
- **Analyze TS-3 results in depth** -- the small delta (+0.05) between keyword-only and layered routing suggests careful cost-benefit analysis is needed
- **Evaluate routing complexity vs. benefit** -- is the LLM fallback worth the added complexity for Jerry's current 8-skill scope?
- **Consider scaling trajectory** -- at what skill count (15? 20? 30?) does layered routing become essential?
- **Design the decision framework** for when to route via keyword vs. when to escalate to LLM

### For ps-investigator-001 (Failure Modes)

Use these trade study results to investigate:
- **Context rot failure modes** -- how does agent performance degrade at different context fill levels?
- **Handoff failure modes** -- map the free-text handoff failure chain (identified as #1 failure source)
- **Routing failure modes** -- keyword overlap, false negatives, ambiguous inputs, routing loops
- **Quality gate bypass modes** -- how could the creator-critic cycle be circumvented or produce false positives?
- **Error amplification** -- the "Bag of Agents" 17x amplification effect; how does this manifest in Jerry's architecture?
- **Anti-patterns from TS-1 through TS-5** -- each losing alternative represents a failure mode if accidentally adopted
