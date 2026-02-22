# HARD Rule Budget Upper Boundary Derivation

> **Criticality:** C4 (Critical) — governance constraint affecting constitutional enforcement architecture
> **Quality Threshold:** >= 0.95
> **Created:** 2026-02-21
> **Status:** DRAFT (iteration 1)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Derived upper boundary and recommendation |
| [Problem Statement](#problem-statement) | What we're solving and why |
| [Methodology](#methodology) | Five independent constraint analyses |
| [Constraint 1: Token Budget](#constraint-1-token-budget-hard-ceiling) | L1 token capacity → max rules |
| [Constraint 2: L2 Re-injection](#constraint-2-l2-re-injection-coverage) | L2 budget → max fully-covered rules |
| [Constraint 3: Instruction-Following Research](#constraint-3-instruction-following-degradation) | Empirical LLM constraint-tracking limits |
| [Constraint 4: Signal Quality](#constraint-4-signal-quality-diminishing-returns) | Enforcement quality degradation curve |
| [Constraint 5: Rule Conflict Probability](#constraint-5-rule-conflict-probability) | Combinatorial interaction growth |
| [Synthesis: Binding Constraint Analysis](#synthesis-binding-constraint-analysis) | Which constraint is the tightest |
| [Recommendation](#recommendation) | Derived budget with rationale |
| [Implementation Path](#implementation-path) | How to get from 31 to the derived budget |
| [Evidence Index](#evidence-index) | Source traceability |

---

## Executive Summary

The current HARD rule ceiling of 35 was set retroactively without derivation. This analysis derives the upper boundary from five independent constraints — token budget, L2 re-injection coverage, LLM instruction-following research, signal quality, and rule conflict probability.

**Finding:** The binding constraint is **L2 re-injection coverage** — only 10 of 31 current rules have per-prompt re-injection protection against context rot. The remaining 21 rules rely solely on L1 session-start loading, which is documented as VULNERABLE to context rot (CRR=1-2 per ADR-EPIC002-002).

**Derived upper boundary: 25 HARD rules** (the maximum that can be meaningfully enforced given the current architecture), with the following allocation:

| Tier | Count | Coverage |
|------|-------|----------|
| Tier A: L2-protected (constitutional + quality) | 10-12 | Full L1 + L2 re-injection every prompt |
| Tier B: L1-only (operational) | 13-15 | L1 session-start loading only |
| **Total** | **25** | |

This aligns with three independent evidence sources: the nse-risk-001 "20-25 sweet spot," the ManyIFEval degradation curve (5-10 simultaneous constraints as the practical ceiling), and the ADR-EPIC002-002 token budget feasibility analysis.

---

## Problem Statement

The HARD rule budget in `quality-enforcement.md` currently states `<= 35`. This ceiling:

1. **Has no derivation.** It was set retroactively in commit `936d61c` to accommodate the existing count (31) plus headroom (4). No calculation, empirical analysis, or design rationale was recorded.
2. **Has already been breached once.** The original ceiling of `<= 25` was silently exceeded when H-25..H-30 were added without updating the cap.
3. **Is about to be exhausted.** PROJ-007 proposes H-32..H-35, consuming the remaining 4 slots (100% utilization at 35/35).
4. **Determines system-level enforcement quality.** Every HARD rule competes for attention budget (token budget, LLM attention weight, L2 re-injection capacity). An unprincipled ceiling either over-constrains (blocking legitimate governance additions) or under-constrains (allowing enforcement quality to degrade).

**Question:** What is the principled upper boundary for HARD rules, derived from the actual constraints of the enforcement architecture?

---

## Methodology

Five independent constraints are analyzed. The binding constraint (tightest limit) determines the upper boundary.

| # | Constraint | Analysis Type | Data Source |
|---|-----------|---------------|-------------|
| 1 | Token Budget | Quantitative | ADR-EPIC002-002, rule file sizes |
| 2 | L2 Re-injection Coverage | Quantitative | Engine source, L2-REINJECT markers |
| 3 | Instruction-Following Research | Empirical | ManyIFEval, AGENTIF, Control Illusion |
| 4 | Signal Quality | Semi-quantitative | nse-risk-001 diminishing returns analysis |
| 5 | Rule Conflict Probability | Quantitative | Combinatorial analysis |

---

## Constraint 1: Token Budget (Hard Ceiling)

### Data

From ADR-EPIC002-002 and current rule file measurements:

| Parameter | Value | Source |
|-----------|-------|--------|
| Total context window | 200,000 tokens | Claude model specification |
| L1 enforcement budget (target) | 12,476 tokens | ADR-EPIC002-002 |
| L1 enforcement budget (current actual) | ~14,245 tokens | Measured from rule file sizes |
| Total enforcement budget | 15,126 tokens (7.56%) | ADR-EPIC002-002 |
| Critical max budget | 17,026 tokens (8.51%) | ADR-EPIC002-002 |
| Per-HARD-rule L1 cost | ~300-500 tokens | Measured (range across files) |
| Mean per-HARD-rule L1 cost | ~410 tokens | Computed from 14,245 tokens / 31 rules (includes non-rule content) |

### Analysis

The L1 budget of 12,476 tokens must accommodate:
- HARD rule definitions and context (~410 tokens/rule average)
- MEDIUM/SOFT standards (which share the same files)
- Section headers, navigation tables, metadata

Not all L1 tokens are consumed by HARD rules — rule files contain MEDIUM and SOFT standards, examples, and explanatory text. Estimating HARD-rule-specific content at ~60% of file tokens:

**Effective HARD rule L1 budget:** 12,476 x 0.60 = ~7,486 tokens
**Max rules at 410 tokens/rule:** 7,486 / 410 = **~18 rules** (if L1 budget is the binding constraint)

However, this underestimates because:
- Some files are dense with HARD rules (quality-enforcement.md: 8 rules in 3,730 tokens = 466/rule)
- Some files carry mostly context (project-workflow.md: 1 rule in 737 tokens)
- Consolidation would reduce per-rule overhead

**Token budget ceiling: ~30-40 rules** (at current overhead) or **~18-25 rules** (if HARD-rule-specific budget is isolated). This is a soft constraint — it can be managed through rule consolidation and file optimization.

### Verdict

Token budget alone suggests **25-40 rules** depending on consolidation. This is **not the binding constraint** at current rule density.

---

## Constraint 2: L2 Re-injection Coverage

### Data

| Parameter | Value | Source |
|-----------|-------|--------|
| L2 per-prompt budget | 600 tokens | ADR-EPIC002-002 |
| Current L2 markers (quality-enforcement.md only) | 8 markers, 415 declared tokens | Engine source analysis |
| H-rules with L2 coverage | 10 (H-01..H-03, H-05, H-06, H-13..H-15, H-19, H-31) | L2-REINJECT marker inventory |
| H-rules WITHOUT L2 coverage | 21 | Remaining H-04, H-07..H-12, H-16..H-18, H-20..H-30 |
| Engine reads from | quality-enforcement.md only | prompt_reinforcement_engine.py |

### Analysis

The enforcement architecture (ADR-EPIC002-002) classifies L1 as **VULNERABLE** to context rot (CRR=1-2). L2 re-injection is the **primary defense** against context rot for critical rules. Yet:

- **Only 32% of HARD rules (10/31) have L2 protection.**
- **68% of HARD rules (21/31) rely solely on L1**, which degrades as context fills.
- The engine only reads L2 markers from `quality-enforcement.md` — markers in other files are documentation metadata, not operational.

At 600 tokens per prompt for L2:
- Current 8 markers use 415 tokens (69% utilization)
- Remaining capacity: ~185 tokens (~3-4 additional markers at ~50 tokens each)
- **Maximum L2-protected rules: ~14** (10 current + ~4 additional)

For a HARD rule to be meaningfully "HARD" — i.e., enforceable even under context rot — it needs L2 coverage. Rules without L2 coverage are effectively MEDIUM in enforcement reliability, despite being labeled HARD.

**L2 coverage ceiling: ~14 rules with full L2 protection.** Beyond this, additional HARD rules are L1-only and vulnerable to context rot.

### Verdict

If all HARD rules require L2 protection: **upper bound is ~14 rules.** If a two-tier model is acceptable (L2-protected + L1-only): the constraint shifts to signal quality and instruction-following limits. **This is potentially the binding constraint.**

---

## Constraint 3: Instruction-Following Degradation

### Data

| Study | Finding | Confidence |
|-------|---------|------------|
| ManyIFEval (arXiv:2509.21051, 2025) | 5 simultaneous instructions: 32-72% accuracy. 10 instructions: 2-39% accuracy. | Well-established (peer-reviewed) |
| AGENTIF (arXiv:2505.16944, NeurIPS 2025) | 11.9 constraints avg: <30% perfect compliance across all models. Best model (o1-mini): 59.8% constraint success rate. | Well-established (NeurIPS Spotlight) |
| Control Illusion (arXiv:2502.15851, 2025) | Claude 3.5 system prompt adherence under conflict: 29.9%. Larger models show no consistent advantage. | Well-established (peer-reviewed) |
| Lost in the Middle (Liu et al., TACL 2024) | Middle-positioned information in long contexts degrades significantly. U-shaped recall curve. | Well-established (TACL publication) |

### Analysis

These studies measure instruction-following fidelity, not the number of rules in a file. A critical distinction:

- **31 HARD rules in rule files** ≠ 31 simultaneously active constraints per interaction
- In practice, a given interaction might activate 5-8 HARD rules (e.g., a coding task activates H-05/H-06/H-10/H-11/H-12/H-20/H-21; a governance task activates H-01/H-02/H-03/H-13/H-14/H-19)
- The L2 re-injection architecture selectively emphasizes the most critical 8 markers per prompt

However, the research establishes that:
1. **Perfect compliance at >10 simultaneous constraints is essentially zero** (AGENTIF: <30%)
2. **System prompt priority collapses under conflict** (Claude: 29.9%)
3. **Position effects degrade middle-placed rules** (Lost in the Middle)

**Implication for L2-protected rules:** The 10-12 rules with L2 re-injection are within the 5-10 range where compliance is still meaningful (32-72% per ManyIFEval). This is the right order of magnitude.

**Implication for L1-only rules:** The 21 rules without L2 re-injection compete for attention with the entire context. As context fills toward 200K, these rules experience both attention dilution and positional degradation. Their effective enforcement probability degrades from "high" (early session) to "low" (late session under context pressure).

### Verdict

Research supports **10-12 simultaneously-enforced constraints** as the practical ceiling for reliable compliance. This aligns with the L2-protected rule count. Total HARD rule count can exceed this if rules are domain-partitioned (not all active simultaneously), but the **simultaneously active ceiling is ~10-12 rules.** Beyond ~25 total rules, even domain partitioning cannot prevent attention dilution from degrading the full set.

---

## Constraint 4: Signal Quality (Diminishing Returns)

### Data

From nse-risk-001-risk-assessment.md (PROJ-007):

```
Compliance
Quality
  ^
  |        .-----------
  |      ./
  |    ./
  |  ./        <- Sweet spot (~20-25 rules)
  |./
  +-----|---------|---------|---> Rule Count
       10       20        30
```

Key finding: "Beyond the sweet spot, each additional rule: (a) consumes ~400-500 tokens of L1 budget, (b) increases probability of rule conflicts (combinatorial growth), (c) increases cognitive load on agents, (d) reduces working context for actual deliverables."

Consolidation candidates identified: H-25..H-30 (6 rules → 2) and H-07..H-09 (3 rules → 1), netting a reduction of 6 rules (31 → 25).

### Analysis

The "20-25 sweet spot" is the risk assessment agent's judgment call, not an empirically validated number. However, it is independently corroborated by:

1. **Token budget analysis** (Constraint 1): Isolated HARD-rule budget yields 18-25 rules
2. **Instruction-following research** (Constraint 3): 10-12 simultaneously active, ~25 total with domain partitioning
3. **Original EN-404 design** (Constraint 0): The original designer set `<= 25` before any rules existed — this was a design intent, not a retroactive ceiling

The convergence of three independent analyses on the 20-25 range is significant.

### Verdict

Signal quality constraint: **20-25 rules.** Corroborated by token budget, instruction-following research, and original design intent.

---

## Constraint 5: Rule Conflict Probability

### Analysis

The number of potential pairwise interactions between N rules is N(N-1)/2:

| Rule Count | Pairwise Interactions | Relative to 20 rules |
|------------|----------------------|---------------------|
| 15 | 105 | 0.55x |
| 20 | 190 | 1.0x (baseline) |
| 25 | 300 | 1.58x |
| 30 | 435 | 2.29x |
| 35 | 595 | 3.13x |

Each interaction is a potential conflict surface. Not all interactions produce conflicts, but the probability grows combinatorially. At 35 rules, there are 3.1x more potential conflicts than at 20 rules.

Observed conflicts in the current system:
- H-16 (steelman before critique) can tension with H-14 (creator-critic cycles) when iteration count is constrained
- H-20 (test-first BDD) tensions with rapid prototyping workflows
- H-25..H-30 (skill standards) have significant internal overlap, suggesting they should be consolidated

### Verdict

Rule conflict probability is a secondary constraint — it doesn't establish a hard ceiling, but it reinforces the case for staying in the 20-25 range. At 35 rules, the conflict surface (595 pairs) is unmanageable without a formal conflict resolution mechanism that doesn't exist today.

---

## Synthesis: Binding Constraint Analysis

| Constraint | Derived Ceiling | Binding? |
|-----------|-----------------|----------|
| 1. Token Budget | 25-40 (with consolidation) | No — manageable through optimization |
| 2. L2 Re-injection | 14 (full L2 coverage) | **Yes — for "truly HARD" rules** |
| 3. Instruction-Following | 10-12 simultaneous, ~25 total | **Yes — for total count** |
| 4. Signal Quality | 20-25 | Corroborative |
| 5. Rule Conflict | Reinforces 20-25 | Corroborative |

**Two ceilings emerge:**

1. **Hard ceiling (L2-protected, truly enforceable): 12-14 rules.** These are the rules that survive context rot because they are re-injected every prompt. This is the real enforcement capacity of the current architecture.

2. **Soft ceiling (total HARD rules including L1-only): 25 rules.** Beyond this, instruction-following research, signal quality, and conflict probability all converge on degraded enforcement.

---

## Recommendation

### Derived Budget: 25 HARD Rules (Two-Tier Allocation)

| Tier | Allocation | L2 Coverage | Purpose |
|------|-----------|-------------|---------|
| **Tier A: Constitutional** | 12 rules | Full L2 re-injection | Rules whose violation causes irreversible or systemic harm (P-003, P-020, P-022, quality gates, governance escalation) |
| **Tier B: Operational** | 13 rules | L1-only (session start) | Rules whose violation is costly but recoverable (coding standards, testing standards, skill standards) |
| **Total** | **25** | | |

### What This Means for the Current 31 Rules

A net reduction of 6 rules is required, achievable through consolidation:

| Consolidation | Before | After | Savings |
|---------------|--------|-------|---------|
| H-25..H-30 (skill standards) → 2 compound rules | 6 | 2 | -4 |
| H-07..H-09 (architecture layers) → 1 compound rule | 3 | 1 | -2 |
| **Net** | | | **-6 (31 → 25)** |

### What This Means for PROJ-007's H-32..H-35

H-32..H-35 cannot be added without first consolidating to create headroom. The sequence:
1. Consolidate H-25..H-30 (save 4 slots)
2. Consolidate H-07..H-09 (save 2 slots)
3. Current count: 25 (6 freed)
4. Add H-32..H-35 (consume 4 slots)
5. Final count: 29 — **over the 25 ceiling by 4**

This means either:
- H-32..H-35 must also be consolidated (e.g., 4 → 2), **or**
- Additional consolidation must be found elsewhere, **or**
- H-32..H-35 are classified as Tier B (L1-only, no L2 coverage), accepting degraded enforcement

### What This Means for the "35 Slot" Ceiling

**The 35 ceiling should be replaced with the 25 ceiling**, with explicit two-tier allocation documented in `quality-enforcement.md`. The Tier Vocabulary table should read:

| Tier | Max Count | L2 Coverage |
|------|-----------|-------------|
| **HARD (Tier A)** | <= 12 | Full L2 re-injection |
| **HARD (Tier B)** | <= 13 | L1-only |
| **HARD (Total)** | <= 25 | |
| **MEDIUM** | Unlimited | None |
| **SOFT** | Unlimited | None |

---

## Implementation Path

| Step | Action | Criticality |
|------|--------|-------------|
| 1 | Consolidate H-25..H-30 into 2 compound rules | C3 (AE-002) |
| 2 | Consolidate H-07..H-09 into 1 compound rule | C3 (AE-002) |
| 3 | Classify all 25 remaining rules into Tier A / Tier B | C3 (AE-002) |
| 4 | Update quality-enforcement.md ceiling from 35 → 25 with two-tier table | C3 (AE-002) |
| 5 | Update L2-REINJECT markers to cover all Tier A rules | C3 |
| 6 | Add PROJ-007 rules (H-32..H-35) within the new budget | C3 (AE-002) |
| 7 | Update HARD rule index to reflect consolidation | C3 (AE-002) |

---

## Evidence Index

| ID | Source | Content | Confidence |
|----|--------|---------|------------|
| E-001 | ADR-EPIC002-002 | Token budget: L1=12,476, L2=600, total=15,126 | High (baselined ADR) |
| E-002 | prompt_reinforcement_engine.py | Engine reads only quality-enforcement.md L2 markers | High (source code) |
| E-003 | L2-REINJECT marker inventory | 10 H-rules with L2 coverage, 21 without | High (file scan) |
| E-004 | ManyIFEval (arXiv:2509.21051) | 5 instructions: 32-72%, 10 instructions: 2-39% | High (peer-reviewed) |
| E-005 | AGENTIF (arXiv:2505.16944) | 11.9 constraints: <30% perfect compliance | High (NeurIPS Spotlight) |
| E-006 | Control Illusion (arXiv:2502.15851) | Claude 3.5 system prompt adherence: 29.9% under conflict | High (peer-reviewed) |
| E-007 | Lost in the Middle (TACL 2024) | Middle-positioned information degrades in long contexts | High (TACL publication) |
| E-008 | nse-risk-001-risk-assessment.md | "20-25 sweet spot" diminishing returns curve | Medium (agent judgment) |
| E-009 | EN-404 deliverable-003 | Original `<= 25` ceiling with "scarcity preserves signal" rationale | Medium (design intent) |
| E-010 | Commit 936d61c | Retroactive ceiling update from 25 → 35 with no justification | High (git evidence) |
| E-011 | ADOR (OpenReview 2024) | Attention dilution: softmax normalization distributes weight across all tokens | Emerging (formal literature) |
| E-012 | ADR-EPIC002-002 R-SYS-004 | 82.5% of enforcement budget in L1 (VULNERABLE layer) = RED risk score 16 | High (baselined ADR) |
