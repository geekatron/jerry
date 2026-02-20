# Adversarial Quality Deep Dives

> Trade studies, risk registers (FMEA), scoring methodology, and the strategy selection decision tree — the supporting research behind Jerry's adversarial quality framework.

---

## Key Findings

- **NASA SE trade study methodology** applied to adversarial strategy selection: Pugh Matrix scoring across 6 weighted dimensions with sensitivity analysis
- **105 risk assessments** (15 strategies × 7 categories) produced 3 RED, 18 YELLOW, 84 GREEN ratings — context window is the dominant systemic risk
- **Composite scoring framework** scored all 15 strategies on 6 dimensions with deterministic tiebreaking and 12-configuration sensitivity analysis
- **Deterministic decision tree** maps criticality levels (C1-C4) to required strategy sets with auto-escalation rules and token budget adaptation

---

## Architecture Trade Study: Adversarial Strategy Selection

NASA SE Trade Study Report (TSR) format applied to the adversarial strategy selection problem — Pugh Matrix analysis, token budget modeling, and composition matrix.

??? note "Methodology"
    Applied NASA SE weighted additive scoring with Pugh Matrix against all 15 candidate strategies. Assessed P-003 (no recursive subagents) compliance, token budget per strategy, and inter-strategy composition (synergy/tension/conflict pairs).

??? abstract "Key Data"
    - **Pugh Matrix Tier 1** (architectural winners): S-003, S-010, S-013, S-014, S-004 — all in the final top 10
    - **Token efficiency**: Ultra-Low tier (S-003: 1,600 tokens, S-010: 2,000, S-014: 2,000, S-013: 2,100) vs. High tier (S-009: 15,000-30,000)
    - **Composition matrix**: 16 SYN pairs, 7 TEN pairs, 0 CON pairs across all 15 strategies
    - **P-003 compliance**: All 15 structurally compliant; S-009 carries implementation risk ("COMPLIANT WITH CARE")

[:octicons-link-external-16: Trade Study (800 lines)](https://github.com/geekatron/jerry/blob/main/projects/PROJ-001-oss-release/work/EPIC-002-quality-enforcement/FEAT-004-adversarial-strategy-research/EN-302-strategy-selection-framework/deliverable-003-trade-study.md)

---

## Risk Register: Adversarial Strategy Adoption

FMEA-style risk assessment across all 15 adversarial strategies with severity, occurrence, and detection scoring.

??? note "Methodology"
    Applied FMEA methodology with 7 risk categories per strategy (105 total assessments). Risk scoring uses Severity × Likelihood × Detection matrix with RED/YELLOW/GREEN classification. NASA risk management standards referenced.

??? abstract "Key Data"
    - **Risk portfolio**: 3 RED | 18 YELLOW | 84 GREEN across 105 assessments
    - **All 3 RED risks are context window risks**: S-009 (score 20), S-015 (score 16), S-005 (score 16)
    - **Lowest-risk strategies**: S-013 (15/175), S-003 (16/175), S-010 (23/175)
    - **Highest-risk strategies**: S-015 (56/175), S-009 (48/175), S-007 (45/175)
    - **Systemic risk DA-002**: Shared model bias — six strategies rely on self-critique with correlated failure modes

[:octicons-link-external-16: Risk Register (798 lines)](https://github.com/geekatron/jerry/blob/main/projects/PROJ-001-oss-release/work/EPIC-002-quality-enforcement/FEAT-004-adversarial-strategy-research/EN-302-strategy-selection-framework/deliverable-002-risk-assessment.md)

---

## Composite Scoring and Top-10 Selection

The scoring methodology that ranked all 15 strategies and produced the final top-10 selection with boundary analysis and epistemic limitations.

??? note "Methodology"
    15 strategies scored on 6 weighted dimensions (Effectiveness 25%, LLM Applicability 25%, Complementarity 15%, Implementation Complexity 15%, Cognitive Load 10%, Differentiation 10%). 12-configuration sensitivity analysis tested robustness. Deterministic tiebreaking: D1 > D2 > D3 > qualitative assessment.

??? abstract "Key Data"
    - **Score range**: 4.40 (S-014 LLM-as-Judge) to 2.70 (S-009 Multi-Agent Debate, S-015 PAE)
    - **Clear cluster separation**: 7 strategies at 4.00-4.40, 3 at 3.35-3.75, 5 at 2.70-3.25
    - **Sensitivity**: 9/10 stable across all 12 weight configurations (threshold: 8/10)
    - **Only sensitive boundary**: S-001 (rank 10) vs. S-006 (rank 12) — swaps in 2 of 12 configurations

[:octicons-link-external-16: Scoring & Selection (774 lines)](https://github.com/geekatron/jerry/blob/main/projects/PROJ-001-oss-release/work/EPIC-002-quality-enforcement/FEAT-004-adversarial-strategy-research/EN-302-strategy-selection-framework/deliverable-004-scoring-and-selection.md)

---

## Strategy Selection Decision Tree

Deterministic decision tree mapping context (criticality, artifact type, available budget) to the required strategy set with auto-escalation rules.

??? abstract "Key Data"
    - **4 criticality levels** (C1-C4) with monotonically increasing strategy requirements
    - **Auto-escalation rules**: governance files → auto-C4, `.context/rules/` → auto-C3, new ADR → auto-C3
    - **Token budget adaptation**: strategies can be dropped in priority order when budget is constrained
    - **Platform adaptation**: guidance for different Claude model tiers

[:octicons-link-external-16: Decision Tree (661 lines)](https://github.com/geekatron/jerry/blob/main/projects/PROJ-001-oss-release/work/EPIC-002-quality-enforcement/FEAT-004-adversarial-strategy-research/EN-303-situational-applicability-mapping/TASK-004-decision-tree.md)

---

## Related Research

- [Adversarial Strategy Catalog](adversarial-strategy-catalog.md)
- [Strategy Selection & Enforcement (ADRs)](strategy-selection-enforcement.md)
- [Single vs. Multi-Agent Analysis](single-vs-multi-agent.md)
