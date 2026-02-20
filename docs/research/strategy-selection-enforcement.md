# Strategy Selection & Enforcement (ADRs)

> Two architecture decision records documenting the selection of Jerry's 10 adversarial strategies and the design of its 5-layer enforcement architecture — both with full evidence trails, sensitivity analysis, and user ratification.

---

## Key Findings

- **10 strategies selected from 15** using a 6-dimension weighted composite scoring framework with 12-configuration sensitivity analysis — 9/10 selections are robust across all weight configurations
- **5 excluded strategies carry 3 RED risks** (context window); all selected strategies have zero RED risks
- **5-layer enforcement architecture** addresses context rot through defense-in-depth: behavioral rules → prompt re-injection → deterministic gating → output inspection → CI verification
- **Total enforcement budget: ~15,100 tokens** (7.6% of 200K context) — down from 25,700 tokens through optimization
- **Token-efficient strategy portfolio**: typical Layer 2 review costs 12,000-18,000 tokens with no selected strategy exceeding 10,000 individually

---

## ADR-EPIC002-001: Selection of 10 Adversarial Strategies

The formal architecture decision record for selecting Jerry's adversarial strategy portfolio. Ratified by the user on 2026-02-13 per P-020 (User Authority), with a directive to revisit cross-model LLM involvement in a future epic.

??? note "Methodology"
    The selection followed a 4-task evidence pipeline:

    1. **TASK-001**: Defined 6-dimension weighted evaluation framework
        - Quality Outcome: Effectiveness (25%) + LLM Applicability (25%) = 50%
        - Portfolio Fitness: Complementarity (15%) + Implementation Complexity (15%) = 30%
        - User Experience: Cognitive Load (10%) + Differentiation (10%) = 20%
    2. **TASK-002**: Risk assessment — 105 assessments (15 strategies × 7 categories) → 3 RED, 18 YELLOW, 84 GREEN
    3. **TASK-003**: Architecture trade study — Pugh Matrix, token budget modeling, composition matrix
    4. **TASK-004**: Composite scoring, rank ordering, 12-configuration sensitivity analysis

    Three options were considered: Top 10 by composite score (chosen), Top 8 + 2 diversity picks (rejected), All 15 with tiered activation (rejected — user directed revisiting in future epic).

??? abstract "Key Data: The 10 Selected Strategies"
    | Rank | ID | Strategy | Score | Family |
    |------|-----|----------|-------|--------|
    | 1 | S-014 | LLM-as-Judge | 4.40 | Iterative Self-Correction |
    | 2 | S-003 | Steelman Technique | 4.30 | Dialectical Synthesis |
    | 3 | S-013 | Inversion Technique | 4.25 | Structured Decomposition |
    | 4 | S-007 | Constitutional AI Critique | 4.15 | Iterative Self-Correction |
    | 5 | S-002 | Devil's Advocate | 4.10 | Role-Based Adversarialism |
    | 6 | S-004 | Pre-Mortem Analysis | 4.10 | Role-Based Adversarialism |
    | 7 | S-010 | Self-Refine | 4.00 | Iterative Self-Correction |
    | 8 | S-012 | FMEA | 3.75 | Structured Decomposition |
    | 9 | S-011 | Chain-of-Verification | 3.75 | Structured Decomposition |
    | 10 | S-001 | Red Team Analysis | 3.35 | Role-Based Adversarialism |

    **Sensitivity analysis**: 9/10 stable across all 12 weight configurations (threshold: 8/10). Only S-001 at rank 10 is sensitive in 2 configurations where S-006 (ACH) would replace it.

    **5 Excluded** (all with RED risks or insufficient composite score): S-005 Dialectical Inquiry, S-006 ACH, S-008 Socratic Method, S-009 Multi-Agent Debate, S-015 Prompt Adversarial Examples.

[:octicons-link-external-16: Full ADR (480 lines)](https://github.com/geekatron/jerry/blob/main/projects/PROJ-001-oss-release/decisions/ADR-EPIC002-001-strategy-selection.md)

---

## ADR-EPIC002-002: Enforcement Vector Prioritization

The companion ADR designing Jerry's 5-layer enforcement architecture to address the fundamental problem: rules loaded at session start degrade as context fills, with effectiveness dropping to 40-60% at 50K+ tokens.

??? note "Methodology"
    The decision was informed by a comprehensive evaluation of **62 enforcement vectors** across 7 families, cataloged in EN-401. Five user-confirmed priorities governed the selection:

    1. Authoritative data source (EN-401 Revised Catalog v1.1)
    2. Prioritize LLM-portable vectors (38 of 62); support Windows adaptations
    3. Token budget envelope: ~25,700 tokens → optimized to ~12,476 tokens
    4. Reference adversary model for bypass resistance
    5. Prioritize context-rot-resilient vectors (CRR as highest-weighted criterion at 25%)

??? abstract "Key Data: 5-Layer Architecture"
    | Layer | Timing | Function | Context Rot Resistance | Tokens |
    |-------|--------|----------|----------------------|--------|
    | L1 | Session start | Behavioral foundation via `.claude/rules/` | Vulnerable | ~12,500 |
    | L2 | Every prompt | Re-inject critical rules (L2-REINJECT tags) | **Immune** | ~600/prompt |
    | L3 | Before tool calls | Deterministic gating (AST checks) | **Immune** | 0 |
    | L4 | After tool calls | Output inspection, self-correction | Mixed | 0-1,350 |
    | L5 | Commit/CI | Post-hoc verification (pre-commit hooks) | **Immune** | 0 |

    **Key insight**: Layers L2, L3, and L5 are immune to context rot because they operate outside the LLM's context window (L3/L5 are deterministic; L2 is re-injected fresh each turn). This provides defense-in-depth even when L1 rules degrade.

[:octicons-link-external-16: Full ADR (713 lines)](https://github.com/geekatron/jerry/blob/main/projects/PROJ-001-oss-release/decisions/ADR-EPIC002-002-enforcement-architecture.md)

---

## Related Research

- [Adversarial Strategy Catalog](adversarial-strategy-catalog.md)
- [Adversarial Quality Deep Dives](adversarial-deep-dives.md)
- [Single vs. Multi-Agent Analysis](single-vs-multi-agent.md)
- [Governance & Constitutional AI](governance-constitutional-ai.md)
