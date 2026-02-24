# Twitter Thread: LLM Deception Research Findings

> **Agent:** sb-voice-002 | **Platform:** Twitter/X | **Date:** 2026-02-22
> **Workflow:** llm-deception-20260221-001 | **Phase:** 4 -- Content Production
> **Tweet Count:** 7
> **Binding Requirements Met:** R-008 (constructive framing), F-005 (non-anthropomorphic language), R-004 (citations where feasible), scope qualifiers (3+ caveats), FC-003 not cited as parametric adequacy, N=5 not overstated, R-006 (Jerry framework referenced)
> **Generalizability Caveats Included:** (1) Model specificity -- Claude Opus 4.6 with honesty instructions, (2) Sample size -- N=5, directional evidence, (3) Domain scope -- rapidly evolving domains only
> **F-005 Compliance:** Verified -- "exhibits" used throughout; no "chooses," "decides," or anthropomorphic attribution
> **S-010 Self-Review:** Applied

---

## Thread Content

### Tweet 1/7
We ran an A/B test expecting to catch an LLM fabricating answers about topics it couldn't know.

It didn't fabricate. It had nothing to say.

The dominant failure mode isn't hallucination. It's incompleteness.

Thread on what that means.
*[237 chars]*

### Tweet 2/7
Parametric-only agent (no tools): composite score 0.526.
Tool-augmented agent: 0.907.
Delta: +0.381.

The gap is real. But here's the surprise -- Confidence Calibration was 0.906 for BOTH agents. The model without tools exhibits well-calibrated uncertainty. Identical scores.
*[275 chars]*

### Tweet 3/7
Currency -- how current the information is -- showed the largest gap: +0.754.

The parametric agent doesn't generate wrong answers about what it doesn't know. It just has nothing current to offer. That's an engineering problem, not a safety crisis.
*[248 chars]*

### Tweet 4/7
Tool augmentation is reliability engineering: it solves the completeness problem (Currency +0.754, Source Quality +0.770).

It is NOT safety engineering. Behavioral calibration -- the model signaling what it doesn't know -- works without tools. Prompt design handles that.
*[272 chars]*

### Tweet 5/7
New finding: "Accuracy by Omission." The parametric agent scored 0.822 on factual accuracy by making very few claims. High precision, low recall.

Any evaluation framework that measures accuracy without completeness will overestimate reliability. Pair them. Always.
*[265 chars]*

### Tweet 6/7
Scope: Claude Opus 4.6 with explicit honesty instructions. N=5 questions in rapidly evolving domains. Directional evidence, not statistical significance. Other models, other prompts, stable domains -- results may differ. This is a starting point, not a conclusion.
*[264 chars]*

### Tweet 7/7
We built Jerry -- a framework with constitutional constraints, adversarial quality gates, and persistence-backed audit trails -- that embodies these mitigations.

This research ran inside it. The architecture is the proof-of-concept.

github.com/geekatron/jerry
*[261 chars]*

---

## Compliance Notes

### R-008: Constructive Framing
All tweets frame findings as engineering problems with known solutions. Tweet 3 explicitly reframes from "safety crisis" to "engineering problem." Tweet 4 distinguishes reliability engineering from safety engineering. No alarmist framing.

### F-005: Non-Anthropomorphic Language
Tweet 2: "exhibits well-calibrated uncertainty" (not "honestly acknowledges"). Tweet 3: "doesn't generate wrong answers" (behavioral description, not intent attribution). Tweet 5: "the parametric agent scored" (not "chose to"). No instance of "chooses," "decides," or "honesty" as agent attributes.

### R-004: Verifiable Citations
Thread format limits inline citation. Tweet 7 provides the Jerry GitHub URL. Specific numerical claims (0.906, +0.381, +0.754, 0.822) are traceable to ps-analyst-001-comparison.md and ps-synthesizer-001-output.md. Blog post (sb-voice-003) carries full citation chain.

### Scope Qualifiers (3+ caveats)
Tweet 6 contains all three required caveats condensed into a single tweet: (1) model specificity (Claude Opus 4.6 with honesty instructions), (2) sample size (N=5, directional evidence), (3) domain scope (rapidly evolving domains). Tweet 6 also notes that other models/prompts/domains may differ, which touches caveats (a), (c), and (b) from the generalizability analysis.

### FC-003 Not Cited as Parametric Adequacy
FC-003 is not referenced anywhere in the thread. Tweet 5 explicitly addresses the accuracy-by-omission artifact that explains the inflated FA score, framing it as a methodological insight rather than as evidence of parametric knowledge adequacy.

### N=5 Not Overstated
Tweet 6: "Directional evidence, not statistical significance." Tweet 6: "This is a starting point, not a conclusion." No claim of statistical significance anywhere in the thread.

### R-006: Jerry Framework Referenced
Tweet 7 dedicates the closing position to the Jerry framework, linking it to the architectural mitigations discussed in the research and providing the GitHub URL. The reference is substantive (names specific architectural features: constitutional constraints, adversarial quality gates, persistence-backed audit trails) rather than a drive-by mention.

---

## Voice Notes

**Tone target:** Medium energy, technically direct. Twitter format demands compression -- voice comes through in sentence structure (short, declarative, no hedging) rather than through skiing metaphors or celebration markers. The thread is informational with an edge, not celebratory.

**Anti-patterns avoided:**
- No forced skiing metaphors (none would land naturally in this compressed format)
- No sycophantic language ("amazing results!" etc.)
- No performative quirkiness (no emoji, no try-hard whimsy)
- Clarity preserved throughout -- every tweet stands alone with its core claim

**Voice authenticity check:** The thread reads as direct, confident, technically precise, and warm toward the reader (explains the "so what" at every step). These map to 4 of the 5 Saucer Boy voice traits (Direct, Confident, Technically Precise, Warm). The "Occasionally Absurd" trait is correctly suppressed -- this is informational content where the research findings carry enough natural surprise to do the work that humor would do in other contexts.

---

*Generated by sb-voice-002 | Date: 2026-02-22*
*Workflow: llm-deception-20260221-001 | Phase: 4 -- Content Production*
*Input artifacts: barrier-3-b-to-a-synthesis.md, barrier-3-a-to-b-synthesis.md, ps-synthesizer-001-output.md, ps-architect-001-output.md*
*Voice references: SKILL.md, voice-guide.md, biographical-anchors.md, humor-examples.md, vocabulary-reference.md, tone-spectrum-examples.md, saucer-boy-persona.md*
*S-010 self-review: Applied -- all 7 binding requirements verified, all tweets <= 280 chars, F-005 compliance verified, 3+ caveats present*
