# Governance & Constitutional AI

> The Jerry Constitution implements Constitutional AI for LLM agent governance, drawing on Anthropic, OpenAI, and DeepMind prior art. Progressive enforcement from advisory to hard constraints, with behavior tests for verification.

---

## Key Findings

- **Constitutional AI pattern** applied to LLM agent governance: agents self-evaluate against declarative principles rather than procedural rules
- **13+ principles** organized across core behavior (truth, persistence, provenance), safety constraints (no recursive subagents, user authority, no deception), and operational standards
- **Progressive enforcement model**: Advisory → Soft → Medium → Hard — enabling graduated compliance rather than binary pass/fail
- **Behavior test suite** provides verifiable compliance scenarios for each constitutional principle
- **Prior art synthesis** from Anthropic (Constitutional AI), OpenAI (Model Spec), and Google DeepMind (Frontier Safety Framework)

---

## Jerry Constitution v1.0

The foundational governance document establishing behavioral principles for all agents operating within the Jerry Framework. Rather than encoding rules procedurally, the Constitution follows the Constitutional AI pattern where agents self-critique against explicit written principles.

??? note "Design Philosophy"
    The Constitution follows four design principles:

    1. **Principles over procedures** (declarative > imperative) — agents understand *why*, not just *what*
    2. **Self-critique and revision capability** — agents can evaluate their own output against principles
    3. **Transparency and inspectability** — all principles are human-readable and auditable
    4. **Progressive enforcement** — graduated from advisory (suggest compliance) through soft (log violations), medium (block with override), to hard (block without override)

    This draws directly on:
    - [Anthropic Constitutional AI](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback) — self-critique against written principles
    - [OpenAI Model Spec](https://model-spec.openai.com/2025-12-18.html) — "models should be useful, safe, and aligned"
    - [Google DeepMind Frontier Safety Framework](https://deepmind.google/discover/blog/introducing-the-frontier-safety-framework/) — graduated safety levels

??? abstract "Key Data: Core Principles"
    | ID | Principle | Category | Enforcement |
    |----|-----------|----------|-------------|
    | P-001 | Truth and Accuracy | Core | Soft |
    | P-002 | File Persistence | Core | Medium |
    | P-003 | No Recursive Subagents | Safety | **Hard** |
    | P-004 | Explicit Provenance | Core | Soft |
    | P-005 | Graceful Degradation | Operational | Soft |
    | P-011 | Evidence-Based Decisions | Core | Medium |
    | P-020 | User Authority | Safety | **Hard** |
    | P-022 | No Deception | Safety | **Hard** |
    | P-043 | Mandatory Disclaimer | Transparency | Medium |

    **Three HARD constraints** (cannot be overridden): P-003 (no recursive subagents), P-020 (user authority), P-022 (no deception). These form the inviolable foundation of agent behavior.

??? abstract "Key Data: Enforcement Levels"
    | Level | Behavior | Override | Example |
    |-------|----------|----------|---------|
    | **Advisory** | Suggest compliance; log non-compliance | Always | "Consider citing sources" |
    | **Soft** | Warn on violation; continue with notice | Documented justification | Citation requirements |
    | **Medium** | Block action; allow user override | User explicit approval | File persistence mandate |
    | **Hard** | Block action; no override possible | Cannot be overridden | No recursive subagents |

[:octicons-link-external-16: Jerry Constitution v1.0 (426 lines)](https://github.com/geekatron/jerry/blob/main/docs/governance/JERRY_CONSTITUTION.md)

---

## Behavior Tests

The verification companion to the Constitution — concrete test scenarios that validate whether agents comply with each constitutional principle.

??? abstract "Key Data"
    - 463 lines of behavioral test specifications
    - Test scenario for each constitutional principle (BHV-001 through BHV-0XX)
    - Verifiable pass/fail criteria for agent behavior
    - Enables automated and manual compliance checking

[:octicons-link-external-16: Behavior Tests (463 lines)](https://github.com/geekatron/jerry/blob/main/docs/governance/BEHAVIOR_TESTS.md)

---

## Agent Conformance Rules

The operational translation of constitutional principles into agent-level conformance requirements.

??? abstract "Key Data"
    - 246 lines of conformance specifications
    - Maps constitutional principles to concrete agent behaviors
    - Defines conformance levels per agent type
    - Integrates with the `/adversary` skill's S-007 (Constitutional AI Critique) strategy

[:octicons-link-external-16: Agent Conformance Rules (246 lines)](https://github.com/geekatron/jerry/blob/main/docs/governance/AGENT_CONFORMANCE_RULES.md)

---

## Related Research

- [Strategy Selection & Enforcement (ADRs)](strategy-selection-enforcement.md)
- [Adversarial Strategy Catalog](adversarial-strategy-catalog.md)
- [Skill Compliance Framework](skill-compliance-framework.md)
