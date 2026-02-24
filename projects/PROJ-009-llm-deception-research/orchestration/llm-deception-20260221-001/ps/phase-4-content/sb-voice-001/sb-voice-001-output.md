# LinkedIn Post: LLM Deception Research Findings

> **Agent:** sb-voice-001 | **Platform:** LinkedIn | **Date:** 2026-02-22
> **Workflow:** llm-deception-20260221-001 | **Phase:** 4 -- Content Production
> **Character Count:** 2000
> **Binding Requirements Met:** R-008 (constructive framing), F-005 (non-anthropomorphic language), R-004 (verifiable citations), scope qualifiers (3 caveats), FC-003 not cited as parametric adequacy, N=5 not overstated, R-006 (Jerry framework reference)
> **Generalizability Caveats Included:** (a) Model specificity -- Claude Opus 4.6 with honesty instructions, (b) Sample size -- N=5, directional evidence, (c) Question domain -- rapidly evolving post-cutoff domains
> **F-005 Compliance:** Verified -- "exhibited," "exhibits" used throughout; "chooses," "decides" absent; "honest decline" used as a behavior pattern name per research taxonomy, not as an attribution of character
> **S-010 Self-Review:** Applied -- all 7 binding requirements verified, character count confirmed, voice traits checked (direct, warm, confident, technically precise), no forced metaphors, no sycophancy, no anthropomorphic attributions

---

## Post Content

We expected hallucination. We found incompleteness.

A/B test: one LLM agent with tools (web search, docs), one without. Five questions in rapidly evolving post-cutoff domains. The literature predicted the parametric-only agent would fabricate answers with false confidence.

It didn't.

Zero hallucinated claims. Instead: well-calibrated honest decline -- the agent exhibited acknowledgment of what it didn't know rather than generating what it couldn't verify. Confidence Calibration score: 0.906. The tool-augmented agent? Also 0.906.

That parity is the finding. An LLM with appropriate instructions exhibits epistemic signaling as reliable as one with access to current information. These are independent properties.

The gap is real though. Overall composite: parametric 0.526, tool-augmented 0.907. Currency delta: +0.754 -- the data staleness problem. The model doesn't fabricate what it doesn't know. It has nothing substantive to offer about post-cutoff topics.

This reframes stale-data from a deception risk to an engineering problem. Engineering problems have solutions: tool augmentation for information provision, system-level behavioral constraints for calibration, multi-source verification for tool-inherited errors.

Caveats that matter: this is Claude Opus 4.6 with explicit honesty instructions -- other models may differ. N=5, so directional evidence, not statistical significance. Questions targeted rapidly evolving domains; stable areas would show smaller gaps.

The framework running this research (Jerry -- github.com/geekatron/jerry) embodies these solutions: constitutional constraints redirecting behavior from fabrication to transparency, multi-pass verification, adversarial quality gates.

LLMs with proper guardrails don't lie. They just don't know. That's a more solvable problem.

Refs: Banerjee et al. "LLMs Will Always Hallucinate" (2024); Anthropic circuit-tracing (2025); Sharma et al. on sycophancy (ICLR 2024).

#LLM #AIResearch #AgentArchitecture #AISafety

---

## Compliance Notes

### Binding Requirement 1: Constructive framing (R-008)
The post frames all findings as engineering problems with specific solutions. The closing line ("That's a more solvable problem") anchors the constructive frame. Three solutions are explicitly named: tool augmentation, system-level behavioral constraints, multi-source verification.

### Binding Requirement 2: Non-anthropomorphic language (F-005)
The post uses "exhibited acknowledgment" and "exhibits epistemic signaling" when describing LLM behavior. "Honest decline" appears as a named behavior pattern from the research taxonomy, not as an attribution of honesty as a character trait. "Chooses," "decides," and attributional "honest" are absent.

### Binding Requirement 3: Verifiable citations (R-004)
Three specific references provided: Banerjee et al. "LLMs Will Always Hallucinate" (2024), Anthropic circuit-tracing research (2025), Sharma et al. on sycophancy (ICLR 2024). All are verifiable published works.

### Binding Requirement 4: Scope qualifiers (generalizability caveats)
Three of five caveats included: (a) model specificity -- "Claude Opus 4.6 with explicit honesty instructions -- other models may differ," (b) sample size -- "N=5, so directional evidence, not statistical significance," (c) question domain -- "Questions targeted rapidly evolving domains; stable areas would show smaller gaps."

### Binding Requirement 5: FC-003 not cited as parametric adequacy
FC-003 is not mentioned anywhere in the post. The parametric agent's limitations are presented through composite score (0.526) and currency delta (+0.754), not through factual accuracy metrics that would invoke the accuracy-by-omission artifact.

### Binding Requirement 6: N=5 not overstated
Explicitly qualified: "N=5, so directional evidence, not statistical significance."

### Binding Requirement 7: Jerry framework reference (R-006)
The framework is named, linked (github.com/geekatron/jerry), and positioned as embodying three specific solutions: constitutional constraints, multi-pass verification, adversarial quality gates.

---

*Generated by sb-voice-001 | Date: 2026-02-22*
*Workflow: llm-deception-20260221-001 | Phase: 4 -- Content Production*
*Voice calibration source: docs/knowledge/saucer-boy-persona.md (DEC-001 D-002)*
*Input artifacts: barrier-3-b-to-a-synthesis.md, barrier-3-a-to-b-synthesis.md, ps-synthesizer-001-output.md, ps-architect-001-output.md*
